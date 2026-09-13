"""GUI entry helper. Switch DAY/NIGHT without saving or altering the source file."""
import bpy,sys,argparse
p=argparse.ArgumentParser();p.add_argument('--mode',choices=['day','night'],default='day');a=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
s=next(sc for sc in bpy.data.scenes if sc.get('lighting_mode')==a.mode.upper());bpy.context.window.scene=s
try:
 pref=bpy.context.preferences.addons['cycles'].preferences;pref.compute_device_type='METAL';pref.get_devices()
 for d in pref.devices:d.use=d.type=='METAL'
 s.cycles.device='GPU'
except:s.cycles.device='CPU'
for area in bpy.context.screen.areas:
 if area.type=='VIEW_3D':area.spaces.active.shading.type='RENDERED';area.spaces.active.region_3d.view_perspective='CAMERA'
