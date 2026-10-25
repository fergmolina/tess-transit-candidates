"""Append-only, hash-chained ledger of every metadata check and acquisition for ONE TIC and sector of the S111+ tests (v1.19, 2026-10-25;
DECISIONS 193-195; review S111-3/4). The validator (scripts/validate_s111_inputs.py) replays the same function, replay(), so the route it
accepts is the route the recorded history implies.
  init   --ledger DIR --tic T --sector N --lock-qlp LQ --lock-spoc LS   fresh ledger bound to BOTH locks' SHA-256 and their shared time
  append --ledger DIR --type TYPE --record PATH [--role record|secondary]
         TYPE is designation_snapshot (PATH = a snapshot directory of scripts/target_list_designation.py), spoc_check (a
         scripts/spoc_selection.py select record), qlp_check (a scripts/qlp_selection.py select record), acquisition (a spoc_ or
         qlp_acquisition record, with --role) or disposition (a JSON record {"disposition": "UNAVAILABLE"|"UNRESOLVED",
         "disposition_utc": ..., "basis": ...}). The record is copied into DIR/records/; the entry stores its SHA-256 and the SHA-256 of
         the previous entry. The whole ledger is replayed with the new entry, and an entry the rules forbid is REFUSED and not written.
  replay --ledger DIR                                           print the state
Rules (DECISIONS 178(a), 193, 194):
  - Every entry is later than the lock, and event times never decrease.
  - OPERATIVE DESIGNATION: the first designation_snapshot whose re-derived status is DESIGNATED. Its sector end and cutoffs are frozen;
    later snapshots are documented but never operative.
  - Release date: t_obs_release (MJD; MJD 0 = 1858-11-17 00:00 UTC). Usable only if finite and 0 < MJD < 200000; any other value
    (missing, non-numeric, infinite, out of range) is unusable, never qualifies and makes a SELECTED check unresolved.
  - Robustness: any parsing failure while replaying is a refusal (LedgerError). Appends are serialized transactions (see append()):
    an exclusive writer lock, a once-staged record, full validation of the candidate history, and an atomic commit, so a refused
    append leaves the live ledger unchanged even with concurrent writers.
  - Designated QLP -> route QLP.
  - Designated SPOC:
      - SPOC route: the first spoc_check that is SELECTED with release date <= SPOC cutoff (end + 120 d), at ANY time, makes the route
        SPOC with that file as release of record (irreversible). The exception: a QLP record acquisition under a certified fallback
        has already made the fallback final.
      - Fallback certification: two complete clean spoc_checks (NONE, or SELECTED with release date > cutoff) at or after the
        cutoff, >= 7 days apart, with no unresolved check (AMBIGUOUS, INCOMPLETE, or SELECTED without a usable release date) between
        or after them, CERTIFY the QLP fallback. It becomes FINAL when the QLP record acquisition is appended.
      - UNRESOLVED: an unresolved check at or after the cutoff makes the route UNRESOLVED, also after certification, until a later
        qualifying selection or a new two-check certification resolves it. Only a final fallback (QLP record acquisition) is immune.
  - Checks recorded BEFORE the operative designation are kept and, once the designation fixes the cutoffs, evaluated in ledger order
    under the same rules (the first qualifying record wins).
  - QLP release of record: the first qlp_check that is SELECTED with release date <= unavailable cutoff (end + 365 d); irreversible.
  - Acquisitions:
      - none before the operative designation, while the route is unsettled or UNRESOLVED, or after a disposition;
      - role 'record' must be of the route's product and reference that product's release-of-record selection record; at most ONE
        record acquisition per ledger;
      - role 'secondary' must be of the OTHER product than the route's, reference a SELECTED check of that product in this ledger
        (same dataURI and file name), and is allowed only once the route is settled; it never affects the route.
  - Dispositions:
      - UNAVAILABLE needs a QLP route, no QLP release of record, and a complete qlp_check (NONE, or SELECTED with a later release
        date) at or after the unavailable cutoff;
      - UNRESOLVED needs the route still UNRESOLVED or unsettled at or after the unavailable cutoff;
      - both are final."""
