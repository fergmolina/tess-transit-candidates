"""Vetting toolkit for a transit candidate on a TESS 2-min target.
Usage: python -I vet.py TIC PERIOD T0 DUR_H [--label name]
Steps: masked re-detrend, TLS refinement (narrow window), per-sector/per-year depth, odd/even, secondary scan,
individual transit timing (O-C), blind-year prediction test, batman shape fit, SAP vs PDCSAP, Gaia neighbours,
difference-image centroid, stellar-density check, planet parameters, future transit predictions.
Outputs results/vet/<TIC>/report.json + figures.
"""
import sys, os, json, glob, re, warnings, argparse
sys.path.insert(0, "/Users/fernando/Desktop/NASA/scripts")
warnings.filterwarnings("ignore")
import numpy as np, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from scipy.optimize import least_squares, minimize
from tsearch import load_spoc_lc, trim_edges
from time_utils import geocentric_utc
from search_pipeline import sector_files, year_of, bin_lc, load_lc, SOURCE
import batman

def masked_detrend(t, f, P, T0, dur_d, window=0.75):
    from wotan import flatten, transit_mask
    mask = transit_mask(time=t, period=P, duration=2.0 * dur_d, T0=T0)
    flat, trend = flatten(t, f, method="biweight", window_length=window, return_trend=True, break_tolerance=0.5, mask=mask)
    ok = np.isfinite(flat) & trim_edges(t)
    oot = ok & ~mask
    mad = np.nanmedian(np.abs(flat[oot] - np.nanmedian(flat[oot]))) * 1.4826
    ok &= flat < 1 + 5 * mad
    return flat, ok, trend

MASK_KNOWN = None  # (P, T0, dur_d) of a known signal to remove
def load_all(tic, P, T0, dur_d, flux_col="PDCSAP_FLUX"):
    secs = {}
    for fp in sector_files(tic):
        if SOURCE == "spoc": t, f, fe, m = load_spoc_lc(fp, flux_col=flux_col)
        else:
            from tsearch import load_qlp_lc
            t, f, fe, m = load_qlp_lc(fp, flux_col=("SAP_FLUX" if flux_col == "SAP_FLUX" else "DET_FLUX"))
        if len(t) < 1000 and (t.max() - t.min()) < 10: continue   # cadence-aware (review: a 1800-s sector has ~1,100 points and was dropped)
        if str(m["sector"]) in os.environ.get("EXCLUDE_SECTORS", "").split(","): print(f"  excluding sector {m['sector']} (EXCLUDE_SECTORS)"); continue
        flat, ok, _ = masked_detrend(t, f, P, T0, dur_d)
        if MASK_KNOWN is not None:
            from wotan import transit_mask
            ok &= ~transit_mask(time=t, period=MASK_KNOWN[0], duration=1.5 * MASK_KNOWN[2], T0=MASK_KNOWN[1])
        secs[m["sector"]] = dict(t=t[ok], f=flat[ok], fe=fe[ok], meta=m)
    return secs

def stitch(secs):
    T = np.concatenate([v["t"] for v in secs.values()]); F = np.concatenate([v["f"] for v in secs.values()]); E = np.concatenate([v["fe"] for v in secs.values()])
    o = np.argsort(T); return T[o], F[o], E[o]

def box_depth(t, f, P, T0, dur_d, phase=0.0):
    ph = ((t - T0) / P - phase + 0.5) % 1 - 0.5
    intr = np.abs(ph * P) < dur_d / 2
    oot = (np.abs(ph * P) > dur_d) & (np.abs(ph * P) < 3 * dur_d)
    if intr.sum() < 3: return np.nan, np.nan, int(intr.sum())
    d = np.median(f[oot]) - np.mean(f[intr]) if oot.sum() > 10 else 1 - np.mean(f[intr])
    sig = np.std(f[oot]) if oot.sum() > 10 else np.std(f)
    return float(d), float(sig / np.sqrt(intr.sum())), int(intr.sum())

def per_point_exposure(t, half=5, gap_d=0.1):
    """Per-cadence exposure (days) from UNFOLDED time stamps (v1.12-1, full-repo re-check N3). The series is split into segments at
    gaps > gap_d (so sectors/cadences are not mixed); within a segment each point gets the median spacing over +-half neighbouring
    cadences (robust to single missing cadences), snapped to 120/200/600/1800 s when within 20 %. Compute on the full series, then subset."""
    t = np.asarray(t, float); n = len(t)
    if n < 2: return np.full(n, 120 / 86400)
    o = np.argsort(t); ts = t[o]; e = np.empty(n); cut = np.r_[0, np.where(np.diff(ts) > gap_d)[0] + 1, n]
    for a, b in zip(cut[:-1], cut[1:]):
        seg = ts[a:b]
        if len(seg) < 3: e[a:b] = np.median(np.diff(ts[max(0, a - 1):b + 1])) if b - a >= 1 else 120 / 86400; continue
        d = np.diff(seg); pad = np.r_[np.full(half, np.nan), d, np.full(half, np.nan)]
        e[a:b] = np.nanmedian(np.lib.stride_tricks.sliding_window_view(pad, 2 * half), axis=1)
    for c in (120, 200, 600, 1800):
        near = np.abs(e * 86400 / c - 1) < 0.2; e[near] = c / 86400
    out = np.empty(n); out[o] = e; return out

def transit_model(params, t, P, u=(0.4, 0.25), exp_time=None):
    """batman model. exp_time: scalar (days), or a per-point array (evaluated per cadence group). If None, it is inferred from t, which is
    valid ONLY for unfolded time stamps; callers passing folded or phase times must supply exp_time (v1.12, review F3)."""
    T0, rprs, ars, b = params
    if exp_time is None: exp_time = float(np.median(np.diff(np.sort(t)))) if len(t) > 3 else 120 / 86400   # real cadence (review 2026-10-18: 120 s was hard-coded for 200/600/1800-s QLP data)
    inc = np.degrees(np.arccos(np.clip(b / ars, 0, 1)))
    p = batman.TransitParams(); p.t0 = T0; p.per = P; p.rp = rprs; p.a = ars; p.inc = inc; p.ecc = 0; p.w = 90; p.u = list(u); p.limb_dark = "quadratic"
    if np.ndim(exp_time) == 0:
        return batman.TransitModel(p, t, supersample_factor=3, exp_time=float(exp_time)).light_curve(p)
    exp_time = np.asarray(exp_time, float); out = np.empty(len(t))
    for ex in np.unique(np.round(exp_time * 86400)):
        s = np.round(exp_time * 86400) == ex
        out[s] = batman.TransitModel(p, t[s], supersample_factor=max(3, int(round(ex / 120))), exp_time=ex / 86400).light_curve(p)
    return out

