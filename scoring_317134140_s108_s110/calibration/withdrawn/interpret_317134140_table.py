"""WITHDRAWN 2026-10-25 (DECISIONS 187): the combined-LR interpretation this builds is not supported (structural-zero null). Kept for
history; its outputs interpretation_table_v1.3.* are withdrawn. The release uses scripts/calibration_diagnostics_317134140.py.
Build the TIC 317134140 S108-S110 interpretation table from the calibration, applying EXACTLY the rule logged in DECISIONS 185 before
any calibration trial was run (2026-10-25; DECISIONS 186):
- per-sector LR(L) = P(L|H1) / P(L|H0), each estimated as (k + 1/2) / (N + 1);
- the table pools the single-sector training sectors S6, S87, S107 at 185 ppm (H1) and their H0 trials; S98 is reported separately and
  not used;
- INSUFFICIENT, UNAVAILABLE and INVALID_INPUT contribute LR 1;
- combined LR = product over S108, S109, S110 (treated as independent);
- verbal scale: > 10 strong evidence that the signal persists; 3-10 moderate; 1/3-3 inconclusive; 1/10-1/3 moderate evidence against;
  < 1/10 strong evidence against; a boundary value belongs to the less extreme category.
Also reported, never used: per-sector tables, S98, and the 130 / 240 ppm sensitivity tables.
Usage: python -I interpret_317134140_table.py CALIBRATION.json OUT.json OUT.md"""
import sys, json, hashlib, itertools, collections
cal_p, out_j, out_m = sys.argv[1:4]; cal = json.load(open(cal_p)); sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
LABELS = ("PASS", "PARTIAL", "INCONCLUSIVE", "FAIL"); NODATA = "INSUFFICIENT / UNAVAILABLE / INVALID_INPUT"
TABLE_SECTORS = (6, 87, 107)
def freq(rows):
    c = collections.Counter(r["outcome"] for r in rows); n = len(rows)
    return dict(n=n, counts={L: c.get(L, 0) for L in LABELS + ("INSUFFICIENT",)})
def lr(h1, h0):
    return {L: ((h1["counts"][L] + 0.5) / (h1["n"] + 1)) / ((h0["counts"][L] + 0.5) / (h0["n"] + 1)) for L in LABELS}
def verbal(x):
    if x > 10: return "strong evidence that the signal persists"
    if x > 3: return "moderate evidence that the signal persists"
    if x >= 1 / 3: return "inconclusive"
    if x >= 1 / 10: return "moderate evidence against persistence"
    return "strong evidence against persistence"
h1 = lambda secs, d: [r for r in cal["h1"] if r["sector"] in secs and r["depth_ppm"] == d]
h0 = lambda secs: [r for r in cal["h0"] if r["sector"] in secs]
main_h1, main_h0 = freq(h1(TABLE_SECTORS, 185.0)), freq(h0(TABLE_SECTORS)); LR = lr(main_h1, main_h0)
per_sector = {s: dict(h1_185=freq(h1((s,), 185.0)), h0=freq(h0((s,))), lr=lr(freq(h1((s,), 185.0)), freq(h0((s,))))) for s in (6, 87, 98, 107)}
sens = {d: dict(h1=freq(h1(TABLE_SECTORS, d)), lr=lr(freq(h1(TABLE_SECTORS, d)), main_h0)) for d in (130.0, 240.0)}
states = LABELS + (NODATA,); lrs = dict(LR, **{NODATA: 1.0})
combos = []
for c in itertools.combinations_with_replacement(states, 3):
    x = 1.0
    for s in c: x *= lrs[s]
    alt = {}
    for d in (130.0, 240.0):
        y = 1.0
        for st in c: y *= dict(sens[d]["lr"], **{NODATA: 1.0})[st]
        alt[f"combined_lr_if_h1_{int(d)}ppm"] = y
    combos.append(dict(outcomes=list(c), combined_lr=x, conclusion=verbal(x), sensitivity_not_used=alt, conclusion_if_130ppm_not_used=verbal(alt["combined_lr_if_h1_130ppm"])))
