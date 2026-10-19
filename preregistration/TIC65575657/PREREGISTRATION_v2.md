# Pre-registered transit predictions v2 - TIC 65575657
Frozen: 2026-10-19 12:51:32 UTC. Author: Fernando Molina (Independent researcher, ORCID 0009-0002-2872-3406). Analysis with Claude (Anthropic) under the author's direction.
First freeze for this object (v2 tooling: all-sector ephemeris). Reason (external review 2026-10-18,
results/external_review_allsky/REVIEW.md): v1 timed only the 200-s sectors (vet.py min_pts cut), ignoring 2018-2021 data; v2 fits one time offset per
sector from ALL sectors (raw SAP flux, cadence-aware model, local baselines; SPOC 2-min sectors where they exist) on top of the all-data BLS ephemeris.
Ephemeris: T0 = BTJD 3654.05954 +- 3.3 min (epoch 358), P = 5.187879 +- 0.000058 d (chi2/dof 2.8/1, inflation x1.66); all-data BLS P = 5.187879.
Sector times used: S18 QLP SAP (3 ev, O-C +5.0 +- 3.6 min), S86 QLP SAP (4 ev, O-C -2.2 +- 2.4 min).
Depth per sector (fixed shape, local baseline, raw SAP): S18 2031, S86 1853 ppm.
Round-2 object with no TESS coverage through Sector 134; ground-based ephemeris test only. See results/allsky_classA_round2_outcomes.csv for vetting status (marginal/weak/rediscovery as listed).
SHA-256 of predicted_transits_2026_2027_v2.csv: 8e7400d246ac23103afce5096fe25ce0d63e821a6eaa8ed30b7622d99cd7c9af
**Test of record: next TESS sector(s).** Predicted mid-transits (conservative window +-20 min):
 epoch   tc_bjd_tdb              utc  sigma_min         tess_sector     status
   489 2.461334e+06 2026-10-20 03:59       11.4 none (ground-based) prediction
   490 2.461339e+06 2026-10-25 08:30       11.5 none (ground-based) prediction
   491 2.461344e+06 2026-10-30 13:00       11.6 none (ground-based) prediction
   492 2.461349e+06 2026-11-04 17:30       11.6 none (ground-based) prediction
   493 2.461354e+06 2026-11-09 22:00       11.7 none (ground-based) prediction
   494 2.461360e+06 2026-11-15 02:31       11.8 none (ground-based) prediction
   495 2.461365e+06 2026-11-20 07:01       11.9 none (ground-based) prediction
   496 2.461370e+06 2026-11-25 11:32       12.0 none (ground-based) prediction
   497 2.461375e+06 2026-11-30 16:02       12.0 none (ground-based) prediction
   498 2.461380e+06 2026-12-05 20:33       12.1 none (ground-based) prediction
   499 2.461386e+06 2026-12-11 01:04       12.2 none (ground-based) prediction
   500 2.461391e+06 2026-12-16 05:35       12.3 none (ground-based) prediction
   501 2.461396e+06 2026-12-21 10:05       12.4 none (ground-based) prediction
   502 2.461401e+06 2026-12-26 14:36       12.4 none (ground-based) prediction
   503 2.461406e+06 2026-12-31 19:07       12.5 none (ground-based) prediction
   504 2.461411e+06 2027-01-05 23:38       12.6 none (ground-based) prediction
   505 2.461417e+06 2027-01-11 04:09       12.7 none (ground-based) prediction
   506 2.461422e+06 2027-01-16 08:40       12.8 none (ground-based) prediction
   507 2.461427e+06 2027-01-21 13:11       12.8 none (ground-based) prediction
   508 2.461432e+06 2027-01-26 17:43       12.9 none (ground-based) prediction
   509 2.461437e+06 2027-01-31 22:14       13.0 none (ground-based) prediction
   510 2.461443e+06 2027-02-06 02:45       13.1 none (ground-based) prediction
   511 2.461448e+06 2027-02-11 07:16       13.2 none (ground-based) prediction
   512 2.461453e+06 2027-02-16 11:47       13.2 none (ground-based) prediction
   513 2.461458e+06 2027-02-21 16:19       13.3 none (ground-based) prediction
   514 2.461463e+06 2027-02-26 20:50       13.4 none (ground-based) prediction
   515 2.461469e+06 2027-03-04 01:21       13.5 none (ground-based) prediction
   516 2.461474e+06 2027-03-09 05:52       13.6 none (ground-based) prediction
   517 2.461479e+06 2027-03-14 10:23       13.6 none (ground-based) prediction
   518 2.461484e+06 2027-03-19 14:55       13.7 none (ground-based) prediction
   519 2.461489e+06 2027-03-24 19:26       13.8 none (ground-based) prediction
   520 2.461494e+06 2027-03-29 23:57       13.9 none (ground-based) prediction
   521 2.461500e+06 2027-04-04 04:28       14.0 none (ground-based) prediction
   522 2.461505e+06 2027-04-09 08:59       14.0 none (ground-based) prediction
   523 2.461510e+06 2027-04-14 13:30       14.1 none (ground-based) prediction
   524 2.461515e+06 2027-04-19 18:01       14.2 none (ground-based) prediction
   525 2.461520e+06 2027-04-24 22:32       14.3 none (ground-based) prediction
   526 2.461526e+06 2027-04-30 03:03       14.4 none (ground-based) prediction
   527 2.461531e+06 2027-05-05 07:34       14.4 none (ground-based) prediction
   528 2.461536e+06 2027-05-10 12:04       14.5 none (ground-based) prediction
   529 2.461541e+06 2027-05-15 16:35       14.6 none (ground-based) prediction
   530 2.461546e+06 2027-05-20 21:06       14.7 none (ground-based) prediction
   531 2.461552e+06 2027-05-26 01:36       14.8 none (ground-based) prediction
   532 2.461557e+06 2027-05-31 06:07       14.9 none (ground-based) prediction
   533 2.461562e+06 2027-06-05 10:37       14.9 none (ground-based) prediction
   534 2.461567e+06 2027-06-10 15:08       15.0 none (ground-based) prediction
   535 2.461572e+06 2027-06-15 19:38       15.1 none (ground-based) prediction
   536 2.461578e+06 2027-06-21 00:08       15.2 none (ground-based) prediction
   537 2.461583e+06 2027-06-26 04:38       15.3 none (ground-based) prediction
   538 2.461588e+06 2027-07-01 09:09       15.3 none (ground-based) prediction
   539 2.461593e+06 2027-07-06 13:39       15.4 none (ground-based) prediction
   540 2.461598e+06 2027-07-11 18:09       15.5 none (ground-based) prediction
   541 2.461603e+06 2027-07-16 22:39       15.6 none (ground-based) prediction
   542 2.461609e+06 2027-07-22 03:09       15.7 none (ground-based) prediction
   543 2.461614e+06 2027-07-27 07:39       15.7 none (ground-based) prediction
   544 2.461619e+06 2027-08-01 12:09       15.8 none (ground-based) prediction
   545 2.461624e+06 2027-08-06 16:39       15.9 none (ground-based) prediction
   546 2.461629e+06 2027-08-11 21:09       16.0 none (ground-based) prediction
   547 2.461635e+06 2027-08-17 01:38       16.1 none (ground-based) prediction
   548 2.461640e+06 2027-08-22 06:08       16.2 none (ground-based) prediction
   549 2.461645e+06 2027-08-27 10:38       16.2 none (ground-based) prediction
   550 2.461650e+06 2027-09-01 15:08       16.3 none (ground-based) prediction
   551 2.461655e+06 2027-09-06 19:38       16.4 none (ground-based) prediction
   552 2.461661e+06 2027-09-12 00:08       16.5 none (ground-based) prediction
   553 2.461666e+06 2027-09-17 04:38       16.6 none (ground-based) prediction
   554 2.461671e+06 2027-09-22 09:08       16.6 none (ground-based) prediction
   555 2.461676e+06 2027-09-27 13:38       16.7 none (ground-based) prediction
   556 2.461681e+06 2027-10-02 18:08       16.8 none (ground-based) prediction
   557 2.461686e+06 2027-10-07 22:38       16.9 none (ground-based) prediction
   558 2.461692e+06 2027-10-13 03:08       17.0 none (ground-based) prediction
   559 2.461697e+06 2027-10-18 07:38       17.0 none (ground-based) prediction
   560 2.461702e+06 2027-10-23 12:08       17.1 none (ground-based) prediction
   561 2.461707e+06 2027-10-28 16:38       17.2 none (ground-based) prediction
   562 2.461712e+06 2027-11-02 21:08       17.3 none (ground-based) prediction
   563 2.461718e+06 2027-11-08 01:39       17.4 none (ground-based) prediction
   564 2.461723e+06 2027-11-13 06:09       17.5 none (ground-based) prediction
   565 2.461728e+06 2027-11-18 10:40       17.5 none (ground-based) prediction
   566 2.461733e+06 2027-11-23 15:10       17.6 none (ground-based) prediction
   567 2.461738e+06 2027-11-28 19:41       17.7 none (ground-based) prediction
   568 2.461744e+06 2027-12-04 00:11       17.8 none (ground-based) prediction
   569 2.461749e+06 2027-12-09 04:42       17.9 none (ground-based) prediction
   570 2.461754e+06 2027-12-14 09:13       17.9 none (ground-based) prediction
   571 2.461759e+06 2027-12-19 13:43       18.0 none (ground-based) prediction
   572 2.461764e+06 2027-12-24 18:14       18.1 none (ground-based) prediction
   573 2.461769e+06 2027-12-29 22:45       18.2 none (ground-based) prediction
   574 2.461775e+06 2028-01-04 03:16       18.3 none (ground-based) prediction
   575 2.461780e+06 2028-01-09 07:47       18.4 none (ground-based) prediction
   576 2.461785e+06 2028-01-14 12:18       18.4 none (ground-based) prediction
   577 2.461790e+06 2028-01-19 16:49       18.5 none (ground-based) prediction
   578 2.461795e+06 2028-01-24 21:20       18.6 none (ground-based) prediction
   579 2.461801e+06 2028-01-30 01:52       18.7 none (ground-based) prediction
   580 2.461806e+06 2028-02-04 06:23       18.8 none (ground-based) prediction
   581 2.461811e+06 2028-02-09 10:54       18.8 none (ground-based) prediction
   582 2.461816e+06 2028-02-14 15:25       18.9 none (ground-based) prediction
   583 2.461821e+06 2028-02-19 19:56       19.0 none (ground-based) prediction
   584 2.461827e+06 2028-02-25 00:28       19.1 none (ground-based) prediction
   585 2.461832e+06 2028-03-01 04:59       19.2 none (ground-based) prediction
   586 2.461837e+06 2028-03-06 09:30       19.3 none (ground-based) prediction
   587 2.461842e+06 2028-03-11 14:01       19.3 none (ground-based) prediction
   588 2.461847e+06 2028-03-16 18:33       19.4 none (ground-based) prediction
   589 2.461852e+06 2028-03-21 23:04       19.5 none (ground-based) prediction
   590 2.461858e+06 2028-03-27 03:35       19.6 none (ground-based) prediction
   591 2.461863e+06 2028-04-01 08:06       19.7 none (ground-based) prediction
   592 2.461868e+06 2028-04-06 12:37       19.7 none (ground-based) prediction
   593 2.461873e+06 2028-04-11 17:08       19.8 none (ground-based) prediction
   594 2.461878e+06 2028-04-16 21:39       19.9 none (ground-based) prediction
   595 2.461884e+06 2028-04-22 02:10       20.0 none (ground-based) prediction
   596 2.461889e+06 2028-04-27 06:41       20.1 none (ground-based) prediction
   597 2.461894e+06 2028-05-02 11:12       20.2 none (ground-based) prediction
   598 2.461899e+06 2028-05-07 15:42       20.2 none (ground-based) prediction
Outcomes defined in advance (QLP or SPOC light curve of the test sector, or a TESScut fixed-aperture extraction, transit-masked biweight detrend): (1) recovered - a box of
depth 0.5-1.5x and duration 0.7-1.3x the values above within +-3 sigma_min (and in any case within +-30 min) of >= 2 predicted times, stacked SNR >= 5;
(2) inconsistent - a comparable dip exists but its times differ by > 30 min from every prediction; (3) excluded - stacked depth at the predicted phase
< 0.3x at 3 sigma with >= 2 transits fully covered; (4) insufficient - fewer than 2 predicted transits covered. The QLP S99-S105 timestamp error shifts
these ephemerides by < 1.5 min (review, timing_propagation.json). Generated by scripts/prereg_v2.py 65575657 --freeze.
