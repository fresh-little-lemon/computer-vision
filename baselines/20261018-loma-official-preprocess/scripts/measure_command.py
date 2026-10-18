import datetime,json,resource,subprocess,sys,time
from pathlib import Path
out=Path(sys.argv[1]);command=sys.argv[2:]
start=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.perf_counter()
ret=subprocess.run(command)
r=resource.getrusage(resource.RUSAGE_CHILDREN)
report=dict(command=command,started_utc=start,finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),elapsed_seconds=time.perf_counter()-t,exit_code=ret.returncode,max_rss_mib=r.ru_maxrss/1024,user_cpu_seconds=r.ru_utime,system_cpu_seconds=r.ru_stime)
out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2));sys.exit(ret.returncode)
