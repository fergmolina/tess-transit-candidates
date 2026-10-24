"""Lock per-sector conformance configs for the 14 frozen objects with tests in S107-S121 (2026-10-23; DECISIONS 166), BEFORE any of
these sectors' photometry is examined. Same schema and rules as scripts/make_conformance_configs_round4.py (whose configs are not
touched); refuses to overwrite any existing config.
- Test sectors: sectors with >= 1 row whose status starts with "prediction" in the object's latest prediction CSV (both evaluators score
  only such rows). Retrodiction-only sectors get no config.
- Primary sector (test of record) = the earliest test sector; never replaced (DECISIONS 120(2), adopted for these objects in item 166).
- Reference depth/T14: the registration's frozen "Reference values for the outcome clauses" line. Where a registration predates that line
  (five round-2 objects), the generator rule of every later freeze, as for TIC 70441745 in S106: report.json sap_depth and the shape-fit
  T14_h if present, else the BLS duration_h. It is recorded as a dated amendment.
- Product QLP SAP_FLUX, release of record v01, conformance v2.1 rc4 general rules, pooled edge rule, clock gate with the c0 prior
  results/qlp_clock_v2/<TIC>.json.
Output: configs/conformance/<TIC>_S<sector>.json and configs/conformance/LOCK_2026-10-23_S107_S121.json"""
import os, re, csv, json, hashlib, datetime
R = "/Users/fernando/Desktop/NASA"; OUT = f"{R}/configs/conformance"; LOCK = f"{OUT}/LOCK_2026-10-23_S107_S121.json"
VER = {24526743: "v2", 160330868: "v2", 196514928: "v2", 53825235: "v3", 19119739: "v2", 159033763: "v2", 283913390: "v2", 333661705: "v2",
       162304222: "v4", 258006047: "v2", 333735955: "v2", 467959906: "v2", 203381983: "v2", 366047768: "v2"}
