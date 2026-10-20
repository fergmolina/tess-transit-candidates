# Independent focused recheck: conformance-v2.1-rc3

Date: 2026-10-20. Reviewer/tool: OpenAI Codex. Working directory: `/Users/fernando/Desktop/NASA`.

Instructions: `results/PROMPT_conformance_recheck_rc3.txt`. Baseline: `results/REVIEW_conformance_v21_rc2.md` and the hash-verified rc2 evaluator backup. Sources actually opened include the current evaluator, input/logic tests, seven configurations, procedure/governance/amendment drafts, manifest, decisions 88–89, rc2/rc3 calibration CSVs and permitted earlier-sector calibration result JSONs. Executions and additional evidence are identified below. No protected target's Sector 106-or-later photometry or cutout was opened or downloaded.

Evaluator reviewed: SHA-256 **579d50acbcaba7ec67e64ec20868c8322497a30c2f0f7c4b4fd31467f0522bbd**. The rc2 backup hashes to **000b0dfb16e0cc7080ff5645885babd859806ae0de40645b07a93cfe5c5d3cb7**. Verification: `hashlib.sha256` and the source comparison in `/tmp/conformance_rc3_review/audit.py`.

## Verdict

**Publish after listed fixes; rc3 still has publication blockers.** The single-missing-cadence protection now works, the duration/split claims are corrected, and all 1,080 calibration outcomes agree with rc2 with consistent evaluator provenance. However, the newly promised all-flagged → INSUFFICIENT path crashes instead. Worse, the input suite reports that case passing by reading a stale result from the previous case. Governance also retains the superseded two-cadence threshold. Repair these implementation, verification and governing-text defects before declaring the procedure final. The header policy needs a small clarification/hardening, and the rc3 calibration report needs its version label corrected. These findings arise from source inspection and fresh executions below, not acceptance of the authors' log assertions.

## Requested status table

“Resolved” applies to the specific earlier finding, not to general validation of the seven astrophysical candidates or calibrated S106 error rates.

| Item | Status | Evidence and remaining work |
|---|---|---|
| **N1: one missing cadence escaped the strict override** | **Resolved for the demonstrated bug** | `strict_epoch_check()` now uses internal spacing >1.5 median cadences and an edge allowance of 1.05 cadences. My unchanged synthetic `strict_probe.py`, copied to a new scratch directory, detects one missing central sample at all three previously tested centres. My end-to-end S98 synthetic clean case remains RECOVERED; removing one central sample changes the final result to INSUFFICIENT and preserves RECOVERED as `outcome_before_override`. See the two scratch logs and JSONs below. The outside-window flag remains clean, consistent with the explicitly nominal-window scope. |
| **N2: authoritative duration/split descriptions contradicted the corrected claims** | **Resolved** | Current evaluator opening, steps 6/8, `comparable()` docstring, and governance departure 5 describe an amended operational test, an uncalibrated SNR-squared score rule, and a partial parity safeguard. The earlier “~2 sigma”, “Defeats alternating displacements” and calibrated-likelihood interpretations are removed from these passages. Verified by the complete rc2→rc3 evaluator diff and direct reads of the current governance/procedure. |
| **N3: stale counts, missing diagnostics, undisclosed design INCONSISTENT** | **Resolved** | Procedure §5 now has 120444365 S69 **3/35**, S103 **27/36**, and explicitly states the **1/160** on-time 183374279 INCONSISTENT result. I regrouped the rc3 holdout CSV and `discriminating_ontime160.csv`: the latter has 137 RECOVERED, 22 AMBIGUOUS, 1 INCONSISTENT under `outcome_split`. Current `outcome()` emits `events_measured_per_gate_offset` with both coordinates and counts; the new fields are present in the rc3 CSV/JSON evidence. |
| **N4: no-data and time-header/epoch policy** | **Partially resolved** | Finite-integer prediction epochs are checked, numeric nonzero BJDREFF is refused, and the pre-clock no-data exception is now disclosed. But an all-flagged input crashes before classification; missing TIMEUNIT/TIMEREF are accepted despite mandatory wording, and nonnumeric BJDREFF crashes. Verified by independent end-to-end/header probes, not just the supplied suite. See F1/F4. |
| **R6: strict override and precedence** | **Partially resolved** | The original positive-outcome failure is repaired in code and the procedure summary. The governance precedence table, however, still says spacing **>2 cadences**, contradicting **>1.5** in the evaluator and procedure §3.9. All seven draft amendments exist and their current configuration/evaluator hashes match, but are not release-final after the required code repair. See F3 and the amendment assessment below. |
| **R9: power/reachability and stale sector rates** | **Resolved** | Procedure §§5–6 and the amendment drafts retain conditional, template-dependent claims, not universal outcome probabilities; the stale sector rates are corrected. I compared those passages with the rc2 report and independently grouped the rc3 CSV. The actual seven-test family-wise false-RECOVERED rate remains explicitly uncalibrated. |
| **R10: parity and duration interpretation** | **Resolved** | The authoritative docstring now agrees with the procedure's limitations; governance no longer calls the duration score a likelihood criterion. `timing_split` and the executable `comparable` body remain AST-identical to rc2. Evidence: direct text comparison and `/tmp/conformance_rc3_review/audit.txt`. |
| **R13: validation/no-usable-data handling** | **Partially resolved** | New epoch and header checks improve validation, but F1/F2 show that the all-flagged policy and its purported regression are not functioning. F4 records the narrower header discrepancy. This does not imply any of the seven existing prediction CSVs is malformed. |

