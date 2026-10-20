"""Referee M4 (v2: fake windows now carry an INJECTED transit of the real depth, as Bryson et al. 2013 / Twicken et al. 2018 prescribe; pure-noise windows overstate the error): empirical calibration of the flux-loss-centroid error for TIC 89247735. For each sector, the same estimator as
ffi_pixel_test.py (per-event local in/out differences, positive-depth pixels within 3.5 px, flux-weighted centroid) is applied to N
fake 'transit' windows at random out-of-transit times (same duration, same per-window baseline rule) on the cached TESScut cube; the
scatter of the fake-window centroids about the target is the per-epoch error. Also computes, in the same image frame, the real
loss-minus-star vector and compares it with the catalogue neighbour-minus-target vector (WCS-independent formulation).
Output: results/vet_qlp/89247735/pixel_calib.json"""
import sys, os, json, warnings; warnings.filterwarnings("ignore"); sys.path.insert(0, "/Users/fernando/Desktop/NASA/scripts")
import numpy as np, lightkurve as lk
def load_cached_tpf(sector):
    """Use the TESScut cutout already on disk (lightkurve cache) instead of querying MAST, which hung for 6 h on 2026-10-19."""
    import glob, lightkurve as lk
    fs = glob.glob(f"/Users/fernando/Desktop/NASA/data/lk_cache/tesscut/tess-s{sector:04d}-*_275.22*_-45.56*_11x11_astrocut.fits")
    if fs: return lk.TessTargetPixelFile(fs[0])
    return lk.search_tesscut(f"TIC 89247735", sector=sector).download(cutout_size=11, download_dir="/Users/fernando/Desktop/NASA/data/lk_cache")

TIC, RA, DEC = 89247735, 275.223692413, -45.5611672045; NB_RA, NB_DEC = None, None
v3 = json.load(open("/Users/fernando/Desktop/NASA/results/vet_qlp/89247735/final_ephemeris_v3.json")); P, T0 = v3["P_d"], v3["T0_btjd"]; dur_d = 4.0 / 24
rep = json.load(open("/Users/fernando/Desktop/NASA/results/vet_qlp/89247735/report.json")); nb = [g for g in rep["gaia_neighbours"] if abs(g["G"] - 15.49) < 0.05][0]
# neighbour coordinates: Gaia query by source id
from astroquery.gaia import Gaia
r = Gaia.launch_job(f"SELECT ra, dec, pmra, pmdec FROM gaiadr3.gaia_source WHERE source_id = {nb['source_id']}").get_results(); NB_RA, NB_DEC = float(r["ra"][0]), float(r["dec"][0])
tg = Gaia.launch_job(f"SELECT ra, dec, pmra, pmdec, ref_epoch FROM gaiadr3.gaia_source WHERE source_id = 6708071581514074368").get_results(); TRA, TDEC, PMRA, PMDEC = float(tg["ra"][0]), float(tg["dec"][0]), float(tg["pmra"][0]), float(tg["pmdec"][0])
def centroid(cube, t, windows, px_t):
    ny, nx = cube.shape[1:]; yy, xx = np.mgrid[0:ny, 0:nx]; near = np.hypot(xx - px_t[0], yy - px_t[1]) < 3.5; diff = np.zeros((ny, nx)); var = np.zeros((ny, nx)); n = 0
    for tc in windows:
        dt = t - tc; wi = np.abs(dt) < dur_d / 2; wo = (np.abs(dt) > dur_d) & (np.abs(dt) < 3 * dur_d)
        if wi.sum() < 3 or wo.sum() < 6: continue
        d = cube[wo].mean(axis=0) - cube[wi].mean(axis=0); s2 = cube[wo].var(axis=0) * (1 / wi.sum() + 1 / wo.sum()); diff += d / np.maximum(s2, 1e-12); var += 1 / np.maximum(s2, 1e-12); n += 1
    if n == 0: return None
    dm = diff / np.maximum(var, 1e-12); w = np.where(near & (dm > 0), dm, 0)
    if w.sum() <= 0: return None
    return np.array([(w * xx).sum() / w.sum(), (w * yy).sum() / w.sum()]), n