OBSERVED = {107: "observed 2026-08-09 to 09-07", 108: "observed 2026-09-07 to 10-05", 109: "being observed 2026-10-05 to 10-31"}
PRIMARY_RULE = ("The primary sector is the test of record. It stays the test of record whatever its result, including INSUFFICIENT, "
                "CLOCK_UNVERIFIED or INVALID_INPUT; it is never replaced by a later sector. Later listed sectors are scored separately with "
                "their own configs and reported as further tests, never pooled with the primary.")
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest(); EV = sha(f"{R}/scripts/prereg_conformance.py")
assert EV == "a864b07ace8d3220a2d94a60513a488c8a5d87b54f41ebf510ff40ef1755311f", "evaluator changed"
if os.path.exists(LOCK): raise SystemExit(f"refused: {LOCK} exists (locked once)")
stamp = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d %H:%M:%S UTC"); lock = {}
for tic, ver in VER.items():
    d = f"{R}/results/vet_allsky/{tic}"; txt = open(f"{d}/PREREGISTRATION_{ver}.md").read(); pred = f"{d}/predicted_transits_2026_2027_{ver}.csv"
    eph = json.load(open(f"{d}/final_ephemeris_{ver}.json")); h = sha(pred); assert h == eph["sha256_csv"] and h in txt, tic
    secs = sorted({int(m.group(1)) for r in csv.DictReader(open(pred)) if r["status"].startswith("prediction")
                   for m in [re.match(r"\s*(\d+)", r.get("tess_sector") or "")] if m and int(m.group(1)) >= 106})
    m = re.search(r"Reference values for the outcome clauses: depth (\d+) ppm \([^)]*\), T14 ([\d.]+) h", txt)
    if m:
        dep, dur, src = float(m.group(1)), float(m.group(2)), f"PREREGISTRATION_{ver}.md reference-values line (frozen text)"
    else:
        rep = json.load(open(f"{d}/report.json")); dep = round(rep["sap_depth"]["depth_ppm"]); has = "T14_h" in rep.get("shape_mcmc", {})
        dur = rep["shape_mcmc"]["T14_h"] if has else rep["bls_refine"]["duration_h"]
        src = ("dated amendment 2026-10-23 (generator rule, TIC 70441745 precedent): report.json sap_depth; "
               + ("shape-fit T14_h" if has else "BLS duration_h (no shape-fit T14_h)") + f"; PREREGISTRATION_{ver}.md predates the reference-values line")
    prior = f"results/qlp_clock_v2/{tic}.json"; assert os.path.exists(f"{R}/{prior}"), f"no c0 prior for {tic}"
    for sec in secs:
        p = f"{OUT}/{tic}_S{sec}.json"
        if os.path.exists(p): raise SystemExit(f"refused: {p} exists (configs are locked once)")
        primary = sec == secs[0]
        cfg = dict(tic=tic, sector=sec, primary=primary,
                   test_of_record=(f"YES - primary sector of {ver} ({os.path.basename(pred)})" if primary else f"no - further test (primary is S{secs[0]})"),
                   primary_rule=PRIMARY_RULE, product="QLP", flux_col="SAP_FLUX", pred_csv=pred, pred_sha256=h, ref_depth_ppm=round(float(dep), 1),
                   ref_dur_h=round(float(dur), 3), reference_source=src,
                   timing_rule="max(3 mean sigma_min, 30 min) (CLARIFICATION_TIMING_RULE_2026-10-20.md); min(3 sigma, 30 min) reading also reported",
                   evaluator="scripts/prereg_conformance.py (conformance-v2.1 rc4, general rules); frozen scripts/prereg_test.py literal outputs reported as secondary readouts",
                   evaluator_sha256=EV, clock_prior=prior, clock_prior_sha256=sha(f"{R}/{prior}"),
                   clock_note="qlp_clock_test_sector.py reads TIME/TIMECORR of a TESScut cutout of the test sector (run with --declared-test only when this test is run); no TESScut flux is used or scored",
                   frozen_evaluator_commands=[f"python -I scripts/prereg_test.py --lc <QLP S{sec} HLSP FITS> --flux-col {c} --pred {os.path.relpath(pred, R)} --depth-ppm {round(float(dep), 1)} --dur-h {round(float(dur), 3)} --sector {sec}" for c in ("SAP_FLUX", "DET_FLUX")],
                   release_of_record="v01", strict_epochs=None, object_specific_clauses=None,
                   product_note=("QLP SAP_FLUX: the star is on no published 2-min target list for this sector at the lock (S107 manifest; S109/S110 lists; S111+ lists not yet published). "
                                 "If it later appears on one, QLP stays the product of record and SPOC PDCSAP is reported only as a secondary readout."),
                   edge_rule="drop 1.5 d after data start / resume (gap > 0.5 d) and 0.5 d before any gap > 0.1 d or data end (pooled rule; DECISIONS 76, 82, 86)",
                   data_status=(f"sector {OBSERVED[sec]}; public data products exist; the authors attest that no target-sector photometry of this star has been examined "
                                "(held-out check of already-observed data, ERRATUM_S106 class)" if sec in OBSERVED else
                                f"future sector: not observed when the predictions were frozen ({eph['frozen']}) nor when this config was locked"),
                   calibration="none object-specific; the conformance false-recovery calibration was made on the S106 objects only",
                   locked_utc=stamp)
        json.dump(cfg, open(p, "w"), indent=1)
        lock[os.path.basename(p)] = dict(config_sha256=sha(p), tic=tic, sector=sec, primary=primary, pred_sha256=h, clock_prior=prior, clock_prior_sha256=cfg["clock_prior_sha256"])
        print("locked", os.path.basename(p), dep, dur, "PRIMARY" if primary else "", src[:30])
json.dump(dict(made_utc=stamp, note=("Lock manifest for the S107-S121 tests of 14 frozen objects (DECISIONS 166): the SHA-256 of every locked config and of the c0 "
                                     "prior each one names. scripts/validate_round4_inputs.py --lock <this file> refuses any config, prior or clock record not bound to these values."),
               evaluator_sha256=EV, configs=lock), open(LOCK, "w"), indent=1)
print(len(lock), "configs locked; lock", sha(LOCK)[:16])
