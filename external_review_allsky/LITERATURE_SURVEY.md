# State-of-the-art vetting checks for 700-800 ppm QLP/FFI candidates (fetched 2026-10-18)

Note on IDs: arXiv 2308.09033, 2302.09534, 1703.03797 and 2009.11245 in the brief resolve to unrelated papers and were not used. Correct IDs: Hord 2024 = 2308.09617; VaTEST III = 2311.00688; DIAmante = 2008.09832; Mills & Fabrycky = 1606.04485. arXiv PDFs were fetched and text-extracted locally; quotes are from that text.

## 1. Pixel-level localisation

1a. Twicken et al. 2018, PASP 130, 064502 (Kepler DV). https://arxiv.org/pdf/1803.04526 — "The minimum 3σ uncertainty in the magnitude of the mean offset is therefore 0.2 arcsec, and no offset less than that is considered significant" (Kepler). "It is therefore possible in a crowded field to obtain a significant offset with respect to the out-of-transit centroid even for a genuine transiting planet." Difference images "cannot be trusted" for saturated sources or stellar variability on transit timescales.

1b. Guerrero et al. 2021, ApJS 254, 39 (TOI catalog; SPOC DV as run on TESS). https://arxiv.org/pdf/2103.12538 — "For TESS, the plate scale is larger (21 arcsec/pixel) and a majority of targets are only observed in a single sector; the quadrature error term is set so that the centroid offsets are not significant at the 3-σ level if they are < 7.5 arcsec." Two reference positions: proper-motion-corrected catalog position ("robust against crowding... more reliable... for crowded TESS images") and out-of-transit PRF centroid (not robust against crowding).

1c. Bryson et al. 2013, PASP 125, 889. https://arxiv.org/pdf/1303.0052 — FP declared if source "significantly offset (more then three standard deviations, written > 3σ)"; "offsets > 3σ due to random fluctuations about 1.11% of the time." Depth/centroid aperture mismatch "invalidates the above analysis when significant flux from the transit source falls outside the optimal aperture... when the transit source and target star are separated by more than one Kepler pixel (3.98 arcseconds)" — i.e. the measured depth of an off-target source is aperture-dependent. Single-quarter offsets scatter 0.90 arcsec vs 0.41 arcsec for 12-quarter averages (Kepler; 4 arcsec pixels).

1d. Kostov et al. 2019, AJ 157, 124 (DAVE). https://arxiv.org/pdf/1901.07459 — flags "potential CO" when "the centroid offset is at the > 3σ level of significance and on the order of a pixel or larger"; warns that "bright field stars inside the aperture... may capture the out-of-transit PRF fit and thus result in a false centroid offset"; for neighbours ≥1 pixel away, custom per-star apertures decide the host. (Hord 2024 applies DAVE to TESS.)

1e. Kunimoto et al. 2025, AJ accepted (LEO-Vetter). https://arxiv.org/html/2509.10619v1 and https://arxiv.org/pdf/2509.10619 — Only pixel test is a difference-image PRF-fit centroid (transit-diffImage): "When the transit SNR is high, this fitting method is accurate to within about 0.2 pixels (= 5.2 arcsec with TESS' 21-arcsec pixels)... this accuracy degrades with lower transit SNR"; "prfFitQuality < 0.3 means that the fit results should not be trusted"; "We fail TCEs as likely off-target when Δθ > 15″" (threshold "empirically chosen", "lenient", "high completeness over high reliability"). On real QLP FFI TCEs: 153 of 325 flux-passing TCEs failed the centroid test; two known NEBs (TOI-633.01, TOI-5648.01) still passed. Also notes QLP's AstroNet "cannot yet distinguish between transiting planets and eclipsing binaries, and do not implement any pixel-level vetting." tess-point is used for (RA,Dec)->pixel conversion (not a vetting tool).

1f. Bryson & Kunimoto 2025 (Transit-APP, NASA NTRS accepted manuscript). https://ntrs.nasa.gov/api/citations/20250003461/downloads/transitApp.pdf — centroid-free Bayesian comparison of observed vs simulated difference images per star; "When the S/N is high, our method can distinguish sources separated by about 0.2 pixels, ≈0.8 arcsec for Kepler and ≈5 arcsec for TESS"; fails when "difference images [are] dominated by a nearby bright variable star... most commonly encountered in TESS data due to its larger pixels"; "currently being incorporated into TRICERATOPS."

