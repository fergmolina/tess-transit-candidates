# Pre-registered transit predictions v2 - TIC 3367979
Frozen: 2026-10-19 12:47:13 UTC. Author: Fernando Molina (Independent researcher, ORCID 0009-0002-2872-3406). Analysis with Claude (Anthropic) under the author's direction.
First freeze for this object (v2 tooling: all-sector ephemeris). Reason (external review 2026-10-18,
results/external_review_allsky/REVIEW.md): v1 timed only the 200-s sectors (vet.py min_pts cut), ignoring 2018-2021 data; v2 fits one time offset per
sector from ALL sectors (raw SAP flux, cadence-aware model, local baselines; SPOC 2-min sectors where they exist) on top of the all-data BLS ephemeris.
Ephemeris: T0 = BTJD 3273.30254 +- 1.8 min (epoch 423), P = 3.439623 +- 0.000009 d (chi2/dof 0.4/2, inflation x1.00); all-data BLS P = 3.439599.
Sector times used: S43 QLP SAP (6 ev, O-C +0.7 +- 3.0 min), S45 QLP SAP (7 ev, O-C -1.0 +- 3.6 min), S71 QLP SAP (6 ev, O-C -4.3 +- 8.4 min), S72 QLP SAP (5 ev, O-C +0.2 +- 1.8 min).
Depth per sector (fixed shape, local baseline, raw SAP): S43 993, S45 693, S71 749, S72 1071 ppm.
Round-2 object with no TESS coverage through Sector 134; ground-based ephemeris test only. See results/allsky_classA_round2_outcomes.csv for vetting status (marginal/weak/rediscovery as listed).
SHA-256 of predicted_transits_2026_2027_v2.csv: ea98dcc1f26fd65dad16d02137d3f777a770544912b57812b1356f049b53de25
**Test of record: next TESS sector(s).** Predicted mid-transits (conservative window +-20 min):
 epoch   tc_bjd_tdb              utc  sigma_min         tess_sector     status
   732 2.461336e+06 2026-10-22 15:24        5.3 none (ground-based) prediction
   733 2.461340e+06 2026-10-26 01:56        5.3 none (ground-based) prediction
   734 2.461343e+06 2026-10-29 12:29        5.3 none (ground-based) prediction
   735 2.461346e+06 2026-11-01 23:02        5.3 none (ground-based) prediction
   736 2.461350e+06 2026-11-05 09:35        5.3 none (ground-based) prediction
   737 2.461353e+06 2026-11-08 20:07        5.3 none (ground-based) prediction
   738 2.461357e+06 2026-11-12 06:40        5.3 none (ground-based) prediction
   739 2.461360e+06 2026-11-15 17:13        5.4 none (ground-based) prediction
   740 2.461364e+06 2026-11-19 03:46        5.4 none (ground-based) prediction
   741 2.461367e+06 2026-11-22 14:19        5.4 none (ground-based) prediction
   742 2.461371e+06 2026-11-26 00:51        5.4 none (ground-based) prediction
   743 2.461374e+06 2026-11-29 11:24        5.4 none (ground-based) prediction
   744 2.461377e+06 2026-12-02 21:57        5.4 none (ground-based) prediction
   745 2.461381e+06 2026-12-06 08:30        5.4 none (ground-based) prediction
   746 2.461384e+06 2026-12-09 19:03        5.4 none (ground-based) prediction
   747 2.461388e+06 2026-12-13 05:36        5.5 none (ground-based) prediction
   748 2.461391e+06 2026-12-16 16:09        5.5 none (ground-based) prediction
   749 2.461395e+06 2026-12-20 02:42        5.5 none (ground-based) prediction
   750 2.461398e+06 2026-12-23 13:16        5.5 none (ground-based) prediction
   751 2.461401e+06 2026-12-26 23:49        5.5 none (ground-based) prediction
   752 2.461405e+06 2026-12-30 10:22        5.5 none (ground-based) prediction
   753 2.461408e+06 2027-01-02 20:55        5.5 none (ground-based) prediction
   754 2.461412e+06 2027-01-06 07:28        5.5 none (ground-based) prediction
   755 2.461415e+06 2027-01-09 18:02        5.6 none (ground-based) prediction
   756 2.461419e+06 2027-01-13 04:35        5.6 none (ground-based) prediction
   757 2.461422e+06 2027-01-16 15:08        5.6 none (ground-based) prediction
   758 2.461426e+06 2027-01-20 01:41        5.6 none (ground-based) prediction
   759 2.461429e+06 2027-01-23 12:15        5.6 none (ground-based) prediction
   760 2.461432e+06 2027-01-26 22:48        5.6 none (ground-based) prediction
   761 2.461436e+06 2027-01-30 09:22        5.6 none (ground-based) prediction
   762 2.461439e+06 2027-02-02 19:55        5.6 none (ground-based) prediction
   763 2.461443e+06 2027-02-06 06:28        5.7 none (ground-based) prediction
   764 2.461446e+06 2027-02-09 17:02        5.7 none (ground-based) prediction
   765 2.461450e+06 2027-02-13 03:35        5.7 none (ground-based) prediction
   766 2.461453e+06 2027-02-16 14:09        5.7 none (ground-based) prediction
   767 2.461457e+06 2027-02-20 00:42        5.7 none (ground-based) prediction
   768 2.461460e+06 2027-02-23 11:16        5.7 none (ground-based) prediction
   769 2.461463e+06 2027-02-26 21:49        5.7 none (ground-based) prediction
   770 2.461467e+06 2027-03-02 08:23        5.8 none (ground-based) prediction
   771 2.461470e+06 2027-03-05 18:56        5.8 none (ground-based) prediction
   772 2.461474e+06 2027-03-09 05:30        5.8 none (ground-based) prediction
   773 2.461477e+06 2027-03-12 16:04        5.8 none (ground-based) prediction
   774 2.461481e+06 2027-03-16 02:37        5.8 none (ground-based) prediction
   775 2.461484e+06 2027-03-19 13:11        5.8 none (ground-based) prediction
   776 2.461487e+06 2027-03-22 23:44        5.8 none (ground-based) prediction
   777 2.461491e+06 2027-03-26 10:18        5.8 none (ground-based) prediction
   778 2.461494e+06 2027-03-29 20:51        5.9 none (ground-based) prediction
   779 2.461498e+06 2027-04-02 07:25        5.9 none (ground-based) prediction
   780 2.461501e+06 2027-04-05 17:58        5.9 none (ground-based) prediction
   781 2.461505e+06 2027-04-09 04:32        5.9 none (ground-based) prediction
   782 2.461508e+06 2027-04-12 15:05        5.9 none (ground-based) prediction
   783 2.461512e+06 2027-04-16 01:39        5.9 none (ground-based) prediction
   784 2.461515e+06 2027-04-19 12:12        5.9 none (ground-based) prediction
   785 2.461518e+06 2027-04-22 22:46        5.9 none (ground-based) prediction
   786 2.461522e+06 2027-04-26 09:19        6.0 none (ground-based) prediction
   787 2.461525e+06 2027-04-29 19:53        6.0 none (ground-based) prediction
   788 2.461529e+06 2027-05-03 06:26        6.0 none (ground-based) prediction
   789 2.461532e+06 2027-05-06 16:59        6.0 none (ground-based) prediction
   790 2.461536e+06 2027-05-10 03:33        6.0 none (ground-based) prediction
   791 2.461539e+06 2027-05-13 14:06        6.0 none (ground-based) prediction
   792 2.461543e+06 2027-05-17 00:39        6.0 none (ground-based) prediction
   793 2.461546e+06 2027-05-20 11:13        6.0 none (ground-based) prediction
   794 2.461549e+06 2027-05-23 21:46        6.1 none (ground-based) prediction
   795 2.461553e+06 2027-05-27 08:19        6.1 none (ground-based) prediction
   796 2.461556e+06 2027-05-30 18:52        6.1 none (ground-based) prediction
   797 2.461560e+06 2027-06-03 05:25        6.1 none (ground-based) prediction
   798 2.461563e+06 2027-06-06 15:59        6.1 none (ground-based) prediction
   799 2.461567e+06 2027-06-10 02:32        6.1 none (ground-based) prediction
   800 2.461570e+06 2027-06-13 13:05        6.1 none (ground-based) prediction
   801 2.461573e+06 2027-06-16 23:38        6.1 none (ground-based) prediction
   802 2.461577e+06 2027-06-20 10:11        6.2 none (ground-based) prediction
   803 2.461580e+06 2027-06-23 20:44        6.2 none (ground-based) prediction
   804 2.461584e+06 2027-06-27 07:17        6.2 none (ground-based) prediction
   805 2.461587e+06 2027-06-30 17:50        6.2 none (ground-based) prediction
   806 2.461591e+06 2027-07-04 04:23        6.2 none (ground-based) prediction
   807 2.461594e+06 2027-07-07 14:56        6.2 none (ground-based) prediction
   808 2.461598e+06 2027-07-11 01:28        6.2 none (ground-based) prediction
   809 2.461601e+06 2027-07-14 12:01        6.2 none (ground-based) prediction
   810 2.461604e+06 2027-07-17 22:34        6.3 none (ground-based) prediction
   811 2.461608e+06 2027-07-21 09:07        6.3 none (ground-based) prediction
   812 2.461611e+06 2027-07-24 19:40        6.3 none (ground-based) prediction
   813 2.461615e+06 2027-07-28 06:12        6.3 none (ground-based) prediction
   814 2.461618e+06 2027-07-31 16:45        6.3 none (ground-based) prediction
   815 2.461622e+06 2027-08-04 03:18        6.3 none (ground-based) prediction
   816 2.461625e+06 2027-08-07 13:51        6.3 none (ground-based) prediction
   817 2.461629e+06 2027-08-11 00:23        6.3 none (ground-based) prediction
   818 2.461632e+06 2027-08-14 10:56        6.4 none (ground-based) prediction
   819 2.461635e+06 2027-08-17 21:29        6.4 none (ground-based) prediction
   820 2.461639e+06 2027-08-21 08:01        6.4 none (ground-based) prediction
   821 2.461642e+06 2027-08-24 18:34        6.4 none (ground-based) prediction
   822 2.461646e+06 2027-08-28 05:06        6.4 none (ground-based) prediction
