# Pre-registered transit predictions v2 - TIC 196514928
Frozen: 2026-10-20 00:43:22 UTC. Author: Fernando Molina (Independent researcher, ORCID 0009-0002-2872-3406). Analysis with Claude (Anthropic) under the author's direction.
First freeze for this object (v2 tooling: all-sector ephemeris). Reason (external review 2026-10-18,
results/external_review_allsky/REVIEW.md): v1 timed only the 200-s sectors (vet.py min_pts cut), ignoring 2018-2021 data; v2 fits one time offset per
sector from ALL sectors (raw SAP flux, cadence-aware model, local baselines; SPOC 2-min sectors where they exist) on top of the all-data BLS ephemeris.
Ephemeris: T0 = BTJD 3706.38734 +- 5.8 min (epoch 914), P = 2.392124 +- 0.000010 d (chi2/dof 23.3/3, inflation x2.79); all-data BLS P = 2.392112.
Sector times used: S8 QLP SAP (6 ev, O-C +11.0 +- 4.8 min), S34 QLP SAP (9 ev, O-C +6.9 +- 11.4 min), S35 QLP SAP (7 ev, O-C -1.7 +- 4.8 min), S62 QLP SAP (8 ev, O-C -8.3 +- 2.4 min), S88 QLP SAP (8 ev, O-C +5.7 +- 2.4 min).
Depth per sector (fixed shape, local baseline, raw SAP): S8 426, S34 589, S35 659, S62 599, S88 607 ppm.
Round-3 object (P 2.39 d, ~590 ppm, ~2.1 R_E). On target; triage pass (SNR 12.2, seen 4/4 years). Sector timings scatter (chi2/dof 23/3). No prior listing found in the sweep corpus. Test: Sector 109.
Reference values for the outcome clauses: depth 593 ppm (raw SAP, all sectors), T14 2.20 h.
SHA-256 of predicted_transits_2026_2027_v2.csv: 1fa2a7e068d35809c1f51ed7b021ecbd11e39ade86476d31879371333b853017
**Test of record: next TESS sector(s).** Predicted mid-transits (sigma_min = 1-sigma timing uncertainty at that epoch):
 epoch    tc_bjd_tdb              utc  sigma_min                  tess_sector     status
  1177 2461335.51603 2026-10-22 00:24    8.90000                          109 prediction
  1178 2461337.90816 2026-10-24 09:48    8.90000                          109 prediction
  1179 2461340.30028 2026-10-26 19:13    9.00000                          109 prediction
  1180 2461342.69240 2026-10-29 04:37    9.00000                          109 prediction
  1181 2461345.08453 2026-10-31 14:02    9.00000                          109 prediction
  1182 2461347.47665 2026-11-02 23:26    9.00000                          110 prediction
  1183 2461349.86878 2026-11-05 08:50    9.00000                          110 prediction
  1184 2461352.26090 2026-11-07 18:15    9.00000                          110 prediction
  1185 2461354.65303 2026-11-10 03:39    9.00000                          110 prediction
  1186 2461357.04515 2026-11-12 13:04    9.00000                          110 prediction
  1187 2461359.43727 2026-11-14 22:28    9.10000                          110 prediction
  1188 2461361.82940 2026-11-17 07:52    9.10000                          110 prediction
  1189 2461364.22152 2026-11-19 17:17    9.10000                          110 prediction
  1190 2461366.61365 2026-11-22 02:41    9.10000                          110 prediction
  1191 2461369.00577 2026-11-24 12:06    9.10000                          110 prediction
  1192 2461371.39790 2026-11-26 21:30    9.10000                          111 prediction
  1193 2461373.79002 2026-11-29 06:54    9.10000                          111 prediction
  1194 2461376.18214 2026-12-01 16:19    9.10000                          111 prediction
  1195 2461378.57427 2026-12-04 01:43    9.20000                          111 prediction
  1196 2461380.96639 2026-12-06 11:08    9.20000                          111 prediction
  1197 2461383.35852 2026-12-08 20:32    9.20000                          111 prediction
  1198 2461385.75064 2026-12-11 05:57    9.20000 111 (span only, gap unknown) prediction
  1199 2461388.14277 2026-12-13 15:21    9.20000 111 (span only, gap unknown) prediction
  1200 2461390.53489 2026-12-16 00:45    9.20000 111 (span only, gap unknown) prediction
  1201 2461392.92701 2026-12-18 10:10    9.20000 111 (span only, gap unknown) prediction
  1202 2461395.31914 2026-12-20 19:34    9.30000 111 (span only, gap unknown) prediction
  1203 2461397.71126 2026-12-23 04:59    9.30000 112 (span only, gap unknown) prediction
  1204 2461400.10339 2026-12-25 14:23    9.30000 112 (span only, gap unknown) prediction
  1205 2461402.49551 2026-12-27 23:48    9.30000 112 (span only, gap unknown) prediction
  1206 2461404.88764 2026-12-30 09:12    9.30000 112 (span only, gap unknown) prediction
  1207 2461407.27976 2027-01-01 18:37    9.30000 112 (span only, gap unknown) prediction
  1208 2461409.67188 2027-01-04 04:01    9.30000 112 (span only, gap unknown) prediction
  1209 2461412.06401 2027-01-06 13:26    9.30000 112 (span only, gap unknown) prediction
  1210 2461414.45613 2027-01-08 22:50    9.40000 112 (span only, gap unknown) prediction
  1211 2461416.84826 2027-01-11 08:15    9.40000 112 (span only, gap unknown) prediction
  1212 2461419.24038 2027-01-13 17:39    9.40000 112 (span only, gap unknown) prediction
  1213 2461421.63251 2027-01-16 03:04    9.40000 112 (span only, gap unknown) prediction
