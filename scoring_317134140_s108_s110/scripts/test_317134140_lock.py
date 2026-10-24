"""Tests for the TIC 317134140 S108-S110 lock (scorer v1.3; DECISIONS 179; review G1, G2, G4). NO real light curve of a test sector is read:
every light curve is an ARTIFICIAL SPOC-format FITS fixture (seeded white noise, optional injected box transits at the frozen predicted
times) in a fresh directory, and every MAST response is an artificial product list.
Per config:
  binding: --stage pre binds the real config; refuses an edited config copy and lock copies whose scorer or selection-tool hash differs;
  mechanics: injected 185 ppm -> A_CONSISTENT; no signal -> FAIL; TOI mask applied;
  G1 input refusals: TIMEUNIT, TIMEREF, BJDREFF, BJDREFI, TIMESYS; missing or malformed TICID; missing column; ORIGIN; wrong TIC or sector;
     unreadable file; unsorted and duplicate times -> INVALID_INPUT. All cadences flagged, zero errors, too short, constant flux
     (sigma 0) -> INSUFFICIENT. Changed scorer or prediction hash in a config copy -> INVALID_INPUT. Existing output path and
     --insample-check on a test sector -> refused;
  G2 release binding: selection stage binds a single-candidate MAST record; refuses AMBIGUOUS, NONE, a candidate of another sector, a
     non-MAST (test-response) record and a record older than the lock. Result stage binds selection + acquisition + light curve + output;
     refuses a substituted file (pipeline 9999), altered bytes, an acquisition of another selection, a non-download acquisition, an
     acquisition older than the selection, a missing record, another config's output and output made by other code.
  Re-check R1/R2: refuses deleted product rows (old or recomputed hash), two eligible rows under a one-candidate summary, a missing
     dataURI, absent/null/empty/whitespace/placeholder observation ids (re-check 2), malformed query/download timestamps, and a first SELECTED record after the cutoff; binds a record exactly at the
     (inclusive) cutoff and a timely selection acquired long after the cutoff.
Once: G4 complete truth table of the ordered outcome mapping (5 clause-A x 2 clause-B states).
These tests do not cover real SPOC systematics, MAST behaviour, or the power of the tests on real data.
Usage: python -I test_317134140_lock.py LOCK.json TMPDIR   (TMPDIR must not exist)"""
import sys, os, csv, json, hashlib, subprocess, shutil
import numpy as np
from astropy.io import fits
R = "/Users/fernando/Desktop/NASA"; PY = f"{R}/.venv/bin/python"; LOCKF, TMP = sys.argv[1], sys.argv[2]; VAL = f"{R}/scripts/validate_nonclock_inputs.py"
SCORER = f"{R}/scripts/prereg_spoc_317134140.py"; SELT = f"{R}/scripts/spoc_selection.py"
if os.path.exists(TMP): raise SystemExit(f"refused: {TMP} exists (fresh directory required)")
os.makedirs(TMP); sys.path.insert(0, f"{R}/scripts"); sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest(); fails = []; n = 0
import prereg_spoc_317134140 as S
from spoc_selection import make_acquisition
lock = json.load(open(LOCKF))
def check(cond, msg):
    global n; n += 1
    if not cond: fails.append(msg)
    print(("PASS " if cond else "FAIL ") + msg)
def run(args): r = subprocess.run([PY, "-I"] + args, capture_output=True, text=True); return r.returncode, r.stdout + r.stderr
def val(stage, cfg, lockf=LOCKF, **kw): return run([VAL, "--lock", lockf, "--stage", stage, "--config", cfg] + sum(([f"--{k}", v] for k, v in kw.items()), []))[0]
def score(cfgp, lc, out, extra=()):
    rc, txt = run([SCORER, "--config", cfgp, "--lc", lc, "--out", out] + list(extra))
    return (json.load(open(out)) if os.path.exists(out) else {"outcome": f"CRASH rc={rc} {txt[-200:]}"}), rc
