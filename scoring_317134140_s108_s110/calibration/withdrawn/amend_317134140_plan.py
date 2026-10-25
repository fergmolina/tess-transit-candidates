"""SUPERSEDED (2026-10-25, DECISIONS 187): the combined-LR interpretation it wrote was withdrawn after review. Do not run.

Append the dated interpretation plan (DECISIONS 185-186) to the TIC 317134140 registration. It refuses unless the local registration
is byte-identical to the copy published in v1.18 (git tag v1.18 in public_release/), so the published text stays a frozen prefix. Runs
once: it refuses if the plan paragraph is already present.
Usage: python -I amend_317134140_plan.py TABLE.json"""
import sys, json, hashlib, subprocess
raise SystemExit("superseded (DECISIONS 187)")
R = "/Users/fernando/Desktop/NASA"; REG = f"{R}/results/vet/317134140/PREREGISTRATION.md"
sha = lambda b: hashlib.sha256(b).hexdigest()
pub = subprocess.run(["git", "-C", f"{R}/public_release", "show", "v1.18:preregistration/TIC317134140/PREREGISTRATION.md"], capture_output=True, check=True).stdout
cur = open(REG, "rb").read()
if b"Dated interpretation plan" in cur: raise SystemExit("refused: the plan is already appended")
if cur != pub: raise SystemExit("refused: the local registration differs from the v1.18 published copy")
T = json.load(open(sys.argv[1])); tab = open(sys.argv[1], "rb").read()
L = T["lr"]; h1, h0 = T["h1_185"], T["h0"]; g = lambda x: f"{x:.3g}"
strong = [c for c in T["combinations"] if "strong evidence that" in c["conclusion"]]; against = [c for c in T["combinations"] if "strong evidence against" in c["conclusion"]]
txt = (f"\n**Dated interpretation plan 2026-10-25 (before any S108-S110 photometry of this star is examined).** The frozen per-sector outcomes "
       f"remain the outcomes of record. Their combined interpretation follows a rule fixed in DECISIONS 185 BEFORE any calibration trial was run. "
       f"H1: a periodic ~185 ppm, 1.5-h dip at the frozen ephemeris is present in a test sector. H0: no such dip, only this star's noise. H1 is "
       f"satisfied equally by a planet and by a blended eclipsing binary, so the plan concerns persistence of the signal, not its origin, and no "
       f"outcome yields \"validated\". Calibration: scripts/calibrate_317134140_scorer.py ran the LOCKED v1.3 scorer functions on the real "
       f"training sectors with the real signal divided out, using {h1['n']} injections of the registration's transit shape at 185 ppm (measured as "
       f"clause A measures it) at random periods 0.53-0.70 d and phases, and {h0['n']} noise-only trials. Both are pooled over the single-sector "
       f"training sectors S6, S87 and S107; S98, two sectors long, is reported but not used. Per-sector likelihood ratios, P(outcome|H1) / "
       f"P(outcome|H0), each estimated as (k + 1/2) / (N + 1): PASS {g(L['PASS'])}, PARTIAL {g(L['PARTIAL'])}, INCONCLUSIVE {g(L['INCONCLUSIVE'])}, "
       f"FAIL {g(L['FAIL'])}; INSUFFICIENT, UNAVAILABLE and INVALID_INPUT count 1. The combined LR is the product over S108, S109 and S110, which are "
       f"treated as independent. Conclusion: > 10 strong evidence that the signal persists; 3-10 moderate; 1/3-3 inconclusive; 1/10-1/3 moderate "
       f"evidence against; < 1/10 strong evidence against; boundaries go to the less extreme category. The full lookup of all "
       f"{len(T['combinations'])} order-free outcome combinations is results/conformance_317134140/interpretation_table_v1.3.md (table JSON "
       f"SHA-256 {sha(tab)[:16]}..., calibration SHA-256 {T['calibration_sha256'][:16]}...). The trials share one noise realization per "
       f"sector, so these ratios carry more uncertainty than their counts suggest. The PASS ratio rests on zero noise-only PASS counts and is a "
       f"bound set by the estimator. The ratios assume a 185 ppm signal; the training sectors measured 127-210 ppm. At 130 ppm a real signal "
       f"FAILs in about 14 % of sectors (LR(FAIL) {g(T['sensitivity']['130.0']['lr']['FAIL'])}), and "
       f"{sum(c['conclusion'] != c['conclusion_if_130ppm_not_used'] for c in T['combinations'])} of the {len(T['combinations'])} combinations, all with a FAIL "
       f"or several INCONCLUSIVE outcomes, would change category. These depth-sensitivity columns are reported in the table, are NOT used, and were "
       f"added after the calibration was seen. The pooled depth remains a secondary readout and plays no part. "
       f"Nothing in the v1.18 lock is changed. DECISIONS 185-186.\n")
open(REG, "wb").write(cur.rstrip(b"\n") + b"\n" + txt.encode()); print("appended;", len(strong), "combinations give strong support,", len(against), "strong evidence against")
