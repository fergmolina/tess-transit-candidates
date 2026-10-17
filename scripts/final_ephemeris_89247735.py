"""Final ephemeris and falsifiable predictions for TIC 89247735 from the three individually timed transits (S66, S93, S104).
Weighted linear fit; errors inflated by sqrt(chi2/dof); predictions for 2026-10 to 2027-12 with TESS coverage (tess-point) and
sector windows from TESS_orbit_times.csv where available."""
import sys, json, hashlib, datetime, numpy as np, pandas as pd; sys.path.insert(0, "/Users/fernando/Desktop/NASA/scripts")
from astropy.time import Time
rep = json.load(open("/Users/fernando/Desktop/NASA/results/vet_qlp/89247735/report.json"))
tt = rep["transit_times"]
# Re-time each transit on a fine grid (0.24-min step; vet.py's 121-step grid floored the errors at 1.2 min) with the MCMC shape.
import os; os.environ["TSEARCH_SOURCE"] = "qlp"
from vet import load_all, stitch, transit_model
P_in = rep["bls_refine"]["period"]; T0_in = rep["bls_refine"]["T0"]; dur_d = 4.0 / 24
rprs, ars, b = rep["shape_mcmc"]["median"][1:4]
secs = load_all(89247735, P_in, T0_in, dur_d); T, F, Er = stitch(secs)
retimed = []
for x in tt:
    tc0 = x["tc"]; w = np.abs(T - tc0) < 2.5 * dur_d; t_, f_, e_ = T[w], F[w], Er[w]
    grid = tc0 + np.linspace(-0.1, 0.1, 1201)
    chi = np.array([np.sum(((f_ - transit_model([g, rprs, ars, b], t_, P_in)) / e_) ** 2) for g in grid])
    i = int(np.argmin(chi)); dof = len(t_) - 1; scale = max(1.0, chi[i] / dof)   # rescale errors so reduced chi2 = 1
    okk = chi < chi[i] + scale; err = (grid[okk].max() - grid[okk].min()) / 2
    retimed.append(dict(epoch=x["epoch"], tc=float(grid[i]), tc_err=float(err), sector=x["sector"], n_pts=int(len(t_)), redchi2=float(chi[i] / dof)))
    print(f"epoch {x['epoch']} S{x['sector']}: tc={grid[i]:.5f} +- {err*1440:.2f} min (n={len(t_)}, red.chi2 {chi[i]/dof:.2f}; vet.py grid value {x['tc']:.5f} +- {x['tc_err']*1440:.1f} min)")
tt = retimed
e = np.array([x["epoch"] for x in tt], float); tc = np.array([x["tc"] for x in tt]); er = np.array([x["tc_err"] for x in tt])
# re-reference epochs to the last transit for minimal covariance
e0 = e[-1]; E = e - e0
A = np.vstack([np.ones_like(E), E]).T; W = np.diag(1 / er**2)
cov = np.linalg.inv(A.T @ W @ A); beta = cov @ A.T @ W @ tc
res = tc - A @ beta; chi2 = float(np.sum(res**2 / er**2)); dof = len(tc) - 2; infl = max(1.0, np.sqrt(chi2 / dof))
cov *= infl**2; T0, P = beta; T0_err, P_err = np.sqrt(np.diag(cov)); corr = cov[0, 1] / (T0_err * P_err)
print(f"transits used: {[(int(x['epoch']), round(x['tc'],5), x['sector']) for x in tt]}")
print(f"linear ephemeris (epoch ref {int(e0)}): T0 = BTJD {T0:.5f} +- {T0_err:.5f} ({T0_err*1440:.1f} min), P = {P:.6f} +- {P_err:.6f} d; chi2/dof = {chi2:.2f}/{dof}; inflation {infl:.2f}; corr {corr:.2f}")
print(f"residuals (min): {np.round(res*1440, 1).tolist()}")
# predictions
from tess_stars2px import tess_stars2px_function_entry
ra, dec = rep["meta"]["ra"], rep["meta"]["dec"]
r = tess_stars2px_function_entry(89247735, ra, dec); secs_tp = sorted(set(int(s) for s in r[3]))
orb = pd.read_csv("/Users/fernando/Desktop/NASA/catalogs/TESS_orbit_times.csv", comment="#")
print("tess-point sectors (all):", secs_tp); print("orbit table columns:", list(orb.columns)[:8])
def sector_at(jd):
    for _, row in orb.iterrows():
        try:
            s = int(row["Sector"]); t1 = Time(str(row["Start of Orbit"]).strip()).jd; t2 = Time(str(row["End of Orbit"]).strip()).jd
        except Exception: continue
        if t1 <= jd <= t2: return s
    return None
rows = []
for k in range(1, 26):
    n = e0 + k; t = T0 + k * P; sig = np.sqrt(cov[0, 0] + (k**2) * cov[1, 1] + 2 * k * cov[0, 1])
    jd = t + 2457000; s = sector_at(jd)
    rows.append(dict(epoch=int(n), tc_btjd=round(t, 5), tc_bjd_tdb=round(jd, 5), utc=Time(jd, format="jd", scale="tdb").utc.iso[:16], sigma_min=round(sig * 1440, 1),
                     ingress_utc=Time(jd - 2.0 / 24, format="jd", scale="tdb").utc.iso[:16], egress_utc=Time(jd + 2.0 / 24, format="jd", scale="tdb").utc.iso[:16],
                     tess_sector_observing=(s if s in secs_tp else None), status=("retrodiction: before freeze, untested" if jd < Time(datetime.datetime.now(datetime.UTC)).jd else "prediction")))
df = pd.DataFrame(rows); out = "/Users/fernando/Desktop/NASA/results/vet_qlp/89247735/predicted_transits_2026_2027.csv"; df.to_csv(out, index=False)
print(df.to_string(index=False))
sha = hashlib.sha256(open(out, "rb").read()).hexdigest(); print("SHA-256", sha, "frozen", datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d %H:%M:%S UTC"))
json.dump(dict(T0_btjd=T0, T0_err_d=T0_err, P_d=P, P_err_d=P_err, epoch_ref=int(e0), chi2=chi2, dof=dof, inflation=infl, corr=corr, residual_min=(res*1440).tolist(), sha256_csv=sha, tesspoint_sectors=secs_tp, transit_times=tt), open("/Users/fernando/Desktop/NASA/results/vet_qlp/89247735/final_ephemeris.json", "w"), indent=1)
