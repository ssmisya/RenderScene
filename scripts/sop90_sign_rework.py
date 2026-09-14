"""Replace generic system-font market sign with digitized physical sign plates.
Perspective/spacing remain subject to multi-view calibration in SOP90.
"""
from mathutils import Matrix
pbr('Market sign green','sop90/green_sign',1.0)
data=json.loads((ROOT/'assets/geometry/daoli_sign_outlines.json').read_text())
for ob in list(sign_objects):
 if ob.name.startswith(('V221_Daoli_letter_','V221_Bazashi_')):
  sign_objects.remove(ob);bpy.data.objects.remove(ob,do_unlink=True)
# Previous gold roof-and-three-arches primitive geometry lives in the canopy group.
for key in list(B):
 if key[1]=='SOP_Market_canopy_seams_and_soffit' and key[2]=='Gold leaf':del B[key]

def sign_plate(item,F,normal,u,z,height,mat,name):
 x,y,w,h=item['bounds_pixels'];width=height*w/h
 cu=bpy.data.curves.new(name,'CURVE');cu.dimensions='2D';cu.fill_mode='BOTH';cu.extrude=.027;cu.bevel_depth=.002;cu.bevel_resolution=1;cu.resolution_u=1
 for contour in item['contours']:
  spline=cu.splines.new('POLY');pts=contour['points'];spline.points.add(len(pts)-1)
  for point,(a,b) in zip(spline.points,pts):point.co=((a-.5)*width,(1-b)*height,0,1)
  spline.use_cyclic_u=True
 ob=bpy.data.objects.new(name,cu);COLS['03_OSM_BUILDINGS'].objects.link(ob);cu.materials.append(M[mat])
 nx,ny=normal
 ob.matrix_world=Matrix(((-ny,0,nx,F(u,z,.99)[0]),(nx,0,ny,F(u,z,.99)[1]),(0,1,0,z),(0,0,0,1)))
 ob['role']='render_geometry';ob['source_photo_id']=data['source_photo_id'];ob['source_sha256']=data['source_sha256'];ob['review_status']='UNVERIFIED: digitized contour, camera calibration pending'
 # Convert the real 2D plate to solid mesh, retaining voids and thickness in glTF.
 bpy.ops.object.select_all(action='DESELECT');ob.select_set(True);bpy.context.view_layer.objects.active=ob;bpy.ops.object.convert(target='MESH')
 ob=bpy.context.object
 if mat=='Market sign green':
  uv=ob.data.uv_layers.new(name='Metric LED pitch 15mm')
  for poly in ob.data.polygons:
   for li in poly.loop_indices:
    v=ob.data.vertices[ob.data.loops[li].vertex_index].co
    uv.data[li].uv=(v.x/.015,v.y/.015)
 sign_objects.append(ob)
 return ob
for F,normal,L in market_frames[:1]:
 for k,glyph in enumerate(data['glyphs']):sign_plate(glyph,F,normal,4.9-k*2.45,4.88,1.65,'Market sign green','SOP90_Daoli_sign_'+glyph['character'])
 sign_plate(data['logo'],F,normal,7.55,4.76,1.85,'Gold leaf','SOP90_Bazashi_sign_silhouette')
 # The lower counters in the gold plate are the physical dark raised wordmark;
 # their backing is flush behind the gold face, rather than hidden inside it.
 ACTIVE='03_OSM_BUILDINGS';GROUP='SOP90_Bazashi_dark_wordmark'
 for c in data['logo']['contours']:
  if c['hole'] and sum(p[1] for p in c['points'])/len(c['points'])>.56:
   width=1.85*data['logo']['bounds_pixels'][2]/data['logo']['bounds_pixels'][3]
   add([F(7.55-(a-.5)*width,4.76+(1-b)*1.85,1.017) for a,b in c['points']],[tuple(range(len(c['points'])))],'Iron black')
print('SOP90 physical market lettering rebuilt from high-resolution observed outlines',flush=True)
