"""Collect ffi_pixel_summary.txt results for a candidate list and classify: ON_TARGET (all tested sectors offset <= 0.5 px and at least one
sector), OFF_TARGET (any sector offset >= 0.9 px), AMBIGUOUS otherwise / no sectors. Usage: python -I pixel_collect.py LIST.csv OUT.csv"""
import sys, re, os, pandas as pd, numpy as np
lst = pd.read_csv(sys.argv[1]); rows = []
for _, r in lst.iterrows():
    f = f"/Users/fernando/Desktop/NASA/results/vet_qlp/{int(r.tic)}/ffi_pixel_summary.txt"; offs = []
    if os.path.exists(f):
        for line in open(f):
            m = re.search(r"offset ([0-9.]+) px", line)
            if m: offs.append(float(m.group(1)))
    status = "pending" if not os.path.exists(f) else ("no_data" if not offs else ("OFF_TARGET" if max(offs) >= 0.9 else ("ON_TARGET" if max(offs) <= 0.5 else "AMBIGUOUS")))
    rows.append(dict(tic=int(r.tic), period=r.period, t0=r.t0, dur_h=r.dur_h, depth_ppm=r.depth_ppm, sde=r.sde, next_sector=r.next_sector, group=r.group, prior_listed=r.prior_listed, n_sectors_tested=len(offs), max_offset_px=max(offs) if offs else np.nan, offsets=";".join(f"{o:.2f}" for o in offs), pixel_status=status))
out = pd.DataFrame(rows); out.to_csv(sys.argv[2], index=False); print(out.pixel_status.value_counts().to_dict())
print(out[out.pixel_status == "ON_TARGET"][["tic", "period", "depth_ppm", "sde", "next_sector", "group", "prior_listed", "offsets"]].to_string(index=False))
