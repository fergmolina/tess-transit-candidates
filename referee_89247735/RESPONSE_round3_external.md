# Response to the round-3 external review (Codex), 2026-10-19

Manuscript before changes: results/referee_89247735/round3_fixes/main_before_round3.tex. Revised: paper/main.tex, main.pdf (9 pp).

| # | Issue | Verdict | Action |
|---|---|---|---|
| 1 | S104 QLP timestamps wrong by ~7.5 min | **Confirmed.** QLP and TESScut have identical cadence lists, so gap edges align them exactly: QLP−TESScut = +0.20 min in S66/S93, −7.82 min at the S104 event, giving a correction of +8.02 min (scripts/s104_clock_89247735.py → round3_fixes/s104_clock.json) | Timing section rewritten; the false "≤1 min" claim was withdrawn and its correction stated in the text; S104 tc = 4196.80989 with stat/clock/extraction errors kept separate (1.4/0.2/4.0 → 4.2 min); v4 ephemeris P = 18.323176 ± 0.000040 d, residuals ≤1 min (scripts/final_ephemeris_89247735_v4.py); Fig. 1 and tables regenerated |
| 2 | 2.4σ centroid significance not calibrated | Agreed | Significance claim removed; text now says "consistent with the target, does not significantly distinguish the neighbour". **Open:** two-hypothesis injection calibration not done |
| 3 | Background EB on the neighbour not excluded | Agreed | The neighbour is now an open false-positive scenario; TRICERATOPS described as prioritisation; small-aperture ground transit named as the decisive test. **Open:** explicit EB parameter-space model not done |
| 4 | Gaia RV mass limit not derivable | Agreed | Numerical bound removed from the abstract, §5 and summary; qualitative statement only, with a ~30 MJup orientation figure |
| 5 | Shape-fit sensitivity | Partly done | Refit with corrected clock (χ² 1554→1547), with free LD under priors, and with quadratic baselines (refit_v4_*.json): k 0.098–0.099, Rp 7.9–8.5 R⊕. Text says intervals are conditional. **Open:** dilution fit, red-noise model, common-extraction comparison with Zarco |
| 6 | Contacts in utcfix files not corrected; 1σ vs ±15 min; observability | **Confirmed** (TIC 89247735 only) | *_utcfix2.csv + CORRECTION_UTC_2026-10-19b.md; v4 CSV gives geocentric contacts and CTIO altitudes; criteria stated (target >30°, Sun <−12°); both 2027 events flagged as marginal; 1σ (3.0/3.2 min) separated from the ±15-min operational window |
| 7 | "Pre-registered" fourth event | Agreed | Version roles itemised; epoch 118 described as a post hoc held-out check; noted that the public archive alone does not prove the v1-before-v2 order |
| 8 | Neighbour separation by epoch; flux fraction | Done | Gaia: 7.96″ (2016.0), 7.32/7.15/7.08″ at S66/S93/S104; 0.787 described as a TIC-based estimate |
| 9 | Bit-31 wording; the 22/40→5/40 claim | Done | Wording softened; 22/40→5/40 labelled an informal, unmatched test |
| 10 | "Roughly even" prior; Giacalone wording | Done | Prior statement removed; Giacalone scope stated accurately |
| m1–m10 | Minor issues | Mostly done | "about three years"; flag counts stated in the Table 1 note; centroid-floor heuristics cited separately; Fig. 2 caption softened; secondary-eclipse Teff assumptions stated; QLP HLSP DOI acknowledged. Not done: Boyle/TARS citation split (m8), kunimoto2022 key check (m9), removing the draft header (m10, at submission) |

Side finding: v1 (test of record) was fitted with the uncorrected S104 time. v4 is +4.4 to +5.6 min from v1 at the 2026–2027 epochs, about 1.3× v1's 1σ, so v1's frozen rules still apply.

Recommendation before deposit: one fresh referee round on the revised PDF, and ideally the two open analyses (centroid injection calibration, neighbour EB model).
