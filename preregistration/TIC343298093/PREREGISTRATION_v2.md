# Pre-registered transit predictions v2 - TIC 343298093
Frozen: 2026-10-21 01:57:22 UTC. Author: Fernando Molina (Independent researcher, ORCID 0009-0002-2872-3406). Analysis with Claude (Anthropic) under the author's direction.
First freeze for this object (v2 tooling: all-sector ephemeris). Reason (external review 2026-10-18,
results/external_review_allsky/REVIEW.md): v1 timed only the 200-s sectors (vet.py min_pts cut), ignoring 2018-2021 data; v2 fits one time offset per
sector from ALL sectors (raw SAP flux, cadence-aware model, local baselines; SPOC 2-min sectors where they exist) on top of the all-data BLS ephemeris.
Ephemeris: T0 = BTJD 4164.67665 +- 2.6 min (epoch 3309), P = 0.766143 +- 0.000007 d (chi2/dof 29.2/5, inflation x2.42); all-data BLS P = 0.766141.
Sector times used: S39 QLP SAP (29 ev, O-C +10.5 +- 10.2 min), S66 QLP SAP (32 ev, O-C -41.6 +- 18.6 min), S93 QLP SAP (29 ev, O-C -1.3 +- 4.8 min), S100 QLP SAP (24 ev, O-C +8.6 +- 9.0 min), S101 QLP SAP (25 ev, O-C +3.6 +- 9.0 min), S102 QLP SAP (24 ev, O-C -2.6 +- 1.2 min), S103 QLP SAP (27 ev, O-C +10.0 +- 2.4 min).
Depth per sector (fixed shape, local baseline, raw SAP): S39 353, S66 196, S93 457, S100 264, S101 309, S102 397, S103 353 ppm.
Round 4 of the all-sky search (DECISIONS 113-117): on-target in the FFI pixel test, vet.py v1.13, triage PASS (SNR 9.1), TRICERATOPS FPP 0.065 / NFPP 0.0010 (single run, no contrast curve; screening, not validation). No prior report found (period-matched search of ExoFOP TOI/CTOI and public GitHub/Zenodo candidate lists, 2026-10-20). Scoring statement (fixed at this freeze, before any test-sector photometry of this star is examined): each listed TESS sector will be scored separately, in sector order, with the published conformance evaluator scripts/prereg_conformance.py v2.1 rc4 (SHA-256 a864b07ace8d3220a2d94a60513a488c8a5d87b54f41ebf510ff40ef1755311f; conformance_v2.1/CONFORMANCE_PROCEDURE_v2.1.md), using its general rules (the object-specific clauses written for the S106 objects do not apply) and a per-object config locked before that sector is examined: QLP SAP_FLUX, release of record v01, the QLP clock gate, and the reference depth and T14 stated below. The first listed sector with a released QLP v01 light curve is the test of record; later sectors are reported as further tests. Where the generic outcome clause below differs, the conformance procedure governs. Its false-recovery calibration was made on the S106 objects; no object-specific calibration has been made for this star. No TESScut or other ad hoc extraction will be used.

