"""Unmodified official AnyCalib model on the first LaMAR2k CSV row.
Camera family is supplied as pinhole; this is not automatic model selection.
Official full-resolution metric function is executed unchanged via AST extraction.
"""
import argparse,ast,csv,hashlib,json,math,os,platform,resource,subprocess,time
from pathlib import Path
import numpy as np
import torch
from PIL import Image
from anycalib import AnyCalib
from anycalib.cameras import CameraFactory
from anycalib.cameras.base import BaseCamera
from anycalib.manifolds import Unit3
p=argparse.ArgumentParser();p.add_argument('--data-root',required=True);p.add_argument('--repo',required=True);p.add_argument('--outdir',required=True);p.add_argument('--index',type=int,default=0);p.add_argument('--threads',type=int,default=4);a=p.parse_args()
out=Path(a.outdir);out.mkdir(parents=True,exist_ok=True)
torch.set_num_threads(a.threads);torch.set_num_interop_threads(1);torch.manual_seed(0);np.random.seed(0)
rows=list(csv.DictReader((Path(a.data_root)/'images.csv').open()));row=rows[a.index];image_path=Path(a.data_root)/'images'/row['fname'];pil=Image.open(image_path).convert('RGB');w,h=pil.size
assert (w,h)==(int(float(row['width'])),int(float(row['height'])))
x=torch.from_numpy(np.asarray(pil).copy()).permute(2,0,1).float()/255
# This is the official CSV loader's pinhole convention: shared focal from vfov,
# principal point at image center, as no focal/px/py columns are provided here.
f=h/2/torch.tan(torch.tensor(float(row['vfov']),dtype=torch.float32)/2)
gt=torch.stack((f,f,torch.tensor(w/2),torch.tensor(h/2)))
manifest=dict(status='prepared',source_commit=subprocess.check_output(['git','-C',a.repo,'rev-parse','HEAD'],text=True).strip(),model='anycalib_gen',camera_family_supplied='pinhole',sample_index=a.index,selection='First row of official images.csv; no quality-based selection',sample_id=row['fname'],source_image_sha256=hashlib.file_digest(image_path.open('rb'),'sha256').hexdigest(),csv_row=row,original_size=[h,w],ground_truth_intrinsics=gt.tolist(),ground_truth_derivation='Official load_csv_openpano_format: fx=fy=(H/2)/tan(vfov/2), cx=W/2, cy=H/2',device='cpu',dtype='float32',threads=a.threads,python=platform.python_version(),torch_version=torch.__version__,seed=0,full_benchmark=False,automatic_camera_model_selection=False)
(out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');print(json.dumps(manifest),flush=True)
t=time.perf_counter();model=AnyCalib(model_id='anycalib_gen').to('cpu').eval();load_seconds=time.perf_counter()-t
print(f'Model loaded in {load_seconds:.3f}s',flush=True)
t=time.perf_counter()
with torch.inference_mode():pred=model.predict(x,cam_id='pinhole')
inference_seconds=time.perf_counter()-t
intrinsics=pred['intrinsics'];intrinsics=intrinsics[0] if isinstance(intrinsics,list) else intrinsics
raw={k:v.detach().cpu().numpy() for k,v in pred.items() if isinstance(v,torch.Tensor)};raw.update(intrinsics=intrinsics.numpy(),ground_truth_intrinsics=gt.numpy(),pred_size=np.array(pred['pred_size']))
np.savez_compressed(out/'raw_prediction.npz',**raw)
print('Inference completed; scoring official full-resolution metrics',flush=True)
metric_file=Path(a.repo)/'siclib/eval/simple_pipeline_rays.py';text=metric_file.read_text();node=next(n for n in ast.parse(text).body if isinstance(n,ast.FunctionDef) and n.name=='compute_metrics');function_source=ast.get_source_segment(text,node)
ns={'torch':torch,'BaseCamera':BaseCamera,'CameraFactory':CameraFactory,'Unit3':Unit3,'RAD2DEG':180/math.pi};exec(compile(function_source,str(metric_file),'exec'),ns)
cam=CameraFactory.create_from_id('pinhole');data=dict(scale_xy=torch.ones(2),shift_xy=torch.zeros(2),cam_id_gt='pinhole',intrinsics_gt=gt,original_image_size=torch.tensor([w,h]))
with torch.inference_mode():metrics=ns['compute_metrics']({'intrinsics':intrinsics},data,cam,[0.5,1,3,5])
report=dict(manifest,status='real_lamar_single_image_completed',parameters=sum(p.numel() for p in model.parameters()),pred_size=list(pred['pred_size']),intrinsics=intrinsics.tolist(),success=bool(pred['success'].item()),finite_intrinsics=bool(torch.isfinite(intrinsics).all()),finite_rays=bool(torch.isfinite(pred['rays']).all()),load_seconds=load_seconds,inference_seconds=inference_seconds,max_rss_mib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024,metrics=metrics,metric_function_sha256=hashlib.sha256(function_source.encode()).hexdigest(),evaluation_scope='Single real image, supplied known pinhole family; official metric function at original resolution. Not full benchmark, crop consistency, or unknown-camera model-selection evaluation')
(out/'result.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2),flush=True)
# Render real model field and a sampled view of the calibrated-camera GT error.
os.environ['MPLCONFIGDIR']=str(out/'mpl_cache')
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
hp,wp=pred['pred_size'];rgb=np.clip((pred['rays'].numpy().reshape(hp,wp,3)+1)/2,0,1)
ys=(torch.arange(192)+.5)*h/192;xs=(torch.arange(144)+.5)*w/144;coords=torch.stack(torch.meshgrid(xs,ys,indexing='xy'),dim=-1)
with torch.inference_mode():
 gt_rays,_=cam.unproject(gt,coords);fit_rays,_=cam.unproject(intrinsics,coords);errors=Unit3.distance(gt_rays,fit_rays).numpy()*180/math.pi
np.savez_compressed(out/'visualization_grid.npz',pixel_xy=coords.numpy(),calibrated_camera_angular_error_degrees=errors)
pil.thumbnail((480,640));pil.save(out/'input_thumbnail.png');Image.fromarray(np.uint8(rgb*255)).save(out/'network_rays_rgb.png')
fig,axes=plt.subplots(1,3,figsize=(12,6),layout='constrained');axes[0].imshow(pil);axes[0].set_title('Real LaMAR2k input');axes[1].imshow(rgb);axes[1].set_title('Predicted network ray field\nRGB=(x,y,z + 1)/2');im=axes[2].imshow(errors,cmap='magma',vmin=0);axes[2].set_title('Calibrated pinhole vs GT\nangular error (degrees)');fig.colorbar(im,ax=axes[2],shrink=.75)
for ax in axes:ax.axis('off')
fig.suptitle(f"Official AnyCalib-gen | {row['fname']} | CPU | single-image sample, not benchmark",fontsize=12)
fig.savefig(out/'real_calibration_demo.png',dpi=160);plt.close(fig)
