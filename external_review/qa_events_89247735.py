"""External review: raw QLP columns around every predicted epoch of TIC 89247735 that falls inside a sector's time range
(including partially covered edge epochs), with all quality flags shown. Frozen ephemeris from PREREGISTRATION.md."""
from astropy.io import fits
import numpy as np, glob, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
P=18.32312630839195; T0=4196.80731906277; dur=4.0/24
OUT="/Users/fernando/Desktop/NASA/results/external_review"
rows=[]
for fp in sorted(glob.glob('/Users/fernando/Desktop/NASA/data/qlp/*89247735*')):
    with fits.open(fp) as h:
        sec=h[0].header['SECTOR']; d=h[1].data; cols=h[1].columns.names
        t=np.array(d['TIME'],float); q=np.array(d['QUALITY'],int); sap=np.array(d['SAP_FLUX'],float)
        det=np.array(d['DET_FLUX'] if 'DET_FLUX' in cols else d['KSPSAP_FLUX'],float)
        bkg=np.array(d['SAP_BKG'],float); sx=np.array(d['SAP_X'],float); sy=np.array(d['SAP_Y'],float)
    ok=np.isfinite(t)
    n0=int(np.floor((np.nanmin(t)-T0)/P))-1; n1=int(np.ceil((np.nanmax(t)-T0)/P))+1
    for n in range(n0,n1+1):
        tc=T0+n*P
        if tc < np.nanmin(t)-0.3 or tc > np.nanmax(t)+0.3: continue
        w=ok&(np.abs(t-tc)<1.0)
        if w.sum()==0: print(f"S{sec} epoch {n} tc={tc:.3f}: NO cadences within +-1 d"); continue
        intr=ok&(np.abs(t-tc)<dur/2); intr0=intr&(q==0)
        oot=ok&(np.abs(t-tc)>dur)&(np.abs(t-tc)<3*dur)&(q==0)
        med=np.nanmedian(sap[oot]) if oot.sum()>5 else np.nan
        dsap=(med-np.nanmean(sap[intr0]))/med if intr0.sum()>2 else np.nan
        # also depth using ALL flags (any quality) to see if flagged cadences hide something
        intr_any=intr&np.isfinite(sap); dsap_any=(med-np.nanmean(sap[intr_any]))/med if intr_any.sum()>2 else np.nan
        print(f"S{sec} epoch {n} tc={tc:.4f}: cadences within +-1d={w.sum()} (Q0 {np.sum(w&(q==0))}); in-transit all={intr.sum()} Q0={intr0.sum()}; "
              f"SAP depth (Q0) = {dsap*1e6:.0f} ppm; SAP depth (all flags) = {dsap_any*1e6:.0f} ppm; in-transit flags: {dict(zip(*np.unique(q[intr],return_counts=True)))}")
        rows.append((sec,n,tc,w.sum(),intr.sum(),intr0.sum(),dsap))
        fig,ax=plt.subplots(5,1,figsize=(10,11),sharex=True)
        x=(t[w]-tc)*24
        for a_,y,lab in zip(ax,[sap[w]/np.nanmedian(sap[w]),det[w],bkg[w],sx[w],sy[w]],['SAP_FLUX (norm)','DET/KSPSAP_FLUX','SAP_BKG','SAP_X','SAP_Y']):
            qq=q[w]; a_.plot(x[qq==0],y[qq==0],'k.',ms=3,label='Q==0'); a_.plot(x[qq!=0],y[qq!=0],'r.',ms=3,label='flagged'); a_.set_ylabel(lab); a_.axvspan(-2,2,color='orange',alpha=0.15)
        ax[0].legend(loc='lower left'); ax[0].set_title(f'TIC 89247735 S{sec} epoch {n} predicted tc=BTJD {tc:.4f}'); ax[-1].set_xlabel('hours from predicted mid-transit')
        plt.tight_layout(); plt.savefig(f'{OUT}/plots/qa_S{sec}_epoch{n}.png',dpi=90); plt.close()
