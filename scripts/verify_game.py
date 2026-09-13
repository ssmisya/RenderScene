import bpy,json,struct
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
reports={}
for file in ['Sophia_Square.glb','Sophia_Collision.glb']:
 path=ROOT/'game'/file
 with open(path,'rb') as f:
  magic,version,total=struct.unpack('<4sII',f.read(12));length,typ=struct.unpack('<II',f.read(8));j=json.loads(f.read(length))
 report={'size_bytes':path.stat().st_size,'header_valid':magic==b'glTF' and version==2 and total==path.stat().st_size,'meshes':len(j.get('meshes',[])),'materials':len(j.get('materials',[])),'images':len(j.get('images',[])),'external_uris':[v['uri'] for key in ['images','buffers'] for v in j.get(key,[]) if 'uri' in v and not v['uri'].startswith('data:')]}
 bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(path))
 report['pigeon_meshes']=[ob.name for ob in bpy.context.scene.objects if 'pigeon' in ob.name.lower()];report['revision']=(ROOT/'VERSION').read_text().strip()
 report['imported_meshes']=sum(ob.type=='MESH' for ob in bpy.context.scene.objects);report['loaded_images']=[{'name':im.name,'size':list(im.size)} for im in bpy.data.images if im.type=='IMAGE'];report['empty_meshes']=[o.name for o in bpy.context.scene.objects if o.type=='MESH' and not len(o.data.vertices)]
 reports[file]=report
json.dump(reports,open(ROOT/'game/export_validation.json','w'),indent=2)
print('GLB_IMPORT_VALIDATION',reports,flush=True)
assert all(v['header_valid'] and not v['external_uris'] and not v['empty_meshes'] and not v['pigeon_meshes'] and v['imported_meshes']>0 for v in reports.values())
