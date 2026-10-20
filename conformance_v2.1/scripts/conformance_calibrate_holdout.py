"""conformance-v2.1 calibration on HOLDOUT sectors only (DECISIONS item 76): 183374279 S69 S103 | 120444365 S69 S103 | 70441745 S68 |
206620592 S68 | 122522485 S105 | 253931796 S68 | 115692561 S69. Locked depth/T14/sigma (hence gates) of each S106 test.
Real transits (rc2, external review R8): for P > 6 d no cadence is masked; instead every placement is at least 0.3 d + 7.5 x T14 from a
real transit of the frozen v2 ephemeris (beyond the +-0.3 d search, the widest box and its +-3-box baseline). For P <= 6 d real transits are
masked (QUALITY |= 1) within +-(T14/2 + 10 min) in CLOCK-CORRECTED time (the clock tool is run on the unmasked copy first). Masks wider than
0.1 d count as gaps for the edge rule (122522485: 0.105 d), so 0.5 d before each masked transit is also trimmed there; S106 has no such
holes. Nulls are nulls only to the extent that the real signal lies inside this support.
Placements: P <= 6 d: scrambled period P' = P x U(0.85, 1.15) and random phase (decorrelates realisations that share one light curve);
P > 6 d: the S106 number of events at random kept times (>= 1 d apart). Cases: null; ontime (reference box); displaced (all events
+(gate + 60) min, i.e. INCONSISTENT power). Production path: QLP FITS copy (same file name) and, for sectors >= 99, the clock tool on
the copy (injections at tc - correction). Realisations share one light curve; their outcomes are not independent. Reported rates are counts of this conditional simulation
(conformance_calib_report.py); no effective-N or family-wise bound is claimed (external review R2).
Usage: python -I conformance_calibrate_holdout.py WORKDIR OUTCSV [N=60] [TIC:SEC ...]"""
import sys, os, glob, json, shutil, hashlib, subprocess, numpy as np, pandas as pd
from multiprocessing import Pool
from astropy.io import fits
R = "/Users/fernando/Desktop/NASA"; PY = f"{R}/.venv/bin/python"; EV, CK = f"{R}/scripts/prereg_conformance.py", f"{R}/scripts/qlp_clock_test_sector.py"
sys.path.insert(0, f"{R}/scripts"); import prereg_conformance as pc
HOLDOUT = [(183374279, 69), (183374279, 103), (120444365, 69), (120444365, 103), (70441745, 68), (206620592, 68), (122522485, 105), (253931796, 68), (115692561, 69)]
CASES = ("null", "ontime", "displaced")
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
def setup(tic, sec):
    assert sec <= 105 and (tic, sec) in HOLDOUT
    lock = json.load(open(f"{R}/configs/conformance/{tic}_S106.json")); p106 = pd.read_csv(lock["pred_csv"])
    lead = pd.to_numeric(p106.tess_sector.astype(str).str.extract(r"^(\d+)")[0], errors="coerce"); m = p106.status.astype(str).str.startswith("prediction") & (lead == 106)
    sig = float(p106[m].sigma_min.mean()); eph = json.load(open(f"{R}/results/vet_allsky/{tic}/final_ephemeris_v2.json"))
    name = f"hlsp_qlp_tess_ffi_s{sec:04d}-{tic:016d}_tess_v01_llc.fits"; qlp = glob.glob(f"{R}/data/qlp*/{name}")[0]
    return dict(tic=tic, sec=sec, n106=int(m.sum()), dep=lock["ref_depth_ppm"], dur_h=lock["ref_dur_h"], sig=sig, gate=max(3 * sig, 30.0), T0=eph["T0_btjd"], P=eph["P_d"], name=name, qlp=qlp)
def placements(S, tg, k):
    rng = np.random.default_rng(1000 * S["tic"] % 2**31 + 7 * S["sec"] + k); T = S["dur_h"] / 24; T0, P = S["T0"], S["P"]
    if P <= 6:
        Pp = P * rng.uniform(0.85, 1.15); ph = rng.uniform(0, 1); n = np.arange(np.ceil((tg.min() - T0) / Pp - ph), np.floor((tg.max() - T0) / Pp - ph) + 1).astype(int)
        return n, T0 + (n + ph) * Pp, Pp
    tk = pc.edge_trim(np.sort(tg), np.ones(len(tg)))[0]; cad = np.median(np.diff(tk))
    ok = lambda c: len(tk[np.abs(tk - c) < 1.5 * T]) >= 0.9 * 3 * T / cad and np.abs(((c - T0) / P + 0.5) % 1 - 0.5) * P > 0.3 + 7.5 * T
    for _ in range(20000):
        c = np.sort(rng.choice(tk, S["n106"], replace=False))
        if np.all(np.diff(c) >= 1.0) and all(ok(x) for x in c): return np.arange(len(c)), c, None
    raise RuntimeError("no placement")
def clock(cp, lc, out):
    r = subprocess.run([PY, "-I", CK, "--config", cp, "--qlp", lc, "--out", out], capture_output=True, text=True)
    return json.load(open(out)) if r.returncode == 0 else None
