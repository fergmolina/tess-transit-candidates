# Pre-registered transit predictions v2 - TIC 151767028
Frozen: 2026-10-21 01:57:12 UTC. Author: Fernando Molina (Independent researcher, ORCID 0009-0002-2872-3406). Analysis with Claude (Anthropic) under the author's direction.
First freeze for this object (v2 tooling: all-sector ephemeris). Reason (external review 2026-10-18,
results/external_review_allsky/REVIEW.md): v1 timed only the 200-s sectors (vet.py min_pts cut), ignoring 2018-2021 data; v2 fits one time offset per
sector from ALL sectors (raw SAP flux, cadence-aware model, local baselines; SPOC 2-min sectors where they exist) on top of the all-data BLS ephemeris.
Ephemeris: T0 = BTJD 4056.10895 +- 6.6 min (epoch 1123), P = 2.210401 +- 0.000012 d (chi2/dof 13.4/2, inflation x2.59); all-data BLS P = 2.210392.
Sector times used: S36 QLP SAP (8 ev, O-C -0.9 +- 4.2 min), S63 QLP SAP (12 ev, O-C -6.8 +- 6.6 min), S90 QLP SAP (12 ev, O-C +7.8 +- 3.0 min), S99 QLP SAP (6 ev, O-C -8.5 +- 3.6 min).
Depth per sector (fixed shape, local baseline, raw SAP): S36 763, S63 546, S90 542, S99 662 ppm.
Round 4 of the all-sky search (DECISIONS 113-117): on-target in the FFI pixel test, vet.py v1.13, triage WEAK (SNR 8.1), TRICERATOPS FPP 0.11 / NFPP 0.043 (single run, no contrast curve; screening, not validation). Independent rediscovery: a signal at this period is listed in eumemic/exoplanets and ahrazzle/exoplanets (results_public/followup_kmdwarfs.csv, checked 2026-10-20); we claim no priority. S100 sector time rejected by the generator (weak). Scoring statement (fixed at this freeze, before any test-sector photometry of this star is examined): each listed TESS sector will be scored separately, in sector order, with the published conformance evaluator scripts/prereg_conformance.py v2.1 rc4 (SHA-256 a864b07ace8d3220a2d94a60513a488c8a5d87b54f41ebf510ff40ef1755311f; conformance_v2.1/CONFORMANCE_PROCEDURE_v2.1.md), using its general rules (the object-specific clauses written for the S106 objects do not apply) and a per-object config locked before that sector is examined: QLP SAP_FLUX, release of record v01, the QLP clock gate, and the reference depth and T14 stated below. The first listed sector with a released QLP v01 light curve is the test of record; later sectors are reported as further tests. Where the generic outcome clause below differs, the conformance procedure governs. Its false-recovery calibration was made on the S106 objects; no object-specific calibration has been made for this star. No TESScut or other ad hoc extraction will be used.

