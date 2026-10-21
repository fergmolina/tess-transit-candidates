# Independent re-check of the round-4 corrections

Date: 2026-10-21 UTC. Reviewer: Codex review team. Sources actually opened: `results/PROMPT_recheck_round4_fixes.txt`, the previous review, current registrations/configs/scripts/errata, DECISIONS 120–122, STATUS, the unchanged public_release tree, primary RAVEN CSVs and local eumemic catalogs, and the public RAVEN Zenodo page and paper. Numerical checks used saved ephemerides and permitted control-sector timing data only. No prohibited test-sector photometry was accessed. This report is the only project file edited by this re-check; test products are under `/tmp/round4_recheck/`.

## Verdict

**No — not yet ready to include in v1.15.** Most original scientific wording corrections are now satisfactory, the three round-4 prediction files are unchanged, and the new clock constant and eight configs have the intended current values. Four matters still prevent approval: the new ground-based horizon version is incorrectly configured and its identical-row claim is false; the matcher misses the primary RAVEN period column; the config's newly promised clock-prior binding is not enforced; and the prior-detections erratum preserves an unsupported “first human” priority claim. The test harness and remaining supersession-template error also need correction. None requires looking at test data or changing the seven S106 configs.

## Status of findings F1–F9

| Finding | Status | Evidence and assessment |
|---|---|---|
| F1 — 343298093 prior report | **Resolved** | `results/vet_allsky/343298093/PREREGISTRATION_v2.md:92–97` explicitly withdraws the old claim, identifies the compressed catalog and weak flag, calls the result an independent rediscovery and claims no priority. STATUS.md:17 agrees. I re-read the source `vetted_signals.csv.gz`, decompressed line 64: P = 0.7661376546406703 d. The original CSV hash remains `4f14d1fe…`. |
| F2 — complete locked scoring inputs | **Partially resolved** | Eight configs exist with correct reference values, prediction/evaluator hashes, primary flags and future-data status (`make_conformance_configs_round4.py:10–38`). The previously missing 188664994 c0 prior is present and numerically verified. All seven S106 configs are byte-identical to their v1.14 copies. However, `clock_prior`/`clock_prior_sha256` are stored but not enforced by the clock/evaluation path; the existing tests do not test that promise. See R3 below. |
| F3 — comprehensive horizon correction | **Partially resolved** | `ERRATUM_PREDICTION_HORIZON_2026-10-21.md:18–26` now includes all five affected records and the correct omission counts. Keeping the published 115692561 list without supplementation is explicitly declared at lines 29–32 and is consistent with its unchanged config and published governance. 162304222 v4 and 53825235 v3 reproduce the preceding ephemerides and have the stated expanded coverage/status labels. But 3367979 v3 is not properly registered as a ground test, and its identical-overlap claim is false. The future header template still emits “First freeze” for later versions. See R1/R5. |
| F4 — primary sector and TESScut exception | **Resolved as a declaration** | The three amendments explicitly fix primaries S112, S113 and S117, prohibit substitution for any result/refusal, and require separate later-sector tests. They permit only TESScut TIME/TIMECORR for the clock and prohibit flux substitution: 151767028:60–67, 343298093:98–105, 188664994:52–59. This is unambiguous and the configs identify exactly one primary per object. The per-sector evaluator need not choose an overall primary; subsequent reporting must honor the locked flags. |
| F5 — reproducible prior matching | **Partially resolved** | `prior_match.py` now parses CSV/gzip/ZIP records and associates TIC and named period fields within one row, avoiding the old neighbouring luminosity false match. Safe reruns recover the known eumemic and mirrored RAVEN matches. But line 19 omits RAVEN's actual `bls_per` column; a direct run on the newly downloaded primary tables returns zero matches. See R2. |
| F6 — 151767028 RAVEN credit | **Resolved** | The amendment at 151767028:56–59 accurately records the evidence available when appended. The later primary table independently confirms P = 2.2103981294347577 d at `nsfp09_table.csv:4832`. It is absent from the primary vetted/validated tables. Append the subsequent primary confirmation/citation so the historical “not yet checked” statement is not mistaken for the latest status. |
| F7 — rounding/scope/status | **Resolved for the original finding** | 343298093:96–97 now uses NFPP 0.00097 and correctly says the FPP condition fails. 188664994:50–51 explicitly limits this version to S117–119 and describes undated later coverage. STATUS.md:21 distinguishes local freezes from archived ones and its public-release row now identifies v1.14. A new priority problem in STATUS.md:10 is covered by R4. |
| F8 — 188664994 uncertainty | **Resolved** | Lines 40–44 distinguish the formal inflated linear-ephemeris error from uncalibrated additional sector systematics, give the previously verified 22.9-min RMS / 21.7-min sensitivity, and forbid changing the frozen gate after the data. No retrospective replacement error bar is claimed. |
| F9 — 188664994 depth/exclusion provenance | **Resolved** | Lines 45–49 retain the original 412-ppm all-sector depth, explicitly acknowledge S26, give the 420 ±43-ppm sensitivity, correct the retained-depth range to 239–614 ppm, state the quality estimator and admit the post-dry-run exclusion. These agree with the previous independent numerical reproduction; no new flux analysis was needed. |

