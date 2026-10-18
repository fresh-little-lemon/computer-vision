import json
from pathlib import Path
import numpy as np
from hardmatch.benchmark import fraction_of_gt_corrs_consisent_with_F
root=Path(__file__).resolve().parent.parent
results=[]
for run in ['loma_hardmatch_3','loma_hardmatch_official3']:
 folder=root/'outputs'/run;s=json.loads((folder/'summary.json').read_text());curves=[]
 for r in s['pairs']:
  d=np.load(folder/(r['files_prefix']+'.npz'))
  assert np.isfinite(d['matches_A']).all() and np.isfinite(d['matches_B']).all()
  assert len(d['matches_A'])==r['matches']
  curve=np.asarray(fraction_of_gt_corrs_consisent_with_F(d['F'],d['ground_truth_correspondences']))
  np.testing.assert_allclose(curve,d['fraction_curve'],rtol=0,atol=0)
  np.testing.assert_allclose(curve[:11].mean(),r['mAA_10px'],rtol=0,atol=1e-8)
  curves.append(curve)
 np.testing.assert_allclose(np.stack(curves).mean(0)[:11].mean(),s['mAA_10px'],rtol=0,atol=1e-8)
 results.append(dict(run=run,status='pass',samples=len(s['pairs']),recomputed_mAA_10px=float(np.stack(curves).mean(0)[:11].mean())))
print(json.dumps(results,indent=2))
(root/'logs/verify_loma_results.json').write_text(json.dumps(results,indent=2)+'\n')
