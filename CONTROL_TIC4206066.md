# Positive control: TIC 4206066 (Rabtsevich 2026 candidate host)

Purpose: verify that this project's search machinery recovers the independently reported signals before trusting
any null or positive result on new stars.

Data used (via lightkurve/MAST): S98 QLP (200 s FFI, 12,067 pts, rms 636 ppm), S6 TESS-SPOC (1800 s FFI, 975 pts, rms 223 ppm),
S32 SPOC (120 s, 17,092 pts, rms 872 ppm). Detrending: wotan biweight, 0.5 d window; 5-sigma upward clip only.
Search: astropy BoxLeastSquares, SNR objective, durations 1-3 h, log-uniform frequency grid with step d(ln f) = dur_min/(T*oversample).

## Single-sector results (period range 0.5-13 d)
| Sector | top-3 peaks (P d / depth ppm / SDE / Ntr) |
|---|---|
| S98 QLP | 11.1328 / 900 / 9.0 / 3 ; 3.7112 / 405 / 8.7 / 8 ; **3.1816 / 332 / 7.2 / 10** |
| S6 TESS-SPOC | **3.1845 / 398 / 9.2 / 6** ; 6.3667 / 450 / 8.1 / 4 ; 1.5929 / 201 / 5.8 / 13 |
| S32 SPOC | 9.3123 / 605 / 6.7 / 3 ; 10.9084 / 595 / 5.4 / 3 ; 4.3607 / 394 / 5.0 / 5 |

The 3.18 d signal is the top peak in S6 and the 3rd peak in S98; it is not among the top-3 in S32 alone. The 11.13 d
signal (the reference work's tentative "signal B") is the S98 top peak. Fixed-period test at P=11.1328 shows ~455 ppm
dips in S6 and S32 as well.

## Stitched S6+S32+S98 (baseline 2578 d, 456,399 trial periods, 10-min bins)
| rank | P (d) | depth (ppm) | dur (h) | SNR | SDE | Ntr | odd / even / phase-0.5 (ppm) |
|---|---|---|---|---|---|---|---|
| 1 | **3.18279** | 367 | 1.5 | 13.7 | 14.2 | 24 | 343 / 386 / 188 |
| 2 | **11.13273** | 717 | 1.5 | 14.1 | 14.1 | 7 | 652 / 850 / 370 |
| 3 | 5.56637 | 375 | 1.5 | 10.7 | 10.0 | 14 | 78 / 717 / 201 |

Conclusion: both reported signals are recovered blind as the two highest stitched peaks. Per-sector SDE for a
~400 ppm signal on a T~10 K dwarf is only 7-9, i.e. below typical single-sector thresholds; multi-year stacking is
what makes it detectable. The main search therefore ranks on the stitched multi-year SDE. Note TIC 4206066 has 2-min
SPOC data only in S32, so it would NOT have entered the 2-min-only target list used in the main search; the main
search's target class (2-min dwarfs with >=2 years of data) is a different, SPOC-covered population.

Catalog cross-check: TIC 4206066 is absent from TOI, CTOI, confirmed-planet and all SPOC TCE tables as of 2026-10-17.
Files: control_results.json, stitched_peaks.json, control_data.npz, ../../logs/control_4206066.log, ../../scripts/control_4206066.py
