# All-sky round 4 tables (2026-10-20/21)

| File | Content |
|---|---|
| allsky_round4_primary.csv | the 182 primary signals (next TESS sector S112-S120); pool rule in DECISIONS 112 |
| allsky_round4_pixel.csv | FFI pixel-test classification (ON_TARGET <= 0.5 px in all sectors, OFF_TARGET >= 0.9 px): 27 on target |
| allsky_round4_triage.csv | automatic triage of the 27 with the round-3 thresholds (2 PASS, 2 WEAK, 23 FAIL); not a verdict |
| allsky_round4_prior.csv | **superseded, kept as the historical product of DECISIONS 113.** Its column prior_strict came from an inline "period within 200 characters of the TIC" check that did not read compressed tables: it gave a false "catalog" tag for 188664994 (a neighbouring row's luminosity value) and missed 343298093 (eumemic vetted_signals.csv.gz). Use the matcher outputs below. |
| prior_match_20261021.csv | first run of the row-aware matcher (scripts/prior_match.py) |
| prior_match_20261021b.csv (+ _text.csv, _unresolved.csv) | corrected run (pipeline-prefixed period columns such as RAVEN's bls_per; unresolved schemas listed); this is the current result |
| prior_match_targets_20261021.csv | the 67 objects searched (all registered objects and the round-4 on-target signals) |

Selection, freezes and corrections: README "All-sky round 4 and corrections"; prior_search/ERRATUM_PRIOR_DETECTIONS_2026-10-21.md.
