"""S107 eligibility forecast for the QLP tests of TIC 24526743 and TIC 160330868 (configs/conformance/<TIC>_S107.json), using the segment
times of the SPOC data release notes for Sector 107 (DRN 145, tess_sector_107_drn145_v01.pdf, SHA-256 beginning 0eb0a443, Table 1).
DESCRIPTIVE ONLY, declared in DECISIONS 252 (2026-11-19): NO Sector 107 photometry is read; no rule, config or evaluator changes; the scorer
will use the QLP file's own gaps and flags, not this forecast. Modelled on scripts/conformance_s106_forecast_drn144.py (not edited).
What it does: the same seven gap templates as the published S106 forecast (QLP QUALITY==0 gap patterns of the in-sample 4-segment sectors
S68, S69, S96, S105 of the S106 test targets, relative to those sectors' orbit-table breaks), mapped onto S107's orbit-table breaks; the
evaluator's own edge_trim and coverage functions; the frozen predicted times (status 'prediction', sector 107); ideal 200 s cadence.
Cases: (a) each template; (c) the DRN 145 segment times alone, with no other gap. There is no case b (DRN 145 reports no gap inside a segment).
Not modelled: the 2.03 d of SPOC Manual Exclude (pointing excursions, placed 'near the end of each half-orbit' without times; QLP's flags
are unknown), the barycentric correction (<= ~8 min; DRN times are spacecraft TJD), clock or noise issues. No SNR is given (counts only).
Output: results/s107_drn145/s107_forecast_drn145.{csv,txt}"""
import sys, os, glob, json, numpy as np, pandas as pd
from astropy.io import fits
from astropy.time import Time
R = "/Users/fernando/Desktop/NASA"; sys.path.insert(0, f"{R}/scripts"); import prereg_conformance as pc
OUT = f"{R}/results/s107_drn145/s107_forecast_drn145"
assert not os.path.exists(OUT + ".csv") and not os.path.exists(OUT + ".txt"), "refused: output exists"
TESTS = (24526743, 160330868); TEMPLATE_TICS = (183374279, 120444365, 70441745, 206620592, 122522485, 253931796, 115692561)
DRN = [(4262.08493, 4268.95437), (4269.16409, 4276.26409), (4276.47381, 4283.54464), (4283.74742, 4290.77381)]   # DRN 145 Table 1, TJD
orb = pd.read_csv(f"{R}/catalogs/TESS_orbit_times.csv", comment="#"); orb = orb[pd.to_numeric(orb.Sector, errors="coerce").notna()]; orb["Sector"] = orb.Sector.astype(int)
def segs(s):
    o = orb[orb.Sector == s]; f = lambda x: Time(x.replace(" ", "T"), scale="utc").tdb.jd - 2457000
    return [(f(a), f(b)) for a, b in zip(o["Start of Orbit"], o["End of Orbit"])]
tmpl = {}
for p in sorted(glob.glob(f"{R}/data/qlp*/hlsp_qlp_tess_ffi_s*_llc.fits")):
    tic = int(p.split("-")[-1][:16]); s = int(p.split("_s")[-1][:4])
    if tic not in TEMPLATE_TICS or s not in (68, 69, 96, 105): continue                          # sector filter BEFORE any file is opened
    with fits.open(p) as h: cam = h[0].header["CAMERA"]; d = h[1].data; t = d["TIME"]; g = np.isfinite(t) & (d["QUALITY"] == 0) & np.isfinite(d["SAP_FLUX"]); tg = np.sort(t[g])
    if (s, cam) in tmpl: continue
    sg = segs(s); br = [(sg[i][1], sg[i + 1][0]) for i in range(len(sg) - 1)]; gaps = []
    for i in np.where(np.diff(tg) > 0.5)[0]:
        a, b = tg[i], tg[i + 1]; k = int(np.argmin([abs((x + y) / 2 - (a + b) / 2) for x, y in br])); gaps.append((k, br[k][0] - a, b - br[k][1]))
    tmpl[(s, cam)] = dict(start=tg[0] - sg[0][0], end=sg[-1][1] - tg[-1], gaps=gaps)
assert len(tmpl) == 7, sorted(tmpl)
s107 = segs(107); assert len(s107) == 4, s107
dmax = max(abs(x - y) for a, b in zip(s107, DRN) for x, y in zip(a, b)); assert dmax < 0.02, dmax    # orbit table vs DRN 145 segment times
br107 = [(s107[i][1], s107[i + 1][0]) for i in range(3)]; CAD = 200 / 86400
def tmpl_times(T):
    t = np.arange(s107[0][0] + T["start"], s107[-1][1] - T["end"], CAD); keep = np.ones(len(t), bool)
    for a, b in br107: keep &= ~((t > a) & (t < b))
    for k, pre, post in T["gaps"]: keep &= ~((t > br107[k][0] - pre) & (t < br107[k][1] + post))
    return t[keep]
def drn_times(): return np.concatenate([np.arange(a, b, CAD) for a, b in DRN])
rows = []
for tic in TESTS:
    lock = json.load(open(f"{R}/configs/conformance/{tic}_S107.json")); Dd = lock["ref_dur_h"] / 24
    pr = pd.read_csv(lock["pred_csv"]); lead = pd.to_numeric(pr.tess_sector.astype(str).str.extract(r"^(\d+)")[0], errors="coerce")
    ev = pr[pr.status.astype(str).str.startswith("prediction") & (lead == 107)].sort_values("tc_btjd")
    cases = [(f"S{s}cam{c}", "a_template", tmpl_times(T)) for (s, c), T in sorted(tmpl.items())] + [("DRN145", "c_drn_segments_only", drn_times())]
    for name, case, tt in cases:
        tk = pc.edge_trim(tt, np.ones(len(tt)))[0]; det = []; el = []
        for _, e in ev.iterrows():
            fi, lb, rb = pc.coverage(tk, e.tc_btjd, Dd, CAD); ok = bool(fi >= 0.9 and lb >= 0.5 and rb >= 0.5)
            det.append(f"{int(e.epoch)}:{fi:.2f}/{lb:.2f}/{rb:.2f}"); el += [int(e.epoch)] if ok else []
        rows.append(dict(tic=tic, case=case, template=name, n_pred=len(ev), n_eligible=len(el), eligible_epochs=" ".join(map(str, el)), coverage_in_left_right=" ".join(det)))
df = pd.DataFrame(rows); df.to_csv(OUT + ".csv", index=False)
summ = df.groupby(["tic", "case"]).agg(n_pred=("n_pred", "first"), elig_min=("n_eligible", "min"), elig_med=("n_eligible", "median"), elig_max=("n_eligible", "max"),
                                       frac_below_2=("n_eligible", lambda v: round(float(np.mean(np.array(v) < 2)), 3)))
txt = ("S107 eligibility forecast from DRN 145 segment times (descriptive; no S107 photometry; counts only; DECISIONS 252).\n"
       f"Orbit-table segments (BTJD TDB): {[(round(a, 5), round(b, 5)) for a, b in s107]}; max difference from DRN 145 times {dmax:.5f} d.\n"
       "templates: " + ", ".join(f"S{s}cam{c}: start+{T['start']:.2f} end-{T['end']:.2f} gaps " + str([(k, round(a, 2), round(b, 2)) for k, a, b in T["gaps"]]) for (s, c), T in sorted(tmpl.items()))
       + "\n\n" + summ.to_string() + "\n\n" + df.to_string(index=False) + "\n")
open(OUT + ".txt", "w").write(txt); print(txt)
