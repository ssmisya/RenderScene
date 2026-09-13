"""2025 photo-led street corrections. Dimensions remain estimates; see evidence gate.
References: v2_2 brick_gallery_2025, steel_gallery_2025, xinhua_moon_0_2025,
hualian_2025_a, golden_sun_2025_a. No reference photos are used as textures.
"""
# Remove the previous single-file arcade strips: mapped outlines are L-shaped passages.
for key in list(B):
 if key[1]=='Mapped_brick_arcades':del B[key]
collision[:]=[c for c in collision if c['name']!='arcade pier']
ACTIVE='05_STREET_PROPS';GROUP='V22_Brick_gallery_L_plan'
material('Gallery red sandstone',(.28,.105,.075),.82)
material('Gallery aged coping',(.12,.18,.15),.65,.35)
# The OSM L footprints constrain the two wings. Roof thickness, bays and stairs are photo estimates.
def gallery_run(a,b,width,bays):
 dx=b[0]-a[0];dy=b[1]-a[1];length=math.hypot(dx,dy);ux=dx/length;uy=dy/length;nx=-uy;ny=ux
 for side in [-1,1]:
  F=frame(((a[0]+b[0])/2+side*nx*width/2,(a[1]+b[1])/2+side*ny*width/2,0),(side*nx,side*ny))
  for i in range(bays+1):
   u=-length/2+i*length/bays;pos=F(u,3.1)
   box('gallery pier',pos,(1.00,1.0,6.2),'Gallery red sandstone',collide=True)
   for z,w,h,d in [(.22,1.25,.44,1.26),(1.0,1.08,.22,1.10),(4.85,1.16,.20,1.2),(5.5,1.26,.30,1.28)]:fbox(F,u,z,.08,w,h,d,'Gallery red sandstone')
   for du in [-.35,.35]:
    fbox(F,u+du,3.3,.55,.13,3.0,.09,'Carved terracotta')
  for i in range(bays):
   u=-length/2+(i+.5)*length/bays;r=(length/bays-1.0)/2
   for j in range(3):arc(F,u,4.08,r+j*.09,.07,.12+j*.06,'Gallery aged coping',24)
   # Photo shows metal tracery within the upper arch, not a solid wall filling the passage.
   for k in range(1,10):
    aa=k*pi/10;path([F(u,4.08,.31),F(u+r*.95*cos(aa),4.08+r*.95*sin(aa),.31)],.016,'Iron dark green',6)
  for z,h,depth in [(6.05,.28,.6),(6.35,.22,.85),(6.57,.12,1.02)]:fbox(F,0,z,.08,length+1.2,h,depth,'Gallery aged coping')
 mid=((a[0]+b[0])/2,(a[1]+b[1])/2)
 box('',(mid[0],mid[1],6.52),(length+.8,width+1.1,.18),'Gallery aged coping',math.atan2(dy,dx))
# L returns replace the previous straight-only representation.
gallery_run((-64,37.5),(-50.5,37.5),7.6,3)
gallery_run((-50.5,37.5),(-50.5,54.5),7.6,4)
gallery_run((-64.8,72.0),(-64.8,104.1),7.8,7)
gallery_run((-64.8,104.1),(-50.0,104.1),7.8,3)
# Raised entrances, side rails and pediments on the terminal pavilions are clearly visible in 2025.
GROUP='V22_Gallery_terminal_pediments'
for x,y,normal in [(-64,37.5,(-1,0)),(-64.8,72.0,(0,-1))]:
 F=frame((x,y,0),normal)
 for k in range(7):
  # Stairs occupy a short entrance apron; not the main walking loop around the church.
  p=F(0,.075*(k+1),4.8-k*.34)
  box('gallery stair',p,(.34,6.4,.15*(k+1)) if normal[0] else (6.4,.34,.15*(k+1)),'Granite foundation',collide=True)
 add([F(-3.8,6.72,0),F(3.8,6.72,0),F(0,8.0,0)],[(0,1,2)],'Gallery aged coping')
 path([F(-3.9,6.7,.16),F(0,8.12,.16),F(3.9,6.7,.16)],.13,'Gallery aged coping',8)
 for side in [-1,1]:
  path([F(side*3.2,1.0,5),F(side*3.2,1.85,2.3)],.035,'Iron dark green',8)
