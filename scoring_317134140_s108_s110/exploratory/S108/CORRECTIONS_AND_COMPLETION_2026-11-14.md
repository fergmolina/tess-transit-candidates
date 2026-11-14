# Corrections and completion of the exploratory Sector 108 report of TIC 317134140 (2026-11-14)

**EXPLORATORY, POST-OUTCOME. The Sector 108 outcome of record is PARTIAL and is unchanged.**

This note corrects and completes `REPORT.md` (SHA-256 `1e28db50d767de28...`) after the external review
`REVIEW_exploratory_S108.md` (SHA-256 `cdd0d385e8fad66f...`, verdict "fix first", findings F1 to F10). The report itself is
kept unchanged. Where this note and the report differ, this note holds. Every number here comes from the saved `report.json` and
`quality_addendum.json`. No photometry was opened and no script was run to write this note.

The plan was written after the Sector 108 outcome was known. It is an author-reported advance plan for a post-outcome
exploration, not an independently timed blind test. The review read sources, saved outputs and figures; it is not an independent
computational reproduction.

## F1, F2. The 20 events that were not eligible
Withdrawn: "the losses are data gaps of the sector, not a property of the rule", and "the missing 20 events are explained by
gaps".

Replaced by the reviewer's text: Of 48 predicted events, 20 fail the locked eligibility rules. The dominant removal stages within
±3 h are nonfinite corrected flux or uncertainty (12), absent finite-time rows (3), edge trimming (3) and the TOI mask (2).
Seventeen have no retained cadences in the ±0.75-h transit window; fifteen have none throughout ±3 h. These are consequences of
both data availability and the fixed processing rules.

- The tally is an ordered accounting of which preprocessing step removed the most cadences. It is not a causal experiment.
- The report's "Seventeen of the 20 have no usable cadence at all in the window" referred to the ±0.75-h window, which the
  sentence did not say.
- Without the TOI-2514.01 mask 30 events would be eligible instead of 28. The locked rules are not changed.

## F8. Rows without corrected flux
- The 5,132 rows have nonfinite corrected (PDCSAP) flux **or uncertainty**, not necessarily nonfinite flux alone.
- QUALITY values of all 5,132 rows: 4096: 3,507; 128: 648; 32768: 537; 0: 421; 32: 8; 160: 7; 16: 2; 144: 1; 168: 1. The report
  listed only the first four (5,113 rows); the other 19 rows carry the remaining values. That the raw SAP flux is finite in
  5,113 rows is a separate count that happens to be equal.
- Bit 128 is set in 657 rows when combined values are included.
- Rows with error <= 0: none.
- The four intervals in the report are clusters of such rows, joined when less than 0.05 d apart. They are not proven
  continuous gaps.
