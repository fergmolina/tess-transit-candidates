"""Round-6 S0 (review S0-9): FILENAME-ONLY inventory of local caches under data/ for pool stars. No file is opened; only names from
os.walk are parsed (standard TIC/sector filename patterns: SPOC/TESS-SPOC/QLP/TGLC/TESScut). Output:
results/round6_s0/previously_examined_tic_sectors.csv (tic, sector, path) and exposure_inventory.json."""
import os, re, sys, json, pandas as pd
R = "/Users/fernando/Desktop/NASA"; D = f"{R}/results/round6_s0/"
SFX = sys.argv[1] if len(sys.argv) > 1 else ""   # "_v11": pool from prior/pool_targets_ticonly_v11.csv, outputs suffixed
pool = set(pd.read_csv(D + f"prior/pool_targets_ticonly{SFX}.csv").tic.astype("int64"))
TIC = re.compile(r"(?<![\d.])(\d{16})(?![\d.])|tic[-_ ]?0*(\d{4,10})(?!\d)", re.I)   # 16-digit zero-padded id or explicit TIC prefix; never coordinate digits
SEC = re.compile(r"[-_]s0*(\d{1,4})[-_]", re.I)
rows = []; nfiles = 0
for dp, dn, fn in os.walk(f"{R}/data", followlinks=False):
    for f in fn:
        nfiles += 1; full = os.path.join(dp, f); sm = SEC.search(f); sec = int(sm.group(1)) if sm else None
        rel = os.path.relpath(full, f"{R}/data"); hits = {int(m.group(1) or m.group(2)) for m in TIC.finditer(rel)}
        # 2026-10-23 (configs review S3): also the bare-TIC directory convention data/lk_cache/clockcheck/<TIC>/ (clock-tool cutouts)
        parts = rel.split(os.sep)
        if len(parts) >= 3 and parts[0] == "lk_cache" and parts[1] == "clockcheck" and parts[2].isdigit(): hits.add(int(parts[2]))
        for t in hits:
            if t in pool: rows.append(dict(tic=t, sector=sec, path=os.path.relpath(full, R)))
df = pd.DataFrame(rows, columns=["tic", "sector", "path"]).drop_duplicates()
df.to_csv(D + f"previously_examined_tic_sectors{SFX}.csv", index=False)
out = dict(files_listed=nfiles, pool_stars_with_files=int(df.tic.nunique()), by_top_dir=df.path.str.split("/").str[1].value_counts().to_dict(),
           stars_by_sector=df.groupby("sector").tic.nunique().to_dict(), note="recognized local filename evidence only (16-digit ids, TIC-prefixed names, lk_cache/clockcheck/<TIC>/); no file opened. Not proof of non-examination: coordinate-only or unrecognized names, files elsewhere or deleted, and earlier inspection are not ruled out")
json.dump(out, open(D + f"exposure_inventory{SFX}.json", "w"), indent=1, default=str); print(json.dumps(out, default=str))
