"""Grep the prior-detection sweep corpus (cloned GitHub repos, Zenodo file texts) for TIC numbers, excluding our own repository copies and
pure catalog/neighbour lists. Usage: python -I prior_grep.py TIC [TIC ...]  -> hits with 120-char context."""
import sys, os, re
ROOT = "/Users/fernando/Desktop/NASA/results/prior_search/data"; SKIP = ("fergmolina__", "tic_neighbours", "gaiadr3_cone", "exofop_", "/tce", "bulk_downloads", "tessspoc_dv", "tesscurl_sector", "23460915", "23443245", "23445705", "23462")
files = []
for dp, dn, fn in os.walk(ROOT):
    for f in fn:
        p = os.path.join(dp, f)
        if any(k in p for k in SKIP) or os.path.getsize(p) > 200_000_000: continue
        if f.endswith((".csv", ".md", ".txt", ".json", ".py", ".tex", ".cff", ".html")): files.append(p)
for tic in sys.argv[1:]:
    hits = []
    for p in files:
        try: s = open(p, errors="ignore").read()
        except Exception: continue
        i = s.find(tic)
        if i >= 0: hits.append((p.replace(ROOT + "/", ""), s[max(0, i - 90):i + 70].replace("\n", " ")))
    print(f"== {tic}: {len(hits)} hit(s)")
    for p, c in hits[:4]: print(f"   {p}\n      ...{c}...")
