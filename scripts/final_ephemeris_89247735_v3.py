"""v3 ephemeris for TIC 89247735: as v2 (four transits re-timed from raw SAP flux with a local linear baseline) but with the Sector 104
transit time replaced by the midpoint of the QLP (TGLC-method) and TESScut aperture determinations, BTJD 4196.8085, with a 6-min systematic
error (the two extractions differ by 5-13 min for this ramp-affected event; S66/S93 agree across methods to <= 1.6 min).
Reproduces the frozen predicted_transits_2026_2027_v3.csv (same inputs -> same SHA-256 except the freeze timestamp in the JSON)."""
import json, hashlib, datetime, numpy as np, pandas as pd
from astropy.time import Time
OUT = "/Users/fernando/Desktop/NASA/results/vet_qlp/89247735"; rep = json.load(open(f"{OUT}/final_ephemeris_v2.json")); tt = rep["transit_times"]
S104_TC, S104_ERR_D = 4196.8085, 6 / 1440
times = [(x["epoch"], x["tc"], x["tc_err"], x["sector"]) for x in tt if x["sector"] != 104] + [(138, S104_TC, S104_ERR_D, 104)]
e = np.array([x[0] for x in times], float); tc = np.array([x[1] for x in times]); er = np.array([x[2] for x in times]); e0 = 138
E = e - e0; A = np.vstack([np.ones_like(E), E]).T; W = np.diag(1 / er ** 2); cov = np.linalg.inv(A.T @ W @ A); beta = cov @ A.T @ W @ tc
res = tc - A @ beta; chi2 = float(np.sum(res ** 2 / er ** 2)); dof = len(tc) - 2; infl = max(1, np.sqrt(chi2 / dof)); cov *= infl ** 2; T0, P = beta; T0e, Pe = np.sqrt(np.diag(cov))
print(f"v3: T0 = BTJD {T0:.5f} +- {T0e*1440:.1f} min, P = {P:.6f} +- {Pe:.6f} d, chi2/dof {chi2:.2f}/{dof}")
freeze = Time("2026-10-18 03:20:13", scale="utc")   # the original freeze instant; retrodiction flags are evaluated against it so the file is reproducible
rows = []
for k in range(1, 26):
    t = T0 + k * P; sig = np.sqrt(cov[0, 0] + k * k * cov[1, 1] + 2 * k * cov[0, 1]); jd = t + 2457000
    rows.append(dict(epoch=e0 + k, tc_btjd=round(t, 5), tc_bjd_tdb=round(jd, 5), utc=Time(jd, format="jd", scale="tdb").utc.iso[:16], sigma_min=round(sig * 1440, 1), ingress_utc=Time(jd - 2 / 24, format="jd", scale="tdb").utc.iso[:16], egress_utc=Time(jd + 2 / 24, format="jd", scale="tdb").utc.iso[:16], status=("retrodiction: before freeze, untested" if jd < freeze.jd else "prediction")))
df = pd.DataFrame(rows); out = f"{OUT}/predicted_transits_2026_2027_v3_check.csv"; df.to_csv(out, index=False)
sha = hashlib.sha256(open(out, "rb").read()).hexdigest(); sha0 = hashlib.sha256(open(f"{OUT}/predicted_transits_2026_2027_v3.csv", "rb").read()).hexdigest()
print("regenerated SHA", sha[:16], "frozen SHA", sha0[:16], "MATCH" if sha == sha0 else "MISMATCH")
