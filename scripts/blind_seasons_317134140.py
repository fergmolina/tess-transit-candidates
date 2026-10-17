"""Season-holdout blind test with the fine ephemeris fit: for each observing season, fit (P, T0) on all OTHER seasons only
(fixed shape), predict the held-out transits, and measure the stacked depth at the predicted phase vs a random-phase null."""
import sys, json, warnings; sys.path.insert(0, "/Users/fernando/Desktop/NASA/scripts"); warnings.filterwarnings("ignore")
import numpy as np, lightkurve as lk
from wotan import flatten, transit_mask
from tsearch import load_spoc_lc, trim_edges
from search_pipeline import sector_files, period_grid, bls_stats, bin_lc
from vet import transit_model, box_depth
tic = 317134140; P0, T00, dur = 0.571864, 1468.67525, 1.5 / 24; rprs, ars, b = 0.0131, 2.6666, 0.4024
mP, mT0, mdur = 6.3951381, 2459215.084143 - 2457000, 4.047 / 24
def prep(t, f, exp):
    keep = trim_edges(t) & ~transit_mask(time=t, period=mP, duration=1.5 * mdur, T0=mT0); t, f = t[keep], f[keep]
    tm = transit_mask(time=t, period=P0, duration=2 * dur, T0=T00)
    flat = flatten(t, f, method="biweight", window_length=0.5, break_tolerance=0.5, mask=tm); ok = np.isfinite(flat)
    oot = ok & ~tm; mad = 1.4826 * np.median(np.abs(flat[oot] - np.median(flat[oot]))); ok &= flat < 1 + 5 * mad
    return t[ok], flat[ok], np.full(ok.sum(), 1.4826 * np.median(np.abs(np.diff(flat[ok]))) / np.sqrt(2)), np.full(ok.sum(), exp)
sets = {}
for fp in sector_files(tic):
    t, f, fe, m = load_spoc_lc(fp); sets[f"S{m['sector']}"] = prep(t, f, 120 / 86400)
sr = lk.search_lightcurve(f"TIC {tic}", author="TESS-SPOC")
for sec in (32, 33):
    lc = sr[sr.mission == f"TESS Sector {sec:02d}"][0].download(download_dir="/Users/fernando/Desktop/NASA/data/lk_cache").remove_nans(); lc = lc[lc.quality == 0].normalize()
    sets[f"S{sec}"] = prep(lc.time.value, lc.flux.value.astype(float), 600 / 86400)
seasons = {"2018-19 (S6)": ["S6"], "2020-21 (S32,S33)": ["S32", "S33"], "2024-25 (S87)": ["S87"], "2025 (S98)": ["S98"], "2026 (S107)": ["S107"]}
def stack(keys):
    T = np.concatenate([sets[k][0] for k in keys]); F = np.concatenate([sets[k][1] for k in keys]); E = np.concatenate([sets[k][2] for k in keys]); X = np.concatenate([sets[k][3] for k in keys]); o = np.argsort(T); return T[o], F[o], E[o], X[o]
def chi2_grid(T, F, E, X, Ps, T0s):
    ph0 = ((T - T00) / P0 + 0.5) % 1 - 0.5; near = np.abs(ph0 * P0) < 2.5 * dur; tt, ff, ee, xx = T[near], F[near], E[near], X[near]
    chi = np.empty((len(Ps), len(T0s)))
    for i, Pi in enumerate(Ps):
        for j, T0j in enumerate(T0s):
            phi = ((tt - T0j) / Pi + 0.5) % 1 - 0.5; mod = np.empty_like(ff)
            for exp in np.unique(xx): s = xx == exp; mod[s] = transit_model([0.0, rprs, ars, b], phi[s] * Pi, Pi, exp_time=exp)
            chi[i, j] = np.sum(((ff - mod) / ee)**2)
    return chi, len(ff)
