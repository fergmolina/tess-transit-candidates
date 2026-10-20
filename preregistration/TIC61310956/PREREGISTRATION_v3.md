# Pre-registered transit predictions v3 - TIC 61310956
Frozen: 2026-10-19 14:09:02 UTC. Author: Fernando Molina (Independent researcher, ORCID 0009-0002-2872-3406). Analysis with Claude (Anthropic) under the author's direction.
First freeze for this object (v2 tooling: all-sector ephemeris). v3 supersedes v2 (SHA of v2 CSV kept on record in final_ephemeris_v2.json); reason: v2 counted the S22 and S45 transits twice (QLP and SPOC rows), see results/referee_round2/REFEREE_REPORT.md. Reason (external review 2026-10-18,
results/external_review_allsky/REVIEW.md): v1 timed only the 200-s sectors (vet.py min_pts cut), ignoring 2018-2021 data; v2 fits one time offset per
sector from ALL sectors (raw SAP flux, cadence-aware model, local baselines; SPOC 2-min sectors where they exist) on top of the all-data BLS ephemeris.
Ephemeris: T0 = BTJD 3262.56598 +- 14.2 min (epoch 82), P = 16.537966 +- 0.000150 d (chi2/dof 7.2/2, inflation x1.90); all-data BLS P = 16.537846.
Sector times used: S22 SPOC 2-min (2 ev, O-C -2.0 +- 3.6 min), S45 SPOC 2-min (1 ev, O-C +2.4 +- 4.2 min), S46 QLP SAP (1 ev, O-C +24.8 +- 12.6 min), S72 QLP SAP (2 ev, O-C -19.7 +- 12.0 min).
Depth per sector (fixed shape, local baseline, raw SAP): S22 905, S45 1224, S46 1436, S72 1276 ppm.
All-sky round-2 candidate: isolated K dwarf (TYC 1428-1096-1, Tmag 10.6; nearest star able to mimic the signal 82 arcsec away, needing 20 %; no Gaia DR3 source within 60 arcsec can produce the depth). P = 16.538 d, depth 1.0-1.5 ppt, T14 3.3 h; six events in QLP FFI data (S22 x2, S45, S46, S72 x2); the three 2020-2021 events are also recovered in the SPOC 2-min light curves at the QLP ephemeris (1068 +- 240 ppm, 4.5 sigma empirical; the 2-min data alone do not yield the period). Density from the shape consistent with the catalogue (1.4 +0.6/-0.8), secondary -29 +- 102 ppm, odd/even 1.2 sigma, blind holdout recovered in both testable years, flux-loss centroid consistent with the target in S22, S45 and S72 (0.1-0.3 px, calibrated errors 0.14-0.24 px), TRICERATOPS FPP 0.020 / NFPP 0.000 (no contrast curve; above the 0.015 validation threshold). Host is a Gaia DR3 / VSX rotational variable. No TOI/CTOI/TCE within 60 arcsec; round-2 prior-detection sweep: no prior report (the period and depth were public as a row of our own tables/allsky_testable_soon.csv from 2026-10-18 23:24 to 2026-10-19 12:16 UTC). Ephemeris: one time per sector (SPOC 2-min times for S22 and S45, QLP for S46 and S72).
Reference values for the outcome clauses: depth 1334 ppm (raw SAP, all sectors), T14 2.70 h.
SHA-256 of predicted_transits_2026_2027_v3.csv: 76e892963501c62cdedcf07a94b1f2e65bbc47f91427bdd6006ec2250ab1da63
**Test of record: ground-based photometry (no TESS coverage of this star through Sector 134); any observer may test any listed epoch.** Predicted mid-transits (sigma_min = 1-sigma timing uncertainty at that epoch):
 epoch    tc_bjd_tdb              utc  sigma_min         tess_sector     status
   147 2461337.53374 2026-10-24 00:52   27.70000 none (ground-based) prediction
   148 2461354.07171 2026-11-09 13:44   27.90000 none (ground-based) prediction
   149 2461370.60967 2026-11-26 02:37   28.20000 none (ground-based) prediction
   150 2461387.14764 2026-12-12 15:29   28.40000 none (ground-based) prediction
   151 2461403.68560 2026-12-29 04:21   28.60000 none (ground-based) prediction
   152 2461420.22357 2027-01-14 17:14   28.80000 none (ground-based) prediction
   153 2461436.76154 2027-01-31 06:08   29.00000 none (ground-based) prediction
   154 2461453.29950 2027-02-16 19:02   29.20000 none (ground-based) prediction
   155 2461469.83747 2027-03-05 07:56   29.40000 none (ground-based) prediction
   156 2461486.37543 2027-03-21 20:52   29.60000 none (ground-based) prediction
   157 2461502.91340 2027-04-07 09:47   29.90000 none (ground-based) prediction
   158 2461519.45136 2027-04-23 22:44   30.10000 none (ground-based) prediction
   159 2461535.98933 2027-05-10 11:41   30.30000 none (ground-based) prediction
   160 2461552.52730 2027-05-27 00:38   30.50000 none (ground-based) prediction
   161 2461569.06526 2027-06-12 13:35   30.70000 none (ground-based) prediction
   162 2461585.60323 2027-06-29 02:31   30.90000 none (ground-based) prediction
   163 2461602.14119 2027-07-15 15:28   31.10000 none (ground-based) prediction
   164 2461618.67916 2027-08-01 04:24   31.30000 none (ground-based) prediction
   165 2461635.21712 2027-08-17 17:19   31.60000 none (ground-based) prediction
   166 2461651.75509 2027-09-03 06:14   31.80000 none (ground-based) prediction
   167 2461668.29305 2027-09-19 19:08   32.00000 none (ground-based) prediction
   168 2461684.83102 2027-10-06 08:02   32.20000 none (ground-based) prediction
   169 2461701.36899 2027-10-22 20:55   32.40000 none (ground-based) prediction
   170 2461717.90695 2027-11-08 09:47   32.60000 none (ground-based) prediction
   171 2461734.44492 2027-11-24 22:40   32.80000 none (ground-based) prediction
   172 2461750.98288 2027-12-11 11:32   33.00000 none (ground-based) prediction
   173 2461767.52085 2027-12-28 00:24   33.30000 none (ground-based) prediction
   174 2461784.05881 2028-01-13 13:17   33.50000 none (ground-based) prediction
   175 2461800.59678 2028-01-30 02:10   33.70000 none (ground-based) prediction
   176 2461817.13475 2028-02-15 15:04   33.90000 none (ground-based) prediction
   177 2461833.67271 2028-03-03 03:59   34.10000 none (ground-based) prediction
   178 2461850.21068 2028-03-19 16:54   34.30000 none (ground-based) prediction
   179 2461866.74864 2028-04-05 05:50   34.50000 none (ground-based) prediction
   180 2461883.28661 2028-04-21 18:46   34.80000 none (ground-based) prediction
   181 2461899.82457 2028-05-08 07:43   35.00000 none (ground-based) prediction
