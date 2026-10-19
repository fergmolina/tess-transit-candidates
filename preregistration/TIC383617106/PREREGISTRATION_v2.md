# Pre-registered transit predictions v2 - TIC 383617106
Frozen: 2026-10-19 12:47:16 UTC. Author: Fernando Molina (Independent researcher, ORCID 0009-0002-2872-3406). Analysis with Claude (Anthropic) under the author's direction.
First freeze for this object (v2 tooling: all-sector ephemeris). Reason (external review 2026-10-18,
results/external_review_allsky/REVIEW.md): v1 timed only the 200-s sectors (vet.py min_pts cut), ignoring 2018-2021 data; v2 fits one time offset per
sector from ALL sectors (raw SAP flux, cadence-aware model, local baselines; SPOC 2-min sectors where they exist) on top of the all-data BLS ephemeris.
Ephemeris: T0 = BTJD 3871.54023 +- 3.9 min (epoch 236), P = 9.499158 +- 0.000034 d (chi2/dof 3.3/3, inflation x1.06); all-data BLS P = 9.499194.
Sector times used: S12 QLP SAP (1 ev, O-C -20.0 +- 21.6 min), S39 QLP SAP (2 ev, O-C -1.7 +- 9.0 min), S65 QLP SAP (2 ev, O-C +0.9 +- 2.4 min), S93 QLP SAP (2 ev, O-C +3.8 +- 5.4 min), S94 QLP SAP (2 ev, O-C -8.1 +- 6.0 min).
Depth per sector (fixed shape, local baseline, raw SAP): S12 866, S39 1109, S65 1188, S93 1080, S94 774 ppm.
Round-2 object with no TESS coverage through Sector 134; ground-based ephemeris test only. See results/allsky_classA_round2_outcomes.csv for vetting status (marginal/weak/rediscovery as listed).
SHA-256 of predicted_transits_2026_2027_v2.csv: edf4f0ef127158b2d6282c48d4fcb5f76c8e8e46b78ee86ba9275d807a77738d
**Test of record: next TESS sector(s).** Predicted mid-transits (conservative window +-20 min):
 epoch   tc_bjd_tdb              utc  sigma_min         tess_sector     status
   285 2.461337e+06 2026-10-23 11:59        6.1 none (ground-based) prediction
   286 2.461346e+06 2026-11-01 23:58        6.1 none (ground-based) prediction
   287 2.461356e+06 2026-11-11 11:57        6.2 none (ground-based) prediction
   288 2.461365e+06 2026-11-20 23:56        6.2 none (ground-based) prediction
   289 2.461375e+06 2026-11-30 11:55        6.3 none (ground-based) prediction
   290 2.461384e+06 2026-12-09 23:54        6.3 none (ground-based) prediction
   291 2.461394e+06 2026-12-19 11:53        6.4 none (ground-based) prediction
   292 2.461403e+06 2026-12-28 23:52        6.4 none (ground-based) prediction
   293 2.461413e+06 2027-01-07 11:50        6.4 none (ground-based) prediction
   294 2.461422e+06 2027-01-16 23:49        6.5 none (ground-based) prediction
   295 2.461432e+06 2027-01-26 11:47        6.5 none (ground-based) prediction
   296 2.461441e+06 2027-02-04 23:46        6.6 none (ground-based) prediction
   297 2.461451e+06 2027-02-14 11:44        6.6 none (ground-based) prediction
   298 2.461460e+06 2027-02-23 23:42        6.7 none (ground-based) prediction
   299 2.461470e+06 2027-03-05 11:40        6.7 none (ground-based) prediction
   300 2.461479e+06 2027-03-14 23:39        6.8 none (ground-based) prediction
   301 2.461489e+06 2027-03-24 11:37        6.8 none (ground-based) prediction
   302 2.461498e+06 2027-04-02 23:35        6.9 none (ground-based) prediction
   303 2.461508e+06 2027-04-12 11:33        6.9 none (ground-based) prediction
   304 2.461517e+06 2027-04-21 23:32        7.0 none (ground-based) prediction
   305 2.461527e+06 2027-05-01 11:30        7.0 none (ground-based) prediction
   306 2.461536e+06 2027-05-10 23:28        7.0 none (ground-based) prediction
   307 2.461546e+06 2027-05-20 11:27        7.1 none (ground-based) prediction
   308 2.461555e+06 2027-05-29 23:26        7.1 none (ground-based) prediction
   309 2.461565e+06 2027-06-08 11:24        7.2 none (ground-based) prediction
   310 2.461574e+06 2027-06-17 23:23        7.2 none (ground-based) prediction
   311 2.461584e+06 2027-06-27 11:22        7.3 none (ground-based) prediction
   312 2.461593e+06 2027-07-06 23:21        7.3 none (ground-based) prediction
   313 2.461603e+06 2027-07-16 11:20        7.4 none (ground-based) prediction
   314 2.461612e+06 2027-07-25 23:19        7.4 none (ground-based) prediction
   315 2.461622e+06 2027-08-04 11:18        7.5 none (ground-based) prediction
   316 2.461631e+06 2027-08-13 23:17        7.5 none (ground-based) prediction
   317 2.461641e+06 2027-08-23 11:17        7.6 none (ground-based) prediction
   318 2.461650e+06 2027-09-01 23:16        7.6 none (ground-based) prediction
   319 2.461660e+06 2027-09-11 11:15        7.7 none (ground-based) prediction
   320 2.461669e+06 2027-09-20 23:15        7.7 none (ground-based) prediction
   321 2.461679e+06 2027-09-30 11:14        7.7 none (ground-based) prediction
   322 2.461688e+06 2027-10-09 23:13        7.8 none (ground-based) prediction
   323 2.461698e+06 2027-10-19 11:13        7.8 none (ground-based) prediction
   324 2.461707e+06 2027-10-28 23:12        7.9 none (ground-based) prediction
   325 2.461717e+06 2027-11-07 11:11        7.9 none (ground-based) prediction
   326 2.461726e+06 2027-11-16 23:10        8.0 none (ground-based) prediction
   327 2.461736e+06 2027-11-26 11:09        8.0 none (ground-based) prediction
   328 2.461745e+06 2027-12-05 23:08        8.1 none (ground-based) prediction
   329 2.461755e+06 2027-12-15 11:07        8.1 none (ground-based) prediction
   330 2.461764e+06 2027-12-24 23:06        8.2 none (ground-based) prediction
   331 2.461774e+06 2028-01-03 11:04        8.2 none (ground-based) prediction
   332 2.461783e+06 2028-01-12 23:03        8.3 none (ground-based) prediction
   333 2.461793e+06 2028-01-22 11:01        8.3 none (ground-based) prediction
   334 2.461802e+06 2028-01-31 23:00        8.4 none (ground-based) prediction
   335 2.461812e+06 2028-02-10 10:58        8.4 none (ground-based) prediction
   336 2.461821e+06 2028-02-19 22:56        8.5 none (ground-based) prediction
   337 2.461831e+06 2028-02-29 10:55        8.5 none (ground-based) prediction
   338 2.461840e+06 2028-03-09 22:53        8.5 none (ground-based) prediction
   339 2.461850e+06 2028-03-19 10:51        8.6 none (ground-based) prediction
   340 2.461859e+06 2028-03-28 22:49        8.6 none (ground-based) prediction
   341 2.461869e+06 2028-04-07 10:48        8.7 none (ground-based) prediction
   342 2.461878e+06 2028-04-16 22:46        8.7 none (ground-based) prediction
   343 2.461888e+06 2028-04-26 10:44        8.8 none (ground-based) prediction
   344 2.461897e+06 2028-05-05 22:43        8.8 none (ground-based) prediction
Outcomes defined in advance (QLP or SPOC light curve of the test sector, or a TESScut fixed-aperture extraction, transit-masked biweight detrend): (1) recovered - a box of
depth 0.5-1.5x and duration 0.7-1.3x the values above within +-3 sigma_min (and in any case within +-30 min) of >= 2 predicted times, stacked SNR >= 5;
(2) inconsistent - a comparable dip exists but its times differ by > 30 min from every prediction; (3) excluded - stacked depth at the predicted phase
< 0.3x at 3 sigma with >= 2 transits fully covered; (4) insufficient - fewer than 2 predicted transits covered. The QLP S99-S105 timestamp error shifts
these ephemerides by < 1.5 min (review, timing_propagation.json). Generated by scripts/prereg_v2.py 383617106 --freeze.
