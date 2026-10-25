"""DOCSTRING CORRECTED 2026-10-25 (DECISIONS 187, 189); the code is unchanged from the version that ran (SHA-256 63738417451a42d2...).
The H0 design below yields a STRUCTURAL ZERO for PASS (fixed noise-only BLS peaks never hit the allowed trial periods), so its output
is a conditional diagnostic, not a calibrated null rate.
Real-noise calibration of the locked TIC 317134140 scorer v1.3 (2026-10-25; DECISIONS 185-186). It runs on TRAINING sectors only
(S6, S87, S98, S107; data/lc). The interpretation rule this feeds (hypotheses, LR estimator, pooling, combination, verbal scale) was
logged in DECISIONS 185. The author logged the rule as fixed at 02:20 UTC; available local timestamps are consistent with that account,
but do not independently prove insertion time (documentation-only correction, DECISIONS 189).
- Locked code: the scorer's own preprocess(), clause_a(), clause_b() and sector_outcome() are imported unchanged (SHA-256 asserted).
  For a trial at test period P', the module's period constant P_SIG is set to P' (clause A's random-shift range and clause B's hit
  test use it). Nothing else is changed. The injected light curve is written as a copy of the real SPOC FITS file with only its
  PDCSAP_FLUX column changed, so the scorer's loading, quality mask, edge trim, TOI mask, detrending and clipping all apply as locked.
- Control: P' = P at the frozen phase on the unmodified file must reproduce results/conformance_317134140/insample_v1.3b_S<s>.json
  for the eleven scientific fields listed in the control comparison (this does not exercise every validation/provenance path; the
  output's control string 'field for field' overstates in the same way; documentation-only correction, DECISIONS 189); otherwise the
  script stops and no calibration is written.
- Cleaning: the real 0.5719-d signal is divided out with the registration's transit shape (vet.transit_model; T0 BTJD 1468.67922,
  P 0.5718634 d, rp/R* 0.0131, a/R* 2.6666, b 0.4024, quadratic u = 0.4, 0.25, 2-min exposure). The residual clause-A depth at the true
  ephemeris on the cleaned data is recorded per sector.
- H1 trials: that shape is injected at P' drawn uniformly in [0.53, 0.70] d (excluding |P'/P - 1| < 2 %, P/2 and 2P, and within 2 % of
  the TOI-2514.01 harmonics 6.3951381/n) with a uniform random phase. a/R* is scaled as 2.6666 x P'/P. CORRECTION 2026-10-25
  (DECISIONS 187): this holds the duration only APPROXIMATELY; the injected geometric T14 was 1.554-1.584 h. 1.5 h is clause A's
  scoring window, not the injected T14. rp/R* is set so that the NOISELESS model's mean
  in-transit depth over +-0.75 h, against the out-of-transit median, equals the target depth (the way clause A measures it).
- H0 trials: the cleaned data, no injection, scored at random (P', phase). The data do not depend on (P', phase), so preprocessing and
  the BLS run once per sector; clause A runs per trial and clause B's hit test is applied to the fixed top 3 at each P'.
Usage: python -I calibrate_317134140_scorer.py OUT.json TMPDIR [--n185 100 --n-side 50 --n-null 2000 --workers 12]"""
import sys, os, json, glob, hashlib, argparse, warnings, time
import numpy as np
warnings.filterwarnings("ignore")
R = "/Users/fernando/Desktop/NASA"; sys.path.insert(0, f"{R}/scripts")
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
LOCKED = {"prereg_spoc_317134140.py": "f3f55c0d74733f8aa4ee6264b99c29c547990d885d5cfdd2c29c43c47baa1613"}
P0, T00, RP0, AR0, B0 = 0.5718634, 1468.67922, 0.0131, 2.6666, 0.4024
P_TOI = 6.3951381
SECTORS = (6, 87, 98, 107)

def lc_path(s): return glob.glob(f"{R}/data/lc/*-s{s:04d}-0000000317134140-*-s_lc.fits")[0]

def model(t, T0, P, rp, ar):
    from vet import transit_model
    out = np.ones(len(t)); ok = np.isfinite(t)
    out[ok] = transit_model([T0, rp, ar, B0], t[ok], P, exp_time=120 / 86400)
    return out

