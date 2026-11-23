# Auditor computational reproduction: TIC 317134140, Sector 108

**Date:** 2026-11-19 UTC. **Operator:** OpenAI Codex auditor. **Instructions:** `results/PROMPT_reproduction_S108.txt`; authorization and author declaration: DECISIONS 252 and 254. Workspace: `/Users/fernando/Desktop/NASA`.

## Result: PARTIAL reproduced; exact equality not achieved

I independently downloaded the specified light curve from MAST, confirmed that its SHA-256 equals the file of record, installed the five recorded software versions in a fresh virtual environment, and executed the unmodified locked scorer **once**. It returned **PARTIAL**; the requested validator returned **BOUND**. The output is **not byte-identical**: 20/22 top-level fields and 49/56 scalar or empty-list leaves are exactly equal. Seven floating-point leaves differ, with absolute differences from approximately 8.6 × 10⁻¹³ to 8.8 × 10⁻¹² in their respective units. The main stacked depth, event/cadence counts, peak periods and outcome are exactly equal. All differences are retained below; none was exempted or rounded away to obtain an equality verdict.

Thus the declared exact-field/byte comparison **does not pass**. The published numerical precision and outcome are reproduced. This is one additional computation of the same observational data, not another observational test, a planet confirmation, or a replacement for the result of record. I do not decide which unrounded value is right. Evidence: `results/reproduction_317134140_S108_auditor/scorer.log`, `validator.log`, `result_S108.json`, and `comparison.json`.

The separate S107 forecast's saved eligibility counts check out within the metadata-only checks described below, but its “not the expected case” wording is unsupported and should be corrected before publication. A related log statement about the absence of a noise figure is also false as written.

## Scope, declaration and preserved records

Below **A** means `results/reproduction_317134140_S108_auditor/`; **O** means `results/test_317134140/S108/`; other paths are workspace-relative.

Before downloading or scoring, I wrote A/audit_plan.json at **15:36:44.686917 UTC**, specifying one scoring run, no output replacement, exact comparisons with no exemptions, and retention of failures. I first checked the input hashes against the lock, the recorded result and RESULT_S108.md. I then checked them again immediately before scoring and after the run. A/protected_inputs_after.json reports no changes among the protected paths, including every existing file under O. Nothing under O was written. The original outcome remains PARTIAL.

This is independently executed by the auditor relative to the author's Claude re-execution, but **on the same computer and with the same locked implementation**. The Python base interpreter is also the same installed Python 3.12.15. It is not an independent algorithm, independent hardware replication, or a blind measurement; I knew the recorded outcome and values. Shared implementation errors can reproduce.

## Input integrity and acquisition

Full SHA-256 values were checked using `hashlib.sha256` against the relevant lock entry and recorded artifacts, not merely the shortened prompt strings:

| Input | SHA-256 |
|---|---|
| `scripts/prereg_spoc_317134140.py` | `f3f55c0d74733f8aa4ee6264b99c29c547990d885d5cfdd2c29c43c47baa1613` |
| `configs/conformance/317134140_spoc_S108.json` | `b4f091bc63a595a2c78c3ddb9645ba846ba21e73d75aca55ca2db7e1acffb42b` |
| `configs/conformance/LOCK_2026-10-24_317134140.json` | `58df364513d9d2bd3f2d0c7474d069b55737420614b10eb631cf82e4eba0db41` |
| `results/vet/317134140/predicted_transits_S108_S109_S110.csv` | `63e98fc87ebc6ce65198e066028d7f9ea58d24b51b35771d9fc551c41f59deb3` |
| `scripts/tsearch.py` | `3b691ffc47054cb898b199fa19f0e952a04c3574833de0154eb03ae9bbe54b05` |
| `scripts/search_pipeline.py` | `34e56bb1016ac31c45c73aed4115301cdcbab46977363dbb57ab060178ef2415` |
| `scripts/spoc_selection.py` | `600e9504a811ac14c10c8129324e9f5707c3103be85bd1d5961d47bafac4ac05` |
| S108 light curve, both copies | `cea2619b6228e770064ed39176ad446c02320311dbd3751e15cdc0876b4331a0` |