## Remaining fixes

### R1 — the ground-based horizon correction is incomplete and its fidelity claim is wrong

`freeze_horizon_fix.sh:7` omits `--ground` for TIC 3367979. Its v3 CSV therefore labels **all 435 rows** `undated (future sectors [])`; v2 labelled its rows `none (ground-based)`. All **399 overlapping rows** differ in `tess_sector`, although their shared numerical predictions, UTC/status values and the fitted ephemeris agree. The new registration still selects “next TESS sector(s)” and prints the QLP/SPOC outcome paragraph, despite the stated absence of TESS coverage. `ERRATUM_PREDICTION_HORIZON_2026-10-21.md:39–40`, the reason in `freeze_horizon_fix.sh:7`, and DECISIONS 121 therefore incorrectly say the 399 rows are identical. Verification: CSV field comparison in `/tmp/round4_recheck/integrity.py` and `.json`; direct reading of `results/vet_allsky/3367979/PREREGISTRATION_v3.md`.

**Fix:** retain v3 and its hash; correct the erratum/log with “The numerical predictions agree for all 399 shared epochs, but the sector labels changed because `--ground` was omitted.” Prefer a new version generated explicitly with `--ground`, with the actual ground-observation precision, coverage, timing and outcome requirements fixed before observations. Alternatively, make a complete dated ground-scoring amendment and explicitly withdraw the inapplicable TESS clauses. Do not advertise v3 as a complete correctly generated ground registration.

The other two horizon versions passed the targeted comparison:

| Record | Numerical ephemeris vs preceding version | Rows and status | Shared-row check |
|---|---|---|---|
| 162304222 v4, `b4a26083…` | Identical | 208 predictions in S111–114 | All 68 rows shared with v3 are identical in all fields. |
| 53825235 v3, `1408a7cd…` | Identical | 136 rows: 75 retrodictions, 61 predictions | No overlap with the old truncated v2 list; no identical-overlap claim is needed. |
| 3367979 v3, `0e8f5ea1…` | Identical | 435 rows, but wrong TESS/ground labels | 399 shared rows agree numerically but differ in `tess_sector`. |

For 53825235, 47 S108 rows and 28 early-S109 rows are correctly labelled before-freeze retrodictions; the remaining 18 S109 and 43 S110 rows are predictions. Evidence: the paired JSONs/CSVs and `/tmp/round4_recheck/integrity.json`. This is a chronology check, not evidence of the author's personal non-examination.

For 115692561, the unchanged 32-row frozen S106 list and its hash remain the declared input; omitted epochs 3418–3419 are disclosed and S107 will not be tested. This agrees with the hashed-CSV precedence in `public_release/conformance_v2.1/GOVERNANCE_S106_TESTS_2026-10-20.md:12` and the unchanged `115692561_S106.json`. No new event list or transfer of calibration is implied. The erratum's discussion of possible eligibility is a forecast based on nominal orbit times, not an observation of the withheld data.

### R2 — the matcher still misses a central primary-source schema

The actual primary RAVEN column is **`bls_per`**, absent from `PERC` at `scripts/prior_match.py:19`. I ran the unmodified script safely with its output under `/tmp`:

```text
.venv/bin/python -I scripts/prior_match.py results/prior_match_targets_20261021.csv /tmp/round4_recheck/raven_matches.csv results/prior_search_round4/data/20261021_raven
```