def name(sector, d, pipe="0000"): return f"{d}/tess2099001000000-s{sector:04d}-{317134140:016d}-{pipe}-s_lc.fits"
def fixture(path, sector, tcs, depth_ppm, seed=1, h0x=None, h1x=None, drop=(), quality=0, err=2.0, const=False, shuffle=False, dup=False, span=None):
    rng = np.random.default_rng(seed); t0, t1 = (tcs.min() - 1.0, tcs.max() + 1.0) if span is None else span; t = np.arange(t0, t1, 2 / 1440)
    mid = 0.5 * (t0 + t1); t = t[np.abs(t - mid) > 0.5] if span is None else t
    f = np.ones(len(t)) if const else 1 + rng.normal(0, 2000e-6, len(t))
    for tc in tcs: f[np.abs(t - tc) < 0.75 / 24] -= depth_ppm * 1e-6
    if shuffle: t[[10, 11]] = t[[11, 10]]
    if dup: t[11] = t[10]
    h0 = fits.PrimaryHDU(); h0.header.update(dict(ORIGIN="NASA/Ames", TICID=317134140, SECTOR=sector, TELESCOP="TESS", PROCVER="artificial", DATA_REL=0), **(h0x or {}))
    cols = {"TIME": ("D", t), "PDCSAP_FLUX": ("E", f * 1000), "PDCSAP_FLUX_ERR": ("E", np.full(len(t), err)), "QUALITY": ("J", np.full(len(t), quality))}
    h1 = fits.BinTableHDU.from_columns([fits.Column(name=k, format=v[0], array=v[1]) for k, v in cols.items() if k not in drop])
    h1.header.update(dict(TIMESYS="TDB", TIMEREF="SOLARSYSTEM", BJDREFI=2457000, BJDREFF=0.0, TIMEUNIT="d"), **(h1x or {}))
    for k in [k for k, v in {**(h0x or {}), **(h1x or {})}.items() if v is None]:
        for hh in (h0.header, h1.header): hh.pop(k, None)
    fits.HDUList([h0, h1]).writeto(path)
def edited(cfg, nm, **kw): p = f"{TMP}/{nm}.json"; json.dump(dict(cfg, **kw), open(p, "w"), indent=1); return p
def response(path, files):
    obs = [dict(obs_id=os.path.basename(f)[:-8], t_obs_release="61400.0", t_exptime="120.0") for f in files]
    prods = [dict(productFilename=os.path.basename(f), dataURI="mast:TESS/product/" + os.path.basename(f), obsID=str(i), obs_id=os.path.basename(f)[:-8], size="1")
             for i, f in enumerate(files)]
    json.dump(dict(observations=obs, products=prods), open(path, "w")); return path
def selection(out, sector, files, mode="mast_query", query_utc=None):
    rc, txt = run([SELT, "select", "--tic", "317134140", "--sector", str(sector), "--out", out, "--from-response", response(out + ".resp", files)])
    s = json.load(open(out)); s["mode"] = mode            # tests stand in for a MAST query; the validator refuses any other mode
    if query_utc: s["query_utc"] = query_utc
    json.dump(s, open(out, "w"), indent=1); return out
def acquisition(out, sel, lc, mode="mast_download", t=None):
    json.dump(make_acquisition(sel, lc, mode, t), open(out, "w"), indent=1); return out

# G4 truth table (once)
want = {("INSUFFICIENT", b): "INSUFFICIENT" for b in ("B_TOP3", "B_NOT_TOP3")}
want.update({("A_LOW", "B_TOP3"): "FAIL", ("A_LOW", "B_NOT_TOP3"): "FAIL", ("A_CONSISTENT", "B_TOP3"): "PASS", ("A_CONSISTENT", "B_NOT_TOP3"): "PARTIAL",
             ("A_HIGH", "B_TOP3"): "PARTIAL", ("A_HIGH", "B_NOT_TOP3"): "INCONCLUSIVE", ("A_INCONCLUSIVE", "B_TOP3"): "PARTIAL", ("A_INCONCLUSIVE", "B_NOT_TOP3"): "INCONCLUSIVE"})
for (ca, cb), w in sorted(want.items()): check(S.sector_outcome(ca, cb) == w, f"truth table {ca} + {cb} -> {w}")