Reference values for the outcome clauses: depth 540 ppm (raw SAP, all sectors), T14 1.00 h.
SHA-256 of predicted_transits_2026_2027_v2.csv: befcc2e8d522cd252657a5cd4a09df1d6dd6d94b773e3e9b9f6bcd6fca9ba8a5
**Test of record: next TESS sector(s).** Predicted mid-transits (sigma_min = 1-sigma timing uncertainty at that epoch):
 epoch    tc_bjd_tdb              utc  sigma_min                  tess_sector     status
  1277 2461396.51076 2026-12-22 00:15    8.50000 112 (span only, gap unknown) prediction
  1278 2461398.72116 2026-12-24 05:17    8.60000 112 (span only, gap unknown) prediction
  1279 2461400.93156 2026-12-26 10:20    8.60000 112 (span only, gap unknown) prediction
  1280 2461403.14197 2026-12-28 15:23    8.60000 112 (span only, gap unknown) prediction
  1281 2461405.35237 2026-12-30 20:26    8.60000 112 (span only, gap unknown) prediction
  1282 2461407.56277 2027-01-02 01:28    8.60000 112 (span only, gap unknown) prediction
  1283 2461409.77317 2027-01-04 06:31    8.60000 112 (span only, gap unknown) prediction
  1284 2461411.98357 2027-01-06 11:34    8.60000 112 (span only, gap unknown) prediction
  1285 2461414.19397 2027-01-08 16:37    8.70000 112 (span only, gap unknown) prediction
  1286 2461416.40437 2027-01-10 21:39    8.70000 112 (span only, gap unknown) prediction
  1287 2461418.61478 2027-01-13 02:42    8.70000 112 (span only, gap unknown) prediction
  1288 2461420.82518 2027-01-15 07:45    8.70000 112 (span only, gap unknown) prediction
  1289 2461423.03558 2027-01-17 12:48    8.70000 112 (span only, gap unknown) prediction
  1290 2461425.24598 2027-01-19 17:50    8.70000 113 (span only, gap unknown) prediction
  1291 2461427.45638 2027-01-21 22:53    8.70000 113 (span only, gap unknown) prediction
  1292 2461429.66678 2027-01-24 03:56    8.70000 113 (span only, gap unknown) prediction
  1293 2461431.87718 2027-01-26 08:59    8.80000 113 (span only, gap unknown) prediction
  1294 2461434.08758 2027-01-28 14:01    8.80000 113 (span only, gap unknown) prediction
  1295 2461436.29799 2027-01-30 19:04    8.80000 113 (span only, gap unknown) prediction
  1296 2461438.50839 2027-02-02 00:07    8.80000 113 (span only, gap unknown) prediction
  1297 2461440.71879 2027-02-04 05:10    8.80000 113 (span only, gap unknown) prediction
  1298 2461442.92919 2027-02-06 10:12    8.80000 113 (span only, gap unknown) prediction
  1299 2461445.13959 2027-02-08 15:15    8.80000 113 (span only, gap unknown) prediction
  1300 2461447.34999 2027-02-10 20:18    8.90000 113 (span only, gap unknown) prediction
  1301 2461449.56039 2027-02-13 01:21    8.90000 113 (span only, gap unknown) prediction
  1302 2461451.77080 2027-02-15 06:24    8.90000 114 (span only, gap unknown) prediction
  1303 2461453.98120 2027-02-17 11:26    8.90000 114 (span only, gap unknown) prediction
  1304 2461456.19160 2027-02-19 16:29    8.90000 114 (span only, gap unknown) prediction
  1305 2461458.40200 2027-02-21 21:32    8.90000 114 (span only, gap unknown) prediction
  1306 2461460.61240 2027-02-24 02:35    8.90000 114 (span only, gap unknown) prediction
  1307 2461462.82280 2027-02-26 07:38    9.00000 114 (span only, gap unknown) prediction
  1308 2461465.03320 2027-02-28 12:41    9.00000 114 (span only, gap unknown) prediction
  1309 2461467.24361 2027-03-02 17:44    9.00000 114 (span only, gap unknown) prediction
  1310 2461469.45401 2027-03-04 22:46    9.00000 114 (span only, gap unknown) prediction
  1311 2461471.66441 2027-03-07 03:49    9.00000 114 (span only, gap unknown) prediction
  1312 2461473.87481 2027-03-09 08:52    9.00000 114 (span only, gap unknown) prediction
  1313 2461476.08521 2027-03-11 13:55    9.00000 114 (span only, gap unknown) prediction
  1314 2461478.29561 2027-03-13 18:58    9.10000 114 (span only, gap unknown) prediction
Outcomes defined in advance (QLP or SPOC light curve of the test sector, transit-masked biweight detrend; no TESScut fallback - withdrawn 2026-10-20 in conformance v2.1): (1) recovered - a box of depth 0.5-1.5x and duration 0.7-1.3x the reference values at >= 2 covered predicted transit windows, stacked SNR >= 5, timing gate |sum(w_i dt_i)/sum(w_i)| <= max(3 mean(sigma_min,i), 30 min) with w_i = 1/depth_err_i^2 over the coverage-qualified windows (frozen evaluator; inverse depth-variance weights); duration and full-coverage criteria are assessed under the separately versioned conformance procedure (see CLARIFICATION_TIMING_RULE_2026-10-20.md); (2) inconsistent - a comparable dip exists but its times differ by > 30 min from every prediction; (3) excluded - stacked depth at the predicted phase < 0.3x at 3 sigma with >= 2 transits fully covered; (4) insufficient - fewer than 2 predicted transits covered. QLP S99+ sector times were corrected for the barycentric timestamp error before the fit (results/qlp_clock_v2/; corrections in min: {99: -0.0}). Generated by scripts/prereg_v2.py 151767028 --freeze --version 2.


