"""Generic TRICERATOPS (Giacalone+2021) runner for a QLP candidate, run in .venv_tri (numpy<2). Adapted from the external review's
triceratops_review.py: 2.5-px circular aperture around the target in FFI pixel coordinates from a 15x15 TESScut cutout, folded QLP DET_FLUX
(masked 0.7-d biweight, 10-min bins) at the vet.py ephemeris. No contrast curve. Usage: python -I triceratops_qlp.py TIC [sector sector ...]
Output: results/vet_allsky/TIC/triceratops.json"""
import sys, os, json, glob, warnings; warnings.filterwarnings("ignore")
import numpy as np
from astropy.io import fits; from wotan import flatten, transit_mask
from triceratops import triceratops as tr
tic = int(sys.argv[1]); OUT = f"/Users/fernando/Desktop/NASA/results/vet_allsky/{tic}/"; QD = "/Users/fernando/Desktop/NASA/data/qlp_allsky/"
rep = json.load(open(OUT + "report.json")); b = rep["bls_refine"]; P, T0, dur_h = b["period"], b["T0"], b["duration_h"]; ra, dec = rep["meta"]["ra"], rep["meta"]["dec"]
secs = [int(x) for x in sys.argv[2:]] if len(sys.argv) > 2 else sorted({int(os.path.basename(f).split("_s")[1][:4]) for f in glob.glob(QD + f"*{tic:016d}*.fits")})[-3:]
dur = dur_h / 24
T,F=[],[]
for f in sorted(glob.glob(QD+f"*{tic:016d}*.fits")):
    d=fits.open(f)[1].data; t=np.asarray(d["TIME"],float); fl=np.asarray(d["DET_FLUX"] if "DET_FLUX" in d.columns.names else d["KSPSAP_FLUX"],float); q=np.asarray(d["QUALITY"],int); ok=np.isfinite(t)&np.isfinite(fl)&(q==0)&(fl>0); t,fl=t[ok],fl[ok]
    if len(t)<1000: continue
    fl=fl/np.nanmedian(fl); m=transit_mask(time=t,period=P,duration=2*dur,T0=T0); f2=flatten(t,fl,method="biweight",window_length=0.7,mask=m,break_tolerance=0.5); ok=np.isfinite(f2); T.append(t[ok]); F.append(f2[ok])
T=np.concatenate(T); F=np.concatenate(F); ph=((T-T0)/P+0.5)%1-0.5; sel=np.abs(ph*P*24)<6
tb=np.round(ph[sel]*P/(10/1440))*(10/1440); u=np.unique(tb); fb=np.array([np.mean(F[sel][tb==x]) for x in u]); eb=np.array([np.std(F[sel][tb==x])/np.sqrt(np.sum(tb==x)) for x in u])
depth=1-np.mean(fb[np.abs(u*24)<dur_h/4]); print("folded bins",len(u),"depth",depth*1e6,"ppm",flush=True)
aps=[]; use=[]
for s in secs:
    import lightkurve as lk
    try: tpf = lk.search_tesscut(f"TIC {tic}", sector=s).download(cutout_size=15, download_dir="/Users/fernando/Desktop/NASA/data/lk_cache")
    except Exception as e: print("tesscut fail", s, e, flush=True); continue
    h = fits.open(tpf.path); hd=h[1].header; c0=hd["1CRV4P"]; r0=hd["2CRV4P"]   # FFI column/row of the first cutout pixel
    from astropy.wcs import WCS; w=WCS(h[2].header); px=w.all_world2pix([[ra,dec]],0)[0]
    yy,xx=np.mgrid[0:15,0:15]; ap=np.hypot(xx-px[0],yy-px[1])<=2.5; cols=xx[ap]+c0; rows=yy[ap]+r0
    aps.append(np.array([[c,r] for c,r in zip(cols,rows)])); use.append(s); print("sector",s,"aperture pixels",ap.sum(),"origin",c0,r0,"target px",px,flush=True)
target=tr.target(ID=tic,sectors=np.array(use))
target.calc_depths(tdepth=depth,all_ap_pixels=aps)
print(target.stars.head(12).to_string(),flush=True)
target.stars.to_csv(OUT+"triceratops_stars.csv",index=False)
target.calc_probs(time=u,flux_0=fb,flux_err_0=float(np.median(eb)),P_orb=P,parallel=True,drop_scenario=[],verbose=1)
print("\nFPP =",target.FPP," NFPP =",target.NFPP,flush=True)
target.probs.to_csv(OUT+"triceratops_probs.csv",index=False)
json.dump(dict(tic=tic,FPP=float(target.FPP),NFPP=float(target.NFPP),depth_used=float(depth),sectors=use,note="2.5-px circular aperture from TESScut WCS; QLP DET_FLUX masked 0.7-d biweight fold; no contrast curve"),open(OUT+"triceratops.json","w"),indent=1)
