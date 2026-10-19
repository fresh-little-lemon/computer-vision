"""Propose a deterministic grouped pilot split from metadata only; does not evaluate it."""
from pathlib import Path
import json,hashlib,collections
O=Path('/workspace/shared/cv-evidence-audit-20261019');rows=json.loads((O/'hardmatch_inventory.json').read_text());lookup={r['pair']:r for r in rows};parent={r['pair']:r['pair']for r in rows}
def find(x):
 while parent[x]!=x:parent[x]=parent[parent[x]];x=parent[x]
 return x
def union(a,b):
 a,b=find(a),find(b)
 if a!=b:parent[max(a,b)]=min(a,b)
links={}
for r in rows:
 keys=['scene:'+r['scene_key']]
 for im in r['images']:
  keys.append('image:'+im['sha256'])
  if im['original_url']:keys.append('url:'+im['original_url'])
 for k in keys:
  if k in links:union(r['pair'],links[k])
  else:links[k]=r['pair']
groups=collections.defaultdict(list)
for r in rows:groups[find(r['pair'])].append(r)
seed='cv-loma-pilot-20261019-v1'
def key(s):return hashlib.sha256((seed+'|'+s).encode()).hexdigest()
known=['bell_tower/Bell_tower_of_the_church_of_the_Intercession,_Lozova/pair_00058','bell_tower/Denny_Chimes/pair_00052','bell_tower/Denny_Chimes/pair_00053']
forced={find(p) for p in known};groups_ready=[];excluded=[]
for g,rs in groups.items():
 eligible=[r for r in rs if r['eligible']]
 if not eligible:continue
 if len({r['official_split']for r in rs})!=1:excluded.append(g);continue
 building=[r for r in eligible if 'building'in r['labels']]
 candidates=building or eligible
 representative=sorted(candidates,key=lambda r:key(r['pair']))[0]
 if g in forced:
  seen=[r for r in candidates if r['pair']in known]
  if seen:representative=sorted(seen,key=lambda r:r['pair'])[0]
 groups_ready.append(dict(group_id=g,official_split=rs[0]['official_split'],stratum='building'if building else'nonbuilding',pair=representative['pair'],all_group_pairs=sorted(r['pair']for r in rs),scene_keys=sorted({r['scene_key']for r in rs}),previously_observed=g in forced))
out={'status':'PROPOSED_NOT_EXECUTED_PENDING_REVIEW','seed':seed,'grouping':'Connected components of physical scene directory, source image URL and exact image SHA256. No heldout GT values or model scores used. Same-name generic scene names alone not merged. Near-duplicate residual risk remains.','dev':[],'heldout':[],'excluded_cross_split_components':excluded}
for role,split,names in [('dev','val',{'building':10,'nonbuilding':6}),('heldout','test',{'building':20,'nonbuilding':12})]:
 for stratum,n in names.items():
  candidates=[g for g in groups_ready if g['official_split']==split and g['stratum']==stratum]
  candidates=sorted(candidates,key=lambda g:(not g['previously_observed'],key(g['group_id'])))
  out[role].extend(candidates[:n]);assert len(candidates)>=n
selected={g['group_id']for role in ['dev','heldout']for g in out[role]}
out['reserved_test_group_count']=sum(g['official_split']=='test'and g['group_id']not in selected for g in groups_ready)
out['counts']={role:{'scene_components':len(out[role]),'selected_pairs':len(out[role]),'building':sum(g['stratum']=='building'for g in out[role]),'nonbuilding':sum(g['stratum']=='nonbuilding'for g in out[role])}for role in ['dev','heldout']}
path=O/'proposed_split.json';path.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'counts':out['counts'],'reserved_test_group_count':out['reserved_test_group_count'],'excluded_cross_split_components':excluded,'manifest_sha256':hashlib.sha256(path.read_bytes()).hexdigest()},indent=2))
