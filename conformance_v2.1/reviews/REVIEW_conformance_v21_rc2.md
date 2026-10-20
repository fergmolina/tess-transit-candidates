# Focused independent recheck: conformance-v2.1-rc2

Date: 2026-10-20. Reviewer/tool: OpenAI Codex. Working directory: `/Users/fernando/Desktop/NASA`.

Instructions followed: `results/PROMPT_conformance_recheck_rc2.txt`. This report rechecks R1–R13 of `results/REVIEW_conformance_v21.md`; it is not a new candidate-discovery review.

Evaluator examined and executed: SHA-256 **`000b0dfb16e0cc7080ff5645885babd859806ae0de40645b07a93cfe5c5d3cb7`**. The supplied rc1 backup hashes to **`590502679b335e8b93f7f30612dda58894112fbbf83f0fb62f8b0acbaf5ac684`**, matching the evaluator reviewed previously. Verified with `hashlib.sha256` in `/tmp/conformance_rc2_review/audit.py` and the initial setup check.

## Verdict

**Publish after listed fixes.** The original EXCLUDED NaN failure is repaired, both test suites pass, and the completed rc2 simulation has consistent provenance and substantially more candid statistical wording. The RECOVERED, INCONSISTENT and parity-split calculations are unchanged from rc1, apart from the declared refusals and final override. However, the stricter “any gap” commitment still fails on a single missing cadence: my new end-to-end regression returns RECOVERED while calling that window clean. The authoritative evaluator docstring also retains the withdrawn “~2 sigma” duration interpretation and an unqualified claim to defeat alternating displacements. Correct those before publication, reconcile the small documentation/output mismatches below, and complete the already drafted registration amendments as part of the release. Evidence and the limits of these conclusions follow.

## R1–R13 status

“Resolved” refers to the specific rc1 finding; it does not imply general validation of the candidate or an astrophysical false-positive rate. Draft amendments may appropriately remain unappended during review, but they must be finalised with the release rather than left as placeholders.

