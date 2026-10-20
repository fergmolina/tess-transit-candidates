"""Input-validation self-test of prereg_conformance.py v2.1 (rc2 cases added after the external review: R3, R6, R7, R13; rc3 cases: re-check N1, N4; rc4: fresh output per case, exit codes and result identity checked, F1/F4 cases) and qlp_clock_test_sector.py v2.1 (2026-10-20), on IN-SAMPLE data only
(TIC 183374279 QLP Sector 105; no test-sector photometry). Each case declares its expected outcome prefix BEFORE running.
Usage: python -I test_conformance_inputs.py OUTDIR   (writes only under OUTDIR)"""
import sys, os, json, shutil, hashlib, subprocess, numpy as np, pandas as pd
from astropy.io import fits
D = sys.argv[1]; os.makedirs(D, exist_ok=True); R = "/Users/fernando/Desktop/NASA"; PY = f"{R}/.venv/bin/python"
EV, CK = f"{R}/scripts/prereg_conformance.py", f"{R}/scripts/qlp_clock_test_sector.py"
TIC, SEC = 183374279, 105; NAME = f"hlsp_qlp_tess_ffi_s{SEC:04d}-{TIC:016d}_tess_v01_llc.fits"; QLP = f"{R}/data/qlp_allsky/{NAME}"
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
eph = json.load(open(f"{R}/results/vet_allsky/{TIC}/final_ephemeris_v2.json")); T0, P = eph["T0_btjd"], eph["P_d"]
t = fits.getdata(QLP, 1)["TIME"]; t = t[np.isfinite(t)]; n = np.arange(np.ceil((t.min() - T0) / P), np.floor((t.max() - T0) / P) + 1)
def mkcfg(tag, sector=SEC, product="QLP", rows=None, **extra):
    pp = f"{D}/{tag}_pred.csv"
    (rows if rows is not None else pd.DataFrame(dict(epoch=n.astype(int), tc_btjd=T0 + n * P, sigma_min=2.7, tess_sector=SEC, status="prediction (in-sample back-projection)"))).to_csv(pp, index=False)
    cfg = dict(tic=TIC, sector=sector, product=product, flux_col="SAP_FLUX", pred_csv=pp, pred_sha256=sha(pp), ref_depth_ppm=1090.0, ref_dur_h=2.84); cfg.update(extra)
    cp = f"{D}/{tag}_cfg.json"; json.dump(cfg, open(cp, "w")); return cp
def copy_fits(tag, edit=None, name=NAME):
    os.makedirs(f"{D}/{tag}", exist_ok=True); p = f"{D}/{tag}/{name}"; shutil.copy(QLP, p)
    if edit:
        with fits.open(p, mode="update") as h: edit(h)
    return p
def clock_for(cp, lc, tag):
    out = f"{D}/{tag}_ownclock.json"
    if os.path.exists(out): os.remove(out)
    r = subprocess.run([PY, "-I", CK, "--config", cp, "--qlp", lc, "--out", out], capture_output=True, text=True); return out if r.returncode == 0 else None
RUN_N = [0]
def run_eval(cp, lc, clock=None):
    """rc4 (re-check F2): a fresh output path per call, a successful exit required, and the result must refer to the requested
    light curve and config; a crash or a stale/mismatched result is reported as CRASH/STALE, never as an outcome."""
    RUN_N[0] += 1; out = f"{D}/out_{RUN_N[0]:03d}.json"
    if os.path.exists(out): os.remove(out)
    args = [PY, "-I", EV, "--config", cp, "--lc", lc, "--out", out] + (["--clock", clock] if clock else [])
    r = subprocess.run(args, capture_output=True, text=True)
    if r.returncode != 0 or not os.path.exists(out): return "CRASH (exit %d): %s" % (r.returncode, r.stderr.strip().splitlines()[-1] if r.stderr.strip() else "no output")
    j = json.load(open(out))
    if j.get("lc_sha256") != sha(lc) or j.get("config_sha256") != sha(cp): return "STALE (result does not match the requested light curve/config)"
    return j["outcome"]
base = mkcfg("base"); good_clock = f"{D}/good_clock.json"
r = subprocess.run([PY, "-I", CK, "--config", base, "--qlp", QLP, "--out", good_clock], capture_output=True, text=True); assert r.returncode == 0, r.stdout[-300:]
def edited_clock(tag, **kv):
    c = json.load(open(good_clock)); c.update(kv); p = f"{D}/{tag}_clock.json"; json.dump(c, open(p, "w")); return p
ck = json.load(open(good_clock))
csv = f"{D}/lc.csv"; pd.DataFrame(dict(time=t, flux=np.ones(len(t)))).to_csv(csv, index=False)
tq = fits.getdata(QLP, 1); qq0 = np.asarray(tq["QUALITY"]); tt0 = np.asarray(tq["TIME"], float)
ep_flag = int([e for e in n if np.any(np.abs(tt0 - (T0 + e * P)) < 0.02)][0])          # first epoch with data at its centre
def flag_centre(h):
    tt = np.asarray(h[1].data["TIME"], float); q = np.array(h[1].data["QUALITY"]); q[int(np.nanargmin(np.abs(tt - (T0 + ep_flag * P))))] |= 1; h[1].data["QUALITY"] = q
