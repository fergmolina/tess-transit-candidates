# Pre-publication re-check of release v1.21

**Date:** 2026-11-14 UTC. **Reviewer/tool:** OpenAI Codex. **Instructions:** `results/PROMPT_recheck_v1_21.txt`. Workspace: `/Users/fernando/Desktop/NASA`.

## Verdict: **publish these bytes as v1.21**

F1–F10 are resolved for publication as a **qualified exploratory addendum**, through corrections, disclosures and withdrawal of unsupported interpretations. They are not resolved by new statistical calibration or independent photometric reproduction, and the release now makes that distinction. The 21 manifest entries match; the exact changed set, original byte prefixes, frozen artifacts and result of record pass the checks below. I found no remaining material publication blocker. PARTIAL remains unchanged. This verdict does not authorize me to publish, and I have not done so.

**Date condition:** approval assumes publication on **2026-11-14 UTC**, matching `CITATION.cff` and the new publication statements. If publication occurs later, update the actual release date in CITATION and the new publication/status notices and manifest, regenerate affected hashes, and verify that date-only rebuild before publication. Preserve the original November 13 analysis date, November 14 corrections-note date and historical log timestamps. Approval of the exact hashes below does not extend automatically to altered bytes.

## F1–F10 disposition

Here **E** denotes `public_release/scoring_317134140_s108_s110/exploratory/S108/`, **C** its `CORRECTIONS_AND_COMPLETION_2026-11-14.md`, and **X** the unchanged `scripts/exploratory_317134140_S108.py`. I read C against the original review, saved JSONs and relevant source. “Resolved” below means the publication defect is addressed; disclosed methodological limitations remain.

| Finding | Status | Evidence |
|---|---|---|
| F1: losses falsely attributed entirely to gaps | **Resolved** | C “F1, F2” expressly withdraws both gap-only claims, gives the 12/3/3/2 dominant-stage tally and distinguishes ordered accounting from a causal experiment. The root README, exploratory README and release notes use the corrected passage. |
| F2: 17 empty windows | **Resolved** | C distinguishes 17 empty ±0.75-h transit windows from 15 empty ±3-h windows. Recounting `item1_events` reproduces both. |
| F3: changed trimming order | **Resolved by disclosure** | C “F3, F5” describes trimming after finite/quality selection, disclaims numerical equivalence with the older implementation and labels it a departure. This agrees with X:116,133 versus `scripts/vet.py:276,308`. No equivalence test is claimed. |
| F4: odd/even covariance and significance | **Resolved by qualification** | C calls the quadrature spread an uncorrelated approximation, labels the ratios nominal, withdraws a calibrated detection/sensitivity claim and says the covariance was not saved. The release summaries retain the uncertainty qualification where they quote the spread. |
| F5: localization errors and neighbour inference | **Resolved by qualification** | C identifies coordinate scatters from 200 independent-pixel Gaussian perturbations, not radial bootstrap errors; lists covariance/WCS/positive-weighting limitations and lack of TOI masking; and explains why the distance threshold is not met. No confidence-level neighbour exclusion remains in the current statement. X:117–159 supports these descriptions. |
| F6: “exactly 2P” | **Resolved** | C distinguishes the nearest grid point, 1.143457 d, from 2P = 1.1437268 d, and gives the correctly rounded 0.024% offset. |
| F7: incomplete reporting | **Resolved by completion/disclosure** | C reports all three window maxima for P and 2P, the 2P grid step, model-time counts and duration-scaled offsets. It discloses that full periodogram arrays and no-TOI count triples were not retained. C “F10” describes both fold panels. No reconstruction is claimed. |
| F8: incomplete flags and overstated missing-flux description | **Resolved** | C supplies all nine exact QUALITY values and the omitted 19 rows, distinguishes bit 128 from exact value 128, uses flux **or uncertainty**, adds the two short kept-data gaps and qualifies the grouped intervals. The mission-document lookup is attributed to the prior review and explicitly does not alter the mask. |
| F9: equal support, gap causation and general 2P exclusion | **Resolved** | C withdraws “equally” and “mainly because,” denies quantified relative support, restricts the 400/0 illustration to a simplified single-eclipse model and rejects a general 2P/EB exclusion. This is consistent with the current summaries. |
| F10: figure interpretation and calibration language | **Resolved by captions/disclosure** | C gives the bin-error definition, parity placement, pixel axes, aperture contour, ±3000-ppm clipping, saved extrema and missing colour bars. It withdraws the claimed calibration range. Both PNGs are byte-identical to those inspected in the first review; I did not regenerate or reanalyse them. |

The withdrawal of **“S98 (two sectors)”** is appropriate: `results/vet/317134140/report.json`, `pixel_depth_map`, identifies sector 98 and 4280 in-transit rows. The current S108 map has 1857, so “roughly half” remains a reasonable descriptive comparison. The note properly presents the control offsets as recorded assertions, not reconstructed calibration.

