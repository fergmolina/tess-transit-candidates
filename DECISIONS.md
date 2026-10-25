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
    the light-curve tests: 120444365, 120517801, 140017995, 36568378, 293857021, 33480523, 71096594, 284331183, 268688836, 32077129, 235283074.
    **TIC 80387959 TESS-SPOC check (scripts/tessspoc_check.py):** independent FFI extraction (PDCSAP, S36/S37 at 600 s, S63 at 200 s) gives
    810 +- 79, 905 +- 76, 803 +- 83 ppm at the QLP ephemeris (combined 831 +- 53 ppm, 16 sigma; QLP masked-detrend depth 757 +- 41); blind BLS on
    the TESS-SPOC data alone: top period 4.19224 d, SDE 12.4. Pipeline artefact excluded; blend question rests on the pixel test (done, on target).
    TESS-SPOC has no S90/S100 products, so the 2025-26 depth drop remains untested by a second extraction.
    **Pixel-test outcomes (continued):** 140017995 REJECTED (loss centroid 1.71 / 1.43 px = 30-36" off target in S61/S88). 120444365 ON TARGET
    (0.03 / 0.19 / 0.04 px in S96/S103/S105; isolated star: nearest Gaia source able to mimic the signal is 64" away and would need 58 %);
    5.14808 d, 743 ppm, 2.45 Re, Tmag 11.06, K dwarf, seen 2018/2020/2023/2025/2026; only future coverage is S106 (observed Jul-Aug 2026, QLP
    file not on MAST as of 2026-10-18, not on any 2-min list) -> pre-registered as "sector observed, data not public at freeze"; has SPOC 2-min
    S29 and TESS-SPOC S2/S29/S69 for extraction checks. 120517801 ON TARGET by centroid (0.43 / 0.12 / 0.07 px) but a G=14.7 star 4.2" away
    needing only 1 % cannot be excluded with 21" pixels; crowded field (105 TIC entries within 60"); pre-registered v1 with that caveat
    (ephemeris test only; S111-S113).
    **Pixel-test outcomes (continued 2):** 36568378 REJECTED (1.34 / 2.04 px off in S61/S88); 293857021 REJECTED (1.53 px off in S87).
    120517801 frozen v1 (SHA cbb409bb..., 2026-10-18 20:25:07 UTC; 16 times, chi2/dof 75/14, inflation 2.3; S111 test, 8 predicted transits).
    120444365 extraction checks: TESS-SPOC S2/S29/S69 668 / 998 / 824 ppm and SPOC 2-min S29 1002 +- 116 ppm at the QLP ephemeris (blind BLS on
    the single 2-min sector alone does not find it: SDE 3.2; red noise) -> freeze v1 launched with S106 as the test of record.
    33480523 REJECTED (loss centroid 2.97 / 1.50 px off target in S89/S90; only 2 events per sector).
    **120444365 frozen v1** (SHA 64b5b026..., 2026-10-18 20:26:00 UTC): P = 5.148082 +- 0.000037 d, T0 = BTJD 4213.82117 +- 4.6 min (epoch 555);
    6 predicted transits in Sector 106 (2026-07-12 to 08-07), status "sector observed, data not public at freeze"; QLP S106 expected late Oct 2026.
    Frozen local candidates so far (none deposited publicly): 80387959 (S111), 120444365 (S106, unreleased), 120517801 (S111; crowding caveat).
    **Pixel-test outcomes (final for class A):** 71096594 REJECTED (0.91 / 1.24 / 1.31 px off in S89/S99/S100); 284331183 REJECTED (2.80 px, S87);
    268688836 REJECTED (1.48 px, S87); 32077129 REJECTED (2.44 / 1.38 px, S61/S88); 235283074 UNRESOLVED (0.37 +- 0.1 px in the single testable
    sector S87, 3 events; SNR 12.6, rho 0.17x, blind 2/4) - parked, re-test after S111. Tally: 12 stars pixel-tested, 3 on target (80387959,
    120444365, 120517801), 1 unresolved, 8 off-target blends at 20-60" (plus 30832104 = 9 of 12). Blends from faint EBs inside the large QLP
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
    80387959 SURVIVES, 120444365 SURVIVES (cleanest; TRICERATOPS NFPP 0.000, FPP 0.041), 120517801 WOUNDED (host not demonstrable; 4.2" G=14.7
    star; NFPP 0.062). Findings adopted: (1) cross-sector QLP depths are not astrophysical (per-sector normalisation, S94 dilution change) -
    the 80387959 x1.5 depth caveat is withdrawn (fixed-aperture 687 +- 36 ppm constant); (2) v1 ephemerides used 200-s sectors only (vet.py
    min_pts=15 + len<1000 cut dropped every 600/1800-s event and all of S10) -> scripts/prereg_v2.py (one time offset per sector, all sectors,
    cadence-aware batman, SPOC 2-min where present) -> v2 frozen for all three at 22:34 UTC (SHA 5d0e7651 / 32b5e085 / 0e6bd698); v1 kept on
    record; 120517801 v1 S111 predictions were 22-45 min early and would have failed a real signal; (3) QLP S99-S105 timestamp error < 1.5 min
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
    03:14 UTC, tier A, with S109/S110 predictions), TIC 120444365 at 5.148151 d (2026-10-09 03:34 UTC, tier C, MES 9.0) and TIC 120517801
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
    earlier by eumemic (2026-10-09, tier C); 317134140 second signal listed earlier by eumemic (2026-10-08, tier A); 120517801 listed by eumemic
    (2026-10-09) and brahle (2026-10-18). Ecosystem: at least eight independent Rabtsevich-style amateur deposits in October 2026. Applied: a
    "Prior and concurrent reports" section in public README, REPORT (before section 12), dataset README, note, protocol; sweep copied to
    public_release/prior_search/ (third object's ID withheld); TESS-SPOC TCE hosts appended to catalogs/known_signals.csv (source TESSSPOC_TCE,
    period NaN). Novelty claims now read "independent rediscovery" for 120444365 and 317134140. To publish as v1.4.

44. **Three Zenodo records published 2026-10-19 (scripts/zenodo_deposit.py; result in zenodo_upload/DEPOSIT_RESULT.json):** preprint note
    10.5281/zenodo.23462434; supporting data and code 10.5281/zenodo.23462438; pre-registration protocol v1 + bundle 10.5281/zenodo.23462442.
    All CC BY 4.0, linked to the concept DOI 10.5281/zenodo.23443244 and the v1.4 release. README updated with the links. v1.4 release
    (535519a) archives automatically. Token stored by the user in ~/.zenodo_token (never echo it). DDT proposal and the two e-mails remain
    with the user (ddt_80387959/README.md, zenodo_upload/EMAIL_zarco_draft.md, paper/COAUTHOR_OUTREACH.md).
    **2026-10-19:** DDT proposal e-mailed by the user to the TESS DDT office (proposal.pdf + target_list.csv; TIC 80387959, S111-S114).
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
    Zenodo 10.5281/zenodo.23477866. TIC 120517801 stays withheld.

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
55. 2026-10-19 — v1.8 published (user: "1 go"). Corrections only: GitHub c4e5594, release v1.8, Zenodo 10.5281/zenodo.23482865. The revised
    TIC 89247735 manuscript is held for a fresh review round.
56. 2026-10-19 ~20:30 UTC — Round-4 external review (Codex): major revision, all repairable. Confirmed: TESScut TIMECORR is an
    FFI-reference correction, not target-specific, so v1.8's +8.02 min was mis-derived. New method qlp_clock_v2.py (JPL Horizons TESS
    vectors): S104 correction +7.533 min; v5 ephemeris P 18.323174 ± 0.000040 d (frozen 19:57:20 UTC, SHA 216e7a4c…); revised addendum b for
    all 8 objects (shifts ≤1.2σ). Manuscript fixes applied (neighbour depth 28–31 %, flag counts, SIMBAD, etc.). Pending: v1.9 public
    correction (user approval) and a format decision (RNAAS vs AJ).
57. 2026-10-19 — Round-5 external review: minor revision; v1.9 held for 4 release-summary errors (≤1.2σ excluded 89247735; S102 grouping
    and cause; overstated round-4 response; no manifest). All fixed; qlp_clock_v2.py hardened (spacecraft-time LTT, unique controls,
    S74–79 excluded, cadence check; corrections change <0.01 s). v1.9 published on the user's prior go, conditional on this review.
    v1.9 published: GitHub d995a1f, Zenodo 10.5281/zenodo.23483639.
58. 2026-10-19 — RNAAS note drafted (paper/rnaas/note.tex, aastex701, ~1,340 words, 131-word abstract, Figure 1). Not submitted; the user submits via aas.msubmit.net after review.
59. 2026-10-19 — RNAAS note revised per external review (paper/rnaas/REVIEW_note_external.md): all 17 findings applied; new 2x2+fold figure (paper/rnaas/make_fig_rnaas.py); refs: Zarco v1.1 title/DOI, MAST notice, Horizons, Lightkurve, Kovacs, Boyle; doubled-comma fix (misc howpublished->publisher in rnaas/refs.bib). Not submitted.
60. 2026-10-19 — RNAAS note re-check (Codex): submit after minor fixes; applied (TARS -> ApJS 284, 75; caption; 200-s exposure in drawn curves; stray brace; corporate-author citation spacing; NASA SMD credit). Ready for the user to submit.
61. 2026-10-19 — Internal final review of RNAAS note: submit after minor polish, no must-fix. Applied: TARS initials (now 'Boyle et al. 2026a,b'), qlphlsp per DataCite (Huang, C. X.; official title; STScI/MAST), k and BTJD defined, 'The Astropy Collaboration', legend 'joint-fit shape'. Draft header left (AAS builds its own). Ready to submit.
62. 2026-10-19 ~18:10 EDT — RNAAS note on TIC 89247735 SUBMITTED by the user via aas.msubmit.net (manuscript AAS82560 (internal ms_id 159131); corridor: Solar System, Exoplanets, and Astrobiology; files note.tex, refs.bib, fig1_rnaas.pdf, author PDF). Awaiting editor decision (RNAAS typically publishes within ~72 h).
63. 2026-10-19 — Round 3 (user: "go with 1"): previously unvetted testable-soon signals. From allsky_testable_soon.csv (1,737 at SDE>=9) minus
    the 197 class-A vetted in rounds 1-2: clean, no known source, odd/even and secondary <3 sigma, >=1 predicted transit in the next sector
    -> 190 (results/allsky_round3.csv; excluded from class A for P<3 d [119], not seen every year [~137], depth >5 ppt [9]).
    Next sectors: S106 60, S107 17, S108 25, S109 22, S110 22, S111 44. URGENT: S106 predictions must be frozen before QLP S106 release
    (late Oct). Pixel test first (pixel_runner2.sh, two queues, launched ~22:20 UTC). Several stars at P = 18.42 d -> likely systematic.
