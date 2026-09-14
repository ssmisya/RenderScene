"""Harbin Sophia Square — photo-informed, metre-scale exterior map.
Run with Blender 5.2+: blender -b --python build_scene.py
Public reference provenance is in REFERENCES.md. No survey accuracy is claimed.
"""
import bpy, math, random, json, os, sys, argparse
from mathutils import Vector
from pathlib import Path
from collections import defaultdict
from math import sin, cos, pi
ROOT=Path(__file__).resolve().parents[1]
random.seed(1932)
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
for c in list(bpy.data.collections):
 if c.name!='Collection': bpy.data.collections.remove(c)
scene=bpy.context.scene
scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=1
COLS={}
for name in ['01_CATHEDRAL','02_SQUARE','03_OSM_BUILDINGS','04_VEGETATION','05_STREET_PROPS','06_ROADS','07_COLLISION','08_CAMERAS_LIGHTS','09_GAME_MARKERS']:
 c=bpy.data.collections.new(name); scene.collection.children.link(c);COLS[name]=c
M={}; TEX=ROOT/'assets/textures'
def material(name,color,rough=.65,metal=0,noise=True):
 m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True
 n=m.node_tree.nodes;l=m.node_tree.links;p=n.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1);p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal
 if noise:
  tc=n.new('ShaderNodeTexCoord'); tex=n.new('ShaderNodeTexNoise');tex.inputs['Scale'].default_value=4.5;tex.inputs['Detail'].default_value=4;l.new(tc.outputs['Object'],tex.inputs['Vector'])
  ramp=n.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].position=.15;ramp.color_ramp.elements[0].color=(*(v*.55 for v in color),1);ramp.color_ramp.elements[1].position=.85;ramp.color_ramp.elements[1].color=(*(min(1,v*1.3) for v in color),1);l.new(tex.outputs['Fac'],ramp.inputs[0]);l.new(ramp.outputs[0],p.inputs['Base Color'])
  micro=n.new('ShaderNodeTexNoise');micro.inputs['Scale'].default_value=90;micro.inputs['Detail'].default_value=2;l.new(tc.outputs['Object'],micro.inputs['Vector']);b=n.new('ShaderNodeBump');b.inputs['Strength'].default_value=.3;b.inputs['Distance'].default_value=.012;l.new(micro.outputs['Fac'],b.inputs['Height']);l.new(b.outputs[0],p.inputs['Normal'])
 M[name]=m;return m

def pbr(name,prefix,scale=1):
 m=material(name,(.3,.2,.15),noise=False);n=m.node_tree.nodes;l=m.node_tree.links;p=n.get('Principled BSDF')
 uv=n.new('ShaderNodeTexCoord');mp=n.new('ShaderNodeVectorMath');mp.operation='SCALE';mp.inputs[3].default_value=scale;l.new(uv.outputs['UV'],mp.inputs[0])
 for suf,socket in [('diff','Base Color'),('rough','Roughness'),('nor_gl','Normal')]:
  im=n.new('ShaderNodeTexImage');im.image=bpy.data.images.load(str(TEX/(prefix+'_'+suf+'.jpg')),check_existing=True);l.new(mp.outputs[0],im.inputs[0])
  if suf!='diff':im.image.colorspace_settings.name='Non-Color'
  if suf=='nor_gl':
   nm=n.new('ShaderNodeNormalMap');nm.inputs['Strength'].default_value=.65;l.new(im.outputs[0],nm.inputs['Color']);l.new(nm.outputs[0],p.inputs[socket])
  else:l.new(im.outputs[0],p.inputs[socket])
 return m
pbr('Historic red brick • CC0 scan','brick',.88)
pbr('Small granite setts • CC0 scan','paving',.55)
material('Carved terracotta',(.30,.108,.046),.8)
material('Terracotta highlight',(.41,.174,.073),.78)
material('Recessed soot',(.056,.035,.027),.93)
material('Granite foundation',(.24,.252,.237),.83)
material('Limestone facade',(.60,.55,.42),.8)
material('Ivory cornice',(.76,.73,.62),.74)
material('Sandstone facade',(.40,.32,.22),.83)
material('Roof burgundy',(.115,.029,.021),.5,.25)
material('Iron dark green',(.016,.042,.037),.5,.6)
material('Dome seams',(.007,.017,.015),.64,.6)
for i in range(9):material('Painted roof %02d'%i,(.015+i*.0027,.058+i*.0055,.045+i*.0047),.30+i*.036,.58)
material('Gold leaf',(.58,.32,.060),.25,.8)
material('Window lead',(.21,.26,.24),.48,.6)
material('Old glass',(.070,.12,.135),.19,.42,False)
material('Window shadow',(.008,.012,.012),.63,0,False)
material('Timber doors',(.043,.027,.022),.75)
material('Timber seat',(.19,.082,.024),.65)
material('Iron black',(.014,.021,.019),.48,.75)
material('Asphalt',(.049,.052,.052),.96)
material('Road paint',(.72,.68,.52),.79)
material('Grate',(.035,.039,.035),.9,.65)
material('Soil',(.051,.043,.022),1)
material('Bark',(.105,.070,.033),.95)
for i in range(8):material('Leaves %02d'%i,(.028+i*.012,.057+i*.017,.011+i*.004),.9,0)
material('Cream lamp glass',(.85,.77,.57),.22,0,False)
p=M['Cream lamp glass'].node_tree.nodes.get('Principled BSDF');p.inputs['Emission Color'].default_value=(1,.67,.30,1);p.inputs['Emission Strength'].default_value=.3
material('Sign enamel',(.025,.079,.083),.42,.1)
material('Fountain water',(.024,.069,.067),.12,.1)
p=M['Fountain water'].node_tree.nodes.get('Principled BSDF');p.inputs['Transmission Weight'].default_value=.48;p.inputs['IOR'].default_value=1.333
# Large format granite slabs, metric coordinates; irregular tonal variation and grit.
m=material('Square granite slabs',(.31,.32,.30),.8,noise=False);n=m.node_tree.nodes;l=m.node_tree.links;p=n.get('Principled BSDF');tc=n.new('ShaderNodeTexCoord')
bt=n.new('ShaderNodeTexBrick');l.new(tc.outputs['UV'],bt.inputs['Vector']);bt.inputs['Scale'].default_value=1;bt.inputs['Brick Width'].default_value=1.2;bt.inputs['Row Height'].default_value=.65;bt.inputs['Mortar Size'].default_value=.004;bt.inputs['Mortar Smooth'].default_value=.004;bt.inputs['Color1'].default_value=(.28,.285,.267,1);bt.inputs['Color2'].default_value=(.41,.407,.374,1);bt.inputs['Mortar'].default_value=(.081,.085,.076,1);bt.offset=.0
noise=n.new('ShaderNodeTexNoise');l.new(tc.outputs['Object'],noise.inputs[0]);noise.inputs['Scale'].default_value=18;noise.inputs['Detail'].default_value=4
mix=n.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=.23;l.new(bt.outputs['Color'],mix.inputs[1]);l.new(noise.outputs['Fac'],mix.inputs[2]);l.new(mix.outputs[0],p.inputs['Base Color'])
b=n.new('ShaderNodeBump');b.inputs['Distance'].default_value=.01;b.inputs['Strength'].default_value=.6;b.invert=True;l.new(bt.outputs['Fac'],b.inputs['Height']);l.new(b.outputs[0],p.inputs['Normal'])

