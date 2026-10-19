"""QLP S99-S104 barycentric clock check for frozen ephemerides (follow-up to the round-3 external review, 2026-10-19).
For each TIC: for every QLP sector used in its frozen ephemeris that lies in S99-S104, plus one control sector outside that range, the QLP
light curve is aligned with a TESScut cutout of the same FFIs. Identical cadence lists give an element-wise offset (gap-edge alignment
otherwise). correction = control offset - affected-sector offset (QLP minus TESScut). The ephemeris is then refitted with the
same weighted linear fit (P held at the BLS value when fewer than 3 sector times exist, as prereg_v2.py does) with and without the corrected
times, and the shift of every frozen prediction is reported. Frozen files are not touched. Output: results/qlp_clock_check/<TIC>.json"""
import sys, glob, json, os, numpy as np, pandas as pd, lightkurve as lk
from astropy.io import fits
ROOT = "/Users/fernando/Desktop/NASA"; OUT = f"{ROOT}/results/qlp_clock_check"; os.makedirs(OUT, exist_ok=True)
def qlp_file(tic, s):
    f = glob.glob(f"{ROOT}/data/qlp*/hlsp_qlp_tess_ffi_s{s:04d}-{tic:016d}_tess_v01_llc.fits"); return f[0] if f else None
def cut(tic, s):
    f = glob.glob(f"{ROOT}/data/lk_cache/clockcheck/{tic}/**/tess-s{s:04d}-*astrocut.fits", recursive=True)
    if f: return f[0]
    r = lk.search_tesscut(f"TIC {tic}", sector=s)
    if len(r) == 0: return None
    r.download(cutout_size=3, download_dir=f"{ROOT}/data/lk_cache/clockcheck/{tic}")
    f = glob.glob(f"{ROOT}/data/lk_cache/clockcheck/{tic}/**/tess-s{s:04d}-*astrocut.fits", recursive=True); return f[0] if f else None
def offset(tic, s):
    q, c = qlp_file(tic, s), cut(tic, s)
    if not q or not c: return None
    tq = fits.getdata(q, 1)["TIME"]; tq = tq[np.isfinite(tq)]; d = fits.getdata(c, 1); tc = d["TIME"][np.isfinite(d["TIME"]) & (d["TIME"] > 0)]
    if len(tq) == len(tc): dt = (tq - tc) * 1440; mode = "elementwise"
    else:   # gap-edge alignment
        def gaps(t): g = np.diff(t) * 1440; k = np.where(g > 10)[0]; return t[k], t[k + 1], g[k]
        a1, b1, g1 = gaps(tq); a2, b2, g2 = gaps(tc); dt = []
        for a, b, g in zip(a1, b1, g1):
            j = np.argmin(np.abs(a2 - a) * 1440 + np.abs(g2 - g)) if len(a2) else None
            if j is not None and abs(g2[j] - g) < 1 and abs(a2[j] - a) * 1440 < 20: dt += [(a - a2[j]) * 1440, (b - b2[j]) * 1440]
        dt = np.array(dt); mode = f"gap-edge ({len(dt)//2} gaps)"
        if len(dt) == 0: return None
    return dict(median_min=float(np.median(dt)), min_min=float(dt.min()), max_min=float(dt.max()), mode=mode, timecorr_min=float(np.median(d["TIMECORR"]) * 1440))
def fit(rows, P0):
    e = np.array([r["mean_epoch"] for r in rows]); t = np.array([r["tc"] for r in rows]); w = 1 / np.array([r["tc_err"] for r in rows]) ** 2
    if len(rows) >= 3:
        A = np.vstack([np.ones_like(e), e]).T; cov = np.linalg.inv(A.T @ (A * w[:, None])); b = cov @ A.T @ (w * t); return b[0], b[1]
    T0 = np.sum(w * (t - e * P0)) / w.sum(); return T0, P0
tic = int(sys.argv[1]); eph = sorted(glob.glob(f"{ROOT}/results/vet*/{tic}/final_ephemeris_v*.json"))[-1]; d = json.load(open(eph)); rows = d["sector_times"]
aff = [r["sector"] for r in rows if r["source"].startswith("QLP") and r["sector"] >= 99]
qlp_secs = sorted(int(os.path.basename(f).split("_s0")[1][:3]) for f in glob.glob(f"{ROOT}/data/qlp*/hlsp_qlp_tess_ffi_s*-{tic:016d}_tess_v01_llc.fits"))
ctrl_cands = [s for s in qlp_secs if 56 <= s <= 98]; ctrl = None
for s in sorted(ctrl_cands, key=lambda s: abs(s - 101)):
    o = offset(tic, s)
    if o: ctrl = (s, o); break
res = dict(tic=tic, ephemeris_file=os.path.relpath(eph, ROOT), control=ctrl, sectors={})
for s in aff: res["sectors"][s] = offset(tic, s)
c0 = ctrl[1]["median_min"] if ctrl else 0.20
new = []
for r in rows:
    r2 = dict(r)
    if r["sector"] in res["sectors"] and res["sectors"][r["sector"]]:
        corr = c0 - res["sectors"][r["sector"]]["median_min"]; r2["tc"] = r["tc"] + corr / 1440; res["sectors"][r["sector"]]["correction_min"] = corr
    new.append(r2)
P0 = d.get("bls_P", d["P_d"]); T0a, Pa = fit(rows, P0); T0b, Pb = fit(new, P0)
res["refit_reproduces_frozen"] = dict(dP_d=float(Pa - d["P_d"]), note="check only; P/T0 frames may differ from the frozen reference epoch")
res["P_old"], res["P_new"] = float(Pa), float(Pb)
csv = sorted(glob.glob(f"{os.path.dirname(eph)}/predicted_transits_*v{d.get('version', 2)}.csv"))
shifts = []
if csv:
    p = pd.read_csv(csv[0]); tcol = "tc_btjd" if "tc_btjd" in p else [c for c in p.columns if c.lower().startswith("tc_b")][0]
    for _, r in p.iterrows():
        tb = r[tcol] - (2457000 if r[tcol] > 2e6 else 0); n = round((tb - T0a) / Pa)
        shifts.append(dict(epoch=int(r["epoch"]), sector=(r.get("tess_sector") if "tess_sector" in p else None), shift_min=float(((T0b + n * Pb) - (T0a + n * Pa)) * 1440), sigma_min=float(r.get("sigma_min", np.nan))))
res["prediction_shifts"] = shifts
json.dump(res, open(f"{OUT}/{tic}.json", "w"), indent=1, default=str)
print(tic, "control", ctrl[0] if ctrl else None, f"{c0:+.2f}", {s: (round(v["median_min"], 2), round(v.get("correction_min", np.nan), 2), v["mode"]) if v else None for s, v in res["sectors"].items()})
if shifts:
    sh = pd.DataFrame(shifts); print("   prediction shift (min): range %+.1f..%+.1f; first rows:" % (sh.shift_min.min(), sh.shift_min.max())); print(sh.head(4).to_string(index=False))
