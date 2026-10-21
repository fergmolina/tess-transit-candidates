> **2026-10-21 — not yet published (for v1.15, after re-check). Handling decided by the author on 2026-10-21. No frozen file was changed.**

# Erratum: incomplete prediction lists from two generator bugs in scripts/prereg_v2.py

Found 2026-10-21 while freezing round 4 (DECISIONS 117, 119). The complete audit, by the independent review in results/REVIEW_round4_freezes.md
(section "Complete horizon audit", 42 registrations), was checked against the frozen files. All original files and hashes are kept unchanged.

## Two distinct bugs
1. **Epoch cap (before 2026-10-20 ~01:30 UTC, DECISIONS 68).** The generator listed at most 399 epochs after the reference epoch
   (`range(1, 400)`). For short periods or old reference epochs, the list stopped before, or partway through, the test sectors.
2. **Wrong end date (DECISIONS 69 to 2026-10-21).** The fix for bug 1 meant to list transits through 2027-12-31 but used JD 2461406.5,
   which is 2027-01-01. Fixed on 2026-10-21 to JD 2461771.5 (2028-01-01).

Twelve records made before DECISIONS 69 list predictions beyond 2027 (the old loop allowed JD 2461900). These are extra predictions, not
omissions, and are left as frozen.

## Affected records
| Record | Public? | Cause | What is missing |
|---|---|---|---|
| TIC 115692561 v2 (CSV d8fe193d) | yes; **S106 test** | epoch cap | S106 epochs 3418-3419 (BJD_TDB 2461260.88623, 2461261.73655) and all 34 S107 epochs 3420-3453. The S106 list ends at epoch 3417. |
| TIC 162304222 v2 | yes | epoch cap | every future prediction (S111-S114); superseded by v3 in v1.10 |
| TIC 162304222 v3 | yes | wrong end date | S112 after 2026-12-31 (33 rows), all of S113 (52) and S114 (55) |
| TIC 53825235 v2 | yes | epoch cap | every future prediction (S108: 47, S109: 46, S110: 43 rows); the v3 that DECISIONS 68 said was needed was never made |
| TIC 3367979 v2 | local (named in README) | epoch cap | ground predictions after 2027-08-28 (epochs 823-858) |

The other 37 registrations made by prereg_v2.py were checked: no dated-sector omission (review audit table).

## Handling (decided by the author, 2026-10-21)
- **115692561 S106:** the test of record stays the frozen list as published (epochs up to 3417; configs/conformance/115692561_S106.json,
  CSV d8fe193d). It will be scored and reported as such, with this omission stated next to the result. Epoch 3418 lies about 1.0 d before
  the end of the sector and might have been eligible; 3419 lies inside the 0.5-d end-of-data edge cut. No supplementary list is made, so
  S107 is not tested for this star.
- **162304222:** v4 frozen 2026-10-21 02:57:30 UTC (CSV SHA-256 b4a26083fd8ae387242157f69bf03013f34c1f149b5f65a6551592c17a2d70d8). The
  ephemeris is identical to v3 (T0, P and their errors reproduced exactly; the 68 shared rows are identical); it lists S111-S114 through
  2027. S111 is scored from v3 unchanged; S112-S114 from v4.
- **53825235:** v3 frozen 2026-10-21 02:57:37 UTC (CSV SHA-256 1408a7cda5e0d01a573ab9c36cb6159f05ebbc84bbc5bea3398ab16cecee4aab), same
  ephemeris as v2. S108 and S109 up to the freeze were already observed and are labelled retrodictions (not prospective); S109 after the
  freeze and S110 are predictions.
- **3367979:** v3 frozen 2026-10-21 02:57:42 UTC (CSV 0e8f5ea1...) was generated without --ground: its numerical predictions agree
  with v2 for all 399 shared epochs, but the sector labels changed ("undated (future sectors [])" instead of "none (ground-based)") and
  its text kept the TESS-sector clauses. v3 is superseded and is not a test of record. v4 frozen 2026-10-21 03:40:48 UTC (CSV SHA-256
  b6c94c8ee2a926a8a8663f8d4069ecc16d28b669f73804cae696da366fc36aef) is the ground registration: same ephemeris, all 399 rows shared with
  v2 identical in every field, list through 2027, required precision <= 0.6 mmag per 10-min bin (SNR 4 per transit at 788 ppm).
- The generated headers of 162304222 v4, 53825235 v3 and 3367979 v3 wrongly say "First freeze for this object" (and, for 162304222,
  "v4 supersedes v2"); dated corrections are appended to each. The template now writes a single introduction from the requested
  version and the records that exist (3367979 v4 is the first output of the fixed template).
