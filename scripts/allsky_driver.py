"""All-sky QLP driver: download light curves by direct MAST URL (deterministic from TIC and sector) in batches, and run the stitched
periodic search (search_pipeline.py, TSEARCH_SOURCE=qlp) on each batch while the next batch downloads. Resumable: files already on disk
and stars with a result JSON are skipped; 404s are recorded in the manifest and not retried.
Layout: data/qlp_allsky/ (flat, QLP filenames), results/search_allsky/, catalogs/allsky_manifest.csv (tic, sector, status).
Usage: python -I allsky_driver.py [--batch 2000] [--dl-parallel 16] [--workers 13] [--first-tics file] [--max-batches N]"""
import sys, os, json, time, argparse, subprocess, glob
import numpy as np, pandas as pd
ROOT = "/Users/fernando/Desktop/NASA"; LC = f"{ROOT}/data/qlp_allsky"; OUT = f"{ROOT}/results/search_allsky"; MAN = f"{ROOT}/catalogs/allsky_manifest.csv"
os.makedirs(LC, exist_ok=True); os.makedirs(OUT, exist_ok=True)

def url(tic, sec):
    t = f"{tic:016d}"; return f"https://mast.stsci.edu/api/v0.1/Download/file/?uri=mast:HLSP/qlp/s{sec:04d}/{t[0:4]}/{t[4:8]}/{t[8:12]}/{t[12:16]}/hlsp_qlp_tess_ffi_s{sec:04d}-{t}_tess_v01_llc.fits"
def fname(tic, sec): return f"{LC}/hlsp_qlp_tess_ffi_s{sec:04d}-{tic:016d}_tess_v01_llc.fits"

def download(pairs, parallel):
    """pairs: list of (tic, sec). Uses curl via xargs; returns dict (tic,sec)->status."""
    todo = [(t, s) for t, s in pairs if not os.path.exists(fname(t, s))]
    if not todo: return {}
    lst = f"{LC}/.dl_list_{os.getpid()}.txt"
    with open(lst, "w") as fh:
        for t, s in todo: fh.write(f"{url(t, s)}\n{fname(t, s)}\n")
    # xargs feeds url+output pairs; curl -f fails on 404, --retry handles transient errors
    cmd = f"xargs -n 2 -P {parallel} sh -c 'curl -sf --retry 3 --retry-delay 5 --max-time 120 -o \"$1\" \"$0\" || rm -f \"$1\"' < {lst}"
    subprocess.run(cmd, shell=True, cwd=LC)
    os.remove(lst)
    return {(t, s): ("ok" if os.path.exists(fname(t, s)) and os.path.getsize(fname(t, s)) > 10000 else "missing") for t, s in todo}

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--batch", type=int, default=2000); ap.add_argument("--dl-parallel", type=int, default=16); ap.add_argument("--workers", type=int, default=13)
    ap.add_argument("--first-tics", default=""); ap.add_argument("--max-batches", type=int, default=0); a = ap.parse_args()
    tg = pd.read_csv(f"{ROOT}/catalogs/allsky_targets.csv"); t2s = json.load(open(f"{ROOT}/catalogs/allsky_tic2sectors.json"))
    tics = tg["ID"].astype(int).tolist()
    if a.first_tics:   # put these stars first (e.g. the Pool B stars for a before/after comparison)
        first = [int(x) for x in open(a.first_tics).read().split()]; fs = set(first); tics = [t for t in first if t in set(tics)] + [t for t in tics if t not in fs]
    done = {int(os.path.basename(f)[:-5]) for f in glob.glob(f"{OUT}/*.json")}
    man = pd.read_csv(MAN) if os.path.exists(MAN) else pd.DataFrame(columns=["tic", "sector", "status"])
    known_missing = set(zip(man[man.status == "missing"].tic.astype(int), man[man.status == "missing"].sector.astype(int)))
    pending = [t for t in tics if t not in done]
    print(f"targets {len(tics)}, done {len(done)}, pending {len(pending)}, batch {a.batch}", flush=True)
    batches = [pending[i:i + a.batch] for i in range(0, len(pending), a.batch)]
    if a.max_batches: batches = batches[:a.max_batches]
    def pairs_for(b): return [(t, s) for t in b for s in t2s.get(str(t), []) if (t, s) not in known_missing]
    import threading
    # prefetch batch 0
    status = download(pairs_for(batches[0]), a.dl_parallel) if batches else {}
    for i, b in enumerate(batches):
        t0 = time.time()
        # start downloading the next batch in a thread while searching this one
        nxt = {}; th = None
        if i + 1 < len(batches):
            th = threading.Thread(target=lambda: nxt.update(download(pairs_for(batches[i + 1]), a.dl_parallel))); th.start()
        if status:
            man = pd.concat([man, pd.DataFrame([dict(tic=t, sector=s, status=v) for (t, s), v in status.items()])]); man.to_csv(MAN, index=False)
        tl = f"{LC}/.batch_{i}.txt"; open(tl, "w").write(" ".join(map(str, b)))
        env = dict(os.environ, TSEARCH_SOURCE="qlp", TSEARCH_LC_DIR=LC, TSEARCH_OUT=OUT)
        subprocess.run(f"{ROOT}/.venv/bin/python -I {ROOT}/scripts/search_pipeline.py --workers {a.workers} --tics $(tr ' ' ',' < {tl})", shell=True, env=env, stdout=open(f"{ROOT}/logs/allsky_search_batch{i}.log", "w"), stderr=subprocess.STDOUT)
        # second pass on the same files: single-transit search (keeps the ramp cadences; SAP flux + local baseline)
        env2 = dict(os.environ, TSEARCH_LC_DIR=LC)
        subprocess.run(f"{ROOT}/.venv/bin/python -I {ROOT}/scripts/single_transit_search.py --workers {a.workers} --tics-file {tl} --out {ROOT}/results/single_allsky", shell=True, env=env2, stdout=open(f"{ROOT}/logs/allsky_single_batch{i}.log", "w"), stderr=subprocess.STDOUT)
        os.remove(tl)
        n_json = len(glob.glob(f"{OUT}/*.json")); n_files = len(glob.glob(f"{LC}/*.fits"))
        print(f"batch {i + 1}/{len(batches)}: {len(b)} stars searched in {(time.time() - t0) / 60:.1f} min; results {n_json}; files on disk {n_files}; missing so far {int((man.status == 'missing').sum())}", flush=True)
        if th: th.join()
        status = nxt
    if status:
        man = pd.concat([man, pd.DataFrame([dict(tic=t, sector=s, status=v) for (t, s), v in status.items()])]); man.to_csv(MAN, index=False)
    print("all batches done", flush=True)
