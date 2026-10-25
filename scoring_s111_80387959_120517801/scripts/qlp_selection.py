"""Release-of-record records for QLP light curves (v1.19, 2026-10-25; DECISIONS 193-194). This is the QLP counterpart of
scripts/spoc_selection.py, which v1.18 binds and which is not changed.
  select  --tic T --sector N --out SEL.json
      METADATA ONLY. Queries MAST for QLP HLSP time series (obs_collection HLSP, provenance_name QLP) of this TIC and sector and saves
      every observation and product row, with the SHA-256 of their canonical JSON. The eligible product is the release of record v01:
      hlsp_qlp_tess_ffi_s<SSSS>-<TIC 16 digits>_tess_v01_llc.fits. Status is SELECTED if exactly one is listed (with a 'mast:' dataURI
      and exactly one observation row with the same valid obs_id); otherwise NONE, AMBIGUOUS or INCOMPLETE. Nothing is chosen
      silently. The record keeps the observation release date t_obs_release (MJD), which the S111 rule uses.
  acquire --selection SEL.json --out-dir DIR --record ACQ.json
      Downloads exactly the selected dataURI and records the selection record's SHA-256 and the file's SHA-256. Refuses unless the
      status is SELECTED. This downloads photometry: run it only for a test whose route is settled and that is approved for scoring.
derive() is shared with scripts/validate_s111_inputs.py. --from-response replaces the MAST query (tests only; the record says so)."""
import sys, os, re, json, hashlib, argparse, datetime
QLP_NAME = re.compile(r"^hlsp_qlp_tess_ffi_s(\d{4})-(\d{16})_tess_(v\d+)_llc\.fits$")
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
now = lambda: datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
canon = lambda obj: hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str).encode()).hexdigest()
def response_digest(orows, prows): return canon(dict(observations=orows, products=prows))
def valid_id(v): return isinstance(v, str) and v.strip() == v and v != "" and v.lower() not in ("none", "null", "nan", "--", "n/a")

def derive(tic, sector, orows, prows):
    cand = [r for r in prows if (m := QLP_NAME.match(str(r.get("productFilename", "")))) and int(m.group(1)) == sector and int(m.group(2)) == tic and m.group(3) == "v01"]
    names = [r["productFilename"] for r in cand]
    if not cand: return dict(candidates=names, status="NONE", selected=None)
    if len(cand) > 1: return dict(candidates=names, status="AMBIGUOUS", selected=None)
    r = cand[0]; oid = r.get("obs_id")
    if not valid_id(oid) or not str(r.get("dataURI") or "").startswith("mast:"): return dict(candidates=names, status="INCOMPLETE", selected=None)
    obs = [o for o in orows if valid_id(o.get("obs_id")) and o["obs_id"] == oid]
    if len(obs) != 1: return dict(candidates=names, status="INCOMPLETE", selected=None)
    return dict(candidates=names, status="SELECTED", selected=dict(filename=r["productFilename"], dataURI=r["dataURI"], obsID=r.get("obsID"), obs_id=oid,
                release="v01", size=r.get("size"), t_obs_release=[obs[0].get("t_obs_release")]))

def query_rows(tic, sector):
    from astroquery.mast import Observations
    obs = Observations.query_criteria(obs_collection="HLSP", provenance_name="QLP", target_name=str(tic), sequence_number=sector)
    if len(obs) == 0: return [], []
    prods = Observations.get_product_list(obs)
    keep = ("obsid", "obs_id", "target_name", "sequence_number", "t_obs_release", "provenance_name", "dataURL")
    return ([{k: (str(r[k]) if k in obs.colnames else None) for k in keep} for r in obs], [{k: str(r[k]) for k in prods.colnames} for r in prods])

def select(a):
    if os.path.exists(a.out): raise SystemExit(f"refused: {a.out} exists")
    t = now()
    if a.from_response: src = json.load(open(a.from_response)); orows, prows = src["observations"], src["products"]; mode = f"from_response:{os.path.basename(a.from_response)}"
    else: orows, prows = query_rows(a.tic, a.sector); mode = "mast_query"
    import importlib.metadata
    d = derive(a.tic, a.sector, orows, prows)
    rec = dict(record="qlp_selection", version="1.0", tic=a.tic, sector=a.sector, product="QLP_V01_LLC", mode=mode, query_utc=t,
               query=dict(obs_collection="HLSP", provenance_name="QLP", target_name=str(a.tic), sequence_number=a.sector),
               astroquery=importlib.metadata.version("astroquery"), observations=orows, products=prows, response_sha256=response_digest(orows, prows),
               candidates=d["candidates"], status=d["status"], selected=d["selected"])
    json.dump(rec, open(a.out, "w"), indent=1); print(d["status"], (d["selected"] or {}).get("filename", d["candidates"]))

def make_acquisition(sel_path, file_path, mode, download_utc=None):
    s = json.load(open(sel_path))
    return dict(record="qlp_acquisition", version="1.0", selection_file=os.path.basename(sel_path), selection_sha256=sha(sel_path), tic=s["tic"], sector=s["sector"],
                mode=mode, data_uri=s["selected"]["dataURI"], filename=os.path.basename(file_path), file_sha256=sha(file_path), size=os.path.getsize(file_path),
                download_utc=download_utc or now())

def acquire(a):
    if os.path.exists(a.record): raise SystemExit(f"refused: {a.record} exists")
    s = json.load(open(a.selection))
    if s.get("status") != "SELECTED": raise SystemExit(f"refused: selection status {s.get('status')}")
    dst = os.path.join(a.out_dir, s["selected"]["filename"])
    if os.path.exists(dst): raise SystemExit(f"refused: {dst} exists")
    os.makedirs(a.out_dir, exist_ok=True)
    from astroquery.mast import Observations
    st, msg, _ = Observations.download_file(s["selected"]["dataURI"], local_path=dst)
    if st != "COMPLETE" or not os.path.exists(dst): raise SystemExit(f"download failed: {st} {msg}")
    json.dump(make_acquisition(a.selection, dst, "mast_download"), open(a.record, "w"), indent=1); print("acquired", dst)

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); sp = ap.add_subparsers(dest="cmd", required=True)
    p = sp.add_parser("select"); p.add_argument("--tic", type=int, required=True); p.add_argument("--sector", type=int, required=True); p.add_argument("--out", required=True); p.add_argument("--from-response")
    p = sp.add_parser("acquire"); p.add_argument("--selection", required=True); p.add_argument("--out-dir", required=True); p.add_argument("--record", required=True)
    a = ap.parse_args(); select(a) if a.cmd == "select" else acquire(a)
