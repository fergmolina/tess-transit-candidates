"""Binding checks for scored tests WITHOUT a QLP clock gate (2026-10-24; DECISIONS 175, 179): SPOC 2-min tests scored by the TIC 317134140
dedicated scorer scripts/prereg_spoc_317134140.py (and, from v1.19, scripts/prereg_conformance_spoc.py). Mirrors
scripts/validate_round4_inputs.py without its clock stages (SPOC times are target-barycentric; no clock record exists). Fails closed.
  --stage pre       --config C                   before ANY test-sector data access: C's SHA-256 is in the lock; its prediction CSV
                                                 bytes and the locked code (scorer + tsearch.py + search_pipeline.py, or evaluator) match.
  --stage selection --config C --selection SEL   before download: SEL is a metadata-only spoc_selection record (scripts/spoc_selection.py
                                                 select) for this TIC and sector. Its response hash is RECOMPUTED from its saved rows, and
                                                 its candidates/status/selected summary is RE-DERIVED with spoc_selection.derive() and must
                                                 match exactly (status SELECTED). Its query time is a valid UTC timestamp later than the lock
                                                 and AT OR BEFORE the config's unavailable_cutoff_utc (else the sector is UNAVAILABLE).
  --stage result    --config C --selection SEL --acquisition ACQ --lc L --result E
                                                 after scoring: everything in 'selection', plus ACQ is a mast_download acquisition record
                                                 of exactly SEL (by SHA-256) and of exactly L (file name, SHA-256), downloaded after SEL
                                                 was made (parsed timestamps; acquisition may be after the cutoff); and E was made from exactly C, by the locked code, from L.
Exit 0 = bound; exit 2 = refused. Usage: python -I validate_nonclock_inputs.py --lock LOCK --stage S --config C [...]"""
import sys, os, re, json, hashlib, argparse
R = "/Users/fernando/Desktop/NASA"; sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
HEX = lambda v: isinstance(v, str) and re.fullmatch(r"[0-9a-f]{64}", v) is not None
SPOC_NAME = re.compile(r"^tess(\d{13})-s(\d{4})-(\d{16})-(\d{4})-s_lc\.fits$")
ap = argparse.ArgumentParser(); ap.add_argument("--lock", required=True); ap.add_argument("--stage", required=True, choices=["pre", "selection", "result"])
ap.add_argument("--config", required=True); ap.add_argument("--selection"); ap.add_argument("--acquisition"); ap.add_argument("--lc"); ap.add_argument("--result"); a = ap.parse_args()
def refuse(m): print("REFUSED:", m); sys.exit(2)
def load(p, what):
    try: return json.load(open(p))
    except (OSError, ValueError, TypeError) as e: refuse(f"{what} unreadable ({type(e).__name__})")
lock = load(a.lock, "lock"); cs = sha(a.config); L = next((v for v in lock.get("configs", {}).values() if v.get("config_sha256") == cs), None)
if L is None: refuse(f"config SHA-256 {cs[:16]} is not in the lock manifest")
c = load(a.config, "config")
for k in ("tic", "sector", "pred_sha256"):
    if c.get(k) != L.get(k): refuse(f"config {k} differs from the lock")
if not os.path.exists(c.get("pred_csv", "")) or sha(c["pred_csv"]) != L["pred_sha256"]: refuse("prediction CSV bytes differ from the lock")
code = {k: v for k, v in L.items() if k.endswith("_code_sha256")}
if not code or f"{L.get('scoring_code')}_code_sha256" not in code: refuse("lock entry names no scoring-code hash")
for k, want in code.items():
    path = f"{R}/scripts/{k[:-len('_code_sha256')]}.py"
    if not HEX(want) or not os.path.exists(path) or sha(path) != want: refuse(f"{os.path.basename(path)} SHA-256 differs from the lock")
