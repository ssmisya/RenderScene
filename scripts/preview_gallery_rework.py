"""Render an unaccepted gallery topology candidate; never overwrite the main scene.
G01 is informed by the paired arches in Figure 70 (2025). Dimensions remain estimates.
Run Blender with the root blend loaded, then --python this script.
"""
import bpy, math, json, hashlib
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[1];D=R/'verification/sop_reaudit/local';D.mkdir(parents=True,exist_ok=True)
day=next(s for s in bpy.data.scenes if s.get('lighting_mode')=='DAY');bpy.context.window.scene=day
col=bpy.data.collections.new('SOP_G01_REWORK_CANDIDATE_NOT_ACCEPTED');day.collection.children.link(col)
material=bpy.data.materials.get('Gallery red sandstone');metal=bpy.data.materials.get('Gallery aged coping')
def obj(name,verts,faces,mat):
 mesh=bpy.data.meshes.new(name);mesh.from_pydata(verts,[],faces);mesh.update();ob=bpy.data.objects.new(name,mesh);col.objects.link(ob);mesh.materials.append(mat)
 uv=mesh.uv_layers.new(name='MetricUV')
 for poly in mesh.polygons:
  for li in poly.loop_indices:
   co=mesh.vertices[mesh.loops[li].vertex_index].co
   uv.data[li].uv=(co.y*.88,co.z*.88) if abs(poly.normal.x)>.5 else (co.x*.88,co.z*.88)
 ob['sop_item']='G01';ob['review_status']='REWORK_CANDIDATE';return ob
# Local facade coordinates: u along the terminal, z elevation, d outward towards street.
def point(u,z,d=0):return (-64-d,37.5+u,z)
def box(name,u,z,d,w,h,depth,mat=material):
 v=[point(u+a*w/2,z+b*h/2,d+c*depth/2) for a,b,c in [(-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1),(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1)]]
 return obj(name,v,[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],mat)
def rod(name,a,b,r,mat=metal):
 axis=Vector(b)-Vector(a);u=axis.cross(Vector((0,0,1)))
 if u.length<.01:u=axis.cross(Vector((0,1,0)))
 u.normalize();v=axis.normalized().cross(u);verts=[]
 for p in [Vector(a),Vector(b)]:
  verts.extend([p+r*(u*math.cos(i*math.tau/10)+v*math.sin(i*math.tau/10)) for i in range(10)])
 return obj(name,verts,[(i,(i+1)%10,(i+1)%10+10,i+10) for i in range(10)]+[tuple(range(9,-1,-1)),tuple(range(10,20))],mat)
box('G01_center_masonry_pier',0,3.62,0,1.0,5.2,1.0)
for z,w,h,d in [(1.20,1.27,.30,1.27),(1.60,1.13,.18,1.13),(4.85,1.16,.20,1.20),(5.5,1.26,.30,1.28)]:box('G01_center_pier_course',0,z,.08,w,h,d)
for u in [-1.9,1.9]:
 for layer in range(3):
  r=1.31+layer*.10;verts=[]
  for i in range(33):
   a=i*math.pi/32
   for rr,d in [(r,.11),(r+.065,.11),(r,.27),(r+.065,.27)]:verts.append(point(u+rr*math.cos(a),4.18+rr*math.sin(a),d))
  faces=[]
  for i in range(32):
   k=4*i;faces.extend([(k,k+4,k+5,k+1),(k+2,k+3,k+7,k+6),(k,k+2,k+6,k+4),(k+1,k+5,k+7,k+3)])
  faces += [(0,1,3,2),(128,130,131,129)]
  obj('G01_paired_arch',verts,faces,metal)
 for i in range(1,10):
  a=i*math.pi/10;rod('G01_fan_tracery',point(u,4.18,.34),point(u+1.28*math.cos(a),4.18+1.28*math.sin(a),.34),.016)
 rod('G01_arch_spring_tie',point(u-1.31,4.18,.34),point(u+1.31,4.18,.34),.025)
# This is a local review candidate. Existing main-scene collisions and test results
# are not reused as proof for the added pier. No candidate game package is published.
cam=day.camera;cam.location=(-95,26,2.5);target=Vector((-62,37.5,4));cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=48
pref=bpy.context.preferences.addons['cycles'].preferences;pref.compute_device_type='METAL';pref.get_devices()
for d in pref.devices:d.use=d.type=='METAL'
day.cycles.device='GPU';day.cycles.samples=24;day.render.resolution_x=1200;day.render.resolution_y=800;day.render.resolution_percentage=100
for mode in ['baseline','candidate']:
 col.hide_render=mode=='baseline';day.render.filepath=str(D/('gallery_'+mode+'.png'));bpy.ops.render.render(write_still=True,scene=day.name)
col.hide_render=False;day['sop_status']='REWORK_REQUIRED; topology candidate only, no dimensional or gameplay acceptance'
bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(D/'Gallery_rework_candidate.blend'))
meta={'status':'UNVERIFIED','position':list(cam.location),'rotation':list(cam.rotation_euler),'lens_mm':cam.data.lens,'resolution':[1200,800],'photo_id':'brick_gallery_2025','calibration':'NOT_CALIBRATED; source lacks camera and dimensional anchors','known_limitations':['Candidate has no gameplay collision integration','Only paired-bay topology addressed; G02-G09 unresolved'],'assets':json.loads((R/'demo/assets/manifest.json').read_text())}
(D/'gallery_camera.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n');print('LOCAL_GALLERY_CANDIDATE_RENDERED_NOT_ACCEPTED',flush=True)
