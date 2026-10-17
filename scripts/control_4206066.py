"""Positive control: recover the reported 3.18 d / ~500 ppm signal on TIC 4206066 with the project's BLS machinery.
Data: S98 QLP (200 s FFI), S6 TESS-SPOC (1800 s FFI), S32 SPOC (120 s). Blind-style: search S98 alone, then test S6/S32."""
import sys, json, warnings, os; sys.path.insert(0, "/Users/fernando/Desktop/NASA/scripts")
warnings.filterwarnings("ignore")
import numpy as np, lightkurve as lk
from tsearch import detrend
from search_pipeline import period_grid, bls_stats, bin_lc
OUT = "/Users/fernando/Desktop/NASA/results/control_TIC4206066"; os.makedirs(OUT, exist_ok=True)
sr = lk.search_lightcurve("TIC 4206066")
def get(sector, prefs=("SPOC", "TESS-SPOC", "QLP")):
    for a in prefs:
        s = sr[(sr.author == a) & (sr.mission == f"TESS Sector {sector:02d}")]
        if len(s):
            return s[0].download(download_dir="/Users/fernando/Desktop/NASA/data/lk_cache"), a
    return None, None
durs = np.array([1.0, 1.5, 2.0, 3.0]) / 24
res = {}; data = {}
for sec in (98, 6, 32):
    lc, author = get(sec)
    lc = lc.remove_nans()
    if "quality" in lc.columns: lc = lc[lc.quality == 0]
    lc = lc.normalize()
    t, f = lc.time.value, lc.flux.value.astype(float)
    fe = lc.flux_err.value.astype(float) if np.all(np.isfinite(lc.flux_err.value)) else np.full_like(f, np.std(f))
    td, fd, m, _ = detrend(t, f, window=0.5); fed = fe[m]
    data[sec] = (td, fd, fed)
    base = td.max() - td.min()
    pg = period_grid(base, 0.5, 13, durs.min(), oversample=3)
    peaks = bls_stats(td, fd, fed, pg, durs)
    print(f"S{sec} {author}: N={len(td)} cadence={np.median(np.diff(td))*1440:.0f}min rms={np.std(fd)*1e6:.0f}ppm", flush=True)
    for p in peaks: print(f"   P={p['period']:.4f} T0={p['t0']:.3f} depth={p['depth']*1e6:.0f}ppm dur={p['duration_h']:.1f}h SNR={p['snr']:.1f} SDE={p['sde']:.1f} Ntr={p['n_transits']}", flush=True)
    res[sec] = dict(author=author, n=len(td), rms_ppm=float(np.std(fd)*1e6), peaks=peaks)
# Did S98 alone recover P~3.18?
P98 = res[98]["peaks"][0]["period"]; T098 = res[98]["peaks"][0]["t0"]
print(f"\nS98 top peak P={P98:.4f}; reported 3.18 d -> {'RECOVERED' if abs(P98-3.18)<0.02 or abs(P98*2-3.18)<0.02 or abs(P98/2-3.18)<0.02 else 'NOT top peak'}")
# Fixed-period test in S6 and S32: fold at S98 period, scan epoch, measure depth at best epoch vs noise
for sec in (6, 32):
    td, fd, fed = data[sec]
    best = None
    for ph0 in np.linspace(0, P98, 400, endpoint=False):
        ph = ((td - T098 - ph0) / P98 + 0.5) % 1 - 0.5
        intr = np.abs(ph * P98) < 1.0 / 24
        if intr.sum() < 3: continue
        d = 1 - np.mean(fd[intr]); de = np.std(fd[~intr]) / np.sqrt(intr.sum())
        if best is None or d / de > best[0]: best = (d / de, d, de, ph0, int(intr.sum()))
    # phase offset expected if ephemeris exact = 0 (modulo period); report
    print(f"S{sec}: best in-transit depth at P={P98:.4f}: {best[1]*1e6:.0f}+-{best[2]*1e6:.0f} ppm (SNR {best[0]:.1f}) at epoch offset {best[3]:.3f} d (of {P98:.3f}); n_in={best[4]}")
    res[sec]["fixedP_test"] = dict(snr=best[0], depth=best[1], err=best[2], offset=best[3])
json.dump(res, open(f"{OUT}/control_results.json", "w"), indent=1, default=float)
np.savez(f"{OUT}/control_data.npz", **{f"S{k}": np.vstack(v) for k, v in data.items()})
