"""Visible corrections from gallery 2025/2018 and market 2025-06-21 photographs.

Executed in build_scene's metric geometry context. Dimensions are estimates; this
does not close the photo acceptance gate. No source photographs become textures.
"""
ACTIVE='05_STREET_PROPS'
for key in list(B):
 if key[1]=='V221_Gallery_roof_joinery':del B[key]

# Reuse the licensed scan's mortar-free face, with portable color/roughness/normal
# maps. A flat diffuse swatch disappears into plastic-looking blocks in the game.
pbr('Gallery dressed red stone','v2/brick_face',1.0)
material('Gallery cornice shadow',(.019,.035,.029),.78,.12,False)
material('Gallery lamp glass',(.68,.72,.64),.32,0,False)

def pier_courses(F,u):
 # Raised horizontal courses and inset faces, instead of an uninterrupted brick tile.
 for z,h,w in [(1.25,.23,1.13),(1.95,.50,1.04),(2.55,.50,1.04),(3.15,.50,1.04),(3.75,.50,1.04),(4.35,.50,1.04),(4.90,.22,1.22),(5.50,.30,1.30)]:
  fbox(F,u,z,0,w,h,w,'Gallery dressed red stone')
 for side in [-1,1]:
  fbox(F,u+side*.38,3.12,.545,.13,3.20,.09,'Gallery red sandstone')

def pier_lantern(F,u):
 fbox(F,u,4.77,.59,.19,.37,.09,'Iron dark green')
 path([F(u,4.65,.62),F(u,4.65,.91),F(u,4.96,1.05)],.029,'Iron dark green',10)
 for du in [-.20,.20]:
  path([F(u,4.72,.81),F(u+du,4.78,1.03),F(u+du,4.98,1.03)],.021,'Iron dark green',8)
  fbox(F,u+du,5.13,1.03,.19,.28,.19,'Gallery lamp glass')
  for a in [-.10,.10]:
   for b in [-.10,.10]:beam(F(u+du+a,4.97,1.03+b),F(u+du+a,5.29,1.03+b),.012,'Iron dark green',6)
  fbox(F,u+du,4.96,1.03,.24,.05,.24,'Iron dark green')
  add([F(u+du+a,5.30,1.03+b) for a,b in [(-.15,-.15),(.15,-.15),(.15,.15),(-.15,.15)]]+[F(u+du,5.43,1.03)],[(0,1,4),(1,2,4),(2,3,4),(3,0,4)],'Iron dark green')
  night_targets.append((F(u+du,5.10,1.1),F(u+du,2.1,2.0),'street',22))

