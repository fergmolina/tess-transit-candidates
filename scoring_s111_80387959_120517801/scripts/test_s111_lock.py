"""Tests for the v1.19 S111+ package, v2 (DECISIONS 192-195; review S111-1 to S111-5). Everything is ARTIFICIAL and written to a fresh
directory: no real light curve and no real snapshot of a test sector is read. Every negative case asserts its REFUSAL REASON, not only
the exit status (S111-5).
A. Designation through the REAL snapshot(), with fetch() and the clock mocked:
     - complete and listed -> SPOC; complete and unlisted -> QLP;
     - v1 404 + v2 200 listing the TIC -> SPOC;
     - DDT page 503 or a CTL 503 -> unaffected; a CTL-only listing -> QLP;
     - PENDING with the reason for: a list HTTP 503, a curl failure (0), an HTML body with HTTP 200, a non-integer row, all nine
       versions 404, the orbit table 503 / wrong header / no N+1 row, and a snapshot before the end;
     - a saved file edited after hashing -> derive() refuses.
B. Ledger histories through the real s111_ledger.py CLI and validate_s111_inputs.py, for both TICs in S111:
     - QLP designated, with a later SPOC-listing snapshot that is not operative;
     - SPOC designated with a qualifying selection;
     - a late check with an early release date -> SPOC;
     - fallback certified then final, a later SPOC find staying secondary;
     - a fallback overturned before acquisition;
     - two clean checks < 7 days apart -> not certified;
     - SELECTED with a late release date counting as clean;
     - AMBIGUOUS -> UNRESOLVED, then resolved;
     - UNAVAILABLE final, and its preconditions;
     - acquisition before the route, of the wrong product, or of a non-record selection; a second record acquisition; secondary
       acquisitions (refused while unsettled, accepted after); an AMBIGUOUS QLP check before UNAVAILABLE; a ledger bound to an edited lock;
     - tampered record bytes, a broken hash chain, event-time order, an entry before the lock, another TIC's ledger;
     - results: binds; another light curve; another config's output (consistent chain); output made by other code.
R. Re-check R1-R4: AMBIGUOUS/INCOMPLETE after certification -> UNRESOLVED; pre-designation checks evaluated; same-product secondary
   refused; unusable release dates without crash; byte-exact rollback; empty HTTP-200 bodies -> PENDING.
T. Append transactions: a second writer waits for the lock; the committed bytes are the staged ones even if the source changes;
   an earlier-dated second writer is refused cleanly; no partial files; an interrupted-commit leftover is replaced.
C. Every config: pre binds; refuses an edited config copy and a lock copy whose ledger-tool hash differs; a QLP-designated route binds
   the QLP config and refuses the SPOC config with the stated reason.
Usage: python -I test_s111_lock.py QLP_LOCK SPOC_LOCK TMPDIR   (TMPDIR must not exist)"""
import sys, os, re, csv, json, hashlib, subprocess, shutil, datetime
import numpy as np
from astropy.io import fits
R = "/Users/fernando/Desktop/NASA"; PY = f"{R}/.venv/bin/python"; LQ, LS, TMP = sys.argv[1:4]; VAL = f"{R}/scripts/validate_s111_inputs.py"; LED = f"{R}/scripts/s111_ledger.py"
if os.path.exists(TMP): raise SystemExit(f"refused: {TMP} exists")
os.makedirs(TMP); sys.path.insert(0, f"{R}/scripts"); sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
import target_list_designation as TD, spoc_selection as XS, qlp_selection as XQ
fails = []; n = 0; UTC = datetime.timezone.utc
def check(cond, msg):
    global n; n += 1
    if not cond: fails.append(msg)
    print(("PASS " if cond else "FAIL ") + msg)
def run(args): r = subprocess.run([PY, "-I"] + args, capture_output=True, text=True); return r.returncode, (r.stdout + r.stderr).strip()
def val(lock, stage, cfg, **kw): return run([VAL, "--lock", lock, "--stage", stage, "--config", cfg] + sum(([f"--{k}", v] for k, v in kw.items()), []))
def refused(res, why): return res[0] == 2 and why in res[1]
def bound(res, why=""): return res[0] == 0 and "BOUND" in res[1] and why in res[1]
qlp, spoc = json.load(open(LQ)), json.load(open(LS)); MADE = qlp["made_utc_iso"]; assert spoc["made_utc_iso"] == MADE
END = "2026-12-22 12:00:00"; E = datetime.datetime(2026, 12, 22, 12, tzinfo=UTC); C = E + datetime.timedelta(days=120); F = E + datetime.timedelta(days=365)
iso = lambda t: t.strftime("%Y-%m-%dT%H:%M:%S.%fZ"); mjd = lambda t: (t - datetime.datetime(1858, 11, 17, tzinfo=UTC)).total_seconds() / 86400

# ---------- A: designation via the real snapshot() with mocked fetch and clock
def orbit_table(sector, nxt=True, header="Sector,Orbit,Start of Orbit,End of Orbit", end=END):
    rows = [header, f"{sector},1,2026-11-26 09:15:00,2026-12-09 06:15:00", f"{sector},2,2026-12-09 11:15:00,{end}"]
    if nxt: rows.append(f"{sector + 1},3,2026-12-23 00:00:00,2027-01-05 00:00:00")
    return ("\n".join(rows) + "\n").encode()
