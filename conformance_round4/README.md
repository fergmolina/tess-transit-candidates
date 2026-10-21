# Conformance scoring for the round-4 tests (locked 2026-10-21, before any of these sectors is observed)

Three round-4 registrations (TIC 151767028, 343298093, 188664994; `preregistration/TIC<id>/PREREGISTRATION_v2.md` with their dated
amendments) are scored with the published conformance evaluator v2.1 rc4 (`conformance_v2.1/scripts/prereg_conformance.py`, SHA-256
`a864b07ace8d3220a2d94a60513a488c8a5d87b54f41ebf510ff40ef1755311f`) under its general rules, and the clock tool `conformance_v2.1/scripts/qlp_clock_test_sector.py`. Neither is changed; the seven
Sector 106 tests keep their published code and configs.

## Locked inputs
- `configs/<TIC>_S<sector>.json`: one config per listed sector (151767028 S112-S114, 343298093 S113-S114, 188664994 S117-S119), made by
  `scripts/make_conformance_configs_round4.py`. QLP SAP_FLUX, release of record v01, reference depth and T14 from each registration's
  frozen line, the c0 clock prior (`preregistration/qlp_clock_v2/<TIC>.json`) and its SHA-256, the evaluator SHA-256.
- `configs/ROUND4_LOCK.json` (SHA-256 `d7a20a59cccbf8bf1908ba57cb4bc2447a674b1901359abfd9ed727b32c5ade3`): the SHA-256 of every config and of the prior it names.

## Primary sector (test of record)
S112 for 151767028, S113 for 343298093, S117 for 188664994. The primary stays the test of record whatever its result, including
INSUFFICIENT, CLOCK_UNVERIFIED or INVALID_INPUT, and is never replaced by a later sector. Later listed sectors are scored separately and
reported as further tests, never pooled with the primary.

## Binding (`scripts/validate_round4_inputs.py`)
Every test must pass three stages; a refusal at any stage is reported as the result for that sector.
1. `--stage pre`, before any test-sector data access: the config, prediction CSV, evaluator and c0 prior are the locked bytes, and the
   prior is the canonical file the clock tool reads.
2. `--stage clock`, after the clock tool: the clock record was made from that config and that prior (all hashes present and valid).
3. `--stage result`, after the evaluator: the output was made from that config by the locked evaluator, from the same light curve, and
   was scored with the same clock record. An output without clock provenance counts only as a pre-clock outcome (INVALID_INPUT,
   INSUFFICIENT or CLOCK_UNVERIFIED). If no clock record can be made at all, the validator refuses; that refusal and the evaluator's early
   outcome are reported as they are, and no clock record is ever fabricated.

The clock tool reads the TIME and TIMECORR columns of a TESScut cutout of the test sector; no TESScut flux is used or scored.

## Tests
`scripts/test_round4_configs.py` (200 checks, in-sample files and synthetic records only; log `tests/test_round4_configs_20261021c.log`).

## Limits
No object-specific false-recovery calibration exists for these stars (the conformance calibration was made on the S106 objects). 188664994's
timing uncertainty is a formal, inflated linear-ephemeris error, not a calibrated prediction interval (see its amendment).

## Paths
Paths inside the configs and scripts refer to the authors' working tree. Public copies: `results/vet_allsky/<TIC>/` ->
`preregistration/TIC<TIC>/`; `results/qlp_clock_v2/` -> `preregistration/qlp_clock_v2/`; `configs/conformance/` ->
`conformance_round4/configs/` (S106 configs: `conformance_v2.1/configs/conformance/`).