# The carved brick trim should share the historic masonry color, not glossy orange.
for trim_name,factor in [('Carved terracotta',1.15),('Terracotta highlight',1.26)]:
 old=M[trim_name];old.name=trim_name+' unused';m=pbr(trim_name,'brick',.88);m.diffuse_color=(.27,.135,.077,1)
 p=m.node_tree.nodes.get('Principled BSDF');l=m.node_tree.links;n=m.node_tree.nodes
 oldlink=p.inputs['Base Color'].links[0];src=oldlink.from_socket;l.remove(oldlink)
 mix=n.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(factor*1.20,factor*.61,factor*.38,1);l.new(src,mix.inputs[1]);l.new(mix.outputs[0],p.inputs['Base Color'])
# Match the orange-red historic masonry rather than a desaturated gray scan.
m=M['Historic red brick • CC0 scan'];p=m.node_tree.nodes.get('Principled BSDF');l=m.node_tree.links;n=m.node_tree.nodes
oldlink=p.inputs['Base Color'].links[0];src=oldlink.from_socket;l.remove(oldlink)
mix=n.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(1.26,.64,.41,1);l.new(src,mix.inputs[1]);l.new(mix.outputs[0],p.inputs['Base Color'])

# Subtler green paint variation makes the real metal sheet geometry legible.
for i in range(9):
 m=M['Painted roof %02d'%i];n=m.node_tree.nodes;p=n.get('Principled BSDF');p.inputs['Roughness'].default_value=.46+i*.012;p.inputs['Metallic'].default_value=.50
 color=(.013+i*.0012,.045+i*.0022,.034+i*.0018);m.diffuse_color=(*color,1)
 for node in n:
  if node.type=='VALTORGB':
   node.color_ramp.elements[0].color=(*(v*.9 for v in color),1);node.color_ramp.elements[1].color=(*(v*1.1 for v in color),1)

exec(compile((ROOT/'scripts/v2_materials.py').read_text(),str(ROOT/'scripts/v2_materials.py'),'exec'))

# Batched native mesh geometry. Collections and group names retain editing structure.
B={};ACTIVE='01_CATHEDRAL';GROUP='Masonry';collision=[]
def add(verts,faces,mat,smooth=False,uv=None):
 key=(ACTIVE,GROUP,mat)
 if key not in B:B[key]=[[],[],[],[]]
 v,f,sm,uvs=B[key];o=len(v);v.extend(verts)
 for face in faces:
  f.append(tuple(o+i for i in face));sm.append(smooth)
  if uv is not None:uvs.append([uv[i] for i in face])
  else:
   pts=[Vector(verts[i]) for i in face];norm=(pts[1]-pts[0]).cross(pts[2]-pts[0]);norm.normalize()
   if abs(norm.z)>.65: uvs.append([(p.x,p.y) for p in pts])
   else:
    tangent=Vector((-norm.y,norm.x,0));tangent.normalize();uvs.append([(p.dot(tangent),p.z) for p in pts])
def box(name,loc,size,mat,angle=0,collide=False):
 x,y,z=loc;a,b,c=[v/2 for v in size];co=cos(angle);si=sin(angle)
 vs=[(x+u*co-v*si,y+u*si+v*co,z+w) for u,v,w in [(-a,-b,-c),(a,-b,-c),(a,b,-c),(-a,b,-c),(-a,-b,c),(a,-b,c),(a,b,c),(-a,b,c)]]
 add(vs,[(0,3,2,1),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,6,7)],mat)
 if collide:collision.append({'name':name,'type':'box','center':loc,'size':size,'rotation_z':angle})
def lathe(loc,profile,mat,N=64,phase=0,smooth=True):
 x,y,z=loc;vs=[];uv=[]
 for r,h in profile:
  for i in range(N+1):
   a=2*pi*i/N+phase;vs.append((x+r*cos(a),y+r*sin(a),z+h));uv.append((i/N*2*pi*max(r,.05),z+h))
 fs=[]
 for j in range(len(profile)-1):
  for i in range(N):a=j*(N+1)+i;fs.append((a,a+1,a+N+2,a+N+1))
 add(vs,fs,mat,smooth,uv)
def cylinder(loc,r,h,mat,N=32):lathe(loc,[(0,0),(r,0),(r,h),(0,h)],mat,N)
def beam(a,b,r,mat,N=8,r2=None):
 a=Vector(a);b=Vector(b);d=(b-a).normalized();u=d.cross(Vector((0,0,1)))
 if u.length<.001:u=d.cross(Vector((0,1,0)))
 u.normalize();v=d.cross(u);vs=[]
 for pt,rr in [(a,r),(b,r if r2 is None else r2)]:
  for i in range(N):vs.append(tuple(pt+rr*(cos(2*pi*i/N)*u+sin(2*pi*i/N)*v)))
 fs=[tuple(range(N-1,-1,-1)),tuple(range(N,2*N))]+[(i,(i+1)%N,(i+1)%N+N,i+N) for i in range(N)];add(vs,fs,mat,True)
def path(points,r,mat,N=6):
 for a,b in zip(points,points[1:]):beam(a,b,r,mat,N)
def sphere(loc,r,mat,scale=(1,1,1),N=12,rings=8):
 vs=[]
 for j in range(rings+1):
  a=pi*j/rings
  for i in range(N):b=2*pi*i/N;vs.append((loc[0]+r*sin(a)*cos(b)*scale[0],loc[1]+r*sin(a)*sin(b)*scale[1],loc[2]+r*cos(a)*scale[2]))
 fs=[]
 for j in range(rings):
  for i in range(N):a=j*N+i;b=j*N+(i+1)%N;fs.append((a,b,b+N,a+N))
 add(vs,fs,mat,True)
def extrude_poly(poly,z,h,mat):
 poly=poly[:-1] if poly[0]==poly[-1] else poly;n=len(poly)
 area=sum(poly[i][0]*poly[(i+1)%n][1]-poly[(i+1)%n][0]*poly[i][1] for i in range(n))
 if area<0:poly=list(reversed(poly))
 vs=[(x,y,zz) for zz in [z,z+h] for x,y in poly];fs=[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)];add(vs,fs,mat)
 return poly
# A facade frame has horizontal coordinate u, height v and outward distance d.
def frame(center,normal):
 nx,ny=normal;ux,uy=ny,-nx
 return lambda u,v,d=0:(center[0]+u*ux+d*nx,center[1]+u*uy+d*ny,center[2]+v)
def fbox(F,u,z,d,w,h,depth,mat):
 vs=[F(u+a,z+b,d+c) for a,b,c in [(-w/2,-h/2,-depth/2),(w/2,-h/2,-depth/2),(w/2,h/2,-depth/2),(-w/2,h/2,-depth/2),(-w/2,-h/2,depth/2),(w/2,-h/2,depth/2),(w/2,h/2,depth/2),(-w/2,h/2,depth/2)]]
 add(vs,[(0,1,2,3),(4,7,6,5),(0,4,5,1),(1,5,6,2),(2,6,7,3),(3,7,4,0)],mat)
