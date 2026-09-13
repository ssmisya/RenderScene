"""Executed inside build_scene.py: 4K scans, metric weathering and surface detail."""
# Keep the original CC0 files; use the separate 4K set.
for im in bpy.data.images:
 if im.name.startswith(('brick_','paving_')):
  candidate=TEX/'v2'/im.name.split('.')[0]
  # Original names end in .jpg; Blender may append a datablock suffix.
  candidate=TEX/'v2'/im.name[:im.name.find('.jpg')+4]
  if candidate.exists():im.filepath=str(candidate);im.reload()
for name in ['Historic red brick • CC0 scan','Carved terracotta','Terracotta highlight']:
 m=M[name];n=m.node_tree.nodes;l=m.node_tree.links;p=n.get('Principled BSDF')
 for node in n:
  if node.type=='MIX_RGB':node.inputs[2].default_value=(1.15,.81,.64,1)
 m.diffuse_color=(.245,.129,.078,1)
 tex=n.new('ShaderNodeTexCoord');mp=n.new('ShaderNodeVectorMath');mp.operation='MULTIPLY';mp.inputs[1].default_value=(2.2,2.2,.20);l.new(tex.outputs['Object'],mp.inputs[0])
 weather=n.new('ShaderNodeTexNoise');weather.label='Vertical rain streaks at metre scale';weather.inputs['Scale'].default_value=1.8;weather.inputs['Detail'].default_value=5;weather.inputs['Roughness'].default_value=.72;l.new(mp.outputs[0],weather.inputs[0])
 ramp=n.new('ShaderNodeValToRGB');ramp.label='Soot and uneven historic masonry';ramp.color_ramp.elements[0].position=.29;ramp.color_ramp.elements[0].color=(.16,.145,.12,1);ramp.color_ramp.elements[1].position=.67;ramp.color_ramp.elements[1].color=(1,.96,.85,1);l.new(weather.outputs['Fac'],ramp.inputs[0])
 src=p.inputs['Base Color'].links[0].from_socket;mix=n.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=.66;l.new(src,mix.inputs[1]);l.new(ramp.outputs[0],mix.inputs[2]);l.new(mix.outputs[0],p.inputs['Base Color'])
 # Actual measured scan height + normal, no subdivision needed for the game mesh.
 scan=n.new('ShaderNodeTexImage');scan.image=bpy.data.images.load(str(TEX/'v2/brick_disp.jpg'),check_existing=True);scan.image.colorspace_settings.name='Non-Color'
 original=next(q for q in n if q.type=='TEX_IMAGE' and q.image and 'brick_diff' in q.image.name)
 l.new(original.inputs[0].links[0].from_socket,scan.inputs[0]);b=n.new('ShaderNodeBump');b.inputs['Distance'].default_value=.014;b.inputs['Strength'].default_value=.48;l.new(scan.outputs[0],b.inputs['Height'])
 if p.inputs['Normal'].links:l.new(p.inputs['Normal'].links[0].from_socket,b.inputs['Normal'])
 l.new(b.outputs[0],p.inputs['Normal'])
# Radial arch segments use individual brick colors; no horizontal mortar scan on a curved arch.
for i in range(14):
 color=(.145+i*.007,.070+i*.0044,.037+i*.0033)
 material('Arch fired brick %02d'%i,color,.86)
 m=M['Arch fired brick %02d'%i];n=m.node_tree.nodes;p=n.get('Principled BSDF');l=m.node_tree.links
 tc=n.new('ShaderNodeTexCoord');mp=n.new('ShaderNodeVectorMath');mp.operation='MULTIPLY';mp.inputs[1].default_value=(1.4,1.4,.28);l.new(tc.outputs['Object'],mp.inputs[0]);no=n.new('ShaderNodeTexNoise');no.inputs['Scale'].default_value=2;no.inputs['Detail'].default_value=4;l.new(mp.outputs[0],no.inputs[0]);ra=n.new('ShaderNodeValToRGB');ra.color_ramp.elements[0].color=(.20,.20,.18,1);ra.color_ramp.elements[1].color=(1,1,.93,1);l.new(no.outputs[0],ra.inputs[0]);mi=n.new('ShaderNodeMixRGB');mi.blend_type='MULTIPLY';mi.inputs[0].default_value=.55;l.new(p.inputs['Base Color'].links[0].from_socket,mi.inputs[1]);l.new(ra.outputs[0],mi.inputs[2]);l.new(mi.outputs[0],p.inputs['Base Color'])
