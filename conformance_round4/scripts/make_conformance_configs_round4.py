"""Lock per-sector conformance configs for the three round-4 registrations (2026-10-21; review F2 in results/REVIEW_round4_freezes.md),
BEFORE any of these sectors is observed. Separate from make_conformance_configs.py, whose seven S106 configs are not touched; refuses to
overwrite any existing config. Reference depth/duration: the registration's frozen "Reference values for the outcome clauses" line.
Product QLP SAP_FLUX, release of record v01, general rules of conformance v2.1 rc4 (no strict epochs, no object-specific clauses), pooled
edge rule, clock gate (qlp_clock_test_sector.py with the c0 prior results/qlp_clock_v2/<TIC>.json). The frozen prereg_test.py literal
outputs (SAP_FLUX and DET_FLUX) are secondary readouts. PRIMARY = the test of record per object (rule in PRIMARY_RULE).
Output: configs/conformance/<TIC>_S<sector>.json"""
import os, re, json, hashlib, datetime
R = "/Users/fernando/Desktop/NASA"; OUT = f"{R}/configs/conformance"
TESTS = {151767028: [112, 113, 114], 343298093: [113, 114], 188664994: [117, 118, 119]}
PRIMARY = {151767028: 112, 343298093: 113, 188664994: 117}
PRIMARY_RULE = ("The primary sector is the test of record. It stays the test of record whatever its result, including INSUFFICIENT, "
                "CLOCK_UNVERIFIED or INVALID_INPUT; it is never replaced by a later sector. Later listed sectors are scored separately with "
                "their own configs and reported as further tests, never pooled with the primary.")
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest(); EV = sha(f"{R}/scripts/prereg_conformance.py")
assert EV == "a864b07ace8d3220a2d94a60513a488c8a5d87b54f41ebf510ff40ef1755311f", "evaluator changed"
stamp = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d %H:%M:%S UTC")
for tic, secs in TESTS.items():
    d = f"{R}/results/vet_allsky/{tic}"; txt = open(f"{d}/PREREGISTRATION_v2.md").read(); pred = f"{d}/predicted_transits_2026_2027_v2.csv"
    m = re.search(r"Reference values for the outcome clauses: depth (\d+) ppm \([^)]*\), T14 ([\d.]+) h", txt); dep, dur = float(m.group(1)), float(m.group(2))
    eph = json.load(open(f"{d}/final_ephemeris_v2.json")); h = sha(pred); assert h == eph["sha256_csv"] and h in txt, tic
    assert os.path.exists(f"{R}/results/qlp_clock_v2/{tic}.json"), f"no c0 prior for {tic}"
    for sec in secs:
        p = f"{OUT}/{tic}_S{sec}.json"
        if os.path.exists(p): raise SystemExit(f"refused: {p} exists (configs are locked once)")
        cfg = dict(tic=tic, sector=sec, primary=(sec == PRIMARY[tic]), test_of_record=(f"YES - primary sector of v2 ({os.path.basename(pred)})" if sec == PRIMARY[tic] else f"no - further test (primary is S{PRIMARY[tic]})"),
                   primary_rule=PRIMARY_RULE, product="QLP", flux_col="SAP_FLUX", pred_csv=pred, pred_sha256=h, ref_depth_ppm=dep, ref_dur_h=dur,
                   reference_source="PREREGISTRATION_v2.md reference-values line (frozen text)",
                   timing_rule="max(3 mean sigma_min, 30 min) (CLARIFICATION_TIMING_RULE_2026-10-20.md); min(3 sigma, 30 min) reading also reported",
                   evaluator="scripts/prereg_conformance.py (conformance-v2.1 rc4, general rules); frozen scripts/prereg_test.py literal outputs reported as secondary readouts",
                   evaluator_sha256=EV, clock_prior=f"results/qlp_clock_v2/{tic}.json", clock_prior_sha256=sha(f"{R}/results/qlp_clock_v2/{tic}.json"),
                   clock_note="qlp_clock_test_sector.py reads TIME/TIMECORR of a TESScut cutout of the test sector (run with --declared-test only when this test is run); no TESScut flux is used or scored",
                   frozen_evaluator_commands=[f"python -I scripts/prereg_test.py --lc <QLP S{sec} HLSP FITS> --flux-col {c} --pred {os.path.relpath(pred, R)} --depth-ppm {dep} --dur-h {dur} --sector {sec}" for c in ("SAP_FLUX", "DET_FLUX")],
                   release_of_record="v01", strict_epochs=None, object_specific_clauses=None,
                   edge_rule="drop 1.5 d after data start / resume (gap > 0.5 d) and 0.5 d before any gap > 0.1 d or data end (pooled rule; DECISIONS 76, 82, 86)",
                   data_status=f"future sector: not observed when the predictions were frozen ({eph['frozen']}) nor when this config was locked",
                   calibration="none object-specific; the conformance false-recovery calibration was made on the S106 objects only",
                   locked_utc=stamp)
        json.dump(cfg, open(p, "w"), indent=1); print("locked", p, dep, dur, "primary" if cfg["primary"] else "")
