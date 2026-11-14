"""EXPLORATORY, POST-OUTCOME look at Sector 108 of TIC 317134140 (plan: results/exploratory_317134140_S108/PLAN.md, declared in
DECISIONS 232 before this script was written). It cannot change the outcome of record (PARTIAL, v1.20). Frozen ephemeris only."""
import sys, os, json, csv, hashlib, importlib.util
import numpy as np
R = "/Users/fernando/Desktop/NASA"; E = f"{R}/results/exploratory_317134140_S108"; sys.path.insert(0, f"{R}/scripts")
LC = f"{R}/results/test_317134140/S108/lc/tess2026250081459-s0108-0000000317134140-0310-s_lc.fits"
TPF_NAME = "tess2026250081459-s0108-0000000317134140-0310-s_tp.fits"; TPF = f"{E}/tpf/{TPF_NAME}"
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
assert sha(f"{E}/PLAN.md").startswith("07c490b3e9a69399") and sha(LC).startswith("cea2619b6228e770")
spec = importlib.util.spec_from_file_location("scorer", f"{R}/scripts/prereg_spoc_317134140.py"); S = importlib.util.module_from_spec(spec); spec.loader.exec_module(S)
assert sha(f"{R}/scripts/prereg_spoc_317134140.py").startswith("f3f55c0d74733f8a")
from astropy.io import fits
from tsearch import trim_edges
from wotan import flatten, transit_mask
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
P, T0, T14 = S.P_SIG, S.T0_SIG, S.T14_H / 24
rec = json.load(open(f"{R}/results/test_317134140/S108/result_S108.json")); out = dict(label="EXPLORATORY, POST-OUTCOME; not the outcome of record", plan_sha256=sha(f"{E}/PLAN.md"))
tcs = np.array([float(r["tc_BJD_TDB"]) - 2457000 for r in csv.DictReader(open(f"{R}/results/vet/317134140/predicted_transits_S108_S109_S110.csv")) if int(r["sector"]) == 108])

# ---- Item 0: gate
t, f, fe, m = S.preprocess(LC); a = S.clause_a(t, f, list(tcs))
gate = dict(n_cadences=int(len(t)), n_eligible=a["n_eligible"], n_predicted=a["n_predicted"], depth_ppm=a["depth_ppm"], sigma_ppm=a["sigma_ppm"])
assert len(t) == rec["n_cadences"] == 11862 and a["n_eligible"] == 28 and a["n_predicted"] == 48 and a["depth_ppm"] == rec["depth_ppm"] and a["sigma_ppm"] == rec["sigma_ppm"], gate
out["item0_gate"] = dict(gate, identical_to_result_of_record=True)

# ---- Item 1: cadence accounting and per-event eligibility
with fits.open(LC, memmap=False) as h:
    d = h[1].data; rt = np.asarray(d["TIME"], float); rf = np.asarray(d["PDCSAP_FLUX"], float); rfe = np.asarray(d["PDCSAP_FLUX_ERR"], float); rq = np.asarray(d["QUALITY"], int)
    rsap = np.asarray(d["SAP_FLUX"], float); cx = np.asarray(d["MOM_CENTR1"], float); cy = np.asarray(d["MOM_CENTR2"], float)
N = len(rt); label = np.array(["kept"] * N, dtype=object)
def account(apply_toi=True):
    lab = np.array(["kept"] * N, dtype=object); live = np.ones(N, bool)
    def cut(mask_bad, name):
        nonlocal live
        lab[live & mask_bad] = name; live = live & ~mask_bad
    cut(~np.isfinite(rt), "time not finite"); cut(~(np.isfinite(rf) & np.isfinite(rfe)), "flux or error not finite"); cut(rq != 0, "QUALITY != 0"); cut(~(rfe > 0), "error <= 0")
    idx = np.where(live)[0]; tt = rt[idx]; trim = trim_edges(tt); tm = transit_mask(time=tt, period=S.P_TOI, duration=S.TOI_MASK_MULT * S.DUR_TOI_H / 24, T0=S.T0_TOI)
    lab[idx[~trim]] = "edge trim"; lab[idx[trim & tm]] = "TOI-2514.01 mask" if apply_toi else "kept"
    keep = trim & ~tm if apply_toi else trim; idx = idx[keep]; med = np.nanmedian(rf[np.isfinite(rt) & np.isfinite(rf) & np.isfinite(rfe) & (rq == 0)])
    flat = flatten(rt[idx], rf[idx] / med, method="biweight", window_length=0.5, break_tolerance=0.5); ok = np.isfinite(flat)
    lab[idx[~ok]] = "detrending NaN"; mad = 1.4826 * np.median(np.abs(flat[ok] - np.median(flat[ok]))); clip = ok & ~(flat < 1 + 5 * mad); lab[idx[clip]] = "upward clip"
    return lab
