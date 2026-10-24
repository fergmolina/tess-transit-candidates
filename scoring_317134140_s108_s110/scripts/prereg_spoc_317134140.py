"""Dedicated scorer for the TIC 317134140 pre-registration (frozen 2026-10-17 18:30:15 UTC; results/vet/317134140/PREREGISTRATION.md),
version 1.3 (2026-10-24; DECISIONS 172-179). It is a DATED OPERATIONALIZATION of the qualitative frozen test

    "Test: stacked depth at predicted phase in each of S108/S109/S110 should be ~185 +- 40 ppm; blind BLS of each sector should rank
     0.5719 d near the top."  (Data used: SPOC 2-min; TOI-2514.01, P = 6.3951381 d, masked.)

The frozen text fixes the two clauses, the depth band and the product. Every number below that is not in it is a post-freeze operational
choice, declared before any test-sector data: the 10-event minimum, the eligibility rule, 200 random shifts, the nominal 1.96-sigma
interval, depth/sigma >= 2, top 3 = "near the top", the 0.1 % period tolerance and the outcome labels. All are fixed in the locked config
(configs/conformance/317134140_spoc_S<sector>.json).
- Product: SPOC 2-min light curve (tess<date>-s<SSSS>-<TIC 16 digits>-<pipeline>-s_lc.fits), PDCSAP_FLUX. Header checks (INVALID_INPUT
  on any failure, including missing or malformed keywords or columns): ORIGIN 'NASA/Ames'; TICID 317134140; SECTOR = file and config
  sector; TIMESYS 'TDB', TIMEREF 'SOLARSYSTEM', TIMEUNIT 'd', BJDREFI 2457000, BJDREFF absent or 0; columns TIME, PDCSAP_FLUX,
  PDCSAP_FLUX_ERR, QUALITY. Usable cadences: QUALITY == 0, finite time, flux and error, error > 0. Times must be strictly increasing
  (otherwise INVALID_INPUT). The release of record (the eligible version listed at the first recorded check; an earlier replaced
  delivery cannot be excluded) is bound outside this scorer: scripts/spoc_selection.py writes a metadata-only selection record before
  download and an acquisition record after it, and scripts/validate_nonclock_inputs.py --stage result requires both and checks them
  against this output.
- Preprocessing: the registration's own preparation (public scripts/blind_seasons_317134140.py prep(), line 12) with three stated
  differences. The candidate is not masked during detrending, so the search stays blind. The PDCSAP_FLUX_ERR errors are used (prep()
  used a constant point-to-point error). The clipping MAD is computed over all retained points (prep(): candidate-excluded points).
  The steps are: tsearch.load_spoc_lc; keep = tsearch.trim_edges(t) AND NOT wotan.transit_mask(TOI-2514.01: P 6.3951381 d, T0 BTJD
  2215.084143, full window 1.5 x 4.047 h), so the TOI is removed BEFORE detrending; wotan biweight 0.5 d (break_tolerance 0.5);
  upward-only 5-sigma clip. Fewer than 10 usable cadences at any step -> INSUFFICIENT. Cadences removed by the TOI mask are recorded.
- Clause A (compatibility with the frozen depth plus positive-depth evidence; not a measurement constrained to the band): uses the
  frozen predicted times of this sector (prediction CSV, SHA-256 pinned). Every predicted row of the sector is a candidate event; the
  CSV column in_science_orbit is not used. An event is eligible if >= 50 % of its expected 2-min cadences within +-T14/2 (T14 1.50 h)
  are present after preprocessing and it has >= 10 out-of-transit cadences on each side within 0.75-3.0 h of the predicted time.
  Depth = median(out-of-transit flux) - mean(in-transit flux), pooled over all eligible events. sigma = standard deviation of the same
  statistic at 200 seeded random phase shifts (uniform in 0.15-0.85 P, applied to all events together).
  INSUFFICIENT if < 10 eligible events, < 100 usable shifts, or sigma is nonfinite or <= 0.
  A_LOW: depth + 1.96 sigma < 145 ppm.   A_HIGH: depth - 1.96 sigma > 225 ppm.
  A_CONSISTENT: depth +- 1.96 sigma overlaps [145, 225] ppm AND depth / sigma >= 2.   A_INCONCLUSIVE: otherwise.
  1.96 is a nominal multiplier. The random-phase sigma is an empirical spread, not a calibrated Gaussian error, so the interval has no
  established 95 % coverage under real systematics.
- Clause B (blind BLS rank): the ORIGINAL per-sector search (search_pipeline.bls_stats on 6-min bins, period_grid from 0.5 d to
  max(1, baseline/2) with oversample 3, durations 1-4 h), which keeps the top 3 distinct peaks (> 1 % apart in period). B_TOP3 if one of
  them is within 0.1 % of 0.5718634 d; aliases (P/2, 2P) are reported but do not count. B_NOT_TOP3 otherwise. Not run when clause A is
  INSUFFICIENT.
- Sector outcome, ORDERED (the first rule that applies):
  (1) INSUFFICIENT if clause A is INSUFFICIENT; (2) FAIL if A_LOW, whatever clause B says; (3) PASS if A_CONSISTENT and B_TOP3;
  (4) PARTIAL if exactly one of A_CONSISTENT / B_TOP3 holds (this includes A_HIGH + B_TOP3 and A_INCONCLUSIVE + B_TOP3);
  (5) INCONCLUSIVE otherwise. INVALID_INPUT for refused inputs.
  Only PASS meets both frozen clauses. PARTIAL and INCONCLUSIVE are not confirmations. FAIL is adverse evidence under this declared
  measurement model, not proof that the signal is absent.
  Each sector is scored and reported separately; sectors are never pooled and never replaced.
Not a validation of the planet. Usage:
  python -I prereg_spoc_317134140.py --config C --lc FITS --out OUT.json
  python -I prereg_spoc_317134140.py --insample-check --lc FITS --out OUT.json   (mechanics check on a TRAINING sector, predicted times
       generated from the frozen T0/P; refuses any sector >= 108; never an outcome)"""
