"""Product-of-record designation snapshot for the S111+ tests of TIC 80387959 and 120517801 (v2, 2026-10-25; rule DECISIONS 178(a) as
refined in 193-194; review S111-1/2). METADATA ONLY: no light curve, FFI, cutout or pixel file is fetched.
  snapshot --sector N --tics T1,T2 --dir DIR
      Fetches and SAVES (bytes, HTTP status, SHA-256), in a fresh directory DIR:
        REQUIRED  the official orbit table https://tess.mit.edu/public/files/TESS_orbit_times.csv;
        REQUIRED  the 2-min target lists https://tess.mit.edu/public/target_lists/2m/all_targets_S<N>_v<k>.csv for EVERY k = 1..9
                  (bounded discovery: the directory index is forbidden, so versions above 9 are not discovered; declared);
        CONTEXT   the DDT page https://tess.mit.edu/public/DDTs/DDT_list.html and every DDT target list it links (DDT lists carry no
                  sector and never affect the designation; their failures are recorded but are not blocking).
      It writes DIR/snapshot.json and DIR/designation.json = derive(DIR).
  derive(DIR): the ONE derivation, re-run by scripts/validate_s111_inputs.py on the saved files. Status DESIGNATED requires:
      - every saved file matches its recorded SHA-256;
      - the orbit table: HTTP 200, header exactly 'Sector,Orbit,Start of Orbit,End of Orbit', at least one row for sector N and one for
        sector N+1 (otherwise the end of N may not be final); the sector end is the latest 'End of Orbit' of N in THIS saved table;
      - snapshot time >= sector end;
      - every target-list version k = 1..9 answered 200 or 404 (any other status or a fetch error -> PENDING), at least one answered
        200, and every 200 body is a valid list: after '#' comment lines, a header line starting 'TICID', then >= 1 integer TIC rows
        and no non-integer rows.
      An HTTP 200 with an empty body counts as malformed. Any failure gives PENDING with the reasons; PENDING never means "unlisted".
      Designation (DESIGNATED only): SPOC if the TIC is in the TICID column of any saved valid all_targets_S<N>_v<k>.csv, otherwise QLP.
      Cutoffs from the same saved table: spoc_cutoff_utc = end + 120 d, unavailable_cutoff_utc = end + 365 d.
Fetching uses the system curl with TLS verified (Python's OpenSSL + certifi fails on tess.mit.edu's certificate chain).
Never overwrites. Usage: python -I target_list_designation.py snapshot --sector 111 --tics 80387959,120517801 --dir DIR"""
import sys, os, re, csv, io, json, hashlib, argparse, datetime
ORBIT_URL = "https://tess.mit.edu/public/files/TESS_orbit_times.csv"
LIST_URL = "https://tess.mit.edu/public/target_lists/2m/all_targets_S{n}_v{k}.csv"; MAX_VERSION = 9
DDT_URL = "https://tess.mit.edu/public/DDTs/DDT_list.html"; DDT_BASE = "https://tess.mit.edu/public/DDTs/"
ORBIT_HEADER = "Sector,Orbit,Start of Orbit,End of Orbit"
sha = lambda b: hashlib.sha256(b).hexdigest()
UTC = datetime.timezone.utc; ISO = "%Y-%m-%dT%H:%M:%S.%fZ"

def fetch(url):
    """HTTP GET with the system curl (TLS verified). Returns (status, bytes); status 0 means the fetch itself failed."""
    import subprocess, tempfile
    with tempfile.NamedTemporaryFile(delete=False) as tf: tmp = tf.name
    try:
        r = subprocess.run(["curl", "-sS", "--max-time", "90", "-A", "tess-transit-candidates/1.19", "-o", tmp, "-w", "%{http_code}", url], capture_output=True, text=True)
        code = int(r.stdout.strip() or 0) if r.returncode == 0 else 0
        return code, (open(tmp, "rb").read() if code == 200 else b"")
    finally: os.remove(tmp)

