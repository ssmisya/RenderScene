"""Render a saved scene: blender -b Harbin_Sophia_Square.blend --python scripts/render_scene.py -- --view hero --width 1920 --samples 128"""
import bpy,sys,argparse
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--view',choices=['hero','eye','east','overview','detail','all'],default='hero');p.add_argument('--width',type=int,default=1920);p.add_argument('--samples',type=int,default=128);p.add_argument('--cpu',action='store_true');args=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
root=Path(bpy.data.filepath).parent;s=bpy.context.scene
s.render.engine='CYCLES';s.cycles.samples=args.samples;s.cycles.use_denoising=True
if args.cpu:s.cycles.device='CPU'
else:
 try:
  pref=bpy.context.preferences.addons['cycles'].preferences;pref.compute_device_type='METAL';pref.get_devices()
  for d in pref.devices:d.use=d.type=='METAL'
  s.cycles.device='GPU'
 except:s.cycles.device='CPU'
s.render.resolution_x=args.width;s.render.resolution_y=round(args.width*2/3);s.render.resolution_percentage=100
views={'hero':('01_HERO_West_square','01_Hero.png'),'eye':('02_EYE_LEVEL_170cm','02_Eye_Level.png'),'east':('03_EAST_Facade','03_East.png'),'overview':('04_MAP_Overview','04_Overview.png'),'detail':('05_Brick_detail','05_Detail.png')}
for key in views if args.view=='all' else [args.view]:
 name,out=views[key];s.camera=bpy.data.objects[name];s.render.filepath=str(root/'renders'/out);print('RENDERING',key,flush=True);bpy.ops.render.render(write_still=True);print('COMPLETE',out,flush=True)
