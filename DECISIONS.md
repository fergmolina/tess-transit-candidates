# Decision log — TESS multi-year transit search (started 2026-10-17)

1. Environment: Python 3.12 venv (.venv) with lightkurve 2.6.0, astropy 8.0.2, numpy 2.5.4, scipy 1.18.1, batman, TLS 2.0.1, wotan 2.0, emcee, tess-point. Python 3.14 rejected (no batman/distutils).
2. Reference method (Rabtsevich 2026, Zenodo README): searched 126,246 stars (Tmag<=11.5) in S98, traced back to S6/S32 (FFI products), LEO-Vetter + TRICERATOPS FPP, archival false-alarm test with 20,000 fake-period trials, pre-registered S110 transit times (~4 min 1-sigma).
3. Target selection (this work): newest sector with SPOC 2-min LCs on MAST = S107 (12,998 targets, southern field dec -43..-9). Built TIC->sectors map from all 107 MAST bulk scripts (592,581 unique 2-min targets). Kept S107 targets with 2-min data in >=2 calendar years: 9,283. TIC query -> dwarf filter (Tmag<13.5, Teff<6000, R<1 Rsun or (R missing & Teff<4200), logg>4 or missing, lumclass!=GIANT): 1,637 targets, 6,720 LC files (14 GB).
   Rationale: small stars make shallow signals detectable; multi-year baseline is required by the brief; 2-min SPOC data allow 1-hour transits and TPF centroid vetting.
4. Known-signal exclusion set: TOI (8,151), CTOI (5,138), NASA Exoplanet Archive confirmed (6,144 w/ TIC), SPOC TCE stats tables for all 132 single+multi-sector runs (341,351 TCE rows, 75,503 unique TICs). Match by TIC and by period incl. 2x, 0.5x, 3x, 1/3x aliases (1% tol).
5. Search: per-sector biweight 0.5 d detrend, upward-only 5-sigma clip, quality==0, PDCSAP. Per-sector BLS (6-min bins, P 0.5-13 d) + stitched BLS (10-min bins, P 0.5-20 d, log-f grid oversample 2). SDE = (power - running median)/robust MAD. Ranking on stitched SDE, Ntr>=3, per-year depth consistency.
   Speed: 21 s/target after binning (was 150-350 s unbinned). 11 workers.
