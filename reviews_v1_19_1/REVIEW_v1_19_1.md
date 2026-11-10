> Public copy (2026-11-10 (v1.19.2)): 2 local temporary paths replaced by "[reviewer temporary path redacted]". No other change.

# Post-publication review of v1.19.1

Reviewed 2026-11-10 UTC by Codex, independently of the release assembly. Scope: commit `a8493bfd6928876aba324bd136af85f46440778a`, tag `v1.19.1`, and Zenodo record `24096235`, compared with `v1.19`. Paths below are relative to `/Users/fernando/Desktop/NASA`; line numbers refer to the inspected files, whose published copies were checked against the tag.

## Verdict

**Needs a corrective release now: a documentation-only v1.19.2.** Preserve v1.19.1, its tag, archive, manifest, forecast outputs and all frozen inputs. Publish dated corrections, not replacement history. The principal reasons are an undisclosed breach of the S108 monitoring interval, overbroad data-integrity statements, and a timestamp correction currently confined to the local log. The numerical eligibility forecast survives this audit; there is no evidence here of a changed S106 scoring rule or a reason to withdraw those tests. A local correction alone is insufficient for readers of the public release.

This is an audit judgment based on F1–F7 below, not a claim that the timestamp errors invalidate the frozen tests. A publicly dated correction attached to both release locations could convey the necessary information, but a small corrective release is the clearest way to make all the affected documents, disclosure and manifest consistent before scoring. Nothing was published or changed by this review except this report.

## Verification and boundaries

I inspected the local scripts before execution, read the full extracted DRN text, independently extracted it from the PDF, and visually checked its observation table on PDF page 5 (printed page 1). I re-ran the DRN forecast with only its two output destinations redirected to `[reviewer temporary path redacted]`. The wrapper disabled bytecode writes, intercepted FITS opens, restricted them to S68/S69/S96/S105, and checked the headers against the allowed filenames. It recorded 15 opens, all in those four sectors. I did not run the original forecast's noise-fitting stage, any selection/designation/ledger command, or any prohibited test-sector photometry analysis. No credentials were read.

