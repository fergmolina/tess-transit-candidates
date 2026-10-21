"""Refusal/config/binding tests for the round-4 conformance configs (2026-10-21; review F2, re-check R3). Uses NO test-sector data: only
in-sample QLP files of the same stars (sectors <= 105), copies of configs/priors and synthetic clock/evaluator records in a FRESH directory.
Every case has its own output path, the expected exit status is required, and evaluator outputs must carry the config and light-curve
SHA-256 of the case that produced them (stale or crashed outputs cannot pass).
Per config: (1) prediction hash / evaluator SHA / reference values = frozen line; (2) clock tool refuses the test sector without
--declared-test (exit 2, no output); (3)-(5) evaluator gives INVALID_INPUT for an in-sample file, a corrupted prediction hash and a changed
evaluator SHA; (6) validate_round4_inputs.py --stage pre binds the real config and refuses: a config with a changed prior hash, a prior path
other than the canonical one, altered prior bytes; (7) --stage clock refuses a clock record made from another config, from another prior,
for another sector; accepts a synthetic record bound to the config; (8) --stage result requires the output to name the same clock file (refuses one scored with another clock file of identical identity
fields but other corrections), refuses missing/malformed hashes, another evaluator or config, and a science outcome without clock
provenance, and labels a pre-clock INVALID_INPUT as PRE-CLOCK; (9) --stage clock refuses a record without a light-curve hash.
Usage: python -I test_round4_configs.py TMPDIR   (TMPDIR must not exist)"""
import sys, os, glob, json, re, hashlib, subprocess, shutil
R = "/Users/fernando/Desktop/NASA"; PY = f"{R}/.venv/bin/python"; TMP = sys.argv[1]; VAL = f"{R}/scripts/validate_round4_inputs.py"
if os.path.exists(TMP): raise SystemExit(f"refused: {TMP} exists (fresh directory required)")
os.makedirs(TMP); sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest(); fails = []; n = 0
def check(cond, msg):
    global n; n += 1
    if not cond: fails.append(msg)
    print(("PASS " if cond else "FAIL ") + msg)
def run(args): r = subprocess.run([PY, "-I"] + args, capture_output=True, text=True); return r.returncode, r.stdout + r.stderr
def ev(cfgpath, lc, out):
    assert not os.path.exists(out); rc, txt = run([f"{R}/scripts/prereg_conformance.py", "--config", cfgpath, "--lc", lc, "--out", out])
    if rc != 0 or not os.path.exists(out): return f"CRASH rc={rc} {txt[-150:]}"
    e = json.load(open(out))
    if e.get("config_sha256") != sha(cfgpath) or e.get("lc_sha256") != sha(lc): return "STALE/MISMATCHED OUTPUT"
    return e["outcome"]
