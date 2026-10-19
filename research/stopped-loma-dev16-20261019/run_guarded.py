"""Run sequential capture and cached analysis under real-time resource limits."""
import os,sys,time,json,signal,subprocess,shutil,datetime
from pathlib import Path
R=Path(__file__).resolve().parent
# Restrict the whole run to four logical CPUs; children inherit this affinity.
allowed=sorted(os.sched_getaffinity(0));os.sched_setaffinity(0,set(allowed[:4]))
MAX_RSS=3*1024**3;MAX_OUTPUT=1024**3;MIN_FREE=2*1024**3;MAX_SECONDS=900
started=time.monotonic();initial=sum(p.stat().st_size for p in R.rglob('*')if p.is_file())
def size():return sum(p.stat().st_size for p in R.rglob('*')if p.is_file())
def rss(pid):
 try:
  for line in Path(f'/proc/{pid}/status').read_text().splitlines():
   if line.startswith('VmRSS:'):return int(line.split()[1])*1024
 except FileNotFoundError:return 0
 return 0
state={'status':'running','limits':{'rss_bytes':MAX_RSS,'incremental_output_bytes':MAX_OUTPUT,'min_disk_free_bytes':MIN_FREE,'wall_seconds':MAX_SECONDS},'stages':[],'cpu_affinity':sorted(os.sched_getaffinity(0))}
def save():
 tmp=R/'guard_resources.json.tmp';tmp.write_text(json.dumps(state,indent=2)+'\n');tmp.replace(R/'guard_resources.json')
for stage in ['diagnose_dev.py','analyze_cached_dev.py']:
 logfile=R/(stage+'.log');record={'script':stage,'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'max_rss_bytes':0,'stop_reason':None};state['stages'].append(record);save()
 with logfile.open('w')as log:
  p=subprocess.Popen([sys.executable,'-u',str(R/stage)],cwd=R,stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
  next_disk=0
  while p.poll()is None:
   used=rss(p.pid);record['max_rss_bytes']=max(record['max_rss_bytes'],used);reason=None
   if used>MAX_RSS:reason='RSS_LIMIT_EXCEEDED'
   if time.monotonic()-started>MAX_SECONDS:reason='WALL_LIMIT_EXCEEDED'
   if time.monotonic()>next_disk:
    next_disk=time.monotonic()+.5;increment=size()-initial;free=shutil.disk_usage(R).free
    state['incremental_output_bytes']=increment;state['disk_free_bytes']=free
    if increment>MAX_OUTPUT:reason='OUTPUT_LIMIT_EXCEEDED'
    if free<MIN_FREE:reason='DISK_FLOOR_CROSSED'
    save()
   if reason:
    record['stop_reason']=reason;os.killpg(p.pid,signal.SIGTERM)
    try:p.wait(timeout=5)
    except subprocess.TimeoutExpired:os.killpg(p.pid,signal.SIGKILL);p.wait()
    break
   time.sleep(.05)
  record['exit_code']=p.wait();record['finished_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();save()
 if record['exit_code']!=0:
  state['status']='stopped';save();print(json.dumps(state,indent=2));sys.exit(record['exit_code']or 1)
state['status']='completed';state['elapsed_seconds']=time.monotonic()-started;state['incremental_output_bytes']=size()-initial;save();print(json.dumps(state,indent=2))
