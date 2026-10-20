"""Referee M3/M7: joint transit-shape fit of the four TIC 89247735 events in RAW QLP SAP_FLUX (all quality flags kept) with per-event
local linear baselines, quadratic limb darkening fixed at (0.52, 0.18) (TESS band, Teff ~4400 K), P fixed at the v3 value.
Free: T0 (epoch 138), rprs, a/R*, b (+ 2 baseline coefficients per event, solved linearly). emcee for errors. Reports model depth, T14,
T23, rho*, Rp with the TIC R* error (0.785 +- 0.066) and with the Gaia GSP-Phot / SED radii; and the empirical secondary-eclipse
scatter from the same estimator at 150 random phases. Output: results/vet_qlp/89247735/refit_raw_sap.json"""
import sys, os, json, glob, numpy as np; sys.path.insert(0, "/Users/fernando/Desktop/NASA/scripts"); os.environ["TSEARCH_SOURCE"] = "qlp"
import batman, emcee; from astropy.io import fits; from scipy.optimize import minimize
OUT = "/Users/fernando/Desktop/NASA/results/vet_qlp/89247735"; v3 = json.load(open(f"{OUT}/final_ephemeris_v3.json")); P = v3["P_d"]; T0g = v3["T0_btjd"]
U = [0.52, 0.18]; events = [(66, 79), (93, 118), (93, 119), (104, 138)]; data = []
def lc(sec, quality_zero=False):
    f = [x for x in glob.glob("/Users/fernando/Desktop/NASA/data/qlp/*89247735*") if f"s{sec:04d}" in x][0]
    with fits.open(f, memmap=False) as h: d = h[1].data; t = np.asarray(d["TIME"], float); fl = np.asarray(d["SAP_FLUX"], float); qq = np.asarray(d["QUALITY"], int)
    ok = np.isfinite(t) & np.isfinite(fl) & ((qq == 0) if quality_zero else True); return t[ok], fl[ok] / np.nanmedian(fl[ok])
for sec, ep in events:
    t, fl = lc(sec); tc0 = T0g + (ep - 138) * P; w = np.abs(t - tc0) < 0.45; t_, f_ = t[w], fl[w] / np.nanmedian(fl[w])
    oot = np.abs(t_ - tc0) > 0.15; sig = 1.4826 * np.median(np.abs(f_[oot] - np.median(f_[oot]))); data.append((ep, tc0, t_, f_, sig))
def model_lc(t, tc, rprs, ars, b):
    inc = np.degrees(np.arccos(np.clip(b / ars, 0, 1))); p = batman.TransitParams(); p.t0 = tc; p.per = P; p.rp = rprs; p.a = ars; p.inc = inc; p.ecc = 0; p.w = 90; p.u = U; p.limb_dark = "quadratic"
    return batman.TransitModel(p, t, supersample_factor=3, exp_time=200 / 86400).light_curve(p)
def chi2(theta):
    T0, rprs, ars, b = theta[:4]
    if not (0.03 < rprs < 0.3 and 5 < ars < 80 and 0 <= b < 1 + rprs): return 1e30
    c = 0.0
    for ep, tc0, t_, f_, sig in data:
        m = model_lc(t_, T0 + (ep - 138) * P, rprs, ars, b); A = np.vstack([m, m * (t_ - tc0)]).T; coef, *_ = np.linalg.lstsq(A, f_, rcond=None); c += np.sum(((f_ - A @ coef) / sig) ** 2)
    return c
x0 = np.array([T0g, 0.105, 31.0, 0.4]); res = minimize(chi2, x0, method="Nelder-Mead", options=dict(maxiter=4000, xatol=1e-6, fatol=1e-3)); best = res.x; npts = sum(len(d[2]) for d in data); print("best", best, "chi2", res.fun, "npts", npts, flush=True)
def lnp(theta): c = chi2(theta); return -0.5 * c if c < 1e29 else -np.inf
nw = 24; rng = np.random.default_rng(1); p0 = best + np.array([2e-4, 2e-3, 0.8, 0.05]) * rng.normal(size=(nw, 4)); p0[:, 3] = np.abs(p0[:, 3])
sam = emcee.EnsembleSampler(nw, 4, lnp); sam.run_mcmc(p0, 1500, progress=False); ch = sam.get_chain(discard=500, flat=True)
q = lambda x: np.percentile(x, [16, 50, 84]); T0q, kq, aq, bq = q(ch[:, 0]), q(ch[:, 1]), q(ch[:, 2]), q(ch[:, 3])
k, ars, b = kq[1], aq[1], bq[1]; inc = np.arccos(b / ars)
T14 = P / np.pi * np.arcsin(np.sqrt((1 + k) ** 2 - b ** 2) / (ars * np.sin(inc))) * 24; T23 = P / np.pi * np.arcsin(np.sqrt(max((1 - k) ** 2 - b ** 2, 0)) / (ars * np.sin(inc))) * 24
rho = 3 * np.pi / (6.674e-8 * (P * 86400) ** 2) * ars ** 3 / 1.41; depth_model = float(1 - model_lc(np.array([T0q[1]]), T0q[1], k, ars, b)[0])
Rs = dict(TIC=(0.785, 0.066), GSPPhot=(0.726, 0.03), SED_Zarco=(0.74, 0.04)); rp = {n: [k * r * 109.08, float(np.hypot(0.5 * (kq[2] - kq[0]) * r, k * e) * 109.08)] for n, (r, e) in Rs.items()}
def depth_at(phase):
    vals, errs = [], []
    for sec in (66, 93, 104):
        t, fl = lc(sec, quality_zero=True)
        for n in range(-300, 300):
            tc = T0q[1] + (n + phase) * P
            if tc < t.min() + 0.3 or tc > t.max() - 0.3: continue
            w = np.abs(t - tc) < 0.4; intr = np.abs(t - tc) < 2.0 / 24; oot = w & ~intr & (np.abs(t - tc) > 3.0 / 24)
            if intr.sum() < 20 or oot.sum() < 40: continue
            pf = np.polyfit(t[oot] - tc, fl[oot], 1); base = np.polyval(pf, t[intr] - tc); vals.append(1 - np.mean(fl[intr] / base)); errs.append(np.std(fl[oot] / np.polyval(pf, t[oot] - tc)) / np.sqrt(intr.sum()))
    vals, errs = np.array(vals), np.array(errs)
    if not len(vals): return (np.nan, np.nan, 0)
    w = 1 / errs ** 2; return (float(np.sum(vals * w) / w.sum()), float(1 / np.sqrt(w.sum())), int(len(vals)))
sec = depth_at(0.5); rng = np.random.default_rng(3); rnd = np.array([depth_at(float(ph))[0] for ph in rng.uniform(0.1, 0.9, 150)]); rnd = rnd[np.isfinite(rnd)]
out = dict(T0=T0q.tolist(), rprs=kq.tolist(), ars=aq.tolist(), b=bq.tolist(), T14_h=float(T14), T23_h=float(T23), rho_fit_solar=float(rho), depth_model_ppm=depth_model * 1e6, Rp_Re=rp, limb_dark=U, chi2=float(res.fun), npts=int(npts),
           secondary_phase05=dict(depth_ppm=sec[0] * 1e6, formal_err_ppm=sec[1] * 1e6, n_windows=sec[2]), random_phase_scatter_ppm=float(np.std(rnd) * 1e6), random_phase_p_exceed=float(np.mean(rnd >= sec[0])), random_phase_n=int(len(rnd)))
json.dump(out, open(f"{OUT}/refit_raw_sap.json", "w"), indent=1); print(json.dumps(out, indent=1))
