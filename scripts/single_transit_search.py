"""Single-transit (and duotransit) search of the QLP FFI pool, keeping the scattered-light-flagged cadences.
Motivation: the external review found a 1 %-deep transit of TIC 89247735 inside QLP-flagged (bit 2^30) cadences that the periodic
search had discarded; periodic pipelines also need >= 2 transits per sector and miss P > ~13 d. This search looks for individual
box-shaped dips of 1.5-8 h in every sector, vets each event on its own, and matches events across sectors later (single_rank.py).

Cadence policy: drop NaN flux and TESS bits 2 (safe mode), 4 (coarse point), 8 (earth point), 32 (desaturation), 128 (manual exclude);
KEEP bit 2048 (stray light) and QLP bit 2^30 (ramp). Flux: SAP_FLUX (DET_FLUX is QLP-detrended and not trustworthy in flagged regions).
Detector: stage 1 = biweight (1 d) detrend + sliding box at 6 durations with local noise from +-3-duration windows (SNR > 5 kept);
stage 2 = refit of box + local linear baseline on the UNdetrended SAP flux in the +-3-duration window (final SNR, depth).
Per-event metrics: pre/post baseline difference, fraction of in-transit points below baseline, box-vs-V delta-chi2, SAP_BKG in/out ratio,
SAP_X/Y in-out shift, fraction of in-transit cadences flagged, time since orbit start, nearest momentum dump, camera/CCD.
Known catalog transits (TOI/CTOI) are masked before detection unless --keep-known.
Usage: python -I single_transit_search.py [--workers 12] [--tics 89247735 ...] [--limit N] [--invert] [--keep-known] [--out DIR]"""
import sys, os, glob, re, json, argparse, warnings, time, traceback; warnings.filterwarnings("ignore"); sys.path.insert(0, "/Users/fernando/Desktop/NASA/scripts")
import numpy as np, pandas as pd
from astropy.io import fits
from wotan import flatten
ROOT = "/Users/fernando/Desktop/NASA"; LC_DIR = f"{ROOT}/data/qlp"
DROP_BITS = 2 | 4 | 8 | 32 | 128
DURS_H = np.array([1.5, 2.0, 3.0, 4.0, 6.0, 8.0])
_dumps = None; _known = None

def momentum_dumps():
    global _dumps
    if _dumps is None:
        md = pd.read_csv(f"{ROOT}/catalogs/Table_of_momentum_dumps.csv", comment="#", header=None); _dumps = pd.to_numeric(md.iloc[:, 1], errors="coerce").dropna().values
    return _dumps

def known_signals():
    """dict tic -> list of (epoch_btjd, period, dur_h) from TOI + CTOI tables."""
    global _known
    if _known is None:
        k = {}
        toi = pd.read_csv(f"{ROOT}/catalogs/toi.csv", low_memory=False)
        for _, r in toi.iterrows():
            try: k.setdefault(int(r["TIC ID"]), []).append((float(r["Epoch (BJD)"]) - 2457000, float(r["Period (days)"]), float(r["Duration (hours)"])))
            except Exception: pass
        ctoi = pd.read_csv(f"{ROOT}/catalogs/ctoi.csv", low_memory=False)
        for _, r in ctoi.iterrows():
            try: k.setdefault(int(r["TIC ID"]), []).append((float(r["Transit Epoch (BJD)"]) - 2457000, float(r["Period (days)"]), float(r["Duration (hrs)"])))
            except Exception: pass
        _known = k
    return _known

def sector_files(tic): return sorted(glob.glob(f"{LC_DIR}/hlsp_qlp_tess_ffi_s*-{tic:016d}_tess_v01_llc.fits"), key=lambda f: int(re.search(r"s(\d{4})-", f).group(1)))

