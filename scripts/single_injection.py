"""Injection-recovery test for the single-transit detector: inject batman transits (depth 1-20 ppt log-uniform, duration 2-8 h,
b = 0.3, random mid-time anywhere in the sector INCLUDING flagged ramps) into the raw SAP flux of random Pool-B stars (one sector each),
run the identical detector + event cuts, and record recovery vs expected SNR and vs time since orbit start.
Usage: python -I single_injection.py --n 300 --workers 8"""
import sys, os, glob, re, json, argparse, warnings; warnings.filterwarnings("ignore"); sys.path.insert(0, "/Users/fernando/Desktop/NASA/scripts")
import numpy as np, pandas as pd
import single_transit_search as sts
from single_rank import event_cuts
import batman
ROOT = "/Users/fernando/Desktop/NASA"
_inj = {}

def load_injected(path):
    t, f, q, bkg, x, y, tso, meta = sts._load_orig(path)
    p = _inj.get(path)
    if p is not None:
        pr = batman.TransitParams(); pr.t0 = p["tc"]; pr.per = 1000.0; pr.rp = np.sqrt(p["depth"]); pr.a = (1000.0 / (p["dur_h"] / 24) / np.pi) * (1 + pr.rp)  # a/R* giving the requested full duration at b~0
        pr.inc = 90.0; pr.ecc = 0; pr.w = 90; pr.u = [0.4, 0.25]; pr.limb_dark = "quadratic"
        m = batman.TransitModel(pr, t, supersample_factor=3, exp_time=10 / 1440).light_curve(pr); f = f * m
    return t, f, q, bkg, x, y, tso, meta

def one(args):
    path, tc, depth, dur_h, seed = args
    if not hasattr(sts, '_load_orig'): sts._load_orig = sts.load; sts.load = load_injected   # spawned workers re-import the module
    _inj[path] = dict(tc=tc, depth=depth, dur_h=dur_h)
    try:
        meta, ev = sts.process_sector(path)
        t, f, q, bkg, x, y, tso, _ = sts._load_orig(path)
        intr = np.abs(t - tc) < dur_h / 48; n_in = int(intr.sum()); oot = (np.abs(t - tc) > dur_h / 24) & (np.abs(t - tc) < 3 * dur_h / 24)
        sig = 1.4826 * np.median(np.abs(f[oot] - np.median(f[oot]))) if oot.sum() > 10 else np.nan
        snr_exp = depth / (sig / np.sqrt(max(n_in, 1))) if sig and sig > 0 else np.nan
        df = pd.DataFrame(ev) if ev else pd.DataFrame()
        hit = None
        if len(df):
            near = df[(np.abs(df.tc - tc) * 24 < 1.5) & (df.depth > 0.5 * depth) & (df.depth < 2 * depth)]
            if len(near):
                near = near.sort_values("snr", ascending=False); hit = near.iloc[0].to_dict(); hit["passes_cuts"] = bool(event_cuts(near.head(1)).iloc[0])
        return dict(path=os.path.basename(path), tic=meta["tic"], sector=meta["sector"], tc=tc, depth=depth, dur_h=dur_h, n_in=n_in, tso=float(np.median(tso[intr])) if n_in else np.nan, frac_flagged=float(np.mean(q[intr] != 0)) if n_in else np.nan,
                    snr_expected=float(snr_exp), detected=hit is not None, passes_cuts=bool(hit["passes_cuts"]) if hit else False, snr_found=float(hit["snr"]) if hit else np.nan, depth_found=float(hit["depth"]) if hit else np.nan)
    except Exception as e:
        return dict(path=os.path.basename(path), error=repr(e)[:200])

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--n", type=int, default=300); ap.add_argument("--workers", type=int, default=8); a = ap.parse_args()
    sts._load_orig = sts.load; sts.load = load_injected
    rng = np.random.default_rng(11); files = sorted(glob.glob(f"{sts.LC_DIR}/*.fits")); pick = rng.choice(files, a.n, replace=False)
    jobs = []
    for p in pick:
        t = sts._load_orig(p)[0]
        if len(t) < 500: continue
        tc = float(rng.uniform(t.min() + 0.1, t.max() - 0.1)); depth = float(10 ** rng.uniform(-3, np.log10(0.02))); dur = float(rng.choice([2.0, 3.0, 4.0, 6.0, 8.0]))
        jobs.append((p, tc, depth, dur, 0))
    from concurrent.futures import ProcessPoolExecutor
    with ProcessPoolExecutor(a.workers) as ex: res = list(ex.map(one, jobs))
    df = pd.DataFrame(res); df.to_csv(f"{ROOT}/results/single/injection_recovery.csv", index=False)
    d = df[df.error.isna()] if "error" in df else df; d = d[d.n_in >= 4]
    print(f"injections with >= 4 in-transit cadences: {len(d)}")
    for lo, hi in [(0, 5), (5, 7), (7, 10), (10, 15), (15, 30), (30, 1e9)]:
        m = (d.snr_expected >= lo) & (d.snr_expected < hi)
        if m.sum(): print(f"  expected SNR {lo:>4.0f}-{hi:<4.0f}: n={m.sum():3d} detected {d[m].detected.mean():.2f} pass cuts {d[m].passes_cuts.mean():.2f}")
    for lo, hi in [(0, 0.5), (0.5, 1), (1, 2), (2, 100)]:
        m = (d.tso >= lo) & (d.tso < hi) & (d.snr_expected >= 10)
        if m.sum(): print(f"  time since orbit start {lo}-{hi} d (SNR>=10): n={m.sum():3d} detected {d[m].detected.mean():.2f} pass cuts {d[m].passes_cuts.mean():.2f}")
    m = (d.frac_flagged > 0.5) & (d.snr_expected >= 10); print(f"  in flagged cadences (>50 %, SNR>=10): n={m.sum()} detected {d[m].detected.mean() if m.sum() else float('nan'):.2f} pass cuts {d[m].passes_cuts.mean() if m.sum() else float('nan'):.2f}")