Outcomes defined in advance (QLP or SPOC light curve of the test sector, or a TESScut fixed-aperture extraction, transit-masked biweight detrend): (1) recovered - a box of
depth 0.5-1.5x and duration 0.7-1.3x the values above within +-3 sigma_min (and in any case within +-30 min) of >= 2 predicted times, stacked SNR >= 5;
(2) inconsistent - a comparable dip exists but its times differ by > 30 min from every prediction; (3) excluded - stacked depth at the predicted phase
< 0.3x at 3 sigma with >= 2 transits fully covered; (4) insufficient - fewer than 2 predicted transits covered. The QLP S99-S105 timestamp error shifts
these ephemerides by < 1.5 min (review, timing_propagation.json). Generated by scripts/prereg_v2.py 3367979 --freeze.


**Addendum 2026-10-20 (timing rule):** the phrase "and in any case within +-30 min" above misstates the rule. The governing rule is the public protocol's (Zenodo 10.5281/zenodo.23462442): stacked timing offset within max(3 sigma_pred, 30 min), as implemented in the frozen evaluator scripts/prereg_test.py. No prediction, CSV or checksum is changed. See CLARIFICATION_TIMING_RULE_2026-10-20.md.

**Dated note 2026-10-21 (appended; frozen CSV unchanged).** This star has no TESS coverage through Sector 134, but this v2 was generated
without --ground: its text names "next TESS sector(s)" and the TESS outcome clauses, although its rows are labelled "none (ground-based)".
Its list also stops at epoch 822 (2027-08-28) because the generator then stopped after 399 epochs. v4 (frozen 2026-10-21, CSV b6c94c8e...)
is the ground registration with the same ephemeris (v3 is superseded). See ERRATUM_PREDICTION_HORIZON_2026-10-21.md.
