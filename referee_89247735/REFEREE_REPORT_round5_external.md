# Round-5 external referee report — 2026-10-19

**Reviewer/tool:** GPT-6 Codex, using local Python/Astropy/NumPy, Poppler, and read-only JPL Horizons, MAST, SIMBAD and GitHub queries. **Scope:** the corrections after round 4, not a new survey-wide validation. I opened the round-4 report and response, `round3_fixes/main_before_round4.tex`, the current `paper/main.tex` and ten-page `paper/main.pdf`, the relevant tables, clock scripts and JSONs, ephemerides, prediction CSVs, and local FITS. Only this report was written in the repository; nothing was published or sent to another person.

## Recommendation: Minor revision for the focused correction release

The central correction is now physically sound: my independent spacecraft-vector calculation gives **+7.533125 min**, agreeing with the saved **+7.533022 min** to 0.006 s. Independent checks of TIC 258006047 and TIC 183374279 also reproduce their event corrections to within 0.013 s. The v5 fit, checksum, contact duration and nominal CTIO visibility flags reproduce. The neighbour normalization, conditional radius wording, quality percentages and SIMBAD wording have substantially improved. Nevertheless, **the proposed v1.9 set should not be published unchanged**: its addendum incorrectly says every shift is ≤1.2σ, misgroups S102 with the substantial nonzero-correction cases, and misattributes the S100–S101 behavior to the later position/velocity mix-up. There are also small but definite manuscript/response inconsistencies and an inadequately specified background diagnostic. These require corrections and clearer labels, not another wholesale timing analysis. This recommendation concerns an accurately labelled correction release and unvalidated candidate account; it is not acceptance of the present manuscript as an AJ discovery paper. Evidence for these conclusions is specified below.

### Verification identifiers

All local paths are relative to `/Users/fernando/Desktop/NASA`. Page references use the **current** PDF. Each identifier below refers to files actually opened and computations performed in this round.

