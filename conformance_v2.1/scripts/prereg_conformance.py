"""Pre-registration CONFORMANCE evaluator v2.1 (2026-10-20; release candidate, not yet published). Separately versioned from the frozen evaluator scripts/prereg_test.py
(SHA-256 630815cc..., kept unchanged and run alongside). Written after independent reviews (public_release/reviews_2026-10-20/) showed that the frozen
evaluator averages timing offsets, does not test duration, accepts brightenings and can return EXCLUDED without full transit coverage.
This is a newly amended operational test; the departures from the original protocol are listed in the governance statement
(GOVERNANCE_S106_TESTS). It uses a joint fit across events plus per-event consistency, with all choices fixed in advance in a per-object config (configs/conformance/, made by make_conformance_configs.py).

INPUTS
  --config configs/conformance/<TIC>_S<sector>.json  (locked: prediction CSV path + SHA-256, sector, flux column, reference depth (ppm)
            and duration (h), timing rule; see make_conformance_configs.py)
  --lc     light curve of the test sector: for product "QLP" the QLP HLSP FITS (header ORIGIN 'MIT/QLP', file name
           hlsp_qlp_tess_ffi_s<SSSS>-<TIC 16 digits>_tess_v<NN>_llc.fits); a two-column CSV (time, flux) is accepted ONLY when the config
           product is "synthetic" (self-tests); anything else is refused (INVALID_INPUT).
  --clock  clock record JSON for the test sector (required for QLP sectors >= 99; produced by qlp_clock_test_sector.py). The record must
           match the config (TIC, sector, prediction-CSV hash), the --lc file (SHA-256) and the predicted event list, otherwise, or
           without it, the evaluator REFUSES to score (outcome CLOCK_UNVERIFIED). There is no bypass.

FIXED PROCEDURE
 1. Validate: prediction CSV SHA-256 == config; product (header ORIGIN and file-name pattern); FITS header SECTOR == config sector and
    TICID == config TIC (TICID must be present); extension TIMESYS 'TDB' and BJDREFI 2457000; TIME in BTJD; >= 1 predicted event in
    the sector (leading integer of tess_sector == config sector). Header provenance (ORIGIN, file name, header DATE/PROCVER/DATA_REL
    when present) and the software versions are recorded in the output.
 2. Clock: add the per-event clock correction (minutes) from the clock record to the light-curve times. Predictions are never shifted.
 2b. Edge rule (DECISIONS item 76, derived on design sectors): drop cadences within 1.5 d after the data start or any resume following a
    gap > 0.5 d, and within 0.5 d before any gap > 0.1 d or the data end (on QUALITY == 0, finite cadences).
 3. Preprocess: QUALITY == 0 and finite flux; normalise; biweight detrend (wotan, window 0.7 d, break tolerance 0.5 d) with every predicted
    transit masked over +-(1.0 x T14_ref + max(3 sigma_min, 30 min)) before detrending.
 4. Per predicted transit (status starting with "prediction", sector == config sector):
      coverage: fraction of the in-transit interval [tc - T14/2, tc + T14/2] with a cadence within half a cadence (needs >= 0.90 = "full"),
      and >= 0.5 x T14 of data on EACH side within 1.5 x T14 beyond the transit edges ("baselines"). Only FULL events are eligible.
 5. Joint box search over all eligible events, with a COMMON mid-time offset (2-min grid, +-0.3 d) and duration (0.5-2.0 x T14_ref,
    5 % grid). For each event and grid point: depth = median of out-of-box points within +-3 box durations minus the in-box mean (a robust
    local baseline that a short brightening cannot raise); error = robust (MAD) out-of-transit point scatter x red-noise factor beta
    (>= 1, time-averaging at the reference duration) x sqrt(1/n_in + (pi/2)/n_out) (the baseline is a median). Stacked depth = inverse-variance weighted mean over events.
    A grid point is VALID only if: stacked depth > 0 (dips only), the per-event depths are mutually consistent (chi2 p >= 0.01) and >= 2
    events are positive at 1 sigma. Joint SNR = stacked depth / stacked error.
 6. "Comparable" signal at a set of grid points: the best VALID fit with duration in 0.7-1.3 x T14_ref has SNR >= 5 and depth 0.5-1.5 x
    ref, and SNR^2(band) >= SNR^2(any duration) - 4 over the same offset set. This is a nominal score rule, not a calibrated likelihood
    or 2-sigma duration interval; 0.6x and 1.5x durations are often accepted at operating SNR (procedure section 5).
    Separately, each event's own best positive box (free offset/duration) is recorded for information.
 7. gate = max(3 mean(sigma_min), 30 min) [protocol, adopted]; the outcome is also computed with min(3 mean(sigma_min), 30 min).
 8. Outcome (precedence fixed in advance):
      INSUFFICIENT : < 2 eligible (fully covered) events
      RECOVERED    : comparable signal among offsets |o| <= max(gate, 30) + T14/2, and that band-duration fit's offset |o| <= gate, AND
                     the timing-split check: eligible events split by epoch parity, each half stacked at the joint duration over the same
                     local window; both halves non-empty with best offset |o| <= gate (else AMBIGUOUS). The parity split reduces
                     some alternating-offset recoveries; it does not eliminate alternating or non-alternating timing failures at
                     operating SNR (DECISIONS 81, 86).
      INCONSISTENT : the best VALID band-duration fit over all offsets (+-0.3 d) is comparable, has joint SNR >= 7 (look-elsewhere
                     allowance for ~20-40 independent offset/duration trials) and |o| > max(gate, 30 min). Per-event displaced dips
                     are recorded for information only (calibration showed independent noise peaks at unrelated offsets).
      EXCLUDED     : (a) at duration = ref, stacked depth + 3 sigma < 0.3 x ref at EVERY offset |o| <= gate, with EVERY eligible event
                     measured (>= 3 in-box, >= 5 baseline points) at every such offset; (b) per-event depths at the
                     predicted times consistent (chi2 p >= 0.01); (c) no VALID fit with SNR >= 5 and depth >= 0.5 x ref within +-0.3 d
      AMBIGUOUS    : anything else (declared residual category)
    The frozen evaluator's literal output is reported alongside. Synthetic and real-data validation: scripts/test_conformance.py,
    scripts/validate_conformance_real.py.
    Object-specific stricter clauses (config "strict_epochs"): if a listed epoch has a gap or flagged cadences within tc +- T14/2
    (clock-corrected), or is not eligible, the outcome becomes INSUFFICIENT (the procedure's outcome is kept as outcome_before_override).
    Refusals: release other than the config's release_of_record (INVALID_INPUT); clock record with a whole-cadence warning
    (CLOCK_UNVERIFIED); evaluator SHA-256 different from the config's (INVALID_INPUT); config/prediction invariants; duplicate times.
    Fewer than 10 usable cadences (QUALITY == 0, finite) after the edge rule -> INSUFFICIENT, including an all-flagged product; this is
    classified before the clock gate. Time headers must be TIMESYS TDB, BJDREFI 2457000, TIMEUNIT d and TIMEREF SOLARSYSTEM (both required), BJDREFF absent or numeric 0.
Secondary readouts (never the outcome of record): outcome_joint_only (without the split check), the min() reading, the per-event
min() reading (CLARIFICATION promise), per-event best boxes, odd/even depth diagnostic, EXCLUDED diagnostics.
OUTPUT JSON (all inputs' hashes, every per-event number, both gates, the outcome)."""
import sys, os, re, json, hashlib, argparse, platform, numpy as np, pandas as pd
from astropy.io import fits
from wotan import flatten

