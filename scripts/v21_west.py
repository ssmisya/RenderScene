"""V2.1 west massing, based on N509FZ 2023 west photographs and EditQ details.
Executed in build_scene.py. Dimensions are photo estimates, not survey data.
"""
ACTIVE='01_CATHEDRAL'
GROUP='V21_West_structural_masonry'
# Higher central bay with lower projecting shoulders: never a full-width tall box.
box('west central tower base',(-15.2,0,10.5),(9.4,9.3,19.6),brick,collide=True)
for sign in [-1,1]:
 box('west lower shoulder',(-18.25,sign*5.99,8.4),(4.6,2.78,15.4),brick,collide=True)
# Front centre and shoulders deliberately occupy different depth planes.
F=frame((-19.92,0,0),(-1,0))
S=frame((-20.57,0,0),(-1,0))

def slab_outline(F,u,z,w,h,d,mat=brick):
 fbox(F,u,z,d,w,h,.12,mat)

def inset_square(F,u,z,w=.68,h=.64,d=.10,boss=True):
 # The back is wall-colored; a deep raised frame casts a real recess shadow.
 fbox(F,u,z,d,w,h,.055,'Recessed soot')
 fbox(F,u,z,d+.04,w-.11,h-.11,.06,brick)
 for k in range(3):
  ww=w+k*.12;hh=h+k*.12;dep=d+.09+k*.045
  for side in [-1,1]:
   fbox(F,u+side*ww/2,z,dep,.070,hh+.06,.095,'Carved terracotta')
   fbox(F,u,z+side*hh/2,dep,ww+.07,.070,.095,'Carved terracotta')
 if boss:
  fbox(F,u,z-.03,d+.23,w*.36,h*.40,.10,'Carved terracotta')
  fbox(F,u,z-h*.15,d+.27,w*.59,h*.16,.10,'Carved terracotta')

def double_arch(F,u,z,w,d=.36,point=.70):
 r=w/4
 for side in [-1,1]:
  arch_panel(F,u+side*r,z,2*r,r,d-.035,brick)
  for k in range(3):radial_arch(F,u+side*r,z,r+k*.085,.065,d+k*.052,.10)
 # A triangular centre above the cusped pair; cap follows actual stepped outline.
 tip=z+r+point
 vs=[F(u-.34,z+r*.92,d),F(u,tip,d),F(u+.34,z+r*.92,d),F(u-.34,z+r*.92,d+.17),F(u,tip,d+.17),F(u+.34,z+r*.92,d+.17)]
 add(vs,[(0,1,2),(3,5,4),(0,3,4,1),(1,4,5,2),(2,5,3,0)],brick)
 path([F(u-.34,z+r*.92,d+.19),F(u,tip,d+.19),F(u+.34,z+r*.92,d+.19)],.027,'Iron dark green',6)

def tablet(F,u,bottom,w,h,d=.26):
 # Rectangular blind panel, slim engaged colonnettes, twin arched head and brick pendants.
 fbox(F,u,bottom+h/2,d,w,h,.10,'Recessed soot')
 fbox(F,u,bottom+h/2,d+.055,w-.14,h-.14,.08,brick)
 for side in [-1,1]:
  x=u+side*(w/2+.09)
  fbox(F,x,bottom+h/2,d+.14,.14,h+.20,.18,'Carved terracotta')
  beam(F(x,bottom+.10,d+.23),F(x,bottom+h-.10,d+.23),.082,'Carved terracotta',12)
  for j in range(int(h/.46)+1):
   zz=bottom+j*.46
   fbox(F,x,zz,d+.23,.25,.11,.21,'Carved terracotta')
   fbox(F,x,zz+.12,d+.22,.19,.075,.17,brick)
 for zz in [bottom-.09,bottom+h+.10]:
  for k in range(3):fbox(F,u,zz+k*.08,d+.16+k*.055,w+.5+k*.13,.10,.30,'Carved terracotta')
 double_arch(F,u,bottom+h+.34,w+.25,d+.25,.67)
 for j in range(7):
  x=u+(j-3)*(w+.50)/7;hh=.12+.10*(3-abs(j-3))
  fbox(F,x,bottom-.25-hh/2,d+.16,.18,hh,.23,'Carved terracotta')

