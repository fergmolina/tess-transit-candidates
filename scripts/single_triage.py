"""Quick-look figures for single-transit candidates: raw SAP flux +-1.5 d around every passing event (box overlaid), background and
centroid in the same window. Usage: python -I single_triage.py [--dir results/single] [--tics ...] [--n 40]"""
import sys, os, json, argparse, warnings; warnings.filterwarnings("ignore"); sys.path.insert(0, "/Users/fernando/Desktop/NASA/scripts")
import numpy as np, pandas as pd, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from single_transit_search import sector_files, load
ap = argparse.ArgumentParser(); ap.add_argument("--dir", default="/Users/fernando/Desktop/NASA/results/single"); ap.add_argument("--tics", type=int, nargs="*"); ap.add_argument("--n", type=int, default=40); a = ap.parse_args()
ev = pd.read_csv(f"{a.dir}/events_pass.csv"); duo = pd.read_csv(f"{a.dir}/duotransits.csv") if os.path.exists(f"{a.dir}/duotransits.csv") else pd.DataFrame()
tics = a.tics or (list(duo.tic.head(a.n)) if len(duo) else []); out = f"{a.dir}/triage"; os.makedirs(out, exist_ok=True)
for tic in tics:
    g = ev[ev.tic == tic].sort_values("tc"); n = len(g)
    if n == 0: continue
    fig, ax = plt.subplots(3, n, figsize=(4.2 * n, 8), squeeze=False); files = {int(os.path.basename(f).split("-")[0].split("s")[-1]): f for f in sector_files(tic)}
    for i, (_, e) in enumerate(g.iterrows()):
        t, f, q, bkg, x, y, tso, meta = load(files[int(e.sector)]); w = np.abs(t - e.tc) < 1.5
        ax[0, i].plot(t[w] - e.tc, f[w], ".", ms=2, color="0.5"); fl = w & (q != 0); ax[0, i].plot(t[fl] - e.tc, f[fl], ".", ms=2, color="orange")
        ax[0, i].axvspan(-e.dur_h / 48, e.dur_h / 48, color="red", alpha=0.15); ax[0, i].set_title(f"TIC {tic} S{int(e.sector)} tc={e.tc:.3f} {e.depth*1e6:.0f}ppm {e.dur_h}h SNR{e.snr:.1f} tso={e.t_since_orbit_start:.1f}d", fontsize=8)
        lo, hi = np.nanpercentile(f[w], [1, 99]); ax[0, i].set_ylim(lo - 2 * e.depth, hi + e.depth)
        ax[1, i].plot(t[w] - e.tc, bkg[w], ".", ms=2); ax[1, i].set_ylabel("SAP_BKG", fontsize=8); ax[1, i].axvspan(-e.dur_h / 48, e.dur_h / 48, color="red", alpha=0.15)
        ax[2, i].plot(t[w] - e.tc, x[w] - np.nanmedian(x[w]), ".", ms=2, label="x"); ax[2, i].plot(t[w] - e.tc, y[w] - np.nanmedian(y[w]), ".", ms=2, label="y"); ax[2, i].set_ylabel("centroid [px]", fontsize=8); ax[2, i].axvspan(-e.dur_h / 48, e.dur_h / 48, color="red", alpha=0.15); ax[2, i].legend(fontsize=7)
    plt.tight_layout(); plt.savefig(f"{out}/{tic}.png", dpi=90); plt.close()
print("figures for", len(tics), "stars in", out)