The lock file also matches its public copy. The validator's own hash and the selection/acquisition/result hashes are retained in A/audit_plan.json. The scorer, helpers, config, lock and predictions were not edited or copied into modified substitutes.

The authorized file is `tess2026250081459-s0108-0000000317134140-0310-s_lc.fits`. My successful request used the MAST Download API with exactly `mast:TESS/product/` plus that filename. MAST redirected to the corresponding `stpubdata.s3.us-east-1.amazonaws.com/tess/public/tid/s0108/0000/0003/1713/4140/` object. The response was HTTP 200, `application/fits`, **2,001,600 bytes**, and the resulting SHA matched the local original exactly. Request time: **15:37:40.612436–15:37:41.421214 UTC**. Evidence: A/download_attempt2.json and the new A/lc/ file, checked as bytes before the scorer opened it. The HTTP Last-Modified header was retained but is not interpreted as the first public release time.

## Environment and complete attempt history

The scoring environment was created with `/opt/homebrew/bin/python3.12 -B -m venv` in the unique temporary directory recorded in A/audit_plan.json. It was **not** the project's `.venv`. Packages were independently installed from PyPI with explicit pins for the five recorded versions. A/environment_fresh.json and A/requirements_fresh.txt record the environment actually used.

| Component | Recorded result | Fresh scorer environment |
|---|---|---|
| Python | 3.12.15 | 3.12.15 |
| numpy | 2.5.4 | 2.5.4 |
| scipy | 1.18.1 | 1.18.1 |
| astropy | 8.0.2 | 8.0.2 |
| wotan | 2.0 | 2.0 |

The published five-version record is not a complete dependency lock. The fresh environment installed **Numba 0.68.1**, whereas the project's current `.venv` has **0.68.0**; its `astropy-iers-data` is also newer (**0.2026.11.16.0.37.44** versus **0.2026.10.12.1.3.27**). The comparison environment inventory was obtained through package metadata only. It describes the project's environment today, not independently proven versions of every dependency on November 13. These differences are possible explanatory leads, **not a demonstrated cause** of the floating-point discrepancies. I did not downgrade dependencies or rerun to chase equality.

| Attempt | Outcome / evidence |
|---|---|
| Fresh environment creation | Success; A/env_create.log. |
| Initial pinned installation in sandbox | Failed because PyPI DNS resolution failed; pip's internal retries and final error are preserved in A/env_install.log. No scorer execution occurred. |
| Initial MAST request in sandbox | Failed DNS resolution; A/download_attempt1.json retains the exception. No FITS was obtained by that attempt. |
| Network-enabled MAST retry | Success, correct SHA; A/download_attempt2.json. |
| Network-enabled pinned-install retry | Success; A/env_install_retry.log. No substituted package versions. |
| Locked scorer, one invocation | Exit 0, PARTIAL; **15:38:29.120853–15:38:55.182059 UTC**; A/scorer.log. |
| Validator, one invocation | Exit 0, BOUND; **15:38:55.182923–15:38:55.227763 UTC**; A/validator.log. |

The exact command arrays, executable path and UTC times are preserved in those logs and A/attempts.jsonl. In compact form, from the workspace root:

```text
<fresh-python> -I -B scripts/prereg_spoc_317134140.py
  --config configs/conformance/317134140_spoc_S108.json
  --lc <absolute A/lc/tess2026250081459-s0108-0000000317134140-0310-s_lc.fits>
  --out <absolute A/result_S108.json>

<fresh-python> -I -B scripts/validate_nonclock_inputs.py
  --lock configs/conformance/LOCK_2026-10-24_317134140.json
  --stage result --config configs/conformance/317134140_spoc_S108.json
  --selection <absolute results/selection_records/317134140/S108/sel_20261113T195427Z.json>
  --acquisition <absolute O/acquisition_S108.json>
  --lc <absolute A/lc/tess2026250081459-s0108-0000000317134140-0310-s_lc.fits>
  --result <absolute A/result_S108.json>
```

