"""Clock record for a TEST sector, required by prereg_conformance.py for QLP sectors >= 99 (v2.1, 2026-10-20; replaces v2.0 after the
internal review: v2.0's equal-length branch could never pass because TESScut CADENCENO is always 0, and its unequal-length branch measured
a globbed file instead of --qlp).
For every predicted transit time in the locked config, the QLP-minus-spacecraft offset of the --qlp light curve is measured against a
TESScut cutout of the same sector, camera and CCD (spacecraft time = TESScut TIME - TIMECORR); the target light-travel time is computed from
JPL Horizons TESS vectors at spacecraft time; correction = LTT + c0 - (QLP - spacecraft), with c0 the target's QLP convention offset from
results/qlp_clock_v2/<TIC>.json (clean control sectors <= 98). If MAST has delivered correctly timed products the measured correction is ~0
and is recorded as such: nothing is assumed from the sector number.
ALIGNMENT (absolute, integer cadences): TESScut spacecraft times on their regular cadence grid give FFI indices; QLP CADENCENO gives QLP
indices; the integer shift (within +-8 cadences of the time-based guess) that matches the most cadences is the alignment. Accepted only if
  (a) the best shift matches >= 2 more cadences than any other shift (the data-gap pattern pins the alignment; whether one gap suffices depends on the margin it produces - a single internal gap can pass),
  (b) QLP TIME steps agree with CADENCENO steps: |dTIME - dCADENCENO x cadence| <= 1 s + 2e-4 x dTIME,
  (c) the matched offsets QLP - spacecraft never jump by more than 2 s + 3e-4 x elapsed time between consecutive matched cadences,
  (d) >= 80 % of QLP cadences are matched, and every predicted event lies within the matched time range (+-0.5 d).
Otherwise the script refuses (exit 2) and the evaluator cannot score (CLOCK_UNVERIFIED).
Only the TIME/TIMECORR/CADENCENO columns are used (the files are opened whole; no flux is used). The record stores the hashes of the
config, the prediction CSV, the --qlp file (the evaluator requires it to equal its --lc), the TESScut cutout and the c0 prior.
HOLDOUT: a TESScut cutout is downloaded only when not cached; for sectors >= 106 the script refuses unless --declared-test is given
(the cutout contains pixel data of the test sector). A median offset within 10 s of a whole number of cadences (>= 0.5 cadence)
is corrected but flagged in a "warning" field, which the evaluator copies into its output.
Usage: python -I qlp_clock_test_sector.py --config configs/conformance/<TIC>_S<N>.json --qlp <QLP FITS> --out <clock JSON> [--declared-test]"""
import sys, os, re, glob, json, hashlib, argparse, numpy as np, pandas as pd
sys.path.insert(0, "/Users/fernando/Desktop/NASA/scripts")
import qlp_clock_v2 as q
from astropy.io import fits

VERSION = "qlp_clock_test_sector v2.1 (2026-10-20)"
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
def refuse(msg): print("REFUSED:", msg); sys.exit(2)

