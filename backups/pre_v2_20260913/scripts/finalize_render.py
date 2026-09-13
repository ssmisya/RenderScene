import bpy,sys,runpy,json
from mathutils import Vector
from pathlib import Path
root=Path(bpy.data.filepath).parent;s=bpy.context.scene
cam=bpy.data.objects['01_HERO_West_square'];cam.location=(-63,24,1.7);cam.rotation_euler=(Vector((0,0,22.3))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=29;s.camera=cam
s.render.resolution_x=1920;s.render.resolution_y=1280;s.render.resolution_percentage=100;s.cycles.samples=96;s.render.filepath=str(root/'renders/01_Hero.png')
# Reset the saved navigation view to its default camera.
for screen in bpy.data.screens:
 for area in screen.areas:
  if area.type=='VIEW_3D':area.spaces.active.region_3d.view_perspective='CAMERA';area.spaces.active.clip_end=1800
bpy.ops.wm.save_as_mainfile(filepath=str(root/'Harbin_Sophia_Square.blend'))
images=[{'name':im.name,'packed':bool(im.packed_file),'size':list(im.size)} for im in bpy.data.images if im.source=='FILE']
cat=bpy.data.collections['01_CATHEDRAL'];pts=[ob.matrix_world@Vector(co) for ob in cat.objects if ob.type=='MESH' for co in ob.bound_box]
errors=[]
for im in images:
 if not im['packed'] or 0 in im['size']:errors.append('missing_image:'+im['name'])
for ob in bpy.data.collections['07_COLLISION'].objects:
 if not ob.hide_render:errors.append('visible_collision:'+ob.name)
height=max(p.z for p in pts)
if abs(height-53.35)>.02:errors.append('height_anchor:'+str(height))
result={'blender':bpy.app.version_string,'packed_images':images,'cathedral_mesh_height_m':height,'collision_proxies':len(bpy.data.collections['07_COLLISION'].objects),'errors':errors,'validation_scope':'saved-scene data, geometry height and asset portability; no game-engine runtime validation'}
json.dump(result,open(root/'validation.json','w'),indent=2);print('VALIDATION',result,flush=True)
if errors:raise RuntimeError(str(errors))
sys.argv=['render_scene.py','--','--view','all','--width','1920','--samples','96'];runpy.run_path(str(root/'scripts/render_scene.py'),run_name='__main__')
