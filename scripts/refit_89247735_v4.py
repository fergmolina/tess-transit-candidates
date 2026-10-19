"""Round-3 external referee (issues 1 and 5): joint raw-SAP transit-shape fit of TIC 89247735 as refit_89247735_raw.py, but
(a) the Sector-104 QLP TIME column is corrected by the clock offset of s104_clock_89247735.py (+8.02 min; MAST S99-S104 barycentric issue),
(b) P fixed at the v4 value, and (c) sensitivity variants: --ld fixed (u = 0.52, 0.18) or --ld prior (u1, u2 free with Gaussian priors
sigma 0.1 about those values), and --base 1 or 2 (per-event polynomial baseline order). Secondary-eclipse statistics are computed only for
the reference configuration (fixed LD, linear baseline). Output: results/vet_qlp/89247735/refit_v4_<ld>_b<base>.json"""
import sys, os, json, glob, argparse, numpy as np
import batman, emcee; from astropy.io import fits; from scipy.optimize import minimize
ap = argparse.ArgumentParser(); ap.add_argument("--ld", default="fixed"); ap.add_argument("--base", type=int, default=1); a = ap.parse_args()
OUT = "/Users/fernando/Desktop/NASA/results/vet_qlp/89247735"; v4 = json.load(open(f"{OUT}/final_ephemeris_v4.json")); P = v4["P_d"]; T0g = v4["T0_btjd"]
CORR104 = v4["s104_clock_correction_min"] / 1440; U0 = np.array([0.52, 0.18]); events = [(66, 79), (93, 118), (93, 119), (104, 138)]; data = []
def lc(sec, quality_zero=False):
    f = [x for x in glob.glob("/Users/fernando/Desktop/NASA/data/qlp/*89247735*") if f"s{sec:04d}" in x][0]
    with fits.open(f, memmap=False) as h: d = h[1].data; t = np.asarray(d["TIME"], float); fl = np.asarray(d["SAP_FLUX"], float); qq = np.asarray(d["QUALITY"], int)
    if sec == 104: t = t + CORR104
    ok = np.isfinite(t) & np.isfinite(fl) & ((qq == 0) if quality_zero else True); return t[ok], fl[ok] / np.nanmedian(fl[ok])
for sec, ep in events:
    t, fl = lc(sec); tc0 = T0g + (ep - 138) * P; w = np.abs(t - tc0) < 0.45; t_, f_ = t[w], fl[w] / np.nanmedian(fl[w])
    oot = np.abs(t_ - tc0) > 0.15; sig = 1.4826 * np.median(np.abs(f_[oot] - np.median(f_[oot]))); data.append((ep, tc0, t_, f_, sig))
def model_lc(t, tc, rprs, ars, b, u):
    inc = np.degrees(np.arccos(np.clip(b / ars, 0, 1))); p = batman.TransitParams(); p.t0 = tc; p.per = P; p.rp = rprs; p.a = ars; p.inc = inc; p.ecc = 0; p.w = 90; p.u = list(u); p.limb_dark = "quadratic"
    return batman.TransitModel(p, t, supersample_factor=3, exp_time=200 / 86400).light_curve(p)
NP = 4 if a.ld == "fixed" else 6
def chi2(theta):
    T0, rprs, ars, b = theta[:4]; u = U0 if a.ld == "fixed" else theta[4:6]
    if not (0.03 < rprs < 0.3 and 5 < ars < 80 and 0 <= b < 1 + rprs): return 1e30
    if a.ld != "fixed" and not (0 < u[0] + u[1] < 1 and u[0] > 0): return 1e30
    c = 0.0
    for ep, tc0, t_, f_, sig in data:
        m = model_lc(t_, T0 + (ep - 138) * P, rprs, ars, b, u); A = np.vstack([m * (t_ - tc0) ** j for j in range(a.base + 1)]).T
        coef, *_ = np.linalg.lstsq(A, f_, rcond=None); c += np.sum(((f_ - A @ coef) / sig) ** 2)
    if a.ld != "fixed": c += np.sum(((np.asarray(u) - U0) / 0.1) ** 2)
    return c
