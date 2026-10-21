"""Row/field-aware prior-report matcher (2026-10-21; replaces the inline "period within 200 characters of the TIC" heuristic of DECISIONS
113, after review F1/F5 in results/REVIEW_round4_freezes.md). For every tabular file (.csv, .tsv, .csv.gz, .tsv.gz; also tables inside .zip)
under the given roots, the header is parsed; a record counts only if a TIC column of that SAME record equals the target TIC and a named
period column of that record matches P, P/2 or 2P within 0.1 %. Excluded: our own records (paths with fergmolina__, Zenodo records whose
creators include "Molina, Fernando" per records_index.json) and neighbour/cone/target-list files. Every TIC-bearing record is written
with its provenance (file, 1-based data row, column names, period, ratio, relative difference, any flag/status fields), so a reader can
check each decision. Non-tabular text (md/txt/json/tex/html) is reported separately as TEXT_MENTION (TIC string only; not a match).
Usage: python -I prior_match.py TARGETS.csv OUT.csv ROOT [ROOT ...]   (TARGETS.csv columns: tic, period)"""
import sys, os, re, io, gzip, zipfile, json, pandas as pd, numpy as np
TARGETS, OUT, ROOTS = sys.argv[1], sys.argv[2], sys.argv[3:]
tg = pd.read_csv(TARGETS); T = {int(r.tic): float(r.period) for r in tg.itertuples()}; TS = {str(t) for t in T}
SKIP = ("fergmolina__", "tic_neighbours", "gaiadr3_cone", "vizier_allcat", "mast_hlsp_products", "tce_hits_targets_neighbours", "simbad_refs", "ztf_raw", "/lcs/", "_dryrun")
OWN = set()
for r in ROOTS:
    for dp, dn, fn in os.walk(r):
        if "records_index.json" in fn:
            for k, v in json.load(open(os.path.join(dp, "records_index.json"))).items():
                if any("Molina, Fernando" in c for c in v.get("creators", [])): OWN.add(str(k).split(".")[-1]); OWN.add(v.get("doi", "").split(".")[-1])
TICC = re.compile(r"^(tic|tic_?id|ticid|tic id|tic_number|target_tic|tess_id|id_tic)$", re.I); # 2026-10-21 (re-check R2): pipeline-prefixed names (bls_per, juliet_per, tls_period, ...) included; uncertainty columns excluded
PERC = re.compile(r"^((bls|tls|juliet|best|fit|orb|orbital|pl_orb|pl|koi|toi|tce)_?)?(period|per|p|orbper)(_?\(?(d|day|days)\)?)?$|^period \(days\)$", re.I)
PERX = re.compile(r"(unc|err|sig|lower|upper|_lo$|_hi$|min$|max$)", re.I)
FLAGC = re.compile(r"(flag|fail|status|disposition|known|comment|note|tier|verdict|class|^label$|^cls$|prob)", re.I)
def own(p): return any(k in p for k in SKIP) or any(f"/{z}" in p or f"{z}_" in os.path.basename(p) for z in OWN if z)
def tables(p):
    b = os.path.basename(p).lower()
    if b.endswith((".csv", ".tsv")): yield p, open(p, "rb").read()
    elif b.endswith((".csv.gz", ".tsv.gz")): yield p, gzip.open(p).read()
    elif b.endswith(".zip"):
        try:
            with zipfile.ZipFile(p) as z:
                for n in z.namelist():
                    if n.lower().endswith((".csv", ".tsv", ".csv.gz")) and "fergmolina" not in n:
                        x = z.read(n); yield f"{p}::{n}", (gzip.decompress(x) if n.lower().endswith(".gz") else x)
        except Exception: return
rows, text = [], []; TXT = re.compile(r"(?<!\d)(" + "|".join(sorted(TS)) + r")(?!\d)"); nf = 0
for root in ROOTS:
    for dp, dn, fn in os.walk(root):
        for f in fn:
            p = os.path.join(dp, f); nf += 1
            if nf % 2000 == 0: print("files", nf, p[-80:], file=sys.stderr, flush=True)
            try:
                if os.path.islink(p) or own(p) or os.path.getsize(p) > 400_000_000: continue
            except OSError: continue
            lo = f.lower()
            if lo.endswith((".md", ".txt", ".json", ".tex", ".html", ".py", ".cff")):
                try: s = open(p, errors="ignore").read()
                except Exception: continue
                for t in set(TXT.findall(s)): text.append(dict(tic=int(t), source=p, kind="TEXT_MENTION"))
                continue
            for name, raw in tables(p):
                if not any(t.encode() in raw for t in TS): continue
                first = raw.split(b"\n", 1)[0]; sep = max([b",", b"\t", b";", b"|"], key=first.count).decode()   # delimiter from the header line
                try: df = pd.read_csv(io.BytesIO(raw), sep=sep, dtype=str, keep_default_na=False, on_bad_lines="skip", low_memory=False)
                except Exception as e: text.append(dict(tic=-1, source=name, kind=f"UNPARSED {type(e).__name__}")); continue
                tcols = [c for c in df.columns if TICC.match(str(c).strip())]; pcols = [c for c in df.columns if PERC.match(str(c).strip()) and not PERX.search(str(c))]
                fcols = [c for c in df.columns if FLAGC.search(str(c))][:6]
                if not tcols:
                    for t in TS:
                        if t.encode() in raw: text.append(dict(tic=int(t), source=name, kind="TABLE_NO_TIC_COLUMN"))
                    continue
                for tc in tcols:
                    v = pd.to_numeric(df[tc].astype(str).str.replace(r"^TIC[ _-]?", "", regex=True), errors="coerce")
                    for i in np.where(v.isin(list(T)))[0]:
                        tic = int(v.iloc[i]); P = T[tic]; best = None
                        for pc in pcols:
                            x = pd.to_numeric(df[pc].iloc[i], errors="coerce")
                            if not np.isfinite(x) or x <= 0: continue
                            for k in (0.5, 1.0, 2.0):
                                d = abs(x - k * P) / (k * P)
                                if best is None or d < best[3]: best = (pc, x, k, d)
                        rows.append(dict(tic=tic, source=name, data_row=int(i) + 1, tic_col=tc, period_col=best[0] if best else "", period=best[1] if best else np.nan,
                                         ratio=best[2] if best else np.nan, rel_diff=best[3] if best else np.nan, match=bool(best and best[3] < 1e-3),
                                         flags=" | ".join(f"{c}={df[c].iloc[i]}" for c in fcols if str(df[c].iloc[i]).strip())[:300], decision="PERIOD_MATCH" if best and best[3] < 1e-3 else ("TIC_ONLY_NO_PERIOD_FIELD" if not best else "TIC_ONLY_PERIOD_DIFFERS")))
o = pd.DataFrame(rows); o.to_csv(OUT, index=False)
if len(o): o[o.decision == "TIC_ONLY_NO_PERIOD_FIELD"].drop_duplicates("source")[["source", "tic_col"]].assign(note="TIC-bearing table with no recognised period column: UNRESOLVED (not a negative period search)").to_csv(OUT.replace(".csv", "_unresolved.csv"), index=False); pd.DataFrame(text).drop_duplicates().to_csv(OUT.replace(".csv", "_text.csv"), index=False)
print("records", len(o), "| period matches", int(o.match.sum()) if len(o) else 0, "| own zenodo ids excluded", len(OWN))
if len(o): print(o[o.match].groupby("tic").source.apply(lambda s: "; ".join(sorted({x.split("/github/")[-1].split("/github_sweep/")[-1].split("/")[0] for x in s}))).to_string())
