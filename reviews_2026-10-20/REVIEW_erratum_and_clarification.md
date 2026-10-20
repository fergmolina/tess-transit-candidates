# Independent publication review: data-availability erratum and timing-rule clarification

**Date:** 2026-10-20 UTC (2026-10-19 locally, EDT). **Reviewer/tool:** OpenAI Codex, shell/Python, FITS-header inspection, PDF text extraction and public HTTP/web access. **Workspace:** `/Users/fernando/Desktop/NASA`.

**Sources actually opened:** both proposed corrective documents; the previous timing review; current generator/evaluator; frozen registrations, ephemeris JSONs and prediction CSVs; decision logs; the named manuscript, protocol, dossier, proposal and email sources; local/cached public-release copies; local S106/S107 FITS headers and filesystem metadata; MAST bulk-download lists, holdings and DRN pages; the MAST TICA notice; the public GitHub head API; the Zenodo two-candidate preprint API/PDF; and the previously downloaded, independently acquired protocol APIs and archived protocol/evaluator files, reopened and rehashed here. I did not inspect actual holdout-sector flux. I ran historical-data generator tests only in temporary copies and used synthetic objects for the test-sector guard checks. Evidence identifiers below apply to all factual entries in the corresponding paragraph or table.

## Verdicts

**A — `ERRATUM_S106_DATA_AVAILABILITY_2026-10-20.md`: publish after listed fixes.** Its central correction is necessary and supported: the broad assertion that S106 data were unavailable at the freezes is wrong. The quoted local time converts correctly to approximately 16:45 UTC. However, the retained files do not substantiate the stated count of 899 downloads on that date; the affected-record table omits later S106 freezes and analogous S107 claims; the non-examination statement must be identified as an author attestation, with the later TIC 206620592 cutout disclosed; and the process promises are not implemented. Name TIC 88407114 and mark its S106 test withdrawn in the active record. Preserve the predictions and historical releases while making the correction discoverable beside them. These are publication blockers for the draft **as written**, not reasons to withhold an accurate erratum. [A,L,F,G,H; reviewer judgment]

**B — `CLARIFICATION_TIMING_RULE_2026-10-20.md`: publish after listed fixes.** The revised chronology, mathematical impact, 37-file count, three v1 retractions, byte-preservation distinction and evaluator caveats substantially address the earlier review. The max() rule demonstrably predates this correction, but not every object registration. Keep its adoption explicitly dated and scoped. Replace “For every object” with the affected, non-withdrawn TESS-v2 scope; qualify “before any test photometry is evaluated/inspected” because the withdrawn TIC 88407114 S106 data were already fitted; give the exact aggregation in the generator instead of “depth-weighted”; and link the availability erratum. Public dissemination and conformance testing remain pending. Publication of an accurate clarification need not wait for a new evaluator, provided no outcome is certified as satisfying the written protocol in the meantime. [B,P,C,H,I; reviewer judgment]

## Evidence and methods

