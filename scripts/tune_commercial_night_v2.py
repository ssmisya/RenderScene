"""Balance the photographed north commercial facades; retain daytime unchanged."""
import bpy,json
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[1];col=bpy.data.collections['11_NIGHT_Architectural_lighting'];p=R/'game/lighting_v2.json';meta=json.load(open(p))
for name,pos,target,energy,color,size in [('NIGHT_North_arcade_fill',(-10,65,14),(4,120,18),13000,(1,.76,.45),14),('NIGHT_East_commercial_fill',(37,48,14),(63,68,17),8500,(1,.76,.46),12),('NIGHT_Market_fill',(-76,60,18),(-113,50,16),10000,(.79,.86,1),14)]:
 if name in bpy.data.objects:
  bpy.data.objects[name].data.energy=energy
  for rec in meta['night_lights']:
   if rec['name']==name:rec['power_watts']=energy
  continue
 d=bpy.data.lights.new(name,'AREA');d.energy=energy;d.color=color;d.shape='DISK';d.size=size;o=bpy.data.objects.new(name,d);col.objects.link(o);o.location=pos;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler();o['night_only']=True
 meta['night_lights'].append({'name':name,'type':'AREA','position_blender':list(pos),'target_blender':list(target),'power_watts':energy,'color_linear':list(color),'spot_degrees':None})
p.write_text(json.dumps(meta,ensure_ascii=False,indent=2));bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(R/'Harbin_Sophia_Square.blend'))