## New and remaining findings

### F1 — Blocker: all-flagged/no-finite-data input crashes instead of returning INSUFFICIENT

The evaluator docstring, procedure §3.3 and decision 88 promise that an all-flagged product returns INSUFFICIENT before the clock gate. In `scripts/prereg_conformance.py:204–208`, removing the old empty-array refusal allows an empty `t` into `edge_trim()`. That unchanged function indexes `t[0]` and `t[-1]` at line 119. Consequently the new `no_data` branch at line 221 is never reached.

My fresh synthetic S98 `override_end_to_end.py` execution exits **1**, with **IndexError: index 0 is out of bounds for axis 0 with size 0**, and creates no result JSON for `all_quality_bad`. Its edge-emptied case correctly returns INSUFFICIENT. Evidence: `/tmp/conformance_rc3_review/override_end_to_end.log` and the absence of `override_end_to_end/all_quality_bad/res.json` in that fresh directory. Repeating with the suite's permitted S105 all-flagged file independently produces the same crash (`stale_probe.log`).

**Exact fix:** make the empty-array case safe before indexing in `edge_trim` (or bypass trimming when no finite QUALITY=0 samples remain), then retain prediction validation and return the documented INSUFFICIENT result with a reason. Exercise both all-flagged and all-nonfinite/empty usable arrays through the real command-line entry point with fresh output paths. No threshold retuning is needed.

### F2 — Blocker: the input suite falsely passes a crashed evaluator using stale JSON

`scripts/test_conformance_inputs.py:24–26` repeatedly uses `D/out.json`, ignores `subprocess.run(...).returncode`, and immediately reads that path. The new all-flagged test follows the missing-one-cadence test, whose outcome is INSUFFICIENT. When all-flagged crashes, the previous JSON survives and meets the next expected prefix.

I reran the supplied suite with only `-B` added to child Python commands; it prints **FAILURES: 0**, including “all cadences flagged ... got INSUFFICIENT.” I then reproduced the relevant two calls independently, logging the exit code and saved/requested light-curve paths:

| Call | Exit | JSON read back | Stored input |
|---|---:|---|---|
| Strict epoch with one missing cadence | 0 | INSUFFICIENT | `inputs_network/strict_miss/...fits` |
| All cadences flagged, same output path | **1** | **The preceding INSUFFICIENT** | **Still `inputs_network/strict_miss/...fits`, rather than requested `inputs_network/allflag/...fits`** |

Evidence: `/tmp/conformance_rc3_review/stale_probe.py`, `stale_probe.log`, `stale_result.json`, and `inputs_network.log`. These S105 files are temporary copies of previously used, permitted in-sample data. This is a demonstrated false pass, not a hypothetical test-harness concern. Decision 88's “31/31” cannot be presented as 31 correctly verified successful cases.

**Exact fix:** use a unique output path per case, remove any pre-existing result before invocation, require a successful subprocess exit, and require a newly written JSON that matches the requested light-curve/configuration hashes. Unexpected exceptions must fail the test with stderr. The logic suite also ignores subprocess return codes; harden its runner consistently, especially for reruns into an existing directory. Correct the validation claim after rerunning the repaired suite. Changing the expected prefix alone does not repair this failure.