def drop_centre_row(h):   # re-check N1: one missing cadence (row removed) at the strict epoch's centre
    tt = np.asarray(h[1].data["TIME"], float); i = int(np.nanargmin(np.abs(tt - (T0 + ep_flag * P)))); keep = np.ones(len(tt), bool); keep[i] = False
    h[1].data = h[1].data[keep]
def all_flagged(h):
    q = np.array(h[1].data["QUALITY"]); q[:] |= 1; h[1].data["QUALITY"] = q
def dup_time(h):
    tt = np.array(h[1].data["TIME"]); q = np.asarray(h[1].data["QUALITY"]); fl = np.asarray(h[1].data["SAP_FLUX"], float)
    g = np.isfinite(tt) & (q == 0) & np.isfinite(fl); i = int(np.where(g[:-1] & g[1:])[0][100]); tt[i + 1] = tt[i]; h[1].data["TIME"] = tt
def probe_r3():   # external review R3 regression: one event loses a whole allowed shifted box (+100 min) -> must not read EXCLUDED
    tt = np.arange(97, 108, 200 / 86400); ff = 1 + np.random.default_rng(99106).normal(0, 100e-6, len(tt)); keep = ~(np.abs(tt - (100 + 100 / 1440)) < 42.5 / 1440)
    pp = f"{D}/r3_pred.csv"; pd.DataFrame(dict(epoch=[1, 2], tc_btjd=[100.0, 105.0], sigma_min=[43.4, 43.4], tess_sector=[106, 106], status=["prediction"] * 2)).to_csv(pp, index=False)
    cp = f"{D}/r3_cfg.json"; json.dump(dict(tic=1, sector=106, product="synthetic", flux_col="SAP_FLUX", pred_csv=pp, pred_sha256=sha(pp), ref_depth_ppm=1829.0, ref_dur_h=1.5), open(cp, "w"))
    lc = f"{D}/r3.csv"; pd.DataFrame(dict(time=tt[keep], flux=ff[keep])).to_csv(lc, index=False); return run_eval(cp, lc)
def strict_case(tag, epochs, edit=None):
    cp = mkcfg(tag, strict_epochs=epochs); lc = copy_fits(tag, edit) if edit else QLP; return run_eval(cp, lc, clock_for(cp, lc, tag))
