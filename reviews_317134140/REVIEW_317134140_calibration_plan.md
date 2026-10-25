> Public copy (2026-10-25 (v1.18.1)): 4 local temporary paths replaced by "[reviewer temporary path redacted]". No other change.

# TIC 317134140 calibration and interpretation plan: external review

**Date:** 2026-10-25 UTC (2026-10-24 EDT). **Reviewer:** OpenAI Codex, same reviewer as the preceding scoring-package reviews.

**Scope and access:** I read the full calibration-plan prompt, calibration/table/amendment sources, locked scorer, relevant transit-model source, DECISIONS 185–186, saved trial JSON and training summaries, table and run log, and local Git tag v1.18. I recomputed the table and noiseless injection properties. No real photometry was opened or acquired, including the training sectors; the optional raw-data rerun was not performed under the standing access restriction.

## Verdict

**Publish after listed changes.** The arithmetic and implementation of the declared table reproduce, the frozen scorer and registration prefix are intact, and the saved calibration is useful as a conditional injection/recovery experiment. It does **not** establish the proposed quantitative likelihood ratios for future sectors. In particular, noise-only PASS is impossible anywhere in the allowed trial-period support for these fixed cleaned noise realizations. The large smoothed PASS ratio therefore cannot be called a measured ratio or a bound on future evidence. The safest small release is to publish the calibration as descriptive diagnostics, preserve the frozen per-sector outcomes, and withdraw the formal combined “strong evidence” interpretation pending a defensible predictive calibration. A transparent pre-test amendment is legitimate; it must be labelled as made after seeing this calibration. No change to the published v1.18 scoring lock is needed.

## Ranked findings and fixes

| Severity / issue | Evidence and implication | Exact fix |
|---|---|---|
| **Major: the null experiment cannot produce PASS, by construction** | `calibrate_317134140_scorer.py:63–64,68–73,89–96` reuses fixed cleaned BLS peaks and draws periods only in a restricted interval. In saved `calibration_v1.3.json`, S6 peaks are 0.919610, 5.243470 and 6.413136 d; S107 peaks are 0.849851, 1.132917 and 7.136099 d, all outside [0.53,0.70] d. S87 has 0.911401, 0.934671 and 0.532684 d; the last is inside the excluded 2% neighbourhood of TOI period/12 = 0.532928175 d. Its entire 0.1% hit window is excluded. Thus all three pooled null realizations necessarily yield B_NOT_TOP3 for every permitted trial period, and PASS is impossible. All 8000 saved H0 trials, including S98, indeed have B_NOT_TOP3. Zero pooled PASS counts are not evidence from 6000 new future-sector noise realizations. | Explicitly disclose this structural zero. Do not use the resulting PASS ratio to assign future-sector evidential strength. Either release these as conditional recovery/null diagnostics with no formal combined LR conclusions, or design a separate predictive calibration that permits relevant null BLS peaks and represents variation between noise realizations. Declare that design before running it and before test photometry is examined; retain this run and its history. |
| **Major: smoothed ratios are presented as bounds and transferable combined evidence** | `interpret_317134140_table.py:19–20,35–42,67` and the registration call the zero-count PASS ratio a “bound.” The value **3728.196** is the specified pseudocount point estimate, with no confidence level or coverage construction. Increasing the number of random-period null trials increases it approximately linearly while adding no new noise realization and leaving the structural zero unchanged. Products such as PASS + FAIL + no data = **36.8** consequently acquire an unsupported “strong evidence” label. The table also multiplies the same uncertain pooled rates as though they were known probabilities for independent future sectors. | Replace “bound” with “pseudocount-based conditional estimate; not a confidence bound or calibrated future-sector likelihood ratio.” Remove formal evidential-strength claims from this release unless the predictive model and calibration uncertainty are addressed. Keep any original numerical table explicitly exploratory and conditional. State that independence of future-sector observations and transfer of training-sector outcome rates are assumptions, not established calibration results. |
| **Moderate: depth sensitivity is incomplete in the proposed interpretation** | The 9/35 changes at 130 ppm are correct, but **12/35** change at 240 ppm and only **19/35** agree across all three depths. Example: PARTIAL + INCONCLUSIVE + INCONCLUSIVE changes from strong support at 185 ppm (16.8) to strong evidence against at 240 ppm (0.0107). These are in the saved table; I recomputed the classifications. The current default conclusion ignores both alternatives by design (`interpret_317134140_table.py:29,38–42`). | Disclose both counts and both alternative verbal categories. Prefer a pre-test depth-robust descriptive rule: report a category only if all three depth readings agree, otherwise “depth-dependent.” But do **not** represent this consensus as repairing the null/predictive-calibration defect above. If formal evidence language is removed, describe agreement of the conditional diagnostics instead. |
| **Moderate factual correction: the injected T14 is not fixed at 1.5 h** | `calibrate_317134140_scorer.py:14–16,82` scales a/R* linearly with P. Under the actual circular model (`vet.py:79–80`), that preserves duration only approximately. Using every saved P, rp and a/R* gives geometric first-to-fourth-contact durations **1.55354–1.58441 h**, depending on trial/depth. The measurement window is 1.5 h; it is not the model's exact T14. | Correct the script documentation, DECISIONS 185 and public amendment/table description to distinguish the fixed **1.5-h scoring window** from the injected registration-shape duration. The existing experiment can be published with its actual duration range. If an exact 1.5-h injection is desired, solve the circular duration relation jointly with the depth normalization and label any new run as a changed experiment; do not silently relabel this one. |
| **Minor: chronology and control claims exceed the retained evidence** | File times are consistent with the claimed order, but the current DECISIONS modification time is later than the run and does not timestamp the insertion of paragraph 185. The harness control checks eleven named scientific fields (`calibrate_317134140_scorer.py:112`), not the entire scorer output or all validation/provenance paths. Saved calibration records retain “control OK” assertions, not a full independent replay. | Say “the author logged the rule as fixed at 02:20 UTC; available local timestamps are consistent with that account” unless an immutable earlier snapshot exists. Say “the eleven listed scientific fields matched the training summaries,” not unrestricted “field for field” or proof of complete harness equivalence. Preserve the rule, code and artifacts with this release. |

