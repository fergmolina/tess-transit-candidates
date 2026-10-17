"""Independent TESS pipelines for TIC 89247735: TARS (S66, S93), TESS-SPOC + ELEANOR-LITE (S13). Measure the depth at each
predicted epoch (frozen ephemeris) with a local box; check S13 coverage at the predicted epoch using ALL cadences."""
import lightkurve as lk, numpy as np, warnings, json; warnings.filterwarnings("ignore")
P=18.32312630839195; T0=4196.80731906277; dur=4.0/24
DD="/Users/fernando/Desktop/NASA/results/external_review/data/hlsp"
sr=lk.search_lightcurve("TIC 89247735")
out={}
for r in sr:
    au=r.author[0] if hasattr(r.author,'__len__') and not isinstance(r.author,str) else r.author
    mis=r.mission[0] if not isinstance(r.mission,str) else r.mission
    if au=="QLP": continue
    try: lc=r.download(download_dir=DD)
    except Exception as e: print(mis,au,"download failed",e); continue
    cols=lc.columns
    print("===",mis,au,"N",len(lc),"columns",[c for c in cols][:14])
    t=np.asarray(lc.time.value,float)
    for col in [c for c in ("pdcsap_flux","sap_flux","corr_flux","flux","psf_flux","cal_flux") if c in cols]:
        f=np.asarray(lc[col].value,float); q=np.asarray(lc['quality'].value if 'quality' in cols else np.zeros(len(t)),int)
        n0=int(np.floor((np.nanmin(t)-T0)/P))-1; n1=int(np.ceil((np.nanmax(t)-T0)/P))+1
        for n in range(n0,n1+1):
            tc=T0+n*P
            if tc<np.nanmin(t)-0.2 or tc>np.nanmax(t)+0.2: continue
            intr=np.isfinite(f)&(np.abs(t-tc)<dur/2); oot=np.isfinite(f)&(np.abs(t-tc)>dur)&(np.abs(t-tc)<3*dur)
            near=np.isfinite(t)&(np.abs(t-tc)<0.5)
            if intr.sum()<2 or oot.sum()<5:
                print(f"  {col} epoch {n} tc={tc:.3f}: cadences within +-0.5 d = {near.sum()}, in-transit finite = {intr.sum()} -> not measurable"); continue
            med=np.nanmedian(f[oot]); d=(med-np.nanmean(f[intr]))/med; e=np.nanstd(f[oot])/med/np.sqrt(intr.sum())
            print(f"  {col} epoch {n} tc={tc:.3f}: depth {d*1e6:.0f} +- {e*1e6:.0f} ppm (n_in {intr.sum()}, Q0 in-transit {np.sum(intr&(q==0))}, oot rms {np.nanstd(f[oot])/med*1e6:.0f} ppm)")
            out[f"{mis}_{au}_{col}_e{n}"]=dict(depth_ppm=d*1e6,err_ppm=e*1e6,n_in=int(intr.sum()))
json.dump(out,open("/Users/fernando/Desktop/NASA/results/external_review/hlsp_check_89247735.json","w"),indent=1)
