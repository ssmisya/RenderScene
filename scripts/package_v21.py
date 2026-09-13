"""Package the verified V2.1 scene without replacing the historical V2 ZIP."""
from pathlib import Path
import json,hashlib,zipfile
from PIL import Image,ImageStat,ImageChops,ImageOps,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[1];D=R/'renders/v2_1'
views=['Hero','Eye','East','Overview','Detail','North','Close','Front','Return']
records=[]
for mode in ['DAY','NIGHT']:
 for view in views:
  p=D/f'{mode}_{view}.png';im=Image.open(p).convert('RGB');im.load()
  assert im.size==(2400,1600),(p,im.size)
  mean=ImageStat.Stat(im).mean;assert sum(mean)>9,(p,mean)
  records.append({'file':str(p.relative_to(R)),'size':list(im.size),'mean_rgb':mean,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
for view in views:
 delta=sum(ImageStat.Stat(ImageChops.difference(Image.open(D/f'DAY_{view}.png').convert('RGB'),Image.open(D/f'NIGHT_{view}.png').convert('RGB'))).mean)/3
 assert delta>10,(view,delta)
scene_hash=hashlib.sha256((R/'Harbin_Sophia_Square.blend').read_bytes()).hexdigest()
validation=json.loads((R/'validation_v2_1.json').read_text());assert validation['source_scene_sha256']==scene_hash
assert all(validation['checks'].values())
(D/'render_validation.json').write_text(json.dumps({'revision':'2.1.0','source_scene_sha256':scene_hash,'images':records,'all_18_images_valid':True,'day_night_pairs_differ':True},indent=2)+'\n')
# A labeled, same-camera before/after contact sheet; both sides are actual Blender renders.
font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',28)
canvas=Image.new('RGB',(2400,850),(22,27,28));draw=ImageDraw.Draw(canvas)
for i,(p,label) in enumerate([(R/'renders/v2/DAY_Hero.png','V2.0 — previous geometry'),(D/'DAY_Hero.png','V2.1 — stepped facade / no pigeons')]):
 im=Image.open(p).convert('RGB');canvas.paste(im.resize((1200,800),Image.Resampling.LANCZOS),(i*1200,50));draw.text((i*1200+24,10),label,font=font,fill=(235,237,230))
canvas.save(D/'BEFORE_AFTER.jpg',quality=94)
files=[]
for directory in ['scripts','assets','references','game','renders/v2_1']:
 files.extend(p for p in (R/directory).rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='.DS_Store' and p.suffix!='.log')
for name in ['Harbin_Sophia_Square.blend','README.md','V2.1_结构修正与实景核对.md','V2_实景核对与使用.md','目录与使用指南.md','REFERENCES.md','PHOTO_AUDIT_V2.json','scene_stats.json','validation_v2.json','validation_v2_1.json','preview.html','AGENTS.md','VERSION','CHANGELOG.md','版本管理.md','打开白天.command','打开夜晚.command','渲染白天.command','渲染夜晚.command','verification/offline_validation.json','verification/offline/NIGHT_Portability.png','verification/README.md']:
 files.append(R/name)
files=sorted(set(files));assert all(p.is_file() for p in files)
manifest={'revision':'2.1.0','main':'Harbin_Sophia_Square.blend','source_scene_sha256':scene_hash,'lighting_scenes':['01_DAY_白天','02_NIGHT_夜晚'],'files':[{'path':str(p.relative_to(R)),'size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files]}
mp=R/'MANIFEST_v2_1.json';mp.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n');files.append(mp)
(R/'MANIFEST.json').write_text(json.dumps({'current_manifest':mp.name,'revision':'2.1.0','historical_v2_manifest':'MANIFEST_v2.json'},indent=2)+'\n')
archive=R/'Harbin_Sophia_v2.1_Day_Night.zip'
with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=5) as z:
 for p in files:z.write(p,Path('Harbin_Sophia_v2.1')/p.relative_to(R))
with zipfile.ZipFile(archive) as z:assert z.testzip() is None
report={'revision':'2.1.0','archive':archive.name,'bytes':archive.stat().st_size,'sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),'entries':len(files),'crc_check':'PASS','main_scene_sha256':scene_hash,'images_verified':18}
(R/'package_validation_v2_1.json').write_text(json.dumps(report,indent=2)+'\n');print('V21_PACKAGE_PASS',report,flush=True)