- **[A: availability]** Ran the requested `find data -iname '*s0106*' -exec ls -l -D '%Y-%m-%d %H:%M %Z' {} +`, saved to `/tmp/erratum_review/s106_ls.txt`; independently inspected `stat().st_mtime`, `st_birthtime`, and FITS primary/extension headers, without accessing flux arrays. `/tmp/erratum_review/local_audit.py`, `late_files.json` and `local_audit.txt` record the inventory. Read the [MAST bulk page](https://archive.stsci.edu/tess/bulk_downloads/bulk_downloads_ffi-tp-lc-dv.html), [download-script directory](https://archive.stsci.edu/missions/tess/download_scripts/sector/), [holdings table](https://outerspace.stsci.edu/spaces/TESS/pages/35094700/TESS+Holdings+Available+by+MAST+Service), [DRN page](https://archive.stsci.edu/tess/tess_drn.html) and [DRN directory](https://archive.stsci.edu/missions/tess/doc/tess_drn/). Retrieved the S106/S107 LC lists completely and FFI-script headers/initial content; parsed the holdings table's checked/unchecked HTML controls rather than treating every row as available. Raw HTTP results are `public_requests.json`, `public_more.json`, `extra_public.json` under that temporary directory. Read the [TICA data notes](https://archive.stsci.edu/hlsp/tica) through web search; the first HTTP chunk alone did not contain the body, so the quoted historical notice is from the web tool's returned primary-source text. A MAST CAOM release-date query timed out; I did not establish an exact first-ingestion time.
- **[L: text inventory]** Read current sources with `cat`, `nl -ba`, `rg` and Python. `/tmp/erratum_review/claims.py` extracted PDF text with `pdftotext -layout`; `claims2.py` searched the requested document trees; additional `rg` searches covered cached GitHub/Zenodo corpus copies and phrases such as `unreleased`, `not public`, `not available`, `not released`, and `before the test data`. The inventory below separates incorrect assertions from historical quotations and narrower QLP claims. Line numbers refer to the inspected version.
- **[F: fitted versus test sectors]** `/tmp/erratum_review/freeze_fixscan.py` parsed **138** `final_ephemeris*.json` files, including duplicate releases/caches; this is a file count, not 138 independent freezes. Fitted sectors came only from fitted-data fields (`sector_times`, `transit_times`, `full`), not prediction/coverage lists. Test sectors came from the SHA-linked CSV's `prediction` rows, or the older TIC 317134140 explicit prediction schema. Nine figure-directory copies lacking adjacent CSVs were byte-identical to copies with matching CSVs. Result: `freeze_scan_corrected.json`. Also read the individual registrations and logs, so “contains S106” in a prediction table was not mistaken for an S106 fit.
- **[G: generator tests]** Read all of `scripts/prereg_v2.py`, SHA-256 `dcb437ddc915cae9df39cf6d7243765926038ef079f93d1d96269cc2c8005830`. Copied it to `/tmp/erratum_review/prereg_v2_tmp.py` and `prereg_v2_tmp162.py`, redirected `OUT` and supporting `report.json` copies to temporary directories, disabled network-dependent IERS downloads and redirected caches to `/tmp`. Ran the temporary scripts with `--no-2min --freeze --version 99` for TIC 53825235 (also `--unreleased-sectors 108`) and TIC 162304222 (also `--clock`). **No project generator was run with `--freeze`.** Drivers/logs: `generator_tests.py`, `horizon2.py`, `generator_tests.txt`, `horizon_dryrun.log`, `horizon162.log`. Exact source AST loading blocks were also exercised with mock Lightkurve/FITS objects: no actual test-sector download or flux read occurred in those tests. `guard_results.json` records calls.
- **[C: evaluator]** Read all 60 lines of `scripts/prereg_test.py`, including the actual branches rather than its inaccurate docstring. Its SHA-256 is still `630815cc1400f0434dc9f30c8ce08cc42635ee5d1d429338c4010f6115043366`. This review rechecked the implementation and earlier synthetic-test records; it did not run it on real S106 photometry.
- **[P: chronology/public records]** Reopened raw JSON responses and extracted archive files in `/tmp/timing_rule_review/23462442*`, `23474138*`, `23477866*`; rehashed all three archived evaluators and reread the protocol's purpose/timing clauses. Those downloads came from [original protocol API](https://zenodo.org/api/records/23462442), [v1.2](https://zenodo.org/api/records/23474138), [v1.3](https://zenodo.org/api/records/23477866). Inspected local public Git history and refreshed the [GitHub head API](https://api.github.com/repos/fergmolina/tess-transit-candidates/commits?per_page=1): head remained `d995a1fff8ad24171cad4bd35dc07ebe04a66539`. Queried [preprint concept API](https://zenodo.org/api/records/23462433), which returned version record **23463582**, and downloaded its [PDF](https://zenodo.org/api/records/23463582/files/Molina2026_two_candidates_note.pdf/content); extracted its erroneous preregistration paragraph. Creation times are record metadata, not a cryptographic proof of when every byte first became public; Git commit dates alone are not push timestamps.
- **[H: hashes/preservation]** `/tmp/erratum_review/clarification_check.py` compared all **92** versioned CSV copies inventoried during the previous review with their saved full digests: no changes. Re-ran `/tmp/timing_rule_review/hash_final.py`: 31 local/public pairs match and all 31 inspected public CSVs match their first-addition Git versions; the three v1 primary CSV hashes match both JSON and Markdown. The special v4/v5 TIC 89247735 metadata/registration formats require separate handling rather than interpreting the generic script's missing-Markdown flag as a hash failure; I separately recalculated both CSV digests and matched their `sha256_csv` JSON fields (prefixes `4f6aba63` and `216e7a4c`). All 63 inputs recorded in the current review's `input_hashes.json` were unchanged at final comparison. Read the three amended v1 documents and confirmed dated retractions. For TIC 80387959 and 120444365, historical public originals remain exact byte prefixes; no independent pre-append original was available for withheld TIC 120517801.
- **[I: timing impact]** Recomputed gates directly from `results/vet_allsky/<TIC>/predicted_transits_2026_2027_v2.csv`, selecting S106 prediction rows and multiplying recorded `sigma_min` by three. Calculations are in `clarification_check.py`. The evaluator's actual aggregate depends on which windows qualify for coverage, not on an assumed selection made before the observations.
- **[B: revised clarification]** Direct comparison of current `results/CLARIFICATION_TIMING_RULE_2026-10-20.md`, `results/REVIEW_timing_rule.md`, all 37 affected v2 originals/addenda, the three v1 corrections and `logs/DECISIONS.md:325–349`. Original-rule counts were computed after stripping the appended timing note, avoiding counting the note's quotation as original wording.

## Findings and required fixes

| Issue | Evidence and finding | Exact action needed before publication |
|---|---|---|
| A1. Local time correct; download count unsupported | Erratum “899” versus **897 retained S106 FITS in `data/lc/`**; one additional S106 SPOC file for TIC 88407114 was created in `data/lk_cache/` on Oct 20, not Oct 17. The separate 1×1 cutout is also Oct 20. Earliest Oct-17 timestamp is 12:45:25 EDT = 16:45:25 UTC. [A] | Replace the count with “retained S106 SPOC light-curve files establish local access by 2026-10-17 16:45 UTC,” or document the original 899-download manifest. Do not add later files to an Oct-17 download count. |
| A2. Sector availability is not target-product availability | The full S106/S107 SPOC LC download lists do **not** contain TIC 120444365, 183374279, 70441745, 206620592, 122522485, 253931796 or 115692561. TIC 88407114 is on the S106 list. [A, exact 16-digit TIC matching in `lc106.txt`/`lc107.txt`] | Say SPOC LC products **for other targets** were public; the relevant independent route for these FFI targets is publicly available imagery. A missing QLP product is not proof that the observations were inaccessible. |
| A3. Affected scope incomplete | Erratum's four-row table omits five local S106 v2 freezes, including withdrawn 88407114, and S107 registrations for 160330868/24526743/88407114. See chronology/inventory. [L,F,A] | Add all affected local freezes, identify which were public, and include a separate S107 section or companion erratum. Correct current indexes/preprint/protocol purpose as listed below. |
| A4. Non-examination is not proved by absence from final fits | No pre-freeze test-sector file/fit was found for the six requested objects; an S106 cutout **does exist for 206620592**, created after its freeze. Absence from disk/fitted rows cannot exclude deleted, remote, exploratory or human viewing. [A,F] | Use an explicitly attributed author attestation. Disclose the cutout and distinguish download, flux inspection and fit inclusion. Replace unconditional “remain blind”/“genuine out-of-sample” with conditional interpretation tied to that attestation and an unchanged analysis. |
| A5. Withdrawal incomplete in active records | 88407114 v2 includes S106 SPOC in `sector_times`; its `PREREGISTRATION_v2.md` has no withdrawal notice and `results/allsky_round3_outcomes.csv` still lists its test. Public Git history contains no path for its freeze. [F,L,P] | Name **TIC 88407114 v2, frozen 2026-10-20 00:44:14 UTC**, and S106 as invalid. Append a withdrawal to that registration and flag the active index; preserve CSV bytes. State “not found in the inspected public releases,” or provide a release-manifest audit for a universal never-published claim. |
| A6. Claimed process fix is not implemented | `prereg_v2.py:52–59` admits test-sector QLP; `:61–68` calls `download_all`/`lk.read` and accesses flux before skipping SPOC sectors; no MAST availability query populates status. Synthetic spies reproduce each route. [G] | Either implement and test pre-download/pre-flux guards for **all** products and availability logging, or replace “From 2026-10-20 … will” with an explicit pending fix and suspend new freezes until it passes. The current SPOC fit exclusion alone is narrower than the promise. |
| A7. Misleading log assertion | Item 67 says “No other frozen fit contains S106+ data.” TIC 317134140's `final_ephemeris_predictions.json` contains S107 training data; its declared tests are S108–S110. Only 88407114 overlaps its own declared test sectors in this audit. [F] | Append: “Only TIC 88407114 overlaps its declared test sectors; TIC 317134140 intentionally uses S107 training data.” Do not rewrite the historical entry. |
| A8. Exclusions mostly sound, year too narrow | 80387959's S111 starts Nov 26; 89247735's v1 is a different, ground-based test, but its first prediction row is epoch 146 on **2026-10-29**, not only 2027. [L: original 892 CSV/registration; official sector page below] | Change “ground-based (2027)” to “ground-based predictions for 2026–2027”; retain distinction from the post hoc S93 recovery. |
| B1. Scope/pre-evaluation wording still overbroad | “For every object” conflicts with the explicit v1/ground exceptions. “Before any test photometry is evaluated” overlooks withdrawn 88407114's S106 fit. [B,F] | Use the exact scoped replacement in the wording section; explicitly exclude withdrawn tests and cross-link the availability erratum. |
| B2. Accurate aggregation in clarification, inaccurate template | Clarification says inverse depth variance; template says “depth-weighted mean.” Actual weights are `1/depth_err_ppm**2`, and sigma is an arithmetic mean over coverage-qualified predictions. [B,C:44–45,G:136] | Replace template phrase with the explicit equation/wording below. This is an algorithmic distinction, not a stylistic preference. |
| C1. Horizon extension works but advertised endpoint is wrong | Both temporary historical-data runs generate future predictions. However `range(1,200000)` still stops at JD **2461900**, i.e. **2028-05-08 12:00 TDB**, while `--ground` help says through 2027-12. [G; `astropy.time.Time(2461900,format='jd',scale='tdb')`] | Use an explicit exclusive 2028-01-01 endpoint for “through December 2027,” or change documentation/file scope to the actual endpoint. Compute the epoch limit from the date rather than an arbitrary cap. |
| C2. New corrected freezes would contain a false reason | For **every** `--version > 2`, template line 125 inserts the claim that v2 double-counted S22/S45. Both temporary v99 outputs reproduce it for stars whose issue is the horizon. [G] | Make the supersession reason object/version-specific and require an explicit reason. Do not issue the proposed new v3 horizon corrections with the current generic sentence. |
| C3. New status removes false public-absence claim but invents an attestation | `:111` assigns “test data not examined by us … check public availability” from a manual sector list; it neither checks availability nor verifies non-examination. [G] | Separate `observed`, product-specific `availability_checked_at/status`, and explicit author `not_examined_before_freeze` attestation. Unknown availability must say unknown. Rename/deprecate `--unreleased-sectors` so it cannot imply a release fact. |
| C4. Historical empty selections still exist | Original v2 CSVs for 162304222, 408110117 and 53825235 remain unchanged; the first/third horizon problem is demonstrated fixed only in temporary new outputs. Item 68 correctly says new versions are needed, but overattributes all three to the 399-epoch cap. [H,G; original CSV statuses] | Publish separate dated replacements with accurate reasons after holdout guards work. 408110117 also needs its already-observed test-sector eligibility addressed; extending a loop alone does not change past rows to predictions. Do not label an empty selection a test result. |

## Availability chronology and what it establishes

### Archive evidence

| Source/product | Verified date/status | Interpretation and limit |
|---|---|---|
| [S106 SPOC LC download script](https://archive.stsci.edu/missions/tess/download_scripts/sector/tesscurl_sector_106_lc.sh) | HTTP 200; `Last-Modified: 2026-09-10 18:08:16 GMT`. [A] | Public list exists and predates the freezes by metadata. **Not** a certified first product-release timestamp. |
| [S107 SPOC LC download script](https://archive.stsci.edu/missions/tess/download_scripts/sector/tesscurl_sector_107_lc.sh) | HTTP 200; `Last-Modified: 2026-10-02 00:27:40 GMT`. [A] | Same limit; local files independently corroborate access before these freezes. |
| [S106 SPOC FFI script](https://archive.stsci.edu/missions/tess/download_scripts/sector/tesscurl_sector_106_ffic.sh) | HTTP 200; `Last-Modified: 2026-08-13 14:46:32 GMT`. [A] | Evidence for an earlier available FFI listing, not an exact TESScut deployment date. |
| [TICA S106 data notice](https://archive.stsci.edu/hlsp/tica) | Says missing S106 orbit-2a camera-1/2/3 cadences became available **2026-08-14**; identifies TICA cutouts as accessible through TESSCut. [A, web primary-source text] | Strong historical evidence that S106 image products were available well before October. TICA and SPOC are different calibrations; this does not date the first SPOC TESScut availability. |
| [S107 FFI script](https://archive.stsci.edu/missions/tess/download_scripts/sector/tesscurl_sector_107_ffic.sh) | HTTP 200; `Last-Modified: 2026-09-23 12:54:56 GMT`. [A] | Broad “S107 data not public” is untenable alongside the local S107 SPOC downloads. |
| [S108 FFI script](https://archive.stsci.edu/missions/tess/download_scripts/sector/tesscurl_sector_108_ffic.sh) | HTTP 200; `Last-Modified: 2026-10-19 16:14:50 GMT`. [A] | Current availability corroborated; this modification date alone does **not** prove availability before TIC 317134140's Oct-17 freeze. |
| [S109 FFI script](https://archive.stsci.edu/missions/tess/download_scripts/sector/tesscurl_sector_109_ffic.sh) | HTTP 200; `Last-Modified: 2026-10-15 21:06:40 GMT`. [A] | At least an available listing during this review, with earlier metadata. Do not infer complete-sector coverage or LC availability. |
| [MAST holdings table](https://outerspace.stsci.edu/spaces/TESS/pages/35094700/TESS+Holdings+Available+by+MAST+Service) | On Oct 20: S106/107 LC and FFI services checked; S108 FFI/TESSCut checked but LC unchecked; S109 FFI portal/bulk checked but TESSCut/LC unchecked. [A, parsed HTML checkbox classes] | Release is product/service-specific. It is wrong to extrapolate the absence of QLP or SPOC LCs to absence of images. Current table does not reconstruct every freeze-time service state. |
| [DRN listings](https://archive.stsci.edu/tess/tess_drn.html) | No S106 DRN located in the inspected listing, which reached S104/DRN142. [A] | Do not confuse **DRN106** with **Sector106**. Exact S106 SPOC first-release date remains unverified. |

### Local timestamps and freezes

`ls` printed **EDT**, not UTC. The earliest retained S106 file is `data/lc/tess2026192185000-s0106-0000000616407043-0308-s_lc.fits`: mtime **2026-10-17 16:45:25.970231 UTC**, birthtime **16:45:25.653878 UTC**. Its header identifies S106 and TIC 616407043. There are 897 S106 files in `data/lc/`; including the later TIC 88407114 cache file makes 898 project-data S106 FITS. The 1×1 `/tmp` cutout is a third category, not an Oct-17 SPOC LC. Filesystem times can be preserved or altered and are not server release certificates; agreement of birthtime, mtime and public archive evidence makes the quoted approximately 16:45 UTC credible. I cannot rule out two historically downloaded files subsequently removed, so **899 is unsubstantiated, not proved historically impossible**. [A]

S107 files also predate all these freezes: earliest retained `data/lc/tess2026221103959-s0107-0000000097468416-0309-s_lc.fits` has mtime **2026-10-17 16:45:25.943936 UTC**. There are 1637 S107 FITS in `data/lc/`, plus two cached TIC 317134140 copies. [A]

The following timestamps are the actual JSON `frozen` values. “Public” means found in the inspected public release/archive, not merely locally timestamped. Training sectors are independently parsed fitted-data fields. [F,P]

| Object/version | Frozen UTC | Fitted sectors | Disposition |
|---|---|---|---|
| 120444365 v1 | 2026-10-18 20:26:00 | 69, 96, 103, 105 | Public; S106 wording affected |
| 120444365 v2 | 2026-10-18 22:34:49 | 2, 29, 69, 96, 103, 105 | Public; S106 wording affected |
| 183374279 v2 | 2026-10-19 11:44:14 | 2, 29, 69, 96, 103, 105 | Public; S106 wording affected |
| 70441745 v2 | 2026-10-19 12:51:12 | 68 | Public; S106 wording affected |
| 122522485 v2 | 2026-10-20 00:33:06 | 3, 4, 30, 97, 105 | Local; omitted from erratum table |
| 206620592 v2 | 2026-10-20 00:33:10 | 28, 68, 96 | Local; omitted; later 1×1 cutout below |
| 253931796 v2 | 2026-10-20 00:33:12 | 28, 68 | Local; omitted |
| 115692561 v2 | 2026-10-20 00:44:10 | 2, 29, 69, 96 | Local; omitted |
| 88407114 v2 | 2026-10-20 00:44:14 | 4, 31, 97, 105, **106** | Local; **S106 cannot be an out-of-sample test** |

The corresponding analogous S107 records are TIC **160330868** (00:43:17 UTC), **24526743** (00:43:31) and **88407114** (00:44:14), all on Oct 20. Their original CSV status fields explicitly say “data not public at freeze.” None of these S107 sectors appears as a fitted sector in those records. This does not establish non-examination. [F,L: individual `final_ephemeris_v2.json` and CSVs]

### Non-examination and the small cutout

The file is:

`/tmp/claude-501/-Users-fernando-Desktop-NASA/c3c861f6-d690-49d9-96f5-051efe8a7e34/scratchpad/s106/tess-s0106-1-2_341.971994_-33.857307_1x1_astrocut.fits`.

Its header coordinates match TIC **206620592** in `results/vet_allsky/206620592/report.json` (RA 341.971994096°, Dec −33.8573068371°). It is an S106 1×1-pixel cutout; mtime **2026-10-20 01:21:13.475440 UTC**, birthtime **01:21:13.474580 UTC**, approximately **48 min 3.5 s after** that object's frozen timestamp. The internal review `results/referee_round3/REFEREE_REPORT_round3.md:10` discloses the download and says flux was not examined. I verified identity/time from headers/stat, not from that assurance, and did not inspect its flux myself. [A,L]

Therefore the cutout does **not** contradict the stated pre-freeze non-examination chronology, but an assertion that no such data exist anywhere in a cache is false for 206620592. Downloading pixels and evaluating their flux are different actions; the latter cannot be reconstructed conclusively from the file's presence. The erratum should disclose the event without presenting the internal review's statement as independently proved. [A; reviewer inference]

I searched project `data/`, known Lightkurve caches, `/tmp` paths, and standard Astropy cache contents. The `.cache/astropy` scan found no FITS-magic files among 1818 files; `.lightkurve` FITS filenames were all earlier than S106. For the six requested objects, no other S106-or-later photometry file was found. Logs contain **predictions** for S106, which are not evidence of using S106 flux. No S106-or-later fitted row occurs in their frozen ephemerides. These are bounded negative checks, not a forensic proof against deleted files, other machines, browser viewing or earlier exploratory analysis. [A,F; direct filename/header scans and log searches]

## Complete correction inventory within the inspected trees

“Correct” here means correct current explanatory prose or append/link an erratum. **Do not silently modify frozen CSV status bytes, original Markdown text, old PDFs, historical logs, cached third-party material or archived manifests.** A manifest mapping path + original hash + corrected interpretation is preferable for immutable copies. The inventory is complete for the matched assertions in the named local trees and inspected public artifacts; inaccessible/uninspected remote versions are explicitly outside that claim. [L,H]

### Current prose, tables, protocol and public-facing copies

| File/place | Verified location/claim | Required treatment |
|---|---|---|
| `STATUS.md` | Lines 11,13, S106 “data not public” for 120444365/183374279 | Correct current status and link erratum |
| `public_release/README.md`; `dataset_v1/README.md` | Line 37 / line 16, 120444365 light curves not public | Correct current README; link correction beside historical dataset |
| `results/REPORT.md`; `public_release/REPORT.md` | Lines644 /638, S106 not public | Correct current narrative |
| `dataset_v1/REPORT.md` | Lines118, 174, S108 not public | Historical availability qualifier; see S108 limit above |
| `results/REPORT.md`; `public_release/REPORT.md` | Lines118, 174, S108 not public | Update current product-specific status; do not claim exact Oct-17 release history proved |
| `results/allsky_classA_outcomes.csv`; `public_release/tables/allsky_classA_outcomes.csv`; `dataset_v1/allsky_classA_outcomes.csv` | TIC 120444365 row, “106 (unreleased)” | Correct current index/new version, preserve archived original |
| `results/allsky_classA_round2_outcomes.csv`; `public_release/tables/allsky_classA_round2_outcomes.csv` | TIC 183374279 row, S106 “data unreleased” | Same |
| `results/allsky_round3_outcomes.csv` | TIC 88407114 still listed with S106 test | Add explicit withdrawal in active index; this is consequential even without an availability phrase |
| `note_allsky/note.tex`; `note_allsky/note.pdf` | TEX45–47; PDF p.1 preregistration paragraph | Correct both blanket before-data claim and S106 unavailability in a new version |
| `dataset_v1/documents/note.tex`; `dataset_v1/documents/note.pdf`; `zenodo_upload/Molina2026_two_candidates_note.pdf` | Same paragraph | Link erratum / rebuild only new released version |
| [Zenodo two-candidate note 23462433](https://doi.org/10.5281/zenodo.23462433), returned version [23463582](https://zenodo.org/records/23463582) | Downloaded PDF p.1 has both claims | Public version/erratum link required; local Markdown alone does not correct this publication |
| `prereg_protocol/PREREG_PROTOCOL.tex`; `prereg_protocol/PREREG_PROTOCOL.pdf` | Purpose, TEX11/PDF p.1: all tests fixed before data exist/public | Qualify observed, publicly available but reportedly unexamined tests |
| `prereg_bundle/PREREG_PROTOCOL.tex`; `prereg_bundle/PREREG_PROTOCOL.pdf`; `dataset_v1/documents/PREREG_PROTOCOL.tex`; `dataset_v1/documents/PREREG_PROTOCOL.pdf`; `zenodo_upload/PREREG_PROTOCOL.pdf` | Same purpose sentence | Link correction to old bundles; fix new edition |
| [Protocol23462442](https://zenodo.org/records/23462442), [23474138](https://zenodo.org/records/23474138), [23477866](https://zenodo.org/records/23477866) | Reopened archived TEX11/PDF purpose; bundled registrations | Publish linked correction/new version while retaining old records |
| `results/round2_dossiers/DOSSIERS.md` | Lines24–26 repeat frozen S106 status; opening paragraph says FFIs not checked | Annotate quoted table and update current availability caveat |
| `results/external_review_allsky/ephemeris_check.json`; `dataset_v1/external_review_allsky/ephemeris_check.json` | Repeated copied S106 status at lines 548–593 | Historical numerical audit: preserve and cross-reference correction |
| `zenodo_upload/EMAIL_tfop_application_draft.md` | Lines33–34: predictions archived before test data exist | Revise draft before use; no email was sent in this review |
| `logs/DECISIONS.md`; `public_release/DECISIONS.md` | Older entries at lines 102, 112–113, 249; local items65–68 | Append cross-reference; correct item67's overbroad “no other S106+ fit” and distinguish historical 40 notes from 37 correctly affected originals |
| `results/ERRATUM_S106_DATA_AVAILABILITY_2026-10-20.md` | Scope/process/attestation problems above | Replace with corrected version before publication |

The protocol's **table entries** for TIC 120444365/183374279, the later 183374279 registration addendum, its public README paragraph and the opening dossier prose already limit the missing-product claim to **QLP**. They must be supplemented with the image-availability distinction; they should not be “corrected” into a claim that target-specific SPOC 2-minute LCs existed. The previous timing review itself explicitly restricted its successful 404 checks to QLP and said it did not establish general absence of SPOC/TESScut data. [L: protocol27–28, dossier5/20, registration25, `results/REVIEW_timing_rule.md:63–71`; A]

### Every matched registration and prediction CSV

Each row below is an actual file opened by the scan. S106 entries need the S106 erratum; S107 entries need the analogous correction; mixed 88407114 also needs the S106 withdrawal. A Markdown timing addendum is **not** an availability correction. Frozen CSVs must retain their bytes and receive an external mapping/link. [L: direct per-file line scan and CSV status fields]

| File | Affected sector(s) | Treatment |
|---|---|---|
| `dataset_v1/TIC120444365/PREREGISTRATION.md` | 106 | Append/link availability erratum |
| `dataset_v1/TIC120444365/PREREGISTRATION_v2.md` | 106 | Append/link availability erratum |
| `dataset_v1/TIC120444365/predicted_transits_2026_2027.csv` | 106 | Preserve CSV; map corrected status |
| `dataset_v1/TIC120444365/predicted_transits_2026_2027_v2.csv` | 106 | Preserve CSV; map corrected status |
| `prereg_bundle/preregistration/TIC120444365/PREREGISTRATION.md` | 106 | Append/link availability erratum |
| `prereg_bundle/preregistration/TIC120444365/PREREGISTRATION_v2.md` | 106 | Append/link availability erratum |
| `prereg_bundle/preregistration/TIC120444365/predicted_transits_2026_2027.csv` | 106 | Preserve CSV; map corrected status |
| `prereg_bundle/preregistration/TIC120444365/predicted_transits_2026_2027_utcfix.csv` | 106 | Preserve CSV; map corrected status |
| `prereg_bundle/preregistration/TIC120444365/predicted_transits_2026_2027_v2.csv` | 106 | Preserve CSV; map corrected status |
| `prereg_bundle/preregistration/TIC120444365/predicted_transits_2026_2027_v2_utcfix.csv` | 106 | Preserve CSV; map corrected status |
| `prereg_bundle/preregistration/TIC183374279/PREREGISTRATION_v2.md` | 106 | Append/link availability erratum |
| `prereg_bundle/preregistration/TIC183374279/predicted_transits_2026_2027_v2.csv` | 106 | Preserve CSV; map corrected status |
| `prereg_bundle/preregistration/TIC70441745/PREREGISTRATION_v2.md` | 106 | Append/link availability erratum |
| `prereg_bundle/preregistration/TIC70441745/predicted_transits_2026_2027_v2.csv` | 106 | Preserve CSV; map corrected status |
| `public_release/preregistration/TIC120444365/PREREGISTRATION.md` | 106 | Append/link availability erratum |
| `public_release/preregistration/TIC120444365/PREREGISTRATION_v2.md` | 106 | Append/link availability erratum |
| `public_release/preregistration/TIC120444365/predicted_transits_2026_2027.csv` | 106 | Preserve CSV; map corrected status |
| `public_release/preregistration/TIC120444365/predicted_transits_2026_2027_utcfix.csv` | 106 | Preserve CSV; map corrected status |
| `public_release/preregistration/TIC120444365/predicted_transits_2026_2027_v2.csv` | 106 | Preserve CSV; map corrected status |
| `public_release/preregistration/TIC120444365/predicted_transits_2026_2027_v2_utcfix.csv` | 106 | Preserve CSV; map corrected status |
| `public_release/preregistration/TIC183374279/PREREGISTRATION_v2.md` | 106 | Append/link availability erratum |
| `public_release/preregistration/TIC183374279/predicted_transits_2026_2027_v2.csv` | 106 | Preserve CSV; map corrected status |
| `public_release/preregistration/TIC70441745/PREREGISTRATION_v2.md` | 106 | Append/link availability erratum |
| `public_release/preregistration/TIC70441745/predicted_transits_2026_2027_v2.csv` | 106 | Preserve CSV; map corrected status |
| `results/vet_allsky/115692561/PREREGISTRATION_v2.md` | 106 | Append/link availability erratum |
| `results/vet_allsky/115692561/predicted_transits_2026_2027_v2.csv` | 106 | Preserve CSV; map corrected status |
| `results/vet_allsky/120444365/PREREGISTRATION.md` | 106 | Append/link availability erratum |
| `results/vet_allsky/120444365/PREREGISTRATION_v2.md` | 106 | Append/link availability erratum |
| `results/vet_allsky/120444365/predicted_transits_2026_2027.csv` | 106 | Preserve CSV; map corrected status |
| `results/vet_allsky/120444365/predicted_transits_2026_2027_utcfix.csv` | 106 | Preserve CSV; map corrected status |
| `results/vet_allsky/120444365/predicted_transits_2026_2027_v2.csv` | 106 | Preserve CSV; map corrected status |
| `results/vet_allsky/120444365/predicted_transits_2026_2027_v2_utcfix.csv` | 106 | Preserve CSV; map corrected status |
| `results/vet_allsky/122522485/PREREGISTRATION_v2.md` | 106 | Append/link availability erratum |
| `results/vet_allsky/122522485/predicted_transits_2026_2027_v2.csv` | 106 | Preserve CSV; map corrected status |
| `results/vet_allsky/160330868/PREREGISTRATION_v2.md` | 107 | Append/link availability erratum |
| `results/vet_allsky/160330868/predicted_transits_2026_2027_v2.csv` | 107 | Preserve CSV; map corrected status |
| `results/vet_allsky/183374279/PREREGISTRATION_v2.md` | 106 | Append/link availability erratum |
| `results/vet_allsky/183374279/predicted_transits_2026_2027_v2.csv` | 106 | Preserve CSV; map corrected status |
| `results/vet_allsky/206620592/PREREGISTRATION_v2.md` | 106 | Append/link availability erratum |
| `results/vet_allsky/206620592/predicted_transits_2026_2027_v2.csv` | 106 | Preserve CSV; map corrected status |
| `results/vet_allsky/24526743/PREREGISTRATION_v2.md` | 107 | Append/link availability erratum |
| `results/vet_allsky/24526743/predicted_transits_2026_2027_v2.csv` | 107 | Preserve CSV; map corrected status |
| `results/vet_allsky/253931796/PREREGISTRATION_v2.md` | 106 | Append/link availability erratum |
| `results/vet_allsky/253931796/predicted_transits_2026_2027_v2.csv` | 106 | Preserve CSV; map corrected status |
| `results/vet_allsky/70441745/PREREGISTRATION_v2.md` | 106 | Append/link availability erratum |
| `results/vet_allsky/70441745/predicted_transits_2026_2027_v2.csv` | 106 | Preserve CSV; map corrected status |
| `results/vet_allsky/88407114/PREREGISTRATION_v2.md` | 106, 107 | Append/link availability erratum; mark S106 withdrawn |
| `results/vet_allsky/88407114/predicted_transits_2026_2027_v2.csv` | 106, 107 | Preserve CSV; map corrected status; mark S106 withdrawn |

### Local ZIP artifacts requiring a linked correction

I opened these ZIPs with Python `zipfile.ZipFile`, searched decoded text members for the same assertions, and recorded the following exact members. This adds archive-level coverage to the unpacked-path inventory; the old ZIPs should be preserved, with an erratum link/new version rather than an in-place rewrite. PDF counterparts inside the protocol bundles carry the same purpose sentence verified in their extracted copies. [L; `/tmp/erratum_review/archive_inventory.json`]

- `zenodo_upload/preregistration_bundle_v1.1.zip`: `preregistration/TIC120444365/PREREGISTRATION_v2.md`, `preregistration/TIC120444365/PREREGISTRATION.md`, `preregistration/TIC120444365/predicted_transits_2026_2027.csv`, `preregistration/TIC120444365/predicted_transits_2026_2027_utcfix.csv`, `preregistration/TIC120444365/predicted_transits_2026_2027_v2.csv`, `preregistration/TIC120444365/predicted_transits_2026_2027_v2_utcfix.csv`, `PREREG_PROTOCOL.tex`.
- `zenodo_upload/preregistration_bundle_v1.2.zip`: `preregistration/TIC120444365/PREREGISTRATION_v2.md`, `preregistration/TIC120444365/PREREGISTRATION.md`, `preregistration/TIC120444365/predicted_transits_2026_2027.csv`, `preregistration/TIC120444365/predicted_transits_2026_2027_utcfix.csv`, `preregistration/TIC120444365/predicted_transits_2026_2027_v2.csv`, `preregistration/TIC120444365/predicted_transits_2026_2027_v2_utcfix.csv`, `preregistration/TIC183374279/PREREGISTRATION_v2.md`, `preregistration/TIC183374279/predicted_transits_2026_2027_v2.csv`, `PREREG_PROTOCOL.tex`.
- `zenodo_upload/preregistration_bundle_v1.3.zip`: `preregistration/TIC70441745/PREREGISTRATION_v2.md`, `preregistration/TIC70441745/predicted_transits_2026_2027_v2.csv`, `preregistration/TIC120444365/PREREGISTRATION_v2.md`, `preregistration/TIC120444365/PREREGISTRATION.md`, `preregistration/TIC120444365/predicted_transits_2026_2027.csv`, `preregistration/TIC120444365/predicted_transits_2026_2027_utcfix.csv`, `preregistration/TIC120444365/predicted_transits_2026_2027_v2.csv`, `preregistration/TIC120444365/predicted_transits_2026_2027_v2_utcfix.csv`, `preregistration/TIC183374279/PREREGISTRATION_v2.md`, `preregistration/TIC183374279/predicted_transits_2026_2027_v2.csv`, `PREREG_PROTOCOL.tex`.
- `zenodo_upload/supporting_data_and_code_v1.zip`: `TIC120444365/PREREGISTRATION_v2.md`, `TIC120444365/PREREGISTRATION.md`, `TIC120444365/predicted_transits_2026_2027.csv`, `TIC120444365/predicted_transits_2026_2027_v2.csv`, `external_review_allsky/ephemeris_check.json`, `allsky_classA_outcomes.csv`, `documents/note.tex`, `documents/PREREG_PROTOCOL.tex`, `prior_search/query_log_all.csv`.

### Historical logs and cached public copies

These also contain the assertion, but are evidence of what was said. Preserve them and list them in the correction's provenance manifest; do not retroactively clean them. The following logs were directly matched in the scan. [L]

- `logs/prereg_120444365.log`
- `logs/prereg_r3_115692561.log`
- `logs/prereg_r3_122522485.log`
- `logs/prereg_r3_160330868.log`
- `logs/prereg_r3_206620592.log`
- `logs/prereg_r3_24526743.log`
- `logs/prereg_r3_253931796.log`
- `logs/prereg_r3_88407114.log`
- `logs/prereg_r3_dry_122522485.log`
- `logs/prereg_r3_dry_206620592.log`
- `logs/prereg_r3_dry_253931796.log`
- `logs/prereg_v2_120444365.log`
- `logs/prereg_v2_183374279.log`
- `logs/prereg_v2_70441745.log`

Cached source/archive copies found by the additional corpus search (retain as historical evidence; annotate the index, not the downloaded original): [L]

- `results/prior_search/query_log_all.csv`
- `results/prior_search_round2/data/zenodo_new/23462438/supporting_data_and_code_v1.zip.txt`
- `results/prior_search_round2/data/zenodo_new/23474130/tess-transit-candidates-v1.6.zip.txt`
- `results/prior_search_round2/data/zenodo_new/23474138/PREREG_PROTOCOL.pdf.txt`
- `results/prior_search_round2/data/zenodo_new/23474138/preregistration_bundle_v1.2.zip.txt`
- `results/prior_search/data/zenodo_deep/23445705/tess-transit-candidates-v1.2.zip.txt`
- `results/prior_search_round2/data/zenodo_new/23463582/Molina2026_two_candidates_note.pdf.txt`
- `results/prior_search/data/zenodo_deep/23460915/tess-transit-candidates-v1.3.zip.txt`
- `results/prior_search/data/github_sweep/fergmolina__tess-transit-candidates/DECISIONS.md`
- `results/prior_search/data/github_sweep/fergmolina__tess-transit-candidates/preregistration/TIC120444365/predicted_transits_2026_2027_v2.csv`
- `results/prior_search/data/github_sweep/fergmolina__tess-transit-candidates/preregistration/TIC120444365/predicted_transits_2026_2027.csv`
- `results/prior_search/data/github_sweep/fergmolina__tess-transit-candidates/preregistration/TIC120444365/PREREGISTRATION.md`
- `results/prior_search/data/github_sweep/fergmolina__tess-transit-candidates/preregistration/TIC120444365/PREREGISTRATION_v2.md`
- `results/prior_search_round2/data/github_sweep/fergmolina__tess-transit-candidates/DECISIONS.md`
- `results/prior_search_round2/data/github_sweep/fergmolina__tess-transit-candidates/prior_search/query_log_all.csv`
- `results/prior_search_round2/data/github_sweep/fergmolina__tess-transit-candidates/preregistration/TIC183374279/predicted_transits_2026_2027_v2.csv`
- `results/prior_search_round2/data/github_sweep/fergmolina__tess-transit-candidates/preregistration/TIC183374279/PREREGISTRATION_v2.md`
- `results/prior_search_round2/data/github_sweep/fergmolina__tess-transit-candidates/preregistration/TIC120444365/predicted_transits_2026_2027_v2_utcfix.csv`
- `results/prior_search_round2/data/github_sweep/fergmolina__tess-transit-candidates/preregistration/TIC120444365/predicted_transits_2026_2027_v2.csv`
- `results/prior_search_round2/data/github_sweep/fergmolina__tess-transit-candidates/preregistration/TIC120444365/predicted_transits_2026_2027_utcfix.csv`
- `results/prior_search_round2/data/github_sweep/fergmolina__tess-transit-candidates/preregistration/TIC120444365/predicted_transits_2026_2027.csv`
- `results/prior_search_round2/data/github_sweep/fergmolina__tess-transit-candidates/preregistration/TIC120444365/PREREGISTRATION.md`
- `results/prior_search_round2/data/github_sweep/fergmolina__tess-transit-candidates/preregistration/TIC120444365/PREREGISTRATION_v2.md`
- `results/prior_search_round2/data/github_sweep/fergmolina__tess-transit-candidates/tables/allsky_classA_round2_outcomes.csv`

Additional cached copies found on the broader availability-phrase pass (all retained as historical snapshots): [L, `rg` and direct file reads]

- `results/prior_search/data/github_sweep/fergmolina__tess-transit-candidates/README.md` — same S106 README/status or S108 report wording as the corresponding public/staged copy.
- `results/prior_search/data/github_sweep/fergmolina__tess-transit-candidates/REPORT.md` — same S106 README/status or S108 report wording as the corresponding public/staged copy.
- `results/prior_search/data/github_sweep/fergmolina__tess-transit-candidates/tables/allsky_classA_outcomes.csv` — same S106 README/status or S108 report wording as the corresponding public/staged copy.
- `results/prior_search/data/github_sweep/fergmolina__tess-transit-candidates/external_review_allsky/REVIEW.md` — historical review or recommendation; preserve, with a contextual correction link rather than a rewritten assertion.
- `results/prior_search/data/github_sweep/fergmolina__tess-transit-candidates/research/RESEARCH.md` — historical review or recommendation; preserve, with a contextual correction link rather than a rewritten assertion.
- `results/prior_search_round2/data/github_sweep/fergmolina__tess-transit-candidates/README.md` — same S106 README/status or S108 report wording as the corresponding public/staged copy.
- `results/prior_search_round2/data/github_sweep/fergmolina__tess-transit-candidates/REPORT.md` — same S106 README/status or S108 report wording as the corresponding public/staged copy.
- `results/prior_search_round2/data/github_sweep/fergmolina__tess-transit-candidates/tables/allsky_classA_outcomes.csv` — same S106 README/status or S108 report wording as the corresponding public/staged copy.
- `results/prior_search_round2/data/github_sweep/fergmolina__tess-transit-candidates/external_review_allsky/REVIEW.md` — historical review or recommendation; preserve, with a contextual correction link rather than a rewritten assertion.
- `results/prior_search_round2/data/github_sweep/fergmolina__tess-transit-candidates/research/RESEARCH.md` — historical review or recommendation; preserve, with a contextual correction link rather than a rewritten assertion.

Cached `prior_search/VERDICTS.md` and `prior_search/PRIOR_SEARCH.md` also matched a broad phrase search, but their matches concern non-refereed publication status or QLP TCE lists, not S106 light-curve availability; no S106 erratum is required for those passages. [L, contextual `rg -n` inspection]

The following matches are **not new operative S106 false claims** and should not be rewritten as though they were: `results/REVIEW_timing_rule.md`; `results/referee_89247735/REVIEW_S106_test_procedure.md`; `results/referee_round2/REFEREE_REPORT.md` and its public copy; `results/referee_round3/REFEREE_REPORT_round3.md`; `results/external_review_allsky/REVIEW.md` and its public/dataset copies; `results/PROMPT_timing_rule_review.txt`, `results/PROMPT_erratum_review.txt`, and `results/referee_89247735/PROMPT_S106_test_review.txt`. They quote or investigate the old assertions. Add a link where the earlier audit conclusion is superseded; preserve reviewer text. `results/research/RESEARCH.md:199` and its public/cached copies recommend preregistering before data exist, rather than assert that S106 complied. [L, contextual inspection]

**Checked exclusions:** `paper/rnaas/note.tex` concerns TIC89247735; its prospective ground-based test does not depend on the S106 availability claim or the disputed TESS-v2 gate. Current `paper/main.tex` likewise has no S106 holdout claim. Older TIC89247735 PDF exports in `zenodo_upload/` mention future predictions, not S106 test data for the all-sky targets; they are not S106-erratum targets. `ddt_80387959/proposal.tex` has no S106 unavailability assertion. However its lines16/32 say FFI light curves arrive months later: specify **QLP-produced light curves**, since promptly available FFIs permit a separate extraction. The official [Sector111 page](https://tess.mit.edu/observations/sector-111/) confirms observations begin **2026-11-26**; the 80387959 exclusion is appropriate. [L,A; public sector page]

## Recheck of every prior timing-review fix

| Prior finding | Status | Verification and remaining action |
|---|---|---|
| Protocol claimed to precede all object files | **Fixed** | Revised chronology admits 80387959/120444365 v2 precede protocol; protocol API creation **2026-10-19 01:36:22.688677 UTC**, versus early public commit `24cd0de`/archive23460915. Archived evaluator hashes match. Do not interpret “earlier-archived” as earlier than those object files. [B,P] |
| Impact allegedly only σ>10 min | **Fixed** | Revised text correctly says σ≠10 min. Independent table below reproduces values. [B,I] |
| 40 affected originals versus37; three v1 notes wrong | **Fixed locally** | Count is37 originals. 80387959, 120444365, 120517801 v1 now explicitly withdraw the misapplied timing note while retaining the original60-min rule. Original public prefixes for first two preserved. [B,H] |
| Local versus public completion | **Pending release**, not falsely claimed complete | Twenty affected public-release v2 originals still lack the local timing addendum. Public head is unchanged. Publish the corrected note and per-record discoverable links/new manifests; do not say the public set is already corrected. [P,B] |
| “Preserved bytes” ambiguity | **Fixed in clarification** | Now distinguishes unchanged CSV bytes/digests from amended Markdown hashes. All92 prior CSV digests unchanged. Universal historical byte preservation for local-only originals cannot be independently certified. [B,H] |
| Evaluator differs from protocol | **Disclosure substantially fixed; executable unchanged** | Duration absent; EXCLUDED not separately full-coverage; mean offsets; actual branch order and AMBIGUOUS now acknowledged. Promise of a separately versioned conformance procedure is appropriate but not yet delivered. [B,C] |
| Scope cannot cover every object | **Partial** | Explicit v1, 61310956-v3 and 89247735-v1 exceptions are correct. “For every object” remains in Resolution; exclude withdrawn 88407114 and scope non-examination claims. [B,F] |
| Three empty eligible prediction sets | **Partial** | Two successful temporary horizon tests; original invalid selections unchanged, no new corrected freezes produced here. 408110117 also needs past-sector eligibility correction. [G,H] |
| Template grammar/aggregation/precedence | **Partial** | “at >=2 covered predicted transit windows” fixes grammar; linked caveats improve honesty. “Depth-weighted mean” still wrong, exact sigma aggregation left indirect, and generic v>2 reason introduces a new false claim. [G,C] |

The six rows actually printed in the revised clarification are acceptable rounded summaries. For precision, distinguish per-event gates from the executable's coverage-dependent aggregate. The following recomputation uses the original rounded frozen CSV sigmas; the last column assumes **all** listed S106 rows qualify, which may not occur. [I,C]

| TIC | Frozen S106 σ range (min) | Per-event min(3σ,30) (min) | Per-event max(3σ,30) (min) | max(3 mean σ,30), all rows (min) |
|---|---:|---:|---:|---:|
| 206620592 | 1.4 | 4.2 | 30 | 30 |
| 120444365 | 2.1 | 6.3 | 30 | 30 |
| 183374279 | 2.7–2.8 | 8.1–8.4 | 30 | 30 |
| 122522485 | 15.9–16.1 | 30 | 47.7–48.3 | 48.05 |
| 70441745 | 43.4 | 30 | 130.2 | 130.2 |
| 253931796 | 44.8–45.5 | 30 | 134.4–136.5 | 135.5 |
| 115692561 | 3.4 | 10.2 | 30 | 30 |
| 88407114 — **withdrawn S106 test** | 4.4 | 13.2 | 30 | 30; historical illustration only |

The “≈135 min” entry is not a substantive arithmetic error, but **≈136 min (134.4–136.5 per event)** is a clearer rounded description. The phrase “Among the Sector 106 objects” permits a non-exhaustive six-row table; omission of 115692561 there is not itself false. A referenced older full table containing 88407114 must now identify its withdrawn status. [B,I; reviewer judgment]

## Generator results and remaining evaluator limitations

The temporary TIC 53825235 run returned **136 rows, 110 beginning with `prediction`**; the first eligible row was epoch 4811, **2026-09-07 14:51 UTC**, S108, and the final row epoch 4946, **2026-11-25**, S110. The TIC 162304222 run returned **208 rows, all predictions**, from epoch 5348, **2026-11-26 10:04 UTC**, S111, to epoch 5555, **2027-03-14 17:36 UTC**, S114. These demonstrate that the 399-epoch truncation is removed for representative short periods; they do not validate every new ephemeris or justify replacing an old freeze in place. [G: temporary CSVs/logs]

The mock SPOC branch attempted `download_all` and accessed `remove_nans`, quality, time and flux for sectors 105, 106, 111, then passed only 105 to `sector_offset`. Thus **“SPOC test sectors never fitted” is true in this tested branch**, whereas **“never download test data” is false**. A synthetic QLP S106 object was passed to `sector_offset` and added to fitted rows. Tests used mocks; no real S106 flux was examined. A guard must run on sector metadata before downloading/reading data, apply to QLP and SPOC and any cutouts, and also ensure the upstream BLS/shape reference was not built from holdout data. [G]

The revised clarification honestly discloses major evaluator defects, but it is not an outcome-validation certificate. Beyond the expressly listed duration/full-coverage issues, the code still: fits a box of fixed supplied duration; averages potentially cancelling offsets using depth-error weights; permits a signed box coefficient without a positivity gate in the offset search; restricts that offset search to ±0.1 d even when the tolerance may be larger; scans displaced dips over ±0.3 d only after EXCLUDED fails; and implements INCONSISTENT as a local per-prediction test, not a proof of separation from every predicted event. Coverage is a cadence-count threshold, not an explicit uninterrupted contact/baseline test. These statements follow directly from `prereg_test.py:29–58`; the earlier synthetic examples remain relevant but were not repeated on real data. [C]

Do not silently repair the frozen evaluator or pretend the clarification repairs it. Preserve its literal output, define a separate conformance assessment and precedence before inspecting any **remaining unexamined** target/sector data, and retain both outcomes if they differ. The clarification can be published to document the conflict before that procedure exists; testing/reporting under a supposedly fully conformant executable cannot. [B,C; reviewer recommendation]

## Proposed exact replacement wording

The following text is proposed author wording, **not an independent certification of the authors' non-examination**. It should be adopted only where they can affirm it. The inventory and dates above supply its factual support. [A,F,L,P; reviewer proposal]

### A: availability, scope and interpretation

> Several records incorrectly described Sector 106 as “observed, data not public at freeze.” Public availability is product-specific. Retained local SPOC two-minute light-curve files for other targets establish access by 2026-10-17 approximately 16:45 UTC (12:45 EDT), before the freezes listed below. Public FFI products were also available; the MAST TICA notice dates recovery of missing S106 cadences to 2026-08-14. We have not established the exact first release time of all S106 SPOC or TESScut products. The absence of the checked target-specific QLP light curves did not mean that no S106 observations could be downloaded and analysed.
>
> The affected S106 records are TIC 120444365 v1/v2, 183374279 v2, 70441745 v2, 122522485 v2, 206620592 v2, 253931796 v2, 115692561 v2 and 88407114 v2. The first four registrations in this list were public; the later round-three freezes were local in the releases audited here. Analogous “data not public” status labels for S107 in TIC 160330868, 24526743 and 88407114 also require correction. The accompanying manifest lists every affected path and its unchanged prediction-file hash.
>
> Except for the withdrawn TIC 88407114 S106 test, we state that we did not inspect or use the affected target/sector photometry before each freeze. The audited frozen fitted-sector lists are consistent with this statement; they do not independently prove non-examination. An internal reviewer downloaded a 1×1 S106 cutout at TIC 206620592's position on 2026-10-20 at 01:21:13 UTC, after its 00:33:10 UTC freeze, and reports not inspecting its flux. This later download is disclosed here.
>
> These are predictions registered after the observations were acquired and public image products were available. Conditional on the stated non-examination, unchanged prediction selection and no other use of those data, they provide a held-out check of the frozen ephemerides. They are not prospective predictions of observations unavailable to the authors or public. For the valid affected rows, read the old status as “observed sector; public data existed; authors attest target-sector photometry was not examined before freeze.” This correction does not establish that every target had a public SPOC or QLP light curve.
>
> TIC 88407114 v2, frozen 2026-10-20 at 00:44:14 UTC, fitted S106 SPOC photometry and therefore cannot use S106 as an out-of-sample test. Its S106 test is withdrawn. Its original files and hashes are retained and marked accordingly; no publication of that freeze was found in the audited public release history. Other sectors require their own non-examination and eligibility assessment.
>
> TIC 89247735 has a separate ground-based test of record covering predictions in 2026–2027; its fourth TESS event remains a post hoc recovery. TIC 80387959's prospective S111 test begins with observations scheduled from 2026-11-26. Neither is invalidated by this S106 availability correction. Prediction CSV bytes and recorded digests are unchanged; amended explanatory documents receive new hashes.

Include the full timestamp table and inventory rather than retaining only the original four rows. [Reviewer recommendation]

### A: replace the process-fix promise unless the implementation is actually completed

> Process correction is incomplete. The current patch excludes declared test sectors from the SPOC ephemeris fit after loading them, but it does not prevent their download or flux access, does not protect the QLP loading path and does not query product availability for status labels. We will not generate a new freeze with this script until these paths have pre-download/pre-flux sector guards, product-specific availability records and explicit non-examination attestations. Existing frozen artifacts remain unchanged.

This wording accurately describes the reviewed code; alternatively implement the promised safeguards and publish the tests before claiming them. [G]

### B: scope and precedence

> This amendment resolves the conflicting timing clauses in the 37 identified TESS-v2 registrations. It adopts the already-public max() implementation as a dated precedence decision; it does not assert that the protocol preceded every object file or that the original min() reading was impossible. For each applicable, non-withdrawn TESS-v2 test, we will also report the individual-event min(3σ,30 min) assessment. Older v1 rules, TIC 61310956's dedicated v3 ground-based rules and TIC 89247735's v1 ground-based test are unchanged. TIC 88407114's S106 test is withdrawn because those data entered its fit, and is not an unevaluated test covered by this promise. The data-availability erratum documents which observations were already public and the limits of our non-examination attestation.
>
> For the remaining tests whose photometry has not been inspected, the separately versioned conformance procedure and its precedence will be fixed and published before inspection. We will preserve and report the frozen evaluator's literal output without equating it to satisfaction of every written criterion.

### C: exact timing-aggregation sentence for future TESS templates

> The frozen executable's timing gate is |Σ(wᵢΔtᵢ)/Σwᵢ| ≤ max[3 mean(σpred,ᵢ),30 min], where wᵢ=1/(depth_err,ᵢ)² and both summaries use the coverage-qualified prediction rows. These are inverse depth-variance weights, not depth weights or timing-uncertainty weights. Duration and complete-transit-coverage criteria are assessed separately under the versioned conformance procedure; see the dated timing clarification for precedence and exceptions.

### Protocol purpose and public summaries

> These records freeze predictions and assessment rules before the stated tests are evaluated. Some concern future observations; others concern already observed sectors whose image products were public at freeze and whose target photometry the authors attest they had not examined. The dated availability erratum identifies those records and the withdrawn test. Historical prediction files and rules remain on record; later amendments are separately dated and scoped.

This replaces the blanket “before the test data exist or are public” claim without erasing genuine prospective tests. [L,A; reviewer proposal]

## Limits and publication conditions

- **No exact first-release timestamp certified.** The report separates HTTP metadata, current service holdings, TICA's historical note and local filesystem times. No successful CAOM first-release query or S106 DRN was obtained. S108 service availability before the Oct-17 TIC 317134140 freeze is not established by the newer script modification date. [A]
- **No universal proof of blindness.** Disk/cache searches and fitted-sector scans support a bounded negative finding. They cannot certify author intent, non-access on other machines, deleted files, unlogged exploratory selection or absence of all external results. The local-only freeze timestamps are not independent public timestamps. [A,F,P]
- **Not a new transit-candidate validation.** I did not inspect S106/S107 target flux, refit the candidate physics, audit every upstream detection input, or re-evaluate the scientific claims of the old manuscripts. Dry runs used historical input sectors and outputs confined to `/tmp`; guard tests were synthetic. [G,C]
- **Inventory scope:** all matched current/staged records in the named trees are listed, along with located cached duplicates. The inspected public protocol/preprint versions were opened; this does not certify every version of every remote archive. Existing cached reviews are evidence, not mutable author prose. [L,P]
- **Release requirements:** for A, resolve A1–A8 and provide the affected-path/withdrawal mapping; either implement the claimed safeguards or explicitly call them pending. For B, make the scope/non-examination correction, correct aggregation in the accompanying template, flag withdrawn 88407114 in linked impact material, and link the published availability erratum. Publish the corrected notes with links beside the current records and new document manifests while retaining old CSVs/releases. A promised future conformance procedure must be completed before any remaining holdout data are inspected or certified. [Reviewer judgment based on findings above]

Only `results/REVIEW_erratum_and_clarification.md` was written inside the project by this review. Temporary diagnostics and outputs were written under `/tmp`; nothing was published, pushed, uploaded or sent to another person.
