"""Analytic, original LED-cap PBR tile: no photographic pixels copied."""
from pathlib import Path
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parents[1];D=R/'assets/textures/sop90';D.mkdir(exist_ok=True)
y,x=np.mgrid[0:128,0:128]/128.;r=np.sqrt((x-.5)**2+(y-.5)**2);cap=np.maximum(0,1-(r/.28)**2)**.5
base=np.zeros((128,128,3))+[74,124,57]
base+=(cap[...,None])*[22,27,12]
base[(r>.275)&(r<.33)]=[43,85,33]
height=cap*.045;dy,dx=np.gradient(height,1/128,1/128);n=np.dstack([-dx,-dy,np.ones_like(dx)]);n/=np.linalg.norm(n,axis=2)[...,None]
rough=np.where(r<.275,88,148)
for suffix,data in [('diff',base),('rough',rough),('nor_gl',(n*.5+.5)*255)]:
 Image.fromarray(np.uint8(np.clip(data,0,255))).save(D/('green_sign_'+suffix+'.jpg'),quality=98,subsampling=0)
(D/'README.md').write_text('原创数学生成灯点纹理。每格代表约 15 mm 的估算灯点间距；未作为实测值验收。颜色、粗糙度、OpenGL 法线可同时供 Blender 与 glTF 使用。生成器：scripts/make_sign_surface.py。参考照片只用于观察点阵形态，没有嵌入照片像素。\n')
