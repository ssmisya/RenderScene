"""Validate rendered files, write release hashes, and package only current deliverables."""
from pathlib import Path
import json,hashlib,zipfile,shutil
from PIL import Image,ImageStat,ImageChops
R=Path(__file__).resolve().parents[1]
reports=[]
for mode in ['DAY','NIGHT']:
 for view in ['Hero','Eye','East','Overview','Detail','North','Close']:
  p=R/'renders/v2'/f'{mode}_{view}.png';im=Image.open(p).convert('RGB');im.load();mean=ImageStat.Stat(im).mean
  assert im.size==(2400,1600),(p,im.size)
  assert sum(mean)/3>3,(p,mean)
  reports.append({'file':str(p.relative_to(R)),'size':list(im.size),'mean_rgb_srgb_255':mean,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
for view in ['Hero','Eye','East','Overview','Detail','North','Close']:
 d=Image.open(R/'renders/v2'/f'DAY_{view}.png').convert('RGB');n=Image.open(R/'renders/v2'/f'NIGHT_{view}.png').convert('RGB');delta=sum(ImageStat.Stat(ImageChops.difference(d,n)).mean)/3
 assert delta>10,(view,delta)
(R/'renders/v2/render_validation.json').write_text(json.dumps({'images':reports,'day_night_pairs_differ':True,'all_14_images_valid':True},indent=2))
# Build release contents explicitly: do not recursively include backups, legacy GLBs or ZIPs.
files=[]
for directory in ['scripts','assets','references','game','renders/v2']:
 files.extend(p for p in (R/directory).rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='.DS_Store')
for name in ['Harbin_Sophia_Square.blend','README.md','V2_实景核对与使用.md','目录与使用指南.md','REFERENCES.md','PHOTO_AUDIT_V2.json','scene_stats.json','validation_v2.json','preview.html','AGENTS.md','打开白天.command','打开夜晚.command','渲染白天.command','渲染夜晚.command']:
 if (R/name).exists():files.append(R/name)
for name in ['verification/offline_validation.json','verification/offline/NIGHT_Portability.png','verification/README.md']:
 if (R/name).exists():files.append(R/name)
files=sorted(set(files))
manifest={'revision':'v2','project':'Harbin Saint Sophia Square','main':'Harbin_Sophia_Square.blend','lighting_scenes':['01_DAY_白天','02_NIGHT_夜晚'],'files':[{'path':str(p.relative_to(R)),'size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files]}
old=R/'MANIFEST.json';backup=R/'backups/pre_v2_20260913/MANIFEST.json'
if old.exists() and not backup.exists():shutil.copy2(old,backup)
(R/'MANIFEST_v2.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2));old.write_text(json.dumps({'current_manifest':'MANIFEST_v2.json','revision':'v2','old_manifest':'backups/pre_v2_20260913/MANIFEST.json'},indent=2));files.append(R/'MANIFEST_v2.json')
archive=R/'Harbin_Sophia_v2_Day_Night.zip'
with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=5) as z:
 for p in files:z.write(p,Path('Harbin_Sophia_v2')/p.relative_to(R))
with zipfile.ZipFile(archive) as z:
 bad=z.testzip();assert bad is None,bad
 assert 'Harbin_Sophia_v2/Harbin_Sophia_Square.blend' in z.namelist()
report={'archive':archive.name,'size_bytes':archive.stat().st_size,'sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),'entries':len(files),'crc_check':'PASS','main_scene_sha256':hashlib.sha256((R/'Harbin_Sophia_Square.blend').read_bytes()).hexdigest(),'images_verified':14}
(R/'package_validation_v2.json').write_text(json.dumps(report,indent=2));print('V2_PACKAGE_READY',report,flush=True)
