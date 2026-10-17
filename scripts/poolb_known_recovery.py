"""Why are 22 of the 40 known hosts in Pool B not recovered at the catalog period? Classify each miss by (a) period outside the
0.5-20 d grid, (b) < 3 transits falling on QLP data, (c) catalog depth below ~3x the per-transit noise, or (d) in-grid with >= 3
covered transits and adequate depth = a genuine pipeline miss."""
import os, sys, json, glob, numpy as np, pandas as pd; os.environ["TSEARCH_SOURCE"] = "qlp"; sys.path.insert(0, "/Users/fernando/Desktop/NASA/scripts")
from search_pipeline import sector_files, load_lc
known = pd.read_csv("catalogs/known_signals.csv"); known = known[known.source.isin(["TOI", "CTOI", "CONF"])]
toi = pd.read_csv("catalogs/toi.csv", low_memory=False); ctoi = pd.read_csv("catalogs/ctoi.csv", low_memory=False)
top = pd.read_csv("results/ranked_top_peak_qlp.csv"); allp = pd.read_csv("results/ranked_all_peaks_qlp.csv")
hosts = sorted(set(known.tic) & set(top.tic)); print("known hosts in Pool B:", len(hosts))
rows = []
for tic in hosts:
    k = known[known.tic == tic]; pk = allp[allp.tic == tic]; tp = top[top.tic == tic].iloc[0]
    def match(P): return any(abs(pk.period / (m * P) - 1).min() < 0.01 for m in (1, 2, 0.5, 3, 1 / 3)) if len(pk) else False
    # light-curve time coverage
    T = np.concatenate([load_lc(f)[0] for f in sector_files(tic)]); T = T[np.isfinite(T)]
    rms = float(tp.get("rms_ppm", np.nan)) if "rms_ppm" in tp else np.nan
    for _, s in k.iterrows():
        P = s.period
        if not np.isfinite(P) or P <= 0: continue
        t = toi[(toi["TIC ID"] == tic) & (abs(toi["Period (days)"] - P) < 0.01)]
        epoch = float(t["Epoch (BJD)"].iloc[0]) - 2457000 if len(t) and np.isfinite(t["Epoch (BJD)"].iloc[0]) else None
        depth = float(t["Depth (ppm)"].iloc[0]) if len(t) and "Depth (ppm)" in t else np.nan
        dur = float(t["Duration (hours)"].iloc[0]) if len(t) and "Duration (hours)" in t else np.nan
        if epoch is not None:
            n = np.arange(np.floor((T.min() - epoch) / P), np.ceil((T.max() - epoch) / P) + 1); tcs = epoch + n * P
            ncov = int(sum(np.sum(np.abs(T - tc) < max(dur, 1) / 48) >= 3 for tc in tcs))
        else: ncov = int((T.max() - T.min()) / P * 0.6)  # rough duty estimate when no epoch
        rec = match(P)
        if rec: cls = "recovered (top-3 peak incl. aliases)"
        elif P < 0.5 or P > 20: cls = "period outside grid"
        elif ncov < 3: cls = f"<3 transits on data ({ncov})"
        else: cls = "in-grid, >=3 transits: pipeline miss"
        rows.append(dict(tic=tic, src=s.source, name=s.get("name", ""), P=round(P, 4), depth_ppm=depth, dur_h=dur, n_cov=ncov, top_P=round(tp.period, 4), top_sde=round(tp.sde, 1), cls=cls))
df = pd.DataFrame(rows).drop_duplicates(["tic", "P"]); pd.set_option("display.width", 250)
print(df.sort_values("cls").to_string(index=False)); print(df.groupby("cls").size()); df.to_csv("results/poolb_known_recovery.csv", index=False)
