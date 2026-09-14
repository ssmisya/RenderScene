"""Repair user-reported gallery construction defects and Daoli/New 100 frontage.
Source coverage and dimensional uncertainties stay explicit in references/v2_2_1.
Executed before mesh buffers are committed; native source and game share geometry.
"""
ACTIVE='05_STREET_PROPS'
# Replace the untextured pink pier material with metric CC0 brick PBR.
old=M['Gallery red sandstone'];old.name='Gallery flat pink superseded'
pbr('Gallery red sandstone','v2/brick',.88)
M['Gallery red sandstone'].diffuse_color=(.28,.14,.10,1)
# Keep geometry/texture scale consistent in both Cycles and exported glTF.
for key,buffer in B.items():
 if key[2]=='Gallery red sandstone':
  buffer[3][:]=[[(u*.88,v*.88) for u,v in face] for face in buffer[3]]
for node in M['Gallery red sandstone'].node_tree.nodes:
 if node.type=='VECT_MATH' and node.operation=='SCALE':node.inputs[3].default_value=1
# Remove the defective terminal stairs, unsupported rails and single-sheet pediments.
for key in list(B):
 if key[1]=='V22_Gallery_terminal_pediments':del B[key]
collision[:]=[c for c in collision if c['name']!='gallery stair']
GROUP='V221_Gallery_landings_and_rails'
def local_solid(F,u,z,d,w,h,depth,mat,name=None):
 fbox(F,u,z,d,w,h,depth,mat)
 if name:
  origin=F(0,0);along=Vector(F(1,0))-Vector(origin)
  collision.append({'name':name,'type':'box','center':F(u,z,d),'size':[w,depth,h],'rotation_z':math.atan2(along.y,along.x)})
# The landing is continuous behind the top riser, so stairs no longer finish in empty space.
for x,y,normal in [(-64,37.5,(-1,0)),(-64.8,72,(0,-1))]:
 F=frame((x,y,0),normal)
 # June/September 2025 street-side photo: steps align with the right arch.
 # The second pavilion has no equivalent recent view, so retain its estimate.
 offset_entry=(normal==(-1,0))
 stair_u=-1.9 if offset_entry else 0
 stair_w=3.15 if offset_entry else 6.4
 for k in range(7):
  d=5.20-k*.34;top=.15*(k+1)
  local_solid(F,stair_u,top/2,d,stair_w,top,.34,'Granite foundation','gallery repaired tread')
  fbox(F,stair_u,top-.013,d+.151,stair_w,.026,.038,'Painted plaster')
  for u in [stair_u+j for j in ([-.8,.8] if offset_entry else [-2.4,-1.2,0,1.2,2.4])]:fbox(F,u,top+.001,d,.007,.002,.30,'Grate')
 local_solid(F,stair_u,.525,1.495,stair_w,1.05,2.99,'Granite foundation','gallery connected landing')
 local_solid(F,0,.525,-1.6,6.4,1.05,3.2,'Granite foundation','gallery inner landing')
 for side in [-1,1]:
  u=stair_u+side*(stair_w/2-.17)
  def rail_z(d):return 1.12+(5.2-d)*(.9/2.04)
  ramp_side=offset_entry and side==1
  rail_pts=[F(u,1.12,5.5),F(u,1.12,5.2),F(u,2.02,3.16)]
  if not ramp_side:rail_pts.extend([F(u,2.02,2.6),F(u,2.02,.3)])
  path(rail_pts,.036,'Iron dark green',10)
  for d in ([5.18,4.68,4.18,3.68,3.18] if ramp_side else [5.18,4.68,4.18,3.68,3.18,2.60,1.45,.35]):
   k=max(0,min(6,int((5.37-d)/.34)));floor=.15*(k+1) if d>2.99 else 1.05
   top=rail_z(d) if d>=3.16 else 2.02
   beam(F(u,floor+.03,d),F(u,top,d),.028,'Iron dark green',10)
   fbox(F,u,floor+.027,d,.15,.054,.15,'Iron dark green')
  path([F(u,.38,5.18),F(u,1.28,3.16)]+([] if ramp_side else [F(u,1.28,.3)]),.018,'Iron dark green',8)
  # Guard infill follows the slope; every vertical reaches the lower and upper rails.
  for k in range(9 if ramp_side else 20):
   d=5.16-k*.245;top=rail_z(d) if d>=3.16 else 2.02
   beam(F(u,top-.73,d),F(u,top-.025,d),.012,'Iron dark green',6)
 # Three-dimensional, layered pediment, integrated with the cornice rather than floating.
 GROUP='V221_Gallery_roof_joinery'
 verts=[F(u,z,d) for d in [-.24,.24] for u,z in [(-3.8,6.62),(3.8,6.62),(0,7.78)]]
 add(verts,[(0,2,1),(3,4,5),(0,1,4,3),(1,2,5,4),(2,0,3,5)],'Gallery aged coping')
 path([F(-3.94,6.68,.32),F(0,7.96,.32),F(3.94,6.68,.32)],.105,'Gallery aged coping',10)
 for z,w in [(6.63,8.15),(6.78,8.5)]:fbox(F,0,z,.10,w,.15,.88,'Gallery aged coping')
 for i in range(25):fbox(F,-3.75+i*.3125,6.24,.30,.12,.18,.40,'Gallery aged coping')
 # Roof top is closed and slopes towards its eaves; fascia and soffit meet.
 add([F(-4.05,6.73,-.20),F(4.05,6.73,-.20),F(4.05,6.73,-3.5),F(-4.05,6.73,-3.5),F(0,7.86,-.20),F(0,7.86,-3.5)],[(0,4,5,3),(4,1,2,5),(3,5,2),(0,1,4)],'Gallery aged coping')
 GROUP='V221_Gallery_landings_and_rails'
