# External adversarial review of `results/REPORT.md` (TESS candidate search)

Reviewer: external consultant (independent of the team). Date: 2026-10-17 (UTC evening).
Scope: claims 1 (TIC 89247735, 18.32-d, 1 %), 2 (TIC 317134140, 0.5719-d, 185 ppm) and 3 (methodology / statistics).
Nothing under `results/` outside this directory was modified. All scripts, data pulls, JSON outputs and plots are in
`results/external_review/` (scripts: `*.py`; outputs: `*.json`, `observability_89247735.csv`; plots: `plots/`; downloaded
data: `data/`).

---

## 1. Verdicts

### TIC 89247735 (SCR J1820-4533), P = 18.323 d, 1.0 % — **SURVIVES, and is stronger than the report states**
The most consequential finding is not damaging: the team's pipeline *missed a fourth transit*. Sector 93 contains a second
predicted epoch (epoch 118, BTJD 3830.345, 0.49 d after the sector start, inside the scattered-light ramp) whose 72 cadences
all carry the QLP-specific quality bit 2^30 and were therefore dropped by `QUALITY == 0` (`scripts/tsearch.py:45`). The raw
QLP `SAP_FLUX` at those cadences shows a 1 %-deep, 4-h, flat-bottomed dip with no background or centroid excursion
(`plots/qa_S93_epoch-20.png`), and the independent TARS HLSP pipeline shows the same dip. Timed with the team's own
transit shape, this never-used event falls **+3.0 to +3.5 min from the 3-event frozen prediction** (prediction 1σ ≈ 3 min,
measurement 1σ ≈ 2 min), i.e. it is a genuine out-of-sample confirmation of the ephemeris that was available inside the
team's own data. The two S93 events are consecutive transits, so the period is now *measured directly* within one sector:
tc(119) − tc(118) = 18.3219 ± 0.0021 d (QLP SAP), 18.3220 ± 0.0020 d (TARS), 18.3242 ± 0.0017 d (own cutout photometry),
all agreeing with the stitched 18.3231 d; until now the period rested on the coprime-epoch inference. With four events at
epochs 79, 118, 119, 138, every period alias longer than 18.32 d — including the 36.65-d twin-eclipse binary loophole left
open in §8.3 — is closed by data rather than by argument. Because the fourth event lies entirely in flagged scattered-light
cadences, I ran a field control: of 190 other S93 stars on the same camera/CCD with local QLP files, none shows a ≥ 0.8 %,
> 5σ box at the same time whose off-window residuals are below half its on-window depth; the control distribution of
on-window box depths has a robust σ of 1,100 ppm, making the target's 10,300 ± 460 ppm a 9σ outlier, and the strongest
control "dips" are ramps or a V-shaped eclipsing binary (`plots/control_stars_s93.png`). The event is not field-wide.
Independent checks that could have killed it did not: TARS (independent FFI photometry) reproduces all events at the same
depth; the S13 gap claim is true in three products (QLP, TESS-SPOC, ELEANOR-LITE: zero cadences within ±2 h); the 144-epoch
ASAS-SN V light curve (2016–2018) has only 3 in-transit epochs (all faint, but at +38 ± 7 mmag too deep for an 11-mmag
transit; uninformative); a PSF fit to the TESScut flux-loss map rejects the G = 15.5 neighbour by
Δχ² = 83–214 in each sector and the team's centroid estimator proves nearly unbiased under injection. Remaining weaknesses:
no catalog entry, no spectroscopy, nature (planet / brown dwarf / late-M) unknown; and the pre-registered 2026-10 to 2027-02
epochs are **unobservable from the ground** (target within ~2 h of the Sun; see §5) — the first fully observable epochs are
2027-06-25 and 2027-08-19 from Chile. A single 1 %-dip is also mimicable by an unresolved (< 1″) eclipsing companion of the
target, which no TESS pixel test can exclude.

