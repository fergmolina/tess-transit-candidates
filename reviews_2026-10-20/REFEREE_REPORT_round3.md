# Referee report, round 3: four new TESS candidates

Referee: independent adversarial review (Claude agent), 2026-10-19 local / 2026-10-20 UTC.
Scope: TIC 206620592, 122522485, 283913390, 196514928.
The referee edited no project files. All temporary scripts are in the session scratchpad
(`/private/tmp/claude-501/.../scratchpad/code/`: `recompute.py`, `extra.py`, `refit.py`, `refit_robust.py`, `vz.py`; downloads in `scratchpad/dl/`).

## 0. Must-fix items (all objects)

1. **The S106 test is not "data not public at freeze" (206620592, 122522485).** `Tesscut.get_sectors` lists S106 for both stars, and S107/S108 for 122522485. I downloaded a 1x1 S106 TESScut cutout for 206620592 (`scratchpad/s106/tess-s0106-1-2_..._1x1_astrocut.fits`, 10,982 cadences, BTJD 4233.43-4261.88, header DATE 2026-08-13). I did **not** look at its flux. The project also had S106 and S107 SPOC 2-min light curves of other stars on disk from 2026-10-17 (`data/lc/tess2026192185000-s0106-*`, mtime Oct 17), before the freeze at 2026-10-20 00:33 UTC. The status label comes from a manual flag (`scripts/prereg_v2.py` line 101, `--unreleased-sectors`), not from a release check. I found no local S106 files for these four TICs, so the predictions may still have been made without seeing the data. But the CSV/PREREGISTRATION wording "data not public at freeze" is false. The S106 tests must be described as "public FFI data, not analysed before the freeze", and that claim now rests on process, not on the data being unavailable. The frozen files cannot be changed, so a dated erratum is needed, like the 2026-10-20 timing clarification. Check S109/S111 availability (196514928, 283913390) the same way before calling those tests blind.
2. **283913390 "5/5 years" is a double count** (the round-2 error again). Only three sectors exist (S7, S33, S87: `report.json` `per_sector`, and only three QLP files in `data/qlp_allsky`). S33 (Dec 2020 to Jan 2021) and S87 (Dec 2024 to Jan 2025) each cross New Year, so `per_year` splits them into 2020+2021 and 2024+2025. `vet_summary.png` shows 5 colours from 3 sectors. The correct count is **3 independent sectors**, and the 2021/2024 "blind tests" are not independent: their training sets contain the other half of the same sector. `results/allsky_round3_outcomes.csv` (`years 5/5`) and `allsky_round3_triage.csv` must be corrected.
3. **None of the four passes the project's TRICERATOPS thresholds** (FPP < 0.015, NFPP < 1e-3; `triceratops.json`): FPP 0.032 / 0.075 / 0.045 / 0.043. NFPP 7e-9 / **0.0082 / 0.025 / 0.0068**. Every "candidate" label needs an explicit "unvalidated; fails FPP threshold; blend not excluded" caveat. 160330868 was downgraded to "weak" for FPP 0.38. That is a different degree, but the outcomes table should state the rule it uses.
4. **The timing errors per sector are 2-10x too small** (all objects). The `tc_err` values (1.2, 2.4, 3, 4.2 min...) sit on the 1.2-min grid of the timing scan. I injected boxes of the measured depth at random phases into the same detrended data (`extra.py`, 40 injections per sector) and recovered times with an rms of 4-37 min, with 0-23% of recoveries off by more than 30 min. This alone explains the 122522485 chi2/dof = 93/3 (Section 2). The frozen sigma_pred values for 206620592 (1.4 min) and 283913390 (5.7 min) are overconfident. The 30-min floor of the governing rule max(3 sigma, 30 min) (verified in `scripts/prereg_test.py` line 47, and `results/CLARIFICATION_TIMING_RULE_2026-10-20.md`) rescues them in practice, except possibly 283913390 (Section 3).
5. **The quoted SNRs are white-noise SNRs.** With an empirical red-noise null (box depth at 300 random phases per sector, `recompute.py`), per-sector SNRs combine in quadrature to about **7.1 / 7.3 / 11.2 / 11.8**. The project quotes 10.1 / 10.0 / 9.4 / 12.2. Under the project's own "SNR < 9 means weak" cut, 206620592 and 122522485 would be weak by this metric. Report both numbers.
6. **Radii use DET_FLUX depths**, against the project rule. The SAP depths in `allsky_round3_outcomes.csv` give Rp scaled by sqrt(SAP/DET). 122522485: 1.05 → about 1.14 R_E (229 vs 193 ppm). The others change by 3% or less.

