"""Future TESS sectors (> 105) for every all-sky target, from tess-point. Output catalogs/allsky_tic2sectors_future.json {tic: [sectors]}."""
import json, pandas as pd
from tess_stars2px import tess_stars2px_function_entry as f
ROOT = "/Users/fernando/Desktop/NASA"; tg = pd.read_csv(f"{ROOT}/catalogs/allsky_targets.csv")
ids, ras, decs = tg["ID"].values, tg["ra"].values, tg["dec"].values; out = {}
for i in range(0, len(ids), 5000):
    r = f(ids[i:i + 5000], ras[i:i + 5000], decs[i:i + 5000])
    for tid, sec in zip(r[0], r[3]):
        if int(sec) > 105: out.setdefault(int(tid), []).append(int(sec))
    print(i + 5000, flush=True)
out = {k: sorted(set(v)) for k, v in out.items()}; json.dump(out, open(f"{ROOT}/catalogs/allsky_tic2sectors_future.json", "w"))
print("targets with future sectors:", len(out), "of", len(ids))
