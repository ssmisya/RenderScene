"""Make the active scene's render and image paths relative after a project move."""
from pathlib import Path
import bpy,json
root=Path(bpy.data.filepath).parent
for im in bpy.data.images:
 if im.source=='FILE':
  local=root/'assets'/'textures'/Path(im.filepath).name
  if local.exists():im.filepath='//assets/textures/'+local.name
bpy.context.scene.render.filepath='//renders/01_Hero.png'
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(root/'Harbin_Sophia_Square.blend'))
images=[{'name':i.name,'path':i.filepath,'packed':bool(i.packed_file)} for i in bpy.data.images if i.source=='FILE']
assert all(i['packed'] and i['path'].startswith('//assets/textures/') for i in images)
print('RELOCATED',str(root),'PACKED_IMAGES',len(images),'RENDER_PATH',bpy.context.scene.render.filepath,flush=True)