| Finding | Status | Evidence, verification and remaining action |
|---|---|---|
| **R1: completed calibration/provenance** | **Resolved** | I read `holdout_calibration_rc2_runs.csv` and compared all **1,080** corresponding `scratchpad/cal_rc2/*/*/res.json` files. Every result has the current evaluator SHA, exactly the declared nine target-sector pairs occur, and every CSV outcome agrees with its JSON. The **67** entries in `results/conformance_v21/README.md` match their actual SHA-256 values. See `audit.py`/`audit.txt` under `/tmp/conformance_rc2_review/`. |
| **R2: invalid effective-N/family-wise intervals and refusal denominators** | **Resolved for the requested correction** | `scripts/conformance_calib_report.py` and `conformance_summarise.py` remove rounded effective counts and the product-based family bound. Scored denominators explicitly whitelist RECOVERED, INCONSISTENT, EXCLUDED and AMBIGUOUS. The full report lists not-scored outcomes separately. Procedure §5 and log 86 withdraw the 0.14-per-test claim and explicitly say the seven-test family-wise rate is not calibrated. Running the report generator on the supplied CSV reproduces the supplied Markdown **byte for byte**. Raw CP intervals remain binomial-reference summaries conditional on this simulation, not validated coverage guarantees for the actual seven S106 tests; that limitation must remain with the tables. |
| **R3: EXCLUDED drops an event through nan-summing** | **Resolved for the demonstrated bug** | `outcome()` now requires finite per-event depths **and errors** for every eligible event at every gate-grid offset. My separately rerun original 70441745-like probe returns **AMBIGUOUS**, not EXCLUDED: `gate_window_all_finite=false`, `min_events_measured_in_gate=1`, `n_eligible=2`, condition (a) false. Evidence: `/tmp/conformance_rc2_review/probe704.py`, `probe.log`, `probe704/result.json`. “Measured” still means the declared ≥3 in-box/≥5 baseline points, not ≥90% coverage of every shifted box. Also fix the per-offset diagnostic wording in N3 below. |
| **R4: false literal edge-selection criterion** | **Resolved by disclosure** | Procedure §5 now explicitly says the 1.5/0.5-d cuts do **not** satisfy the literal every-bin criterion and quotes the failing bins. Log 86 corrects item 76 and identifies the cuts as an author-selected pooled design rule after inspecting profiles. I compared the rc1 and rc2 draft texts and checked the quoted values against the previous independent grouped-count audit. `edge_trim` is AST-identical to rc1; this is a correction of provenance/claims, not a secretly changed cut. |
| **R5: failed 40-run split-selection rule** | **Resolved by disclosure** | Procedure §5 and log 86 explicitly state the original 34→28/40 loss was 15 points, the rule failed, the author overrode it, and 160 runs reused the phase sequence and were exploratory. The earlier “was noise” claim is withdrawn. Verified by reading those passages and comparing them with the original report's directly checked CSV counts. |
| **R6: object-specific override and document precedence** | **Partially resolved** | `strict_epoch_check()` and `override()` now enforce flagged/missing listed epochs and save the pre-override outcome; the 27-case suite exercises flagged and absent epochs. Governance explicitly defines precedence and the final `outcome` field. All seven amendment drafts now exist. But a **single missing cadence passes the strict check**, because its spacing is two cadences, not greater than two. My end-to-end example still returns RECOVERED. See N1. The nominal window is now explicitly tc ± T14/2; that choice is disclosed rather than left implicit. |
| **R7: release selection/clock-warning discretion** | **Resolved** | All seven configs specify `release_of_record=v01`. The evaluator rejects other versions and any nonempty clock warning; independently rerun regression cases pass. Governance says that if v01 is withdrawn before scoring, the test is deferred and a dated note precedes examination of any replacement. This is a clear policy rather than an automatic v02 substitution. Verified from configs, evaluator diff, governance and `inputs_network.log`. I did not query MAST to decide whether any release is presently withdrawn. |
| **R8: calibration time frame, masks and artificial holes** | **Resolved at the stated conditional-simulation level** | The rc1/rc2 harness diff shows clock correction before short-period real-transit masking; the mask is ±(T14/2+10 min). For P>6 d the harness instead avoids real events by 0.3+7.5 T14 and does not cut their transit holes. Its text now qualifies whether residual real signal is excluded. Procedure §7 discloses that the **122522485** short-period mask is about **0.10556 d**, exceeding the 0.1-d gap threshold and causing extra trimming absent in S106. My 30-run S69 rerun agrees with the corresponding stored rc2 runs. These changes do not prove every residual transit is removed or make simulated placements identical to the actual S106 experiment. |
| **R9: absolute power/reachability claims** | **Partially resolved** | The “whatever the truth,” universal EXCLUDED-unreachability and no-future-TESS assertions are replaced by conditional template/noise statements in procedure §6 and amendment drafts. The forecast's light-travel, short-gap, override and parity limitations are now listed, and transfer to S106 is called an assumption. One unlabelled **rc1** sector comparison remains in the rc2 evidence section: **4/36 vs 28/36**, where rc2 is **3/35 vs 27/36**. See N3. |
| **R10: parity-specific safeguard and uncalibrated duration score** | **Partially resolved** | Procedure §§3/5 correctly call the score non-calibrated, disclose parity matching, and quote the independent paired-pattern recovery **3/10**. But the **authoritative evaluator docstring** still calls the duration rule “~2 sigma” and says the split “Defeats alternating displacements.” Governance departure 5 still calls the duration test a “likelihood criterion.” See N2. These wording contradictions survived despite the public summary being corrected. |
| **R11: integrity inventory and known scratch cutout** | **Resolved as disclosure/attestation** | Log 86 narrows the earlier statement; procedure §9 discloses the known 206620592 S106 cutout and says filename searches cannot prove non-examination. This is consistent with the previous report and the erratum disclosure. I checked the text; I did not open that cutout or independently verify the non-examination attestation. |
| **R12: source labels and one-gap clock wording** | **Resolved** | The 183374279 config now says **post-freeze dated addendum**; 120444365/70441745 say BLS fallback because the shape output has no T14 field. The generator distinguishes raw-SAP reference depths from ephemerides that also use SPOC PDCSAP. Replacing the clock tool's new one-gap sentence by the old sentence reconstructs the exact rc1 SHA **`c016ad7a…`**: its change is demonstrably docstring-only. Evidence: config/source reads and `audit.txt`. |
| **R13: validation and no-usable-data policy** | **Partially resolved** | New checks enforce a supplied evaluator lock, positive finite references, duplicate times/epochs and finite nonnegative sigma; the input suite passes. An edge-emptied input now returns INSUFFICIENT. However, TIMEUNIT/BJDREFF/TIMEREF are still only recorded; prediction epochs are not explicitly checked as finite integers; and an otherwise valid all-flagged series returns INVALID_INPUT, while an edge-emptied series returns INSUFFICIENT. See N4 for the precise scope of this remaining input-policy issue. These are not new failures of the seven valid frozen CSVs. |