def tlist(tics, extra=""): return ("# Full target list\nTICID,Camera,CCD,Tmag,RA,Dec\n" + "".join(f"{t},1,1,10.0,0,0\n" for t in tics) + extra).encode()
DDT_HTML = b'<table><tr><th>DDT #</th><th>PI</th><th>S</th><th>C</th><th>N</th><th>CTL</th></tr><tr><td>200</td><td>A</td><td>B</td><td>2m</td><td>1</td><td><a href="ctls/DDT200_CTL.csv"> x </a></td></tr></table>'
def mock_snapshot(d, sector, tics, now, lists=None, orbit=None, ddt=(200, DDT_HTML), ctl=(200, b"# DDT\nTICID\n9\n")):
    lists = lists if lists is not None else {1: (200, tlist([1, 2, 3]))}
    def fetch(url):
        if url == TD.ORBIT_URL: return orbit if orbit is not None else (200, orbit_table(sector))
        m = re.search(r"all_targets_S(\d+)_v(\d+)\.csv$", url)
        if m: return lists.get(int(m.group(2)), (404, b""))
        if url == TD.DDT_URL: return ddt
        if url.endswith("DDT200_CTL.csv"): return ctl
        return (404, b"")
    class FixedDT(datetime.datetime):
        @classmethod
        def now(cls, tz=None): return now
    TD.fetch, TD.datetime.datetime = fetch, FixedDT
    class A_: pass
    a = A_(); a.sector, a.tics, a.dir = sector, ",".join(map(str, tics)), d
    try: TD.snapshot(a)
    finally: TD.datetime.datetime = datetime.datetime.__mro__[0] if False else _REAL_DT
    return json.load(open(os.path.join(d, "designation.json")))
_REAL_DT = datetime.datetime; _REAL_FETCH = TD.fetch
SNAP_T = datetime.datetime(2027, 1, 5, tzinfo=UTC); T1 = 80387959
def A(tag, **kw): return mock_snapshot(f"{TMP}/A_{tag}", 111, [T1], kw.pop("now", SNAP_T), **kw)
d = A("listed", lists={1: (200, tlist([1, T1]))}); check(d["status"] == "DESIGNATED" and d["per_tic"][str(T1)]["designation"] == "SPOC", "A complete + listed -> SPOC")
d = A("unlisted"); check(d["status"] == "DESIGNATED" and d["per_tic"][str(T1)]["designation"] == "QLP", "A complete + unlisted -> QLP")
d = A("v2only", lists={1: (404, b""), 2: (200, tlist([T1]))}); check(d["per_tic"][str(T1)]["designation"] == "SPOC" and d["per_tic"][str(T1)]["in_target_lists"] == ["all_targets_S111_v2.csv"], "A v1 404 + v2 200 listing the TIC -> SPOC (v2 found)")
d = A("ddt503", ddt=(503, b"")); check(d["status"] == "DESIGNATED", "A DDT page 503 does not affect the designation")
d = A("ctl503", ctl=(503, b"")); check(d["status"] == "DESIGNATED", "A DDT CTL 503 does not affect the designation")
d = A("ctlonly", ctl=(200, f"# DDT\nTICID\n{T1}\n".encode())); check(d["per_tic"][str(T1)]["designation"] == "QLP", "A CTL-only listing -> QLP (DDT lists are context only)")
for tag, kw, why in (("l503", dict(lists={1: (503, b"")}), "version 1: HTTP 503"), ("curl0", dict(lists={1: (200, tlist([1])), 3: (0, b"")}), "version 3: HTTP 0"),
                     ("html200", dict(lists={1: (200, b"<html><body>Maintenance</body></html>")}), "malformed: no TICID header line"),
                     ("nonint", dict(lists={1: (200, tlist([1], extra="abc,1,1,1,0,0\n"))}), "non-integer rows"), ("all404", dict(lists={}), "all 404"),
                     ("orb503", dict(orbit=(503, b"")), "orbit table not retrieved"), ("orbhdr", dict(orbit=(200, orbit_table(111, header="S,O,Start,End"))), "header"),
                     ("orbnext", dict(orbit=(200, orbit_table(111, nxt=False))), "no row for sector 112"),
                     ("early", dict(now=datetime.datetime(2026, 12, 20, tzinfo=UTC)), "before the sector end")):
    d = A(tag, **kw); check(d["status"] == "PENDING" and any(why in r for r in d.get("reasons", [])) and d["per_tic"][str(T1)]["designation"] == "PENDING", f"A {tag} -> PENDING ({why})")
tam = f"{TMP}/A_tam"; shutil.copytree(f"{TMP}/A_unlisted", tam); open(f"{tam}/all_targets_S111_v1.csv", "ab").write(f"{T1},1,1,1,0,0\n".encode())
try: TD.derive(tam); check(False, "A tampered list must not derive")
except ValueError as e: check("does not match its recorded SHA-256" in str(e), "A a saved list edited after hashing -> derive refuses")
TD.fetch = _REAL_FETCH

# ---------- helpers for B
def check_record(kind, out, tic, sector, files, t, release=None, mode="mast_query"):
    X, tool = (XS, "spoc_selection.py") if kind == "spoc" else (XQ, "qlp_selection.py")
    obs = [dict(obs_id=os.path.basename(f)[:-8], t_obs_release=(f"{release:.6f}" if release is not None else "nan"), t_exptime="120.0") for f in files]
    prods = [dict(productFilename=os.path.basename(f), dataURI="mast:TESS/product/" + os.path.basename(f), obsID=str(i), obs_id=os.path.basename(f)[:-8], size="1") for i, f in enumerate(files)]
    resp = out + ".resp"; json.dump(dict(observations=obs, products=prods), open(resp, "w"))
    rc, txt = run([f"{R}/scripts/{tool}", "select", "--tic", str(tic), "--sector", str(sector), "--out", out, "--from-response", resp]); assert rc == 0, txt
    s = json.load(open(out)); s["mode"] = mode; s["query_utc"] = iso(t); json.dump(s, open(out, "w"), indent=1); return out
