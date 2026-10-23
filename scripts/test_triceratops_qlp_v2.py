"""Guard tests for triceratops_qlp_v2.py: refusals happen before any file access (no FITS opened, no network)."""
import sys, os, subprocess, builtins
sys.path.insert(0, "/Users/fernando/Desktop/NASA/scripts"); import triceratops_qlp_v2 as T
ok = 0; fail = 0
def expect_refusal(tic, secs, label):
    global ok, fail
    opened = []; real = builtins.open
    builtins.open = lambda *a, **k: (opened.append(a[0]), real(*a, **k))[1]
    try: T.guard(tic, secs); r = "no refusal"
    except SystemExit as e: r = str(e)
    finally: builtins.open = real
    good = r.startswith("refused") and not opened; ok += good; fail += (not good); print("PASS" if good else "FAIL", label, "|", r, "| files opened:", opened)
for t in sorted(T.PROTECTED): expect_refusal(t, [50], f"protected TIC {t}")
expect_refusal(13450993, [85, 106], "sector 106"); expect_refusal(13450993, [121], "sector 121"); expect_refusal(240488148, [56, 200], "sector 200")
try: T.guard(13450993, [18, 58, 85, 86]); print("PASS in-sample allowed"); ok += 1
except SystemExit as e: print("FAIL in-sample refused", e); fail += 1
r = subprocess.run([sys.executable, "-I", "/Users/fernando/Desktop/NASA/scripts/triceratops_qlp_v2.py", "13450993"], capture_output=True, text=True)
good = r.returncode != 0 and "--sectors" in r.stderr; ok += good; fail += (not good); print("PASS" if good else "FAIL", "--sectors required")
# 2026-10-22 (round-5 re-check C1/C4): output directory join and QLP header refusal on synthetic files (no real data read)
import tempfile, numpy as np
from astropy.io import fits
tmp = tempfile.mkdtemp()
d = T.out_dir(13450993, os.path.join(tmp, "out")); good = d.is_dir() and str(d / "triceratops_v2.json") == os.path.join(tmp, "out", "triceratops_v2.json")
ok += good; fail += (not good); print("PASS" if good else "FAIL", "--out directory created and joined")
def synth(tic_hdr, sec_hdr, tic, sec):
    h0 = fits.PrimaryHDU(); h0.header["TICID"] = tic_hdr; h0.header["SECTOR"] = sec_hdr
    t = fits.BinTableHDU.from_columns([fits.Column(name="TIME", format="D", array=np.arange(3.0))])
    fits.HDUList([h0, t]).writeto(os.path.join(tmp, os.path.basename(T.qlp_path(tic, sec))), overwrite=True)
for label, th, sh in (("wrong TICID", 999, 58), ("wrong SECTOR", 13450993, 59)):
    synth(th, sh, 13450993, 58)
    try: T.load_qlp(13450993, 58, qd=tmp); r = "no refusal"
    except SystemExit as e: r = str(e)
    good = r.startswith("header mismatch"); ok += good; fail += (not good); print("PASS" if good else "FAIL", "header refusal:", label, "|", r[-60:])
synth(13450993, 58, 13450993, 58)
try: T.load_qlp(13450993, 58, qd=tmp); good = True
except SystemExit: good = False
ok += good; fail += (not good); print("PASS" if good else "FAIL", "matching synthetic header accepted")
try: T.load_qlp(13450993, 57, qd=tmp); good = False
except SystemExit as e: good = str(e).startswith("missing")
ok += good; fail += (not good); print("PASS" if good else "FAIL", "missing exact path refused (no globbing)")
print(f"{ok} pass, {fail} fail"); sys.exit(1 if fail else 0)