## New and remaining findings

### N1 — Must fix: one missing cadence does not trigger the strict override

In `scripts/prereg_conformance.py:strict_epoch_check`, the internal-gap predicate is:

```python
np.max(np.diff(tw)) > 2 * cad
```

Removing one sample from a regular 200-s series makes a **400-s** separation. It is not greater than two cadences. My direct tests at tc=100.0, 4214.9134372290555 and 4226.651420766412 all return `violated=false, reason="clean"` with one central cadence absent. Two missing central samples do trigger the gap check. A present, flagged central cadence triggers it as expected. Evidence: `/tmp/conformance_rc2_review/strict_probe.py` and `strict_probe.log`; these FITS files are synthetic and contain no target S106 data.

I also tested the complete evaluator on artificial QLP-format **S98** inputs, with two high-SNR transits, the 183374279 reference depth/duration and strict epochs numbered 245/246. Both the clean version and the version missing one central cadence return **RECOVERED**, with both strict windows called clean and the override untriggered. Evidence: `/tmp/conformance_rc2_review/override_end_to_end.py`, `override_end_to_end.log` and its two result JSONs. This is an end-to-end demonstration of the logical omission, not a claim about actual S106 flux.

The rc2 threshold is openly stated in governance, but the same documents/amendments still say the original “a gap or flagged cadences” clause stays in force. Treating a missing expected cadence as clean relaxes that commitment. Use an expected cadence grid or a declared jitter-tolerant threshold that detects a **single** absent cadence, and check missing samples at the window edges as well. For regular 200-s timestamps a threshold between one and two nominal cadences can detect this case; anchor the tolerance to the cadence rather than floating-point equality. Add a missing-one-cadence regression, alongside the existing flagged-cadence regression.

The tc ± T14/2 definition itself is now explicit. A flagged sample outside that nominal window does not trigger this override, even if it could overlap a permitted shifted transit; this is a declared scope limitation rather than a hidden implementation choice. Do not describe it as a flag-free check across the whole timing gate.

### N2 — Must fix: the authoritative computation description contradicts the revised claims

The evaluator's module docstring, designated authoritative by procedure §2/§3, still says:

- Step 6: “duration consistent with 0.7-1.3 x ref at **~2 sigma**”;
- Step 8: the split “**Defeats alternating displacements**”;
- Opening paragraph: “It implements the written protocol outcome rules,” without the new qualification that this is an amended operational test.

Governance departure 5 also retains “a **likelihood criterion**.” These passages were verified in `scripts/prereg_conformance.py` and `results/GOVERNANCE_S106_TESTS_DRAFT.md`, rather than inferred from the authors' response. They conflict with the corrected summary and the counterexamples retained in `results/REVIEW_conformance_v21.md`.

