"""Shared time helpers (2026-10-20, v1.12; full-repo review F5). BJD_TDB -> geocentric UTC: subtract the barycentric light-travel time
toward the target, then convert the time scale. Time(jd, scale='tdb').utc alone only changes the scale (off by up to +-8 min), and
reading a BJD number directly as a UTC calendar date is off by a further ~69 s."""
from astropy.time import Time
def geocentric_utc(jd_tdb, ra_deg, dec_deg):
    from astropy.coordinates import SkyCoord, EarthLocation; import astropy.units as u
    t = Time(jd_tdb, format="jd", scale="tdb")
    ltt = t.light_travel_time(SkyCoord(ra_deg, dec_deg, unit="deg"), kind="barycentric", location=EarthLocation.from_geocentric(0, 0, 0, unit=u.m))
    return (t - ltt).utc
