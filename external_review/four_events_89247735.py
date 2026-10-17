"""External review: time and measure all FOUR events of TIC 89247735 (including the QLP-flagged S93 epoch 118 event) using
raw QLP SAP_FLUX with a local polynomial baseline (handles the scattered-light ramp) and the team's batman shape; test the
3-event ephemeris prediction for epoch 118; 4-event linear ephemeris; odd/even with 4 events; same in TARS flux."""
import sys, json, warnings, glob; warnings.filterwarnings("ignore"); sys.path.insert(0,"/Users/fernando/Desktop/NASA/scripts")
import numpy as np; from astropy.io import fits; from scipy.optimize import least_squares
import os; os.environ["TSEARCH_SOURCE"]="qlp"
from vet import transit_model
P0=18.32312630839195; T00=4196.80731906277; dur=4.0/24; rprs,ars,b=0.09961737438108847,30.915970707905185,0.43768515989976475
def load_qlp(sec):
    fp=glob.glob(f'/Users/fernando/Desktop/NASA/data/qlp/*s{sec:04d}*89247735*')[0]; d=fits.open(fp)[1].data
    return np.array(d['TIME'],float),np.array(d['SAP_FLUX'],float),np.array(d['QUALITY'],int)
def load_tars(sec):
    fp=glob.glob(f'/Users/fernando/Desktop/NASA/results/external_review/data/hlsp/mastDownload/HLSP/hlsp_tars*s{sec:04d}*/*.fits')[0]; d=fits.open(fp)[1].data
    return np.array(d['TIME'],float),np.array(d['FLUX'],float),np.zeros(len(d),int)
events={79:66,118:93,119:93,138:104}
def fit_event(t,f,tc0,label,exp=200/86400,deg=2,win=0.5):
    w=np.isfinite(t)&np.isfinite(f)&(np.abs(t-tc0)<win); tt,ff=t[w],f[w]; ff=ff/np.nanmedian(ff)
    x=(tt-tc0)
    def model(p):
        tc,dep_scale=p[0],p[1]; poly=np.polyval(p[2:],x)
        m=transit_model([tc,rprs*np.sqrt(max(dep_scale,1e-6)),ars,b],tt,P0,exp_time=exp); return poly*m
    p0=[tc0,1.0]+[0]*deg+[1.0]
    r=least_squares(lambda p:(ff-model(p)),p0,x_scale=[0.001,0.1]+[0.01]*(deg+1))
    res=ff-model(r.x); sig=np.std(res); J=r.jac; cov=np.linalg.inv(J.T@J)*sig**2; err=np.sqrt(np.diag(cov))
    # depth = (rprs*sqrt(scale))^2 ~ scale*rprs^2 ; report box depth too
    intr=np.abs(tt-r.x[0])<dur/2*0.8; base=np.polyval(r.x[2:],x)
    dbox=1-np.mean((ff/base)[intr]); dbox_e=sig/np.sqrt(intr.sum())
    return dict(label=label,tc=float(r.x[0]),tc_err_min=float(err[0]*1440),depth_scale=float(r.x[1]),depth_scale_err=float(err[1]),model_depth_ppm=float(r.x[1]*rprs**2*1e6),
                box_depth_ppm=float(dbox*1e6),box_depth_err_ppm=float(dbox_e*1e6),n=int(len(tt)),rms_ppm=float(sig*1e6),oc_min=float((r.x[0]-tc0)*1440))
out={}
for src,loader,exp in (("QLP_SAP_allflags",load_qlp,200/86400),("TARS",load_tars,200/86400)):
    rows=[]
    for ep,sec in events.items():
        try: t,f,q=loader(sec)
        except Exception as e: print(src,sec,'no data',e); continue
        if src=="QLP_SAP_allflags" and sec==66: exp=600/86400   # S66 QLP cadence 10 min? check
        tc0=T00+(ep-138)*P0
        r=fit_event(t,f,tc0,f"{src} S{sec} e{ep}",exp=exp); rows.append(dict(epoch=ep,sector=sec,**r))
        print(f"{src:18s} S{sec} epoch {ep}: tc={r['tc']:.5f} +- {r['tc_err_min']:.1f} min (O-C vs frozen eph {r['oc_min']:+.1f} min); model depth {r['model_depth_ppm']:.0f} ppm (scale {r['depth_scale']:.3f}+-{r['depth_scale_err']:.3f}); box depth {r['box_depth_ppm']:.0f}+-{r['box_depth_err_ppm']:.0f}; rms {r['rms_ppm']:.0f}")
    # 4-event linear ephemeris
    e=np.array([x['epoch'] for x in rows],float); tc=np.array([x['tc'] for x in rows]); er=np.array([x['tc_err_min'] for x in rows])/1440
    A=np.vstack([np.ones_like(e),e-138]).T; W=np.diag(1/er**2); cov=np.linalg.inv(A.T@W@A); beta=cov@A.T@W@tc; res=tc-A@beta; chi2=float(np.sum(res**2/er**2))
    print(f"   4-event ephemeris: T0={beta[0]:.5f}+-{np.sqrt(cov[0,0])*1440:.1f} min, P={beta[1]:.6f}+-{np.sqrt(cov[1,1]):.6f} d, chi2={chi2:.2f}/2, residuals (min) {np.round(res*1440,1).tolist()}")
    # odd/even
    odd=[x for x in rows if x['epoch']%2==1]; even=[x for x in rows if x['epoch']%2==0]
    def wmean(xs,key,ekey):
        v=np.array([x[key] for x in xs]); s=np.array([x[ekey] for x in xs]); w=1/s**2; return float(np.sum(w*v)/np.sum(w)), float(1/np.sqrt(np.sum(w)))
    do=wmean(odd,'box_depth_ppm','box_depth_err_ppm'); de=wmean(even,'box_depth_ppm','box_depth_err_ppm')
    print(f"   odd (epochs {[x['epoch'] for x in odd]}) {do[0]:.0f}+-{do[1]:.0f} vs even ({[x['epoch'] for x in even]}) {de[0]:.0f}+-{de[1]:.0f} ppm -> {abs(do[0]-de[0])/np.hypot(do[1],de[1]):.1f} sigma")
    out[src]=dict(events=rows,ephemeris=dict(T0=float(beta[0]),T0_err_min=float(np.sqrt(cov[0,0])*1440),P=float(beta[1]),P_err=float(np.sqrt(cov[1,1])),chi2=chi2,residual_min=(res*1440).tolist()),odd=do,even=de)
json.dump(out,open('/Users/fernando/Desktop/NASA/results/external_review/four_events_89247735.json','w'),indent=1)
