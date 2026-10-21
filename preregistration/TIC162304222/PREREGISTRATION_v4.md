# Pre-registered transit predictions v4 - TIC 162304222
Frozen: 2026-10-21 02:57:30 UTC. Author: Fernando Molina (Independent researcher, ORCID 0009-0002-2872-3406). Analysis with Claude (Anthropic) under the author's direction.
First freeze for this object (v2 tooling: all-sector ephemeris). v4 supersedes v2 (SHA of v2 CSV kept on record in final_ephemeris_v2.json); reason: v3 stopped at 2026-12-31 because of the wrong end-date constant in prereg_v2.py (JD 2461406.5 = 2027-01-01): S112 after that date, S113 and S114 had no predictions. v4 has the identical ephemeris (T0, P and errors reproduced exactly) and lists through 2027; the 68 rows shared with v3 are identical. v3 and its hash stay on record; S111 is scored from v3 unchanged, S112-S114 from v4. Reason (external review 2026-10-18,
results/external_review_allsky/REVIEW.md): v1 timed only the 200-s sectors (vet.py min_pts cut), ignoring 2018-2021 data; v2 fits one time offset per
sector from ALL sectors (raw SAP flux, cadence-aware model, local baselines; SPOC 2-min sectors where they exist) on top of the all-data BLS ephemeris.
Ephemeris: T0 = BTJD 4085.20161 +- 6.1 min (epoch 4802), P = 0.523290 +- 0.000002 d (chi2/dof 5.0/2, inflation x1.58); all-data BLS P = 0.523291.
Sector times used: S36 QLP SAP (35 ev, O-C -2.7 +- 7.2 min), S37 QLP SAP (35 ev, O-C +1.0 +- 4.2 min), S99 QLP SAP (31 ev, O-C -20.7 +- 10.2 min), S100 QLP SAP (35 ev, O-C +3.4 +- 4.2 min).
Depth per sector (fixed shape, local baseline, raw SAP): S36 296, S37 229, S99 351, S100 186 ppm.
See ERRATUM_PREDICTION_HORIZON_2026-10-21.