import datetime
def ts(v, what):
    """Strict UTC timestamp (YYYY-MM-DDTHH:MM:SS[.ffffff]Z); malformed -> refused."""
    for fmt in ("%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%SZ"):
        try: return datetime.datetime.strptime(str(v), fmt).replace(tzinfo=datetime.UTC)
        except ValueError: pass
    refuse(f"{what} {str(v)[:40]!r} is not a UTC timestamp")
if a.stage in ("selection", "result"):
    if not a.selection: refuse("--selection is required at this stage")
    if "spoc_selection_code_sha256" not in L: refuse("lock entry does not bind scripts/spoc_selection.py")
    sys.path.insert(0, f"{R}/scripts"); import spoc_selection as X          # bytes already checked against the lock above
    s = load(a.selection, "selection record")
    if s.get("record") != "spoc_selection" or s.get("product") != "SPOC_2MIN_LC": refuse("not a spoc_selection record for SPOC_2MIN_LC")
    if s.get("tic") != c["tic"] or s.get("sector") != c["sector"]: refuse("selection record TIC/sector differs from the config")
    if s.get("mode") != "mast_query": refuse(f"selection record mode {str(s.get('mode'))[:40]} is not a MAST query")
    orows, prows = s.get("observations"), s.get("products")
    if not isinstance(orows, list) or not isinstance(prows, list): refuse("selection record lacks its saved observation/product rows")
    if s.get("response_sha256") != X.response_digest(orows, prows): refuse("selection response hash does not match the saved rows")
    d = X.derive(c["tic"], c["sector"], orows, prows)
    if dict(candidates=s.get("candidates"), status=s.get("status"), selected=s.get("selected")) != d: refuse(f"selection summary differs from the saved rows (re-derived status {d['status']})")
    if d["status"] != "SELECTED": refuse(f"selection status {d['status']} with {len(d['candidates'])} candidates (not scorable)")
    sel = d["selected"]
    made, q, cut = ts(lock.get("made_utc_iso"), "lock time"), ts(s.get("query_utc"), "selection query_utc"), ts(c.get("unavailable_cutoff_utc"), "config cutoff")
    if not q > made: refuse("selection record is not later than the lock")
    if q > cut: refuse(f"UNAVAILABLE: no SELECTED record made by the cutoff {c['unavailable_cutoff_utc']} (this one is later)")
if a.stage == "result":
    if not (a.acquisition and a.lc and a.result): refuse("--acquisition, --lc and --result are required at this stage")
    qa = load(a.acquisition, "acquisition record"); e = load(a.result, "scorer output"); lcsha = sha(a.lc)
    if qa.get("record") != "spoc_acquisition" or qa.get("mode") != "mast_download": refuse("not a mast_download spoc_acquisition record")
    if qa.get("selection_sha256") != sha(a.selection): refuse("acquisition record was made from a different selection record")
    if qa.get("tic") != c["tic"] or qa.get("sector") != c["sector"]: refuse("acquisition record TIC/sector differs from the config")
    if qa.get("data_uri") != sel["dataURI"] or qa.get("filename") != sel["filename"] or os.path.basename(a.lc) != sel["filename"]: refuse("scored file is not the selected file")
    if qa.get("file_sha256") != lcsha: refuse("scored file bytes differ from the acquired file")
    if not ts(qa.get("download_utc"), "acquisition download_utc") > q: refuse("acquisition is not later than the selection")
    for f in ("config_sha256", "script_sha256", "lc_sha256"):
        if not HEX(e.get(f)): refuse(f"output {f} is missing or not a SHA-256")
    if e["config_sha256"] != cs: refuse("output was made from a different config")
    if e["script_sha256"] != L[f"{L['scoring_code']}_code_sha256"]: refuse("output was made by different scoring code")
    if e["lc_sha256"] != lcsha: refuse("output was made from a different light curve")
    if not e.get("outcome"): refuse("output has no outcome")
print(f"BOUND: stage {a.stage}, {os.path.basename(a.config)} (lock {sha(a.lock)[:16]})")
