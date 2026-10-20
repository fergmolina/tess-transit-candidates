"""Holdout calibration report (conformance-v2.1): per target-sector and per target, outcome rates with Clopper-Pearson 95 % intervals
on the scored runs and on the effective number of independent realisations, N_eff = max(1, min(N, floor(usable days / (median
events per realisation x 2 x (0.3 d + 3 x T14))))), usable days = QUALITY 0 data after the edge rule. Family-wise false RECOVERED
across the seven tests = 1 - prod(1 - p_i) (point estimate and with each p_i at its N_eff upper bound).
Usage: python -I conformance_calib_report.py RUNS.csv OUT.md"""
import sys, glob, json, numpy as np, pandas as pd
from astropy.io import fits
from scipy.stats import beta
R = "/Users/fernando/Desktop/NASA"; sys.path.insert(0, f"{R}/scripts"); import prereg_conformance as pc
def cp(k, n): return (0.0 if k == 0 else float(beta.ppf(.025, k, n - k + 1)), 1.0 if k == n else float(beta.ppf(.975, k + 1, n - k))) if n else (np.nan, np.nan)
d = pd.read_csv(sys.argv[1], keep_default_na=False, na_values=[""]); d["o"] = d.outcome.astype(str).str.split(" ").str[0]
lines = ["# Holdout calibration, conformance-v2.1 (holdout sectors only; DECISIONS 76, 82)", "",
         "Outcome of record includes the timing-split check. Cases: null (real transits removed), ontime (reference box), displaced (+(gate+60) min).",
         "Real-transit holes exceed 0.1 d for 183374279 and 253931796 and trigger the 0.5-d pre-gap trim there (not present in S106).", ""]
rows = []; neff = {}
for (tic, sec), g in d.groupby(["tic", "sector"]):
    lock = json.load(open(f"{R}/configs/conformance/{tic}_S106.json")); T = lock["ref_dur_h"] / 24
    p = glob.glob(f"{R}/data/qlp*/hlsp_qlp_tess_ffi_s{sec:04d}-{tic:016d}_tess_v01_llc.fits")[0]; t = np.sort(pc.load_lc(p, "SAP_FLUX")[0]); tk = pc.edge_trim(t, np.ones(len(t)))[0]
    usable = float(np.sum(np.minimum(np.diff(tk), 0.1))); nev = float(np.median(g.n_pred)); N = int(g.k.nunique())
    ne = int(max(1, min(N, np.floor(usable / (nev * 2 * (0.3 + 3 * T)))))); neff[(tic, sec)] = ne
    for case, h in g.groupby("case"):
        s = h[h.o != "INSUFFICIENT"]; n = len(s); r = dict(tic=tic, sector=sec, case=case, runs=len(h), insufficient=int((h.o == "INSUFFICIENT").sum()), scored=n, N_eff=ne)
        for oc in ("RECOVERED", "INCONSISTENT", "EXCLUDED", "AMBIGUOUS"):
            k = int((s.o == oc).sum()); lo, hi = cp(k, n); f = k / n if n else np.nan; lo2, hi2 = cp(int(round(f * ne)), ne) if n else (np.nan, np.nan)
            r[oc] = f"{k}/{n} [{lo:.2f}-{hi:.2f}] Neff[{lo2:.2f}-{hi2:.2f}]" if n else "-"
        rows.append(r)
t = pd.DataFrame(rows); pd.set_option("display.width", 400); pd.set_option("display.max_colwidth", 60)
lines += ["## Per target-sector", "```", t.to_string(index=False), "```", ""]
# per target pooled over its holdout sectors, null false RECOVERED
fw = []; lines += ["## Per target (holdout sectors pooled)", "```"]
for tic, g in d.groupby("tic"):
    ne = sum(neff[(tic, s)] for s in g.sector.unique()); parts = []
    for case in ("null", "ontime", "displaced"):
        s = g[(g.case == case) & (g.o != "INSUFFICIENT")]; n = len(s)
        for oc in (("RECOVERED", "EXCLUDED") if case == "null" else ("RECOVERED", "INCONSISTENT")):
            k = int((s.o == oc).sum()); lo, hi = cp(k, n); parts.append(f"{case}->{oc} {k}/{n} [{lo:.2f}-{hi:.2f}]")
            if case == "null" and oc == "RECOVERED": fw.append((k / n if n else 0.0, cp(int(round((k / n if n else 0) * ne)), ne)[1]))
    lines.append(f"{tic} (N_eff total {ne}; INSUFFICIENT {int((g.o == 'INSUFFICIENT').sum())}/{len(g)}): " + "; ".join(parts))
lines += ["```", "", f"Family-wise false RECOVERED across the {len(fw)} tests: point {1 - np.prod([1 - a for a, b in fw]):.3f}; with every per-test rate at its N_eff upper bound {1 - np.prod([1 - b for a, b in fw]):.3f}."]
open(sys.argv[2], "w").write("\n".join(lines) + "\n"); print("\n".join(lines))
