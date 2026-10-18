"""Deterministic 3-image public VisA subset, followed by official preprocessing.
Select before any model inference; never select on result quality. Extract only
explicit data members, never tar.extractall(). Archive retained for SHA auditing.
"""
import csv,tarfile,pathlib,json,hashlib,subprocess,sys
R=pathlib.Path(__file__).resolve().parents[1]
archive=R/'downloads/VisA_20220922.tar'
with tarfile.open(archive) as t:
 m=next(m for m in t if m.name=='split_csv/1cls.csv')
 (R/'data/visa_1cls.csv').write_bytes(t.extractfile(m).read())
rows=list(csv.DictReader(open(R/'data/visa_1cls.csv'))); selected=[]
for split,label in [('train','normal'),('test','normal'),('test','anomaly')]:
 r=next(r for r in rows if r['object']=='pcb1' and r['split']==split and (r['label']=='normal')==(label=='normal'))
 selected.append(dict(r))
with open(R/'data/visa_micro.csv','w') as f:
 w=csv.DictWriter(f,fieldnames=list(selected[0]));w.writeheader();w.writerows(selected)
wanted={r[k] for r in selected for k in ['image','mask'] if r[k]}
with tarfile.open(archive) as t:
 for m in t:
  if m.name in wanted:
   assert not pathlib.PurePosixPath(m.name).is_absolute() and '..' not in pathlib.PurePosixPath(m.name).parts
   p=R/'data/visa_selected_raw'/m.name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(t.extractfile(m).read());wanted.remove(m.name)
  if not wanted:break
assert not wanted,wanted
for r in selected:
 for k in ['image','mask']:
  if r[k]:r[k+'_sha256']=hashlib.sha256((R/'data/visa_selected_raw'/r[k]).read_bytes()).hexdigest()
out=R/'outputs/subspacead_visa3';out.mkdir(exist_ok=True)
(out/'sample_selection.json').write_text(json.dumps({'rule':'First CSV row for pcb1 train normal, test normal, test anomaly, before model inference. No outcome-based selection.','samples':selected},indent=2)+'\n')
subprocess.run([sys.executable,str(R/'sources/SubspaceAD/tools/prepare_visa.py'),'--data-folder',str(R/'data/visa_selected_raw'),'--save-folder',str(R/'data/visa_micro'),'--split-file',str(R/'data/visa_micro.csv')],check=True)
print(json.dumps(selected,indent=2))
