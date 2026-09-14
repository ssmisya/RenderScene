"""Render the integrated rework at fixed, explicitly uncalibrated inspection views."""
import bpy,json,hashlib
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[1];D=R/'renders/sop_rework';D.mkdir(exist_ok=True)
assets={p:hashlib.sha256((R/p).read_bytes()).hexdigest() for p in ['Harbin_Sophia_Square.blend','game/Sophia_Square.glb','game/Sophia_Collision.glb']}
pref=bpy.context.preferences.addons['cycles'].preferences;pref.compute_device_type='METAL';pref.get_devices()
for d in pref.devices:d.use=d.type=='METAL'
views=[('gallery',(-86,28,2.0),(-61,38,4.0),42),('market',(-93,16.4,1.7),(-113.9,18.45,3.5),32)]
records=[]
for mode in ['DAY','NIGHT']:
 s=next(s for s in bpy.data.scenes if s.get('lighting_mode')==mode);bpy.context.window.scene=s
 s.cycles.device='GPU';s.cycles.samples=48;s.cycles.use_denoising=True
 s.render.resolution_x=1600;s.render.resolution_y=1000;s.render.resolution_percentage=100
 for name,pos,target,lens in views:
  c=s.camera;c.location=pos;c.rotation_euler=(Vector(target)-c.location).to_track_quat('-Z','Y').to_euler();c.data.lens=lens
  output=D/(mode+'_'+name+'.png');s.render.filepath=str(output)
  bpy.ops.render.render(write_still=True,scene=s.name)
  records.append({'name':mode+'_'+name,'position':list(c.location),'rotation_euler':list(c.rotation_euler),'lens_mm':lens,'resolution':[1600,1000],'assets':assets,'render':str(output.relative_to(R)),'status':'INSPECTION_ONLY_NOT_CAMERA_MATCHED'})
(D/'cameras.json').write_text(json.dumps(records,indent=2)+'\n')
print('SOP_REWORK_RENDERS_COMPLETE',flush=True)
