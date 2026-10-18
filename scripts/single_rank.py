"""Rank the single-transit search (results/single[_inverted]/*.json):
1. event-level cuts (SNR, depth, background, baseline step, flat bottom, momentum dumps, noise sanity);
2. field control: events that coincide in time with events on other stars of the same sector/camera/CCD are scattered-light
   systematics and are rejected (time bins of 0.25 d; a bin is "systematic" if >= max(3, 4x the median per-bin count) stars have events);
3. per-star matching: >= 2 surviving events with consistent depth (3 sigma) and duration (x1.6) -> duotransit candidate with the set of
   period aliases P = dt/n allowed by the kept data (a predicted epoch on >= 60 % covered data with no dip excludes n);
4. tables: events_all.csv, events_pass.csv, duotransits.csv, singles_top.csv in the results directory.
Usage: python -I single_rank.py [--dir results/single] [--snr 7]"""
import sys, os, glob, json, argparse, warnings; warnings.filterwarnings("ignore"); sys.path.insert(0, "/Users/fernando/Desktop/NASA/scripts")
import numpy as np, pandas as pd
ROOT = "/Users/fernando/Desktop/NASA"

def event_cuts(df, snr=7.0):
    c = (df.snr >= snr) & (df.depth > 0) & (df.depth < 0.1)
    c &= df.bkg_ratio.isna() | ((df.bkg_ratio > 0.5) & (df.bkg_ratio < 2.0))
    c &= df.pre_post_sig.isna() | (df.pre_post_sig.abs() < 4)
    c &= df.frac_below >= 0.8
    c &= df.dchi2_box_minus_v > -10          # box fits at least as well as a V (within 10 chi2) -> excludes most dumps/ramps
    c &= df.dump_dt_h > 1.0
    c &= df.sig_local < 0.02
    c &= df.bottom_ratio.isna() | (df.bottom_ratio > 0.4)
    return c

def field_control(df, bin_d=0.25):
    """Flag events whose time bin hosts events on a large fraction of the stars observed in the same sector/camera/CCD
    (>= max(3, 30 %) of the stars with any event on that CCD-sector) or sector-wide (>= max(5, 10 %) of stars in the sector).
    Thresholds are proportional so that crowded event lists do not flag everything; +-1 neighbouring bins of a flagged CCD bin are flagged."""
    df = df.copy(); df["tbin"] = np.floor(df.tc / bin_d).astype(int); df["field_flag"] = False; df["field_nstars"] = 0
    for (s, cam, ccd), g in df.groupby(["sector", "camera", "ccd"]):
        counts = g.groupby("tbin").tic.nunique(); nst = g.tic.nunique(); thr = max(3, 0.3 * nst)
        bad = set(counts[counts >= thr].index); bad |= {b + d for b in list(bad) for d in (-1, 1)}
        df.loc[g.index, "field_nstars"] = g.tbin.map(counts).values; df.loc[g.index[g.tbin.isin(bad)], "field_flag"] = True
    for s, g in df.groupby("sector"):
        counts = g.groupby("tbin").tic.nunique(); nbins = max((g.tc.max() - g.tc.min()) / bin_d, 1); mean = len(g) / nbins
        thr = max(4, mean + 3 * np.sqrt(mean)); bad = set(counts[counts >= thr].index); bad |= {b + d for b in list(bad) for d in (-1, 1)}
        df.loc[g.index[g.tbin.isin(bad)], "field_flag"] = True
    return df

_tcache = {}
def kept_times(tic):
    from single_transit_search import sector_files, load
    if tic not in _tcache: _tcache[tic] = np.concatenate([load(p)[0] for p in sector_files(tic)] or [np.array([])])
    return _tcache[tic]
def coverage(tic, tc, dur_d):
    """fraction of a +-dur/2 window around tc covered by kept cadences (loader policy), for alias exclusion."""
    t = kept_times(tic); n = np.sum(np.abs(t - tc) < dur_d / 2); return n / max(dur_d / (10 / 1440), 1)   # relative to 10-min cadence

