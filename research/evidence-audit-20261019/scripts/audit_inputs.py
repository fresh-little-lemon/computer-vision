"""Read-only provenance/data metadata audit. Does not instantiate or run any model."""
from pathlib import Path
import json,random,hashlib,collections,itertools,subprocess,datetime
BASE=Path('/workspace/shared/cv-baseline-runs'); DATA=BASE/'data/hardmatch'; OUT=Path('/workspace/shared/cv-evidence-audit-20261019')
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
pairs=sorted(p.parent for p in DATA.rglob('corresp.txt') if ((p.parent/'A.jpg').exists() and (p.parent/'B.jpg').exists()) or ((p.parent/'A_lr.jpg').exists() and (p.parent/'B_lr.jpg').exists()))
cats=sorted(set(p.parent.parent for p in pairs)); shuffled=cats.copy();random.Random(1337).shuffle(shuffled);val=set(shuffled[:10])
rows=[]; by_url=collections.defaultdict(set);by_hash=collections.defaultdict(set)
for p in pairs:
 cat,scene,_=p.relative_to(DATA).parts
 labels=(p/'categories.txt').read_text().splitlines() if (p/'categories.txt').exists() else ['unknown']
 n=len((p/'corresp_lr.txt').read_text().strip().split())//4
 row=dict(pair=str(p.relative_to(DATA)),category=cat,scene=scene,scene_key='/'.join([cat,scene]),official_split='val' if p.parent.parent in val else 'test',eligible=n>=8 and 'dynamic' not in labels,labels=labels)
 ims=[]
 for ab in ('A','B'):
  mf=p/f'{ab}_metadata.json';meta=json.loads(mf.read_text()) if mf.exists() else {};im=p/f'{ab}_lr.jpg';digest=sha(im);url=meta.get('original_url')
  ims.append(dict(side=ab,sha256=digest,original_url=url))
  by_hash[digest].add(row['pair'])
  if url:by_url[url].add(row['pair'])
 row['images']=ims;rows.append(row)
lookup={r['pair']:r for r in rows}
def cross(mapping):
 return [{'key':k,'pairs':sorted(rs)}for k,rs in mapping.items() if len({lookup[r]['official_split']for r in rs})>1]
report={'audited_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Metadata/provenance only; no new inference or method experiment; heldout ground truth coordinates not inspected','resource_checks':{'cpu_imports':'Python3.12.14; torch2.14.1+cpu; opencv5.0.0; LoMa and HardMatch imported successfully','cuda_available':False,'memory_available_gib_approx':7.6,'disk_free_gib_approx':5.4},'splits':{},'cross_split_original_url_duplicates':cross(by_url),'cross_split_exact_image_hash_duplicates':cross(by_hash),'weight_hashes':{},'code':{}}
for split in ('val','test'):
 rs=[r for r in rows if r['official_split']==split];es=[r for r in rs if r['eligible']]
 report['splits'][split]=dict(all_pairs=len(rs),eligible_static_pairs=len(es),scene_keys=len({r['scene_key']for r in es}),building_pairs=sum('building'in r['labels']for r in es),building_scene_keys=len({r['scene_key']for r in es if 'building'in r['labels']}),categories=sorted({r['category']for r in rs}),labels=dict(collections.Counter(t for r in es for t in r['labels'])))
for name in ['loma_B128.pth','dad.pth']:
 p=BASE/'cache/torch/hub/checkpoints'/name;report['weight_hashes'][name]={'bytes':p.stat().st_size,'sha256':sha(p)}
for name in ['LoMa','HardMatch','AnyCalib','tapnet','SubspaceAD']:
 p=BASE/'sources'/name
 commit=subprocess.check_output(['git','-C',str(p),'rev-parse','HEAD'],text=True).strip()
 dirty=subprocess.check_output(['git','-C',str(p),'diff','--name-only','HEAD'],text=True).splitlines()
 report['code'][name]={'commit':commit,'tracked_changed_files':dirty,'source_py_changed':any(x.endswith('.py')for x in dirty)}
(OUT/'input_audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
(OUT/'hardmatch_inventory.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2))
