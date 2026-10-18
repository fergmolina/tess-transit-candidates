"""All-sky 'testable soon' table. From results/candidates_physical_allsky.csv (rank.py output) keep SDE >= SDE_MIN, add
(1) period-density flag: top-peak period of ALL searched stars histogrammed in log bins; a candidate in a bin with > 2x the smooth
    expectation (median of +-5 neighbouring bins) and > 20 stars is flagged 'period_cluster';
(2) shared-time flag: number of other stars whose top-3 peak shares the period within 0.5 % AND the transit phase within one duration
    (scattered-light features are shared across stars; a planet is unique);
(3) future coverage from catalogs/allsky_tic2sectors_future.json (sectors 106-134), next sector, its orbit windows from TESS_orbit_times.csv,
    the number of predicted transits inside the windows vs in gaps, 2-min target flag (catalogs/target_lists), release deadline.
Output: results/allsky_testable_soon.csv (sorted by next sector, then clean SDE). Usage: python -I allsky_testable.py [--sde 9]"""
import os, json, glob, argparse, numpy as np, pandas as pd
ROOT = "/Users/fernando/Desktop/NASA"; R = f"{ROOT}/results"; C = f"{ROOT}/catalogs"
ap = argparse.ArgumentParser(); ap.add_argument("--sde", type=float, default=9.0); a = ap.parse_args()
top = pd.read_csv(f"{R}/ranked_top_peak_allsky.csv", low_memory=False); allp = pd.read_csv(f"{R}/ranked_all_peaks_allsky.csv", low_memory=False)
phys = pd.read_csv(f"{R}/candidates_physical_allsky.csv", low_memory=False); cand = phys[phys.sde >= a.sde].copy()
print(f"stars ranked {len(top)}; physical {len(phys)}; SDE >= {a.sde}: {len(cand)}")
# (1) period density
lp = np.log10(top.period.values); edges = np.arange(np.log10(0.5), np.log10(20.5), 0.005); h, _ = np.histogram(lp, edges)
smooth = np.array([np.median(np.r_[h[max(0, i - 5):i], h[i + 1:i + 6]]) for i in range(len(h))])
hot = (h > 2 * np.maximum(smooth, 1)) & (h > 20)
cand["period_cluster"] = [bool(hot[min(max(np.searchsorted(edges, np.log10(p)) - 1, 0), len(h) - 1)]) for p in cand.period]
print("period-cluster bins:", int(hot.sum()), "flagged candidates:", int(cand.period_cluster.sum()))
# (2) shared time
P_all = allp.period.values; T_all = allp.t0.values; tic_all = allp.tic.values; dur_all = allp.dur_h.values / 24
shared, expect = [], []
for _, r in cand.iterrows():
    m = (np.abs(P_all - r.period) / r.period < 0.005) & (tic_all != r.tic); w = max(r.dur_h / 24, 0.05)
    if m.any():
        dphi = np.abs(((T_all[m] - r.t0 + r.period / 2) % r.period) - r.period / 2); shared.append(int(np.sum(dphi < w))); expect.append(float(m.sum() * 2 * w / r.period))
    else: shared.append(0); expect.append(0.0)
cand["shared_time_n"] = shared; cand["shared_time_expected"] = np.round(expect, 2)
# chance coincidences are common at short periods (many stars within 0.5 % in period, loose phase window): flag only a clear excess
cand["shared_time_flag"] = cand.shared_time_n > np.maximum(5, 3 * cand.shared_time_expected)
# (3) future coverage
fut = json.load(open(f"{C}/allsky_tic2sectors_future.json")); fut = {int(k): [s for s in v if s <= 134] for k, v in fut.items()}
orb = pd.read_csv(f"{C}/TESS_orbit_times.csv", comment="#"); orb = orb[pd.to_numeric(orb.Sector, errors="coerce").notna()]
orb["Sector"] = orb.Sector.astype(int); orb["s"] = pd.to_datetime(orb["Start of Orbit"]).map(lambda t: t.to_julian_date() - 2457000); orb["e"] = pd.to_datetime(orb["End of Orbit"]).map(lambda t: t.to_julian_date() - 2457000)
win = {s: list(zip(g.s, g.e)) for s, g in orb.groupby("Sector")}
tl = {}
for f in glob.glob(f"{C}/target_lists/all_targets_S*_v1.csv"):
    s = int(os.path.basename(f).split("_S")[1][:3]); d = pd.read_csv(f, comment="#", header=None, usecols=[0], low_memory=False); tl[s] = set(pd.to_numeric(d[0], errors="coerce").dropna().astype(int))
