"""v2 ephemeris for TIC 89247735 using FOUR transits. The external review found a fourth event at epoch 118 (S93, BTJD ~3830.35)
whose cadences carry QLP quality bit 2^30 (scattered-light ramp) and were dropped by the QUALITY==0 mask. Here every event is
re-timed from raw QLP SAP_FLUX (all quality flags kept, NaNs dropped) with the MCMC transit shape plus a local linear baseline
fitted simultaneously, on a 0.24-min grid; errors from delta-chi2 = 1 after rescaling to reduced chi2 = 1. v1 files are untouched."""
import sys, os, json, glob, hashlib, datetime, numpy as np, pandas as pd; sys.path.insert(0, "/Users/fernando/Desktop/NASA/scripts"); os.environ["TSEARCH_SOURCE"] = "qlp"
from astropy.io import fits; from astropy.time import Time
from vet import transit_model
OUT = "/Users/fernando/Desktop/NASA/results/vet_qlp/89247735"
rep = json.load(open(f"{OUT}/report.json")); P0 = 18.323126; T0_v1 = 4196.80732; dur_d = 4.0 / 24
rprs, ars, b = rep["shape_mcmc"]["median"][1:4]
events = [(66, 79), (93, 118), (93, 119), (104, 138)]
timed = []
for sec, ep in events:
    f = [x for x in glob.glob("/Users/fernando/Desktop/NASA/data/qlp/*89247735*") if f"s{sec:04d}" in x][0]; h = fits.open(f)[1].data
    t, fl, q = h["TIME"], h["SAP_FLUX"], h["QUALITY"]; ok = np.isfinite(t) & np.isfinite(fl)
    tc0 = T0_v1 + (ep - 138) * P0; w = ok & (np.abs(t - tc0) < 2.5 * dur_d); t_, f_ = t[w], fl[w] / np.nanmedian(fl[w])
    oot = np.abs(t_ - tc0) > 0.75 * dur_d; sig = 1.4826 * np.median(np.abs(f_[oot] - np.median(f_[oot])))
    grid = tc0 + np.linspace(-0.08, 0.08, 961); chi = np.empty(len(grid))
    for i, g in enumerate(grid):
        m = transit_model([g, rprs, ars, b], t_, P0)           # model with unit baseline
        A = np.vstack([m, m * (t_ - tc0)]).T                     # baseline (c0 + c1*(t-tc0)) multiplying the model
        c, *_ = np.linalg.lstsq(A, f_, rcond=None); chi[i] = np.sum(((f_ - A @ c) / sig) ** 2)
    i = int(np.argmin(chi)); dof = len(t_) - 3; scale = max(1.0, chi[i] / dof); okk = chi < chi[i] + scale
    err = max((grid[okk].max() - grid[okk].min()) / 2, (grid[1] - grid[0]) / 2)
    m = transit_model([grid[i], rprs, ars, b], t_, P0); A = np.vstack([m, m * (t_ - tc0)]).T; c, *_ = np.linalg.lstsq(A, f_, rcond=None)
    base = A @ c / m; intr = np.abs(t_ - grid[i]) < dur_d / 2 * 0.8; depth = 1 - np.mean(f_[intr] / base[intr])
    flagged = int(np.sum(q[w] != 0)); print(f"S{sec} epoch {ep}: tc={grid[i]:.5f} +- {err*1440:.2f} min  depth {depth*1e6:.0f} ppm  n={len(t_)} (flagged cadences {flagged})  red.chi2 {chi[i]/dof:.2f}  O-C(v1) {(grid[i]-tc0)*1440:+.1f} min")
    timed.append(dict(sector=sec, epoch=ep, tc=float(grid[i]), tc_err=float(err), depth_ppm=float(depth * 1e6), n_pts=int(len(t_)), n_flagged=flagged, oc_v1_min=float((grid[i] - tc0) * 1440)))
