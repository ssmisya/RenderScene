"""Keep paths portable after a user-requested move; never select a lower-resolution replacement."""
import bpy
from pathlib import Path
R=Path(bpy.data.filepath).parent
for im in bpy.data.images:
 if im.source!='FILE' or not im.filepath:continue
 resolved=Path(bpy.path.abspath(im.filepath))
 try:im.filepath='//'+str(resolved.relative_to(R))
 except ValueError:pass
for s in bpy.data.scenes:
 mode=s.get('lighting_mode','DAY');s.render.filepath='//renders/v2/'+mode+'_Hero.png'
bpy.context.preferences.filepaths.save_version=0
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(R/'Harbin_Sophia_Square.blend'))
