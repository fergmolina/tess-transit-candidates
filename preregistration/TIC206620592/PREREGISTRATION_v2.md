# Pre-registered transit predictions v2 - TIC 206620592
Frozen: 2026-10-20 00:33:10 UTC. Author: Fernando Molina (Independent researcher, ORCID 0009-0002-2872-3406). Analysis with Claude (Anthropic) under the author's direction.
First freeze for this object (v2 tooling: all-sector ephemeris). Reason (external review 2026-10-18,
results/external_review_allsky/REVIEW.md): v1 timed only the 200-s sectors (vet.py min_pts cut), ignoring 2018-2021 data; v2 fits one time offset per
sector from ALL sectors (raw SAP flux, cadence-aware model, local baselines; SPOC 2-min sectors where they exist) on top of the all-data BLS ephemeris.
Ephemeris: T0 = BTJD 3921.30310 +- 1.2 min (epoch 1712), P = 1.085671 +- 0.000001 d (chi2/dof 0.1/1, inflation x1.00); all-data BLS P = 1.085676.
Sector times used: S28 SPOC 2-min (16 ev, O-C -0.1 +- 1.2 min), S68 SPOC 2-min (20 ev, O-C +0.5 +- 2.4 min), S96 QLP SAP (16 ev, O-C -0.1 +- 1.2 min).
Depth per sector (fixed shape, local baseline, raw SAP): S28 226, S68 245, S96 240 ppm.
Round-3 object (P 1.086 d, ~240 ppm, ~1.0 R_E; M dwarf T=9.9). Pixel offset 0.41-0.42 px in both tested sectors (within the 0.5-px on-target limit). SPOC 2-min S28/S68 recover the dip at the known ephemeris (extraction check). No prior listing found in the sweep corpus. Test: Sector 106 (observed, data not public at freeze).
Reference values for the outcome clauses: depth 287 ppm (raw SAP, all sectors), T14 1.00 h.
SHA-256 of predicted_transits_2026_2027_v2.csv: 75b6ea732c2db970f4bd11a3ff62c58b14a2d0a4d745ff9180703077a5dcf343
**Test of record: next TESS sector(s).** Predicted mid-transits (sigma_min = 1-sigma timing uncertainty at that epoch):
 epoch    tc_bjd_tdb              utc  sigma_min  tess_sector                                                  status
  2000 2461233.97623 2026-07-12 11:18    1.40000          106 prediction (sector observed, data not public at freeze)
  2001 2461235.06190 2026-07-13 13:21    1.40000          106 prediction (sector observed, data not public at freeze)
  2002 2461236.14758 2026-07-14 15:25    1.40000          106 prediction (sector observed, data not public at freeze)
  2003 2461237.23325 2026-07-15 17:28    1.40000          106 prediction (sector observed, data not public at freeze)
  2004 2461238.31892 2026-07-16 19:31    1.40000          106 prediction (sector observed, data not public at freeze)
  2005 2461239.40459 2026-07-17 21:35    1.40000          106 prediction (sector observed, data not public at freeze)
  2006 2461240.49026 2026-07-18 23:38    1.40000          106 prediction (sector observed, data not public at freeze)
  2007 2461241.57593 2026-07-20 01:41    1.40000          106 prediction (sector observed, data not public at freeze)
  2008 2461242.66160 2026-07-21 03:44    1.40000          106 prediction (sector observed, data not public at freeze)
  2009 2461243.74727 2026-07-22 05:48    1.40000          106 prediction (sector observed, data not public at freeze)
  2010 2461244.83294 2026-07-23 07:51    1.40000          106 prediction (sector observed, data not public at freeze)
  2011 2461245.91861 2026-07-24 09:54    1.40000          106 prediction (sector observed, data not public at freeze)
  2012 2461247.00428 2026-07-25 11:58    1.40000          106 prediction (sector observed, data not public at freeze)
  2013 2461248.08995 2026-07-26 14:01    1.40000          106 prediction (sector observed, data not public at freeze)
  2014 2461249.17562 2026-07-27 16:04    1.40000          106 prediction (sector observed, data not public at freeze)
  2015 2461250.26129 2026-07-28 18:08    1.40000          106 prediction (sector observed, data not public at freeze)
  2016 2461251.34696 2026-07-29 20:11    1.40000          106 prediction (sector observed, data not public at freeze)
  2017 2461252.43263 2026-07-30 22:14    1.40000          106 prediction (sector observed, data not public at freeze)
  2018 2461253.51830 2026-08-01 00:18    1.40000          106 prediction (sector observed, data not public at freeze)
  2019 2461254.60398 2026-08-02 02:21    1.40000          106 prediction (sector observed, data not public at freeze)
  2020 2461255.68965 2026-08-03 04:24    1.40000          106 prediction (sector observed, data not public at freeze)
  2021 2461256.77532 2026-08-04 06:27    1.40000          106 prediction (sector observed, data not public at freeze)
  2022 2461257.86099 2026-08-05 08:31    1.40000          106 prediction (sector observed, data not public at freeze)
  2023 2461258.94666 2026-08-06 10:34    1.40000          106 prediction (sector observed, data not public at freeze)
  2024 2461260.03233 2026-08-07 12:37    1.40000          106 prediction (sector observed, data not public at freeze)
  2025 2461261.11800 2026-08-08 14:41    1.40000          106 prediction (sector observed, data not public at freeze)
