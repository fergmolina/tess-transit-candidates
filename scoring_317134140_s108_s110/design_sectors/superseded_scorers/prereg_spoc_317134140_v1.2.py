"""Dedicated scorer for the TIC 317134140 pre-registration (frozen 2026-10-17 18:30:15 UTC; results/vet/317134140/PREREGISTRATION.md),
version 1.2 (2026-10-24; DECISIONS 172-176). It implements exactly the frozen test:

    "Test: stacked depth at predicted phase in each of S108/S109/S110 should be ~185 +- 40 ppm; blind BLS of each sector should rank
     0.5719 d near the top."  (Data used: SPOC 2-min; TOI-2514.01, P = 6.3951381 d, masked.)

Every operational choice is fixed in the locked config (configs/conformance/317134140_spoc_S<sector>.json) before any test-sector data:
- Product: SPOC 2-min light curve (tess<date>-s<SSSS>-<TIC 16 digits>-<pipeline>-s_lc.fits, header ORIGIN 'NASA/Ames'), PDCSAP_FLUX,
  QUALITY == 0, finite values. First SPOC delivery of the sector is the release of record (the config names how it is identified).
- Preprocessing (v1.2), the registration's own preparation (public scripts/blind_seasons_317134140.py and final_ephemeris_317134140.py,
  prep(), line 12 / 20) without its candidate mask, so the search stays blind: tsearch.load_spoc_lc (PDCSAP, QUALITY == 0); keep =
  tsearch.trim_edges(t) AND NOT wotan.transit_mask(TOI-2514.01: P 6.3951381 d, T0 BTJD 2215.084143, duration 1.5 x 4.047 h), i.e. the TOI
  is removed BEFORE detrending; wotan biweight 0.5 d (break_tolerance 0.5); upward-only 5-sigma clip; PDCSAP_FLUX_ERR errors. (v1.0/v1.1
  detrended first and masked after, at 1.5x and 2.5x; DECISIONS 173-176.) Cadences removed by the TOI mask are recorded.
- Clause A, stacked depth at the predicted phase: the frozen predicted times of this sector (prediction CSV, SHA-256 pinned). An event
  is eligible if >= 50 % of its expected 2-min cadences within +-T14/2 (T14 = 1.50 h) are present after preprocessing and it has
  >= 10 out-of-transit cadences on each side within 0.75-3.0 h of the predicted time. Depth = median(out-of-transit flux) - mean(in-
  transit flux) over all eligible events pooled. Uncertainty = standard deviation of the same statistic at 200 seeded random phase
  shifts (uniform in 0.15-0.85 P, applied to all events together). Needs >= 10 eligible events, else INSUFFICIENT.
  Every predicted row of the sector is a candidate event; the CSV column in_science_orbit is not used (eligibility is decided only
  by data coverage after preprocessing).
  A_CONSISTENT: the interval depth +- 1.96 sigma overlaps [145, 225] ppm AND depth / sigma >= 2.
  A_LOW: depth + 1.96 sigma < 145 ppm.   A_HIGH: depth - 1.96 sigma > 225 ppm.   A_INCONCLUSIVE: otherwise.
- Clause B, blind BLS rank: the ORIGINAL per-sector search (search_pipeline.bls_stats on 6-min bins, period_grid from 0.5 d to
  max(1, baseline/2) with oversample 3, durations 1-4 h), which keeps the top 3 distinct peaks (> 1 % apart in period). B_TOP3 if one of
  them is within 0.1 % of 0.5718634 d; aliases (P/2, 2P) are reported but do not count. B_NOT_TOP3 otherwise.
- Sector outcome: PASS = A_CONSISTENT and B_TOP3; FAIL = A_LOW (signal absent at the predicted phase), whatever B says; PARTIAL = exactly
  one of A_CONSISTENT / B_TOP3; INCONCLUSIVE = otherwise; INSUFFICIENT and INVALID_INPUT as above. Each sector is scored and reported
  separately; sectors are never pooled; there is no replacement of a sector.
Not a validation of the planet. Usage:
  python -I prereg_spoc_317134140.py --config C --lc FITS --out OUT.json
  python -I prereg_spoc_317134140.py --insample-check --lc FITS --out OUT.json   (mechanics check on a TRAINING sector, predicted times
       generated from the frozen T0/P; refuses any sector >= 108; never an outcome)"""
