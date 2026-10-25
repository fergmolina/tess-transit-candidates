"""Binding checks for the S111+ tests of TIC 80387959 / 120517801 (v2, 2026-10-25; DECISIONS 192-195; review S111-1 to S111-5). Fails
closed. Exit 0 = bound, 2 = refused. The product-of-record history is the per-TIC/sector ledger of scripts/s111_ledger.py; this
validator REPLAYS it with the same function (s111_ledger.replay) after checking that function's bytes against the lock.
  --stage pre    --lock L --config C
        C's SHA-256 is in the lock; its prediction CSV bytes and every code hash named in the lock entry match the files: the designation
        tool, both selection tools, the ledger, and the SPOC evaluator (SPOC lock) or the QLP lock's evaluator.
  --stage route  --lock L --config C --ledger DIR
        The ledger replays without error, was initialised with this lock's SHA-256 (it records both locks' hashes), TIC and sector, and has an operative designation made after
        the lock. Its route is settled and C's product is the route's product:
          SPOC                     needs a qualifying SPOC release of record;
          QLP                      designated QLP;
          QLP_FALLBACK_CERTIFIED / FINAL   SPOC designated, fallback certified.
        UNSETTLED, SPOC_PENDING, UNRESOLVED and any final disposition are refused, with the reason.
  --stage result --lock L --config C --ledger DIR --lc LC --result E
        As 'route', plus: the ledger holds a role-'record' acquisition of C's product whose file name and SHA-256 equal LC; and E was
        made from exactly C, by the locked evaluator, from LC. For QLP configs the published scripts/validate_round4_inputs.py must
        ALSO bind its clock and result stages for the same config and light curve; both BOUND lines are required in the final result.
Usage: python -I validate_s111_inputs.py --lock LOCK --stage S --config C [...]"""
import sys, os, re, json, hashlib, argparse
R = "/Users/fernando/Desktop/NASA"; sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
HEX = lambda v: isinstance(v, str) and re.fullmatch(r"[0-9a-f]{64}", v) is not None
ap = argparse.ArgumentParser(); ap.add_argument("--lock", required=True); ap.add_argument("--stage", required=True, choices=["pre", "route", "result"])
ap.add_argument("--config", required=True); ap.add_argument("--ledger"); ap.add_argument("--lc"); ap.add_argument("--result"); a = ap.parse_args()
def refuse(m): print("REFUSED:", m); sys.exit(2)
def load(p, what):
    try: return json.load(open(p))
    except (OSError, ValueError, TypeError) as e: refuse(f"{what} unreadable ({type(e).__name__})")
lock = load(a.lock, "lock"); cs = sha(a.config); L = next((v for v in lock.get("configs", {}).values() if v.get("config_sha256") == cs), None)
if L is None: refuse(f"config SHA-256 {cs[:16]} is not in the lock manifest")
c = load(a.config, "config")
for k in ("tic", "sector", "pred_sha256", "product"):
    if c.get(k) != L.get(k): refuse(f"config {k} differs from the lock")
if not os.path.exists(c.get("pred_csv", "")) or sha(c["pred_csv"]) != L["pred_sha256"]: refuse("prediction CSV bytes differ from the lock")
code = {k: v for k, v in L.items() if k.endswith("_code_sha256")}
for need in ("target_list_designation", "spoc_selection", "qlp_selection", "s111_ledger"):
    if f"{need}_code_sha256" not in code: refuse(f"lock entry does not bind {need}.py")
if c["product"] == "SPOC" and f"{L.get('scoring_code')}_code_sha256" not in code: refuse("SPOC lock entry names no scoring-code hash")
if c["product"] == "QLP" and (not HEX(lock.get("evaluator_sha256")) or sha(f"{R}/scripts/prereg_conformance.py") != lock["evaluator_sha256"]): refuse("QLP evaluator differs from the lock")
for k, want in code.items():
    path = f"{R}/scripts/{k[:-len('_code_sha256')]}.py"
    if not HEX(want) or not os.path.exists(path) or sha(path) != want: refuse(f"{os.path.basename(path)} SHA-256 differs from the lock")
if a.stage == "pre": print(f"BOUND: stage pre, {os.path.basename(a.config)} (lock {sha(a.lock)[:16]})"); sys.exit(0)
if not a.ledger: refuse("--ledger is required at this stage")
sys.path.insert(0, f"{R}/scripts"); import s111_ledger as LG          # bytes checked against the lock above
try: head = json.loads(open(os.path.join(a.ledger, "ledger.jsonl")).readline())
except (OSError, ValueError) as e: refuse(f"ledger unreadable ({type(e).__name__})")
if head.get("tic") != c["tic"] or head.get("sector") != c["sector"]: refuse("ledger is for another TIC or sector")
if sha(a.lock) not in (head.get("lock_sha256s") or []) or head.get("lock_made_utc_iso") != lock.get("made_utc_iso"): refuse("ledger was initialised for another lock (it must name this lock's SHA-256)")
try: st = LG.replay(a.ledger, lock["made_utc_iso"])
except LG.LedgerError as e: refuse(f"ledger does not replay: {e}")
if st["disposition"]: refuse(f"final disposition {st['disposition']}: no outcome of record")
if not st["operative"]: refuse("no operative designation (no DESIGNATED snapshot in the ledger)")
route = st["route"]
if route in ("UNSETTLED", "SPOC_PENDING", "UNRESOLVED"): refuse(f"route is {route}: no product of record yet")
route_prod = "SPOC" if route == "SPOC" else "QLP"
if c["product"] != route_prod: refuse(f"config product {c['product']} is not the product of record (route {route})")
if a.stage == "route": print(f"BOUND: stage route, {os.path.basename(a.config)}: route {route} (operative snapshot {st['operative']['snapshot_sha256'][:16]}; lock {sha(a.lock)[:16]})"); sys.exit(0)
if not (a.lc and a.result): refuse("--lc and --result are required at this stage")
lcsha = sha(a.lc); acq = [x for x in st["acquisitions"] if x["role"] == "record" and x["product"] == c["product"]]
if not acq: refuse(f"the ledger holds no record acquisition of {c['product']}")
if acq[0]["file_sha256"] != lcsha or acq[0]["filename"] != os.path.basename(a.lc): refuse("scored file is not the ledger's record acquisition")
e = load(a.result, "evaluator output")
for f in ("config_sha256", "script_sha256", "lc_sha256"):
    if not HEX(e.get(f)): refuse(f"output {f} is missing or not a SHA-256")
if e["config_sha256"] != cs: refuse("output was made from a different config")
want_ev = L[f"{L['scoring_code']}_code_sha256"] if c["product"] == "SPOC" else lock["evaluator_sha256"]
if e["script_sha256"] != want_ev: refuse("output was made by a different evaluator")
if e["lc_sha256"] != lcsha: refuse("output was made from a different light curve")
if not e.get("outcome"): refuse("output has no outcome")
tail = "" if c["product"] == "SPOC" else "; ALSO REQUIRED: validate_round4_inputs.py --stage clock and --stage result BOUND for this config and light curve"
print(f"BOUND: stage result, {os.path.basename(a.config)}: route {route}, outcome {str(e['outcome'])[:40]} (ledger tip {st['last_entry_sha256'][:16]}){tail}")
