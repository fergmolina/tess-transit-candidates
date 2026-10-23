"""TRICERATOPS runner v2 (2026-10-22; round-5 review R5-2/R5-3). Supersedes triceratops_qlp.py for new runs; v1 and its outputs are kept
unchanged for provenance (v1 folded EVERY cached QLP file of the TIC while recording only the three aperture sectors; audit:
results/triceratops_qlp_sector_audit_20261022.json). Changes:
- photometry and aperture sectors are explicit (--sectors, optional --phot-sectors); nothing is globbed from the cache;
- holdout guard BEFORE any file or TESScut access: every sector must be <= MAX_SECTOR (105; raise only by an explicit, logged decision)
  and the TIC must not be a registered test target listed in PROTECTED;
- each FITS is opened only by its exact expected path and checked (primary-header TICID and SECTOR) before use;
- this runner uses the same gap-edge mask function as vet.py (tsearch.trim_edges), but a separate documented photometry preparation
  (QUALITY == 0, finite positive flux, edge mask, 0.7-d masked biweight; vet.py differs: flux-error and 50 % excursion checks, 0.75-d
  window, upward-outlier clipping). Equality of retained events or depths with vet.py has NOT been established;
- the output manifest records the ephemeris values and the SHA-256 of report.json; photometry sectors with file SHA-256, points and
  in-transit points; aperture sectors requested / used / failed, with cutout paths, SHA-256 and aperture pixels (cutout SECTOR header and
  target position checked before use); the script SHA-256.
STATUS (2026-10-22, round-5 re-check C1/C1b): UNVALIDATED for new screening runs until preparation and header tests on synthetic inputs
pass and the runner is reviewed.
No contrast curve. Screening only. Usage: python -I triceratops_qlp_v2.py TIC --sectors 56 82 83 [--phot-sectors ...] [--out DIR]"""
import sys, os, json, hashlib, argparse, warnings; warnings.filterwarnings("ignore")
from pathlib import Path
R = "/Users/fernando/Desktop/NASA"; QD = f"{R}/data/qlp_allsky/"; MAX_SECTOR = 105
PROTECTED = {183374279, 120444365, 70441745, 206620592, 122522485, 253931796, 115692561, 151767028, 343298093, 188664994, 162304222,
             53825235, 3367979, 120517801, 80387959}
def qlp_path(tic, s): return f"{QD}hlsp_qlp_tess_ffi_s{s:04d}-{tic:016d}_tess_v01_llc.fits"
def guard(tic, secs):
    if tic in PROTECTED: raise SystemExit(f"refused: TIC {tic} is a registered test target")
    bad = [s for s in secs if s > MAX_SECTOR]
    if bad: raise SystemExit(f"refused: sector(s) {bad} > MAX_SECTOR {MAX_SECTOR}")
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
def out_dir(tic, out=None):
    d = Path(out) if out else Path(f"{R}/results/vet_allsky/{tic}"); d.mkdir(parents=True, exist_ok=True); return d
def load_qlp(tic, s, qd=QD):
    """Open one QLP file by its exact path after the guard; refuse on a TICID/SECTOR header mismatch."""
    from astropy.io import fits
    p = os.path.join(qd, os.path.basename(qlp_path(tic, s)))
    if not os.path.exists(p): raise SystemExit(f"missing {p}")
    h = fits.open(p); hd = h[0].header
    if int(hd["TICID"]) != tic or int(hd["SECTOR"]) != s: raise SystemExit(f"header mismatch {p}: TICID {hd['TICID']} SECTOR {hd['SECTOR']}")
    return p, h
