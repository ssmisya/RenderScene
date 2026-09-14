"""New 100 curtain-wall structure from ZOL photo 50962488 (2026-06-28).
Observed stepped silhouette and staggered glazing replace transparent box/slabs.
Existing mapped footprint and total height retained; offsets remain estimates.
"""
ACTIVE='03_OSM_BUILDINGS'
for key in list(B):
 if key[1] in ['New_100_setback','V221_New100_roof_support']:del B[key]
for ob in list(sign_objects):
 if ob.name=='V221_Dashang_mounted':
  sign_objects.remove(ob);bpy.data.objects.remove(ob,do_unlink=True)
material('New100 curtain opaque backing',(.045,.085,.10),.58,.16,False)
material('New100 silver frame',(.32,.37,.36),.30,.72,False)
for i,col in enumerate([(.32,.48,.51),(.46,.60,.61),(.25,.40,.44),(.40,.54,.57),(.50,.62,.61)]):
 material('New100 architectural glass '+str(i),col,.20+.025*(i%3),.38,False)
GROUP='SOP90_New100_stepped_curtain_wall'
# Ground footprint follows the pre-existing map; upper volume steps back 8 m.
for xmin,xmax,ymin,ymax,zlo,zhi in [(-239,-127,15,89,27,32.4),(-239,-135,18,85,32.4,39)]:
 box('',((xmin+xmax)/2,(ymin+ymax)/2,(zlo+zhi)/2),(xmax-xmin,ymax-ymin,zhi-zlo),'New100 curtain opaque backing')
 for center,normal,length in [((xmax,(ymin+ymax)/2,0),(1,0),ymax-ymin),(((xmin+xmax)/2,ymin,0),(0,-1),xmax-xmin),(((xmin+xmax)/2,ymax,0),(0,1),xmax-xmin),((xmin,(ymin+ymax)/2,0),(-1,0),ymax-ymin)]:
  F=frame(center,normal);cols=max(1,round(length/1.45));step=length/cols
  for k in range(cols):
   u=-length/2+(k+.5)*step
   # Alternate vertical joints; clip panels at the physical floor/roof boundaries.
   bottom=zlo-(.74 if k%2 else 0);j=0
   while bottom<zhi:
    lo=max(bottom,zlo);hi=min(bottom+1.48,zhi)
    if hi-lo>.06:
     fbox(F,u,(lo+hi)/2,.12,step-.065,hi-lo-.045,.09,'New100 architectural glass '+str((k*7+j*3)%5))
     fbox(F,u,lo,.185,step,.027,.055,'New100 silver frame')
    bottom+=1.48;j+=1
   fbox(F,u-step/2,(zlo+zhi)/2,.18,.033,zhi-zlo,.05,'New100 silver frame')
  for z in [zlo,zhi]:fbox(F,0,z,.20,length+.18,.14,.36,'New100 silver frame')
GROUP='SOP90_New100_roof_letter_support'
F=frame((-134.75,45,0),(1,0))
for u in [-19,-12,-5,2,9,16,22]:
 beam(F(u,38.8,-.20),F(u,41.9,-.20),.045,'New100 silver frame',8)
 beam(F(u,39,-2.2),F(u,41.8,-.20),.045,'New100 silver frame',8)
for z in [39.7,41.5]:beam(F(-22,z,-.20),F(23,z,-.20),.04,'New100 silver frame',8)
street_text('大商集团 DASHANG GROUP',F(0,39.7,.03),2.0,(1,0),'Iron dark green','SOP90_Dashang_mounted')
print('SOP90 New100 opaque staggered curtain-wall panels and supported setback roof lettering rebuilt; dimensions unverified',flush=True)
