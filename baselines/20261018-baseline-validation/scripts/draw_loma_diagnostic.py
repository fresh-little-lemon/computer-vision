"""Readable diagnostic figures. Never changes inference or evaluation selection.
Prediction lines are neutral blue because sparse GT does not label each prediction.
Ground-truth correspondences are colored by residual to the predicted F.
"""
import json
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
root=Path(__file__).resolve().parent.parent;src=root/'outputs/loma_hardmatch_official3';out=root/'outputs/loma_ppt_diagnostics';out.mkdir(parents=True,exist_ok=True)
fontpath='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
try:font=ImageFont.truetype(fontpath,17);small=ImageFont.truetype(fontpath,13)
except OSError:font=small=ImageFont.load_default()
s=json.loads((src/'summary.json').read_text());reports=[]
for row in s['pairs']:
 stem=row['files_prefix'];data=np.load(src/(stem+'.npz'));a=Image.open(src/(stem+'_A.png')).convert('RGB');b=Image.open(src/(stem+'_B.png')).convert('RGB');scale=1200/(a.width+b.width);wa=round(a.width*scale);wb=1200-wa;h=max(round(a.height*scale),round(b.height*scale))
 base=Image.new('RGB',(1200,h),'#101722');base.paste(a.resize((wa,round(a.height*scale))));base.paste(b.resize((wb,round(b.height*scale))),(wa,0))
 indices=np.linspace(0,len(data['matches_A'])-1,min(30,len(data['matches_A'])),dtype=int)
 pred=base.copy();pd=ImageDraw.Draw(pred,'RGBA')
 def line(d,p,q,color):
  x,y=p*scale;u,v=q*scale;d.line((float(x),float(y),float(u+wa),float(v)),fill=color,width=2)
  for xx,yy in [(x,y),(u+wa,v)]:d.ellipse((xx-3,yy-3,xx+3,yy+3),fill=color)
 for i in indices:line(pd,data['matches_A'][i],data['matches_B'][i],(15,200,255,175))
 gt=base.copy();gd=ImageDraw.Draw(gt,'RGBA');err=data['gt_symmetric_epipolar_error_px'];pts=data['ground_truth_correspondences'];good=err<=10
 for p,e,ok in zip(pts,err,good):line(gd,p[:2],p[2:],(40,245,90,215) if ok else (255,55,60,215))
 canvas=Image.new('RGB',(1200,2*h+158),'#101722');d=ImageDraw.Draw(canvas)
 d.text((12,8),f"HardMatch val {row['index']} | LoMaB128 official preprocessing / 2048kp | mAA10={row['mAA_10px']:.4f}",font=font,fill='white')
 d.text((12,33),f"Predicted matches: {len(indices)} evenly spaced examples from {row['matches']} total; neutral blue, no per-match GT label",font=small,fill='#b5eaff')
 canvas.paste(pred,(0,56));d.text((12,h+66),f"Annotated correspondences: {len(pts)} total; residual to predicted F: green <=10px, red >10px (original-image pixels)",font=small,fill='white');canvas.paste(gt,(0,h+90))
 d.text((12,2*h+102),f"GT <=10px: {int(good.sum())}/{len(good)} | median GT epipolar residual: {np.median(err):.2f}px | no selection changed for evaluation",font=font,fill='white')
 d.text((12,2*h+130),row['pair']+' | Wikimedia attribution retained in checkpoint metadata',font=small,fill='#c4cad4')
 canvas.save(out/(stem+'_diagnostic.png'),optimize=True)
 reports.append(dict(pair=row['pair'],val_index=row['index'],predicted_total=row['matches'],displayed_prediction_indices=indices.tolist(),ground_truth_count=len(pts),ground_truth_within10=int(good.sum()),threshold_original_pixels=10,definition='Official symmetric epipolar residual of known GT correspondence to estimated F; not per-predicted-match correctness'))
(out/'figure_manifest.json').write_text(json.dumps(reports,indent=2)+'\n')
(out/'README.md').write_text('''# Readable LoMa diagnosis figures

Three unchanged, deterministically selected validation pairs; these are supplemental display figures. The original 200-line images and all raw predictions remain untouched.

Top: at most 30 evenly spaced predicted correspondences, drawn in neutral blue. No prediction is chosen based on quality. Bottom: all sparse ground-truth correspondences, colored by their official symmetric epipolar residual to the model-estimated F, green <=10 original-image pixels, red >10 pixels. These colors diagnose estimated geometry against real annotations; they are not ground-truth correctness labels for each predicted match. The display selection never changes evaluation.

Pair 0 is a real baseline failure (mAA10=0.062937, GT median residual44.27px), while pairs1/2 are better. No claimed new method or improvement is involved. The 3-pair sample is not a full benchmark.

Per-photo Wikimedia licenses and attribution remain in the LoMa official-preprocess checkpoint results. The pair0-derived image is CC BY-SA4.0; preserve credits, source links and license. See source checkpoint attribution.json.
''')
print(json.dumps(reports,indent=2))
