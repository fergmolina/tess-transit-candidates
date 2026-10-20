# Dated addendum — QLP barycentric clock error and the frozen predictions (2026-10-19)

The frozen files are not changed. This addendum quantifies how much the QLP S99+ clock error moves each frozen prediction.

Method: scripts/qlp_clock_check.py. Each QLP light curve is aligned with a TESScut cutout of the same FFIs (identical cadence lists, or
data-gap edges when the lists differ). The QLP−TESScut offset is compared with a clean control sector (S56–S98, where QLP−TESScut ≈ 0 to
+0.3 min), and the ephemeris is refitted with the same weighted linear fit, which reproduces each frozen period to <1e-13 d.

Finding beyond MAST's notice: **QLP Sector 105 is also affected.** There QLP−TESScut ≈ −TIMECORR (−3.70 vs 3.66 min; −2.11 vs 2.08 min),
i.e. the S105 QLP times carry no barycentric correction. Sector 106 QLP data, the test data for two objects, must therefore be checked
the same way before any test is run.

| Object | Affected sectors used (correction, min) | Shift of frozen predictions | Frozen 1σ at test |
|---|---|---|---|
| TIC 89247735 | S104 (+8.02) | see v4 (+4.4 to +5.6 vs v1) | 3–4 min |
| TIC 183374279 | S103 (−2.87), S105 (+3.98) | +1.4 min (S106) | 2.7 min |
| TIC 120444365 | S103 (−3.14), S105 (+2.12) | −0.04 min (S106) | 2.1 min |
| TIC 80387959 | S100 (+1.08) | +0.5 min (S111) | 3.5 min |
| TIC 258006047 | S99 (+0.30), S100 (+0.96), S101 (+4.41), S102 (+3.92) | +3.9 min (S114) | 4.7 min |
| TIC 333735955 | S100 (+1.60), S101 (+2.67) | +3.1 min (S114) | 2.7 min |
| TIC 467959906 | S103 (+3.59) | +3.6 min (S114) | 4.1 min |
| TIC 120517801 | S100 (+1.02) | +0.7 min (S111) | 15.9 min |

Every shift is at most about 1.1 times the frozen 1σ, far inside the ±3σ / ±30-min windows of the frozen outcome rules. No outcome rule
changes. Each test will report both the frozen and the clock-corrected prediction, and the test data themselves will be clock-checked
first.
