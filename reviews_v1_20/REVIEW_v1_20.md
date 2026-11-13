> Public copy (2026-11-13 (v1.20)): 2 local temporary paths replaced by "[reviewer temporary path redacted]". No other change. This review covers the FIRST assembly of v1.20, which was not published; the published v1.20 is the rebuild that applies F1-F4.

# Pre-publication review of v1.20

**Date:** 2026-11-13 (America/New_York). **Reviewer/tool:** OpenAI Codex. **Instructions:** `results/PROMPT_review_v1_20.txt`.

**Sources opened:** the named local source, locks/config, selection/acquisition/result JSONs, run and precheck logs, release Markdown, calibration diagnostics, saved training-output JSONs, local Git tags v1.18/v1.19.2, and the assembled working tree. The S108 FITS was read **only to compute SHA-256 and by the expressly permitted validator, which hashes it**; its headers/arrays were not independently opened. No scorer, photometry analysis, download, live archive query, assembler, publication or credential operation was performed. Only this report was written in the project; temporary audit code/output is under `[reviewer temporary path redacted]`.

## Verdict: fix first

The recorded outcome **PARTIAL is correct under the locked decision rules**, all three validator stages pass independently, and the exact assembled bytes pass the manifest and preservation checks. I found no incorrect reported measurement or changed frozen scientific artifact. Before publication, make the bounded wording and reproduction-instruction corrections below. They do not require rescoring, changing the outcome, explaining the ineligible events through new analysis, or changing any lock. Each release edit requires a rebuilt manifest and new reviewed hashes. The current `CITATION.cff` date is valid only for publication on **2026-11-13 UTC**; if publication occurs later, set the actual UTC release date and rebuild/recheck the affected hashes.

## Required publication corrections

Paths in this table are relative to `public_release/` unless explicitly prefixed otherwise. `RESULT` denotes `scoring_317134140_s108_s110/results/S108/RESULT_S108.md`; its local source is `results/test_317134140/S108/RESULT_S108.md`.

| ID | Finding and evidence | Exact correction |
|---|---|---|
| F1 — interpretation | README lines 260–261 actively reaffirm that S108–S110 “decide the case.” The actual lock permits PARTIAL, INCONCLUSIVE, INSUFFICIENT and unavailable outcomes and supplies no combined decision rule establishing the astrophysical case. RESULT lines 27–28 say a prospective result “does not test” the advance expectation. A single outcome can be consistent with that qualitative expectation without calibrating it or establishing a real signal. Verification: locked scorer lines 40–47, config `scope`/`advance_expectation`, and the published calibration diagnostics. | Replace the new README's last bullet with: **“Unchanged: every lock, config, scorer and prediction file. One of three sectors has been scored: PARTIAL, neither PASS nor FAIL. Sectors 109 and 110 remain separate prospective tests; their outcomes may also be inconclusive and do not by themselves identify the host or validate a planet.”** This qualifies the historical “decide the case” sentence without changing the earlier bytes. Replace RESULT's “agrees with it and does not test it” with **“is consistent with that qualitative expectation; one outcome does not establish its frequency, calibrate its predictive accuracy, or demonstrate a real signal.”** Add a dated clarification to log item 227's proposed wording rather than silently rewriting history. |
| F2 — evidentiary scope of conduct claims | README lines 257–258, RESULT lines 64–65/74–75 and `zenodo_upload/RELEASE_NOTES_v1.20.md:15–16` state the pre-download plan, unique run and absence of other access without distinguishing author testimony from independent evidence. The saved sequence supports the account, but the current log's mtime cannot establish when item 225 was inserted; one saved run cannot prove the absence of another. Also, “opened … by nothing else” is literally too broad: the assembler hashes the FITS, as does this permitted review. Verification: file timestamps below, scorer log, and `scripts/assemble_v1_20.py`'s FITS hash operations. | Use **“The author reports recording the run plan before download and performing one acquisition and one locked scoring run. The retained records are consistent with that account; they do not independently timestamp insertion of the plan or exclude unrecorded activity. Apart from byte-integrity checks and validation, no additional photometric analysis is reported.”** Put the full distinction in RESULT and use “author-reported”/“no additional photometric analysis is reported” in the short README/release-note accounts. Preserve the original log entries with a dated qualification. This is not a finding that the reported conduct was false. |
| F3 — reproduction instructions | RESULT lines 86–93 advise adjusting embedded absolute paths to run elsewhere. Editing the scorer changes its SHA and causes its config-hash check to refuse it; editing the config's prediction path changes the config hash and causes the published validator to refuse it. The printed commands also do not state a working directory. Verification: `prereg_spoc_317134140.py:172–177`, `validate_nonclock_inputs.py:26–36`, and the current config's absolute `pred_csv`. No scorer execution was needed to establish this conflict. | Replace “adjust them to run elsewhere” with **“Exact locked reproduction requires the original absolute-path layout and unmodified scorer, helpers, config and prediction CSV. Run these commands from `scoring_317134140_s108_s110/`, supplying absolute paths to the saved selection/acquisition records and an output path that does not exist. Editing embedded paths changes the recorded hashes and will not pass the published binding checks. A portable adaptation must be documented separately as a reproduction experiment, not substituted for the outcome of record.”** Do not update the frozen hashes to make a modified reproduction pass. |
| F4 — acknowledge this review accurately | RESULT line 78 says the result has not been externally reviewed unless a review is listed in the release notes. This audit reviews the recorded result, conduct evidence and release bytes, not its extraction from flux. Verification: that sentence, current release notes, and this report's access limits. | In the rebuilt release, identify/link this report and replace that sentence with **“External review checked the recorded outcome, provenance bindings and release bytes; it did not independently rerun the S108 photometry analysis.”** Keep the separate later-reproduction distinction below. |

