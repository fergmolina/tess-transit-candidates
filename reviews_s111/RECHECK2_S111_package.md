> Public copy (2026-10-25 (v1.19)): 6 local temporary paths replaced by "[reviewer temporary path redacted]"; reviewer runtime paths likewise. No other change.

# Focused second re-check: S111+ package v1.19d

Date: 2026-10-25 UTC. Reviewer: Codex, same reviewer as `results/RECHECK_S111_package.md`. Instructions: `results/PROMPT_recheck2_S111_package.txt`. Sources opened: current source, DECISIONS 197, locked config JSONs, saved reference/prediction records, amended registrations, saved S108 v2 metadata and artificial test fixtures. No real photometry of any star, live archive query, live selection/acquisition, credential or publication action was used.

## Verdict

**Publish after one remaining implementation fix: serialize and atomically commit ledger appends.** R1–R5 are corrected for the tested sequential histories. Fresh suites pass **196/196** and **182/182**, and all config/hash, prediction-byte and registration-prefix checks pass. The explicitly requested concurrent-append probe nevertheless demonstrates that an append validated against an old ledger state can be committed after another writer, fail replay, and leave the live ledger invalid. This is a reproducible failure of the new transactional guarantee, not evidence of an accepted incorrect scientific outcome. Fix that narrowly scoped issue and re-check the append transaction; no changes to the scientific evaluators, frozen predictions, primary sectors or product policy are required.

## R1–R5 status and independent probe results

| Item | Status | Verification |
|---|---|---|
| **R1: unresolved evidence after certification** | **Fixed.** | `s111_ledger.py:96–116` withdraws certification and clears its clean-check history when a subsequent check is unresolved. Re-running `amb_after_cert_route` now returns exit 2, “route is UNRESOLVED”; `acquire_after_amb` refuses without writing. A further qualifying selection resolves the state to SPOC. The supplied suite also checks both AMBIGUOUS and unusable-date cases, followed by a new two-check certification. Sources: `[reviewer temporary path redacted]`, `extra/results.json`, fresh `tests.log`. |
| **R2: pre-designation evidence** | **Fixed.** | `s111_ledger.py:151–163` buffers checks and replays them in ledger order when the first complete designation fixes the cutoffs. The former `prior_spoc_ignored` history now refuses QLP because the route is SPOC; `prior_qlp_ignored` now refuses UNAVAILABLE because a qualifying QLP release exists. An additional sequence of SPOC check → PENDING snapshot → QLP check → DESIGNATED snapshot → later SPOC check preserved both first qualifying record hashes and chose SPOC. Sources: `probes/results.json`, `extra/results.json`. |
| **R3: secondary-role finality bypass** | **Fixed.** | `s111_ledger.py:177–182` requires a secondary acquisition to be the other product and to reference its SELECTED record in the ledger, with matching filename/URI. The former same-product secondary QLP acquisition now refuses with the specific “other product” reason. A later qualifying SPOC check can then choose SPOC because that QLP acquisition was **not accepted**; this is the correct outcome, not a remaining bypass. A separate accepted QLP record acquisition finalized fallback; a later genuine secondary SPOC acquisition was accepted without changing `QLP_FALLBACK_FINAL`. Sources: `probes.log`, `extra/results.json`; supplied R3 tests. |
| **R4: malformed metadata and sequential rollback** | **Fixed for the original cases; concurrent commit remains open below.** | `mjd_utc():55–61` checks finiteness and range; the previous positive-infinity check is now retained as unusable and gives UNRESOLVED after the cutoff, with no crash. This is an accepted metadata observation, so unchanged ledger bytes are not expected for that particular case. The new supplied tests show out-of-range dates are unresolved and invalid JSON/rule-refused appends leave the live ledger bytes and record listing unchanged. A real mocked HTTP-200 empty-body snapshot now returns PENDING with “empty body,” rather than KeyError (`target_list_designation.py:120–122`). Sources: `probes/results.json`, `extra/results.json`, `tests.log`. |
| **R5: stale/conflicting wording** | **Fixed for the requested text.** | The generator opening now refers to the operative rule string instead of the old one-NONE/selection-by-deadline rule (`make_configs_s111.py:1–15`). Its rule explicitly handles post-certification UNRESOLVED and pre-designation checks (`:42–45`); the monitoring paragraph discloses missed/replaced-product evidence limitations (`:56–58`). The ledger docstring now says unresolved evidence withdraws certification until resolution (`s111_ledger.py:25–31`). Current configs and appended amendments carry the revised text; DECISIONS 197 records the changes. |

The old HTTP503/HTML200, missing-v1/present-v2, DDT-context failure and acquisition-before-designation probes were also rerun against current production functions. They retain the intended PENDING/designation/refusal behavior (`[reviewer temporary path redacted]`). No further contrary sequential history was found in the scoped additional probes.

