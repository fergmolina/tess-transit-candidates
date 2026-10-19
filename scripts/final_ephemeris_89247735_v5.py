"""v5 ephemeris for TIC 89247735 (round-4 external review, 2026-10-19). Supersedes v4, whose +8.02-min S104 correction wrongly
assumed TESScut TIMECORR was target-specific. Here the correction is LTT_target(event, JPL Horizons TESS vectors) + QLP convention c0
- (QLP - spacecraft time) = +7.533 min (scripts/qlp_clock_v2.py). S104 error terms: photometric 1.44, clock 0.05, extraction systematic
4.0 min (half the TESScut aperture range, those times re-referenced to the target being a sub-minute change that this systematic absorbs).
Contacts use T14 from refit_v4_fixed_b1.json. Otherwise identical to v4 (CTIO full-visibility flags; v1 remains the test of record)."""
import json, hashlib, datetime, numpy as np, pandas as pd, astropy.units as u
from astropy.time import Time; from astropy.coordinates import SkyCoord, EarthLocation, AltAz, get_sun
D = "/Users/fernando/Desktop/NASA/results/vet_qlp/89247735"; v2 = json.load(open(f"{D}/final_ephemeris_v2.json"))
clk = json.load(open("/Users/fernando/Desktop/NASA/results/qlp_clock_v2/89247735.json"))["sectors"]["104"]
T14_h = json.load(open(f"{D}/refit_v4_fixed_b1.json"))["T14_h"]; rep = json.load(open(f"{D}/report.json")); ra, dec = rep["meta"]["ra"], rep["meta"]["dec"]
s104 = [x for x in v2["transit_times"] if x["sector"] == 104][0]
tc104 = s104["tc"] + clk["correction_min"] / 1440
err_terms = dict(statistical_min=s104["tc_err"] * 1440, clock_min=0.05, extraction_systematic_min=(4196.8132 - 4196.8077) / 2 * 1440)
err104 = np.sqrt(sum(v ** 2 for v in err_terms.values())) / 1440
times = [(x["epoch"], x["tc"], x["tc_err"], x["sector"]) for x in v2["transit_times"] if x["sector"] != 104] + [(138, tc104, err104, 104)]
e = np.array([x[0] for x in times], float); tc = np.array([x[1] for x in times]); er = np.array([x[2] for x in times]); e0 = 138
E = e - e0; A = np.vstack([np.ones_like(E), E]).T; W = np.diag(1 / er ** 2); cov = np.linalg.inv(A.T @ W @ A); beta = cov @ A.T @ W @ tc
res = tc - A @ beta; chi2 = float(np.sum(res ** 2 / er ** 2)); dof = len(tc) - 2; infl = max(1, np.sqrt(chi2 / dof)); cov *= infl ** 2; T0, P = beta; T0e, Pe = np.sqrt(np.diag(cov))
print(f"S104 corrected tc {tc104:.5f} +- {err104*1440:.2f} min  {err_terms}")
print(f"v5: T0 = BTJD {T0:.5f} +- {T0e*1440:.1f} min (epoch 138), P = {P:.6f} +- {Pe:.6f} d, chi2/dof {chi2:.2f}/{dof}, residuals (min) {np.round(res*1440,2).tolist()}")
v1 = json.load(open(f"{D}/final_ephemeris.json")); oc_v1 = (tc104 - (v1["T0_btjd"] + (138 - v1["epoch_ref"]) * v1["P_d"])) * 1440
print(f"S104 corrected time minus v1 prediction: {oc_v1:+.2f} min (v1 sigma at epoch 138 not recomputed here)")
sc = SkyCoord(ra, dec, unit="deg"); geo0 = EarthLocation.from_geocentric(0, 0, 0, unit=u.m); ctio = EarthLocation.of_site("ctio") if False else EarthLocation(lat=-30.1690 * u.deg, lon=-70.8063 * u.deg, height=2207 * u.m)
def geo_utc(jd):
    t = Time(jd, format="jd", scale="tdb"); return (t - t.light_travel_time(sc, kind="barycentric", location=geo0)).utc
rows = []
for k in range(1, 26):
    t = T0 + k * P; sig = np.sqrt(cov[0, 0] + k * k * cov[1, 1] + 2 * k * cov[0, 1]); jd = t + 2457000
    mid = geo_utc(jd); ing = mid - T14_h / 2 * u.h; egr = mid + T14_h / 2 * u.h
    alts = []
    for tt in (ing, egr):
        fr = AltAz(obstime=tt, location=ctio); alts += [sc.transform_to(fr).alt.deg, get_sun(tt).transform_to(fr).alt.deg]
    full = alts[0] > 30 and alts[2] > 30 and alts[1] < -12 and alts[3] < -12
    rows.append(dict(epoch=e0 + k, tc_btjd=round(t, 5), tc_bjd_tdb=round(jd, 5), utc_geocentric=mid.iso[:16], sigma_min=round(sig * 1440, 1),
                     ingress_utc_geocentric=ing.iso[:16], egress_utc_geocentric=egr.iso[:16], ctio_target_alt_ingress=round(alts[0], 1), ctio_target_alt_egress=round(alts[2], 1),
                     ctio_sun_alt_ingress=round(alts[1], 1), ctio_sun_alt_egress=round(alts[3], 1), ctio_full=full))
df = pd.DataFrame(rows); out = f"{D}/predicted_transits_2026_2027_v5.csv"; df.to_csv(out, index=False)
sha = hashlib.sha256(open(out, "rb").read()).hexdigest(); now = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d %H:%M:%S UTC")
print(df[df.ctio_full | df.epoch.isin([159, 162])].to_string(index=False)); print("SHA-256", sha, "frozen", now)
json.dump(dict(T0_btjd=T0, T0_err_d=T0e, P_d=P, P_err_d=Pe, epoch_ref=e0, chi2=chi2, dof=dof, inflation=infl, corr=float(cov[0, 1] / (T0e * Pe)), residual_min=(res * 1440).tolist(),
               s104_error_terms_min=err_terms, s104_clock_correction_min=clk["correction_min"], s104_minus_v1_min=oc_v1, T14_h=T14_h,
               transit_times=[dict(epoch=int(a), tc=float(b), tc_err=float(c), sector=int(s)) for a, b, c, s in times], sha256_csv=sha, frozen=now,
               note="v1 remains the test of record; v5 supersedes v4: S104 clock correction recomputed from JPL TESS vectors and the target light-travel time (qlp_clock_v2.py), contacts from the v4-clock shape fit T14"), open(f"{D}/final_ephemeris_v5.json", "w"), indent=1)
