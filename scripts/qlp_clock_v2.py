"""QLP barycentric clock correction, method 2 (round-4 external review, 2026-10-19). Supersedes qlp_clock_check.py and s104_clock_89247735.py,
which wrongly treated TESScut TIME as target-barycentric (TESScut TIMECORR is computed for an FFI reference position, not the target).
For each QLP sector: spacecraft time = TESScut TIME - TIMECORR, matched to QLP cadences (identical cadence lists, else data-gap edges).
QLP offset = QLP - spacecraft. The target light-travel time LTT(t) = r_TESS . n / c is computed from JPL Horizons barycentric TESS vectors
(ICRF) at the event time. Control sectors (S56-S98) give the QLP convention c0 = median(QLP - spacecraft - LTT) (about +2 s).
Correction for an affected sector at the event = LTT(t_event) + c0 - QLP offset(t_event). Frozen files untouched.
Usage: qlp_clock_v2.py TIC  -> results/qlp_clock_v2/<TIC>.json"""
import sys, glob, json, os, numpy as np, pandas as pd, lightkurve as lk
from astropy.io import fits
ROOT = "/Users/fernando/Desktop/NASA"; OUT = f"{ROOT}/results/qlp_clock_v2"; os.makedirs(OUT, exist_ok=True); C_AU_MIN = 149597870.7 / 299792.458 / 60
def qlp_file(tic, s):
    f = glob.glob(f"{ROOT}/data/qlp*/hlsp_qlp_tess_ffi_s{s:04d}-{tic:016d}_tess_v01_llc.fits"); return f[0] if f else None
def cut(tic, s):
    pats = [f"{ROOT}/data/lk_cache/clockcheck/{tic}/**/tess-s{s:04d}-*astrocut.fits"]
    for p in pats:
        f = glob.glob(p, recursive=True)
        if f: return f[0]
    r = lk.search_tesscut(f"TIC {tic}", sector=s)
    if len(r) == 0: return None
    r.download(cutout_size=3, download_dir=f"{ROOT}/data/lk_cache/clockcheck/{tic}")
    f = glob.glob(pats[0], recursive=True); return f[0] if f else None
def ltt(times_btjd, ra, dec):
    """r_TESS . n / c from the JPL Horizons API (barycentric ICRF vectors, TDB epochs), with retries; one request per call."""
    import requests, time
    tl = "\n".join(f"{float(t) + 2457000:.6f}" for t in times_btjd)
    p = dict(format="text", COMMAND="'-95'", EPHEM_TYPE="VECTORS", CENTER="'500@0'", REF_PLANE="FRAME", REF_SYSTEM="ICRF", OUT_UNITS="AU-D", VEC_TABLE="1", CSV_FORMAT="YES", TLIST=tl, TLIST_TYPE="JD", TIME_TYPE="TDB")
    for k in range(8):
        r = requests.get("https://ssd.jpl.nasa.gov/api/horizons.api", params=p, timeout=60)
        if r.ok and "$$SOE" in r.text: break
        time.sleep(5 * (k + 1))
    body = r.text.split("$$SOE")[1].split("$$EOE")[0].strip().splitlines()
    xyz = np.array([[float(v) for v in ln.split(",")[2:5]] for ln in body if ln.strip()])
    a, d = np.radians(ra), np.radians(dec); n = np.array([np.cos(d) * np.cos(a), np.cos(d) * np.sin(a), np.sin(d)])
    return xyz @ n * C_AU_MIN
