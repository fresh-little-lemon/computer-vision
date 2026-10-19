"""Read cached approved dev outputs in a separate process; never creates a model."""
from pathlib import Path
import gc,json,resource
import numpy as np
import torch,cv2
import diagnose_dev as d

def main():
 torch.set_num_threads(4);torch.set_num_interop_threads(1);cv2.setNumThreads(1)
 root=d.ROOT;dev=json.loads((root/'dev_only_manifest.json').read_text())['dev'];assert len(dev)==16
 assert json.loads((root/'observer_gate.json').read_text())['exact_matches_equal']
 assert json.loads((root/'progress.json').read_text())['status']=='captured_dev_only'
 d.event('analysis_started',script_sha256=d.sha(__file__),helper_sha256=d.sha(d.__file__),heldout_accessed=False)
 completed=[]
 for idx,entry in enumerate(dev):
  rawfile=root/'raw'/f'pair_{idx:02d}_capture.npz';meta=json.loads((root/'raw'/f'pair_{idx:02d}_meta.json').read_text())
  assert meta['pair']==entry['pair']and meta['raw_capture_sha256']==d.sha(rawfile)
  with np.load(rawfile)as z:
   xyA=z['keypoints_A_px'];xyB=z['keypoints_B_px'];scores=z['scores'][0];sim=z['sim'][0];gt=z['ground_truth_dev_only'];observedA=z['baseline_matches_A'];observedB=z['baseline_matches_B']
  e0=d.original_edges(scores,.1);assert np.array_equal(xyA[e0[:,0]],observedA)and np.array_equal(xyB[e0[:,1]],observedB)
  dA=np.linalg.norm(gt[:,None,:2]-xyA[None],axis=2);dB=np.linalg.norm(gt[:,None,2:]-xyB[None],axis=2)
  variants,selection_times,budgets,uncapped=d.build_variants(scores,sim);results={};edge_store={}
  for name,edges in variants.items():
   results[name]=d.evaluate(edges,xyA,xyB,gt,dA,dB);results[name]['selection_seconds']=selection_times[name]['wall_seconds'];results[name]['selection_cpu_seconds']=selection_times[name]['cpu_seconds'];edge_store[name]=edges
  raw_cov={f'top{k}':{str(r):d.recall_from_distances(e,dA,dB,r)for r in[1,3,5]}for k,e in uncapped.items()}
  np.savez_compressed(root/'raw'/f'pair_{idx:02d}_candidate_edges.npz',**edge_store)
  row={**meta,'analysis_max_rss_mib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024,'budget':budgets,'uncapped_candidate_recall':raw_cov,'variants':results}
  d.dump(root/'results'/f'pair_{idx:02d}.json',row);completed.append({'index':idx,'pair':entry['pair'],'status':'completed'})
  d.dump(root/'analysis_progress.json',{'status':'analyzing','completed':completed,'completed_count':len(completed),'total':16,'heldout_accessed':False,'updated_utc':d.utc()})
  d.event('pair_analyzed',index=idx,pair=entry['pair'],baseline_mAA10=results['B0']['mAA_10px'],baseline_matches=len(e0),reachable_GT3=results['B0']['recall']['3']['reachable_count'],retained_GT3=results['B0']['recall']['3']['retained_count'],analysis_max_rss_mib=row['analysis_max_rss_mib'])
  del xyA,xyB,scores,sim,gt,observedA,observedB,dA,dB,variants,results,edge_store,uncapped
  gc.collect()
 d.dump(root/'analysis_progress.json',{'status':'completed_dev_only','completed':completed,'completed_count':16,'total':16,'heldout_accessed':False,'updated_utc':d.utc()})
 d.event('analysis_completed',pairs=16,heldout_accessed=False,max_rss_mib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024)
if __name__=='__main__':
 try:main()
 except Exception as exc:d.event('analysis_failed',exception_type=type(exc).__name__,message=str(exc));raise
