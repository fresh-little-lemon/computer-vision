from pathlib import Path
import importlib.util
import numpy as np
import torch
p=Path(__file__).with_name('diagnose_dev.py');spec=importlib.util.spec_from_file_location('d',p);d=importlib.util.module_from_spec(spec);spec.loader.exec_module(d)
# Deterministic ties for row/column top-2 union, excluding only (2,2).
s=np.ones((3,3),dtype=np.float32);e=d.candidates(s,2)
assert e.tolist()==[[i,j]for i in range(3)for j in range(3)if(i,j)!=(2,2)]
assert d.original_edges(s,1.1).shape==(0,2)
# Every retained GT must first be detector-reachable; unreachable denominator is excluded.
da=np.array([[0.,10.],[10.,0.],[20.,20.]]);db=da.copy();r=d.recall_from_distances(np.array([[0,0]]),da,db,3)
assert r['reachable_count']==2 and r['retained_count']==1 and r['retention_given_reachable']==.5
assert d.recall_from_distances(np.empty((0,2),int),da,db,3)['retained_count']==0
# Correct dtype and reconstruction for the temperature=1 control.
sim=torch.tensor([[[3.,1.,-1.],[0.,5.,0.],[-2.,1.,4.]]]);scores=(sim.softmax(2)*sim.softmax(1))[0].numpy()
v,t,b,raw=d.build_variants(scores,sim[0].numpy());assert np.array_equal(v['B0'],v['temperature_1'])
assert len({len(v[k])for k in v if k.endswith('equal_count')})==1
# Verify selected-dev GT read path matches the already published raw baseline arrays exactly.
pair=d.DATA/'bell_tower/Denny_Chimes/pair_00052'
from PIL import Image
with Image.open(pair/'A_lr.jpg')as im:wa,ha=im.size
with Image.open(pair/'B_lr.jpg')as im:wb,hb=im.size
gt=d.load_gt(pair,wa,ha,wb,hb)
old=np.load(d.BASE/'outputs/loma_hardmatch_official3/01_val001.npz')
assert np.array_equal(gt,old['ground_truth_correspondences'])
curve=np.asarray(d.fraction_of_gt_corrs_consisent_with_F(old['F'],gt));assert np.array_equal(curve,old['fraction_curve'])
print('PASS: deterministic candidate ties, empty matches, reachable-GT recall, temperature identity, count-matched cells, official dev-GT path, official metric recomputation')