def measured_depth(P, rp, ar):
    """Noiseless depth as clause A measures it: median OOT (0.75-3 h) minus mean in-transit (+-0.75 h), in ppm."""
    t = np.arange(-0.2, 0.2, 2 / 1440); f = model(t, 0.0, P, rp, ar); d = np.abs(t) * 24
    return (np.median(f[(d > 0.75) & (d < 3.0)]) - np.mean(f[d < 0.75])) * 1e6

def rp_for(depth, P, ar):
    rp = RP0
    for _ in range(6): rp *= np.sqrt(depth / measured_depth(P, rp, ar))
    return rp

def write_variant(src, dst, factor):
    from astropy.io import fits
    with fits.open(src, memmap=False) as h:
        h[1].data["PDCSAP_FLUX"] = h[1].data["PDCSAP_FLUX"] * factor
        h.writeto(dst)

def score(S, path, P, T0, top3=None, pre=None):
    """Run the locked functions at period P / reference epoch T0. Returns the outcome record (and the preprocessed arrays for reuse)."""
    S.P_SIG = P
    try: t, f, fe, m = pre if pre is not None else S.preprocess(path)
    except S.Insufficient: return dict(outcome="INSUFFICIENT", clause_a="INSUFFICIENT", clause_b="NOT_RUN"), None
    n0, n1 = int(np.ceil((t.min() - T0) / P)), int(np.floor((t.max() - T0) / P)); tcs = [T0 + n * P for n in range(n0, n1 + 1)]
    r = S.clause_a(t, f, tcs)
    if r["clause_a"] == "INSUFFICIENT": r.update(clause_b="NOT_RUN", outcome="INSUFFICIENT"); return r, (t, f, fe, m)
    if top3 is None: r.update(S.clause_b(t, f, fe))
    else:
        r["clause_b"] = "B_TOP3" if any(abs(p["period"] / P - 1) <= 0.001 for p in top3) else "B_NOT_TOP3"; r["top3"] = top3
    r["outcome"] = S.sector_outcome(r["clause_a"], r["clause_b"]); r["n_cadences"] = int(len(t)); r["toi_mask_removed"] = m["toi_mask_removed"]
    return r, (t, f, fe, m)

def draw_period(rng):
    while True:
        P = rng.uniform(0.53, 0.70)
        if abs(P / P0 - 1) < 0.02 or abs(P / (P0 / 2) - 1) < 0.02 or abs(P / (2 * P0) - 1) < 0.02: continue
        if any(abs(P / (P_TOI / n) - 1) < 0.02 for n in range(1, 30)): continue
        return P

def h1_trial(args):
    sec, depth, i, tmp = args
    import prereg_spoc_317134140 as S
    rng = np.random.default_rng([317134140, sec, int(depth), i]); P = draw_period(rng); T0 = 1468.0 + rng.uniform(0, P)
    src = lc_path(sec)
    from astropy.io import fits
    with fits.open(src, memmap=False) as h: t = np.asarray(h[1].data["TIME"], float)
    ar = AR0 * P / P0; rp = rp_for(depth, P, ar)
    factor = model(t, T00, P0, RP0, AR0) ** -1 * model(t, T0, P, rp, ar)
    dst = f"{tmp}/h1_s{sec}_{int(depth)}_{i}.fits"; write_variant(src, dst, factor)
    r, _ = score(S, dst, P, T0); os.remove(dst)
    return dict(sector=sec, depth_ppm=depth, trial=i, P=P, T0=T0, rp=rp, ar=ar, outcome=r["outcome"], clause_a=r["clause_a"], clause_b=r["clause_b"],
                depth_meas=r.get("depth_ppm"), sigma=r.get("sigma_ppm"), n_eligible=r.get("n_eligible"))

def h0_trial(args):
    sec, i, cleaned, top3 = args
    import prereg_spoc_317134140 as S
    global _PRE
    if _PRE.get(sec) is None: _PRE[sec] = S.preprocess(cleaned)
    rng = np.random.default_rng([317134140, sec, 0, 10_000 + i]); P = draw_period(rng); T0 = 1468.0 + rng.uniform(0, P)
    r, _ = score(S, cleaned, P, T0, top3=top3, pre=_PRE[sec])
    return dict(sector=sec, trial=i, P=P, T0=T0, outcome=r["outcome"], clause_a=r["clause_a"], clause_b=r["clause_b"], depth_meas=r.get("depth_ppm"), sigma=r.get("sigma_ppm"))
