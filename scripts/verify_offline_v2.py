"""Render a copied .blend in an isolated project subfolder with no adjacent assets."""
import bpy,json
from pathlib import Path
R=Path(__file__).resolve().parents[1];D=Path(bpy.data.filepath).parent
assert D==R/'verification/offline'
images=[{'name':im.name,'packed':bool(im.packed_file),'adjacent_file_exists':Path(bpy.path.abspath(im.filepath)).exists()} for im in bpy.data.images if im.source=='FILE']
assert all(i['packed'] and not i['adjacent_file_exists'] for i in images),images
s=next(s for s in bpy.data.scenes if s.get('lighting_mode')=='NIGHT');bpy.context.window.scene=s
try:
 p=bpy.context.preferences.addons['cycles'].preferences;p.compute_device_type='METAL';p.get_devices()
 for d in p.devices:d.use=d.type=='METAL'
 s.cycles.device='GPU'
except:s.cycles.device='CPU'
s.render.resolution_x=640;s.render.resolution_y=426;s.render.resolution_percentage=100;s.cycles.samples=16;s.render.filepath=str(D/'NIGHT_Portability.png');bpy.ops.render.render(write_still=True)
report={'copied_scene':'verification/offline/Harbin_Sophia_Square.blend','external_images_absent':True,'packed_images':images,'render':'verification/offline/NIGHT_Portability.png','result':'PASS'}
json.dump(report,open(R/'verification/offline_validation.json','w'),indent=2);print('OFFLINE_PORTABILITY_PASS',flush=True)