Outcomes defined in advance (QLP or SPOC light curve of the test sector, or a TESScut fixed-aperture extraction, transit-masked biweight detrend): (1) recovered - a box of depth 0.5-1.5x and duration 0.7-1.3x the reference values within +-3 sigma_min (and in any case within +-30 min) of >= 2 predicted times, stacked SNR >= 5; (2) inconsistent - a comparable dip exists but its times differ by > 30 min from every prediction; (3) excluded - stacked depth at the predicted phase < 0.3x at 3 sigma with >= 2 transits fully covered; (4) insufficient - fewer than 2 predicted transits covered. No QLP S99+ sector time enters this ephemeris. Generated by scripts/prereg_v2.py 206620592 --freeze --version 2.


**Addendum 2026-10-20 (timing rule):** the phrase "and in any case within +-30 min" above misstates the rule. The governing rule is the public protocol's (Zenodo 10.5281/zenodo.23462442): stacked timing offset within max(3 sigma_pred, 30 min), as implemented in the frozen evaluator scripts/prereg_test.py. No prediction, CSV or checksum is changed. See CLARIFICATION_TIMING_RULE_2026-10-20.md.


**Erratum 2026-10-20 (data availability):** the status "data not public at freeze" above is incorrect. This sector had already been observed and public data products existed at the freeze (product-specific; target QLP light curves were not yet released). The authors attest that the target-sector photometry was not examined before the freeze. Read the status as "sector already observed; public data existed; authors attest target-sector photometry not examined before freeze". See ERRATUM_S106_DATA_AVAILABILITY_2026-10-20.md. Prediction CSV bytes and hashes are unchanged.


**Amendment 2026-10-20 (scoring procedure fixed before any S106 photometry is examined):** this test will be scored with the conformance procedure conformance-v2.1 (conformance_v2.1/scripts/prereg_conformance.py, SHA-256 a864b07ace8d3220a2d94a60513a488c8a5d87b54f41ebf510ff40ef1755311f) and the locked configuration conformance_v2.1/configs/conformance/206620592_S106.json (SHA-256 56a1f68b16ec2b1e84a7a13f9c958edf734f1feb8ff40b287e163f0569f6135e): product QLP SAP_FLUX, reference depth 287.0 ppm, T14 1.0 h, timing gate max(3 sigma_min, 30 min) from the hashed CSV above. Its outcome under max() is the outcome of record; the min() reading, the per-event min() assessment and the frozen evaluator's (conformance_v2.1/scripts/prereg_test.py) literal output are reported next to it. The procedure replaces the per-event depth/duration matching wording above with a joint fit plus per-transit checks, removes cadences within 1.5 d after a data resume and 0.5 d before a gap (an author-selected edge rule), requires full transit coverage, and scores only the first QLP release (v01). RECOVERED means compatibility with the procedure's common-box and parity-split rule; it does not show that each transit meets the original timing and duration limits. Which document governs each item, and every departure from the protocol, is listed in conformance_v2.1/GOVERNANCE_S106_TESTS_2026-10-20.md. Stated in advance (conditional on in-sample noise and gap templates, not outcome probabilities): 13-20 eligible events expected (median expected joint SNR 5.5); holdout on-time RECOVERED 11/40. A decisive outcome is uncertain. Prediction CSV bytes and hashes are unchanged.