import sys, os, json, shutil, hashlib, argparse, datetime
R = "/Users/fernando/Desktop/NASA"; sys.path.insert(0, f"{R}/scripts")
UTC = datetime.timezone.utc
class LedgerError(Exception): pass
def fsha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
def bsha(b): return hashlib.sha256(b).hexdigest()
def ts(v, what):
    for fmt in ("%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%SZ"):
        try: return datetime.datetime.strptime(str(v), fmt).replace(tzinfo=UTC)
        except ValueError: pass
    raise LedgerError(f"{what} {str(v)[:40]!r} is not a UTC timestamp")
def mjd_utc(v):
    import math
    try: x = float(v[0] if isinstance(v, list) else v)
    except (TypeError, ValueError, IndexError): return None
    if not math.isfinite(x) or not (0 < x < 200000): return None
    try: return datetime.datetime(1858, 11, 17, tzinfo=UTC) + datetime.timedelta(days=x)
    except OverflowError: return None

def load_check(path, kind, tic, sector):
    import spoc_selection as XS, qlp_selection as XQ
    X, rec, prod = (XS, "spoc_selection", "SPOC_2MIN_LC") if kind == "spoc_check" else (XQ, "qlp_selection", "QLP_V01_LLC")
    s = json.load(open(path))
    if s.get("record") != rec or s.get("product") != prod or s.get("mode") != "mast_query": raise LedgerError(f"{kind} is not a MAST-query {rec} record")
    if s.get("tic") != tic or s.get("sector") != sector: raise LedgerError(f"{kind} TIC/sector differs from the ledger")
    o, p = s.get("observations"), s.get("products")
    if not isinstance(o, list) or not isinstance(p, list): raise LedgerError(f"{kind} lacks its saved rows")
    if s.get("response_sha256") != X.response_digest(o, p): raise LedgerError(f"{kind} response hash does not match the saved rows")
    d = X.derive(tic, sector, o, p)
    if dict(candidates=s.get("candidates"), status=s.get("status"), selected=s.get("selected")) != d: raise LedgerError(f"{kind} summary differs from the saved rows (re-derived status {d['status']})")
    rel = mjd_utc(d["selected"]["t_obs_release"]) if d["status"] == "SELECTED" else None
    return s, d, rel

def replay(ldir, made_iso=None):
    try: return _replay(ldir, made_iso)
    except LedgerError: raise
    except (KeyError, TypeError, ValueError, OverflowError, OSError, AttributeError, IndexError) as x:
        raise LedgerError(f"ledger or record could not be parsed ({type(x).__name__}: {str(x)[:80]})")