## 1. TIC 206620592 (P 1.08567 d, ~240-290 ppm, ~1.0 R_E, M dwarf T 9.9, d ≈ 34 pc)

**Recommendation: candidate (unvalidated; low red-noise SNR).** It has the cleanest false-positive profile of the four, but the signal is weak.

Novelty (nothing prior found; all hits checked):
- ExoFOP TOI CSV (8151 rows) and CTOI CSV (5138 rows), downloaded 2026-10-19 from the URLs in the brief: no match. NASA Exoplanet Archive TAP `toi` table: no match. ExoFOP target JSON (`target.php?id=206620592&json`): no TOI, CTOI, files or follow-up.
- SPOC TCEs: MAST shows SPOC 2-min only in S28 and S68, and no DV products. Bulk TCE stats files (`archive.stsci.edu/missions/tess/catalogs/tce/`) for s0028, s0068, s0027, s0069, and the multi-sector runs s0001-s0036/39/46/65/69/92/96 contain no row for this TIC. SPOC never made a TCE. That fits a real signal with per-sector SPOC SNR of about 2-4 (my PDCSAP S28 164±48, S68 155±64 ppm), well below MES 7.1. It is not evidence against the signal.
- `scripts/prior_grep.py`: (a) **mkunimoto/LEO-Vetter `tutorials/scr_subset.csv`** lists this TIC at P = 11.6858 d, depth 390 ppm, MES 10.0, 4 transits. This is the *scrambled-data* (false-alarm) training subset (`5_Optimize_Thresholds.ipynb`, `scr_FA`), at a different, non-harmonic period (11.686/1.0857 = 10.76). It is not a report of this signal, but disclose it. (b) break-the-build/astrosearch target-ranking CSVs and paraschopra/tess-planet-candidates `targets_ranked.csv` are target lists only. The paraschopra `phase2/triage.csv` and `phase3/inverted_triage.csv` have no row. (c) GitHub code search: plain-number hits are tessgi/TessGiWebsite `approved-programs/cycle5/G05121.txt` (a GI target list, which explains the S68 2-min data) plus unrelated noise. The quoted "TIC 206620592" / "TIC206620592" / "TIC-206620592" searches return 0. Zenodo API (quoted and unquoted, all versions): 0.
- VSX, Gaia DR3 variability (I/358/vclassre) within 60": none. SIMBAD: PM J22478-3351, no object type.

Signal checks:
- 10-min-binned QLP SAP BLS over 0.5-6 d (`extra.py`): the top peak is 1.08568 d, SDE 14.1, rank 1. It is seen in each sector: QLP SAP S28 339±60, S68 197±51, S96 233±110 ppm (red-noise errors). Combined red-noise SNR is about 7 (vs 10.1 claimed).
- SPOC 2-min S28/S68 are re-extractions of sectors already counted in the QLP data. They are an extraction check, not extra detections. They are weak (PDCSAP SNR 3.4 / 2.4).
- Odd/even: mine is 128±45 vs 318±67 (about 2.3σ; project 1.75σ). In a 2P test the deeper half swaps between sectors (QLP S28: B deeper; S68/S96: A deeper; SPOC S28: A deeper, against QLP S28). With P_err × 1700 epochs ≈ 0.001 d the parity bookkeeping is reliable, so the asymmetry is not stable. This argues against an EB at 2P. TRICERATOPS EBx2P is about 3e-12.
- No secondary at phase 0.5 (−82±47 ppm, a brightening). Density check: rho_fit/rho_TIC = 0.91, consistent.
- Blind tests: the 2023 holdout gives stacked SNR −0.7, because the training-set period (1.08504) is wrong by 6.7e-4 d. That is an ephemeris failure, not absence of the signal. The 2020 holdout's training search peaks at 2P (2.1713). Treat the blind tests as weak support only.
- The `inverted_null` inverted-data top SNR (11.9) is higher than the real SNR (9.5). The SDE margin (3.6) is the only favourable statistic there.

