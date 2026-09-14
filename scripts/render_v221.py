"""Actual native renders of the two user-reported areas, without saving source changes."""
import bpy
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[1];D=R/'renders/v2_2_1';D.mkdir(exist_ok=True)
pref=bpy.context.preferences.addons['cycles'].preferences;pref.compute_device_type='METAL';pref.get_devices()
for d in pref.devices:d.use=d.type=='METAL'
for mode in ['DAY','NIGHT']:
 s=next(s for s in bpy.data.scenes if s.get('lighting_mode')==mode);bpy.context.window.scene=s;s.cycles.device='GPU';s.cycles.samples=32;s.cycles.use_denoising=True;s.render.resolution_x=1440;s.render.resolution_y=900;s.render.resolution_percentage=100
 for name,pos,target,lens in [('Gallery',(-77,30,1.7),(-57,40,4.1),30),('Market',(-70,15,1.7),(-118,25,12),25)]:
  cam=s.camera;cam.location=pos;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=lens
  s.render.filepath=str(D/(mode+'_'+name+'.png'));bpy.ops.render.render(write_still=True,scene=s.name)
print('V221_TARGET_RENDERS_COMPLETE',flush=True)
