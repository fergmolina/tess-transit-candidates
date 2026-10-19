"""Referee recomputation on cached TESScut cubes: loss centroid vs (a) WCS target, (b) restricted star centroid; fake-injection
calibration of the centroid error (Bryson+2013 style, injected depth); depth vs aperture with and without background subtraction;
per-event depths. Read-only on project files."""
import sys, glob, json, warnings; warnings.filterwarnings("ignore")
import numpy as np, lightkurve as lk
from astropy.io import fits
ROOT="/Users/fernando/Desktop/NASA"
def cube_of(path):
    tpf=lk.TessTargetPixelFile(path); t=tpf.time.value; cube=tpf.flux.value; q=np.isfinite(cube).all(axis=(1,2))&np.isfinite(t)&(tpf.quality==0)
    return tpf, t[q], cube[q]
def loss_centroid(cube,t,windows,px,dur_d,near_r=3.5,bg=False):
    ny,nx=cube.shape[1:]; yy,xx=np.mgrid[0:ny,0:nx]; near=np.hypot(xx-px[0],yy-px[1])<near_r; diff=np.zeros((ny,nx)); var=np.zeros((ny,nx)); n=0
    if bg:
        ring=np.hypot(xx-nx/2,yy-ny/2)>=min(nx,ny)/2-1.5
        cube=cube-np.median(cube[:,ring],axis=1)[:,None,None]
    for tc in windows:
        dt=t-tc; wi=np.abs(dt)<dur_d/2; wo=(np.abs(dt)>dur_d)&(np.abs(dt)<3*dur_d)
        if wi.sum()<3 or wo.sum()<6: continue
        d=cube[wo].mean(axis=0)-cube[wi].mean(axis=0); s2=cube[wo].var(axis=0)*(1/wi.sum()+1/wo.sum()); diff+=d/np.maximum(s2,1e-12); var+=1/np.maximum(s2,1e-12); n+=1
    if n==0: return None,0
    dm=diff/np.maximum(var,1e-12); w=np.where(near&(dm>0),dm,0)
    return np.array([(w*xx).sum()/w.sum(),(w*yy).sum()/w.sum()]),n
def depth_vs_ap(cube,t,windows,px,dur_d,bg=False):
    ny,nx=cube.shape[1:]; yy,xx=np.mgrid[0:ny,0:nx]
    if bg:
        ring=np.hypot(xx-nx/2,yy-ny/2)>=min(nx,ny)/2-1.5; cube=cube-np.median(cube[:,ring],axis=1)[:,None,None]
    out={}
    for r_ in (1.5,2.5):
        ap=np.hypot(xx-px[0],yy-px[1])<=r_; lc=cube[:,ap].sum(axis=1); num=den=0; ev=[]
        for tc in windows:
            dt=t-tc; wi=np.abs(dt)<dur_d/2; wo=(np.abs(dt)>dur_d)&(np.abs(dt)<3*dur_d)
            if wi.sum()<3 or wo.sum()<6: continue
            # local linear baseline instead of mean
            c=np.polyfit(t[wo]-tc,lc[wo],1); base=np.polyval(c,t-tc); d=1-np.mean(lc[wi]/base[wi]); s2=np.var(lc[wo]/base[wo])*(1/wi.sum()+1/wo.sum()); num+=d/s2; den+=1/s2; ev.append(round(d*1e6))
        out[r_]=(round(num/den*1e6) if den else None, round(1e6/np.sqrt(den)) if den else None, ev)
    return out