## Numerical and quotation checks

I used standard-library Python (`python3 -B`, `json`, `collections`, `math`) on E/report.json and E/quality_addendum.json, not on photometry. All reported scientific values agree at the stated precision:

| Quantity | Independently checked saved value |
|---|---|
| Eligibility | 48 predictions, 20 ineligible; dominant stages 12 nonfinite flux/error, 3 absent finite-time rows, 3 trim, 2 TOI mask; 17 zero in-window counts, 15 zero full-window counts; 30 eligible without TOI mask. |
| QUALITY | Exact counts `0:421, 16:2, 32:8, 128:648, 144:1, 160:7, 168:1, 4096:3507, 32768:537` sum to 5132. Omitted categories sum to 19. Bit-128 count is 657. Finite SAP count is separately 5113. |
| Short gaps | 4299.771458–4300.025644 and 4312.562687–4312.816872 BTJD; widths 0.254186 d. |
| P grid summaries | Nearest 0.5719903066 d, SDE 4.679046, rank 22. Best ±0.1%: 0.5716615948 d, 4.843542, rank 17. Best ±0.5% and ±1%: 0.5726482973 d, 5.236762, rank 9. |
| 2P grid summaries | Nearest 1.1434569709 d, SDE 2.003855, rank 374/5541; 0.0235921% below 2P. Best ±0.1%: 1.1447723501 d, 2.938400, rank 162. Best ±0.5% and ±1%: 1.1467482565 d, 7.071403, rank 1. Local step 0.0574846%. |
| Model phases | 14/21 within ±0.75 h; first offset −0.2084457 h = −0.1389638 T14; last +1.2417574 h; baseline drift 1.531721 h = 1.021147 T14; leading-period offset 0.2641764% above 2P. |
| Parity | Odd 249.680048, spread 64.688066, 13/24; even 166.552603, spread 63.254122, 15/24. Difference 83.127445; quadrature 90.474470; nominal ratios 0.918794 and 2.633071. |
| Position and map | Shift 0.0980511 mpx, nominal norm 1.512201. Target offset 0.5644654 px. Coordinate scatters 0.147086/0.172661 px; 17035 map rows, 1857 map in-transit rows, 1319 LC-centroid in-transit rows; 43 finite pixel depths, extrema −9292.7/+39250.6 ppm. |

The methodological numbers—200 perturbations, 40/80 bins, mask/windows and colour limits—were checked in X, not inferred from JSON. The earlier S98 values were checked in its older report. The quality-flag meanings faithfully reproduce the prior review's documented [MAST cadence-quality table lookup](https://outerspace.stsci.edu/spaces/TESS/pages/14563420/2.0%2B-%2BData%2BProduct%2BOverview): scattered-light exclusion, manual anomaly exclusion, and insufficient targets for error correction. I made no new archive query during this re-check.

I parsed the assembler with `ast.parse`/`ast.literal_eval` **without importing or executing it**, extracted its five `RQ` passages, normalized whitespace, and compared them to the original review and assembled documents. All five match, including the result-update paragraph. I found no misquotation of the suggested substantive text.

## Current statements, historical text and navigation

The exploratory README directs readers to the corrections note first; REPORT's appended status note explicitly says the corrections prevail. The corrections note itself also establishes that precedence. Thus preserving withdrawn claims in the historical REPORT does not present them as the current conclusions. The root README, scoring README, appended RESULT note and release notes consistently retain PARTIAL and distinguish exploration from an independent reproduction. Conduct is explicitly author-reported in the detailed account; shorter pointers do not claim independent proof.

I searched `public_release/` Markdown/text using `rg` for the obsolete availability-of-analysis statements and withdrawn scientific phrases. Remaining occurrences were in the preserved RESULT/README/log, historical report/reviews/prompts, or explicit withdrawals. RESULT's appended note covers unexamined event losses, figures/centroids, the target-pixel download and—explicitly in its next paragraph—“no additional photometric analysis is reported.” The root README has its own dated qualification. DECISIONS 232 and 235 supply dated qualifications for the log. I found no additional current, unqualified instance requiring a new notice within that text-search scope.

I resolved **21 explicit reader-navigation paths** with `Path.exists()` from the new exploratory README, REPORT status suffix, RESULT suffix, scoring README suffix and root README block; all resolve. The paths in the external release notes resolve from the intended release-root context. Preserved reviewer/source citations and `SHA256.txt` use the original workspace paths rather than pretending to be release-relative links; the exploratory README explicitly explains that distinction. The original review's basename cited in the correction note is accessible through the README's full relative review path.

## Exact-byte checks

Independent checks used `git status --short --untracked-files=all`, `git diff v1.20`, `git show v1.20:<path>`, `git ls-tree`, `git hash-object`, and Python byte comparisons/SHA-256. I did not run the assembler.

