"""Run the unedited official main.py; a return-event observer saves its existing results.
No model, PCA, scoring, threshold, or metric function is replaced. Profiling only
adds observational overhead to timings. Single-category micro-test only.
"""
import os,sys,runpy,json,time,hashlib
from pathlib import Path
import numpy as np
import torch
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'sources/SubspaceAD/main.py'
OUT=ROOT/'outputs/subspacead_visa3'
OUT.mkdir(exist_ok=True)
torch.set_num_threads(4)
before=hashlib.sha256(SOURCE.read_bytes()).hexdigest()
def observe(frame,event,arg):
    if event=='return' and frame.f_code.co_name=='main' and Path(frame.f_code.co_filename).resolve()==SOURCE:
        loc=frame.f_locals
        if 'pro_anomaly_maps' not in loc:return
        arrays={k:np.asarray(loc[k]) for k in ['pro_anomaly_maps','pro_gt_masks','img_true','img_pred_auroc','px_pred_all_normalized','all_inference_times'] if k in loc}
        np.savez_compressed(OUT/'raw_predictions.npz',**arrays)
        params=loc.get('pca_params',{})
        if isinstance(params,dict):
            safe={k: v.detach().cpu().numpy() if torch.is_tensor(v) else v for k,v in params.items() if torch.is_tensor(v) or isinstance(v,np.ndarray)}
            np.savez_compressed(OUT/'pca_arrays.npz',**safe)
        metrics={k:float(loc[k]) if np.isfinite(loc[k]) else None for k in ['img_auroc','img_aupr','px_auroc','au_pro','img_f1','px_f1'] if k in loc}
        (OUT/'captured_result.json').write_text(json.dumps({'metrics':metrics,'train_paths':list(map(str,loc.get('train_paths',[]))),'test_paths':list(map(str,loc.get('test_paths',[]))),'test_image_scores':list(map(float,loc.get('img_pred_auroc',[]))),'test_inference_seconds':list(map(float,loc.get('all_inference_times',[]))),'actual_config':vars(loc['args']),'source_main_sha256':before,'capture':'Read-only Python profile return-event observer of official main locals; no algorithm function replaced. Timing includes observer overhead.'},indent=2)+'\n')
sys.path.insert(0,str(SOURCE.parent))
sys.argv=[str(SOURCE)]+sys.argv[1:]
os.chdir(SOURCE.parent)
sys.setprofile(observe)
try:runpy.run_path(str(SOURCE),run_name='__main__')
finally:sys.setprofile(None)
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==before
