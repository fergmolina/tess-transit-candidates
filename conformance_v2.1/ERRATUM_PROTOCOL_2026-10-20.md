# Erratum to the pre-registration protocol (PREREG_PROTOCOL.tex / .pdf v1.3, Zenodo 10.5281/zenodo.23477866), 2026-10-20

Published before any Sector 106 photometry of a test target was examined. The protocol PDF is not edited; this dated erratum accompanies it.

The protocol's text gives the first TESS prediction of TIC 120444365 as "epoch 559 at 2026-07-12 21:51 UTC (sigma 4.7 min)". The time
is the v2 value of record (geocentric UTC, v2_utcfix CSV), but **4.7 min is the superseded v1 sigma** (predicted_transits_2026_2027.csv,
SHA-256 64b5b026...). The v2 CSV of record (SHA-256 32b5e085...) gives **sigma 2.1 min** for every S106 epoch, consistent with the
protocol's own table row ("T0 BTJD 4218.97007 +- 2.1 min"). Effect: the min() timing gate for this test is 3 x 2.1 = 6.3 min, not
14.1 min; the max() gate of record is 30 min either way. The other two first-epoch entries on that line (TIC 80387959 epoch 498,
01:20 UTC, 3.5 min; TIC 183374279 epoch 245, 21:14 UTC, 2.7 min) were checked against their v2 CSVs and are correct.

## Which document governs the documents
- This governance statement defines the precedence between documents.
- The evaluator docstring defines the computation, including the overrides listed here.
- The procedure document summarises both, and must agree with them.
- The outcome of record is always the evaluator's `outcome` field. If a disagreement between the code and this statement is found after
  scoring, the code is not changed and the outcome is not re-labelled. The disagreement is reported next to the outcome, together
  with the outcome the statement's wording would have given. It is never resolved in a way that turns a non-RECOVERED outcome into
  RECOVERED.

See also GOVERNANCE_S106_TESTS_2026-10-20.md (precedence of documents and all departures of the conformance procedure from the protocol).
