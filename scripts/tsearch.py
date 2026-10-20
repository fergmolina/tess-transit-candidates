"""Core transit-search utilities: load SPOC 2-min LCs, detrend, BLS search, TLS refinement.
Written for this project (2026-10-17). Uses lightkurve, wotan, astropy BLS, transitleastsquares.
"""
import os, glob, warnings, json
import numpy as np
from astropy.io import fits
from astropy.timeseries import BoxLeastSquares
warnings.filterwarnings("ignore")

DATA = "/Users/fernando/Desktop/NASA/data"

def load_spoc_lc(path, flux_col="PDCSAP_FLUX", quality_zero=True):
    """Return time (BTJD), normalised flux, flux_err, header meta for one SPOC _lc.fits file."""
    with fits.open(path, memmap=False) as h:
        d = h[1].data; hdr0 = h[0].header; hdr1 = h[1].header
        t = np.asarray(d["TIME"], float); f = np.asarray(d[flux_col], float)
        fe = np.asarray(d[flux_col + "_ERR"], float); q = np.asarray(d["QUALITY"], int)
        meta = dict(tic=int(hdr0["TICID"]), sector=int(hdr0["SECTOR"]), tmag=hdr0.get("TESSMAG"),
                    teff=hdr0.get("TEFF"), rad=hdr0.get("RADIUS"), logg=hdr0.get("LOGG"),
                    ra=hdr0.get("RA_OBJ"), dec=hdr0.get("DEC_OBJ"),
                    crowdsap=hdr1.get("CROWDSAP"), flfrcsap=hdr1.get("FLFRCSAP"),
                    camera=hdr0.get("CAMERA"), ccd=hdr0.get("CCD"))
    m = np.isfinite(t) & np.isfinite(f) & np.isfinite(fe)
    if quality_zero: m &= (q == 0)
    t, f, fe = t[m], f[m], fe[m]
    med = np.nanmedian(f)
    return t, f / med, fe / med, meta

def load_qlp_lc(path, flux_col="DET_FLUX", quality_zero=True):
    """QLP HLSP light curve: TIME (BTJD), DET_FLUX (QLP-detrended, normalised), DET_FLUX_ERR, QUALITY."""
    with fits.open(path, memmap=False) as h:
        d = h[1].data; hdr0 = h[0].header; cols = h[1].columns.names
        if flux_col not in cols: flux_col = "KSPSAP_FLUX" if "KSPSAP_FLUX" in cols else "SAP_FLUX"
        t = np.asarray(d["TIME"], float); f = np.asarray(d[flux_col], float)
        ecol = flux_col + "_ERR"
        fe = np.asarray(d[ecol], float) if ecol in cols else np.full_like(f, np.nan)
        q = np.asarray(d["QUALITY"], int)
        if np.mean(np.isfinite(fe) & (fe > 0)) < 0.5:  # QLP sectors >= ~94 ship NaN errors: use point-to-point scatter
            g = np.isfinite(f) & (q == 0); sig = 1.4826 * np.nanmedian(np.abs(np.diff(f[g]))) / np.sqrt(2) if g.sum() > 10 else np.nanstd(f)
            fe = np.full_like(f, sig)
        meta = dict(tic=int(hdr0["TICID"]), sector=int(hdr0["SECTOR"]), tmag=hdr0.get("TESSMAG"), teff=hdr0.get("TEFF"),
                    rad=hdr0.get("RADIUS"), logg=hdr0.get("LOGG"), ra=hdr0.get("RA_OBJ"), dec=hdr0.get("DEC_OBJ"),
                    crowdsap=None, flfrcsap=None, camera=hdr0.get("CAMERA"), ccd=hdr0.get("CCD"), source="QLP")
    m = np.isfinite(t) & np.isfinite(f) & np.isfinite(fe) & (fe > 0)
    # Quality policy for the PERIODIC search: QUALITY == 0. Keeping the QLP bit-2^30 (orbit-start ramp) cadences was tested on
    # 2026-10-18 (results/search_qlp_v2): DET_FLUX there carries ramp residuals of up to 12 % (the QLP spline is fit on unflagged
    # data), known-signal recovery fell from 22 to 5 of 40 and the TIC 89247735 periodogram was swamped by a 15-d ramp alias.
    # Transits inside ramps are instead covered by the single-transit pass (single_transit_search.py, SAP flux + local baseline).
    # Flux excursions > 50 % of the median (data dropouts) are dropped in any case.
    if quality_zero: m &= (q == 0)
    med0 = np.nanmedian(f[m]) if m.any() else np.nan
    if np.isfinite(med0): m &= np.abs(f / med0 - 1) < 0.5
    t, f, fe = t[m], f[m], fe[m]
    med = np.nanmedian(f)
    return t, f / med, fe / med, meta

