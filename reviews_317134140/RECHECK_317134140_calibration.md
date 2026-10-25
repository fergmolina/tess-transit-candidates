> Public copy (2026-10-25 (v1.18.1)): 4 local temporary paths replaced by "[reviewer temporary path redacted]". No other change.

# TIC 317134140 calibration: focused re-check

**Date:** 2026-10-25 UTC. **Reviewer:** OpenAI Codex, same reviewer as `REVIEW_317134140_calibration_plan.md`.

## Verdict

**Publish after listed changes.** The substantive inference problem is resolved by withdrawing the combined likelihood-ratio interpretation and replacing it with explicitly conditional, descriptive diagnostics. The replacement calculations reproduce exactly, including the structural zero in all four training sectors. Only two small presentation fixes remain: make the retained historical tables visibly withdrawn in their own packaging, and correct two residual claims in the current harness docstring. No calibration rerun, scientific threshold change or edit to the v1.18 scoring lock is required.

## Findings and exact fixes

| Priority / item | Status and verification | Required fix |
|---|---|---|
| Structural zero and unsupported combined evidence | **Resolved in the replacement material.** `calibration_diagnostics_317134140.py:38–44,56–71`, its generated Markdown, the new registration note (`PREREGISTRATION.md:16`) and DECISIONS 187 explicitly deny calibrated future-sector probabilities or a combined evidential-strength conclusion. The PASS ratio is not calculated by the new diagnostics. My exact interval checks confirm no reachable noise-only peak in S6, S87, S98 or S107. | None for the replacement interpretation. |
| **Small required packaging fix: retained tables are not self-labelled as withdrawn** | `interpretation_table_v1.3.md:1` still opens “declared interpretation table,” its table presents “Declared conclusion,” and its closing caveat still calls the ratios bounds. The JSON still begins with the old rule and contains active-looking conclusions without withdrawal metadata. The README calibration section and DECISIONS 187 clearly withdraw these artifacts, and the old table **script** is labelled withdrawn, but those notices do not accompany someone reading either table alone. | Add a prominent withdrawal header/metadata identifying DECISIONS 187 and linking the replacement diagnostics. Alternatively preserve the original bytes in an explicitly withdrawn archive with a conspicuous notice in the same package. Do not erase historical calculations or retroactively pretend they were never proposed. Ensure the release does not present these as current interpretations. |
| **Small required text fix: two harness-docstring claims remain unqualified** | `calibrate_317134140_scorer.py:5–6` still says the rule was logged BEFORE the script existed; lines 11–12 still promise reproduction “field for field.” These conflict with the appropriately qualified corrections in DECISIONS 187 lines 1809–1812 and the diagnostics' eleven-field description. | Replace the chronology claim with: “The author logged the rule as fixed at 02:20 UTC; available local timestamps are consistent with that account, but do not independently prove insertion time.” Replace “field for field” with “for the eleven scientific fields listed in the control comparison; this does not exercise every validation/provenance path.” Keep the as-run source hash and state these are documentation-only corrections. |
| Duration, depth sensitivity and no-data convention | **Resolved.** The current duration description distinguishes the 1.5-h scoring window from geometric T14. DECISIONS 187 records both category-change counts, the three-depth agreement count, and that assigning INSUFFICIENT LR 1 was a convention. That LR convention is no longer used in the replacement. | None. |
| Registration's interpretation and origin claims | **Resolved.** The appended note reports conditional frequencies at all three depths, explains the structural zero and harmonic exclusion, denies a quantitative combined conclusion, retains the frozen outcomes, and states a persistent dip does not distinguish a planet from a blended eclipsing binary (`amend_317134140_diagnostics.py:15–29`). | None. |

Historical claims in DECISIONS 185–186 may appropriately remain with the explicit dated withdrawal/correction in item 187. The issue above concerns the standalone table artifacts and current script documentation, not a demand to rewrite the decision history.

## Independent reproduction

