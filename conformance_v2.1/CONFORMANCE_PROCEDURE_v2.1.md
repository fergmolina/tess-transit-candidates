> **Published 2026-10-20 as conformance-v2.1** (evaluator `scripts/prereg_conformance.py`, SHA-256 `a864b07ace8d3220a2d94a60513a488c8a5d87b54f41ebf510ff40ef1755311f`; internal label rc4), in release
> v1.11 of github.com/fergmolina/tess-transit-candidates, before any Sector 106 photometry of a test target was examined. External
> review: REVIEW_conformance_v21.md and re-checks _rc2, _rc3, _rc4 (rc4 verdict: publish as declared procedure). It replaces the
> v2.0 draft, which was withdrawn before publication. Governance and departures: GOVERNANCE_S106_TESTS_2026-10-20.md. Design log:
> DECISIONS.md items 70-96. Paths below are relative to the repository folder `conformance_v2.1/`. The locked configs record the authors'
> absolute local paths (section 7); their prediction CSVs are the hashed files under `preregistration/TIC<id>/`.

# Conformance procedure for the seven Sector 106 tests

## 1. Why a second evaluator
Independent reviews showed that the frozen evaluator `scripts/prereg_test.py` (SHA-256 `630815cc…`):
- averages timing offsets, so opposite offsets cancel;
- never measures duration;
- can lock onto a brightening;
- can return EXCLUDED without full coverage;
- has an undeclared fifth outcome.

It stays frozen, and its literal output is reported for every test in two locked variants:
- the same source FITS and SAP_FLUX column (it applies its own preprocessing and no clock correction);
- the protocol's DET_FLUX column.

The outcome of record comes from the conformance procedure below. It is a newly amended operational test, not a literal restoration of every original protocol clause.

## 2. Code and locked inputs
Full SHA-256 values of every file in this folder: MANIFEST.md (results/conformance_v21/README.md is the review-time manifest and uses the draft file names).

| File | Role |
|---|---|
| `scripts/prereg_conformance.py` | evaluator v2.1; the docstring is the authoritative procedure |
| `scripts/qlp_clock_test_sector.py` + `scripts/qlp_clock_v2.py` | per-event QLP clock record (S99+ products), using integer cadence alignment against a TESScut cutout. **For S106 this downloads a TESScut cutout of the test target (S106 pixel data).** It runs only with `--declared-test`, at test time. |
| `results/qlp_clock_v2/<TIC>.json` | clock constants c0 from control sectors ≤ 98. SHA-256 prefixes: 183374279 77f91265, 120444365 8af71b26, 70441745 1e6cd1b2, 206620592 3fe2b7c9, 122522485 97a82f4f, 253931796 c07a319b, 115692561 81d285ee. |
| `scripts/make_conformance_configs.py`, `configs/conformance/<TIC>_S106.json` | locked per-test settings: prediction CSV and hash, product, release of record (v01), reference depth/T14 and their provenance, evaluator SHA (enforced), both frozen-evaluator commands, edge rule, strict epochs (183374279) |
| `scripts/test_conformance.py` | logic tests at about 10× the operating SNR; they check each outcome route, not performance |
| `scripts/test_conformance_inputs.py` | 35 input, refusal and regression cases; each case writes a fresh result, a crash fails the case, and the result must match the requested inputs |
| `scripts/conformance_edge_profile.py` | edge profiles (design sectors) |
| `scripts/conformance_discriminating_test.py`, `scripts/conformance_disc_analyse.py` | operating-SNR tests on design sectors |
| `scripts/conformance_calibrate_holdout.py`, `scripts/conformance_calib_report.py`, `scripts/conformance_summarise.py` | holdout calibration and reports |
| `scripts/conformance_s106_forecast.py` | S106 eligibility and noise forecast, made without S106 photometry |
| `results/conformance_v21/requirements_venv_locked.txt` | pinned environment (Python 3.12.9; numpy 2.5.4, scipy 1.18.1, pandas 2.3.3, astropy 8.0.2, wotan 2.0) |

