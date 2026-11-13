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