Reference values for the outcome clauses: depth 302 ppm (raw SAP, all sectors), T14 1.10 h.
SHA-256 of predicted_transits_2026_2027_v2.csv: 4f14d1fe96b152eab1139e0bbcc55b9ab70095268ef67f954780284fb6dd06c1
**Test of record: next TESS sector(s).** Predicted mid-transits (sigma_min = 1-sigma timing uncertainty at that epoch):
 epoch    tc_bjd_tdb              utc  sigma_min                  tess_sector     status
  3646 2461422.86669 2027-01-17 08:51    4.70000 113 (span only, gap unknown) prediction
  3647 2461423.63283 2027-01-18 03:14    4.70000 113 (span only, gap unknown) prediction
  3648 2461424.39897 2027-01-18 21:37    4.70000 113 (span only, gap unknown) prediction
  3649 2461425.16512 2027-01-19 16:00    4.70000 113 (span only, gap unknown) prediction
  3650 2461425.93126 2027-01-20 10:24    4.70000 113 (span only, gap unknown) prediction
  3651 2461426.69740 2027-01-21 04:47    4.80000 113 (span only, gap unknown) prediction
  3652 2461427.46354 2027-01-21 23:10    4.80000 113 (span only, gap unknown) prediction
  3653 2461428.22969 2027-01-22 17:33    4.80000 113 (span only, gap unknown) prediction
  3654 2461428.99583 2027-01-23 11:56    4.80000 113 (span only, gap unknown) prediction
  3655 2461429.76197 2027-01-24 06:20    4.80000 113 (span only, gap unknown) prediction
  3656 2461430.52811 2027-01-25 00:43    4.80000 113 (span only, gap unknown) prediction
  3657 2461431.29426 2027-01-25 19:06    4.80000 113 (span only, gap unknown) prediction
  3658 2461432.06040 2027-01-26 13:29    4.80000 113 (span only, gap unknown) prediction
  3659 2461432.82654 2027-01-27 07:52    4.80000 113 (span only, gap unknown) prediction
  3660 2461433.59268 2027-01-28 02:16    4.80000 113 (span only, gap unknown) prediction
  3661 2461434.35883 2027-01-28 20:39    4.80000 113 (span only, gap unknown) prediction
  3662 2461435.12497 2027-01-29 15:02    4.80000 113 (span only, gap unknown) prediction
  3663 2461435.89111 2027-01-30 09:25    4.90000 113 (span only, gap unknown) prediction
  3664 2461436.65725 2027-01-31 03:48    4.90000 113 (span only, gap unknown) prediction
  3665 2461437.42340 2027-01-31 22:12    4.90000 113 (span only, gap unknown) prediction
  3666 2461438.18954 2027-02-01 16:35    4.90000 113 (span only, gap unknown) prediction
  3667 2461438.95568 2027-02-02 10:58    4.90000 113 (span only, gap unknown) prediction
  3668 2461439.72182 2027-02-03 05:21    4.90000 113 (span only, gap unknown) prediction
  3669 2461440.48797 2027-02-03 23:44    4.90000 113 (span only, gap unknown) prediction
  3670 2461441.25411 2027-02-04 18:08    4.90000 113 (span only, gap unknown) prediction
  3671 2461442.02025 2027-02-05 12:31    4.90000 113 (span only, gap unknown) prediction
  3672 2461442.78639 2027-02-06 06:54    4.90000 113 (span only, gap unknown) prediction
  3673 2461443.55254 2027-02-07 01:17    4.90000 113 (span only, gap unknown) prediction
  3674 2461444.31868 2027-02-07 19:40    5.00000 113 (span only, gap unknown) prediction
  3675 2461445.08482 2027-02-08 14:04    5.00000 113 (span only, gap unknown) prediction
  3676 2461445.85097 2027-02-09 08:27    5.00000 113 (span only, gap unknown) prediction
  3677 2461446.61711 2027-02-10 02:50    5.00000 113 (span only, gap unknown) prediction
  3678 2461447.38325 2027-02-10 21:13    5.00000 113 (span only, gap unknown) prediction
  3679 2461448.14939 2027-02-11 15:36    5.00000 113 (span only, gap unknown) prediction
  3680 2461448.91554 2027-02-12 10:00    5.00000 113 (span only, gap unknown) prediction
  3681 2461449.68168 2027-02-13 04:23    5.00000 113 (span only, gap unknown) prediction
  3682 2461450.44782 2027-02-13 22:46    5.00000 113 (span only, gap unknown) prediction
  3683 2461451.21396 2027-02-14 17:09    5.00000 114 (span only, gap unknown) prediction
  3684 2461451.98011 2027-02-15 11:32    5.00000 114 (span only, gap unknown) prediction
  3685 2461452.74625 2027-02-16 05:55    5.00000 114 (span only, gap unknown) prediction
  3686 2461453.51239 2027-02-17 00:19    5.10000 114 (span only, gap unknown) prediction
  3687 2461454.27853 2027-02-17 18:42    5.10000 114 (span only, gap unknown) prediction
  3688 2461455.04468 2027-02-18 13:05    5.10000 114 (span only, gap unknown) prediction
  3689 2461455.81082 2027-02-19 07:28    5.10000 114 (span only, gap unknown) prediction
  3690 2461456.57696 2027-02-20 01:51    5.10000 114 (span only, gap unknown) prediction
  3691 2461457.34310 2027-02-20 20:15    5.10000 114 (span only, gap unknown) prediction
  3692 2461458.10925 2027-02-21 14:38    5.10000 114 (span only, gap unknown) prediction
  3693 2461458.87539 2027-02-22 09:01    5.10000 114 (span only, gap unknown) prediction
  3694 2461459.64153 2027-02-23 03:24    5.10000 114 (span only, gap unknown) prediction
  3695 2461460.40767 2027-02-23 21:47    5.10000 114 (span only, gap unknown) prediction
  3696 2461461.17382 2027-02-24 16:11    5.10000 114 (span only, gap unknown) prediction
  3697 2461461.93996 2027-02-25 10:34    5.10000 114 (span only, gap unknown) prediction
  3698 2461462.70610 2027-02-26 04:57    5.20000 114 (span only, gap unknown) prediction
  3699 2461463.47224 2027-02-26 23:20    5.20000 114 (span only, gap unknown) prediction
  3700 2461464.23839 2027-02-27 17:43    5.20000 114 (span only, gap unknown) prediction
  3701 2461465.00453 2027-02-28 12:06    5.20000 114 (span only, gap unknown) prediction
  3702 2461465.77067 2027-03-01 06:30    5.20000 114 (span only, gap unknown) prediction
  3703 2461466.53681 2027-03-02 00:53    5.20000 114 (span only, gap unknown) prediction
  3704 2461467.30296 2027-03-02 19:16    5.20000 114 (span only, gap unknown) prediction
  3705 2461468.06910 2027-03-03 13:39    5.20000 114 (span only, gap unknown) prediction
  3706 2461468.83524 2027-03-04 08:02    5.20000 114 (span only, gap unknown) prediction
  3707 2461469.60138 2027-03-05 02:26    5.20000 114 (span only, gap unknown) prediction
  3708 2461470.36753 2027-03-05 20:49    5.20000 114 (span only, gap unknown) prediction
  3709 2461471.13367 2027-03-06 15:12    5.20000 114 (span only, gap unknown) prediction
  3710 2461471.89981 2027-03-07 09:35    5.30000 114 (span only, gap unknown) prediction
  3711 2461472.66595 2027-03-08 03:58    5.30000 114 (span only, gap unknown) prediction
  3712 2461473.43210 2027-03-08 22:21    5.30000 114 (span only, gap unknown) prediction
  3713 2461474.19824 2027-03-09 16:45    5.30000 114 (span only, gap unknown) prediction
  3714 2461474.96438 2027-03-10 11:08    5.30000 114 (span only, gap unknown) prediction
  3715 2461475.73052 2027-03-11 05:31    5.30000 114 (span only, gap unknown) prediction
  3716 2461476.49667 2027-03-11 23:54    5.30000 114 (span only, gap unknown) prediction
  3717 2461477.26281 2027-03-12 18:17    5.30000 114 (span only, gap unknown) prediction
  3718 2461478.02895 2027-03-13 12:41    5.30000 114 (span only, gap unknown) prediction
  3719 2461478.79509 2027-03-14 07:04    5.30000 114 (span only, gap unknown) prediction
