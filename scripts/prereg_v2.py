"""v2 pre-registration: ephemeris from ALL sectors (external review, results/external_review_allsky/REVIEW.md 3.1/4.1: v1 used only the
200-s sectors because vet.py times single transits with min_pts=15, dropping every 600-s/1800-s event -> biased periods).
Method: start from the all-data BLS ephemeris (report.json bls_refine); for every QLP sector (raw SAP_FLUX, QUALITY==0, cadence-aware batman
model with the MCMC shape, per-event local linear baseline) fit ONE common time offset dt for all transits in that sector on a grid
(stacking the events), error from delta-chi2 = 1 after rescaling to reduced chi2 >= 1; add SPOC 2-min sectors the same way if present.
Weighted linear fit of the per-sector times vs mean epoch -> v2 ephemeris -> predictions (same machinery/outcome rules as v1).
Writes PREREGISTRATION_v2.md, predicted_transits_2026_2027_v2.csv, final_ephemeris_v2.json; v1 files untouched.
Usage: python -I prereg_v2.py TIC [--freeze] [--no-2min] [--unreleased-sectors 106] [--desc text]"""
import os, re, sys, json, glob, hashlib, datetime, argparse, numpy as np, pandas as pd; sys.path.insert(0, "/Users/fernando/Desktop/NASA/scripts"); os.environ["TSEARCH_SOURCE"] = "qlp"
import batman, lightkurve as lk; from astropy.time import Time; from astropy.io import fits

def geocentric_utc(jd_tdb, ra_deg, dec_deg):
    """UTC of arrival at the geocentre: BJD_TDB minus the barycentric light-travel time toward the target (referee finding 2026-10-19:
    Time(jd, scale='tdb').utc alone only changes the time SCALE and is off by up to +-8 min)."""
    from astropy.coordinates import SkyCoord, EarthLocation; import astropy.units as u
    t = Time(jd_tdb, format="jd", scale="tdb"); ltt = t.light_travel_time(SkyCoord(ra_deg, dec_deg, unit="deg"), kind="barycentric", location=EarthLocation.from_geocentric(0, 0, 0, unit=u.m))
    return (t - ltt).utc
ROOT = "/Users/fernando/Desktop/NASA"
ap = argparse.ArgumentParser(); ap.add_argument("tic", type=int); ap.add_argument("--freeze", action="store_true"); ap.add_argument("--no-2min", action="store_true"); ap.add_argument("--unreleased-sectors", default=""); ap.add_argument("--desc", default=""); ap.add_argument("--version", type=int, default=2, help="output version suffix (corrections are new versions; earlier files untouched)"); ap.add_argument("--reason", default="", help="required for --version > 2: why this version supersedes the previous one"); ap.add_argument("--clock", action="store_true", help="apply QLP S99+ barycentric clock corrections from results/qlp_clock_v2/<TIC>.json (qlp_clock_v2.py method 2)"); ap.add_argument("--ground", action="store_true", help="no TESS coverage: list every predicted transit through 2027-12 regardless of sector"); a = ap.parse_args()
if a.version > 2 and not a.reason.strip(): raise SystemExit('--reason is required for --version > 2')
TIC = a.tic; OUT = f"{ROOT}/results/vet_allsky/{TIC}"; rep = json.load(open(f"{OUT}/report.json")); RA_DEG, DEC_DEG = rep["meta"]["ra"], rep["meta"]["dec"]; b0 = rep["bls_refine"]
P0, T00 = b0["period"], b0["T0"]; SPAN = []; rprs, ars, bimp = rep["shape_mcmc"]["median"][1:4]; dur_d = b0["duration_h"] / 24
def model(t, tc, exp):
    inc = np.degrees(np.arccos(np.clip(bimp / ars, 0, 1))); p = batman.TransitParams(); p.t0 = tc; p.per = P0; p.rp = rprs; p.a = ars; p.inc = inc; p.ecc = 0; p.w = 90; p.u = [0.4, 0.25]; p.limb_dark = "quadratic"
    return batman.TransitModel(p, t, supersample_factor=max(3, int(round(exp * 86400 / 120))), exp_time=exp).light_curve(p)
