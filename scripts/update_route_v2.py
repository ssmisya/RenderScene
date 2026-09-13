"""Fit the exterior circulation loop around the mapped ticket hut and service counter."""
import bpy,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
route=[[-55,-21,1.7],[-29,-18,1.7],[-15,-18,1.7],[-7,-24,1.7],[27,-20,1.7],[33,0,1.7],[24,22,1.7],[-9,24,1.7],[-35,18,1.7],[-55,-21,1.7]]
c=bpy.data.collections['09_GAME_MARKERS']
for ob in list(c.objects):bpy.data.objects.remove(ob,do_unlink=True)
for i,p in enumerate(route[:-1]):
 ob=bpy.data.objects.new('SPAWN_Main' if i==0 else 'ROUTE_%02d'%i,None);c.objects.link(ob);ob.location=p;ob.empty_display_type='ARROWS';ob.empty_display_size=1.0
p=R/'game/map_metadata.json';meta=json.load(open(p));meta['walking_loop_blender']=route;meta['revision']='v2';p.write_text(json.dumps(meta,indent=2))
bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(R/'Harbin_Sophia_Square.blend'))