for cp in sorted(glob.glob(f"{R}/configs/conformance/*_S11[2-9].json")):
    c = json.load(open(cp)); tic, sec = c["tic"], c["sector"]; tag = f"{tic}_S{sec}"; D = f"{TMP}/{tag}"; os.makedirs(D)
    check(sha(c["pred_csv"]) == c["pred_sha256"], f"{tag} prediction hash")
    check(sha(f"{R}/scripts/prereg_conformance.py") == c["evaluator_sha256"], f"{tag} evaluator SHA")
    m = re.search(r"Reference values for the outcome clauses: depth (\d+) ppm \([^)]*\), T14 ([\d.]+) h", open(f"{R}/results/vet_allsky/{tic}/PREREGISTRATION_v2.md").read())
    check((float(m.group(1)), float(m.group(2))) == (c["ref_depth_ppm"], c["ref_dur_h"]), f"{tag} reference values = frozen line")
    insample = sorted(glob.glob(f"{R}/data/qlp_allsky/hlsp_qlp_tess_ffi_s0*-{tic:016d}_tess_v01_llc.fits"))[-1]; assert int(re.search(r"_s0*(\d+)-", insample).group(1)) <= 105
    rc, txt = run([f"{R}/scripts/qlp_clock_test_sector.py", "--config", cp, "--qlp", insample, "--out", f"{D}/clock.json"])
    check(rc == 2 and "declared-test" in txt and not os.path.exists(f"{D}/clock.json"), f"{tag} clock tool refuses test sector without --declared-test")
    o = ev(cp, insample, f"{D}/wrongfile.json"); check(o.startswith("INVALID_INPUT"), f"{tag} in-sample file refused: {o[:80]}")
    for k, v in (("pred_sha256", "0" * 64), ("evaluator_sha256", "f" * 64)):
        c2 = dict(c); c2[k] = v; p2 = f"{D}/cfg_{k}.json"; json.dump(c2, open(p2, "w"))
        o = ev(p2, insample, f"{D}/out_{k}.json"); check(o.startswith("INVALID_INPUT"), f"{tag} corrupted {k} refused: {o[:80]}")
    rc, txt = run([VAL, "--stage", "pre", "--config", cp]); check(rc == 0 and "BOUND" in txt, f"{tag} validator binds the locked config")
    for k, v in (("clock_prior_sha256", "0" * 64), ("clock_prior", f"results/qlp_clock_v2/other/{tic}.json")):
        c2 = dict(c); c2[k] = v; p2 = f"{D}/cfg_{k}.json"; json.dump(c2, open(p2, "w"))
        rc, txt = run([VAL, "--stage", "pre", "--config", p2]); check(rc == 2 and "REFUSED" in txt, f"{tag} validator refuses changed {k}")
    alt = f"{D}/altroot/results/qlp_clock_v2"; os.makedirs(alt); b = open(f"{R}/{c['clock_prior']}", "rb").read(); open(f"{alt}/{tic}.json", "wb").write(b.replace(b"c0_min", b"c0_mim"))
    rc, txt = run([VAL, "--stage", "pre", "--config", cp, "--prior-root", f"{D}/altroot"]); check(rc == 2 and "bytes differ" in txt, f"{tag} validator refuses altered prior bytes")
    good = dict(tic=tic, sector=sec, config_sha256=sha(cp), c0_prior_file=f"{R}/{c['clock_prior']}", c0_prior_sha256=c["clock_prior_sha256"], pred_sha256=c["pred_sha256"], qlp_sha256="a" * 64)
    for name, rec, want in (("bound", good, 0), ("other config", dict(good, config_sha256="1" * 64), 2), ("other prior", dict(good, c0_prior_sha256="2" * 64), 2),
                            ("other sector", dict(good, sector=sec + 1), 2), ("other prior path", dict(good, c0_prior_file="/tmp/x.json"), 2)):
        kp = f"{D}/clock_{name.replace(' ', '_')}.json"; json.dump(rec, open(kp, "w")); rc, txt = run([VAL, "--stage", "clock", "--config", cp, "--clock", kp])
        check(rc == want, f"{tag} clock-stage {name}: exit {rc} (want {want})")
    # result stage (re-check 2): the scored output must name the SAME clock file; hashes must exist; pre-clock outcomes are labelled
    kp = f"{D}/clock_bound.json"; kp2 = f"{D}/clock_bound_other_corrections.json"
    json.dump(dict(good, event_btjd=[1.0], correction_min=[0.1]), open(kp, "w")); json.dump(dict(good, event_btjd=[1.0], correction_min=[99.9]), open(kp2, "w"))
    base = dict(config_sha256=sha(cp), script_sha256=c["evaluator_sha256"], lc_sha256="a" * 64, outcome="RECOVERED", clock_record=dict(path=kp, sha256=sha(kp)))
    cases = [("bound scored output", base, kp, 0, "BOUND: stage result"),
             ("output scored with another clock file (same identity, other corrections)", dict(base, clock_record=dict(path=kp2, sha256=sha(kp2))), kp, 2, "different clock record"),
             ("science outcome without clock provenance", {k: v for k, v in base.items() if k != "clock_record"}, kp, 2, "no clock provenance"),
             ("pre-clock INVALID_INPUT without clock provenance", dict({k: v for k, v in base.items() if k != "clock_record"}, outcome="INVALID_INPUT (x)"), kp, 0, "PRE-CLOCK"),
             ("missing lc_sha256", {k: v for k, v in base.items() if k != "lc_sha256"}, kp, 2, "lc_sha256 is missing"),
             ("malformed clock_record hash", dict(base, clock_record=dict(path=kp, sha256="xyz")), kp, 2, "different clock record"),
             ("other evaluator", dict(base, script_sha256="4" * 64), kp, 2, "different evaluator"),
             ("other config", dict(base, config_sha256="3" * 64), kp, 2, "different config")]
    for name, e, kk, want, needle in cases:
        ep = f"{D}/eval_{re.sub(r'[^a-z0-9]+', '_', name)}.json"; json.dump(e, open(ep, "w")); rc, txt = run([VAL, "--stage", "result", "--config", cp, "--clock", kk, "--result", ep])
        check(rc == want and needle in txt, f"{tag} result-stage {name}: exit {rc} (want {want})")
    nolc = {k: v for k, v in good.items() if k != "qlp_sha256"}; kp3 = f"{D}/clock_no_qlp_hash.json"; json.dump(nolc, open(kp3, "w"))
    rc, txt = run([VAL, "--stage", "clock", "--config", cp, "--clock", kp3]); check(rc == 2 and "qlp_sha256 is missing" in txt, f"{tag} clock-stage refuses a record without a light-curve hash")
print(f"{n - len(fails)}/{n} passed"); sys.exit(1 if fails else 0)
