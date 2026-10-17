"""Forward (prediction) test on sectors NOT used to build the ephemeris, with our own aperture photometry from TESScut
cutouts (independent of QLP/SPOC). Steps: download cutout, sum pixels within r px of the target, divide by a background
estimate from the outer annulus, detrend with an unmasked biweight (window = max(0.5 d, 6 x duration)), then (a) measure the
stacked depth at the predicted ephemeris vs 1000 random-phase trials, and (b) run a blind BLS on the new data alone.
Usage: python -I tesscut_forward_test.py TIC P P_ERR T0 T0_ERR DUR_H --sectors 96 103 --r 1.5"""
import sys, os, json, argparse, warnings; warnings.filterwarnings("ignore"); sys.path.insert(0, "/Users/fernando/Desktop/NASA/scripts")
import numpy as np, pandas as pd, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
import lightkurve as lk
from wotan import flatten
from search_pipeline import period_grid, bls_stats, bin_lc

def extract(tic, sector, ra, dec, r_px, size=15):
    sr = lk.search_tesscut(f"TIC {tic}", sector=sector)
    if len(sr) == 0: return None
    tpf = sr.download(cutout_size=size, download_dir="/Users/fernando/Desktop/NASA/data/lk_cache")
    t = tpf.time.value; cube = tpf.flux.value
    q = np.isfinite(cube).all(axis=(1, 2)) & (tpf.quality == 0); t, cube = t[q], cube[q]
    px = tpf.wcs.all_world2pix([[ra, dec]], 0)[0]; ny, nx = cube.shape[1:]; yy, xx = np.mgrid[0:ny, 0:nx]
    d = np.hypot(xx - px[0], yy - px[1]); ap = d <= r_px; bkg = (d > 5) & (d < 7)
    # background: per-cadence median of annulus pixels (scattered light), subtracted per pixel
    b = np.median(cube[:, bkg], axis=1)
    flux = cube[:, ap].sum(axis=1) - b * ap.sum()
    return t, flux, int(ap.sum())

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("tic", type=int); ap.add_argument("P", type=float); ap.add_argument("P_err", type=float); ap.add_argument("T0", type=float); ap.add_argument("T0_err", type=float); ap.add_argument("dur_h", type=float)
    ap.add_argument("--sectors", type=int, nargs="+", required=True); ap.add_argument("--r", type=float, default=1.5); ap.add_argument("--label", default="forward"); a = ap.parse_args()
    pool = pd.read_csv("/Users/fernando/Desktop/NASA/catalogs/qlp/s104_dwarf_pool.csv", usecols=["ID", "ra", "dec"]).set_index("ID"); ra, dec = [float(x) for x in pool.loc[a.tic, ["ra", "dec"]]]
    out = f"/Users/fernando/Desktop/NASA/results/vet_qlp/{a.tic}"; os.makedirs(out, exist_ok=True)
    dur_d = a.dur_h / 24; T, F = [], []; per_sector = {}
    for s in a.sectors:
        r = extract(a.tic, s, ra, dec, a.r)
        if r is None: print("no cutout for", s); continue
        t, flux, npx = r; f = flux / np.nanmedian(flux)
        flat = flatten(t, f, method="biweight", window_length=max(0.5, 6 * dur_d), return_trend=False)
        ok = np.isfinite(flat) & (np.abs(flat - 1) < 5 * 1.4826 * np.nanmedian(np.abs(flat - np.nanmedian(flat))))
        # drop 0.3 d after gaps > 0.25 d (edge ramps)
        tt = t[ok]; gaps = np.where(np.diff(tt) > 0.25)[0]; edge = np.zeros(len(tt), bool)
        for g in gaps: edge |= (tt > tt[g]) & (tt < tt[g] + 0.3); edge |= (tt <= tt[g]) & (tt > tt[g] - 0.3)
        edge |= tt < tt[0] + 0.3; edge |= tt > tt[-1] - 0.3
        t2, f2 = tt[~edge], flat[ok][~edge]
        per_sector[s] = dict(n=len(t2), rms_ppm=float(np.std(f2) * 1e6), n_pix=npx); T.append(t2); F.append(f2)
        print(f"S{s}: {len(t2)} pts, rms {np.std(f2)*1e6:.0f} ppm, aperture {npx} px", flush=True)
    T = np.concatenate(T); F = np.concatenate(F); o = np.argsort(T); T, F = T[o], F[o]
    E = np.full_like(F, np.std(F))
    # (a) prediction test
    n = np.round((T - a.T0) / a.P); tc = a.T0 + n * a.P; sig_t = np.sqrt(a.T0_err ** 2 + (n * a.P_err) ** 2)
    intr = np.abs(T - tc) < dur_d / 2; oot = (np.abs(T - tc) > dur_d) & (np.abs(T - tc) < 4 * dur_d)
    def stacked(phase_shift):
        tcs = tc + phase_shift; i = np.abs(T - tcs) < dur_d / 2; o_ = (np.abs(T - tcs) > dur_d) & (np.abs(T - tcs) < 4 * dur_d)
        if i.sum() < 5: return np.nan
        return np.median(F[o_]) - np.mean(F[i])
    d0 = stacked(0.0); err0 = np.std(F[oot]) / np.sqrt(intr.sum())
    rng = np.random.default_rng(7); null = np.array([stacked(rng.uniform(dur_d, a.P - dur_d)) for _ in range(1000)]); null = null[np.isfinite(null)]
    p = float(np.mean(null >= d0)); n_pred = len(np.unique(n[intr]))
    print(f"prediction: {n_pred} predicted transits covered, mean 1-sigma timing {np.median(sig_t[intr])*24*60:.0f} min; stacked depth at predicted phase {d0*1e6:.0f}+-{err0*1e6:.0f} ppm (SNR {d0/err0:.1f}); random-phase null: median {np.median(null)*1e6:.0f}, 99th pct {np.percentile(null,99)*1e6:.0f} ppm, p={p:.4f}")
    # scan +-3 h around prediction
    shifts = np.arange(-3, 3.01, 0.1) / 24; scan = np.array([stacked(s) for s in shifts]); i = np.nanargmax(scan)
    print(f"deepest within +-3 h: {scan[i]*1e6:.0f} ppm at {shifts[i]*24:+.1f} h")
    # (b) blind BLS on the new data alone
    tb, fb, eb = bin_lc(T, F, E, 10 / 1440)
    periods = period_grid(T.max() - T.min(), 0.5, 20.0, 0.75 / 24, 2); st = bls_stats(tb, fb, eb, periods, np.array([0.75, 1, 1.5, 2, 3, 4]) / 24)
    pk = st["peaks"] if isinstance(st, dict) else st
    tops = [(round(x["period"], 5), round(x["sde"], 1), round(x["depth"] * 1e6)) for x in pk[:5]]
    rank = next((k for k, x in enumerate(pk) if abs(x["period"] / a.P - 1) < 0.002 or abs(x["period"] / (2 * a.P) - 1) < 0.002 or abs(x["period"] / (a.P / 2) - 1) < 0.002), None)
    print(f"blind BLS on new data: top peaks (P, SDE, depth) = {tops}; candidate period rank = {rank}")
    res = dict(sectors=a.sectors, per_sector=per_sector, n_pred=n_pred, depth_ppm=d0 * 1e6, err_ppm=err0 * 1e6, snr=d0 / err0, p_null=p, null_median_ppm=float(np.median(null) * 1e6), null_p99_ppm=float(np.percentile(null, 99) * 1e6), scan_best_ppm=float(scan[i] * 1e6), scan_best_h=float(shifts[i] * 24), bls_top=tops, bls_rank=rank, r_px=a.r)
    json.dump(res, open(f"{out}/{a.label}.json", "w"), indent=1, default=float)
    fig, ax = plt.subplots(1, 2, figsize=(13, 4)); ph = ((T - a.T0) / a.P + 0.5) % 1 - 0.5
    ax[0].plot(ph * a.P * 24, F, ".", ms=1, color="0.7"); tb2, fb2, _ = bin_lc(ph * a.P * 24, F, E, 0.25); ax[0].plot(tb2, fb2, "k.-"); ax[0].set_xlim(-8, 8); ax[0].set_title(f"TIC {a.tic} S{a.sectors} TESScut r={a.r}px folded at predicted ephemeris; depth {d0*1e6:.0f}+-{err0*1e6:.0f} ppm")
    ax[0].axvspan(-a.dur_h / 2, a.dur_h / 2, color="red", alpha=0.1); ax[0].set_xlabel("hours from predicted mid-transit")
    ax[1].hist(null * 1e6, 50, color="0.7"); ax[1].axvline(d0 * 1e6, color="r"); ax[1].set_title(f"random-phase null (p={p:.4f})"); plt.tight_layout(); plt.savefig(f"{out}/{a.label}.png", dpi=110)