def trim_edges(t, gap=0.25, pad=0.3):
    """Mask points within `pad` days of any gap longer than `gap` days and of the start/end of the series (ramps, scattered light)."""
    keep = np.ones(len(t), bool)
    if len(t) == 0: return keep
    dt = np.diff(t); gi = np.where(dt > gap)[0]
    edges_lo = [t[0]] + [t[i + 1] for i in gi]      # starts of segments
    edges_hi = [t[i] for i in gi] + [t[-1]]          # ends of segments
    for lo in edges_lo: keep &= ~((t >= lo) & (t < lo + pad))
    for hi in edges_hi: keep &= ~((t <= hi) & (t > hi - pad))
    return keep

def detrend(t, f, window=0.5, method="biweight", edge_trim=True):
    from wotan import flatten
    if edge_trim:
        k = trim_edges(t); t, f = t[k], f[k]
        # callers rely on the returned mask being relative to the ORIGINAL arrays: rebuild below
    flat, trend = flatten(t, f, method=method, window_length=window, return_trend=True, break_tolerance=0.5)
    m = np.isfinite(flat)
    # clip only upward outliers (flares, cosmic rays); keep dips
    mad = np.nanmedian(np.abs(flat[m] - np.nanmedian(flat[m]))) * 1.4826
    m &= flat < 1 + 5 * mad
    if edge_trim:
        full = np.zeros(len(k), bool); full[np.where(k)[0][m]] = True
        return t[m], flat[m], full, trend
    return t[m], flat[m], m, trend

def bls_search(t, f, fe=None, pmin=0.5, pmax=None, durations_h=(1, 1.5, 2, 3, 4, 5), oversample=5, min_transits=2):
    """Astropy BLS over a period grid; returns dict with best period, t0, depth, duration, SDE-like stat."""
    baseline = t.max() - t.min()
    if pmax is None: pmax = baseline / min_transits
    durs = np.array(durations_h) / 24.0
    bls = BoxLeastSquares(t, f, dy=fe)
    # frequency grid with duration-based oversampling
    periods = bls.autoperiod(durs, minimum_period=pmin, maximum_period=pmax, frequency_factor=1.0 / oversample)
    res = bls.power(periods, durs, objective="snr")
    pw = res.power
    i = int(np.nanargmax(pw))
    # SDE: (peak - mean)/std of the periodogram (after removing a smooth trend)
    sde = (pw[i] - np.nanmean(pw)) / np.nanstd(pw)
    stats = bls.compute_stats(res.period[i], res.duration[i], res.transit_time[i])
    return dict(period=float(res.period[i]), t0=float(res.transit_time[i]), duration_h=float(res.duration[i] * 24),
                depth=float(res.depth[i]), depth_err=float(res.depth_err[i]), snr=float(pw[i]), sde=float(sde),
                n_transits=int(np.sum(stats["per_transit_count"] > 0)),
                depth_odd=float(stats["depth_odd"][0]), depth_even=float(stats["depth_even"][0]),
                depth_half=float(stats["depth_half"][0]),  # secondary at phase 0.5
                harmonic_delta_log_likelihood=float(stats["harmonic_delta_log_likelihood"]),
                periods=res.period, power=pw)

def tls_search(t, f, fe, pmin=0.5, pmax=None, R_star=1.0, M_star=1.0, oversampling=3, duration_grid_step=1.1, use_threads=4):
    from transitleastsquares import transitleastsquares
    model = transitleastsquares(t, f, fe)
    kw = dict(period_min=pmin, oversampling_factor=oversampling, duration_grid_step=duration_grid_step,
              R_star=R_star, M_star=M_star, R_star_min=0.1, R_star_max=3.5, M_star_min=0.08, M_star_max=3.0,
              use_threads=use_threads, show_progress_bar=False)
    if pmax: kw["period_max"] = pmax
    r = model.power(**kw)
    return dict(period=float(r.period), period_err=float(r.period_uncertainty), t0=float(r.T0), duration_h=float(r.duration * 24),
                depth=float(1 - r.depth), sde=float(r.SDE), snr=float(r.snr), n_transits=int(r.transit_count),
                distinct_transits=int(r.distinct_transit_count), odd_even_mismatch=float(r.odd_even_mismatch),
                rp_rs=float(r.rp_rs), transit_times=[float(x) for x in r.transit_times],
                per_transit_depth=[float(x) for x in r.transit_depths] if hasattr(r, "transit_depths") else None,
                periods=r.periods, power=r.power)
