# External review of the three all-sky QLP candidates (TIC 80387959, TIC 120444365, TIC 120517801)

> **Note 2026-10-20 (v1.14).** Until v1.13 the public copy of this review withheld the third object (TIC 120517801) and its section 4. Both are restored by author decision. Section 4 is historical review text from 2026-10-18; current status is in README.md and `preregistration/TIC120517801/` (likely blend, host unresolved; independent rediscovery).


Reviewer: independent external referee (not part of the project). Date: 2026-10-18 (UTC evening).
Scope: REPORT.md section 12 claims for the three frozen candidates; the vetting chain in `scripts/vet.py`, `ffi_pixel_test.py`,
`tessspoc_check.py`, `prereg_candidate.py`, `known_nearby.py`; the three pre-registrations. Nothing outside
`results/external_review_allsky/` was modified. All scripts are in `scripts/`, outputs are `*.json` / `*.csv` in this directory,
plots in `plots/`, downloaded data in `data/` (TESScut 15x15 cubes for every sector of every star; every MAST light-curve product).

---

## 1. Executive summary and verdicts

| candidate | verdict | decisive evidence |
|---|---|---|
| **TIC 80387959** (P = 4.1921 d, ~700 ppm) | **SURVIVES** as a planet candidate; the "two-level depth" weakness is removed; the pixel case is weaker than stated | Independent 15x15 TESScut photometry with per-cadence background and a fixed 1.5-px aperture gives 687 +- 36 ppm with chi2 = 10.2 for 5 d.o.f. across six sectors (2019-2026) and **no early/late difference (32 +- 73 ppm)**: the QLP two-level depth is a QLP normalisation artefact, not astrophysics. Loss position combined over six sectors in sky coordinates is 2.0 +- 1.1 arcsec from the target (1.9 sigma formal, ~0.8 sigma after the per-sector scatter is accounted for); TRICERATOPS FPP = 0.047, NFPP = 0.010. Gaia DR3 RVs (26 transits, chisq p = 0.18) exclude a stellar-mass companion on the target. Signal confirmed in TESS-SPOC (S10/S36/S37/S63), TARS, ELEANOR-LITE, TGLC. |
| **TIC 120444365** (P = 5.1481 d, ~750 ppm) | **SURVIVES**, and is the cleanest of the three; but the **frozen ephemeris has the wrong period** (fixable, harmless for S106) | Isolated (nearest star able to mimic it is 64 arcsec away and would need 58 %), TRICERATOPS at the all-data ephemeris FPP = 0.041, **NFPP = 0.000** (0.049 / 0.000 at the frozen ephemeris); "likely planet" by the Giacalone et al. criteria, not validated (FPP threshold 0.015). Signal present in every independent product once the correct period is used: SPOC 2-min S29 892 +- 129 ppm, TESS-SPOC S2/S29/S69 681/955/894 ppm, TARS S2/S29/S69/S96 1001/832/930/1008 ppm, fixed-aperture cutouts 751/766/747/1176/995/674 ppm. The frozen P = 5.148082 d (from 2023-2026 times only) disagrees with the all-data BLS period 5.148179 d by 9.7e-5 d = 2.6 sigma of its own error; at that P the 2018-2023 transits fall 50-90 min early. The S106 predictions are only 4-9 epochs from T0 so they move by < 1.3 min; later predictions would not. |
| **TIC 120517801** (P = 3.2823 d, ~760 ppm) | **WOUNDED**: the signal is real and stable, and the host is probably but not demonstrably TIC 120517801 (TRICERATOPS on-target probability 0.94, pixel test inconclusive in a crowded field), and the **frozen ephemeris is biased by 22-45 min at Sector 111**, so the pre-registered test as frozen would probably fail even if the signal is real | At the project's own all-data BLS ephemeris (not the frozen one) the transit is present in every sector 2019-2026 in every product, with a constant fixed-aperture depth of 759 +- 59 ppm (chi2 10.3 / 6). The frozen P = 3.282184 d (200-s sectors only) is 3.6 sigma short of the all-data 3.282280 d and 4.6 sigma short of a seven-sector refit (3.282305 d); it places the 2019/2021 transits 66-96 min late and the S111 predictions 22-25 min (BLS) to 40-45 min (refit) early, outside the +-20 min window. TRICERATOPS at the all-data ephemeris: **FPP = 0.088, NFPP = 0.062** (the frozen-ephemeris fold gave 0.54 / 0.47 because it smeared the 2021 sectors); 29.8 % contamination, G = 14.7 star at 4.2 arcsec = 0.18 px needing 1.0-1.8 %; PSF-fit loss positions have a ~0.5 px sector-to-sector floor and a sky-combined mean 5.4 +- 1.3 arcsec from the target, 1.7 arcsec from the G = 14.7 star (not significant after the scatter). The pixel test cannot assign the host; REPORT's "pixel centroid on target" should go. |

The three findings I would put first:

