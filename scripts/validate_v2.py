"""Verify a freshly opened v2 scene, lighting separation, portability and walking route."""
import bpy,json,math
from mathutils import Vector
from pathlib import Path
R=Path(__file__).resolve().parents[1];errors=[];report={'blender':bpy.app.version_string,'scenes':{}}
for mode in ['DAY','NIGHT']:
 matches=[s for s in bpy.data.scenes if s.get('lighting_mode')==mode]
 if len(matches)!=1:errors.append('scene_count_'+mode);continue
 s=matches[0];lights=[o for o in s.objects if o.type=='LIGHT'];art=[o for o in lights if o.data.type!='SUN'];em=[]
 for o in s.objects:
  if o.type!='MESH':continue
  for m in o.data.materials:
   if not m or not m.use_nodes:continue
   p=m.node_tree.nodes.get('Principled BSDF')
   if p and p.inputs['Emission Strength'].default_value>0:em.append(o.name)
 report['scenes'][mode]={'name':s.name,'objects':len(s.objects),'lights':len(lights),'artificial_lights':len(art),'emissive_meshes':len(set(em)),'cameras':sum(o.type=='CAMERA' for o in s.objects),'saved_resolution':[s.render.resolution_x,s.render.resolution_y],'saved_samples':s.cycles.samples,'camera':s.camera.name}
 if mode=='DAY' and (art or em):errors.append('day_architectural_illumination_is_not_off')
 if mode=='NIGHT' and (len(art)<100 or any(o.data.type=='SUN' for o in lights)):errors.append('night_light_setup')
 for o in bpy.data.collections['07_COLLISION'].objects:
  if not o.hide_render or not o.hide_get(view_layer=s.view_layers[0]):errors.append('collision_visibility_'+mode+'_'+o.name)
report['packed_images']=[]
for im in bpy.data.images:
 if im.source!='FILE':continue
 record={'name':im.name,'packed':bool(im.packed_file),'size':list(im.size),'path':im.filepath};report['packed_images'].append(record)
 if not im.packed_file or not all(im.size):errors.append('missing_image_'+im.name)
report['packed_fonts']=[{'name':f.name,'packed':bool(f.packed_file)} for f in bpy.data.fonts if f.filepath!='<builtin>']
for f in report['packed_fonts']:
 if not f['packed']:errors.append('unpacked_font_'+f['name'])
pts=[o.matrix_world@Vector(p) for o in bpy.data.collections['01_CATHEDRAL'].objects if o.type=='MESH' for p in o.bound_box];height=max(p.z for p in pts);report['height_m']=height
if abs(height-53.35)>.03:errors.append('height_anchor')
report['collision_proxies']=len(bpy.data.collections['07_COLLISION'].objects)
# 2D route clearance at player capsule radius. Ground slabs/road surfaces are not obstacles.
meta=json.load(open(R/'game/map_metadata.json'));coll=json.load(open(R/'game/colliders.json'))['colliders'];route=meta['walking_loop_blender'];radius=meta['player_capsule_radius']
def in_poly(p,poly):
 x,y=p;inside=False
 for a,b in zip(poly,poly[1:]+poly[:1]):
  if (a[1]>y)!=(b[1]>y) and x<(b[0]-a[0])*(y-a[1])/(b[1]-a[1])+a[0]:inside=not inside
 return inside
def segdist(p,a,b):
 dx=b[0]-a[0];dy=b[1]-a[1];t=max(0,min(1,((p[0]-a[0])*dx+(p[1]-a[1])*dy)/(dx*dx+dy*dy))) if dx*dx+dy*dy>1e-12 else 0
 return math.hypot(p[0]-a[0]-t*dx,p[1]-a[1]-t*dy)
def hit(p,c):
 if c['type']=='box':
  if c['center'][2]+c['size'][2]/2<.25:return False
  dx=p[0]-c['center'][0];dy=p[1]-c['center'][1];a=c.get('rotation_z',0);x=dx*math.cos(a)+dy*math.sin(a);y=-dx*math.sin(a)+dy*math.cos(a)
  return abs(x)<c['size'][0]/2+radius and abs(y)<c['size'][1]/2+radius
 if c['type']=='cylinder':return math.hypot(p[0]-c['center'][0],p[1]-c['center'][1])<c['radius']+radius
 poly=c['points'];return in_poly(p,poly) or any(segdist(p,a,b)<radius for a,b in zip(poly,poly[1:]+poly[:1]))
samples=[]
for a,b in zip(route,route[1:]):
 count=max(1,math.ceil(math.dist(a,b)/.35))
 for i in range(count):samples.append([a[k]+(b[k]-a[k])*i/count for k in range(2)])
hits=[]
for i,p in enumerate(samples):
 for c in coll:
  if hit(p,c):hits.append({'sample':i,'position':p,'obstacle':c['name']})
route_report={'route_samples':len(samples),'capsule_radius_m':radius,'route_collision_intersections':hits,'method':'2D expanded box/cylinder and polygon boundary clearance; ground excluded. Not a game-engine physics test.'}
json.dump(route_report,open(R/'game/route_validation.json','w'),indent=2)
if hits:errors.append('walking_route_intersection')
# The revised southern plaza boundary leaves the mapped Toulong centreline outside the paving.
plaza=next(c for c in coll if c['name']=='square');ymin=plaza['center'][1]-plaza['size'][1]/2;report['plaza_south_edge_m']=ymin;report['toulong_sample_y_m']=-43.1
if ymin<=-36.6:errors.append('plaza_overlaps_toulong')
report['route']=route_report;report['errors']=errors;report['scope']='Data and actual image-generation checks. No survey accuracy, engine FPS or NavMesh certification.'
json.dump(report,open(R/'validation_v2.json','w'),ensure_ascii=False,indent=2)
print('V2_VALIDATION',json.dumps({k:v for k,v in report.items() if k not in ['packed_images','route']},ensure_ascii=False),flush=True)
if errors:raise RuntimeError(errors)