def alias_set(tic, ev, all_ev, max_n=60):
    """ev: list of >=2 passing events (dict). Returns allowed periods from the two strongest events' separation."""
    ev = sorted(ev, key=lambda e: -e["snr"]); e1, e2 = ev[0], ev[1]; dt = abs(e1["tc"] - e2["tc"]); dur_d = max(e1["dur_h"], e2["dur_h"]) / 24
    others = [e["tc"] for e in all_ev]
    allowed = []
    for n in range(1, max_n + 1):
        P = dt / n
        if P < 2 * dur_d: break
        ok = True; tested = 0
        for k in range(-300, 301):
            tp = min(e1["tc"], e2["tc"]) + k * P
            if any(abs(tp - e["tc"]) < dur_d for e in ev): continue
            cov = coverage(tic, tp, dur_d)
            if cov >= 0.6:
                tested += 1
                if not any(abs(tp - o) < dur_d for o in others): ok = False; break
        if ok: allowed.append(dict(n=n, P=round(P, 5), epochs_tested=tested))
    return allowed

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--dir", default=f"{ROOT}/results/single"); ap.add_argument("--snr", type=float, default=7.0); ap.add_argument("--no-alias", action="store_true"); a = ap.parse_args()
    rows = []; metas = {}
    for f in glob.glob(f"{a.dir}/[0-9]*.json"):
        r = json.load(open(f)); metas[r["tic"]] = r.get("meta", {})
        for e in r["events"]: rows.append(dict(tic=r["tic"], **e))
    df = pd.DataFrame(rows); print(f"targets {len(metas)}, raw events {len(df)}")
    for col in ("bkg_ratio", "pre_post_sig", "bottom_ratio", "dx", "dy", "cxy_err", "frac_flagged", "t_since_orbit_start"):
        if col in df: df[col] = pd.to_numeric(df[col], errors="coerce")
    df["pass_cuts"] = event_cuts(df, a.snr); print(f"events passing cuts: {df.pass_cuts.sum()} on {df[df.pass_cuts].tic.nunique()} stars")
    # star-level tier 1 (before field control, so eclipsing binaries do not poison the bins): obvious EBs/variables
    per_sec = df[df.pass_cuts].groupby(["tic", "sector"]).size(); tot = df[df.pass_cuts].groupby("tic").size()
    busy = set(per_sec[per_sec > 8].index.get_level_values(0)) | set(tot[tot > 30].index)
    df["star_ok"] = ~df.tic.isin(busy) & (df.depth < 0.05)
    print(f"tier-1 star cuts (<=8 events/sector, <=30 total, depth < 5 %): {(df.pass_cuts & df.star_ok).sum()} events on {df[df.pass_cuts & df.star_ok].tic.nunique()} stars; {len(busy)} EB/variable stars set aside")
    fc = field_control(df[df.pass_cuts & df.star_ok].copy())
    df["field_flag"] = False; df["field_nstars"] = np.nan; df.loc[fc.index, "field_flag"] = fc.field_flag.values; df.loc[fc.index, "field_nstars"] = fc.field_nstars.values
    # direct coincidence control: number of OTHER stars (any camera) with a passing event within +-0.1 d; compared with the
    # chance expectation for that sector (events in sector x 0.2 d / sector span); flagged if > max(5, 3 x expected)
    sub = df[df.pass_cuts & df.star_ok]; df["coinc_stars"] = np.nan; df["coinc_expected"] = np.nan
    for s_, g in sub.groupby("sector"):
        tcs = g.tc.values; tics = g.tic.values; span = max(g.tc.max() - g.tc.min(), 1.0); exp = (g.tic.nunique() - 1) * len(g) / g.tic.nunique() * 0.2 / span
        order = np.argsort(tcs); tcs_s = tcs[order]; tics_s = tics[order]
        co = np.array([len(set(tics_s[np.searchsorted(tcs_s, tc - 0.1):np.searchsorted(tcs_s, tc + 0.1)]) - {ti}) for tc, ti in zip(tcs, tics)])
        df.loc[g.index, "coinc_stars"] = co; df.loc[g.index, "coinc_expected"] = exp
    df["coinc_flag"] = df.coinc_stars > np.maximum(5, 3 * df.coinc_expected)
    df["pass"] = df.pass_cuts & df.star_ok & ~df.field_flag & ~df.coinc_flag
    print(f"coincidence control flagged {int((df.pass_cuts & df.star_ok & df.coinc_flag).sum())} events")
    print(f"after field control: {df['pass'].sum()} events on {df[df['pass']].tic.nunique()} stars (field-flagged: {int(df.field_flag.sum())})")
    # star-level tier 2 on the surviving events: a long-period transiting object gives <= 2-3 events per sector and few overall
    per_sec = df[df["pass"]].groupby(["tic", "sector"]).size(); tot = df[df["pass"]].groupby("tic").size()
    busy2 = set(per_sec[per_sec > 3].index.get_level_values(0)) | set(tot[tot > 10].index)
    pd.DataFrame(dict(tic=sorted(busy | busy2))).to_csv(f"{a.dir}/variables.csv", index=False)
    df.loc[df.tic.isin(busy2), "pass"] = False
    print(f"tier-2 star cuts (<=3 surviving events/sector, <=10 total): {df['pass'].sum()} events on {df[df['pass']].tic.nunique()} stars; {len(busy2)} more stars set aside")
    for k in ("tmag", "teff", "rad"): df[k] = df.tic.map(lambda t: metas.get(t, {}).get(k))
    df.to_csv(f"{a.dir}/events_all.csv", index=False); ok = df[df["pass"]].copy(); ok.to_csv(f"{a.dir}/events_pass.csv", index=False)
    # singles ranked
    singles = ok.sort_values("snr", ascending=False); singles.head(200).to_csv(f"{a.dir}/singles_top.csv", index=False)
    # duotransits
    duo = []
    for tic, g in ok.groupby("tic"):
        if len(g) < 2: continue
        g = g.sort_values("snr", ascending=False); e1 = g.iloc[0]
        mates = g.iloc[1:][(np.abs(g.iloc[1:].depth - e1.depth) < 3 * np.hypot(g.iloc[1:].depth_err, e1.depth_err)) & (np.maximum(g.iloc[1:].dur_h, e1.dur_h) / np.minimum(g.iloc[1:].dur_h, e1.dur_h) < 1.6) & (np.abs(g.iloc[1:].tc - e1.tc) > 1.0)]
        if len(mates) == 0: continue
        evs = [e1.to_dict()] + [m.to_dict() for _, m in mates.iterrows()]
        # policy: a candidate needs at least one event in unflagged data (flagged ramp events may support, not create, a candidate)
        if all((e.get("frac_flagged") or 0) > 0.5 for e in evs): continue
        # orbit-synchronous pairs (dt = k x 13.7 d with the same time-since-orbit-start) are scattered-light repeats, not transits
        def orbit_sync(a_, b_):
            dt = abs(a_["tc"] - b_["tc"]); k = round(dt / 13.7)
            return k >= 1 and abs(dt - 13.7 * k) < 1.0 and abs((a_.get("t_since_orbit_start") or 0) - (b_.get("t_since_orbit_start") or 0)) < 0.7 and dt < 30
        evs = [evs[0]] + [e for e in evs[1:] if not orbit_sync(evs[0], e)]
        if len(evs) < 2: continue
        allowed = [] if a.no_alias else alias_set(tic, evs, [e.to_dict() for _, e in g.iterrows()])
        duo.append(dict(tic=tic, n_events=len(evs), sectors=sorted(set(int(e["sector"]) for e in evs)), depth_ppm=round(float(np.mean([e["depth"] for e in evs]) * 1e6)), dur_h=round(float(np.mean([e["dur_h"] for e in evs])), 1),
                        snr_sum=round(float(np.sqrt(np.sum([e["snr"] ** 2 for e in evs]))), 1), dt_d=round(abs(evs[0]["tc"] - evs[1]["tc"]), 3), n_allowed=len(allowed), P_max=(allowed[0]["P"] if allowed else None), allowed=json.dumps(allowed[:12]),
                        tcs=json.dumps([round(e["tc"], 4) for e in evs]), max_frac_flagged=round(float(np.nanmax([e.get("frac_flagged") or 0 for e in evs])), 2), tmag=metas.get(tic, {}).get("tmag"), teff=metas.get(tic, {}).get("teff"), rad=metas.get(tic, {}).get("rad")))
    duo = pd.DataFrame(duo).sort_values("snr_sum", ascending=False) if duo else pd.DataFrame(); duo.to_csv(f"{a.dir}/duotransits.csv", index=False)
    pd.set_option("display.width", 250); print(f"\nduotransit candidates: {len(duo)}")
    if len(duo): print(duo.drop(columns=["allowed", "tcs"]).head(40).to_string(index=False))
    print("\ntop single events (stars with exactly one passing event):")
    one = ok.groupby("tic").filter(lambda g: len(g) == 1).sort_values("snr", ascending=False)
    print(one[["tic", "sector", "tc", "dur_h", "depth", "depth_err", "snr", "dchi2_box_minus_v", "bkg_ratio", "frac_flagged", "t_since_orbit_start", "field_nstars", "tmag", "teff", "rad"]].head(25).to_string(index=False))
