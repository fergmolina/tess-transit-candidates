"""Independent-extraction check (pipeline artefacts, NOT blends): measure the depth of a candidate at its vet.py ephemeris in TESS-SPOC FFI
light curves (PDCSAP, QUALITY==0, transit-masked biweight), per sector and combined, plus a blind BLS on the TESS-SPOC data alone.
Usage: python -I tessspoc_check.py TIC [AUTHOR=TESS-SPOC] [EXPTIME]  e.g. "TIC SPOC 120" for 2-min (uses results/vet_allsky/TIC/report.json)"""
import sys, os, json, numpy as np, lightkurve as lk
from wotan import flatten, transit_mask; from astropy.timeseries import BoxLeastSquares
AUTHOR = sys.argv[2] if len(sys.argv) > 2 else "TESS-SPOC"; EXPT = int(sys.argv[3]) if len(sys.argv) > 3 else None
TIC = int(sys.argv[1]); OUT = f"/Users/fernando/Desktop/NASA/results/vet_allsky/{TIC}"; rep = json.load(open(f"{OUT}/report.json")); b = rep["bls_refine"]; P, T0, DUR_H = b["period"], b["T0"], b["duration_h"]
sr = lk.search_lightcurve(f"TIC {TIC}", author=AUTHOR, exptime=EXPT) if EXPT else lk.search_lightcurve(f"TIC {TIC}", author=AUTHOR); print(sr)
if len(sr) == 0: print(f"no {AUTHOR} products"); sys.exit()
lcs = sr.download_all(download_dir="/Users/fernando/Desktop/NASA/data/lk_cache"); res = {}; T, F = [], []
for lc in lcs:
    try: lc = lc.remove_nans().normalize(); q = lc.quality == 0; t = lc.time.value[q]; f = lc.flux.value[q]
    except Exception as e: print("skip", e); continue
    m = transit_mask(time=t, period=P, duration=2 * DUR_H / 24, T0=T0); fl = flatten(t, f, method="biweight", window_length=0.7, mask=m); ok = np.isfinite(fl); t, fl = t[ok], fl[ok]
    ph = ((t - T0) / P + 0.5) % 1 - 0.5; intr = np.abs(ph * P) < DUR_H / 48; oot = (np.abs(ph * P) > DUR_H / 24) & (np.abs(ph * P) < 3 * DUR_H / 24)
    if intr.sum() < 5: continue
    d = 1 - np.mean(fl[intr]); de = np.std(fl[oot]) / np.sqrt(intr.sum()); sec = int(lc.sector); res[f"S{sec}"] = dict(depth_ppm=float(d * 1e6), err_ppm=float(de * 1e6), n_in=int(intr.sum()), exptime_s=float(np.median(np.diff(t)) * 86400)); print(sec, res[f"S{sec}"]); T.append(t); F.append(fl)
T = np.concatenate(T); F = np.concatenate(F); ph = ((T - T0) / P + 0.5) % 1 - 0.5; intr = np.abs(ph * P) < DUR_H / 48; oot = np.abs(ph * P) > DUR_H / 24
res["combined"] = dict(depth_ppm=float((1 - np.mean(F[intr])) * 1e6), err_ppm=float(np.std(F[oot]) / np.sqrt(intr.sum()) * 1e6), n_in=int(intr.sum()), qlp_depth_ppm=b["depth_ppm"])
bls = BoxLeastSquares(T, F); per = np.exp(np.linspace(np.log(0.5), np.log(25), 50000)); r = bls.power(per, [1 / 24, 2 / 24, 3 / 24, 4 / 24], objective="snr")
sde = (r.power - np.median(r.power)) / (1.4826 * np.median(np.abs(r.power - np.median(r.power)))); i = int(np.argmax(sde)); k = np.argmin(np.abs(per - P))
res["blind_bls"] = dict(top_period=float(per[i]), top_sde=float(sde[i]), sde_at_qlp_period=float(sde[max(0, k - 20):k + 20].max()))
print(json.dumps(res, indent=1)); json.dump(res, open(f"{OUT}/{AUTHOR.lower().replace('-', '')}{'_' + str(EXPT) if EXPT else ''}_check.json", "w"), indent=1)