1. **The TIC 80387959 depth change is not real.** It is present in QLP (and in TARS) but absent in a fixed-aperture, background-subtracted extraction of the same FFIs across all six sectors. QLP normalises each sector independently and switched to TGLC-method light curves at Sector 94 (https://archive.stsci.edu/hlsp/qlp); cross-sector QLP depths should not be used as an astrophysical test for any candidate in this project. The x1.5 depth uncertainty in the pre-registration can be dropped; the depth on the target is 690-830 ppm depending on dilution treatment (2.4 R_Earth).
2. **The project's ephemeris procedure can be biased when early sectors have few points per transit.** `vet.py:122` (`min_pts=15` in-transit points) silently discards every 600-s and 1800-s transit, so `prereg_candidate.py:13` builds the ephemeris from 200-s sectors only. For TIC 120444365 that is 2023-2026 and the resulting period is off by 2.6 sigma; the global BLS/ephemeris fit in the same `report.json` (`bls_refine.period`, `ephemeris.P`) already had the right value. The same restriction biases **TIC 120517801**: frozen P = 3.282184 vs all-data 3.282280 d (3.6 sigma), and the frozen Sector 111 predictions are 22-45 min early, i.e. outside the pre-registered +-20 min window (section 4.1); a v2 freeze is required before S111 data exist. For TIC 80387959 I checked the same thing: frozen 4.192142 vs BLS 4.192178 d (1.8 sigma), the S36/S37 box fits sit at 0 to -6 min on the frozen ephemeris, and the S111 predictions differ by 11-12 min between the two, inside the window. Separately, `vet.py:35` (`len(t) < 1000`) drops Sector 10 (2019) entirely for both southern stars, so the "detected every year" statements and the per-sector tables omit 2019; TESS-SPOC S10 (953 +- 94 ppm) is in `tessspoc_check.json` but not in REPORT.md.
3. **The QLP S99-S105 timing error is real but harmless here.** Flux-matched cadence comparison of QLP TIME against the SPOC-calibrated TESScut TIME shows QLP times drifting to -2.3 min by the end of S100, +3 to +4 min in S103, and -1 to -3.5 min in S105 (S105 is outside the range MAST lists as affected). Propagated through the frozen transit-time fits, T0 moves by 0.05, -0.8 and +1.3 min and P by < 0.1 sigma for the three stars (`timing_propagation.json`), well inside the quoted +-20 min windows. MAST has not redelivered v02 files for S99-S104 as of today (HEAD requests return 404; `mast_products.json`).

---

## 2. TIC 80387959 (TYC 8203-2056-1)

### 2.1 Independent extractions at the frozen ephemeris (`hlsp_depths.json`, `scripts/hlsp_depths2.py`)
Masked 0.7-d biweight, box depth with per-event local baselines (+-3 durations), free (duration, dt) box fit with dt up to +-90 min.

| sector (year) | QLP SAP | QLP DET | TESS-SPOC PDCSAP | TARS | review fixed aperture r = 1.5 px, bkg-subtracted, clean events | duration (h) / dt (min) from the fixed aperture |
|---|---|---|---|---|---|---|
| S10 (2019, 1800 s) | 1007 +- 131 | - | 970 +- 110 | 430 +- 184 | 660 +- 113 (4/5 ev) | 3.1 / -54 (30-min cadence) |
| S36 (2021, 600 s) | 866 +- 99 | 912 +- 92 (team) | 770 +- 86 | 818 +- 142 | 718 +- 90 | 1.9 / 0 |
| S37 (2021, 600 s) | 842 +- 118 | 993 +- 100 (team) | 777 +- 86 | 476 +- 137 | 673 +- 73 | 2.0 / -6 |
| S63 (2023, 200 s) | 790 +- 104 | 788 +- 103 | 788 +- 94 | 830 +- 150 | 801 +- 87 | 2.4 / -15 |
| S90 (2025, 200 s) | 528 +- 89 | 590 +- 88 | none (TESS-SPOC ends at S85) | 313 +- 126 | 596 +- 73 | 1.8 / +9 |
| S100 (2026, 200 s) | 619 +- 80 | 561 +- 80 | none | not delivered | 614 +- 84 | 2.1 / +3 |

Fixed-aperture weighted mean 687 +- 36 ppm (r = 1.5 px), chi2 for a constant depth 10.2 / 5 d.o.f.; r = 2.5 px: 615 +- 38 ppm, chi2 5.3 / 5.
Sectors before 2024 vs after: 700 +- 46 vs 668 +- 57 ppm (0.4 sigma). The QLP two-level pattern (920 vs 590 ppm) is not present when the same
FFIs are measured with one aperture and one background model. TARS also shows a drop in S90, but TARS is a rotation survey
("unpopular" causal-pixel-model systematics correction, https://archive.stsci.edu/hlsp/tars) with no stated aperture or dilution treatment, so it
is not a depth reference either. The fixed-aperture values are undiluted lower limits (the 1.5-px aperture contains the G = 14.0 star and the field; TIC contamination ratio 0.16), which is why TESS-SPOC PDCSAP (CROWDSAP-corrected) sits ~10 % above them in 2019-2023; the three products agree once that is allowed for. Conclusion: the depth change is a product-normalisation effect. The project should not quote a x1.5 depth
uncertainty, and it should not use QLP depths from different sectors to test for astrophysical depth variation.

Per-event aperture vs annulus check (`per_event_80387959.json`): in-transit dimming is confined to the 1.5-px aperture; the 3-5 px annulus and the
per-cadence background show nothing at the transit times except at two events with background jumps (S100 e1, e4), which were excluded above.

### 2.2 Pixel-level localisation, done independently (`scripts/pixel_review.py`, `pixel_review_80387959.json`, `plots/pixel_review_80387959.png`, `pixel_combine_80387959.csv`)
Differences from the team's test: 15x15 cutouts (team: 11x11, centroid restricted to 3.5 px, `ffi_pixel_test.py:41`); per-cadence background
subtracted (team: none, `ffi_pixel_test.py:21`); Gaia DR3 positions proper-motion corrected to the sector epoch (team: J2000 catalogue
position, `ffi_pixel_test.py:89-90`; PM shift here is only 0.06-0.08 px); PSF fit of the loss map with a free position instead of a positive-pixel
centroid; chi2 at the target and at every Gaia neighbour; all six sectors (team: three).

| sector | PSF sigma (px) | loss-fit offset from target (px) | chi2(target) - chi2(free) | G = 17.3 at 7.6 arcsec: dchi2 vs target / implied eclipse | G = 14.0 at 13.7 arcsec: dchi2 / implied eclipse | per-event mean offset (px, sigma) |
|---|---|---|---|---|---|---|
| 10 | 0.60 | 0.59 +- 0.23 | 5.5 | -0.7 / 28 % | -5.4 / 1.2 % | 0.20 (2.0) |
| 36 | 0.90 | 0.12 +- 0.19 | 0.8 | +6.4 / 23 % | +20.9 / 0.8 % | 0.22 (1.9) |
| 37 | 0.76 | 0.59 +- 0.19 | 14.4 | -9.6 / 28 % | +19.3 / 0.8 % | 0.58 (5.0 formal; event scatter chi2 33/10) |
| 63 | 0.71 | 0.23 +- 0.15 | 5.1 | +15.3 / 24 % | +4.7 / 1.1 % | 0.18 (1.8) |
| 90 | 0.64 | 0.45 +- 0.21 | 7.9 | -7.7 / 22 % | +13.4 / 0.5 % | 0.16 (1.6) |
| 100 | 0.63 | 0.36 +- 0.17 | 8.2 | +17.6 / 25 % | +19.5 / 1.0 % | 0.13 (1.4) |

Combined in sky coordinates (pixel axes rotate between sectors): weighted-mean loss position 2.05 +- 1.10 arcsec from the target (1.9 sigma),
but the six sector positions scatter with chi2 = 51.7 for 10 d.o.f., i.e. the formal per-sector errors are ~2.3x too small. With errors inflated
accordingly the mean is 0.8 sigma from the target, 2.7 sigma from the G = 17.3 star (joint dchi2 = +21 formally, ~+4 inflated) and 4.4 sigma
from the G = 14.0 star (joint dchi2 = +72, ~+14 inflated). No pixel beyond 2 px from the target reaches 4 sigma in any sector, so an eclipsing
binary 20-60 arcsec away of the kind that killed nine class-A stars is excluded; the G = 12.9 star at 43 arcsec (TIC 80387943, needs 0.4 %) sits
inside the 3.5-px fit region and is disfavoured (loss fit never moves toward it).

What this does and does not exclude: an EB 10-60 arcsec away, yes; the G = 14.0 star at 13.7 arcsec (needs 0.8-1.2 %), yes at ~4 sigma; the
G = 17.3 star at 7.6 arcsec (needs 22-28 %, a plausible EB), only at ~2.7 sigma; anything within ~1 pixel core (< 10 arcsec) that is fainter than
G ~ 18, no (would need > 50 % eclipses). The team's per-sector exclusion significances (4.8/2.8/4.3 sigma for the G = 17.3 star) are overstated
because they use the bootstrap error of the centroid estimator, which does not include the sector-to-sector systematic that both my test and
theirs show. The in-vs-out flux-weighted centroid shift is 0.0-0.2 +- 0.1-0.2 mpx in every sector, consistent with the 0.1-0.2 mpx expected for
a target-hosted 700-ppm event and 10x too small to discriminate the G = 17.3 star (expected difference ~0.3 mpx); it is not a useful test here.

### 2.3 TRICERATOPS (`scripts/triceratops_review.py`, `triceratops_80387959.json`, `_probs.csv`, `_stars.csv`)
2.5-px circular aperture in FFI coordinates (QLP apertures are not published), S63/S90/S100, QLP DET_FLUX fold, no contrast curve.
FPP = 0.047, NFPP = 0.0099. Scenario split: TP 0.76, PTP 0.18, STP 0.037, DTP 0.015; NEB/NTP on TIC 80387965 (G = 14.0, 13.8 arcsec,
flux ratio 4.5 %) 0.006, NEB on TIC 80387968 (35 arcsec) 0.003. The G = 17.3 star (TIC 80387961, flux ratio 0.26 %) contributes < 1e-3 because
TRICERATOPS uses its own flux-ratio prior, not the pixel data. Neither threshold of Giacalone et al. 2021 (FPP < 0.015 and NFPP < 1e-3,
https://arxiv.org/abs/2002.00691) is met, so this is a "likely planet" number, not validation; the earlier survey's caveat (FPP unreliable at
SNR < 15; this fold is at SNR ~17) applies.

### 2.4 Star, catalogues, phase tests
* Gaia DR3 5362389543781401216: G = 11.07, parallax 8.600 +- 0.013 mas (116.3 pc), RUWE 0.83, non_single_star 0, ipd_frac_multi_peak 0,
  ipd_gof_harmonic_amplitude 0.005, astrometric_excess_noise 0.09 mas (sig 14, normal for G = 11), not in vari_summary, no NSS solution.
  RV 7.02 +- 0.32 km/s from 26 transits, rv_amplitude_robust 5.96 km/s, rv_chisq_pvalue 0.18, rv_renormalised_gof 0.44: no RV variability. A
  0.1 M_sun companion at 4.19 d would give K ~ 13 km/s; the target is therefore not itself an eclipsing binary with a stellar companion (a brown
  dwarf or planet is allowed). GSP-Phot Teff 5128 K, logg 4.53, R 0.809; FLAME M 0.832, R 0.811 -> rho 1.56 rho_sun (TIC: 0.797 R, 0.89 M, 1.76).
  Expected T14 for b = 0.39: 2.3-2.4 h (observed 2.2 h): consistent. Rp = 2.35-2.40 R_Earth at Rp/R* = 0.0270 (undiluted); with the 16 % TIC
  contamination ratio applied to the fixed-aperture depth, ~2.5 R_Earth.
* Catalogues within 3 arcmin (`catalogs_vizier.json`): VSX lists only Gaia rotators and one Gaia EB candidate (DR3 5362390810794576128,
  G = 19.6, P = 0.567 d, 134 arcsec away; 4.192/0.567 is not an integer ratio and it would need a 200 % eclipse); SIMBAD: the target is a
  high-PM star, nothing else; no TOI/CTOI/TCE on any of the 484 TIC entries within 3 arcmin (local tables); TESS EB catalogue, ASAS-SN
  variables, WISE variables: nothing.
* Phase tests on my own stitched QLP light curve (`phase_tests.json`): depth 689 +- 42 ppm; odd 727 +- 58 vs even 648 +- 60 (0.9 sigma);
  secondary at phase 0.5: -47 +- 38 ppm; deepest other phase 81 +- 39 ppm (2.1 sigma, noise); out-of-transit harmonics (ellipsoidal cos 2phi,
  beaming/reflection sin phi, cos phi) all < 2 +- 9 ppm; box model beats a sinusoid at P by dchi2 = 258. Rotation: Lomb-Scargle of SAP flux
  peaks at 8-15 d with < 1 mmag amplitude (scattered light scale), no signal at P or P/2.

### 2.5 Ephemeris and pre-registration (`ephemeris_check.json`, `timing_propagation.json`)
The weighted linear fit, the 26 predicted times, their UTC conversion and the Sector 111-114 assignment from the orbit table were reproduced to
< 0.5 s. Dropping the one 3-sigma outlier (epoch 352, +44 min) changes T0 by -1.1 min and P by -2.7e-6 d. The S100 QLP timing error at the
two S100 epochs is -0.3 and -0.6 min; corrected ephemeris: T0 +0.05 min, P +0.02 sigma. tess-point confirms S111 (cam 4 CCD 3), S112, S113,
S114. The frozen P (4.192142 d) and the all-data BLS P (4.192178 d) differ by 1.8 sigma and by 11-12 min at the S111 epochs; the frozen
value is supported by the 2021 box fits (dt 0 to -6 min), so no change is needed, but the v2 freeze recommended below for the other
two stars should use all sectors here as well. The S111 2-min list is not yet public (I could not check it either). Bottom line: the pre-registration is arithmetically sound, and the
first testable prediction is 2026-11-27 01:11 UTC +- 6.3 min (formal).

---

## 3. TIC 120444365

### 3.1 The period problem and its consequences
`final_ephemeris.json` uses 12 QLP times from S69/S96/S103/S105 (2023-2026) only; the 2018 (S2, 1800 s) and 2020 (S29, 600 s) transits were
dropped by `vet.py:122` (`min_pts = 15` in-transit points per event) and the SPOC 2-min S29 times were not added (`prereg_candidate.py` ran
with `--no-2min`, or the 2-min times failed the dchi2 > 9 cut; `final_ephemeris.json` has no 2-min entries). Result: P = 5.148082 +- 0.000037 d,
whereas the project's own all-data BLS (`report.json: bls_refine.period = 5.148179`, `inverted_null.real_top = 5.148166`) and my free box
fits in every 2018-2023 product place the transits 50-90 min earlier than the frozen ephemeris predicts (S2: -60 to -90 min, S29: -45 to -54,
S69: -51 to -57 min). The all-data period is right: with P = 5.148179 d, T0 = 1356.5822 the dt of every product is within +-30 min (table
below). The difference, 9.7e-5 d, is 2.6 sigma of the frozen P error and produces a 0.6-1.3 min shift at the S106 epochs (559-564), which is
irrelevant for the S106 test; it would be ~1 h by 2029. The pre-registration should be re-issued with the all-data ephemeris (a v2, with v1
kept), and `prereg_candidate.py` should time the 600-s/1800-s transits (lower `min_pts`, or weight) and include the 2-min S29 events.

### 3.2 Independent extractions at the corrected ephemeris (`hlsp_depths_bls_120444365.json`)

| sector (year) | SPOC 2-min | TESS-SPOC | TARS | ELEANOR-LITE | QLP SAP / DET | review fixed aperture r = 1.5 px (clean events) | dt (min) |
|---|---|---|---|---|---|---|---|
| S2 (2018, 1800 s) | - | 681 +- 111 | 1001 +- 201 | 714 +- 162 | 597 +- 131 / - | 751 +- 144 | +3 to +12 |
| S29 (2020) | **892 +- 129** (120 s) | 955 +- 176 (600 s) | 832 +- 229 | - | 697 +- 193 | 766 +- 178 | 0 to +27 |
| S69 (2023, 200 s) | - | 894 +- 130 | 930 +- 219 | - | 866 +- 184 / 923 +- 182 | 747 +- 140 | -24 to -30 |
| S96 (2025) | - | none | 1008 +- 197 | - | 910 +- 111 / 1110 +- 108 | 1176 +- 123 | -6 to +18 |
| S103 (2026) | - | none | not delivered | - | 852 +- 111 / 740 +- 118 | 995 +- 126 | -3 |
| S105 (2026) | - | none | not delivered | - | 634 +- 116 / 609 +- 114 | 674 +- 134 | +9 |

(T16 EPD2 S2 gives -289 +- 128 ppm: the T16 EPD/TFA detrending suppresses a 2-h signal on 30-min data; TASOC S2 is unusable, rms 7-9 %.)
Fixed-aperture mean 752 +- 54 ppm, chi2 31.9 / 5 (S96/S103 high, S105 low); early vs late 746 +- 78 vs 758 +- 76 ppm. The signal is present in
2018, 2020, 2023, 2025 and 2026 in independent pipelines. The 2-min S29 detection at 6.9 sigma with dt = +3 min is the single strongest
cross-check in the whole sample. (As the team's DECISIONS item 35 says, a 2-min recovery is not a blend test; here the blend question is
answered by isolation, section 3.3.)

### 3.3 Pixel-level and blend status (`pixel_review_120444365_bls.json`, `pixel_combine_120444365_bls.csv`, `plots/pixel_review_120444365_bls.png`)
Loss-fit offsets 0.21, 0.59, 0.46, 0.06, 0.17, 0.26 px (errors 0.12-0.33) in S2/S29/S69/S96/S103/S105; sky-combined 3.5 +- 1.3 arcsec (2.6 sigma
formal; scatter chi2 15.9/10, so ~2.1 sigma). No pixel beyond 2 px from the target above 4 sigma in any sector. Gaia DR3 within 150 arcsec: 19
sources; the nearest that could produce 750 ppm is G = 18.9 at 64 arcsec (needs 58 %); the only star brighter than G = 16 within 150 arcsec is
G = 15.2 at 102 arcsec (needs 1.9 %, 4.9 px away: no loss there). TIC contamination ratio 1.1e-4. TRICERATOPS (S96/S103/S105 aperture), fold at the all-data ephemeris (`triceratops_bls_120444365.json`):
FPP = 0.041, **NFPP = 0.000**; TP 0.78, PTP 0.17, STP 0.041, DTP 0.0008, all other scenarios < 2e-4 (frozen-ephemeris fold: 0.049 / 0.000).
FPP is above the 0.015 validation threshold because of the unresolved-companion terms, so the status is "likely planet", not validated. The residual FPP is the unresolved-companion
scenarios (STP/DTP), which only imaging or RVs address. The centroid-shift test is again at the 0.1-0.3 mpx noise level.

### 3.4 Star, catalogues, phase tests
Gaia DR3 4995962239959504256: G = 11.70, parallax 7.698 +- 0.014 (129.9 pc), RUWE 0.95, non_single_star 0, ipd_frac_multi_peak 0;
**phot_variable_flag = VARIABLE**, vari_classifier SOLAR_LIKE (score 0.74), G range 0.029 mag, std 6.3 mmag: a spotted, rotating K dwarf.
The rotation signal in the QLP SAP flux is at 12.8-14.2 d with 4-11 mmag amplitude (close to the 13.7-d TESS orbit, so partly scattered
light); P_rot/P = 2.5-2.8, not a harmonic, and the box model beats a sinusoid at P by dchi2 = 173. The secondary at phase 0.5 is
-31 +- 55 ppm, odd/even 650 +- 87 vs 841 +- 75 (1.7 sigma), ellipsoidal/beaming harmonics < 14 +- 10 ppm. RV 18.89 +- 0.34 km/s from 20
transits, rv_chisq_pvalue 0.66: no stellar companion at 5.15 d. GSP-Phot Teff 4870 K, R 0.764; FLAME M 0.770 -> rho 1.73 (TIC: R 0.756, M 0.80,
1.85; the team's REPORT quotes R = 0.84 from the QLP header, which is the older TIC value in that file). Expected T14(b = 0.42) 2.4-2.5 h,
observed 2.0 h: consistent with b ~ 0.6-0.7, and the fitted rho (2.45 rho_sun, "1.78x catalog" in REPORT) is not a discrepancy: with
a/R* = 16.9 (+1.8/-4.0) the density is unconstrained at the 50 % level. Rp = 2.20-2.23 R_Earth with the Gaia/TIC v8.2 radius (REPORT: 2.45 with
R = 0.84). VSX: the target itself as a Gaia rotator (ROT); nothing else within 3 arcmin; 25 TIC entries within 3 arcmin, no known signal.

### 3.5 Ephemeris, test sector, timing error
Predictions reproduced exactly. The S103 QLP times are +2.9 to +3.9 min late and the S105 times -1.0 to -1.6 min early relative to the
SPOC-calibrated cutout times; corrected fit: T0 -0.8 min, P -0.09 sigma. tess-point confirms S106 (cam 2 CCD 4) as the only future sector
through S134, and the QLP S106 file is still absent (HTTP 404 on the product URL on 2026-10-18); the project's v1 freeze predates the data.
Observed-but-unreleased is acceptable pre-registration provided the freeze hash is deposited before the release; it is not yet deposited.
Minor: `PREREGISTRATION.md` says the star is "on no 2-min target list for S106-S110"; the local `catalogs/target_lists/all_targets_S106_v1.csv`
does not contain it, confirmed.

---

## 4. TIC 120517801
> *Historical review text (2026-10-18), restored 2026-10-20. Its "probably, but not demonstrably" host wording is superseded by the current, more cautious status: host unresolved, likely blend.*

### 4.1 The frozen ephemeris is wrong at the level that matters for the Sector 111 test
`final_ephemeris.json`: 16 QLP times from S63/S64/S90/S100 (2023-2026) only (S10/S36/S37 discarded by `vet.py:122`), P = 3.2821840 +- 0.0000264 d,
chi2/dof 75/14. The project's all-data BLS in the same `report.json` gives P = 3.2822796 d (`bls_refine`), T0 = 2284.851168. The two
differ by 9.6e-5 d = 3.6 sigma of the frozen error. Checked against the data: at the frozen ephemeris every 2019-2021 product shows the
transit 65-100 min early (S36/S37 box fits dt = -81/-84 min; S10 deepest dips at -80 to -100 min); at the BLS ephemeris the same fits give
dt = +6 (S10), -21/-18 (S36/S37), +12 (S63/S64), +9 (S90), +18 (S100) min. A weighted linear fit of these seven sector-level offsets on top of the
BLS ephemeris gives P = 3.2823045 +- 0.000014 d (chi2 5.4 / 5), 4.6 sigma from the frozen value. Consequences at the Sector 111 epochs
(636-660): the frozen predictions are 22-25 min early relative to the BLS ephemeris and 40-45 min early relative to the refit. The
pre-registered outcome rule ("within +-3 sigma_min, and in any case within +-60 min, of >= 2 predicted times"; sigma_min = 10 min) would then
classify a real, on-time signal as "inconsistent", or at best recover it only through the +-60 min fallback. **A v2 freeze from all seven
sectors is required before the S111 data exist** (same for the sentence in `PREREGISTRATION.md` "conservative +-20 min window").

### 4.2 Independent extractions at the all-data ephemeris (`hlsp_depths_bls_120517801.json`, `s10_scan_120517801_bls.json`, `per_event_120517801_bls.json`)

| sector (year) | QLP SAP / DET | TARS | other | review fixed aperture r = 1.5 px (clean events) | dt (min) |
|---|---|---|---|---|---|
| S10 (2019, 1800 s) | 486 +- 214 | 513 +- 300 | ELEANOR-LITE 538 +- 183, TGLC 974 +- 405, T16-EPD2 339 +- 146 | 614 +- 258 (box scan: 664 +- 244 at dt 0, best 813 +- 249 at +10 min; QLP 531 +- 184 at -10; TARS 929 +- 224 at +10) | +6 |
| S36 (2021, 600 s) | 874 +- 213 | 769 +- 188 | - | 864 +- 151 | -21 |
| S37 (2021, 600 s) | 1003 +- 205 | 1115 +- 195 | - | 791 +- 152 | -18 |
| S63 (2023, 200 s) | 615 +- 185 / 650 +- 184 | 670 +- 196 | - | 819 +- 133 | +12 |
| S64 (2023) | 635 +- 188 / 620 +- 187 | 333 +- 182 | - | 442 +- 119 | +12 |
| S90 (2025) | 1064 +- 189 / 1114 +- 188 | 833 +- 189 | - | 978 +- 125 | +9 |
| S100 (2026) | 866 +- 121 / 894 +- 120 | not delivered | - | 563 +- 156 | +18 |

Fixed-aperture mean 759 +- 59 ppm, chi2 = 10.3 for 6 d.o.f.; before 2024 vs after 739 +- 71 vs 801 +- 103 ppm (0.5 sigma). The 2019 Sector 10
transit, never examined by the project (`vet.py:35`), is present at 2.7-3.6 sigma in the cutout, QLP and TARS at the all-data ephemeris and
absent at the frozen one. The signal is therefore stable in depth and phase over 2019-2026 and is not a sector-dependent systematic. (TESS-SPOC
produced no light curve at all for this star in any sector, which for a Tmag 11.4 target indicates crowding-based exclusion.) Per-event
aperture-vs-annulus checks: the dimming is confined to the aperture; S90 e452 and S100 e553 have background jumps and were excluded.

### 4.3 Crowding and what TRICERATOPS says (`triceratops_bls_120517801.json` = reference run; `triceratops_120517801.json` = frozen-ephemeris run)
TIC v8.2 contamination ratio 0.298; 629 Gaia sources within 150 arcsec, 343 of them bright enough to produce the signal with a < 100 % eclipse;
within the 2.5-px aperture TRICERATOPS counts the target at 67 % of the flux, TIC 936944659 (= Gaia G = 14.69 at 4.09 arcsec) at 4.7 %, and
eight further stars at 0.2-1.2 % each. Two runs. (a) Fold at the frozen ephemeris (which places the 2021 transits 66 min late and so smears the S36/S37 contribution):
FPP = 0.54, NFPP = 0.47, nearby-star probability spread over a dozen faint stars. (b) Fold at the all-data ephemeris (reference):
**FPP = 0.088, NFPP = 0.062**; TP 0.72, PTP 0.16, DTP 0.028, STP 0.021, NTP on TIC 936944659 (the G = 14.7 star) 0.011, NEB on
TIC 120517800 / 936944647 / 120517845 / 120517809 0.003-0.006 each; on-target scenarios sum to 0.94. The 8x drop between (a) and (b) is the
shape term: a correctly folded, flat-bottomed 2.2-h event disfavours the diluted deep eclipses the NEB scenarios need, and I was wrong to
expect the flux ratios alone to fix the answer. Run (b) meets Giacalone et al.'s "likely planet" criteria (FPP < 0.5, NFPP < 0.1) but not the
validation thresholds (FPP < 0.015, NFPP < 1e-3), and the residual 6 % nearby-star probability is split between the 4.2-arcsec star and four
stars at 15-40 arcsec. Caveats: 2.5-px circle, not QLP's aperture; no contrast curve; fold SNR ~12 (< 15, where FPP is a weak predictor).

### 4.4 Pixel-level (`pixel_review_120517801_bls.json`, `pixel_combine_120517801_bls.csv`, `per_event_psf_120517801_bls.json`, `plots/pixel_review_120517801_bls.png`)

| sector | loss-fit offset (px) | chi2(target) - chi2(free) | G = 14.7 at 0.18 px: dchi2 vs target / implied eclipse | per-event mean offset (px, sigma; event-scatter chi2/dof) | pixels > 4 sigma beyond 2 px |
|---|---|---|---|---|---|
| 10 (2019, 1800 s) | 1.02 +- 0.46 | 10.3 | -0.6 / 1.0 % | - | 4 (one hot pixel at 4.5 px dominates the map) |
| 36 | 0.46 +- 0.19 | 9.7 | +1.7 / 0.95 % | 0.56 (5.2; 37/14) | 0 |
| 37 | 0.38 +- 0.18 | 9.3 | -2.3 / 1.4 % | 0.49 (4.3; 13/14) | 0 |
| 63 | 0.33 +- 0.23 | 4.6 | -3.7 / 1.1 % | 0.23 (1.9; 52/14) | 0 |
| 64 | 0.70 +- 0.36 | 5.5 | +1.2 / 0.46 % | 0.45 (2.7; 98/14) | 1 |
| 90 | 0.65 +- 0.17 | 70.4 | -30.3 / 1.8 % | 0.36 (3.6; 34/16) | 10 (extended 5x5 loss blob) |
| 100 | 0.09 +- 0.28 | 0.2 | +0.2 / 0.95 % | 0.72 (6.4; 88/14) | 0 |

* The loss position is offset by 0.3-0.7 px in six of seven sectors, in different directions (S36 +x, S37 +y, S90 +y, S100 -y, S64 +x+y), with
  per-event scatter chi2 of 2-7x the degrees of freedom in S63/S64/S100. There is a ~0.5 px (10 arcsec) systematic floor in this field, as
  expected for a target that supplies only 67 % of the aperture flux and a PSF (sigma 0.7-0.8 px) that contains a dozen G = 15-19 stars.
* Sky-combined mean: 5.4 +- 1.3 arcsec from the target (4.2 sigma formal; scatter chi2 44 / 12, so ~2.2 sigma) and 1.7 arcsec (1.4 sigma formal)
  from the G = 14.7 star, which lies 3.6 arcsec north of the target; joint dchi2 (neighbour minus target) = -34, dominated by S90 (-30). The
  neighbour is mildly favoured by position, not significantly. S64, which the team quotes as "0.43 px on target", has one event with
  negative amplitude and a per-event chi2 of 98/14: it is a non-detection at pixel level.
* No far neighbour is indicated: nothing beyond 2 px reaches 4 sigma except the S90 extended blob (centred 0.65 px north of the target,
  not on any specific star) and a hot pixel in S10. An EB 20-60 arcsec away is excluded; anything within ~10 arcsec is not.
* Flux-weighted centroid shifts are 0.0-0.4 +- 0.15 mpx, 10x too small to separate the two stars (expected difference ~0.15 mpx).

### 4.5 The G = 14.7 star at 4.2 arcsec
Gaia DR3 5359600666906791424: G = 14.69, BP-RP 0.78, parallax 0.54 mas (1.85 kpc), RUWE 1.01, ipd_frac_multi_peak 1; GSP-Phot Teff 5883 K,
logg 4.12, R = 1.53 R_sun; FLAME M = 1.14, R = 1.76. An eclipse of 1.0-1.8 % on it is an M-dwarf companion (R ~ 0.15-0.2 R_sun) or a
Jupiter-sized body on a 1.5-R_sun G star at 3.28 d: both are common configurations. It is 0.18 px from the target; nothing TESS can do
separates them. The target: G = 11.99, parallax 5.561 +- 0.011 (179.8 pc), RUWE 0.93, RV 1.36 +- 0.83 km/s from 15 transits
(rv_chisq_pvalue 0.71, no stellar companion at 3.28 d), GSP-Phot Teff 5067 K, R 0.844, FLAME M 0.80 -> rho 1.33; expected T14(b = 0.45) 2.2-2.3 h
(observed 2.2 h), Rp = 2.5 R_Earth if on target and undiluted; with the 30 % contamination ratio, ~2.8 R_Earth.

### 4.6 Catalogues, phase tests (all-data ephemeris, `phase_tests_bls.json`)
VSX within 3 arcmin: Gaia DR3 5359601315431877888 (EB, P = 0.2918 d, 135 arcsec, G = 17.9, needs 19 %; 3.2823/0.2918 = 11.25, not an alias),
a delta Scuti/gamma Dor candidate at 149 arcsec, a 0.036-d variable at 167 arcsec; 915 TIC entries within 3 arcmin, no TOI/CTOI/TCE among
them. Phase tests: depth 775 +- 73 ppm; odd/even 783 +- 108 vs 768 +- 100 (0.1 sigma); secondary -29 +- 74 ppm; harmonics < 17 +- 19 ppm;
box vs sinusoid dchi2 104.

### 4.7 Ephemeris and pre-registration
The frozen fit itself was reproduced exactly (three 3-sigma outliers, epochs 225/229/547; S100 timing error -0.65 to -2.07 min at the five
S100 epochs; corrected fit T0 +1.3 min, P +0.1 sigma). tess-point: S111 (cam 4 CCD 3), S112, S113. The problem is 4.1, not arithmetic.
Required: re-freeze (v2) from all seven sectors including S10 and the 600-s sectors, with the all-data period; keep v1 on record. The right
wording for this object is "transit-like signal in a crowded field, host probably but not demonstrably TIC 120517801 (TRICERATOPS on-target
probability 0.94, pixel test inconclusive)"; it should not be counted as a planet candidate on TIC 120517801 in any public text until
seeing-limited photometry (section 7) assigns it.

---


> **Correction, 2026-10-20:** Section 4.3 misstated the Giacalone et al. “likely planet” NFPP threshold: it is 0.001, not 0.1. With FPP = 0.088 and NFPP = 0.062, this run meets neither their likely-planet nor validation criteria. Section 4.5's Gaia summary-RV probability does not exclude a stellar companion or provide a calibrated mass bound. The current interpretation is a likely blend with the host unresolved. Section 4.1's 22–45-minute v1/v2 timing range is also corrected: The frozen v2 predictions are 27.4–28.4 minutes later than v1 in S111, and 27.4–30.9 minutes later over S111–113. All these differences lie inside the corresponding written v1 3σ timing windows. Timing alone therefore does not establish that v1 would fail a real signal. The historical 22–45-minute range is not the frozen v1-to-v2 comparison reproduced here. The prospective test outcome remains unmeasured.

## 5. Methods audit against the literature (sources I fetched)

| requirement | source (fetched) | project status |
|---|---|---|
| Pixel-level localisation by PRF/PSF fit to difference images, with a quality metric, and a stated off-target criterion | LEO-Vetter (Kunimoto et al. 2025, https://arxiv.org/html/2509.10619v1, sec. IV.5): PRF fit to in-minus-out images, centroid accurate to ~0.2 px (5.2 arcsec) at high SNR, fails TCEs at offset > 15 arcsec, "prfFitQuality < 0.3 means that the fit results should not be trusted"; two known NEB TOIs survived its pixel test. Twicken et al. 2018 (https://arxiv.org/html/1803.04526v2, III.4.1): PRF centroiding, difference images used only when a quality metric exceeds ~0.7, out-of-transit centroid "subject to aperture crowding". Bryson et al. 2013 (https://arxiv.org/html/1303.0052v2): false positive declared when the source is offset by more than three standard deviations; "PRF model error and crowding contribute systematic errors"; the methods "cannot detect all background transit sources", e.g. a source "extremely close to the target star on the sky". | Flux-weighted positive-pixel centroid within 3.5 px, no PSF fit, no quality metric, bootstrap error only, J2000 positions, no background subtraction. Adequate for 20-60 arcsec blends (it caught nine); not adequate to claim sub-pixel exclusions. This review adds the PSF fit, the sky-coordinate combination and the per-event consistency check; the team should adopt them. |
| Depth vs aperture; centroid moving to a star >= 1 px away | Guerrero et al. 2021 (https://arxiv.org/html/2103.12538v2): QLP diagnostics are "centroid information, difference image comparison, multi-aperture comparison"; "Movement of the centroid in the difference images to a star 1 pixel away or more" and "If the transit depth increases with aperture size, the TCE signal usually comes from a nearby source"; 565/2241 TOIs (25 %) were false positives after follow-up. | Done (depth vs radius), but on raw, background-included apertures, where the decline with radius is dominated by sky and neighbours; not diagnostic for sources inside 1 px. |
| QLP apertures and normalisation | Kunimoto et al. 2022 (https://arxiv.org/html/2211.04386): QLP delivers an "optimal aperture" plus one smaller and one larger; global background via nebuliser/fitsh plus local background; no published per-sector aperture in the HLSP files (confirmed: no aperture keywords in the headers). MAST QLP page (https://archive.stsci.edu/hlsp/qlp): "As of Sector 94, QLP is now using the TESS-Gaia Light Curve (TGLC) methodology"; timing error orbits 210-220, sectors 99-104 "have not yet been redelivered" (page updated 2026-08-12; my HEAD checks confirm no v02 today). MIT QLP page (https://tess.mit.edu/qlp/): S74-79 timing error "up to roughly +-3.0 minutes", fixed in v02; bit 31 = QLP quality flag. | The project used QLP sector depths as an astrophysical depth test (REPORT 12.3 "two-level depth"), which this review shows is a normalisation effect. The project knew about the timing error (RESEARCH.md) but did not propagate it; now done here (harmless). |
| Second pipeline, all sectors | TESS-SPOC (https://archive.stsci.edu/hlsp/tess-spoc): delivered through Sector 85; Tmag <= 13.5 or H <= 10 or 2-min targets, max 10,000 per CCD per sector. TARS (https://archive.stsci.edu/hlsp/tars): S1-96, "unpopular causal pixel model", a rotation survey, no aperture/dilution description. | TESS-SPOC checked for S36/S37/S63 (S10 computed but unreported); TARS, TGLC, ELEANOR-LITE, T16 not used. TESS-SPOC has no product at all for TIC 120517801 (not selected; crowding), which the project did not note. |
| Statistical validation thresholds and limits | Giacalone et al. 2021 (https://arxiv.org/abs/2002.00691): validated if FPP < 0.015 and NFPP < 1e-3; (SNR < 15 caveat and Rp < 8 R_Earth range: earlier survey, RESEARCH.md items 1 and 5). | Not run for these three before this review. Results above: 80387959 FPP 0.047 / NFPP 0.010 and 120444365 FPP 0.041 / NFPP 0.000 ("likely planet", not validated); 120517801 FPP 0.088 / NFPP 0.062 at the all-data ephemeris (0.54 / 0.47 at the frozen one, which smears the 2021 sectors). |
| Ground-based NEB clearing | TFOP SG1 purpose: "identify false positives due to nearby eclipsing binaries" (https://tess.mit.edu/followup/). The 2.5-arcmin Gaia-star search and the "cleared / NEB" disposition scheme appear in a 2019 SG1 talk and in TFOP tables found by web search (Collins 2019 talk, arXiv:2202.00042) that I did not fetch; I cite them as unverified. | Not possible from TESS; the right next step for 120517801 and, at lower priority, for the G = 17.3 star near 80387959. |
| Gaia DR3 blend diagnostics | Gaia DR3 columns queried directly (ipd_frac_multi_peak, ipd_gof_harmonic_amplitude, RUWE, astrometric_excess_noise, non_single_star, phot_variable_flag, vari_* tables, RV variability statistics). | `vet.py:218` stores G, BP-RP, parallax, RUWE only. Added here; the RV-variability statistics are the one Gaia product that constrains the target-EB scenario at these periods, and they clear all three targets of stellar-mass companions. |

Not done by either the project or this review, and required before any public "candidate" claim beyond the ephemeris test: seeing-limited
photometry of a predicted transit in a small aperture (SG1-style NEB clearing of every Gaia star within 2.5 arcmin that could produce the
depth; for 120517801 that is ~340 stars, for 80387959 the G = 14.0 and G = 17.3 stars, for 120444365 none), speckle/AO imaging for companions
inside 1 arcsec, and reconnaissance spectroscopy. The citations above are pages I fetched myself; the commissioned literature sub-survey
arrived after the data work was finished and is reproduced in full in `LITERATURE_SURVEY.md` (all URLs fetched 2026-10-18). Its points that
bear on the three candidates:

### 5.1 Addendum from the literature sub-survey (`LITERATURE_SURVEY.md`)
* **Pixel-test reach.** SPOC DV on TESS treats centroid offsets as not significant at 3 sigma if < 7.5 arcsec (Guerrero et al. 2021,
  https://arxiv.org/pdf/2103.12538); LEO-Vetter fails only Delta-theta > 15 arcsec and quotes ~0.2 px (5.2 arcsec) accuracy at high SNR
  (https://arxiv.org/pdf/2509.10619); Transit-APP (Bryson & Kunimoto 2025, https://ntrs.nasa.gov/api/citations/20250003461/downloads/transitApp.pdf)
  distinguishes sources ~0.2 px apart only at high SNR. My sector-to-sector floors (0.1-0.2 px for 80387959 and 120444365; ~0.5 px for
  120517801) and the 2-5 arcsec combined positions are consistent with that literature; no pixel method reaches the 4.2-arcsec star of
  TIC 120517801, as section 4 says. DAVE (Kostov et al. 2019, https://arxiv.org/pdf/1901.07459) warns that bright field stars in the
  aperture can "capture the out-of-transit PRF fit and thus result in a false centroid offset", which is the right reading of the S90 blob.
* **QLP apertures and dilution.** QLP uses five circular apertures of 1.75, 2.5, 3.0, 3.5 and 8.0 px, chosen per magnitude bin, and deblends
  with the TIC constant flux and difference-image variability (Guerrero et al. 2021); from Sector 94 the dilution system is TGLC/Gaia
  (https://tess.mit.edu/qlp/, Han & Brandt 2023 https://arxiv.org/abs/2301.03704). Mills & Fabrycky 2017 (https://arxiv.org/pdf/1606.04485)
  describe exactly the season-dependent dilution mechanism: "a given pixel or group of pixels in the aperture sum might observe a slightly
  different group of stars causing the transit depth to change". This is the mechanism behind section 2.1 and supports using a single
  fixed aperture for any cross-sector depth comparison. It also justifies my 2.5-px TRICERATOPS aperture as being inside QLP's range for
  these magnitudes.
* **Sector 100 attitude-control test (SPOC DRN 137,
  https://archive.stsci.edu/missions/tess/doc/tess_drn/tess_sector_100_drn137_v01.pdf):** a new attitude control algorithm was tested in the
  last 27 h of Sector 100 and reaction wheels were calibrated in the first ~1 h, with elevated pointing scatter. Checked against the cutout
  time span (BTJD 4073.99-4100.47): no TIC 80387959 transit falls in either window (epochs 428-433 at 4078.10-4099.06; the next at 4073.91 is
  before the data start); TIC 120517801 epoch 553 (4099.95) is inside the last-27-h window and is the S100 event my per-event filter already
  excluded for its background jump (section 4.2). TIC 120444365 has no S100 data. Sector 104 ACS 5.11 windows (DRN 142) do not concern these
  stars (no S104 data).
* **SG1 practice at < 1 ppt** (Collins 2019 SG1 talk, https://tsc.mit.edu/2019/talks/Karen%20Collins.pdf): search all Gaia stars within
  2.5 arcmin with ~1.5-arcsec apertures; the achievable disposition at this depth is "cleared planet candidate" (no NEB found), not an
  on-target detection; ground sensitivity threshold ~1 ppt. This sets what section 7 can deliver: for 120517801 a CPC/PNEB/NEB outcome on
  the 4.2-arcsec star is realistic only under good seeing with small apertures; a 750-ppm on-target detection is at the limit.
* **Gaia blind zone** (Penoyre et al. 2022, https://arxiv.org/pdf/2202.06963; VaTEST III, https://arxiv.org/pdf/2311.00688): Gaia resolves
  pairs at >~ 2 arcsec, the IPD flags act from ~1 arcsec down to ~0.18 arcsec, and ipd_frac_multi_peak <= 2 is treated as single. All three
  targets have ipd_frac_multi_peak = 0 and RUWE < 1.0, so companions at 0.2-1 arcsec are disfavoured but not excluded; the TOI-864.01 preprint
  (https://arxiv.org/html/2601.02171v4, not refereed) is the cautionary example of a 0.04-arcsec companion behind RUWE 1.18 and flat
  centroids. Gaia DR3 EB-catalogue completeness is 25-50 % (Mowlavi et al. 2023, https://arxiv.org/pdf/2211.00929), so the absence of the
  neighbours from `vari_eclipsing_binary` is weak evidence, as stated in sections 2.4/3.4/4.6.
* **Priors.** NEBs are the largest false-positive class in a 23-arcsec-pixel survey (34 % of 1,128 KELT false positives, Collins et al. 2018,
  https://arxiv.org/pdf/1803.01869) and ~25 % of Prime-Mission TOIs were false positives (Guerrero et al. 2021); the small-planet occurrence
  for K dwarfs is ~1.2 planets per star at 1-2.83 R_Earth, P < 200 d (Kunimoto & Matthews 2020, https://arxiv.org/pdf/2004.05296). No
  published NEB fraction for QLP/FFI TOIs vs galactic latitude was found by the sub-survey either.
* **Validation practice** (Hord et al. 2024, https://arxiv.org/pdf/2308.09617; VaTEST III): contrast curves, several TRICERATOPS runs
  averaged, SG1 dispositions and non-V-shaped fits are prerequisites; none of the three objects has any of these yet, which is why the
  FPP numbers in this review are indicative only.

---

## 6. Corrections to the project's claims and code (file:line)

1. **REPORT.md 12.3, PREREGISTRATION.md (80387959), DECISIONS 36:** "two-level depth ... unexplained; treat the depth as uncertain by a
   factor 1.5". Not supported: fixed-aperture depths are constant (chi2 10.2/5; early-late 32 +- 73 ppm). Replace with: QLP per-sector
   normalisation differs between the FIPHOT-era and later sectors; the depth from a single-aperture extraction is 687 +- 36 ppm before dilution.
2. **REPORT.md 12.3 (80387959):** "G = 17.3 neighbour at 8 arcsec excluded at 4.8/2.8/4.3 sigma". The sector-to-sector scatter of the loss
   position (chi2 52/10 here; the team's own three sectors differ by 0.1-0.3 px) is 2.3x the bootstrap error; the exclusion is ~2.7 sigma
   combined. The G = 14.0 star is excluded at ~4 sigma. State both.
3. **REPORT.md 12.3 (120517801):** "Pixel centroid on target (0.07-0.43 px)". S64 is a non-detection at pixel level (per-event chi2 98/14,
   one event with negative amplitude); S90 is 0.65 +- 0.17 px off in my PSF fit with an extended loss map; offsets of 0.3-0.7 px in different
   directions in six of seven sectors. Replace with: "pixel test inconclusive; loss-position systematic floor ~10 arcsec in this field; the
   G = 14.7 star at 4.2 arcsec is mildly favoured by position (1.4 sigma)". Add: TRICERATOPS NFPP = 0.062 at the all-data ephemeris (0.47 at
   the frozen one).
4. **`scripts/vet.py:35` and `:249`** (`if len(t) < 1000: continue`): drops Sector 10 (1800 s, ~1,100 points) for both southern stars. REPORT
   12.3 "24 transits in S10/S36/S37/S63/S90/S100" is wrong for the count (S10 contributed nothing to vet.py) and the per-sector/per-year tables
   lack 2019. Use a cadence-aware threshold (e.g. > 10 d of data).
5. **`scripts/vet.py:122`** (`min_pts = 15` in-transit points) and **`scripts/prereg_candidate.py:13`**: transit times exist only for 200-s
   sectors, so the frozen ephemerides ignore 2018-2021 data. For TIC 120444365 this yields P = 5.148082 d vs the all-data 5.148179 d (2.6 sigma;
   the 2018-2023 transits sit 50-90 min early on the frozen ephemeris). Re-freeze a v2 from all sectors plus the SPOC 2-min S29 times. For
   TIC 120517801 it yields P = 3.282184 d vs the all-data 3.282280 d (3.6 sigma) and a seven-sector refit 3.282305 d (4.6 sigma); the frozen
   S111 predictions are 22-45 min early, outside the +-20 min window: re-freeze v2 now. For TIC 80387959 the two periods agree at 1.8 sigma
   (11-12 min at S111); fix the same way.
6. **`scripts/vet.py:57`** (`exp_time = 120 / 86400` in `transit_model`): the batman supersampling uses the 2-min exposure for QLP data at 200,
   600 and 1800 s. For 600-s data the smearing of a 2.2-h transit's ingress is ~0.1 h, which biases a/R* and b slightly; pass the real cadence
   (`np.median(np.diff(t))`).
7. **`scripts/ffi_pixel_test.py:21`**: no background subtraction before the per-pixel differences and the depth-vs-radius curve; the
   sky-dominated decline of depth with radius is then read as "field dilution". Subtract a per-cadence background (faintest 30 % of pixels or an
   annulus). **`:41`**: the 3.5-px restriction and positive-only weighting hide any source beyond 70 arcsec and bias toward the centre; report
   the full-cutout significance map and the PSF-fit position with chi2 at every neighbour. **`:89-90`**: no proper-motion correction (0.06-0.08 px
   for these three; 0.13 px for TIC 89247735 earlier).
8. **`scripts/tessspoc_check.py` / REPORT 12.3 / DECISIONS 36:** the S10 (2019) TESS-SPOC depth 953 +- 94 ppm is in `tessspoc_check.json` and in
   the "combined 831 +- 53" but the text says S36/S37/S63 only; TESS-SPOC coverage ends at S85 (page), so "no S90/S100 products" is right.
9. **`scripts/known_nearby.py:6`**: reads a local `known_signals.csv` snapshot; no VSX/Gaia-variability/SIMBAD check. Here: the only EBs within
   3 arcmin of any target are Gaia EB candidates at 134-135 arcsec with non-aliased periods; nothing changes, but the check should be live.
10. **REPORT 12.3 (120444365):** "R 0.84 R_sun, Rp 2.45 R_Earth" uses the QLP-header radius; TIC v8.2 (MAST) and Gaia GSP-Phot/FLAME give
    0.756-0.764 R_sun, Rp = 2.2 R_Earth. "rho 1.78x catalog" is not a tension: a/R* has a 25-50 % uncertainty in the MCMC.
11. **PREREGISTRATION.md (all three):** the predicted UTC times are from QLP v01 transit times; the S100/S103/S105 timing error shifts the
    ephemerides by 0.05 / -0.8 / +1.3 min (T0) and < 0.1 sigma (P). Add one sentence and the corrected T0 so that an observer is not surprised when
    v02 files appear. Note also that S105 shows the same drift pattern as S103 although MAST lists the error as ending with orbit 220.
12. **REPORT 12.3 (120444365):** "blind 4/4" is 4 of 5 years: the 2018 holdout had no covered predicted transit (`report.json` blind_tests.2018:
    ok = false); and the per-sector S2/S29 depths at the frozen ephemeris (578 +- 159, 678 +- 172) are each < 4 sigma partly because the frozen
    period places those transits 1 h early; at the all-data ephemeris they are 751 +- 144 and 766 +- 178 (fixed aperture) / 892 +- 129 (2-min).

---

## 7. Cheapest next observations, ranked

**TIC 120444365** (first priority: the only object that is both clean and isolated)
1. Wait for QLP S106 (expected late October 2026) and apply the pre-registered test; also run it on a TESScut extraction so that the result
   does not depend on QLP's S106 normalisation. Re-freeze a v2 ephemeris from all sectors now (before the release) and deposit both hashes.
2. One ground-based transit at ~1 mmag precision (0.4-1 m telescope, 2.0 h event, Tmag 11.1, Dec -42): confirms depth on the target
   (no NEB clearing needed; nothing within 60 arcsec can mimic it). Northern spring/southern spring evenings from Chile/South Africa/Australia.
3. Speckle or AO imaging (SOAR HRCam / Zorro) for companions inside 1 arcsec: removes the remaining STP/DTP term in TRICERATOPS.
4. Reconnaissance spectroscopy (CHIRON/FEROS) for stellar parameters and a few-hundred-m/s RV check.

**TIC 80387959**
1. Same S111-S114 TESS test as pre-registered, but extract from TESScut with a fixed aperture rather than relying on the QLP depth.
2. A ground-based transit with 2-3 arcsec seeing and defocus-free apertures small enough to separate the G = 14.0 star at 13.7 arcsec and,
   if seeing allows, the G = 17.3 star at 7.6 arcsec (needs 22-28 %: trivially detectable in a 0.4-m telescope if it is the source). This single
   observation settles the only remaining blend scenarios with > 1e-3 probability.
3. Speckle imaging for sub-arcsecond companions; spectroscopy.

**TIC 120517801**
1. Seeing-limited photometry of a predicted transit (Tmag 11.4, P = 3.28 d, 2.2 h, Dec -53) with light curves of every Gaia star within 2.5 arcmin
   brighter than G ~ 18.5 (SG1 NEB-check style). The G = 14.7 star at 4.2 arcsec needs ~1.5 arcsec seeing and a small aperture to separate;
   a 1-2 % eclipse on it would be obvious. This is the only observation that can turn the object into a candidate on a specific star.
2. Re-freeze the ephemeris (v2) from all seven sectors before S111; with v1 as frozen the TESS test would likely return "inconsistent" for a
   real signal (section 4.1). Then the S111-S113 data test the ephemeris only.
3. Until 1 is done, keep the object out of any public candidate list (host undetermined; TRICERATOPS NFPP 0.06, 60x above the validation
   threshold, with the 4.2-arcsec star unresolvable by TESS).

---

## 8. What could not be done
* The QLP aperture per sector is not published; TRICERATOPS and the dilution corrections use a 2.5-px circle.
* No contrast curves exist for any of the three stars (nothing on ExoFOP; none of them has a TOI/CTOI).
* S111 2-min target lists are not public; S106 QLP is not released.
* The literature sub-survey arrived after the data work; it is included as `LITERATURE_SURVEY.md` and summarised in section 5.1. It found no
  published NEB fraction for QLP/FFI TOIs, no NEB rate vs galactic latitude, and no 2024-2026 paper on TESS pointing degradation beyond the
  S100/S104 DRN notes.
* Red-noise-aware per-sector depth errors (e.g. time-averaging beta factors) were not computed; the per-event scatter chi2 values given
  above are the proxy, and they indicate ~1.5-2.5x underestimates for the 600-s and crowded-field data.

## 9. File index
* `scripts/qlp_time_check.py`, `qlp_time_check2.py`, `timing_propagation.py` -> `qlp_time_check*.json`, `timing_propagation.json`, `plots/qlp_time_offsets.png`
* `scripts/ephemeris_check.py` -> `ephemeris_check.json`
* `scripts/gaia_retry.py`, `catalogs_vizier.py` -> `gaia_dr3.json`, `gaia_<tic>_150as.csv`, `catalogs_vizier.json`, `tic_<tic>_180as.csv`
* `scripts/mast_products.py` -> `mast_products.json` (all MAST products per star; QLP v01/v02 URL checks)
* `scripts/tesscut_fetch.py` -> `data/tesscut/` (15x15 cubes, all sectors)
* `scripts/hlsp_depths2.py`, `hlsp_depths_bls.py`, `hlsp_depths_bls_120517801.py` -> `hlsp_depths.json`, `hlsp_depths_bls_120444365.json`, `hlsp_depths_bls_120517801.json`
* `scripts/pixel_review.py`, `pixel_combine.py`, `per_event.py`, `per_event_psf.py` -> `pixel_review_<tic>[_bls].json`, `pixel_combine_<tic>[_bls].csv/json`, `per_event_<tic>.json`, `per_event_psf_<tic>.json`, `plots/pixel_review_<tic>[_bls].png`
* `scripts/phase_tests.py`, `phase_tests_bls.py` -> `phase_tests.json`, `phase_tests_bls.json` (120517801 at the all-data ephemeris)
* `scripts/s10_scan_120517801.py`, `s10_scan_120517801_bls.py` -> `s10_scan_120517801.json` (frozen ephemeris), `s10_scan_120517801_bls.json` (all-data ephemeris)
* `scripts/stellar_summary.py` (prints the stellar/catalogue/TRICERATOPS summary used in sections 2.4, 3.4, 4.3)
* `LITERATURE_SURVEY.md`: the commissioned literature sub-survey (verbatim)
* `scripts/triceratops_review.py`, `triceratops_review_bls.py`, `triceratops_review_bls_120444365.py` (run in `.venv_tri`; the `_bls` runs fold at the all-data ephemeris and are the reference numbers) -> `triceratops_<tic>.json`, `triceratops_bls_<tic>.json`, `*_probs.csv`, `*_stars.csv`; the `*_gaia_background.csv` files are TRICERATOPS working files
