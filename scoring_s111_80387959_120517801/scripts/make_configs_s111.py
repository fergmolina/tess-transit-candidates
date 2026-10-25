"""Lock the S111+ scoring configs of TIC 80387959 (S111-S114) and TIC 120517801 (S111-S113) for release v1.19 (DECISIONS 178(a), 192-197; v2
after review S111-1 to S111-5 and re-check R1-R5), before
any of their S111+ photometry exists or is examined. New file; the superseded GAP3 generator is not reused. Per sector, two configs:
  <TIC>_S<N>.json       product QLP SAP_FLUX, release v01, published evaluator scripts/prereg_conformance.py v2.1 rc4 with its clock gate
  <TIC>_S<N>_spoc.json  product SPOC PDCSAP_FLUX, scripts/prereg_conformance_spoc.py (conformance-v2.1-spoc1; reviewed in GAP3)
Exactly one of them is the product of record. The rule (DECISIONS 178(a) as refined in 193-194) is the DESIGNATION_RULE string below,
which every config carries:
  - a sector-lists-only designation from the first complete post-end snapshot;
  - the SPOC release-date rule with a two-check fallback certification that becomes final on QLP acquisition;
  - UNRESOLVED and UNAVAILABLE states;
  - all history kept in the hash-chained per-TIC/sector ledger of scripts/s111_ledger.py.
The other product is always a secondary readout. Primary sector S111; never replaced. Reference values: the generator rule (report.json
sap_depth; BLS duration_h, as no shape-fit T14 exists), applied identically to both products.
Two locks: LOCK_2026-10-25_S111_QLP.json (round-4 format; scripts/validate_round4_inputs.py, plus scripts/validate_s111_inputs.py
--stage route/result) and LOCK_2026-10-25_S111_SPOC.json (scripts/validate_s111_inputs.py). Refuses to overwrite anything."""
import os, re, csv, json, hashlib, datetime
R = "/Users/fernando/Desktop/NASA"; OUT = f"{R}/configs/conformance"
LQ, LS = f"{OUT}/LOCK_2026-10-25_S111_QLP.json", f"{OUT}/LOCK_2026-10-25_S111_SPOC.json"
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
for p in (LQ, LS):
    if os.path.exists(p): raise SystemExit(f"refused: {p} exists")
EV = sha(f"{R}/scripts/prereg_conformance.py"); assert EV == "a864b07ace8d3220a2d94a60513a488c8a5d87b54f41ebf510ff40ef1755311f"
EVS = sha(f"{R}/scripts/prereg_conformance_spoc.py"); assert EVS == "c7e1b4cd43bac06330a39f13e486b48a0041f251c1c88720bd3ac7d064a90b54", "SPOC variant differs from the GAP3-reviewed bytes"
SEL = sha(f"{R}/scripts/spoc_selection.py"); assert SEL == "600e9504a811ac14c10c8129324e9f5707c3103be85bd1d5961d47bafac4ac05"
DES = sha(f"{R}/scripts/target_list_designation.py"); QSEL = sha(f"{R}/scripts/qlp_selection.py"); LED = sha(f"{R}/scripts/s111_ledger.py")
now = datetime.datetime.now(datetime.UTC); stamp = now.strftime("%Y-%m-%d %H:%M:%S UTC"); iso = now.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
PRIMARY_RULE = ("The primary sector is the test of record. It stays the test of record whatever its result, including INSUFFICIENT, "
                "CLOCK_UNVERIFIED, INVALID_INPUT or UNAVAILABLE, and whichever product is designated; it is never replaced by a later sector. "
                "Later listed sectors are scored separately and reported as further tests, never pooled with the primary.")
