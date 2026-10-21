"""Binding checks for the round-4 conformance tests (2026-10-21; re-check R3). The pinned evaluator and qlp_clock_test_sector.py are not
changed (the seven S106 tests keep their published code); this separately versioned step must pass at each stage, otherwise the test is
not run / not scored, and the refusal is reported for that sector (it stays the test of record if it is the primary).
  --stage pre    --config C            before ANY test-sector data access: C's SHA-256 is in configs/conformance/ROUND4_LOCK.json; its
                                       prediction CSV, evaluator and c0 prior hash match the lock; its clock_prior is the canonical
                                       results/qlp_clock_v2/<TIC>.json that qlp_clock_test_sector.py actually reads, with the locked bytes.
  --stage clock  --config C --clock K  after the clock tool, before scoring: K was made from exactly C (config_sha256), from the locked c0
                                       prior (path and SHA-256), for the same TIC, sector and prediction CSV.
  --stage result --config C --clock K --result E   after the evaluator: E was made from exactly C, by the locked evaluator, from the
                                       light curve K was made from, and was scored with the SAME clock record K (its clock_record.sha256).
                                       An output without clock provenance is accepted only as a PRE-CLOCK outcome (INVALID_INPUT,
                                       INSUFFICIENT, CLOCK_UNVERIFIED). All hashes must be present and well-formed (fail closed).
Exit 0 = bound; exit 2 = refused (reason printed). Usage: python -I validate_round4_inputs.py --stage S --config C [--clock K] [--result E]"""
import sys, os, json, hashlib, argparse
R = "/Users/fernando/Desktop/NASA"; sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
ap = argparse.ArgumentParser(); ap.add_argument("--stage", required=True, choices=["pre", "clock", "result"]); ap.add_argument("--config", required=True)
ap.add_argument("--clock"); ap.add_argument("--result"); ap.add_argument("--lock", default=f"{R}/configs/conformance/ROUND4_LOCK.json"); ap.add_argument("--prior-root", default=R, help="tests only: root of the canonical prior path"); a = ap.parse_args(); PR = a.prior_root
def refuse(m): print("REFUSED:", m); sys.exit(2)
import re as _re
HEX = lambda v: isinstance(v, str) and _re.fullmatch(r"[0-9a-f]{64}", v) is not None   # well-formed SHA-256 (re-check 2: fail closed on missing hashes)
lock = json.load(open(a.lock)); cs = sha(a.config); L = next((v for v in lock["configs"].values() if v["config_sha256"] == cs), None)
if L is None: refuse(f"config SHA-256 {cs[:16]} is not in the lock manifest")
c = json.load(open(a.config)); canon = f"results/qlp_clock_v2/{c['tic']}.json"
for k in ("tic", "sector", "pred_sha256", "clock_prior", "clock_prior_sha256"):
    if c.get(k) != L[k]: refuse(f"config {k} differs from the lock")
if c["clock_prior"] != canon: refuse(f"config clock_prior {c['clock_prior']} is not the canonical {canon} read by qlp_clock_test_sector.py")
if not os.path.exists(f"{PR}/{canon}") or sha(f"{PR}/{canon}") != L["clock_prior_sha256"]: refuse(f"c0 prior {canon} is missing or its bytes differ from the lock")
if sha(c["pred_csv"]) != L["pred_sha256"]: refuse("prediction CSV bytes differ from the lock")
if sha(f"{R}/scripts/prereg_conformance.py") != lock["evaluator_sha256"] or c["evaluator_sha256"] != lock["evaluator_sha256"]: refuse("evaluator SHA-256 differs from the lock")
if a.stage in ("clock", "result"):
    if not a.clock: refuse("--clock is required at this stage")
    k = json.load(open(a.clock))
    for f, want in (("config_sha256", cs), ("c0_prior_sha256", L["clock_prior_sha256"]), ("tic", c["tic"]), ("sector", c["sector"]), ("pred_sha256", c["pred_sha256"])):
        if k.get(f) != want: refuse(f"clock record {f} = {str(k.get(f))[:20]} != {str(want)[:20]}")
    if os.path.abspath(k.get("c0_prior_file", "")) != os.path.abspath(f"{R}/{canon}"): refuse("clock record c0_prior_file is not the locked prior")
    for f in ("config_sha256", "c0_prior_sha256", "pred_sha256", "qlp_sha256"):
        if not HEX(k.get(f)): refuse(f"clock record {f} is missing or not a SHA-256")
if a.stage == "result":
    if not a.result: refuse("--result is required at this stage")
    e = json.load(open(a.result))
    for f in ("config_sha256", "script_sha256", "lc_sha256"):
        if not HEX(e.get(f)): refuse(f"evaluator output {f} is missing or not a SHA-256")
    if e.get("config_sha256") != cs: refuse("evaluator output was made from a different config")
    if e.get("script_sha256") != lock["evaluator_sha256"]: refuse("evaluator output was made by a different evaluator")
    if e.get("lc_sha256") != k.get("qlp_sha256"): refuse("evaluator light curve differs from the one the clock record was made from")
    cr = e.get("clock_record")
    if cr is None:
        # the evaluator returns before its clock gate only with INVALID_INPUT, INSUFFICIENT (no usable data) or CLOCK_UNVERIFIED;
        # such an output is certified as a PRE-CLOCK outcome, never as clock-dependent scoring
        if not str(e.get("outcome", "")).startswith(("INVALID_INPUT", "INSUFFICIENT", "CLOCK_UNVERIFIED")): refuse(f"outcome {str(e.get('outcome'))[:40]} has no clock provenance")
        print(f"BOUND (PRE-CLOCK outcome, no clock correction applied): {e['outcome'][:80]}; {os.path.basename(a.config)}"); sys.exit(0)
    if not HEX(cr.get("sha256")) or cr.get("sha256") != sha(a.clock): refuse("evaluator output was scored with a different clock record (clock_record.sha256 != SHA-256 of --clock)")
print(f"BOUND: stage {a.stage}, {os.path.basename(a.config)} (lock {cs[:16]})")