out = {}
for sec in (66, 93, 104):
    tpf = load_cached_tpf(sec)
    t = tpf.time.value; cube = tpf.flux.value; q = np.isfinite(cube).all(axis=(1, 2)) & np.isfinite(t) & (tpf.quality == 0); t, cube = t[q], cube[q]
    yrs = (np.mean(t) + 2457000 - 2451545.0) / 365.25 + 2000 - 2016.0   # years since Gaia DR3 epoch 2016.0
    ra_pm = TRA + PMRA / 3.6e6 * yrs / np.cos(np.radians(TDEC)); dec_pm = TDEC + PMDEC / 3.6e6 * yrs
    px_t = tpf.wcs.all_world2pix([[ra_pm, dec_pm]], 0)[0]; px_n = tpf.wcs.all_world2pix([[NB_RA, NB_DEC]], 0)[0]
    mean_img = cube.mean(axis=0); ny, nx = mean_img.shape; yy, xx = np.mgrid[0:ny, 0:nx]; near = np.hypot(xx - px_t[0], yy - px_t[1]) < 3.5
    fw = np.where(near, mean_img, 0); star = np.array([(fw * xx).sum() / fw.sum(), (fw * yy).sum() / fw.sum()])
    ep = np.round((t - T0) / P); real_w = sorted(set(T0 + e * P for e in ep if np.any(np.abs(t - (T0 + e * P)) < dur_d / 2)))
    real = centroid(cube, t, real_w, px_t)
    depth = 0.0110 * 0.787   # 1.1 % of the target = 0.87 % of the aperture light; injected as a loss of the whole image scaled (target-dominated PSF)
    # fake windows: random times at least 1.5 d from any real transit, fully covered
    rng = np.random.default_rng(sec); fakes = []
    cand = rng.uniform(t.min() + 0.6, t.max() - 0.6, 3000)
    for tc in cand:
        if min(abs(tc - rw) for rw in real_w) < 1.5: continue
        if np.sum(np.abs(t - tc) < dur_d / 2) < 40 or np.sum((np.abs(t - tc) > dur_d) & (np.abs(t - tc) < 3 * dur_d)) < 120: continue
        # inject the real signal (fractional loss `depth` of the target's light, approximated by the mean image which the target dominates)
        wi = np.abs(t - tc) < dur_d / 2; cube_f = cube.copy(); cube_f[wi] = cube_f[wi] - depth * mean_img[None, :, :]
        c = centroid(cube_f, t, [tc], px_t)
        if c: fakes.append(c[0] - px_t)
        if len(fakes) >= 60: break
    fakes = np.array(fakes); scat = fakes.std(axis=0); rad = np.sqrt(np.mean(np.sum(fakes ** 2, axis=1)))
    v_loss = real[0] - star; v_nb = px_n - px_t; proj = np.dot(v_loss, v_nb) / np.linalg.norm(v_nb); dist_nb = np.linalg.norm(v_loss - v_nb); dist_t = np.linalg.norm(v_loss)
    out[f"S{sec}"] = dict(n_real_events=real[1], target_px_pm=px_t.tolist(), star_centroid_px=star.tolist(), neighbour_px=px_n.tolist(), loss_centroid_px=real[0].tolist(), loss_minus_star_px=v_loss.tolist(), neighbour_minus_target_px=v_nb.tolist(), sep_px=float(np.linalg.norm(v_nb)),
                          proj_toward_neighbour_px=float(proj), dist_to_neighbour_px=float(dist_nb), dist_to_target_px=float(dist_t), n_fake=int(len(fakes)), fake_scatter_xy_px=scat.tolist(), fake_rms_radius_px=float(rad), sigma_per_event_px=float(rad / np.sqrt(real[1])) if real[1] else None,
                          dist_to_neighbour_sigma=float(dist_nb / (rad / np.sqrt(max(real[1], 1)))), dist_to_target_sigma=float(dist_t / (rad / np.sqrt(max(real[1], 1)))))
    print(sec, json.dumps(out[f"S{sec}"]), flush=True)
json.dump(out, open("/Users/fernando/Desktop/NASA/results/vet_qlp/89247735/pixel_calib.json", "w"), indent=1); print("done")
