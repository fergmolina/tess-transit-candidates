import sys, glob, json, warnings; warnings.filterwarnings("ignore")
import numpy as np, lightkurve as lk
sys.path.insert(0,'.'); from pixel_check import cube_of, loss_centroid
ROOT="/Users/fernando/Desktop/NASA"
def run(tic,ra,dec,P,T0,dur_h,sectors,size,depth_inj):
    dur_d=dur_h/24
    for sec in sectors:
        fs=glob.glob(f"{ROOT}/data/lk_cache/tesscut/tess-s{sec:04d}-*_{ra:.6f}_{dec:.6f}_{size}x{size}_astrocut.fits")
        tpf,t,cube=cube_of(fs[0]); px=tpf.wcs.all_world2pix([[ra,dec]],0)[0]
        ny,nx=cube.shape[1:]; yy,xx=np.mgrid[0:ny,0:nx]; mean_img=cube.mean(axis=0)
        near=np.hypot(xx-px[0],yy-px[1])<3.5; fw=np.where(near,mean_img,0); star=np.array([(fw*xx).sum()/fw.sum(),(fw*yy).sum()/fw.sum()])
        ep=np.round((t-T0)/P); real_w=sorted(set(T0+e*P for e in ep if np.any(np.abs(t-(T0+e*P))<dur_d/2)))
        real,n=loss_centroid(cube,t,real_w,px,dur_d)
        # per-event real centroids
        per=[]
        for rw in real_w:
            c,_=loss_centroid(cube,t,[rw],px,dur_d)
            if c is not None and np.all(np.isfinite(c)): per.append((round(rw,3),(c-star).round(3).tolist()))
        rng=np.random.default_rng(sec); fakes=[]; cand=rng.uniform(t.min()+0.6,t.max()-0.6,6000); cad=np.median(np.diff(t))
        for tc in cand:
            if real_w and min(abs(tc-rw) for rw in real_w)<1.0: continue
            if np.sum(np.abs(t-tc)<dur_d/2)<0.6*dur_d/cad or np.sum((np.abs(t-tc)>dur_d)&(np.abs(t-tc)<3*dur_d))<3*0.6*dur_d/cad: continue
            wi=np.abs(t-tc)<dur_d/2; cf=cube.copy(); cf[wi]=cf[wi]-depth_inj*mean_img[None]
            c,_=loss_centroid(cf,t,[tc],px,dur_d)
            if c is not None and np.all(np.isfinite(c)): fakes.append(c-star)
            if len(fakes)>=80: break
        fakes=np.array(fakes); rad=np.sqrt(np.mean(np.sum(fakes**2,axis=1))); sig=rad/np.sqrt(max(n,1))
        # sky direction of the real loss offset (loss - star), arcsec E and N
        sky_l=tpf.wcs.all_pix2world([real],0)[0]; sky_s=tpf.wcs.all_pix2world([star],0)[0]
        dE=(sky_l[0]-sky_s[0])*np.cos(np.radians(dec))*3600; dN=(sky_l[1]-sky_s[1])*3600
        d=float(np.linalg.norm(real-star))
        print(f"{tic} S{sec} {size}x{size}: n_ev {n}; loss-star {d:.3f} px = {d*21:.1f} arcsec (dE {dE:+.1f}, dN {dN:+.1f}); per-event {per}; fakes n={len(fakes)} rms radius {rad:.3f} px/event, median |fake| {np.median(np.hypot(fakes[:,0],fakes[:,1])):.3f}; sigma({n} ev) {sig:.3f} px -> offset {d/sig:.1f} sigma; p(fake>=d, 1ev) {np.mean(np.hypot(fakes[:,0],fakes[:,1])>=d):.2f}",flush=True)
run(61310956,160.180867,16.192444,16.5378463389246,1906.445639457648,2.7,[72,22,45],15,0.0011)
run(183374279,357.519179,-39.334388,11.737992570458777,1362.5824224663447,2.6,[96,103,105],15,0.0012)
