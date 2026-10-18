# Multi-year TESS transit search for unreported planet candidates — methods and results

Author: Fernando Molina (Independent researcher). Analysis performed with Claude (Anthropic) under the author's direction.
Date: 2026-10-17. All code, data lists, logs and intermediate products are in `/Users/fernando/Desktop/NASA/`.
Status line for every object in this report: **candidate pending confirmation; no object here is a validated planet.**
Outcome in one line: two candidates survive — TIC 317134140 (0.5719 d, ~185 ppm, §6; plausible but unproven, decisive test S108–S110) and
TIC 89247735 (18.32 d, 1.0 %, §8; three unambiguous on-target transits in 2023/2025/2026, nature unknown). Everything else was rejected (§5, §7).

## 1. Objective
Search public TESS photometry for periodic transit-like dimming (0.01–0.5 % deep, hours long) that (a) repeats with the same
period and phase in observations from different years, (b) is not already listed in the TOI/CTOI/confirmed-planet catalogs or the
SPOC Threshold-Crossing-Event (TCE) tables, (c) survives standard false-positive tests, and (d) yields published-in-advance
transit times that future TESS sectors can falsify. The approach follows the methodology of Rabtsevich (2026) for TIC 4206066.

## 2. Data
* **Pool A — SPOC 2-minute light curves.** Newest sector on MAST at run time: Sector 107 (12,998 2-min targets, southern field,
  Dec −43° to −9°). Using the MAST bulk-download scripts for Sectors 1–107 we built a TIC→sectors map (592,581 unique 2-min targets)
  and kept S107 targets with 2-min data in ≥2 calendar years (9,283). TIC v8.2 parameters were queried for all of them and the
  dwarf cut applied (Tmag<13.5, Teff<6000 K, R<1 R☉ [or R unknown and Teff<4200 K], log g>4 or unknown, not flagged GIANT):
  **1,637 targets, 6,720 light-curve files (14 GB)**, each with 2–9 sectors spanning 2018–2026. Flux: PDCSAP, QUALITY==0.
* **Pool B — QLP full-frame-image light curves.** Newest QLP sector on MAST: Sector 104 (1,152,719 targets). TIC criteria query
  for the S104 footprint (Dec −73° to −27°): Tmag≤11.5, Teff≤5300 K, luminosity class DWARF, R<0.85 R☉, log g>4 → **3,413 stars**,
  of which only 52 overlap Pool A. Sectors per star from `tess-point`; QLP files for every sector 1–104 fetched directly from MAST
  (21,343 URLs attempted). Flux: QLP detrended flux (`DET_FLUX`, or `KSPSAP_FLUX` in older releases), QUALITY==0; QLP error
  columns are NaN for Sectors ≥94 and are replaced by the point-to-point scatter.
* **Known-signal catalogs** (downloaded 2026-10-17): ExoFOP TOI (8,151 rows), ExoFOP CTOI (5,138), NASA Exoplanet Archive
  `pscomppars` (6,144 planets with TIC IDs), and all 132 SPOC TCE statistics tables on MAST (single- and multi-sector runs;
  341,351 TCE rows, 75,503 unique TICs). A candidate is "known" if its TIC has a catalog period within 1 % of the candidate period
  or of its 2×, ½×, 3×, ⅓× aliases.

## 3. Search pipeline (`scripts/tsearch.py`, `scripts/search_pipeline.py`)
1. Per sector: normalise, drop points within 0.3 d of any gap >0.25 d and of the sector ends (removes thermal ramps and
   scattered-light edges that otherwise repeat every 13.7-d TESS orbit), biweight detrend (wotan, 0.5 d window), clip only upward
   5σ outliers so dips are preserved.
2. Per-sector box-least-squares (astropy BLS, SNR objective, durations 1–4 h, periods 0.5 d to half the baseline).
3. Stitched multi-year BLS on all sectors (10-min bins, periods 0.5–20 d, log-uniform frequency grid with step
   Δln f = d_min/(T·2) so that phase drift over the full baseline stays below half a transit; 0.5–0.9 million trial periods per star).
   Detection statistic SDE = (peak − running median)/robust MAD of the periodogram. Top three peaks kept with odd/even depths,
   secondary-eclipse depth (phase 0.5), per-year depth at fixed ephemeris.
4. Ranking (`scripts/rank.py`): known-period exclusion; physical filters: ≥3 transits, secondary <3σ, odd/even <5σ, duration ≤1.6×
   the central-transit duration expected from the TIC stellar density, depth <3 %, detections in ≥2 calendar years.
5. Triage (`scripts/triage.py`): per-event depths, single-event dominance, fraction of events within 0.5 d of a data gap, figures.
6. Vetting (`scripts/vet.py`): masked re-detrend, fine BLS refinement, inverted-light-curve null (same search on 2−F),
   per-sector/per-year depths, odd/even, secondary scan at all phases, batman transit fit (least squares + emcee), stellar density
   from the fit vs TIC, individual transit times and linear ephemeris (O−C), **blind test** (hold out one year; run an independent
   full BLS on the other years; predict the held-out transits from training-only ephemeris; compare with a 1000-trial random-phase
   null), SAP vs PDCSAP depth, Gaia DR3 neighbours within 2′ with the eclipse depth each would need, in-/out-of-transit difference
   image from the 2-min target pixel file with centroid offset, planet radius / equilibrium temperature, future transit times with
   propagated uncertainty labelled by upcoming TESS sector.
7. Null calibration (`scripts/null_calibration.py`): the identical stitched search on inverted light curves for a random subset of
   each pool gives the empirical distribution of the top-peak SDE in the absence of transits.

## 4. Positive control
TIC 4206066 (Rabtsevich 2026): see `results/control_TIC4206066/CONTROL_SUMMARY.md`. Single sectors give SDE 7–9 for the
3.18-d signal; the stitched S6+S32+S98 search returns P = 3.18279 d (SDE 14.2, 24 transits, 367 ppm) as the top peak and
11.1327 d (SDE 14.1) as the second — both reported signals recovered blind. Known TOIs in Pool A are recovered at the catalog
period (12 of 14 hosts in the first 269 targets processed), and all of them pass the physical filters.

## 5. Results

### 5.1 Pool A (SPOC 2-min, 1,637 dwarfs) — search outcome
* 1,637 targets searched (edge-trimmed v2 pipeline). Known-host recovery: 80 of 105 TOI/CTOI/confirmed hosts in the pool are
  recovered at the catalog period (the remainder are mostly longer-period or single-transit objects outside the 0.5–20 d grid).
* After the physical filters, 17 unreported signals had stitched SDE > 9 (`results/candidates_physical.csv`, `results/triage/`).
  Most are the 13–18 d family with 3–6 events that triage tags as gap-edge ramps or single-event dominated. Four were vetted in full:

