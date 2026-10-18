"""Scientific figures of saved real official scores, no synthetic image content."""
from pathlib import Path
import json,numpy as np
from PIL import Image
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
R=Path(__file__).resolve().parents[1];out=R/'outputs/subspacead_visa3'
d=np.load(out/'raw_predictions.npz');r=json.loads((out/'captured_result.json').read_text());maps=d['pro_anomaly_maps'];gt=d['pro_gt_masks'];vmin=float(maps.min());vmax=float(maps.max())
fig,axes=plt.subplots(2,3,figsize=(12,8.4),layout='constrained')
for i,path in enumerate(r['test_paths']):
 img=Image.open(path).convert('RGB').resize((224,224))
 axes[i,0].imshow(img);axes[i,1].imshow(gt[i],cmap='gray',vmin=0,vmax=1);im=axes[i,2].imshow(maps[i],cmap='inferno',vmin=vmin,vmax=vmax)
 for j in range(3):axes[i,j].axis('off')
 label='Anomaly 000.JPG' if d['img_true'][i] else 'Normal 0107.JPG'
 axes[i,0].set_title(label+' | real VisA');axes[i,1].set_title('Ground-truth mask');axes[i,2].set_title(f"Raw anomaly map | score {d['img_pred_auroc'][i]:.4f}")
 Image.fromarray(np.uint8(np.asarray(img))).save(out/f'test_{i}_input_clean.png')
 Image.fromarray(np.uint8(gt[i]*255)).save(out/f'test_{i}_gt_clean.png')
 heat=(plt.get_cmap('inferno')((maps[i]-vmin)/(vmax-vmin))[...,:3]*255).astype('uint8');Image.fromarray(heat).save(out/f'test_{i}_heatmap_clean.png')
 strip=np.concatenate([np.asarray(img),np.repeat((gt[i]*255)[...,None],3,axis=-1),heat],axis=1);Image.fromarray(strip).resize((1344,448)).save(out/f'test_{i}_three_panel_clean.png')
fig.colorbar(im,ax=axes[:,2],shrink=.85,label='Shared raw-score scale (both images)')
fig.suptitle('SubspaceAD official CPU variant: DINOv2-S / 224 / 1 training + 2 test images\nFixed CSV-first samples; evidence of execution only, not a benchmark claim',fontsize=13)
fig.savefig(out/'real_anomaly_demo.png',dpi=150);plt.close(fig)
Image.open(r['train_paths'][0]).convert('RGB').resize((448,448)).save(out/'train_reference_clean.png')
(out/'figure_manifest.json').write_text(json.dumps({'source_npz':'raw_predictions.npz','rows':['test bad 000.JPG','test good 0107.JPG'],'columns':['real input resized224','official GT nearest-resized224','official raw anomaly map inferno, same scale both images'],'common_color_limits':[vmin,vmax],'image_score':'Official mean of top1% raw anomaly pixels; not a calibrated probability','gt_positive_pixels':int(gt.sum()),'interpolation':'Input PIL default bicubic RGB resize for illustration; no changes to evaluated maps/GT','license':'VisA, Zou et al., 2022, CC BY4.0 https://github.com/amazon-science/spot-diff ; image crops not used, only resize, panel arrangement, score/GT visualization.'},indent=2)+'\n')
