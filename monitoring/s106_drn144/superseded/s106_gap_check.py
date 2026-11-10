"""Descriptive only, NO photometry: which frozen S106 predicted events fall in the data gaps reported in DRN 144 Table 1.
Kept intervals = DRN 144 segment times (spacecraft TJD, TDB) with the locked edge rule (drop 1.5 d after start/resume over a gap > 0.5 d;
drop 0.5 d before any gap > 0.1 d or data end). Barycentric correction (<= ~8 min) ignored; QLP's own quality flags unknown."""
import json, csv, glob
SEG = [(4233.42522, 4240.04466), (4240.25439, 4247.86410), (4248.07383, 4252.30716), (4254.91132, 4261.87521)]      # DRN 144
NOM = [(4233.4313, 4240.0529), (4240.2612, 4247.8724), (4248.0807, 4254.7092), (4254.9175, 4261.8828)]              # orbit table (UTC+69 s)
def kept(seg):
    out = []
    for i, (a, b) in enumerate(seg):
        gap_before = None if i == 0 else a - seg[i - 1][1]
        lo = a + 1.5 if (i == 0 or gap_before > 0.5) else a
        out.append((lo, b - 0.5))
    return out
K, KN = kept(SEG), kept(NOM)
inside = lambda t, h, ks: any(lo <= t - h and t + h <= hi for lo, hi in ks)
for p in sorted(glob.glob("configs/conformance/*_S106.json")):
    c = json.load(open(p)); h = c["ref_dur_h"] / 48.0
    ev = [(int(r["epoch"]), float(r["tc_btjd"])) for r in csv.DictReader(open(c["pred_csv"])) if r.get("tess_sector", "").strip() in ("106", "106.0")]
    el = [e for e, t in ev if inside(t, h, K)]; eln = [e for e, t in ev if inside(t, h, KN)]
    lost = [e for e in eln if e not in el]
    print(f"TIC {c['tic']:>10}  pred {len(ev):>2}  eligible nominal {len(eln):>2} -> with DRN gaps {len(el):>2}  newly lost {lost}  strict {c.get('strict_epochs')}")
    if len(ev) <= 6: print("      ", [(e, round(t, 3), 'kept' if e in el else 'out') for e, t in ev])
print("kept (DRN):", [(round(a, 3), round(b, 3)) for a, b in K])
