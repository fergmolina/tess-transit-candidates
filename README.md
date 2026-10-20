# TESS multi-year transit search: two planet candidates with pre-registered predictions

**Author:** Fernando Molina (Independent researcher, ORCID [0009-0002-2872-3406](https://orcid.org/0009-0002-2872-3406)). Analysis performed with Claude (Anthropic) under the author's direction.
**Date:** 2026-10-17, updated 2026-10-20 (v1.11: conformance procedure for the Sector 106 tests, protocol erratum, dossier corrections; v1.10: data-availability erratum, timing-rule clarification, all-sky round 3 frozen predictions; see below). **DOI:** [10.5281/zenodo.23443245](https://doi.org/10.5281/zenodo.23443245) [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23443245.svg)](https://doi.org/10.5281/zenodo.23443245) **Status of every object here: candidate pending confirmation. Nothing in this repository is a validated planet.**

A search of public NASA TESS photometry (SPOC 2-min light curves for 1,637 dwarfs and QLP full-frame-image light curves for
3,411 dwarfs, sectors 1 to 107, 2018 to 2026) for periodic transit-like signals that repeat with the same period and phase in
different years and are absent from the TOI, CTOI, confirmed-planet and TCE catalogs. Method modelled on Rabtsevich (2026, TIC 4206066).
Full methods, results, rejected objects and null calibrations are in [REPORT.md](REPORT.md); every decision is logged in
[DECISIONS.md](DECISIONS.md); an independent adversarial review is in [external_review/REVIEW.md](external_review/REVIEW.md).

## Candidates

**TIC 89247735 (SCR J1820-4533)** — K dwarf, Tmag 11.1, 104 pc. Four flat-bottomed transits of 1.0 % depth and 4.0 h duration in
2023, 2025 (two, consecutive) and 2026 at P = 18.323077 ± 0.000070 d; on-target by pixel-level tests; no secondary eclipse;
no catalog entry. Radius 8.5 Earth radii (0.76 Jupiter radii): a giant planet or a brown dwarf (Gaia radial velocities bound the mass below about 25 Jupiter masses); the two cannot be separated without radial velocities, and no statistical-validation route exists at this radius. Status: transiting companion candidate.
Predicted transit times through 2027 are frozen in `preregistration/TIC89247735/` (v1: three transits; v2: four transits).
The first ground-observable full transits are 2027-06-25 and 2027-08-19 from Chile.

**TIC 317134140 (TOI-2514 host)** — a second, 0.571863-d, ~185 ppm signal (1.4 Earth radii if on target) recovered in data from
2018, 2020, 2024, 2025 and 2026. Plausible but unproven: the periodogram statistic alone is within the false-positive expectation,
one 2020 sector does not show it and one sector's centroid is in tension. Transit times for TESS Sectors 108 to 110 are frozen in
`preregistration/TIC317134140/`; those sectors decide the case.

**TIC 80387959 (TYC 8203-2056-1)** — K dwarf, Tmag 10.5, 116 pc. A 4.192173-d, ≈ 700 ppm, 2.2-h transit seen 24 times in 2019–2026
(QLP full-frame images; TESS-SPOC extraction agrees). Radius ≈ 2.4 Earth radii if on the target. On target by pixel tests (the only
neighbours able to mimic it are excluded at ≈ 2.7σ and ≈ 4σ); no secondary eclipse; stellar density consistent; four of four blind holdout
years recovered; TRICERATOPS FPP 0.047, NFPP 0.010 (indicative, not validated); no catalog entry within 60″. An external review
([external_review_allsky/REVIEW.md](external_review_allsky/REVIEW.md)) found the apparent sector-to-sector depth change to be a QLP
normalisation artefact. Status: planet candidate pending the pre-registered test (an unpromoted TESS-SPOC Sector-63 pipeline alert at the same period exists, see below). **Test of record: TESS Sector 111 (2026-11-26 to
12-22)**; predictions in `preregistration/TIC80387959/` (v2 supersedes v1, which used only the 200-s sectors).

**TIC 120444365** — K dwarf, Tmag 11.1. A 5.148171-d, ≈ 750 ppm transit seen 22 times in 2018–2026, in every year and in every
independent extraction (SPOC 2-min, TESS-SPOC, TARS, fixed-aperture cutouts). Radius ≈ 2.2 Earth radii if on the target. Isolated star
(nothing within 60″ can mimic it); on target by pixel tests; TRICERATOPS FPP 0.041, NFPP 0.000 ("likely planet" by the published
criteria, not validated). Status: planet candidate pending the pre-registered test; **independently listed earlier by eumemic/exoplanets (2026-10-09), see below**. **Test of record: TESS Sector 106** (observed
2026-07-11 to 08-09; its QLP light curves were not yet released when the predictions were frozen on 2026-10-18, but other public S106 data products, including image data, existed; the authors attest they did not examine this star's S106 photometry before the freeze. See `ERRATUM_S106_DATA_AVAILABILITY_2026-10-20.md`. QLP light curves are expected in late
October 2026); predictions in `preregistration/TIC120444365/`.

A third signal from the same search, in a crowded field, is withheld until its host star can be assigned from the ground (it too is listed in eumemic/exoplanets).

**TIC 183374279** — K dwarf (TIC v8.2: Teff 4518 K, R = 0.708 R_sun, Tmag 11.40). An approximately 11.73798-d transit-like signal of about 2.8 h and 1.0–1.4 ppt depth (QLP detrended 970 ppm; raw SAP 1090 ± 90 ppm; SPOC 2-min S29 1380 ppm at the known ephemeris; sky-subtracted cutouts 1200–1540). Formal depth/error ratios of 3–10 appear in each of the five observed years on QLP's detrended flux; this is not a product-independent significance (raw SAP 2023: 2.3). Radius about 2.3–2.9 Earth radii if on the target (an illustrative scale from three depth measures, not a confidence interval). The shape-fit stellar density is 1.24× the catalogue value with the adopted TIC mass and radius. Odd/even 0.4σ; no secondary detected at phase 0.5 (45 ± 82 ppm). Retrospective leave-one-year-out checks show positive predicted-phase dimming in the four testable years (formal SNR 4.6, 3.2, 3.7, 8.1). These are consistency checks, not independent confirmations. The loss centroid is consistent with the target under the tested estimator (0.06–0.40 px); that test does not localise the source or give an exclusion probability. Catalogued sources within 60″ are too faint to explain the depth under the adopted flux and aperture models; unresolved or uncatalogued contamination remains possible. The SPOC 2-min transit is an extraction check, not a blend test or an independent detection. TRICERATOPS FPP 0.031 (above the 0.015 validation threshold; NFPP 0 is structural in this setup; no contrast curve). Gaia DR3: RUWE 1.12, not duplicated, no non-single-star solution, no significant RV variability in the summary test (p = 0.28; no mass limit). No TOI/CTOI within 60″; no earlier public report found in the searched sources (bounded search). Status: unvalidated planet candidate. **Test of record: TESS Sector 106** (2026-07-11 to 08-09), scored with the conformance procedure (to be published before any S106 photometry of the star is examined). Epochs 245 and 246 (geocentric 2026-07-16 21:14:45 and 07-28 14:56:35 UTC; σ 2.7 and 2.8 min) lie inside the science orbits; epoch 247 will be partial. Data gaps may leave fewer than two eligible events (INSUFFICIENT); no further TESS sector is scheduled through S134. S106 data products existed before the freeze (ERRATUM_S106_DATA_AVAILABILITY); the authors attest no S106 photometry of this star has been examined. Predictions in `preregistration/TIC183374279/` (v2 ephemeris).

**TIC 61310956** — K dwarf (TYC 1428-1096-1, Tmag 10.6; Gaia DR3 VARIABLE flag). An approximately 16.53797-d transit-like signal in six QLP events (Sectors 22 ×2, 45, 46, 72 ×2). Raw-SAP depth about 1.33 ppt (formal box SNR 12.7); median shape-fit duration 3.3 h (the frozen v3 reference duration is 2.70 h; see the dated clarification in its registration). The 2020–2021 events are recovered in SPOC 2-min data at the known ephemeris (1068 ppm; 4 exceedances in 388 random-phase draws); the 2-min data alone do not recover the period, so this is an extraction check, not an independent detection. Radius about 2.5–3.2 Earth radii if on the target. **Odd/even depths are baseline-sensitive** (1.2σ on detrended flux, 3.75σ on raw SAP with a global baseline, 1.76σ with local baselines). This is a photometric-systematics caveat, not a demonstrated eclipsing binary, but a 2P eclipsing binary remains an alternative. No secondary detected (−29 ± 102 ppm). Retrospective holdout checks are positive in both testable years (formal SNR 7.9, 4.9). The loss centroid is consistent with the target under the tested estimator in Sectors 22, 45 and 72 (not a calibrated localisation). TRICERATOPS FPP 0.020 (above the 0.015 validation threshold; NFPP 0 structural; no contrast curve). No TOI/CTOI within 60″; no earlier independent report found in the searched sources. Its period and depth were public as a row of our own `tables/allsky_testable_soon.csv` at releases v1.3–v1.5 (2026-10-18 23:24 to 2026-10-19 12:16 UTC) and masked at v1.6. Status: unvalidated planet candidate, with a photometric-systematics caveat.
**No TESS revisit through Sector 134; the test of record is ground-based.** Predictions v3 (frozen 2026-10-19 14:09 UTC, one timing per sector; σ about 28 min growing to 33 min at the end of 2027) supersede v2, which counted Sectors 22 and 45 twice. Nominal contacts for epochs 151, 152 and 153 are accessible from the Canaries, Japan and Chile respectively (epoch-151 geocentric mid-time 2026-12-29 04:21:53 UTC). Covering the full ±3σ timing support, the 3.3-h duration and 1-h baselines needs about 8.1–8.2 h, which may require several sites. A test needs ≤ 1.5 mmag per 10-min bin around at least two predicted transits.

### All-sky round 2: every frozen object (v1.7)
All 26 stars whose transit was on target after the pixel test were checked against the full prior-detection sweep (`prior_search_round2/`).
Predictions are frozen for the 18 below; the other eight are listed in `tables/allsky_classA_round2_outcomes.csv` only (seven failed the
stellar-density or odd/even test; TIC 3367979 is an eumemic rediscovery with a marginal density). Only the two objects above are claimed as
candidates. Marginal and weak objects are frozen so that any later report can be checked against a dated ephemeris; most are expected to fail.

| TIC | P (d) | tier | prior report | test |
|---|---|---|---|---|
| 183374279 | 11.73798 | candidate | none | TESS S106 |
| 61310956 | 16.53797 | candidate | none | ground |
| 258006047 | 10.02224 | credited rediscovery (crowded: 2.6″ companion) | B. Murray, Zenodo 23230562, 2026-10-08 | TESS S114 |
| 333735955 | 11.22618 | credited rediscovery; density 4× | Murray 2026-10-08; eumemic/exoplanets 2026-10-09 | TESS S114 |
| 366047768 | 9.49897 | credited rediscovery | eumemic/exoplanets 2026-10-09 | TESS S121 |
| 65575657 | 5.18788 | credited rediscovery | eumemic/exoplanets 2026-10-09 | ground |
| 383617106 | 9.49916 | credited rediscovery | eumemic/exoplanets 2026-10-09 | ground |
| 249813122 | 4.17615 | marginal (density 5×) | none | TESS S122 |
| 70441745 | 15.85190 | marginal (density 5×; one sector time) | none | TESS S106 |
| 203381983 | 9.73639 | marginal (density 4×) | none | TESS S115 |
| 36694943 | 12.89889 | marginal (density 3×) | none | TESS S134 |
| 376225363 | 3.44662 | weak (SNR 8) | none | TESS S122 |
| 467959906 | 7.80014 | weak (SNR 8) | none | TESS S114 |
| 50514263 | 14.59315 | weak (SNR 7) | none | TESS S124 |
| 245503256 | 14.58187 | weak (SNR 8) | none | TESS S124 |
| 332709057 | 12.56298 | weak (SNR 8) | none | ground |
| 371421714 | 11.68257 | weak (SNR 5) | none | ground |
| 91617711 | 15.07141 | weak (two sectors) | none | ground |



## Prior and concurrent reports (prior-detection sweep of 2026-10-18/19, `prior_search/`)
A documented sweep of 32 services (1,585 logged queries; 558,074 automated pipeline alerts scanned: 341,351 SPOC TCE rows and 216,723
TESS-SPOC FFI DV targets; 101 GitHub repositories and 157 Zenodo records grepped by content) found:
* **TIC 89247735**: no prior report of any kind. A **concurrent** independent analysis (same four transits, P = 18.323173 ± 0.000031 d) was
  posted at github.com/alejandrozarco/tess-candidates-2026 on 2026-10-18 19:22 UTC, about twenty hours after this record's first public
  release (GitHub v1.0 2026-10-17 23:01 UTC; Zenodo 2026-10-17 23:05 UTC). It does not cite this record.
* **TIC 80387959**: no human-reported candidate anywhere, but the TESS-SPOC FFI pipeline's Sector 63 single-sector run produced an
  unpromoted threshold-crossing event at the same signal (P = 4.1905 ± 0.0012 d, 869 ± 107 ppm, 2.4 R⊕, MES 7.6), never a TOI or CTOI. Our
  known-signal cross-match had covered SPOC 2-min TCEs only; TESS-SPOC TCEs are now included.
* **TIC 120444365**: **listed earlier** by an independent, pseudonymous, non-refereed search (github.com/eumemic/exoplanets, tier-C candidate at
  P = 5.148151 d, 856 ppm, first public commit 2026-10-09 03:34 UTC), nine days before our deposit. Ours is an independent rediscovery with
  deeper vetting (pixel localisation, extraction cross-checks, TRICERATOPS NFPP 0.000, external review, Sector 106 pre-registration); priority
  of the listing is theirs.
* **TIC 317134140 (0.5719-d second signal)**: **listed earlier** by the same repository as a tier-A candidate (first commit 2026-10-08 03:14 UTC)
  with Sector 109/110 predictions; again an independent rediscovery on our side.
Statements elsewhere in this record that an object has "no catalog entry" refer to the TOI, CTOI, Exoplanet Archive and SPOC TCE tables and
remain true; they are not claims of priority over the listings above.

## Pre-registration
**Correction 2026-10-19:** the UTC columns of all prediction files published before this date lacked the barycentric light-travel term (up to ±8 min); `tc_bjd_tdb` and all hashes are unaffected. Corrected copies (`*_utcfix.csv`) and the details are in `preregistration/CORRECTION_UTC_2026-10-19.md`.

**Correction 2026-10-19 (v1.8), found by an external review:**
1. The QLP v01 light curves of Sectors 99–104 carry the barycentric clock error that MAST has announced. Sector 105 is also affected, which the notice does not cover: there the QLP times lack the barycentric correction. For TIC 89247735 the Sector-104 times were 8.02 min early, and our earlier statement that they had been verified was wrong. The new version-4 ephemeris is `preregistration/TIC89247735/PREREGISTRATION_v4.md`; version 1 remains the test of record.
2. For every other frozen object that used QLP S99+ times, `preregistration/ADDENDUM_QLP_CLOCK_2026-10-19.md` gives the size of the effect. Predictions move by −0.04 to +3.9 min (at most about 1.1σ), and no outcome rule changes. QLP test data from S99 onward (including Sector 106) will be clock-checked against TESScut before any test is run.
3. The ingress and egress columns of the TIC 89247735 `*_utcfix.csv` files were not light-time corrected. `*_utcfix2.csv` fixes them; details are in `CORRECTION_UTC_2026-10-19b.md`.

**Correction 2026-10-19 (v1.9), found by a further external review:** v1.8's clock corrections wrongly treated TESScut `TIMECORR` as specific to the target (it refers to a reference position in the image). Recomputed with JPL Horizons TESS vectors, the TIC 89247735 Sector-104 correction is +7.53 min, not +8.02 min. The new version-5 ephemeris (`preregistration/TIC89247735/PREREGISTRATION_v5.md`) supersedes v4, and version 1 remains the test of record. The revised clock addendum (`preregistration/ADDENDUM_QLP_CLOCK_2026-10-19b.md`) supersedes v1.8's. Shifts of the frozen predictions are at most 1.2σ for the seven other objects and 1.25–1.38σ for TIC 89247735's v5 refinement, and no outcome rule changes. `MANIFEST_v1.9.md` lists which files are current and which are superseded.

**Erratum and clarification 2026-10-20 (v1.10):**
1. **Data availability.** Several pre-registrations said TESS Sector 106 (and, for three local round-3 records, Sector 107) was "observed, data not public at freeze". That was wrong. Target QLP light curves were not yet released, but other public data products for those sectors existed, including image data available since mid-August 2026. We attest that we did not examine the target-sector photometry before the freezes. These tests are therefore held-out checks of already-observed data, not prospective predictions. One test, TIC 88407114 Sector 106, is withdrawn because its frozen fit included S106 data. See `preregistration/ERRATUM_S106_DATA_AVAILABILITY_2026-10-20.md` and `ERRATUM_S106_MANIFEST.csv`.
2. **Timing rule.** The per-object registration text ("within +-3 sigma (and in any case within +-30 min)") conflicted with the published protocol and frozen evaluator (max(3 sigma, 30 min)). We adopt the protocol rule as a dated precedence decision, and will also report the narrower per-event reading. See `preregistration/CLARIFICATION_TIMING_RULE_2026-10-20.md`.
3. **Evaluator limitations.** Independent reviews (`reviews_2026-10-20/`) found that the frozen evaluator `prereg_test.py` does not check transit duration, averages timing offsets, and can return EXCLUDED without full transit coverage. Its literal output will be kept, but no TESS outcome will be reported until a separately versioned conformance procedure has been published.
4. **Notes on the registrations.** Dated notes are appended to the affected registrations; original texts, prediction CSVs and their hashes are unchanged.

**Conformance procedure for the Sector 106 tests (2026-10-20, v1.11):** published before any Sector 106 photometry of a test target was examined. See `conformance_v2.1/`.
1. **Scoring.** The seven S106 tests (TIC 183374279, 120444365, 70441745, 206620592, 122522485, 253931796, 115692561) are scored with the separately versioned conformance procedure (`conformance_v2.1/CONFORMANCE_PROCEDURE_v2.1.md`). Its evaluator SHA-256 is locked in each test's config. The frozen `prereg_test.py` output is reported alongside, but it is not the outcome of record. The procedure is an amended operational test; every departure from the protocol is listed in `conformance_v2.1/GOVERNANCE_S106_TESTS_2026-10-20.md`.
2. **Review.** The procedure was reviewed externally four times (rc1 to rc4, `conformance_v2.1/reviews/`). An earlier version (v2.0) was withdrawn before publication after an internal adversarial review.
3. **Advance statements**, conditional on in-sample noise and gap templates (they are not outcome probabilities):
   - 70441745 is the one test with high power.
   - 253931796, and probably 183374279, are expected to have fewer than two usable transits (INSUFFICIENT). Neither has a further TESS sector through S134.
   - 115692561 and 122522485 have low expected signal-to-noise.
   - The family-wise false-RECOVERED rate across the seven tests is not calibrated.
4. **Protocol erratum.** The protocol gives TIC 120444365's first-epoch sigma as 4.7 min, which is the superseded v1 value. The v2 file of record gives 2.1 min (`preregistration/ERRATUM_PROTOCOL_2026-10-20.md`).
5. **Dossier corrections.** The TIC 183374279 and TIC 61310956 summaries above were corrected after an external dossier referee (`referee_round2/REFEREE_REPORT_dossiers_external.md`). TIC 61310956 has a dated clarification of its reference duration in its v3 registration.

**All-sky round 3 (2026-10-20):** 190 previously unvetted signals with an upcoming TESS sector were run through the same pipeline: pixel test, then vetting, triage, prior-report check, TRICERATOPS and an independent review. 15 objects have frozen predictions in `preregistration/TIC<id>/`; the outcome table is `tables/allsky_round3_outcomes.csv`.
- **Labels:**
  - 1 candidate, TIC 206620592 (unvalidated);
  - 3 marginal (122522485, 196514928, 253931796);
  - weak signals;
  - 5 credited rediscoveries (eumemic/exoplanets, brahle, killercatfish/tess-hunt and Zenodo 23289478).
- **Not validated:** none of these passes statistical validation thresholds, and all are small (~1–4 Earth radii).
- **Excluded from the test record:**
  - **TIC 53825235 and TIC 408110117:** their v2 files contain no eligible predictions (a generator defect, since fixed), so they carry no valid test.
  - **TIC 162304222:** superseded by a v3 freeze for Sector 111.


Each `PREREGISTRATION.md` records the ephemeris, the freeze time (UTC) and the SHA-256 of its CSV of predicted transit times.
The first commit of this repository is the public timestamp. The files are not edited after freezing; corrections are new versions.

## Reproduce
`scripts/` contains the full pipeline (Python 3.12; lightkurve, astropy, wotan, batman, emcee, transitleastsquares, tess-point).
Data are public (MAST). Commands are listed in the header of [REPORT.md](REPORT.md) section 3 and in `scripts/*.py` docstrings.

## Related Zenodo records (2026-10-19)
* Preprint (research note on TIC 80387959 and TIC 120444365): concept DOI [10.5281/zenodo.23462433](https://doi.org/10.5281/zenodo.23462433) (v1.0 23462434, v1.1 23462857)
* Supporting data and code (all objects; checksummed bundle): [10.5281/zenodo.23462438](https://doi.org/10.5281/zenodo.23462438)
* Pre-registration protocol v1 and frozen prediction bundle: [10.5281/zenodo.23462442](https://doi.org/10.5281/zenodo.23462442)
* This repository's releases (concept DOI 10.5281/zenodo.23443244): v1.1 = 23443245, v1.2 = 23445705, v1.3 = 23460915, v1.4 = pending archive.

## Cite
Molina, F. (2026). Multi-year TESS transit search: two planet candidates with pre-registered transit predictions (TIC 89247735, TIC 317134140). Zenodo. https://doi.org/10.5281/zenodo.23443245 — machine-readable form in [CITATION.cff](CITATION.cff). Code is MIT-licensed; text and tables may be reused with attribution.
