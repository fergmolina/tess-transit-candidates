> **DRAFT 2026-10-20 (release candidate conformance-v2.1-rc1), NOT PUBLISHED.** For external review before publication. It replaces
> the withdrawn v2.0 draft (CONFORMANCE_PROCEDURE_2026-10-20.md). Must be published before any Sector 106 photometry of a test target
> is examined. Governance and departures: GOVERNANCE_S106_TESTS_DRAFT.md. Design log: logs/DECISIONS.md items 70-82.

# Conformance procedure for the seven Sector 106 tests

## 1. Why a second evaluator
Independent reviews showed that the frozen evaluator `scripts/prereg_test.py` (SHA-256 `630815cc…`):
- averages timing offsets, so opposite offsets cancel;
- never measures duration;
- can lock onto a brightening;
- can return EXCLUDED without full coverage;
- has an undeclared fifth outcome.

It stays frozen, and its literal output is reported for every test in two locked variants: the same inputs (SAP_FLUX), and the protocol's column (DET_FLUX). The outcome of record comes from the conformance evaluator below.

## 2. Code and locked inputs
The hashes are filled in at release; the current values are from rc1.

| File | Role |
|---|---|
| `scripts/prereg_conformance.py` | evaluator v2.1; the docstring is the authoritative procedure |
| `scripts/qlp_clock_test_sector.py` + `scripts/qlp_clock_v2.py` | per-event QLP clock record (S99+ products); integer cadence alignment against a TESScut cutout. **For S106 this downloads a TESScut cutout of the test target, i.e. S106 pixel data**; it runs only with `--declared-test` at test time. |
| `results/qlp_clock_v2/<TIC>.json` | clock constants c0 from control sectors ≤ 98 (seven files; SHA-256 prefixes 77f91265, 8af71b26, 1e6cd1b2, 3fe2b7c9, 97a82f4f, c07a319b, 81d285ee) |
| `scripts/make_conformance_configs.py`, `configs/conformance/<TIC>_S106.json` | locked per-test settings: prediction CSV + hash, product, reference depth/T14, evaluator SHA, both frozen-evaluator commands, edge rule |
| `scripts/test_conformance.py` | logic tests (about 10× the operating SNR; they check each outcome route, not performance) |
| `scripts/test_conformance_inputs.py` | 18 input and clock-gate refusal cases |
| `scripts/conformance_edge_profile.py` | derivation of the edge rule (design sectors) |
| `scripts/conformance_discriminating_test.py` | operating-SNR tests on design sectors |
| `scripts/conformance_calibrate_holdout.py`, `scripts/conformance_summarise.py` | calibration on holdout sectors |
| `scripts/conformance_s106_forecast.py` | S106 eligibility and power forecast, made without S106 photometry |
| `results/conformance_v21/requirements_venv_locked.txt` | pinned environment (Python 3.12.9; numpy 2.5.4, scipy 1.18.1, pandas 2.3.3, astropy 8.0.2, wotan 2.0) |

## 3. Procedure (summary; the docstring governs)
1. **Validate the inputs:**
   - the prediction-CSV hash;
   - the product: QLP HLSP file-name pattern, `ORIGIN` MIT/QLP, `TIMESYS` TDB, `BJDREFI` 2457000;
   - header `SECTOR` and `TICID` match the config;
   - at least one predicted event.
2. **Clock:** for QLP sectors ≥ 99, a clock record must match the TIC, sector, light-curve SHA-256, prediction-CSV SHA-256 and event list, otherwise the outcome is CLOCK_UNVERIFIED (there is no bypass). Corrections shift the observations; predictions are never shifted.
3. **Edge rule:** drop cadences within 1.5 d after the data start or any resume following a gap > 0.5 d, and within 0.5 d before any gap > 0.1 d or the data end. The rule was derived on design sectors with a criterion declared in advance (§5).
4. **Preprocess:** keep QUALITY = 0; biweight detrend (0.7 d window) with predicted transits masked.
5. **Eligibility:** ≥ 90 % of the in-transit interval sampled, plus baselines on both sides.
6. **Joint box search:** common offset (±0.3 d) and duration (0.5–2.0× reference). A box is VALID only if it is a dip, the per-event depths are consistent (χ² p ≥ 0.01), and ≥ 2 events are positive at 1σ.
7. **Comparable signal:** a band-duration (0.7–1.3×) fit with SNR ≥ 5, depth 0.5–1.5× reference, and Δχ² ≤ 4 against the best fit at any duration.
8. **Outcomes, in order:**
   1. INSUFFICIENT: fewer than 2 eligible events.
   2. RECOVERED: a comparable signal with offset within max(3σ, 30 min), **and** the timing-split check: each epoch-parity half's best offset is within the gate.
   3. INCONSISTENT: the best comparable VALID fit within ±0.3 d has SNR ≥ 7 and lies more than max(gate, 30 min) away.
   4. EXCLUDED, all three required:
      - (a) depth + 3σ < 0.3× reference at every offset within the gate;
      - (b) per-event consistency at the prediction;
      - (c) no VALID fit with SNR ≥ 5 and depth ≥ 0.5× reference anywhere within ±0.3 d.
   5. AMBIGUOUS: everything else.
