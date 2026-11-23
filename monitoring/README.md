# Monitoring records between releases (2026-11-10 (v1.19.1))

Records made while waiting for test data. All are metadata or mission documents. **No test-sector photometry of any frozen star has
been downloaded, opened or analysed.** Nothing here changes a lock, a config, an evaluator, a registration or a prediction file.
The log entries are DECISIONS 201-210.

- `s106_drn144/`: what the Sector 106 data release notes (DRN 144) report, and an updated forecast of how many predicted events can
  be scored in the seven Sector 106 tests. Start with `NOTE_S106_DRN144_2026-11-10.md`. The forecast is descriptive; the locked
  evaluator and the QLP file decide.
- `selection_records_317134140/`: the weekly metadata-only checks for a SPOC 2-minute light curve of TIC 317134140 in Sectors 108 and
  109, required by the v1.18 lock (`../scoring_317134140_s108_s110/README.md`). Each record is the unedited output of
  `spoc_selection.py select`. All five say `NONE`: no such product was listed at MAST at the query time (2026-10-25, 2026-11-01 and
  2026-11-08 UTC). The checks continue weekly; those for Sector 110 start on 2026-11-26.
- `orbit_table/TESS_orbit_times_lastmod_2026-11-07.csv`: the mission's orbit table as served on 2026-11-08 (Last-Modified
  2026-11-07 05:12:12 GMT). It is the first copy seen that lists Sector 112. Under the v1.19 rule this publishes the end of
  Sector 111, 2026-12-22 08:30 UTC. The first designation snapshot for TIC 80387959 and TIC 120517801 counts only if taken at or
  after that time (DECISIONS 206). Nothing is designated yet.

Also recorded in the log: the Sector 111 2-minute target list includes TIC 80387959 and not TIC 120517801 (DECISIONS 201-203; this
does not yet designate anything), and the author's 2026-11-01 follow-up to the DDT office (DECISIONS 205).

---

## Corrections and new records, 2026-11-10 (v1.19.2)

An independent review of v1.19.1 (`../reviews_v1_19_1/REVIEW_v1_19_1.md`) found two statements above that need correcting. The text
above is kept as published. All corrections are in `../corrections/CORRECTION_v1.19.1_2026-11-10.md`. The wording in quotation
blocks is the reviewer's.

**The checks were not all weekly (C1).** This corrects "the weekly metadata-only checks" above.

> The S108 monitoring schedule was not fully met. The checks at 2026-10-25T00:04:12.835692Z and 2026-11-01T22:32:01.307139Z were
> 7 days 22:27:48.471447 apart, exceeding the locked seven-day interval by 22:27:48.471447. Both retained records are NONE. This
> does not establish continuous unavailability or exclude an intervening replaced delivery. The original records, selection rule and
> cutoff remain unchanged. Subsequent checks will be scheduled no more than seven days apart, with the locked final check retained.

**Scope of the photometry statement (C2).** This replaces "No test-sector photometry of any frozen star has been downloaded, opened
or analysed" above.

> The work reported in v1.19.1 used mission documents, metadata and previously examined in-sample QLP files; it did not acquire or
> examine test-sector photometry. This statement does not supersede the earlier S106 data-availability erratum, including its
> disclosure of a downloaded, reportedly unopened TIC 206620592 S106 cutout. The log records QLP s0106 directory checks returning 404
> on November 8 and November 9; no publication-time check was retained. These checks do not establish the first availability time of
> every QLP light curve. The authors' non-examination statement remains an attestation.

**New records.**
- `selection_records_317134140/S108/sel_20261110T040457Z.json` and `selection_records_317134140/S109/sel_20261110T040457Z.json`: checks made at
  2026-11-10 04:04:57 and 04:04:58 UTC. Both say `NONE`. The next check is due no later than 2026-11-17 04:04 UTC.
- `qlp_s0106_checks/head_20261110T040457Z.txt`: status line and date of a header request to the QLP Sector 106 directory at MAST (HTTP 404 at
  2026-11-10 04:04:59 GMT). It is a status request; no data product was requested.
- Checks for Sector 110 start at 2026-11-26 04:15 UTC, the sector end in the lock.

Log entries: DECISIONS 211-216.


---

## New records, 2026-11-13 (v1.20)

- `selection_records_317134140/S108/sel_20261112T045349Z.json` and `S109/sel_20261112T045349Z.json`: checks at 2026-11-12 04:53:49
  and 04:53:50 UTC. Both say `NONE`.