These are proportional interpretation/documentation corrections. Mixed outcomes are not inherently incompatible with likelihood-ratio reasoning: under a valid model a strongly informative outcome can outweigh an adverse one. The problem here is the unestablished model and rate transfer, not the algebraic fact that PASS can outweigh FAIL.

## Sequencing and faithfulness of the table

DECISIONS 185 specifies hypotheses, depth/period sampling, trial counts, the estimator, S6/S87/S107 pooling, S98 exclusion, product combination, no-data treatment and verbal thresholds. The table script applies those choices correctly. Boundary handling is also faithful: 10 and 0.1 receive the moderate categories, while 3 and 1/3 are inconclusive (`interpret_317134140_table.py:21–26`). Depth-side trials were already specified in item 185; the extra sensitivity **display columns**, not the existence of those trials, are labelled as added after seeing the run (`interpret_317134140_table.py:57`; DECISIONS 186).

I inspected local file metadata using `stat -f '%N birth=%SB modify=%Sm'` and converted EDT to UTC:

| Artifact | Relevant UTC timestamp |
|---|---|
| DECISIONS item 185's written timestamp | 2026-10-25 02:20, self-reported in the text |
| Calibration script birth / modification | 02:21:08 / 02:21:19 |
| Calibration output birth / modification | 02:30:23 / 02:30:23 |
| Table script birth / modification | 02:22:36 / 02:30:58 |
| Current DECISIONS modification | 02:31:44 |

This is compatible with declaration before calibration, but the mutable log's age or present modification time cannot prove when item 185 was inserted. I found no independent timestamp in the materials reviewed establishing that exact insertion time. This limitation is not evidence that the account is false.

Running the table script with outputs under `[reviewer temporary path redacted]` reproduced the saved JSON and Markdown exactly. Independently recomputed counts and ratios are:

| Label | H1, 185 ppm, N=300 | H0, N=6000 | Declared smoothed ratio |
|---|---:|---:|---:|
| PASS | 93 | 0 | 3728.1960 |
| PARTIAL | 175 | 107 | 32.54811 |
| INCONCLUSIVE | 30 | 846 | 0.7183399 |
| FAIL | 2 | 5047 | 0.00987463 |

