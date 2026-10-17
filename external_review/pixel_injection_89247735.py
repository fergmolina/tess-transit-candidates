"""External review: (1) reproduce the team's flux-loss centroid estimator on the cached TESScut cutouts of TIC 89247735;
(2) quantify its bias by injecting the same total flux loss at the target position and at the G=15.49 neighbour position
(PSF taken from the mean image), using out-of-transit cadences as the fake in-transit cadences; (3) fit the loss map with
a Gaussian-PSF point source at a free position and compare chi2 for target vs neighbour; (4) correct the target position
for proper motion (Gaia J2016 -> observation epoch) and compare WCS vs local flux centroid."""
import numpy as np, json, warnings; warnings.filterwarnings("ignore")
import lightkurve as lk, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from scipy.optimize import least_squares
from astropy.time import Time
P=18.32312630839195; T0=4196.80731906277; dur=4.0/24
CACHE="/Users/fernando/Desktop/NASA/data/lk_cache/tesscut/"
files={66:"tess-s0066-1-2_275.223692_-45.561167_11x11_astrocut.fits",93:"tess-s0093-1-2_275.223692_-45.561167_11x11_astrocut.fits",104:"tess-s0104-1-3_275.223692_-45.561167_11x11_astrocut.fits"}
# Gaia DR3 J2016 positions
tgt=dict(ra=275.2234460704073,dec=-45.56163775820568,pmra=-39.0734,pmdec=-105.8401,G=11.851)
nb=dict(ra=275.22077986704636,dec=-45.562825283905,pmra=1.694,pmdec=-6.031,G=15.486)
def pos_at(src,yr):
    dt=yr-2016.0; return src['ra']+src['pmra']*dt/3.6e6/np.cos(np.radians(src['dec'])), src['dec']+src['pmdec']*dt/3.6e6
def team_centroid(depth_map,sig_map,px_t,ny,nx):
    yy,xx=np.mgrid[0:ny,0:nx]; near=np.hypot(xx-px_t[0],yy-px_t[1])<3.5
    w=np.where(near&(depth_map>0),depth_map,0); return (w*xx).sum()/w.sum(),(w*yy).sum()/w.sum()
def depth_map_from(cube,t,q):
    ph=((t-T0)/P+0.5)%1-0.5; dt=ph*P; intr=np.abs(dt)<dur/2; oot=(np.abs(dt)>dur)&(np.abs(dt)<3*dur)
    ep=np.round((t-T0)/P).astype(int); diff=np.zeros(cube.shape[1:]); var=np.zeros_like(diff); n_ev=0
    for e in np.unique(ep):
        wi=intr&(ep==e); wo=oot&(ep==e)
        if wi.sum()<3 or wo.sum()<6: continue
        d=cube[wo].mean(axis=0)-cube[wi].mean(axis=0); s2=cube[wo].var(axis=0)*(1/wi.sum()+1/wo.sum())
        diff+=d/np.maximum(s2,1e-12); var+=1/np.maximum(s2,1e-12); n_ev+=1
    dm=diff/np.maximum(var,1e-12); return dm, dm*np.sqrt(var), 1/np.sqrt(np.maximum(var,1e-12)), intr, oot, ep, n_ev
