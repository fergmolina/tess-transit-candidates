"""Automatic triage of round-3 vet.py reports (results/vet_allsky/<TIC>/report.json) into PASS / WEAK / FAIL with reasons, to focus the
manual review. Not a verdict. Thresholds as in rounds 1-2 practice: SNR >= 9; dip seen (SNR >= 3) in >= 2 years and in >= 60 % of years with
in-transit data; fit/TIC density ratio 0.25-4; |odd-even| < 3 sigma; |secondary at phase 0.5| < 3 sigma; inverted-null SDE margin >= 2;
duration > 0.6 h (grid floor 0.5 h); Rp < 20 R_E. Output results/allsky_round3_triage.csv."""
import json, os, math, pandas as pd, numpy as np
L = pd.read_csv("/Users/fernando/Desktop/NASA/results/allsky_round3_vetlist.csv"); px = pd.read_csv("/Users/fernando/Desktop/NASA/results/allsky_round3_pixel.csv").set_index("tic")
rows = []
for tic in L.tic:
    f = f"/Users/fernando/Desktop/NASA/results/vet_allsky/{tic}/report.json"
    if not os.path.exists(f): rows.append(dict(tic=tic, triage="NO_REPORT")); continue
    r = json.load(open(f)); b = r["bls_refine"]; fails, weak = [], []
    yrs = [v for v in r["per_year"].values() if v.get("n_in", 0) > 0 and v.get("snr") == v.get("snr") and v.get("snr") is not None]
    ndet = sum(1 for v in yrs if v["snr"] >= 3); nyr = len(yrs)
    dc = r.get("density_check", {}); ratio = (dc.get("rho_star_fit_solar") or np.nan) / (dc.get("rho_star_tic_solar") or np.nan)
    oe = r.get("odd_even", {}).get("sigma"); sec = r.get("secondary", {}).get("snr_at_0p5"); marg = r.get("inverted_null", {}).get("sde_margin")
    rp = r.get("planet", {}).get("Rp_Rearth"); dur = b.get("duration_h")
    if b["snr"] < 9: weak.append(f"SNR {b['snr']:.1f}")
    if ndet < 2 or (nyr and ndet / nyr < 0.6): fails.append(f"seen {ndet}/{nyr} yrs")
    if not (0.25 <= ratio <= 4): fails.append(f"density x{ratio:.2g}")
    if oe is not None and oe == oe and abs(oe) >= 3: fails.append(f"odd/even {oe:.1f}s")
    if sec is not None and sec == sec and abs(sec) >= 3: fails.append(f"secondary {sec:.1f}s")
    if marg is not None and marg < 2: fails.append(f"inv-null margin {marg:.1f}")
    if dur is not None and dur <= 0.6: fails.append(f"dur {dur:.2f} h")
    if rp is not None and rp == rp and rp >= 20: fails.append(f"Rp {rp:.0f}")
    rows.append(dict(tic=tic, P=b["period"], depth=b["depth_ppm"], sap_depth=r.get("sap_depth", {}).get("depth_ppm"), snr=b["snr"], ntr=b["n_transits"], years=f"{ndet}/{nyr}",
                     rho_ratio=ratio, dur_h=dur, Rp=rp, next_sector=px.loc[tic, "next_sector"], triage="FAIL" if fails else ("WEAK" if weak else "PASS"), reasons="; ".join(fails + weak)))
o = pd.DataFrame(rows); o.to_csv("/Users/fernando/Desktop/NASA/results/allsky_round3_triage.csv", index=False)
print(o.triage.value_counts().to_dict()); pd.set_option("display.width", 220)
print(o[o.triage != "FAIL"].round(2).to_string(index=False))
print(o[o.triage == "FAIL"].reasons.str.split("; ").explode().str.replace(r"[-0-9.x]+.*$", "", regex=True).value_counts().head(8))
