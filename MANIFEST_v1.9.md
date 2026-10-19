# Manifest — release v1.9 (2026-10-19): corrections only

| File | Role | Status |
|---|---|---|
| preregistration/TIC89247735/predicted_transits_2026_2027.csv (v1) | Test of record for TIC 89247735 | **Current test of record** (unchanged, SHA af83f110…) |
| preregistration/TIC89247735/predicted_transits_2026_2027_v5.csv + final_ephemeris_v5.json + PREREGISTRATION_v5.md | Refined ephemeris, S104 clock +7.533 min | **Current refinement** (SHA 216e7a4c…) |
| …_v4.csv / final_ephemeris_v4.json / PREREGISTRATION_v4.md (v1.8) | +8.02-min clock (mis-derived) | **Superseded by v5** |
| …_v2.csv, …_v3.csv | Earlier S104 treatments | Superseded |
| …_utcfix2.csv + CORRECTION_UTC_2026-10-19b.md | Geocentric contacts for v1–v3 | Current |
| …_utcfix.csv + preregistration/CORRECTION_UTC_2026-10-19.md | First UTC fix (contacts not corrected) | Superseded by utcfix2 |
| preregistration/TIC89247735/fits/refit_v4_{fixed_b1,prior_b1,fixed_b2}.json | Shape fit and sensitivity runs, fitted with the earlier +8.02-min S104 clock | Current shape (Table 2); not a v5 posterior |
| preregistration/TIC89247735/fits/refit_raw_sap.json | Shape fit before any clock correction | Historical |
| preregistration/ADDENDUM_QLP_CLOCK_2026-10-19b.md + qlp_clock_v2/*.json + qlp_clock_v2/shifts.csv | QLP clock corrections (method 2) and prediction shifts for all frozen objects | **Current** |
| preregistration/ADDENDUM_QLP_CLOCK_2026-10-19.md + qlp_clock_check/*.json (v1.8) | Method 1 (TESScut TIMECORR wrongly treated as target-specific) | **Superseded by revision b** |
| scripts/qlp_clock_v2.py, qlp_clock_v2_shifts.py, final_ephemeris_89247735_v5.py | Code for the current products | Current |
| scripts/qlp_clock_check.py, s104_clock_89247735.py, final_ephemeris_89247735_v4.py | Code for method 1 / v4 | Superseded |
| scripts/refit_89247735_v4.py | Code for the fits above | Current |
| referee_89247735/REFEREE_REPORT_round{3,4,5}_external.md, RESPONSE_round{3,4,5}_external.md | External reviews (Codex) and responses; round 4 response carries a dated correction | Record |

Inputs not redistributed: QLP and TESScut FITS files (public at MAST; file names in the scripts) and JPL Horizons vectors (queried live).
The withheld object's clock result is computed but not published.