`-B` prevents Python bytecode writes alongside source files. The Numba cache and helper output directory were redirected into the auditor's temporary directory; `TSEARCH_SOURCE=spoc` was explicit. No scoring algorithm or scientific input was changed. The validator binds the independently downloaded identical bytes to the **original** selection/acquisition provenance; its BOUND output is not a record of my new download. That is what A/download_attempt2.json supplies.

## Comparison with the outcome of record

There are exactly 22 top-level fields. Twenty are exactly equal; `sigma_ppm` and `top3` differ. At leaf level, 49/56 are exactly equal. All seven differences are listed here; signed difference means auditor minus original:

| Field | Original | Auditor | Signed difference |
|---|---:|---:|---:|
| `sigma_ppm` | 54.98724022369697 | 54.98724022369818 | +1.2079226507921703e-12 |
| `top3[0].depth_ppm` | 451.0049228755831 | 451.00492287558563 | +2.5579538487363607e-12 |
| `top3[0].sde` | 7.071402562443457 | 7.0714025624421195 | −1.3375967000683886e-12 |
| `top3[1].depth_ppm` | 914.2455391711887 | 914.24553917118 | −8.753886504564434e-12 |
| `top3[1].sde` | 6.247188402010623 | 6.2471884020091935 | −1.4299672557172016e-12 |
| `top3[2].depth_ppm` | 326.6315648333144 | 326.6315648333212 | +6.764366844436154e-12 |
| `top3[2].sde` | 5.697226657153764 | 5.697226657152909 | −8.553158181712206e-13 |

Original JSON SHA-256: **bc62b2495c66d18c86ec5078f44abb14d965d9f2ff7dc3c02e2742d46d316b54**.

Auditor JSON SHA-256: **7ad62764472ad88fadb651c6526b49d527e3e13244803cd16a70430607900f26**.

The full leaf-by-leaf table is appended below, and A/comparison.json preserves both values, types/equality checks, signed numeric differences and the top-level comparison. No approximate tolerance was used to mark fields equal. I did not perform a second scoring run, and do not claim bitwise portability from this result.

## Check of the author's earlier re-execution

I independently compared `results/reproduction_317134140_S108/rerun_result_S108.json` with O/result_S108.json and reread that folder's README, rerun.log and comparison.json. The **22/22 equal fields and byte identity are correct** for that re-execution; both hashes are `bc62b249...`. The saved log reports PARTIAL, scorer exit 0 and validator BOUND/exit 0 at the stated 15:16:36–15:16:38 UTC times. A/claude_reexecution_check.json records my comparison.

The revised README appropriately describes the same operator/machine, qualifies the declaration's timing, and no longer claims that two executions prove determinism. DECISIONS 253's original “deterministic here” wording is qualified by dated item 254. I cannot independently establish that there were no unrecorded earlier attempts or prove when the editable declaration was inserted. The retained records support the narrower account. The fact that the author's rerun is byte-identical does not erase the auditor's seven differences.

## Sector 107 forecast: checks and corrections

I read `results/s107_drn145/NOTE_S107_FORECAST_2026-11-19.md`, the forecast script and CSV/text outputs, both S107 configs and their frozen prediction CSVs, and the evaluator's `edge_trim`/`coverage` definitions. I independently extracted text from the local **DRN 145 PDF**, visually checked Table 1 (printed page 1), and read the pointing/Manual Exclude discussion (§1.2, printed pages 2–3) and noise-figure captions. The PDF SHA is `0eb0a443508a67e7f2586f75f3949599762e62eed03c3eb9f42e4bf258180492`. My attempted web opening of the official DRN URL failed; the document check is therefore of the retained local PDF, not a fresh archive-byte verification.

