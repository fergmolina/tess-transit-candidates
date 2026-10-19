# Pre-registered transit predictions v2 - TIC 61310956
Frozen: 2026-10-19 12:45:32 UTC. Author: Fernando Molina (Independent researcher, ORCID 0009-0002-2872-3406). Analysis with Claude (Anthropic) under the author's direction.
First freeze for this object (v2 tooling: all-sector ephemeris). Reason (external review 2026-10-18,
results/external_review_allsky/REVIEW.md): v1 timed only the 200-s sectors (vet.py min_pts cut), ignoring 2018-2021 data; v2 fits one time offset per
sector from ALL sectors (raw SAP flux, cadence-aware model, local baselines; SPOC 2-min sectors where they exist) on top of the all-data BLS ephemeris.
Ephemeris: T0 = BTJD 3262.56581 +- 10.3 min (epoch 82), P = 16.537975 +- 0.000111 d (chi2/dof 8.8/4, inflation x1.48); all-data BLS P = 16.537846.
Sector times used: S22 QLP SAP (2 ev, O-C -12.7 +- 11.4 min), S22 SPOC 2-min (2 ev, O-C -0.7 +- 3.6 min), S45 QLP SAP (1 ev, O-C -2.8 +- 7.2 min), S45 SPOC 2-min (1 ev, O-C +3.2 +- 4.2 min), S46 QLP SAP (1 ev, O-C +25.6 +- 12.6 min), S72 QLP SAP (2 ev, O-C -19.4 +- 12.0 min).
Depth per sector (fixed shape, local baseline, raw SAP): S22 1058, S22 905, S45 1047, S45 1224, S46 1436, S72 1276 ppm.
All-sky round-2 candidate: isolated K dwarf (Tmag 10.6; nearest star able to mimic the signal is 82 arcsec away and would need 20 %). P = 16.538 d, ~1,100 ppm, 3.2 h; six transits in QLP FFI data (S22, S45, S46, S72) and an independent SPOC 2-min detection in S22+S45 (1068 +- 95 ppm, 11 sigma). rho_fit/rho_TIC 1.45, b 0.41, no secondary, odd/even consistent, blind holdout 2/2, dip on target by pixel test (0.16 px), TRICERATOPS FPP 0.020 / NFPP 0.000 (no contrast curve). No TOI/CTOI/TCE within 60 arcsec; prior-detection corpus grep clean (full sweep in progress at the freeze). No TESS coverage through Sector 134: the test of record is GROUND-BASED photometry of any predicted transit below (1 mmag precision over 5 h suffices); the frozen outcome rules of the protocol apply with the TESS sector replaced by the observing night.
SHA-256 of predicted_transits_2026_2027_v2.csv: 1f15a633e0e56a8a2e00329cf447d39de3be292d4d73055bde6032e98872ace0
**Test of record: next TESS sector(s).** Predicted mid-transits (conservative window +-20 min):
 epoch   tc_bjd_tdb              utc  sigma_min         tess_sector     status
   147 2.461338e+06 2026-10-24 00:52       20.3 none (ground-based) prediction
   148 2.461354e+06 2026-11-09 13:45       20.5 none (ground-based) prediction
   149 2.461371e+06 2026-11-26 02:37       20.6 none (ground-based) prediction
   150 2.461387e+06 2026-12-12 15:30       20.8 none (ground-based) prediction
   151 2.461404e+06 2026-12-29 04:22       20.9 none (ground-based) prediction
   152 2.461420e+06 2027-01-14 17:15       21.1 none (ground-based) prediction
   153 2.461437e+06 2027-01-31 06:08       21.3 none (ground-based) prediction
   154 2.461453e+06 2027-02-16 19:02       21.4 none (ground-based) prediction
   155 2.461470e+06 2027-03-05 07:57       21.6 none (ground-based) prediction
   156 2.461486e+06 2027-03-21 20:52       21.7 none (ground-based) prediction
   157 2.461503e+06 2027-04-07 09:48       21.9 none (ground-based) prediction
   158 2.461519e+06 2027-04-23 22:45       22.0 none (ground-based) prediction
   159 2.461536e+06 2027-05-10 11:41       22.2 none (ground-based) prediction
   160 2.461553e+06 2027-05-27 00:38       22.4 none (ground-based) prediction
   161 2.461569e+06 2027-06-12 13:35       22.5 none (ground-based) prediction
   162 2.461586e+06 2027-06-29 02:32       22.7 none (ground-based) prediction
   163 2.461602e+06 2027-07-15 15:29       22.8 none (ground-based) prediction
   164 2.461619e+06 2027-08-01 04:25       23.0 none (ground-based) prediction
   165 2.461635e+06 2027-08-17 17:20       23.1 none (ground-based) prediction
   166 2.461652e+06 2027-09-03 06:15       23.3 none (ground-based) prediction
   167 2.461668e+06 2027-09-19 19:09       23.5 none (ground-based) prediction
   168 2.461685e+06 2027-10-06 08:03       23.6 none (ground-based) prediction
   169 2.461701e+06 2027-10-22 20:56       23.8 none (ground-based) prediction
   170 2.461718e+06 2027-11-08 09:48       23.9 none (ground-based) prediction
   171 2.461734e+06 2027-11-24 22:40       24.1 none (ground-based) prediction
   172 2.461751e+06 2027-12-11 11:33       24.3 none (ground-based) prediction
   173 2.461768e+06 2027-12-28 00:25       24.4 none (ground-based) prediction
   174 2.461784e+06 2028-01-13 13:18       24.6 none (ground-based) prediction
   175 2.461801e+06 2028-01-30 02:11       24.7 none (ground-based) prediction
   176 2.461817e+06 2028-02-15 15:05       24.9 none (ground-based) prediction
   177 2.461834e+06 2028-03-03 04:00       25.0 none (ground-based) prediction
   178 2.461850e+06 2028-03-19 16:55       25.2 none (ground-based) prediction
   179 2.461867e+06 2028-04-05 05:51       25.4 none (ground-based) prediction
   180 2.461883e+06 2028-04-21 18:47       25.5 none (ground-based) prediction
   181 2.461900e+06 2028-05-08 07:44       25.7 none (ground-based) prediction
Outcomes defined in advance (QLP or SPOC light curve of the test sector, or a TESScut fixed-aperture extraction, transit-masked biweight detrend): (1) recovered - a box of
depth 0.5-1.5x and duration 0.7-1.3x the values above within +-3 sigma_min (and in any case within +-30 min) of >= 2 predicted times, stacked SNR >= 5;
(2) inconsistent - a comparable dip exists but its times differ by > 30 min from every prediction; (3) excluded - stacked depth at the predicted phase
< 0.3x at 3 sigma with >= 2 transits fully covered; (4) insufficient - fewer than 2 predicted transits covered. The QLP S99-S105 timestamp error shifts
these ephemerides by < 1.5 min (review, timing_propagation.json). Generated by scripts/prereg_v2.py 61310956 --freeze.
