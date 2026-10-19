# TIC 89247735: version-5 ephemeris (2026-10-19) — supersedes v4

- File: `predicted_transits_2026_2027_v5.csv`, SHA-256 `216e7a4c6a9863dbe7bbf0777e1638c083553b4eb146d2425a4ab0e1fd2153a5`, frozen 2026-10-19 19:57:20 UTC.
- Why: v4's +8.02-min Sector-104 correction wrongly treated TESScut `TIMECORR` as target-specific (it refers to an FFI reference position).
  v5 uses spacecraft time (TESScut `TIME − TIMECORR`), plus the target light-travel time from JPL Horizons TESS vectors, plus the QLP
  convention (+0.033 min): +7.533 min (`scripts/qlp_clock_v2.py`). Independent external check: +7.533125 min.
- S104 time BTJD 4196.80955 ± 4.2 min (photometric 1.44, clock 0.05 [adopted allowance], extraction 4.0 min).
- P = 18.323174 ± 0.000040 d, T0 = BTJD 4196.80991 ± 1.9 min (epoch 138); χ² = 0.37 for 2 degrees of freedom.
- Contacts are geocentric UTC with T14 = 4.536 h (from `fits/refit_v4_fixed_b1.json`, which was fitted with the earlier +8.02-min clock).
  Cerro Tololo "full" means target >30° and Sun <−12° at both contacts. Epoch 159 (2027-06-25 02:10 UTC) is the only full transit in the
  file; epoch 162 misses by 0.0025° of solar altitude.
- **Version 1 remains the test of record.** v5 differs from v1 by +4.3 to +5.5 min (1.25–1.38σ of v1) at epochs 146–163. v4 is superseded.
