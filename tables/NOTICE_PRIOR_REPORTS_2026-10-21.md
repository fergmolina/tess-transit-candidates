# Dated notice on the prior_report columns (2026-10-21)

The CSV files are kept byte-for-byte as published. Read their prior_report entries with these corrections
(prior_search/ERRATUM_PRIOR_DETECTIONS_2026-10-21.md; matches require the TIC and a period column in the same record, P, P/2 or 2P within 0.1 %):

| File | TIC | Published | Read as |
|---|---|---|---|
| allsky_classA_round2_outcomes.csv | 249813122 | none | prior machine detection: first-stage RAVEN candidate (Lafarga et al. 2026), P = 4.17453 d |
| allsky_round3_outcomes.csv | 122522485, 159033763, 162304222 | none found | no candidate report found; a period within our matching tolerance appears in eumemic/exoplanets' public raw BLS table (results_public/all_signals.csv.gz), a raw search output, not a promoted or validated candidate |
| allsky_round3_outcomes.csv | 196514928, 283913390 | none found | eumemic/exoplanets' false-alarm classifier table (validation/false_alarm_classifier_table.csv.gz) lists the signal with label "real", class "offset" (a classifier label, not a physical confirmation or host assignment) |
| allsky_round3_outcomes.csv | 333661705 | brahle | brahle; also a first-stage RAVEN candidate, P = 1.38324 d |

Round-4 objects (tables/round4/): 343298093 and 151767028 are independent rediscoveries (eumemic; 151767028 also RAVEN first stage).