x0 = np.array([T0g, 0.10, 32.0, 0.3] + ([] if a.ld == "fixed" else list(U0)))
res = minimize(chi2, x0, method="Nelder-Mead", options=dict(maxiter=8000, xatol=1e-6, fatol=1e-3)); best = res.x; npts = sum(len(d[2]) for d in data); print("best", best, "chi2", res.fun, "npts", npts, flush=True)
def lnp(theta): c = chi2(theta); return -0.5 * c if c < 1e29 else -np.inf
nw = 32; rng = np.random.default_rng(1); sc = np.array([2e-4, 2e-3, 0.8, 0.05] + ([] if a.ld == "fixed" else [0.03, 0.03]))
p0 = best + sc * rng.normal(size=(nw, NP)); p0[:, 3] = np.abs(p0[:, 3])
sam = emcee.EnsembleSampler(nw, NP, lnp); sam.run_mcmc(p0, 2000, progress=False); ch = sam.get_chain(discard=700, flat=True)
q = lambda x: np.percentile(x, [16, 50, 84]).tolist(); k, ars, b = np.median(ch[:, 1]), np.median(ch[:, 2]), np.median(ch[:, 3]); inc = np.arccos(b / ars)
T14 = P / np.pi * np.arcsin(np.sqrt((1 + k) ** 2 - b ** 2) / (ars * np.sin(inc))) * 24; T23 = P / np.pi * np.arcsin(np.sqrt(max((1 - k) ** 2 - b ** 2, 0)) / (ars * np.sin(inc))) * 24
rho_ch = 3 * np.pi / (6.674e-8 * (P * 86400) ** 2) * ch[:, 2] ** 3 / 1.41
u_med = U0 if a.ld == "fixed" else np.median(ch[:, 4:6], axis=0); depth_model = float(1 - model_lc(np.array([0.0]), 0.0, k, ars, b, u_med)[0])
Rs = dict(TIC=(0.785, 0.066), GSPPhot=(0.726, 0.03), SED_Zarco=(0.74, 0.04)); kq = q(ch[:, 1]); rp = {n: [k * r * 109.08, float(np.hypot(0.5 * (kq[2] - kq[0]) * r, k * e) * 109.08)] for n, (r, e) in Rs.items()}
out = dict(config=dict(ld=a.ld, baseline_order=a.base, s104_clock_correction_min=v4["s104_clock_correction_min"], P_fixed=P), T0=q(ch[:, 0]), rprs=kq, ars=q(ch[:, 2]), b=q(ch[:, 3]),
           u=(U0.tolist() if a.ld == "fixed" else [q(ch[:, 4]), q(ch[:, 5])]), T14_h=float(T14), T23_h=float(T23), rho_fit_solar=q(rho_ch), depth_model_ppm=depth_model * 1e6, Rp_Re=rp, chi2=float(res.fun), npts=int(npts))
if a.ld == "fixed" and a.base == 1:
    def depth_at(phase):
        vals, errs = [], []
        for sec in (66, 93, 104):
            t, fl = lc(sec, quality_zero=True)
            for n in range(-300, 300):
                tc = out["T0"][1] + (n + phase) * P
                if tc < t.min() + 0.3 or tc > t.max() - 0.3: continue
                w = np.abs(t - tc) < 0.4; intr = np.abs(t - tc) < 2.0 / 24; oot = w & ~intr & (np.abs(t - tc) > 3.0 / 24)
                if intr.sum() < 20 or oot.sum() < 40: continue
                pf = np.polyfit(t[oot] - tc, fl[oot], 1); base = np.polyval(pf, t[intr] - tc); vals.append(1 - np.mean(fl[intr] / base)); errs.append(np.std(fl[oot] / np.polyval(pf, t[oot] - tc)) / np.sqrt(intr.sum()))
        vals, errs = np.array(vals), np.array(errs)
        if not len(vals): return (np.nan, np.nan, 0)
        w = 1 / errs ** 2; return (float(np.sum(vals * w) / w.sum()), float(1 / np.sqrt(w.sum())), int(len(vals)))
    sec = depth_at(0.5); rng = np.random.default_rng(3); rnd = np.array([depth_at(float(ph))[0] for ph in rng.uniform(0.1, 0.9, 150)]); rnd = rnd[np.isfinite(rnd)]
    out.update(secondary_phase05=dict(depth_ppm=sec[0] * 1e6, formal_err_ppm=sec[1] * 1e6, n_windows=sec[2]), random_phase_scatter_ppm=float(np.std(rnd) * 1e6), random_phase_p_exceed=float(np.mean(rnd >= sec[0])))
fn = f"{OUT}/refit_v4_{a.ld}_b{a.base}.json"; json.dump(out, open(fn, "w"), indent=1); print(json.dumps(out, indent=1))
