"""Create two render-ready native scenes, sharing geometry but separate worlds and lights."""
scene.name='01_DAY_白天';scene['lighting_mode']='DAY';scene['revision']='v2.1-structural-west-20260913'
daylights=bpy.data.collections.new('10_DAY_Sun');scene.collection.children.link(daylights)
for ob in list(COLS['08_CAMERAS_LIGHTS'].objects):
 if ob.type=='LIGHT':COLS['08_CAMERAS_LIGHTS'].objects.unlink(ob);daylights.objects.link(ob)
night=bpy.data.scenes.new('02_NIGHT_夜晚');night['lighting_mode']='NIGHT';night['revision']=scene['revision']
for col in scene.collection.children:
 if col!=daylights:night.collection.children.link(col)
nlights=bpy.data.collections.new('11_NIGHT_Architectural_lighting');night.collection.children.link(nlights)
night.world=bpy.data.worlds.new('Harbin blue hour night');night.world.use_nodes=True
n=night.world.node_tree.nodes;l=night.world.node_tree.links;bg=n.get('Background');bg.inputs[0].default_value=(.105,.15,.28,1);bg.inputs[1].default_value=.16
# A twilight sky gradient with a faint city glow; real illumination is provided by fixtures below.
tc=n.new('ShaderNodeTexCoord');sep=n.new('ShaderNodeSeparateXYZ');l.new(tc.outputs['Normal'],sep.inputs[0]);ra=n.new('ShaderNodeValToRGB');ra.color_ramp.elements[0].position=0;ra.color_ramp.elements[0].color=(.10,.135,.24,1);ra.color_ramp.elements[1].position=.80;ra.color_ramp.elements[1].color=(.005,.010,.035,1);l.new(sep.outputs['Z'],ra.inputs[0]);l.new(ra.outputs[0],bg.inputs[0])
lighting_record=[]
def light(name,kind,pos,target,energy,color,size=.18,spread=50):
 d=bpy.data.lights.new(name,kind);d.energy=energy;d.color=color
 if kind=='SPOT':d.spot_size=math.radians(spread);d.spot_blend=.52;d.shadow_soft_size=size
 elif kind=='AREA':d.shape='DISK';d.size=size
 else:d.shadow_soft_size=size
 ob=bpy.data.objects.new(name,d);nlights.objects.link(ob);ob.location=pos
 if target:ob.rotation_euler=(Vector(target)-ob.location).to_track_quat('-Z','Y').to_euler()
 ob['night_only']=True;lighting_record.append({'name':name,'type':kind,'position_blender':list(pos),'target_blender':list(target) if target else None,'power_watts':energy,'color_linear':list(color),'spot_degrees':spread if kind=='SPOT' else None});return ob
for i,(pos,target,kind,power) in enumerate(night_targets):
 color=(1,.72,.40) if kind=='commercial' else ((1,.80,.49) if kind=='drum' else (1,.75,.40))
 pos=tuple(Vector(pos)+(Vector(target)-Vector(pos)).normalized()*.20)
 power*=3.2 if kind=='commercial' else 8.5
 # Wider commercial lighting; cathedral close fixtures graze relief and fluting.
 light('NIGHT_%03d_%s'%(i,kind),'SPOT',pos,target,power,color,.095,65 if kind=='commercial' else 62)
