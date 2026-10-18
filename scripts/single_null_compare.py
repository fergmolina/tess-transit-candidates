"""Compare duotransit yields of the real and inverted single-transit searches under a grid of event-quality cut sets.
A cut set is useful only where the real search exceeds the inverted null. Writes results/single/summary/duo_cut_grid.json."""
import pandas as pd, numpy as np, itertools, json
R = pd.read_csv("/Users/fernando/Desktop/NASA/results/single/events_all.csv"); N = pd.read_csv("/Users/fernando/Desktop/NASA/results/single_inverted/events_all.csv")
def duos(d, sel, min_ev=2, diff_sector=True, cons=3.0):
    p = d[d["pass"] & sel]; tics = []
    for tic, g in p.groupby("tic"):
        if len(g) < min_ev: continue
        g = g.sort_values("snr", ascending=False); e1 = g.iloc[0]; r = g.iloc[1:]
        m = (np.abs(r.depth - e1.depth) < cons * np.hypot(r.depth_err, e1.depth_err)) & (np.maximum(r.dur_h, e1.dur_h) / np.minimum(r.dur_h, e1.dur_h) < 1.6) & (np.abs(r.tc - e1.tc) > 1.0)
        if diff_sector: m &= r.sector != e1.sector
        if m.sum() >= min_ev - 1 and (g.frac_flagged < 0.5).any(): tics.append(int(tic))
    return tics
grid = []
for snr, dur, bv, mev in itertools.product([8, 10, 12], [4.0, 6.0, 8.0], [0, 20, 50], [2, 3]):
    sel = lambda p, snr=snr, dur=dur, bv=bv: (p.snr >= snr) & (p.dur_h <= dur) & (p.bottom_ratio >= 0.6) & (p.dchi2_box_minus_v >= bv)
    tr = duos(R, sel(R), mev); tn = duos(N, sel(N), mev); grid.append(dict(snr=snr, dur=dur, boxv=bv, min_ev=mev, real=len(tr), null=len(tn), tics=tr))
print(f"{'cut set':45s} real  null  real tics (first 6)")
for g in sorted(grid, key=lambda g: (g["null"], -g["real"])):
    print(f"snr>={g['snr']:2d} dur<={g['dur']:.0f}h boxV>={g['boxv']:2d} n_ev>={g['min_ev']} diff-sector   {g['real']:4d}  {g['null']:4d}  {g['tics'][:6]}")
json.dump(grid, open("/Users/fernando/Desktop/NASA/results/single/summary/duo_cut_grid.json", "w"))