def load(path):
    with fits.open(path, memmap=False) as h:
        d = h[1].data; hd = h[0].header; cols = h[1].columns.names
        t = np.asarray(d["TIME"], float); f = np.asarray(d["SAP_FLUX"], float); q = np.asarray(d["QUALITY"], int)
        bkg = np.asarray(d["SAP_BKG"], float) if "SAP_BKG" in cols else np.full_like(f, np.nan)
        x = np.asarray(d["SAP_X"], float) if "SAP_X" in cols else np.full_like(f, np.nan); y = np.asarray(d["SAP_Y"], float) if "SAP_Y" in cols else np.full_like(f, np.nan)
        orb = np.asarray(d["ORBITID"], int) if "ORBITID" in cols else np.zeros(len(t), int)
        meta = dict(tic=int(hd["TICID"]), sector=int(hd["SECTOR"]), camera=int(hd.get("CAMERA", 0)), ccd=int(hd.get("CCD", 0)), tmag=hd.get("TESSMAG"), teff=hd.get("TEFF"), rad=hd.get("RADIUS"), ra=hd.get("RA_OBJ"), dec=hd.get("DEC_OBJ"))
    ok = np.isfinite(t) & np.isfinite(f) & (f > 0) & ((q & DROP_BITS) == 0)
    t, f, q, bkg, x, y, orb = t[ok], f[ok], q[ok], bkg[ok], x[ok], y[ok], orb[ok]
    f = f / np.nanmedian(f)
    ok2 = np.abs(f - 1) < 0.5   # drop flux dropouts / saturation excursions (> 50 % of the median), which are data failures not transits
    t, f, q, bkg, x, y, orb = t[ok2], f[ok2], q[ok2], bkg[ok2], x[ok2], y[ok2], orb[ok2]
    # time since the start of the orbit segment (ORBITID if present, else gaps > 0.5 d)
    if orb.max() == orb.min():
        seg = np.concatenate([[0], np.cumsum(np.diff(t) > 0.5)])
    else: seg = orb
    tso = np.empty_like(t)
    for s in np.unique(seg): m = seg == s; tso[m] = t[m] - t[m].min()
    return t, f, q, bkg, x, y, tso, meta

def mask_known(t, tic, pad=1.5):
    m = np.zeros(len(t), bool)
    for ep, P, dh in known_signals().get(tic, []):
        if not (np.isfinite(ep) and np.isfinite(P) and P > 0): continue
        dh = dh if np.isfinite(dh) and dh > 0 else 3.0
        ph = ((t - ep) / P + 0.5) % 1 - 0.5; m |= np.abs(ph * P) < pad * dh / 24 / 2
    return m

def box_scan(t, f, dur_d, step):
    """Sliding box: returns centre times, depth, SNR using local out-of-transit (+-3 dur, excluding +-0.75 dur) MAD noise."""
    out = []
    if len(t) < 20: return out
    centres = np.arange(t.min() + dur_d, t.max() - dur_d, step)
    for tc in centres:
        intr = np.abs(t - tc) < dur_d / 2; oot = (np.abs(t - tc) > 0.75 * dur_d) & (np.abs(t - tc) < 3 * dur_d)
        if intr.sum() < 4 or oot.sum() < 12: continue
        base = np.median(f[oot]); sig = 1.4826 * np.median(np.abs(f[oot] - base))
        if sig <= 0: continue
        d = base - np.mean(f[intr]); out.append((tc, d, d / (sig / np.sqrt(intr.sum())), int(intr.sum())))
    return out

