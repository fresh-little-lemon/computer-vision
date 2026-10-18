"""Single-pair LoMa smoke, prepared from official API; execution pending.

Run from cloned LoMa root, with its editable package installed:
  python /path/to/loma_smoke.py --variant b128 --side 224 --keypoints 256
Reduced-resolution GPU smoke:
  python /path/to/loma_smoke.py --variant b --side 448 --keypoints 2048

The reduced tensor resolution is a smoke configuration, not a benchmark score.
"""
import argparse
import json
import time
from pathlib import Path

import numpy as np
import torch
from PIL import Image, ImageDraw
from loma import LoMa, LoMaB, LoMaB128
from loma.device import device

p = argparse.ArgumentParser()
p.add_argument('--variant', choices=['b', 'b128'], default='b128')
p.add_argument('--side', type=int, default=224)
p.add_argument('--keypoints', type=int, default=256)
p.add_argument('--left', default='assets/toronto_A.jpg')
p.add_argument('--right', default='assets/toronto_B.jpg')
p.add_argument('--out', default='loma_smoke.json')
a = p.parse_args()
torch.set_num_threads(4)
torch.set_num_interop_threads(1)
assert a.side % 32 == 0, 'Use a side divisible by 32, e.g. 224 or 768'
if a.variant == 'b':
    assert a.side % 14 == 0, 'DINOv2 also requires divisibility by 14; use 224, 448 or 896'
cfg = (LoMaB128 if a.variant == 'b128' else LoMaB)(num_keypoints=a.keypoints, compile=False, mp=(device.type != 'cpu'))
t0 = time.perf_counter()
model = LoMa(cfg)
load_s = time.perf_counter() - t0

def read(path):
    im = Image.open(path).convert('RGB').resize((a.side, a.side))
    return torch.from_numpy(np.asarray(im).copy()).permute(2, 0, 1).float()[None].div(255)

left, right = read(a.left), read(a.right)
if device.type == 'cuda':
    torch.cuda.reset_peak_memory_stats()
    torch.cuda.synchronize()
t0 = time.perf_counter()
with torch.inference_mode():
    xy0, xy1 = model.match(left, right)
if device.type == 'cuda':
    torch.cuda.synchronize()
elapsed = time.perf_counter() - t0
assert xy0.shape == xy1.shape and xy0.ndim == 2 and xy0.shape[1] == 2
assert np.isfinite(xy0).all() and np.isfinite(xy1).all()
report = dict(status='smoke_completed', device=str(device), variant=a.variant,
              input_side=a.side, keypoints=a.keypoints, matches=len(xy0),
              load_seconds=load_s, first_pair_seconds=elapsed,
              torch_version=torch.__version__,
              note='No ground-truth accuracy measured. Single cold pair; not steady-state latency.')
if device.type == 'cuda':
    report['peak_allocated_bytes'] = torch.cuda.max_memory_allocated()
out = Path(a.out)
out.parent.mkdir(parents=True,exist_ok=True)
np.savez_compressed(out.with_suffix('.npz'), matches_A=xy0, matches_B=xy1)
canvas=Image.new('RGB',(a.side*2,a.side+36),'#101722')
canvas.paste(Image.open(a.left).convert('RGB').resize((a.side,a.side)),(0,0))
canvas.paste(Image.open(a.right).convert('RGB').resize((a.side,a.side)),(a.side,0))
draw=ImageDraw.Draw(canvas);rng=np.random.default_rng(0)
for (x,y),(u,v) in zip(xy0,xy1):
    color=tuple(int(c) for c in rng.integers(40,255,3))
    draw.line([(float(x),float(y)),(float(u+a.side),float(v))],fill=color,width=1)
draw.text((6,a.side+5),f'Official LoMa {a.variant}: {len(xy0)} real matches | demo only',fill='white')
canvas.save(out.with_suffix('.png'))
out.write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
