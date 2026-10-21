# Pre-registered transit predictions v3 - TIC 53825235
Frozen: 2026-10-21 02:57:37 UTC. Author: Fernando Molina (Independent researcher, ORCID 0009-0002-2872-3406). Analysis with Claude (Anthropic) under the author's direction.
First freeze for this object (v2 tooling: all-sector ephemeris). v3 supersedes v2 (SHA of v2 CSV kept on record in final_ephemeris_v2.json); reason: v2 listed no future predictions (generator capped at 399 epochs; last epoch 2025-08-23). The v3 that DECISIONS 68 required was never made. v3 has the identical ephemeris (reproduced exactly). S108 and the first part of S109 were observed before this freeze and are labelled retrodictions; the authors have not examined any S106+ data of this star (the generator refuses them), but these epochs are not prospective. S109 after the freeze and S110 are predictions. Reason (external review 2026-10-18,
results/external_review_allsky/REVIEW.md): v1 timed only the 200-s sectors (vet.py min_pts cut), ignoring 2018-2021 data; v2 fits one time offset per
sector from ALL sectors (raw SAP flux, cadence-aware model, local baselines; SPOC 2-min sectors where they exist) on top of the all-data BLS ephemeris.
Ephemeris: T0 = BTJD 3676.94846 +- 1.8 min (epoch 3764), P = 0.586599 +- 0.000003 d (chi2/dof 0.0/0, inflation x1.00); all-data BLS P = 0.586599.
Sector times used: S87 QLP SAP (35 ev, O-C +0.0 +- 1.8 min).
Depth per sector (fixed shape, local baseline, raw SAP): S87 339 ppm.
See ERRATUM_PREDICTION_HORIZON_2026-10-21.