def local_fit(t, fraw, tc, dur_d):
    """Stage 2: box + linear baseline on raw flux in +-3 dur. Returns depth, depth_err, snr, baseline metrics, box-vs-V delta-chi2."""
    w = np.abs(t - tc) < 3 * dur_d; tt, ff = t[w], fraw[w]
    if w.sum() < 20: return None
    intr = np.abs(tt - tc) < dur_d / 2
    if intr.sum() < 4 or (~intr).sum() < 12: return None
    x = tt - tc; A = np.vstack([np.ones_like(x), x, -intr.astype(float)]).T
    c, *_ = np.linalg.lstsq(A, ff, rcond=None); res = ff - A @ c; sig = 1.4826 * np.median(np.abs(res[~intr]))
    if sig <= 0: return None
    cov = np.linalg.inv(A.T @ A) * sig ** 2; depth, derr = c[2], np.sqrt(cov[2, 2]); chi_box = np.sum(res ** 2) / sig ** 2
    # V-shaped alternative: triangular dip of the same half-width
    tri = np.clip(1 - np.abs(x) / (dur_d / 2), 0, None); Av = np.vstack([np.ones_like(x), x, -tri]).T
    cv, *_ = np.linalg.lstsq(Av, ff, rcond=None); chi_v = np.sum((ff - Av @ cv) ** 2) / sig ** 2
    chi_flat = np.sum((ff - np.polyval(np.polyfit(x, ff, 1), x)) ** 2) / sig ** 2
    pre = (x < -0.75 * dur_d); post = (x > 0.75 * dur_d)
    base = c[0] + c[1] * x; pre_post = (np.median(ff[pre] - base[pre]) - np.median(ff[post] - base[post])) / (sig / np.sqrt(min(pre.sum(), post.sum()) or 1)) if pre.sum() > 3 and post.sum() > 3 else np.nan
    frac_below = float(np.mean(ff[intr] < base[intr]));
    # ingress/egress sharpness: compare first/last quarter of the box to the middle
    mid = np.abs(x) < dur_d / 4; edge = intr & ~mid
    bottom_ratio = float((np.mean(base[edge] - ff[edge]) / depth)) if edge.sum() >= 2 and depth != 0 else np.nan
    return dict(depth=float(depth), depth_err=float(derr), snr=float(depth / derr), dchi2_flat=float(chi_flat - chi_box), dchi2_box_minus_v=float(chi_v - chi_box), pre_post_sig=float(pre_post) if np.isfinite(pre_post) else None, frac_below=frac_below, bottom_ratio=bottom_ratio, n_in=int(intr.sum()), n_win=int(w.sum()), sig_local=float(sig))

def process_sector(path, invert=False, keep_known=False, snr1=5.0, snr2=7.0):
    t, f, q, bkg, x, y, tso, meta = load(path)
    if len(t) < 300 or not np.isfinite(f).any(): return meta, []
    if invert: f = 2 - f
    km = np.zeros(len(t), bool) if keep_known else mask_known(t, meta["tic"])
    # stage 1 on detrended flux (known transits masked out of the detrend AND the scan)
    try: flat = flatten(t, f, method="biweight", window_length=1.0, return_trend=False)
    except Exception: return meta, []
    good = np.isfinite(flat) & ~km
    # upward-only clip (flares) at 5 sigma
    sig0 = 1.4826 * np.nanmedian(np.abs(flat[good] - 1)); good &= flat < 1 + 5 * sig0
    tg, fg = t[good], flat[good]
    cands = []
    for dh in DURS_H:
        dd = dh / 24
        for tc, d, snr, nin in box_scan(tg, fg, dd, dd / 4):
            if snr > snr1 and 0 < d < 0.2: cands.append((tc, dd, snr))
    # merge overlapping stage-1 hits: keep the best SNR within +-max(dur) clusters
    cands.sort(key=lambda c: -c[2]); kept = []
    for tc, dd, snr in cands:
        if all(abs(tc - k[0]) > max(dd, k[1]) for k in kept): kept.append((tc, dd, snr))
    events = []; dumps = momentum_dumps()
    for tc, dd, snr1v in kept[:80]:
        # stage 2 on raw flux, refine duration among neighbours and centre on a fine grid
        best = None
        for dh in DURS_H[(DURS_H / 24 > dd / 1.6) & (DURS_H / 24 < dd * 1.6)]:
            for tc2 in np.arange(tc - dd / 2, tc + dd / 2 + 1e-9, dd / 8):
                r = local_fit(t[~km], f[~km], tc2, dh / 24)
                if r and (best is None or r["snr"] > best[0]["snr"]): best = (r, tc2, dh)
        if best is None or best[0]["snr"] < snr2: continue
        r, tc2, dh = best; intr = np.abs(t - tc2) < dh / 48; oot = (np.abs(t - tc2) > 0.75 * dh / 24) & (np.abs(t - tc2) < 3 * dh / 24)
        bk = float(np.nanmedian(bkg[intr]) / np.nanmedian(bkg[oot])) if np.isfinite(bkg).any() and oot.sum() and np.nanmedian(bkg[oot]) != 0 else None
        cx = float(np.nanmean(x[intr]) - np.nanmean(x[oot])) if np.isfinite(x).any() else None; cy = float(np.nanmean(y[intr]) - np.nanmean(y[oot])) if np.isfinite(y).any() else None
        cx_sig = float(np.nanstd(x[oot]) / np.sqrt(max(intr.sum(), 1))) if np.isfinite(x).any() else None
        events.append(dict(tc=float(tc2), dur_h=float(dh), snr1=float(snr1v), **r, bkg_ratio=bk, dx=cx, dy=cy, cxy_err=cx_sig, frac_flagged=float(np.mean(q[intr] != 0)) if intr.sum() else None,
                           t_since_orbit_start=float(np.median(tso[intr])) if intr.sum() else None, dump_dt_h=float(np.min(np.abs(dumps - tc2)) * 24), sector=meta["sector"], camera=meta["camera"], ccd=meta["ccd"]))
    events.sort(key=lambda e: -e["snr"])
    return meta, events