CASES = [  # (name, thunk -> outcome, expected prefix)
 ("correct record scores",           lambda: run_eval(base, QLP, good_clock), ("RECOVERED", "AMBIGUOUS", "EXCLUDED", "INCONSISTENT", "INSUFFICIENT")),
 ("no clock record",                 lambda: run_eval(base, QLP), ("CLOCK_UNVERIFIED",)),
 ("clock record wrong TIC",          lambda: run_eval(base, QLP, edited_clock("tic", tic=1)), ("CLOCK_UNVERIFIED",)),
 ("clock record wrong sector",       lambda: run_eval(base, QLP, edited_clock("sec", sector=103)), ("CLOCK_UNVERIFIED",)),
 ("clock record other light curve",  lambda: run_eval(base, QLP, edited_clock("sha", qlp_sha256="0" * 64)), ("CLOCK_UNVERIFIED",)),
 ("clock record other predictions",  lambda: run_eval(base, QLP, edited_clock("pred", pred_sha256="0" * 64)), ("CLOCK_UNVERIFIED",)),
 ("clock record event list differs", lambda: run_eval(base, QLP, edited_clock("ev", event_btjd=[x + 0.01 for x in ck["event_btjd"]])), ("CLOCK_UNVERIFIED",)),
 ("clock record NaN correction",     lambda: run_eval(base, QLP, edited_clock("nan", correction_min=[float("nan")] * len(ck["correction_min"]))), ("CLOCK_UNVERIFIED",)),
 ("CSV with product QLP",            lambda: run_eval(base, csv, good_clock), ("INVALID_INPUT",)),
 ("product not QLP (FITS)",          lambda: run_eval(mkcfg("spoc", product="SPOC"), QLP), ("INVALID_INPUT",)),
 ("file name not QLP HLSP",          lambda: run_eval(base, copy_fits("renamed", name="lc.fits"), good_clock), ("INVALID_INPUT",)),
 ("header ORIGIN not MIT/QLP",       lambda: run_eval(base, copy_fits("origin", lambda h: h[0].header.__setitem__("ORIGIN", "NASA/Ames")), good_clock), ("INVALID_INPUT", "CLOCK_UNVERIFIED")),
 ("header TICID missing",            lambda: run_eval(base, copy_fits("noticid", lambda h: h[0].header.remove("TICID")), good_clock), ("INVALID_INPUT", "CLOCK_UNVERIFIED")),
 ("config sector != header",         lambda: run_eval(mkcfg("wrongsec", sector=104), QLP), ("INVALID_INPUT",)),
 ("no predictions in sector",        lambda: run_eval(mkcfg("nopred", rows=pd.DataFrame(dict(epoch=[1], tc_btjd=[4300.0], sigma_min=[2.7], tess_sector=["107"], status=["prediction"]))), QLP), ("INVALID_INPUT",)),
 ("sector string '1050' not 105",    lambda: run_eval(mkcfg("s1050", rows=pd.DataFrame(dict(epoch=[1], tc_btjd=[4210.0], sigma_min=[2.7], tess_sector=["1050"], status=["prediction"]))), QLP), ("INVALID_INPUT",)),
 ("R3: event missing at a gate offset",  probe_r3, ("AMBIGUOUS", "INCONSISTENT")),
 ("strict epoch with flagged cadence",   lambda: strict_case("strict_flag", [ep_flag], flag_centre), ("INSUFFICIENT",)),
 ("strict epoch not predicted",          lambda: strict_case("strict_none", [99999]), ("INSUFFICIENT",)),
 ("release not of record (v02)",         lambda: run_eval(mkcfg("rel", release_of_record="v01"), copy_fits("v02", name=NAME.replace("_v01_", "_v02_")), good_clock), ("INVALID_INPUT",)),
 ("clock record whole-cadence warning",  lambda: run_eval(base, QLP, edited_clock("warn", warning="median offset within 10 s of a whole cadence")), ("CLOCK_UNVERIFIED",)),
 ("config evaluator SHA mismatch",       lambda: run_eval(mkcfg("evsha", evaluator_sha256="0" * 64), QLP, good_clock), ("INVALID_INPUT",)),
 ("config negative reference depth",     lambda: run_eval(mkcfg("negdep", ref_depth_ppm=-5.0), QLP, good_clock), ("INVALID_INPUT",)),
 ("duplicate prediction epochs",         lambda: run_eval(mkcfg("dupep", rows=pd.DataFrame(dict(epoch=[1, 1], tc_btjd=[4210.0, 4215.0], sigma_min=[2.7, 2.7], tess_sector=[105, 105], status=["prediction"] * 2))), QLP), ("INVALID_INPUT",)),
 ("duplicate cadence times",             lambda: run_eval(base, copy_fits("duptime", dup_time), good_clock), ("INVALID_INPUT",)),
 ("strict epoch with one missing cadence", lambda: strict_case("strict_miss", [ep_flag], drop_centre_row), ("INSUFFICIENT",)),
 ("all cadences flagged",                lambda: (lambda lc: run_eval(base, lc, clock_for(base, lc, "allflag")))(copy_fits("allflag", all_flagged)), ("INSUFFICIENT",)),
 ("all cadences flagged, no clock",      lambda: run_eval(base, copy_fits("allflag2", all_flagged)), ("INSUFFICIENT",)),
 ("TIMEREF header missing",              lambda: run_eval(base, copy_fits("notref", lambda h: h[1].header.remove("TIMEREF")), good_clock), ("INVALID_INPUT",)),
 ("TIMEUNIT header missing",             lambda: run_eval(base, copy_fits("nounit", lambda h: h[1].header.remove("TIMEUNIT")), good_clock), ("INVALID_INPUT",)),
 ("BJDREFF non-numeric",                 lambda: run_eval(base, copy_fits("badreff", lambda h: h[1].header.__setitem__("BJDREFF", "oops")), good_clock), ("INVALID_INPUT",)),
 ("non-integer prediction epoch",        lambda: run_eval(mkcfg("fracep", rows=pd.DataFrame(dict(epoch=[1.5, 2], tc_btjd=[4210.0, 4215.0], sigma_min=[2.7, 2.7], tess_sector=[105, 105], status=["prediction"] * 2))), QLP), ("INVALID_INPUT",)),
 ("TIMEUNIT not days",                   lambda: run_eval(base, copy_fits("tunit", lambda h: h[1].header.__setitem__("TIMEUNIT", "s")), good_clock), ("INVALID_INPUT", "CLOCK_UNVERIFIED")),
 ("clock tool: S106 without flag",   lambda: "REFUSED" if subprocess.run([PY, "-I", CK, "--config", f"{R}/configs/conformance/{TIC}_S106.json", "--qlp", QLP, "--out", f"{D}/x.json"], capture_output=True, text=True).returncode == 2 else "RAN", ("REFUSED",)),
 ("clock tool: QLP header TIC mismatch", lambda: "REFUSED" if subprocess.run([PY, "-I", CK, "--config", base, "--qlp", copy_fits("tic2", lambda h: h[0].header.__setitem__("TICID", 1)), "--out", f"{D}/x.json"], capture_output=True, text=True).returncode == 2 else "RAN", ("REFUSED",)),
]
fails = 0
for name, fn, exp in CASES:
    got = fn(); ok = got.startswith(exp) and not got.startswith(("CRASH", "STALE")); fails += not ok; print(f"{'ok ' if ok else 'FAIL'} {name:38s} expected {'/'.join(exp):40s} got {got[:110]}")
print("FAILURES:", fails); sys.exit(1 if fails else 0)