def spoc_name(tic, sector, d, pipe="0000"): return f"{d}/tess2099001000000-s{sector:04d}-{tic:016d}-{pipe}-s_lc.fits"
def qlp_name(tic, sector, d, rel="v01"): return f"{d}/hlsp_qlp_tess_ffi_s{sector:04d}-{tic:016d}_tess_{rel}_llc.fits"
def lc_fixture(path, tic, sector, tcs, depth, dur, product, seed=1):
    rng = np.random.default_rng(seed); t = np.arange(tcs.min() - 1.0, tcs.max() + 1.0, 2 / 1440 if product == "SPOC" else 200 / 86400); f = 1 + rng.normal(0, 1500e-6, len(t))
    for tc in tcs: f[np.abs(t - tc) < dur / 48] -= depth * 1e-6
    h0 = fits.PrimaryHDU(); h0.header.update(ORIGIN="NASA/Ames" if product == "SPOC" else "MIT/QLP", TICID=tic, SECTOR=sector, TELESCOP="TESS")
    col = "PDCSAP_FLUX" if product == "SPOC" else "SAP_FLUX"
    h1 = fits.BinTableHDU.from_columns([fits.Column(name="TIME", format="D", array=t), fits.Column(name=col, format="E", array=f * 1000), fits.Column(name=col + "_ERR", format="E", array=np.full(len(t), 1.5)),
                                        fits.Column(name="QUALITY", format="J", array=np.zeros(len(t), int))])
    h1.header.update(TIMESYS="TDB", TIMEREF="SOLARSYSTEM", BJDREFI=2457000, BJDREFF=0.0, TIMEUNIT="d"); fits.HDUList([h0, h1]).writeto(path)
def ledger(tag, tic, sector, lq=None, ls=None):
    p = f"{TMP}/B_{tag}"; rc, txt = run([LED, "init", "--ledger", p, "--tic", str(tic), "--sector", str(sector), "--lock-qlp", lq or LQ, "--lock-spoc", ls or LS]); assert rc == 0, txt; return p
def app(lg, typ, rec, role=None): return run([LED, "append", "--ledger", lg, "--type", typ, "--record", rec] + (["--role", role] if role else []))
def snapdir(tag, tic, sector, listed, now): return mock_snapshot(f"{TMP}/S_{tag}", sector, [tic], now, lists={1: (200, tlist([1] + ([tic] if listed else [])))}) and f"{TMP}/S_{tag}"
def acq(kind, out, sel, lc, t): X = XS if kind == "spoc" else XQ; json.dump(X.make_acquisition(sel, lc, "mast_download", iso(t)), open(out, "w")); return out
def dispo(out, kind, t): json.dump(dict(disposition=kind, disposition_utc=iso(t), basis="test"), open(out, "w")); return out
day = lambda k: datetime.timedelta(days=k)
CFG = lambda tic, s, prod: f"{R}/configs/conformance/{tic}_S{s}{'_spoc' if prod == 'SPOC' else ''}.json"

