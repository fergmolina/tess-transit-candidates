> Public copy (2026-10-25 (v1.19)): 5 local temporary paths replaced by "[reviewer temporary path redacted]"; reviewer runtime paths likewise. No other change.

# S111+ package v1.19b: independent re-check

Date: 2026-10-25 UTC. Reviewer: Codex, same reviewer as `results/REVIEW_S111_package.md`. Instructions: `results/PROMPT_recheck_S111_package.txt`. Sources actually opened: current scripts, configs/locks, DECISIONS 193–196, registrations and saved prediction/reference JSONs, saved S108 v2 metadata demo, and artificial fixtures. No real photometry of any star was opened or downloaded; no live archive query, select/acquire command, publication or credential access occurred.

## Verdict

**Publish after listed changes; do not publish this assembly yet.** The rebuild substantially fixes the previous metadata and binding defects, and both fresh supplied suites pass. The new ledger correctly preserves the first designation, validates ordinary record bytes and rejects acquisition before designation. However, three replay paths still contradict the adopted policy: unresolved evidence can be ignored after fallback certification, qualifying records before designation are discarded from route decisions, and a same-product acquisition labelled “secondary” permits a subsequent product switch after flux access. Malformed release metadata can also leave a failed append permanently written. These are specific, repairable state/validation problems; the scientific evaluators, reference values and frozen predictions need no change. Evidence below comes from current source and new synthetic runs, not the authors' test summaries.

## Status of the previous findings

| Previous finding | Status | Independently verified evidence |
|---|---|---|
| S111-1, failed metadata → unlisted | **Substantially fixed; small failure-handling gap remains.** | Real `snapshot()` with mocked HTTP 503 now yields PENDING; HTML HTTP 200 yields PENDING. Required versions are checked individually (`target_list_designation.py:115–126`). DDT/CTL failures are deliberately nonblocking because those files are now context, consistent with DECISIONS 193(a). An empty HTTP-200 list still crashes instead of producing PENDING; see R4. |
| S111-2, version/DDT scope | **Fixed within the expressly bounded policy.** | All v1–v9 URLs are probed (`target_list_designation.py:74–75`); a v1=404/v2=200 fixture now finds the TIC and designates SPOC. CTL-only membership no longer changes the choice. Generator `:30–36` and config text explicitly disclose that versions above 9 are not discovered. This is an honest bounded inventory, not proof of exhaustive archive completeness. DECISIONS 193(a,c) supplies the refined sector-only/first-complete-snapshot policy. |
| S111-3, fallback/history/finality | **Partial.** | Two clean checks less than seven days apart do not certify; a late check with a timely MAST release does select SPOC; a qualifying post-designation selection cannot be displaced by later NONE; final UNAVAILABLE blocks acquisition and outcome validation. Fresh supplied histories exercise these. R1–R3 identify remaining contrary histories. |
| S111-4, sequencing/operative decision | **Substantially fixed; role/history loopholes remain.** | Independent pre-designation acquisition attempt is refused with “acquisition before the operative designation,” and ledger bytes are restored. Later snapshots cannot replace the first DESIGNATED snapshot (`s111_ledger.py:104–110`); the fresh suite verifies that. Config, code, prediction, acquired-file and result hashes are bound. R2–R3 address information already retained and acquisition-role finality. |
| S111-5, wrong-reason output/config test | **Fixed.** | Current `test_s111_lock.py:185–190` builds a consistent S112 chain and asserts the specific “output was made from a different config” refusal. The fresh run passes. Current negative cases check reason text as well as refusal; this does not substitute for the additional histories below. |

## Remaining findings and exact fixes

### R1 — major: uncertified information is ignored after certification, before finality

At `s111_ledger.py:126–129`, an AMBIGUOUS/INCOMPLETE check clears the clean-check history but deliberately preserves `QLP_FALLBACK_CERTIFIED`. This contradicts DECISIONS 194(b), `logs/DECISIONS.md:1902–1905`, and the current config clause generated at `make_configs_s111.py:42`: unresolved checks after the cutoff leave the product unresolved until a later complete check. Only acquisition makes fallback final under 194(a).

Independent reproduction, TIC80387959/S111, artificial end 2026-12-22T12:00Z: NONE at cutoff+1 d and +9 d certified fallback; AMBIGUOUS at +10 d was accepted and the production route validator still returned **BOUND QLP_FALLBACK_CERTIFIED**. A QLP selection at +11 d and record acquisition at +12 d then yielded **QLP_FALLBACK_FINAL**. No photometry was needed for these metadata/acquisition-record probes. Evidence: `[reviewer temporary path redacted]`, `probes/results.json`, cases `amb_after_cert_route` and `acquire_after_amb`.

