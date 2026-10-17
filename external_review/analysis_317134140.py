"""External review of the TIC 317134140 0.5719-d signal: (a) Lomb-Scargle of raw PDCSAP/SAP per sector (rotation / harmonic
series?), (b) detrend-window sensitivity of the depth at the frozen ephemeris, (c) sinusoid vs box model comparison on the fold,
(d) depth-constancy chi2, (e) masked-vs-unmasked detrend bias of the random-phase null used in the holdout test."""
import sys, json, warnings; warnings.filterwarnings("ignore"); sys.path.insert(0,"/Users/fernando/Desktop/NASA/scripts")
import numpy as np, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from astropy.timeseries import LombScargle
from wotan import flatten, transit_mask
from tsearch import load_spoc_lc, trim_edges
from search_pipeline import sector_files, bin_lc
from vet import box_depth
P=0.5718634; T0=1468.67922; dur=1.5/24
mP,mT0,mdur=6.3951381,2459215.084143-2457000,4.047/24
OUT="/Users/fernando/Desktop/NASA/results/external_review"
res={}
raw={}
for fp in sector_files(317134140):
    for col in ("PDCSAP_FLUX","SAP_FLUX"):
        t,f,fe,m=load_spoc_lc(fp,flux_col=col); keep=trim_edges(t)&~transit_mask(time=t,period=mP,duration=1.5*mdur,T0=mT0); t,f=t[keep],f[keep]
        raw[(m['sector'],col)]=(t,f)
# (a) Lomb-Scargle on raw flux (no detrend) 0.2-15 d
res['lombscargle']={}
for (sec,col),(t,f) in raw.items():
    freq=np.linspace(1/15,1/0.2,200000); ls=LombScargle(t,f); pw=ls.power(freq)
    top=np.argsort(pw)[::-1]; peaks=[]
    for i in top:
        if all(abs(1/freq[i]-p[0])/p[0]>0.03 for p in peaks): peaks.append((float(1/freq[i]),float(pw[i]),float(np.sqrt(4*pw[i]/len(t))*np.std(f)*1e6*0+ls.model_parameters(freq[i])[1:].__abs__().max()*1e6)))
        if len(peaks)>=5: break
    at={}
    for lab,per in (("P",P),("2P",2*P),("3P",3*P),("P/2",P/2)):
        i=np.argmin(np.abs(freq-1/per)); mp=ls.model_parameters(freq[i]); at[lab]=dict(power=float(pw[i]),amp_ppm=float(np.hypot(mp[1],mp[2])*1e6))
    res['lombscargle'][f"S{sec}_{col}"]=dict(top_peaks=[dict(period=p[0],power=p[1],amp_ppm=p[2]) for p in peaks],at=at,rms_ppm=float(np.std(f)*1e6))
    print(f"LS S{sec} {col}: top periods {[(round(p[0],3),round(p[2])) for p in peaks]} ; amp at P {at['P']['amp_ppm']:.0f} ppm, 2P {at['2P']['amp_ppm']:.0f}, 3P {at['3P']['amp_ppm']:.0f}, P/2 {at['P/2']['amp_ppm']:.0f}")
# (b) detrend window scan (unmasked biweight, as the discovery search) and masked
res['window_scan']={}
for sec in sorted({s for s,c in raw}):
    t,f=raw[(sec,"PDCSAP_FLUX")]; row={}
    for win in (0.25,0.5,0.75,1.0,2.0):
        fl=flatten(t,f,method="biweight",window_length=win,break_tolerance=0.5); ok=np.isfinite(fl)
        d,de,n=box_depth(t[ok],fl[ok],P,T0,dur)
        mask=transit_mask(time=t,period=P,duration=2*dur,T0=T0); flm=flatten(t,f,method="biweight",window_length=win,break_tolerance=0.5,mask=mask); okm=np.isfinite(flm)
        dm,dem,nm=box_depth(t[okm],flm[okm],P,T0,dur)
        row[win]=dict(unmasked=[d*1e6,de*1e6],masked=[dm*1e6,dem*1e6]); 
    res['window_scan'][sec]=row
    print(f"S{sec} depth at frozen ephemeris vs window:", {w:(round(v['unmasked'][0]),round(v['masked'][0]),round(v['masked'][1])) for w,v in row.items()})
