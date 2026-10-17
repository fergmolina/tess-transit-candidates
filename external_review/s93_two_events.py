"""Same-aperture, own-photometry comparison of the two S93 events (epochs 118 and 119) of TIC 89247735 from the cached
TESScut cutout: 1.5-px aperture, per-cadence annulus background, local quadratic baseline, batman shape with free depth scale."""
import sys, json, warnings; warnings.filterwarnings("ignore"); sys.path.insert(0,"/Users/fernando/Desktop/NASA/scripts")
import os; os.environ["TSEARCH_SOURCE"]="qlp"
import numpy as np, lightkurve as lk, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from scipy.optimize import least_squares
from vet import transit_model
P0=18.32312630839195; T00=4196.80731906277; dur=4.0/24; rprs,ars,b=0.09961737438108847,30.915970707905185,0.43768515989976475
tpf=lk.read("/Users/fernando/Desktop/NASA/data/lk_cache/tesscut/tess-s0093-1-2_275.223692_-45.561167_11x11_astrocut.fits")
t=tpf.time.value; cube=tpf.flux.value.astype(float); ok=np.isfinite(cube).all(axis=(1,2)); t,cube=t[ok],cube[ok]
ny,nx=cube.shape[1:]; yy,xx=np.mgrid[0:ny,0:nx]
px=tpf.wcs.all_world2pix([[275.22345-0.00019,-45.56164-0.00028]],0)[0]   # PM-corrected (2025.45) target position
res={}
fig,ax=plt.subplots(1,2,figsize=(12,4),sharey=True)
for k,(rap) in enumerate((1.5,2.5)):
    d=np.hypot(xx-px[0],yy-px[1]); ap=d<=rap; bkg=(d>4)&(d<5.5)
    flux=cube[:,ap].sum(axis=1)-np.median(cube[:,bkg],axis=1)*ap.sum()
    row={}
    for ep in (118,119):
        tc0=T00+(ep-138)*P0; w=np.abs(t-tc0)<0.5; tt,ff=t[w],flux[w]/np.nanmedian(flux[w]); x=tt-tc0
        def model(p): return np.polyval(p[2:],x)*transit_model([p[0],rprs*np.sqrt(max(p[1],1e-6)),ars,b],tt,P0,exp_time=200/86400)
        r=least_squares(lambda p: ff-model(p),[tc0,1.0,0,0,1.0]); sig=np.std(ff-model(r.x)); cov=np.linalg.inv(r.jac.T@r.jac)*sig**2; err=np.sqrt(np.diag(cov))
        base=np.polyval(r.x[2:],x); intr=np.abs(tt-r.x[0])<0.8*dur/2; dbox=1-np.mean((ff/base)[intr]); dbe=sig/np.sqrt(intr.sum())
        row[ep]=dict(tc=float(r.x[0]),tc_err_min=float(err[0]*1440),oc_min=float((r.x[0]-tc0)*1440),depth_scale=float(r.x[1]),depth_scale_err=float(err[1]),box_depth_ppm=float(dbox*1e6),box_err_ppm=float(dbe*1e6),rms_ppm=float(sig*1e6),n=int(len(tt)))
        print(f"r={rap} px epoch {ep}: tc O-C {row[ep]['oc_min']:+.1f}+-{row[ep]['tc_err_min']:.1f} min; depth scale {r.x[1]:.3f}+-{err[1]:.3f}; box depth {dbox*1e6:.0f}+-{dbe*1e6:.0f} ppm (rms {sig*1e6:.0f})")
        if k==0: ax[0 if ep==118 else 1].plot(x*24,ff/base,'.',ms=3,color='0.4'); ax[0 if ep==118 else 1].plot(np.sort(x)*24,(model(r.x)/base)[np.argsort(x)],'r-'); ax[0 if ep==118 else 1].set_title(f'S93 epoch {ep} (own 1.5-px photometry)'); ax[0 if ep==118 else 1].set_xlabel('hours from predicted')
    s=(row[118]['depth_scale']-row[119]['depth_scale'])/np.hypot(row[118]['depth_scale_err'],row[119]['depth_scale_err'])
    print(f"   r={rap}: depth(118)/depth(119) = {row[118]['depth_scale']/row[119]['depth_scale']:.3f}; difference {s:+.1f} sigma")
    res[rap]=dict(events=row,diff_sigma=float(s))
plt.tight_layout(); plt.savefig('/Users/fernando/Desktop/NASA/results/external_review/plots/s93_two_events.png',dpi=100)
json.dump(res,open('/Users/fernando/Desktop/NASA/results/external_review/s93_two_events.json','w'),indent=1)
