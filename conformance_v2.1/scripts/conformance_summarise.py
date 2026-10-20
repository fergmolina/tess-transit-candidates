"""Summarise conformance-v2.1 test runs (discriminating test or holdout calibration CSV): outcome rates per target and case with
Clopper-Pearson 95 % intervals on the raw counts (conditional on this simulation; realisations share light curves and are not
independent; no effective-N interval is offered - external review R2). Usage: python -I conformance_summarise.py RUNS.csv OUT.txt"""
import sys, json, numpy as np, pandas as pd
from scipy.stats import beta
def cp(k, n, a=0.05):
    if n == 0: return (np.nan, np.nan)
    return (0.0 if k == 0 else float(beta.ppf(a / 2, k, n - k + 1)), 1.0 if k == n else float(beta.ppf(1 - a / 2, k + 1, n - k)))
d = pd.read_csv(sys.argv[1], keep_default_na=False, na_values=[""])
d["o"] = (d.outcome_joint_only.fillna(d.outcome) if "outcome_joint_only" in d else d.outcome).astype(str).str.split(" ").str[0]; d["os"] = d.outcome_split.fillna(d.outcome).astype(str).str.split(" ").str[0]
out = []
for (tic, sec, case), g in d.groupby(["tic", "sector", "case"]):
    sc = g[g.o.isin(["RECOVERED", "INCONSISTENT", "EXCLUDED", "AMBIGUOUS"])]; n = len(sc); row = dict(tic=tic, sector=sec, case=case, runs=len(g), insufficient=int((g.o == "INSUFFICIENT").sum()), n_scored=n)
    for lab, col in (("", "o"), ("split_", "os")):
        for oc in ("RECOVERED", "INCONSISTENT", "EXCLUDED", "AMBIGUOUS"):
            k = int((sc[col] == oc).sum()); lo, hi = cp(k, n); row[f"{lab}{oc[:3]}"] = f"{k}/{n} [{lo:.2f},{hi:.2f}]" if n else "-"
t = pd.DataFrame(out); pd.set_option("display.width", 400); pd.set_option("display.max_colwidth", 40)
txt = t.to_string(index=False); open(sys.argv[2], "w").write(txt + "\n"); print(txt)