For F1's calibration presentation, retain all three depths as promised by the registration. The detailed table is properly qualified; the juxtaposition of 2% and 35–58% nevertheless invites informal odds. Add beside the abbreviated README/release-note frequencies: **“These are descriptive frequencies in selected training noise realizations, not a Sector 108 false-alarm probability or calibrated odds for a real signal.”** No new calibration or likelihood ratio is requested.

## 1. Conduct and binding against v1.18

I ran the **unmodified** `scripts/validate_nonclock_inputs.py` with Python 3.15, `-B -I`, the v1.18 lock/config, and the supplied records. Stages **pre, selection and result each exited 0 with BOUND**. I also ran stage result using the public copies of validator, lock, config, selection, acquisition and result: **BOUND**. Commands and outputs are retained in `pre.txt`, `selection.txt`, `result.txt` and `public_result.txt` under the temporary audit directory. The validator uses standard-library hashing/JSON; this was not a photometric rerun in a different scientific environment.

Independent byte comparison with tag v1.18 confirms the local/public scorer, two helpers, selection tool, validator, S108 config and lock are the originally published bytes. Key SHA-256 values:

| Artifact | SHA-256 |
|---|---|
| Lock | `58df364513d9d2bd3f2d0c7474d069b55737420614b10eb631cf82e4eba0db41` |
| Scorer | `f3f55c0d74733f8aa4ee6264b99c29c547990d885d5cfdd2c29c43c47baa1613` |
| Validator | `f3bca6924c16216c9bbc745b4a5b4f169e525a45417645681d72ec250dca7e01` |
| Selected/scored FITS | `cea2619b6228e770064ed39176ad446c02320311dbd3751e15cdc0876b4331a0` |

The selected name is `tess2026250081459-s0108-0000000317134140-0310-s_lc.fits`. Re-deriving the retained MAST response yields exactly **one** candidate. Its metadata size, acquisition-record size and local `stat` size all equal **2,001,600 bytes**. Selection SHA, filename/URI, acquisition SHA and result SHA chain agree. The query precedes the download and the inclusive cutoff **2027-02-01T20:30:00Z**. The result has its locked config/sector and no training-mode field; the locked scorer explicitly refuses `--insample-check` for sectors ≥108. These support the reported normal scoring path, although the scoring log itself does not echo the entire command line. Sources: the two JSON records, result JSON, scorer lines 165–177, config, and `audit.py`/`audit.json`.

### Timing evidence and limits

All file times below were converted from filesystem epochs to UTC with Python `datetime`, not interpreted from local `ls` clock displays.

| Event/evidence | UTC on 2026-11-13 |
|---|---|
| Selection query timestamp | 19:54:28.012085 |
| Selection JSON birth / mtime | 19:54:46.090577 / 19:54:46.090972 |
| Four retained training-output JSON mtimes | 19:57:29.090701–19:57:34.454249 |
| Precheck log final mtime | 19:58:29.719528 |
| Acquisition start, scoring log | 19:58:41 |
| FITS birth / mtime | 19:58:45.913552 / 19:58:47.776235 |
| Acquisition record timestamp | 19:58:47.778676 |
| Scorer start, scoring log | 19:58:52 |
| Result JSON birth / mtime | 19:58:54.323013 / 19:58:54.323253 |
| Result validation start / log final mtime | 19:58:54 / 19:58:54.517585 |
| Current local DECISIONS mtime | 20:07:43.832551 |