Use the following consistent descriptions in all authoritative sources:

> Compatibility requires SNR²(band) ≥ SNR²(any duration) − 4. This is a nominal score rule, not a calibrated likelihood or 2σ duration interval.

> The parity split reduces some alternating-offset recoveries. It does not eliminate alternating or nonalternating timing failures at operating SNR.

> This is a newly amended operational test; the departures from the original protocol are listed in the governance statement.

These are documentation corrections, not a request to retune RECOVERED, INCONSISTENT or the split after seeing more simulations. Refresh hashes after correcting them and preserve which evaluator SHA generated each existing result set.

### N3 — Small factual/output inconsistencies to fix

1. **Stale sector rates.** Procedure §5, immediately after the rc2 table, says “Sectors differ strongly (120444365: S69 **4/36** vs S103 **28/36**).” Those are rc1 figures. The rc2 CSV gives **3/35** and **27/36**. Replace the values or explicitly label the comparison rc1. I verified this by grouping `holdout_calibration_rc2_runs.csv` and cross-checking the underlying JSONs.
2. **Per-offset diagnostics are not emitted.** Procedure §3.10 promises EXCLUDED diagnostics “including per-offset event counts.” The code computes an array `nfin` but serialises only `min_events_measured_in_gate` and `n_eligible`. Either emit the count array with its offset coordinates or change the promise to “minimum number of events measured over the gate.” Verified from `outcome()` and my probe JSON. This does not undo the repaired finite-event test.
3. **One negative-outcome design result remains absent from the compact public discussion.** The previous review identified **1/160 on-time 183374279 design injections returned INCONSISTENT**. The rc2 procedure still shows only RECOVERED in the design table. Add that count or explicitly direct readers to a complete outcome table including it. Source: the previously checked `discriminating_ontime160.csv`, re-tabulated against the original report; the rc2 holdout itself has zero on-time INCONSISTENT outcomes.

### N4 — Input-policy boundary remains incomplete; document or harden it

My end-to-end synthetic S98 tests give:

| Input | Current outcome | Verification |
|---|---|---|
| Cadences present, but all removed by the fixed edge rule | INSUFFICIENT, reason “no usable cadences after the edge rule” | `override_end_to_end/trim_empty/res.json` |
| Same otherwise valid series, all QUALITY values nonzero | INVALID_INPUT (“no valid cadences, or times look like BJD...”) | `override_end_to_end/all_quality_bad/res.json` |

The first early return occurs before clock validation and before strict-epoch records are made. This is a conservative, nonpositive outcome, not a route to RECOVERED. Nevertheless, the documentation should say that an edge-empty series is classified without a clock record, and explain the separate all-flagged INVALID_INPUT policy. Alternatively, classify a valid but unobservable all-flagged product as INSUFFICIENT too. Keep these categories out of calibration's scored denominators, as the revised report already does.

The pre-existing time-header gaps also remain: `load_lc` records TIMEUNIT, BJDREFF and TIMEREF, while `main` checks only TIMESYS/BJDREFI. Explicitly validate the supported units, zero fractional reference and reference frame, or state the exact trusted-product assumption. Epoch validation should reject nonfinite/noninteger epochs before later integer conversion. I established these points by code inspection; I did not perform new attacks on every malformed-header or epoch case, and none is evidence that the seven frozen CSVs are malformed. This is why R13 is only partially resolved rather than a claim of another demonstrated candidate-scoring failure.

## Independent reproduction results

All temporary files, copied drivers, generated light curves and caches are under `/tmp/conformance_rc2_review/`. I wrote no project file other than this report. Temporary drivers add `-B` to subprocess invocations and reduce multiprocessing from 12 to three workers; their numerical/scoring code calls the unmodified project evaluator. The R3 probe was copied to a new scratch path so the authors' earlier overwriting of `/tmp/conformance_v21_review/probes704/result.json` does not affect this recheck.

