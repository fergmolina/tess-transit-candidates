"""Position-based known-signal check: TIC cone search (MAST) around a target, then look up every neighbouring TIC in catalogs/known_signals.csv
(TOI/CTOI/confirmed/TCE) and flag period matches (1x, 2x, 0.5x, 3x, 1/3x within 1 %). Usage: python -I known_nearby.py TIC PERIOD [--radius-arcsec 60]"""
import sys, argparse, numpy as np, pandas as pd
from astroquery.mast import Catalogs
ap = argparse.ArgumentParser(); ap.add_argument("tic", type=int); ap.add_argument("period", type=float); ap.add_argument("--radius-arcsec", type=float, default=60); a = ap.parse_args()
known = pd.read_csv("/Users/fernando/Desktop/NASA/catalogs/known_signals.csv", low_memory=False)
cat = Catalogs.query_object(f"TIC {a.tic}", catalog="TIC", radius=a.radius_arcsec / 3600).to_pandas()
cat["ID"] = cat["ID"].astype(int); print(f"{len(cat)} TIC entries within {a.radius_arcsec}\" of TIC {a.tic}")
hits = known[known.tic.isin(cat.ID)]
if not len(hits): print("no TOI/CTOI/confirmed/TCE entry on any TIC within the radius"); sys.exit()
for _, r in hits.iterrows():
    row = cat[cat.ID == r.tic].iloc[0]; sep = float(row.get("dstArcSec", np.nan)); kp = r.period
    tag = [lab for mult, lab in ((1, "P"), (2, "2P"), (0.5, "P/2"), (3, "3P"), (1 / 3, "P/3")) if pd.notna(kp) and kp > 0 and abs(a.period * mult - kp) / kp < 0.01]
    print(f"  TIC {r.tic} sep {sep:.1f}\" Tmag {row.get('Tmag')}: {r.source} P={kp}  {'<-- PERIOD MATCH ' + ','.join(tag) if tag else ''}")
