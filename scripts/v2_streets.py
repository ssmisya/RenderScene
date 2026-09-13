"""OSM footprints + individually differentiated photo-referenced city facades.
Facade heights / shop placement are photointerpretation, not surveyed measurements.
"""
ACTIVE='03_OSM_BUILDINGS'
night_targets=[];sign_objects=[]
font_candidates=['/System/Library/Fonts/STHeiti Medium.ttc','/System/Library/Fonts/Hiragino Sans GB.ttc','/System/Library/Fonts/Supplemental/Songti.ttc']
chinese_font=None
for p in font_candidates:
 if Path(p).exists():
  try:chinese_font=bpy.data.fonts.load(p);break
  except:pass
def street_text(text,loc,size,normal=(0,-1),mat='Ivory cornice',name='Photo_sign'):
 cu=bpy.data.curves.new(name,'FONT');cu.body=text;cu.size=size;cu.align_x='CENTER';cu.extrude=.009;cu.bevel_depth=.004
 if chinese_font:cu.font=chinese_font
 ob=bpy.data.objects.new(name,cu);COLS['03_OSM_BUILDINGS'].objects.link(ob);ob.location=loc;ob.rotation_euler=Vector((*normal,0)).to_track_quat('Z','Y').to_euler();cu.materials.append(M[mat]);sign_objects.append(ob);return ob
material('North arcade sage plaster',(.31,.36,.16),.82)
# A small palette of glass avoids a single repeated blue window on every storey.
for i in range(7):material('City glazing %d'%i,(.025+i*.013,.042+i*.016,.048+i*.017),.17+i*.025,.38,False)
def city_window(F,u,z,w,h,ornate=False):
 fbox(F,u,z,.13,w+.24,h+.26,.22,'Painted plaster');fbox(F,u,z,.263,w,h,.05,'City glazing %d'%random.randrange(7))
 fbox(F,u,z,.302,.055,h,.06,'Ivory cornice');fbox(F,u,z-h*.14,.302,w,.05,.06,'Ivory cornice')
 fbox(F,u,z-h/2-.10,.35,w+.38,.14,.40,'Painted plaster')
 if ornate:
  for side in [-1,1]:fbox(F,u+side*(w/2+.24),z,.25,.17,h+.65,.25,'Painted plaster')
  fbox(F,u,z+h/2+.21,.37,w+.62,.17,.51,'Painted plaster')
  for side in [-1,1]:fbox(F,u+side*(w/2+.12),z+h/2+.37,.29,.19,.28,.27,'Painted plaster')
 # Some dark interior depth and half drawn blinds, visible through varied glass.
 if random.random()<.22:fbox(F,u,z+h*.28,.31,w-.10,h*.29,.012,'Canvas cream')
def arch_shop(F,u,z,w,h):
 arch_panel(F,u,z,w+.35,h+.16,.12,'Painted plaster');arch_panel(F,u,z+.08,w,h-.04,.25,'Cool shop glazing')
 arc(F,u,z+h-w/2,w/2,.13,.28,'Ivory cornice',28)
 for du in [-w*.28,0,w*.28]:fbox(F,u+du,z+(h-w/2)/2,.30,.055,h-w/2,.07,'Window lead')
 for zz in [z+1.1,z+2.5]:fbox(F,u,zz,.30,w,.055,.07,'Window lead')
 fbox(F,u,z+1.05,.32,.045,1.6,.08,'Old brass hardware')
def band(F,length,z,mat='Painted plaster'):
 for zz,ww,dd in [(z,.22,.25),(z+.22,.13,.36),(z+.37,.19,.49)]:fbox(F,0,zz,dd,length,ww,dd+.10,mat)
def roof_front(F,L,z):
 add([F(-L/2,z,-.10),F(L/2,z,-.10),F(L/2,z+3.0,-3.6),F(-L/2,z+3.0,-3.6)],[(0,1,2,3)],'Roof burgundy')
 for i in range(max(1,int(L/8))):
  u=-L/2+(i+.5)*L/max(1,int(L/8));arch_panel(F,u,z+.08,1.32,1.65,-.55,'Window shadow');arc(F,u,z+1.07,.68,.25,-.45,'Painted plaster',24)
  fbox(F,u,z+.08,-.31,2.0,.18,.65,'Painted plaster')
 for u in [(-L/2+i*.45) for i in range(int(L/.45))]:path([F(u,z+.05,.02),F(u,z+3,-3.52)],.012,'Iron black',4)
