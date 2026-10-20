# Independent audit of the Sector-106 preregistered test procedure

**Date:** 2026-10-19. **Reviewer/tool:** OpenAI Codex. **Verdict: NOT READY.**

**Sources actually opened:** the two objects' local registrations, prediction CSVs, ephemeris and vetting JSONs; the evaluator and clock/extraction scripts; existing S96/S105 QLP FITS files; the public Zenodo v1.9 ZIP and GitHub tree; the MAST QLP notice; and JPL Horizons spacecraft vectors at the S106 prediction dates. No S106 photometry was fetched or loaded. Only this report was created in the repository; temporary diagnostic inputs, scripts and logs were written under `/tmp/s106_audit/`.

## Verdict

The frozen predictions are identifiable and their checksums are correct, but the evaluator is not a faithful implementation of the registered test. It substitutes a 30-minute timing tolerance for the much narrower registered three-sigma windows, does not measure duration, averages individual timing offsets that can cancel, and can declare exclusion without full transit coverage. These are demonstrated failures, not only theoretical objections: the unchanged evaluator returned RECOVERED for deliberately too-short transits and opposite approximately 50-minute timing errors, and EXCLUDED with 90% of both transit windows missing. An earlier-sector test also changes from RECOVERED to INCONSISTENT solely by choosing SAP_FLUX versus the default DET_FLUX. The clock policy is publicly archived, but the current clock script does not visit S106 and the evaluator does not apply or require its result. The procedure therefore needs implementation corrections and a dated public clarification before it can yield an interpretable registered outcome. This is a judgment about the test machinery, not a rejection of either candidate. [D,C,P,T,J below]

## Evidence and scope

All repository paths below are relative to `/Users/fernando/Desktop/NASA`.

