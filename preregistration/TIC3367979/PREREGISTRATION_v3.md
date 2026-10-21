# Pre-registered transit predictions v3 - TIC 3367979
Frozen: 2026-10-21 02:57:42 UTC. Author: Fernando Molina (Independent researcher, ORCID 0009-0002-2872-3406). Analysis with Claude (Anthropic) under the author's direction.
First freeze for this object (v2 tooling: all-sector ephemeris). v3 supersedes v2 (SHA of v2 CSV kept on record in final_ephemeris_v2.json); reason: v2's list stopped at epoch 822 (2027-08-28; generator capped at 399 epochs). v3 has the identical ephemeris (reproduced exactly) and lists through 2027; the 399 rows shared with v2 are identical. v2 and its hash stay on record. Reason (external review 2026-10-18,
results/external_review_allsky/REVIEW.md): v1 timed only the 200-s sectors (vet.py min_pts cut), ignoring 2018-2021 data; v2 fits one time offset per
sector from ALL sectors (raw SAP flux, cadence-aware model, local baselines; SPOC 2-min sectors where they exist) on top of the all-data BLS ephemeris.
Ephemeris: T0 = BTJD 3273.30254 +- 1.8 min (epoch 423), P = 3.439623 +- 0.000009 d (chi2/dof 0.4/2, inflation x1.00); all-data BLS P = 3.439599.
Sector times used: S43 QLP SAP (6 ev, O-C +0.7 +- 3.0 min), S45 QLP SAP (7 ev, O-C -1.0 +- 3.6 min), S71 QLP SAP (6 ev, O-C -4.3 +- 8.4 min), S72 QLP SAP (5 ev, O-C +0.2 +- 1.8 min).
Depth per sector (fixed shape, local baseline, raw SAP): S43 993, S45 693, S71 749, S72 1071 ppm.
See ERRATUM_PREDICTION_HORIZON_2026-10-21.