def run(job):
    S, case, k, work = job; D = f"{work}/{S['tic']}_S{S['sec']}/{case}_{k:03d}"; os.makedirs(f"{D}/lc", exist_ok=True)
    with fits.open(S["qlp"], memmap=False) as h:
        d = h[1].data; t = np.asarray(d["TIME"], float); f = np.asarray(d["SAP_FLUX"], float); q = np.asarray(d["QUALITY"], int)
    g = np.isfinite(t) & np.isfinite(f) & (q == 0); tg = t[g]; med = float(np.median(f[g])); T = S["dur_h"] / 24
    n, tcs, Pp = placements(S, tg, k)
    pp = f"{D}/pred.csv"; pd.DataFrame(dict(epoch=n, tc_btjd=tcs, sigma_min=S["sig"], tess_sector=S["sec"], status="prediction (holdout calibration)")).to_csv(pp, index=False)
    cfg = dict(tic=S["tic"], sector=S["sec"], product="QLP", flux_col="SAP_FLUX", pred_csv=pp, pred_sha256=sha(pp), ref_depth_ppm=S["dep"], ref_dur_h=S["dur_h"])
    cp = f"{D}/cfg.json"; json.dump(cfg, open(cp, "w")); lc = f"{D}/lc/{S['name']}"; shutil.copy(S["qlp"], lc)
    corr = np.zeros(len(tcs)); ck = None; cfn = lambda tt: np.zeros(len(tt))
    if S["sec"] >= 99:   # clock on the UNMASKED copy first, so masking and injection use clock-corrected time
        ck0 = clock(cp, lc, f"{D}/clock_pre.json")
        if ck0 is None: return dict(tic=S["tic"], sector=S["sec"], case=case, k=k, outcome="CLOCK_FAILED")
        corr = np.array(ck0["correction_min"]); ev0 = np.array(ck0["event_btjd"]); cfn = lambda tt: np.interp(tt, ev0, corr) / 1440
    if S["P"] <= 6:
        with fits.open(lc, mode="update") as h:      # remove the real transits: QUALITY |= 1 within +-(T14/2 + 10 min), clock-corrected time
            tt = np.asarray(h[1].data["TIME"], float); qq = np.array(h[1].data["QUALITY"]); fin = np.isfinite(tt); tc_ = np.where(fin, tt, 0) + cfn(np.where(fin, tt, 0))
            real = fin & (np.abs(((tc_ - S["T0"]) / S["P"] + 0.5) % 1 - 0.5) * S["P"] < T / 2 + 10 / 1440); qq[real] |= 1; h[1].data["QUALITY"] = qq
    if case != "null":
        off = (S["gate"] + 60) / 1440 if case == "displaced" else 0.0
        with fits.open(lc, mode="update") as h:
            tt = np.asarray(h[1].data["TIME"], float); ff = np.array(h[1].data["SAP_FLUX"], float)
            for tc, c in zip(tcs, corr): ff[np.abs(tt - (tc + off - c / 1440)) < T / 2] -= S["dep"] * 1e-6 * med
            h[1].data["SAP_FLUX"] = ff
    args = [PY, "-I", EV, "--config", cp, "--lc", lc, "--out", f"{D}/res.json"]
    if S["sec"] >= 99:
        ck = clock(cp, lc, f"{D}/clock.json")
        if ck is None: return dict(tic=S["tic"], sector=S["sec"], case=case, k=k, outcome="CLOCK_FAILED")
        args += ["--clock", f"{D}/clock.json"]
    subprocess.run(args, capture_output=True, text=True); os.remove(lc)
    r = json.load(open(f"{D}/res.json")); J = r.get("joint") or {}; el = [e for e in r.get("events", []) if e.get("eligible")]
    res_ = r.get("edge_trim", {}).get("resumes_btjd", [])
    since = [min([e["tc_btjd"] - s for s in res_ if s <= e["tc_btjd"]] or [np.nan]) for e in el]
    return dict(tic=S["tic"], sector=S["sec"], case=case, k=k, P_used=Pp, outcome=r["outcome"], outcome_split=r.get("outcome_with_split"), outcome_joint_only=r.get("outcome_joint_only"), outcome_min=r.get("outcome_min_gate_reading"),
                per_event_min_met=(r.get("per_event_min_reading") or {}).get("met"), n_eligible=r.get("n_eligible"), n_pred=r.get("n_predicted"), joint_off=J.get("offset_min"),
                joint_dur=J.get("dur_h"), joint_dep=J.get("depth_ppm"), joint_snr=J.get("snr"), min_days_after_resume=float(np.nanmin(since)) if since else None,
                clock_warning=(r.get("clock_record") or {}).get("warning"), excl_diag=json.dumps(r.get("excluded_diagnostics_max")) if r.get("excluded_diagnostics_max") else None)
if __name__ == "__main__":
    work, outcsv = sys.argv[1], sys.argv[2]; N = int(sys.argv[3]) if len(sys.argv) > 3 else 60
    sel = [tuple(int(x) for x in a.split(":")) for a in sys.argv[4:]] or HOLDOUT
    jobs = [(setup(tic, sec), c, k, work) for tic, sec in sel for k in range(N) for c in CASES]
    with Pool(12) as pool: rows = pool.map(run, jobs, chunksize=1)
    pd.DataFrame(rows).to_csv(outcsv, index=False); print(len(rows), "runs ->", outcsv)