def _replay(ldir, made_iso=None):
    import target_list_designation as TD
    lines = open(os.path.join(ldir, "ledger.jsonl")).read().splitlines()
    if not lines: raise LedgerError("empty ledger")
    head = json.loads(lines[0])
    if head.get("type") != "init": raise LedgerError("ledger does not start with init")
    tic, sector = head["tic"], head["sector"]; made = ts(made_iso or head["lock_made_utc_iso"], "lock time")
    if made_iso and head["lock_made_utc_iso"] != made_iso: raise LedgerError("ledger was initialised for another lock")
    st = dict(tic=tic, sector=sector, operative=None, route="UNSETTLED", spoc_release=None, qlp_release=None, acquisitions=[], disposition=None, notes=[], clean=[], unresolved_after_cut=False, fallback_final=False)
    pre, selected = [], {}          # checks before the operative designation; every SELECTED check by record SHA-256

    def on_spoc(i, t, d, rel, rsha):
        op = st["operative"]
        if op["designation"] != "SPOC": st["notes"].append(f"entry {i}: SPOC check ({d['status']}); not route-relevant (QLP designated)"); return
        cut = op["spoc_cutoff"]; qualifying = d["status"] == "SELECTED" and rel is not None and rel <= cut
        if st["fallback_final"]:
            if qualifying: st["notes"].append(f"entry {i}: qualifying SPOC release found after the fallback became final; secondary only")
            return
        if qualifying:
            if st["spoc_release"] is None: st["spoc_release"] = dict(entry=i, record_sha256=rsha, selected=d["selected"], release_utc=rel.isoformat())
            st["route"] = "SPOC"; return
        if st["route"] == "SPOC" or t < cut: return
        clean = d["status"] == "NONE" or (d["status"] == "SELECTED" and rel is not None and rel > cut)
        if clean:
            st["clean"].append(t)
            if len(st["clean"]) >= 2 and (st["clean"][-1] - st["clean"][0]) >= datetime.timedelta(days=7): st["route"] = "QLP_FALLBACK_CERTIFIED"
        else:
            if st["route"] == "QLP_FALLBACK_CERTIFIED": st["notes"].append(f"entry {i}: unresolved SPOC check after certification; certification withdrawn")
            st["clean"] = []; st["route"] = "UNRESOLVED"

    def on_qlp(i, t, d, rel, rsha):
        op = st["operative"]
        if d["status"] == "SELECTED" and rel is not None and rel <= op["unavailable_cutoff"] and st["qlp_release"] is None:
            st["qlp_release"] = dict(entry=i, record_sha256=rsha, selected=d["selected"], release_utc=rel.isoformat())
        if t >= op["unavailable_cutoff"] and (d["status"] == "NONE" or (d["status"] == "SELECTED" and rel is not None and rel > op["unavailable_cutoff"])):
            st["qlp_complete_after_final"] = True
    prev, last_t = bsha(lines[0].encode()), made
    for i, line in enumerate(lines[1:], 1):
        e = json.loads(line)
        if e.get("seq") != i: raise LedgerError(f"entry {i}: sequence number {e.get('seq')}")
        if e.get("prev_entry_sha256") != prev: raise LedgerError(f"entry {i}: hash chain broken")
        prev = bsha(line.encode()); path = os.path.join(ldir, e["record"]); typ = e["type"]
        rsha = fsha(os.path.join(path, "snapshot.json")) if typ == "designation_snapshot" else fsha(path)
        if rsha != e["record_sha256"]: raise LedgerError(f"entry {i}: record bytes differ from the ledger")
        if typ == "designation_snapshot":
            try: d = TD.derive(path)
            except (OSError, ValueError, KeyError) as x: raise LedgerError(f"entry {i}: snapshot does not re-derive ({x})")
            if json.load(open(os.path.join(path, "designation.json"))) != d: raise LedgerError(f"entry {i}: saved designation.json differs from the re-derived designation")
            if d["sector"] != sector or str(tic) not in d["per_tic"]: raise LedgerError(f"entry {i}: snapshot is for another sector or lacks this TIC")
            t = ts(d["snapshot_utc"], "snapshot time")
        elif typ in ("spoc_check", "qlp_check"):
            s, d, rel = load_check(path, typ, tic, sector); t = ts(s["query_utc"], "query time")
        elif typ == "acquisition":
            q = json.load(open(path)); t = ts(q.get("download_utc"), "download time")
        elif typ == "disposition":
            q = json.load(open(path)); t = ts(q.get("disposition_utc"), "disposition time")
        else: raise LedgerError(f"entry {i}: unknown type {typ}")
        if t != ts(e["event_utc"], "event time"): raise LedgerError(f"entry {i}: event time differs from the record")
        if not t > made: raise LedgerError(f"entry {i}: not later than the lock")
        if t < last_t: raise LedgerError(f"entry {i}: event time earlier than the previous entry")
        last_t = t; op = st["operative"]
        if st["disposition"] and typ in ("acquisition", "disposition"): raise LedgerError(f"entry {i}: {typ} after the final disposition {st['disposition']}")
        if typ == "designation_snapshot":
            if op is None and d["status"] == "DESIGNATED":
                st["operative"] = dict(entry=i, snapshot_sha256=e["record_sha256"], designation=d["per_tic"][str(tic)]["designation"], sector_end_utc=d["sector_end_utc"],
                                       spoc_cutoff=ts(d["spoc_cutoff_utc"], "SPOC cutoff"), unavailable_cutoff=ts(d["unavailable_cutoff_utc"], "unavailable cutoff"))
                st["route"] = "QLP" if st["operative"]["designation"] == "QLP" else "SPOC_PENDING"
                for (pi, pt, pk, pd, prel, psha) in pre: (on_spoc if pk == "spoc_check" else on_qlp)(pi, pt, pd, prel, psha)
                if pre: st["notes"].append(f"entries {[x[0] for x in pre]}: checks before the designation evaluated under its cutoffs")
            elif op is not None: st["notes"].append(f"entry {i}: later snapshot recorded; not operative")
            continue
        if typ in ("spoc_check", "qlp_check"):
            if d["status"] == "SELECTED": selected[e["record_sha256"]] = ("SPOC" if typ == "spoc_check" else "QLP", d["selected"])
            if op is None: pre.append((i, t, typ, d, rel, e["record_sha256"])); continue
            (on_spoc if typ == "spoc_check" else on_qlp)(i, t, d, rel, e["record_sha256"]); continue
        if typ == "acquisition":
            role = e.get("role"); prod = "SPOC" if q.get("record") == "spoc_acquisition" else ("QLP" if q.get("record") == "qlp_acquisition" else None)
            if op is None: raise LedgerError(f"entry {i}: acquisition before the operative designation")
            if prod is None or q.get("mode") != "mast_download": raise LedgerError(f"entry {i}: not a mast_download spoc_/qlp_acquisition record")
            if q.get("tic") != tic or q.get("sector") != sector: raise LedgerError(f"entry {i}: acquisition TIC/sector differs from the ledger")
            settled = st["route"] in ("SPOC", "QLP", "QLP_FALLBACK_CERTIFIED", "QLP_FALLBACK_FINAL")
            if not settled: raise LedgerError(f"entry {i}: acquisition while the route is {st['route']}")
            route_prod = "SPOC" if st["route"] == "SPOC" else "QLP"
            if role == "record":
                if any(x["role"] == "record" for x in st["acquisitions"]): raise LedgerError(f"entry {i}: a record acquisition already exists (only one per ledger)")
                if prod != route_prod: raise LedgerError(f"entry {i}: record acquisition of {prod} but the route is {st['route']}")
                rel_rec = st["spoc_release"] if prod == "SPOC" else st["qlp_release"]
                if rel_rec is None: raise LedgerError(f"entry {i}: no {prod} release of record selected")
                if q.get("selection_sha256") != rel_rec["record_sha256"]: raise LedgerError(f"entry {i}: acquisition does not reference the release-of-record selection")
                if q.get("data_uri") != rel_rec["selected"]["dataURI"] or q.get("filename") != rel_rec["selected"]["filename"]: raise LedgerError(f"entry {i}: acquired file is not the release of record")
                if st["route"] == "QLP_FALLBACK_CERTIFIED": st["route"] = "QLP_FALLBACK_FINAL"; st["fallback_final"] = True
            elif role == "secondary":
                if prod == route_prod: raise LedgerError(f"entry {i}: a secondary acquisition must be of the other product (the route's product is {route_prod})")
                ref = selected.get(q.get("selection_sha256"))
                if not ref or ref[0] != prod: raise LedgerError(f"entry {i}: secondary acquisition does not reference a SELECTED {prod} check in this ledger")
                if q.get("data_uri") != ref[1]["dataURI"] or q.get("filename") != ref[1]["filename"]: raise LedgerError(f"entry {i}: secondary acquired file is not the referenced selection")
            else: raise LedgerError(f"entry {i}: acquisition role must be record or secondary")
            st["acquisitions"].append(dict(entry=i, product=prod, role=role, filename=q.get("filename"), file_sha256=q.get("file_sha256"), selection_sha256=q.get("selection_sha256")))
            continue
        if typ == "disposition":
            kind = q.get("disposition")
            if op is None or t < op["unavailable_cutoff"]: raise LedgerError(f"entry {i}: disposition before the unavailable cutoff")
            if kind == "UNAVAILABLE":
                if st["route"] not in ("QLP", "QLP_FALLBACK_CERTIFIED") or st["qlp_release"] is not None: raise LedgerError(f"entry {i}: UNAVAILABLE needs a QLP route with no QLP release of record")
                if not st.get("qlp_complete_after_final"): raise LedgerError(f"entry {i}: UNAVAILABLE needs a complete QLP check (no qualifying release) at or after the unavailable cutoff")
            elif kind == "UNRESOLVED":
                if st["route"] not in ("UNRESOLVED", "SPOC_PENDING"): raise LedgerError(f"entry {i}: UNRESOLVED needs an unresolved or unsettled route")
            else: raise LedgerError(f"entry {i}: disposition must be UNAVAILABLE or UNRESOLVED")
            st["disposition"] = kind; continue
    out = dict(st); out.pop("clean"); out["last_entry_sha256"] = prev
    if out["operative"]: out["operative"] = {k: (v.isoformat() if isinstance(v, datetime.datetime) else v) for k, v in out["operative"].items()}
    return out

