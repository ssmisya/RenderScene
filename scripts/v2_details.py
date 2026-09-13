"""Pedestrian-scale details and photographed north-square landmarks."""
ACTIVE='01_CATHEDRAL';GROUP='V2_Relief_panels'
# East-facing transept returns have glazed openings; avoid the previous blank rear walls.
for sy in [-1,1]:
 F=frame((8.54,sy*10,0),(1,0))
 for u in [-1.7,1.7]:window(F,u,6.1,1.35,6.3)
 for u in [-3.25,0,3.25]:
  fbox(F,u,10.0,.17,.45,11.6,.33,brick)
  for z in [6.1+i*.6 for i in range(16)]:fbox(F,u,z,.32,.54,.11,.22,'Carved terracotta')
 for u in [-1.7,1.7]:crown(F,u,16.5,.7,filled=True)
# Stepped brick panels and small cross-like centre bosses on the west plinth.
F=frame((-20.44,0,0),(-1,0))
for u in [-6.1,6.1]:
 for z,ww,hh in [(2.7,1.65,1.6),(8.0,1.0,.72),(10,1.0,.72),(12,1.0,.72),(14,1.0,.72),(16,1.0,.72),(18,1.0,.72)]:
  fbox(F,u,z,.35,ww,hh,.12,'Recessed soot')
  for k in range(3):
   w=ww-k*.17;h=hh-k*.17;dd=.43+k*.035
   for side in [-1,1]:
    fbox(F,u+side*w/2,z,dd,.09,h,.12,'Carved terracotta');fbox(F,u,z+side*h/2,dd,w,.09,.12,'Carved terracotta')
  fbox(F,u,z,.57,.32,.42,.13,'Carved terracotta');fbox(F,u,z,.58,.46,.16,.14,'Carved terracotta')
# Soot-darkened drip edges along cornices, with geometry rather than flat black stripes.
for sy in [-1,1]:
 F=frame((-12.8,sy*7.61,0),(0,sy))
 for z in [5.20,14.48,18.15]:
  fbox(F,0,z,.20,13.8,.045,.36,'Recessed soot')
# Entry plaques from the actual museum usage; precise typography is an approximation.
F=frame((-20.44,0,0),(-1,0))
for u,txt in [(-2.35,'全国重点文物保护单位'),(2.35,'哈尔滨市建筑艺术馆')]:
 fbox(F,u,2.60,1.12,.63,.46,.06,'Old brass hardware')
 street_text(txt,F(u,2.61,1.162),.045,(-1,0),'Door black lacquer','Entrance_plaque')
# Wheelchair access ramp on one side, fitted to the 0.55 m landing.
GROUP='V2_Entry_access'
box('door landing',(-21.2,0,.34),(1.60,7.4,.58),'Granite foundation',collide=True)
verts=[(-21.65,-3.7,.04),(-20.55,-3.7,.04),(-20.55,-10.7,.04),(-21.65,-10.7,.04),(-21.65,-3.7,.63),(-20.55,-3.7,.63),(-20.55,-10.7,.06),(-21.65,-10.7,.06)]
add(verts,[(0,1,2,3),(4,7,6,5),(0,4,5,1),(1,5,6,2),(2,6,7,3)],'Granite foundation')
for xx in [-21.65,-20.55]:
 beam((xx,-3.7,1.48),(xx,-10.7,.94),.027,'Window lead',10)
 for yy in [-3.7,-5.7,-7.7,-9.7]:
  zz=.63-(abs(yy)-3.7)/7*.57;beam((xx,yy,zz),(xx,yy,zz+.85),.023,'Window lead',8)
# Small visible projector housings at ledges and base, recording targets for NIGHT.
GROUP='V2_Architectural_projector_fixtures'
def projector(pos,target,power=100,kind='cathedral'):
 night_targets.append((pos,target,kind,power))
 p=Vector(pos);t=Vector(target);axis=(t-p).normalized();u=axis.cross(Vector((0,0,1)))
 if u.length<.01:u=Vector((1,0,0))
 u.normalize();v=axis.cross(u);a=.14;b=.10;depth=.12
 vs=[tuple(p+u*x+v*y+axis*z) for x,y,z in [(-a,-b,-depth),(a,-b,-depth),(a,b,-depth),(-a,b,-depth),(-a,-b,0),(a,-b,0),(a,b,0),(-a,b,0)]]
 add(vs,[(0,3,2,1),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],'Iron black')
 add([tuple(p+u*x+v*y) for x,y in [(-a*.85,-b*.80),(a*.85,-b*.80),(a*.85,b*.80),(-a*.85,b*.80)]],[(0,1,2,3)],'Lamp reflector')
 beam(pos,(pos[0],pos[1],pos[2]-.20),.027,'Iron black',8)
