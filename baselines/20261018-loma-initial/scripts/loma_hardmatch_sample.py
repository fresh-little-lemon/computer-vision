"""Real HardMatch validation smoke with the official F/mAA scoring functions.

Prepared from official source, not executed by the author of this script.
Example:
  python loma_hardmatch_sample.py --data-root /path/to/hardmatch --out /path/to/out

Requires editable installs of LoMa and HardMatch. Uses existing extracted data;
does not download the dataset. LoMa initialization may fetch official weights.
Reduced square 224-pixel input and 256 keypoints are intentionally smoke-only.
"""
import argparse
import json
import time
import resource
from pathlib import Path

import cv2
import numpy as np
import torch
from PIL import Image, ImageDraw
from loma import LoMa, LoMaB128
from loma.device import device
from hardmatch.dataset import HardMatch
from hardmatch.geometry import to_pixel
from hardmatch.benchmark import (
    _symmetrical_epipolar_distance,
    fraction_of_gt_corrs_consisent_with_F,
)

p = argparse.ArgumentParser()
p.add_argument('--data-root', required=True)
p.add_argument('--out', required=True)
p.add_argument('--count', type=int, default=3)
p.add_argument('--side', type=int, default=224)
p.add_argument('--keypoints', type=int, default=256)
p.add_argument('--start', type=int, default=0)
p.add_argument('--threads', type=int, default=4)
p.add_argument('--official-preprocess', action='store_true')
a = p.parse_args()
assert a.side % 32 == 0 and a.count > 0
out = Path(a.out)
out.mkdir(parents=True, exist_ok=True)
torch.set_num_threads(a.threads)
torch.set_num_interop_threads(1)
torch.manual_seed(0)
np.random.seed(0)
cv2.setRNGSeed(0)
ds = HardMatch(HardMatch.Cfg(split='val', data_root=a.data_root, download=False))
model = LoMa(LoMaB128(num_keypoints=a.keypoints, compile=False, mp=(device.type != 'cpu')))
rows, curves = [], []

def tensor(im):
    arr = np.asarray(im.resize((a.side, a.side)), dtype=np.float32).copy()
    return torch.from_numpy(arr).permute(2, 0, 1)[None].div(255)

def sync():
    if device.type == 'cuda':
        torch.cuda.synchronize()

for index in range(a.start, len(ds)):
    if len(rows) >= a.count:
        break
    batch = ds[index]
    pair_dir = Path(batch.img_A_path).parent
    catfile = pair_dir / 'categories.txt'
    categories = catfile.read_text().splitlines() if catfile.exists() else ['unknown']
    if batch.correspondences_AB.shape[0] < 8 or 'dynamic' in categories:
        continue
    im0, im1 = (Image.open(x).convert('RGB') for x in (batch.img_A_path, batch.img_B_path))
    w0, h0 = im0.size
    w1, h1 = im1.size
    gt = torch.cat((to_pixel(batch.correspondences_AB[:, :2], H=h0, W=w0),
                    to_pixel(batch.correspondences_AB[:, 2:], H=h1, W=w1)), dim=-1).numpy().astype(np.float64)
    x0, x1 = tensor(im0), tensor(im1)
    sync()
    t0 = time.perf_counter()
    with torch.inference_mode():
        xy0_small, xy1_small = model.match(str(batch.img_A_path), str(batch.img_B_path)) if a.official_preprocess else model.match(x0, x1)
    sync()
    seconds = time.perf_counter() - t0
    # Official HardMatch LoMa adapter uses offset=0.0. Restore its pixel
    # coordinate convention from the square smoke grid to original file space.
    xy0 = xy0_small.astype(np.float64) * (1 if a.official_preprocess else np.array([w0/a.side, h0/a.side]))
    xy1 = xy1_small.astype(np.float64) * (1 if a.official_preprocess else np.array([w1/a.side, h1/a.side]))
    F, mask = None, None
    try:
        F, mask = cv2.findFundamentalMat(xy0, xy1, cv2.USAC_MAGSAC, 0.25, 0.999, 100000)
    except cv2.error:
        pass
    estimated = F is not None and np.asarray(F).shape == (3, 3)
    if not estimated:
        # Preserve the official benchmark fallback for metric compatibility,
        # and label it explicitly rather than presenting it as estimated F.
        F = np.array([[0., 0., 0.], [0., 0., -1.], [0., 1., 0.]])
    errors = _symmetrical_epipolar_distance(gt[None, :, :2], gt[None, :, 2:], F[None]).reshape(-1)
    curve = np.asarray(fraction_of_gt_corrs_consisent_with_F(F, gt))
    curves.append(curve)
    stem = f'{len(rows):02d}_val{index:03d}'
    np.savez_compressed(out / f'{stem}.npz', matches_A=xy0, matches_B=xy1,
                        matches_A_smoke=xy0_small, matches_B_smoke=xy1_small,
                        ground_truth_correspondences=gt, F=F,
                        gt_symmetric_epipolar_error_px=errors,
                        thresholds_px=np.arange(20), fraction_curve=curve,
                        ransac_inlier_mask=(np.asarray(mask).reshape(-1) if mask is not None else np.zeros(len(xy0), dtype=np.uint8)))
    im0.save(out / f'{stem}_A.png')
    im1.save(out / f'{stem}_B.png')
    canvas = Image.new('RGB', (w0+w1, max(h0,h1)))
    canvas.paste(im0, (0,0)); canvas.paste(im1, (w0,0))
    draw = ImageDraw.Draw(canvas)
    rng = np.random.default_rng(0)
    for (x,y),(u,v) in zip(xy0[:200],xy1[:200]):
        color = tuple(int(c) for c in rng.integers(40,255,3))
        draw.line([(float(x),float(y)),(float(u+w0),float(v))], fill=color, width=2)
    canvas.save(out / f'{stem}_matches.png')
    row = dict(index=index, pair=str(pair_dir.relative_to(Path(a.data_root))),
               categories=categories, matches=len(xy0), estimated_F=estimated,
               used_official_fallback_F=not estimated, match_seconds=seconds,
               mAA_10px=float(curve[:11].mean()),
               median_gt_epipolar_error_px=float(np.median(errors)),
               files_prefix=stem)
    rows.append(row)
    print(json.dumps(row, ensure_ascii=False), flush=True)

assert rows, 'No eligible static validation pairs found'
report = dict(status='sample_smoke_completed', split='val', samples=len(rows),
              variant='LoMaB128', side=None if a.official_preprocess else a.side, official_preprocess=a.official_preprocess, keypoints=a.keypoints, device=str(device),
              mAA_10px=float(np.stack(curves).mean(axis=0)[:11].mean()),
              scoring='Official HardMatch symmetric epipolar errors and mean fractions over thresholds 0..10px',
              note=('Official path preprocessing/2048-keypoint small validation sample' if a.official_preprocess else 'Reduced-resolution few-pair smoke') + '; not the 900-pair test benchmark or paper reproduction. No direct pointwise match-error ground truth is implied by this F evaluation.',
              torch_version=torch.__version__, opencv_version=cv2.__version__, threads=a.threads, max_rss_mib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024, pairs=rows)
(out / 'summary.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
print(json.dumps(report, ensure_ascii=False, indent=2))
