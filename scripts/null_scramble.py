"""Season/sector-scrambled null for the all-sky periodic search (Kepler DR25-style reliability null, replacing the inverted-LC null that
cannot reproduce one-signed FFI artefacts). Each sector of a star is shifted in time by a cumulative random offset (3-25 d per step, so
sector order and within-sector structure, incl. orbit-cadence scattered-light features, are preserved while cross-sector phase coherence of
any real periodic signal is destroyed). The identical search_pipeline.process() then runs; results go to results/null_scramble_allsky/.
Usage: TSEARCH_LC_DIR=data/qlp_allsky python -I null_scramble.py --n 300 --workers 3 --seed 7"""
import os, sys, argparse, json, numpy as np, pandas as pd
ROOT = "/Users/fernando/Desktop/NASA"; os.environ["TSEARCH_SOURCE"] = "qlp"; os.environ.setdefault("TSEARCH_LC_DIR", f"{ROOT}/data/qlp_allsky")
os.environ["TSEARCH_OUT"] = f"{ROOT}/results/null_scramble_allsky"; os.makedirs(os.environ["TSEARCH_OUT"], exist_ok=True)
sys.path.insert(0, f"{ROOT}/scripts"); import search_pipeline as sp
_orig_load = sp.load_lc; SEED = 7
def load_shifted(path):
    t, f, fe, m = _orig_load(path)
    rng = np.random.default_rng(SEED * 1000003 + int(m["tic"]) % 1000003)
    secs = sorted(int(s) for s in sp.sector_files(int(m["tic"])) and [int(os.path.basename(p).split("_s")[1][:4]) for p in sp.sector_files(int(m["tic"]))])
    shifts = np.cumsum(rng.uniform(3, 25, len(secs))); sh = dict(zip(secs, shifts))
    return t + sh.get(int(m["sector"]), 0.0), f, fe, m
def _init(seed):
    global SEED; SEED = seed; sp.load_lc = load_shifted
def run(tic): return sp.process(tic)
if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--n", type=int, default=300); ap.add_argument("--workers", type=int, default=3); ap.add_argument("--seed", type=int, default=7); a = ap.parse_args()
    top = pd.read_csv(f"{ROOT}/results/ranked_top_peak_allsky.csv", low_memory=False); pool = top[top.known_src.isna()].tic.astype(int).tolist()
    rng = np.random.default_rng(a.seed); tics = [int(x) for x in rng.choice(pool, a.n, replace=False)]
    done = {int(f[:-5]) for f in os.listdir(os.environ["TSEARCH_OUT"]) if f[0].isdigit()}; tics = [t for t in tics if t not in done]
    json.dump(dict(seed=a.seed, n=a.n), open(f"{os.environ['TSEARCH_OUT']}/null_config.json", "w"))
    from concurrent.futures import ProcessPoolExecutor
    with ProcessPoolExecutor(a.workers, initializer=_init, initargs=(a.seed,)) as ex:
        for i, r in enumerate(ex.map(run, tics)): print(i + 1, r.get("tic"), r.get("sde"), r.get("error", "")[:80], flush=True)
