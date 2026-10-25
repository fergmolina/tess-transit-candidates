"""Descriptive diagnostics from the TIC 317134140 calibration run (results/conformance_317134140/calibration_v1.3.json; 2026-10-25;
DECISIONS 187). This REPLACES the withdrawn combined-LR interpretation (scripts/interpret_317134140_table.py). It reports:
- conditional outcome and clause frequencies of the locked v1.3 scorer for 185 / 130 / 240 ppm injections and for noise-only trials,
  per training sector and pooled over the single-sector training sectors S6, S87 and S107 (S98 separately);
- a STRUCTURAL-ZERO check (exact interval test in the scorer's ratio direction, abs(p / P - 1) <= 0.001; review note 2026-10-25):
  for each sector, whether ANY allowed noise-only trial period could have hit the fixed noise-only BLS top 3
  (if not, B_TOP3 and PASS are impossible under H0 by construction, and their H0 frequency is NOT estimated);
- the injected geometric T14 range (circular orbit, b = 0.4024) and the residual depth left after removing the real signal.
No likelihood ratio, product or verbal evidential category is computed. These are frequencies in three selected training noise
realizations, conditional on the injection model; they are not calibrated future-sector probabilities.
Usage: python -I calibration_diagnostics_317134140.py CALIBRATION.json OUT.json OUT.md"""
import sys, json, hashlib, collections, numpy as np
cal_p, out_j, out_m = sys.argv[1:4]; cal = json.load(open(cal_p)); sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
OUT = ("PASS", "PARTIAL", "INCONCLUSIVE", "FAIL", "INSUFFICIENT"); A = ("A_CONSISTENT", "A_HIGH", "A_INCONCLUSIVE", "A_LOW", "INSUFFICIENT")
P0, P_TOI, B = 0.5718634, 6.3951381, 0.4024; POOL = (6, 87, 107)
def allowed(P):
    if abs(P / P0 - 1) < 0.02 or abs(P / (P0 / 2) - 1) < 0.02 or abs(P / (2 * P0) - 1) < 0.02: return False
    return not any(abs(P / (P_TOI / n) - 1) < 0.02 for n in range(1, 30))
def tab(rows):
    o = collections.Counter(r["outcome"] for r in rows); a = collections.Counter(r["clause_a"] for r in rows); b = collections.Counter(r["clause_b"] for r in rows)
    return dict(n=len(rows), outcome={k: o.get(k, 0) for k in OUT}, clause_a={k: a.get(k, 0) for k in A}, b_top3=b.get("B_TOP3", 0))
h1 = lambda secs, d: [r for r in cal["h1"] if r["sector"] in secs and r["depth_ppm"] == d]
h0 = lambda secs: [r for r in cal["h0"] if r["sector"] in secs]
def allowed_intervals():
    """[0.53, 0.70] minus the open 2 % exclusion bands, as closed intervals (exact; no grid)."""
    refs = [P0, P0 / 2, 2 * P0] + [P_TOI / n for n in range(1, 30)]; segs = [(0.53, 0.70)]
    for r in refs:
        lo, hi = 0.98 * r, 1.02 * r; nxt = []
        for a, b in segs:
            if hi <= a or lo >= b: nxt.append((a, b)); continue
            if a < lo: nxt.append((a, lo))
            if hi < b: nxt.append((hi, b))
        segs = nxt
    return segs
SEGS = allowed_intervals()
def reachable(p):
    """The scorer's hit test is abs(p / P - 1) <= 0.001, i.e. P in [p / 1.001, p / 0.999]; is any allowed P in that interval?"""
    lo, hi = p / 1.001, p / 0.999
    return any(max(lo, a) < min(hi, b) or (lo <= a <= hi) or (lo <= b <= hi) for a, b in SEGS)
struct = {}
for s, v in cal["sectors"].items():
    peaks = [p["period"] for p in v["cleaned_top3"]]
    hit = [p for p in peaks if reachable(p)]
    struct[s] = dict(noise_only_top3_periods_d=peaks, peaks_reachable_by_allowed_trial_periods=hit, pass_possible_under_h0=bool(hit))
def t14(P, rp, ar): return P / np.pi * np.arcsin(np.sqrt(((1 + rp) ** 2 - B ** 2) / (ar ** 2 - B ** 2))) * 24
dur = {d: [min(t14(r["P"], r["rp"], r["ar"]) for r in cal["h1"] if r["depth_ppm"] == d), max(t14(r["P"], r["rp"], r["ar"]) for r in cal["h1"] if r["depth_ppm"] == d)] for d in (130.0, 185.0, 240.0)}
res = dict(source=cal_p.split("/")[-1], source_sha256=sha(cal_p), scorer_sha256=cal["scorer_sha256"], decisions="187",
           h1={f"{int(d)}ppm": dict(pooled_S6_S87_S107=tab(h1(POOL, d)), **{f"S{s}": tab(h1((s,), d)) for s in (6, 87, 98, 107)}) for d in (185.0, 130.0, 240.0)},
           h0=dict(pooled_S6_S87_S107=tab(h0(POOL)), **{f"S{s}": tab(h0((s,))) for s in (6, 87, 98, 107)}),
           structural_zero=struct, injected_t14_h=dur, scoring_window_h=1.5,
           cleaning_residual={s: v["cleaned_true_ephemeris"] for s, v in cal["sectors"].items()})
