# TIC 317134140 scorer v1.3: calibration diagnostics (descriptive; DECISIONS 187)

Source `calibration_v1.3.json` (SHA-256 `d2c5b2ec162d9509...`), produced by the locked scorer (`f3f55c0d74733f8a...`) on the TRAINING sectors only.

**What these are.** Conditional outcome frequencies in three selected training noise realizations (S6, S87, S107; S98 separately),
with the real signal divided out and a registration-shape signal injected at random periods of 0.53-0.70 d.
They are not calibrated probabilities for S108-S110, and no likelihood ratio or combined evidential-strength conclusion is drawn from them.
The frozen per-sector outcomes remain the outcomes of record.

## Injected signal (H1), pooled S6 + S87 + S107

| Depth | Trials | PASS | PARTIAL | INCONCLUSIVE | FAIL | INSUFFICIENT |
|---|---:|---:|---:|---:|---:|---:|
| 130 ppm | 150 | 10/150 (7 %) | 82/150 (55 %) | 37/150 (25 %) | 21/150 (14 %) | 0/150 (0 %) |
| 185 ppm | 300 | 93/300 (31 %) | 175/300 (58 %) | 30/300 (10 %) | 2/300 (1 %) | 0/300 (0 %) |
| 240 ppm | 150 | 98/150 (65 %) | 52/150 (35 %) | 0/150 (0 %) | 0/150 (0 %) | 0/150 (0 %) |

Per sector at 185 ppm:

| Sector | Trials | PASS | PARTIAL | INCONCLUSIVE | FAIL |
|---|---:|---:|---:|---:|---:|
| S6 | 100 | 44/100 (44 %) | 49/100 (49 %) | 6/100 (6 %) | 1/100 (1 %) |
| S87 | 100 | 36/100 (36 %) | 53/100 (53 %) | 11/100 (11 %) | 0/100 (0 %) |
| S98 (two sectors; not pooled) | 100 | 71/100 (71 %) | 27/100 (27 %) | 2/100 (2 %) | 0/100 (0 %) |
| S107 | 100 | 13/100 (13 %) | 73/100 (73 %) | 13/100 (13 %) | 1/100 (1 %) |

## Noise only (H0), pooled S6 + S87 + S107

Clause A at random periods and phases (6000 trials): A_CONSISTENT 107/6000 (2 %), A_HIGH 0/6000 (0 %), A_INCONCLUSIVE 846/6000 (14 %), A_LOW 5047/6000 (84 %).
Outcomes: PARTIAL 107/6000 (2 %), INCONCLUSIVE 846/6000 (14 %), FAIL 5047/6000 (84 %).

**Structural zero.** Each sector's noise-only BLS top 3 is fixed, and no allowed trial period lies within 0.1 % of any of its peaks:

- S6: peaks 0.9196, 5.2435, 6.4131 d; reachable: none.
- S87: peaks 0.9114, 0.9347, 0.5327 d; reachable: none.
- S98: peaks 6.4043, 0.7989, 0.5119 d; reachable: none.
- S107: peaks 0.8499, 1.1329, 7.1361 d; reachable: none.

So B_TOP3, and therefore PASS, cannot occur in these noise-only trials. **The zero PASS count is a structural zero, not an estimate of a false-PASS rate.**
Clause A's noise-only frequencies are not affected by this.

## Injection model and cleaning

Injected geometric T14 (circular, b = 0.4024; a/R* scaled with P', which holds the duration only approximately): 130 ppm 1.554-1.577 h; 185 ppm 1.558-1.581 h; 240 ppm 1.561-1.584 h.
1.5 h is clause A's scoring window, not the injected T14.
Depth is defined as clause A measures it, on the noiseless model.
Residual clause-A depth at the true ephemeris after dividing out the registration-shape model: S6 -47 +- 62 ppm; S87 -38 +- 86 ppm; S98 31 +- 25 ppm; S107 20 +- 50 ppm.
The cleaned light curves may retain model error and unrelated signals.

## Limits

- The trials share one noise realization per sector, so the frequencies carry more uncertainty than their counts suggest, and the three sectors differ (see per-sector rows).
- The trial periods avoid a 2 % band around TOI-2514.01's eleventh harmonic, which contains the candidate period (0.5719 d lies 1.6 % below 6.3951/11), so transfer to the frozen ephemeris is an assumption.
- The 11 compared scientific fields of the harness controls matched the training summaries; that is not a complete equivalence of every scorer path.
- A predictive calibration, with variation between noise realizations and null BLS peaks able to hit, would need its own design, declared before it is run and before any test photometry.