def gauss(xx,yy,x0,y0,s): return np.exp(-((xx-x0)**2+(yy-y0)**2)/(2*s*s))/(2*np.pi*s*s)
out={}
for sec,fn in files.items():
    tpf=lk.read(CACHE+fn); t=tpf.time.value; cube=tpf.flux.value.astype(float)
    q=np.isfinite(cube).all(axis=(1,2))&np.isfinite(t)&(tpf.quality==0); t,cube=t[q],cube[q]
    ny,nx=cube.shape[1:]; yy,xx=np.mgrid[0:ny,0:nx]
    yr=Time(t.mean()+2457000,format='jd').decimalyear
    ra_t,dec_t=pos_at(tgt,yr); ra_n,dec_n=pos_at(nb,yr)
    px_t=tpf.wcs.all_world2pix([[ra_t,dec_t]],0)[0]; px_n=tpf.wcs.all_world2pix([[ra_n,dec_n]],0)[0]
    px_t2000=tpf.wcs.all_world2pix([[275.223692,-45.561167]],0)[0]   # the catalogue position the team used
    dm,sm,em,intr,oot,ep,n_ev=depth_map_from(cube,t,q[q])
    # --- (4) PSF from the mean image: fit Gaussian + background to pixels within 2.5 px of the target
    mean_img=cube[oot].mean(axis=0); near=np.hypot(xx-px_t[0],yy-px_t[1])<=2.5
    def resid_img(p):
        A,x0,y0,s,bkg,An=p; m=A*gauss(xx,yy,x0,y0,s)+An*gauss(xx,yy,x0+(px_n[0]-px_t[0]),y0+(px_n[1]-px_t[1]),s)+bkg; return (m-mean_img)[near]
    p0=[mean_img.max()*2*np.pi,px_t[0],px_t[1],0.7,np.median(mean_img),mean_img.max()*2*np.pi*10**(-0.4*(nb['G']-tgt['G']))]
    fi=least_squares(resid_img,p0); A,x0,y0,sig,bkg,An=fi.x
    wcs_vs_fit=np.hypot(x0-px_t[0],y0-px_t[1])
    # --- (1) team's estimator on the real data, with J2000 target (as the team did) and with PM-corrected target
    c_real=team_centroid(dm,sm,px_t2000,ny,nx); c_real_pm=team_centroid(dm,sm,px_t,ny,nx)
    # --- (3) fit the loss map with a point source (Gaussian PSF of width sig) at free / target / neighbour position
    w=1/np.maximum(em,1e-9); fitreg=np.hypot(xx-px_t[0],yy-px_t[1])<=3.5
    def chi2_at(x0_,y0_):
        g=gauss(xx,yy,x0_,y0_,sig)[fitreg]; d=dm[fitreg]; ww=w[fitreg]**2
        Amp=np.sum(ww*g*d)/np.sum(ww*g*g); return float(np.sum(ww*(d-Amp*g)**2)), float(Amp)
    def free_fit(start,dmap=None):
        dmap=dm if dmap is None else dmap
        r=least_squares(lambda p: ((dmap-p[0]*gauss(xx,yy,p[1],p[2],sig))*w)[fitreg], [chi2_at(*start)[1],start[0],start[1]])
        J=r.jac; cov=np.linalg.inv(J.T@J)*max(1,np.sum(r.fun**2)/(fitreg.sum()-3)); return r.x, np.sqrt(np.diag(cov)), float(np.sum(r.fun**2))
    xf,ef,chi_free=free_fit(px_t); chi_t,_=chi2_at(*px_t); chi_n,_=chi2_at(*px_n)
    # also allow PSF width free in the loss-map fit (shape check)
    rr=least_squares(lambda p: ((dm-p[0]*gauss(xx,yy,p[1],p[2],p[3]))*w)[fitreg], [xf[0],xf[1],xf[2],sig])
    # --- (2) injection: fake in-transit cadences = out-of-transit cadences minus L*PSF at the chosen position
    # total flux loss L chosen to reproduce the observed loss-map amplitude (fit amplitude at free position)
    L=xf[0]
    def inject(xi,yi,seed=0):
        rng=np.random.default_rng(seed); cube2=cube.copy()
        for e in np.unique(ep):
            wi=np.where(intr&(ep==e))[0]; wo=np.where(oot&(ep==e))[0]
            if len(wi)<3 or len(wo)<6: continue
            src=rng.choice(wo,size=len(wi),replace=True)
            cube2[wi]=cube[src]-L*gauss(xx,yy,xi,yi,sig)[None,:,:]
        dmi,smi,_,_,_,_,_=depth_map_from(cube2,t,None)
        ct=team_centroid(dmi,smi,px_t2000,ny,nx); xf2,_,_=free_fit((xi,yi),dmi); return ct, xf2
    res_inj={}
    for lab,(xi,yi) in dict(target=px_t,neighbour=px_n,J2000target=px_t2000).items():
        cts=[]; ffs=[]
        for s in range(5):
            ct,xf2=inject(xi,yi,s); cts.append(ct); ffs.append(xf2[1:3])
        cts=np.array(cts); ffs=np.array(ffs)
        res_inj[lab]=dict(injected_px=[float(xi),float(yi)], team_centroid_mean=cts.mean(0).tolist(), team_centroid_sd=cts.std(0).tolist(),
                          team_offset_from_J2000target_px=float(np.hypot(*(cts.mean(0)-px_t2000))), team_offset_from_injected_px=float(np.hypot(*(cts.mean(0)-np.array([xi,yi])))),
                          psf_fit_pos_mean=ffs.mean(0).tolist(), psf_fit_offset_from_injected_px=float(np.hypot(*(ffs.mean(0)-np.array([xi,yi])))),
                          psf_fit_offset_from_pmtarget_px=float(np.hypot(*(ffs.mean(0)-px_t))), psf_fit_offset_from_neighbour_px=float(np.hypot(*(ffs.mean(0)-px_n))))
    sep_tn=float(np.hypot(*(px_n-px_t)))
    out[sec]=dict(n_events=n_ev, epoch_year=float(yr), target_px_J2000=px_t2000.tolist(), target_px_pm_corrected=px_t.tolist(), neighbour_px=px_n.tolist(), target_neighbour_sep_px=sep_tn,
                  psf_sigma_px=float(sig), mean_image_fit_pos=[float(x0),float(y0)], wcs_minus_imagefit_px=float(wcs_vs_fit),
                  team_loss_centroid_vs_J2000target_px=float(np.hypot(*(np.array(c_real)-px_t2000))), team_loss_centroid_vs_pmtarget_px=float(np.hypot(*(np.array(c_real)-px_t))),
                  team_loss_centroid_vs_neighbour_px=float(np.hypot(*(np.array(c_real)-px_n))),
                  psf_fit_loss_pos=xf[1:3].tolist(), psf_fit_loss_pos_err=ef[1:3].tolist(), psf_fit_vs_pmtarget_px=float(np.hypot(*(xf[1:3]-px_t))), psf_fit_vs_neighbour_px=float(np.hypot(*(xf[1:3]-px_n))),
                  psf_fit_vs_imagefit_px=float(np.hypot(xf[1]-x0,xf[2]-y0)),
                  chi2_free=chi_free, chi2_at_target=chi_t, chi2_at_neighbour=chi_n, dchi2_neighbour_minus_target=chi_n-chi_t, n_pix_fit=int(fitreg.sum()),
                  loss_psf_width_free=float(rr.x[3]), loss_amplitude=float(xf[0]), injection=res_inj)
    print(f"S{sec}: events={n_ev} epoch {yr:.2f}; PSF sigma {sig:.2f} px; WCS(PM-corr) vs image-fit target pos {wcs_vs_fit:.2f} px; target-neighbour sep {sep_tn:.2f} px")
    print(f"   team centroid: vs J2000 target {out[sec]['team_loss_centroid_vs_J2000target_px']:.3f}, vs PM-corrected target {out[sec]['team_loss_centroid_vs_pmtarget_px']:.3f}, vs neighbour {out[sec]['team_loss_centroid_vs_neighbour_px']:.3f} px")
    print(f"   PSF fit of loss map: pos ({xf[1]:.2f}+-{ef[1]:.2f}, {xf[2]:.2f}+-{ef[2]:.2f}); vs PM target {out[sec]['psf_fit_vs_pmtarget_px']:.2f} px, vs neighbour {out[sec]['psf_fit_vs_neighbour_px']:.2f} px, vs image-fit star pos {out[sec]['psf_fit_vs_imagefit_px']:.2f} px; chi2 free {chi_free:.1f} target {chi_t:.1f} neighbour {chi_n:.1f} (N={fitreg.sum()}); loss PSF width free {rr.x[3]:.2f}")
    for lab,r in res_inj.items(): print(f"   INJECT at {lab}: team estimator lands {r['team_offset_from_J2000target_px']:.3f} px from J2000 target, {r['team_offset_from_injected_px']:.3f} px from injected pos; PSF-fit of injected map: {r['psf_fit_offset_from_injected_px']:.3f} px from injected pos, {r['psf_fit_offset_from_pmtarget_px']:.3f} from PM target, {r['psf_fit_offset_from_neighbour_px']:.3f} from neighbour")
    fig,ax=plt.subplots(1,3,figsize=(14,4.3))
    ax[0].imshow(np.log10(np.maximum(mean_img,1)),origin='lower',cmap='gray'); ax[0].set_title(f'S{sec} mean image (log)')
    im=ax[1].imshow(dm,origin='lower',cmap='RdBu_r',vmin=-np.nanmax(np.abs(dm)),vmax=np.nanmax(np.abs(dm))); ax[1].set_title('flux-loss map (e-/s)'); plt.colorbar(im,ax=ax[1])
    im=ax[2].imshow(sm,origin='lower',cmap='RdBu_r',vmin=-np.nanmax(np.abs(sm)),vmax=np.nanmax(np.abs(sm))); ax[2].set_title('loss significance'); plt.colorbar(im,ax=ax[2])
    for a in ax:
        a.plot(*px_t,'x',color='lime',ms=12,mew=2,label='target (PM-corr)'); a.plot(*px_t2000,'+',color='green',ms=10,mew=1.5,label='target J2000 (team)'); a.plot(*px_n,'o',mfc='none',mec='orange',ms=12,mew=2,label='G=15.5 neighbour')
        a.plot(*c_real,'+',color='cyan',ms=14,mew=2,label='team loss centroid'); a.plot(xf[1],xf[2],'s',mfc='none',mec='magenta',ms=10,mew=2,label='PSF-fit loss pos'); a.set_xlim(2.5,8.5); a.set_ylim(2.5,8.5)
    ax[0].legend(fontsize=7,loc='upper left'); plt.tight_layout(); plt.savefig(f'/Users/fernando/Desktop/NASA/results/external_review/plots/pixel_review_S{sec}.png',dpi=100); plt.close()
json.dump(out,open('/Users/fernando/Desktop/NASA/results/external_review/pixel_injection_89247735.json','w'),indent=1)