# ---------- B: ledger histories (both TICs, S111)
for tic in (80387959, 120517801):
    sec = 111; cq, cs_ = CFG(tic, sec, "QLP"), CFG(tic, sec, "SPOC"); W = f"{TMP}/w_{tic}"; os.makedirs(W)
    cfgq = json.load(open(cq)); tcs = np.array([float(r["tc_btjd"]) for r in csv.DictReader(open(cfgq["pred_csv"])) if r["status"].startswith("prediction") and (m := re.match(r"(\d+)", str(r["tess_sector"]))) and int(m.group(1)) == sec])
    lcs = spoc_name(tic, sec, W); lc_fixture(lcs, tic, sec, tcs, cfgq["ref_depth_ppm"], cfgq["ref_dur_h"], "SPOC")
    lcq = qlp_name(tic, sec, W); lc_fixture(lcq, tic, sec, tcs, cfgq["ref_depth_ppm"], cfgq["ref_dur_h"], "QLP")
    ev_s = f"{W}/ev_spoc.json"; run([f"{R}/scripts/prereg_conformance_spoc.py", "--config", cs_, "--lc", lcs, "--out", ev_s])
    ev_q = f"{W}/ev_qlp.json"; run([f"{R}/scripts/prereg_conformance.py", "--config", cq, "--lc", lcq, "--out", ev_q])
    k = f"{tic} S111"
    # B1: QLP designated; PENDING first; later SPOC-listing snapshot not operative
    lg = ledger(f"{tic}_qlp", tic, sec)
    pend = mock_snapshot(f"{TMP}/S_{tic}_pend", sec, [tic], E + day(1), orbit=(200, orbit_table(sec, nxt=False)))
    check(app(lg, "designation_snapshot", f"{TMP}/S_{tic}_pend")[0] == 0, f"{k} B1 a PENDING snapshot is recorded")
    check(refused(val(LQ, "route", cq, ledger=lg), "no operative designation"), f"{k} B1 route refused while only PENDING")
    app(lg, "designation_snapshot", snapdir(f"{tic}_q1", tic, sec, False, E + day(2)))
    check(app(lg, "designation_snapshot", snapdir(f"{tic}_q2", tic, sec, True, E + day(9)))[0] == 0, f"{k} B1 a later SPOC-listing snapshot is recorded")
    check(bound(val(LQ, "route", cq, ledger=lg), "route QLP"), f"{k} B1 route QLP binds the QLP config (the later snapshot is not operative)")
    check(refused(val(LS, "route", cs_, ledger=lg), "is not the product of record"), f"{k} B1 route refuses the SPOC config")
    q_none = check_record("qlp", f"{W}/q_none.json", tic, sec, [], E + day(20))
    check(app(lg, "qlp_check", q_none)[0] == 0, f"{k} B1 QLP NONE check recorded")
    r = app(lg, "acquisition", acq("qlp", f"{W}/a_q_early.json", q_none if False else check_record("qlp", f"{W}/q_tmp.json", tic, sec, [lcq], E + day(21), mjd(E + day(21))), lcq, E + day(22)), "record")
    check(r[0] != 0 and "no QLP release of record" in r[1], f"{k} B1 QLP acquisition before any QLP selection in the ledger is refused")
    q_sel = check_record("qlp", f"{W}/q_sel.json", tic, sec, [lcq], E + day(30), mjd(E + day(28)))
    app(lg, "qlp_check", q_sel)
    r = app(lg, "acquisition", acq("qlp", f"{W}/a_q_wrongsel.json", f"{W}/q_tmp.json", lcq, E + day(31)), "record")
    check(r[0] != 0 and "does not reference the release-of-record selection" in r[1], f"{k} B1 acquisition referencing another selection is refused")
    check(app(lg, "acquisition", acq("qlp", f"{W}/a_q.json", q_sel, lcq, E + day(32)), "record")[0] == 0, f"{k} B1 QLP record acquisition appended")
    check(bound(val(LQ, "result", cq, ledger=lg, lc=lcq, result=ev_q), "ALSO REQUIRED: validate_round4_inputs.py"), f"{k} B1 QLP result binds and names the round-4 requirement")
    lcq2 = f"{W}/other/" + os.path.basename(lcq); os.makedirs(f"{W}/other"); lc_fixture(lcq2, tic, sec, tcs, 0, 2, "QLP", seed=5)
    check(refused(val(LQ, "result", cq, ledger=lg, lc=lcq2, result=ev_q), "not the ledger's record acquisition"), f"{k} B1 result refuses another light curve")
    # tamper
    tl = f"{TMP}/B_{tic}_qlp_tam"; shutil.copytree(lg, tl); recf = sorted(os.listdir(f"{tl}/records"))[-1]; open(f"{tl}/records/{recf}", "a").write(" ")
    check(refused(val(LQ, "route", cq, ledger=tl), "record bytes differ"), f"{k} B tampered record bytes refused")
    tl2 = f"{TMP}/B_{tic}_qlp_chain"; shutil.copytree(lg, tl2); L_ = open(f"{tl2}/ledger.jsonl").read().splitlines(); L_[2] = L_[2].replace('"seq": 2', '"seq": 2 ') ; open(f"{tl2}/ledger.jsonl", "w").write("\n".join(L_) + "\n")
    check(refused(val(LQ, "route", cq, ledger=tl2), "hash chain broken"), f"{k} B edited ledger line refused (hash chain)")
    r = app(lg, "qlp_check", check_record("qlp", f"{W}/q_back.json", tic, sec, [], E + day(5)))
    check(r[0] != 0 and "earlier than the previous entry" in r[1], f"{k} B entry earlier than the previous one refused")
    bad_lock = f"{W}/edited_lock.json"; bl = json.load(open(LQ)); bl["note"] = "edited"; json.dump(bl, open(bad_lock, "w"))
    lge = ledger(f"{tic}_badlock", tic, sec, lq=bad_lock); app(lge, "designation_snapshot", snapdir(f"{tic}_bl", tic, sec, False, E + day(2)))
    check(refused(val(LQ, "route", cq, ledger=lge), "initialised for another lock"), f"{k} B a ledger initialised against an edited lock copy is refused")
    other_tic = 120517801 if tic == 80387959 else 80387959
    check(refused(val(LQ, "route", CFG(other_tic, sec, "QLP"), ledger=lg), "another TIC"), f"{k} B another TIC's ledger refused")
    lgb = ledger(f"{tic}_prelock", tic, sec); r = app(lgb, "designation_snapshot", snapdir(f"{tic}_old", tic, sec, False, datetime.datetime(2026, 10, 1, tzinfo=UTC)))
    check(r[0] != 0 and "not later than the lock" in r[1], f"{k} B entry before the lock refused")
    # B2: SPOC designated with qualifying selection
    lg = ledger(f"{tic}_spoc", tic, sec); app(lg, "designation_snapshot", snapdir(f"{tic}_s1", tic, sec, True, E + day(2)))
    s_sel = check_record("spoc", f"{W}/s_sel.json", tic, sec, [lcs], E + day(40), mjd(E + day(35)))
    q_pre = check_record("qlp", f"{W}/s_qpre.json", tic, sec, [lcq], E + day(3), mjd(E + day(3))); app(lg, "qlp_check", q_pre)
    r = app(lg, "acquisition", acq("qlp", f"{W}/a_q_sec_early.json", q_pre, lcq, E + day(3) + datetime.timedelta(hours=1)), "secondary")
    check(r[0] != 0 and "route is SPOC_PENDING" in r[1], f"{k} B2 a secondary acquisition is refused while the route is SPOC_PENDING")
    r = app(lg, "acquisition", acq("spoc", f"{W}/a_s_early.json", s_sel, lcs, E + day(3)), "record")
    check(r[0] != 0 and "route is SPOC_PENDING" in r[1], f"{k} B2 acquisition before a qualifying selection refused (route SPOC_PENDING)")
    check(refused(val(LS, "route", cs_, ledger=lg), "route is SPOC_PENDING"), f"{k} B2 route refused while SPOC_PENDING")
    app(lg, "spoc_check", s_sel); app(lg, "acquisition", acq("spoc", f"{W}/a_s.json", s_sel, lcs, E + day(41)), "record")
    check(bound(val(LS, "route", cs_, ledger=lg), "route SPOC"), f"{k} B2 route SPOC binds the SPOC config")
    check(refused(val(LQ, "route", cq, ledger=lg), "is not the product of record"), f"{k} B2 route refuses the QLP config")
    check(bound(val(LS, "result", cs_, ledger=lg, lc=lcs, result=ev_s)), f"{k} B2 SPOC result binds")
    r = app(lg, "acquisition", acq("spoc", f"{W}/a_s_twice.json", s_sel, lcs, E + day(42)), "record")
    check(r[0] != 0 and "a record acquisition already exists" in r[1], f"{k} B2 a second record acquisition is refused")
    q2 = check_record("qlp", f"{W}/s_qsec.json", tic, sec, [lcq], E + day(43), mjd(E + day(40))); app(lg, "qlp_check", q2)
    check(app(lg, "acquisition", acq("qlp", f"{W}/a_q_sec.json", q2, lcq, E + day(44)), "secondary")[0] == 0, f"{k} B2 a secondary QLP acquisition is accepted once the route is settled")
    check(bound(val(LS, "route", cs_, ledger=lg), "route SPOC"), f"{k} B2 a secondary acquisition does not change the route")
    e2 = json.load(open(ev_s)); e2["script_sha256"] = "0" * 64; json.dump(e2, open(f"{W}/ev_alt.json", "w"))
    check(refused(val(LS, "result", cs_, ledger=lg, lc=lcs, result=f"{W}/ev_alt.json"), "different evaluator"), f"{k} B2 result refuses output made by other code")
    # consistent chain for another sector (S112) with this sector's output -> config mismatch
    lg12 = ledger(f"{tic}_spoc12", tic, 112); app(lg12, "designation_snapshot", snapdir(f"{tic}_s12", tic, 112, True, E + day(2)))
    lcs12 = spoc_name(tic, 112, f"{W}/s12"); os.makedirs(f"{W}/s12"); shutil.copy(lcs, f"{W}/s12/tmp.fits"); lc_fixture(lcs12, tic, 112, tcs, 500, 2, "SPOC")
    s12 = check_record("spoc", f"{W}/s12_sel.json", tic, 112, [lcs12], E + day(40), mjd(E + day(35))); app(lg12, "spoc_check", s12); app(lg12, "acquisition", acq("spoc", f"{W}/a12.json", s12, lcs12, E + day(41)), "record")
    ev12 = f"{W}/ev12_wrongcfg.json"; e3 = json.load(open(ev_s)); e3["lc_sha256"] = sha(lcs12); json.dump(e3, open(ev12, "w"))
    check(refused(val(LS, "result", CFG(tic, 112, "SPOC"), ledger=lg12, lc=lcs12, result=ev12), "output was made from a different config"), f"{k} B2 result refuses another config's output (consistent S112 chain)")
    # B3: late check with an early release date -> SPOC
    lg = ledger(f"{tic}_late", tic, sec); app(lg, "designation_snapshot", snapdir(f"{tic}_l1", tic, sec, True, E + day(2)))
    app(lg, "spoc_check", check_record("spoc", f"{W}/l_none.json", tic, sec, [], C + day(1)))
    app(lg, "spoc_check", check_record("spoc", f"{W}/l_sel.json", tic, sec, [lcs], C + day(5), mjd(C - day(10))))
    check(bound(val(LS, "route", cs_, ledger=lg), "route SPOC"), f"{k} B3 a late check finding a release dated before the cutoff -> SPOC")
    # B4: fallback certified then final; later SPOC find secondary
    lg = ledger(f"{tic}_fb", tic, sec); app(lg, "designation_snapshot", snapdir(f"{tic}_f1", tic, sec, True, E + day(2)))
    app(lg, "spoc_check", check_record("spoc", f"{W}/f_n1.json", tic, sec, [], C + day(1)))
    check(refused(val(LQ, "route", cq, ledger=lg), "route is SPOC_PENDING"), f"{k} B4 one clean check after the cutoff does not certify")
    app(lg, "spoc_check", check_record("spoc", f"{W}/f_n2.json", tic, sec, [], C + day(9)))
    check(bound(val(LQ, "route", cq, ledger=lg), "QLP_FALLBACK_CERTIFIED"), f"{k} B4 two clean checks >= 7 d apart certify the fallback")
    fq = check_record("qlp", f"{W}/f_q.json", tic, sec, [lcq], C + day(10), mjd(C)); app(lg, "qlp_check", fq)
    app(lg, "acquisition", acq("qlp", f"{W}/f_aq.json", fq, lcq, C + day(11)), "record")
    app(lg, "spoc_check", check_record("spoc", f"{W}/f_late.json", tic, sec, [lcs], C + day(20), mjd(C - day(30))))
    check(bound(val(LQ, "route", cq, ledger=lg), "QLP_FALLBACK_FINAL"), f"{k} B4 fallback final after QLP acquisition; a later SPOC find stays secondary")
    check(refused(val(LS, "route", cs_, ledger=lg), "is not the product of record"), f"{k} B4 SPOC config refused after the fallback is final")
    # B5: fallback overturned before acquisition
    lg = ledger(f"{tic}_over", tic, sec); app(lg, "designation_snapshot", snapdir(f"{tic}_o1", tic, sec, True, E + day(2)))
    app(lg, "spoc_check", check_record("spoc", f"{W}/o_n1.json", tic, sec, [], C + day(1))); app(lg, "spoc_check", check_record("spoc", f"{W}/o_n2.json", tic, sec, [], C + day(9)))
    app(lg, "spoc_check", check_record("spoc", f"{W}/o_sel.json", tic, sec, [lcs], C + day(12), mjd(C - day(3))))
    check(bound(val(LS, "route", cs_, ledger=lg), "route SPOC"), f"{k} B5 a qualifying SPOC release before any QLP acquisition overturns the certified fallback")
    # B6: two clean < 7 d apart -> not certified; B7: SELECTED with a late release counts as clean
    lg = ledger(f"{tic}_short", tic, sec); app(lg, "designation_snapshot", snapdir(f"{tic}_sh", tic, sec, True, E + day(2)))
    app(lg, "spoc_check", check_record("spoc", f"{W}/sh1.json", tic, sec, [], C + day(1))); app(lg, "spoc_check", check_record("spoc", f"{W}/sh2.json", tic, sec, [], C + day(4)))
    check(refused(val(LQ, "route", cq, ledger=lg), "route is SPOC_PENDING"), f"{k} B6 two clean checks < 7 d apart do not certify")
    app(lg, "spoc_check", check_record("spoc", f"{W}/sh3.json", tic, sec, [lcs], C + day(10), mjd(C + day(2))))
    check(bound(val(LQ, "route", cq, ledger=lg), "QLP_FALLBACK_CERTIFIED"), f"{k} B7 a SELECTED check with a release date after the cutoff counts as clean")
    # B8: AMBIGUOUS -> UNRESOLVED, then resolved
    lg = ledger(f"{tic}_amb", tic, sec); app(lg, "designation_snapshot", snapdir(f"{tic}_a1", tic, sec, True, E + day(2)))
    app(lg, "spoc_check", check_record("spoc", f"{W}/am1.json", tic, sec, [lcs, spoc_name(tic, sec, W, "0001")], C + day(1), mjd(C - day(1))))
    check(refused(val(LQ, "route", cq, ledger=lg), "route is UNRESOLVED"), f"{k} B8 AMBIGUOUS after the cutoff -> UNRESOLVED")
    r = app(lg, "acquisition", acq("qlp", f"{W}/am_aq.json", fq, lcq, C + day(2)), "record"); check(r[0] != 0 and "route is UNRESOLVED" in r[1], f"{k} B8 acquisition refused while UNRESOLVED")
    app(lg, "spoc_check", check_record("spoc", f"{W}/am2.json", tic, sec, [], C + day(3))); app(lg, "spoc_check", check_record("spoc", f"{W}/am3.json", tic, sec, [], C + day(11)))
    check(bound(val(LQ, "route", cq, ledger=lg), "QLP_FALLBACK_CERTIFIED"), f"{k} B8 later clean checks resolve UNRESOLVED into a certified fallback")
    # B9/B10: UNAVAILABLE
    lg = ledger(f"{tic}_unav", tic, sec); app(lg, "designation_snapshot", snapdir(f"{tic}_u1", tic, sec, False, E + day(2)))
    r = app(lg, "disposition", dispo(f"{W}/d_early.json", "UNAVAILABLE", E + day(100))); check(r[0] != 0 and "before the unavailable cutoff" in r[1], f"{k} B10 UNAVAILABLE before end + 365 d refused")
    r = app(lg, "disposition", dispo(f"{W}/d_nocheck.json", "UNAVAILABLE", F + day(1))); check(r[0] != 0 and "complete QLP check" in r[1], f"{k} B10 UNAVAILABLE without a complete QLP check after the cutoff refused")
    app(lg, "qlp_check", check_record("qlp", f"{W}/u_qamb.json", tic, sec, [lcq, qlp_name(tic, sec, W + "/x")], F + day(1) + datetime.timedelta(hours=12), mjd(F + day(1))))
    r = app(lg, "disposition", dispo(f"{W}/d_amb.json", "UNAVAILABLE", F + day(1) + datetime.timedelta(hours=13)))
    check(r[0] != 0 and "complete QLP check" in r[1], f"{k} B10 an AMBIGUOUS QLP check after end + 365 d does not allow UNAVAILABLE")
    app(lg, "qlp_check", check_record("qlp", f"{W}/u_q.json", tic, sec, [], F + day(2)))
    check(app(lg, "disposition", dispo(f"{W}/d_ok.json", "UNAVAILABLE", F + day(3)))[0] == 0, f"{k} B9 UNAVAILABLE recorded after a complete QLP check past end + 365 d")
    r = app(lg, "acquisition", acq("qlp", f"{W}/u_aq.json", fq, lcq, F + day(4)), "record"); check(r[0] != 0 and "after the final disposition" in r[1], f"{k} B9 acquisition after UNAVAILABLE refused")
    check(refused(val(LQ, "route", cq, ledger=lg), "final disposition UNAVAILABLE"), f"{k} B9 route refused after UNAVAILABLE")

    # R1: unresolved after certification (AMBIGUOUS and INCOMPLETE) withdraws it
    for kind in ("amb", "inc"):
        lg = ledger(f"{tic}_r1{kind}", tic, sec); app(lg, "designation_snapshot", snapdir(f"{tic}_r1{kind}", tic, sec, True, E + day(2)))
        app(lg, "spoc_check", check_record("spoc", f"{W}/r1{kind}_n1.json", tic, sec, [], C + day(1))); app(lg, "spoc_check", check_record("spoc", f"{W}/r1{kind}_n2.json", tic, sec, [], C + day(9)))
        bad = (check_record("spoc", f"{W}/r1{kind}_bad.json", tic, sec, [lcs, spoc_name(tic, sec, W, "0001")], C + day(10), mjd(C - day(1))) if kind == "amb"
               else check_record("spoc", f"{W}/r1{kind}_bad.json", tic, sec, [lcs], C + day(10), None))
        app(lg, "spoc_check", bad)
        check(refused(val(LQ, "route", cq, ledger=lg), "route is UNRESOLVED"), f"{k} R1 {kind.upper()} after certification withdraws it (UNRESOLVED)")
        fq1 = check_record("qlp", f"{W}/r1{kind}_q.json", tic, sec, [lcq], C + day(11), mjd(C)); app(lg, "qlp_check", fq1)
        r = app(lg, "acquisition", acq("qlp", f"{W}/r1{kind}_aq.json", fq1, lcq, C + day(12)), "record"); check(r[0] != 0 and "route is UNRESOLVED" in r[1], f"{k} R1 {kind.upper()}: QLP acquisition refused while UNRESOLVED")
        app(lg, "spoc_check", check_record("spoc", f"{W}/r1{kind}_n3.json", tic, sec, [], C + day(13))); app(lg, "spoc_check", check_record("spoc", f"{W}/r1{kind}_n4.json", tic, sec, [], C + day(21)))
        check(bound(val(LQ, "route", cq, ledger=lg), "QLP_FALLBACK_CERTIFIED"), f"{k} R1 {kind.upper()}: a new two-check certification resolves it")
    # R2: checks before the designation are evaluated under its cutoffs
    lg = ledger(f"{tic}_r2s", tic, sec)
    app(lg, "spoc_check", check_record("spoc", f"{W}/r2s_sel.json", tic, sec, [lcs], E + day(1), mjd(E + day(1))))
    app(lg, "designation_snapshot", snapdir(f"{tic}_r2s", tic, sec, True, E + day(2)))
    app(lg, "spoc_check", check_record("spoc", f"{W}/r2s_n1.json", tic, sec, [], C + day(1))); app(lg, "spoc_check", check_record("spoc", f"{W}/r2s_n2.json", tic, sec, [], C + day(9)))
    check(bound(val(LS, "route", cs_, ledger=lg), "route SPOC"), f"{k} R2 a qualifying SPOC selection before the designation keeps SPOC despite later NONE checks")
    lg = ledger(f"{tic}_r2q", tic, sec)
    r2q = check_record("qlp", f"{W}/r2q_sel.json", tic, sec, [lcq], E + day(1), mjd(E + day(1))); app(lg, "qlp_check", r2q)
    app(lg, "designation_snapshot", snapdir(f"{tic}_r2q", tic, sec, False, E + day(2)))
    app(lg, "qlp_check", check_record("qlp", f"{W}/r2q_n.json", tic, sec, [], F + day(1)))
    r = app(lg, "disposition", dispo(f"{W}/r2q_d.json", "UNAVAILABLE", F + day(2))); check(r[0] != 0 and "no QLP release of record" in r[1], f"{k} R2 a qualifying QLP selection before the designation blocks UNAVAILABLE")
    check(app(lg, "acquisition", acq("qlp", f"{W}/r2q_aq.json", r2q, lcq, F + day(3)), "record")[0] == 0, f"{k} R2 the pre-designation QLP selection is the release of record")
    # R3: secondary role cannot be the route's own product
    lg = ledger(f"{tic}_r3", tic, sec); app(lg, "designation_snapshot", snapdir(f"{tic}_r3", tic, sec, True, E + day(2)))
    app(lg, "spoc_check", check_record("spoc", f"{W}/r3_n1.json", tic, sec, [], C + day(1))); app(lg, "spoc_check", check_record("spoc", f"{W}/r3_n2.json", tic, sec, [], C + day(9)))
    r3q = check_record("qlp", f"{W}/r3_q.json", tic, sec, [lcq], C + day(10), mjd(C)); app(lg, "qlp_check", r3q)
    r = app(lg, "acquisition", acq("qlp", f"{W}/r3_aq_sec.json", r3q, lcq, C + day(11)), "secondary")
    check(r[0] != 0 and "must be of the other product" in r[1], f"{k} R3 a secondary acquisition of the route's own product (QLP under fallback) is refused")
    r = app(lg, "acquisition", acq("spoc", f"{W}/r3_as_sec.json", f"{W}/s_sel.json", lcs, C + day(11)), "secondary")
    check(r[0] != 0 and "does not reference a SELECTED SPOC check in this ledger" in r[1], f"{k} R3 a secondary acquisition without a selection in this ledger is refused")
    app(lg, "acquisition", acq("qlp", f"{W}/r3_aq.json", r3q, lcq, C + day(12)), "record")
    app(lg, "spoc_check", check_record("spoc", f"{W}/r3_late.json", tic, sec, [lcs], C + day(13), mjd(C - day(5))))
    check(bound(val(LQ, "route", cq, ledger=lg), "QLP_FALLBACK_FINAL"), f"{k} R3 after the QLP record acquisition a timely SPOC find cannot promote SPOC")
    # R4: unusable release dates; byte-exact rollback of refused appends
    lg = ledger(f"{tic}_r4", tic, sec); app(lg, "designation_snapshot", snapdir(f"{tic}_r4", tic, sec, True, E + day(2)))
    rinf = app(lg, "spoc_check", check_record("spoc", f"{W}/r4_inf.json", tic, sec, [lcs], E + day(3), float("inf")))
    check(rinf[0] == 0 and refused(val(LS, "route", cs_, ledger=lg), "route is SPOC_PENDING"), f"{k} R4 an infinite release date is accepted as unusable (not qualifying), no crash")
    app(lg, "spoc_check", check_record("spoc", f"{W}/r4_big.json", tic, sec, [lcs], C + day(1), 1e9))
    check(refused(val(LQ, "route", cq, ledger=lg), "route is UNRESOLVED"), f"{k} R4 an out-of-range release date after the cutoff is unresolved")
    before = (open(f"{lg}/ledger.jsonl", "rb").read(), sorted(os.listdir(f"{lg}/records")))
    open(f"{W}/r4_notjson.json", "w").write("{not json")
    r = app(lg, "qlp_check", f"{W}/r4_notjson.json"); after = (open(f"{lg}/ledger.jsonl", "rb").read(), sorted(os.listdir(f"{lg}/records")))
    check(r[0] != 0 and "REFUSED (not written)" in r[1] and before == after, f"{k} R4 an unparsable record is refused and the ledger bytes are unchanged")
    r = app(lg, "acquisition", acq("qlp", f"{W}/r4_aq.json", fq, lcq, C + day(2)), "record"); after2 = (open(f"{lg}/ledger.jsonl", "rb").read(), sorted(os.listdir(f"{lg}/records")))
    check(r[0] != 0 and before == after2, f"{k} R4 a rule-refused append leaves the ledger bytes unchanged")