combos.sort(key=lambda r: -r["combined_lr"])
res = dict(rule="DECISIONS 185", calibration_file=cal_p.split("/")[-1], calibration_sha256=sha(cal_p), scorer_sha256=cal["scorer_sha256"],
           table_sectors=list(TABLE_SECTORS), h1_185=main_h1, h0=main_h0, lr=LR, per_sector=per_sector, sensitivity=sens,
           cleaning={s: v["cleaned_true_ephemeris"] for s, v in cal["sectors"].items()}, combinations=combos,
           caveat="trials share one noise realization per sector; binomial uncertainties understate the true uncertainty")
json.dump(res, open(out_j, "w"), indent=1)
f = lambda x: f"{x:.3g}"
md = [f"# TIC 317134140 S108-S110: declared interpretation table (rule DECISIONS 185; calibration `{res['calibration_file']}`, SHA-256 `{res['calibration_sha256'][:16]}...`)", "",
      f"Pooled single-sector training sectors S6, S87, S107. H1 is a 185 ppm injection ({main_h1['n']} trials); H0 is noise only ({main_h0['n']} trials). Each probability is (k + 1/2) / (N + 1).", "",
      "| Sector outcome | H1 count | H0 count | P(outcome given H1) | P(outcome given H0) | LR |", "|---|---:|---:|---:|---:|---:|"]
for L in LABELS:
    md.append(f"| {L} | {main_h1['counts'][L]} | {main_h0['counts'][L]} | {f((main_h1['counts'][L] + .5) / (main_h1['n'] + 1))} | {f((main_h0['counts'][L] + .5) / (main_h0['n'] + 1))} | {f(LR[L])} |")
md += [f"| INSUFFICIENT (calibration count only; LR fixed at 1) | {main_h1['counts']['INSUFFICIENT']} | {main_h0['counts']['INSUFFICIENT']} | | | 1 |", "",
       "## All outcome combinations for S108, S109 and S110 (order-free)", "",
       "The last three columns are a depth-sensitivity disclosure (added 2026-10-25 after the calibration was seen; DECISIONS 186). They are reported, NOT used; the declared conclusion is the one in the third column.", "",
       "| Outcomes | Combined LR (H1 = 185 ppm) | Declared conclusion | LR if H1 = 130 ppm | LR if H1 = 240 ppm | Conclusion if 130 ppm (not used) |", "|---|---:|---|---:|---:|---|"]
md += [f"| {' + '.join(c['outcomes'])} | {f(c['combined_lr'])} | {c['conclusion']} | {f(c['sensitivity_not_used']['combined_lr_if_h1_130ppm'])} | {f(c['sensitivity_not_used']['combined_lr_if_h1_240ppm'])} | {c['conclusion_if_130ppm_not_used']} |" for c in combos]
md += ["", "## Reported, not used", "", "| Set | H1 trials | PASS | PARTIAL | INCONCLUSIVE | FAIL | INSUFFICIENT | H0 trials | H0 FAIL | H0 PASS |", "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
for s, v in per_sector.items():
    a, b = v["h1_185"], v["h0"]
    md.append(f"| S{s} at 185 ppm | {a['n']} | " + " | ".join(str(a['counts'][L]) for L in LABELS + ('INSUFFICIENT',)) + f" | {b['n']} | {b['counts']['FAIL']} | {b['counts']['PASS']} |")
for d, v in sens.items():
    a = v["h1"]; md.append(f"| S6+S87+S107 at {int(d)} ppm | {a['n']} | " + " | ".join(str(a['counts'][L]) for L in LABELS + ('INSUFFICIENT',)) + " | | | |")
md += ["", "Residual clause-A depth at the true ephemeris after dividing out the real signal: " + "; ".join(f"S{s} {v['depth_ppm']:.0f} +- {v['sigma_ppm']:.0f} ppm" for s, v in res["cleaning"].items()) + ".",
       "", "Caveats: the trials share one noise realization per sector, so binomial uncertainties understate the true uncertainty. Ratios for outcomes with zero noise-only counts (PASS) are set by the (k + 1/2) / (N + 1) estimator, so they are bounds of order N, not measured values. The ratios assume a 185 ppm signal: the training sectors measured 127-210 ppm, and at 130 ppm a real signal FAILs in about 14 % of sectors, so combinations containing a FAIL are strongly depth-dependent (see the sensitivity columns). H1 is equally satisfied by a planet and by a blended eclipsing binary; no conclusion here means \"validated\"."]
open(out_m, "w").write("\n".join(md) + "\n"); print("\n".join(md[:12]))
