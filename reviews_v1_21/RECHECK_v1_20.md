> Public copy (2026-11-14 (v1.21)): 2 local temporary paths replaced by "[reviewer temporary path redacted]". No other change. This is the re-check of the rebuilt v1.20, received after the public log of v1.20 was closed.

# Focused re-check of rebuilt release v1.20

**Date:** 2026-11-13 (America/New_York). **Reviewer/tool:** OpenAI Codex. **Instructions:** `results/PROMPT_recheck_v1_20.txt`. I read the revised assembler without executing it, the revised release text, the original review, local/public records and Git baseline, and DECISIONS 229–230. This re-check used source/text and byte comparisons only; no FITS contents, scorer execution, live query, download or publication operation was involved. Only this report was written in the project; audit files are under `[reviewer temporary path redacted]`.

## Verdict: publish these bytes as v1.20

F1–F4 and the accompanying qualifications are resolved. All **18 manifest hashes** match; the exact file set, preserved prefixes, frozen artifacts and original result/acquisition bytes pass independent checks. I found no new blocking or material issue in the requested scope. No further editorial rebuild or photometric analysis is required for this assembly.

**Date condition:** this verdict assumes publication on **2026-11-13 UTC**, matching `CITATION.cff`. If publication falls on **2026-11-14 UTC**, change `date-released` to `2026-11-14`, regenerate the affected manifest/hash anchors and verify the date-only rebuild before publication. The approval of the exact hashes below does not extend to altered bytes. Scientific outputs, the November 13 result date, historical log timestamps and frozen records should not be rewritten merely because publication occurs a day later.

## Findings resolved

Paths below are relative to `public_release/` except where stated. `RESULT` means `scoring_317134140_s108_s110/results/S108/RESULT_S108.md`.

| Finding | Status | Evidence |
|---|---|---|
| F1: implication that three sectors necessarily “decide the case”; “does not test it” | **Resolved.** | README lines 266–267 expressly qualify the historical sentence and allow inconclusive outcomes without host identification or planet validation. RESULT lines 27–33 distinguish consistency with a qualitative expectation from calibrating its frequency or demonstrating a signal. DECISIONS item 229 adds the requested dated clarification of items 226–227. |
| F2: conduct claims versus independent evidence; literal “opened by nothing else” | **Resolved.** | RESULT lines 68–72 label the account author-reported and state the limits of the retained evidence. Its Limits section includes hash checks and describes the absence of further photometric analysis as reported. README lines 260–263, scoring README lines 72–73 and release notes lines 17–20 use the same qualified account. Item 229 preserves and qualifies the earlier log entries rather than silently rewriting them. |
| F3: path edits would break locked reproduction | **Resolved.** | RESULT lines 106–110 specify the original absolute-path layout, unmodified artifacts, working directory, absolute record paths and a fresh output path; they warn that editing embedded paths breaks binding and distinguish portable adaptation from the outcome of record. The assembler's replacement text agrees with the requested wording. |
| F4: identify review and its limits | **Resolved.** | RESULT lines 89–92, README line 264, scoring README line 74 and release notes lines 21–23 link the review and distinguish checks of saved outcome/bindings/bytes from an independent photometric rerun. The public review header identifies the first assembly as its subject. |
| Calibration-frequency caution | **Resolved.** | README lines 255–259 and release notes lines 12–14 contain the requested sentence denying a Sector 108 false-alarm probability or calibrated odds. Registration line 18 carries the same substantive limitation with a grammatical “They are …” introduction. RESULT retains the full three-depth table and its training-realization limitations. |
| “Not a failure” | **Resolved.** | Release notes lines 3–4 now say “not a confirmation and not a FAIL under the locked rule.” This avoids obscuring the failed BLS clause. |
| Item 224's inferred first availability | **Resolved.** | Item 229 and RESULT lines 84–86 distinguish the change in retained query results from the first public availability time. The MJD/header-date qualifications are consistent with the first review. |