def cov(r):
    fs = fut.get(int(r.tic), []); nxt = min(fs) if fs else np.nan
    if not fs: return pd.Series(dict(next_sector=np.nan, future_sectors="", n_future=0, sector_start=np.nan, sector_end=np.nan, n_transits_in_windows=np.nan, n_transits_in_gaps=np.nan, two_min=False, release_deadline=""))
    w = win.get(nxt, []); 
    if not w: return pd.Series(dict(next_sector=nxt, future_sectors=",".join(map(str, fs)), n_future=len(fs), sector_start=np.nan, sector_end=np.nan, n_transits_in_windows=np.nan, n_transits_in_gaps=np.nan, two_min=int(r.tic) in tl.get(nxt, set()), release_deadline="unknown dates"))
    s0, e0 = min(x for x, _ in w), max(y for _, y in w); n = np.arange(np.ceil((s0 - r.t0) / r.period), np.floor((e0 - r.t0) / r.period) + 1); tt = r.t0 + n * r.period
    inw = sum(any(x <= t <= y for x, y in w) for t in tt); two = int(r.tic) in tl.get(nxt, set())
    dl = pd.Timestamp("2000-01-01") + pd.to_timedelta(e0 + 2457000 - 2451544.5, "D") + pd.Timedelta(days=21 if two else 80)
    return pd.Series(dict(next_sector=nxt, future_sectors=",".join(map(str, fs)), n_future=len(fs), sector_start=round(s0, 2), sector_end=round(e0, 2), n_transits_in_windows=int(inw), n_transits_in_gaps=int(len(tt) - inw), two_min=two, release_deadline=dl.strftime("%Y-%m-%d")))
cand = pd.concat([cand, cand.apply(cov, axis=1)], axis=1)
cand["clean"] = (~cand.period_cluster) & (~cand.shared_time_flag) & (~cand.near_tess_orbit.astype(bool))
cols = ["tic", "next_sector", "n_transits_in_windows", "n_transits_in_gaps", "two_min", "release_deadline", "sde", "clean", "period_cluster", "shared_time_n", "shared_time_expected", "shared_time_flag", "near_tess_orbit", "period", "t0", "dur_h", "dur_ratio", "depth_ppm", "depth_snr", "ntr", "n_sectors", "n_years", "yrs_det", "odd_even_sig", "secondary_sig", "nsec_same", "tmag", "teff", "rad", "known_src", "future_sectors", "n_future"]
out = cand[cols].sort_values(["next_sector", "clean", "sde"], ascending=[True, False, False]); out.to_csv(f"{R}/allsky_testable_soon.csv", index=False)
soon = out[(out.next_sector <= 116)]; print(f"with a sector <= 116: {len(soon)}; clean: {int(soon.clean.sum())}; clean & >=1 transit in windows: {int((soon.clean & (soon.n_transits_in_windows >= 1)).sum())}; clean & SDE>=12 & >=1 transit: {int((soon.clean & (soon.sde >= 12) & (soon.n_transits_in_windows >= 1)).sum())}")
print(soon[soon.clean & (soon.n_transits_in_windows >= 1)].sort_values("sde", ascending=False).head(25)[["tic", "next_sector", "n_transits_in_windows", "two_min", "release_deadline", "sde", "period", "dur_h", "dur_ratio", "depth_ppm", "ntr", "n_years", "yrs_det", "tmag", "rad"]].to_string(index=False))
