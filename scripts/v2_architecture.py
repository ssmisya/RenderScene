"""Photographic portal reconstruction helpers, called before cathedral construction."""
def radial_arch(F,u,sp,r,width,d,depth=.18,full=pi):
 # Real wedge-shaped voussoirs and recessed mortar, with radial rather than horizontal joints.
 arc(F,u,sp,r,width,d-.16,'Old lime mortar',max(24,int(r*24)),0,full)
 count=max(12,int(full*(r+width*.5)/.115));gap=.009/max(r,.1)
 for i in range(count):
  a=i*full/count+gap/2;b=(i+1)*full/count-gap/2
  vs=[F(u+rr*cos(ang),sp+rr*sin(ang),dd) for dd in [d,d+depth] for rr,ang in [(r,a),(r,b),(r+width,b),(r+width,a)]]
  add(vs,[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],'Arch fired brick %02d'%random.randrange(14),uv=[(0,0),(0,1),(1,1),(1,0)]*2)
def panel_frame(F,u,z,w,h,d):
 fbox(F,u,z,d,w,h,.052,'Door carved relief')
 fbox(F,u,z,d+.037,w-.12,h-.12,.036,'Door black lacquer')
 for du in [-w/2,w/2]:fbox(F,u+du,z,d+.052,.047,h+.035,.035,'Door carved relief')
 for dz in [-h/2,h/2]:fbox(F,u,z+dz,d+.052,w+.035,.047,.035,'Door carved relief')