import sys, os, re, json, hashlib, argparse
R = "/Users/fernando/Desktop/NASA"; sys.path.insert(0, f"{R}/scripts")
VERSION = "1.3"
SPOC_NAME = re.compile(r"^tess(\d{13})-s(\d{4})-(\d{16})-(\d{4})-s_lc\.fits$")
P_SIG, T0_SIG, T14_H = 0.5718634, 1468.67922, 1.50
P_TOI, T0_TOI, DUR_TOI_H = 6.3951381, 2215.084143000189, 4.047
TOI_MASK_MULT = 1.5   # full window = 1.5 x duration, as wotan.transit_mask in the registration's prep()
BAND = (145.0, 225.0)
MIN_CAD, MIN_EVENTS, N_SHIFTS, MIN_SHIFTS = 10, 10, 200, 100
COLUMNS = ("TIME", "PDCSAP_FLUX", "PDCSAP_FLUX_ERR", "QUALITY")
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()

class Insufficient(Exception): pass

def preprocess(path):
    import numpy as np
    from tsearch import load_spoc_lc, trim_edges
    from wotan import flatten, transit_mask
    t, f, fe, m = load_spoc_lc(path)
    good = fe > 0; t, f, fe = t[good], f[good], fe[good]
    if len(t) < MIN_CAD: raise Insufficient(f"{len(t)} usable cadences (QUALITY == 0, finite, error > 0)")
    if np.any(np.diff(t) <= 0): raise ValueError("cadence times are not strictly increasing")
    trim = trim_edges(t); tm = transit_mask(time=t, period=P_TOI, duration=TOI_MASK_MULT * DUR_TOI_H / 24, T0=T0_TOI); keep = trim & ~tm
    m = dict(m, toi_mask_removed=int((trim & tm).sum()), toi_mask_mult=TOI_MASK_MULT); t, f, fe = t[keep], f[keep], fe[keep]
    if len(t) < MIN_CAD: raise Insufficient(f"{len(t)} cadences after edge trim and TOI mask")
    flat = flatten(t, f, method="biweight", window_length=0.5, break_tolerance=0.5); ok = np.isfinite(flat)
    if ok.sum() < MIN_CAD: raise Insufficient(f"{int(ok.sum())} finite cadences after detrending")
    mad = 1.4826 * np.median(np.abs(flat[ok] - np.median(flat[ok]))); ok &= flat < 1 + 5 * mad
    if ok.sum() < MIN_CAD: raise Insufficient(f"{int(ok.sum())} cadences after clipping")
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
    for _ in range(N_SHIFTS):
        s, k = stat(np.asarray(tcs) + rng.uniform(0.15, 0.85) * P_SIG)
        if s is not None: null.append(s)
    sig = float(np.std(null)) if len(null) >= MIN_SHIFTS else float("nan")
    res = dict(depth_ppm=dep, sigma_ppm=sig, n_eligible=n, n_predicted=len(tcs), n_null=len(null))
    if n < MIN_EVENTS or dep is None: res["clause_a"] = "INSUFFICIENT"; res["insufficient_reason"] = f"{n} eligible events (< {MIN_EVENTS})"; return res
    if not (np.isfinite(sig) and sig > 0): res["clause_a"] = "INSUFFICIENT"; res["insufficient_reason"] = f"unusable noise estimate (sigma {sig}, {len(null)} usable shifts)"; return res
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
    top = [dict(period=p["period"], t0=p["t0"], duration_h=p["duration_h"], n_transits=p["n_transits"], sde=p["sde"], depth_ppm=p["depth"] * 1e6) for p in peaks]
    hit = any(abs(p["period"] / P_SIG - 1) <= 0.001 for p in peaks)
    alias = [r for r in (0.5, 2.0) if any(abs(p["period"] / (P_SIG * r) - 1) <= 0.001 for p in peaks)]
    return dict(clause_b="B_TOP3" if hit else "B_NOT_TOP3", top3=top, alias_hits=alias)

