"""Rank search results; cross-match against known signals (TOI/CTOI/confirmed/TCE) by TIC and by period (incl. 2x, 0.5x aliases)."""
import json, glob, os, numpy as np, pandas as pd
import os
SOURCE = os.environ.get("TSEARCH_SOURCE", "spoc")
R = "/Users/fernando/Desktop/NASA/results"; B = "/Users/fernando/Desktop/NASA/catalogs"
SEARCH_DIR = os.environ.get("TSEARCH_OUT") or (f"{R}/search" if SOURCE == "spoc" else f"{R}/search_qlp")
SUFFIX = os.environ.get("TSEARCH_SUFFIX", "" if SOURCE == "spoc" else "_qlp")
known = pd.read_csv(f"{B}/known_signals.csv", low_memory=False)
tp = pd.read_csv(os.environ.get("TSEARCH_PARAMS") or (f"{B}/s107_multiyear_tic_params.csv" if SOURCE == "spoc" else f"{B}/qlp/s104_dwarf_pool.csv"), low_memory=False).set_index("ID")
def expected_duration_h(P, tic):
    """Central-transit duration for circular orbit: T = (P/pi) * asin(R*/a) ~ 13 h (P/365)^(1/3) rho^(-1/3) ; rho in solar units."""
    r = tp.loc[tic] if tic in tp.index else None
    if r is None or not np.isfinite(r.get("rad", np.nan)): return np.nan
    R = r["rad"]; M = r["mass"] if np.isfinite(r.get("mass", np.nan)) else (R if R < 0.7 else R**1.25)
    rho = M / R**3
    return 13.0 * (P / 365.25) ** (1 / 3) * rho ** (-1 / 3)
known_by_tic = {t: g for t, g in known.groupby("tic")}
def match_known(tic, P, tol=0.01):
    g = known_by_tic.get(tic)
    if g is None: return "", ""
    tags = []
    for _, r in g.iterrows():
        kp = r["period"]
        if pd.isna(kp) or kp <= 0: continue
        for mult, lab in ((1, ""), (2, "x2"), (0.5, "x0.5"), (3, "x3"), (1/3, "x1/3")):
            if abs(P * mult - kp) / kp < tol: tags.append(f"{r['source']}{lab}:{kp:.4f}")
    return ";".join(sorted(set(g["source"].str.split(":").str[0]))), ";".join(tags)
rows = []
for f in glob.glob(f"{SEARCH_DIR}/*.json"):
    d = json.load(open(f)); tic = d["tic"]
    st = d["stitched"]; m = d["meta"]
    for rank, p in enumerate(st["peaks"][:3]):
        py = st["per_year"] if rank == 0 else {}
        yrs_det = sum(1 for v in py.values() if v["depth"] / v["err"] > 2.5)
        oe = abs(p["depth_odd"] - p["depth_even"]) / np.hypot(p["depth_odd_err"], p["depth_even_err"]) if p["depth_odd_err"] > 0 else np.nan
        # astropy: depth_phased = depth of a model shifted by half a period (secondary eclipse); depth_half = model at P/2 (NOT secondary)
        sec_sig = p["depth_phased"] / p["depth_err"] if p["depth_err"] > 0 else np.nan
        halfP_sig = p["depth_half"] / p["depth_half_err"] if p["depth_half_err"] > 0 else np.nan
        # how many individual sectors show the same period among their top-3 peaks (within 1% or alias)
        nsec_same = 0
        for s, v in d["sectors"].items():
            for q in v["peaks"]:
                if any(abs(q["period"] * k - p["period"]) / p["period"] < 0.01 for k in (1, 2, 0.5, 3, 1/3)): nsec_same += 1; break
        src, ptag = match_known(tic, p["period"])
        dur_exp = expected_duration_h(p["period"], tic)
        near_orbit = min(abs(p["period"] - 13.7 * k) for k in (0.5, 1, 1.5)) < 0.8
        rows.append(dict(tic=tic, rank=rank, period=p["period"], t0=p["t0"], dur_h=p["duration_h"], depth_ppm=p["depth"] * 1e6,
                         depth_snr=p["depth"] / p["depth_err"] if p["depth_err"] > 0 else np.nan, snr=p["snr"], sde=p["sde"], ntr=p["n_transits"],
                         odd_even_sig=oe, secondary_sig=sec_sig, secondary_ppm=p["depth_phased"] * 1e6, halfP_sig=halfP_sig, nsec_same=nsec_same, n_sectors=d["n_sectors"], years=",".join(map(str, st["years"])),
                         n_years=len(st["years"]), yrs_det=yrs_det, per_year=json.dumps(py) if rank == 0 else "",
                         dur_exp_h=dur_exp, dur_ratio=p["duration_h"] / dur_exp if dur_exp and np.isfinite(dur_exp) else np.nan, near_tess_orbit=near_orbit,
                         rms_ppm=st["rms_ppm"], tmag=m["tmag"], teff=m["teff"], rad=m["rad"], crowdsap=m["crowdsap"],
                         known_src=src, known_period_match=ptag))
df = pd.DataFrame(rows)
df.to_csv(f"{R}/ranked_all_peaks{SUFFIX}.csv", index=False)
top = df[df["rank"] == 0].sort_values("sde", ascending=False)
top.to_csv(f"{R}/ranked_top_peak{SUFFIX}.csv", index=False)
print("targets processed:", top.tic.nunique())
print("SDE percentiles (top peak):", np.percentile(top.sde, [50, 90, 99, 100]).round(1))
phys = top[(top.ntr >= 3) & (top.known_period_match == "") & (top.secondary_sig.abs() < 3) & (top.odd_even_sig < 5) & ((top.dur_ratio < 1.6) | top.dur_ratio.isna()) & (top.depth_ppm < 30000)]
phys = phys.sort_values("sde", ascending=False)
phys.to_csv(f"{R}/candidates_physical{SUFFIX}.csv", index=False)
cand = phys[(phys.sde > 9) & (phys.yrs_det >= 2)]
print("after physical filters (ntr>=3, secondary<3sig, odd/even<5sig, dur<=1.6x expected, depth<3%, not known-period):", len(phys), " of which SDE>9:", len(cand))
pd.set_option("display.width", 250)
print(cand[["tic", "period", "depth_ppm", "dur_h", "dur_ratio", "snr", "sde", "ntr", "odd_even_sig", "secondary_sig", "secondary_ppm", "nsec_same", "n_years", "yrs_det", "near_tess_orbit", "tmag", "teff", "rad", "known_src"]].head(40).round(3).to_string())
print("\nKnown TOI/CTOI/CONF among top-peak hits with matching period (pipeline sanity):")
k = top[top.known_period_match.str.contains("TOI|CONF|CTOI", na=False)]
print(k[["tic", "period", "depth_ppm", "sde", "snr", "ntr", "known_period_match"]].head(20).to_string())
print("recovered known TOI/CTOI/CONF periods:", len(k), "of", top.known_src.str.contains("TOI|CONF|CTOI", na=False).sum(), "known hosts in set")
