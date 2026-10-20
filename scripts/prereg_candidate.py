"""LEGACY (v1 generator; refuses new freezes since 2026-10-20, re-check N5; historical rules kept for provenance). Pre-registered transit predictions for an all-sky candidate (generic; first written for TIC 30832104, later rejected).
Transit times: (a) QLP S35/S36/S62/S89 per-transit times from results/vet_allsky/30832104/report.json (vet.py, fixed MCMC shape);
(b) SPOC 2-min S8/S9 (2019) events re-timed here with the same shape on a 0.5-min grid with a local linear baseline (lightkurve cache).
Weighted linear ephemeris (errors rescaled to reduced chi2 >= 1) -> predictions for Sectors 110 and 111 (orbit windows from
catalogs/TESS_orbit_times.csv) and through 2027; CSV + SHA-256 + PREREGISTRATION.md in results/vet_allsky/30832104/.
Usage: python -I prereg_candidate.py TIC [--freeze] [--no-2min] [--depth-ppm D] [--desc "text"]"""
import os, sys, json, hashlib, datetime, argparse, numpy as np, pandas as pd; sys.path.insert(0, "/Users/fernando/Desktop/NASA/scripts"); os.environ["TSEARCH_SOURCE"] = "qlp"
import lightkurve as lk; from wotan import flatten, transit_mask; from astropy.time import Time

def geocentric_utc(jd_tdb, ra_deg, dec_deg):
    """UTC of arrival at the geocentre: BJD_TDB minus the barycentric light-travel time toward the target (referee finding 2026-10-19:
    Time(jd, scale='tdb').utc alone only changes the time SCALE and is off by up to +-8 min)."""
    from astropy.coordinates import SkyCoord, EarthLocation; import astropy.units as u
    t = Time(jd_tdb, format="jd", scale="tdb"); ltt = t.light_travel_time(SkyCoord(ra_deg, dec_deg, unit="deg"), kind="barycentric", location=EarthLocation.from_geocentric(0, 0, 0, unit=u.m))
    return (t - ltt).utc
from vet import transit_model
ap = argparse.ArgumentParser(); ap.add_argument("tic", type=int); ap.add_argument("--freeze", action="store_true"); ap.add_argument("--no-2min", action="store_true"); ap.add_argument("--depth-ppm", type=float, default=0); ap.add_argument("--desc", default=""); ap.add_argument("--unreleased-sectors", default="", help="comma list of sectors already observed whose data are not yet public (checked today)"); a = ap.parse_args()
if a.freeze: raise SystemExit("prereg_candidate.py is the LEGACY v1 generator (historical rules and wording, kept for provenance); it refuses new freezes since v1.12-1. Use prereg_v2.py with a new --version.")   # re-check N5
TIC = a.tic; OUT = f"/Users/fernando/Desktop/NASA/results/vet_allsky/{TIC}"; rep = json.load(open(f"{OUT}/report.json")); RA_DEG, DEC_DEG = rep["meta"]["ra"], rep["meta"]["dec"]
P0, T00 = rep["ephemeris"]["P"], rep["ephemeris"]["T0"]; rprs, ars, b = rep["shape_mcmc"]["median"][1:4]; dur_d = rep["bls_refine"]["duration_h"] / 24
times = [(x["epoch"], x["tc"], x["tc_err"], f"S{x['sector']} QLP") for x in rep["transit_times"] if x["dchi2"] > 4]
# 2019 SPOC 2-min events
lcs = []
if not a.no_2min:
    sr = lk.search_lightcurve(f"TIC {TIC}", author="SPOC", exptime=120); lcs = sr.download_all(download_dir="/Users/fernando/Desktop/NASA/data/lk_cache") if len(sr) else []