def arc(F,u,spring,r,width,d,mat,N=24,start=0,end=pi):
 vs=[]
 for a in [start+(end-start)*i/N for i in range(N+1)]:
  for rr,dd in [(r,d),(r+width,d),(r,d+.13),(r+width,d+.13)]:vs.append(F(u+rr*cos(a),spring+rr*sin(a),dd))
 fs=[]
 for i in range(N):k=4*i;fs.extend([(k,k+4,k+5,k+1),(k+2,k+3,k+7,k+6),(k,k+2,k+6,k+4),(k+1,k+5,k+7,k+3)])
 add(vs,fs,mat)
def arch_panel(F,u,z,w,h,d,mat):
 r=w/2;spring=z+h-r
 pts=[F(u-r,z,d),F(u+r,z,d)]+[F(u+r*cos(i*pi/24),spring+r*sin(i*pi/24),d) for i in range(25)]
 add(pts,[tuple(range(len(pts)))],mat)
def crown(F,u,z,r,d=.35,filled=False):
 if filled:arch_panel(F,u,z-.02,2*(r+.30),r+.32,d-.06,'Historic red brick • CC0 scan')
 # Russian kokoshnik: nested rounded archivolts with a raised point.
 for k in range(3):arc(F,u,z,r+k*.13,.09,d+k*.045,'Carved terracotta',20)
 vs=[F(u-r*.40,z+r*.95,d),F(u,z+r*1.55,d),F(u+r*.40,z+r*.95,d),F(u-r*.40,z+r*.95,d+.13),F(u,z+r*1.55,d+.13),F(u+r*.40,z+r*.95,d+.13)]
 add(vs,[(0,1,2),(3,5,4),(0,3,4,1),(1,4,5,2)],'Carved terracotta')
 path([F(u-r*.4,z+r*.95,d+.17),F(u,z+r*1.55,d+.17),F(u+r*.4,z+r*.95,d+.17)],.055,'Terracotta highlight')
def window(F,u,z,w,h,ornate=True,glass='Old glass'):
 r=w/2;sp=z+h-r
 arch_panel(F,u,z,w+.22,h+.13,.025,'Window shadow');arch_panel(F,u,z+.10,w-.16,h-.19,.075,glass)
 for k in range(3 if ornate else 1):
  rr=r+.05+k*.14;arc(F,u,sp,rr,.095,.15+k*.05,'Carved terracotta' if k else 'Window lead')
  for side in [-1,1]:fbox(F,u+side*(rr+.045),(z+sp)/2,.2+k*.05,.095,sp-z,.16,'Carved terracotta' if k else 'Window lead')
 fbox(F,u,z-.05,.25,w+.65,.16,.48,'Carved terracotta')
 for du in [-w*.24,0,w*.24]:
  top=sp+math.sqrt(max(0,(r-.13)**2-du**2));fbox(F,u+du,(z+.16+top)/2,.15,.027,top-z-.16,.035,'Window lead')
 for zz in [z+.35+i*.47 for i in range(max(1,int((h-r-.35)/.47)))]:fbox(F,u,zz,.16,w-.25,.029,.035,'Window lead')
 # Circular tracery and flower at arched head; geometric metal, not painted detail.
 circle=[F(u+(r*.59)*cos(i*2*pi/20),sp+(r*.59)*sin(i*2*pi/20),.18) for i in range(21)];path(circle,.023,'Window lead',4)
 for a in range(8):
  aa=a*pi/4;path([F(u,sp,.18),F(u+r*.62*cos(aa),sp+r*.62*sin(aa),.18)],.018,'Window lead',4)
 if ornate:
  crown(F,u,sp,r+.43,.32)
  for side in [-1,1]:
   for zz in [z+.5+i*.64 for i in range(int((sp-z)/.64))]:fbox(F,u+side*(r+.40),zz,.3,.22,.17,.24,'Terracotta highlight')
def portal(F,w=3.2,h=5.5):
 arch_panel(F,0,.15,w,h,.09,'Timber doors')
 for k in range(7):
  r=w/2+.12+k*.27;arc(F,0,h-w/2,r,.14,.22+k*.06,'Carved terracotta',40)
  for s in [-1,1]:fbox(F,s*(r+.06),(h-w/2+.15)/2,.27+k*.06,.15,h-w/2-.15,.22,'Carved terracotta')
 for s in [-1,1]:
  for z in [.75,2,3.25]:fbox(F,s*w*.235,z,.16,w*.40,1.06,.06,'Timber doors')
  fbox(F,s*.19,2.2,.23,.05,.45,.07,'Iron black')
 fbox(F,0,(h-w/2)/2,.18,.05,h-w/2,.08,'Iron black')
 for i in range(43):
  a=i*pi/42;r=w/2+1.44;fbox(F,r*cos(a),h-w/2+r*sin(a),.58,.09,.13,.1,'Recessed soot')

def cornice_rect(cx,cy,sx,sy,z):
 for dz,grow,h in [(0,.0,.15),(.17,.15,.11),(.3,.26,.16),(.47,.36,.1)]:box('',(cx,cy,z+dz),(sx+grow,sy+grow,h),'Carved terracotta')
 for side in [-1,1]:
  for u in range(int(sx/.4)):box('',(cx-sx/2+.2+u*.4,cy+side*(sy/2+.05),z-.16),(.18,.25,.20),'Terracotta highlight')
  for u in range(int(sy/.4)):box('',(cx+side*(sx/2+.05),cy-sy/2+.2+u*.4,z-.16),(.25,.18,.20),'Terracotta highlight')
def hiproof(cx,cy,sx,sy,z,h,mat='Painted roof 03'):
 topx=max(.1,sx-sy)*.5;vs=[(cx-sx/2,cy-sy/2,z),(cx+sx/2,cy-sy/2,z),(cx+sx/2,cy+sy/2,z),(cx-sx/2,cy+sy/2,z),(cx-topx,cy,z+h),(cx+topx,cy,z+h)]
 add(vs,[(0,1,5,4),(1,2,5),(2,3,4,5),(3,0,4)],mat)
 for face in [(0,1,5,4),(2,3,4,5)]:
  a,b,c,d=[Vector(vs[i]) for i in face]
  for t in [i/28 for i in range(29)]:beam(a.lerp(b,t)+Vector((0,0,.02)),d.lerp(c,t)+Vector((0,0,.02)),.024,'Dome seams',5)
def cross(x,y,z,h=2.4):
 beam((x,y,z),(x,y,z+h),.062,'Gold leaf',10)
 for zz,ww in [(z+h*.68,h*.72),(z+h*.89,h*.37)]:beam((x,y-ww/2,zz),(x,y+ww/2,zz),.063,'Gold leaf',10)
 beam((x,y-h*.2,z+h*.30),(x,y+h*.2,z+h*.19),.043,'Gold leaf',8)
 for yy,zz in [(0,z+h),(-h*.36,z+h*.68),(h*.36,z+h*.68)]:sphere((x,y+yy,zz),.10,'Gold leaf',N=10,rings=6)
def gilded_finial(x,y,z,scale=1):
 pr=[(.23,0),(.35,.15),(.23,.35),(.19,.9),(.60,1.35),(.65,1.60),(.5,1.85),(.20,2.15),(.07,2.6)]
 lathe((x,y,z),[(r*scale,h*scale) for r,h in pr],'Gold leaf',48)
 cross(x,y,z+2.55*scale,2.2*scale)
