# Pre-registered transit predictions v2 - TIC 249813122
Frozen: 2026-10-19 12:51:17 UTC. Author: Fernando Molina (Independent researcher, ORCID 0009-0002-2872-3406). Analysis with Claude (Anthropic) under the author's direction.
First freeze for this object (v2 tooling: all-sector ephemeris). Reason (external review 2026-10-18,
results/external_review_allsky/REVIEW.md): v1 timed only the 200-s sectors (vet.py min_pts cut), ignoring 2018-2021 data; v2 fits one time offset per
sector from ALL sectors (raw SAP flux, cadence-aware model, local baselines; SPOC 2-min sectors where they exist) on top of the all-data BLS ephemeris.
Ephemeris: T0 = BTJD 3595.31078 +- 2.6 min (epoch 444), P = 4.176147 +- 0.000011 d (chi2/dof 2.5/3, inflation x1.00); all-data BLS P = 4.176145.
Sector times used: S16 QLP SAP (3 ev, O-C -5.6 +- 8.4 min), S56 QLP SAP (7 ev, O-C -1.3 +- 3.0 min), S57 QLP SAP (6 ev, O-C +4.7 +- 3.6 min), S83 QLP SAP (6 ev, O-C -1.7 +- 4.2 min), S84 QLP SAP (6 ev, O-C -0.5 +- 3.6 min).
Depth per sector (fixed shape, local baseline, raw SAP): S16 1839, S56 2245, S57 1882, S83 1937, S84 2108 ppm.
Round-2 object: SDE 24.6, SNR 15, blind 1/1, on target (0.15-0.47 px); rho_fit/rho_TIC 5.3 (short duration - density tension, grazing or wrong host radius possible). No prior listing in corpus. Test: Sector 122.
SHA-256 of predicted_transits_2026_2027_v2.csv: 8c47e87946d91d3bdf214ff0c80adc3c9e9a8306b56347a5eb0ba03893f1abd7
**Test of record: next TESS sector(s).** Predicted mid-transits (conservative window +-20 min):
 epoch   tc_bjd_tdb              utc  sigma_min                              tess_sector     status
   621 2.461334e+06 2026-10-20 23:37        5.0 undated (future sectors [122, 128, 129]) prediction
   622 2.461339e+06 2026-10-25 03:51        5.0 undated (future sectors [122, 128, 129]) prediction
   623 2.461343e+06 2026-10-29 08:05        5.0 undated (future sectors [122, 128, 129]) prediction
   624 2.461347e+06 2026-11-02 12:19        5.0 undated (future sectors [122, 128, 129]) prediction
   625 2.461351e+06 2026-11-06 16:33        5.1 undated (future sectors [122, 128, 129]) prediction
   626 2.461355e+06 2026-11-10 20:46        5.1 undated (future sectors [122, 128, 129]) prediction
   627 2.461360e+06 2026-11-15 01:00        5.1 undated (future sectors [122, 128, 129]) prediction
   628 2.461364e+06 2026-11-19 05:14        5.1 undated (future sectors [122, 128, 129]) prediction
   629 2.461368e+06 2026-11-23 09:28        5.1 undated (future sectors [122, 128, 129]) prediction
   630 2.461372e+06 2026-11-27 13:42        5.1 undated (future sectors [122, 128, 129]) prediction
   631 2.461376e+06 2026-12-01 17:56        5.2 undated (future sectors [122, 128, 129]) prediction
   632 2.461380e+06 2026-12-05 22:10        5.2 undated (future sectors [122, 128, 129]) prediction
   633 2.461385e+06 2026-12-10 02:24        5.2 undated (future sectors [122, 128, 129]) prediction
   634 2.461389e+06 2026-12-14 06:38        5.2 undated (future sectors [122, 128, 129]) prediction
   635 2.461393e+06 2026-12-18 10:52        5.2 undated (future sectors [122, 128, 129]) prediction
   636 2.461397e+06 2026-12-22 15:06        5.2 undated (future sectors [122, 128, 129]) prediction
   637 2.461401e+06 2026-12-26 19:20        5.2 undated (future sectors [122, 128, 129]) prediction
   638 2.461405e+06 2026-12-30 23:34        5.3 undated (future sectors [122, 128, 129]) prediction
   639 2.461410e+06 2027-01-04 03:48        5.3 undated (future sectors [122, 128, 129]) prediction
   640 2.461414e+06 2027-01-08 08:02        5.3 undated (future sectors [122, 128, 129]) prediction
   641 2.461418e+06 2027-01-12 12:16        5.3 undated (future sectors [122, 128, 129]) prediction
   642 2.461422e+06 2027-01-16 16:30        5.3 undated (future sectors [122, 128, 129]) prediction
   643 2.461426e+06 2027-01-20 20:44        5.3 undated (future sectors [122, 128, 129]) prediction
   644 2.461431e+06 2027-01-25 00:58        5.3 undated (future sectors [122, 128, 129]) prediction
   645 2.461435e+06 2027-01-29 05:12        5.4 undated (future sectors [122, 128, 129]) prediction
   646 2.461439e+06 2027-02-02 09:26        5.4 undated (future sectors [122, 128, 129]) prediction
   647 2.461443e+06 2027-02-06 13:40        5.4 undated (future sectors [122, 128, 129]) prediction
   648 2.461447e+06 2027-02-10 17:54        5.4 undated (future sectors [122, 128, 129]) prediction
   649 2.461451e+06 2027-02-14 22:08        5.4 undated (future sectors [122, 128, 129]) prediction
   650 2.461456e+06 2027-02-19 02:22        5.4 undated (future sectors [122, 128, 129]) prediction
   651 2.461460e+06 2027-02-23 06:36        5.5 undated (future sectors [122, 128, 129]) prediction
   652 2.461464e+06 2027-02-27 10:50        5.5 undated (future sectors [122, 128, 129]) prediction
   653 2.461468e+06 2027-03-03 15:04        5.5 undated (future sectors [122, 128, 129]) prediction
   654 2.461472e+06 2027-03-07 19:17        5.5 undated (future sectors [122, 128, 129]) prediction
   655 2.461476e+06 2027-03-11 23:31        5.5 undated (future sectors [122, 128, 129]) prediction
   656 2.461481e+06 2027-03-16 03:45        5.5 undated (future sectors [122, 128, 129]) prediction
   657 2.461485e+06 2027-03-20 07:59        5.5 undated (future sectors [122, 128, 129]) prediction
   658 2.461489e+06 2027-03-24 12:12        5.6 undated (future sectors [122, 128, 129]) prediction
   659 2.461493e+06 2027-03-28 16:26        5.6 undated (future sectors [122, 128, 129]) prediction
   660 2.461497e+06 2027-04-01 20:40        5.6 undated (future sectors [122, 128, 129]) prediction
   661 2.461502e+06 2027-04-06 00:53        5.6 undated (future sectors [122, 128, 129]) prediction
   662 2.461506e+06 2027-04-10 05:07        5.6 undated (future sectors [122, 128, 129]) prediction
   663 2.461510e+06 2027-04-14 09:20        5.6 undated (future sectors [122, 128, 129]) prediction
   664 2.461514e+06 2027-04-18 13:34        5.7 undated (future sectors [122, 128, 129]) prediction
   665 2.461518e+06 2027-04-22 17:48        5.7 undated (future sectors [122, 128, 129]) prediction
   666 2.461522e+06 2027-04-26 22:01        5.7 undated (future sectors [122, 128, 129]) prediction
   667 2.461527e+06 2027-05-01 02:14        5.7 undated (future sectors [122, 128, 129]) prediction
   668 2.461531e+06 2027-05-05 06:28        5.7 undated (future sectors [122, 128, 129]) prediction
   669 2.461535e+06 2027-05-09 10:41        5.7 undated (future sectors [122, 128, 129]) prediction
   670 2.461539e+06 2027-05-13 14:55        5.7 undated (future sectors [122, 128, 129]) prediction
   671 2.461543e+06 2027-05-17 19:08        5.8 undated (future sectors [122, 128, 129]) prediction
   672 2.461547e+06 2027-05-21 23:22        5.8 undated (future sectors [122, 128, 129]) prediction
   673 2.461552e+06 2027-05-26 03:35        5.8 undated (future sectors [122, 128, 129]) prediction
   674 2.461556e+06 2027-05-30 07:48        5.8 undated (future sectors [122, 128, 129]) prediction
   675 2.461560e+06 2027-06-03 12:02        5.8 undated (future sectors [122, 128, 129]) prediction
   676 2.461564e+06 2027-06-07 16:15        5.8 undated (future sectors [122, 128, 129]) prediction
   677 2.461568e+06 2027-06-11 20:28        5.8 undated (future sectors [122, 128, 129]) prediction
   678 2.461573e+06 2027-06-16 00:41        5.9 undated (future sectors [122, 128, 129]) prediction
   679 2.461577e+06 2027-06-20 04:55        5.9 undated (future sectors [122, 128, 129]) prediction
   680 2.461581e+06 2027-06-24 09:08        5.9 undated (future sectors [122, 128, 129]) prediction
   681 2.461585e+06 2027-06-28 13:21        5.9 undated (future sectors [122, 128, 129]) prediction
   682 2.461589e+06 2027-07-02 17:35        5.9 undated (future sectors [122, 128, 129]) prediction
   683 2.461593e+06 2027-07-06 21:48        5.9 undated (future sectors [122, 128, 129]) prediction
   684 2.461598e+06 2027-07-11 02:01        6.0 undated (future sectors [122, 128, 129]) prediction
   685 2.461602e+06 2027-07-15 06:15        6.0 undated (future sectors [122, 128, 129]) prediction
   686 2.461606e+06 2027-07-19 10:28        6.0 undated (future sectors [122, 128, 129]) prediction
   687 2.461610e+06 2027-07-23 14:41        6.0 undated (future sectors [122, 128, 129]) prediction
   688 2.461614e+06 2027-07-27 18:54        6.0 undated (future sectors [122, 128, 129]) prediction
   689 2.461618e+06 2027-07-31 23:08        6.0 undated (future sectors [122, 128, 129]) prediction
   690 2.461623e+06 2027-08-05 03:21        6.0 undated (future sectors [122, 128, 129]) prediction
   691 2.461627e+06 2027-08-09 07:34        6.1 undated (future sectors [122, 128, 129]) prediction
   692 2.461631e+06 2027-08-13 11:48        6.1 undated (future sectors [122, 128, 129]) prediction
   693 2.461635e+06 2027-08-17 16:01        6.1 undated (future sectors [122, 128, 129]) prediction
   694 2.461639e+06 2027-08-21 20:15        6.1 undated (future sectors [122, 128, 129]) prediction
   695 2.461644e+06 2027-08-26 00:28        6.1 undated (future sectors [122, 128, 129]) prediction
   696 2.461648e+06 2027-08-30 04:41        6.1 undated (future sectors [122, 128, 129]) prediction
   697 2.461652e+06 2027-09-03 08:55        6.2 undated (future sectors [122, 128, 129]) prediction
   698 2.461656e+06 2027-09-07 13:08        6.2 undated (future sectors [122, 128, 129]) prediction
   699 2.461660e+06 2027-09-11 17:22        6.2 undated (future sectors [122, 128, 129]) prediction
   700 2.461664e+06 2027-09-15 21:36        6.2 undated (future sectors [122, 128, 129]) prediction
   701 2.461669e+06 2027-09-20 01:49        6.2 undated (future sectors [122, 128, 129]) prediction
   702 2.461673e+06 2027-09-24 06:03        6.2 undated (future sectors [122, 128, 129]) prediction
   703 2.461677e+06 2027-09-28 10:16        6.2 undated (future sectors [122, 128, 129]) prediction
   704 2.461681e+06 2027-10-02 14:30        6.3 undated (future sectors [122, 128, 129]) prediction
   705 2.461685e+06 2027-10-06 18:44        6.3 undated (future sectors [122, 128, 129]) prediction
   706 2.461689e+06 2027-10-10 22:57        6.3 undated (future sectors [122, 128, 129]) prediction
   707 2.461694e+06 2027-10-15 03:11        6.3 undated (future sectors [122, 128, 129]) prediction
   708 2.461698e+06 2027-10-19 07:25        6.3 undated (future sectors [122, 128, 129]) prediction
   709 2.461702e+06 2027-10-23 11:39        6.3 undated (future sectors [122, 128, 129]) prediction
   710 2.461706e+06 2027-10-27 15:52        6.3 undated (future sectors [122, 128, 129]) prediction
   711 2.461710e+06 2027-10-31 20:06        6.4 undated (future sectors [122, 128, 129]) prediction
   712 2.461715e+06 2027-11-05 00:20        6.4 undated (future sectors [122, 128, 129]) prediction
   713 2.461719e+06 2027-11-09 04:34        6.4 undated (future sectors [122, 128, 129]) prediction
   714 2.461723e+06 2027-11-13 08:48        6.4 undated (future sectors [122, 128, 129]) prediction
   715 2.461727e+06 2027-11-17 13:02        6.4 undated (future sectors [122, 128, 129]) prediction
   716 2.461731e+06 2027-11-21 17:16        6.4 undated (future sectors [122, 128, 129]) prediction
   717 2.461735e+06 2027-11-25 21:30        6.5 undated (future sectors [122, 128, 129]) prediction
   718 2.461740e+06 2027-11-30 01:44        6.5 undated (future sectors [122, 128, 129]) prediction
   719 2.461744e+06 2027-12-04 05:58        6.5 undated (future sectors [122, 128, 129]) prediction
   720 2.461748e+06 2027-12-08 10:12        6.5 undated (future sectors [122, 128, 129]) prediction
   721 2.461752e+06 2027-12-12 14:26        6.5 undated (future sectors [122, 128, 129]) prediction
   722 2.461756e+06 2027-12-16 18:40        6.5 undated (future sectors [122, 128, 129]) prediction
   723 2.461760e+06 2027-12-20 22:54        6.5 undated (future sectors [122, 128, 129]) prediction
   724 2.461765e+06 2027-12-25 03:08        6.6 undated (future sectors [122, 128, 129]) prediction
   725 2.461769e+06 2027-12-29 07:22        6.6 undated (future sectors [122, 128, 129]) prediction
   726 2.461773e+06 2028-01-02 11:36        6.6 undated (future sectors [122, 128, 129]) prediction
   727 2.461777e+06 2028-01-06 15:50        6.6 undated (future sectors [122, 128, 129]) prediction
   728 2.461781e+06 2028-01-10 20:04        6.6 undated (future sectors [122, 128, 129]) prediction
   729 2.461786e+06 2028-01-15 00:18        6.6 undated (future sectors [122, 128, 129]) prediction
   730 2.461790e+06 2028-01-19 04:32        6.7 undated (future sectors [122, 128, 129]) prediction
   731 2.461794e+06 2028-01-23 08:46        6.7 undated (future sectors [122, 128, 129]) prediction
   732 2.461798e+06 2028-01-27 13:00        6.7 undated (future sectors [122, 128, 129]) prediction
   733 2.461802e+06 2028-01-31 17:14        6.7 undated (future sectors [122, 128, 129]) prediction
   734 2.461806e+06 2028-02-04 21:28        6.7 undated (future sectors [122, 128, 129]) prediction
   735 2.461811e+06 2028-02-09 01:42        6.7 undated (future sectors [122, 128, 129]) prediction
   736 2.461815e+06 2028-02-13 05:56        6.7 undated (future sectors [122, 128, 129]) prediction
   737 2.461819e+06 2028-02-17 10:10        6.8 undated (future sectors [122, 128, 129]) prediction
   738 2.461823e+06 2028-02-21 14:23        6.8 undated (future sectors [122, 128, 129]) prediction
   739 2.461827e+06 2028-02-25 18:37        6.8 undated (future sectors [122, 128, 129]) prediction
   740 2.461831e+06 2028-02-29 22:51        6.8 undated (future sectors [122, 128, 129]) prediction
   741 2.461836e+06 2028-03-05 03:05        6.8 undated (future sectors [122, 128, 129]) prediction
   742 2.461840e+06 2028-03-09 07:19        6.8 undated (future sectors [122, 128, 129]) prediction
   743 2.461844e+06 2028-03-13 11:32        6.9 undated (future sectors [122, 128, 129]) prediction
   744 2.461848e+06 2028-03-17 15:46        6.9 undated (future sectors [122, 128, 129]) prediction
   745 2.461852e+06 2028-03-21 20:00        6.9 undated (future sectors [122, 128, 129]) prediction
   746 2.461857e+06 2028-03-26 00:14        6.9 undated (future sectors [122, 128, 129]) prediction
   747 2.461861e+06 2028-03-30 04:27        6.9 undated (future sectors [122, 128, 129]) prediction
   748 2.461865e+06 2028-04-03 08:41        6.9 undated (future sectors [122, 128, 129]) prediction
   749 2.461869e+06 2028-04-07 12:55        6.9 undated (future sectors [122, 128, 129]) prediction
   750 2.461873e+06 2028-04-11 17:08        7.0 undated (future sectors [122, 128, 129]) prediction
   751 2.461877e+06 2028-04-15 21:22        7.0 undated (future sectors [122, 128, 129]) prediction
   752 2.461882e+06 2028-04-20 01:35        7.0 undated (future sectors [122, 128, 129]) prediction
   753 2.461886e+06 2028-04-24 05:49        7.0 undated (future sectors [122, 128, 129]) prediction
   754 2.461890e+06 2028-04-28 10:02        7.0 undated (future sectors [122, 128, 129]) prediction
   755 2.461894e+06 2028-05-02 14:16        7.0 undated (future sectors [122, 128, 129]) prediction
   756 2.461898e+06 2028-05-06 18:29        7.1 undated (future sectors [122, 128, 129]) prediction
Outcomes defined in advance (QLP or SPOC light curve of the test sector, or a TESScut fixed-aperture extraction, transit-masked biweight detrend): (1) recovered - a box of
depth 0.5-1.5x and duration 0.7-1.3x the values above within +-3 sigma_min (and in any case within +-30 min) of >= 2 predicted times, stacked SNR >= 5;
(2) inconsistent - a comparable dip exists but its times differ by > 30 min from every prediction; (3) excluded - stacked depth at the predicted phase
< 0.3x at 3 sigma with >= 2 transits fully covered; (4) insufficient - fewer than 2 predicted transits covered. The QLP S99-S105 timestamp error shifts
these ephemerides by < 1.5 min (review, timing_propagation.json). Generated by scripts/prereg_v2.py 249813122 --freeze.


**Addendum 2026-10-20 (timing rule):** the phrase "and in any case within +-30 min" above misstates the rule. The governing rule is the public protocol's (Zenodo 10.5281/zenodo.23462442): stacked timing offset within max(3 sigma_pred, 30 min), as implemented in the frozen evaluator scripts/prereg_test.py. No prediction, CSV or checksum is changed. See CLARIFICATION_TIMING_RULE_2026-10-20.md.