- HEAD and peeled tag v1.20 both resolve to **896692ee58df80ff05bd552e155db379c0a8e04a**.
- Exactly **5 modified + 16 new files + MANIFEST_v1.21.md**; no deletion. Manifest entries cover precisely the 21 files excluding the manifest itself, and **21/21 hashes match**. No FITS/FIT/FZ file is added. `git diff --check` is clean.
- The full v1.20 blobs of DECISIONS, scoring README and RESULT are byte prefixes of their new versions. Removing the single new root-README block restores its v1.20 bytes exactly. CITATION differs only in version and date-released.
- The public REPORT begins with the original bytes whose SHA is **1e28db50d767de28509911eb3719cd069bed9e2aaed77663f2231fef3bb8b0e4**. PLAN, both JSONs, PNGs, run.log, SHA256.txt and both scripts match their reviewed local sources exactly. All seven historical shortened checksum entries also match their original workspace sources.
- Explicit Git-object checks of **169 selected protected artifacts**, including all **68 prediction CSVs**, configurations/locks, relevant scoring/registration/validation Python files and S108 result/acquisition JSONs, find no changes. The complete changed-file set independently excludes any other lock, config, scorer, validator or prediction modification.
- The local `results/test_317134140/S108/RESULT_S108.md` equals the public appended version. No scientific result file has been replaced.
- The exploratory review and its prompt, and the v1.20 re-check prompt, are identical to their local originals. The public v1.20 re-check differs only by its explanatory header and **two** temporary-path redactions; I reproduced the redaction transformation and compared the full text.

Verified anchors:

| Artifact | SHA-256 |
|---|---|
| `public_release/MANIFEST_v1.21.md` | `fa6c7d6a992b99cab48f7522c054965d06194639f00ec480becf675d4dd7f829` |
| `zenodo_upload/RELEASE_NOTES_v1.21.md` | `c51189e2a496d9dc79beda9384d813b324e5564cf50c837acf5bdd8eb7ff4539` |
| `scripts/assemble_v1_21.py` | `939bd0505993cf9ce35d0f6900f8758c2c8787d90ff7f858618a5659618cbae2` |
| E corrections note | `9ef32a244346a1fa54ba11f32fd0bff2443e9ee1a33f28e9ca632861280ac12a` |

The assembler's source contains the asserted single-build guard and integrity checks, but source assertions are not substitutes for the independent byte checks above. Local DECISIONS 237 reports an initial assertion failure and a subsequent successful assembly. I did not rerun either attempt or independently establish their execution history.

## Public log and small editorial qualifications

The added public log contains exactly **230–236**, not 237. Manual reading and a regex scan of that suffix found no email address, recipient name, session link or temporary path. Item 235 adequately corrects item 233's scientific summary, including nominal errors, changed trimming order, nearest-grid wording, omitted flags and unsaved intermediates. Historical claims are preserved as such, rather than silently erased.

There are minor literal imprecisions, none of which changes the release conclusions or requires another build:

- Item 236's **plan** says “one temporary path redacted”; the actual public copy transparently declares two, and the independently verified transformation removes two. Local item 237 records the mistaken expectation and corrected assembly. Preserve that history; when 237 is published, it supplies the explanation.
- C's opening “Every number here comes from” the two current JSONs is too sweeping literally: S98's 4280 comes from the older comparison report, and bin/perturbation counts are source-code settings. The later sections identify those contexts and all these values were independently verified above. A future provenance sentence could say “Scientific measurements are taken from the saved outputs; method settings and earlier comparisons are identified separately.”
- In C/F8, “error <= 0: none” is the **additional removals at that stage of the ordered accounting**, not a census of error values in rows already rejected. The cluster implementation starts a new run at a gap **greater than** 0.05 d, so its precise joining rule is “at most 0.05 d,” rather than “less than.” Neither wording difference establishes a different saved count or interval.
- The short exploratory README's SDE “4.7 to 5.2” summarizes the nearby grid values, not multiple measurements at exactly fixed P. Its immediately following “candidate-period grid summaries” sentence and C's explicit grid table supply the necessary distinction.

These are documented here to avoid implying literal perfection. They do not revive F1–F10's material problems or change the verdict on this assembled release.

## Limits

This was a source/text, saved-number and byte-integrity re-check. I did not execute the assembler, exploratory scripts, locked scorer, validator or any live acquisition operation. I did not open, hash anew or parse the FITS files, download anything, inspect future-sector photometry, regenerate plots, or independently recover the measured depths/periodogram. Author conduct, absence of unrecorded activity and remote publication state are not established by these comparisons. Uncertainty calibration and an independent computational reproduction remain unperformed, as the corrected package states.

Only `results/RECHECK_v1_21.md` was written in the project. **No blocking edits are requested; publish the reviewed bytes as v1.21 on 2026-11-14 UTC, subject to the author's publication decision.**
