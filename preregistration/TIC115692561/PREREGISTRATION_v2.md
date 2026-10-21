# Pre-registered transit predictions v2 - TIC 115692561
Frozen: 2026-10-20 00:44:10 UTC. Author: Fernando Molina (Independent researcher, ORCID 0009-0002-2872-3406). Analysis with Claude (Anthropic) under the author's direction.
First freeze for this object (v2 tooling: all-sector ephemeris). Reason (external review 2026-10-18,
results/external_review_allsky/REVIEW.md): v1 timed only the 200-s sectors (vet.py min_pts cut), ignoring 2018-2021 data; v2 fits one time offset per
sector from ALL sectors (raw SAP flux, cadence-aware model, local baselines; SPOC 2-min sectors where they exist) on top of the all-data BLS ephemeris.
Ephemeris: T0 = BTJD 3920.75813 +- 3.0 min (epoch 3018), P = 0.850320 +- 0.000001 d (chi2/dof 4.6/2, inflation x1.52); all-data BLS P = 0.850316.
Sector times used: S2 SPOC 2-min (30 ev, O-C -1.1 +- 1.8 min), S29 QLP SAP (25 ev, O-C +3.5 +- 3.6 min), S69 QLP SAP (24 ev, O-C +3.3 +- 2.4 min), S96 QLP SAP (27 ev, O-C -2.8 +- 2.4 min).
Depth per sector (fixed shape, local baseline, raw SAP): S2 225, S29 218, S69 164, S96 119 ppm.
Round-3 object, independent rediscovery: listed by eumemic/exoplanets (candidates_allsky.csv). Weak (SNR 7.6; P 0.850 d, ~140 ppm). On target. Test: Sector 106 (observed, data not public at freeze).
Reference values for the outcome clauses: depth 143 ppm (raw SAP, all sectors), T14 1.30 h.
SHA-256 of predicted_transits_2026_2027_v2.csv: d8fe193dfce203392ad380c74d1ee08a9364d7335dc3b0e72bc9e77f0ed41085
**Test of record: next TESS sector(s).** Predicted mid-transits (sigma_min = 1-sigma timing uncertainty at that epoch):
 epoch    tc_bjd_tdb              utc  sigma_min  tess_sector                                                  status
  3386 2461233.67598 2026-07-12 04:08    3.40000          106 prediction (sector observed, data not public at freeze)
  3387 2461234.52630 2026-07-13 00:33    3.40000          106 prediction (sector observed, data not public at freeze)
  3388 2461235.37662 2026-07-13 20:57    3.40000          106 prediction (sector observed, data not public at freeze)
  3389 2461236.22694 2026-07-14 17:21    3.40000          106 prediction (sector observed, data not public at freeze)
  3390 2461237.07726 2026-07-15 13:46    3.40000          106 prediction (sector observed, data not public at freeze)
  3391 2461237.92758 2026-07-16 10:10    3.40000          106 prediction (sector observed, data not public at freeze)
  3392 2461238.77790 2026-07-17 06:35    3.40000          106 prediction (sector observed, data not public at freeze)
  3393 2461239.62822 2026-07-18 02:59    3.40000          106 prediction (sector observed, data not public at freeze)
  3394 2461240.47854 2026-07-18 23:23    3.40000          106 prediction (sector observed, data not public at freeze)
  3395 2461241.32886 2026-07-19 19:48    3.40000          106 prediction (sector observed, data not public at freeze)
  3396 2461242.17918 2026-07-20 16:12    3.40000          106 prediction (sector observed, data not public at freeze)
  3397 2461243.02950 2026-07-21 12:37    3.40000          106 prediction (sector observed, data not public at freeze)
  3398 2461243.87982 2026-07-22 09:01    3.40000          106 prediction (sector observed, data not public at freeze)
  3399 2461244.73014 2026-07-23 05:25    3.40000          106 prediction (sector observed, data not public at freeze)
  3400 2461245.58046 2026-07-24 01:50    3.40000          106 prediction (sector observed, data not public at freeze)
  3401 2461246.43078 2026-07-24 22:14    3.40000          106 prediction (sector observed, data not public at freeze)
  3402 2461247.28110 2026-07-25 18:38    3.40000          106 prediction (sector observed, data not public at freeze)
  3403 2461248.13142 2026-07-26 15:03    3.40000          106 prediction (sector observed, data not public at freeze)
  3404 2461248.98174 2026-07-27 11:27    3.40000          106 prediction (sector observed, data not public at freeze)
  3405 2461249.83207 2026-07-28 07:52    3.40000          106 prediction (sector observed, data not public at freeze)
  3406 2461250.68239 2026-07-29 04:16    3.40000          106 prediction (sector observed, data not public at freeze)
  3407 2461251.53271 2026-07-30 00:40    3.40000          106 prediction (sector observed, data not public at freeze)
  3408 2461252.38303 2026-07-30 21:05    3.40000          106 prediction (sector observed, data not public at freeze)
  3409 2461253.23335 2026-07-31 17:29    3.40000          106 prediction (sector observed, data not public at freeze)
  3410 2461254.08367 2026-08-01 13:54    3.40000          106 prediction (sector observed, data not public at freeze)
  3411 2461254.93399 2026-08-02 10:18    3.40000          106 prediction (sector observed, data not public at freeze)
  3412 2461255.78431 2026-08-03 06:42    3.40000          106 prediction (sector observed, data not public at freeze)
  3413 2461256.63463 2026-08-04 03:07    3.40000          106 prediction (sector observed, data not public at freeze)
  3414 2461257.48495 2026-08-04 23:31    3.40000          106 prediction (sector observed, data not public at freeze)
  3415 2461258.33527 2026-08-05 19:56    3.40000          106 prediction (sector observed, data not public at freeze)
  3416 2461259.18559 2026-08-06 16:20    3.40000          106 prediction (sector observed, data not public at freeze)
  3417 2461260.03591 2026-08-07 12:44    3.40000          106 prediction (sector observed, data not public at freeze)
