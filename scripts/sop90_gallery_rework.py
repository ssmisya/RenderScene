"""Brick-gallery interior arch and ironwork reconstruction from close photographs.
2022/2024 photographs are historical structural evidence, not recent-photo quota.
"""
ACTIVE='05_STREET_PROPS'
GROUP='SOP90_Gallery_interior_lamps_and_guards'
# Interior wall lanterns differ from the paired front-facing fixtures.
def interior_lamp(F,u):
 z=3.60
 fbox(F,u,z,.59,.16,.34,.08,'Iron dark green')
 path([F(u,z+.20,.61),F(u,z+.28,.87),F(u,z+.06,.98)],.02,'Iron dark green',10)
 # Slender six-sided cage, pale diffuser, pointed cap and lower finial.
 center=Vector(F(u,z-.10,.97));N=6
 v=[]
 for zz,r in [(-.25,.08),(-.17,.13),(.22,.13),(.29,.055)]:
  v.extend([tuple(center+Vector((cos(a*2*pi/N)*r,sin(a*2*pi/N)*r,zz))) for a in range(N)])
 add(v,[(j*N+k,j*N+(k+1)%N,(j+1)*N+(k+1)%N,(j+1)*N+k) for j in range(3) for k in range(N)],'Gallery lamp glass')
 for k in range(N):
  a=k*2*pi/N;off=Vector((cos(a)*.14,sin(a)*.14,0))
  beam(tuple(center+off+Vector((0,0,-.19))),tuple(center+off+Vector((0,0,.24))),.012,'Iron dark green',6)
 for zz,r in [(-.23,.09),(-.18,.15),(.25,.15),(.29,.08)]:
  path([tuple(center+Vector((r*cos(a*pi/12),r*sin(a*pi/12),zz))) for a in range(25)],.02,'Iron dark green',8)
 beam(tuple(center+Vector((0,0,-.23))),tuple(center+Vector((0,0,-.36))),.055,'Iron dark green',10,.008)
 night_targets.append((F(u,z-.10,1.10),F(u,z-.45,0),'street',9))

runs=[((-64,37.5),(-50.5,37.5),7.6,3),((-50.5,37.5),(-50.5,54.5),7.6,4),((-64.8,72),(-64.8,104.1),7.8,7),((-64.8,104.1),(-50,104.1),7.8,3)]
for a,b,width,bays in runs:
 dx=b[0]-a[0];dy=b[1]-a[1];L=math.hypot(dx,dy);nx=-dy/L;ny=dx/L
 # The close photo looks from the interior through the plaza-side bays.
 # Preserve the outside public entrances; add guards only to the plaza-facing side.
 side=1 if nx>=0 else -1
 outer=(side*nx,side*ny);mid=((a[0]+b[0])/2+outer[0]*width/2,(a[1]+b[1])/2+outer[1]*width/2)
 F=frame((*mid,0),outer);inside=frame((*mid,0),(-outer[0],-outer[1]))
 for i in range(bays+1):
  u=-L/2+i*L/bays;interior_lamp(inside,u)
 for i in range(bays):
  u=-L/2+(i+.5)*L/bays;half=(L/bays-1.08)/2
  local_solid(F,u,1.18,0,half*2,.26,.44,'Gallery red sandstone','gallery parapet sill')
  fbox(F,u,1.32,0,half*2+.10,.10,.51,'Granite foundation')
  for z,r in [(1.49,.020),(2.37,.035),(2.16,.018)]:beam(F(u-half,z,.06),F(u+half,z,.06),r,'Iron dark green',10)
  bars=max(3,round(half*2/.27))
  for k in range(bars+1):
   uu=u-half+k*2*half/bars
   path([F(uu,1.47+t*.87,.06+.19*sin(t*pi)) for t in [j/12 for j in range(13)]],.016,'Iron dark green',8)
   if k%2==0:
    for z,sign in [(2.23,1),(1.58,-1)]:
     for sgn in [-1,1]:
      path([F(uu+sgn*(.042+.067*(1-t/16))*cos(t*pi/8),z+sign*.077*sin(t*pi/8),.08) for t in range(25)],.011,'Iron dark green',6)
  # Separate slim proxy follows the visible guard envelope.
  origin=F(0,0);along=Vector(F(1,0))-Vector(origin)
  collision.append({'name':'gallery curved guard','type':'box','center':F(u,1.89,.10),'size':[half*2,.32,1.04],'rotation_z':math.atan2(along.y,along.x)})
