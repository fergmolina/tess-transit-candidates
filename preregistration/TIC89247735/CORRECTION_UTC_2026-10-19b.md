# Second UTC correction — TIC 89247735 prediction files (2026-10-19)

Found by the round-3 external review (results/referee_89247735/REFEREE_REPORT_round3_external.md, issue 6).

The first correction (`*_utcfix.csv`, CORRECTION_UTC_2026-10-19.md) added a geocentric mid-time column `utc_geocentric` but left
`ingress_utc` and `egress_utc` as the old time-scale-only conversion, so those contact times were late or early by the same
barycentric light-travel time as the old mid-time (up to ±8 min; +7.9 min for the 2027 June/August transits).

`*_utcfix2.csv` (scripts/prereg_utc_fix2.py) shifts both contact columns by the same light-travel time as the mid-time. Example, epoch 159:
mid 2027-06-25 02:09 UTC, contacts 00:09–04:09 UTC (previously listed 00:17–04:17).

Unchanged: the frozen CSVs and their SHA-256, all BJD_TDB values, and the first `*_utcfix.csv` files (kept for traceability).
Only TIC 89247735 is affected; the other objects' correction files have no contact columns, or label them `tdb_scale_only`.

New: version 4 (`predicted_transits_2026_2027_v4.csv`, SHA-256 4f6aba63…, frozen 2026-10-19 19:19:21 UTC) uses the Sector-104
time corrected for the QLP S99–S104 barycentric clock error (+8.02 min; scripts/s104_clock_89247735.py) and gives geocentric UTC
mid-times and contacts plus Cerro Tololo altitudes. Version 1 remains the test of record; v4 differs from it by +4.4 to +5.6 min
at the 2026–2027 epochs (about 1.3 × v1's own 1σ).