VERSION = "conformance-v2.1-rc4 (2026-10-20; rc3 + second re-check fixes F1 F4; DECISIONS 74-91)"

def sha(path): return hashlib.sha256(open(path, "rb").read()).hexdigest()

QLP_NAME = re.compile(r"^hlsp_qlp_tess_ffi_s(\d{4})-(\d{16})_tess_(v\d+)_llc\.fits$")

def strict_epoch_check(path, cfg, pred, corr_fn):
    """Object-specific stricter clause (config "strict_epochs", e.g. TIC 183374279 addendum 2026-10-19 item 1): for each listed epoch, in
    clock-corrected time within tc +- T14/2, any cadence with QUALITY != 0 or non-finite flux, any spacing > 1.5 median cadences (one
    missing cadence gives 2), or a first/last cadence more than 1.05 median cadences inside the window edge counts as 'a gap or flagged
    cadences at the epoch' (rc3, re-check N1). Rows with non-finite TIME count as missing. Scope: the nominal window only, not the
    whole timing gate."""
    with fits.open(path, memmap=False) as h:
        d = h[1].data; t = np.asarray(d["TIME"], float); f = np.asarray(d[cfg["flux_col"]], float); q = np.asarray(d["QUALITY"], int)
    ok_t = np.isfinite(t); t, f, q = t[ok_t], f[ok_t], q[ok_t]; o = np.argsort(t); t, f, q = t[o], f[o], q[o]; t = t + corr_fn(t)
    cad = float(np.median(np.diff(t))); half = cfg["ref_dur_h"] / 48; out = {}
    for ep in cfg["strict_epochs"]:
        row = pred[pred.epoch.astype(int) == int(ep)]
        if not len(row): out[str(ep)] = dict(violated=True, reason="epoch not among the sector's predictions"); continue
        tc = float(row.tc_btjd.iloc[0]); w = np.abs(t - tc) <= half; tw = t[w]
        why = []
        if not w.any(): why.append("no cadences")
        else:
            if np.any(q[w] != 0): why.append(f"{int(np.sum(q[w] != 0))} flagged cadences")
            if np.any(~np.isfinite(f[w])): why.append("non-finite flux")
            if len(tw) > 1 and np.max(np.diff(tw)) > 1.5 * cad: why.append("internal gap (>= 1 missing cadence)")
            if tw[0] - (tc - half) > 1.05 * cad or (tc + half) - tw[-1] > 1.05 * cad: why.append("window edge not covered")
        out[str(ep)] = dict(violated=bool(why), reason=", ".join(why) or "clean")
    return out

