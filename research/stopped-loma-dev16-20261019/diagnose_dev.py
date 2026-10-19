"""Frozen 16-scene dev diagnostic. No heldout access, training, or downloads.
All author source remains unmodified. Hooks observe detached copies only.
"""
import argparse,datetime,gc,hashlib,inspect,json,os,resource,shutil,sys,time
from pathlib import Path
import numpy as np
import torch
import cv2
from PIL import Image
from loma import LoMa,LoMaB128
from loma.loma import filter_matches,to_pixel_coords
from hardmatch.dataset import _parse_corresp_txt
from hardmatch.geometry import to_normalized,to_pixel
from hardmatch.benchmark import fraction_of_gt_corrs_consisent_with_F,_symmetrical_epipolar_distance

ROOT=Path(__file__).resolve().parent
BASE=Path('/workspace/shared/cv-baseline-runs')
DATA=BASE/'data/hardmatch'
FALLBACK=np.array([[0.,0.,0.],[0.,0.,-1.],[0.,1.,0.]])

def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def dump(path,obj):
 path=Path(path);tmp=path.with_suffix(path.suffix+'.tmp')
 tmp.write_text(json.dumps(obj,ensure_ascii=False,indent=2,allow_nan=False)+'\n');tmp.replace(path)
def event(kind,**kw):
 row={'utc':utc(),'event':kind,**kw};line=json.dumps(row,ensure_ascii=False,allow_nan=False)
 with (ROOT/'events.jsonl').open('a')as f:f.write(line+'\n');f.flush();os.fsync(f.fileno())
 print(line,flush=True)
def deny_download(*a,**kw):raise RuntimeError('Downloads forbidden: missing local checkpoint must be reported')

def original_edges(scores,threshold):
 m0,_,_,_=filter_matches(torch.from_numpy(scores[None]),threshold)
 ia=torch.where(m0[0]>=0)[0].numpy();ib=m0[0,ia].numpy()
 return np.stack([ia,ib],axis=1).astype(np.int64)

def sorted_edges(edges,scores):
 if len(edges)==0:return np.empty((0,2),dtype=np.int64)
 e=np.unique(np.asarray(edges,dtype=np.int64),axis=0)
 order=np.lexsort((e[:,1],e[:,0],-scores[e[:,0],e[:,1]]))
 return e[order]

def candidates(scores,k):
 n,m=scores.shape
 # Stable full sorting makes ties deterministic; candidate construction never reads GT.
 row=np.argsort(-scores,axis=1,kind='stable')[:,:k]
 col=np.argsort(-scores,axis=0,kind='stable')[:k,:]
 edges=np.concatenate([np.stack([np.repeat(np.arange(n),k),row.ravel()],1),np.stack([col.T.ravel(),np.repeat(np.arange(m),k)],1)])
 return sorted_edges(edges,scores)

def build_variants(scores,sim):
 variants={};timings={}
 for t in [0.1,0.01,0.03,0.05]:
  name='B0'if t==0.1 else f'threshold_{t:g}';start=time.perf_counter();cpu=time.process_time();variants[name]=original_edges(scores,t);timings[name]={"wall_seconds":time.perf_counter()-start,"cpu_seconds":time.process_time()-cpu}
 for temp in [0.5,1.,2.]:
  start=time.perf_counter();cpu=time.process_time();x=torch.from_numpy(sim[None])/temp
  ds=(torch.softmax(x,2)*torch.softmax(x,1))[0].numpy()
  if temp==1.:
   assert np.array_equal(ds,scores),'Temperature=1 must exactly reproduce author scores'
  variants[f'temperature_{temp:g}']=original_edges(ds,0.1);timings[f'temperature_{temp:g}']={'wall_seconds':time.perf_counter()-start,'cpu_seconds':time.process_time()-cpu}
  del x,ds
 m0=len(variants['B0']);K=min(2048,max(8,2*m0));ra=np.argmax(scores,axis=1);cb=np.argmax(scores,axis=0);ia=np.where(np.arange(len(ra))==cb[ra])[0];strict=np.stack([ia,ra[ia]],1)
 strictset=set(map(tuple,strict));raw={}
 for k in [1,2]:
  start=time.perf_counter();cpu=time.process_time();raw[k]=candidates(scores,k);build_seconds=time.perf_counter()-start;build_cpu=time.process_time()-cpu
  for mutual in [False,True]:
   start=time.perf_counter();cpu=time.process_time();e=raw[k]
   if mutual:e=np.asarray([pair for pair in e if tuple(pair)in strictset],dtype=np.int64).reshape(-1,2)
   name=f'top{k}_'+('mutual'if mutual else'free')
   variants[name]=e[:K].copy();timings[name]={'wall_seconds':build_seconds+time.perf_counter()-start,'cpu_seconds':build_cpu+time.process_time()-cpu}
 # Equal-count diagnostics at the minimum size of all four 2x2 cells.
 # Original B0 is never truncated or replaced.
 common=min(len(variants[f'top{k}_{mode}'])for k in [1,2]for mode in ['free','mutual'])
 for k in [1,2]:
  for mode in ['free','mutual']:
   name=f'top{k}_{mode}';start=time.perf_counter();cpu=time.process_time();variants[name+'_equal_count']=variants[name][:common].copy();timings[name+'_equal_count']={'wall_seconds':timings[name]['wall_seconds']+time.perf_counter()-start,'cpu_seconds':timings[name]['cpu_seconds']+time.process_time()-cpu}
 return variants,timings,{'budget_K':K,'baseline_matches':m0,'common_2x2_edge_count':common,'uncapped_top1_count':len(raw[1]),'uncapped_top2_count':len(raw[2])},raw

