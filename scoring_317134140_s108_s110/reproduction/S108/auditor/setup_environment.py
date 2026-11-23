import subprocess,json,datetime,sys
from pathlib import Path
A=Path(sys.argv[1]);T=Path(sys.argv[2])
def run(label,args):
 start=datetime.datetime.now(datetime.timezone.utc).isoformat()
 with (A/(label+'.log')).open('xb') as log:
  log.write(('COMMAND '+json.dumps(args)+'\nSTART '+start+'\n').encode());log.flush()
  p=subprocess.run(args,stdout=log,stderr=subprocess.STDOUT)
  end=datetime.datetime.now(datetime.timezone.utc).isoformat();log.write(('\nEND '+end+' EXIT '+str(p.returncode)+'\n').encode())
 with (A/'attempts.jsonl').open('a') as f:f.write(json.dumps(dict(label=label,command=args,start_utc=start,end_utc=end,exit_code=p.returncode))+'\n')
 print(label,p.returncode,flush=True);return p.returncode
if run('env_create',['/opt/homebrew/bin/python3.12','-B','-m','venv',str(T/'venv')]):sys.exit(1)
sys.exit(run('env_install',[str(T/'venv/bin/python'),'-B','-m','pip','--disable-pip-version-check','--cache-dir',str(T/'pip_cache'),'install','--index-url','https://pypi.org/simple','numpy==2.5.4','scipy==1.18.1','astropy==8.0.2','wotan==2.0']))
