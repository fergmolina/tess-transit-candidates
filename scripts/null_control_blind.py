"""Control for the season-holdout blind test: apply it to the best INVERTED-light-curve false signal from the null calibration
(TIC 120896927, bump at 4.756 d, SDE 14.0). A sound blind test should NOT show the bump at the predicted phase in held-out years."""
import sys, json, warnings; sys.path.insert(0, "/Users/fernando/Desktop/NASA/scripts"); warnings.filterwarnings("ignore")
import numpy as np
from tsearch import load_spoc_lc, detrend
from search_pipeline import sector_files, year_of, bin_lc, period_grid, bls_stats
import vet
tic, P, T0, dur_h = 120896927, 4.756, None, None
d = json.load(open(f"/Users/fernando/Desktop/NASA/results/null/{tic}.json")); pk = d["peaks"][0]; P, T0, dur_h = pk["period"], pk["t0"], pk["duration_h"]
secs = {}
for fp in sector_files(tic):
    t, f, fe, m = load_spoc_lc(fp)
    if len(t) < 2000: continue
    td, fd, mask, _ = detrend(t, f, 0.5); secs[m["sector"]] = dict(t=td, f=2 - fd, fe=fe[mask], meta=m)   # INVERTED
T = np.concatenate([v["t"] for v in secs.values()]); F = np.concatenate([v["f"] for v in secs.values()]); E = np.concatenate([v["fe"] for v in secs.values()]); o = np.argsort(T); T, F, E = T[o], F[o], E[o]
print(f"TIC {tic} inverted: sectors {sorted(secs)}; inverted peak P={P:.4f} T0={T0:.3f} dur={dur_h:.1f} h depth={pk['depth']*1e6:.0f} ppm SDE={pk['sde']:.1f}")
fit = vet.fit_shape(T, F, E, P, T0, dur_h / 24, max(pk["depth"], 1e-6), float(np.clip(P / (np.pi * dur_h / 24), 2, 400)))
print(f"  shape fit on inverted data: rprs={fit['rprs']:.4f} ars={fit['ars']:.1f} b={fit['b']:.2f}")
for y in sorted({year_of(x) for x in T}):
    bt = vet.blind_test(T, F, E, secs, P, T0, dur_h / 24, fit["rprs"], fit["ars"], fit["b"], y)
    if bt.get("ok") and "predicted" in bt:
        sc = bt["holdout_scan"]; ib = int(np.nanargmax([q["depth"] for q in sc]))
        print(f"  HOLDOUT {y}: training BLS rank={bt['training_search']['rank_of_candidate']} (top SDE {bt['training_search']['top_peaks'][0]['sde']:.1f}); predicted-phase 1-sigma {max(q['tc_pred_err_min'] for q in bt['predicted']):.0f} min; depth at predicted phase {bt['stacked_depth']*1e6:.0f}+-{bt['stacked_err']*1e6:.0f} ({bt['stacked_snr']:.1f} sigma); null p={bt['null_p_value']:.3f}; deepest within +-3h {sc[ib]['depth']*1e6:.0f} at {sc[ib]['offset_h']:+.2f} h")
    else: print(f"  HOLDOUT {y}: {bt.get('reason')} | training top: {[(round(q['period'],4), round(q['sde'],1)) for q in bt.get('training_search', {}).get('top_peaks', [])]}")
