# Pre-registered transit predictions v2 - TIC 80387959
Frozen: 2026-10-18 22:34:41 UTC. Author: Fernando Molina (Independent researcher, ORCID 0009-0002-2872-3406). Analysis with Claude (Anthropic) under the author's direction.
Supersedes v1 (PREREGISTRATION.md, SHA 4652f7a3...), which is kept unchanged on record. Reason (external review 2026-10-18,
results/external_review_allsky/REVIEW.md): v1 timed only the 200-s sectors (vet.py min_pts cut), ignoring 2018-2021 data; v2 fits one time offset per
sector from ALL sectors (raw SAP flux, cadence-aware model, local baselines; SPOC 2-min sectors where they exist) on top of the all-data BLS ephemeris.
Ephemeris: T0 = BTJD 4086.48634 +- 2.9 min (epoch 430), P = 4.192173 +- 0.000007 d (chi2/dof 3.3/4, inflation x1.00); v1 P = 4.192142, all-data BLS P = 4.192178.
Sector times used: S10 QLP SAP (3 ev, O-C -6.2 +- 7.8 min), S36 QLP SAP (5 ev, O-C +1.2 +- 4.8 min), S37 QLP SAP (4 ev, O-C +0.0 +- 3.0 min), S63 QLP SAP (5 ev, O-C +0.2 +- 1.8 min), S90 QLP SAP (6 ev, O-C +4.1 +- 4.2 min), S100 QLP SAP (4 ev, O-C -6.0 +- 4.8 min).
Depth per sector (fixed shape, local baseline, raw SAP): S10 871, S36 893, S37 961, S63 876, S90 712, S100 750 ppm.
External review (2026-10-18) corrections applied: v1 timed only 200-s sectors; the QLP two-level depth was a QLP per-sector normalisation artefact (fixed-aperture TESScut depths constant at 687 +- 36 ppm over six sectors, chi2 10.2/5) and the x1.5 depth uncertainty is withdrawn; pixel-level exclusion of the G=17.3 star at 7.6 arcsec is ~2.7 sigma (not 4.8/2.8/4.3) once sector-to-sector scatter of the loss position is included, the G=14.0 star at 13.7 arcsec ~4 sigma; TRICERATOPS FPP 0.047, NFPP 0.010 (indicative; below validation).
SHA-256 of predicted_transits_2026_2027_v2.csv: 5d0e7651818e62542d316ff5e8e598b5a8255b29b0ada693b8584b529827a3f4
**Test of record: next TESS sector(s).** Predicted mid-transits (conservative window +-20 min):
 epoch   tc_bjd_tdb              utc  sigma_min                  tess_sector     status
   498 2.461372e+06 2026-11-27 01:16        3.5                          111 prediction
   499 2.461376e+06 2026-12-01 05:53        3.5                          111 prediction
   500 2.461380e+06 2026-12-05 10:30        3.6                          111 prediction
   501 2.461384e+06 2026-12-09 15:06        3.6 111 (span only, gap unknown) prediction
   502 2.461388e+06 2026-12-13 19:43        3.6 111 (span only, gap unknown) prediction
   503 2.461393e+06 2026-12-18 00:20        3.6 111 (span only, gap unknown) prediction
   504 2.461397e+06 2026-12-22 04:57        3.6 111 (span only, gap unknown) prediction
   505 2.461401e+06 2026-12-26 09:33        3.6 112 (span only, gap unknown) prediction
   506 2.461405e+06 2026-12-30 14:10        3.6 112 (span only, gap unknown) prediction
   507 2.461409e+06 2027-01-03 18:47        3.6 112 (span only, gap unknown) prediction
   508 2.461413e+06 2027-01-07 23:23        3.6 112 (span only, gap unknown) prediction
   509 2.461418e+06 2027-01-12 04:00        3.6 112 (span only, gap unknown) prediction
   510 2.461422e+06 2027-01-16 08:37        3.6 112 (span only, gap unknown) prediction
   511 2.461426e+06 2027-01-20 13:14        3.7 113 (span only, gap unknown) prediction
   512 2.461430e+06 2027-01-24 17:50        3.7 113 (span only, gap unknown) prediction
   513 2.461434e+06 2027-01-28 22:27        3.7 113 (span only, gap unknown) prediction
   514 2.461439e+06 2027-02-02 03:04        3.7 113 (span only, gap unknown) prediction
   515 2.461443e+06 2027-02-06 07:41        3.7 113 (span only, gap unknown) prediction
   516 2.461447e+06 2027-02-10 12:17        3.7 113 (span only, gap unknown) prediction
   517 2.461451e+06 2027-02-14 16:54        3.7 114 (span only, gap unknown) prediction
   518 2.461455e+06 2027-02-18 21:31        3.7 114 (span only, gap unknown) prediction
   519 2.461460e+06 2027-02-23 02:08        3.7 114 (span only, gap unknown) prediction
   520 2.461464e+06 2027-02-27 06:44        3.7 114 (span only, gap unknown) prediction
   521 2.461468e+06 2027-03-03 11:21        3.7 114 (span only, gap unknown) prediction
   522 2.461472e+06 2027-03-07 15:58        3.8 114 (span only, gap unknown) prediction
   523 2.461476e+06 2027-03-11 20:34        3.8 114 (span only, gap unknown) prediction
Outcomes defined in advance (QLP or SPOC light curve of the test sector, or a TESScut fixed-aperture extraction, transit-masked biweight detrend): (1) recovered - a box of
depth 0.5-1.5x and duration 0.7-1.3x the values above within +-3 sigma_min (and in any case within +-30 min) of >= 2 predicted times, stacked SNR >= 5;
(2) inconsistent - a comparable dip exists but its times differ by > 30 min from every prediction; (3) excluded - stacked depth at the predicted phase
< 0.3x at 3 sigma with >= 2 transits fully covered; (4) insufficient - fewer than 2 predicted transits covered. The QLP S99-S105 timestamp error shifts
these ephemerides by < 1.5 min (review, timing_propagation.json). Generated by scripts/prereg_v2.py 80387959 --freeze.
