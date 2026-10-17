"""Final ephemeris + pre-registered transit predictions for the 0.5719-d signal on TIC 317134140 (TOI-2514 host).
Data: SPOC 2-min S6, S87, S98, S107 (PDCSAP, masked biweight detrend, TOI-2514.01 transits removed) + TESS-SPOC 10-min FFI S32, S33.
Model: batman with shape fixed to the MCMC posterior medians; free (P, T0) on a 2-stage grid; 1-sigma from the delta-chi2=1 profile
(inflated by sqrt(reduced chi2)); season-jackknife for robustness. Predictions for S108 (observed, not yet public), S109, S110."""
import sys, os, json, warnings; sys.path.insert(0, "/Users/fernando/Desktop/NASA/scripts"); warnings.filterwarnings("ignore")
import numpy as np, lightkurve as lk
from astropy.time import Time
from wotan import flatten, transit_mask
from tsearch import load_spoc_lc, trim_edges
from search_pipeline import sector_files, year_of, bin_lc
import vet
from vet import transit_model, box_depth, sector_window_jd, sector_orbits
OUT = "/Users/fernando/Desktop/NASA/results/vet/317134140"
tic = 317134140; P0, T00, dur = 0.571864, 1468.67525, 1.5 / 24
rprs, ars, b = 0.0131, 2.6666, 0.4024
mP, mT0, mdur = 6.3951381, 2459215.084143 - 2457000, 4.047 / 24
def prep(t, f, exp):
    keep = trim_edges(t) & ~transit_mask(time=t, period=mP, duration=1.5 * mdur, T0=mT0); t, f = t[keep], f[keep]
    tm = transit_mask(time=t, period=P0, duration=2 * dur, T0=T00)
    flat = flatten(t, f, method="biweight", window_length=0.5, break_tolerance=0.5, mask=tm); ok = np.isfinite(flat)
    oot = ok & ~tm; mad = 1.4826 * np.median(np.abs(flat[oot] - np.median(flat[oot]))); ok &= flat < 1 + 5 * mad
    e = np.full(ok.sum(), 1.4826 * np.median(np.abs(np.diff(flat[ok]))) / np.sqrt(2))
    return t[ok], flat[ok], e, np.full(ok.sum(), exp)
sets = {}
for fp in sector_files(tic):
    t, f, fe, m = load_spoc_lc(fp); sets[f"S{m['sector']}_2min"] = prep(t, f, 120 / 86400)
sr = lk.search_lightcurve(f"TIC {tic}", author="TESS-SPOC")
for sec in (32, 33):
    s = sr[sr.mission == f"TESS Sector {sec:02d}"]
    lc = s[0].download(download_dir="/Users/fernando/Desktop/NASA/data/lk_cache").remove_nans(); lc = lc[lc.quality == 0].normalize()
    sets[f"S{sec}_ffi"] = prep(lc.time.value, lc.flux.value.astype(float), 600 / 86400)
for k, v in sets.items(): print(f"{k}: N={len(v[0])} rms={np.std(v[1])*1e6:.0f} ppm depth@eph={box_depth(v[0], v[1], P0, T00, dur)[0]*1e6:.0f}+-{box_depth(v[0], v[1], P0, T00, dur)[1]*1e6:.0f}")
def stack(keys):
    T = np.concatenate([sets[k][0] for k in keys]); F = np.concatenate([sets[k][1] for k in keys]); E = np.concatenate([sets[k][2] for k in keys]); X = np.concatenate([sets[k][3] for k in keys])
    o = np.argsort(T); return T[o], F[o], E[o], X[o]