- `selection_records_317134140/S108/sel_20261113T195427Z.json`: check at 2026-11-13 19:54:28 UTC. It says `SELECTED`, with exactly
  one candidate. This is the first `SELECTED` record for Sector 108 and it ends the Sector 108 checks. It was made after a daily
  metadata monitor reported that the Sector 108 light-curve manifest had appeared. The result is in
  `../scoring_317134140_s108_s110/results/S108/`.
- `selection_records_317134140/S109/sel_20261113T195427Z.json`: check at 2026-11-13 19:54:46 UTC. It says `NONE`. The next Sector 109
  check is due no later than 2026-11-20 19:54 UTC.
- `orbit_table/TESS_orbit_times_lastmod_2026-11-11.csv`: the mission's orbit table as re-issued on 2026-11-11. Compared with the
  2026-11-07 copy only the comment line "# Created ..." changed; every data row is identical.
- Intervals between consecutive checks since the last note: Sector 108, 2 d 0 h 49 min and 1 d 15 h 1 min; Sector 109, 2 d 0 h 49 min
  and 1 d 15 h 1 min. All are under seven days.

Log entries: DECISIONS 217-229.


---

## New records, 2026-11-23 (v1.22)

The work reported here used mission documents, metadata and previously examined in-sample QLP files. It did not acquire or examine
test-sector photometry of the Sector 107 stars. This statement is limited to that work; it does not supersede the Sector 106
data-availability erratum of 2026-10-20, and the authors' non-examination statement remains an attestation. (The Sector 108 light curve
of TIC 317134140, already scored in v1.20, was re-executed; see `../scoring_317134140_s108_s110/reproduction/S108/`.)

- `s107_drn145/`: an eligibility forecast for the Sector 107 tests of TIC 24526743 and TIC 160330868, from the segment times of the
  Sector 107 data release notes (DRN 145). Start with `NOTE_S107_FORECAST_2026-11-19.md`. Result: TIC 160330868 has no eligible
  event in any case, which agrees with the advance statement published with its lock (expected INSUFFICIENT). TIC 24526743 has two
  eligible events with the release-note segments alone and in four of seven past gap patterns, and one in the other three; that
  "2 of 2" is a fragile conditional scenario, not an established expectation. The forecast is descriptive: the locked evaluator and
  the QLP file decide. The note names the script as `scripts/conformance_s107_forecast_drn145.py`; it is in this folder.
  `NOTE_S107_FORECAST_2026-11-19_as_checked_by_auditor.md` is the version the auditor checked, before the wording corrections it
  asked for. The auditor's check is in `../scoring_317134140_s108_s110/reproduction/S108/REPRODUCTION_S108_auditor.md`.
- `qlp_s0107_checks/head_20261123T134940Z.txt`: status line and date of a header request to the QLP Sector 107 directory at MAST
  (HTTP 404 at 2026-11-23 13:49:40 GMT), made when this release was assembled. It is a status request; no data product was
  requested. It does not establish the first availability time of every QLP light curve.
- `selection_records_317134140/S109/sel_20261114T150448Z.json`, `sel_20261119T151140Z.json` and `sel_20261123T134156Z.json`: checks at
  2026-11-14 15:04:48, 2026-11-19 15:11:40 and 2026-11-23 13:41:56 UTC. All say `NONE`. Intervals between consecutive Sector 109
  checks since the last note: 0 d 19 h 10 min, 5 d 0 h 6 min and 3 d 22 h 30 min; all are under seven days. The next check is due no later
  than 2026-11-30 13:41 UTC. Checks for Sector 110 start at 2026-11-26 04:15 UTC.
- `orbit_table/TESS_orbit_times_lastmod_2026-11-16.csv` and `TESS_orbit_times_fetched_20261123T134155Z.csv`: the mission's orbit table
  as served on 2026-11-16 and 2026-11-23. Each adds one Sector 112 row to the copy before it. The end of Sector 111 is unchanged
  (2026-12-22 08:30 UTC). The end of Sector 112 is not final.
- `ddt/DDT104_CTL_09.01_fetched_20261119T151139Z.csv`: the target list of TESS DDT 104 as served by the mission on 2026-11-19. Its
  single target is TIC 80387959, at 2-minute cadence. Under the v1.19 rule DDT lists never decide the product of record for
  Sectors 111 to 114; only the per-sector 2-minute target lists do (`../scoring_s111_80387959_120517801/`).

Log entries: DECISIONS 237-260.
