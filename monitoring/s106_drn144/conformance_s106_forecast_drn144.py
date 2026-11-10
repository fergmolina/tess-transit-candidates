"""Update of the S106 eligibility forecast (scripts/conformance_s106_forecast.py, conformance-v2.1) with the data gap reported in the
SPOC data release notes for Sector 106 (DRN 144, tess_sector_106_drn144_v01.pdf, SHA-256 3fc6c8f03058ae5426b7291c26a27b91e754c1e9d941c75daeebc1e18c682889,
Table 1). DESCRIPTIVE ONLY, 2026-11-10: NO Sector 106 photometry is read; no rule, config or evaluator changes; the scorer will use the
QLP file's own gaps and flags, not this forecast.
What it does: the same gap templates as the published forecast (QLP QUALITY==0 gap patterns of the in-sample 4-segment sectors S68, S69,
S96, S105, mapped onto S106's orbit-table breaks), the evaluator's own edge_trim and coverage functions, and the frozen predicted times.
Three cases per test: (a) each template as published (must reproduce results/conformance_v21/s106_forecast.csv); (b) each template with
the DRN 144 'SSR overflow' window removed (TJD 4252.30716 to 4254.91132); (c) the DRN 144 segment times alone, with no other gap.
Not modelled: QLP's handling of the ACS 5.11 pointing excursions (SPOC flagged 3.39 d as Manual Exclude; QLP flags are unknown), and
any extra noise from them. DRN times are spacecraft TJD (TDB); the barycentric correction (<= ~8 min) is ignored, as in the forecast.
Per-event SNR values are taken unchanged from the published forecast (design-sector noise).
Output: results/s106_drn144/s106_forecast_drn144.{csv,txt}"""
import sys, glob, json, numpy as np, pandas as pd
from astropy.io import fits
from astropy.time import Time
R = "/Users/fernando/Desktop/NASA"; sys.path.insert(0, f"{R}/scripts"); import prereg_conformance as pc
TESTS = (183374279, 120444365, 70441745, 206620592, 122522485, 253931796, 115692561)
SSR = (4252.30716, 4254.91132)                                                                   # DRN 144 Table 1: SSR overflow -> orbit 224b start
DRN = [(4233.42522, 4240.04466), (4240.25439, 4247.86410), (4248.07383, 4252.30716), (4254.91132, 4261.87521)]
orb = pd.read_csv(f"{R}/catalogs/TESS_orbit_times.csv", comment="#"); orb = orb[pd.to_numeric(orb.Sector, errors="coerce").notna()]; orb["Sector"] = orb.Sector.astype(int)
def segs(s):
    o = orb[orb.Sector == s]; f = lambda x: Time(x.replace(" ", "T"), scale="utc").tdb.jd - 2457000
    return [(f(a), f(b)) for a, b in zip(o["Start of Orbit"], o["End of Orbit"])]
tmpl = {}                                                                                        # identical to the published forecast
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
def s106_times(T, ssr):
    t = np.arange(s106[0][0] + T["start"], s106[-1][1] - T["end"], CAD); keep = np.ones(len(t), bool)
    for a, b in br106: keep &= ~((t > a) & (t < b))
    for k, pre, post in T["gaps"]: keep &= ~((t > br106[k][0] - pre) & (t < br106[k][1] + post))
    if ssr: keep &= ~((t > SSR[0]) & (t < SSR[1]))
    return t[keep]
def drn_times(): return np.concatenate([np.arange(a, b, CAD) for a, b in DRN])
old = pd.read_csv(f"{R}/results/conformance_v21/s106_forecast.csv"); rows = []
for tic in TESTS:
    lock = json.load(open(f"{R}/configs/conformance/{tic}_S106.json")); Dd = lock["ref_dur_h"] / 24
    p106 = pd.read_csv(lock["pred_csv"]); lead = pd.to_numeric(p106.tess_sector.astype(str).str.extract(r"^(\d+)")[0], errors="coerce")
    ev = p106[p106.status.astype(str).str.startswith("prediction") & (lead == 106)].sort_values("tc_btjd")
    snr1 = float(old[old.tic == tic].snr_event.iloc[0])
    def elig(t6):
        tk = pc.edge_trim(t6, np.ones(len(t6)))[0]; out = []
        for _, e in ev.iterrows():
            fi, lb, rb = pc.coverage(tk, e.tc_btjd, Dd, CAD)
            if fi >= 0.9 and lb >= 0.5 and rb >= 0.5: out.append(int(e.epoch))
        return out
    cases = [(f"S{s}cam{c}", "a_published", s106_times(T, False)) for (s, c), T in sorted(tmpl.items())]
    cases += [(f"S{s}cam{c}", "b_with_ssr_gap", s106_times(T, True)) for (s, c), T in sorted(tmpl.items())] + [("DRN144", "c_drn_segments_only", drn_times())]
    for name, case, t6 in cases:
        el = elig(t6)
        if case == "a_published":
            ref = old[(old.tic == tic) & (old.template == name)].iloc[0]; assert int(ref.n_eligible) == len(el), (tic, name, ref.n_eligible, len(el))
        rows.append(dict(tic=tic, case=case, template=name, n_pred=len(ev), n_eligible=len(el), eligible_epochs=" ".join(map(str, el)), snr_event=snr1,
                         snr_joint=round(snr1 * np.sqrt(len(el)), 2), strict_epochs=" ".join(map(str, lock.get("strict_epochs") or [])),
                         strict_all_eligible=("" if not lock.get("strict_epochs") else bool(set(lock["strict_epochs"]) <= set(el)))))
df = pd.DataFrame(rows); df.to_csv(f"{R}/results/s106_drn144/s106_forecast_drn144.csv", index=False)
summ = df.groupby(["tic", "case"]).agg(n_pred=("n_pred", "first"), elig_min=("n_eligible", "min"), elig_med=("n_eligible", "median"), elig_max=("n_eligible", "max"),
                                       frac_below_2=("n_eligible", lambda v: round(float(np.mean(np.array(v) < 2)), 3)), snr_event=("snr_event", "first"),
                                       snr_joint_min=("snr_joint", "min"), snr_joint_med=("snr_joint", "median"), snr_joint_max=("snr_joint", "max"))
txt = ("S106 eligibility forecast with the DRN 144 gap (descriptive; no S106 photometry). Case a reproduces the published forecast (asserted).\n"
       f"SSR gap removed in case b: TJD {SSR[0]} to {SSR[1]}. Case c: DRN 144 segment times only.\n\n" + summ.to_string() + "\n\n" + df.to_string(index=False) + "\n")
open(f"{R}/results/s106_drn144/s106_forecast_drn144.txt", "w").write(txt); print(summ.to_string())
