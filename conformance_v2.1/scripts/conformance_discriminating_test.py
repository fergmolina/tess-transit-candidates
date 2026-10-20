"""conformance-v2.1 discriminating test (DECISIONS item 77), DESIGN sectors only (S96; S97 for 122522485). Real QLP noise, locked
depth/T14/sigma of each S106 test, back-projected predictions at random phases in [0.2, 0.8]. Cases: null, ontime, opposite
(+-(gate+20) min by epoch parity), randsign (same size, random sign per event; added 2026-10-20 after item 79), dur06 (0.6 x T14), dur15 (1.5 x T14). Targets with P > 6 d (fewer than 2 events fit one design
sector after the edge rule) get their S106 number of events placed at random kept times instead (>= 1 d apart, >= 3.5 T14 from real
transits, fully inside kept data), epochs 0..N-1; the test is then conditional on the events being eligible. Production path: QLP FITS copy (same name) with SAP_FLUX
modified; the evaluator is run as a subprocess. Usage: python -I conformance_discriminating_test.py WORKDIR OUTCSV [N=40] [TIC ...]"""
import sys, os, glob, json, shutil, hashlib, subprocess, numpy as np, pandas as pd
from multiprocessing import Pool
from astropy.io import fits
R = "/Users/fernando/Desktop/NASA"; PY = f"{R}/.venv/bin/python"; EV = f"{R}/scripts/prereg_conformance.py"
DESIGN = {183374279: 96, 120444365: 96, 70441745: 96, 206620592: 96, 122522485: 97, 253931796: 96, 115692561: 96}
CASES = tuple(os.environ.get("DISC_CASES", "null,ontime,opposite,dur06,dur15").split(","))
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
def setup(tic):
    lock = json.load(open(f"{R}/configs/conformance/{tic}_S106.json")); p106 = pd.read_csv(lock["pred_csv"])
    lead = pd.to_numeric(p106.tess_sector.astype(str).str.extract(r"^(\d+)")[0], errors="coerce")
    sig = float(p106[p106.status.astype(str).str.startswith("prediction") & (lead == 106)].sigma_min.mean())
    eph = json.load(open(f"{R}/results/vet_allsky/{tic}/final_ephemeris_v2.json")); sec = DESIGN[tic]
    name = f"hlsp_qlp_tess_ffi_s{sec:04d}-{tic:016d}_tess_v01_llc.fits"; qlp = glob.glob(f"{R}/data/qlp*/{name}")[0]
    n106 = int((p106.status.astype(str).str.startswith("prediction") & (lead == 106)).sum())
    return dict(tic=tic, sec=sec, n106=n106, dep=lock["ref_depth_ppm"], dur_h=lock["ref_dur_h"], sig=sig, gate=max(3 * sig, 30.0), T0=eph["T0_btjd"], P=eph["P_d"], name=name, qlp=qlp)
