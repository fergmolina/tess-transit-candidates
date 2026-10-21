"""Regression tests for prior_match.py (2026-10-21; re-check R2). Cases: (1) the primary RAVEN tables (Zenodo 19661443, column bls_per)
must give period matches for 80387959, 249813122, 333661705 and 151767028; (2) a synthetic copy of the Nigraha neighbouring-row layout
(a matching number in ANOTHER star's column) must give no match; (3) a gzip table must be read; (4) a TIC-bearing table without a period
column must be listed as unresolved, not as a negative. Fresh output directory per run; exit codes checked. Usage: python -I
test_prior_match.py TMPDIR (must not exist)"""
import sys, os, gzip, subprocess, pandas as pd
R = "/Users/fernando/Desktop/NASA"; PY = f"{R}/.venv/bin/python"; T = sys.argv[1]
if os.path.exists(T): raise SystemExit(f"refused: {T} exists (fresh directory required)")
os.makedirs(f"{T}/corpus/syn"); fails = []
pd.DataFrame(dict(tic=[80387959, 249813122, 333661705, 151767028, 188664994, 999], period=[4.192173, 4.176147, 1.383225, 2.210401, 3.781806, 1.0])).to_csv(f"{T}/targets.csv", index=False)
open(f"{T}/corpus/syn/nigraha_like.csv", "w").write("rowid,TIC_ID,T0,Period,lum\n1,207439389,1931.7,8.705,3.78238988\n2,188664994,1933.1,12.4289,0.18\n")
with gzip.open(f"{T}/corpus/syn/signals.csv.gz", "wt") as g: g.write("tic,bls_per,label\n999,1.0004,real\n")
open(f"{T}/corpus/syn/noperiod.csv", "w").write("tic,depth\n999,500\n")
def run(roots, out):
    r = subprocess.run([PY, "-I", f"{R}/scripts/prior_match.py", f"{T}/targets.csv", out] + roots, capture_output=True, text=True)
    if r.returncode != 0: fails.append(f"matcher exit {r.returncode}: {r.stderr[-300:]}"); return None
    return pd.read_csv(out, keep_default_na=False)
a = run([f"{R}/results/prior_search_round4/data/20261021_raven"], f"{T}/raven.csv")
if a is not None:
    hit = set(a[a.match.astype(str) == "True"].tic)
    for t in (80387959, 249813122, 333661705, 151767028): (None if t in hit else fails.append(f"RAVEN primary: no match for {t}"))
    if 188664994 in hit: fails.append("RAVEN primary: unexpected match for 188664994")
b = run([f"{T}/corpus"], f"{T}/syn.csv")
if b is not None:
    m = b[b.match.astype(str) == "True"]
    if 188664994 in set(m.tic): fails.append("neighbouring-row false match reproduced")
    if 999 not in set(m.tic): fails.append("gzip table not matched")
    u = pd.read_csv(f"{T}/syn_unresolved.csv", keep_default_na=False) if os.path.exists(f"{T}/syn_unresolved.csv") else pd.DataFrame(columns=["source"])
    if not u.source.str.endswith("noperiod.csv").any(): fails.append("TIC-only table not listed as unresolved")
print("\n".join(fails) if fails else "all prior_match regression checks passed"); sys.exit(1 if fails else 0)
