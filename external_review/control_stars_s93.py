"""Control test for the QLP-flagged fourth transit of TIC 89247735 (S93, BTJD 3830.345): measure the in-window SAP_FLUX
depth (all quality flags, local linear baseline from +-0.5 d excluding the +-2.5 h window) for every local S93 QLP star on the
same camera/CCD and on other CCDs. If the field dips, the event is a systematic."""
import glob, numpy as np, json
from astropy.io import fits
tc=3830.3448; dur=4.0/24
rows=[]
for fp in sorted(glob.glob('/Users/fernando/Desktop/NASA/data/qlp/hlsp_qlp_tess_ffi_s0093-*')):
    try:
        with fits.open(fp,memmap=False) as h:
            cam,ccd=h[0].header['CAMERA'],h[0].header['CCD']; tic=h[0].header['TICID']; tmag=h[0].header.get('TESSMAG'); d=h[1].data
            t=np.array(d['TIME'],float); f=np.array(d['SAP_FLUX'],float); q=np.array(d['QUALITY'],int)
    except Exception: continue
    w=np.isfinite(t)&np.isfinite(f)&(np.abs(t-tc)<0.5)
    intr=w&(np.abs(t-tc)<dur/2*0.8); oot=w&(np.abs(t-tc)>dur/2*1.3)
    if intr.sum()<20 or oot.sum()<60: continue
    c=np.polyfit(t[oot]-tc,f[oot],2); base=np.polyval(c,t-tc)
    r=f/base; depth=1-np.mean(r[intr]); sig=np.std(r[oot]); err=sig/np.sqrt(intr.sum())
    rows.append(dict(tic=int(tic),cam=int(cam),ccd=int(ccd),tmag=float(tmag) if tmag else None,depth_ppm=float(depth*1e6),err_ppm=float(err*1e6),rms_ppm=float(sig*1e6),n_in=int(intr.sum()),flagged_frac=float(np.mean(q[intr]!=0))))
import pandas as pd
df=pd.DataFrame(rows); df.to_csv('/Users/fernando/Desktop/NASA/results/external_review/control_stars_s93.csv',index=False)
print('stars with coverage of the window:',len(df)); 
for (cam,ccd),g in df.groupby(['cam','ccd']):
    print(f"cam{cam} ccd{ccd}: N={len(g)} median depth {g.depth_ppm.median():.0f} ppm, 16-84% [{g.depth_ppm.quantile(.16):.0f},{g.depth_ppm.quantile(.84):.0f}], max {g.depth_ppm.max():.0f}, n(|depth|>5000 ppm)={np.sum(np.abs(g.depth_ppm)>5000)}, n(>5sigma dips)={np.sum(g.depth_ppm/g.err_ppm>5)}")
tg=df[df.tic==89247735]; print('target:',tg.to_dict('records'))
same=df[(df.cam==tg.cam.iloc[0])&(df.ccd==tg.ccd.iloc[0])&(df.tic!=89247735)]
print(f"same CCD controls: N={len(same)}; target depth is {(tg.depth_ppm.iloc[0]-same.depth_ppm.median())/same.depth_ppm.std():.1f} sd above the control distribution (control sd {same.depth_ppm.std():.0f} ppm)")
print(same.sort_values('depth_ppm',ascending=False).head(8)[['tic','tmag','depth_ppm','err_ppm','rms_ppm','flagged_frac']].to_string(index=False))
