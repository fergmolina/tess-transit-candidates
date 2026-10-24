# Conformance scoring for the S107-S121 tests (locked 2026-10-24 00:18 UTC, before any of these sectors' photometry is examined)

Fourteen frozen registrations with TESS tests in Sectors 107-121 are scored with the published conformance evaluator v2.1 rc4
(`conformance_v2.1/scripts/prereg_conformance.py`, SHA-256 `a864b07ace8d3220a2d94a60513a488c8a5d87b54f41ebf510ff40ef1755311f`), general
rules only, and the clock tool `conformance_v2.1/scripts/qlp_clock_test_sector.py`. Neither is changed. The binding check is the
published `conformance_round4/scripts/validate_round4_inputs.py`, run with `--lock configs/LOCK_2026-10-23_S107_S121.json`
(lock SHA-256 `a8731dfcb4a482f633b08fbfe26fbd398670c5616e791c3b3805c602837ef694`). Each registration carries a dated scoring amendment naming its configs and hashes.

## Configs and primary sectors (bold = test of record)
| TIC | Sectors |
|---|---|
| 19119739 | **S111**, S112 |
| 24526743 | **S107** |
| 53825235 | **S109**, S110 |
| 159033763 | **S111** |
| 160330868 | **S107**, S109 |
| 162304222 | **S111**, S112, S113, S114 |
| 196514928 | **S109**, S110, S111, S112 |
| 203381983 | **S115** |
| 258006047 | **S114** |
| 283913390 | **S111** |
| 333661705 | **S111**, S112, S113, S114 |
| 333735955 | **S114** |
| 366047768 | **S121** |
| 467959906 | **S114** |

**Primary-sector rule.**
- The explicit primary sector named in each locked config is the test of record. This holds irrespective of release order, and
  whether or not a QLP v01 product is eventually available.
- If the primary is unavailable, that status is recorded and no later sector is promoted.
- The primary stays the test of record whatever its result, including INSUFFICIENT, CLOCK_UNVERIFIED and INVALID_INPUT.
- Later sectors are scored separately as further tests and are never pooled with it.

**Test sectors.** Only rows whose status starts with "prediction" are scored; both evaluators filter on this. Retrodiction-only sectors
(S108 for 24526743, 53825235 and 160330868) have no config.

**Advance expectation, TIC 160330868.** Under the declared edge rule, neither S107 event is expected to be eligible, and S109 has a
single prediction-status event. The primary is therefore expected INSUFFICIENT. This is a schedule-based expectation, stated in the
registration before any data are examined.

## Reference values
- **Nine objects:** the registration's frozen reference-values line.
- **Five round-2 objects** (258006047, 333735955, 467959906, 203381983, 366047768): their registrations predate that line. They use the
  generator rule of every later freeze, as for TIC 70441745 in S106: report.json sap_depth, and the BLS duration_h, since no shape-fit
  T14 exists. This is a post-freeze dated amendment, not an original frozen number.

## Product and data status
- **Product:** QLP SAP_FLUX, release of record v01. No star is on a published 2-min list for its test sector at the lock (the S107
  manifest and the S109/S110 target lists were checked; S111+ lists were not yet published). If one appears later, QLP stays the
  product of record and SPOC is a secondary readout only. The frozen `prereg_test.py` SAP/DET outputs are secondary readouts.
- **S107:** already observed at the lock.
- **S109:** being observed (partly public through TESScut).
- **S110 and later:** future.
- **Tests on already-observed data:** they are held-out checks of already-observed data, not prospective predictions. The authors
  attest that no target-sector photometry of these stars has been examined.
- **Supporting evidence (bounded):** a recognized-filename inventory of the authors' local caches (`scripts/s0_exposure_inventory.py`,
  including the clock-cutout directory convention) finds nothing after S104 for these stars. It is not proof of non-examination:
  unrecognized names, files elsewhere or deleted, and earlier inspection are not ruled out.

## Clock priors (`preregistration/qlp_clock_v2/<TIC>.json`; bound by hash)
- Two are new: 203381983 (controls S91/S64) and 366047768 (S83/S82).
- TIC 162304222's prior is the documented fallback (+0.033 min; no clean control sector).
- TIC 366047768's S83 control samples include outliers (+0.148, -0.111, -0.355 min) beside a clean group near +0.033 min. The locked
  median (+0.03265 min) is kept.
- The priors are internally consistent and restricted to control sectors 56-98 (excluding 74-79). They are not independently
  re-derived from raw timing columns. The test-sector clock gate still applies.

## Tests (`scripts/test_locked_configs.py`, `tests/`)
- **Result:** 655/655 binding and refusal checks on this lock; the same file reproduces the round-4 suite, 200/200.
- **Method:** since 2026-10-23 the tests use an artificial byte fixture, not a real light curve.
- **What they cover:** config, prior, CSV and evaluator binding; refusals; stale-output protection.
- **What they do not cover:** valid FITS headers, pixel timing alignment, clock corrections and scoring.
- **Calibration:** the conformance false-recovery calibration was made on the S106 objects only. No object-specific or family-wise
  rate is established for these 14 objects.

Review: `reviews_s107_s121/` ("lock sound after the listed changes"; the changes are DECISIONS 168).