def load_lc(path, flux_col):
    with fits.open(path, memmap=False) as h:
        hdr0, hdr1, d = h[0].header, h[1].header, h[1].data
        t = np.asarray(d["TIME"], float); f = np.asarray(d[flux_col], float)
        if "QUALITY" not in d.columns.names: raise ValueError("no QUALITY column")
        q = np.asarray(d["QUALITY"], int)
        prov = {k: (str(hdr0[k]) if k in hdr0 else None) for k in ("ORIGIN", "TELESCOP", "SECTOR", "TICID", "CAMERA", "CCD", "DATE", "PROCVER", "DATA_REL")}
        prov.update({k: (str(hdr1[k]) if k in hdr1 else None) for k in ("TIMESYS", "TIMEREF", "BJDREFI", "BJDREFF", "TIMEUNIT")}); prov["file_name"] = os.path.basename(path)
        if "SECTOR" not in hdr0 or "TICID" not in hdr0: raise ValueError("header SECTOR/TICID missing")
        sector, tic = int(hdr0["SECTOR"]), int(hdr0["TICID"])
    m = np.isfinite(t) & np.isfinite(f) & (q == 0)
    return t[m], f[m] / np.nanmedian(f[m]), sector, tic, prov

EDGE_AFTER_D, EDGE_BEFORE_D, GAP_LONG_D, GAP_SHORT_D = 1.5, 0.5, 0.5, 0.1

def edge_trim(t, f):
    """Edge rule (DECISIONS item 76, derived on design sectors): drop cadences within EDGE_AFTER_D after the data start or any resume
    following a gap > GAP_LONG_D, and within EDGE_BEFORE_D before any gap > GAP_SHORT_D or the data end. Gaps are measured on the
    QUALITY == 0, finite-flux cadences, before the clock correction (minutes; irrelevant at this scale)."""
    dt = np.diff(t); starts = np.r_[t[0], t[1:][dt > GAP_LONG_D]]; ends = np.r_[t[:-1][dt > GAP_SHORT_D], t[-1]]
    drop = np.zeros(len(t), bool)
    for s0 in starts: drop |= (t >= s0) & (t < s0 + EDGE_AFTER_D)
    for e0 in ends: drop |= (t <= e0) & (t > e0 - EDGE_BEFORE_D)
    info = dict(rule=f"drop {EDGE_AFTER_D} d after start/resume (gap > {GAP_LONG_D} d) and {EDGE_BEFORE_D} d before gap (> {GAP_SHORT_D} d)/end",
                resumes_btjd=[float(x) for x in starts], gap_or_end_btjd=[float(x) for x in ends], n_dropped=int(drop.sum()), n_kept=int((~drop).sum()))
    return t[~drop], f[~drop], info

def red_noise_beta(t, r, dur_d, cad_d):
    """Time-averaging beta: observed scatter of bin means vs white-noise expectation, at bin = reference duration (>= 1)."""
    n = max(int(round(dur_d / cad_d)), 2); sig1 = 1.4826 * np.median(np.abs(r - np.median(r)))
    edges = np.arange(t.min(), t.max() + dur_d, dur_d); idx = np.digitize(t, edges)
    means = [r[idx == k].mean() for k in np.unique(idx) if (idx == k).sum() >= 0.7 * n]
    if len(means) < 8: return 1.0, sig1
    obs = 1.4826 * np.median(np.abs(np.array(means) - np.median(means))); exp = sig1 / np.sqrt(n)
    return max(1.0, obs / exp), sig1

def coverage(t, tc, dur_d, cad_d):
    grid = np.arange(tc - dur_d / 2, tc + dur_d / 2, cad_d)
    near = np.searchsorted(t, grid); near = np.clip(near, 1, len(t) - 1)
    dist = np.minimum(np.abs(t[near] - grid), np.abs(t[near - 1] - grid))
    frac_in = float(np.mean(dist <= cad_d / 2 + 1e-9)) if len(grid) else 0.0
    left = ((t >= tc - 2.0 * dur_d) & (t < tc - 0.5 * dur_d)).sum() * cad_d
    right = ((t > tc + 0.5 * dur_d) & (t <= tc + 2.0 * dur_d)).sum() * cad_d
    return frac_in, left / dur_d, right / dur_d

def box_fit(t, r, tc, dur_ref, sig_pt, beta, cad_d, fixed=None):
    """Best positive box: offset (min) on a 1-min grid over +-0.3 d, duration 0.5-2.0 x ref; or a fixed (offset, duration)."""
    win = np.abs(t - tc) < 0.3 + 6.5 * dur_ref; tt, rr = t[win], r[win]
    offs = [fixed[0]] if fixed else np.arange(-432, 433, 1.0)
    durs = [fixed[1]] if fixed else dur_ref * np.arange(0.5, 2.0001, 0.05)
    best = None
    for D in durs:
        for o in offs:
            c = tc + o / 1440; inn = np.abs(tt - c) < D / 2; out = (np.abs(tt - c) >= D / 2) & (np.abs(tt - c) < 3.0 * D)
            if inn.sum() < 3 or out.sum() < 5: continue
            dep = np.median(rr[out]) - np.mean(rr[inn]); err = beta * sig_pt * np.sqrt(1 / inn.sum() + (np.pi / 2) / out.sum())
            if fixed is None and dep <= 0: continue
            dchi = (dep / err) ** 2
            if best is None or dchi > best["dchi2"]: best = dict(offset_min=float(o), dur_h=float(D * 24), depth_ppm=float(dep * 1e6), err_ppm=float(err * 1e6), snr=float(dep / err), dchi2=float(dchi), n_in=int(inn.sum()))
    return best

