# Pre-registered transit predictions v2 - TIC 371421714
Frozen: 2026-10-19 12:51:35 UTC. Author: Fernando Molina (Independent researcher, ORCID 0009-0002-2872-3406). Analysis with Claude (Anthropic) under the author's direction.
First freeze for this object (v2 tooling: all-sector ephemeris). Reason (external review 2026-10-18,
results/external_review_allsky/REVIEW.md): v1 timed only the 200-s sectors (vet.py min_pts cut), ignoring 2018-2021 data; v2 fits one time offset per
sector from ALL sectors (raw SAP flux, cadence-aware model, local baselines; SPOC 2-min sectors where they exist) on top of the all-data BLS ephemeris.
Ephemeris: T0 = BTJD 3243.51874 +- 7.2 min (epoch 68), P = 11.682574 +- 0.000150 d (chi2/dof 0.0/0, inflation x1.00); all-data BLS P = 11.682574.
Sector times used: S71 QLP SAP (2 ev, O-C +0.0 +- 7.2 min).
Depth per sector (fixed shape, local baseline, raw SAP): S71 413 ppm.
Round-2 object with no TESS coverage through Sector 134; ground-based ephemeris test only. See results/allsky_classA_round2_outcomes.csv for vetting status (marginal/weak/rediscovery as listed).
SHA-256 of predicted_transits_2026_2027_v2.csv: d1d84735958dc97e59ee3f79936e1984979bbb13ac5d83bd592d46efc07a4c02
**Test of record: next TESS sector(s).** Predicted mid-transits (conservative window +-20 min):
 epoch   tc_bjd_tdb              utc  sigma_min         tess_sector     status
   162 2.461342e+06 2026-10-28 04:11       21.5 none (ground-based) prediction
   163 2.461353e+06 2026-11-08 20:33       21.7 none (ground-based) prediction
   164 2.461365e+06 2026-11-20 12:56       21.9 none (ground-based) prediction
   165 2.461377e+06 2026-12-02 05:20       22.1 none (ground-based) prediction
   166 2.461388e+06 2026-12-13 21:44       22.3 none (ground-based) prediction
   167 2.461400e+06 2026-12-25 14:08       22.6 none (ground-based) prediction
   168 2.461412e+06 2027-01-06 06:32       22.8 none (ground-based) prediction
   169 2.461423e+06 2027-01-17 22:56       23.0 none (ground-based) prediction
   170 2.461435e+06 2027-01-29 15:21       23.2 none (ground-based) prediction
   171 2.461447e+06 2027-02-10 07:45       23.4 none (ground-based) prediction
   172 2.461459e+06 2027-02-22 00:10       23.6 none (ground-based) prediction
   173 2.461470e+06 2027-03-05 16:34       23.8 none (ground-based) prediction
   174 2.461482e+06 2027-03-17 08:59       24.0 none (ground-based) prediction
   175 2.461494e+06 2027-03-29 01:23       24.2 none (ground-based) prediction
   176 2.461505e+06 2027-04-09 17:47       24.4 none (ground-based) prediction
   177 2.461517e+06 2027-04-21 10:10       24.6 none (ground-based) prediction
   178 2.461529e+06 2027-05-03 02:33       24.8 none (ground-based) prediction
   179 2.461540e+06 2027-05-14 18:56       25.0 none (ground-based) prediction
   180 2.461552e+06 2027-05-26 11:19       25.2 none (ground-based) prediction
   181 2.461564e+06 2027-06-07 03:41       25.4 none (ground-based) prediction
   182 2.461575e+06 2027-06-18 20:03       25.6 none (ground-based) prediction
   183 2.461587e+06 2027-06-30 12:25       25.9 none (ground-based) prediction
   184 2.461599e+06 2027-07-12 04:46       26.1 none (ground-based) prediction
   185 2.461610e+06 2027-07-23 21:08       26.3 none (ground-based) prediction
   186 2.461622e+06 2027-08-04 13:29       26.5 none (ground-based) prediction
   187 2.461634e+06 2027-08-16 05:50       26.7 none (ground-based) prediction
   188 2.461645e+06 2027-08-27 22:12       26.9 none (ground-based) prediction
   189 2.461657e+06 2027-09-08 14:33       27.1 none (ground-based) prediction
   190 2.461669e+06 2027-09-20 06:55       27.3 none (ground-based) prediction
   191 2.461680e+06 2027-10-01 23:16       27.5 none (ground-based) prediction
   192 2.461692e+06 2027-10-13 15:38       27.7 none (ground-based) prediction
   193 2.461704e+06 2027-10-25 08:01       27.9 none (ground-based) prediction
   194 2.461716e+06 2027-11-06 00:23       28.1 none (ground-based) prediction
   195 2.461727e+06 2027-11-17 16:46       28.3 none (ground-based) prediction
   196 2.461739e+06 2027-11-29 09:10       28.6 none (ground-based) prediction
   197 2.461751e+06 2027-12-11 01:33       28.8 none (ground-based) prediction
   198 2.461762e+06 2027-12-22 17:57       29.0 none (ground-based) prediction
   199 2.461774e+06 2028-01-03 10:22       29.2 none (ground-based) prediction
   200 2.461786e+06 2028-01-15 02:46       29.4 none (ground-based) prediction
   201 2.461797e+06 2028-01-26 19:10       29.6 none (ground-based) prediction
   202 2.461809e+06 2028-02-07 11:35       29.8 none (ground-based) prediction
   203 2.461821e+06 2028-02-19 04:00       30.0 none (ground-based) prediction
   204 2.461832e+06 2028-03-01 20:24       30.2 none (ground-based) prediction
   205 2.461844e+06 2028-03-13 12:49       30.4 none (ground-based) prediction
   206 2.461856e+06 2028-03-25 05:13       30.7 none (ground-based) prediction
   207 2.461867e+06 2028-04-05 21:37       30.9 none (ground-based) prediction
   208 2.461879e+06 2028-04-17 14:00       31.1 none (ground-based) prediction
   209 2.461891e+06 2028-04-29 06:24       31.3 none (ground-based) prediction
Outcomes defined in advance (QLP or SPOC light curve of the test sector, or a TESScut fixed-aperture extraction, transit-masked biweight detrend): (1) recovered - a box of
depth 0.5-1.5x and duration 0.7-1.3x the values above within +-3 sigma_min (and in any case within +-30 min) of >= 2 predicted times, stacked SNR >= 5;
(2) inconsistent - a comparable dip exists but its times differ by > 30 min from every prediction; (3) excluded - stacked depth at the predicted phase
< 0.3x at 3 sigma with >= 2 transits fully covered; (4) insufficient - fewer than 2 predicted transits covered. The QLP S99-S105 timestamp error shifts
these ephemerides by < 1.5 min (review, timing_propagation.json). Generated by scripts/prereg_v2.py 371421714 --freeze.
