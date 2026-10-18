"""Official TAPNext++ inference on a disclosed real TAP-Vid DAVIS subset.
No network, architecture, weights, or matching/tracking logic is modified.
A truncated single-query clip is a smoke/measurement sample, not a benchmark.
"""
import argparse, ast, gc, hashlib, io, json, os, pickle, platform, resource, subprocess, time
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw
import torch
from tapnet.tapnextpp.votsp2026.model import TAPNextPP

p=argparse.ArgumentParser()
p.add_argument('--checkpoint',required=True)
p.add_argument('--data',required=True)
p.add_argument('--repo',required=True)
p.add_argument('--outdir',required=True)
p.add_argument('--frames',type=int,default=16)
p.add_argument('--threads',type=int,default=4)
p.add_argument('--sample',default=None)
a=p.parse_args()
out=Path(a.outdir);out.mkdir(parents=True,exist_ok=True)
torch.set_num_threads(a.threads);torch.set_num_interop_threads(1);torch.manual_seed(0);np.random.seed(0)
def save_json(name,data): (out/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
print('Loading official DAVIS pickle',flush=True)
with open(a.data,'rb') as f: dataset=pickle.load(f)
name=a.sample or sorted(dataset)[0]
sample=dataset[name]
video=sample['video']
occ=np.asarray(sample['occluded'],bool)
valid=np.flatnonzero(np.any(~occ,axis=1))
if not len(valid): raise ValueError('No visible query')
q=int(valid[0]);t0=int(np.flatnonzero(~occ[q])[0]);end=min(t0+a.frames,len(video))
frames=video[t0:end]
if isinstance(frames[0],bytes): frames=np.stack([np.asarray(Image.open(io.BytesIO(v)).convert('RGB')) for v in frames])
else: frames=np.array(frames,copy=True)
gt_normalized=np.array(sample['points'][q,t0:end],copy=True)
gt_occ=np.array(occ[q,t0:end],copy=True)
source_frames=len(video);source_queries=len(occ)
del dataset,sample,video,occ;gc.collect()
h,w=frames.shape[1:3];gt_xy=gt_normalized*np.array([w,h]);query=gt_xy[0:1].astype(np.float32)
manifest=dict(status='prepared',video=name,source_frame_start=t0,source_frame_stop_exclusive=end,source_total_frames=source_frames,query_index=q,source_query_count=source_queries,source_resolution=[h,w],model_resolution=[256,256],frames=len(frames),queries=1,query_xy=query.tolist(),device='cpu',dtype='float32',threads=a.threads,seed=0,torch_version=torch.__version__,python=platform.python_version(),algorithm='TAPNextPP.from_checkpoint + track_frame, unmodified official code',sample_selection='Alphabetically first video, first query with any visibility, first visible frame',benchmark_claim=False,source_commit=subprocess.check_output(['git','-C',a.repo,'rev-parse','HEAD'],text=True).strip())
save_json('manifest.json',manifest)
print(json.dumps(manifest),flush=True)
load0=time.perf_counter();model=TAPNextPP.from_checkpoint(a.checkpoint,device='cpu',input_resolution=256);load_seconds=time.perf_counter()-load0
print(f'Loaded official model in {load_seconds:.3f}s; params={sum(x.numel() for x in model.parameters())}',flush=True)
state=None;timings=[];tracks=[];visibility=[]
with torch.inference_mode():
 for i,frame in enumerate(frames):
  t=time.perf_counter();xy,vis,state=model.track_frame(np.ascontiguousarray(frame[...,::-1]),query if state is None else None,state=state)
  elapsed=time.perf_counter()-t
  timings.append(elapsed);tracks.append(xy[0].tolist());visibility.append(bool(vis[0]))
  row=dict(local_frame=i,source_frame=t0+i,pred_xy=xy[0].tolist(),pred_visible=bool(vis[0]),ground_truth_xy=gt_xy[i].tolist(),ground_truth_occluded=bool(gt_occ[i]),seconds=elapsed)
  with (out/'per_frame.jsonl').open('a') as f:f.write(json.dumps(row)+'\n')
  print(json.dumps(row),flush=True)
tracks=np.asarray(tracks);visibility=np.asarray(visibility)
np.savez_compressed(out/'raw_predictions.npz',pred_xy=tracks,pred_visible=visibility,gt_xy=gt_xy,gt_occluded=gt_occ,source_frame_indices=np.arange(t0,end),query_xy=query)
# Execute the official pure-NumPy metric function unchanged, avoiding unrelated TF dataset imports.
metric_file=Path(a.repo)/'tapnet/tapvid/evaluation_datasets.py'
metric_text=metric_file.read_text();tree=ast.parse(metric_text)
node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='compute_tapvid_metrics')
function_source=ast.get_source_segment(metric_text,node)
namespace={'np':np,'Mapping':dict}
exec(compile(function_source,str(metric_file),'exec'),namespace)
metrics=namespace['compute_tapvid_metrics'](query_points=np.array([[[0,query[0,1]*256/h,query[0,0]*256/w]]]),gt_occluded=gt_occ[None,None],gt_tracks=(gt_xy*[256/w,256/h])[None,None],pred_occluded=(~visibility)[None,None],pred_tracks=(tracks*[256/w,256/h])[None,None],query_mode='first')
metrics={k:float(v[0]) for k,v in metrics.items()}
result=dict(manifest,status='real_davis_sample_completed',load_seconds=load_seconds,inference_seconds=sum(timings),first_frame_seconds=timings[0],subsequent_mean_seconds=float(np.mean(timings[1:])),per_frame_seconds=timings,parameters=sum(x.numel() for x in model.parameters()),max_rss_mib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024,finite=bool(np.isfinite(tracks).all()),metrics=metrics,metrics_scope='One query, truncated clip; initial query frame excluded by official first-query metric; not comparable to full DAVIS benchmark',metric_function_sha256=hashlib.sha256(function_source.encode()).hexdigest())
save_json('result.json',result)
indices=sorted(set([0,len(frames)//3,2*len(frames)//3,len(frames)-1]))
canvas=Image.new('RGB',(512*2,320*2),'#101722');d=ImageDraw.Draw(canvas)
for panel,i in enumerate(indices):
 im=Image.fromarray(frames[i]).resize((512,256));draw=ImageDraw.Draw(im)
 for xy,col in [(gt_xy[i],'#22ff77'),(tracks[i],'#ff4444')]:
  x,y=xy*[512/w,256/h];draw.ellipse((x-5,y-5,x+5,y+5),outline=col,width=3)
 x=(panel%2)*512;y=(panel//2)*320;canvas.paste(im,(x,y));d.text((x+8,y+260),f'{name}: frame {t0+i} | query {q}',fill='white');d.text((x+8,y+278),f'GT green (occ={bool(gt_occ[i])}) / prediction red (vis={bool(visibility[i])})',fill='white')
d.text((8,622),'Real TAP-Vid DAVIS subset | official TAPNext++ | CPU 256x256 | not full benchmark',fill='white')
canvas.save(out/'real_tracking_demo.png')
print(json.dumps(result,indent=2),flush=True)