small_ids={'338425685','338425686','338425687','338425941','1294641280','1294641332'}
heights={'338425684':6.9,'1294641996':21.6,'338426095':27,'1294641989':17,'1294641998':15,'338426656':36,'338427461':48}
for o in mapdata:
 if 'building' not in o['tags'] or o['id']=='338425563' or o['id'] in small_ids:continue
 poly=o['aligned_xy'];cx=sum(p[0] for p in poly)/len(poly);cy=sum(p[1] for p in poly)/len(poly)
 if abs(cx)>290 or abs(cy)>295:continue
 ident=o['id'];h=heights.get(ident,random.choice([17,21,25,30]));GROUP='OSM_'+ident
 mat='North arcade sage plaster' if ident=='338425684' else ('Warm ochre stone' if ident=='1294641989' else 'Painted plaster')
 poly=extrude_poly(poly,0,h,mat);collision.append({'name':'OSM_'+ident,'type':'polygon','points':poly,'height':h})
 for pa,pb in zip(poly,poly[1:]+poly[:1]):
  dx=pb[0]-pa[0];dy=pb[1]-pa[1];L=math.hypot(dx,dy)
  if L<2.4:continue
  norm=(dy/L,-dx/L);F=frame(((pa[0]+pb[0])/2,(pa[1]+pb[1])/2,0),norm)
  ncol=max(1,int(L/(4.8 if ident=='338425684' else 3.8)));spacing=L/ncol
  if ident=='338426095':
   # Daoli market / New 100 is a broad contemporary shopping volume, not a neo-classical arch wall.
   for zz in [.9,5.3,13.0,22.5,26.7]:band(F,L,zz)
   for i in range(ncol):
    u=-L/2+(i+.5)*spacing
    fbox(F,u,3.0,.11,spacing-.30,4.2,.06,'Cool shop glazing')
    fbox(F,u,16.5,.12,1.0,5.0,.06,'Cool shop glazing')
    fbox(F,u,10.0,.10,spacing-.12,.015,.05,'Ivory cornice')
   continue
  if ident=='338425684':
   band(F,L,.45);band(F,L,6.65)
   for i in range(ncol):
    u=-L/2+(i+.5)*spacing;arch_shop(F,u,.30,min(3.35,spacing-.7),5.2)
    sphere(F(u-spacing*.48,5.6,.20),.16,'Painted plaster',N=10,rings=6)
    night_targets.append((F(u,5.7,1.0),F(u,6.7,.1),'commercial',75))
   # Balustrade atop the low green shopping arcade.
   for i in range(int(L/.5)):
    u=-L/2+i*.5;fbox(F,u,7.23,.15,.12,.65,.15,'Painted plaster')
   fbox(F,0,7.65,.17,L,.17,.40,'Painted plaster')
   continue
  if ident=='1294641996':
   for zz in [.8,12.0,14.1,21.1]:band(F,L,zz)
   for i in range(ncol):
    u=-L/2+(i+.5)*spacing
    arch_shop(F,u,.35,min(2.8,spacing-.65),10.8)
    city_window(F,u,17.1,1.30,3.0)
    fbox(F,u-spacing/2,6.2,.28,.34,11.8,.50,'Painted plaster')
    night_targets.append((F(u,13.8,.85),F(u,20.8,.3),'commercial',170))
   roof_front(F,L,h)
   if L>60:
    street_text('埃 曼 影 城',F(0,13.0,.63),1.3,norm,'Red enamel letters','Cinema_photo_reference')
   continue
  # Two recognisable southern skyline buildings: ochre vertical slab and rounded hotel.
  floorh=3.30 if ident in ['1294641989','1294641998'] else 3.65
  for fl in range(1,int(h/floorh)):
   zz=fl*floorh
   if ident=='1294641998':fbox(F,0,zz-.47,.24,L,.15,.42,'Painted plaster')
   for i in range(ncol):
    u=-L/2+(i+.5)*spacing;city_window(F,u,zz+1.0,1.55,1.88)
  if ident=='1294641989':
   for i in range(ncol+1):fbox(F,-L/2+i*spacing,h/2,.25,.28,h,.48,'Ivory cornice')
  band(F,L,h-.55)
  # Air conditioners, exposed conduit and roof equipment break the perfect repeated grid.
  for i in range(ncol):
   if random.random()<.5:
    u=-L/2+(i+.75)*spacing;z=random.choice([7.1,10.6,14.2]);fbox(F,u,z,.53,.65,.40,.38,'Air conditioner casing')
    for q in range(5):fbox(F,u,z-.13+q*.066,.75,.5,.025,.018,'Window lead')
# Commercial upper floors set back behind the footprint's low arcade.
def heritage_wing(cx,cy,sx,sy,h,base=7.0,central=False):
 global GROUP
 GROUP='North_shopping_upper_'+str(cx)+'_'+str(cy)
 box('',(cx,cy,(base+h)/2),(sx,sy,h-base),'Painted plaster',collide=True)
 for normal,center,L in [((0,-1),(cx,cy-sy/2,0),sx),((0,1),(cx,cy+sy/2,0),sx),((-1,0),(cx-sx/2,cy,0),sy),((1,0),(cx+sx/2,cy,0),sy)]:
  F=frame(center,normal);band(F,L,base+.15);band(F,L,h-.8)
  count=max(1,int(L/3.7));step=L/count
  for i in range(count):
   u=-L/2+(i+.5)*step
   for z in [base+3.2,base+7.0,base+10.8,base+14.6,base+18.4]:
    if z+1.8<h:city_window(F,u,z,1.65,2.60,True)
   for side in [-1,1]:
    fbox(F,u+side*step*.44,(base+h)/2,.16,.16,h-base,.31,'Ivory cornice')
   night_targets.append((F(u,base+.6,.75),F(u,h-1,.15),'commercial',130))
  roof_front(F,L,h)