Outcomes defined in advance (ground-based light curve, <= 1.5 mmag per 10-min bin, covering the predicted time +-3 sigma_min plus >= 1 h baseline on each side): (1) recovered - a dip of depth 0.5-1.5x and duration 0.7-1.3x the reference values within +-3 sigma_min of the predicted time on >= 2 epochs, each at SNR >= 4; (2) inconsistent - a comparable dip exists but its time differs by > 3 sigma_min from the prediction on >= 2 epochs; (3) excluded - no dip > 0.3x the reference depth (3 sigma) with >= 2 predicted windows fully covered at the required precision; (4) insufficient - fewer than 2 windows covered. Generated by scripts/prereg_v2.py 61310956 --freeze --version 3 --ground.


**Clarification 2026-10-20 (before any ground observation of a predicted transit; after the external dossier referee, results/referee_round2/REFEREE_REPORT_dossiers_external.md):**
1. **Reference duration.** The frozen reference line gives T14 2.70 h (the BLS grid duration), while the description above quotes the median shape-fit duration, about 3.3 h. **The frozen 2.70 h governs the outcome clauses**: duration band 0.7-1.3 x 2.70 = 1.89-3.51 h, which contains the 3.3-h shape value. It is not replaced by 3.3 h. For planning, observations should cover the predicted time +-3 sigma_min plus the longer 3.3-h duration plus >= 1 h of baseline on each side, about 8.1-8.2 h around the 2026-2027 epochs, not the ~7 h suggested earlier. A shorter sequence covers less than the full support and is reported as such; it is not by itself an "excluded" observation.
2. **Epoch 83.** The CSV row for epoch 83 (status "before freeze, untested", sector "none (ground-based)") is the second Sector 72 transit, which is part of the training data. It is not an untested ground-based prediction and is not a test epoch.
3. **Time columns.** For observing, use the geocentric UTC contact times, or topocentric times computed consistently from BJD_TDB. The epoch-151 geocentric mid-time is 2026-12-29 04:21:53 UTC.
4. **Odd/even.** The odd/even depth difference is baseline-sensitive (1.2 sigma on detrended flux; 3.75 sigma on raw SAP with a global baseline; 1.76 sigma with local-linear baselines). A ground result will be reported with per-event depths.

No prediction, CSV byte or checksum is changed.
