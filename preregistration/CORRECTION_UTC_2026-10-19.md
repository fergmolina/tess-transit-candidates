# Correction to the UTC columns of all frozen prediction files (2026-10-19)

**What was wrong.** In every `predicted_transits_*.csv` and `PREREGISTRATION*.md` published before 2026-10-19, the `utc` (or `tc_UTC`)
column was computed as `Time(BJD_TDB, scale='tdb').utc`, which only changes the time scale (TDB to UTC, about 69 s) and does **not**
remove the barycentric light-travel time toward the target. The geocentric arrival time of a transit differs from that value by up to
±8 min depending on the date (the Rømer delay). This was found by an adversarial referee review of the TIC 89247735 manuscript.

**What is unaffected.** The primary quantities, `tc_bjd_tdb` and `tc_btjd`, are correct and unchanged, as are every SHA-256 checksum and
freeze time. All TESS-based tests compare predictions with TESS timestamps in BTJD, so the Sector 106, 108–111 tests are unaffected.
Only an observer planning a ground-based observation from the clock-time column would have been early or late by the amounts below.

**What changes.** Each affected directory now also contains `<name>_utcfix.csv`: same rows, `tc_bjd_tdb` unchanged, the old column
renamed `utc_tdb_scale_only`, a new `utc_geocentric` column (BJD_TDB minus the light-travel time, computed with astropy for the
geocentre; `scripts/prereg_utc_fix.py`), and `ltt_min`. The original frozen files are kept byte-for-byte. From this date the
pre-registration tools write geocentric UTC directly.

| object | epoch | old clock time (UTC) | corrected geocentric UTC | shift |
|---|---|---|---|---|
| TIC 89247735 | 146 | 2026-10-29 21:27 | 2026-10-29 21:31 | +4 min |
| TIC 89247735 | 159 (first full ground transit, Chile) | 2027-06-25 02:17 | 2027-06-25 02:09 | −8 min |
| TIC 89247735 | 162 | 2027-08-19 01:33 | 2027-08-19 01:28 | −5 min |
| TIC 80387959 | 498 (first Sector-111 transit) | 2026-11-27 01:16 | 2026-11-27 01:20 | +4 min |
| TIC 120444365 | 559 (first Sector-106 transit) | 2026-07-12 21:55 | 2026-07-12 21:51 | −4 min |
| TIC 317134140 | 4936 (first Sector-108 transit) | 2026-09-07 21:31 | 2026-09-07 21:31 | −1 min |

Range of the shift over each file: TIC 89247735 −7.5 to +7.9 min; TIC 80387959 −5.4 to +5.5; TIC 120444365 −6.5 to +6.6; TIC 317134140 −1.2 to +5.7.
