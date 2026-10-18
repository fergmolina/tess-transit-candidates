# TESS multi-year transit search: two planet candidates with pre-registered predictions

**Author:** Fernando Molina (Independent researcher, ORCID [0009-0002-2872-3406](https://orcid.org/0009-0002-2872-3406)). Analysis performed with Claude (Anthropic) under the author's direction.
**Date:** 2026-10-17. **DOI:** [10.5281/zenodo.23443245](https://doi.org/10.5281/zenodo.23443245) [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23443245.svg)](https://doi.org/10.5281/zenodo.23443245) **Status of every object here: candidate pending confirmation. Nothing in this repository is a validated planet.**

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

## Pre-registration
Each `PREREGISTRATION.md` records the ephemeris, the freeze time (UTC) and the SHA-256 of its CSV of predicted transit times.
The first commit of this repository is the public timestamp. The files are not edited after freezing; corrections are new versions.

## Reproduce
`scripts/` contains the full pipeline (Python 3.12; lightkurve, astropy, wotan, batman, emcee, transitleastsquares, tess-point).
Data are public (MAST). Commands are listed in the header of [REPORT.md](REPORT.md) section 3 and in `scripts/*.py` docstrings.

## Cite
Molina, F. (2026). Multi-year TESS transit search: two planet candidates with pre-registered transit predictions (TIC 89247735, TIC 317134140). Zenodo. https://doi.org/10.5281/zenodo.23443245 — machine-readable form in [CITATION.cff](CITATION.cff). Code is MIT-licensed; text and tables may be reused with attribution.
