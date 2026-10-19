"""Sector-104 QLP clock check for TIC 89247735 (round-3 external referee, issue 1).
QLP and TESScut cutouts of the same FFIs have identical cadence counts, so data-gap edges give an unambiguous time offset between the two
products. TESScut TIME carries a per-target TIMECORR and is taken as the reference clock; the S66/S93 offset (+0.2 min, a cadence-time
convention difference) is the control. The S104 correction is the offset at the event minus the control offset."""
import glob, json, numpy as np
from astropy.io import fits
OUT = "/Users/fernando/Desktop/NASA/results/referee_89247735/round3_fixes"
def gap_offsets(s):
    q = fits.getdata(glob.glob(f"/Users/fernando/Desktop/NASA/data/qlp/hlsp_qlp_tess_ffi_s{s:04d}-0000000089247735*")[0], 1)
    d = fits.getdata(glob.glob(f"/Users/fernando/Desktop/NASA/data/lk_cache/tesscut/tess-s{s:04d}-*275.22*")[0], 1)
    tq = q["TIME"][np.isfinite(q["TIME"])]; tc = d["TIME"][np.isfinite(d["TIME"]) & (d["TIME"] > 0)]
    assert len(tq) == len(tc), (s, len(tq), len(tc))
    dt = (tq - tc) * 1440   # identical cadence lists -> element-wise offset
    return tq, dt, float(np.median(d["TIMECORR"]) * 1440)
res = {}
for s in (66, 93, 104):
    t, dt, tcorr = gap_offsets(s); res[s] = dict(t=t, dt=dt, timecorr_min=tcorr)
    print(f"S{s}: QLP-TESScut median {np.median(dt):+.2f} min, range {dt.min():+.2f}..{dt.max():+.2f}; TESScut TIMECORR {tcorr:.2f} min")
ctrl = float(np.median(np.concatenate([res[66]["dt"], res[93]["dt"]])))
TQ = 4196.8043   # v2 QLP retiming of the S104 event
off = float(np.interp(TQ, res[104]["t"], res[104]["dt"])); corr = ctrl - off
local = res[104]["dt"][np.abs(res[104]["t"] - TQ) < 0.5]
print(f"control offset {ctrl:+.3f} min; S104 offset at event {off:+.3f} min (+-0.5 d spread {local.min():+.2f}..{local.max():+.2f}); correction to add to QLP S104 times {corr:+.3f} min")
print(f"corrected S104 QLP event time BTJD {TQ + corr/1440:.5f}")
json.dump(dict(control_offset_min=ctrl, s104_offset_at_event_min=off, correction_min=corr, corrected_tc=TQ + corr / 1440,
               local_spread_min=[float(local.min()), float(local.max())], timecorr_min={s: res[s]["timecorr_min"] for s in res}), open(f"{OUT}/s104_clock.json", "w"), indent=1)
