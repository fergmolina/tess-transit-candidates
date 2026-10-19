"""Second UTC correction (external referee round 3, issue 6, 2026-10-19): prereg_utc_fix.py added a geocentric 'utc_geocentric' mid-time
but left 'ingress_utc'/'egress_utc' as the old time-SCALE-only conversion, so the contacts were off by the same light-travel time as the
old mid-time (up to +-8 min). This script reads each *_utcfix.csv and writes *_utcfix2.csv with both contact columns shifted by the same
light-travel time as the mid-time (geocentric contact = old contact - ltt). Recomputed from tc_bjd_tdb, the old contact offsets from mid
(ingress/egress minus utc_tdb_scale_only) are preserved exactly. tc_bjd_tdb, the frozen files and their SHA-256, and the first
*_utcfix.csv files are untouched. Usage: python -I prereg_utc_fix2.py TIC RA DEC file_utcfix.csv [...]"""
import sys, hashlib, pandas as pd
from astropy.time import Time; from astropy.coordinates import SkyCoord, EarthLocation; import astropy.units as u
tic, ra, dec = int(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]); sc = SkyCoord(ra, dec, unit="deg"); loc = EarthLocation.from_geocentric(0, 0, 0, unit=u.m)
for f in sys.argv[4:]:
    p = pd.read_csv(f); t = Time(p.tc_bjd_tdb.values, format="jd", scale="tdb"); ltt = t.light_travel_time(sc, kind="barycentric", location=loc)
    geo = (t - ltt).utc; old_mid = Time(list(p.utc_tdb_scale_only), scale="utc")
    assert all(a[:16] == b for a, b in zip(geo.iso, p.utc_geocentric)), f"{f}: geocentric mid-times do not reproduce"
    for c in ("ingress_utc", "egress_utc"):
        off = Time(list(p[c]), scale="utc") - old_mid   # contact offset from mid as frozen (minute-rounded strings)
        p[c] = [x[:16] for x in (geo + off).iso]
    out = f.replace("_utcfix.csv", "_utcfix2.csv"); p.to_csv(out, index=False); sha = hashlib.sha256(open(out, "rb").read()).hexdigest()
    print(f"{out}: {len(p)} rows; SHA-256 {sha[:16]}"); print("   first row:", p.iloc[0][["epoch", "utc_geocentric", "ingress_utc", "egress_utc"]].tolist())
