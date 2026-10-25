> **WITHDRAWN 2026-10-25 before publication (DECISIONS 187). This combined likelihood-ratio interpretation is NOT supported: its noise-only PASS count is a structural zero (fixed noise-only BLS peaks unreachable by the allowed trial periods), so the PASS ratio is neither a bound nor a calibrated likelihood ratio, and the 'declared conclusions' below are not current interpretations of anything. Kept for history only. Current material: calibration_diagnostics_v1.3.md / .json (descriptive conditional frequencies). Original bytes before this label: .md SHA-256 d5ec8f26d6375a16a9eff0251c2d5385b8af7e8050e653a59c8ade9cb3b09199, .json SHA-256 db092d38d9955345e6c0ba0ad86fae3486235885647601b6f580b6606ce99019.**

# [WITHDRAWN] TIC 317134140 S108-S110: interpretation table as drafted (rule DECISIONS 185; calibration `calibration_v1.3.json`, SHA-256 `d2c5b2ec162d9509...`)

Pooled single-sector training sectors S6, S87, S107. H1 is a 185 ppm injection (300 trials); H0 is noise only (6000 trials). Each probability is (k + 1/2) / (N + 1).

| Sector outcome | H1 count | H0 count | P(outcome given H1) | P(outcome given H0) | LR |
|---|---:|---:|---:|---:|---:|
| PASS | 93 | 0 | 0.311 | 8.33e-05 | 3.73e+03 |
| PARTIAL | 175 | 107 | 0.583 | 0.0179 | 32.5 |
| INCONCLUSIVE | 30 | 846 | 0.101 | 0.141 | 0.718 |
| FAIL | 2 | 5047 | 0.00831 | 0.841 | 0.00987 |
| INSUFFICIENT (calibration count only; LR fixed at 1) | 0 | 0 | | | 1 |

## All outcome combinations for S108, S109 and S110 (order-free)

The last three columns are a depth-sensitivity disclosure (added 2026-10-25 after the calibration was seen; DECISIONS 186). They are reported, NOT used; the declared conclusion is the one in the third column.