I ran the inspected diagnostics script with bundled Python, `-B -I` and the existing import-path bootstrap, writing only under `[reviewer temporary path redacted]`. Both generated JSON and Markdown are **byte-identical** to the saved replacements. I separately counted all pooled and per-sector outcomes, Clause-A labels and B_TOP3 counts from the saved raw trial rows: **240/240 comparisons passed**. Evidence: `[reviewer temporary path redacted]`; source `calibration_v1.3.json`; `calibration_diagnostics_317134140.py:18–35`.

For the structural-zero check, I did not rely solely on the diagnostic's numerical grid. The locked scorer accepts a peak p at trial period P when `abs(p/P−1) <= 0.001`; therefore its exact candidate interval is `[p/1.001, p/0.999]`. Intersecting each saved peak interval with [0.53,0.70] and subtracting the declared 2% exclusion bands gives:

| Sector | Exact check |
|---|---|
| S6 | All three peak-hit intervals lie outside the trial range; none reachable. |
| S87 | Two lie outside; the 0.532684-d peak's entire hit interval lies inside the excluded TOI/12 band; none reachable. |
| S98 | Peaks at 6.404318, 0.798932 and 0.511910 d all have hit intervals outside the trial range; none reachable. |
| S107 | All three peak-hit intervals lie outside the trial range; none reachable. |

Evidence: saved `cleaned_top3` values, locked scorer `prereg_spoc_317134140.py:116`, calibration `draw_period()` and the independent interval calculation recorded in `[reviewer temporary path redacted]`.

**Nonblocking implementation note:** diagnostics lines 23–27 use a finite grid and `abs(grid/peak−1)`, whereas the scorer uses `abs(peak/P−1)`. Those tolerances differ slightly. This cannot alter any of the four current results because their intervals have ample separation from allowed support, as the exact check establishes. Before reusing the diagnostic on other inputs, prefer the exact interval test with the scorer's ratio direction; no current scientific finding needs revision.

Fresh evaluation of the circular-duration formula from saved P/rp/a values reproduces the diagnostic ranges:

| Depth | Geometric T14 range, h |
|---|---|
| 130 ppm | 1.553543–1.576802 |
| 185 ppm | 1.557573–1.580797 |
| 240 ppm | 1.561280–1.584407 |

I also independently recomputed **9/35** historical table category changes at 130 ppm, **12/35** at 240 ppm, and **19/35** agreement across all three depths. These are now appropriately historical disclosures, not a replacement evidential-strength rule. Source: saved trial parameters and withdrawn table's numerical columns, checked with Python `math` and direct category comparisons.

## Source history and immutable-prefix checks

Undoing the two documented docstring edits in the current calibration harness reconstructs the exact as-run SHA-256:

`63738417451a42d260936d68ee245600901ead09ed35ab892b61f46d6f3a6136`.

The reconstructed source is `[reviewer temporary path redacted]`. Parsing both versions and removing only the module docstring gives **identical ASTs**. The executable harness was not changed or silently rerun under a revised model.

The raw calibration JSON remains SHA-256 `d2c5b2ec162d9509afac677f55ece5a23ba544aaf4989f290d56a98d63d9c265`. Direct byte comparison with `git -C public_release show v1.18:preregistration/TIC317134140/PREREGISTRATION.md` confirms that the entire published registration is still an exact prefix. The appended text is the new descriptive calibration note, not the withdrawn interpretation plan. The old amendment generator raises `SystemExit` before reading or writing the registration (`amend_317134140_plan.py:8`). These checks used source inspection, `hashlib`, AST comparison and local Git; no amendment generator was executed.

## Limits

Only source, saved JSON/Markdown, metadata and synthetic numerical calculations were inspected. No real photometry—including training data—was opened, downloaded or reanalysed; no live select/acquire, credential or publication operation occurred. Saved recovery outcomes and residual depths were counted/checked, not independently regenerated from raw flux. Historical non-examination and the exact original log insertion time remain unauthenticated author assertions. The descriptive release is otherwise suitable once the two bounded presentation fixes above are applied; no broader scientific audit is requested by this re-check.
