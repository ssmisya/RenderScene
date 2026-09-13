"""Original synthesized demo foley, no downloaded third-party recordings."""
from pathlib import Path
import math,random,wave,struct
R=Path(__file__).resolve().parents[1]/'demo/audio';R.mkdir(exist_ok=True);sr=22050
rng=random.Random(2202)
def write(name,dur,fn):
 with wave.open(str(R/(name+'.wav')),'wb') as w:
  w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr)
  w.writeframes(b''.join(struct.pack('<h',int(max(-1,min(1,fn(i/sr)))*32767)) for i in range(int(dur*sr))))
write('shot',.8,lambda t:(rng.uniform(-1,1)*math.exp(-t*30)+.3*math.sin(t*math.tau*83)*math.exp(-t*13)+rng.uniform(-.12,.12)*math.exp(-t*4))*.7)
write('step',.26,lambda t:(rng.uniform(-1,1)*.45+math.sin(t*math.tau*110)*.35)*math.exp(-t*24)*(1-math.exp(-t*180)))
def reload(t):
 return sum((rng.uniform(-.5,.5)+.15*math.sin(t*math.tau*450))*math.exp(-(t-s)*70) for s in [0,.12,.65,1.1,1.38] if t>=s)
write('reload',1.65,reload)
last=0
def ambient(t):
 global last
 last=last*.992+rng.uniform(-1,1)*.008
 return last*.65+.01*math.sin(t*math.tau*85)*(1+math.sin(t*.4))
write('ambience',20,ambient)