def tent(x,y,z,r,h):
 lathe((x,y,z),[(r,0),(r*.83,h*.22),(.38,h)],'Dome seams',8,pi/8,False)
 for i in range(8):a=2*pi*i/8+pi/8;beam((x+r*cos(a),y+r*sin(a),z),(x+.38*cos(a),y+.38*sin(a),z+h),.048,'Iron dark green',6)
 # Individually modeled diamond sheets on all eight planar tent faces.
 def R(t):
  return r+(r*.83-r)*t/.22 if t<.22 else r*.83+(.38-r*.83)*(t-.22)/.78
 cols=14;rows=max(14,int(h/.30))
 for k in range(8):
  a=k*pi/4+pi/8;b=a+pi/4;normal=Vector((cos((a+b)/2),sin((a+b)/2),.20)).normalized()
  def P(u,t):
   rr=R(t);return tuple(Vector((x+rr*((1-u)*cos(a)+u*cos(b)),y+rr*((1-u)*sin(a)+u*sin(b)),z+h*t))+normal*.026)
  for j in range(1,rows):
   for i in range(1,cols):
    if (i+j)%2:continue
    u=i/cols;t=j/rows;du=.94/cols;dt=.94/rows
    verts=[P(u-du,t),P(u,t+dt),P(u+du,t),P(u,t-dt)]
    add(verts,[(0,1,2,3)],'Painted roof %02d'%random.randrange(9))

 # Raised diagonal sheet seams, projected onto the octagonal conical faces.
 for k in range(8):
  a=2*pi*k/8+pi/8;b=a+pi/4
  for j in range(1,int(h/.5)):
   t=j*.5/h;rr=r*(1-t)+.38*t;beam((x+rr*cos(a),y+rr*sin(a),z+j*.5),(x+rr*cos(b),y+rr*sin(b),z+j*.5),.018,'Dome seams',4)
 gilded_finial(x,y,z+h,.72)

exec(compile((ROOT/'scripts/v2_architecture.py').read_text(),str(ROOT/'scripts/v2_architecture.py'),'exec'))

# --- Cathedral. Main axis +X toward the east apse, west door at -X. ---
GROUP='01_Foundation_and_cruciform_shell'
brick='Historic red brick • CC0 scan'
# Footprint proportions use published approximately 42 m length, 28 m overall width.
box('nave lower aisles',(-5.0,0,8.45),(30.0,15.0,15.3),brick,collide=True)
box('nave raised central bay',(-5.0,0,10.3),(30.0,9.3,19.0),brick,collide=True)
box('crossing',(2.0,0,12.6),(16.0,16.0,23.6),brick,collide=True)
for sy in [-1,1]:box('transept',(2,sy*9.6,8.9),(13.0,8.8,16.2),brick,collide=True)
lathe((13.5,0,.8),[(0,0),(7.0,0),(7.0,14.5),(6.8,16.1),(0,16.1)],brick,48,smooth=False)
collision.append({'name':'east_apse','type':'cylinder','center':[13.5,0,8.5],'radius':7,'height':15.4})
for cx,cy,sx,sy in [(-5,0,30.6,15.6),(2,0,16.6,16.6),(2,-9.6,13.6,9.4),(2,9.6,13.6,9.4)]:
 box('',(cx,cy,.65),(sx,sy,1.3),'Granite foundation')
 for z,ext in [(1.40,.10),(1.62,.10),(4.7,.10)]:box('',(cx,cy,z),(sx-.6+ext,sy-.6+ext,.12),'Carved terracotta')
 cornice_rect(cx,cy,sx-.5,sy-.5,4.95)
lathe((13.5,0,0),[(7.2,0),(7.2,1.2),(7.1,1.4),(7.4,1.55),(7.15,1.7),(7.15,4.7),(7.45,4.9),(7.45,5.1),(7.2,5.3)],'Carved terracotta',48,smooth=False)
# Nave/wing eaves and sheet-metal roofs.
for cx,cy,sx,sy,z,h in [(-7,0,27,9.6,19.8,1.0),(2,0,16.6,16.6,24,2.1),(2,-9.6,13.6,9.0,17,2),(2,9.6,13.6,9,17,2)]:cornice_rect(cx,cy,sx,sy,z-.5);hiproof(cx,cy,sx,sy,z,h)
lathe((13.5,0,16.8),[(7.3,0),(7.3,.2),(2.6,3.0)],'Painted roof 04',48,smooth=False)
GROUP='02_Nave_windows_and_brick_carving'
for sy in [-1,1]:
 F=frame((-13,sy*7.52,0),(0,sy))
 for u in [-5,-1.7,1.7,5]:
  window(F,u,5.8,1.60,7.5)
  window(F,u,2.05,1.2,2.2,False,glass='Window shadow')
 for u in [-6.5,-3.3,0,3.3,6.5]:
  fbox(F,u,9.9,.12,.52,11.9,.30,brick)
  for z in [6+i*.65 for i in range(14)]:fbox(F,u,z,.32,.38,.22,.23,'Carved terracotta')
 for u in [-5,-1.7,1.7,5]:crown(F,u,15.85,.85,filled=True)
# Wing round ends with paired tall arched windows.
for sy in [-1,1]:
 F=frame((2,sy*14.02,0),(0,sy))
 for u in [-4.4,-1.5,1.5,4.4]:window(F,u,6.1,1.4,6.2)
 for u in [-6,-3,0,3,6]:
  fbox(F,u,10.6,.1,.60,12.7,.30,brick)
  for z in [6.3+i*.75 for i in range(14)]:fbox(F,u,z,.29,.38,.18,.16,'Carved terracotta')
 for u in [-4.5,-1.5,1.5,4.5]:crown(F,u,16.6,.75,filled=True)
 # West-facing ears with small portals.
 F=frame((-4.53,sy*10,0),(-1,0));portal(F,2.25,4.4);window(F,0,8.1,1.8,5.1)
# Exposed central crossing upper faces.
for normal,center in [((0,-1),(2,-8.02,0)),((0,1),(2,8.02,0)),((1,0),(10.02,0,0))]:
 F=frame(center,normal)
 for u in [-5.2,0,5.2]:window(F,u,17.8,1.25,4.5,True)
 for u in [-6.8,-2.5,2.5,6.8]:fbox(F,u,20.4,.2,.6,7,.45,brick)
 for u in [-5.6,-2.8,0,2.8,5.6]:crown(F,u,24,.80,filled=True)
# Recess-like lower-wall decorative panels, with profile depth.
for sy in [-1,1]:
 F=frame((-13,sy*7.54,0),(0,sy))
 for u in [-5,-1.7,1.7,5]:
  fbox(F,u,15.3,.12,2.05,.86,.11,'Recessed soot');fbox(F,u,15.3,.19,1.8,.65,.09,brick)
 for z in [14.5,15.35,15.85]:
  fbox(F,0,z,.22,13.7,.12,.3,'Carved terracotta')
  for u in [-6.6+i*.35 for i in range(39)]:fbox(F,u,z-.18,.17,.15,.16,.23,'Carved terracotta')

