"""Create separate glTF PBR/mesh exports, without altering the Cycles source .blend."""
import bpy, json, math
import numpy as np
from pathlib import Path
root=Path(bpy.data.filepath).parent
s=next(sc for sc in bpy.data.scenes if sc.get('lighting_mode')=='DAY');bpy.context.window.scene=s
# Export visible models with simplified portable PBR nodes and no render-only bevel.
# Cycles original remains on disk unchanged.
for ob in s.objects:
 ob.select_set(False)
 if ob.type=='MESH' and not ob.hide_render:
  for mod in list(ob.modifiers):
   if ob.name.startswith('SOP_') and mod.type=='BEVEL':
    bpy.context.view_layer.objects.active=ob
    bpy.ops.object.modifier_apply(modifier=mod.name)
   else:ob.modifiers.remove(mod)
# Copy/resample only the transient export datablocks; source .blend stays at 4K.
export_copies={}
for mat in bpy.data.materials:
 if not mat.use_nodes:continue
 for node in mat.node_tree.nodes:
  if node.type=='TEX_IMAGE' and node.image and max(node.image.size)>2048:
   source=node.image
   if source.name not in export_copies:
    cp=source.copy();cp.name=source.name+' game2K';cp.scale(2048,2048);cp.pack();export_copies[source.name]=cp
   node.image=export_copies[source.name]
for mat in bpy.data.materials:
 if not mat.use_nodes:continue
 n=mat.node_tree.nodes;p=n.get('Principled BSDF')
 if p is None:continue
 images={}
 for node in n:
  if node.type=='TEX_IMAGE' and node.image:
   nm=node.image.name
   if '_diff' in nm:images['diff']=node.image
   if '_rough' in nm:images['rough']=node.image
   if '_nor_gl' in nm:images['normal']=node.image
 col=tuple(mat.diffuse_color);rough=p.inputs['Roughness'].default_value;metal=p.inputs['Metallic'].default_value
 n.clear();l=mat.node_tree.links;p=n.new('ShaderNodeBsdfPrincipled');out=n.new('ShaderNodeOutputMaterial');l.new(p.outputs[0],out.inputs['Surface']);p.inputs['Base Color'].default_value=col;p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal
 for typ,img in images.items():
  if typ=='diff' and mat.name.startswith('Arch fired brick'):
   p.inputs['Base Color'].default_value=(.90,.76,.61,1)
  if typ=='diff' and mat.name in ['Historic red brick • CC0 scan','Carved terracotta','Terracotta highlight']:
   factors={'Historic red brick • CC0 scan':(1.15,.81,.64),'Carved terracotta':(1.15,.81,.64),'Terracotta highlight':(1.15,.81,.64)}[mat.name]
   arr=np.array(img.pixels[:],dtype=np.float32).reshape(-1,4);arr[:,:3]*=np.array(factors);arr=np.clip(arr,0,1)
   baked=bpy.data.images.new(mat.name+' portable color',width=img.size[0],height=img.size[1]);baked.pixels.foreach_set(arr.ravel());baked.pack();img=baked
  tex=n.new('ShaderNodeTexImage');tex.image=img
  if typ=='normal':
   normal=n.new('ShaderNodeNormalMap');normal.inputs['Strength'].default_value=.65;l.new(tex.outputs['Color'],normal.inputs['Color']);l.new(normal.outputs[0],p.inputs['Normal'])
  else:l.new(tex.outputs['Color'],p.inputs['Base Color' if typ=='diff' else 'Roughness'])
 if mat.name=='Cream lamp glass':p.inputs['Emission Color'].default_value=(1,.7,.4,1);p.inputs['Emission Strength'].default_value=0
 # Preview diffuse colors for image materials are not reliable; real images above are preserved.
# Portable tiled granite base-color and normal; repeat domain 9.6 m x 7.8 m.
mat=bpy.data.materials['Square granite slabs'];n=mat.node_tree.nodes;l=mat.node_tree.links;p=n.get('Principled BSDF')
W,H=2048,1664;yy,xx=np.mgrid[0:H,0:W];xm=xx/W*9.6;ym=yy/H*7.8
rng=np.random.default_rng(1932);cell=rng.uniform(.26,.39,(12,8));val=cell[np.minimum((ym/.65).astype(int),11),np.minimum((xm/1.2).astype(int),7)]
val+=rng.normal(0,.014,(H,W));edge=(np.minimum(xm%1.2,1.2-xm%1.2)<.006)|(np.minimum(ym%.65,.65-ym%.65)<.006);val[edge]=.09
rgba=np.ones((H,W,4),dtype=np.float32);rgba[:,:,0]=val;rgba[:,:,1]=val*1.005;rgba[:,:,2]=val*.94
im=bpy.data.images.new('Portable granite slabs',width=W,height=H);im.pixels.foreach_set(rgba.ravel());im.pack();tex=n.new('ShaderNodeTexImage');tex.image=im;l.new(tex.outputs['Color'],p.inputs['Base Color'])

for ob in s.objects:
 if ob.type=='MESH' and not ob.hide_render:
  if ob.data.materials:
   name=ob.data.materials[0].name;scale=.88 if name in ['Historic red brick • CC0 scan','Carved terracotta','Terracotta highlight'] else (.55 if name.startswith('Small granite setts') else 1)
   if name=='Square granite slabs':
    for loop in ob.data.uv_layers.active.data:loop.uv.x/=9.6;loop.uv.y/=7.8
   if scale!=1:
    for loop in ob.data.uv_layers.active.data:loop.uv*=scale
  ob.select_set(True)
# Text is converted to polygons for game engines.
for ob in list(s.objects):
 if ob.type=='FONT':
  bpy.ops.object.select_all(action='DESELECT');ob.select_set(True);bpy.context.view_layer.objects.active=ob;bpy.ops.object.convert(target='MESH')
bpy.ops.object.select_all(action='DESELECT')
for ob in s.objects:
 if ob.type=='MESH' and not ob.hide_render:ob.select_set(True)
print('EXPORTING RENDER GLB',flush=True)
bpy.ops.export_scene.gltf(filepath=str(root/'game/Sophia_Square.glb'),export_format='GLB',use_selection=True,export_apply=False,export_cameras=False,export_lights=False,export_extras=True,export_yup=True,export_materials='EXPORT')
# Collision-only GLB, no materials, explicitly disabled by default in Blender source.
bpy.ops.object.select_all(action='DESELECT');coll=bpy.data.collections['07_COLLISION'];coll.hide_render=False
for ob in coll.objects:ob.hide_set(False);ob.hide_render=False;ob.select_set(True)
print('EXPORTING COLLISION GLB',flush=True)
bpy.ops.export_scene.gltf(filepath=str(root/'game/Sophia_Collision.glb'),export_format='GLB',use_selection=True,export_apply=True,export_cameras=False,export_lights=False,export_extras=True,export_materials='NONE')
print('GAME_EXPORT_COMPLETE',flush=True)
