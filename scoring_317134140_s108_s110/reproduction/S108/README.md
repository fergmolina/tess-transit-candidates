# Re-executions of the locked Sector 108 computation, TIC 317134140. PARTIAL UNCHANGED.

Published 2026-11-23 (v1.22). This folder is **not a new test result**. The Sector 108 outcome of record is PARTIAL
(`../../results/S108/RESULT_S108.md`, v1.20; `result_S108.json`, SHA-256 `bc62b2495c66d18c86ec5078f44abb14d965d9f2ff7dc3c02e2742d46d316b54`), and nothing here replaces it. No lock, config,
scorer, validator or prediction file changed. These are checks that the computation can be repeated, not new observations.

Three executions of the locked scorer on this light curve now exist: the run of record (2026-11-13) and the two below (2026-11-19). The exploratory analysis of v1.21 also recomputed the gate through the scorer's functions. The file of record was downloaded a second time, by the auditor, with the same SHA-256.

1. **Same operator, same machine (Claude, under the author's direction).** One run. The output is byte-identical to the result of record (22 of 22 fields; SHA-256 `bc62b2495c66d18c86ec5078f44abb14d965d9f2ff7dc3c02e2742d46d316b54`), and the validator answered `BOUND`. Two executions gave identical bytes; that does not test the code, the environment or the machine independently.
   Records: `same_operator/` (start with its README).
2. **The auditor, a different operator on the same host (fresh environment, its own download).** In the auditor's words: "On 2026-11-19, the Codex auditor independently downloaded the same S108 SPOC light curve from MAST and verified its original SHA-256. One execution of the unchanged locked scorer in a fresh environment matching the five recorded software versions returned PARTIAL, and the binding validator returned BOUND. The output was not byte-identical: seven floating-point leaves differed by at most 8.8 × 10⁻¹² in their respective units, while the published precision and outcome agreed. All differences and attempts are retained. The original result remains the outcome of record. This is a computational reproduction on the same host, not another observational test or an independent implementation." The seven differing values are the random-phase sigma and the depth and SDE of the three BLS peaks. The stacked depth, all counts, the three peak periods, both clauses and the outcome are exactly equal. The declared exact comparison therefore does not pass. A possible lead named by the auditor, not a demonstrated cause, is a different Numba version (0.68.1 against 0.68.0); the five recorded software versions are not a complete dependency lock. Nobody decides which unrounded value is right, and nothing was re-run to obtain equality.
   Records: `REPRODUCTION_S108_auditor.md` (the auditor's report) and `auditor/`.

## Limits
- Both runs used the same locked code on the same computer. Neither is an independent implementation or independent hardware. An
  error in the code would repeat in all three executions.
- The auditor knew the recorded outcome and values. Its reproduction was recommended in its own review of v1.20 (section 5) and was
  declared in the log before it was run (DECISIONS 252; author-reported order, minute stamps).
- Nothing here says anything new about the star. PARTIAL is not a confirmation.
- The auditor's report also checks the Sector 107 eligibility forecast (`../../../monitoring/s107_drn145/`).

## Paths
The reports were written in the author's workspace and name its paths. In this release:

| Path in the reports | Here |
|---|---|
| `results/reproduction_317134140_S108/` | `same_operator/` |
| `results/reproduction_317134140_S108_auditor/` (also "A") | `auditor/` |
| `results/REPRODUCTION_S108_auditor.md` | `REPRODUCTION_S108_auditor.md` |
| `results/test_317134140/S108/` (also "O") | `../../results/S108/` |
| `results/PROMPT_reproduction_S108.txt` | `../../../reviews_v1_22/PROMPT_reproduction_S108.txt` |
| `results/s107_drn145/`, `scripts/conformance_s107_forecast_drn145.py` | `../../../monitoring/s107_drn145/` |

Log entries: DECISIONS 252-255.