Bottom line: no TESS pixel method resolves <~5″ even at high SNR; practical FFI thresholds are 7.5″ (SPOC 3σ floor) to 15″ (LEO-Vetter), i.e. 0.35-0.7 px. Neighbours inside that radius cannot be excluded from pixels alone.

## 2. Blended-EB false-positive statistics

2a. Guerrero 2021 (above): "In the Prime Mission, 565/2241 TOIs (about 25%) have been identified as False Positives from follow-up observations." No NEB or galactic-latitude breakdown ("beyond the scope of this paper"). QLP photometry: "five circular apertures with radii of 1.75, 2.5, 3.0, 3.5, 8.0 pixels"; constant flux "taken from the theoretical calculation in the TIC", variability from difference images — "This method effectively de-blends the light curve from contamination by an additional star inside the aperture"; aperture chosen per magnitude bin.

2b. Kunimoto et al. 2022, RNAAS (QLP HLSP). https://arxiv.org/pdf/2211.04386 — HLSP files contain "an optimal aperture, and additional raw light curves from one smaller and one larger apertures." QLP page (https://tess.mit.edu/qlp/): "our nominal planet candidate vetting is only performed down to T = 10.5 mag"; TGLC "forward models the FFIs with the effective point spread function to remove contamination from nearby stars" and "replaced our previous FIPHOT method... beginning with Sector-94."

2c. Montalto et al. 2020, MNRAS 498, 1726 (DIAmante). https://arxiv.org/abs/2008.09832 — search "limited to the least crowded regions of the sky"; a statistical model gives "the probability of correct identification of the source of variability"; 396 candidates, 70 objects with Gaia evidence of binarity.

2d. Collins et al. 2018, AJ 156, 234 (KELT-FUN). https://arxiv.org/pdf/1803.01869 — Table 3 (KELT False Positives by Category): of 1128 catalogued FPs, 378 (34%) are NEB ("Nearby EB (Blend in KELT aperture)"), 130 EB1, 25 EB2, 90 BEB, 307 SB1, 140 SB2; "The most common photometric FPs result from... NEBs"; "nearly 30% of all our FPs being non-astrophysical." (23″ pixels, ~3′ aperture — the closest published analogue to TESS FFIs.)

2e. Hord et al. 2024, AJ 167, 233. https://arxiv.org/pdf/2308.09617 — of 103 TOIs vetted with SPOC DV, DAVE, TFOP SG1/SG2, TRICERATOPS and vespa: 23 validated, 33 marginal, 29 "likely false positives", 4 inconclusive.