**Dated amendment 2026-10-21 (appended after the independent review results/REVIEW_round4_freezes.md; the frozen predictions and CSV are unchanged).**
Credit (addition). The searched catalogues also associate this signal with the RAVEN nsfp09 detection list (eumemic vetted_signals.csv.gz
known_detail "literature:RAVEN nsfp09:x1"; Kuberwastaken/planethunt known_signals.csv, P = 2.2103981294347577 d, source nsfp09_table.csv).
This is a prior detection, not a validation. The primary RAVEN table has not yet been checked, so no earliest-publication date is assigned.
Scoring (amends the scoring statement above; the predictions are unchanged). The test of record is S112. It stays the test of
record whatever its result, including INSUFFICIENT, CLOCK_UNVERIFIED or INVALID_INPUT, and is never replaced by a later sector; later
listed sectors are scored separately with their own configs and reported as further tests, never pooled with it. The per-sector configs
are locked in configs/conformance/151767028_S<sector>.json (made by scripts/make_conformance_configs_round4.py; SHA-256 prefixes: 151767028_S112.json 27495b8da07491f2; 151767028_S113.json c71b4d676e30cc1f; 151767028_S114.json c8ffb5d991d2a3d4). The sentence "No TESScut or other ad hoc extraction will be used" is replaced by: "No TESScut flux extraction or substitute
light curve will be scored. The declared clock tool (scripts/qlp_clock_test_sector.py) uses the TIME and TIMECORR columns of a TESScut
cutout of the test sector at test time; that cutout contains pixels, but no flux from it is used." The generic outcome paragraph above
is a secondary historical readout; the pinned conformance docstring (prereg_conformance.py, SHA a864b07a...) governs all science
outcomes and refusals.

**Dated note 2026-10-21 (appended after the re-check results/REVIEW_round4_recheck.md; predictions unchanged).** Every test of this star
also requires scripts/validate_round4_inputs.py to pass at three stages: before any test-sector data access (the config, prediction CSV,
evaluator and c0 prior are the bytes recorded in configs/conformance/ROUND4_LOCK.json, SHA-256 prefix d7a20a59cccbf8bf), after the clock tool (the clock
record was made from that config and that prior) and after the evaluator (the output was made from that config and the same light curve).
A refusal at any stage is reported as the result for that sector; a refused primary sector stays the test of record.
Credit (update to the amendment above). The primary RAVEN table has now been checked: Lafarga et al. (2026, MNRAS, doi:10.1093/mnras/stag512;
online material Zenodo 19661443, nsfp09_table.csv line 4832) list this signal at P = 2.2103981294347577 d (NSFP score 0.983) in their
first-stage candidate catalog, with a 3P alias; it is not in their vetted or validated tables. This is a prior detection, not a validation.
Addendum 2026-10-21 (after results/REVIEW_round4_recheck2.md). At the final stage the validator also requires that the evaluator output
was scored with the SAME clock record (its clock_record SHA-256 equals that of the clock file), and every hash must be present and
well-formed. An output without clock provenance counts only as a pre-clock outcome (INVALID_INPUT, INSUFFICIENT or CLOCK_UNVERIFIED).

---
**Dated note 2026-10-23 (v1.16).** The TRICERATOPS values quoted above (single screening run, scripts/triceratops_qlp.py) were computed on a light-curve fold of sectors 36, 63, 90, 99, 100 (recorded: 90, 99, 100); the saved record listed only the aperture sectors. The values are the original saved outputs; no probability was recomputed. Frozen predictions and scoring rules are unchanged. See corrections/CORRECTION_TRICERATOPS_PIXEL_2026-10-22.md.
