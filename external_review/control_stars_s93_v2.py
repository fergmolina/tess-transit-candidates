"""Shape-based control for the S93 epoch-118 window: for every local S93 QLP star covering the window, fit
quadratic baseline x 4-h box at the predicted time (ON) and at +-0.35 d (OFF1, OFF2) using SAP_FLUX with all flags;
report ON depth, OFF depths and the excess ON - mean(OFF). A field-wide systematic would give ON excesses in many stars."""
import glob, numpy as np, pandas as pd, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from astropy.io import fits
tc=3830.3448; dur=4.0/24
def boxfit(t,f,tcen):
    w=np.isfinite(t)&np.isfinite(f)&(np.abs(t-tcen)<0.5)
    if w.sum()<150: return np.nan,np.nan,0
    x=t[w]-tcen; y=f[w]/np.nanmedian(f[w]); box=(np.abs(x)<dur/2).astype(float)
    if box.sum()<20 or (box==0).sum()<60: return np.nan,np.nan,0
    A=np.vstack([np.ones_like(x),x,x**2,x**3,-box]).T; c,res,_,_=np.linalg.lstsq(A,y,rcond=None)
    r=y-A@c; sig=np.std(r); cov=np.linalg.inv(A.T@A)*sig**2
    return float(c[4]), float(np.sqrt(cov[4,4])), int(box.sum())
rows=[]; curves={}
for fp in sorted(glob.glob('/Users/fernando/Desktop/NASA/data/qlp/hlsp_qlp_tess_ffi_s0093-*')):
    try:
        with fits.open(fp,memmap=False) as h:
            cam,ccd=h[0].header['CAMERA'],h[0].header['CCD']; tic=h[0].header['TICID']; tmag=h[0].header.get('TESSMAG'); d=h[1].data
            t=np.array(d['TIME'],float); f=np.array(d['SAP_FLUX'],float)
    except Exception: continue
    on=boxfit(t,f,tc); 
    if on[2]==0: continue
    offs=[boxfit(t,f,tc+s) for s in (-0.35,0.35,0.6)]
    offd=[o[0] for o in offs if np.isfinite(o[0])]
    rows.append(dict(tic=int(tic),cam=int(cam),ccd=int(ccd),tmag=tmag,on_ppm=on[0]*1e6,on_err=on[1]*1e6,on_sig=on[0]/on[1],off_mean_ppm=np.mean(offd)*1e6 if offd else np.nan,off_max_abs_ppm=np.max(np.abs(offd))*1e6 if offd else np.nan,n_in=on[2]))
    if int(tic)==89247735 or (on[0]/on[1]>6 and cam==1 and ccd==2): curves[int(tic)]=(t,f)
df=pd.DataFrame(rows); df.to_csv('/Users/fernando/Desktop/NASA/results/external_review/control_stars_s93_v2.csv',index=False)
tg=df[df.tic==89247735].iloc[0]; same=df[(df.cam==1)&(df.ccd==2)&(df.tic!=89247735)]
print(f"target: ON {tg.on_ppm:.0f}+-{tg.on_err:.0f} ppm ({tg.on_sig:.1f} sigma), OFF mean {tg.off_mean_ppm:.0f}, OFF max|.| {tg.off_max_abs_ppm:.0f}")
print(f"same-CCD controls N={len(same)}: ON depth median {same.on_ppm.median():.0f}, robust sd {1.4826*np.median(np.abs(same.on_ppm-same.on_ppm.median())):.0f} ppm; n(ON>5000 ppm & >5sig)={np.sum((same.on_ppm>5000)&(same.on_sig>5))}; n(ON>8000 & >5sig & OFFmax<ON/2)={np.sum((same.on_ppm>8000)&(same.on_sig>5)&(same.off_max_abs_ppm<same.on_ppm/2))}")
print(f"all S93 controls N={len(df)-1}: n(ON>8000 & >5sig & OFFmax<ON/2)={np.sum((df.on_ppm>8000)&(df.on_sig>5)&(df.off_max_abs_ppm<df.on_ppm/2)&(df.tic!=89247735))}")
print(same.sort_values('on_sig',ascending=False).head(10)[['tic','tmag','on_ppm','on_err','on_sig','off_mean_ppm','off_max_abs_ppm']].round(0).to_string(index=False))
# plot the target and the strongest same-CCD controls
keys=[89247735]+[k for k in curves if k!=89247735][:7]
fig,ax=plt.subplots(len(keys),1,figsize=(9,2.2*len(keys)),sharex=True)
for a,k in zip(np.atleast_1d(ax),keys):
    t,f=curves[k]; w=np.abs(t-tc)<0.6; a.plot((t[w]-tc)*24,f[w]/np.nanmedian(f[w]),'k.',ms=2); a.axvspan(-2,2,color='orange',alpha=0.2); a.set_ylabel(f'TIC {k}',fontsize=8)
np.atleast_1d(ax)[-1].set_xlabel('hours from predicted epoch-118 mid-transit (S93 raw SAP_FLUX, all flags)'); plt.tight_layout(); plt.savefig('/Users/fernando/Desktop/NASA/results/external_review/plots/control_stars_s93.png',dpi=90)
