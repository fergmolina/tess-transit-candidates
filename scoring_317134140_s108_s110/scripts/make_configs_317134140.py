"""Lock the TIC 317134140 S108-S110 scoring configs (dedicated scorer v1.3; DECISIONS 172-179), before any S108-S110 photometry of this star
is examined. Replaces the 317134140 part of scripts/make_conformance_configs_gap3.py (its unpublished outputs are archived as superseded).
Output: configs/conformance/317134140_spoc_S<sector>.json and configs/conformance/LOCK_2026-10-24_317134140.json (for
scripts/validate_nonclock_inputs.py --lock). Sector end dates come from catalogs/TESS_orbit_times.csv. Refuses to overwrite anything."""
import os, csv, json, hashlib, datetime
R = "/Users/fernando/Desktop/NASA"; OUT = f"{R}/configs/conformance"; LOCK = f"{OUT}/LOCK_2026-10-24_317134140.json"
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
if os.path.exists(LOCK): raise SystemExit(f"refused: {LOCK} exists")
SC, TS, SP = (sha(f"{R}/scripts/{k}.py") for k in ("prereg_spoc_317134140", "tsearch", "search_pipeline"))
VAL, SEL = sha(f"{R}/scripts/validate_nonclock_inputs.py"), sha(f"{R}/scripts/spoc_selection.py")
pred = f"{R}/results/vet/317134140/predicted_transits_S108_S109_S110.csv"; h = sha(pred)
assert h.startswith("63e98fc87ebc6ce6") and h in open(f"{R}/results/vet/317134140/PREREGISTRATION.md").read()
ends = {}
for r in csv.DictReader(open(f"{R}/catalogs/TESS_orbit_times.csv")):
    if not str(r["Sector"]).strip().isdigit(): continue      # comment rows
    ends[int(r["Sector"])] = max(ends.get(int(r["Sector"]), ""), r["End of Orbit"])
now = datetime.datetime.now(datetime.UTC); stamp = now.strftime("%Y-%m-%d %H:%M:%S UTC"); iso = now.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
STATUS = {108: "observed 2026-09-07 to 10-05; the authors attest that no S108 photometry of this star has been examined",
          109: "being observed 2026-10-05 to 10-31", 110: "future sector (2026-10-31 to 11-26)"}
