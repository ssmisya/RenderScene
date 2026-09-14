"""Fit a pinhole inspection camera to native lettering landmarks.
This is a diagnostic fit, not photographic acceptance or a dimensional survey.
No output pixels are warped, and errors are retained rather than overwritten.
"""
import json,math
from pathlib import Path
import numpy as np
import cv2
from scipy.optimize import least_squares
R=Path(__file__).resolve().parents[1];data=json.loads((R/'assets/geometry/daoli_sign_outlines.json').read_text())
W,H=data['source_resolution'];points=[]
for idx,item in enumerate(data['glyphs']):
 x,y,w,h=item['bounds_pixels'];height=1.65;width=height*w/h;u=4.9-idx*2.45
 pts=np.array([p for c in item['contours'] if not c['hole'] for p in c['points']])
 for name,i in [('top',pts[:,1].argmin()),('bottom',pts[:,1].argmax()),('left',pts[:,0].argmin()),('right',pts[:,0].argmax())]:
  a,b=pts[i];points.append({'feature':item['character']+'_'+name,'photo_pixels':[float(x+a*w),float(y+b*h)],'world_facade':[-u+(float(a)-.5)*width,4.88+(1-float(b))*height,.99]})
xyz=np.array([p['world_facade'] for p in points]);uv=np.array([p['photo_pixels'] for p in points])
# Alternating extrema are held out to expose a camera fit that only agrees at fitted points.
fit=np.array([i%4 in [0,2] for i in range(len(points))])
def project(q):
 f=np.exp(q[6]);K=np.array([[f,0,W/2],[0,f,H/2],[0,0,1.]])
 return cv2.projectPoints(xyz,q[:3],q[3:6],K,np.zeros(5))[0][:,0,:]
q=np.array([math.pi,0,0,0,1.7,11,math.log(W*24/36)])
res=least_squares(lambda a:(project(a)[fit]-uv[fit]).ravel(),q,bounds=([math.pi-.7,-.6,-.6,-4,-3,5,math.log(W*14/36)],[math.pi+.7,.6,.6,4,8,35,math.log(W*85/36)]),max_nfev=1500)
pred=project(res.x);errors=np.linalg.norm(pred-uv,axis=1)/math.hypot(W,H)
rot=cv2.Rodrigues(res.x[:3])[0];position=-rot.T@res.x[3:6]
for p,xy,error,isfit in zip(points,pred,errors,fit):p.update(render_prediction_pixels=xy.tolist(),diagonal_error=float(error),used_in_fit=bool(isfit))
out={'status':'DIAGNOSTIC_NOT_ACCEPTED','photo_id':data['source_photo_id'],'source_sha256':data['source_sha256'],'resolution':[W,H],'focal_pixels':float(np.exp(res.x[6])),'lens_mm_36mm_sensor':float(np.exp(res.x[6])*36/W),'camera_position_facade':position.tolist(),'world_to_opencv_rotation':rot.tolist(),'max_error_percent':float(errors.max()*100),'held_out_max_error_percent':float(errors[~fit].max()*100),'landmarks':points,'limitations':['Shape outlines were digitized from this same photograph; this is not independent multi-view validation.','Native glyph size/spacing are estimates; no facade curvature or lens distortion silently added.','A single front-facing fit cannot prove entry location or whole-building geometry.']}
(R/'verification/sop90/market_camera_fit.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print({k:out[k] for k in ['lens_mm_36mm_sensor','camera_position_facade','max_error_percent','held_out_max_error_percent']})
