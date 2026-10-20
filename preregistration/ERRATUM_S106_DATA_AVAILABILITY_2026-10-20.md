# Erratum — availability of TESS Sector 106 (and 107) data at the freeze times (2026-10-20)

## What was wrong
Several records described Sector 106 as "observed, data not public at freeze", and three local records said the same of Sector 107. That was wrong. Public availability is product-specific.

- **SPOC 2-minute light curves:** files we retained for other targets show that we had S106 and S107 SPOC 2-minute light curves by 2026-10-17, about 16:45 UTC (12:45 EDT). That is before every freeze listed below. MAST's S106 SPOC download script carries an HTTP Last-Modified date of 2026-09-10, and the S107 script one of 2026-10-02.
- **Full-frame images:** S106 FFI products were also public. MAST's S106 FFI script carries a Last-Modified date of 2026-08-13, and MAST's TICA notice dates the recovery of missing S106 cadences, accessible through TESSCut, to 2026-08-14.
- **What we have not established:** the exact first release time of every S106/S107 SPOC or TESScut product.
- **What was genuinely unavailable:** target-specific QLP light curves for these stars were not on MAST when checked (HTTP 404 on 2026-10-20). Statements limited to QLP were correct; statements that the sector's data were not public were not.

## Affected records

| Object / version | Frozen (UTC) | Sector(s) | Public release containing it |
|---|---|---|---|
| TIC 120444365 v1 | 2026-10-18 20:26:00 | S106 | yes (also in the Zenodo preprint 10.5281/zenodo.23462433) |
| TIC 120444365 v2 | 2026-10-18 22:34:49 | S106 | yes |
| TIC 183374279 v2 | 2026-10-19 11:44:14 | S106 | yes |
| TIC 70441745 v2 | 2026-10-19 12:51:12 | S106 | yes |
| TIC 122522485 v2 | 2026-10-20 00:33:06 | S106 | not in the audited public releases (local) |
| TIC 206620592 v2 | 2026-10-20 00:33:10 | S106 | local |
| TIC 253931796 v2 | 2026-10-20 00:33:12 | S106 | local |
| TIC 115692561 v2 | 2026-10-20 00:44:10 | S106 | local |
| TIC 88407114 v2 | 2026-10-20 00:44:14 | S106, S107 | local; S106 test **withdrawn** (below) |
| TIC 160330868 v2 | 2026-10-20 00:43:17 | S107 | local |
| TIC 24526743 v2 | 2026-10-20 00:43:31 | S107 | local |

`ERRATUM_S106_MANIFEST.csv` lists every affected path, including registrations, prediction CSVs, outcome tables, README/REPORT passages, the preprint note, the protocol's purpose sentence and archived bundles, with each prediction file's unchanged SHA-256.

Frozen CSV status fields and original texts are not edited. Each current registration carries an appended, dated note that points here.

## What we attest, and what it does and does not prove
- **Our statement:** except for the withdrawn TIC 88407114 S106 test, we state that we did not inspect or use the affected target/sector photometry before each freeze.
- **What supports it:** the audited frozen fitted-sector lists contain no affected test sector, and no such target/sector file existed in our data directories before the freezes.
- **What it cannot prove:** the absence of a file does not independently prove that the data were never examined.
- **A later download, disclosed:** an internal reviewer downloaded a 1×1-pixel S106 cutout at TIC 206620592's position on 2026-10-20 at 01:21:13 UTC. That was after its 00:33:10 UTC freeze, and the reviewer reports not inspecting its flux.

## How the affected tests should be read
These are predictions registered **after the observations were acquired and while public image products existed**. They are not prospective predictions of observations unavailable to us or to the public.

Conditional on the attestation above, an unchanged prediction selection and no other use of those data, they remain a held-out check of the frozen ephemerides. That is weaker evidence than a prospective prediction, and every outcome will be reported with this caveat.

For the valid affected rows, read the original status as: "sector already observed; public data existed; authors attest target-sector photometry was not examined before freeze."

## Withdrawn test
TIC 88407114 v2 (frozen 2026-10-20 00:44:14 UTC) fitted S106 SPOC photometry: the freeze script downloaded every available 2-minute sector. S106 therefore cannot be an out-of-sample test for it, and that test is withdrawn. Its original files and hashes are retained and marked. No publication of that freeze was found in the audited public release history. Its S107 entry is subject to the same availability correction.

## Not affected
- **TIC 89247735:** its test of record is ground-based, with predictions covering 2026–2027. Its fourth TESS event remains a post hoc recovery from existing data, as already stated.
- **TIC 80387959:** its prospective S111 test begins with observations scheduled from 2026-11-26.
- **Hashes:** no prediction CSV bytes or recorded digests change; amended explanatory documents get new hashes.

## Process correction
On 2026-10-20 the freeze script `scripts/prereg_v2.py` was changed so that declared test sectors, every future sector of the target, and any sector ≥ 106 are excluded **before** any file is opened or downloaded, for both QLP and SPOC products. A dry run on a temporary copy confirmed that the cached S106 file of TIC 88407114 is no longer read.

The script still does not query product availability. Its status label now says that availability was not checked, and it records the authors' non-examination as an attestation rather than a fact. No new freeze will be made until each test sector's public availability has been recorded by hand in the freeze description.