# Masonry course joints and discrete pier caps remain readable at eye level.
GROUP='V221_Gallery_course_details'
for a,b,width,bays in [((-64,37.5),(-50.5,37.5),7.6,3),((-50.5,37.5),(-50.5,54.5),7.6,4),((-64.8,72),(-64.8,104.1),7.8,7),((-64.8,104.1),(-50,104.1),7.8,3)]:
 dx=b[0]-a[0];dy=b[1]-a[1];L=math.hypot(dx,dy);nx=-dy/L;ny=dx/L
 PF=frame(((a[0]+b[0])/2,(a[1]+b[1])/2,0),(nx,ny))
 local_solid(PF,0,.525,0,L+.5,1.05,width-1.2,'Granite foundation','gallery continuous floor')
 for side in [-1,1]:
  F=frame(((a[0]+b[0])/2+side*nx*width/2,(a[1]+b[1])/2+side*ny*width/2,0),(side*nx,side*ny))
  for i in range(bays+1):
   u=-L/2+i*L/bays
   for z in [1.45,2.05,2.65,3.25,3.85,4.45]:fbox(F,u,z,.51,1.01,.018,.025,'Old lime mortar')
   for z in [.44,4.92,5.66]:fbox(F,u,z,.08,1.30,.08,1.31,'Carved terracotta')
print('V221 gallery stairs, landing, supported rails, masonry and closed pediments repaired',flush=True)
# Remove all duplicated market strips and labels, then build each mapped facade once.
for key in list(B):
 if key[1]=='OSM_338426095':del B[key]
for ob in list(sign_objects):
 if ob.name.startswith(('Daoli_market_photo_reference','Dashang_group_photo_reference')):
  sign_objects.remove(ob);bpy.data.objects.remove(ob,do_unlink=True)