Reference values for the outcome clauses: depth 788 ppm (raw SAP, all sectors), T14 1.30 h.
SHA-256 of predicted_transits_2026_2027_v3.csv: 0e8f5ea10443cf1e9adda0c31d27f4d9da206cf600aa3375acd5166e10af3dfa
**Test of record: next TESS sector(s).** Predicted mid-transits (sigma_min = 1-sigma timing uncertainty at that epoch):
 epoch    tc_bjd_tdb              utc  sigma_min                 tess_sector     status
   732 2461336.14595 2026-10-22 15:24    5.30000 undated (future sectors []) prediction
   733 2461339.58558 2026-10-26 01:56    5.30000 undated (future sectors []) prediction
   734 2461343.02520 2026-10-29 12:29    5.30000 undated (future sectors []) prediction
   735 2461346.46482 2026-11-01 23:02    5.30000 undated (future sectors []) prediction
   736 2461349.90444 2026-11-05 09:35    5.30000 undated (future sectors []) prediction
   737 2461353.34407 2026-11-08 20:07    5.30000 undated (future sectors []) prediction
   738 2461356.78369 2026-11-12 06:40    5.30000 undated (future sectors []) prediction
   739 2461360.22331 2026-11-15 17:13    5.40000 undated (future sectors []) prediction
   740 2461363.66293 2026-11-19 03:46    5.40000 undated (future sectors []) prediction
   741 2461367.10256 2026-11-22 14:19    5.40000 undated (future sectors []) prediction
   742 2461370.54218 2026-11-26 00:51    5.40000 undated (future sectors []) prediction
   743 2461373.98180 2026-11-29 11:24    5.40000 undated (future sectors []) prediction
   744 2461377.42143 2026-12-02 21:57    5.40000 undated (future sectors []) prediction
   745 2461380.86105 2026-12-06 08:30    5.40000 undated (future sectors []) prediction
   746 2461384.30067 2026-12-09 19:03    5.40000 undated (future sectors []) prediction
   747 2461387.74029 2026-12-13 05:36    5.50000 undated (future sectors []) prediction
   748 2461391.17992 2026-12-16 16:09    5.50000 undated (future sectors []) prediction
   749 2461394.61954 2026-12-20 02:42    5.50000 undated (future sectors []) prediction
   750 2461398.05916 2026-12-23 13:16    5.50000 undated (future sectors []) prediction
   751 2461401.49878 2026-12-26 23:49    5.50000 undated (future sectors []) prediction
   752 2461404.93841 2026-12-30 10:22    5.50000 undated (future sectors []) prediction
   753 2461408.37803 2027-01-02 20:55    5.50000 undated (future sectors []) prediction
   754 2461411.81765 2027-01-06 07:28    5.50000 undated (future sectors []) prediction
   755 2461415.25728 2027-01-09 18:02    5.60000 undated (future sectors []) prediction
   756 2461418.69690 2027-01-13 04:35    5.60000 undated (future sectors []) prediction
   757 2461422.13652 2027-01-16 15:08    5.60000 undated (future sectors []) prediction
   758 2461425.57614 2027-01-20 01:41    5.60000 undated (future sectors []) prediction
   759 2461429.01577 2027-01-23 12:15    5.60000 undated (future sectors []) prediction
   760 2461432.45539 2027-01-26 22:48    5.60000 undated (future sectors []) prediction
   761 2461435.89501 2027-01-30 09:22    5.60000 undated (future sectors []) prediction
   762 2461439.33463 2027-02-02 19:55    5.60000 undated (future sectors []) prediction
   763 2461442.77426 2027-02-06 06:28    5.70000 undated (future sectors []) prediction
   764 2461446.21388 2027-02-09 17:02    5.70000 undated (future sectors []) prediction
   765 2461449.65350 2027-02-13 03:35    5.70000 undated (future sectors []) prediction
   766 2461453.09312 2027-02-16 14:09    5.70000 undated (future sectors []) prediction
   767 2461456.53275 2027-02-20 00:42    5.70000 undated (future sectors []) prediction
   768 2461459.97237 2027-02-23 11:16    5.70000 undated (future sectors []) prediction
   769 2461463.41199 2027-02-26 21:49    5.70000 undated (future sectors []) prediction
   770 2461466.85162 2027-03-02 08:23    5.80000 undated (future sectors []) prediction
   771 2461470.29124 2027-03-05 18:56    5.80000 undated (future sectors []) prediction
   772 2461473.73086 2027-03-09 05:30    5.80000 undated (future sectors []) prediction
   773 2461477.17048 2027-03-12 16:04    5.80000 undated (future sectors []) prediction
   774 2461480.61011 2027-03-16 02:37    5.80000 undated (future sectors []) prediction
   775 2461484.04973 2027-03-19 13:11    5.80000 undated (future sectors []) prediction
   776 2461487.48935 2027-03-22 23:44    5.80000 undated (future sectors []) prediction
   777 2461490.92897 2027-03-26 10:18    5.80000 undated (future sectors []) prediction
   778 2461494.36860 2027-03-29 20:51    5.90000 undated (future sectors []) prediction
   779 2461497.80822 2027-04-02 07:25    5.90000 undated (future sectors []) prediction
   780 2461501.24784 2027-04-05 17:58    5.90000 undated (future sectors []) prediction
   781 2461504.68747 2027-04-09 04:32    5.90000 undated (future sectors []) prediction
   782 2461508.12709 2027-04-12 15:05    5.90000 undated (future sectors []) prediction
   783 2461511.56671 2027-04-16 01:39    5.90000 undated (future sectors []) prediction
   784 2461515.00633 2027-04-19 12:12    5.90000 undated (future sectors []) prediction
   785 2461518.44596 2027-04-22 22:46    5.90000 undated (future sectors []) prediction
   786 2461521.88558 2027-04-26 09:19    6.00000 undated (future sectors []) prediction
   787 2461525.32520 2027-04-29 19:53    6.00000 undated (future sectors []) prediction
   788 2461528.76482 2027-05-03 06:26    6.00000 undated (future sectors []) prediction
   789 2461532.20445 2027-05-06 16:59    6.00000 undated (future sectors []) prediction
   790 2461535.64407 2027-05-10 03:33    6.00000 undated (future sectors []) prediction
   791 2461539.08369 2027-05-13 14:06    6.00000 undated (future sectors []) prediction
   792 2461542.52331 2027-05-17 00:39    6.00000 undated (future sectors []) prediction
   793 2461545.96294 2027-05-20 11:13    6.00000 undated (future sectors []) prediction
   794 2461549.40256 2027-05-23 21:46    6.10000 undated (future sectors []) prediction
   795 2461552.84218 2027-05-27 08:19    6.10000 undated (future sectors []) prediction
   796 2461556.28181 2027-05-30 18:52    6.10000 undated (future sectors []) prediction
   797 2461559.72143 2027-06-03 05:25    6.10000 undated (future sectors []) prediction
   798 2461563.16105 2027-06-06 15:59    6.10000 undated (future sectors []) prediction
   799 2461566.60067 2027-06-10 02:32    6.10000 undated (future sectors []) prediction
   800 2461570.04030 2027-06-13 13:05    6.10000 undated (future sectors []) prediction
   801 2461573.47992 2027-06-16 23:38    6.10000 undated (future sectors []) prediction
   802 2461576.91954 2027-06-20 10:11    6.20000 undated (future sectors []) prediction
   803 2461580.35916 2027-06-23 20:44    6.20000 undated (future sectors []) prediction
   804 2461583.79879 2027-06-27 07:17    6.20000 undated (future sectors []) prediction
   805 2461587.23841 2027-06-30 17:50    6.20000 undated (future sectors []) prediction
   806 2461590.67803 2027-07-04 04:23    6.20000 undated (future sectors []) prediction
   807 2461594.11766 2027-07-07 14:56    6.20000 undated (future sectors []) prediction
   808 2461597.55728 2027-07-11 01:28    6.20000 undated (future sectors []) prediction
   809 2461600.99690 2027-07-14 12:01    6.20000 undated (future sectors []) prediction
   810 2461604.43652 2027-07-17 22:34    6.30000 undated (future sectors []) prediction
   811 2461607.87615 2027-07-21 09:07    6.30000 undated (future sectors []) prediction
   812 2461611.31577 2027-07-24 19:40    6.30000 undated (future sectors []) prediction
   813 2461614.75539 2027-07-28 06:12    6.30000 undated (future sectors []) prediction
   814 2461618.19501 2027-07-31 16:45    6.30000 undated (future sectors []) prediction
   815 2461621.63464 2027-08-04 03:18    6.30000 undated (future sectors []) prediction
   816 2461625.07426 2027-08-07 13:51    6.30000 undated (future sectors []) prediction
   817 2461628.51388 2027-08-11 00:23    6.30000 undated (future sectors []) prediction
   818 2461631.95351 2027-08-14 10:56    6.40000 undated (future sectors []) prediction
   819 2461635.39313 2027-08-17 21:29    6.40000 undated (future sectors []) prediction
   820 2461638.83275 2027-08-21 08:01    6.40000 undated (future sectors []) prediction
   821 2461642.27237 2027-08-24 18:34    6.40000 undated (future sectors []) prediction
   822 2461645.71200 2027-08-28 05:06    6.40000 undated (future sectors []) prediction
   823 2461649.15162 2027-08-31 15:39    6.40000 undated (future sectors []) prediction
   824 2461652.59124 2027-09-04 02:12    6.40000 undated (future sectors []) prediction
   825 2461656.03086 2027-09-07 12:44    6.40000 undated (future sectors []) prediction
   826 2461659.47049 2027-09-10 23:17    6.50000 undated (future sectors []) prediction
   827 2461662.91011 2027-09-14 09:49    6.50000 undated (future sectors []) prediction
   828 2461666.34973 2027-09-17 20:22    6.50000 undated (future sectors []) prediction
   829 2461669.78935 2027-09-21 06:54    6.50000 undated (future sectors []) prediction
   830 2461673.22898 2027-09-24 17:27    6.50000 undated (future sectors []) prediction
   831 2461676.66860 2027-09-28 04:00    6.50000 undated (future sectors []) prediction
   832 2461680.10822 2027-10-01 14:32    6.50000 undated (future sectors []) prediction
   833 2461683.54785 2027-10-05 01:05    6.50000 undated (future sectors []) prediction
   834 2461686.98747 2027-10-08 11:37    6.60000 undated (future sectors []) prediction
   835 2461690.42709 2027-10-11 22:10    6.60000 undated (future sectors []) prediction
   836 2461693.86671 2027-10-15 08:43    6.60000 undated (future sectors []) prediction
   837 2461697.30634 2027-10-18 19:15    6.60000 undated (future sectors []) prediction
   838 2461700.74596 2027-10-22 05:48    6.60000 undated (future sectors []) prediction
   839 2461704.18558 2027-10-25 16:21    6.60000 undated (future sectors []) prediction
   840 2461707.62520 2027-10-29 02:53    6.60000 undated (future sectors []) prediction
   841 2461711.06483 2027-11-01 13:26    6.60000 undated (future sectors []) prediction
   842 2461714.50445 2027-11-04 23:59    6.70000 undated (future sectors []) prediction
   843 2461717.94407 2027-11-08 10:31    6.70000 undated (future sectors []) prediction
   844 2461721.38370 2027-11-11 21:04    6.70000 undated (future sectors []) prediction
   845 2461724.82332 2027-11-15 07:37    6.70000 undated (future sectors []) prediction
   846 2461728.26294 2027-11-18 18:10    6.70000 undated (future sectors []) prediction
   847 2461731.70256 2027-11-22 04:43    6.70000 undated (future sectors []) prediction
   848 2461735.14219 2027-11-25 15:16    6.70000 undated (future sectors []) prediction
   849 2461738.58181 2027-11-29 01:48    6.80000 undated (future sectors []) prediction
   850 2461742.02143 2027-12-02 12:21    6.80000 undated (future sectors []) prediction
   851 2461745.46105 2027-12-05 22:54    6.80000 undated (future sectors []) prediction
   852 2461748.90068 2027-12-09 09:27    6.80000 undated (future sectors []) prediction
   853 2461752.34030 2027-12-12 20:00    6.80000 undated (future sectors []) prediction
   854 2461755.77992 2027-12-16 06:33    6.80000 undated (future sectors []) prediction
   855 2461759.21954 2027-12-19 17:06    6.80000 undated (future sectors []) prediction
   856 2461762.65917 2027-12-23 03:40    6.80000 undated (future sectors []) prediction
   857 2461766.09879 2027-12-26 14:13    6.90000 undated (future sectors []) prediction
   858 2461769.53841 2027-12-30 00:46    6.90000 undated (future sectors []) prediction
