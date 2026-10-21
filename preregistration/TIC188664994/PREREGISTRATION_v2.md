# Pre-registered transit predictions v2 - TIC 188664994
Frozen: 2026-10-21 01:57:29 UTC. Author: Fernando Molina (Independent researcher, ORCID 0009-0002-2872-3406). Analysis with Claude (Anthropic) under the author's direction.
First freeze for this object (v2 tooling: all-sector ephemeris). Reason (external review 2026-10-18,
results/external_review_allsky/REVIEW.md): v1 timed only the 200-s sectors (vet.py min_pts cut), ignoring 2018-2021 data; v2 fits one time offset per
sector from ALL sectors (raw SAP flux, cadence-aware model, local baselines; SPOC 2-min sectors where they exist) on top of the all-data BLS ephemeris.
Ephemeris: T0 = BTJD 3597.39365 +- 8.2 min (epoch 484), P = 3.781806 +- 0.000021 d (chi2/dof 201.1/15, inflation x3.66); all-data BLS P = 3.781784.
Sector times used: S17 SPOC 2-min (5 ev, O-C -1.1 +- 4.8 min), S20 SPOC 2-min (7 ev, O-C +35.4 +- 20.4 min), S23 SPOC 2-min (5 ev, O-C +13.1 +- 25.8 min), S24 SPOC 2-min (6 ev, O-C +11.7 +- 3.6 min), S40 QLP SAP (8 ev, O-C +5.7 +- 7.8 min), S47 QLP SAP (7 ev, O-C -4.3 +- 5.4 min), S50 QLP SAP (5 ev, O-C -9.8 +- 7.8 min), S51 QLP SAP (4 ev, O-C -28.0 +- 6.6 min), S52 QLP SAP (5 ev, O-C -28.3 +- 6.6 min), S53 QLP SAP (6 ev, O-C -14.1 +- 7.8 min), S54 QLP SAP (7 ev, O-C -5.9 +- 12.6 min), S57 QLP SAP (5 ev, O-C +40.2 +- 19.2 min), S60 QLP SAP (5 ev, O-C -1.3 +- 18.6 min), S73 QLP SAP (5 ev, O-C +4.2 +- 9.6 min), S80 QLP SAP (7 ev, O-C -2.2 +- 3.6 min), S81 QLP SAP (6 ev, O-C -15.6 +- 3.6 min), S84 QLP SAP (6 ev, O-C +59.4 +- 5.4 min).
Depth per sector (fixed shape, local baseline, raw SAP): S17 422, S20 406, S23 325, S24 568, S40 614, S47 566, S50 549, S51 513, S52 490, S53 535, S54 484, S57 239, S60 523, S73 328, S80 415, S81 605, S84 321 ppm.
Round 4 of the all-sky search (DECISIONS 113-117): on-target in the FFI pixel test, vet.py v1.13, triage PASS (SNR 13.1), TRICERATOPS FPP 0.081 / NFPP 0.0078 (single run, no contrast curve; screening, not validation). No prior report found (period-matched search of ExoFOP TOI/CTOI and public GitHub/Zenodo candidate lists, 2026-10-20; a Nigraha period_info match was a neighbouring-row artefact). Caution: the per-sector times scatter well beyond their errors (chi2/dof 201/15; e.g. S84 +59 min, S51-S52 -28 min); the error inflation (x3.66) is applied to the predictions. Scoring statement (fixed at this freeze, before any test-sector photometry of this star is examined): each listed TESS sector will be scored separately, in sector order, with the published conformance evaluator scripts/prereg_conformance.py v2.1 rc4 (SHA-256 a864b07ace8d3220a2d94a60513a488c8a5d87b54f41ebf510ff40ef1755311f; conformance_v2.1/CONFORMANCE_PROCEDURE_v2.1.md), using its general rules (the object-specific clauses written for the S106 objects do not apply) and a per-object config locked before that sector is examined: QLP SAP_FLUX, release of record v01, the QLP clock gate, and the reference depth and T14 stated below. The first listed sector with a released QLP v01 light curve is the test of record; later sectors are reported as further tests. Where the generic outcome clause below differs, the conformance procedure governs. Its false-recovery calibration was made on the S106 objects; no object-specific calibration has been made for this star. No TESScut or other ad hoc extraction will be used.
Sectors excluded from the ephemeris fit (data quality, decided before freezing): S26 - QLP and SPOC S26 light curves of this star are corrupted (6-h-binned p1-p99 flux range: SPOC PDCSAP 112 % vs 0.4-0.8 % in S17-S24, QLP SAP 14.7 % vs 1.3-2.1 %; point-to-point scatter SPOC 9030 vs 1840-2050 ppm, QLP 1572 vs 597-683 ppm); the S26 dry-run depth was 12379 ppm vs 320-610 ppm elsewhere
Reference values for the outcome clauses: depth 412 ppm (raw SAP, all sectors), T14 1.80 h.
SHA-256 of predicted_transits_2026_2027_v2.csv: 0d450700afaa54f26ea80620681ebff98aaed03878ea8a7d75d3a1612a2a2dd4
**Test of record: next TESS sector(s).** Predicted mid-transits (sigma_min = 1-sigma timing uncertainty at that epoch):
 epoch    tc_bjd_tdb              utc  sigma_min                  tess_sector     status
   733 2461539.06323 2027-05-13 13:27   14.80000 117 (span only, gap unknown) prediction
   734 2461542.84503 2027-05-17 08:13   14.80000 117 (span only, gap unknown) prediction
   735 2461546.62684 2027-05-21 02:59   14.80000 117 (span only, gap unknown) prediction
   736 2461550.40865 2027-05-24 21:45   14.90000 117 (span only, gap unknown) prediction
   737 2461554.19045 2027-05-28 16:31   14.90000 117 (span only, gap unknown) prediction
   738 2461557.97226 2027-06-01 11:16   14.90000 117 (span only, gap unknown) prediction
   739 2461561.75406 2027-06-05 06:02   15.00000 117 (span only, gap unknown) prediction
   740 2461565.53587 2027-06-09 00:48   15.00000 118 (span only, gap unknown) prediction
   741 2461569.31767 2027-06-12 19:34   15.00000 118 (span only, gap unknown) prediction
   742 2461573.09948 2027-06-16 14:20   15.00000 118 (span only, gap unknown) prediction
   743 2461576.88128 2027-06-20 09:05   15.10000 118 (span only, gap unknown) prediction
   744 2461580.66309 2027-06-24 03:51   15.10000 118 (span only, gap unknown) prediction
   745 2461584.44489 2027-06-27 22:37   15.10000 118 (span only, gap unknown) prediction
   746 2461588.22670 2027-07-01 17:23   15.20000 118 (span only, gap unknown) prediction
   747 2461592.00851 2027-07-05 12:09   15.20000 119 (span only, gap unknown) prediction
   748 2461595.79031 2027-07-09 06:55   15.20000 119 (span only, gap unknown) prediction
   749 2461599.57212 2027-07-13 01:41   15.20000 119 (span only, gap unknown) prediction
   750 2461603.35392 2027-07-16 20:27   15.30000 119 (span only, gap unknown) prediction
   751 2461607.13573 2027-07-20 15:13   15.30000 119 (span only, gap unknown) prediction
   752 2461610.91753 2027-07-24 09:58   15.30000 119 (span only, gap unknown) prediction
   753 2461614.69934 2027-07-28 04:44   15.40000 119 (span only, gap unknown) prediction
