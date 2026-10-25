"""Append the dated v1.19 scoring amendment to the TIC 80387959 and TIC 120517801 registrations (DECISIONS 192-195; v2 after review). Refuses unless each local
registration is byte-identical to its copy in the published release (git HEAD of public_release/), and runs once."""
import json, hashlib, subprocess
R = "/Users/fernando/Desktop/NASA"; C = f"{R}/configs/conformance"; sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
LQ, LS = f"{C}/LOCK_2026-10-25_S111_QLP.json", f"{C}/LOCK_2026-10-25_S111_SPOC.json"; lq, ls = json.load(open(LQ)), json.load(open(LS))
for tic in (80387959, 120517801):
    reg = f"{R}/results/vet_allsky/{tic}/PREREGISTRATION_v2.md"
    pub = subprocess.run(["git", "-C", f"{R}/public_release", "show", f"HEAD:preregistration/TIC{tic}/PREREGISTRATION_v2.md"], capture_output=True, check=True).stdout
    cur = open(reg, "rb").read()
    if b"Dated scoring amendment 2026-10-25" in cur: raise SystemExit(f"refused: {tic} already amended")
    if cur != pub: raise SystemExit(f"refused: {tic} local registration differs from the published copy")
    qs = sorted((v["sector"], k, v) for k, v in lq["configs"].items() if v["tic"] == tic); cfg = json.load(open(f"{C}/{qs[0][1]}"))
    items = "; ".join(f"S{sec}: {k} (SHA-256 {v['config_sha256'][:16]}...) and {k[:-5]}_spoc.json (SHA-256 {ls['configs'][k[:-5] + '_spoc.json']['config_sha256'][:16]}...)"
                      + (" PRIMARY - test of record" if v["primary"] else "") for sec, k, v in qs)
    txt = (f"\n**Dated scoring amendment 2026-10-25 (before any S111+ photometry of this star exists or is examined).** Each listed TESS sector is "
           f"scored separately, with two configs per sector locked on {cfg['locked_utc']}. Exactly one product is the product of record. "
           + cfg["designation_rule"].replace("\n", " ") + " "
           f"QLP config: the published evaluator scripts/prereg_conformance.py v2.1 rc4 (SHA-256 {lq['evaluator_sha256']}), QLP SAP_FLUX release v01 (only v01 is a release of record; a "
           f"v02-only listing leads to UNAVAILABLE), with the clock gate and the "
           f"c0 prior results/qlp_clock_v2/{tic}.json (SHA-256 {cfg['clock_prior_sha256'][:16]}...). SPOC config: scripts/prereg_conformance_spoc.py (conformance-v2.1-spoc1, "
           f"SHA-256 {ls['configs'][qs[0][1][:-5] + '_spoc.json']['prereg_conformance_spoc_code_sha256']}), i.e. the v2.1 rc4 rules with a SPOC product branch and no QLP clock "
           f"gate, since SPOC times are target-barycentric; its release of record is the eligible version listed at the first recorded check "
           f"(scripts/spoc_selection.py), and an earlier replaced delivery cannot be excluded. Configs: {items}. Locks: "
           f"configs/conformance/LOCK_2026-10-25_S111_QLP.json (SHA-256 {sha(LQ)[:16]}...) and LOCK_2026-10-25_S111_SPOC.json (SHA-256 {sha(LS)[:16]}...). "
           f"Binding: every designation snapshot, product check, acquisition and disposition is an entry of the per-TIC/sector hash-chained ledger "
           f"(scripts/s111_ledger.py, SHA-256 {ls['configs'][qs[0][1][:-5] + '_spoc.json']['s111_ledger_code_sha256'][:16]}...), and scripts/validate_s111_inputs.py replays it at "
           f"its pre, route and result stages. For QLP, the published scripts/validate_round4_inputs.py must ALSO bind its pre, clock and result "
           f"stages for the same config and light curve. Monitoring: " + cfg["monitoring_rule"].replace("\n", " ") + " "
           f"Primary-sector rule: {cfg['primary_rule']} Reference values: depth {cfg['ref_depth_ppm']} ppm, T14 {cfg['ref_dur_h']} h ({cfg['reference_source']}). "
           f"{cfg['dilution_note']} Timing: {cfg['timing_rule']}. The frozen scripts/prereg_test.py literal outputs are secondary readouts. "
           f"No prediction, ephemeris or checksum is changed. DECISIONS 172, 178, 192-198.\n")
    open(reg, "wb").write(cur.rstrip(b"\n") + b"\n" + txt.encode()); print("amended", tic)
