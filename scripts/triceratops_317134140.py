"""TRICERATOPS false-positive probability for the 0.5719-d signal of TIC 317134140 (supporting evidence only: Giacalone+2021 note FPP is
not a reliable predictor at SNR < 15). Uses the SPOC S98 pipeline aperture, the masked-detrended multi-sector light curve folded on the
frozen ephemeris, and no contrast curve. Run with .venv_tri (numpy<2)."""
import sys, os, json, warnings; warnings.filterwarnings("ignore")
import numpy as np, pandas as pd, lightkurve as lk
from triceratops import triceratops as tr
P, T0, dur_h, depth = 0.5718634, 1468.67922, 1.5, 185e-6
OUT = "/Users/fernando/Desktop/NASA/results/vet/317134140"
# folded light curve from the vetting products: rebuild from SPOC PDCSAP with a 0.5-d biweight (the same detrending family as the search)
from astropy.io import fits; from wotan import flatten
import glob
T, F = [], []
for f in sorted(glob.glob("/Users/fernando/Desktop/NASA/data/lc/*317134140*")):
    d = fits.open(f)[1].data; t, fl, q = d["TIME"], d["PDCSAP_FLUX"], d["QUALITY"]; ok = np.isfinite(t) & np.isfinite(fl) & (q == 0); t, fl = t[ok], fl[ok] / np.nanmedian(fl[ok])
    # mask TOI-2514.01 (6.3951381 d, epoch BTJD 1470.77, 2.1 h) before detrending
    ph1 = ((t - 1470.77) / 6.3951381 + 0.5) % 1 - 0.5; m1 = np.abs(ph1 * 6.3951381 * 24) < 1.6
    flat = flatten(t[~m1], fl[~m1], method="biweight", window_length=0.5, return_trend=False); ok2 = np.isfinite(flat); T.append(t[~m1][ok2]); F.append(flat[ok2])
T = np.concatenate(T); F = np.concatenate(F); ph = ((T - T0) / P + 0.5) % 1 - 0.5; sel = np.abs(ph * P * 24) < 6
tb = np.round(ph[sel] * P / (10 / 1440)) * (10 / 1440); u = np.unique(tb); fb = np.array([np.mean(F[sel][tb == x]) for x in u]); eb = np.array([np.std(F[sel][tb == x]) / np.sqrt(np.sum(tb == x)) for x in u])
print("folded points (10-min bins):", len(u), "depth check:", (1 - np.mean(fb[np.abs(u * 24) < 0.5])) * 1e6, "ppm", flush=True)
# SPOC aperture of S98
sr = lk.search_targetpixelfile("TIC 317134140", sector=98, author="SPOC", exptime=120); tpf = sr.download(download_dir="/Users/fernando/Desktop/NASA/data/lk_cache")
ap = tpf.pipeline_mask; rows, cols = np.where(ap); ap_pix = np.array([[tpf.column + c, tpf.row + r] for r, c in zip(rows, cols)])
print("aperture pixels:", len(ap_pix), flush=True)
target = tr.target(ID=317134140, sectors=np.array([98]))
target.calc_depths(tdepth=depth, all_ap_pixels=[ap_pix])
print(target.stars.head(10).to_string(), flush=True)
target.calc_probs(time=u, flux_0=fb, flux_err_0=float(np.median(eb)), P_orb=P, parallel=True, drop_scenario=[], verbose=1)
print("\nFPP =", target.FPP, " NFPP =", target.NFPP, flush=True)
target.probs.to_csv(f"{OUT}/triceratops_probs.csv", index=False)
json.dump(dict(FPP=float(target.FPP), NFPP=float(target.NFPP), note="no contrast curve; SPOC S98 aperture; masked 0.5-d biweight fold; supporting evidence only (SNR<15)"), open(f"{OUT}/triceratops.json", "w"), indent=1)