**Evaluator versions behind each result set** (design results were not all run on the final file):

| Result set | Evaluator SHA |
|---|---|
| Discriminating test, 1,400 runs | `c6fdfa41…` (481 runs) and `4858c3b6…` (919 runs; a readout-only edit) |
| EXCLUDED re-run, 160-run on-time, random-sign (1,240 runs) | `17c6ca71…` |
| rc1 holdout calibration (1,080 runs) | `59050267…` |
| rc2 holdout re-calibration (1,080 runs) | `000b0dfb…` |
| rc3 holdout calibration (1,080 runs) | `579d50ac…` |
| rc4 holdout calibration (1,080 runs; final) | `a864b07a…` (the SHA locked in the configs) |

The outcome logic of RECOVERED, INCONSISTENT and the split is unchanged from `17c6ca71…` onward. rc2 changed EXCLUDED (every event measured at every gate offset), added overrides and refusals, and changed nothing else (DECISIONS 86). rc3 and rc4 changed the final strict-epoch override, input handling (an all-flagged product now returns INSUFFICIENT instead of crashing; TIMEUNIT/TIMEREF required) and wording. The joint RECOVERED/INCONSISTENT/split/EXCLUDED calculations are unchanged (DECISIONS 88, 91).

## 3. Procedure (summary; the docstring governs)
1. **Validate the inputs:**
   - prediction-CSV hash, and the evaluator SHA against the config;
   - config and prediction invariants (positive finite reference values; finite integer, unique epochs; unique finite times; finite sigma_min ≥ 0);
   - product: QLP HLSP file-name pattern, **release of record v01** (later releases are reported separately, never as the outcome of record), `ORIGIN` MIT/QLP, `TIMESYS` TDB, `BJDREFI` 2457000, `TIMEUNIT` d and `TIMEREF` SOLARSYSTEM (both required), `BJDREFF` absent or numeric 0;
   - header `SECTOR`/`TICID` match the config; no duplicate cadence times; at least one predicted event.
2. **Clock:** for QLP sectors ≥ 99 a clock record must match the TIC, sector, light-curve SHA-256, prediction-CSV SHA-256 and event list.
   - If it doesn't, the outcome is CLOCK_UNVERIFIED.
   - **A record carrying the whole-cadence warning also refuses scoring:** a time-label error and a row misregistration cannot be told apart, so the test is not scored.
   - Corrections shift the observations; predictions are never shifted.
3. **Edge rule:** drop cadences within 1.5 d after the data start or any resume following a gap > 0.5 d, and within 0.5 d before any gap > 0.1 d or the data end. If fewer than 10 usable cadences remain (this includes an all-flagged product), the outcome is INSUFFICIENT. That decision is made before the clock gate, so no clock record is checked in that case.
4. **Preprocess:** keep QUALITY = 0; biweight detrend (0.7-d window), with predicted transits masked.
5. **Eligibility:** ≥ 90 % of the in-transit interval sampled, plus baselines on both sides.
6. **Joint box search:** common offset (±0.3 d) and duration (0.5–2.0× reference). A box is VALID only if:
   - it is a dip;
   - the per-event depths are consistent (χ² p ≥ 0.01);
   - ≥ 2 events are positive at 1σ.
7. **Compatible signal:** a band-duration (0.7–1.3×) fit with SNR ≥ 5 and depth 0.5–1.5× reference, and SNR²(band) ≥ SNR²(any duration) − 4.
   - The last condition is an exact score rule on maximised nominal SNRs.
   - It is not a calibrated 2σ duration interval.
