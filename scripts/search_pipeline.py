"""Stage A/B search: per-target, load all SPOC 2-min sectors, detrend per sector, BLS per sector and on the stitched
multi-year light curve. Writes one JSON per target to results/search/ and a summary CSV.
Usage: python -I search_pipeline.py [--limit N] [--workers W] [--tics 123,456]
"""
import sys, os, glob, json, re, time, argparse, warnings, traceback
sys.path.insert(0, "/Users/fernando/Desktop/NASA/scripts")
warnings.filterwarnings("ignore")
import numpy as np
from astropy.timeseries import BoxLeastSquares
from tsearch import load_spoc_lc, load_qlp_lc, detrend
SOURCE = os.environ.get("TSEARCH_SOURCE", "spoc")

def bin_lc(t, f, fe, dt):
    """Bin to cadence dt (days), weighted mean; errors from propagated weights."""
    if dt <= 0: return t, f, fe
    idx = np.floor((t - t.min()) / dt).astype(int)
    uniq, inv = np.unique(idx, return_inverse=True)
    w = 1 / fe**2
    sw = np.bincount(inv, w); st = np.bincount(inv, w * t); sf = np.bincount(inv, w * f)
    return st / sw, sf / sw, 1 / np.sqrt(sw)

LC = "/Users/fernando/Desktop/NASA/data/lc" if SOURCE == "spoc" else "/Users/fernando/Desktop/NASA/data/qlp"
OUT = "/Users/fernando/Desktop/NASA/results/search" if SOURCE == "spoc" else "/Users/fernando/Desktop/NASA/results/search_qlp"
os.makedirs(OUT, exist_ok=True)

def sector_files(tic):
    if SOURCE == "spoc": pat = f"{LC}/*-s????-{tic:016d}-*_lc.fits"
    else: pat = f"{LC}/hlsp_qlp_tess_ffi_s????-{tic:016d}_tess_v01_llc.fits"
    return sorted(glob.glob(pat), key=lambda f: int(re.search(r"s(\d{4})-", f).group(1)))

def load_lc(path):
    return load_spoc_lc(path) if SOURCE == "spoc" else load_qlp_lc(path)

def period_grid(baseline, pmin, pmax, min_dur_d, oversample=2.5):
    """Frequency grid with step df = min_dur/(P*T)/oversample  ->  uniform in log f with step dln f = min_dur/T/oversample."""
    fmin, fmax = 1 / pmax, 1 / pmin
    dlnf = min_dur_d / baseline / oversample
    n = int(np.ceil(np.log(fmax / fmin) / dlnf)) + 1
    return 1 / np.exp(np.linspace(np.log(fmin), np.log(fmax), n))