6. Positive control (TIC 4206066): both reported signals recovered as top-2 stitched peaks (see results/control_TIC4206066/CONTROL_SUMMARY.md). Single-sector SDE 7-9 only.
7. Early TLS attempt with use_threads=12 deadlocked in a multiprocessing pool on macOS; TLS is now run single-threaded and only in narrow period windows for refinement.
8. v1 search (no edge trim) found its SDE>9 'candidates' were all gap-edge ramps repeating at ~13.7 d (TESS orbit). Added trim_edges (0.3 d around gaps >0.25 d and sector ends) and restarted search as v2; v1 outputs kept in results/search_v1_notrim.
9. Ranking bug fixed: astropy BLS `depth_half` is the depth at P/2, not the secondary eclipse; `depth_phased` (model shifted by half a period) is the secondary. With the wrong statistic every known planet failed the "no secondary" cut. Odd/even cut relaxed to <5 sigma (two marginal known TOIs failed at 3 sigma).
10. TLS refinement on multi-year stitched data returned implausible durations (0.06-0.08 h) even for a confirmed planet (TIC 12421862); replaced by a fine-grid BLS refinement (P +-0.5%, 4001 steps, durations 0.5-1.5x). TLS kept behind --tls as an optional cross-check.
11. Mean in/out difference image is dominated by a pointing-jitter dipole for ~1000 ppm signals (seen on the confirmed planet). Replaced by (a) in-vs-out shift of SPOC MOM_CENTR1/2 after masked detrending (known planet: 0.8 sigma) and (b) per-pixel detrended depth map / flux-loss centroid (known planet: 0.46 px from target).
12. Blind test rewritten after advisor review: training years only -> fresh full BLS (same grid) must rank the candidate period in its top 3 -> training-only shape fit, transit times and linear ephemeris -> predicted holdout transits measured against a 1000-trial random-phase null. Known planet: rank 1 in all five holdouts, p<0.001.
13. Null calibration: inverted-light-curve (2-F) search per candidate (vet.py) and on a random subset of each pool (null_calibration.py) sets the empirical SDE threshold; SDE>9 alone is NOT a detection (median noise top-peak SDE ~8).
14. Pool B added: QLP FFI light curves for 3,413 bright dwarfs (Tmag<=11.5, Teff<=5300, R<0.85) in the newest QLP sector (S104); 21,222 files from sectors 1-104. QLP loader handles DET_FLUX/KSPSAP_FLUX and NaN error columns (sectors >=94).
15. Future transit windows use the official tess.mit.edu TESS_orbit_times.csv (through S111); tess-point 0.9.5.post1 has pointings through S134. Control star correctly maps to S110.
16. Pool A outcome: 17 filtered signals with SDE>9; 4 vetted in full. 299903841 = blend (SAP/PDCSAP 466/2738 ppm, centroid 9 sigma, pixel loss 39" off target). 313934283 = noise (inverted margin -0.7, not recovered in training years). 176798599 = 8 clean events in 2025-26 but every odd epoch in Cycle-8 data gaps; 2018 (S4) and 2020 (S31) FFI data exclude a 3000-ppm transit at the predicted phase (5-8 sigma) -> rejected (lesson: BLS over 1e6 periods will place missing epochs in gaps; always test archival sectors).
17. 317134140 (TOI-2514 host): 0.5719-d, ~185 ppm. Season-holdout blind tests pass (4/5 seasons at 2.8-7.6 sigma at exactly the predicted phase), S33 FFI blind BLS top peak, independent lightkurve pipeline recovers it in S98 and S107 alone, pixel/centroid/aperture tests on target, no secondary, odd=even, density consistent. Caveats: S32 non-detection (3 sigma below expectation; TOI-2514.01 is recovered there), depth chi2 18.5/5; TESS cannot exclude a 1.1437-d equal-eclipse EB companion within ~1". Known TOI-2514.01 itself is only recovered in 2020-21.
18. Ephemeris errors: grid-limited at first; fixed with a 2-stage grid + quadratic covariance in grid-step units (unscaled lstsq gave NaN). Jackknife spread of P is 2x the formal error; conservative 1-sigma 6 min quoted for S108-S110.
19. Null calibration v1 (inverted LCs, top peak only) is dominated by stellar-variability bumps (34% > SDE 9); v3 applies the identical physical + 2-year cuts to the inverted peaks.
20. Filtered null (400 inverted LCs, same cuts): max SDE 14.3; >=13.2 in 0.8%, >=14.3 in 0.2% -> ~4 false positives expected at the candidate's SDE across Pool A. Season-holdout blind test applied to the strongest inverted null signal (TIC 120896927) PASSES at 3-7 sigma -> the holdout test is not independent of a multi-year stitched selection. Only data outside the selection (FFI-only S32/S33 for 317134140; future S108-110) count as independent. Report revised (section 7.1).
21. Pool B (QLP) ranking showed strong period clustering (12.7-14.1 d and 18.9-19.9 d; 29% of SDE>9 top peaks in 12.5-14.5 d): FFI scattered-light systematics. Added a period-density flag (0.4% log bins, >5x local median and >6 objects) and the yrs_det>=2 / not-near-orbit cuts -> 106 clean survivors; 80 triaged.
22. triage.py crashed on single-event targets (GridSpec slice with ncol=1); fixed by ncol=min(6,max(2,nev)).
23. vet.py pixel tests are SPOC-TPF only. Wrote scripts/ffi_pixel_test.py (TESScut 11x11 cutout, per-event local-baseline depth map, flux-loss centroid, depth vs aperture radius) and scripts/tesscut_forward_test.py (own aperture photometry of later sectors, prediction vs random-phase null + blind BLS). Added EXCLUDE_SECTORS env var to vet.py for sectors with unusable QLP data.
24. Pool B vetting: 234520293 = 3/2 harmonic of its own SPOC TCE (0.37636 d); 367223147 (0.5303 d, top peak in 5 sectors over 7 years!) = off-target blend by depth map (loss centroid 1.4-1.6 px off, depth rising with aperture) and rho* 3x off; 469939201 = off-target + forward test in S96/S103/S104 with own photometry gives -57+-56 ppm where >=290 expected; 119221437 = off-target (1.15 px); 120707329 vanishes in 2026; 364788827 depth varies 225-3664 ppm (contamination 0.5).
25. TIC 89247735: three 34-41 sigma single-sector transits (S66, S93, S104) at P=18.3231 d. Aliases P/n (n=2..12) excluded by 4-43 covered empty epochs; coprime epoch differences (40, 19) make 18.32 d the longest period. On-target by TESScut depth map in all three sectors (loss centroid <=0.18 px; neighbour at 0.46 px would need 23% eclipses). Shape flat, rho* consistent, no secondary, SAP=DET, Gaia single, no catalog entry (TOI/CTOI/TCE/confirmed/ExoFOP). Classified as candidate pending RV. Ephemeris from 3 timings, predictions frozen (SHA-256 84fbf94d...). TESS will not revisit before S134 -> ground-based follow-up is the falsification route.
26. Pool B inverted null (300 stars, same cuts): max filtered SDE 11.6, 0/300 above 12; but the inverted null underestimates dips from asymmetric scattered-light systematics (clusters at 13.5/19 d), so it is quoted only as a lower bound on the Pool-B false-positive rate.
27. Final review fixes: vet.py per-transit timing errors were grid-floored (121 steps over 1.2 durations = 1.2 min); re-timed TIC 89247735 on a 0.24-min grid with rescaled errors (1.6-2.2 min), ephemeris P=18.323126+-0.000058 d, predictions re-frozen 21:28:13 UTC (SHA af83f110...) with pre-freeze epochs flagged as retrodictions. Depth-vs-aperture cannot separate an 8-9.5" neighbour inside the 1-px aperture; only the loss centroid does (<=0.15 px toward it vs 0.46 px expected). Pool B known-signal recovery broken down (22/54 recovered, 14 outside grid, 12 RV non-transiting, 2 second planets, 1 at 170 ppm, 2 CTOIs without depth).
28. External adversarial review (independent agent; results/external_review/REVIEW.md). Found a FOURTH transit of TIC 89247735 at epoch 118 (S93) hidden by the QUALITY==0 mask (QLP bit 2^30, orbit-start ramp); verified on raw SAP flux (10,500+-360 ppm box, no background excursion); +3.4 min from the v1 prediction. Built v2 ephemeris from four events (scripts/final_ephemeris_89247735_v2.py, raw SAP + local linear baseline): P=18.323077+-0.000070 d, predictions shift <=2 min; v1 kept frozen as test of record. Reviewer's code findings logged in REPORT.md section 9; not re-run: the quality-mask policy (keep bit 2^30 cadences, down-weight) should be adopted before any future Pool-B search. Ground observability: epochs 147-151 are behind the Sun; first full transits 2027-06-25 and 2027-08-19 (Chile); RVs can start now.
29. Single-transit search of Pool B (scripts/single_transit_search.py, single_rank.py, single_null_compare.py, single_injection.py, single_triage.py; results/single*, REPORT.md section 10). Kept QLP bit-2^30 cadences, dropped >50% flux dropouts and TESS bits 2/4/8/32/128. Lessons: (a) EBs must be removed before any field control or they poison the time bins; (b) proportional per-CCD thresholds miss sector-wide systematics - a direct +-0.1 d cross-star coincidence count vs Poisson expectation is the test that works; (c) two-event depth consistency is as common in inverted data as in real data (158 vs 160 matched stars); only >=3 events in different sectors separates TIC 89247735 from the null; (d) own summary JSONs placed in a results dir silently broke the loader glob - keep summaries in a subfolder. Injection completeness: 87-98% detection at SNR>=10, 48-76% after event cuts, 38-59% end to end (field/coincidence controls flag 27% of random times); first 0.5 d of an orbit: 40% detected, 20% end to end (5-15 injections per bin). Outcome: no new candidate.
30. All-sky scale-up (scripts/allsky_targets.py, allsky_driver.py): TIC dwarfs Tmag<=11.5, Teff<=5300, R<0.85, lumclass DWARF (~64k), tess-point sectors 1-105 (QLP on MAST ends at S105 on 2026-10-18), >=2 years required; direct-URL downloads into data/qlp_allsky (flat), results in results/search_allsky + results/single_allsky; env overrides TSEARCH_LC_DIR/TSEARCH_OUT/TSEARCH_SUFFIX added to the pipeline scripts. Quality-policy test: keeping QLP bit-2^30 cadences in the PERIODIC search (DET_FLUX) was tried and rejected - ramp residuals up to 12%, known-signal recovery 22->5 of 40, TIC 89247735 periodogram swamped by a 15-d alias; the periodic search keeps QUALITY==0 (+ >50% dropout cut, results identical to Pool B), and ramp-embedded transits are covered by the single-transit pass run on every batch.
31. Literature review flagged a QLP barycentric timing error for S99-S104 (MAST QLP page, not yet redelivered). Verified: QLP timestamps agree with a target-specific barycentric correction recomputed from FFI spacecraft times to 0.03 min (S66/S93) and <=1 min (S104). But the S104 transit TIME depends on the photometry: QLP TGLC-method 4196.8043 vs TESScut apertures 4196.8077-4196.8132 (5-13 min later); S93/S66 agree across methods to <=1.6 min. Ephemeris v3 (S104 midpoint +-6 min systematic): P=18.323172+-0.000042 d, chi2/dof 0.5/2; predictions +6.5..+8.6 min vs v2, within the +-15 min window. Also from the review: ExoFOP now accepts community candidates only after refereed publication (RNAAS acceptable only if the methodology is refereed) - CTOI submission is not available to us yet; QLP FFI product latency is ~2.7 months, but SPOC 2-min light curves appear ~3 weeks after a sector ends (S104: 23 d, S107: 18 d, file DATE headers), so the S108-S110 2-min test of TIC 317134140 runs late Oct-mid Dec 2026 as originally planned; inverted-light-curve nulls are known (Kepler DR25) to miss one-signed artefacts - use orbit-phase-preserving scrambles for the all-sky null.
32. Literature calibration applied (results/research/RESEARCH.md; REPORT.md section 11): TIC 89247735 relabelled 'transiting companion candidate (giant planet or brown dwarf)'; planet/BD prior ~1:1; Gaia RUWE/non-single-star argument withdrawn (DR3 astrometric sensitivity is at P>=10 d with a peak near 1000 d, blind to 18 d); Gaia DR3 RV diagnostics (N=14, eps 0.544 km/s, p=0.52, GoF -0.16, not variable) -> per-epoch scatter 1.6 km/s, K<~2.2 km/s, M2<~25 MJ (analyst estimate). Depth scatter across QLP sectors attributed to the S94 FIPHOT->TGLC photometry change. TIC 317134140: momentum-dump removal (+-1.5..6 h) leaves the depth unchanged (167->164+-23 ppm); TRICERATOPS installed in .venv_tri (numpy<2) and run as supporting evidence only (FPP not decisive at SNR<15). ExoFOP CTOI route requires a refereed paper (policy 2026-08-19); S108-S110 (2-min) decision expected late Oct-mid Dec 2026; v3 ephemeris script added (final_ephemeris_89247735_v3.py reproduces the frozen SHA); Gaia rv_amplitude_robust 5.7 km/s noted (consistent with noise; bound quoted as M2 <~ 25-30 MJ).

33. **Paper draft and co-author route (2026-10-18).** A refereed paper is the only door to CTOI/TOI/TFOP for TIC 89247735 (item 31). Drafted
    `paper/main.tex` (AASTeX, AJ format, single object, no planet claim; co-author placeholder; AI assistance disclosed in the acknowledgments),
    with figure and tables generated from the frozen v2/v3 JSON files by `paper/make_figure1.py`. Not compiled locally (no LaTeX), not
    committed to `public_release`, not uploaded anywhere, per the user's instruction. References limited to entries with arXiv IDs/DOIs
    fetched in the research memo plus canonical software papers marked `TODO verify`. Co-author channels and a draft e-mail in
    `paper/COAUTHOR_OUTREACH.md` (TFOP general membership, Visual Survey Group, Planet Hunters TESS, duotransit/NGTS and TESS brown-dwarf
    groups, QLP team). TRICERATOPS for TIC 317134140 finished (FPP 0.051, NFPP 0.008; informational only) and was recorded in REPORT §6.9.

34. **All-sky run reprioritised to fields TESS will re-observe (2026-10-18).** Rationale: a candidate in a field with an upcoming sector gets
    its pre-registered test from TESS itself (the Rabtsevich design), independent of any co-author. `scripts/allsky_future_sectors.py`
    (tess-point, sectors > 105) -> `catalogs/allsky_tic2sectors_future.json`: 36,103 of 57,853 targets have a sector through S134; 13,947
    have one in S109-S116 (`catalogs/allsky_priority_tics.txt`, sorted by earliest upcoming sector; 8,583 still unsearched at restart).
    Driver killed mid-batch 12 and relaunched with `--first-tics catalogs/allsky_priority_tics.txt` (resumable; per-star JSONs kept).
    Known gap: stars of the interrupted batch that have a periodic result but no single-transit result are skipped by the driver's `done`
    set; run `single_transit_search.py` on that list at the end. Note: tess-point returns a spurious sector 1751 for some stars; ignore > 134.
    Data-release deadline for freezing predictions: QLP ~2.7 months after sector end (e.g. S110 -> ~Feb 2027); 2-min ~3 weeks.

35. **All-sky priority ranking and first vetting (2026-10-18 evening).** rank.py gained TSEARCH_PARAMS (all-sky TIC table; without it dur_ratio
    was NaN for every non-Pool-B star). `scripts/allsky_testable.py` builds results/allsky_testable_soon.csv: SDE>=9 (1,238 of 36,981 stars),
    period-density flag (one hot bin), shared-time flag = excess over chance (n > max(5, 3 x expected); a plain "any sharing star" flag rejected
    606/615 because chance coincidences at 0.5 % period tolerance are ~12 per candidate), near-orbit flag, future coverage, predicted transits in
    the next sector's orbit windows, 2-min flag (S108-S110 lists; S111+ not published yet), release deadline (+80 d QLP, +21 d 2-min).
    615 candidates have a sector <= 116; 417 clean; 222 with >= 1 predicted transit in the test sector; class A (P >= 3 d, depth <= 5 ppt,
    detected every year, odd/even < 3 sigma, not a Pool-B reject, not TIC 4206066 which appears at 11.13 d = Rabtsevich's second signal) = 28,
    vetted by scripts/vet_runner.sh (vet.py, 3 parallel) -> results/vet_allsky/; one-line summaries by scripts/vet_summary_table.py.
    Rejected so far: 127132777 (rprs 0.24, b 1.15, rho 0.03x: grazing EB), 75582311 (V-shaped, rho 0.02x, SAP/DET 1.66, sector depths chi2 93: blended EB).
    TIC 30832104 (P 9.7141 d, 576 ppm, 2.2 Re, Tmag 9.7, K dwarf, next sector S110 with 3 transits, QLP release ~2027-02-14): SPOC 2-min S8+S9
    (2019) at the QLP ephemeris give 676 +- 56 ppm (12 sigma) and a blind BLS of the 2-min data alone returns 9.7053 d as its top peak
    (scripts/spoc_check_30832104.py) - independent-pipeline confirmation. No TOI/CTOI/TCE/ExoFOP entry. TIC 80387959 (4.1922 d, 757 ppm, 2.4 Re,
    rho 1.06x, blind 4/4, no secondary) also promising. Sector-scrambled null running (scripts/null_scramble.py, 300 stars, cumulative random
    per-sector time shifts 3-25 d -> results/null_scramble_allsky/). Single-transit all-sky ranking done: 1,504 duotransit pairs, inverted
    comparison not yet run. ffi_pixel_test.py now falls back to catalogs/allsky_targets.csv for coordinates.
    **Addendum (19:50 UTC): TIC 30832104 REJECTED** - ffi_pixel_test S62/S89: flux-loss centroid 2.17 / 2.02 px (45.5" / 42.3") from the target
    (+-0.06-0.10 px), same sky direction in two sectors with different orientations; the target pixel shows no loss; depth rises from ~0 at r <= 1.5 px
    to 530-590 ppm at r = 3 px. Source is a faint Gaia star ~40-46" NW (G 16.1 at 38.9" needs a 14 % eclipse; G 17.0 at 45.6" needs 33 %): a
    background EB diluted into the QLP and SPOC apertures. LESSON: a SPOC 2-min recovery of a QLP signal is NOT independent evidence against
    blending (both apertures contain the neighbour); only the pixel-level test discriminates. Run ffi_pixel_test BEFORE any 2-min cross-check or
    pre-registration. TIC 80387959 pixel test: offsets 0.17 / 0.28 / 0.22 px (+-0.10) in S63/S90/S100, depth flat-to-declining with aperture:
    on target. ffi_pixel_test writes to results/vet_qlp/<tic>/ regardless of TSEARCH_SUFFIX (copied to vet_allsky by hand).

36. **TIC 80387959 pre-registered (v1, frozen 2026-10-18 19:40:16 UTC, SHA 4652f7a3...).** TYC 8203-2056-1, K dwarf (Teff 5220 K, R 0.80, Tmag 10.5,
    116 pc, high PM). P = 4.192142 +- 0.000020 d, T0 = BTJD 4082.29250 +- 4.6 min (12 QLP transit times, chi2/dof 25.7/10, one +44-min outlier,
    conservative +-20 min quoted), depth 757 +- 41 ppm, 2.2 h, Rp ~ 2.4 Re, rho_fit/rho_TIC 1.06, odd/even 0.7 sigma, no secondary, blind 4/4,
    pixel test on target (8" G=17.3 neighbour excluded 4.8/2.8/4.3 sigma; 14" G=14.0 at 6.1/7.6/4.7 sigma), no TOI/CTOI/TCE within 60"
    (scripts/known_nearby.py, position-based). Open weakness: two-level depth (850-990 ppm 2021-23 vs ~590 ppm 2025-26, chi2 19/4; same camera,
    CCD mixed) - unexplained; quoted as x1.5 depth uncertainty. Test of record: Sector 111 (2026-11-26 to 12-22; 7 predicted transits, 3 in the
    orbit windows the orbit table covers), then S112-S114; QLP release ~mid-March 2027; check the S111 2-min list in early November.
    Tools: scripts/prereg_candidate.py (generic; restricts predictions to the star's tess-point sectors; sector spans from
    catalogs/TESS_sector_dates_future.csv (MIT Year-9 table) where the orbit table ends, flagged "span only"). NOT deposited publicly yet
    (advisor: wait for TESS-SPOC FFI depth check, the rest of class A, and the user's review). PREREGISTRATION.md wording "S110" -> "Sector 111"
    corrected by hand after the freeze; the hashed CSV is untouched.
    **Addendum: TIC 355658330 REJECTED** - pixel test S63/S89/S90: flux-loss centroid 2.24 / 2.43 / 2.07 px (43-51") from the target in all three
    sectors, target-pixel depth consistent with zero; off-target EB diluted into the aperture (also explains the 9x density mismatch). Class-A
    light-curve-only rejects: 113288623, 126526772, 127132777, 632483638 (grazing: rprs 0.24-0.30, b > 1.1, rho 0.02-0.04x), 75582311 (V-shaped blend),
    73763470 (odd/even 4.2 sigma, depth chi2 122). Parked as noise-level (SNR < 9, blind tests fail/inconclusive): 13071480, 178130889, 234059307,
    279787271, 398543433, 178155658; TIC radius missing: 12377308, 279370402. Pixel tests queued (scripts/pixel_runner.sh, bash) for the 11 that pass
    the light-curve tests: 120444365, [withheld], 140017995, 36568378, 293857021, 33480523, 71096594, 284331183, 268688836, 32077129, 235283074.
    **TIC 80387959 TESS-SPOC check (scripts/tessspoc_check.py):** independent FFI extraction (PDCSAP, S36/S37 at 600 s, S63 at 200 s) gives
    810 +- 79, 905 +- 76, 803 +- 83 ppm at the QLP ephemeris (combined 831 +- 53 ppm, 16 sigma; QLP masked-detrend depth 757 +- 41); blind BLS on
    the TESS-SPOC data alone: top period 4.19224 d, SDE 12.4. Pipeline artefact excluded; blend question rests on the pixel test (done, on target).
    TESS-SPOC has no S90/S100 products, so the 2025-26 depth drop remains untested by a second extraction.
    **Pixel-test outcomes (continued):** 140017995 REJECTED (loss centroid 1.71 / 1.43 px = 30-36" off target in S61/S88). 120444365 ON TARGET
    (0.03 / 0.19 / 0.04 px in S96/S103/S105; isolated star: nearest Gaia source able to mimic the signal is 64" away and would need 58 %);
    5.14808 d, 743 ppm, 2.45 Re, Tmag 11.06, K dwarf, seen 2018/2020/2023/2025/2026; only future coverage is S106 (observed Jul-Aug 2026, QLP
    file not on MAST as of 2026-10-18, not on any 2-min list) -> pre-registered as "sector observed, data not public at freeze"; has SPOC 2-min
    S29 and TESS-SPOC S2/S29/S69 for extraction checks. [withheld] ON TARGET by centroid (0.43 / 0.12 / 0.07 px) but a G=14.7 star 4.2" away
    needing only 1 % cannot be excluded with 21" pixels; crowded field (105 TIC entries within 60"); pre-registered v1 with that caveat
    (ephemeris test only; S111-S113).
    **Pixel-test outcomes (continued 2):** 36568378 REJECTED (1.34 / 2.04 px off in S61/S88); 293857021 REJECTED (1.53 px off in S87).
    [withheld] frozen v1 (SHA cbb409bb..., 2026-10-18 20:25:07 UTC; 16 times, chi2/dof 75/14, inflation 2.3; S111 test, 8 predicted transits).
    120444365 extraction checks: TESS-SPOC S2/S29/S69 668 / 998 / 824 ppm and SPOC 2-min S29 1002 +- 116 ppm at the QLP ephemeris (blind BLS on
    the single 2-min sector alone does not find it: SDE 3.2; red noise) -> freeze v1 launched with S106 as the test of record.
    33480523 REJECTED (loss centroid 2.97 / 1.50 px off target in S89/S90; only 2 events per sector).
    **120444365 frozen v1** (SHA 64b5b026..., 2026-10-18 20:26:00 UTC): P = 5.148082 +- 0.000037 d, T0 = BTJD 4213.82117 +- 4.6 min (epoch 555);
    6 predicted transits in Sector 106 (2026-07-12 to 08-07), status "sector observed, data not public at freeze"; QLP S106 expected late Oct 2026.
    Frozen local candidates so far (none deposited publicly): 80387959 (S111), 120444365 (S106, unreleased), [withheld] (S111; crowding caveat).
    **Pixel-test outcomes (final for class A):** 71096594 REJECTED (0.91 / 1.24 / 1.31 px off in S89/S99/S100); 284331183 REJECTED (2.80 px, S87);
    268688836 REJECTED (1.48 px, S87); 32077129 REJECTED (2.44 / 1.38 px, S61/S88); 235283074 UNRESOLVED (0.37 +- 0.1 px in the single testable
    sector S87, 3 events; SNR 12.6, rho 0.17x, blind 2/4) - parked, re-test after S111. Tally: 12 stars pixel-tested, 3 on target (80387959,
    120444365, [withheld]), 1 unresolved, 8 off-target blends at 20-60" (plus 30832104 = 9 of 12). Blends from faint EBs inside the large QLP
    apertures of bright targets are the dominant false-positive mode of this sample; the light-curve tests (shape, density, odd/even, blind
    years) do not catch them, only the pixel test does. For the all-sky ranking, run ffi_pixel_test BEFORE vet.py on every survivor.

37. **Sector-scrambled null result (300 random all-sky stars, scripts/null_scramble.py; ranked with rank.py, SUFFIX _nullscr).** After the physical
    cuts (198 stars): SDE 50/90/99th pct 7.2 / 8.1 / 11.3, max 23.3; 6.1 % >= 9, 1.0 % >= 12 (real search: 5.1 % and 1.5 %). The high-SDE null
    entries at P < 3 d are the same stars' REAL signals (e.g. TIC 374608381 P 0.750 d SDE 23.3 in both): shifting whole sectors preserves
    within-sector coherence, so for periods short relative to a sector the scramble is not a null (the Kepler DR25 caveat). Usable regime P > 7 d:
    null 8.2 % >= 9, 0 % >= 12, max 11.1 (n = 49) vs real 11.3 % and 2.9 %; the null does reproduce the 13-20 d orbit-cadence cluster (4 of its
    12 SDE >= 9 entries are at 13.5-19.9 d). Adopted: SDE >= 12 is above the null for P > 7 d; for P <= 7 d the periodogram statistic is not
    calibrated by any scramble and reliability rests on the per-event vetting and the pixel test (which is what decided every class-A outcome).
    A proper short-period null would need a within-sector shuffle (e.g. reversing or block-permuting cadences inside each sector) - not done.

38. **External review of the three all-sky candidates applied (results/external_review_allsky/REVIEW.md + LITERATURE_SURVEY.md).** Verdicts:
    80387959 SURVIVES, 120444365 SURVIVES (cleanest; TRICERATOPS NFPP 0.000, FPP 0.041), [withheld] WOUNDED (host not demonstrable; 4.2" G=14.7
    star; NFPP 0.062). Findings adopted: (1) cross-sector QLP depths are not astrophysical (per-sector normalisation, S94 dilution change) -
    the 80387959 x1.5 depth caveat is withdrawn (fixed-aperture 687 +- 36 ppm constant); (2) v1 ephemerides used 200-s sectors only (vet.py
    min_pts=15 + len<1000 cut dropped every 600/1800-s event and all of S10) -> scripts/prereg_v2.py (one time offset per sector, all sectors,
    cadence-aware batman, SPOC 2-min where present) -> v2 frozen for all three at 22:34 UTC (SHA 5d0e7651 / 32b5e085 / 0e6bd698); v1 kept on
    record; [withheld] v1 S111 predictions were 22-45 min early and would have failed a real signal; (3) QLP S99-S105 timestamp error < 1.5 min
    effect; (4) published pixel floors 7.5-15" - our 0.1-px centroid errors understate sector-to-sector scatter; exclusion of the 7.6" star
    of 80387959 is ~2.7 sigma. Code fixed: vet.py transit_model exp_time = real cadence; sector cut cadence-aware; time_transits min_pts
    cadence-aware. TODO from REVIEW 6: ffi_pixel_test.py background subtraction + PM correction + full-cutout PSF fit (adopt reviewer's
    pixel_review.py); known_nearby.py live VSX/Gaia-variability; 120444365 radius 0.76 Rsun (Rp 2.2 Re); blind test "4 of 5 years".
    Public deposit still withheld pending the user's review.

39. **Public deposit v1.3 (2026-10-18, user decision "go with these two").** GitHub release v1.3 (commit 24cd0de) of fergmolina/tess-transit-
    candidates: pre-registration v1+v2 files, pixel/extraction JSONs and figures for TIC 80387959 and TIC 120444365; external review and
    literature survey; report section 12; class-A outcome and testable-soon tables; pipeline scripts. The third object (wounded, host
    unresolved) is withheld: its TIC is replaced by "[withheld]" in every public copy (REPORT, DECISIONS, REVIEW, tables) and its review section
    body removed. Zenodo archives the release automatically under the concept DOI 10.5281/zenodo.23443245 (new version DOI to be recorded).
    Status wording everywhere: "planet candidate pending the pre-registered test"; not validated; not submitted to ExoFOP (requires a refereed paper).
    **Zenodo check (23:30 UTC):** v1.3 archived as record 23460915 (DOI 10.5281/zenodo.23460915), v1.2 = 23445705, v1.1 = 23443245; concept
    DOI 10.5281/zenodo.23443244 (the README cites the v1.1 version DOI 23443245 as "the DOI" - acceptable, but the concept DOI is the
    version-independent one; fix in the next release). GitHub webhook last response 409 (duplicate delivery), archive nevertheless complete.

41. **Parity package with Rabtsevich's record (user request, 2026-10-18 night).** His set: (1) preprint PDF on Zenodo (RNAAS-style, "No
    statistical validation is claimed"), (2) supporting data+code dataset record with README and md5 (3 zips, 18 MB), (3) separate
    pre-registration record (protocol PDF full+short, SHA256SUMS, frozen code zip, four-outcome rules computed by frozen code), (4) DDT
    program 100, (5) a documented prior-detection sweep ("30+ sources, 550+ searches, 340k+ alerts"). Ours now: (1) note_allsky/note.pdf
    (research-note manuscript on 80387959 + 120444365) and paper/main.tex (AJ draft, 89247735; needs Overleaf), (2) dataset_v1/ bundle with
    README, SHA256SUMS, MD5SUMS, frozen scripts, environments, reviews (third object withheld), (3) prereg_protocol/PREREG_PROTOCOL.pdf +
    scripts/prereg_test.py (frozen evaluator; retrodiction test on 80387959 S100 -> RECOVERED, 870 +- 104 ppm, offset -6 min), (4)
    ddt_80387959/ (user to send), (5) prior-detection sweep running (results/prior_search/). PDFs rendered with scripts/tex2pdf_lite.py
    (reportlab) because tectonic cannot download its bundle on this machine and no TeX is installed. NOTHING new uploaded until the
    prior-detection sweep is in and the user has reviewed.

42. **Prior-detection sweep, interim (2026-10-19 00:xx UTC; results/prior_search/).** (a) github.com/eumemic/exoplanets (pseudonymous,
    Claude-Code-built Rabtsevich-style search; first commit 2026-10-07) lists TIC 317134140's 0.5719-d second signal (first commit 2026-10-08
    03:14 UTC, tier A, with S109/S110 predictions), TIC 120444365 at 5.148151 d (2026-10-09 03:34 UTC, tier C, MES 9.0) and [withheld]
    at 3.282292 d (2026-10-09, tier N "neighbour < 15 arcsec"). Neither TIC 89247735 nor TIC 80387959 appears there. Our public record must
    credit these prior listings (README, REPORT 6/12, note, dataset README) -> v1.4 before any further upload. (b) TIC 80387959 has an
    UNPROMOTED TESS-SPOC FFI TCE in the Sector 63 single-sector DV run (P 4.19050 +- 0.0012 d, depth 869 +- 107 ppm, Rp 2.40 Re, MES 7.57,
    SNR 8.0; dvr.xml verified) - an automated alert, never a TOI/CTOI. Our known-signal table covered SPOC 2-min TCEs only; TESS-SPOC FFI
    TCEs must be added to catalogs/known_signals.csv for the all-sky ranking (the sweep is downloading the 51 bulk lists). Honest wording for
    80387959: "no prior candidate report; a TESS-SPOC S63 TCE at the same period exists on MAST". (c) Zenodo file contents are not indexed;
    the sweep is grepping the files of every recent independent TESS-candidate deposit (Tovar Contreras 23134068, Ozturk 23118499, 23249265, ...).
    (d) CONCURRENT (not prior) report of TIC 89247735: github.com/alejandrozarco/tess-candidates-2026, commit 5537855 at 2026-10-18 19:22 UTC
    (repo created 14:21 UTC with two other stars), same four transits, P 18.323173 +- 0.000031 d, T0 4196.80899, TRICERATOPS, Gaia limits,
    predictions to 2027-10, catalogue table; "Zenodo DOI: to be added"; does not cite our record. Our record is earlier: GitHub v1.0 2026-10-17
    23:01 UTC, Zenodo v1.1 (23443245) 2026-10-17 23:05 UTC, v1.2 2026-10-18 03:48 UTC. Priority stands on timestamps; note the concurrent
    report in the public record and consider a courteous e-mail pointing to our DOI.

43. **Prior-detection sweep final (results/prior_search/PRIOR_SEARCH.md, VERDICTS.md, query_log_all.csv): 32 services, 1,585 logged queries,
    558,074 automated alerts (341,351 SPOC TCE rows + 216,723 TESS-SPOC DV targets), 101 GitHub repos and 157 Zenodo records grepped by content.**
    Verdicts: 89247735 no prior report (concurrent Zarco report 20 h after ours); 80387959 unpromoted TESS-SPOC S63 TCE only; 120444365 listed
    earlier by eumemic (2026-10-09, tier C); 317134140 second signal listed earlier by eumemic (2026-10-08, tier A); [withheld] listed by eumemic
    (2026-10-09) and brahle (2026-10-18). Ecosystem: at least eight independent Rabtsevich-style amateur deposits in October 2026. Applied: a
    "Prior and concurrent reports" section in public README, REPORT (before section 12), dataset README, note, protocol; sweep copied to
    public_release/prior_search/ (third object's ID withheld); TESS-SPOC TCE hosts appended to catalogs/known_signals.csv (source TESSSPOC_TCE,
    period NaN). Novelty claims now read "independent rediscovery" for 120444365 and 317134140. To publish as v1.4.

44. **Three Zenodo records published 2026-10-19 (scripts/zenodo_deposit.py; result in zenodo_upload/DEPOSIT_RESULT.json):** preprint note
    10.5281/zenodo.23462434; supporting data and code 10.5281/zenodo.23462438; pre-registration protocol v1 + bundle 10.5281/zenodo.23462442.
    All CC BY 4.0, linked to the concept DOI 10.5281/zenodo.23443244 and the v1.4 release. README updated with the links. v1.4 release
    (535519a) archives automatically. Token stored by the user in ~/.zenodo_token (never echo it). DDT proposal and the two e-mails remain
    with the user (ddt_80387959/README.md, zenodo_upload/EMAIL_zarco_draft.md, paper/COAUTHOR_OUTREACH.md).
    **2026-10-19:** DDT proposal e-mailed by the user to tess-ddt@mit.edu (proposal.pdf + target_list.csv; TIC 80387959, S111-S114).
    Courtesy notice to the concurrent TIC 89247735 author filed as GitHub issue
    https://github.com/alejandrozarco/tess-candidates-2026/issues/1 (no e-mail address exists for him). The prior-detection sweep agent was
    stopped by the user with its last background job (Zenodo content grep, 32 of 157 records) unfinished; PRIOR_SEARCH.md stands as written.
    2026-10-19: TFOP general-member application e-mailed by the user to the TFOP chair.
    Note v1.1 (e-mail added) published as 10.5281/zenodo.23462857; preprint concept DOI 10.5281/zenodo.23462433.

45. **Referee review of the TIC 89247735 manuscript (results/referee_89247735/REFEREE_REPORT.md): MAJOR REVISION.** Ten major points.
    M1 is a project-wide error: every prediction file's UTC column was Time(BJD_TDB).utc without the light-travel term (geocentric arrival
    differs by up to +-8 min; e.g. 89247735 epoch 159 is 02:09 UTC, not 02:17). BJD_TDB/BTJD and all hashes unaffected; TESS tests
    unaffected; e-mailed documents (DDT, TFOP) carry dates only. Fixed: scripts/prereg_utc_fix.py produced *_utcfix.csv for all seven
    frozen files (originals untouched); prereg_candidate.py / prereg_v2.py now write geocentric UTC; public_release/preregistration/
    CORRECTION_UTC_2026-10-19.md; clock times corrected in README, REPORT, STATUS, protocol, note, manuscript. Other majors to apply in the
    manuscript: M2 (2P twin-EB not closed by the 4th transit; it is closed by flux/shape on the target and by the pixel test for the
    neighbour), M3 (depth/dilution/radius: fit on DET_FLUX vs raw depths; dilution never stated; R* error; T14 4.57 h vs "4.0"; LD coefficients),
    M4 (pixel exclusion overstated; neighbour needs 37-40 % not 23 %; calibrate centroid errors on off-transit windows; published floors),
    M5 (S104 event is 4.8 d into orbit 220, not an orbit-start ramp; flagged cadences after egress + RW-calibration windows; 6-min systematic
    ad hoc), M6 (search context: 763/3,411 SDE>12 raw, 165 pass filters, candidate rank 3; two 18.09-d look-alikes), M7 (secondary limit
    empirical scatter 298 ppm -> 2-sigma ~1,000 ppm, Teff < 2850 K), M8 (bit 31 facts: present since S56 EM2 products, 19 % in S66; MAST
    documents it as bit 13 "low precision points"), M9 (RV bound arithmetic: 2.2 km/s = 22 MJ; priors' period ranges; Gaia astrometric
    table; <1" channel quantified), M10 (4th-transit narrative: found within hours from already-downloaded data). Minor: abstract 286 words,
    UAT 2119 wrong, deluxetable* for Table 1, Figure 2 remake, TARS/Boyle bib entry, 5 wrong bib identifiers (refs_corrected.bib provided).
    Referee's own tectonic compile warmed the bundle cache: tectonic now compiles paper/main.tex locally (AASTeX, 7 pages).

46. **TIC 89247735 manuscript revised per the referee (paper/main.tex; AASTeX-compiled 9 pp via tectonic, cache warmed by the referee).**
    New computations: scripts/refit_89247735_raw.py (joint raw-SAP fit, LD 0.52/0.18: rprs 0.0977 +0.0018/-0.0012, a/R* 33.0, b 0.27 +- 0.17,
    T14 4.52 h, T23 3.66 h, rho 1.43 = TIC 1.43, model depth 11,740 ppm, Rp 8.4 +- 0.7 Re (TIC R*) / 7.9 +- 0.4 (SED R*); secondary 229 +- 127
    ppm formal, random-phase scatter 331 ppm, p = 0.14 -> 2-sigma ~900 ppm, Teff < ~2800 K); scripts/pixel_calib_89247735.py (injection of
    the real depth into 60 off-transit windows: per-window centroid scatter 0.16/0.17/0.19 px; relative formulation; chi2 target 4.0 vs
    neighbour 9.7 for 6 dof -> neighbour disfavoured at ~2.4 sigma by pixels alone; pure-noise windows give 0.5-0.7 px and are the wrong
    calibration); fig2_pixel_89247735.py (1x3 significance maps). Text: abstract <= 250 words, UAT fixed, deluxetable*, M2 twin-EB logic,
    M5 S104 description + RW windows + uniform-inflation alternative fit, M6 search context, M8 bit-31 facts, M9 RV-bound arithmetic + Gaia
    astrometric diagnostics + <1" channel, M10 narrative, TARS/QLP HLSP citations, refs_corrected.bib adopted. Required-neighbour eclipse
    37-40 %. Second referee pass launched (results/referee_89247735/REFEREE_REPORT_round2.md). Preprint NOT deposited; rev1 PDF staged.
    **Round-2 referee (REFEREE_REPORT_round2.md): MINOR REVISION, 14 required edits, all applied:** uniform-inflation fit = v2 (18.323077
    +- 0.000070, 1.2 sigma, 8 min at epoch 159); neighbour separation 7.1-7.5" at TESS epochs (8.0" at 2016.0), not 8-9.5"; centroid rms
    described as rms about the WCS target (random part 0.09-0.11 px); peak-pixel S/N 11-21; "consistent with the target"; dilution arithmetic
    (host >= 56 % of light; diluting companion >~ 1.2 mag fainter); like-for-like k comparison with Zarco (0.0977 vs 0.1075; 7.9 vs 8.7 Re on
    the SED radius; difference unexplained); Zarco cited (zarco2026, Zenodo 10.5281/zenodo.23453967); sweep stats to a footnote; Sec 6 UTC
    statement + single concept DOI; stale 0.76 RJup / 16 S / 540-560 K / 4-h fixed; per-window secondary values (+51, +320, +236 ppm);
    refs (kunimoto2025 AJ 170, 280; boyle2026 authors; claret2017; gaiadr3docs; kunimoto2022faint for TOI promotion); Figure 1 replotted
    with the raw-flux fit (legends on all panels); acknowledgments environment -> \section* (AASTeX line-number glitch). Compiled: 9 pp.
    Staged as zenodo_upload/Molina2026_TIC89247735_preprint_rev2.pdf; NOT deposited pending the user's reading.

47. **All-sky run complete (2026-10-19 ~10:40 UTC): 57,835 of 57,853 stars searched (periodic + single-transit passes).** Re-ranked with the
    TESS-SPOC-inclusive known list: known-host recovery 384/764 (50 %); 36,388 pass physical cuts; 1,737 at SDE >= 9. Testable-soon
    (S <= 116): 656, 446 clean, 253 with a predicted transit in the test sector. Round-2 class A (SDE >= 9, P >= 3 d, depth <= 5 ppt, every year,
    odd/even < 3, not near-orbit, no known source, not previously vetted): 94 near-term + 39 later (S117-134) + 36 with no future sector = 169,
    of which 18 already listed by eumemic (queued last). Pixel test FIRST via scripts/pixel_runner2.sh (two parallel queues, 3 latest 200-s
    sectors each); scripts/pixel_collect.py classifies ON/OFF/AMBIGUOUS; vet.py only for ON_TARGET. Scheduled cron for the continuation deleted
    (work started directly on the driver's completion notice).

48. **All-sky round 2 (2026-10-19 11:00-11:50 UTC): 169 new class-A -> pixel test first: 95 off-target blends, 20 ambiguous (0.5-0.9 px), 26
    unique on-target (7 no data). Full vetting of the 26 (results/allsky_classA_round2_outcomes.csv).** New CANDIDATES: TIC 183374279 (11.738 d,
    ~970 ppm, 2.5 Re, isolated K dwarf, blind 4/4, rho 1.45x, SPOC 2-min S29 1380 +- 235 ppm; nothing in the sweep corpus; v2 frozen 11:44 UTC,
    SHA 069d8298, test S106 unreleased - same timing as 120444365) and TIC 61310956 (16.538 d, ~1,140 ppm, 2.7 Re, isolated, SPOC 2-min S22+S45
    1068 +- 95 ppm = 11 sigma; no TESS coverage through S134, ground-based only; not frozen). TIC 258006047 (10.022 d, 920 ppm, 2.3 Re) passes
    everything but (a) a G=15.95 star 2.6" away (needs 7 %) is unresolvable and (b) scripts/prior_grep.py found it listed on 2026-10-08 in
    B. Murray's Zenodo 23230562 bundle ("2.1 Re on a 10.0-d orbit") -> REDISCOVERY; v2 frozen (SHA 48805ca7) as an ephemeris-only S114 test,
    note added to its PREREGISTRATION_v2.md. Eight further on-target stars are eumemic/ahrazzle rediscoveries (parked), four rejected on
    density (rho 10-30x), four on odd/even, the rest weak (SNR < 9) or marginal. Lesson: run prior_grep.py on every survivor BEFORE freezing
    (258006047 was frozen 40 min before its prior listing was found). Nothing published.

49. **v1.6 deposited (user: "Go with 279").** GitHub release v1.6 (1ba1f67): TIC 183374279 pre-registration (v2 CSV with geocentric UTC,
    ephemeris JSON, pixel and 2-min checks, vetting report, figures), README dossier, REPORT section 12.5, round-2 outcome table and
    testable table with the two withheld IDs masked ([withheld] = crowded 3.28-d object; [withheld-2] = the isolated 16.5-d candidate without
    TESS coverage, not deposited at the user's choice). Pre-registration protocol v1.2 (five objects) published as a new Zenodo version.
    TRICERATOPS (scripts/triceratops_qlp.py, 2.5-px aperture, QLP DET_FLUX fold, no contrast curve): TIC 183374279 FPP 0.031, NFPP 0.000
    ("likely planet" by the Giacalone+2021 categories, not validated). TIC 61310956 ephemeris with the SPOC 2-min S22/S45 transit times:
    P = 16.537975 +- 0.000111 d, T0 = BTJD 3262.56581 +- 10.3 min (6 sector times, chi2/dof 8.8/4) - ground-based predictions sigma ~20-25
    min in 2027 (QLP-only was ~45 min). Full prior-detection sweep for both running (results/prior_search_round2/).
    TRICERATOPS TIC 61310956 (sectors 72, 45, 22; S46 has no TESScut product): FPP 0.020, NFPP 0.000 - the lowest FPP of any object in the
    project, just above the 0.015 validation threshold and without a contrast curve; "likely planet" category.

50. **Round-2 freezes (user: "do everyone", 2026-10-19 12:45-12:52 UTC).** v2 predictions frozen locally for all 19 round-2 on-target objects
    that are not rejected on density or odd/even: 183374279 (11:44), 258006047 (11:44), 61310956 (12:45, --ground, 2-min times included),
    333735955, 203381983, 366047768, 3367979, 383617106 (12:46-12:47), 70441745, 467959906, 249813122, 376225363, 50514263, 245503256,
    36694943, 332709057, 65575657, 371421714, 91617711 (12:51). prereg_v2.py extended: --ground mode; 1-2 sector times -> period held at the
    BLS value with sigma_P = (T14/4)/baseline cycles; future sectors without published dates -> every transit listed as "undated". Seven
    objects rejected by light-curve vetting (261562226, 135425484, 92134828: rho 10-30x; 185296189, 428079143, 164661702, 124609967:
    odd/even) were NOT frozen. known_nearby: 26/26 clean. Full prior-detection sweep of all 26 running (results/prior_search_round2/).
    Public deposit of the set awaits the user's confirmation of the tiered list (candidate / credited rediscovery / marginal / weak).

51. **Round-2 referee review (results/referee_round2/REFEREE_REPORT.md, 2026-10-19 ~13:30 UTC): both objects "revise, keep as candidate".**
    Findings accepted: (a) 61310956 "independent SPOC 2-min detection, 11 sigma" was wrong - the 2-min data do not detect the period blind
    (SDE 2.9 at P); the depth at the QLP ephemeris is 1068 +- 240 ppm empirical (4.5 sigma); the v2 ephemeris double-counted S22 and S45 (QLP
    + SPOC rows) -> prereg_v2.py now keeps one time per sector (SPOC replaces QLP) and takes --version; v3 frozen for 61310956 with ground-based
    outcome rules (+-3 sigma_min, no 30-min cap, reference depth/T14 stated). (b) 61310956 was NOT "never public": its period and depth sat in
    tables/allsky_testable_soon.csv at v1.3-v1.5 (2026-10-18 23:24 to 10-19 12:16 UTC); public text must say so. (c) 183374279: quote the depth
    range 1.0-1.4 ppt and radius 2.3-2.9 Re (TIC v8.2 R 0.708), blind holdout "4 of 4 testable years" (2018 untestable), pixel offsets with
    calibrated errors (0.16-0.22 px), third S106 transit is half covered (orbit 224 ends 09:10 UTC) -> addendum appended to its
    PREREGISTRATION_v2.md (hashed CSV untouched), "data not public" verified for QLP only. (d) TRICERATOPS wording: give the 0.015 threshold,
    drop "likely planet". Public README (v1.6) carries the old 183374279 wording -> corrected in v1.7. DOSSIERS.md and the outcome table updated.
    v3 frozen 2026-10-19 14:09:02 UTC (SHA 76e89296): 4 sector times (SPOC S22/S45, QLP S46/S72), P 16.537966 +- 0.000150 d, chi2/dof 7.2/2, sigma 27.7 min at epoch 147 (reproduces the referee's refit). prereg_v2.py now reads cached SPOC files before querying MAST.

52. **v1.7 deposited (user: "all tiers", 2026-10-19 ~15:10 UTC).** GitHub release v1.7 (b944812): TIC 61310956 dossier and v3 predictions,
    corrected TIC 183374279 text, 18 round-2 frozen objects in four labelled tiers, referee_round2/, prior_search_round2/ (sweep agent hit
    a usage limit at 14:54; GitHub counts filled by the lead from the logs, completion note in LIMITATIONS_round2.md). Protocol v1.3 on
    Zenodo 10.5281/zenodo.23477866. [withheld] stays withheld.

53. 2026-10-19 ~19:30 UTC — Round-3 external review (Codex) of the TIC 89247735 manuscript: major revision. Two factual errors confirmed:
    (a) QLP S104 timestamps are early by 8.02 min (the MAST S99–S104 barycentric issue; our earlier "≤1 min" check was wrong), and
    (b) the contact columns in *_utcfix.csv were not light-time corrected. Fixes: v4 ephemeris (P 18.323176 ± 0.000040 d, frozen
    19:19:21 UTC, SHA 4f6aba63…); *_utcfix2.csv; shape refit plus LD/baseline sensitivity runs; manuscript rewritten (centroid significance,
    neighbour-EB exclusion and Gaia mass limit withdrawn). v1 stays the test of record (v4 is +4.4 to +5.6 min, about 1.3σ). Nothing published;
    the utcfix2 files and the v4 freeze still need to go to the public repository on the user's go. Response: results/referee_89247735/RESPONSE_round3_external.md.
54. 2026-10-19 ~20:00 UTC — QLP clock check of all frozen ephemerides using QLP S99+ (scripts/qlp_clock_check.py; results/qlp_clock_check/).
    S105 is ALSO affected (QLP times lack the barycentric correction; not in MAST's S99–104 notice). Corrected predictions shift by
    −0.04 to +3.9 min (≤1.1σ); no outcome rule changes; dated addendum only. RULE: clock-check any S99+ QLP test data (including S106)
    against TESScut before running prereg_test.py.