- **[M] Text/PDF:** `results/referee_89247735/REFEREE_REPORT_round4_external.md`, `RESPONSE_round4_external.md`, `round3_fixes/main_before_round4.tex`, `paper/main.tex`, `paper/main.pdf`, `paper/refs.bib`, `paper/tables/*.tex`, `paper/make_figure1.py`, and `paper/README.md`. I used `diff -u`, `rg`, and `pdftotext -layout paper/main.pdf -`; rendered and visually inspected current PDF p. 4 with `pdftoppm`.
- **[C] Clock:** `scripts/qlp_clock_v2.py` and all eight `results/qlp_clock_v2/*.json`. Independent FITS/JPL checks used TIC 89247735 S66/S93/S104, TIC 258006047 S65/S99/S100/S101/S102, and TIC 183374279 S69/S96/S103/S105. Files were selected from `data/qlp*/hlsp_qlp_tess_ffi_sSSSS-TTTTTTTTTTTTTTTT_tess_v01_llc.fits` and matching `data/lk_cache/clockcheck/<TIC>/**/tess-sSSSS-*_astrocut.fits`; the original 89247735 cutouts under `data/lk_cache/tesscut/` were also used. I additionally inspected the FITS offsets for TIC 333735955 S100/S101. No original clock script was run, because it writes outputs/downloads files.
- **[E] Ephemeris/predictions:** `scripts/final_ephemeris_89247735_v5.py`, `results/vet_qlp/89247735/final_ephemeris{,_v2,_v4,_v5}.json`, `predicted_transits_2026_2027{,_v5}.csv`, and the local registration documents. I independently solved weighted least squares, propagated its covariance, computed SHA-256, inverted barycentric light time iteratively, and calculated CTIO target/Sun altitudes.
- **[S] Other prediction shifts:** `scripts/qlp_clock_v2_shifts.py`, `results/qlp_clock_v2/shifts.csv`, `ADDENDUM_QLP_CLOCK_2026-10-19b.md`, each JSON's referenced original ephemeris, and the corresponding `results/vet_allsky/<TIC>/predicted_transits_2026_2027_v2.csv` and `PREREGISTRATION_v2.md`. I independently fitted the timing corrections as a linear perturbation, avoiding subtraction of two large Julian dates.
- **[D] FITS diagnostics:** the original S66/S93/S104 QLP files for TIC 89247735, read with `astropy.io.fits`. Flag masks use finite TIME/SAP_FLUX and the adopted v5 event centres. Background/position calculations use the original S93 `TIME`, `SAP_BKG`, `SAP_X`, `SAP_Y` at epoch 118; exact windows are given below.
- **[F] Shape:** `scripts/refit_89247735_v4.py` and `results/vet_qlp/89247735/refit_v4_{fixed_b1,fixed_b2,prior_b1}.json`. I recalculated nominal geometry, radii and quantile differences, and ran only the read/optimization prefix of the script in memory with the v5 clock/period substituted, stopping before MCMC/output writes. I did not regenerate the posterior chains.
- **[W] External checks:** fresh calls to [JPL Horizons](https://ssd.jpl.nasa.gov/api/horizons.api), the [MAST QLP notice](https://archive.stsci.edu/hlsp/qlp), [SIMBAD TAP](https://simbad.cds.unistra.fr/simbad/sim-tap/sync), and the [author's public GitHub tree](https://api.github.com/repos/fergmolina/tess-transit-candidates/git/trees/main?recursive=1). The public tree returned SHA `c4e559468053392eb02a607b6f6bc4a72ef66e87` at inspection. That is a snapshot, not an inspection of an assembled future v1.9 archive.

## Round-4 issues table

The first table covers the four major and twelve numbered minor issues in round 4. The following rows cover distinct numerical/cumulative items that were not separately numbered there. “Fixed” by qualification does not mean an excluded false-positive scenario has now been tested.

| Round-4 issue | Status | Evidence in the actual revised files |
|---|---|---|
| Major 1: target versus FFI-reference barycentric correction | **Fixed in the principal result** | §3.2 p. 3 now reconstructs spacecraft time and projects JPL TESS vectors on the target. +7.533 min independently reproduces. The former +8.02 derivation is explicitly superseded. Implementation/uncertainty qualifications remain below. [M,C,W] |
| Major 2: neighbour dilution and duration-ratio argument | **Partial** | §4.2 pp. 5–6 now uses target-normalized depths and explicitly labels Gaia G as a TESS proxy. The 28–31% arithmetic and k≤0.11 constraint reproduce. The literal “at most ≈1.2% of the host's light” omits limb darkening; it is an area/uniform-brightness estimate. General EB configurations remain expressly untested. [M,F] |
| Major 3: conditional radius, classification and convergence | **Partial** | §3.3 pp. 3–4 calls 7.9–8.5 R⊕ a span of conditional medians, includes the concurrent 8.7 R⊕ result, and admits no convergence documentation. Summary p. 9 now lists possible interpretations rather than “either.” No new dilution posterior or chain diagnostics were supplied. The unquantified “less likely” qualifier is still a judgment rather than a computed probability. [M,F] |
| Major 4: SIMBAD and archive completeness | **Partial** | §4.5 p. 7 correctly says the star exists in SIMBAD; my fresh query returns it. Acknowledgments p. 9 narrow the archive claim, but still say the timing/fit products and a number-to-file manifest “are public.” The inspected public tree does not yet contain the proposed v5/new-clock/fit products; no such manifest was located in the inspected paper/referee paths. The planned release may remedy availability, but does not do so in advance. [M,W] |
| Minor 1: T0–P correlation | **Fixed** | Table 2 p. 5 says 0.84; independent v5 covariance gives 0.835881527. [M,E] |
| Minor 2: a and Teq derivations | **Fixed** | Table 2 now gives 0.119 AU and 544 K from the fitted a/Rstar and TIC radius, and distinguishes the 0.120 AU/541 K Kepler estimates. Direct calculation gives 0.119138 AU/543.88 K. [M,F] |
| Minor 3: SED radius uncertainty | **Fixed** | Table 2, §3.3 and §5 consistently use ±0.45 R⊕; saved propagation is 0.448789 R⊕. [M,F] |
| Minor 4: k and a/Rstar error rounding | **Partial** | Table 2 has +0.0020 and −2.3, as requested. §3.3 p. 3 still has +0.0021 and −2.2. [M,F] |
| Minor 5: alias/coprime logic | **Fixed** | §4.1 p. 5 now attributes rejection to missing events for n=2–12, says larger n were not tested, and calls P the longest common identical-event period. [M; direct arithmetic of epoch differences] |
| Minor 6: nonexistent Figure 1 background panel | **Partial** | §3.1 p. 2 no longer cites Figure 1 as a background plot. It substitutes a new scatter-ratio claim, but does not define its windows or distinguish it clearly in the response from a significance. The claim can be reproduced for one specific window; details below. [M,D] |
| Minor 7: independent pipeline coverage | **Fixed** | Summary p. 9 specifically names TARS and its three covered events. The ambiguous all-four claim is removed from the shortened abstract. [M] |
| Minor 8: epoch range for prediction differences | **Partial** | §§3.2/6 explicitly specify epochs 146–163, but generated macros still omit epoch 163 and print +4.3 to +5.4 min. Correct endpoint is +5.5 min after rounding. [M,E; `range(146,163)` in `paper/make_figure1.py`] |
| Minor 9: observability and second-band wording | **Fixed at the claimed nominal precision** | §6 p. 8 defines CTIO thresholds, identifies epoch 159 as full and epoch 162 as narrowly failing, and changes “establish achromaticity” to a consistency check. My nominal calculation agrees, with the caveat that 162 misses by only 0.0025°, not the response's 0.03°. [M,E] |
| Minor 10: timing/concurrent/software citations | **Partial** | JPL and the MAST notice are named in the text, but the exact timing provenance still rests on scripts rather than an explicit reference/link in the manuscript. `zarco2026` still combines an initial commit, later v1.1 and a concept record without assigning each borrowed result to its version. Lightkurve still lacks a citation. [M] |
| Minor 11: stale source macros / response page count | **Partial** | The response correctly says ten pages. Old unused macros such as `rhofit=1.18`, `aAU=0.113`, `Teq=559` remain, and the generator still emits them from old `report.json` fields. They are not the displayed Table 2 values. [M] |
| Minor 12: abstract/formatting | **Partial** | Current rendered abstract has approximately 222 whitespace-delimited tokens, versus the response's 210; it is shortened below the ordinary 250-word ceiling. The ten-page/two-figure/two-table draft still is not RNAAS format, and AJ referee line numbering remains absent. This does not block a correction data release. [M; format comparison with the requirements documented in round 4] |
| Round-4 error table: S104 flags 27/139 and S93/118 count 235 | **Partial** | Direct counts and table rows are now 27/139/235, and §3.2 gives the correct 34-before/78-after split. **Table 1's note on p. 4 still says 28.** [M,D] |
| Round-4 error table: quality-mask percentages | **Fixed** | §7 p. 9 distinguishes bit 31 (19/18/25%) from any nonzero QUALITY (30/20/25% of all rows). Independent FITS fractions reproduce the rounding. [M,D] |
| Round-4 error table: obsolete contact duration | **Fixed** | v5 reads 4.536242314887044 h from the nominal shape JSON, which rounds to 4.54 h. It no longer uses the older 4.524342-h fit. [E,F] |
| Round-4 S105 finding / wider clock application | **Fixed numerically for checked products; partial explanatory text** | TIC 183374279 S105 correction +3.266053 min reproduces. The revised addendum explicitly supersedes v1.8 and explains the wrong TESScut premise. Its S100–S102 versus S103–S105 grouping needs correction below. [C,S,W] |
| Cumulative: unsupported centroid/EB/Gaia mass exclusions | **Fixed by withdrawal; retained** | Abstract, §4.2, Figure 2 caption and summary retain the open-neighbour/unconstrained-mass interpretation. No new calibrated two-hypothesis centroid test, EB fit or RV mass measurement is claimed. §5's unresolved-host argument is now explicitly conditional on a dark-transit model. [M] |
| Cumulative: v1 test of record and chronology | **Fixed; retained** | §6 p. 8 preserves v1 as the test of record and labels v4 superseded/v5 a refinement. Frozen CSV hashes match the registration documents. This verifies local integrity, not independent authentication of discovery/freeze chronology. [M,E,S] |
| Cumulative: QLP acknowledgement/TARS release/draft housekeeping | **Partial** | Requested complete MAST acknowledgement and exact TARS release identification remain editorial work. The product/article and Kunimoto citation distinctions remain correct in the source; the draft header itself is not a scientific defect. [M; MAST page in W] |

## New issues

### 1. Clock physics is correct; the uncertainty and implementation should be described accurately

The appropriate calculation is

`t_sc = TIME_cut − TIMECORR_cut`

`LTT = dot(r_TESS(t_sc), n_target)/c`

`correction = LTT + c0 − (TIME_QLP − t_sc)`.

This is the method described in the new script. It preserves the empirically measured approximately two-second QLP convention instead of pretending that TESScut TIME is already target-barycentric. [C]

For an independent check I matched integer cadence sequences, not nearest timestamps: QLP `CADENCENO−CADENCENO[0]` against the reconstructed spacecraft sequence `round((t_sc−t_sc[0])*86400/200)`, with gap positions used to check the alignment. Equal-length lists have matching increments in the checked sectors. In TIC 258006047 S102 the cutout has **10442** rows versus **10420** QLP rows; the integer match accounts for the missing samples rather than pairing whole arrays. TIC 183374279 S105 has **11652** cutout rows versus **11723** QLP rows, with matching shared cadence sequence and three gap anchors. Thus neither difficult case depends on choosing the nearest 200-s cadence. [C]

I obtained fresh vectors from [JPL Horizons](https://ssd.jpl.nasa.gov/api/horizons.api), using TESS `COMMAND=-95`, Solar System barycentre `CENTER=500@0`, `EPHEM_TYPE=VECTORS`, `REF_PLANE=FRAME`, `REF_SYSTEM=ICRF`, `OUT_UNITS=AU-D`, and TDB Julian-date queries at reconstructed spacecraft times. I projected them onto each JSON's RA/Dec. Some initial batch requests failed; the smaller retry queries below succeeded. [C,W]

| TIC / sector | QLP minus spacecraft (min), independently measured | Independent target LTT (min) | Independent convention-preserving correction (min) | Saved correction (min) |
|---|---:|---:|---:|---:|
| 89247735 / 104 | −0.085101883 | 7.415380761 | **7.533124870** | 7.533021825 |
| 258006047 / 99 | −2.573768058 | −2.606135366 | 0.000280101 | 0.000072641 |
| 258006047 / 100 | −2.084876598 | −0.788244030 | 1.329279977 | 1.329094353 |
| 258006047 / 101 | −2.084876599 | 1.629201689 | 3.746725697 | 3.746543839 |
| 258006047 / 102 | −0.020273999 | 3.746545804 | 3.799467213 | 3.799412252 |
| 183374279 / 103 | −0.052310524 | −3.334289885 | −3.250005976 | −3.249979944 |
| 183374279 / 105 | −0.051646265 | 3.182407497 | 3.266027146 | 3.266053084 |

The independently sampled c0 values are **0.032642226 min** for 89247735 (S66/S93), **0.032647409 min** for 258006047 (S65), and **0.031973385 min** for 183374279 (S69/S96). The largest saved-versus-independent difference in this table is **0.01245 s**. These verify the target correction and two other objects, including the requested S100–S102 case. The near-zero S99 correction is specifically for the sampled event; it is not a claim that all S99 is unaffected. [C,W]

There are four modest implementation limitations:

1. **JPL evaluation time:** the script actually calls `ltt(t_QLP,...)`, not `ltt(t_sc,...)`, including for controls. My calculation uses t_sc. The discrepancy is negligible here (table above), but the implementation should match its derivation rather than relying on the small derivative. [C]
2. **Duplicate controls:** `89247735.json` lists S93 twice, and `467959906.json` lists S94 twice. The sector list is built from two cache directories without deduplication. These are repeated observations, not two independent control sectors. For 89247735 I independently checked S66 as well; it agrees. Use unique sector IDs and record the exact input path/hash. [C; local glob results]
3. **“Clean” control range:** the code labels S56–S98 suitable controls but selects v01 files, although the MAST notice identifies a separate S74–S79 v01 timing error. None of the eight current JSON control lists uses those sectors, so this does not invalidate their numbers. It is a genuine reuse hazard in the released script. Exclude affected versions or validate every chosen control. [C; MAST notice in W]
4. **Matching assertion:** equal length alone is not proof of identical cadence lists. My checked cases pass an increment/gap check; the script should enforce it. For unequal lengths, the current gap-edge interpolation is adequate in the checked S102/S105 cases because QLP−spacecraft is effectively constant, but should not be assumed exact for an arbitrary time-varying error. [C]

**0.05-min clock uncertainty:** three seconds is a reasonable conservative **allowance** for this verified S104 correction. The independently sampled S66/S93 convention residuals range only from **0.032618977 to 0.032663082 min**, and the saved correction differs from mine by 0.006 s. Nothing in these checks suggests a remaining half-minute clock error. However, the script/JSON does not derive a calibrated Gaussian 1σ of three seconds or document an absolute spacecraft-timing error budget. Label it as an adopted conservative systematic allowance and give these checks, rather than imply it is a measured statistical uncertainty. I did not independently calibrate the underlying spacecraft clock or JPL trajectory errors. [C,W; §3.2 and v5 error terms in M,E]

### 2. The revised addendum's summary is false as written

**“Every shift is at most 1.2σ.”** `qlp_clock_v2_shifts.py` explicitly skips TIC 89247735. For the other seven objects I reproduce every saved shift to within **3.2×10⁻⁹ min**. Their maximum ratio using the CSV's rounded frozen errors is **1.18112**; reconstructing the frozen covariance for the limiting TIC 333735955 gives **1.18362** at epoch 259. Thus ≤1.2σ is supported for that seven-object set. [S]

But the addendum's table includes TIC 89247735, and its v5−v1 differences over epochs 146–163 are **4.282513–5.460341 min**. With the unrounded v1 covariance these are approximately **1.256–1.376σ**, with the maximum at epoch 146. The correct all-eight statement is approximately **≤1.4σ**, or report the separate ranges. The response repeats the erroneous ≤1.2σ statement. This is a release blocker because it is a quantitative headline of the correction. [S,E,M]

**Sector grouping and cause.** The addendum says S100–S102 have a wrong nonzero term, “consistent with the position/velocity mix-up,” unlike S103–S105 with none. For TIC 258006047, S100 and S101 carry an almost constant **−2.084877 min**, whereas S102 carries only **−0.020274 min = −1.21644 s**. The latter is effectively missing its approximately **3.74655-min** target barycentric term, in the same practical sense as the few-second residuals in S103–S105. For comparison TIC 333735955 has approximately **+4.6048/+4.6041 min** in S100/S101, also a substantial spurious term. [C]

The [MAST notice](https://archive.stsci.edu/hlsp/qlp) attributes the earlier problem to an expired ephemeris/interpolation failure and dates the position/velocity-column mix-up from **Orbit 215, the first half of S102**. Therefore the S100–S101 offsets should not be attributed to that later mix-up. Describe the measured product/event behavior rather than a categorical all-stars sector rule. Also change “within 5 s” to “within about 5 s” or give the residual: 89247735 S104 is **5.1061 s** away. [W,C,S]

**Supersession:** this part is correctly done. The first paragraph explicitly says the new addendum supersedes `ADDENDUM_QLP_CLOCK_2026-10-19.md (v1.8)` and explains the mistaken target-specific TESScut premise. Retain that paragraph. [S]

**No outcome-rule changes:** no change is needed merely to accommodate the checked shifts; all are smaller than the applicable stated windows. I verified that all eight frozen CSV SHA-256 values still match their local registration documents, and the new scripts read rather than overwrite them. However, an unchanged rule must still be evaluated around the **frozen prediction**, with the corrected prediction reported separately. A small shift does not logically guarantee that a future marginal observation will receive the same classification if the window centre is moved. There are no new observed outcomes in this audit, and I cannot certify historical byte-for-byte invariance of every prose rule from local hashes of CSVs alone. [E,S]

### 3. The new background/position claim is reproducible only as a specified scatter ratio

The manuscript now says “less than 0.4 times their scatter,” while the response calls it “<0.4σ.” Those are not interchangeable descriptions of a mean shift. [M]

Using the original S93 FITS, `tc=3830.347133333333`, all quality flags, **in-transit |t−tc|<2 h**, and **out-of-transit 2 h≤|t−tc|<0.4 d**, I obtain 72 in-transit and 273 baseline samples:

| Column | Mean(in) − mean(out), native column units | Baseline sample standard deviation | Difference / baseline scatter |
|---|---:|---:|---:|
| SAP_BKG | −2009.337248 | 5090.448941 | **−0.394727** |
| SAP_X | +0.006648957 | 0.022302432 | **+0.298127** |
| SAP_Y | +0.002693167 | 0.012029283 | **+0.223884** |

Thus the literal scatter statement can reproduce. But a baseline with a one-hour guard (`3 h<|t−tc|<0.4 d`) gives **−0.426905,+0.325844,+0.258512**, so the background no longer satisfies <0.4. The time window matters because the baseline contains a ramp. Moreover, the naive independent-sample standard errors of the mean would give ratios approximately **−6.40,+4.78,+3.53**, not <0.4. Those are **not calibrated detection significances either**, because the trend and correlation invalidate that naive model. [D; direct NumPy means, `std(ddof=1)`, and standard-error propagation]

**Fix:** specify windows, statistic and detrending; publish the small diagnostic table or code. Call these ratios to per-cadence baseline scatter, not σ evidence for absence of an in-transit excursion. A trend-aware comparison is needed if this is meant to exclude an instrumental explanation. This issue does not negate the separate transit-shape and field-control evidence, which I have not re-run in this focused round. [D,M]

### 4. Do not confuse historical fit products with a new v5 shape posterior

The old +8.02 references in §3.2, the Table 2 note and the v4 history bullet are intentional and mostly correct: the shape posterior remains `refit_v4_*.json`, and its correction is explicitly disclosed. They should not be mechanically changed to +7.53 without a refit. Figure 1 uses the v5 ephemeris/timestamps with the old shape parameters, as the actual `paper/make_figure1.py` confirms. [M,F]

As a limited sensitivity check, substituting v5 into the optimization prefix gives χ² **1547.402325**, with maximum-likelihood `k≈0.0984365`, `a/Rstar≈32.0422`, `b≈0.34921`; the previous optimizer had χ² **1547.291844**. This small change does not compel a new MCMC merely for an honest data-correction release. It does not establish convergence of the existing chains. Archive the JSONs under their true configuration names and do not call them a newly sampled v5 posterior. [F]

The line that “re-timing with the final shape moves the event times by ≤0.3 min” should identify which clock convention was used for that comparison. In round 4 the ≤0.3-min calculation was conditional on the then-adopted clock; the separate change of the S104 clock from v4 to v5 is **−0.489368 min**. These are different effects and should not be conflated. [M; v4/v5 correction fields in E; round-4 report]

## Factual and numerical errors

| Location / claim | Correct value or qualification | Verification |
|---|---|---|
| Revised addendum and response: all shifts ≤1.2σ | For all eight, approximately **≤1.4σ**; 89247735 reaches **1.37627σ** using unrounded v1 errors. Seven objects in `shifts.csv` satisfy ≤1.2σ. | [S,E], independent perturbation fits and covariance propagation. |
| Addendum: S100–S102 substantially nonzero, unlike S103–S105 | Checked 258006047 S100/S101: **−2.084877 min**; S102: only **−1.21644 s**, effectively missing the target term. State product-specific behavior; do not put S102 in the same substantial-offset group. | [C], matched cadence IDs and raw FITS subtraction. |
| Addendum attribution to position/velocity mix-up for S100–S101 | MAST dates that mix-up to **S102 / Orbit 215**; the earlier issue involved ephemeris range/interpolation. | Fresh [MAST notice](https://archive.stsci.edu/hlsp/qlp), [W]. |
| Addendum: S103–S105 within 5 s of spacecraft time | For target S104, **−5.106113 s**. “About 5 s” is accurate. | [C], QLP−(TESScut TIME−TIMECORR). |
| `89247735.json`: two control entries S93; `467959906.json`: S94 twice | Each pair is one distinct sector duplicated, not two controls. Deduplicate the input sector list. | [C], JSON contents and cache globs. |
| Table 1 note, p. 4: 28 flagged in central S104 ±2 h | **27 of 72**. §3.2 already says 27. | [D], finite-SAP/time masks centred on v5 Tc. |
| §3.3 p. 3: k upper error +0.0021; a/Rstar lower error −2.2 | **+0.0020 and −2.3**, consistent with Table 2. Unrounded differences are 0.002033742 and 2.27292182. | [F], saved 16/50/84 percentiles. |
| §§3.2/6 rendered +4.3 to +5.4 min at epochs 146–163 | **+4.282513 to +5.460341 min**, hence **+4.3 to +5.5**. | [E]; `paper/make_figure1.py` uses `range(146,163)`, excluding 163. |
| Abstract p. 1 / summary p. 9: residuals ≤1 min | Maximum absolute v5 residual is **1.027670 min**. Use “about 1 min,” “≲1 min,” or “≤1.03 min.” | [E], independent WLS and v5 JSON. |
| Response: epoch 162 misses solar-altitude threshold by 0.03° | With the actual stored **T14=4.5362423 h**, ingress Sun is **−11.99754°**, a miss of **0.00246°**. Rounding duration to exactly 4.54 h is enough to alter such a tiny margin. | [E], iterative geocentric contacts and CTIO AltAz. |
| Response: new background diagnostic <0.4σ | Reproduces as **−0.3947,+0.2981,+0.2239 times baseline scatter** for the specified 2–9.6-h baseline; it is not a mean-shift significance. | [D], table and alternative window in New issue 3. |
| §4.2 p. 6: k≤0.11 blocks at most ≈1.2% of host light | Approximately **1.16–1.23% of projected area** under the simple geometry. Uniform surface brightness converts that to flux; limb darkening changes it. Using the target's adopted coefficients gives a small-central-disk estimate ≈1.45% for k=0.10759. This does not rescue a 30% dark-body eclipse. | [F], q=0.8057198, kmax=0.1075916; central intensity/mean intensity `1/(1−u1/3−u2/6)`. This is illustrative, not a fitted neighbour spectrum. |
| Response: abstract 210 words | My `pdftotext` extraction gives approximately **222 whitespace-delimited tokens**. Counting conventions differ; it is nevertheless below 250. | [M], extract between ABSTRACT and Keywords. |
| `final_ephemeris_89247735_v5.py` console says “v4:” | Should say **v5**. The output file names and JSON note correctly say v5. | [E], source read. |
| `paper/make_figure1.py` docstring says v3 | Actual data source is **v5**, shape source **v4**. Update the docstring; its `v3` variable name is confusing but not a numerical error. | [M], source read. |
| Acknowledgments: current products/manifest “are public” | They are **planned for v1.9**, not present in the inspected public snapshot. Include an actual manifest and update the claim after release. | [W], public tree SHA above; local manifest search [M]. |

The following requested numbers **are correct**, not errors: neighbour depth **28.46–31.31%** under the stated G-band proxy; nominal duration ratio **0.805720** and kmax **0.107592**; flag totals **0/235/8/139** for the four ±10-h windows; S104 split **34 before / 27 central / 78 after**; any-nonzero QUALITY percentages **30.4920/19.6252/24.8953%** of all S66/S93/S104 rows; bit-31 percentages **19.1048/17.7424/24.8953%**; Table 2's correlation, a, Teq and SED radius uncertainty. These were recalculated from [D,F,E], not accepted from the response.

## Is the v1.9 release set safe to publish as supplied? **No**

This is a **temporary, specific hold on misleading release claims**, not a request to withhold valid corrected data. I would clear a corrected, accurately labelled release after these items:

1. **Correct the all-eight shift statement** in the addendum and response, explicitly include 89247735 in its significance accounting, and preserve the distinction between frozen outcome windows and refined observing predictions. [S,E]
2. **Correct the sector behavior/causal description** in the addendum: distinguish the substantial S100–S101 offsets from the few-second S102 residual in the checked product, and place the MAST position/velocity mix-up at S102. Avoid claiming a universal property from the limited tested products. [C,W]
3. **Correct or annotate the response's inaccurate completion statements:** Table 1 still says 28; the prose still has the old quantile rounding; the rendered endpoint is +5.4; the background number is a scatter ratio; the August altitude miss is approximately 0.0025°. A response presented as a factual description of the final files should not say these are all fixed. If preserving it as a historical document, include a dated correction rather than silently rewriting history. [M,D,E]
4. **Supply the actual release manifest and configuration labels.** Include the v5 CSV/hash and dependencies, clock JSON input paths/versions, the v4-configured fit JSONs as such, and explicit supersession labels on obsolete timing products. Deduplicate the control-sector records so they do not imply independent controls that were not used. I have inspected the listed local components, not an assembled v1.9 ZIP, and cannot certify files that have not been supplied as that bundle. [C,E,F,M,W]

The **v5 ephemeris/CSV themselves need no numerical change on the evidence of this audit**. It is acceptable to release historical referee reports, responses and fit products if their dates, configurations and supersession status are explicit. Undocumented MCMC convergence and missing full EB/localization models remain limitations of the scientific interpretation; they need not prevent archiving an expressly unvalidated candidate's corrected data. For journal acceptance, the quantitative posterior claims still need adequate diagnostics and the manuscript needs a final consistency pass. [E,F,M]

## Checks performed, and their limits

### Independent v5 fit and hash

From the four saved times/errors I used `A=[1,epoch−138]`, `cov=(A.T W A)^−1`, `beta=cov A.T W t`, without shrinking errors for χ²/dof<1. Results:

- **T0 = 4196.809908119191 BTJD**, σT0 = **0.001317665843438 d**;
- **P = 18.323174422287 d**, σP = **0.000040197306640 d**;
- correlation **0.835881526993**, χ² **0.365983578**, 2 degrees of freedom;
- residuals **−0.092934,+1.027670,−0.482058,−0.513870 min**.

The adopted S104 midpoint **4196.809551265156** follows from the saved original midpoint plus the independently supported correction. Its quadrature uncertainty is **4.213989 min** (the JSON stores 0.002926380978323 d), consistent with 4.2 min after rounding. These reproduce the table's ephemeris entries and do not depend on the response. [E]

Using `hashlib.sha256(open(csv,'rb').read()).hexdigest()`, I obtain exactly:

`216e7a4c6a9863dbe7bbf0777e1638c083553b4eb146d2425a4ab0e1fd2153a5`

The required **216e7a4c** prefix and JSON hash match. The contacts use **4.536242314887044 h**, properly rounded to 4.54 h, rather than exactly substituting the rounded duration. [E,F]

### Geocentric UTC and CTIO

I independently solved `t_geo,TDB=BJD_TDB−LTT(t_geo,target)` iteratively, then converted to UTC and evaluated the contacts separately. Site: latitude **−30.169°**, longitude **−70.8063°**, height **2207 m**, no atmospheric refraction. IERS network updates were disabled for this calculation; the last millidegree is not a prediction of future weather/atmospheric observing conditions. [E]

| Epoch | Midpoint UTC | Ingress UTC | Egress UTC | Target altitude in/out | Sun altitude in/out | Nominal full? |
|---|---|---|---|---|---|---|
| 159 | 2027-06-25 02:10:03.080 | 2027-06-24 23:53:57.859 | 2027-06-25 04:26:08.302 | 30.92433° / 73.69520° | −25.61388° / −81.93175° | **Yes** |
| 162 | 2027-08-19 01:29:08.728 | 2027-08-18 23:13:02.906 | 2027-08-19 03:45:14.551 | 61.23914° / 57.35493° | −11.99754° / −67.56595° | **No, narrowly** |

The corresponding formal ephemeris errors are **2.98894 and 3.15228 min**. The CSV truncates its times to minutes, which explains ingress “23:53” despite being close to 23:54. Its rounded altitudes and boolean flags reproduce. Epoch 159 is the only `ctio_full=True` row in the file. I independently spot-checked these two events, not all southern sites or the global observability assertions. The epoch-162 yes/no boundary is much smaller than the timing/duration uncertainties, so the manuscript should continue to call it marginal rather than an assured observing distinction. [E]

### Limits of this focused review

- I independently checked physical clock corrections for the target and **two additional objects**, with extra FITS-offset inspection for TIC 333735955. I reproduced the **shift arithmetic for all seven additional objects**, but did not obtain fresh JPL vectors for all eight. [C,S]
- I read all eight clock JSONs and checked their control-sector lists. I did not calibrate JPL ephemeris accuracy, spacecraft clock hardware, or a universal convention applicable to every TESS product. The 0.05-min allowance assessment is specific to the checked method/product consistency. [C,W]
- I verified the FITS flag and new background/position calculations, and checked Table 2 arithmetic against the saved fit products. I did not rerun the entire candidate search, field-control ensemble, TARS extraction, centroid injections, EB models, RV inference, secondary-temperature integration, or MCMC chains. [D,F,M]
- A fresh SIMBAD query `SELECT main_id,ra,dec FROM basic WHERE main_id='SCR J1820-4533'` returned that name and coordinates **275.2236941035°, −45.56116735744°**. This confirms the repaired existence wording, not exhaustive absence of previous transit/variability reports. [W]
- I checked the revised source and rendered PDF for stale v4/+8.02 statements. The substantive remaining occurrences are historical or explicitly describe the still-v4 shape fit. I did not treat those honest configuration labels as errors. Source-console/docstring mistakes and remaining numeric inconsistencies are identified above. [M,E,F]
- I did not alter any original file, run a publishing command, contact a collaborator, or inspect an unpublished assembled release archive. The release verdict applies to the components and claims actually available here. [Recorded tool actions; scope of this report]
