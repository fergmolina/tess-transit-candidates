# Pre-registered transit predictions v2 - TIC 245503256
Frozen: 2026-10-19 12:51:25 UTC. Author: Fernando Molina (Independent researcher, ORCID 0009-0002-2872-3406). Analysis with Claude (Anthropic) under the author's direction.
First freeze for this object (v2 tooling: all-sector ephemeris). Reason (external review 2026-10-18,
results/external_review_allsky/REVIEW.md): v1 timed only the 200-s sectors (vet.py min_pts cut), ignoring 2018-2021 data; v2 fits one time offset per
sector from ALL sectors (raw SAP flux, cadence-aware model, local baselines; SPOC 2-min sectors where they exist) on top of the all-data BLS ephemeris.
Ephemeris: T0 = BTJD 3624.43662 +- 4.8 min (epoch 125), P = 14.581868 +- 0.000124 d (chi2/dof 0.0/0, inflation x1.00); all-data BLS P = 14.581868.
Sector times used: S85 QLP SAP (1 ev, O-C +0.0 +- 4.8 min).
Depth per sector (fixed shape, local baseline, raw SAP): S85 1976 ppm.
Round-2 weak object (SNR 8.1, 3 transits; shared-time flag); on target. Test: Sector 124.
SHA-256 of predicted_transits_2026_2027_v2.csv: 41678702f848b0cbb8b8bc54bb25ee82cb817cb5daad2b1304734da832446eb0
**Test of record: next TESS sector(s).** Predicted mid-transits (conservative window +-20 min):
 epoch   tc_bjd_tdb              utc  sigma_min                    tess_sector     status
   174 2.461339e+06 2026-10-25 10:38       10.0 undated (future sectors [124]) prediction
   175 2.461354e+06 2026-11-09 00:35       10.1 undated (future sectors [124]) prediction
   176 2.461368e+06 2026-11-23 14:33       10.3 undated (future sectors [124]) prediction
   177 2.461383e+06 2026-12-08 04:31       10.4 undated (future sectors [124]) prediction
   178 2.461397e+06 2026-12-22 18:30       10.6 undated (future sectors [124]) prediction
   179 2.461412e+06 2027-01-06 08:29       10.7 undated (future sectors [124]) prediction
   180 2.461426e+06 2027-01-20 22:28       10.9 undated (future sectors [124]) prediction
   181 2.461441e+06 2027-02-04 12:28       11.1 undated (future sectors [124]) prediction
   182 2.461456e+06 2027-02-19 02:27       11.2 undated (future sectors [124]) prediction
   183 2.461470e+06 2027-03-05 16:27       11.4 undated (future sectors [124]) prediction
   184 2.461485e+06 2027-03-20 06:26       11.5 undated (future sectors [124]) prediction
   185 2.461499e+06 2027-04-03 20:25       11.7 undated (future sectors [124]) prediction
   186 2.461514e+06 2027-04-18 10:24       11.9 undated (future sectors [124]) prediction
   187 2.461529e+06 2027-05-03 00:23       12.0 undated (future sectors [124]) prediction
   188 2.461543e+06 2027-05-17 14:21       12.2 undated (future sectors [124]) prediction
   189 2.461558e+06 2027-06-01 04:18       12.4 undated (future sectors [124]) prediction
   190 2.461572e+06 2027-06-15 18:16       12.5 undated (future sectors [124]) prediction
   191 2.461587e+06 2027-06-30 08:13       12.7 undated (future sectors [124]) prediction
   192 2.461601e+06 2027-07-14 22:09       12.9 undated (future sectors [124]) prediction
   193 2.461616e+06 2027-07-29 12:06       13.0 undated (future sectors [124]) prediction
   194 2.461631e+06 2027-08-13 02:02       13.2 undated (future sectors [124]) prediction
   195 2.461645e+06 2027-08-27 15:58       13.3 undated (future sectors [124]) prediction
   196 2.461660e+06 2027-09-11 05:55       13.5 undated (future sectors [124]) prediction
   197 2.461674e+06 2027-09-25 19:51       13.7 undated (future sectors [124]) prediction
   198 2.461689e+06 2027-10-10 09:48       13.8 undated (future sectors [124]) prediction
   199 2.461703e+06 2027-10-24 23:45       14.0 undated (future sectors [124]) prediction
   200 2.461718e+06 2027-11-08 13:42       14.2 undated (future sectors [124]) prediction
   201 2.461733e+06 2027-11-23 03:40       14.3 undated (future sectors [124]) prediction
   202 2.461747e+06 2027-12-07 17:38       14.5 undated (future sectors [124]) prediction
   203 2.461762e+06 2027-12-22 07:37       14.7 undated (future sectors [124]) prediction
   204 2.461776e+06 2028-01-05 21:36       14.9 undated (future sectors [124]) prediction
   205 2.461791e+06 2028-01-20 11:35       15.0 undated (future sectors [124]) prediction
   206 2.461806e+06 2028-02-04 01:35       15.2 undated (future sectors [124]) prediction
   207 2.461820e+06 2028-02-18 15:34       15.4 undated (future sectors [124]) prediction
   208 2.461835e+06 2028-03-04 05:34       15.5 undated (future sectors [124]) prediction
   209 2.461849e+06 2028-03-18 19:33       15.7 undated (future sectors [124]) prediction
   210 2.461864e+06 2028-04-02 09:32       15.9 undated (future sectors [124]) prediction
   211 2.461878e+06 2028-04-16 23:31       16.0 undated (future sectors [124]) prediction
   212 2.461893e+06 2028-05-01 13:30       16.2 undated (future sectors [124]) prediction
Outcomes defined in advance (QLP or SPOC light curve of the test sector, or a TESScut fixed-aperture extraction, transit-masked biweight detrend): (1) recovered - a box of
depth 0.5-1.5x and duration 0.7-1.3x the values above within +-3 sigma_min (and in any case within +-30 min) of >= 2 predicted times, stacked SNR >= 5;
(2) inconsistent - a comparable dip exists but its times differ by > 30 min from every prediction; (3) excluded - stacked depth at the predicted phase
< 0.3x at 3 sigma with >= 2 transits fully covered; (4) insufficient - fewer than 2 predicted transits covered. The QLP S99-S105 timestamp error shifts
these ephemerides by < 1.5 min (review, timing_propagation.json). Generated by scripts/prereg_v2.py 245503256 --freeze.
