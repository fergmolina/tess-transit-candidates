"""Append the dated, DESCRIPTIVE calibration note (DECISIONS 187) to the TIC 317134140 registration. It refuses unless the local
registration is byte-identical to the copy published in v1.18 (git tag v1.18), and runs once.
Usage: python -I amend_317134140_diagnostics.py DIAGNOSTICS.json"""
import sys, json, hashlib, subprocess
R = "/Users/fernando/Desktop/NASA"; REG = f"{R}/results/vet/317134140/PREREGISTRATION.md"
pub = subprocess.run(["git", "-C", f"{R}/public_release", "show", "v1.18:preregistration/TIC317134140/PREREGISTRATION.md"], capture_output=True, check=True).stdout
cur = open(REG, "rb").read()
if b"Dated calibration note" in cur: raise SystemExit("refused: already appended")
if cur != pub: raise SystemExit("refused: the local registration differs from the v1.18 published copy")
raw = open(sys.argv[1], "rb").read(); D = json.loads(raw); p = D["h1"]
f = lambda t, k: f"{100 * t['outcome'][k] / t['n']:.0f} %"
row = lambda d: (f"{d[:-3]} ppm: PASS {f(p[d]['pooled_S6_S87_S107'], 'PASS')}, PARTIAL {f(p[d]['pooled_S6_S87_S107'], 'PARTIAL')}, "
                 f"INCONCLUSIVE {f(p[d]['pooled_S6_S87_S107'], 'INCONCLUSIVE')}, FAIL {f(p[d]['pooled_S6_S87_S107'], 'FAIL')}")
h0 = D["h0"]["pooled_S6_S87_S107"]; t = D["injected_t14_h"]
txt = (f"\n**Dated calibration note 2026-10-25 (before any S108-S110 photometry of this star is examined).** The locked v1.3 scorer was run "
       f"on the training sectors, with the real signal divided out, on injected registration-shape signals at random periods of 0.53-0.70 d "
       f"(injected geometric T14 {min(v[0] for v in t.values()):.2f}-{max(v[1] for v in t.values()):.2f} h; clause A's scoring window is 1.5 h) "
       f"and on noise-only trials (scripts/calibrate_317134140_scorer.py; diagnostics in "
       f"results/conformance_317134140/calibration_diagnostics_v1.3.md, JSON SHA-256 {hashlib.sha256(raw).hexdigest()[:16]}...). Pooled over the "
       f"single-sector training sectors S6, S87 and S107, the injected-signal outcome frequencies were: {row('130ppm')}; {row('185ppm')}; "
       f"{row('240ppm')}. Noise only: FAIL {100 * h0['outcome']['FAIL'] / h0['n']:.0f} %, INCONCLUSIVE {100 * h0['outcome']['INCONCLUSIVE'] / h0['n']:.0f} %, "
       f"PARTIAL {100 * h0['outcome']['PARTIAL'] / h0['n']:.0f} %. These experiments describe conditional recovery and outcome frequencies in three "
       f"selected training noise realizations. Their noise-only BLS peaks cannot satisfy PASS anywhere in the allowed trial-period range, so the "
       f"zero PASS count does not calibrate a future-sector false-PASS probability. The trial periods also avoid the band around TOI-2514.01's "
       f"eleventh harmonic that contains the candidate period. The frozen per-sector outcomes remain the outcomes of record. Each test-sector "
       f"outcome will be reported with its conditional frequencies at all three injection depths. No quantitative combined evidential-strength "
       f"conclusion is adopted from this calibration. A persistent dip would not distinguish a planetary transit from a blended eclipsing "
       f"binary. A combined likelihood-ratio interpretation drafted on 2026-10-25 was withdrawn before publication after external review "
       f"(DECISIONS 185-187). Nothing in the v1.18 lock is changed.\n")
open(REG, "wb").write(cur.rstrip(b"\n") + b"\n" + txt.encode()); print("appended")
