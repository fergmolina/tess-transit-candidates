"""Query MAST TIC for stellar params of a TIC list, in chunks."""
import json, sys, time, warnings; warnings.filterwarnings("ignore")
import pandas as pd
from astroquery.mast import Catalogs
B = "/Users/fernando/Desktop/NASA/catalogs"
tics = json.load(open(f"{B}/s107_multiyear_tics.json"))
cols = ["ID","ra","dec","Tmag","Teff","logg","rad","mass","lum","d","contratio","GAIA","Vmag","Jmag","gaiabp","gaiarp","objType","lumclass","disposition"]
rows = []
CH = 500
for i in range(0, len(tics), CH):
    chunk = tics[i:i+CH]
    for attempt in range(4):
        try:
            tab = Catalogs.query_criteria(catalog="TIC", ID=chunk)
            break
        except Exception as e:
            print("retry", i, e, file=sys.stderr); time.sleep(5)
    df = tab.to_pandas()
    rows.append(df[[c for c in cols if c in df.columns]])
    print(f"{i+len(chunk)}/{len(tics)}", flush=True)
out = pd.concat(rows, ignore_index=True)
out["ID"] = out["ID"].astype(int)
out.to_csv(f"{B}/s107_multiyear_tic_params.csv", index=False)
print(out.describe().T[["count","min","50%","max"]])
