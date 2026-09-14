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
for prefix in ['SOP_Gallery_terminal_twin_arches','SOP_Market_canopy_seams_and_soffit','SOP_Market_recessed_entry_and_shops']:
 obs=[o for o in s.objects if o.type=='MESH' and o.name.startswith(prefix)]
 checks[prefix+'_has_geometry']=bool(obs) and all(len(o.data.polygons)>0 for o in obs)
out={'status':'TECHNICAL_CHECK_ONLY_NOT_PHOTO_ACCEPTANCE','source_scene_sha256':hashlib.sha256((R/'Harbin_Sophia_Square.blend').read_bytes()).hexdigest(),'checks':checks,'scene_checks':report,'collision_rays':ray_hits}
(R/'verification/sop_reaudit/native_rework_validation.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print('SOP_NATIVE_CHECKS',checks,flush=True)
assert all(checks.values()),checks
