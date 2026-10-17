"""Archival test for TIC 176798599: the 7.334-d signal was found in SPOC 2-min data from S97/S106/S107 (2025-26).
The star was observed in FFIs in S4 (2018) and S31 (2020). Test: (1) blind BLS on each archival sector alone,
(2) depth at the phase predicted by the 2025-26 ephemeris vs random-phase null, (3) stitched all-years search."""
import sys, os, json, warnings; sys.path.insert(0, "/Users/fernando/Desktop/NASA/scripts"); warnings.filterwarnings("ignore")
import numpy as np, lightkurve as lk
from tsearch import detrend
from search_pipeline import period_grid, bls_stats, bin_lc
from vet import box_depth
OUT = "/Users/fernando/Desktop/NASA/results/vet/176798599"; os.makedirs(OUT, exist_ok=True)
P, P_err, T0, T0_err = float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4])
dur = 2.4 / 24
sr = lk.search_lightcurve("TIC 176798599")
res = {"ephemeris_used": dict(P=P, P_err=P_err, T0=T0, T0_err=T0_err)}
data = {}
for sec, authors in ((4, ("TESS-SPOC", "QLP")), (31, ("TESS-SPOC", "QLP"))):
    for au in authors:
        s = sr[(sr.author == au) & (sr.mission == f"TESS Sector {sec:02d}")]
        if not len(s): continue
        lc = s[0].download(download_dir="/Users/fernando/Desktop/NASA/data/lk_cache").remove_nans()
        if "quality" in lc.columns: lc = lc[lc.quality == 0]
        lc = lc.normalize(); t, f = lc.time.value, lc.flux.value.astype(float)
        td, fd, m, _ = detrend(t, f, 0.5); fe = np.full_like(fd, 1.4826 * np.median(np.abs(np.diff(fd))) / np.sqrt(2))
        key = f"S{sec}_{au}"; data[key] = (td, fd, fe)
        base = td.max() - td.min(); pg = period_grid(base, 0.5, 13, np.array([1, 1.5, 2, 3]).min() / 24, oversample=3)
        peaks = bls_stats(td, fd, fe, pg, np.array([1.0, 1.5, 2.0, 2.5, 3.0]) / 24)
        n = round((td.mean() - T0) / P); tc_pred = T0 + n * P; sig_pred = np.sqrt(T0_err**2 + (n * P_err)**2)
        d, de, nin = box_depth(td, fd, P, T0, dur)
        rng = np.random.default_rng(0); nulls = np.array([box_depth(td, fd, P, T0 + P * (0.1 + 0.8 * rng.random()), dur)[0] for _ in range(1000)]); nulls = nulls[np.isfinite(nulls)]
        # phase scan: depth vs phase offset, to see where the best dip lies relative to prediction
        offs = np.linspace(-0.5, 0.5, 201) * P; scan = np.array([box_depth(td, fd, P, T0 + o, dur)[0] for o in offs])
        ib = int(np.nanargmax(scan))
        print(f"{key}: N={len(td)} cadence={np.median(np.diff(td))*1440:.0f} min rms={np.std(fd)*1e6:.0f} ppm | cycles from T0: {n} -> predicted-phase uncertainty {sig_pred*1440:.0f} min")
        print(f"   blind BLS top-3: {[(round(p['period'],4), round(p['depth']*1e6), round(p['sde'],1), p['n_transits']) for p in peaks]}")
        print(f"   depth at predicted phase: {d*1e6:.0f}+-{de*1e6:.0f} ppm (n_in={nin}); null mean {np.mean(nulls)*1e6:.0f} sd {np.std(nulls)*1e6:.0f}; p(null>=obs)={np.mean(nulls>=d):.3f}")
        print(f"   phase scan: deepest box at offset {offs[ib]*24:+.1f} h ({scan[ib]*1e6:.0f} ppm)")
        res[key] = dict(n=len(td), rms_ppm=float(np.std(fd)*1e6), cycles=int(n), pred_sigma_min=float(sig_pred*1440), blind_peaks=[{k: v for k, v in p.items() if k not in ("per_transit_ll", "transit_times")} for p in peaks],
                        depth_pred=d, depth_pred_err=de, n_in=nin, null_p=float(np.mean(nulls >= d)), null_mean=float(np.mean(nulls)), null_sd=float(np.std(nulls)),
                        scan_best_offset_h=float(offs[ib]*24), scan_best_depth=float(scan[ib]))
# stitched: archival (best product per sector) + SPOC 2-min (from vet data: reload via search_pipeline loader)
from search_pipeline import sector_files, load_lc
parts = [data.get("S4_TESS-SPOC", data.get("S4_QLP")), data.get("S31_TESS-SPOC", data.get("S31_QLP"))]
for fp in sector_files(176798599):
    t, f, fe, m = load_lc(fp); td, fd, mk, _ = detrend(t, f, 0.5); parts.append((td, fd, fe[mk]))
parts = [p for p in parts if p is not None]
T = np.concatenate([p[0] for p in parts]); F = np.concatenate([p[1] for p in parts]); E = np.concatenate([p[2] for p in parts]); o = np.argsort(T); T, F, E = T[o], F[o], E[o]
Tb, Fb, Eb = bin_lc(T, F, E, 10 / 1440); pg = period_grid(T.max() - T.min(), 0.5, 20, 1 / 24, oversample=2.0)
pk = bls_stats(Tb, Fb, Eb, pg, np.array([1.0, 1.5, 2.0, 3.0, 4.0]) / 24)
pki = bls_stats(Tb, 2 - Fb, Eb, pg, np.array([1.0, 1.5, 2.0, 3.0, 4.0]) / 24)
print(f"STITCHED 2018+2020+2025+2026 (baseline {T.max()-T.min():.0f} d, {len(pg)} periods): top-3 {[(round(p['period'],5), round(p['depth']*1e6), round(p['sde'],1), p['n_transits']) for p in pk]}; inverted top SDE {pki[0]['sde']:.1f}")
res["stitched_all_years"] = dict(peaks=[{k: v for k, v in p.items() if k not in ("per_transit_ll", "transit_times")} for p in pk], inverted_top_sde=pki[0]["sde"], baseline=float(T.max() - T.min()))
json.dump(res, open(f"{OUT}/archival_test.json", "w"), indent=1, default=float)
np.savez(f"{OUT}/archival_data.npz", **{k: np.vstack(v) for k, v in data.items()})