lock = {}
for sec in (108, 109, 110):
    p = f"{OUT}/317134140_spoc_S{sec}.json"
    if os.path.exists(p): raise SystemExit(f"refused: {p} exists")
    end = datetime.datetime.strptime(ends[sec], "%Y-%m-%d %H:%M:%S"); cutoff = (end + datetime.timedelta(days=120)).strftime("%Y-%m-%dT%H:%M:%SZ")
    cfg = dict(tic=317134140, sector=sec, product="SPOC", flux_col="PDCSAP_FLUX", pred_csv=pred, pred_sha256=h,
               scorer="scripts/prereg_spoc_317134140.py (dedicated scorer v1.3; full definitions in its docstring)", scorer_sha256=SC,
               tsearch_sha256=TS, search_pipeline_sha256=SP,
               status_of_procedure="dated operationalization (2026-10-24) of the qualitative frozen test; the operational numbers below are post-freeze choices declared before any test-sector data",
               frozen_test="stacked depth at predicted phase in each of S108/S109/S110 should be ~185 +- 40 ppm; blind BLS of each sector should rank 0.5719 d near the top",
               events="every row of the prediction CSV for this sector is a candidate event; the in_science_orbit column is not used; eligibility is decided only by data coverage after preprocessing",
               clause_a=("compatibility with the frozen depth plus positive-depth evidence: A_LOW if depth + 1.96 sigma < 145 ppm; A_HIGH if depth - 1.96 sigma > 225; "
                         "A_CONSISTENT if depth +- 1.96 sigma overlaps [145, 225] and depth/sigma >= 2; else A_INCONCLUSIVE. INSUFFICIENT if < 10 eligible events, "
                         "< 100 usable random shifts, or sigma is nonfinite or <= 0. 1.96 is nominal: the random-phase sigma is an empirical spread with no established 95 % coverage"),
               clause_b="B_TOP3: one of the top 3 distinct peaks (> 1 % apart) of the original per-sector search within 0.1 % of 0.5718634 d; aliases reported, not counted; not run if clause A is INSUFFICIENT",
               sector_outcome=("ORDERED, first rule that applies: (1) INSUFFICIENT if clause A is INSUFFICIENT; (2) FAIL if A_LOW, whatever clause B says; "
                               "(3) PASS if A_CONSISTENT and B_TOP3; (4) PARTIAL if exactly one of A_CONSISTENT / B_TOP3 (includes A_HIGH + B_TOP3); (5) INCONCLUSIVE otherwise. "
                               "Only PASS meets both frozen clauses; PARTIAL and INCONCLUSIVE are not confirmations; FAIL is adverse evidence under this measurement model, not proof of absence"),
               scope="each of S108, S109, S110 scored and reported separately; no pooling; no replacement",
               secondary_readout="pooled S108-S110 depth = inverse-variance weighted mean of the per-sector clause-A depths, nominal 1.96-sigma interval vs [145, 225] ppm; never the outcome",
               preprocessing=("registration prep() (public scripts/blind_seasons_317134140.py:12) with three stated differences: no candidate mask in detrending (blind search), "
                              "PDCSAP_FLUX_ERR errors instead of a constant point-to-point error, clipping MAD over all retained points"),
               toi_mask="TOI-2514.01 (P 6.3951381 d, T0 BTJD 2215.084143, 4.047 h) removed BEFORE detrending with wotan.transit_mask, full window 1.5 x 4.047 h",
               release_of_record=("the eligible version listed at the FIRST RECORDED CHECK; an earlier, replaced delivery cannot be excluded (MAST lists the current version only). "
                                  "A metadata-only selection record (scripts/spoc_selection.py select) is made at the first check after a SPOC 2-min s_lc.fits of this TIC and "
                                  "sector is listed; exactly one candidate is required (else NONE, AMBIGUOUS or INCOMPLETE, kept and reported, nothing chosen). The "
                                  "selected dataURI is then downloaded (spoc_selection.py acquire), and validate_nonclock_inputs.py re-derives the selection from the saved "
                                  "rows and binds selection, acquisition, light curve and output"),
               selection_tool_sha256=SEL, validator_sha256=VAL,
               sector_end_utc=ends[sec], unavailable_cutoff_utc=cutoff,
               no_product_rule=(f"cutoff {cutoff} (sector end {ends[sec]} UTC + 120 days; inclusive). If a SELECTED selection record is made at or before the cutoff, the "
                                f"product may be acquired and scored at any later time. If no SELECTED record exists by the cutoff, the sector is UNAVAILABLE; no other "
                                f"product replaces it, and a later listing or delivery is a secondary readout only. UNAVAILABLE means that no SELECTED record was made by the cutoff, "
                                f"not that no archive product ever existed"),
               monitoring_rule=(f"Starting at the later of this lock's effective time ({stamp}) and the sector end ({ends[sec]} UTC), a metadata-only check "
                                f"(scripts/spoc_selection.py select) is performed and retained at least weekly until the first SELECTED record. If none exists, a final "
                                f"check is made within the 24 hours before the inclusive cutoff. Every check is retained, including NONE, AMBIGUOUS and INCOMPLETE, and the "
                                f"first eligible selected release is never replaced by a later one. This is periodic, not continuous, monitoring: a delivery between the "
                                f"final check and the cutoff could be missed." + (f" This sector ended before the obligation took effect. No selection record for it was "
                                f"made before this lock, and the schedule is not claimed to have been followed before {stamp}." if ends[sec] < stamp[:19] else "")),
               advance_expectation="training sectors S6/S87/S98/S107: 1 PASS, 2 PARTIAL, 1 INCONCLUSIVE; mostly PARTIAL expected under a real signal (a conditional extrapolation, not a calibrated probability)",
               data_status=STATUS[sec], locked_utc=stamp)
    json.dump(cfg, open(p, "w"), indent=1)
    lock[os.path.basename(p)] = dict(config_sha256=sha(p), tic=317134140, sector=sec, primary=None, pred_sha256=h, scoring_code="prereg_spoc_317134140",
                                     prereg_spoc_317134140_code_sha256=SC, tsearch_code_sha256=TS, search_pipeline_code_sha256=SP, spoc_selection_code_sha256=SEL)
    print("locked", os.path.basename(p), "cutoff", cutoff)
json.dump(dict(made_utc=stamp, made_utc_iso=iso, note="TIC 317134140 S108-S110 lock (scorer v1.3); use scripts/validate_nonclock_inputs.py --lock this file.",
               configs=lock), open(LOCK, "w"), indent=1)
print("lock", sha(LOCK)[:16])
