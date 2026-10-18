"""Pixel-level blend test for FFI-only (QLP) targets using a TESScut cutout.
For each listed sector: download an NxN cutout, build a per-pixel transit depth map from local in/out-of-transit
differences (each transit uses its own +-3 duration baseline, so slow scattered-light trends cancel), locate the
flux-loss centroid, compare with the target and Gaia neighbour positions, and measure relative depth vs aperture radius.
Usage: python -I ffi_pixel_test.py TIC P T0 DUR_H --sectors 66 93 --size 11"""
import os, sys, os, json, argparse, warnings; warnings.filterwarnings("ignore"); sys.path.insert(0, "/Users/fernando/Desktop/NASA/scripts")
import numpy as np, pandas as pd, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
import lightkurve as lk
from astropy.coordinates import SkyCoord; import astropy.units as u

def gaia_list(ra, dec, radius=60):
    from astroquery.gaia import Gaia; Gaia.ROW_LIMIT = 100
    r = Gaia.cone_search_async(SkyCoord(ra, dec, unit="deg"), radius=radius * u.arcsec, table_name="gaiadr3.gaia_source").get_results().to_pandas().sort_values("dist")
    return r[["ra", "dec", "phot_g_mean_mag", "dist"]].values

def run(tic, P, T0, dur_d, sector, size, ra, dec, gaia, out):
    sr = lk.search_tesscut(f"TIC {tic}", sector=sector)
    if len(sr) == 0: print("no TESScut for sector", sector); return None
    tpf = sr.download(cutout_size=size, download_dir="/Users/fernando/Desktop/NASA/data/lk_cache")
    t = tpf.time.value; cube = tpf.flux.value  # (n, y, x) e-/s
    q = np.isfinite(cube).all(axis=(1, 2)) & np.isfinite(t) & (tpf.quality == 0)
    t, cube = t[q], cube[q]
    ph = ((t - T0) / P + 0.5) % 1 - 0.5; dt = ph * P
    intr = np.abs(dt) < dur_d / 2; oot = (np.abs(dt) > dur_d) & (np.abs(dt) < 3 * dur_d)
    # per-transit local differences
    ep = np.round((t - T0) / P).astype(int); diff = np.zeros(cube.shape[1:]); wsum = 0.0; n_ev = 0
    var = np.zeros_like(diff)
    for e in np.unique(ep):
        wi = intr & (ep == e); wo = oot & (ep == e)
        if wi.sum() < 3 or wo.sum() < 6: continue
        d = cube[wo].mean(axis=0) - cube[wi].mean(axis=0)
        s2 = cube[wo].var(axis=0) * (1 / wi.sum() + 1 / wo.sum())
        diff += d / np.maximum(s2, 1e-12); var += 1 / np.maximum(s2, 1e-12); n_ev += 1
    depth_map = diff / np.maximum(var, 1e-12); sig_map = depth_map * np.sqrt(var)
    mean_img = cube[oot].mean(axis=0)
    # positions
    ny, nx = mean_img.shape
    px_t = tpf.wcs.all_world2pix([[ra, dec]], 0)[0]  # (x, y) in cutout pixels
    gx = tpf.wcs.all_world2pix(gaia[:, :2], 0)
    # flux-loss centroid (positive depth pixels within 3 px of target)
    yy, xx = np.mgrid[0:ny, 0:nx]; near = np.hypot(xx - px_t[0], yy - px_t[1]) < 3.5
    w = np.where(near & (depth_map > 0), depth_map, 0)
    cx, cy = (w * xx).sum() / w.sum(), (w * yy).sum() / w.sum()
    # bootstrap-ish error on loss centroid via sig_map noise: perturb depth_map
    rng = np.random.default_rng(1); cs = []
    err_map = depth_map / np.where(sig_map != 0, sig_map, 1)
    for _ in range(200):
        pm = depth_map + rng.normal(size=depth_map.shape) * np.abs(err_map); wp = np.where(near & (pm > 0), pm, 0)
        cs.append(((wp * xx).sum() / wp.sum(), (wp * yy).sum() / wp.sum()))
    cs = np.array(cs); cerr = cs.std(axis=0)
    # star flux centroid in/out
    fw = mean_img; sx, sy = (fw * xx).sum() / fw.sum(), (fw * yy).sum() / fw.sum()
    # depth vs aperture radius (relative, using per-transit local baselines on summed aperture)
    rows = []
    for r_ in (1.0, 1.5, 2.0, 2.5, 3.0):
        ap = np.hypot(xx - px_t[0], yy - px_t[1]) <= r_; lc = cube[:, ap].sum(axis=1)
        num = 0.0; den = 0.0
        for e in np.unique(ep):
            wi = intr & (ep == e); wo = oot & (ep == e)
            if wi.sum() < 3 or wo.sum() < 6: continue
            base = lc[wo].mean(); d = (base - lc[wi].mean()) / base; s2 = lc[wo].var() / base ** 2 * (1 / wi.sum() + 1 / wo.sum())
            num += d / s2; den += 1 / s2
        rows.append(dict(r_px=r_, depth_ppm=float(num / den * 1e6) if den else np.nan, err_ppm=float(1e6 / np.sqrt(den)) if den else np.nan, n_pix=int(ap.sum())))
    # brightest-pixel dilution: fraction of in-aperture flux from target vs neighbours not computable w/o PSF; report neighbour list in px coords
    neigh = [dict(dx=float(g[0] - px_t[0]), dy=float(g[1] - px_t[1]), sep_px=float(np.hypot(g[0] - px_t[0], g[1] - px_t[1])), G=float(m[2])) for g, m in zip(gx, gaia)]
    res = dict(sector=int(sector), n_events=n_ev, target_px=[float(px_t[0]), float(px_t[1])], loss_centroid_px=[float(cx), float(cy)], loss_centroid_err_px=[float(cerr[0]), float(cerr[1])],
               loss_offset_px=float(np.hypot(cx - px_t[0], cy - px_t[1])), loss_offset_arcsec=float(np.hypot(cx - px_t[0], cy - px_t[1]) * 21),
               star_centroid_px=[float(sx), float(sy)], peak_sig_pixel=[int(v) for v in np.unravel_index(np.argmax(sig_map), sig_map.shape)][::-1],
               depth_vs_aperture=rows, neighbours=neigh[:10])
    # figure
    fig, ax = plt.subplots(1, 3, figsize=(15, 4.6))
    ax[0].imshow(np.log10(np.maximum(mean_img, 1)), origin="lower", cmap="gray"); ax[0].set_title(f"TIC {tic} S{sector} mean image (log)")
    im = ax[1].imshow(sig_map, origin="lower", cmap="RdBu_r", vmin=-np.nanmax(np.abs(sig_map)), vmax=np.nanmax(np.abs(sig_map))); ax[1].set_title("per-pixel transit depth significance"); plt.colorbar(im, ax=ax[1])
    for a in ax[:2]:
        a.plot(px_t[0], px_t[1], "x", color="lime", ms=12, mew=2, label="target")
        for g, m in zip(gx, gaia[:]):
            if 0 <= g[0] < nx and 0 <= g[1] < ny and m[3] * 3600 > 0.5: a.plot(g[0], g[1], "o", mfc="none", mec="orange", ms=max(2, 14 - (m[2] - gaia[0][2]) * 1.5))
        a.plot(cx, cy, "+", color="cyan", ms=14, mew=2, label="loss centroid")
    ax[0].legend(loc="upper left", fontsize=8)
    ax[2].errorbar([r["r_px"] for r in rows], [r["depth_ppm"] for r in rows], [r["err_ppm"] for r in rows], fmt="o-"); ax[2].set_xlabel("aperture radius [px]"); ax[2].set_ylabel("depth [ppm]"); ax[2].set_title("depth vs aperture")
    plt.tight_layout(); plt.savefig(f"{out}/ffi_pixel_S{sector}.png", dpi=110); plt.close()
    json.dump(res, open(f"{out}/ffi_pixel_S{sector}.json", "w"), indent=1)
    print(f"S{sector}: events={n_ev} loss-centroid offset {res['loss_offset_px']:.2f} px ({res['loss_offset_arcsec']:.1f}\") +-({cerr[0]:.2f},{cerr[1]:.2f}) px; depth vs r: " + ", ".join(f"r{r['r_px']}:{r['depth_ppm']:.0f}+-{r['err_ppm']:.0f}" for r in rows), flush=True)
    return res

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("tic", type=int); ap.add_argument("period", type=float); ap.add_argument("t0", type=float); ap.add_argument("dur_h", type=float)
    ap.add_argument("--sectors", type=int, nargs="+", required=True); ap.add_argument("--size", type=int, default=11); a = ap.parse_args()
    pool = pd.read_csv(os.environ.get("TSEARCH_PARAMS") or "/Users/fernando/Desktop/NASA/catalogs/qlp/s104_dwarf_pool.csv", usecols=["ID", "ra", "dec"], low_memory=False).set_index("ID")
    if a.tic not in pool.index: pool = pd.read_csv("/Users/fernando/Desktop/NASA/catalogs/allsky_targets.csv", usecols=["ID", "ra", "dec"]).set_index("ID")
    ra, dec = [float(x) for x in pool.loc[a.tic, ["ra", "dec"]]]
    gaia = gaia_list(ra, dec)
    out = f"/Users/fernando/Desktop/NASA/results/vet_qlp/{a.tic}"; os.makedirs(out, exist_ok=True)
    for s in a.sectors:
        try: run(a.tic, a.period, a.t0, a.dur_h / 24, s, a.size, ra, dec, gaia, out)
        except Exception as e: print("sector", s, "failed:", repr(e))