9. **Secondary readouts** (never the outcome of record):
   - the joint-only outcome (without the split check);
   - the min(3σ, 30 min) reading;
   - the per-event min() reading;
   - odd/even depths;
   - EXCLUDED diagnostics;
   - the frozen evaluator's output.

## 4. Data partition
Only 200-s sectors are used.
- **Design sectors** (edge rule, discriminating tests):
  - 183374279 and 120444365: S96, S105;
  - 70441745, 206620592, 253931796 and 115692561: S96;
  - 122522485: S97.
- **Holdout sectors** (calibration only): 183374279 and 120444365: S69, S103; 70441745, 206620592 and 253931796: S68; 122522485: S105; 115692561: S69.
- **Not used:** 30-min and 10-min sectors.
- **Data examined during development:** the v2.0 design work (four versions) used S96/S105 of 183374279 and 120444365. Those results are development checks, not validation.
- **Other uses of holdout sectors:**
  - All holdout sectors are in-sample for the ephemerides. Their real transits are removed (flagged) in every calibration copy.
  - The clock-tool validation reproduced published clock corrections that include S103 (183374279, 120444365) and S105 (122522485). That used QLP and TESScut timestamps only; no transit photometry or evaluator outcome was involved.
  - S68 was used for 70441745's clock constant c0.
  - No clock warning fired on any of the 360 holdout runs that went through the clock tool.
- **Reproducing the add-on comparison:** runs made before the split check became part of the outcome (DECISIONS 82) carry the joint-only outcome in `outcome` and the split outcome in `outcome_with_split`. Later runs carry `outcome_joint_only` explicitly (`scripts/conformance_disc_analyse.py` handles both).

## 5. Evidence at the operating signal-to-noise
- **Edge rule:**
  - Declared criterion: the smallest X beyond which every 0.25-d bin has a pooled fraction of |z| > 3 of at most 0.03 (the interior level is 0.02).
  - Fraction of |z| > 3 after a resume: 0.31, 0.25, 0.07, 0.09, 0.09, 0.06 in the bins up to 1.5 d.
  - Before a gap: 0.12, 0.17 in the first two bins.
  - After short gaps: no excess. Before short gaps: 0.05–0.06.
  - The worst case is TIC 183374279: z reaches +26 in the first 0.1 d after a resume.
- **Discriminating tests** (design sectors, real noise, locked settings, 40 realisations each; DECISIONS 79–81). RECOVERED counts under the final rule (with the split check):

| | 70441745 | 120444365 | 122522485 | 183374279 | 206620592 | 253931796 | 115692561 |
|---|---|---|---|---|---|---|---|
| on-time reference transit | 38/40 | 103/160 | 28/40 | 137/160 | 21/40 | 39/40 | 0/40 |
| null (no transit) | 0/40 | 0/40 | 0/40 | 0/40 | 0/40 | 0/40 | 0/40 |
| alternating ±(gate + 20 min) | 0/40 | 0/40 | 0/40 | 1/40 | 0/40 | 0/40 | 0/40 |
| random-sign ±(gate + 20 min) | – | 1/40 | – | 5/40 | – | – | – |
| 0.6 × T14 | 19/40 | 13/40 | 10/40 | 20/40 | 5/40 | 1/40 | 0/40 |
| 1.5 × T14 | 0/40 | 8/40 | 14/40 | 4/40 | 15/40 | 1/40 | 2/40 |

  - **Cost of the split check:** on-time recovery 0.74 → 0.64 (120444365) and 0.94 → 0.86 (183374279), measured on 160 realisations.
  - **Literal per-event alternative** (rejected): on-time recovery 29, 10, 0, 26, 0, 40, 0 of 40.
  - **EXCLUDED under the final rule:** displaced real transits read EXCLUDED 0/280; true nulls read EXCLUDED only for 253931796 (39/40) and 183374279 (1/40).
- **Holdout calibration.** The clearest lesson is that design-sector numbers are optimistic: TIC 122522485 recovered 28/40 on-time transits on its design sector (S97, a double-length sector) and 0/40 on its holdout sector (S105). Details (holdout sectors only; final evaluator SHA `59050267…`, the one recorded in the configs; 1,080 runs; real transits removed from every copy; full table in `results/conformance_v21/holdout_calibration_report.md`):

