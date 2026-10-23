# Release v1.16 manifest (2026-10-23)

Files added or changed since v1.15, with SHA-256. Round 5 (closed, no freeze); TRICERATOPS
sector-provenance and pixel-screen correction with dated, append-only notes; corrected tools. All 68 prediction CSVs are unchanged; the
two other tracked registration-area CSVs are also unchanged. The round-5 review copies carry path-only redactions (labelled at their top).
Round 6: decision-history summary only.

| SHA-256 | file |
|---|---|
| `caf3e0faf624cc081dc2e6c5ace372f41474e3e2093e63a9a552626729d085b4` | CITATION.cff |
| `7f9429dbca7a6550e13bb6dca16b953f440f7606a74d6f986f794a55b73d2fc7` | DECISIONS.md |
| `c1a16575d25a7232e38d3ce531c8b982754312c4cb17e6128973127b8dfafd8d` | README.md |
| `e4d0c47e492b259204bccdc939411e88299656a87e6ca0484a8e120abfdd4b22` | REPORT.md |
| `562ae41d92cb63b84a1e1d4e74b6145d213ab9c09e211174fddf59d9ce8fdcef` | corrections/CORRECTION_TRICERATOPS_PIXEL_2026-10-22.md |
| `92ff02cf4c14d6429ad7936742b240aa785c74f3645158ab96d05f67697c97d5` | preregistration/TIC151767028/PREREGISTRATION_v2.md |
| `9027ab9a200a92192d55d3a338643f7cbf10e4670b894f5256acd43ffcdcb250` | preregistration/TIC160330868/PREREGISTRATION_v2.md |
| `268ee143495e43e48e17c04819e8adb6e65eac7cccd6b4819cdcf4c2bbcbab05` | preregistration/TIC160330868/TRICERATOPS_SECTOR_NOTE_2026-10-22.md |
| `812863f57e57e4c2c5a327f8241116f5c50358253c99074709012648a981337e` | preregistration/TIC188664994/PREREGISTRATION_v2.md |
| `5e9bfc0cfb45fa5c64c1bbf7c754e6997ec158775a4178d9c5a274af596b65d9` | preregistration/TIC196514928/TRICERATOPS_SECTOR_NOTE_2026-10-22.md |
| `aad023e1a99598462120407a21641e3f24155687dc92dcb2c530078cbfd13e7c` | preregistration/TIC253931796/PREREGISTRATION_v2.md |
| `f901ebdb0b969c747f88597068fe5df790995446a6cab1991e2397170d67bf92` | preregistration/TIC343298093/PREREGISTRATION_v2.md |
| `26e59a990c2a2f5ab1c4040e45e79b83508c4ffb3da33b5d93bcd8e1bfe7e8f5` | preregistration/TIC61310956/TRICERATOPS_SECTOR_NOTE_2026-10-22.md |
| `87d5a7e84906bb2f5db34642021b67616db7ab5afb577a03353b23a76cb42332` | preregistration/TIC91617711/PREREGISTRATION_v2.md |
| `3d717c611c2ec64cc05fd56e2b8909997a50493569dccc884682fac39506ce11` | reviews_round5/PROMPT_recheck_round5.txt |
| `fface95b451276bf1f807ae86771564e3a78259f637223cc4597c1d96f223e3d` | reviews_round5/PROMPT_review_round5_results.txt |
| `e4a581e2f02683fa93b7da97b092113022ddb51fc2211d418f69c45ab73fa3b4` | reviews_round5/REVIEW_round5_recheck.md |
| `906e773583a47b30d56c0a17caca36030cbd9852ac856da806df32ff9654677d` | reviews_round5/REVIEW_round5_results.md |
| `75ea0bd520be31c50210375ce5aade33fe9aa56fc94028285e31109a3ec9cddd` | scripts/pixel_collect_v2.py |
| `29385f67fe1008f96ffb75dca60d594f5167abea3ea646074f1c8459bde73954` | scripts/prior_match.py |
| `2cd8f124485041399d49b93ea2e4eb1032938e17a83d376cd1f497abaf8a9f2c` | scripts/test_prior_match.py |
| `276b893069d1507df5697498e127e282067639d2bfe9ec3cbb8b9a1c1528a273` | scripts/test_triceratops_qlp_v2.py |
| `040747d42b86c1f9eaffdcf5b614523fc5bbdf2e7577deecd3aa146cb3427263` | scripts/tri_runner_round5.sh |
| `18300d7b4ba9ce5e33cdcb2b3b5c3f5b0d4427b46b8fba3be2dbf5658fd4d2e4` | scripts/triage_round5.py |
| `42ef529b6631f317b0bf75c0252d8ac17c81197bd1318e8cb531d9d7c4731ab7` | scripts/triceratops_qlp_v2.py |
| `6214f0ff53b39173589f015682d7dbed9dc6e73982137739969e7267361a9f26` | tables/pixel_v2/allsky_classA_round2_pixel_v2.csv |
| `6c295b76638035abc39db86b85ac1aca6854d712959dedc3f9893dae6f3a4d96` | tables/pixel_v2/allsky_round3_pixel_v2.csv |
| `87195f7e54b7b66d1dcec1d2c56691356c04c53d081dbf12e49cf46060d29589` | tables/pixel_v2/allsky_round4_pixel_v2.csv |
| `b8a140f77a54ac176e1889367ef21fd1dbf87e7ba521a2b334776ac106527e39` | tables/pixel_v2/allsky_round5_pixel_v2.csv |
| `3d04ea4a9f4026d51707063d41f6cacb93dbd03cd18142b14b3d525f8682c2f7` | tables/round5/README.md |
| `f45ef151b2e531db7099753f8f23f22d206b68564bc80cf66711ca12ed5528d0` | tables/round5/allsky_round4_secondary.csv |
| `528d35c805386e230524377ddbd844352791e40bba9b4f28a8c5fe567c045e0e` | tables/round5/allsky_round5_pixel.csv |
| `04b0aea95d9e9f64e4ffb9eaa21969b45e3dbc1c79e51081ebc1b10897342398` | tables/round5/allsky_round5_triage.csv |
| `638e28e30d449cd08bdf2294789f1ef628cabe0b7a7d571bac86c5c6674b4db4` | tables/round5/allsky_round5_vetlist.csv |
| `9c46082730881ffc86a2de4bb9064733d4fe7a021d0380d7ad36c87beda18fd0` | tables/round5/prior_match_round5.csv |
| `f7726f88c9f6fb4e843d1a6466519eb9c280ea287c66eda4b636a691aa255906` | tables/round5/prior_match_round5_text.csv |
| `99f1be38a0f2a6af5dbc4990a07d4041777a819c8b4cad4ec8c27bbc607522db` | tables/round5/prior_match_round5_unresolved.csv |
| `487383ac5ce7244a3f2aceac605d0f4efe3e1bb84c1db19acbe07c9708e4d633` | tables/round5/tests/test_prior_match_20261022.log |
| `c2b4417ddd74646d07e0cae88b6521b1d1ec111ae81a85d1937037a620b71cf2` | tables/round5/tests/test_triceratops_qlp_v2_20261022b.log |
| `5fbf0027d299f9fcd33e57ea75f00005cfa9103f10aefeee329f5bb83fd5d4db` | tables/round5/triceratops_qlp_sector_audit_20261022.json |
