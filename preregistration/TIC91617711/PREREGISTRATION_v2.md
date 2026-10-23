# Pre-registered transit predictions v2 - TIC 91617711
Frozen: 2026-10-19 12:51:37 UTC. Author: Fernando Molina (Independent researcher, ORCID 0009-0002-2872-3406). Analysis with Claude (Anthropic) under the author's direction.
First freeze for this object (v2 tooling: all-sector ephemeris). Reason (external review 2026-10-18,
results/external_review_allsky/REVIEW.md): v1 timed only the 200-s sectors (vet.py min_pts cut), ignoring 2018-2021 data; v2 fits one time offset per
sector from ALL sectors (raw SAP flux, cadence-aware model, local baselines; SPOC 2-min sectors where they exist) on top of the all-data BLS ephemeris.
Ephemeris: T0 = BTJD 3261.89626 +- 7.8 min (epoch 50), P = 15.071405 +- 0.000800 d (chi2/dof 0.2/1, inflation x1.00); all-data BLS P = 15.071405.
Sector times used: S44 QLP SAP (2 ev, O-C -1.4 +- 8.4 min), S72 QLP SAP (2 ev, O-C +8.2 +- 20.4 min).
Depth per sector (fixed shape, local baseline, raw SAP): S44 2628, S72 1552 ppm.
Round-2 object with no TESS coverage through Sector 134; ground-based ephemeris test only. See results/allsky_classA_round2_outcomes.csv for vetting status (marginal/weak/rediscovery as listed).
SHA-256 of predicted_transits_2026_2027_v2.csv: 559b438ceac090042d0f8fd8e35f18fbc7c950a58ecfdafc894c2affcf9de661
**Test of record: next TESS sector(s).** Predicted mid-transits (conservative window +-20 min):
 epoch   tc_bjd_tdb              utc  sigma_min         tess_sector     status
   122 2.461347e+06 2026-11-02 12:49       83.3 none (ground-based) prediction
   123 2.461362e+06 2026-11-17 14:30       84.5 none (ground-based) prediction
   124 2.461377e+06 2026-12-02 16:11       85.6 none (ground-based) prediction
   125 2.461392e+06 2026-12-17 17:53       86.8 none (ground-based) prediction
   126 2.461407e+06 2027-01-01 19:35       87.9 none (ground-based) prediction
   127 2.461422e+06 2027-01-16 21:18       89.1 none (ground-based) prediction
   128 2.461437e+06 2027-01-31 23:02       90.2 none (ground-based) prediction
   129 2.461453e+06 2027-02-16 00:46       91.4 none (ground-based) prediction
   130 2.461468e+06 2027-03-03 02:30       92.5 none (ground-based) prediction
   131 2.461483e+06 2027-03-18 04:15       93.6 none (ground-based) prediction
   132 2.461498e+06 2027-04-02 06:00       94.8 none (ground-based) prediction
   133 2.461513e+06 2027-04-17 07:45       95.9 none (ground-based) prediction
   134 2.461528e+06 2027-05-02 09:30       97.1 none (ground-based) prediction
   135 2.461543e+06 2027-05-17 11:15       98.2 none (ground-based) prediction
   136 2.461558e+06 2027-06-01 12:59       99.4 none (ground-based) prediction
   137 2.461573e+06 2027-06-16 14:43      100.5 none (ground-based) prediction
   138 2.461588e+06 2027-07-01 16:26      101.7 none (ground-based) prediction
   139 2.461603e+06 2027-07-16 18:09      102.8 none (ground-based) prediction
   140 2.461618e+06 2027-07-31 19:51      104.0 none (ground-based) prediction
   141 2.461633e+06 2027-08-15 21:32      105.1 none (ground-based) prediction
   142 2.461648e+06 2027-08-30 23:14      106.3 none (ground-based) prediction
   143 2.461664e+06 2027-09-15 00:55      107.4 none (ground-based) prediction
   144 2.461679e+06 2027-09-30 02:35      108.6 none (ground-based) prediction
   145 2.461694e+06 2027-10-15 04:16      109.7 none (ground-based) prediction
   146 2.461709e+06 2027-10-30 05:57      110.9 none (ground-based) prediction
   147 2.461724e+06 2027-11-14 07:38      112.0 none (ground-based) prediction
   148 2.461739e+06 2027-11-29 09:19      113.2 none (ground-based) prediction
   149 2.461754e+06 2027-12-14 11:01      114.3 none (ground-based) prediction
   150 2.461769e+06 2027-12-29 12:43      115.5 none (ground-based) prediction
   151 2.461784e+06 2028-01-13 14:26      116.6 none (ground-based) prediction
   152 2.461799e+06 2028-01-28 16:09      117.8 none (ground-based) prediction
   153 2.461814e+06 2028-02-12 17:53      118.9 none (ground-based) prediction
   154 2.461829e+06 2028-02-27 19:38      120.1 none (ground-based) prediction
   155 2.461844e+06 2028-03-13 21:23      121.2 none (ground-based) prediction
   156 2.461859e+06 2028-03-28 23:07      122.4 none (ground-based) prediction
   157 2.461875e+06 2028-04-13 00:52      123.5 none (ground-based) prediction
   158 2.461890e+06 2028-04-28 02:37      124.7 none (ground-based) prediction
Outcomes defined in advance (QLP or SPOC light curve of the test sector, or a TESScut fixed-aperture extraction, transit-masked biweight detrend): (1) recovered - a box of
depth 0.5-1.5x and duration 0.7-1.3x the values above within +-3 sigma_min (and in any case within +-30 min) of >= 2 predicted times, stacked SNR >= 5;
(2) inconsistent - a comparable dip exists but its times differ by > 30 min from every prediction; (3) excluded - stacked depth at the predicted phase
< 0.3x at 3 sigma with >= 2 transits fully covered; (4) insufficient - fewer than 2 predicted transits covered. The QLP S99-S105 timestamp error shifts
these ephemerides by < 1.5 min (review, timing_propagation.json). Generated by scripts/prereg_v2.py 91617711 --freeze.


**Addendum 2026-10-20 (timing rule):** the phrase "and in any case within +-30 min" above misstates the rule. The governing rule is the public protocol's (Zenodo 10.5281/zenodo.23462442): stacked timing offset within max(3 sigma_pred, 30 min), as implemented in the frozen evaluator scripts/prereg_test.py. No prediction, CSV or checksum is changed. See CLARIFICATION_TIMING_RULE_2026-10-20.md.

---
**Dated note 2026-10-23 (v1.16).** The original ON_TARGET label used only finite rounded offsets. The corrected screen is AMBIGUOUS_INCOMPLETE because sector S71 supplied no finite offset. The remaining finite offsets are S72: 0.0275 px. This is not a calibrated host assignment or neighbour exclusion. Frozen predictions and scoring rules are unchanged. See corrections/CORRECTION_TRICERATOPS_PIXEL_2026-10-22.md.