for sy in [-1,1]:
 for x in [-18.6,-15.0,-11.5,-7.8]:projector((x,sy*8.25,5.55),(x,sy*7.8,15.6),95)
 for x in [-3.8,-.4,3.4,7.6]:projector((x,sy*14.65,5.35),(x,sy*14.15,14.1),110)
 for x in [-17,-10,-2,7]:projector((x,sy*(16.0 if x>-5 else 9.5),.8),(x,sy*(14.1 if x>-5 else 7.5),4.3),45)
for u in [-6,-4.3,-2.3,2.3,4.3,6]:projector((-21.30,u,5.35),(-20.60,u,17.8),105)
for u in [-5.3,5.3]:projector((-22.4,u,.8),(-20.6,u,3.3),70)
for k in range(16):
 a=k*pi/8;projector((2+6.33*cos(a),6.33*sin(a),26.85),(2+5.9*cos(a),5.9*sin(a),34.1),125,'drum')
for k in range(8):
 a=k*pi/4;projector((-15.2+4.38*cos(a),4.38*sin(a),21.7),(-15.2+3.75*cos(a),3.75*sin(a),28),85,'belltower')
for k in range(7):
 a=-pi/2+k*pi/6;projector((13.5+7.7*cos(a),7.7*sin(a),5.5),(13.5+7.1*cos(a),7.1*sin(a),13.8),80)
# Fine metal access ladder / cage beside drum, confirmed in modern photographs.
GROUP='V2_Roof_maintenance'
for y in [-.28,.28]:beam((8.38,y,25.8),(8.38,y,40),.025,'Iron black',8)
for i in range(45):beam((8.38,-.28,26+i*.30),(8.38,.28,26+i*.30),.017,'Iron black',6)
for z in [28,30,32,34,36,38]:path([(8.38+.55*sin(a*pi/16),.44*cos(a*pi/16),z) for a in range(17)],.015,'Iron black',6)
# Enclosed octagonal kiosks on mapped circular footprints. The previous open gazebo geometry is removed.
ACTIVE='05_STREET_PROPS';GROUP='V2_Mapped_kiosks'
for oid in ['338425687','338425941']:
 o=next(o for o in mapdata if o['id']==oid);ps=o['aligned_xy'][:-1];x=sum(p[0] for p in ps)/len(ps);y=sum(p[1] for p in ps)/len(ps)
 cylinder((x,y,.02),4.8,.26,'Granite foundation',48)
 lathe((x,y,.28),[(4.15,0),(4.15,3.35)],'Timber doors',8,pi/8,False)
 collision.append({'name':'enclosed_kiosk','type':'cylinder','center':[x,y,1.85],'radius':4.15,'height':3.7})
 for k in range(8):
  a=k*pi/4;F=frame((x+3.84*cos(a),y+3.84*sin(a),0),(cos(a),sin(a)))
  fbox(F,0,1.85,.07,2.72,2.75,.06,'Cool shop glazing')
  for u in [-1.4,-.46,.46,1.4]:fbox(F,u,1.85,.13,.075,2.86,.13,'Timber doors')
  fbox(F,0,3.5,.17,3.2,.42,.16,'Canvas cream')
 lathe((x,y,3.70),[(4.95,0),(4.55,.30),(3.3,1.70),(0,2.50)],'Painted roof 04',8,pi/8,False)
 for k in range(8):
  a=k*pi/4+pi/8;beam((x+4.95*cos(a),y+4.95*sin(a),3.72),(x,y,6.20),.028,'Iron dark green',6)
 for k in range(8):
  a=k*pi/4;rr=3.5;lathe((x+rr*cos(a),y+rr*sin(a),5),[(.10,0),(.12,.28),(.26,.5),(.20,.70),(0,.80)],'Gold leaf',20)
 street_text('联升服装广场',(x,y-3.89,3.46),.34,(0,-1),'Old brass hardware','Kiosk_photo_reference')
