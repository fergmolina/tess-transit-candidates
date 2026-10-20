"""conformance-v2.1 (2026-10-20): forecast of S106 eligible events per test under the edge rule (DECISIONS item 76) and the expected joint
SNR, WITHOUT any S106 photometry. S106 data gaps are not known (QLP S106 not released); they are modelled with every in-sample 4-segment
sector's QLP QUALITY==0 gap pattern (S68, S69, S96, S105; one template per sector+camera of the test targets), expressed relative to
that sector's orbit-time breaks (catalogs/TESS_orbit_times.csv) and mapped onto S106's breaks. Per-event noise at the reference T14 is
measured on each target's DESIGN sector (item 76) with the evaluator's own preprocessing and error model.
Output: results/conformance_v21/s106_forecast.{csv,txt}"""
import sys, glob, json, numpy as np, pandas as pd
from astropy.io import fits
from astropy.time import Time
from wotan import flatten
R = "/Users/fernando/Desktop/NASA"; sys.path.insert(0, f"{R}/scripts"); import prereg_conformance as pc
TESTS = (183374279, 120444365, 70441745, 206620592, 122522485, 253931796, 115692561)
DESIGN = {183374279: 96, 120444365: 96, 70441745: 96, 206620592: 96, 122522485: 97, 253931796: 96, 115692561: 96}
orb = pd.read_csv(f"{R}/catalogs/TESS_orbit_times.csv", comment="#"); orb = orb[pd.to_numeric(orb.Sector, errors="coerce").notna()]; orb["Sector"] = orb.Sector.astype(int)
def segs(s):
    o = orb[orb.Sector == s]; f = lambda x: Time(x.replace(" ", "T"), scale="utc").tdb.jd - 2457000
    return [(f(a), f(b)) for a, b in zip(o["Start of Orbit"], o["End of Orbit"])]
# templates
tmpl = {}
for p in sorted(glob.glob(f"{R}/data/qlp*/hlsp_qlp_tess_ffi_s*_llc.fits")):
    tic = int(p.split("-")[-1][:16]); s = int(p.split("_s")[-1][:4])
    if tic not in TESTS or s not in (68, 69, 96, 105): continue
    with fits.open(p) as h: cam = h[0].header["CAMERA"]; d = h[1].data; t = d["TIME"]; g = np.isfinite(t) & (d["QUALITY"] == 0) & np.isfinite(d["SAP_FLUX"]); tg = np.sort(t[g])
    if (s, cam) in tmpl: continue
    sg = segs(s); br = [(sg[i][1], sg[i + 1][0]) for i in range(len(sg) - 1)]; gaps = []
    for i in np.where(np.diff(tg) > 0.5)[0]:
        a, b = tg[i], tg[i + 1]; k = int(np.argmin([abs((x + y) / 2 - (a + b) / 2) for x, y in br])); gaps.append((k, br[k][0] - a, b - br[k][1]))
    tmpl[(s, cam)] = dict(start=tg[0] - sg[0][0], end=sg[-1][1] - tg[-1], gaps=gaps)
s106 = segs(106); br106 = [(s106[i][1], s106[i + 1][0]) for i in range(len(s106) - 1)]; CAD = 200 / 86400
def s106_times(T):
    t = np.arange(s106[0][0] + T["start"], s106[-1][1] - T["end"], CAD); keep = np.ones(len(t), bool)
    for a, b in br106: keep &= ~((t > a) & (t < b))
    for k, pre, post in T["gaps"]: keep &= ~((t > br106[k][0] - pre) & (t < br106[k][1] + post))
    return t[keep]
rows = []; noise = {}
for tic in TESTS:
    lock = json.load(open(f"{R}/configs/conformance/{tic}_S106.json")); Dd = lock["ref_dur_h"] / 24; dep = lock["ref_depth_ppm"]
    p106 = pd.read_csv(lock["pred_csv"]); lead = pd.to_numeric(p106.tess_sector.astype(str).str.extract(r"^(\d+)")[0], errors="coerce")
    ev = p106[p106.status.astype(str).str.startswith("prediction") & (lead == 106)].sort_values("tc_btjd")
    # noise on the design sector (evaluator preprocessing, known transits masked)
    eph = json.load(open(f"{R}/results/vet_allsky/{tic}/final_ephemeris_v2.json")); T0, P = eph["T0_btjd"], eph["P_d"]
    t, f, *_ = pc.load_lc(glob.glob(f"{R}/data/qlp*/hlsp_qlp_tess_ffi_s{DESIGN[tic]:04d}-{tic:016d}_tess_v01_llc.fits")[0], "SAP_FLUX"); o = np.argsort(t); t, f = t[o], f[o]
    t, f, _ = pc.edge_trim(t, f); intr = np.abs(((t - T0) / P + 0.5) % 1 - 0.5) * P < 1.5 * Dd
    r = f / flatten(t, f, method="biweight", window_length=0.7, break_tolerance=0.5, return_trend=True, mask=intr)[1]; g = np.isfinite(r) & ~intr
    cad = float(np.median(np.diff(t))); beta, sig = pc.red_noise_beta(t[g], r[g], Dd, cad)
    err1 = beta * sig * np.sqrt(1 / (Dd / cad) + (np.pi / 2) / (5 * Dd / cad)) * 1e6; noise[tic] = (beta, sig * 1e6, err1)
    for (s, cam), T in sorted(tmpl.items()):
        tt = pc.edge_trim(s106_times(T), np.ones(1))[0] if False else None
        t6 = s106_times(T); t6k = pc.edge_trim(t6, np.ones(len(t6)))[0]; elig = []
        for _, e in ev.iterrows():
            fi, lb, rb = pc.coverage(t6k, e.tc_btjd, Dd, CAD); elig.append(bool(fi >= 0.9 and lb >= 0.5 and rb >= 0.5))
        n = int(sum(elig)); rows.append(dict(tic=tic, template=f"S{s}cam{cam}", n_pred=len(ev), n_eligible=n, eligible_epochs=" ".join(str(int(x)) for x, y in zip(ev.epoch, elig) if y),
                                             err_event_ppm=round(err1), snr_event=round(dep / err1, 2), snr_joint=round(dep / err1 * np.sqrt(n), 2), beta=round(beta, 2), sig_pt_ppm=round(sig * 1e6)))
df = pd.DataFrame(rows); df.to_csv(f"{R}/results/conformance_v21/s106_forecast.csv", index=False)
summ = df.groupby("tic").agg(n_pred=("n_pred", "first"), elig_min=("n_eligible", "min"), elig_med=("n_eligible", "median"), elig_max=("n_eligible", "max"),
                              p_insufficient=("n_eligible", lambda v: float(np.mean(np.array(v) < 2))), snr_event=("snr_event", "first"),
                              snr_joint_min=("snr_joint", "min"), snr_joint_med=("snr_joint", "median"), snr_joint_max=("snr_joint", "max"))
txt = "templates: " + ", ".join(f"S{s}cam{c}: start+{T['start']:.2f} end-{T['end']:.2f} gaps " + str([(k, round(a, 2), round(b, 2)) for k, a, b in T["gaps"]]) for (s, c), T in sorted(tmpl.items()))
txt += "\nS106 breaks (BTJD TDB): " + str([(round(a, 2), round(b, 2)) for a, b in br106]) + f"; segments {s106[0][0]:.2f}-{s106[-1][1]:.2f}\n\n" + summ.to_string() + "\n\n" + df.to_string(index=False)
open(f"{R}/results/conformance_v21/s106_forecast.txt", "w").write(txt); print(txt[:6000])
