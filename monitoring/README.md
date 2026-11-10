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
