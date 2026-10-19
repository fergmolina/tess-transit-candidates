"""Prediction shifts of frozen ephemerides under the method-2 QLP clock corrections (results/qlp_clock_v2/<TIC>.json). Same refit as
qlp_clock_check.py (weighted linear; P held at the BLS value when fewer than 3 sector times), which reproduces each frozen period exactly.
Writes results/qlp_clock_v2/shifts.csv."""
import glob, json, os, numpy as np, pandas as pd
ROOT = "/Users/fernando/Desktop/NASA"; out = []
def fit(rows, P0):
    e = np.array([r["mean_epoch"] for r in rows]); t = np.array([r["tc"] for r in rows]); w = 1 / np.array([r["tc_err"] for r in rows]) ** 2
    if len(rows) >= 3:
        A = np.vstack([np.ones_like(e), e]).T; cov = np.linalg.inv(A.T @ (A * w[:, None])); b = cov @ A.T @ (w * t); return b[0], b[1]
    return np.sum(w * (t - e * P0)) / w.sum(), P0
for f in sorted(glob.glob(f"{ROOT}/results/qlp_clock_v2/*.json")):
    c = json.load(open(f)); tic = c["tic"]
    if tic == 89247735: continue
    d = json.load(open(f"{ROOT}/{c['ephemeris_file']}")); rows = d["sector_times"]; new = []
    for r in rows:
        r2 = dict(r); v = c["sectors"].get(str(r["sector"]))
        if v: r2["tc"] = r["tc"] + v["correction_min"] / 1440
        new.append(r2)
    P0 = d.get("bls_P", d["P_d"]); T0a, Pa = fit(rows, P0); T0b, Pb = fit(new, P0); assert abs(Pa - d["P_d"]) < 1e-9, tic
    p = pd.read_csv(sorted(glob.glob(f"{os.path.dirname(f'{ROOT}/{c[chr(101)+'phemeris_file']}')}/predicted_transits_*v{d.get('version', 2)}.csv"))[0])
    for _, r in p.iterrows():
        tb = r["tc_btjd"]; n = round((tb - T0a) / Pa); out.append(dict(tic=tic, epoch=int(r["epoch"]), sector=r.get("tess_sector"), shift_min=((T0b + n * Pb) - (T0a + n * Pa)) * 1440, frozen_sigma_min=r["sigma_min"]))
o = pd.DataFrame(out); o.to_csv(f"{ROOT}/results/qlp_clock_v2/shifts.csv", index=False)
print(o.groupby("tic").agg(shift_min=("shift_min", "min"), shift_max=("shift_min", "max"), sigma=("frozen_sigma_min", "min"), test=("sector", "first")).round(2).to_string())
