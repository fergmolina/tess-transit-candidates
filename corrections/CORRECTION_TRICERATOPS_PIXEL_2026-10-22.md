# Correction — TRICERATOPS sector provenance and pixel-screen accounting (2026-10-22; published in v1.16, 2026-10-23)

Source: the round-5 review (reviews_round5/REVIEW_round5_results.md, R5-2 and R5-5) and its re-check
(reviews_round5/REVIEW_round5_recheck.md), widened by our own audit to all earlier rounds (DECISIONS 137-140). Paths beginning
`results/` are the authors' workspace (see REPORT correction 8); public copies: tables/round5/, tables/pixel_v2/, scripts/.

## 1. TRICERATOPS runs made with scripts/triceratops_qlp.py

The script folded every cached QLP light curve of the star that had at least 1000 good points, but recorded only the three sectors
whose TESScut apertures it used. The FPP/NFPP values below are the original saved single-run outputs; no probability
calculation was repeated for this audit. The light-curve fold used the sectors in the "photometry" column, not those in the "recorded"
column. The photometry-sector inventory was reconstructed from the surviving files, their timestamps and the original selection code
(independently reproduced by the reviewer); it covers every surviving result of that runner and cannot exclude deleted runs. No run used a sector 106 or later. The values are single screening runs without
contrast curves. None meets the validation thresholds (FPP < 0.015 and NFPP < 0.001). New runs use scripts/triceratops_qlp_v2.py, which
takes explicit sectors and refuses test sectors before any file access. It records its QLP photometry inputs and their hashes, the
ephemeris source and the aperture cutouts; it uses the vet.py gap-edge mask but a separate photometry preparation, and is not yet
validated for new screening runs. No replacement values are quoted.

| TIC | Recorded (aperture) sectors | Photometry sectors in the fold | FPP / NFPP | Provenance differs |
|---|---|---|---|---|
| 122522485 | 30, 97, 105 | 30, 97, 105 | 0.075 / 0.0082 | no |
| 13450993 | 58, 85, 86 | 58, 85, 86 | 0.611 / 0.4780 | no |
| 151767028 | 90, 99, 100 | 36, 63, 90, 99, 100 | 0.113 / 0.0431 | yes |
| 160330868 | 33, 87, 98 | 32, 33, 87, 98 | 0.377 / 0.0716 | yes |
| 183374279 | 96, 103, 105 | 2, 29, 69, 96, 103, 105 | 0.031 / 0.0000 | yes |
| 188664994 | 80, 81, 84 | 20, 24, 40, 47, 50, 51, 52, 53, 54, 57, 60, 73, 80, 81, 84 | 0.081 / 0.0078 | yes |
| 195343302 | 55, 56, 83 | 55, 56, 83 | 0.156 / 0.1115 | no |
| 196514928 | 35, 62, 88 | 34, 35, 62, 88 | 0.043 / 0.0068 | yes |
| 206620592 | 28, 68, 96 | 28, 68, 96 | 0.032 / 0.0000 | no |
| 240488148 | 56, 82, 83 | 56, 82, 83 | 0.101 / 0.0368 | no |
| 253931796 | 28, 68, 96 | 28, 68, 96 | 0.084 / 0.0492 | no |
| 283913390 | 7, 33, 87 | 7, 33, 87 | 0.045 / 0.0252 | no |
| 343298093 | 101, 102, 103 | 13, 39, 66, 93, 100, 101, 102, 103 | 0.065 / 0.0010 | yes |
| 372343190 | 84, 85, 86 | 52, 57, 58, 84, 85, 86 | 0.678 / 0.6562 | yes |
| 61310956 | 72, 45, 22 | 45, 46, 72 | 0.020 / 0.0000 | yes |

(Photometry sectors: files present before the run that passed the script's 1000-point cut;
results/triceratops_qlp_sector_audit_20261022.json.)
TIC 13450993: the fold does not represent the vetted 2.5-2.8 ppt events (edge points that vetting removed, S18 dropped). The inference
that a nearby or binary origin is more likely is withdrawn.

## 2. Pixel screen (scripts/pixel_collect.py)

"On target" in earlier text means only that every finite loss-centroid offset, rounded to 0.01 px, was <= 0.50 px (the old
screen applied the 0.50-px threshold to offsets rounded to 0.01 px). It is a screen, not an exclusion of
neighbouring stars. The v1 collector ignored sectors whose offset was NaN or whose download failed, and it applied the thresholds to
offsets rounded to 0.01 px. scripts/pixel_collect_v2.py reads full-precision offsets, counts failed and non-finite sectors, and does not
allow ON_TARGET when any attempted sector failed or gave no finite offset (AMBIGUOUS_INCOMPLETE). Changes from v1 to v2:

| Round | Objects changed | TICs |
|---|---|---|
| classA_round2 | 4 | 185296189, 124609967, 164661702, 91617711 |
| round3 | 19 | 197684341, 160147750, 144335936, 101936650, 253931796, 393940391, 321980862, 91508602, 270410802, 183562325, 322048389, 89042807, 160330868, 91642908, 33579422, 101499286, 32006449, 163254516, 152232065 |
| round4 | 7 | 347357598, 143404791, 382390957, 276903941, 421977047, 188664994, 194050677 |
| round5 | 10 | 136763133, 372343190, 323407257, 389029596, 272231474, 245715694, 280808697, 278277011, 262785470, 111750335 |

Frozen objects affected: 91617711 (S71 non-finite), 253931796 (S68), 160330868 (S98), 188664994 (S80). Their on-target label rests on
one or two finite sectors. Their frozen predictions and test procedures are unchanged.

## 3. TIC 240488148 (round 5)

A recovery of a previously reported candidate: eumemic/ahrazzle catalogue (P = 1.512519 d), Advait Paliwal's dedicated report
(github.com/advaitpaliwal/TIC240488148, P = 1.5125149 d; public report 2026-10-09, reported discovery date 2026-10-08) and the moosesteve21 PlanetCandidates report (P = 1.5125120 d,
reported discovery date 2026-10-12; https://github.com/moosesteve21/PlanetCandidates/tree/main/TIC240488148). Our refined period is 1.5125181513 d. We claim no first discovery or statistical validation, and did not register it.

## 4. Placement (append-only; frozen bodies and CSV bytes unchanged)

Dated notes linking this correction, at:
- README.md: TIC 183374279 and TIC 61310956 paragraphs, the round-4 probabilities, and the aggregate "all 26 ... on
  target" statement (also REPORT.md);
- preregistration/TIC{151767028,343298093,188664994}/PREREGISTRATION_v2.md (TRICERATOPS sectors; 188664994 also the
  pixel screen) and TIC{253931796,160330868,91617711}/PREREGISTRATION_v2.md (pixel screen);
- beside the public triceratops.json files of TIC 160330868, 196514928 and 61310956;
- the round-2 dossiers are not part of this repository; their README summary (the "All 26" sentence) carries the note.

Pixel note text for each affected frozen object: "The original ON_TARGET label used only finite rounded offsets. The corrected screen is
AMBIGUOUS_INCOMPLETE because sector S<n> supplied no finite offset. The remaining finite offsets are <values>. This is not a calibrated
host assignment or neighbour exclusion. Frozen predictions and scoring rules are unchanged."