The forecast script SHA is `b06a31ca15884ca3c764112566b3636c6066dd7b30dff40a2aed1c6433751c05`. The evaluator SHA **a864b07ace8d3220a2d94a60513a488c8a5d87b54f41ebf510ff40ef1755311f** agrees with both configs. Both prediction CSV hashes match their configs. The source filters target IDs and the allowed historical sectors **before** opening template FITS. I did **not** run that script, since it reads historical template photometry beyond this audit's authorized S108 computation.

Instead, A/forecast_metadata_check.py uses only synthetic cadence times. It extracts the exact two pure time/coverage functions from the inspected evaluator source, supplies their unchanged constants, uses the frozen prediction rows, and separately constructs the DRN-only cadence grid from Table 1. It also reconstructs the seven scenarios from the **rounded aggregate gap descriptions already saved in the forecast text**. This latter check is not a raw-template reconstruction and cannot verify the original gap extraction or every rounded coverage fraction.

| TIC | Prediction epochs | DRN-only eligibility, independently recomputed | Template eligibility counts from saved CSV, also reproduced using rounded summaries |
|---|---|---|---|
| 24526743 | 191, 192 | Both eligible: 2 | 2, 2, 2, 2, 1, 1, 1; min/median/max = 1/2/2; 3/7 below two |
| 160330868 | 187, 188 | Neither eligible: 0 | 0 in all seven; 7/7 below two |

The matching integer/epoch results are recorded in A/forecast_metadata_check.json. The threshold combination is indeed in-transit coverage ≥0.90 and left/right baseline coverage ≥0.5; the locked evaluator requires at least two eligible events. The published advance INSUFFICIENT expectation for TIC 160330868 is present in public DECISIONS item 166. These are conditional coverage results, not measurements of those stars or unconditional forecasts of the final scorer outcome.

The DRN lists **2.03 days** of SPOC Manual Exclude flags, related to pointing excursions and reaction-wheel frequency crossings. The text places relevant excursions near half-orbit ends; it does not allocate that total evenly or provide a target-specific QLP mask. Omitting those unknown masks, barycentric/clock effects and noise is clearly disclosed. The note is right to describe sensitivity to an extension of the short gaps: the DRN gap widths are **0.20972, 0.20972 and 0.20278 d**. Approximately another 0.3 d can cross the 0.5-d threshold and activate the 1.5-d post-resume trim. This mechanism is sound, but no probability for it is established.

### Required wording corrections before publishing the forecast/account

| Issue | Evidence | Exact correction |
|---|---|---|
| “2 of 2 … is not the expected case” is unsupported | NOTE Result third bullet. Four of seven selected template scenarios give two eligible events; the note itself correctly denies that their frequencies are probabilities. Neither an actual S107 QLP mask nor a probability model is available in the calculation. | Replace the bold sentence with: **“The ‘2 of 2’ for TIC 24526743 is a fragile conditional scenario, not an established expectation. The present scenarios do not determine the probability of retaining both events.”** Keep the following threshold explanation and the unknown-QLP-treatment qualification. |
| “No published Sector 107 noise figure” is false literally | DECISIONS 252(B). DRN 145 Figure 4 describes a SPOC two-minute MAD diagnostic; Figure 5, printed page 8, describes 1-hour CDPP versus magnitude for 12998 light curves. I verified the captions in text extracted directly from the PDF; I did not extract star measurements from the plotted points. | Add a dated log correction: **“DRN 145 includes SPOC noise/precision figures. They do not establish target-specific QLP SAP noise for these two held-out tests, so this forecast reports coverage only and no SNR.”** Preserve the historical entry. |
| Mixed timing bases in “0.07 d before the end” | For epoch 188, frozen tc = 4290.71394. DRN end 4290.77381 gives **0.05987 d ≈0.06 d**; the orbit-table-derived end 4290.7820507 gives **0.0681107 d ≈0.07 d**. The nearby 0.85/1.05-d statements use the DRN segment starts. | Say: **“Epoch 188 is 0.05987 d before the DRN sector end (0.06811 d before the orbit-table-derived end); it is lost in both forecast constructions.”** Label which timing basis is used rather than mixing them. |

