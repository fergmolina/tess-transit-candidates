# TIC 317134140 scorer v1.3: calibration on the training sectors (descriptive; 2026-10-25 (v1.18.1))

**What it is:** the locked v1.3 scorer run on the four TRAINING sectors (S6, S87, S98, S107):
- with the real signal divided out;
- on registration-shape signals injected at random periods of 0.53-0.70 d and depths of 130, 185 and 240 ppm;
- and on noise-only trials.

**What it is not:** these are conditional frequencies in three selected training noise realizations, **not** calibrated
probabilities for S108-S110.
- **Structural zero:** the noise-only BLS peaks cannot satisfy PASS anywhere in the allowed trial-period range, so the zero PASS count
  says nothing about a future-sector false-PASS rate.
- **No combined conclusion:** none is adopted. The frozen per-sector outcomes remain the outcomes of record, and each will be
  reported with its conditional frequencies at all three depths.

**Files:**
- `calibration_diagnostics_v1.3.md` / `.json`: the diagnostics (made by `scripts/calibration_diagnostics_317134140.py`).
- `calibration_v1.3.json`: every trial row (made by `scripts/calibrate_317134140_scorer.py`).
- `calibrate_317134140_scorer_as_run.py`: the byte-exact source as it ran (SHA-256 `63738417...`); the current script differs only in
  its corrected docstring.
- `calibrate_317134140_20261025.log`: the run log.
- `withdrawn/`: the combined-LR draft, withdrawn before publication.

**Review:** `../../reviews_317134140/REVIEW_317134140_calibration_plan.md` and `RECHECK_317134140_calibration.md`.

Nothing in the v1.18 lock, configs or scorer changed.
