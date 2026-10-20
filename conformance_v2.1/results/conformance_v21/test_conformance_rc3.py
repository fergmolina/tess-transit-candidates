"""Self-test of prereg_conformance.py on the synthetic cases used by the independent reviews (reviews_2026-10-20/), plus extra cases.
LOGIC TESTS ONLY, at about 10x the operating signal-to-noise of the S106 tests: they check that each outcome route works, not how
the evaluator performs on real data (operating-SNR rates: conformance_discriminating_test.py on design sectors and
conformance_calibrate_holdout.py on holdout sectors; DECISIONS items 76-79).
Construction (as in the reviews, span widened for the edge rule on 2026-10-20): 200-s cadence over BTJD 97-108, predicted centres 100 and 105, sigma_pred 2.1 min, reference 1000 ppm,
2 h; Gaussian white noise 100 ppm (rng seed 99106); rectangular dips. Writes only under the directory given as argv[1].
Expected outcomes are declared below BEFORE running; the test fails loudly on any mismatch."""
import sys, os, json, hashlib, subprocess, numpy as np, pandas as pd
D = sys.argv[1]; os.makedirs(D, exist_ok=True); PY = "/Users/fernando/Desktop/NASA/.venv/bin/python"; EV = "/Users/fernando/Desktop/NASA/scripts/prereg_conformance.py"
t0 = np.arange(97, 108, 200 / 86400); rng = np.random.default_rng(99106); noise = rng.normal(0, 100e-6, len(t0))
pred = pd.DataFrame(dict(epoch=[1, 2], tc_btjd=[100.0, 105.0], sigma_min=[2.1, 2.1], tess_sector=[106, 106], status=["prediction", "prediction"]))
pp = f"{D}/pred.csv"; pred.to_csv(pp, index=False); psha = hashlib.sha256(open(pp, "rb").read()).hexdigest()
cfg = dict(tic=1, sector=106, product="synthetic", flux_col="SAP_FLUX", pred_csv=pp, pred_sha256=psha, ref_depth_ppm=1000.0, ref_dur_h=2.0)
cp = f"{D}/cfg.json"; json.dump(cfg, open(cp, "w"))
def lc(boxes, gaps=(), extra=None):
    f = 1 + noise.copy(); t = t0.copy()
    for tc, off, dep, w_h in boxes: f[np.abs(t - (tc + off / 1440)) < w_h / 48] -= dep * 1e-6
    keep = np.ones(len(t), bool)
    for tc, half_h in gaps: keep &= ~(np.abs(t - tc) < half_h / 24)
    if extra is not None: f = extra(t, f)
    return t[keep], f[keep]
CASES = {  # name: (boxes [(tc, offset_min, depth_ppm, width_h)], gaps [(tc, half-width h)], expected outcome, expected min-gate outcome)
 "control":          ([(100, 0, 1000, 2), (105, 0, 1000, 2)], [], "RECOVERED", "RECOVERED"),
 "late20":           ([(100, 20, 1000, 2), (105, 20, 1000, 2)], [], "RECOVERED", "AMBIGUOUS"),
 "opposite50":       ([(100, -50, 1200, 2), (105, 50, 1200, 2)], [], "AMBIGUOUS", "AMBIGUOUS"),   # changed 2026-10-20 after calibration: no common offset -> not a coherent wrong ephemeris; must not be RECOVERED
 "too_short_0p6":    ([(100, 0, 1000, 1.2), (105, 0, 1000, 1.2)], [], "AMBIGUOUS", "AMBIGUOUS"),
 "too_long_1p8":     ([(100, 0, 1000, 3.6), (105, 0, 1000, 3.6)], [], "AMBIGUOUS", "AMBIGUOUS"),
 "strong_plus_weak": ([(100, 0, 1400, 2), (105, 0, 100, 2)], [], "AMBIGUOUS", "AMBIGUOUS"),
 "one_dip_only":     ([(100, 0, 1400, 2)], [], "AMBIGUOUS", "AMBIGUOUS"),
 "missing_centres":  ([], [(100, 0.9), (105, 0.9)], "INSUFFICIENT", "INSUFFICIENT"),
 "displaced_200":    ([(100, 200, 1000, 2), (105, 200, 1000, 2)], [], "INCONSISTENT", "INCONSISTENT"),
 "no_signal":        ([], [], "EXCLUDED", "EXCLUDED"),
 "brightening":      ([(100, 0, -1500, 2), (105, 0, -1500, 2)], [], "EXCLUDED", "EXCLUDED"),
 "half_depth_0p6":   ([(100, 0, 600, 2), (105, 0, 600, 2)], [], "RECOVERED", "RECOVERED"),
 "partial_one":      ([(100, 0, 1000, 2), (105, 0, 1000, 2)], [(105, 0.6)], "INSUFFICIENT", "INSUFFICIENT"),
 "red_noise_signal": ([(100, 0, 1000, 2), (105, 0, 1000, 2)], [], "RECOVERED", "ANY"),   # min-gate reading not asserted: red noise shifts fitted times by ~10 min > the 6.3-min narrow gate (correct behaviour)
 "red_noise_none":   ([], [], "NOT_RECOVERED", "NOT_RECOVERED"),
}
RED = lambda t, f: f + 250e-6 * np.sin(2 * np.pi * t / 0.23 + 1.0) + 150e-6 * np.sin(2 * np.pi * t / 0.41 + 2.0)   # correlated noise on ~hour scales
fails = 0; rows = []
for name, (boxes, gaps, exp, exp_min) in CASES.items():
    t, f = lc(boxes, gaps, RED if name.startswith('red_noise') else None); p = f"{D}/{name}.csv"; pd.DataFrame(dict(time=t, flux=f)).to_csv(p, index=False)
    out = f"{D}/{name}.json"; subprocess.run([PY, "-I", EV, "--config", cp, "--lc", p, "--out", out], capture_output=True, text=True)
    r = json.load(open(out))
    if exp == "NOT_RECOVERED": ok = r["outcome"] != "RECOVERED" and r["outcome_min_gate_reading"] != "RECOVERED"
    else: ok = r["outcome"] == exp and (exp_min == "ANY" or r["outcome_min_gate_reading"] == exp_min)
    if name.startswith("red_noise"): ok = ok and r["beta"] > 1.2   # the red-noise factor must engage
    fails += not ok
    bests = [(round(e["best"]["offset_min"], 1), round(e["best"]["dur_h"], 2), round(e["best"]["depth_ppm"]), round(e["best"]["snr"], 1)) if e.get("best") else None for e in r["events"]]
    rows.append(dict(case=name, expected=exp, got=r["outcome"], expected_min=exp_min, got_min=r["outcome_min_gate_reading"], ok=ok, eligible=r["n_eligible"], beta=round(r["beta"], 2), events=bests))
pd.set_option("display.width", 250); print(pd.DataFrame(rows).to_string(index=False)); print("FAILURES:", fails)
sys.exit(1 if fails else 0)
