# Independent full-repository review — v1.11

**Date:** 2026-10-20. **Reviewer/tool:** OpenAI Codex, with delegated code, claims and repository-hygiene audits; consolidated and checked by the primary reviewer. **Scope:** `results/PROMPT_full_repo_review_v1.11.txt`. **Public tree examined:** `public_release/`, commit `655c229f63afefaf3f953a376b8345541e91c487`; the surrounding NASA directory is the local analysis workspace, not this Git repository.

**Sources actually opened:** the public tracked files and their Git history; relevant local scripts, registrations, ephemeris/fit JSONs, tables, manuscripts' LaTeX sources and decision logs; three permitted TIC 89247735 QLP FITS files, S66/S93/S104 only; unauthenticated Zenodo record APIs and release ZIPs identified below. I did not open any of the seven protected targets' S106-or-later photometry, cutouts or FFIs. No credential file, private session URL, or third-party prior-search repository corpus was opened. Only this report was written in the project; calculations and downloaded archives were confined to `/tmp`.

## Verdicts

**The frozen numerical record survives the checks, but v1.11 is not a satisfactory current scientific/reproducibility release without corrections.** All 56 public prediction CSVs retain their first-committed bytes, the current manifests verify, and the downloaded v1.11 archive matches the repository. Independent regression reproduces the main v5 ephemeris. However, the current README and REPORT still assert withdrawn mass/localisation conclusions, public pipeline copies contain demonstrated numerical and wiring defects, and an explicitly withheld object's sky coordinates remain in the public prior-search record. Those are material issues despite the much more careful current manuscript and correction documents. This review does not invalidate the already-reviewed conformance procedure or establish that any particular frozen transit prediction is wrong.

| Area | Verdict | Basis |
|---|---|---|
| 1. Preregistration integrity | **needs corrections** | Numerical integrity is sound in the tested record; chronology wording, one rewritten provenance sentence and a legacy UTC label need correction. See integrity audit and F14–F16 below. |
| 2. Pipeline code | **serious problems** | Demonstrated folded-exposure error, repeated stacked values labelled per-event, remaining UTC producer errors, and stale public dependencies. F2–F5. |
| 3. Reproducibility/drift | **serious problems** | Six public/local script differences, missing original producers, machine-specific imports/paths and incomplete environment records prevent the claimed full reproduction. F2, F6–F8. |
| 4. Claims versus evidence | **serious problems** | Withdrawn Gaia/host claims, false 2P exclusion and reversed validation-threshold comparison remain in current public summaries. F9–F13, F17. |
| 5. Cross-document consistency | **needs corrections** | Current manuscript, README, REPORT, metadata, observing times and version citations disagree. F9–F13, F18–F25. |
| 6. Masking/privacy | **serious problems** | An explicitly withheld row retains sky coordinates. Public private-session references also remain. F1, F26–F27. No identity reconstruction was attempted. |
| 7. Git hygiene/navigation | **needs corrections** | Absolute paths and missing reproduction references; no large-binary blocker found. F7–F8, F28 and inventories below. |

Already-reviewed material, consistency only: the conformance package's 84 manifest entries verify and its archived 85 files match the public directory; the updated dossier qualifications in README:42–45 and the TIC 61310956 duration clarification agree with the prior review, while older REPORT/STATUS claims still conflict with them. I did not reopen the conformance design adjudication.

## Findings, sorted by severity

Locations below are relative to `/Users/fernando/Desktop/NASA`; `public_release/` is written explicitly. Numerical demonstrations and commands are documented after the table. “Inspection” means an executable-path or textual defect was identified without claiming an end-to-end scientific rerun.

