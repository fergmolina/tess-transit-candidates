"""Why is the 0.5719-d signal weak in S32 FFI products? Re-measure with raw SAP fluxes + own masked detrend, per orbit halves."""
import sys, warnings; sys.path.insert(0, "/Users/fernando/Desktop/NASA/scripts"); warnings.filterwarnings("ignore")
import numpy as np, lightkurve as lk
from wotan import flatten, transit_mask
from vet import box_depth
from tsearch import trim_edges
P, T0, dur = 0.571860, 1468.69518, 1.5 / 24
mP, mT0, mdur = 6.3951381, 2459215.084143 - 2457000, 4.047 / 24
sr = lk.search_lightcurve("TIC 317134140")
for sec in (32, 33):
    for au, cols in (("TESS-SPOC", ("pdcsap_flux", "sap_flux")), ("QLP", ("det_flux", "sap_flux", "kspsap_flux"))):
        s = sr[(sr.author == au) & (sr.mission == f"TESS Sector {sec:02d}")]
        if not len(s): continue
        for col in cols:
            try: lc = s[0].download(download_dir="/Users/fernando/Desktop/NASA/data/lk_cache", flux_column=col)
            except Exception as e: print(f"S{sec} {au} {col}: {e}"); continue
            lc = lc.remove_nans()
            if "quality" in lc.columns: lc = lc[lc.quality == 0]
            lc = lc.normalize(); t, f = lc.time.value, lc.flux.value.astype(float)
            keep = ~transit_mask(time=t, period=mP, duration=1.5 * mdur, T0=mT0) & trim_edges(t); t, f = t[keep], f[keep]
            mask = transit_mask(time=t, period=P, duration=2 * dur, T0=T0)
            flat = flatten(t, f, method="biweight", window_length=0.5, break_tolerance=0.5, mask=mask); ok = np.isfinite(flat)
            t, f = t[ok], flat[ok]
            d, de, n = box_depth(t, f, P, T0, dur)
            half = t < np.median(t); d1 = box_depth(t[half], f[half], P, T0, dur); d2 = box_depth(t[~half], f[~half], P, T0, dur)
            print(f"S{sec} {au:9s} {col:12s}: N={len(t)} rms={np.std(f)*1e6:.0f} depth@pred={d*1e6:.0f}+-{de*1e6:.0f} ({d/de:.1f}s)  1st half {d1[0]*1e6:.0f}+-{d1[1]*1e6:.0f}  2nd half {d2[0]*1e6:.0f}+-{d2[1]*1e6:.0f}")
