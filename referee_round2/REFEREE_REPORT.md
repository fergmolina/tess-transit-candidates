# Referee report, round 2: TIC 183374279 and TIC 61310956

**Material reviewed:** `results/round2_dossiers/DOSSIERS.md` (both dossiers and the verbatim frozen pre-registrations), the public dossier of TIC 183374279 in `public_release/README.md`, and the underlying products in `results/vet_allsky/<TIC>/` (report.json, final_ephemeris_v2.json, predicted_transits_2026_2027_v2.csv, PREREGISTRATION_v2.md, spoc_120_check.json, triceratops.json, triceratops_probs.csv, triceratops_stars.csv, vet_summary.png) and `results/vet_qlp/<TIC>/` (ffi_pixel_S*.json/png); the scripts vet.py, ffi_pixel_test.py, prereg_v2.py, triceratops_qlp.py, tessspoc_check.py; REPORT.md sections 11 and 12; the external review `results/external_review_allsky/REVIEW.md`; the round-2 prior-detection sweep `results/prior_search_round2/`; the earlier referee report on TIC 89247735; `catalogs/TESS_orbit_times.csv`; the Sector 106 two-minute target list.
**Recomputed from cached data (no MAST or TESScut downloads):** QLP light curves and SPOC 2-min files on disk, the TESScut cutouts already in `data/lk_cache/tesscut/` (11x11 and 15x15), tess-point (offline, pointing table through Sector 134), astropy UTC conversions, the v2 ephemeris fits, and the Gaia-luminosity stellar radii. One light Gaia DR3 TAP query (two source IDs, astrometric and radial-velocity flags) was made. My scripts are `pixel_check.py` and `pixel_calib2.py` in this directory; every other check is a few lines of numpy documented in the text.
**Standard:** same as the TIC 89247735 report (AJ referee / TFOP SG1 coordinator). Frozen files were not modified.
**Date:** 2026-10-19.

---

## 1. Verdicts

| object | verdict | one-line reason |
|---|---|---|
| **TIC 183374279** | **Revise; keep as planet candidate (ephemeris-test stage)** | The signal is real, periodic over 2018-2026 and on no catalogued neighbour. The dossier overstates precision in five places (radius, depth, pixel offsets, "every year", "4/4"), the third Sector 106 transit is only half covered, and "data not public at the freeze" is true of QLP only. Nothing found kills the candidate. |
| **TIC 61310956** | **Revise; keep as planet candidate, but re-freeze (v3) before 2026-10-24** | The light-curve case is as good as 183374279's. But the "independent SPOC 2-min detection, 11 sigma" is wrong (the 2-min data alone do not detect the period; the empirical significance at the known ephemeris is 4.5 sigma), the frozen ephemeris double-counts two sectors, the frozen outcome rules would fail a true planet one time in six, and "not yet public" is false. |

Neither object is a reject. Both are consistent with ~2.5-3 R_Earth planets on isolated K dwarfs; the corrections below are about what the files can and cannot support.

---

## 2. What was verified and agrees with the files

Numbers in the dossier text that trace exactly to a file (value, file, field):

| quantity | 183374279 | 61310956 |
|---|---|---|
| period, T0, sigma, chi2/dof, inflation | final_ephemeris_v2.json, reproduced by refitting sector_times (chi2 1.26/4, T0 err 2.7 min) | reproduced (chi2 8.76/4, inflation 1.48, sigma 20.3 min at epoch 147) |
| QLP depth | 969 ppm (report.json bls_refine) | 1138 ppm |
| duration from the fitted shape (T14) | 2.84 h ("2.9 h") | 3.31 h ("3.2 h") |
| rho_fit/rho_TIC | 2.485/1.710 = 1.45 | 2.345/1.621 = 1.45 |
| b (MCMC median) | 0.44 | 0.41 |
| odd/even | 0.36 sigma ("0.4") | 1.20 sigma ("consistent") |
| secondary at phase 0.5 | +45 +- 82 ppm | -29 +- 102 ppm |
| nearest possible mimic | 72.0", G 17.98, needs 22.3 % | 82.3", G 16.88, needs 20.5 % |
| Gaia RUWE | 1.124 | 0.774 |
| SPOC 2-min depth, white-noise error | 1380 +- 235 ppm (S29, 1 transit) | 1068 +- 95 ppm (S22+S45, 3 transits) |
| TRICERATOPS FPP / NFPP | 0.031 / 0.000 | 0.020 / 0.000 |
| pixel offsets as quoted (loss centroid minus WCS target) | 0.16 / 0.24 / 0.35 px (S96/S103/S105) | 0.16 px (S72) |
| SHA-256 of the frozen CSV | matches | matches |
| prereg text in DOSSIERS.md | verbatim copy of PREREGISTRATION_v2.md | verbatim |
| geocentric UTC of predictions | recomputed with astropy light_travel_time: agrees to the minute (Roemer term +4.8 to +6.4 min) | agrees (-4.8 to -0.3 min) |
| Sector 106 coverage | tess-point: camera 2, CCD 3 | tess-point: no sector through 134 (pointing table covers S1-134) |
| TOI / CTOI within 60" | nearest TOI 2291", nearest CTOI 2672" (local tables of 2026-10-17) | 11584" / 1754" |
| prior-detection sweep | PRIOR_SEARCH_round2.md: "No prior report" | "No prior report" (with a public-history caveat, see M4 below) |
| Gaia binarity flags (live query) | duplicated_source False, non_single_star 0, ipd_frac_multi_peak 1, RV 16 transits, rv_chisq_pvalue 0.28 (no excess scatter) | False, 0, 4, RV 13 transits, p 0.44 (no excess scatter) |