e = np.array([x["epoch"] for x in timed], float); tc = np.array([x["tc"] for x in timed]); er = np.array([x["tc_err"] for x in timed])
e0 = 138; E = e - e0; A = np.vstack([np.ones_like(E), E]).T; W = np.diag(1 / er ** 2)
cov = np.linalg.inv(A.T @ W @ A); beta = cov @ A.T @ W @ tc; res = tc - A @ beta; chi2 = float(np.sum(res ** 2 / er ** 2)); dof = len(tc) - 2
infl = max(1.0, np.sqrt(chi2 / dof)); cov *= infl ** 2; T0, P = beta; T0_err, P_err = np.sqrt(np.diag(cov)); corr = cov[0, 1] / (T0_err * P_err)
print(f"\nv2 ephemeris (4 transits, epoch ref 138): T0 = BTJD {T0:.5f} +- {T0_err:.5f} ({T0_err*1440:.1f} min), P = {P:.6f} +- {P_err:.6f} d; chi2/dof {chi2:.2f}/{dof}; inflation {infl:.2f}; corr {corr:.2f}")
print("residuals (min):", np.round(res * 1440, 1).tolist()); print(f"direct consecutive-transit period tc(119)-tc(118) = {timed[2]['tc']-timed[1]['tc']:.4f} +- {np.hypot(timed[1]['tc_err'], timed[2]['tc_err']):.4f} d")
now = datetime.datetime.now(datetime.UTC); rows = []
for k in range(1, 26):
    t = T0 + k * P; sig = np.sqrt(cov[0, 0] + k ** 2 * cov[1, 1] + 2 * k * cov[0, 1]); jd = t + 2457000
    rows.append(dict(epoch=e0 + k, tc_btjd=round(t, 5), tc_bjd_tdb=round(jd, 5), utc=Time(jd, format="jd", scale="tdb").utc.iso[:16], sigma_min=round(sig * 1440, 1),
                     ingress_utc=Time(jd - 2 / 24, format="jd", scale="tdb").utc.iso[:16], egress_utc=Time(jd + 2 / 24, format="jd", scale="tdb").utc.iso[:16],
                     status=("retrodiction: before freeze, untested" if jd < Time(now).jd else "prediction")))
df = pd.DataFrame(rows); csv = f"{OUT}/predicted_transits_2026_2027_v2.csv"; df.to_csv(csv, index=False)
sha = hashlib.sha256(open(csv, "rb").read()).hexdigest(); stamp = now.strftime("%Y-%m-%d %H:%M:%S UTC")
print(df[df.status == "prediction"][["epoch", "tc_bjd_tdb", "utc", "sigma_min"]].head(8).to_string(index=False)); print("SHA-256", sha, "frozen", stamp)
json.dump(dict(T0_btjd=T0, T0_err_d=T0_err, P_d=P, P_err_d=P_err, epoch_ref=e0, chi2=chi2, dof=dof, inflation=infl, corr=corr, residual_min=(res * 1440).tolist(), transit_times=timed, sha256_csv=sha, frozen=stamp), open(f"{OUT}/final_ephemeris_v2.json", "w"), indent=1)
open(f"{OUT}/PREREGISTRATION_v2.md", "w").write(f"""# Pre-registered transit predictions v2 — TIC 89247735 (SCR J1820-4533), 18.32-d signal
Frozen: {stamp}. Supersedes v1 (PREREGISTRATION.md, 2026-10-17 21:28:13 UTC, SHA af83f110...), which is kept unchanged as the 3-transit record.
Change: a fourth transit (S93, epoch 118, BTJD {timed[1]['tc']:.5f}) found by the external review in cadences flagged with QLP quality bit 2^30
(scattered-light ramp) and excluded by the QUALITY==0 mask; it fell {timed[1]['oc_v1_min']:+.1f} min from the v1 prediction. All four events re-timed from raw
SAP_FLUX with a local linear baseline.
SHA-256 of predicted_transits_2026_2027_v2.csv: {sha}
Ephemeris: T0 = BTJD {T0:.5f} +- {T0_err:.5f} (epoch 138 = S104 transit), P = {P:.6f} +- {P_err:.6f} d (corr {corr:.2f}; errors inflated x{infl:.2f} from chi2/dof {chi2:.2f}/{dof}).
Direct period from the two consecutive S93 transits: {timed[2]['tc']-timed[1]['tc']:.4f} +- {np.hypot(timed[1]['tc_err'], timed[2]['tc_err']):.4f} d.
Duration 4.0 h, depth 1.0 % (10,200 +- 150 ppm in QLP flux). Conservative 1-sigma window: +-15 min.
Observability (external review, altitude > 30 deg, Sun < -12 deg): epochs 146-151 (2026-10-29 to 2027-01-29) are not observable from the ground (target near the Sun);
first full transits from Chile: epoch 159 (2027-06-25) and 162 (2027-08-19). Radial velocities can be taken at any time.
Generated by scripts/final_ephemeris_89247735_v2.py; parameters in final_ephemeris_v2.json.
""")
