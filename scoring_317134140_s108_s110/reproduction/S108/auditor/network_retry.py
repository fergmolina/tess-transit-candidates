from pathlib import Path
import json,datetime,urllib.request,urllib.parse,hashlib,traceback,subprocess
A=Path('/Users/fernando/Desktop/NASA/results/reproduction_317134140_S108_auditor');T=Path(json.loads((A/'audit_plan.json').read_text())['temp_directory'])
name='tess2026250081459-s0108-0000000317134140-0310-s_lc.fits';p=A/'lc'/name
url='https://mast.stsci.edu/api/v0.1/Download/file?'+urllib.parse.urlencode({'uri':'mast:TESS/product/'+name})
r={'start_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'url':url,'destination':str(p),'attempt':2,'sandbox':'network escalation'}
assert not (A/'download_attempt2.json').exists() and not p.exists()
try:
 with urllib.request.urlopen(url,timeout=40) as response,p.open('xb') as f:
  r.update(http_status=response.status,final_url=response.url,headers={k:response.headers.get(k) for k in ['Content-Type','Content-Length','ETag','Last-Modified']})
  while True:
   b=response.read(1024*1024)
   if not b:break
   f.write(b)
 r.update(bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest());r['hash_matches_record']=r['sha256']=='cea2619b6228e770064ed39176ad446c02320311dbd3751e15cdc0876b4331a0'
except Exception as e:r['exception']=repr(e);r['traceback']=traceback.format_exc()
r['end_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();(A/'download_attempt2.json').write_text(json.dumps(r,indent=2)+'\n');print('DOWNLOAD',json.dumps({k:v for k,v in r.items() if k!='traceback'}),flush=True)
args=[str(T/'venv/bin/python'),'-B','-m','pip','--disable-pip-version-check','--cache-dir',str(T/'pip_cache'),'install','--index-url','https://pypi.org/simple','numpy==2.5.4','scipy==1.18.1','astropy==8.0.2','wotan==2.0']
start=datetime.datetime.now(datetime.timezone.utc).isoformat()
with (A/'env_install_retry.log').open('xb') as log:
 log.write(('COMMAND '+json.dumps(args)+'\nSTART '+start+'\n').encode());log.flush();proc=subprocess.run(args,stdout=log,stderr=subprocess.STDOUT);end=datetime.datetime.now(datetime.timezone.utc).isoformat();log.write(('\nEND '+end+' EXIT '+str(proc.returncode)+'\n').encode())
with (A/'attempts.jsonl').open('a') as f:f.write(json.dumps(dict(label='env_install_retry',command=args,start_utc=start,end_utc=end,exit_code=proc.returncode))+'\n')
print('INSTALL_EXIT',proc.returncode,flush=True)
