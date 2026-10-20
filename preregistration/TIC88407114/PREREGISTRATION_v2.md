# Pre-registered transit predictions v2 - TIC 88407114
Frozen: 2026-10-20 00:44:14 UTC. Author: Fernando Molina (Independent researcher, ORCID 0009-0002-2872-3406). Analysis with Claude (Anthropic) under the author's direction.
First freeze for this object (v2 tooling: all-sector ephemeris). Reason (external review 2026-10-18,
results/external_review_allsky/REVIEW.md): v1 timed only the 200-s sectors (vet.py min_pts cut), ignoring 2018-2021 data; v2 fits one time offset per
sector from ALL sectors (raw SAP flux, cadence-aware model, local baselines; SPOC 2-min sectors where they exist) on top of the all-data BLS ephemeris.
Ephemeris: T0 = BTJD 4246.43040 +- 4.4 min (epoch 1893), P = 1.497514 +- 0.000003 d (chi2/dof 17.4/3, inflation x2.41); all-data BLS P = 1.497527.
Sector times used: S4 SPOC 2-min (14 ev, O-C -17.1 +- 6.0 min), S31 SPOC 2-min (16 ev, O-C +2.0 +- 1.8 min), S97 QLP SAP (27 ev, O-C +0.3 +- 1.8 min), S105 SPOC 2-min (13 ev, O-C -28.7 +- 10.2 min), S106 SPOC 2-min (13 ev, O-C +0.4 +- 4.2 min).
Depth per sector (fixed shape, local baseline, raw SAP): S4 234, S31 264, S97 203, S105 159, S106 180 ppm.
Round-3 object, independent rediscovery: listed in killercatfish/tess-hunt (P 1.4975 d). Weak (SNR 8.4; ~180 ppm). On target. Test: Sector 106 (observed, data not public at freeze).
Reference values for the outcome clauses: depth 158 ppm (raw SAP, all sectors), T14 1.50 h.
SHA-256 of predicted_transits_2026_2027_v2.csv: 751ec316080ae4a6e9de8840f92a3f332e4dfb2b1aeb5be9bf3fa088dc9163f6
**Test of record: next TESS sector(s).** Predicted mid-transits (sigma_min = 1-sigma timing uncertainty at that epoch):
 epoch    tc_bjd_tdb              utc  sigma_min tess_sector                                                  status
  1894 2461247.92792 2026-07-26 10:15    4.40000   106 (gap) prediction (sector observed, data not public at freeze)
  1895 2461249.42543 2026-07-27 22:11    4.40000         106 prediction (sector observed, data not public at freeze)
  1896 2461250.92294 2026-07-29 10:07    4.40000         106 prediction (sector observed, data not public at freeze)
  1897 2461252.42046 2026-07-30 22:03    4.40000         106 prediction (sector observed, data not public at freeze)
  1898 2461253.91797 2026-08-01 10:00    4.40000         106 prediction (sector observed, data not public at freeze)
  1899 2461255.41548 2026-08-02 21:56    4.40000         106 prediction (sector observed, data not public at freeze)
  1900 2461256.91300 2026-08-04 09:52    4.40000         106 prediction (sector observed, data not public at freeze)
  1901 2461258.41051 2026-08-05 21:48    4.40000         106 prediction (sector observed, data not public at freeze)
  1902 2461259.90803 2026-08-07 09:45    4.40000         106 prediction (sector observed, data not public at freeze)
  1903 2461261.40554 2026-08-08 21:41    4.40000         106 prediction (sector observed, data not public at freeze)
  1904 2461262.90305 2026-08-10 09:37    4.40000         107 prediction (sector observed, data not public at freeze)
  1905 2461264.40057 2026-08-11 21:33    4.40000         107 prediction (sector observed, data not public at freeze)
  1906 2461265.89808 2026-08-13 09:30    4.50000         107 prediction (sector observed, data not public at freeze)
  1907 2461267.39559 2026-08-14 21:26    4.50000         107 prediction (sector observed, data not public at freeze)
  1908 2461268.89311 2026-08-16 09:22    4.50000         107 prediction (sector observed, data not public at freeze)
  1909 2461270.39062 2026-08-17 21:19    4.50000         107 prediction (sector observed, data not public at freeze)
  1910 2461271.88813 2026-08-19 09:15    4.50000         107 prediction (sector observed, data not public at freeze)
  1911 2461273.38565 2026-08-20 21:11    4.50000         107 prediction (sector observed, data not public at freeze)
  1912 2461274.88316 2026-08-22 09:07    4.50000         107 prediction (sector observed, data not public at freeze)
  1913 2461276.38067 2026-08-23 21:04    4.50000   107 (gap) prediction (sector observed, data not public at freeze)
  1914 2461277.87819 2026-08-25 09:00    4.50000         107 prediction (sector observed, data not public at freeze)
  1915 2461279.37570 2026-08-26 20:56    4.50000         107 prediction (sector observed, data not public at freeze)
  1916 2461280.87322 2026-08-28 08:52    4.50000         107 prediction (sector observed, data not public at freeze)
  1917 2461282.37073 2026-08-29 20:49    4.50000         107 prediction (sector observed, data not public at freeze)
  1918 2461283.86824 2026-08-31 08:45    4.50000         107 prediction (sector observed, data not public at freeze)
  1919 2461285.36576 2026-09-01 20:41    4.50000         107 prediction (sector observed, data not public at freeze)
  1920 2461286.86327 2026-09-03 08:38    4.50000         107 prediction (sector observed, data not public at freeze)
  1921 2461288.36078 2026-09-04 20:34    4.50000         107 prediction (sector observed, data not public at freeze)
  1922 2461289.85830 2026-09-06 08:30    4.50000         107 prediction (sector observed, data not public at freeze)