def main(argv):
    ap = argparse.ArgumentParser(); ap.add_argument("tic", type=int); ap.add_argument("--sectors", type=int, nargs="+", required=True)
    ap.add_argument("--phot-sectors", type=int, nargs="+"); ap.add_argument("--out"); a = ap.parse_args(argv)
    phot = a.phot_sectors or a.sectors; guard(a.tic, sorted(set(a.sectors) | set(phot)))   # before any access
    import numpy as np; from astropy.io import fits; from wotan import flatten, transit_mask
    sys.path.insert(0, f"{R}/scripts"); from tsearch import trim_edges
    OUT = out_dir(a.tic, a.out); RP = f"{R}/results/vet_allsky/{a.tic}/report.json"; rep = json.load(open(RP))
    b = rep["bls_refine"]; P, T0, dur_h = b["period"], b["T0"], b["duration_h"]; ra, dec = rep["meta"]["ra"], rep["meta"]["dec"]; dur = dur_h / 24
    T, F, inputs = [], [], []
    for s in phot:
        p, h = load_qlp(a.tic, s)
        d = h[1].data; t = np.asarray(d["TIME"], float); fl = np.asarray(d["DET_FLUX"] if "DET_FLUX" in d.columns.names else d["KSPSAP_FLUX"], float)
        q = np.asarray(d["QUALITY"], int); ok = np.isfinite(t) & np.isfinite(fl) & (q == 0) & (fl > 0); t, fl = t[ok], fl[ok]
        ok = trim_edges(t); t, fl = t[ok], fl[ok]
        fl = fl / np.nanmedian(fl); m = transit_mask(time=t, period=P, duration=2 * dur, T0=T0)
        f2 = flatten(t, fl, method="biweight", window_length=0.7, mask=m, break_tolerance=0.5); ok = np.isfinite(f2)
        ph = ((t[ok] - T0) / P + 0.5) % 1 - 0.5; nin = int(np.sum(np.abs(ph * P * 24) < dur_h / 2))
        inputs.append(dict(sector=s, file=os.path.relpath(p, R), sha256=sha(p), n_points=int(ok.sum()), n_in_transit=nin)); T.append(t[ok]); F.append(f2[ok])
        print("photometry", inputs[-1], flush=True)
    T = np.concatenate(T); F = np.concatenate(F); ph = ((T - T0) / P + 0.5) % 1 - 0.5; sel = np.abs(ph * P * 24) < 6
    tb = np.round(ph[sel] * P / (10 / 1440)) * (10 / 1440); u = np.unique(tb); fb = np.array([np.mean(F[sel][tb == x]) for x in u])
    eb = np.array([np.std(F[sel][tb == x]) / np.sqrt(np.sum(tb == x)) for x in u]); depth = 1 - np.mean(fb[np.abs(u * 24) < dur_h / 4])
    print("folded bins", len(u), "depth", depth * 1e6, "ppm", flush=True)
    import lightkurve as lk; from astropy.wcs import WCS; from triceratops import triceratops as tr
    aps, use, failed, cutouts = [], [], [], []
    for s in a.sectors:
        try: tpf = lk.search_tesscut(f"TIC {a.tic}", sector=s).download(cutout_size=15, download_dir=f"{R}/data/lk_cache")
        except Exception as e: print("tesscut fail", s, e, flush=True); failed.append(dict(sector=s, reason=repr(e)[:200])); continue
        h = fits.open(tpf.path); hd = h[1].header; c0 = hd["1CRV4P"]; r0 = hd["2CRV4P"]; w = WCS(h[2].header); px = w.all_world2pix([[ra, dec]], 0)[0]
        sec_h = int(h[0].header.get("SECTOR", -1))
        if sec_h != s or not (5 <= px[0] <= 9 and 5 <= px[1] <= 9):
            failed.append(dict(sector=s, reason=f"cutout check failed: SECTOR {sec_h}, target px {px.tolist()}")); continue
        yy, xx = np.mgrid[0:15, 0:15]; apm = np.hypot(xx - px[0], yy - px[1]) <= 2.5
        pix = [[int(c), int(r)] for c, r in zip(xx[apm] + c0, yy[apm] + r0)]
        aps.append(np.array(pix)); use.append(s); cutouts.append(dict(sector=s, path=os.path.relpath(tpf.path, R), sha256=sha(tpf.path), target_px=px.tolist(), aperture_pixels=pix))
    target = tr.target(ID=a.tic, sectors=np.array(use)); target.calc_depths(tdepth=depth, all_ap_pixels=aps)
    target.stars.to_csv(OUT / "triceratops_v2_stars.csv", index=False)
    target.calc_probs(time=u, flux_0=fb, flux_err_0=float(np.median(eb)), P_orb=P, parallel=True, drop_scenario=[], verbose=1)
    target.probs.to_csv(OUT / "triceratops_v2_probs.csv", index=False)
    json.dump(dict(tic=a.tic, FPP=float(target.FPP), NFPP=float(target.NFPP), depth_used=float(depth), photometry_sectors=phot,
                   aperture_sectors_requested=a.sectors, aperture_sectors=use, aperture_failed=failed, cutouts=cutouts,
                   ephemeris=dict(P=P, T0=T0, duration_h=dur_h, ra=ra, dec=dec, source=os.path.relpath(RP, R), source_sha256=sha(RP)),
                   inputs=inputs, script="scripts/triceratops_qlp_v2.py", script_sha256=sha(os.path.abspath(__file__)),
                   note="2.5-px circular aperture from TESScut WCS; QLP DET_FLUX, vet.py edge rule, masked 0.7-d biweight fold; no contrast curve; screening only"),
              open(OUT / "triceratops_v2.json", "w"), indent=1)
if __name__ == "__main__": main(sys.argv[1:])
