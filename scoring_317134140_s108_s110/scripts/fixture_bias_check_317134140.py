"""Small idealized fixture check of the TIC 317134140 clause-A depth statistic (2026-10-24; DECISIONS 176(3), 179; review G5). Artificial
SPOC-format fixtures only (2000 ppm white noise, 185 ppm 1.5-h boxes at the frozen S108/S109/S110 predicted times, one 1-d mid-sector
gap), 8 seeds per sector, processed by the locked scorer's own preprocess() and clause_a(). Scope: it can show a gross bias of the
statistic in idealized data; it does NOT establish unbiased real-data depths or calibrated false-FAIL/PASS rates (no red noise, no
systematics). Usage: python -I fixture_bias_check_317134140.py TMPDIR OUT.json   (TMPDIR must not exist)"""
import sys, os, csv, json, hashlib, numpy as np, warnings; warnings.filterwarnings("ignore")
R = "/Users/fernando/Desktop/NASA"; sys.path.insert(0, f"{R}/scripts"); import prereg_spoc_317134140 as S
from astropy.io import fits
D, OUT = sys.argv[1], sys.argv[2]
if os.path.exists(D) or os.path.exists(OUT): raise SystemExit("refused: output exists")
os.makedirs(D); pred = f"{R}/results/vet/317134140/predicted_transits_S108_S109_S110.csv"; rows = []
for sec in (108, 109, 110):
    tcs = np.array([float(r["tc_BJD_TDB"]) - 2457000 for r in csv.DictReader(open(pred)) if int(r["sector"]) == sec])
    for seed in range(8):
        rng = np.random.default_rng(1000 + seed); t = np.arange(tcs.min() - 1, tcs.max() + 1, 2 / 1440); t = t[np.abs(t - t.mean()) > 0.5]
        f = 1 + rng.normal(0, 2000e-6, len(t))
        for tc in tcs: f[np.abs(t - tc) < 1.5 / 48] -= 185e-6
        p = f"{D}/s{sec}_{seed}.fits"; h0 = fits.PrimaryHDU(); h0.header.update(ORIGIN="NASA/Ames", TICID=317134140, SECTOR=sec)
        h1 = fits.BinTableHDU.from_columns([fits.Column(name="TIME", format="D", array=t), fits.Column(name="PDCSAP_FLUX", format="E", array=f * 1000),
             fits.Column(name="PDCSAP_FLUX_ERR", format="E", array=np.full(len(t), 2.0)), fits.Column(name="QUALITY", format="J", array=np.zeros(len(t), int))])
        fits.HDUList([h0, h1]).writeto(p); tt, ff, ee, m = S.preprocess(p); a = S.clause_a(tt, ff, list(tcs))
        rows.append(dict(sector=sec, seed=1000 + seed, depth_ppm=a["depth_ppm"], sigma_ppm=a["sigma_ppm"], n_eligible=a["n_eligible"], clause_a=a["clause_a"]))
summ = {}
for sec in (108, 109, 110):
    d = np.array([r["depth_ppm"] for r in rows if r["sector"] == sec]); s = np.array([r["sigma_ppm"] for r in rows if r["sector"] == sec])
    summ[sec] = dict(mean_depth_ppm=float(d.mean()), seed_scatter_ppm=float(d.std(ddof=1)), mean_quoted_sigma_ppm=float(s.mean()), mean_offset_in_standard_errors=float((d.mean() - 185) / (d.std(ddof=1) / np.sqrt(len(d)))))
json.dump(dict(scorer_sha256=hashlib.sha256(open(f"{R}/scripts/prereg_spoc_317134140.py", "rb").read()).hexdigest(), injected_ppm=185.0, noise_ppm=2000.0,
               scope="idealized white-noise fixtures; no bias detected here does not establish unbiased real-data depths or calibrated error rates", per_seed=rows, summary=summ),
          open(OUT, "w"), indent=1)
for k, v in summ.items(): print(k, {kk: round(vv, 1) for kk, vv in v.items()})