for x,y,normal in [(-64,37.5,(-1,0)),(-64.8,72,(0,-1))]:
 F=frame((x,y,0),normal)
 GROUP='SOP_Gallery_terminal_twin_arches'
 local_solid(F,0,3.1,0,1.0,6.2,1.0,'Gallery red sandstone','gallery terminal middle pier')
 for u in [-3.8,0,3.8]:pier_courses(F,u)
 for u in [-1.9,1.9]:
  for j in range(3):arc(F,u,4.08,1.34+j*.09,.065,.17+j*.06,'Gallery aged coping',32)
  for k in range(1,10):
   a=k*pi/10
   beam(F(u,4.08,.39),F(u+1.30*cos(a),4.08+1.30*sin(a),.39),.014,'Iron dark green',8)
  for du in [-1.39,1.39]:fbox(F,u+du,3.03,.30,.055,2.10,.095,'Iron dark green')
 GROUP='SOP_Gallery_terminal_lanterns'
 for u in [-3.8,0,3.8]:pier_lantern(F,u)
 # May 2025 side photo shows the northern end has a taller lattice clerestory.
 # Its distinct roof is constructed by sop90_gallery_rework, not copied here.
 if normal==(0,-1):continue
 GROUP='SOP_Gallery_layered_cornice_and_hip_roof'
 for z,w,h,dep,mat in [(5.92,8.03,.22,.85,'Gallery aged coping'),(6.10,8.25,.12,1.05,'Gallery cornice shadow'),(6.23,8.44,.12,1.20,'Gallery aged coping'),(6.36,8.63,.10,1.38,'Gallery cornice shadow'),(6.49,8.79,.16,1.53,'Gallery aged coping')]:
  fbox(F,0,z,.13,w,h,dep,mat)
 for i in range(28):fbox(F,-4.05+i*.30,6.14,.78,.10,.17,.20,'Gallery aged coping')
 # Small central pediment sits in front of the set-back hipped metal roof.
 verts=[F(u,z,d) for d in [.00,.25] for u,z in [(-1.6,6.56),(1.6,6.56),(0,7.18)]]
 add(verts,[(0,2,1),(3,4,5),(0,1,4,3),(1,2,5,4),(2,0,3,5)],'Gallery aged coping')
 for j in range(2):path([F(-1.68,6.59+j*.07,.31),F(0,7.25+j*.07,.31),F(1.68,6.59+j*.07,.31)],.045,'Gallery aged coping',10)
 add([F(-3.96,6.62,-.88),F(3.96,6.62,-.88),F(3.96,6.62,-7.6),F(-3.96,6.62,-7.6),F(-2.65,7.74,-2.2),F(2.65,7.74,-2.2),F(2.65,7.74,-6.25),F(-2.65,7.74,-6.25)],[(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,6,7),(3,2,1,0)],'Gallery aged coping')
 # Raised sheet seams follow each pitch, not the world axes.
 for i in range(13):
  u=-3.75+i*.625
  beam(F(u,6.65,-.91),F(u*.67,7.77,-2.2),.013,'Gallery cornice shadow',6)
 for u in [-2.42,2.42]:
  arch_panel(F,u,6.70,.75,.74,-1.24,'Gallery cornice shadow')
  arc(F,u,7.065,.375,.105,-1.19,'Gallery dressed red stone',24)
  fbox(F,u,6.73,-1.11,.94,.10,.24,'Gallery dressed red stone')

# Right-hand retail display and narrower entry doors are visible in the June 2025
# straight-frontage photograph. Keep the unresolved curved entrance separate.
ACTIVE='03_OSM_BUILDINGS'
for key in list(B):
 if key[1]=='V221_Daoli_entries':del B[key]
