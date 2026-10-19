# Pre-registered transit predictions v2 - TIC 332709057
Frozen: 2026-10-19 12:51:30 UTC. Author: Fernando Molina (Independent researcher, ORCID 0009-0002-2872-3406). Analysis with Claude (Anthropic) under the author's direction.
First freeze for this object (v2 tooling: all-sector ephemeris). Reason (external review 2026-10-18,
results/external_review_allsky/REVIEW.md): v1 timed only the 200-s sectors (vet.py min_pts cut), ignoring 2018-2021 data; v2 fits one time offset per
sector from ALL sectors (raw SAP flux, cadence-aware model, local baselines; SPOC 2-min sectors where they exist) on top of the all-data BLS ephemeris.
Ephemeris: T0 = BTJD 3962.20995 +- 3.2 min (epoch 203), P = 12.562981 +- 0.000076 d (chi2/dof 3.2/1, inflation x1.80); all-data BLS P = 12.562981.
Sector times used: S4 QLP SAP (1 ev, O-C -13.7 +- 7.8 min), S97 QLP SAP (3 ev, O-C +0.7 +- 1.8 min).
Depth per sector (fixed shape, local baseline, raw SAP): S4 1657, S97 602 ppm.
Round-2 object with no TESS coverage through Sector 134; ground-based ephemeris test only. See results/allsky_classA_round2_outcomes.csv for vetting status (marginal/weak/rediscovery as listed).
SHA-256 of predicted_transits_2026_2027_v2.csv: 32afcd7e3e1cf1d99f6a04add84de602d32c22eb9bbb1712469ba6d36c2a53e8
**Test of record: next TESS sector(s).** Predicted mid-transits (conservative window +-20 min):
 epoch   tc_bjd_tdb              utc  sigma_min         tess_sector     status
   233 2.461339e+06 2026-10-25 14:13        4.6 none (ground-based) prediction
   234 2.461352e+06 2026-11-07 03:44        4.6 none (ground-based) prediction
   235 2.461364e+06 2026-11-19 17:16        4.7 none (ground-based) prediction
   236 2.461377e+06 2026-12-02 06:47        4.8 none (ground-based) prediction
   237 2.461389e+06 2026-12-14 20:19        4.9 none (ground-based) prediction
   238 2.461402e+06 2026-12-27 09:52        5.0 none (ground-based) prediction
   239 2.461414e+06 2027-01-08 23:24        5.1 none (ground-based) prediction
   240 2.461427e+06 2027-01-21 12:57        5.1 none (ground-based) prediction
   241 2.461440e+06 2027-02-03 02:29        5.2 none (ground-based) prediction
   242 2.461452e+06 2027-02-15 16:01        5.3 none (ground-based) prediction
   243 2.461465e+06 2027-02-28 05:33        5.4 none (ground-based) prediction
   244 2.461477e+06 2027-03-12 19:05        5.5 none (ground-based) prediction
   245 2.461490e+06 2027-03-25 08:37        5.6 none (ground-based) prediction
   246 2.461502e+06 2027-04-06 22:08        5.7 none (ground-based) prediction
   247 2.461515e+06 2027-04-19 11:39        5.8 none (ground-based) prediction
   248 2.461528e+06 2027-05-02 01:10        5.9 none (ground-based) prediction
   249 2.461540e+06 2027-05-14 14:40        6.0 none (ground-based) prediction
   250 2.461553e+06 2027-05-27 04:10        6.0 none (ground-based) prediction
   251 2.461565e+06 2027-06-08 17:39        6.1 none (ground-based) prediction
   252 2.461578e+06 2027-06-21 07:09        6.2 none (ground-based) prediction
   253 2.461590e+06 2027-07-03 20:38        6.3 none (ground-based) prediction
   254 2.461603e+06 2027-07-16 10:07        6.4 none (ground-based) prediction
   255 2.461615e+06 2027-07-28 23:36        6.5 none (ground-based) prediction
   256 2.461628e+06 2027-08-10 13:05        6.6 none (ground-based) prediction
   257 2.461641e+06 2027-08-23 02:34        6.7 none (ground-based) prediction
   258 2.461653e+06 2027-09-04 16:03        6.8 none (ground-based) prediction
   259 2.461666e+06 2027-09-17 05:33        6.9 none (ground-based) prediction
   260 2.461678e+06 2027-09-29 19:03        7.0 none (ground-based) prediction
   261 2.461691e+06 2027-10-12 08:33        7.1 none (ground-based) prediction
   262 2.461703e+06 2027-10-24 22:04        7.2 none (ground-based) prediction
   263 2.461716e+06 2027-11-06 11:34        7.3 none (ground-based) prediction
   264 2.461729e+06 2027-11-19 01:06        7.4 none (ground-based) prediction
   265 2.461741e+06 2027-12-01 14:37        7.5 none (ground-based) prediction
   266 2.461754e+06 2027-12-14 04:09        7.6 none (ground-based) prediction
   267 2.461766e+06 2027-12-26 17:42        7.7 none (ground-based) prediction
   268 2.461779e+06 2028-01-08 07:14        7.8 none (ground-based) prediction
   269 2.461791e+06 2028-01-20 20:46        7.9 none (ground-based) prediction
   270 2.461804e+06 2028-02-02 10:19        8.0 none (ground-based) prediction
   271 2.461816e+06 2028-02-14 23:51        8.1 none (ground-based) prediction
   272 2.461829e+06 2028-02-27 13:23        8.2 none (ground-based) prediction
   273 2.461842e+06 2028-03-11 02:55        8.3 none (ground-based) prediction
   274 2.461854e+06 2028-03-23 16:27        8.4 none (ground-based) prediction
   275 2.461867e+06 2028-04-05 05:58        8.5 none (ground-based) prediction
   276 2.461879e+06 2028-04-17 19:29        8.6 none (ground-based) prediction
   277 2.461892e+06 2028-04-30 09:00        8.7 none (ground-based) prediction
Outcomes defined in advance (QLP or SPOC light curve of the test sector, or a TESScut fixed-aperture extraction, transit-masked biweight detrend): (1) recovered - a box of
depth 0.5-1.5x and duration 0.7-1.3x the values above within +-3 sigma_min (and in any case within +-30 min) of >= 2 predicted times, stacked SNR >= 5;
(2) inconsistent - a comparable dip exists but its times differ by > 30 min from every prediction; (3) excluded - stacked depth at the predicted phase
< 0.3x at 3 sigma with >= 2 transits fully covered; (4) insufficient - fewer than 2 predicted transits covered. The QLP S99-S105 timestamp error shifts
these ephemerides by < 1.5 min (review, timing_propagation.json). Generated by scripts/prereg_v2.py 332709057 --freeze.
