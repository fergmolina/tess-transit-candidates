"""Two-step Zenodo new version (2026-10-20; replaces the one-shot zenodo_newversion.py for releases that need an inspection point).
  draft:   python -I zenodo_newversion_staged.py draft RECORD_ID VERSION DATE "note appended to the description" file1 [file2 ...]
           (note = "REPLACE:path/to/description.html" replaces the whole description instead of appending)
           -> creates the new-version draft, replaces its files, sets version/date/description, prints the draft id, files and metadata.
  publish: python -I zenodo_newversion_staged.py publish DRAFT_ID   -> publishes the draft and prints the DOI.
Token from ~/.zenodo_token or $ZENODO_TOKEN (never printed)."""
import os, sys, json, requests
tok = os.environ.get("ZENODO_TOKEN") or open(os.path.expanduser("~/.zenodo_token")).read().strip(); H = {"Authorization": f"Bearer {tok}"}; BASE = "https://zenodo.org/api"
if sys.argv[1] == "draft":
    rid, ver, date, note, files = int(sys.argv[2]), sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6:]
    r = requests.post(f"{BASE}/deposit/depositions/{rid}/actions/newversion", headers=H)
    if r.status_code in (401, 403): sys.exit(f"AUTH FAILED ({r.status_code}): token rejected; nothing was created")
    r.raise_for_status(); d = requests.get(r.json()["links"]["latest_draft"], headers=H).json(); did = d["id"]
    for f in d.get("files", []): requests.delete(f"{BASE}/deposit/depositions/{did}/files/{f['id']}", headers=H).raise_for_status()
    for f in files:
        with open(f, "rb") as fh: u = requests.put(f"{d['links']['bucket']}/{os.path.basename(f)}", data=fh, headers=H); u.raise_for_status()
    md = d["metadata"]; md["version"] = ver; md["publication_date"] = date; md["description"] = open(note[8:]).read().strip() if note.startswith("REPLACE:") else md["description"] + " " + note   # 2026-10-21: "REPLACE:<file>" replaces the whole description (used when the old text carries a withdrawn claim)
    for k in ("doi", "prereserve_doi"): md.pop(k, None)
    requests.put(f"{BASE}/deposit/depositions/{did}", headers=H, json={"metadata": md}).raise_for_status()
    d = requests.get(f"{BASE}/deposit/depositions/{did}", headers=H).json()
    print("DRAFT", did, "state", d.get("state"), "submitted", d.get("submitted"))
    print("FILES", [(f["filename"], f["filesize"], f["checksum"]) for f in d.get("files", [])])
    print("META", json.dumps({k: d["metadata"].get(k) for k in ("title", "version", "publication_date", "upload_type")}))
    print("DESC_TAIL", d["metadata"]["description"][-700:])
elif sys.argv[1] == "publish":
    did = int(sys.argv[2]); r = requests.post(f"{BASE}/deposit/depositions/{did}/actions/publish", headers=H); r.raise_for_status(); pub = r.json()
    print("PUBLISHED", pub.get("doi"), pub["links"].get("record_html") or pub["links"].get("html"))
