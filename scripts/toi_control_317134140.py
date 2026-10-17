"""In-aperture control: per-sector depth of the KNOWN TOI-2514.01 (P=6.3951381 d, ExoFOP epoch 2459215.084143, 4.047 h, 510 ppm)
with the same machinery used for the 0.5719-d signal, in all six sectors."""
import sys, warnings; sys.path.insert(0, "/Users/fernando/Desktop/NASA/scripts"); warnings.filterwarnings("ignore")
import numpy as np, lightkurve as lk
from wotan import flatten, transit_mask
from tsearch import load_spoc_lc, trim_edges
from search_pipeline import sector_files
from vet import box_depth
tic = 317134140; P, T0, dur = 6.3951381, 2459215.084143 - 2457000, 4.047 / 24
cP, cT0, cdur = 0.5718634, 1468.67922, 1.5 / 24
def prep(t, f):
    keep = trim_edges(t); t, f = t[keep], f[keep]
    tm = transit_mask(time=t, period=P, duration=2 * dur, T0=T0) | transit_mask(time=t, period=cP, duration=2 * cdur, T0=cT0)
    flat = flatten(t, f, method="biweight", window_length=1.0, break_tolerance=0.5, mask=tm); ok = np.isfinite(flat); return t[ok], flat[ok]
sets = {}
for fp in sector_files(tic):
    t, f, fe, m = load_spoc_lc(fp); sets[f"S{m['sector']}"] = prep(t, f)
sr = lk.search_lightcurve(f"TIC {tic}", author="TESS-SPOC")
for sec in (32, 33):
    lc = sr[sr.mission == f"TESS Sector {sec:02d}"][0].download(download_dir="/Users/fernando/Desktop/NASA/data/lk_cache").remove_nans(); lc = lc[lc.quality == 0].normalize()
    sets[f"S{sec}"] = prep(lc.time.value, lc.flux.value.astype(float))
print("sector | TOI-2514.01 depth (ppm) n_in | 0.5719-d depth (ppm)")
for k in sorted(sets, key=lambda x: int(x[1:])):
    t, f = sets[k]; d, de, n = box_depth(t, f, P, T0, dur); c, ce, cn = box_depth(t, f, cP, cT0, cdur)
    print(f"{k:5s} | {d*1e6:5.0f} +- {de*1e6:3.0f}  (n_in={n:4d}) | {c*1e6:4.0f} +- {ce*1e6:3.0f}")
