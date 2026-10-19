# Pre-registered transit predictions v2 - TIC 36694943
Frozen: 2026-10-19 12:51:27 UTC. Author: Fernando Molina (Independent researcher, ORCID 0009-0002-2872-3406). Analysis with Claude (Anthropic) under the author's direction.
First freeze for this object (v2 tooling: all-sector ephemeris). Reason (external review 2026-10-18,
results/external_review_allsky/REVIEW.md): v1 timed only the 200-s sectors (vet.py min_pts cut), ignoring 2018-2021 data; v2 fits one time offset per
sector from ALL sectors (raw SAP flux, cadence-aware model, local baselines; SPOC 2-min sectors where they exist) on top of the all-data BLS ephemeris.
Ephemeris: T0 = BTJD 3828.27606 +- 4.5 min (epoch 107), P = 12.898889 +- 0.000195 d (chi2/dof 0.7/1, inflation x1.00); all-data BLS P = 12.898889.
Sector times used: S70 QLP SAP (2 ev, O-C -10.6 +- 13.2 min), S92 QLP SAP (1 ev, O-C +1.4 +- 4.8 min).
Depth per sector (fixed shape, local baseline, raw SAP): S70 11058, S92 5480 ppm.
Round-2 marginal (depth 5.2 ppt, rho 2.9x, SAP/DET 1.54); on target. Test: Sector 134.
SHA-256 of predicted_transits_2026_2027_v2.csv: a51d71a1994743818576af064c2025588c53ee55614da972582fe0ae3f061c62
**Test of record: next TESS sector(s).** Predicted mid-transits (conservative window +-20 min):
 epoch   tc_bjd_tdb              utc  sigma_min                    tess_sector     status
   147 2.461344e+06 2026-10-30 17:27       12.1 undated (future sectors [134]) prediction
   148 2.461357e+06 2026-11-12 15:03       12.3 undated (future sectors [134]) prediction
   149 2.461370e+06 2026-11-25 12:39       12.6 undated (future sectors [134]) prediction
   150 2.461383e+06 2026-12-08 10:16       12.9 undated (future sectors [134]) prediction
   151 2.461396e+06 2026-12-21 07:52       13.1 undated (future sectors [134]) prediction
   152 2.461409e+06 2027-01-03 05:28       13.4 undated (future sectors [134]) prediction
   153 2.461422e+06 2027-01-16 03:04       13.7 undated (future sectors [134]) prediction
   154 2.461435e+06 2027-01-29 00:39       13.9 undated (future sectors [134]) prediction
   155 2.461447e+06 2027-02-10 22:15       14.2 undated (future sectors [134]) prediction
   156 2.461460e+06 2027-02-23 19:50       14.4 undated (future sectors [134]) prediction
   157 2.461473e+06 2027-03-08 17:24       14.7 undated (future sectors [134]) prediction
   158 2.461486e+06 2027-03-21 14:58       15.0 undated (future sectors [134]) prediction
   159 2.461499e+06 2027-04-03 12:32       15.3 undated (future sectors [134]) prediction
   160 2.461512e+06 2027-04-16 10:05       15.5 undated (future sectors [134]) prediction
   161 2.461525e+06 2027-04-29 07:38       15.8 undated (future sectors [134]) prediction
   162 2.461538e+06 2027-05-12 05:11       16.1 undated (future sectors [134]) prediction
   163 2.461551e+06 2027-05-25 02:44       16.3 undated (future sectors [134]) prediction
   164 2.461564e+06 2027-06-07 00:16       16.6 undated (future sectors [134]) prediction
   165 2.461576e+06 2027-06-19 21:49       16.9 undated (future sectors [134]) prediction
   166 2.461589e+06 2027-07-02 19:22       17.1 undated (future sectors [134]) prediction
   167 2.461602e+06 2027-07-15 16:54       17.4 undated (future sectors [134]) prediction
   168 2.461615e+06 2027-07-28 14:28       17.7 undated (future sectors [134]) prediction
   169 2.461628e+06 2027-08-10 12:01       17.9 undated (future sectors [134]) prediction
   170 2.461641e+06 2027-08-23 09:35       18.2 undated (future sectors [134]) prediction
   171 2.461654e+06 2027-09-05 07:09       18.5 undated (future sectors [134]) prediction
   172 2.461667e+06 2027-09-18 04:44       18.8 undated (future sectors [134]) prediction
   173 2.461680e+06 2027-10-01 02:19       19.0 undated (future sectors [134]) prediction
   174 2.461693e+06 2027-10-13 23:54       19.3 undated (future sectors [134]) prediction
   175 2.461705e+06 2027-10-26 21:30       19.6 undated (future sectors [134]) prediction
   176 2.461718e+06 2027-11-08 19:06       19.9 undated (future sectors [134]) prediction
   177 2.461731e+06 2027-11-21 16:42       20.1 undated (future sectors [134]) prediction
   178 2.461744e+06 2027-12-04 14:18       20.4 undated (future sectors [134]) prediction
   179 2.461757e+06 2027-12-17 11:54       20.7 undated (future sectors [134]) prediction
   180 2.461770e+06 2027-12-30 09:31       20.9 undated (future sectors [134]) prediction
   181 2.461783e+06 2028-01-12 07:07       21.2 undated (future sectors [134]) prediction
   182 2.461796e+06 2028-01-25 04:42       21.5 undated (future sectors [134]) prediction
   183 2.461809e+06 2028-02-07 02:18       21.8 undated (future sectors [134]) prediction
   184 2.461821e+06 2028-02-19 23:53       22.0 undated (future sectors [134]) prediction
   185 2.461834e+06 2028-03-03 21:27       22.3 undated (future sectors [134]) prediction
   186 2.461847e+06 2028-03-16 19:02       22.6 undated (future sectors [134]) prediction
   187 2.461860e+06 2028-03-29 16:35       22.9 undated (future sectors [134]) prediction
   188 2.461873e+06 2028-04-11 14:09       23.1 undated (future sectors [134]) prediction
   189 2.461886e+06 2028-04-24 11:42       23.4 undated (future sectors [134]) prediction
   190 2.461899e+06 2028-05-07 09:15       23.7 undated (future sectors [134]) prediction
Outcomes defined in advance (QLP or SPOC light curve of the test sector, or a TESScut fixed-aperture extraction, transit-masked biweight detrend): (1) recovered - a box of
depth 0.5-1.5x and duration 0.7-1.3x the values above within +-3 sigma_min (and in any case within +-30 min) of >= 2 predicted times, stacked SNR >= 5;
(2) inconsistent - a comparable dip exists but its times differ by > 30 min from every prediction; (3) excluded - stacked depth at the predicted phase
< 0.3x at 3 sigma with >= 2 transits fully covered; (4) insufficient - fewer than 2 predicted transits covered. The QLP S99-S105 timestamp error shifts
these ephemerides by < 1.5 min (review, timing_propagation.json). Generated by scripts/prereg_v2.py 36694943 --freeze.
