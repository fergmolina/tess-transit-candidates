"""Fold the ASAS-SN v1 (legacy Sky Patrol) V-band light curve of TIC 89247735 on the frozen ephemeris and run a blind BLS."""
import numpy as np, pandas as pd, json, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from astropy.timeseries import BoxLeastSquares
P=18.32312630839195; T0=4196.80731906277+2457000; dur=4.0/24
d=pd.read_csv('/Users/fernando/Desktop/NASA/results/external_review/data/asassn/asassn_v1_lc.csv')
print(len(d),'epochs; cameras',d.camera.value_counts().to_dict(),'HJD range',d.hjd.min(),d.hjd.max(),'(',(d.hjd.max()-d.hjd.min())/365.25,'yr )')
d=d[(d.mag<99)&(d.mag_err<0.1)].copy()
# per-camera median subtraction
d['dmag']=d.mag-d.groupby('camera').mag.transform('median')
print('rms per camera (mag):',d.groupby('camera').dmag.std().round(4).to_dict())
# HJD vs BJD_TDB difference ~ 1 min, negligible against 4 h
ph=((d.hjd-T0)/P+0.5)%1-0.5; dt=ph*P
intr=np.abs(dt)<dur/2; oot=np.abs(dt)>dur
print('in-transit points:',intr.sum(),' out:',oot.sum())
if intr.sum()>0:
    din=d.dmag[intr].mean()-d.dmag[oot].mean(); e=d.dmag[oot].std()/np.sqrt(intr.sum()); print(f'in-out depth = {din*1e3:.1f} +- {e*1e3:.1f} mmag (expected ~ +11 mmag for a 1 % transit)')
    print('in-transit points:'); print(d[intr][['hjd','camera','mag','mag_err','dmag']].to_string())
# blind BLS 2-40 d on dmag
f=10**(-0.4*d.dmag.values); t=d.hjd.values
bls=BoxLeastSquares(t,f,dy=np.full_like(f,d.dmag.std()*0.92))
periods=np.exp(np.linspace(np.log(1.0),np.log(40),20000)); r=bls.power(periods,[2/24,4/24,6/24],objective='snr')
i=np.argmax(r.power); print(f'blind BLS top: P={r.period[i]:.4f} d depth={r.depth[i]*1e6:.0f} ppm snr={r.power[i]:.1f}; power at 18.323 d: {r.power[np.argmin(np.abs(r.period-18.3231))]:.1f}; median power {np.median(r.power):.1f}')
json.dump(dict(n=int(len(d)),n_in=int(intr.sum()),depth_mmag=float(din*1e3) if intr.sum() else None,err_mmag=float(e*1e3) if intr.sum() else None,hjd_min=float(d.hjd.min()),hjd_max=float(d.hjd.max())),open('/Users/fernando/Desktop/NASA/results/external_review/asassn_v1_fold_89247735.json','w'),indent=1)
plt.figure(figsize=(8,4)); plt.errorbar(dt*24,d.dmag*1e3,d.mag_err*1e3,fmt='.',color='0.5'); plt.axvspan(-2,2,color='orange',alpha=0.2); plt.gca().invert_yaxis(); plt.xlabel('hours from predicted mid-transit'); plt.ylabel('dmag (mmag)'); plt.title(f'ASAS-SN v1 V-band, {len(d)} epochs, folded on frozen ephemeris'); plt.xlim(-220,220); plt.savefig('/Users/fernando/Desktop/NASA/results/external_review/plots/asassn_v1_fold.png',dpi=100)