# Photo-defined upper centre tablet and shorter paired flanking tablets.
GROUP='V21_West_blind_tablets'
tablet(F,0,12.15,1.74,6.52,.20)
for u in [-3.30,3.30]:tablet(F,u,10.12,1.35,3.28,.16)
# Low outer shoulders have 2 columns of paired square panels, not a vertical strip of crosses.
GROUP='V21_West_shoulder_recesses'
for sign in [-1,1]:
 for u in [sign*5.34,sign*6.54]:
  for z in [7.08,8.65,11.10,12.67]:inset_square(S,u,z,.57,.61,.09,True)
  fbox(S,u,9.87,.18,.68,.15,.13,'Carved terracotta')
 for u in [sign*4.76,sign*7.18]:fbox(S,u,10.10,.15,.17,10.7,.23,'Carved terracotta')
 # Projecting shoulder base with nested masonry panel, brick courses and stone footing.
 inset_square(S,sign*5.99,2.90,1.53,1.45,.10,True)
 for z,d,w,h in [(.55,.12,2.88,.23),(1.0,.18,3.00,.15),(1.36,.22,3.10,.14),(4.65,.24,3.03,.17),(4.92,.28,3.16,.18),(5.18,.34,3.28,.12)]:
  fbox(S,sign*5.99,z,d,w,h,.42,'Carved terracotta')
 for j in range(10):fbox(S,sign*5.99+(j-4.5)*.29,4.46,.25,.12,.17,.22,'Carved terracotta')
 # Same relief wraps around the exposed lateral returns.
 sf=frame((-18.2,sign*7.40,0),(0,sign))
 for uu in [-1.3,0,1.3]:
  for zz in [7.08,8.65,11.10,12.67]:inset_square(sf,uu,zz,.56,.61,.10,True)
 for zz in [4.9,5.15,15.80]:fbox(sf,0,zz,.22,4.7,.15,.35,'Carved terracotta')

# Central cornice stays on the narrow tall bay; shoulder eaves stop 4 m lower.
GROUP='V21_Stepped_eaves_and_roof_returns'
for z in [17.0,17.4,19.35,19.72]:
 fbox(F,0,z,.16,9.4,.13,.28,'Carved terracotta')
# Separate narrow centre cornice and actual pitched transition under octagonal bell chamber.
cornice_rect(-15.2,0,9.5,9.45,19.9)
hiproof(-15.2,0,9.9,9.9,20.45,1.05)

def sheet_slope(x0,x1,y0,y1,z0,z1):
 vs=[(x0,y0,z0),(x1,y0,z0),(x1,y1,z1),(x0,y1,z1)]
 add(vs,[(0,1,2,3)],'Painted roof 04')
 # Folded standing seams and a fine drip lip, scaled to metal sheets.
 for i in range(max(1,int((x1-x0)/.46))+1):
  x=x0+(x1-x0)*i/max(1,int((x1-x0)/.46))
  beam((x,y0,z0+.024),(x,y1,z1+.024),.012,'Dome seams',5)
 beam((x0,y0,z0),(x1,y0,z0),.035,'Iron dark green',8)
