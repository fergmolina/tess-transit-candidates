"""pixel_collect v2 (2026-10-22; round-5 review R5-5). Same thresholds as pixel_collect.py (ON <= 0.5 px, OFF >= 0.9 px) but:
- offsets read at full precision from results/vet_qlp/<TIC>/ffi_pixel_S<sector>.json (loss_offset_px), not the rounded summary text;
- sectors counted separately: attempted (summary line, JSON, or a 'sector N failed' / 'no TESScut for sector N' line in
  logs/ffi_pixel_<TIC>.log), finite (offset measured), nonfinite (offset NaN), failed (download/processing failure);
- acceptance rule for invalid sectors: OFF_TARGET if any finite offset >= 0.9 px; ON_TARGET only if every attempted sector gave a finite
  offset <= 0.5 px; an object whose finite offsets are all <= 0.5 px but with a non-finite or failed sector is AMBIGUOUS_INCOMPLETE.
  ON_TARGET is a finite-offset screen, not a neighbour exclusion.
The v1 output is not modified. Usage: python -I pixel_collect_v2.py IN.csv OUT.csv  (IN = any v1 output or input list with a tic column)"""
import sys, re, os, glob, json, math, pandas as pd
R = "/Users/fernando/Desktop/NASA"
lst = pd.read_csv(sys.argv[1]); rows = []
for tic in lst.tic.astype(int).drop_duplicates():
    d = f"{R}/results/vet_qlp/{tic}"; summ = f"{d}/ffi_pixel_summary.txt"; att, fin, nonfin, failed = set(), {}, [], []
    if os.path.exists(summ):
        for line in open(summ):
            m = re.match(r"S(\d+):", line)
            if m: att.add(int(m.group(1)))
    for j in glob.glob(f"{d}/ffi_pixel_S*.json"):
        js = json.load(open(j)); s = int(js["sector"]); att.add(s); o = js.get("loss_offset_px")
        if o is not None and math.isfinite(float(o)): fin[s] = float(o)
        else: nonfin.append(s)
    lg = f"{R}/logs/ffi_pixel_{tic}.log"
    if os.path.exists(lg):
        for line in open(lg, errors="replace"):
            m = re.match(r"(?:sector (\d+) failed|no TESScut for sector (\d+))", line)
            if m: s = int(m.group(1) or m.group(2)); att.add(s); failed.append(s)
    for s in att:
        if s not in fin and s not in nonfin and s not in failed: nonfin.append(s)   # summary line without a usable JSON
    mx = max(fin.values()) if fin else float("nan")
    if not os.path.exists(summ) and not att: st = "pending"
    elif not fin: st = "no_data"
    elif mx >= 0.9: st = "OFF_TARGET"
    elif mx <= 0.5: st = "ON_TARGET" if not nonfin and not failed else "AMBIGUOUS_INCOMPLETE"
    else: st = "AMBIGUOUS"
    rows.append(dict(tic=tic, n_attempted=len(att), n_finite=len(fin), nonfinite_sectors=";".join(map(str, sorted(set(nonfin)))),
                     failed_sectors=";".join(map(str, sorted(set(failed)))), max_offset_px=mx,
                     offsets_full=";".join(f"S{s}:{fin[s]:.6f}" for s in sorted(fin)), pixel_status_v2=st))
out = pd.DataFrame(rows)
v1 = lst.drop_duplicates("tic").set_index("tic").pixel_status if "pixel_status" in lst else None
if v1 is not None: out["pixel_status_v1"] = out.tic.map(v1)
out.to_csv(sys.argv[2], index=False); print(out.pixel_status_v2.value_counts().to_dict())
if v1 is not None:
    ch = out[out.pixel_status_v1 != out.pixel_status_v2]; print("changed:", len(ch)); print(ch[["tic", "pixel_status_v1", "pixel_status_v2", "max_offset_px", "nonfinite_sectors", "failed_sectors"]].to_string(index=False))
