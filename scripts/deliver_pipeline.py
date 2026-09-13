"""Validate, render fourteen v2 views, export game assets, and reimport both GLBs."""
from pathlib import Path
import runpy,json,bpy,numpy as np
root=Path(__file__).resolve().parents[1]
for name in ['finalize_render.py','export_game.py','verify_game.py']:
 print('DELIVERY_STAGE',name,flush=True);runpy.run_path(str(root/'scripts'/name),run_name='__main__')
reports=[]
for mode in ['DAY','NIGHT']:
 for view in ['Hero','Eye','East','Overview','Detail','North','Close']:
  name=mode+'_'+view+'.png';im=bpy.data.images.load(str(root/'renders/v2'/name));a=np.asarray(im.pixels[:],dtype=np.float32).reshape(-1,4)[:,:3];r={'file':name,'size':list(im.size),'mean_rgb':float(a.mean()),'nonblack_fraction':float((a.max(axis=1)>.01).mean())};reports.append(r)
  assert list(im.size)==[2400,1600] and r['mean_rgb']>.008 and r['nonblack_fraction']>.5,r
json.dump(reports,open(root/'renders/v2/render_validation.json','w'),indent=2)
print('DELIVERY_PIPELINE_COMPLETE',flush=True)
