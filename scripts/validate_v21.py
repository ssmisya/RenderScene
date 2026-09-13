"""Check V2.1 structure, no pigeon meshes, daylight separation and exterior clearances."""
import bpy,json,hashlib
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[1]
# Retain established packed-resource, lighting, height and route checks.
exec(compile((R/'scripts/validate_v2.py').read_text(),str(R/'scripts/validate_v2.py'),'exec'))
s=next(s for s in bpy.data.scenes if s.get('lighting_mode')=='DAY')
bpy.context.window.scene=s;dg=bpy.context.evaluated_depsgraph_get()
checks={}
checks['no_pigeon_objects']=not any('pigeon' in o.name.lower() for o in bpy.data.objects)
checks['nine_inspection_cameras']=sum(o.type=='CAMERA' for o in s.objects)==9
hits={}
for label,y,z in [('centre_upper',0,18),('shoulder_upper',6,18),('shoulder_lower',6,14),('portal_jamb',3.7,2.4)]:
 found,point,normal,index,ob,matrix=s.ray_cast(dg,Vector((-32,y,z)),Vector((1,0,0)),distance=45)
 hits[label]={'hit':found,'point':list(point) if found else None,'object':ob.name if ob else None}
checks['centre_reaches_upper_level']=hits['centre_upper']['hit'] and hits['centre_upper']['point'][0]<-19
checks['shoulder_is_lower_than_centre']=not hits['shoulder_upper']['hit'] or hits['shoulder_upper']['point'][0]>-17
checks['lower_shoulder_exists']=hits['shoulder_lower']['hit'] and hits['shoulder_lower']['point'][0]<-20
checks['portal_projects_forward']=hits['portal_jamb']['hit'] and hits['portal_jamb']['point'][0]<-21
checks['no_scene_errors']=not report['errors']
result={'revision':'2.1.0','source_scene_sha256':hashlib.sha256((R/'Harbin_Sophia_Square.blend').read_bytes()).hexdigest(),'checks':checks,'west_surface_rays':hits,'scene_checks':report,'accuracy_scope':'These checks verify model structure and data, not a 100% real-building match.'}
(R/'validation_v2_1.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print('V21_VALIDATION',checks,flush=True)
assert all(checks.values()),checks