def chi2_grid(T, F, E, X, Ps, T0s):
    ph0 = ((T - T00) / P0 + 0.5) % 1 - 0.5; near = np.abs(ph0 * P0) < 2.5 * dur
    tt, ff, ee, xx = T[near], F[near], E[near], X[near]
    chi = np.empty((len(Ps), len(T0s)))
    for i, Pi in enumerate(Ps):
        for j, T0j in enumerate(T0s):
            phi = ((tt - T0j) / Pi + 0.5) % 1 - 0.5
            # two cadences: evaluate model separately for 2-min and 10-min exposure times
            mod = np.empty_like(ff)
            for exp in np.unique(xx):
                s = xx == exp; mod[s] = transit_model([0.0, rprs, ars, b], phi[s] * Pi, Pi, exp_time=exp)
            chi[i, j] = np.sum(((ff - mod) / ee)**2)
    return chi, len(ff)
def fit(keys, label):
    T, F, E, X = stack(keys)
    Ps = P0 + np.linspace(-3e-5, 3e-5, 61); T0s = T00 + np.linspace(-0.02, 0.02, 41)
    chi, n = chi2_grid(T, F, E, X, Ps, T0s); i, j = np.unravel_index(np.argmin(chi), chi.shape)
    # stage 2: fine grid around minimum
    dP, dT = np.diff(Ps)[0], np.diff(T0s)[0]
    Ps2 = Ps[i] + np.linspace(-1.5 * dP, 1.5 * dP, 61); T0s2 = T0s[j] + np.linspace(-4 * dT, 4 * dT, 81)
    chi2_, n = chi2_grid(T, F, E, X, Ps2, T0s2); i2, j2 = np.unravel_index(np.argmin(chi2_), chi2_.shape)
    cmin = chi2_[i2, j2]; dof = n - 2; infl = max(1.0, cmin / dof)
    def width(prof, grid):
        ok = prof <= cmin + infl
        return max((grid[ok].max() - grid[ok].min()) / 2, np.diff(grid)[0] / 2), bool(ok[0] or ok[-1])
    P_err, pe = width(chi2_.min(axis=1), Ps2); T0_err, te = width(chi2_.min(axis=0), T0s2)
    # covariance via local quadratic fit of the chi2 surface
    ii = slice(max(0, i2 - 8), i2 + 9); jj = slice(max(0, j2 - 8), j2 + 9)
    sP, sT = np.diff(Ps2)[0], np.diff(T0s2)[0]   # fit the quadratic in grid-step units to keep the design matrix well scaled
    PP, TT = np.meshgrid((Ps2[ii] - Ps2[i2]) / sP, (T0s2[jj] - T0s2[j2]) / sT, indexing="ij"); Z = chi2_[ii, jj] - cmin
    A = np.vstack([PP.ravel()**2, TT.ravel()**2, PP.ravel() * TT.ravel(), PP.ravel(), TT.ravel(), np.ones(PP.size)]).T
    c = np.linalg.lstsq(A, Z.ravel(), rcond=None)[0]; H = np.array([[2 * c[0], c[2]], [c[2], 2 * c[1]]])
    cov_uv = np.linalg.inv(H / 2) * infl; S = np.diag([sP, sT]); cov = S @ cov_uv @ S
    # refine the minimum from the quadratic (sub-grid) and report the correlation
    xmin = -np.linalg.solve(H, c[3:5]); Pbest, T0best = Ps2[i2] + xmin[0] * sP, T0s2[j2] + xmin[1] * sT
    corr = cov[0, 1] / np.sqrt(cov[0, 0] * cov[1, 1])
    res = dict(label=label, keys=keys, n_pts_near_transit=int(n), P=float(Pbest), P_err_profile=float(P_err), T0=float(T0best), T0_err_profile=float(T0_err), corr_P_T0=float(corr),
               cov_PT0=cov.tolist(), P_err_cov=float(np.sqrt(cov[0, 0])), T0_err_cov=float(np.sqrt(cov[1, 1])), chi2=float(cmin), dof=int(dof), error_inflation=float(np.sqrt(infl)),
               grid_edge=bool(pe or te))
    print(f"{label}: P={res['P']:.7f} +- {res['P_err_cov']:.7f} (profile {P_err:.7f})  T0={res['T0']:.5f} +- {res['T0_err_cov']:.5f} (profile {T0_err:.5f}) corr={corr:+.2f} chi2/dof={cmin:.0f}/{dof} infl={np.sqrt(infl):.2f}{'  GRID EDGE' if res['grid_edge'] else ''}", flush=True)
    return res