64. 2026-10-20 ~00:45 UTC — Round 3 results. 190 -> pixel ON_TARGET 84 (TIC 4206066 = Rabtsevich's 11.13-d signal, excluded/credited) -> vet.py 83
    -> triage (scripts/triage_round3.py) 7 PASS / 8 WEAK / 68 FAIL. Prior-report grep: 115692561, 19119739 (eumemic), 333661705 (brahle),
    408110117 (Zenodo 23289478), 88407114 (killercatfish/tess-hunt). prereg_v2.py gained --clock (method-2 QLP S99+ corrections applied before
    the fit; CLOCK_NOTE in the frozen text); qlp_clock_v2.py gained a +0.033-min fallback convention when no clean control sector exists.
    15 v2 freezes made locally 2026-10-20 00:33-00:44 UTC (S106: 122522485, 206620592, 253931796, 115692561, 88407114). TRICERATOPS on the 6
    unlisted passes. Outcomes: results/allsky_round3_outcomes.csv. Issue: 253931796 sigma 45 min > the frozen 30-min cap. Nothing published.
65. 2026-10-20 — Found: the per-object TESS rule text ('within +-3 sigma (and in any case within +-30 min)', 40 files) contradicts the public protocol and the frozen evaluator (max(3 sigma, 30 min)). Protocol governs; dated clarification results/CLARIFICATION_TIMING_RULE_2026-10-20.md; template fixed. No v3 for 253931796 needed (tolerance 135 min under the protocol).
66. 2026-10-20 — Dated timing-rule addendum appended (not rewritten) to every PREREGISTRATION*.md containing the misstated phrase (40 files). Public copies follow in v2.0.
67. 2026-10-20 ~01:30 UTC — Two external/internal reviews in. (a) S106 test-procedure review (Codex): evaluator NOT READY (mean-offset
    cancellation, no duration check, brightening accepted, coverage-based false EXCLUDED, check order, undefined AMBIGUOUS, flux-column choice,
    no S106 clock gate, 120444365 reference depth/duration not locked). Its claim that prereg_test.py was never public is FALSE (in Zenodo
    protocol records 23462442/23474138/23477866 bundles). Its min(3σ,30) reading conflicts with the protocol's max(); pending timing-rule review.
    (b) Round-3 candidate review: no prior reports for 206620592, 122522485, 283913390, 196514928 (TOI/CTOI/TCE/GitHub/Zenodo); verdicts
    206620592 candidate, 122522485 marginal/candidate, 283913390 weak (5/5 years was a New-Year double count), 196514928 marginal (centroid,
    aperture-depth, RUWE 2.09, G17 star at 2"). Per-sector timing errors 2-10x too small.
    CRITICAL: S106 data were PUBLIC before every S106 freeze: SPOC 2-min S106 files downloaded 2026-10-17 12:45 local for other stars; FFIs on
    TESScut. Freezes of 120444365 (10-18), 183374279 (10-19), round 3 (10-20) all say "data not public at freeze" - false; correct wording is
    "public but not examined by us". Public files affected: README, TIC120444365 v1/v2, TIC183374279 v2, TIC70441745 v2. TIC 88407114 frozen
    fit INCLUDES S106 SPOC data (prereg_v2 fetches all 2-min sectors) -> its S106 test is invalid. No other frozen fit contains S106+ data.
68. 2026-10-20 — Timing-rule review (Codex, results/REVIEW_timing_rule.md): handled with fixes needed. Applied locally: clarification
    rewritten (true chronology: 80387959/120444365 v2 predate the protocol; impact differs whenever sigma != 10 min; scope = 37 v2 TESS files;
    evaluator limitations stated); dated corrections appended to the 3 v1 files (60-min rules) that wrongly received the addendum; generator
    template wording fixed; generator horizon bug fixed (range(1,400) left 162304222, 408110117, 53825235 with no future predictions -> need v3);
    status label no longer claims "data not public"; SPOC 2-min test sectors (unreleased list, future sectors, >=106) are never fitted.
    Draft erratum results/ERRATUM_S106_DATA_AVAILABILITY_2026-10-20.md awaiting review + user go.
69. 2026-10-20 — Erratum/clarification review (Codex, results/REVIEW_erratum_and_clarification.md): both "publish after listed fixes".
    Corrections to earlier entries (not rewriting them): item 66's "40 files" = 37 correctly affected v2 originals + 3 v1 files corrected
    later; item 67's "No other frozen fit contains S106+ data" should read "only TIC 88407114 overlaps its declared test sectors; TIC
    317134140 intentionally uses S107 training data (its tests are S108-S110)". S106 FFIs were public by mid-August 2026 (MAST S106 FFI
    script Last-Modified 2026-08-13; TICA notice 2026-08-14); S107 SPOC/FFI also public before the Oct-20 S107 freezes. Applied: erratum
    rewritten (product-specific availability, all 11 affected records incl. S107, attestation wording, 206620592 cutout disclosure,
    88407114 withdrawal, process-fix status); manifest results/ERRATUM_S106_MANIFEST.csv; dated availability notes on 11 current
    registrations + withdrawal on 88407114 v2; clarification scope/aggregation fixed; prereg_v2.py: pre-read/pre-download holdout guard
    for QLP and SPOC (dry-run verified), endpoint through 2027-12-31, explicit --reason for v>2, honest status label.
70. 2026-10-20 — v1.10 published (user: 'Do 1'): GitHub 87a9c15, release v1.10, Zenodo v1.10 10.5281/zenodo.23487718. Erratum + manifest, clarification, round-3 freezes (15 objects; 162304222 v3), dated notes, reviews. Pending (separate go): new Zenodo versions of the protocol and the two-candidate preprint; evaluator conformance procedure.
71. 2026-10-20 — Conformance evaluator v2 (user: "Go evaluator v2"). scripts/prereg_conformance.py (joint common-offset/duration box fit
    over fully covered events; dips only; per-event depth consistency; red-noise beta; duration via delta-chi2 <= 4; timing gate
    max(3σ,30) plus min() reading; precedence INSUFFICIENT > RECOVERED > INCONSISTENT > EXCLUDED > AMBIGUOUS; clock gate refuses QLP >= 99
    without a record). Design iterated on evidence: per-event-only matching failed real injections (1/3) -> joint fit; gate-confined
    search let a 20-min-late transit pass the 6.3-min gate -> local search + point-estimate timing; partial-overlap false INCONSISTENT ->
    global best. Final: synthetic 15/15; real in-sample transits 3/3 RECOVERED, nulls 0/3, injections 3/3. Calibration (60 nulls + 60
    injections) running. qlp_clock_test_sector.py (CADENCENO anchor). Locked configs configs/conformance/*_S106.json; dated amendments:
    reference values for 120444365 (855 ppm, 2.0 h) and 70441745 (1829 ppm, 1.5 h); 183374279 TESScut fallback withdrawn (test deferred
    if QLP S106 not out by 11-15). Observed: 120444365 in-sample transits +10..+18 min from v2 (sigma 2.1) - min() reading would fail.
72. 2026-10-20 — Calibration 1 (seed 2026; 3 in-sample LCs x 20 null + 20 injection phases): of runs with >=2 eligible events,
    injections RECOVERED 44/49 (90%), nulls RECOVERED 1/49 (2%), nulls INCONSISTENT 6/49 (12%), nulls EXCLUDED 11/49; 22 INSUFFICIENT
    (183374279 S105 has 2-3 transits). False INCONSISTENT came from (a) per-event "displaced" noise peaks at unrelated offsets and (b)
    look-elsewhere in the +-0.3 d joint search (SNR 5.1-5.7). Changed (before any test data): per-event displaced route removed
    (information only); INCONSISTENT requires joint SNR >= 7. Synthetic opposite50 expectation INCONSISTENT -> AMBIGUOUS (declared in
    test file). RECOVERED threshold kept at the protocol's SNR >= 5 (2% false rate disclosed, not tuned). Independent re-check with fresh
    phases (seed 7777) launched. Review prompt: results/PROMPT_conformance_review.txt.
73. 2026-10-20 — Independent re-check (seed 7777): injections RECOVERED 46/51 (90%); nulls RECOVERED 1/51 (2%), INCONSISTENT 0/51, EXCLUDED 9/51; min() reading recovers 31/51 injections. Procedure document completed with hashes and rates; awaiting external review before publication.
74. 2026-10-20 — Internal adversarial review of evaluator v2.0 (workflow, 112 agents; results/REVIEW_conformance_internal_findings.json
    is the complete record: 52 upheld blocker/major findings, none refuted; the synthesis file *_TRUNCATED.md saw only part of its input).
    DECISION: conformance-v2.0 (prereg_conformance.py SHA 0520ea58...) is WITHDRAWN as the declared procedure before publication; it was
    never published. Pure bugs being fixed now (v2.1): clock tool equal-length branch could never pass (TESScut CADENCENO is always 0);
    unequal-length branch measured a globbed file, not --qlp; clock record not validated; --allow-no-clock untraced; CSV path skips
    checks; product (ORIGIN) not enforced; no clock prior for 70441745; validation injected in raw (uncorrected) time.
    Design questions put to the user (not decided): post-gap ramp/edge policy (locked S106 epochs fall in ramp zones; 6/8 calibration
    false nulls edge-adjacent); EXCLUDED definition (displaced real transit can read EXCLUDED); operating-SNR validation (suite ran at
    ~10x real SNR; opposite +-50 min and 0.6x/1.5x durations are RECOVERED in 5-50% of realisations at real noise); out-of-sample,
    per-config calibration; declare 115692561/122522485 low-power in advance; governance statement + protocol erratum (tex:35 gives
    v1 sigma 4.7 min for 120444365; the hashed v2 CSV gives 2.1). CORRECTION to item 71: "120444365 in-sample transits +10..+18 min from
    v2" is estimator scatter (injection rms 8-12 min), not ephemeris error; the registration's S96 O-C is +0.2 +- 1.8 min.
    Holdout check after the review: no S106+ file for any test TIC was created (all agent FITS are S105 in-sample derivatives).
75. 2026-10-20 — Pure-bug fixes applied (conformance-v2.1-dev; not published; v2.0 copies kept in results/qlp_clock_v2/*_v2.0*.py):
    - qlp_clock_test_sector.py v2.1 (SHA 2e6595b0...): integer cadence alignment (TESScut spacecraft-time grid vs QLP CADENCENO; best shift
      must beat all others by >= 2 matched cadences; TIME steps must agree with CADENCENO steps; offset must not jump; >= 80% matched);
      reads only --qlp (no glob); camera/CCD-matched cutout; records config/pred/QLP/TESScut/prior hashes and an offset-state label;
      refuses sectors >= 106 without --declared-test. Reproduces all 21 published clock corrections (S99-S105) to < 1e-8 min;
      misregistered-gap file now correct (v2.0 biased +1.3/+2.6 min); no-gap and one-gap files refused.
    - results/qlp_clock_v2/70441745.json: c0 +0.0328 min from control sectors S96, S68 (run with a <= 98 guard).
    - prereg_conformance.py (SHA 9bffdd2f...): clock record must match TIC, sector, light-curve SHA-256, prediction-CSV SHA-256 and the
      event list, with finite corrections (else CLOCK_UNVERIFIED); --allow-no-clock removed; CSV only for product 'synthetic'; product
      QLP enforced (HLSP file name, ORIGIN MIT/QLP, TIMESYS TDB, BJDREFI 2457000, TICID present); header provenance, script SHA and
      software versions recorded; no-prediction sector -> INVALID_INPUT; sector rule = leading integer; median-baseline error uses
      pi/2; stale comment fixed. test_conformance.py 15/15 still pass (high-SNR suite; design caveat stands);
      new test_conformance_inputs.py 18/18 (in-sample S105 only).
    - validate_conformance_real.py v2.1: production path (FITS copies + clock tool), locked depth/T14/sigma per test, injections at
      tc - corr(tc), time-since-segment-start recorded. CONFORMANCE_PROCEDURE draft marked superseded (not for publication).
    Addendum to 75 (same day): clock record gains a "warning" when the median QLP - spacecraft offset is >= 0.5 cadence and within 10 s
    of a whole number of cadences (label error vs row misregistration indistinguishable; inspect before reporting); evaluator copies it.
    Current SHAs: prereg_conformance.py fb0cba17..., qlp_clock_test_sector.py c016ad7a...; test_conformance_inputs.py 18/18 re-run.
76. 2026-10-20 — User accepted design decisions 1-6 as recommended ("Go"). SECTOR PARTITION, declared before any further run (200-s
    sectors only; 30-min S1-26 and 10-min S27-55 QLP are a different noise regime and are not used for design or calibration):
    - DESIGN (used for the edge rule, the discriminating test and the operating-SNR suite; S96/S105 were already used in v2.0 work):
      183374279 S96 S105 | 120444365 S96 S105 | 70441745 S96 | 206620592 S96 | 122522485 S97 | 253931796 S96 | 115692561 S96.
    - HOLDOUT (calibration only, not looked at for design): 183374279 S69 S103 | 120444365 S69 S103 | 70441745 S68 | 206620592 S68 |
      122522485 S105 | 253931796 S68 | 115692561 S69. 70441745/206620592/253931796/115692561 have no holdout sector >= 99 (calibration
      runs without the clock-tool path there; stated, not simulated). S68 was used only to measure 70441745's clock constant c0.
    EDGE RULE (decision 1), derived on DESIGN sectors (scripts/conformance_edge_profile.py; results/conformance_v21/edge_profile_*):
    evaluator box depth at reference T14 on a 0.02-d grid away from known transits, z = depth/err normalised by each target's robust
    scale beyond 3 d from any edge. Declared criterion: smallest X such that every 0.25-d bin beyond X has pooled fraction |z| > 3
    <= 0.03 (interior level 0.02). Result: AFTER a data resume following a gap > 0.5 d (sector start counts) X = 1.5 d (pooled
    |z|>3 fraction 0.31, 0.25, 0.07, 0.09, 0.09, 0.06 in the 0.25-d bins to 1.5 d; 0.02-0.03 after; worst 183374279 S96/S105: z up to
    +26 in the first 0.1 d, overshoot to -5.6 at 0.3-0.4 d); BEFORE any gap > 0.1 d or the data end X = 0.5 d (0.12, 0.17 in the
    first two bins; 0.02 after; 115692561 S96 worst). After short (< 0.5 d) downlink gaps no excess (0.006, 0.000). Implementation:
    those cadences are removed before detrending; events then fail coverage/baselines by the existing rule, and the +-0.3 d search
    cannot use edge data. QLP S106 is not on MAST (2026-10-20 directory listing ends at s0105); S106 data gaps are therefore
    estimated from catalogs/TESS_orbit_times.csv (SHA 40ed1f99...) plus in-sample QLP gap patterns, never from test-target files.
77. 2026-10-20 — DISCRIMINATING TEST (decision 3), declared before running. Design sectors only (S96; S97 for 122522485; no clock path
    needed, all < 99). Per target, 40 realisations, each at a random phase in [0.2, 0.8] (seed 77 + TIC), back-projected predictions with
    the test's own mean S106 sigma_min, locked depth/T14. Five cases: null (no injection); on-time reference box; opposite offsets
    (+(gate+20) min on even epochs, -(gate+20) min on odd epochs, so every event lies 20 min outside its gate); 0.6 x T14; 1.5 x T14
    (reference depth, on time). Edge rule (item 76) in force.
    ADD-ON (timing split), defined now: when the joint rule gives RECOVERED, split the eligible events by epoch parity; for each half,
    stack (inverse variance) at the joint duration over the same local offset window and take its best offset; the add-on requires both
    halves non-empty and both best offsets |o| <= gate. Otherwise the outcome becomes AMBIGUOUS. Reported as outcome_with_split.
    Claimed behaviour to restore (v2.0 document): opposite offsets and 0.6x/1.5x durations are not RECOVERED; on-time reference
    transits are. Judged per target: false RECOVERED (null, opposite, 0.6x, 1.5x) and on-time RECOVERED rates with Clopper-Pearson 95%.
    Decision rule: if with the add-on every target has opposite-offset RECOVERED <= 10% and on-time RECOVERED loses <= 10 points vs
    without, the add-on is adopted; durations are judged separately (the protocol band 0.7-1.3 cannot be resolved at per-event SNR ~1,
    so their rates are disclosed rather than "restored"). Otherwise a literal per-event evaluator is proposed to the user.
78. 2026-10-20 — Other v2.1 changes made while item 77 ran (none alters an outcome rule beyond items 76-77):
    - per_event_min_reading added (secondary readout honouring the published CLARIFICATION promise of an individual-event min()
      assessment): an eligible event matches if its own best box has SNR >= 3, depth 0.5-1.5x, duration 0.7-1.3x, |offset| <= min gate;
      met if >= 2 match. (Edited while item-77 runs were in progress; it adds an output field only.)
    - test_conformance.py relabelled LOGIC TESTS (about 10x operating SNR; not performance evidence); span widened to BTJD 97-108 so the
      edge rule does not remove the BTJD-100 event (new noise realisation, same seed and expectations).
    - S106 has no 2-min data for any of the seven targets (catalogs/target_lists/all_targets_S106_v1.csv SHA dc8eb3f1...,
      catalogs/tesscurl_sector_106_lc.sh 42daeac2...): QLP is the product under the protocol's own rule; SAP vs DET_FLUX is a departure.
    - Environment lock: results/conformance_v21/requirements_venv_locked.txt (80 packages; numpy 2.5.4, scipy 1.18.1, pandas 2.3.3,
      astropy 8.0.2, wotan 2.0). The published requirements_venv.txt files are empty (to be replaced at the next release).
    - S106 edge forecast (scripts/conformance_s106_forecast.py; results/conformance_v21/s106_forecast.*; no S106 photometry used; 7
      in-sample QLP gap templates mapped onto S106 orbit breaks): eligible events min/median/max and joint SNR (median):
      70441745 1/2/2, 10.7 | 115692561 16/19/23, 2.8 | 120444365 2/2/3, 4.8 | 122522485 6/7/10, 3.5 | 183374279 1/1/2, 4.2 (2 events
      in 2/7 templates) | 206620592 13/16/20, 5.5 | 253931796 0/1/1 (INSUFFICIENT in every template: epoch 173 falls 0.2 d before the
      mid-sector downlink break, inside the 0.5-d pre-gap zone; epoch 172 within 1.66 d of the sector start).
79. 2026-10-20 — DISCRIMINATING TEST RESULT (item 77; 1400 runs, evaluator SHA c6fdfa41... plus a readout-only edit mid-run, harness
    4807c5ec...; results/conformance_v21/discriminating_{raw,runs,summary}.*). RECOVERED, scored runs, CP 95%:
      on-time   70441745 38/40 | 120444365 34/40 | 122522485 28/40 | 183374279 39/40 | 206620592 21/40 | 253931796 40/40 | 115692561 0/40
      opposite  3/40 | 3/40 | 0 | 12/40 | 0 | 0 | 0           null 0/40 everywhere
      0.6xT14   19 | 16 | 10 | 21 | 5 | 1 | 0 (of 40)       1.5xT14  0 | 9 | 14 | 6 | 15 | 1 | 2
    With the timing-split add-on: opposite 0,0,0,1,0,0,0; on-time 38, 28 (-6 runs = -15 points), 28, 37 (-5 pts), 21, 39, 0.
    Literal per-event alternative (>= 2 events each with own best box SNR >= 3, depth/duration in band, within gate): on-time 29, 10,
    0, 26, 0, 40, 0 - power collapses for four tests.
    By the declared rule (on-time loss <= 10 points for every target) the add-on FAILS on 120444365 (-15 points; CIs overlap), so per
    item 77 the literal per-event evaluator is put to the author - with the recommendation to adopt the add-on anyway, because the
    literal alternative is far worse on every target and the add-on removes the opposite-offset failure (30% -> 2% on 183374279).
    Duration: 0.6x/1.5x T14 cannot be separated from the 0.7-1.3x band at these SNRs (up to 52% RECOVERED); disclosed, not claimed.
    EXCLUDED (old rule): displaced real transits read EXCLUDED (70441745 opposite 33/40, 206620592 5/40).
    EXCLUDED v2.1 (decision 2) implemented now: (a) max over |o| <= gate at D = ref of stacked depth + 3 err < 0.3 x ref; (b) per-event
    chi2 p >= 0.01 at the prediction; (c) no VALID fit with SNR >= 5 and depth >= 0.5 x ref anywhere within +-0.3 d. Logic suite 15/15,
    input suite 18/18 after the change. Re-run of null/on-time/opposite under the new rule launched (same seeds, so same placements).
80. 2026-10-20 — Provenance of item 79: the 1400 discriminating runs record evaluator SHA c6fdfa41... (481 runs, as launched) and
    4858c3b6... (919 runs, after the readout-only per_event_min edit); outcome logic identical. EXCLUDED re-run under the v2.1 rule
    (same seeds; results/conformance_v21/discriminating_excluded_rerun*): displaced transits read EXCLUDED 0/280 (was 70441745 33/40,
    206620592 5/40); nulls read EXCLUDED only for 253931796 (39/40) and 183374279 (1/40); 70441745 nulls 30/40 -> 0/40 because condition
    (a) (depth + 3 err below 0.3 x ref everywhere in the +-130-min gate) fails (median ratio 1.39). Kept: excluding a transit whose time
    is uncertain by +-130 min requires excluding it across that window; without (a) alternating displacements read EXCLUDED. Stated in
    advance: EXCLUDED is effectively reachable only for 253931796. Note: pandas reads the case label "null" as NaN; summaries now use
    keep_default_na=False (an interim tally that dropped null rows was not used for any decision).
    EDGE RULE OPTIONS for the author (no S106 data used): A (declared, item 76) pooled noise criterion: 1.5 d after resume, 0.5 d
    before any gap > 0.1 d. B (same 0.03 criterion, counted per target, only positions with |z| > 3 AND |depth| > 0.3 x ref): per target
    (after / before long gap or end / before short gap, d) 183374279 2.25/3.0/2.25, 120444365 1.0/0.5/0, 70441745 2.0/1.0/0.5,
    206620592 1.75/0.75/0.5, 122522485 0/1.75/1.75, 253931796 0/0/0, 115692561 0.5/0.75/1.75 (10-65 positions per 0.25-d bin).
    Forecast eligible events (min/median/max), B vs A: 183374279 0/0/0 vs 1/1/2; 253931796 0/1/2 vs 0/1/1; 120444365 3/3/4 vs 2/2/3;
    others similar. Pooled, criterion B gives the same 1.5/0.5 d as A (and 1.75 d before short gaps). Per-target noise criterion
    (|z| only) was also computed: 253931796 2.5/2.5 d, no help. Recommendation: A (pooled, larger samples); B trades one test for another.
81. 2026-10-20 — Add-on cost pinned (results/conformance_v21/discriminating_{ontime160,randsign,extra_summary}*): on-time RECOVERED,
    160 realisations: 120444365 119/160 (0.74) -> 103/160 (0.64) with the split; 183374279 151/160 (0.94) -> 137/160 (0.86). Cost ~10
    and ~9 points: at the declared 10-point limit (the 40-run figure of -15 was noise). Random-sign displacements (+-(gate+20) min, sign
    random per event; the split by epoch parity defeats only alternating patterns): false RECOVERED 183374279 8/40 -> 5/40, 120444365
    3/40 -> 1/40 (8/40 and 1/40 INCONSISTENT). Disclose: the split check does not catch random-sign displacements reliably.
    STATUS: design paused for two author decisions (add-on vs literal per-event evaluator; edge rule A vs B). Holdout calibration
    (scripts/conformance_calibrate_holdout.py, ready, not run) waits for the final design. Drafts: results/GOVERNANCE_S106_TESTS_DRAFT.md
    (hierarchy, departures, tex:35 erratum sigma 4.7 -> 2.1), results/conformance_v21/requirements_venv_locked.txt. Nothing published.
82. 2026-10-20 — AUTHOR DECISIONS: keep the timing-split check (A) and the pooled edge rule (B, option A of item 80). Implemented as
    conformance-v2.1-rc1 (prereg_conformance.py SHA 590502679b335e8b93f7f30612dda58894112fbbf83f0fb62f8b0acbaf5ac684): the split check is now part of the outcome of record (joint-only outcomes
    kept as readouts); odd/even depth diagnostic added (information only); docstring updated (edge rule, split, EXCLUDED). Logic suite
    15/15, input suite 18/18. Configs regenerated (reference values unchanged; evaluator string v2.1, evaluator_sha256, both frozen-
    evaluator commands locked (SAP_FLUX = same inputs; DET_FLUX = protocol column), edge rule, 183374279 stricter clause recorded);
    v2.0 configs kept in results/conformance_v21/configs_v2.0_backup/. Holdout calibration launched on this SHA (N = 40 per case, cases
    null/ontime/displaced, 9 holdout sector-target pairs). The evaluator is not edited while it runs.
83. 2026-10-20 — Pre-review packaging: GOVERNANCE draft corrected (raw-SAP wording: reference depths are raw SAP, ephemerides also
    use SPOC 2-min; 183374279 values come from the post-freeze addendum; T14 rule: shape fit has no T14 field so BLS 2.0/1.5 h were used,
    shape-implied 2.18/1.97 h; superseded 120444365 v1 S106 file; changes from earlier commitments; TESScut cross-check withdrawn for
    all seven). New results/CONFORMANCE_PROCEDURE_v2.1_DRAFT.md and results/PROMPT_conformance_review_v21.txt (the v2.0 prompt is stale).
    Holdout integrity: 907 S106 files on disk (other stars' SPOC 2-min, withdrawn 88407114, third-party sweep files); none is, or
    mentions, any of the seven test TICs (file names and text grep only; no file opened as photometry).
84. 2026-10-20 — HOLDOUT CALIBRATION done (1080 runs, all on evaluator SHA 59050267..., the SHA in the regenerated configs;
    results/conformance_v21/holdout_calibration_{runs.csv,report.md}; scripts/conformance_calib_report.py). Nulls falsely RECOVERED
    0/352 scored (N_eff 25 in total; 95% upper bound 0.14 per test; family-wise rate not constrained beyond that). On-time RECOVERED:
    70441745 37/40 | 120444365 32/72 (S69 4/36, S103 28/36) | 183374279 45/80 (S69 8/40, S103 37/40) | 206620592 15/40 |
    122522485 0/40 (design S97, a double sector, gave 28/40) | 253931796 38/40 | 115692561 0/40. Displaced -> INCONSISTENT: 31/40,
    12/72, 31/80, 0, 0, 37/40, 0. Nulls -> EXCLUDED: 253931796 37/40, 183374279 7/80, 120444365 1/72, others 0. Holdout power is lower
    and more sector-dependent than design power; the procedure draft and the amendment drafts
    (results/conformance_v21/REGISTRATION_AMENDMENTS_DRAFT.md, not appended) state the holdout figures. Package ready for external review.
85. 2026-10-20 — Provenance and packaging (advisor check before review): evaluator SHA of the item-80/81 runs: EXCLUDED re-run 840
    runs, 160-run on-time and random-sign runs 400 runs, all 17c6ca71... (after the EXCLUDED rule, before the split promotion; their
    "outcome" is joint-only, "outcome_with_split" carries the split). Holdout calibration: 59050267... (= configs). Harnesses now also
    record outcome_joint_only; scripts/conformance_disc_analyse.py added. Procedure draft: edge-rule wording, other uses of holdout
    sectors (clock validation S103/S105 timestamps only; S68 c0), "INSUFFICIENT = no TESS test" for 183374279/253931796 (no sector
    through S134), clock warnings 0/360. Manifest: results/conformance_v21/README.md.
86. 2026-10-20 — EXTERNAL REVIEW of v2.1-rc1 (results/REVIEW_conformance_v21.md; OpenAI Codex; verdict "publish after listed fixes").
    CORRECTIONS TO THIS LOG: (i) item 81's "the 40-run figure of -15 was noise" is withdrawn: the declared item-77 rule (40 runs, <= 10
    points) FAILED for 120444365 (-15); the 160-run sample reuses those 40 phases and is an exploratory refinement, not a pass. The
    author kept the split by overriding the declared rule on its trade-off against the alternatives (item 82). (ii) Item 76's edge rule
    does not meet its own literal criterion in every later bin (1.75-2.0 d after resume 7/229 = 0.031; before gaps > 0.1 d, 0.5-1.25 d
    bins 0.043, 0.035, 0.051): 1.5 d / 0.5 d is an author-selected pooled rule chosen after inspecting the design profiles. (iii) Item
    76's "holdout ... not looked at for design" is too broad: 120444365 S69 had evaluator/timing fits in the v2.0 development (internal
    critic), and the S106 forecast uses QUALITY/timing metadata of S68/S69/S105. (iv) Item 83's integrity statement is narrowed: one
    S106 1x1 TESScut cutout of 206620592 exists in the session scratch (scratchpad/s106/), disclosed earlier in the S106 erratum and
    never opened as data here; filename searches cannot prove non-examination. (v) The item-84 "N_eff 25 / 0.14 per test" bound is
    withdrawn (invalid). Running the reviewer's probe script to check the fix rewrote its result file under /tmp/conformance_v21_review/
    probes704/ (its original output is quoted in the review).
    FIXES (conformance-v2.1-rc2, prereg_conformance.py SHA 000b0dfb16e0cc7080ff5645885babd859806ae0de40645b07a93cfe5c5d3cb7; rc1 kept as results/conformance_v21/prereg_conformance_rc1_59050267.py):
    R3 EXCLUDED requires every eligible event measured at every gate offset; R6 config strict_epochs (183374279: 245, 246) enforced
    deterministically -> INSUFFICIENT, procedure outcome kept as outcome_before_override; R7 release_of_record v01 enforced, a clock-record
    whole-cadence warning now refuses scoring (CLOCK_UNVERIFIED); R13 config/prediction invariants, duplicate times refused, evaluator
    SHA in the config enforced, no usable data after the edge rule -> INSUFFICIENT. Input suite 27/27 (9 new regression cases incl. the
    reviewer's R3 probe), logic suite 15/15. Configs regenerated (reference values unchanged; provenance labels corrected; 183374279
    "post-freeze dated addendum"; amendment T14 label "BLS duration (shape fit has no T14 field)"). Clock tool docstring corrected
    ("one gap is not enough" -> margin-dependent; SHA 0b768374328ba9dc...). R8 calibration harness: no masking for P > 6 d (placements >= 0.3 d + 7.5
    T14 from real transits); P <= 6 d masked +-(T14/2 + 10 min) in clock-corrected time. R2 reports: raw counts, all categories,
    conditional CP only; no effective-N or family-wise bound. Holdout re-calibration launched on rc2 (the holdout sectors are now
    already-seen development evidence; disclosed).
87. 2026-10-20 — rc2 HOLDOUT RE-CALIBRATION (1080 runs, all evaluator 000b0dfb16e0cc70... = configs; results/conformance_v21/holdout_calibration_rc2_
    {runs.csv,report.md}). Nulls falsely RECOVERED 0/346 scored; on-time RECOVERED 70441745 40/40 | 120444365 30/71 (S69 3/35, S103 27/36)
    | 183374279 46/80 (S69 9/40, S103 37/40) | 206620592 11/40 | 122522485 0/35 | 253931796 40/40 | 115692561 0/40; displaced ->
    INCONSISTENT 33/40, 12/71, 26/80, 0, 0, 40/40, 0; nulls EXCLUDED 253931796 39/40, 183374279 6/80, 120444365 1/71; not scored:
    120444365 27 INSUFFICIENT, 122522485 15 INSUFFICIENT (122522485 masks trigger the pre-gap trim; disclosed); clock warnings 0/360.
    Procedure draft rc2 filled in; amendments regenerated (conditional wording, rc2 SHA, enforced strict epochs); manifest refreshed.
    Focused re-check prompt for the external reviewer: results/PROMPT_conformance_recheck_rc2.txt. Nothing published.
88. 2026-10-20 — RE-CHECK of rc2 (results/REVIEW_conformance_v21_rc2.md; verdict "publish after listed fixes"; R1-R5, R7, R8, R11,
    R12 resolved; R6, R9, R10, R13 partial). Fixes as conformance-v2.1-rc3 (SHA 579d50acbcaba7ec67e64ec20868c8322497a30c2f0f7c4b4fd31467f0522bbd; rc2 kept as
    results/conformance_v21/prereg_conformance_rc2_000b0dfb.py): N1 strict-epoch check now catches a single missing cadence (spacing >
    1.5 cadences; window edges > 1.05 cadences; rows with non-finite TIME count as missing); N2 docstring/governance wording (amended
    operational test; Delta-chi2 is a nominal score rule, not a likelihood or 2-sigma interval; the parity split reduces but does not
    eliminate timing failures); N3 rc2 sector rates corrected, per-offset EXCLUDED event counts now emitted, the 1/160 on-time
    INCONSISTENT design result stated; N4 all-flagged product -> INSUFFICIENT like an edge-emptied one (classified before the clock
    gate, documented), TIMEUNIT/TIMEREF/BJDREFF validated, epochs must be finite integers. Input suite 31/31 (4 new), logic 15/15.
    RECOVERED/INCONSISTENT/split/EXCLUDED logic unchanged from rc2. Configs regenerated (evaluator SHA only). Holdout re-run on rc3 so
    every calibration result carries the final SHA.
89. 2026-10-20 — rc3 HOLDOUT CALIBRATION (1080 runs, all on evaluator 579d50ac... = configs; results/conformance_v21/
    holdout_calibration_rc3_{runs.csv,report.md}): outcomes identical to rc2 for all 1080 runs (scoring logic unchanged); 0/346 null
    false RECOVERED; clock warnings 0/360. Procedure draft, amendment drafts (rc3 evaluator and config SHAs) and manifest refreshed.
    Second focused re-check prompt: results/PROMPT_conformance_recheck_rc3.txt. Dossier review prompt (results/referee_89247735/
    PROMPT_dossiers_review.txt) updated with the S106 holdout rule and the 61310956 observability note before sending (original kept as
    *_2026-10-19.txt). Nothing published.
90. 2026-10-20 — External dossier referee (results/referee_round2/REFEREE_REPORT_dossiers_external.md; OpenAI Codex): both
    candidates "revise; retain candidate status" (61310956 with a photometric-systematics caveat). No S106 data used. Key items:
    183374279 - pixel "excludes blends" and "RV constant" overstated, density ratio convention (1.24 with the adopted TIC M/R, not
    1.45), contaminant fraction band/aperture, radius range is illustrative, availability text stale vs the S106 erratum, S106 outlook
    must be conditional, holdouts are retrospective. 61310956 - DOSSIERS.md still shows superseded v2 and the "independent 11 sigma
    SPOC" claim; frozen v3 reference T14 is 2.70 h while prose says 3.3 h (needs a dated clarification BEFORE any ground observation);
    odd/even is baseline-sensitive (global SAP 3.75 sigma, local-linear 1.76 sigma, DET 1.20 sigma); sigma 28-33 min through 2027;
    "likely planet" label must go; S72 raw-aperture figure unexplained; epoch-83 CSV status note. Shared: pixel calibration is not
    source-localisation validation; NFPP = 0 is structural; "empirical sigma" is not Gaussian; Gaia gives no mass limit; VERDICTS
    placeholders. CORRECTION (my error): the 61310956 observing note used the time-scale-only UTC column; the geocentric epoch-151
    mid-time is 2026-12-29 04:21:53 UTC, and "fully observable" overstated nominal-transit access. STATUS corrected.
91. 2026-10-20 — SECOND RE-CHECK of rc3 (results/REVIEW_conformance_v21_rc3.md; "publish after listed fixes; blockers remain").
    CORRECTION: item 88's "input suite 31/31" was a false pass. Every case wrote to one output file and exit codes were ignored, so the
    crashed all-flagged case read the previous case's INSUFFICIENT (reviewer F2). Fixes as conformance-v2.1-rc4 (SHA a864b07ace8d3220a2d94a60513a488c8a5d87b54f41ebf510ff40ef1755311f; rc3 kept as
    results/conformance_v21/prereg_conformance_rc3_579d50ac.py):
    - F1: an all-flagged input no longer crashes (edge rule skipped when no usable cadences remain) and returns INSUFFICIENT.
    - F4: TIMEUNIT d and TIMEREF SOLARSYSTEM are required; a non-numeric BJDREFF returns INVALID_INPUT.
    - F2: test runners hardened (fresh output path per case, exit code required, the result must match the requested light-curve
      and config hashes; a crash fails the case); the logic suite also checks exit codes.
    - Input suite 35/35 (4 new cases), logic 15/15.
    - F3: the governance strict-clause text now matches the code (> 1.5 cadences; edges > 1.05; non-finite TIME rows discarded).
    - F5: the calibration report takes a version label; the rc3 report is relabelled.
    Procedure wording: rc3/rc4 changed the strict override and input handling, not the joint calculations. Configs regenerated
    (evaluator SHA and locked_utc only). Holdout calibration re-run on rc4.
92. 2026-10-20 — Dossier referee corrections applied locally (user: "Yes"); nothing published or committed.
    - results/round2_dossiers/DOSSIERS.md rewritten for both objects; the 2026-10-19 text is kept as DOSSIERS_2026-10-19.md, and the
      frozen excerpts are verbatim, with the 61310956 v2 excerpt marked SUPERSEDED. Corrected: conditional pixel and RV wording,
      density ratio 1.24 with the adopted TIC M/R, band- and aperture-dependent contaminant fractions, an illustrative radius range,
      retrospective holdouts, SPOC as an extraction check, the "likely planet" label withdrawn, NFPP 0 called structural, the
      baseline-sensitive odd/even caveat for 61310956, sigma 28-33 min, the S72 figure caveat, S106 conditional eligibility and the
      erratum link.
    - Dated clarification appended to results/vet_allsky/61310956/PREREGISTRATION_v3.md (CSV bytes unchanged): the frozen 2.70-h
      reference governs (band 1.89-3.51 h); planning uses 3.3 h + +-3 sigma + 1-h baselines (about 8.1-8.2 h); epoch 83 is a training
      event; geocentric times; odd/even reporting.
    - public_release/README.md working copy updated with the same corrections (uncommitted; goes into the next release with the user's
      go; the v1.10 text is kept in the session scratch).
93. 2026-10-20 — rc4 HOLDOUT CALIBRATION (1080 runs, all on evaluator a864b07ace8d3220... = configs; results/conformance_v21/holdout_calibration_
    rc4_{runs.csv,report.md}): outcomes identical to rc3 (and rc2) for all 1080 runs; 0/346 null false RECOVERED; clock warnings 0/360.
    Procedure draft, amendment drafts (rc4 evaluator and config SHAs) and manifest refreshed. Third focused re-check prompt:
    results/PROMPT_conformance_recheck_rc4.txt. Nothing published.
94. 2026-10-20 — THIRD RE-CHECK of rc4 (results/REVIEW_conformance_v21_rc4.md): "Publish as declared procedure; no remaining
    publication blockers found" (F1-F5 resolved; suites reject crashes and stale results; provenance of all 1080 rc4 results checked).
    Editorial items applied: procedure intro cites items 70-93 and the four reviews; governance names the rc4 evaluator SHA. Not acted
    on (cosmetic, per reviewer): NumPy "mean of empty slice" warning on empty inputs. The evaluator bytes are frozen at rc4 (a864b07a...);
    publication dates and dated filenames are filled at release. AWAITING THE AUTHOR'S GO TO PUBLISH; no S106 photometry of any test
    target is examined before that release.
95. 2026-10-20 — Reviewer update to the rc4 report: approval stands; two manifest hashes were stale (procedure and governance, changed
    by the item-94 editorial edits). Manifest regenerated (80 files incl. the rc4 review and prompt) and every entry re-verified.
96. 2026-10-20 — RELEASE v1.11 (user: "go"). Content: conformance_v2.1/ (procedure CONFORMANCE_PROCEDURE_v2.1.md, governance
    GOVERNANCE_S106_TESTS_2026-10-20.md, ERRATUM_PROTOCOL_2026-10-20.md (tex:35 sigma 4.7 -> 2.1), evaluator rc4 a864b07a... + clock tool
    + frozen prereg_test.py 630815cc..., locked configs, all conformance scripts, results/conformance_v21 outputs, the seven clock priors
    as cited, all review reports and prompts incl. the masked internal findings JSON); dated 2026-10-20 amendments appended to the seven
    S106 registrations (the three earlier unpublished 2026-10-20 amendments are published as written; their v2.0 citation is superseded);
    61310956 v3 clarification; README corrections from the dossier referee and a v1.11 note; dossier referee report; environment lock;
    DECISIONS public copy (items 1-96, withheld object masked); MANIFEST_v1.11.md; CITATION 1.11. Zenodo: the repository record
    versions automatically via the GitHub integration; the protocol record gets v1.4 (unchanged v1.3 PDF + erratum + governance +
    procedure) by script. Not in this release (pending a separate go): the dataset_v1 bundle and the two-candidate preprint.
97. 2026-10-20 — v1.11 PUBLISHED. GitHub commit 655c229, tag and release v1.11
    (https://github.com/fergmolina/tess-transit-candidates/releases/tag/v1.11); Zenodo repository version v1.11 10.5281/zenodo.23508798
    (automatic GitHub integration); protocol record v1.4 10.5281/zenodo.23508864 (scripts/zenodo_newversion_staged.py: draft inspected,
    then published; PDF and v1.3 bundle byte-identical to v1.3; added erratum, governance, procedure and conformance_v2.1.zip, built by
    git archive of tag v1.11). Pre-publication checks: withheld TIC absent from the staged tree and the zip; every config, amendment and
    published script carries evaluator SHA a864b07a...; prediction CSVs match their locks; no S106+ file of the seven targets anywhere.
    The old (2026-10-18) Zenodo token was used; the author should revoke it now. Still pending (separate go): dataset_v1 bundle and the
    two-candidate preprint. NEXT: score the seven S106 tests once QLP S106 is released (declared test; needs the author's go).
98. 2026-10-20 — FULL-REPO REVIEW of v1.11 (results/REVIEW_full_repo_v1.11.md; external; verdict "corrections required"). All 56 public
    prediction CSVs keep their first-committed bytes and the manifests verify; the v5 ephemeris reproduces. Findings:
    - MASKING: the withheld object's query coordinates (ra/dec) remain in public prior_search/PRIOR_SEARCH.md:160 and
      prior_search/query_log_all.csv (8 rows), public since v1.4 (2026-10-18) and in every repo release and Zenodo archive since. The
      withheld rows in tables/allsky_testable_soon.csv and allsky_classA_outcomes.csv also carry period, depth and sectors (by the
      earlier design). My v1.11 pre-release scans checked only the TIC number - an inadequate check; corrected practice: scan
      withheld rows for coordinates and other identifiers.
    - CODE: vet.py transit_model infers exposure from folded times (F3); per-event holdout numbers repeat the stacked value (F4);
      legacy UTC producers (F5); freeze outputs can be overwritten (F14); public/local script drift, missing producers, absolute
      paths, incomplete environments (F2, F6-F8); single_injection b docstring (F29).
    - CLAIMS: withdrawn TIC 89247735 mass/localisation claims remain in README/REPORT/dataset (F9); the 4th event does not exclude the
      2P EB (F10); TIC 80387959 FPP/NFPP are ABOVE the validation thresholds (F11); "single star"/RV mass exclusion unsupported (F12);
      "before the test data exist" wording in note/dataset/protocol metadata (F13); superseded S104 clock certification in REPORT
      (F17); "out-of-sample"/"blind" wording (F18); BLS log-grid fraction presented as a chance probability (F19); plus stale
      observing plans, numbers, the novelty scope, document status, the CITATION DOI (it points at v1.1) and links (F20-F25, F28).
    - PRIVACY: Claude session URLs in 25 commit messages and in the Zenodo v1.11 description (F26); a DDT recipient email in the
      public DECISIONS.md (F27).
    Awaiting the author's decisions on masking remediation and session links; a v1.12 corrections release is proposed.
99. 2026-10-20 — Correction e-mailed by the author to the TESS DDT office for the TIC 80387959 proposal (wording reviewed by the
    external agent): FPP/NFPP above the validation thresholds; no single-star or RV mass-exclusion claim; holdouts retrospective; the
    neighbouring EB scenario remains open; the request is unchanged. Starting the v1.12 corrections (forward correction; no history
    rewrite; nothing published before the author sees it).
100. 2026-10-20 — v1.12 CORRECTIONS prepared locally (not published), after the full-repo review (item 98):
    - F1 masking: the withheld object's coordinates, 2MASS/Gaia/UCAC4/APASS/WISE and extra AllWISE/SkyMapper/unWISE/GSC identifiers
      are removed from public prior_search/ (260 object rows: query/URL/hits/note -> [withheld]; 13 other lines scrubbed); a dated
      correction note heads PRIOR_SEARCH.md. The whole tracked tree was rescanned for aliases, decimal and sexagesimal coordinates: no
      alias remains (the remaining short-digit matches are timestamps and unrelated numbers, checked in context). No history rewrite.
    - F27: scripts/make_public_decisions.py writes the public log (withheld number masked; DDT e-mail -> "the TESS DDT office").
    - F23: CITATION DOI -> concept 10.5281/zenodo.23443244.
    - Claims (F9-F13, F15-F22, F24, F25, F28): REPORT gets a dated current-status block plus inline Superseded/Corrected markers;
      README candidate summary, novelty, freeze-timestamp, reproduction limits and observing times corrected; dated clarifications
      appended to TIC80387959/PREREGISTRATION_v2.md (FPP/NFPP above thresholds) and CORRECTION_UTC_2026-10-19.md (legacy raw-BJD
      labels); note_allsky/note.tex corrected (validation, Gaia, retrospective checks, S106 data-availability wording; recompiled);
      paper/README status (AJ draft not submitted; RNAAS submitted); dataset_v1/README notice prepared for a v1.1 dataset version.
    - Code (F3, F4, F5, F14, F18, F29): vet.py per-point exposures from unfolded times (folded-time inference could give 0 s; synthetic
      check: model within 110 ppm of a fine-supersampled reference vs 775 ppm before), per-event holdout depths (1000/3000/6000 ppm
      recovered; previously 3333 each), geocentric UTC via scripts/time_utils.py in vet.py and final_ephemeris_317134140.py, training-shape
      fallback recorded; prereg_v2.py/prereg_candidate.py refuse to overwrite a frozen version and dry runs write to _dryrun/ (not
      executed end to end); single_injection docstring b = 0. None of this changes a frozen file. Affected exploratory outputs:
      report.json "ephemeris" and retrospective holdout numbers; frozen v2 ephemerides use prereg_v2's own per-sector cadence model.
    - F2/F6/F7: public scripts synced to the local versions that ran (10 files + time_utils.py); 4 missing producers published; the
      end-to-end injection scorer was ad hoc and is not recoverable (stated); TRICERATOPS environment pinned.
    - Not changed: absolute paths in code (F8) are disclosed, not refactored. Pending the author's go: session links (F26), Zenodo
      metadata edits (v1.11 description; protocol v1.4 opening text, F13), new Zenodo versions of the dataset and the two-candidate
      preprint, and publishing v1.12.
101. 2026-10-20 — Author decisions: (1) no Claude session URLs in commits, release notes or Zenodo descriptions from now on (keep the
    Co-Authored-By credit; history before v1.12 not rewritten); (2) publish v1.12; (3) edit Zenodo metadata: remove the session link
    from the v1.11 repository description and correct the protocol record's "before the test data exist or are public" wording. New
    Zenodo versions of the dataset and the two-candidate preprint remain pending.
102. 2026-10-20 — v1.12 PUBLISHED: GitHub 73ac202, release v1.12 (no session link in the commit or the notes); Zenodo repository version
    v1.12 10.5281/zenodo.23510604 (automatic). Zenodo metadata edits (scripts/zenodo_edit_description.py; staged, inspected, published):
    the session link was removed from the v1.11 description (23508798); a dated notice on S106 data availability was prepended to the
    protocol record description (23508864; the historical paragraphs are kept). All three checked afterwards: no session links. Old
    token used; the author should revoke it. Pending (separate go): new Zenodo versions of the dataset bundle (README notice prepared)
    and the two-candidate preprint (note_allsky/note.tex corrected and recompiled).
103. 2026-10-20 — Author reports the RNAAS licence form signed and the AI-disclosure request e-mailed to AAS (AAS82560).
104. 2026-10-20 — RE-CHECK of v1.12 (results/REVIEW_full_repo_v1.12_recheck.md: "v1.12 needs further corrections; preprint needs wording
    fixes; dataset must not be published as staged"). Fixes (v1.13, local, not published):
    - N1 (blocker): the staged dataset still redistributed the withheld object's coordinates/aliases. Worse than reported: the
      PUBLISHED dataset v1 zip (10.5281/zenodo.23462438, 2026-10-19) carries its coordinates in 15 external_review_allsky scripts and
      aliases in the Gaia/VizieR outputs and prior-search copies (TIC number itself absent). New dataset_v1.1/ (v1 left intact): prior_search
      replaced by the redacted v1.12 copies; every "[withheld]" entry in 27 external_review_allsky files replaced by a placeholder (one diff
      hunk per file); whole-folder rescan clean.
    - N2: dataset_v1.1 README notice in the reviewer's wording (legacy status, withdrawn claims, TESS or ground tests, target QLP light
      curves, empty environments, 4.54-h T14, CTIO qualification); checksums regenerated (210 files, all verify, manifests excluded).
    - N3: vet.per_point_exposure is now segment-aware (split at gaps > 0.1 d) with a +-5-cadence median, which is robust to missing
      cadences; it is used in fit_shape, mcmc_shape, time_transits and global_ephemeris. Tests: mixed 600/200 s -> 600/200; 200 s with
      every 7th cadence missing -> 200; 1800 then 120 s -> 1800/120; F3 probe still 1800. Old exploratory values are explicitly NOT
      recomputed and are flagged in the README.
    - N5: prereg_v2 refuses before any data access if any output member of the version exists (tested on a throwaway TIC with a JSON-only
      sentinel: refused, sentinel intact, folder removed); prereg_candidate is marked LEGACY and refuses all freezes.
    - N4: five preprint wording fixes (rules/evaluator vs conformance, repository scope, neighbour EB open, speckle wording, DDT
      submitted + corrected); recompiled, 2 pages.
    - N6-N8: README provenance sentence, observing wording, TIC 183 procedure now published, DOI badge/citation = concept DOI, version list;
      REPORT TIC 803 first transit 01:20 UTC; STATUS header and TIC 613 row; RNAAS local source labels v1.9 as the analysis release
      (as-submitted copy kept as paper/rnaas/note_as_submitted_AAS82560.tex; it differs only in the first-line comment).
105. 2026-10-20 — Re-check of the v1.13 staging (results/REVIEW_v1.13_dataset_preprint_recheck.md: fixes needed on all three; N2, N4, N5,
    N7, N8 resolved). Fixed: (1) dataset_v1.1 mast_products.json - six nested product URLs still encoded the withheld TIC as QLP path
    components (filename masked, directories not); the object's whole entry and the six per-sector URL values are now [withheld], and the
    split-path forms were added to the scan patterns (whole public tree, dataset and preprint rescanned clean); checksums regenerated
    (210, all verify). (2) README exposure wording narrowed (spacing-based estimates unreliable for severely thinned or ambiguous
    segments; cadence metadata needed). (3) Preprint: one sentence saying the quoted shape and retrospective-check summaries are historical,
    not recomputed, and not precision constraints; recompiled, 2 pages. (4) README provenance wording ("current local copies"). Manifest refreshed.
106. 2026-10-20 — Final re-check (results/REVIEW_v1.13_final_recheck.md): v1.13 yes, dataset v1.1 yes, preprint yes, no remaining fixes.
    Publishing (author's standing instruction: publish when all three are cleared): GitHub v1.13; Zenodo dataset v1.1 (record 23462438);
    preprint as v1.3 (the latest existing preprint version is v1.2, 23463582; I called it "v1.2" earlier by mistake).
107. 2026-10-20 — PUBLISHED: GitHub v1.13 (1620a8b; Zenodo 10.5281/zenodo.23512921, automatic); dataset v1.1 10.5281/zenodo.23512928
    (zip of dataset_v1.1, 212 members, rescanned clean before upload; md5 665d8021...); preprint v1.3 10.5281/zenodo.23512950 (md5
    4666ac0b...; the version note replaces "all code and data are public"). All via draft -> inspect -> publish; no session links.
    The old Zenodo token was used again; the author should revoke it. Everything from the full-repo review is now published.
108. 2026-10-20 — AUTHOR DECISION ("Go 2", confirmed "go" after the auto-mode classifier paused the first unmasking step): publish the
    previously withheld object TIC 120517801 openly, as a likely blend with the host unresolved and an independent rediscovery (eumemic
    2026-10-09; Rahle 2026-10-18). Pre-registration chain: the v1 (cbb409bb...) and v2 (0e6bd698...) hash prefixes have been public
    in DECISIONS.md since v1.3 (commit 24cd0de, 2026-10-18 23:24:45 UTC); the full freeze times are local attestations; its tests are
    S111-S113 (S111 starts 2026-11-26), not yet observed. Actions (v1.14, local until reviewed):
    - preregistration/TIC120517801/: v1 and v2 files, with UTC-fix derivatives generated now (prereg_utc_fix.py; originals unchanged).
    - Clock priors 120517801.json published; clock addenda rows unmasked.
    - Tables and 2026-10-20 reviews restored from the local originals (mask-only differences).
    - Round-1 prior search restored to its v1.11 content with the TIC named, plus a dated note; round-2 sweep unmasked.
    - external_review_allsky/REVIEW.md restored, including section 4, with historical labels.
    - The public decision log no longer masks the TIC.
    - README/REPORT paragraph to follow. A short reviewer check comes before release.
109. 2026-10-20 — Review of staged v1.14 (results/REVIEW_v1.14_TIC120517801.md: fixes needed; all numerical checks passed - hashes,
    refits, UTC derivatives, clock propagation, restoration fidelity, the 29-file manifest, 56 prior CSVs unchanged). Fixes:
    - CORRECTION to the decision log around item 36 and to the REPORT: "the v1 test would have failed a real signal" is overstated. v2 is
      27.4-30.9 min later than v1 over S111-S113, all inside the written v1 3-sigma windows; the historical 22-45-min range is not that
      comparison. Dated correction appended to REPORT and the v2 registration, and folded into the review erratum.
    - Restored review section 4 erratum: Giacalone "likely planet" needs NFPP < 0.001 (not 0.1), so FPP 0.088 / NFPP 0.062 meets neither
      category; the Gaia RV summary gives no companion exclusion or mass bound.
    - Public qlp_clock_v2/shifts.csv: the object's 24 rows restored (public = local minus those rows before).
    - Provenance paragraph (8-character prefixes in commit 24cd0de and the v1.3 Zenodo zip created 23:24:53 UTC; prefixes do not
      authenticate full bytes; the published dataset v1 had exposed v1 ephemeris values under a masked label; freeze times attested) added
      to the README and both registrations; VERDICTS "never in public copies" annotated.
    - 4.2" = about 0.20 TESS pixel (current prose); "our TESS analyses do not assign the eclipse to either star".
110. 2026-10-20 — Final re-check (results/REVIEW_v1.14_final_recheck.md): ready to publish v1.14, all five findings resolved. Author: "go".
111. 2026-10-20 — v1.14 PUBLISHED: GitHub 87984af, release v1.14 (no session link); Zenodo 10.5281/zenodo.23516414 (automatic). TIC 120517801 is now public (likely blend, host
    unresolved, independent rediscovery; S111-S113 ephemeris test, scoring procedure to be stated before those data are examined).
112. 2026-10-20 — ROUND 4 (user: "go 1"): mine the rest of the completed all-sky QLP run (57,835 stars). Pool definition, fixed before
    any processing: from results/allsky_testable_soon.csv (SDE >= 9), minus everything taken into rounds 1-3; clean, no known source,
    odd/even and secondary < 3 sigma, no period-cluster or shared-time flag, depth <= 5 ppt. Round 3 used the same filters but only next
    sector S106-S111. The "transits in next-sector windows" filter is NOT applied, because orbit windows beyond S111 are approximate.
    - Primary: next sector S112-S120 (results/allsky_round4_primary.csv); freeze before those sectors are observed (S112 starts about
      2026-12-22).
    - Secondary: S121-S134 (allsky_round4_secondary.csv).
    - Ground-only subset deferred unless depth >= 1.5 ppt and SDE >= 12 (allsky_round4_ground.csv).
    Expectation from round 3 (190 -> 84 on target -> 7 pass / 8 weak -> 1 candidate, 3 marginal, 5 credited rediscoveries): about 1-3
    new candidates.
    Order: refreshed prior-report grep FIRST; then pixel tests (runner refuses the seven S106 TICs and any cutout sector >= 106); then
    vet.py with the v1.13 fixes (not comparable to the round 2-3 exploratory values); then triage_round3.py unchanged; then TRICERATOPS
    with the corrected wording; then a prompt freeze with the template checked; then external review before release.
113. 2026-10-20 — Round 4 step 2 (prior-report check, before pixel tests). Corpus refreshed 2026-10-20 (results/prior_search_round4/data/
    20261020/: shallow clones of eumemic/exoplanets, ahrazzle/exoplanets, brahle/exoplanet-candidates, alejandrozarco/tess-candidates-2026,
    killercatfish/tess-hunt, samsonmaximus/tess-three-candidates, paraschopra/tess-planet-candidates; ExoFOP TOI 8,151 / CTOI 5,138 rows),
    plus the round 1-2 corpora. A bare TIC match is meaningless: the corpora hold target lists and our own published tables. So a hit
    counts only with a period (or half/twice) quoted to >= 3 decimals within 0.1 % and 200 characters of the TIC; our own Zenodo
    records (all 29 ids under the ORCID) and neighbour lists are excluded. Result: 29 of 303 have external period-matched mentions
    (eumemic/ahrazzle 10, brahle 4, others), tagged as likely rediscoveries but kept; results/allsky_round4_prior.csv.
    Step 3 launched: pixel tests on the 182 primary signals (two queues; results/allsky_round4_pixel_q{1,2}.csv). ffi_pixel_test.py now
    refuses the seven S106 test TICs and any sector >= 106 (tested on both cases).
114. 2026-10-21 — Round 4 pixel tests (pixel_collect.py, same thresholds as rounds 2-3: ON <= 0.5 px in all sectors, OFF >= 0.9 px):
    182 -> ON_TARGET 27, OFF_TARGET 85, AMBIGUOUS 52, no 200-s sector 11, no data 7 (results/allsky_round4_pixel.csv). Shared-period
    pairs among the on-target list (likely one source in neighbouring stars): 121201412/121201410 (1.13430 d), 276903941/331634064
    (12.857 d). Step 4: vet.py (v1.13 fixes) on the 27, three in parallel.
115. 2026-10-21 — Round 4 step 4-5. vet.py (v1.13) finished on all 27 on-target signals (logs/round4_vet.log, 01:06 UTC). Triage with
    scripts/triage_round4.py = triage_round3.py with round-4 file paths only (diff checked; thresholds unchanged):
    PASS 2, WEAK 2, FAIL 23 (results/allsky_round4_triage.csv). Survivors: 343298093 (P 0.766 d, SNR 9.1, PASS, no prior report),
    188664994 (P 3.782 d, SNR 13.1, PASS), 195343302 (P 1.185 d, SNR 7.6, WEAK, density ratio 0.37), 151767028 (P 2.210 d, SNR 8.1,
    WEAK; period-matched in eumemic/ahrazzle followup_kmdwarfs.csv -> likely rediscovery). Both shared-period pairs FAIL (121201412/410,
    276903941/331634064). The "catalog" prior tag on 188664994 is a false match: the 3.7824 value lies in the neighbouring row of
    Nigraha period_info-sec23.csv (TIC 207439389); Nigraha's own BLS periods for 188664994 are 4.25/10.0/11.9/12.4/13.2 d; prior_grep.py
    gives 0 hits. No ExoFOP TOI/CTOI rows for any survivor. TRICERATOPS launched on the four (scripts/tri_runner_round4.sh, in-sample
    local sectors only).
116. 2026-10-21 — Round 4 TRICERATOPS (single run each, scripts/triceratops_qlp.py in .venv_tri, last 3 local in-sample QLP sectors,
    no contrast curve; screening only, not validation): 343298093 FPP 0.065 NFPP 0.0010 (S101-103); 188664994 FPP 0.081 NFPP 0.0078
    (S80,81,84); 195343302 FPP 0.156 NFPP 0.111 (S55,56,83); 151767028 FPP 0.113 NFPP 0.043 (S90,99,100). None meets the Giacalone+2021
    validation threshold (FPP < 0.015 and NFPP < 0.001); all are FPP < 0.5. 195343302's NFPP (0.11) means a nearby-star origin is not
    excluded. Awaiting the author's cap on how many go to pre-registration.
117. 2026-10-21 — Author's go: "Do the 3" -> pre-register 343298093, 188664994, 151767028 (cap 3; 195343302 held back, NFPP 0.11).
    Before freezing, three dated script changes (local; to be reviewed before any release):
    (a) BUG FOUND in scripts/prereg_v2.py (present since the item-69 change, published in v1.10-v1.14): the prediction horizon
        `if jd >= 2461406.5` stops at 2027-01-01, not 2027-12-31 as its comment and item 69 say. Fixed to JD 2461771.5 (2028-01-01).
        Affected frozen record: 162304222 v3 (frozen 2026-10-20 02:03 UTC) lists S111 and S112 only to 2026-12-31; S112 after that date,
        S113 and S114 have no predictions. Freezes made before item 69 used the older loop (range(1,400), JD 2461900) and are unaffected
        by this bug. Also found: 53825235 never received the v3 that item 68 said was needed (its v2 has no future predictions; S108-S109
        are now past). Both to be reported to the author; no record changed.
    (b) prereg_v2.py outcome template: removed "or a TESScut fixed-aperture extraction" (fallback withdrawn 2026-10-20, conformance v2.1).
    (c) scripts/qlp_clock_v2.py: optional argv[2] = explicit ephemeris JSON (e.g. the prereg_v2 dry run), because since v1.12 dry runs go to
        _dryrun/ and first-time freezes had no ephemeris for the clock step. Only the uncorrected per-sector times are used, as in round 3.
    Orbit table checked: tess.mit.edu TESS_orbit_times.csv regenerated 2026-10-20 is identical to ours (ends S111); S112+ windows are
    "span only, gap unknown".
118. 2026-10-21 01:57 UTC — Round-4 freezes (local, not published): scripts/freeze_round4.sh (prereg_v2.py v2 with the item-117 fixes).
    - 151767028 v2: P 2.210401 +- 0.000012 d, T0 BTJD 4056.10895 +- 6.6 min; S36/S63/S90/S99 (S100 rejected, weak); --clock (S99 -0.00 min);
      tests S112-S114 (38 predictions, sigma <= 9.1 min); ref 540 ppm / 1.00 h; CSV SHA befcc2e8...; credited as independent rediscovery
      (eumemic/ahrazzle followup_kmdwarfs.csv).
    - 343298093 v2: P 0.766143 +- 0.000007 d, T0 BTJD 4164.67665 +- 2.6 min; 7 QLP sector times; --clock (S100-S103: 0.93/3.14/1.82/3.67
      min); tests S113-S114 (74 predictions, sigma <= 5.3 min); ref 302 ppm / 1.10 h; CSV SHA 4f14d1fe...
    - 188664994 v2: P 3.781806 +- 0.000021 d, T0 BTJD 3597.39365 +- 8.2 min; 17 sector times (S26 excluded: corrupted QLP and SPOC light
      curves, numbers in the frozen text); chi2/dof 201/15, inflation x3.66 (timing scatter flagged in the text); tests S117-S119 (21
      predictions, sigma <= 15.4 min); S122-S132 not listed (no published dates; TESS_sector_dates_future.csv ends at S121) -> a later
      version once dates exist; ref 412 ppm / 1.80 h; CSV SHA 0d450700...
    Each text carries a scoring statement: conformance v2.1 rc4 (SHA a864b07a...) general rules, per-object config locked before the
    sector is examined, QLP SAP_FLUX v01, clock gate, sectors scored separately in order, first released sector = test of record,
    no TESScut; calibration only exists for the S106 objects. Clock records results/qlp_clock_v2/{151767028,343298093}.json were made
    from the dry-run ephemerides (item 117c). Next: external review before any release (v1.15); publish only on the author's go.
119. 2026-10-21 — Follow-up to 117a: item 68's third object, 408110117, is NOT truncated: its v2 CSV lists all 10 S108 transits
    (2026-09-09 to 2026-10-03; S108 runs 2026-09-07 to 10-04), labelled "retrodiction: before freeze, untested" because S108 was observed
    before the 2026-10-20 freeze. So of item 68's three objects: 408110117 covered; 162304222 v3 truncated by the horizon bug (S112
    partial, S113-S114 missing); 53825235 has no future predictions and no v3. public_release/ working tree checked clean (git status
    empty): no published file was changed by items 115-118.
120. 2026-10-21 — Independent review of round 4 (results/REVIEW_round4_freezes.md): "include after listed fixes". Findings F1-F9 checked by us:
    F1 confirmed (343298093 is in eumemic vetted_signals.csv.gz, P 0.7661376546 d, flagged "inconsistent transit SNRs", and in
    all_signals.csv.gz; not in their candidate lists; our search never decompressed .gz tables). F3 confirmed (115692561 v2 S106 list
    ends at epoch 3417; 3418-3419 are in S106 and S107 is absent; old 399-epoch cap; 3367979 v2 ground list also truncated). Corrects
    items 115, 118 ("no prior report" for 343298093) and 117a/119 (the horizon audit was incomplete; item 117a's "unaffected" was true
    only of the newer end-date bug).
    Author's decisions (2026-10-21): (1) 115692561 S106 is scored on the frozen list as published, omission disclosed, no supplement;
    (2) primary-sector rule adopted (S112 / S113 / S117 are the tests of record and stay so whatever their result; later sectors are
    separate tests); (3) new versions for 162304222, 53825235, 3367979; (4) 343298093 kept among the three as an independent rediscovery.
121. 2026-10-21 — Fixes applied (local; nothing published):
    - scripts/prior_match.py: row/field-aware matcher (CSV, CSV.gz, tables in .zip; TIC and named period field in the same record;
      P, P/2, 2P within 0.1 %; own records and neighbour/cone files excluded; provenance per record). Run on all 67 registered and
      round-4 objects over results/prior_search*/ -> results/prior_match_20261021.csv (+ _text.csv). Separately, candidate folder
      names TIC<id>_P<period> (eumemic/ahrazzle) were matched: hits only for objects already credited as rediscoveries (317134140,
      120444365, 120517801, 115692561, 19119739, 3367979, 65575657, 366047768, 383617106, 333735955); none for 183374279, 61310956,
      89247735, 80387959.
    - results/qlp_clock_v2/188664994.json: c0 prior from control sectors S84/S81 (+0.032 min).
    - scripts/make_conformance_configs_round4.py -> 8 locked configs configs/conformance/{151767028_S112-S114, 343298093_S113-S114,
      188664994_S117-S119}.json (primary flag, primary rule, clock prior hash, evaluator SHA a864b07a..., future-data status). The seven
      S106 configs are untouched. scripts/test_round4_configs.py: 56/56 refusal/config checks pass using in-sample files only
      (logs/test_round4_configs_20261021.log).
    - Dated amendments appended to the three round-4 registrations (343298093 priority correction and NFPP 0.00097; 151767028 RAVEN
      nsfp09 credit; 188664994 timing-uncertainty caveat, reference-depth provenance 412 vs 420 +- 43 ppm without S26, 239-614 ppm range,
      S117-S119 coverage; all three: primary-sector rule, config hashes, TESScut TIME/TIMECORR clock exception, generic paragraph secondary).
    - New versions (scripts/freeze_horizon_fix.sh; ephemerides reproduced exactly by dry runs, overlapping rows identical):
      162304222 v4 (CSV b4a26083...), 53825235 v3 (1408a7cd...; S108 and early S109 labelled retrodictions), 3367979 v3 (0e8f5ea1...).
      The template wrongly wrote "First freeze for this object" / "v4 supersedes v2": dated corrections appended; template fixed.
    - results/ERRATUM_PREDICTION_HORIZON_2026-10-21.md (two bugs, five records, handling as decided). STATUS corrected (v1.14 current
      release; local vs public freezes; 343298093 and 151767028 credits).
122. 2026-10-21 — Row-aware matcher results (results/prior_match_20261021.csv; 9,246 TIC records, 7,025 period matches across mirrored
    corpora) and a primary-source check of RAVEN (Lafarga et al. 2026, MNRAS, arXiv 2603.22597; Zenodo 19661443 downloaded 2026-10-21 to
    results/prior_search_round4/data/20261021_raven/). Earlier machine detections missed by our searches:
    - TIC 80387959 (published as "no human-reported candidate"; preprint v1.3 says "no catalogued periodic signal"): RAVEN first-stage
      nsfp09 candidate at P = 4.19222 d (prob_NSFP 0.98) plus a P/3 alias; NOT in RAVEN's vetted/validated tables. The preprint sentence is
      false and needs a new version; README/REPORT need qualification.
    - TIC 249813122 (README: prior "none"): RAVEN nsfp09 P = 4.17453 d. TIC 333661705 (brahle credit): also RAVEN. 151767028: also RAVEN.
    - Round-3 table "none found": 122522485, 159033763, 162304222 appear in eumemic all_signals.csv.gz (public raw BLS output) at our
      period; 196514928 and 283913390 appear in eumemic's false_alarm_classifier_table as label "real", class "offset".
    - No earlier detection for 183374279, 61310956, 89247735, 188664994, 195343302 and 14 others (bounded search).
    Draft: results/ERRATUM_PRIOR_DETECTIONS_2026-10-21_DRAFT.md. Awaiting the author before any public correction.
123. 2026-10-21 — Re-check (results/REVIEW_round4_recheck.md): "No" until R1-R5. Fixes (local; nothing published):
    - R1: item 121 and the erratum wrongly said 3367979 v3's 399 shared rows were identical: v3 omitted --ground, so its sector labels
      changed and its text kept TESS clauses. Corrected; dated superseded notice appended to v3. 3367979 v4 frozen 2026-10-21 03:40:48
      UTC with --ground --ground-mmag 0.6 (CSV b6c94c8e...; same ephemeris; all 399 shared rows identical in every field; 0.6 mmag per
      10-min bin = SNR 4 per transit at 788 ppm / 1.30 h). prereg_v2.py gained --ground-mmag (the ground clause was a fixed 1.5 mmag).
    - R2: prior_match.py now recognises pipeline-prefixed period columns (bls_per, juliet_per, tls_period, ...), excludes uncertainty
      columns, records label/cls/prob fields and lists TIC-bearing tables without a period column as UNRESOLVED (*_unresolved.csv).
      Regression tests scripts/test_prior_match.py (primary RAVEN tables, neighbouring-row case, gzip, unresolved): pass
      (logs/test_prior_match_20261021.log). Full re-run -> results/prior_match_20261021b.csv.
    - R3: configs/conformance/ROUND4_LOCK.json (SHA-256 of the 8 configs and their c0 priors; manifest SHA d7a20a59...);
      scripts/validate_round4_inputs.py binds config, prediction CSV, evaluator and c0 prior before data access, the clock record to
      that config and prior, and the evaluator output to that config and light curve. The pinned evaluator and clock tool are unchanged
      (S106 tests keep their published code). scripts/test_round4_configs.py rewritten (fresh directory, required exit status, outputs
      bound to their case; adds tampered prior bytes/path/hash and stale clock/result cases): 144/144 pass
      (logs/test_round4_configs_20261021b.log). Dated note appended to the three round-4 registrations making the validator required.
    - R4: the "first human(-vetted)" wording is withdrawn for 80387959; the reviewer's replacement text is adopted in the prior-detections
      erratum and STATUS; the public-correction table now lists README, REPORT, prior_search/VERDICTS.md, the preprint, both outcome
      tables and a dated correction file for the DDT proposal (sending anything to the DDT office is the author's decision). RAVEN dates
      stated as paper 2026-03-23 / Zenodo displayed 2026-03-25, created 2026-04-20. 151767028: primary RAVEN confirmation appended.
    - R5: prereg_v2.py writes one introduction chosen from the requested version and the records that exist ("vN supersedes vK" with
      K = the latest earlier record; refuses --version > 2 without one).
    Integrity: all 50 frozen prediction CSVs match their JSON and registration hashes; the seven S106 configs equal their v2.1 public copies.
124. 2026-10-21 — Full matcher re-run with the R2 fixes (results/prior_match_20261021b.csv; 9,258 TIC records, 7,029 period matches):
    the same 25 objects match as before, now including the primary RAVEN tables directly (bls_per). No match for 183374279, 61310956,
    89247735, 188664994 or 195343302. 86 TIC-bearing tables without a period column are listed in results/prior_match_20261021b_unresolved.csv;
    for the first-report objects and the round-4 three, the only such hits are Nigraha tic2file-sec*.csv light-curve index tables
    (188664994: S17/S23/S24/S26; 61310956: S22), which are file lists, not reports. The prior-detections erratum is unchanged by the re-run.
125. 2026-10-21 — Second re-check (results/REVIEW_round4_recheck2.md): "No" until the clock-record binding and the correction inventory
    are fixed. Fixes (local; nothing published):
    - validate_round4_inputs.py result stage now requires the evaluator output's clock_record.sha256 to equal the SHA-256 of the clock file
      given, and every hash (config, evaluator, light curve, clock record; clock-stage prior/prediction/light-curve) to be present and a
      well-formed SHA-256 (fail closed). An output without clock provenance is accepted only as a PRE-CLOCK outcome (INVALID_INPUT,
      INSUFFICIENT, CLOCK_UNVERIFIED), never as clock-dependent scoring. test_round4_configs.py: positive fixture now a genuinely bound
      scored output; new refusal cases (other clock file with identical identity fields but other corrections, science outcome without
      clock provenance, missing/malformed hashes, other evaluator/config; clock record without light-curve hash); 200/200 pass
      (logs/test_round4_configs_20261021c.log). Addendum appended to the three round-4 registrations.
    - Prior-detections erratum: points to the corrected matcher run (20261021b); the correction inventory now covers every local copy found
      by a text search: repository README/REPORT/VERDICTS/PRIOR_SEARCH and both outcome tables; the preprint; BOTH dataset versions
      (v1.0 and the published v1.1, which the review did not list: README, REPORT, VERDICTS, PRIOR_SEARCH, documents/note.tex); local
      working copies.
    - 3367979 v4: dated clarification of the precision arithmetic (0.597 mmag; ideal SNR 3.98 at 0.6 mmag, 1.6 at 1.5 mmag).
    - prereg_v2.py: the no-predecessor refusal for --version > 2 now runs before any data access or write (tested on 195343302: refused,
      no file written).
    Hash inventory, defined: 50 v2+ prediction CSVs under results/vet*/ match their final_ephemeris_v*.json hashes (the review's 46 are the
    generator-produced registrations with CSV/JSON/Markdown; its 55 add v1 and other records). Seven S106 configs equal their published
    copies; public_release/ unchanged.
126. 2026-10-21 — Third re-check (results/REVIEW_round4_recheck3.md): "Yes — ready to include in v1.15 within the requested review
    scope". It approves the corrections for release assembly, not an assembled release (which does not yet exist): the dated-notice plan in
    the prior-detections erratum must be carried out, not the old claims re-exported. Operational note from the review, adopted: the
    validator's result stage needs a clock file even for pre-clock outcomes, so an early INSUFFICIENT/INVALID_INPUT without a clock record
    is refused (exit 2); such a refusal and the evaluator's original early outcome are reported as they are, and no clock record is ever
    fabricated to obtain BOUND. Next: assemble v1.15 + preprint v1.4 + dataset v1.2 + DDT correction file, final re-check of the
    assembled release, then the author's go to publish.
127. 2026-10-21 — Author's go: assemble v1.15 + preprint v1.4 + dataset v1.2 + DDT correction (nothing published yet).
    - Dated pointer notes appended to 162304222 v3, 53825235 v2, 115692561 v2 (omission disclosed; S106 test stays the frozen list),
      3367979 v2 (generated without --ground; list truncated).
    - public_release/ (uncommitted): preregistration/TIC151767028, TIC343298093, TIC188664994 (+ qlp_clock_v2 priors), TIC3367979 (v2-v4;
      frozen 2026-10-19 but not published before), 162304222 v4, 53825235 v3, updated notes; preregistration/ERRATUM_PREDICTION_HORIZON_
      2026-10-21.md; prior_search/ERRATUM_PRIOR_DETECTIONS_2026-10-21.md (final); conformance_round4/ (8 configs, lock, validator, config
      maker, tests + log, README); tables/round4/ (pool, pixel, triage, old prior table, matcher runs and targets);
      tables/NOTICE_PRIOR_REPORTS_2026-10-21.md; corrections/DDT_PROPOSAL_80387959_CORRECTION_2026-10-21.md (also ddt_80387959/);
      reviews_round4/ (review, three re-checks, prompts); scripts updated/added; dated correction prepended to prior_search/VERDICTS.md and
      PRIOR_SEARCH.md; README (date line, 80387959 paragraph and prior-report bullet, 249813122 row, 3367979 note, round-3 notes, new
      round-4 and corrections block, Reproduce, Related Zenodo records); REPORT correction 9 and marker; CITATION 1.15; MANIFEST_v1.15.md.
      The empty stray directory "preregistration/TIC122522485 206620592 ..." (untracked, never published) was removed.
      conformance_v2.1/scripts/qlp_clock_v2.py is kept as hashed in that bundle (README says so). Checks: no previously public prediction
      CSV changed; registrations append-only, VERDICTS/PRIOR_SEARCH prepend-only; no session links, secrets or e-mail addresses.
    - Preprint v1.4: note_allsky/note.tex (v1.3 kept as note_v1.3.tex/.pdf) - prior-report paragraph replaced by the reviewed RAVEN
      wording; tectonic, 2 pages; zenodo_upload/preprint_v1.4/ (md5 f8b44ce904036c58c877b08dc0e9378c).
    - Dataset v1.2: dataset_v1.2/ = v1.1 + v1.2 README notice, REPORT notice and markers, dated corrections in VERDICTS/PRIOR_SEARCH,
      preprint v1.4 in documents/, the erratum; checksums regenerated (211 files; only the declared files differ from v1.1);
      zenodo_upload/supporting_data_and_code_v1.2.zip (213 entries, md5 fbf0fe5df994e42062023855068853e1 after the line-number label fix; checksums verify after unzip; scan clean).
    Next: final re-check of the assembled release, then the author's go to publish.
128. 2026-10-21 — Before the final check: (1) tables/round4/README.md marks allsky_round4_prior.csv as superseded (DECISIONS 113 inline
    check; false 188664994 tag, missed 343298093). (2) Scan for this session's scratchpad paths: none in any new v1.15 file; already
    published reviews from v1.10-v1.11 (conformance_v2.1/reviews/, reviews_2026-10-20/) and scripts/download_lcs.sh contain local
    /tmp/claude-501/... paths with a session transcript id (not a session URL); left as published, reported to the author. (3) Publication
    texts drafted for review: zenodo_upload/RELEASE_NOTES_v1.15.md, zenodo_upload/ZENODO_DESCRIPTIONS_2026-10-21.md, and
    zenodo_upload/preprint_v1.4/description_v1.4.html. The preprint's Zenodo description (all versions) repeats "no human-reported
    candidate", so v1.4 REPLACES the description (scripts/zenodo_newversion_staged.py gained "REPLACE:<file>"); earlier versions of the
    preprint (23462434, 23462857, 23463582, 23512950) and dataset (23462438, 23512928) get a dated prepended notice. Erratum line numbers
    labelled as v1.14 line numbers (all three copies); dataset v1.2 checksums and zip rebuilt.
129. 2026-10-21 — Assembled-release review (results/REVIEW_v1.15_assembled.md): "No-go" for three documentation fixes; all numerical
    artifacts, manifest, frozen records, dataset checksums/ZIP and the compiled preprint pass. Fixed: (1) the dataset v1.2 Zenodo note
    now lists every changed file (README, REPORT, both prior-search files, note.tex/pdf, erratum, checksum lists) instead of "all other
    files identical"; (2) the preprint v1.4 replacement description no longer says "blind holdout years" or "all code and data are public"
    in its summary (retrospective leave-one-year-out consistency checks; repository scope and Reproduce limits), with a "Version history"
    label; (3) README round-4 block lists the five truncated records (162304222 v2 and v3). Reviewer's judgment on DECISIONS 128(2): leave
    the already-published scratchpad paths as published. Manifest and public DECISIONS regenerated.
130. 2026-10-21 — PUBLISHED after the assembled-release re-check (results/REVIEW_v1.15_assembled_recheck.md: yes) and the author's go,
    in the reviewed order: (1) preprint v1.4 10.5281/zenodo.23535541 (description replaced by the reviewed text, verified identical in
    the draft; PDF md5 f8b44ce9...) and dataset v1.2 10.5281/zenodo.23535544 (v1.1 description + reviewed note, verified; zip md5
    fbf0fe5d...); (2) GitHub commit 9a17efc, tag and release v1.15 (no session link; release notes + the two new DOIs), archived
    automatically as Zenodo 10.5281/zenodo.23535575; (3) dated correction notice prepended to the descriptions of preprint v1.0-v1.3
    (23462434, 23462857, 23463582, 23512950) and dataset v1.0-v1.1 (23462438, 23512928); each grew by exactly the notice; public API
    check confirms all eight records. A first draft attempt failed with a TLS hostname error before any request was sent (nothing
    created); the retry succeeded. The Zenodo token used is the one from 2026-10-18, so it has not been revoked yet.
131. 2026-10-21 — ROUND 5 declared (author: "do first 1 and then 4"), before any round-5 processing. Pool: the 104 round-4 SECONDARY
    signals (results/allsky_round4_secondary.csv; next TESS sector S121 25, S122 18, S123 19, S124 16, S125 8, S126 2, S127 1, S128 3,
    S132 1, S134 11), selected by the item-112 filters; none is registered, protected or in the round-4 primary pool. Procedure = round 4
    unchanged, with the review lessons applied:
    1. Prior-report check FIRST with scripts/prior_match.py (row-aware, CSV.gz/zip, P/2-P-2P within 0.1 %), on a corpus refreshed
       today (eumemic, ahrazzle, brahle and the other round-4 repositories; ExoFOP TOI/CTOI exports) plus the primary RAVEN tables
       (Zenodo 19661443) and the earlier corpora; plus the TIC<id>_P<period> folder-name check. Matches are credited, not dropped.
    2. Pixel test (ffi_pixel_test.py via pixel_runner2.sh; in-sample sectors only; guard refuses S106+ and the protected TICs);
       classification by pixel_collect.py (ON <= 0.5 px all sectors, OFF >= 0.9 px).
    3. vet.py (v1.13) on ON_TARGET; triage with the round-3 thresholds (a path-only copy, as triage_round4.py); data-quality check of every
       sector used (round-4 lesson: 188664994 S26).
    4. TRICERATOPS (single run, screening only) on survivors; the author sets the cap before freezing.
    5. Freeze with prereg_v2.py (current version), configs + lock + validator as conformance_round4, before each primary sector is
       observed (S121 starts about 2027-08-23; dated windows exist only to S121, so later sectors are listed when dates are published).
    6. External review of the results before any release (prompt prepared at the end).
132. 2026-10-21 — Round 5 started: corpus refreshed (results/prior_search_round5/data/20261021/: 8 GitHub repositories, shallow clones;
    ExoFOP was down for maintenance - its export returned an HTML maintenance page, deleted - so the NASA Exoplanet Archive TOI table
    (8,151 rows) is used, with the 2026-10-20 ExoFOP CTOI snapshot); prior_match.py launched on the 104 (results/prior_match_round5.csv);
    pixel tests launched (two queues, results/allsky_round5_pixel_q{1,2}.csv).
    Round 6 (author's option 4, "fainter M dwarfs, Tmag 11.5-13"): a documentation-only scoping check found that range already covered by
    eumemic/exoplanets (4.04 million FGKM dwarfs, T < 13.5, Sectors 1-104, raw detections public) and RAVEN (2.2 million stars,
    Sectors 1-55, P 0.5-16 d). Draft design results/DESIGN_round6_faint_M_dwarfs_DRAFT.md proposes 13.5 < T <= 16 M dwarfs within 100 pc
    with TESS-SPOC/TGLC light curves; it needs the author's approval and a design review (results/PROMPT_review_round6_design.txt) before
    any download. Round-5 results review prompt prepared: results/PROMPT_review_round5_results.txt (to send when round 5 is complete).
133. 2026-10-21 — Round 5 prior check and pixel tests done. prior_match.py (results/prior_match_round5.csv; 5,168 TIC records, 2,511 period
    matches across mirrored corpora): 10 of the 104 have a period-matched record somewhere (240488148, 240782253, 240910173, 252636793,
    346079633, 372186355, 372343190, 427279177, 446131714, 743411589); each will be classified by source type (candidate list, raw search
    output, classifier table, TCE/vetting table, RAVEN) only for survivors. Pixel tests (pixel_collect.py, unchanged thresholds): 104 ->
    ON_TARGET 21, OFF_TARGET 54, AMBIGUOUS 19, no 200-s sector 8, no data 2 (results/allsky_round5_pixel.csv). No shared-period pair among
    the 21. Eight of the 21 have P 12.4-18.4 d and depths 1.3-2.2 ppt, a pattern typical of orbit-period systematics; triage decides.
    vet.py launched on the 21 (results/allsky_round5_vetlist.csv; logs/round5_vet.log).
134. 2026-10-22 — Round 5 vetting and triage. vet.py on the 21 (logs/round5_vet.log, all exit 0). scripts/triage_round5.py = triage_round3.py
    with round-5 paths only (diff checked): PASS 2, WEAK 1, FAIL 18 (results/allsky_round5_triage.csv; main fail reasons: inverted-null
    margin 12, SNR 10, density 9). Survivors:
    - 240488148: P 1.512529 d, ~440 ppm SAP, SNR 13.3, 1.4 R_E, 3/3 years; next S121. Independent rediscovery: eumemic/ahrazzle tier-B
      candidate (results_public/candidates_allsky.csv, P 1.512519 d; their classifier label "real", class "clean"). S82 somewhat noisier
      (6-h range 1.17 % vs ~0.35 %), not corrupt; kept.
    - 372343190: P 1.202779 d, ~250 ppm, SNR 8.8 (WEAK), density ratio 0.63, 3/4 years; next S122. Only earlier record: Nigraha's raw
      per-sector BLS table (period_info-sec17.csv, P = 0.60108 d = P/2) - a raw machine output, not a candidate report. Sectors uniform.
    - 13450993: P 14.591174 d, ~2.5-2.8 ppt, 4.2 R_E, SNR 9.4; next S124; no earlier record. WEAK EVIDENCE despite PASS: one transit per
      sector (S18, S58, S85, S86); the 2019 event has 4 in-transit points (30-min cadence), 2022 is not detected (SNR 1.1), 2024 carries
      the signal; odd/even depths 892 vs 2851 ppm (passes only through large errors). The period is poorly constrained (aliases possible).
    TRICERATOPS running (scripts/tri_runner_round5.sh).
135. 2026-10-22 — Round 5 TRICERATOPS (single run each, screening only, last 3 local in-sample sectors): 240488148 FPP 0.101 / NFPP 0.037
    (S56, S82, S83); 372343190 FPP 0.678 / NFPP 0.656 (S84-S86; folded depth used 151 ppm); 13450993 FPP 0.611 / NFPP 0.478 (S58, S85, S86;
    folded depth used 105 ppm, far below the 2.5-2.8 ppt event depth - the fold over single-event sectors dilutes it). 372343190 and
    13450993 exceed FPP 0.5 (a nearby or eclipsing-binary origin is more likely than a planet). Only 240488148 remains plausible; it is an
    independent rediscovery. Awaiting the author's cap.
136. 2026-10-22 — CORRECTION to item 134 and freeze PAUSED. The author answered "Freeze" (TIC 240488148). Before running prereg_v2.py,
    the prior-match rows for 240488148 were re-read. Row 1 of results/prior_match_round5.csv (PERIOD_MATCH, rel. diff 7e-6) is
    results/prior_search/data/github_sweep/advaitpaliwal__TIC240488148/data/search/autovet.csv: a repository dedicated to this
    star (in our corpus since the 2026-10-18 sweep), which item 134 and our report to the author left out. Item 134 credited only the
    eumemic/ahrazzle tier-B list.
    The repository (github.com/advaitpaliwal/TIC240488148; read-only GitHub API check 2026-10-22, last commit b919f1b 2026-10-12) is a
    human-vetted candidate report:
    - discovered 2026-10-08, released 2026-10-09 (CITATION.cff v1.0);
    - P 1.5125149 +- 0.0000029 d, T0 BJD_TDB 2460393.34348, 411 ppm, 1.41 h, 1.37 R_E;
    - six TESS-SPOC sectors plus QLP, six-sector difference-image localisation;
    - TRICERATOPS + MOLUSC FPP 0.020-0.024;
    - an RNAAS research note in editorial revision (revision1/response.txt);
    - a public ephemeris through 2027-12-31 at about 4-5 min, so it covers S121;
    - a prepared but not uploaded ExoFOP CTOI row.
    It is not in the 2026-10-20 ExoFOP CTOI/TOI snapshots or the 2026-10-21 NASA TOI table. Our P (1.512518 d) is the same signal.
    The matcher found the record; the source-type classification promised in item 133 was not done row by row. Same class of error as
    the 343298093 and 80387959 misses. The round-5 refresh (8 repositories) did not re-clone this repository; the older copy was still
    scanned. Nothing was frozen, downloaded or published. The question goes back to the author: freeze as a replication test of our
    pipeline's ephemeris, crediting Paliwal as discoverer, or close round 5 with no freeze. Round-5 review prompt updated to state the miss.
137. 2026-10-22 — Round-5 results review (results/REVIEW_round5_results.md): "Include after listed fixes; no freeze or release approval".
    Findings re-checked by us before acting. R5-1 confirmed:
    - moosesteve21/PlanetCandidates/TIC240488148/README.md reports the same star, found 2026-10-12, P 1.5125120 d;
    - it was already in our corpus (prior_search_round2 sweep).
    R5-2 confirmed and wider than reported. scripts/triceratops_qlp.py (public since v1.12) folds every cached QLP file of the TIC, but
    records only the three aperture sectors. Audit: results/triceratops_qlp_sector_audit_20261022.json. It lists the files present at run
    time that passed the 1000-point cut. Photometry != recorded list for 8 of the 15 runs:
    - 151767028 (+S36, S63)
    - 160330868 (+S32)
    - 183374279 (+S2, S29, S69)
    - 188664994 (+12 sectors S20-S73; S26 not among them)
    - 196514928 (+S34)
    - 343298093 (+S13, S39, S66, S93, S100)
    - 372343190 (+S52, S57, S58)
    - 61310956 (photometry S45, S46, S72; S22 aperture only)
    No run used a sector >= 106. Several of these values appear in published records (rounds 3-4, v1.15).
    R5-3, R5-4, R5-9 confirmed from report.json (13450993: global real-top P 16.867 d, not the 14.591 d candidate).
    R5-5 confirmed and wider. Re-classification of rounds 2-5 with scripts/pixel_collect_v2.py (outputs results/*_pixel_v2.csv; v1
    tables unchanged): 40 ON_TARGET objects become AMBIGUOUS_INCOMPLETE (a NaN or failed sector). 321980862 (round 3, 0.5028 px) and
    389029596 (round 5, 0.8970 px) change class through rounding. Four FROZEN objects were ON_TARGET with one non-finite sector: 91617711
    (S71), 253931796 (S68), 160330868 (S98), 188664994 (S80). Their on-target label rests on 1-2 finite sectors. Their frozen predictions
    are unaffected; the published wording needs a qualification.
    Author's decisions (2026-10-22): (1) ROUND 5 CLOSED WITH NO FREEZE. 240488148 is a recovery of a previously reported candidate
    (eumemic/ahrazzle P 1.512519 d; Advait Paliwal P 1.5125149 d, report 2026-10-09; moosesteve21 P 1.5125120 d, found 2026-10-12;
    our refined P 1.5125181513 d). We claim no first discovery or validation. 372343190 and 13450993 stay unregistered (weak / not
    resolved). (2) Go for the fixes (item 138).
    Corrections to item 134/135, adopting the review's wording:
    - periods are the refined 1.512518 d / 1.202785 d (1.512529 was the initial search value);
    - Nigraha's record is a raw per-sector TLS search output, not BLS;
    - 13450993 has sparse usable events and NO retained in-transit S85 points (not "one transit per sector");
    - its triage PASS uses a global null margin from another period (16.867 d), not a candidate-period significance; the candidate is
      deferred as weak, with possible aliases;
    - the 13450993 TRICERATOPS run does not represent the vetted 2.5-2.8 ppt events; the "nearby/binary more likely" inference is
      WITHDRAWN. No replacement FPP is quoted. The 372343190 run used six photometry sectors, not three.
    - ON_TARGET means "passes the finite-offset pixel screen", not neighbour exclusion.
    - Chronology: prior matching and pixel screening ran concurrently (03:14:57 / 03:15:03 UTC). The prior results existed before
      vetting and survivor selection. This differs from item 131's "prior check FIRST". The decision log alone does not authenticate when
      item 131 was written.
138. 2026-10-22 — Fixes (local; nothing published, nothing frozen, no new data downloaded):
    - scripts/triceratops_qlp_v2.py: explicit --sectors / --phot-sectors; holdout guard (sector <= 105 and no registered test target)
      before any file or TESScut access; exact-path FITS with a TICID/SECTOR header check; vet.py edge rule; inputs + SHA-256 + per-sector
      in-transit counts recorded. The v1 script and its outputs are kept unchanged for provenance. Tests: scripts/test_triceratops_qlp_v2.py
      20/20 (logs/test_triceratops_qlp_v2_20261022.log). Not run: the review asks for no replacement FPP values.
    - scripts/pixel_collect_v2.py:
      - full-precision offsets from the per-sector JSON;
      - attempted / finite / non-finite / failed sector counts;
      - an object with a non-finite or failed sector cannot be ON_TARGET.
      Applied to rounds 2-5 (item 137).
    - scripts/prior_match.py recognises "tid" (NASA Exoplanet Archive TOI schema). The regression test gained a NASA-schema fixture; it
      fails on the previous matcher and passes now (logs/test_prior_match_20261022.log). Direct join: no NASA TOI row for any of the 104.
    - Not done: a candidate-period null statistic for 13450993 (optional; candidate deferred instead).
    - Draft correction for the next release: results/CORRECTION_TRICERATOPS_PIXEL_2026-10-22_DRAFT.md.
139. 2026-10-22 — Round-6 design revised after the design review (results/REVIEW_round6_design.md, R6-1 to R6-10; author's go):
    results/DESIGN_round6_v2.md (SHA-256 417afa6c3413e4fd...; v1 draft kept unchanged).
    - The reviewer's replacement title, premise, S0-authorization and holdout texts are adopted verbatim.
    - Both samples (A: 11.5<T<=13.0, B: 13.5<T<=16.0) are carried through S0, with field-validity rules.
    - Six S0 deliverables, with metadata-only guards.
    - Proposed holdout default: S1-S105 for design/search; every sector >= S106 is test for the whole eligible pool, across all products.
    - Later gates written for detrending, search grid, radius-dependent depth scope (0.8-6 R_E; no fixed 50 ppt), calibration
      (n >= 2995, N*q), faint-star pixel vetting, TRICERATOPS and a product-specific freeze/scoring path.
    - Round-5 lessons added (row-by-row prior adjudication).
    Re-check prompt: results/PROMPT_recheck_round6_design.txt. No round-6 query or download yet; S0 starts only after the re-check and
    the author's approval.
140. 2026-10-22 — Round-5 re-check (results/REVIEW_round5_recheck.md): "Sufficient after listed changes". Applied (local only):
    - C2: CORRECTION to item 137. Forty rows change class: 38 ON_TARGET rows become AMBIGUOUS_INCOMPLETE; TIC 321980862 goes from
      ON_TARGET to AMBIGUOUS; TIC 389029596 goes from OFF_TARGET to AMBIGUOUS. Item 137 said "40 ON_TARGET objects".
    - C1/C1b/C4: scripts/triceratops_qlp_v2.py.
      - The docstring no longer claims vet.py event selection; it states the shared gap-edge mask, the separate preparation and the
        status UNVALIDATED.
      - The manifest adds the ephemeris values, the report.json hash, aperture sectors requested/used/failed, and cutout paths, hashes
        and pixels. The cutout SECTOR and target position are checked before use.
      - --out is a created Path directory.
      - Tests: 25/25 (logs/test_triceratops_qlp_v2_20261022b.log); new cases are output join, TICID/SECTOR header refusal on synthetic
        FITS, and no globbing.
    - C3/C5: draft correction reworded. FPP values are the original saved single-run outputs; the old pixel screen used rounded
      offsets. Claimed discovery dates are separated from the verified public dates. A placement list for the dated notes was added.
    Round 5 is closed; the correction goes into the next release (author's go).
141. 2026-10-22 — Round-6 design re-check (results/REVIEW_round6_design_recheck.md): "S0 may start, after the author's approval".
    Author approved S0 ONLY (metadata). Conditions: lock the selection definitions and pass the wrapper's synthetic refusal tests before
    the first query. No photometry retrieval, pilot or search is approved. Reviewer refinements adopted for S0:
    - fail-closed allowlist wrapper with redirect checks;
    - hashed selection specification (numerical absolute-magnitude band, missing-uncertainty and tie policies, alias-resolving
      exclusion);
    - folder-named-after-TIC wording;
    - S106+ held out during S0;
    - scope-table wording.
142. 2026-10-22 15:11 UTC — Round-6 S0 preparation.
    Pre-S0 orientation, before any S0 query: MAST documentation pages (archive.stsci.edu/hlsp/tess-spoc, /hlsp/tglc) and HTTP HEAD
    size checks on manifests. No catalogue, metadata or photometry query.
    Archive limits found:
    - TESS-SPOC bulk target lists and dl-lc.sh scripts exist for S1-S85 only (S86-S105 return 404); later sectors must come from MAST
      CAOM metadata.
    - Example sizes: TESS-SPOC s0050 target list 8.0 MB, dl-lc.sh 47.9 MB; TGLC s0050 target list 99.5 MB, llc.sh 457 MB.
    - TGLC covers S1-S55; its documentation states 1.3-12.7 million light curves per sector.
    Design text v2.1 (results/DESIGN_round6_v2.1.md, SHA-256 101c169a...) adopts the re-check wording.
143. 2026-10-22 15:12 UTC — S0 selection specification LOCKED before any S0 query:
    results/round6_s0/SELECTION_SPEC_v1.0.json (SHA-256 12fb5bf7f9e747c5e5eafc858673f5e74d5c270803ad219323bcd0d18191df26).
    - Distance: Gaia DR3, parallax >= 10 mas and parallax_over_error >= 5, no zero-point or extinction correction.
    - Cuts: Teff <= 3900 K, R <= 0.6 R_sun, TIC lumclass DWARF, empty TIC disposition.
    - Absolute-magnitude band: Pecaut & Mamajek dwarf locus (M_G vs BP-RP), -1.5 / +1.0 mag.
    - Missing-value and missing-uncertainty rules, deterministic TIC-DR3 tie rule.
    - Identity exclusion of the 42 registered/protected TICs by TIC id, DR2 id, DR3 id and 2" position.
    - Holdout masking of report-table outcome columns: rows with sectors >= 106 or dated on/after 2026-07-11.
    - Availability classes and sources.
    Any change requires a dated item before the selection query.
144. 2026-10-22 15:14 UTC — S0 wrapper scripts/s0_net.py (SHA-256 446511d9b8c8172f...) passes its synthetic refusal tests:
    scripts/test_s0_net.py (SHA-256 2f5c251801182586...), 38/38, logs/test_s0_net_20261022.log. No network is used in the tests.
    The wrapper is a fail-closed allowlist:
    - allowed: VizieR/Gaia/NASA TAP, MAST invoke limited to Caom.Filtered and Catalogs TIC services, TESS-SPOC/TGLC target lists S1-S105
      only, the TGLC readme, the Pecaut & Mamajek table, and the ExoFOP TOI/CTOI exports;
    - refused: LC/FFI/TPF/cutout files, DV/TCE/plot endpoints and every byte-download manifest (dl-lc/dl-tp/dl-dv/llc);
    - redirects are re-checked; content type and size are checked; manifest lines naming sector > 105 are dropped;
    - holdout outcome columns are masked by substring match (one fix during testing: a prefix match missed pl_orbper; the safe side is
      over-masking);
    - guarded_open refuses data/ caches, FITS and the catalogs S106 manifests.
    One test-driven code change before the first real request. The first real S0 request follows this entry.
145. 2026-10-22 15:18 UTC — S0 wrapper change, test-driven. MAST serves the target-list CSVs as application/octet-stream,
    which the wrapper refused (fail-closed, logged). Octet-stream is now accepted only for allowlisted .csv/.txt manifests, and only
    after sniffing the first 4 kB: plain text required, no FITS header, no NUL bytes. Four new tests (FITS bytes, binary bytes,
    octet-stream on TAP, plain-text manifest); 42/42 pass (logs/test_s0_net_20261022b.log).
    Additions to the availability inventory (selection unchanged): CAOM also returns QLP, SPOC 2-min/20-s and TGLC (S1-S11) light-curve
    records. They are kept for the product-hierarchy deliverable.
146. 2026-10-22 15:26 UTC — S0 execution change, dated before the selection query (no cut changed).
    - TIC source: the TIC v8.2 copy at MAST (Mast.Catalogs.Filtered.Tic, the TIC's home archive) replaces the VizieR copy IV/39/tic82.
      VizieR timed out even on a 1-degree band (300 s) and on COUNT(*). Same catalogue and the same prefilter (11.5 < Tmag <= 16.0,
      plx >= 7). MAST count: 451,657 rows. It is fetched in declination bands; the column mapping to the spec's field names is
      recorded in the output.
    - Gaia DR3: the single anonymous async job was aborted at the 60-s anonymous execution limit. The same query is run as 200
      source_id slices (HEALPix-level-12 ranges), sync, about 10 s each, and concatenated; slice completeness is checked.
    The registered/protected identities (42 TIC rows; DR3 ids via dr2_neighbourhood) were already fetched from VizieR (identical
    catalogue) and are re-fetched from MAST for consistency.
147. 2026-10-22 15:29 UTC — S0 wrapper fixes, test-driven; 45/45 tests pass (logs/test_s0_net_20261022c.log).
    (1) guarded_open refused the published-table corpus results/prior_search*/data/ because the path contains "/data/". The refusal now
        applies to the top-level data/ photometry caches only. Tests added: corpus readable; top-level data/ non-FITS file refused.
    (2) The 2026-10-20 ExoFOP CTOI snapshot has no sector or date column. Its outcome columns are masked for ALL rows (membership
        only), via mask_holdout(kw_all=True), with a test.
    ExoFOP returned HTTP 503 (maintenance page) again. The fallback is the NASA Exoplanet Archive TOI table (8,151 rows; masked by
    toi_created >= 2026-07-11) plus the CTOI snapshot (5,138 rows, fully masked). Fetched for the prior matrix: VizieR
    J/AJ/165/265/table1 (Ment & Charbonneau 2023 targets) and J/A+A/710/A352 tables a2, a3, a4, c1 (Tschudi 2026). No public parent
    lists were found in VizieR for NEMESIS I/II, Bryant et al. 2023 or GEMS; RAVEN publishes candidate tables only.
148. 2026-10-22 16:26 UTC — S0 selection funnel (spec v1.0, SHA-256 12fb5bf7...). Run 2 is the result of record.
    Implementation fixes made after run 1, both disclosed:
    (a) Locus parser: the Pecaut & Mamajek header line starts with "#SpT"; the parser now reads the main dwarf table (62 rows).
    (b) Order of operations: run 1 resolved TIC-to-DR3 ties BEFORE the spec's empty-disposition exclusion. A DUPLICATE/SPLIT twin
        sharing a DR2 id then knocked out a valid TIC as an "ambiguous tie" (8,562 tie exclusions). The disposition exclusion now runs
        first; no cut changed. Run-1 funnel kept as results/round6_s0/funnel_run1_tieorder_bug.json (A 34,482 / B 86,528).
    Run 2 (results/round6_s0/funnel.json):
    - inputs: Gaia DR3 506,246 sources (parallax >= 10, poe >= 5); TIC prefilter 451,653 rows; 20,186 TIC rows excluded by disposition;
      1,979 genuine ties excluded and listed (two or more valid TICs on one DR3 source); 27 lost to a closer TIC;
    - FINAL: sample A (11.5 < T <= 13.0) 34,547 stars; sample B (13.5 < T <= 16.0) 86,550 stars;
    - registered/protected identity exclusion removed 0 (all 42 lie outside both magnitude ranges or failed earlier cuts).
    Known incompleteness (to report, not fixed under spec v1.0): DR3 100-pc M-band stars with estimated T in range but no prefiltered
    TIC row number about 5,132 (A) and 7,099 (B). In a random 300 checked against the full MAST TIC:
    - about one third have no DR2 parallax in TIC, so the plx >= 7 prefilter dropped them;
    - about two thirds have no TIC row under that DR2 id;
    - 11 have a TIC Tmag just outside the range.
    Any fix (e.g. prefilter "plx >= 7 OR plx missing") is a spec revision needing a dated decision.
149. 2026-10-22 16:37 UTC — S0 holdout safeguard. A TIC-only run of scripts/prior_match.py over the corpus was stopped before
    it wrote anything: that tool stores each matched record's period, and corpus tables could hold signals derived from S106+ data
    for pool stars (the spec masks outcome fields before storage). It was replaced by scripts/s0_corpus_scan.py, which reads ONLY the
    TIC column(s) of each table and stores (tic, file, has_period_column, n_rows), plus folder names TIC<id>. The prior-matrix
    builder likewise reads only TIC columns from the eumemic, RAVEN, Ment, Tschudi and TOI/CTOI tables.
    Availability runs launched: tess-point S1-S134; CAOM light-curve metadata (TESS-SPOC/QLP/SPOC/TGLC) for the 121,097 pool stars;
    TESS-SPOC target lists S1-S85; TGLC target lists S1-S55 (about 5.5 GB of text, streamed and filtered, nothing stored but hits).
150. 2026-10-22 17:11 UTC — Round-6 S0 COMPLETE (metadata only). Report: results/round6_s0/S0_REPORT.md (SHA-256 dab45526ab186428...).
    Samples: A 34,547; B 86,550.
    Availability (CAOM 303/303 chunks; TESS-SPOC target lists S1-S85; TGLC target lists S1-S55; tess-point to S134):
    - B: 62,701 stars with LCs in >= 2 campaigns, 44,918 with TESS-SPOC in >= 2 campaigns, 59,606 with LCs in S56-S105;
    - CAOM lists QLP LCs for 55,295 B stars (T > 13.5).
    Prior matrix: 97.6 % of A is on eumemic's published faint-M searched-star lists (same Teff/R cuts, S1-S104); 0 % of B. RAVEN rule
    G < 14 covers 38 B stars. NEMESIS/Bryant/GEMS overlap is rule-based only (lists not public). TOI/CTOI hosts: A 117/72, B 33/40.
    New exposure finding: 299 pool stars (catalogs/s107_dwarf_targets.csv, our original 2026-10-17 search) have SPOC 2-min files in
    data/lc for S106 (149 stars) and S107 (all 299). They were listed by filename only. They are to be treated as retrospective and
    excluded from any prospective claim.
    Request-log audit: 969 allowed requests (TAP 397, MAST 413, manifests 153, docs/tables 6); 0 allowed requests matching a product
    pattern; refusals are test-suite cases plus the logged real ones (octet-stream; corpus path).
    Proposals for the author (none authorized):
    - drop A as a discovery sample;
    - B toward a bounded P1 pilot, with TESS-SPOC first, QLP as a cross-check and TGLC S1-S55 as an independent extraction;
    - S1-S105 design/search and S106+ test for the whole pool;
    - optional spec v1.1 to recover about 7,100 B stars lost to the TIC parallax prefilter.
    Review prompt: results/PROMPT_review_round6_S0.txt.
151. 2026-10-22 17:14 UTC — S0 report revised (supersedes the hash in item 150). results/round6_s0/S0_REPORT.md is now
    SHA-256 cf4f6720d025f1fa...
    (1) New table, as the re-check required: status of S106+ as of 2026-10-22 (scripts/s0_holdout_status.py,
        results/round6_s0/holdout_status.{csv,json}). Classes: (d) previously examined, (a) observed with a public LC, (b) observed
        with no public LC yet, (c) in progress or future.
        - B: (a) 2,406 stars, (b) 8,345, (c) 44,789, (d) 0.
        - A: (d) 299, (a) 1,232, (b) 3,211, (c) 17,875.
        Special sector 1751 (3I/ATLAS) is treated as a test sector (conservative).
    (2) The 299 previously examined stars are confirmed SEARCHED, not just downloaded: search_pipeline.py loaded every SPOC 2-min
        sector of each S107 target (DECISIONS 3, 5). All 299 are in sample A.
    (3) NASA TOI table re-masked on max(toi_created, rowupdate) >= 2026-07-11: 884 rows masked, 87 before. Membership is unchanged
        (A 117, B 33). The Tschudi and Ment tables got a holdout note in their meta files: both predate S106.
152. 2026-10-22 17:38 UTC — Round-6 S0 review (results/REVIEW_round6_S0.md): "S0 is not complete". Findings S0-1 to S0-10
    were checked by us. S0-1 is confirmed in our files: the combined raw/gaia.csv and raw/tic.csv store Gaia DR2 ids as floats
    (e.g. 1153598151720704.0, scientific notation). The integer cast then shifts ids by up to 256, so the joins, ties and samples of
    run 2 are wrong. The original slice/band files keep exact ids.
    Run 2 is preserved unchanged as results/round6_s0/superseded_run2/ (with SHA256SUMS).
    The repair stays within S0 (metadata only; the author's S0 approval):
    - exact-ID rebuild with a regression test;
    - positive-allowlist holdout masking;
    - TGLC target lists counted as produced LCs and joined by exact Gaia DR3 id;
    - GEMS parent list attempted (Zenodo 15738847);
    - prior-cell wording;
    - wrapper hardening (content type, byte cap, payload logging, test tagging);
    - reproducible prefilter-loss diagnostic;
    - exposure ledger;
    - chronology and decision wording.
    Nothing beyond metadata is authorized; no P1 work until the author says so.
153. 2026-10-22 18:22 UTC — S0 repairs after the review (item 152); all metadata only.
    Access layer (S0-7, S0-2, S0-5): scripts/s0_net.py (SHA-256 95dd57b5d638c897...).
    - Refuses a missing content type. Every non-JSON body must look like text (UTF-8, at least 95 % printable, no FITS/NUL).
    - Streamed bodies have a byte cap.
    - POST payload hash, TAP query text and MAST service/columns/filter names are logged. Synthetic tests are tagged and write to
      logs/round6_s0_requests_tests.log.
    - Holdout masking is a POSITIVE allowlist (explicit keep columns; every other column of a held row is blanked).
    - The GEMS Zenodo record (15738847) is allowed, as record JSON and .csv/.txt only.
    - Tests: 58/58 (logs/test_s0_net_20261022d.log).
    Identifiers (S0-1): scripts/s0_selection.py parses Gaia/TIC ids exactly from text (exact_ids, read_ids). Regression test
    scripts/test_s0_ids.py: 6/6, ids 128/256 apart. Combined raw/gaia.csv and raw/tic.csv were rebuilt from the original slice/band
    files. Registered DR3 aliases were re-fetched, because run 2 had queried rounded DR2 ids. The 2" identity match now propagates
    Gaia positions to epoch 2000.0.
    Snapshots (S0-2): the NASA TOI query now requests tid, toi and dates only; the CTOI snapshot keeps TIC ID and CTOI only. Earlier
    S0 copies, including those in superseded_run2/prior/, were stripped to these columns; their original hashes are in
    results/round6_s0/stripped_files_original_hashes.txt (superseded_run2/SHA256SUMS regenerated). EXPOSURE_LEDGER.md records what was
    stored before.
154. 2026-10-22 18:22 UTC — Round-6 S0 run 3 (result of record; runs 1-2 superseded). Report: results/round6_s0/S0_REPORT.md
    (SHA-256 ed456ce3303b6107...).
    - Funnel (exact ids): A 35,036, B 87,208; 0 ambiguous ties; 30 lost to a closer TIC. This matches the reviewer's independent
      reconstruction.
    - Prefilter diagnostic (seeded, unique sources): of 300 unmatched sources, 272 have no TIC parallax and 28 a TIC Tmag outside the
      range. Run 2's "two thirds have no TIC row" was an artifact of the rounding.
    - Availability: TGLC manifests count as produced LCs, resolved by exact DR3 id (901 rows re-assigned to pool stars). B: 81,618
      stars with any LC, 70,681 with >= 2 campaigns, 45,063 with TESS-SPOC in >= 2 campaigns, 60,046 with LCs in S56-S105.
    - Prior: GEMS parent list 72.5 % of A and 74.8 % of B; eumemic faint-M lists 97.6 % of A, 0 of B. RAVEN partial screen covers
      0 B stars.
    - Exposure: 307 A stars previously searched (S107 for all, S106 for 153); EXPOSURE_LEDGER.md. Corpus read errors: 7, all empty
      files.
    - Test-sector status for B: (a) 2,408, (b) 8,451, (c) 45,107 stars.
    Proposals unchanged in kind: drop A; draft a P1 design for B for review only. Re-check prompt:
    results/PROMPT_recheck_round6_S0.txt.
155. 2026-10-22 18:25 UTC — Run-3 verification and spec-text notes.
    (1) Star-for-star check: the run-3 samples equal the reviewer's independent exact-ID samples ([local temporary path redacted]
        sample_exact_{A,B}.csv): A 35,036 = 35,036, B 87,208 = 87,208, no star in one set and not the other.
    (2) Request-log audit of run 3 (entries after 17:38 UTC): 465 allowed requests (MAST 313, MAST archive manifests 140, Zenodo 9,
        Gaia 1, NASA archive 1, ExoFOP 1); 0 allowed URLs matching a product pattern. Whole log: 1,436 allowed.
    (3) No real manifest or GEMS line was dropped by the sector filter: the 4 REFUSED_LINES entries are synthetic test cases from
        before tagging. GEMS counts are complete.
    (4) Spec-text divergences, recorded here; neither is a cut change.
        - SELECTION_SPEC_v1.0 lists masked_column_patterns; the implementation now uses a stricter positive allowlist.
        - The spec says the 2" identity match is "at epoch 2016.0"; the implementation propagates Gaia positions to 2000.0, the TIC's
          native epoch. This is an equivalent test at a common epoch.
    Report SHA-256 after adding the audit total: da6bafff0492957e... (supersedes the hash in item 154).
156. 2026-10-22 21:05 UTC — S0 re-check (results/REVIEW_round6_S0_recheck.md): "S0 complete after the listed changes"; a P1
    design document may be drafted. Changes applied:
    - RC1: the ExoFOP-success paths (scripts/s0_prior.py exofop_toi_membership / exofop_ctoi_membership) read identifier and date
      columns only. The local CTOI snapshot is read with usecols. Caller-level synthetic tests: scripts/test_s0_prior_exofop.py, 4/4.
    - RC2: GEMS file verified against the deposit: md5 3e9745b7bc79bcabdf98a83554ff79b0, 495,018,405 bytes. It holds 153,606 rows /
      distinct ids, while the source description and paper state 149,316. It is labelled "deposited-table membership; final
      analysed-sample membership not individually verified". Counts unchanged (B 65,268).
    - RC3: s0_prefilter_loss.py saves the minimal TIC responses (prefilter_loss_tic_responses.csv), so the reasons can be recomputed
      (rerun: 272 missing parallax / 28 out of range); the locus end convention is documented. The stale run-2 file
      prefilter_loss_sample_tic.csv was removed from the run-3 directory; an identical copy is in superseded_run2/.
    - RC4: ledger "not displayed" statements relabelled as author declarations.
    - The stream-cap test now omits Content-Length; 58/58 pass.
    - Correction to item 155(4): "equivalent test" overstates it. It is a declared common-epoch (2000.0) implementation, with no
      exclusion in this run.
    S0 COMPLETE. Report SHA-256 44758aab0f394329...
    Author's decisions (2026-10-22):
    (2) Sample A dropped as a discovery sample.
    (3) Draft a P1 pilot DESIGN document for sample B, for review. Nothing executes.
    (5) Spec v1.1 approved: measure what an enlarged parallax prefilter adds. It must be locked before its query.
    (4) Asked for advice. Recommendation recorded: stars previously searched by this project are EXCLUDED from round-6 pools (all 307
        are in A, which is dropped); the filename inventory is rerun for any star added by v1.1.
157. 2026-10-22 21:06 UTC — Selection spec v1.1 LOCKED before its query: results/round6_s0/SELECTION_SPEC_v1.1.json
    (SHA-256 1186dffe0796a050c72abeb2e5a2270943ca4d44b9cc78a550536c4de5c86d07).
    - Sample B only; A dropped.
    - TIC candidates = the v1.0 prefilter UNION TIC rows of any parallax matched by exact DR2 id to unmatched DR3 100-pc sources. A
      query-volume screen of BP-RP >= 1.0 and 12.5 <= G <= 19.5 is applied (95,829 DR2 ids; >= 1 mag of margin beyond the v1.0 B
      sample).
    - Previously examined stars are excluded.
    - All other cuts are unchanged.
    The screen margins were set from the v1.0 sample's G/colour span and a count of query volume, not from any v1.1 result.
158. 2026-10-22 23:04 UTC — Spec v1.1 result (sample B). The lookup (95,829 DR2 ids, 192 chunks, row counts checked; 2 read
    timeouts retried) returned 98,195 extra TIC rows (raw/tic_v11_extra.csv).
    Funnel (results/round6_s0/funnel_v11.json): 105,344 in the magnitude range, then 92,187 final.
    - All 87,208 run-3 B stars are kept; 4,979 are added (T 13.5-16.0, median 14.39; median distance 81 pc).
    - "Lost to a closer TIC" rises to 18,280, as expected: the lookup also returned TIC rows for secondary DR2 neighbours of DR3
      sources that were already matched, and the locked closest-match rule discards them.
    - 0 ties.
    - Previously examined: 0 (filename inventory rerun on the v1.1 pool: exposure_inventory_v11.json).
    - Registered/protected: 0; closest 6.2".
    Availability and prior-matrix rows for the 4,979 added stars are not yet inventoried (metadata). They are to be done before any P1
    draw, under the same S0 tools.
    P1 pilot design drafted (document only): results/DESIGN_round6_P1_pilot_DRAFT.md; review prompt
    results/PROMPT_review_round6_P1_design.txt. Nothing executes.
159. 2026-10-22 23:38 UTC — P1 design review (results/REVIEW_round6_P1_design.md): "ready after listed changes"; P1-1 to P1-8
    blocking/major. Author's go (2026-10-22): (a) the metadata inventory of the spec-v1.1 pool, and (b) a revision of the P1 design to
    v2 for one more review. Pilot execution stays UNAPPROVED.
    Stopping rule recorded (author agreed with the recommendation):
    - if the v2 review still finds blocking issues, round 6 pauses;
    - if an approved P1 fails its pre-declared criteria, round 6 closes with the measured limits.
    The S106 scoring, the DDT reply and ground windows take priority over round 6.
    (a) is run as a FULL inventory of the 92,187-star v1.1 pool into separate *_v11 outputs (S0 tools, selected with S0_POOL=v11), not
    by patching run-3 files.
160. 2026-10-23 00:00 UTC — (a) Metadata inventory of the spec-v1.1 pool (92,187 stars; S0 tools with S0_POOL=v11; outputs
    availability_v11/, prior/*_v11*, holdout_status_v11.*, s0_stats_v11.json, s0_cost_v11.json).
    - Completeness: CAOM 231/231 chunks, 0 failed; all 85 TESS-SPOC and 55 TGLC target-list sectors ok; pointing done.
    - Corpus scan: 10,073 stars hit; 7 read errors, all empty files.
    - Availability: any LC 86,125; >= 2 campaigns 74,605; TESS-SPOC >= 2 campaigns 45,322; S56-S105 63,305.
    - Prior: GEMS deposited table 68,695 (74.5 %, as the reviewer computed independently); eumemic faint lists 0; RAVEN G < 14 screen 0;
      unique known hosts 71 (36 TOI, 41 CTOI, 6 both).
    - Test-sector status, B stars: (a) 2,432, (b) 8,963, (c) 47,810.
    Allocation table (scripts/s0_p1_allocation.py; p1_allocation_v2.{csv,json}; no star drawn): search-eligible 74,336, after
    excluding 71 K, 199 missing e_Rad and 17,581 with < 2 campaigns. 14 cells after 2 recorded merges; D 1,000 / C 3,000; about 733 D
    stars in the targeted 2 R_E stratum (R* <= 0.3).
    (b) P1 design v2: results/DESIGN_round6_P1_pilot_v2.md (SHA-256 36b99b53f64f5f93...), addressing P1-1 to P1-8. v1 is kept unchanged.
    Review prompt: results/PROMPT_review_round6_P1_design_v2.txt. Execution stays UNAPPROVED; the stopping rule of item 159 applies.
161. 2026-10-23 00:42 UTC — ROUND 6 PAUSED under the stopping rule of item 159. The P1 v2 review
    (results/REVIEW_round6_P1_design_v2.md) says "not ready". Two blocking issues:
    - B1: our QLP injection convention is wrong. QLP SAP_FLUX is deblended under the target-origin assumption (Huang et al. 2020,
      Sec. II-III; DRN004: TGLC-based decontamination from S94), so the extra 1/(1 + contratio) factor would bias the product
      comparison. This was our error.
    - B2: the C gate (<= 1 trigger in 3,000) has no consistent estimand, given the weighted stratified sample, the single-product
      trigger with no substitution (only about 1,816 C stars are expected to have two TESS-SPOC campaigns) and correlated sectors.
    Resolved per the reviewer: P1-3, P1-5, P1-7 at design level; allocation feasibility (reproduced exactly).
    Pre-run items noted for any reopening (not blocking on their own): P1 probability labels, the allocation rule and the approval
    order; P2 a total order for (S, M) and the alias/inversion control flow; P3 N2 is a stress test (counterexample probability
    0.0167), and the N1 wording is wrong; P4 the QLP clock policy and TGLC refusal policy; P5 C's machine-only real-orientation
    comparator; P6 the eligibility order and denominators.
    State at pause:
    - S0 complete; spec v1.1 pool B = 92,187 with full metadata inventory; allocation table computed, no draw;
    - no light curve was downloaded for round 6; D/C/K were never drawn.
    Nothing is published. Reopening needs the author's explicit decision and a v3 addressing B1-B2, then review.
    Priorities now: S106 scoring (on the author's go), the DDT reply, ground windows, and the next release with the round-5 corrections.
162. 2026-10-23 01:34 UTC — Author's go (2026-10-23): "go 3 and 1".
    (1) S106 scoring: QLP S106 is NOT yet released. https://archive.stsci.edu/hlsps/qlp/s0106/ returns 404; the QLP HLSP directory
        ends at s0105; MAST CAOM has QLP records only through S104. Nothing was downloaded. A session-only twice-daily check (cron
        94d49683, 7-day expiry) reports the release. Scoring then follows the locked conformance-v2.1 procedure under the author's
        standing go, starting with a run plan logged here before the first S106 file is fetched.
    (2) Release v1.16 ASSEMBLED LOCALLY (scripts/assemble_v1_16.py; nothing committed, pushed or uploaded):
        - round 5: tables/round5/, reviews_round5/, README block;
        - corrections/CORRECTION_TRICERATOPS_PIXEL_2026-10-22.md, with dated append-only notes in 6 registrations (151767028,
          343298093, 188664994, 253931796, 160330868, 91617711), notes beside 3 triceratops.json, README inline markers (FPP 0.031,
          0.020, 0.065-0.11; "All 26"), and REPORT correction 10;
        - scripts: triceratops_qlp_v2 + tests, pixel_collect_v2, prior_match (tid) + test, triage_round5, tri_runner_round5;
        - tables/pixel_v2/; CITATION 1.16; public DECISIONS regenerated; MANIFEST_v1.16.md;
        - release notes zenodo_upload/RELEASE_NOTES_v1.16.md; draft Zenodo notice for the dataset records
          (zenodo_upload/ZENODO_NOTICES_v1.16_DRAFT.md).
        Checks: 70 prediction CSVs byte-identical; registrations and DECISIONS changed by appends only; no e-mail addresses, session
        links or scratch paths in changed files.
        Round 6 is not released (paused). Next: the assembled-release review (results/PROMPT_review_v1.16_assembled.txt), then the
        author's go to publish.
163. 2026-10-23 13:47 UTC — Assembled-release review of v1.16 (results/REVIEW_v1.16_assembled.md): "publish after listed
    fixes". The author's go (2026-10-23) covers A1-A6, with A3 as the informational cross-reference.
    CLARIFICATION to item 162: its statement "no scratch paths in changed files" was wrong. The two copied round-5 reviews contained 9
    local temporary paths each, the public DECISIONS item 155 one, and the release-notes attribution an e-mail address (review A1).
    Fixes:
    - public review copies with paths redacted and labelled;
    - scripts/make_public_decisions.py redacts temporary paths after the already-published prefix (items 1-130 stay byte-identical,
      including the inherited published paths in items 86 and 128, disclosed here);
    - plain-text attribution in the release notes.
    A2: TIC 61310956's fold used S46 INSTEAD OF S22 (S45 and S72 common). Seven runs included additional sectors; the eighth was a
    substitution. Wording corrected in README, its note, the release notes, the dataset notice and the assembly script.
    A5: "70 prediction CSVs" should read "all 68 prediction CSVs unchanged; the two other registration-area CSVs also unchanged".
    A4, A6: the historical pixel counts and the round-6 scope sentence are labelled.
164. 2026-10-23 13:48 UTC — v1.16 fixes A1-A6 applied locally (scripts/fix_v1_16_review.py; assembly templates patched).
    Checks:
    - privacy scan clean, except the round-5 prompts' "do not read ~/.zenodo_token" instruction (a file name, not a credential);
    - registrations and DECISIONS append-only (prefix byte-identical to HEAD);
    - 68 prediction CSVs + 2 other registration-area CSVs unchanged;
    - manifest 40 rows, all hashes correct.
    Re-check prompt: results/PROMPT_recheck_v1.16_assembled.txt. Nothing is published.
165. 2026-10-23 23:26 UTC — v1.16 PUBLISHED. The re-check (results/REVIEW_v1.16_assembled_recheck.md) said "publish as
    assembled". The author's go covers the exact reviewed files, not a rebuild.
    - Before commit: MANIFEST_v1.16.md 57ce05fb..., RELEASE_NOTES_v1.16.md fd8b90ab... and ZENODO_NOTICES_v1.16_DRAFT.md afb9d847... match
      the review hashes; all 40 manifest hashes pass; HEAD was the reviewed base 9a17efc.
    - GitHub: commit cf556794 (41 files, no session link, Co-Authored-By trailer), tag v1.16, release with the reviewed notes.
      Archived automatically as Zenodo 10.5281/zenodo.23606533.
    - Dataset notice (informational cross-reference, reviewed text with the release link filled in) prepended to 23535544, 23512928
      and 23462438. Each deposited ZIP's md5 equals the local copy the reviewer inspected (fbf0fe5d / 665d8021 / 4d3a8086). Each
      description grew by exactly the notice; verified on the public API. No preprint notice.
    Non-blocking notes from the re-check, recorded:
    - N1: the local rebuild scripts (assemble_v1_16.py + fix_v1_16_review.py) are inconsistent with each other. They must not be used
      to rebuild v1.16; the published bytes are the record.
    - N2: item 163's "9 local temporary paths each" counts affected lines. There were 11 and 13 occurrences, as the public-copy labels
      state.
    The Zenodo token of 2026-10-18 was used again and is still not revoked.
166. 2026-10-24 00:17 UTC — Author's go (2026-10-23) to lock scoring configs for the frozen tests in S107-S121. This is
    BEFORE any of these sectors' photometry is examined; the round-4 pattern applies. The author's "yes" adopts, for these 14 objects,
    the primary-sector rule of item 120(2): the first listed sector with a released QLP v01 light curve is the test of record and is
    never replaced; later sectors are separate tests.
    Facts established first (metadata and own files only):
    - Test sectors come from rows of the latest prediction CSV whose status starts with "prediction". Both evaluators score only
      those rows (prereg_conformance.py:212-213, prereg_test.py:23). Retrodiction-only sectors get no config: S108 for 24526743,
      53825235 and 160330868.
    - 26 configs:
      - 24526743 S107;
      - 160330868 S107, S109;
      - 196514928 S109-S112;
      - 53825235 v3 S109-S110;
      - 19119739 S111-S112;
      - 159033763 S111;
      - 283913390 S111;
      - 333661705 S111-S114;
      - 162304222 v4 S111-S114;
      - 258006047 S114; 333735955 S114; 467959906 S114;
      - 203381983 S115;
      - 366047768 S121.
      These match the monitoring agent's table.
    - Product: none of the stars is on the 2-min list of its test sector where a list exists: S107 manifest (local); S109 and S110
      target lists fetched (catalogs/target_lists/all_targets_S109_v1.csv sha 02319a02..., S110 8706361c...). S111+ lists are not yet
      published. QLP SAP_FLUX is therefore locked for all 26. If a star later appears on a 2-min list, QLP stays the product of
      record and SPOC is reported as a secondary readout only.
    - Reference values:
      - 9 registrations carry the frozen reference-values line;
      - 5 round-2 registrations (258006047, 333735955, 467959906, 203381983, 366047768) predate it. For them, the generator rule is
        applied as a dated amendment (S106 precedent, 70441745): report.json sap_depth, and the BLS duration_h because no shape-fit
        T14_h exists.
    - Exposure (filename-only inventory of data/, results/round6_s0/exposure_inventory_tests14.json): local files for these stars
      reach S104 at most; none from S105 or later.
    - Data status: S107 (and S108-S109) are already observed. Public products exist for S107 (FFIs; SPOC 2-min LCs of other stars).
      The authors attest that no target-sector photometry of these stars has been examined. Those tests are held-out checks of
      already-observed data (ERRATUM_S106 class), not prospective predictions. S110+ are future or in progress at the lock.
    - Clock priors: 12 exist. New ones for 203381983 (controls S91, S64; c0 +0.032 min) and 366047768 (S83, S82; +0.033 min),
      made by qlp_clock_v2.py from in-sample controls (56-98, excluding 74-79); neither star has an S99+ sector.
    Next: generator (refuse-on-exists), lock file, a validator taking the lock as an argument, tests on in-sample files only, dated
    scoring amendments in the 14 registrations, then external review.
167. 2026-10-24 00:22 UTC — S107-S121 configs LOCKED (scripts/make_conformance_configs_s107_s121.py; refuse-on-exists).
    - 26 configs in configs/conformance/; lock configs/conformance/LOCK_2026-10-23_S107_S121.json (SHA-256 a8731dfcb4a482f6...).
      ROUND4_LOCK.json and the S106 configs are untouched.
    - Primary sectors (tests of record):
      - 24526743 S107; 160330868 S107; 196514928 S109; 53825235 S109;
      - 19119739, 159033763, 283913390, 333661705, 162304222 S111;
      - 258006047, 333735955, 467959906 S114;
      - 203381983 S115; 366047768 S121.
    - Generator-rule reference values (dated amendment): 258006047 1075 ppm / 2.7 h; 333735955 906 / 1.8; 467959906 289 / 1.65;
      203381983 1616 / 1.35; 366047768 322 / 3.0 (report.json sap_depth; BLS duration_h).
    Tests: scripts/test_locked_configs.py (generalised from test_round4_configs.py, which is unchanged) gives 655/655 on the new lock
    (logs/test_locked_configs_S107_S121_20261023.log) and 200/200 on ROUND4_LOCK.json, identical to its published suite. Only
    in-sample files (<= S105) and synthetic records were used.
    Dated scoring amendments were appended to the 14 registrations (latest version of each). They give the configs and hashes, the
    product, clock gate, primary rule, reference values and data status; S109 is worded as "being observed".
    Sync: v1.16 had appended its notes directly to the public copies. The local copies of 151767028, 343298093, 188664994, 253931796
    and 91617711 were updated to the public bytes, and 160330868 was rebuilt as public + amendment. All local registrations now
    extend their public copies.
    Next: external review of the lock (results/PROMPT_review_S107_S121_configs.txt); publication in the next release on the author's go.
168. 2026-10-24 01:09 UTC — Configs review (results/REVIEW_S107_S121_configs.md): "lock sound after the listed changes".
    v1.17 publication is held until the corrections are re-checked (author). Fixes:
    - S1 (CLARIFICATION to item 166): the explicit primary sector named in each locked config is the test of record, irrespective of
      release order or whether a QLP v01 product is eventually available. If it is unavailable, that status is recorded and no later
      sector is promoted. The phrase "first listed sector with a released QLP v01 light curve" in item 166 does not authorize
      replacement. The 14 primary flags are unchanged.
    - Precision on item 166's data status: S107 was already observed; S109 was still being observed at the lock (2026-10-24 00:18 UTC;
      partly public via TESScut through S109 orbit 1a); S110 had not started. The registrations already said so. The lock's UTC time is
      2026-10-24 00:18:34; "2026-10-23" in the amendment titles is the author's local date.
    - S2: advance statement appended to TIC 160330868 v2 (the reviewer's text). S107 primary is expected INSUFFICIENT (both events in the
      edge trims); S109 has a single prediction-status event. No change of primary, no pooling, no promotion of the retrodiction.
    - S3: scripts/s0_exposure_inventory.py also recognizes data/lk_cache/clockcheck/<TIC>/. Inventory: 122 paths (34 previously
      unrecognized clock cutouts), still nothing after S104. The v1 snapshot is kept (*_snapshot_v1.*). It is described as recognized
      filename evidence, not proof of non-examination; the authors' attestation stands.
    - S4: provenance caveats for the public bundle: TIC 162304222's prior is the +0.033-min fallback (no clean control); TIC
      366047768's S83 control samples include outliers (+0.148, -0.111, -0.355 min) beside a clean group. The locked median (+0.03265
      min) is kept.
    - S5: scripts/test_locked_configs.py now uses an artificial byte fixture instead of a real QLP file. 655/655 (new lock,
      logs/test_locked_configs_S107_S121_20261023b.log) and 200/200 (round-4 lock). This does not cover valid FITS, timing alignment or
      scoring.
169. 2026-10-24 01:10 UTC — v1.17 assembled locally (scripts/assemble_v1_17.py; single pass, final text emitted directly;
    refuses to run twice). Content:
    - conformance_s107_s121/: 26 configs + lock, generator, generalized tests with the artificial fixture, inventory script, test log,
      README with the S1 rule, the 160330868 expectation, reference-value provenance, data status, S4 prior caveats and S5 test limits;
    - the 14 amended registrations;
    - the two new clock priors in preregistration/qlp_clock_v2/; the other 12 are already published byte-identical to the lock;
    - reviews_s107_s121/ (review copy with path-only redactions; prompt);
    - README block; CITATION 1.17; DECISIONS regenerated; MANIFEST_v1.17.md.
    Not published: a re-check of the corrections comes first (author: hold v1.17 until checked).
170. 2026-10-24 03:56 UTC — v1.17 PUBLISHED after the re-check (results/REVIEW_S107_S121_v1.17_recheck.md: "publish as
    assembled") and the author's go for the reviewed files.
    - Before commit: anchors matched (MANIFEST_v1.17.md 299b4f93..., lock a8731dfc..., RELEASE_NOTES_v1.17.md 302bd623...); 53 manifest
      hashes passed; base cf556794.
    - Published: commit 50377874 (no session link; Co-Authored-By trailer); tag and GitHub release v1.17; Zenodo 10.5281/zenodo.23609152.
    The S107-S121 lock now has a public timestamp before any of those sectors' QLP data were released.
    ENVIRONMENT PROBLEM found while fetching the DOI: Homebrew python@3.12 is no longer installed (system python3 is 3.15.0). The
    project venv .venv points to the missing /opt/homebrew/opt/python@3.12 interpreter (pyvenv.cfg records 3.12.9, the version the venv was created with; Homebrew had since upgraded it in place to 3.12.15). .venv_tri (Anaconda) is unaffected. Every project
    script, including the locked S106 scoring, cannot run until Python 3.12 is restored. The reviewer saw the same thing. No project
    file is affected.
171. 2026-10-24 04:16 UTC — Environment restored (author's go while away). Command: HOMEBREW_NO_AUTO_UPDATE=1
    HOMEBREW_NO_INSTALL_CLEANUP=1 brew install python@3.12, so no other formula was upgraded or cleaned. .venv runs again: Python
    3.12.15.
    - Packages: all 79 installed distributions equal results/conformance_v21/requirements_venv_locked.txt (importlib.metadata, as the
      record was made); 0 differences.
    - Interpreter: patch level 3.12.15 against the record's 3.12.9. The record was taken 2026-10-20; Homebrew had upgraded the venv's
      interpreter in place to 3.12.15 before 2026-10-21 (earlier tracebacks show 3.12.15). The rounds-5/6 and lock work ran on
      3.12.15. To be reported with the S106 scoring as a disclosed environment difference.
    - Checks: test_s0_ids 6/6; test_locked_configs on ROUND4_LOCK 200/200.
172. 2026-10-24 14:12 UTC — Author's decisions (2026-10-24), before any of these sectors' data are examined:
    (a) TIC 317134140 (S108-S110). It is on the 2-min target lists of S108, S109 and S110 (catalogs/target_lists/all_targets_S10{8,9}
        and S110 _v1.csv). Its 2026-10-17 registration defines its own test: per-sector stacked depth at the predicted phase about
        185 +- 40 ppm; blind BLS of each sector ranks 0.5719 d near the top. It will be scored by a DEDICATED SPOC scorer that implements
        exactly that frozen test on SPOC 2-min PDCSAP_FLUX. Every operational choice ("near the top" = top 3, as in the blind tests of
        item 12; window; detrending; error model) is fixed in a locked config before any S108 data, then reviewed and published.
    (b) TIC 80387959 and 120517801 (S111-S114). Their registrations allow "QLP or SPOC". Product of record by AVAILABILITY, fixed now:
        if a SPOC 2-min light curve exists for the sector at scoring time, it is the product of record, scored with a reviewed SPOC
        procedure published before those data; otherwise QLP SAP_FLUX with the locked conformance v2.1 evaluator. The other product is
        always reported as a secondary readout. This differs from the QLP-always rule of the 14 objects locked in v1.17; each rule is
        declared before its data.
    Gap found 2026-10-24: these three objects had no locked scoring configs (my omission when choosing the 14).
173. 2026-10-24 14:15 UTC — TIC 317134140 dedicated scorer v1.0 draft (scripts/prereg_spoc_317134140.py, SHA-256 584f9bf6d87d549f...).
    Design-sector mechanics check on its four TRAINING sectors (the signal is assumed present there; not independent;
    results/conformance_317134140/insample_S*.json). Recorded BEFORE any change to the scorer:
      S6:   clause A A_CONSISTENT, 127 +- 56 ppm, 31 eligible | B_NOT_TOP3 (0.9196, 5.1278, 3.3766) -> PARTIAL
      S87:  A_INCONCLUSIVE, 139 +- 83 ppm, 32 eligible       | B_NOT_TOP3 (0.9114, 1.7238, 0.5327) -> INCONCLUSIVE
      S98:  A_CONSISTENT, 208 +- 32 ppm, 53 eligible         | B_TOP3 (0.5717, 1.1428, 6.3992)    -> PASS
      S107: A_CONSISTENT, 201 +- 56 ppm, 32 eligible         | B_NOT_TOP3 (1.4295, 0.8499, 7.1322) -> PARTIAL
    The per-sector blind-rank clause (original search_pipeline per-sector BLS, top 3 distinct peaks) has low power at about 185 ppm.
    The search method will NOT be swapped. Peaks at 6.3992 d (S98) and 7.1322 d (S107) suggest the TOI-2514.01 mask (+-1.5 x 4.047 h / 2)
    leaks; widening it is a correctness fix to the registration's required mask. Any change is to be shown on these four sectors
    before/after.
174. 2026-10-24 14:15 UTC — TIC 317134140 scorer v1.1 (SHA-256 4c53a94be32f978a...): TOI-2514.01 mask widened from 1.5x to 2.5x of its half-duration;
    cadences removed are recorded. Four training sectors before (v1.0) -> after (v1.1):
      S6   PARTIAL -> PARTIAL       (127 +- 56 -> 118 +- 55 ppm; top 3 unchanged 0.9196, 5.1278, 3.3766)
      S87  INCONCLUSIVE -> INCONCLUSIVE (139 +- 83 -> 140 +- 86; 0.9114, 1.7238, 0.5327 -> 0.9114, 1.7238, 1.6652)
      S98  PASS -> PASS             (208 +- 32 -> 212 +- 34; 0.5717, 1.1428, 6.3992 -> 0.5717, 1.1434, 6.3992)
      S107 PARTIAL -> PARTIAL       (201 +- 56 -> 188 +- 56; 1.4295, 0.8499, 7.1322 -> 0.8583, 7.1322, 10.4333)
    The 6.3992-d and 7.1322-d peaks survive the wider mask, so they are not mask leakage (my hypothesis in item 173 is not supported).
    No outcome changed. The 2.5x mask is kept as declared. The search method and the clause definitions are unchanged.
    Pre-declared secondary readout (never the outcome): pooled S108-S110 depth = inverse-variance weighted mean of the per-sector
    clause-A depths, with its 95 % interval compared with [145, 225] ppm.
175. 2026-10-24 14:26 UTC — GAP3 locks (DECISIONS 172), before any test-sector data of these three stars. Not yet reviewed or published.
    (1) TIC 317134140: scorer v1.1 final (SHA-256 4a188827ce05ae13...; the only change since item 174 is that the
        light-curve hash is recorded first, so early refusals stay bindable; the four training outputs are re-run and identical).
        Eligibility check (advisor fix 2): ineligible training events are mostly ones with no in-transit data (gaps, edge trim, TOI
        mask: S6 5, S87 9, S98 33, S107 9). Only 2/1/7/4 per sector fail partial coverage or the out-of-transit count. The rule is kept.
        Configs 317134140_spoc_S108/S109/S110.json; each sector is scored separately, with no primary and no pooling. The pooled depth
        is a secondary readout only. Dated advance expectation and scoring amendment appended to results/vet/317134140/PREREGISTRATION.md.
    (2) TIC 80387959 (S111-S114) and 120517801 (S111-S113): two configs per sector, QLP (v2.1 rc4 + clock gate) and SPOC
        (scripts/prereg_conformance_spoc.py = conformance-v2.1-spoc1, SHA-256 c7e1b4cd43bac063...). It is v2.1 rc4 with only
        a SPOC product branch: file name, ORIGIN NASA/Ames, PDCSAP_FLUX, no QLP clock gate. The diff against v2.1 is in
        results/conformance_317134140/prereg_conformance_v2.1_to_spoc1.diff. The product of record is chosen by availability
        (item 172). S111 is the primary for both. Reference values use the generator rule (726 ppm / 2.2 h; 830 ppm / 2.2 h). Dated
        amendments are appended to both PREREGISTRATION_v2.md files.
    (3) Locks: configs/conformance/LOCK_2026-10-24_GAP3_QLP.json (1df553d7482cfece...; 7 configs; validate_round4_inputs.py)
        and LOCK_2026-10-24_GAP3_SPOC.json (ff565e9c08d7f126...; 10 configs; new
        scripts/validate_nonclock_inputs.py 20f73edbb43ae85f...). Generator: scripts/make_conformance_configs_gap3.py.
    (4) Tests: test_locked_configs.py on the QLP lock 182/182 (logs/test_locked_configs_GAP3_QLP_20261024.log); new
        scripts/test_spoc_configs.py 176/176 on artificial SPOC-format fixtures (logs/test_spoc_configs_GAP3_20261024.log). On the
        fixtures, 317134140's injected 185 ppm gives A_CONSISTENT in all three sectors and no signal gives FAIL.
        The first SPOC run had 7 failures. The test wrongly expected the v2.1-derived evaluator to refuse an existing output path;
        published v2.1 does not and relies on the result-stage binding. The check was restricted to the scorer.
    Next: external review, then the author's go, then v1.18 before SPOC S108 data appear.
176. 2026-10-24 14:38 UTC — TIC 317134140 scorer v1.2 (SHA-256 2e011c13aaa3ef69...) and the GAP3 locks regenerated. Not yet reviewed or published.
    (1) The S98 6.399-d peak. The TOI-2514.01 dip sits at its ephemeris phase within +-2 h in S6, S98 and S107 (detrended, unmasked
        profile), so the ephemeris and mask cover the TOI. The 6.3992-d BLS event (5 events, 2 h, 535 ppm) lies 58.8 h from the TOI
        phase: it is not the TOI and not mask leakage. It is unexplained, in-sample only, and no claim is made. It is noted in the
        advance expectation as an example of an unrelated peak that can occupy a clause-B slot.
    (2) Fidelity fix. The registration's own preparation (public scripts/blind_seasons_317134140.py:12, final_ephemeris_317134140.py:20)
        removes TOI-2514.01 cadences BEFORE detrending: trim_edges(t) & ~wotan.transit_mask(duration = 1.5 x 4.047 h), i.e. +-3.03 h.
        v1.0/v1.1 detrended first. v1.2 mirrors the original order and width exactly; the candidate is not masked, so the search stays
        blind. The 2.5x widening of item 174 is dropped: its motivation was disproven and it was not in the original.
        Training sectors, v1.0 -> v1.1 -> v1.2:
          S6 PARTIAL (127+-56 -> 118+-55 -> 127+-57), S87 INCONCLUSIVE (139+-83 -> 140+-86 -> 139+-81),
          S98 PASS (208+-32 -> 212+-34 -> 210+-32), S107 PARTIAL (201+-56 -> 188+-56 -> 199+-56). No outcome changed in any version.
          v1.2 top 3: S6 0.9196/5.1278/3.3766; S87 0.9114/1.7238/0.9347; S98 0.5717/1.1434/6.3992; S107 1.4295/0.8499/0.9891.
    (3) Bias check on artificial fixtures (2000 ppm white noise, 185 ppm injected, 8 seeds per sector): mean recovered depth
        190/188/182 ppm (S108/S109/S110), within 0.3 standard errors of 185. The quoted random-phase sigma (62-65 ppm) is slightly
        above the seed scatter (47-61 ppm). There is no bias. The single S108 fixture at 344 ppm (+2.5 sigma) is noise.
    (4) Availability rule tightened (advisor), now in every 80387959/120517801 config. The designation is made once per sector, at
        the first scoring attempt, from a saved MAST product-list query (timestamp + SHA-256) made before any light curve is opened.
        SPOC means a 2-min '*-s_lc.fits' (not TESS-SPOC FFI, not 20-s fast-lc). A later delivery of the other product is secondary only.
        My addition, to be confirmed by the author: if the star is on the sector's 2-min target list, no scoring attempt is made
        before the SPOC delivery or 120 days after the sector ends, whichever comes first. 317134140: no SPOC 2-min delivery within
        120 days -> the sector is recorded as UNAVAILABLE, with no substitute product.
    (5) The v1.1 configs and locks (never published) were moved to configs/conformance/superseded_gap3_v1.1_2026-10-24/ and their test
        logs to logs/superseded/. New locks: LOCK_2026-10-24_GAP3_QLP.json 2d2763d07f15342d...,
        LOCK_2026-10-24_GAP3_SPOC.json eb555d349c156b72....
        Tests: 182/182 (logs/test_locked_configs_GAP3_QLP_20261024b.log) and 176/176 (logs/test_spoc_configs_GAP3_20261024b.log).
        Today's unpublished amendment drafts were removed (the remaining text is byte-identical to the public copies) and re-appended
        with the v1.2 hashes.
177. 2026-10-24 14:44 UTC — Provenance before review (advisor). The 317134140 scorer now records version "1.2" and software versions (python,
    numpy, scipy, astropy, wotan via package metadata) in every output, like the v2.1 evaluator. The docstring and configs now state
    that every predicted row is a candidate event, the in_science_orbit column is not used, and eligibility is decided only by data
    coverage. No logic change: the four training outputs are identical. Scorer SHA-256 acfd7d34bb284485...
    Regenerated (unpublished v1.2a configs/locks archived in configs/conformance/superseded_gap3_v1.2a_2026-10-24/): LOCK_GAP3_QLP
    4578b11c4d046495..., LOCK_GAP3_SPOC d800792e49e9a301.... Tests 182/182 and 176/176
    (logs/*GAP3*20261024c.log). The amendments are written by scripts/amend_gap3_registrations.py, which resets each file to its
    public copy (refusing on any difference) and re-appends; it must not be run once these paragraphs are published.
    v1.18 assembly note: the superseded_gap3_* directories are not live configs. Bundle them only under a "superseded" label, or
    exclude them and cite DECISIONS 176(5)/177.
178. 2026-10-24 21:42 UTC — External review results/REVIEW_GAP3_configs.md: "locks sound after the listed changes; not ready to publish", with
    G1-G5 open after a re-check. Author's decisions (question tool, 2026-10-24):
    (a) G3, the product of record for 80387959 / 120517801: TARGET LIST AT SECTOR END. On each sector's end date, the sector's
        published 2-min target lists, including DDT lists, are saved with hashes. If the TIC is listed, SPOC is the product of record;
        otherwise QLP. If SPOC was designated but no SPOC 2-min light curve is delivered within 120 days of sector end, QLP becomes the
        product of record, decided on that date without opening any light curve. If no product exists within 365 days, the sector is
        UNAVAILABLE. This replaces the availability-at-first-attempt wording of items 172 and 176(4); the 120-day wait clause of
        176(4) is superseded.
    (b) Release split: v1.18 = the corrected TIC 317134140 package only, after a re-check and the author's go. The S111 material
        follows as v1.19.
179. 2026-10-24 21:50 UTC — Review G1-G5 addressed for TIC 317134140 (v1.18 package); the S111 material waits for v1.19 (item 178(b)).
    Scorer v1.3 (SHA-256 cd21f1fc10ff4315...). The clauses, thresholds, mask and search are UNCHANGED; the four training outcomes and
    depths are identical to v1.2 (results/conformance_317134140/insample_v1.3_S*.json, at the locked SHA).
    G1 (input validation): full time-header checks (TIMESYS TDB, TIMEREF SOLARSYSTEM, TIMEUNIT d, BJDREFI 2457000, BJDREFF absent or
        0); TICID/SECTOR parse errors, missing columns and unreadable files -> INVALID_INPUT; non-increasing or duplicate times ->
        INVALID_INPUT; usable = QUALITY 0, finite, error > 0. INSUFFICIENT when fewer than 10 cadences remain at any preprocessing step,
        when there are fewer than 10 eligible events or fewer than 100 usable random shifts, or when sigma is not finite and > 0. BLS
        is not run on INSUFFICIENT. The output now also records helper hashes and the top-3 epochs.
    G2 (release of record): new scripts/spoc_selection.py (c6685372fd8095ba...).
        - 'select' is metadata-only. It saves a MAST product list, its hash and the UTC time; the status is SELECTED only with exactly
          one SPOC 2-min s_lc.fits, otherwise AMBIGUOUS or NONE.
        - 'acquire' downloads exactly the selected dataURI and records its hash.
        - validate_nonclock_inputs.py (1933d8385acc8628...) gains a 'selection' stage. The 'result' stage
          requires both records: a MAST-query selection made after the lock; an acquisition of exactly that record and that file,
          made later; and the output from that file.
        - Live check on the in-sample S107 product: one candidate, and the download is byte-identical to the training file
          (results/conformance_317134140/selection_demo_S107/).
        - Limitation, declared: MAST lists only the current version, so a reprocessing that replaced the first delivery before our
          first check is undetectable. DATA_REL and the pipeline field are disclosed.
    G3: decided by the author (item 178(a)); it applies to the S111 material (v1.19).
    G4: the ordered outcome mapping is now written identically in the scorer, configs and registration. A complete truth-table test
        covers A_LOW+B_TOP3 -> FAIL and A_HIGH+B_TOP3 -> PARTIAL.
    G5: the scorer is now described as a dated operationalization of the qualitative frozen test, with its post-freeze numbers
        listed. Clause A is described as compatibility plus positive-depth evidence; 1.96 is nominal, with no established coverage.
        The registration text states that PARTIAL/INCONCLUSIVE are not confirmations and that FAIL is adverse evidence, not proof of
        absence. The preprocessing differences from prep() are listed: no candidate mask, PDCSAP errors, MAD over all retained points.
    CORRECTIONS (append-only):
        - Item 176(3) said "There is no bias". Read instead: "No bias was detected in this small idealized white-noise fixture check;
          it does not establish unbiased real-data depths or calibrated false-FAIL/PASS rates." Script and seed-level outputs are now
          scripts/fixture_bias_check_317134140.py and results/conformance_317134140/fixture_bias_check_v1.3.json (same means:
          189.5/187.9/181.8 ppm).
        - Item 177 said "the four training outputs are identical" at the final SHA. They were run at ce29f0fe; only S98 was re-run at
          acfd7d34. The SHA history is indexed in results/conformance_317134140/README.md.
    Lock configs/conformance/LOCK_2026-10-24_317134140.json (5dc86db2830fd672...; generator
    scripts/make_configs_317134140.py; UNAVAILABLE deadlines 2027-02-01 / 02-28 / 03-26). Tests scripts/test_317134140_lock.py:
    151/151 (logs/test_317134140_lock_20261024.log; validator refusal reasons spot-checked).
    Superseded and never published: all GAP3 v1.2a configs and locks, in configs/conformance/superseded_gap3_v1.2b_2026-10-24/.
    make_conformance_configs_gap3.py and amend_gap3_registrations.py are marked superseded and refuse to run. The 80387959 and
    120517801 registrations are reset to their public bytes until v1.19. Registration amendment: scripts/amend_317134140_registration.py.
180. 2026-10-24 21:51 UTC — The reviewed v1.2 scorer bytes were reconstructed for diffing. The copy is
    results/conformance_317134140/superseded_scorers/prereg_spoc_317134140_v1.2.py, and its SHA-256 equals the reviewed acfd7d34....
    Re-check prompt: results/PROMPT_recheck_317134140_v1.3.txt -> results/RECHECK_317134140_v1.3.md.
181. 2026-10-24 22:24 UTC — Re-check results/RECHECK_317134140_v1.3.md: "publish after listed changes" (R1-R4). Fixes:
    R1: scripts/spoc_selection.py (ed019dfe23ec461d...) has a single derive() of candidates/status/selected from the saved MAST rows. SELECTED
        needs exactly one candidate, a 'mast:' dataURI and its observation row; otherwise NONE, AMBIGUOUS or INCOMPLETE. The validator
        (f3bca6924c16216c...) recomputes the response hash from the saved rows and re-derives the summary, refusing any
        difference. The reviewer's cases are now tests: deleted rows with the old or a recomputed hash, two rows under a one-candidate
        summary, a missing dataURI. The saved S107 demo record re-derives identically.
    R2: timestamps are parsed strictly as UTC (malformed -> refused). Each config stores the exact cutoff, sector end + 120 days,
        inclusive: S108 2027-02-01T20:30:00Z, S109 2027-02-28T18:55:00Z, S110 2027-03-26T04:15:00Z, matching the reviewer's table.
        - A SELECTED record made at or before the cutoff permits scoring at any later time.
        - If no SELECTED record exists by the cutoff, the sector is UNAVAILABLE; a later listing is secondary only.
        - The validator refuses a first SELECTED record after the cutoff.
        - Checks are made at least weekly from sector end until SELECTED, plus a final check in the 24 h before the cutoff; all
          records, including NONE, are kept.
        - Tests: exact-cutoff binds, cutoff + 1 microsecond refused, timely selection with acquisition in 2028 binds, malformed
          query and download times refused.
    R3 CORRECTION to item 179 ("the clauses, thresholds, mask and search are UNCHANGED"), read instead: "The depth-compatibility
        boundaries, TOI mask and BLS search are unchanged. v1.3 tightens input/noise eligibility: at least 100 usable random shifts
        instead of 11, positive errors, and a strictly positive finite sigma. These guards did not change the four saved training
        outcomes." The training index (results/conformance_317134140/README.md) says the same.
    R4 CORRECTION to item 179's "sigma not finite and > 0", read: "sigma is nonfinite or <= 0". Fixed in the scorer docstring,
        generator, configs and registration. The release of record is described as "the eligible version listed at the first
        recorded check; an earlier replaced delivery cannot be excluded".
    Scorer docstring-only change: SHA-256 f3f55c0d74733f8a...; the training outputs are re-run at this SHA and identical
        (insample_v1.3b_S*.json).
    The first v1.3 lock and configs (never published) are archived in configs/conformance/superseded_317134140_v1.3a_2026-10-24/. New lock
        LOCK_2026-10-24_317134140.json 6ef9583863141fb5.... Tests: 178/178 (logs/test_317134140_lock_20261024b.log;
        no local paths); refusal reasons spot-checked. Registration amendment regenerated; the public prefix is intact.
182. 2026-10-24 23:41 UTC — Second re-check results/RECHECK2_317134140_v1.3b.md: "publish after listed changes" (two small items). Fixes:
    (1) spoc_selection.derive() (600e9504a811ac14...): a product-observation association needs a VALID obs_id (non-empty string, no
        surrounding whitespace, not None/null/nan/--/n/a) on the product and exactly one observation row with the same valid id;
        otherwise INCOMPLETE. Tests: absent, null, empty, whitespace, padded and 'None' ids on both rows, with the hash and summary
        regenerated -> INCOMPLETE and refused. The saved S107 demo record still re-derives identically.
    (2) Monitoring is now PROSPECTIVE (new config field monitoring_rule, repeated in the registration). It starts at the later of the
        lock's effective time and the sector end. Checks are weekly until the first SELECTED record, plus a final check within 24 h
        before the cutoff; every check is retained; the first eligible selected release is never replaced. It is periodic, not
        continuous monitoring. S108 ended before the obligation: no selection record for it was made before this lock, and the
        schedule is not claimed for that period. UNAVAILABLE means no SELECTED record by the cutoff, not that no archive product
        ever existed.
    (3) The training-index label for fixture_bias_check_v1.3.json now names its actual SHA, cd21f1fc, whose executable logic is
        identical to the current f3f55c0d (passing note).
    Scorer and validator are unchanged. The previous lock is archived in configs/conformance/superseded_317134140_v1.3b_2026-10-24/.
    New lock LOCK_2026-10-24_317134140.json 58df364513d9d2bd.... Tests 196/196
    (logs/test_317134140_lock_20261024c.log). Registration amendment regenerated; the public prefix is intact; the S111 registrations
    are still at their public bytes.
183. 2026-10-24 23:54 UTC — Third check results/RECHECK3_317134140.md: "publish as v1.18" (317134140 package only). v1.18 ASSEMBLED
    LOCALLY by scripts/assemble_v1_18.py (single pass; refuses to run twice).
    - The reviewed bytes are asserted: lock 58df3645..., scorer f3f55c0d..., validator f3bca692..., selector 600e9504...;
      tsearch.py, search_pipeline.py and blind_seasons_317134140.py are byte-identical to the published copies.
    - Content: scoring_317134140_s108_s110/ (configs + lock, 7 scripts, test log, design-sector outputs with the training index and the
      byte-exact v1.2 scorer, the S107 selection demo, README); the amended 317134140 registration; reviews_317134140/ (review + 3
      re-checks with path-only redactions, 4 prompts); README block; CITATION 1.18; public DECISIONS through item 182; MANIFEST_v1.18.md
      (59 files, all hashes verified).
    - Excluded and checked: S111 material, the SPOC evaluator variant, superseded drafts.
    - The 68 prediction CSVs and both S111 registrations are unchanged. No session link, job path or address appears in any changed
      file.
    - Release notes: zenodo_upload/RELEASE_NOTES_v1.18.md. Nothing is committed, pushed or uploaded; this waits for the author's go
      on the assembled bytes.
184. 2026-10-25 00:04 UTC — v1.18 PUBLISHED with the author's go for the assembled bytes (question tool: "Publish now as assembled").
    - Before commit: anchors matched (MANIFEST_v1.18.md aad32fc7..., RELEASE_NOTES_v1.18.md 300a41f2...); 59 manifest hashes passed;
      base 5037787.
    - Published: commit 1f81a4b2 (Co-Authored-By trailer, no session link); tag and GitHub release v1.18; Zenodo 10.5281/zenodo.23629288
      (GitHub integration, created 2026-10-24T23:57:36Z). The 317134140 S108-S110 lock now has a public timestamp.
    - Monitoring obligation started (monitoring_rule). First S108 metadata-only check at 2026-10-25T00:04:12Z: status NONE (0
      observations, 0 products), retained in results/selection_records/317134140/S108/. Next checks are due at least weekly. S109 checks
      start at its sector end (2026-10-31 18:55 UTC) and S110 checks at 2026-11-26 04:15 UTC. Acquisition and scoring need the author's
      go each time.
185. 2026-10-25 02:20 UTC — Author asked for (1) a real-noise calibration of the locked 317134140 scorer and (2) an interpretation plan
    for the S108-S110 outcomes. The INTERPRETATION RULE is fixed HERE, BEFORE ANY CALIBRATION TRIAL IS RUN (no calibration code
    exists at this time). Nothing in the v1.18 lock changes, whatever the calibration shows; low power is reported as low power.
    (a) Hypotheses. H1: a periodic ~185 ppm, 1.5-h dip at the frozen ephemeris is present in the test sector. H0: no such dip; only
        this star's noise. H1 is satisfied equally by a planet and by a blended eclipsing binary. The plan concerns PERSISTENCE of
        the signal, not its origin, and no outcome yields "validated" or "confirmed planet".
    (b) Calibration that feeds the table, declared before it is run:
        - Data: the training sectors with the real signal divided out using the registration's transit shape.
        - H1 trials inject that shape at random periods P' in [0.53, 0.70] d (excluding |P'/P - 1| < 2 %, the P/2 and 2P aliases
          and the TOI-2514.01 harmonics) and random phases. Depth is defined as clause A measures it: the noiseless model's mean
          in-transit depth over +-0.75 h against the out-of-transit median equals 185 ppm. a/R* is scaled with P' to hold
          T14 = 1.5 h.
        - Scoring uses the locked v1.3 functions with the period constant set to P'.
        - H0 trials are the same cleaned data with no injection, scored at random P' and phases.
        - Trials: N >= 100 H1 trials per sector at 185 ppm (plus 50 each at 130 and 240 ppm, sensitivity only); N >= 2000 H0
          trials per sector.
        - Harness control: P' = P at the frozen phase on unsubtracted data must reproduce insample_v1.3b_S*.json field for field,
          or the calibration is not used.
    (c) Per-sector likelihood ratio for each outcome label L: LR(L) = P(L|H1) / P(L|H0), each estimated as (k + 1/2) / (N + 1).
        The S108-S110 table pools the three single-sector training sectors (S6, S87, S107) at 185 ppm. S98 is two sectors long and is
        reported separately, not used, because S108-S110 are single ~27-d sectors.
    (d) Combination: the product of the per-sector LRs over S108, S109 and S110, treated as independent. INSUFFICIENT, UNAVAILABLE and
        INVALID_INPUT contribute LR 1.
    (e) Verbal conclusion on the combined LR:
        - > 10: strong evidence that the signal persists;
        - 3 to 10: moderate evidence that it persists;
        - 1/3 to 3: inconclusive;
        - 1/10 to 1/3: moderate evidence against persistence;
        - < 1/10: strong evidence against persistence.
        Boundaries belong to the less extreme category.
    (f) The per-sector frozen outcomes remain the outcomes of record. The combined LR and its verbal conclusion are the declared
        interpretation. The pooled depth stays a secondary readout and plays no part in it. The trials share one noise realization
        per sector, so binomial uncertainties understate the true uncertainty; this is stated with the table.
    (g) Publication needs the author's go: a small release (calibration, plan and its review), intended before any S108 data.
186. 2026-10-25 02:31 UTC — Calibration run and interpretation plan written (rule DECISIONS 185, logged before any trial).
    - Harness scripts/calibrate_317134140_scorer.py (63738417451a42d2...). It imports the locked v1.3 functions
      (SHA asserted) and sets only the period constant per trial. All four controls (P' = P, frozen phase, unmodified file) reproduce
      insample_v1.3b field for field.
    - Real signal divided out with the registration shape (180.4 ppm by the clause-A measure). Residual at the true ephemeris: S6
      -47 +- 62, S87 -38 +- 86, S98 +31 +- 25, S107 +20 +- 50 ppm.
    - Output results/conformance_317134140/calibration_v1.3.json (d2c5b2ec162d9509...): 400 H1 trials at 185 ppm, 200 each at 130 and
      240 ppm, 8000 H0 trials; log logs/calibrate_317134140_20261025.log; runtime about 9 min.
    - Pooled table (S6 + S87 + S107, 185 ppm):
        H1 (300 trials): PASS 93, PARTIAL 175, INCONCLUSIVE 30, FAIL 2.
        H0 (6000 trials): PASS 0, PARTIAL 107, INCONCLUSIVE 846, FAIL 5047.
        Per-sector LR: PASS 3.73e3 (a bound: zero H0 counts), PARTIAL 32.5, INCONCLUSIVE 0.718, FAIL 0.00987.
        Of the 35 order-free combinations, 21 give strong support, 7 strong evidence against, 5 inconclusive and 2 moderate against.
        S98 (not used): PASS 71 of 100.
    - Depth sensitivity (reported, NOT used; added AFTER the calibration was seen, as disclosure only): at 130 ppm, H1 gives PASS 10,
      PARTIAL 82, INCONCLUSIVE 37, FAIL 21 of 150, so LR(FAIL) = 0.169. Nine of the 35 combinations would change category, all with a
      FAIL or several INCONCLUSIVE. The declared rule is NOT changed. Whether to adopt a depth-robust rule before S108 data is an author
      decision.
    - Table: scripts/interpret_317134140_table.py -> results/conformance_317134140/interpretation_table_v1.3.json / .md
      (db092d38d9955345...).
    - Registration: dated interpretation plan appended by scripts/amend_317134140_plan.py, which requires the v1.18 published bytes as
      its prefix (verified).
    - Not published; it awaits review and the author's go (a small release, intended before any S108 data).
187. 2026-10-25 02:46 UTC — Review results/REVIEW_317134140_calibration_plan.md: "publish after listed changes". The author relayed it
    as "no go as written; the calibration does not justify the combined strong-evidence claims". Accepted in full.
    WITHDRAWN (dated, after seeing the calibration and its review; no test photometry examined): the formal combined interpretation
    of item 185(c)-(e), i.e. the per-sector likelihood ratios, their product and the verbal "strong / moderate evidence" scale, and
    the interpretation-table lookup built on them. Reason (review, major):
    - The H0 design cannot produce PASS. Each sector's noise-only BLS top 3 was fixed, and no allowed trial period could hit it: S6
      peaks 0.9196 / 5.2435 / 6.4131 d and S107 0.8499 / 1.1329 / 7.1361 d lie outside 0.53-0.70 d; S87's 0.5327 d lies in the
      excluded TOI/12 band. So 0 PASS in 6000 is a structural zero, not an estimate, and the pseudocount ratio 3728 is neither
      a bound nor a calibrated likelihood ratio.
    - Combining pooled plug-in rates as known probabilities for independent future sectors is also unsupported.
    The superseded table files (interpretation_table_v1.3.*) are retained as withdrawn history. The unpublished plan paragraph was
    removed from the registration (reset to the v1.18 published bytes); scripts/amend_317134140_plan.py is marked superseded.
    REPLACEMENT (descriptive only): the calibration is released as conditional injection/null DIAGNOSTICS of three selected training
    noise realizations (plus S98, separately). The frozen per-sector outcomes remain the outcomes of record. For each test-sector
    outcome we will report its conditional frequencies in these diagnostics at all three depths (130, 185 and 240 ppm). No
    quantitative combined evidential-strength conclusion is adopted from this calibration. A predictive calibration (variation between
    noise realizations, null BLS peaks able to hit) would need its own design, declared before it is run and before any test
    photometry; none is planned now.
    CORRECTIONS:
    - Duration: a/R* proportional to P' only approximately holds the duration. The injected geometric T14 was 1.554-1.584 h; 1.5 h
      is the scoring window, not the injected T14. Items 185(b) and 186 and the calibration docstring are corrected; the run is not
      relabelled. The script that ran has SHA-256 63738417...; only its docstring changes now.
    - Controls: the eleven listed scientific fields matched insample_v1.3b. This was not a complete equivalence of every output and
      validation path.
    - Chronology: the author logged the rule as fixed at 02:20 UTC (item 185). Local timestamps (calibration script created 02:21:08
      UTC, output 02:30:23 UTC) are consistent with that account; the mutable log cannot itself prove when the item was inserted.
    - Depth sensitivity of the withdrawn table, for completeness: 9 of 35 combinations change category at 130 ppm, 12 at 240 ppm;
      19 of 35 agree at all three depths.
    - INSUFFICIENT counting as LR 1 was a convention, not an established equality (moot after the withdrawal).
188. 2026-10-25 02:48 UTC — Replacement material for item 187, not yet published:
    - scripts/calibration_diagnostics_317134140.py (fb41795ecc55d4ac...) ->
      results/conformance_317134140/calibration_diagnostics_v1.3.json (fb7b9d407263cd40...) / .md: conditional frequencies only.
      The structural zero is checked explicitly: in none of S6, S87, S98, S107 can an allowed noise-only trial period reach a fixed
      BLS peak. The injected T14 is 1.554-1.584 h, matching the reviewer's independent figures.
    - The registration was reset to the v1.18 bytes, then scripts/amend_317134140_diagnostics.py appended the dated DESCRIPTIVE
      calibration note, using the reviewer's suggested central wording. The v1.18 prefix is intact.
    - The training index has a calibration section. Superseded and withdrawn: interpret_317134140_table.py and its outputs;
      amend_317134140_plan.py (refuses to run).
189. 2026-10-25 03:04 UTC — Re-check results/RECHECK_317134140_calibration.md: "publish after listed changes" (presentation only;
    scientific corrections pass; all 240 counts and the structural zero reproduced exactly). Fixes:
    (1) The withdrawn tables are now self-labelled. interpretation_table_v1.3.md has a WITHDRAWN header and title; the .json has
        WITHDRAWN/status/replacement as leading keys. Both name DECISIONS 187, the replacement diagnostics and their original SHA-256
        (md d5ec8f26..., json db092d38...). The historical numbers are kept.
    (2) Calibration-script docstring, documentation-only:
        - chronology: "the author logged the rule as fixed at 02:20 UTC; local timestamps are consistent with that account, but do not
          independently prove insertion time";
        - control: "for the eleven scientific fields listed in the control comparison"; the saved output's 'field for field' control
          string overstates in the same way.
        The non-docstring AST is identical to the as-run source (SHA-256 63738417...). The reviewer's byte-exact reconstruction is
        kept as results/conformance_317134140/calibrate_317134140_scorer_as_run.py.
    (3) Non-blocking note taken: the structural-zero check now uses the exact interval test in the scorer's ratio direction. The
        diagnostics outputs are byte-identical (json fb7b9d40..., md 3d195858...), so the registration note's cited hash stands.
    Current script hashes: calibrate cde10a021d79c56b..., diagnostics b0a884bb4aa7b6f0....
190. 2026-10-25 03:05 UTC — v1.18.1 ASSEMBLED LOCALLY by scripts/assemble_v1_18_1.py.
    - Content: scoring_317134140_s108_s110/calibration/ (raw trials, descriptive diagnostics, the as-run calibration source, the log,
      scripts, README; withdrawn/ holds the self-labelled LR draft and superseded scripts with a notice); the registration with the
      dated calibration note; the calibration review and re-check, path-only redactions; the design-sector index; README block;
      CITATION 1.18.1; public DECISIONS through item 189; MANIFEST_v1.18.1.md (23 files, verified).
    - Asserted: the v1.18 configs and scorer are unchanged.
    - The first attempt stopped on an over-strict path check: DECISIONS.md's published v1.15 prefix carries temporary paths that
      were already disclosed. The partial changes were reverted file by file (the tree was clean at 1f81a4b), the check was limited
      to the text after that prefix, and the assembly was re-run.
    - Release notes: zenodo_upload/RELEASE_NOTES_v1.18.1.md. Nothing is committed, pushed or uploaded; this awaits the author's go.
191. 2026-10-25 03:52 UTC — v1.18.1 PUBLISHED with the author's go for the assembled bytes (question tool).
    - Anchors matched: MANIFEST_v1.18.1.md 9828bc59..., RELEASE_NOTES_v1.18.1.md 1d6b994b...; 23 manifest hashes passed.
    - Published: commit f3233b31 (Co-Authored-By trailer, no session link); tag and GitHub release v1.18.1; Zenodo
      10.5281/zenodo.23632740 (created 2026-10-25T03:51:39Z). The calibration and the withdrawal of the combined-LR draft are now
      public before any S108-S110 data of this star.
192. 2026-10-25 04:21 UTC — v1.19 S111+ package built for TIC 80387959 (S111-S114) and 120517801 (S111-S113). The author's "do it" was read
    as this package, not as a ground-photometry procedure. Not yet reviewed or published.
    - Designation tool scripts/target_list_designation.py (7fc6424788ed5a9f...), metadata only; the author's rule 178(a).
        Snapshot: the official orbit table, every all_targets_S<N>_v<k>.csv (probed to the first 404, since the index is forbidden),
          and the DDT page with every linked CTL, all with saved bytes and hashes.
        Sector end: the latest End of Orbit of sector N, accepted only when the table also lists N+1; otherwise PENDING (the
          current table lists only part of S111).
        Designation: listed in any saved list or CTL -> SPOC, else QLP. A single derive() is re-run by the validator.
        Fetching uses the system curl with TLS verified: the venv's Python OpenSSL plus certifi fails on tess.mit.edu's chain.
        Live demo S108 (results/designation_records/demo_S108/): 317134140 -> SPOC, 24526743 -> QLP; end 2026-10-04T20:30Z; SPOC
          cutoff 2027-02-01T20:30Z, equal to the v1.18 cutoff; re-derives identically.
    - Configs (scripts/make_configs_s111.py): 7 QLP (published v2.1 rc4 evaluator, clock gate) + 7 SPOC (prereg_conformance_spoc.py,
      unchanged at c7e1b4cd...). They carry the designation rule, a prospective monitoring rule and the dilution note (one reference
      depth for both products; never rescaled). Reference values 726 ppm / 2.2 h and 830 ppm / 2.2 h; primary S111.
      Locks: LOCK_2026-10-25_S111_QLP.json 561985662ebf9d68... and LOCK_2026-10-25_S111_SPOC.json 0ec46bcc3f6f2cc1....
    - New validator scripts/validate_s111_inputs.py (ac58df5f44a9a4ba...), stages pre / designation / selection / result:
        it re-derives the designation;
        QLP by fallback needs a re-derived NONE selection record made at or after the SPOC cutoff;
        the SPOC selection must be made by the cutoff.
      validate_nonclock_inputs.py and prereg_conformance_spoc.py are untouched. QLP clock/result stay with validate_round4_inputs.py.
    - Tests: scripts/test_s111_lock.py 280/280 (logs/test_s111_lock_20261025.log, artificial only); test_locked_configs.py 182/182 on
      the QLP lock. Refusal reasons were spot-checked; one case that first passed for the wrong reason (old snapshot refused as
      PENDING) was fixed in the fixture.
    - Amendments appended to both PREREGISTRATION_v2.md files (scripts/amend_s111_registrations.py); published prefixes intact.
    - Observation: the live DDT page (fetched 2026-10-25 ~04:00 UTC) lists DDT 001-099 only; DDT 100-102 reported by the monitoring
      bot are not on it.
193. 2026-10-25 04:39 UTC — Review results/REVIEW_S111_package.md: "publish after listed changes; hold v1.19" (S111-1 to S111-4 blocking:
    failed metadata read as "unlisted"; version and DDT scope; fallback history; designation before acquisition; S111-5 a test defect).
    Author's decisions (question tool, 2026-10-25), refining 178(a) after this review and before any S111 data exist:
    (a) DDT SCOPE: only the sector's published 2-min target lists (all_targets_S<N>_v<k>.csv) decide listing. They already
        concatenate the approved DDT targets. DDT target lists carry no sector and are saved as context only. This is the literal
        reading of 178(a); the broader CTL trigger of item 192 is dropped.
    (b) FALLBACK BASIS: SPOC stays the product of record if any retained check, including one after the cutoff, finds a SPOC 2-min
        light curve whose MAST release date (t_obs_release) is on or before sector end + 120 d. Otherwise QLP. The first selected
        qualifying release is irreversible. This replaces "delivered within 120 days" with the MAST release date, the only
        observable delivery evidence.
    (c) TIMING: the first successful, COMPLETE designation snapshot at or after the published sector end decides; checks are at least
        weekly. Failed, malformed or incomplete fetches are retained as PENDING and retried, never read as "unlisted". The accepted
        snapshot and its sector end are fixed before any flux of either product is acquired; later metadata cannot replace them.
        This clarifies 178(a)'s "on the sector's end date".
    Item 192's package is superseded before publication; it will be rebuilt as v1.19b and re-checked.
194. 2026-10-25 04:43 UTC — Two further author decisions (question tool), before any S111 data and before the rebuild code is written:
    (a) FALLBACK FINALITY: the QLP fallback is CERTIFIED by two complete SPOC checks made at or after the SPOC cutoff, at least 7 days
        apart, both finding no qualifying release (no SPOC 2-min light curve with MAST release date <= end + 120 d). It becomes FINAL
        when QLP flux is acquired under it (ledger order). A qualifying SPOC release found later is recorded and reported as a
        secondary readout only, never a re-designation. Until QLP flux is acquired, a qualifying SPOC release found by any retained
        check makes SPOC the product of record (item 193(b)).
    (b) AMBIGUOUS / INCOMPLETE: if SPOC checks after the cutoff are AMBIGUOUS (two or more eligible files) or INCOMPLETE (no usable
        dataURI, observation row or release date), the product of record is UNRESOLVED. It is reported with no outcome of record,
        and both products are secondary readouts. A later complete check before any acquisition can resolve it, either by a
        qualifying SELECTED or by contributing to the two-check fallback certification.
    Declared conventions for the rebuild:
    - The MAST release date is t_obs_release, read as MJD (MJD 0 = 1858-11-17 00:00 UTC). A missing or non-numeric value never
      qualifies. Whether reprocessing changes t_obs_release is not established.
    - The "final check within 24 h before the cutoff" clause is dropped; under the release-date rule it has no evidential role.
    - No flux of either product is acquired before the route is settled.
    - The same release-date logic applies to the 365-day rule. QLP v01 with release date <= end + 365 d is the product of record
      on the QLP route. A complete QLP check at or after end + 365 d with none, recorded as a disposition entry, makes the sector
      UNAVAILABLE, and that is final.
195. 2026-10-25 04:53 UTC — v1.19b rebuild of the S111+ package after review S111-1 to S111-5, implementing items 193-194. Not yet re-checked
    or published.
    - Designation tool v2 scripts/target_list_designation.py (c66f3a774202e378...):
        required sources are the orbit table and target-list versions v1-v9, ALL probed (bounded and declared);
        any non-200/404 status, curl failure, malformed body, wrong orbit-table header, missing N+1 row, all-404 lists, or a
        snapshot before the end gives PENDING with the reasons, never "unlisted";
        DDT page and lists are context only.
      The reviewed v1 is archived in results/conformance_s111/superseded_v1.19a/. S108 demo re-run with v2
      (results/designation_records/demo_S108_v2/): same designations, end and cutoff; all nine versions probed.
    - New scripts/qlp_selection.py (6c52378495fe8989...): the QLP counterpart of spoc_selection.py (unchanged), release of record
      v01 with MAST t_obs_release. Live in-sample check (80387959 S100) SELECTED.
    - New ledger scripts/s111_ledger.py (089f6c68fc5ad482...): append-only, hash-chained, per TIC/sector, with the entry types
      designation_snapshot, spoc_check, qlp_check, acquisition and disposition. Forbidden entries are refused at append time.
      replay() implements items 193-194:
        the first DESIGNATED snapshot is operative, with frozen cutoffs;
        the release-date rule (MJD) with the first qualifying selection irreversible;
        two clean checks >= 7 d apart certify the fallback, and the QLP record acquisition makes it final;
        AMBIGUOUS / INCOMPLETE after the cutoff -> UNRESOLVED;
        UNAVAILABLE needs a complete QLP check after end + 365 d and is final;
        no acquisition before a settled route.
    - Validator v2 scripts/validate_s111_inputs.py (4b2312590e81647d...), stages pre / route / result, replays the ledger.
      QLP results also need validate_round4_inputs.py, and the output says so.
    - Configs regenerated with the item 193-194 rule text; the 24-hour final-check clause is dropped. The v1.19a configs and locks
      (never published) are archived in configs/conformance/superseded_s111_v1.19a_2026-10-25/.
      New locks: LOCK_2026-10-25_S111_QLP.json e0bd156031edafc3..., LOCK_2026-10-25_S111_SPOC.json 54f6aa2a00d2c893...; both bind the designation,
      both selection tools and the ledger.
    - Tests: scripts/test_s111_lock.py v2, 150/150 (logs/test_s111_lock_20261025b.log). It drives the real snapshot() with a mocked
      fetch and clock, and every negative case asserts its refusal reason (S111-5). test_locked_configs.py on the QLP lock: 182/182.
    - Registrations reset to their published bytes and re-amended (prefixes intact).
196. 2026-10-25 04:57 UTC — Pre-review hardening of v1.19b (advisor), regenerated as the current package:
    (1) Each ledger is now bound to BOTH locks by SHA-256. s111_ledger.py init takes --lock-qlp and --lock-spoc and records both hashes;
        the validator requires this lock's hash. A ledger initialised against an edited lock copy is refused (tested).
    (2) Replay allows at most ONE record acquisition per ledger. Secondary acquisitions are refused while the route is unsettled
        and accepted after it settles. An AMBIGUOUS QLP check after end + 365 d does not allow UNAVAILABLE. All three are tested.
    (3) Generator docstring: "--stage designation" corrected to route/result.
    (4) Disclosure in the QLP release_rule and the amendments: only v01 is a release of record, so a v02-only listing leads to
        UNAVAILABLE (as for the v1.17 locks).
    Hashes: s111_ledger.py c444bca837a6d289..., validate_s111_inputs.py a2e78bded6072e16...; locks QLP 3f2000a626a8245d..., SPOC f3a1bc7bcbae5856....
    The v1.19b configs and locks (never published) are archived in configs/conformance/superseded_s111_v1.19b_2026-10-25/.
    Tests: 162/162 (logs/test_s111_lock_20261025c.log) and 182/182 (logs/test_locked_configs_S111_QLP_20261025c.log). Registrations
    re-amended; prefixes intact. The S108 v2 demo still re-derives.
197. 2026-10-25 13:52 UTC — Re-check results/RECHECK_S111_package.md: "publish after listed changes" (R1-R5). Fixes, regenerated as v1.19d (not published):
    R1: an unresolved SPOC check (AMBIGUOUS, or INCOMPLETE including an unusable release date) at or after the cutoff now makes the
        route UNRESOLVED even after certification, as item 194(b) says. A later qualifying selection or a new two-check certification
        resolves it; only a final fallback is immune. The contrary docstring sentence is removed.
    R2: checks recorded before the operative designation are kept and, once it fixes the cutoffs, evaluated in ledger order under
        the same rules: a prior qualifying SPOC selection keeps SPOC, and a prior qualifying QLP selection blocks UNAVAILABLE and is
        the release of record.
    R3: a secondary acquisition must be of the OTHER product than the route's, and must reference a SELECTED check of that product in
        the same ledger (same dataURI and file name). A same-product "secondary" can no longer avoid finality.
    R4: release dates are usable only if finite and 0 < MJD < 200000; otherwise unusable, without a crash. replay() turns any parsing
        failure into a refusal. append() validates on a temporary copy first, so refused appends leave the ledger bytes unchanged
        (tested byte-exact). An HTTP 200 with an empty body (target list or orbit table) gives PENDING.
    R5: the generator docstring now describes the current rule. The monitoring sentence uses the reviewer's wording ("A later check
        can recognize a timely release if it remains listed ... earlier replaced deliveries cannot be excluded ...").
    QLP receipt: kept as two BOUND outputs plus the identifiable artifacts (config, light curve, evaluator JSON, clock record, ledger
    at its validated tip, lock and code hashes), which the reviewer judged sufficient.
    Hashes: s111_ledger.py ab5373e900ce9d59..., target_list_designation.py f91b9be2174438e2..., validate_s111_inputs.py a2e78bded6072e16...; locks
    QLP 3545a827b3191150..., SPOC 9b0095f6d47263f7....
    The v1.19c configs and locks (never published) are archived in configs/conformance/superseded_s111_v1.19c_2026-10-25/; the previous
    tool versions are in results/conformance_s111/superseded_v1.19a/.
    Tests: 196/196 (logs/test_s111_lock_20261025d.log) and 182/182 (logs/test_locked_configs_S111_QLP_20261025d.log). Registrations
    re-amended; prefixes intact. The S108 v2 demo still re-derives.
198. 2026-10-25 15:15 UTC — Second re-check results/RECHECK2_S111_package.md: R1-R5 fixed; one blocker remained (concurrent appends could commit a
    record validated against an older ledger state). Fix, regenerated as v1.19e (not published):
    - s111_ledger.py append() is now a serialized transaction.
      - Lock: an exclusive per-ledger writer lock (fcntl.flock on DIR/.writer.lock) is held from reading the history through the
        commit; a second writer waits.
      - Staging: the source record is staged ONCE, and the candidate history built from it is fully replayed. A refusal writes
        nothing live.
      - Commit: the validated bytes are placed under a temporary name and renamed, then ledger.jsonl is replaced atomically
        (os.replace). Readers see the old or the new history only. An unreferenced leftover of an interrupted commit is replaced
        under the lock.
      - Test hook: an opt-in hook (S111_LEDGER_PAUSE_AFTER_STAGE), inactive unless set, schedules interleavings for the tests.
    - Tests (scripts/test_s111_lock.py, section T), deterministic:
      - a second writer waits while the first holds the lock;
      - nothing is committed during the pause;
      - the committed bytes are the staged ones even after the source file is altered;
      - a later-dated second writer commits after the first;
      - an earlier-dated second writer is refused cleanly, with nothing written;
      - no partial files remain;
      - an interrupted-commit leftover is replaced.
      Suites: 209/209 (logs/test_s111_lock_20261025e.log) and 182/182 (logs/test_locked_configs_S111_QLP_20261025e.log).
    - CORRECTION to item 197: "refused appends leave the ledger bytes unchanged" held only for sequential writers. It now holds for
      concurrent writers as well, by serialization.
    Hashes: s111_ledger.py 16b987ac0cc8b116...; locks QLP d3f2d0ed93e7db2c..., SPOC a88d676e745d247f....
    The v1.19d configs and locks (never published) are archived in configs/conformance/superseded_s111_v1.19d_2026-10-25/; the v1.19d
    ledger is in results/conformance_s111/superseded_v1.19a/s111_ledger_v1.19d.py. Registrations re-amended; prefixes intact.
