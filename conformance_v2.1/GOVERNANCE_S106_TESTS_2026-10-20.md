> Published 2026-10-20 with conformance-v2.1 (release v1.11), before any Sector 106 photometry of a test target was examined.
> Companion documents: CONFORMANCE_PROCEDURE_v2.1.md and ERRATUM_PROTOCOL_2026-10-20.md.

# Which document governs what: the seven Sector 106 tests

Applies to: TIC 183374279, 120444365, 70441745, 206620592, 122522485, 253931796 and 115692561. TIC 88407114's S106 test is withdrawn
(ERRATUM_S106). Nothing below changes a prediction CSV, an ephemeris or a checksum.

## Precedence, item by item
| Item | Governing source | Notes |
|---|---|---|
| Predicted epochs, mid-times, sigma_min | the hashed v2 prediction CSV of each registration | Overrides any number quoted in prose, including PREREG_PROTOCOL.tex (see the erratum below). |
| Outcome categories and their meaning | protocol "Outcome rules" and each registration's outcome clauses | Operationalised by the conformance procedure; every place where that procedure departs from the written wording is listed below. |
| Timing tolerance | CLARIFICATION_TIMING_RULE_2026-10-20.md: max(3 mean sigma_min, 30 min) | The min() reading and the per-event min() assessment promised there are reported as secondary readouts. |
| Light-curve product and column | the locked config: QLP SAP_FLUX | Departure, see below. |
| Reference depth and T14 | the registration's reference-values line; where none exists, the dated amendment (generator rule) | Overrides the protocol's numbers; see below. |
| Coverage, eligibility, edge rule, error model, outcome precedence | the conformance procedure (conformance-v2.1-rc4, scripts/prereg_conformance.py SHA-256 a864b07ace8d3220a2d94a60513a488c8a5d87b54f41ebf510ff40ef1755311f) | Departure from the protocol's 60 % "covered" rule; see below. |
| Outcome of record | the `outcome` field of scripts/prereg_conformance.py (locked SHA in each config), run on the release of record with a valid clock record | This field already includes the object-specific override (183374279). Nothing outside the evaluator adjusts it. The frozen scripts/prereg_test.py literal outputs are always reported next to it but are not the outcome of record. |
| Release of record | the first QLP release of the sector (file version v01), enforced by the evaluator | Later reprocessings are scored and reported separately as secondary results. If v01 is withdrawn from MAST before scoring, the test is deferred and a dated note is published before any replacement is examined. |
| Object-specific stricter clauses | stay in force; implemented in the evaluator | TIC 183374279 (addendum 2026-10-19, item 1): the config lists strict_epochs 245 and 246. Within tc +- T14/2 in clock-corrected time, any flagged cadence, non-finite flux, internal spacing greater than 1.5 median cadences, or first/last cadence more than 1.05 median cadences inside a window edge triggers the strict clause. Non-finite TIME rows are discarded and the resulting coverage gaps are tested. An absent or ineligible listed epoch also makes the final outcome INSUFFICIENT; the procedure's own result is kept as outcome_before_override. |

## Departures from the written protocol (PREREG_PROTOCOL.tex, Zenodo 10.5281/zenodo.23477866), each with its reason
1. **Product.** The protocol (tex:41-42) says "SPOC PDCSAP if 2-min data exist, otherwise QLP DET_FLUX". None of the seven targets is on
   the S106 2-min target list (catalogs/target_lists/all_targets_S106_v1.csv, SHA-256 dc8eb3f1...) or in the S106 SPOC light-curve
   manifest (catalogs/tesscurl_sector_106_lc.sh, 42daeac2...), so QLP is the product under the protocol's own rule. The column is
   **SAP_FLUX, not DET_FLUX**: every locked reference depth was measured on raw SAP flux, and the QLP sectors of every ephemeris were
   timed on SAP flux (some ephemerides also use SPOC 2-min sectors, PDCSAP); DET_FLUX is QLP's own detrended flux, whose filtering can
   distort transit depth and shape differently from the transit-masked biweight used here.
   No TESScut fallback (withdrawn 2026-10-20).
2. **Reference values.** The protocol (tex:43-44) gives TIC 120444365 750 ppm, 2.0 h and TIC 183374279 970 ppm, 2.9 h. The locked
   values are 855 ppm, 2.0 h (120444365: dated amendment, raw-SAP all-sector depth; competing readings in the record: 743-750 ppm
   v1/QLP, per-sector 668-923 ppm) and 1090 ppm, 2.84 h (183374279: from the registration's **post-freeze addendum of 2026-10-19**,
   not from the frozen text itself; raw-SAP all-sector). TIC 70441745 is locked at 1829 ppm (all-sector raw SAP; the single-sector
   S68 value is 1597 ppm). **T14 for 120444365 and 70441745:** the amendment rule reads "shape-fit T14 if available, else the BLS
   duration"; the shape fit exists but its output has no T14 field, so the BLS grid durations (2.0 h, 1.5 h) were used; the
   shape-implied T14s are 2.18 h and 1.97 h. 183374279 uses a shape-fit T14 (2.84 h) because its addendum states it. The
   registrations postdate or are more specific than the protocol table.
