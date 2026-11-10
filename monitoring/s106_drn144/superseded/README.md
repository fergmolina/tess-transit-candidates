# SUPERSEDED quick check (2026-11-10 (v1.19.1))

`s106_gap_check.py` and its output were a first quick check of the Sector 106 data gap (DECISIONS 208). **Do not use its counts.**
It counted an event as eligible when its duration fitted inside the kept intervals. The evaluator also requires baseline coverage on
both sides, and the published forecast models QLP's own gap patterns. The check was too optimistic for TIC 253931796 and
TIC 183374279. It is corrected by DECISIONS 209 and replaced by `../conformance_s106_forecast_drn144.py`.

The two files are kept byte-identical to the versions hashed in DECISIONS 208, for the record only.