2f. DEATHSTAR (https://arxiv.org/html/2312.08373v1): ZTF/ATLAS photometry of all TIC stars within 2.5′ found 35 off-target vs 17 on-target (biased sample, depths "≳1.5%"); not usable at 750 ppm.

Not found after several searches: a published NEB fraction for QLP/FFI TOIs from SG1, or NEB rate vs galactic latitude.

## 3. TFOP SG1 standards

3a. Collins 2019, TFOP SG1 talk (TSC, 2019-08-01). https://tsc.mit.edu/2019/talks/Karen%20Collins.pdf — "Search stars within 2.5 arcmin of target for nearby EBs (NEBs)... r = 1.5″ apertures"; "Ground-based sensitivity general threshold ~1000 ppm (1 ppt or ~1 mmag)"; "For transit depths < 1 ppt: Primary goal is to check all Gaia DR2 star locations within 2.5 arcmin of the target for NEBs. Confirmation of no NEBs (no Gaia stars blended in target PSF) => CPC = Cleared Planet Candidate; ... contaminated with known nearby star => CPC-; Confirmed off target (1st time) => PNEB; (2nd time) => NEB." For >1 ppt: VPC/VPC-/VPC+ (achromatic) / BEB (chromatic). Goals include "Measure transit depths to confirm TESS deblending factor."

3b. https://tess.mit.edu/followup/ — SG1 purpose: "identify false positives due to nearby eclipsing binaries"; "Provide better inventory and better photometry of scene than is provided by the TIC." No procedural thresholds on the page.

3c. Collins 2018 (above): check "all detected stars within a 3′ radius" and brighter stars "out to 6′"; "most NEBs are found within 1′-2′ (~3-5 KELT pixels)"; an NEB call needs the neighbour close enough to cause the event, timing consistent with the ephemeris, and a depth "deep enough to exclude a transiting planet."

## 4. Sector-to-sector depth changes

4a. Per-sector dilution: Guerrero 2021 — SPOC "Flux levels are adjusted for crowding"; "The CROWDSAP keyword... reports the average fraction of the flux in the photometric aperture that is from the target star"; QLP deblends via TIC constant flux (above). The QLP Data Production Description (supplement to Kunimoto et al. 2022 RNAAS; local copy, not re-fetched by URL this session) lists BESTAP/SMALLAP/LARGEAP keys and KSPSAP_FLUX_SML/LAG columns, enabling a within-sector depth-vs-aperture test. Starspot-driven depth changes: no source fetched, not covered. TESS-ExoClass: only evidence fetched is LEO-Vetter's note that SPOC TCEs pass TEC before TOI alerting; no TEC pixel metric was retrieved.

4b. Method boundary: QLP page and MAST HLSP page (https://archive.stsci.edu/hlsp/qlp, "Updated: 2026-08-12"): "As of Sector 94, QLP is now using the TESS-Gaia Light Curve (TGLC) methodology." Han & Brandt 2023, AJ 165, 71 (https://arxiv.org/abs/2301.03704): TGLC forward-models FFIs with an ePSF and Gaia DR3 priors, publishes "TGLC Aperture and PSF light curves", precision "<~2% at 16th TESS magnitude even in crowded fields." So pre-S94 (FIPHOT/TIC deblend) and post-S94 (TGLC/Gaia deblend) depths sit on different dilution systems.

4c. Mills & Fabrycky 2017, AJ 153, 45 (https://arxiv.org/pdf/1606.04485): "in different observing seasons, a given pixel or group of pixels in the aperture sum might observe a slightly different group of stars causing the transit depth to change as the transit is diluted by background stars." The astrophysical alternative (Kepler-108 "strong TDVs", mutual inclination "~15-60 degrees") requires a massive mutually inclined companion; implausible for a lone 3-5 d sub-Neptune on sector timescales.

4d. DRNs (https://archive.stsci.edu/tess/tess_drn.html: DRN 118-142 for S85-104; S105 not posted). DRN 124 (S90, https://archive.stsci.edu/missions/tess/doc/tess_drn/tess_sector_90_drn124_v01.pdf): no pointing/attitude anomaly noted; reverse-clocked CCD data taken at the end of Orbit 187 (Mar 25-26 2025). DRN 137 (S100, .../tess_sector_100_drn137_v01.pdf): "A new attitude control algorithm was tested during the last 27 hours of Sector 100. Reaction wheel speeds were calibrated during the first ~1 hour, which resulted in elevated pointing scatter." DRN 142 (S104, .../tess_sector_104_drn142_v01.pdf): "a test of a new spacecraft attitude control system, ACS 5.11... included three reaction-wheel calibration episodes, which resulted in large dispersions in the spacecraft pointing" at "TJD 4198.61-4198.72, 4200.81-4200.91, and 4203.00-4203.11"; "Users should expect increased photometric scatter during these times." HEASARC summaries for S101-103 (https://heasarc.gsfc.nasa.gov/docs/tess/sector102_summary.html etc.) list no pointing anomalies; S102 lost ~9.8 h to missed downlinks (S103 recovered 3.5 h + 1.9 h as FFIs only).

4e. QLP S99-104 timing: MAST HLSP page — "A barycentric timing correction error was identified starting in Orbit 210 (second half of Sector 99)" through S104; "MAST is in the process of updating these sector files with corrected timestamps"; S99-104 still asterisked as not redelivered (page updated 2026-08-12). TESS-SPOC HLSP (https://archive.stsci.edu/hlsp/tess-spoc, updated 2026-07-23): latest FFI light curves listed are Sector 85.

## 5. Gaia DR3 blend diagnostics

5a. Gaia DR3 datamodel (https://gea.esac.esa.int/archive/documentation/GDR3/Gaia_archive/chap_datamodel/sec_dm_main_source_catalogue/ssec_dm_gaia_source.html): ipd_frac_multi_peak = "fraction of windows... for which the IPD algorithm has identified a double peak" (resolved double star); ipd_gof_harmonic_amplitude = amplitude of GoF variation with scan angle (the phase entry notes a binary "≲0.1 arcsec" raises GoF along the pair's axis); astrometric_excess_noise = "disagreement, expressed as an angle" with the 5-parameter model; non_single_star bits = astrometric / spectroscopic / eclipsing binary; duplicated_source criterion 0.18″; phot_variable_flag 'NOT_AVAILABLE' for most sources.

5b. Penoyre, Belokurov & Evans 2022, MNRAS (https://arxiv.org/pdf/2202.06963): Gaia "seems to reliably resolve 2 sources at separations around 2 arcseconds and above... though they may be distinguishable down to 0.6 arcseconds. We would expect these IPD measures to start flagging systems up around one arcsecond separations and down to around 180 mas." VaTEST III (below) adopts "ipd_frac_multi_peak value of 2 or lower are likely to be single stars" and RUWE>1.4 as binary indicator. Practical reading: a 4″ companion is a separate Gaia source (inventory/TIC check, TRICERATOPS flux ratio); ~1″-0.18″ is the IPD regime; <0.18″ needs speckle/AO or RVs.

5c. Mowlavi et al. 2023, A&A 674, A16 (https://arxiv.org/pdf/2211.00929): "2 184 477 sources with brightnesses from a few magnitudes to 20 mag in the Gaia G-band"; "restricted to orbital periods larger than 0.2 days"; "Catalogue completeness is estimated to be between 25% and 50%... relative to the OGLE4 catalogues." Absence of a neighbour from vari_eclipsing_binary is weak evidence.

5d. Cautionary case (non-refereed preprint by an independent researcher; the EB interpretation is argued, not established): Escolà-Rodrigo 2026, arXiv:2601.02171v4 (https://arxiv.org/html/2601.02171v4) — TOI 864.01 (~640 ppm SPOC depth) had "RUWE = 1.18", flat centroids, TRICERATOPS FPP 0.25/NFPP ~7e-5, yet high-resolution imaging shows "a stellar companion at a separation of 0.04″"; ground depth 0.37 vs 0.64 ppt predicted; argued hierarchical EB (TFOP VPC-). Illustrates sub-arcsec blends invisible to Gaia and pixels.

## 6. Validation thresholds and priors

6a. Giacalone et al. 2021, AJ 161, 24 (https://arxiv.org/pdf/2002.00691): "validated planets (FPP < 0.015 and NFPP < 10^-3), likely planets (FPP < 0.5 and NFPP < 10^-3), and likely nearby false positives (NFPP > 10^-1)"; stars "within a circle of radius 10 pixels" are candidate hosts; "FPP alone does not appear to be a reliable predictor of TOI disposition when SNR < 15"; only "Rp < 8R⊕" is validatable.

6b. Hord 2024 (above): adopts Giacalone's categories; for vespa "Signals with an FPP < 0.01 are considered statistically validated", marginal FPP<0.25; averages multiple TRICERATOPS runs; uses high-resolution-imaging contrast curves and SG1/SG2 dispositions.

6c. Mistry et al. 2024, PASA 41, e030 (VaTEST III, https://arxiv.org/pdf/2311.00688): sample requires no companion in high-resolution imaging, non-V-shaped fits, and SG1 disposition "CPC, VPC or VPC+"; speckle (Gemini 'Alopeke/Zorro, SOAR HRCam) and AO (Keck NIRC2, Palomar) imaging; Gaia RUWE and ipd_frac_multi_peak checked.

6d. Priors: Fressin et al. 2013 (https://arxiv.org/abs/1301.0842): Kepler "global false positive rate... is 9.4%", lowest for small Neptunes (2-4 R⊕) at 6.7%. Kunimoto & Matthews 2020, AJ 159, 248 (https://arxiv.org/pdf/2004.05296): for 1-2.83 R⊕ and P<200 d, 1.20 (+0.11/-0.10) planets per K star vs 0.67 (G), 0.26 (F); grid uses period edges 1.56/3.13/6.25 d and radius edges 2/2.83 R⊕ (bin values in figures only). Note the Kepler FP rate is for a vetted KOI list with 4″ pixels; FFI 21″-pixel samples have a much larger blend prior (Collins 2018: 378/1128 NEB for 23″ pixels).

## 7. 2024-2026 pointing/precision

No 2024-2026 arXiv paper on TESS pointing degradation surfaced in two searches. The evidence is the DRNs: ACS 5.11 attitude-control tests with reaction-wheel calibrations in S100 and S104 producing "large dispersions in the spacecraft pointing" (DRN 137, 142 above). The TESS Users Committee report (19 Feb 2026) raises no pointing issue.

## Checks a referee would require for a 750-ppm FFI candidate on a K dwarf (Tmag 10.5-11.4)

1. Difference-image PRF-fit centroid per sector with fit-quality weighting; report Δθ and the 3σ radius of confusion; state that offsets <7.5″ (SPOC floor) / <15″ (LEO-Vetter) are not excludable and that accuracy is ~5″ only at high SNR [Guerrero 2021; Kunimoto 2025; Bryson & Kunimoto 2025].
2. Compute offsets against both the proper-motion-corrected Gaia position and the out-of-transit centroid; a crowded-field offset vs the out-of-transit centroid alone is not evidence [Twicken 2018; Guerrero 2021].
3. Run Transit-APP / TRICERATOPS positional probabilities for every Gaia/TIC star within TRICERATOPS's 10-px (≈3.5′) query radius (SG1 and Hord 2024 use 2.5′) bright enough to produce 750 ppm; list each star's required eclipse depth [Giacalone 2021; Bryson & Kunimoto 2025].
4. Within-sector depth vs aperture (QLP SML/best/LAG; TGLC aperture vs PSF): an off-target source gives aperture-dependent depth [Bryson 2013; QLP HLSP supplement].
5. Tabulate per-sector depth against the S94 FIPHOT->TGLC boundary and against BESTAP per sector; a depth step coincident with S94 is a dilution-system change, not astrophysics [QLP page; Han & Brandt 2023; Mills & Fabrycky 2017 for the Kepler analogue].
6. Check transit epochs in S100 and S104 against the reaction-wheel calibration windows (TJD 4198.61-4198.72, 4200.81-4200.91, 4203.00-4203.11; S100 first ~1 h / last 27 h) and scattered-light flags; exclude or down-weight [DRN 137, 142].
7. Do not use QLP S99-104 timestamps for ephemeris/TTV work until MAST redelivers corrected files (not done as of the 2026-08-12 page) [MAST QLP HLSP].
8. Odd-even depth, secondary eclipse (<10% of primary), SWEET/variability test at P, P/2, 2P at LEO-Vetter thresholds [Kunimoto 2025]; transit shape (V vs U) via full modelling [VaTEST III].
9. Gaia inventory within 2.5′ with per-star maximum depth; Gaia DR3 RUWE, ipd_frac_multi_peak (≤2 ≈ single), ipd_gof_harmonic_amplitude, astrometric_excess_noise, non_single_star, duplicated_source; state the blind zone (<0.18″; 0.6-2″ only partially resolved) explicitly [Gaia datamodel; Penoyre 2022; VaTEST III].
10. Cross-match neighbours with vari_eclipsing_binary but treat non-detection as weak (25-50% completeness, P>0.2 d) [Mowlavi 2023].
11. SG1-style ground photometry: at <1 ppt the achievable disposition is CPC (all Gaia stars within 2.5′ cleared with ~1.5″ apertures), not an on-target detection; a referee should expect CPC or an explicit statement that it is pending [Collins 2019; Collins 2018].
12. Speckle/AO contrast curve to exclude sub-arcsec companions; the TOI-864.01 preprint illustrates RUWE 1.18 and flat centroids coexisting with a 0.04″ companion argued to host the eclipse [VaTEST III; Escolà-Rodrigo 2026, non-refereed].
13. TRICERATOPS FPP<0.015 and NFPP<0.001 with contrast curves, multiple runs averaged, and SNR stated; at SNR<15 report FPP as indicative only and do not claim validation [Giacalone 2021; Hord 2024].
14. Reconnaissance spectroscopy/RV to exclude stellar-mass companions and SB2 lines (standard in validation papers) [Hord 2024; VaTEST III].
15. Quote the prior honestly: ~1.2 small planets per K star (1-2.83 R⊕, P<200 d), against the fact that NEBs are the single largest FP class in a 23″-pixel survey (34% of 1128 catalogued KELT FPs) and ~25% of Prime-Mission TOIs were FPs [Kunimoto & Matthews 2020; Collins 2018; Guerrero 2021].