def fit(keys):
    T, F, E, X = stack(keys)
    Ps = P0 + np.linspace(-4e-5, 4e-5, 41); T0s = T00 + np.linspace(-0.03, 0.03, 31)
    chi, n = chi2_grid(T, F, E, X, Ps, T0s); i, j = np.unravel_index(np.argmin(chi), chi.shape); dP, dT = np.diff(Ps)[0], np.diff(T0s)[0]
    Ps2 = Ps[i] + np.linspace(-1.5 * dP, 1.5 * dP, 41); T0s2 = T0s[j] + np.linspace(-1.5 * dT, 1.5 * dT, 41)
    chi2_, n = chi2_grid(T, F, E, X, Ps2, T0s2); i2, j2 = np.unravel_index(np.argmin(chi2_), chi2_.shape); cmin = chi2_[i2, j2]; infl = max(1.0, cmin / (n - 2))
    ii = slice(max(0, i2 - 5), i2 + 6); jj = slice(max(0, j2 - 5), j2 + 6); PP, TT = np.meshgrid(Ps2[ii] - Ps2[i2], T0s2[jj] - T0s2[j2], indexing="ij"); Z = chi2_[ii, jj]
    A = np.vstack([PP.ravel()**2, TT.ravel()**2, PP.ravel() * TT.ravel(), PP.ravel(), TT.ravel(), np.ones(PP.size)]).T; c = np.linalg.lstsq(A, Z.ravel(), rcond=None)[0]
    H = np.array([[2 * c[0], c[2]], [c[2], 2 * c[1]]]); cov = np.linalg.inv(H / 2) * infl
    return dict(P=float(Ps2[i2]), T0=float(T0s2[j2]), cov=cov, P_err=float(np.sqrt(cov[0, 0])), T0_err=float(np.sqrt(cov[1, 1])), chi2=float(cmin), dof=int(n - 2))
out = {}
for name, hold in seasons.items():
    train = [k for k in sets if k not in hold]
    # (1) independent BLS on training data recovers the period?
    T, F, E, X = stack(train); Tb, Fb, Eb = bin_lc(T, F, E, 10 / 1440)
    pg = period_grid(T.max() - T.min(), 0.5, 20, 1 / 24, oversample=2.0); peaks = bls_stats(Tb, Fb, Eb, pg, np.array([1.0, 1.5, 2.0, 3.0, 4.0]) / 24)
    rank = next((i for i, pk in enumerate(peaks) if any(abs(pk["period"] * k - P0) / P0 < 0.01 for k in (1, 2, 0.5))), None)
    # (2) training-only ephemeris
    e = fit(train)
    # (3) holdout prediction
    Th, Fh, Eh, Xh = stack(hold); n_mid = round((Th.mean() - e["T0"]) / e["P"]); sig = np.sqrt(e["cov"][1, 1] + 2 * n_mid * e["cov"][0, 1] + n_mid**2 * e["cov"][0, 0])
    d, de, nin = box_depth(Th, Fh, e["P"], e["T0"], dur)
    rng = np.random.default_rng(0); nulls = np.array([box_depth(Th, Fh, e["P"], e["T0"] + e["P"] * (0.1 + 0.8 * rng.random()), dur)[0] for _ in range(2000)]); nulls = nulls[np.isfinite(nulls)]
    offs = np.arange(-3, 3.01, 0.25) / 24; scan = np.array([box_depth(Th, Fh, e["P"], e["T0"] + o, dur)[0] for o in offs]); ib = int(np.nanargmax(scan))
    print(f"HOLDOUT {name:18s}: training BLS rank={rank} (top {peaks[0]['period']:.4f} SDE {peaks[0]['sde']:.1f}); train P={e['P']:.7f}+-{e['P_err']:.7f} T0={e['T0']:.5f}+-{e['T0_err']:.5f}; predicted-phase 1-sigma at holdout = {sig*1440:.1f} min; depth at predicted phase {d*1e6:.0f}+-{de*1e6:.0f} ppm ({d/de:.1f} sigma, n_in={nin}); null sd {np.std(nulls)*1e6:.0f}, p={np.mean(nulls>=d):.4f}; deepest within +-3 h {scan[ib]*1e6:.0f} ppm at {offs[ib]*24:+.2f} h", flush=True)
    out[name] = dict(train=train, bls_rank=rank, train_top=[(p["period"], p["sde"]) for p in peaks], P=e["P"], P_err=e["P_err"], T0=e["T0"], T0_err=e["T0_err"], pred_sigma_min=float(sig * 1440), depth=d, depth_err=de, n_in=nin, null_p=float(np.mean(nulls >= d)), null_sd=float(np.std(nulls)), scan_best_h=float(offs[ib] * 24), scan_best_depth=float(scan[ib]))
json.dump(out, open("/Users/fernando/Desktop/NASA/results/vet/317134140/blind_seasons.json", "w"), indent=1, default=float)
