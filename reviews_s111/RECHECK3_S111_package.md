> Public copy (2026-10-25 (v1.19)): 5 local temporary paths replaced by "[reviewer temporary path redacted]"; reviewer runtime paths likewise. No other change.

# Focused third re-check: S111+ package v1.19e

Date: 2026-10-25 UTC. Reviewer: Codex, same reviewer as `results/RECHECK2_S111_package.md`. Scope: `results/PROMPT_recheck3_S111_package.txt` — append transaction and affected integrity records only. Sources opened: current and archived ledger source, current tests, DECISIONS 198, locks/configs, registration/prediction records, and artificial fixtures. No real photometry of any star, live archive query, live selection/acquisition, credential or publication action was used.

## Verdict

**Publish as v1.19.** The sole remaining blocker from the second re-check is resolved. Fresh actual two-process probes show that writers serialize, a stale earlier event is refused without being committed, and changing the original source after staging cannot alter the committed record. Reader-boundary and interruption probes preserve a valid history and recover the unreferenced record at the next append. The fresh supplied suite passes **209/209**. All affected code/config/lock hashes and registration-prefix checks pass. This is approval of the reviewed package, not authorization to access test photometry or a claim of real-data calibration.

## Findings and verification

| Check | Result | Evidence |
|---|---|---|
| Two writers / previous `race_A` failure | **Resolved.** | `s111_ledger.py:226` acquires an exclusive per-ledger `flock` before staging/history access, and releases it only in `finally` at `:253–254`. Independent real subprocess tests paused A after staging while holding the lock, then started B. Both remained running until A was released. With A dated Dec 25 and B Dec 26, both committed in order. With A dated Dec 26 and B Dec 25, B refused with “event time earlier than the previous entry”; only A's entry was present and final replay succeeded. `[reviewer temporary path redacted]`, `probes/results.json`, `later_second` and `earlier_second`. |
| Exact staged bytes | **Pass.** | After detecting A's staged file, I changed A's original source timestamp by 30 days before releasing the pause. In both writer-order cases, the committed record hash matched the original staged bytes, not the changed source. The source is copied once at `:229–232`; candidate validation uses that copy at `:241`, and commit copies the candidate record at `:250`. Same independent probe output. |
| Reader atomicity | **Pass at the requested commit boundary.** | At the point immediately before `os.replace` of `ledger.jsonl`, an independent replay still read the old valid history, while the new record already existed complete and hash-matched. After replacement, the new history replayed. This follows the record-rename-before-ledger-replacement order at `:249–251`; the controlled reader probe is `probes/results.json`, `reader_commit`. No entry exposed by this sequence refers to an incomplete record. |
| Interruption between record rename and ledger replacement | **Pass.** | I injected an `OSError` exactly at the final ledger replacement. The old ledger bytes were unchanged and replayable; the complete new record was unreferenced. Retrying the append replaced that leftover under the lock and succeeded, with the expected record hash and valid final history. Cleanup/replacement code: `:244–251`. Probe: `interruption` in the same results JSON. |
| Test hook unset | **Pass.** | The hook is an explicit environment-variable branch at `:234–236`; when absent, no wait occurs. The reviewer process had it unset, and independent normal/interruption-retry appends completed without it. Only the controlled writer-A subprocesses received the variable. The hook delays a transaction while retaining the lock; it does not bypass validation. |
| Scope of source change | **Pass.** | AST comparison with `results/conformance_s111/superseded_v1.19a/s111_ledger_v1.19d.py` found only `_write_entry` and `append` changed, `_referenced` added, and no functions removed. Replay/state functions are unchanged. Verification: `[reviewer temporary path redacted]`; independent `ast.dump(..., include_attributes=False)` comparison. |

No further blocking finding was found within this focused scope. There is no need to change the product policy, scientific evaluators, frozen prediction values or primary sectors.

## Integrity

Fresh `hashlib`/byte-prefix checks (`[reviewer temporary path redacted]`, `audit.json`, `diff_integrity.json`) confirm all **14** current config hashes, their prediction and named-code hashes, QLP prior hashes and evaluator hash match the locks. Both amended registrations preserve their complete published copies as exact prefixes and name both new lock-hash prefixes. Both frozen v2 CSVs remain byte-identical to their published copies and match the ephemeris hashes.

Reviewed hashes:

- `scripts/s111_ledger.py`: `16b987ac0cc8b11616566d1107485ace7b2c283c9214cd12809de327d9519100`
- QLP lock: `d3f2d0ed93e7db2cd1378f3fb3a40e4f3c6639b084d9032a6af7cdefb400ecf6`
- SPOC lock: `a88d676e745d247f6b25bf85152935a02e32e184a990b0eed2c4429ce7d151d6`

The current registration amendments refer to these locks. DECISIONS 198 records the transaction change and corrects the earlier unconditional claim about failed concurrent appends; the code and tested behavior now support that correction for cooperating writers using this append function.

## Tests and limits

I inspected and freshly ran the supplied `test_s111_lock.py`, including section T: **209/209 passed** (`[reviewer temporary path redacted]`). The temporary test copy changed only interpreter invocation to bundled Python `[reviewer runtime path redacted]`, with `-B -I` and `[reviewer temporary path redacted]` supplying existing installed packages. Child Python calls also used `-B`; all fixtures/caches/results were under `/tmp`. Production scripts/configs were unchanged. The independent transaction probes above used production append/replay functions and actual writer subprocesses; the interruption/reader boundaries were controlled in temporary probe code.

The unchanged QLP suite's prior fresh **182/182** result was not rerun in this narrow transaction review; its current lock/config/code integrity was checked afresh. No real photometry, scientific calibration, clock recalculation or live archive behavior was tested.

The atomicity assessment concerns ordinary cooperating processes and the specified interruption after record rename, before ledger replacement. It is not a claim of power-loss durability, protection against arbitrary external edits, or exhaustive recovery from every disk/storage failure. Recovery was demonstrated for the interrupted record slot reused by the next append. These limits do not reopen the resolved publication blocker.