# Green steel bell/clock landmark seen in the north-square tourist panoramas.
GROUP='V2_North_square_clock_tower';x,y=-55.2,107.0
cylinder((x,y,.03),3.0,.45,'Granite foundation',48)
collision.append({'name':'north_clock_tower','type':'cylinder','center':[x,y,1.5],'radius':2.7,'height':3.0})
for sx in [-1,1]:
 for sy in [-1,1]:
  px=x+sx*1.95;py=y+sy*1.95
  beam((px,py,.4),(px,py,24.5),.105,'Iron dark green',12)
  for dx,dy in [(sx*.24,0),(0,sy*.24)]:beam((px+dx,py+dy,.4),(px+dx,py+dy,24.5),.037,'Window lead',8)
for z in [1.0,5.0,9.5,14.1,18.6,23.4]:
 for sx in [-1,1]:
  beam((x-2.4,y+sx*2.1,z),(x+2.4,y+sx*2.1,z),.09,'Iron dark green',10)
  beam((x+sx*2.1,y-2.4,z),(x+sx*2.1,y+2.4,z),.09,'Iron dark green',10)
 for k in range(4):
  a=k*pi/2;F=frame((x+2.13*cos(a),y+2.13*sin(a),0),(cos(a),sin(a)))
  if z<19:
   for u in [-1.25,-.63,0,.63,1.25]:
    fbox(F,u,z+2.0,.01,.045,3.5,.05,'Iron dark green')
   arc(F,0,z+2.85,1.45,.05,.02,'Iron dark green',28)
   path([F(-1.75,z+.1),F(0,z+2),F(1.75,z+.1)],.023,'Window lead',6)
# Clock box and four clock faces, showing a fixed architectural dial (not a running clock).
box('',(x,y,25),(4.8,4.8,3.0),'Iron dark green')
for k in range(4):
 a=k*pi/2;F=frame((x+2.415*cos(a),y+2.415*sin(a),0),(cos(a),sin(a)))
 arc(F,0,25,.88,.08,.08,'Gold leaf',48,0,2*pi)
 add([F(.84*cos(i*pi/24),25+.84*sin(i*pi/24),.08) for i in range(48)],[tuple(range(48))],'Cream lamp glass')
 for j in range(12):
  aa=j*pi/6;beam(F(.67*cos(aa),25+.67*sin(aa),.10),F(.77*cos(aa),25+.77*sin(aa),.10),.025,'Iron black',6)
 beam(F(0,25,.13),F(.48,25.32,.13),.029,'Iron black',8);beam(F(0,25,.14),F(-.20,25.60,.14),.020,'Iron black',8)
 night_targets.append((F(0,23.6,1.9),F(0,25,.1),'clock',70))
lathe((x,y,26.7),[(3.6,0),(2.8,.65),(1.65,2.1),(.12,9.1)],'Iron dark green',4,pi/4,False)
for k in range(4):
 a=k*pi/2+pi/4;xx=x+2.8*cos(a);yy=y+2.8*sin(a)
 lathe((xx,yy,26.5),[(.65,0),(.10,5.8)],'Iron dark green',4,pi/4,False);sphere((xx,yy,32.4),.11,'Gold leaf',N=12,rings=8)
beam((x,y,35.8),(x,y,37.5),.045,'Gold leaf',8)
# Clock tower structure stays visibly open below its dial, unlike a solid medieval turret.
# Carousel anchors the mapped circular footprint. Detailed canopy; no invented giant fountain.
GROUP='V2_North_square_carousel';x,y=-24.8,89.6
cylinder((x,y,.03),4.8,.24,'Granite foundation',64);cylinder((x,y,.29),4.15,.15,'Roof burgundy',64)
beam((x,y,.30),(x,y,4.5),.25,'Gold leaf',16)
for k in range(12):
 a=k*pi/6;xx=x+3.2*cos(a);yy=y+3.2*sin(a);beam((xx,yy,.45),(xx,yy,3.45),.027,'Gold leaf',8)
 # Empty period-style carousel seats instead of coarse animal mannequins.
 sphere((xx,yy,1.04),.34,'Ivory cornice',scale=(1.0,.60,.55),N=14,rings=8)