import sys, os, re, json, hashlib, argparse
R = "/Users/fernando/Desktop/NASA"; sys.path.insert(0, f"{R}/scripts")
SPOC_NAME = re.compile(r"^tess(\d{13})-s(\d{4})-(\d{16})-(\d{4})-s_lc\.fits$")
P_SIG, T0_SIG, T14_H = 0.5718634, 1468.67922, 1.50
P_TOI, T0_TOI, DUR_TOI_H = 6.3951381, 2215.084143000189, 4.047
TOI_MASK_MULT = 1.5   # full window = 1.5 x duration, as wotan.transit_mask in the registration's prep()
BAND = (145.0, 225.0)
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()

def preprocess(path):
    import numpy as np
    from tsearch import load_spoc_lc, trim_edges
    from wotan import flatten, transit_mask
    t, f, fe, m = load_spoc_lc(path)
    trim = trim_edges(t); tm = transit_mask(time=t, period=P_TOI, duration=TOI_MASK_MULT * DUR_TOI_H / 24, T0=T0_TOI); keep = trim & ~tm
    m = dict(m, toi_mask_removed=int((trim & tm).sum()), toi_mask_mult=TOI_MASK_MULT); t, f, fe = t[keep], f[keep], fe[keep]
    flat = flatten(t, f, method="biweight", window_length=0.5, break_tolerance=0.5); ok = np.isfinite(flat)
    mad = 1.4826 * np.median(np.abs(flat[ok] - np.median(flat[ok]))); ok &= flat < 1 + 5 * mad
    return t[ok], flat[ok], fe[ok], m

def clause_a(t, f, tcs, cad_d=2 / 1440, seed=317134140):
    import numpy as np
    half = T14_H / 48; lo, hi = 0.75 / 24, 3.0 / 24; nexp = max(1, int(round(2 * half / cad_d)))
    def stat(centres):
        inn, out, n = [], [], 0
        for tc in centres:
            d = t - tc; i = np.abs(d) < half; o = (np.abs(d) > lo) & (np.abs(d) < hi)
            if i.sum() >= 0.5 * nexp and (o & (d < 0)).sum() >= 10 and (o & (d > 0)).sum() >= 10:
                inn.append(f[i]); out.append(f[o]); n += 1
        if n == 0: return None, 0
        return (np.median(np.concatenate(out)) - np.mean(np.concatenate(inn))) * 1e6, n
    dep, n = stat(tcs)
    rng = np.random.default_rng(seed); null = []
    for _ in range(200):
        s, k = stat(np.asarray(tcs) + rng.uniform(0.15, 0.85) * P_SIG)
        if s is not None: null.append(s)
    sig = float(np.std(null)) if len(null) > 10 else float("nan")
    res = dict(depth_ppm=dep, sigma_ppm=sig, n_eligible=n, n_predicted=len(tcs), n_null=len(null))
    if n < 10 or dep is None or not np.isfinite(sig): res["clause_a"] = "INSUFFICIENT"; return res
    lo95, hi95 = dep - 1.96 * sig, dep + 1.96 * sig
    if hi95 < BAND[0]: res["clause_a"] = "A_LOW"
    elif lo95 > BAND[1]: res["clause_a"] = "A_HIGH"
    elif (lo95 <= BAND[1] and hi95 >= BAND[0]) and dep / sig >= 2: res["clause_a"] = "A_CONSISTENT"
    else: res["clause_a"] = "A_INCONCLUSIVE"
    return res

def clause_b(t, f, fe):
    import numpy as np
    from search_pipeline import bin_lc, period_grid, bls_stats
    durs = np.array([1.0, 1.5, 2.0, 3.0, 4.0]) / 24; base = t.max() - t.min()
    pg = period_grid(base, 0.5, max(1.0, base / 2), durs.min(), oversample=3)
    tb, fb, eb = bin_lc(t, f, fe, 6 / 1440); peaks = bls_stats(tb, fb, eb, pg, durs)
    top = [dict(period=p["period"], sde=p["sde"], depth_ppm=p["depth"] * 1e6) for p in peaks]
    hit = any(abs(p["period"] / P_SIG - 1) <= 0.001 for p in peaks)
    alias = [r for r in (0.5, 2.0) if any(abs(p["period"] / (P_SIG * r) - 1) <= 0.001 for p in peaks)]
    return dict(clause_b="B_TOP3" if hit else "B_NOT_TOP3", top3=top, alias_hits=alias)