def portal(F,w=3.2,h=5.5):
 s=w/3.5
 # Door head is a paired round arch under a brick tympanum, not a tall single wooden arch.
 sp=3.55*s;inner=1.91*s;outer=4.62*s;bottom=.28*s
 arch_panel(F,0,bottom,inner*2,sp+inner-bottom,.11,'Historic red brick • CC0 scan')
 leafw=1.58*s;leafsp=3.38*s
 for sign in [-1,1]:
  u=sign*.83*s
  arch_panel(F,u,bottom,leafw+.10*s,leafsp+.85*s-bottom,.16,'Window shadow')
  arch_panel(F,u,bottom,leafw,leafsp+leafw/2-bottom,.22,'Door black lacquer')
  arch_panel(F,u,leafsp-.035*s,leafw-.22*s,(leafw-.22*s)/2+.035*s,.245,'Door smoked glass')
  arc(F,u,leafsp,leafw/2-.10*s,.055*s,.25,'Door carved relief',36)
  panel_frame(F,u,1.94*s,1.23*s,1.88*s,.28)
  panel_frame(F,u,.65*s,1.23*s,.27*s,.28)
  panel_frame(F,u,3.05*s,1.23*s,.23*s,.28)
  # Raised Orthodox cross and fine carved rays on each main panel.
  fbox(F,u,1.99*s,.37,.065*s,1.36*s,.025,'Door carved relief')
  for zz,ww in [(2.35,.75),(2.57,.40)]:fbox(F,u,zz*s,.37,ww*s,.07*s,.026,'Door carved relief')
  beam(F(u-.24*s,1.49*s,.385),F(u+.24*s,1.34*s,.385),.025*s,'Door carved relief',6)
  for j in range(24):
   a=j*2*pi/24;beam(F(u+.15*s*cos(a),2.34*s+.15*s*sin(a),.385),F(u+.34*s*cos(a),2.34*s+.34*s*sin(a),.385),.009*s,'Door carved relief',4)
  for j in range(10):
   x=u+(-.50+j*.11)*s;path([F(x,3.04*s,.375),F(x+.045*s,3.10*s,.375),F(x+.09*s,3.04*s,.375)],.010*s,'Door carved relief',4)
  fbox(F,sign*.085*s,1.80*s,.40,.038*s,.39*s,.045,'Old brass hardware')
 # Central cusp and round brick medallion in tympanum.
 fbox(F,0,3.39*s,.34,.22*s,.22*s,.20,'Door carved relief')
 radial_arch(F,0,4.53*s,.37*s,.13*s,.21,depth=.08,full=2*pi)
 # Unequal layered profiles visible in close-up photographs.
 rings=[(1.93,.27,.36),(2.21,.12,.47),(2.35,.23,.48),(2.61,.095,.59),(2.72,.34,.57),(3.08,.10,.68),(3.20,.28,.64),(3.50,.11,.75),(3.63,.47,.70),(4.12,.12,.84),(4.25,.37,.80)]
 for r,ww,dd in rings:
  radial_arch(F,0,sp,r*s,ww*s,dd*s,depth=.13*s)
 # Deep dentil rings; each brick rotated to the arch tangent, including side faces.
 for r,dd,num in [(2.40,.76,35),(3.93,1.0,47)]:
  for i in range(num):
   a=(i+.5)*pi/num;dr=.20*s;da=.075/max(r,.1)
   vs=[F(rr*cos(aa),sp+rr*sin(aa),dep) for dep in [(dd-.13)*s,dd*s] for rr,aa in [((r-.10)*s,a-da),((r-.10)*s,a+da),((r+.10)*s,a+da),((r+.10)*s,a-da)]]
   add(vs,[(0,1,2,3),(4,7,6,5),(0,4,5,1),(1,5,6,2),(2,6,7,3)],'Arch fired brick %02d'%random.randrange(14))
 # Broad stepped jambs, corbels and masonry courses.
 for sign in [-1,1]:
  for k in range(7):
   u=sign*(2.06+k*.36)*s;wid=.28*s;d=(.33+k*.07)*s
   fbox(F,u,sp/2+.15*s,d,wid,sp-.28*s,.24*s,'Carved terracotta')
   for j in range(int(sp/(.19*s))):
    z=.3*s+j*.19*s
    fbox(F,u,z,d+.14*s,wid+.08*s,.06*s,.11*s,'Arch fired brick %02d'%((j+k)%14))
   for zz in [.35,1.16,2.35,3.30]:fbox(F,u,zz*s,d+.15*s,wid+.19*s,.15*s,.23*s,'Carved terracotta')
  # Outer capital's small blind semi-arch and raised point.
  center=sign*4.36*s;radial_arch(F,center,sp+.08*s,.53*s,.16*s,.92*s,.09*s)
  radial_arch(F,center,sp+.08*s,.73*s,.10*s,.93*s,.10*s)
  path([F(center-.20*s,sp+.82*s,1.02*s),F(center,sp+1.12*s,1.02*s),F(center+.20*s,sp+.82*s,1.02*s)],.032*s,'Iron dark green',6)
  fbox(F,center,sp-.04*s,.86*s,1.7*s,.18*s,.53*s,'Carved terracotta')
 # Thin green metal weather cap follows the main outer archivolt.
 pts=[F((outer+.08*s)*cos(i*pi/90),sp+(outer+.08*s)*sin(i*pi/90),.91*s) for i in range(91)]
 path(pts,.029*s,'Iron dark green',6)
# Overwrite windows only when the requested surface is a blind brick niche.
original_window=window
def window(F,u,z,w,h,ornate=True,glass='Old glass'):
 if glass!='Historic red brick • CC0 scan':return original_window(F,u,z,w,h,ornate,glass)
 arch_panel(F,u,z,w+.16,h+.08,.04,'Recessed soot');arch_panel(F,u,z+.1,w-.12,h-.20,.09,glass)
 radial_arch(F,u,z+h-w/2,w/2+.02,.13,.16,.12)
 for sign in [-1,1]:
  fbox(F,u+sign*(w/2+.13),z+(h-w/2)/2,.19,.15,h-w/2,.20,'Carved terracotta')
  for zz in [z+.3+i*.47 for i in range(int((h-w/2)/.47))]:fbox(F,u+sign*(w/2+.15),zz,.29,.23,.10,.17,'Carved terracotta')
 fbox(F,u,z-.07,.29,w+.45,.19,.37,'Carved terracotta')