Reference values for the outcome clauses: depth 235 ppm (raw SAP, all sectors), T14 0.90 h.
SHA-256 of predicted_transits_2026_2027_v4.csv: b4a26083fd8ae387242157f69bf03013f34c1f149b5f65a6551592c17a2d70d8
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
  5416 2461406.50150 2027-01-01 00:01    7.30000 112 (span only, gap unknown) prediction
  5417 2461407.02478 2027-01-01 12:34    7.30000 112 (span only, gap unknown) prediction
  5418 2461407.54807 2027-01-02 01:08    7.30000 112 (span only, gap unknown) prediction
  5419 2461408.07136 2027-01-02 13:41    7.30000 112 (span only, gap unknown) prediction
  5420 2461408.59465 2027-01-03 02:15    7.30000 112 (span only, gap unknown) prediction
  5421 2461409.11794 2027-01-03 14:48    7.30000 112 (span only, gap unknown) prediction
  5422 2461409.64123 2027-01-04 03:22    7.30000 112 (span only, gap unknown) prediction
  5423 2461410.16452 2027-01-04 15:55    7.30000 112 (span only, gap unknown) prediction
  5424 2461410.68781 2027-01-05 04:29    7.40000 112 (span only, gap unknown) prediction
  5425 2461411.21110 2027-01-05 17:02    7.40000 112 (span only, gap unknown) prediction
  5426 2461411.73439 2027-01-06 05:35    7.40000 112 (span only, gap unknown) prediction
  5427 2461412.25768 2027-01-06 18:09    7.40000 112 (span only, gap unknown) prediction
  5428 2461412.78097 2027-01-07 06:42    7.40000 112 (span only, gap unknown) prediction
  5429 2461413.30426 2027-01-07 19:16    7.40000 112 (span only, gap unknown) prediction
  5430 2461413.82755 2027-01-08 07:49    7.40000 112 (span only, gap unknown) prediction
  5431 2461414.35084 2027-01-08 20:23    7.40000 112 (span only, gap unknown) prediction
  5432 2461414.87413 2027-01-09 08:56    7.40000 112 (span only, gap unknown) prediction
  5433 2461415.39742 2027-01-09 21:30    7.40000 112 (span only, gap unknown) prediction
  5434 2461415.92071 2027-01-10 10:03    7.40000 112 (span only, gap unknown) prediction
  5435 2461416.44400 2027-01-10 22:37    7.40000 112 (span only, gap unknown) prediction
  5436 2461416.96729 2027-01-11 11:10    7.40000 112 (span only, gap unknown) prediction
  5437 2461417.49058 2027-01-11 23:44    7.40000 112 (span only, gap unknown) prediction
  5438 2461418.01387 2027-01-12 12:17    7.40000 112 (span only, gap unknown) prediction
  5439 2461418.53716 2027-01-13 00:51    7.40000 112 (span only, gap unknown) prediction
  5440 2461419.06045 2027-01-13 13:24    7.40000 112 (span only, gap unknown) prediction
  5441 2461419.58374 2027-01-14 01:58    7.40000 112 (span only, gap unknown) prediction
  5442 2461420.10703 2027-01-14 14:31    7.40000 112 (span only, gap unknown) prediction
  5443 2461420.63032 2027-01-15 03:05    7.40000 112 (span only, gap unknown) prediction
  5444 2461421.15361 2027-01-15 15:38    7.40000 112 (span only, gap unknown) prediction
  5445 2461421.67690 2027-01-16 04:12    7.40000 112 (span only, gap unknown) prediction
  5446 2461422.20019 2027-01-16 16:45    7.40000 112 (span only, gap unknown) prediction
  5447 2461422.72348 2027-01-17 05:19    7.40000 112 (span only, gap unknown) prediction
  5448 2461423.24677 2027-01-17 17:52    7.40000 112 (span only, gap unknown) prediction
  5449 2461423.77006 2027-01-18 06:26    7.40000 113 (span only, gap unknown) prediction
  5450 2461424.29335 2027-01-18 18:59    7.40000 113 (span only, gap unknown) prediction
  5451 2461424.81663 2027-01-19 07:33    7.40000 113 (span only, gap unknown) prediction
  5452 2461425.33992 2027-01-19 20:06    7.40000 113 (span only, gap unknown) prediction
  5453 2461425.86321 2027-01-20 08:40    7.40000 113 (span only, gap unknown) prediction
  5454 2461426.38650 2027-01-20 21:13    7.40000 113 (span only, gap unknown) prediction
  5455 2461426.90979 2027-01-21 09:46    7.40000 113 (span only, gap unknown) prediction
  5456 2461427.43308 2027-01-21 22:20    7.40000 113 (span only, gap unknown) prediction
  5457 2461427.95637 2027-01-22 10:53    7.40000 113 (span only, gap unknown) prediction
  5458 2461428.47966 2027-01-22 23:27    7.40000 113 (span only, gap unknown) prediction
  5459 2461429.00295 2027-01-23 12:00    7.40000 113 (span only, gap unknown) prediction
  5460 2461429.52624 2027-01-24 00:34    7.40000 113 (span only, gap unknown) prediction
  5461 2461430.04953 2027-01-24 13:07    7.40000 113 (span only, gap unknown) prediction
  5462 2461430.57282 2027-01-25 01:41    7.40000 113 (span only, gap unknown) prediction
  5463 2461431.09611 2027-01-25 14:14    7.40000 113 (span only, gap unknown) prediction
  5464 2461431.61940 2027-01-26 02:48    7.40000 113 (span only, gap unknown) prediction
  5465 2461432.14269 2027-01-26 15:21    7.40000 113 (span only, gap unknown) prediction
  5466 2461432.66598 2027-01-27 03:55    7.40000 113 (span only, gap unknown) prediction
  5467 2461433.18927 2027-01-27 16:28    7.40000 113 (span only, gap unknown) prediction
  5468 2461433.71256 2027-01-28 05:02    7.40000 113 (span only, gap unknown) prediction
  5469 2461434.23585 2027-01-28 17:35    7.40000 113 (span only, gap unknown) prediction
  5470 2461434.75914 2027-01-29 06:09    7.40000 113 (span only, gap unknown) prediction
  5471 2461435.28243 2027-01-29 18:42    7.40000 113 (span only, gap unknown) prediction
  5472 2461435.80572 2027-01-30 07:16    7.40000 113 (span only, gap unknown) prediction
  5473 2461436.32901 2027-01-30 19:49    7.50000 113 (span only, gap unknown) prediction
  5474 2461436.85230 2027-01-31 08:23    7.50000 113 (span only, gap unknown) prediction
  5475 2461437.37559 2027-01-31 20:56    7.50000 113 (span only, gap unknown) prediction
  5476 2461437.89888 2027-02-01 09:30    7.50000 113 (span only, gap unknown) prediction
  5477 2461438.42217 2027-02-01 22:03    7.50000 113 (span only, gap unknown) prediction
  5478 2461438.94546 2027-02-02 10:37    7.50000 113 (span only, gap unknown) prediction
  5479 2461439.46875 2027-02-02 23:10    7.50000 113 (span only, gap unknown) prediction
  5480 2461439.99204 2027-02-03 11:44    7.50000 113 (span only, gap unknown) prediction
  5481 2461440.51533 2027-02-04 00:17    7.50000 113 (span only, gap unknown) prediction
  5482 2461441.03862 2027-02-04 12:51    7.50000 113 (span only, gap unknown) prediction
  5483 2461441.56191 2027-02-05 01:24    7.50000 113 (span only, gap unknown) prediction
  5484 2461442.08520 2027-02-05 13:58    7.50000 113 (span only, gap unknown) prediction
  5485 2461442.60849 2027-02-06 02:31    7.50000 113 (span only, gap unknown) prediction
  5486 2461443.13177 2027-02-06 15:05    7.50000 113 (span only, gap unknown) prediction
  5487 2461443.65506 2027-02-07 03:38    7.50000 113 (span only, gap unknown) prediction
  5488 2461444.17835 2027-02-07 16:12    7.50000 113 (span only, gap unknown) prediction
  5489 2461444.70164 2027-02-08 04:45    7.50000 113 (span only, gap unknown) prediction
  5490 2461445.22493 2027-02-08 17:19    7.50000 113 (span only, gap unknown) prediction
  5491 2461445.74822 2027-02-09 05:52    7.50000 113 (span only, gap unknown) prediction
  5492 2461446.27151 2027-02-09 18:26    7.50000 113 (span only, gap unknown) prediction
  5493 2461446.79480 2027-02-10 06:59    7.50000 113 (span only, gap unknown) prediction
  5494 2461447.31809 2027-02-10 19:33    7.50000 113 (span only, gap unknown) prediction
  5495 2461447.84138 2027-02-11 08:06    7.50000 113 (span only, gap unknown) prediction
  5496 2461448.36467 2027-02-11 20:40    7.50000 113 (span only, gap unknown) prediction
  5497 2461448.88796 2027-02-12 09:13    7.50000 113 (span only, gap unknown) prediction
  5498 2461449.41125 2027-02-12 21:47    7.50000 113 (span only, gap unknown) prediction
  5499 2461449.93454 2027-02-13 10:20    7.50000 113 (span only, gap unknown) prediction
  5500 2461450.45783 2027-02-13 22:54    7.50000 113 (span only, gap unknown) prediction
  5501 2461450.98112 2027-02-14 11:27    7.50000 114 (span only, gap unknown) prediction
  5502 2461451.50441 2027-02-15 00:01    7.50000 114 (span only, gap unknown) prediction
  5503 2461452.02770 2027-02-15 12:34    7.50000 114 (span only, gap unknown) prediction
  5504 2461452.55099 2027-02-16 01:08    7.50000 114 (span only, gap unknown) prediction
  5505 2461453.07428 2027-02-16 13:41    7.50000 114 (span only, gap unknown) prediction
  5506 2461453.59757 2027-02-17 02:15    7.50000 114 (span only, gap unknown) prediction
  5507 2461454.12086 2027-02-17 14:48    7.50000 114 (span only, gap unknown) prediction
  5508 2461454.64415 2027-02-18 03:22    7.50000 114 (span only, gap unknown) prediction
  5509 2461455.16744 2027-02-18 15:55    7.50000 114 (span only, gap unknown) prediction
  5510 2461455.69073 2027-02-19 04:29    7.50000 114 (span only, gap unknown) prediction
  5511 2461456.21402 2027-02-19 17:02    7.50000 114 (span only, gap unknown) prediction
  5512 2461456.73731 2027-02-20 05:36    7.50000 114 (span only, gap unknown) prediction
  5513 2461457.26060 2027-02-20 18:09    7.50000 114 (span only, gap unknown) prediction
  5514 2461457.78389 2027-02-21 06:43    7.50000 114 (span only, gap unknown) prediction
  5515 2461458.30718 2027-02-21 19:16    7.50000 114 (span only, gap unknown) prediction
  5516 2461458.83047 2027-02-22 07:50    7.50000 114 (span only, gap unknown) prediction
  5517 2461459.35376 2027-02-22 20:23    7.50000 114 (span only, gap unknown) prediction
  5518 2461459.87705 2027-02-23 08:57    7.50000 114 (span only, gap unknown) prediction
  5519 2461460.40034 2027-02-23 21:30    7.50000 114 (span only, gap unknown) prediction
  5520 2461460.92362 2027-02-24 10:04    7.50000 114 (span only, gap unknown) prediction
  5521 2461461.44691 2027-02-24 22:37    7.50000 114 (span only, gap unknown) prediction
  5522 2461461.97020 2027-02-25 11:11    7.60000 114 (span only, gap unknown) prediction
  5523 2461462.49349 2027-02-25 23:44    7.60000 114 (span only, gap unknown) prediction
  5524 2461463.01678 2027-02-26 12:18    7.60000 114 (span only, gap unknown) prediction
  5525 2461463.54007 2027-02-27 00:51    7.60000 114 (span only, gap unknown) prediction
  5526 2461464.06336 2027-02-27 13:25    7.60000 114 (span only, gap unknown) prediction
  5527 2461464.58665 2027-02-28 01:58    7.60000 114 (span only, gap unknown) prediction
  5528 2461465.10994 2027-02-28 14:32    7.60000 114 (span only, gap unknown) prediction
  5529 2461465.63323 2027-03-01 03:05    7.60000 114 (span only, gap unknown) prediction
  5530 2461466.15652 2027-03-01 15:39    7.60000 114 (span only, gap unknown) prediction
  5531 2461466.67981 2027-03-02 04:12    7.60000 114 (span only, gap unknown) prediction
  5532 2461467.20310 2027-03-02 16:46    7.60000 114 (span only, gap unknown) prediction
  5533 2461467.72639 2027-03-03 05:19    7.60000 114 (span only, gap unknown) prediction
  5534 2461468.24968 2027-03-03 17:53    7.60000 114 (span only, gap unknown) prediction
  5535 2461468.77297 2027-03-04 06:26    7.60000 114 (span only, gap unknown) prediction
  5536 2461469.29626 2027-03-04 19:00    7.60000 114 (span only, gap unknown) prediction
  5537 2461469.81955 2027-03-05 07:33    7.60000 114 (span only, gap unknown) prediction
  5538 2461470.34284 2027-03-05 20:07    7.60000 114 (span only, gap unknown) prediction
  5539 2461470.86613 2027-03-06 08:40    7.60000 114 (span only, gap unknown) prediction
  5540 2461471.38942 2027-03-06 21:14    7.60000 114 (span only, gap unknown) prediction
  5541 2461471.91271 2027-03-07 09:47    7.60000 114 (span only, gap unknown) prediction
  5542 2461472.43600 2027-03-07 22:21    7.60000 114 (span only, gap unknown) prediction
  5543 2461472.95929 2027-03-08 10:54    7.60000 114 (span only, gap unknown) prediction
  5544 2461473.48258 2027-03-08 23:28    7.60000 114 (span only, gap unknown) prediction
  5545 2461474.00587 2027-03-09 12:01    7.60000 114 (span only, gap unknown) prediction
  5546 2461474.52916 2027-03-10 00:35    7.60000 114 (span only, gap unknown) prediction
  5547 2461475.05245 2027-03-10 13:08    7.60000 114 (span only, gap unknown) prediction
  5548 2461475.57574 2027-03-11 01:42    7.60000 114 (span only, gap unknown) prediction
  5549 2461476.09903 2027-03-11 14:15    7.60000 114 (span only, gap unknown) prediction
  5550 2461476.62232 2027-03-12 02:49    7.60000 114 (span only, gap unknown) prediction
  5551 2461477.14561 2027-03-12 15:22    7.60000 114 (span only, gap unknown) prediction
  5552 2461477.66890 2027-03-13 03:56    7.60000 114 (span only, gap unknown) prediction
  5553 2461478.19219 2027-03-13 16:29    7.60000 114 (span only, gap unknown) prediction
  5554 2461478.71547 2027-03-14 05:03    7.60000 114 (span only, gap unknown) prediction
  5555 2461479.23876 2027-03-14 17:36    7.60000 114 (span only, gap unknown) prediction
