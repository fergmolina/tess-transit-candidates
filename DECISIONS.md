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