The record's query timestamp marks query initiation, not the later creation of the SELECTED JSON. Both precede acquisition. Item 225's minute-resolution “19:58” could precede the 19:58:41 download start, but the mutable containing log does **not** prove that insertion order. I found no immutable pre-download snapshot of that paragraph among the named materials. File times are supporting consistency evidence, not independent trusted timestamps.

The precheck log contains 196 PASS assertions and ends `196/196 passed`; I did not rerun that synthetic suite. The four scratch-directory JSONs explicitly referenced by the assembler exist and are fully equal as parsed JSON to the published `insample_v1.3b_S*.json`, including software fields. Their mtimes precede download. I read only those output JSONs, not training flux, and did not rerun them. The scorer log records one successful acquisition and one successful PARTIAL run with no exception/refusal. Historical pre/selection BOUND statements are recorded in item 224; those actual pre-download validator outputs are not separately present in the two supplied run logs. My fresh validations establish current binding, not when those earlier checks occurred. Sources: logs, source, saved JSON comparison and filesystem metadata in `audit.json`.

## 2. Monitoring and release of record

All **six S108 and five S109** local selection records match their public copies; every saved response hash and derived summary checks. From the November 1 checks onward, consecutive intervals are:

| Pair | S108 | S109 |
|---|---|---|
| Nov 1 → Nov 8 | 6 d 04:41:51.630 | 6 d 04:41:51.546 |
| Nov 8 → Nov 10 | 2 d 00:51:04.804 | 2 d 00:51:04.627 |
| Nov 10 → Nov 12 | 2 d 00:48:51.910 | 2 d 00:48:52.160 |
| Nov 12 → Nov 13 | 1 d 15:00:38.360 | 1 d 15:00:55.260 |

All are below seven days. The two rounded intervals in the new monitoring note are correct. The preceding Oct 25→Nov 1 S108 gap remains **7 d 22:27:48.471447**, already correctly disclosed in correction C1. The extra daily-monitor trigger is consistent with “at least weekly” and the selection tool's explicit monitoring-trigger description; no requirement mandates waiting for the next weekly date. Sources: `results/selection_records/317134140/S10{8,9}/*.json`, config `monitoring_rule`, `spoc_selection.py:10–16`, correction C1, and audit calculations.

The earlier-replaced-delivery caveat in RESULT lines 71–72 is adequate. Header DATE **2026-11-07** is only a provenance value copied into the result, not an archive-release timestamp. The selected observation's retained `t_obs_release=61355.0`, interpreted as MJD, corresponds to **2026-11-11 00:00 UTC**, while the Nov 12 query still returned NONE. This does not invalidate the locked first-recorded-selection rule; it demonstrates why neither header date nor release metadata establishes the first retrievable listing. I did not replay past archive inventories or verify current MAST availability.

**Small log qualification:** item 224, public DECISIONS line 2303, says “so the product was listed between those two checks.” Prefer a dated clarification: **“The retained query results changed from NONE to SELECTED between those checks; they do not establish the first public availability time.”** Do not interpret the earlier MJD as proof that the NONE query was wrong. Item 221's “nothing was learned” is scoped to its failed requests and is followed by item 222's successful retry; those entries are not contradictory. The reported TLS diagnosis and private communications were not independently authenticated in this review.

## 3. Outcome and numerical cross-check

I applied the locked predicates directly to `result_S108.json`, without loading or executing the scorer on flux:

| Quantity | Independent calculation / check |
|---|---|
| Depth / random-phase sigma | 206.33598689023813 / 54.98724022369697 ppm |
| Depth divided by sigma | 3.752433947418165 → **3.75** |
| Nominal depth ±1.96 sigma | **98.56099605179207–314.1109777286842 ppm**, correctly printed 98.6–314.1 |
| Band and eligibility | Interval overlaps [145,225]; 28≥10 eligible; 200≥100 usable shifts; sigma finite and positive |
| Clause A | **A_CONSISTENT**, neither A_LOW nor A_HIGH |
| Top-three periods / SDE | 1.1467482565 / 7.07140256; 8.0221698642 / 6.24718840; 0.9302391435 / 5.69722666 — published rounding correct |
| Clause B / aliases | None within 0.1% of 0.5718634 d; none within tolerance of P/2 or 2P; **B_NOT_TOP3**, empty aliases |
| First peak versus 2P | 2P=1.1437268 d; difference 0.00302145650836 d; fractional difference **0.264176419435%**, correctly rounded 0.26% |
| Ordered outcome | Exactly one passing clause → **PARTIAL** |
| Counts | CSV independently contains 48 S108 rows; result has 28 eligible, 20 ineligible (41.67%), 200 shifts, 11,862 retained cadences, 363 TOI-mask removals |