def _write_entry(ldir, typ, record, role):
    """Append one entry to the ledger in DIR (used only on the candidate copy). Returns the record's path relative to DIR."""
    L = os.path.join(ldir, "ledger.jsonl"); lines = open(L).read().splitlines(); i = len(lines)
    rdir = os.path.join(ldir, "records"); os.makedirs(rdir, exist_ok=True); name = f"{i:03d}_{typ}"
    if typ == "designation_snapshot":
        dst = os.path.join(rdir, name); shutil.copytree(record, dst); rsha = fsha(os.path.join(dst, "snapshot.json")); t = json.load(open(os.path.join(dst, "snapshot.json")))["snapshot_utc"]
    else:
        dst = os.path.join(rdir, name + ".json"); shutil.copy2(record, dst); rsha = fsha(dst); r = json.load(open(dst))
        t = r.get("query_utc") or r.get("download_utc") or r.get("disposition_utc")
    e = dict(seq=i, type=typ, event_utc=t, record=os.path.relpath(dst, ldir), record_sha256=rsha, prev_entry_sha256=bsha(lines[-1].encode()))
    if typ == "acquisition": e["role"] = role
    open(L, "a").write(json.dumps(e, sort_keys=True) + "\n"); return os.path.relpath(dst, ldir)

def _referenced(ldir):
    return {json.loads(l)["record"] for l in open(os.path.join(ldir, "ledger.jsonl")).read().splitlines()[1:]}