def sector_offset(t, f, label):
    """Common time offset for all covered transits in one sector. Returns (mean_epoch, tc, err, n_events, depth) or None."""
    exp = float(np.median(np.diff(t))); eps = range(int(np.floor((t.min() - T00) / P0)) - 1, int(np.ceil((t.max() - T00) / P0)) + 2); events = []
    for ep in eps:
        tc0 = T00 + ep * P0; w = np.abs(t - tc0) < 2.5 * dur_d; intr = np.abs(t - tc0) < dur_d / 2
        if intr.sum() < max(3, 0.6 * dur_d / exp) or w.sum() < 4 * intr.sum(): continue
        t_, f_ = t[w], f[w] / np.nanmedian(f[w]); oot = np.abs(t_ - tc0) > 0.75 * dur_d
        if oot.sum() < 5: continue
        sig = 1.4826 * np.median(np.abs(f_[oot] - np.median(f_[oot]))); events.append((ep, tc0, t_, f_, sig))
    if not events: return None
    grid = np.linspace(-0.12, 0.12, 289); chi = np.zeros(len(grid)); npts = sum(len(e[2]) for e in events)
    for i, dt in enumerate(grid):
        for ep, tc0, t_, f_, sig in events:
            m = model(t_, tc0 + dt, exp); A = np.vstack([m, m * (t_ - tc0)]).T; c, *_ = np.linalg.lstsq(A, f_, rcond=None); chi[i] += np.sum(((f_ - A @ c) / sig) ** 2)
    i = int(np.argmin(chi)); dof = npts - 2 * len(events) - 1; scale = max(1.0, chi[i] / dof); ok = chi < chi[i] + scale
    err = max((grid[ok].max() - grid[ok].min()) / 2, (grid[1] - grid[0]) / 2); dchi2 = float(chi[int(np.argmin(np.abs(grid)))] - chi[i])
    # depth at the best offset (mean over events, central 80 %)
    deps = []
    for ep, tc0, t_, f_, sig in events:
        m = model(t_, tc0 + grid[i], exp); A = np.vstack([m, m * (t_ - tc0)]).T; c, *_ = np.linalg.lstsq(A, f_, rcond=None); base = A @ c / m; ii = np.abs(t_ - tc0 - grid[i]) < 0.4 * dur_d
        if ii.sum() > 2: deps.append(1 - np.mean(f_[ii] / base[ii]))
    me = float(np.mean([e[0] for e in events])); tc = T00 + me * P0 + grid[i]
    flat_chi = sum(np.sum(((f_ - np.median(f_)) / sig) ** 2) for ep, tc0, t_, f_, sig in events); sig_det = float(flat_chi - chi[i])
    print(f"  {label:14s} exp {exp*86400:5.0f} s  {len(events)} events  dt = {grid[i]*1440:+6.1f} +- {err*1440:4.1f} min  depth {np.mean(deps)*1e6 if deps else np.nan:5.0f} ppm  dchi2(vs flat) {sig_det:6.0f}  red.chi2 {chi[i]/dof:.2f}")
    if sig_det < 16 or err * 1440 > 45 or abs(grid[i]) >= 0.115: print("     -> rejected (weak or at grid edge)"); return None
    return (me, float(tc), float(err), len(events), float(np.mean(deps)) if deps else np.nan)