material('Old lime mortar',(.092,.087,.071),.97)
material('Door black lacquer',(.018,.021,.020),.39,.12)
material('Door carved relief',(.024,.027,.025),.5,.08)
material('Old brass hardware',(.24,.16,.065),.46,.72)
material('Painted plaster',(.70,.67,.60),.78)
material('Warm ochre stone',(.48,.36,.19),.8)
material('Cool shop glazing',(.065,.10,.117),.16,.50,False)
material('Red enamel letters',(.35,.013,.014),.41,.25)
material('Dark blue enamel',(.018,.052,.11),.40)
material('Canvas cream',(.50,.43,.29),.95)
material('Canvas green',(.017,.095,.066),.9)
material('Lamp reflector',(.62,.63,.60),.22,.83)
material('Terracotta pots',(.24,.079,.043),.93)
material('Air conditioner casing',(.45,.47,.46),.63,.20)
# Eliminate architectural emission during DAY. NIGHT luminous elements are separate objects.
M['Cream lamp glass'].node_tree.nodes.get('Principled BSDF').inputs['Emission Strength'].default_value=0
# More local variation in stone grains and damp patches, subtle rather than mirror-wet.
m=M['Square granite slabs'];n=m.node_tree.nodes;l=m.node_tree.links;p=n.get('Principled BSDF');tc=n.new('ShaderNodeTexCoord')
no=n.new('ShaderNodeTexNoise');no.inputs['Scale'].default_value=.32;no.inputs['Detail'].default_value=3;l.new(tc.outputs['Object'],no.inputs[0]);ra=n.new('ShaderNodeValToRGB');ra.color_ramp.elements[0].color=(.35,.34,.32,1);ra.color_ramp.elements[0].position=.18;ra.color_ramp.elements[1].color=(1,1,1,1);ra.color_ramp.elements[1].position=.8;l.new(no.outputs[0],ra.inputs[0]);mi=n.new('ShaderNodeMixRGB');mi.blend_type='MULTIPLY';mi.inputs[0].default_value=.5;l.new(p.inputs['Base Color'].links[0].from_socket,mi.inputs[1]);l.new(ra.outputs[0],mi.inputs[2]);l.new(mi.outputs[0],p.inputs['Base Color'])
rough=n.new('ShaderNodeMapRange');rough.inputs['To Min'].default_value=.48;rough.inputs['To Max'].default_value=.84;l.new(no.outputs[0],rough.inputs[0]);l.new(rough.outputs[0],p.inputs['Roughness'])
# Subtle crown weathering: hand-painted sheet colors remain independently editable.
for i in range(9):
 m=M['Painted roof %02d'%i];n=m.node_tree.nodes;p=n.get('Principled BSDF');p.inputs['Metallic'].default_value=.36;p.inputs['Roughness'].default_value=.49+i*.017
 for q in n:
  if q.type=='VALTORGB':
   col=(.011+i*.0014,.036+i*.0021,.027+i*.0019);q.color_ramp.elements[0].color=(*(v*.48 for v in col),1);q.color_ramp.elements[1].color=(*(v*1.23 for v in col),1)
# Real scanned brick-face detail on each independently UV-mapped voussoir.
for i in range(14):
 m=M['Arch fired brick %02d'%i];n=m.node_tree.nodes;l=m.node_tree.links;p=n.get('Principled BSDF')
 for suf,socket in [('diff','Base Color'),('rough','Roughness'),('nor_gl','Normal')]:
  im=n.new('ShaderNodeTexImage');im.image=bpy.data.images.load(str(TEX/f'v2/brick_face_{suf}.jpg'),check_existing=True)
  if suf!='diff':im.image.colorspace_settings.name='Non-Color'
  if suf=='diff':
   tint=n.new('ShaderNodeMixRGB');tint.blend_type='MULTIPLY';tint.inputs[0].default_value=1;fac=.76+i*.043;tint.inputs[2].default_value=(fac,fac*.83,fac*.66,1);l.new(im.outputs[0],tint.inputs[1]);l.new(tint.outputs[0],p.inputs['Base Color'])
   tc=n.new('ShaderNodeTexCoord');mp=n.new('ShaderNodeVectorMath');mp.operation='MULTIPLY';mp.inputs[1].default_value=(1.5,1.5,.30);l.new(tc.outputs['Object'],mp.inputs[0]);no=n.new('ShaderNodeTexNoise');no.inputs['Scale'].default_value=2.0;l.new(mp.outputs[0],no.inputs[0]);ra=n.new('ShaderNodeValToRGB');ra.color_ramp.elements[0].position=.35;ra.color_ramp.elements[0].color=(.16,.18,.16,1);ra.color_ramp.elements[1].position=.64;ra.color_ramp.elements[1].color=(1,1,1,1);l.new(no.outputs[0],ra.inputs[0]);mi=n.new('ShaderNodeMixRGB');mi.blend_type='MULTIPLY';mi.inputs[0].default_value=.70;l.new(tint.outputs[0],mi.inputs[1]);l.new(ra.outputs[0],mi.inputs[2]);l.new(mi.outputs[0],p.inputs['Base Color'])
  elif suf=='nor_gl':
   nm=n.new('ShaderNodeNormalMap');nm.inputs['Strength'].default_value=.78;l.new(im.outputs[0],nm.inputs['Color']);l.new(nm.outputs[0],p.inputs['Normal'])
  else:l.new(im.outputs[0],p.inputs[socket])
for name in ['Door black lacquer','Door carved relief','Old brass hardware']:
 for node in M[name].node_tree.nodes:
  if node.type=='BUMP':node.inputs['Distance'].default_value=.00035;node.inputs['Strength'].default_value=.20
material('Door smoked glass',(.008,.013,.015),.20,.30,False)
m=M['Old glass'];m.diffuse_color=(.15,.18,.18,1);p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(.15,.18,.18,1);p.inputs['Metallic'].default_value=.18;p.inputs['Roughness'].default_value=.29
for name in ['Historic red brick • CC0 scan','Carved terracotta','Terracotta highlight']:
 for node in M[name].node_tree.nodes:
  if node.type=='VALTORGB' and node.label=='Soot and uneven historic masonry':
   node.color_ramp.elements[0].position=.38;node.color_ramp.elements[0].color=(.10,.12,.105,1);node.color_ramp.elements[1].position=.61
