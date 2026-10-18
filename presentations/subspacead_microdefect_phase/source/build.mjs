import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { Presentation, PresentationFile } from '@oai/artifact-tool';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const FONT = 'Noto Sans CJK SC';
const C = { navy:'#102A43', body:'#243B53', muted:'#627D98', blue:'#1769AA', white:'#FFFFFF', pale:'#EDF3F8', line:'#C7D5E0' };
const inputPath = process.argv[2] || path.join(ROOT, 'source', 'slides.json');
if (!inputPath) throw new Error('Usage: build-deck.mjs <source-backed-slide-spec.json> [revision]');
const spec = JSON.parse(await fs.readFile(inputPath, 'utf8'));
const rev = process.argv[3] || 'v1';
const base = `${spec.id}-${rev}`;
const staging = path.join(ROOT, 'generated', base);
const out = staging;
await fs.mkdir(staging, {recursive:true});
await fs.mkdir(out, {recursive:true});
const p = Presentation.create({slideSize:{width:1280,height:720}});
const nativeTables = [];

function txt(s, name, content, x, y, w, h, opts={}) {
  const t=s.shapes.add({geometry:'textbox',name,position:{left:x,top:y,width:w,height:h},fill:'none',line:{style:'solid',fill:'none',width:0}});
  t.text=content;
  t.text.style={typeface:FONT,fontSize:opts.size??28,color:opts.color??C.body,bold:opts.bold??false,alignment:opts.align??'left',verticalAlignment:'top',wrap:'square',autoFit:'none',insets:0,...(opts.style||{})};
  return t;
}
function note(s,d) {
  s.speakerNotes.text=[d.notes||'',...(d.sources||[]).map(x=>`${x.title||'来源'}：${x.url||x}`)].filter(Boolean).join('\n\n');
}
function heading(s,d,i) {
  s.background.fill=C.white;
  txt(s,'slide-title',d.title,64,42,1150,76,{size:d.titleSize||44,bold:true,color:C.navy});
  if(d.subtitle) txt(s,'slide-subtitle',d.subtitle,66,120,1140,45,{size:23,color:C.muted});
  txt(s,'folio',String(i+1),1170,677,44,25,{size:18,color:C.muted,align:'right'});
  if(d.sourceLabel) txt(s,'visible-source',d.sourceLabel,64,676,1060,29,{size:18,color:C.muted});
}
async function img(s,asset,x,y,w,h) {
  const b=await fs.readFile(path.resolve(ROOT, asset.path));
  const ext=path.extname(asset.path).toLowerCase();
  const type=ext==='.jpg'||ext==='.jpeg'?'image/jpeg':ext==='.webp'?'image/webp':'image/png';
  return s.images.add({name:asset.name||'research-evidence',blob:b.buffer.slice(b.byteOffset,b.byteOffset+b.byteLength),contentType:type,alt:asset.caption||asset.alt||'Research evidence',fit:'contain',position:{left:x,top:y,width:w,height:h}});
}
function rows(s,arr,{x=66,y=180,w=1144,gap=112,labelW=210,bodySize=28}={}) {
  for(const [k,r]of arr.entries()) {
    const yy=y+k*gap;
    txt(s,`row-${k}-label`,r.label,x,yy,labelW,58,{size:27,bold:true,color:C.blue});
    txt(s,`row-${k}-content`,r.text,x+labelW+24,yy,w-labelW-24,gap-17,{size:bodySize,color:C.body});
  }
}
function table(s,d,index) {
  const vals=[d.headers,...d.rows];
  const widths=d.widths??d.headers.map(()=>1144/d.headers.length);
  const tab=s.tables.add({rows:vals.length,columns:d.headers.length,left:d.x??64,top:d.y??180,width:d.width??1144,height:d.height??400,columnWidths:widths,values:vals});
  tab.styleOptions={headerRow:true,bandedRows:false};
  tab.borders.assign({style:'solid',fill:C.line,width:0.7});
  for(let r=0;r<vals.length;r++)for(let c=0;c<d.headers.length;c++) {
    const cell=tab.getCell(r,c);
    cell.fill=r===0?C.navy:C.white;
    cell.text.style={typeface:FONT,fontSize:d.fontSize??25,color:r===0?C.white:C.body,bold:r===0,verticalAlignment:'middle',insets:12};
  }
  if(d.rowHeights) d.rowHeights.forEach((v,r)=>{tab.rows[r].height=v;});
  nativeTables.push(index+1);
}

