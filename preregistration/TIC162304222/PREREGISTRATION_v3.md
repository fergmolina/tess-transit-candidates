# Pre-registered transit predictions v3 - TIC 162304222
Frozen: 2026-10-20 02:03:13 UTC. Author: Fernando Molina (Independent researcher, ORCID 0009-0002-2872-3406). Analysis with Claude (Anthropic) under the author's direction.
First freeze for this object (v2 tooling: all-sector ephemeris). v3 supersedes v2 (SHA of v2 CSV kept on record in final_ephemeris_v2.json); reason: v2 (SHA 742f2b16...) contains no prediction rows: the generator stopped after 399 epochs, before the test sectors (generator horizon defect found 2026-10-20). v3 uses the same data and method with the horizon extended through 2027-12-31. Test sector S111 starts 2026-11-26 and was not yet observed at this freeze. Reason (external review 2026-10-18,
results/external_review_allsky/REVIEW.md): v1 timed only the 200-s sectors (vet.py min_pts cut), ignoring 2018-2021 data; v2 fits one time offset per
sector from ALL sectors (raw SAP flux, cadence-aware model, local baselines; SPOC 2-min sectors where they exist) on top of the all-data BLS ephemeris.
Ephemeris: T0 = BTJD 4085.20161 +- 6.1 min (epoch 4802), P = 0.523290 +- 0.000002 d (chi2/dof 5.0/2, inflation x1.58); all-data BLS P = 0.523291.
Sector times used: S36 QLP SAP (35 ev, O-C -2.7 +- 7.2 min), S37 QLP SAP (35 ev, O-C +1.0 +- 4.2 min), S99 QLP SAP (31 ev, O-C -20.7 +- 10.2 min), S100 QLP SAP (35 ev, O-C +3.4 +- 4.2 min).
Depth per sector (fixed shape, local baseline, raw SAP): S36 296, S37 229, S99 351, S100 186 ppm.
Round-3 weak object (SNR 6.3, red-noise SNR lower; P 0.523 d, ~240 ppm). On target. Clock convention offset from the all-sky fallback (+0.033 min). Test: Sector 111 (not yet observed at freeze).
Reference values for the outcome clauses: depth 235 ppm (raw SAP, all sectors), T14 0.90 h.
SHA-256 of predicted_transits_2026_2027_v3.csv: 445f1dd701470764a0471644c981738b8fc019920fb14743b73d83b8e16031ba
**Test of record: next TESS sector(s).** Predicted mid-transits (sigma_min = 1-sigma timing uncertainty at that epoch):
 epoch    tc_bjd_tdb              utc  sigma_min                  tess_sector     status
  5348 2461370.91779 2026-11-26 10:04    7.20000                          111 prediction
  5349 2461371.44108 2026-11-26 22:37    7.20000                          111 prediction
  5350 2461371.96437 2026-11-27 11:11    7.20000                          111 prediction
  5351 2461372.48766 2026-11-27 23:44    7.20000                          111 prediction
  5352 2461373.01095 2026-11-28 12:18    7.20000                          111 prediction
  5353 2461373.53424 2026-11-29 00:51    7.20000                          111 prediction
  5354 2461374.05753 2026-11-29 13:25    7.20000                          111 prediction
  5355 2461374.58082 2026-11-30 01:58    7.20000                          111 prediction
  5356 2461375.10411 2026-11-30 14:32    7.20000                          111 prediction
  5357 2461375.62740 2026-12-01 03:05    7.20000                          111 prediction
  5358 2461376.15069 2026-12-01 15:39    7.20000                          111 prediction
  5359 2461376.67398 2026-12-02 04:12    7.20000                          111 prediction
  5360 2461377.19727 2026-12-02 16:46    7.20000                          111 prediction
  5361 2461377.72056 2026-12-03 05:19    7.20000                    111 (gap) prediction
  5362 2461378.24385 2026-12-03 17:53    7.20000                          111 prediction
  5363 2461378.76714 2026-12-04 06:26    7.20000                          111 prediction
  5364 2461379.29043 2026-12-04 18:59    7.20000                          111 prediction
  5365 2461379.81372 2026-12-05 07:33    7.20000                          111 prediction
  5366 2461380.33701 2026-12-05 20:06    7.20000                          111 prediction
  5367 2461380.86030 2026-12-06 08:40    7.20000                          111 prediction
  5368 2461381.38359 2026-12-06 21:13    7.20000                          111 prediction
  5369 2461381.90688 2026-12-07 09:47    7.20000                          111 prediction
  5370 2461382.43017 2026-12-07 22:20    7.20000                          111 prediction
  5371 2461382.95346 2026-12-08 10:54    7.20000                          111 prediction
  5372 2461383.47675 2026-12-08 23:27    7.20000                          111 prediction
  5373 2461384.00004 2026-12-09 12:01    7.20000 111 (span only, gap unknown) prediction
  5374 2461384.52333 2026-12-10 00:34    7.20000 111 (span only, gap unknown) prediction
  5375 2461385.04662 2026-12-10 13:08    7.30000 111 (span only, gap unknown) prediction
  5376 2461385.56991 2026-12-11 01:41    7.30000 111 (span only, gap unknown) prediction
  5377 2461386.09320 2026-12-11 14:15    7.30000 111 (span only, gap unknown) prediction
  5378 2461386.61649 2026-12-12 02:48    7.30000 111 (span only, gap unknown) prediction
  5379 2461387.13978 2026-12-12 15:22    7.30000 111 (span only, gap unknown) prediction
  5380 2461387.66307 2026-12-13 03:55    7.30000 111 (span only, gap unknown) prediction
  5381 2461388.18636 2026-12-13 16:29    7.30000 111 (span only, gap unknown) prediction
  5382 2461388.70964 2026-12-14 05:02    7.30000 111 (span only, gap unknown) prediction
  5383 2461389.23293 2026-12-14 17:36    7.30000 111 (span only, gap unknown) prediction
  5384 2461389.75622 2026-12-15 06:09    7.30000 111 (span only, gap unknown) prediction
  5385 2461390.27951 2026-12-15 18:43    7.30000 111 (span only, gap unknown) prediction
  5386 2461390.80280 2026-12-16 07:16    7.30000 111 (span only, gap unknown) prediction
  5387 2461391.32609 2026-12-16 19:50    7.30000 111 (span only, gap unknown) prediction
  5388 2461391.84938 2026-12-17 08:23    7.30000 111 (span only, gap unknown) prediction
  5389 2461392.37267 2026-12-17 20:57    7.30000 111 (span only, gap unknown) prediction
  5390 2461392.89596 2026-12-18 09:30    7.30000 111 (span only, gap unknown) prediction
  5391 2461393.41925 2026-12-18 22:04    7.30000 111 (span only, gap unknown) prediction
  5392 2461393.94254 2026-12-19 10:37    7.30000 111 (span only, gap unknown) prediction
  5393 2461394.46583 2026-12-19 23:11    7.30000 111 (span only, gap unknown) prediction
  5394 2461394.98912 2026-12-20 11:44    7.30000 111 (span only, gap unknown) prediction
  5395 2461395.51241 2026-12-21 00:18    7.30000 111 (span only, gap unknown) prediction
  5396 2461396.03570 2026-12-21 12:51    7.30000 111 (span only, gap unknown) prediction
  5397 2461396.55899 2026-12-22 01:25    7.30000 111 (span only, gap unknown) prediction
  5398 2461397.08228 2026-12-22 13:58    7.30000 111 (span only, gap unknown) prediction
  5399 2461397.60557 2026-12-23 02:31    7.30000 112 (span only, gap unknown) prediction
  5400 2461398.12886 2026-12-23 15:05    7.30000 112 (span only, gap unknown) prediction
  5401 2461398.65215 2026-12-24 03:38    7.30000 112 (span only, gap unknown) prediction
  5402 2461399.17544 2026-12-24 16:12    7.30000 112 (span only, gap unknown) prediction
  5403 2461399.69873 2026-12-25 04:45    7.30000 112 (span only, gap unknown) prediction
  5404 2461400.22202 2026-12-25 17:19    7.30000 112 (span only, gap unknown) prediction
  5405 2461400.74531 2026-12-26 05:52    7.30000 112 (span only, gap unknown) prediction
  5406 2461401.26860 2026-12-26 18:26    7.30000 112 (span only, gap unknown) prediction
  5407 2461401.79189 2026-12-27 06:59    7.30000 112 (span only, gap unknown) prediction
  5408 2461402.31518 2026-12-27 19:33    7.30000 112 (span only, gap unknown) prediction
  5409 2461402.83847 2026-12-28 08:06    7.30000 112 (span only, gap unknown) prediction
  5410 2461403.36176 2026-12-28 20:40    7.30000 112 (span only, gap unknown) prediction
  5411 2461403.88505 2026-12-29 09:13    7.30000 112 (span only, gap unknown) prediction
  5412 2461404.40834 2026-12-29 21:47    7.30000 112 (span only, gap unknown) prediction
  5413 2461404.93163 2026-12-30 10:20    7.30000 112 (span only, gap unknown) prediction
  5414 2461405.45492 2026-12-30 22:54    7.30000 112 (span only, gap unknown) prediction
  5415 2461405.97821 2026-12-31 11:27    7.30000 112 (span only, gap unknown) prediction
