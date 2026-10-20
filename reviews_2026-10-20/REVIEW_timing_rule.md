# Independent review of the timing-rule clarification

**Date:** 2026-10-20 UTC. **Reviewer/tool:** OpenAI Codex, using shell, Python, public HTTP APIs and PDF extraction/rendering. **Workspace:** `/Users/fernando/Desktop/NASA`.

**Sources actually opened:** the local clarification, protocol TEX/PDF, evaluator, generator, decision log, all local/public/cached PREREGISTRATION Markdown files found under `results/` and `public_release/`, versioned prediction CSVs and corresponding JSON/hash records, and `paper/rnaas/note.tex`; the public GitHub commit APIs; Zenodo record APIs and ZIP contents for the original protocol, v1.2, v1.3 and the earlier data release; and MAST QLP availability endpoints. The protocol PDF's outcome page was also rendered and inspected. No Sector-106 test photometry was loaded. Only this report was written inside the repository; diagnostic scripts, downloaded public documents and synthetic outputs were written under `/tmp/timing_rule_review/`.

## Verdict: handled with fixes needed

Using `max(3σ, 30 min)` is a defensible **dated resolution of a documented conflict**, because that rule and the identical evaluator were already public in the first protocol deposit, well before this clarification. It is not defensible to claim that they preceded every object registration, that the clarification affects only uncertainties above 10 minutes, or that all 40 appended notes correct an original 30-minute clause. Two objects' v1/v2 registrations demonstrably predate the protocol; only 37 local originals contain that clause, and three addenda misquote older 60-minute rules. The prediction CSVs pass the applicable hash checks, but the public copies still lack the clarification, and the evaluator demonstrably fails other stated requirements. Publish a corrected, explicitly scoped amendment before applying the test; preserve the original artifacts and report both the frozen evaluator's output and any separately specified protocol-conformance assessment. The present clarification is **not ready to be published unchanged**. [P,G,L,H,T below]

## Evidence key and reproducible checks

All unqualified paths are relative to the workspace. Evidence labels on tables and paragraphs apply to every factual entry in them.

