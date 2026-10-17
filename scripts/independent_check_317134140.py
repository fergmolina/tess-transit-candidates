"""Independent re-analysis with different code paths: fresh lightkurve downloads, lightkurve flatten (Savitzky-Golay) and
lightkurve's BLS periodogram (astropy BLS via a different wrapper and grid), plus TLS on the single best sector."""
import warnings; warnings.filterwarnings("ignore")
import numpy as np, lightkurve as lk, json
sr = lk.search_lightcurve("TIC 317134140", author="SPOC", exptime=120)
lcs = []
for r in sr:
    lc = r.download(download_dir="/Users/fernando/Desktop/NASA/data/lk_cache_fresh", quality_bitmask="hard").remove_nans().normalize()
    lc = lc.flatten(window_length=1001, polyorder=2, break_tolerance=50)  # Savitzky-Golay, ~1.4 d window at 2 min
    lc = lc.remove_outliers(sigma_upper=4, sigma_lower=20)
    lcs.append(lc); print("sector", lc.sector, "N", len(lc), "rms ppm", round(float(np.nanstd(np.asarray(lc.flux.value, float))) * 1e6))
coll = lk.LightCurveCollection(lcs); st = coll.stitch()
out = {}
for name, lcx in [("stitched_all", st)] + [(f"S{l.sector}", l) for l in lcs]:
    pg = lcx.to_periodogram(method="bls", minimum_period=0.4, maximum_period=3.0, frequency_factor=200 if name == "stitched_all" else 20, duration=[0.04, 0.06, 0.08, 0.1])
    P = pg.period_at_max_power.value; pw = pg.power.value; pw = np.asarray(pw, float); pw = pw[np.isfinite(pw)]; sde = (pw.max() - np.median(pw)) / (1.4826 * np.median(np.abs(pw - np.median(pw))))
    print(f"{name}: lightkurve BLS best P={P:.5f} d, depth={pg.depth_at_max_power.value*1e6:.0f} ppm, dur={pg.duration_at_max_power.value*24:.1f} h, SDE~{sde:.1f}, n_periods={len(pg.period)}")
    out[name] = dict(P=float(P), depth_ppm=float(pg.depth_at_max_power.value * 1e6), sde=float(sde))
# TLS on S98 alone (single sector keeps TLS well-behaved)
from transitleastsquares import transitleastsquares
l98 = [l for l in lcs if l.sector == 98][0]
r = transitleastsquares(l98.time.value, l98.flux.value, l98.flux_err.value).power(period_min=0.4, period_max=3.0, oversampling_factor=5, duration_grid_step=1.07, R_star=0.98, M_star=0.95, use_threads=1, show_progress_bar=False)
print(f"TLS S98: P={r.period:.5f}+-{r.period_uncertainty:.5f} depth={(1-r.depth)*1e6:.0f} ppm dur={r.duration*24:.2f} h SDE={r.SDE:.1f} SNR={r.snr:.1f} Ntr={r.distinct_transit_count} odd/even={r.odd_even_mismatch:.2f}")
out["tls_S98"] = dict(P=float(r.period), P_err=float(r.period_uncertainty), depth_ppm=float((1 - r.depth) * 1e6), sde=float(r.SDE), snr=float(r.snr))
json.dump(out, open("/Users/fernando/Desktop/NASA/results/vet/317134140/independent_check.json", "w"), indent=1)
