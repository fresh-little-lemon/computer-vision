import gc,json,pickle
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
root=Path(__file__).resolve().parent.parent;out=root/'outputs/tapnextpp_davis16';pred=np.load(out/'raw_predictions.npz');r=json.loads((out/'result.json').read_text())
with (root/'data/tapvid_davis/tapvid_davis.pkl').open('rb') as f:ds=pickle.load(f)
idx=[0,5,10,15];frames=np.array(ds[r['video']]['video'][idx],copy=True);del ds;gc.collect()
canvas=Image.new('RGB',(1456,768));
for k,i in enumerate(idx):
 im=Image.fromarray(frames[k]).resize((728,384));d=ImageDraw.Draw(im)
 gx,gy=pred['gt_xy'][i]*.8;px,py=pred['pred_xy'][i]*.8
 d.line((gx-8,gy,gx+8,gy),fill='#20ff68',width=3);d.line((gx,gy-8,gx,gy+8),fill='#20ff68',width=3)
 d.ellipse((px-5,py-5,px+5,py+5),outline='#ff3030',width=3)
 canvas.paste(im,((k%2)*728,(k//2)*384))
 if i==0:im.save(out/'frame0_tracking_clean.png');Image.fromarray(frames[k]).save(out/'frame0_source_clean.png')
canvas.save(out/'tracking_four_frames_clean.png',optimize=True)
(out/'clean_figures_manifest.json').write_text(json.dumps(dict(video=r['video'],source_frame_indices=idx,query_index=0,gt_marker='green cross',prediction_marker='red circle',layout='2x2 row-major:0,5,10,15',source='Official TAP-Vid DAVIS archive',original_video='https://www.youtube.com/watch?v=2JMcuDkvX8I',original_video_provenance='Official archive tapvid_davis/SOURCES.md',annotation_license='CC BY 4.0',video_license='Original video owned by its creator; official TAPNet README states DAVIS source videos have creator-specific Creative Commons licenses. No exact YouTube license variant independently reverified.',scope='Research result illustration, not dataset or video redistribution'),indent=2)+'\n')
print('Clean TAPNext figures ready')