I independently compared the assembler's six literal replacement passages against the original review, then checked their occurrences in the rebuilt documents. The designated passages preserve the words with line wrapping normalized. RESULT's review sentence has a link inserted before its final punctuation; the registration uses a grammatical adaptation rather than purporting to be a quotation. Neither changes the meaning. Short summaries in the scoring README and log are faithful paraphrases, not misquoted reviewer text. Verification: source inspection plus `audit.py`'s phrase comparisons; the assembler itself was not run.

**The author's two additions:** I have no objection to either. “First availability” accurately limits what the saved query results and metadata establish; it does not assert a new archive-release chronology. “Review” accurately states my recommendation for a later declared computational reproduction and does not portray it as performed. “None has been made or decided” is the author's current status report, not something that hashes can independently prove. It is consistent with the retained unchanged result/run records and with this review's own lack of a rerun. No amendment is required on that account.

## Exact-byte checks

Independent `git status`, `git diff`, `git show`, `hashlib`, sequence comparison and JSON/text checks are recorded in `[reviewer temporary path redacted]` and `audit.json`:

- HEAD and local tag v1.19.2 both resolve to **`17a66414f233f8cc7326197d50db00713e495122`**. There are no staged changes or deletions.
- The working tree has exactly **6 modified files + 12 new files + the manifest**. The 18 manifest entries cover that complete changed/new set excluding the manifest itself, and **18/18** digests match.
- All **68 prediction CSVs** equal their v1.19.2 blobs. Explicit comparison of **194 tracked Python/config artifacts** finds no changes; the complete Git changed set contains no lock, scorer or validator modification.
- Monitoring README, scoring README, registration and DECISIONS retain their complete v1.19.2 byte prefixes. README has exactly one insertion; removing it restores its old bytes. CITATION differs only in version and `date-released`.
- The public log ends at **item 229**, not 230. Items 224–227 remain as historical entries with the new clarification. Local and public registrations are equal; the local and public RESULT notes are equal.
- `result_S108.json` remains **`bc62b2495c66d18c86ec5078f44abb14d965d9f2ff7dc3c02e2742d46d316b54`** and `acquisition_S108.json` remains **`ff320218910b7e145ed956b8a263211ee5b88dad7c95d1a4bea4c9e53ec17d56`**, matching the first review. The four added selection records, orbit snapshot and two run/precheck logs match their retained local sources.

**Reviewed release anchors:**

| Artifact | SHA-256 |
|---|---|
| `public_release/MANIFEST_v1.20.md` | `34336b1ece3c8c3de341d7f0fd52c5c80027d9f0175e8a8664e3cf7ac6d7f026` |
| `zenodo_upload/RELEASE_NOTES_v1.20.md` | `25e00d0a23b944051fcdd99071b5463d30b292e221f1b8ca20cc39592b5a50d2` |

Both match the re-check prompt. The fixes change presentation and documentation, not the recorded PARTIAL outcome or the test.

## Public copy of the first review

After removing the added header and blank separator, the public review equals `results/REVIEW_v1_20.md` exactly after **two temporary-path replacements** with `[reviewer temporary path redacted]`. No other body change was found. The public prompt is byte-identical to the original prompt. Verification: independent transformation/byte comparison, not reliance on the assembler's assertion.

I have **no objection to publication in this form**. The header correctly explains that the first review's “fix first” verdict concerns the unpublished first assembly and that the release is its corrected rebuild. It does not imply that I independently reproduced the flux analysis or approved the first assembly unchanged. The original verdict, findings and limits remain intact. This report supplies the separate verdict on the rebuilt bytes.

## Limits

The first review's successful validator runs and recorded-outcome arithmetic remain applicable to the unchanged artifacts; I did not represent them as newly rerun checks here. I did not execute the assembler, scorer or synthetic suites, inspect FITS data, verify historical archive availability or independently prove author attestations about unique runs/non-examination. No publication was performed. Within this focused re-check, all requested corrections and integrity checks pass, subject to the UTC publication-date condition above.
