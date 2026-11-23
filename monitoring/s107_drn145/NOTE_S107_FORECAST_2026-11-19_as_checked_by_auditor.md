# Sector 107: eligibility forecast for TIC 24526743 and TIC 160330868 (2026-11-19)

Descriptive only. The declaration is DECISIONS 252; that it was written before the run is author-reported (the log has minute stamps and
is not independently time-stamped). **No Sector 107 photometry was read.** No rule, config or evaluator
changes. When the QLP Sector 107 light curves exist, the scorer uses each file's own gaps and flags, not this forecast.
The QLP Sector 107 folder did not exist when this was made (HEAD 404 at 2026-11-19T15:15:58Z).

## Result

Number of predicted events that would be eligible under the locked edge and coverage rules (the evaluator gives INSUFFICIENT
below 2 eligible events):

| TIC | Predicted events in S107 | DRN 145 segments alone | Seven gap templates (min / median / max) | Templates with fewer than 2 |
|---|---:|---:|---:|---:|
| 24526743 | 2 (epochs 191, 192) | 2 | 1 / 2 / 2 | 3 of 7 |
| 160330868 | 2 (epochs 187, 188) | 0 | 0 / 0 / 0 | 7 of 7 |

- **TIC 160330868:** no event is eligible in any case. Epoch 187 (BTJD 4275.778) lies 0.49 d before the end of segment 225b and
  epoch 188 (4290.714) lies 0.07 d before the end of the sector; both fall in the 0.5-d trim before a gap. This agrees with the
  advance statement published with the lock (S107 primary "expected INSUFFICIENT (both events in the edge trims)").
- **TIC 24526743:** both events are eligible with the DRN 145 times alone and in 4 of the 7 templates. In the three Sector 105
  templates epoch 192 (4284.799, 1.05 d after the start of segment 226b) is lost, because those templates carry a 1.5 to 1.7 d
  QLP gap before the second orbit's mid-point break plus the 1.5-d trim after a resume. With one eligible event the outcome would be
  INSUFFICIENT. Which pattern QLP Sector 107 follows is not known.
- **The "2 of 2" for TIC 24526743 is fragile and is not the expected case.** Epoch 191 lies 0.85 d after the start of segment 225b
  and epoch 192 lies 1.05 d after the start of 226b. Both are inside the 1.5-d trim that the rule applies after a gap longer than
  0.5 d. They survive with the DRN times only because the gaps at those two breaks are 0.21 d and 0.20 d. About 0.3 d more of
  unusable QLP data next to either break removes that event, and one lost event gives INSUFFICIENT. The unmodelled Manual Exclude
  time sits near the end of each half-orbit, that is, next to these breaks; 2.03 d over four half-orbits is about 0.5 d each if
  spread evenly (the notes do not say how it is spread, and it is SPOC's flag, not QLP's). No sensitivity case was run.

## Method and limits

- Script `scripts/conformance_s107_forecast_drn145.py` (SHA-256 `b06a31ca...`), modelled on the published Sector 106 forecast;
  outputs `s107_forecast_drn145.csv` and `.txt`.
- Templates: the QLP QUALITY==0 gap patterns of Sectors 68, 69, 96 and 105 (seven sector-camera combinations of the Sector 106
  test targets), mapped onto the Sector 107 orbit-table breaks. They are examples of past QLP behaviour, not a sample of what
  Sector 107 will be; the fractions above are counts of templates, not probabilities.
- The orbit-table segment times agree with DRN 145 Table 1 to 0.008 d.
- Evaluator functions: `edge_trim` and `coverage` are imported from `scripts/prereg_conformance.py`, whose SHA-256 (`a864b07a...`)
  equals `evaluator_sha256` in both Sector 107 configs (checked 2026-11-19). The thresholds 0.90 / 0.5 / 0.5 are the evaluator's own
  (its line 255).
- Not modelled: the 2.03 d that SPOC flagged Manual Exclude for pointing excursions (the notes place them near the end of each
  half-orbit, without times; QLP's treatment is unknown); the barycentric correction; ideal 200-s cadence; clock checks; noise.
  No signal-to-noise figure is given.
- The 0.49 d of epoch 187 is 0.01 d inside the trim; a small change of the true data end would not rescue it, because the
  event also needs out-of-transit baseline on its right side.
