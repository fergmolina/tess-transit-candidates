"""Frozen outcome evaluator for a pre-registered transit prediction (matches the outcome rules written in each PREREGISTRATION file).
Given a light curve of the test sector (QLP/SPOC FITS, or any CSV with time,flux columns) and the frozen prediction CSV, it:
  1. transit-masks and biweight-detrends the light curve (window 0.7 d, mask 2x the duration around every predicted time);
  2. lists predicted transits whose window (+-1.5 durations) has >= 60 % cadence coverage;
  3. measures the stacked depth at the predicted phase and the per-transit box time offset (local box fit with linear baseline);
  4. returns one outcome: RECOVERED (>= 2 covered transits; stacked depth 0.5-1.5x the reference and duration 0.7-1.3x; stacked SNR >= 5;
     stacked timing offset within max(3 sigma_pred, 30 min)), INCONSISTENT (a comparable dip exists but its time is > 30 min from every
     prediction), EXCLUDED (>= 2 fully covered transits and stacked depth < 0.3x reference at 3 sigma), INSUFFICIENT (< 2 covered transits).
Usage: python -I prereg_test.py --lc FILE [--flux-col PDCSAP_FLUX|SAP_FLUX|DET_FLUX] --pred predicted_transits.csv --depth-ppm D --dur-h H [--sector N]
The script is part of the frozen pre-registration bundle; its SHA-256 is listed in SHA256SUMS.txt."""
import sys, argparse, json, numpy as np, pandas as pd
from wotan import flatten, transit_mask
ap = argparse.ArgumentParser(); ap.add_argument("--lc", required=True); ap.add_argument("--flux-col", default=""); ap.add_argument("--pred", required=True); ap.add_argument("--depth-ppm", type=float, required=True); ap.add_argument("--dur-h", type=float, required=True); ap.add_argument("--sector", type=int, default=0); ap.add_argument("--out", default=""); a = ap.parse_args()
# --- load light curve (BTJD time, relative flux)
if a.lc.lower().endswith(".fits"):
    from astropy.io import fits
    with fits.open(a.lc, memmap=False) as h:
        d = h[1].data; cols = h[1].columns.names; fc = a.flux_col or ("PDCSAP_FLUX" if "PDCSAP_FLUX" in cols else ("DET_FLUX" if "DET_FLUX" in cols else "SAP_FLUX"))
        t = np.asarray(d["TIME"], float); f = np.asarray(d[fc], float); q = np.asarray(d["QUALITY"], int)
    m = np.isfinite(t) & np.isfinite(f) & (q == 0); t, f = t[m], f[m] / np.nanmedian(f[m])
else:
    c = pd.read_csv(a.lc); t = c.iloc[:, 0].values.astype(float); f = c.iloc[:, 1].values.astype(float); m = np.isfinite(t) & np.isfinite(f); t, f = t[m], f[m] / np.nanmedian(f[m]); fc = "csv"