for(const [i,d]of spec.slides.entries()) {
  const s=p.slides.add();
  if(d.layout==='cover') {
    s.background.fill=C.navy;
    txt(s,'cover-context',d.context||'计算机视觉课程 · 课题开题',68,61,1100,40,{size:24,color:'#B8CBDC'});
    txt(s,'cover-title',d.title,64,202,1144,220,{size:d.titleSize||60,bold:true,color:C.white});
    if(d.subtitle)txt(s,'cover-subtitle',d.subtitle,68,448,1090,100,{size:29,color:'#D5E3EF'});
    if(d.team)txt(s,'cover-team',d.team,68,620,1100,36,{size:22,color:'#B8CBDC'});
  } else {
    heading(s,d,i);
    if(d.layout==='rows') rows(s,d.items,d.rowOptions||{});
    else if(d.layout==='table') {
      table(s,d,i);
      if(d.takeaway)txt(s,'table-takeaway',d.takeaway,66,d.takeawayY||604,1138,55,{size:27,color:C.blue,bold:true});
    } else if(d.layout==='image') {
      const fr=d.frame||{x:64,y:179,w:744,h:425};
      await img(s,d.asset,fr.x,fr.y,fr.w,fr.h);
      if(d.items)rows(s,d.items,{x:850,y:184,w:357,gap:144,labelW:0,bodySize:27,...d.rowOptions});
      if(d.sideText)txt(s,'image-explanation',d.sideText,850,185,357,420,{size:28});
      if(d.caption)txt(s,'image-caption',d.caption,fr.x,fr.y+fr.h+13,fr.w,48,{size:21,color:C.muted});
      if(d.bottomText)txt(s,'bottom-statement',d.bottomText,66,597,1138,64,{size:27,bold:true,color:C.blue});
    } else if(d.layout==='question') {
      txt(s,'research-question',d.question,66,190,1128,170,{size:d.questionSize||43,bold:true,color:C.blue});
      if(d.hypothesis)txt(s,'research-hypothesis',d.hypothesis,66,395,1128,104,{size:29});
      if(d.definition)txt(s,'research-definition',d.definition,66,541,1128,90,{size:25,color:C.muted});
    } else if(d.layout==='two_column') {
      txt(s,'column-left-heading',d.left.title,66,180,530,50,{size:31,bold:true,color:C.blue});
      txt(s,'column-right-heading',d.right.title,670,180,538,50,{size:31,bold:true,color:C.blue});
      txt(s,'column-left-body',d.left.text,66,254,530,362,{size:d.bodySize||28});
      txt(s,'column-right-body',d.right.text,670,254,538,362,{size:d.bodySize||28});
    } else if(d.layout==='free') {
      for(const [k,t] of (d.texts||[]).entries())txt(s,t.name||`content-${k}`,t.text,t.x,t.y,t.w,t.h,t);
      for(const a of (d.images||[]))await img(s,a,a.x,a.y,a.w,a.h);
      if(d.table)table(s,d.table,i);
    } else throw new Error(`Unknown layout: ${d.layout}`);
  }
  note(s,d);
}

const finalPath=path.join(out,`${spec.id}.pptx`);
await (await PresentationFile.exportPptx(p)).save(finalPath);
for(const [i,s] of p.slides.items.entries()) {
  const png=await p.export({slide:s,format:'png',scale:1.5});
  await fs.writeFile(path.join(out,`slide-${String(i+1).padStart(2,'0')}.png`),new Uint8Array(await png.arrayBuffer()));
}
console.log(`Exported ${spec.slides.length} slides to ${out}`);
