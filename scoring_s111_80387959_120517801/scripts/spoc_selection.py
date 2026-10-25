"""Release-of-record binding for SPOC 2-min scoring (2026-10-24; DECISIONS 179; review G2). Two steps, each writing a record that is never
overwritten:
  select  --tic T --sector S --out SEL.json
      METADATA ONLY (no file is downloaded). Queries MAST (astroquery Observations) for TESS 2-min time-series observations of this TIC
      and sector, lists their products, and keeps the SPOC 2-min light curves: file names matching
      tess<13 digits>-s<SSSS>-<TIC 16 digits>-<4 digits>-s_lc.fits. This excludes 20-s 'fast-lc', TESS-SPOC FFI HLSPs and QLP.
      The record stores the query parameters, the UTC time, the astroquery version, every product row of the matched observations and
      the SHA-256 of their canonical JSON. Status is SELECTED if exactly one candidate is listed (with a 'mast:' dataURI and its
      observation row), NONE if none, AMBIGUOUS if more than one and INCOMPLETE otherwise; nothing is chosen silently. The derivation is
      the function derive(), which the validator re-runs on the saved rows.
      Rule: the selection record is made at the first check after a SPOC 2-min light curve of this TIC and sector is listed at MAST
      (the monitoring agent reports new listings). The release of record is the eligible version listed at the FIRST RECORDED CHECK;
      an earlier, replaced delivery cannot be excluded, because MAST lists the current version only. The record stores the observation
      release date (t_obs_release) and the file's pipeline field, and DATA_REL is recorded from the header at scoring, so any
      reprocessing is disclosed. All selection records made, including NONE ones, are kept.
      Monitoring and cutoff: see the config's monitoring_rule. The sector's config fixes unavailable_cutoff_utc (sector end + 120 days, inclusive). A SELECTED record made at or before
      the cutoff permits acquisition and scoring at any later time. If no SELECTED record exists by then, the sector is UNAVAILABLE, and
      a later listing is a secondary readout only.
  acquire --selection SEL.json --out-dir DIR --record ACQ.json
      Downloads exactly the selected dataURI, then records the selection record's SHA-256, the file name, the file's SHA-256 and size,
      and the UTC time. Refuses unless the status is SELECTED. This step downloads photometry: run it only for a test that is declared
      and approved for scoring.
scripts/validate_nonclock_inputs.py --stage result requires both records and checks them against the scored light curve and the output.
Usage: python -I spoc_selection.py select|acquire ...   (--from-response ROWS.json replaces the MAST query; for tests only, recorded)"""
import sys, os, re, json, hashlib, argparse, datetime
SPOC_NAME = re.compile(r"^tess(\d{13})-s(\d{4})-(\d{16})-(\d{4})-s_lc\.fits$")
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
now = lambda: datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
canon = lambda obj: hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str).encode()).hexdigest()

def query_rows(tic, sector):
    from astroquery.mast import Observations
    obs = Observations.query_criteria(obs_collection="TESS", dataproduct_type="timeseries", target_name=str(tic), sequence_number=sector)
    if len(obs) == 0: return [], []
    prods = Observations.get_product_list(obs)
    keep_o = ("obsid", "obs_id", "target_name", "sequence_number", "t_exptime", "t_obs_release", "provenance_name", "dataURL")
    orows = [{k: (str(r[k]) if k in obs.colnames else None) for k in keep_o} for r in obs]
    prow = [{k: str(r[k]) for k in prods.colnames} for r in prods]
    return orows, prow

def response_digest(orows, prows): return canon(dict(observations=orows, products=prows))

def valid_id(v):
    """A usable observation identifier: a non-empty string, not whitespace-padded, not a placeholder. Absent, null or empty ids never
    establish a product-observation association (re-check 2)."""
    return isinstance(v, str) and v.strip() == v and v != "" and v.lower() not in ("none", "null", "nan", "--", "n/a")

def derive(tic, sector, orows, prows):
    """The ONE derivation of candidates / status / selected from the saved MAST rows, used by 'select' and by
    validate_nonclock_inputs.py (which recomputes it and refuses any record whose summary differs). SELECTED requires exactly one
    candidate, a 'mast:' dataURI, a valid obs_id (valid_id) and exactly one observation row with that same valid obs_id."""
    cand = [r for r in prows if (m := SPOC_NAME.match(str(r.get("productFilename", "")))) and int(m.group(2)) == sector and int(m.group(3)) == tic]
    names = [r["productFilename"] for r in cand]
    if not cand: return dict(candidates=names, status="NONE", selected=None)
    if len(cand) > 1: return dict(candidates=names, status="AMBIGUOUS", selected=None)
    r = cand[0]; m = SPOC_NAME.match(r["productFilename"]); oid = r.get("obs_id")
    if not valid_id(oid) or not str(r.get("dataURI") or "").startswith("mast:"): return dict(candidates=names, status="INCOMPLETE", selected=None)
    obs = [o for o in orows if valid_id(o.get("obs_id")) and o["obs_id"] == oid]
    if len(obs) != 1: return dict(candidates=names, status="INCOMPLETE", selected=None)
    return dict(candidates=names, status="SELECTED", selected=dict(filename=r["productFilename"], dataURI=r["dataURI"], obsID=r.get("obsID"), obs_id=r.get("obs_id"),
                pipeline_field=m.group(4), size=r.get("size"), t_obs_release=[obs[0].get("t_obs_release")]))

def select(a):
    if os.path.exists(a.out): raise SystemExit(f"refused: {a.out} exists")
    t_query = now()
    if a.from_response:
        src = json.load(open(a.from_response)); orows, prows = src["observations"], src["products"]; mode = f"from_response:{os.path.basename(a.from_response)}"
    else:
        orows, prows = query_rows(a.tic, a.sector); mode = "mast_query"
    import importlib.metadata
    d = derive(a.tic, a.sector, orows, prows); status, sel = d["status"], d["selected"]
    rec = dict(record="spoc_selection", version="1.0", tic=a.tic, sector=a.sector, product="SPOC_2MIN_LC", mode=mode, query_utc=t_query,
               query=dict(obs_collection="TESS", dataproduct_type="timeseries", target_name=str(a.tic), sequence_number=a.sector),
               astroquery=importlib.metadata.version("astroquery"), observations=orows, products=prows,
               response_sha256=response_digest(orows, prows), candidates=d["candidates"], status=status, selected=sel,
               rule="first check after a SPOC 2-min s_lc.fits of this TIC and sector is listed at MAST; exactly one candidate required")
    json.dump(rec, open(a.out, "w"), indent=1); print(status, sel["filename"] if sel else d["candidates"])

def make_acquisition(sel_path, file_path, mode, download_utc=None):
    s = json.load(open(sel_path))
    return dict(record="spoc_acquisition", version="1.0", selection_file=os.path.basename(sel_path), selection_sha256=sha(sel_path), tic=s["tic"], sector=s["sector"],
                mode=mode, data_uri=s["selected"]["dataURI"], filename=os.path.basename(file_path), file_sha256=sha(file_path), size=os.path.getsize(file_path),
                download_utc=download_utc or now())

def acquire(a):
    if os.path.exists(a.record): raise SystemExit(f"refused: {a.record} exists")
    s = json.load(open(a.selection))
    if s.get("status") != "SELECTED": raise SystemExit(f"refused: selection status {s.get('status')}")
    dst = os.path.join(a.out_dir, s["selected"]["filename"])
    if os.path.exists(dst): raise SystemExit(f"refused: {dst} exists (download into a fresh directory)")
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