| TIC | P (d) | depth (ppm) | verdict | decisive evidence |
|---|---|---|---|---|
| 299903841 | 3.3837 | 2740 (PDCSAP) | **rejected: blend** | CROWDSAP 0.146; SAP depth 466 ppm vs PDCSAP 2738; centroid shift 9σ; flux-loss centroid 1.9 px (39″) from target; fitted ρ★ 0.02 vs TIC 2.4 ρ☉; 84 Gaia neighbours within 2′ |
| 313934283 | 1.8260 | 400 | **rejected: noise** | inverted-light-curve search gives a higher SDE than the real one (margin −0.7); candidate period not recovered by a search of the training years in 3 of 4 blind holdouts; O−C χ²/dof 706/32 |
| 176798599 | 7.3345 | 3000 | **rejected: not recovered in archival data** | 8 events in S97/S106/S107 (2025–26) pass shape, odd/even, secondary, centroid and pixel tests (3.3 R⊕, 551 K if real), but every odd epoch falls in a Cycle-8 data gap, and the 2018 (S4) and 2020 (S31) FFI light curves show 550–900 ± 350–630 ppm at the predicted phase where 3000 ppm would be 5–8σ; blind BLS on S31 alone does not find the period; stitched all-years SDE drops to 7.4 |
| 317134140 (TOI-2514) | 0.57186 | 185 | **candidate — see §6** | second signal in a known TOI system; recovered independently in 2018, 2024, 2025, 2026 data; passes all tests so far |

### 5.2 Pool B (QLP FFI, 3,411 bright dwarfs, sectors 1–104) — search outcome
* 3,411 of 3,413 targets processed (`results/search_qlp/`, 2 had no usable sectors). Known-signal recovery (`scripts/poolb_known_recovery.py`,
  `results/poolb_known_recovery.csv`): the 40 known hosts carry 54 catalog signals; 22 are recovered as a top-3 stitched peak (18 as the
  top peak), 14 have periods outside the 0.5–20 d grid (radial-velocity planets at 25 d to 70 yr), and 18 are in-grid misses. Of those 18,
  12 are non-transiting radial-velocity planets (GJ 682 b, GJ 674 b, HD 181433 b, …) that no transit search can recover, 2 are the
  second planet of a system whose first planet we did recover (TOI-1130 b behind the 1.7 %-deep TOI-1130 c; TOI-1064.02 behind
  TOI-1064.01 — the pipeline does not mask and re-search), 1 is a 170-ppm TOI (TOI-6978.01) below the QLP noise for 10 transits, and
  2 are CTOIs without a catalog depth. So every transiting known signal deeper than ~300 ppm with a single dominant planet was recovered;
  the known Pool-B limitations are second planets and sub-200-ppm depths.
* The physical filters leave 1,867 signals, 198 with SDE > 9 (`results/candidates_physical_qlp.csv`). **Pool B is dominated by
  instrumental periods**: a density test on the top-peak periods (0.4 %-wide log-period bins, > 5× the local median and > 6 objects)
  flags 13 clusters at 12.7–14.1 d (half-sector/orbit) and 18.9–19.9 d (scattered-light recurrence); 29 % of all SDE > 9 top peaks lie
  between 12.5 and 14.5 d. Removing the flagged clusters, requiring ≥2 years with a detected depth and excluding
  `near_tess_orbit` periods leaves 106 (`results/candidates_physical_qlp_clean.csv`); 80 were triaged (`results/triage_qlp/`).
* Shared-period check: no second Pool-B star shows the 0.5719-d period of the Pool-A candidate to better than 0.06 %
  (closest: TIC 89413558 at 0.57222 d, TIC 57129024 at 0.57100 d — different periods at the stitched 5-year resolution); 0.5–0.6 d
  peaks are simply common in red-noise periodograms. One pair of neighbouring TICs (119221437/119222179, 32′ apart) has 1.591/1.589 d
  top peaks; these also differ by 0.13 % and are not the same signal.
* Seven signals that triage did not reject (consistent per-year depths, no gap-edge dominance) were examined further. Three were rejected
  from the search products and catalogs alone (234520293, 120707329, 364788827 in the table); four were vetted in full with `vet.py` plus a new
  pixel-level test for FFI-only stars (`scripts/ffi_pixel_test.py`: per-pixel transit-depth map from an 11×11 TESScut cutout with
  per-event local baselines, flux-loss centroid vs target and Gaia neighbours, depth vs aperture radius) and, where the ephemeris was
  built from earlier years, a forward test with our own cutout photometry in later sectors (`scripts/tesscut_forward_test.py`):

| TIC | P (d) | depth (ppm) | years | verdict | decisive evidence |
|---|---|---|---|---|---|
| 234520293 | 0.5645 | 183 | 2018–2026 | **rejected: harmonic of a known TCE** | 0.5645 d = 3/2 × 0.37636 d (SPOC TCE on this star); 0.7527 (2×) and 0.9408 (5/2×) d peaks present; a stellar-variability harmonic series |
| 367223147 | 0.5303 | 300 | 2019–2026 (top peak in 5 of 6 sectors) | **rejected: off-target blend** | TESScut depth map S66 and S39: flux-loss centroid 1.56 and 1.38 px (33″, 29″) from the target; depth rises with aperture radius (76 → 349 ppm, 1 → 2.5 px); fitted ρ★ 0.59 vs TIC 1.94 ρ☉; inverted-null margin only 2.7 |
| 469939201 | 4.4478 | 290 | 2018, 2020, 2023 | **rejected: off-target / not recovered in 2025–26** | QLP 2025–26 sectors unusable (rms 3×10⁵ ppm); forward test with our own 1.5-px TESScut photometry in S96/S103/S104: 14 predicted transits covered, stacked depth −57 ± 56 ppm where ≥ 290 ppm was expected (p = 0.92 vs random phases), blind BLS of the new data does not contain the period; depth map S68/S28: loss centroid 1.9/1.8 px off target |
| 119221437 | 1.5913 | 760 | 2019–2026 | **rejected: likely off-target blend** | depth map S66: loss centroid 1.15 px (24″) from target, depth rises with aperture (314 → 560 ppm, 1 → 3 px) |
| 120707329 | 2.0622 | 135 | 2019–2025, absent 2026 | **rejected** | per-year depths 266, 239, 179, 218 ppm then −1 ± 21 ppm in 2026 (S103+S104, same noise level): a strictly periodic transit cannot vanish |
| 364788827 | 2.9369 | 1609 | 2019–2026 | **rejected: variable-dilution blend** | per-year depths 225, 3664, 3020, 1528, 683 ppm (±90–150); TIC contamination ratio 0.50 |
| **89247735** | **18.3231** | **10,235** | **2023, 2025, 2026** | **candidate — see §8** | three individually 34–41σ flat-bottomed transits, on-target by pixel test, no TOI/CTOI/TCE/ExoFOP entry |

