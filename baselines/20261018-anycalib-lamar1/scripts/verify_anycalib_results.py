import ast,json,math
from pathlib import Path
import numpy as np
import torch
from anycalib.cameras import CameraFactory
from anycalib.cameras.base import BaseCamera
from anycalib.manifolds import Unit3
root=Path(__file__).resolve().parent.parent;out=root/'outputs/anycalib_lamar1';r=json.loads((out/'result.json').read_text());d=np.load(out/'raw_prediction.npz');torch.set_num_threads(4)
file=root/'sources/AnyCalib/siclib/eval/simple_pipeline_rays.py';text=file.read_text();node=next(x for x in ast.parse(text).body if isinstance(x,ast.FunctionDef) and x.name=='compute_metrics');ns={'torch':torch,'BaseCamera':BaseCamera,'CameraFactory':CameraFactory,'Unit3':Unit3,'RAD2DEG':180/math.pi};exec(compile(ast.get_source_segment(text,node),str(file),'exec'),ns)
h,w=r['original_size'];data=dict(scale_xy=torch.ones(2),shift_xy=torch.zeros(2),cam_id_gt='pinhole',intrinsics_gt=torch.from_numpy(d['ground_truth_intrinsics']),original_image_size=torch.tensor([w,h]))
with torch.inference_mode():calc=ns['compute_metrics']({'intrinsics':torch.from_numpy(d['intrinsics'])},data,CameraFactory.create_from_id('pinhole'),[0.5,1,3,5])
for k,v in calc.items():np.testing.assert_allclose(v,r['metrics'][k],rtol=0,atol=0)
assert np.isfinite(d['rays']).all() and np.isfinite(d['intrinsics']).all()
report=dict(status='pass',sample=r['sample_id'],checks=['All official metrics independently recomputed exactly from saved NPZ','Raw rays and intrinsics finite','Fixed first official CSV row retained; no performance-based sample choice'],metrics=calc)
(root/'logs/verify_anycalib_results.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