GROUP='03_East_apse'
for k in range(9):
 a=-pi/2+k*pi/8;F=frame((13.5+7.015*cos(a),7.015*sin(a),0),(cos(a),sin(a)))
 window(F,0,6.1,1.40,6.8)
 fbox(F,1.13,9.8,.20,.34,11,.30,brick);crown(F,0,16.65,.71,filled=True)
# Low polygonal sanctuary/entrance on the east.
lathe((18,0,.2),[(0,0),(4.2,0),(4.2,6.5),(4.4,6.7),(4.4,6.9),(2.1,8.6)],brick,8,pi/8,False)
lathe((18,0,6.9),[(4.5,0),(1.7,1.8)],'Painted roof 04',8,pi/8,False)
F=frame((21.9,0,.3),(1,0));portal(F,2.1,4.2)
for sy in [-1,1]:
 F=frame((18,sy*3.9,0),(0,sy));window(F,0,1.8,1.2,3.7)
lathe((20.0,0,6.85),[(2,0),(2,3.8),(2.3,3.85)],brick,8,pi/8,False)
for k in range(8):
 a=k*pi/4;F=frame((20.0+1.85*cos(a),1.85*sin(a),0),(cos(a),sin(a)));crown(F,0,10.3,.65,filled=True)
tent(20.0,0,10.7,2.3,4.5)
# Side towers on north/south wings, octagonal brick drums.
GROUP='04_Transept_towers'
for sy in [-1,1]:
 cx,cy=2,sy*10.1
 lathe((cx,cy,16.8),[(3.35,0),(3.35,4.4),(3.6,4.6),(3.6,4.9)],brick,8,pi/8,False)
 for k in range(8):
  a=k*pi/4;F=frame((cx+3.1*cos(a),cy+3.1*sin(a),0),(cos(a),sin(a)))
  window(F,0,18.1,1.15,2.5,False);crown(F,0,21.2,1.0,filled=True)
 tent(cx,cy,22.4,3.9,7.6)
exec(compile((ROOT/'scripts/v21_west.py').read_text(),str(ROOT/'scripts/v21_west.py'),'exec'))
# Large central drum, 16 windows with pilasters, two ornamental arcade tiers.
GROUP='06_Main_drum'
cx,cy=2.0,0
lathe((cx,cy,25.4),[(5.8,0),(5.8,.65),(6.1,.9),(6.1,1.15),(5.70,1.3),(5.70,10.5),(6.08,10.8),(6.08,11),(6.3,11.2),(6.3,13.25),(6.50,13.5)],brick,16,pi/16,False)
for k in range(16):
 a=k*2*pi/16;F=frame((cx+5.61*cos(a),cy+5.61*sin(a),0),(cos(a),sin(a)))
 window(F,0,27.6,1.32,6.6,True)
 fbox(F,1.05,31.5,.21,.26,9.7,.34,brick)
 for zz in [27.3+i*.61 for i in range(15)]:fbox(F,1.05,zz,.4,.30,.16,.18,'Carved terracotta')
 crown(F,0,35.6,.87,.31,filled=True)
 for du in [-.52,.52]:arc(F,du,37.2,.38,.10,.24,'Carved terracotta',14)
# Upper drum arcade is placed on the outward circular frieze, not buried in it.
for k in range(40):
 a=k*2*pi/40;F=frame((cx+6.28*cos(a),cy+6.28*sin(a),0),(cos(a),sin(a)))
 arch_panel(F,0,36.96,.54,.87,.075,'Recessed soot')
 for q in range(3):arc(F,0,37.43,.27+q*.11,.074,.11+q*.05,'Carved terracotta',12)
 for u in [-.42,.42]:fbox(F,u,37.12,.13,.11,.35,.15,'Carved terracotta')

for z,r in [(36.4,5.95),(36.65,6.05),(38.0,6.2),(38.35,6.32),(38.65,6.43),(38.95,6.50)]:lathe((cx,cy,z),[(r,0),(r+.05,.12),(r,.19)],'Carved terracotta',96)
for i in range(112):
 a=i*2*pi/112;box('',(cx+6.35*cos(a),cy+6.35*sin(a),38.68),(.15,.16,.16),'Terracotta highlight',a)
GROUP='07_Main_onion_diamond_sheet_roof'
profile=[(6.40,39.05),(6.72,39.75),(7.07,40.9),(7.25,42.1),(7.13,43.4),(6.69,44.6),(5.97,45.7),(4.87,46.75),(3.45,47.7),(2.05,48.45),(.87,49.02),(.35,49.40)]
lathe((cx,cy,0),profile,'Dome seams',128)
def radius_at(z):
 for (r0,z0),(r1,z1) in zip(profile,profile[1:]):
  if z0<=z<=z1:return r0+(r1-r0)*(z-z0)/(z1-z0)
 return profile[-1][0]
# Rhombus metal sheets; visible seam gaps are geometry.
rows=42;cols=96;z0=39.07;dz=(49.3-z0)/rows;da=2*pi/cols
for j in range(rows-1):
 for i in range(cols):
  if (i+j)%2:continue
  aa=i*da;zz=z0+(j+1)*dz
  coords=[(aa-da*.91,zz),(aa,zz+dz*.91),(aa+da*.91,zz),(aa,zz-dz*.91)]
  vs=[(cx+(radius_at(z)+.027)*cos(a),cy+(radius_at(z)+.027)*sin(a),z) for a,z in coords]
  add(vs,[(0,1,2,3)],'Painted roof %02d'%random.randrange(9),True)
lathe((cx,cy,49.3),[(.40,0),(.49,.16),(.29,.3),(.15,.9),(.08,1.25)],'Gold leaf',48)
cross(cx,cy,50.50,2.75)
# Four delicate stay wires under the cross.
for a in [0,pi/2,pi,3*pi/2]:beam((cx,cy,51.8),(cx+2.2*cos(a),cy+2.2*sin(a),48.6),.010,'Iron dark green',4)
# Drainpipes and thresholds reinforce pedestrian-scale detail.
GROUP='08_Drains_and_steps'
for x,y in [(-19.9,-7.4),(-19.9,7.4),(-4.7,-13.7),(-4.7,13.7),(8.5,-13.7),(8.5,13.7)]:
 path([(x,y,16),(x+.23,y,15.6),(x+.23,y,1.0),(x+.55,y,.6)],.088,'Iron dark green',10)
 for z in [2,5,8,11,14]:box('',(x+.22,y,z),(.30,.25,.05),'Iron black')
# V2.1 stairs are generated once in v21_west.py.
for sy in [-1,1]:
 for i in range(3):box('ear step',(-5.0-i*.32,sy*10,.12+(2-i)*.13),(.34,4,.22),'Granite foundation',collide=True)
print('CATHEDRAL geometry ready',flush=True)
# --- Walkable plaza / mapped roads ---
ACTIVE='02_SQUARE';GROUP='01_Granite_plaza'
box('square',(0,50,-.22),(178,170,.44),'Square granite slabs',collide=True)
# Paver bands are visible in the reference plaza and break the broad granite grid.
for x in range(-87,90,9):box('',(x,50,.008),(.39,170,.023),'Small granite setts • CC0 scan')
for y in range(-31,136,9):box('',(0,y,.011),(178,.38,.024),'Small granite setts • CC0 scan')
# Continuous peripheral curb, metre scale.
for x in [-89,89]:box('curb',(x,50,.04),(.45,170,.20),'Granite foundation',collide=True)
box('curb',(0,-35,.04),(178,.45,.20),'Granite foundation',collide=True)
# Drains, tactile route and sporadic maintenance covers.
GROUP='03_Drainage'
for x,y in [(-45,-32),(-80,45),(50,17),(40,-43),(-18,64)]:
 box('',(x,y,.02),(1.2,.6,.045),'Grate')
 for k in range(12):box('',(x-.53+k*.096,y,.05),(.035,.52,.02),'Iron black')