def ddt_rows(html):
    out = []
    for r in re.findall(r"<tr[^>]*>(.*?)</tr>", html, re.S | re.I):
        cells = re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", r, re.S | re.I)
        if len(cells) < 5 or not re.sub(r"<[^>]+>", "", cells[0]).strip().isdigit(): continue
        link = re.search(r'href="([^"]+)"', cells[5]) if len(cells) > 5 else None
        txt = lambda c: re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", c)).strip()
        out.append(dict(ddt=txt(cells[0]), pi=txt(cells[1]), subject=txt(cells[2]), cadence=txt(cells[3]), n_targets=txt(cells[4]), ctl=link.group(1) if link else None))
    return out

def parse_target_list(raw):
    """(set of TIC ids, error or None). Valid: optional '#' comment lines, a header line starting 'TICID', then integer TIC rows only."""
    lines = [l for l in raw.decode("utf-8", "replace").splitlines() if l.strip()]
    body = [l for l in lines if not l.lstrip().startswith("#")]
    if not body or not body[0].replace(" ", "").upper().startswith("TICID"): return set(), "no TICID header line"
    tics, bad = set(), 0
    for l in body[1:]:
        f = l.split(",")[0].strip()
        if f.isdigit(): tics.add(int(f))
        else: bad += 1
    if not tics: return set(), "no integer TIC rows"
    if bad: return set(), f"{bad} non-integer rows"
    return tics, None

def save(d, name, raw, url, status, required, manifest):
    if raw: open(os.path.join(d, name), "wb").write(raw)
    manifest.append(dict(file=name if raw else None, url=url, http_status=status, sha256=sha(raw) if raw else None, bytes=len(raw), required=required))

def snapshot(a):
    if os.path.exists(a.dir): raise SystemExit(f"refused: {a.dir} exists")
    os.makedirs(a.dir); t = datetime.datetime.now(UTC).strftime(ISO); man = []
    st, raw = fetch(ORBIT_URL); save(a.dir, "TESS_orbit_times.csv", raw, ORBIT_URL, st, True, man)
    for k in range(1, MAX_VERSION + 1):
        url = LIST_URL.format(n=a.sector, k=k); st, raw = fetch(url); save(a.dir, f"all_targets_S{a.sector}_v{k}.csv", raw, url, st, True, man)
    st, raw = fetch(DDT_URL); save(a.dir, "DDT_list.html", raw, DDT_URL, st, False, man)
    for row in ddt_rows(raw.decode("utf-8", "replace")):
        if row["ctl"]:
            url = DDT_BASE + row["ctl"]; st2, raw2 = fetch(url); save(a.dir, "ctl_" + os.path.basename(row["ctl"]), raw2, url, st2, False, man)
    json.dump(dict(record="target_list_snapshot", version="2.0", sector=a.sector, tics=[int(x) for x in a.tics.split(",")], snapshot_utc=t, files=man),
              open(os.path.join(a.dir, "snapshot.json"), "w"), indent=1)
    des = derive(a.dir); json.dump(des, open(os.path.join(a.dir, "designation.json"), "w"), indent=1)
    print(des["status"], des.get("reasons", ""), {k: v["designation"] for k, v in des["per_tic"].items()})