# Open steel lateral gallery around the tower. Multi-layer rings / diamond infill are in the night closeup.
GROUP='V22_Steel_lateral_gallery';ACTIVE='05_STREET_PROPS'
x=-55.2;y=107.0
for side in [-1,1]:
 F=frame((x+side*3.2,y-9.0,0),(side,0))
 for i in range(6):
  u=-10+i*4
  for du in [-.31,.31]:
   fbox(F,u+du,4.35,0,.10,8.7,.12,'Iron dark green')
  for z in [.35,1.1,3.6,6.7,8.35]:fbox(F,u,z,.06,.95,.19,.5,'Iron dark green')
  # Diamond-pattern lattice, referenced but not dimensionally surveyed.
  for z in [1.5,2.2,2.9]:
   path([F(u-.23,z,.1),F(u,z+.35,.1),F(u+.23,z,.1),F(u,z-.35,.1),F(u-.23,z,.1)],.018,'Iron dark green',6)
 for i in range(5):
  u=-8+i*4
  for j in range(3):arc(F,u,4.5,1.60+j*.10,.065,.05+j*.04,'Iron dark green',24)
 for z in [7.05,7.40,8.20,8.60]:fbox(F,0,z,0,21.5,.12,.18,'Iron dark green')
 for i in range(21):
  u=-10+i
  path([F(u,7.4),F(u+.5,8.2),F(u+1,7.4)],.022,'Iron dark green',6)
for yy in [y-19+i*2 for i in range(11)]:
 # Barrel-vault ribs cross the gallery width; each is genuinely open mesh.
 F=frame((x,yy,0),(0,1));arc(F,0,7.15,3.25,.065,0,'Iron dark green',32)
for xx in [-3.25,-2.3,0,2.3,3.25]:
 zz=7.15+math.sqrt(max(0,3.25**2-xx**2));beam((x+xx,y-19,zz),(x+xx,y+1,zz),.033,'Iron dark green',8)
# Roof dormers/coping/corner crown improve the previously blank roofline.
ACTIVE='03_OSM_BUILDINGS';GROUP='V22_Commercial_roof_details'
for cx,cy,sx,sy,h in [(-12,131.5,121,21,22.0),(75,80,23,100,23.0),(72.5,36,25,21,30.5)]:
 for normal,center,L in [((0,-1),(cx,cy-sy/2,0),sx),((0,1),(cx,cy+sy/2,0),sx),((-1,0),(cx-sx/2,cy,0),sy),((1,0),(cx+sx/2,cy,0),sy)]:
  F=frame(center,normal)
  # Moulded cornice with dentils, seam strips, and dormer framing.
  for i in range(max(1,int(L/.55))):fbox(F,-L/2+(i+.5)*.55,h-.25,.48,.18,.26,.30,'Ivory cornice')
  count=max(1,int(L/8))
  for i in range(count):
   u=-L/2+(i+.5)*L/count
   for du in [-.76,.76]:fbox(F,u+du,h+.65,-.4,.18,1.4,.28,'Painted plaster')
   arc(F,u,h+1.0,.71,.16,-.4,'Painted plaster',24)
   fbox(F,u,h+.63,-.21,.045,1.10,.05,'Window lead')
  # Downpipes are functional vertical routes, not randomly floating facade props.
  for u in [-L/2+.5,L/2-.5]:
   beam(F(u,.15,.34),F(u,h-.3,.34),.052,'Gallery aged coping',10)
   beam(F(u,.15,.34),F(u,.06,.65),.052,'Gallery aged coping',10)
print('V22 evidence-led street corrections applied; accuracy gate pending',flush=True)
# 2024-25 CNR aerial/ground evidence shows a circular glazed opening with green rail,
# not a carousel with seats. Preserve mapped centre; remove the invented canopy/chairs.
for key in list(B):
 if key[1]=='V2_North_square_carousel':del B[key]
ACTIVE='05_STREET_PROPS';GROUP='V22_Circular_glazed_opening';x,y=-24.8,89.6
lathe((x,y,.03),[(3.55,0),(4.6,0),(4.6,.22),(3.55,.22)],'Granite foundation',64)
lathe((x,y,.08),[(0,.58),(1,.52),(2,.36),(3.45,.08)],'Cool shop glazing',64)
for k in range(16):
 a=k*pi/8
 beam((x,y,.67),(x+3.48*cos(a),y+3.48*sin(a),.17),.024,'Iron dark green',6)
for k in range(40):
 a=k*pi/20
 beam((x+4.15*cos(a),y+4.15*sin(a),.25),(x+4.15*cos(a),y+4.15*sin(a),1.18),.033,'Iron dark green',8)
for z in [.45,1.15]:lathe((x,y,z),[(4.13,0),(4.20,0),(4.20,.06),(4.13,.06)],'Iron dark green',64)
collision.append({'name':'glazed opening perimeter','type':'cylinder','center':[x,y,.6],'radius':4.25,'height':1.2})
# Roof identification visible in the CNR aerial and Xinhua night photograph.
ACTIVE='03_OSM_BUILDINGS';GROUP='V22_Manhattan_roof_letters'
street_text('MANHATTAN',(-9,-53.2,25.0),2.6,(0,1),'Ivory cornice','V22_Manhattan_rooftop')