for y in range(-46,108,2):
 for j in range(4):box('',(-92+j*.085,y,.018),(.023,1.98,.016),'Granite foundation')
ACTIVE='06_ROADS';GROUP='Mapped_streets'
box('terrain',(0,0,-.72),(650,650,.5),'Asphalt',collide=True)
mapdata=json.load(open(ROOT/'references/map_aligned.json'))
for o in mapdata:
 if 'highway' not in o['tags']:continue
 pts=o['aligned_xy'];typ=o['tags']['highway'];width={'secondary':17,'tertiary':13,'service':5,'footway':3}.get(typ,6)
 for pa,pb in zip(pts,pts[1:]):
  a=Vector(pa);b=Vector(pb);d=b-a;length=d.length
  if length<.01:continue
  mid=(a+b)/2;angle=math.atan2(d.y,d.x)
  box('',(mid.x,mid.y,-.26),(length+.15,width,.25),'Asphalt',angle,collide=True)
  if typ in ['secondary','tertiary']:
   for t in range(int(length/7)):
    p0=a+d*((t+.4)*7/length);box('',(p0.x,p0.y,-.125),(3.0,.10,.015),'Road paint',angle)
exec(compile((ROOT/'scripts/v2_streets.py').read_text(),str(ROOT/'scripts/v2_streets.py'),'exec'))
# Mapped freestanding brick corridors, modeled as genuinely open passages.
ACTIVE='05_STREET_PROPS';GROUP='Mapped_brick_arcades'
for oid in ['338425685','338425686']:
 o=next(o for o in mapdata if o['id']==oid);pts=o['aligned_xy'];xs=[p[0] for p in pts];ys=[p[1] for p in pts];cx=(min(xs)+max(xs))/2;cy=(min(ys)+max(ys))/2
 # Map outline is bounding zone; the decorative arcade is made as a passable segment along Y.
 length=max(ys)-min(ys);count=max(3,int(length/4.6));gap=length/count
 for i in range(count+1):
  y=min(ys)+i*gap;box('arcade pier',(cx,y,2.8),(1.0,.75,5.6),brick,collide=True);box('',(cx,y,5.0),(1.25,1, .28),'Carved terracotta')
 for i in range(count):
  y=min(ys)+(i+.5)*gap;F=frame((cx-.52,y,0),(-1,0));arc(F,0,3.8,(gap-.72)/2,.28,.02,'Carved terracotta',24)
 box('',(cx,cy,6.12),(1.45,length+1,.35),'Carved terracotta');hiproof(cx,cy,1.6,length+1,6.3,.25)
# Benches and planted edges, arranged to retain wide circulation around the church.
def bench(x,y,angle=0):
 co=cos(angle);si=sin(angle)
 def P(u,v,z):return(x+co*u-si*v,y+si*u+co*v,z)
 for i in range(6):box('',P(0,-.26+i*.10,.5),(2.1,.078,.07),'Timber seat',angle)
 for z in [.78,.96,1.14]:box('',P(0,.24,z),(2.1,.075,.14),'Timber seat',angle)
 for u in [-.78,.78]:
  for v in [-.20,.20]:beam(P(u,v,.08),P(u,v,.53),.044,'Iron black',8)
  beam(P(u,.25,.08),P(u,.25,1.25),.04,'Iron black',8)
  path([P(u,-.3,.7),P(u,-.3,.82),P(u,.28,.82)],.036,'Iron black',8)
 collision.append({'name':'bench','type':'box','center':[x,y,.62],'size':[2.2,.8,1.25],'rotation_z':angle})
GROUP='Benches'
for x,y,a in [(-81,-28,0),(-81,36,0),(-80,68,0),(-45,-28,0),(-10,-29,0),(25,-29,0),(43,26,pi/2),(38,66,pi/2),(-9,57,0),(21,76,0)]:bench(x,y,a)
# Reference-like white globe lamps, decorative cast-iron bases.
GROUP='Ornamental_globe_lamps'
def lamp(x,y):
 lathe((x,y,0),[(.48,0),(.48,.16),(.32,.3),(.24,.58),(.17,1.3),(.115,3.8),(.20,3.95),(.10,4.25)],'Iron dark green',24)
 for a in [0,2*pi/3,4*pi/3]:
  xx=x+.72*cos(a);yy=y+.72*sin(a)
  path([(x,y,3.5),(xx,yy,3.8),(xx,yy,4.18)],.046,'Iron dark green',8)
  lathe((xx,yy,4.12),[(.14,0),(.25,.09),(.29,.14)],'Gold leaf',16)
  sphere((xx,yy,4.52),.29,'Cream lamp glass',scale=(1,1,1.22),N=16,rings=10)
 sphere((x,y,4.80),.34,'Cream lamp glass',scale=(1,1,1.2),N=16,rings=10)
 collision.append({'name':'lamp','type':'cylinder','center':[x,y,2.1],'radius':.33,'height':4.2})
for x,y in [(-73,-33),(-73,36),(-75,85),(-36,-32),(-34,35),(33,-31),(35,38),(32,84),(63,16),(-86,14),(-23,85)]:lamp(x,y)
# Tree planters, soil and vegetation. Crown geometry is individual leaves.
ACTIVE='04_VEGETATION';GROUP='Trees'
def leaf(center,s,angle,tilt,mat):
 cx,cy,cz=center;u=Vector((cos(angle),sin(angle),tilt)).normalized()*s;v=Vector((-sin(angle),cos(angle),.15))*s*.48;c=Vector(center)
 vs=[tuple(c-u),tuple(c+v),tuple(c+u),tuple(c-v),tuple(c+Vector((0,0,.025)))];add(vs,[(0,1,4),(1,2,4),(2,3,4),(3,0,4)],mat)
def tree(x,y,height=7,seed=1):
 rr=random.Random(seed);base=.38
 lathe((x,y,0),[(.55,0),(.36,.7),(.18,height*.60),(.06,height*.87)],'Bark',12,smooth=True)
 collision.append({'name':'tree','type':'cylinder','center':[x,y,height*.35],'radius':.42,'height':height*.7})
 for k in range(18):
  a=k*2.399+rr.uniform(-.25,.25);zz=height*(.40+k*.025);span=rr.uniform(1.4,2.8)*(1-k*.022)
  start=(x,y,zz);mid=(x+span*.5*cos(a),y+span*.5*sin(a),zz+.6);end=(x+span*cos(a),y+span*sin(a),zz+1.4)
  beam(start,mid,.08*(1-k*.025),'Bark',8,r2=.048);beam(mid,end,.048,'Bark',7,r2=.014)
  for m in range(3):
   aa=a+m*2.1;cc=(end[0]+.55*cos(aa),end[1]+.55*sin(aa),end[2]+rr.uniform(-.2,.7))
   beam(mid,cc,.020,'Bark',5,r2=.006)
   for j in range(110):
    u=rr.random()*2*pi;v=rr.uniform(-1,1);r=rr.random()**(1/3);sx=math.sqrt(1-v*v)
    p=(cc[0]+.88*r*sx*cos(u),cc[1]+.88*r*sx*sin(u),cc[2]+.70*r*v)
    leaf(p,rr.uniform(.095,.16),rr.random()*2*pi,rr.uniform(-.8,.8),'Leaves %02d'%rr.randrange(8))
 # Raised planter protects roots while leaving paths accessible.
 box('tree planter',(x,y,.20),(3.4,3.4,.4),'Granite foundation',collide=True);box('',(x,y,.42),(3.0,3.0,.025),'Soil')
