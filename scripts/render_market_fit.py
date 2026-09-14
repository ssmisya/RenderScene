"""Render the fitted diagnostic camera through Blender, with no image warping."""
import bpy,json,hashlib
from pathlib import Path
from mathutils import Matrix,Vector
R=Path(__file__).resolve().parents[1];D=R/'renders/sop90';D.mkdir(exist_ok=True)
j=json.loads((R/'verification/sop90/market_camera_fit.json').read_text())
s=next(x for x in bpy.data.scenes if x.get('lighting_mode')=='DAY');bpy.context.window.scene=s
n=(.9949941789807715,-.09993289645747541);Q=Matrix(((-n[1],0,n[0]),(n[0],0,n[1]),(0,1,0)));base=Vector((-113.9240607518968,18.45474513609582,0))
c=s.camera;c.location=base+Q@Vector(j['camera_position_facade']);c.rotation_euler=(Q@Matrix(j['world_to_opencv_rotation']).transposed()@Matrix.Diagonal(Vector((1,-1,-1)))).to_euler();c.data.sensor_fit='HORIZONTAL';c.data.sensor_width=36;c.data.lens=j['lens_mm_36mm_sensor']
s.render.resolution_x=2209;s.render.resolution_y=1356;s.render.resolution_percentage=100
pref=bpy.context.preferences.addons['cycles'].preferences;pref.compute_device_type='METAL';pref.get_devices()
for d in pref.devices:d.use=d.type=='METAL'
s.cycles.device='GPU';s.cycles.samples=48;s.cycles.use_denoising=True
# Keep the saved afternoon environment; light/color are not being claimed matched.
s.render.filepath=str(D/'market_fit.png');bpy.ops.render.render(write_still=True,scene=s.name)
assets={p:hashlib.sha256((R/p).read_bytes()).hexdigest() for p in ['Harbin_Sophia_Square.blend','game/Sophia_Square.glb','game/Sophia_Collision.glb']}
record={'position':list(c.location),'rotation':list(c.rotation_euler),'lens_mm':c.data.lens,'resolution':[2209,1356],'assets':assets,'status':'DIAGNOSTIC_NOT_ACCEPTED','lighting':'Saved afternoon scene; not source matched','fit_file':'verification/sop90/market_camera_fit.json'}
(D/'market_camera.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
