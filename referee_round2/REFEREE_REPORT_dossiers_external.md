# Independent external referee report: two round-2 dossiers

Date: 2026-10-20. Reviewer/tool: OpenAI Codex. Working directory: `/Users/fernando/Desktop/NASA`.

Instructions: `results/referee_89247735/PROMPT_dossiers_review.txt`. Reviewed `results/round2_dossiers/DOSSIERS.md`, the two corresponding `results/vet_allsky/` directories, the relevant public README paragraphs and outcome-table rows, the earlier internal report and pixel scripts, the prior-search report/verdicts/limitations, and the relevant processing scripts. Independent calculations and read-only public queries are preserved under `/tmp/dossiers_external_review/`; commands and limitations are identified below. I modified only this report in the project. I did not download or open any S106-or-later photometry, cutout or FFI of the seven protected targets. All TESS data used here have sector numbers ≤105, checked from filenames before opening.

## Recommendations

**TIC 183374279: revise; retain candidate status.** Repeated transit-like dimming, an approximately 11.73798-d ephemeris, extraction consistency and the absence of a sufficiently bright catalogued close contaminant support further investigation. I reproduced the principal photometric and clock numbers. The case does not establish the host uniquely, exclude unresolved false positives, or validate a planet. The public text overstates the pixel exclusion and RV interpretation, mixes stellar-density conventions, and still gives an obsolete availability/test outlook. Its S106 outcome remains unexamined and must not be inferred from the forecast. Evidence: object-specific tables and shared methodological findings below.

**TIC 61310956: revise; retain candidate status with a photometric-systematics caveat.** The six-event signal and corrected v3 linear ephemeris are reproducible. The local dossier is substantially obsolete compared with the README and v3 files. The supposed independent 11σ SPOC detection is a known-ephemeris extraction check; the adopted SAP photometry has a baseline-sensitive odd/even difference; and the ground-test duration, timing uncertainty and observing-window claims need reconciliation. None of my checks demonstrates a false positive strongly enough to justify withdrawal, but neither the present FPP calculation nor Gaia proves a planetary interpretation. Evidence: second-object tables, the event-level recomputation, and visibility calculations below.

## TIC 183374279

### Verified claims and their limits

| Claim | Independent result | Verification |
|---|---|---|
| Frozen v2 ephemeris | **T0=4226.651420766412 BTJD**, epoch 244; **P=11.7379835373565 d**, σP=0.00002517885 d; χ²=**1.25506**, 4 dof | Weighted least-squares refit of all six `final_ephemeris_v2.json:sector_times`, including its covariance and stated inflation, in `ephemeris_visibility.py`. |
| Frozen prediction integrity | SHA-256 **`069d82980645e2adb5bc81895b187de8654dc880205574a50af764b79b04d621`** agrees with JSON and registration | `hashlib.sha256` of `predicted_transits_2026_2027_v2.csv`; regenerated times agree within CSV rounding (<0.38 s), errors within 0.05 min. |
| Period present in SAP data | Independent narrow SAP BLS maximum **11.73796257 d**, duration-grid value **2.6 h** | `photometry.py`, using only S2,29,69,96,103,105, QUALITY=0, masked biweight and the declared 0.3-d edge trim. This is a local period check, not an exhaustive alias exclusion. |
| Raw-SAP depth | **1092.06 ± 91.38 ppm**, formal box SNR **11.95** | Independently reimplemented detrending/box estimator in `photometry.py`; agrees with `report.json:sap_depth`. Errors here are nominal scatter-based errors, not calibrated false-alarm probabilities. |
| Reported detrended diagnostics | Odd/even **0.3551σ**; phase-0.5 secondary **44.77 ± 81.54 ppm** | Independently reproduced with the QLP detrended column (KSPSAP fallback where DET_FLUX is absent). In SAP the corresponding values are **−0.655σ** and **−90.29 ± 80.83 ppm**. Source: `photometry.log`. |
| Duration and density arithmetic | Circular median-parameter T14 **2.8410 h**; stored density ratio **1.45364** under the report's original host convention | Analytic transit geometry from `report.json:shape_mcmc` and the ratio of its density fields; `ephemeris_visibility.py`. The ratio changes when the newly adopted TIC radius/mass is used, as below. |
| Five observed calendar years | DET/KSPSAP formal depth/error ratios **5.44, 5.82, 3.17, 4.44, 9.59** for 2018,2020,2023,2025,2026 | Recomputed from the FITS. The “3–10σ” statement describes this product/estimator; SAP's 2023 ratio is **2.26**, so it is not a product-independent confidence statement. |
| Retrospective holdout numbers | Stored formal ratios **4.55, 3.21, 3.73, 8.14** in the four testable years; 2018 untestable | Directly checked `report.json:blind_tests` and `scripts/vet.py:blind_test`. I did not rerun all training-only searches; these are retrospective consistency checks, discussed below. |
| SPOC S29 extraction check | **1380.39 ppm** with **78** in-transit 2-min samples; random-phase RMS **284 ppm** in my check | Recomputed directly from the cached PDCSAP FITS using the documented estimator. Its blind BLS instead peaks at **9.124490 d**, SDE **3.269**; near the QLP period SDE **1.888**. This supports extraction consistency, not an independent period detection. |
| Pixel-offset numbers | Reproduced loss-minus-image-centroid offsets **0.063/0.243/0.400 px** in S96/103/105 and the supplied simulation scatters **0.167/0.164/0.218 px** for the sector stacks | Reran the inspected `pixel_calib2.py` via a temporary copy, using cached 15×15 cutouts only; `pixel_calib2.log`. Their interpretation as calibrated localization confidence is not established by that simulation, below. |
| TRICERATOPS numerical output | **FPP=0.03097705**, NFPP=0 in this run; above the 0.015 validation threshold | Recomputed FPP as 1−(TP+PTP+DTP) from `triceratops_probs.csv`; checked installed package definition and `triceratops.json`. No contrast curve was supplied. |
| Gaia flags | RUWE **1.12436**, duplicated=false, NSS=0; RV **22.2438 ±0.6939 km/s**, 16 transits, constancy p=**0.28429** | Fresh two-source Gaia DR3 ADQL query, saved as `gaia_hosts.txt`; these are catalogue summaries, not an orbital mass constraint. |
| Nearby known planet listings | No TOI or CTOI within **60″** | Fresh ExoFOP exports: 8,151 TOI and 5,138 CTOI rows, by-TIC and coordinate checks; `public_checks.py` and the cone calculation. Current TCE/Archive absence was not independently established. |

