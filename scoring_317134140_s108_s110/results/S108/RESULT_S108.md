# TIC 317134140, Sector 108: outcome PARTIAL (scored 2026-11-13)

This is the first of three per-sector results of the test locked in v1.18 (`../../README.md`). Sectors 109 and 110 are scored
separately when their SPOC 2-min light curves are listed. Results are never pooled and never replaced.

## Outcome

**PARTIAL**: clause A is met, clause B is not.

| Clause | Result | Measured |
|---|---|---|
| A, stacked depth at the frozen times | `A_CONSISTENT` | depth 206.3 ppm, random-phase sigma 55.0 ppm (depth/sigma 3.75); nominal 1.96-sigma interval 98.6 to 314.1 ppm, which overlaps the frozen band 145 to 225 ppm |
| B, blind BLS of the sector | `B_NOT_TOP3` | top three peaks 1.14675 d (SDE 7.07), 8.02217 d (SDE 6.25), 0.93024 d (SDE 5.70); none within 0.1 % of 0.5718634 d |

- Events: 28 of the 48 predicted events were eligible (the minimum is 10). 200 random shifts were usable.
- Cadences: 11,862 after preprocessing; 363 removed by the TOI-2514.01 mask.
- Aliases: the scorer reports none (`alias_hits` is empty). The first peak is 0.26 % from twice the period (1.1437268 d), outside
  the locked 0.1 % tolerance. Aliases do not count toward clause B in any case.

## What PARTIAL means

- Only PASS meets both frozen clauses. **PARTIAL is not a confirmation.**
- The frozen text asked for two things: a stacked depth of about 185 +- 40 ppm at the predicted phase, and 0.5719 d near the top of
  a blind BLS. In Sector 108 the first holds under the locked measurement and the second does not.
- The 1.96-sigma interval is nominal. The random-phase sigma is an empirical spread, and its coverage under real systematics is not
  established.
- The advance expectation of the lock was "mostly PARTIAL expected under a real signal". That was a conditional extrapolation from
  four training sectors, not a calibrated probability. A PARTIAL outcome is consistent with that qualitative expectation; one
  outcome does not establish its frequency, calibrate its predictive accuracy, or demonstrate a real signal.
- The lock allows PARTIAL, INCONCLUSIVE, INSUFFICIENT and UNAVAILABLE outcomes and has no combined decision rule. Sectors 109 and
  110 remain separate prospective tests; their outcomes may also be inconclusive and do not by themselves identify the host or
  validate a planet.
- A dip at the predicted phase would not distinguish a planetary transit from a blended eclipsing binary.

## Conditional frequencies from the v1.18.1 calibration

The registration's calibration note of 2026-10-25 says each test-sector outcome is reported with these. They are the frequencies of
the outcome PARTIAL in the training-sector trials (`../../calibration/calibration_diagnostics_v1.3.md`; pooled S6 + S87 + S107):

| Trial type | PARTIAL |
|---|---:|
| Injected signal, 130 ppm | 82/150 (55 %) |
| Injected signal, 185 ppm | 175/300 (58 %) |
| Injected signal, 240 ppm | 52/150 (35 %) |
| Noise only | 107/6000 (2 %) |

These describe three selected training noise realizations. They are **not** calibrated probabilities for Sector 108, and no
likelihood ratio or combined conclusion is drawn from them. The trial periods avoided the band that contains the candidate period,
and each training sector contributes one noise realization. All limits listed in the calibration diagnostics apply.

## Sequence and records

| Time (UTC) | Step | Record |
|---|---|---|
| 2026-11-12 04:53:49 | selection check: `NONE` | `../../../monitoring/selection_records_317134140/S108/sel_20261112T045349Z.json` |
| 2026-11-13 19:54:28 | selection check: `SELECTED`, exactly one candidate | `../../../monitoring/selection_records_317134140/S108/sel_20261113T195427Z.json` |
| 2026-11-13 19:58:47 | download of exactly the selected file | `acquisition_S108.json` |
| 2026-11-13 19:58:52 | locked scorer v1.3, one run | `result_S108.json` |
| 2026-11-13 19:58:54 | validator, stage `result`: `BOUND` | `score_317134140_S108_20261113.log` |