rows = []
# Holdout guard (erratum 2026-10-20): declared test sectors (--unreleased-sectors), every future sector of this target (tess-point list) and any sector >= 106
# are excluded BEFORE their files are opened or downloaded, for both QLP and SPOC products.
TESTSECS = {int(x) for x in a.unreleased_sectors.split(",") if x.strip()} | {x for x in json.load(open(f"{ROOT}/catalogs/allsky_tic2sectors_future.json")).get(str(TIC), []) if x <= 134}
def is_test(sec): return sec in TESTSECS or sec >= 106
for fpath in sorted(glob.glob(f"{ROOT}/data/qlp_allsky/*{TIC:016d}*.fits")):
    m_ = re.search(r"_s0*(\d+)-", os.path.basename(fpath)); fsec = int(m_.group(1)) if m_ else None
    if fsec is None or is_test(fsec): print(f"QLP {os.path.basename(fpath)} SKIPPED before reading (test sector or unparsable sector)"); continue
    with fits.open(fpath, memmap=False) as h:
        d = h[1].data; sec = int(h[0].header["SECTOR"]); t = np.asarray(d["TIME"], float); f = np.asarray(d["SAP_FLUX"], float); q = np.asarray(d["QUALITY"], int)
    m = np.isfinite(t) & np.isfinite(f) & (q == 0); t, f = t[m], f[m]
    if len(t) < 200: continue
    m &= True; med = np.nanmedian(f); keep = np.abs(f / med - 1) < 0.5; t, f = t[keep], f[keep]
    SPAN.append((float(t.min()), float(t.max()))); r = sector_offset(t, f, f"S{sec} QLP SAP")
    if r: rows.append(dict(sector=sec, source="QLP SAP", mean_epoch=r[0], tc=r[1], tc_err=r[2], n_events=r[3], depth_ppm=r[4] * 1e6))
if not a.no_2min:
    cached = sorted(glob.glob(f"{ROOT}/data/lk_cache/**/*{TIC:016d}*-s_lc.fits", recursive=True))
    cached = [c for c in cached if (lambda m: m is not None and not is_test(int(m.group(1))))(re.search(r"-s0*(\d+)-", os.path.basename(c)))]
    if cached: lcs = [lk.read(f) for f in cached]; print("SPOC 2-min from cache:", len(cached))
    else:
        sr = lk.search_lightcurve(f"TIC {TIC}", author="SPOC", exptime=120)
        if len(sr): sr = sr[[not is_test(int(str(m).split()[-1])) for m in sr.table["mission"]]]   # e.g. "TESS Sector 106" -> filtered BEFORE download
        lcs = sr.download_all(download_dir=f"{ROOT}/data/lk_cache") if len(sr) else []
    for lc in lcs:
        lc = lc.remove_nans(); qq = lc.quality == 0; t = lc.time.value[qq]; f = lc.flux.value[qq]; sec = int(lc.sector)
        if is_test(sec): raise SystemExit(f'holdout guard failed: S{sec} SPOC loaded')
        r = sector_offset(t, f, f"S{sec} SPOC 2-min")
        if r: rows[:] = [x for x in rows if x["sector"] != sec]; rows.append(dict(sector=sec, source="SPOC 2-min", mean_epoch=r[0], tc=r[1], tc_err=r[2], n_events=r[3], depth_ppm=r[4] * 1e6)) if r else None
CLOCK = {}
if a.clock:   # QLP S99+ barycentric timestamp error (MAST notice; S105 also affected): add the method-2 correction to each affected QLP sector time
    cj = json.load(open(f"{ROOT}/results/qlp_clock_v2/{TIC}.json"))
    for x in rows:
        v = cj["sectors"].get(str(x["sector"]))
        if x["source"].startswith("QLP") and x["sector"] >= 99:
            if v is None: raise SystemExit(f"--clock: no clock correction for S{x['sector']}")
            x["tc"] += v["correction_min"] / 1440; x["clock_correction_min"] = v["correction_min"]; CLOCK[x["sector"]] = v["correction_min"]
    print("clock corrections applied (min):", CLOCK)
CLOCK_NOTE = (("QLP S99+ sector times were corrected for the barycentric timestamp error before the fit (results/qlp_clock_v2/; corrections in min: " + str({k: round(v, 2) for k, v in CLOCK.items()}) + "). ") if CLOCK
              else ("No QLP S99+ sector time enters this ephemeris. " if not any(x["source"].startswith("QLP") and x["sector"] >= 99 for x in rows) else "WARNING: QLP S99+ sector times NOT clock-corrected. "))
df = pd.DataFrame(rows).sort_values("tc"); e = df.mean_epoch.values; tc = df.tc.values; er = df.tc_err.values; e0 = float(np.round(e[-1]))
E = e - e0
if len(tc) >= 3:
    A = np.vstack([np.ones_like(E), E]).T; W = np.diag(1 / er ** 2); cov = np.linalg.inv(A.T @ W @ A); beta = cov @ A.T @ W @ tc
    res = tc - A @ beta; chi2 = float(np.sum(res ** 2 / er ** 2)); dof = len(tc) - 2; infl = max(1, np.sqrt(chi2 / dof)); cov *= infl ** 2; T0, P = beta; T0e, Pe = np.sqrt(np.diag(cov))
