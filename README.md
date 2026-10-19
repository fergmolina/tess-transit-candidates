# TESS multi-year transit search: two planet candidates with pre-registered predictions

**Author:** Fernando Molina (Independent researcher, ORCID [0009-0002-2872-3406](https://orcid.org/0009-0002-2872-3406)). Analysis performed with Claude (Anthropic) under the author's direction.
**Date:** 2026-10-17, updated 2026-10-19 (v1.7: TIC 61310956 and all round-2 frozen objects; referee corrections). **DOI:** [10.5281/zenodo.23443245](https://doi.org/10.5281/zenodo.23443245) [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23443245.svg)](https://doi.org/10.5281/zenodo.23443245) **Status of every object here: candidate pending confirmation. Nothing in this repository is a validated planet.**

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
2026-07-11 to 08-09; its light curves were not public when the predictions were frozen on 2026-10-18 and are expected in late
October 2026); predictions in `preregistration/TIC120444365/`.

A third signal from the same search, in a crowded field, is withheld until its host star can be assigned from the ground (it too is listed in eumemic/exoplanets).

**TIC 183374279** — K dwarf (TIC v8.2: Teff 4518 K, R = 0.708 R_sun, Tmag 11.40), isolated: the nearest star able to mimic the signal is 72″ away and would need a 22 % eclipse, and no Gaia DR3 source within 60″ can produce the depth. An 11.737984-d transit of 2.8-h duration and 1.0–1.4 ppt depth (QLP detrended 970 ppm; raw SAP 1090 ± 90; SPOC 2-min S29 1380 ± 290; sky-subtracted cutouts 1200–1540), present at 3–10σ in each of the five observed years (2018, 2020, 2023, 2025, 2026). Radius 2.3–2.9 Earth radii if on the target (the range follows the depth range). Stellar density from the shape consistent with the catalogue (1.4 +0.6/−0.9), odd/even 0.4σ, secondary at phase 0.5 45 ± 82 ppm. The signal is recovered in each of the four testable blind-holdout years (2020, 2023, 2025, 2026 at 4.6, 3.2, 3.7 and 8.1σ; the 2018 holdout had no covered transit). Flux-loss centroid consistent with the target in all three 200-s sectors (0.1–0.4 px, calibrated errors 0.16–0.22 px; combined offset 3 ± 2″): this excludes blends 20–60″ away but not an unresolved companion inside ~1 px. The single SPOC 2-min transit of Sector 29 gives 1380 ± 290 ppm (empirical error) at the QLP ephemeris; the 2-min data alone do not yield the period and the aperture contains the same stars, so this is an extraction check, not a blend test. TRICERATOPS FPP 0.031, NFPP 0.000 (no contrast curve; above the 0.015 validation threshold; indicative at SNR 12). Gaia DR3: RUWE 1.12, not a duplicated source, no non-single-star solution, RV constant over 16 epochs. No TOI/CTOI/TCE within 60″; round-2 prior-detection sweep: no prior report. Status: planet candidate pending the pre-registered test. **Test of record: TESS Sector 106** (2026-07-11 to 08-09). Two predicted transits (2026-07-16 21:14 and 07-28 14:56 UTC, σ 2.7 min) fall inside the science orbits; the third (08-09 08:38 UTC) is cut by the end of orbit 224 at 09:10 UTC and will be partial, so the test rests on two events. The QLP light curve had not been released at the freeze (2026-10-19 11:44 UTC) and no Sector 106 data of any kind were examined before it; whether FFIs were already retrievable through TESScut was not checked. Predictions in `preregistration/TIC183374279/` (v2 ephemeris, geocentric UTC; addendum of 2026-10-19 in the frozen record).

**TIC 61310956** — K dwarf (TYC 1428-1096-1, Tmag 10.6; Gaia DR3 / VSX rotational variable), isolated: the nearest star able to mimic the
signal is 82″ away and would need 20 %, and no Gaia DR3 source within 60″ can produce the depth. A 16.538-d transit of 3.3-h duration and
1.0–1.5 ppt depth: six events in QLP FFI data (Sectors 22 ×2, 45, 46, 72 ×2). The three 2020–2021 events are also recovered in the SPOC 2-min
light curves at the QLP ephemeris (1068 ± 240 ppm, 4.5σ empirical); the 2-min data alone do not yield the period, so this is an extraction check,
not an independent detection. Radius 2.5–3.2 Earth radii if on the target. Density from the shape consistent with the catalogue (1.4 +0.6/−0.8),
secondary −29 ± 102 ppm, odd/even 1.2σ, blind holdout recovered in both testable years, flux-loss centroid consistent with the target in Sectors
22, 45 and 72 (0.1–0.3 px, calibrated errors 0.14–0.24 px). TRICERATOPS FPP 0.020, NFPP 0.000 (no contrast curve; above the 0.015 validation
threshold). No TOI/CTOI/TCE within 60″; round-2 prior-detection sweep: no prior report. Its period and depth were public as a row of our own
`tables/allsky_testable_soon.csv` at releases v1.3–v1.5 (2026-10-18 23:24 to 2026-10-19 12:16 UTC) and masked at v1.6. Status: planet candidate.
**No TESS revisit through Sector 134; the test of record is ground-based.** Predictions v3 (frozen 2026-10-19 14:09 UTC, σ ≈ 28 min through 2027,
one timing per sector) supersede v2, which counted Sectors 22 and 45 twice (found by the round-2 referee review, `referee_round2/`). A test needs
≈ 1 mmag photometry over ≈ 7 h around two predicted transits.

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
