"""Digitize visible sign silhouettes as editable geometry, never photo textures.

The public reporter original is kept locally. Extracted silhouettes still need
camera/plane calibration: they are explicitly NOT accepted real dimensions.
Run with .tools/sop90env/bin/python.
"""
from pathlib import Path
import json,hashlib
import cv2
import numpy as np
R=Path(__file__).resolve().parents[1]
source=R/'references/sop_reaudit/local/market_primary_20250621.jpg'
im=cv2.imread(str(source));hsv=cv2.cvtColor(im,cv2.COLOR_BGR2HSV)
green=cv2.inRange(hsv,np.array([34,45,45]),np.array([85,255,240]))
green[820:]=0;green[:,:500]=0
_,labels,stats,_=cv2.connectedComponentsWithStats(green)
components=sorted([(i,row) for i,row in enumerate(stats) if 3000<row[4]<1000000],key=lambda t:t[1][0])
assert len(components)==5
def outlines(mask,bounds):
 x,y,w,h=map(int,bounds)
 contours,tree=cv2.findContours(mask,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)
 result=[]
 for i,c in enumerate(contours):
  area=cv2.contourArea(c)
  if area<70:continue # LED pinholes are surface detail, not holes through the glyph.
  points=cv2.approxPolyDP(c,.65,True).reshape(-1,2)
  result.append({'hole':int(tree[0,i,3])>=0,'pixel_area':area,'points':[[round((float(a)-x)/w,6),round((float(b)-y)/h,6)] for a,b in points]})
 return result
glyphs=[]
for character,(label,stat) in zip('道里菜市场',components):
 mask=np.uint8(labels==label)*255
 # Close scan-sized dot gaps; preserve the real larger counters of the character.
 mask=cv2.morphologyEx(mask,cv2.MORPH_CLOSE,np.ones((3,3),np.uint8))
 glyphs.append({'character':character,'bounds_pixels':list(map(int,stat[:4])),'contours':outlines(mask,stat[:4])})
gold=cv2.inRange(hsv,np.array([10,70,50]),np.array([36,255,255]))
gold[:,550:]=0;gold[:260]=0;gold[880:]=0
_,gl,gs,_=cv2.connectedComponentsWithStats(gold)
idx=next(i for i,row in enumerate(gs) if 50000<row[4]<200000)
mask=cv2.morphologyEx(np.uint8(gl==idx)*255,cv2.MORPH_CLOSE,np.ones((3,3),np.uint8))
logo={'bounds_pixels':list(map(int,gs[idx,:4])),'contours':outlines(mask,gs[idx,:4])}
result={'status':'DIGITIZED_VISIBLE_SILHOUETTES_NOT_CAMERA_CALIBRATED','source_photo_id':'market_front_20250621','source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'source_resolution':[im.shape[1],im.shape[0]],'method':'HSV segmentation; outer contour and real counters; sub-pixel-scale polygon approximation. No bitmap from the reference embedded in the model.','glyphs':glyphs,'logo':logo}
dest=R/'assets/geometry/daoli_sign_outlines.json';dest.parent.mkdir(exist_ok=True);dest.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
v=R/'verification/sop90';v.mkdir(exist_ok=True)
parts=['<svg xmlns="http://www.w3.org/2000/svg" width="1500" height="330" viewBox="0 0 1500 330"><rect width="1500" height="330" fill="#eeeeea"/>']
for idx,item in enumerate([logo]+glyphs):
 paths=[]
 for c in item['contours']:
  paths.append('M'+' L'.join(f'{idx*245+20+x*205:.3f},{20+y*255:.3f}' for x,y in c['points'])+' Z')
 parts.append('<path fill="'+('#b39230' if idx==0 else '#286731')+'" fill-rule="evenodd" d="'+' '.join(paths)+'"/>')
parts.append('</svg>');(v/'sign_digitized.svg').write_text(''.join(parts))
print('Digitized 5 glyphs and gold sign; no photographic acceptance asserted.')
