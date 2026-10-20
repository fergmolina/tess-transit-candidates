"""Re-tabulate discriminating-test runs from their res.json files (joint, joint + split, literal per-event). Usage: python -I conformance_disc_analyse.py RUNDIR OUT.csv
Runs made before DECISIONS item 82 carry the joint-only outcome in "outcome" and the split outcome in "outcome_with_split"; later runs carry the
split outcome in "outcome" and the joint-only one in "outcome_joint_only" (both handled here)."""
import sys, glob, json, numpy as np, pandas as pd
from scipy.stats import beta
def cp(k,n): return (0.0 if k==0 else beta.ppf(.025,k,n-k+1), 1.0 if k==n else beta.ppf(.975,k+1,n-k))
rows=[]
for p in glob.glob(f"{sys.argv[1]}/*/*/res.json"):
    tic=int(p.split("/")[-3]); case=p.split("/")[-2].rsplit("_",1)[0]; r=json.load(open(p))
    el=[e for e in r.get("events",[]) if e.get("eligible")]
    lit = "INSUFFICIENT" if len(el)<2 else ("RECOVERED" if sum(bool(e.get("match_max")) for e in el)>=2 else "NOT")
    rows.append(dict(tic=tic,case=case,o=(r.get("outcome_joint_only") or r["outcome"]).split(" ")[0],os=r.get("outcome_with_split") or r["outcome"].split(" ")[0],lit=lit,nel=len(el)))
d=pd.DataFrame(rows); d.to_csv(sys.argv[2],index=False)
for col,lab in (("o","joint (v2.1 as is)"),("os","joint + timing split"),("lit","literal per-event (>=2 events: own best box SNR>=3, depth 0.5-1.5x, dur 0.7-1.3x, |o|<=gate)")):
    print("==",lab)
    out={}
    for (tic,case),g in d.groupby(["tic","case"]):
        s=g[g.o!="INSUFFICIENT"]; n=len(s); k=int((s[col]=="RECOVERED").sum()); lo,hi=cp(k,n) if n else (np.nan,np.nan)
        out.setdefault(tic,{})[case]=f"{k}/{n} ({lo:.2f}-{hi:.2f})"
    print(pd.DataFrame(out).T[["ontime","null","opposite","dur06","dur15"]].to_string())
s=d[d.o!="INSUFFICIENT"]
print("== EXCLUDED / INCONSISTENT counts (joint as is)"); print(pd.crosstab([s.tic,s.case],s.o).to_string())