def append(a):
    """One append as a serialized transaction (review RECHECK2: concurrent appends).
    1. An exclusive per-ledger writer lock (fcntl.flock on DIR/.writer.lock) is held from reading the history to the commit; a second
       writer waits.
    2. The source record is staged ONCE into a private temporary directory; the candidate ledger is built from the live history plus
       those staged bytes and fully replayed. A refusal writes nothing to the live ledger.
    3. Commit: the validated record bytes are copied from the candidate into DIR/records under a temporary name and renamed into
       place, then the validated ledger.jsonl replaces the live one with os.replace (atomic). A reader therefore sees either the old
       history or the new one, never an entry whose record is incomplete. An interruption between the two steps leaves at most an
       unreferenced record, which the next append removes under the lock.
    Test hook (inactive unless set): S111_LEDGER_PAUSE_AFTER_STAGE=FILE makes the writer wait, after staging and while holding the
    lock, until FILE exists. It is used only by scripts/test_s111_lock.py to schedule interleavings deterministically."""
    import fcntl, tempfile, time
    lockf = open(os.path.join(a.ledger, ".writer.lock"), "a"); fcntl.flock(lockf, fcntl.LOCK_EX)
    tmp = tempfile.mkdtemp(prefix="s111_ledger_txn_")
    try:
        staged = os.path.join(tmp, "staged")
        try:
            if a.type == "designation_snapshot": shutil.copytree(a.record, staged)
            else: shutil.copy2(a.record, staged)
        except OSError as x: raise SystemExit(f"REFUSED (not written): record could not be read ({type(x).__name__})")
        hook = os.environ.get("S111_LEDGER_PAUSE_AFTER_STAGE")
        if hook:
            while not os.path.exists(hook): time.sleep(0.05)
        cand = os.path.join(tmp, "ledger"); shutil.copytree(a.ledger, cand, ignore=shutil.ignore_patterns(".writer.lock", ".tmp_*"))
        ref = _referenced(cand)
        for f in os.listdir(os.path.join(cand, "records")) if os.path.isdir(os.path.join(cand, "records")) else []:
            if f"records/{f}" not in ref: (shutil.rmtree if os.path.isdir(os.path.join(cand, "records", f)) else os.remove)(os.path.join(cand, "records", f))
        try: rel = _write_entry(cand, a.type, staged, a.role); replay(cand)
        except LedgerError as x: raise SystemExit(f"REFUSED (not written): {x}")
        except (KeyError, TypeError, ValueError, OverflowError, OSError, AttributeError, IndexError) as x: raise SystemExit(f"REFUSED (not written): record could not be parsed ({type(x).__name__}: {str(x)[:80]})")
        live_rec = os.path.join(a.ledger, rel); os.makedirs(os.path.dirname(live_rec), exist_ok=True)
        live_ref = _referenced(a.ledger)
        if os.path.exists(live_rec):
            if rel in live_ref: raise SystemExit("REFUSED (not written): record path already referenced (ledger changed unexpectedly)")
            shutil.rmtree(live_rec) if os.path.isdir(live_rec) else os.remove(live_rec)          # unreferenced leftover of an interrupted commit
        part = os.path.join(os.path.dirname(live_rec), ".tmp_" + os.path.basename(live_rec))
        (shutil.copytree if os.path.isdir(os.path.join(cand, rel)) else shutil.copy2)(os.path.join(cand, rel), part); os.rename(part, live_rec)
        newl = os.path.join(a.ledger, ".tmp_ledger.jsonl"); shutil.copy2(os.path.join(cand, "ledger.jsonl"), newl); os.replace(newl, os.path.join(a.ledger, "ledger.jsonl"))
        s = replay(a.ledger)
    finally:
        shutil.rmtree(tmp, ignore_errors=True); fcntl.flock(lockf, fcntl.LOCK_UN); lockf.close()
    print("appended", rel, "->", s["route"], s.get("disposition") or "")