lathe((x,y,3.5),[(4.7,0),(4.5,.3),(.2,2.2)],'Canvas cream',48)
for k in range(24):
 a=k*pi/12;beam((x+4.7*cos(a),y+4.7*sin(a),3.52),(x+.18*cos(a),y+.18*sin(a),5.7),.029,'Gold leaf',6)
# Realistic street-level life cues without blocking the FPS circulation ring.
GROUP='V2_Umbrellas_and_service_booth'
for x,y,r in [(-10,-20,2.15),(-9,20,2.15),(26,-11,2.2),(-50,114,2.2)]:
 beam((x,y,.10),(x,y,2.9),.033,'Iron dark green',10);cylinder((x,y,.02),.34,.07,'Granite foundation',20)
 lathe((x,y,2.45),[(r,0),(.1,.65)],'Canvas green',8,pi/8,False)
 for k in range(8):
  a=k*pi/4+pi/8;beam((x+r*cos(a),y+r*sin(a),2.44),(x,y,3.1),.012,'Iron black',5)
 box('service counter',(x,y,.62),(1.50,.70,1.24),'Timber doors',collide=True)
# Small museum ticket hut behind entry on its mapped site.
x,y=-21,-22.2;box('ticket hut',(x,y,1.35),(5.7,2.7,2.7),'Painted plaster',collide=True);hiproof(x,y,6.1,3.1,2.8,.72,'Roof burgundy')
F=frame((x,y-1.38,0),(0,-1))
for u in [-2,0,2]:arch_shop(F,u,.15,1.6,2.3)
street_text('建筑艺术馆  服务中心',(-21,-23.65,2.54),.19,(0,-1),'Red enamel letters','Museum_service_hut')
# Blue information boards beside the entry seen in the modern tourist images.
for x,y in [(-24,-9),(-25,8),(-8,-19),(27,6)]:
 box('',(x,y,.80),(.65,.045,.85),'Dark blue enamel')
 for xx in [x-.25,x+.25]:beam((xx,y,.08),(xx,y,1.24),.017,'Window lead',7)
 for zz in [.58,.67,.76,.85,.99]:box('',(x,y-.027,zz),(.48,.01,.015),'Ivory cornice')
# Dense clipped conifers and leafy shrubs, using leaf geometry rather than stacked cones.
ACTIVE='04_VEGETATION';GROUP='V2_Dense_entry_foliage'
rr=random.Random(551)
for x,y in [(-22,-6),(-22,6),(24,-5),(24,5),(-6,-17),(-6,17)]:
 for j in range(1800):
  zz=rr.uniform(1,3.8);a=rr.uniform(0,2*pi);rad=(3.95-zz)*.30*rr.random()**.4
  leaf((x+rad*cos(a),y+rad*sin(a),zz),rr.uniform(.06,.13),a+rr.uniform(-.5,.5),rr.uniform(-.6,.6),'Leaves %02d'%rr.randrange(6))
# Hedges along outer plazas, avoiding the measured cathedral footprint and walking loop.
for x,y,sx,sy in [(-80,0,4,18),(-81,56,4,17),(47,61,5,17),(46,86,5,13),(-13,103,18,2.2)]:
 box('hedge planter',(x,y,.19),(sx+.3,sy+.3,.38),'Granite foundation',collide=True);box('',(x,y,.4),(sx,sy,.05),'Soil')
 for j in range(int(sx*sy*75)):
  xx=x+rr.uniform(-sx/2,sx/2);yy=y+rr.uniform(-sy/2,sy/2);zz=rr.uniform(.6,1.6)
  leaf((xx,yy,zz),rr.uniform(.075,.17),rr.random()*2*pi,rr.uniform(-1,1),'Leaves %02d'%rr.randrange(8))
# Paver seams, patched stones and tiny irregular cracks limited to a plausible scale.
ACTIVE='02_SQUARE';GROUP='V2_Paving_repairs'
for i in range(75):
 x=rr.uniform(-86,40);y=rr.uniform(-44,100)
 if -25<x<28 and -17<y<17:continue
 xx=round(x/1.2)*1.2;yy=round(y/.65)*.65
 if i%4==0:box('',(xx+.6,yy+.325,.014),(1.189,.639,.023),'Granite foundation')
 else:
  pts=[(xx+.18,yy+.05,.028),(xx+.34,yy+.22,.028),(xx+.42,yy+.37,.028),(xx+.73,yy+.62,.028)];path(pts,.0018,'Recessed soot',4)