def align(tq, cq, sc, search=8):
    """Integer alignment of QLP (TIME, CADENCENO) to TESScut spacecraft times sc. Returns matched (t_qlp, offset_s, stats) or raises ValueError."""
    cad = float(np.median(np.diff(sc))); kf = (sc - sc[0]) / cad; ksc = np.round(kf).astype(int)
    if np.max(np.abs(kf - ksc)) > 0.01: raise ValueError("TESScut spacecraft times are not on a regular cadence grid")
    if np.any(np.diff(cq) <= 0): raise ValueError("QLP CADENCENO not strictly increasing")
    kq = cq - cq[0]; dev = np.abs(np.diff(tq) - np.diff(kq) * cad) * 86400; lim = 1.0 + 2e-4 * np.diff(tq) * 86400
    if np.any(dev > lim): raise ValueError(f"QLP TIME steps disagree with CADENCENO steps (max excess {np.max(dev - lim):.2f} s)")
    pos = {k: i for i, k in enumerate(ksc.tolist())}; s0 = int(np.round((tq[0] - sc[0]) / cad))
    n = {s: sum((k + s) in pos for k in kq.tolist()) for s in range(s0 - search, s0 + search + 1)}
    order = sorted(n, key=lambda s: -n[s]); sb = order[0]; margin = n[sb] - n[order[1]]
    if margin < 2: raise ValueError(f"alignment not pinned: best shift {sb} matches {n[sb]}, next {n[order[1]]} (needs >= 2 more; too few data gaps)")
    if n[sb] < 0.8 * len(tq): raise ValueError(f"only {n[sb]} of {len(tq)} QLP cadences matched (< 80 %)")
    iq = np.array([i for i, k in enumerate(kq.tolist()) if (k + sb) in pos]); isc = np.array([pos[kq[i] + sb] for i in iq])
    t, off = tq[iq], (tq[iq] - sc[isc]) * 86400
    exc = np.abs(np.diff(off)) - (2.0 + 3e-4 * np.diff(t) * 86400)
    if np.any(exc > 0): raise ValueError(f"QLP - spacecraft offset jumps between consecutive matched cadences (max excess {np.max(exc):.1f} s)")
    return t, off, dict(cadence_s=cad * 86400, shift=int(sb), n_matched=int(n[sb]), n_next_best=int(n[order[1]]), n_qlp=len(tq), n_tesscut=len(sc),
                        offset_s_min=float(off.min()), offset_s_max=float(off.max()), max_jump_excess_s=float(np.max(exc)) if len(exc) else None)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--config", required=True); ap.add_argument("--qlp", required=True); ap.add_argument("--out", required=True)
    ap.add_argument("--declared-test", action="store_true", help="required for sectors >= 106: this run downloads/reads the test-sector TESScut cutout")
    a = ap.parse_args(); cfg = json.load(open(a.config)); tic, sec = int(cfg["tic"]), int(cfg["sector"])
    if sec >= 106 and not a.declared_test: refuse(f"sector {sec} is a test sector; rerun with --declared-test only when the declared test is being run")
    if sha(cfg["pred_csv"]) != cfg["pred_sha256"]: refuse("prediction CSV hash != config")
    pf = f"{q.ROOT}/results/qlp_clock_v2/{tic}.json"
    if not os.path.exists(pf): refuse(f"no clock prior {pf} (c0 from control sectors)")
    prior = json.load(open(pf)); c0 = prior["c0_min"]; ra, dec = prior["ra"], prior["dec"]
    if int(prior["tic"]) != tic: refuse("clock prior TIC != config")
    with fits.open(a.qlp, memmap=False) as h:
        H = h[0].header
        if int(H.get("SECTOR", -1)) != sec or int(H.get("TICID", -1)) != tic: refuse(f"QLP header SECTOR/TICID {H.get('SECTOR')}/{H.get('TICID')} != config {sec}/{tic}")
        cam, ccd = int(H["CAMERA"]), int(H["CCD"]); d = h[1].data; tq = np.asarray(d["TIME"], float); cq = np.asarray(d["CADENCENO"], int); ok = np.isfinite(tq); tq, cq = tq[ok], cq[ok]
    pat = f"{q.ROOT}/data/lk_cache/clockcheck/{tic}/**/tess-s{sec:04d}-{cam}-{ccd}_*astrocut.fits"
    cutf = (glob.glob(pat, recursive=True) or [None])[0]
    if cutf is None:
        q.cut(tic, sec); cutf = (glob.glob(pat, recursive=True) or [None])[0]
    if cutf is None: refuse(f"no TESScut cutout for sector {sec} camera {cam} CCD {ccd}")
    with fits.open(cutf, memmap=False) as h:
        d = h[1].data; ok = np.isfinite(d["TIME"]) & (d["TIME"] > 0); sc = (np.asarray(d["TIME"], float) - np.asarray(d["TIMECORR"], float))[ok]
    try: t_ref, off_s, stats = align(tq, cq, sc)
    except ValueError as e: refuse(str(e))
    pred = pd.read_csv(cfg["pred_csv"]); pred = pred[pred.status.astype(str).str.startswith("prediction") & (pd.to_numeric(pred.tess_sector.astype(str).str.extract(r"^(\d+)")[0], errors="coerce") == sec)]
    ev = np.sort(pred.tc_btjd.values.astype(float))
    if not len(ev): refuse("no predicted events in this sector")
    if ev.min() < t_ref.min() - 0.5 or ev.max() > t_ref.max() + 0.5: refuse("a predicted event lies outside the matched time range")
    off = np.interp(ev, t_ref, off_s) / 60; L = q.ltt(ev - off / 1440, ra, dec); corr = L + c0 - off
    idx = np.linspace(0, len(t_ref) - 1, 12).astype(int); Ls = q.ltt(t_ref[idx] - off_s[idx] / 86400, ra, dec); resid_fixed = off_s[idx] / 60 - (Ls + c0)
    state = ("no barycentric term (QLP - spacecraft constant within 10 s)" if np.ptp(off_s) < 10 and abs(np.median(off_s)) < 10 else
             "barycentric term present (QLP - spacecraft - LTT - c0 within 5 s)" if np.max(np.abs(resid_fixed)) * 60 < 5 else "other offset (measured and corrected)")
    med, cad_s = float(np.median(off_s)), stats["cadence_s"]; r = abs(med) % cad_s
    warning = (f"median QLP - spacecraft offset {med:.1f} s is within 10 s of a whole number of cadences: a time-label error and a row "
               "misregistration look the same here; inspect before the outcome is reported") if abs(med) >= 0.5 * cad_s and min(r, cad_s - r) < 10 else None
    out = dict(version=VERSION, warning=warning, script_sha256=sha(__file__), tic=tic, sector=sec, config=os.path.abspath(a.config), config_sha256=sha(a.config), pred_csv=cfg["pred_csv"], pred_sha256=cfg["pred_sha256"],
               qlp_file=os.path.abspath(a.qlp), qlp_sha256=sha(a.qlp), camera=cam, ccd=ccd, tesscut_file=cutf, tesscut_sha256=sha(cutf),
               c0_min=c0, c0_source=prior.get("c0_source", "control sectors"), c0_prior_file=pf, c0_prior_sha256=sha(pf), anchor="integer cadence alignment", alignment=stats, state=state,
               event_btjd=ev.tolist(), qlp_minus_spacecraft_min=off.tolist(), target_ltt_min=L.tolist(), correction_min=corr.tolist(),
               offset_range_over_sector_min=[float(off_s.min() / 60), float(off_s.max() / 60)], method="qlp_clock_test_sector.py v2.1 (method 2, per event)")
    json.dump(out, open(a.out, "w"), indent=1); print(json.dumps({k: out[k] for k in ("tic", "sector", "state", "alignment", "c0_min", "correction_min")}, indent=1))

if __name__ == "__main__": main()