Pixel offset (task question). `ffi_pixel_S68/S96.json`, converted to sky with the TESScut WCS. I checked the axis convention: the WCS position of the 15" neighbour matches the JSON `neighbours` dx/dy in both sectors. The loss-centroid offsets are 8.5" at **PA 154°** (S68) and 8.1" at **PA 34°** (S96), about 120° apart. S68 and S96 have nearly the same detector orientation. The offsets agree in size but **not in direction**. Each is about 2.4σ, and a Rayleigh-distributed offset with σ ≈ 0.17 px reaches 0.42 px about 5% of the time. Along PA 154° the only Gaia source within 45" is DR3 6603415224353564672 (TIC 2056001666, G 20.4, 15.4", PA 169°). It would need a 183% eclipse, which is impossible. Toward PA 34° there is nothing within 60". The nearest source able to make the depth is G 17.18 at 73.8" (needs 9.4%), which the pixel test excludes. Depth falls with aperture radius (S68 215→162, S96 329→214 ppm), as expected for an on-target signal. **No catalogued source can host the signal.** The offset looks like method noise. The Gaia target RUWE is 1.30 (mild).

Errors to fix: the "consistent 0.41-0.42 px offset" wording implies a consistent direction, which is wrong. The sigma_pred of 1.4 min is about 6-20x too small (realistic 8-29 min, `refit*.py`). The `vet_summary.png` fold uses the BLS period 1.085676, not v2 1.085671 (−7.8σ apart in the log). Not serious, but label the figure. The S106 public-data status (must-fix 1).

## 2. TIC 122522485 (P 2.32213 d, ~200-230 ppm, K dwarf T 10.0)

**Recommendation: marginal / candidate (unvalidated).** The period is solid, but NFPP 0.0082 is 8x the threshold, FPP is 0.075, and the red-noise SNR is about 7.

Novelty: TOI, CTOI, Exoplanet Archive and ExoFOP target JSON: none. MAST: SPOC 2-min in S3, S4 and S30, and no DV products. Bulk TCE files for s0003, s0004, s0030 and the multi-sector s0001-s0003/06/09/13/36/39/46/65/69/92/96 runs: no row, so **SPOC never produced a TCE.** prior_grep hits are SrihariSr/Stellaris SPOC target lists (S3/S4), paraschopra target/catalogue lists (no triage row) and AliBaig-xD/tess-quiet sector TIC lists. All are target lists, not detections. GitHub quoted searches and Zenodo: 0. VSX/Gaia variability: none. SIMBAD: TYC 7010-171-1.

Signal checks: the binned BLS top peak is 2.32210 d, SDE 14.0, rank 1. QLP SAP per sector (red-noise errors): S3 247±60, S4 119±56, S30 185±65, S97 166±47, S105 290±72 ppm. Combined about 7.3σ. Odd/even 214±38 vs 186±41 (consistent). Secondary −20±27 ppm (none). rho_fit/rho_TIC = 0.54: the duration is about 25% longer than a central transit on the TIC star. Among the 7 PASS rows in the triage file, rho_ratio is 0.33-1.71, so 0.5 is common and partly reflects the coarse duration grid. It is a soft flag, not a failure. The 2018 holdout's training search peaks at 13.22 d (SDE 12.2, 1090 ppm), close to the TESS orbit length and the known ~13.7-d edge-ramp systematic (`tess-pipeline-pitfalls`). It is probably systematic, but I did not verify this. The 2.32-d signal itself reappears in the other holdouts.

Timing scatter (chi2/dof 93.3/3, log `logs/prereg_r3_122522485.log`):
- **Cause: underestimated per-sector errors, not TTVs, an alias or a wrong period.** Injection-recovery rms errors: SPOC S3 6.9, S4 16.2, S30 32.9; QLP S97 16.3, S105 7.8 min. The project used 3.0-6.0 min. Refitting the same five times with these errors gives chi2/dof = 3.3/3 and P = 2.322134 d. The first S106 transit moves +3.5 min, with sigma ≈ 7.5 min (`refit.py`).
- **S3 SPOC at −41 min depends on the extraction.** The same S3 2-min data give a best-box shift of +37 min (SAP) and +1 min (PDCSAP) against v2. QLP S3 gives −10.8±25.8 min (log) and +50 min (my SAP box). That spread of tens of minutes is not astrophysical.
- Aliasing: the S3-S30 baseline (315 cycles) fixes P to about 6e-5 d even with 20-30 min errors. Projected over the 790-cycle gap that is about 50 min, far below P, so there is no cycle-count ambiguity.
- The frozen ephemeris is sound. The 5.58x inflation (sigma_pred about 16 min, window max(3σ,30) ≈ 48 min) is crude but conservative.
- Note that the per-object PREREGISTRATION text reads as min(3σ, 30 min). The governing max() reading is set in `prereg_test.py` and the protocol on Zenodo 10.5281/zenodo.23462442 (record exists, created 2026-10-19 01:36 UTC). This object is the one where the two readings differ (48 vs 30 min), so disclose it in the outcome report.

Pixel: S97 offset 0.43 px (9.1") at PA 238°, about 2.7σ. S105 offset 0.13 px at PA 122°. The only capable neighbour, TIC 122522486 (G 14.5, 21.8", PA 65°, needs about 0.6%), lies roughly **opposite** the S97 offset. Depth versus aperture is flat to slightly falling. There is no pixel evidence for that neighbour, but at 21.8" (about 1 px) the test only marginally excludes it, and it drives the NFPP.

Errors: the timing errors (above); Rp should be about 1.14 R_E from the SAP depth (must-fix 6); the S106 status (must-fix 1). The S107/S108 rows are honestly labelled "retrodiction: before freeze, untested", but those data are also public.

## 3. TIC 283913390 (P 2.48111 d, ~460-500 ppm, ~1.8 R_E, T 10.8)

**Recommendation: weak.**

Novelty: TOI, CTOI, Exoplanet Archive and ExoFOP: none. FFI-only, with no SPOC 2-min, so there can be no SPOC single-sector TCE. The multi-sector TCE files I downloaded have no row. prior_grep: 0 hits. Zenodo: 0. GitHub: the plain-number search first timed out (HTTP 408), and the retry returned 25 unrelated rows. Quoted searches: 0. VSX/Gaia variability/SIMBAD within 10": none.

Signal checks: **3 sectors, not 5 years** (must-fix 2). QLP SAP: S7 342±63, S33 573±65, S87 436±101 ppm, combined about 11σ in quadrature. The binned BLS still ranks it first, but at **SDE 8.4 only**. The fold of all data with an unweighted red-noise null gives 5.5σ. Blind holdouts: 2020 6.3, 2021 3.6 (same sector as 2020), 2024 4.2, 2025 2.1 (same sector as 2024). Odd/even and secondary are fine (488±114 vs 444±159; −104±85). rho ratio 0.54. **Gaia RUWE 2.05** points to an astrometric binary: an unresolved companion would dilute the signal or could host it. TRICERATOPS without a contrast curve does not account for this. NFPP 0.025 is 25x the threshold. Neighbours: TIC 283913393 (G 16.7, 17.1", PA 72°, needs about 5.5%) and G 17.6 at 18.9" (RUWE 2.2, needs about 13.7%) are not excluded by a pixel test that only covers 20-60". The S87 offset is 0.18 px (3.8") at PA 333°, about 2.2σ, not toward them. Depth falls with aperture (541→283 ppm), which fits an on-target or very close source.

Ephemeris sensitivity: the S7 time (tc_err 31 min) barely constrains P. BLS P (2.481056) and v2 P (2.481107) differ by 5e-5 d, which the log reports as +4.3σ. I did not propagate the BLS ephemeris to S111 myself. My refits with realistic errors move the first S111 prediction by −11 to −20 min, with sigma 20-32 min, compared with the frozen 5.7 min. **The S111 test is sensitive, at the level of the 30-min window, to which ephemeris is chosen.** An "inconsistent" outcome would not cleanly separate a false positive from a bad ephemeris.

## 4. TIC 196514928 (P 2.39212 d, ~590 ppm, ~2.1 R_E, T 11.0)

**Recommendation: marginal. The signal is strong but its source is unresolved.**

Novelty: TOI, CTOI, Exoplanet Archive and ExoFOP: none. FFI-only, and no TCE row. prior_grep: 0. Zenodo and GitHub quoted searches: 0. VSX/Gaia DR3 list a DSCT|GDOR|SXPHE pulsator (Gaia DR3 5647001495889091968, G ≈ 14.4) at 54". It is not an eclipsing binary and is irrelevant to a box signal. SIMBAD: UCAC2 20833403.

Signal checks: this is the strongest signal of the four. The binned BLS top peak is 2.39211 d, **SDE 30.4**. It appears in all 5 sectors and 4 distinct seasons (QLP SAP S8 476±135, S34 578±93, S35 636±130, S62 550±102, S88 644±107 ppm), about 12σ in quadrature. The 4/4 years count is correct here. Odd/even is 530±88 vs 655±86 (about 1σ; project 1.6σ). No secondary at phase 0.5 (−45±61). The project's best "secondary" is at phase 0.475 with SNR 3.4, which is noise. The fold in `vet_summary.png` looks asymmetric, deeper in the first half.

False-positive concerns:
- **Consistent pixel offset:** S62 0.28 px (5.6") at PA 130° and S88 0.31 px (6.3") at PA 135°. Each is about 2σ, in the same direction, about 2.8σ combined.
- **Inverted depth-versus-aperture in S62:** 129±104 ppm at r = 1 px against 368±66 at 2 px. An on-target signal should get shallower with radius, as it does for 206620592 and 283913390. S88 is weakly inverted too (264±142 → 368±90).
- **Gaia RUWE 2.09**, a binary indicator.
- **Inside 1 px:** TIC 830552246, G 17.05 at 1.99", PA 340°, needs about 11% eclipses. The pixel test cannot exclude it, and it drives the NFPP of 0.0068 (7x the threshold). It is not in the offset direction.
- **Toward the offset:** sources at PA 130-152° include TIC 196514936 (G 17.2, 19.4", PA 152°, needs about 15%, a possible EB). It is inside the 20" floor where the pixel test claims nothing. The G 20.3 (13.3", PA 130°) and G 19.3 (16.6", PA 148°) sources would need more than 80% and are excluded on depth.
- rho ratio 0.49.

This one needs a dedicated difference-image or PRF centroid analysis over all five sectors before it is called a candidate.

S109 timing: the frozen sigma is 9 min. My refit with realistic errors shifts the first S109 transit by −4.5 / +2.7 min (sigma 8-12.5 min), well inside 30 min. The ephemeris is fine.

## 5. Frozen predictions (all four)

- SHA-256 of each `predicted_transits_2026_2027_v2.csv` (`shasum -a 256`) matches `sha256_csv` in `final_ephemeris_v2.json` and the hash in `PREREGISTRATION_v2.md`: 75b6ea73... (206620592), 47ce36bc... (122522485), fe3ad466... (283913390), 1fa2a7e0... (196514928). The first 16 hex characters also match `allsky_round3_outcomes.csv`.
- The test sectors agree with tess-point: 206620592 S106; 122522485 S105-108; 283913390 S111; 196514928 S109-112.
- Predicted times are linear in epoch with the v2 P, and the sigmas grow slowly. They are numerically sensible but too small (must-fix 4).
- Governing rule: max(3σ, 30 min), verified in `scripts/prereg_test.py`. Effective windows: 30, 48, 30 and 30 min.
- Freeze timestamps (2026-10-20 00:33-00:43 UTC) come before the clarification file dated 2026-10-20.

## 6. Overall summary

| TIC | Recommendation | Main reasons |
|---|---|---|
| 206620592 | candidate (unvalidated) | rank-1 BLS, all 3 sectors, density OK, no capable neighbour; offsets point different ways; red-noise SNR ~7; FPP 0.032 |
| 122522485 | marginal / candidate (unvalidated) | period solid, timing scatter explained by error underestimate; NFPP 0.0082, FPP 0.075, SNR ~7 |
| 283913390 | weak | 3 sectors not 5; SDE 8.4; RUWE 2.05; NFPP 0.025; S111 outcome sensitive to ephemeris choice |
| 196514928 | marginal | strong signal (SDE 30) but consistent ~2.8σ centroid offset, inverted aperture trend, RUWE 2.09, G 17 star at 2", NFPP 0.0068 |

No object shows evidence of an earlier report in any source I checked, so none qualifies for "rediscovery-credit".

Never write "likely planet" or "validated" for any of them. Write "no earlier report found in [list of sources, dated]", not "new".

## 7. Limits of this review

- The Zenodo API `q=` search covers record metadata, not the contents of uploaded files. It is not a full-text search; the local sweep corpus (`prior_grep.py`) is the file-content proxy.
- GitHub code search indexes default branches and files under about 384 KB only. Plain-number searches return mostly noise and are capped at 100 results.
- The TCE bulk file s0014-s0023 failed to download. It is a northern-hemisphere run and irrelevant to these southern targets.
- I did not search ADS or arXiv full text beyond the local corpus, and did not search AAVSO, TFOP-internal lists or private CTOIs.
- My red-noise SNRs and injection timing errors use a simple box model with a biweight detrend (window 0.7 d). They are approximate, but independent of the project code.
- I did not rerun TRICERATOPS. I did not look at any S106 flux data.