# (e) masked vs unmasked null: distribution of random-phase box depths with masked detrend (at the candidate phase) vs unmasked
res['null_bias']={}
for sec in sorted({s for s,c in raw}):
    t,f=raw[(sec,"PDCSAP_FLUX")]
    mask=transit_mask(time=t,period=P,duration=2*dur,T0=T0); flm=flatten(t,f,method="biweight",window_length=0.75,break_tolerance=0.5,mask=mask); okm=np.isfinite(flm)
    flu=flatten(t,f,method="biweight",window_length=0.75,break_tolerance=0.5); oku=np.isfinite(flu)
    rng=np.random.default_rng(3); ph=0.1+0.8*rng.random(300)
    # for each random phase, measure depth in (i) the candidate-masked detrend (what the team's null does) and (ii) a detrend masked at THAT phase (apples to apples)
    d_team=[]; d_fair=[]
    for p_ in ph:
        d_team.append(box_depth(t[okm],flm[okm],P,T0+P*p_,dur)[0])
        mk=transit_mask(time=t,period=P,duration=2*dur,T0=T0+P*p_); fl2=flatten(t,f,method="biweight",window_length=0.75,break_tolerance=0.5,mask=mk); ok2=np.isfinite(fl2)
        d_fair.append(box_depth(t[ok2],fl2[ok2],P,T0+P*p_,dur)[0])
    d_team=np.array(d_team)*1e6; d_fair=np.array(d_fair)*1e6
    dc=box_depth(t[okm],flm[okm],P,T0,dur)[0]*1e6
    res['null_bias'][sec]=dict(candidate_depth_masked=dc,null_team_sd=float(np.std(d_team)),null_team_mean=float(np.mean(d_team)),null_fair_sd=float(np.std(d_fair)),null_fair_mean=float(np.mean(d_fair)),
                               p_team=float(np.mean(d_team>=dc)),p_fair=float(np.mean(d_fair>=dc)))
    print(f"S{sec} null bias: candidate {dc:.0f} ppm; team-style null mean {np.mean(d_team):.0f} sd {np.std(d_team):.0f} (p={np.mean(d_team>=dc):.3f}); fair (phase-masked) null mean {np.mean(d_fair):.0f} sd {np.std(d_fair):.0f} (p={np.mean(d_fair>=dc):.3f})")
# (c) sinusoid vs box on stitched masked-detrended data
T=[];F=[]
for sec in sorted({s for s,c in raw}):
    t,f=raw[(sec,"PDCSAP_FLUX")]; mask=transit_mask(time=t,period=P,duration=2*dur,T0=T0); fl=flatten(t,f,method="biweight",window_length=0.75,break_tolerance=0.5,mask=mask); ok=np.isfinite(fl)
    mad=1.4826*np.median(np.abs(fl[ok]-np.median(fl[ok]))); ok&=fl<1+5*mad; T.append(t[ok]); F.append(fl[ok])