else:  # one or two sector times: period held at the all-data BLS value; its error = quarter-duration timing tolerance over the data baseline
    P = P0; span_cycles = (max(y for _, y in SPAN) - min(x for x, _ in SPAN)) / P0; Pe = (dur_d / 4) / span_cycles
    w = 1 / er ** 2; T0 = float(np.sum(w * (tc - E * P)) / np.sum(w)); T0e = float(1 / np.sqrt(np.sum(w))); res = tc - (T0 + E * P); chi2 = float(np.sum(res ** 2 / er ** 2)); dof = len(tc) - 1
    infl = max(1, np.sqrt(chi2 / dof)) if dof > 0 else 1.0; T0e *= infl; cov = np.diag([T0e ** 2, Pe ** 2]); print(f"NOTE: {len(tc)} sector time(s) only - period held at the BLS value, sigma_P from the {span_cycles:.0f}-cycle baseline")
df["oc_min"] = res * 1440; print(df.round(5).to_string(index=False))
print(f"\nv2 ephemeris ({len(tc)} sector times, epoch ref {e0:.0f}): T0 = BTJD {T0:.5f} +- {T0e*1440:.1f} min, P = {P:.6f} +- {Pe:.6f} d; chi2/dof {chi2:.1f}/{dof}; inflation {infl:.2f}")
v1 = json.load(open(f"{OUT}/final_ephemeris.json")) if os.path.exists(f"{OUT}/final_ephemeris.json") else dict(P_d=P0, P_err_d=np.nan, sha256_csv="(no v1 freeze)"); print(f"v1/BLS: P = {v1['P_d']:.6f}; all-data BLS P = {P0:.6f}; v2 - BLS = {(P - P0)/Pe:+.1f} sigma")
orb = pd.read_csv(f"{ROOT}/catalogs/TESS_orbit_times.csv", comment="#"); orb = orb[pd.to_numeric(orb.Sector, errors="coerce").notna()]; orb["Sector"] = orb.Sector.astype(int)
orb["s"] = pd.to_datetime(orb["Start of Orbit"]).map(lambda x: x.to_julian_date() - 2457000); orb["e"] = pd.to_datetime(orb["End of Orbit"]).map(lambda x: x.to_julian_date() - 2457000)
win = {s: list(zip(g.s, g.e)) for s, g in orb.groupby("Sector")}; approx_win = set()
sd = pd.read_csv(f"{ROOT}/catalogs/TESS_sector_dates_future.csv")
for _, r in sd.iterrows():
    s0, e1 = pd.Timestamp(r.start).to_julian_date() - 2457000, pd.Timestamp(r.end).to_julian_date() + 1 - 2457000
    if int(r.Sector) not in win: win[int(r.Sector)] = [(s0, e1)]; approx_win.add((s0, e1))
    elif max(y for _, y in win[int(r.Sector)]) < e1 - 3: w2 = (max(y for _, y in win[int(r.Sector)]) + 0.2, e1); win[int(r.Sector)].append(w2); approx_win.add(w2)
