# Scoring for the TIC 317134140 S108-S110 test (locked 2026-10-24 23:40:31 UTC, before any S108-S110 photometry of this star is examined)

The frozen registration (`preregistration/TIC317134140/PREREGISTRATION.md`, frozen 2026-10-17) states a qualitative test: the stacked
depth at the predicted phase in each of S108, S109 and S110 should be about 185 +- 40 ppm, and a blind BLS of each sector should rank
0.5719 d near the top. This bundle is a dated operationalization of that test, declared before the data. The prediction CSV is
unchanged (SHA-256 `63e98fc87ebc6ce65198e066028d7f9ea58d24b51b35771d9fc551c41f59deb3`).

## What is locked
- **Scorer** `scripts/prereg_spoc_317134140.py` v1.3 (SHA-256 `f3f55c0d74733f8aa4ee6264b99c29c547990d885d5cfdd2c29c43c47baa1613`), on SPOC 2-min PDCSAP_FLUX. It reuses the
  published `scripts/tsearch.py` and `scripts/search_pipeline.py` unchanged.
  - **Clause A (stacked depth):** compatibility with the frozen depth plus positive-depth evidence, with a nominal 1.96-sigma interval
    whose coverage under real systematics is not established.
  - **Clause B (blind BLS):** 0.5719 d within the top 3 peaks of the original per-sector search, to 0.1 %.
  - **Ordered outcome:** INSUFFICIENT, then FAIL (A_LOW, whatever B says), then PASS, PARTIAL, INCONCLUSIVE. Only PASS meets both
    frozen clauses. FAIL is adverse evidence under this measurement model, not proof that the signal is absent.
  - **Post-freeze choices:** every number not in the frozen text is listed as such in the scorer docstring and the registration.
- **Release of record** `scripts/spoc_selection.py`:
  - `select` is metadata-only: it saves the MAST product list and its hash. Exactly one SPOC 2-min `s_lc.fits` is required;
    otherwise the status is NONE, AMBIGUOUS or INCOMPLETE and nothing is chosen.
  - `acquire` downloads exactly the selected file.
  - The selected version is the eligible version listed at the first recorded check. An earlier, replaced delivery cannot be
    excluded.
- **Binding** `scripts/validate_nonclock_inputs.py --lock configs/LOCK_2026-10-24_317134140.json` (lock SHA-256 `58df364513d9d2bd3f2d0c7474d069b55737420614b10eb631cf82e4eba0db41`):
  - stage `pre`: before any data;
  - stage `selection`: recomputes the response hash, re-derives the selection from the saved rows, and checks parsed UTC
    timestamps;
  - stage `result`: binds selection, acquisition, light curve and output.
- **Scope:** each sector is scored and reported separately, never pooled and never replaced. A pooled depth is a secondary readout
  only.

## Cutoffs and monitoring
| Sector | Sector end (UTC) | Inclusive cutoff (end + 120 d) | Status at the lock |
|---|---|---|---|
| S108 | 2026-10-04 20:30:00 | 2027-02-01T20:30:00Z | observed 2026-09-07 to 10-05 |
| S109 | 2026-10-31 18:55:00 | 2027-02-28T18:55:00Z | being observed 2026-10-05 to 10-31 |
| S110 | 2026-11-26 04:15:00 | 2027-03-26T04:15:00Z | future sector (2026-10-31 to 11-26) |

- **Before the cutoff:** a SELECTED record made at or before the cutoff permits scoring at any later time.
- **No selection by the cutoff:** the sector is UNAVAILABLE. No other product replaces it, and a later listing is a secondary readout
  only. UNAVAILABLE means no SELECTED record was made by the cutoff, not that no archive product ever existed.
- **Monitoring:** prospective, starting at the later of the lock time and the sector end. Checks are made at least weekly until the
  first SELECTED record, plus a final check within 24 h before the cutoff, and every record is kept. It is periodic, not continuous.
  S108 ended before the lock; no S108 selection record was made before it.

## Advance expectation
On the four training sectors (S6, S87, S98, S107), where the signal is assumed present, the locked procedure gives 1 PASS, 2 PARTIAL
and 1 INCONCLUSIVE. Under a real signal the expected S108-S110 outcomes are therefore mostly PARTIAL. This is a conditional
extrapolation, not a calibrated probability. See `design_sectors/README.md` for the version history: outcomes are identical in every
version, the v1.0 results were logged before any change, and a byte-exact copy of the reviewed v1.2 scorer is included.

## Tests and limits
- **Tests:** `scripts/test_317134140_lock.py` gives 196/196 (`tests/`) on ARTIFICIAL fixtures and artificial MAST responses. They
  cover the outcome truth table, malformed inputs, INSUFFICIENT paths, and selection/acquisition binding, substitution, cutoff and
  observation-id refusals.
- **Fixture bias check** (`scripts/fixture_bias_check_317134140.py`): no bias was detected in a small idealized white-noise check.
  It does not establish unbiased real-data depths or calibrated error rates.
- **Not covered:** real SPOC systematics and the power of the tests on real data.

Review chain: `reviews_317134140/`. The first review covered an earlier combined draft; its findings were resolved over three
re-checks, the last of which recommends "publish as v1.18". Superseded drafts were never published and are not included (DECISIONS
176-182). The S111 tests of TIC 80387959 and 120517801 are not in this release (v1.19).