material('Market panel joint',(.17,.19,.19),.8,noise=False)
for i in range(5):material('Market enamel panel %d'%i,(.51+i*.003,.51+i*.003,.48+i*.0028),.48,.08,False)
material('Market blue curtain glass',(.06,.16,.22),.24,.48,False)
material('Market sign green',(.025,.235,.075),.44,.1,False)
material('Market canopy metal',(.46,.48,.44),.4,.35)
material('Market LED red',(.43,.025,.008),.65,0,False)
ACTIVE='03_OSM_BUILDINGS';GROUP='V221_Daoli_cladding'
outline=next(o['aligned_xy'] for o in mapdata if o['id']=='338426095')
# OSM has the closing point twice; omit it to avoid zero length roof / facade edges.
outline=outline[:-1] if outline[0]==outline[-1] else outline
poly=list(outline)
if sum(poly[i][0]*poly[(i+1)%len(poly)][1]-poly[(i+1)%len(poly)][0]*poly[i][1] for i in range(len(poly)))<0:poly.reverse()
# The source shows recessed/open doorways. A solid extrusion behind them would
# occlude every modeled return, so split the actual exterior wall at the portal.
for a,b in zip(poly,poly[1:]+poly[:1]):
 dx=b[0]-a[0];dy=b[1]-a[1];length=math.hypot(dx,dy)
 if length<.05:continue
 n=(dy/length,-dx/length);mid=((a[0]+b[0])/2,(a[1]+b[1])/2)
 FF=frame((*mid,0),n)
 spans=[(-length/2,length/2,0,27)]
 if length>25 and n[0]>.8 and mid[1]<40:
  spans=[(-length/2,-9.1,0,27),(9.1,length/2,0,27),(-9.1,9.1,4.65,27),(-9.1,9.1,0,.55)]
 for left,right,bottom,top in spans:
  add([FF(left,bottom),FF(right,bottom),FF(right,top),FF(left,top)],[(0,3,2,1)],'Market panel joint')
add([(x,y,27) for x,y in poly],[tuple(range(len(poly)))],'Market panel joint')
market_frames=[]
for pa,pb in zip(poly,poly[1:]+poly[:1]):
 dx=pb[0]-pa[0];dy=pb[1]-pa[1];L=math.hypot(dx,dy)
 if L<.05:continue
 normal=(dy/L,-dx/L);F=frame(((pa[0]+pb[0])/2,(pa[1]+pb[1])/2,0),normal)
 count=max(1,round(L/1.45));step=L/count
 # Closed rounded corner segments retain blank sheet metal, not repeated slit windows.
 long=L>25
 for col in range(count):
  u=-L/2+(col+.5)*step
  for row in range(12):
   z=5.03+(row+.5)*1.82
   if long and 5.5<z<17.9 and col%4==1:
    mat='Market blue curtain glass'
   else:mat='Market enamel panel %d'%((col*7+row*3)%5)
   fbox(F,u,z,.055,step-.023,1.797,.16,mat)
   if mat=='Market blue curtain glass':
    for du in [-step/2+.035,step/2-.035]:fbox(F,u+du,z,.15,.055,1.82,.09,'Window lead')
  # Leave the reworked 18.2 m portal genuinely open, including its shop returns.
  if not (long and normal[0]>.8 and (pa[1]+pb[1])/2<40 and abs(u)<9.1+step/2):
   fbox(F,u,2.55,.085,step-.11,4.68,.08,'Cool shop glazing')
   fbox(F,u-step/2+.04,2.55,.18,.08,4.83,.16,'Market canopy metal')
   fbox(F,u,1.25,.16,step,.065,.10,'Market canopy metal')
 for z,h,d in [(5.06,.11,.22),(18.35,.17,.17),(24.0,.18,.15),(26.90,.17,.28)]:
  fbox(F,0,z,.10,L,h,d,'Market canopy metal')
 if long and normal[0]>.8:market_frames.append((F,normal,L))
