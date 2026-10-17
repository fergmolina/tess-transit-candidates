"""Archival test of a candidate in FFI sectors (QLP / TESS-SPOC) that have no 2-min data.
Usage: python -I archival_test.py TIC P P_err T0 T0_err DUR_H --sectors 32,33 [--mask P,T0,dur_h]
For each sector/product: blind BLS, depth at predicted phase vs random-phase null, +-4 h phase scan; then a stacked fold of all archival sectors."""
import sys, os, json, argparse, warnings; sys.path.insert(0, "/Users/fernando/Desktop/NASA/scripts"); warnings.filterwarnings("ignore")
import numpy as np, lightkurve as lk, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from tsearch import detrend
from search_pipeline import period_grid, bls_stats, bin_lc
from vet import box_depth
ap = argparse.ArgumentParser(); ap.add_argument("tic", type=int); ap.add_argument("P", type=float); ap.add_argument("P_err", type=float); ap.add_argument("T0", type=float); ap.add_argument("T0_err", type=float); ap.add_argument("dur_h", type=float)
ap.add_argument("--sectors", required=True); ap.add_argument("--mask", default=""); ap.add_argument("--authors", default="TESS-SPOC,QLP"); ap.add_argument("--label", default="archival"); ap.add_argument("--invert", action="store_true", help="invert the flux (null control)")
a = ap.parse_args()
P, P_err, T0, T0_err, dur = a.P, a.P_err, a.T0, a.T0_err, a.dur_h / 24
OUT = f"/Users/fernando/Desktop/NASA/results/vet/{a.tic}"; os.makedirs(OUT, exist_ok=True)
sr = lk.search_lightcurve(f"TIC {a.tic}")
res = dict(ephemeris_used=dict(P=P, P_err=P_err, T0=T0, T0_err=T0_err, dur_h=a.dur_h)); data = {}
for sec in [int(x) for x in a.sectors.split(",")]:
    for au in a.authors.split(","):
        s = sr[(sr.author == au) & (sr.mission == f"TESS Sector {sec:02d}")]
        if not len(s): print(f"S{sec} {au}: no product"); continue
        lc = s[0].download(download_dir="/Users/fernando/Desktop/NASA/data/lk_cache").remove_nans()
        if "quality" in lc.columns: lc = lc[lc.quality == 0]
        lc = lc.normalize(); t, f = lc.time.value, lc.flux.value.astype(float)
        if a.mask:
            from wotan import transit_mask
            mp, mt0, mdh = [float(x) for x in a.mask.split(",")]; mt0 = mt0 - 2457000 if mt0 > 2457000 else mt0
            keep = ~transit_mask(time=t, period=mp, duration=1.5 * mdh / 24, T0=mt0); t, f = t[keep], f[keep]
        td, fd, m, _ = detrend(t, f, 0.5); fe = np.full_like(fd, 1.4826 * np.median(np.abs(np.diff(fd))) / np.sqrt(2))
        if a.invert: fd = 2 - fd
        key = f"S{sec}_{au}"; data[key] = (td, fd, fe)
        base = td.max() - td.min(); pg = period_grid(base, 0.5, min(13, base / 2), 1 / 24, oversample=3)
        peaks = bls_stats(td, fd, fe, pg, np.array([1.0, 1.5, 2.0, 2.5, 3.0]) / 24)
        n = round((td.mean() - T0) / P); sig_pred = np.sqrt(T0_err**2 + (n * P_err)**2)
        d, de, nin = box_depth(td, fd, P, T0, dur)
        rng = np.random.default_rng(0); nulls = np.array([box_depth(td, fd, P, T0 + P * (0.1 + 0.8 * rng.random()), dur)[0] for _ in range(1000)]); nulls = nulls[np.isfinite(nulls)]
        offs = np.arange(-4, 4.01, 1 / 6) / 24; scan = np.array([box_depth(td, fd, P, T0 + o, dur)[:2] for o in offs]); ib = int(np.nanargmax(scan[:, 0]))
        rank = next((i for i, pk in enumerate(peaks) if any(abs(pk["period"] * k - P) / P < 0.01 for k in (1, 2, 0.5))), None)
        print(f"{key}: N={len(td)} cadence={np.median(np.diff(td))*1440:.0f} min rms={np.std(fd)*1e6:.0f} ppm | {n} cycles from T0 -> predicted-phase 1-sigma {sig_pred*1440:.0f} min")
        print(f"   blind BLS top-3: {[(round(p['period'],4), round(p['depth']*1e6), round(p['sde'],1), p['n_transits']) for p in peaks]}  candidate rank: {rank}")
        print(f"   depth at predicted phase: {d*1e6:.0f}+-{de*1e6:.0f} ppm (n_in={nin}, {d/de:.1f} sigma); null sd {np.std(nulls)*1e6:.0f}; p(null>=obs)={np.mean(nulls>=d):.3f}; deepest within +-4 h: {scan[ib,0]*1e6:.0f}+-{scan[ib,1]*1e6:.0f} at {offs[ib]*24:+.1f} h")
        res[key] = dict(n=len(td), rms_ppm=float(np.std(fd) * 1e6), cycles=int(n), pred_sigma_min=float(sig_pred * 1440), blind_rank=rank,
                        blind_peaks=[{k: v for k, v in p.items() if k not in ("per_transit_ll", "transit_times")} for p in peaks],
                        depth_pred=d, depth_pred_err=de, n_in=nin, null_p=float(np.mean(nulls >= d)), null_sd=float(np.std(nulls)), scan_best_offset_h=float(offs[ib] * 24), scan_best_depth=float(scan[ib, 0]), scan_best_err=float(scan[ib, 1]))
