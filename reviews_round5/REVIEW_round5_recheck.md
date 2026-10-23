> Public copy (2026-10-23): 13 local temporary paths replaced by "[reviewer temporary path redacted]". No other change.

# Round-5 re-check and cross-round correction audit

Date: 2026-10-22. Reviewer/tool: OpenAI Codex, independent reviewer agent, including an independent historical-input reconstruction in this re-check. Instructions: `results/PROMPT_recheck_round5.txt`; baseline: `results/REVIEW_round5_results.md`. Sources opened: the current decision log, correction draft, named Python scripts/tests, saved audit/pixel/report JSONs and CSVs, registrations and local public-release documents. Temporary reproductions are under `[reviewer temporary path redacted]`. No new TESS downloads or TRICERATOPS calculation was performed. Protected-sector photometry was not accessed. The sector-inventory reconstruction used only existing, filename- and header-verified S105-or-earlier inputs; no fold or probability was recalculated.

## Verdict

**Sufficient after listed changes.** Closing round 5 without a freeze and withdrawing the unsupported interpretation of TIC 13450993 resolve the principal scientific issues without requiring another fit. The prior credits, chronology qualification, refined periods and TLS terminology are corrected. The pixel reclassification and NASA identifier fix reproduce. The historical correction is worth publishing, but its wording and the decision-log count need small corrections, and the proposed replacement runner must not be described as reproducing `vet.py` event selection: it still uses a different preparation procedure and has an incomplete input manifest. These are corrections to provenance and prospective software claims, not evidence that the frozen predictions were changed or that protected test data entered these runs. This verdict does not authorize a new probability calculation or constitute an assembled-release review.

## Status of the original findings

| Original finding | Status | Independently checked evidence |
|---|---|---|
| R5-1: prior credit | Fixed for this closed round, with date-attribution clarification below | `logs/DECISIONS.md`:1024–1026, 1045–1047 names eumemic/ahrazzle, Paliwal and moosesteve21 and rejects first-discovery/validation claims. Draft correction:56–58 does likewise. The periods match the source reports checked in the original review; the source paths remain in `prior_match_round5.csv` and its text companion. |
| R5-2: sector provenance and runner | Historical inventory expanded; replacement partly fixed | Current draft gives the full 15-run inventory, rather than correcting only round 5. `triceratops_qlp_v2.py`:24 guards both sector lists before access; :30–41 uses exact QLP paths, checks TIC/sector headers and records hashes. Remaining preparation/manifest issues are C1 below. |
| R5-3: TIC 13450993 FPP inference | Fixed by withdrawal and deferral | Decision log:1052–1056 and draft:34–35 explicitly withdraw the nearby/binary inference and quote no replacement probability. The original outputs remain historical. |
| R5-4: wrong-period null margin | Adequately disclosed; statistic not repaired | Decision log:1053–1054 identifies the 16.867-day global peak rather than the 14.591-day candidate, and :1073 states that no candidate-period statistic was calculated. Deferral is an acceptable disposition. The original mechanical PASS must not be reused as candidate-specific evidence. |
| R5-5: failed/NaN and rounded pixel offsets | Functionally fixed for the checked products; count error remains | All four new CSVs reproduce byte-for-byte. Failure lines emitted by `ffi_pixel_test.py`:18,99 are recognized by `pixel_collect_v2.py`:25. The frozen-object inventory is independently complete across the 42 locally registered IDs checked. See C2 and the tables below. |
| R5-6: ON_TARGET interpretation | Fixed in the correction, requires links at affected public statements | Decision log:1057 and draft:39–42 limit the result to a screen, not neighbour exclusion. Current published registration wording remains unqualified at the locations below; append/link the correction in the next release. |
| R5-7: chronology | Fixed as a qualified account | Decision log:1058–1060 states that prior matching and pixels ran concurrently, that this differed from item 131, and that the mutable log does not authenticate declaration time. This matches the original independently reconstructed sequence. |
| R5-8: NASA `tid` parsing | Fixed, with discriminating regression test | `prior_match.py`:19 recognizes `tid`. The current regression test passes; a temporary copy with only that recognition removed fails the NASA fixture, reporting `NASA TOI schema (tid) not matched`. |
| R5-9: periods, TLS, S85 count | Fixed | Decision log:1050–1052 gives 1.512518 and 1.202785 days, calls Nigraha TLS, and states that no S85 in-transit points were retained. These agree with the current reports and original numerical checks. |

