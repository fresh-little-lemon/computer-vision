"""Single real-image inference smoke; no benchmark metrics or accuracy claim."""
import argparse
import json
import resource
import time
from pathlib import Path

import numpy as np
import torch
from PIL import Image
from anycalib import AnyCalib

p = argparse.ArgumentParser()
p.add_argument('--image', required=True)
p.add_argument('--model', default='anycalib_gen')
p.add_argument('--camera', default='pinhole')
p.add_argument('--threads', type=int, default=4)
p.add_argument('--out', default='anycalib_smoke.json')
a = p.parse_args()
torch.set_num_threads(a.threads)
x = np.asarray(Image.open(a.image).convert('RGB')).copy()
x = torch.from_numpy(x).permute(2, 0, 1).float() / 255
t0 = time.perf_counter()
model = AnyCalib(model_id=a.model).to('cpu').eval()
load_seconds = time.perf_counter() - t0
t0 = time.perf_counter()
with torch.inference_mode():
    out = model.predict(x, cam_id=a.camera)
elapsed = time.perf_counter() - t0
intrinsics = out['intrinsics']
if isinstance(intrinsics, list):
    intrinsics = intrinsics[0]
report = {
    'status': 'inference_completed', 'image': str(Path(a.image).resolve()),
    'model': a.model, 'camera': a.camera, 'device': 'cpu',
    'image_shape': list(x.shape), 'pred_size': list(out['pred_size']),
    'intrinsics': intrinsics.detach().cpu().tolist(),
    'finite_intrinsics': bool(torch.isfinite(intrinsics).all()),
    'finite_rays': bool(torch.isfinite(out['rays']).all()),
    'success': bool(out['success'].item()),
    'load_seconds_including_download_if_uncached': load_seconds,
    'single_inference_seconds': elapsed,
    'peak_rss_mib_linux': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024,
    'torch_version': torch.__version__, 'threads': a.threads,
    'evaluation_scope': 'single image smoke; not accuracy reproduction'
}
Path(a.out).write_text(json.dumps(report, indent=2, ensure_ascii=False))
print(json.dumps(report, indent=2, ensure_ascii=False))