def sector_outcome(a, b):
    """Ordered mapping: the first rule that applies."""
    if a == "INSUFFICIENT": return "INSUFFICIENT"
    if a == "A_LOW": return "FAIL"
    if a == "A_CONSISTENT" and b == "B_TOP3": return "PASS"
    if (a == "A_CONSISTENT") != (b == "B_TOP3"): return "PARTIAL"
    return "INCONCLUSIVE"

def read_header(path, sector):
    """Header and column checks; returns (provenance, error message or None). Never raises on a malformed file."""
    from astropy.io import fits
    try:
        with fits.open(path, memmap=False) as h:
            if len(h) < 2: return {}, "no light-curve extension"
            h0, h1 = h[0].header, h[1].header; cols = getattr(h[1], "columns", None); names = set(cols.names) if cols is not None else set()
            prov = {k: (None if h0.get(k) is None else str(h0.get(k))) for k in ("ORIGIN", "TICID", "SECTOR", "PROCVER", "DATA_REL", "DATE", "CAMERA", "CCD")}
            prov.update({k: (None if h1.get(k) is None else str(h1.get(k))) for k in ("TIMESYS", "TIMEREF", "TIMEUNIT", "BJDREFI", "BJDREFF")})
    except Exception as e: return {}, f"unreadable FITS ({type(e).__name__})"
    if prov["ORIGIN"] != "NASA/Ames": return prov, f"ORIGIN {prov['ORIGIN']!r} is not 'NASA/Ames'"
    try: tic, sec = int(prov["TICID"]), int(prov["SECTOR"])
    except (TypeError, ValueError): return prov, "header TICID/SECTOR missing or malformed"
    if tic != 317134140 or sec != sector: return prov, f"header TICID/SECTOR {tic}/{sec} != 317134140/{sector}"
    try: bjdrefi_ok = int(prov["BJDREFI"]) == 2457000
    except (TypeError, ValueError): bjdrefi_ok = False
    try: bjdreff_ok = prov["BJDREFF"] is None or float(prov["BJDREFF"]) == 0.0
    except (TypeError, ValueError): bjdreff_ok = False
    if prov["TIMESYS"] != "TDB" or prov["TIMEREF"] != "SOLARSYSTEM" or prov["TIMEUNIT"] != "d" or not bjdrefi_ok or not bjdreff_ok:
        return prov, (f"time header TIMESYS/TIMEREF/TIMEUNIT/BJDREFI/BJDREFF = {prov['TIMESYS']}/{prov['TIMEREF']}/{prov['TIMEUNIT']}/"
                      f"{prov['BJDREFI']}/{prov['BJDREFF']}, expected TDB/SOLARSYSTEM/d/2457000/absent or 0")
    miss = [c for c in COLUMNS if c not in names]
    if miss: return prov, f"missing columns {miss}"
    return prov, None

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--config"); ap.add_argument("--lc", required=True); ap.add_argument("--out", required=True)
    ap.add_argument("--insample-check", action="store_true"); a = ap.parse_args()
    if os.path.exists(a.out): raise SystemExit(f"refused: {a.out} exists")
    import platform, importlib.metadata, numpy, scipy, astropy
    res = dict(version=VERSION, script_sha256=sha(os.path.abspath(__file__)), lc_file=os.path.basename(a.lc), lc_sha256=sha(a.lc),   # hash first, so early refusals stay bindable
               helper_sha256={k: sha(f"{R}/scripts/{k}.py") for k in ("tsearch", "search_pipeline")},
               software=dict(python=platform.python_version(), numpy=numpy.__version__, scipy=scipy.__version__, astropy=astropy.__version__, wotan=importlib.metadata.version("wotan")))
    def finish(o): res["outcome"] = o; json.dump(res, open(a.out, "w"), indent=1, default=str); print(o); sys.exit(0)
    mname = SPOC_NAME.match(os.path.basename(a.lc))
    if not mname or int(mname.group(3)) != 317134140: finish("INVALID_INPUT (file name is not a SPOC 2-min light curve of TIC 317134140)")
    sector = int(mname.group(2)); res["spoc_pipeline_field"] = mname.group(4)
    if a.insample_check:
        if sector >= 108: finish("REFUSED (insample-check refuses test sectors >= 108)")
        res["mode"] = "INSAMPLE_CHECK (training sector; predicted times generated from the frozen T0/P; NOT an outcome)"
    else:
        if not a.config: finish("INVALID_INPUT (config required)")
        try: cfg = json.load(open(a.config)); cfg_sector = int(cfg["sector"])
        except (OSError, ValueError, KeyError, TypeError) as e: finish(f"INVALID_INPUT (config unreadable: {type(e).__name__})")
        res["config_sha256"] = sha(a.config); res["sector"] = cfg_sector
        if sector != cfg_sector: finish(f"INVALID_INPUT (file sector {sector} != config sector {cfg_sector})")
        if res["script_sha256"] != cfg.get("scorer_sha256"): finish("INVALID_INPUT (scorer SHA-256 differs from the config)")
        for k in ("tsearch", "search_pipeline"):
            if res["helper_sha256"][k] != cfg.get(f"{k}_sha256"): finish(f"INVALID_INPUT ({k}.py SHA-256 differs from the config)")
        if not os.path.exists(cfg.get("pred_csv", "")) or sha(cfg["pred_csv"]) != cfg.get("pred_sha256"): finish("INVALID_INPUT (prediction CSV SHA-256 differs from the config)")
    prov, err = read_header(a.lc, sector); res["provenance"] = prov
    if err: finish(f"INVALID_INPUT ({err})")
    if a.insample_check: tcs = None
    else:
        import csv
        tcs = [float(r["tc_BJD_TDB"]) - 2457000 for r in csv.DictReader(open(cfg["pred_csv"])) if int(r["sector"]) == sector]
        if not tcs: finish("INVALID_INPUT (no predicted event in this sector)")
    try: t, f, fe, m = preprocess(a.lc)
    except Insufficient as e: res["insufficient_reason"] = str(e); res["clause_a"] = "INSUFFICIENT"; res["clause_b"] = "NOT_RUN"; finish("INSUFFICIENT")
    except ValueError as e: finish(f"INVALID_INPUT ({e})")
    res["n_cadences"] = int(len(t)); res["toi_mask_removed"] = m["toi_mask_removed"]
    if tcs is None:
        import numpy as np
        n0, n1 = int(np.ceil((t.min() - T0_SIG) / P_SIG)), int(np.floor((t.max() - T0_SIG) / P_SIG)); tcs = [T0_SIG + n * P_SIG for n in range(n0, n1 + 1)]
    res.update(clause_a(t, f, tcs))
    if res["clause_a"] == "INSUFFICIENT": res["clause_b"] = "NOT_RUN"; finish("INSUFFICIENT")
    res.update(clause_b(t, f, fe))
    finish(sector_outcome(res["clause_a"], res["clause_b"]))

if __name__ == "__main__": main()