The maximum orbit-table/DRN discrepancy is **0.00824405856 d**, approximately **11.87 minutes**. “To 0.008 d” is understandable rounding but should not be read as a strict ≤0.008-d bound. Use “about 0.00824 d” if quoting the bound. For epoch 187 the DRN end-minus-midtime difference is **0.48562 d**; its in-transit coverage is only about 0.37 and right baseline is zero in the DRN-only construction. A small minute-scale change of end time does not restore the required right-hand baseline, consistent with the note's caution. Evidence: frozen prediction rows and A/forecast_metadata_check.json.

Other limitations worth retaining explicitly: the templates are selected examples, one retained example per sector/camera, rather than independent draws from a predictive distribution; only their aggregate rounded summaries were independently reconstructed here. The original source's asserted seven-template count and matching evaluator do not by themselves establish a complete hash-locked template data provenance. The historical HEAD-404 claim is author-recorded at a stated time; I did not reconstruct past archive availability or query/open the S107 folder. None of these checks authorizes changing the primary tests or their rules.

## Publication wording for this reproduction

An accurate short account would be:

> On 2026-11-19, the Codex auditor independently downloaded the same S108 SPOC light curve from MAST and verified its original SHA-256. One execution of the unchanged locked scorer in a fresh environment matching the five recorded software versions returned PARTIAL, and the binding validator returned BOUND. The output was not byte-identical: seven floating-point leaves differed by at most 8.8 × 10⁻¹² in their respective units, while the published precision and outcome agreed. All differences and attempts are retained. The original result remains the outcome of record. This is a computational reproduction on the same host, not another observational test or an independent implementation.

Do not replace this with “all fields equal,” “byte-identical,” “determinism proved,” or a new PASS label. Preserve the original v1.20/v1.21 bytes and add dated pointers in any later release for their historical “no reproduction made or decided” statements. I made no publication changes.

## What I did not do

No second scorer run; no trial with Numba changed to match the current project environment; no modified scoring implementation; no new detrending, fold, period search, centroid analysis or parameter fit beyond what the locked scorer itself performs. No exploratory script or original S107 forecast script was run. No S109/S110 photometry of TIC 317134140, no S107 photometry of TIC 24526743 or TIC 160330868, and no test-sector photometry of any other frozen star was downloaded, opened or analysed. I did not open the historical template FITS either. I did not publish, push, upload or contact anyone. All new project artifacts are in A and this report; protected original files passed the after-check unchanged.

## Appendix: every output leaf

The table below is generated from the exact saved JSON comparison. “Same” means identical type and value, not agreement within a tolerance. Slash-separated paths identify nested fields; array indices are zero-based. Empty `alias_hits` is included as an empty-list leaf. All dictionary key sets and list lengths agree.