I checked that none of `results/vet_allsky/{240488148,372343190,13450993}/` contains a registration or frozen ephemeris/prediction bundle. Thus the current record agrees with the no-freeze decision at `logs/DECISIONS.md`:1045–1048. There is no new object to approve for scoring.

## Remaining findings and exact fixes

| ID / severity | Evidence and consequence | Required correction |
|---|---|---|
| C1 / moderate, before claiming the replacement runner is ready | `scripts/triceratops_qlp_v2.py`:8 says that applying `trim_edges` means “the fold uses vet.py's event selection.” It does not. Lines 35–39 select finite positive flux with quality zero, trim before flattening, use a 0.7-day window and retain every finite flattened point. `tsearch.py`:29–55 also checks usable flux errors and rejects excursions of at least 50% from the median; `vet.py`:18–26 flattens with a 0.75-day default, then applies the edge mask and clips upward outliers. These differences can change retained cadences and depths even though the edge-mask function is shared. The 20 supplied tests only exercise guards/required arguments, not preparation equivalence, header refusal or output provenance. | Either share and test the actual vetting preparation on explicit allowed inputs, or replace the claim with: **“This runner uses the same gap-edge mask function as vet.py, but a separate documented photometry preparation; equality of retained events or depths has not been established.”** Label it unvalidated for new screening runs until synthetic preparation/header tests pass. Do not make a new probability run merely to satisfy this review. |
| C1b / moderate, prospective reproducibility | The manifest at `triceratops_qlp_v2.py`:59–62 hashes QLP files and the runner, but not the report supplying P/T0/duration/coordinates (:27–28), the actual TESScut files/apertures (:49–54), or their requested-versus-failed selection. The QLP header is checked; the returned TESScut identity is not checked in this script. Therefore “records its inputs and hashes” in the draft:12 is incomplete if read as a full run manifest. | Record the ephemeris values and report hash; requested/successful/failed aperture sectors; actual cutout paths/hashes and aperture pixels; verify returned sector/target geometry before use. Until implemented, narrow the draft to **“records its QLP photometry inputs and their hashes; complete aperture/ephemeris provenance is still being added.”** A historical erratum can be published with this limitation; it should not advertise an already validated replacement workflow. |
| C2 / minor but definite arithmetic error | Decision log:1041 says **40 ON_TARGET objects become AMBIGUOUS_INCOMPLETE**. Reproduction gives **38**, plus two other changes. The draft's per-round totals 4/19/7/10 are correct. | Replace with: **“Forty rows change classification: 38 ON_TARGET rows become AMBIGUOUS_INCOMPLETE, TIC 321980862 changes from ON_TARGET to AMBIGUOUS, and TIC 389029596 changes from OFF_TARGET to AMBIGUOUS.”** |
| C3 / moderate publication wording and placement | Draft:9 claims the FPP/NFPP values “are reproducible as computed.” Inventory reconstruction is not a repeated stochastic probability calculation; the old runs lack complete historical input manifests. Draft:39 also describes old acceptance as every finite offset ≤0.5 px, whereas it used rounded offsets: TIC 321980862 has 0.5028183 px. The new correction is not yet linked from affected public object records. | Say **“These are the original saved single-run FPP/NFPP outputs; no probability calculation was repeated for this audit. The photometry-sector inventory was reconstructed from surviving files, their timestamps and the original selection code.”** Say **“The old screen applied the 0.50-px threshold to offsets rounded to 0.01 px.”** Add dated correction links at the object/aggregate statements listed below, preserving frozen bodies and CSV bytes. |
| C4 / minor software usability | `triceratops_qlp_v2.py`:27 accepts an arbitrary directory through `--out`, but :56,58,62 concatenate filenames directly. `--out [reviewer temporary path redacted]` consequently targets `[reviewer temporary path redacted]`, not `[reviewer temporary path redacted]`, and the directory is not created. This follows directly from the string expressions; no probability run was needed. | Use a `Path` output directory, create it explicitly and join filenames with `/`. Add a temporary-directory test. |
| C5 / minor date attribution | Decision log:1025,1046 and draft:58 give moosesteve21's “found 2026-10-12” as an unqualified fact. The source README makes that claim; the original review independently checked GitHub commit/publication evidence, not the private discovery act. | Use **“reported discovery date 2026-10-12”**, and link the named report. Similarly distinguish Paliwal's claimed discovery date from the verified public-report date; do not turn credited recovery into an absolute first-person priority claim. |