Stellar radius from Gaia G, parallax and the TIC Teff (Andrae et al. 2018 bolometric correction, no extinction): 0.71 R_sun for 183374279 and 0.755 R_sun for 61310956. Both hosts sit on the K-dwarf main sequence (M_G 6.75 and 6.61 at BP-RP 1.36 and 1.29); neither is evolved, and the Gaia RV scatter excludes a stellar-mass companion at the transit period on either star (per-epoch RV precision 2.2 and 1.2 km/s, no excess over 16 and 13 epochs; K below ~3 and ~2 km/s).

---

## 3. TIC 183374279

### Major points

**M1. The depth is quoted from the one product known to be biased low, and the radius uses a superseded stellar radius.**
"~970 ppm" is QLP DET_FLUX (report.json's own `planet.note` says this depth "may be biased low"). Every other measurement is deeper: raw SAP all-sector 1092 +- 91 ppm (report.json sap_depth); per-sector raw SAP 843-1457 ppm (final_ephemeris_v2.json); SPOC PDCSAP S29 1380 +- 235 ppm; and my background-subtracted fixed-aperture cutout depths (2.5-px aperture, sky from the cutout edge ring) 1450-1535 ppm in S103, 1424-1537 in S105, 1203-1227 in S96 (+- 230-250 each; the 15x15 cutouts, whose sky ring lies at >= 6 px, give values 6-8 % lower than the 11x11 ones, so PSF-wing over-subtraction is at most that level, and the SPOC PDCSAP value does not depend on any sky ring). The raw cutout apertures that the project's `depth_vs_aperture` reports are diluted by sky: the background is 145-193 e/s per pixel against a peak pixel of 790-1315 e/s, i.e. 20-40 % of a 2.5-px aperture, which is why the project's raw S103/S105 values (711-945 ppm) are shallower than every detrended product. The honest depth is 1.1-1.4 ppt.
"Radius ~2.5 R_Earth" = k 0.0300 (MCMC on DET_FLUX) x 0.750 R_sun, where 0.750 is the QLP FITS-header radius. TIC v8.2 (triceratops_stars.csv, the same table the external review used for 120444365 when it made exactly this correction) gives 0.708 R_sun; the Gaia-luminosity radius is 0.71. With 0.708 R_sun: 2.32 R_Earth at the DET_FLUX depth, 2.55 at 1092 ppm, 2.87 at 1380 ppm. Quote "2.3-2.9 R_Earth" with the radius source and the depth range, or fit the shape to raw SAP flux as the 89247735 report (M3) already required. Also Teff 4571 K / Tmag 11.31 (header) vs 4518 K / 11.40 (TIC v8.2): say which catalogue version is used. RAVE spectroscopic parameters exist for this star (RAVE J235004.6-392004); cite them as the independent check.

**M2. The third Sector 106 transit is only half covered, and the "data not public" wording is QLP-specific.**
Orbit 224 ends 2026-08-09 09:10 UTC (catalogs/TESS_orbit_times.csv). Epoch 247 is predicted at 08:38 UTC with T14 = 2.84 h: ingress at ~07:13, mid-transit 32 min before the end of science data, egress at ~10:03 after it. The frozen CSV labels all three epochs identically. By the project's own pipeline rule (trim 0.3 d at sector ends) epoch 247 would be discarded; by the frozen outcome rules the test then rests on epochs 245 and 246 only, and a single gap or flagged event turns "recovered" into "insufficient". State this in the dossier now (it does not require editing the frozen file) so that an "insufficient" outcome is not read as a failure.
"Its light curves were not public when the predictions were frozen" is documented only for the QLP product (HTTP 404). Sector 106 ended on 2026-08-09; SPOC and FFI products of earlier sectors reached MAST within 3-6 weeks (REPORT section 11, and the project itself held S105 cutouts), so S106 full-frame images were very probably retrievable through TESScut on 2026-10-19. I could not check this offline. Unless the project can show the FFIs were absent, the correct statement is "the QLP light curve had not been released and no Sector 106 data of any kind were examined before the freeze" (a pre-analysis freeze, not a pre-data freeze). The star is not on the Sector 106 orbit-223 two-minute list (`catalogs/target_lists/all_targets_S106_v1.csv`), so the test will be QLP or a cutout extraction; say so.

**M3. The pixel-test numbers are WCS-relative offsets with bootstrap errors; calibrated errors are ~1.5-2x larger, and the sentence should state consistency, not precision.**
The quoted 0.16/0.24/0.35 px are loss-centroid minus WCS-projected catalogue position. Relative to the flux-weighted stellar image (restricted to 3.5 px; the `star_centroid_px` field in the project's JSON is computed over the whole cutout and is pulled 0.5-0.8 px by field stars, which is why it disagrees with `target_px`), I get 0.06, 0.24 and 0.40 px (15x15 cutouts, same estimator). The injected-transit calibration (same method as `results/vet_qlp/89247735/pixel_calib.json`: 80 fake windows per sector, 1200-ppm loss injected) gives a per-event scatter of 0.24, 0.23 and 0.31 px, i.e. 0.17, 0.16 and 0.22 px for the two-event sectors, against the project's bootstrap 0.33, 0.17 and 0.14. The offsets are then 0.4, 1.5 and 1.8 sigma. In sky coordinates the three loss positions combine to 3.3 +- 2.2 arcsec south of the target (1.5 sigma). S103 and S105 both lean south, toward the only Gaia source inside 60" (G = 20.95 at 24.7", PA 179 deg); that star would need a 344 % eclipse, and a dip hosted there would put the loss centroid 24", not 3-7", away, so the lean is a systematic or noise. S96 contributes little: its second event (BTJD 3933.20) has 40 of 94 cadences carrying QLP bit 30 and sits 0.25 d from a gap with the background rising from 15,500 to 23,000 e/s; the project's own S96 depth-vs-aperture values (1567 +- 2918 ppm and worse) are meaningless for the same reason.
What the test establishes: no flux loss 20-60" away (the blend mode that killed ~60 % of class A), and no Gaia DR3 source anywhere within 60" that could host the signal (any source fainter than G ~ 21 contributes < 250 ppm and cannot produce 1,000 ppm). What it does not establish: anything inside ~1 px (7.5-15" published floors, REVIEW section 5), which is the TRICERATOPS domain. Replace "dip on the target in all three 200-s sectors tested (0.16-0.35 px)" by "loss centroid consistent with the target in three sectors (combined offset 3 +- 2 arcsec; per-sector 0.1-0.4 px with calibrated errors 0.16-0.22 px); no Gaia DR3 source within 60 arcsec can produce the depth".

**M4. The SPOC 2-min statement is an extraction cross-check at a fixed ephemeris, and its significance is 4.8 sigma empirically.**
The sentence is correctly worded ("at the same ephemeris"), but readers will take 1380 +- 235 as a 5.9-sigma independent confirmation. The error is white-noise only (`std(oot)/sqrt(n_in)`); the random-phase scatter of the same box estimator on the same light curve is 290 ppm (p_null < 0.0025), so the single S29 transit is a 4.8-sigma recovery. A blind BLS of the SPOC data alone returns 9.12 d (SDE 3.3) and SDE 1.9 at the QLP period (spoc_120_check.json). It agrees with the QLP S29 depth (1605 +- 276) at 0.6 sigma and with the all-sector DET_FLUX depth at 1.7 sigma: consistent, once sector normalisation is allowed for (REVIEW finding 1). Add the empirical error and the sentence "the 2-min aperture contains the same stars as the QLP aperture, so this is an extraction check, not a blend test" (DECISIONS 35).

### Minor points

1. "Seen in every year from 2018 to 2026": per-year SNR is 5.4 (2018), 5.8 (2020), 3.2 (2023), 4.4 (2025), 9.6 (2026). Say "present at 3-10 sigma in each of the five observed years".
2. "Four of four blind holdout years recovered": four of five years were testable (2018 had no covered predicted transit), and the recoveries are 4.6, 3.2, 3.7 and 8.1 sigma (null p 0.007, 0.007, < 0.001, < 0.001; blind_tests in report.json). Use the 120444365 wording ("4 of 5 years; the 2018 holdout had no covered transit") and give the significances.
3. "Stellar density from the shape 1.45x catalog": a/R_star is 29.4 (+3.4/-7.8), so the ratio is 1.45 (+0.57/-0.88), i.e. consistent with the catalogue at 1 sigma; with the TIC v8.2 radius it is 1.24. Write "consistent (1.4 +0.6/-0.9)". Same for b = 0.44 +- 0.3.
4. "No secondary": give the limit (45 +- 82 ppm at phase 0.5, 2-sigma < 210 ppm, formal) and note that the phase scan's best feature (336 ppm, 3.3 sigma formal at phase 0.895) is the expected maximum of 181 trials. Formal errors here are ~2x optimistic (89247735 report M7).
5. TRICERATOPS: the depth used is 1098 ppm (DET_FLUX fold), 20-25 % below the SPOC/cutout depths; the FPP is driven entirely by the unresolved-companion scenarios (PTP 0.17, STP 0.031) and the project's own literature calibration says FPP is unreliable at SNR < 15 (SNR 12.0 here). "Likely planet" is the Giacalone et al. category (FPP < 0.5 and NFPP < 1e-3) and may be kept only with those two thresholds printed next to it; NFPP = 0 is trivially true here because no Gaia source can produce the depth, so it is not evidence. Prefer "FPP 0.03 (no contrast curve, indicative)".
6. The v2 ephemeris uses six QLP sector times and no SPOC S29 time although the product exists and prereg_v2.py tries to add it; the log should state why it was rejected (sig_det < 16, error > 45 min, or grid edge). Harmless (the S29 QLP time is +2.9 +- 7.2 min).
7. S103 lies inside the QLP timing-error range (orbits 217-218); the external review measured +2.9 to +3.9 min for S103 and -1.0 to -1.6 min for S105. The frozen text says "< 1.5 min on the ephemeris", which is consistent with the review's propagation (T0 -0.8 min for 120444365, same sectors). Fine, but the sentence should cite the review's number for this star once computed.
8. The T0 anchor (epoch 244, S105 second event) is 0.58 d after an orbit start; no cadences are flagged and the S105 two-event offset is -0.7 +- 3.6 min, so no action, but it belongs in the per-event table.
9. The frozen PREREGISTRATION_v2.md prints `tc_bjd_tdb` as `2.461238e+06` (pandas to_string), i.e. to 1 day. The CSV is correct. A v3 or an addendum should print full precision; the dossier should quote BJD_TDB to 5 decimals from the CSV.
10. Sweep counts: "101 repositories and 157 Zenodo records" are the round-1 numbers; PRIOR_SEARCH_round2.md says 182 Zenodo records and leaves the GitHub count as `GH_PLACEHOLDER_1`. Fill the placeholder and quote round 2.
11. report.json `future.tess_sectors_all` includes Sector 106 and `upcoming_sectors` is empty because the sector is already past; fine. For 61310956 the same field lists sector 1751 (tess-point's 3I/ATLAS pseudo-sector) as "upcoming" (see below).

---

## 4. TIC 61310956

### Major points

**M1. "An independent SPOC 2-min detection in Sectors 22 and 45 (1068 +- 95 ppm, 11 sigma)" is not supported by spoc_120_check.json.**
(a) The 2-min data alone do not detect the signal: the blind BLS of the SPOC light curves returns 24.83 d (SDE 5.8) and SDE 2.9 at the QLP period. The 1068 ppm is a box depth at the QLP ephemeris. (b) 95 ppm is the white-noise error; the random-phase scatter of the same estimator on the same data is 240 ppm, so the recovery is 4.5 sigma (p_null 0.0075), not 11 sigma. (c) The three 2-min transits (epochs 0, 1, 38: 1230 +- 166, 880 +- 155, 1170 +- 146 ppm at the v2 ephemeris) are the same events as three of the six QLP events, from an aperture containing the same stars. It is a valuable extraction cross-check (QLP 1138 +- 78, SPOC 1068, raw SAP 1334 +- 105, cutouts 1200-1600: consistent within the known QLP normalisation scatter) and nothing more. Rewrite as "recovered in the SPOC 2-min light curves of S22 and S45 at the QLP ephemeris (1068 +- 240 ppm, 4.5 sigma empirical; the 2-min data alone do not yield the period)". The outcome table's "SPOC 2-min S22+S45 1068+-95 ppm (11 sigma)" needs the same change.

**M2. The frozen v2 ephemeris double-counts Sectors 22 and 45, and the frozen outcome rules cannot be met by a true planet with this precision.**
final_ephemeris_v2.json has six rows, but "S22 QLP SAP" and "S22 SPOC 2-min" time the same two transits, and "S45 QLP SAP" and "S45 SPOC 2-min" the same one (prereg_v2.py appends the SPOC row instead of replacing the QLP row). Refitting with the SPOC rows only (n = 4): chi2 7.2/2, inflation 1.9, sigma at epoch 147 = 27.7 min, not 20.3; dropping S46 instead (the +25.6 +- 12.6 min, 2.0-sigma point) gives 16.9 min. The dossier's "sigma ~ 20-25 min through 2027" is therefore a lower bound; 28-35 min is honest. Two of the six events are also within 0.3 d of a gap (S22 epoch 0 at 0.29 d with 4 stray-light-flagged cadences and only 7 good 1800-s cadences in +-T14; S72 epoch 1 at 0.23 d), and the S72 epoch-0 event (the T0 anchor) sits on a background gradient (QLP SAP_BKG 5119 in transit vs 5667 out), which is the likely origin of the -19 min S72 offset and of chi2 8.8/4.
The frozen rules then do not fit the object: "recovered" requires each event "within +-3 sigma_min (and in any case within +-30 min)" and the text calls +-20 min "conservative", while sigma is 20-28 min. A correct ephemeris misses a +-30 min window with probability 14-28 % per event; rule (2) would then declare the signal "inconsistent". The reference depth and duration for the "0.5-1.5x" and "0.7-1.3x" clauses are not stated anywhere in the frozen file (only six per-sector SAP depths, 905-1436 ppm, and no duration). Required before the first predicted event (2026-10-24 00:52 UTC, five days away): a v3 freeze that removes the duplicate rows, states T14 = 3.3 h and the reference depth, and uses a sigma-matched window (+-3 sigma, no 30-min cap). Keep v2 on record. Ground observers need coverage of +-1.5 h around the prediction plus the 3.3-h transit plus baseline, i.e. ~7 h, not the "5 h" in the dossier.

**M3. The pixel test as quoted is weaker and stronger than stated.**
Weaker: the 0.16 px is against the WCS position with a bootstrap error of 0.07 px; the injected-transit calibration on the same S72 cutout gives 0.20 px per event, 0.14 px for two events, and the offset from the flux-weighted stellar image is 0.09 px = 0.6 sigma. The project's S72 `depth_vs_aperture` (2037-2215 ppm, twice the light-curve depth) is a background artefact: the first S72 event has a raw-aperture "depth" of 5654-8170 ppm because of the scattered-light gradient noted above; after sky subtraction both events give 1450-1660 ppm. Remove or recompute that panel; a referee who sees 2x depth in the pixel data will assume dilution of the light curve by 50 %.
Stronger: the 15x15 cutouts of S22 and S45 are already on disk (downloaded for TRICERATOPS) and give the same answer at the 1800-s and 600-s cadences: loss minus star 0.31 px (1.3 sigma) and 0.20 px (0.8 sigma) with calibrated per-event errors 0.34 and 0.23 px; background-subtracted depths 1387-1414 and 1224-1280 ppm. Report all three sectors. As for 183374279, the test's real content is that no Gaia DR3 source within 60" can host the signal (nearest: G 21.4 at 11.2", would need 1329 %); unresolved companions inside ~1 px are not tested.

**M4. "Status: planet candidate (not yet public)" is false, and "full sweep in progress" is out of date.**
PRIOR_SEARCH_round2.md (convention paragraph) records that a machine-readable row for this star (P = 16.537888 d, depth 863 ppm) was public in `tables/allsky_testable_soon.csv` of the GitHub release at tags v1.3-v1.5 and in Zenodo 23460915 / 23461948 / 23463569 from 2026-10-18 23:24 UTC, and was removed at v1.6 (2026-10-19 12:16 UTC). A referee or a concurrent searcher will find those versions. Say exactly that: "the period and depth were public as a table row for 13 h (v1.3-v1.5); the star was withheld as a named candidate at v1.6 pending the ground-based plan". The round-2 sweep is complete ("No prior report"), so replace "full sweep in progress".

### Minor points

1. "Six events in QLP FFI data": correct (S22 x2, S45, S46, S72 x2). The dossier does not say that two of them are 1800-s (S22) and two 600-s (S45, S46) cadence; the 2020 event has 7-11 good cadences in transit. Say so.
2. "Blind holdout 2/2": two of three years were testable (2020 had too little data). The 2023 holdout is a pass with a caveat: predicted times 72 and 50 min from the observed events (2.0-2.9 sigma of the training prediction), stacked depth 645 +- 133 ppm = 0.57x at the predicted phase (SNR 4.9, null p 0.018), scan maximum 941 ppm at -1.25 h. The 2021 holdout is clean (7.9 sigma). Quote both.
3. "~1,100 ppm": products range from 1068 (SPOC) to 1334 (raw SAP) and 1200-1600 (sky-subtracted cutouts). Quote 1.0-1.5 ppt; with R = 0.759 R_sun (TIC v8.2 = header = Gaia-luminosity 0.755, all consistent) the radius is 2.5-3.2 R_Earth, "~2.7" being the DET_FLUX value.
4. Density and b: 1.45 (+0.58/-0.80); b 0.41 (+0.32/-0.27). "Consistent", not "1.45x".
5. Odd/even 1.2 sigma on three odd and three even events is weak; the 2P eclipsing-binary alternative is instead excluded by the Gaia RV scatter (no stellar companion) and by TRICERATOPS EBx2P 2e-5; say that.
6. The host is a Gaia DR3 VARIABLE (classifier SOLAR_LIKE) and a VSX rotational variable (PRIOR_SEARCH_round2.md), i.e. a spotted, rotating K dwarf; the dossier does not mention it. State the rotation period if it can be measured from the QLP data and that it is not a harmonic of 16.54 d; spot crossings also bear on the per-event depth scatter (905-1436 ppm). LAMOST parameters exist (LAMOST J104043.41+161132.8); cite them as the spectroscopic check of Teff/logg.
7. Proper motion is -103 mas/yr in Dec (Gaia), ~1" since the Gaia epoch: 0.05 px, negligible for the pixel test, but the J2000 position in ffi_pixel_test.py should be propagated (REVIEW section 6 item still open).
8. The frozen file says "**Test of record: next TESS sector(s).**" above the table and "The QLP S99-S105 timestamp error shifts these ephemerides by < 1.5 min" although the star has no sector later than 72: template text that a reader will take as errors of fact. Fix in v3.
9. The CSV marks epoch 83 (2023-11-30, the second S72 event, which is in the fit) as "retrodiction: before freeze, untested" and "none (ground-based)". Harmless but wrong; v3 should drop or label fitted epochs.
10. report.json `future.tess_sectors_all` = [22, 45, 46, 72, 1751] and `upcoming_sectors` = [1751]: 1751 is tess-point's 3I/ATLAS pseudo-sector. Filter it in vet.py; the "no revisit through S134" statement itself is correct.
11. TRICERATOPS caveats as for 183374279 (depth used 1026 ppm, no contrast curve, SNR 14.6 < 15; "likely planet" only with the printed thresholds).
12. The frozen MD prints tc_bjd_tdb to 1 day (`2.461338e+06`); CSV correct.

---

## 5. Factual errors found (text -> correct value, file)

| # | object | text | correct | source |
|---|---|---|---|---|
| F1 | 61310956 | "independent SPOC 2-min detection ... 11 sigma" | depth at the QLP ephemeris, 1068 +- 240 ppm empirical (4.5 sigma); SPOC-only BLS: SDE 2.9 at the period | spoc_120_check.json `blind_bls`; this report, section 4 M1 |
| F2 | 61310956 | "Status: planet candidate (not yet public)" | period and depth public as a table row 2026-10-18 23:24 to 2026-10-19 12:16 UTC (v1.3-v1.5, Zenodo 23460915/23461948/23463569) | PRIOR_SEARCH_round2.md, convention paragraph |
| F3 | 61310956 | "sigma ~ 20-25 min through 2027" | 20-25 min only with the duplicated S22/S45 rows; 28-35 min with each sector counted once | final_ephemeris_v2.json `sector_times`; refit in this report |
| F4 | 61310956 | pixel JSON `depth_vs_aperture` 2037-2215 ppm (and the PNG panel) | 1450-1660 ppm after sky subtraction; the raw first event is on a background gradient | ffi_pixel_S72.json; pixel_check.py |
| F5 | 61310956 | "prior-detection corpus clean at the freeze; full sweep in progress" | sweep complete: "No prior report" | PRIOR_SEARCH_round2.md row 2 |
| F6 | 183374279 | "Radius ~ 2.5 R_Earth" | 2.3-2.9 R_Earth (TIC v8.2 R = 0.708 R_sun, depth 970-1380 ppm); 2.46 uses the header radius 0.750 | triceratops_stars.csv `rad`; report.json shape_mcmc |
| F7 | 183374279 | "~970 ppm" as the depth | DET_FLUX value; raw SAP 1092 +- 91, SPOC 1380 +- 235, sky-subtracted cutouts 1200-1540 | report.json sap_depth; spoc_120_check.json; pixel_check.py |
| F8 | 183374279 | three Sector 106 transits implied equal | epoch 247 (2026-08-09 08:38 UTC) ends 53 min after the orbit-224 science data end (09:10 UTC): half a transit | catalogs/TESS_orbit_times.csv |
| F9 | 183374279 | "its light curves were not public when the predictions were frozen" | verified for the QLP product only; FFIs/TESScut status at the freeze unknown | PREREGISTRATION_v2.md ("QLP file absent ... HTTP 404") |
| F10 | 183374279 | "dip on the target ... (0.16-0.35 px)" with bootstrap errors 0.13-0.33 px | offsets vs the stellar image 0.06/0.24/0.40 px, calibrated errors 0.17/0.16/0.22 px; combined 3.3 +- 2.2" | pixel_calib2.py output (section 3 M3) |
| F11 | 183374279 | "four of four blind holdout years" | 4 of 5 (2018 untestable); 4.6/3.2/3.7/8.1 sigma | report.json blind_tests |
| F12 | both | "rho 1.45x catalog" | 1.45 (+0.6/-0.9), consistent with 1 | report.json shape_mcmc `ars` interval |
| F13 | both | frozen MD `tc_bjd_tdb` column `2.46e+06` | full precision in the CSV | PREREGISTRATION_v2.md vs CSV |
| F14 | 183374279 | "101 repositories and 157 Zenodo records" | round-2 sweep: 182 Zenodo records, GitHub count unfilled (`GH_PLACEHOLDER_1`) | PRIOR_SEARCH_round2.md |
| F15 | 61310956 | "Test of record: next TESS sector(s)" and the S99-S105 sentence in the frozen file | ground-based test; no sector after 72 | PREREGISTRATION_v2.md (template text) |

---

## 6. Anything else a hostile referee would raise

1. **Both FPP values are below the "likely planet" line only because there is no contrast curve to cost the unresolved-companion scenarios properly, and TRICERATOPS FPP is seed-dependent and uncalibrated at SNR < 15** (the project's own RESEARCH.md). The sentence "likely planet by the published categories" should not appear in a public README without the thresholds in parentheses; "FPP 0.03 / 0.02 without contrast curve, indicative" is safer. Speckle or AO imaging is the cheapest next observation for both.
2. **Red noise is absent from every quoted error.** SPOC and QLP box errors are `std/sqrt(n)`; the random-phase scatter is 2.5-3x larger for both stars. Each per-sector depth in the frozen files carries the same optimism, which matters for the "0.5-1.5x depth" outcome clause.
3. **Limb darkening** is fixed at (0.40, 0.25) for a 4520 K star in prereg_v2.py and vet.py; tabulated TESS-band values are ~(0.5, 0.2). It changes T14 by minutes and depth by a few per cent; state it (89247735 report M3e).
4. **The S106 test for 183374279 is not independent of the project** in the sense the dossier implies for other objects ("the test comes from TESS itself"): the recovery criterion will be applied by the same analyst to the same pipeline. Pre-registering the exact extraction (QLP DET_FLUX vs TESScut aperture and sky treatment) would remove the remaining freedom; the frozen rule allows three alternatives.
5. **The 61310956 ground test is hard at this depth and period:** a 1.1-ppt, 3.3-h event on a V = 11.6 star with a +-1.5 h timing window needs ~7 h of 1-mmag photometry on a night when the 16.5-d ephemeris cooperates; from a single site that is a few opportunities per season. Say which SG1-class facilities are meant, or note that a two-transit "recovered" outcome may take a year.
6. **The all-sky search context** (how many class-A survivors, the sector-scrambled null showing SDE >= 12 is above the null only for P > 7 d) is in REPORT 12.4 but not in the dossiers; both objects are above that line (SDE 14.8 and 18.2), which is worth one sentence.

---

## 7. Exactly what text should change

**DOSSIERS.md and public_release/README.md, TIC 183374279 paragraph**
- "An 11.737984-d, ~970 ppm, 2.9-h transit" -> "An 11.737984-d transit of 2.8-h duration and 1.0-1.4 ppt depth (QLP detrended 970 ppm; raw SAP 1090 +- 90; SPOC 2-min S29 1380 +- 290; sky-subtracted cutouts 1200-1540)".
- "SPOC 2-min Sector 29 gives 1380 +- 235 ppm at the same ephemeris" -> "the single SPOC 2-min transit of Sector 29 gives 1380 +- 290 ppm (empirical error) at the QLP ephemeris; the 2-min data alone do not yield the period, and the aperture contains the same stars, so this is an extraction check, not a blend test".
- "Radius ~ 2.5 Earth radii if on the target" -> "Radius 2.3-2.9 Earth radii if on the target (TIC v8.2 and Gaia-luminosity radius 0.71 R_sun; the range follows the depth range)".
- "Stellar density from the shape 1.45x catalog, odd/even 0.4 sigma, no secondary" -> "stellar density from the shape consistent with the catalogue (1.4 +0.6/-0.9), odd/even 0.4 sigma, secondary at phase 0.5 45 +- 82 ppm".
- "four of four blind holdout years recovered" -> "the signal is recovered in each of the four testable blind-holdout years (2020, 2023, 2025, 2026 at 4.6, 3.2, 3.7 and 8.1 sigma; the 2018 holdout had no covered transit)".
- "seen in every year from 2018 to 2026" -> "present at 3-10 sigma in each of the five observed years (2018, 2020, 2023, 2025, 2026)".
- "dip on the target in all three 200-s sectors tested (0.16-0.35 px)" -> "flux-loss centroid consistent with the target in all three 200-s sectors (0.1-0.4 px, calibrated errors 0.16-0.22 px; combined offset 3 +- 2 arcsec); no Gaia DR3 source within 60 arcsec can produce the depth".
- 'TRICERATOPS FPP 0.031, NFPP 0.000 ("likely planet" by the published categories, not validated)' -> "TRICERATOPS FPP 0.031, NFPP 0.000 (no contrast curve; below the Giacalone et al. validation threshold of 0.015; indicative at SNR 12)".
- "no listing in any of the 101 repositories and 157 Zenodo records" -> the round-2 numbers once the GitHub placeholder is filled.
- "Test of record: TESS Sector 106 (observed 2026-07-11 to 08-09; its light curves were not public when the predictions were frozen ...)" -> "Test of record: TESS Sector 106 (2026-07-11 to 08-09). Two predicted transits (2026-07-16 21:14 and 07-28 14:56 UTC, sigma 2.7 min) fall inside the science orbits; the third (08-09 08:38 UTC) is cut by the end of orbit 224 at 09:10 UTC and will be partial. The QLP light curve had not been released at the freeze (2026-10-19 11:44 UTC) and no Sector 106 data were examined; the star is not a Sector 106 two-minute target, so the test will use QLP or a fixed-aperture cutout extraction."

**DOSSIERS.md, TIC 61310956 paragraph**
- "six events in QLP FFI data (Sectors 22, 45, 46, 72) and an independent SPOC 2-min detection in Sectors 22 and 45 (1068 +- 95 ppm, 11 sigma)" -> "six events in QLP FFI data (S22 x2 at 1800 s, S45 and S46 at 600 s, S72 x2 at 200 s); the three 2020-2021 events are also recovered in the SPOC 2-min light curves at the QLP ephemeris (1068 +- 240 ppm, 4.5 sigma empirical; the 2-min data alone do not yield the period)".
- "~ 1,100 ppm, 3.2-h" -> "1.0-1.5 ppt, 3.3-h"; "Radius ~ 2.7" -> "2.5-3.2".
- "Stellar density from the shape 1.45x catalog, no secondary, odd/even consistent, blind holdout 2/2" -> "density consistent with the catalogue (1.4 +0.6/-0.8), secondary -29 +- 102 ppm, odd/even 1.2 sigma (3 vs 3 events), blind holdout recovered in both testable years (2021 at 7.9 sigma; 2023 at 4.9 sigma with the predicted times 50-70 min from the observed events)".
- "dip on the target by pixel test (0.16 px, one 200-s sector)" -> "flux-loss centroid consistent with the target in S22, S45 and S72 (0.1-0.3 px, calibrated errors 0.14-0.24 px); no Gaia DR3 source within 60 arcsec can produce the depth".
- "TRICERATOPS FPP 0.020 / NFPP 0.000 (no contrast curve; 'likely planet' category, not validated)" -> as for 183374279.
- "prior-detection corpus clean at the freeze; full sweep in progress" -> "round-2 prior-detection sweep: no prior report".
- "the test of record is ground-based photometry of any predicted transit (sigma ~ 20-25 min through 2027) at ~ 1 mmag over 5 h" -> "ground-based photometry of two predicted transits (prediction sigma 28-35 min once each sector is counted once, see v3), ~ 1 mmag over ~7 h (transit 3.3 h plus +-1.5 h window plus baseline)".
- "Status: planet candidate (not yet public)" -> "Status: planet candidate. Its period and depth were public as a table row (tables/allsky_testable_soon.csv, v1.3-v1.5, 2026-10-18 23:24 to 2026-10-19 12:16 UTC) and withdrawn from the public tables at v1.6; it has not been named publicly as a candidate".
- Add: "Host is a Gaia DR3 / VSX rotational variable."

**Frozen files (do not edit; issue v3 for 61310956, addendum for 183374279)**
- 61310956 v3: one time per sector (SPOC rows for S22 and S45), T14 and reference depth stated, +-3 sigma window with no 30-min cap, remove the "next TESS sector(s)" header and the S99-S105 sentence, label fitted epochs, print BJD_TDB to 5 decimals. Freeze before 2026-10-24.
- 183374279 addendum (not a new ephemeris): the partial-coverage note for epoch 247, the extraction to be used, and the FFI-availability statement.

**Outcome table `allsky_classA_round2_outcomes.csv`**
- 61310956 `extraction_check`: "SPOC 2-min S22+S45 1068+-240 ppm at QLP ephemeris (4.5 sigma empirical; no blind detection)".
- 183374279 `pixel_test`: "consistent with target, 0.1-0.4 px (calibrated 0.16-0.22 px)".

**Code (for the record, not blocking)**
- prereg_v2.py: replace, not append, the QLP row when a SPOC row exists for the same sector; print full-precision BJD; suppress the S99-S105 sentence and the "next TESS sector(s)" header under `--ground`.
- ffi_pixel_test.py: sky subtraction (edge-ring median per cadence), restricted-aperture stellar centroid, proper-motion propagation, injected-transit error calibration (the 89247735 `rerun_pixel_calib.py` already does all four).
- vet.py: drop tess-point sector 1751; add the Gaia flags (duplicated_source, non_single_star, ipd_frac_multi_peak, phot_variable_flag, RV statistics) to `gaia_neighbours`.

---

## 8. Recomputed numbers (for reuse)

| quantity | 183374279 | 61310956 |
|---|---|---|
| Gaia-luminosity radius (R_sun) | 0.71 | 0.755 |
| R_p with TIC v8.2 radius at 970 / 1092 / 1380 ppm (R_Earth) | 2.32 (DET_FLUX k) / 2.55 / 2.87 | 2.67 (DET_FLUX k); 2.5-3.2 over 1.0-1.5 ppt |
| rho ratio 1-sigma interval | 0.57-2.02 | 0.65-2.03 |
| SPOC 2-min empirical error / significance | 290 ppm / 4.8 sigma (1 transit) | 240 ppm / 4.5 sigma (3 transits), p_null 0.0075 |
| SPOC per-transit depths at v2 (ppm) | epoch 62: 1380 +- 234 | epochs 0/1/38: 1230 +- 166 / 880 +- 155 / 1170 +- 146 |
| sky-subtracted 2.5-px cutout depths (ppm) | S96 1203-1227, S103 1449-1535, S105 1424-1537 (+-230-250) | S22 1387, S45 1224, S72 1505-1583 (+-130-150) |
| loss centroid minus stellar image (px) and calibrated sigma | S96 0.06 (0.17), S103 0.24 (0.16), S105 0.40 (0.22) | S22 0.31 (0.24), S45 0.20 (0.23), S72 0.09 (0.14) |
| combined loss position on the sky | 3.3 +- 2.2" south (1.5 sigma) | consistent with target in all three sectors |
| ephemeris refit without duplicate rows | n/a (none) | n = 4, chi2 7.2/2, sigma(epoch 147) 27.7 min |
| ephemeris refit without S46 | n/a | n = 5, chi2 4.4/3, sigma 16.9 min |
| Sector 106 orbit windows (UTC) | 07-11 22:20 to 07-18 13:15; 07-18 18:15 to 07-26 08:55; 07-26 13:55 to 08-02 05:00; 08-02 10:00 to 08-09 09:10 | - |
| Gaia DR3 flags (live) | RUWE 1.124, AEN 0.082 mas (10.7 sig; at this level with RUWE 1.12 and ipd_frac_multi_peak 1 it is not a binarity indicator), ipd_frac_multi_peak 1, duplicated False, NSS 0, var NOT_AVAILABLE, RV 22.2 +- 0.69 km/s (16 epochs, chisq p 0.28, amplitude_robust 7.7) | RUWE 0.774, AEN 0.068 mas (5.6 sig), ipd 4, duplicated False, NSS 0, VARIABLE, RV -4.66 +- 0.43 km/s (13 epochs, p 0.44, amplitude_robust 4.2), pmdec -102.9 mas/yr |