def recall_from_distances(edges,dA,dB,radius):
 reachable=(dA<=radius).any(1)&(dB<=radius).any(1)
 retained=np.zeros(len(dA),dtype=bool) if len(edges)==0 else ((dA[:,edges[:,0]]<=radius)&(dB[:,edges[:,1]]<=radius)).any(1)
 assert not (retained&~reachable).any()
 n=int(reachable.sum());r=int(retained.sum())
 return {'gt_count':len(dA),'reachable_count':n,'retained_count':r,'reachable_fraction':n/len(dA),'retained_fraction_all_gt':r/len(dA),'retention_given_reachable':r/n if n else None,'reachable_mask':reachable.tolist(),'retained_mask':retained.tolist()}

def evaluate(edges,xyA,xyB,gt,dA,dB):
 start=time.perf_counter();cpu=time.process_time();a=xyA[edges[:,0]];b=xyB[edges[:,1]]
 cv2.setRNGSeed(0);estimated=None;mask=None;error=None
 try:estimated,mask=cv2.findFundamentalMat(a,b,cv2.USAC_MAGSAC,0.25,0.999,100000)
 except cv2.error as exc:error=str(exc).splitlines()[0]
 valid=estimated is not None and np.asarray(estimated).shape==(3,3)and np.isfinite(estimated).all()
 F=estimated if valid else FALLBACK.copy();geo_seconds=time.perf_counter()-start;geo_cpu=time.process_time()-cpu
 curve=np.asarray(fraction_of_gt_corrs_consisent_with_F(F,gt))
 residual=_symmetrical_epipolar_distance(gt[None,:,:2],gt[None,:,2:],F[None]).reshape(-1)
 assert np.isfinite(curve).all()and np.isfinite(residual).all()
 metrics={'edge_count':len(edges),'estimated_F':bool(valid),'used_fallback_F':not bool(valid),'opencv_error':error,'F':F.tolist(),'ransac_inliers':int(mask.sum())if mask is not None else 0,'geometry_seconds':geo_seconds,'geometry_cpu_seconds':geo_cpu,'invalid_shape_or_nonfinite_F':bool(estimated is not None and not valid),'mAA_10px':float(curve[:11].mean()),'mAA_5px':float(curve[:6].mean()),'median_gt_epipolar_error_px':float(np.median(residual)),'fraction_curve':curve.tolist(),'gt_residuals_px':residual.tolist(),'recall':{str(r):recall_from_distances(edges,dA,dB,r)for r in [1,3,5]}}
 return metrics

class Capture:
 def __init__(self,model):self.model=model;self.values={};self.handles=[]
 def __enter__(self):
  def before(module,args):
   for name,t in zip(['keypoints_A_normalized','keypoints_B_normalized','descriptors_A','descriptors_B'],args):self.values[name]=t.detach().cpu().clone()
   return None
  def after(module,args,result):
   self.values['scores']=result[0].detach().cpu().clone();self.values['sim']=result[1].detach().cpu().clone()
   return None
  self.handles=[self.model.register_forward_pre_hook(before),self.model.log_assignment[-1].register_forward_hook(after)]
  return self
 def __exit__(self,*exc):
  for h in self.handles:h.remove()

def load_gt(pair,wA,hA,wB,hB):
 # Identical official parsing/normalization/denormalization; no full Dataset enumeration.
 raw=_parse_corresp_txt(pair/'corresp_lr.txt')
 normalized=torch.cat([to_normalized(raw[:,:2],H=hA,W=wA),to_normalized(raw[:,2:],H=hB,W=wB)],-1)
 return torch.cat([to_pixel(normalized[:,:2],H=hA,W=wA),to_pixel(normalized[:,2:],H=hB,W=wB)],-1).numpy().astype(np.float64)