* The remaining ~100 clean SDE > 9 survivors are mostly 3–8-event signals at 11–20 d with depths 1–20 ppt whose per-year depths disagree
  or whose events sit at sector edges; they were not vetted individually and are listed in `results/candidates_physical_qlp_clean.csv`.

## 6. Candidate: TIC 317134140 (TOI-2514 host) — a second, 0.5719-day transit-like signal
**Status: candidate pending confirmation. Not validated. Pre-registered transit times are given in §6.6 for TESS Sectors 108–110.**

### 6.1 Star
TIC 317134140 = TOI-2514 (ExoFOP: TOI-2514.01, P = 6.395 d, 2.1 R⊕, planet candidate; 5 imaging, 4 spectroscopic and 2 time-series
follow-up entries exist). TIC v8.2: Tmag 10.667, Teff 5563 K, R★ = 0.977 R☉, log g 4.45, contamination ratio 0.034, Gaia G = 11.14,
RA 05:46:52.69, Dec −17:01:44.7. TESS coverage: 2-min SPOC in S6 (2018-12/2019-01), S87 (2024-12/2025-01), S98 (2025-10/11),
S107 (2026-06/07); FFI only in S32 and S33 (2020-11 to 2021-01); being observed now in S108 (2026-09/10, data not yet public),
S109 (current) and S110 (2026-11).

### 6.2 Detection (Pool A search)
Stitched 4-sector BLS: top peak **P = 0.5719 d, depth 175 ppm, 1.5 h, SDE 14.3, 166 transits**; second peak 6.4039 d (the known
TOI-2514.01, SDE 10.2); third peak 1.1437 d (the 2× harmonic). Single sectors: 0.5717 d is the top peak in S98 alone (SDE 10.4) and
sub-threshold in S6, S87, S107 (SDE 4–5), i.e. detectable only by stacking years. No SPOC TCE exists for this star at any period;
no TOI/CTOI at 0.5719 d or its aliases; no entry in `pscomppars`.

### 6.3 Vetting summary (`results/vet/317134140/`, TOI-2514.01 transits masked)
| test | result |
|---|---|
| fine BLS refinement | P = 0.571864 d, depth 190 ± 19 ppm (SNR 9.9), duration 1.50 h, 162 transits |
| inverted-light-curve search | real top SDE 13.2 vs inverted 7.0 → margin +6.2 |
| per-sector depth (ppm) | S6 129 ± 38, S32(FFI) 56 ± 36, S33(FFI) 192 ± 34, S87 106 ± 38, S98 220 ± 30, S107 220 ± 38 |
| odd / even | 171 ± 26 vs 168 ± 25 ppm (0.1σ) |
| secondary at phase 0.5 | 13 ± 17 ppm (none); no other phase above 5σ |
| transit shape (batman + emcee) | Rp/R★ = 0.0131 +0.0010/−0.0008, a/R★ = 2.67 +0.26/−0.47, b = 0.40 ± 0.3 |
| stellar density from a/R★ and P | 0.78 ρ☉ vs 1.05 ρ☉ from TIC (consistent) |
| SAP vs PDCSAP depth | 183 ± 18 vs 190 ppm (consistent; not a PDC artefact) |
| crowding | CROWDSAP 0.953–0.958 in every sector (uniform) |
| centroid shift (MOM_CENTR, in−out) | 0.1 millipixel (0.002″); the size expected for an on-target 190-ppm dip given the flux centroid sits 0.7 px from the target |
| per-pixel depth map (S98 TPF) | flux-loss centroid 0.64 ± 0.2 px (14″) from the target, on the target's PSF core (known-planet reference 0.46 px) |
| depth vs aperture (S98 / S107 TPF) | 1 px 196 ± 57; r≤1.5 px 155 ± 29 / 160 ± 36; pipeline 125 ± 33 / 153 ± 36; +1 ring 60 ± 42 / 90 ± 44; +2 rings 12 ± 52 / −3 ± 54 → depth largest on the target core and diluted by larger apertures, the opposite of a neighbour-sourced signal |
| Gaia DR3 neighbours | 36 within 2′; brightest within 1′: G = 14.75 at 24″ (would need a 0.5 % eclipse), G = 15.86 at 32″ (1.4 %); TESS cannot exclude a companion inside ~20″ |
| independent code path | fresh lightkurve downloads + Savitzky–Golay flatten + lightkurve BLS: top peak 0.57191 d in S98 alone (SDE 14.3) and 0.57173 d in S107 alone (SDE 11.3); TLS on S98 returns the 2× alias 1.1432 d |

### 6.4 Multi-year and blind tests
* **Season-holdout blind test** (`blind_seasons.json`): for each season, (P, T0) were fitted to the other seasons only and an independent
  full BLS was run on them; the held-out season was then measured at the predicted phase:

| held-out season | training BLS rank of 0.5719 d (SDE) | predicted-phase 1σ | depth at predicted phase | deepest box within ±3 h | random-phase null p |
|---|---|---|---|---|---|
| 2018–19 (S6, 2-min) | 1st (16.8) | 26 min | 64 ± 38 ppm (1.7σ) | 122 ppm at −0.25 h | 0.03 |
| 2020–21 (S32+S33, FFI, never searched) | 1st (14.5) | 2.7 min | **125 ± 25 ppm (5.0σ)** | at 0.00 h | <0.0005 |
| 2024–25 (S87) | 1st (16.4) | 2.1 min | 107 ± 38 ppm (2.8σ) | at 0.00 h | <0.0005 |
| 2025 (S98) | 1st (13.2) | 3.1 min | **226 ± 30 ppm (7.6σ)** | at 0.00 h | <0.0005 |
| 2026 (S107) | 1st (14.5) | 3.1 min | **206 ± 38 ppm (5.4σ)** | at 0.00 h | <0.0005 |

* **Archival FFI test** (`archival_2020_test.json`): S33 TESS-SPOC 10-min light curve searched blind returns **0.5718 d as its top
  peak** (SDE 7.0), and the depth at the phase predicted 1305 cycles back is 188 ± 36 ppm (5.2σ) within 12 min of the prediction.
  S32 (the preceding sector) shows only 20–75 ppm in four flux products (a 185-ppm transit would have been ~5σ). Crowding is identical
  in S32 and S33, so the S32 non-detection is unexplained; a constant depth across all six sectors is disfavoured (χ² ≈ 18.5 for 5 d.o.f.).
  This is the main open caveat and is exactly what S108–S110 will test.

### 6.5 Planet parameters if the signal is on the target
Rp = 0.0131 × 0.977 R☉ = **1.39 ± 0.1 R⊕**; a = 0.0121 AU (a/R★ 2.67); Teq ≈ 2400 K (zero albedo, full redistribution);
insolation ≈ 5600 S⊕. An ultra-short-period rocky planet interior to the 6.4-d candidate TOI-2514.01 would be a common
architecture. Dilution: CROWDSAP already applied by SPOC; no additional correction.

