"""conformance-v2.1 design analysis (2026-10-20). Usage: python -I conformance_edge_profile.py GAP_DAYS (0.5 = resumes after long gaps; 0.1 = also short downlink gaps).
Edge (post-resume / pre-gap) systematics on DESIGN sectors only. Box depth by the evaluator's own estimator (median baseline within
+-3D minus in-box mean, D = reference T14) at positions on a 0.02-d grid away from known transits, after the evaluator's preprocessing
(QUALITY 0, biweight 0.7 d / break 0.5 d with known transits masked). Reports depth/err vs time since data resume and time to next gap."""
import sys, json, glob, numpy as np
sys.path.insert(0, "/Users/fernando/Desktop/NASA/scripts"); import prereg_conformance as pc
from wotan import flatten
GAP = float(sys.argv[1]); R = "/Users/fernando/Desktop/NASA"
DESIGN = {183374279: [96, 105], 120444365: [96, 105], 70441745: [96], 206620592: [96], 122522485: [97], 253931796: [96], 115692561: [96]}
rows = []
for tic, secs in DESIGN.items():
    lock = json.load(open(f"{R}/configs/conformance/{tic}_S106.json")); D = lock["ref_dur_h"] / 24; dep = lock["ref_depth_ppm"]
    eph = json.load(open(f"{R}/results/vet_allsky/{tic}/final_ephemeris_v2.json")); T0, P = eph["T0_btjd"], eph["P_d"]
    for s in secs:
        p = glob.glob(f"{R}/data/qlp*/hlsp_qlp_tess_ffi_s{s:04d}-{tic:016d}_tess_v01_llc.fits")[0]
        t, f, *_ = pc.load_lc(p, "SAP_FLUX"); o = np.argsort(t); t, f = t[o], f[o]
        ph = ((t - T0) / P + 0.5) % 1 - 0.5; intr = np.abs(ph * P) < 1.5 * D
        tr = flatten(t, f, method="biweight", window_length=0.7, break_tolerance=0.5, return_trend=True, mask=intr)[1]; r = f / tr; g = np.isfinite(r) & ~intr
        tt, rr = t[g], r[g]; cad = np.median(np.diff(t)); sig = 1.4826 * np.median(np.abs(rr - np.median(rr)))
        gi = np.where(np.diff(t) > GAP)[0]; starts = np.r_[t[0], t[gi + 1]]; ends = np.r_[t[gi], t[-1]]
        for c in np.arange(t[0] + D / 2, t[-1] - D / 2, 0.02):
            if np.abs(((c - T0) / P + 0.5) % 1 - 0.5) * P < 3.5 * D: continue
            x = np.abs(tt - c); inn = x < D / 2; out = (x >= D / 2) & (x < 3 * D)
            if inn.sum() < 0.8 * D / cad or out.sum() < 5: continue
            d = np.median(rr[out]) - rr[inn].mean(); e = sig * np.sqrt(1 / inn.sum() + (np.pi / 2) / out.sum())
            k = np.searchsorted(starts, c, "right") - 1
            rows.append((tic, s, c, c - starts[k], ends[k] - c, d * 1e6, e * 1e6, d * 1e6 / dep, k == 0, k == len(starts) - 1))
import pandas as pd
df = pd.DataFrame(rows, columns="tic sec c since_resume to_gap depth_ppm err_ppm depth_over_ref first_seg last_seg".split()); df.to_csv(f"{R}/results/conformance_v21/edge_profile_gap{GAP}.csv", index=False)
df["z"] = df.depth_ppm / df.err_ppm
bins = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.75, 1.0, 1.25, 1.5, 2, 3, 30]
for side, col in (("AFTER RESUME", "since_resume"), ("BEFORE GAP/END", "to_gap")):
    print("==", side); df["b"] = pd.cut(df[col], bins)
    print(df.groupby(["tic", "b"], observed=True).agg(n=("z", "size"), z_med=("z", "median"), z_rms=("z", lambda v: float(np.sqrt(np.mean(v ** 2)))), dep_med=("depth_ppm", "median"), absdep_p90=("depth_ppm", lambda v: float(np.percentile(np.abs(v), 90))), fr_med=("depth_over_ref", "median")).round(2).to_string())
