"""Render and verify the V2.1 deliverables; never rebuild or overwrite the source scene."""
from pathlib import Path
import subprocess,hashlib,shutil,json
R=Path(__file__).resolve().parents[1]
B='/Applications/Blender.app/Contents/MacOS/Blender'
source=R/'Harbin_Sophia_Square.blend';before=hashlib.sha256(source.read_bytes()).hexdigest()
def run(name,args):
 print('START',name,flush=True)
 with (R/(name+'.log')).open('w') as log:subprocess.run([B,'-b',*args],cwd=R,stdout=log,stderr=subprocess.STDOUT,check=True)
 print('PASS',name,flush=True)
run('validation_v21',[str(source),'--python-exit-code','1','--python','scripts/validate_v21.py'])
run('render_v21_final',[str(source),'--python-exit-code','1','--python','scripts/render_v2.py','--','--mode','both','--view','all','--width','2400','--samples','192'])
run('export_v21',[str(source),'--python-exit-code','1','--python','scripts/export_game.py'])
run('game_validation_v21',['--python-exit-code','1','--python','scripts/verify_game.py'])
off=R/'verification/offline/Harbin_Sophia_Square.blend';assert not off.exists();shutil.copy2(source,off)
try:run('offline_v21',[str(off),'--python-exit-code','1','--python','scripts/verify_offline_v2.py'])
finally:off.unlink(missing_ok=True)
p=R/'verification/offline_validation.json';report=json.loads(p.read_text());report['revision']='2.1.0';report['temporary_blend_retained']=False;p.write_text(json.dumps(report,indent=2)+'\n')
assert hashlib.sha256(source.read_bytes()).hexdigest()==before,'Export or render changed source blend'
print('V21_DELIVERABLES_PASS',before,flush=True)