# Two existing east-facing wings are separated by the mapped return. Each receives its
# own attached entrance; a label is never positioned by an unrelated world X coordinate.
GROUP='V221_Daoli_entries'
for idx,(F,normal,L) in enumerate(market_frames[:1]):
 width=min(18.0,L-.8)
 # Recessed black vestibule and physical glazed double door frame.
 fbox(F,0,2.15,.24,width-.8,3.7,.12,'Window shadow')
 for u in [-4.7,-2.35,0,2.35,4.7]:
  fbox(F,u,1.98,.35,2.19,3.12,.10,'Cool shop glazing')
  for du in [-1.11,1.11]:fbox(F,u+du,1.98,.44,.075,3.26,.11,'Market canopy metal')
  fbox(F,u,3.59,.44,2.30,.09,.13,'Market canopy metal')
  fbox(F,u,1.9,.44,2.30,.055,.12,'Market canopy metal')
  for du in [-.16,.16]:beam(F(u+du,1.25,.54),F(u+du,1.83,.54),.018,'Market canopy metal',8)
 # Segmented shallow bowed canopy, opaque soffit and supported underside ribs.
 for i in range(24):
  a=-width/2+i*width/24;b=-width/2+(i+1)*width/24
  da=1.45+1.15*math.sqrt(max(0,1-(a/(width/2))**2));db=1.45+1.15*math.sqrt(max(0,1-(b/(width/2))**2))
  va=[F(a,4.68,.08),F(b,4.68,.08),F(b,4.5,db),F(a,4.5,da),F(a,4.57,.08),F(b,4.57,.08),F(b,4.39,db),F(a,4.39,da)]
  add(va,[(0,1,2,3),(4,7,6,5),(2,6,7,3),(0,4,5,1)],'Market canopy metal')
  beam(F(a,4.46,da),F(b,4.46,db),.062,'Market canopy metal',10)
  if i%3==0:
   beam(F(a,4.6,.08),F(a,4.39,da),.032,'Window lead',8)
   beam(F(a,4.52,da-.15),F(a,6.1,.1),.015,'Window lead',6)
 fbox(F,0,3.94,.50,12.8,.59,.21,'Iron black')
 street_text('欢 迎 光 临 道 里 菜 市 场',F(0,3.74,.64),.43,normal,'Market LED red','V221_Market_LED_'+str(idx))
 # Photo's five large green characters; each has real brackets to the canopy.
 for k,t in enumerate('道里菜市场'):
  u=4.9-k*2.45
  street_text(t,F(u,4.95,.90),1.65,normal,'Market sign green',f'V221_Daoli_letter_{idx}_{k}')
  beam(F(u,4.65,.84),F(u,5.22,.84),.023,'Window lead',8)
 # The older name is a separate small sign at the left, never prefixed as “商业”.
 # Gold three-arch emblem and shallow traditional roof silhouette, as in the entrance photo.
 for u in [7.13,7.70,8.27]:
  arc(F,u,5.65,.23,.075,.85,'Gold leaf',20)
  for du in [-.27,.27]:fbox(F,u+du,5.48,.91,.07,.38,.14,'Gold leaf')
 fbox(F,7.7,5.18,.88,1.77,.41,.17,'Gold leaf')
 add([F(u,z,.98) for u,z in [(6.64,6.01),(7.2,6.22),(7.7,6.52),(8.2,6.22),(8.76,6.01),(8.17,6.13),(7.23,6.13)]],[(0,1,2,3,4,5,6)],'Gold leaf')
 for u in [7.14,8.26]:fbox(F,u,5.95,.91,.065,.40,.14,'Gold leaf')
 street_text('八杂市',F(7.7,5.07,.94),.44,normal,'Iron black','V221_Bazashi_'+str(idx))
 for k in range(3):
  local_solid(F,0,.10*(k+1),3.4-k*.36,12.8,.20*(k+1),.36,'Granite foundation','market entry step')
 local_solid(F,0,.30,1.39,12.8,.60,2.42,'Granite foundation','market connected landing')
 # Corner/entrance lights are fixtures, day-off and night-on in the shared lighting manifest.
 night_targets.append((F(0,4.30,2.0),F(0,1.3,1.1),'commercial',140))
# Department-store roof letters on a mounted frame, above the setback facade.
GROUP='V221_New100_roof_support'
F=frame((-126.5,45,0),(1,0))
for u in [-19,-12,-5,2,9,16,22]:
 beam(F(u,38.8,-.2),F(u,41.9,-.2),.045,'Window lead',8)
 beam(F(u,39,-2.2),F(u,41.8,-.2),.045,'Window lead',8)
for z in [39.7,41.5]:beam(F(-22,z,-.2),F(23,z,-.2),.04,'Window lead',8)
street_text('大商集团 DASHANG GROUP',F(0,39.7,.03),2.0,(1,0),'Dark blue enamel','V221_Dashang_mounted')
print('V221 Daoli panel joints, glazing, attached green signage and entrance canopies rebuilt',flush=True)
