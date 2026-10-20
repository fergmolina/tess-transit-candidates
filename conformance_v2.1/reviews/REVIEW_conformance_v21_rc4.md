# Independent focused recheck: conformance-v2.1-rc4

Date: 2026-10-20. Reviewer/tool: OpenAI Codex. Working directory: `/Users/fernando/Desktop/NASA`.

Instructions followed: `results/PROMPT_conformance_recheck_rc4.txt`. Baseline: `results/REVIEW_conformance_v21_rc3.md`. Sources actually opened: the rc3/current evaluator and test runners, current procedure/governance/amendment drafts, seven configurations, manifest, decisions 91/93, report generator, rc3/rc4 calibration CSVs and all corresponding rc4 result JSONs. Fresh executions and their evidence are identified below. No protected target's S106-or-later photometry or cutout was opened or downloaded.

Reviewed evaluator SHA-256: **a864b07ace8d3220a2d94a60513a488c8a5d87b54f41ebf510ff40ef1755311f**. The supplied rc3 backup hashes to **579d50acbcaba7ec67e64ec20868c8322497a30c2f0f7c4b4fd31467f0522bbd**, matching the preceding review. Verification: `hashlib.sha256`, the full evaluator diff and `/tmp/conformance_rc4_review/audit.py`.

## Verdict

**Publish as declared procedure. No remaining publication blocker was found in this focused check.** F1–F5 are resolved: empty usable inputs now produce INSUFFICIENT, the runners reject crashes and stale results, governance agrees with the strict override, the header policy is enforced, and calibration reports identify their evaluator version. Both suites pass in fresh executions, and deliberate failure tests demonstrate that the earlier false-pass mechanism is closed. The 1,080 rc4 calibration outcomes match rc3 and their stored evaluator hashes match the seven locked configurations. This verdict concerns publication of the explicitly amended operational scoring procedure, with its existing limitations; it does not certify the candidates, literal compliance with every original registration clause, or calibrated S106 error probabilities. Routine finalisation of publication dates, filenames and document hash references remains necessary.

## F1–F5 status

| Finding | Status | Independent evidence |
|---|---|---|
| **F1: all-flagged input crashes instead of INSUFFICIENT** | **Resolved** | Current `main()` bypasses `edge_trim()` when the usable array is empty, then validates predictions and reaches the documented pre-clock no-data branch. My fresh `override_end_to_end.py` returns INSUFFICIENT for both all-flagged and edge-emptied synthetic S98 inputs. An additional all-nonfinite-flux case also exits 0 with INSUFFICIENT. Evidence: `override_end_to_end.log`, `additional_audit.log` and their fresh JSONs under `/tmp/conformance_rc4_review/`. |
| **F2: suite falsely passes a crashed case using stale JSON** | **Resolved** | `test_conformance_inputs.py:run_eval` uses numbered output paths, deletes pre-existing results, checks exit/output existence and verifies light-curve/configuration hashes. The logic runner deletes each prior output and checks exit/output existence. The current suites pass **35/35** and **15/15**. A deliberately crashing evaluator fails the input-runner fixture and all 15 full logic cases; an evaluator returning wrong input hashes fails as STALE. Evidence: runner diffs, `inputs_network.log`, `logic.log`, `runner_failure_checks.py/.log`, `logic_broken.log`. Decision 91 explicitly corrects the earlier false “31/31” claim. |
| **F3: governance retains old two-cadence threshold** | **Resolved** | The governance precedence row now says internal spacing **>1.5 median cadences**, window edges **>1.05 median cadences**, and non-finite TIME rows discarded with resulting gaps tested. This agrees with `strict_epoch_check()` and procedure §3.9. Procedure §2 now distinguishes changed override/input handling from unchanged joint calculations. Verified by reading the current three sources and the rc3→rc4 evaluator diff. |
| **F4: optional headers contradict mandatory wording; malformed BJDREFF crashes** | **Resolved** | TIMEUNIT=`d` and TIMEREF=`SOLARSYSTEM` are now required, and BJDREFF conversion errors are caught. Re-executing my synthetic `extra_checks.py` gives exit 0 and INVALID_INPUT for absent TIMEUNIT, absent TIMEREF, fractional BJDREFF=0.1 and nonnumeric BJDREFF=`oops`. Corresponding supplied input-suite cases also pass. Evidence: `extra_checks.log`, fresh header-probe JSONs, `inputs_network.log`, and current header-validation code. |
| **F5: rc3 calibration report labelled rc2** | **Resolved** | The report generator accepts a version label. The rc3 report now identifies rc3 and its evaluator prefix; the rc4 report identifies rc4 and the full current evaluator SHA. Regenerating the rc4 report with its stated label produces a byte-identical file. Evidence: `scripts/conformance_calib_report.py`, both report headings and `/tmp/conformance_rc4_review/rebuilt_report.md` compared with the supplied rc4 report. |