for i,(x,y,h) in enumerate([(-82,-29,8),(-82,-9,8.6),(-84,53,8),(-81,78,7.5),(-45,-30,7),(-13,-30,7.5),(20,-30,7.9),(43,28,8),(40,56,8.5),(38,81,7.3),(-15,79,7),(1,80,7.5),(-88,98,8),(-84,120,8),(-50,112,7),(59,-34,7)]):
 GROUP='Tree_%02d'%i;tree(x,y,h,100+i)
# Potted conifers by the entries are visible in reference photos.
def conifer(x,y,h=3.4):
 cylinder((x,y,.1),.85,.80,'Timber seat',32)
 for z in [.20,.72]:lathe((x,y,z),[(.85,0),(.87,.07)],'Iron dark green',32)
 beam((x,y,.7),(x,y,h+.8),.075,'Bark',8)
 for j in range(13):
  z=.9+j*h/14;r=(h+.8-z)*.28
  for k in range(12):
   a=k*pi/6+j;end=(x+r*cos(a),y+r*sin(a),z-.20);beam((x,y,z+.2),end,.015,'Bark',5)
   for t in [.3,.6,1]:
    p=(x+r*t*cos(a),y+r*t*sin(a),z+.2-.4*t)
    for q in [-1,1]:leaf(p,.17,a+q*.7,.5,'Leaves %02d'%(j%5))
for i,(x,y) in enumerate([(-22,-6),(-22,6),(24,-5),(24,5),(-6,-17),(-6,17)]):GROUP='Potted_conifer_%d'%i;conifer(x,y)
# Street furniture: restrained informational signage, bollards, bins.
ACTIVE='05_STREET_PROPS';GROUP='Bollards_and_bins'
for x in range(-85,85,8):
 lathe((x,-50,0),[(.16,0),(.13,.1),(.12,.75),(.17,.84),(.1,.98),(0,1.02)],'Iron dark green',16)
for x,y in [(-77,-27),(-78,64),(41,44),(30,-35)]:
 box('bin',(x,y,.55),(.65,.55,1.1),'Iron dark green',collide=True);box('',(x,y-.286,.85),(.43,.025,.17),'Window shadow')
 for k in range(8):box('',(x-.29+k*.082,y-.29,.42),(.027,.025,.68),'Gold leaf')
# Cast plaques and bilingual text are separate editable Blender text objects.
def label(text,loc,size,normal=(0,-1),material_name='Ivory cornice',name='Sign'):
 cu=bpy.data.curves.new(name,'FONT');cu.body=text;cu.size=size;cu.align_x='CENTER';cu.extrude=.003
 ob=bpy.data.objects.new(name,cu);COLS['05_STREET_PROPS'].objects.link(ob);ob.location=loc
 # Text local +Z faces normal; local +Y remains up.
 n=Vector((normal[0],normal[1],0));ob.rotation_euler=n.to_track_quat('Z','Y').to_euler();ob.data.materials.append(M[material_name])
 return ob
GROUP='Wayfinding'
for x,y in [(-39,-22),(30,21)]:
 box('wayfinding',(x,y,1.18),(1.25,.14,2.35),'Sign enamel',collide=True)
 label('SOPHIA SQUARE',(x,y-.08,1.83),.105,name='Wayfinding title');label('ARCHITECTURE MUSEUM',(x,y-.081,1.60),.063,name='Wayfinding subtitle')
 label('1932',(x,y-.082,1.31),.15,material_name='Gold leaf',name='Heritage year')
 label('EXTERIOR WALK',(x,y-.081,.78),.077,name='Wayfinding direction')
# Coarse pigeon meshes removed in V2.1; no substitute animal placeholders.
print('Environment geometry ready',flush=True)

exec(compile((ROOT/'scripts/v2_details.py').read_text(),str(ROOT/'scripts/v2_details.py'),'exec'))

exec(compile((ROOT/'scripts/v22_street_refinements.py').read_text(),str(ROOT/'scripts/v22_street_refinements.py'),'exec'))
exec(compile((ROOT/'scripts/v221_targeted_repairs.py').read_text(),str(ROOT/'scripts/v221_targeted_repairs.py'),'exec'))

# --- Convert geometry buffers into editable native mesh datablocks. ---
for (collection,group,mat),(verts,faces,smooth,uvs) in B.items():
 me=bpy.data.meshes.new(group+' | '+mat);me.from_pydata(verts,[],faces);me.update()
 ob=bpy.data.objects.new(group+' | '+mat,me);COLS[collection].objects.link(ob);me.materials.append(M[mat]);uv=me.uv_layers.new(name='UVMap')
 for poly,sm,coords in zip(me.polygons,smooth,uvs):
  poly.use_smooth=sm
  for idx,co in zip(poly.loop_indices,coords):uv.data[idx].uv=co
 ob['role']='render_geometry';ob['source_confidence']='photo-informed approximate'
 if group.startswith('OSM_'):ob['osm_way_id']=group[4:];ob['source_confidence']='OSM footprint; estimated height and facade'
 # Submillimetre edges catch light without smoothing masonry into plastic.
 if collection=='01_CATHEDRAL' and mat in [brick,'Carved terracotta','Granite foundation']:
  be=ob.modifiers.new('Small masonry edge highlights','BEVEL');be.width=.0035 if mat.startswith('Arch fired brick') else .010;be.segments=2;be.limit_method='ANGLE'
print('Native meshes:',len(B),flush=True)
# Collision proxies are separate, hidden from render, and exported as a separate file.
for idx,c in enumerate(collision):
 if c['type']=='box':
  bpy.ops.mesh.primitive_cube_add(size=1,location=c['center']);ob=bpy.context.object;ob.scale=c['size'];ob.rotation_euler.z=c.get('rotation_z',0)
 elif c['type']=='cylinder':
  bpy.ops.mesh.primitive_cylinder_add(vertices=16,radius=c['radius'],depth=c['height'],location=c['center']);ob=bpy.context.object
 elif c['type']=='polygon':
  ps=c['points'];nn=len(ps);verts=[(x,y,z) for z in [0,c['height']] for x,y in ps];faces=[tuple(range(nn-1,-1,-1)),tuple(range(nn,2*nn))]+[(i,(i+1)%nn,(i+1)%nn+nn,i+nn) for i in range(nn)]
  me=bpy.data.meshes.new('collision');me.from_pydata(verts,[],faces);me.update();ob=bpy.data.objects.new('collision',me);COLS['07_COLLISION'].objects.link(ob)
 for cc in list(ob.users_collection):cc.objects.unlink(ob)
 COLS['07_COLLISION'].objects.link(ob);ob.name='COL_%03d_%s'%(idx,c['name']);ob.hide_render=True;ob.display_type='WIRE';ob['collision_only']=True;ob.hide_set(True)