lab = account(True); kept_t = rt[lab == "kept"]
steps = ["time not finite", "flux or error not finite", "QUALITY != 0", "error <= 0", "edge trim", "TOI-2514.01 mask", "detrending NaN", "upward clip", "kept"]
acc = {s: int((lab == s).sum()) for s in steps}; acc["total_rows"] = N
assert acc["kept"] == 11862 and np.array_equal(kept_t, t) and acc["TOI-2514.01 mask"] == rec["toi_mask_removed"], acc
out["item1_cadence_accounting"] = acc
ft = rt[np.isfinite(rt)]; gi = np.where(np.diff(kept_t) > 0.25)[0]
out["item1_time"] = dict(first_row=float(ft.min()), last_row=float(ft.max()), kept_first=float(kept_t.min()), kept_last=float(kept_t.max()),
                         gaps_in_kept_gt_0p25d=[[float(kept_t[i]), float(kept_t[i + 1]), float(kept_t[i + 1] - kept_t[i])] for i in gi])
half, lo, hi, nexp = T14 / 2, 0.75 / 24, 3.0 / 24, 45
def per_event(kt):
    rows = []
    for tc in tcs:
        dd = kt - tc; i = int((np.abs(dd) < half).sum()); o = (np.abs(dd) > lo) & (np.abs(dd) < hi); b, af = int((o & (dd < 0)).sum()), int((o & (dd > 0)).sum())
        rows.append((i, b, af, i >= 0.5 * nexp and b >= 10 and af >= 10))
    return rows
ev = per_event(kept_t); lab2 = account(False); ev2 = per_event(rt[lab2 == "kept"]); events = []
for k, tc in enumerate(tcs):
    i, b, af, ok = ev[k]; near = np.isfinite(rt) & (np.abs(rt - tc) < hi); cnt = {s: int((lab[near] == s).sum()) for s in steps if s != "kept" and (lab[near] == s).sum()}
    exp_rows = int(round(2 * hi / (2 / 1440))); missing = exp_rows - int(near.sum())
    if missing > 0: cnt["no row with finite time"] = missing
    failed = [n for n, c in (("in-window < 23", i < 0.5 * nexp), ("before < 10", b < 10), ("after < 10", af < 10)) if c]
    events.append(dict(epoch=int(round((tc - T0) / P)), tc_btjd=float(tc), n_in=i, n_before=b, n_after=af, eligible=bool(ok), failed=failed,
                       removed_within_3h=cnt, dominant_removal=(max(cnt, key=cnt.get) if cnt and not ok else None), eligible_without_toi_mask=bool(ev2[k][3])))
assert sum(e["eligible"] for e in events) == 28
out["item1_events"] = events
dom = {}
for e in events:
    if not e["eligible"]: dom[e["dominant_removal"]] = dom.get(e["dominant_removal"], 0) + 1
out["item1_summary"] = dict(ineligible_by_dominant_removal=dom, eligible_without_toi_mask=int(sum(e["eligible_without_toi_mask"] for e in events)),
                            ineligible_tc_range=[[e["epoch"], round(e["tc_btjd"], 3), e["dominant_removal"]] for e in events if not e["eligible"]])

