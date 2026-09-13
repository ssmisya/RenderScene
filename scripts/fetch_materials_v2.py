from pathlib import Path
import urllib.request,concurrent.futures
R=Path(__file__).resolve().parents[1];D=R/'assets/textures/v2';D.mkdir(exist_ok=True)
jobs=[]
for a,p in [('red_brick_03','brick'),('pavement_04','paving')]:
 for s in ['diff','rough','nor_gl','disp']:
  jobs.append((f'https://dl.polyhaven.org/file/ph-assets/Textures/jpg/4k/{a}/{a}_{s}_4k.jpg',D/f'{p}_{s}.jpg'))
def f(j):
 try:
  if not j[1].exists():urllib.request.urlretrieve(j[0],j[1])
  return str(j[1].name)+' '+str(j[1].stat().st_size)
 except Exception as e:return str(e)
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
 for x in ex.map(f,jobs):print(x,flush=True)