json.dump(res, open(out_j, "w"), indent=1)
pct = lambda k, n: f"{k}/{n} ({100 * k / n:.0f} %)" if n else "-"
md = [f"# TIC 317134140 scorer v1.3: calibration diagnostics (descriptive; DECISIONS 187)", "",
      f"Source `{res['source']}` (SHA-256 `{res['source_sha256'][:16]}...`), produced by the locked scorer (`{res['scorer_sha256'][:16]}...`) on the TRAINING sectors only.",
      "",
      "**What these are.** Conditional outcome frequencies in three selected training noise realizations (S6, S87, S107; S98 separately),",
      "with the real signal divided out and a registration-shape signal injected at random periods of 0.53-0.70 d.",
      "They are not calibrated probabilities for S108-S110, and no likelihood ratio or combined evidential-strength conclusion is drawn from them.",
      "The frozen per-sector outcomes remain the outcomes of record.",
      "", "## Injected signal (H1), pooled S6 + S87 + S107", "", "| Depth | Trials | PASS | PARTIAL | INCONCLUSIVE | FAIL | INSUFFICIENT |", "|---|---:|---:|---:|---:|---:|---:|"]
for d in ("130ppm", "185ppm", "240ppm"):
    t = res["h1"][d]["pooled_S6_S87_S107"]; md.append(f"| {d[:-3]} ppm | {t['n']} | " + " | ".join(pct(t['outcome'][k], t['n']) for k in OUT) + " |")
md += ["", "Per sector at 185 ppm:", "", "| Sector | Trials | PASS | PARTIAL | INCONCLUSIVE | FAIL |", "|---|---:|---:|---:|---:|---:|"]
for s in ("S6", "S87", "S98", "S107"):
    t = res["h1"]["185ppm"][s]; md.append(f"| {s}{' (two sectors; not pooled)' if s == 'S98' else ''} | {t['n']} | " + " | ".join(pct(t['outcome'][k], t['n']) for k in OUT[:4]) + " |")
t0 = res["h0"]["pooled_S6_S87_S107"]
md += ["", "## Noise only (H0), pooled S6 + S87 + S107", "",
       f"Clause A at random periods and phases ({t0['n']} trials): " + ", ".join(f"{k} {pct(t0['clause_a'][k], t0['n'])}" for k in A[:4]) + ".",
       f"Outcomes: PARTIAL {pct(t0['outcome']['PARTIAL'], t0['n'])}, INCONCLUSIVE {pct(t0['outcome']['INCONCLUSIVE'], t0['n'])}, FAIL {pct(t0['outcome']['FAIL'], t0['n'])}.",
       "",
       "**Structural zero.** Each sector's noise-only BLS top 3 is fixed, and no allowed trial period lies within 0.1 % of any of its peaks:",
       ""]
md += [f"- S{s}: peaks {', '.join(f'{p:.4f}' for p in v['noise_only_top3_periods_d'])} d; reachable: {'yes' if v['pass_possible_under_h0'] else 'none'}." for s, v in struct.items()]
md += ["", "So B_TOP3, and therefore PASS, cannot occur in these noise-only trials. **The zero PASS count is a structural zero, not an estimate of a false-PASS rate.**",
       "Clause A's noise-only frequencies are not affected by this.",
       "", "## Injection model and cleaning", "",
       "Injected geometric T14 (circular, b = 0.4024; a/R* scaled with P', which holds the duration only approximately): " + "; ".join(f"{int(d)} ppm {v[0]:.3f}-{v[1]:.3f} h" for d, v in dur.items()) + ".",
       "1.5 h is clause A's scoring window, not the injected T14.",
       "Depth is defined as clause A measures it, on the noiseless model.",
       "Residual clause-A depth at the true ephemeris after dividing out the registration-shape model: " + "; ".join(f"S{s} {v['depth_ppm']:.0f} +- {v['sigma_ppm']:.0f} ppm" for s, v in res["cleaning_residual"].items()) + ".",
       "The cleaned light curves may retain model error and unrelated signals.",
       "", "## Limits", "",
       "- The trials share one noise realization per sector, so the frequencies carry more uncertainty than their counts suggest, and the three sectors differ (see per-sector rows).",
       "- The trial periods avoid a 2 % band around TOI-2514.01's eleventh harmonic, which contains the candidate period (0.5719 d lies 1.6 % below 6.3951/11), so transfer to the frozen ephemeris is an assumption.",
       "- The 11 compared scientific fields of the harness controls matched the training summaries; that is not a complete equivalence of every scorer path.",
       "- A predictive calibration, with variation between noise realizations and null BLS peaks able to hit, would need its own design, declared before it is run and before any test photometry."]
open(out_m, "w").write("\n".join(md) + "\n"); print("\n".join(md[10:16])); print({s: v["pass_possible_under_h0"] for s, v in struct.items()})
