# Corrections to release v1.19.1 (2026-11-10, published in v1.19.2)

Release v1.19.1 was published without external review. An independent review made afterwards
(`reviews_v1_19_1/REVIEW_v1_19_1.md`; paths here are relative to the repository root) found the points below. The eligibility forecast itself was reproduced and stands. No lock,
config, evaluator, registration or prediction file is affected. v1.19.1, its tag, archive, manifest and files are preserved; the
corrections are dated additions, and the wording in quotation blocks is the reviewer's.

## C1. The Sector 108 monitoring schedule was not fully met

> The S108 monitoring schedule was not fully met. The checks at 2026-10-25T00:04:12.835692Z and 2026-11-01T22:32:01.307139Z were
> 7 days 22:27:48.471447 apart, exceeding the locked seven-day interval by 22:27:48.471447. Both retained records are NONE. This
> does not establish continuous unavailability or exclude an intervening replaced delivery. The original records, selection rule and
> cutoff remain unchanged. Subsequent checks will be scheduled no more than seven days apart, with the locked final check retained.

v1.19.1 called the checks "weekly" without this exception (`monitoring/README.md`, release notes). No retrospective check was
created. Further checks were made on 2026-11-10 at 04:04:57 UTC (S108) and 04:04:58 UTC (S109); both are NONE and are included in
`monitoring/selection_records_317134140/`. Checks for Sector 110 start at 2026-11-26 04:15 UTC, the sector end in the lock.

## C2. Scope of the "no test-sector photometry" and "no QLP Sector 106 light curve existed" statements

> The work reported in v1.19.1 used mission documents, metadata and previously examined in-sample QLP files; it did not acquire or
> examine test-sector photometry. This statement does not supersede the earlier S106 data-availability erratum, including its
> disclosure of a downloaded, reportedly unopened TIC 206620592 S106 cutout. The log records QLP s0106 directory checks returning 404
> on November 8 and November 9; no publication-time check was retained. These checks do not establish the first availability time of
> every QLP light curve. The authors' non-examination statement remains an attestation.

The erratum is `preregistration/ERRATUM_S106_DATA_AVAILABILITY_2026-10-20.md`. This replaces the unscoped wording in
`monitoring/README.md`, the Sector 106 note, the README block and the release notes of v1.19.1 ("no test-sector photometry of any
frozen star has been downloaded, opened or analysed"; "written before any QLP Sector 106 light curve exists"; "last checked on
2026-11-08"). After publication, the same directory returned 404 to the reviewer at 2026-11-10 03:55:09 GMT and to the author's side
at 2026-11-10 04:04:59 GMT.

For the README block of v1.19.1, which called the forecast descriptive without the controlling rule:

> These are conditional forecast counts, not scores or changes to eligibility. The locked evaluator, its required clock record, and
> the selected QLP v01 file determine the outcome of record. No test or event is discarded or replaced on the basis of this forecast.

The README block and release notes also said that TIC 120444365 "loses one event". In full: its epoch 563 was eligible in four of
the seven templates before the gap and is eligible in none with it; the other three templates are unchanged.

## C3. Time stamps of log items 209 to 211

> Items 209 and 210 in v1.19.1 carry estimated, erroneous timestamps of 02:50 and 02:40 UTC. Item 210 had already corrected item 209
> to approximately 02:25. The forecast output mtimes are 02:24:41 UTC and the assembled public log mtime is 02:29:18 UTC. These
> support approximate reconstruction, not exact entry-writing times. Local item 211's 02:55 timestamp is also erroneous; the manifest
> was assembled at approximately 02:29:18 UTC. The containing commit is dated 02:38:49 UTC; GitHub records release publication at
> 02:38:53 UTC and Zenodo records creation at 02:38:58.133488 UTC on 2026-11-10. The public release anchors establish the existence
> of the released bytes. Original entries are preserved; no earlier public timestamp is claimed.

The stamps were typed from an estimate instead of the system clock. Since item 212 every stamp is read from the clock. Item 212's
phrase "true times from file times" is to be read with the limits above, and its "tag and GitHub release (02:38:53Z)" as: tag
created 02:38:49 UTC, GitHub release published 02:38:53 UTC.

## C4. "All 49 rows reproduce" and the joint signal-to-noise values

> For all 49 case-(a) rows, the predicted-event counts, eligible-event counts and eligible-epoch lists reproduce the published
> forecast; per-event SNR values are copied. The script's original assertion checks eligible-event counts only. Joint SNR is
> recalculated as the published rounded per-event SNR times the square root of the eligible count, rounded to two decimals.
> Consequently 19 case-(a) joint SNR entries differ from the earlier forecast by 0.01. No eligibility result changes.

This corrects the Sector 106 note ("All 49 rows reproduce the published forecast"; "per-event and joint signal-to-noise values ...
are carried over") and the matching sentence of DECISIONS 209. The published CSV is not replaced.

## C5. The name redaction in the public log, and the scope of the path scan

> In the public copy of item 205, the two private-email recipient names are replaced by “the two contacts named on the mission's DDT
> page.” This is a role redaction only; the reported action and date are unchanged. The v1.19 log remains a byte prefix. Previously
> published temporary paths in the historical prefix remain as disclosed in item 163; no new temporary or session path was introduced
> by this release. The forecast retains the existing absolute workspace-path convention.

Item 211's statement that no temporary path is in any changed file applies to the text added after the historical prefix, not to
the whole log file.

## C6. Release-note context missing from the Sector 106 note, and the limits of the forecast

> DRN 144 also warns of spurious transit detections from ACS systematics and many likely false-positive two-transit SPOC detections
> at periods of 8–20 days. Its Appendix A includes Manual Exclude among FFI flags; this does not establish how QLP will propagate
> those flags. Scattered light and calibration effects may further affect usable data. None of these warnings is a new rejection
> rule. The forecast uses ideal 200-second cadences and the evaluator's edge/coverage functions, not its full product preprocessing,
> clock correction or strict flag veto. Template fractions are scenarios, not outcome probabilities. Case (c) is an optimistic
> segment-only scenario under the stated timing approximation, not a guaranteed bound or score.

For TIC 183374279:

> Both strict epochs, 245 and 246, must be eligible **and** pass the locked nominal-window gap/flag check. `strict_all_eligible`
> tests only membership in the forecast eligible set; True is not a prediction that the strict veto will pass.

The reviewer's sensitivity check: shifting the synthetic times by 8 minutes either way changes one marginal event of
TIC 115692561 in two rows and no fewer-than-two result. "The DRN reports no timing issue" does not mean the QLP clock is verified;
the locked clock gate still applies.

## C7. The superseded quick check's hashes

> The quick-check files are retained byte-identical to their local source copies. Their SHA-256 digests are recorded in
> MANIFEST_v1.19.1.md; item 208 identifies the files and the superseded calculation but does not give their digests.

This corrects `monitoring/s106_drn144/superseded/README.md`, which said the files were "hashed in DECISIONS 208".

## Other points from the review, for the record

- The DDT addendum in v1.19.1 says the 2026-10-21 correction "was delivered on 2026-11-01". That is the author's report of sending
  it; no mail header or delivery receipt is retained or was examined.
- `CITATION.cff` carries the concept DOI (10.5281/zenodo.23443244), which resolves to the latest version. For exact reproduction
  cite the version DOI; v1.19.1 is 10.5281/zenodo.24096235.
- The review's own limits: it verified the retained records and published bytes. It cannot prove that no test-sector photometry was
  ever examined, or replay the historical archive queries.