fut = [x for x in json.load(open(f"{ROOT}/catalogs/allsky_tic2sectors_future.json")).get(str(TIC), []) if x <= 134]; win = {s: w for s, w in win.items() if s in fut}; print("future sectors:", fut)
freeze = Time(datetime.datetime.now(datetime.UTC)); unrel = {int(x) for x in a.unreleased_sectors.split(",") if x.strip()}; prow = []
for k in range(1, 200000):
    t = T0 + k * P; sig = np.sqrt(cov[0, 0] + k * k * cov[1, 1] + 2 * k * cov[0, 1]); jd = t + 2457000
    if jd >= 2461406.5: break   # through 2027-12-31
    sec = next((s for s, ws in win.items() if any(x <= t <= y for x, y in ws)), None); isapprox = any((x, y) in approx_win for ws in win.values() for x, y in ws if x <= t <= y)
    insec = next((s for s, ws in win.items() if min(x for x, _ in ws) <= t <= max(y for _, y in ws)), None)
    if sec is None and insec is None and not a.ground: continue
    prow.append(dict(epoch=int(e0 + k), tc_btjd=round(t, 5), tc_bjd_tdb=round(jd, 5), utc=geocentric_utc(jd, RA_DEG, DEC_DEG).iso[:16], utc_tdb_scale_only=Time(jd, format="jd", scale="tdb").utc.iso[:16], sigma_min=round(sig * 1440, 1), tess_sector=((f"{sec} (span only, gap unknown)" if isapprox else sec) if sec else (f"{insec} (gap)" if insec else "none (ground-based)")),
                     status=("prediction (sector already observed; public availability not checked by this script; authors attest target-sector photometry not examined before freeze)" if (sec in unrel or insec in unrel) else ("retrodiction: before freeze, untested" if jd < freeze.jd else "prediction"))))
if not prow:
    print("NOTE: no dated window for future sectors", fut, "- listing every transit; match to sector dates when they are published")
    for k in range(1, 200000):
        t = T0 + k * P; sig = np.sqrt(cov[0, 0] + k * k * cov[1, 1] + 2 * k * cov[0, 1]); jd = t + 2457000
        if jd >= 2461406.5: break   # through 2027-12-31
        prow.append(dict(epoch=int(e0 + k), tc_btjd=round(t, 5), tc_bjd_tdb=round(jd, 5), utc=geocentric_utc(jd, RA_DEG, DEC_DEG).iso[:16], utc_tdb_scale_only=Time(jd, format="jd", scale="tdb").utc.iso[:16], sigma_min=round(sig * 1440, 1), tess_sector=f"undated (future sectors {fut})", status=("retrodiction: before freeze, untested" if jd < freeze.jd else "prediction")))