def qlp_minus_sc(tic, s):
    q, c = qlp_file(tic, s), cut(tic, s)
    if not q or not c: return None
    tq = fits.getdata(q, 1)["TIME"]; tq = tq[np.isfinite(tq)]; d = fits.getdata(c, 1); ok = np.isfinite(d["TIME"]) & (d["TIME"] > 0)
    sc = (d["TIME"] - d["TIMECORR"])[ok]
    if len(tq) == len(sc):
        cq = fits.getdata(q, 1)["CADENCENO"][np.isfinite(fits.getdata(q, 1)["TIME"])]
        assert np.array_equal(np.diff(cq), np.round(np.diff(sc) * 86400 / 200).astype(int)) or np.allclose(np.diff(tq), np.diff(sc), atol=2e-5), f"S{s}: cadence lists differ"
        return tq, (tq - sc) * 1440, "elementwise", sc
    def gaps(t): g = np.diff(t) * 1440; k = np.where(g > 10)[0]; return t[k], t[k + 1], g[k]
    a1, b1, g1 = gaps(tq); a2, b2, g2 = gaps(sc); tt, dt = [], []
    for a, b, g in zip(a1, b1, g1):
        if not len(a2): break
        j = np.argmin(np.abs(a2 - a) * 1440 + np.abs(g2 - g))
        if abs(g2[j] - g) < 1 and abs(a2[j] - a) * 1440 < 20: tt += [a, b]; dt += [(a - a2[j]) * 1440, (b - b2[j]) * 1440]
    return (np.array(tt), np.array(dt), f"gap-edge ({len(dt)//2} gaps)", np.array(tt) - np.array(dt) / 1440) if dt else None
def main():
    global tic
    tic = int(sys.argv[1]); eph = sorted(glob.glob(f"{ROOT}/results/vet*/{tic}/final_ephemeris_v*.json"))
    if tic == 89247735: eph = [f"{ROOT}/results/vet_qlp/89247735/final_ephemeris_v2.json"]   # the raw (uncorrected) QLP retimings
    eph = eph[-1]; d = json.load(open(eph)); rows = d.get("sector_times") or d["transit_times"]
    rep = json.load(open(glob.glob(f"{ROOT}/results/vet*/{tic}/report.json")[0])); ra, dec = rep["meta"]["ra"], rep["meta"]["dec"]
    qlp_secs = sorted(int(os.path.basename(f).split("_s0")[1][:3]) for f in glob.glob(f"{ROOT}/data/qlp*/hlsp_qlp_tess_ffi_s*-{tic:016d}_tess_v01_llc.fits"))
    ctrl = []
    for s in sorted(set(s for s in qlp_secs if 56 <= s <= 98 and not 74 <= s <= 79), key=lambda s: -s)[:2]:   # unique sectors; S74-S79 v01 have a separate MAST-noted timing issue
        m = qlp_minus_sc(tic, s)
        if m is None: continue
        t, dt, mode, tsc = m; idx = np.linspace(0, len(t) - 1, 6).astype(int); c = dt[idx] - ltt(tsc[idx], ra, dec); ctrl.append(dict(sector=s, mode=mode, c0_min=[float(x) for x in c]))
    c0 = float(np.median(np.concatenate([x["c0_min"] for x in ctrl]))) if ctrl else 0.033   # fallback: c0 = +0.032-0.033 min for every star measured (all-sky QLP convention); flagged below
    res = dict(c0_source=("control sectors" if ctrl else "fallback +0.033 min (no clean control sector)"), tic=tic, ephemeris_file=os.path.relpath(eph, ROOT), ra=ra, dec=dec, control=ctrl, c0_min=c0, sectors={})
    for r in rows:
        s = r["sector"]; src = r.get("source", "QLP SAP")
        if not (src.startswith("QLP") and s >= 99): continue
        m = qlp_minus_sc(tic, s)
        if m is None: res["sectors"][s] = None; continue
        t, dt, mode, tsc = m; te = r["tc"]; off = float(np.interp(te, t, dt)); L = float(ltt([te - off / 1440], ra, dec)[0]); corr = L + c0 - off   # LTT at spacecraft time
        res["sectors"][s] = dict(mode=mode, event_btjd=te, qlp_minus_spacecraft_min=off, target_ltt_min=L, correction_min=corr)
    json.dump(res, open(f"{OUT}/{tic}.json", "w"), indent=1)
    print(tic, "c0 %+.3f min" % c0, {s: (round(v["qlp_minus_spacecraft_min"], 3), round(v["target_ltt_min"], 3), round(v["correction_min"], 3)) if v else None for s, v in res["sectors"].items()})


if __name__ == "__main__": main()