# Historical broad views locate the raised roof behind the southern entrance,
# above its L-junction; it is not a triangular sheet sitting directly on the portal.
GROUP='SOP90_Gallery_raised_roof_block'
x,y=-50.5,37.5
box('',(x,y,7.30),(6.9,6.9,1.36),'Gallery red sandstone')
for z,w,h in [(6.71,7.4,.20),(7.90,7.43,.20),(8.08,7.75,.12)]:box('',(x,y,z),(w,w,h),'Gallery aged coping')
verts=[(x+dx,y+dy,8.18) for dx,dy in [(-4,-4),(4,-4),(4,4),(-4,4)]]+[(x+dx,y+dy,9.48) for dx,dy in [(-2.6,-2.6),(2.6,-2.6),(2.6,2.6),(-2.6,2.6)]]
add(verts,[(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,6,7)],'Gallery aged coping')
for normal in [(-1,0),(1,0),(0,-1),(0,1)]:
 F=frame((x+normal[0]*3.60,y+normal[1]*3.60,0),normal)
 for u in [-1.60,1.60]:
  arch_panel(F,u,8.17,.90,.86,.04,'Gallery cornice shadow')
  arc(F,u,8.58,.45,.16,.09,'Gallery red sandstone',32)
  fbox(F,u,8.21,.12,1.15,.10,.29,'Gallery aged coping')
 for u in [-3.1,-2.5,-1.9,-1.3,-.7,0,.7,1.3,1.9,2.5,3.1]:beam(F(u,8.24,.13),F(u*.72,9.46,-.98),.014,'Gallery cornice shadow',6)
print('SOP90 gallery real arch plates, interior cages, curved guards and raised roof integrated; dimensions pending calibration',flush=True)

# The 2025 primary front view shows right-arch steps and a transverse left ramp.
# Keep the slope and masonry thickness explicit estimates, pending matched views.
GROUP='SOP90_Gallery_offset_entry_ramp'
F=frame((-64,37.5,0),(-1,0))
a,b=-.325,4.9;dlo,dhi=1.30,2.80
rv=[F(u,z,d) for u,z,d in [(a,0,dlo),(b,0,dlo),(b,0,dhi),(a,0,dhi),(a,1.05,dlo),(b,.03,dlo),(b,.03,dhi),(a,1.05,dhi)]]
rf=[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]
add(rv,rf,'Granite foundation')
collision.append({'name':'gallery transverse entrance ramp','type':'mesh','vertices':rv,'faces':rf})
def slope_z(u):return 1.05-(u-a)/(b-a)*1.02
for d in [dlo+.08,dhi-.08]:
 path([F(u,slope_z(u)+.98,d) for u in [a,b]],.033,'Iron dark green',10)
 path([F(u,slope_z(u)+.21,d) for u in [a,b]],.018,'Iron dark green',8)
 for i in range(20):
  u=a+(b-a)*i/19
  beam(F(u,slope_z(u)+.035,d),F(u,slope_z(u)+.96,d),.022 if i%4==0 else .011,'Iron dark green',8)
# Retaining wall/guard in front of the unused left opening; no false level entry.
local_solid(F,1.90,.53,.18,2.78,1.06,.26,'Gallery red sandstone','gallery left entry retaining wall')
for z,r in [(1.32,.018),(2.05,.032)]:beam(F(.54,z,.36),F(3.26,z,.36),r,'Iron dark green',10)
for i in range(13):
 u=.54+2.72*i/12
 beam(F(u,1.10,.36),F(u,2.05,.36),.016,'Iron dark green',8)

# P3, 2025-05-29 15:18:55, ZOL photo 50479524: the northern raised block
# is a green metal clerestory with diamond lattice, NOT a red brick box.
# Distinct geometry from the still-unverified southern pavilion roof.
GROUP='SOP90_Gallery_north_lattice_clerestory'
x,y=-64.8,76.60;half=4.40
for normal in [(-1,0),(1,0),(0,-1),(0,1)]:
 F=frame((x+normal[0]*half,y+normal[1]*half,0),normal)
 for z,w,h,depth in [(6.67,9.28,.25,.48),(6.87,9.08,.13,.60),(7.03,8.96,.17,.38),(8.74,9.0,.18,.41),(8.94,9.45,.15,.63)]:
  fbox(F,0,z,0,w,h,depth,'Gallery aged coping')
 for u,w in [(-4.12,.56),(0,.40),(4.12,.56)]:
  fbox(F,u,7.88,0,w,1.64,.31,'Gallery aged coping')
  for du in [-w/2,w/2]:fbox(F,u+du,7.88,.175,.035,1.58,.035,'Gallery cornice shadow')
 for center in [-2.10,2.10]:
  hw,hh=1.66,.68;cz=7.88
  for u in [center-hw,center+hw]:fbox(F,u,cz,.18,.11,hh*2+.20,.15,'Gallery aged coping')
  for z in [cz-hh,cz+hh]:fbox(F,center,z,.18,hw*2+.20,.10,.15,'Gallery aged coping')
  # Lines are clipped to the actual rectangular aperture, with no solid backing.
  for slope in [-.60,.60]:
   for k in range(-15,16):
    c=k*.205;crossings=[]
    for xx in [-hw,hw]:
     zz=slope*xx+c
     if -hh<=zz<=hh:crossings.append((xx,zz))
    for zz in [-hh,hh]:
     xx=(zz-c)/slope
     if -hw<=xx<=hw:crossings.append((xx,zz))
    if len(crossings)>=2:
     a0,b0=crossings[0],crossings[-1]
     beam(F(center+a0[0],cz+a0[1],.02),F(center+b0[0],cz+b0[1],.02),.018,'Iron dark green',8)