def sector_outcome(a, b):
    if a == "INSUFFICIENT": return "INSUFFICIENT"
    if a == "A_LOW": return "FAIL"
    if a == "A_CONSISTENT" and b == "B_TOP3": return "PASS"
    if (a == "A_CONSISTENT") != (b == "B_TOP3"): return "PARTIAL"
    return "INCONCLUSIVE"

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--config"); ap.add_argument("--lc", required=True); ap.add_argument("--out", required=True)
    ap.add_argument("--insample-check", action="store_true"); a = ap.parse_args()
    if os.path.exists(a.out): raise SystemExit(f"refused: {a.out} exists")
    import platform, importlib.metadata, numpy, scipy, astropy
    res = dict(version="1.2", script_sha256=sha(os.path.abspath(__file__)), lc_file=os.path.basename(a.lc), lc_sha256=sha(a.lc),   # hash first, so early refusals stay bindable
               software=dict(python=platform.python_version(), numpy=numpy.__version__, scipy=scipy.__version__, astropy=astropy.__version__, wotan=importlib.metadata.version("wotan")))
    def finish(o): res["outcome"] = o; json.dump(res, open(a.out, "w"), indent=1, default=str); print(o); sys.exit(0)
    mname = SPOC_NAME.match(os.path.basename(a.lc))
    if not mname or int(mname.group(3)) != 317134140: finish("INVALID_INPUT (file name is not a SPOC 2-min light curve of TIC 317134140)")
    sector = int(mname.group(2))
    if a.insample_check:
        if sector >= 108: finish("REFUSED (insample-check refuses test sectors >= 108)")
        res["mode"] = "INSAMPLE_CHECK (training sector; predicted times generated from the frozen T0/P; NOT an outcome)"
    else:
        if not a.config: finish("INVALID_INPUT (config required)")
        cfg = json.load(open(a.config)); res["config_sha256"] = sha(a.config); res["sector"] = cfg["sector"]
        if sector != cfg["sector"]: finish(f"INVALID_INPUT (file sector {sector} != config sector {cfg['sector']})")
        if res["script_sha256"] != cfg["scorer_sha256"]: finish("INVALID_INPUT (scorer SHA-256 differs from the config)")
        for k in ("tsearch", "search_pipeline"):
            if sha(f"{R}/scripts/{k}.py") != cfg[f"{k}_sha256"]: finish(f"INVALID_INPUT ({k}.py SHA-256 differs from the config)")
        if sha(cfg["pred_csv"]) != cfg["pred_sha256"]: finish("INVALID_INPUT (prediction CSV SHA-256 differs from the config)")
        rel = cfg.get("release_of_record") or {}
        if rel.get("pipeline") and mname.group(4) != rel["pipeline"]: res["release_note"] = f"pipeline {mname.group(4)} != release of record {rel['pipeline']}"; finish("INVALID_INPUT (not the release of record)")
    from astropy.io import fits
    with fits.open(a.lc, memmap=False) as h:
        h0, h1 = h[0].header, h[1].header
        prov = dict(ORIGIN=h0.get("ORIGIN"), TICID=h0.get("TICID"), SECTOR=h0.get("SECTOR"), TIMESYS=h1.get("TIMESYS"), BJDREFI=h1.get("BJDREFI"),
                    PROCVER=h0.get("PROCVER"), DATA_REL=h0.get("DATA_REL"), DATE=h0.get("DATE"))
    res["provenance"] = prov
    if str(prov["ORIGIN"]) != "NASA/Ames": finish(f"INVALID_INPUT (ORIGIN {prov['ORIGIN']!r} is not 'NASA/Ames')")
    if int(prov["TICID"]) != 317134140 or int(prov["SECTOR"]) != sector: finish("INVALID_INPUT (header TICID/SECTOR mismatch)")
    if str(prov["TIMESYS"]) != "TDB" or int(prov["BJDREFI"]) != 2457000: finish("INVALID_INPUT (time system is not BTJD/TDB)")
    t, f, fe, m = preprocess(a.lc)
    if a.insample_check:
        import numpy as np
        n0, n1 = int(np.ceil((t.min() - T0_SIG) / P_SIG)), int(np.floor((t.max() - T0_SIG) / P_SIG)); tcs = [T0_SIG + n * P_SIG for n in range(n0, n1 + 1)]
    else:
        import csv
        tcs = [float(r["tc_BJD_TDB"]) - 2457000 for r in csv.DictReader(open(cfg["pred_csv"])) if int(r["sector"]) == sector]
        if not tcs: finish("INVALID_INPUT (no predicted event in this sector)")
    res.update(clause_a(t, f, tcs)); res.update(clause_b(t, f, fe)); res["n_cadences"] = int(len(t)); res["toi_mask_removed"] = m["toi_mask_removed"]
    finish(sector_outcome(res["clause_a"], res["clause_b"]))

if __name__ == "__main__": main()
