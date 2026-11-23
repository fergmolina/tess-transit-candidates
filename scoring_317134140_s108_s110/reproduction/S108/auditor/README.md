# Auditor computational reproduction of TIC 317134140, S108

Date: 2026-11-19 UTC. Operator: OpenAI Codex auditor, same host, freshly installed environment and independent MAST download.

Outcome: PARTIAL; validator: BOUND. Exact equality NOT achieved: 20/22 top-level fields and 49/56 leaves are exactly equal; seven floating-point leaves differ. JSON bytes differ. See comparison.json and ../REPRODUCTION_S108_auditor.md. No tolerance rule was substituted for the declared exact-equality comparison.

The scorer was executed exactly once. Initial sandbox DNS failures for pip and MAST are retained; network-enabled retries succeeded before scoring. All attempt logs are preserved. The existing original result and all protected files were left unchanged.

Files: audit_plan.json (declaration and before hashes), attempts.jsonl and setup logs, download_attempt1.json and download_attempt2.json (the latter binds the newly downloaded lc/ file), environment_fresh.json and requirements_fresh.txt, environment_original_current.json (current project environment, not a historical full lock), scorer.log, validator.log, result_S108.json, comparison.json, protected_inputs_after.json, claude_reexecution_check.json, forecast_metadata_check.py/.json/.log. Setup/network helper scripts are an execution record, not a new scoring procedure; do not rerun them over existing outputs.

The only S108 photometric computation was the unmodified locked scorer. No other target/test-sector photometry was accessed. The forecast check used synthetic cadence times and saved aggregate gap summaries; it did not open template FITS files. The original forecast script was not run.