for lc in (lcs or []):
    lc = lc.remove_nans().normalize(); q = lc.quality == 0; t = lc.time.value[q]; f = lc.flux.value[q]; sec = int(lc.sector)
    m = transit_mask(time=t, period=P0, duration=2 * dur_d, T0=T00); fl = flatten(t, f, method="biweight", window_length=0.7, mask=m); ok = np.isfinite(fl); t, fl = t[ok], fl[ok]
    for ep in range(int(np.floor((t.min() - T00) / P0)) - 1, int(np.ceil((t.max() - T00) / P0)) + 2):
        tc0 = T00 + ep * P0; w = np.abs(t - tc0) < 2.5 * dur_d
        if w.sum() < 100 or (np.abs(t[w] - tc0) < dur_d / 2).sum() < 30: continue
        t_, f_ = t[w], fl[w]; oot = np.abs(t_ - tc0) > 0.75 * dur_d; sig = 1.4826 * np.median(np.abs(f_[oot] - np.median(f_[oot])))
        grid = tc0 + np.linspace(-0.1, 0.1, 577); chi = np.empty(len(grid))
        for i, g in enumerate(grid):
            mm = transit_model([g, rprs, ars, b], t_, P0); A = np.vstack([mm, mm * (t_ - tc0)]).T; c, *_ = np.linalg.lstsq(A, f_, rcond=None); chi[i] = np.sum(((f_ - A @ c) / sig) ** 2)
        i = int(np.argmin(chi)); dof = len(t_) - 3; scale = max(1.0, chi[i] / dof); okk = chi < chi[i] + scale; err = max((grid[okk].max() - grid[okk].min()) / 2, (grid[1] - grid[0]) / 2)
        dchi2 = float(np.sum(((f_ - np.median(f_)) / sig) ** 2) - chi[i])
        mm = transit_model([grid[i], rprs, ars, b], t_, P0); A = np.vstack([mm, mm * (t_ - tc0)]).T; c, *_ = np.linalg.lstsq(A, f_, rcond=None); base = A @ c / mm; intr = np.abs(t_ - grid[i]) < dur_d / 2 * 0.8; depth = 1 - np.mean(f_[intr] / base[intr])
        print(f"S{sec} 2-min epoch {ep}: tc={grid[i]:.5f} +- {err*1440:.1f} min depth {depth*1e6:.0f} ppm dchi2 {dchi2:.0f} n={len(t_)}")
        if dchi2 > 9 and err * 1440 < 60: times.append((ep, float(grid[i]), float(err), f"S{sec} SPOC 2-min"))
times.sort(); e = np.array([x[0] for x in times], float); tc = np.array([x[1] for x in times]); er = np.array([x[2] for x in times])
e0 = int(e[-1]); E = e - e0; A = np.vstack([np.ones_like(E), E]).T; W = np.diag(1 / er ** 2); cov = np.linalg.inv(A.T @ W @ A); beta = cov @ A.T @ W @ tc
res = tc - A @ beta; chi2 = float(np.sum(res ** 2 / er ** 2)); dof = len(tc) - 2; infl = max(1, np.sqrt(chi2 / dof)); cov *= infl ** 2; T0, P = beta; T0e, Pe = np.sqrt(np.diag(cov))
print(f"\n{len(tc)} transit times; ephemeris (epoch ref {e0}): T0 = BTJD {T0:.5f} +- {T0e*1440:.1f} min, P = {P:.6f} +- {Pe:.6f} d; chi2/dof {chi2:.1f}/{dof}; inflation {infl:.2f}")
for (ep, t, s, src), r in zip(times, res): print(f"  epoch {ep:4d} {src:16s} O-C {r*1440:+6.1f} +- {s*1440:4.1f} min")
orb = pd.read_csv("/Users/fernando/Desktop/NASA/catalogs/TESS_orbit_times.csv", comment="#"); orb = orb[pd.to_numeric(orb.Sector, errors="coerce").notna()]; orb["Sector"] = orb.Sector.astype(int)
orb["s"] = pd.to_datetime(orb["Start of Orbit"]).map(lambda x: x.to_julian_date() - 2457000); orb["e"] = pd.to_datetime(orb["End of Orbit"]).map(lambda x: x.to_julian_date() - 2457000)
win = {s: list(zip(g.s, g.e)) for s, g in orb.groupby("Sector")}
# sectors beyond the orbit-times table: whole sector span from the MIT Year-9 table (orbit gap unknown; flagged in the CSV)
sd = pd.read_csv("/Users/fernando/Desktop/NASA/catalogs/TESS_sector_dates_future.csv"); approx = set(); approx_win = set()
for _, r in sd.iterrows():
    s0, e1 = pd.Timestamp(r.start).to_julian_date() - 2457000, pd.Timestamp(r.end).to_julian_date() + 1 - 2457000
    if int(r.Sector) not in win: win[int(r.Sector)] = [(s0, e1)]; approx.add(int(r.Sector)); approx_win.add((s0, e1))
    elif max(y for _, y in win[int(r.Sector)]) < e1 - 3: w2 = (max(y for _, y in win[int(r.Sector)]) + 0.2, e1); win[int(r.Sector)].append(w2); approx_win.add(w2)   # orbit table ends mid-sector
fut = json.load(open("/Users/fernando/Desktop/NASA/catalogs/allsky_tic2sectors_future.json")).get(str(TIC), []); fut = [x for x in fut if x <= 134]
win = {s: w for s, w in win.items() if s in fut}   # only sectors in which tess-point says the star is on silicon
print("future sectors for this star:", fut)
freeze = Time(datetime.datetime.now(datetime.UTC)); rows = []; unrel = {int(x) for x in a.unreleased_sectors.split(",") if x.strip()}
for k in range(1, 130):
    t = T0 + k * P; sig = np.sqrt(cov[0, 0] + k * k * cov[1, 1] + 2 * k * cov[0, 1]); jd = t + 2457000
    if jd > 2461900: break
    sec = next((s for s, ws in win.items() if any(x <= t <= y for x, y in ws)), None); isapprox = any((x, y) in approx_win for ws in win.values() for x, y in ws if x <= t <= y); insec = next((s for s, ws in win.items() if min(x for x, _ in ws) <= t <= max(y for _, y in ws)), None)
    rows.append(dict(epoch=e0 + k, tc_btjd=round(t, 5), tc_bjd_tdb=round(jd, 5), utc=geocentric_utc(jd, RA_DEG, DEC_DEG).iso[:16], utc_tdb_scale_only=Time(jd, format="jd", scale="tdb").utc.iso[:16], sigma_min=round(sig * 1440, 1), tess_sector=(f"{sec} (span only, gap unknown)" if isapprox else sec) if sec else (f"{insec} (gap)" if insec else ""), status=("prediction (sector observed, data not public at freeze)" if (sec in unrel or insec in unrel) else ("retrodiction: before freeze, untested" if jd < freeze.jd else "prediction"))))
