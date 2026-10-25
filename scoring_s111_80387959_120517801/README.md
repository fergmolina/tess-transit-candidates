# Scoring for the S111+ tests of TIC 80387959 and TIC 120517801 (locked 2026-10-25 15:14:04 UTC, before any S111 data exist)

## Tests (bold = primary sector, the test of record)
| TIC | Sectors | Reference depth / duration |
|---|---|---|
| 80387959 | **S111**, S112, S113, S114 | 726 ppm / 2.2 h |
| 120517801 | **S111**, S112, S113 | 830 ppm / 2.2 h |

Each sector has two configs: QLP (`<TIC>_S<N>.json`) and SPOC (`<TIC>_S<N>_spoc.json`). Exactly one is the product of record:
- **QLP config:** the published evaluator `prereg_conformance.py` v2.1 rc4, with its clock gate.
- **SPOC config:** `scripts/prereg_conformance_spoc.py`, which is v2.1 rc4 with a SPOC product branch and no QLP clock gate. The diff
  is `scripts/prereg_conformance_v2.1_to_spoc1.diff`.

The reference values follow the generator rule and are the same for both products. They are a fixed product-dependent comparison,
never rescaled.

## Product of record (the full text is in every config's `designation_rule`)
1. **Designation snapshot** (`scripts/target_list_designation.py`, metadata only):
   - It saves the official orbit table and the sector's 2-min target lists v1-v9. Versions above 9 are not discovered.
   - The DDT lists are saved as context only.
   - The sector end must be final: the table must also list the next sector.
   - Failed or malformed fetches give PENDING, never "unlisted".
2. **Operative designation:** the first complete snapshot after the sector end. The TIC listed means SPOC; otherwise QLP. Its
   cutoffs are frozen.
3. **SPOC designated:**
   - SPOC stays if any retained check finds a SPOC 2-min light curve whose MAST release date is <= end + 120 d.
   - Otherwise the QLP fallback is certified by two clean checks >= 7 d apart, and becomes final once QLP data are acquired.
   - Ambiguous or incomplete checks after the cutoff make the route UNRESOLVED.
4. **QLP:** the v01 light curve with release date <= end + 365 d. Without one, the sector is UNAVAILABLE (final). A v02-only listing
   is not a release of record.
5. **Ledger:** every snapshot, check, acquisition and disposition is an entry of a hash-chained, per-TIC/sector ledger
   (`scripts/s111_ledger.py`).
   - Appends are serialized, validated and atomically committed.
   - `scripts/validate_s111_inputs.py` replays the ledger.
   - No data of either product are acquired before the route is settled.
   - A QLP result needs both validators: `validate_s111_inputs.py` and the published `validate_round4_inputs.py`.

The primary sector is never replaced. Monitoring is prospective and periodic; earlier replaced deliveries cannot be excluded.

## Evidence
- **Tests:** `scripts/test_s111_lock.py` passes 209/209 and the published round-4 suite passes 182/182 on the QLP lock (`tests/`).
  All fixtures are artificial: mocked fetches, artificial MAST responses and artificial light curves.
- **Demo:** `demo/designation_S108_v2/` is a live metadata snapshot of S108 (TIC 317134140 -> SPOC, TIC 24526743 -> QLP).
- **Review chain:** `../reviews_s111/` (one review and three re-checks; the last says "publish as v1.19").
- **Earlier review:** the GAP3 review in `../reviews_317134140/` covered an earlier S111 draft. Every S111 draft before v1.19e was
  superseded and never published (DECISIONS 176-198).