# stacked archival fold (prefer TESS-SPOC where both exist)
keys = {}
for k in data: keys.setdefault(k.split("_")[0], []).append(k)
use = [sorted(v, key=lambda x: 0 if "TESS-SPOC" in x else 1)[0] for v in keys.values()]
if use:
    T = np.concatenate([data[k][0] for k in use]); F = np.concatenate([data[k][1] for k in use]); E = np.concatenate([data[k][2] for k in use])
    d, de, nin = box_depth(T, F, P, T0, dur); rng = np.random.default_rng(1); nulls = np.array([box_depth(T, F, P, T0 + P * (0.1 + 0.8 * rng.random()), dur)[0] for _ in range(1000)]); nulls = nulls[np.isfinite(nulls)]
    offs = np.arange(-4, 4.01, 1 / 6) / 24; scan = np.array([box_depth(T, F, P, T0 + o, dur)[:2] for o in offs]); ib = int(np.nanargmax(scan[:, 0]))
    base = T.max() - T.min(); pg = period_grid(base, 0.5, min(13, base / 2), 1 / 24, oversample=3); peaks = bls_stats(bin_lc(T, F, E, 10 / 1440)[0], bin_lc(T, F, E, 10 / 1440)[1], bin_lc(T, F, E, 10 / 1440)[2], pg, np.array([1.0, 1.5, 2.0, 3.0]) / 24)
    rank = next((i for i, pk in enumerate(peaks) if any(abs(pk["period"] * k - P) / P < 0.01 for k in (1, 2, 0.5))), None)
    print(f"STACKED {use}: depth at predicted phase {d*1e6:.0f}+-{de*1e6:.0f} ppm ({d/de:.1f} sigma, n_in={nin}); null p={np.mean(nulls>=d):.3f}; deepest within +-4 h {scan[ib,0]*1e6:.0f}+-{scan[ib,1]*1e6:.0f} at {offs[ib]*24:+.1f} h; blind BLS top-3 {[(round(p['period'],4), round(p['depth']*1e6), round(p['sde'],1)) for p in peaks]} candidate rank {rank}")
    res["stacked"] = dict(products=use, depth_pred=d, depth_pred_err=de, n_in=nin, null_p=float(np.mean(nulls >= d)), scan_best_offset_h=float(offs[ib] * 24), scan_best_depth=float(scan[ib, 0]), blind_rank=rank,
                          blind_peaks=[{k: v for k, v in p.items() if k not in ("per_transit_ll", "transit_times")} for p in peaks])
    fig, ax = plt.subplots(1, 2, figsize=(13, 4))
    ph = ((T - T0) / P + 0.5) % 1 - 0.5; ax[0].plot(ph * P * 24, F, ".", ms=2, color="0.7"); pb, fb, eb = bin_lc(ph * P * 24 + 500, F, E, 0.25); ax[0].errorbar(pb - 500, fb, eb, fmt="ko", ms=3)
    ax[0].axvspan(-a.dur_h / 2, a.dur_h / 2, color="r", alpha=0.1); ax[0].set_xlim(-6, 6); ax[0].set_ylim(1 - 4 * max(abs(d), 2e-4), 1 + 3 * max(abs(d), 2e-4)); ax[0].set_title(f"TIC {a.tic} {a.label} {use} folded at P={P:.5f}"); ax[0].set_xlabel("hours from predicted mid-transit")
    ax[1].errorbar(offs * 24, scan[:, 0] * 1e6, scan[:, 1] * 1e6, fmt="k.-"); ax[1].axvline(0, color="r"); ax[1].set_xlabel("phase offset from prediction (h)"); ax[1].set_ylabel("box depth (ppm)"); ax[1].set_title("phase scan")
    fig.tight_layout(); fig.savefig(f"{OUT}/{a.label}_fold.png", dpi=100)
json.dump(res, open(f"{OUT}/{a.label}_test.json", "w"), indent=1, default=float)
np.savez(f"{OUT}/{a.label}_data.npz", **{k: np.vstack(v) for k, v in data.items()})
