"""Depth vs aperture size from the 2-min TPF: on-target signals keep a constant depth (after dilution correction is ignored,
depth should slightly DEcrease with larger apertures as neighbours dilute); a signal from a neighbour grows with aperture."""
import sys, warnings; sys.path.insert(0, "/Users/fernando/Desktop/NASA/scripts"); warnings.filterwarnings("ignore")
import numpy as np, lightkurve as lk
from wotan import flatten, transit_mask
from vet import box_depth
from tsearch import trim_edges
from scipy.ndimage import binary_dilation, binary_erosion
tic, P, T0, dur = int(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]) / 24
mask_known = sys.argv[5] if len(sys.argv) > 5 else ""
for sec in [int(s) for s in sys.argv[6].split(",")] if len(sys.argv) > 6 else []:
    sr = lk.search_targetpixelfile(f"TIC {tic}", sector=sec, author="SPOC", exptime=120)
    tpf = sr[0].download(download_dir="/Users/fernando/Desktop/NASA/data/lk_cache", quality_bitmask="default")
    ap = tpf.pipeline_mask
    yy, xx = np.mgrid[:ap.shape[0], :ap.shape[1]]
    img = np.nanmedian(tpf.flux.value, axis=0); py, px = np.unravel_index(np.nanargmax(np.where(ap, img, -1)), img.shape)
    r = np.hypot(xx - px, yy - py)
    aps = {"1px": r < 0.5, "r<=1.5": r <= 1.5, "pipeline": ap, "pipe+1": binary_dilation(ap, iterations=1), "pipe+2": binary_dilation(ap, iterations=2)}
    print(f"S{sec}: brightest pipeline pixel ({px},{py}); pipeline aperture {ap.sum()} px")
    for name, m in aps.items():
        lc = tpf.to_lightcurve(aperture_mask=m).remove_nans().normalize()
        t, f = lc.time.value, lc.flux.value.astype(float)
        keep = trim_edges(t)
        if mask_known:
            mp, mt0, mdh = [float(x) for x in mask_known.split(",")]; mt0 = mt0 - 2457000 if mt0 > 2457000 else mt0
            keep &= ~transit_mask(time=t, period=mp, duration=1.5 * mdh / 24, T0=mt0)
        t, f = t[keep], f[keep]
        tm = transit_mask(time=t, period=P, duration=2 * dur, T0=T0)
        flat = flatten(t, f, method="biweight", window_length=0.5, break_tolerance=0.5, mask=tm); ok = np.isfinite(flat)
        d, de, n = box_depth(t[ok], flat[ok], P, T0, dur)
        print(f"   {name:9s} ({int(m.sum()):2d} px): depth {d*1e6:6.0f} +- {de*1e6:4.0f} ppm  rms {np.std(flat[ok])*1e6:.0f}")
