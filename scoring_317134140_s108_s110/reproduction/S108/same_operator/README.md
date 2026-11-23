# TIC 317134140, Sector 108: re-execution of the locked computation (2026-11-19)

**What this is.** A second execution of the locked scorer on the file of record. The declaration is DECISIONS 252 (stamped
15:16 UTC; the run started 15:16:36 UTC). That the declaration was written first is author-reported: minute stamps cannot show the
order and the log is not independently time-stamped. It was made by the same operator (Claude, under the author's direction) on the same machine and in the same
software environment as the run of record of 2026-11-13.

**What this is not.** It is not the independent reproduction recommended by the external reviewer (review of v1.20, section 5):
that needs a different operator. It is not a second observational test, and it does not replace the outcome of record
(`result_S108.json`, PARTIAL).

## Result

The new output is **byte-identical** to the result of record: 22 of 22 fields equal, same SHA-256
(`bc62b2495c66d18c86ec5078f44abb14d965d9f2ff7dc3c02e2742d46d316b54`). Outcome PARTIAL; depth 206.336 ppm, sigma 54.987 ppm,
28 of 48 events eligible, 200 shifts, top-three periods unchanged. The validator, stage `result`, answered `BOUND` on the new output.

| Item | Value |
|---|---|
| Run | one, 2026-11-19 15:16:36 to 15:16:38 UTC, `python -I`, no `--insample-check` (`rerun.log`) |
| Inputs, unmodified | scorer `f3f55c0d...`, config `b4f091bc...`, lock `58df3645...`, prediction CSV `63e98fc8...`, light curve `cea2619b...` (the local file of record; no new download) |
| Software | Python 3.12.15, numpy 2.5.4, scipy 1.18.1, astropy 8.0.2, wotan 2.0 (as recorded in the result of record) |
| Comparison rule (fixed before the run) | every field equal, no exempt field (`comparison.json`) |
| Attempts | one; no exception, `INVALID_INPUT` or `REFUSED` |

## What it shows, and its limits

- Two executions on this machine, six days apart, gave identical bytes from the same inputs. That is evidence against the result
  of record depending on an unrecorded state of the first run; two runs do not prove determinism.
- It does not test the code, the environment or the machine against an independent one. An error shared by both runs would repeat.
- It says nothing new about the star. The 1.96-sigma interval stays nominal and PARTIAL is not a confirmation.
- The in-sample re-scores and the 196 lock tests were not repeated (declared).
- The statements "one locked scoring run" and "none has been made or decided" in `RESULT_S108.md` describe the record at v1.20;
  that file is unchanged.