It returns **12 TIC-bearing records, zero period matches**, classifying the relevant RAVEN records as `TIC_ONLY_NO_PERIOD_FIELD`; the explicit CSV parsing below confirms four relevant matching stars. The existing positive RAVEN matches come from a mirror with a renamed `period` column. Evidence: `/tmp/round4_recheck/raven_matches.csv` and `.log`.

**Fix:** support `bls_per` and audit the real schemas already in the corpus; rerun the matcher and save a regression using the actual primary RAVEN header. Include provenance columns `label` and `cls` as well as the current flags (`prior_match.py:20` currently misses these two important classifier fields). Keep unknown-schema files in an explicit unresolved-input list, rather than treating a TIC-only/no-recognized-period result as a negative period search. The `.csv.gz`/same-record improvement is real; this is a remaining coverage defect, not a reason to revert it.

### R3 — locked clock-prior fields are not enforced; the tests have a stale-output failure mode

`make_conformance_configs_round4.py:31` stores a prior path and SHA. Nevertheless, `qlp_clock_test_sector.py:55–59` ignores both fields and reads its hard-coded `results/qlp_clock_v2/<TIC>.json`. The evaluator's clock checks at `prereg_conformance.py:231–235` do not bind the record to the locked c0 prior or config hash. A safe probe copied the 188664994 config, changed its sector to the permitted S84, supplied a nonexistent configured prior and an all-zero prior hash, and used the existing S84 file. The tool reached “no predicted events in this sector” instead of rejecting the invalid prior; it had read the hard-coded prior. Evidence: `/tmp/round4_recheck/bad_clock_prior.json` and `.log`. No S106+ data were used.

**Fix:** add an explicit round-4 validation wrapper or separately versioned validation step that checks the locked config identity, configured c0 path/hash and clock-record/config binding before data access/scoring, preserving the seven S106 configs and pinned evaluator if desired. Test altered prior bytes/path/hash and stale/wrong config binding. The primary flags are correctly assigned only to S112/S113/S117. There is no overall promotion function in the per-sector evaluator; that is not itself a blocker, provided reporting follows the locked rule and never substitutes a later success for a primary refusal.

The fresh input suite passed **56/56** in this re-check, using the same logic with child Python bytecode disabled and outputs in a fresh temporary directory (`/tmp/round4_recheck/config_tests.log`). However, `test_round4_configs.py:25–31` does not clear previous result files and ignores the subprocess exit code whenever JSON already exists. Extracting its unchanged `ev()` function and simulating exit 137 with an old INVALID_INPUT JSON returns that old result as a pass (`/tmp/round4_recheck/stale_probe.py` and `.log`). **Fix the harness** to use fresh output paths or remove old files, require the expected exit status, and verify the returned input identity. The successful fresh run remains valid; the current reusable harness is not a reliable future regression gate.

### R4 — the new prior-detections erratum must withdraw, not preserve, the “first human” distinction

The primary files substantiate the earlier RAVEN detections. They do **not** substantiate the assertion in `ERRATUM_PRIOR_DETECTIONS_2026-10-21_DRAFT.md:17` that “no human-reported candidate” remains literally true, or that this work is the “first human-vetted report.” A human-authored scientific paper can publish an automated candidate catalog. Absence from its later vetted/validated subsets establishes a different selection stage, not that nobody previously inspected the object or reported it. STATUS.md:10 repeats the new unsupported priority formulation.

**Exact replacement:** “TIC 80387959 was previously reported at P = 4.1922173881 d in the first-stage RAVEN candidate catalog of Lafarga et al. (2026). It is absent from their vetted and validated subsets. Our work independently recovers this signal, provides additional vetting and freezes predictions for a later observational test; we do not claim first detection.” Keep the earlier SPOC alert as an additional source. Neither RAVEN's first-stage score nor its absence from later subsets establishes a planet.