def derive(d):
    snap = json.load(open(os.path.join(d, "snapshot.json"))); n = int(snap["sector"]); reasons = []; files = {}
    if snap.get("record") != "target_list_snapshot" or snap.get("version") != "2.0": raise ValueError("not a v2 target_list_snapshot")
    for m in snap["files"]:
        if m["file"] is None: continue
        raw = open(os.path.join(d, m["file"]), "rb").read()
        if sha(raw) != m["sha256"]: raise ValueError(f"{m['file']} does not match its recorded SHA-256")
        files[m["file"]] = raw
    byurl = {m["url"]: m for m in snap["files"]}
    out = dict(record="target_list_designation", version="2.0", sector=n, snapshot_utc=snap["snapshot_utc"],
               snapshot_sha256=sha(open(os.path.join(d, "snapshot.json"), "rb").read()))
    t = datetime.datetime.strptime(snap["snapshot_utc"], ISO).replace(tzinfo=UTC)
    om = byurl.get(ORBIT_URL); end = None
    if not om or om["http_status"] != 200 or om["file"] != "TESS_orbit_times.csv": reasons.append("orbit table not retrieved (HTTP %s%s)" % ((om or {}).get("http_status"), ", empty body" if om and om["http_status"] == 200 else ""))
    else:
        text = files["TESS_orbit_times.csv"].decode("utf-8", "replace"); lines = [l for l in text.splitlines() if l.strip() and not l.startswith("#")]
        if not lines or lines[0].strip() != ORBIT_HEADER: reasons.append("orbit table header is not the expected four columns")
        else:
            ends, nxt = [], False
            for r in csv.DictReader(io.StringIO("\n".join(lines))):
                s = str(r.get("Sector", "")).strip()
                if s.isdigit() and int(s) == n:
                    try: ends.append(datetime.datetime.strptime(r["End of Orbit"].strip(), "%Y-%m-%d %H:%M:%S").replace(tzinfo=UTC))
                    except (ValueError, AttributeError): reasons.append("malformed End of Orbit in the orbit table")
                if s.isdigit() and int(s) == n + 1: nxt = True
            if not ends: reasons.append(f"orbit table has no row for sector {n}")
            elif not nxt: reasons.append(f"orbit table has no row for sector {n + 1}, so the end of sector {n} is not final")
            else: end = max(ends)
    if end is not None and t < end: reasons.append("snapshot made before the sector end")
    lists, n200, http_bad = {}, 0, False
    for k in range(1, MAX_VERSION + 1):
        url = LIST_URL.format(n=n, k=k); m = byurl.get(url)
        if m is None: reasons.append(f"target-list version {k} not probed"); http_bad = True; continue
        if m["http_status"] == 404: continue
        if m["http_status"] != 200: reasons.append(f"target-list version {k}: HTTP {m['http_status']} (not 200 or 404)"); http_bad = True; continue
        n200 += 1
        if m["file"] is None: reasons.append(f"target-list version {k} malformed: HTTP 200 with an empty body"); continue
        tics, err = parse_target_list(files[m["file"]])
        if err: reasons.append(f"target-list version {k} malformed: {err}"); continue
        lists[m["file"]] = tics
    if n200 == 0 and not http_bad: reasons.append(f"no 2-min target list published for sector {n} (v1-v{MAX_VERSION} all 404)")
    if end is not None: out["sector_end_utc"] = end.strftime("%Y-%m-%dT%H:%M:%SZ")
    if reasons:
        out.update(status="PENDING", reasons=reasons, per_tic={str(x): dict(designation="PENDING") for x in snap["tics"]}); return out
    out.update(status="DESIGNATED", n_valid_target_lists=len(lists), max_version_probed=MAX_VERSION,
               spoc_cutoff_utc=(end + datetime.timedelta(days=120)).strftime("%Y-%m-%dT%H:%M:%SZ"),
               unavailable_cutoff_utc=(end + datetime.timedelta(days=365)).strftime("%Y-%m-%dT%H:%M:%SZ"),
               ddt_context=dict(files_saved=sum(1 for f in files if f.startswith("ctl_")), note="context only; never affects the designation"), per_tic={})
    for x in snap["tics"]:
        inl = sorted(f for f, s in lists.items() if x in s)
        out["per_tic"][str(x)] = dict(designation="SPOC" if inl else "QLP", in_target_lists=inl)
    return out

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); sp = ap.add_subparsers(dest="cmd", required=True)
    p = sp.add_parser("snapshot"); p.add_argument("--sector", type=int, required=True); p.add_argument("--tics", required=True); p.add_argument("--dir", required=True)
    p = sp.add_parser("derive"); p.add_argument("--dir", required=True)
    a = ap.parse_args()
    if a.cmd == "snapshot": snapshot(a)
    else: print(json.dumps(derive(a.dir), indent=1))