| Outcomes | Combined LR (H1 = 185 ppm) | Declared conclusion | LR if H1 = 130 ppm | LR if H1 = 240 ppm | Conclusion if 130 ppm (not used) |
|---|---:|---|---:|---:|---|
| PASS + PASS + PASS | 5.18e+10 | strong evidence that the signal persists | 5.81e+08 | 4.8e+11 | strong evidence that the signal persists |
| PASS + PASS + PARTIAL | 4.52e+08 | strong evidence that the signal persists | 2.12e+07 | 1.19e+09 | strong evidence that the signal persists |
| PASS + PASS + INSUFFICIENT / UNAVAILABLE / INVALID_INPUT | 1.39e+07 | strong evidence that the signal persists | 6.97e+05 | 6.13e+07 | strong evidence that the signal persists |
| PASS + PASS + INCONCLUSIVE | 9.98e+06 | strong evidence that the signal persists | 1.23e+06 | 1.44e+06 | strong evidence that the signal persists |
| PASS + PARTIAL + PARTIAL | 3.95e+06 | strong evidence that the signal persists | 7.76e+05 | 2.95e+06 | strong evidence that the signal persists |
| PASS + PASS + FAIL | 1.37e+05 | strong evidence that the signal persists | 1.18e+05 | 2.41e+05 | strong evidence that the signal persists |
| PASS + PARTIAL + INSUFFICIENT / UNAVAILABLE / INVALID_INPUT | 1.21e+05 | strong evidence that the signal persists | 2.55e+04 | 1.52e+05 | strong evidence that the signal persists |
| PASS + PARTIAL + INCONCLUSIVE | 8.72e+04 | strong evidence that the signal persists | 4.48e+04 | 3.57e+03 | strong evidence that the signal persists |
| PARTIAL + PARTIAL + PARTIAL | 3.45e+04 | strong evidence that the signal persists | 2.84e+04 | 7.31e+03 | strong evidence that the signal persists |
| PASS + INSUFFICIENT / UNAVAILABLE / INVALID_INPUT + INSUFFICIENT / UNAVAILABLE / INVALID_INPUT | 3.73e+03 | strong evidence that the signal persists | 835 | 7.83e+03 | strong evidence that the signal persists |
| PASS + INCONCLUSIVE + INSUFFICIENT / UNAVAILABLE / INVALID_INPUT | 2.68e+03 | strong evidence that the signal persists | 1.47e+03 | 184 | strong evidence that the signal persists |
| PASS + INCONCLUSIVE + INCONCLUSIVE | 1.92e+03 | strong evidence that the signal persists | 2.59e+03 | 4.31 | strong evidence that the signal persists |
| PASS + PARTIAL + FAIL | 1.2e+03 | strong evidence that the signal persists | 4.31e+03 | 598 | strong evidence that the signal persists |
| PARTIAL + PARTIAL + INSUFFICIENT / UNAVAILABLE / INVALID_INPUT | 1.06e+03 | strong evidence that the signal persists | 930 | 377 | strong evidence that the signal persists |
| PARTIAL + PARTIAL + INCONCLUSIVE | 761 | strong evidence that the signal persists | 1.64e+03 | 8.84 | strong evidence that the signal persists |
| PASS + FAIL + INSUFFICIENT / UNAVAILABLE / INVALID_INPUT | 36.8 | strong evidence that the signal persists | 141 | 30.8 | strong evidence that the signal persists |
| PARTIAL + INSUFFICIENT / UNAVAILABLE / INVALID_INPUT + INSUFFICIENT / UNAVAILABLE / INVALID_INPUT | 32.5 | strong evidence that the signal persists | 30.5 | 19.4 | strong evidence that the signal persists |
| PASS + INCONCLUSIVE + FAIL | 26.4 | strong evidence that the signal persists | 249 | 0.724 | strong evidence that the signal persists |
| PARTIAL + INCONCLUSIVE + INSUFFICIENT / UNAVAILABLE / INVALID_INPUT | 23.4 | strong evidence that the signal persists | 53.7 | 0.456 | strong evidence that the signal persists |
| PARTIAL + INCONCLUSIVE + INCONCLUSIVE | 16.8 | strong evidence that the signal persists | 94.5 | 0.0107 | strong evidence that the signal persists |
| PARTIAL + PARTIAL + FAIL | 10.5 | strong evidence that the signal persists | 157 | 1.48 | strong evidence that the signal persists |
| INSUFFICIENT / UNAVAILABLE / INVALID_INPUT + INSUFFICIENT / UNAVAILABLE / INVALID_INPUT + INSUFFICIENT / UNAVAILABLE / INVALID_INPUT | 1 | inconclusive | 1 | 1 | inconclusive |
| INCONCLUSIVE + INSUFFICIENT / UNAVAILABLE / INVALID_INPUT + INSUFFICIENT / UNAVAILABLE / INVALID_INPUT | 0.718 | inconclusive | 1.76 | 0.0235 | inconclusive |
| INCONCLUSIVE + INCONCLUSIVE + INSUFFICIENT / UNAVAILABLE / INVALID_INPUT | 0.516 | inconclusive | 3.1 | 0.000551 | moderate evidence that the signal persists |
| INCONCLUSIVE + INCONCLUSIVE + INCONCLUSIVE | 0.371 | inconclusive | 5.46 | 1.29e-05 | moderate evidence that the signal persists |
| PASS + FAIL + FAIL | 0.364 | inconclusive | 23.9 | 0.121 | strong evidence that the signal persists |
| PARTIAL + FAIL + INSUFFICIENT / UNAVAILABLE / INVALID_INPUT | 0.321 | moderate evidence against persistence | 5.16 | 0.0764 | moderate evidence that the signal persists |
| PARTIAL + INCONCLUSIVE + FAIL | 0.231 | moderate evidence against persistence | 9.09 | 0.00179 | moderate evidence that the signal persists |
| FAIL + INSUFFICIENT / UNAVAILABLE / INVALID_INPUT + INSUFFICIENT / UNAVAILABLE / INVALID_INPUT | 0.00987 | strong evidence against persistence | 0.169 | 0.00394 | moderate evidence against persistence |
| INCONCLUSIVE + FAIL + INSUFFICIENT / UNAVAILABLE / INVALID_INPUT | 0.00709 | strong evidence against persistence | 0.298 | 9.24e-05 | moderate evidence against persistence |
| INCONCLUSIVE + INCONCLUSIVE + FAIL | 0.0051 | strong evidence against persistence | 0.525 | 2.17e-06 | inconclusive |
| PARTIAL + FAIL + FAIL | 0.00317 | strong evidence against persistence | 0.874 | 0.000301 | inconclusive |
| FAIL + FAIL + INSUFFICIENT / UNAVAILABLE / INVALID_INPUT | 9.75e-05 | strong evidence against persistence | 0.0287 | 1.55e-05 | strong evidence against persistence |
| INCONCLUSIVE + FAIL + FAIL | 7e-05 | strong evidence against persistence | 0.0505 | 3.64e-07 | strong evidence against persistence |
| FAIL + FAIL + FAIL | 9.63e-07 | strong evidence against persistence | 0.00485 | 6.1e-08 | strong evidence against persistence |

## Reported, not used

| Set | H1 trials | PASS | PARTIAL | INCONCLUSIVE | FAIL | INSUFFICIENT | H0 trials | H0 FAIL | H0 PASS |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| S6 at 185 ppm | 100 | 44 | 49 | 6 | 1 | 0 | 2000 | 1690 | 0 |
| S87 at 185 ppm | 100 | 36 | 53 | 11 | 0 | 0 | 2000 | 1603 | 0 |
| S98 at 185 ppm | 100 | 71 | 27 | 2 | 0 | 0 | 2000 | 1953 | 0 |
| S107 at 185 ppm | 100 | 13 | 73 | 13 | 1 | 0 | 2000 | 1754 | 0 |
| S6+S87+S107 at 130 ppm | 150 | 10 | 82 | 37 | 21 | 0 | | | |
| S6+S87+S107 at 240 ppm | 150 | 98 | 52 | 0 | 0 | 0 | | | |

Residual clause-A depth at the true ephemeris after dividing out the real signal: S6 -47 +- 62 ppm; S87 -38 +- 86 ppm; S98 31 +- 25 ppm; S107 20 +- 50 ppm.

Caveats: the trials share one noise realization per sector, so binomial uncertainties understate the true uncertainty. Ratios for outcomes with zero noise-only counts (PASS) are set by the (k + 1/2) / (N + 1) estimator, so they are bounds of order N, not measured values. The ratios assume a 185 ppm signal: the training sectors measured 127-210 ppm, and at 130 ppm a real signal FAILs in about 14 % of sectors, so combinations containing a FAIL are strongly depth-dependent (see the sensitivity columns). H1 is equally satisfied by a planet and by a blended eclipsing binary; no conclusion here means "validated".