for k, L in sorted(lock["configs"].items()):
    cfgp = f"{R}/configs/conformance/{k}"; cfg = json.load(open(cfgp)); sec = cfg["sector"]; d = f"{TMP}/{k[:-5]}"; os.makedirs(d)
    tcs = np.array([float(r["tc_BJD_TDB"]) - 2457000 for r in csv.DictReader(open(cfg["pred_csv"])) if int(r["sector"]) == sec])
    check(sha(cfgp) == L["config_sha256"] and sha(cfg["pred_csv"]) == L["pred_sha256"], f"{k} config and prediction CSV match the lock ({len(tcs)} predicted events)")
    check(val("pre", cfgp) == 0, f"{k} --stage pre binds")
    check(val("pre", edited(cfg, f"{k}_edit", note="x")) == 2, f"{k} --stage pre refuses an edited config copy")
    for code in ("prereg_spoc_317134140", "spoc_selection"):
        bl = json.loads(json.dumps(lock)); bl["configs"][k][f"{code}_code_sha256"] = "0" * 64; blp = f"{TMP}/{k}_{code}_badlock.json"; json.dump(bl, open(blp, "w"))
        check(val("pre", cfgp, blp) == 2, f"{k} --stage pre refuses a lock whose {code} hash differs")
    def case(tag, expect_prefix, **fx):
        dd = f"{d}/{tag}"; os.makedirs(dd); lc = name(fx.pop("sector", sec), dd, fx.pop("pipe", "0000")); fixture(lc, fx.pop("hdr_sector", sec), tcs, fx.pop("depth", 185.0), **fx)
        o, _ = score(fx.get("cfg", cfgp), lc, f"{dd}/out.json"); ok = str(o["outcome"]).startswith(expect_prefix)
        check(ok, f"{k} {tag}: {str(o['outcome'])[:90]}"); return lc, o
    lci, oi = f"{d}/inj.fits", None
    os.makedirs(f"{d}/inj"); lci = name(sec, f"{d}/inj"); fixture(lci, sec, tcs, 185.0, seed=sec); oi, _ = score(cfgp, lci, f"{d}/inj/out.json")
    check(oi.get("clause_a") == "A_CONSISTENT" and oi["outcome"] in ("PASS", "PARTIAL") and oi.get("toi_mask_removed", 0) > 0,
          f"{k} injected 185 ppm: {oi['outcome']} / {oi.get('clause_a')} ({oi.get('depth_ppm', 0):.0f} +- {oi.get('sigma_ppm', 0):.0f} ppm, TOI mask {oi.get('toi_mask_removed')})")
    case("null", "FAIL", depth=0.0, seed=sec + 1000)
    for tag, h0x, h1x in (("TIMEUNIT s", None, dict(TIMEUNIT="s")), ("TIMEREF LOCAL", None, dict(TIMEREF="LOCAL")), ("BJDREFF 0.5", None, dict(BJDREFF=0.5)),
                          ("BJDREFI 2400000", None, dict(BJDREFI=2400000)), ("TIMESYS UTC", None, dict(TIMESYS="UTC")), ("TIMEUNIT missing", None, dict(TIMEUNIT=None)),
                          ("TICID missing", dict(TICID=None), None), ("TICID malformed", dict(TICID="abc"), None), ("ORIGIN MIT/QLP", dict(ORIGIN="MIT/QLP"), None)):
        case(tag, "INVALID_INPUT", h0x=h0x, h1x=h1x)
    case("missing PDCSAP_FLUX_ERR", "INVALID_INPUT", drop=("PDCSAP_FLUX_ERR",))
    case("header sector differs", "INVALID_INPUT", hdr_sector=sec - 1)
    case("file sector differs", "INVALID_INPUT", sector=sec - 1, hdr_sector=sec - 1)
    case("unsorted times", "INVALID_INPUT", shuffle=True)
    case("duplicate time", "INVALID_INPUT", dup=True)
    case("all cadences flagged", "INSUFFICIENT", quality=1)
    case("zero errors", "INSUFFICIENT", err=0.0)
    case("constant flux (sigma 0)", "INSUFFICIENT", const=True)
    case("two days of data", "INSUFFICIENT", span=(tcs.min(), tcs.min() + 2.0))
    os.makedirs(f"{d}/junk"); junk = name(sec, f"{d}/junk"); open(junk, "w").write("not a FITS file")
    o, _ = score(cfgp, junk, f"{d}/junk/out.json"); check(str(o["outcome"]).startswith("INVALID_INPUT"), f"{k} unreadable file: {str(o['outcome'])[:60]}")
    os.makedirs(f"{d}/tic"); lt = f"{d}/tic/tess2099001000000-s{sec:04d}-{317134141:016d}-0000-s_lc.fits"; shutil.copy(lci, lt)
    o, _ = score(cfgp, lt, f"{d}/tic/out.json"); check(str(o["outcome"]).startswith("INVALID_INPUT"), f"{k} another TIC: {str(o['outcome'])[:60]}")
    o, _ = score(edited(cfg, f"{k}_badcode", scorer_sha256="0" * 64), lci, f"{d}/badcode.json"); check(str(o["outcome"]).startswith("INVALID_INPUT"), f"{k} changed scorer hash in config")
    o, _ = score(edited(cfg, f"{k}_badpred", pred_sha256="0" * 64), lci, f"{d}/badpred.json"); check(str(o["outcome"]).startswith("INVALID_INPUT"), f"{k} changed prediction hash in config")
    o, _ = score(cfgp, lci, f"{d}/insample.json", ["--insample-check"]); check(str(o["outcome"]).startswith("REFUSED"), f"{k} --insample-check refuses a test sector")
    _, rc = score(cfgp, lci, f"{d}/inj/out.json"); check(rc != 0, f"{k} refuses to overwrite an existing output")
    # G2: selection and acquisition binding
    sel = selection(f"{d}/sel.json", sec, [lci]); acq = acquisition(f"{d}/acq.json", sel, lci)
    check(val("selection", cfgp, selection=sel) == 0, f"{k} selection stage binds a single-candidate MAST record")
    check(val("result", cfgp, selection=sel, acquisition=acq, lc=lci, result=f"{d}/inj/out.json") == 0, f"{k} result stage binds selection + acquisition + light curve + output")
    other_pipe = name(sec, f"{d}/inj", "0001")
    check(val("selection", cfgp, selection=selection(f"{d}/sel_amb.json", sec, [lci, other_pipe])) == 2, f"{k} refuses an AMBIGUOUS selection (two candidates)")
    check(val("selection", cfgp, selection=selection(f"{d}/sel_none.json", sec, [])) == 2, f"{k} refuses a NONE selection")
    check(val("selection", cfgp, selection=selection(f"{d}/sel_sec.json", sec, [name(sec - 1, d)])) == 2, f"{k} refuses a candidate of another sector")
    check(val("selection", cfgp, selection=selection(f"{d}/sel_resp.json", sec, [lci], mode="from_response:x")) == 2, f"{k} refuses a non-MAST (test-response) selection")
    check(val("selection", cfgp, selection=selection(f"{d}/sel_old.json", sec, [lci], query_utc="2026-10-01T00:00:00.000000Z")) == 2, f"{k} refuses a selection older than the lock")
    os.makedirs(f"{d}/sub"); sub = name(sec, f"{d}/sub", "9999"); shutil.copy(lci, sub); os.makedirs(f"{d}/sub/o"); osub, _ = score(cfgp, sub, f"{d}/sub/o/out.json")
    check(osub["outcome"] in ("PASS", "PARTIAL") and val("result", cfgp, selection=sel, acquisition=acquisition(f"{d}/acq_sub.json", sel, sub), lc=sub, result=f"{d}/sub/o/out.json") == 2,
          f"{k} refuses a substituted file (pipeline 9999) although it scores {osub['outcome']}")
    os.makedirs(f"{d}/alt"); alt = name(sec, f"{d}/alt"); fixture(alt, sec, tcs, 185.0, seed=sec + 7); oa, _ = score(cfgp, alt, f"{d}/alt/out.json")
    check(val("result", cfgp, selection=sel, acquisition=acq, lc=alt, result=f"{d}/alt/out.json") == 2, f"{k} refuses altered bytes under the selected name")
    sel2 = selection(f"{d}/sel2.json", sec, [lci])
    check(val("result", cfgp, selection=sel2, acquisition=acq, lc=lci, result=f"{d}/inj/out.json") == 2, f"{k} refuses an acquisition of another selection record")
    check(val("result", cfgp, selection=sel, acquisition=acquisition(f"{d}/acq_local.json", sel, lci, mode="local_copy"), lc=lci, result=f"{d}/inj/out.json") == 2, f"{k} refuses a non-download acquisition")
    check(val("result", cfgp, selection=sel, acquisition=acquisition(f"{d}/acq_early.json", sel, lci, t="2026-10-02T00:00:00.000000Z"), lc=lci, result=f"{d}/inj/out.json") == 2, f"{k} refuses an acquisition older than the selection")
    check(val("result", cfgp, selection=sel, lc=lci, result=f"{d}/inj/out.json") == 2, f"{k} refuses a missing acquisition record")
    check(val("result", cfgp, acquisition=acq, lc=lci, result=f"{d}/inj/out.json") == 2, f"{k} refuses a missing selection record")
    # R1 (re-check): saved rows, response hash and summary must agree
    import spoc_selection as X
    def mutate(tag, fn):
        r = json.load(open(sel)); fn(r); out = f"{d}/sel_{tag}.json"; json.dump(r, open(out, "w"), indent=1); return out
    check(val("selection", cfgp, selection=mutate("noprod_oldhash", lambda r: r.update(products=[]))) == 2, f"{k} refuses deleted product rows with the old response hash")
    check(val("selection", cfgp, selection=mutate("noprod_newhash", lambda r: r.update(products=[], response_sha256=X.response_digest(r["observations"], [])))) == 2,
          f"{k} refuses deleted product rows with a recomputed hash but the old SELECTED summary")
    def two(r):
        extra = dict(r["products"][0], productFilename=os.path.basename(other_pipe), dataURI="mast:TESS/product/" + os.path.basename(other_pipe))
        r["products"] = r["products"] + [extra]; r["response_sha256"] = X.response_digest(r["observations"], r["products"])
    check(val("selection", cfgp, selection=mutate("two_rows", two)) == 2, f"{k} refuses two eligible rows with a correct hash but a one-candidate SELECTED summary")
    def nouri(r):
        r["products"][0]["dataURI"] = ""; r["response_sha256"] = X.response_digest(r["observations"], r["products"])
    check(val("selection", cfgp, selection=mutate("no_uri", nouri)) == 2, f"{k} refuses a selected product without a dataURI")
    # re-check 2: absent, null, empty, whitespace or placeholder observation ids never establish the association
    for tag, v in (("absent", None), ("null", "null"), ("empty", ""), ("space", " "), ("padded", " x "), ("none_str", "None")):
        def badid(r, v=v):
            for row in (r["products"][0], r["observations"][0]):
                if v is None: row.pop("obs_id", None)
                else: row["obs_id"] = v
            r["response_sha256"] = X.response_digest(r["observations"], r["products"])
            dd_ = X.derive(r["tic"], r["sector"], r["observations"], r["products"]); r.update(candidates=dd_["candidates"], status=dd_["status"], selected=dd_["selected"])
        rec = mutate(f"id_{tag}", badid); st = json.load(open(rec))["status"]
        check(st == "INCOMPLETE" and val("selection", cfgp, selection=rec) == 2, f"{k} {tag} obs_id on both rows (hash and summary regenerated): derive -> {st}, refused")
    # R2 (re-check): parsed timestamps and the inclusive cutoff
    cut = cfg["unavailable_cutoff_utc"]; cut_us = cut[:-1] + ".000000Z"; after = cut[:-1] + ".000001Z"
    check(val("selection", cfgp, selection=selection(f"{d}/sel_zzz.json", sec, [lci], query_utc="zzz")) == 2, f"{k} refuses a malformed query_utc")
    check(val("selection", cfgp, selection=selection(f"{d}/sel_atcut.json", sec, [lci], query_utc=cut_us)) == 0, f"{k} binds a SELECTED record made exactly at the cutoff {cut}")
    check(val("selection", cfgp, selection=selection(f"{d}/sel_late.json", sec, [lci], query_utc=after)) == 2, f"{k} refuses a first SELECTED record made after the cutoff (UNAVAILABLE)")
    check(val("result", cfgp, selection=sel, acquisition=acquisition(f"{d}/acq_zzz.json", sel, lci, t="zzz"), lc=lci, result=f"{d}/inj/out.json") == 2, f"{k} refuses a malformed download_utc")
    check(val("result", cfgp, selection=sel, acquisition=acquisition(f"{d}/acq_late.json", sel, lci, t="2028-06-01T00:00:00.000000Z"), lc=lci, result=f"{d}/inj/out.json") == 0,
          f"{k} binds a timely selection acquired and scored long after the cutoff")
    other = next(kk for kk in sorted(lock["configs"]) if kk != k)
    check(val("result", f"{R}/configs/conformance/{other}", selection=sel, acquisition=acq, lc=lci, result=f"{d}/inj/out.json") == 2, f"{k} refuses the output under another config")
    e = json.load(open(f"{d}/inj/out.json")); e["script_sha256"] = "0" * 64; json.dump(e, open(f"{d}/out_alt.json", "w"))
    check(val("result", cfgp, selection=sel, acquisition=acq, lc=lci, result=f"{d}/out_alt.json") == 2, f"{k} refuses output made by other code")
print(f"{n - len(fails)}/{n} passed"); sys.exit(1 if fails else 0)
