# Pre-registered transit predictions v2 - TIC 333661705
Frozen: 2026-10-20 00:44:26 UTC. Author: Fernando Molina (Independent researcher, ORCID 0009-0002-2872-3406). Analysis with Claude (Anthropic) under the author's direction.
First freeze for this object (v2 tooling: all-sector ephemeris). Reason (external review 2026-10-18,
results/external_review_allsky/REVIEW.md): v1 timed only the 200-s sectors (vet.py min_pts cut), ignoring 2018-2021 data; v2 fits one time offset per
sector from ALL sectors (raw SAP flux, cadence-aware model, local baselines; SPOC 2-min sectors where they exist) on top of the all-data BLS ephemeris.
Ephemeris: T0 = BTJD 4113.01126 +- 2.3 min (epoch 1836), P = 1.383225 +- 0.000003 d (chi2/dof 9.5/3, inflation x1.78); all-data BLS P = 1.383225.
Sector times used: S37 QLP SAP (16 ev, O-C -2.4 +- 3.0 min), S64 QLP SAP (18 ev, O-C +5.6 +- 3.6 min), S99 QLP SAP (12 ev, O-C -1.0 +- 2.4 min), S100 QLP SAP (15 ev, O-C +6.5 +- 3.0 min), S101 QLP SAP (14 ev, O-C -2.3 +- 1.8 min).
Depth per sector (fixed shape, local baseline, raw SAP): S37 679, S64 779, S99 813, S100 552, S101 605 ppm.
Round-3 object, independent rediscovery: listed by brahle (tic-333661705-s01, assessed 2026-10-11). P 1.383 d, ~700 ppm, ~2.2 R_E; triage pass. On target. Test: Sector 111.
Reference values for the outcome clauses: depth 705 ppm (raw SAP, all sectors), T14 1.10 h.
SHA-256 of predicted_transits_2026_2027_v2.csv: e7752bf76ab70b924362d09f957bf2df2e541f34fc19e29d6a44a1f7ff177872
**Test of record: next TESS sector(s).** Predicted mid-transits (sigma_min = 1-sigma timing uncertainty at that epoch):
 epoch    tc_bjd_tdb              utc  sigma_min                  tess_sector     status
  2023 2461371.67440 2026-11-27 04:14    2.80000                          111 prediction
  2024 2461373.05763 2026-11-28 13:26    2.80000                          111 prediction
  2025 2461374.44085 2026-11-29 22:38    2.80000                          111 prediction
  2026 2461375.82408 2026-12-01 07:49    2.80000                          111 prediction
  2027 2461377.20730 2026-12-02 17:01    2.80000                          111 prediction
  2028 2461378.59053 2026-12-04 02:13    2.80000                          111 prediction
  2029 2461379.97375 2026-12-05 11:25    2.80000                          111 prediction
  2030 2461381.35698 2026-12-06 20:36    2.80000                          111 prediction
  2031 2461382.74020 2026-12-08 05:48    2.80000                          111 prediction
  2032 2461384.12343 2026-12-09 15:00    2.80000 111 (span only, gap unknown) prediction
  2033 2461385.50665 2026-12-11 00:12    2.80000 111 (span only, gap unknown) prediction
  2034 2461386.88988 2026-12-12 09:23    2.80000 111 (span only, gap unknown) prediction
  2035 2461388.27310 2026-12-13 18:35    2.80000 111 (span only, gap unknown) prediction
  2036 2461389.65633 2026-12-15 03:47    2.80000 111 (span only, gap unknown) prediction
  2037 2461391.03955 2026-12-16 12:58    2.90000 111 (span only, gap unknown) prediction
  2038 2461392.42278 2026-12-17 22:10    2.90000 111 (span only, gap unknown) prediction
  2039 2461393.80601 2026-12-19 07:22    2.90000 111 (span only, gap unknown) prediction
  2040 2461395.18923 2026-12-20 16:34    2.90000 111 (span only, gap unknown) prediction
  2041 2461396.57246 2026-12-22 01:45    2.90000 111 (span only, gap unknown) prediction
  2042 2461397.95568 2026-12-23 10:57    2.90000 112 (span only, gap unknown) prediction
  2043 2461399.33891 2026-12-24 20:09    2.90000 112 (span only, gap unknown) prediction
  2044 2461400.72213 2026-12-26 05:20    2.90000 112 (span only, gap unknown) prediction
  2045 2461402.10536 2026-12-27 14:32    2.90000 112 (span only, gap unknown) prediction
  2046 2461403.48858 2026-12-28 23:44    2.90000 112 (span only, gap unknown) prediction
  2047 2461404.87181 2026-12-30 08:56    2.90000 112 (span only, gap unknown) prediction
  2048 2461406.25503 2026-12-31 18:07    2.90000 112 (span only, gap unknown) prediction
  2049 2461407.63826 2027-01-02 03:19    2.90000 112 (span only, gap unknown) prediction
  2050 2461409.02148 2027-01-03 12:31    2.90000 112 (span only, gap unknown) prediction
  2051 2461410.40471 2027-01-04 21:42    2.90000 112 (span only, gap unknown) prediction
  2052 2461411.78793 2027-01-06 06:54    2.90000 112 (span only, gap unknown) prediction
  2053 2461413.17116 2027-01-07 16:06    2.90000 112 (span only, gap unknown) prediction
  2054 2461414.55439 2027-01-09 01:18    2.90000 112 (span only, gap unknown) prediction
  2055 2461415.93761 2027-01-10 10:29    2.90000 112 (span only, gap unknown) prediction
  2056 2461417.32084 2027-01-11 19:41    2.90000 112 (span only, gap unknown) prediction
  2057 2461418.70406 2027-01-13 04:53    2.90000 112 (span only, gap unknown) prediction
  2058 2461420.08729 2027-01-14 14:04    2.90000 112 (span only, gap unknown) prediction
  2059 2461421.47051 2027-01-15 23:16    2.90000 112 (span only, gap unknown) prediction
  2060 2461422.85374 2027-01-17 08:28    2.90000 112 (span only, gap unknown) prediction
  2061 2461424.23696 2027-01-18 17:39    2.90000 113 (span only, gap unknown) prediction
  2062 2461425.62019 2027-01-20 02:51    2.90000 113 (span only, gap unknown) prediction
  2063 2461427.00341 2027-01-21 12:03    2.90000 113 (span only, gap unknown) prediction
  2064 2461428.38664 2027-01-22 21:15    2.90000 113 (span only, gap unknown) prediction
  2065 2461429.76986 2027-01-24 06:26    2.90000 113 (span only, gap unknown) prediction
  2066 2461431.15309 2027-01-25 15:38    2.90000 113 (span only, gap unknown) prediction
  2067 2461432.53631 2027-01-27 00:50    2.90000 113 (span only, gap unknown) prediction
  2068 2461433.91954 2027-01-28 10:01    2.90000 113 (span only, gap unknown) prediction
  2069 2461435.30277 2027-01-29 19:13    2.90000 113 (span only, gap unknown) prediction
  2070 2461436.68599 2027-01-31 04:25    3.00000 113 (span only, gap unknown) prediction
  2071 2461438.06922 2027-02-01 13:36    3.00000 113 (span only, gap unknown) prediction
  2072 2461439.45244 2027-02-02 22:48    3.00000 113 (span only, gap unknown) prediction
  2073 2461440.83567 2027-02-04 08:00    3.00000 113 (span only, gap unknown) prediction
  2074 2461442.21889 2027-02-05 17:12    3.00000 113 (span only, gap unknown) prediction
  2075 2461443.60212 2027-02-07 02:23    3.00000 113 (span only, gap unknown) prediction
  2076 2461444.98534 2027-02-08 11:35    3.00000 113 (span only, gap unknown) prediction
  2077 2461446.36857 2027-02-09 20:47    3.00000 113 (span only, gap unknown) prediction
  2078 2461447.75179 2027-02-11 05:58    3.00000 113 (span only, gap unknown) prediction
  2079 2461449.13502 2027-02-12 15:10    3.00000 113 (span only, gap unknown) prediction
  2080 2461450.51824 2027-02-14 00:22    3.00000 114 (span only, gap unknown) prediction
  2081 2461451.90147 2027-02-15 09:34    3.00000 114 (span only, gap unknown) prediction
  2082 2461453.28469 2027-02-16 18:45    3.00000 114 (span only, gap unknown) prediction
  2083 2461454.66792 2027-02-18 03:57    3.00000 114 (span only, gap unknown) prediction
  2084 2461456.05115 2027-02-19 13:09    3.00000 114 (span only, gap unknown) prediction
  2085 2461457.43437 2027-02-20 22:20    3.00000 114 (span only, gap unknown) prediction
  2086 2461458.81760 2027-02-22 07:32    3.00000 114 (span only, gap unknown) prediction
  2087 2461460.20082 2027-02-23 16:44    3.00000 114 (span only, gap unknown) prediction
  2088 2461461.58405 2027-02-25 01:56    3.00000 114 (span only, gap unknown) prediction
  2089 2461462.96727 2027-02-26 11:07    3.00000 114 (span only, gap unknown) prediction
  2090 2461464.35050 2027-02-27 20:19    3.00000 114 (span only, gap unknown) prediction
  2091 2461465.73372 2027-03-01 05:31    3.00000 114 (span only, gap unknown) prediction
  2092 2461467.11695 2027-03-02 14:43    3.00000 114 (span only, gap unknown) prediction
  2093 2461468.50017 2027-03-03 23:54    3.00000 114 (span only, gap unknown) prediction
  2094 2461469.88340 2027-03-05 09:06    3.00000 114 (span only, gap unknown) prediction
  2095 2461471.26662 2027-03-06 18:18    3.00000 114 (span only, gap unknown) prediction
  2096 2461472.64985 2027-03-08 03:30    3.00000 114 (span only, gap unknown) prediction
  2097 2461474.03308 2027-03-09 12:41    3.00000 114 (span only, gap unknown) prediction
  2098 2461475.41630 2027-03-10 21:53    3.00000 114 (span only, gap unknown) prediction
  2099 2461476.79953 2027-03-12 07:05    3.00000 114 (span only, gap unknown) prediction
  2100 2461478.18275 2027-03-13 16:17    3.00000 114 (span only, gap unknown) prediction