material('Market door bronze',(.13,.135,.105),.44,.55,False)
material('Market soffit warm',(.31,.32,.285),.72,.15,False)
material('Market display card',(.70,.72,.63),.87,0,False)
material('Market retail red',(.38,.032,.018),.76,0,False)
material('Market retail blue',(.026,.115,.24),.64,0,False)
for F,normal,L in market_frames[:1]:
 GROUP='SOP_Market_recessed_entry_and_shops'
 fbox(F,0,2.15,.22,17.2,3.70,.12,'Window shadow')
 # Six narrow framed leaves at the left/middle; individual mullions and transoms.
 for k in range(6):
  u=5.5-k*1.05
  fbox(F,u,1.99,.32,.96,2.75,.07,'Cool shop glazing')
  for du in [-.515,.515]:fbox(F,u+du,2.10,.41,.065,3.02,.10,'Market door bronze')
  for z in [.61,3.36,3.66]:fbox(F,u,z,.41,1.05,.065,.10,'Market door bronze')
  fbox(F,u,3.51,.32,.96,.24,.07,'Cool shop glazing')
  beam(F(u-.20,1.52,.49),F(u-.20,2.06,.49),.016,'Market door bronze',10)
  fbox(F,u,.79,.43,.94,.26,.028,'Market door bronze')
 # Recessed shop returns, short shelves and dense hanging retail cards.
 for center,width in [(-2.15,2.1),(-4.48,2.1),(-7.05,2.55),(7.50,1.6)]:
  fbox(F,center,3.23,.45,width,.64,.16,'Market display card')
  for du in [-width/2,width/2]:fbox(F,center+du,2.02,.47,.09,2.98,.15,'Market door bronze')
  for row in range(6):
   z=.86+row*.35
   fbox(F,center,z,.61,width-.15,.035,.57,'Market door bronze')
   for col in range(max(1,int(width/.20))):
    u=center-width/2+.17+col*.20
    variant=(row*7+col)%5
    h=.16+.012*variant
    fbox(F,u,z+.145,.68,.135,h,.019,'Market display card')
    # Hanging souvenir cards: wire hook, metal ring and a small relief charm.
    beam(F(u,z+.27,.62),F(u,z+.27,.74),.004,'Market door bronze',6)
    path([F(u+.025*cos(a*pi/8),z+.18+.025*sin(a*pi/8),.699) for a in range(17)],.004,'Lamp reflector',6)
    sphere(F(u,z+.115,.709),.032,'Gold leaf' if variant in [0,3] else 'Lamp reflector',scale=(.62,.22,1.25),N=8,rings=5)
    fbox(F,u,z+.145+h/2-.022,.697,.11,.019,.008,'Market retail blue' if variant%2 else 'Market retail red')
 for text_,u in [('10元三个',-1.50),('小件寄存',-1.50),('5元1个',-4.58)]:
  z=3.26 if text_!='小件寄存' else 2.98
  street_text(text_,F(u,z,.56),.25,normal,'Market retail red','SOP_Market_price_'+text_)
 GROUP='SOP_Market_canopy_seams_and_soffit'
 width=18.0
 def edge_depth(u):return 1.45+1.15*math.sqrt(max(0,1-(u/9.0)**2))
 for i in range(36):
  a=-9+i*.5;b=a+.5;da=edge_depth(a);db=edge_depth(b)
  add([F(a,4.62,.1),F(b,4.62,.1),F(b,4.43,db),F(a,4.43,da),F(a,4.50,.1),F(b,4.50,.1),F(b,4.31,db),F(a,4.31,da)],[(0,1,2,3),(4,7,6,5),(2,6,7,3),(0,4,5,1)],'Market soffit warm')
  beam(F(a,4.39,da),F(b,4.39,db),.078,'Market canopy metal',16)
  beam(F(a,4.36,da),F(a+.055,4.36,edge_depth(a+.055)),.093,'Market canopy metal',16)
  beam(F(a,4.49,.1),F(a,4.30,da),.011,'Market panel joint',6)
  for t in [.25,.50,.75]:beam(F(a,4.49-.19*t,.1+(da-.1)*t),F(b,4.49-.19*t,.1+(db-.1)*t),.009,'Market panel joint',6)
 for u in [-7,-3.5,0,3.5,7]:
  d=edge_depth(u)
  beam(F(u,4.29,d-.12),F(u,4.48,.15),.031,'Market door bronze',8)
  beam(F(u,4.30,d-.12),F(u,5.82,.15),.022,'Market canopy metal',10)
  fbox(F,u,5.80,.18,.18,.27,.10,'Market canopy metal')
 # Retain the existing attached letters/logo; recreate their supports and LED housing.
 fbox(F,1.10,3.94,.51,12.2,.59,.21,'Iron black')
 for k in range(5):beam(F(4.9-k*2.45,4.50,.84),F(4.9-k*2.45,5.22,.84),.025,'Window lead',8)
 for u in [7.13,7.70,8.27]:
  arc(F,u,5.65,.23,.075,.85,'Gold leaf',20)
  for du in [-.27,.27]:fbox(F,u+du,5.48,.91,.07,.38,.14,'Gold leaf')
 fbox(F,7.7,5.18,.88,1.77,.41,.17,'Gold leaf')
 add([F(u,z,.98) for u,z in [(6.64,6.01),(7.2,6.22),(7.7,6.52),(8.2,6.22),(8.76,6.01),(8.17,6.13),(7.23,6.13)]],[(0,1,2,3,4,5,6)],'Gold leaf')
 for k in range(3):fbox(F,0,.10*(k+1),3.4-k*.36,12.8,.20*(k+1),.36,'Granite foundation')
 fbox(F,0,.30,1.39,12.8,.60,2.42,'Granite foundation')
print('SOP visible gallery/market repairs integrated; photographic acceptance remains OPEN',flush=True)
