"""Render current native scene inspection views without overwriting historical renders."""
import bpy
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[1];D=R/'renders/v2_2';D.mkdir(exist_ok=True)
pref=bpy.context.preferences.addons['cycles'].preferences;pref.compute_device_type='METAL';pref.get_devices()
for d in pref.devices:d.use=d.type=='METAL'
for mode in ['DAY','NIGHT']:
 s=next(s for s in bpy.data.scenes if s.get('lighting_mode')==mode);bpy.context.window.scene=s
 s.cycles.device='GPU';s.cycles.samples=64;s.cycles.use_denoising=True;s.render.resolution_x=1600;s.render.resolution_y=1000;s.render.resolution_percentage=100
 for name,pos,target,lens in [('Streets',(-104,49,5),(-40,96,12),30),('North',(-34,66,1.7),(-22,125,12),28),('Hero',(-67,29,1.7),(0,0,23),31)]:
  cam=s.camera;cam.location=pos;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=lens
  s.render.filepath=str(D/(mode+'_'+name+'.png'));bpy.ops.render.render(write_still=True,scene=s.name)
print('V22_NATIVE_RENDERS_COMPLETE',flush=True)