Reference values for the outcome clauses: depth 245 ppm (raw SAP, all sectors), T14 1.10 h.
SHA-256 of predicted_transits_2026_2027_v3.csv: 1408a7cda5e0d01a573ab9c36cb6159f05ebbc84bbc5bea3398ab16cecee4aab
**Test of record: next TESS sector(s).** Predicted mid-transits (sigma_min = 1-sigma timing uncertainty at that epoch):
 epoch    tc_bjd_tdb              utc  sigma_min tess_sector     status
  4886 2461335.11266 2026-10-21 14:40    5.20000         109 prediction
  4887 2461335.69926 2026-10-22 04:44    5.20000         109 prediction
  4888 2461336.28586 2026-10-22 18:49    5.20000         109 prediction
  4889 2461336.87245 2026-10-23 08:54    5.20000         109 prediction
  4890 2461337.45905 2026-10-23 22:58    5.20000         109 prediction
  4891 2461338.04565 2026-10-24 13:03    5.20000         109 prediction
  4892 2461338.63225 2026-10-25 03:08    5.20000         109 prediction
  4893 2461339.21885 2026-10-25 17:12    5.20000         109 prediction
  4894 2461339.80545 2026-10-26 07:17    5.20000         109 prediction
  4895 2461340.39205 2026-10-26 21:22    5.20000         109 prediction
  4896 2461340.97865 2026-10-27 11:26    5.30000         109 prediction
  4897 2461341.56525 2026-10-28 01:31    5.30000         109 prediction
  4898 2461342.15185 2026-10-28 15:36    5.30000         109 prediction
  4899 2461342.73845 2026-10-29 05:40    5.30000         109 prediction
  4900 2461343.32505 2026-10-29 19:45    5.30000         109 prediction
  4901 2461343.91164 2026-10-30 09:49    5.30000         109 prediction
  4902 2461344.49824 2026-10-30 23:54    5.30000         109 prediction
  4903 2461345.08484 2026-10-31 13:59    5.30000         109 prediction
  4904 2461345.67144 2026-11-01 04:03    5.30000         110 prediction
  4905 2461346.25804 2026-11-01 18:08    5.30000         110 prediction
  4906 2461346.84464 2026-11-02 08:13    5.30000         110 prediction
  4907 2461347.43124 2026-11-02 22:17    5.30000         110 prediction
  4908 2461348.01784 2026-11-03 12:22    5.30000         110 prediction
  4909 2461348.60444 2026-11-04 02:27    5.30000         110 prediction
  4910 2461349.19104 2026-11-04 16:31    5.30000         110 prediction
  4911 2461349.77764 2026-11-05 06:36    5.30000         110 prediction
  4912 2461350.36423 2026-11-05 20:41    5.30000         110 prediction
  4913 2461350.95083 2026-11-06 10:45    5.30000         110 prediction
  4914 2461351.53743 2026-11-07 00:50    5.30000   110 (gap) prediction
  4915 2461352.12403 2026-11-07 14:55    5.30000         110 prediction
  4916 2461352.71063 2026-11-08 04:59    5.30000         110 prediction
  4917 2461353.29723 2026-11-08 19:04    5.30000         110 prediction
  4918 2461353.88383 2026-11-09 09:09    5.30000         110 prediction
  4919 2461354.47043 2026-11-09 23:13    5.30000         110 prediction
  4920 2461355.05703 2026-11-10 13:18    5.30000         110 prediction
  4921 2461355.64363 2026-11-11 03:23    5.40000         110 prediction
  4922 2461356.23023 2026-11-11 17:27    5.40000         110 prediction
  4923 2461356.81682 2026-11-12 07:32    5.40000         110 prediction
  4924 2461357.40342 2026-11-12 21:36    5.40000         110 prediction
  4925 2461357.99002 2026-11-13 11:41    5.40000         110 prediction
  4926 2461358.57662 2026-11-14 01:46    5.40000         110 prediction
  4927 2461359.16322 2026-11-14 15:50    5.40000         110 prediction
  4928 2461359.74982 2026-11-15 05:55    5.40000         110 prediction
  4929 2461360.33642 2026-11-15 20:00    5.40000         110 prediction
  4930 2461360.92302 2026-11-16 10:04    5.40000         110 prediction
  4931 2461361.50962 2026-11-17 00:09    5.40000         110 prediction
  4932 2461362.09622 2026-11-17 14:14    5.40000         110 prediction
  4933 2461362.68282 2026-11-18 04:18    5.40000         110 prediction
  4934 2461363.26941 2026-11-18 18:23    5.40000         110 prediction
  4935 2461363.85601 2026-11-19 08:28    5.40000         110 prediction
  4936 2461364.44261 2026-11-19 22:32    5.40000   110 (gap) prediction
  4937 2461365.02921 2026-11-20 12:37    5.40000         110 prediction
  4938 2461365.61581 2026-11-21 02:42    5.40000         110 prediction
  4939 2461366.20241 2026-11-21 16:46    5.40000         110 prediction
  4940 2461366.78901 2026-11-22 06:51    5.40000         110 prediction
  4941 2461367.37561 2026-11-22 20:56    5.40000         110 prediction
  4942 2461367.96221 2026-11-23 11:00    5.40000         110 prediction
  4943 2461368.54881 2026-11-24 01:05    5.40000         110 prediction
  4944 2461369.13541 2026-11-24 15:10    5.40000         110 prediction
  4945 2461369.72200 2026-11-25 05:14    5.50000         110 prediction
  4946 2461370.30860 2026-11-25 19:19    5.50000         110 prediction
Outcomes defined in advance (QLP or SPOC light curve of the test sector, transit-masked biweight detrend; no TESScut fallback - withdrawn 2026-10-20 in conformance v2.1): (1) recovered - a box of depth 0.5-1.5x and duration 0.7-1.3x the reference values at >= 2 covered predicted transit windows, stacked SNR >= 5, timing gate |sum(w_i dt_i)/sum(w_i)| <= max(3 mean(sigma_min,i), 30 min) with w_i = 1/depth_err_i^2 over the coverage-qualified windows (frozen evaluator; inverse depth-variance weights); duration and full-coverage criteria are assessed under the separately versioned conformance procedure (see CLARIFICATION_TIMING_RULE_2026-10-20.md); (2) inconsistent - a comparable dip exists but its times differ by > 30 min from every prediction; (3) excluded - stacked depth at the predicted phase < 0.3x at 3 sigma with >= 2 transits fully covered; (4) insufficient - fewer than 2 predicted transits covered. No QLP S99+ sector time enters this ephemeris. Generated by scripts/prereg_v2.py 53825235 --freeze --version 3.

**Dated correction 2026-10-21 (appended; frozen CSV unchanged).** The generated header above reads "First freeze for this object"; that is
a template error. This is the second version for this object; v3 supersedes v2 (CSV SHA in final_ephemeris_v2.json).