### 6.6 Pre-registered transit predictions (frozen 2026-10-17 18:30:15 UTC)
Ephemeris (all six sectors, shape fixed to the MCMC medians, TOI-2514.01 masked):
**T0 = BTJD 1468.67922 ± 0.00127 (BJD_TDB 2458468.67922), P = 0.5718634 ± 0.0000004 d**, corr(P, T0) = −0.74, duration 1.50 h,
expected depth ≈ 185 ppm (per-sector range 56–220 ppm). Formal propagated 1σ at Sectors 108–110 = 2.0 min; the season-jackknife
spread of P (±8.5e-07 d) implies a conservative **1σ ≈ 6 min**. Use ±6 min.
Full table: `results/vet/317134140/predicted_transits_S108_S109_S110.csv` (SHA-256 `63e98fc87ebc6ce65198e066028d7f9ea58d24b51b35771d9fc551c41f59deb3`), 136 mid-transit times inside the
science orbits of S108 (observed 2026-09-07 to 10-04, data not yet public), S109 (in progress) and S110 (2026-11-01 to 11-25).

| sector | transits in science orbits | first (UTC) | last (UTC) | first tc (BJD_TDB) | last tc (BJD_TDB) |
|---|---|---|---|---|---|
| S108 | 47 | 2026-09-07 21:31 | 2026-10-04 18:35 | 2461291.3968 | 2461318.2744 |
| S109 | 46 | 2026-10-05 08:18 | 2026-10-31 15:38 | 2461318.8462 | 2461345.1519 |
| S110 | 43 | 2026-11-01 05:22 | 2026-11-25 19:32 | 2461345.7238 | 2461370.3139 |

First ten Sector-110 events:

| sector | epoch | tc (BJD_TDB) | mid-transit UTC | ingress–egress UTC | 1σ (min, formal) |
|---|---|---|---|---|---|
| 110 | 5031 | 2461345.72379 | 2026-11-01 05:22 | 04:37–06:07 | 2.0 |
| 110 | 5032 | 2461346.29566 | 2026-11-01 19:05 | 18:20–19:50 | 2.0 |
| 110 | 5033 | 2461346.86752 | 2026-11-02 08:49 | 08:04–09:34 | 2.0 |
| 110 | 5034 | 2461347.43938 | 2026-11-02 22:32 | 21:47–23:17 | 2.0 |
| 110 | 5035 | 2461348.01125 | 2026-11-03 12:16 | 11:31–13:01 | 2.0 |
| 110 | 5036 | 2461348.58311 | 2026-11-04 01:59 | 01:14–02:44 | 2.0 |
| 110 | 5037 | 2461349.15497 | 2026-11-04 15:43 | 14:58–16:28 | 2.0 |
| 110 | 5038 | 2461349.72684 | 2026-11-05 05:26 | 04:41–06:11 | 2.0 |
| 110 | 5039 | 2461350.29870 | 2026-11-05 19:10 | 18:25–19:55 | 2.0 |
| 110 | 5040 | 2461350.87056 | 2026-11-06 08:53 | 08:08–09:38 | 2.0 |

### 6.7 What would confirm or falsify it
* **Confirmation of the periodic signal:** in each of S108, S109 and S110 (2-min cadence requested for TOI-2514), the stacked depth at the
  predicted phase should be ≈185 ± 40 ppm (≈5σ per sector), and a blind BLS of each sector alone should return 0.5719 d near its top.
  With S32-like behaviour (≲60 ppm) in two of the three new sectors, the constant-depth planet hypothesis is falsified.
* **Confirmation that it is a planet on this star** requires more than TESS: high-resolution imaging / Gaia to exclude companions within
  ~20″, a check for a 1.1437-d eclipsing-binary alternative (equal eclipses at twice the period; TESS odd/even cannot separate these for a
  185-ppm signal), and ideally ground-based or RV follow-up. ExoFOP already lists imaging and spectroscopy for TOI-2514 that could be
  re-examined. No statistical validation is claimed here.

### 6.8 Additional checks requested in review
* **Existing follow-up on TOI-2514 (ExoFOP, downloaded 2026-10-17):** SOAR/HRCam speckle imaging (2021-10-01, I band, contrast Δmag = 4.6 at 1″),
  Shane/ShARCS adaptive optics in J and Ks (2021-11-21, two epochs each); TRES reconnaissance spectra (2021-03-07/10: G dwarf,
  Teff ≈ 5250–5750 K, v sin i ≤ 8 km/s, 50 m/s RV offset between epochs judged "probably not significant"); CHIRON spectra
  (2021-09-24/25, R = 80,000). Companions brighter than Δmag ≈ 4.6 beyond 1″ are excluded; the inner 1″ is unconstrained.
  TFOPWG disposition of TOI-2514.01: PC (planet candidate), not validated.
* **In-aperture control with the known TOI-2514.01** (P = 6.3951381 ± 0.0001339 d, ExoFOP depth 510 ppm): measured per sector with
  the same box machinery, S6 109 ± 73, S32 379 ± 68, S33 686 ± 71, S87 −177 ± 76, S98 238 ± 57, S107 118 ± 69 ppm (phase scans ±8 h find
  nothing better in S87/S98/S107). So the catalogued candidate on this star is clearly recovered only in 2020–21 (the sectors it was
  alerted from) and is weak or absent in 2018 and 2024–26, while the 0.5719-d signal shows the opposite pattern (weak in S32, strong in
  S33, S98, S107). Two consequences: (i) S32 photometry does recover a real-depth signal (the TOI at 5.6σ), so the S32 non-detection of
  the 0.5719-d signal is specific to that signal and remains a genuine caveat; (ii) on this star, catalogued 100–500 ppm signals are not
  consistently recovered sector to sector, so depth-consistency is a weak discriminant here and the status of TOI-2514.01 itself deserves
  re-examination with the 2024–26 data.
* **Shared instrumental period?** Among all 1,637 Pool-A stars, 21 have a top-3 BLS peak within ±0.5 % of 0.5719 d and 9 within ±0.5 % of
  1.1437 d; apart from the candidate and one known 0.5705-d eclipsing binary (TIC 299967130, a TCE), all have SDE 5.9–7.8 (noise level) and
  their periods scatter across 0.569–0.574 d with no concentration at 0.57186 d and no common camera/CCD. No evidence of a
  spacecraft-related period.
* **Archival-recovery significance:** the S33 single-sector blind BLS grid (0.5–13 d, log-uniform) has ≈1.2 % of its range within ±1 % of the
  candidate period or its 2× alias; the probability that an unrelated sector's top peak lands there by chance is therefore ≈1 %, and the
  depth at the predicted phase in that sector is 5.2σ.
* **Dependencies in the blind test (disclosed):** the transit shape (Rp/R★, a/R★, b) used to time the training data was fixed from the all-data
  MCMC, and the holdout detrending masked the predicted transit windows. Neither can create a dip in the holdout; both are what a
  pre-registered test would do.