def process(tic, out_dir, invert=False, keep_known=False):
    t0 = time.time(); res = dict(tic=tic, sectors={}, events=[])
    try:
        for p in sector_files(tic):
            meta, ev = process_sector(p, invert=invert, keep_known=keep_known)
            res["sectors"][meta["sector"]] = dict(camera=meta["camera"], ccd=meta["ccd"]); res["meta"] = {k: meta[k] for k in ("tmag", "teff", "rad", "ra", "dec")}; res["events"] += ev
        res["elapsed"] = time.time() - t0
        json.dump(res, open(f"{out_dir}/{tic}.json", "w"), default=float)
        return dict(tic=tic, n_events=len(res["events"]), best_snr=max([e["snr"] for e in res["events"]], default=0), elapsed=res["elapsed"])
    except Exception:
        return dict(tic=tic, error=traceback.format_exc()[-400:])

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--workers", type=int, default=12); ap.add_argument("--tics", type=int, nargs="*"); ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--invert", action="store_true"); ap.add_argument("--keep-known", action="store_true"); ap.add_argument("--out", default=""); ap.add_argument("--redo", action="store_true"); a = ap.parse_args()
    out_dir = a.out or f"{ROOT}/results/single" + ("_inverted" if a.invert else ""); os.makedirs(out_dir, exist_ok=True)
    tics = a.tics or sorted({int(re.search(r"-(\d{16})_", f).group(1)) for f in glob.glob(f"{LC_DIR}/*.fits")})
    if a.limit: tics = tics[:a.limit]
    if not a.redo: tics = [t for t in tics if not os.path.exists(f"{out_dir}/{t}.json")]
    print(f"single-transit search: {len(tics)} targets, {a.workers} workers, invert={a.invert}, out={out_dir}", flush=True)
    known_signals(); momentum_dumps()
    from concurrent.futures import ProcessPoolExecutor, as_completed
    n = 0
    with ProcessPoolExecutor(a.workers) as ex:
        futs = [ex.submit(process, t, out_dir, a.invert, a.keep_known) for t in tics]
        for fu in as_completed(futs):
            r = fu.result(); n += 1
            if "error" in r: print(f"[{n}/{len(tics)}] TIC {r['tic']} ERROR {r['error'][-200:]}", flush=True)
            elif n % 25 == 0 or r["n_events"]: print(f"[{n}/{len(tics)}] TIC {r['tic']} events={r['n_events']} bestSNR={r['best_snr']:.1f} {r['elapsed']:.0f}s", flush=True)