There are 35 order-free combinations: 21 labelled strong support, 7 strong against, 5 inconclusive and 2 moderate against. These numerical facts agree with DECISIONS 186. They do not establish that the verbal strengths are empirically calibrated. Reproduction evidence: `[reviewer temporary path redacted]`, `table.md`, `audit.json`, and the saved trial rows.

The estimator is a separate binary Jeffreys-style smoothed frequency for each label. The four displayed probabilities sum to **1.0033223** under H1 and **1.0001666** under H0, rather than one. This small normalization discrepancy is not the main failure, but the outputs are not a coherent categorical predictive distribution. If a formal categorical model is developed, specify its category set, coherent smoothing and treatment of insufficient-data states; disclose any change from item 185 rather than quietly replacing its estimator.

## Harness and injection model

**The conditional H0 caching is sound.** The cleaned flux, its preprocessing and BLS grid/ranking do not depend on trial P or phase. The scorer's BLS function uses P_SIG only to classify the fixed peaks and aliases (`prereg_spoc_317134140.py:109–118`); the calibration recomputes the relevant hit test at each trial period. Reusing preprocessing and top-three peaks therefore preserves the outcome calculation for this fixed cleaned realization. Random period/phase draws can be independent conditional on that realization; it would be inaccurate to say that all conditional Monte Carlo counts are invalid merely because the flux is reused. The failure arises when those conditional probabilities are transferred to unseen sector noise, especially the structural PASS zero.

Source inspection shows that `score()` calls the locked preprocessing, Clause A and outcome mapping, with P_SIG assigned to the trial period and event centres generated from trial P/T0 (`calibrate_317134140_scorer.py:54–66`). This matches the scientific path of the training mode. The full CLI's file/header/config gates are not exercised by that function. Controls compare outcomes, clauses, depth, sigma, event/null counts, top-three peaks, retained cadences and TOI-mask removal; all four logs report success. I did not independently rerun these real-data controls. Current scorer, tsearch and search_pipeline hashes match the lock, and vet.py matches the hash saved in the calibration.

Writing a temporary copy with only PDCSAP_FLUX multiplied by the removal/injection factor preserves cadence, quality, gaps and the error-column inputs used by this experiment (`calibrate_317134140_scorer.py:48–52,83–85`). It is a reasonable small-signal injection mechanism for this conditional recovery question, not a new simulation of photon noise, crowding corrections or pipeline extraction. Retaining the original uncertainty column is an approximation, not an exact generative noise model.

I independently evaluated the AST-isolated, inspected `vet.transit_model` on synthetic uniform two-minute timestamps for **all 800 saved injection parameter sets**. The mean-depth normalization agrees with the requested 130/185/240 ppm values to within **5.8×10⁻¹⁰ ppm**. Thus the radius-ratio solver does what it says for its noiseless scoring-window definition. The actual circular duration is

`T14 = P/pi * asin(sqrt(((1+rp)^2 - b^2)/(a^2 - b^2)))`,

with b=0.4024, yielding:

| Injection depth | Trials | Actual geometric T14 range, h |
|---|---:|---:|
| 130 ppm | 200 | 1.553543–1.576802 |
| 185 ppm | 400 | 1.557573–1.580797 |
| 240 ppm | 200 | 1.561280–1.584407 |

Evidence: saved P/rp/ar values, `vet.py:74–86`, and `[reviewer temporary path redacted]`/`audit.json`. Finite exposure integration and the 1.5-h measurement window are separate from these geometric contacts.

The source divides out the adopted registration model, not an independently known true signal (`calibrate_317134140_scorer.py:10–12,117`). Saved residuals are −47.18±61.73, −37.87±86.48, +31.45±25.41 and +20.13±50.03 ppm for S6/S87/S98/S107. The rounded disclosures are accurate, but this does not prove that the cleaned light curves contain only noise. Subtraction retains model error and unrelated signals. I verified those residual numbers against the JSON, not by opening the underlying flux.