for sign in [-1,1]:
 # Hipped front termination avoids an open triangular void above the shoulder.
 A=Vector((-20.65,sign*7.64,16.20));B0=Vector((-20.65,sign*4.66,16.20));C0=Vector((-17.67,sign*4.66,18.55));D0=Vector((-5.8,sign*7.64,16.20));E0=Vector((-5.8,sign*4.66,18.55))
 add([tuple(p) for p in [A,B0,C0,D0,E0]],[(0,1,2),(0,2,4,3)],'Painted roof 04')
 for j in range(1,16):
  t=j/16;beam(A.lerp(B0,t)+Vector((0,0,.022)),C0,.012,'Dome seams',5)
 for j in range(1,30):
  t=j/30;beam(A.lerp(D0,t)+Vector((0,0,.022)),C0.lerp(E0,t)+Vector((0,0,.022)),.012,'Dome seams',5)
 cornice_rect(-18.25,sign*5.99,4.70,2.86,15.92)
 # Small gabled kokoshnik at the outside front corner, projecting above the eave.
 g=frame((-20.68,sign*6.12,0),(-1,0));crown(g,0,16.25,.62,.17,filled=True)
 # Small scalloped gables break the long side eave line.
 g=frame((-12.3,sign*7.66,0),(0,sign))
 for u in [-4.9,-1.65,1.65,4.9]:crown(g,u,16.18,.68,.13,filled=True)

# Entrance archivolt has real thickness and projects well forward of the central wall.
GROUP='V21_Deep_west_portal'
P=frame((-20.30,0,.36),(-1,0));portal(P,4.03,5.6)
# Rose is an ogee-shaped masonry surround, not a circular disc with a thin triangle stuck on it.
GROUP='V21_Ogee_oculus'
rz=11.0;inner=.55;outer=.91;dep=.95
radial_arch(F,0,rz,inner,.21,dep,.16,full=2*pi)
# Ogee profile: round lower shoulders narrowing into a raised point.
profile=[(-.74,rz-.48),(-1.00,rz-.06),(-.99,rz+.40),(-.76,rz+.82),(-.43,rz+1.14),(0,rz+1.58),(.43,rz+1.14),(.76,rz+.82),(.99,rz+.40),(1.00,rz-.06),(.74,rz-.48)]
for i in range(len(profile)-1):
 u0,z0=profile[i];u1,z1=profile[i+1]
 a0=math.atan2(z0-rz,u0);a1=math.atan2(z1-rz,u1)
 vs=[F(u0,z0,dep-.12),F(u1,z1,dep-.12),F(outer*.87*cos(a1),rz+outer*.87*sin(a1),dep-.12),F(outer*.87*cos(a0),rz+outer*.87*sin(a0),dep-.12)]
 add(vs,[(0,1,2,3)],brick)
 # Broad metal cap has an actual side surface connecting back to the wall.
 add([F(u0,z0,.08),F(u1,z1,.08),F(u1,z1,dep+.17),F(u0,z0,dep+.17)],[(0,1,2,3)],'Painted roof 04')
path([F(u,z,dep+.18) for u,z in profile],.028,'Iron dark green',6)
pts=[F(.52*cos(i*pi/32),rz+.52*sin(i*pi/32),dep+.18) for i in range(64)]
add(pts,[tuple(range(64))],'Door smoked glass')
# Distinctive white cross and eight rays visible in the west oculus.
for i in range(8):
 a=i*pi/4;beam(F(.08*cos(a),rz+.08*sin(a),dep+.21),F(.41*cos(a),rz+.41*sin(a),dep+.21),.016,'Window lead',8)
for zz in [rz-.30,rz+.30]:beam(F(-.10,zz,dep+.21),F(.10,zz,dep+.21),.014,'Window lead',8)
for uu in [-.30,.30]:beam(F(uu,rz-.10,dep+.21),F(uu,rz+.10,dep+.21),.014,'Window lead',8)

# Closed-entry exterior geometry, with modest plaques fixed on masonry jambs.
GROUP='V21_Entry_landing'
box('west threshold',(-20.68,0,.36),(1.5,4.0,.61),'Granite foundation',collide=True)
# Widening lower steps; door is seated exactly at the landing level.
for i in range(5):
 box('west front stair',(-21.4-i*.31,0,.10+(4-i)*.106),(.34,5.0+i*.15,.18),'Granite foundation',collide=True)
# Hardware plaques are added as small geometry; street_text is not yet defined here.
for sign in [-1,1]:fbox(P,sign*2.19,2.60,.59,.50,.31,.025,'Old brass hardware')