def bls_stats(t, f, fe, periods, durs, min_transits=2):
    bls = BoxLeastSquares(t, f, dy=fe)
    res = bls.power(periods, durs, objective="snr")
    pw = np.asarray(res.power); pw[~np.isfinite(pw)] = 0
    # Clean SDE: subtract running median in log-period, divide by robust std
    k = max(51, len(pw) // 200 | 1)
    from scipy.ndimage import median_filter
    base = median_filter(pw, size=k, mode="nearest")
    resid = pw - base
    mad = np.median(np.abs(resid - np.median(resid))) * 1.4826 + 1e-12
    sde_arr = resid / mad
    order = np.argsort(sde_arr)[::-1]
    peaks = []
    for i in order:
        if all(abs(res.period[i] - p["period"]) / p["period"] > 0.01 for p in peaks):
            st = bls.compute_stats(res.period[i], res.duration[i], res.transit_time[i])
            ntr = int(np.sum(st["per_transit_count"] > 0))
            peaks.append(dict(period=float(res.period[i]), t0=float(res.transit_time[i]), duration_h=float(res.duration[i] * 24),
                              depth=float(res.depth[i]), depth_err=float(res.depth_err[i]), snr=float(pw[i]), sde=float(sde_arr[i]),
                              n_transits=ntr, depth_odd=float(st["depth_odd"][0]), depth_odd_err=float(st["depth_odd"][1]),
                              depth_even=float(st["depth_even"][0]), depth_even_err=float(st["depth_even"][1]),
                              depth_half=float(st["depth_half"][0]), depth_half_err=float(st["depth_half"][1]),
                              depth_phased=float(st["depth_phased"][0]),
                              per_transit_ll=[float(x) for x in st["per_transit_log_likelihood"]],
                              transit_times=[float(x) for x in st["transit_times"]]))
        if len(peaks) >= 3: break
    return peaks

def year_of(t_btjd):  # BTJD -> calendar year (approx)
    return 2000 + int((t_btjd + 2457000 - 2451544.5) // 365.25)

def process(tic):
    t0 = time.time()
    try:
        files = sector_files(tic)
        if not files: return dict(tic=tic, error="no files")
        secs = {}; meta = None
        for fpath in files:
            try:
                t, f, fe, m = load_lc(fpath)
            except Exception as e:
                continue
            if len(t) < (2000 if SOURCE == "spoc" else 400): continue
            td, fd, mask, _ = detrend(t, f, window=0.5)
            fed = fe[mask]
            secs[m["sector"]] = (td, fd, fed, m)
            meta = meta or m
        if not secs: return dict(tic=tic, error="no usable sectors")
        out = dict(tic=tic, meta={k: v for k, v in meta.items() if k not in ("sector",)}, sectors={}, n_sectors=len(secs))
        durs = np.array([1.0, 1.5, 2.0, 3.0, 4.0]) / 24
        # per-sector search
        for s, (td, fd, fed, m) in secs.items():
            base = td.max() - td.min()
            pg = period_grid(base, 0.5, max(1.0, base / 2), durs.min(), oversample=3)
            tb, fb, eb = bin_lc(td, fd, fed, 6 / 1440)
            peaks = bls_stats(tb, fb, eb, pg, durs)
            out["sectors"][s] = dict(n=len(td), rms_ppm=float(np.std(fd) * 1e6), baseline=float(base), crowdsap=m["crowdsap"],
                                     year=year_of(td.mean()), peaks=peaks)
        # stitched search
        T = np.concatenate([v[0] for v in secs.values()]); F = np.concatenate([v[1] for v in secs.values()]); E = np.concatenate([v[2] for v in secs.values()])
        o = np.argsort(T); T, F, E = T[o], F[o], E[o]
        base = T.max() - T.min()
        pmax = 20.0 if base > 60 else max(1.0, base / 2)
        pg = period_grid(base, 0.5, pmax, durs.min(), oversample=2.0)
        Tb, Fb, Eb = bin_lc(T, F, E, 10 / 1440)
        out["stitched"] = dict(n=len(T), n_binned=len(Tb), baseline=float(base), n_periods=len(pg), rms_ppm=float(np.std(F) * 1e6),
                               years=sorted({year_of(v[0].mean()) for v in secs.values()}), peaks=bls_stats(Tb, Fb, Eb, pg, durs))
        # per-year consistency for the top stitched peak: fit depth at fixed P, T0, dur in each year
        bp = out["stitched"]["peaks"][0]
        yrs = {}
        for s, (td, fd, fed, m) in secs.items():
            y = year_of(td.mean())
            ph = ((td - bp["t0"]) / bp["period"] + 0.5) % 1 - 0.5
            intr = np.abs(ph * bp["period"]) < bp["duration_h"] / 48
            if intr.sum() < 3: continue
            d = 1 - np.mean(fd[intr]); de = np.std(fd[~intr]) / np.sqrt(intr.sum())
            yrs.setdefault(y, []).append((d, de, int(intr.sum())))
        out["stitched"]["per_year"] = {str(y): dict(depth=float(np.average([a for a, b, c in v], weights=[1 / b**2 for a, b, c in v])),
                                                    err=float(1 / np.sqrt(sum(1 / b**2 for a, b, c in v))), n_in=int(sum(c for a, b, c in v))) for y, v in yrs.items()}
        out["elapsed"] = time.time() - t0
        json.dump(out, open(f"{OUT}/{tic}.json", "w"), default=float)
        return dict(tic=tic, ok=True, sde=bp["sde"], period=bp["period"], elapsed=out["elapsed"])
    except Exception as e:
        return dict(tic=tic, error=traceback.format_exc()[-500:])

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--limit", type=int, default=0); ap.add_argument("--workers", type=int, default=12)
    ap.add_argument("--tics", type=str, default=""); ap.add_argument("--redo", action="store_true")
    a = ap.parse_args()
    import pandas as pd
    if a.tics: tics = [int(x) for x in a.tics.split(",")]
    elif SOURCE == "spoc": tics = pd.read_csv("/Users/fernando/Desktop/NASA/catalogs/s107_dwarf_targets.csv").ID.astype(int).tolist()
    else: tics = sorted({int(re.search(r"-(\d{16})_", f).group(1)) for f in glob.glob(f"{LC}/*.fits")})
    if not a.redo: tics = [t for t in tics if not os.path.exists(f"{OUT}/{t}.json")]
    if a.limit: tics = tics[:a.limit]
    print(f"processing {len(tics)} targets with {a.workers} workers", flush=True)
    from multiprocessing import Pool
    done = 0
    with Pool(a.workers) as pool:
        for r in pool.imap_unordered(process, tics):
            done += 1
            if "error" in r: print(f"[{done}] TIC {r['tic']} ERROR {r['error'][:200]}", flush=True)
            elif done % 25 == 0 or a.tics: print(f"[{done}/{len(tics)}] TIC {r['tic']} SDE={r['sde']:.1f} P={r['period']:.4f} {r['elapsed']:.0f}s", flush=True)
