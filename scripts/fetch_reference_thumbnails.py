from pathlib import Path
import hashlib,urllib.parse,subprocess,json,time
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[1];D=R/'references/v2';ns={"__file__":str(R/"scripts/research_v2.py")};exec((R/'scripts/research_v2.py').read_text().split('def get(url):')[0],ns);names=ns['names'];records=[]
for i,name in enumerate(names):
 f=name.replace(' ','_');h=hashlib.md5(f.encode()).hexdigest();url='https://upload.wikimedia.org/wikipedia/commons/thumb/'+h[0]+'/'+h[:2]+'/'+urllib.parse.quote(f)+'/960px-'+urllib.parse.quote(f)
 p=D/f'ref_{i:02d}.jpg'
 if not p.exists():
  result=subprocess.run(['curl','-L','-f','--max-time','18','-A','Mozilla/5.0',url,'-o',str(p)],capture_output=True)
 try:
  im=Image.open(p);im.verify();print(i,'OK',name,flush=True);records.append({'index':i,'name':name,'file':p.name,'url':url,'source':'https://commons.wikimedia.org/wiki/File:'+urllib.parse.quote(f),'use':'visual modeling reference only, not used as textures'})
 except:print(i,'unavailable',flush=True)
 time.sleep(.4)
(D/'reference_index.json').write_text(json.dumps(records,ensure_ascii=False,indent=2))
for part in range((len(names)+7)//8):
 canvas=Image.new('RGB',(1600,1000),'#ddd');draw=ImageDraw.Draw(canvas)
 for j in range(8):
  i=part*8+j
  if i>=len(names):break
  try:
   im=Image.open(D/f'ref_{i:02d}.jpg');im.thumbnail((395,442));x=(j%4)*400;y=(j//4)*500;canvas.paste(im,(x+(400-im.width)//2,y));draw.text((x+5,y+446),f'{i:02d} '+names[i][:37],fill='black')
  except:pass
 canvas.save(D/f'sheet_{part}.jpg')