| test (holdout sectors) | null → RECOVERED | null → EXCLUDED | on-time → RECOVERED | displaced (+gate + 60 min) → INCONSISTENT | N_eff |
|---|---|---|---|---|---|
| 70441745 (S68) | 0/40 | 0/40 | 37/40 | 31/40 | 8 |
| 120444365 (S69, S103) | 0/72 | 1/72 | 32/72 (S69 4/36, S103 28/36) | 12/72 | 5 |
| 183374279 (S69, S103) | 0/80 | 7/80 | 45/80 (S69 8/40, S103 37/40) | 31/80 | 6 |
| 206620592 (S68) | 0/40 | 0/40 | 15/40 | 0/40 | 1 |
| 122522485 (S105) | 0/40 | 0/40 | **0/40** | 0/40 | 1 |
| 253931796 (S68) | 0/40 | 37/40 | 38/40 | 37/40 | 3 |
| 115692561 (S69) | 0/40 | 0/40 | 0/40 | 0/40 | 1 |

  - **No null was falsely RECOVERED** in any holdout run: 0 of 352 scored.
  - **The runs are not independent.** Realisations share one light curve, so the honest sample size is the effective number of independent realisations: 25 across all tests. A rate of 0/25 has a 95 % upper bound of 0.14 per test.
  - **The family-wise false-RECOVERED rate** across the seven tests is therefore not well constrained by calibration. The point estimate is 0, and the conservative bound is uninformative.
  - **Holdout power is lower than design-sector power,** and it varies strongly from sector to sector:
    - TIC 122522485: 28/40 on S97, a double-length sector with 17 events, but 0/40 on S105.
    - TIC 120444365: S69 4/36 against S103 28/36.
    - TIC 183374279: S69 8/40 against S103 37/40.

    The holdout numbers are the ones to expect for S106.
  - **Caveat on the holes:** the holes cut at real transits trigger the pre-gap trim for 183374279 and 253931796. S106 will have no such holes.

## 6. Stated in advance, before any S106 photometry
- **Forecast of eligible events** (no S106 photometry used; S106 gaps modelled with seven in-sample QLP gap patterns mapped onto the S106 downlink schedule; values are min/median/max, then expected joint SNR):
  - 70441745: 1/2/2, SNR 10.7;
  - 120444365: 2/2/3, SNR 4.8;
  - 183374279: 1/1/2, SNR 4.2;
  - 206620592: 13/16/20, SNR 5.5;
  - 122522485: 6/7/10, SNR 3.5;
  - 115692561: 16/19/23, SNR 2.8;
  - 253931796: 0/1/1.
- **Expected uninformative:**
  - 253931796 is expected INSUFFICIENT (epoch 173 sits 0.2 d before a downlink break; epoch 172 is within 1.7 d of the sector start).
  - 183374279 is probably INSUFFICIENT.
  - For both, **INSUFFICIENT means no TESS test of these ephemerides at all.** Neither star has any further TESS sector through S134 (catalogs/allsky_tic2sectors_future.json), so the 183374279 addendum's "the test moves to a later sector" cannot apply.
  - 115692561 and 122522485 will almost certainly be AMBIGUOUS whatever the truth: expected joint SNR < 5, and 0/40 on-time recovery on their holdout sectors.
  - 120444365 and 206620592 have holdout on-time recovery of about 44 % and 38 %, so an AMBIGUOUS result there says little about whether the signal is real.
  - 70441745 is the one test with high power: holdout on-time recovery 37/40, and a displaced transit is identified as INCONSISTENT in 31/40.
- **EXCLUDED** is effectively reachable only for 253931796. For 70441745 the ±130-min gate makes it unreachable.
- **Duration:** a 0.6× or 1.5× duration cannot be told from the 0.7–1.3× band at these signal-to-noise levels; RECOVERED does not certify the duration to better than this.
- **Random-sign timing displacements** beyond the gate are only partly caught.
- **RECOVERED does not exclude a half-period eclipsing binary** at these signal-to-noise levels (the odd/even depth diagnostic is reported).

## 7. Known limitations (not fixed)
- **Red-noise factor:** β is MAD-based and measured at one timescale; it rarely exceeds 1 on real data. SNR values are nominal, and the false-positive rates above are empirical.
- **High SNR:** at high per-event SNR the χ² depth-consistency gate can reject a real transit with modest depth variation. This is relevant only for 253931796 (per-event SNR ≈ 23), which is expected INSUFFICIENT.
- **Injections** are rectangular boxes at exactly the reference depth.
- **Baseline:** the local baseline is a median, where the protocol says linear; the detrend mask is 1.0 × T14 + gate where the protocol says twice the duration.
- **Precedence:** INCONSISTENT is tested before EXCLUDED, unlike the frozen evaluator.
- **Thresholds:** RECOVERED uses SNR ≥ 5 and INCONSISTENT uses SNR ≥ 7. The asymmetry is a look-elsewhere allowance, set after the v2.0 calibration.
- **Configs** contain absolute local paths.

## 8. What is reported for each test
- the outcome of record;
- every secondary readout;
- both frozen-evaluator outputs;
- the clock record (including its warning field);
- the edge-trim record;
- all per-event numbers;
- the ERRATUM_S106 data-availability caveat;
- the advance statements of §6.
