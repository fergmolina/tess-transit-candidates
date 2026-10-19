# Response to the round-4 external review (Codex), 2026-10-19

Pre-revision text: results/referee_89247735/round3_fixes/main_before_round4.tex. Revised: paper/main.tex and main.pdf (10 pp; the round-3 response wrongly said 9).

| Item | Verdict | Action |
|---|---|---|
| M1. +8.02 min premise wrong (TESScut TIMECORR is not target-specific) | **Confirmed.** At the S104 event TIMECORR = 7.74 min; the target's light-travel time is 7.42 (geocentric 7.40). S104 QLP = spacecraft time −0.085 min | New method (scripts/qlp_clock_v2.py: JPL Horizons TESS vectors, convention c0 = +0.033 min): correction +7.533 min, matching the reviewer. v5 ephemeris P = 18.323174 ± 0.000040 d (SHA 216e7a4c…); clock error 0.05 min. All 8 objects redone (results/qlp_clock_v2/, revised addendum b); shifts ≤1.2σ |
| S105 claim | Independently supported | Kept. Also found: S100–S102 carry a wrong non-zero correction, S103–S105 none |
| M2. Neighbour depth 28–31 %, not 37–40 %; duration-ratio argument | **Confirmed** (arithmetic) | Fixed; k ≤ 0.11 shape constraint added with its limits; "not ruled out, simplest versions disfavoured" |
| M3. Radius span not an interval; exclusive classification | Agreed | Labelled as conditional estimates; Zarco's 8.7 R⊕ noted; summary now lists possible interpretations; MCMC settings stated (convergence not documented) |
| M4. SIMBAD; "all products public" | **Confirmed** | SIMBAD wording fixed; archive claim narrowed; fit JSONs and the clock products go public in v1.9 |
| Flag counts 27/139/235; mask percentages; correlation 0.84; a 0.119 AU / Teq 544 K; ±0.45; quantile rounding | **All confirmed** from the FITS files and JSONs | Fixed; flag counts are now generated from the data by make_figure1.py |
| Contacts used the old T14; epoch-162 Sun margin | Confirmed | v5 contacts use T14 = 4.54 h. Under the strict criteria epoch 159 is the only full CTIO transit; 162 misses by 0.03° of solar altitude (text says so) |
| Coprime wording; Fig. 1 background/centroid; "independent pipeline"; v1−v4 epoch range; "first ground-observable" | Agreed | Fixed. The background/centroid claim was checked in the QLP columns (in−out < 0.4σ) and stated with that number |
| Abstract length | Agreed | 210 words |
| Not done | — | Retiming events with the final shape (≤0.3 min, stated in text); stale macros in the generated table file; Lightkurve citation; exact MAST QLP acknowledgement text; diluted-EB fit; centroid injection calibration |

---
**Dated correction (2026-10-19, after the round-5 review).** Several statements above were inaccurate when written:
- Table 1's note still said 28 (now 27).
- §3.3 kept +0.0021 / −2.2 (now +0.0020 / −2.3).
- The rendered v5−v1 endpoint was +5.4 min (the generator omitted epoch 163; now +5.5).
- The background figure is a ratio to per-cadence scatter, not a "<0.4σ" significance.
- Epoch 162 misses the solar-altitude criterion by 0.0025°, not 0.03°.
- "All shifts ≤1.2σ" holds only for the seven objects other than TIC 89247735, which reaches 1.38σ.
See RESPONSE_round5_external.md.
