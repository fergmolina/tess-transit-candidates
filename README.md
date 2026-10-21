# TESS multi-year transit search: two planet candidates with pre-registered predictions

**Author:** Fernando Molina (Independent researcher, ORCID [0009-0002-2872-3406](https://orcid.org/0009-0002-2872-3406)). Analysis performed with Claude (Anthropic) under the author's direction.
**Date:** 2026-10-17, updated 2026-10-21 (v1.15: all-sky round 4 - three new pre-registered tests, two of them independent rediscoveries; locked scoring configs; errata on truncated prediction lists and on earlier machine detections missed by our searches, including a RAVEN first-stage detection of TIC 80387959, so no first-detection claim is made for it; v1.14: TIC 120517801 published - likely blend, host unresolved, independent rediscovery; v1.13: follow-up corrections from the re-check of v1.12 - exposure handling in vet.py, freeze guard, documentation and DOI labels; v1.12: corrections after an independent full-repository review - masking of a withheld object, superseded claims marked, code fixes, scripts synced; v1.11: conformance procedure for the Sector 106 tests, protocol erratum, dossier corrections; v1.10: data-availability erratum, timing-rule clarification, all-sky round 3 frozen predictions; see below). **DOI (all versions, concept):** [10.5281/zenodo.23443244](https://doi.org/10.5281/zenodo.23443244) [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23443244.svg)](https://doi.org/10.5281/zenodo.23443244) **Status of every object here: candidate pending confirmation. Nothing in this repository is a validated planet.**

A search of public NASA TESS photometry (SPOC 2-min light curves for 1,637 dwarfs and QLP full-frame-image light curves for
3,411 dwarfs, sectors 1 to 107, 2018 to 2026) for periodic transit-like signals that repeat with the same period and phase in
different years and are absent from the TOI, CTOI, confirmed-planet and TCE catalogs. Method modelled on Rabtsevich (2026, TIC 4206066).
Full methods, results, rejected objects and null calibrations are in [REPORT.md](REPORT.md); every decision is logged in
[DECISIONS.md](DECISIONS.md); an independent adversarial review is in [external_review/REVIEW.md](external_review/REVIEW.md).

## Candidates

**TIC 89247735 (SCR J1820-4533)** — K dwarf, Tmag 11.1, ≈ 105 pc. Four approximately 1.1 %-deep, 4.54-h transit-like events in 2023, 2025 (two, consecutive) and 2026 follow the clock-corrected v5 ephemeris, P = 18.323174 ± 0.000040 d. No secondary eclipse was detected, and there is no catalogue entry. Conditional on the target hosting the signal and the adopted deblending, Rp ≈ 7.9–8.4 Earth radii. A G = 15.5 neighbour about 7″ away remains a possible eclipsing-binary host, and the companion mass is unconstrained. The four event times do not exclude a binary at twice the period with alternating primary and secondary eclipses. *(Corrected 2026-10-20: earlier text claimed on-target pixel tests and a Gaia mass bound below about 25 Jupiter masses; both are withdrawn.)* Status: transiting companion candidate, not validated.
Predicted transit times are frozen in `preregistration/TIC89247735/`. Version 1 (three transits) remains the test of record; v5 is the current timing refinement.
The v5 geocentric midpoints are 2027-06-25 02:10 and 2027-08-19 01:29 UTC; at CTIO, epoch 159 qualifies, while epoch 162 is marginal (it narrowly fails the stated ingress darkness cut).

**TIC 317134140 (TOI-2514 host)** — a second, 0.571863-d, ~185 ppm signal (1.4 Earth radii if on target) recovered in data from
2018, 2020, 2024, 2025 and 2026. Plausible but unproven: the periodogram statistic alone is within the false-positive expectation,
one 2020 sector does not show it and one sector's centroid is in tension. Transit times for TESS Sectors 108 to 110 are frozen in
`preregistration/TIC317134140/`; those sectors decide the case.

**TIC 80387959 (TYC 8203-2056-1)** — K dwarf, Tmag 10.5, 116 pc. A 4.192173-d, ≈ 700 ppm, 2.2-h transit seen 24 times in 2019–2026
(QLP full-frame images; TESS-SPOC extraction agrees). Radius ≈ 2.4 Earth radii if on the target. On target by pixel tests (the only
neighbours able to mimic it are excluded at ≈ 2.7σ and ≈ 4σ); no secondary eclipse; stellar density consistent; four of four blind holdout
years recovered; TRICERATOPS FPP 0.047, NFPP 0.010 (indicative, not validated); no TOI, CTOI, Exoplanet Archive or SPOC 2-min TCE entry within 60″. **Correction 2026-10-21:** the signal was previously reported in the first-stage RAVEN candidate catalog (Lafarga et al. 2026), see below; we do not claim first detection. An external review
([external_review_allsky/REVIEW.md](external_review_allsky/REVIEW.md)) found the apparent sector-to-sector depth change to be a QLP
normalisation artefact. Status: planet candidate pending the pre-registered test; an independent recovery of an earlier RAVEN first-stage detection, and an unpromoted TESS-SPOC Sector-63 pipeline alert at the same period exists (see below). **Test of record: TESS Sector 111 (2026-11-26 to
12-22)**; predictions in `preregistration/TIC80387959/` (v2 supersedes v1, which used only the 200-s sectors).

**TIC 120444365** — K dwarf, Tmag 11.1. A 5.148171-d, ≈ 750 ppm transit seen 22 times in 2018–2026, in every year and in every
independent extraction (SPOC 2-min, TESS-SPOC, TARS, fixed-aperture cutouts). Radius ≈ 2.2 Earth radii if on the target. Isolated star
(nothing within 60″ can mimic it); consistent with the target under the tested pixel estimator; TRICERATOPS FPP 0.041, above the 0.015 validation
threshold (NFPP 0 is structural in this setup); not validated. Status: planet candidate pending the pre-registered test; **independently listed earlier by eumemic/exoplanets (2026-10-09), see below**. **Test of record: TESS Sector 106** (observed
2026-07-11 to 08-09; its QLP light curves were not yet released when the predictions were frozen on 2026-10-18, but other public S106 data products, including image data, existed; the authors attest they did not examine this star's S106 photometry before the freeze. See `ERRATUM_S106_DATA_AVAILABILITY_2026-10-20.md`. QLP light curves are expected in late
October 2026); predictions in `preregistration/TIC120444365/`.

**TIC 120517801** (K dwarf, Tmag 11.4; published 2026-10-20 after being withheld until v1.13) — a real, stable 3.28-d transit-like signal of about 760 ppm (fixed-aperture 759 ± 59 ppm; present since 2019), in a crowded field. **Likely blend, host unresolved:**
- A G = 14.7 star 4.2″ (about 0.20 TESS pixel) away needs only about a 1 % eclipse to produce the signal. An external review placed the combined flux-loss position 1.7″ from that star and 5.4″ from the target. Our TESS analyses do not assign the eclipse to either star.
- TRICERATOPS FPP 0.088 and NFPP 0.062 are well above the validation thresholds.
- The retrospective year checks only show the signal is persistent; they say nothing about the host.

**Independent rediscovery:** listed earlier by eumemic/exoplanets (2026-10-09) and by Rahle (2026-10-18).

Its ephemeris is pre-registered (`preregistration/TIC120517801/`; v2 P = 3.282292 ± 0.000024 d). **Provenance (2026-10-20):** The decision-log commit 24cd0de, dated 2026-10-18 23:24:45 UTC, contains the eight-character v1/v2 SHA-256 prefixes; the independently archived v1.3 ZIP also contains them (Zenodo record created 23:24:53.814353 UTC). These abbreviated anchors do not authenticate the complete CSV bytes. The original published supporting dataset also exposed v1 ephemeris values and a 24-row test-time summary under a masked label. This release intentionally supplies the named full registrations, original CSVs and full SHA-256 digests. The earlier local freeze times and non-examination statements remain the author's attestations. The test is TESS Sectors 111–113 (ephemeris only); assigning the host needs seeing-limited ground photometry of every Gaia star within 2.5′.

**TIC 183374279** — K dwarf (TIC v8.2: Teff 4518 K, R = 0.708 R_sun, Tmag 11.40). An approximately 11.73798-d transit-like signal of about 2.8 h and 1.0–1.4 ppt depth (QLP detrended 970 ppm; raw SAP 1090 ± 90 ppm; SPOC 2-min S29 1380 ppm at the known ephemeris; sky-subtracted cutouts 1200–1540). Formal depth/error ratios of 3–10 appear in each of the five observed years on QLP's detrended flux; this is not a product-independent significance (raw SAP 2023: 2.3). Radius about 2.3–2.9 Earth radii if on the target (an illustrative scale from three depth measures, not a confidence interval). The shape-fit stellar density is 1.24× the catalogue value with the adopted TIC mass and radius. Odd/even 0.4σ; no secondary detected at phase 0.5 (45 ± 82 ppm). Retrospective leave-one-year-out checks show positive predicted-phase dimming in the four testable years (formal SNR 4.6, 3.2, 3.7, 8.1). These are consistency checks, not independent confirmations. The loss centroid is consistent with the target under the tested estimator (0.06–0.40 px); that test does not localise the source or give an exclusion probability. Catalogued sources within 60″ are too faint to explain the depth under the adopted flux and aperture models; unresolved or uncatalogued contamination remains possible. The SPOC 2-min transit is an extraction check, not a blend test or an independent detection. TRICERATOPS FPP 0.031 (above the 0.015 validation threshold; NFPP 0 is structural in this setup; no contrast curve). Gaia DR3: RUWE 1.12, not duplicated, no non-single-star solution, no significant RV variability in the summary test (p = 0.28; no mass limit). No TOI/CTOI within 60″; no earlier public report found in the searched sources (bounded search). Status: unvalidated planet candidate. **Test of record: TESS Sector 106** (2026-07-11 to 08-09), scored with the conformance procedure v2.1, published on 2026-10-20 (release v1.11, `conformance_v2.1/`) before any S106 photometry of the star was examined. Epochs 245 and 246 (geocentric 2026-07-16 21:14:45 and 07-28 14:56:35 UTC; σ 2.7 and 2.8 min) lie inside the science orbits; epoch 247 will be partial. Data gaps may leave fewer than two eligible events (INSUFFICIENT); no further TESS sector is scheduled through S134. S106 data products existed before the freeze (ERRATUM_S106_DATA_AVAILABILITY); the authors attest no S106 photometry of this star has been examined. Predictions in `preregistration/TIC183374279/` (v2 ephemeris).

**TIC 61310956** — K dwarf (TYC 1428-1096-1, Tmag 10.6; Gaia DR3 VARIABLE flag). An approximately 16.53797-d transit-like signal in six QLP events (Sectors 22 ×2, 45, 46, 72 ×2). Raw-SAP depth about 1.33 ppt (formal box SNR 12.7); median shape-fit duration 3.3 h (the frozen v3 reference duration is 2.70 h; see the dated clarification in its registration). The 2020–2021 events are recovered in SPOC 2-min data at the known ephemeris (1068 ppm; 4 exceedances in 388 random-phase draws); the 2-min data alone do not recover the period, so this is an extraction check, not an independent detection. Radius about 2.5–3.2 Earth radii if on the target. **Odd/even depths are baseline-sensitive** (1.2σ on detrended flux, 3.75σ on raw SAP with a global baseline, 1.76σ with local baselines). This is a photometric-systematics caveat, not a demonstrated eclipsing binary, but a 2P eclipsing binary remains an alternative. No secondary detected (−29 ± 102 ppm). Retrospective holdout checks are positive in both testable years (formal SNR 7.9, 4.9). The loss centroid is consistent with the target under the tested estimator in Sectors 22, 45 and 72 (not a calibrated localisation). TRICERATOPS FPP 0.020 (above the 0.015 validation threshold; NFPP 0 structural; no contrast curve). No TOI/CTOI within 60″; no earlier independent report found in the searched sources. Its period and depth were public as a row of our own `tables/allsky_testable_soon.csv` at releases v1.3–v1.5 (2026-10-18 23:24 to 2026-10-19 12:16 UTC) and masked at v1.6. Status: unvalidated planet candidate, with a photometric-systematics caveat.
**No TESS revisit through Sector 134; the test of record is ground-based.** Predictions v3 (frozen 2026-10-19 14:09 UTC, one timing per sector; σ about 28 min growing to 33 min at the end of 2027) supersede v2, which counted Sectors 22 and 45 twice. Nominal contacts for epochs 151, 152 and 153 are accessible from the Canaries, Japan and Chile respectively (epoch-151 geocentric mid-time 2026-12-29 04:21:53 UTC). Covering the full ±3σ timing support, the 3.3-h duration and 1-h baselines needs about 8.1–8.2 h, which may require several sites. A test needs ≤ 1.5 mmag per 10-min bin around at least two predicted transits.

### All-sky round 2: every frozen object (v1.7)
All 26 stars whose transit was on target after the pixel test were checked against the full prior-detection sweep (`prior_search_round2/`).
Predictions are frozen for the 18 below; the other eight are listed in `tables/allsky_classA_round2_outcomes.csv` only (seven failed the
stellar-density or odd/even test; TIC 3367979 is an eumemic rediscovery with a marginal density; *note 2026-10-21: 3367979 was in fact frozen locally on 2026-10-19 but not published; its records, with a v4 ground registration, are now in `preregistration/TIC3367979/`*). Only the two objects above are claimed as
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
| 249813122 | 4.17615 | marginal (density 5×) | none found then; RAVEN first stage (notice 2026-10-21) | TESS S122 |
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
* **TIC 89247735**: no earlier matching report was found in the sources searched by this dated sweep; its coverage and indexing limits apply. A **concurrent** independent analysis (same four transits, P = 18.323173 ± 0.000031 d) was
  posted at github.com/alejandrozarco/tess-candidates-2026 on 2026-10-18 19:22 UTC, about twenty hours after this record's first public
  release (GitHub v1.0 2026-10-17 23:01 UTC; Zenodo 2026-10-17 23:05 UTC). It does not cite this record.
* **TIC 80387959** (corrected 2026-10-21, `prior_search/ERRATUM_PRIOR_DETECTIONS_2026-10-21.md`): TIC 80387959 was previously reported at
  P = 4.1922173881 d in the first-stage RAVEN candidate catalog of Lafarga et al. (2026, MNRAS, doi:10.1093/mnras/stag512). It is absent from
  their vetted and validated subsets. Our work independently recovers this signal, provides additional vetting and freezes predictions for
  a later observational test; we do not claim first detection. In addition, the TESS-SPOC FFI pipeline's Sector 63 single-sector run produced an
  unpromoted threshold-crossing event at the same signal (P = 4.1905 ± 0.0012 d, 869 ± 107 ppm, 2.4 R⊕, MES 7.6), never a TOI or CTOI. The earlier
  statement here ("no human-reported candidate found in the searched sources") is withdrawn: our sweep did not read compressed tables or the
  RAVEN online material.
* **TIC 120444365**: **listed earlier** by an independent, pseudonymous, non-refereed search (github.com/eumemic/exoplanets, tier-C candidate at
  P = 5.148151 d, 856 ppm, first public commit 2026-10-09 03:34 UTC), nine days before our deposit. Ours is an independent rediscovery with
  deeper vetting (pixel localisation, extraction cross-checks, TRICERATOPS NFPP 0.000, external review, Sector 106 pre-registration); priority
  of the listing is theirs.
* **TIC 317134140 (0.5719-d second signal)**: **listed earlier** by the same repository as a tier-A candidate (first commit 2026-10-08 03:14 UTC)
  with Sector 109/110 predictions; again an independent rediscovery on our side.
Statements elsewhere in this record that an object has "no catalog entry" refer to the TOI, CTOI, Exoplanet Archive and SPOC TCE tables and
remain true for those tables; they do not cover survey candidate catalogs such as RAVEN's, and they are not claims of priority. Further earlier
machine detections found on 2026-10-21 (TIC 249813122 and five round-3 objects) are listed in `prior_search/ERRATUM_PRIOR_DETECTIONS_2026-10-21.md`
and `tables/NOTICE_PRIOR_REPORTS_2026-10-21.md`.

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

**Corrections 2026-10-20 (v1.12), after an independent full-repository review** (`reviews_full_repo/REVIEW_full_repo_v1.11.md`):
1. **Masking.** From v1.4 to v1.11 the public prior-search record still carried the withheld object's coordinates and catalogue identifiers. They are removed now. Earlier releases are not rewritten, because their public timestamps are part of the pre-registration record. See the note at the top of `prior_search/PRIOR_SEARCH.md`. *Update (v1.14): the object was then published by author decision (TIC 120517801), and the redaction is lifted.*
2. **Superseded claims** are marked in REPORT.md and corrected here:
   - the TIC 89247735 mass bound and on-target conclusion are withdrawn;
   - its fourth event is a post-hoc recovery that does not exclude a 2P eclipsing binary;
   - the TRICERATOPS values are above, not below, the validation thresholds;
   - Gaia summaries give no mass limit;
   - "blind" tests were retrospective;
   - the S104 clock verification was incorrect;
   - novelty statements are bounded to the searched sources.
3. **Code.** Fixes in `vet.py` (exposure inferred from folded times; per-event holdout depths), geocentric UTC in the remaining producers, and freeze scripts that now refuse to overwrite. Public scripts match the current local sources, including post-production corrections; see Reproduce for historical provenance limits, four missing producers are added, and the TRICERATOPS environment is pinned. No frozen prediction file changed.
4. **Dated clarifications** are appended to `preregistration/TIC80387959/PREREGISTRATION_v2.md` and `preregistration/CORRECTION_UTC_2026-10-19.md`.

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
  - **TIC 53825235 and TIC 408110117:** their v2 files contain no eligible predictions (a generator defect, since fixed), so they carry no valid test. *(2026-10-21: 53825235 v3 now lists S108-S110 with the same ephemeris; S108 and early S109 are retrodictions, the rest predictions.)*
  - **TIC 162304222:** superseded by a v3 freeze for Sector 111. *(2026-10-21: v3 stops at 2026-12-31; v4 adds S112-S114, same ephemeris.)*

**All-sky round 4 and corrections (2026-10-21, v1.15):**
1. **Round 4.** 182 further signals whose next TESS sector is S112-S120 -> 27 on target in the pixel test -> vetting and triage with the round-3 thresholds (2 pass, 2 weak) -> author's cap of three. Predictions frozen for:
   - **TIC 343298093** (P 0.766143 d, ~300 ppm, 1.35 R⊕; test of record S113): independent rediscovery (listed by eumemic/exoplanets, flagged);
   - **TIC 188664994** (P 3.781806 d, ~410 ppm, 1.7 R⊕; test of record S117): no earlier report found in the searched sources (a bounded search); timing-scattered ephemeris, see its amendment;
   - **TIC 151767028** (P 2.210401 d, ~540 ppm, 1.6 R⊕; test of record S112): independent rediscovery (eumemic/ahrazzle; RAVEN first stage).
   None is validated (TRICERATOPS FPP 0.065-0.11). Tables: `tables/round4/`; reviews: `reviews_round4/` (one review, three re-checks).
2. **Scoring.** Per-sector configs, a primary sector that cannot be replaced, and a three-stage binding check are locked in `conformance_round4/` before any of these sectors is observed.
3. **Truncated prediction lists.** Two generator bugs (an old 399-epoch cap and a wrong end date) cut short five records: 115692561 v2 (two S106 transits and all of S107 missing; the S106 test stays the frozen list, omission disclosed), 162304222 v2 and v3, 53825235 v2, 3367979 v2. New versions with identical ephemerides: 162304222 v4, 53825235 v3, 3367979 v4 (ground). `preregistration/ERRATUM_PREDICTION_HORIZON_2026-10-21.md`.
4. **Earlier detections.** A row-aware matcher that also reads compressed tables found earlier machine detections our searches missed: TIC 80387959 (RAVEN first stage; no first-detection claim), 249813122 (RAVEN), 343298093 (eumemic), and five round-3 objects in eumemic's raw or classifier tables. `prior_search/ERRATUM_PRIOR_DETECTIONS_2026-10-21.md`; the DDT proposal for 80387959 is corrected in `corrections/`.


Each `PREREGISTRATION.md` records the ephemeris, the freeze time (UTC) and the SHA-256 of its CSV of predicted transit times.
Each version's public timestamp is its first public commit or archive. Frozen CSV bytes are preserved. Registration annotations are dated; numerical refinements receive new versions. *(Historical note: one generator-description sentence in `preregistration/TIC89247735/PREREGISTRATION_v3.md` was replaced on 2026-10-18; the numerical freeze did not change.)*

## Reproduce
`scripts/` contains the main pipeline stages (Python 3.12; lightkurve, astropy, wotan, batman, emcee, transitleastsquares, tess-point; pinned in `environment/requirements_venv_locked.txt`). Data are public (MAST). Commands are in the header of [REPORT.md](REPORT.md) section 3 and in the `scripts/*.py` docstrings.
**Limits (2026-10-20, after an independent full-repository review):**
- The scripts were written for the authors' workspace and contain absolute local paths, so they do not run unchanged from a clean clone.
- Producers added in v1.12: `prior_grep.py` (prior-search corpus grep), `triceratops_qlp.py` (TRICERATOPS runner), `refit_89247735_raw.py` (raw TIC 89247735 refit) and `pixel_calib_89247735.py` (its pixel calibration).
- The end-to-end injection scoring behind `tables/single_transit_search/injection_recovery_end_to_end.csv` was an ad hoc calculation; its producer was not kept and cannot be recovered. Those numbers can be checked against the table, but not regenerated.
- Current public script copies match the current local copies, except `conformance_v2.1/scripts/qlp_clock_v2.py`, which is kept as hashed in that bundle's manifest; the current `scripts/qlp_clock_v2.py` differs only in its command-line entry point (an optional explicit ephemeris path, v1.15), not in the helper functions the clock tool imports. They include post-production corrections and are not byte-for-byte historical producer snapshots for every older output; historical output provenance and the unrecomputed affected values are identified separately (the git history keeps every earlier public copy). Earlier public copies of `search_pipeline.py`, `tsearch.py`, `prereg_candidate.py`, `qlp_clock_v2.py`, `single_transit_search.py` and `triage.py` had drifted; the older copies remain in the git history.
- Code fixes in v1.12, none of which changes a frozen prediction file:
  - `vet.py` built its fixed-shape ephemeris model with an exposure inferred from folded times, and its shape fits and single-transit timing used one median cadence for mixed-cadence data. The shape, MCMC, global-ephemeris and individual-timing fits now pass per-point exposure estimates derived from the full unfolded series. Tests cover regular mixed cadences and isolated missing samples. These spacing-based estimates remain unreliable for severely thinned or ambiguous segments; original cadence metadata is needed to resolve those cases. The exploratory values produced before this fix (the `ephemeris`, `shape_fit`/`shape_mcmc`, `transit_times` and `blind_tests` entries of the `report.json` files, and the retrospective holdout numbers) have **not** been recomputed and should not be relied on as precise values. The frozen v2/v5 ephemerides come from separate per-sector timing fits with their own cadence-aware models, though they reuse the shape parameters.
  - The per-event holdout depths repeated the stacked value.
  - Several producers wrote mislabelled UTC.
  - The freeze scripts could overwrite a frozen version; they now refuse.
- The TRICERATOPS runs used a separate environment (numpy < 2), pinned in `environment/requirements_triceratops_locked.txt` (triceratops 1.1.0, numpy 1.26.4, scipy 1.13.1). The `requirements_venv.txt` files in the older Zenodo bundles (dataset v1, pre-registration bundles) are empty; use the two lock files here instead.
- `conformance_v2.1/` is the one fully self-contained package (all scripts, configs, outputs and hashes).
- Added in v1.15 (round 4): `pixel_collect.py` (pixel-test classification), `triage_round4.py` (round-3 thresholds, round-4 paths), `prior_match.py` and `test_prior_match.py` (row-aware prior-report matcher and its regression tests), and the freeze command files `freeze_round4.sh`, `freeze_horizon_fix.sh`, `tri_runner_round4.sh`. Changed: `prereg_v2.py` (prediction horizon through 2027, version-aware introduction, `--exclude-sectors`, `--ground-mmag`), `qlp_clock_v2.py` (explicit ephemeris path), `ffi_pixel_test.py` (holdout guard). `conformance_round4/` holds the round-4 configs, lock, validator and tests; it uses the evaluator and clock tool in `conformance_v2.1/`.

## Related Zenodo records (updated 2026-10-21)
Each concept DOI always resolves to the latest version.
* Preprint (research note on TIC 80387959 and TIC 120444365): concept DOI [10.5281/zenodo.23462433](https://doi.org/10.5281/zenodo.23462433). v1.3 = 10.5281/zenodo.23512950; v1.4 (2026-10-21) corrects the prior-report statement (TIC 80387959 was earlier a RAVEN first-stage candidate) and is published alongside this release. Earlier: v1.0 23462434, v1.1 23462857.
* Supporting data and code (checksummed bundle): concept via [10.5281/zenodo.23462438](https://doi.org/10.5281/zenodo.23462438). v1.1 = 10.5281/zenodo.23512928; v1.2 (2026-10-21) adds the same prior-report correction and the corrected preprint, published alongside this release. v1.0 and v1.1 are kept unchanged.
* Pre-registration protocol and frozen evaluator: concept via [10.5281/zenodo.23462442](https://doi.org/10.5281/zenodo.23462442); v1.3 = 10.5281/zenodo.23477866; v1.4 (erratum, governance, conformance procedure v2.1) = 10.5281/zenodo.23508864.
* This repository's releases (concept DOI 10.5281/zenodo.23443244): v1.14 = 10.5281/zenodo.23516414 (v1.15 is archived automatically on release). Historical versions include v1.1 = 23443245, v1.2 = 23445705, v1.3 = 23460915, v1.10 = 23487718, v1.11 = 23508798, v1.12 = 23510604, v1.13 = 23512921.

## Cite
Molina, F. (2026). Multi-year TESS transit search: two planet candidates with pre-registered transit predictions (TIC 89247735, TIC 317134140). Zenodo. https://doi.org/10.5281/zenodo.23443244 (concept DOI; cite the version DOI, e.g. 10.5281/zenodo.23510604 for v1.12, for exact reproducibility) — machine-readable form in [CITATION.cff](CITATION.cff). Code is MIT-licensed; text and tables may be reused with attribution.
