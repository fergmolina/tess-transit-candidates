"""Correct the UTC column of frozen prediction CSVs (referee finding M1, 2026-10-19): the 'utc' column was Time(BJD_TDB).utc, i.e. a
time-SCALE conversion of the barycentric time, without removing the barycentric light-travel time; the geocentric arrival time differs by
-8 to +8 min depending on the date. BJD_TDB (the primary quantity, and all TESS/BTJD comparisons) is unaffected. This script writes a
corrected copy <name>_utcfix.csv next to each frozen file: tc_bjd_tdb unchanged, 'utc_geocentric' added (BJD_TDB minus the light-travel
time toward the target, geocentre), the old column kept as 'utc_tdb_scale_only' for traceability. The original frozen files and their
SHA-256 are untouched. Usage: python -I prereg_utc_fix.py TIC RA DEC file1.csv [file2.csv ...]"""
import sys, hashlib, pandas as pd
from astropy.time import Time; from astropy.coordinates import SkyCoord, EarthLocation; import astropy.units as u
tic, ra, dec = int(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]); sc = SkyCoord(ra, dec, unit="deg"); loc = EarthLocation.from_geocentric(0, 0, 0, unit=u.m)
for f in sys.argv[4:]:
    p = pd.read_csv(f); t = Time(p.tc_bjd_tdb.values, format="jd", scale="tdb"); ltt = t.light_travel_time(sc, kind="barycentric", location=loc); geo = (t - ltt).utc
    p = p.rename(columns={"utc": "utc_tdb_scale_only"}); p.insert(list(p.columns).index("utc_tdb_scale_only") + 1, "utc_geocentric", [x[:16] for x in geo.iso]); p["ltt_min"] = (ltt.to(u.min).value).round(1)
    out = f[:-4] + "_utcfix.csv"; p.to_csv(out, index=False); sha = hashlib.sha256(open(out, "rb").read()).hexdigest()
    print(f"{out}: {len(p)} rows; ltt range {p.ltt_min.min():+.1f} to {p.ltt_min.max():+.1f} min; SHA-256 {sha[:16]}")