Outcomes defined in advance (QLP or SPOC light curve of the test sector, or a TESScut fixed-aperture extraction, transit-masked biweight detrend): (1) recovered - a box of depth 0.5-1.5x and duration 0.7-1.3x the reference values within +-3 sigma_min (and in any case within +-30 min) of >= 2 predicted times, stacked SNR >= 5; (2) inconsistent - a comparable dip exists but its times differ by > 30 min from every prediction; (3) excluded - stacked depth at the predicted phase < 0.3x at 3 sigma with >= 2 transits fully covered; (4) insufficient - fewer than 2 predicted transits covered. No QLP S99+ sector time enters this ephemeris. Generated by scripts/prereg_v2.py 196514928 --freeze --version 2.


**Addendum 2026-10-20 (timing rule):** the phrase "and in any case within +-30 min" above misstates the rule. The governing rule is the public protocol's (Zenodo 10.5281/zenodo.23462442): stacked timing offset within max(3 sigma_pred, 30 min), as implemented in the frozen evaluator scripts/prereg_test.py. No prediction, CSV or checksum is changed. See CLARIFICATION_TIMING_RULE_2026-10-20.md.

---
**Dated scoring amendment 2026-10-23 (before any test-sector photometry of this star is examined).** Each listed TESS sector is scored separately with the published conformance evaluator scripts/prereg_conformance.py v2.1 rc4 (SHA-256 a864b07ace8d3220a2d94a60513a488c8a5d87b54f41ebf510ff40ef1755311f), general rules only, using a per-sector config locked on 2026-10-24 00:18:34 UTC and bound by configs/conformance/LOCK_2026-10-23_S107_S121.json (SHA-256 a8731dfcb4a482f6...): S109: 196514928_S109.json (SHA-256 b460454b93e56e9b...) PRIMARY - test of record; S110: 196514928_S110.json (SHA-256 6a80b8ca514e1a07...); S111: 196514928_S111.json (SHA-256 07dac49a027a9387...); S112: 196514928_S112.json (SHA-256 2f8f2bc7f7868335...). Product QLP SAP_FLUX, release of record v01, QLP clock gate with the c0 prior results/qlp_clock_v2/196514928.json (SHA-256 a932676a275a367f...); the binding check scripts/validate_round4_inputs.py --lock <that file> must pass at each stage. Primary-sector rule: The primary sector is the test of record. It stays the test of record whatever its result, including INSUFFICIENT, CLOCK_UNVERIFIED or INVALID_INPUT; it is never replaced by a later sector. Later listed sectors are scored separately with their own configs and reported as further tests, never pooled with the primary. Reference values: depth 593.0 ppm, T14 2.2 h (PREREGISTRATION_v2.md reference-values line (frozen text)). Timing: max(3 mean sigma_min, 30 min) (CLARIFICATION_TIMING_RULE_2026-10-20.md); min(3 sigma, 30 min) reading also reported. The frozen scripts/prereg_test.py literal outputs (SAP_FLUX and DET_FLUX) are secondary readouts. Sector(s) S109 were already observed, or were being observed (S109 runs 2026-10-05 to 10-31), at this amendment, and public data products exist or will appear; the authors attest that no target-sector photometry of this star has been examined, so those tests are held-out checks of already-observed data, not prospective predictions (ERRATUM_S106 class). No prediction, ephemeris or checksum is changed. DECISIONS 166-167.
