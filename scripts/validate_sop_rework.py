"""Re-open native assets and check structure/lighting, independent of photo acceptance."""
import bpy,json,hashlib
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[1]
exec(compile((R/'scripts/validate_v2.py').read_text(),str(R/'scripts/validate_v2.py'),'exec'))
s=next(s for s in bpy.data.scenes if s.get('lighting_mode')=='DAY');bpy.context.window.scene=s
coll=bpy.data.collections['07_COLLISION']
middle=[o for o in coll.objects if 'gallery terminal middle pier' in o.name]
lamps=[o for o in s.objects if o.type=='MESH' and o.data.materials and o.data.materials[0].name=='Gallery lamp glass']
night=next(s for s in bpy.data.scenes if s.get('lighting_mode')=='NIGHT')
checks={'inherited_native_validation':not report['errors'],
 'two_terminal_middle_colliders':len(middle)==2,
 'new_lamps_have_night_diffusers':bool(lamps) and all(any(n.name=='NIGHT luminous '+o.name for n in night.objects) for o in lamps),
 'old_roof_removed':not any(o.name.startswith('V221_Gallery_roof_joinery') for o in s.objects),
 'old_uniform_market_entries_removed':not any(o.name.startswith('V221_Daoli_entries') for o in s.objects)}
ray_hits=[]
for ob in middle:
 origin=Vector((0,0,0));direction=Vector((1,0,0))
 # Test each evaluated local collision mesh itself, not a matching name alone.
 hit,point,normal,index=ob.ray_cast(Vector((-2,0,0)),direction,distance=4)
 ray_hits.append({'object':ob.name,'hit':hit,'position':list(ob.matrix_world@point) if hit else None})
checks['middle_collision_meshes_solid']=all(r['hit'] for r in ray_hits)
for prefix in ['SOP_Gallery_terminal_twin_arches','SOP_Market_canopy_seams_and_soffit','SOP90_Market_observed_portals','SOP90_Market_gift_shop','SOP90_Gallery_interior_lamps_and_guards']:
 obs=[o for o in s.objects if o.type=='MESH' and o.name.startswith(prefix)]
 checks[prefix+'_has_geometry']=bool(obs) and all(len(o.data.polygons)>0 for o in obs)
letters=[o for o in s.objects if o.name.startswith('SOP90_Daoli_sign_')]
checks['five_native_contour_letters_with_portable_uv']=len(letters)==5 and all(o.type=='MESH' and len(o.data.polygons)>0 and o.data.uv_layers.active for o in letters)
# Regress the actual occlusion bug: the generic market wall must not close the shop recess.
n=Vector((.9949941789807715,-.09993289645747541,0));u=Vector((n.y,-n.x,0));base=Vector((-113.9240607518968,18.45474513609582,0))
origin=base+u*(-3.68)+n*3+Vector((0,0,2.05));direction=-n
occluders=[]
for ob in s.objects:
 if ob.type=='MESH' and ob.name.startswith('V221_Daoli_cladding'):
  inv=ob.matrix_world.inverted();hit,point,norm,index=ob.ray_cast(inv@origin,inv.to_3x3()@direction,distance=3.05)
  if hit:occluders.append(ob.name)
checks['shop_recess_not_occluded_by_old_wall']=not occluders
# Inspect the exported wedge's actual top surface, not its object name alone.
ramp=next((o for o in coll.objects if 'gallery transverse entrance ramp' in o.name),None)
ramp_samples=[]
if ramp:
 for u0 in [0.0,2.0,4.5]:
  expected=1.05-(u0+.325)/5.225*1.02
  hit,pt,norm,idx=ramp.ray_cast(Vector((-66.05,37.5+u0,10)),Vector((0,0,-1)),distance=11)
  ramp_samples.append(hit and abs(pt.z-expected)<.001)
checks['transverse_ramp_has_continuous_sloped_collision']=len(ramp_samples)==3 and all(ramp_samples)
out={'status':'TECHNICAL_CHECK_ONLY_NOT_PHOTO_ACCEPTANCE','source_scene_sha256':hashlib.sha256((R/'Harbin_Sophia_Square.blend').read_bytes()).hexdigest(),'checks':checks,'scene_checks':report,'collision_rays':ray_hits}
(R/'verification/sop_reaudit/native_rework_validation.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print('SOP_NATIVE_CHECKS',checks,flush=True)
assert all(checks.values()),checks