These requests do not require rewriting old probabilities or changing frozen scoring thresholds. They require accurate labels for the saved calculations and honest claims about the replacement software.

## Historical TRICERATOPS inventory: independently reproduced

I ran `.venv/bin/python -B -I [reviewer temporary path redacted]`, which inventories all 15 `results/vet_allsky/*/triceratops.json` outputs, compares each matching local QLP file's modification time with that result's completion-time proxy, verifies the filename sector before opening anything, checks header TIC/sector, and reproduces the exact finite-time/finite-positive-flux/quality-zero count in `triceratops_qlp.py`:15–16. Every file inspected was in S105 or earlier. There were no matching files timestamped after these result files and no high-sector file requiring refusal. No file was modified. This reproduces all 15 sector lists in the supplied audit JSON, including all eight differences:

| TIC | Saved aperture sectors | Reconstructed photometry sectors | Different? |
|---|---|---|---|
| 122522485 | 30, 97, 105 | 30, 97, 105 | no |
| 13450993 | 58, 85, 86 | 58, 85, 86 | no |
| 151767028 | 90, 99, 100 | 36, 63, 90, 99, 100 | yes |
| 160330868 | 33, 87, 98 | 32, 33, 87, 98 | yes |
| 183374279 | 96, 103, 105 | 2, 29, 69, 96, 103, 105 | yes |
| 188664994 | 80, 81, 84 | 20, 24, 40, 47, 50, 51, 52, 53, 54, 57, 60, 73, 80, 81, 84 | yes |
| 195343302 | 55, 56, 83 | 55, 56, 83 | no |
| 196514928 | 35, 62, 88 | 34, 35, 62, 88 | yes |
| 206620592 | 28, 68, 96 | 28, 68, 96 | no |
| 240488148 | 56, 82, 83 | 56, 82, 83 | no |
| 253931796 | 28, 68, 96 | 28, 68, 96 | no |
| 283913390 | 7, 33, 87 | 7, 33, 87 | no |
| 343298093 | 101, 102, 103 | 13, 39, 66, 93, 100, 101, 102, 103 | yes |
| 372343190 | 84, 85, 86 | 52, 57, 58, 84, 85, 86 | yes |
| 61310956 | 72, 45, 22 | 45, 46, 72 | yes |

The short-sector cut matters: TIC 61310956 S22 has 900 good points and supplies an aperture but no photometry; its S46 enters the fold. TIC 188664994 S26 has 895 good points and does not enter this calculation (S17: 950; S23: 956 also fail); TIC 13450993 S18 has 993 and fails. These counts are in `tri_audit.json` and were obtained from the unchanged filter, not inferred from the authors' summary. All remaining seven sector sets agree with their recorded lists. The draft's FPP/NFPP figures are rounded versions of the saved JSON outputs; no probability was recalculated.