Outcomes defined in advance (QLP or SPOC light curve of the test sector, transit-masked biweight detrend; no TESScut fallback - withdrawn 2026-10-20 in conformance v2.1): (1) recovered - a box of depth 0.5-1.5x and duration 0.7-1.3x the reference values at >= 2 covered predicted transit windows, stacked SNR >= 5, timing gate |sum(w_i dt_i)/sum(w_i)| <= max(3 mean(sigma_min,i), 30 min) with w_i = 1/depth_err_i^2 over the coverage-qualified windows (frozen evaluator; inverse depth-variance weights); duration and full-coverage criteria are assessed under the separately versioned conformance procedure (see CLARIFICATION_TIMING_RULE_2026-10-20.md); (2) inconsistent - a comparable dip exists but its times differ by > 30 min from every prediction; (3) excluded - stacked depth at the predicted phase < 0.3x at 3 sigma with >= 2 transits fully covered; (4) insufficient - fewer than 2 predicted transits covered. No QLP S99+ sector time enters this ephemeris. Generated by scripts/prereg_v2.py 3367979 --freeze --version 3.

**Dated correction 2026-10-21 (appended; frozen CSV unchanged).** The generated header above reads "First freeze for this object"; that is
a template error. This is the second version for this object; v3 supersedes v2 (CSV SHA in final_ephemeris_v2.json).

**Dated notice 2026-10-21 (appended; frozen CSV unchanged): v3 is superseded by v4 and is not a test of record.** v3 was generated without
--ground. Its numerical predictions agree with v2 for all 399 shared epochs, but its sector labels read "undated (future sectors [])"
instead of "none (ground-based)", and its text keeps the TESS-sector outcome clauses although this star has no TESS coverage through
Sector 134. The earlier claim that the shared rows are identical was wrong. v4 (CSV b6c94c8e...) is the ground registration.
