"""Correct a verified cinema sign from the actual photograph crop; preserve all cameras."""
import bpy
from pathlib import Path
R=Path(__file__).resolve().parents[1]
for ob in bpy.data.objects:
 if ob.type=='FONT' and 'Cinema_photo_reference' in ob.name:ob.data.body='埃 曼 影 城'
bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(R/'Harbin_Sophia_Square.blend'))