light('NIGHT_West_square_fill','AREA',(-37,12,11),(-13,0,13),4000,(1,.80,.52),9)
light('NIGHT_South_square_fill','AREA',(-4,-30,13),(1,-3,16),5400,(1,.79,.50),10)
light('NIGHT_North_square_fill','AREA',(-4,31,13),(1,3,16),5400,(1,.80,.53),10)
light('NIGHT_East_square_fill','AREA',(38,4,11),(12,0,13),6000,(1,.78,.48),8)
# Green roof remains significantly darker than the masonry in the tourist night photographs.
for i,(p,t) in enumerate([((-28,17,33),(2,0,43)),((24,-22,34),(2,0,43)),((7,19,31),(2,0,42))]):light('NIGHT_Roof_low_fill_%d'%i,'AREA',p,t,4500,(.71,.85,1.0),7)
light('NIGHT_Square_ambient','AREA',(-40,30,24),(0,40,0),3000,(.70,.81,1),18)
# Duplicate only luminous lantern glass into the NIGHT scene. DAY's actual glass stays non-emissive.
em=bpy.data.materials.new('NIGHT warm luminous diffusers');em.use_nodes=True;p=em.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(.90,.74,.43,1);p.inputs['Emission Color'].default_value=(1,.70,.34,1);p.inputs['Emission Strength'].default_value=3.5
dayglass=bpy.data.collections.new('12_DAY_Non_emissive_glass');scene.collection.children.link(dayglass)
nightglass=bpy.data.materials.new('NIGHT subdued cathedral glass');nightglass.use_nodes=True;p=nightglass.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(.09,.12,.13,1);p.inputs['Roughness'].default_value=.24;p.inputs['Metallic'].default_value=.20;p.inputs['Emission Color'].default_value=(1,.77,.46,1);p.inputs['Emission Strength'].default_value=.27
for ob in list(scene.objects):
 if ob.type!='MESH' or not ob.data.materials:continue
 mn=ob.data.materials[0].name
 cathedral_glass=mn=='Old glass' and any(c.name=='01_CATHEDRAL' for c in ob.users_collection)
 if mn=='Cream lamp glass' or cathedral_glass:
  duplicate=ob.copy();duplicate.data=ob.data.copy();duplicate.name='NIGHT luminous '+ob.name;duplicate.data.materials.clear();duplicate.data.materials.append(nightglass if cathedral_glass else em);nlights.objects.link(duplicate)
  for c in list(ob.users_collection):c.objects.unlink(ob)
  dayglass.objects.link(ob)
# Actual lamppost positions used by the base geometry, discovered from lamp globe components.
# Geometry is batched; connected globe vertices identify each lantern cluster spatially.
lamps=set()
for ob in scene.objects:
 if ob.type=='MESH' and 'Lamps' in ob.name and 'Cream lamp glass' in ob.name:
  for v in ob.data.vertices:lamps.add((round(v.co.x/2)*2,round(v.co.y/2)*2))
# Fixed positions match the lamp placement in build_scene.py (single source recorded below).
for i,(x,y) in enumerate([(-73,-33),(-73,36),(-75,85),(-36,-32),(-34,35),(33,-31),(35,38),(32,84),(63,16),(-86,14),(-23,85)]):
 light('NIGHT_Plaza_lantern_%02d'%i,'POINT',(x,y,4.80),None,160,(1,.76,.43),.19)
light('NIGHT_North_arcade_fill','AREA',(-10,65,14),(4,120,18),13000,(1,.76,.45),14)
light('NIGHT_East_commercial_fill','AREA',(37,48,14),(63,68,17),8500,(1,.76,.46),12)
light('NIGHT_Market_fill','AREA',(-76,60,18),(-113,50,16),10000,(.79,.86,1),14)
# Soft lighting on the north landmark and carousel canopy.
light('NIGHT_North_clock','AREA',(-48,98,11),(-55,107,20),700,(.62,.87,.83),5)
light('NIGHT_Carousel','POINT',(-24.8,89.6,2.6),None,120,(1,.68,.36),.5)
for sc in [scene,night]:
 sc.unit_settings.system='METRIC';sc.unit_settings.scale_length=1;sc.render.engine='CYCLES';sc.cycles.samples=192;sc.cycles.use_denoising=True;sc.cycles.adaptive_threshold=.018;sc.cycles.max_bounces=9;sc.cycles.diffuse_bounces=4;sc.cycles.glossy_bounces=4;sc.cycles.transmission_bounces=4
 sc.cycles.device=scene.cycles.device;sc.render.resolution_x=2400;sc.render.resolution_y=1600;sc.render.resolution_percentage=100;sc.render.image_settings.file_format='PNG';sc.render.image_settings.color_mode='RGB';sc.render.image_settings.color_depth='8';sc.render.film_transparent=False
 sc.view_settings.view_transform='AgX';sc.view_settings.look='AgX - Medium High Contrast';sc.view_settings.exposure=.20 if sc==scene else .35
 sc.camera=cam;sc.render.filepath='//renders/v2_1/'+('DAY_Hero.png' if sc==scene else 'NIGHT_Hero.png')
 sc['accuracy_note']='Photo-interpreted exterior. OSM footprint references. No photogrammetric or surveyed claim. See V2_实景核对与使用.md.'
 sc['architectural_lights']='OFF - no artificial light collection linked' if sc==scene else 'ON - facade, portal, drum, bell tower and street fixtures'