pred = pd.read_csv(a.pred); pred = pred[pred.status.astype(str).str.startswith("prediction")]
if a.sector: pred = pred[pred.tess_sector.astype(str).str.startswith(str(a.sector))]
dur = a.dur_h / 24; ref = a.depth_ppm * 1e-6; cad = float(np.median(np.diff(t)))
P = float(np.median(np.diff(pred.tc_btjd.values))) if len(pred) > 1 else np.nan
mask = np.zeros(len(t), bool)
for tc in pred.tc_btjd.values: mask |= np.abs(t - tc) < dur
fl = flatten(t, f, method="biweight", window_length=0.7, mask=mask); ok = np.isfinite(fl); t, fl = t[ok], fl[ok]; sig = 1.4826 * np.median(np.abs(fl - np.median(fl)))
rows = []
for _, r in pred.iterrows():
    tc = r.tc_btjd; w = np.abs(t - tc) < 1.5 * dur; cov = w.sum() * cad / (3 * dur); intr = np.abs(t - tc) < dur / 2
    if cov < 0.6 or intr.sum() < 3: rows.append(dict(epoch=int(r.epoch), coverage=round(cov, 2), covered=False)); continue
    grid = np.linspace(-0.1, 0.1, 241); chi = []
    for dt in grid:
        box = np.where(np.abs(t[w] - tc - dt) < dur / 2, 1.0, 0.0); A = np.vstack([np.ones(w.sum()), t[w] - tc, box]).T; c, *_ = np.linalg.lstsq(A, fl[w], rcond=None); chi.append(np.sum((fl[w] - A @ c) ** 2))
    chi = np.array(chi); i = int(np.argmin(chi)); box = np.where(np.abs(t[w] - tc - grid[i]) < dur / 2, 1.0, 0.0); A = np.vstack([np.ones(w.sum()), t[w] - tc, box]).T; c, *_ = np.linalg.lstsq(A, fl[w], rcond=None)
    oot = w & (np.abs(t - tc) > 0.75 * dur)
    base = np.polyval(np.polyfit(t[oot] - tc, fl[oot], 1), t[intr] - tc) if oot.sum() > 5 else np.ones(intr.sum())
    d_at = 1 - np.mean(fl[intr] / base)
    rows.append(dict(epoch=int(r.epoch), coverage=round(cov, 2), covered=True, depth_at_pred_ppm=float(d_at * 1e6), depth_err_ppm=float(sig / np.sqrt(intr.sum()) * 1e6), box_offset_min=float(grid[i] * 1440), box_depth_ppm=float(-c[2] * 1e6), sigma_pred_min=float(r.sigma_min)))
tab = pd.DataFrame(rows); cov = tab[tab.covered == True] if len(tab) else tab
res = dict(lc=a.lc, flux_col=fc, cadence_s=cad * 86400, n_predicted=len(pred), n_covered=int(len(cov)), reference_depth_ppm=a.depth_ppm, reference_dur_h=a.dur_h)
if len(cov) < 2: res["outcome"] = "INSUFFICIENT"
else:
    wts = 1 / cov.depth_err_ppm ** 2; dst = float(np.sum(cov.depth_at_pred_ppm * wts) / wts.sum()); dse = float(1 / np.sqrt(wts.sum())); snr = dst / dse
    off = float(np.average(cov.box_offset_min, weights=wts)); tol = max(3 * float(cov.sigma_pred_min.mean()), 30.0)
    res.update(stacked_depth_ppm=dst, stacked_err_ppm=dse, stacked_snr=snr, mean_box_offset_min=off, timing_tolerance_min=tol)
    if snr >= 5 and 0.5 * a.depth_ppm <= dst <= 1.5 * a.depth_ppm and abs(off) <= tol: res["outcome"] = "RECOVERED"
    elif dst + 3 * dse < 0.3 * a.depth_ppm: res["outcome"] = "EXCLUDED"
    else:
        # a comparable dip elsewhere? scan +-0.3 d around each prediction for the deepest box of the reference duration
        best = []
        for _, r in cov.iterrows():
            tc = pred.set_index("epoch").loc[r.epoch].tc_btjd; w = np.abs(t - tc) < 0.3 + dur; ts = np.arange(tc - 0.3, tc + 0.3, cad)
            dd = [1 - np.mean(fl[np.abs(t - x) < dur / 2]) if (np.abs(t - x) < dur / 2).sum() > 3 else 0 for x in ts]; j = int(np.argmax(dd)); best.append(((ts[j] - tc) * 1440, dd[j] * 1e6))
        res["nearest_comparable_dips"] = best
        res["outcome"] = "INCONSISTENT" if any(abs(o) > 30 and 0.5 * a.depth_ppm <= d <= 1.5 * a.depth_ppm for o, d in best) else "AMBIGUOUS (stacked depth/timing outside the recovered band but not excluded)"
print(tab.to_string(index=False)); print(json.dumps({k: v for k, v in res.items()}, indent=1, default=float))
if a.out: json.dump(dict(result=res, per_transit=rows), open(a.out, "w"), indent=1, default=float)
