# Response to the round-5 external review (Codex), 2026-10-19

Verdict: minor revision; v1.9 held until the release-summary errors were fixed. Every blocking item is addressed:

| Item | Action |
|---|---|
| ≤1.2σ excludes TIC 89247735 (reaches 1.38σ) | Addendum b now gives the separate ranges: seven objects ≤1.2σ; TIC 89247735 v5−v1 1.25–1.38σ (checked with the frozen CSV errors); about 1.4σ overall. It also states that tests are evaluated around the frozen prediction, with the corrected one reported for information |
| S100–S102 grouping and cause | Rewritten as measured, product-specific behaviour: S102 for TIC 258006047 is missing its term (−1.2 s), like S103–S105; S100–S101 carry spurious −2.08 / +4.60 min. MAST's dating of the mix-up (Orbit 215, S102) is cited; no per-sector cause is assigned |
| "Within 5 s" | "About 5 s (5.1 s)" |
| Clock implementation | qlp_clock_v2.py evaluates the light-travel time at spacecraft time, uses unique control sectors excluding S74–S79 v01, and verifies equal-length cadence lists. Re-run: corrections change by <0.01 s (89247735: +7.533124, matching the review's +7.533125). v5 unaffected; previous outputs kept in results/qlp_clock_v2/prev_round4/ |
| 0.05-min clock term | Labelled an adopted conservative allowance in the text and addendum |
| Background/position diagnostic | Windows, statistic and limits stated in the text (descriptive ratios on a ramping baseline; no trend-aware test) |
| Table 1 "28"; §3.3 rounding; +5.4 endpoint; "≤1 min" | Fixed (27; +0.0020 / −2.3; generator now includes epoch 163 → +5.5; "about 1 min") |
| k ≤ 0.11 "of the host's light" | Now "projected disk (≈1.5 % of light at disk centre with limb darkening)" |
| ≤0.3 min vs clock change | Distinguished in the text (−0.49 min clock change v4→v5 is a separate effect) |
| v4 shape JSONs | Released under their own names and labelled as fitted with the earlier +8.02-min clock; not called a v5 posterior |
| Console "v4:" label; make_figure1 docstring | Fixed |
| Manifest | MANIFEST_v1.9.md lists every released file, its role and its supersession status |
| Round-4 response accuracy | A dated correction is appended to it (not silently rewritten) |
| Not done | Stale unused macros in the generated table file; Lightkurve citation; per-result version attribution of zarco2026; MCMC convergence diagnostics |