Outcomes defined in advance (QLP or SPOC light curve of the test sector, transit-masked biweight detrend; no TESScut fallback - withdrawn 2026-10-20 in conformance v2.1): (1) recovered - a box of depth 0.5-1.5x and duration 0.7-1.3x the reference values at >= 2 covered predicted transit windows, stacked SNR >= 5, timing gate |sum(w_i dt_i)/sum(w_i)| <= max(3 mean(sigma_min,i), 30 min) with w_i = 1/depth_err_i^2 over the coverage-qualified windows (frozen evaluator; inverse depth-variance weights); duration and full-coverage criteria are assessed under the separately versioned conformance procedure (see CLARIFICATION_TIMING_RULE_2026-10-20.md); (2) inconsistent - a comparable dip exists but its times differ by > 30 min from every prediction; (3) excluded - stacked depth at the predicted phase < 0.3x at 3 sigma with >= 2 transits fully covered; (4) insufficient - fewer than 2 predicted transits covered. No QLP S99+ sector time enters this ephemeris. Generated by scripts/prereg_v2.py 188664994 --freeze --version 2.


**Dated amendment 2026-10-21 (appended after the independent review results/REVIEW_round4_freezes.md; the frozen predictions and CSV are unchanged).**
Timing uncertainty. The listed sigma values are formal uncertainties of the linear ephemeris after a common error-inflation factor. They
do not include an independently calibrated additional sector timing systematic. Sector residuals have RMS 22.9 min, and leaving one
sector out changes the final listed prediction by up to 21.7 min. This is an exploratory, timing-scattered ephemeris test; its nominal
3-sigma gate has not been shown to have 99.7 % predictive coverage. The frozen gate is kept; it will not be enlarged after the test data
are seen.
Reference depth. The frozen 412-ppm reference keeps the original all-sector SAP estimate, which includes S26; removing S26 gives
420 +- 43 ppm. S26 is excluded from the timing fit only. In the exclusion reason above, "320-610 ppm elsewhere" should read "239-614 ppm
among the retained sector fits". The quality numbers use 6-h median bins of median-normalised flux (QUALITY = 0) and the point-to-point
estimator 1.4826 median(|diff(f)|)/sqrt(2). The S26 exclusion was decided after a first dry run of this fit, in which S26 was not a timing
outlier (O-C +12 min); including it changes the forecast by seconds.
Coverage. This version covers only S117-S119. Predicted later coverage in S122-S125 and S129-S132 has no published dates in the schedule
used here; any later supplement will not replace the S117 test of record.
Scoring (amends the scoring statement above; the predictions are unchanged). The test of record is S117. It stays the test of
record whatever its result, including INSUFFICIENT, CLOCK_UNVERIFIED or INVALID_INPUT, and is never replaced by a later sector; later
listed sectors are scored separately with their own configs and reported as further tests, never pooled with it. The per-sector configs
are locked in configs/conformance/188664994_S<sector>.json (made by scripts/make_conformance_configs_round4.py; SHA-256 prefixes: 188664994_S117.json 82ceaf8d8a82b69c; 188664994_S118.json 9b8ee77578638012; 188664994_S119.json 7b2afa81be6fb0af). The sentence "No TESScut or other ad hoc extraction will be used" is replaced by: "No TESScut flux extraction or substitute
light curve will be scored. The declared clock tool (scripts/qlp_clock_test_sector.py) uses the TIME and TIMECORR columns of a TESScut
cutout of the test sector at test time; that cutout contains pixels, but no flux from it is used." The generic outcome paragraph above
is a secondary historical readout; the pinned conformance docstring (prereg_conformance.py, SHA a864b07a...) governs all science
outcomes and refusals.

**Dated note 2026-10-21 (appended after the re-check results/REVIEW_round4_recheck.md; predictions unchanged).** Every test of this star
also requires scripts/validate_round4_inputs.py to pass at three stages: before any test-sector data access (the config, prediction CSV,
evaluator and c0 prior are the bytes recorded in configs/conformance/ROUND4_LOCK.json, SHA-256 prefix d7a20a59cccbf8bf), after the clock tool (the clock
record was made from that config and that prior) and after the evaluator (the output was made from that config and the same light curve).
A refusal at any stage is reported as the result for that sector; a refused primary sector stays the test of record.
Addendum 2026-10-21 (after results/REVIEW_round4_recheck2.md). At the final stage the validator also requires that the evaluator output
was scored with the SAME clock record (its clock_record SHA-256 equals that of the clock file), and every hash must be present and
well-formed. An output without clock provenance counts only as a pre-clock outcome (INVALID_INPUT, INSUFFICIENT or CLOCK_UNVERIFIED).