- **[D — frozen documents/data products]** Read `results/vet_allsky/{183374279,120444365}/PREREGISTRATION*.md`, matching `final_ephemeris*.json`, `predicted_transits_2026_2027*.csv`, and `report.json`, using `cat`, numbered source reads, and Python JSON/CSV parsers. Recomputed CSV SHA-256 values with `hashlib`. Read `catalogs/TESS_orbit_times.csv` and the clock addendum/JSONs/`shifts.csv`. References to a registration's “outcomes” or “addendum” identify those sections of the named file.
- **[C — code audit]** Read all 60 lines of `scripts/prereg_test.py`, all 71 lines of `scripts/qlp_clock_v2.py`, relevant generation logic in `scripts/prereg_v2.py:69–124`, `scripts/vet.py:17–22`, `scripts/tsearch.py:29–65`, and all of `scripts/triceratops_qlp.py`. Inspected the installed `wotan.flatten` signature and its default handling of `break_tolerance`. Evaluator SHA-256: **`630815cc1400f0434dc9f30c8ce08cc42635ee5d1d429338c4010f6115043366`**, identical to `prereg_bundle/prereg_test.py` and its entry in `prereg_bundle/SHA256SUMS.txt`. This is the evaluator run below.
- **[T — executed diagnostics]** Ran the original evaluator in subprocesses using `.venv/bin/python -B -I scripts/prereg_test.py`, without changing it. Used existing `data/qlp_allsky/hlsp_qlp_tess_ffi_s{0096,0105}-<16-digit TIC>_tess_v01_llc.fits`, temporary backward predictions from each frozen v2 ephemeris, and deterministic synthetic CSVs. Harnesses `/tmp/s106_audit/dryrun.py` and `additional_cases.py` record exact commands and stdout/stderr in individual `.log` files. A summary and reproducible construction are included below so the conclusions do not depend on retaining temporary files. NumPy/Numba caches were directed to temporary storage where applicable.
- **[J — independent clock/UTC calculation]** Queried [JPL Horizons](https://ssd.jpl.nasa.gov/api/horizons.api) with TESS target **−95**, barycentric centre **500@0**, geometric ICRF vectors, `REF_PLANE=FRAME`, `OUT_UNITS=AU-D`, `TIME_TYPE=TDB`, `VEC_CORR=NONE`, `VEC_TABLE=1`. Projected vectors onto the two target directions myself. The query driver and raw responses are `/tmp/s106_audit/clock_and_public.py`, `horizons_<TIC>.json`, and `clock_numbers.json`. Separately inverted barycentric light time with Astropy at the geocentre to check UTC labels and orbit-end coverage. These are geometry calculations, not observations of an S106 timestamp defect.
- **[P — public-record verification]** Retrieved [Zenodo record 23483639](https://zenodo.org/api/records/23483639), created **2026-10-19 20:19:29 UTC**, version **v1.9**, and opened its **6,813,226-byte ZIP** in memory. Relevant documents and CSVs match the local hashes. Retrieved the complete, non-truncated [GitHub tree at d995a1fff8ad24171cad4bd35dc07ebe04a66539](https://api.github.com/repos/fergmolina/tess-transit-candidates/git/trees/d995a1fff8ad24171cad4bd35dc07ebe04a66539?recursive=1), whose commit timestamp is **20:19:23 UTC**. This establishes what those public records contain, not private access/discovery chronology.
- **[M — mission notice]** Opened the [MAST QLP page](https://archive.stsci.edu/hlsp/qlp), including “Corrected timestamps for QLP Sectors 99–104” and its sector-availability table, and the [Horizons manual](https://ssd.jpl.nasa.gov/horizons/manual.html). The inspected MAST table had no S106 entry. I did not probe S106 product URLs or TESScut, so I do not independently certify that every form of S106 data is unavailable.

The prompt's “before its data exist” framing needs qualification: S106 was already observed in July–August 2026 according to the local orbit table. The registrations concern photometry not examined/released at the stated freeze, not future observations. TIC 183374279's addendum correctly admits that FFI availability through TESScut at the freeze was not checked. Preserve that distinction. [D,M]

## 1. Test of record and integrity

**Both objects use v2.** TIC 183374279 explicitly calls v2 its first freeze; no v1 ephemeris/registration was present in its inspected directory. TIC 120444365's v2 explicitly **supersedes v1**, retaining the older files as historical records. The clock addendum says the frozen prediction remains the test centre; it does not undo this v2 selection. Do not import TIC 89247735's separate “v1 remains the test of record” rule into these objects. [D,P]

| Object/version | CSV SHA-256 | Verification/status |
|---|---|---|
| TIC 183374279 v2 | `069d82980645e2adb5bc81895b187de8654dc880205574a50af764b79b04d621` | Local CSV = ephemeris JSON = registration = public v1.9 ZIP. **Test of record.** |
| TIC 120444365 v2 | `32b5e0857265e33e4902c5736d379bf0d7443516a9277678c2b403ac7b22de17` | Same four-way agreement. **Test of record.** |
| TIC 120444365 v1 | `64b5b02607a23e21d3270eb1862dde28aec81050807ea0584f49f312de1f7094` | Same four-way agreement. **Superseded**, not an interchangeable test. |

The rule change between TIC 120444365 v1 and v2 is real: v1 uses a **0.6–1.5 depth band and 60-minute absolute timing cap**, whereas v2 uses **0.5–1.5 and 30 minutes**. v2's explicit supersession establishes which applies. An audit of v1 alone against the current code would therefore be the wrong comparison. [D, both outcome paragraphs]

Reference values are not equally well frozen:

- **TIC 183374279:** its dated addendum specifies **1090 ppm**, **T14=2.84 h**, **QLP SAP_FLUX**, **QUALITY=0**, masked **0.7-d biweight**; a TESScut fallback is triggered only if QLP is not released by **2026-11-15**. Use the stated rounded 1090, not silently the `report.json` value 1092.0646. [D]
- **TIC 120444365:** v2 says depth/duration “the values above,” but lists several sector depths and **no single reference depth or duration**. Its `report.json` contains masked-BLS **743.2843 ppm/2.0 h** and raw-SAP **855.3393 ppm**; the nominal circular shape implies approximately **2.1827 h**. The present generator would choose raw-SAP depth but fall back to BLS duration, because `shape_mcmc` has no `T14_h` key. None of this establishes a unique number in the already archived v2 text. Freeze an explicit choice and product of record; do not choose whichever gives a pass. [D; `prereg_v2.py:109,119`; direct circular-duration calculation from the shape medians]

The timing records and clock policy are public, but I did **not** find `prereg_test.py` or `SHA256SUMS.txt` in the inspected v1.9 ZIP/current GitHub tree. The evaluator's docstring says it is part of a frozen bundle; its checksum is verifiable in the **local** `prereg_bundle`, but that is not proof that this implementation was publicly frozen. This finding is limited to the public release/tree inspected; I did not search every possible separate deposit. Publish an explicit evaluator/configuration version with the dated implementation correction. [C,P]

## 2. Rule-versus-code discrepancies

Line numbers in this table refer to `scripts/prereg_test.py` unless stated otherwise. “Ambiguity” identifies a choice the documents do not fully specify; it is not permission to make the choice after seeing S106.

| Registered requirement / issue | Actual implementation | Consequence and necessary correction | Evidence |
|---|---|---|---|
| Timing within **3 sigma AND at most 30 min** | Line 47 uses **`max(3*mean(sigma_pred),30)`**. | For the S106 v2 rows, the written gates are **8.1/8.4 min** for TIC 183374279 and **6.3 min** for TIC 120444365; code uses **30 min**. Use the per-event intersection, i.e. the smaller bound, not the larger. | D; C:47; T `late20` |
| Matching at least two predicted transit times | Lines 44–49 require two covered windows, then test a **weighted mean offset**. | Opposite bad offsets cancel. Count at least two qualifying events; report their individual residuals. A mean residual is supplementary, not a substitute. | C:41,44–49; T `opposite50` |
| Duration **0.7–1.3× reference** | Every fitted box has the input duration; no duration estimate or acceptance check exists. | A fixed-duration fit cannot test duration. Fit/measure it with a predefined method and check the interval. | C:35–41,49; T `narrow0p6` |
| Positive transit-like dip | Box coefficient is unconstrained; minimum residual sum of squares can select a **brightening**. | A positive excursion can determine the purported transit time. Require an appropriate positive eclipse depth and report cases without an identified dip. | C:36–41; T S96/S105 examples below |
| Depth band associated with matching events | Only the unshifted, inverse-variance **stacked mean** is checked; event depths are not checked. | One strong dip plus a very weak/absent event can pass the stack. Clarify whether the band is per event or for a common-depth joint fit, while still requiring two actual timing matches. | D ambiguity; C:46–49; T strong/weak case |
| EXCLUDED requires at least two **fully covered transits** | Coverage is total cadence count within **±1.5 durations**, accepted at **60%**, plus only three samples inside the nominal transit. | Baseline points can compensate for a missing transit centre. Require contact/window coverage and usable baselines, not a single count over a broad window. | C:32–33,50; T missing-centres case |
| TIC 183374279 addendum: gap/flags compromising either of epochs 245/246 means insufficient | No object-specific eligibility or full-coverage rule; 60% coverage is tolerated generally. | State exactly which gap/flag patterns invalidate a transit. Do not treat a partially covered event as satisfying the two-event requirement merely because a broad count passes. | D addendum §1; C:32–44 |
| Product/reference depth of record | Default FITS selection is PDCSAP, else DET, else SAP; no object configuration binds depth/duration to a product. | Default violates TIC 183374279's primary SAP instruction unless `--flux-col SAP_FLUX` is supplied. TIC 120444365's choice is unresolved. Earlier-sector SAP/DET outcomes differ. Freeze commands/configuration and prohibit outcome-driven product selection. | C:13,18; T real-data table |
| Quality policy | FITS keeps only QUALITY=0, but CSV uses its first two columns and ignores flags/errors. | An externally prepared CSV can silently include flagged measurements. Validate preprocessing provenance and record dropped-cadence counts. | C:19–22 |
| Detrending/edge policy | Mask is ±one input duration; biweight window 0.7 d; Wotan default break tolerance 0.35 d; no explicit edge trim. | The 0.7-d window matches the TIC 183374279 addendum, but “same as vet.py” does not specify this exact pipeline: `vet.py` uses 0.75 d and break tolerance 0.5 d. The addendum mentions a 0.3-d trim absent here. Freeze one policy, including how gaps/edges affect eligibility. | C:28–29; `vet.py:17–20`; `tsearch.py:57–65`; installed Wotan source; D |
| Stacked SNR and “3 sigma” exclusion | One global MAD scatter is divided by square root of the number of in-transit points; baseline uncertainty and time correlations are omitted. | This is an uncalibrated white-noise approximation. It can overstate recovery significance and the strength of an upper limit, especially around ramps/gaps. Predefine and test a correlated-noise/baseline-aware uncertainty procedure using existing sectors or injections. | C:29,38–46,50 |
| Prediction versus measurement timing uncertainty | No measurement-time uncertainty is estimated. Weights are **depth** weights; prediction sigmas are simply averaged. | The written tolerance refers to frozen `sigma_min`; code does not implement that and does not combine errors statistically. Do not silently widen the frozen gate with a new quadrature rule. State how timing uncertainty is reported/handled without changing the registered acceptance window. | D; C:41,46–47 |
| INCONSISTENT if a comparable displaced signal exists | EXCLUDED is tested first. Only otherwise scan ±0.3 d; use the deepest un-baselined moving-window mean, without an explicit duration fit/SNR test. | A real displaced signal can be labelled EXCLUDED; a noise dip can be labelled INCONSISTENT; the deepest non-comparable feature can hide a comparable one. Define precedence, search domain, comparability and significance before the data. | C:50–58; T `late200`; real S105 default |
| Four advertised outcomes | Line 58 also emits **AMBIGUOUS**. | The four written clauses do not exhaust all possibilities. The fifth outcome is reasonable in principle but currently unregistered. Define the residual category explicitly rather than forcing a pass/exclusion. | D; C:58; T S96 TIC 183374279 |
| Clock check before testing | Evaluator takes FITS TIME directly; clock script loops only over sectors in the **existing fitted ephemeris**. | `qlp_clock_v2.py TIC` will revisit S103/S105, not S106, even if a new QLP file is present. It also writes a correction JSON, not a corrected test light curve. An explicit S106 clock-check/application stage and fail-closed gate are missing. | C evaluator:19; clock:51–69; D ephemeris sector lists |
| Frozen file/identity and input validity | No checksum, target/sector-header, time-standard, order, duplicate or empty-input validation. Sector selection is string-prefix matching; CSV column names are ignored. | Wrong product, changed references, BJD instead of BTJD, or duplicate/unsorted rows can give misleading outputs or exceptions. Add validation and immutable input/configuration hashes to the result. `--sector 10` can match 106 in this generic selector; this specific misuse does not occur with an exact 106 request. | C:13–26,43,60 |
| TESScut fallback as specified | Referenced `triceratops_qlp.py` builds aperture coordinates for contamination analysis but folds **QLP DET/KSPSAP flux**; it does not implement an edge-ring sky-subtracted light curve. | The fallback extraction is not reproducibly defined by that script. Specify actual cutout photometry, sky-ring pixels/statistic, quality selection, normalization/dilution, timing conversion and reference-depth mapping. | D TIC 183374279 addendum §2; `triceratops_qlp.py:14–29` |

The input mask correctly prevents the predicted central windows from defining the biweight trend, and the explicit `len(cov)<2` branch correctly returns INSUFFICIENT when fewer than two windows pass its own coverage test. These limited correct behaviors do not cure the coverage definition or the requirement for two detected/matching events. [C:27–29,44; T original-CSV/partial-window smoke tests]

## 3. Clock assessment

### Expected S106 scale, independently computed

Target directions were read from each `report.json` and cross-checked with its clock JSON: TIC 183374279 **RA 357.519160°, Dec −39.334344°**; TIC 120444365 **RA 1.030380°, Dec −41.709317°**. I calculated `LTT = r_TESS dot n / c` using geometric barycentric JPL vectors, not the TESScut reference-position correction. Query epochs were estimated spacecraft times by subtracting the geocentric light time from the frozen BJD; this is adequate at the displayed 0.001-min precision. Adopted convention offsets from clean-sector JSONs were **0.031976784 min** and **0.032139935 min**, respectively. [D,J]

| TIC | Epoch | Target LTT, min | Correction if QLP TIME = spacecraft time, min | Correction if the small S105 residual persists, min |
|---|---:|---:|---:|---:|
| 183374279 | 245 | +4.844 | +4.876 | +4.928 |
| 183374279 | 246 | +5.706 | +5.738 | +5.790 |
| 183374279 | 247 | +6.364 | +6.396 | +6.448 |
| 120444365 | 559 | +4.171 | +4.203 | +4.249 |
| 120444365 | 560 | +4.616 | +4.648 | +4.694 |
| 120444365 | 561 | +5.016 | +5.048 | +5.094 |
| 120444365 | 562 | +5.349 | +5.381 | +5.426 |
| 120444365 | 563 | +5.683 | +5.715 | +5.761 |
| 120444365 | 564 | +5.957 | +5.989 | +6.035 |

The third column is the independently calculated light time. The fourth adds c0. The fifth additionally subtracts the saved S105 `QLP−spacecraft` residual, **−0.051646264 min** or **−0.045700439 min**. These last two columns are explicitly **conditional forecasts**, not measured S106 corrections. If MAST delivers correctly timed S106 products, the measured correction should instead be consistent with zero. Do not apply a missing-term correction merely because the sector number is ≥99. [D,J,M]

These new-data timestamp errors are different from the small **ephemeris-refit shifts** in `shifts.csv`: **+0.857–0.869 min** for TIC 183374279 and **+0.0501–0.0508 min** for TIC 120444365. A sub-minute change to the historical fit does not make a possible four-to-six-minute error in the test data harmless. [D,J]

**Could the clock alone change a decision?** Yes for a measurement near a boundary, but not automatically for a perfectly centred noiseless transit. For TIC 120444365, a roughly 6-minute error uses almost all its **6.3-minute** registered tolerance; an otherwise acceptable −1-minute residual would become approximately −7 minutes and fail the timing clause. Conversely, an unacceptable positive residual can be shifted into the window. For the central frozen/refined ephemerides alone, the calculated missing-term shifts remain inside the registered gates for both objects; claiming that S106 must fail without correction would be wrong. The current code's erroneous 30-minute gate conceals much of this sensitivity. Threshold crossings could yield AMBIGUOUS/INCONSISTENT rather than necessarily EXCLUDED; the categorical hierarchy must be fixed too. [D,J; direct boundary arithmetic; C:47–58]

### Is the planned method sound and public?

The physical procedure is sound in principle: reconstruct `TIME−TIMECORR`, establish the same-image correspondence, calculate the target's geometric correction at spacecraft time, retain the empirically measured QLP convention, and compare the corrected measurements with the **unchanged frozen BJD prediction**. The revised prediction can be shown alongside but must not recenter the scored window. The policy appears verbatim in the public v1.9 clock addendum, whose SHA-256 is **`90228ac3f47dfa363892f8579d2d7628a066f06caf3fc7bef04ec2086f26b67e`**, identical to the local file. It was publicly archived by the v1.9 creation time stated above. I cannot independently prove this predates every form of S106 data availability. [C,D,J,P,M]

Implementation is incomplete. Besides the absent S106 loop/application step, corrections must be evaluated across the test events rather than blindly using one constant sector offset: the light time varies by **1.52 min** across the three TIC 183374279 predictions and **1.79 min** across TIC 120444365's six. `qlp_clock_v2.py:68` currently evaluates one ephemeris-row time per sector. Record both raw and corrected times, the actual product version/hash, cadence correspondence, interpolation and residuals. [C,J]

The equal-length safeguard at clock-script lines 40–43 checks **increments**, which alone cannot exclude a whole-cadence origin error: shifting one equally spaced sequence by 200 s leaves its increments unchanged. A one-cadence mistake is **3.333 min**, substantial against these gates. This is a logical limitation of the guard, not a demonstrated misalignment in the existing JSONs. Require an absolute cadence/image anchor or independently matched gaps/orbit boundaries, and reject ambiguous matches. Gap-edge matching must likewise be checked rather than inferred solely from nearest times. [C; direct invariance of differences under a constant shift]

The adopted **0.05-min** allowance is explicitly described as conservative, not a calibrated absolute spacecraft-clock error distribution, in the public addendum. Preserve that qualification. [D,P]

### UTC and the end of S106

TIC 120444365's frozen v2 `utc` column is **not geocentric UTC**; it is the time-scale-only conversion. The existing `_v2_utcfix.csv` correctly distinguishes `utc_tdb_scale_only` from `utc_geocentric`. Independent Astropy inversion gives epoch 559 **2026-07-12 21:51:39.724 UTC**, versus frozen display **21:55**, and epoch 564 **2026-08-07 15:36:44.083 UTC**, versus frozen **15:42**. The evaluator uses `tc_btjd`, so this display error does not itself change its fit. Preserve the original hash and cite the corrected companion table for civil-time scheduling; do not substitute a re-centred ephemeris. [D,J; `prereg_test.py:32`]

For TIC 183374279 epoch 247, I obtain midpoint **2026-08-09 08:38:36.825 UTC**. With T14=2.84 h and the orbit-table end **09:10 UTC**, egress is approximately **53.81 min after data end** and approximately **68.4%** of the transit duration precedes that end. Thus “about half” in the addendum is imprecise; the event is nevertheless incomplete. Ideal dense coverage over the evaluator's three-duration window would be only **56.1%**, so its existing 60% rule would reject this particular edge event even though the rule fails other gap patterns. The test really depends on epochs **245 and 246**, as the addendum says. [D orbit-table rows for orbit 224; J; C:32–33]

## 4. Dry runs

### Existing-sector smoke tests

The frozen CSVs list later predictions, not the older-sector events. Running the original TIC 183374279 CSV against S105, still selecting `--sector 106`, correctly gives **three predictions, zero covered, INSUFFICIENT**. To exercise recovery, I generated temporary backward predictions from the **unchanged frozen v2 T0 and P**; reconstructed its timing covariance from the saved sector times/errors and inflation; and labelled the temporary rows `prediction (diagnostic back-projection only)` so the evaluator would accept them. These are in-sample implementation tests, not independent confirmation or registered outcomes. [D,T]

Representative command, with no `--out` argument and no writes by the evaluator:

```sh
NUMBA_CACHE_DIR=/tmp/s106_audit/numba .venv/bin/python -B -I scripts/prereg_test.py \
  --lc data/qlp_allsky/hlsp_qlp_tess_ffi_s0105-0000000183374279_tess_v01_llc.fits \
  --pred /tmp/s106_audit/183374279_s105_backprojection.csv \
  --depth-ppm 1090 --dur-h 2.84 --sector 105 --flux-col SAP_FLUX
```

I used unmodified archived S105 TIME for these smoke tests, not a new clock-corrected extraction. For TIC 120444365 the diagnostic reference was **743 ppm, 2.0 h** from v1, explicitly because v2 fails to specify one; I also repeated the clean S96 SAP test with **855.339 ppm**. Neither choice is being declared the proper future test configuration. [D,T]

| Object / sector / flux | Predicted / covered | Stacked depth ± error, ppm | SNR | Mean box offset, min | Evaluator output |
|---|---:|---:|---:|---:|---|
| 183374279 / S105 / SAP | 2 / 2 | 1171.87 ± 155.62 | 7.53 | +1.20 | RECOVERED |
| 183374279 / S105 / default DET | 2 / 2 | 1143.46 ± 148.12 | 7.72 | +1.20 | RECOVERED |
| 183374279 / S96 / SAP | 3 / 2 | 809.21 ± 163.82 | 4.94 | +19.02 | AMBIGUOUS |
| 120444365 / S96 / SAP | 5 / 5 | 908.31 ± 97.24 | 9.34 | −17.52 | RECOVERED |
| 120444365 / S105 / SAP | 5 / 4 | 733.70 ± 107.18 | 6.85 | −3.44 | RECOVERED |
| 120444365 / S105 / default DET | 5 / 4 | 720.51 ± 106.45 | 6.77 | +33.59 | INCONSISTENT |

The S96 alternate reference depth changes no measured statistic and still yields RECOVERED. The S96 TIC 120444365 event at epoch 497 receives **box_offset=−135.6 min and box_depth=−1585.34 ppm**: the selected feature is a brightening. In S105 DET, epoch 557 similarly supplies **+135.6 min and −787.73 ppm**, materially shifting the mean time. These explain why “the code runs” is insufficient validation and why a flux choice cannot be left discretionary. [T, `real_120444365_s96_SAP.log`, `real_120444365_s105_default.log`]

### Controlled adversarial cases

Construction: `t=np.arange(99,106,200/86400)` BTJD; predicted centres **100 and 105**; prediction sigmas **2.1 min**; reference **1000 ppm, 2 h**; Gaussian white noise **100 ppm** from `np.random.default_rng(99106)`. Inject rectangular dips, write two-column time/flux CSVs in `/tmp`, and run the unchanged evaluator with `--sector 106`. Flux generation uses `f=1+noise`, subtracting each specified depth where `abs(t−tc−offset/1440)<width_factor/24`. No synthetic result is an estimate of either star's actual false-positive rate. [T]

| Case | Actual input | Returned result | What it establishes |
|---|---|---|---|
| Control | Two on-time 1000-ppm, 2-h boxes | RECOVERED; depth **1010.48±12.03 ppm**, SNR **83.98**, offset 0 | Basic executable works on clean matching input. |
| Late by 20 min | Both otherwise matching boxes +20 min late | RECOVERED; fitted offset **+20.4 min**, depth **843.82 ppm** | Violates the **6.3-min** written gate but passes the code's 30-min gate. |
| Opposite timing errors | 1200-ppm boxes at −50 and +50 min | RECOVERED; individual fitted offsets **−49.2/+50.4**, mean **+0.6 min** | Neither event meets even ±30 min; averaging masks both failures. |
| Too short | Two **1.2-h** boxes, 0.6× reference duration | RECOVERED; depth **593.82±11.95 ppm**, SNR **49.70** | A duration below the registered 0.7× minimum is accepted. |
| Strong plus weak | On-time 1400-ppm and 100-ppm boxes | RECOVERED; stacked **760.50±11.96 ppm** | No per-event comparability requirement is enforced; clarify the intended depth rule. |
| Missing centres | No injected signal; delete **±0.9 h** around both centres | EXCLUDED; coverage **0.69** each, depth **4.94±40.71 ppm** | With 90% of both nominal transit durations unobserved, full-coverage exclusion is falsely asserted. |
| Real but displaced | Two 1000-ppm, 2-h boxes +200 min late | EXCLUDED; nominal-phase depth **−211.95±11.97 ppm** | Exclusion is returned without reaching the displaced-signal search, even though the comparable dips lie within its stated ±0.3-d domain. The registered category precedence needs clarification. |

A 1.8×-duration case was also run; it returned INCONSISTENT rather than identifying a duration failure. A partial-window mask leaving less than 60% broad-window coverage returned INSUFFICIENT, as its implemented coverage rule dictates. I did not tune the noise seed to make the core failures appear. [T, `synthetic_wide1p8.log`, `synthetic_partial_ends.log`]

## 5. Failure modes and protection by the frozen rules

| Failure mode | Do the frozen rules handle it? | Audit finding |
|---|---|---|
| Same ephemeris but faulty S106 clock | **Policy addresses it**, implementation incomplete. | Public clock-first statement is appropriate; require verified S106 coverage and actual application before scoring. [C,D,J,P] |
| Wrong-period/incorrect-time dips whose offsets cancel | **Yes**, if at least two individual times must match. | Current code substitutes a mean and can return false RECOVERED. [D,T] |
| Noise/systematic dip or transit of wrong duration | **Partly:** depth/duration/SNR rules intended to restrict it. | Duration is untested; SNR is not calibrated for correlated noise. No recovery result alone identifies a planet or eclipse host. [C,T; methodological limitation] |
| Transit hidden in a data gap or quality mask | **Yes for exclusion:** full coverage is explicitly required. | Broad 60% coverage can produce false EXCLUDED. Flagged cadences should not be silently restored to rescue a pass. [D,C,T] |
| One good transit and one absent/weak event | **Insufficiently precise about event depth**, but two timing matches are required. | Stacked significance can be dominated by one event; report all individual fits and predefine eligibility. [D,C,T] |
| Signal displaced from the frozen ephemeris | **INCONSISTENT is intended to cover it**, but overlaps with nominal-phase exclusion. | Fix ordering/search rules and label exclusion as exclusion of the registered signal/ephemeris, not proof that the star has no transit. [D,C,T] |
| SAP versus DET, or alternate aperture chosen after seeing the answer | **183374279 primary is specified; 120444365 is not adequately locked.** | Demonstrated SAP/DET output change makes this a practical selection risk. Fallback dilution and timing also need a fixed recipe. [D,C,T] |
| Red noise/baseline failure makes a tight upper limit | **Not quantitatively specified.** | White-noise errors can make exclusion too strong; predefined calibration and an unresolved-result category are needed. [C] |
| Wrong CSV, hash, units, duplicate times or product version | **Hashes exist**, but no enforcement. | Validate before analysis; archive exact commands, versions and diagnostics with the output. [C,D] |
| Treating post-release revisions as original preregistration | **Not solved by a checksum alone.** | Keep originals and publish dated amendments/implementation fixes, with access history; do not backdate or silently overwrite rules. [D,P; provenance inference] |

## 6. Required fixes or public clarifications before testing S106

1. **Lock the per-object configuration publicly.** Name the two v2 CSVs and full hashes above, the product/flux column, depth, duration, quality policy and evaluator hash. TIC 183374279 already supplies 1090 ppm/2.84 h/SAP; TIC 120444365 needs explicit reference values and a product of record. If choosing new values changes rather than clarifies its original specification, label the change as a dated amendment and preserve both records. [D,C]
2. **Correct the outcome evaluator before applying it to test flux.** Implement individual timing windows `min(3*sigma_min,30 min)`, at least two matching events, actual duration measurement, a positive-dip constraint, full-coverage exclusion, and an explicit residual/ambiguous category. Resolve depth-per-event versus joint-depth semantics and the INCONSISTENT/EXCLUDED ordering. Preserve the existing script/hash as the erroneous historical implementation. [C,T]
3. **Publish exact preprocessing and uncertainty definitions.** Set the edge/gap policy, biweight window/break tolerance, detrending masks, baseline model, usable-contact criteria, stacked-depth estimator and correlated-noise uncertainty procedure. Define measurement-time error reporting without silently relaxing the frozen timing gate. Verify with old-sector, gap, displaced, wrong-duration and red-noise injections; report failed diagnostics as well as successes. [C,T]
4. **Add an explicit S106 clock gate and corrected-data stage.** It must visit the selected test sector, verify absolute cadence correspondence, measure the correction over each event/window, avoid double-correcting repaired products, and refuse scoring if the clock cannot be established. Correct observed timestamps first; keep the frozen predictions and sigmas unchanged. Save product hashes, original/corrected times, vector-query parameters, convention and uncertainty justification. [C,D,J]
5. **Make coverage and fallback rules operational.** Keep epoch 247 of TIC 183374279 in the record but identify it as incomplete; epochs 245/246 must satisfy the published eligibility requirements. Specify what “a gap or flagged cadences” means quantitatively. Supply a real TESScut extraction implementation and its depth/timing mapping if invoking the November-15 fallback; the cited TRICERATOPS script is not that implementation. [D,C,J]
6. **Release the reviewed implementation/configuration with a dated clarification and then report exactly that test.** The verified public addendum already states clock-first/frozen-centre policy, but a bare policy is not a runnable audit trail. Link the corrected UTC companion table for TIC 120444365, retain original CSV bytes, and explicitly distinguish data already observed, data publicly available, and data actually examined. Do not claim the evaluator was in the inspected public v1.9 archive when it was not. [D,P]

A suitable explicit clock clarification is:

> Before inspecting the S106 transit flux, we will verify the timing of the selected QLP product using same-image spacecraft times and JPL TESS vectors at the target position. Any required correction will be applied to the observations, with its derivation and product hashes retained. The scored windows remain centred on the unchanged registered v2 BJD_TDB values, with their frozen sigma_min and thresholds. A corrected/refitted ephemeris will be reported only as supplementary information. An unverified clock or inadequate coverage will not be used to claim recovery or exclusion.

This wording clarifies the existing public policy; it does not supply the missing object configuration, statistical definitions or code corrections by itself. [D,P; reviewer recommendation]

## Limits and completion

I did not examine S106 flux, rerun the discovery search, validate the candidates astrophysically, or publish/contact anyone. The public availability check is limited to the inspected MAST page and archive/repository records; no claim is made that S106 FFIs never existed or were inaccessible to others. JPL numbers are conditional estimates of the missing-term scenario, not measurements of released S106 FITS timing. Old-sector runs are in-sample diagnostics and were not clock-corrected; synthetic tests demonstrate logical defects without calibrating real-signal completeness. The rules/JSONs/CSVs, evaluator and clock code were not modified. Their inspected hashes were checked for stability during the audit. [D,C,T,J,P,M; recorded operations]

**Final verdict: NOT READY.** The frozen timing records are intact, but the current executable cannot be relied upon to report the frozen test. Resolve the listed implementation and specification defects before the S106 outcome is examined or announced.
