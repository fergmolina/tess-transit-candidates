# Pre-registered transit predictions v2 - TIC 376225363
Frozen: 2026-10-19 12:51:20 UTC. Author: Fernando Molina (Independent researcher, ORCID 0009-0002-2872-3406). Analysis with Claude (Anthropic) under the author's direction.
First freeze for this object (v2 tooling: all-sector ephemeris). Reason (external review 2026-10-18,
results/external_review_allsky/REVIEW.md): v1 timed only the 200-s sectors (vet.py min_pts cut), ignoring 2018-2021 data; v2 fits one time offset per
sector from ALL sectors (raw SAP flux, cadence-aware model, local baselines; SPOC 2-min sectors where they exist) on top of the all-data BLS ephemeris.
Ephemeris: T0 = BTJD 3597.78188 +- 31.3 min (epoch 476), P = 3.446624 +- 0.000106 d (chi2/dof 111.2/2, inflation x7.46); all-data BLS P = 3.446721.
Sector times used: S24 QLP SAP (6 ev, O-C +77.2 +- 10.2 min), S57 QLP SAP (6 ev, O-C +7.9 +- 4.2 min), S58 QLP SAP (8 ev, O-C -12.6 +- 2.4 min), S84 QLP SAP (6 ev, O-C +23.0 +- 4.8 min).
Depth per sector (fixed shape, local baseline, raw SAP): S24 374, S57 419, S58 363, S84 526 ppm.
Round-2 weak object (SNR 8.3); on target. Test: Sector 122.
SHA-256 of predicted_transits_2026_2027_v2.csv: 034139b99d992aa3f11937f16dfe16d208350b30b323603afd381f2967306a87
**Test of record: next TESS sector(s).** Predicted mid-transits (conservative window +-20 min):
 epoch   tc_bjd_tdb              utc  sigma_min                         tess_sector     status
   690 2.461335e+06 2026-10-21 20:33       62.2 undated (future sectors [122, 129]) prediction
   691 2.461339e+06 2026-10-25 07:16       62.4 undated (future sectors [122, 129]) prediction
   692 2.461342e+06 2026-10-28 17:59       62.5 undated (future sectors [122, 129]) prediction
   693 2.461346e+06 2026-11-01 04:42       62.7 undated (future sectors [122, 129]) prediction
   694 2.461349e+06 2026-11-04 15:25       62.8 undated (future sectors [122, 129]) prediction
   695 2.461353e+06 2026-11-08 02:08       63.0 undated (future sectors [122, 129]) prediction
   696 2.461356e+06 2026-11-11 12:52       63.1 undated (future sectors [122, 129]) prediction
   697 2.461359e+06 2026-11-14 23:35       63.3 undated (future sectors [122, 129]) prediction
   698 2.461363e+06 2026-11-18 10:18       63.4 undated (future sectors [122, 129]) prediction
   699 2.461366e+06 2026-11-21 21:01       63.6 undated (future sectors [122, 129]) prediction
   700 2.461370e+06 2026-11-25 07:44       63.7 undated (future sectors [122, 129]) prediction
   701 2.461373e+06 2026-11-28 18:28       63.9 undated (future sectors [122, 129]) prediction
   702 2.461377e+06 2026-12-02 05:11       64.0 undated (future sectors [122, 129]) prediction
   703 2.461380e+06 2026-12-05 15:54       64.2 undated (future sectors [122, 129]) prediction
   704 2.461384e+06 2026-12-09 02:37       64.3 undated (future sectors [122, 129]) prediction
   705 2.461387e+06 2026-12-12 13:21       64.5 undated (future sectors [122, 129]) prediction
   706 2.461391e+06 2026-12-16 00:04       64.6 undated (future sectors [122, 129]) prediction
   707 2.461394e+06 2026-12-19 10:47       64.8 undated (future sectors [122, 129]) prediction
   708 2.461397e+06 2026-12-22 21:31       64.9 undated (future sectors [122, 129]) prediction
   709 2.461401e+06 2026-12-26 08:14       65.1 undated (future sectors [122, 129]) prediction
   710 2.461404e+06 2026-12-29 18:57       65.2 undated (future sectors [122, 129]) prediction
   711 2.461408e+06 2027-01-02 05:40       65.4 undated (future sectors [122, 129]) prediction
   712 2.461411e+06 2027-01-05 16:24       65.5 undated (future sectors [122, 129]) prediction
   713 2.461415e+06 2027-01-09 03:07       65.7 undated (future sectors [122, 129]) prediction
   714 2.461418e+06 2027-01-12 13:50       65.8 undated (future sectors [122, 129]) prediction
   715 2.461422e+06 2027-01-16 00:34       66.0 undated (future sectors [122, 129]) prediction
   716 2.461425e+06 2027-01-19 11:17       66.1 undated (future sectors [122, 129]) prediction
   717 2.461428e+06 2027-01-22 22:01       66.3 undated (future sectors [122, 129]) prediction
   718 2.461432e+06 2027-01-26 08:44       66.4 undated (future sectors [122, 129]) prediction
   719 2.461435e+06 2027-01-29 19:27       66.6 undated (future sectors [122, 129]) prediction
   720 2.461439e+06 2027-02-02 06:11       66.7 undated (future sectors [122, 129]) prediction
   721 2.461442e+06 2027-02-05 16:54       66.9 undated (future sectors [122, 129]) prediction
   722 2.461446e+06 2027-02-09 03:37       67.0 undated (future sectors [122, 129]) prediction
   723 2.461449e+06 2027-02-12 14:21       67.2 undated (future sectors [122, 129]) prediction
   724 2.461453e+06 2027-02-16 01:04       67.3 undated (future sectors [122, 129]) prediction
   725 2.461456e+06 2027-02-19 11:47       67.5 undated (future sectors [122, 129]) prediction
   726 2.461459e+06 2027-02-22 22:31       67.6 undated (future sectors [122, 129]) prediction
   727 2.461463e+06 2027-02-26 09:14       67.8 undated (future sectors [122, 129]) prediction
   728 2.461466e+06 2027-03-01 19:57       67.9 undated (future sectors [122, 129]) prediction
   729 2.461470e+06 2027-03-05 06:41       68.0 undated (future sectors [122, 129]) prediction
   730 2.461473e+06 2027-03-08 17:24       68.2 undated (future sectors [122, 129]) prediction
   731 2.461477e+06 2027-03-12 04:07       68.3 undated (future sectors [122, 129]) prediction
   732 2.461480e+06 2027-03-15 14:50       68.5 undated (future sectors [122, 129]) prediction
   733 2.461484e+06 2027-03-19 01:34       68.6 undated (future sectors [122, 129]) prediction
   734 2.461487e+06 2027-03-22 12:17       68.8 undated (future sectors [122, 129]) prediction
   735 2.461490e+06 2027-03-25 23:00       68.9 undated (future sectors [122, 129]) prediction
   736 2.461494e+06 2027-03-29 09:43       69.1 undated (future sectors [122, 129]) prediction
   737 2.461497e+06 2027-04-01 20:27       69.2 undated (future sectors [122, 129]) prediction
   738 2.461501e+06 2027-04-05 07:10       69.4 undated (future sectors [122, 129]) prediction
   739 2.461504e+06 2027-04-08 17:53       69.5 undated (future sectors [122, 129]) prediction
   740 2.461508e+06 2027-04-12 04:36       69.7 undated (future sectors [122, 129]) prediction
   741 2.461511e+06 2027-04-15 15:20       69.8 undated (future sectors [122, 129]) prediction
   742 2.461515e+06 2027-04-19 02:03       70.0 undated (future sectors [122, 129]) prediction
   743 2.461518e+06 2027-04-22 12:46       70.1 undated (future sectors [122, 129]) prediction
   744 2.461521e+06 2027-04-25 23:29       70.3 undated (future sectors [122, 129]) prediction
   745 2.461525e+06 2027-04-29 10:12       70.4 undated (future sectors [122, 129]) prediction
   746 2.461528e+06 2027-05-02 20:55       70.6 undated (future sectors [122, 129]) prediction
   747 2.461532e+06 2027-05-06 07:38       70.7 undated (future sectors [122, 129]) prediction
   748 2.461535e+06 2027-05-09 18:22       70.9 undated (future sectors [122, 129]) prediction
   749 2.461539e+06 2027-05-13 05:05       71.0 undated (future sectors [122, 129]) prediction
   750 2.461542e+06 2027-05-16 15:48       71.2 undated (future sectors [122, 129]) prediction
   751 2.461546e+06 2027-05-20 02:31       71.3 undated (future sectors [122, 129]) prediction
   752 2.461549e+06 2027-05-23 13:14       71.5 undated (future sectors [122, 129]) prediction
   753 2.461552e+06 2027-05-26 23:57       71.6 undated (future sectors [122, 129]) prediction
   754 2.461556e+06 2027-05-30 10:40       71.8 undated (future sectors [122, 129]) prediction
   755 2.461559e+06 2027-06-02 21:23       71.9 undated (future sectors [122, 129]) prediction
   756 2.461563e+06 2027-06-06 08:06       72.1 undated (future sectors [122, 129]) prediction
   757 2.461566e+06 2027-06-09 18:49       72.2 undated (future sectors [122, 129]) prediction
   758 2.461570e+06 2027-06-13 05:32       72.4 undated (future sectors [122, 129]) prediction
   759 2.461573e+06 2027-06-16 16:15       72.5 undated (future sectors [122, 129]) prediction
   760 2.461577e+06 2027-06-20 02:58       72.7 undated (future sectors [122, 129]) prediction
   761 2.461580e+06 2027-06-23 13:41       72.8 undated (future sectors [122, 129]) prediction
   762 2.461584e+06 2027-06-27 00:24       73.0 undated (future sectors [122, 129]) prediction
   763 2.461587e+06 2027-06-30 11:07       73.1 undated (future sectors [122, 129]) prediction
   764 2.461590e+06 2027-07-03 21:50       73.3 undated (future sectors [122, 129]) prediction
   765 2.461594e+06 2027-07-07 08:33       73.4 undated (future sectors [122, 129]) prediction
   766 2.461597e+06 2027-07-10 19:16       73.6 undated (future sectors [122, 129]) prediction
   767 2.461601e+06 2027-07-14 05:59       73.7 undated (future sectors [122, 129]) prediction
   768 2.461604e+06 2027-07-17 16:42       73.9 undated (future sectors [122, 129]) prediction
   769 2.461608e+06 2027-07-21 03:25       74.0 undated (future sectors [122, 129]) prediction
   770 2.461611e+06 2027-07-24 14:08       74.2 undated (future sectors [122, 129]) prediction
   771 2.461615e+06 2027-07-28 00:50       74.3 undated (future sectors [122, 129]) prediction
   772 2.461618e+06 2027-07-31 11:33       74.5 undated (future sectors [122, 129]) prediction
   773 2.461621e+06 2027-08-03 22:16       74.6 undated (future sectors [122, 129]) prediction
   774 2.461625e+06 2027-08-07 08:59       74.8 undated (future sectors [122, 129]) prediction
   775 2.461628e+06 2027-08-10 19:42       74.9 undated (future sectors [122, 129]) prediction
   776 2.461632e+06 2027-08-14 06:25       75.1 undated (future sectors [122, 129]) prediction
   777 2.461635e+06 2027-08-17 17:08       75.2 undated (future sectors [122, 129]) prediction
   778 2.461639e+06 2027-08-21 03:51       75.4 undated (future sectors [122, 129]) prediction
   779 2.461642e+06 2027-08-24 14:34       75.5 undated (future sectors [122, 129]) prediction
   780 2.461646e+06 2027-08-28 01:17       75.7 undated (future sectors [122, 129]) prediction
   781 2.461649e+06 2027-08-31 12:00       75.8 undated (future sectors [122, 129]) prediction
   782 2.461652e+06 2027-09-03 22:43       76.0 undated (future sectors [122, 129]) prediction
   783 2.461656e+06 2027-09-07 09:26       76.1 undated (future sectors [122, 129]) prediction
   784 2.461659e+06 2027-09-10 20:09       76.3 undated (future sectors [122, 129]) prediction
   785 2.461663e+06 2027-09-14 06:52       76.4 undated (future sectors [122, 129]) prediction
   786 2.461666e+06 2027-09-17 17:35       76.6 undated (future sectors [122, 129]) prediction
   787 2.461670e+06 2027-09-21 04:18       76.7 undated (future sectors [122, 129]) prediction
   788 2.461673e+06 2027-09-24 15:01       76.9 undated (future sectors [122, 129]) prediction
   789 2.461677e+06 2027-09-28 01:44       77.0 undated (future sectors [122, 129]) prediction
   790 2.461680e+06 2027-10-01 12:27       77.2 undated (future sectors [122, 129]) prediction
   791 2.461683e+06 2027-10-04 23:10       77.3 undated (future sectors [122, 129]) prediction
   792 2.461687e+06 2027-10-08 09:53       77.5 undated (future sectors [122, 129]) prediction
   793 2.461690e+06 2027-10-11 20:36       77.6 undated (future sectors [122, 129]) prediction
   794 2.461694e+06 2027-10-15 07:19       77.8 undated (future sectors [122, 129]) prediction
   795 2.461697e+06 2027-10-18 18:02       77.9 undated (future sectors [122, 129]) prediction
   796 2.461701e+06 2027-10-22 04:45       78.1 undated (future sectors [122, 129]) prediction
   797 2.461704e+06 2027-10-25 15:28       78.2 undated (future sectors [122, 129]) prediction
   798 2.461708e+06 2027-10-29 02:12       78.4 undated (future sectors [122, 129]) prediction
   799 2.461711e+06 2027-11-01 12:55       78.5 undated (future sectors [122, 129]) prediction
   800 2.461714e+06 2027-11-04 23:38       78.7 undated (future sectors [122, 129]) prediction
   801 2.461718e+06 2027-11-08 10:21       78.8 undated (future sectors [122, 129]) prediction
   802 2.461721e+06 2027-11-11 21:04       79.0 undated (future sectors [122, 129]) prediction
   803 2.461725e+06 2027-11-15 07:47       79.1 undated (future sectors [122, 129]) prediction
   804 2.461728e+06 2027-11-18 18:31       79.3 undated (future sectors [122, 129]) prediction
   805 2.461732e+06 2027-11-22 05:14       79.4 undated (future sectors [122, 129]) prediction
   806 2.461735e+06 2027-11-25 15:57       79.6 undated (future sectors [122, 129]) prediction
   807 2.461739e+06 2027-11-29 02:40       79.7 undated (future sectors [122, 129]) prediction
   808 2.461742e+06 2027-12-02 13:24       79.9 undated (future sectors [122, 129]) prediction
   809 2.461746e+06 2027-12-06 00:07       80.0 undated (future sectors [122, 129]) prediction
   810 2.461749e+06 2027-12-09 10:50       80.2 undated (future sectors [122, 129]) prediction
   811 2.461752e+06 2027-12-12 21:33       80.3 undated (future sectors [122, 129]) prediction
   812 2.461756e+06 2027-12-16 08:17       80.5 undated (future sectors [122, 129]) prediction
   813 2.461759e+06 2027-12-19 19:00       80.6 undated (future sectors [122, 129]) prediction
   814 2.461763e+06 2027-12-23 05:43       80.8 undated (future sectors [122, 129]) prediction
   815 2.461766e+06 2027-12-26 16:27       81.0 undated (future sectors [122, 129]) prediction
   816 2.461770e+06 2027-12-30 03:10       81.1 undated (future sectors [122, 129]) prediction
   817 2.461773e+06 2028-01-02 13:53       81.3 undated (future sectors [122, 129]) prediction
   818 2.461777e+06 2028-01-06 00:37       81.4 undated (future sectors [122, 129]) prediction
   819 2.461780e+06 2028-01-09 11:20       81.6 undated (future sectors [122, 129]) prediction
   820 2.461783e+06 2028-01-12 22:03       81.7 undated (future sectors [122, 129]) prediction
   821 2.461787e+06 2028-01-16 08:47       81.9 undated (future sectors [122, 129]) prediction
   822 2.461790e+06 2028-01-19 19:30       82.0 undated (future sectors [122, 129]) prediction
   823 2.461794e+06 2028-01-23 06:13       82.2 undated (future sectors [122, 129]) prediction
   824 2.461797e+06 2028-01-26 16:57       82.3 undated (future sectors [122, 129]) prediction
   825 2.461801e+06 2028-01-30 03:40       82.5 undated (future sectors [122, 129]) prediction
   826 2.461804e+06 2028-02-02 14:23       82.6 undated (future sectors [122, 129]) prediction
   827 2.461808e+06 2028-02-06 01:07       82.8 undated (future sectors [122, 129]) prediction
   828 2.461811e+06 2028-02-09 11:50       82.9 undated (future sectors [122, 129]) prediction
   829 2.461814e+06 2028-02-12 22:33       83.1 undated (future sectors [122, 129]) prediction
   830 2.461818e+06 2028-02-16 09:17       83.2 undated (future sectors [122, 129]) prediction
   831 2.461821e+06 2028-02-19 20:00       83.4 undated (future sectors [122, 129]) prediction
   832 2.461825e+06 2028-02-23 06:43       83.5 undated (future sectors [122, 129]) prediction
   833 2.461828e+06 2028-02-26 17:27       83.7 undated (future sectors [122, 129]) prediction
   834 2.461832e+06 2028-03-01 04:10       83.8 undated (future sectors [122, 129]) prediction
   835 2.461835e+06 2028-03-04 14:53       84.0 undated (future sectors [122, 129]) prediction
   836 2.461839e+06 2028-03-08 01:37       84.1 undated (future sectors [122, 129]) prediction
   837 2.461842e+06 2028-03-11 12:20       84.3 undated (future sectors [122, 129]) prediction
   838 2.461845e+06 2028-03-14 23:03       84.4 undated (future sectors [122, 129]) prediction
   839 2.461849e+06 2028-03-18 09:46       84.6 undated (future sectors [122, 129]) prediction
   840 2.461852e+06 2028-03-21 20:30       84.7 undated (future sectors [122, 129]) prediction
   841 2.461856e+06 2028-03-25 07:13       84.9 undated (future sectors [122, 129]) prediction
   842 2.461859e+06 2028-03-28 17:56       85.0 undated (future sectors [122, 129]) prediction
   843 2.461863e+06 2028-04-01 04:39       85.2 undated (future sectors [122, 129]) prediction
   844 2.461866e+06 2028-04-04 15:23       85.3 undated (future sectors [122, 129]) prediction
   845 2.461870e+06 2028-04-08 02:06       85.5 undated (future sectors [122, 129]) prediction
   846 2.461873e+06 2028-04-11 12:49       85.6 undated (future sectors [122, 129]) prediction
   847 2.461876e+06 2028-04-14 23:32       85.8 undated (future sectors [122, 129]) prediction
   848 2.461880e+06 2028-04-18 10:15       85.9 undated (future sectors [122, 129]) prediction
   849 2.461883e+06 2028-04-21 20:59       86.1 undated (future sectors [122, 129]) prediction
   850 2.461887e+06 2028-04-25 07:42       86.2 undated (future sectors [122, 129]) prediction
   851 2.461890e+06 2028-04-28 18:25       86.4 undated (future sectors [122, 129]) prediction
   852 2.461894e+06 2028-05-02 05:08       86.5 undated (future sectors [122, 129]) prediction
   853 2.461897e+06 2028-05-05 15:51       86.7 undated (future sectors [122, 129]) prediction
Outcomes defined in advance (QLP or SPOC light curve of the test sector, or a TESScut fixed-aperture extraction, transit-masked biweight detrend): (1) recovered - a box of
depth 0.5-1.5x and duration 0.7-1.3x the values above within +-3 sigma_min (and in any case within +-30 min) of >= 2 predicted times, stacked SNR >= 5;
(2) inconsistent - a comparable dip exists but its times differ by > 30 min from every prediction; (3) excluded - stacked depth at the predicted phase
< 0.3x at 3 sigma with >= 2 transits fully covered; (4) insufficient - fewer than 2 predicted transits covered. The QLP S99-S105 timestamp error shifts
these ephemerides by < 1.5 min (review, timing_propagation.json). Generated by scripts/prereg_v2.py 376225363 --freeze.


**Addendum 2026-10-20 (timing rule):** the phrase "and in any case within +-30 min" above misstates the rule. The governing rule is the public protocol's (Zenodo 10.5281/zenodo.23462442): stacked timing offset within max(3 sigma_pred, 30 min), as implemented in the frozen evaluator scripts/prereg_test.py. No prediction, CSV or checksum is changed. See CLARIFICATION_TIMING_RULE_2026-10-20.md.
