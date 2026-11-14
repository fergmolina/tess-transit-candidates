# EXPLORATORY, POST-OUTCOME: Sector 108 of TIC 317134140. PARTIAL UNCHANGED.

Published 2026-11-14 (v1.21). This folder is **not a test result**. The Sector 108 outcome of record is PARTIAL
(`../../results/S108/RESULT_S108.md`, v1.20) and nothing here changes it. No lock, config, scorer or prediction file changed.

After v1.20 was published, the author looked at the same Sector 108 light curve again, and at the Sector 108 target-pixel file,
to answer three questions: why 20 of the 48 predicted events were not eligible, what the 1.1467-d BLS peak is, and whether the dip
shows any sign of coming from another star. The plan was written after the outcome was known. It is an author-reported advance
plan for a post-outcome exploration, not an independently timed blind test.

## Read in this order
1. `CORRECTIONS_AND_COMPLETION_2026-11-14.md`: the current statement. It corrects the report after external review.
2. `REPORT.md`: the report as first written, kept byte for byte, with a dated status note appended. Several of its statements
   are withdrawn or qualified by the corrections note.
3. `PLAN.md`: the plan (SHA-256 `07c490b3e9a69399...`).
4. Review: `../../../reviews_v1_21/REVIEW_exploratory_S108.md` and its prompt.

## What it found, in short
- **Ineligible events.** Of 48 predicted events, 20 fail the locked eligibility rules. The dominant removal stages within ±3 h are nonfinite corrected flux or uncertainty (12), absent finite-time rows (3), edge trimming (3) and the TOI mask (2). Seventeen have no retained cadences in the ±0.75-h transit window; fifteen have none throughout ±3 h. These are consequences of both data availability and the fixed processing rules.
- **Blind search.** At the candidate period the SDE is about 4.7 to 5.2. The candidate-period grid summaries are below the three selected BLS peaks; these diagnostics do not establish that gaps caused the rank. The leading peak is 0.264% above 2P and overlaps odd-epoch phases for part of the baseline, but its origin and association with the candidate remain unresolved.
- **Odd and even events.** 250 ppm and 167 ppm; the difference is 83 ppm. An approximate spread of 90 ppm neglects
  covariance and is not a calibrated error. No compelling parity contrast is established by this exploratory diagnostic.
- **Position.** Centroid shift 0.10 mpx; flux-loss centroid 0.56 px from the target. The position diagnostics do not localize the signal securely or exclude nearby blended sources.

## Files
| File | Content |
|---|---|
| `report.json`, `quality_addendum.json` | saved numbers |
| `fold_S108.png`, `pixelmap_S108.png` | figures; captions are in the corrections note (F10) |
| `run.log` | output of the run (the download message of the target-pixel file) |
| `scripts_as_run/` | the two scripts as run, unmodified. They contain the author's absolute workspace paths and import the locked scorer; they are a record, not a portable tool |
| `SHA256.txt` | hashes recorded on 2026-11-13, with workspace-relative paths. The `REPORT.md` entry is the hash of the original bytes, which are the prefix of the copy here |

## Limits
- **Data.** The light curve of record (SHA-256 `cea2619b6228e770064ed39176ad446c02320311dbd3751e15cdc0876b4331a0`) and the target-pixel file
  `tess2026250081459-s0108-0000000317134140-0310-s_tp.fits` (48,268,800 bytes, SHA-256 `fd96a0c06789a69346b573613e292d708f09bc6a25454406f14dc931f5d3b455`) are public
  at MAST and are not copied here. No Sector 109 or 110 data of this star have been downloaded or opened; that is the author's
  attestation.
- **Conduct (author-reported).** One run of the main script and one of the quality-flag script, after the plan was written. File
  times are consistent with that account; they cannot prove it or exclude earlier unrecorded inspection.
- **Review.** The review read sources, saved outputs and figures and checked hashes. It did not open the photometry or run the
  scripts. It is not an independent computational reproduction; none has been made or decided.
- **Not done.** A paired-shift null for the odd/even difference; a test of whether the changed trim order matters; the full
  periodogram arrays were not saved.
- **Remaining test.** Sectors 109 and 110 are scored separately by the locked procedure, each published whatever the outcome,
  never pooled. Knowing Sector 108 can influence interpretation, so any further exploration stays separate and labelled.

Log entries: DECISIONS 232-236.
