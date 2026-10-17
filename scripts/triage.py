"""Quick-look triage for ranked candidates: folded LC, per-year fold, individual events, single-event dominance.
Usage: python -I triage.py [--n 20] [--min-sde 8.5] [--tics a,b,c]"""
import sys, os, json, argparse, warnings; sys.path.insert(0, "/Users/fernando/Desktop/NASA/scripts"); warnings.filterwarnings("ignore")
import numpy as np, pandas as pd, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from tsearch import load_spoc_lc, detrend
from search_pipeline import sector_files, year_of, bin_lc, load_lc, SOURCE
OUT = "/Users/fernando/Desktop/NASA/results/triage" + ("" if SOURCE == "spoc" else "_qlp"); os.makedirs(OUT, exist_ok=True)

def triage(tic, P, T0, dur_h, depth_ppm, tag=""):
    dur = dur_h / 24
    secs = {}
    for fp in sector_files(tic):
        t, f, fe, m = load_lc(fp)
        if len(t) < 1000: continue
        td, fd, mask, _ = detrend(t, f, 0.5); secs[m["sector"]] = (td, fd, fe[mask])
    T = np.concatenate([v[0] for v in secs.values()]); F = np.concatenate([v[1] for v in secs.values()]); E = np.concatenate([v[2] for v in secs.values()])
    o = np.argsort(T); T, F, E = T[o], F[o], E[o]
    # data-gap edges (after trimming): gap > 0.25 d, plus series ends
    gi = np.where(np.diff(T) > 0.25)[0]; edges = np.concatenate([[T[0], T[-1]], T[gi], T[gi + 1]])
    ph = ((T - T0) / P + 0.5) % 1 - 0.5
    ep = np.round((T - T0) / P).astype(int)
    # per-event depth & SNR
    events = []
    for n in np.unique(ep):
        m = (ep == n) & (np.abs(ph * P) < dur / 2)
        mo = (ep == n) & (np.abs(ph * P) > dur) & (np.abs(ph * P) < 3 * dur)
        if m.sum() < 5 or mo.sum() < 10: continue
        d = np.median(F[mo]) - np.mean(F[m]); e = np.std(F[mo]) / np.sqrt(m.sum())
        sec = [s for s, v in secs.items() if v[0].min() - 0.5 < T0 + n * P < v[0].max() + 0.5]
        tc = T0 + n * P; edge_dist = float(np.min(np.abs(edges - tc)))
        events.append(dict(epoch=int(n), tc=float(tc), depth=float(d), err=float(e), snr=float(d / e), n_in=int(m.sum()), sector=sec[0] if sec else None, year=year_of(tc), edge_dist_d=edge_dist))
    snrs = np.array([x["snr"] for x in events]); pos = np.clip(snrs, 0, None)
    dom = float(pos.max()**2 / np.sum(pos**2)) if len(pos) and np.sum(pos**2) > 0 else np.nan
    stacked = np.sum([x["depth"] / x["err"]**2 for x in events]) / np.sum([1 / x["err"]**2 for x in events]) if events else np.nan
    stacked_err = 1 / np.sqrt(np.sum([1 / x["err"]**2 for x in events])) if events else np.nan
    # stacked SNR excluding the strongest event
    if len(events) > 1:
        i = int(np.argmax(snrs)); rest = [x for j, x in enumerate(events) if j != i]
        s2 = np.sum([x["depth"] / x["err"]**2 for x in rest]) / np.sum([1 / x["err"]**2 for x in rest]); e2 = 1 / np.sqrt(np.sum([1 / x["err"]**2 for x in rest]))
        snr_wo_best = float(s2 / e2)
    else: snr_wo_best = np.nan
    n_sig = int(np.sum(snrs > 2))
    sig_ev = [x for x in events if x["snr"] > 2]
    edge_frac = float(np.mean([x["edge_dist_d"] < 0.5 for x in sig_ev])) if sig_ev else np.nan
    # figure
    nev = len(events); ncol = min(6, max(2, nev)); nrow = int(np.ceil(nev / ncol)) if nev else 1
    fig = plt.figure(figsize=(16, 4 + 2.2 * nrow)); gs = fig.add_gridspec(1 + nrow, ncol)
    ax = fig.add_subplot(gs[0, :ncol // 2 or 1]); ax.plot(ph * P * 24, F, ".", ms=1, color="0.7", alpha=0.4)
    pb, fb, eb = bin_lc(ph * P * 24 + 500, F, E, 10 / 60); ax.errorbar(pb - 500, fb, eb, fmt="ko", ms=3)
    ax.set_xlim(-4 * dur_h, 4 * dur_h); ax.set_ylim(1 - 3.5 * depth_ppm * 1e-6 - 2 * np.median(eb), 1 + 2 * depth_ppm * 1e-6 + 2 * np.median(eb))
    ax.axvspan(-dur_h / 2, dur_h / 2, color="r", alpha=0.08); ax.set_title(f"TIC {tic} P={P:.5f} d depth={depth_ppm:.0f} ppm {tag}"); ax.set_xlabel("hours")
    ax2 = fig.add_subplot(gs[0, ncol // 2 or 1:]);
    for y in sorted(set(year_of(x) for x in T)):
        m = np.array([year_of(x) == y for x in T]); pb, fb, eb = bin_lc(ph[m] * P * 24 + 500, F[m], E[m], 20 / 60); ax2.errorbar(pb - 500, fb, eb, fmt="o", ms=3, label=str(y))
    ax2.set_xlim(-4 * dur_h, 4 * dur_h); ax2.set_ylim(ax.get_ylim()); ax2.legend(fontsize=8); ax2.set_title("per year, 20-min bins")
    for i, x in enumerate(events):
        a = fig.add_subplot(gs[1 + i // ncol, i % ncol]); w = np.abs(T - x["tc"]) < 3 * dur
        a.plot((T[w] - x["tc"]) * 24, F[w], ".", ms=2, color="0.6"); pb, fb, eb = bin_lc((T[w] - x["tc"]) * 24 + 500, F[w], E[w], 0.5); a.plot(pb - 500, fb, "k-o", ms=3)
        a.axvspan(-dur_h / 2, dur_h / 2, color="r", alpha=0.08); a.set_ylim(ax.get_ylim()); a.set_title(f"S{x['sector']} ep{x['epoch']} {x['depth']*1e6:.0f}±{x['err']*1e6:.0f} ({x['snr']:.1f}σ) edge {x['edge_dist_d']:.1f}d", fontsize=8)
    fig.tight_layout(); fig.savefig(f"{OUT}/{tic}_P{P:.4f}.png", dpi=90); plt.close(fig)
    return dict(tic=tic, period=P, n_events=nev, n_events_snr2=n_sig, dominance=dom, edge_frac=edge_frac, stacked_snr=float(stacked / stacked_err) if events else np.nan, snr_without_best=snr_wo_best,
                events=events, png=f"{OUT}/{tic}_P{P:.4f}.png")

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--n", type=int, default=20); ap.add_argument("--min-sde", type=float, default=8.5); ap.add_argument("--tics", default="")
    ap.add_argument("--csv", default="/Users/fernando/Desktop/NASA/results/candidates_physical" + ("" if SOURCE == "spoc" else "_qlp") + ".csv")
    a = ap.parse_args()
    df = pd.read_csv(a.csv)
    if a.tics: df = df[df.tic.isin([int(x) for x in a.tics.split(",")])]
    else: df = df[df.sde >= a.min_sde].head(a.n)
    rows = []
    for _, r in df.iterrows():
        res = triage(int(r.tic), r.period, r.t0, r.dur_h, r.depth_ppm, tag=f"SDE={r.sde:.1f} Ntr={r.ntr} yrs={r.years}")
        rows.append({**{k: v for k, v in res.items() if k not in ("events", "png")}, "sde": r.sde, "near_orbit": r.near_tess_orbit, "tmag": r.tmag, "teff": r.teff, "rad": r.rad})
        print(f"TIC {res['tic']:>11} P={res['period']:8.4f} SDE={r.sde:5.1f} events={res['n_events']:3d} (>2σ: {res['n_events_snr2']}) dominance={res['dominance']:.2f} edgeFrac={res['edge_frac']:.2f} stackedSNR={res['stacked_snr']:.1f} SNR w/o best={res['snr_without_best']:.1f} nearOrbit={r.near_tess_orbit}", flush=True)
        json.dump(res, open(f"{OUT}/{res['tic']}_P{res['period']:.4f}.json", "w"), default=float)
    pd.DataFrame(rows).to_csv(f"{OUT}/triage_summary.csv", index=False)