**Fix:** before a final acquisition, an unresolved SPOC check must invalidate certification, set UNRESOLVED and prevent acquisition until a qualifying SPOC selection or a new valid two-check certification resolves it. Preserve the final-acquisition exception already adopted. Remove the contradictory “does not reopen it” sentence from the ledger docstring (`:24–26`) and align tests/configs with the adopted rule. Test both AMBIGUOUS and INCOMPLETE after certification.

### R2 — major: qualifying checks retained before designation are forgotten

`replay()` records pre-designation SPOC and QLP checks but skips their route/release implications (`s111_ledger.py:111–112,131–134`). On the first operative designation it does not reconsider those records. Metadata surveillance before designation is allowed; ignoring its evidence is not consistent with “any retained check” and the first qualifying release rule in DECISIONS 193(b) and generator `:38–43`.

My fresh histories put a qualifying selection at end+1 d, then the operative designation at end+2 d. For SPOC designation, two subsequent NONE checks certified QLP despite that retained timely SPOC selection (**BOUND QLP_FALLBACK_CERTIFIED**). For QLP designation, a later NONE check after +365 d allowed **UNAVAILABLE** despite the retained qualifying QLP selection. Evidence: `probes/results.json`, `prior_spoc_ignored` and `prior_qlp_ignored`. All entries were appended through the actual ledger CLI in chronological order.

**Fix:** retain candidate selection history independently of designation. When the first designation fixes the cutoffs, evaluate all earlier retained checks for that TIC/sector against them and choose the first qualifying record. Preserve its release identity thereafter. Alternatively a newly adopted rule could prohibit pre-designation selection records altogether, but silently accepting and discarding them is not the present declared rule. Add both histories to the suite.

### R3 — major: a “secondary” label bypasses finality after QLP acquisition

The ledger docstring describes secondary acquisitions as “the other product” (`s111_ledger.py:31–32`), but code `:145–155` checks product/selection and makes fallback final only inside `role == 'record'`. The secondary branch permits the current route's own product, without its selection binding.

Independent history: certify fallback; retain qualifying QLP selection; append QLP acquisition with `--role secondary`; then append a qualifying timely-release SPOC check. The acquisition passed, fallback remained certified, and the later validator returned **BOUND route SPOC**, after recorded QLP flux acquisition. Evidence: `probes/results.json`, `secondary_same_product_acq` and `secondary_then_spoc_route`. This conflicts with DECISIONS 194(a)'s finality “when QLP flux is acquired under it.” It is an ordinary permitted CLI role choice, not an allegation of fabricated archive records.

**Fix:** reject a secondary acquisition of the route's own product, or make any such QLP acquisition under certified fallback finalize that fallback and bind the selected artifact. Define and enforce secondary acquisitions consistently, including their identity/selection provenance, so changing a label cannot preserve discretion after flux access. Keep genuine opposite-product readouts explicitly secondary. Add a role-mislabel test and verify that no accepted QLP acquisition under fallback permits later promotion of SPOC.

### R4 — required robustness fix: malformed metadata can leave a broken ledger

`mjd_utc()` rejects NaN/nonpositive values but not positive infinity or out-of-range values (`s111_ledger.py:49–53`). A SELECTED record with `t_obs_release='inf'` raised `OverflowError`. `append()` had already written the line and copied the record before replay; it rolls back only `LedgerError` (`:171–187`). I compared bytes before/after: **the failed append remained written**, and subsequent replay still raised. Evidence: `probes/results.json`, `infinite_release_append`, `infinite_release_rollback=false`, `infinite_release_state`. This violates the advertised “refused and not written” contract and can force manual repair of supposedly append-only history.

Separately, real mocked `snapshot()` receiving HTTP 200 with an empty target-list body raised **KeyError(None)** at `target_list_designation.py:120`: `save():66–68` records `file=None`, which derive then indexes. `snapshot.json` exists but `designation.json` does not (`[reviewer temporary path redacted]`). This fails closed rather than falsely designating, but does not produce the promised retained PENDING record.

**Fix:** require a finite, representable release MJD and classify unusable dates as unresolved/refused without crashing. Validate a proposed append against a temporary candidate history before committing it, or guarantee rollback for all expected input/parsing failures. Preserve the existing valid ledger bytes on refusal. Treat HTTP-200 empty/missing bodies as malformed/PENDING explicitly. Test infinity, an out-of-range finite date, empty-body HTTP 200, and byte-exact rollback. These fixes do not alter the policy or scientific thresholds.

### R5 — wording corrections required alongside the code