def run(tic,ra,dec,P,T0,dur_h,sectors,size,depth_inj):
    dur_d=dur_h/24; res={}
    for sec in sectors:
        fs=glob.glob(f"{ROOT}/data/lk_cache/tesscut/tess-s{sec:04d}-*_{ra:.6f}_{dec:.6f}_{size}x{size}_astrocut.fits")
        if not fs: print("no cutout",sec,size); continue
        tpf,t,cube=cube_of(fs[0]); px=tpf.wcs.all_world2pix([[ra,dec]],0)[0]
        ny,nx=cube.shape[1:]; yy,xx=np.mgrid[0:ny,0:nx]; mean_img=cube.mean(axis=0)
        near=np.hypot(xx-px[0],yy-px[1])<3.5; fw=np.where(near,mean_img,0); star=np.array([(fw*xx).sum()/fw.sum(),(fw*yy).sum()/fw.sum()])
        fw2=np.where(np.hypot(xx-px[0],yy-px[1])<1.5,mean_img,0); star15=np.array([(fw2*xx).sum()/fw2.sum(),(fw2*yy).sum()/fw2.sum()])
        ep=np.round((t-T0)/P); real_w=sorted(set(T0+e*P for e in ep if np.any(np.abs(t-(T0+e*P))<dur_d/2)))
        real,n=loss_centroid(cube,t,real_w,px,dur_d); realbg,_=loss_centroid(cube,t,real_w,px,dur_d,bg=True)
        # fakes with injection
        rng=np.random.default_rng(sec); fakes=[]; cand=rng.uniform(t.min()+0.6,t.max()-0.6,4000)
        for tc in cand:
            if real_w and min(abs(tc-rw) for rw in real_w)<1.0: continue
            if np.sum(np.abs(t-tc)<dur_d/2)<0.6*dur_d/np.median(np.diff(t)) or np.sum((np.abs(t-tc)>dur_d)&(np.abs(t-tc)<3*dur_d))<3*0.6*dur_d/np.median(np.diff(t)): continue
            wi=np.abs(t-tc)<dur_d/2; cf=cube.copy(); cf[wi]=cf[wi]-depth_inj*mean_img[None]
            c,_=loss_centroid(cf,t,[tc],px,dur_d)
            if c is not None: fakes.append(c-star)
            if len(fakes)>=60: break
        fakes=np.array(fakes); rad=np.sqrt(np.mean(np.sum(fakes**2,axis=1))); med=np.median(fakes,axis=0)
        dva=depth_vs_ap(cube,t,real_w,px,dur_d); dvabg=depth_vs_ap(cube,t,real_w,px,dur_d,bg=True)
        # background level vs star peak
        ring=np.hypot(xx-nx/2,yy-ny/2)>=min(nx,ny)/2-1.5; bgl=np.median(mean_img[ring]); peak=mean_img.max()
        r=dict(n_events=n,target_wcs=px.round(3).tolist(),star_centroid_3p5=star.round(3).tolist(),star_centroid_1p5=star15.round(3).tolist(),
               loss=real.round(3).tolist(),loss_bgsub=realbg.round(3).tolist(),
               loss_minus_wcs=float(np.linalg.norm(real-px)),loss_minus_star=float(np.linalg.norm(real-star)),loss_bgsub_minus_star=float(np.linalg.norm(realbg-star)),
               n_fake=len(fakes),fake_rms_radius_px=float(rad),fake_median_bias=med.round(3).tolist(),sigma_for_n_events=float(rad/np.sqrt(max(n,1))),
               depth_vs_ap_raw=dva,depth_vs_ap_bgsub=dvabg,bg_per_pixel=float(bgl),peak_pixel=float(peak),events_btjd=[round(x,3) for x in real_w])
        res[sec]=r; print(tic,sec,json.dumps(r),flush=True)
    return res
if __name__=="__main__":
    which=sys.argv[1]
    if which=="61310956":
        run(61310956,160.180867,16.192444,16.5378463389246,1906.445639457648,2.7,[72],11,0.0011); run(61310956,160.180867,16.192444,16.5378463389246,1906.445639457648,2.7,[22,45,72],15,0.0011)
    else:
        run(183374279,357.519179,-39.334388,11.737992570458777,1362.5824224663447,2.6,[96,103,105],11,0.001); run(183374279,357.519179,-39.334388,11.737992570458777,1362.5824224663447,2.6,[96,103,105],15,0.001)