This audit covers every extant result at the old runner's hard-coded output path. It does not prove that no deleted run ever existed, or independently recreate historical file bytes from current mtimes. Result completion time is a proxy for the run, not a signed start-time manifest. All surviving input mtimes precede their results by more than an hour; the evidence supports the no-S106 statement for these reconstructed runs. Publish that scope rather than an unlimited forensic assertion.

Earlier published locations needing a provenance link include `public_release/README.md`:47 (TIC 183374279), :49 (TIC 61310956), :161 (round-4 probabilities), and `public_release/preregistration/TIC{151767028,343298093,188664994}/PREREGISTRATION_v2.md`:9. Public saved `triceratops.json` files exist for affected TICs 160330868, 196514928 and 61310956; place the correction beside them. The affected 183374279 and 61310956 probabilities also occur in `results/round2_dossiers/DOSSIERS.md`. Preserve their original values as historical outputs, but link the actual photometry/aperture-sector distinction. The dedicated earlier analyses for other stars must not be declared affected solely because they also used TRICERATOPS: this audit concerns the identified `triceratops_qlp.py` runs.

## Pixel reproduction and cross-round scope

Command pattern: `.venv/bin/python -B -I scripts/pixel_collect_v2.py results/<round>_pixel.csv [reviewer temporary path redacted]`. Before execution I inventoried every candidate's `ffi_pixel_S*.json` filename and refused any sector ≥106; all inspected files were earlier sectors. This is a reclassification of saved diagnostics, not another pixel extraction.

| Input round | Rows changing class | ON_TARGET → AMBIGUOUS_INCOMPLETE | Other changes |
|---|---:|---:|---|
| classA_round2 | 4 | 4 | None |
| round3 | 19 | 18 | 321980862: ON_TARGET → AMBIGUOUS; maximum 0.5028183 px |
| round4 | 7 | 7 | None |
| round5 | 10 | 9 | 389029596: OFF_TARGET → AMBIGUOUS; maximum 0.8970285 px |
| Total | 40 | 38 | Two rounding-boundary changes |

Every output byte-matches the corresponding saved `results/*_pixel_v2.csv`. The correction draft's TIC lists match these changed rows. For example, TIC 372343190 now correctly becomes incomplete because the log records the failed S84 download, even though its remaining finite offsets are small. The v2 collector uses full-precision JSON for thresholds; `offsets_full` is only a six-decimal display field. Failed/NaN sectors do not override a positive ≥0.9-px off-target flag; this is consistent with the documented rule. The code does not claim that all incomplete objects are neighbours or false positives.

To check omissions among freezes, I built a TIC-only list from all `results/{vet,vet_allsky,vet_qlp}/*/PREREGISTRATION*.md`, deduplicated to 42 IDs, and ran the same collector to `[reviewer temporary path redacted]`. Exactly the following four were incomplete; 37 were ON_TARGET and one had no applicable summary (`pending`). This verifies completeness among the extant registered objects and these saved diagnostics, not any deleted historical attempt.

| Frozen TIC | Invalid sector | Finite sectors and full-precision offset, rounded here to six decimals | Relevant public claim |
|---|---|---|---|
| 91617711 | S71 | S72: 0.027511 px | Aggregate “all 26 … on target” at `public_release/README.md`:53 and `public_release/REPORT.md`:672; the object is in that frozen list. |
| 253931796 | S68 | S96: 0.058444 px | `public_release/preregistration/TIC253931796/PREREGISTRATION_v2.md`:9: “On target (0.06 px S96).” |
| 160330868 | S98 | S87: 0.142930 px | `public_release/preregistration/TIC160330868/PREREGISTRATION_v2.md`:9: “On target”. |
| 188664994 | S80 | S81: 0.495208; S84: 0.096390 px | `public_release/preregistration/TIC188664994/PREREGISTRATION_v2.md`:9: “on-target in the FFI pixel test”. |