def fit_shape(t, f, fe, P, T0, dur_d, depth, ars_guess):
    # work only near transits for speed
    ph = ((t - T0) / P + 0.5) % 1 - 0.5
    near = np.abs(ph * P) < 3 * dur_d
    tt, ff, ee = t[near], f[near], fe[near]; ex = per_point_exposure(t)[near]   # per-point exposures (re-check N3)
    x0 = [T0, float(np.clip(np.sqrt(max(depth, 1e-6)), 0.0015, 0.45)), float(np.clip(ars_guess, 2.0, 400.0)), 0.3]
    lo = [T0 - 0.1, 0.001, 1.5, 0.0]; hi = [T0 + 0.1, 0.5, 500, 1.2]
    def resid(x): return (ff - transit_model(x, tt, P, exp_time=ex)) / ee
    r = least_squares(resid, x0, bounds=(lo, hi), x_scale=[0.001, 0.01, 1, 0.1])
    chi2 = np.sum(r.fun**2); dof = len(ff) - 4
    # box/null comparison
    chi2_null = np.sum(((ff - 1) / ee)**2)
    try:
        J = r.jac; cov = np.linalg.inv(J.T @ J) * max(1, chi2 / dof); err = np.sqrt(np.diag(cov))
    except Exception: err = [np.nan] * 4
    return dict(T0=r.x[0], rprs=r.x[1], ars=r.x[2], b=r.x[3], err=[float(e) for e in err], chi2=float(chi2), dof=int(dof),
                dchi2_vs_flat=float(chi2_null - chi2), n_pts=int(len(ff)))