Outcomes defined in advance (QLP or SPOC light curve of the test sector, or a TESScut fixed-aperture extraction, transit-masked biweight detrend): (1) recovered - a box of depth 0.5-1.5x and duration 0.7-1.3x the reference values within +-3 sigma_min (and in any case within +-30 min) of >= 2 predicted times, stacked SNR >= 5; (2) inconsistent - a comparable dip exists but its times differ by > 30 min from every prediction; (3) excluded - stacked depth at the predicted phase < 0.3x at 3 sigma with >= 2 transits fully covered; (4) insufficient - fewer than 2 predicted transits covered. No QLP S99+ sector time enters this ephemeris. Generated by scripts/prereg_v2.py 115692561 --freeze --version 2.


**Addendum 2026-10-20 (timing rule):** the phrase "and in any case within +-30 min" above misstates the rule. The governing rule is the public protocol's (Zenodo 10.5281/zenodo.23462442): stacked timing offset within max(3 sigma_pred, 30 min), as implemented in the frozen evaluator scripts/prereg_test.py. No prediction, CSV or checksum is changed. See CLARIFICATION_TIMING_RULE_2026-10-20.md.


**Erratum 2026-10-20 (data availability):** the status "data not public at freeze" above is incorrect. This sector had already been observed and public data products existed at the freeze (product-specific; target QLP light curves were not yet released). The authors attest that the target-sector photometry was not examined before the freeze. Read the status as "sector already observed; public data existed; authors attest target-sector photometry not examined before freeze". See ERRATUM_S106_DATA_AVAILABILITY_2026-10-20.md. Prediction CSV bytes and hashes are unchanged.


**Amendment 2026-10-20 (scoring procedure fixed before any S106 photometry is examined):** this test will be scored with the conformance procedure conformance-v2.1 (conformance_v2.1/scripts/prereg_conformance.py, SHA-256 a864b07ace8d3220a2d94a60513a488c8a5d87b54f41ebf510ff40ef1755311f) and the locked configuration conformance_v2.1/configs/conformance/115692561_S106.json (SHA-256 ef7eb24089b7c3ed953a53a14694dcb8b802e9d7702294abc5c416954cf4cd2f): product QLP SAP_FLUX, reference depth 143.0 ppm, T14 1.3 h, timing gate max(3 sigma_min, 30 min) from the hashed CSV above. Its outcome under max() is the outcome of record; the min() reading, the per-event min() assessment and the frozen evaluator's (conformance_v2.1/scripts/prereg_test.py) literal output are reported next to it. The procedure replaces the per-event depth/duration matching wording above with a joint fit plus per-transit checks, removes cadences within 1.5 d after a data resume and 0.5 d before a gap (an author-selected edge rule), requires full transit coverage, and scores only the first QLP release (v01). RECOVERED means compatibility with the procedure's common-box and parity-split rule; it does not show that each transit meets the original timing and duration limits. Which document governs each item, and every departure from the protocol, is listed in conformance_v2.1/GOVERNANCE_S106_TESTS_2026-10-20.md. Stated in advance (conditional on in-sample noise and gap templates, not outcome probabilities): median expected joint SNR 2.8; holdout on-time RECOVERED 0/40. A decisive outcome may be unlikely; no outcome probability has been established. Prediction CSV bytes and hashes are unchanged.

**Dated note 2026-10-21 (appended; frozen CSV unchanged).** This list stops at epoch 3417 because the generator then stopped after 399
epochs. Two S106 transits (epochs 3418 and 3419, BJD_TDB 2461260.88623 and 2461261.73655) and all 34 S107 transits are missing. The S106
test of record remains this frozen list as published (configs/conformance/115692561_S106.json); the omission will be stated next to its
result. Epoch 3418 lies about 1.0 d before the end of the sector and might have been eligible; 3419 lies inside the end-of-data edge cut.
No supplementary list is made, so S107 is not tested for this star. See ERRATUM_PREDICTION_HORIZON_2026-10-21.md.
