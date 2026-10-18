import ast,hashlib,json,logging
from pathlib import Path
import numpy as np
from scipy.ndimage import label as cc_label,generate_binary_structure
from sklearn.metrics import roc_auc_score,average_precision_score
ROOT=Path(__file__).resolve().parents[1];out=ROOT/'outputs/subspacead_visa3'
source=(ROOT/'sources/SubspaceAD/main.py').read_text();node=next(n for n in ast.parse(source).body if isinstance(n,ast.FunctionDef) and n.name=='compute_aupro');fn=ast.get_source_segment(source,node)
exec(compile(ast.Module(body=[node],type_ignores=[]),'official_compute_aupro','exec'))
d=np.load(out/'raw_predictions.npz');r=json.loads((out/'captured_result.json').read_text())
actual={'img_auroc':roc_auc_score(d['img_true'],d['img_pred_auroc']),'img_aupr':average_precision_score(d['img_true'],d['img_pred_auroc']),'px_auroc':roc_auc_score(d['pro_gt_masks'].ravel(),d['pro_anomaly_maps'].ravel()),'au_pro':compute_aupro(list(d['pro_anomaly_maps']),list(d['pro_gt_masks']),fpr_limit=.3,num_thresholds=300,connectivity=8)}
report={'passed':all(np.isclose(actual[k],r['metrics'][k],rtol=0,atol=1e-12) for k in actual),'recomputed':{k:float(v) for k,v in actual.items()},'recorded':r['metrics'],'official_compute_aupro_sha256':hashlib.sha256(fn.encode()).hexdigest(),'test_positive_pixels':int(d['pro_gt_masks'].sum()),'test_total_pixels':int(d['pro_gt_masks'].size),'finite_anomaly_maps':bool(np.isfinite(d['pro_anomaly_maps']).all()),'source':'Official unchanged compute_aupro and sklearn roc_auc_score/average_precision_score; saved NPZ only; no model rerun.'}
(ROOT/'logs/verify_subspacead_results.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2));assert report['passed']
