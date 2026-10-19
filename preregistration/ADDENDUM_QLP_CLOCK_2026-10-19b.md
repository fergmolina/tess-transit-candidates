# Dated addendum (revision b) — QLP barycentric clock error and the frozen predictions (2026-10-19)

**This supersedes ADDENDUM_QLP_CLOCK_2026-10-19.md (v1.8).** That version, and the TIC 89247735 v4 ephemeris, treated the TESScut `TIME`
as target-barycentric. It is not: TESScut `TIMECORR` is computed for an FFI reference position. A round-4 external review found this; we
checked it. In Sector 104 the TESScut correction at the event is 7.74 min, while the target's light-travel time is 7.42 min.

**Method 2** (`scripts/qlp_clock_v2.py`):
- spacecraft time = TESScut `TIME − TIMECORR`, matched to the QLP cadences;
- target light-travel time from JPL Horizons TESS barycentric vectors;
- QLP convention c0 = +0.033 min (≈2 s), from clean control sectors;
- correction = light-travel time + c0 − (QLP − spacecraft), evaluated at the event.

The frozen files are unchanged.

| Object | QLP sector corrections (min) | Shift of frozen predictions | Frozen 1σ |
|---|---|---|---|
| TIC 89247735 | S104 +7.53 (v1.8 said +8.02) | v5 ephemeris: +4.3 to +5.5 min vs v1 at epochs 146–163 | 3–4 min |
| TIC 183374279 | S103 −3.25, S105 +3.27 | +0.9 min (S106) | 2.7 min |
| TIC 120444365 | S103 −3.00, S105 +2.80 | +0.05 min (S106) | 2.1 min |
| TIC 80387959 | S100 +1.16 | +0.5 min (S111) | 3.5 min |
| TIC 258006047 | S99 0.00, S100 +1.33, S101 +3.75, S102 +3.80 | +3.6 min (S114) | 4.7 min |
| TIC 333735955 | S100 +1.07, S101 +2.78 | +3.2 min (S114) | 2.7 min |
| TIC 467959906 | S103 +3.87 | +3.9 min (S114) | 4.1 min |
| [withheld] | S100 +1.03 | +0.7 min (S111) | 15.9 min |

Observations (for the products checked; not a rule for every star in a sector):
- TIC 89247735 S104 and both S103/S105 products checked: QLP time equals spacecraft time to within about 5 s (5.1 s for TIC 89247735),
  i.e. the barycentric term is missing. Sector 105 is outside MAST's S99–S104 notice. TIC 258006047's S102 product behaves the same way
  (QLP − spacecraft = −1.2 s; missing term 3.75 min).
- S100–S101 products carry a substantial spurious term instead: −2.08 min for TIC 258006047, +4.60 min for TIC 333735955. MAST attributes
  the S99–S101 problem to an ephemeris-range/interpolation failure and dates the position/velocity column mix-up from Orbit 215 (first half of
  S102); we describe only the measured behaviour and do not assign a cause to individual sectors.
- Size of the shifts relative to the frozen 1σ:
  - the seven objects other than TIC 89247735 move by at most 1.2σ (1.18σ, TIC 333735955);
  - TIC 89247735's v5 refinement sits 1.25–1.38σ from v1 at epochs 146–163;
  - so across all eight the shifts are at most about 1.4σ.
- No outcome rule changes. Each test is evaluated around the frozen prediction, exactly as frozen; the clock-corrected prediction is
  reported alongside it for information only.
- Any QLP test data from S99 onward (including S106) will be checked with method 2 before a test is run.

Method notes (round-5 review): the light-travel time is evaluated at the reconstructed spacecraft time; control sectors are unique and
exclude S74–S79 v01, which MAST lists with a separate timing issue; equal-length cadence lists are verified increment by increment.
Re-running with these changes moves every correction by less than 0.01 s. The v5 ephemeris (frozen with +7.533022 min, now +7.533124)
is unaffected at its stored precision. The 0.05-min clock term is an adopted conservative allowance: the independent checks agree to
0.006 s, but no absolute spacecraft-clock error budget has been derived.
