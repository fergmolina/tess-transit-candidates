> **2026-10-21. Published with release v1.15 after three independent re-checks (reviews_round4/). No frozen file is changed.**

# Erratum: earlier machine detections missed by our prior-report searches

The round-4 review (reviews_round4/REVIEW_round4_freezes.md, F1/F5) showed that our searches did not read compressed tables and matched
numbers by proximity. A row/field-aware matcher (scripts/prior_match.py; first run results/prior_match_20261021.csv; corrected run results/prior_match_20261021b.csv with _text.csv,
_unresolved.csv and logs/prior_match_20261021b.log — the corrected period-column rule adds four primary RAVEN records but no additional matched
object; regression tests scripts/test_prior_match.py) was run on all 67 registered
and round-4 objects over the saved corpora, and the RAVEN tables were downloaded from their primary source (Zenodo record 19661443;
results/prior_search_round4/data/20261021_raven/; nsfp09_table.csv SHA-256 7b4fb0b0...). A match requires the TIC and a period column in
the same record, with P, P/2 or 2P within 0.1 %.

RAVEN = Lafarga, Armstrong, Cui, Hadjigeorghiou, Kunovac, Doyle et al. 2026, MNRAS, doi:10.1093/mnras/stag512, arXiv:2603.22597 (dated
2026-03-23); online material Zenodo 19661443 (displayed publication date 2026-03-25, archive creation date 2026-04-20; we have not
established when the table bytes first became downloadable). Either way it precedes our October 2026 work. Cited as "Lafarga et al. (2026)". Its nsfp09 table lists 14,815 automated first-stage candidates (NSFP probability > 0.9); the vetted
(2,170) and validated (143) tables are separate.

| Object | Our public statement | Earlier detection found | Correction |
|---|---|---|---|
| TIC 80387959 | README/REPORT: "no human-reported candidate found in the searched sources" (+ SPOC S63 alert); prior_search/VERDICTS.md: "no human-reported candidate anywhere", "appears in no catalog, paper, repository or deposit"; preprint v1.3: "no catalogued periodic signal exists on any star within 60''" | RAVEN nsfp09 (primary table line 2706): P = 4.19221738810686 d, NSFP score 0.980; line 2707: 1.3973872442 d (about P/3), score 0.933. Not in RAVEN's vetted, validated or large-radius tables. | Withdraw the priority claims. Replacement text: "TIC 80387959 was previously reported at P = 4.1922173881 d in the first-stage RAVEN candidate catalog of Lafarga et al. (2026). It is absent from their vetted and validated subsets. Our work independently recovers this signal, provides additional vetting and freezes predictions for a later observational test; we do not claim first detection." Keep the TESS-SPOC FFI Sector-63 alert as an additional earlier source; any absence statement about threshold-crossing events refers to SPOC 2-minute TCEs only. Neither RAVEN's score nor its absence from later subsets establishes a planet. |
| TIC 249813122 | README table: prior report "none" | RAVEN nsfp09: P = 4.17453 d (ours 4.17615 d, 0.04 %), prob_NSFP 0.999 | "prior machine detection (RAVEN first stage)" |
| TIC 333661705 | credited rediscovery (brahle) | also RAVEN nsfp09, P = 1.38324 d | add RAVEN |
| TIC 151767028 | rediscovery (eumemic/ahrazzle) | also RAVEN nsfp09, P = 2.21040 d | added in the round-4 amendment |
| TIC 343298093 | "no prior report found" (local only) | eumemic vetted_signals.csv.gz (flagged) | corrected in the round-4 amendment |
| TIC 122522485, 159033763, 162304222 | round-3 table: "none found" | eumemic results_public/all_signals.csv.gz (their public raw BLS output) at the same period | "no candidate report found; a period within our matching tolerance (0.1 %) appears in eumemic's public raw BLS table (a raw search output, not a promoted or validated candidate)" |
| TIC 196514928, 283913390 | round-3 table: "none found" | eumemic validation/false_alarm_classifier_table.csv.gz: label "real", class "offset" | "eumemic's classifier table lists this signal as real but off-target (class 'offset')" (a classifier label, not an independent physical confirmation or host assignment) |