Representative invocations, with NUMBA/MPL cache paths set under that directory:

```text
.venv/bin/python -B -I /tmp/conformance_rc2_review/test_conformance.py /tmp/conformance_rc2_review/logic
.venv/bin/python -B -I /tmp/conformance_rc2_review/test_conformance_inputs.py /tmp/conformance_rc2_review/inputs_network
.venv/bin/python -B -I /tmp/conformance_rc2_review/probe704.py
.venv/bin/python -B -I /tmp/conformance_rc2_review/conformance_calibrate_holdout.py /tmp/conformance_rc2_review/holdout /tmp/conformance_rc2_review/holdout.csv 5 120444365:69 183374279:69
.venv/bin/python -B -I /tmp/conformance_rc2_review/audit.py
```

| Check | Result | Evidence |
|---|---|---|
| Logic suite | **15/15 pass** | `logic.log`, final `FAILURES: 0` |
| Input/refusal/regression suite | **27/27 pass** | `inputs_network.log`, final `FAILURES: 0` |
| Original EXCLUDED probe | **AMBIGUOUS; missing-event gate explicitly fails** | `probe.log`, fresh `probe704/result.json` |
| Additional strict-gap probe | **Fails intended “any gap” protection for one missing sample** | `strict_probe.log`, end-to-end results described in N1 |
| Small rc2 recalibration rerun | **30 runs; 30/30 outcomes agree with matching stored rc2 runs** | `holdout.csv`, `audit.txt` |
| Full report regeneration | **Byte-identical to authors' rc2 report** | `rebuilt_full_report.md` compared with `results/conformance_v21/holdout_calibration_rc2_report.md` |

The first sandboxed input-suite attempt stopped because `ssd.jpl.nasa.gov` could not resolve; `clock_retry.log` records the DNS failure. Re-running with authorised network access to JPL completed all 27 cases. The successful clock test used **cached S105** QLP/TESScut inputs; no S106 cutout was requested. The S106-without-flag refusal case supplies the existing S105 file and refuses before opening test-sector data. This environmental failure was not counted as an evaluator regression.

Small recalibration subset, five realisations per case:

| Target/sector | Null | On-time injection | Common displaced injection |
|---|---|---|---|
| 120444365 S69 | 4 AMBIGUOUS, 1 INSUFFICIENT | 4 AMBIGUOUS, 1 INSUFFICIENT | 4 AMBIGUOUS, 1 INSUFFICIENT |
| 183374279 S69 | 5 AMBIGUOUS | 1 RECOVERED, 4 AMBIGUOUS | 5 AMBIGUOUS |

These are conditional code-reproduction counts, not new estimates of S106 performance. Source: independent grouping of `/tmp/conformance_rc2_review/holdout.csv`; matching target/sector/case/k rows in the supplied full CSV all agree.

## Recalibration provenance and numerical cross-checks

I audited the JSON files under the already identified, permitted earlier-sector directory:

```text
/tmp/claude-501/-Users-fernando-Desktop-NASA/c3c861f6-d690-49d9-96f5-051efe8a7e34/scratchpad/cal_rc2/
```

No FITS file in that provenance audit was opened. The JSONs show exactly these nine pairs, each with 120 runs (40 per case): **183374279 S69/S103; 120444365 S69/S103; 70441745 S68; 206620592 S68; 253931796 S68; 122522485 S105; 115692561 S69.** All **1,080** evaluator hashes equal the seven configs' `evaluator_sha256`. All result mtimes are after the rc2 evaluator mtime; this is consistent with the recorded execution order, not immutable independent evidence of declaration times. Source: `audit.py`/`audit.txt`.