d = mock_snapshot(f"{TMP}/A_empty200", 111, [T1], SNAP_T, lists={1: (200, b"")}) if False else None
_REAL_FETCH2 = TD.fetch
d = A("empty200", lists={1: (200, b"")}); check(d["status"] == "PENDING" and any("empty body" in r for r in d["reasons"]), "A an HTTP 200 with an empty target-list body -> PENDING (empty body), no crash")
d = A("orbempty", orbit=(200, b"")); check(d["status"] == "PENDING" and any("empty body" in r for r in d["reasons"]), "A an HTTP 200 with an empty orbit table -> PENDING, no crash")
TD.fetch = _REAL_FETCH

# ---------- T: append transactions under concurrent writers (RECHECK2)
import time
def popen_app(lg, typ, rec, env_extra=None):
    env = dict(os.environ, **(env_extra or {}))
    return subprocess.Popen([PY, "-I", LED, "append", "--ledger", lg, "--type", typ, "--record", rec], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=env)
def ledger_bytes(lg): return open(f"{lg}/ledger.jsonl", "rb").read()
tic, sec = 80387959, 111; W = f"{TMP}/w_T"; os.makedirs(W)
for order in ("later_second", "earlier_second"):
    lg = ledger(f"T_{order}", tic, sec); app(lg, "designation_snapshot", snapdir(f"T_{order}", tic, sec, False, E + day(2)))
    tA, tB = (E + day(3), E + day(4)) if order == "later_second" else (E + day(4), E + day(3))
    recA = check_record("qlp", f"{W}/{order}_A.json", tic, sec, [], tA); recB = check_record("qlp", f"{W}/{order}_B.json", tic, sec, [], tB)
    shaA = sha(recA); flag = f"{W}/{order}_go"
    pA = popen_app(lg, "qlp_check", recA, {"S111_LEDGER_PAUSE_AFTER_STAGE": flag}); time.sleep(2.0)
    pB = popen_app(lg, "qlp_check", recB); time.sleep(2.0)
    before = ledger_bytes(lg)
    check(pA.poll() is None and pB.poll() is None, f"T {order}: writer B waits while writer A holds the lock (both still running)")
    j = json.load(open(recA)); j["query_utc"] = iso(tA + day(30)); json.dump(j, open(recA, "w"))       # alter A's source after staging
    check(ledger_bytes(lg) == before, f"T {order}: nothing committed while A is paused")
    open(flag, "w").write("go"); outA, _ = pA.communicate(timeout=120); outB, _ = pB.communicate(timeout=120)
    lines = open(f"{lg}/ledger.jsonl").read().splitlines(); ents = [json.loads(l) for l in lines[1:]]
    qlp_ents = [e for e in ents if e["type"] == "qlp_check"]
    check(pA.returncode == 0 and qlp_ents and qlp_ents[0]["record_sha256"] == shaA, f"T {order}: A committed its STAGED bytes (SHA matches the pre-alteration record)")
    rc, txt = run([LED, "replay", "--ledger", lg]); check(rc == 0, f"T {order}: the final history replays")
    if order == "later_second":
        check(pB.returncode == 0 and len(qlp_ents) == 2 and [e["event_utc"] for e in qlp_ents] == [iso(tA), iso(tB)], f"T {order}: B committed after A, in event order")
    else:
        check(pB.returncode != 0 and "earlier than the previous entry" in outB and len(qlp_ents) == 1, f"T {order}: B (earlier event) refused after A's commit, nothing of B written")
    check(not any(f.startswith(".tmp_") for f in os.listdir(lg)) and all(e["record"] in {x["record"] for x in ents} for e in ents), f"T {order}: no partial files left in the ledger")