* **Cadence note:** predictions assume 2-min SPOC data for S108–S110 (TOI-2514 is a 2-min target in S107; its S108–S110 status is not yet
  listed on MAST). 200-s FFI light curves (QLP/TESS-SPOC) will exist regardless and suffice for the ≈5σ-per-sector test.
* **Open step for falsifiability (user action):** the frozen prediction file and `PREREGISTRATION.md` carry only a local timestamp and
  SHA-256. To make the prediction externally verifiable they must be deposited with an independent timestamp (e.g. Zenodo, as in the
  reference work, or a signed public commit) **before the S108 data release (expected ~mid-November 2026)**.

### 6.9 Numbers the external review asked to be stated explicitly
* The MOM_CENTR centroid shift quoted in §6.3 (0.1 millipixel) is the four-sector mean; the S98 value alone is 0.34 ± 0.07 mpx (5.3σ), about
  3× the ≈0.10 mpx expected for an on-target 185-ppm dip in that sector. The other sectors are consistent with on-target. This is an unresolved
  tension, not a rejection.
* The per-sector depth test for a constant depth gives χ² = 16.1–18.5 for 5 d.o.f. (p ≈ 0.007), driven by S32 (56 ± 36 ppm where ≈185 was predicted).
* The reviewer found no instrumental or stellar origin: no rotation signal or harmonic series at 0.572/1.144/1.716 d in raw PDCSAP or SAP; the
  signal is box-shaped (Δχ² vs flat: box 104, sinusoid 31); depth is stable for detrending windows 0.5–2 d; the masked-detrend random-phase
  null is unbiased. A 291-min CHEOPS visit of TOI-2514 on 2023-01-06 (CHATEAUX filler) exists on ExoFOP and has a ~46 % chance of containing
  a predicted 0.5719-d transit; requesting it is the cheapest independent test before S108.

## 7. Null calibration of the detection statistic (Pool A)
The identical stitched search was run on inverted light curves (2 − F) of 400 randomly chosen Pool-A targets (`scripts/null_calibration.py`,
`results/null/`). Transits cannot survive inversion; noise, gap systematics and stellar variability do.
* Raw inverted top-peak SDE: median 7.8, 90th percentile 23, maximum 54 — dominated by stellar variability (flares, spots), which the real
  ranking removes with the physical cuts.
* After applying **the same physical cuts as the real ranking** (the review notes one difference: the null keeps the best surviving peak among the top three, the real ranking cuts only the top peak, so the null over-counts false positives — conservative) (≥3 events, |secondary| < 3σ, odd/even < 5σ, duration ≤ 1.6× expected, depth < 3 %,
  ≥2 years with >2.5σ depth): median 6.4, 90th percentile 8.2, 99th percentile 11.0, **maximum 14.3**; fraction above SDE 13.2 = 0.8 %
  (3/400), above 14.3 = 0.2 % (1/400).
* Implication: across 1,637 stars, ≈4 filtered false positives at SDE ≥ 14.3 and ≈12 at SDE ≥ 13.2 are expected from noise/systematics
  alone. **The periodogram statistic by itself therefore does not establish the TIC 317134140 signal** (SDE 14.3 in the search, 13.2 with
  TOI-2514.01 masked); it only makes it worth testing. What distinguishes it from the null population is the out-of-sample evidence:
  the period is the top peak of an independent search of every training subset, the withheld seasons show the dip at the predicted phase
  (5.0σ, 2.8σ, 7.6σ, 5.4σ; 1.7σ in S6) against random-phase nulls, and a sector never used in the search (S33) returns the period blind.
  The 17 other SDE > 9 survivors in Pool A are consistent with this null expectation and none passed triage/vetting.

### 7.1 Control of the blind test itself — an important correction to §6.4
The season-holdout test was applied to the strongest *inverted-light-curve* false signal from the null set (TIC 120896927, an 81-ppm,
4.756-d "bump" with 38 events in 4 years, filtered SDE 14.0; `scripts/null_control_blind.py`, `logs/null_control_blind.log`). It **passed**
exactly like the candidate: the training-only search ranked the period first in every holdout and the held-out years showed the bump at the
predicted phase at 3.3σ, 3.5σ, 3.3σ and 7.4σ.

Interpretation: a period selected by a stitched multi-year search over ~10⁶ trial periods × 1,637 stars is, by construction, one at which
noise or systematics line up in *all* years; holding out a year afterwards therefore does not test the signal independently of its
selection. **The season-holdout results in §6.4 should not be read as independent confirmation.** The only prior data that are
independent of the selection are the 2020 FFI sectors (S32, S33), which were never part of the search: S33 returns the period blind and
shows the dip at the predicted phase (5.2σ; chance ≈1 %), S32 does not (0.9σ where 5σ was expected). Stacked, the two give 110 ± 26 ppm
(4.2σ) at the predicted phase, with the candidate period ranked second in a blind search of the stacked FFI data.

Revised assessment: TIC 317134140's 0.5719-d signal is at the 99.8th percentile of the filtered null (≈4 such false positives expected in
the pool), is consistent with an on-target transit in every pixel-level and shape test, and has one independent archival recovery and one
independent archival non-recovery. It is a **plausible but unproven candidate whose decisive test is the pre-registered S108–S110
prediction** (§6.6), not the archival record. The same control was then applied to the archival-sector test (§7.2).

### 7.2 Control of the archival-sector test
The same inverted-null approach was applied to the archival-sector test using the only high-SDE null star with an FFI-only sector
(TIC 67630845, inverted 9.46-d, 1055-ppm, 8-event signal, filtered SDE 13.3; S3 2018 TESS-SPOC and QLP 30-min light curves, inverted;
`logs/archival_null_67630845.log`). Result: the null period is **not** among the top-3 blind BLS peaks of the archival sector in either
product, and the depth at the predicted phase is 1.0σ / 1.9σ. The candidate's S33 test (top peak, 5.2σ) therefore behaves differently
from a selection-effect false positive in the one available control, while its S32 test behaves like one. One control is anecdotal;
the pre-registered S108–S110 test remains the decisive one.

### 7.3 Null calibration for Pool B (QLP)
The inverted search on 300 random Pool-B stars (`results/null_qlp/`): raw inverted top-peak SDE median 7.6, 90th pct 12.1, 99th pct 32.9,
max 57.5 (stellar variability and scattered-light bumps); **after the same physical cuts: median 7.1, 90th pct 8.4, 99th pct 10.6, maximum
11.6; 3.7 % above SDE 9, 0 of 300 above 12.** The real Pool-B search has 5.8 % of stars above SDE 9 after the same cuts — only a modest
excess, and the period clustering (§5.2) shows why: FFI systematics are *asymmetric* (scattered-light dips at orbit/sector cadence), so
an inverted-light-curve null underestimates the false-positive rate for dips at 12–20 d. The inverted null therefore calibrates Pool B only
for periods away from those clusters. TIC 89247735 (SDE 26.9, three events each > 30σ) is not a periodogram-threshold case; its reality
is established event by event, and the open question is astrophysical nature, not noise.