## Fresh reproduction and adversarial runner checks

Temporary drivers and caches are confined to `/tmp/conformance_rc4_review/`. The two suite copies differ from the project drivers only by adding `-B` to child Python invocations to prevent bytecode writes in the project. Their numerical code and the evaluator executed are unmodified. Representative commands, with NUMBA/MPL cache directories set under that scratch directory:

```text
.venv/bin/python -B -I /tmp/conformance_rc4_review/override_end_to_end.py
.venv/bin/python -B -I /tmp/conformance_rc4_review/extra_checks.py
.venv/bin/python -B -I /tmp/conformance_rc4_review/test_conformance.py /tmp/conformance_rc4_review/logic
.venv/bin/python -B -I /tmp/conformance_rc4_review/test_conformance_inputs.py /tmp/conformance_rc4_review/inputs_network
.venv/bin/python -B -I /tmp/conformance_rc4_review/stale_probe.py
.venv/bin/python -B -I /tmp/conformance_rc4_review/runner_failure_checks.py
.venv/bin/python -B -I /tmp/conformance_rc4_review/audit.py
.venv/bin/python -B -I /tmp/conformance_rc4_review/additional_audit.py
```

The input suite queried JPL spacecraft vectors using cached, permitted S105 inputs. Its S106-without-flag case uses the existing S105 file and checks refusal; no `--declared-test` invocation or protected S106 data access was made. Evidence: the copied driver and its successful execution log.

| Independent check | Observed result | Evidence under the scratch directory |
|---|---|---|
| Synthetic S98 clean high-SNR transits | RECOVERED; strict override inactive | `override_end_to_end/clean/res.json` |
| Same input with one central cadence missing | INSUFFICIENT; pre-override outcome RECOVERED | `override_end_to_end/one_missing/res.json` |
| Edge-emptied, all-flagged, all-nonfinite-flux inputs | Each exits 0 with INSUFFICIENT | `override_end_to_end.log`, `all_flux_nonfinite/res.json` |
| Original two-call stale-result probe | Both calls exit 0; second JSON now names the requested all-flagged S105 file rather than the preceding strict-missing file | `stale_probe.log`, `stale_result.json` |
| Input-runner crash injection | Exit 1; reports CRASH and FAILURES: 1; preseeded old output removed | `input_runner_crash.log` |
| Input-runner wrong-identity injection | Exit 1; reports STALE and FAILURES: 1 | `input_runner_wrong_identity.log` |
| Full logic suite directed at broken evaluator | Exit 1; all 15 cases explicitly fail on evaluator crash | `logic_broken.log` |
| Actual rc4 suites | 15/15 logic and 35/35 input cases pass | `logic.log`, `inputs_network.log` |

For the input-runner attacks, I extracted the actual `sha` and `run_eval` functions and final pass/fail loop into a temporary fixture, supplied synthetic S98 files, and pointed it at temporary broken/wrong-identity evaluators. I preseeded its output with a purported INSUFFICIENT result. Thus the attack tests the actual runner implementation without repeating unnecessary clock-network setup. For the logic attack I ran the full copied suite, changing only its evaluator path to the broken temporary script and precreating several stale outputs. Verification: `runner_failure_checks.py` and the generated fixture files.

## Scope of the diff and calibration provenance

The complete rc3→rc4 evaluator diff contains only the declared header wording/version change, required-header/robust-BJDREFF validation, and empty-array bypass before edge trimming. AST comparisons show every function body other than `main()` unchanged, including the complete nested **`outcome`**, **`comparable`**, **`timing_split`**, **`strict_epoch_check`** and **`override`** bodies. Consequently the joint RECOVERED/INCONSISTENT/split/EXCLUDED calculations have not been retuned. Verification: `diff -u results/conformance_v21/prereg_conformance_rc3_579d50ac.py scripts/prereg_conformance.py`, and `audit.py/.txt`. The retained diagnostic-removal comparison in that reused audit script is irrelevant here: the complete outcome AST itself is identical.