- **File of record:** `tess2026250081459-s0108-0000000317134140-0310-s_lc.fits`, 2,001,600 bytes, SHA-256
  `cea2619b6228e770064ed39176ad446c02320311dbd3751e15cdc0876b4331a0`. Header: PROCVER `spoc-6.1.1-20261030`, DATA_REL 146,
  DATE 2026-11-07, camera 3, CCD 4. The file is public at MAST and is not copied here.
- **Lock:** `../../configs/LOCK_2026-10-24_317134140.json` (SHA-256 `58df364513d9d2bd...`); config `317134140_spoc_S108.json`;
  scorer SHA-256 `f3f55c0d74733f8a...`. Stages `pre` and `selection` were `BOUND` before the download.
- **Checks made before the download:** the lock tests gave 196/196 (`test_317134140_lock_20261113_precheck.log`). The four
  training sectors, re-scored on the same machine, were identical field for field to `../../design_sectors/insample_v1.3b_S*.json`.
- **Conduct (author-reported):** The author reports recording the run plan before download and performing one acquisition and one locked scoring run. The
  retained records are consistent with that account; they do not independently timestamp insertion of the plan or exclude
  unrecorded activity. Apart from byte-integrity checks and validation, no additional photometric analysis is reported.
  The plan (DECISIONS 225) included the rule that any exception, `INVALID_INPUT` or `REFUSED` stops the work with no re-run; the
  scoring log shows none.
- **Trigger:** the first `SELECTED` check was made after a daily metadata monitor reported that the Sector 108 light-curve
  manifest had appeared. The check before it was 39 hours earlier.

## Limits

- **Release of record:** it is the version listed at the first recorded `SELECTED` check. An earlier, replaced delivery cannot be
  excluded. The monitoring gap disclosed in `../../../corrections/CORRECTION_v1.19.1_2026-11-10.md` (C1) stays on the record.
- **Eligible events:** why 20 of the 48 predicted events were not eligible has not been examined. The scorer records counts only.
- **No additional analysis reported:** the file was read by the locked scorer, by the validator and by byte-integrity (hash)
  checks of the assembler and the reviewer. No figure, fold, centroid test or other periodogram of Sector 108 is reported. Any
  later look is exploratory and cannot change this outcome.
- **First availability:** the retained query results changed from `NONE` to `SELECTED` between the checks of 2026-11-12 and
  2026-11-13; they do not establish the first public availability time. Neither the header DATE nor the archive's release field
  (`t_obs_release` 61355.0) establishes it.
- **Scope of the data statement:** for Sector 108 of this star, only the selected `s_lc.fits` was downloaded; the target-pixel
  file was not. No Sector 109 or 110 data of this star have been downloaded or opened; that is the authors' attestation.
- **Review:** External review checked the recorded outcome, provenance bindings and release bytes; it did not independently rerun
  the S108 photometry analysis (`../../../reviews_v1_20/`). The depth, sigma and BLS peaks are therefore verified as saved output,
  not recomputed from the file. The reviewer recommends a later, declared computational reproduction; none has been made or
  decided.

## To reproduce

Download the file of record from MAST (`mast:TESS/product/tess2026250081459-s0108-0000000317134140-0310-s_lc.fits`), compare its
SHA-256, then:

```
python -I scripts/prereg_spoc_317134140.py --config configs/317134140_spoc_S108.json --lc <file> --out result.json
python scripts/validate_nonclock_inputs.py --lock configs/LOCK_2026-10-24_317134140.json --stage result \
    --config configs/317134140_spoc_S108.json --selection <selection record> --acquisition acquisition_S108.json \
    --lc <file> --result result.json
```

Exact locked reproduction requires the original absolute-path layout and unmodified scorer, helpers, config and prediction CSV. Run
these commands from `scoring_317134140_s108_s110/`, supplying absolute paths to the saved selection/acquisition records and an output
path that does not exist. Editing embedded paths changes the recorded hashes and will not pass the published binding checks. A
portable adaptation must be documented separately as a reproduction experiment, not substituted for the outcome of record.
Software as run: Python
3.12.15, numpy 2.5.4, scipy 1.18.1, astropy 8.0.2, wotan 2.0.

Log entries: DECISIONS 224-229.
