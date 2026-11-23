from pathlib import Path
import ast,json,csv,hashlib,statistics
import numpy as np
from astropy.time import Time
R=Path('/Users/fernando/Desktop/NASA'); A=R/'results/reproduction_317134140_S108_auditor'
src=(R/'scripts/prereg_conformance.py').read_text(); tree=ast.parse(src)
nodes=[x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name in ('edge_trim','coverage')]
ns={'np':np,'EDGE_AFTER_D':1.5,'EDGE_BEFORE_D':.5,'GAP_LONG_D':.5,'GAP_SHORT_D':.1}
exec(compile(ast.Module(body=nodes,type_ignores=[]),str(R/'scripts/prereg_conformance.py'), 'exec'),ns)
DRN=[(4262.08493,4268.95437),(4269.16409,4276.26409),(4276.47381,4283.54464),(4283.74742,4290.77381)]
orb=list(csv.DictReader(line for line in (R/'catalogs/TESS_orbit_times.csv').read_text().splitlines() if not line.startswith('#')))
o=[x for x in orb if x.get('Sector')=='107'];conv=lambda s:float(Time(s.replace(' ','T'),scale='utc').tdb.jd-2457000)
segs=[(conv(x['Start of Orbit']),conv(x['End of Orbit'])) for x in o]
# Only rounded aggregate gap metadata published in the existing forecast text is used. No template FITS is read.
templates={'S68cam1':(.06,3.31,[(1,2.79,.04)]),'S69cam2':(2.01,1.48,[(1,1.58,.02)]),'S96cam1':(2.20,.38,[(1,.44,4.03)]),'S96cam2':(.86,.03,[(1,.03,1.09)]),'S105cam2':(.88,.52,[(1,.40,1.05),(2,1.48,.02)]),'S105cam3':(1.25,.76,[(1,.40,1.43),(2,1.48,0)]),'S105cam4':(2.48,.76,[(1,.40,2.74),(2,1.71,.02)])}
CAD=200/86400
br=[(segs[i][1],segs[i+1][0]) for i in range(3)]
def times(tpl):
 start,end,gaps=tpl;t=np.arange(segs[0][0]+start,segs[-1][1]-end,CAD);keep=np.ones(len(t),bool)
 for a,b in br:keep&=~((t>a)&(t<b))
 for k,pre,post in gaps:keep&=~((t>br[k][0]-pre)&(t<br[k][1]+post))
 return t[keep]
rows=[];inputs={}
saved=list(csv.DictReader((R/'results/s107_drn145/s107_forecast_drn145.csv').open()))
for tic in [24526743,160330868]:
 cfg=json.loads((R/f'configs/conformance/{tic}_S107.json').read_text());pred=Path(cfg['pred_csv']);assert hashlib.sha256(pred.read_bytes()).hexdigest()==cfg['pred_sha256'];assert hashlib.sha256(src.encode()).hexdigest()==cfg['evaluator_sha256']
 ev=[x for x in csv.DictReader(pred.open()) if x['status'].startswith('prediction') and x['tess_sector']=='107']; D=cfg['ref_dur_h']/24;inputs[str(tic)]=ev
 cases=[('DRN145',np.concatenate([np.arange(a,b,CAD) for a,b in DRN]))]+[(n,times(T)) for n,T in templates.items()]
 for name,tt in cases:
  kept=ns['edge_trim'](tt,np.ones(len(tt)))[0];checks=[]
  for e in ev:
   cov=ns['coverage'](kept,float(e['tc_btjd']),D,CAD);checks.append({'epoch':int(e['epoch']),'coverage':cov,'eligible':bool(cov[0]>=.9 and cov[1]>=.5 and cov[2]>=.5)})
  eligible=[x['epoch'] for x in checks if x['eligible']];old=next(x for x in saved if int(x['tic'])==tic and x['template']==name)
  rows.append({'tic':tic,'template':name,'basis':'DRN times independently transcribed from PDF Table 1' if name=='DRN145' else 'rounded saved template summary, NOT raw-data reconstruction','checks':checks,'eligible_epochs':eligible,'saved_eligible_epochs':old['eligible_epochs'],'count_matches_saved':len(eligible)==int(old['n_eligible']),'epochs_match_saved':' '.join(map(str,eligible))==old['eligible_epochs']})
r={'orbit_segments':segs,'max_orbit_DRN_difference_d':max(abs(x-y) for a,b in zip(segs,DRN) for x,y in zip(a,b)),'DRN_gaps':[DRN[i+1][0]-DRN[i][1] for i in range(3)],'inputs':inputs,'cases':rows,'timing_distances':{'24526743_e191_after_225b_DRN_d':4270.01197-DRN[1][0],'24526743_e192_after_226b_DRN_d':4284.79874-DRN[3][0],'160330868_e187_before_225b_end_DRN_d':DRN[1][1]-4275.77847,'160330868_e188_before_sector_end_DRN_d':DRN[3][1]-4290.71394,'160330868_e188_before_sector_end_orbit_d':segs[3][1]-4290.71394,'manual_exclude_even_share_d':2.03/4},'all_eligibility_counts_match':all(x['count_matches_saved'] and x['epochs_match_saved'] for x in rows)}
(A/'forecast_metadata_check.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:v for k,v in r.items() if k not in ['inputs','cases']},indent=2));print([(x['tic'],x['template'],x['eligible_epochs']) for x in rows])