df = pd.DataFrame(rows); csv = f"{OUT}/predicted_transits_2026_2027.csv"
# v1.12 (review F14): never overwrite a frozen v1; a run without --freeze writes only to OUT/_dryrun/
if os.path.exists(f"{OUT}/PREREGISTRATION.md") or (a.freeze and os.path.exists(csv)): raise SystemExit(f"refused: v1 of TIC {TIC} is already frozen; use prereg_v2.py with a new --version")
if not a.freeze: os.makedirs(f"{OUT}/_dryrun", exist_ok=True); csv = f"{OUT}/_dryrun/predicted_transits_2026_2027.csv"
df.to_csv(csv, index=False); sha = hashlib.sha256(open(csv, "rb").read()).hexdigest(); stamp = freeze.utc.iso[:19] + " UTC"
print(df[df.status.str.startswith("prediction") & df.tess_sector.astype(str).str.match(r"^\d+")].to_string(index=False)); print("SHA-256", sha, "frozen", stamp)
json.dump(dict(tic=TIC, T0_btjd=T0, T0_err_d=T0e, P_d=P, P_err_d=Pe, epoch_ref=e0, chi2=chi2, dof=dof, inflation=infl, transit_times=[dict(epoch=int(x[0]), tc=x[1], tc_err=x[2], source=x[3], oc_min=float(r * 1440)) for x, r in zip(times, res)], sha256_csv=sha, frozen=stamp), open(f"{OUT}/" + ("" if a.freeze else "_dryrun/") + "final_ephemeris.json", "w"), indent=1)
if a.freeze:
    s110 = df[df.status.str.startswith("prediction") & df.tess_sector.astype(str).str.match(r"^\d+")]
    open(f"{OUT}/PREREGISTRATION.md", "w").write(f"""# Pre-registered transit predictions - TIC {TIC} (all-sky QLP search candidate)
Frozen: {stamp}. Author: Fernando Molina (Independent researcher, ORCID 0009-0002-2872-3406). Analysis with Claude (Anthropic) under the author's direction.
Signal: P = {P:.6f} +- {Pe:.6f} d, T0 = BTJD {T0:.5f} +- {T0e*1440:.1f} min (epoch {e0}), depth {rep["bls_refine"]["depth_ppm"]:.0f} +- {rep["bls_refine"]["depth_err_ppm"]:.0f} ppm (QLP, masked detrend), duration {rep["bls_refine"]["duration_h"]:.1f} h,
Rp ~ {rep["planet"]["Rp_Rearth"]:.1f} R_Earth if on the target (Tmag {rep["meta"]["tmag"]}, Teff {rep["meta"]["teff"]} K, R {rep["meta"]["rad"]:.2f} Rsun). Sectors with timed transits: {sorted(set(x[3] for x in times))}. {a.desc}
Ephemeris from {len(tc)} transit times (chi2/dof {chi2:.1f}/{dof}; errors inflated x{infl:.2f}). SHA-256 of predicted_transits_2026_2027.csv: {sha}
**Test of record: the next TESS sector(s) listed below.** Predicted mid-transits in science-orbit windows:
{s110[['epoch','tc_bjd_tdb','utc','sigma_min','tess_sector','status']].to_string(index=False)}
Outcomes defined in advance (QLP or SPOC light curve of the test sector, same detrending as vet.py): (1) recovered - a box of depth 0.6-1.5x the QLP depth and duration 0.7-1.3x the QLP duration
within +-3 sigma_min (and in any case within +-60 min) of >= 2 of the predicted times, stacked SNR >= 5; (2) inconsistent - a comparable dip exists but
its times differ by > 60 min from every prediction (ephemeris wrong, signal real); (3) excluded - the stacked depth at the predicted phase is
< 0.3x the QLP depth at 3 sigma with >= 2 transits fully covered; (4) insufficient - fewer than 2 predicted transits covered by good data.
Data-release timing: QLP ~2.5-3 months after the sector ends; SPOC 2-min ~3 weeks (only if the star is on that sector's 2-min list).
Files: final_ephemeris.json, predicted_transits_2026_2027.csv; generated by scripts/prereg_candidate.py TIC --freeze.
""")
    print("PREREGISTRATION.md written")