T=np.concatenate(T); F=np.concatenate(F); ph=((T-T0)/P+0.5)%1-0.5; sig=np.std(F)
def chi2(model): return float(np.sum((F-model)**2)/sig**2)
box=np.where(np.abs(ph*P)<dur/2,1.0,0.0); A=np.vstack([np.ones_like(F),box]).T; cb=np.linalg.lstsq(A,F,rcond=None)[0]; c_box=chi2(A@cb)
A1=np.vstack([np.ones_like(F),np.cos(2*np.pi*ph),np.sin(2*np.pi*ph)]).T; c1=np.linalg.lstsq(A1,F,rcond=None)[0]; c_sin1=chi2(A1@c1)
A2=np.vstack([np.ones_like(F),np.cos(2*np.pi*ph),np.sin(2*np.pi*ph),np.cos(4*np.pi*ph),np.sin(4*np.pi*ph)]).T; c2=np.linalg.lstsq(A2,F,rcond=None)[0]; c_sin2=chi2(A2@c2)
c_flat=chi2(np.full_like(F,F.mean()))
res['model_comparison']=dict(n=len(F),chi2_flat=c_flat,chi2_box=c_box,box_depth_ppm=float(-cb[1]*1e6),chi2_sin1=c_sin1,sin1_amp_ppm=float(np.hypot(c1[1],c1[2])*1e6),chi2_sin2=c_sin2,
                             dchi2_box_vs_flat=c_flat-c_box,dchi2_sin1_vs_flat=c_flat-c_sin1,dchi2_sin2_vs_flat=c_flat-c_sin2, bic_box=c_box+2*np.log(len(F)), bic_sin1=c_sin1+3*np.log(len(F)), bic_sin2=c_sin2+5*np.log(len(F)))
print("model comparison (N=%d): dchi2 vs flat: box(1 par) %.1f, sinusoid(2) %.1f, sin+harm(4) %.1f; box depth %.0f ppm, sin amp %.0f ppm"%(len(F),c_flat-c_box,c_flat-c_sin1,c_flat-c_sin2,-cb[1]*1e6,np.hypot(c1[1],c1[2])*1e6))
# (d) depth constancy
secs={6:(117.7,38.1),87:(113.0,38.0),98:(212.8,29.8),107:(199.8,38.1),32:(56,36),33:(192,34)}
d=np.array([v[0] for v in secs.values()]); e=np.array([v[1] for v in secs.values()]); wm=np.sum(d/e**2)/np.sum(1/e**2); chi=np.sum((d-wm)**2/e**2)
from scipy.stats import chi2 as c2d
res['depth_constancy']=dict(weighted_mean_ppm=float(wm),chi2=float(chi),dof=len(d)-1,p=float(c2d.sf(chi,len(d)-1)))
print(f"depth constancy (report per-sector values): mean {wm:.0f} ppm, chi2 {chi:.1f}/{len(d)-1}, p={c2d.sf(chi,len(d)-1):.4f}")
# fold figure
fig,ax=plt.subplots(1,2,figsize=(12,4)); pb,fb,eb=bin_lc(ph*P*24+100,F,np.full_like(F,sig),0.25); ax[0].errorbar(pb-100,(fb-1)*1e6,eb*1e6,fmt='ko',ms=3)
xs=np.linspace(-0.5,0.5,400); ax[0].plot(xs*P*24,(A2[:0].shape and 0) or (c2[0]+c2[1]*np.cos(2*np.pi*xs)+c2[2]*np.sin(2*np.pi*xs)+c2[3]*np.cos(4*np.pi*xs)+c2[4]*np.sin(4*np.pi*xs)-1)*1e6,'r-',label='sin+harmonic')
ax[0].plot(xs*P*24,(cb[0]+cb[1]*(np.abs(xs*P)<dur/2)-1)*1e6,'b-',label='box'); ax[0].legend(); ax[0].set_xlabel('hours from predicted mid-transit'); ax[0].set_ylabel('ppm'); ax[0].set_title('TIC 317134140 all 2-min sectors, 15-min bins')
ax[1].bar([str(k) for k in secs],d,yerr=e,color='0.6'); ax[1].axhline(wm,color='r'); ax[1].set_ylabel('depth ppm'); ax[1].set_title(f'per-sector depth, chi2={chi:.1f}/{len(d)-1}')
plt.tight_layout(); plt.savefig(f'{OUT}/plots/review_317134140_fold.png',dpi=100)
json.dump(res,open(f'{OUT}/analysis_317134140.json','w'),indent=1,default=float)