# Slightly less theatrical wide-angle perspective; camera remains at real pedestrian eye height.
for name,loc,tgt,lens in [('01_HERO_West_square',(-67,29,1.70),(0,0,23.0),31),('02_EYE_LEVEL_170cm',(-57,-32,1.70),(0,0,20.5),28),('03_EAST_Facade',(62,-10,1.70),(2,0,21.5),28),('05_Brick_detail',(-34,-4.5,1.70),(-20.4,0,4.75),42)]:
 ob=bpy.data.objects[name];ob.location=loc;ob.rotation_euler=(Vector(tgt)-ob.location).to_track_quat('-Z','Y').to_euler();ob.data.lens=lens
camera('06_NORTH_Square',(-8,30,1.7),(-10,112,16),29)
camera('07_Portal_close',(-29.8,-2,1.7),(-20.4,0,3.2),49)
camera('08_FRONT_Elevation',(-70,0,1.7),(-8,0,24),26.5)
camera('09_WEST_Return',(-66,-35,1.7),(-6,0,23),31)
# Cameras added after linking collections are available in both scenes.
for t in list(bpy.data.texts):
 if t.name=='START_HERE.txt':bpy.data.texts.remove(t)
t=bpy.data.texts.new('START_HERE.txt');t.write('圣索菲亚广场 v2.1 / SAINT SOPHIA SQUARE\n\n右上角 Scene 选择：01_DAY_白天 / 02_NIGHT_夜晚\nF12 渲染当前场景。两套场景共享原生可编辑几何，但灯光和世界环境独立。\n白天无建筑照明；夜晚有立面、门廊、鼓座、钟楼和广场灯。\n摄影机 01-09 在 08_CAMERAS_LIGHTS。\n选中摄影机 -> Ctrl+小键盘0 设为当前；小键盘0进入相机视角。\nShift+` 启动步行导航，WASD + 鼠标；Esc退出。\n材质预览模式不代表最终夜间灯光，请选 Rendered 或 F12。\n\n纹理已打包。实景资料、估计范围和命令见 V2_实景核对与使用.md。\n本工程为照片参考的外景重建，非实测数字孪生；室内未建模。\n')
(ROOT/'renders/v2').mkdir(exist_ok=True)
json.dump({'units':'Blender metres; watts are Cycles radiometric power, not electrical consumption','day_artificial_lights':0,'night_lights':lighting_record},open(ROOT/'game/lighting_v2.json','w'),ensure_ascii=False,indent=2)
# Relative image paths are valid on relocation; packed data permits offline render.
for im in bpy.data.images:
 if im.source=='FILE' and im.filepath:
  try:im.filepath='//'+str(Path(im.filepath).relative_to(ROOT))
  except ValueError:pass
print('V2 DAY and NIGHT ready:',len(lighting_record),'night lights',flush=True)

# Save an immersive camera viewport; render samples converge progressively on opening.
for screen in bpy.data.screens:
 for area in screen.areas:
  if area.type=='VIEW_3D':
   sp=area.spaces.active;sp.shading.type='RENDERED';sp.overlay.show_overlays=False;sp.region_3d.view_perspective='CAMERA';sp.region_3d.view_camera_zoom=10;sp.clip_end=1800
for sc in [scene,night]:sc.cycles.preview_samples=24

for sc in [scene,night]:
 for ob in COLS['07_COLLISION'].objects:ob.hide_set(True,view_layer=sc.view_layers[0])