- The kept data also have two short gaps of 0.254 d (BTJD 4299.77 to 4300.03 and 4312.56 to 4312.82) beside the two long ones.
- **Flag meanings** (reviewer's lookup on 2026-11-14 UTC in the MAST TESS Data Product Overview, cadence quality flags table,
  https://outerspace.stsci.edu/spaces/TESS/pages/14563420/2.0%2B-%2BData%2BProduct%2BOverview): 4096, exclusion for scattered
  light; 128, manual exclusion for an anomaly; 32768, exclusion because too few targets were available for error correction.
  This is a documentation lookup, not photometry. The labels do not establish the cause of each nonfinite value or the history
  of the sector. Most of these rows still have finite SAP flux, so they are not uniformly "no observation collected". The lookup
  is not used to change the locked quality mask or to recover cadences.

## F6, F7. Periodogram numbers
- Corrected: "At exactly 2P: SDE 2.0" should read "at the grid point nearest 2P". The grid point is 1.143457 d; 2P is
  1.1437268 d; the grid point is 0.024 % below 2P. Its SDE is 2.00 (374th of 5,541 grid points).
- Near P: nearest grid point 0.571990 d, SDE 4.68 (22nd). Best within 0.1 %: 0.571662 d, SDE 4.84 (17th). Best within 0.5 % and
  within 1 %: 0.572648 d, SDE 5.24 (9th).
- Near 2P: best within 0.1 %: 1.144772 d, SDE 2.94 (162nd). Best within 0.5 % and within 1 %: the first peak itself, 1.146748 d,
  SDE 7.07 (1st).
- Local grid step at 2P: 0.0575 %, the same as at P.
- First peak: 14 of its 21 model transit times are within ±0.75 h of a frozen odd-epoch time. The first offset is -0.21 h
  (-0.14 T14) and the last +1.24 h. The drift against a 2P ephemeris across the kept baseline is 1.53 h (1.02 T14). These are
  model times, not 21 observed transits.
- **Not retained:** the script saved summaries of the periodogram, not the full power and SDE arrays the plan mentions. For the
  variant without the TOI mask it saved only whether each event would be eligible, not the three counts per event. Neither is
  reconstructed here.

## F4, F9. Odd and even events, and the reading of the first peak
- Measured depths stand: odd 249.7 ppm (spread 64.7 ppm, 13 of 24 events), even 166.6 ppm (spread 63.3 ppm, 15 of 24). The
  difference is 83.1 ppm.
- 90.5 ppm is the quadrature sum of the two spreads. It is an **uncorrelated approximation**: both halves use the same seeded
  shifts, their covariance was not saved, and it is not a calibrated error on the difference. The ratios 0.92 (difference) and
  2.63 (even depth) are nominal ratios, not calibrated tail probabilities.
- Withdrawn: "no parity difference detected" as a detection statement, and the "measured" sensitivity of 90 ppm. Replaced by:
  no compelling parity contrast is established by this exploratory diagnostic.
- The 400 ppm / 0 ppm illustration holds only for a simplified model: a single eclipse per cycle at exactly 2P with no
  secondary event. The even-depth ratio does not exclude all 2P or eclipsing-binary scenarios.
- Withdrawn: "equally" in the reading of the first peak, and "mainly because" in the closing paragraph. Replaced by the
  reviewer's text: The candidate-period grid summaries are below the three selected BLS peaks; these diagnostics do not
  establish that gaps caused the rank. The leading peak is 0.264% above 2P and overlaps odd-epoch phases for part of the
  baseline, but its origin and association with the candidate remain unresolved. Both readings (every second event of the
  candidate, or an unrelated fluctuation) remain possible, with no quantified relative support.

## F3, F5. Position checks
- **Departure from the plan, not listed in the report.** The plan promised the definitions of `scripts/vet.py` unchanged. The
  order of edge trimming differs. `vet.py` trims on the original time array and then combines the masks. The exploratory
  script first selects rows with finite time, centroids and flux and QUALITY 0 (centroid check), or with all pixels finite
  (pixel map), and trims those. Because the trim finds gaps and ends from the array it is given, the two orders are not
  generally equivalent. Numerical equivalence with the earlier implementation was not established, so the Sector 108 values are
  not strictly comparable with those of the earlier sectors or of the control star. No re-run was made to test this.
- **Centroid shift.** 0.098 mpx; the "1.5 sigma" is a nominal value that treats cadences and the two axes as independent. It is
  not a calibrated significance.
- **Flux-loss centroid.** The values 0.15 and 0.17 px are not "bootstrap errors" of the two offsets. They are the scatters of
  the x and y coordinates of the loss centroid over 200 independent Gaussian perturbations of the per-pixel depths. They are
  not calibrated location errors and not one error per radial offset.
- Not accounted for: correlation in time, between pixels and between axes; the weighting by positive loss only; the uncertainty
  of the target position and WCS. TOI-2514.01 transits are not masked in these two diagnostics.
- The flag declared in advance (> 1 px and > 3 sigma) was not triggered because the distance is below 1 px (0.56 px). No
  confidence-level exclusion of a neighbour follows.
- Withdrawn: "within the range seen for a known on-target planet" as a calibration. The earlier offsets (0.46 and 0.65 px for
  the control star, 0.64 and 0.71 px for S98) are examples, not a calibrated distribution; the control values are recorded
  assertions that the reviewer could not reconstruct from saved coordinates.
- The pixel map used 17,035 cadences with 1,857 in transit; the centroid check used 1,319 in-transit cadences. The selections
  differ.
- The plan's "S98 (two sectors)" is withdrawn: the saved comparison is for Sector 98 alone. "Roughly half the in-transit
  cadences" stands for the pixel map (1,857 against 4,280).
- The pixel loop skips a pixel silently if detrending raises an exception and does not record why; 43 pixels were measured.
  There is no minimum out-of-transit count for the map.
- Reviewer's summary, adopted: The position diagnostics do not localize the signal securely or exclude nearby blended sources.

## F10. Figure captions
- `fold_S108.png`: the two folds use the frozen P and 2P. Error bars are the scatter within each bin divided by sqrt(N), with
  no red-noise calibration. In the 2P panel the even epochs lie at the centre and the odd epochs at the joined boundaries.
- `pixelmap_S108.png`: axes are image pixels; the white contour is the pipeline aperture; markers are labelled. The depth
  colour scale saturates at ±3,000 ppm, while the saved per-pixel values run from -9,292.7 to +39,250.6 ppm. There are no
  colour bars.

## Other limits
- Choices of bin number (40 and 80), quality mask, plotting scale and masking order were at the author's discretion. The plan is
  not a pre-registered significance calibration.
- The script writes its outputs in place; nothing in it enforces a single execution. One run is author-reported.
- File times support the account that the plan preceded the analysis; they cannot prove it or exclude earlier unrecorded
  inspection.
- None of this changes PARTIAL. The locks, configs, predictions and scoring procedure for Sectors 109 and 110 are unchanged, and
  those sectors are scored and published separately, without pooling.