I compared both runner backups with the current runners; their changes implement the declared failure/identity checks and four added input cases. The comparison with the preceding review's input-hash snapshot finds only the declared conformance files and the growing decision log changed among the snapshotted files. This is not a comparison of every file in the project. Evidence: both runner diffs and `/tmp/conformance_rc4_review/changes_from_rc3.json`.

For each of the seven configs, replacing only `evaluator_sha256` and `locked_utc` reconstructs its exact prior rc3 file hash. Reference values, products, strict epochs, prediction locks and frozen-evaluator commands are therefore unchanged. Every actual prediction CSV hash also matches its configuration and `final_ephemeris_v2.json:sha256_csv`. Verification: `additional_audit.py/.log` using the previous review's `start_hashes.json`.

I read every rc4 calibration result JSON under:

```text
/tmp/claude-501/-Users-fernando-Desktop-NASA/c3c861f6-d690-49d9-96f5-051efe8a7e34/scratchpad/cal_rc4/
```

All **1,080** `script_sha256` values equal **a864b07a…**, matching all seven configs. Every CSV outcome agrees with its corresponding JSON. Exactly the declared nine pairs occur, each with 120 runs: **183374279 S69/S103; 120444365 S69/S103; 70441745 S68; 206620592 S68; 253931796 S68; 122522485 S105; 115692561 S69.** The rc3/rc4 CSVs have unique `(tic, sector, case, k)` keys and are **byte-identical**, not merely outcome-identical. Their evaluator provenance is established from the separate JSONs, not from a SHA column in the CSV. Evidence: `audit.py/.txt` and `additional_audit.py/.log`.

Independent totals are **714 AMBIGUOUS, 167 RECOVERED, 111 INCONSISTENT, 46 EXCLUDED and 42 INSUFFICIENT**. Nulls contain **0 RECOVERED / 346 scored**, plus 14 INSUFFICIENT null runs. All **360** clock-bearing results have empty warnings. These agree with procedure §5 and decision 93. The rc4 report regenerates byte for byte with its label, and all **78** current manifest file hashes verify. Evidence: the full JSON/CSV/hash audit, `report_generation.log`, `rebuilt_report.md` and the `cmp` check.

## Publication readiness and remaining editorial points

**The seven amendment drafts, procedure and governance are substantively ready.** Each of the seven draft amendments contains the correct current evaluator and configuration SHA; the quoted conditional calibration rates agree with the audited outputs. Governance and the procedure now agree on the previously disputed strict override, while the procedure explicitly describes the no-data exception before clock validation. Verification: current draft reads, seven configuration-hash checks in `audit.txt`, and the fresh no-clock all-flagged input-suite case.

Complete the publication dates and dated governance filenames, resolve the governance table's remaining “final version, SHA-256 to be listed” reference, and refresh document hashes after those editorial changes. Preserve the reviewed evaluator bytes and their actual version/provenance; changing its version string would itself change the locked hash. These are release-packaging tasks, not grounds for another scientific redesign.

Two nonblocking editorial/diagnostic details remain:

- The procedure introduction still cites log items **70–86**, although its body correctly cites the later fixes and calibrations. Update the introductory pointer through item 93 and optionally include the rc3/rc4 review links. Verification: procedure introductory paragraph versus its version table and decisions 91/93.
- Empty usable flux arrays still produce NumPy's “Mean of empty slice” warning during normalisation. The fresh all-flagged/nonfinite probes nevertheless exit successfully and write the correct INSUFFICIENT result. This is cosmetic stderr noise, not the previous crash or a false positive. Verification: `stale_probe.log` and `additional_audit.log`. It need not trigger another evaluator change before release.

The existing caveats must remain: the procedure is an amended operational test; the design-selection overrides and parity-matched injections are disclosed; duration compatibility is an uncalibrated score rule; simulation rates are conditional on already-seen sectors; and the seven-test family-wise false-RECOVERED rate is not calibrated. These limitations remain stated in procedure §§1, 4–7. This focused review finds no additional reason to block publication with those qualifications.

## Limits