| ID / severity | Location | Issue and verified evidence | Exact correction required |
|---|---|---|---|
| **F1 — blocker for a masked release** | `public_release/prior_search/PRIOR_SEARCH.md:160`; `public_release/prior_search/query_log_all.csv`, records ending at physical lines622,623,625,892,893,1645,1647,1940; same members in the Zenodo v1.11 ZIP | A row explicitly marked `[withheld]` retains `ra=` and `dec=` query coordinates. The bounded archive/text audit found this, and a second check of line 160 confirmed the withheld marker and both coordinate labels without printing their values. CSV-aware checks separately confirmed `target == "[withheld]"` and numeric RA/Dec query fields at the eight listed record-ending lines. This defeats coordinate masking even though I did not determine the object's identity or prove a particular unmasked TIC is that object. | Remove identifying coordinates, target aliases and identifying query arguments from public withheld rows; check their explicitly associated public query-log entries and archives. Preserve private provenance. Explain the correction transparently and address archived copies; do not silently rewrite preregistration history. Do not describe the current release as successfully masked. No coordinates or withheld identifier are reproduced here. |
| **F2 — major** | `public_release/scripts/search_pipeline.py:6,22–23`; `null_scramble.py:7–9`; `allsky_driver.py:8`; `single_transit_search.py:18`; `tsearch.py:44–48` | Six shipped scripts differ from local namesakes: `search_pipeline.py`, `tsearch.py`, `prereg_candidate.py`, `qlp_clock_v2.py`, `single_transit_search.py`, `triage.py` (byte comparison and `diff -u`). Public search ignores the environment-directory overrides used by its callers; public single-transit search lacks the local input override/target-list interface; public tsearch lacks the local >50% dropout rejection. Absolute imports can silently pick up the local corrected modules on the author's machine. The clock difference is principally a `main()` guard, not evidence of changed clock arithmetic. | Publish versioned source snapshots tied to each result and disclose differences; ship a consistently wired current pipeline with repository-relative imports and explicit input/output paths. Add a clean-clone smoke demonstration. Do not replace frozen CSVs to make a rerun agree. |
| **F3 — major** | Public and local `scripts/vet.py:57–62,99–112` | `transit_model` infers exposure from sorted time differences, but `global_ephemeris` passes **folded** times. The folded spacing is not an exposure. Direct extraction/execution of these functions on a synthetic 1800-s series gave inferred exposure **131.9904 s**, changing the model by **3097.29 ppm**; passing 1800 s explicitly restored agreement to numerical precision. | Carry actual exposure durations through folding and explicitly integrate each observation/sector; mixed cadences require appropriate individual/sector exposure values. Recompute affected exploratory fits/holdout summaries and report their sensitivity. This probe alone does **not** show the separate v2/v5 frozen ephemerides are wrong. |
| **F4 — major** | Public/local `scripts/vet.py:188–193` | Each purported event calls `box_depth` on the **entire holdout** with the same period and a reference time shifted by an integer period. It therefore repeats the stacked depth/SNR/count. A synthetic series with individual depths 1000, 3000 and 6000 ppm returned **3333.33 ppm for every event**. | Restrict per-event measurements to that event and its local baseline. Keep the annual/folded stack separately. Relabel/recompute existing per-event fields; do not present the stack's significance as evidence that each event individually has that significance. |
| **F5 — major** | Public/local `scripts/vet.py:358`; public `scripts/prereg_candidate.py:55`; public/local `scripts/final_ephemeris_317134140.py:90–91` | Active legacy producers still emit incorrect “UTC”: vet/317 interpret the BJD numerical value directly as UTC; public prereg_candidate performs only a timescale conversion. At TIC 89247735 v5 epoch 159, those paths give **02:19:03.733** and **02:17:54.549**, versus geocentric **02:10:03.079**. Errors are +9.0109/+7.8578 min. Current corrected v5 CSV is not implicated. Verified by code and independent Astropy calculation. | Use one tested, explicitly BJD_TDB-to-geocentric-UTC helper in every active producer and for both contacts. Mark legacy fields superseded; retain frozen bytes and provide corrected versioned products. Reword the global statement that all preregistration tools were already fixed. |
| **F6 — major** | `public_release/README.md:137–138`; `public_release/REPORT.md:482–487,635`; public script inventory | “Full pipeline” is not demonstrated by the published producers. Original local generators `prior_grep.py`, `triceratops_qlp.py`, `refit_89247735_raw.py`, `pixel_calib_89247735.py` are absent from the public script set. Published reviewer alternatives do not identify the exact original production path. No local/public producer for `injection_recovery_end_to_end.csv` was found by searching that output name; `single_injection.py` writes the earlier injection table only. | Publish the original generators/postprocessing and an input/output/version map, with masking applied. If an original calculation was ad hoc or its producer cannot be recovered, say so and distinguish table-arithmetic reproduction from independent regeneration. Replace “full pipeline” until this is supplied. |
| **F7 — major** | `dataset_v1/environment/requirements_venv.txt`; `dataset_v1/environment/requirements_triceratops_env.txt`; `prereg_bundle/requirements_venv.txt`; `dataset_v1/README.md:53`; `public_release/scripts/triceratops_317134140.py:6` | All three old environment files are **0 bytes**, despite the pip-freeze description. The newer public main lock is populated (80 lines, 1495 bytes), but contains no TRICERATOPS dependency for the explicit import; it does not document the separate environment. Verified with file sizes, contents and import inspection. | Supply complete separate environment records, Python versions and installation steps, or state that historical versions are unavailable. Add a dated notice to archived bundles identifying the replacement; do not imply an empty file records an environment. Installation was not tested in this review. |
| **F8 — major** | Core paths including `public_release/scripts/search_pipeline.py:6,22–23,132`, `vet.py:9,278,331,371`, `prereg_v2.py:9,18`; full inventory below | Published code imports/reads/writes the author's absolute workspace. The text scan found 358 matching lines in 116 files, including historical reviews; these are not 358 independent bugs. Current core entry points cannot simply be moved to another computer as the reproduction paragraph implies. | Use an explicit root/input/output interface or derive the repository root. Document required MAST inputs and their expected layout. Keep immutable historical scripts and provide a clearly versioned portable runner, especially for the already-frozen conformance package. |
| **F9 — major** | `public_release/README.md:14–18`; `public_release/REPORT.md:7,344–351,359–374,423–425,505–508`; corresponding `dataset_v1/REPORT.md`; `dataset_v1/README.md:13` | Withdrawn TIC 89247735 claims survive: target assignment, Gaia mass below about 25–30 Jupiter masses, old precise radius and giant/BD odds. Current `paper/main.tex:107,110–121,133–135` and `paper/rnaas/note.tex:15,28–31` instead retain the neighbour EB and no calibrated mass limit. This is a direct contradiction, not a new mass determination. | Replace the candidate summary with: **“Four approximately 1.1%-deep, 4.54-h events follow the clock-corrected v5 ephemeris P=18.323174±0.000040 d. Conditional on the target hosting the signal and the adopted deblending, Rp≈7.9–8.4 R⊕. The 7″ neighbour remains a possible eclipsing-binary host; the companion mass is unconstrained. Version 1 remains the test of record; v5 is the current timing refinement.”** Mark the old REPORT physical interpretation superseded before readers encounter it. |
| **F10 — major** | `public_release/REPORT.md:342`; compare `paper/main.tex:107` | The fourth event does **not** exclude the 36.65-d eclipsing-binary alternative as claimed. The v5 JSON epochs are 79,118,119,138, with parity odd/even/odd/even; a 2P binary can give alternating primary/secondary eclipses. This is verified directly from stored times/epochs and arithmetic. | **“P is the longest common recurrence period if the four events are of the same type. A 2P binary with alternating primary and secondary eclipses is not excluded by these times; the neighbour-hosted version remains open.”** |
| **F11 — major** | `public_release/REPORT.md:598`; `dataset_v1/REPORT.md:598`; `ddt_80387959/proposal.tex:21`; ambiguous “below validation” wording in `public_release/preregistration/TIC80387959/PREREGISTRATION_v2.md:9` | TIC 80387959 FPP=.047/NFPP=.010 are **above**, not below, the .015/.001 validation thresholds. Summing `results/external_review_allsky/triceratops_80387959_probs.csv` gives .0472978/.00993713. The published TRICERATOPS abstract specifies those thresholds (source below). | **“FPP=0.047 and NFPP=0.010, both above the validation thresholds FPP<0.015 and NFPP<0.001; these model-conditional results do not validate the candidate.”** Append a dated clarification to a frozen registration rather than replacing its text. |
| **F12 — major** | `ddt_80387959/proposal.tex:21`; `note_allsky/note.tex:32–33`; `public_release/REPORT.md:598`; dataset REPORT counterpart | “Single star” from RUWE .83 and “radial velocities exclude a stellar-mass companion” are unsupported. The cited internal review (`results/external_review_allsky/REVIEW.md:15`) supplies a constancy p-value and count, not a target-period sensitivity calculation. Official Gaia definitions describe goodness-of-fit and summary variability statistics, not a mass-exclusion likelihood. | **“Gaia DR3 summary diagnostics show no significant RV variability and RUWE 0.83. We have not calibrated a companion-mass exclusion from these summaries; spectroscopy remains necessary.”** Do not substitute the internal review's assertion for a demonstrated sensitivity calculation. |
| **F13 — major** | `note_allsky/note.tex:44–48`; `dataset_v1/README.md:16`; [protocol record 23508864 description](https://zenodo.org/api/records/23508864), opening and v1.2 paragraphs | “Before the test data exist or are public” / generic “observed but not public at freeze” survive outside the corrected README. These conflict with the explicit product-specific erratum in `public_release/README.md:105` and decision log acknowledgements of pending updates. This review verified the contradiction and API text, not a fresh MAST release-date reconstruction. | Put a leading dated notice in current metadata and subsequent preprint/dataset versions: **“The S106 test uses held-out, already-observed data for which public products existed. Target QLP light curves were absent at freeze; other S106 products existed. The authors attest that they did not examine the target's test-sector photometry before freezing. See the data-availability erratum and timing-rule clarification.”** Retain old statements only as explicitly superseded historical text. |
| **F14 — major, prevention** | Public/local `scripts/prereg_v2.py:127–132`; `scripts/prereg_candidate.py:56–61` | Inspection shows CSV/JSON writes are unconditional; `--freeze` controls the Markdown write, not whether existing frozen numeric files can be overwritten. A reproduction invocation can therefore overwrite a version while leaving its registration behind. **No historical CSV overwrite was found** in the independent Git audit. | Refuse existing frozen output paths, require a fresh version/output directory, and make dry runs genuinely nonmutating unless an explicit temporary output is supplied. Do not test this by writing over the actual project record. |
| **F17 — major** | `public_release/REPORT.md:401–411`; compare README:102 and `TIC89247735/PREREGISTRATION_v5.md:4–12` | REPORT still certifies the S104 clock within ≤1 min and presents v3 as the final refinement, although v5 explicitly supersedes that derivation with +7.533 min. Historical content is legitimate; an unqualified current certification is not. | Prepend: **“Superseded: the S104 clock verification below was incorrect. The current target-projected correction is +7.533 min. v5 supersedes v3/v4 as the timing refinement; v1 remains the test of record.”** Link the current addendum/registration. |
| **F18 — major** | `public_release/REPORT.md:319,424,45–47,146–155`; `ddt_80387959/proposal.tex:21`; `note_allsky/note.tex:28`; compare `paper/main.tex:51,127,144,149` and RNAAS note:19 | Unqualified “out-of-sample confirmation” and “blind” language obscures post-hoc recovery from data already on disk and retrospective split dependencies. Code also silently falls back to all-data shape on training-fit failure (`vet.py:181`). The revised paper explains the fourth-event limitation; public summaries do not consistently do so. | For the flagged event: **“Post-hoc recovery from quality-flagged observations already on disk, consistent with the locally frozen ephemeris; not a prediction of new observations.”** For year splits: **“Retrospective leave-one-year-out consistency checks with disclosed shape, alias and detrending dependencies.”** Log any training-fit fallback and do not call such a run independently blind. |
| **F19 — major, significance** | `public_release/REPORT.md:224–226`, contrasted with instrumental-period structure at :83–89 | A fraction of a logarithmic BLS grid is converted into an approximately 1% chance probability without demonstrating a uniform null distribution for the strongest peak. The document itself shows structured instrumental periods. This is an unsupported probability inference, not a newly measured false-alarm rate. | **“The matching windows occupy approximately 1.2% of the searched log-period range. This geometric fraction is not a calibrated chance probability for the strongest peak in structured TESS noise.”** Keep formal depth/scatter significance separate from empirical false-alarm probability. |
| **F15 — minor, integrity wording** | `public_release/README.md:134`; `public_release/preregistration/TIC89247735/PREREGISTRATION_v3.md:12`; commits `34fe84c` and `c0824ea` | “The first commit of this repository is the public timestamp” is false for later-added freezes. “Files are not edited” is also too broad: most registration changes are appended notes, but the v3 generator-provenance sentence was replaced between these commits. Diff shows this is **only provenance wording**, not timing/rules/CSV manipulation. | **“Each version's public timestamp is its first public commit/archive. Frozen CSV bytes are preserved. Registration annotations are dated; numerical refinements receive new versions.”** Add a specific historical note that the v3 generator sentence was replaced on 2026-10-18, without implying the numerical freeze changed. |
| **F16 — minor, legacy UTC description** | `public_release/preregistration/CORRECTION_UTC_2026-10-19.md:3–5,12–15,24`; `TIC317134140/predicted_transits_S108_S109_S110_utcfix.csv:2` | The universal “old columns were TDB→UTC only” description is false for 317: its generator used raw BJD as UTC. At epoch4936 the legacy field is **21:31:21**, true scale-only UTC **21:30:11.745**, and geocentric UTC **21:31:26.641**. The retained `tc_UTC_tdb_scale_only` label is wrong; the corrected geocentric column itself is correct to its minute resolution. The displayed “−1 min” shift is not old-column-to-new-column shift for that example. | Append a correction distinguishing raw numerical-BJD calendar labels from timescale-only UTC. Name preserved legacy fields `legacy_clock_label` in a new derivative, or explicitly document the historical mislabel. For this row the actual correction from the displayed legacy second value is about **+5.6 s**, not −1 min. Leave frozen products intact. |
| **F20 — minor, observing plans** | `public_release/README.md:18`; `REPORT.md:410–415,599`; `dataset_v1/README.md:13`; `STATUS.md:9,63` | Old “both full” Chile claims conflict with current contacts. Independent geocentric/CTIO calculation gives epoch159 ingress target30.922°/Sun−25.611°; epoch162 ingress Sun−11.9945°, narrowly failing strict Sun<−12°. REPORT's TIC803 first S111 transit **Nov27 21:13** should be **Nov27 01:20 UTC** for v2 epoch498. | State the ephemeris version, duration and site criteria: **“At CTIO, v5 epoch159 qualifies; epoch162 is marginal and narrowly fails the stated ingress darkness cut.”** Use 2027-06-25 02:10 UTC and 2027-08-19 01:29 UTC midpoint labels; for TIC803 use 2026-11-27 01:20 UTC geocentric. Do not claim worldwide “first full” visibility from one site's calculation. |
| **F21 — minor, physical numbers** | `public_release/REPORT.md:359,423`; README:14–16; dataset README:13 | “3.5 years” is **1081.0669986 d / 365.25 = 2.9598001 yr** from v5 transit times. Current fitted/adopted inputs imply Rp **8.391/7.910 R⊕**, a≈**0.119–0.120 AU**, Teq≈**544 K**, rather than the old radius/error, .113AU and560K. Main text uses the appropriately rounded current values. | Use “about 3 years,” Rp=8.4±0.7R⊕ (TIC radius) or7.9±0.45R⊕ (SED radius), conditional on host/deblending; a≈.12AU, Teq≈540K. Distinguish the historical4h search box from the fitted4.54h contact duration. |
| **F22 — minor, dossier consistency** | `public_release/REPORT.md:636–637`; `STATUS.md:13–14`; compare updated README:42–45 and TIC613 v3 clarification | REPORT retains TIC183 density ratio1.45 and blind4/4, whereas current adopted-host ratio is1.24 and the dossier qualifications are retrospective. STATUS retains TIC613 P16.53785/~1140ppm/SPOC11σ after README corrected them. This is a cross-document check of the completed dossier review, not a new photometric refit. | Align REPORT/STATUS with current adopted-host1.24 and qualified retrospective checks. For TIC613 use P16.5379656d, raw SAP≈1334ppm, known-ephemeris SPOC extraction≈1068ppm, with its baseline-sensitive odd/even caveat. Keep the frozen2.70h scoring reference distinct from the3.3h planning window. |
| **F23 — minor, DOI/version** | `public_release/CITATION.cff:9–12`; README:4,144,147; `paper/rnaas/note.tex:33` | CFF declares1.11 but DOI23443245 is record **v1.1**, not the concept or v1.11 DOI. Read-only API gives concept23443244 and current v1.11 **23508798**. README release list still has v1.4 pending. RNAAS's “current release” for the older analysis release becomes ambiguous. | CFF v1.11 DOI: **10.5281/zenodo.23508798**. Use concept DOI23443244 only when explicitly citing the evolving project. Update current badge/list/citation. Label the RNAAS cited version as its **analysis release**, preserving the actual version/DOI used. |
| **F24 — minor, novelty** | `public_release/README.md:79–83`; `dataset_v1/README.md:23–28`; REPORT:527–532 | “No prior report of any kind” / “no human-reported candidate anywhere” exceed the demonstrated search scope. The corrected dossier wording is bounded, but other summaries remain absolute. No new exhaustive catalogue/literature search was attempted here. | **“No earlier matching report was found in the sources searched by the dated prior-detection sweep; its coverage and indexing limits apply.”** Keep the concurrent report credited and distinguish local analysis dates from public priority. |
| **F25 — minor, stale document status** | `public_release/REPORT.md:6–7,581`; README:42,134; `STATUS.md:3,48,55–56`; `paper/README.md:3–11,21–22`; `dataset_v1/README.md:7` | “Everything else rejected,” “not deposited publicly,” procedure “to be published,” and old uncompiled/v3 manuscript instructions conflict with current files/releases. Dataset's “every object pending its pre-registered TESS test” conflicts with its own ground-test row. Dated historical timeline entries can remain; current headings must identify the snapshot. | Give REPORT an explicit historical-snapshot banner and current-status link; update active status/build instructions and distinguish AJ draft from submitted RNAAS note. Say **“No object is validated; individual dispositions and test types are explicitly labelled.”** Preserve dated history. |
| **F26 — minor, privacy** | Git commit-message locations listed below; [Zenodo23508798](https://zenodo.org/api/records/23508798) `metadata.description` | Twenty-five public commit messages contain private AI-session URL references; the current Zenodo description contains one too. URLs were detected but not opened or reproduced. Access permissions and exposure of session content are **unverified**, so this is not a demonstrated credential compromise. | Stop inserting private session links into public commits/descriptions; remove current metadata links and review access/sharing at the provider. Any necessary historical privacy remediation must preserve externally verifiable preregistration evidence and be disclosed. |
| **F27 — minor, contact-data policy** | `public_release/DECISIONS.md:194`; Git author/committer metadata | A professional DDT recipient email appears in public prose; Git metadata contains two unique email strings, one non-noreply. These exceed a literal “only author's ORCID/affiliation” personal-data policy, but are not demonstrated secrets. Values are intentionally omitted. | Review whether the recipient address should be public; use a role/official public-contact description if not. State the intended policy for normal Git attribution metadata. Do not silently rewrite chronology to remove routine attribution. |
| **F28 — minor, navigation** | `public_release/REPORT.md:54,76,173,413,483,491,495,502,524,548,569,581,635` | Backticked `results/...` paths frequently refer to the local workspace, not shipped locations. Static scan:369 mentions of259 distinct absent paths; many are deliberate build outputs/history, not broken Markdown links. Explicit relative Markdown-link check found no missing targets. | Add a local-to-release map: control summary→`CONTROL_TIC4206066.md`; poolB recovery→`tables/poolb_known_recovery.csv`; duo grid→`tables/single_transit_search/duo_cut_grid.json`; prior summary→`prior_search/PRIOR_SEARCH.md`. Label unshipped evidence and give producer/input instructions. |
| **F29 — minor** | Public/local `scripts/single_injection.py:1–2,17–18` | Docstring says impact parameter b=.3, but inc=90° makes the injected b=0. Verified directly from the parameter assignment. | Correct the description/calibration label to **central injections, b=0**. Do not change historical result bytes merely to match the old prose. |

**Severity clarification:** F1 blocks claiming that the current artifact protects the withheld object. F2–F13 and F17–F19 require scientific/reproducibility corrections, but no demonstrated CSV tampering or failure of the declared conformance-v2.1 outcome logic is alleged. Several REPORT passages may be intentionally historical; a clear supersession banner solves that editorial problem without falsifying the record.

## Integrity and chronology checks

I ran `git -C public_release ls-files`, `git log --follow --format=%H -- <file>`, `git show <commit>:<file>`, and SHA-256 comparisons in `/tmp/repo_v111_integrity_review/audit_record.py`, then independently compared local JSONs and protocol prefixes using `finish_integrity.py`. Results are in their `.txt`/`.log` outputs and `csv_audit.json`.

- **56 public prediction CSVs:**45 original/versioned freezes plus11 UTC correction derivatives. Every current CSV matches its corresponding local file. Every accessible historical version at that file's path has the same hash as its first version. Rename-following history for correction copies was handled by checking the actual blob/path, not treating an absent old pathname as a modification.
- **45 original registrations quote the correct CSV hash.** All 45 public ephemeris JSONs equal their local counterparts;44 carry matching `sha256_csv`. The older TIC317134140 `final_ephemeris_predictions.json` lacks that hash/freeze schema; its registration:3–4 correctly supplies the freeze and full CSV hash. That absence is not a hash mismatch or evidence of alteration.
- **MANIFEST_v1.11:**99/99 full-hash entries match. **Conformance MANIFEST:**84/84 match. **MANIFEST_v1.9** is a role/status table, not a full-hash manifest; its `af83f110`/`216e7a4c` prefixes match the v1/v5 files, and it correctly labels v4/method1 superseded and the v4-clock shape fit as not a v5 posterior.
- All **eight SHA prefixes** in `prereg_protocol/PREREG_PROTOCOL.tex:24–29` match their named versions. The protocol's v3 parameter row is a historical version-specific row, not evidence that v3 is the current timing refinement. All **27 nonempty hash entries** in `ERRATUM_S106_MANIFEST.csv` match the paths they identify, including local/public/bundle duplicates.
- All registration files preserve their initial text as a prefix, allowing trailing whitespace before appended notes, **except the v3 provenance sentence identified in F15**. Frozen CSVs were unchanged in that case too.
- For 43 original JSONs carrying a `frozen` string, 42 first-commit timestamps are later and one equals the recorded freeze (892v3); differences range0–224.483min. The two older schemas use their registration timestamps instead. First-commit timestamps are version-specific; Git timestamps alone do not establish server receipt time or prove non-examination.
- Where both columns exist, `tc_bjd_tdb − tc_btjd =2457000` to floating-point tolerance in all checked CSV rows.

Selected chronology, all times UTC; first commits obtained from the per-file history, freezes from the named JSON or registration:

| Record | Local recorded freeze | First commit containing CSV | Independent public archive evidence |
|---|---|---|---|
| TIC317 original | Oct17 18:30:15 | `62f5aca`, Oct17 23:01:38 | Main record23443245 created Oct17 23:05:01.066431 |
| TIC892 v1 | Oct17 21:28:13 | `62f5aca`, Oct17 23:01:38 | Same main v1.1 archive |
| TIC803 v2 | Oct18 22:34:41 | `24cd0de`, Oct18 23:24:45 | Main record23460915 created Oct18 23:24:53.814353 |
| TIC120 v2 | Oct18 22:34:49 | `24cd0de`, Oct18 23:24:45 | Same main v1.3 archive |
| Original protocol | Not inferred from document typography | — | Record23462442 created **Oct19 01:36:22.688677** |
| TIC183 v2 | Oct19 11:44:14 | `1ba1f67`, Oct19 12:15:57 | Protocol 1.2 record23474138 created Oct19 12:16:25.531850 |
| TIC704 v2 | Oct19 12:51:12 | `b944812`, Oct19 14:54:52 | Protocol 1.3 record23477866 created Oct19 14:55:17.765642 |
| TIC892 v5 | Oct19 19:57:20 | `d995a1f`, Oct19 20:19:23 | First-commit check; this audit did not download that older release archive |
| TIC122/206/253 v2 | Oct20 00:33:06/10/12 | `87a9c15`, Oct20 02:04:03 | First-commit check |
| TIC115 v2 | Oct20 00:44:10 | `87a9c15`, Oct20 02:04:03 | First-commit check |
| Current main v1.11 | — | `655c229`, Oct20 18:17:15 | Record23508798 created Oct20 18:17:33.040534 |
| Current protocol 1.4 | — | — | Record23508864 created Oct20 18:19:06.902432 |

Thus the original protocol did **not** predate the first public803/120 v2 freeze: the main v1.3 archive precedes it by about2h11min. The current timing clarification treats precedence as a dated decision, and README:106 states that the narrower reading will also be reported; that qualification is appropriate. The analysis is not a proof of what anyone had privately examined.

Public sources actually fetched, unauthenticated: [main v1.11 API](https://zenodo.org/api/records/23508798), [protocol 1.4 API](https://zenodo.org/api/records/23508864), [original main v1.1 API](https://zenodo.org/api/records/23443245), [main v1.3 API](https://zenodo.org/api/records/23460915), [protocol 1.0 API](https://zenodo.org/api/records/23462442), [protocol 1.2 API](https://zenodo.org/api/records/23474138), [protocol 1.3 API](https://zenodo.org/api/records/23477866). API `created` is stronger external evidence of record creation than a local freeze label, but is not a proof that every current metadata word existed at creation; I inspected current metadata and downloaded only the current archives.

Archive checks (`check_archives.py`, saved log): the 23508798 ZIP's **487 files match all 487 tracked files byte-for-byte**, with no extra/missing files. The protocol 1.4 record's historical `preregistration_bundle_v1.3.zip` has132 files; all 35 prediction CSVs match a public frozen CSV. Its `conformance_v2.1.zip` has85 files, all matching the shipped conformance directory. Each downloaded ZIP's MD5 matches the API checksum; none contains FITS members. No inference about older archived contents is made from their current API metadata alone.

## Independently re-derived numbers

Commands used the existing local Python environment without installing packages or executing production entry points that write outputs. Function probes were AST-extracted to avoid import-time side effects. `python -B -I` prevented local bytecode output; Astropy automatic IERS downloads were disabled for the timing calculations.

### Ephemeris, clock propagation and UTC

| Quantity | Independent result | Agreement / source |
|---|---|---|
| TIC892 v5 weighted linear fit | T0=4196.809908119191 BTJD; P=18.32317442228696d; σT0=.00131766584344d=1.89744min; σP=.00004019730664d; χ²=.3659835780 | Matches `results/vet_qlp/89247735/final_ephemeris_v5.json` to printed precision. Refit of its four `transit_times`, not a new raw-light-curve timing extraction. `.venv/bin/python -B -I /tmp/repo_v111_code_review/probes.py`. |
| TIC892 v5 CSV SHA | Prefix216e7a4c | Matches registration, JSON and v1.9 role manifest; full hashes retained in audit JSON. |
| v5−v1, epochs146–163 | +4.2768 to+5.4576min using stored CSV values | Correctly rounds to+4.3 to+5.5min; `check_shifts.py`. |
| Clock propagation, TIC120 | +.050114 to+.050837min | Matches public `qlp_clock_v2/shifts.csv` by independently weighted fitting of old/corrected sector times. |
| Clock propagation, TIC183 | +.857137 to+.868677min | Matches; maximum .31746 of its stored frozen σ. |
| Clock propagation, TIC258 | +3.578042 to+3.614373min | Matches; maximum .76515σ. |
| Clock propagation, TIC333 | +3.170627 to+3.188942min | Matches; maximum1.18109σ, the largest of the six unmasked non892 objects checked. |
| Clock propagation, TIC467 | +3.870782min | Matches; maximum .94409σ. |
| Clock propagation, TIC803 | +.520296 to+.552192min across its CSV | Matches; maximum .14902σ. |

`check_shifts.py` reads only the six **publicly named** clock JSONs and their timing metadata, uses independent least squares, and agrees with saved shifts within2.7×10⁻⁹min. I did not access the withheld object's private result or recompute fresh JPL vectors. The current addendum correctly distinguishes 892's larger v5-v1 refinement from the other objects' ≤1.2σ shifts, describes the 0.05-min clock allowance as adopted rather than an absolute calibrated error budget, and preserves the frozen predictions. This verifies arithmetic/consistency, not the clock method anew.

For UTC I iteratively solved geocentric TDB plus the target barycentric light-travel time = BJD_TDB, using Astropy's built-in ephemeris and target coordinates from the saved report metadata. Commands: `.venv/bin/python -B -I /tmp/repo_v111_integrity_review/check_utc.py` and `/tmp/repo_v111_claims_review/check_numbers.py`. Differences below0.2s between tests arise from rounded CSV BJD versus full-precision fit inputs and one-pass versus iterative inversion; saved display strings truncate to minutes.

| Object/version/epoch | Recomputed geocentric midpoint UTC | Stored corrected display / conclusion |
|---|---|---|
| TIC317 original correction,4936 | 2026-09-07 21:31:26.641 |21:31; correct geocentric display, incorrect retained legacy-column description (F16). |
| TIC892 v1 `utcfix2`,159 | 2027-06-25 02:04:51.955 |02:04; matches v1, which must not be confused with v3/v5 examples. |
| TIC892 v5,159 | 2027-06-25 02:10:02.995 from rounded CSV;02:10:03.080 from full fit |02:10; matches. |
| TIC803 v2 correction,498 | 2026-11-27 01:20:02.014 |01:20; matches. |
| TIC120 v2 correction,559 | 2026-07-12 21:51:39.724 |21:51; matches. |
| TIC183 v2,245 | 2026-07-16 21:14:44.556 |21:14; matches. |
| TIC613 v3,151 | 2026-12-29 04:21:53.232 |04:21; matches. |

CTIO spot check uses longitude−70.81°, latitude−30.17°, height2207m and pressure0. Full-fit v5 epoch159 contacts are **2027-06-24 23:53:57.859 to June25 04:26:08.302 UTC**; target altitudes30.9224°/73.6952°, Sun−25.6110°/−81.9291°. Epoch162 midpoint is **2027-08-19 01:29:08.728**, contacts Aug18 23:13:02.906 to Aug19 03:45:14.551; target61.2374°/57.3581°, Sun−11.9945°/−67.5630°. These reproduce the current “159 qualifies/162 narrowly fails” statement using the fitted approximately4.536h duration without adding a separate timing-uncertainty margin. This is a stated-threshold check, not a physical claim that0.0055° makes an observing programme impossible.

### Allowed raw photometry and numerical probes

The raw check opened only `data/qlp/hlsp_qlp_tess_ffi_s0066-0000000089247735_tess_v01_llc.fits`, the corresponding S0093 file and S0104 file. It used saved v5 event times and S104 clock correction, finite raw SAP including flagged cadences, a linear baseline at T14<|t−tc|<3T14 and the mean inside |t−tc|<T14/2, T14=4.54h. Each event had81 in-transit samples. Results were recorded in `/tmp/repo_v111_code_review/NOTES.md` from an inline `.venv/bin/python -B -I` calculation:

| Sector / epoch | Mean box depth ± formal scatter-only error, ppm | Formal SNR |
|---|---:|---:|
|66 /79 |9050.5±254.8 |35.52 |
|93 /118 |8885.4±342.1 |25.97 |
|93 /119 |10006.8±254.0 |39.40 |
|104 /138 |8953.4±201.0 |44.53 |

This independently supports four approximately1% dimmings under this simple baseline estimator. It does **not** calibrate false-alarm probabilities, establish the host, prove independence of the fourth-event discovery, or require equality with a fitted central depth: these means include ingress/egress and use a different baseline/flux product from some published numbers.

The direct code probes reproduce F3–F5: folded-cadence inference131.9904s versus real1800s,3097.29ppm model discrepancy; three differently deep events all reported3333.33ppm; legacy UTC offsets+9.0109/+7.8578min. Their complete safe probe is `/tmp/repo_v111_code_review/probes.py`, output `probes.log`.

### Table arithmetic and physical conversions

From `public_release/tables/single_transit_search/injection_recovery_end_to_end.csv`:293 rows,278 distinct stars; all n_in≥4;79/293=26.9625% flagged-time injections. Recounted recovery fractions:

| Injected SNR bin | N | Detected | After event cuts | End-to-end |
|---|---:|---:|---:|---:|
|7–10 |21 |16/21=76.19% |13/21=61.90% |8/21=38.10% |
|10–15 |46 |40/46=86.96% |35/46=76.09% |27/46=58.70% |
|15–30 |66 |61/66=92.42% |43/66=65.15% |38/66=57.58% |
|≥30 |94 |92/94=97.87% |45/94=47.87% |36/94=38.30% |

These match REPORT:484–487 rounded values. For SNR≥10, orbit-start distance bins0–.5/.5–1/1–2/>2d have N5/5/15/181 and end-to-end20/20/40/51.38%, also consistent with its indicative discussion. This is table arithmetic, **not** regeneration of the population/injection experiments or validation of their missing postprocessing.

`check_numbers.py` independently converts k=.098 with Rstar=.785/.74Rsun to8.39125/7.91022Rearth; a/Rstar32.6 with the TIC radius gives .119010AU and Teq544.172K under the adopted equilibrium convention; Kepler's law with .69Msun gives .120194AU. These support the rounded revised main-text numbers and identify the stale summaries in F21; the host parameters themselves were not newly measured.

For F11, the source probability sum gives FPP=.0472978186 and NFPP=.0099371341, respectively3.153× and9.937× the validation limits. The [TRICERATOPS primary paper abstract](https://arxiv.org/abs/2002.00691) states FPP<.015 and NFPP<10⁻³ for validation; its broader “likely planet” category is different, so I do not incorrectly apply the validation threshold to every “likely” label. The [official Gaia DR3 field definitions](https://gea.esac.esa.int/archive/documentation/GDR3/Gaia_archive/chap_datamodel/sec_dm_main_source_catalogue/ssec_dm_gaia_source.html) were checked for the meaning of the median-RV uncertainty, constancy statistic and RUWE; they do not themselves supply the candidate-specific mass sensitivity claimed in F9/F12.

## Masking, privacy and Git inventory

The concrete coordinate leak in F1 was found without crossmatching, identifying or reconstructing the withheld object. Explicit withheld rows also retain scientific feature values in `public_release/tables/allsky_testable_soon.csv:320` and `allsky_classA_outcomes.csv:4`; those values were not used to reconstruct an identity. A successful scan for an unmasked TIC cannot be certified under that restriction. Ambiguous proximity of other TICs to a withheld marker is **not** treated as proof of an identifier leak.

The hygiene audit used `git ls-files -z`, `git rev-list --objects --all`, `git cat-file --batch-check`, bounded credential-pattern scans and PNG chunk metadata inspection. The current 487 tracked files total21,559,901bytes; the largest is `prior_search/query_log_all.csv`,2,508,195bytes. There are42PNG files and no tracked FITS/PDF/ZIP archive. The 571 distinct historical blobs total23,060,981bytes. No large-binary repository blocker was demonstrated.

The 532 historical text blobs were scanned for common GitHub/AWS/private-key/API-key formats, embedded user:password URLs and private-address URL patterns: no credential-pattern matches. PNG metadata had39 text entries, all `Software`; no identity reconstruction or OCR of figure pixels was performed. Current ZIP safe-text scans likewise found no credential-pattern matches. These are bounded negative checks, not proof that arbitrary secrets or identifiers are absent. The private session references below are commit/API metadata findings, not a contradiction of the file-content scan.

Public private-session reference locations (commit-message line numbers; no URLs or tokens reproduced):

| Commit | Message line |
|---|---:|
|`655c229f63af`|11|
|`87a9c1531efe`|15|
|`d995a1fff8ad`|9|
|`c4e559468053`|10|
|`b944812ac441`|10|
|`1ba1f673127b`|9|
|`1fb222cf3466`|9|
|`f239afb568d6`|4|
|`e0853714f5cf`|4|
|`535519a5b6c5`|7|
|`c92b513b947a`|4|
|`24cd0deb40ce`|8|
|`eeeaa788077f`|4|
|`b7040a6a97e0`|4|
|`7a512c68bf6b`|4|
|`c0824ea8a9d9`|4|
|`9610bbe7fdde`|4|
|`34fe84caad4f`|4|
|`e2e533e2f41e`|4|
|`72079a58d4c9`|4|
|`4e20a8606278`|4|
|`28e68bed8393`|4|
|`16da3ad8fa61`|4|
|`6c68dc7ed74c`|4|
|`62f5aca71f08`|7|


### Absolute-path inventory

The following is the complete **116-file location inventory** from the public text scan (`/tmp/repo_v111_hygiene_review/absolute_path_locations.md`). Paths in historical review prompts and provenance logs are not necessarily execution defects; maintained imports/input/output paths are the portability issue in F8. This list does not claim that every listed absolute path is secret or that `/tmp` examples need rewriting.

- `public_release/DECISIONS.md`:529
- `public_release/REPORT.md`:4
- `public_release/conformance_v2.1/configs/conformance/115692561_S106.json`:7
- `public_release/conformance_v2.1/configs/conformance/120444365_S106.json`:7
- `public_release/conformance_v2.1/configs/conformance/122522485_S106.json`:7
- `public_release/conformance_v2.1/configs/conformance/183374279_S106.json`:7
- `public_release/conformance_v2.1/configs/conformance/206620592_S106.json`:7
- `public_release/conformance_v2.1/configs/conformance/253931796_S106.json`:7
- `public_release/conformance_v2.1/configs/conformance/70441745_S106.json`:7
- `public_release/conformance_v2.1/results/conformance_v21/configs_v2.0_backup/115692561_S106.json`:7
- `public_release/conformance_v2.1/results/conformance_v21/configs_v2.0_backup/120444365_S106.json`:7
- `public_release/conformance_v2.1/results/conformance_v21/configs_v2.0_backup/122522485_S106.json`:7
- `public_release/conformance_v2.1/results/conformance_v21/configs_v2.0_backup/183374279_S106.json`:7
- `public_release/conformance_v2.1/results/conformance_v21/configs_v2.0_backup/206620592_S106.json`:7
- `public_release/conformance_v2.1/results/conformance_v21/configs_v2.0_backup/253931796_S106.json`:7
- `public_release/conformance_v2.1/results/conformance_v21/configs_v2.0_backup/70441745_S106.json`:7
- `public_release/conformance_v2.1/results/conformance_v21/conformance_calib_report_rc1.py`:9
- `public_release/conformance_v2.1/results/conformance_v21/conformance_calibrate_holdout_rc1.py`:15
- `public_release/conformance_v2.1/results/conformance_v21/qlp_clock_test_sector_c016ad7a.py`:23
- `public_release/conformance_v2.1/results/conformance_v21/test_conformance_inputs_rc3.py`:6
- `public_release/conformance_v2.1/results/conformance_v21/test_conformance_rc3.py`:9
- `public_release/conformance_v2.1/reviews/PROMPT_conformance_recheck_rc2.txt`:2,16
- `public_release/conformance_v2.1/reviews/PROMPT_conformance_recheck_rc3.txt`:2
- `public_release/conformance_v2.1/reviews/PROMPT_conformance_recheck_rc4.txt`:2
- `public_release/conformance_v2.1/reviews/PROMPT_conformance_review_v21.txt`:1
- `public_release/conformance_v2.1/reviews/REVIEW_conformance_internal_findings.json`:24,47,59,66,80,84,97,148,194,309,355,492,521,544,561,567,590,607,613,630,645,653,659,762,785,831,937,960,977,1000,1006,1023,1029,1052,1128,1151,1266,1306,1369,1390,1392,1398,1530,1576,1582,1605,1720
- `public_release/conformance_v2.1/reviews/REVIEW_conformance_internal_synthesis_TRUNCATED.md`:116
- `public_release/conformance_v2.1/reviews/REVIEW_conformance_v21.md`:3,17,18,19,20,28,55,127,132,133,134,135,136,137,138,164,205,232,235,257
- `public_release/conformance_v2.1/reviews/REVIEW_conformance_v21_rc2.md`:3,7,19,21,43,45,92,97,98,99,100,101,122,129,153,154,156
- `public_release/conformance_v2.1/reviews/REVIEW_conformance_v21_rc3.md`:3,7,25,34,49,65,71,75,78,79,80,81,82,83,84,91,96,113
- `public_release/conformance_v2.1/reviews/REVIEW_conformance_v21_rc4.md`:3,7,17,21,25,28,29,30,31,32,33,34,35,57,64,92,103,108
- `public_release/conformance_v2.1/scripts/conformance_calibrate_holdout.py`:17
- `public_release/conformance_v2.1/scripts/conformance_discriminating_test.py`:10
- `public_release/conformance_v2.1/scripts/conformance_edge_profile.py`:6,8
- `public_release/conformance_v2.1/scripts/conformance_s106_forecast.py`:11
- `public_release/conformance_v2.1/scripts/make_conformance_configs.py`:10
- `public_release/conformance_v2.1/scripts/qlp_clock_test_sector.py`:23
- `public_release/conformance_v2.1/scripts/qlp_clock_v2.py`:10
- `public_release/conformance_v2.1/scripts/test_conformance.py`:9
- `public_release/conformance_v2.1/scripts/test_conformance_inputs.py`:6
- `public_release/conformance_v2.1/scripts/validate_conformance_real.py`:13
- `public_release/external_review/analysis_317134140.py`:4,13
- `public_release/external_review/asassn_fetch_89247735.py`:12
- `public_release/external_review/asassn_fold_89247735.py`:5,23,24
- `public_release/external_review/control_stars_s93.py`:8,21
- `public_release/external_review/control_stars_s93_v2.py`:16,28,39
- `public_release/external_review/four_events_89247735.py`:4,10,13,51
- `public_release/external_review/hlsp_check_89247735.py`:5,30
- `public_release/external_review/pixel_injection_89247735.py`:11,104,105
- `public_release/external_review/qa_events_89247735.py`:6,8
- `public_release/external_review/s93_two_events.py`:3,9,30,31
- `public_release/figures/TIC317134140/report.json`:4544
- `public_release/prior_search/query_log_all.csv`:30,31,32,74,80,81,483
- `public_release/prior_search_round2/PRIOR_SEARCH_round2.md`:722,739,760,761,2819,2827,2829,2835
- `public_release/prior_search_round2/query_log_all_round2.csv`:336,337,338,339,1204,1205,1206,1207
- `public_release/referee_89247735/REFEREE_REPORT_round4_external.md`:11,17,18
- `public_release/referee_89247735/REFEREE_REPORT_round5_external.md`:11
- `public_release/referee_round2/REFEREE_REPORT_dossiers_external.md`:3,5,58,115,189,196
- `public_release/referee_round2/pixel_calib2.py`:4
- `public_release/referee_round2/pixel_check.py`:7
- `public_release/reviews_2026-10-20/REFEREE_REPORT_round3.md`:6
- `public_release/reviews_2026-10-20/REVIEW_S106_test_procedure.md`:5,13,17,18,118,120
- `public_release/reviews_2026-10-20/REVIEW_erratum_and_clarification.md`:3,15,16,17,18,20,21,86,181
- `public_release/reviews_2026-10-20/REVIEW_timing_rule.md`:3,5,15,16,17,18,19,20,21
- `public_release/scripts/alias_89247735.py`:3
- `public_release/scripts/allsky_driver.py`:8
- `public_release/scripts/allsky_future_sectors.py`:4
- `public_release/scripts/allsky_targets.py`:6
- `public_release/scripts/allsky_testable.py`:10
- `public_release/scripts/aperture_test.py`:3,13
- `public_release/scripts/archival_176798599.py`:4,9,19
- `public_release/scripts/archival_test.py`:4,13,20
- `public_release/scripts/blind_seasons_317134140.py`:3,22,62
- `public_release/scripts/build_known.py`:3
- `public_release/scripts/control_4206066.py`:3,8,14
- `public_release/scripts/download_lcs.sh`:3,4,6
- `public_release/scripts/ffi_pixel_test.py`:6,19,89,90,93
- `public_release/scripts/final_ephemeris_317134140.py`:5,13,30
- `public_release/scripts/final_ephemeris_89247735.py`:4,6,38,54,57
- `public_release/scripts/final_ephemeris_89247735_v2.py`:5,8,14
- `public_release/scripts/final_ephemeris_89247735_v3.py`:7
- `public_release/scripts/final_ephemeris_89247735_v4.py`:12,13
- `public_release/scripts/final_ephemeris_89247735_v5.py`:8,9
- `public_release/scripts/independent_check_317134140.py`:8,25
- `public_release/scripts/known_nearby.py`:6
- `public_release/scripts/null_calibration.py`:4,53
- `public_release/scripts/null_control_blind.py`:3,9
- `public_release/scripts/null_scramble.py`:7
- `public_release/scripts/pixel_runner.sh`:3
- `public_release/scripts/poolb_known_recovery.py`:4
- `public_release/scripts/prereg_candidate.py`:7,11,17,38,42,47
- `public_release/scripts/prereg_v2.py`:9,18
- `public_release/scripts/qlp_clock_check.py`:9
- `public_release/scripts/qlp_clock_v2.py`:10
- `public_release/scripts/qlp_clock_v2_shifts.py`:5
- `public_release/scripts/rank.py`:5
- `public_release/scripts/refit_89247735_v4.py`:9,12
- `public_release/scripts/s104_clock_89247735.py`:7,9,10
- `public_release/scripts/s32_check_317134140.py`:2,15
- `public_release/scripts/search_pipeline.py`:6,22,23,132
- `public_release/scripts/single_injection.py`:5,10
- `public_release/scripts/single_null_compare.py`:4,21
- `public_release/scripts/single_rank.py`:9,11
- `public_release/scripts/single_transit_search.py`:14,18
- `public_release/scripts/single_triage.py`:3,6
- `public_release/scripts/tesscut_forward_test.py`:6,15,28,29
- `public_release/scripts/tessspoc_check.py`:7,10
- `public_release/scripts/tic_params.py`:5
- `public_release/scripts/toi_control_317134140.py`:3,20
- `public_release/scripts/triage.py`:3,7,66
- `public_release/scripts/triage_round3.py`:6,9,27
- `public_release/scripts/triceratops_317134140.py`:8,13,22
- `public_release/scripts/tsearch.py`:10
- `public_release/scripts/vet.py`:9,278,331,371
- `public_release/scripts/vet_runner.sh`:3,4
- `public_release/scripts/vet_summary_table.py`:4


### Frozen CSV audit inventory

All files below are under `public_release/preregistration/`. Every row's SHA-256 matched the corresponding local file and all available same-path Git blobs; original freezes also matched their registration hash. `UTC derivative` marks a separately introduced correction product, not a replacement of the original. Complete full hashes and first-commit dates were computed in `csv_audit.json`; this table records full hashes to make the checked set unambiguous.

| Public relative path | Kind | SHA-256 |
|---|---|---|
|`TIC115692561/predicted_transits_2026_2027_v2.csv`|Original/versioned freeze|`d8fe193dfce203392ad380c74d1ee08a9364d7335dc3b0e72bc9e77f0ed41085`|
|`TIC120444365/predicted_transits_2026_2027.csv`|Original/versioned freeze|`64b5b02607a23e21d3270eb1862dde28aec81050807ea0584f49f312de1f7094`|
|`TIC120444365/predicted_transits_2026_2027_utcfix.csv`|UTC derivative|`54fe5c77ba722ac4e1e427ea00324bed7481fa6ce592ebeb53296572605348fe`|
|`TIC120444365/predicted_transits_2026_2027_v2.csv`|Original/versioned freeze|`32b5e0857265e33e4902c5736d379bf0d7443516a9277678c2b403ac7b22de17`|
|`TIC120444365/predicted_transits_2026_2027_v2_utcfix.csv`|UTC derivative|`f6241276c680cc6f70c9b81d6bf186c42f3d3e670e4e79a3bac28a823ac13164`|
|`TIC122522485/predicted_transits_2026_2027_v2.csv`|Original/versioned freeze|`47ce36bcb863acc218fdc62c5d61ab9dc411ae7678734a3c09392f596e477d58`|
|`TIC159033763/predicted_transits_2026_2027_v2.csv`|Original/versioned freeze|`c45eb808cb65ed1e7dcc3c57d11cf1391e00e779fd1f99f5da7ea082e3410d2f`|
|`TIC160330868/predicted_transits_2026_2027_v2.csv`|Original/versioned freeze|`fa72f33be927e01156b60eb88da2d7a2be4636a82b79b40c324ed77dd01b79ca`|
|`TIC162304222/predicted_transits_2026_2027_v2.csv`|Original/versioned freeze|`742f2b162856cdbe1ab901e8243ada5011e9d6cf49a281f053e3b7cb9b932be1`|
|`TIC162304222/predicted_transits_2026_2027_v3.csv`|Original/versioned freeze|`445f1dd701470764a0471644c981738b8fc019920fb14743b73d83b8e16031ba`|
|`TIC183374279/predicted_transits_2026_2027_v2.csv`|Original/versioned freeze|`069d82980645e2adb5bc81895b187de8654dc880205574a50af764b79b04d621`|
|`TIC19119739/predicted_transits_2026_2027_v2.csv`|Original/versioned freeze|`5aafcdd96fd6ac1657489539790b0229855b5e94bcbc4cc0773651710dcac8d7`|
|`TIC196514928/predicted_transits_2026_2027_v2.csv`|Original/versioned freeze|`1fa2a7e068d35809c1f51ed7b021ecbd11e39ade86476d31879371333b853017`|
|`TIC203381983/predicted_transits_2026_2027_v2.csv`|Original/versioned freeze|`6ff79f8e8c204567ff1c79a213891f922a86d0c8ad26d5e2e6048b3f1c4907c3`|
|`TIC206620592/predicted_transits_2026_2027_v2.csv`|Original/versioned freeze|`75b6ea732c2db970f4bd11a3ff62c58b14a2d0a4d745ff9180703077a5dcf343`|
|`TIC24526743/predicted_transits_2026_2027_v2.csv`|Original/versioned freeze|`5a39b787e00b3d22d686476c3ae1adfd7c760691b43f797086a7aff7762bf83f`|
|`TIC245503256/predicted_transits_2026_2027_v2.csv`|Original/versioned freeze|`41678702f848b0cbb8b8bc54bb25ee82cb817cb5daad2b1304734da832446eb0`|
|`TIC249813122/predicted_transits_2026_2027_v2.csv`|Original/versioned freeze|`8c47e87946d91d3bdf214ff0c80adc3c9e9a8306b56347a5eb0ba03893f1abd7`|
|`TIC253931796/predicted_transits_2026_2027_v2.csv`|Original/versioned freeze|`7ac1b3519df00914fdab04c49937b1934fd066e96bdc853554709fe842a4378a`|
|`TIC258006047/predicted_transits_2026_2027_v2.csv`|Original/versioned freeze|`48805ca7e45c361f1a7c4092e145bce7c9c6e449edb768663d27efc3b1ba7e68`|
|`TIC283913390/predicted_transits_2026_2027_v2.csv`|Original/versioned freeze|`fe3ad4669d29c5a320aa63c56ff7e489bf0ce9d2278ca0d8ca0e8bb7addcd4bc`|
|`TIC317134140/predicted_transits_S108_S109_S110.csv`|Original/versioned freeze|`63e98fc87ebc6ce65198e066028d7f9ea58d24b51b35771d9fc551c41f59deb3`|
|`TIC317134140/predicted_transits_S108_S109_S110_utcfix.csv`|UTC derivative|`7833ac3ce828f9fc68756546222f0ab38015e29a571b123e6d95600d06309e00`|
|`TIC332709057/predicted_transits_2026_2027_v2.csv`|Original/versioned freeze|`32afcd7e3e1cf1d99f6a04add84de602d32c22eb9bbb1712469ba6d36c2a53e8`|
|`TIC333661705/predicted_transits_2026_2027_v2.csv`|Original/versioned freeze|`e7752bf76ab70b924362d09f957bf2df2e541f34fc19e29d6a44a1f7ff177872`|
|`TIC333735955/predicted_transits_2026_2027_v2.csv`|Original/versioned freeze|`c8551f9c33d0c02a7bd713cc5a2604072ce0fc16e7f259f84a11107ff635aba9`|
|`TIC366047768/predicted_transits_2026_2027_v2.csv`|Original/versioned freeze|`1e246164f0070fed7606c4c9597e49bc7d138f05b912e6340f5048303c654671`|
|`TIC36694943/predicted_transits_2026_2027_v2.csv`|Original/versioned freeze|`a51d71a1994743818576af064c2025588c53ee55614da972582fe0ae3f061c62`|
|`TIC371421714/predicted_transits_2026_2027_v2.csv`|Original/versioned freeze|`d1d84735958dc97e59ee3f79936e1984979bbb13ac5d83bd592d46efc07a4c02`|
|`TIC376225363/predicted_transits_2026_2027_v2.csv`|Original/versioned freeze|`034139b99d992aa3f11937f16dfe16d208350b30b323603afd381f2967306a87`|
|`TIC383617106/predicted_transits_2026_2027_v2.csv`|Original/versioned freeze|`edf4f0ef127158b2d6282c48d4fcb5f76c8e8e46b78ee86ba9275d807a77738d`|
|`TIC408110117/predicted_transits_2026_2027_v2.csv`|Original/versioned freeze|`bc55f95639e29746bcedda4a20933a7b34eda8ba7f2fedd03c1d5e2c1fb486ba`|
|`TIC467959906/predicted_transits_2026_2027_v2.csv`|Original/versioned freeze|`58a25a2ea6f6d13f24712cff3f25242d3b2e93d74e6bdf8fc624016f91da39d2`|
|`TIC50514263/predicted_transits_2026_2027_v2.csv`|Original/versioned freeze|`edba125f1f09f95aef509b2be34bc317da6443321f6b39bc5dbfea8435e728bf`|
|`TIC53825235/predicted_transits_2026_2027_v2.csv`|Original/versioned freeze|`6924d7b6140d569febde846a8e4ca4cdeec194f3ac122eaba14c90ac7bc20fa9`|
|`TIC61310956/predicted_transits_2026_2027_v2.csv`|Original/versioned freeze|`1f15a633e0e56a8a2e00329cf447d39de3be292d4d73055bde6032e98872ace0`|
|`TIC61310956/predicted_transits_2026_2027_v3.csv`|Original/versioned freeze|`76e892963501c62cdedcf07a94b1f2e65bbc47f91427bdd6006ec2250ab1da63`|
|`TIC65575657/predicted_transits_2026_2027_v2.csv`|Original/versioned freeze|`8e7400d246ac23103afce5096fe25ce0d63e821a6eaa8ed30b7622d99cd7c9af`|
|`TIC70441745/predicted_transits_2026_2027_v2.csv`|Original/versioned freeze|`243babb143e6565751f2828f02bafbd851f07dedee53b9b71ed6654f29aed564`|
|`TIC80387959/predicted_transits_2026_2027.csv`|Original/versioned freeze|`4652f7a330bd5cada6e999217d2183d3d391ab3a3dca4042f456c9c1e56690d2`|
|`TIC80387959/predicted_transits_2026_2027_utcfix.csv`|UTC derivative|`3ec99535516d5848896ad0c936f2f3a0dbb92df4299c9b38d8f6866205ff1eec`|
|`TIC80387959/predicted_transits_2026_2027_v2.csv`|Original/versioned freeze|`5d0e7651818e62542d316ff5e8e598b5a8255b29b0ada693b8584b529827a3f4`|
|`TIC80387959/predicted_transits_2026_2027_v2_utcfix.csv`|UTC derivative|`a9cf83636da6708f5f2df8164c33a1f12f6cf4e41cd08d9ab746afc90a721813`|
|`TIC88407114/predicted_transits_2026_2027_v2.csv`|Original/versioned freeze|`751ec316080ae4a6e9de8840f92a3f332e4dfb2b1aeb5be9bf3fa088dc9163f6`|
|`TIC89247735/predicted_transits_2026_2027.csv`|Original/versioned freeze|`af83f1105765b2a179de1a7b6d28f22bf2488fc3e1a04e45605dd3c9729caee8`|
|`TIC89247735/predicted_transits_2026_2027_utcfix.csv`|UTC derivative|`5dc4df26162712d86c2d6d807329995cdd60ea681c0d46b948a212c4ae1ad872`|
|`TIC89247735/predicted_transits_2026_2027_utcfix2.csv`|UTC derivative|`94ef672c90c97c4d54d727e9c39fd3198740191ebc8b5d63a402ae52821701e2`|
|`TIC89247735/predicted_transits_2026_2027_v2.csv`|Original/versioned freeze|`8a2b1ccadd1b820cf36f180b1cc83fe2e978c05e8637b7b566d14233b96f5869`|
|`TIC89247735/predicted_transits_2026_2027_v2_utcfix.csv`|UTC derivative|`a523f74c8be7de0fedd5a2c78d519fcd10e80804f1a3f728087271a3682bff96`|
|`TIC89247735/predicted_transits_2026_2027_v2_utcfix2.csv`|UTC derivative|`d9f591e49391559b94373ce4aed1d32b4bbabf4ea3c6b480efab20c7a3620664`|
|`TIC89247735/predicted_transits_2026_2027_v3.csv`|Original/versioned freeze|`b5338c90e0ac8edb80f01f6018217382602975b26806f1423bc0c87ff9408f04`|
|`TIC89247735/predicted_transits_2026_2027_v3_utcfix.csv`|UTC derivative|`27b2ee62e9dca5feb00a10f7ff8623b57951067e3bc96c38eb293592dcd36808`|
|`TIC89247735/predicted_transits_2026_2027_v3_utcfix2.csv`|UTC derivative|`10b9e1f71dd4bbf12b0407479ff8b37ad4c6bc17853ed755f9d186b21273e3e6`|
|`TIC89247735/predicted_transits_2026_2027_v4.csv`|Original/versioned freeze|`4f6aba63e252c4b205ac2c9ddd8d5c9545600d3f1ff17e215e85632f6a514d88`|
|`TIC89247735/predicted_transits_2026_2027_v5.csv`|Original/versioned freeze|`216e7a4c6a9863dbe7bbf0777e1638c083553b4eb146d2425a4ab0e1fd2153a5`|
|`TIC91617711/predicted_transits_2026_2027_v2.csv`|Original/versioned freeze|`559b438ceac090042d0f8fd8e35f18fbc7c950a58ecfdafc894c2affcf9de661`|


## Checks performed and limits

- **Reproducible review commands/evidence:** `python3 -B /tmp/repo_v111_integrity_review/audit_record.py`; `finish_integrity.py`; `.venv/bin/python -B -I /tmp/repo_v111_integrity_review/check_utc.py`; `check_shifts.py`; `.venv/bin/python -B -I /tmp/repo_v111_code_review/probes.py`; `/tmp/repo_v111_claims_review/check_numbers.py`. Read-only archive download/comparison: `check_archives.py`. Supporting audit inventories and notes are under `/tmp/repo_v111_{integrity,code,claims,hygiene}_review/`; these are temporary local evidence, not publicly deposited reproducibility artifacts. The procedures and numerical outcomes needed to assess the findings are included in this report.
- **Code scope:** search/rank/null/injection/vet/pixel/ephemeris/preregistration/clock/prior tooling were inspected and selected functions exercised. I did not execute the entire population search, every entry point, every prior-search query, TRICERATOPS, MCMC or all pixel calibrations. I did not install environments. F3's effect on each actual candidate remains unquantified. I did not conflate stale source with proof that a published historical result was generated by that stale source; the absence of a producer-version map is itself part of the reproducibility defect.
- **Already disclosed limitations:** `public_release/REPORT.md:439–445` acknowledges the null best-of-top3 versus ranked top1 comparison, secondary-error denominator, all-data alias substitution, WCS/proper-motion omissions and lack of a local timing slope. I did not count these as new undisclosed defects. Pixel significance/centroid error calibration remains subject to the prior referee caveats; the revised manuscript leaves the neighbour scenario open. This review does not newly validate the localisation.
- **Observation embargo:** no S106+ photometry, cutout or FFI for any of the seven protected targets was opened, downloaded or analysed. No declared-test clock command was run. Prediction CSVs and existing timing metadata are not new test photometry. The small permitted raw check was solely TIC892 S66/S93/S104. I did not establish whether forbidden files exist in every cache in this full-review task; earlier non-examination attestations are not independently provable from absence of files.
- **Chronology:** Git history and public API timestamps were checked, but private analysis order and historical MAST availability were not freshly reconstructed. Current API metadata can be edited after record creation; it does not prove its present wording existed on the original date. Current ZIP contents were checked; older release ZIPs were not all downloaded. No claim of an immutable timestamp for later-added files is inferred from the repository's initial commit.
- **Astrophysics:** raw depths are formal box estimates, not calibrated detection probabilities or host assignments. Saved ephemeris regression is a new calculation from saved transit times, not a new transit-time fit. Adopted stellar radii/mass/temperature were used for arithmetic, not independently re-estimated. No Gaia epoch-RV series, new spectroscopy or new host-star likelihood was obtained. No fresh JPL-vector calculation was made in this full-repository pass; clock-addendum arithmetic and version consistency were checked.
- **Documents/references:** the manuscript/preprint/proposal claims were examined through source text and cross-document values; this was not a fresh PDF layout/figure-pixel or exhaustive bibliography review. A bounded text/metadata inspection of the archived protocol PDF was performed by the archive audit. No claim that every remaining sentence, external literature citation or manuscript number has been independently validated is made.
- **Privacy:** no withheld object was identified or reconstructed, no leaked coordinates/aliases or private-session URLs are reproduced, and no credential file was read. Recognized-pattern scanning cannot certify absence of arbitrary secrets. Figure pixels were not OCRed. The concrete identifying-coordinate locations are reported without values; their existence alone is sufficient to require remediation.
- **Mutation/publication:** no source, data, frozen record, manifest, Git history or external service was edited; no commit, upload, push, message to an outside person or publication occurred. Only this report was created in the project. The final public-tree `git status --porcelain` check remained empty.

**Overall disposition:** preserve the verified frozen numerical record. Correct the public masking leak, replace unqualified superseded scientific summaries, fix the demonstrated producer defects, and supply versioned reproducibility information before presenting v1.11 as a complete, internally consistent research release. The report does not recommend altering the frozen scoring targets or reopening the already-approved conformance procedure on the basis of these unrelated defects.