Sources: result JSON, scorer lines 82–126, frozen CSV and `audit.py`. Depth, sigma, BLS peaks and preprocessing counts were verified **as saved output**, not recomputed from the FITS. The header/software numbers in RESULT agree with the result's provenance/software fields; those headers were not independently inspected.

All displayed numerical values in RESULT, the new README/scoring README/registration notes and release notes agree with those sources. Calibration PARTIAL frequencies reproduce as **82/150=54.6667%**, **175/300=58.3333%**, **52/150=34.6667%**, and **107/6000=1.7833%**; the displayed 55/58/35/2% are correct. Verification: the published `calibration/calibration_diagnostics_v1.3.md` rows and arithmetic. Reporting all three depths satisfies the registration's dated calibration note. The detailed warning against transferring the frequencies to S108 is appropriate; do not turn their ratios into odds or a false-alarm estimate.

“Not a confirmation,” “neither PASS nor FAIL,” and the host/blended-binary limitation are accurate under this procedure. “Not a failure” in the release notes is clearest as **“not a FAIL under the locked rule”**: clause B did fail. The result's 20-event loss is explicitly disclosed, not concealed. The saved result contains no per-event rejection reasons, so its cause cannot be established in this permitted review. It must not be attributed to gaps, flags or masking without a separately declared diagnostic. This limitation does not change the locked count-based outcome.

## 4. Data statements, log discipline and exact bytes

The new data statement is confined to S108 of TIC317134140 and separately labels S109/S110 non-access as the authors' attestation (RESULT lines 76–77). It does not withdraw the disclosed, reportedly unopened TIC206620592 S106 cutout. I checked the October 20 erratum and correction C2 in `corrections/CORRECTION_v1.19.1_2026-11-10.md`; the old broad monitoring statement remains visibly superseded. F2 is about literal byte opening and evidentiary limits, not a new breach of the holdout. I did not authenticate universal non-examination.

Manual reading and an email/session/temp-path/known-recipient-name scan of public DECISIONS **217–227** found none of the prohibited disclosures. The orbit-table comparison has exactly one changed comment, `# Created 2026-11-07 …` → `# Created 2026-11-11 …`; all data rows match, including S111 end **2026-12-22 08:30 UTC**. Sources: the two saved monitoring CSV snapshots, public log and audit output. Historical archive/publication claims in those log items were not rechecked against remote services.

Independent Git/hash checks, not execution of the assembler, give:

- HEAD and local tag v1.19.2 resolve to **17a66414f233f8cc7326197d50db00713e495122**; no staged changes.
- Exactly **6 modified + 10 new files + the manifest**, no deletions. All **16/16** manifest entries match their actual bytes and the complete changed/new set.
- Manifest SHA: **`6dccf567dd2e5a790935d84de41c0469a70084f7b634aa26883967fb24a00a78`**. Release-notes SHA: **`2ef8377f23d74c330c35e100d602a8534df33a93491a3aa5d5255b97f78e5795`**. Both match the supplied anchors.
- All **68 prediction CSVs** match tag v1.19.2. The **194 tracked Python/config artifacts** selected for explicit byte comparison are unchanged; Git's complete changed set contains no other lock/scoring/validator change.
- Monitoring README, scoring README, registration and DECISIONS preserve their v1.19.2 blobs as exact prefixes. README differs by one insertion only; deleting that insertion recovers the old bytes exactly. CITATION changes only version and date-released.
- Local and public registrations are equal. The local result/acquisition JSONs and RESULT note equal their assembled copies.

Evidence: `git status`, `git diff`, `git show`, `hashlib`, and `[reviewer temporary path redacted]`/`audit.json`. Appending a clearly dated result note is proper: it changes neither the original registration nor its predictions and does not portray a post-result choice as a freeze. Keep that distinction in the rebuild. These passing hashes identify the **reviewed current assembly**, not approval of unchanged publication despite F1–F4.

## 5. Later independent reproduction

I recommend a later, explicitly declared **computational reproduction**, not another opportunity to select a result, and a separate eligibility diagnostic if desired. It need not precede this descriptive result release once the text is corrected. Suggested wording:

> After preserving and publishing the original outcome of record, an independent reviewer will reproduce the locked computation using the identical FITS SHA, unmodified code/config/predictions and recorded software environment, writing to a new output. Every attempt and any discrepancy will be retained. This is a reproducibility check, not a second independent observational test, and cannot silently replace the original outcome. Any inspection explaining the 20 ineligible events is a separately labelled diagnostic; it cannot change the frozen eligibility rule or outcome.

If this is done before publication instead, update the “one run/no additional analysis” wording and include both records; do not retrospectively conceal the reproduction. No such operation was performed here. The present review establishes recorded-rule consistency, provenance binding and byte integrity, with the limits stated above; it does not independently establish the measured dip from the underlying photometry.