# Thick-walled octagonal belfry, narrow lower openings and short upper arcade.
GROUP='V21_Belfry_masonry_and_openings'
bx,by=-15.2,0;radius=4.55;apothem=radius*cos(pi/8);fw=2*radius*sin(pi/8)
lathe((bx,by,21.25),[(4.61,0),(4.61,.22),(4.50,.32)],'Carved terracotta',8,pi/8,False)

def opening_wall(F,bottom,top,opening_width,spring,width,thickness=.62):
 half=opening_width/2;side=(width-opening_width)/2
 for sign in [-1,1]:fbox(F,sign*(half+side/2),(bottom+top)/2,-thickness/2,side,top-bottom,thickness,brick)
 # Spandrel above the arch: a solid wall with a genuinely empty arched opening.
 for i in range(24):
  u0=-half+opening_width*i/24;u1=-half+opening_width*(i+1)/24
  z0=spring+math.sqrt(max(0,half*half-u0*u0));z1=spring+math.sqrt(max(0,half*half-u1*u1))
  vs=[F(u,z,d) for d in [-thickness,0] for u,z in [(u0,z0),(u1,z1),(u1,top),(u0,top)]]
  add(vs,[(0,3,2,1),(4,5,6,7),(0,1,5,4),(3,7,6,2),(0,4,7,3),(1,2,6,5)],brick)
for k in range(8):
 a=k*pi/4;BF=frame((bx+apothem*cos(a),apothem*sin(a),0),(cos(a),sin(a)))
 opening_wall(BF,21.55,27.52,1.24,25.72,fw)
 # Engaged shafts, broken brick quoins and small recessed ornaments on thick piers.
 for sign in [-1,1]:
  u=sign*1.29
  for z in [22.0,23.3,24.6]:inset_square(BF,u,z,.32,.42,.015,True)
  for j in range(12):fbox(BF,sign*(fw/2-.10),21.80+j*.45,.11,.25,.12,.25,'Carved terracotta')
 radial_arch(BF,0,25.72,.65,.25,.06,.18)
 radial_arch(BF,0,25.72,.93,.13,.17,.16)
 crown(BF,0,25.72,1.13,.22,filled=False)
 for u in [-.48,-.24,0,.24,.48]:fbox(BF,u,22.22,.055,.035,1.25,.04,'Iron black')
 fbox(BF,0,22.69,.055,1.26,.045,.05,'Iron black')
 for z in [25.53,25.68]:
  for sign in [-1,1]:fbox(BF,sign*1.24,z,.12,1.03,.10,.32,'Carved terracotta')
 # Upper openings are smaller and lower than the main bell openings.
 upper_ap=3.75*cos(pi/8);UF=frame((bx+upper_ap*cos(a),upper_ap*sin(a),0),(cos(a),sin(a)))
 opening_wall(UF,27.40,30.14,.96,28.91,2*3.75*sin(pi/8),.50)
 radial_arch(UF,0,28.91,.51,.22,.04,.16);crown(UF,0,28.91,.79,.18,filled=False)
lathe((bx,by,27.30),[(4.60,0),(4.61,.12),(3.70,.32)],'Painted roof 04',8,pi/8,False)
# Seven bronze bells, one larger central bell and six smaller bells, behind the openings.
GROUP='V21_Seven_bronze_bells'
for i in range(7):
 if i==0:x,y,rr,z=bx,0,.73,23.1
 else:
  a=(i-1)*pi/3;x,y,rr,z=bx+1.90*cos(a),1.90*sin(a),.27+.033*i,23.65+.07*i
 lathe((x,y,z),[(rr,0),(rr,.07),(rr*.80,.19),(rr*.48,rr*.96),(rr*.36,rr*1.27),(.06,rr*1.4)],'Old brass hardware',32)
 beam((x,y,z+rr*1.4),(x,y,26.70),.024,'Iron black',8)
 beam((x,y,z-.08),(x,y,z+.40),.035,'Iron black',8)
GROUP='V21_Belfry_tent_roof'
tent(bx,by,30.05,4.05,9.15)
print('V2.1 structural west: high centre, low shoulders, pitched returns, solid belfry piers',flush=True)
