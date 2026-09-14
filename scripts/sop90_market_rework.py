"""June 21 2025 entrance detail rework, from the reporter's full-resolution original.
Visible topology is modeled; hidden door geometry and physical dimensions remain estimates.
"""
ACTIVE='03_OSM_BUILDINGS'
for key in list(B):
 if key[1]=='SOP_Market_recessed_entry_and_shops':del B[key]
for ob in list(sign_objects):
 if ob.name.startswith(('SOP_Market_price_','V221_Market_LED_')):
  sign_objects.remove(ob);bpy.data.objects.remove(ob,do_unlink=True)
material('Market display ivory',(.73,.74,.68),.78,0,False)
material('Market magnet cobalt',(.025,.08,.24),.38,.18,False)
material('Market magnet forest',(.035,.14,.09),.45,.08,False)
material('Market magnet cream',(.64,.56,.37),.55,.1,False)
material('Market fascia orange',(.62,.075,.028),.60,0,False)
material('Market brushed steel',(.31,.34,.33),.31,.75,False)
material('Market LED dark red',(.12,.005,.003),.45,0,False)
for F,normal,L in market_frames[:1]:
 GROUP='SOP90_Market_observed_portals'
 # Real recess envelope prevents an open shell from exposing the opposite street.
 fbox(F,0,2.59,-2.50,18.2,4.12,.15,'Window shadow')
 fbox(F,0,.59,-.95,18.2,.08,3.1,'Granite foundation')
 fbox(F,0,4.59,-.95,18.2,.10,3.1,'Market soffit warm')
 for edge in [-9.06,9.06]:fbox(F,edge,2.59,-.95,.10,4.12,3.1,'Window shadow')
 # The photograph shows unequal posts and open leaves, rather than six identical glass rectangles.
 fbox(F,1.10,2.02,-1.13,12.4,3.32,.08,'Window shadow')
 bounds=[4.75,3.12,2.00,.43,-1.22]
 for idx,(left,right) in enumerate(zip(bounds,bounds[1:])):
  center=(left+right)/2;w=left-right
  for u in [left,right]:fbox(F,u,2.02,.50,.085,2.90,.15,'Market door bronze')
  for z in [.64,3.47,3.67]:fbox(F,center,z,.50,w,.075,.15,'Market door bronze')
  fbox(F,center,3.57,.39,w-.10,.14,.06,'Cool shop glazing')
  # Two clearly recessed portals, with open bronze leaf returns and dark interior.
  if idx in [0,2]:
   for u in [left-.10,right+.10]:
    fbox(F,u,2.02,-.18,.065,2.75,1.25,'Market door bronze')
   fbox(F,center,1.99,-1.0,w-.18,2.58,.05,'Window shadow')
  else:
   fbox(F,center,2.04,.40,w-.12,2.65,.07,'Cool shop glazing')
   fbox(F,center,.81,.50,w-.12,.30,.025,'Market door bronze')
   beam(F(center-.27,1.49,.60),F(center-.27,2.02,.60),.018,'Market brushed steel',10)
 # Narrow price/merchandise pegboards flank a genuinely recessed gift shop.
 GROUP='SOP90_Market_gift_shop'
 for u in [-1.86,-5.50]:
  w=1.16
  fbox(F,u,1.78,.68,w,2.27,.10,'Market display ivory')
  for du in [-w/2,w/2]:fbox(F,u+du,1.78,.75,.035,2.30,.035,'Market brushed steel')
  for row in range(11):
   for col in range(6):
    a=u-w/2+.12+col*.185;z=.83+row*.175
    beam(F(a,z+.12,.75),F(a,z+.12,.84),.0035,'Market brushed steel',6)
    path([F(a+.022*cos(t*pi/8),z+.067+.022*sin(t*pi/8),.825) for t in range(17)],.003,'Lamp reflector',6)
    m=['Gold leaf','Lamp reflector','Market magnet cobalt','Market magnet forest'][(row+col*3)%4]
    fbox(F,a,z+.005,.81,.084,.072,.023,m)
    sphere(F(a,z+.037,.828),.022,m,scale=(.75,.35,1.25),N=8,rings=5)
  fbox(F,u,3.04,.76,w,.67,.09,'Market display ivory')
 street_text('10元3个',F(-1.86,3.15,.823),.28,normal,'Market fascia orange','SOP90_Market_price_left')
 street_text('小件寄存',F(-1.86,2.89,.823),.23,normal,'Market fascia orange','SOP90_Market_luggage')
 street_text('5元1个',F(-5.50,3.16,.823),.30,normal,'Market fascia orange','SOP90_Market_price_right')
 u=-3.68;w=2.30
 # The gift shop is a recess with side walls, head and interior display.
 fbox(F,u,3.22,.40,w,.57,.16,'Market display ivory')
 for du in [-w/2,w/2]:fbox(F,u+du,1.82,-.25,.075,2.51,1.42,'Market door bronze')
 fbox(F,u,.68,-.20,w,.08,1.4,'Granite foundation')
 fbox(F,u,2.86,-.23,w,.075,1.4,'Market door bronze')
 fbox(F,u,1.77,-.92,w,2.16,.10,'Window shadow')
 street_text('东北冰箱贴 礼品店',F(u,3.20,.51),.235,normal,'Market fascia orange','SOP90_Market_gift_fascia')
 for row in range(6):
  z=1.02+row*.285
  fbox(F,u,z-.105,-.51,w-.10,.024,.70,'Market door bronze')
  for col in range(8):
   a=u-w/2+.18+col*.275
   m=['Market magnet cobalt','Market magnet forest','Market magnet cream'][(col+row*5)%3]
   fbox(F,a,z,-.27,.23,.245,.025,m)
   # Raised architectural souvenir reliefs with domes, plinths and windows.
   fbox(F,a,z-.018,-.245,.085,.10,.015,'Market display ivory')
   sphere(F(a,z+.046,-.235),.043,'Gold leaf',scale=(1,.4,1.3),N=8,rings=5)
   fbox(F,a,z-.085,-.23,.14,.019,.015,'Market display ivory')
 for center,text_,width in [(5.53,'马迭尔',1.48),(-7.02,'信誉至上',1.36)]:
  fbox(F,center,3.18,.42,width,.57,.11,'Market magnet forest')
  street_text(text_,F(center,3.18,.50),.28,normal,'Market display ivory','SOP90_Market_shop_'+text_)
  fbox(F,center,1.39,.46,width,1.35,.08,'Cool shop glazing')
 # Beverage counter and the narrow upright menu, separately visible left of entry.
 fbox(F,5.53,1.11,.79,1.45,.9,.62,'Market door bronze')
 fbox(F,4.76,2.22,.64,.41,2.03,.07,'Market display ivory')
 for j,t in enumerate(['手工雪糕','马迭尔冰棍','鲜榨果汁']):
  street_text(t,F(4.76,2.82-j*.32,.69),.10,normal,'Market retail blue','SOP90_Market_drink_menu_'+str(j))
 for row in range(2):
  for col in range(9):
   a=4.94+col*.14;d=.69+row*.13
   beam(F(a,1.61,d),F(a,1.83,d),.037,'Market magnet forest' if col%3 else 'Market retail blue',8)
   fbox(F,a,1.73,d,.077,.07,.077,'Market display ivory')
 GROUP='SOP90_Market_canopy_fittings'
 # Exposed slots are visible in the top of the curved front pipe, not uniform sleeves.
 for u,w in [(0.28,.90),(-1.30,.63),(-3.9,.68)]:
  d=1.45+1.15*math.sqrt(max(0,1-(u/9)**2))
  fbox(F,u,4.454,d-.01,w,.026,.105,'Window shadow')
 # Paired security cameras hang from the soffit to the right of the doorway.
 beam(F(-2.64,4.34,1.71),F(-2.64,4.11,1.71),.025,'Market brushed steel',8)
 for du in [-.10,.10]:
  fbox(F,-2.64+du,4.09,1.74,.12,.11,.24,'Market canopy metal')
  fbox(F,-2.64+du,4.09,1.87,.07,.066,.008,'Window shadow')
 # Exterior exhaust elbow and insulated duct at the right edge of this entrance.
 path([F(-8.47,4.65,.49),F(-8.47,6.67,.49),F(-8.55,6.87,.49),F(-9.10,6.87,.49)],.15,'Market brushed steel',16)
 for z in [5.00,5.61,6.25]:
  beam(F(-8.47,z-.024,.49),F(-8.47,z+.024,.49),.158,'Market canopy metal',16)
print('SOP90 observed market retail, entry recesses and canopy details rebuilt; visual audit remains open',flush=True)