## 8. Candidate: TIC 89247735 (SCR J1820-4533) — an 18.32-day, 1 %-deep transit signal with no catalog entry

### 8.1 Star
TIC 89247735 = Gaia DR3 6708071581514074368 = SCR J1820-4533 (high-proper-motion star, −39/−106 mas/yr). RA 275.2237, Dec −45.5612.
Tmag 11.14, G 11.85, BP−RP 1.45; parallax 9.54 ± 0.02 mas (104 pc). TIC: Teff 4394 K, R★ 0.785 R☉, log g 4.49 (Gaia GSP-Phot 4614 K, log g 4.60).
Gaia: RUWE 1.10, `non_single_star` = 0, no variability flag, RV −21.6 ± 0.5 km/s. TIC contamination ratio 0.27. No TOI, CTOI, community
candidate, SPOC/TESS-SPOC TCE, or ExoFOP observation as of 2026-10-17 (ExoFOP page checked directly). Observed by TESS in S13 (2019),
S66 (2023), S93 (2025), S104 (2026); QLP FFI light curves only (no 2-min data); tess-point lists no further sectors through S134.

### 8.2 Detection (Pool B search)
Stitched BLS top peak P = 18.3230 d, depth 8,239 ppm (QLP DET_FLUX, unmasked spline), duration 4.0 h, SDE 26.9, 3 events — one per
sector in S66, S93 and S104 *in the quality-filtered data*. **The external review (§9) found a fourth, fully covered transit** at epoch 118
(S93, BTJD 3830.347, 0.49 d after the sector start) whose 72 in-transit cadences all carry QLP quality bit 2^30 (scattered-light ramp) and
were discarded by the pipeline's QUALITY == 0 mask. In the raw SAP flux it is a 10,500 ± 360 ppm, 4-h, flat-bottomed box with no background
or centroid excursion, and it falls +3.4 min from the three-transit v1 prediction (1σ ≈ 3 min) — an out-of-sample confirmation that was
sitting in our own data. The two S93 events are consecutive, so the period is now measured directly within one sector:
18.3221 ± 0.0018 d, against 18.3231 d from the stitched search. The per-sector searches saw them only as single events (top peaks at unrelated periods), which is why a
≥2-transits-per-sector pipeline does not flag this star. The 2019 sector's only predicted transit (epoch 0, BTJD 1668.21) falls in the
S13 orbit gap, so 2019 neither confirms nor contradicts the signal.

### 8.3 Vetting (`results/vet_qlp/89247735/`, `results/triage_qlp/89247735_*`)
* Events: S66 10,003 ± 273 ppm (36.7σ), S93 10,835 ± 270 (40.2σ), S104 9,834 ± 236 (41.6σ); flat-bottomed, 4.0 h. Refined depth
  10,235 ± 148 ppm with the transit-masked detrend; QLP SAP flux gives the same (10,434 ± 158). The three depths scatter at 2.5σ
  (χ² 8.5/2); our own TESScut 1-px photometry gives 7,980 ± 203, 8,418 ± 266, 8,729 ± 670 (consistent; diluted by the neighbours in the
  pixel), so the scatter is most likely QLP's sector-dependent crowding correction.
* Shape (batman + emcee, QLP 10/3.3-min cadence): Rp/R★ = 0.0996 ± 0.0020, a/R★ = 30.9 ± 2.3, b = 0.44 (+0.12/−0.20); fitted
  ρ★ = 1.18 ρ☉ vs 1.43 ρ☉ from the TIC radius and mass — consistent. Expected central-transit duration for P = 18.32 d, 0.78 R☉: 4.4 h;
  observed 4.0 h.
* Odd/even: 10,452 ± 191 vs 9,785 ± 259 ppm (2.1σ, with only 2 vs 1 events). Secondary at phase 0.5: 384 ± 160 ppm (2.4σ, not significant);
  deepest feature anywhere else in phase 4.4σ at phase 0.79 (1,090 ppm, single-sector noise); full-phase fold is flat.
* Period aliases: every P/n for n = 2…12 predicts 4–43 transits on good data where no dip is present (`scripts/alias_89247735.py`); the
  epoch differences 40 and 19 are coprime, so 18.323 d is also the longest period consistent with three events of the same kind. The
  remaining loophole — a 36.65-d binary whose primary and secondary eclipses are equal (epochs 79/119 one kind, 138 the other) — needs
  two near-identical stars with ~50 % eclipses diluted ~50×. On the target that is excluded (it supplies ~79 % of the aperture flux, and the
  flat-bottomed 1 % depth with Rp/R★ = 0.10, b = 0.44 is not a grazing twin geometry). On a faint neighbour it is *not* excluded on flux
  grounds — a star with ~2 % of the aperture flux and 50 % eclipses gives exactly 1 %, and the G = 15.49 neighbour supplies ~3.6 % — so
  this scenario collapses onto the neighbour hypothesis and is excluded only to the extent the flux-loss centroid excludes that star.
  **With the fourth transit (epochs 79, 118, 119, 138) every period longer than 18.32 d, including this one, is excluded by data.** Momentum dumps are
  ≥ 33 h from the three original events and 11.7 h from the fourth. Inverted-light-curve search: top SDE 9.7 vs 28.8 real.
