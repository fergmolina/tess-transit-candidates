"""TIC 89247735: three single-sector transits (S66, S93, S104). Which period aliases P=P0/n are allowed by the
data (no predicted transit falling in good data without a dip), and what are the individual transit times?"""
import sys, json, numpy as np; sys.path.insert(0, "/Users/fernando/Desktop/NASA/scripts")
import os; os.environ["TSEARCH_SOURCE"] = "qlp"
from vet import load_all, stitch, time_transits, gaia_neighbours, fit_shape
import pandas as pd
tic = 89247735; P0 = 18.32303; dur_h = 4.0
r = json.load(open(f"results/search_qlp/{tic}.json")); T0 = r["stitched"]["peaks"][0]["t0"]
secs = load_all(tic, P0, T0, dur_h / 24); t, f, fe = stitch(secs)
print("points", len(t), "span", t.min(), t.max())
# individual transit times at P0
sh = fit_shape(t, f, fe, P0, T0, dur_h / 24, 0.0082, 34.0); print("shape fit:", {k: (round(v,4) if isinstance(v,float) else v) for k,v in sh.items() if not isinstance(v,(list,dict))})
tt = time_transits(t, f, fe, P0, T0, dur_h / 24, sh["rprs"], sh["ars"], sh["b"])
print("timed transits:", json.dumps(tt, default=float)[:1500])
# alias test: for P = P0/n, count predicted transits that land on good data (>=60% coverage of +-dur) and whether a dip is seen
out = []
for n in range(1, 13):
    P = P0 / n; eps = np.arange(np.floor((t.min() - T0) / P) - 1, np.ceil((t.max() - T0) / P) + 2)
    cov = []; dips = []
    for e in eps:
        tc = T0 + e * P; w = np.abs(t - tc) < dur_h / 24 / 2; o = (np.abs(t - tc) < 3 * dur_h / 24) & ~w
        if w.sum() >= 6 and o.sum() >= 20:
            d = np.median(f[o]) - np.median(f[w]); err = 1.4826 * np.median(np.abs(f[o] - np.median(f[o]))) / np.sqrt(w.sum())
            cov.append(int(e)); dips.append((round(d * 1e6), round(d / err, 1)))
    seen = sum(1 for d in dips if d[1] > 5); missed = sum(1 for d in dips if d[1] < 3)
    out.append(dict(n=n, P=round(P, 5), n_covered=len(cov), n_dips=seen, n_missed=missed, detail=dips))
    print(f"n={n:2d} P={P:8.4f} covered={len(cov):3d} dips>5sig={seen} missed(<3sig)={missed}  {dips[:12]}")
pool = pd.read_csv("catalogs/qlp/s104_dwarf_pool.csv", usecols=["ID", "ra", "dec", "Tmag"]).set_index("ID")
ra, dec = pool.loc[tic, ["ra", "dec"]]
g = gaia_neighbours(ra, dec, 90, depth=0.0082)
print("\nGaia neighbours within 90 arcsec:")
for s in g[:12]: print(f"  sep={s['sep_arcsec']:6.1f}\" G={s['G']:5.2f} dG={s['dG']:5.2f} req_depth={s['required_depth_if_source']}")
json.dump(dict(transit_times=tt, aliases=out, gaia=g), open("results/triage_qlp/89247735_alias_gaia.json", "w"), default=float, indent=1)
