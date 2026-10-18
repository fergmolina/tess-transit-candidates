"""One-line-per-star summary of results/vet<SUFFIX>/*/report.json for fast triage of vetting outcomes.
Usage: python -I vet_summary_table.py [--dir results/vet_allsky]"""
import json, glob, os, argparse, numpy as np, pandas as pd
ap = argparse.ArgumentParser(); ap.add_argument("--dir", default="/Users/fernando/Desktop/NASA/results/vet_allsky"); a = ap.parse_args()
rows = []
for f in sorted(glob.glob(f"{a.dir}/*/report.json")):
    r = json.load(open(f)); tic = r["tic"]; b = r.get("bls_refine", {}); sm = r.get("shape_mcmc", {}); dc = r.get("density_check", {}); ps = r.get("per_sector", {})
    d = np.array([v["depth_ppm"] for v in ps.values() if v.get("n_in", 0) > 0 and np.isfinite(v["depth_ppm"])]); e = np.array([v["err_ppm"] for v in ps.values() if v.get("n_in", 0) > 0 and np.isfinite(v["depth_ppm"])])
    chi2 = float(np.sum((d - np.average(d, weights=1 / e**2))**2 / e**2)) if len(d) > 1 else np.nan
    bt = r.get("blind_tests", {}); nb = sum(1 for v in bt.values() if v.get("ok")); nb_rank0 = sum(1 for v in bt.values() if v.get("ok") and v.get("training_search", {}).get("rank_of_candidate") == 0)
    med = sm.get("median", [np.nan] * 4); el = r.get("ephemeris_linear", {}); pl = r.get("planet", {}); gn = r.get("gaia_neighbours", [])
    cap = sum(1 for g in gn[1:] if (g.get("required_depth_if_source") or 9) <= 1)
    rows.append(dict(tic=tic, P=round(b.get("period", np.nan), 5), depth=round(b.get("depth_ppm", np.nan)), snr=round(b.get("snr", np.nan), 1), ntr=b.get("n_transits"), sap_over_det=round(r.get("sap_depth", {}).get("depth_ppm", np.nan) / b.get("depth_ppm", np.nan), 2),
                     rprs=round(med[1], 3), b_imp=round(med[3], 2), rho_fit_over_tic=round(dc.get("rho_star_fit_solar", np.nan) / dc.get("rho_star_tic_solar", np.nan), 2),
                     sector_depth_chi2=round(chi2, 1), n_sec=len(d), odd_even_sig=round(r.get("odd_even", {}).get("sigma", np.nan), 1), sec_sig=round(r.get("secondary", {}).get("snr_at_0p5", np.nan), 1), best_other_snr=round(r.get("secondary", {}).get("best_snr", np.nan), 1),
                     blind_rank0=f"{nb_rank0}/{nb}", oc_rms_min=round(el.get("rms_oc_min", np.nan), 1), inv_sde=round(r.get("inverted_null", {}).get("inverted_top", {}).get("sde", np.nan), 1), Rp_Re=round(pl.get("Rp_Rearth", np.nan), 1), gaia_capable=cap))
df = pd.DataFrame(rows); pd.set_option("display.width", 250); print(df.to_string(index=False)); df.to_csv(f"{a.dir}/vet_summary_table.csv", index=False)