lg = ledger("T_orphan", tic, sec); app(lg, "designation_snapshot", snapdir("T_orphan", tic, sec, False, E + day(2)))
open(f"{lg}/records/002_qlp_check.json", "w").write("orphan from an interrupted commit")
check(app(lg, "qlp_check", check_record("qlp", f"{W}/orph.json", tic, sec, [], E + day(3)))[0] == 0 and run([LED, "replay", "--ledger", lg])[0] == 0
      and sha(f"{lg}/records/002_qlp_check.json") == sha(f"{W}/orph.json"), "T an unreferenced leftover of an interrupted commit is replaced under the lock")

# ---------- C: every config
for lockf, lk in ((LQ, qlp), (LS, spoc)):
    for kname, Lent in sorted(lk["configs"].items()):
        cfgp = f"{R}/configs/conformance/{kname}"; c = json.load(open(cfgp)); tic, sec = c["tic"], c["sector"]
        check(sha(cfgp) == Lent["config_sha256"] and bound(val(lockf, "pre", cfgp)), f"{kname} pre binds")
        p = f"{TMP}/C_{kname}"; json.dump(dict(c, note="x"), open(p, "w")); check(refused(val(lockf, "pre", p), "not in the lock manifest"), f"{kname} pre refuses an edited config copy")
        bl = json.loads(json.dumps(lk)); bl["configs"][kname]["s111_ledger_code_sha256"] = "0" * 64; blp = f"{TMP}/C_{kname}_badlock.json"; json.dump(bl, open(blp, "w"))
        check(refused(val(blp, "pre", cfgp), "s111_ledger.py SHA-256 differs"), f"{kname} pre refuses a lock whose ledger-tool hash differs")
        lg = ledger(f"C_{kname}", tic, sec); app(lg, "designation_snapshot", snapdir(f"C_{kname}", tic, sec, False, E + day(2)))
        res = val(lockf, "route", cfgp, ledger=lg)
        if c["product"] == "QLP": check(bound(res, "route QLP"), f"{kname} QLP-designated route binds")
        else: check(refused(res, "is not the product of record"), f"{kname} QLP-designated route refuses the SPOC config")
print(f"{n - len(fails)}/{n} passed"); sys.exit(1 if fails else 0)