### TIC 317134140 (TOI-2514), P = 0.5719 d, ~185 ppm — **WOUNDED (unchanged by this review; no new kill, no new support)**
The team's own §7.1 already removed the season-holdout tests as evidence. My checks: the signal is box-shaped rather than
sinusoidal (Δχ² vs flat: box 104, pure sinusoid 31, sinusoid+harmonic 47; `analysis_317134140.json`), there is no stellar
rotation signal or harmonic series at 0.572 / 1.144 / 1.716 d in the raw PDCSAP or SAP of any sector (sinusoid amplitudes
35–140 ppm at noise level), the depth is insensitive to the detrending window from 0.5 to 2 d, and the masked-detrend
random-phase null that the holdout test relies on is *not* biased (null σ 37/51/37/44 ppm team-style vs 41/52/30/40 ppm with
a fair per-phase mask). Nothing instrumental was found. The single most damaging number remains the per-sector depth
inconsistency: χ² = 16.1 for 5 d.o.f. (p = 0.007) for a constant depth using the report's own per-sector values (S32 56 ± 36
ppm where ≈185 was predicted), and the S98 SPOC centroid shift (0.34 ± 0.07 mpx, 5.3σ) is 3× the on-target expectation of
≈0.10 mpx for that sector (report quotes only the four-sector average). No SPOC TCE exists in any of the 133 local tables
for this star, which is expected: a 185-ppm, 1.5-h signal has a single-sector MES ≈ 5–6, below the 7.1 threshold. Verdict:
plausible, unproven, decided by S108–S110 as the team says. One cheap new lever: ExoFOP lists a 291-min CHEOPS visit of
TOI-2514 on 2023-01-06 (CHATEAUX filler programme) — a ~46 % chance of containing a predicted 0.5719-d transit at ~100 ppm
precision per 1.5 h; the team should ask the CHEOPS GTO for it.

### Methodology (search, inverted null, blind tests, pixel tests) — **SURVIVES with corrections**
The pipeline, SDE, ranking and null-calibration code do what the report says, with one systematic blind spot (quality-flag
masking of QLP bit 2^30 removes real data in scattered-light ramps; this hid the fourth transit above and will hide
transits near orbit starts in every Pool-B star) and several small inconsistencies listed in §3. The inverted-null
calibration is internally consistent but conservative in one direction (null uses best-of-top-3 peaks, real ranking uses the
top peak only). The season-holdout test has a small leak (`vet.py:174`), but the team already demoted that test. The
flux-loss centroid estimator's bias was quantified by injection: ≤ 0.06 px, far smaller than the 0.35–0.46 px target–neighbour
separation, so the "on-target" claim is a real claim.

---

## 2. Tests run (data source, numbers, errors)

### 2.1 TIC 89247735 — local data quality and the missing fourth transit (`qa_events_89247735.py`, `four_events_89247735.py`, `s93_two_events.py`)
Frozen ephemeris used throughout: T0 = BTJD 4196.80732, P = 18.323126 d, duration 4.0 h (from `PREREGISTRATION.md`).

| sector | epoch | predicted tc (BTJD) | cadences ±1 d (Q==0) | in-transit cadences (Q==0) | SAP depth Q==0 | SAP depth all flags |
|---|---|---|---|---|---|---|
| 13 | −138 | 1668.216 | 51 (32) | 0 (0) | — | — (orbit gap 1667.68–1668.64) |
| 66 | −59 | 3115.743 | 864 (864) | 72 (72) | 10,174 ppm | 10,174 |
| 93 | **−20** | **3830.345** | 643 (376) | **72 (0)** | — | **9,899 ppm** (all 72 flagged 2^30) |
| 93 | −19 | 3848.668 | 864 (836) | 72 (71) | 10,971 | 11,023 |
| 104 | 0 | 4196.807 | 864 (461) | 72 (44) | 10,289 | 10,373 (28 of 72 flagged 2^30) |

