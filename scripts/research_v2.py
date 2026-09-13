import urllib.request,urllib.parse,json,concurrent.futures,time
from pathlib import Path
R=Path(__file__).resolve().parents[1];D=R/'references/v2';D.mkdir(exist_ok=True)
names=["Above St Sophia's entrance -1 (5636715679) (2).jpg","Above St Sophia's entrance -2 (5637292518).jpg","Brick detail (5637293596) (2).jpg","St Sophia's entrance (5637293096).jpg","Ogee & iron (5620661473).jpg","St Sophia -night (5791810665).jpg"]+[f'Cathedral of Holy Wisdom, Harbin {i}.jpg' for i in [1,2,3,4,8,9,10,11,12,13,14,15,17,18,19,20,21,22,23,24,25]]+['Harbin Saint Sophia Cathedral 2017 summer.jpg','Harbin Sophia Cathedral 2017 summer.jpg','East facade of St. Sophia Cathedral, Harbin (20230721093312).jpg','26156-Harbin (49026988213).jpg','Saint Sophia Cathedral, Harbin 06.01.2026.jpg']
def get(url):
 return urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'SophiaArchitectureStudy/2.0 (local educational visual reference)'}),timeout=35).read()
records=[]
for i in range(0,len(names),8):
 q={'action':'query','titles':'|'.join('File:'+n for n in names[i:i+8]),'prop':'imageinfo','iiprop':'url|extmetadata','iiurlwidth':1280,'format':'json'}
 try:
  data=json.loads(get('https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode(q)))
  for p in data['query']['pages'].values():
   if 'imageinfo' in p:records.append({'title':p['title'],**p['imageinfo'][0]})
 except Exception as e:print(e,flush=True)
(D/'sources.json').write_text(json.dumps(records,ensure_ascii=False,indent=2))
def dl(pair):
 i,r=pair;r['local']=f'photo_{i:02d}.jpg';p=D/r['local']
 try:
  if not p.exists():p.write_bytes(get(r.get('thumburl',r['url']).replace('thumb.wikimedia.org','upload.wikimedia.org')))
  return f'{i:02d} OK {r["title"]}'
 except Exception as e:return f'{i:02d} FAIL {e}'
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
 for s in ex.map(dl,enumerate(records)):print(s,flush=True)
(D/'sources.json').write_text(json.dumps(records,ensure_ascii=False,indent=2))
from PIL import Image,ImageOps,ImageDraw
for part in range((len(records)+7)//8):
 canvas=Image.new('RGB',(1600,1000),'#ddd');draw=ImageDraw.Draw(canvas)
 for j,r in enumerate(records[part*8:part*8+8]):
  try:im=Image.open(D/r['local']);im.thumbnail((390,435));x=(j%4)*400;y=(j//4)*500;canvas.paste(im,(x+(400-im.width)//2,y));draw.text((x+5,y+445),r['local']+' '+r['title'][5:35],fill='black')
  except:pass
 canvas.save(D/f'contact_{part}.jpg')