def init(a):
    if os.path.exists(a.ledger): raise SystemExit(f"refused: {a.ledger} exists")
    lq, ls = json.load(open(a.lock_qlp)), json.load(open(a.lock_spoc))
    if lq.get("made_utc_iso") != ls.get("made_utc_iso"): raise SystemExit("refused: the two locks do not share one lock time")
    os.makedirs(a.ledger)
    open(os.path.join(a.ledger, "ledger.jsonl"), "w").write(json.dumps(dict(seq=0, type="init", tic=a.tic, sector=a.sector,
        lock_files=[os.path.basename(a.lock_qlp), os.path.basename(a.lock_spoc)], lock_sha256s=[fsha(a.lock_qlp), fsha(a.lock_spoc)],
        lock_made_utc_iso=lq["made_utc_iso"]), sort_keys=True) + "\n")
    print("initialised", a.ledger)

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); sp = ap.add_subparsers(dest="cmd", required=True)
    p = sp.add_parser("init"); p.add_argument("--ledger", required=True); p.add_argument("--tic", type=int, required=True); p.add_argument("--sector", type=int, required=True)
    p.add_argument("--lock-qlp", required=True); p.add_argument("--lock-spoc", required=True)
    p = sp.add_parser("append"); p.add_argument("--ledger", required=True); p.add_argument("--type", required=True); p.add_argument("--record", required=True); p.add_argument("--role", choices=["record", "secondary"])
    p = sp.add_parser("replay"); p.add_argument("--ledger", required=True)
    a = ap.parse_args()
    if a.cmd == "init": init(a)
    elif a.cmd == "append": append(a)
    else:
        try: print(json.dumps(replay(a.ledger), indent=1, default=str))
        except LedgerError as x: raise SystemExit(f"INVALID LEDGER: {x}")
