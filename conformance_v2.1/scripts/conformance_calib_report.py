"""Holdout calibration report (conformance-v2.1; rewritten after external review R2, label argument added for rc4). Reports raw counts of every outcome category
(including refusals and failures) per target-sector and per case, with Clopper-Pearson 95 % intervals on the raw counts. These intervals
describe this conditional simulation only: realisations share one light curve per sector (not independent), placements are artificial,
and sectors differ (pooled counts are shown but assume a common rate that is not established). No effective-N or family-wise bound is
computed; the family-wise false-RECOVERED rate across the seven S106 tests is not calibrated by this experiment.
Usage: python -I conformance_calib_report.py RUNS.csv OUT.md [LABEL]   (LABEL, e.g. "conformance-v2.1-rc4, evaluator SHA ...", goes in the heading)"""
import sys, numpy as np, pandas as pd
from scipy.stats import beta
def cp(k, n): return (0.0 if k == 0 else float(beta.ppf(.025, k, n - k + 1)), 1.0 if k == n else float(beta.ppf(.975, k + 1, n - k))) if n else (np.nan, np.nan)
d = pd.read_csv(sys.argv[1], keep_default_na=False, na_values=[""]); d["o"] = d.outcome.astype(str).str.split(" ").str[0]
SCORED = ("RECOVERED", "INCONSISTENT", "EXCLUDED", "AMBIGUOUS")
L = ["# Holdout calibration report" + (f" ({sys.argv[3]})" if len(sys.argv) > 3 else ""), "", __doc__.split("Usage")[0].strip().replace("Holdout calibration report (conformance-v2.1; rewritten after external review R2, label argument added for rc4). Reports", "This report gives"), "",
     "Scored = RECOVERED/INCONSISTENT/EXCLUDED/AMBIGUOUS; INSUFFICIENT, INVALID_INPUT, CLOCK_UNVERIFIED and CLOCK_FAILED are listed separately and never enter a denominator.", ""]
L += ["## Per target-sector and case (raw counts; CP95 on raw counts, conditional)", "", "| TIC | sector | case | runs | not scored | " + " | ".join(SCORED) + " |", "|---|---|---|---|---|" + "---|" * len(SCORED)]
for (tic, sec, case), g in d.groupby(["tic", "sector", "case"]):
    s = g[g.o.isin(SCORED)]; n = len(s); ns = g[~g.o.isin(SCORED)].o.value_counts().to_dict()
    cells = [f"{int((s.o == oc).sum())}/{n} [{cp(int((s.o == oc).sum()), n)[0]:.3f}, {cp(int((s.o == oc).sum()), n)[1]:.3f}]" for oc in SCORED]
    L.append(f"| {tic} | {sec} | {case} | {len(g)} | {ns or '-'} | " + " | ".join(cells) + " |")
L += ["", "## Per target, sectors pooled (heterogeneous sectors: pooled rate assumes a common probability that is not established)", "",
      "| TIC | null->RECOVERED | null->EXCLUDED | ontime->RECOVERED | displaced->INCONSISTENT | not scored |", "|---|---|---|---|---|---|"]
for tic, g in d.groupby("tic"):
    def c(case, oc):
        s = g[(g.case == case) & g.o.isin(SCORED)]; k = int((s.o == oc).sum()); lo, hi = cp(k, len(s)); return f"{k}/{len(s)} [{lo:.3f}, {hi:.3f}]"
    L.append(f"| {tic} | {c('null','RECOVERED')} | {c('null','EXCLUDED')} | {c('ontime','RECOVERED')} | {c('displaced','INCONSISTENT')} | {g[~g.o.isin(SCORED)].o.value_counts().to_dict() or '-'} |")
tot = d[(d.case == "null") & d.o.isin(SCORED)]
L += ["", f"All null runs: {int((tot.o == 'RECOVERED').sum())} RECOVERED of {len(tot)} scored (empirical frequency of false RECOVERED in this simulation; not a family-wise error bound)."]
if "clock_warning" in d: L.append(f"Clock warnings in sector >= 99 runs: {int(d[d.sector >= 99].clock_warning.notna().sum())} of {int((d.sector >= 99).sum())}.")
open(sys.argv[2], "w").write("\n".join(L) + "\n"); print("\n".join(L[-12:]))