allkeys = list(sets); full = fit(allkeys, "ALL (2-min S6,S87,S98,S107 + FFI S32,S33)")
jack = {}
for drop in ("S6_2min", "S32_ffi", "S33_ffi", "S87_2min", "S98_2min", "S107_2min"):
    jack[drop] = fit([k for k in allkeys if k != drop], f"drop {drop}")
two_min_only = fit([k for k in allkeys if k.endswith("2min")], "2-min only")
# predictions
Pf, T0f = full["P"], full["T0"]; cov = np.array(full["cov_PT0"])  # order (P, T0)
now = Time.now(); orbits = sector_orbits()
preds = []
for sec in (108, 109, 110):
    lo, hi = sector_window_jd(sec); n0 = int(np.ceil((lo - 2457000 - T0f) / Pf)); n1 = int(np.floor((hi - 2457000 - T0f) / Pf))
    for n in range(n0, n1 + 1):
        tc = T0f + n * Pf; var = cov[1, 1] + 2 * n * cov[0, 1] + n * n * cov[0, 0]
        preds.append(dict(sector=sec, epoch=n, tc_btjd=float(tc), tc_bjd_tdb=float(tc + 2457000), utc=Time(tc + 2457000, format="jd").iso[:19],
                          sigma_min=float(np.sqrt(var) * 1440), in_science_orbit=any(a <= tc + 2457000 <= b_ for a, b_ in orbits.get(sec, [])), ingress_utc=Time(tc + 2457000 - dur / 2, format="jd").iso[11:16], egress_utc=Time(tc + 2457000 + dur / 2, format="jd").iso[11:16]))
print(f"\nPredictions generated {now.iso} UTC; ephemeris T0(BTJD)={T0f:.5f}+-{full['T0_err_cov']:.5f}, P={Pf:.7f}+-{full['P_err_cov']:.7f} d, duration {dur*24:.2f} h, depth ~185 ppm")
for sec in (108, 109, 110):
    ps = [p for p in preds if p["sector"] == sec and p["in_science_orbit"]]
    print(f"  S{sec}: {len(ps)} transits inside science orbits; first {ps[0]['utc'] if ps else '-'} last {ps[-1]['utc'] if ps else '-'}; 1-sigma {np.mean([p['sigma_min'] for p in ps]) if ps else 0:.1f} min")
json.dump(dict(generated_utc=now.iso, full=full, jackknife=jack, two_min_only=two_min_only, shape_fixed=dict(rprs=rprs, ars=ars, b=b, dur_h=dur * 24), known_signal_masked=dict(P=mP, T0_btjd=mT0, dur_h=mdur * 24),
               per_set_depth={k: dict(depth_ppm=box_depth(v[0], v[1], Pf, T0f, dur)[0] * 1e6, err_ppm=box_depth(v[0], v[1], Pf, T0f, dur)[1] * 1e6, n=len(v[0])) for k, v in sets.items()},
               predictions=preds), open(f"{OUT}/final_ephemeris_predictions.json", "w"), indent=1, default=float)
import csv
with open(f"{OUT}/predicted_transits_S108_S109_S110.csv", "w", newline="") as fh:
    w = csv.writer(fh); w.writerow(["sector", "epoch", "tc_BJD_TDB", "tc_UTC", "sigma_minutes", "ingress_UTC", "egress_UTC", "in_science_orbit"])
    for p in preds: w.writerow([p["sector"], p["epoch"], f"{p['tc_bjd_tdb']:.5f}", p["utc"], f"{p['sigma_min']:.1f}", p["ingress_utc"], p["egress_utc"], p["in_science_orbit"]])
print("wrote", f"{OUT}/predicted_transits_S108_S109_S110.csv")
