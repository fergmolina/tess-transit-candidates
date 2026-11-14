"""EXPLORATORY, POST-OUTCOME addendum to item 1 (PLAN.md): QUALITY flags of the Sector 108 rows whose PDCSAP flux is not finite."""
import json, numpy as np
from astropy.io import fits
R = "/Users/fernando/Desktop/NASA"; E = f"{R}/results/exploratory_317134140_S108"
with fits.open(f"{R}/results/test_317134140/S108/lc/tess2026250081459-s0108-0000000317134140-0310-s_lc.fits", memmap=False) as h:
    d = h[1].data; t = np.asarray(d["TIME"], float); f = np.asarray(d["PDCSAP_FLUX"], float); fe = np.asarray(d["PDCSAP_FLUX_ERR"], float); q = np.asarray(d["QUALITY"], int); sap = np.asarray(d["SAP_FLUX"], float)
bad = np.isfinite(t) & ~(np.isfinite(f) & np.isfinite(fe)); out = dict(n_rows=int(bad.sum()), quality_zero=int((q[bad] == 0).sum()), sap_finite=int(np.isfinite(sap[bad]).sum()),
    bits={str(b): int(((q[bad] >> b) & 1).sum()) for b in range(16) if ((q[bad] >> b) & 1).sum()}, quality_values={str(v): int(c) for v, c in zip(*np.unique(q[bad], return_counts=True))})
tb = t[bad]; gi = np.where(np.diff(tb) > 0.05)[0]; s = [tb[0]] + [tb[i + 1] for i in gi]; e = [tb[i] for i in gi] + [tb[-1]]
out["runs_btjd"] = [[round(float(a), 3), round(float(b), 3), round(float(b - a), 3)] for a, b in zip(s, e) if b - a > 0.05]
out["quality_nonzero_among_finite_flux"] = int((q[np.isfinite(t) & np.isfinite(f) & np.isfinite(fe)] != 0).sum())
json.dump(out, open(f"{E}/quality_addendum.json", "w"), indent=1); print(json.dumps(out))