A suitable append-only qualification is: **“The original ON_TARGET label used only finite rounded offsets. The corrected screen is AMBIGUOUS_INCOMPLETE because sector S… supplied no finite offset. The remaining finite offsets are … . This is not a calibrated host assignment or neighbour exclusion. Frozen predictions and scoring rules are unchanged.”** Link the consolidated correction from the release README and retained aggregate tables, including `results/round2_dossiers/readme_insert.md`:15 and the corresponding public text. Historical selection counts can remain if explicitly labelled as the original screen rather than current validated localization.

The log-parser audit examined the logs for every object in the four input batches. No emitted `sector N failed` or `no TESScut for sector N` line was missed by the new parser. This does not prove that an unlogged crash never occurred. The four frozen-object list is supported; there is no basis here for declaring every prior pixel localization generally invalid, especially analyses made with other tools.

## Tests, integrity and limits

- Ran temporary copies of `scripts/test_triceratops_qlp_v2.py` and `scripts/test_prior_match.py`, changing only child Python invocations to add `-B` and using fresh `/tmp` outputs. The former reports **20 pass, 0 fail**; all current matcher regression checks pass. A temporary matcher with only `tid` recognition removed fails the new NASA fixture. No project bytecode or scientific products were written.
- Independently exercised the runner's `main` with a forbidden photometry sector, a forbidden aperture sector and a protected TIC, while instrumenting file opens. All three refused before any file open. No real runner preparation, lightkurve/TESScut call or TRICERATOPS calculation was executed. Exact-path/header/manifest behavior beyond these guards was reviewed in source, not certified by the supplied tests.
- Recomputed registration integrity: **46** `prereg_v2.py` registration versions have CSV hashes matching both their JSON and Markdown records; **68** current public prediction CSV copies byte-match their local counterparts (`[reviewer temporary path redacted]`). This establishes current consistency with the frozen records/public copies, not a forensic proof that every historical file was immutable at every intervening moment.
- The candidate-specific null statistic remains uncomputed and the original six-hour noise estimates remain unverified, exactly as in the first review. Since round 5 closes without a freeze and the weak object is deferred, neither omission needs another data analysis to make the historical correction honest.
- This review does not revisit unrelated scientific claims, revalidate planets, rerun Monte Carlo probabilities, or approve a future release assembly. Temporary evidence includes `checks.py`, `pixels.json`, `frozen_pixels.py`, `frozen_pixel_all.csv`, `guard_main.py/json`, regression logs and `frozen_integrity.py/json` under `[reviewer temporary path redacted]`. Only this report was written in the project during this re-check.

---

## Follow-up re-check — 2026-10-22 17:38 UTC

**Verdict: fixes sufficient for the historical correction and closure of round 5.** The outstanding C1/C1b/C2–C5 wording and implementation corrections are now addressed at the level requested for this draft. This is not validation of the replacement TRICERATOPS workflow, a new probability result, or approval of an assembled release. The draft must retain its UNVALIDATED qualification and its planned append-only links must actually be placed during release assembly. Round 5 remains closed without a freeze. Verification: current DECISIONS 137/140; the draft and scripts listed below; fresh synthetic tests. The original review above is preserved, not retrospectively rewritten.

This follow-up reads `results/PROMPT_recheck_round5.txt` again and checks the changes made after the earlier review. I did not repeat the already independently reproduced 15-run inventory or open any real photometry. I did not run TRICERATOPS, TESScut, lightkurve downloads, a search or a freeze. The only FITS opened in this follow-up were the artificial three-row header fixtures created under `[reviewer temporary path redacted]` by the supplied synthetic tests; they are not TESS data.

Current audited hashes, independently computed with SHA-256:

