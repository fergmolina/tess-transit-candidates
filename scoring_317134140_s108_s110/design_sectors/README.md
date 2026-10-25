> Public copy (2026-10-25 (v1.18.1)): the line about the S111 evaluator diff was removed, because that material is not in this release; calibration files are in `../calibration/`. No other change.

# TIC 317134140 scorer: design-sector (training) outputs and checks

All runs below are `--insample-check` mechanics checks on the four TRAINING sectors (S6, S87, S98, S107), where the signal is assumed
present. They are not independent tests and never outcomes. No S108-S110 photometry of this star has been examined.

| Files | Scorer SHA-256 (prefix) | Scorer state | What changed |
|---|---|---|---|
| `insample_S*.json` | `584f9bf6` | v1.0 | first draft; logged before any change (DECISIONS 173) |
| `insample_v1.1_S*.json` | `4c53a94b` | v1.1 | TOI mask widened 1.5x -> 2.5x after detrending (DECISIONS 174; motivation later disproven) |
| `insample_v1.1final_S*.json` | `4a188827` | v1.1 | light-curve hash recorded first; no logic change (DECISIONS 175) |
| `insample_v1.2_S*.json` | `2e011c13` | v1.2 | TOI removed BEFORE detrending, 1.5x window, as in the registration prep() (DECISIONS 176) |
| `insample_v1.2final_S*.json` | `ce29f0fe` | v1.2 | version/software recorded; docstring; no logic change (DECISIONS 177) |
| `insample_v1.2final2_S98.json` | `acfd7d34` | v1.2 | wotan version from package metadata; S98 only (the SHA reviewed in REVIEW_GAP3_configs.md) |
| `insample_v1.3_S*.json` | `cd21f1fc` | v1.3 (first lock, superseded) | review G1/G4/G5 fixes (DECISIONS 179). The depth-compatibility boundaries, TOI mask and BLS search are unchanged. v1.3 tightens input and noise eligibility: at least 100 usable random shifts instead of 11, positive errors, and a strictly positive finite sigma. These guards did not change the four saved training outcomes. |
| `insample_v1.3b_S*.json` | `f3f55c0d` | **v1.3 = locked** | docstring wording only (re-check R4: sigma predicate; release-of-record wording) (DECISIONS 181) |

The outcomes are identical in every version: S6 PARTIAL, S87 INCONCLUSIVE, S98 PASS, S107 PARTIAL. The v1.2, v1.2final, v1.3 and v1.3b
depths are identical; v1.0 and v1.1 differ slightly (see DECISIONS 174, 176).

Other files:
- `fixture_bias_check_v1.3.json`: made by `scripts/fixture_bias_check_317134140.py`, with seed-level outputs at the preceding v1.3 SHA
  `cd21f1fc...`, whose executable logic is identical to the current docstring revision (`f3f55c0d...`). These
  are idealized white-noise fixtures. No bias was detected, but this does not establish unbiased real-data depths or calibrated error
  rates.
- `selection_demo_S107/`: a worked example of the release-of-record records (`scripts/spoc_selection.py`) on the in-sample S107
  product, made with the selector before its derive() refactor. The record re-derives identically with the current
  code. The MAST query listed exactly one SPOC 2-min light curve. The downloaded file is byte-identical to the S107 file used in
  training.
- `superseded_scorers/prereg_spoc_317134140_v1.2.py`: a byte-exact copy of the reviewed v1.2 scorer (SHA-256 `acfd7d34...`), for diffing.

## Calibration (2026-10-25; DECISIONS 185-188)
- `../calibration/calibration_v1.3.json`: raw trials from `scripts/calibrate_317134140_scorer.py` (the locked scorer on the training sectors, real
  signal divided out; injections at 130/185/240 ppm, noise-only trials). The script's code is unchanged from the version that ran
  (SHA-256 `63738417...`); its docstring was corrected on 2026-10-25.
- `calibration_diagnostics_v1.3.md` / `.json`: the DESCRIPTIVE diagnostics (`scripts/calibration_diagnostics_317134140.py`). These are
  conditional frequencies; the zero noise-only PASS count is a structural zero.
- `interpretation_table_v1.3.md` / `.json`: WITHDRAWN before publication (DECISIONS 187). The combined likelihood-ratio interpretation
  it encodes is not supported. Kept for history only. Both files carry their own WITHDRAWN label and original SHA-256 (DECISIONS 189).
- `calibrate_317134140_scorer_as_run.py`: byte-exact source of the calibration script as it ran (SHA-256 `63738417...`); the current
  script differs only in its docstring.