print('V2 portal, street details, lighting fixtures and landmarks ready',flush=True)
# Toulong Street is a genuine roadway immediately south of the square; it must not be paved over.
ACTIVE='06_ROADS';GROUP='V2_Street_crossings_and_sidewalks'
box('Toulong south footway',(0,-51.9,-.07),(174,3.3,.25),'Granite foundation',collide=True)
box('Zhaolin west footway',(-108,49,-.07),(4.5,182,.25),'Granite foundation',collide=True)
for x in [-80,77]:
 for i in range(11):box('',(x+i*.62,-43.1,-.124),(.31,8.4,.014),'Road paint')
# Low curbside rail with open sightlines; foliage and benches stay on the square side of Toulong.
for x in range(-75,73,5):
 if -6<x<12:continue
 beam((x,-35.0,.15),(x,-35.0,.9),.032,'Iron dark green',8)
 for z in [.43,.84]:beam((x,-35.0,z),(x+4.85,-35,z),.028,'Iron dark green',8)
# Parked vehicles provide street scale. Compact background meshes, not hero assets.
ACTIVE='05_STREET_PROPS';GROUP='V2_Curbside_vehicles'
for i,col in enumerate([(.035,.053,.079),(.44,.43,.40),(.08,.013,.016),(.025,.026,.029)]):material('Vehicle paint %d'%i,col,.23,.62)
material('Rubber tyre',(.009,.010,.011),.85)
def car(x,y,ang,color):
 co=cos(ang);si=sin(ang)
 def P(u,v,z):return(x+co*u-si*v,y+si*u+co*v,z-.13)
 mat='Vehicle paint %d'%color
 # Rounded hood/body belt, raised passenger cabin with sloping windscreen.
 stations=[(-2.22,.70,.49),(-2.05,.89,.78),(-1.5,.91,.90),(-.9,.91,1.08),(.90,.91,1.06),(1.62,.87,.85),(2.15,.72,.60)]
 vs=[]
 for u,w,z in stations:vs.extend([P(u,-w,.40),P(u,w,.40),P(u,w,z),P(u,-w,z)])
 fs=[]
 for j in range(len(stations)-1):
  for k in range(4):a=j*4+k;b=j*4+(k+1)%4;fs.append((a,b,b+4,a+4))
 fs.extend([(0,1,2,3),tuple(range(len(vs)-4,len(vs)))]);add(vs,fs,mat,True)
 v=[P(-1.1,-.77,.92),P(-1.1,.77,.92),P(1.35,.77,.96),P(1.35,-.77,.96),P(-.60,-.68,1.48),P(-.60,.68,1.48),P(.62,.68,1.49),P(.62,-.68,1.49)]
 add(v,[(4,5,6,7)],mat);add(v,[(0,1,5,4),(2,3,7,6),(0,4,7,3),(1,2,6,5)],'Cool shop glazing')
 for sy in [-1,1]:
  beam(P(-.08,sy*.78,.95),P(-.08,sy*.69,1.50),.041,mat,8)
  for u in [-1.35,1.35]:
   beam(P(u,sy*.86,.36),P(u,sy*1.0,.36),.33,'Rubber tyre',32)
   beam(P(u,sy*1.003,.36),P(u,sy*1.023,.36),.21,'Window lead',24)
   for j in range(5):
    a=j*2*pi/5;beam(P(u,sy*1.031,.36),P(u+.18*cos(a),sy*1.031,.36+.18*sin(a)),.021,'Lamp reflector',6)
 for sy in [-1,1]:
  sphere(P(1.97,sy*.57,.73),.15,'Cream lamp glass',(.4,1,.44),N=12,rings=8)
  sphere(P(-2.12,sy*.59,.63),.11,'Red enamel letters',(.35,1,.44),N=12,rings=8)
 collision.append({'name':'parked_vehicle','type':'box','center':[x,y,.64],'size':[4.5,2.0,1.55],'rotation_z':ang})
for i,(x,y,a) in enumerate([(-66,-46.5,0),(-53,-46.5,0),(51,-46.5,pi),(-103,6,pi/2),(-103,20,pi/2)]):car(x,y,a,i%4)