3. **Coverage.** The protocol counts a transit as covered if >= 60 % of the cadences within +-1.5 durations exist. The conformance
   procedure requires >= 90 % of the in-transit interval plus baselines on both sides, after removing edge cadences (item 76).
   Reason: partial transits and edge ramps produced false outcomes in the internal review. Effect: fewer eligible events, hence
   more INSUFFICIENT (forecast per test in the procedure).
4. **Timing statistic.** The protocol tests the stacked (weighted-mean) offset from per-event fits within +-0.1 d (tex:42), which lets
   opposite offsets cancel. The procedure instead maximises a joint SNR over a common offset within **+-0.3 d** and a duration of 0.5-2.0x,
   uses a **single gate** from the mean sigma_min of the eligible events, and adds an **epoch-parity veto** (the timing split), which
   is a partial safeguard only (it misses some non-alternating displacements; measured rates in the procedure).
5. **Duration.** The protocol requires duration 0.7-1.3 x reference; the frozen evaluator never measures it. The procedure requires
   SNR^2(band) >= SNR^2(any duration) - 4. This is a nominal score rule, not a calibrated likelihood or 2-sigma duration interval; at the
   operating signal-to-noise a 0.6 x or 1.5 x duration is often accepted (rates disclosed).
6. **Where the depth is measured.** The protocol's frozen implementation measures the stacked depth at the predicted times and the
   offset separately; the registrations say "a box of depth 0.5-1.5x ... within +-3 sigma_min of the predicted times". The two agree
   when the gate is narrower than about half a transit duration, but not for the wide-sigma tests: TIC 70441745 (gate 130 min, T14 90
   min) and TIC 253931796 (gate 136 min, T14 264 min). There a correctly timed-within-gate transit can miss the predicted instant. The
   conformance procedure follows the registration wording (depth of the fitted box, wherever it lies within the gate); the frozen
   evaluator's literal output, which may read EXCLUDED in that situation, is reported next to it.
7. **INCONSISTENT and EXCLUDED.** Operationalised with look-elsewhere and consistency requirements (see the procedure); stated there as
   departures where they narrow the written clauses.

## Erratum to PREREG_PROTOCOL.tex line 35
The protocol's text gives the first TESS prediction of TIC 120444365 as "epoch 559 at 2026-07-12 21:51 UTC (sigma 4.7 min)". The time
is the v2 value of record (geocentric UTC, v2_utcfix CSV), but **4.7 min is the superseded v1 sigma** (predicted_transits_2026_2027.csv,
SHA-256 64b5b026...). The v2 CSV of record (SHA-256 32b5e085...) gives **sigma 2.1 min** for every S106 epoch, consistent with the
protocol's own table row ("T0 BTJD 4218.97007 +- 2.1 min"). Effect: the min() timing gate for this test is 3 x 2.1 = 6.3 min, not
14.1 min; the max() gate of record is 30 min either way. The other two first-epoch entries on that line (TIC 80387959 epoch 498,
01:20 UTC, 3.5 min; TIC 183374279 epoch 245, 21:14 UTC, 2.7 min) were checked against their v2 CSVs and are correct.

## Which document governs the documents
- This governance statement defines the precedence between documents.
- The evaluator docstring defines the computation, including the overrides listed here.
- The procedure document summarises both, and must agree with them.
- The outcome of record is always the evaluator's `outcome` field. If a disagreement between the code and this statement is found after
  scoring, the code is not changed and the outcome is not re-labelled. The disagreement is reported next to the outcome, together
  with the outcome the statement's wording would have given. It is never resolved in a way that turns a non-RECOVERED outcome into
  RECOVERED.

## Superseded predictions on record
TIC 120444365 also has a v1 S106 prediction file (predicted_transits_2026_2027.csv, SHA-256 64b5b026...; epoch 559 at BTJD 4234.4135,
sigma 4.7 min). It is superseded by v2 (SHA-256 32b5e085...), which is the test of record; v1 is kept on record and is not scored.

## Changes from earlier commitments
- Precedence: the earlier addenda said the timing rule is "as implemented in the frozen evaluator"; the outcome of record is now the
  conformance procedure's, with the frozen evaluator's literal output reported alongside.
- The per-event min() assessment promised in CLARIFICATION_TIMING_RULE_2026-10-20.md is reported as a declared secondary readout
  (per_event_min_reading), next to the joint min() reading.
- The protocol's TESScut fixed-aperture cross-check is withdrawn for all seven tests (it was never specified as a procedure; the
  183374279 fallback was withdrawn on 2026-10-20 for the same reason).
- The frozen evaluator's command is locked in each config, in two variants (SAP_FLUX = same inputs; DET_FLUX = the protocol's column).

## Registrations amended (dated notes appended 2026-10-20; CSVs untouched)
All seven S106 registrations carry a dated note naming the conformance procedure (evaluator SHA-256), its precedence over the frozen
evaluator's literal output, the locked config and its SHA-256, product QLP SAP_FLUX, the edge rule, the release of record and this
governance statement. For 183374279, 120444365 and 70441745, an earlier 2026-10-20 amendment cited CONFORMANCE_PROCEDURE_2026-10-20.md
(conformance-v2.0, withdrawn before publication); that citation is superseded, while the reference values and the withdrawal of the
183374279 TESScut fallback stand.
