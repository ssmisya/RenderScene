"""Build macOS release with repository-local official Godot/template, no global install."""
from pathlib import Path
import subprocess,json,shutil,hashlib
import argparse
from release_gate import require_release
args_parser=argparse.ArgumentParser();args_parser.add_argument('--preview',action='store_true',help='Local QA only; writes builds/review, never the deliverable package')
args=args_parser.parse_args()
if not args.preview:require_release()
R=Path(__file__).resolve().parents[1];D=R/'demo';exe=R/'.tools/godot/Godot.app/Contents/MacOS/Godot';template=R/'.tools/godot/macos.zip'
assert exe.is_file() and template.is_file(),'Run scripts/setup_godot.py first.'
for source,target in [('game/Sophia_Square.glb','assets/square.glb'),('game/Sophia_Collision.glb','assets/collision.glb'),('game/lighting_v2.json','assets/lighting.json'),('assets/textures/sky.hdr','assets/day_sky.hdr')]:
 if not (D/target).exists() or hashlib.sha256((R/source).read_bytes()).digest()!=hashlib.sha256((D/target).read_bytes()).digest():shutil.copy2(R/source,D/target)
manifest={p:hashlib.sha256((R/p).read_bytes()).hexdigest() for p in ['Harbin_Sophia_Square.blend','game/Sophia_Square.glb','game/Sophia_Collision.glb']}
(D/'assets/manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
preset=D/'export_presets.cfg';original=preset.read_text();text=original.replace('"../.tools/godot/macos.zip"',json.dumps(str(template),ensure_ascii=False))
output=R/'builds'/'review' if args.preview else R/'builds'
output.mkdir(parents=True,exist_ok=True)
subprocess.run([str(exe),'--headless','--editor','--path',str(D),'--import'],cwd=R,check=True)
try:
 preset.write_text(text)
 subprocess.run([str(exe),'--headless','--path',str(D),'--export-release','macOS',str(output/'SophiaWalk.zip')],cwd=R,check=True)
finally:preset.write_text(original)
subprocess.run(['ditto','-x','-k',str(output/'SophiaWalk.zip'),str(output)],cwd=R,check=True)
print('LOCAL_REVIEW_ONLY_NOT_ACCEPTED' if args.preview else 'MACOS_DEMO_BUILT',flush=True)