### F3 — Required governing-text fix: old gap threshold survives

`results/GOVERNANCE_S106_TESTS_DRAFT.md:20` still defines the strict clause as “a spacing **> 2 cadences**”. The current evaluator's `strict_epoch_check` and procedure §3.9 specify **>1.5 median cadences**, plus a **>1.05-cadence** edge allowance. These governing documents must agree before scoring.

Replace that part of the governance row with:

> Within tc ± T14/2 in clock-corrected time, any flagged cadence, non-finite flux, internal spacing greater than 1.5 median cadences, or first/last cadence more than 1.05 median cadences inside a window edge triggers the strict clause. Non-finite TIME rows are discarded and the resulting coverage gaps are tested. An absent or ineligible listed epoch also makes the final outcome INSUFFICIENT.

This mirrors the inspected implementation and retains the disclosed nominal-window scope. Refresh the governance hash after correction. The procedure's phrase “changed no scoring logic” should preferably say “the joint RECOVERED/INCONSISTENT/split/EXCLUDED calculations are unchanged; the final strict override and input handling changed,” because the demonstrated strict-epoch outcome does change. Verification: full evaluator diff and procedure §2.

### F4 — Small input-policy corrections remain

Current line 201 accepts `TIMEUNIT=None` and `TIMEREF=None`; the docstring and procedure §3.1 say these headers must be `d` and `SOLARSYSTEM`. My synthetic S98 copies with either keyword removed still return **RECOVERED**. Numeric BJDREFF=0.1 returns INVALID_INPUT as intended, but BJDREFF=`oops` raises an uncaught **ValueError** and writes no result. Evidence: `/tmp/conformance_rc3_review/extra_checks.py` and `extra_checks.log`.

Either require the two header values as written, or explicitly declare their absence acceptable under a trusted QLP-product convention. Catch malformed BJDREFF conversion and return INVALID_INPUT. These are defensive/input-contract corrections; I found no evidence that any actual locked prediction CSV or permitted calibration light curve has these malformed values. They should not be used to claim the existing calibration has a timing-unit error.

### F5 — Minor provenance label

`results/conformance_v21/holdout_calibration_rc3_report.md` starts **“Holdout calibration report (conformance-v2.1-rc2)”**. `scripts/conformance_calib_report.py` hard-codes that heading. The report is byte-identical to rc2 because the tabulated counts are identical, but the rc3 evaluator provenance in the underlying JSONs is correct. Label the report rc3, ideally including the evaluator SHA or an explicit source-CSV identifier. Verification: direct first-line read, generator read, and byte-identical independent regeneration under `/tmp/conformance_rc3_review/rebuilt_report.md`.

## Reproduction, diff and provenance checks

All temporary drivers, synthetic FITS, copied earlier-sector inputs, outputs and caches are under `/tmp/conformance_rc3_review/`. Representative commands, with NUMBA/MPL caches directed there:

```text
.venv/bin/python -B -I /tmp/conformance_rc3_review/strict_probe.py
.venv/bin/python -B -I /tmp/conformance_rc3_review/override_end_to_end.py
.venv/bin/python -B -I /tmp/conformance_rc3_review/test_conformance.py /tmp/conformance_rc3_review/logic
.venv/bin/python -B -I /tmp/conformance_rc3_review/test_conformance_inputs.py /tmp/conformance_rc3_review/inputs_network
.venv/bin/python -B -I /tmp/conformance_rc3_review/audit.py
.venv/bin/python -B -I /tmp/conformance_rc3_review/stale_probe.py
.venv/bin/python -B -I /tmp/conformance_rc3_review/extra_checks.py
```

The first sandboxed input-suite attempt stopped at clock-record setup. A rerun with network access to JPL vectors completed; it used cached S105 inputs, not protected test-sector photometry. No `--declared-test` command was run. The completed input-suite log's zero failures is subject to F2 and is not accepted as a clean pass. The logic suite reports **15/15**, and my fresh synthetic probes independently verify the strict-epoch repair and the empty-input regression.

