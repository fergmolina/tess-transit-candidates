# Pre-registered transit predictions v2 - TIC 50514263
Frozen: 2026-10-19 12:51:23 UTC. Author: Fernando Molina (Independent researcher, ORCID 0009-0002-2872-3406). Analysis with Claude (Anthropic) under the author's direction.
First freeze for this object (v2 tooling: all-sector ephemeris). Reason (external review 2026-10-18,
results/external_review_allsky/REVIEW.md): v1 timed only the 200-s sectors (vet.py min_pts cut), ignoring 2018-2021 data; v2 fits one time offset per
sector from ALL sectors (raw SAP flux, cadence-aware model, local baselines; SPOC 2-min sectors where they exist) on top of the all-data BLS ephemeris.
Ephemeris: T0 = BTJD 3640.40350 +- 10.2 min (epoch 126), P = 14.593145 +- 0.000244 d (chi2/dof 0.1/1, inflation x1.00); all-data BLS P = 14.593145.
Sector times used: S59 QLP SAP (1 ev, O-C +1.2 +- 10.8 min), S86 QLP SAP (1 ev, O-C -10.8 +- 32.4 min).
Depth per sector (fixed shape, local baseline, raw SAP): S59 1179, S86 2657 ppm.
Round-2 weak object (SNR 7.3); on target. Test: Sector 124.
SHA-256 of predicted_transits_2026_2027_v2.csv: edba125f1f09f95aef509b2be34bc317da6443321f6b39bc5dbfea8435e728bf
**Test of record: next TESS sector(s).** Predicted mid-transits (conservative window +-20 min):
 epoch   tc_bjd_tdb              utc  sigma_min                    tess_sector     status
   174 2.461341e+06 2026-10-27 08:52       19.7 undated (future sectors [124]) prediction
   175 2.461355e+06 2026-11-10 23:06       20.0 undated (future sectors [124]) prediction
   176 2.461370e+06 2026-11-25 13:20       20.3 undated (future sectors [124]) prediction
   177 2.461385e+06 2026-12-10 03:34       20.6 undated (future sectors [124]) prediction
   178 2.461399e+06 2026-12-24 17:49       20.9 undated (future sectors [124]) prediction
   179 2.461414e+06 2027-01-08 08:04       21.2 undated (future sectors [124]) prediction
   180 2.461428e+06 2027-01-22 22:20       21.5 undated (future sectors [124]) prediction
   181 2.461443e+06 2027-02-06 12:35       21.9 undated (future sectors [124]) prediction
   182 2.461458e+06 2027-02-21 02:51       22.2 undated (future sectors [124]) prediction
   183 2.461472e+06 2027-03-07 17:06       22.5 undated (future sectors [124]) prediction
   184 2.461487e+06 2027-03-22 07:22       22.8 undated (future sectors [124]) prediction
   185 2.461501e+06 2027-04-05 21:37       23.1 undated (future sectors [124]) prediction
   186 2.461516e+06 2027-04-20 11:52       23.4 undated (future sectors [124]) prediction
   187 2.461531e+06 2027-05-05 02:07       23.7 undated (future sectors [124]) prediction
   188 2.461545e+06 2027-05-19 16:21       24.1 undated (future sectors [124]) prediction
   189 2.461560e+06 2027-06-03 06:35       24.4 undated (future sectors [124]) prediction
   190 2.461574e+06 2027-06-17 20:49       24.7 undated (future sectors [124]) prediction
   191 2.461589e+06 2027-07-02 11:02       25.0 undated (future sectors [124]) prediction
   192 2.461604e+06 2027-07-17 01:16       25.3 undated (future sectors [124]) prediction
   193 2.461618e+06 2027-07-31 15:28       25.7 undated (future sectors [124]) prediction
   194 2.461633e+06 2027-08-15 05:41       26.0 undated (future sectors [124]) prediction
   195 2.461647e+06 2027-08-29 19:54       26.3 undated (future sectors [124]) prediction
   196 2.461662e+06 2027-09-13 10:06       26.6 undated (future sectors [124]) prediction
   197 2.461677e+06 2027-09-28 00:19       26.9 undated (future sectors [124]) prediction
   198 2.461691e+06 2027-10-12 14:32       27.3 undated (future sectors [124]) prediction
   199 2.461706e+06 2027-10-27 04:46       27.6 undated (future sectors [124]) prediction
   200 2.461720e+06 2027-11-10 18:59       27.9 undated (future sectors [124]) prediction
   201 2.461735e+06 2027-11-25 09:13       28.3 undated (future sectors [124]) prediction
   202 2.461749e+06 2027-12-09 23:27       28.6 undated (future sectors [124]) prediction
   203 2.461764e+06 2027-12-24 13:42       28.9 undated (future sectors [124]) prediction
   204 2.461779e+06 2028-01-08 03:57       29.2 undated (future sectors [124]) prediction
   205 2.461793e+06 2028-01-22 18:13       29.6 undated (future sectors [124]) prediction
   206 2.461808e+06 2028-02-06 08:28       29.9 undated (future sectors [124]) prediction
   207 2.461822e+06 2028-02-20 22:44       30.2 undated (future sectors [124]) prediction
   208 2.461837e+06 2028-03-06 12:59       30.6 undated (future sectors [124]) prediction
   209 2.461852e+06 2028-03-21 03:15       30.9 undated (future sectors [124]) prediction
   210 2.461866e+06 2028-04-04 17:30       31.2 undated (future sectors [124]) prediction
   211 2.461881e+06 2028-04-19 07:45       31.5 undated (future sectors [124]) prediction
   212 2.461895e+06 2028-05-03 22:00       31.9 undated (future sectors [124]) prediction
Outcomes defined in advance (QLP or SPOC light curve of the test sector, or a TESScut fixed-aperture extraction, transit-masked biweight detrend): (1) recovered - a box of
depth 0.5-1.5x and duration 0.7-1.3x the values above within +-3 sigma_min (and in any case within +-30 min) of >= 2 predicted times, stacked SNR >= 5;
(2) inconsistent - a comparable dip exists but its times differ by > 30 min from every prediction; (3) excluded - stacked depth at the predicted phase
< 0.3x at 3 sigma with >= 2 transits fully covered; (4) insufficient - fewer than 2 predicted transits covered. The QLP S99-S105 timestamp error shifts
these ephemerides by < 1.5 min (review, timing_propagation.json). Generated by scripts/prereg_v2.py 50514263 --freeze.


**Addendum 2026-10-20 (timing rule):** the phrase "and in any case within +-30 min" above misstates the rule. The governing rule is the public protocol's (Zenodo 10.5281/zenodo.23462442): stacked timing offset within max(3 sigma_pred, 30 min), as implemented in the frozen evaluator scripts/prereg_test.py. No prediction, CSV or checksum is changed. See CLARIFICATION_TIMING_RULE_2026-10-20.md.