Public reads were the [Zenodo record API](https://zenodo.org/api/records/24096235), its linked release ZIP, the [GitHub release API](https://api.github.com/repos/fergmolina/tess-transit-candidates/releases/tags/v1.19.1), the [S111 target-list CSV](https://tess.mit.edu/public/target_lists/2m/all_targets_S111_v1.csv), and a HEAD request to the [QLP S106 directory](https://archive.stsci.edu/missions/hlsp/qlp/s0106/). The ZIP contains no FITS files; its 880 entries were compared with Git blob hashes. No science product was requested from MAST. The QLP directory returned **404**, with server date **2026-11-10 03:55:09 GMT**. Thus I did not find QLP S106 available at that endpoint; I did not fetch it. That observation is not a measurement of the first release time of every QLP product.

Reproduction scripts, raw public responses, file-time inventory, comparison results and output copies are under `[reviewer temporary path redacted]`: `audit.py`, `integrity.json`, `forecast_audit.py`, `forecast_audit.txt`, `fits_open_inventory.json`, `final_checks.py`, `final_checks.txt`, `archive_check.json`, `zenodo.json`, `github_release.json`, and `qlp_s0106_head.txt`. Important evidence is also recorded below so the report does not depend on temporary files surviving.

## Findings, ranked by severity

### F1 — Material monitoring deviation: S108 was not checked at least weekly

**Evidence.** The v1.18 rule at `public_release/scoring_317134140_s108_s110/README.md:41–43` says checks are made at least weekly. The `query_utc` fields at line 8 of the three public S108 records are:

| Record | Query time UTC | Interval from preceding check |
|---|---|---|
| `sel_20261025T000412Z.json` | 2026-10-25 00:04:12.835692 | — |
| `sel_20261101T223201Z.json` | 2026-11-01 22:32:01.307139 | **7 d 22:27:48.471447** |
| `sel_20261108T031352Z.json` | 2026-11-08 03:13:52.936804 | 6 d 04:41:51.629665 |

These files are under `public_release/monitoring/selection_records_317134140/S108/`. I parsed the timestamps and subtracted them. The first interval exceeds seven days by **22 h 27 min 48.471447 s**. Calling them weekly checks without recording this exception (`public_release/monitoring/README.md:10–13`; release notes line 17) implies better compliance than the saved evidence supports. A Sunday date in each calendar week does not meet a maximum seven-day interval.

**Consequence.** All saved checks are legitimately NONE, but they cannot exclude a product appearing and disappearing in the extended interval. The lock already acknowledges replaced deliveries (`README.md:21–22,38–43`); it does not prescribe automatic invalidation for a late check. Do not invent an invalidation or silently redefine “weekly.”

**Exact dated correction:**

> The S108 monitoring schedule was not fully met. The checks at 2026-10-25T00:04:12.835692Z and 2026-11-01T22:32:01.307139Z were 7 days 22:27:48.471447 apart, exceeding the locked seven-day interval by 22:27:48.471447. Both retained records are NONE. This does not establish continuous unavailability or exclude an intervening replaced delivery. The original records, selection rule and cutoff remain unchanged. Subsequent checks will be scheduled no more than seven days apart, with the locked final check retained.

Add this to the public log and monitoring README, and reference it in the corrective release notes. Do not create a retrospective check.

### F2 — Material qualification needed for data-integrity and availability claims

**Evidence.** `public_release/monitoring/README.md:3–4` and `zenodo_upload/RELEASE_NOTES_v1.19.1.md:3–4` say no test-sector photometry of any frozen star “has been downloaded, opened or analysed.” Yet the unchanged public erratum explicitly records a downloaded S106 cutout of TIC 206620592 on 2026-10-20 at 01:21:13 UTC, reportedly unopened (`public_release/preregistration/ERRATUM_S106_DATA_AVAILABILITY_2026-10-20.md:31–40`), also retained in `public_release/conformance_v2.1/CONFORMANCE_PROCEDURE_v2.1.md:218–221`. I compared these texts; I did not inspect the cutout. The new wording needs an explicit scope to the v1.19.1 work and a reference to the historical caveat.

The claim that no QLP S106 light curve **existed** when the release was written is stronger than the recorded checks: note lines 3–5 cite a November 8 directory 404, while local item 212 explicitly says availability was not rechecked at publication (`logs/DECISIONS.md:2160–2161`). Public item 207 also records a November 9 404 (`public_release/DECISIONS.md:2083–2092`), so “last checked November 8” is itself inconsistent with that log. My later HEAD response remains 404; it supports current absence at that endpoint, not the global historical nonexistence assertion. Non-examination by earlier participants remains their attestation, not something this audit can prove.

**Exact dated clarification, to use in the note, monitoring README, main README block and release notes:**

> The work reported in v1.19.1 used mission documents, metadata and previously examined in-sample QLP files; it did not acquire or examine test-sector photometry. This statement does not supersede the earlier S106 data-availability erratum, including its disclosure of a downloaded, reportedly unopened TIC 206620592 S106 cutout. The log records QLP s0106 directory checks returning 404 on November 8 and November 9; no publication-time check was retained. These checks do not establish the first availability time of every QLP light curve. The authors' non-examination statement remains an attestation.

The main README's new block (`public_release/README.md:221–232`) calls the forecast descriptive but omits the explicit controlling rule present in the other three locations. Append:

> These are conditional forecast counts, not scores or changes to eligibility. The locked evaluator, its required clock record, and the selected QLP v01 file determine the outcome of record. No test or event is discarded or replaced on the basis of this forecast.

### F3 — Medium: public timestamp repair is incomplete; file times do not prove exact log-entry times

**Evidence.** Public items 209 and 210 are stamped 02:50 and 02:40 UTC (`public_release/DECISIONS.md:2115,2135`), later than their containing commit at **02:38:49Z**. Item 210 already corrects item 209 to “about 02:25”; it does not correct its own stamp. Local item 211 is stamped 02:55 but describes pre-publication assembly; local item 212 explains all three estimates (`logs/DECISIONS.md:2141–2166`). I verified Git author/committer/tagger times and the public API timestamps, not merely the author's report:

- Commit and annotated tag creation: 2026-11-10 02:38:49 UTC.
- GitHub release publication: 2026-11-10 02:38:53 UTC.
- Zenodo record creation: 2026-11-10 02:38:58.133488 UTC.

The file-time evidence is consistent with the approximate reconstruction, but not exact proof of entry creation: forecast outputs were written at 02:24:41; public DECISIONS, manifest and release notes at 02:29:18. The present local log mtime is 03:35:36, after further appends. It cannot independently resolve when each earlier paragraph was written. Therefore item 212's “True times from file times” should be qualified.

**Exact public correction:**

> Items 209 and 210 in v1.19.1 carry estimated, erroneous timestamps of 02:50 and 02:40 UTC. Item 210 had already corrected item 209 to approximately 02:25. The forecast output mtimes are 02:24:41 UTC and the assembled public log mtime is 02:29:18 UTC. These support approximate reconstruction, not exact entry-writing times. Local item 211's 02:55 timestamp is also erroneous; the manifest was assembled at approximately 02:29:18 UTC. The containing commit is dated 02:38:49 UTC; GitHub records release publication at 02:38:53 UTC and Zenodo records creation at 02:38:58.133488 UTC on 2026-11-10. The public release anchors establish the existence of the released bytes. Original entries are preserved; no earlier public timestamp is claimed.

Publish this now with F1/F2 rather than leave it only in local item 212. Exact evidence and limits for the other stamps are tabulated below.

### F4 — Low numerical severity: “all 49 rows reproduce exactly” and “joint SNR carried over” are not literally true

**Evidence.** The assertion in `scripts/conformance_s106_forecast_drn144.py:58–59` compares **only `n_eligible`**. My independent join on TIC/template confirms all 49 `n_pred`, `n_eligible`, `eligible_epochs` and `snr_event` values match. However, **19 of 49 joint SNR values differ by 0.01**. For example, TIC 120444365/S68cam1 changes from 4.76 (`public_release/conformance_v2.1/results/conformance_v21/s106_forecast.csv:9`) to 4.77 (`public_release/monitoring/s106_drn144/s106_forecast_drn144.csv:17`).

The original forecast calculates joint SNR from unrounded depth/error (`scripts/conformance_s106_forecast.py:46,53`). The update reads the rounded two-decimal `snr_event` and multiplies it by sqrt(n) (`scripts/conformance_s106_forecast_drn144.py:47,60–61`). Thus the statement at note line 61 that both per-event and joint SNR values are carried over is inaccurate. This has **no effect on the eligibility table or locked scorer**.

**Exact correction** to note lines 35 and 61, and the corresponding item 209 statement:

> For all 49 case-(a) rows, the predicted-event counts, eligible-event counts and eligible-epoch lists reproduce the published forecast; per-event SNR values are copied. The script's original assertion checks eligible-event counts only. Joint SNR is recalculated as the published rounded per-event SNR times the square root of the eligible count, rounded to two decimals. Consequently 19 case-(a) joint SNR entries differ from the earlier forecast by 0.01. No eligibility result changes.

No need to replace the published CSV. If a future explanatory script strengthens assertions, compare keys and epoch lists as well as counts and label its revision; do not alter a locked evaluator.

### F5 — Low: public redaction disclosure and privacy assertions need precision

**Evidence.** The v1.19 log is a byte prefix of the new public log. I reproduced the masking transformation through item 210 in memory: the old v1.15 prefix is retained, later temporary paths are redacted, and the pair of recipient names is replaced by a role. This matches the public bytes exactly. The implementation is `scripts/make_public_decisions.py:11–20`; its newly added recipient-name policy is disclosed in **local** item 211 (`logs/DECISIONS.md:2150–2151`), which is absent from v1.19.1. Public item 205 uses the role but does not identify it as redaction.

A scan plus inspection of all 19 changed files found no new email address, session URL or session job path. It did find the inherited temporary paths in public DECISIONS lines 529 and 935, retained unchanged and already disclosed in item 163 (lines 1383 onward). The newly copied forecast includes the author's absolute workspace path at line 16, consistent with the old forecast's absolute path. Therefore local item 211's unqualified “no ... temporary path in any changed file” is false when applied to the whole changed DECISIONS file; the assembler actually exempts the historical prefix (`scripts/assemble_v1_19_1.py`, privacy scan). There is no evidence here of a new credential leak, but that is a scoped scan result, not a universal privacy guarantee.

**Exact public disclosure:**

> In the public copy of item 205, the two private-email recipient names are replaced by “the two contacts named on the mission's DDT page.” This is a role redaction only; the reported action and date are unchanged. The v1.19 log remains a byte prefix. Previously published temporary paths in the historical prefix remain as disclosed in item 163; no new temporary or session path was introduced by this release. The forecast retains the existing absolute workspace-path convention.

Do not rewrite the historical prefix. Disclose this masking policy in the corrective public log.

### F6 — Low, interpretive: add omitted DRN context and make the forecast's limits explicit

**Evidence.** DRN §1.2 says ACS excursions can generate erroneous TCEs; §2.2 warns that many two-transit detections at periods 8–20 days are likely false positives. Appendix A explicitly includes Manual Exclude bit 8 among FFI flags, and describes scattered-light/bad-calibration flags. These are in `results/s106_drn144/tess_sector_106_drn144_v01.pdftotext.txt:227–260,363–377,443–468`. The note discusses ACS noise and unknown QLP flags, but omits the FFI flag context and warning about spurious two-transit signals. They matter when interpreting few-event QLP tests, although they do not authorize changing any scoring rule. DRN Table 2's named aperture/no-light-curve exceptions contain none of the seven S106 TICs; I compared the seven IDs with the extracted table.

The forecast calls the same edge/coverage functions and thresholds, but does **not** execute the full evaluator on a test product. It fixes cadence at 200 s, omits the target light-travel correction and test clock correction, lacks actual QUALITY/finite-flux/detrending masks, and cannot establish the full strict-epoch flag veto. Compare forecast lines 34,48–62 with evaluator lines 76–98,209,225–255,355–364. Case (c) gives the greatest counts among the reported gap-added scenarios, but is an optimistic gap-only scenario, not a bound on real-data outcomes or a calibrated probability. The original procedure explicitly says template fractions are not calibrated probabilities (`public_release/conformance_v2.1/CONFORMANCE_PROCEDURE_v2.1.md:181–186`).

**Exact additional limitation:**

> DRN 144 also warns of spurious transit detections from ACS systematics and many likely false-positive two-transit SPOC detections at periods of 8–20 days. Its Appendix A includes Manual Exclude among FFI flags; this does not establish how QLP will propagate those flags. Scattered light and calibration effects may further affect usable data. None of these warnings is a new rejection rule. The forecast uses ideal 200-second cadences and the evaluator's edge/coverage functions, not its full product preprocessing, clock correction or strict flag veto. Template fractions are scenarios, not outcome probabilities. Case (c) is an optimistic segment-only scenario under the stated timing approximation, not a guaranteed bound or score.

For TIC 183374279 add:

> Both strict epochs, 245 and 246, must be eligible **and** pass the locked nominal-window gap/flag check. `strict_all_eligible` tests only membership in the forecast eligible set; True is not a prediction that the strict veto will pass.

This clarifies a necessary-versus-sufficient condition; the existing “unless both ... eligible” statement is not itself an incorrect reading of the lock.

### F7 — Editorial: quick-check hash attribution is wrong

`public_release/monitoring/s106_drn144/superseded/README.md:8` says the two quick-check files are versions “hashed in DECISIONS 208.” I read the whole item (`public_release/DECISIONS.md:2095–2114`): it gives the DRN PDF hash, not hashes of those two files. Their bytes do match the local quick-check sources and the manifest. Replace this sentence in a dated clarification with:

> The quick-check files are retained byte-identical to their local source copies. Their SHA-256 digests are recorded in MANIFEST_v1.19.1.md; item 208 identifies the files and the superseded calculation but does not give their digests.

The prominent SUPERSEDED heading, “Do not use its counts,” item 209 and the note's final section otherwise label the old result adequately. Item 209 corrects the misleading eligibility counts; F4 qualifies its separate exact-reproduction claim.

## Detailed verification results

### 1. Published bytes and assembly

| Check | Independently verified result |
|---|---|
| Commit/tag | Local tag resolves to `a8493bfd6928876aba324bd136af85f46440778a`; GitHub API reports `v1.19.1` and the release times above. |
| Manifest | All **18/18** SHA-256 entries match both tagged blobs and working copies. Manifest SHA-256 is `be93520d9d74fbf0cb0294165d05466bdb7c2253aa5c87a876cc8804fc4eacf1`. |
| Changed set | `git diff --name-only v1.19 v1.19.1` equals exactly those 18 paths plus `MANIFEST_v1.19.1.md`: 19 files. No other tracked file changed. |
| Frozen inputs | All **68** prediction CSVs under public preregistration are byte-identical across the two tags. No locked config/evaluator/registration changed, established by the exhaustive changed-set comparison. All seven local S106 configs equal their public copies. |
| Source copies | Note, forecast script/CSV/TXT, both quick-check files, five selection records and orbit snapshot match the corresponding local sources byte-for-byte. The old forecast, old forecast CSV and evaluator equal their published copies. Evaluator SHA-256 is `a864b07ace8d3220a2d94a60513a488c8a5d87b54f41ebf510ff40ef1755311f`. |
| Generated text | I inspected assembler literals against the README blocks, superseded label and DDT append; independently reproduced the public-log masking through item 210. I did not rerun the mutating assembler. |
| Release notes | Local SHA-256 `cd6189ab8bf244f4f13e787c11bac0b93fd8400dd1ae9b4b6c4240c84451702c`, matching item 211. Zenodo's rendered description contains the same release assertions. |
| Zenodo | API lists one ZIP, **10,727,173 bytes**, `md5:e0cc9ad214e30400721a91c8c62ae091`; downloaded archive matches this size and MD5. Its **880-file path set and every Git blob hash** equal the tag. The archive root's suffix `3102c3c` is not the stated commit prefix, but the exhaustive content comparison establishes byte identity; do not infer a content mismatch from that folder label. |

Source: local Git object comparisons and `integrity.json`; [Zenodo record](https://zenodo.org/records/24096235), public API and `archive_check.json`. No additional unmanifested change was found.

### 2. DRN 144 facts and time arithmetic

The retained PDF is **1,680,677 bytes**, SHA-256 `3fc6c8f03058ae5426b7291c26a27b91e754c1e9d941c75daeebc1e18c682889`. Fresh `pdftotext -layout` output is byte-identical to the retained extraction. Its title page is dated September 03, 2026. These checks support note lines 9–12. Source: the retained PDF and [official DRN URL](https://archive.stsci.edu/missions/tess/doc/tess_drn/tess_sector_106_drn144_v01.pdf); I did not treat the PDF's document date as its web publication date.

- Reading the entire text found no reported S106 clock, timestamp or barycentric-correction fault. This verifies **“the DRN reports no timing issue,” not “the QLP clock is verified.”** The locked clock gate still applies.
- DRN §1 and Table 1 support the missed downlink, recorder overflow, dates and all eight segment endpoints in the note and script. The four segment durations sum to **25.42637 d**, rounding to 25.43 d. The overflow-to-resume elapsed interval is **2.60416 d**, not 2.39 d; **2.39 d is the DRN's lost-science-data figure**, which excludes scheduled downtime. The note distinguishes these correctly. Its reported UTC gap is 2 d 14 h 30 min.
- I converted 2026-07-30T19:21:09 UTC and 2026-08-02T09:51:09 UTC with Astropy to JD(TDB)−2457000: **4252.307154899** and **4254.911321566**. These agree with the table within its rounding. The table values are spacecraft TJD, not target barycentric times; the ignored target correction is a stated approximation, not a hidden UTC/TDB confusion.
- §1/§1.2 support first full-sector ACS 5.11 operation, correlated excursions despite the usual 7-arcsec criterion, concentration near the end of half-orbits 1/2/4, and **3.39 d** flagged. The >3-arcsec, wheel-frequency-crossing and >15-Hz conditions in item 208 accurately summarize the listed criteria. The note's shorter summary is accurate. It does not establish any QLP-specific flag count.
- The saved orbit table does omit the overflow gap: its S106 rows still carry orbit 224a through August 2 05:00 UTC (`catalogs/TESS_orbit_times.csv:318–321`; same rows in the new snapshot). DRN-related omissions needing context are F6.
- The aggregate counts in item 208, 13,000 two-minute targets, 2,121 twenty-second targets, 640 TCEs on 484 targets, agree with §1.1 and Table 3. No target photometry was used to make this check.

### 3. Forecast reproduction and boundary behavior

The redirected run completed successfully and reproduced the published new CSV **and TXT byte-for-byte**. Both the script's 49 count assertions and my independent epoch-list comparison pass. SNR differences from the older forecast are F4.

The gap application is a **union**, not a second sequential trim: orbit-table breaks, mapped template gaps, and the open SSR interval are removed before one call to `edge_trim` (`forecast.py:35–40,48–52`). It never reintroduces points removed by a template. The SSR removal is strictly `4252.30716 < t < 4254.91132`; no generated case-(a) cadence lands exactly on either endpoint, so using inclusive comparisons would remove **zero additional cadences in these seven templates**. Case (c) uses `np.arange(start,end,CAD)`, including starts and excluding ends.

The edge rule is correctly applied to the surviving cadence train: 1.5 d after starts/resumes across gaps >0.5 d, and 0.5 d before gaps >0.1 d/end (`scripts/prereg_conformance.py:113–125`). Trims are referenced to surviving cadences, not necessarily the ideal DRN timestamp. In case (b), the first resume after the SSR gap ranges from **4254.917523693 to 4254.936536793** because the old scheduled/template break also applies. The first retained post-resume sample ranges from **4256.419838508 to 4256.438851608**, safely after epoch 563 at approximately 4255.007. For S68cam1, the last pre-overflow sample is 4252.306863375 and the last retained pre-gap sample is 4251.804548560. S96cam1 and S105cam4 have earlier retained ends because their existing mapped gap/trim also removes that interval. This is expected union behavior, not accidental double application of an edge rule.

For case (c), `edge_trim` detects starts 4233.42522 and 4254.91132, and four pre-gap/end points; it removes 2,166 cadences and keeps 8,820. These direct outputs confirm the intended long-gap resume treatment.

Coverage is the evaluator's actual nearest-cadence transit grid and baseline point-count calculation (`scripts/prereg_conformance.py:136–143`), with thresholds **0.9/0.5/0.5**. The forecast uses **200/86400 d**, whereas the evaluator estimates cadence from its retained time series (`:243,255`) and applies clock/detrend filtering. Replacing the synthetic cadence constant by the measured median changes no eligibility result. Thus this is faithful reproduction of the published *forecast method*, not an exact forecast of the eventual product processing.

As a sensitivity check only, I shifted the synthetic retained times by ±8 minutes. Most counts stayed fixed, but TIC 115692561/S105cam3 gains epoch 3389 for −8 minutes (17→18 events), and its case (c) loses epoch 3403 for +8 minutes (24→23). Neither change affects the fewer-than-two question. These are perturbations, not measured target corrections; they illustrate why case (c) and individual marginal counts must remain conditional.

### 4. Re-derived eligibility table

I grouped the reproduced CSV by TIC/case, recomputed min/median/max and counted rows below two. Every entry in the note's table matches:

| TIC | Predicted | a min/median/max | b min/median/max | c | Below two, a → b |
|---|---:|---|---|---:|---|
| 253931796 | 3 | 0/1/1 | 0/1/1 | 1 | 7/7 → 7/7 |
| 183374279 | 3 | 1/1/2 | 1/1/2 | 2 | 5/7 → 5/7 |
| 70441745 | 2 | 1/2/2 | 1/2/2 | 2 | 1/7 → 1/7 |
| 120444365 | 6 | 2/2/3 | 1/2/2 | 3 | 0/7 → 1/7 |
| 122522485 | 12 | 6/7/10 | 5/6/8 | 9 | 0 → 0 |
| 206620592 | 26 | 13/16/20 | 12/13/17 | 20 | 0 → 0 |
| 115692561 | 32 | 16/19/23 | 15/17/19 | 24 | 0 → 0 |

- **253931796:** expected INSUFFICIENT is supported conditionally by all modeled cases, including case (c). It was already below two in all old templates. This is not an observed outcome, nor permission to skip the eventual test.
- **183374279:** I read `strict_epochs: [245,246]` in the unchanged config and followed `strict_epoch_check` and `override`. S68cam1/S69cam2 contain both epochs in a/b; the other five contain only 245. Case (c) contains both. The full override additionally rejects flagged/non-finite/missing nominal-window cadences, even if a 90% coverage test passes (F6). Epoch 245 at about 4238.39 is approximately 1.65 d before the first segment's end; the warning is contextual, not evidence that its cadences were actually affected.
- **120444365:** epoch 563 was eligible in **four**, not all seven, old templates and is eligible in none after the gap. Counts fall by one in those four and are unchanged in the other three. The detailed note is correct; the main README/release-note shorthand “loses one event” should be read with this qualification.
- **Many-event tests:** maximum per-template losses are 2 (122522485), 3 (206620592), and 4 (115692561). The minimum retained count across these b scenarios is five. The note's “at most four” and “at least five” are correct for these scenarios, not guaranteed properties of real S106.

### 5. Integrity of the tests

The unchanged Git objects and source comparisons establish that this release does not change a lock, outcome criterion, input selection or frozen prediction. Inspecting the forecast shows no data-driven choice of a favored template: all seven old templates and the explicitly optimistic scenario are published. It creates no new outcome-of-record branch. Reading sector-wide mission text can affect expectations, but with the already fixed evaluator it does not itself select a new test. The statements in the note (lines 3–5,65), monitoring README (8–9), and release notes (13–14) reserve decisions to the actual QLP file/evaluator; the main README should add that explicit sentence as specified in F2.

The old quick check is preserved, correctly superseded in substance, and its optimism is corrected in item 209. The remaining issues are public accuracy and qualification, not a reason to choose another sector, drop unfavorable strict epochs, or reinterpret INSUFFICIENT as a successful test. Full historical non-examination cannot be independently proved by hashes or a filename inventory; the earlier erratum's caveat remains operative.

### 6. Selection records and S111 end

All five public selection files equal their local counterparts byte-for-byte. Each contains empty observations/products, no candidates, status NONE and selected null. I independently canonicalized the response object as specified at `scripts/spoc_selection.py:29,41`; all five reproduce SHA-256 `5c44c2c80fbbdf1233b79a6a228e328591e3907d4c97bdf3e7f98c5c68080d36`. This verifies retained content and response consistency, not a separate replay of the historical MAST query or proof that a JSON record was never edited before retention.

The first S108 check was 23 min 41.835692 s after the stated lock time; the first S109 check was 1 d 03:37:02.582335 after its October 31 18:55 UTC end. The S109 inter-check gap was 6 d 04:41:51.546184. Those timings fit prospective weekly monitoring; the S108 interval exception is F1. S110 checks should begin **2026-11-26 04:15 UTC**, not at midnight: this is the end in the v1.18 locked table (`README.md:31–43`). The monitoring README's date-only statement is compatible but should retain that time in execution.

The orbit snapshot is byte-identical locally/publicly, SHA-256 `abb6108a46ef938601d63d6284f3da38fba1f1c24bfca573719e088fa39bc113`. Rows 338–342 list all four S111 segments and S112's first segment. Taking the maximum S111 “End of Orbit” gives **2026-12-22 08:30 UTC**. Adding 120 and 365 days gives **2027-04-21 08:30 UTC** and **2027-12-22 08:30 UTC**, exactly as item 206 states. The v1.19 config's `designation_rule` requires N+1 in the table and the first complete snapshot at or after sector end; these are provisional cutoffs until that operative snapshot, as item 206 already says.

I read all seven local `results/s111_ledgers/*/ledger.jsonl`: each contains only its initialization entry. Thus the retained evidence supports “nothing designated yet.” No designation command was run. The public S111 target-list read has hash `a43c99620d421ec37f31ac8d6f52d81bf5047136f4f5d89b329bd9e563c038ff`, matching item 201's prefix; its row contains TIC 80387959 (camera 4, CCD 3, Tmag 10.52) and none for 120517801. That is target-list metadata, not an operative designation or confirmation of a DDT award.

### 7. Timestamp evidence for items 204–212

File times below are mutable local corroboration. They are not trusted remote attestations and cannot recover per-entry writing times from a repeatedly appended log.

| Item / printed UTC stamp | Available independent evidence | Assessment |
|---|---|---|
| 204 / Nov 1 22:35 | S108/S109 JSON queries 22:32:01.307139 / 22:32:02.582335; file mtimes 22:32:02.505415 / 22:32:03.059258 | Consistent sequence; exact log time not independently recoverable. |
| 205 / Nov 1 22:44 | Local DDT correction/README mtimes 22:44:36.969999 / 22:44:37.019315; explicit author-report addendum | Consistent with recording the follow-up then; does not verify transport/delivery or exact sending time. |
| 206 / Nov 8 03:20 | Selection queries 03:13:52.936804 / 03:13:54.128519; file mtimes 03:13:54.057228 / 03:13:54.626539 | Consistent with a later monitoring entry; snapshot content verifies the end date, not historical HTTP headers. |
| 207 / Nov 9 13:40 | Entry reports bot 13:30 and confirmation 13:34; no independently authenticated historical response examined | Plausible but not independently verified to the minute. Do not promote an assertion to a measured timestamp. |
| 208 / Nov 10 01:40 | PDF/extracted text mtimes 01:28:23.888081 / 01:28:24.118720; quick-check output 01:29:31.349575 | Artifacts predate stamp; compatible, not proof that the log was written at 01:40. |
| 209 / Nov 10 02:50 | Forecast CSV/TXT 02:24:41.210266 / 02:24:41.217960; present in public log assembled 02:29:18.214349 and committed 02:38:49 | Printed stamp wrong; “about 02:25” is plausible, not exactly established. |
| 210 / Nov 10 02:40 | Included in the same 02:29:18 assembled log and 02:38:49 commit | Printed stamp wrong; “about 02:28” is plausible, not exactly established. |
| 211 / Nov 10 02:55 | Assembler mtime 02:29:18.023189; manifest birth/mtime 02:29:18.270516/.271133; release notes 02:29:18.271223 | Assembly occurred at about 02:29:18 on retained file times. Entry-writing time not recoverable; 02:55 misstates the pre-publication chronology. |
| 212 / Nov 10 02:40 | GitHub 02:38:53; Zenodo 02:38:58.133488 | A 02:40 publication report is chronologically consistent. Its exact append time is not separately established. |

The tagger timestamp is **02:38:49**, not 02:38:53; the latter is the GitHub release publication time. Item 212 groups “tag and GitHub release” together and should distinguish them in the correction. The UTC publication date is November 10, even though the local US/Eastern date is November 9; CITATION's date is not a timezone error.

### 8. DDT correction and publication metadata

The entire v1.19 DDT correction is an exact byte prefix of the v1.19.1 version; only the four-line dated addendum was appended. Its description matches public/local item 205 and the November 1 local correction addendum. The proposal PDF/TeX and target-list mtimes remain October 19, consistent with the stated unchanged attachments, but no retained sent-mail headers or delivery receipt were examined. Consequently **reported sent/delivered by the author** is supported; independent proof of delivery is outside the retained evidence. No contact was made. The local DDT README's older parenthetical associating the October 20 email with the October 21 correction is confusing, but the published addendum and item 205 clearly distinguish the two; no alteration of the historical public correction is needed.

CITATION's version `1.19.1` and date `2026-11-10` match GitHub/Zenodo. Its DOI `10.5281/zenodo.23443244` is the concept DOI: the public API's version relation identifies parent record 23443244, whereas this version is 24096235. That is not a wrong DOI; use the version DOI for exact reproducibility, as the existing README citation guidance recommends. Title/author/license/ORCID agree with the public record. The publication record does not falsely claim a new external review; local items 211–212 expressly state there was none, and the older review-chain statements refer to older locks.

## Required corrective-release scope

Publish the dated text in F1–F7 with a fresh manifest and explicit links from the note, README, monitoring index and release notes. Include the qualified timestamp correction and name-redaction policy in the public log. Keep v1.19.1 available and preserve all original records and hashes. Do not regenerate forecasts to improve counts, revise locks, acquire test data for this correction, or backfill missing monitoring records. The correction should state that the eligibility table is reproduced, the SNR differences are rounding-only, and the eventual locked evaluator still decides every test.

The present review changes only this report. Its recommendation to issue v1.19.2 is not authorization to publish or modify the release.