The complete outcome counts are **714 AMBIGUOUS, 167 RECOVERED, 111 INCONSISTENT, 46 EXCLUDED and 42 INSUFFICIENT**. No INVALID_INPUT/CLOCK_UNVERIFIED/CLOCK_FAILED result appears. There are **360** clock-bearing runs and **zero** warnings. The 360 null runs consist of **300 AMBIGUOUS, 46 EXCLUDED and 14 INSUFFICIENT**, hence **0 RECOVERED / 346 scored**. These independently tabulated values agree with log 87 and the revised procedure.

| TIC | On-time RECOVERED / scored | Displaced INCONSISTENT / scored | Null EXCLUDED / scored |
|---|---:|---:|---:|
| 70441745 | 40/40 | 33/40 | 0/40 |
| 120444365 | 30/71 | 12/71 | 1/71 |
| 183374279 | 46/80 | 26/80 | 6/80 |
| 206620592 | 11/40 | 0/40 | 0/40 |
| 122522485 | 0/35 | 0/35 | 0/35 |
| 253931796 | 40/40 | 40/40 | 39/40 |
| 115692561 | 0/40 | 0/40 | 0/40 |

The 42 INSUFFICIENT runs are **27 for 120444365** and **15 for 122522485**, distributed equally across their three cases. Verified directly from the full CSV and every corresponding JSON, rather than relying on the Markdown table.

## Did anything else change?

Within the examined scoring procedure, I found no undeclared retuning of RECOVERED, INCONSISTENT or the split:

- AST comparison of rc1 and rc2 gives identical `load_lc`, `edge_trim`, `red_noise_beta`, `coverage`, `box_fit`, `event_grid`, nested `best`, `comparable`, `timing_split` and `finish` functions, and identical RECOVERED and INCONSISTENT conditional branches. The surrounding added release/input/clock checks, EXCLUDED finite-event gate and final override are the declared changes. Verification: Python `ast.dump` comparisons and the full `git diff --no-index` between the hash-verified rc1 backup and current evaluator.
- Reversing the single clock-docstring sentence reconstructs the exact rc1 clock SHA, proving no clock-body change. The imported `qlp_clock_v2.py` retains its prior-review hash. The edge-profile, forecast, logic-test and real-validation scripts also retain their prior-review hashes. Source: comparison with `/tmp/conformance_v21_review/input_hashes.json`.
- The design harness's extra `outcome_joint_only` output field was already identified during the end of the rc1 review; it is not a new scoring change. The rc1 holdout-harness backup hashes to **`0ff19c53…`**, matching the final rc1 manifest. Its rc2 diff concerns the declared real-transit masks/placements and updated limitations, not the thresholds or case definitions. Source: `/tmp/conformance_rc2_review/calibration.diff` and the previous report's recorded final state.
- All seven configs retain the same reference depths, durations, products, prediction hashes and test sectors as the earlier configuration backups and the rc1 review table. Each actual prediction CSV hash agrees with its config and `final_ephemeris_v2.json:sha256_csv`. New config fields are the declared release/strict-epoch locks and corrected provenance/version metadata. Source: `audit.txt`.
- I compared the snapshotted current inputs at the beginning and end of this recheck; none changed during it. Source: `/tmp/conformance_rc2_review/start_hashes.json` and the final hash check.

This is a scoped statement about the files/hashes above, not a claim that every file anywhere in the project was compared against a complete prior repository snapshot. The prior review did not save such a snapshot. I did not run the generator, publish anything, contact anyone, or open/download any S106-or-later photometry/cutout of the seven test targets. I did not independently verify the authors' attestation of earlier non-examination.

## Minimum remaining release work

Fix the single-missing-cadence strict override and add its regression; align the authoritative docstring/governance with the corrected score and split interpretation; correct the stale rc1 sector rates and diagnostic promise; and make the remaining input-policy assumptions explicit. Finalise the seven dated amendments and refresh the release hashes after changes. Preserve the honest statements that rc2 calibration is already-seen development evidence, the rates are conditional on its artificial placements/noise, and the actual seven-test family-wise error rate remains uncalibrated. These repairs require no target S106 photometry.
