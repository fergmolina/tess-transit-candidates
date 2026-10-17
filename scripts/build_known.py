"""Build the known-signal exclusion set: TIC IDs and periods from TOI, CTOI, confirmed planets, and all SPOC TCE tables."""
import pandas as pd, glob, json, numpy as np, re
B = "/Users/fernando/Desktop/NASA/catalogs"
toi = pd.read_csv(f"{B}/toi.csv", low_memory=False)
ctoi = pd.read_csv(f"{B}/ctoi.csv", low_memory=False)
conf = pd.read_csv(f"{B}/confirmed_planets.csv")
conf["tic"] = conf["tic_id"].astype(str).str.extract(r"(\d+)").astype(float)
rows = []
for _, r in toi.iterrows(): rows.append(("TOI", int(r["TIC ID"]), r["Period (days)"], r.get("TFOPWG Disposition"), str(r["TOI"])))
for _, r in ctoi.iterrows(): rows.append(("CTOI", int(r["TIC ID"]), r["Period (days)"], r.get("User Disposition"), str(r["CTOI"])))
for _, r in conf.dropna(subset=["tic"]).iterrows(): rows.append(("CONF", int(r["tic"]), r["pl_orbper"], "CP", r["pl_name"]))
ntce = 0
for f in sorted(glob.glob(f"{B}/tce/*tcestats.csv")):
    sec = re.search(r"(s\d{4}-s\d{4})", f).group(1)
    d = pd.read_csv(f, comment="#", low_memory=False, usecols=["ticid", "tce_period", "tce_depth", "tce_model_snr", "tce_plnt_num"])
    for _, r in d.iterrows(): rows.append((f"TCE:{sec}", int(r["ticid"]), r["tce_period"], f"snr={r['tce_model_snr']:.1f},depth={r['tce_depth']:.0f}", str(r["tce_plnt_num"])))
    ntce += len(d)
known = pd.DataFrame(rows, columns=["source", "tic", "period", "disp", "name"])
known.to_csv(f"{B}/known_signals.csv", index=False)
print("TOI rows", len(toi), "CTOI rows", len(ctoi), "confirmed with TIC", conf["tic"].notna().sum(), "TCE rows", ntce)
print("unique TICs with any known signal:", known["tic"].nunique(), " unique TOI/CTOI/CONF TICs:", known[~known.source.str.startswith("TCE")]["tic"].nunique())