DESIGNATION_RULE = ("Product of record (DECISIONS 178(a) as refined in 193-194, all before any S111 data):\n"
    "(1) Designation snapshot (scripts/target_list_designation.py v2, metadata only): the official orbit table and the sector's 2-min target "
    "lists all_targets_S<N>_v<k>.csv for k = 1..9 (bounded discovery: versions above 9 are not discovered), with the DDT page and lists "
    "saved as context only. The sector end is the latest 'End of Orbit' of the sector in the saved table, accepted only when the table "
    "also lists the next sector. Failed, malformed or incomplete fetches give PENDING, never 'unlisted'.\n"
    "(2) The FIRST complete (DESIGNATED) snapshot at or after the sector end is OPERATIVE. Its sector end and cutoffs are frozen; later "
    "snapshots are documented, not operative. If the TIC is in any valid saved sector list, SPOC; otherwise QLP.\n"
    "(3) SPOC designated:\n"
    "    - SPOC stays the product of record if any retained SPOC check finds a SPOC 2-min light curve whose MAST release date (t_obs_release, "
    "MJD) is <= end + 120 d. The first such selection is the release of record (irreversible).\n"
    "    - Otherwise QLP: the fallback is CERTIFIED by two complete SPOC checks at or after that cutoff, >= 7 days apart, with no qualifying "
    "release, and FINAL once QLP flux is acquired under it; a later qualifying SPOC release is then a secondary readout only.\n"
    "    - AMBIGUOUS or INCOMPLETE SPOC checks after the cutoff (including a SELECTED file without a usable release date) make the product "
    "of record UNRESOLVED, also after a certification, until a later qualifying selection or a new two-check certification; only a final "
    "fallback is immune.\n"
    "    - Checks recorded before the designation are evaluated, in ledger order, once the designation fixes the cutoffs.\n"
    "(4) QLP release of record: the first QLP check (scripts/qlp_selection.py) finding the v01 light curve with MAST release date <= end + 365 d. "
    "If a complete QLP check at or after end + 365 d finds none, the sector is UNAVAILABLE (final).\n"
    "(5) No flux of either product is acquired before the route is settled. Every snapshot, check, acquisition and disposition is an entry "
    "of the per-TIC/sector hash-chained ledger (scripts/s111_ledger.py); the validator replays it. The other product is always a secondary "
    "readout.")
MONITORING = (f"Prospective from this lock ({stamp}).\n"
    "- Designation: for each sector, from the time its end is published and has passed, a designation snapshot at least weekly until one is "
    "DESIGNATED. Every PENDING snapshot is kept in the ledger.\n"
    "- SPOC designated: SPOC checks (spoc_selection.py select) at least weekly until a qualifying SELECTED or a certified fallback.\n"
    "- QLP route: QLP checks (qlp_selection.py select) at least weekly until a qualifying SELECTED, or until a complete check at or after "
    "end + 365 d.\n"
    "- Nature: these are periodic recorded checks. A later check can recognize a timely release if it remains listed and its release date "
    "is usable. Missed checks or replaced products can change the evidence retained; earlier replaced deliveries cannot be excluded. The "
    "declared ledger finality rules still apply.")
DILUTION = ("The same reference depth is used for QLP SAP_FLUX and SPOC PDCSAP_FLUX. This is a fixed product-dependent comparison, not a host "
            "test: the two products differ in aperture and crowding treatment, and TIC 120517801's host is unresolved. The reference is never "
            "rescaled to rescue an outcome.")
