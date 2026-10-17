"""Population null: run the identical stitched BLS on INVERTED light curves (2 - F) for a random subset of targets.
Transits become bumps (undetectable as dips); systematics and noise remain. The distribution of inverted top-peak SDE
calibrates the threshold for the real search. Usage: TSEARCH_SOURCE=spoc|qlp python -I null_calibration.py --n 400 --workers 6"""
import sys, os, json, glob, re, argparse, warnings, time; sys.path.insert(0, "/Users/fernando/Desktop/NASA/scripts"); warnings.filterwarnings("ignore")
import numpy as np, pandas as pd
from search_pipeline import sector_files, load_lc, period_grid, bls_stats, bin_lc, year_of, SOURCE, OUT as SEARCH_OUT
from tsearch import detrend
OUT = SEARCH_OUT.replace("search", "null")
os.makedirs(OUT, exist_ok=True)

def process(tic):
    try:
        secs = []
        for fp in sector_files(tic):
            t, f, fe, m = load_lc(fp)
            if len(t) < (2000 if SOURCE == "spoc" else 400): continue
            td, fd, mask, _ = detrend(t, f, 0.5); secs.append((td, fd, fe[mask]))
        if not secs: return dict(tic=tic, error="no data")
        T = np.concatenate([s[0] for s in secs]); F = np.concatenate([s[1] for s in secs]); E = np.concatenate([s[2] for s in secs])
        o = np.argsort(T); T, F, E = T[o], F[o], E[o]
        durs = np.array([1.0, 1.5, 2.0, 3.0, 4.0]) / 24; base = T.max() - T.min()
        pg = period_grid(base, 0.5, 20.0 if base > 60 else max(1.0, base / 2), durs.min(), oversample=2.0)
        Tb, Fb, Eb = bin_lc(T, F, E, 10 / 1440)
        peaks = bls_stats(Tb, 2 - Fb, Eb, pg, durs)
        Fi = 2 - F; yrs = np.array([year_of(x) for x in T])
        for q in peaks:
            nyd = 0
            for y in np.unique(yrs):
                m = yrs == y; ph = ((T[m] - q["t0"]) / q["period"] + 0.5) % 1 - 0.5; intr = np.abs(ph * q["period"]) < q["duration_h"] / 48
                if intr.sum() < 3: continue
                d = 1 - np.mean(Fi[m][intr]); de = np.std(Fi[m][~intr]) / np.sqrt(intr.sum())
                if de > 0 and d / de > 2.5: nyd += 1
            q["yrs_det"] = nyd
        pk = peaks[0]
        r = dict(tic=tic, n_sectors=len(secs), baseline=float(base), inv_period=pk["period"], inv_sde=pk["sde"], inv_snr=pk["snr"], inv_ntr=pk["n_transits"], inv_depth_ppm=pk["depth"] * 1e6, inv_dur_h=pk["duration_h"],
                 peaks=[{k: v for k, v in q.items() if k not in ("per_transit_ll", "transit_times")} for q in peaks])
        json.dump(r, open(f"{OUT}/{tic}.json", "w")); return r
    except Exception as e: return dict(tic=tic, error=str(e)[:200])

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--n", type=int, default=400); ap.add_argument("--workers", type=int, default=6); a = ap.parse_args()
    tics = sorted({int(re.search(r"(\d{16})", os.path.basename(f)).group(1)) for f in glob.glob(f"{os.path.dirname(sector_files(0)[0]) if sector_files(0) else ''}/*.fits")}) if False else None
    done = {int(os.path.basename(f)[:-5]) for f in glob.glob(f"{SEARCH_OUT}/*.json")}
    rng = np.random.default_rng(42); tics = sorted(done); tics = [int(x) for x in rng.choice(tics, min(a.n, len(tics)), replace=False)]
    tics = [t for t in tics if not os.path.exists(f"{OUT}/{t}.json")]
    print(f"null calibration on {len(tics)} targets ({SOURCE}) with {a.workers} workers", flush=True)
    from multiprocessing import Pool
    with Pool(a.workers) as pool:
        for i, r in enumerate(pool.imap_unordered(process, tics), 1):
            if i % 25 == 0: print(f"[{i}/{len(tics)}]", flush=True)
    rows = []
    import importlib.util
    tp = pd.read_csv("/Users/fernando/Desktop/NASA/catalogs/s107_multiyear_tic_params.csv" if SOURCE == "spoc" else "/Users/fernando/Desktop/NASA/catalogs/qlp/s104_dwarf_pool.csv").set_index("ID")
    def dur_exp(P, tic):
        if tic not in tp.index or not np.isfinite(tp.loc[tic].get("rad", np.nan)): return np.nan
        R = tp.loc[tic]["rad"]; M = tp.loc[tic]["mass"] if np.isfinite(tp.loc[tic].get("mass", np.nan)) else (R if R < 0.7 else R**1.25)
        return 13.0 * (P / 365.25) ** (1 / 3) * (M / R**3) ** (-1 / 3)
    for f in glob.glob(f"{OUT}/*.json"):
        d = json.load(open(f))
        if "peaks" not in d: continue
        # apply the SAME physical filters as rank.py to the inverted top-3 peaks; keep the best surviving SDE
        best = None
        for q in d["peaks"]:
            oe = abs(q["depth_odd"] - q["depth_even"]) / np.hypot(q["depth_odd_err"], q["depth_even_err"]) if q["depth_odd_err"] > 0 else np.nan
            sec = q["depth_phased"] / q["depth_err"] if q["depth_err"] > 0 else np.nan
            de = dur_exp(q["period"], d["tic"]); dr = q["duration_h"] / de if de and np.isfinite(de) else np.nan
            ok = (q["n_transits"] >= 3) and (abs(sec) < 3) and (oe < 5) and ((dr < 1.6) or not np.isfinite(dr)) and (q["depth"] < 0.03) and (q.get("yrs_det", 0) >= 2)
            if ok and (best is None or q["sde"] > best): best = q["sde"]
        rows.append(dict(tic=d["tic"], inv_sde_top=d["inv_sde"], inv_sde_filtered=best if best is not None else 0.0, inv_period=d["inv_period"], n_sectors=d["n_sectors"]))
    df = pd.DataFrame(rows); df.to_csv(f"{OUT}/null_summary.csv", index=False)
    print("FILTERED inverted SDE (same physical cuts as the real ranking) percentiles 50/90/99/max:", np.percentile(df.inv_sde_filtered, [50, 90, 99, 100]).round(2))
    print("fraction with filtered inverted SDE > 9:", (df.inv_sde_filtered > 9).mean().round(3), " > 10:", (df.inv_sde_filtered > 10).mean().round(3), " > 12:", (df.inv_sde_filtered > 12).mean().round(3), " > 13:", (df.inv_sde_filtered > 13).mean().round(3), " > 13.2:", (df.inv_sde_filtered > 13.2).mean().round(3), " > 14:", (df.inv_sde_filtered > 14).mean().round(3), " > 14.3:", (df.inv_sde_filtered > 14.3).mean().round(3))
    for thr in (13.2, 14.3): print(f"expected false positives above SDE {thr} in 1637 stars: {(df.inv_sde_filtered > thr).mean() * 1637:.1f}; candidate rank in null (1 = above all): {(df.inv_sde_filtered >= thr).sum() + 1}")
    df = df.rename(columns={"inv_sde_top": "inv_sde"})
    print("inverted top-peak SDE percentiles 50/90/99/max:", np.percentile(df.inv_sde, [50, 90, 99, 100]).round(2), "N =", len(df))
    print("fraction with inverted SDE > 9:", (df.inv_sde > 9).mean().round(3), " > 10:", (df.inv_sde > 10).mean().round(3), " > 11:", (df.inv_sde > 11).mean().round(3), " > 12:", (df.inv_sde > 12).mean().round(3))