# ---- Item 2: the blind search, full periodogram (same functions and grid as clause B)
from search_pipeline import bin_lc, period_grid, bls_stats
from astropy.timeseries import BoxLeastSquares
from scipy.ndimage import median_filter
durs = np.array([1.0, 1.5, 2.0, 3.0, 4.0]) / 24; base = t.max() - t.min(); pg = period_grid(base, 0.5, max(1.0, base / 2), durs.min(), oversample=3)
tb, fb, eb = bin_lc(t, f, fe, 6 / 1440); peaks = bls_stats(tb, fb, eb, pg, durs)
assert [p["period"] for p in peaks] == [p["period"] for p in rec["top3"]] and [p["sde"] for p in peaks] == [p["sde"] for p in rec["top3"]]
res = BoxLeastSquares(tb, fb, dy=eb).power(pg, durs, objective="snr"); pw = np.asarray(res.power); pw[~np.isfinite(pw)] = 0
k = max(51, len(pw) // 200 | 1); sde = (pw - median_filter(pw, size=k, mode="nearest")); sde = sde / (np.median(np.abs(sde - np.median(sde))) * 1.4826 + 1e-12)
per = np.asarray(res.period); rank = np.empty(len(sde), int); rank[np.argsort(sde)[::-1]] = np.arange(1, len(sde) + 1)
def at(p0):
    j = int(np.argmin(np.abs(per - p0))); r = dict(grid_period=float(per[j]), sde=float(sde[j]), rank_of_grid_point=int(rank[j]), n_grid=int(len(per)), duration_h=float(res.duration[j] * 24), t0=float(res.transit_time[j]),
                                                   local_step_frac=float(abs(per[min(j + 1, len(per) - 1)] - per[j - 1]) / 2 / per[j]))
    for w in (0.001, 0.005, 0.01):
        mm = np.abs(per / p0 - 1) <= w; jj = np.where(mm)[0][np.argmax(sde[mm])]; r[f"max_sde_within_{w*100:g}pct"] = dict(period=float(per[jj]), sde=float(sde[jj]), rank=int(rank[jj]))
    return r
out["item2_periodogram"] = dict(baseline_d=float(base), n_grid=int(len(per)), top3=[dict(period=p["period"], sde=p["sde"], t0=p["t0"], depth_odd_ppm=p["depth_odd"] * 1e6, depth_even_ppm=p["depth_even"] * 1e6,
                                depth_odd_err_ppm=p["depth_odd_err"] * 1e6, depth_even_err_ppm=p["depth_even_err"] * 1e6) for p in peaks], at_P=at(P), at_half_P=at(P / 2) if P / 2 >= per.min() else "below the grid minimum (0.5 d)", at_2P=at(2 * P))
p1 = peaks[0]; n1 = np.round((tcs - p1["t0"]) / p1["period"]); model_t = p1["t0"] + n1 * p1["period"]; off = (model_t - tcs) * 24
# offset of each first-peak transit from the nearest frozen predicted time
pk_times = p1["t0"] + np.arange(0, int(base / p1["period"]) + 2) * p1["period"]; pk_times = pk_times[(pk_times >= t.min()) & (pk_times <= t.max())]
pk_off = np.array([(x - tcs[np.argmin(np.abs(tcs - x))]) * 24 for x in pk_times])
out["item2_first_peak"] = dict(period=p1["period"], t0=p1["t0"], frac_from_2P=float(p1["period"] / (2 * P) - 1), t0_offset_from_nearest_predicted_h=float(pk_off[0]),
                               offsets_of_its_transits_from_nearest_predicted_h=[float(x) for x in pk_off], drift_vs_2P_over_sector_h=float((p1["period"] - 2 * P) * (base / (2 * P)) * 24), T14_h=1.5,
                               parity_of_nearest_epochs=[int(round((x - T0) / P)) % 2 for x in pk_times])
ep = np.round((tcs - T0) / P).astype(int)
def half_stat(sel):
    r = S.clause_a(t, f, list(tcs[sel])); return dict(depth_ppm=r["depth_ppm"], sigma_ppm=r["sigma_ppm"], n_eligible=r["n_eligible"], n_predicted=r["n_predicted"])
odd, even = half_stat(ep % 2 == 1), half_stat(ep % 2 == 0)
dsig = float(np.hypot(odd["sigma_ppm"], even["sigma_ppm"]))
out["item2_odd_even"] = dict(odd=odd, even=even, difference_ppm=float(odd["depth_ppm"] - even["depth_ppm"]), difference_sigma_ppm=dsig, difference_over_sigma=float((odd["depth_ppm"] - even["depth_ppm"]) / dsig),
                             note="clause A statistic and seeded random-phase sigma on each parity; exploratory")
fig, ax = plt.subplots(1, 2, figsize=(11, 3.8))
for a_, pp, name in ((ax[0], P, "frozen P = 0.5718634 d"), (ax[1], 2 * P, "2P = 1.1437268 d")):
    ph = ((t - T0) / pp + 0.5) % 1 - 0.5; nb = 40 if pp == P else 80; edges = np.linspace(-0.5, 0.5, nb + 1); ib = np.digitize(ph, edges) - 1
    bm = np.array([np.mean(f[ib == j]) if (ib == j).sum() > 5 else np.nan for j in range(nb)]); be = np.array([np.std(f[ib == j]) / np.sqrt((ib == j).sum()) if (ib == j).sum() > 5 else np.nan for j in range(nb)])
    a_.errorbar((edges[:-1] + edges[1:]) / 2 * pp * 24, (bm - 1) * 1e6, be * 1e6, fmt="o", ms=3, color="k"); a_.axvspan(-0.75, 0.75, color="C0", alpha=0.15); a_.axhline(0, color="gray", lw=0.6)
    if pp != P: a_.axvspan(pp * 12 - 0.75, pp * 12, color="C0", alpha=0.15); a_.axvspan(-pp * 12, -pp * 12 + 0.75, color="C0", alpha=0.15)
    a_.set_xlabel("hours from predicted mid-time"); a_.set_ylabel("ppm"); a_.set_title(name, fontsize=10)
fig.suptitle("TIC 317134140 Sector 108, EXPLORATORY post-outcome fold (frozen ephemeris; all kept cadences)", fontsize=10); fig.tight_layout(); fig.savefig(f"{E}/fold_S108.png", dpi=120); plt.close(fig)

# ---- Item 3: on-target checks (definitions of scripts/vet.py centroid_shift and pixel_depth_map; local S108 files)
mm = np.isfinite(rt) & np.isfinite(cx) & np.isfinite(cy) & np.isfinite(rf) & (rq == 0); mm[mm] &= trim_edges(rt[mm]); ct, ccx, ccy = rt[mm], cx[mm], cy[mm]
mask = transit_mask(time=ct, period=P, duration=2 * T14, T0=T0); cres = {}
for name, c in (("x", ccx), ("y", ccy)):
    tr = flatten(ct, c - c.mean() + 10, method="biweight", window_length=0.75, return_trend=True, break_tolerance=0.5, mask=mask)[1]; r = c - tr; ok = np.isfinite(r)
    ph = ((ct - T0) / P + 0.5) % 1 - 0.5; intr = ok & (np.abs(ph * P) < T14 / 2); oot = ok & (np.abs(ph * P) > T14) & (np.abs(ph * P) < 3 * T14)
    cres[name] = (float(np.mean(r[intr]) - np.mean(r[oot])), float(np.sqrt(np.var(r[intr]) / intr.sum() + np.var(r[oot]) / oot.sum())), int(intr.sum()))
out["item3_centroid_shift"] = dict(dx_mpx=cres["x"][0] * 1e3, dx_err_mpx=cres["x"][1] * 1e3, dy_mpx=cres["y"][0] * 1e3, dy_err_mpx=cres["y"][1] * 1e3, n_in=cres["x"][2],
                                   shift_mpx=float(np.hypot(cres["x"][0], cres["y"][0]) * 1e3), shift_sigma=float(np.hypot(cres["x"][0] / cres["x"][1], cres["y"][0] / cres["y"][1])),
                                   note="TOI-2514.01 transits are NOT masked here, as in the earlier per-sector values")
if not os.path.exists(TPF):
    os.makedirs(f"{E}/tpf", exist_ok=False)
    from astroquery.mast import Observations
    st, msg, _ = Observations.download_file(f"mast:TESS/product/{TPF_NAME}", local_path=TPF); assert st == "COMPLETE", (st, msg)
out["item3_tpf"] = dict(file=TPF_NAME, sha256=sha(TPF), size=os.path.getsize(TPF))
import lightkurve as lk
from scipy.ndimage import binary_dilation
tpf = lk.read(TPF, quality_bitmask="default"); pt = tpf.time.value; flux = tpf.flux.value.astype(float); ny, nx = flux.shape[1:]
good = np.isfinite(pt) & np.isfinite(flux).all(axis=(1, 2)); good[good] &= trim_edges(pt[good]); pt, flux = pt[good], flux[good]
mask = transit_mask(time=pt, period=P, duration=2 * T14, T0=T0); ph = ((pt - T0) / P + 0.5) % 1 - 0.5; intr = np.abs(ph * P) < T14 / 2; oot = (np.abs(ph * P) > T14) & (np.abs(ph * P) < 3 * T14)
depth = np.full((ny, nx), np.nan); derr = np.full((ny, nx), np.nan); mean_img = np.nanmean(flux, axis=0); ap = tpf.pipeline_mask; reg = binary_dilation(ap, iterations=2)
for j in range(ny):
    for i in range(nx):
        if not reg[j, i] or mean_img[j, i] <= 0: continue
        pl = flux[:, j, i] / mean_img[j, i]
        try: tr = flatten(pt, pl, method="biweight", window_length=0.75, return_trend=True, break_tolerance=0.5, mask=mask)[1]
        except Exception: continue
        r = pl / tr; ok = np.isfinite(r)
        if (ok & intr).sum() < 10: continue
        depth[j, i] = np.median(r[ok & oot]) - np.mean(r[ok & intr]); derr[j, i] = np.std(r[ok & oot]) / np.sqrt((ok & intr).sum())
loss = depth * mean_img; yy, xx = np.mgrid[:ny, :nx]; w = np.where(np.isfinite(loss) & (loss > 0), loss, 0); wf = np.where(reg, mean_img, 0)
lx, ly = np.sum(w * xx) / w.sum(), np.sum(w * yy) / w.sum(); ox, oy = np.sum(wf * xx) / wf.sum(), np.sum(wf * yy) / wf.sum()
rng = np.random.default_rng(0); cs = []
for _ in range(200):
    l2 = (depth + rng.standard_normal(depth.shape) * derr) * mean_img; w2 = np.where(np.isfinite(l2) & (l2 > 0), l2, 0)
    if w2.sum() > 0: cs.append((np.sum(w2 * xx) / w2.sum(), np.sum(w2 * yy) / w2.sum()))
cs = np.array(cs); px, py = tpf.wcs.all_world2pix([[tpf.ra, tpf.dec]], 0)[0]
apdepth = float(np.nansum(np.where(ap, loss, 0)) / np.nansum(np.where(ap, mean_img, 0)) * 1e6)
fig, ax = plt.subplots(1, 3, figsize=(12, 3.6))
ax[0].imshow(mean_img, origin="lower"); ax[0].set_title("mean image"); ax[1].imshow(np.where(np.isfinite(depth), depth * 1e6, np.nan), origin="lower", cmap="RdBu_r", vmin=-3e3, vmax=3e3); ax[1].set_title("per-pixel depth (ppm)")
ax[2].imshow(np.where(np.isfinite(loss), loss, np.nan), origin="lower"); ax[2].set_title("flux-loss map (depth x flux)")
for a_ in ax: a_.contour(ap, levels=[0.5], colors="w", linewidths=0.8); a_.plot(px, py, "r+", ms=12, mew=2); a_.plot(lx, ly, "cx", ms=10, mew=2); a_.plot(ox, oy, "m.", ms=8)
fig.suptitle("TIC 317134140 S108 EXPLORATORY post-outcome: red + target, magenta . flux centroid, cyan x flux-loss centroid", fontsize=9); fig.tight_layout(); fig.savefig(f"{E}/pixelmap_S108.png", dpi=120); plt.close(fig)
out["item3_pixel_map"] = dict(n_in=int(intr.sum()), n_cadences=int(len(pt)), target_px=[float(px), float(py)], flux_centroid=[float(ox), float(oy)], loss_centroid=[float(lx), float(ly)],
                              loss_centroid_err=[float(cs[:, 0].std()), float(cs[:, 1].std())], offset_loss_vs_target_px=float(np.hypot(lx - px, ly - py)), offset_loss_vs_flux_px=float(np.hypot(lx - ox, ly - oy)),
                              offset_flux_vs_target_px=float(np.hypot(ox - px, oy - py)), n_pixels_measured=int(np.isfinite(depth).sum()), n_pixels_positive_loss=int((np.isfinite(loss) & (loss > 0)).sum()),
                              aperture_flux_weighted_depth_ppm=apdepth, depth_map_ppm=np.where(np.isfinite(depth), np.round(depth * 1e6, 1), None).tolist())
json.dump(out, open(f"{E}/report.json", "w"), indent=1, default=str); print("done")