(Epoch numbering here is relative to epoch 138 = S104; the team's absolute epochs are 79, 118, 119, 138.)

Raw-column plots (`plots/qa_S*_epoch*.png`): every event is a box in raw `SAP_FLUX`; `SAP_BKG`, `SAP_X`, `SAP_Y` show no
feature at the dips. The epoch-118 event sits on the decaying scattered-light background of the orbit start (SAP_BKG falling
from 35,000 to 3,000 e-/s over the preceding 12 h) — that is why QLP flagged it. Nearest momentum dumps: 83.8 h (S66),
−11.7 h (S93 epoch 118), 34.0 h (S93 epoch 119), 33.1 h (S104); no event coincides with a dump.

Timing of all four events with the team's batman shape (Rp/R★ 0.0996, a/R★ 30.9, b 0.44) on a local quadratic baseline:

| product | epoch 79 (S66) | epoch 118 (S93) | epoch 119 (S93) | epoch 138 (S104) |
|---|---|---|---|---|
| QLP SAP, all flags: O−C vs frozen ephemeris | −0.3 ± 1.9 min | **+3.5 ± 2.5 min** | +1.7 ± 1.8 | −4.5 ± 1.6 |
| QLP SAP: box depth (ppm) | 11,099 ± 313 | 11,112 ± 402 | 11,520 ± 299 | 10,606 ± 249 |
| TARS: O−C | −2.2 ± 1.5 | **+3.0 ± 2.2** | +1.3 ± 1.8 | (no S104 product) |
| TARS: box depth (ppm) | 11,154 ± 256 | 9,847 ± 334 | 12,191 ± 325 | — |
| own 1.5-px TESScut photometry, annulus background: O−C | — | +1.1 ± 1.8 | +2.6 ± 1.6 | — |
| own 1.5-px photometry: depth scale vs team model | — | 1.014 ± 0.032 | 0.982 ± 0.028 | — |

* 4-event linear ephemeris (QLP SAP): P = 18.323085 ± 0.000030 d, T0 = 4196.80599 ± 1.3 min, χ² = 8.5/2 (timing errors
  underestimated by ~2× as the team also found); TARS 3-event: P = 18.323199 ± 0.000036. Both consistent with the frozen
  18.323126 ± 0.000058. The frozen predictions move by < 1 min through epoch 163 if the fourth event is added.
* Direct period from the consecutive S93 pair: tc(119) − tc(118) = 18.3219 ± 0.0021 d (QLP SAP), 18.3220 ± 0.0020 (TARS),
  18.3242 ± 0.0017 (own 1.5-px photometry) vs 18.3231 stitched: the period no longer depends on the alias argument.
* Field control for the flagged epoch-118 window (`control_stars_s93_v2.py`, `control_stars_s93_v2.csv`,
  `plots/control_stars_s93.png`): all 770 local S93 QLP stars covering BTJD 3830.345 ± 0.5 d, raw `SAP_FLUX` with all flags,
  cubic baseline × 4-h box fitted ON (at the predicted time) and OFF (−0.35, +0.35, +0.6 d). Target: ON 10,309 ± 464 ppm
  (22σ), OFF mean 1,305, OFF max 5,311 ppm (the ramp alone produces up to 0.5 % spurious box depths, which is why the
  depth of this event is less certain than the others). Same camera/CCD controls (N = 190): ON median −80 ppm, robust
  σ 1,116 ppm; 4 stars have ON > 5,000 ppm at > 5σ but every one has OFF-window "depths" of the same size (ramps; one is a
  V-shaped EB, TIC 85639522); 0 of 190 (5 of 770 on all CCDs, all ramp-dominated) have ON > 8,000 ppm, > 5σ and
  OFF max < ON/2. A field-wide dip at this time is excluded; the target's event is a 9σ outlier in the control
  distribution. The earlier crude test (`control_stars_s93.py`, quadratic baseline only) is superseded by this one.
* Odd/even with four events: QLP SAP odd (79, 119) 11,319 ± 216 vs even (118, 138) 10,746 ± 212 ppm, 1.9σ; TARS 4.4σ but
  driven solely by epoch 118's background treatment (QLP SAP and TARS disagree by 2.4σ on that one event). The same-aperture,
  own-photometry comparison of the two S93 events gives depth ratio 1.03 ± 0.04 (0.8σ) at r = 1.5 px and 1.00 ± 0.07 at
  r = 2.5 px. Odd/even is consistent with equal depths; the 2σ-level excess of odd over even in QLP DET/SAP is not
  significant but should be re-tested with the next transit.

### 2.2 TIC 89247735 — independent TESS pipelines (`hlsp_check_89247735.py`)
MAST holds, besides QLP: TESS-SPOC (S13 only), GSFC-ELEANOR-LITE (S13 only), TARS (S13, S66, S93; HLSP "TESS All-Sky
Rotation Survey", Boyle, DOI 10.17909/2sff-fn29, 200-s cadence). No TESS-SPOC/TGLC/DIAmante products exist for S66/S93/S104.
TARS depths at the frozen ephemeris (simple in/out box): S66 10,552 ± 234, S93 epoch 118 8,766 ± 311, S93 epoch 119
11,296 ± 280 ppm. S13: TESS-SPOC, ELEANOR-LITE and TARS all have 0 cadences within ±2 h of the predicted epoch (4 within
±12 h). The team's "2019 neither confirms nor contradicts" is correct.

### 2.3 TIC 89247735 — pixel-level test, bias of the team's centroid estimator (`pixel_injection_89247735.py`, `pixel_injection_89247735.json`, `plots/pixel_review_S*.png`)
Using the cached 11×11 TESScut cubes (S66, S93, S104; same cadences and the same per-event local baselines as
`ffi_pixel_test.py`):

| sector | PSF σ (px) | target–neighbour sep. (px, PM-corrected) | team centroid vs J2000 target / vs PM-corrected target / vs neighbour (px) | PSF-fit loss position vs PM target / vs neighbour (px) | Δχ² (neighbour − target), N pix |
|---|---|---|---|---|---|
| 66 | 0.61 | 0.36 | 0.164 / 0.168 / 0.345 | 0.12 ± 0.06 / 0.40 | **+214**, 37 |
| 93 | 0.59 | 0.35 | 0.036 / 0.103 / 0.424 | 0.13 ± 0.06 / 0.42 | **+194**, 37 |
| 104 | 0.53 | 0.34 | 0.157 / 0.031 / 0.346 | 0.09 ± 0.07 / 0.35 | **+83**, 39 |

Injection (fake in-transit cadences = resampled out-of-transit cadences minus a Gaussian-PSF point-source loss of the fitted
amplitude; 5 realisations each):

| injected at | team estimator lands (px from J2000 target) S66 / S93 / S104 | team estimator, px from injected position | PSF fit of the injected map, px from injected position | PSF fit, px from PM-corrected target |
|---|---|---|---|---|
| target (PM-corrected) | 0.131 / 0.114 / 0.185 | 0.02 / 0.03 / 0.05 | 0.011 / 0.004 / 0.044 | 0.01 / 0.00 / 0.04 |
| G = 15.49 neighbour | **0.428 / 0.410 / 0.439** | 0.04 / 0.05 / 0.06 | 0.008 / 0.004 / 0.032 | **0.35 / 0.35 / 0.33** |
| target (J2000, team's position) | 0.023 / 0.031 / 0.062 | same | 0.013 / 0.003 / 0.050 | 0.12 / 0.14 / 0.11 |

(An earlier version of the injection script fitted the real map instead of the injected one in the PSF-fit column; fixed
and rerun — the JSON now holds the corrected values. The team-estimator columns were unaffected.)

Conclusions: (i) the positive-depth-only, 3.5-px-circle estimator (`ffi_pixel_test.py:41-43`) is biased toward the circle
centre by only 0.02–0.06 px for a source at the neighbour's position; the report's statement that a neighbour-sourced dip
"would sit at 0.46 px" is right to within 0.05 px. The PSF fit recovers an injected neighbour-sourced loss at 0.33–0.35 px
from the target (its true separation) with 0.01–0.03 px error, versus the measured 0.09–0.13 px for the real loss map:
the real signal sits where a target-sourced injection lands and 0.2–0.3 px (5–8 statistical σ) from where a neighbour-sourced
one lands. (ii) The team used the J2000 catalogue position; the star's proper motion
(−39, −106 mas/yr) moves it 0.13 px toward the south-west, i.e. toward the neighbour, by 2023–2026 — after correction the S104
offset drops from 0.16 to 0.03 px and the S93 one rises from 0.04 to 0.10 px; the WCS-vs-image-fit systematic is 0.16–0.17 px.
(iii) The measured loss position is 0.03–0.17 px from the target and 0.35–0.42 px from the neighbour in all three sectors,
and a free-position PSF fit prefers the target over the neighbour by Δχ² = 83–214. The neighbour is excluded as the source.
The fitted loss-map PSF width (0.73–0.78 px) is slightly broader than the stellar PSF (0.53–0.61 px), which is the expected
effect of the 10-min cadence jitter, not of a second source. (iv) Not excludable by any TESS test: a companion within ≲ 1″
of the target.

### 2.4 TIC 89247735 — archival ground-based photometry
* **ASAS-SN Sky Patrol v2** (`asassn_fetch_89247735.py`): the star is in the catalogue (asas_sn_id 541166660506) but the
  light-curve service is down for maintenance (banner dated 2026-10-13; the client fails with `n_servers = 0`). Not obtainable
  today; the script is ready to re-run (expected ~2,000–3,000 g+V epochs 2014–2026 → ~25 in-transit points → a 3–5σ test).
* **ASAS-SN v1 photometry database** (`asassn_fold_89247735.py`, `asassn_v1_fold_89247735.json`, `plots/asassn_v1_fold.png`):
  144 V-band epochs, camera "be", HJD 2457457–2458382 (2016-03 to 2018-09), mean V = 12.29, rms 12.6 mmag. Folded on the
  frozen ephemeris (extrapolation uncertainty back to 2016 ≈ 12 min): 3 in-transit epochs, dmag +17, +30, +59 mmag, in−out
  = +37.6 ± 6.5 mmag, where a 1 % transit predicts +11 mmag and no transit 0. The three points are all faint, but the mean is
  2.3–4σ *too deep* for the transit (ASAS-SN's faint tail is non-Gaussian: 2.8 % of all 144 points are > +17 mmag). Empirical
  bootstrap (draw 3 of 144 points, 20,000 times): p(in−out ≥ 37.6 mmag) = 0.0003, p(≥ 11 mmag) = 0.066. Conclusion:
  three faint points, too deep to be the transit, uninformative either way. Blind BLS (1–40 d) top peak 2.91 d, SNR 6.6,
  with 18.32 d at SNR 5.1 — uninformative with 144 points.
* **SuperWASP (NASA Exoplanet Archive `superwasptimeseries`)**: no source within RA 275.205–275.245, Dec −45.575 to −45.548;
  the DR1 release does not cover this star. **KELT**: fields are listed only by name (N02…S38); coverage of Dec −45.6 not
  established. **ASAS-3**: server returned HTTP 500. **Gaia DR3 epoch photometry**: none (no variability flag). ATLAS, NGTS:
  no public forced photometry without an account.

### 2.5 TIC 89247735 — catalogues, literature, astrophysics
* SIMBAD: SCR J1820-4533 = TIC 89247735 = 2MASS J18205368-4533401, type "high proper-motion star", no other designations,
  no variability. VizieR cone (40″): no entry in VSX, ASAS-SN variables (II/366), Gaia DR3 variability, ASAS-3 variables, the
  WASP candidate list, Prša+2022 or IJspeert+2024 TESS EB catalogues, Kostov+2019 single transits, Montalto+2020 or
  Hawthorn+2024 FFI candidate lists. ExoFOP page: 0 TOIs, 0 CTOIs, 0 observations, 0 notes. arXiv full-text API: zero
  entries for "89247735" or "J1820-4533"; web search: nothing. **The object is unpublished.**
* Gaia DR3 6708071581514074368: parallax 9.540 ± 0.020 mas, RUWE 1.10, astrometric_excess_noise 0.086 mas (sig 8.7, normal for
  G = 11.9), ipd_frac_multi_peak 0, non_single_star 0, duplicated_source false, no NSS solution, no vari_summary row;
  RV −21.62 ± 0.54 km/s from 14 transits, rv_renormalised_gof −0.16, rv_chisq_pvalue 0.52 (no RV variability detected),
  rv_amplitude_robust 5.7 km/s (consistent with noise for 14 transits at this magnitude). M_G = 6.75, BP−RP 1.45 → single
  K4–K5 dwarf on the main sequence (a twin binary would sit 0.75 mag above). GSP-Phot Teff 4614 K, log g 4.60,
  R = 0.726 R☉ (TIC: 0.785). Stellar density: TIC radius with M = 0.70 M☉ → 1.45 ρ☉; Gaia radius → 1.83 ρ☉. Transit:
  a/R★ = 30.9 ± 2.3 → ρ★ = 1.18 (+0.28/−0.24) ρ☉. Consistent with the TIC radius at 1σ, 2.3σ low against the Gaia radius; the
  degeneracy with b (0.44 +0.12/−0.20) absorbs this. **Not a tension that kills, but the transit prefers a slightly lower
  density than the star, which is the direction a blended or grazing configuration would push it.**
* The G = 15.49 neighbour (6708071581515491456): parallax 0.458 ± 0.043 mas (2.2–2.4 kpc), pm (+1.7, −6.0) mas/yr —
  unrelated background star; GSP-Phot Teff 5620 K, log g 3.83, R = 1.8 R☉, [M/H] −0.76, M_G = +3.5: a metal-poor G subgiant.
  It would need a 23 % eclipse (team's number; with the PM-corrected 2026 separation it contributes the same ~3.6 % of flux).
  Excluded as the source by §2.3.
* RV semi-amplitudes for M★ = 0.70 M☉, P = 18.32 d: 0.3 M_Jup 29 m/s; 1 M_Jup 98 m/s; 13 M_Jup 1.26 km/s; 0.08 M☉ 7.6 km/s;
  0.10 M☉ 9.4 km/s. Gaia's 14-transit RV (error 0.54 km/s, no variability) excludes an M-dwarf companion at ≳ 90 % of
  inclinations but says nothing below ~1.5 km/s: planet vs brown dwarf is open. Rp = 8.5 R⊕ (TIC radius) or 7.9 R⊕ (Gaia radius).

### 2.6 TIC 317134140 (`analysis_317134140.py`, `analysis_317134140.json`, `plots/review_317134140_fold.png`)
Local SPOC 2-min files, S6/S87/S98/S107, QUALITY==0, edges trimmed, TOI-2514.01 masked.
* Lomb–Scargle of raw PDCSAP and SAP (0.2–15 d): top peaks are 3–13 d systematics (amplitudes 85–1,400 ppm); sinusoidal
  amplitudes at 0.5719 d: 35 / 40 / 42 / 67 ppm (PDCSAP S6/S87/S98/S107), at 1.1437 d 29 / 46 / 32 / 24 ppm, at 1.7156 d
  30 / 78 / 17 / 8 ppm. No rotation period, no harmonic series; the P, 2P, 3P pattern in the team's BLS peaks is the usual
  BLS sub-harmonic response, not a stellar harmonic series.
* Detrend-window scan (biweight, unmasked / masked, depth at the frozen ephemeris, ppm): S98 0.25 d 211/247, 0.5 d 232/229,
  0.75 d 223/218, 1 d 236/224, 2 d 230/229; S107 153/191, 200/208, 203/205, 214/208, 204/203. The depth is stable for windows
  ≥ 0.5 d; only the 0.25-d window (comparable to 4× the duration) suppresses it. The 0.5-d discovery window is adequate.
* Model comparison on the stitched masked-detrended fold (N = 63,181): Δχ² vs flat: box (1 parameter) 104.1; sinusoid at P
  (2 parameters) 30.5; sinusoid + first harmonic (4) 47.1. Box depth 192 ppm, sinusoid amplitude 46 ppm. The signal is
  transit-shaped, not a sinusoid.
* Masked-vs-unmasked null bias (random-phase box depths, 300 phases per sector; "team-style" = detrend masked at the
  candidate phase, "fair" = detrend masked at each trial phase): null σ 37/51/37/44 ppm vs 41/52/30/40 ppm; p-values of the
  candidate depth identical (< 1/300). The holdout null is not biased by the masking.
* Depth constancy from the report's own per-sector values (S6 118 ± 38, S32 56 ± 36, S33 192 ± 34, S87 113 ± 38, S98 213 ± 30,
  S107 200 ± 38 ppm): weighted mean 154 ppm, χ² = 16.1 / 5, p = 0.0066. A constant-depth planet is disfavoured at ~2.7σ; the
  report's "χ² ≈ 18.5" and "main open caveat" is confirmed and should be stated as p ≈ 0.007.
* Centroid: `report.json` per-sector `centroid_shift` S98 = 0.34 ± 0.07 mpx (5.3σ) vs an on-target expectation of
  185e-6 × 0.53 px ≈ 0.10 mpx; S6/S87/S107 are 0.06–0.15 mpx (1–2σ). The report quotes only the weighted four-sector mean.
* SPOC TCEs: none of the 133 local `dvr-tcestats` tables (including the S6, S87, S98, S107 single-sector runs) lists TIC
  317134140; no multi-sector run covering S87+S98+S107 exists yet.
* ExoFOP (fetched today): TOI-2514.01 TFOPWG "PC", TOI note "weak signal" (last edit 2025-07-31); CTOI parameters from a
  RAVEN/Lafarga et al. validation; follow-up: SOAR speckle (Δmag 4.6 at 1″), Shane/ShARCS AO, TRES ×2, CHIRON ×2,
  LCO-SAAO 1-m i′ transit 2023-11-08 (349 min), **CHEOPS 291-min visit 2023-01-06**. No mention of any short-period signal.

### 2.7 Pool-level and code reproduction
Reproduced from the team's JSON products (not re-run): `ffi_pixel_S93.json` already recorded `n_events = 2` for S93 while
the report and `alias_89247735.py` count one S93 event — the discrepancy is exactly the flagged epoch-118 event, visible in
the team's own output but not noticed.

---

## 3. Bugs, leaks and inconsistencies in the code (file:line)

1. **`scripts/tsearch.py:45` (and `:24` for SPOC)** — `QUALITY == 0` discards all QLP cadences carrying bit 2^30
   (1,073,741,824). The bit is not defined in the QLP README or HLSP page (the data-product PDF could not be rendered here);
   empirically it covers 72/72 cadences of the S93 epoch-118 transit, where it is co-located with the high, decaying
   `SAP_BKG` of the orbit start, and 28/72 cadences of the S104 transit, where flagged and unflagged cadences are
   interleaved after the event. For Pool B this removes 20–30 % of cadences per sector and can delete any transit in the
   first ~0.5–1 d of an orbit. Consequence here: a fourth, fully covered transit of the headline candidate was
   never seen; `report.json`/`REPORT.md` §8.2–8.3 ("one per sector", "three events") and `PREREGISTRATION.md` are
   incomplete. Consequence for the search: Pool-B completeness near orbit starts is lower than the known-signal recovery test
   suggests (recovered TOIs have many transits and do not depend on any single epoch). Recommended: keep bit 2^30 cadences
   but down-weight or detrend them; at minimum, re-inspect candidate epochs in flagged data (as `qa_events_89247735.py` does).
2. **`scripts/alias_89247735.py:22`** — alias coverage counts are computed on the quality-filtered stitched data, so epoch 118
   was counted as "not covered" and the 36.65-d loophole was left open in §8.3. With the flagged data it is closed.
3. **`scripts/vet.py:174`** — in `blind_test`, if the training-only BLS recovers an alias (2P or P/2), `P_tr` is replaced by the
   all-data period `P`; the holdout prediction then uses a period that was not derived from the training data. Small leak;
   moot since §7.1 demoted the test, but it should be `P_tr *= k` for the matched alias factor, not `P`.
4. **`scripts/vet.py:28-41` with `:17-25`** — `load_all` applies the candidate-ephemeris transit mask to the detrending of
   *all* sectors, including the holdout year, before `blind_test`. The report discloses it; I tested it (§2.6): for a 1.5-h
   box and a 0.75-d window the random-phase null is unaffected (σ changes by < 15 %), so no correction is needed. For the
   4-h events of TIC 89247735 the effect would be larger, but that object's blind tests are 40σ single events and do not
   depend on it.
5. **`scripts/null_calibration.py:61-68` vs `scripts/rank.py:56-63`** — the null keeps the best *surviving* SDE among the top
   three inverted peaks after the cuts, while the real ranking applies the cuts only to the *top* peak (`top = df[df["rank"]
   == 0]`). The null therefore over-counts false positives relative to the real procedure (conservative), but the two are not
   "the identical cuts" as stated in §7. Also `yrs_det` in the null is computed on unbinned inverted data at the inverted
   peak's ephemeris (`null_calibration.py:26-33`) while `rank.py:34` uses the pipeline's binned per-year table; the
   definitions are equivalent in intent, not in code.
6. **`scripts/rank.py:37`** — the secondary-eclipse significance is `depth_phased / depth_err`, i.e. the secondary depth
   divided by the *primary* depth error (astropy's `depth_phased` has its own error, `depth_phased[1]`, which is not stored by
   `search_pipeline.py:63`). The cut `|secondary| < 3σ` is therefore computed with the wrong error; for sparse secondaries it is
   too strict, for dense ones too loose. `halfP_sig` is computed and never used. Same in `null_calibration.py:65`.
7. **`scripts/search_pipeline.py:50-51`** — SDE = (power − running median) / MAD of the *whole* periodogram. Because the
   median filter width `k = max(51, n//200|1)` is in grid points (log-uniform frequency), the baseline is adaptive but the MAD is
   global; at short periods where BLS power has a different variance the SDE is mis-scaled. This is a calibration issue, not
   a bug, and the inverted null calibrates it empirically — but only for the top peak and only in the aggregate.
8. **`scripts/ffi_pixel_test.py:41-43`** — centroid of positive-depth pixels inside a 3.5-px circle centred on the target. Bias
   quantified by injection (§2.3): 0.02–0.06 px toward the target for a source at the neighbour. The quoted statistical error
   (0.03–0.04 px, bootstrap of the same estimator) is realistic; the dominant systematic is the position reference
   (J2000 catalogue vs proper-motion-corrected: 0.13 px; WCS vs image fit: 0.16–0.17 px), which the report estimates at
   "~0.1 px". `ffi_pixel_test.py:89-90` reads `ra, dec` from the pool CSV (J2000) and never applies proper motion.
9. **`scripts/vet.py:132-137` / `final_ephemeris_89247735.py:17-20`** — transit timing on a fixed-shape model with a flat
   baseline (`vet.py`) or a χ² rescaled to reduced χ² = 1 (`final_ephemeris`). Neither allows a local baseline slope; on the
   scattered-light ramp this matters (my quadratic-baseline timings differ from the team's by 1–3 min, comparable to the
   quoted errors). The 4-event χ²/dof of 8.5/2 says the per-event timing errors are still underestimated by ~2×; the frozen
   "±15 min" window is adequate.
10. **`scripts/vet.py:148-150`, `final_ephemeris_89247735.py:29-30`** — covariance inflation by χ²/dof is applied correctly (as
    variance). `vet.py:435-437` density formulas are correct. `vet.py:486` T_eq uses a/R★ from the fit — correct.
11. **`REPORT.md` §8.3** states "Momentum dumps are ≥ 33 h from every event" — true for the three events used; the fourth is
    11.7 h after a dump (still outside any dump-related window).
12. **`REPORT.md` §6.3** quotes the centroid shift as "0.1 millipixel" (four-sector mean) without the 5.3σ S98 value in the
    same JSON; §6.4/§7.1 depth χ² should carry its p-value (0.007).

---

## 4. What could not be tested and why
* ASAS-SN Sky Patrol v2 light curves (the decisive archival test for TIC 89247735: ~25 in-transit epochs expected): service
  offline for maintenance since 2026-10-13. Re-run `asassn_fetch_89247735.py` then `asassn_fold_89247735.py` (adapt the
  column names) when it returns.
* SuperWASP: no DR1 source at the position. KELT-South field coverage: not resolved (field names only). ASAS-3: server error.
  ATLAS/NGTS/ZTF: no access or out of range.
* A companion within ~1″ of TIC 89247735 (hierarchical-triple EB false positive): no TESS test can exclude it; needs
  speckle/AO imaging and/or RVs.
* Nature of the TIC 89247735 companion (planet / brown dwarf / late-M): photometry cannot decide; Gaia RVs only exclude
  K ≳ 1.5 km/s.
* TIC 317134140: the CHEOPS 2023-01-06 visit and the LCO 2023-11-08 light curve are on ExoFOP/CHEOPS archive behind logins;
  the S32 non-detection could not be independently re-derived at pixel level within the time budget (the team's four-product
  check is accepted as is).
* The full Pool-B search was not re-run; the effect of bug 1 on pool completeness is estimated, not measured.

---

## 5. Cheapest next observations, ranked

### TIC 89247735
1. **Almost nothing can be done from the ground until spring 2027.** Sun–target separation makes epochs 147–151
   (2026-11-17 to 2027-01-29) unobservable at any southern site (target altitude > 30° with Sun < −12° at no point of the
   ±2-h window from CTIO, SAAO or Siding Spring; `observability_89247735.csv`); epoch 146 (2026-10-29 21:23 UTC) is only
   partially observable from SAAO (egress side, low in evening twilight) and 152 only partially from Siding Spring. First usable windows: epoch 156 (2027-05-01 02:56 UTC,
   partial from CTIO/SAAO), 158 (2027-06-06 18:27, partial SAAO/SSO), **159 (2027-06-25 02:12 UTC, full transit from Chile)**,
   **162 (2027-08-19 01:28 UTC, full from Chile)**. A 30–40-cm telescope with a small aperture (exclude the 8″ neighbour as far
   as seeing allows) gives a 1 % × 4 h transit at > 10σ. Update the prediction with the fourth event first (shift < 1 min).
2. **Radial velocities now** (target is a V ≈ 12.3 K dwarf; it is observable spectroscopically in twilight/morning from
   March 2027, and in evening twilight until early November 2026): 3–4 HARPS/FEROS/CHIRON epochs at quadrature phases
   (phase 0.25/0.75 of the 18.32-d ephemeris) distinguish 1 M_Jup (K ≈ 100 m/s) from a brown dwarf (K ≈ 1 km/s) from an
   M dwarf (K ≈ 8 km/s) with 10–50 m/s precision. This is the single most valuable observation and does not need a transit.
3. **ASAS-SN v2 fold** as soon as the service is back (free; 2–3σ depth test over 2014–2026, and a fully independent check
   of the 18.32-d period).
4. **Speckle or AO imaging** (SOAR HRCam / Zorro-class) to exclude a Δmag ≲ 5 companion inside 1″, which is the only
   remaining blend channel.
5. Do not edit the frozen file. Deposit the existing `PREREGISTRATION.md` + CSV (SHA af83f110…) as version 1, and add a
   *versioned second* pre-registration (new timestamp, new SHA) that records the fourth transit, the 4-event ephemeris and
   the unchanged predictions, before any new data arrive. Version 1 remains the test of record for epochs ≥ 146.

### TIC 317134140
1. **S108–S110** as pre-registered (data release ~mid-November 2026 onward). This remains the decisive test; the predictions
   are unchanged by this review.
2. **CHEOPS 2023-01-06 visit** (291 min): compute which of the 0.5719-d epochs fall in the visit (≈46 % chance of a full
   transit) and request the light curve from the CHATEAUX team; CHEOPS reaches ~50 ppm per hour on an 11th-mag star, so a
   185-ppm, 1.5-h event is a 3–4σ single-visit test — and it is already taken.
3. Ask SPOC/TESS for a multi-sector DV run over S87+S98+S107(+S108–S110) or run TLS on the stitched 2-min data with the
   TOI masked; a TCE at 0.5719 d from the official pipeline would be independent machinery.
4. The 1.1437-d equal-eclipse alternative needs odd/even at 2P with S108–S110 added (currently 0.1σ on 185 ppm; TESS alone
   will not reach the needed 30-ppm precision until ~10 sectors).

---

## 6. File index
`qa_events_89247735.py` → `plots/qa_S{13,66,93,104}_epoch*.png`; `hlsp_check_89247735.py` → `hlsp_check_89247735.json`;
`four_events_89247735.py` → `four_events_89247735.json`; `control_stars_s93_v2.py` → `control_stars_s93_v2.csv`,
`plots/control_stars_s93.png` (`control_stars_s93.py`/`.csv` is the superseded crude version); `s93_two_events.py` → `s93_two_events.json`,
`plots/s93_two_events.png`; `pixel_injection_89247735.py` → `pixel_injection_89247735.json`, `plots/pixel_review_S*.png`;
`asassn_fetch_89247735.py`, `asassn_fold_89247735.py` → `asassn_v1_fold_89247735.json`, `plots/asassn_v1_fold.png`,
`data/asassn/`; `analysis_317134140.py` → `analysis_317134140.json`, `plots/review_317134140_fold.png`;
`observability_89247735.csv`; `data/` (ExoFOP pages, SuperWASP query result, HLSP downloads).
