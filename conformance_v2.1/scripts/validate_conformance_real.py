"""Real-data validation and calibration of prereg_conformance.py (v2.1, 2026-10-20) on IN-SAMPLE QLP sectors (<= 105) only; NOT a test
of the candidates. Every run goes through the production path: a copy of the QLP HLSP FITS (same file name, own directory) with SAP_FLUX
modified for injections, the clock record from qlp_clock_test_sector.py for sectors >= 99, and the LOCKED settings of
configs/conformance/<TIC>_S106.json (reference depth and T14; sigma_min = the mean sigma_min of that test's S106 predictions, so the
timing gates are the test's own gates). Injections (rectangular boxes at the reference depth and T14) are placed at tc - correction(tc)
in raw QLP time, so that after the clock correction they sit exactly at the predicted times.
Modes: validate        known transit at the back-projected v2 ephemeris; empty half-phase windows; injection at half-phase
       calib N SEED    N random phases in [0.2, 0.8]: a null (no injection) and an injection at each phase
For each eligible event the time since the last data resume after a gap > 0.5 d is recorded (edge diagnostics).
Usage: python -I validate_conformance_real.py OUTDIR TIC SECTOR MODE [N SEED]   (writes only under OUTDIR/<TIC>_S<SECTOR>_<MODE>/)"""
import sys, os, glob, json, shutil, hashlib, subprocess, numpy as np, pandas as pd
from astropy.io import fits
R = "/Users/fernando/Desktop/NASA"; PY = f"{R}/.venv/bin/python"; EV, CK = f"{R}/scripts/prereg_conformance.py", f"{R}/scripts/qlp_clock_test_sector.py"
OUT, TIC, SEC, MODE = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
assert SEC <= 105, "in-sample sectors only (<= 105)"
D = f"{OUT}/{TIC}_S{SEC}_{MODE}" + (f"_{sys.argv[6]}" if MODE == "calib" else ""); os.makedirs(D, exist_ok=True)
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
lock = json.load(open(f"{R}/configs/conformance/{TIC}_S106.json")); dep, dur_h = lock["ref_depth_ppm"], lock["ref_dur_h"]
p106 = pd.read_csv(lock["pred_csv"]); lead = pd.to_numeric(p106.tess_sector.astype(str).str.extract(r"^(\d+)")[0], errors="coerce")
SIG = float(p106[p106.status.astype(str).str.startswith("prediction") & (lead == 106)].sigma_min.mean())
eph = json.load(open(f"{R}/results/vet_allsky/{TIC}/final_ephemeris_v2.json")); T0, P = eph["T0_btjd"], eph["P_d"]
NAME = f"hlsp_qlp_tess_ffi_s{SEC:04d}-{TIC:016d}_tess_v01_llc.fits"; QLP = glob.glob(f"{R}/data/qlp*/{NAME}")[0]
with fits.open(QLP, memmap=False) as h:
    d = h[1].data; t = np.asarray(d["TIME"], float); f = np.asarray(d["SAP_FLUX"], float); qq = np.asarray(d["QUALITY"], int)
good = np.isfinite(t) & np.isfinite(f) & (qq == 0); tg = np.sort(t[good]); med = float(np.median(f[good]))
starts = tg[np.r_[0, np.where(np.diff(tg) > 0.5)[0] + 1]]
def since_start(tc): s = starts[starts <= tc]; return float(tc - s.max()) if len(s) else None
kinds = [("transit", 0.0, False), ("null_halfphase", 0.5, False), ("inject_halfphase", 0.5, True)]
if MODE == "calib":
    rng = np.random.default_rng(int(sys.argv[6]) * 1000 + TIC % 997 + SEC); kinds = [(f"{k}_{ph:.4f}", float(ph), k == "inject") for ph in rng.uniform(0.2, 0.8, int(sys.argv[5])) for k in ("null", "inject")]
def clock(cp, fits_path, tag):
    out = f"{D}/{tag}_clock.json"; r = subprocess.run([PY, "-I", CK, "--config", cp, "--qlp", fits_path, "--out", out], capture_output=True, text=True)
    return (out, json.load(open(out))) if r.returncode == 0 else (None, r.stdout.strip()[-120:])
rows = []
for kind, shift, inject in kinds:
    n = np.arange(np.ceil((tg.min() - T0) / P - shift), np.floor((tg.max() - T0) / P - shift) + 1); tcs = T0 + (n + shift) * P
    pp = f"{D}/{kind}_pred.csv"; pd.DataFrame(dict(epoch=n.astype(int), tc_btjd=tcs, sigma_min=SIG, tess_sector=SEC, status="prediction (diagnostic back-projection; in-sample)")).to_csv(pp, index=False)
    cfg = dict(tic=TIC, sector=SEC, product="QLP", flux_col="SAP_FLUX", pred_csv=pp, pred_sha256=sha(pp), ref_depth_ppm=dep, ref_dur_h=dur_h, locked_from=f"configs/conformance/{TIC}_S106.json", sigma_min_used=SIG)
    cp = f"{D}/{kind}_cfg.json"; json.dump(cfg, open(cp, "w"))
    corr = np.zeros(len(tcs))
    if SEC >= 99:
        ckp, ck = clock(cp, QLP, f"{kind}_orig")
        if ckp is None: rows.append(dict(kind=kind, outcome="CLOCK " + ck)); continue
        corr = np.array(ck["correction_min"]); assert np.allclose(ck["event_btjd"], np.sort(tcs))
    os.makedirs(f"{D}/{kind}", exist_ok=True); lc = f"{D}/{kind}/{NAME}"; shutil.copy(QLP, lc)
    if inject:
        with fits.open(lc, mode="update") as h:
            tt = np.asarray(h[1].data["TIME"], float); ff = np.array(h[1].data["SAP_FLUX"], float)
            for tc, c in zip(np.sort(tcs), corr): ff[np.abs(tt - (tc - c / 1440)) < dur_h / 48] -= dep * 1e-6 * med
            h[1].data["SAP_FLUX"] = ff
    args = [PY, "-I", EV, "--config", cp, "--lc", lc, "--out", f"{D}/{kind}.json"]
    if SEC >= 99:
        ckp, ck = clock(cp, lc, kind)
        if ckp is None: rows.append(dict(kind=kind, outcome="CLOCK " + ck)); continue
        args += ["--clock", ckp]
    subprocess.run(args, capture_output=True, text=True); r = json.load(open(f"{D}/{kind}.json")); J = r.get("joint") or {}
    el = [e for e in r.get("events", []) if e.get("eligible")]
    rows.append(dict(tic=TIC, sector=SEC, kind=kind, outcome=r["outcome"], min_gate=r.get("outcome_min_gate_reading"), eligible=r.get("n_eligible"), n_pred=r.get("n_predicted"),
                     joint_off=J.get("offset_min"), joint_dur=J.get("dur_h"), joint_dep=J.get("depth_ppm"), joint_snr=J.get("snr"), p_cons=J.get("consistency_p"),
                     beta=round(r.get("beta", np.nan), 2), gate_max=r.get("gate_max_min"), min_days_after_start=min([since_start(e["tc_btjd"]) or 99 for e in el]) if el else None,
                     clock_min=[round(x, 2) for x in r.get("clock_correction_min_range", [])]))
pd.set_option("display.width", 250); out = pd.DataFrame(rows); print(out.to_string(index=False)); out.to_csv(f"{D}/summary.csv", index=False)
