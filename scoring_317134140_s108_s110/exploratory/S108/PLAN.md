# Exploratory, post-outcome look at Sector 108 of TIC 317134140: plan declared before any analysis

Status of the test: Sector 108 was scored once under the v1.18 lock on 2026-11-13 (PARTIAL; published in v1.20). That outcome is
the outcome of record. **Nothing here can change it.** No lock, config, scorer, prediction file or frozen ephemeris changes,
whatever is found. Sectors 109 and 110 stay locked and unexamined. Every result below is reported, including adverse ones. All
outputs go to `results/exploratory_317134140_S108/` and are labelled "exploratory, post-outcome". This is NOT the independent
computational reproduction the reviewer recommended (same author, same machine). Nothing is published without the auditor's
check and the author's go. The author approved items 1-3, including the target-pixel download, on 2026-11-13.

Data: the Sector 108 light curve of record (SHA-256 cea2619b...) and, for item 3 only, the Sector 108 SPOC target-pixel file of the
same observation (`tess2026250081459-s0108-0000000317134140-0310-s_tp.fits`), downloaded once into a fresh directory with its
SHA-256 recorded. No other download.

Ephemeris: the frozen one only (P 0.5718634 d, T0 BTJD 1468.67922; event times from the frozen prediction CSV). No refit of P or T0.

## Item 0. Gate: reproduce the outcome of record
`preprocess` and `clause_a` are imported unmodified from the locked scorer. They must give 11,862 cadences, 28 of 48 eligible events
and a depth of 206.336 ppm with sigma 54.987 ppm. If not, stop and report; items 1-3 are not run.

## Item 1. Why were 20 predicted events not eligible?
- Per predicted event: number of in-window cadences (needs >= 23 of 45), out-of-transit cadences before and after (needs >= 10
  each), which of the three tests failed, and eligible yes/no. The count of eligible events must be 28.
- Cadence accounting for the whole sector from the raw columns: total rows; removed by non-finite time/flux/error; QUALITY != 0;
  error <= 0; edge trim (0.3 d around gaps > 0.25 d and the ends); TOI-2514.01 mask; detrending NaN; upward 5-sigma clip. The
  remainder must be 11,862.
- For each ineligible event: which of those steps removed its window (the dominant step by cadence count), and the time ranges of
  the gaps.
- For reference only: the same per-event counts with the TOI mask not applied, to see how many events it costs. No depth is
  computed for that variant.

## Item 2. What is the 1.1467-d peak?
- Re-run the locked clause-B search (same functions and grid) and keep the full periodogram. Report the power/SDE and rank among
  all grid periods of the grid point nearest P (0.5718634 d), P/2 and 2P (1.1437268 d), the local grid step at 2P, and the
  highest SDE within 0.1 %, 0.5 % and 1 % of P and of 2P.
- First peak (1.14675 d, t0 BTJD 4294.2474): offset of its t0 from the nearest frozen predicted time, in hours and in units of
  T14 (1.5 h); and the drift between a 1.14675-d and a 2P ephemeris across the sector, compared with T14.
- Odd/even: clause A's statistic (same windows, same eligibility, same 200 seeded shifts) on eligible events of odd and of even
  epoch number separately (epoch = round((tc - T0)/P)). Sensitivity stated in advance: each half has about sqrt(2) x 55 = 78 ppm
  sigma, so the difference has about 110 ppm sigma; only a difference above about 220 ppm would be notable. A signal truly at
  2P would put the whole depth (~400 ppm) in one parity and ~0 in the other.
- Not done: no comparison of the BLS depth (451 ppm) with the 206-ppm stack; they are different depth definitions.
- One figure: the detrended light curve folded on the frozen ephemeris (binned), and on 2P.

## Item 3. Is the dip on the target? (target-pixel file)
- Methods: those of `scripts/vet.py` used before for this star (`centroid_shift` and `pixel_depth_map`, which made
  `pixelmap_S98.png`), unchanged in their definitions: QUALITY == 0 / lightkurve default bitmask, edge trim, masked biweight 0.75 d,
  in-transit |dt| < T14/2, out-of-transit T14 < |dt| < 3 T14, on the frozen ephemeris. Only the file source differs (the local
  S108 files instead of a search/download inside the function).
- Report: the in-minus-out shift of the flux-weighted centroid (dx, dy, errors, significance) and the flux-loss centroid with its
  bootstrap error and its offsets from the target position and from the flux centroid.
- Comparison values recorded earlier: centroid shift S6 1.0 sigma, S87 1.9 sigma, S98 5.3 sigma (0.34 mpx), S107 0.8 sigma;
  pixel map S98: loss centroid 0.64 px from the target, 0.71 px from the flux centroid, errors about 0.2 px. Calibration on a known
  planet (TIC 12421862 S96): 0.46 px and 0.65 px. So offsets below about 0.7 px are not evidence of an off-target source.
- Sensitivity stated in advance: Sector 108 has roughly half the in-transit cadences of S98 (two sectors). The per-pixel map of a
  ~200 ppm signal in one sector is noisy; the loss-centroid error is expected to be >= 0.2-0.3 px. A null centroid shift does not
  place the signal on the target; a neighbour a few arcsec away would move the centroid by well under 1 mpx. Only a large,
  significant offset (> 1 px and > 3 sigma) would be informative, and then against the target.

## Reporting
One report, `REPORT.md`, with every number above, plus `report.json` and the figures. Any deviation from this plan is listed in the
report.