Outcomes defined in advance (QLP or SPOC light curve of the test sector, or a TESScut fixed-aperture extraction, transit-masked biweight detrend): (1) recovered - a box of depth 0.5-1.5x and duration 0.7-1.3x the reference values within +-3 sigma_min (and in any case within +-30 min) of >= 2 predicted times, stacked SNR >= 5; (2) inconsistent - a comparable dip exists but its times differ by > 30 min from every prediction; (3) excluded - stacked depth at the predicted phase < 0.3x at 3 sigma with >= 2 transits fully covered; (4) insufficient - fewer than 2 predicted transits covered. QLP S99+ sector times were corrected for the barycentric timestamp error before the fit (results/qlp_clock_v2/; corrections in min: {99: -0.01, 100: 1.43, 101: 3.46}). Generated by scripts/prereg_v2.py 333661705 --freeze --version 2.


**Addendum 2026-10-20 (timing rule):** the phrase "and in any case within +-30 min" above misstates the rule. The governing rule is the public protocol's (Zenodo 10.5281/zenodo.23462442): stacked timing offset within max(3 sigma_pred, 30 min), as implemented in the frozen evaluator scripts/prereg_test.py. No prediction, CSV or checksum is changed. See CLARIFICATION_TIMING_RULE_2026-10-20.md.