8. **Outcomes, in order:**
   1. **INSUFFICIENT:** fewer than 2 eligible events.
   2. **RECOVERED:** a compatible signal with offset within max(3σ, 30 min), plus the timing-split check (each epoch-parity half's best offset within the gate).
   3. **INCONSISTENT:** the best compatible VALID fit within ±0.3 d has SNR ≥ 7 and lies more than max(gate, 30 min) away.
   4. **EXCLUDED:** all three of the following hold.
      - (a) Depth + 3σ < 0.3× reference at every offset within the gate, with every eligible event measured at every such offset.
      - (b) Per-event consistency at the prediction.
      - (c) No VALID fit with SNR ≥ 5 and depth ≥ 0.5× reference anywhere within ±0.3 d.
   5. **AMBIGUOUS:** everything else.
9. **Object-specific override (TIC 183374279):** if epoch 245 or 246 is not eligible, or has a flagged cadence, a non-finite flux, a missing cadence (spacing > 1.5 cadences), or an uncovered window edge (> 1.05 cadences) within tc ± T14/2 (clock-corrected), the outcome of record is INSUFFICIENT. The check covers the nominal window only, not the whole timing gate. The procedure's own outcome is kept as `outcome_before_override`.
10. **Secondary readouts** (never the outcome of record):
    - the joint-only outcome;
    - the min(3σ, 30 min) reading;
    - the per-event min() reading;
    - odd/even depths;
    - EXCLUDED diagnostics, including the number of events measured at each gate offset;
    - both frozen-evaluator outputs.

**What the outcomes mean:**
- RECOVERED denotes compatibility with the specified common-box and parity-split scoring rule. It does not demonstrate that every event individually meets the original timing and duration limits, exclude a half-period eclipsing binary, or identify the companion.
- INCONSISTENT requires a coherent displaced common-box signal at the higher SNR threshold; its absence is not evidence that the ephemeris is correct.
- INSUFFICIENT and AMBIGUOUS are not confirmations.

## 4. Data partition and earlier uses
Only 200-s sectors are used.
- **Design sectors:**
  - 183374279 and 120444365: S96, S105;
  - 70441745, 206620592, 253931796, 115692561: S96;
  - 122522485: S97.
- **Holdout sectors (calibration):**
  - 183374279 and 120444365: S69, S103;
  - 70441745, 206620592, 253931796: S68;
  - 122522485: S105;
  - 115692561: S69.

They were held out from the specified v2.1 performance tuning. They are not unseen data:
- All of them are in-sample for the ephemerides.
- 120444365 S69 had evaluator and timing fits during the v2.0 development.
- The S106 forecast used QUALITY/timing metadata (not photometric residuals) of S68/S69/S105.
- The clock-tool validation reproduced published corrections, including S103 (183374279, 120444365) and S105 (122522485), from timestamps only.
- S68 set 70441745's clock constant.
- The rc1 calibration was inspected before the rc2 fixes, so the rc2, rc3 and rc4 re-calibrations on the same sectors are already-seen development evidence.

## 5. Evidence at the operating signal-to-noise
**Edge rule:**
- We selected pooled trims of 1.5 d after long-gap resumes and 0.5 d before gaps exceeding 0.1 d.
- The profiles show large edge excursions: pooled fraction of |z| > 3 of 0.31, 0.25, 0.07, 0.09, 0.09, 0.06 in the 0.25-d bins after a resume; z reaches +26 in the first 0.1 d for TIC 183374279.
- These cuts do not satisfy the literal requirement that every later 0.25-d bin have an exceedance fraction of at most 0.03. Examples:
  - 0.031 at 1.75–2.0 d after a resume;
  - 0.043, 0.035, 0.051 in the 0.5–1.25 d bins before gaps > 0.1 d.
- They are a design choice informed by the profiles and coverage trade-offs. Full profiles: results/conformance_v21/edge_profile_*.
- A per-target alternative was computed and rejected (DECISIONS 80).

**Discriminating tests:** design sectors, real noise, locked settings, 40 realisations each. RECOVERED counts with the split check:

| | 70441745 | 120444365 | 122522485 | 183374279 | 206620592 | 253931796 | 115692561 |
|---|---|---|---|---|---|---|---|
| on-time reference transit | 38/40 | 28/40 (103/160) | 28/40 | 37/40 (137/160) | 21/40 | 39/40 | 0/40 |
| null (no transit) | 0/40 | 0/40 | 0/40 | 0/40 | 0/40 | 0/40 | 0/40 |
| alternating ±(gate + 20 min) | 0/40 | 0/40 | 0/40 | 1/40 | 0/40 | 0/40 | 0/40 |
| random-sign ±(gate + 20 min) | – | 1/40 | – | 5/40 | – | – | – |
| 0.6 × T14 | 19/40 | 13/40 | 10/40 | 20/40 | 5/40 | 1/40 | 0/40 |
| 1.5 × T14 | 0/40 | 8/40 | 14/40 | 4/40 | 15/40 | 1/40 | 2/40 |

  - **Choice of the split check:**
    - The 40-realisation design-selection rule in decision 77 was not met: TIC 120444365 lost 15 percentage points of on-time recovery (34 → 28 of 40).
    - We nevertheless chose the timing split after inspecting the design results. It reduces alternating-offset recoveries (183374279: 12/40 → 1/40), and the literal per-event alternative had poor power (on-time 29, 10, 0, 26, 0, 40, 0 of 40).
    - Expanding the same phase sequence to 160 realisations estimated a 10-point loss. That was a post-result refinement, not a new independent or prespecified acceptance test.
    - The selected procedure is now fixed for calibration and for the S106 tests.
  - **The split is a partial safeguard.** The alternating injection and the split both use epoch parity, so that case is matched by construction. The external reviewer's paired pattern (+, +, −, all outside the gate; 183374279, 10 runs) was RECOVERED 3/10.
  - **Duration** 0.6× or 1.5× T14 cannot be distinguished from the 0.7–1.3× band at these signal-to-noise levels.
  - **Negative outcomes in the design runs:** one of the 160 on-time 183374279 injections returned INCONSISTENT. Complete outcome tables, not only RECOVERED counts: results/conformance_v21/discriminating_*.
  - **EXCLUDED** (rule of `17c6ca71…`): displaced real transits read EXCLUDED 0/280; nulls read EXCLUDED only for 253931796 (39/40) and 183374279 (1/40).

**Holdout calibration (rc4, final):** 1,080 runs, all on the rc4 evaluator locked in the configs. Run for run, the outcomes are identical to the rc2 and rc3 runs, as expected since the joint scoring calculations are unchanged. Holdout sectors only. Real transits handled as in DECISIONS 86 (R8). Full table: `results/conformance_v21/holdout_calibration_rc4_report.md`.

| test (holdout sectors) | null → RECOVERED | null → EXCLUDED | on-time → RECOVERED | displaced (+gate + 60 min) → INCONSISTENT | not scored |
|---|---|---|---|---|---|
| 70441745 (S68) | 0/40 | 0/40 | 40/40 | 33/40 | – |
| 120444365 (S69, S103) | 0/71 | 1/71 | 30/71 (S69 3/35, S103 27/36) | 12/71 | 27 INSUFFICIENT |
| 183374279 (S69, S103) | 0/80 | 6/80 | 46/80 (S69 9/40, S103 37/40) | 26/80 | – |
| 206620592 (S68) | 0/40 | 0/40 | 11/40 | 0/40 | – |
| 122522485 (S105) | 0/35 | 0/35 | 0/35 | 0/35 | 15 INSUFFICIENT |
| 253931796 (S68) | 0/40 | 39/40 | 40/40 | 40/40 | – |
| 115692561 (S69) | 0/40 | 0/40 | 0/40 | 0/40 | – |

  - No null was falsely RECOVERED: 0 of 346 scored.
  - No clock warning fired in any of the 360 sector ≥ 99 runs.
  - The rc1 calibration gave similar figures (DECISIONS 84).

All rates are counts of a conditional simulation:
- Realisations share one light curve per sector and are not independent.
- Sectors differ strongly (120444365 S69 3/35 vs S103 27/36; 183374279 S69 9/40 vs S103 37/40).
- **The family-wise false-RECOVERED rate across the seven S106 tests is not calibrated by this experiment.** The empirical frequency of false RECOVERED in these simulations is zero.

## 6. Stated in advance, before any S106 photometry
**Eligibility forecast** (no S106 photometry; S106 gaps modelled with seven in-sample QLP gap templates mapped onto the S106 downlink schedule):

| Test | Eligible events (min / median / max) | Templates with < 2 eligible | Median expected joint SNR |
|---|---|---|---|
| 70441745 | 1 / 2 / 2 | 1/7 | 10.7 |
| 120444365 | 2 / 2 / 3 | 0/7 | 4.8 |
| 183374279 | 1 / 1 / 2 | 5/7 | 4.2 |
| 206620592 | 13 / 16 / 20 | 0/7 | 5.5 |
| 122522485 | 6 / 7 / 10 | 0/7 | 3.5 |
| 115692561 | 16 / 19 / 23 | 0/7 | 2.8 |
| 253931796 | 0 / 1 / 1 | 7/7 | – |

Limits of the forecast:
- Template extra gaps are taken only above 0.5 d.
- Schedule times omit the target light-travel term.
- The 183374279 override and the split veto are not modelled.
- Template fractions are not calibrated probabilities.

**Conditional expectations:**
- **253931796** fails the two-event eligibility requirement in every template: epoch 173 lies about 0.20 d before the mid-sector break, and epoch 172 about 1.66 d after the nominal sector start. Its holdout EXCLUDED and RECOVERED counts therefore do not apply to S106 unless S106's data gaps differ from all templates.
- **183374279** fails it in five of seven templates. The override (§3.9) adds further INSUFFICIENT risk.
- For both, catalogs/allsky_tic2sectors_future.json lists no further TESS sector through S134. INSUFFICIENT would mean no completed S106 test and no further scheduled TESS test through S134 in that catalogue.
- **115692561 and 122522485:** under these noise and gap templates the reference-signal SNR is low (median 2.8 and 3.5). A decisive outcome may be unlikely, but an outcome probability has not been established. Holdout on-time recovery was 0/40 (115692561) and 0/35 (122522485), while the 122522485 design sector (S97, a double-length sector: 23 predicted and 12–15 eligible events per realisation) gave 28/40 against 2–6 eligible events per S105 holdout realisation.
- **120444365 and 206620592:** intermediate. Holdout on-time recovery was 30/71 and 11/40.
- **70441745:** holdout on-time recovery 40/40; displaced transits INCONSISTENT 33/40; nulls EXCLUDED 0/40 in both design and holdout.
- **Transfer:** whether S106 behaves like the holdout sectors is an assumption, not a measurement.

## 7. Known limitations (not fixed)
These need not block an explicitly limited operational procedure, but they block claims of calibrated significance or of faithful physical duration testing.
- **Red-noise factor:** β is MAD-based and measured at one timescale; it rarely exceeds 1 on real data. SNR values are nominal.
- **Consistency gate at high SNR:** the χ² depth-consistency gate can reject a real transit with modest depth variation at high per-event SNR (relevant to 253931796, which is expected INSUFFICIENT).
- **Injections** are rectangular boxes at exactly the reference depth.
- **Baseline and mask:** the local baseline is a median (the protocol says linear); the detrend mask differs from the protocol's.
- **Precedence:** INCONSISTENT is tested before EXCLUDED; the thresholds are asymmetric (SNR 5 vs 7).
- **Calibration masks:** for P ≤ 6 d, real transits are masked over ±(T14/2 + 10 min) in clock-corrected time. For 122522485 this mask (0.105 d) also triggers the pre-gap trim, which S106 will not have.
- **Configs** contain absolute local paths.

## 8. What is reported for each test
- the outcome of record (after any override), with `outcome_before_override` where applicable;
- every secondary readout;
- both frozen-evaluator outputs;
- the clock record;
- the edge-trim record;
- all per-event numbers;
- the release used;
- the ERRATUM_S106 data-availability caveat;
- the conditional expectations of §6.

## 9. Holdout integrity statement
- A filename inventory of the project found no S106 or later file of the seven test targets.
- One S106 1×1 TESScut cutout of TIC 206620592 exists in a session scratch directory. It was disclosed earlier in the S106 erratum and was never opened as data.
- A filename search cannot prove non-examination; the authors attest that no S106 photometry of these targets has been examined.
