# Public copy of the auditor's records (2026-11-23 (v1.22))

These are the auditor's files from its reproduction of 2026-11-19, with two differences from the originals:

- **Temporary paths redacted.** The auditor's temporary directory path is replaced by "[auditor temporary path redacted]" in 8 files
  (16 occurrences): `attempts.jsonl` (7), `audit_plan.json` (1), `env_create.log` (1), `env_install.log` (2), `env_install_retry.log` (2), `environment_fresh.json` (1), `scorer.log` (1), `validator.log` (1). Nothing else is changed.
- **No FITS file.** The light curve the auditor downloaded (`lc/`, SHA-256 `cea2619b6228e770064ed39176ad446c02320311dbd3751e15cdc0876b4331a0`, identical to the file of record) is public at
  MAST and is not copied here.

`ARTIFACT_SHA256.json` is the auditor's own list and gives the hashes of the **unredacted originals**; for the 8 redacted
files the copies here have different hashes. The hashes of the files as published are in `MANIFEST_v1.22.md`.
The report is `../REPRODUCTION_S108_auditor.md`, unchanged.