I did not rerun all 1,080 injections, repeat the original clock derivation, re-audit every historical protocol claim or re-inventory all scratch photometry. I audited every supplied rc4 result JSON, both complete CSVs, the code/runner diffs and locks, regenerated the report, and executed the requested suites and independent probes. Stored hashes demonstrate supplied provenance consistency, not an immutable external proof of chronology or of the authors' non-examination attestation. I did not publish, contact anyone, run the declared-test clock command, or open/download S106-or-later photometry/cutouts for any of the seven protected targets. Only this report was edited in the project; temporary files are under `/tmp`.

## Final requested round — release-readiness recheck, 2026-10-20

**The approval of the scoring procedure stands. Publish the package after refreshing two stale document hashes in the manifest and completing the already identified publication-date/filename finalisation. No new scientific or evaluator defect was found.** This addendum records the current package state; the earlier statement that all 78 manifest entries matched was correct at the initial rc4 review, before the subsequent editorial changes.

I compared the current files against `/tmp/conformance_rc4_review/start_hashes.json`. Only the decision log and the two draft documents changed among those snapshotted inputs. Reversing the procedure introduction's added review references and revised log range reconstructs its exact reviewed rc4 SHA. Reversing the governance row's replacement of its SHA placeholder with the actual rc4 evaluator SHA likewise reconstructs its exact reviewed SHA. Thus both document changes are precisely the previously requested editorial finalisation, without changes to their scoring specifications. Decision 94 records these edits. Verification: `/tmp/conformance_final_review/audit.py`, `audit.txt`, and direct reads of the current document passages and log tail.

### One package correction still required

`results/conformance_v21/README.md` retains the pre-edit hashes for these two files. The other **76 of 78** entries match their files. Replace the two manifest entries with the following hashes **for the current bytes**:

| File | Current correct SHA-256 |
|---|---|
| `results/CONFORMANCE_PROCEDURE_v2.1_DRAFT.md` | `b085e532004ba065cef0aa7219929ebf2df302e0fe95499a2c09cc0871f30792` |
| `results/GOVERNANCE_S106_TESTS_DRAFT.md` | `4074fdf2eb55264825aa05e53c7797f6b6aac85a1d1b4e2d1984a79bd1d9cfcc` |

The currently recorded, obsolete hashes begin `141e4f4f…` and `e04c9afb…`, respectively. Verification: fresh `hashlib.sha256` calculations for every manifest entry, saved in `/tmp/conformance_final_review/manifest_mismatches.json`. If dates, filenames or text are changed again for publication, recalculate from the final files instead of copying these intermediate hashes. This is the routine manifest refresh already required in the original rc4 report; it does not require changing the evaluator or recalibrating its unchanged scoring calculations.

### Checks reconfirmed

- The evaluator remains **a864b07ace8d3220a2d94a60513a488c8a5d87b54f41ebf510ff40ef1755311f**. Its test runners, seven configurations and amendment draft are unchanged from the initial rc4 review. All seven evaluator locks, actual prediction-CSV hashes, ephemeris-recorded CSV hashes and amendment configuration hashes still agree. Verification: the snapshot comparison and seven `LOCKS` rows in the fresh audit.
- I re-read all **1,080** rc4 result JSONs: every evaluator SHA is correct, every outcome matches its CSV row, and only the previously declared nine target/sector pairs occur. The rc4 calibration CSV remains byte-identical to rc3; the totals remain 714 AMBIGUOUS, 167 RECOVERED, 111 INCONSISTENT, 46 EXCLUDED and 42 INSUFFICIENT. All 360 clock-bearing results still have empty warnings. Verification: `/tmp/conformance_final_review/audit.py/.txt`, reading only result metadata and prediction/calibration CSVs.
- The obsolete governance SHA placeholder is now filled correctly and the procedure introduction now points through decision 93 and the four reviews. The seven amendments retain their explicitly pending `<date>` and dated governance-filename fields. Verification: direct text reads and the exact reverse-edit hash comparisons above.

I did not repeat the unchanged numerical suites: the initial rc4 review's 15/15 logic and 35/35 input results, plus the deliberate-crash and stale-result rejection checks, remain the relevant executions for the identical code. This round independently rechecked package integrity and provenance; it did not add a new empirical performance experiment. No protected S106-or-later photometry was accessed. I changed only this review report; the manifest corrections are listed for the release preparer and were not applied by the reviewer.