- Correction draft: `63d3f10a68665250de1601107a6ca1e9dba51e24711e3c1ff8f679dce5da6fe0`.
- `scripts/triceratops_qlp_v2.py`: `42ef529b6631f317b0bf75c0252d8ac17c81197bd1318e8cb531d9d7c4731ab7`.
- `scripts/test_triceratops_qlp_v2.py`: `276b893069d1507df5697498e127e282067639d2bfe9ec3cbb8b9a1c1528a273`.

| Earlier finding | Follow-up status | Evidence and remaining limit |
|---|---|---|
| C1: unsupported equality with vetting preparation | **Resolved by accurate disclosure** | Runner:8–15 explicitly distinguishes the shared gap-edge mask from its separate 0.7-day preparation and states that equal retained events/depths have not been established. It remains UNVALIDATED. Draft:13–16 repeats that qualification. No synthetic preparation-equivalence test has been added, so this finding is resolved through the review's permitted disclosure option, not by demonstrating scientific equivalence. |
| C1b: incomplete run provenance | **Resolved in source for the requested manifest; operational validation still deferred** | Runner:44–45 obtains P/T0/duration/coordinates from the named report; :77–80 records those values and its hash. Lines 63–72 track requested/used/failed aperture sectors, sector-header and central-position checks, cutout path/hash, target pixels and actual aperture pixels. QLP file hashes and retained-point counts remain recorded at :55. I inspected these expressions; I did not execute a real cutout or probability run, and the supplied tests do not exercise all aperture branches. The draft no longer advertises an already validated workflow. |
| C2: 40 versus 38 incomplete classifications | **Resolved** | DECISIONS 140 explicitly corrects item 137: 38 ON_TARGET→AMBIGUOUS_INCOMPLETE changes plus the two rounding-boundary changes, 40 total. The original dated item is preserved. All four current `results/allsky_*_pixel_v2.csv` files still byte-match the independent reproduction saved at the first re-check; no diagnostic file was reopened. |
| C3: stochastic reproduction claim and historical pixel wording | **Resolved in draft; placement is an assembly task** | Draft:8–16 now calls these the saved single-run outputs, states that no probability calculation was repeated, describes surviving-file reconstruction and its deleted-run limitation, and qualifies the replacement runner. Draft:41–46 explicitly describes the old rounding to 0.01 px. Section 4 (:65–77) lists the public/object/dossier locations and an append-only pixel qualification. Those links are a declared release-assembly requirement; this follow-up does not assert they are already present or approve publication without them. |
| C4: output-path concatenation | **Resolved, tested** | `out_dir` at runner:28–29 creates a `Path` directory; :74,76,82 use path joins. The fresh test checks the directory and joined filename under `/tmp`. |
| C5: private discovery versus public report date | **Resolved in draft** | Draft:61–63 now calls the Paliwal and moosesteve21 dates “reported discovery date,” separately identifies the public-report date, credits all three sources and claims neither first discovery nor validation. This verifies the wording correction; it does not newly authenticate a private discovery act. |

Fresh command: `.venv/bin/python -B [reviewer temporary path redacted]`, a temporary copy of the current test file changing only its child interpreter to `-B -I` and placing fixture directories under `[reviewer temporary path redacted]`. Result: **25 pass, 0 fail**. Tests include the protected-target/sector guards, required sector argument, output-directory joining, wrong-TIC/wrong-sector header refusal, matching synthetic header acceptance and refusal of a missing exact filename. Evidence: `[reviewer temporary path redacted]`. There was no network request or probability calculation.

No remaining issue in C1/C1b/C2–C5 blocks the **honest historical correction** in its current wording. The replacement runner's scientific preparation, aperture branches and end-to-end probability behaviour still need their separately declared validation before new screening runs; retaining that limitation is essential. The old inventory, prior-matcher regression, frozen-record checks and candidate-specific null limitations retain the scope stated in the original review. This follow-up does not broaden them into a new forensic audit or a fresh certification of release files.