def run():
 torch.set_num_threads(4);torch.set_num_interop_threads(1);cv2.setNumThreads(1);torch.manual_seed(0);np.random.seed(0);cv2.setRNGSeed(0)
 torch.hub.download_url_to_file=deny_download
 assert not torch.cuda.is_available(),'Protocol is CPU-only'
 data=json.loads((ROOT/'dev_only_manifest.json').read_text());dev=data['dev'];assert len(dev)==16
 assert len({r['group_id']for r in dev})==16 and all(r['official_split']=='val'for r in dev)
 for name in ['raw','results']: (ROOT/name).mkdir(exist_ok=True)
 assert not list((ROOT/'results').glob('pair_*.json')),'Do not overwrite an existing run'
 event('start',script_sha256=sha(__file__),dev_manifest_sha256=sha(ROOT/'dev_only_manifest.json'),pairs=16,heldout_accessed=False)
 start=time.perf_counter();model=LoMa(LoMaB128(num_keypoints=2048,compile=False,mp=False));event('model_loaded',seconds=time.perf_counter()-start)
 completed=[]
 for idx,entry in enumerate(dev):
  if shutil.disk_usage(ROOT).free<2*1024**3:raise RuntimeError('Disk remaining below 2GiB')
  pair=DATA/entry['pair'];ap=str(pair/'A_lr.jpg');bp=str(pair/'B_lr.jpg')
  with Image.open(ap)as im:wA,hA=im.size
  with Image.open(bp)as im:wB,hB=im.size
  cats=(pair/'categories.txt').read_text().splitlines()if(pair/'categories.txt').exists()else['unknown']
  gt=load_gt(pair,wA,hA,wB,hB);assert len(gt)>=8 and 'dynamic'not in cats
  event('pair_started',index=idx,pair=entry['pair'],stratum=entry['stratum'])
  if idx==0:
   t0=time.perf_counter();plain=model.match(ap,bp);plain_seconds=time.perf_counter()-t0
  t0=time.perf_counter();cpu0=time.process_time()
  with Capture(model)as capture:observed=model.match(ap,bp)
  match_seconds=time.perf_counter()-t0;match_cpu=time.process_time()-cpu0
  if idx==0:
   equality=all(np.array_equal(x,y)for x,y in zip(plain,observed));gate={'status':'pass'if equality else'fail','pair':entry['pair'],'observer_off_seconds':plain_seconds,'observer_on_seconds':match_seconds,'exact_matches_equal':equality,'shape_A':list(plain[0].shape),'shape_B':list(plain[1].shape),'off_A_sha256':hashlib.sha256(plain[0].tobytes()).hexdigest(),'on_A_sha256':hashlib.sha256(observed[0].tobytes()).hexdigest(),'off_B_sha256':hashlib.sha256(plain[1].tobytes()).hexdigest(),'on_B_sha256':hashlib.sha256(observed[1].tobytes()).hexdigest()}
   dump(ROOT/'observer_gate.json',gate);event('observer_gate',**gate);assert equality,'Observer changed baseline output; stop'
   del plain
  cap=capture.values
  assert set(cap)=={'keypoints_A_normalized','keypoints_B_normalized','descriptors_A','descriptors_B','scores','sim'}
  assert all(torch.isfinite(x).all()for x in cap.values())
  xyA=to_pixel_coords(cap['keypoints_A_normalized'],hA,wA)[0].numpy();xyB=to_pixel_coords(cap['keypoints_B_normalized'],hB,wB)[0].numpy()
  scores=cap['scores'][0].numpy();sim=cap['sim'][0].numpy()
  e0=original_edges(scores,.1)
  assert np.array_equal(xyA[e0[:,0]],observed[0])and np.array_equal(xyB[e0[:,1]],observed[1]),'Cached observer reconstructs wrong original matches'
  rawfile=ROOT/'raw'/f'pair_{idx:02d}_capture.npz'
  np.savez_compressed(rawfile,**{k:v.numpy()for k,v in cap.items()},keypoints_A_px=xyA,keypoints_B_px=xyB,baseline_matches_A=observed[0],baseline_matches_B=observed[1],ground_truth_dev_only=gt)
  event('raw_saved',index=idx,file=str(rawfile.relative_to(ROOT)),bytes=rawfile.stat().st_size,sha256=sha(rawfile))
  meta={'index':idx,'pair':entry['pair'],'scene_group':entry['group_id'],'stratum':entry['stratum'],'gt_count':len(gt),'model_match_seconds_with_observer':match_seconds,'model_match_cpu_seconds_with_observer':match_cpu,'model_matches_reconstructed_exactly':True,'max_rss_mib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024,'raw_capture_sha256':sha(rawfile)}
  dump(ROOT/'raw'/f'pair_{idx:02d}_meta.json',meta)
  completed.append({'index':idx,'pair':entry['pair'],'status':'captured'})
  dump(ROOT/'progress.json',{'status':'capturing','completed':completed,'completed_count':len(completed),'total':16,'heldout_accessed':False,'updated_utc':utc()})
  event('pair_captured',index=idx,pair=entry['pair'],baseline_matches=len(e0),max_rss_mib=meta['max_rss_mib'])
  del cap,capture,xyA,xyB,scores,sim,gt,observed
  gc.collect()
 dump(ROOT/'progress.json',{'status':'captured_dev_only','completed':completed,'completed_count':16,'total':16,'heldout_accessed':False,'updated_utc':utc()})
 event('capture_completed',pairs=16,heldout_accessed=False,max_rss_mib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024)

if __name__=='__main__':
 try:run()
 except Exception as exc:
  event('failed',exception_type=type(exc).__name__,message=str(exc));raise
