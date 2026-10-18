"""All-sky target list for the QLP scale-up: TIC dwarfs with Tmag <= 11.5, Teff <= 5300 K, R < 0.85 Rsun (lumclass DWARF), queried in
RA slices; then tess-point sectors (1-105 = QLP coverage on MAST as of 2026-10-18) and the multi-year requirement (>= 2 distinct years).
Outputs catalogs/allsky_dwarfs.csv, catalogs/allsky_tic2sectors.json, catalogs/allsky_targets.csv (the stars to search)."""
import sys, json, time, numpy as np, pandas as pd
from astroquery.mast import Catalogs
ROOT = "/Users/fernando/Desktop/NASA"; MAXSEC = 105
rows = []
for ra0 in range(0, 360, 10):
    for attempt in range(3):
        try:
            tab = Catalogs.query_criteria(catalog="TIC", Tmag=[0, 11.5], Teff=[2000, 5300], rad=[0.05, 0.85], objType="STAR", lumclass="DWARF", ra=[ra0, ra0 + 10], dec=[-90, 90])
            df = tab[["ID", "ra", "dec", "Tmag", "Teff", "rad", "mass", "logg", "contratio", "d", "GAIA"]].to_pandas(); rows.append(df); print(f"RA {ra0:3d}-{ra0+10:3d}: {len(df)}", flush=True); break
        except Exception as e:
            print("retry", ra0, repr(e)[:100], flush=True); time.sleep(20)
cat = pd.concat(rows).drop_duplicates("ID"); cat["ID"] = cat["ID"].astype(int); cat.to_csv(f"{ROOT}/catalogs/allsky_dwarfs.csv", index=False)
print("all-sky dwarfs:", len(cat), "(radius cut applied by the query: stars without a TIC radius are excluded)", flush=True)
# tess-point sectors
from tess_stars2px import tess_stars2px_function_entry
ids, ras, decs = cat["ID"].values, cat["ra"].values, cat["dec"].values
t2s = {}
for i in range(0, len(ids), 5000):
    r = tess_stars2px_function_entry(ids[i:i + 5000], ras[i:i + 5000], decs[i:i + 5000])
    for tid, sec in zip(r[0], r[3]):
        if 1 <= int(sec) <= MAXSEC: t2s.setdefault(int(tid), []).append(int(sec))
    print(f"tess-point {i + 5000}/{len(ids)}", flush=True)
t2s = {k: sorted(set(v)) for k, v in t2s.items()}
json.dump(t2s, open(f"{ROOT}/catalogs/allsky_tic2sectors.json", "w"))
# year of a sector: approximate via sector start dates (sector 1 = 2018-07-25, ~27.4 d each; cycle gaps make this approximate, use table)
orb = pd.read_csv(f"{ROOT}/catalogs/TESS_orbit_times.csv", comment="#")
sec_year = {}
for _, r in orb.iterrows():
    try: sec_year[int(r["Sector"])] = int(str(r["Start of Orbit"]).strip()[:4])
    except Exception: pass
cat["sectors"] = cat["ID"].map(lambda t: t2s.get(t, [])); cat["n_sectors"] = cat.sectors.map(len)
cat["years"] = cat.sectors.map(lambda ss: sorted({sec_year.get(s, 2018 + (s - 1) // 13) for s in ss})); cat["n_years"] = cat.years.map(len)
tg = cat[cat.n_years >= 2].copy(); tg.to_csv(f"{ROOT}/catalogs/allsky_targets.csv", index=False)
print(f"targets with >= 2 years: {len(tg)}; files to download: {int(tg.n_sectors.sum())}; median sectors/star {tg.n_sectors.median()}", flush=True)