def run(job):
    S, case, k, ph, work = job; D = f"{work}/{S['tic']}/{case}_{k:02d}"; os.makedirs(D, exist_ok=True)
    with fits.open(S["qlp"], memmap=False) as h:
        d = h[1].data; t = np.asarray(d["TIME"], float); f = np.asarray(d["SAP_FLUX"], float); q = np.asarray(d["QUALITY"], int)
    g = np.isfinite(t) & np.isfinite(f) & (q == 0); tg = t[g]; med = float(np.median(f[g])); T0, P = S["T0"], S["P"]
    if P <= 6:
        n = np.arange(np.ceil((tg.min() - T0) / P - ph), np.floor((tg.max() - T0) / P - ph) + 1).astype(int); tcs = T0 + (n + ph) * P
    else:
        sys.path.insert(0, f"{R}/scripts"); import prereg_conformance as pc
        tk = pc.edge_trim(np.sort(tg), np.ones(len(tg)))[0]; T = S["dur_h"] / 24; rng = np.random.default_rng(int(ph * 1e9)); cad = np.median(np.diff(tk))
        def ok(c):
            w = tk[np.abs(tk - c) < 1.5 * T]
            return len(w) >= 0.9 * 3 * T / cad and np.abs(((c - T0) / P + 0.5) % 1 - 0.5) * P > 3.5 * T
        for _ in range(10000):
            c = np.sort(rng.choice(tk, S["n106"], replace=False))
            if np.all(np.diff(c) >= 1.0) and all(ok(x) for x in c): break
        else: raise RuntimeError("no placement")
        n = np.arange(len(c)); tcs = c
    pp = f"{D}/pred.csv"; pd.DataFrame(dict(epoch=n, tc_btjd=tcs, sigma_min=S["sig"], tess_sector=S["sec"], status="prediction (design-sector discriminating test)")).to_csv(pp, index=False)
    cfg = dict(tic=S["tic"], sector=S["sec"], product="QLP", flux_col="SAP_FLUX", pred_csv=pp, pred_sha256=sha(pp), ref_depth_ppm=S["dep"], ref_dur_h=S["dur_h"])
    cp = f"{D}/cfg.json"; json.dump(cfg, open(cp, "w")); os.makedirs(f"{D}/lc", exist_ok=True); lc = f"{D}/lc/{S['name']}"; shutil.copy(S["qlp"], lc)
    if case != "null":
        dd = S["dur_h"] / 24 * {"dur06": 0.6, "dur15": 1.5}.get(case, 1.0); off = (S["gate"] + 20) / 1440 if case in ("opposite", "randsign") else 0.0
        with fits.open(lc, mode="update") as h:
            tt = np.asarray(h[1].data["TIME"], float); ff = np.array(h[1].data["SAP_FLUX"], float)
            sg = np.random.default_rng(7919 * k + S["tic"] % 1000).choice([-1.0, 1.0], len(n)) if case == "randsign" else np.where(n % 2 == 0, 1.0, -1.0)
            for e, tc, sgn in zip(n, tcs, sg): ff[np.abs(tt - (tc + sgn * off)) < dd / 2] -= S["dep"] * 1e-6 * med
            h[1].data["SAP_FLUX"] = ff
    subprocess.run([PY, "-I", EV, "--config", cp, "--lc", lc, "--out", f"{D}/res.json"], capture_output=True, text=True); os.remove(lc)
    r = json.load(open(f"{D}/res.json")); J = r.get("joint") or {}; sp = r.get("timing_split_max") or {}
    return dict(tic=S["tic"], sector=S["sec"], case=case, k=k, phase=ph, outcome=r["outcome"], outcome_split=r.get("outcome_with_split"), outcome_joint_only=r.get("outcome_joint_only"), outcome_min=r.get("outcome_min_gate_reading"),
                outcome_min_split=r.get("outcome_min_gate_with_split"), n_eligible=r.get("n_eligible"), n_pred=r.get("n_predicted"), joint_off=J.get("offset_min"), joint_dur=J.get("dur_h"),
                joint_dep=J.get("depth_ppm"), joint_snr=J.get("snr"), split_passed=sp.get("passed"), beta=r.get("beta"), sp_depth=(r.get("stack_at_prediction") or {}).get("depth_ppm"),
                sp_err=(r.get("stack_at_prediction") or {}).get("err_ppm"))
if __name__ == "__main__":
    work, outcsv = sys.argv[1], sys.argv[2]; N = int(sys.argv[3]) if len(sys.argv) > 3 else 40; tics = [int(x) for x in sys.argv[4:]] or list(DESIGN)
    jobs = []
    for tic in tics:
        S = setup(tic); rng = np.random.default_rng(77 + tic); phs = rng.uniform(0.2, 0.8, N)
        jobs += [(S, c, k, float(phs[k]), work) for k in range(N) for c in CASES]
    with Pool(12) as pool: rows = pool.map(run, jobs, chunksize=1)
    pd.DataFrame(rows).to_csv(outcsv, index=False); print(len(rows), "runs ->", outcsv)
