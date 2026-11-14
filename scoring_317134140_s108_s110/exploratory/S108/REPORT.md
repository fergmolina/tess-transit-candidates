# Sector 108 of TIC 317134140: EXPLORATORY, post-outcome report (2026-11-13)

**Status.** Exploratory. The outcome of record for Sector 108 is PARTIAL (v1.20) and does not change. Plan: `PLAN.md`
(SHA-256 `07c490b3e9a69399...`, declared in DECISIONS 232 before the analysis). Frozen ephemeris only; no refit. Numbers:
`report.json`, `quality_addendum.json`. Not reviewed. Not published.

## Gate
The locked `preprocess` and `clause_a`, imported unmodified, give 11,862 cadences, 28 of 48 eligible events, depth 206.336 ppm and
sigma 54.987 ppm: identical to the result of record. The locked blind search gives the same three peaks and SDE values.
(Same author and machine; this is not an independent reproduction.)

## 1. Why 20 events were not eligible: the sector has large data losses
| Step | Cadences |
|---|---:|
| Rows in the file | 19,702 |
| No finite time stamp | 1,227 |
| Time present, PDCSAP flux or error not finite | 5,132 |
| QUALITY != 0 among the rest | 0 |
| Edge trim (0.3 d around gaps and ends) | 1,118 |
| TOI-2514.01 mask | 363 |
| Detrending NaN / upward clip | 0 / 0 |
| Kept | 11,862 (60 %) |

- The kept data run from BTJD 4293.88 to 4318.04 with two long gaps: 4296.39-4298.29 (1.9 d) and 4304.80-4308.43 (3.6 d).
- The 5,132 rows without corrected flux: 3,507 have QUALITY 4096, 648 have 128, 537 have 32768, 421 have 0; raw SAP flux is finite
  in 5,113 of them. The long runs are 4290.98-4293.58, 4305.10-4308.13, 4310.56-4311.70 and 4317.16-4318.35. The meaning of the
  flag values was not looked up in the mission documents here.
- Ineligible events by the dominant loss within 3 h of the predicted time: no corrected flux 12; no time stamp 3; edge trim 3;
  TOI-2514.01 mask 2. Seventeen of the 20 have no usable cadence at all in the window.
- Without the TOI mask, 30 events would be eligible instead of 28 (counts only; no depth computed).
- So the losses are data gaps of the sector, not a property of the rule. Nothing is known yet about Sectors 109 and 110.

## 2. The 1.1467-d peak
- **At the candidate period:** the grid point nearest P (0.57199 d) has SDE 4.68 and is the 22nd-highest of 5,541 grid points. The
  best grid point within 0.1 % of P has SDE 4.84 (17th); within 0.5 %, SDE 5.24 at 0.57265 d (9th). These are ranks of grid points,
  not of distinct peaks. The third peak of record has SDE 5.70. The grid step is 0.057 %.
- **At exactly 2P:** SDE 2.0 (374th). The best within 0.1 % of 2P is SDE 2.9. The 1.1467-d peak is 0.26 % away.
- **Phase of the first peak:** each of its 21 transit times falls next to a frozen predicted time of ODD epoch. The offset is
  -0.21 h at the start of the sector and grows to +1.24 h at the end (drift 1.53 h against T14 = 1.5 h). For about the first
  two thirds of the sector the offset is inside the +-0.75 h transit window.
- **Odd/even at the frozen ephemeris (clause A statistic):** odd 250 +- 65 ppm (13 events), even 167 +- 63 ppm (15 events);
  difference 83 +- 90 ppm (0.9 sigma). The sensitivity declared in advance was about 110 ppm; the measured one is 90 ppm. A signal
  truly at 2P would put about 400 ppm in one parity and none in the other; that is not seen (even depth is 2.6 sigma above zero).
- **Reading:** the first peak overlaps the candidate's odd-epoch events in phase at a slightly longer period. That is compatible
  with the blind search latching onto every second event of the candidate in gappy data, and equally with an unrelated
  fluctuation. This look cannot tell them apart, and the peak does not count toward clause B either way.
- Figure: `fold_S108.png`. The fold at the frozen P shows the lowest bins inside the predicted window; the scatter of the
  other bins is of similar size to the dip (bin errors about 80 ppm).

## 3. On-target checks (not decisive, as declared)
- **Centroid shift, in minus out of transit:** dx 0.071 +- 0.054 mpx, dy 0.068 +- 0.090 mpx; total 0.098 mpx, 1.5 sigma (1,319
  in-transit cadences). No significant shift. Earlier sectors: 1.0, 1.9, 5.3 (S98) and 0.8 sigma.
- **Pixel map** (`pixelmap_S108.png`; target-pixel file SHA-256 `fd96a0c06789a693...`, 48,268,800 bytes, downloaded once): the
  flux-loss centroid is 0.56 px from the target position and 0.69 px from the flux centroid, with bootstrap errors of 0.15 and
  0.17 px. Both are within the range seen for a known on-target planet with this method (0.46 and 0.65 px) and for S98 (0.64 and
  0.71 px). By the rule declared in advance (> 1 px and > 3 sigma), this is not evidence of an off-target source. It is not
  evidence that the signal is on the target either: a neighbour within a few arcsec cannot be excluded this way.
- 19 of 43 measured pixels have positive flux loss; the edge pixels are noise-dominated (per-pixel values of thousands of ppm).

## Deviations from the plan
- Added: the QUALITY values of the rows without corrected flux (`quality_addendum.json`), within item 1's stated aim.
- Added to `report.json` but not used above: the blind search's own odd/even depths for its three peaks, and an
  aperture flux-weighted mean of the per-pixel depths (111 ppm). The latter is not a calibrated depth.
- "Rank" is the rank among grid points, as the plan says; no list of distinct peaks beyond the top three was made.
- P/2 is below the grid minimum (0.5 d), so nothing is reported for it.

## What this does and does not change
Nothing in the test. For reading the PARTIAL outcome: the missing 20 events are explained by gaps; the candidate period is not a
top peak mainly because its SDE in this gappy sector is about 4.7-5.2; the top peak sits on the candidate's odd events in phase but
no odd/even depth difference is detected; and no off-target signature is seen at the limited sensitivity available.


---

**Dated status note, 2026-11-14 (v1.21).** Everything above this line is the report as written on 2026-11-13 (SHA-256
`1e28db50d767de28509911eb3719cd069bed9e2aaed77663f2231fef3bb8b0e4` for those bytes alone); "Not reviewed. Not published." was its status then. It has since been reviewed
(`../../../reviews_v1_21/REVIEW_exploratory_S108.md`, verdict "fix first", findings F1 to F10) and is published here unchanged
together with `CORRECTIONS_AND_COMPLETION_2026-11-14.md`, which withdraws or qualifies several statements above and lists a departure
from the plan that the report did not disclose. **Where the two differ, the corrections note holds.** The Sector 108 outcome of
record remains PARTIAL.