_PRE = {}

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("out"); ap.add_argument("tmp"); ap.add_argument("--n185", type=int, default=100); ap.add_argument("--n-side", type=int, default=50)
    ap.add_argument("--n-null", type=int, default=2000); ap.add_argument("--workers", type=int, default=12); ap.add_argument("--sectors", default="6,87,98,107"); a = ap.parse_args()
    if os.path.exists(a.out) or os.path.exists(a.tmp): raise SystemExit("refused: output or tmp exists")
    os.makedirs(a.tmp)
    for f, h in LOCKED.items(): assert sha(f"{R}/scripts/{f}") == h, f"{f} is not the locked v1.3"
    import prereg_spoc_317134140 as S
    secs = [int(x) for x in a.sectors.split(",")]; t_start = time.time()
    res = dict(scorer_sha256=LOCKED["prereg_spoc_317134140.py"], vet_sha256=sha(f"{R}/scripts/vet.py"), rule="DECISIONS 185", sectors={}, h1=[], h0=[])
    # control + cleaning
    for sec in secs:
        ref = json.load(open(f"{R}/results/conformance_317134140/insample_v1.3b_S{sec}.json"))
        r, _ = score(S, lc_path(sec), P0, T00)
        keys = ("outcome", "clause_a", "clause_b", "depth_ppm", "sigma_ppm", "n_eligible", "n_predicted", "n_null", "top3", "n_cadences", "toi_mask_removed")
        diff = [k for k in keys if r.get(k) != ref.get(k)]
        if diff: raise SystemExit(f"CONTROL FAILED for S{sec}: fields {diff} differ from insample_v1.3b; no calibration written")
        from astropy.io import fits
        with fits.open(lc_path(sec), memmap=False) as h: t = np.asarray(h[1].data["TIME"], float)
        cleaned = f"{a.tmp}/clean_s{sec}.fits"; write_variant(lc_path(sec), cleaned, model(t, T00, P0, RP0, AR0) ** -1)
        rc, pre = score(S, cleaned, P0, T00)
        res["sectors"][sec] = dict(control="reproduces insample_v1.3b field for field", real_signal_model_depth_ppm=measured_depth(P0, RP0, AR0),
                                   cleaned_true_ephemeris=dict(outcome=rc["outcome"], clause_a=rc["clause_a"], depth_ppm=rc.get("depth_ppm"), sigma_ppm=rc.get("sigma_ppm")),
                                   cleaned_top3=rc.get("top3"), cleaned_file=cleaned)
        print(f"S{sec}: control OK; cleaned residual at true ephemeris {rc.get('depth_ppm'):.0f} +- {rc.get('sigma_ppm'):.0f} ppm ({rc['clause_a']}); {time.time() - t_start:.0f} s", flush=True)
    from multiprocessing import Pool
    jobs = [(s, 185.0, i, a.tmp) for s in secs for i in range(a.n185)] + [(s, d, i, a.tmp) for s in secs for d in (130.0, 240.0) for i in range(a.n_side)]
    with Pool(a.workers) as pool:
        for k, row in enumerate(pool.imap_unordered(h1_trial, jobs, chunksize=1)):
            res["h1"].append(row)
            if (k + 1) % 50 == 0: print(f"H1 {k + 1}/{len(jobs)} ({time.time() - t_start:.0f} s)", flush=True)
        njobs = [(s, i, res["sectors"][s]["cleaned_file"], res["sectors"][s]["cleaned_top3"]) for s in secs for i in range(a.n_null)]
        for k, row in enumerate(pool.imap_unordered(h0_trial, njobs, chunksize=20)):
            res["h0"].append(row)
            if (k + 1) % 2000 == 0: print(f"H0 {k + 1}/{len(njobs)} ({time.time() - t_start:.0f} s)", flush=True)
    for s in res["sectors"].values(): s.pop("cleaned_file")
    res["runtime_s"] = time.time() - t_start
    json.dump(res, open(a.out, "w"), indent=1, default=float); print("written", a.out)

if __name__ == "__main__": main()