heritage_wing(-12,131.5,121,21,22.0)
heritage_wing(75,80,23,100,23.0)
heritage_wing(7,129.0,40,23,30.0,central=True)
# Monumental centre bay with paired giant columns and arched centre opening, per plaza tourist views.
F=frame((7,117.35,0),(0,-1));GROUP='North_central_portico'
fbox(F,0,20,.40,9.5,19,1.2,'Painted plaster');arch_shop(frame((7,116.12,0),(0,-1)),0,12.7,3.0,13.7)
for u in [-4.3,4.3]:
 fbox(F,u,20.5,.98,.85,16,1.15,'Ivory cornice')
 for z in [12.5,27.8]:fbox(F,u,z,1.11,1.7,.42,1.37,'Painted plaster')
band(F,11,28.0)
for u in [-18,-12,-6,0,6,12,18]:
 fbox(F,u,31.2,.08,.30,1.75,.30,'Ivory cornice');sphere(F(u,32.1,.08),.20,'Ivory cornice',N=10,rings=6)
# Eastern anchor tower / vertical sign in photographs.
heritage_wing(72.5,36.0,25,21,30.5)
F=frame((59.9,36,0),(-1,0));GROUP='Golden_sun_corner'
for u in [-7.4,7.4]:
 fbox(F,u,18.5,.55,.90,22,1.1,'Ivory cornice');fbox(F,u,29.2,.70,1.6,.5,1.4,'Painted plaster')
for j,t in enumerate('金太阳'):street_text(t,F(0,23-j*4,.75),2.5,(-1,0),'Red enamel letters','Golden_sun_photo_reference')
# High-rise shafts occupy only part of their mapped podiums, as seen behind the church.
# Chamfered corners on the hotel prevent the former oversize rectangular tower silhouette.
def skyline_tower(cx,cy,sx,sy,h,style):
 global GROUP
 GROUP='V2_Skyline_'+style
 chamfer=2.3
 poly=[(cx-sx/2+chamfer,cy-sy/2),(cx+sx/2-chamfer,cy-sy/2),(cx+sx/2,cy-sy/2+chamfer),(cx+sx/2,cy+sy/2-chamfer),(cx+sx/2-chamfer,cy+sy/2),(cx-sx/2+chamfer,cy+sy/2),(cx-sx/2,cy+sy/2-chamfer),(cx-sx/2,cy-sy/2+chamfer)]
 extrude_poly(poly,0,h,'Warm ochre stone' if style=='Wantai' else 'Painted plaster')
 collision.append({'name':style+'_shaft','type':'polygon','points':poly,'height':h})
 for pa,pb in zip(poly,poly[1:]+poly[:1]):
  dx=pb[0]-pa[0];dy=pb[1]-pa[1];L=math.hypot(dx,dy);F=frame(((pa[0]+pb[0])/2,(pa[1]+pb[1])/2,0),(dy/L,-dx/L));cols=max(1,int(L/2.8));step=L/cols
  for fl in range(2,int(h/3.3)):
   z=fl*3.3
   if style=='Hotel':fbox(F,0,z-.45,.18,L,.17,.42,'Painted plaster')
   for i in range(cols):
    u=-L/2+(i+.5)*step;city_window(F,u,z+1.0,min(1.8,step-.35),1.85)
  if style=='Wantai':
   for i in range(cols+1):fbox(F,-L/2+i*step,h/2,.28,.34,h,.52,'Ivory cornice')
  band(F,L,h-.6)
skyline_tower(-37,-119,49,20,65,'Wantai')
skyline_tower(32,-101,26,31,76,'Hotel')
# Actual photographed skyline lettering. Position/height are approximate within mapped building footprints.
street_text('万 泰 集 团',(-37,-104.4,66.1),3.0,(0,1),'Red enamel letters','Wantai_rooftop')
GROUP='South_hotel_crown'
lathe((32,-94,76),[(6.8,0),(6.8,1.0),(6.4,1.4),(5.2,4.0),(2.4,6.0),(.8,7.2)],'Roof burgundy',64)
for z,r in [(76.8,6.8),(78,6.3),(80,5.2)]:lathe((32,-94,z),[(r,0),(r+.25,.2)],'Painted plaster',64)
beam((32,-94,83),(32,-94,86),.09,'Iron black',8)
# Setback glass volume of the department store, behind its massive lower frontage.
GROUP='New_100_setback'
box('',(-183,52,33),(112,74,12),'Cool shop glazing')
for z in [28,31,34,37,39]:box('',(-183,52,z),(113,75,.12),'Window lead')
street_text('大商集团 DASHANG GROUP',(-124,45,39.6),2.3,(1,0),'Dark blue enamel','Dashang_group_photo_reference')
street_text('商业道里菜市场',(-111.1,42,24.5),2.0,(1,0),'Sign enamel','Daoli_market_photo_reference')
print('V2 differentiated mapped streets ready',flush=True)