The exact online-availability date also needs care. The [Zenodo record](https://zenodo.org/records/19661443) displays publication date 2026-03-25 but technical creation date 2026-04-20; the [paper](https://arxiv.org/html/2603.22597v1) is dated 2026-03-23 and describes the first-stage table in §3.2.3/Table 1. Thus cite the catalog as “Lafarga et al. (2026)” or distinguish the displayed publication date from the archive creation date. I did not independently establish that the downloadable table bytes were already online on March 25. This date uncertainty does not affect their clear precedence over the October freeze.

### R5 — the supersession-template correction is still only partial

`prereg_v2.py:146` still selects “First freeze for this object” whenever `final_ephemeris.json` is absent, even for version >2. The second clause now names `V-1`, but does not remove that false first clause. The dated corrections to the three new registrations are useful; they do not fix future output. **Fix:** branch first on the requested version and actual preceding record, then render a single consistent introduction. Say “v4 supersedes v3” rather than “fourth version” unless all four versions actually exist. Verification: source inspection at line 146, the appended corrections, and the version inventory.

## Primary-source verification of the new erratum

The four local primary table MD5 values match the live [Zenodo file listing](https://zenodo.org/records/19661443): `nsfp09_table.csv` b2c597cfd78481c2e67f6ede2843b761; `vet_table.csv` 9967ea2d22ce8407453679cd51522dbd; `val_table.csv` 10be2f46161868fd218cc1ad43019183; `val_rp8_table.csv` effe3ada0e58efe3bde8bdeb28eafe37. Counts are 14815, 2170, 143 and 207 respectively. The nsfp09 SHA-256 is `7b4fb0b02a8597cad8ecc4ca1687be1e75ab5b04fb74e7232ad834944641df3a`. These were verified by hashing and parsing `results/prior_search_round4/data/20261021_raven/*table.csv`; no light-curve archive was opened.

| Erratum object(s) | Independently verified source values | Assessment |
|---|---|---|
| 80387959 | Primary `nsfp09_table.csv:2706–2707`: 4.19221738810686 d, score 0.98028445; 1.3973872442118918 d, score 0.93346214 | Period/score and approximate P/3 alias claims are correct. Absent from the vetted, validated and large-radius tables. Priority wording needs R4. The P/3 identification is a separate manual alias check, outside the matcher's P/2,P,2P rule. |
| 249813122 | Primary line 7825: 4.174528274171802 d, score 0.99940467; relative difference from saved P 4.1761465447 is 0.03875% | Correct period match and correction of “none.” |
| 333661705 | Primary line 10619: 1.3832408360973667 d, score 0.99830467 | Correct additional RAVEN credit; the table also has a distinct 10.661885-d detection. |
| 151767028 | Primary line 4832: 2.2103981294347577 d, score 0.983298 | Correct earlier detection, not validation; a 3P alias is also listed. |
| 343298093 | eumemic `results_public/vetted_signals.csv.gz`, decompressed line 64: 0.7661376546406703 d, inconsistent-transit-SNR flag | Correction is accurate. |
| 122522485 | eumemic `all_signals.csv.gz`, decompressed lines 7943/28917: 2.322156248573729 / 2.3221586025157146 d | Earlier raw-search output, not a promoted/validated candidate. |
| 159033763 | Same table, lines 14387/35098: 1.023264050305159 / 1.023263837072437 d | Same qualification. |
| 162304222 | Same table, line 862: 0.5237035345881501 d | Meets the 0.1% matching rule; write “within our period-matching tolerance,” not exact equality or proof that the physical source is identical. |
| 196514928 / 283913390 | eumemic `validation/false_alarm_classifier_table.csv.gz`, decompressed lines 3228/4027: P approximately 2.392127 / 2.481094 d, `label=real`, `cls=offset` | Correctly describes that classifier's labels; do not promote them into independent physical confirmation or host assignment. |

A safe rerun of the matcher on copied catalog tables under `/tmp/round4_recheck/safe_catalogs/` gives zero matches for 183374279, 61310956, 89247735, 188664994 and 195343302, one mirrored RAVEN match for 80387959, five table records for 151767028 and three for 343298093 (`safe_matches.csv`). The existing full-corpus output agrees on these positive/negative results. I also checked the primary RAVEN tables directly for all eight requested targets. These are bounded results, not proofs of novelty; fix R2 before making claims about a complete new matcher pass.

An independent directory-name scan reproduces exactly the ten TICs listed in DECISIONS 121: 317134140, 120444365, 120517801, 115692561, 19119739, 3367979, 65575657, 366047768, 383617106 and 333735955. None of the four requested “first-report” targets matches such a directory. Verification: filename-only walk of the eumemic/ahrazzle corpus directories, parsed `TIC<id>_P<period>` with the stated alias/tolerance rule; matches saved in `/tmp/round4_recheck/folders.json`. Directory matches are another bounded source check, not evidence about files that were never searched.

## Public statements requiring correction or a clearly linked dated notice

The public tree is intentionally still v1.14. The following is a release correction list, not a request to retroactively edit archived bytes. Sources were read directly with `rg -n` and line-numbered views.

| Location | What must change in the next public record |
|---|---|
| `public_release/README.md:87–89`; `public_release/REPORT.md:557–559`; `STATUS.md:10` | Replace the 80387959 “no human-reported” / “first human-vetted” distinction with the explicit RAVEN independent-recovery wording in R4. |
| `public_release/prior_search/VERDICTS.md:9` | Its stronger “no human-reported candidate anywhere” and “appears in no catalog, paper, repository or deposit” are false in light of the primary RAVEN table. Append a conspicuous correction and link it from the release summary. This location is missing from the draft erratum's current list. |
| `note_allsky/note.tex:18–22` and the corresponding next preprint version | The “no catalogued periodic signal ... within 60 arcsec” statement is false on the target itself; the no-human-candidate claim also needs R4. Narrow the no-TOI/CTOI statement separately from prior signal reports. Clarify that any absence claim concerns SPOC 2-minute TCEs, while the reported alert is from the distinct TESS-SPOC FFI pipeline; those two statements are not inherently contradictory. |
| `public_release/README.md:67`; `public_release/tables/allsky_classA_round2_outcomes.csv:5` | 249813122 prior “none” becomes prior RAVEN first-stage detection. The latter CSV also needs the notice, not just README. |
| `results/allsky_round3_outcomes.csv` and its public counterpart: rows/lines 2,11–15 | Correct “none found” for 122522485, 196514928, 283913390, 159033763 and 162304222 with the appropriate raw-search/classifier qualification; add RAVEN alongside brahle for 333661705. |
| `ddt_80387959/proposal.tex:16` | “Identified on October 18” is incomplete unless qualified as this team's independent recovery; acknowledge the earlier RAVEN candidate. Clarify “no SPOC 2-minute threshold-crossing event” and separately acknowledge the TESS-SPOC FFI S63 alert; the different pipeline names alone do not establish a factual contradiction. The earlier vetting corrections at line 21 are a separate known issue; this review did not audit whether all corrections have been communicated. Preserve the submitted proposal and attach a dated correction if updating the record; do not send anything as part of this review. |

## Integrity, tests and limits

All **45** current generator-produced frozen CSVs match their JSON and registration hashes; all **60** inspected public CSV copies match the corresponding local bytes. In particular, the three new round-4 hashes remain `befcc2e8…`, `4f14d1fe…`, and `0d450700…`. All eight config hashes match the prefixes printed in their amendments, and their current prior hashes match the current files. A reconstruction from the original v2 generation text, freeze-script descriptions and unchanged frozen numerical inputs reproduces each original registration prefix exactly before the appended amendment: 7457, 10746 and 7026 characters respectively for 151767028, 343298093 and 188664994. Evidence: `/tmp/round4_recheck/integrity.py`, `.json`, and `registration_prefix.py`. No original scientific-body edit was detected.

The new 188664994 prior was checked against fresh JPL vectors at six control times each in S84 and S81: c0 = 0.03248492436856831 min, versus stored 0.03248492436739603 min; maximum control-sample discrepancy 2.35×10⁻¹² min. Evidence: `/tmp/round4_recheck/c0.py` and `.log`. This numerical agreement does not fix the missing runtime binding in R3.

The configuration suite's fresh 56/56 pass and the adversarial prior/stale-output probes are reported above. The seven S106 configs and public_release working tree remain unchanged. I did not rerun the entire multi-year photometric pipeline, open any prohibited test data, infer what the author personally examined, or verify every historical availability date. The primary catalog bytes were authenticated against the live Zenodo listing; the paper's candidate-stage distinction was checked directly. The RAVEN online-file date and universal “first human-vetted” priority were not established. Publish only after the specific remaining code, ground-registration and credit fixes above have been reviewed.