The complete rc2→rc3 evaluator diff contains the declared wording/version changes, strict thresholds, time-header/epoch/no-data handling and added diagnostic arrays. AST comparisons confirm unchanged `load_lc`, `edge_trim`, `red_noise_beta`, `coverage`, `box_fit`, `event_grid`, `best`, `override`, `timing_split`, `finish`, and the executable `comparable` body. Removing only the newly emitted diagnostic field makes the entire nested `outcome` AST identical to rc2. Thus I found no hidden retuning of the joint RECOVERED, INCONSISTENT, parity-split or EXCLUDED calculations. Source/evidence: `diff -u` of the two evaluators, `audit.py`, `audit.txt`.

All seven configs differ from the previous review's snapshotted bytes **only in evaluator SHA and `locked_utc`**, not literally evaluator SHA alone as the prompt says. Replacing those fields reconstructs each original rc2 SHA exactly; the prior timestamp was **2026-10-20 15:59:25 UTC**. This is benign regeneration metadata, not a changed reference value. All seven actual prediction CSV hashes still equal their configuration locks. Verification: `extra_checks.py`/`.log`, the earlier `/tmp/conformance_rc2_review/start_hashes.json`, and `audit.py`.

I inspected all **1,080** `res.json` files under the permitted earlier-sector calibration directory:

```text
/tmp/claude-501/-Users-fernando-Desktop-NASA/c3c861f6-d690-49d9-96f5-051efe8a7e34/scratchpad/cal_rc3/
```

Every `script_sha256` equals the current evaluator SHA and all seven configuration locks. Every CSV outcome matches its corresponding JSON. Exactly the nine declared pairs occur, each with 120 runs: **183374279 S69/S103; 120444365 S69/S103; 70441745 S68; 206620592 S68; 253931796 S68; 122522485 S105; 115692561 S69.** The CSVs have unique `(tic, sector, case, k)` keys and **1,080/1,080** matching outcomes between rc2 and rc3. All other CSV columns agree except the expected expanded EXCLUDED diagnostics. Source: both full CSVs, individual JSON reads and `audit.py`/`audit.txt`; an independent column comparison used `set_index(['tic','sector','case','k']).sort_index()`.

The recomputed totals are **714 AMBIGUOUS, 167 RECOVERED, 111 INCONSISTENT, 46 EXCLUDED, 42 INSUFFICIENT**. Nulls give **0 RECOVERED / 346 scored**, with 14 additional INSUFFICIENT null runs. All **360** clock-bearing results have empty warnings. These match the current procedure and decision 89. All **72** manifest SHA entries match their files. Verification: the same complete JSON/CSV/hash audit; these counts are conditional development-simulation evidence, not new S106 performance estimates.

## Are the seven amendment drafts final apart from the date?

**No, because the evaluator still needs the repairs above.** At the reviewed state, all seven sections exist and each contains the correct current evaluator and individual configuration SHA. Their conditional rates agree with the independently audited rc3 results. The placeholder `<date>` and dated governance filename are understandable draft fields. Verification: `REGISTRATION_AMENDMENTS_DRAFT.md`, all seven config hashes and the audit's seven `AMENDMENT_CONFIG_MATCH` checks.

After repairing the evaluator/test runner and governance, refresh the evaluator lock in all seven configs, their hashes in all seven amendments, and the manifest. Supply actual publication dates/filenames and the remaining final governance reference before appending/releasing. Preserve the current rc3 calibration's true SHA; if the release file changes, do not silently relabel these results as executions of the new file. Record the repair-only diff and its fresh regressions, and either provide calibration on the final SHA or clearly justify reuse as unchanged scoring calculations. The original failure is an input/override defect, not a reason to tune thresholds on already inspected calibration outcomes.

## Limits

This is the requested focused rc2→rc3 check, not a repeat of the full original review. I did not rerun 1,080 numerical injections; I audited every stored result, compared both full CSVs, regenerated the report, reran the two suites and independent synthetic probes. Stored hashes establish consistency of the supplied provenance, not an immutable external proof of execution chronology or non-examination. I did not re-inventory all scratch photometry, contact anyone, publish anything, or open/download S106-or-later photometry/cutouts for any of the seven protected test targets. I edited no project file except this report. The dossier review was handled separately and does not alter this conformance verdict.

The end-of-review hash comparison found no change to the snapshotted evaluator, configurations, test scripts or reviewed procedure/governance/amendment documents. `logs/DECISIONS.md` changed during the check by the addition of dossier-review item 90; the relevant conformance items 88–89 remain present. Verification: `/tmp/conformance_rc3_review/start_hashes.json`, the final `hashlib.sha256` comparison and a direct read of the log tail.