| Field | Original value | Auditor value | Exact equality |
|---|---|---|---|
| `/alias_hits` | `[]` | Same | equal |
| `/clause_a` | `"A_CONSISTENT"` | Same | equal |
| `/clause_b` | `"B_NOT_TOP3"` | Same | equal |
| `/config_sha256` | `"b4f091bc63a595a2c78c3ddb9645ba846ba21e73d75aca55ca2db7e1acffb42b"` | Same | equal |
| `/depth_ppm` | `206.33598689023813` | Same | equal |
| `/helper_sha256/search_pipeline` | `"34e56bb1016ac31c45c73aed4115301cdcbab46977363dbb57ab060178ef2415"` | Same | equal |
| `/helper_sha256/tsearch` | `"3b691ffc47054cb898b199fa19f0e952a04c3574833de0154eb03ae9bbe54b05"` | Same | equal |
| `/lc_file` | `"tess2026250081459-s0108-0000000317134140-0310-s_lc.fits"` | Same | equal |
| `/lc_sha256` | `"cea2619b6228e770064ed39176ad446c02320311dbd3751e15cdc0876b4331a0"` | Same | equal |
| `/n_cadences` | `11862` | Same | equal |
| `/n_eligible` | `28` | Same | equal |
| `/n_null` | `200` | Same | equal |
| `/n_predicted` | `48` | Same | equal |
| `/outcome` | `"PARTIAL"` | Same | equal |
| `/provenance/BJDREFF` | `"0.0"` | Same | equal |
| `/provenance/BJDREFI` | `"2457000"` | Same | equal |
| `/provenance/CAMERA` | `"3"` | Same | equal |
| `/provenance/CCD` | `"4"` | Same | equal |
| `/provenance/DATA_REL` | `"146"` | Same | equal |
| `/provenance/DATE` | `"2026-11-07"` | Same | equal |
| `/provenance/ORIGIN` | `"NASA/Ames"` | Same | equal |
| `/provenance/PROCVER` | `"spoc-6.1.1-20261030"` | Same | equal |
| `/provenance/SECTOR` | `"108"` | Same | equal |
| `/provenance/TICID` | `"317134140"` | Same | equal |
| `/provenance/TIMEREF` | `"SOLARSYSTEM"` | Same | equal |
| `/provenance/TIMESYS` | `"TDB"` | Same | equal |
| `/provenance/TIMEUNIT` | `"d"` | Same | equal |
| `/script_sha256` | `"f3f55c0d74733f8aa4ee6264b99c29c547990d885d5cfdd2c29c43c47baa1613"` | Same | equal |
| `/sector` | `108` | Same | equal |
| `/sigma_ppm` | `54.98724022369697` | `54.98724022369818` | **different** |
| `/software/astropy` | `"8.0.2"` | Same | equal |
| `/software/numpy` | `"2.5.4"` | Same | equal |
| `/software/python` | `"3.12.15"` | Same | equal |
| `/software/scipy` | `"1.18.1"` | Same | equal |
| `/software/wotan` | `"2.0"` | Same | equal |
| `/spoc_pipeline_field` | `"0310"` | Same | equal |
| `/toi_mask_removed` | `363` | Same | equal |
| `/top3/0/depth_ppm` | `451.0049228755831` | `451.00492287558563` | **different** |
| `/top3/0/duration_h` | `1.0` | Same | equal |
| `/top3/0/n_transits` | `13` | Same | equal |
| `/top3/0/period` | `1.1467482565083589` | Same | equal |
| `/top3/0/sde` | `7.071402562443457` | `7.0714025624421195` | **different** |
| `/top3/0/t0` | `4294.24740476184` | Same | equal |
| `/top3/1/depth_ppm` | `914.2455391711887` | `914.24553917118` | **different** |
| `/top3/1/duration_h` | `1.0` | Same | equal |
| `/top3/1/n_transits` | `3` | Same | equal |
| `/top3/1/period` | `8.022169864227612` | Same | equal |
| `/top3/1/sde` | `6.247188402010623` | `6.2471884020091935` | **different** |
| `/top3/1/t0` | `4301.12240476184` | Same | equal |
| `/top3/2/depth_ppm` | `326.6315648333144` | `326.6315648333212` | **different** |
| `/top3/2/duration_h` | `1.0` | Same | equal |
| `/top3/2/n_transits` | `19` | Same | equal |
| `/top3/2/period` | `0.9302391435162888` | Same | equal |
| `/top3/2/sde` | `5.697226657153764` | `5.697226657152909` | **different** |
| `/top3/2/t0` | `4294.25990476184` | Same | equal |
| `/version` | `"1.3"` | Same | equal |