lq, ls = {}, {}
for tic, ver in ((80387959, "v2"), (120517801, "v2")):
    d = f"{R}/results/vet_allsky/{tic}"; pred = f"{d}/predicted_transits_2026_2027_{ver}.csv"; txt = open(f"{d}/PREREGISTRATION_{ver}.md").read()
    eph = json.load(open(f"{d}/final_ephemeris_{ver}.json")); h = sha(pred); assert h == eph["sha256_csv"] and h in txt
    secs = sorted({int(m.group(1)) for r in csv.DictReader(open(pred)) if r["status"].startswith("prediction")
                   for m in [re.match(r"\s*(\d+)", r.get("tess_sector") or "")] if m and int(m.group(1)) >= 106})
    assert not re.search(r"Reference values for the outcome clauses", txt)
    rep = json.load(open(f"{d}/report.json")); dep = round(rep["sap_depth"]["depth_ppm"]); assert "T14_h" not in rep.get("shape_mcmc", {})
    dur = rep["bls_refine"]["duration_h"]
    src = (f"dated amendment 2026-10-25 (generator rule, TIC 120444365 / 70441745 precedent): report.json sap_depth; BLS duration_h (no shape-fit "
           f"T14_h); PREREGISTRATION_{ver}.md predates the reference-values line")
    prior = f"results/qlp_clock_v2/{tic}.json"; assert os.path.exists(f"{R}/{prior}")
    for sec in secs:
        primary = sec == secs[0]
        common = dict(tic=tic, sector=sec, primary=primary, test_of_record=(f"YES - primary sector of {ver}" if primary else f"no - further test (primary is S{secs[0]})"),
                      primary_rule=PRIMARY_RULE, designation_rule=DESIGNATION_RULE, monitoring_rule=MONITORING, dilution_note=DILUTION,
                      pred_csv=pred, pred_sha256=h, ref_depth_ppm=round(float(dep), 1), ref_dur_h=round(float(dur), 3), reference_source=src,
                      timing_rule="max(3 mean sigma_min, 30 min) (CLARIFICATION_TIMING_RULE_2026-10-20.md); min(3 sigma, 30 min) reading also reported",
                      edge_rule="drop 1.5 d after data start / resume (gap > 0.5 d) and 0.5 d before any gap > 0.1 d or data end (pooled rule; DECISIONS 76, 82, 86)",
                      strict_epochs=None, object_specific_clauses=None, designation_tool_sha256=DES, selection_tool_sha256=SEL, qlp_selection_tool_sha256=QSEL, ledger_tool_sha256=LED,
                      data_status=f"future sector: not observed at the freeze ({eph['frozen']}) nor at this lock; its 2-min target list was not yet published",
                      calibration="none object-specific; the conformance false-recovery calibration was made on the S106 objects only", locked_utc=stamp)
        q = dict(common, product="QLP", flux_col="SAP_FLUX", release_of_record="v01",
                 release_rule=("the v01 light curve selected by the first qualifying QLP check (scripts/qlp_selection.py; MAST release date <= end + 365 d), acquired as the ledger's "
                               "record acquisition. Only v01 is a release of record: a sector where MAST lists only a reprocessed version (e.g. v02) reaches UNAVAILABLE although a QLP "
                               "product exists (as for the v1.17 locks)"),
                 binding="BOTH required: scripts/validate_s111_inputs.py --stage route/result (ledger) AND scripts/validate_round4_inputs.py --stage pre/clock/result, for the same config and light curve",
                 evaluator="scripts/prereg_conformance.py (conformance-v2.1 rc4, general rules)",
                 evaluator_sha256=EV, clock_prior=prior, clock_prior_sha256=sha(f"{R}/{prior}"),
                 clock_note="qlp_clock_test_sector.py reads TIME/TIMECORR of a TESScut cutout of the test sector (only with --declared-test); no TESScut flux is used or scored")
        s_ = dict(common, product="SPOC", flux_col="PDCSAP_FLUX", release_of_record=None,
                  release_rule=("the first qualifying SPOC selection in the ledger (scripts/spoc_selection.py; exactly one SPOC 2-min s_lc.fits, MAST release date <= end + 120 d); "
                                "an earlier replaced delivery cannot be excluded; acquired as the ledger's record acquisition"),
                  binding="scripts/validate_s111_inputs.py --stage pre/route/result (ledger replay)",
                  evaluator="scripts/prereg_conformance_spoc.py (conformance-v2.1-spoc1: v2.1 rc4 + SPOC product branch, no QLP clock gate)", evaluator_sha256=EVS)
        pq, ps = f"{OUT}/{tic}_S{sec}.json", f"{OUT}/{tic}_S{sec}_spoc.json"
        for p in (pq, ps):
            if os.path.exists(p): raise SystemExit(f"refused: {p} exists")
        json.dump(q, open(pq, "w"), indent=1); json.dump(s_, open(ps, "w"), indent=1)
        code = dict(target_list_designation_code_sha256=DES, spoc_selection_code_sha256=SEL, qlp_selection_code_sha256=QSEL, s111_ledger_code_sha256=LED)
        lq[os.path.basename(pq)] = dict(config_sha256=sha(pq), tic=tic, sector=sec, primary=primary, pred_sha256=h, clock_prior=prior,
                                        clock_prior_sha256=q["clock_prior_sha256"], product="QLP", **code)
        ls[os.path.basename(ps)] = dict(config_sha256=sha(ps), tic=tic, sector=sec, primary=primary, pred_sha256=h, product="SPOC",
                                        scoring_code="prereg_conformance_spoc", prereg_conformance_spoc_code_sha256=EVS, **code)
        print("locked", os.path.basename(pq), "+", os.path.basename(ps), dep, dur, "PRIMARY" if primary else "")
json.dump(dict(made_utc=stamp, made_utc_iso=iso, note="S111+ QLP lock (80387959, 120517801): round-4 format for scripts/validate_round4_inputs.py --lock; designation via scripts/validate_s111_inputs.py.",
               evaluator_sha256=EV, configs=lq), open(LQ, "w"), indent=1)
json.dump(dict(made_utc=stamp, made_utc_iso=iso, note="S111+ SPOC lock (80387959, 120517801); use scripts/validate_s111_inputs.py --lock this file.", configs=ls), open(LS, "w"), indent=1)
print(len(lq), "QLP +", len(ls), "SPOC configs; locks", sha(LQ)[:16], sha(LS)[:16])