def event_grid(t, r, tc, dur_ref, sig_pt, beta, offs, durs):
    """Box depth/error for one event on the (offset, duration) grid; robust local baseline = median of out-of-box points within +-3 box
    durations. Returns arrays [n_off, n_dur] (NaN where < 3 in-box or < 5 baseline points)."""
    win = np.abs(t - tc) < 0.3 + 6.5 * dur_ref; tt, rr = t[win], r[win]
    dep = np.full((len(offs), len(durs)), np.nan); err = dep.copy()
    for j, D in enumerate(durs):
        for i, o in enumerate(offs):
            c = tc + o / 1440; x = np.abs(tt - c); inn = x < D / 2; out = (x >= D / 2) & (x < 3.0 * D)
            ni, no = inn.sum(), out.sum()
            if ni < 3 or no < 5: continue
            dep[i, j] = np.median(rr[out]) - rr[inn].mean(); err[i, j] = beta * sig_pt * np.sqrt(1 / ni + (np.pi / 2) / no)
    return dep, err

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--config", required=True); ap.add_argument("--lc", required=True); ap.add_argument("--clock"); ap.add_argument("--out")
    a = ap.parse_args(); cfg = json.load(open(a.config))
    import scipy, wotan, astropy
    res = dict(version=VERSION, script_sha256=sha(os.path.abspath(__file__)), software=dict(python=platform.python_version(), numpy=np.__version__, scipy=scipy.__version__,
               pandas=pd.__version__, astropy=astropy.__version__, wotan=getattr(wotan, "__version__", "unknown")), config=cfg, config_sha256=sha(a.config), lc=a.lc, lc_sha256=sha(a.lc))
    if sha(cfg["pred_csv"]) != cfg["pred_sha256"]: res["outcome"] = "INVALID_INPUT (prediction CSV hash mismatch)"; return finish(res, a)
    if cfg.get("evaluator_sha256") and cfg["evaluator_sha256"] != res["script_sha256"]: res["outcome"] = "INVALID_INPUT (evaluator SHA-256 differs from the locked config)"; return finish(res, a)
    try:
        bad = [k for k in ("ref_depth_ppm", "ref_dur_h") if not (np.isfinite(float(cfg[k])) and float(cfg[k]) > 0)] + ([] if int(cfg["sector"]) == cfg["sector"] and int(cfg["tic"]) == cfg["tic"] else ["sector/tic"])
    except (KeyError, TypeError, ValueError) as e: bad = [f"config field {e}"]
    if bad: res["outcome"] = "INVALID_INPUT (config invariants: " + ", ".join(map(str, bad)) + ")"; return finish(res, a)
    product = str(cfg.get("product", "QLP"))
    if a.lc.endswith(".csv"):
        if product != "synthetic": res["outcome"] = f"INVALID_INPUT (CSV light curves are accepted only for product 'synthetic', config product is '{product}')"; return finish(res, a)
        d = pd.read_csv(a.lc); t = d.iloc[:, 0].values.astype(float); f = d.iloc[:, 1].values.astype(float); m = np.isfinite(t) & np.isfinite(f); t, f = t[m], f[m] / np.median(f[m])
        sector, tic = cfg["sector"], cfg["tic"]; res["lc_format"] = "CSV (synthetic; header checks not applicable)"
    else:
        if product != "QLP": res["outcome"] = f"INVALID_INPUT (unsupported product '{product}')"; return finish(res, a)
        mname = QLP_NAME.match(os.path.basename(a.lc))
        if not mname or int(mname.group(1)) != cfg["sector"] or int(mname.group(2)) != cfg["tic"]: res["outcome"] = "INVALID_INPUT (file name is not the QLP HLSP name for this TIC/sector)"; return finish(res, a)
        if cfg.get("release_of_record") and mname.group(3) != cfg["release_of_record"]: res["outcome"] = f"INVALID_INPUT (QLP release {mname.group(3)} is not the release of record {cfg['release_of_record']}; later releases are reported separately, never as the outcome of record)"; return finish(res, a)
        try: t, f, sector, tic, prov = load_lc(a.lc, cfg["flux_col"])
        except (ValueError, KeyError) as e: res["outcome"] = f"INVALID_INPUT ({e})"; return finish(res, a)
        res["lc_format"] = "FITS"; res["lc_provenance"] = prov
        if prov["ORIGIN"] != "MIT/QLP": res["outcome"] = f"INVALID_INPUT (header ORIGIN {prov['ORIGIN']!r} is not 'MIT/QLP')"; return finish(res, a)
        if prov["TIMESYS"] != "TDB" or prov["BJDREFI"] != "2457000": res["outcome"] = f"INVALID_INPUT (time system {prov['TIMESYS']}/{prov['BJDREFI']}, expected TDB/2457000)"; return finish(res, a)
        try: bjdreff_ok = prov["BJDREFF"] is None or float(prov["BJDREFF"]) == 0.0
        except (TypeError, ValueError): bjdreff_ok = False
        if prov["TIMEUNIT"] != "d" or prov["TIMEREF"] != "SOLARSYSTEM" or not bjdreff_ok:
            res["outcome"] = f"INVALID_INPUT (time header TIMEUNIT/TIMEREF/BJDREFF = {prov['TIMEUNIT']}/{prov['TIMEREF']}/{prov['BJDREFF']}, expected d/SOLARSYSTEM/absent or 0)"; return finish(res, a)
    if sector != cfg["sector"] or tic != cfg["tic"]: res["outcome"] = f"INVALID_INPUT (header sector {sector} / TIC {tic} != config)"; return finish(res, a)
    if len(t) and t.min() > 2e6: res["outcome"] = "INVALID_INPUT (times look like BJD, expected BTJD)"; return finish(res, a)
    o = np.argsort(t); t, f = t[o], f[o]
    if np.any(np.diff(t) <= 0): res["outcome"] = "INVALID_INPUT (duplicate or non-increasing cadence times)"; return finish(res, a)
    if len(t): t, f, res["edge_trim"] = edge_trim(t, f)
    else: res["edge_trim"] = dict(rule="not applied: no QUALITY == 0 cadences with finite time and flux", n_dropped=0, n_kept=0)   # rc4 (F1): all-flagged input
    no_data = len(t) < 10      # covers an all-flagged product (no QUALITY == 0 cadences) and an edge-emptied one alike (rc3, N4)
    pred = pd.read_csv(cfg["pred_csv"]); lead = pd.to_numeric(pred.tess_sector.astype(str).str.extract(r"^(\d+)")[0], errors="coerce")
    pred = pred[pred.status.astype(str).str.startswith("prediction") & (lead == cfg["sector"])].sort_values("tc_btjd").copy()
    res["n_predicted"] = int(len(pred))
    if not len(pred): res["outcome"] = "INVALID_INPUT (no predicted events in this sector)"; return finish(res, a)
    pbad = []
    ep_num = pd.to_numeric(pred.epoch, errors="coerce").values
    if not np.all(np.isfinite(ep_num)) or np.any(ep_num != np.round(ep_num)): pbad.append("epochs not finite integers")
    elif pred.epoch.duplicated().any(): pbad.append("duplicate epochs")
    if pred.tc_btjd.duplicated().any() or not np.all(np.isfinite(pred.tc_btjd.values.astype(float))): pbad.append("duplicate or non-finite tc")
    sg = pd.to_numeric(pred.sigma_min, errors="coerce").values
    if not np.all(np.isfinite(sg)) or np.any(sg < 0): pbad.append("sigma_min not finite and >= 0")
    if pbad: res["outcome"] = "INVALID_INPUT (prediction invariants: " + ", ".join(pbad) + ")"; return finish(res, a)
    if no_data: res["n_eligible"] = 0; res["outcome"] = res["outcome_min_gate_reading"] = "INSUFFICIENT"; res["insufficient_reason"] = "fewer than 10 usable cadences (QUALITY == 0, finite) after the edge rule; classified before the clock gate"; return finish(res, a)
    # clock gate (no bypass)
    corr = np.zeros(len(t))
    if cfg["sector"] >= 99 and product == "QLP":
        if not a.clock: res["outcome"] = "CLOCK_UNVERIFIED (no clock record supplied; scoring refused)"; return finish(res, a)
        ck = json.load(open(a.clock)); res["clock_record"] = dict(path=a.clock, sha256=sha(a.clock), version=ck.get("version"), state=ck.get("state"), alignment=ck.get("alignment"), warning=ck.get("warning"))
        ev_t = np.array(ck.get("event_btjd", []), float); ev_c = np.array(ck.get("correction_min", []), float)
        why = [w for w, bad in [("TIC", ck.get("tic") != cfg["tic"]), ("sector", ck.get("sector") != cfg["sector"]), ("light-curve SHA-256", ck.get("qlp_sha256") != res["lc_sha256"]),
                                ("prediction-CSV SHA-256", ck.get("pred_sha256") != cfg["pred_sha256"]),
                                ("event list", len(ev_t) != len(pred) or not np.allclose(ev_t, pred.tc_btjd.values.astype(float), rtol=0, atol=1e-9)),
                                ("corrections not finite", len(ev_c) != len(ev_t) or not np.all(np.isfinite(ev_c)))] if bad]
        if why: res["outcome"] = "CLOCK_UNVERIFIED (clock record does not match: " + ", ".join(why) + ")"; return finish(res, a)
        if ck.get("warning"): res["outcome"] = "CLOCK_UNVERIFIED (clock record carries a whole-cadence warning: label error and row misregistration are indistinguishable; scoring refused, DECISIONS 86)"; return finish(res, a)
        corr = np.interp(t, ev_t, ev_c) / 1440
    t = t + corr; res["clock_correction_min_range"] = [float(corr.min() * 1440), float(corr.max() * 1440)]
    strict = None
    if cfg.get("strict_epochs") and not a.lc.endswith(".csv"):
        cf = (lambda tt: np.interp(tt, ev_t, ev_c) / 1440) if (cfg["sector"] >= 99 and product == "QLP") else (lambda tt: np.zeros(len(tt)))
        strict = strict_epoch_check(a.lc, cfg, pred, cf); res["strict_epoch_check"] = strict
    dur = cfg["ref_dur_h"] / 24; dep_ref = cfg["ref_depth_ppm"] / 1e6; cad = float(np.median(np.diff(t)))
    mask = np.zeros(len(t), bool)
    for _, p in pred.iterrows(): mask |= np.abs(t - p.tc_btjd) < dur * 1.0 + max(3 * p.sigma_min, 30) / 1440
    trend = flatten(t, f, method="biweight", window_length=0.7, break_tolerance=0.5, return_trend=True, mask=mask)[1]
    r = f / trend
    good = np.isfinite(r); t, r = t[good], r[good]
    oot = np.ones(len(t), bool)
    for _, p in pred.iterrows(): oot &= np.abs(t - p.tc_btjd) > 2 * dur
    beta, sig_pt = red_noise_beta(t[oot] if oot.sum() > 50 else t, r[oot] if oot.sum() > 50 else r, dur, cad)
    res.update(beta=beta, point_scatter_ppm=sig_pt * 1e6, cadence_min=cad * 1440)
    events = []
    for _, p in pred.iterrows():
        fi, lb, rb = coverage(t, p.tc_btjd, dur, cad); full = fi >= 0.90 and lb >= 0.5 and rb >= 0.5
        ev = dict(epoch=int(p.epoch), tc_btjd=float(p.tc_btjd), sigma_min=float(p.sigma_min), cov_in=fi, base_left=lb, base_right=rb, eligible=bool(full),
                  gate_max_min=max(3 * p.sigma_min, 30.0), gate_min_min=min(3 * p.sigma_min, 30.0))
        if full:
            ev["best"] = box_fit(t, r, p.tc_btjd, dur, sig_pt, beta, cad)
            ev["at_prediction"] = box_fit(t, r, p.tc_btjd, dur, sig_pt, beta, cad, fixed=(0.0, dur))
            b = ev["best"]
            comp = b is not None and b["snr"] >= 3 and 0.5 <= b["depth_ppm"] / 1e6 / dep_ref <= 1.5 and 0.7 <= b["dur_h"] / 24 / dur <= 1.3
            ev["match_max"] = bool(comp and abs(b["offset_min"]) <= ev["gate_max_min"]); ev["match_min"] = bool(comp and abs(b["offset_min"]) <= ev["gate_min_min"])
            ev["displaced"] = bool(comp and abs(b["offset_min"]) > max(ev["gate_max_min"], 30.0))
        events.append(ev)
    res["events"] = events; el = [e for e in events if e["eligible"]]
    # per-event min() reading promised in CLARIFICATION_TIMING_RULE_2026-10-20.md (secondary readout; never the outcome of record): an
    # eligible event matches if its own best positive box (free offset +-0.3 d, duration 0.5-2.0 x ref) has SNR >= 3, depth 0.5-1.5 x ref,
    # duration 0.7-1.3 x ref and |offset| <= min(3 sigma_min, 30 min); the reading is met when >= 2 events match.
    nm = sum(bool(e.get("match_min")) for e in el)
    res["per_event_min_reading"] = dict(n_eligible=len(el), n_matched=int(nm), met=bool(nm >= 2), criterion="per event: best box SNR >= 3, depth 0.5-1.5x, duration 0.7-1.3x, |offset| <= min(3 sigma_min, 30 min); met if >= 2 events match")
    offs = np.arange(-432, 433, 2.0); durs = dur * np.arange(0.5, 2.0001, 0.05); j_ref = int(np.argmin(np.abs(durs - dur))); i0 = int(np.argmin(np.abs(offs)))
    G = [event_grid(t, r, e["tc_btjd"], dur, sig_pt, beta, offs, durs) for e in el]
    res["joint"] = None; res["stack_at_prediction"] = None
    gate_max = max(3 * float(np.mean([e["sigma_min"] for e in el])) if el else 0, 30.0); gate_min = min(3 * float(np.mean([e["sigma_min"] for e in el])) if el else 0, 30.0)
    res["gate_max_min"], res["gate_min_min"] = gate_max, gate_min
    if len(el) < 2:
        res["n_eligible"] = len(el); res["outcome"] = res["outcome_min_gate_reading"] = "INSUFFICIENT"; return finish(override(res, strict, el, cfg), a)
    from scipy.stats import chi2 as C2
    Dp = np.array([g[0] for g in G]); Ep = np.array([g[1] for g in G]); W = 1 / Ep ** 2; ok_all = np.all(np.isfinite(Dp), axis=0)
    Sd = np.nansum(Dp * W, axis=0) / np.nansum(W, axis=0); Se = 1 / np.sqrt(np.nansum(W, axis=0))
    C2v = np.nansum(((Dp - Sd[None]) / Ep) ** 2, axis=0); Pc = C2.sf(C2v, len(el) - 1); Npos = np.sum(Dp / Ep > 1, axis=0)
    VALID = ok_all & (Sd > 0) & (Pc >= 0.01) & (Npos >= 2)          # a box every event supports consistently
    Sn = np.where(VALID, Sd / Se, -np.inf)
    band = (durs >= 0.7 * dur - 1e-9) & (durs <= 1.3 * dur + 1e-9); alld = np.ones(len(durs), bool)
    def best(omask, dmask):
        M = np.where(omask[:, None] & dmask[None, :], Sn, -np.inf)
        if not np.isfinite(M).any(): return None
        io, jd = np.unravel_index(int(np.argmax(M)), M.shape)
        return dict(offset_min=float(offs[io]), dur_h=float(durs[jd] * 24), depth_ppm=float(Sd[io, jd] * 1e6), err_ppm=float(Se[io, jd] * 1e6), snr=float(Sn[io, jd]),
                    per_event_depth_ppm=(Dp[:, io, jd] * 1e6).tolist(), per_event_err_ppm=(Ep[:, io, jd] * 1e6).tolist(), consistency_chi2=float(C2v[io, jd]),
                    consistency_dof=len(el) - 1, consistency_p=float(Pc[io, jd]), n_events_positive_1sigma=int(Npos[io, jd]))
    def comparable(J_any, J_band):
        """band-duration fit: SNR >= 5 and depth 0.5-1.5 x ref, and SNR^2(band) >= SNR^2(any duration) - 4 in the same offset region
        (a nominal score rule, not a calibrated likelihood or 2-sigma interval)."""
        return bool(J_any and J_band and J_band["snr"] >= 5 and 0.5 <= J_band["depth_ppm"] / cfg["ref_depth_ppm"] <= 1.5 and J_band["snr"] ** 2 >= J_any["snr"] ** 2 - 4.0)
    i0 = int(np.argmin(np.abs(offs))); j_ref = int(np.argmin(np.abs(durs - dur)))
    res["stack_at_prediction"] = dict(depth_ppm=float(Sd[i0, j_ref] * 1e6), err_ppm=float(Se[i0, j_ref] * 1e6))
    def outcome(gate, tag):
        loc = np.abs(offs) <= max(gate, 30.0) + dur * 1440 / 2 + 1e-9
        La, Lb = best(loc, alld), best(loc, band); everywhere = np.ones(len(offs), bool); Ga, Gb = best(everywhere, alld), best(everywhere, band)
        res[f"local_{tag}"] = dict(any_duration=La, band_duration=Lb); res[f"global_{tag}"] = dict(any_duration=Ga, band_duration=Gb)
        if comparable(La, Lb) and abs(Lb["offset_min"]) <= gate + 1e-9: return "RECOVERED"
        # INCONSISTENT: the best consistent signal anywhere within +-0.3 d is comparable, has joint SNR >= 7 and lies > max(gate, 30 min)
        # from the predictions (per-event displaced dips are recorded for information only)
        if comparable(Ga, Gb) and Gb["snr"] >= 7.0 and abs(Gb["offset_min"]) > max(gate, 30.0): return "INCONSISTENT"   # look-elsewhere: SNR >= 7 over the +-0.3 d search
        # EXCLUDED (decision 2, DECISIONS item 78): (a) at D = ref, max over |o| <= gate of stacked depth + 3 err < 0.3 x ref (the timing
        # tolerance applies to EXCLUDED too); (b) per-event depths at the predicted times consistent (chi2 p >= 0.01); (c) no VALID fit with
        # SNR >= 5 and depth >= 0.5 x ref anywhere within +-0.3 d at any duration (a displaced real dip must not read EXCLUDED).
        gw = np.abs(offs) <= gate + 1e-9; ub = Sd[gw, j_ref] + 3 * Se[gw, j_ref]
        nfin = np.sum(np.isfinite(Dp[:, gw, j_ref]) & np.isfinite(Ep[:, gw, j_ref]), axis=0)   # events measured at each gate offset
        okw = np.isfinite(ub) & (nfin == len(el))                                                # every eligible event at EVERY offset (review R3)
        a_ok = bool(okw.all() and np.max(ub) < 0.3 * dep_ref)
        b_ok = bool(np.isfinite(Pc[i0, j_ref]) and Pc[i0, j_ref] >= 0.01)
        strong = (Sn >= 5.0) & (Sd >= 0.5 * dep_ref); c_ok = not bool(strong.any())
        res[f"excluded_diagnostics_{tag}"] = dict(max_depth_plus_3err_ppm=float(np.max(ub[okw]) * 1e6) if okw.any() else None, limit_ppm=0.3 * cfg["ref_depth_ppm"],
                                                 gate_window_all_finite=bool(okw.all()), min_events_measured_in_gate=int(nfin.min()), n_eligible=len(el),
                                                 events_measured_per_gate_offset=dict(offset_min=[float(x) for x in offs[gw]], n_events=[int(x) for x in nfin]), consistency_p_at_prediction=float(Pc[i0, j_ref]),
                                                 any_valid_fit_snr5_depth05=bool(strong.any()), a=a_ok, b=b_ok, c=c_ok)
        if a_ok and b_ok and c_ok: return "EXCLUDED"
        return "AMBIGUOUS"
    par = np.array([int(e["epoch"]) % 2 for e in el])
    def timing_split(gate, Lb):
        """Add-on (DECISIONS item 77): epoch-parity halves stacked at the joint duration over the local window; best offset per half."""
        jd = int(np.argmin(np.abs(durs - Lb["dur_h"] / 24))); loc = np.abs(offs) <= max(gate, 30.0) + dur * 1440 / 2 + 1e-9; out = {}
        for h in (0, 1):
            k = par == h
            if not k.any(): return dict(passed=False, reason=f"no eligible events with epoch parity {h}")
            Dh, Wh = Dp[k][:, :, jd], W[k][:, :, jd]; okh = np.all(np.isfinite(Dh), axis=0) & loc
            if not okh.any(): return dict(passed=False, reason=f"half {h} has no finite local fit")
            sd = np.nansum(Dh * Wh, axis=0) / np.nansum(Wh, axis=0); se = 1 / np.sqrt(np.nansum(Wh, axis=0)); sn = np.where(okh, sd / se, -np.inf); io = int(np.argmax(sn))
            out[f"parity{h}"] = dict(n=int(k.sum()), best_offset_min=float(offs[io]), snr=float(sn[io]))
        out["passed"] = bool(all(abs(out[f"parity{h}"]["best_offset_min"]) <= gate + 1e-9 for h in (0, 1))); return out
    res["n_eligible"] = len(el); res["outcome"] = outcome(gate_max, "max"); res["outcome_min_gate_reading"] = outcome(gate_min, "min")
    for tag, g in (("max", gate_max), ("min", gate_min)):
        oc = res["outcome"] if tag == "max" else res["outcome_min_gate_reading"]
        sp = timing_split(g, res[f"local_{tag}"]["band_duration"]) if oc == "RECOVERED" else None
        res[f"timing_split_{tag}"] = sp; res["outcome_with_split" if tag == "max" else "outcome_min_gate_with_split"] = oc if (sp is None or sp["passed"]) else "AMBIGUOUS"
    # the timing-split check is part of the outcome of record (author decision 2026-10-20, DECISIONS item 82); joint-only outcomes kept as readouts
    res["outcome_joint_only"], res["outcome_min_gate_joint_only"] = res["outcome"], res["outcome_min_gate_reading"]
    res["outcome"], res["outcome_min_gate_reading"] = res["outcome_with_split"], res["outcome_min_gate_with_split"]
    # odd/even depth diagnostic at the joint (local, max-gate) band-duration fit; information only (a half-period EB is not excluded by RECOVERED)
    Lb = res["local_max"]["band_duration"]
    if Lb:
        io, jd = int(np.argmin(np.abs(offs - Lb["offset_min"]))), int(np.argmin(np.abs(durs - Lb["dur_h"] / 24))); oe = {}
        for h in (0, 1):
            k = par == h
            if k.any():
                w = W[k][:, io, jd]; dd = Dp[k][:, io, jd]; oe[f"parity{h}"] = dict(n=int(k.sum()), depth_ppm=float(np.nansum(dd * w) / np.nansum(w) * 1e6), err_ppm=float(1 / np.sqrt(np.nansum(w)) * 1e6))
        if len(oe) == 2: oe["diff_sigma"] = float((oe["parity0"]["depth_ppm"] - oe["parity1"]["depth_ppm"]) / np.hypot(oe["parity0"]["err_ppm"], oe["parity1"]["err_ppm"]))
        res["odd_even_diagnostic"] = oe
    res["joint"] = res["local_max"]["band_duration"]
    return finish(override(res, strict, el, cfg), a)

def override(res, strict, el, cfg):
    """Apply the object-specific stricter clause deterministically (review R6): if any listed epoch has a gap or flagged cadences
    (strict_epoch_check) or is not eligible under this procedure, the outcome of record and the min() reading become INSUFFICIENT; the
    procedure's own outcome is kept as outcome_before_override."""
    if not cfg.get("strict_epochs") or strict is None: return res
    elig = {int(e["epoch"]) for e in el}; bad = [str(ep) for ep in cfg["strict_epochs"] if strict.get(str(ep), {}).get("violated") or int(ep) not in elig]
    res["object_specific_override"] = dict(strict_epochs=cfg["strict_epochs"], triggered=bool(bad), epochs=bad)
    if bad:
        res["outcome_before_override"] = res["outcome"]; res["outcome"] = res["outcome_min_gate_reading"] = "INSUFFICIENT"
    return res

def finish(res, a):
    s = json.dumps(res, indent=1, default=float); print(s if len(s) < 4000 else json.dumps({k: res[k] for k in res if k not in ("events", "config")}, indent=1, default=float))
    if a.out: open(a.out, "w").write(s)
    return res

if __name__ == "__main__": main()