* Pixel test (`ffi_pixel_test.py`, S66/S93/S104 TESScut 11×11): flux-loss centroid 0.18, 0.04, 0.16 px (3.7″, 0.8″, 3.3″) from the
  target's WCS position, 0.03–0.04 px statistical error, plus a TESScut WCS systematic of order 0.1 px. The only neighbour able to mimic
  the signal is Gaia G = 15.49 at 8–9.5″ (epoch-dependent because of the target's proper motion), position angle 238°, ΔG 3.64 — it would
  need a 23 % eclipse. It lies 0.46 px from the target; if it were the source the loss centroid would sit on it. The measured loss centroid
  is displaced toward it by 0.15, 0.02 and 0.12 px in the three sectors — a third of the way at most, within the WCS systematic in two of
  three. **The centroid is the only pixel-level discriminator**: the neighbour is inside even the 1-px aperture, so the fall of depth with
  aperture radius (8,400 → 4,300 ppm from 1 to 3 px in S93) only shows dilution by the wider field, not which of the two stars dims.
  Resolution needs a ground-based transit with a small aperture or seeing-limited imaging.
* Blind tests: training on 2023+2026 (holdout 2025) — training-only BLS top peak 18.3230 d; predicted transit within 39 min; observed
  10,848 ± 269 ppm (40σ) at +0.0 h. Training on 2025+2026 (holdout 2023): rank 0, predicted within 26 min, observed 10,057 ± 273 ppm (37σ).
* Transit times (fixed MCMC shape, 0.24-min grid, Δχ² = 1 with errors rescaled to reduced χ² = 1; `vet.py`'s coarser 121-step grid had
  floored these at 1.2 min): BTJD 3115.74198 ± 2.2 min (S66), 3848.66935 ± 1.6 min (S93), 4196.80603 ± 1.8 min (S104); linear-ephemeris
  residuals −1.3, +2.1, −1.9 min (χ² 3.15 for 1 degree of freedom).

### 8.4 What it is if real
With R★ = 0.785 R☉: Rp = 8.5 ± 0.3 R⊕ (0.76 R_Jup); a = 0.113 AU; Teq ≈ 560 K (albedo 0, full redistribution); insolation 16 S⊕.
**Photometry cannot distinguish a giant planet from a brown dwarf or a late-M dwarf of the same radius.** The absence of a secondary
eclipse (384 ± 160 ppm; the 2σ limit of 700 ppm with Rp/R★ = 0.0996 bounds a thermally emitting companion to Teff < 2680 K in the TESS
band, excluding all but the latest M dwarfs) and of ellipsoidal/beaming variation, the Gaia single-star astrometry (RUWE 1.10) and a Gaia RV error (0.54 km/s)
typical of a non-variable RV at this magnitude argue against a stellar companion (an 0.1 M☉ companion at 18.3 d would give K ≈ 8 km/s)
but do not exclude a brown dwarf. Radial velocities are the decisive test: K ≈ 30 m/s for 0.3 M_Jup, 100 m/s for 1 M_Jup.

### 8.5 Pre-registered transit predictions (frozen 2026-10-17 21:28:13 UTC)
Ephemeris from the three re-timed transits (epoch reference = last transit): **T0 = BTJD 4196.80732 ± 0.00181, P = 18.323126 ± 0.000058 d**
(errors inflated by √(χ²/dof) = 1.78; corr 0.71). Formal 1σ at the 2026-10-29 transit: 3.1 min; because only three timings constrain the
period we quote **±15 min** as the conservative window. `results/vet_qlp/89247735/predicted_transits_2026_2027.csv`
(SHA-256 af83f1105765b2a179de1a7b6d28f22bf2488fc3e1a04e45605dd3c9729caee8) lists epochs 139–163; epochs 139–145 predate the freeze and
are flagged `retrodiction: before freeze, untested` in the `status` column. The next five predictions (mid-transit, UTC; ingress/egress ±2.0 h):

| epoch | mid-transit (BJD_TDB) | UTC |
|---|---|---|
| 146 | 2461343.39233 | 2026-10-29 21:23 |
| 147 | 2461361.71546 | 2026-11-17 05:09 |
| 148 | 2461380.03858 | 2026-12-05 12:54 |
| 149 | 2461398.36171 | 2026-12-23 20:39 |
| 150 | 2461416.68483 | 2027-01-11 04:25 |

**v2 (four transits, frozen 2026-10-17 22:20:50 UTC; v1 above is kept unchanged as the test of record for epochs ≥ 146).** All four events
re-timed from raw SAP flux with a local linear baseline: BTJD 3115.74255 ± 2.2 min, 3830.34713 ± 2.0, 3848.66926 ± 1.6, 4196.80432 ± 1.4;
depths 10,991 / 10,814 / 11,367 / 10,749 ppm. **T0 = BTJD 4196.80611 ± 0.00190, P = 18.323077 ± 0.000070 d** (χ² 10.5 for 2 d.o.f.,
inflation 2.29 — per-event timing errors on the ramps are still ~2× underestimated, which is why ±15 min stays the quoted window).
Predictions move by ≤ 2 min relative to v1 (epoch 146: 2026-10-29 21:21 UTC). Files: `predicted_transits_2026_2027_v2.csv`
(SHA-256 8a2b1ccadd1b820cf36f180b1cc83fe2e978c05e8637b7b566d14233b96f5869), `PREREGISTRATION_v2.md`, `final_ephemeris_v2.json`.

**Observability (external review, `results/external_review/observability_89247735.csv`):** epochs 147–151 (2026-11-17 to 2027-01-29) are
unobservable from any southern site (target too close to the Sun); epoch 146 is partial from SAAO only. The first full ground-based transits
are epoch 159 (2027-06-25 02:12 UTC) and 162 (2027-08-19 01:28 UTC) from Chile. Radial velocities need no transit and can start now.

TESS will not re-observe this field through at least S134, so the falsification route is ground-based: a 1 % deep, 4-h transit on a
V ≈ 12.5 southern star is within reach of 30–40 cm telescopes; a single timed transit at the predicted time to within ±15 min, with the
same depth in a different bandpass, would confirm the ephemeris and an achromatic depth. The pre-registration text is
`results/vet_qlp/89247735/PREREGISTRATION.md`.

### 8.6 Status
**Planet candidate pending confirmation.** Strengths: four unambiguous, consistent, flat-bottomed events over 3.5 years, two of them consecutive;
the fourth confirmed the three-event ephemeris out of sample; on-target by pixel test and by the reviewer's PSF fit (Δχ² 83–214 against the neighbour); ρ★ consistent; no secondary; absent from every catalog checked. Weaknesses: only four events, all from TESS FFIs (QLP, the independent TARS pipeline and our own cutout photometry of the same frames); a 9.5″ neighbour cannot be fully excluded with 21″ pixels (seeing-limited
imaging or a ground-based transit in a small aperture would settle it); nature (planet vs brown dwarf vs M dwarf) requires RV.

## 9. External adversarial review (independent agent, `results/external_review/REVIEW.md`)
An independent reviewer with no access to our reasoning was asked to break both candidates with outside data and to audit the code.
Verdicts: **TIC 89247735 survives and is stronger** (fourth transit found, see §8.2/§8.5; period measured directly from consecutive transits;
field control of 190 same-CCD stars shows no comparable event at that time, the target is a 9σ outlier; the independent TARS FFI pipeline
reproduces every event at the same depth; the S13 gap is confirmed in QLP, TESS-SPOC and ELEANOR-LITE; PSF fit of the flux-loss map rejects
the 8″ neighbour, which Gaia shows to be a background metal-poor subgiant at 2.35 kpc; our centroid estimator is biased by only 0.02–0.06 px
under injection; Gaia DR3 gives a single K4–5 dwarf with RV error 0.54 km/s over 14 transits, excluding M-dwarf companions but not brown
dwarfs; no entry in SIMBAD, VSX, ASAS-SN variables, Gaia variability, TESS EB catalogs, single-transit lists, ExoFOP or arXiv full text).
**TIC 317134140 wounded, unchanged** (no instrumental origin found; the per-sector depth χ² and the S98 centroid value are the weak points,
§6.9; S108–S110 decisive). **Methodology survives with corrections.**