The random-period injection distribution is a useful local sensitivity probe, but not an exact proxy for the frozen period. In particular the actual 0.5718634-d period lies **1.636% below TOI period/11**, inside the harmonic exclusion band used for trials. The trial design deliberately avoids a neighbourhood relevant to the actual candidate's masking/systematic interactions (`draw_period`, lines 68–73). The exclusions are transparently declared; nevertheless transfer to the fixed ephemeris requires an assumption, not an equality established by controls at one phase.

## Pooling, combinations and depth recommendation

Excluding the longer S98 training set was declared in item 185 and is reasonable for a descriptive single-sector comparison. Saved training summaries contain 91 predicted events for S98 versus 37, 41 and 44 for S6/S87/S107; saved injection PASS counts at 185 ppm are 71/100 for S98 versus 44/100, 36/100 and 13/100. These demonstrate both duration and sector heterogeneity, rather than a universal future-sector rate. Pooling three selected realizations gives equal weight to them; it does not validate exchangeability with S108–S110.

Assigning LR 1 to UNAVAILABLE/INVALID_INPUT is a sensible neutral reporting convention. INSUFFICIENT can depend on coverage and preprocessing; its probability is not established equal under both hypotheses by zero such outcomes in these trials. Label that assignment as a convention. Multiplying pooled point estimates additionally assumes conditional independence between future sectors and ignores shared calibration-rate uncertainty. A robust predictive treatment would propagate those uncertainties instead of treating the plug-in rates as known. No independent-noise or prospective validation was supplied here.

**Recommendation on depth:** adopt a transparently amended pre-test interpretation, rather than preserving an overconfident default merely because it was initially declared. The proposed three-depth agreement rule is preferable to silently privileging 185 ppm, with the 16 non-unanimous combinations labelled depth-dependent. It is not a substitute for correcting the null calibration. In the small descriptive release, report all three conditional readings and withhold formal “strong evidence” conclusions. The training depths span 127.12–209.79 ppm, and 21/150 pooled 130-ppm injections FAIL (14%); those disclosures are correct from the saved summaries and trial rows.

Adopting a revision now is legitimate **if no test photometry has been examined**, it is dated and publicly identified as a change made after seeing the calibration, and the old rule/table remain available. Do not call the revised choice fixed before this calibration. The published per-sector outcomes and scoring procedure must remain unchanged. This review cannot authenticate the non-examination condition.

## Registration, publication wording and limits

The H1 statement correctly avoids planet validation: persistence of a dip does not distinguish a planetary transit from a blended eclipsing binary. Prefer “H1 does not distinguish these origins” to any suggestion that the calibration measures equal astrophysical probabilities. The current paragraph is otherwise explicit about conditional independence, shared-noise limitations and post-calibration sensitivity disclosure, but those caveats do not rescue the formal strength labels.

Suggested replacement for the central interpretation claim:

> These experiments describe conditional recovery and outcome frequencies in three selected training noise realizations. Their noise-only BLS peaks cannot satisfy PASS anywhere in the allowed trial-period range, so the zero PASS count does not calibrate a future-sector false-PASS probability. Pseudocount ratios are exploratory diagnostics, not confidence bounds or calibrated Bayes factors. The frozen per-sector outcomes remain the outcomes of record. All three injection-depth readings are reported; disagreement is labelled depth-dependent. No quantitative combined evidential-strength conclusion is adopted from this calibration alone.

Direct byte comparison with `git -C public_release show v1.18:preregistration/TIC317134140/PREREGISTRATION.md` confirms the entire v1.18 registration is an unchanged prefix. The current lock and scorer also equal their corresponding files at tag v1.18: lock SHA `58df364513d9d2bd3f2d0c7474d069b55737420614b10eb631cf82e4eba0db41`, scorer SHA `f3f55c0d74733f8aa4ee6264b99c29c547990d885d5cfdd2c29c43c47baa1613`. These are local Git/source checks, not fresh verification of remote release availability.

Only the table/statistical computations and synthetic noiseless model evaluations were independently rerun. Real-data harness controls, cleaned residuals and injection recovery outcomes were checked as saved artifacts/source, not regenerated from flux. Temporary computation used Python with `-B` and outputs under `[reviewer temporary path redacted]`; only this report was written in the project. No credential, real photometry, live acquisition or publication action was used.