No earlier detection was found for TIC 183374279, 61310956, 89247735, 188664994, 195343302, 70441745, 206620592, 253931796, 160330868,
24526743, 203381983, 36694943, 376225363, 467959906, 50514263, 245503256, 332709057, 371421714 or 91617711 in the searched corpora. This is a
bounded search, not proof of novelty. Separately, candidate folder names of the form TIC<id>_P<period> (eumemic/ahrazzle) match only objects
already credited as rediscoveries.

## Public locations to correct (dated notices; archived bytes are never rewritten)
Found by a text search of every local release and dataset copy (2026-10-21) for the 80387959 claims, plus the tables named below.

**Repository (next release, v1.15; line numbers refer to the v1.14 files, before the notices were added)**
| Location | Change |
|---|---|
| README.md:87 and REPORT.md:557 (TIC 80387959 novelty paragraph) | RAVEN replacement text above |
| prior_search/VERDICTS.md:9 and prior_search/PRIOR_SEARCH.md:41 (TIC 80387959 verdict: "no human-reported candidate anywhere", "appears in no catalog, paper, repository or deposit") | conspicuous dated correction in each file's header, linked from the release notes |
| README.md table and tables/allsky_classA_round2_outcomes.csv (TIC 249813122, prior "none") | "prior machine detection (RAVEN first stage)"; dated notice next to the CSV (CSV bytes kept) |
| tables/allsky_round3_outcomes.csv (122522485, 159033763, 162304222, 196514928, 283913390; RAVEN added for 333661705) | dated notice with the qualified wording above (CSV bytes kept) |
| DDT proposal for TIC 80387959 (submitted 2026-10-19; not in this repository) | corrections/DDT_PROPOSAL_80387959_CORRECTION_2026-10-21.md: the October-18 identification is an independent recovery of the earlier RAVEN candidate; "no SPOC threshold-crossing event" refers to SPOC 2-minute TCEs; the TESS-SPOC FFI S63 alert is acknowledged. Sending a note to the DDT office: author's decision (current choice: only if the office replies). |

**Preprint (Zenodo concept 10.5281/zenodo.23462433)**
| Location | Change |
|---|---|
| note_allsky/note.tex:18-22 (v1.3) | new version v1.4: remove "no catalogued periodic signal"; separate the no-TOI/CTOI statement from prior signal reports; RAVEN text above; SPOC 2-min TCEs vs the TESS-SPOC FFI alert stated separately |

**Dataset (Zenodo: v1.0 10.5281/zenodo.23462438; v1.1 10.5281/zenodo.23512928) — both versions carry the claim**
| Location | Change |
|---|---|
| dataset_v1/README.md:37, README_v1.md:26 (historical, kept as superseded), REPORT.md:530, prior_search/VERDICTS.md:9, prior_search/PRIOR_SEARCH.md:32, documents/note.tex:21 | covered by a dated correction notice in a new dataset version and in its Zenodo description; the v1.0 files are not rewritten |
| dataset_v1.1/README.md:38, REPORT.md:530, prior_search/VERDICTS.md:9, prior_search/PRIOR_SEARCH.md:39, documents/note.tex:21 | same: a new dataset version (v1.2) with the correction notice and corrected copies; v1.1 kept on record |

**Local working copies (so a later export cannot restore the claim)**
| Location | Change |
|---|---|
| results/REPORT.md:557, results/prior_search/VERDICTS.md:9, results/prior_search/PRIOR_SEARCH.md:32, results/allsky_classA_round2_outcomes.csv, results/allsky_round3_outcomes.csv, STATUS.md | annotated with the same dated correction before the next export (STATUS done) |

## Paths in this repository
results/prior_match_20261021*.csv and prior_match_targets_20261021.csv -> tables/round4/; scripts/ -> scripts/. The RAVEN tables are not
redistributed: cite Lafarga et al. (2026) and Zenodo record 19661443 (nsfp09_table.csv SHA-256
7b4fb0b02a8597cad8ecc4ca1687be1e75ab5b04fb74e7232ad834944641df3a). The local working copies listed above are the authors' files.