def mcmc_shape(t, f, fe, P, T0, dur_d, x_best, nwalk=32, nsteps=1500):
    import emcee
    ph = ((t - T0) / P + 0.5) % 1 - 0.5
    near = np.abs(ph * P) < 3 * dur_d
    tt, ff, ee = t[near], f[near], fe[near]; ex = per_point_exposure(t)[near]   # per-point exposures (re-check N3)
    def lnp(x):
        T0_, rprs, ars, b = x
        if not (0.0005 < rprs < 0.5 and 1.5 < ars < 500 and 0 <= b < 1 + rprs and abs(T0_ - T0) < 0.1): return -np.inf
        m = transit_model(x, tt, P, exp_time=ex)
        return -0.5 * np.sum(((ff - m) / ee)**2)
    p0 = np.array(x_best) + 1e-4 * np.random.randn(nwalk, 4); p0[:, 3] = np.abs(p0[:, 3])
    s = emcee.EnsembleSampler(nwalk, 4, lnp); s.run_mcmc(p0, nsteps, progress=False)
    ch = s.get_chain(discard=nsteps // 3, flat=True)
    q = np.percentile(ch, [16, 50, 84], axis=0)
    return dict(names=["T0", "rprs", "ars", "b"], median=q[1].tolist(), lo=(q[1] - q[0]).tolist(), hi=(q[2] - q[1]).tolist(), acc=float(np.mean(s.acceptance_fraction)))

def global_ephemeris(T, F, E, P, T0, dur_d, rprs, ars, b, dP_frac=0.002, nP=161, nT0=81):
    """Joint (P, T0) fit of a fixed-shape batman model to ALL data near transit (works for shallow signals where individual
    transits cannot be timed). Chi2 surface on a grid; 1-sigma from delta-chi2=1 profiles, inflated by sqrt(reduced chi2)."""
    ph = ((T - T0) / P + 0.5) % 1 - 0.5; near = np.abs(ph * P) < 2.5 * dur_d
    tt, ff, ee = T[near], F[near], E[near]; ex = per_point_exposure(T)[near]   # exposures from the full UNFOLDED series (v1.12 F3, re-check N3)
    Ps = P * (1 + np.linspace(-dP_frac, dP_frac, nP)); T0s = T0 + np.linspace(-0.6, 0.6, nT0) * dur_d
    chi = np.full((nP, nT0), np.inf)
    for i, Pi in enumerate(Ps):
        for j, T0j in enumerate(T0s):
            m = transit_model([T0j, rprs, ars, b], tt, Pi) if False else None
            # fast: fold at (Pi, T0j) and evaluate the model once per phase (model depends on phase only)
            phi = ((tt - T0j) / Pi + 0.5) % 1 - 0.5
            mod = transit_model([0.0, rprs, ars, b], phi * Pi, Pi, exp_time=ex)
            chi[i, j] = np.sum(((ff - mod) / ee)**2)
    i0, j0 = np.unravel_index(np.argmin(chi), chi.shape)
    cmin = chi[i0, j0]; dof = len(ff) - 2; infl = max(1.0, cmin / dof)
    prof_P = chi.min(axis=1); prof_T = chi.min(axis=0)
    okP = prof_P <= cmin + infl; okT = prof_T <= cmin + infl
    P_err = max((Ps[okP].max() - Ps[okP].min()) / 2, np.diff(Ps)[0] / 2); T0_err = max((T0s[okT].max() - T0s[okT].min()) / 2, np.diff(T0s)[0] / 2)
    chi_flat = np.sum(((ff - 1) / ee)**2)
    edge = bool(i0 in (0, nP - 1) or j0 in (0, nT0 - 1))
    return dict(P=float(Ps[i0]), P_err=float(P_err), T0=float(T0s[j0]), T0_err=float(T0_err), cov=[[T0_err**2, 0.0], [0.0, P_err**2]],
                chi2=float(cmin), dof=int(dof), dchi2_vs_flat=float(chi_flat - cmin), error_inflation=float(np.sqrt(infl)), hit_grid_edge=edge, n_pts=int(len(ff)))

def time_transits(T, F, E, P, T0, dur_d, rprs, ars, b, min_pts=15):
    """Fit each individual transit's mid-time with the fixed shape model; return list of (epoch, tc, err, depth_snr)."""
    out = []; EXP_T = per_point_exposure(T)   # per-point exposures from the full series (re-check N3)
    n0 = int(np.floor((T.min() - T0) / P)); n1 = int(np.ceil((T.max() - T0) / P))
    for n in range(n0, n1 + 1):
        tc0 = T0 + n * P
        w = np.abs(T - tc0) < 2.5 * dur_d
        intr = np.abs(T - tc0) < dur_d / 2
        cad = float(np.median(np.diff(T))) if len(T) > 3 else 120 / 86400; mp = max(4, min(min_pts, int(0.6 * dur_d / cad)))   # cadence-aware (review 2026-10-18: min_pts=15 dropped every 600/1800-s transit)
        if intr.sum() < mp or w.sum() < 3 * mp: continue
        tt, ff, ee = T[w], F[w], E[w]; exw = EXP_T[w]
        grid = tc0 + np.linspace(-0.6 * dur_d, 0.6 * dur_d, 121)
        chi = np.array([np.sum(((ff - transit_model([g, rprs, ars, b], tt, P, exp_time=exw)) / ee)**2) for g in grid])
        i = int(np.argmin(chi))
        # 1-sigma from delta chi2 = 1
        okk = chi < chi[i] + 1
        err = max((grid[okk].max() - grid[okk].min()) / 2, np.diff(grid)[0] / 2)
        chi_flat = np.sum(((ff - 1) / ee)**2)
        d, de, nin = box_depth(tt, ff, P, grid[i], dur_d)
        out.append(dict(epoch=n, tc=float(grid[i]), tc_err=float(err), oc_min=float((grid[i] - tc0) * 1440), dchi2=float(chi_flat - chi[i]),
                        depth=d, depth_err=de, n_in=nin, sector=None))
    return out

def linear_ephemeris(times):
    n = np.array([x["epoch"] for x in times]); tc = np.array([x["tc"] for x in times]); e = np.array([x["tc_err"] for x in times])
    W = 1 / e**2; A = np.vstack([np.ones_like(n), n]).T
    cov = np.linalg.inv(A.T @ (A * W[:, None])); coef = cov @ (A.T @ (W * tc))
    resid = tc - A @ coef; chi2 = np.sum(resid**2 * W); dof = len(n) - 2
    infl = max(1.0, chi2 / dof) if dof > 0 else 1.0   # inflate covariance when timing errors are underestimated (reduced chi2 > 1)
    cov = cov * infl
    return dict(T0=float(coef[0]), P=float(coef[1]), T0_err=float(np.sqrt(cov[0, 0])), P_err=float(np.sqrt(cov[1, 1])), cov=cov.tolist(),
                chi2=float(chi2), dof=int(dof), rms_oc_min=float(np.std(resid) * 1440), error_inflation=float(np.sqrt(infl)))

def blind_test(T, F, E, secs, P, T0, dur_d, rprs, ars, b, holdout_year):
    """Hold out one calendar year. On the remaining years ONLY: (1) run a fresh full BLS search (same grid machinery as the
    discovery pipeline) and check the candidate period is recovered; (2) fit shape + time transits + linear ephemeris from
    training data only; (3) predict the holdout transits and measure their depth vs a random-phase null."""
    from search_pipeline import period_grid, bls_stats, bin_lc
    yr = np.array([year_of(x) for x in T])
    train = yr != holdout_year; test = ~train
    if train.sum() < 1000 or test.sum() < 1000: return dict(ok=False, reason="holdout or training set too small")
    Tr, Fr, Er = T[train], F[train], E[train]
    # (1) independent search on training data
    durs = np.array([1.0, 1.5, 2.0, 3.0, 4.0]) / 24
    base = Tr.max() - Tr.min(); pmax = 20.0 if base > 60 else max(1.0, base / 2)
    pg = period_grid(base, 0.5, pmax, durs.min(), oversample=2.0)
    Tb, Fb, Eb = bin_lc(Tr, Fr, Er, 10 / 1440)
    peaks = bls_stats(Tb, Fb, Eb, pg, durs)
    rank = next((i for i, pk in enumerate(peaks) if any(abs(pk["period"] * k - P) / P < 0.01 for k in (1, 2, 0.5))), None)
    search = dict(top_peaks=[dict(period=pk["period"], sde=pk["sde"], snr=pk["snr"], depth_ppm=pk["depth"] * 1e6) for pk in peaks], rank_of_candidate=rank)
    if rank is None:
        return dict(ok=True, holdout_year=int(holdout_year), training_search=search, recovered_in_training=False, reason="candidate period not among top-3 BLS peaks of training-only data")
    pk = peaks[rank]; P_tr, T0_tr, dur_tr = pk["period"], pk["t0"], pk["duration_h"] / 24
    if abs(P_tr - P) / P > 0.01: P_tr = P_tr * (P / P_tr)  # alias: fold at candidate multiple
    # (2) training-only shape + timing + ephemeris
    try:
        fit = fit_shape(Tr, Fr, Er, P_tr, T0_tr, dur_tr, max(pk["depth"], 1e-6), float(np.clip(P_tr / (np.pi * dur_tr), 2, 400)))
        rprs_t, ars_t, b_t = fit["rprs"], fit["ars"], fit["b"]; shape_fallback = False
    except Exception: rprs_t, ars_t, b_t = rprs, ars, b; shape_fallback = True   # training fit failed: all-data shape used (recorded, v1.12 review F18)
    eph = global_ephemeris(Tr, Fr, Er, P_tr, T0_tr, dur_tr, rprs_t, ars_t, b_t)
    tt_train = [x for x in time_transits(Tr, Fr, Er, eph["P"], eph["T0"], dur_tr, rprs_t, ars_t, b_t) if x["dchi2"] > 4]
    # (3) predict holdout
    Tt, Ft, Et = T[test], F[test], E[test]
    n0 = int(np.floor((Tt.min() - eph["T0"]) / eph["P"])); n1 = int(np.ceil((Tt.max() - eph["T0"]) / eph["P"]))
    preds = []
    for n in range(n0, n1 + 1):
        tc = eph["T0"] + n * eph["P"]; terr = np.sqrt(eph["T0_err"]**2 + (n * eph["P_err"])**2)
        intr = np.abs(Tt - tc) < dur_tr / 2
        if intr.sum() < 10: continue
        loc = np.abs(Tt - tc) < 3.5 * dur_tr   # THIS event only (v1.12, review F4: box_depth on the whole holdout folds every event)
        d, de, nin = box_depth(Tt[loc], Ft[loc], eph["P"], tc, dur_tr)
        preds.append(dict(epoch=n, tc_pred=float(tc), tc_pred_err_min=float(terr * 1440), depth=d, depth_err=de, n_in=nin, snr=float(d / de) if de > 0 else np.nan))
    if not preds: return dict(ok=False, holdout_year=int(holdout_year), training_search=search, shape_fallback=shape_fallback, recovered_in_training=True, reason="no predicted transits covered in holdout")
    worst = max(p["tc_pred_err_min"] for p in preds)
    if worst > 0.5 * dur_tr * 1440:
        return dict(ok=False, holdout_year=int(holdout_year), training_search=search, shape_fallback=shape_fallback, recovered_in_training=True, train_ephemeris=eph, n_train_transits=len(tt_train), predicted=preds,
                    reason=f"training ephemeris too imprecise to predict holdout phase (1-sigma {worst:.0f} min > half duration); test inconclusive, not failed")
    d_stack, de_stack, nin = box_depth(Tt, Ft, eph["P"], eph["T0"], dur_tr)
    rng = np.random.default_rng(1)
    nulls = np.array([box_depth(Tt, Ft, eph["P"], eph["T0"] + eph["P"] * (0.1 + 0.8 * rng.random()), dur_tr)[0] for _ in range(1000)])
    nulls = nulls[np.isfinite(nulls)]
    pval = float(np.mean(nulls >= d_stack))
    return dict(ok=True, holdout_year=int(holdout_year), training_search=search, shape_fallback=shape_fallback, recovered_in_training=True, train_ephemeris=eph, n_train_transits=len(tt_train),
                predicted=preds, stacked_depth=d_stack, stacked_err=de_stack, stacked_snr=float(d_stack / de_stack) if de_stack > 0 else np.nan,
                null_p_value=pval, null_mean=float(np.mean(nulls)), null_std=float(np.std(nulls)), null_trials=int(len(nulls)),
                # phase scan in the holdout: where is the deepest box within +-3 h of the prediction (diagnoses small ephemeris misses)
                holdout_scan=[dict(offset_h=float(o * 24), depth=box_depth(Tt, Ft, eph["P"], eph["T0"] + o, dur_tr)[0]) for o in np.arange(-3, 3.01, 0.25) / 24])

def secondary_scan(T, F, E, P, T0, dur_d):
    phases = np.linspace(0.05, 0.95, 181); res = []
    for ph in phases:
        d, de, n = box_depth(T, F, P, T0, dur_d, phase=ph); res.append((ph, d, de))
    res = np.array(res); ok = np.isfinite(res[:, 1])
    snr = res[ok, 1] / res[ok, 2]; i = int(np.argmax(snr))
    at_half = box_depth(T, F, P, T0, dur_d, phase=0.5)
    return dict(best_phase=float(res[ok][i, 0]), best_depth=float(res[ok][i, 1]), best_snr=float(snr[i]),
                depth_at_0p5=at_half[0], err_at_0p5=at_half[1], snr_at_0p5=float(at_half[0] / at_half[1]) if at_half[1] > 0 else np.nan)

def gaia_neighbours(ra, dec, radius_arcsec=120, depth=None, tmag=None):
    from astroquery.gaia import Gaia
    from astropy.coordinates import SkyCoord; import astropy.units as u
    Gaia.ROW_LIMIT = 200
    job = Gaia.cone_search_async(SkyCoord(ra, dec, unit="deg"), radius=radius_arcsec * u.arcsec, table_name="gaiadr3.gaia_source")
    r = job.get_results().to_pandas()
    r = r.sort_values("dist")
    tgt = r.iloc[0]; out = []
    for _, s in r.iterrows():
        dG = s["phot_g_mean_mag"] - tgt["phot_g_mean_mag"]
        flux_ratio = 10 ** (-0.4 * dG)
        req = depth / flux_ratio if depth is not None else np.nan  # eclipse depth needed on neighbour to mimic signal (ignoring aperture fraction)
        out.append(dict(source_id=str(s["source_id"]), sep_arcsec=float(s["dist"] * 3600), G=float(s["phot_g_mean_mag"]), dG=float(dG),
                        bp_rp=float(s["bp_rp"]) if np.isfinite(s["bp_rp"]) else None, parallax=float(s["parallax"]) if np.isfinite(s["parallax"]) else None,
                        ruwe=float(s["ruwe"]) if "ruwe" in s and np.isfinite(s["ruwe"]) else None, required_depth_if_source=float(req) if np.isfinite(req) else None))
    return out

def centroid_shift(tic, P, T0, dur_d):
    """In-transit vs out-of-transit shift of the SPOC flux-weighted centroid (MOM_CENTR1/2), per sector, after detrending the centroid
    time series with the same masked biweight. A transit on the target gives ~zero shift; on a neighbour it gives a shift of order
    depth x separation. Bootstrap errors. (SPOC 2-min only.)"""
    from astropy.io import fits
    from wotan import flatten, transit_mask
    out = {}
    for fp in sector_files(tic):
        with fits.open(fp, memmap=False) as h:
            d = h[1].data; sec = int(h[0].header["SECTOR"])
            t = np.asarray(d["TIME"], float); q = np.asarray(d["QUALITY"], int)
            cx = np.asarray(d["MOM_CENTR1"], float); cy = np.asarray(d["MOM_CENTR2"], float); f = np.asarray(d["PDCSAP_FLUX"], float)
        m = np.isfinite(t) & np.isfinite(cx) & np.isfinite(cy) & np.isfinite(f) & (q == 0) & trim_edges(t)
        t, cx, cy = t[m], cx[m], cy[m]
        if len(t) < 1000 and (t.max() - t.min()) < 10: continue   # cadence-aware (review: a 1800-s sector has ~1,100 points and was dropped)
        mask = transit_mask(time=t, period=P, duration=2 * dur_d, T0=T0)
        res = {}
        for name, c in (("x", cx), ("y", cy)):
            tr = flatten(t, c - c.mean() + 10, method="biweight", window_length=0.75, return_trend=True, break_tolerance=0.5, mask=mask)[1]
            r = c - tr; ok = np.isfinite(r)
            ph = ((t - T0) / P + 0.5) % 1 - 0.5; intr = ok & (np.abs(ph * P) < dur_d / 2); oot = ok & (np.abs(ph * P) > dur_d) & (np.abs(ph * P) < 3 * dur_d)
            if intr.sum() < 10 or oot.sum() < 30: res = None; break
            shift = np.mean(r[intr]) - np.mean(r[oot]); err = np.sqrt(np.var(r[intr]) / intr.sum() + np.var(r[oot]) / oot.sum())
            res[name] = (float(shift), float(err), int(intr.sum()))
        if res: out[sec] = dict(dx_px=res["x"][0], dx_err=res["x"][1], dy_px=res["y"][0], dy_err=res["y"][1], n_in=res["x"][2],
                                shift_px=float(np.hypot(res["x"][0], res["y"][0])), shift_sigma=float(np.hypot(res["x"][0] / res["x"][1], res["y"][0] / res["y"][1])))
    if not out: return dict(ok=False, reason="no usable centroid data")
    # weighted mean shift over sectors
    wx = np.array([1 / v["dx_err"]**2 for v in out.values()]); wy = np.array([1 / v["dy_err"]**2 for v in out.values()])
    dx = np.sum([v["dx_px"] for v in out.values()] * wx) / wx.sum(); dy = np.sum([v["dy_px"] for v in out.values()] * wy) / wy.sum()
    ex, ey = 1 / np.sqrt(wx.sum()), 1 / np.sqrt(wy.sum())
    return dict(ok=True, per_sector=out, mean_dx_px=float(dx), mean_dx_err=float(ex), mean_dy_px=float(dy), mean_dy_err=float(ey),
                mean_shift_px=float(np.hypot(dx, dy)), mean_shift_sigma=float(np.hypot(dx / ex, dy / ey)), mean_shift_arcsec=float(np.hypot(dx, dy) * 21))

def pixel_depth_map(tic, sector, P, T0, dur_d, outpng):
    """Per-pixel transit depth from the 2-min TPF: each pixel light curve is masked-biweight detrended, then the in/out depth at the
    candidate ephemeris is measured. The flux-loss map (depth x pixel flux) should peak on the target's PSF if the signal is on target."""
    import lightkurve as lk
    from wotan import flatten, transit_mask
    sr = lk.search_targetpixelfile(f"TIC {tic}", sector=sector, author="SPOC", exptime=120)
    if len(sr) == 0: return dict(ok=False, reason="no TPF")
    tpf = sr[0].download(download_dir="/Users/fernando/Desktop/NASA/data/lk_cache", quality_bitmask="default")
    t = tpf.time.value; flux = tpf.flux.value.astype(float); ny, nx = flux.shape[1:]
    good = np.isfinite(t) & np.isfinite(flux).all(axis=(1, 2)) & trim_edges(t); t, flux = t[good], flux[good]
    mask = transit_mask(time=t, period=P, duration=2 * dur_d, T0=T0)
    ph = ((t - T0) / P + 0.5) % 1 - 0.5; intr = np.abs(ph * P) < dur_d / 2; oot = (np.abs(ph * P) > dur_d) & (np.abs(ph * P) < 3 * dur_d)
    depth = np.full((ny, nx), np.nan); derr = np.full((ny, nx), np.nan); mean_img = np.nanmean(flux, axis=0)
    ap = tpf.pipeline_mask
    from scipy.ndimage import binary_dilation
    reg = binary_dilation(ap, iterations=2)
    for j in range(ny):
        for i in range(nx):
            if not reg[j, i] or mean_img[j, i] <= 0: continue
            pl = flux[:, j, i] / mean_img[j, i]
            try: tr = flatten(t, pl, method="biweight", window_length=0.75, return_trend=True, break_tolerance=0.5, mask=mask)[1]
            except Exception: continue
            r = pl / tr; ok = np.isfinite(r)
            if (ok & intr).sum() < 10: continue
            depth[j, i] = np.median(r[ok & oot]) - np.mean(r[ok & intr]); derr[j, i] = np.std(r[ok & oot]) / np.sqrt((ok & intr).sum())
    loss = depth * mean_img  # e-/s lost per pixel
    yy, xx = np.mgrid[:ny, :nx]
    w = np.where(np.isfinite(loss) & (loss > 0), loss, 0); wf = np.where(reg, mean_img, 0)
    cx, cy = np.sum(w * xx) / w.sum(), np.sum(w * yy) / w.sum(); ox, oy = np.sum(wf * xx) / wf.sum(), np.sum(wf * yy) / wf.sum()
    # bootstrap the loss centroid using per-pixel errors
    rng = np.random.default_rng(0); cs = []
    for _ in range(200):
        l2 = (depth + rng.standard_normal(depth.shape) * derr) * mean_img; w2 = np.where(np.isfinite(l2) & (l2 > 0), l2, 0)
        if w2.sum() > 0: cs.append((np.sum(w2 * xx) / w2.sum(), np.sum(w2 * yy) / w2.sum()))
    cs = np.array(cs)
    # depth significance in aperture pixels: is the deepest pixel the brightest target pixel?
    try: px, py = tpf.wcs.all_world2pix([[tpf.ra, tpf.dec]], 0)[0]
    except Exception: px, py = np.nan, np.nan
    fig, ax = plt.subplots(1, 3, figsize=(12, 3.6))
    ax[0].imshow(mean_img, origin="lower"); ax[0].set_title("mean image")
    ax[1].imshow(np.where(np.isfinite(depth), depth * 1e6, np.nan), origin="lower", cmap="RdBu_r", vmin=-3e3, vmax=3e3); ax[1].set_title("per-pixel depth (ppm)")
    ax[2].imshow(np.where(np.isfinite(loss), loss, np.nan), origin="lower"); ax[2].set_title("flux-loss map (depth x flux)")
    for a_ in ax:
        a_.contour(ap, levels=[0.5], colors="w", linewidths=0.8); a_.plot(px, py, "r+", ms=12, mew=2); a_.plot(cx, cy, "cx", ms=10, mew=2); a_.plot(ox, oy, "m.", ms=8)
    fig.suptitle(f"TIC {tic} S{sector}: red + target (WCS), magenta . flux centroid, cyan x flux-loss centroid"); fig.tight_layout(); fig.savefig(outpng, dpi=120); plt.close(fig)
    return dict(ok=True, sector=sector, n_in=int(intr.sum()), target_px=[float(px), float(py)], flux_centroid=[float(ox), float(oy)], loss_centroid=[float(cx), float(cy)],
                loss_centroid_err=[float(cs[:, 0].std()), float(cs[:, 1].std())] if len(cs) else [np.nan, np.nan],
                offset_loss_vs_flux_px=float(np.hypot(cx - ox, cy - oy)), offset_loss_vs_flux_arcsec=float(np.hypot(cx - ox, cy - oy) * 21),
                offset_loss_vs_target_px=float(np.hypot(cx - px, cy - py)), offset_loss_vs_target_arcsec=float(np.hypot(cx - px, cy - py) * 21),
                offset_flux_vs_target_px=float(np.hypot(ox - px, oy - py)),
                calibration_note="known planet TIC 12421862 S96 gives loss-vs-target 0.46 px, loss-vs-flux 0.65 px (flux centroid pulled by neighbours)",
                depth_map_ppm=np.where(np.isfinite(depth), depth * 1e6, None).tolist(), png=outpng)

SECTOR_DAY0 = 2458324.5  # fallback only: S1 start 2018-07-25, ~27.4 d per sector
_ORBITS = None
def sector_orbits():
    """Official orbit windows per sector from tess.mit.edu TESS_orbit_times.csv (downloaded 2026-10-17); JD_UTC."""
    global _ORBITS
    if _ORBITS is None:
        import pandas as pd; from astropy.time import Time
        d = pd.read_csv("/Users/fernando/Desktop/NASA/catalogs/TESS_orbit_times.csv", comment="#")
        _ORBITS = {}
        for _, r in d.iterrows():
            _ORBITS.setdefault(int(r["Sector"]), []).append((Time(r["Start of Orbit"]).jd, Time(r["End of Orbit"]).jd))
    return _ORBITS
def sector_window_jd(sec):
    ob = sector_orbits().get(sec)
    if ob: return min(a for a, b in ob), max(b for a, b in ob)
    return SECTOR_DAY0 + 27.4 * (sec - 1), SECTOR_DAY0 + 27.4 * sec
def in_orbit(sec, jd):
    ob = sector_orbits().get(sec)
    return None if not ob else any(a <= jd <= b for a, b in ob)

def future_transits(ra, dec, T0, P, T0_err, P_err, cov, n_days=450):
    """Predicted mid-transit times (BJD_TDB) from now, with propagated ephemeris uncertainty; labelled with the upcoming TESS sector
    (tess-point) whose approximate window contains them."""
    from astropy.time import Time
    now_jd = Time.now().jd
    try:
        from tess_stars2px import tess_stars2px_function_entry
        r = tess_stars2px_function_entry(1, ra, dec); sectors = sorted({int(x) for x in r[3]})
    except Exception: sectors = []
    upcoming = [sc for sc in sectors if sector_window_jd(sc)[1] > now_jd]
    cov = np.array(cov); n0 = int(np.ceil((now_jd - 2457000 - T0) / P)); preds = []
    for n in range(n0, n0 + int(n_days / P) + 1):
        tc = T0 + n * P + 2457000; var = cov[0, 0] + 2 * n * cov[0, 1] + n * n * cov[1, 1]
        sec = next((sc for sc in upcoming if sector_window_jd(sc)[0] <= tc <= sector_window_jd(sc)[1]), None)
        preds.append(dict(epoch=n, tc_bjd_tdb=float(tc), utc=geocentric_utc(tc, ra, dec).iso[:16], sigma_min=float(np.sqrt(var) * 1440), tess_sector=sec,
                          in_science_orbit=in_orbit(sec, tc) if sec else None))
    return dict(now_jd=float(now_jd), tess_sectors_all=sectors, upcoming_sectors=upcoming, predictions=preds,
                note="sector/orbit windows from tess.mit.edu TESS_orbit_times.csv (sectors <= 111); later sectors approximated; in_science_orbit=False means the time falls in the perigee data gap")

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("tic", type=int); ap.add_argument("period", type=float); ap.add_argument("t0", type=float); ap.add_argument("dur_h", type=float)
    ap.add_argument("--holdout", type=int, default=0); ap.add_argument("--mask", type=str, default="", help="P,T0,dur_h of a known signal to mask out"); ap.add_argument("--no-mcmc", action="store_true"); ap.add_argument("--tls", action="store_true"); ap.add_argument("--no-pixels", action="store_true")
    a = ap.parse_args()
    tic, P, T0, dur_d = a.tic, a.period, a.t0, a.dur_h / 24
    global MASK_KNOWN
    if a.mask:
        mp, mt0, mdh = [float(x) for x in a.mask.split(",")]; MASK_KNOWN = (mp, mt0 - 2457000 if mt0 > 2457000 else mt0, mdh / 24); print(f"  masking known signal P={mp} T0={MASK_KNOWN[1]:.4f} dur={mdh} h", flush=True)
    OUT = f"/Users/fernando/Desktop/NASA/results/vet{os.environ.get('TSEARCH_SUFFIX', '' if SOURCE == 'spoc' else '_qlp')}/{tic}"; os.makedirs(OUT, exist_ok=True)
    rep = dict(tic=tic, input=dict(period=P, t0=T0, dur_h=a.dur_h))
    secs = load_all(tic, P, T0, dur_d); meta = next(iter(secs.values()))["meta"]; rep["meta"] = meta
    T, F, E = stitch(secs)
    print(f"TIC {tic}: sectors {sorted(secs)}  N={len(T)}  Tmag={meta['tmag']} Teff={meta['teff']} R*={meta['rad']} logg={meta['logg']}", flush=True)
    # 1. Fine-grid BLS refinement around the candidate period (durations 0.5-1.5x input); TLS optional (--tls) as an independent check
    from astropy.timeseries import BoxLeastSquares
    Tb, Fb, Eb = bin_lc(T, F, E, 4 / 1440)
    base = T.max() - T.min()
    pgrid = np.linspace(P * 0.995, P * 1.005, 4001); dgrid = dur_d * np.linspace(0.5, 1.5, 11)
    bls = BoxLeastSquares(Tb, Fb, dy=Eb); res = bls.power(pgrid, dgrid, objective="snr"); i = int(np.nanargmax(res.power))
    st = bls.compute_stats(res.period[i], res.duration[i], res.transit_time[i])
    rep["bls_refine"] = dict(period=float(res.period[i]), T0=float(res.transit_time[i]), duration_h=float(res.duration[i] * 24), depth_ppm=float(res.depth[i] * 1e6),
                             depth_err_ppm=float(res.depth_err[i] * 1e6), snr=float(res.power[i]), n_transits=int(np.sum(st["per_transit_count"] > 0)),
                             depth_odd_ppm=float(st["depth_odd"][0] * 1e6), depth_even_ppm=float(st["depth_even"][0] * 1e6), depth_phased_ppm=float(st["depth_phased"][0] * 1e6))
    P, T0, dur_d = rep["bls_refine"]["period"], rep["bls_refine"]["T0"], rep["bls_refine"]["duration_h"] / 24
    print(f"  BLS refine: P={P:.6f} T0={T0:.5f} depth={rep['bls_refine']['depth_ppm']:.0f}+-{rep['bls_refine']['depth_err_ppm']:.0f}ppm dur={dur_d*24:.2f}h SNR={rep['bls_refine']['snr']:.1f} Ntr={rep['bls_refine']['n_transits']}", flush=True)
    rep["tls"] = dict(depth_ppm=rep["bls_refine"]["depth_ppm"])
    if a.tls:
        from transitleastsquares import transitleastsquares
        R_star = meta["rad"] or 0.7; M_star = max(0.1, min(1.5, R_star)) if meta["rad"] else 0.7
        Tb, Fb, Eb = bin_lc(T, F, E, 10 / 1440)
        r = transitleastsquares(Tb, Fb, Eb).power(period_min=P * 0.98, period_max=P * 1.02, oversampling_factor=5, duration_grid_step=1.05, R_star=R_star, M_star=M_star,
                                                   R_star_min=0.1, R_star_max=2.0, M_star_min=0.08, M_star_max=2.0, use_threads=1, show_progress_bar=False)
        rep["tls"].update(dict(period=float(r.period), period_err=float(r.period_uncertainty), T0=float(r.T0), tls_depth_ppm=float((1 - r.depth) * 1e6), duration_h=float(r.duration * 24),
                               SDE=float(r.SDE), snr=float(r.snr), odd_even_mismatch=float(r.odd_even_mismatch), distinct=int(r.distinct_transit_count)))
        print(f"  TLS (narrow window): P={r.period:.6f}+-{r.period_uncertainty:.6f} T0={r.T0:.5f} depth={(1-r.depth)*1e6:.0f}ppm dur={r.duration*24:.2f}h SDE={r.SDE:.1f} SNR={r.snr:.1f} Ntr={r.distinct_transit_count}", flush=True)
    # re-detrend with refined ephemeris
    secs = load_all(tic, P, T0, dur_d); T, F, E = stitch(secs)
    # 1b. inverted-light-curve null: same stitched BLS on 2-F (dips -> bumps). Real transits vanish; systematics/noise floor stay.
    from search_pipeline import period_grid, bls_stats
    durs = np.array([1.0, 1.5, 2.0, 3.0, 4.0]) / 24
    base = T.max() - T.min(); pg = period_grid(base, 0.5, 20.0 if base > 60 else max(1.0, base / 2), durs.min(), oversample=2.0)
    Tb, Fb, Eb = bin_lc(T, F, E, 10 / 1440)
    real_pk = bls_stats(Tb, Fb, Eb, pg, durs)[0]; inv_pk = bls_stats(Tb, 2 - Fb, Eb, pg, durs)[0]
    rep["inverted_null"] = dict(real_top=dict(period=real_pk["period"], sde=real_pk["sde"], snr=real_pk["snr"]), inverted_top=dict(period=inv_pk["period"], sde=inv_pk["sde"], snr=inv_pk["snr"]),
                                sde_margin=float(real_pk["sde"] - inv_pk["sde"]))
    print(f"  stitched BLS on masked-detrended data: top P={real_pk['period']:.5f} SDE={real_pk['sde']:.1f}; INVERTED top P={inv_pk['period']:.4f} SDE={inv_pk['sde']:.1f} -> margin {real_pk['sde']-inv_pk['sde']:.1f}", flush=True)
    # 2. per-sector & per-year depth
    rep["per_sector"] = {}; rep["per_year"] = {}
    for s, v in secs.items():
        d, de, n = box_depth(v["t"], v["f"], P, T0, dur_d)
        rep["per_sector"][s] = dict(depth_ppm=d * 1e6, err_ppm=de * 1e6, snr=d / de if de > 0 else np.nan, n_in=n, year=year_of(v["t"].mean()), rms_ppm=float(np.std(v["f"]) * 1e6), crowdsap=v["meta"]["crowdsap"])
    yrs = np.array([year_of(x) for x in T])
    for y in sorted(set(yrs)):
        d, de, n = box_depth(T[yrs == y], F[yrs == y], P, T0, dur_d); rep["per_year"][int(y)] = dict(depth_ppm=d * 1e6, err_ppm=de * 1e6, snr=d / de if de > 0 else np.nan, n_in=n)
    print("  per-year depth:", {y: f"{v['depth_ppm']:.0f}+-{v['err_ppm']:.0f} (SNR {v['snr']:.1f})" for y, v in rep["per_year"].items()}, flush=True)
    print("  per-sector:", {s: f"{v['depth_ppm']:.0f}+-{v['err_ppm']:.0f}" for s, v in rep["per_sector"].items()}, flush=True)
    # 3. odd/even and secondary
    ph = ((T - T0) / P + 0.5) % 1 - 0.5; ep = np.round((T - T0) / P).astype(int)
    do = box_depth(T[ep % 2 == 1], F[ep % 2 == 1], P, T0, dur_d); de_ = box_depth(T[ep % 2 == 0], F[ep % 2 == 0], P, T0, dur_d)
    rep["odd_even"] = dict(odd_ppm=do[0] * 1e6, odd_err=do[1] * 1e6, even_ppm=de_[0] * 1e6, even_err=de_[1] * 1e6, sigma=float(abs(do[0] - de_[0]) / np.hypot(do[1], de_[1])))
    rep["secondary"] = secondary_scan(T, F, E, P, T0, dur_d)
    print(f"  odd {do[0]*1e6:.0f}+-{do[1]*1e6:.0f}  even {de_[0]*1e6:.0f}+-{de_[1]*1e6:.0f}  ({rep['odd_even']['sigma']:.1f} sigma); secondary @0.5: {rep['secondary']['depth_at_0p5']*1e6:.0f}+-{rep['secondary']['err_at_0p5']*1e6:.0f} ppm; best other phase {rep['secondary']['best_phase']:.2f} SNR {rep['secondary']['best_snr']:.1f}", flush=True)
    # 4. shape fit
    depth = rep["tls"]["depth_ppm"] * 1e-6 if rep["tls"].get("depth_ppm") else max(1e-6, box_depth(T, F, P, T0, dur_d)[0])
    # a/R* guess from duration: dur ~ P/(pi a/R*) for b=0
    ars_guess = float(np.clip(P / (np.pi * dur_d), 2.0, 400.0))
    fit = fit_shape(T, F, E, P, T0, dur_d, depth, ars_guess); rep["shape_fit"] = fit
    print(f"  batman LSQ: rp/rs={fit['rprs']:.4f}+-{fit['err'][1]:.4f} a/R*={fit['ars']:.1f}+-{fit['err'][2]:.1f} b={fit['b']:.2f}+-{fit['err'][3]:.2f}  dchi2 vs flat={fit['dchi2_vs_flat']:.1f} (N={fit['n_pts']})", flush=True)
    if not a.no_mcmc:
        mc = mcmc_shape(T, F, E, P, T0, dur_d, [fit["T0"], fit["rprs"], fit["ars"], fit["b"]]); rep["shape_mcmc"] = mc
        print(f"  MCMC: " + ", ".join(f"{n}={m:.4f}+{h:.4f}-{l:.4f}" for n, m, l, h in zip(mc["names"], mc["median"], mc["lo"], mc["hi"])), flush=True)
        rprs, ars, b = mc["median"][1], mc["median"][2], mc["median"][3]
    else: rprs, ars, b = fit["rprs"], fit["ars"], fit["b"]
    # stellar density from fit vs TIC
    G = 6.674e-11; rho_fit = 3 * np.pi * ars**3 / (G * (P * 86400)**2) / 1408.0  # solar units
    rho_tic = (10**meta["logg"] / 10**4.438) / (meta["rad"]) if (meta["logg"] and meta["rad"]) else None  # M/R^3 = g/R * (1/R^2)... g ∝ M/R^2 -> M = g R^2; rho ∝ M/R^3 = g/R
    rep["density_check"] = dict(rho_star_fit_solar=float(rho_fit), rho_star_tic_solar=float(rho_tic) if rho_tic else None)
    print(f"  stellar density: fit {rho_fit:.2f} rho_sun vs TIC {rho_tic if rho_tic is None else round(rho_tic,2)} rho_sun", flush=True)
    # 5. individual transit times + linear ephemeris
    times = time_transits(T, F, E, P, T0, dur_d, rprs, ars, b)
    for x in times:
        for s, v in secs.items():
            if v["t"].min() - 1 < x["tc"] < v["t"].max() + 1: x["sector"] = s
    good = [x for x in times if x["dchi2"] > 4]
    rep["transit_times"] = times
    if len(good) >= 3:
        lin = linear_ephemeris(good); rep["ephemeris_linear"] = lin
        print(f"  {len(times)} transits timed, {len(good)} with dchi2>4; linear ephemeris P={lin['P']:.6f}+-{lin['P_err']:.6f} T0={lin['T0']:.5f}+-{lin['T0_err']:.5f} chi2/dof={lin['chi2']:.1f}/{lin['dof']} O-C rms={lin['rms_oc_min']:.1f} min (errors x{lin['error_inflation']:.1f})", flush=True)
    eph = global_ephemeris(T, F, E, P, T0, dur_d, rprs, ars, b); rep["ephemeris"] = eph
    print(f"  GLOBAL ephemeris fit: P={eph['P']:.6f}+-{eph['P_err']:.6f} T0={eph['T0']:.5f}+-{eph['T0_err']:.5f} (dchi2 vs flat {eph['dchi2_vs_flat']:.1f}, errors x{eph['error_inflation']:.1f}{', HIT GRID EDGE' if eph['hit_grid_edge'] else ''})", flush=True)
    # 6. blind test(s): hold out each year that has transits
    rep["blind_tests"] = {}
    for y in sorted(rep["per_year"]):
        bt = blind_test(T, F, E, secs, P, T0, dur_d, rprs, ars, b, y); rep["blind_tests"][int(y)] = bt
        if bt.get("ok") and "predicted" in bt:
            sc = bt["holdout_scan"]; ib = int(np.nanargmax([q["depth"] for q in sc]))
            print(f"  BLIND holdout {y}: training-only BLS rank={bt['training_search']['rank_of_candidate']} (top SDE {bt['training_search']['top_peaks'][0]['sde']:.1f}); train eph P={bt['train_ephemeris']['P']:.6f}+-{bt['train_ephemeris']['P_err']:.6f}; predicted {len(bt['predicted'])} transits (1-sigma {max(q['tc_pred_err_min'] for q in bt['predicted']):.0f} min); stacked depth at predicted phase {bt['stacked_depth']*1e6:.0f}+-{bt['stacked_err']*1e6:.0f} ppm (SNR {bt['stacked_snr']:.1f}); null p={bt['null_p_value']:.4f}; deepest within +-3h: {sc[ib]['depth']*1e6:.0f} ppm at {sc[ib]['offset_h']:+.2f} h", flush=True)
        else: print(f"  BLIND holdout {y}: {bt.get('reason')} | training top peaks: {[(round(q['period'],4), round(q['sde'],1)) for q in bt.get('training_search', {}).get('top_peaks', [])]}", flush=True)
    # 7. SAP vs PDCSAP
    try:
        secs_sap = load_all(tic, P, T0, dur_d, flux_col="SAP_FLUX"); Ts, Fs, Es = stitch(secs_sap)
        ds = box_depth(Ts, Fs, P, T0, dur_d); rep["sap_depth"] = dict(depth_ppm=ds[0] * 1e6, err_ppm=ds[1] * 1e6)
        print(f"  SAP depth {ds[0]*1e6:.0f}+-{ds[1]*1e6:.0f} ppm vs PDCSAP {depth*1e6:.0f}", flush=True)
    except Exception as e: rep["sap_depth"] = dict(error=str(e))
    # 8. Gaia neighbours
    try:
        rep["gaia_neighbours"] = gaia_neighbours(meta["ra"], meta["dec"], 120, depth=depth)
        nb = [g for g in rep["gaia_neighbours"] if g["sep_arcsec"] > 1]
        print(f"  Gaia DR3 neighbours within 2': {len(nb)}; capable (required eclipse depth <= 1): {sum(1 for g in nb if g['required_depth_if_source'] is not None and g['required_depth_if_source'] <= 1)}", flush=True)
    except Exception as e: rep["gaia_neighbours"] = dict(error=str(e)); print("  Gaia query failed:", e)
    # 9. centroid-shift test (SPOC only) and per-pixel depth map on the sector with the strongest per-sector depth SNR
    if SOURCE == "spoc":
        try:
            cs = centroid_shift(tic, P, T0, dur_d); rep["centroid_shift"] = cs
            if cs.get("ok"): print(f"  centroid shift (in - out): dx={cs['mean_dx_px']*1000:.1f}+-{cs['mean_dx_err']*1000:.1f} mpx dy={cs['mean_dy_px']*1000:.1f}+-{cs['mean_dy_err']*1000:.1f} mpx -> {cs['mean_shift_px']*21:.2f}\" ({cs['mean_shift_sigma']:.1f} sigma)", flush=True)
        except Exception as e: rep["centroid_shift"] = dict(error=str(e)); print("  centroid shift failed:", e)
    if not a.no_pixels and SOURCE == "spoc":
        try:
            best_s = max(rep["per_sector"], key=lambda s_: rep["per_sector"][s_]["snr"] if np.isfinite(rep["per_sector"][s_]["snr"]) else -1)
            pm = pixel_depth_map(tic, best_s, P, T0, dur_d, f"{OUT}/pixelmap_S{best_s}.png"); rep["pixel_depth_map"] = pm
            if pm.get("ok"): print(f"  pixel map S{best_s}: flux-loss centroid offset from TARGET {pm['offset_loss_vs_target_px']:.2f} px ({pm['offset_loss_vs_target_arcsec']:.0f}\"), from flux centroid {pm['offset_loss_vs_flux_px']:.2f} px; bootstrap +-({pm['loss_centroid_err'][0]:.2f},{pm['loss_centroid_err'][1]:.2f}) px [known-planet reference: 0.46 px]", flush=True)
        except Exception as e: rep["pixel_depth_map"] = dict(error=str(e)); print("  pixel map failed:", e)
    # 10. planet parameters
    Rs = meta["rad"]; Teff = meta["teff"]
    if Rs and Teff:
        Rp_re = rprs * Rs * 109.2; Teq = Teff * np.sqrt(1 / (2 * ars))  # albedo 0, full redistribution
        a_au = ars * Rs * 0.00465; insol = (Rs**2 * (Teff / 5772)**4) / a_au**2
        rep["planet"] = dict(Rp_Rearth=float(Rp_re), Teq_K=float(Teq), a_AU=float(a_au), insolation_Earth=float(insol), note=("dilution not corrected beyond PDCSAP CROWDSAP; albedo 0" if SOURCE == "spoc" else "QLP DET_FLUX depth may be biased low (QLP spline without transit mask); compare sap_depth; dilution per QLP aperture not corrected; albedo 0"))
        print(f"  planet (if on target): Rp={Rp_re:.2f} Re  Teq={Teq:.0f} K  a={a_au:.4f} AU  S={insol:.1f} S_earth", flush=True)
    # 11. future predictions
    if eph:
        rep["future"] = future_transits(meta["ra"], meta["dec"], eph["T0"], eph["P"], eph["T0_err"], eph["P_err"], eph["cov"], n_days=450)
        cov_preds = [p for p in rep["future"]["predictions"] if p["tess_sector"]]
        print(f"  tess-point sectors: {rep['future']['tess_sectors_all']} upcoming: {rep['future']['upcoming_sectors']}; predictions in upcoming sectors: {len(cov_preds)}; first:", [(p['tess_sector'], p['utc'], round(p['sigma_min'], 1)) for p in cov_preds[:3]], flush=True)
    # figures
    fig, ax = plt.subplots(2, 2, figsize=(13, 8))
    ph = ((T - T0) / P + 0.5) % 1 - 0.5
    ax[0, 0].plot(ph * P * 24, F, ".", ms=1, alpha=0.3, color="0.6")
    pb, fb_, eb_ = bin_lc(ph * P * 24 + 1000, F, E, 10 / 60); ax[0, 0].errorbar(pb - 1000, fb_, eb_, fmt="o", ms=3, color="k")
    tm = np.linspace(-3 * dur_d, 3 * dur_d, 500); ax[0, 0].plot(tm * 24, transit_model([0, rprs, ars, b], tm, P), "r-")
    ax[0, 0].set_xlim(-3 * dur_d * 24, 3 * dur_d * 24); ax[0, 0].set_xlabel("hours from mid-transit"); ax[0, 0].set_title(f"TIC {tic} P={P:.5f} d, folded (all sectors)")
    ax[0, 0].set_ylim(1 - 4 * depth - 3 * np.median(eb_), 1 + 2 * depth + 3 * np.median(eb_))
    for y in sorted(set(yrs)):
        m = yrs == y; pb, fb_, eb_ = bin_lc(ph[m] * P * 24 + 1000, F[m], E[m], 15 / 60); ax[0, 1].errorbar(pb - 1000, fb_, eb_, fmt="o", ms=3, label=str(y))
    ax[0, 1].set_xlim(-3 * dur_d * 24, 3 * dur_d * 24); ax[0, 1].legend(); ax[0, 1].set_title("per-year folded (15-min bins)"); ax[0, 1].set_ylim(ax[0, 0].get_ylim())
    if times:
        n = [x["epoch"] for x in times]; oc = [x["oc_min"] for x in times]; e = [x["tc_err"] * 1440 for x in times]; c = ["k" if x["dchi2"] > 4 else "0.7" for x in times]
        ax[1, 0].errorbar(n, oc, e, fmt="o", ecolor="0.6", mfc="none", mec="k"); ax[1, 0].scatter(n, oc, c=c, zorder=3); ax[1, 0].axhline(0, color="r"); ax[1, 0].set_xlabel("epoch"); ax[1, 0].set_ylabel("O-C (min)"); ax[1, 0].set_title("individual transit times (black: dchi2>4)")
    ax[1, 1].plot(ph, F, ".", ms=1, alpha=0.3, color="0.6"); pb, fb_, eb_ = bin_lc(ph + 10, F, E, 0.01); ax[1, 1].errorbar(pb - 10, fb_, eb_, fmt="o", ms=2, color="k"); ax[1, 1].set_ylim(ax[0, 0].get_ylim()); ax[1, 1].set_title("full phase (secondary check)"); ax[1, 1].set_xlabel("phase")
    fig.tight_layout(); fig.savefig(f"{OUT}/vet_summary.png", dpi=120); plt.close(fig)
    json.dump(rep, open(f"{OUT}/report.json", "w"), indent=1, default=lambda o: float(o) if isinstance(o, (np.floating, np.integer)) else str(o))
    print("  wrote", f"{OUT}/report.json")

if __name__ == "__main__": main()
