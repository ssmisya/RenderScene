"""Render DAY/NIGHT views from the saved .blend, without changing it."""
import bpy,sys,argparse,json
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--mode',choices=['day','night','both'],default='both');p.add_argument('--view',choices=['hero','eye','east','overview','detail','north','close','front','return','all'],default='hero');p.add_argument('--width',type=int,default=2400);p.add_argument('--samples',type=int,default=192);p.add_argument('--cpu',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
R=Path(bpy.data.filepath).parent;D=R/'renders/v2_2_1';D.mkdir(exist_ok=True)
try:
 pref=bpy.context.preferences.addons['cycles'].preferences;pref.compute_device_type='METAL';pref.get_devices()
 for d in pref.devices:d.use=d.type=='METAL'
 device='GPU'
except:device='CPU'
if a.cpu:device='CPU'
views={'hero':'01_HERO_West_square','eye':'02_EYE_LEVEL_170cm','east':'03_EAST_Facade','overview':'04_MAP_Overview','detail':'05_Brick_detail','north':'06_NORTH_Square','close':'07_Portal_close','front':'08_FRONT_Elevation','return':'09_WEST_Return'}
for mode in ['day','night'] if a.mode=='both' else [a.mode]:
 s=next(s for s in bpy.data.scenes if s.get('lighting_mode')==mode.upper());bpy.context.window.scene=s;s.cycles.device=device;s.cycles.samples=a.samples;s.cycles.use_denoising=True;s.render.resolution_x=a.width;s.render.resolution_y=round(a.width*2/3);s.render.resolution_percentage=100
 for v in views if a.view=='all' else [a.view]:
  s.camera=bpy.data.objects[views[v]];s.render.filepath=str(D/(mode.upper()+'_'+v.title()+'.png'));print('RENDER_V2',mode,v,flush=True);bpy.ops.render.render(write_still=True,scene=s.name)
print('RENDER_V2_COMPLETE',flush=True)