Outcomes defined in advance (QLP or SPOC light curve of the test sector, or a TESScut fixed-aperture extraction, transit-masked biweight detrend): (1) recovered - a box of depth 0.5-1.5x and duration 0.7-1.3x the reference values within +-3 sigma_min (and in any case within +-30 min) of >= 2 predicted times, stacked SNR >= 5; (2) inconsistent - a comparable dip exists but its times differ by > 30 min from every prediction; (3) excluded - stacked depth at the predicted phase < 0.3x at 3 sigma with >= 2 transits fully covered; (4) insufficient - fewer than 2 predicted transits covered. No QLP S99+ sector time enters this ephemeris. Generated by scripts/prereg_v2.py 88407114 --freeze --version 2.


**Addendum 2026-10-20 (timing rule):** the phrase "and in any case within +-30 min" above misstates the rule. The governing rule is the public protocol's (Zenodo 10.5281/zenodo.23462442): stacked timing offset within max(3 sigma_pred, 30 min), as implemented in the frozen evaluator scripts/prereg_test.py. No prediction, CSV or checksum is changed. See CLARIFICATION_TIMING_RULE_2026-10-20.md.


**Erratum 2026-10-20 (data availability):** the status "data not public at freeze" above is incorrect. This sector had already been observed and public data products existed at the freeze (product-specific; target QLP light curves were not yet released). The authors attest that the target-sector photometry was not examined before the freeze. Read the status as "sector already observed; public data existed; authors attest target-sector photometry not examined before freeze". See ERRATUM_S106_DATA_AVAILABILITY_2026-10-20.md. Prediction CSV bytes and hashes are unchanged.


**Withdrawal 2026-10-20:** the Sector 106 test of this registration is WITHDRAWN. The frozen ephemeris fitted S106 SPOC 2-minute photometry (the freeze script downloaded every available 2-minute sector), so S106 cannot be an out-of-sample test. Files and hashes are retained unchanged. See ERRATUM_S106_DATA_AVAILABILITY_2026-10-20.md.