Code findings the reviewer logged (all acknowledged; none changes a verdict): (1) `tsearch.py:45` QUALITY == 0 drops QLP bit 2^30 cadences
(20–30 % per sector, concentrated in orbit-start ramps) — Pool-B completeness for transits in the first ~0.5–1 d of an orbit is lower than
the known-signal recovery suggests, and this is what hid the fourth transit; (2) `alias_89247735.py:22` counted alias coverage on the
filtered data; (3) `vet.py:174` substitutes the all-data period when a training search returns an alias (small leak in a test already
demoted in §7.1); (4) `null_calibration.py:61-68` vs `rank.py:56-63` best-of-top-3 vs top-peak (null conservative); (5) `rank.py:37`
secondary significance uses the primary-depth error because `depth_phased`'s own error is not stored; (6) `ffi_pixel_test.py:89-90` uses the
J2000 position without proper motion (0.13 px for this high-PM star; WCS-vs-image systematic 0.16 px); (7) transit timing without a local
baseline slope moves ramp-affected times by 1–3 min — addressed in the v2 ephemeris. Not yet testable: ASAS-SN Sky Patrol v2 (offline since
2026-10-13; ~25 in-transit epochs expected; scripts ready in `results/external_review/`), SuperWASP (no source).

Cheapest next observations (reviewer's ranking): for TIC 89247735 — radial velocities now (K ≈ 30 m/s for 0.3 M_Jup, 100 m/s for 1 M_Jup,
1.3 km/s for 13 M_Jup, 8 km/s for an M dwarf), the ASAS-SN fold when the service returns, speckle/AO imaging for a < 1″ companion, and the
2027-06-25 / 2027-08-19 transits from Chile; for TIC 317134140 — S108–S110, then the archived CHEOPS visit.

## 10. Single-transit search of the QLP pool (follow-up to the external review)
Motivation: periodic pipelines (ours, QLP's, SPOC's) need two transits per sector and so miss P ≳ 13 d, and the review showed that our
QUALITY == 0 mask deleted a real transit inside the orbit-start scattered-light ramp. `scripts/single_transit_search.py` therefore scans every
QLP light curve of the Pool-B stars (3,397 with usable files) for individual box-shaped dips, keeping the flagged cadences.

**Method.** Cadence policy: drop NaN flux, flux excursions > 50 % (data dropouts) and TESS bits 2/4/8/32/128; keep bit 2048 (stray light)
and QLP bit 2^30 (ramp). Flux = raw SAP. Stage 1: 1-d biweight + sliding box at 1.5–8 h with local noise (SNR > 5). Stage 2: box + local
linear baseline refit on the undetrended flux in ±3 durations (final SNR ≥ 7). Each event carries: pre/post baseline step, fraction of
in-transit points below baseline, box-vs-V Δχ², bottom flatness, SAP_BKG in/out ratio, centroid shift, fraction of flagged cadences, time
since orbit start, nearest momentum dump, camera/CCD. Known TOI/CTOI transits are masked. Controls (`single_rank.py`): event cuts; tier-1 star
cuts (eclipsing binaries/variables with > 8 events per sector or > 30 total set aside, 266 stars); **field control** per CCD-sector and
per sector (0.25-d bins, Poisson threshold, ±1 bin) and a **direct coincidence control** (other stars with an event within ±0.1 d, flagged
above max(5, 3× chance)); tier-2 star cuts (≤ 3 surviving events per sector, ≤ 10 total); matching of ≥ 2 events with consistent depth (3σ)
and duration (×1.6) in different sectors, at least one in unflagged data, orbit-synchronous repeats removed; allowed period aliases from the
kept-cadence coverage. The identical chain was run on inverted light curves (`results/single_inverted/`) as the null.

**Detector validation (re-run on the final code).** TIC 89247735: all four transits found (SNR 30.5, 26.5 [the flagged one, 0.48 d
after orbit start], 33.8, 41.3). Long-period TOIs with unmasked transits: TOI-6806.01 (4.9 %, 23.2 d) 7 of 7 covered transits;
TOI-240.01 (1.8 ppt) 7 of 9; TOI-4565.01 (1.5 ppt) 6 of 9 (misses have 5–16 in-transit cadences or sit at the stage-1 threshold).
TIC 89247735 also served as the regression test for the *ranking* chain: successive versions of the star-level and field controls first
set it aside as "busy" and then field-flagged three of its four events, and the controls were revised with it as the positive control
until all four events survived; the null comparison below was made with that final chain, so the controls were not fixed a priori.
The duotransit matcher kept three of the four events (the pair-wise depth-consistency step starts from the strongest pair).
Injection–recovery on 293 random star-sectors (`single_injection.py`, batman transits 1–20 ppt, 2–8 h, random times including ramps),
scored end to end by also asking whether the injected time falls in a window that the field or coincidence control flagged in the real
run (27 % of injected times do; `results/single/summary/injection_recovery_end_to_end.csv`): detection 76 % at expected SNR 7–10, 87 % at
10–15, 92–98 % above 15; after the event cuts 48–76 %; **end to end 38–59 %** (SNR 7–10: 38 %, 10–15: 59 %, 15–30: 58 %, > 30: 38 % —
the deepest injections are limb-darkened and fail the flat-bottom/box-vs-V cuts). In the first 0.5 d of an orbit detection is 40 % and
end-to-end completeness 20 %; at 0.5–2 d it is 20–40 %; beyond 2 d, 51 %. These are the completeness numbers that §5.2 lacked, and they
mean the fourth transit of TIC 89247735 came from exactly the data region where any FFI pipeline is least complete.

**Result.** Raw: 151,010 events; 39,700 pass the event cuts; 2,120 survive all controls on 1,158 stars; 158 stars have ≥ 2 matched
events — and the inverted null gives 2,455 events and 160 matched stars under the same chain. Across a grid of 54 stricter cut sets
(`single_null_compare.py`, `results/single/summary/duo_cut_grid.json`) the real and inverted counts track each other everywhere;
**the only star that exceeds the null in any cut set is TIC 89247735**, the unique real star with ≥ 3 consistent events in different
sectors (null: 0). Single, unmatched events are more numerous in the inverted data than in the real data at every SNR threshold
(e.g. SNR ≥ 15, ≤ 6 h: 27 real vs 72 inverted; flares and variability invert into dips), so no single event can be claimed; the 79
flat, unflagged, SNR ≥ 12 real singles are listed without claim in `results/single/summary/single_events_of_interest.csv` for comparison
with future sectors. Before the coincidence control was added, the real list showed an apparent excess of 2–27 stars over the null
whose events shared identical times across 8–270 stars per sector: sector-wide systematics that a per-CCD bin test with proportional
thresholds had let through. **Conclusion: no new candidate.** The single-event regime of QLP photometry at SNR 7–20 is dominated by
red noise and scattered-light structure, and two-event depth consistency is too weak a constraint to beat it; a third event in a
different sector, as for TIC 89247735, is what separates a candidate from the null.