COLS['07_COLLISION'].hide_render=True
json.dump({'units':'metres','axis':'Blender Z up; local X points 17.3 degrees north of east','colliders':collision},open(ROOT/'game/colliders.json','w'),indent=2)
# Game markers, start outside cathedral, loop to all facades.
route=[[-55,-21,1.7],[-29,-18,1.7],[-15,-18,1.7],[-7,-24,1.7],[27,-20,1.7],[33,0,1.7],[24,22,1.7],[-9,24,1.7],[-35,18,1.7],[-55,-21,1.7]]
for i,p in enumerate(route[:-1]):
 ob=bpy.data.objects.new('SPAWN_Main' if i==0 else 'ROUTE_%02d'%i,None);COLS['09_GAME_MARKERS'].objects.link(ob);ob.location=p;ob.empty_display_type='ARROWS';ob.empty_display_size=1.0
json.dump({'player_eye_height':1.70,'player_capsule_radius':.30,'spawn_blender':route[0],'walking_loop_blender':route,'origin_wgs84':{'latitude':45.76819,'longitude':126.62129},'local_rotation_degrees':17.3,'playable_scope':'exterior square and surrounding street surfaces; closed cathedral interior'},open(ROOT/'game/map_metadata.json','w'),indent=2)
# --- Lighting and cameras ---
world=bpy.data.worlds.new('Harbin daylight • CC0 HDRI');scene.world=world;world.use_nodes=True
n=world.node_tree.nodes;l=world.node_tree.links;n.clear();out=n.new('ShaderNodeOutputWorld');bg=n.new('ShaderNodeBackground');bg.inputs[1].default_value=.9;env=n.new('ShaderNodeTexEnvironment');env.image=bpy.data.images.load(str(TEX/'sky.hdr'));tc=n.new('ShaderNodeTexCoord');mp=n.new('ShaderNodeMapping');mp.inputs['Rotation'].default_value[2]=math.radians(112);l.new(tc.outputs['Generated'],mp.inputs[0]);l.new(mp.outputs[0],env.inputs[0]);l.new(env.outputs[0],bg.inputs[0]);l.new(bg.outputs[0],out.inputs[0])
ld=bpy.data.lights.new('Late afternoon sun','SUN');ld.energy=2.1;ld.angle=math.radians(2.3);ld.color=(1.0,.95,.86);sun=bpy.data.objects.new('Late afternoon sun',ld);COLS['08_CAMERAS_LIGHTS'].objects.link(sun);sun.rotation_euler=(math.radians(33),math.radians(-32),math.radians(-58))
def camera(name,loc,target,lens):
 data=bpy.data.cameras.new(name);ob=bpy.data.objects.new(name,data);COLS['08_CAMERAS_LIGHTS'].objects.link(ob);ob.location=loc;ob.rotation_euler=(Vector(target)-ob.location).to_track_quat('-Z','Y').to_euler();data.lens=lens;data.clip_end=1800;return ob
cam=camera('01_HERO_West_square',(-63,24,1.7),(0,0,22.3),29)
camera('02_EYE_LEVEL_170cm',(-54,-32,1.70),(0,0,22),25)
camera('03_EAST_Facade',(58,-6,1.7),(2,0,23),25)
camera('04_MAP_Overview',(-149,-163,142),(0,26,6),39)
camera('05_Brick_detail',(-34,-6.8,1.7),(-20.4,0,4.9),40)
scene.camera=cam
scene.render.engine='CYCLES';scene.cycles.samples=96;scene.cycles.use_denoising=True;scene.cycles.adaptive_threshold=.035;scene.cycles.max_bounces=7;scene.cycles.diffuse_bounces=3;scene.cycles.glossy_bounces=4;scene.cycles.transmission_bounces=4
try:
 pref=bpy.context.preferences.addons['cycles'].preferences;pref.compute_device_type='METAL';pref.get_devices()
 for d in pref.devices:d.use=d.type=='METAL'
 scene.cycles.device='GPU';print('Cycles devices:',[(d.name,d.type,d.use) for d in pref.devices],flush=True)
except Exception as e:print('CPU fallback',str(e),flush=True);scene.cycles.device='CPU'
scene.render.resolution_x=1920;scene.render.resolution_y=1280;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG';scene.render.film_transparent=False
scene.view_settings.view_transform='AgX';scene.view_settings.look='AgX - Medium High Contrast';scene.view_settings.exposure=.15
scene.render.filepath=str(ROOT/'renders/01_Hero.png')
scene['project']='Harbin Saint Sophia Square | Photo-informed exterior reconstruction'
scene['accuracy_note']='NOT survey/photogrammetry. 2023 photo details + OSM snapshot. Read REFERENCES.md.'
scene['height_anchor_m']=53.35;scene['real_world_origin']='45.76819N,126.62129E';scene['real_north_local_rotation_deg']=17.3
# Readme visible in Blender's text editor, with offline portable assets packed.
readme=bpy.data.texts.new('START_HERE.txt');readme.write('HARBin — SAINT SOPHIA SQUARE\n\nF12: render the selected camera. Cameras in collection 08.\nFor exterior walk: select camera 02, Numpad 0, Shift+grave; WASD + mouse.\nSet Walk Navigation Gravity in Blender preferences if desired.\nAll textures are packed. Geometry is native and editable.\n07_COLLISION contains hidden, separately supplied gameplay proxies.\n\nPhoto-informed reconstruction, not a surveyed digital twin.\nReal height anchor: 53.35 m. Surrounding buildings use OSM outlines,\nbut facade details and heights are estimated. See REFERENCES.md.\n')
for area in bpy.context.screen.areas:
 if area.type=='VIEW_3D':area.spaces.active.region_3d.view_perspective='CAMERA';area.spaces.active.clip_end=1800
exec(compile((ROOT/'scripts/v2_lighting.py').read_text(),str(ROOT/'scripts/v2_lighting.py'),'exec'))
bpy.context.preferences.filepaths.save_version=0
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'Harbin_Sophia_Square.blend'))
# Mesh statistics for delivery and validation.
stats={'revision':'v2.2.1-demo','night_objects':len(night.objects),'night_lights':len(lighting_record),'packed_image_count':sum(bool(im.packed_file) for im in bpy.data.images),'packed_font_count':sum(bool(f.packed_file) for f in bpy.data.fonts),'objects':len(scene.objects),'render_meshes':len(B),'vertices':sum(len(ob.data.vertices) for ob in scene.objects if ob.type=='MESH' and not ob.hide_render),'polygons':sum(len(ob.data.polygons) for ob in scene.objects if ob.type=='MESH' and not ob.hide_render),'collision_proxies':len(collision),'cameras':[o.name for o in scene.objects if o.type=='CAMERA'],'blender_version':bpy.app.version_string}
json.dump(stats,open(ROOT/'scene_stats.json','w'),indent=2);print('SCENE_SAVED',stats,flush=True)
if '--render-preview' in sys.argv:
 scene.render.resolution_percentage=55;scene.cycles.samples=24;scene.render.filepath=str(ROOT/'renders/preview.png');bpy.ops.render.render(write_still=True)
