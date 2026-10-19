# TIC 89247735: version-4 ephemeris (2026-10-19)

- File: `predicted_transits_2026_2027_v4.csv`, SHA-256 `4f6aba63e252c4b205ac2c9ddd8d5c9545600d3f1ff17e215e85632f6a514d88`, frozen 2026-10-19 19:19:21 UTC.
- Why: the QLP v01 Sector-104 light curve carries the MAST-announced S99–S104 barycentric clock error. Aligning it with a TESScut cutout of the
  same FFIs gives a +8.02 min correction (`scripts/s104_clock_89247735.py`). The S104 time becomes BTJD 4196.80989 ± 4.2 min (photometric 1.4,
  clock 0.2 and extraction 4.0 min, in quadrature).
- Ephemeris: P = 18.323176 ± 0.000040 d, T0 = BTJD 4196.80998 ± 1.9 min (epoch 138); χ² = 0.35 for 2 degrees of freedom; residuals −0.0, +1.0, −0.5 and −0.1 min.
- UTC columns are geocentric for mid-times and contacts (T14 = 4.52 h). The file also gives Cerro Tololo target and Sun altitudes; "full" means
  target >30° and Sun <−12° at both contacts. Epochs 159 (2027-06-25 02:10 UTC) and 162 (2027-08-19 01:29 UTC) are the first full ones; both are marginal.
- Status: **version 1 remains the test of record.** v4 is a refined ephemeris, not a new test; its predictions are +4.4 to +5.6 min from v1
  at the 2026–2027 epochs (about 1.3 × v1's 1σ).