pdf = pd.DataFrame(prow); V = a.version; csv = f"{OUT}/predicted_transits_2026_2027_v{V}.csv"
# v1.12 (review F14): never overwrite a frozen version; a run without --freeze writes only to OUT/_dryrun/
if os.path.exists(f"{OUT}/PREREGISTRATION_v{V}.md") or (a.freeze and os.path.exists(csv)): raise SystemExit(f"refused: v{V} of TIC {TIC} is already frozen; use a new --version")
if not a.freeze: os.makedirs(f"{OUT}/_dryrun", exist_ok=True); csv = f"{OUT}/_dryrun/predicted_transits_2026_2027_v{V}.csv"
pdf.to_csv(csv, index=False); sha = hashlib.sha256(open(csv, "rb").read()).hexdigest(); stamp = freeze.utc.iso[:19] + " UTC"
show = pdf[pdf.status.str.startswith("prediction") & (pdf.tess_sector.astype(str).str.match(r"^\d+") | pdf.tess_sector.astype(str).str.startswith("none") | pdf.tess_sector.astype(str).str.startswith("undated"))]; print(show.to_string(index=False)); print("SHA-256", sha, "frozen", stamp)
json.dump(dict(tic=TIC, version=V, dry_run=not a.freeze, T0_btjd=T0, T0_err_d=T0e, P_d=P, P_err_d=Pe, epoch_ref=e0, chi2=chi2, dof=dof, inflation=infl, bls_P=P0, bls_T0=T00, sector_times=df.to_dict("records"), sha256_csv=sha, frozen=stamp), open(f"{OUT}/" + ("" if a.freeze else "_dryrun/") + f"final_ephemeris_v{V}.json", "w"), indent=1, default=float)
if a.freeze:
    pd.options.display.float_format = "{:.5f}".format; ref_depth = rep.get("sap_depth", {}).get("depth_ppm", b0["depth_ppm"]); ref_T14 = rep.get("shape_mcmc", {}).get("T14_h", b0["duration_h"])
    open(f"{OUT}/PREREGISTRATION_v{V}.md", "w").write(f"""# Pre-registered transit predictions v{V} - TIC {TIC}
Frozen: {stamp}. Author: Fernando Molina (Independent researcher, ORCID 0009-0002-2872-3406). Analysis with Claude (Anthropic) under the author's direction.
{('Supersedes v1 (PREREGISTRATION.md, SHA ' + v1['sha256_csv'][:8] + '...), which is kept unchanged on record.') if os.path.exists(f'{OUT}/final_ephemeris.json') else 'First freeze for this object (v2 tooling: all-sector ephemeris).'}{(' v' + str(V) + ' supersedes v2 (SHA of v2 CSV kept on record in final_ephemeris_v2.json); reason: ' + a.reason) if V > 2 else ''} Reason (external review 2026-10-18,
results/external_review_allsky/REVIEW.md): v1 timed only the 200-s sectors (vet.py min_pts cut), ignoring 2018-2021 data; v2 fits one time offset per
sector from ALL sectors (raw SAP flux, cadence-aware model, local baselines; SPOC 2-min sectors where they exist) on top of the all-data BLS ephemeris.
Ephemeris: T0 = BTJD {T0:.5f} +- {T0e*1440:.1f} min (epoch {e0:.0f}), P = {P:.6f} +- {Pe:.6f} d (chi2/dof {chi2:.1f}/{dof}, inflation x{infl:.2f}); all-data BLS P = {P0:.6f}.
Sector times used: {', '.join(f"S{int(r.sector)} {r.source} ({int(r.n_events)} ev, O-C {r.oc_min:+.1f} +- {r.tc_err*1440:.1f} min)" for r in df.itertuples())}.
Depth per sector (fixed shape, local baseline, raw SAP): {', '.join(f"S{int(r.sector)} {r.depth_ppm:.0f}" for r in df.itertuples())} ppm.
{a.desc}
Reference values for the outcome clauses: depth {ref_depth:.0f} ppm (raw SAP, all sectors), T14 {ref_T14:.2f} h.
SHA-256 of predicted_transits_2026_2027_v{V}.csv: {sha}
**Test of record: {"ground-based photometry (no TESS coverage of this star through Sector 134); any observer may test any listed epoch" if a.ground else "next TESS sector(s)"}.** Predicted mid-transits (sigma_min = 1-sigma timing uncertainty at that epoch):
{show[['epoch','tc_bjd_tdb','utc','sigma_min','tess_sector','status']].to_string(index=False)}
{("Outcomes defined in advance (ground-based light curve, <= 1.5 mmag per 10-min bin, covering the predicted time +-3 sigma_min plus >= 1 h baseline on each side): (1) recovered - a dip of depth 0.5-1.5x and duration 0.7-1.3x the reference values within +-3 sigma_min of the predicted time on >= 2 epochs, each at SNR >= 4; (2) inconsistent - a comparable dip exists but its time differs by > 3 sigma_min from the prediction on >= 2 epochs; (3) excluded - no dip > 0.3x the reference depth (3 sigma) with >= 2 predicted windows fully covered at the required precision; (4) insufficient - fewer than 2 windows covered. " if a.ground else "Outcomes defined in advance (QLP or SPOC light curve of the test sector, or a TESScut fixed-aperture extraction, transit-masked biweight detrend): (1) recovered - a box of depth 0.5-1.5x and duration 0.7-1.3x the reference values at >= 2 covered predicted transit windows, stacked SNR >= 5, timing gate |sum(w_i dt_i)/sum(w_i)| <= max(3 mean(sigma_min,i), 30 min) with w_i = 1/depth_err_i^2 over the coverage-qualified windows (frozen evaluator; inverse depth-variance weights); duration and full-coverage criteria are assessed under the separately versioned conformance procedure (see CLARIFICATION_TIMING_RULE_2026-10-20.md); (2) inconsistent - a comparable dip exists but its times differ by > 30 min from every prediction; (3) excluded - stacked depth at the predicted phase < 0.3x at 3 sigma with >= 2 transits fully covered; (4) insufficient - fewer than 2 predicted transits covered. " + CLOCK_NOTE + "")}Generated by scripts/prereg_v2.py {TIC} --freeze --version {V}{" --ground" if a.ground else ""}.
""")
    print(f"PREREGISTRATION_v{V}.md written")