Outcomes defined in advance (QLP or SPOC light curve of the test sector, or a TESScut fixed-aperture extraction, transit-masked biweight detrend): (1) recovered - a box of depth 0.5-1.5x and duration 0.7-1.3x the reference values at >= 2 covered predicted transit windows, stacked SNR >= 5, timing gate |sum(w_i dt_i)/sum(w_i)| <= max(3 mean(sigma_min,i), 30 min) with w_i = 1/depth_err_i^2 over the coverage-qualified windows (frozen evaluator; inverse depth-variance weights); duration and full-coverage criteria are assessed under the separately versioned conformance procedure (see CLARIFICATION_TIMING_RULE_2026-10-20.md); (2) inconsistent - a comparable dip exists but its times differ by > 30 min from every prediction; (3) excluded - stacked depth at the predicted phase < 0.3x at 3 sigma with >= 2 transits fully covered; (4) insufficient - fewer than 2 predicted transits covered. QLP S99+ sector times were corrected for the barycentric timestamp error before the fit (results/qlp_clock_v2/; corrections in min: {99: -0.0, 100: 1.19}). Generated by scripts/prereg_v2.py 162304222 --freeze --version 3.

**Dated note 2026-10-21 (appended; frozen CSV unchanged).** This list stops at 2026-12-31 because of a wrong end-date constant in
prereg_v2.py (JD 2461406.5 = 2027-01-01): S112 after that date, S113 and S114 have no predictions here. v4 (frozen 2026-10-21, CSV
b4a26083...) has the identical ephemeris and the 68 rows shared with this file are identical; S111 is scored from this v3 unchanged,
S112-S114 from v4. See ERRATUM_PREDICTION_HORIZON_2026-10-21.md.
