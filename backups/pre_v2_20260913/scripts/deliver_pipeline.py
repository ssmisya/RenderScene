"""Refresh cameras, verify packed scene, render all views, export and reimport game assets."""
from pathlib import Path
import runpy,json,bpy,numpy as np
root=Path(bpy.data.filepath).parent
for name in ['finalize_render.py','export_game.py','verify_game.py']:
 print('DELIVERY_STAGE',name,flush=True);runpy.run_path(str(root/'scripts'/name),run_name='__main__')
reports=[]
for name in ['01_Hero.png','02_Eye_Level.png','03_East.png','04_Overview.png','05_Detail.png']:
 im=bpy.data.images.load(str(root/'renders'/name));a=np.asarray(im.pixels[:],dtype=np.float32).reshape(-1,4)[:,:3];r={'file':name,'size':list(im.size),'mean_rgb':float(a.mean()),'nonblack_fraction':float((a.max(axis=1)>.04).mean())};reports.append(r)
 assert list(im.size)==[1920,1280] and r['mean_rgb']>.02 and r['nonblack_fraction']>.5, r
json.dump(reports,open(root/'renders/render_validation.json','w'),indent=2)
print('DELIVERY_PIPELINE_COMPLETE',flush=True)