Outcomes defined in advance (QLP or SPOC light curve of the test sector, transit-masked biweight detrend; no TESScut fallback - withdrawn 2026-10-20 in conformance v2.1): (1) recovered - a box of depth 0.5-1.5x and duration 0.7-1.3x the reference values at >= 2 covered predicted transit windows, stacked SNR >= 5, timing gate |sum(w_i dt_i)/sum(w_i)| <= max(3 mean(sigma_min,i), 30 min) with w_i = 1/depth_err_i^2 over the coverage-qualified windows (frozen evaluator; inverse depth-variance weights); duration and full-coverage criteria are assessed under the separately versioned conformance procedure (see CLARIFICATION_TIMING_RULE_2026-10-20.md); (2) inconsistent - a comparable dip exists but its times differ by > 30 min from every prediction; (3) excluded - stacked depth at the predicted phase < 0.3x at 3 sigma with >= 2 transits fully covered; (4) insufficient - fewer than 2 predicted transits covered. QLP S99+ sector times were corrected for the barycentric timestamp error before the fit (results/qlp_clock_v2/; corrections in min: {100: 0.93, 101: 3.14, 102: 1.82, 103: 3.67}). Generated by scripts/prereg_v2.py 343298093 --freeze --version 2.


**Dated amendment 2026-10-21 (appended after the independent review results/REVIEW_round4_freezes.md; the frozen predictions and CSV are unchanged).**
Correction of priority. The statement above "No prior report found" is incorrect. eumemic/exoplanets lists this signal in
results_public/vetted_signals.csv.gz (P = 0.7661376546406703 d, depth 379 ppm, flagged "inconsistent transit SNRs") and in
all_signals.csv.gz (P = 0.766137625107561 d); it is not in their candidate lists. Our prior search missed compressed tables. This is an
independent rediscovery; we claim no priority. TRICERATOPS: NFPP = 0.00097, just below 0.001; FPP = 0.065 fails the validation condition
(FPP < 0.015).
Scoring (amends the scoring statement above; the predictions are unchanged). The test of record is S113. It stays the test of
record whatever its result, including INSUFFICIENT, CLOCK_UNVERIFIED or INVALID_INPUT, and is never replaced by a later sector; later
listed sectors are scored separately with their own configs and reported as further tests, never pooled with it. The per-sector configs
are locked in configs/conformance/343298093_S<sector>.json (made by scripts/make_conformance_configs_round4.py; SHA-256 prefixes: 343298093_S113.json 43eba5e3f6c4e59b; 343298093_S114.json 1bf0d2a756600f70). The sentence "No TESScut or other ad hoc extraction will be used" is replaced by: "No TESScut flux extraction or substitute
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

---
**Dated note 2026-10-23 (v1.16).** The TRICERATOPS values quoted above (single screening run, scripts/triceratops_qlp.py) were computed on a light-curve fold of sectors 13, 39, 66, 93, 100, 101, 102, 103 (recorded: 101, 102, 103); the saved record listed only the aperture sectors. The values are the original saved outputs; no probability was recomputed. Frozen predictions and scoring rules are unchanged. See corrections/CORRECTION_TRICERATOPS_PIXEL_2026-10-22.md.