Outcomes defined in advance (QLP or SPOC light curve of the test sector, transit-masked biweight detrend; no TESScut fallback - withdrawn 2026-10-20 in conformance v2.1): (1) recovered - a box of depth 0.5-1.5x and duration 0.7-1.3x the reference values at >= 2 covered predicted transit windows, stacked SNR >= 5, timing gate |sum(w_i dt_i)/sum(w_i)| <= max(3 mean(sigma_min,i), 30 min) with w_i = 1/depth_err_i^2 over the coverage-qualified windows (frozen evaluator; inverse depth-variance weights); duration and full-coverage criteria are assessed under the separately versioned conformance procedure (see CLARIFICATION_TIMING_RULE_2026-10-20.md); (2) inconsistent - a comparable dip exists but its times differ by > 30 min from every prediction; (3) excluded - stacked depth at the predicted phase < 0.3x at 3 sigma with >= 2 transits fully covered; (4) insufficient - fewer than 2 predicted transits covered. QLP S99+ sector times were corrected for the barycentric timestamp error before the fit (results/qlp_clock_v2/; corrections in min: {99: -0.0, 100: 1.19}). Generated by scripts/prereg_v2.py 162304222 --freeze --version 4.

**Dated correction 2026-10-21 (appended; frozen CSV unchanged).** The generated header above reads "First freeze for this object" and "v4
supersedes v2"; both are template errors. This is the fourth version for this object; v4 supersedes v3 (CSV SHA in final_ephemeris_v3.json),
which superseded v2. The template now names the previous version.