### Errors, unsupported precision and required corrections

| Location / claim | Correct value or defensible interpretation | Verification / fix |
|---|---|---|
| DOSSIERS line 5 / README line 42: “this excludes blends 20–60″ away” | Centroids are consistent with the target under the particular estimator; universal spatial exclusion/completeness was not established. | Pixel code uses a positive-only centroid restricted to 3.5 px. Its fake signals dim the entire mean image, including sky/neighbours; there are no source-specific off-target recovery trials. Replace by the conditional wording below, or supply realistic localized-source injections and calibrated position likelihoods. |
| Same paragraph: “RV constant over 16 epochs” | **No significant variability in the Gaia DR3 constancy statistic (p=0.284, 16 RVS transits)**. It is not a direct assertion that the RV is constant. | Fresh Gaia query and [Gaia DR3 source-column definitions](https://gea.esac.esa.int/archive/documentation/GDR3/Gaia_archive/chap_datamodel/sec_dm_main_source_catalogue/ssec_dm_gaia_source.html). No epoch RVs/orbital fit were supplied here. |
| Same paragraph: new TIC host parameters followed by density ratio “1.4 +0.6/−0.9” | With the table's **M=0.71 M☉, R=0.708091 R☉**, catalogue density is **1.99982 solar**, giving **ρfit/ρcatalogue=1.24267**, rather than 1.45364. | `triceratops_stars.csv` target row and `report.json:density_check`; M/R³ calculation. Either label the old host convention or recompute consistently. It remains broadly compatible with unity. |
| “nearest star able to mimic ... 72″ ... 22%” while adopting SAP depth | **22.3%** is the old total-G-flux proxy at the shallower detrended depth. At SAP 1092 ppm it is approximately **25.3%** using G fluxes; TIC total T magnitudes give approximately **29.9%** at **71.906″**. Actual aperture fractions matter. | Recomputed δ(1+r)/r, r=10^(−0.4Δmag), from `report.json:gaia_neighbours` and `triceratops_stars.csv`. The chosen 2.5-px TRICERATOPS aperture admits only ~213 ppm of that star's flux, so even a complete eclipse cannot produce the signal **under that aperture model**. Say “nearest sufficiently bright total-flux source,” not an established viable contaminant. |
| Radius “2.3–2.9 R⊕ (range follows depth range)” | Reasonable illustrative on-target scale, **not a confidence interval** and not a consistent single fit. k×Rstar gives **2.321 R⊕** from the detrended shape; sqrt(SAP depth)×Rstar gives **2.552 R⊕**; 1380 ppm gives **2.869 R⊕**, before limb darkening/dilution corrections. | Independent radius arithmetic in `ephemeris_visibility.py`. Label the methods and include stellar/dilution/shape uncertainty in any quantitative radius claim. |
| “σ 2.7 min” for both listed S106 events | Stored rounded uncertainties are **2.7 and 2.8 min** for epochs 245 and 246 (2.8 at 247). | Frozen CSV; this is a small rounding omission. |
| “whether FFIs were already retrievable ... was not checked” as the present availability account | Retain the historical non-examination attestation, but link the **2026-10-20 availability erratum** and its product-specific chronology. | `results/ERRATUM_S106_DATA_AVAILABILITY_2026-10-20.md` now records that FFI/TESScut products existed before the freezes. I did not reopen or query protected photometry to re-establish archive availability in this review. |
| Test “rests on two events,” implying a likely decisive S106 result | Two nominal centres are inside science windows, but eligibility depends on trimming/gaps. The separately reviewed conformance forecast has **one eligible event in five of seven templates**, two in the other two; it is a forecast, not observed S106 coverage. | `results/conformance_v21/s106_forecast.csv` and current conformance draft. State the conditional INSUFFICIENT risk if that procedure is adopted; do not describe any actual outcome before the declared test. |
| Frozen excerpt's “<1.5 min” clock sentence | Net prediction shift is small, but individual sector corrections are **−3.25 min (S103), +3.27 min (S105)**. | Fresh cadence alignment/JPL calculation and weighted propagation below. Keep original frozen text as history; append/link the corrected measured statement. |

The epoch-247 partial-coverage arithmetic is correct. From the frozen CSV I obtain geocentric mid-transit **2026-08-09 08:38:36.8 UTC**. With T14=2.841 h, egress is approximately **10:03:51 UTC**, **53 min 51 s after** the orbit-table science end at 09:10 UTC. This uses only the prediction and `catalogs/TESS_orbit_times.csv`, not S106 flux. Nominal centres for epochs 245/246 are **July 16 21:14:44.6** and **July 28 14:56:34.5 UTC**. CSV minute fields are truncated, not rounded.

### Clock verification

I opened only the cached S103/S105 timing columns and the matching cached TESScut timing columns. Integer-cadence matching gives 10,964 matched S103 cadences (runner-up 10,960), and 11,652 matched S105 cadences (runner-up 11,649). An independent JPL vector projection gives:

| Sector | QLP−spacecraft (min) | Target light time (min) | Add to QLP time (min) |
|---|---:|---:|---:|
| 103 | −0.0523105245 | −3.3342899033 | **−3.2500025944** |
| 105 | −0.0516462652 | +3.1824075413 | **+3.2660305910** |

Source: `/tmp/dossiers_external_review/clock_check.py`/`.log`, JPL Horizons `-95`, barycentric ICRF vectors, spacecraft time reconstructed as TIME−TIMECORR; c0 from the existing control-sector record. Results agree with `results/qlp_clock_v2/183374279.json` to its precision. The cadence alignment guards against whole-cadence nearest-neighbour aliases.

Adding those sector corrections and repeating the linear fit shifts frozen S106 predictions by **+0.857, +0.863, +0.869 min** for epochs 245–247; the period changes by **+0.3462 s**. This reproduces the addendum's **+0.9 min**, small relative to the 2.7–2.8-min formal prediction errors. It does not erase the timing problem: observations must be corrected before scoring. Frozen predictions should remain the test of record, with corrected predictions separately identified. Verification: `ephemeris_visibility.py` and the clock addendum; no S106 data were used.

### Novelty and wording

I found no earlier independent matching report in the searches actually completed here. The existing sweep covers aliases and neighbours and is useful evidence; it is not proof that no report exists. Use:

> We found no earlier public report of an approximately 11.73798-d transit-like signal on this target or the searched nearby sources in the catalogues and corpora described in the dated prior-search report. The signal remains an unvalidated candidate.

Replace the localization/RV passage with:

> The loss centroid is consistent with the target under the tested estimator. Catalogued sources within 60″ are too faint to explain the depth under the adopted flux/aperture models; unresolved or uncatalogued contamination remains possible. Gaia DR3 reports no significant RV variability in its summary constancy test, which does not provide a companion-mass limit here.

Replace “blind holdout ... recovered” with “retrospective leave-one-year-out checks show positive predicted-phase dimming in the four testable years,” giving the formal SNRs and the non-Gaussian phase-null caveat. Two reported formal SNRs are below five; these should not be confused with passing the later preregistered scoring rule. Verification: `report.json:blind_tests` and `vet.py:blind_test`.

## TIC 61310956

### Verified claims and their limits

| Claim | Independent result | Verification |
|---|---|---|
| Six QLP transit-like events | Epochs **0,1,38,40,82,83** in S22×2, S45, S46, S72×2; **four even and two odd**, not three of each | Event-by-event raw-FITS check in `event_checks.py`; sector cadences approximately **1800,600,600,200 s**. |
| Reproducible raw-SAP depth | **1334.24 ±104.92 ppm**, formal box SNR **12.72** | Independent processing in `photometry.py`; matches `report.json:sap_depth`. |
| Period supported locally | Narrow SAP BLS maximum **16.53780634 d**, grid duration **3.4 h** | Independent narrow search, not a uniqueness proof or replacement frozen ephemeris. |
| Duration from median fit parameters | **3.30432 h**, with density ratio **1.44664** under the stored host convention | Analytic circular geometry from the median k,a/R,b in `report.json`; not a new posterior sample or duration uncertainty analysis. |
| Corrected v3 fit | **P=16.53796561246 ±0.00014978512 d**, T0=**3262.56597772612 BTJD**, epoch 82; χ²=**7.19375/2**, inflation **1.89654** | Refit four unique sector rows (S22/S45 SPOC, S46/S72 QLP), with full covariance in `ephemeris_visibility.py`. v2 duplicates S22/S45 and has smaller formal extrapolation errors. |
| v3 checksum and prediction precision | SHA **`76e892963501c62cdedcf07a94b1f2e65bbc47f91427bdd6006ec2250ab1da63`** matches JSON/registration | Hash recomputation; regenerated times match within <0.44 s and σ values within 0.05 min. |
| First post-freeze prediction | Epoch 147: **2026-10-24 00:52:11.4 geocentric UTC**, σ=**27.7 min** | Independent inversion of BJD_TDB including Earth's light-travel time. The CSV's 00:52 is correct at its truncated precision. |
| SPOC extraction consistency | **1068.18 ppm**, 242 in-transit 2-min samples; independent random-phase RMS **232 ppm**, depth/RMS≈**4.61** | Direct cached-SPOC reprocessing. The white-noise estimate ≈95 ppm is not the empirical phase scatter. |
| SPOC alone does not recover the period | Blind BLS maximum **24.830401 d**, SDE **5.783**; near the candidate period SDE **2.906** | Recomputed the documented 50,000-period grid from cached S22/S45 PDCSAP data. |
| Detrended-column diagnostics | Odd/even **1.1956σ**; secondary phase 0.5 **−28.83 ±102.43 ppm** | Reproduced in `photometry.py`. The SAP odd/even diagnostic differs materially, below. |
| Pixel numbers | Reproduced offsets **0.309/0.195/0.087 px** (S22/45/72); simulated stack scatters **0.239/0.234/0.142 px** | Rerun of inspected `pixel_calib2.py` on cached 15×15 cubes only. These do not establish calibrated exclusion probabilities for off-target hosts. |
| TRICERATOPS output | **FPP=0.01968067**, NFPP=0 in this run | Recomputed scenario sum. FPP exceeds 0.015; no contrast curve; stellar/unknown blends remain open. |
| Gaia | RUWE **0.77399**, duplicated=false, NSS=0; **VARIABLE**; RV **−4.66215 ±0.43329 km/s**, 13 transits, constancy p=**0.44207** | Fresh Gaia DR3 query. The VARIABLE flag is independently verified; I did not newly verify a rotation period or the VSX classification. |
| No TOI/CTOI within 60″ | Verified in fresh full exports | ExoFOP ID and coordinate matching. Current NASA Archive/TCE absence could not be independently confirmed here. |
| No affected QLP S99+ sector in the fit | v3 uses only S22/S45/S46/S72 | Verified JSON rows and cached filename inventory. The S103/S105 clock error does not affect this dossier's fitted sectors. |

### Errors and required corrections

| Location / claim | Correct value or interpretation | Verification / fix |
|---|---|---|
| DOSSIERS lines 71–77 and frozen v2 excerpt: “independent ... 11σ” | Known-ephemeris extraction check, **1068 ppm**, empirical phase RMS approximately **230–240 ppm**; no independent SPOC period detection | Independently reproduced above. README lines 46–48 correct the independence claim, but the local dossier is not corrected. |
| DOSSIERS period **16.537975 d**, v2 errors **20–25 min**, v2 frozen excerpt without current status | v3 of record is **16.53796561246 d**; epoch-147 σ **27.7 min**, reaching **33.3 min** at the last 2027 prediction | Refit/hash/CSV check. Keep v2 as archival history but clearly mark it superseded and link v3. |
| README: “σ ≈28 min through 2027” | **About 28–33 min** through December 2027; **35.0 min** at May 8, 2028 | v3 CSV. The older internal report's “28–35 through 2027” also overstates the end-year value; do not copy it verbatim. |
| v3 prose “T14 3.3 h,” but reference line **“T14 2.70 h”** | The actual frozen outcome reference is **2.70 h**, the BLS duration; median shape T14 is **3.304 h** | `PREREGISTRATION_v3.md`, `report.json`. This difference affects duration gates and observing support. Resolve by a dated explicit clarification/amendment before observations, preserving frozen originals. Do not silently substitute one for the other. |
| “odd/even consistent” without product qualification | DET/KSPSAP gives **1.20σ**; globally detrended SAP gives **3.75σ**; a per-event local-linear raw-SAP analysis gives **1.76σ** | `photometry.log` and `event_checks.log`. Report the baseline sensitivity and event depths; this is not evidence sufficient to label the candidate an EB, but it prevents claiming a robust odd/even null. |
| “no secondary” in DOSSIERS | At phase 0.5, **−28.8±102.4 ppm** in the detrended column; **−48.9±101.5 ppm** in SAP | Independent box calculations; no detected secondary is supported, universal absence is not. |
| DOSSIERS “blind holdout 2/2” | **Two of three years testable**: stored formal SNR **7.89** (2021), **4.86** (2023), with the 2023 phase/timing caveat | `report.json:blind_tests`. I did not rerun all training fits; these are retrospective checks rather than two new independent detections. |
| DOSSIERS “likely planet,” no thresholds | The numerical run satisfies Giacalone's broad **FPP<0.5/NFPP<0.001** category, but does **not** satisfy the **FPP<0.015/NFPP<0.001** validation criterion. Authors' chosen conservative candidate wording is appropriate. | Scenario sum and the [original TRICERATOPS paper](https://arxiv.org/abs/2002.00691). Remove the unexplained category label; retain the calculated values and assumptions. |
| DOSSIERS “not yet public,” “full sweep in progress” | The signal was a public table row in **v1.3–v1.5**; the sweep report now exists | Independently inspected `git -C public_release show <tag>:tables/allsky_testable_soon.csv`: P=**16.53788768364 d**, depth **863.373 ppm**; row absent at v1.6. README correctly discloses this. |
| “nearest ... 82″, needing 20%” | **20.5%** is the old G-based, shallow-depth proxy; at SAP depth it is ~**24.2%** using G, ~**26.9%** using TIC total T flux. Aperture-admitted flux gives a different, nonviable scenario in the particular 2.5-px model. | Same flux-ratio calculation as the first object; TIC separation **81.987″**, Gaia separation **82.346″**. Specify band and aperture assumption. |
| Pixel figure `ffi_pixel_S72.png`: apparent depth **2037–2215 ppm** | Still the raw-aperture/background-affected panel identified by the internal review, not a corrected transit depth | I opened the figure and inspected the generating code. Label it explicitly or replace with sky-subtracted/local-baseline measurements; it cannot be presented as corroborating the ~1.3-ppt depth without explanation. |
| v3 CSV epoch 83: “before freeze, untested,” “none (ground-based)” | Epoch 83 is the second S72 event contributing to the training sector time, not an untested ground prediction | CSV, v3 S72 mean_epoch=82.5/n_events=2 and event-level data. Add a dated interpretation note; preserve the frozen CSV bytes. |

#### Baseline-sensitive odd/even result

The six epochs split **4 even/2 odd**. In the global SAP calculation I obtain odd **1823.87±158.53 ppm** versus even **1035.32±138.56 ppm**, a formal **3.745σ** difference. A local linear baseline on each raw-SAP event instead gives weighted odd **1483.69±143.02 ppm**, even **1188.31±87.55 ppm**, or **1.761σ**. The S72 pair changes from approximately **871/1832 ppm** after the global biweight baseline to **1098/1612 ppm** with local linear baselines. Source: `/tmp/dossiers_external_review/event_checks.py`/`.log`; these errors remain simple scatter-based estimates.

This is a systematics sensitivity, not a demonstrated eclipsing binary or proof of stable transit depths. Supply a raw-SAP, exposure-integrated joint fit with local baselines and realistic correlated-noise sensitivity before using an odd/even null as a quantitative false-positive rejection. A 2P EB remains an astrophysical alternative; the small EBx2P model probability and Gaia summaries do not independently exclude every such configuration.

### UTC, observability and the author's October-20 note

The CSVs do include the light-travel correction. I inverted BJD_TDB at the geocentre iteratively with Astropy's builtin solar-system ephemeris, rather than applying only `Time(...).utc`. The amended suggestion **“epoch 151 ... 04:26 UTC”** uses the **wrong column**: v3 time-scale-only UTC is **04:26:06.7**, while geocentric arrival is **04:21:53.2** (the stored minute field is 04:21, truncated). Future observers need geocentric UTC contacts or consistently computed topocentric contacts.

Using a physical duration **3.3 h**, pressure=0 and representative site coordinates listed in `ephemeris_visibility.py`, I find:

| Epoch / proposed region | Geocentric UTC midpoint | Minimum target altitude / maximum Sun altitude during nominal 3.3-h transit | Same quantities over T14 + full ±3σ timing support + 1 h baseline each side |
|---|---|---|---|
| **151, La Palma** | **2026-12-29 04:21:53** | **51.0° / −26.1°** | 8.16 h: **19.1° / +3.6°** |
| **152, Okayama** | **2027-01-14 17:14:44** | **50.4° / −40.4°** | 8.18 h: **20.5° / −10.8°** |
| **153, Cerro Tololo** | **2027-01-31 06:08:06** | **33.4° / −27.2°** | 8.20 h: **7.8° / −0.1°** |

Thus the proposed sites can cover the **nominal** transits in darkness. “Fully observable” must say whether it means nominal contacts or complete preregistered timing/baseline support. None of these three examples provides the full support with both target altitude ≥30° and Sun altitude ≤−12°. Even omitting baseline, the ±3σ support reaches Sun altitude **−8.2°** for epoch 151 and target altitude **19.2°** for epoch 153; epoch 152 clears that narrower test. Source: independent 97-point altitude grids over each window in `ephemeris_visibility.log`.

The README's ≈7-h advice also needs qualification. At epoch 147, 3.3 h + 6×27.7 min + 2 h baseline = **8.07 h**; around the December opportunity it is **8.16 h**. At the frozen **2.70-h reference**, those totals are **7.47/7.56 h**. A 7-h sequence can cover less than the full conservative support; it is not automatically an “excluded” observation. Likewise, ≤1.5 mmag per 10-min bin is an input precision requirement, not proof that every allowed shallow transit reaches SNR≥4 or can be excluded to 0.3× reference.

For October 24 the target–Sun separation is approximately **55.0°**; the four checked sites do not provide a useful complete nominal transit. By November 26/December 12 the separations are **87.9°/104.5°**, so “too close to the Sun until late December” is too broad as a geometric statement. The actual obstacle is obtaining the whole transit, uncertainty margin and baselines in a site's dark, high-altitude interval. Among the four sites checked (La Palma, Okayama, CTIO, Hawaii), epoch 151 is the first nominal transit meeting altitude≥30°/Sun≤−12°. I did **not** survey every observatory or latitude and cannot certify the word “first” globally.

The computation uses geocentric UTC and an approximate modern site location, ignores weather/horizon obstructions, and uses offline IERS information (warnings imply arcsecond-scale orientation uncertainty, immaterial to these degree-scale failures). Millisecond-scale topocentric light-time differences and stellar proper-motion effects do not change these observing conclusions. These are geometric checks, not an observing guarantee.

### Novelty and replacement wording

No earlier independent matching report was found in the checks completed here. Qualify this as a searched-literature/corpus result, not exhaustive proof of priority. The author's own public table row counts as a report of this signal even though it was not then labelled a candidate. Local Git history independently gives the first table insertion at **2026-10-18 23:24:45 UTC** and removal at **2026-10-19 12:15:57 UTC**; this establishes recorded commit history, not by itself the precise time a remote release became public. Source: `git -C public_release log --all --reverse --format='%h %aI' -S 61310956 -- tables/allsky_testable_soon.csv`, with EDT converted to UTC, and tag-row inspection.

Suggested current dossier text:

> An approximately 16.53797-d transit-like signal is present in six QLP events. At the known ephemeris, SPOC provides an extraction cross-check rather than an independent period detection. Raw-SAP depth is about 1.33 ppt; its baseline-sensitive odd/even difference requires further assessment. The loss centroid is consistent with the target under the tested estimator, but unresolved contamination and nonplanetary interpretations remain open. The v3 ephemeris uses one timing per sector; its formal uncertainty grows from 28 to 33 min through 2027. Ground tests require at least two adequately covered epochs under the explicitly stated reference depth/duration and timing rule.

For the ground-planning note, use:

> Nominal contacts for epochs 151, 152 and 153 are geometrically accessible from the Canaries, Japan and Chile respectively. The epoch-151 geocentric midpoint is 2026-12-29 04:21:53 UTC. Coverage of the full timing uncertainty and required baselines needs a separate window check and may require multiple sites or later opportunities.

## Shared false-positive and statistical limitations

1. **Pixel numerical reproduction is not source-localization validation.** I reran the supplied calibration on all six relevant sector/object combinations and reproduced the reported offsets/scatters. But `pixel_calib2.py` constructs a fake dip with `cf[wi] -= depth_inj * mean_img`: that dims sky and all stars in the mean image. It is not a localized transit on the target or on a specified contaminant. The centroid uses positive-only depth within 3.5 px, and `rad/sqrt(n_events)` is a radial simulation RMS, not a calibrated one-coordinate Gaussian σ or an off-target exclusion probability. The centroid reference also includes local sky. I also checked QLP S96 epoch 219: **20/47** cadences inside the 2.6-h transit window and **40/93** within ±2.6 h carry nonzero QUALITY (bit 2^30). The cutout script applies TESScut quality, not these QLP flags, and counts this as one of its two S96 events. That is an additional reason to audit quality/gap sensitivity before combining centroids. Provide a background-subtracted target/PRF injection, off-target trials, bias/covariance/tail calibration and proper time/quality treatment before claiming blanket 20–60″ exclusions. The current consistency statement can remain as conditional evidence. Verification: inspected both pixel scripts and reran only their cached ≤105 inputs; `pixel_calib2.log`.
2. **Known neighbours and unknown blends are different questions.** The TIC/target-aperture tables put the known close neighbours at admitted fractions approximately **1.81×10⁻⁴** for each target, well below the observed ≈10⁻³ depths. Under those flux models those particular neighbours cannot supply the whole signal even in a complete eclipse. This supports rejecting the listed stars, not all uncatalogued or unresolved sources. The numerical “22%/20%” statements ignore band/aperture differences, as quantified above.
3. **NFPP=0 is structural in these runs.** The saved probability tables contain the 15 target/unresolved/background scenarios, with no viable resolved-neighbour rows. The installed code sets NFPP=0 when there are no additional rows. Thus exact zero is not measured certainty. FPPs are model-conditional and dominated by the secondary-star planet scenario (STP **0.0308895/0.0193801**). No contrast curve or seed ensemble was supplied. Source: saved tables, `triceratops_qlp.py`, installed `.venv_tri/.../triceratops.py:1697–1701`, and the [TRICERATOPS paper](https://arxiv.org/abs/2002.00691). Neither run meets its validation threshold.
4. **“Empirical σ” needs definition.** The SPOC depth/random-phase-RMS ratios near 4.8 and 4.5 are reproducible, but the phase distributions are not Gaussian tails. My 61310956 phase experiment has **4 exceedances in 388 eligible draws**, an add-one frequency **5/389≈0.0129**, despite depth/RMS≈4.61. The older internal report itself quoted p=0.0075. Do not translate that ratio into a Gaussian 4.5σ false-alarm significance. Report the estimator, scatter and empirical exceedance count separately. Source: `photometry.py`/`.log`; same finite light curves and artificial phase draws, not independent astrophysical trials.
5. **Gaia does not supply the claimed mass limits here.** I do not adopt the internal report's assertion that Gaia excludes stellar-mass companions or every 2P EB. The queried p-values fail to reject RV constancy; they do not provide a period-specific semi-amplitude limit. The quoted `radial_velocity_error` is the error of the published representative/median velocity, not per-transit precision. A mass exclusion requires a justified sampling/noise/orbital analysis; no such epoch-RV analysis was supplied. See the [official Gaia definitions](https://gea.esac.esa.int/archive/documentation/GDR3/Gaia_archive/chap_datamodel/sec_dm_main_source_catalogue/ssec_dm_gaia_source.html) and `gaia_hosts.txt`.
6. **Retrospective holdouts are not untouched preregistered tests.** `vet.py` first loads/detrends using the candidate ephemeris and later splits years; its `blind_test` has candidate-alias selection and a full-data-shape fallback. Its `ok` field denotes a computable check, not automatically a pass of the later outcome rules. The quoted positive excesses are useful consistency evidence, but “blind 4/4” or “2/2” should not imply four/two independent prospective confirmations. I checked the code and stored results, not all training-fit executions.

## Were the internal-review corrections actually made?

| Earlier issue | Current state, independently checked |
|---|---|
| 183374279 depth/radius/catalogue source | Main dossier and README substantially corrected; depth values reproduced. Density convention and interpretation of the radius range still need clarification. |
| 183374279 partial S106 transit / availability | Partial-transit arithmetic is correct. Availability paragraph is now stale relative to the dated erratum; proposed edge-rule eligibility outlook also needs updating if adopted. |
| 183374279 pixel errors and SPOC significance | Numerical corrections reproduced. Blanket spatial exclusion and ambiguous “empirical σ” remain stronger than verified. |
| 61310956 duplicated timings | **Fixed in v3**; four unique sector rows, fit/checksum reproduced. Dossier still showcases v2 without a clear current-version replacement. |
| 61310956 SPOC independence / public-history wording | **Fixed in README and v3 description, not in DOSSIERS**. Tag history confirms the public row. |
| 61310956 ground reference duration and observing support | **Not fully fixed**: v3 still freezes 2.70 h while describing 3.3 h; ~7 h does not cover the full uncertainty plus stated baselines. |
| 61310956 additional pixel sectors | Main README/v3 numbers match the rerun. The supplied S72 raw-aperture figure remains unexplained. |
| Prior-search placeholders/counts | Main PRIOR_SEARCH report has a completion note and substitutions; separate VERDICTS still contains `GH_PLACEHOLDER_1/2`, and LIMITATIONS retains inconsistent old corpus counts. Reconcile before citing exact counts as audited. I did not independently recount every corpus. |
| Internal report's proposed “below 0.015” for FPP 0.031 | That proposed sentence was arithmetically wrong. Current README correctly says **above**; retain the corrected wording. |

## Novelty searches performed and their limits

I performed fresh exact-TIC, period/alias and host-name web searches, plus GitHub-/Zenodo-restricted searches. I found no relevant independent earlier report in the returned results. I also directly queried:

- [ExoFOP TOI export](https://exofop.ipac.caltech.edu/tess/download_toi.php?sort=toi&output=csv): HTTP 200, 8,151 rows; no target or 60″ match.
- [ExoFOP CTOI export](https://exofop.ipac.caltech.edu/tess/download_ctoi.php?sort=ctoi&output=csv): HTTP 200, 5,138 rows; no target or 60″ match.
- Zenodo `/api/records?q="183374279"` and `q="61310956"`: each returned one current metadata hit, the authors' own protocol v1.3 [record 23477866](https://zenodo.org/records/23477866). Metadata search is not full-text absence proof. Separate record-creation queries succeeded for [23460915](https://zenodo.org/records/23460915), [23461948](https://zenodo.org/records/23461948), [23463569](https://zenodo.org/records/23463569) and [23474130](https://zenodo.org/records/23474130): created respectively **2026-10-18 23:24:53 UTC**, **October 19 00:57:28**, **03:35:15**, and **12:16:10**. These agree with the approximate release chronology; I did not re-download their archived file bundles. Results are in `own_record_dates.json`.
- GitHub code-search API for each number: **HTTP 401**, so I do not claim an independent authenticated code-search sweep. General indexed web searches are incomplete for new repositories/files.
- NASA Exoplanet Archive TAP `toi` and `pscomppars` queries: **HTTP 526** in this session. I therefore could not independently verify the current Archive absence. The local sweep's cached absence remains a dated claim, not a fresh result here.
- Gaia DR3 TAP for the two host source IDs: HTTP 200, independently confirming the flags/RV summaries above. Query and URL are saved in `public_checks_summary.json`/`public_checks.py`.

The existing `PRIOR_SEARCH_round2.md`, `VERDICTS_round2.md` and `LIMITATIONS_round2.md` show a broad search of matching periods/aliases and nearby sources, but acknowledge incomplete ADS full text, indexing lag, metadata-only services, restricted survey coverage and failed services. A no-note count from public ExoFOP JSON cannot establish that no authenticated/private note exists; LIMITATIONS' assertion that “nothing was hidden” is unsupported by that count. Absence of a prior report should always be bounded to searched sources and date. I did not repeat the full hundreds-of-repositories/records sweep or certify its exact corpus totals.

## Checks performed and their limits

- Independent weighted ephemeris/covariance refits, actual SHA-256 calculations, BJD_TDB-to-geocentric-UTC inversion and site-altitude grids: `/tmp/dossiers_external_review/ephemeris_visibility.py`/`.log`.
- Independent QLP SAP/detrended processing, depth/odd-even/secondary statistics, narrow period checks, SPOC known-ephemeris measurements, phase-noise checks and blind periodograms: `photometry.py`/`.log`. These reproduce key values but do not exhaustively search aliases or rerun every shape posterior.
- Per-event raw-SAP baseline sensitivity: `event_checks.py`/`.log`. No observed S106 flux entered any calculation.
- Rerun and audit of the supplied earlier-sector centroid calibration: temporary `pixel_check.py`, `pixel_calib2.py` and log. I inspected both vet-summary images and the S72 pixel figure; I did not claim that rerunning a flawed injection design validates its confidence coverage.
- Independent JPL projection plus guarded cadence alignment on cached S103/S105: `clock_check.py`/`.log`. No test-sector clock tool was invoked with `--declared-test`.
- Public catalogue/metadata requests and local public-tag history checks, with failures explicitly reported above. Network outputs were written only under `/tmp`; no publishing, uploading or contact occurred.

The snapshotted dossier, README, outcome-table and two-target product hashes were unchanged at the end of this review (`/tmp/dossiers_external_review/input_hashes.json`, checked with SHA-256).

These checks support retaining both objects as **unvalidated transit-like candidates**, with revisions. They do not establish planetary masses, eliminate unresolved blends, certify novelty globally, or replace the protected prospective tests. Frozen CSV bytes should remain intact; corrections should be dated and versioned, and the current dossiers/README should identify which numerical products and rules actually govern.