## Remaining finding: candidate validation and commit are not one transaction

**Required fix before publication.** `s111_ledger.py:213–218` copies the live ledger, validates a candidate append, deletes the candidate, then calls `_write_entry()` again on the live ledger and original record path. There is no serialization or comparison-and-swap against the state that was validated. The second call also recopies the source record rather than committing the exact validated bytes (`:196–206`).

I reproduced the following deterministic two-writer interleaving using the production `append()` function and a temporary hook only at the live-commit boundary; no project code was edited:

1. The live ledger contains a valid designation dated **2026-12-24T12:00Z**.
2. Writer A validates a QLP check dated **December 25**, then pauses before its live write.
3. Writer B completes a valid production append dated **December 26**.
4. Writer A resumes. It re-reads the new live ledger, appends December 25 after December 26, and only then runs replay.
5. A raises `LedgerError: entry 3: event time earlier than the previous entry`. Its invalid entry remains written; a separate replay fails with the same error.

Evidence: `[reviewer temporary path redacted]`, `extra/results.json`, fields `race_A`, `race_state` and `race_events`. The retained event sequence is `[init, 2026-12-24, 2026-12-26, 2026-12-25]`. This is a controlled scheduling of a possible concurrent interleaving, not a probabilistic stress test. The parent reviewer independently reproduced the same failure with different dates. Neither probe opened real flux.

The final validator remains fail-closed: this corrupt ledger does **not** produce a valid outcome. The defect is that a failed append mutates an allegedly append-only, replayable provenance record and requires repair. Consequently DECISIONS 197's unconditional “refused appends leave the ledger bytes unchanged” remains too strong for concurrent writers.

**Exact fix:** acquire an exclusive per-ledger writer lock before reading/copying the history and hold it through candidate validation and commit. Stage the source record once; validate and commit those same bytes. Commit record and ledger state so any refusal/interruption leaves the previous valid history usable, and concurrent readers cannot observe a committed entry referring to incomplete record bytes. An equivalent correctly implemented atomic state/version check is acceptable. Merely re-running replay after the live append is insufficient. Add a deterministic interleaving test asserting that one operation waits or refuses safely, the final history replays, and no refused entry remains. Also check that changing the original source record after staging cannot change the committed bytes. Update hashes/locks and the associated amendment references after fixing the implementation.

This does not require an authentication system for arbitrary forged local files, and does not require making the scientific evaluator concurrent. It is the requested integrity contract of the new append operation.

## Integrity and fresh tests

Independent `[reviewer temporary path redacted]` and `audit.json` confirm:

- All **14** config hashes, prediction hashes, named code hashes, QLP prior hashes and the QLP evaluator hash match their current locks.
- Both amended registrations start with their complete published registration bytes. Both frozen v2 prediction CSVs are byte-identical to the published copies and match their ephemeris hashes.
- References remain **726 ppm / 2.2 h** and **830 ppm / 2.2 h** from the saved report JSONs, with S111 the permanent primary and sector lists S111–114 / S111–113.
- The S108 v2 demo re-derives exactly from saved metadata, including its end and +120/+365-day cutoffs. The actual rc4→SPOC source diff still equals the archived diff.

Reviewed lock SHA-256 values:

- QLP: `3545a827b319115059456f2cf95e2359a4f873c3b4936c67014ae4605cedd932`
- SPOC: `9b0095f6d47263f7d92fc25edf988ae4529f03dcfb2fbcfc2fb41612b4fdc10f`

Fresh synthetic suites: **196/196** (`[reviewer temporary path redacted]`) and **182/182** (`qlptests.log`). I inspected the current test sources, then used temporary interpreter-only copies with bundled Python `[reviewer runtime path redacted]`, `-B -I`, and `[reviewer temporary path redacted]` to expose existing installed packages. Child Python invocations also used `-B`; all fixtures, outputs and caches were under `/tmp`. Production scripts/configs were unchanged. Thus these are fresh assertions under an adapted runtime, not an unchanged-project-venv execution.

The two identifiable QLP validation outputs plus their matching artifacts remain sufficient as described in DECISIONS 197; a new combined receipt format is not required. The v01-only limitation remains explicitly disclosed. Neither issue needs another redesign for this re-check.

## Limits

No real photometry, clock calculation, live metadata fetch, archive availability authentication, live selection/acquisition, or scientific calibration was performed. Saved JSON/CSV values were verified as records, not re-derived from real light curves. Passing synthetic tests establish the tested transitions and integrity checks, not exhaustive correctness. Within the requested scope, the append transaction is the sole remaining publication blocker; a focused fix and re-check are sufficient.