# Four sloping roof fields meet an inset flat cap, as in the photograph.
v=[(x+dx,y+dy,9.05) for dx,dy in [(-4.58,-4.58),(4.58,-4.58),(4.58,4.58),(-4.58,4.58)]]+[(x+dx,y+dy,10.70) for dx,dy in [(-2.48,-2.48),(2.48,-2.48),(2.48,2.48),(-2.48,2.48)]]
add(v,[(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,6,7)],'Gallery aged coping')
for z,w,h in [(10.71,5.16,.13),(10.86,5.47,.14),(10.96,5.62,.07)]:box('',(x,y,z),(w,w,h),'Gallery aged coping')
for normal in [(-1,0),(1,0),(0,-1),(0,1)]:
 F=frame((x+normal[0]*4.13,y+normal[1]*4.13,0),normal)
 for u in [-2.16,2.16]:
  arch_panel(F,u,9.07,1.20,1.22,.01,'Gallery cornice shadow')
  arc(F,u,9.46,.60,.12,.08,'Carved terracotta',36)
  arc(F,u,9.46,.73,.12,.12,'Gallery aged coping',36)
  fbox(F,u,9.12,.14,1.58,.13,.26,'Gallery aged coping')
  add([F(u-.13,10.13,.12),F(u+.13,10.13,.12),F(u,10.34,.12)],[(0,1,2)],'Gallery aged coping')
 for j in range(23):
  u=-4.22+j*.384
  beam(F(u,9.10,.20),F(u*.56,10.70,-1.63),.012,'Gallery cornice shadow',6)
print('SOP90 northern lattice clerestory rebuilt from dated May 2025 photo; metric fit remains open',flush=True)

# June 28 2026 P5/P6: visible north-wing capitals have toothed brick corbels,
# and each solid arch fascia carries a projecting metal crest and fasteners.
GROUP='SOP90_Gallery_north_corbel_and_arch_crest'
for a,b,width,bays in runs[2:]:
 dx=b[0]-a[0];dy=b[1]-a[1];L=math.hypot(dx,dy);nx=-dy/L;ny=dx/L
 for side in [-1,1]:
  F=frame(((a[0]+b[0])/2+side*nx*width/2,(a[1]+b[1])/2+side*ny*width/2,0),(side*nx,side*ny))
  for i in range(bays+1):
   u=-L/2+i*L/bays
   fbox(F,u,5.84,.12,1.32,.24,1.30,'Gallery red sandstone')
   for k in range(6):
    fbox(F,u-.55+k*.22,5.64,.68,.115,.22,.14,'Gallery red sandstone')
    fbox(F,u-.55+k*.22,5.72,.60,.15,.14,.20,'Gallery red sandstone')
  for i in range(bays):
   u=-L/2+(i+.5)*L/bays;r=(L/bays-1.0)/2;z=4.08+r+.12
   fbox(F,u,z,.28,.24,.46,.20,'Gallery aged coping')
   fbox(F,u,z+.22,.30,.31,.09,.24,'Gallery aged coping')
   add([F(u-.12,z+.265,.42),F(u+.12,z+.265,.42),F(u,z+.38,.42)],[(0,1,2)],'Gallery aged coping')
   for j in range(1,12):
    aa=pi*j/12
    sphere(F(u+(r+.15)*cos(aa),4.08+(r+.15)*sin(aa),.235),.025,'Gallery aged coping',N=8,rings=4)
print('SOP90 north pier dentils and arch crests rebuilt from June 2026 photos',flush=True)