- **[L: local documents/inventory]** Read the named files with `cat`, `nl -ba`, and Python `Path.read_text()`. Exhaustive text searches included `rg -l -F 'and in any case within +-30 min' results public_release` and `rg -l 'and in any case within.*30' results public_release`; stripped the dated addendum before classifying an original as affected. Enumerated `PREREGISTRATION*.md` recursively. The inventory and exact byte-prefix comparisons are in `/tmp/timing_rule_review/{inventory.py,inventory.json,extra_checks.py}`. Read `logs/DECISIONS.md:325–332`, not as proof of publication, but as the authors' account.
- **[P: protocol/archive]** Independently fetched [original protocol API](https://zenodo.org/api/records/23462442), [v1.2 API](https://zenodo.org/api/records/23474138), [v1.3 API](https://zenodo.org/api/records/23477866), and their ZIPs through each API's file-content URL. Read archived `PREREG_PROTOCOL.tex`, extracted PDF text, `prereg_test.py`, `SHA256SUMS.txt` and registrations. Also read local `prereg_protocol/PREREG_PROTOCOL.tex` and PDF p. 2 (“Fixed procedure” and “Outcome rules”). Commands included `pdftotext -layout`, `pdftoppm -f 2 -singlefile`, and `shasum -a 256`. Public downloads/checks are recorded in `/tmp/timing_rule_review/public_check.py` and directories named by record ID.
- **[G: public chronology]** Ran `git -C public_release log --diff-filter=A --format='%H %cI' -- <path>` for each object file and checked the relevant commits against the GitHub API. The [current head API](https://api.github.com/repos/fergmolina/tess-transit-candidates/commits?per_page=1) returned `d995a1fff8ad24171cad4bd35dc07ebe04a66539`, matching the local checkout. Also fetched the [earlier data-record API](https://zenodo.org/api/records/23460915) and its ZIP, independently establishing that the early ambiguous registrations were archived before the protocol. Git commit times are not independently certified push times; the earlier Zenodo archive supplies stronger evidence than a commit timestamp alone. Scripts: `/tmp/timing_rule_review/{availability.py,early_archive.py}`.
- **[H: hashes]** Used `hashlib.sha256(path.read_bytes()).hexdigest()` on every `predicted_transits_*_v*.csv` under both requested trees; compared full digests, not just prefixes, with JSON and registration entries. Compared current public CSV bytes with `git show <first-addition-commit>:<path>`, and local/public duplicate bytes. Scripts/results: `/tmp/timing_rule_review/{inventory.py,hash_final.py,hashes.json,v1_hashes.json}`. The v4/v5 TIC 89247735 public registrations use a different hash-label format and were checked separately by reading them in full.
- **[I: impact]** Read each affected original's named frozen CSV with `csv.DictReader`; retained `status.startswith('prediction')`, grouped by the recorded sector label, and computed `3*float(sigma_min)`, `min(3σ,30)`, and `max(3σ,30)`. No ephemeris was refitted and no sigma was recomputed from a summary. `/tmp/timing_rule_review/{further.py,impact.json,stats.py}` contains the calculations. Sector labels and coverage forecasts are inherited from these files, not independently certified here.
- **[C,T: code and execution]** Read all 60 lines of `scripts/prereg_test.py` and the generation logic in `scripts/prereg_v2.py`. Re-ran the unchanged evaluator on seven deterministic synthetic inputs with `.venv/bin/python -B -I scripts/prereg_test.py --lc <synthetic.csv> --pred <synthetic_pred.csv> --depth-ppm 1000 --dur-h 2 --sector 106 --out <temporary.json>`. Exact commands and output are in `/tmp/timing_rule_review/test_*.log` and `test_*.json`; driver `synthetic_check.py`. Synthetic inputs and their construction are in `/tmp/s106_audit/{dryrun.py,additional_cases.py,synthetic_*.csv}`; the construction is summarized below.
- **[A: availability]** Read the [MAST QLP page](https://archive.stsci.edu/hlsp/qlp), checked sector-product endpoints using read-only HTTP GET, and attempted a read-only MAST CAOM query. URLs/statuses and limits are given below; raw status records are in `/tmp/timing_rule_review/{availability.json,mast_retry.txt,mast_qlp.txt}`.

## Findings and required fixes

| Issue | Evidence and assessment | Required fix |
|---|---|---|
| False blanket chronology | Clarification lines 13–14 says protocol/evaluator were “both public before these files.” Four v1/v2 files for TIC 80387959 and 120444365 were in commit `24cd0de` and the earlier Zenodo archive; see chronology below. [G,P] | Replace with the actual dates. Describe a conflict resolved before evaluation, not an always-unambiguous precedence rule. |
| Impact statement mathematically wrong | Clarification line 16 says the difference matters “only” for σ > 10 min. The two gates differ whenever σ ≠ 10 min. S106 TIC 120444365 is 6.3 versus 30 min; TIC 206620592 is 4.2 versus 30 min. [I] | Correct the statement and publish the full impact table, including precise ephemerides. |
| Incorrect scope/count and three erroneous addenda | 37 original v2 files contain the 30-minute phrase; the 40 appended files include three v1 files with a 60-minute clause generated by `prereg_candidate.py`. No affected original v3 was found. [L] | Correct count and filenames. Append a retraction/correction of the three misapplied addenda; do not silently delete historical text or impose the newer v2 rule on v1. |
| Local versus public completion | All 37 affected local v2 originals have an addendum. All 20 corresponding affected public-release v2 files lack it; GitHub head remains v1.9. Log item 66 explicitly says public copies follow in v2.0. [L,G] | Make the corrected clarification discoverable in a new public release and link it from each current affected record. Preserve archived old releases. |
| Claim that no frozen file changes | Appending changes Markdown bytes and its SHA-256 even when every original byte and embedded CSV digest survives. For the 22 records with public counterparts, the original file is an exact byte prefix of the amended file. [L,H] | Say original text and prediction CSV bytes/digests are preserved; distinguish old document hashes from new amended-document hashes. |
| Evaluator not equivalent to advertised rules | No measured-duration check; exclusion does not require full transit coverage; ordering and residual category are underdescribed. Synthetic failures below. [C,T,P] | Keep the frozen executable immutable, document its defects, and predeclare a separately versioned conformance procedure and reporting hierarchy before test-data inspection. |
| Scope cannot be “every object” | TIC 61310956 v3 has dedicated ground rules (two epochs, each SNR ≥ 4, per-epoch 3σ gate); original v1 records and TIC 89247735 have different tests. [L,P] | Limit this amendment to the listed TESS v2 timing clause. Enumerate exceptions and precedence over, or preservation of, specific later addenda. |
| Three files have no eligible predictions | TIC 162304222, 408110117 and 53825235 v2 CSVs contain only rows labelled retrodiction; evaluator line 23 drops all of them. [I,C] | Fix with a new, dated freeze that preserves the old files, extends generation to actual test dates, and explicitly identifies unreleased observed sectors. Do not call an empty selection a completed test. |
| New template is not verbatim protocol | Generator line 134 fixes `max()` but says “reference values of >= 2 predicted times”, omits the inconsistency search interval and retains other prose/code discrepancies. [L,C,P] | Fix grammar, specify timing aggregation and precedence, and remove the assertion “verbatim”. Validate output with representative TESS/ground fixtures without overwriting frozen records. |

## 1. Which rule governs, and what was public when?

The protocol explicitly specifies `max(3σ_pred,30 min)`. All three downloaded protocol versions contain that expression in both TEX and PDF. Their evaluator is byte-identical to the current local executable:

`630815cc1400f0434dc9f30c8ce08cc42635ee5d1d429338c4010f6115043366`.

That digest agrees with each archived `SHA256SUMS.txt` entry. The exact implementation is `max(3 * cov.sigma_pred_min.mean(), 30.0)`: an arithmetic mean of prediction sigmas over covered rows, not a per-event gate or the standard error of a stacked time. The offset is averaged with **depth-error** inverse-variance weights. Its branch order is: fewer than two covered → INSUFFICIENT; otherwise RECOVERED, then EXCLUDED, then a displaced-dip scan → INCONSISTENT or AMBIGUOUS. [P,C:42–58]

| Public artifact | Verified UTC time | What it establishes |
|---|---|---|
| GitHub first addition of TIC 80387959 / 120444365 v1 and v2 | 2026-10-18 23:24:45 | [Commit 24cd0de](https://github.com/fergmolina/tess-transit-candidates/commit/24cd0deb40ce35f49a37236ffced762e319b5e84); the API lists all four additions. [G] |
| Earlier data release 23460915 | Created 2026-10-18 23:24:53.814353 | Its downloaded ZIP contains those four files; the v2 files contain the ambiguous 30-minute wording. [Earlier archive](https://zenodo.org/records/23460915). [G] |
| Original protocol 23462442 | Created 2026-10-19 01:36:22.688677 | First requested protocol deposit; contains both max() protocol/evaluator and conflicting object files. [P] |
| GitHub first addition of TIC 183374279 v2 | 2026-10-19 12:15:57 | [Commit 1ba1f67](https://github.com/fergmolina/tess-transit-candidates/commit/1ba1f673127b5d54a4974c44a98a4b6cff043051). [G] |
| Protocol v1.2, 23474138 | Created 2026-10-19 12:16:25.531850 | Adds that object to the bundle; initial max() executable unchanged. [P] |
| GitHub round-2 object additions | 2026-10-19 14:54:52 | [Commit b944812](https://github.com/fergmolina/tess-transit-candidates/commit/b944812ac44173c3b3cad3d4a368625b837a8891); individual files listed below. [G] |
| Protocol v1.3, 23477866 | Created 2026-10-19 14:55:17.765642 | Includes round-2 registrations and dedicated TIC 61310956 v3; evaluator unchanged. [P] |
| Current public GitHub head at this review | 2026-10-19 20:19:23 commit time | `d995a1f`; no Oct-20 clarification commit observed. Local checkout clean. [G] |

The two early v2 freezes were internally timestamped **2026-10-18 22:34:41** (80387959) and **22:34:49 UTC** (120444365), also before the protocol's creation. The later round-2 files postdate the first protocol. Seventeen local v2 files have no corresponding path in the inspected public Git history; their internal timestamps establish what the files claim, not an independent public freeze. The per-file table below gives the full chronology. [L,G]

**Judgment:** max() is demonstrably an earlier public specification, not a newly written lenient rule. But the earlier object text and the protocol's own “It supersedes nothing” sentence prevent treating this as an uncontested historical hierarchy. Applying max() now is reasonable if explicitly presented as a pre-evaluation resolution/adoption, with the original narrower interpretation retained in the record and reported as a sensitivity check. It should not be sold as proving that the object documents always meant max(). The fact that both inconsistent forms coexist in the original protocol bundle strengthens the need to acknowledge the conflict. [P: Purpose and archived registrations; G; reviewer assessment]

This also qualifies my earlier S106 report's timing recommendation: `results/referee_89247735/REVIEW_S106_test_procedure.md` advocated min() from the per-object wording. The independently downloaded public protocol now supplies contrary, prior evidence. I do **not** recommend silently changing the frozen executable to min(), nor silently erasing the narrower recorded wording. The duration/coverage implementation defects survive this correction. [Earlier report, timing row; P,C,T]

### Availability and the “no result yet” claim

During this review on **2026-10-20 UTC** (initial product checks at approximately 01:20 UTC), GETs for these exact S106 QLP FITS products returned **404**, while matching S105 paths for both stars returned **200** (a useful path-validity control): [A]

- [TIC 120444365 S106 product](https://archive.stsci.edu/hlsps/qlp/s0106/0000/0001/2044/4365/hlsp_qlp_tess_ffi_s0106-0000000120444365_tess_v01_llc.fits) — first attempt timed out, retry 404.
- [TIC 183374279 S106 product](https://archive.stsci.edu/hlsps/qlp/s0106/0000/0001/8337/4279/hlsp_qlp_tess_ffi_s0106-0000000183374279_tess_v01_llc.fits) — 404.

The [S106 QLP download script](https://archive.stsci.edu/hlsps/qlp/download_scripts/hlsp_qlp_tess_ffi_s0106_tess_v01_llc-fits.sh) and sector-directory endpoint also returned 404. The QLP landing page linked sectors only through 104, despite the successful S105 controls, so the landing page alone is not authoritative evidence of absence. The S106 target-list and MAST CAOM query attempts timed out. [A]

These checks support **“the checked S106 QLP products were not publicly available at review time.”** They do not prove that no SPOC/TESScut/FFI data, private reduction, or result exists anywhere, nor independently establish the authors' non-access. Sector 106 had already been observed, as the protocol and frozen status fields themselves say. Use “before public release/inspection of the test photometry”, not “before the data exist.” I found no basis here for alleging outcome-driven selection, but cannot certify the universal absence of results. [A,P,L; inference and limits]

## 2. Complete affected-file inventory and original-text preservation

The recursive scan found **91 PREREGISTRATION Markdown files**, including public and historical copies. There are **37 affected original local v2 files**, all in `results/vet_allsky/`, and **40 local timing addenda**. No original v3 has the disputed 30-minute phrase. Three additional matches come solely from the newly appended quotation in older v1 documents, not from their original rule. There are **20 affected public-release originals** and **five cached historical originals**, none amended. [L]

In this table, **A** means correctly targeted addendum present and every byte of the old public file remains an exact prefix, checked against both its first-addition Git version and the present public copy. **B** means correctly targeted addendum and original sentence present, but no independently archived pre-append counterpart was located, so full historical byte preservation cannot be certified. **X** means a misapplied addendum quoting 30 minutes where the original says 60. Dates are the `Frozen:` text, UTC. Commit codes are defined in the chronology table; “not found” means absent from the inspected public repository history, not proof of absence from every website. [L,G]

| Local file | Frozen UTC | First public commit | Status |
|---|---|---|---|
| `results/vet_allsky/115692561/PREREGISTRATION_v2.md` | 2026-10-20 00:44:10 | not found | B |
| `results/vet_allsky/120444365/PREREGISTRATION.md` | 2026-10-18 20:26:00 | 24cd0de | X; public prefix preserved |
| `results/vet_allsky/120444365/PREREGISTRATION_v2.md` | 2026-10-18 22:34:49 | 24cd0de | A |
| `results/vet_allsky/120517801/PREREGISTRATION.md` | 2026-10-18 20:25:07 | not found | X; historical prefix unverified |
| `results/vet_allsky/120517801/PREREGISTRATION_v2.md` | 2026-10-18 22:34:41 | not found | B |
| `results/vet_allsky/122522485/PREREGISTRATION_v2.md` | 2026-10-20 00:33:06 | not found | B |
| `results/vet_allsky/159033763/PREREGISTRATION_v2.md` | 2026-10-20 00:43:55 | not found | B |
| `results/vet_allsky/160330868/PREREGISTRATION_v2.md` | 2026-10-20 00:43:17 | not found | B |
| `results/vet_allsky/162304222/PREREGISTRATION_v2.md` | 2026-10-20 00:44:05 | not found | B |
| `results/vet_allsky/183374279/PREREGISTRATION_v2.md` | 2026-10-19 11:44:14 | 1ba1f67 | A |
| `results/vet_allsky/19119739/PREREGISTRATION_v2.md` | 2026-10-20 00:44:39 | not found | B |
| `results/vet_allsky/196514928/PREREGISTRATION_v2.md` | 2026-10-20 00:43:22 | not found | B |
| `results/vet_allsky/203381983/PREREGISTRATION_v2.md` | 2026-10-19 12:46:58 | b944812 | A |
| `results/vet_allsky/206620592/PREREGISTRATION_v2.md` | 2026-10-20 00:33:10 | not found | B |
| `results/vet_allsky/24526743/PREREGISTRATION_v2.md` | 2026-10-20 00:43:31 | not found | B |
| `results/vet_allsky/245503256/PREREGISTRATION_v2.md` | 2026-10-19 12:51:25 | b944812 | A |
| `results/vet_allsky/249813122/PREREGISTRATION_v2.md` | 2026-10-19 12:51:17 | b944812 | A |
| `results/vet_allsky/253931796/PREREGISTRATION_v2.md` | 2026-10-20 00:33:12 | not found | B |
| `results/vet_allsky/258006047/PREREGISTRATION_v2.md` | 2026-10-19 11:44:14 | b944812 | A |
| `results/vet_allsky/283913390/PREREGISTRATION_v2.md` | 2026-10-20 00:43:28 | not found | B |
| `results/vet_allsky/332709057/PREREGISTRATION_v2.md` | 2026-10-19 12:51:30 | b944812 | A |
| `results/vet_allsky/333661705/PREREGISTRATION_v2.md` | 2026-10-20 00:44:26 | not found | B |
| `results/vet_allsky/333735955/PREREGISTRATION_v2.md` | 2026-10-19 12:46:54 | b944812 | A |
| `results/vet_allsky/3367979/PREREGISTRATION_v2.md` | 2026-10-19 12:47:13 | not found | B |
| `results/vet_allsky/366047768/PREREGISTRATION_v2.md` | 2026-10-19 12:47:01 | b944812 | A |
| `results/vet_allsky/36694943/PREREGISTRATION_v2.md` | 2026-10-19 12:51:27 | b944812 | A |
| `results/vet_allsky/371421714/PREREGISTRATION_v2.md` | 2026-10-19 12:51:35 | b944812 | A |
| `results/vet_allsky/376225363/PREREGISTRATION_v2.md` | 2026-10-19 12:51:20 | b944812 | A |
| `results/vet_allsky/383617106/PREREGISTRATION_v2.md` | 2026-10-19 12:47:16 | b944812 | A |
| `results/vet_allsky/408110117/PREREGISTRATION_v2.md` | 2026-10-20 00:44:17 | not found | B |
| `results/vet_allsky/467959906/PREREGISTRATION_v2.md` | 2026-10-19 12:51:14 | b944812 | A |
| `results/vet_allsky/50514263/PREREGISTRATION_v2.md` | 2026-10-19 12:51:23 | b944812 | A |
| `results/vet_allsky/53825235/PREREGISTRATION_v2.md` | 2026-10-20 00:43:36 | not found | B |
| `results/vet_allsky/61310956/PREREGISTRATION_v2.md` | 2026-10-19 12:45:32 | b944812 | A |
| `results/vet_allsky/65575657/PREREGISTRATION_v2.md` | 2026-10-19 12:51:32 | b944812 | A |
| `results/vet_allsky/70441745/PREREGISTRATION_v2.md` | 2026-10-19 12:51:12 | b944812 | A |
| `results/vet_allsky/80387959/PREREGISTRATION.md` | 2026-10-18 19:40:16 | 24cd0de | X; public prefix preserved |
| `results/vet_allsky/80387959/PREREGISTRATION_v2.md` | 2026-10-18 22:34:41 | 24cd0de | A |
| `results/vet_allsky/88407114/PREREGISTRATION_v2.md` | 2026-10-20 00:44:14 | not found | B |
| `results/vet_allsky/91617711/PREREGISTRATION_v2.md` | 2026-10-19 12:51:37 | b944812 | A |

The **three X entries** are `results/vet_allsky/{80387959,120444365,120517801}/PREREGISTRATION.md`. Each original says `within +-3 sigma_min (and in any case within +-60 min)`, requires depth **0.6–1.5×**, and sets the inconsistent threshold to **60 minutes**. Its generator is `scripts/prereg_candidate.py`, not `prereg_v2.py`. The appended statement that “the phrase ... +-30 min above misstates the rule” is false in all three. Correct these addenda explicitly rather than extending a v2-specific clarification retroactively. [L: each file's Outcomes and final generator sentence]

The original 22 public-backed local Markdown prefixes are byte-preserved; the other 18 cannot be independently compared with a pre-change public original in the material located. None of the 37 actual local 30-minute originals was missed. The absence of an addendum on TIC 61310956 **v3** and on TIC 89247735's original records is appropriate: those are different rules, not instances of this wording defect. TIC 61310956 **v2** does contain it and is correctly annotated as a historical superseded record. [L,G]

### Public-release files still requiring a linked clarification in the next release

Every file below still contains the original 30-minute clause and has **no timing addendum**. This is consistent with log item 66's promise of a later public release, but means public remediation is not yet complete. Do not alter already deposited immutable versions; issue a new version with accurate cross-links. [L,G]

- `public_release/preregistration/TIC120444365/PREREGISTRATION_v2.md` — unamended public copy.

- `public_release/preregistration/TIC183374279/PREREGISTRATION_v2.md` — unamended public copy.

- `public_release/preregistration/TIC203381983/PREREGISTRATION_v2.md` — unamended public copy.

- `public_release/preregistration/TIC245503256/PREREGISTRATION_v2.md` — unamended public copy.

- `public_release/preregistration/TIC249813122/PREREGISTRATION_v2.md` — unamended public copy.

- `public_release/preregistration/TIC258006047/PREREGISTRATION_v2.md` — unamended public copy.

- `public_release/preregistration/TIC332709057/PREREGISTRATION_v2.md` — unamended public copy.

- `public_release/preregistration/TIC333735955/PREREGISTRATION_v2.md` — unamended public copy.

- `public_release/preregistration/TIC366047768/PREREGISTRATION_v2.md` — unamended public copy.

- `public_release/preregistration/TIC36694943/PREREGISTRATION_v2.md` — unamended public copy.

- `public_release/preregistration/TIC371421714/PREREGISTRATION_v2.md` — unamended public copy.

- `public_release/preregistration/TIC376225363/PREREGISTRATION_v2.md` — unamended public copy.

- `public_release/preregistration/TIC383617106/PREREGISTRATION_v2.md` — unamended public copy.

- `public_release/preregistration/TIC467959906/PREREGISTRATION_v2.md` — unamended public copy.

- `public_release/preregistration/TIC50514263/PREREGISTRATION_v2.md` — unamended public copy.

- `public_release/preregistration/TIC61310956/PREREGISTRATION_v2.md` — unamended public copy.

- `public_release/preregistration/TIC65575657/PREREGISTRATION_v2.md` — unamended public copy.

- `public_release/preregistration/TIC70441745/PREREGISTRATION_v2.md` — unamended public copy.

- `public_release/preregistration/TIC80387959/PREREGISTRATION_v2.md` — unamended public copy.

- `public_release/preregistration/TIC91617711/PREREGISTRATION_v2.md` — unamended public copy.

### Historical cached registrations

These five files also contain the original wording and no addendum. They are evidence snapshots, not current operational records; preserve them and point to the clarification from a separate index rather than rewriting the evidence. [L]

- `results/prior_search/data/github_sweep/fergmolina__tess-transit-candidates/preregistration/TIC120444365/PREREGISTRATION_v2.md` — historical copy, unamended.

- `results/prior_search/data/github_sweep/fergmolina__tess-transit-candidates/preregistration/TIC80387959/PREREGISTRATION_v2.md` — historical copy, unamended.

- `results/prior_search_round2/data/github_sweep/fergmolina__tess-transit-candidates/preregistration/TIC120444365/PREREGISTRATION_v2.md` — historical copy, unamended.

- `results/prior_search_round2/data/github_sweep/fergmolina__tess-transit-candidates/preregistration/TIC183374279/PREREGISTRATION_v2.md` — historical copy, unamended.

- `results/prior_search_round2/data/github_sweep/fergmolina__tess-transit-candidates/preregistration/TIC80387959/PREREGISTRATION_v2.md` — historical copy, unamended.

### Other matching text files under the requested trees

The literal-text searches also find the following non-registration files. These complete the matching-text inventory; they are not additional object freezes. Counts/searches precede creation of this report. The clarification itself uses the Unicode ± variant. [L]

| File | Status/action |
|---|---|
| `public_release/referee_round2/REFEREE_REPORT.md` | Historical template/archive extract or referee quotation; preserve, not an unamended active freeze. |
| `public_release/scripts/prereg_v2.py` | Old public generator still emits the wrong clause; replace only in a new release. |
| `results/CLARIFICATION_TIMING_RULE_2026-10-20.md` | Quotes the defect intentionally; revise the inaccurate chronology, count and impact claims. |
| `results/PROMPT_timing_rule_review.txt` | Review instructions quoting the defect; no operational amendment needed. |
| `results/prior_search/data/github_sweep/fergmolina__tess-transit-candidates/scripts/prereg_v2.py` | Historical template/archive extract or referee quotation; preserve, not an unamended active freeze. |
| `results/prior_search/data/zenodo_deep/23460915/tess-transit-candidates-v1.3.zip.txt` | Historical template/archive extract or referee quotation; preserve, not an unamended active freeze. |
| `results/prior_search_round2/data/github_sweep/fergmolina__tess-transit-candidates/scripts/prereg_v2.py` | Historical template/archive extract or referee quotation; preserve, not an unamended active freeze. |
| `results/prior_search_round2/data/zenodo_new/23462438/supporting_data_and_code_v1.zip.txt` | Historical template/archive extract or referee quotation; preserve, not an unamended active freeze. |
| `results/prior_search_round2/data/zenodo_new/23474130/tess-transit-candidates-v1.6.zip.txt` | Historical template/archive extract or referee quotation; preserve, not an unamended active freeze. |
| `results/prior_search_round2/data/zenodo_new/23474138/preregistration_bundle_v1.2.zip.txt` | Historical template/archive extract or referee quotation; preserve, not an unamended active freeze. |
| `results/qlp_clock_v2/prereg_v2_before_clockflag.py` | Historical template/archive extract or referee quotation; preserve, not an unamended active freeze. |
| `results/referee_round2/REFEREE_REPORT.md` | Historical template/archive extract or referee quotation; preserve, not an unamended active freeze. |
| `results/round2_dossiers/DOSSIERS.md` | Two copied rule passages (lines 28, 131); add a cross-reference if circulated as current guidance. |

## 3. Prediction integrity and checksum audit

**No prediction-CSV hash discrepancy was found.** There are **92 files** matching the requested versioned CSV glob, representing **48 distinct byte sequences**. Of these, **76 primary-file copies** (42 distinct primary predictions) agree with their associated JSON SHA-256 and a registration digest. For local TIC 89247735 v4/v5, there is no local `results/vet_qlp/.../PREREGISTRATION_v4.md` or `_v5.md`; the matching full hashes are in `public_release/preregistration/TIC89247735/PREREGISTRATION_v4.md` and `_v5.md`. All 31 versioned CSVs in `public_release/` match their first-addition Git bytes; all 31 corresponding local versions match the public bytes. Also checked the three v1 CSVs whose Markdown received an incorrect addendum: all match their JSON and original registration hashes. [H]

The remaining **16 copies**, six distinct `_utcfix`/`_utcfix2` products, have no corresponding primary-CSV hash entry in the named ephemeris JSON/registration. It would be incorrect to compare them with the primary CSV hash and call the difference corruption. Their public versions are among the unchanged Git-history checks above; the duplicates have the same hashes. These exceptions are listed after the primary table. For unpublished local primary files, agreement between local CSV/JSON/Markdown is internal consistency, not independent evidence of a historical public freeze. [H]

Each primary row below names the directory and version: the tested file is `predicted_transits_2026_2027_<version>.csv`, and the matching JSON is `final_ephemeris_<version>.json`. “Registration” means matching `PREREGISTRATION_<version>.md`, with the public counterpart used for local 89247735 v4/v5. Full 64-character values were compared; prefixes are displayed for readability. [H]

| Directory | Version | SHA-256 prefix | JSON / registration |
|---|---|---|---|
| `results/vet_allsky/115692561` | v2 | d8fe193dfce2 | match / match |
| `results/vet_allsky/120444365` | v2 | 32b5e0857265 | match / match |
| `results/vet_allsky/120517801` | v2 | 0e6bd698e1f4 | match / match |
| `results/vet_allsky/122522485` | v2 | 47ce36bcb863 | match / match |
| `results/vet_allsky/159033763` | v2 | c45eb808cb65 | match / match |
| `results/vet_allsky/160330868` | v2 | fa72f33be927 | match / match |
| `results/vet_allsky/162304222` | v2 | 742f2b162856 | match / match |
| `results/vet_allsky/183374279` | v2 | 069d82980645 | match / match |
| `results/vet_allsky/19119739` | v2 | 5aafcdd96fd6 | match / match |
| `results/vet_allsky/196514928` | v2 | 1fa2a7e068d3 | match / match |
| `results/vet_allsky/203381983` | v2 | 6ff79f8e8c20 | match / match |
| `results/vet_allsky/206620592` | v2 | 75b6ea732c2d | match / match |
| `results/vet_allsky/24526743` | v2 | 5a39b787e00b | match / match |
| `results/vet_allsky/245503256` | v2 | 41678702f848 | match / match |
| `results/vet_allsky/249813122` | v2 | 8c47e87946d9 | match / match |
| `results/vet_allsky/253931796` | v2 | 7ac1b3519df0 | match / match |
| `results/vet_allsky/258006047` | v2 | 48805ca7e45c | match / match |
| `results/vet_allsky/283913390` | v2 | fe3ad4669d29 | match / match |
| `results/vet_allsky/332709057` | v2 | 32afcd7e3e1c | match / match |
| `results/vet_allsky/333661705` | v2 | e7752bf76ab7 | match / match |
| `results/vet_allsky/333735955` | v2 | c8551f9c33d0 | match / match |
| `results/vet_allsky/3367979` | v2 | ea98dcc1f26f | match / match |
| `results/vet_allsky/366047768` | v2 | 1e246164f007 | match / match |
| `results/vet_allsky/36694943` | v2 | a51d71a19947 | match / match |
| `results/vet_allsky/371421714` | v2 | d1d84735958d | match / match |
| `results/vet_allsky/376225363` | v2 | 034139b99d99 | match / match |
| `results/vet_allsky/383617106` | v2 | edf4f0ef1271 | match / match |
| `results/vet_allsky/408110117` | v2 | bc55f95639e2 | match / match |
| `results/vet_allsky/467959906` | v2 | 58a25a2ea6f6 | match / match |
| `results/vet_allsky/50514263` | v2 | edba125f1f09 | match / match |
| `results/vet_allsky/53825235` | v2 | 6924d7b6140d | match / match |
| `results/vet_allsky/61310956` | v2 | 1f15a633e0e5 | match / match |
| `results/vet_allsky/61310956` | v3 | 76e892963501 | match / match |
| `results/vet_allsky/65575657` | v2 | 8e7400d246ac | match / match |
| `results/vet_allsky/70441745` | v2 | 243babb143e6 | match / match |
| `results/vet_allsky/80387959` | v2 | 5d0e7651818e | match / match |
| `results/vet_allsky/88407114` | v2 | 751ec316080a | match / match |
| `results/vet_allsky/91617711` | v2 | 559b438ceac0 | match / match |
| `results/vet_qlp/89247735` | v2 | 8a2b1ccadd1b | match / match |
| `results/vet_qlp/89247735` | v3 | b5338c90e0ac | match / match |
| `results/vet_qlp/89247735` | v4 | 4f6aba63e252 | match / match (public MD) |
| `results/vet_qlp/89247735` | v5 | 216e7a4c6a98 | match / match (public MD) |

UTC companion files, each also byte-identical to its existing public counterpart (the four historical-cache copies are duplicates of these products): [H]

- `results/vet_allsky/120444365/predicted_transits_2026_2027_v2_utcfix.csv` — SHA-256 `f6241276c680cc6f70c9b81d6bf186c42f3d3e670e4e79a3bac28a823ac13164`.

- `results/vet_allsky/80387959/predicted_transits_2026_2027_v2_utcfix.csv` — SHA-256 `a9cf83636da6708f5f2df8164c33a1f12f6cf4e41cd08d9ab746afc90a721813`.

- `results/vet_qlp/89247735/predicted_transits_2026_2027_v2_utcfix.csv` — SHA-256 `a523f74c8be7de0fedd5a2c78d519fcd10e80804f1a3f728087271a3682bff96`.

- `results/vet_qlp/89247735/predicted_transits_2026_2027_v2_utcfix2.csv` — SHA-256 `d9f591e49391559b94373ce4aed1d32b4bbabf4ea3c6b480efab20c7a3620664`.

- `results/vet_qlp/89247735/predicted_transits_2026_2027_v3_utcfix.csv` — SHA-256 `27b2ee62e9dca5feb00a10f7ff8623b57951067e3bc96c38eb293592dcd36808`.

- `results/vet_qlp/89247735/predicted_transits_2026_2027_v3_utcfix2.csv` — SHA-256 `10b9e1f71dd4bbf12b0407479ff8b37ad4c6bc17853ed755f9d186b21273e3e6`.

Appending **does** change a frozen Markdown document's hash. For example, TIC 120444365 v2's public original has SHA-256 `cc6ce346a993eb85ebe420f492d3679d29cb85d06c0853569c2a16b036d1d674`; the appended local file is `57ad8b1f31b371fcbb01255a1545450a45be2861f2110875aba8d4ac05a9bdad`. Its prediction CSV remains `32b5e0857265e33e4902c5736d379bf0d7443516a9277678c2b403ac7b22de17`. Thus “no frozen file ... is changed” is false, while “original text and prediction CSV bytes/digests are preserved” is supported where a historical comparison exists. Retain old manifests for old bytes and create new manifests for amended files. [H,L]

## 4. Practical impact from the frozen CSVs

Let `a = 3σ` minutes. The two timing gates are **equal only if a = 30**; otherwise max() is wider by **|a−30|**. For σ < 10 min the change is from 3σ to 30 min; for σ > 10 min it is from 30 min to 3σ. These are timing gates, not guarantees of a changed final outcome, since depth, SNR, coverage, search-window limits and precedence still apply. [Arithmetic; I,C]

All rows below are computed from the named frozen v2 CSVs, not rounded ephemeris parameters. For a row labelled TIC N, the source is `results/vet_allsky/N/predicted_transits_2026_2027_v2.csv`. Epoch ranges are inclusive and consecutive within each row. Ranges in the min/max columns are **per-epoch** tolerances. For groups with at least two rows, the last column is what the existing code would use if **all rows in that group** passed coverage: `max(3*mean(sigma_min),30)`; actual coverage can change that mean. A one-row sector returns INSUFFICIENT before any timing tolerance is computed. [I,C:44–47]

### Dated TESS-sector rows

| TIC | Sector | Epochs | σ (min) | 3σ (min) | min() (min) | max() (min) | Code, all covered (min) |
|---|---|---|---|---|---|---|---|
| 115692561 | 106 | 3386–3417 | 3.4 | 10.2 | 10.2 | 30.0 | 30.00 |
| 120444365 | 106 | 559–564 | 2.1 | 6.3 | 6.3 | 30.0 | 30.00 |
| 120517801 | 111 | 636–643 | 15.9–16.1 | 47.7–48.3 | 30.0 | 47.7–48.3 | 48.04 |
| 120517801 | 112 | 644–651 | 16.1–16.4 | 48.3–49.2 | 30.0 | 48.3–49.2 | 48.75 |
| 120517801 | 113 | 652–659 | 16.4–16.6 | 49.2–49.8 | 30.0 | 49.2–49.8 | 49.50 |
| 122522485 | 106 | 1227–1238 | 15.9–16.1 | 47.7–48.3 | 30.0 | 47.7–48.3 | 48.05 |
| 159033763 | 111 | 2836–2861 | 2.0–2.1 | 6.0–6.3 | 6.0–6.3 | 30.0 | 30.00 |
| 160330868 | 107 | 187–188 | 11.7–11.9 | 35.1–35.7 | 30.0 | 35.1–35.7 | 35.40 |
| 160330868 | 109 | 191 | 12.5 | 37.5 | 30.0 | 37.5 | N/A: one prediction |
| 183374279 | 106 | 245–247 | 2.7–2.8 | 8.1–8.4 | 8.1–8.4 | 30.0 | 30.00 |
| 19119739 | 111 | 1286–1297 | 6.1–6.2 | 18.3–18.6 | 18.3–18.6 | 30.0 | 30.00 |
| 19119739 | 112 | 1298–1309 | 6.2–6.4 | 18.6–19.2 | 18.6–19.2 | 30.0 | 30.00 |
| 196514928 | 109 | 1177–1181 | 8.9–9.0 | 26.7–27.0 | 26.7–27.0 | 30.0 | 30.00 |
| 196514928 | 110 | 1182–1191 | 9.0–9.1 | 27.0–27.3 | 27.0–27.3 | 30.0 | 30.00 |
| 196514928 | 111 | 1192–1202 | 9.1–9.3 | 27.3–27.9 | 27.3–27.9 | 30.0 | 30.00 |
| 196514928 | 112 | 1203–1213 | 9.3–9.4 | 27.9–28.2 | 27.9–28.2 | 30.0 | 30.00 |
| 203381983 | 115 | 223–225 | 7.4–7.5 | 22.2–22.5 | 22.2–22.5 | 30.0 | 30.00 |
| 206620592 | 106 | 2000–2025 | 1.4 | 4.2 | 4.2 | 30.0 | 30.00 |
| 24526743 | 107 | 191–192 | 7.8–8.0 | 23.4–24.0 | 23.4–24.0 | 30.0 | 30.00 |
| 253931796 | 106 | 172–174 | 44.8–45.5 | 134.4–136.5 | 30.0 | 134.4–136.5 | 135.50 |
| 258006047 | 114 | 284–286 | 4.7–4.8 | 14.1–14.4 | 14.1–14.4 | 30.0 | 30.00 |
| 283913390 | 111 | 1160–1170 | 5.7–5.9 | 17.1–17.7 | 17.1–17.7 | 30.0 | 30.00 |
| 333661705 | 111 | 2023–2041 | 2.8–2.9 | 8.4–8.7 | 8.4–8.7 | 30.0 | 30.00 |
| 333661705 | 112 | 2042–2060 | 2.9 | 8.7 | 8.7 | 30.0 | 30.00 |
| 333661705 | 113 | 2061–2079 | 2.9–3.0 | 8.7–9.0 | 8.7–9.0 | 30.0 | 30.00 |
| 333661705 | 114 | 2080–2100 | 3.0 | 9.0 | 9.0 | 30.0 | 30.00 |
| 333735955 | 114 | 259–260 | 2.7 | 8.1 | 8.1 | 30.0 | 30.00 |
| 366047768 | 121 | 308–310 | 22.4–22.7 | 67.2–68.1 | 30.0 | 67.2–68.1 | 67.60 |
| 467959906 | 114 | 358–361 | 4.1–4.2 | 12.3–12.6 | 12.3–12.6 | 30.0 | 30.00 |
| 70441745 | 106 | 137–138 | 43.4 | 130.2 | 30.0 | 130.2 | 130.20 |
| 80387959 | 111 | 498–504 | 3.5–3.6 | 10.5–10.8 | 10.5–10.8 | 30.0 | 30.00 |
| 80387959 | 112 | 505–510 | 3.6 | 10.8 | 10.8 | 30.0 | 30.00 |
| 80387959 | 113 | 511–516 | 3.7 | 11.1 | 11.1 | 30.0 | 30.00 |
| 80387959 | 114 | 517–523 | 3.7–3.8 | 11.1–11.4 | 11.1–11.4 | 30.0 | 30.00 |
| 88407114 | 106 | 1894–1903 | 4.4 | 13.2 | 13.2 | 30.0 | 30.00 |
| 88407114 | 107 | 1904–1922 | 4.4–4.5 | 13.2–13.5 | 13.2–13.5 | 30.0 | 30.00 |

In particular, S106 is not limited to the two objects named in the clarification: TIC **70441745** already has σ = **43.4 min** (gate **30 versus 130.2 min**). TIC 122522485 has 15.9–16.1 min (47.7–48.3 min); TIC 253931796 has 44.8–45.5 min (134.4–136.5 min, code mean **135.50 min** if all three covered). The precise objects below 10 min also change, including 120444365 (6.3 → 30 min), 183374279 (8.1–8.4 → 30 min), and 206620592 (4.2 → 30 min). [I: respective CSVs]

### Ground/undated labels: do not mistake these ranges for verified TESS coverage

These are all remaining **prediction-labelled** rows in affected v2 CSVs. “none” is the CSV's ground-based label. “undated” lists candidate future sectors without assigning each epoch to a particular sector. The displayed ranges cover the listed frozen predictions; actual test-sector epochs cannot be identified from those labels alone. Applying `--sector N` to an “undated” label selects no rows in the frozen evaluator. TIC 61310956 v2 is superseded by its separate v3 ground test and is included here only to audit the historical affected wording. [I,L,C:24]

| TIC | CSV sector label | Epochs | σ (min) | 3σ (min) | min() (min) | max() (min) |
|---|---|---|---|---|---|---|
| 245503256 | undated (future sectors [124]) | 174–212 | 10.0–16.2 | 30.0–48.6 | 30.0 | 30.0–48.6 |
| 249813122 | undated (future sectors [122, 128, 129]) | 621–756 | 5.0–7.1 | 15.0–21.3 | 15.0–21.3 | 30.0 |
| 332709057 | none | 233–277 | 4.6–8.7 | 13.8–26.1 | 13.8–26.1 | 30.0 |
| 3367979 | none | 732–822 | 5.3–6.4 | 15.9–19.2 | 15.9–19.2 | 30.0 |
| 36694943 | undated (future sectors [134]) | 147–190 | 12.1–23.7 | 36.3–71.1 | 30.0 | 36.3–71.1 |
| 371421714 | none | 162–209 | 21.5–31.3 | 64.5–93.9 | 30.0 | 64.5–93.9 |
| 376225363 | undated (future sectors [122, 129]) | 690–853 | 62.2–86.7 | 186.6–260.1 | 30.0 | 186.6–260.1 |
| 383617106 | none | 285–344 | 6.1–8.8 | 18.3–26.4 | 18.3–26.4 | 30.0 |
| 50514263 | undated (future sectors [124]) | 174–212 | 19.7–31.9 | 59.1–95.7 | 30.0 | 59.1–95.7 |
| 61310956 | none | 147–181 | 20.3–25.7 | 60.9–77.1 | 30.0 | 60.9–77.1 |
| 65575657 | none | 489–598 | 11.4–20.2 | 34.2–60.6 | 30.0 | 34.2–60.6 |
| 91617711 | none | 122–158 | 83.3–124.7 | 249.9–374.1 | 30.0 | 249.9–374.1 |

### No eligible prediction rows

These three affected v2 files have zero `status.startswith('prediction')` rows, so no future timing-gate comparison can honestly be supplied from them. Their registrations actually print “Empty DataFrame” in the prediction section. All retained CSV rows are labelled “retrodiction: before freeze, untested”. [I,L]

| TIC / source (same v2 path convention) | Rows / epochs actually frozen | Last recorded UTC | Consequence |
|---|---|---|---|
| 162304222 | 399 / 4803–5201 | 2026-09-10 11:56 | Claimed test S111; no prediction-labelled rows. |
| 408110117 | 10 / 1099–1108 | 2026-10-03 11:53 | Rows carry S108, but every row is filtered out as retrodiction. |
| 53825235 | 399 / 3765–4163 | 2025-08-23 12:05 | Claimed test S108; prediction horizon stops far too early. |

This is a generation/selection defect, not evidence of insufficient observations. The generator uses `range(1,400)` from its reference epoch (`scripts/prereg_v2.py:102,112`), and assigns past epochs to retrodiction unless explicitly listed as unreleased (`:101,109,115`). Those mechanisms explain the short-period horizon problem and the need to audit unreleased-sector labels. The evaluator drops these rows at line 23 and returns INSUFFICIENT at line 44. Freeze a distinct corrected file/version rather than re-labelling old rows in place. [C,I]

## 5. Other outcome-rule/code mismatches

“Protocol” below means local PDF p. 2 and the same outcome clauses in the downloaded protocol archives. “Object text” means the Outcomes paragraph of affected v2 registrations, except where a different version is named explicitly. These defects must not be obscured by the narrow max/min repair. [P,L,C]

| Clause | What the evaluator actually does | Assessment / required action |
|---|---|---|
| Depth 0.5–1.5×; stacked SNR ≥ 5 | Lines 40,46,49 test the inclusive depth interval and SNR ≥ 5 using the mean flux loss at the **unshifted predicted phase**, not the shifted fitted box depth. | The threshold arithmetic agrees with the protocol. State exactly which depth is tested. V1 text uses 0.6–1.5× and is not interchangeable. Uncertainty is global MAD/√N, with no baseline/red-noise calibration; do not call SNR calibrated merely because arithmetic matches. |
| Duration 0.7–1.3× | Line 36 fits a box with fixed input duration; no duration is measured, returned, or compared anywhere. Line 49 has no duration condition. Same defect in the inconsistent scan. | Direct contradiction of protocol, object text and code docstring. Add a separately specified measurement/check in a new conformance evaluator, or explicitly admit the frozen classifier never tests it. |
| At least two transits | Lines 32–44 require two coverage-qualified windows, not two individually matching/detected dips. | Matches protocol’s “≥2 covered” count, but is weaker than the object wording “a box ... of ≥2 predicted times”. Clarify whether stack-only evidence is intended; do not claim the executable demonstrates two individual detections. |
| Timing and its aggregation | Lines 46–47 average best offsets with depth-error weights; sigmas are averaged arithmetically. Opposite offsets cancel. No per-transit timing requirement. | Protocol explicitly says stacked timing; original object wording reads per-event. Clarification must acknowledge this second distinction, not only max/min. A small signed mean does not establish that every event follows the ephemeris. |
| Fully covered for EXCLUDED | Line 50 uses the same ≥60% wide-window coverage plus ≥3 in-transit points as recovery; no separate full-coverage check. | The <0.3× at 3σ test itself is correctly `depth + 3*err < 0.3*ref`; the coverage prerequisite is not implemented. The synthetic central-gap exclusion below demonstrates the consequence. |
| INSUFFICIENT | Line 44 returns it for <2 windows passing the code’s coverage rule. | Count branch agrees, conditional on that definition. It can hide an empty/incorrect prediction selection; report n_predicted and distinguish input invalidity from genuinely missing observations. |
| INCONSISTENT: comparable dip within ±0.3 d, >30 min from **every** prediction | Only reached after EXCLUDED fails; line 56 retains just the deepest mean-flux box around each covered row; line 58 checks offset from that row, not distance to all predictions. No measured-duration criterion or explicit significance test. | Document precedence and implement the actual quantifier/comparability checks in a new procedure. A deepest non-comparable dip can hide another comparable dip. Per-object text also omits the protocol’s ±0.3-d bound. |
| Outcome priority | RECOVERED then EXCLUDED then INCONSISTENT/AMBIGUOUS (49–58). Protocol prose lists Recovered, Inconsistent, Excluded, Insufficient without explicitly resolving overlaps. | Clarification correctly identifies recovery first but omits exclusion’s precedence over displaced-dip detection. State full order. For 3σ>30 both recovered/inconsistent descriptions can apply; code picks RECOVERED. |
| Four stated outcomes | Line 58 returns a fifth, `AMBIGUOUS (stacked depth/timing outside the recovered band but not excluded)`. | Declare this residual category. It is preferable to forcing a false positive/negative, but is absent from the prose and introductory docstring. |
| Timing window versus search domain | Best offsets are confined to ±0.1 d = ±144 min (line 34), regardless of σ. | For tolerances ≥144 min, the timing gate cannot reject any offset returned by that grid. A quoted 3σ window wider than the search is not fully searched; relevant to the undated 376225363 and 91617711 records. State the limitation rather than presenting max() as a complete sigma-matched search. |
| Fixed product and reference values | Protocol says SPOC PDCSAP if available, otherwise QLP DET_FLUX. TIC 183374279’s existing addendum §2 instead specifies QLP SAP_FLUX, 1090 ppm, 2.84 h; protocol explicitly lists 970 ppm, 2.9 h. Code accepts arbitrary CLI depth/duration/column. | A blanket “protocol governs” can accidentally reverse this separate object-specific choice. State the hierarchy and freeze an object configuration. Evaluator itself cannot determine which conflicting reference is authoritative. |
| Ground exceptions | TIC 61310956 v3: each of ≥2 epochs at SNR ≥4, each within 3σ, precision/baseline requirements. TIC 89247735 v1: a single timed ground transit tests the ephemeris and location/colour conditions are specified. | The TESS evaluator does not implement these tests. Exempt them explicitly from “outcomes for every object ... exactly as it returns them”. Protocol’s generic ground language itself needs reconciliation with the object-specific record. |

### Executed counterexamples, not just source inspection

Inputs are 200-s cadence over BTJD 99–106, predicted centres 100 and 105, σ_pred = 2.1 min at each, reference depth 1000 ppm and duration 2 h. Noise is `np.random.default_rng(99106).normal(0,100e-6,len(t))`; inject the boxes described below into `1 + noise`. Except the gap case, sampling is continuous. Evaluator bytes and input files were not modified. The synthetic data are diagnostic only, not TESS observations. [T: input construction and rerun logs]

| Input | Measured output from unchanged evaluator | What it demonstrates |
|---|---|---|
| Control: two centred 2-h, 1000-ppm boxes | RECOVERED; depth 1010.48 ppm; SNR 83.98; mean offset 0.0 min. | Basic intended case passes. |
| Same boxes, both 20 min late | RECOVERED; mean offset 20.4 min; depth 843.82 ppm; SNR 70.03. | σ <10 min has practical impact: 20.4 passes max=30 but fails min=6.3. |
| Two centred boxes only 1.2 h long (0.6× reference) | RECOVERED; stacked depth 593.82 ppm; SNR 49.70. | Fails the required 0.7× minimum duration but code accepts. |
| Two 2-h, 1200-ppm boxes shifted −50/+50 min | RECOVERED; fitted offsets −49.2/+50.4 min, weighted mean +0.6 min; SNR 48.06. | Per-event large offsets cancel in the stacked gate. |
| No injected dips; delete central ±0.9 h at both centres | EXCLUDED; coverage 0.69 each; depth 4.94 ±40.71 ppm. | 90% of each nominal 2-h transit interval is unobserved, yet “fully covered” exclusion is returned. |
| One 1400-ppm box, no second box | AMBIGUOUS; depth 710.50 ppm; SNR 60.00; mean offset −37.8 min. | An actual fifth output category, not described by the four outcome clauses. |
| Two normal boxes shifted +200 min (inside ±0.3 d) | EXCLUDED; depth at predicted phase −211.95 ±11.97 ppm. | Exclusion precedence bypasses the displaced-dip scan. This is code behavior, not proof that the broad prose uniquely prescribes this label. |

Preserve the frozen evaluator and its outputs as an auditable historical artifact. The minimum acceptable repair is to publish its limitations and a completely specified, versioned conformance assessment before inspecting test data, including precedence, durations, coverage, reference values, timing aggregation and the residual category. Report disagreements between these procedures openly. Do not repair the implementation under the old hash or select whichever outcome looks better. These are reviewer recommendations based on the documented discrepancies, not evidence of misconduct. [C,T,P,L]

## 6. RNAAS assessment

**The max/min clarification does not require changing the numerical claims or wording of the local RNAAS note on this evidence.** I read all of `paper/rnaas/note.tex`: neither the abstract, “Nature and predictions” paragraph (line 33), nor the figure caption states a max/min tolerance, a 30-minute gate, or a RECOVERED/EXCLUDED classification of future data. The fourth-transit sentence explicitly calls it post hoc and “not a prediction of new data”. The prediction paragraph preserves TIC 89247735 **v1** as the test of record and distinguishes v5 refinements. The v1 registration `results/vet_qlp/89247735/PREREGISTRATION.md` has no disputed phrase and received no timing addendum. Its test describes one timed ground transit, approximate depth/duration, colour consistency and source location. [L: named source and registration]

However, the clarification's **“every object”** wording must not be used later to replace that original ground test with the generic two-transit TESS classifier. The protocol p. 2 says the same generic rules apply to TIC 89247735, creating a broader hierarchy issue that should be resolved explicitly in the clarification's scope. The note itself need not inherit that ambiguity if v1 remains its stated record. This is a limited assessment of timing-rule dependency, not a fresh certification of all astrophysical numbers or acceptance status. [P,L]

The submission identifier AAS82560 is recorded in `logs/DECISIONS.md:319`; I did not access the submission system or verify the actual submitted artifact. The local TEX's first comment still says “NOT submitted”, inconsistent with that log, but this comment is not manuscript prose. I can certify the content reviewed locally, not the editor's copy. [L]

## 7. Suggested exact replacement wording

The following is proposed text, **not an amendment made by this review**. It intentionally does not pretend that the missing implementation checks have been repaired.

> **Dated resolution of conflicting timing specifications — 2026-10-20**
>
> The original public protocol deposit (Zenodo 23462442, created 2026-10-19 01:36:22 UTC) and its archived evaluator specify a recovered timing tolerance of `max(3 sigma_pred, 30 min)`. In the executable, `sigma_pred` is the arithmetic mean of the frozen `sigma_min` values for coverage-qualified predictions, and the tested offset is the mean fitted offset weighted by inverse depth variance. The evaluator SHA-256 is `630815cc1400f0434dc9f30c8ce08cc42635ee5d1d429338c4010f6115043366`.
>
> The 37 v2 registrations listed in the accompanying inventory instead contain wording that can reasonably be read as `min(3 sigma_min, 30 min)` for individual events. TIC 80387959 and TIC 120444365's registrations were publicly archived before the protocol, so we do not claim that the protocol preceded all object files. The documents conflict. We resolve the TESS v2 timing-clause conflict in favour of the previously archived max() implementation before evaluating the test photometry, and will also report whether events satisfy the original narrower per-event reading. This is a dated clarification/adoption of precedence; it does not erase the earlier wording.
>
> The two timing gates differ whenever sigma is not exactly 10 minutes: max() widens the gate for both smaller and larger sigmas. The accompanying impact table gives the frozen values by object and epoch. These timing tolerances do not alone determine an outcome.
>
> The scope is the listed v2 TESS timing clauses. Older v1 rules, TIC 61310956's dedicated v3 ground rules, and TIC 89247735's v1 test of record are not replaced by this clarification. The three v1 files incorrectly given a 30-minute addendum actually have a 60-minute clause; those addenda require explicit correction. Separate object-specific extraction/reference-value amendments remain identified separately.
>
> Original prediction CSV bytes and their recorded digests are preserved. Dated notes are appended to original Markdown text; amended Markdown files necessarily have new file hashes. Historical releases and their manifests remain intact, and a new release will identify the amended copies.
>
> The frozen executable first checks coverage, then tests RECOVERED, EXCLUDED, and only then INCONSISTENT; otherwise it returns AMBIGUOUS. It does not measure or check duration and does not separately require full transit coverage for EXCLUDED. We will retain and report its literal output, but will not claim that output alone verifies every written outcome criterion. Any corrected conformance procedure and its precedence will be separately versioned and declared before test-data inspection.

The claim of pre-evaluation resolution in that proposed text is a commitment the authors must substantiate with dated public release and access history; the review cannot certify private non-access. Add direct links to the release, a list of affected records, and the exact conformance procedure when available. Replace “protocol rule verbatim” in the existing note with “the TESS template now uses max(), with the aggregation and exceptions specified here.” A grammatically correct future TESS sentence starts “at least two covered predicted transit windows; stacked depth ...; measured duration ...; stacked SNR ...; absolute weighted mean timing offset ...”, but must not claim a measured-duration check until one exists. [C,L; proposed editorial correction]

## 8. Limits and completion status

- Verified the public max() precedent, actual earlier ambiguous records, local/public inventory, all requested versioned CSV hashes, applicable old-byte comparisons, per-epoch impact, and evaluator defects by direct inspection/calculation/execution. No reliance on the clarification's self-description for these conclusions. [P,G,L,H,I,C,T]
- Full historical byte preservation is independently supported for the 22 appended files with public originals; only the retained clause and present file structure can be checked for the other 18. I did not find public copies of the 17 additional local v2 paths in the inspected repository history. [L,G]
- MAST availability checks support nonavailability of the checked QLP products, not a universal assertion about S106 data or the existence of results. No test-sector light curve was evaluated. [A]
- Prediction uncertainties were used exactly as frozen. I did not rederive the stellar parameters, timing covariance, clock corrections, sector footprints or ground observability; they are outside this clarification audit. The impact table concerns the recorded sigmas/labels, not their astrophysical calibration. [I]
- Temporary diagnostics are outside the repository. No manuscript, source script, prediction, public-release artifact or original review was edited, and nothing was published, uploaded, pushed or sent to another person. The only new repository artifact from this review is `results/REVIEW_timing_rule.md`.