- The generator's active opening documentation (`make_configs_s111.py:7–11`) still describes DDT-inclusive listing, selection **by** +120 d, and one NONE record after the cutoff. Replace it with the current sector-only, release-date, two-check/ledger rule. The generated policy string is more current than its docstring; both are publication material.
- The ledger docstring simultaneously says no unresolved check “between or after” the two clean checks (`s111_ledger.py:22–24`) and says unresolved evidence after certification does not reopen it (`:25–26`). Resolve this in favour of the adopted policy in R1.
- “A missed check delays but does not change the route” (`make_configs_s111.py:54–55`, copied to configs/amendments) is too absolute. The policy deliberately finalizes on acquisition, and an earlier replaced release may not appear in a later check; release timestamps do not eliminate that limitation. Suggested replacement: **“These are periodic recorded checks. A later check can recognize a timely release if it remains listed and its release date is usable. Missed checks or replaced products can change the evidence retained; earlier replaced deliveries cannot be excluded. The declared ledger finality rules still apply.”** This is a limitation of the adopted observable-evidence rule, not a demand for continuous monitoring.

## Passing integrity, receipts and reproduction

**Fresh supplied tests:** 162/162 S111 tests and 182/182 QLP-lock tests passed (`[reviewer temporary path redacted]`, `qlptests.log`). After source inspection, I ran temporary interpreter-only adaptations using bundled Python `[reviewer runtime path redacted]`, `-B -I`, and `[reviewer temporary path redacted]` to expose the existing project packages. Child Python calls also used `-B`; outputs/caches were confined to `/tmp`. Production scripts/configs were unchanged. These are fresh runs of the assertions with an adapted runtime, not a claim that the project venv ran unchanged.

The independent prior-probe reruns use the real production `snapshot()` with mocked fetch/time, and real ledger/validator CLI calls with synthetic metadata. HTTP503 and HTML200 now give PENDING; missing v1 does not hide v2; CTL HTTP503 is correctly nonblocking under the revised scope. Acquisition before designation is refused with byte-exact rollback. The supplied histories additionally demonstrate first-snapshot retention, two-check spacing, qualifying release-date treatment, a finalized fallback remaining final, refusal after UNAVAILABLE, record/hash tampering refusal and consistent output binding. All observations above are specific to the tested histories; R1–R4 explain why passing totals are not exhaustive validation.

A fresh metadata/hash audit (`[reviewer temporary path redacted]`, `audit.json`) verified:

- All **14** config hashes, named code/prediction hashes, QLP prior hashes and evaluator hash match the current locks. QLP lock: `3f2000a626a8245d16a501e2d0e5a41a2ab85855386a8ff73327f2abe59b1cfc`; SPOC: `f3a1bc7bcbae5856ca7dfe43eda059e4897ca5e7e269c407700f917321637caa`.
- Both amended v2 registrations preserve their entire published copies as exact prefixes. Both v2 prediction CSVs equal their public copies and match the ephemeris hashes. References still reproduce as **726 ppm / 2.2 h** and **830 ppm / 2.2 h** from saved report JSONs; S111 remains the sole primary and sector lists remain S111–114 / S111–113.
- The saved S108 v2 demo re-derives exactly: TIC317134140 SPOC, TIC24526743 QLP, end 2026-10-04T20:30Z, +120 d 2027-02-01T20:30Z, +365 d 2027-10-04T20:30Z. It explicitly records v1–v9 scope. This is saved-metadata consistency, not a new live archive completeness check.
- The actual rc4→SPOC diff still equals the saved variant diff. Neither statistical evaluator requires a science change to address this report.

**QLP receipt:** a new combined receipt format is not intrinsically required. The proposed bundle can retain both validators' successful outputs, their commands and the exact input artifacts: the same config, light curve, evaluator JSON and clock record, plus the ledger at its validated tip and relevant lock/code hashes. `validate_s111_inputs.py:14–17,56–71` explicitly requires the second gate; `validate_round4_inputs.py` supplies clock/output binding. Two detached “BOUND” strings without identifiable matching artifacts would be inadequate, but that is different from demanding a new file format. The current v01-only statement in `make_configs_s111.py:81–85` and amendments is adequate: a v02-only listing is not an eligible release of record and may end UNAVAILABLE even though some QLP data exist.

## Limits and next step

I did not read real FITS/flux, recalculate clocks, execute live `select`/`acquire`, authenticate archive availability, or rerun scientific calibration. The no-photometry restriction applies even to training stars. I did not claim that local hash chains authenticate the origin of arbitrary manually forged files; the demonstrated problems occur with internally consistent records and ordinary documented CLI operations. No new requirement to change frozen predictions, primary sectors or statistical thresholds follows.

Correct R1–R4 and the associated wording, retain the superseded unpublished package, regenerate the affected code/config/lock references, and run a focused synthetic re-check. The original scientific data and published registration prefixes should remain intact. This verdict does not authorize test-data access or publication.
