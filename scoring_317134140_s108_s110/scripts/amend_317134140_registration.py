"""Write the dated 2026-10-24 paragraphs into the local TIC 317134140 registration from the CURRENT lock and code hashes (scorer v1.3;
DECISIONS 172-179). Idempotent before publication: the local file is first reset to its public copy, and the script refuses unless
everything before today's first paragraph is byte-identical to that copy. It must not be run once these paragraphs are published."""
import json, hashlib
R = "/Users/fernando/Desktop/NASA"; C = f"{R}/configs/conformance"; LS = f"{C}/LOCK_2026-10-24_317134140.json"
REG, PUB = f"{R}/results/vet/317134140/PREREGISTRATION.md", f"{R}/public_release/preregistration/TIC317134140/PREREGISTRATION.md"
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
ls = json.load(open(LS)); SC = sha(f"{R}/scripts/prereg_spoc_317134140.py")
for v in ls["configs"].values():
    for k in ("prereg_spoc_317134140", "tsearch", "search_pipeline", "spoc_selection"): assert v[f"{k}_code_sha256"] == sha(f"{R}/scripts/{k}.py"), f"lock hash for {k} is stale"
s = open(REG).read(); mark = "\n\n---\n**Dated advance expectation 2026-10-24"; cut = s.index(mark) if mark in s else len(s)
if s[:cut].rstrip("\n") != open(PUB).read().rstrip("\n"): raise SystemExit("refused: the local registration differs from its public copy before the dated text")
s = open(PUB).read()
cs = sorted((v["sector"], k, v) for k, v in ls["configs"].items()); cfg = json.load(open(f"{C}/{cs[0][1]}"))
items = "; ".join(f"S{sec}: {k} (SHA-256 {v['config_sha256'][:16]}..., UNAVAILABLE cutoff {json.load(open(f'{C}/{k}'))['unavailable_cutoff_utc']})" for sec, k, v in cs)
s = s.rstrip("\n") + ("\n\n---\n**Dated advance expectation 2026-10-24 (before any S108-S110 data of this star are examined).** The frozen test above is scored by "
    "the dedicated scorer described in the scoring amendment that follows. Applied to the four TRAINING sectors, where the signal is assumed present (S6, S87, S98, "
    "S107; not an independent test), the locked procedure gives 1 PASS (S98), 2 PARTIAL (S6, S107) and 1 INCONCLUSIVE (S87). The stacked depth is consistent with "
    "185 +- 40 ppm in three of the four sectors. The per-sector blind BLS rank (top 3 distinct peaks of the original per-sector search) is met only in S98: at "
    "about 185 ppm in one sector this clause has low power, and unrelated peaks can occupy top-3 slots. For example, S98's third peak (6.399 d, 535 ppm, five events) "
    "lies 2.4 d from the TOI-2514.01 phase and is unexplained. Under the hypothesis of a real signal, the expected S108-S110 outcomes are therefore mostly PARTIAL, "
    "with PASS possible in a longer or quieter sector. This is a conditional extrapolation from four selected training sectors, not a calibrated probability. "
    "A FAIL (stacked depth significantly below 145 ppm) would be adverse evidence under the declared measurement model, not proof that the signal is absent. "
    "These are expectations, not measured outcomes.\n"
    f"\n**Dated scoring amendment 2026-10-24 (before any S108-S110 photometry of this star is examined).** The frozen test above is qualitative. It is scored "
    f"by a dated operationalization: the dedicated scorer scripts/prereg_spoc_317134140.py v1.3 (SHA-256 {SC}), on SPOC 2-min PDCSAP_FLUX. Its operational numbers "
    f"are post-freeze choices declared here before any test-sector data: the 10-event minimum, the eligibility rule, 200 random shifts, the nominal 1.96-sigma "
    f"interval, depth/sigma >= 2, top 3 as \"near the top\" (the top-3 precedent of the blind tests in DECISIONS 12, which concerned training-years searches) "
    f"and the 0.1 % period tolerance. Preprocessing: {cfg['preprocessing']}; {cfg['toi_mask']}; 0.5-d biweight. Clause B uses the original per-sector search "
    f"settings (scripts/tsearch.py SHA-256 {cfg['tsearch_sha256'][:16]}..., scripts/search_pipeline.py SHA-256 {cfg['search_pipeline_sha256'][:16]}...). "
    f"Events: {cfg['events']}. Clause A: {cfg['clause_a']}. Clause B: {cfg['clause_b']}. Sector outcome: {cfg['sector_outcome']}. Scope: {cfg['scope']}. "
    f"Release of record: {cfg['release_of_record']} (scripts/spoc_selection.py SHA-256 {cfg['selection_tool_sha256'][:16]}...). Unavailable product: each sector's "
    f"config fixes an exact cutoff, its sector end + 120 days, inclusive. Only if no SELECTED selection record is made by the cutoff is the sector UNAVAILABLE; then "
    f"no other product replaces it, and a later listing is a secondary readout only. A product selected in time may be scored later. UNAVAILABLE means that "
    f"no SELECTED record was made by the cutoff, not that no archive product ever existed. Monitoring (per sector, from its config): " + " ".join(f"S{sec}: {json.load(open(f'{C}/{k}'))['monitoring_rule']}" for sec, k, v in cs) + " "
    f"Secondary readout: {cfg['secondary_readout']}. Configs locked {cfg['locked_utc']}: {items}; lock configs/conformance/LOCK_2026-10-24_317134140.json "
    f"(SHA-256 {sha(LS)[:16]}...). The binding check scripts/validate_nonclock_inputs.py --lock <that file> must pass at the pre, selection and result stages. "
    f"Data status: S108 was observed 2026-09-07 to 10-05 and S109 is being observed; the authors attest that no S108-S110 photometry of this star has been "
    f"examined. No prediction, ephemeris or checksum is changed. DECISIONS 172-179.\n")
open(REG, "w").write(s); print("amended 317134140")
