"""Bind actual integrated assets and fresh local-app QA to the still-open audit."""
from pathlib import Path
import json,hashlib,shutil,html,os,subprocess
R=Path(__file__).resolve().parents[1];V=R/'verification/sop_reaudit';D=R/'references/sop_reaudit'
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
 return h.hexdigest()
def bound(p):return {'file':str(p.relative_to(R)),'sha256':sha(p)}
def write(p,j):p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n')
assets={p:sha(R/p) for p in ['Harbin_Sophia_Square.blend','game/Sophia_Square.glb','game/Sophia_Collision.glb']}
qa=R/'builds/review/captures/runtime_validation.json';runtime=json.loads(qa.read_text())
assert runtime['assets']==assets and runtime['all_checks_pass'] and runtime['exported_application']
assert runtime['checks'] and all(v is True for v in runtime['checks'].values())
native=V/'native_rework_validation.json';n=json.loads(native.read_text())
assert n['source_scene_sha256']==assets['Harbin_Sophia_Square.blend'] and all(n['checks'].values())
shutil.copy2(qa,V/'runtime_rework_validation.json')
images=[]
for p in sorted(qa.parent.glob('*.png')):
 target=V/('game_rework_'+p.name);shutil.copy2(p,target);images.append(target)
a=json.loads((D/'audit.json').read_text());a['assets']=assets
a['runtime_report']=bound(V/'runtime_rework_validation.json');a['blender_report']=bound(native)
changes={
 'G01':('UNVERIFIED','主工程和 GLB 已补两个端头的实体中柱与左右双拱，独立游戏验证中柱阻挡及拱洞通行。','SOP_Gallery_terminal_twin_arches','按真实机位标定开间、拱高与柱宽；不能仅凭存在中柱验收。'),
 'G02':('MISMATCH','端面重做五层深檐口、阴缝、齿饰和小山花，截面仍未匹配实拍。','SOP_Gallery_layered_cornice_and_hip_roof','核实檐口层数、挑出距离、山花大小。'),
 'G03':('MISMATCH','增加封闭坡屋顶和圆拱小窗；新增2019侧照显示高出低檐的上层屋顶体块，位置与高差尚未重建准确。','SOP_Gallery_layered_cornice_and_hip_roof','用近期高位/侧面照片确认高屋顶位于哪一段，再修复体块与后部接合。'),
 'G04':('MISMATCH','端头柱面增加凸出分段、窄条与无灰缝扫描面材质；侧翼柱仍有通用铺砖，不能判全体通过。','SOP_Gallery_terminal_twin_arches','核实并统一各类柱的实际砌筑和构件截面。'),
 'G05':('UNVERIFIED','端头增加双灯附墙灯具、托臂、框条和夜间灯罩/光源；数量及精确形态待标定。','SOP_Gallery_terminal_lanterns','找近景核对灯臂曲线、灯罩造型、数量及位置。'),
 'M04':('MISMATCH','原等宽五大门组改为较窄的框扇、横楣、踢板和把手；当前六扇为遮挡条件下的估计，非确认门数。','SOP_Market_recessed_entry_and_shops','补无遮挡门组近照，核实各扇边界、开启方向与宽高。'),
 'M05':('MISMATCH','拆分门厅与右侧店面，增加照片可见寄存价签、挂卡、金属挂钩和小货架；商品与未读清店招仍为简化表达。','SOP_Market_recessed_entry_and_shops','继续逐铺核对开间、招牌、陈列，禁止把通用物件当真实商铺完成。'),
 'M06':('UNVERIFIED','补雨棚分段管边、接箍、底板纵横拼缝、支撑杆和固定底板；边缘曲线和间距仍为估计。','SOP_Market_canopy_seams_and_soffit','按原照机位校准雨棚弧度、接缝位置和挂点。')}
for item in a['items']:
 if item['id'] in changes:
  state,current,objects,next_action=changes[item['id']]
  item.update(status=state,current_model=current,implementation_objects=objects,next_action=next_action)
  item['rework_evidence']=['renders/sop_rework/cameras.json',str(native.relative_to(R)),str((V/'runtime_rework_validation.json').relative_to(R))]
  item.pop('candidate_evidence',None);item.pop('candidate_status',None)
 if item['id']=='G03' and 'gallery_2019' not in item['photo_ids']:item['photo_ids'].append('gallery_2019')
a['time_conflicts'][0]['additional_evidence']='2024-12-04 哈尔滨日报报道明确记载当年更换外立面电子屏，但不能由此确认每张游客照的拍摄日期。'
a['time_conflicts'][0]['source_url']='https://www.hrbtv.net/folder137/2024-12-04/977093.html'
write(D/'audit.json',a)
sources=json.loads((D/'sources.json').read_text())
count=len(runtime['checks'])
body=f'''# 主工程返工已整合，实景 SOP 仍未通过

更新：2026-09-14。工作分支 `codex/sop-reaudit-v2.2.1`。本页替代此前“仅独立中柱候选”的进度说明。

## 本机查看

- 主文件：[Harbin_Sophia_Square.blend](../../Harbin_Sophia_Square.blend)，DAY / NIGHT 场景可 F12 渲染。
- 双击根目录 [启动返工预览.command](../../启动返工预览.command)。应用位于 `builds/review/索菲亚广场 · 持枪漫游.app`。
- [照片与前后画面对照](复核.html) / [本轮昼夜渲染](../../renders/sop_rework/)。
- 旧 `启动游戏Demo.command`、V2.2.1 ZIP 和历史标签保持原样，不包含本轮新模型。

## 已实施

砖廊：端头中柱、双拱与扇形铁件；分层檐口、小山花、封闭坡顶；柱面分段及扫描颜色/粗糙度/法线材质；附墙灯的灯臂、灯罩与昼夜开关。

市场：较窄门框、横楣、把手和踢板；分开的店面、寄存价签、挂钩货架；雨棚底板网格、管段接箍、支撑杆。小倒角在游戏导出中保留。门数、商品及未读清店招仍有估计和简化。

## SOP 每步状态

| 步骤 | 当前结果 |
|---|---|
| 范围/时间 | 保留原两处完整外部范围；2025常设结构目标，显示屏时序未闭合。 |
| 近期原照 | 共筛查 {len(sources)} 张候选；有效近期目标外景仍仅2张，未达10张/3独立作者及覆盖要求。 |
| 差异表 | 21项继续开放，8项已有实际建模修订；无项目伪标MATCHED。 |
| 返工 | 主工程、GLB、碰撞和本地应用已整合；其余差异未解决。 |
| 实拍机位比对 | 未完成；本页是检查视图，无6点相机标定，不宣称1%精度。 |
| 技术验证 | 当前资产的独立Mac应用 {count}/{count} 项通过；新中柱碰撞、拱洞通行、昼夜均实际测试。原生检查9项通过，GLB实际重导入通过。 |
| 发布验收 | NOT_ACCEPTED；无新正式包/标签。预览只供本机检查。 |

## 仍然不符合的关键位置

砖廊高低屋顶的关系、侧翼柱、台阶与坡道；市场圆角入口、定制字形、实际门数/商铺、窗带面板数量、建筑高度及夜景；两处街道设施的准确位置。新增2019侧照帮助发现屋顶问题，但不能计入近期照片。

新增游客相册25张主要为教堂、钢塔廊及中央大街；报道照片为市场内部，均未用来凑本批外景数量。HEIC原件本地保留，以macOS转换预览，没有更改几何或伪造日期。所有未经授权的参考原图均不随Git分发。

## 重建/检查

```sh
/Applications/Blender.app/Contents/MacOS/Blender -b --python scripts/build_scene.py
/Applications/Blender.app/Contents/MacOS/Blender -b Harbin_Sophia_Square.blend --python scripts/export_game.py
python3 scripts/build_demo.py --preview
"builds/review/索菲亚广场 · 持枪漫游.app/Contents/MacOS/索菲亚广场 · 持枪漫游" -- --qa
python3 scripts/validate_references.py --strict  # 当前退出2，未通过
```

技术报告：[原生场景](native_rework_validation.json)、[实际应用](runtime_rework_validation.json)、[导出重导入](../../game/export_validation.json)。旧 `candidate_manifest.json` 仅记录上轮独立候选，不代表当前主工程。最新绑定见 [integrated_rework_manifest.json](integrated_rework_manifest.json)。
'''
(V/'README.md').write_text(body)
esc=html.escape
def url(p):return esc(os.path.relpath(R/p,V),quote=True)
parts=['<!doctype html><html lang="zh-CN"><meta charset="utf-8"><title>实景返工复核</title><style>body{background:#172027;color:#e4e9ed;font:16px/1.6 sans-serif;margin:30px}a{color:#84cfff}.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}figure{margin:0;background:#25323b;padding:10px}img{width:100%;height:290px;object-fit:contain}article{border-top:1px solid #53616a;padding:12px}.photos{display:grid;grid-template-columns:repeat(5,1fr);gap:10px}.photos img{height:160px}small{font-size:12px}h1{color:#ffbc79}</style><h1>已整合返工 · NOT_ACCEPTED</h1><p>75张候选，2张近期有效目标外景。无同机位标定、无100%还原结论。以下游戏图来自独立Mac应用，Blender图为实际渲染。</p>']
for title,rows in [('砖廊',[
 ('references/v2_2/brick_gallery_2025.jpg','2025实拍：端头双拱、柱体与檐口'),
 ('renders/v2_2_1/game_gallery_front.png','旧版游戏检查机位'),
 ('verification/sop_reaudit/game_rework_gallery_front.png','本轮游戏相同检查机位')]),('菜市场',[
 ('references/v2_2_1/local/market_front_20250621.jpg','2025-06-21实拍：门组、价签、雨棚'),
 ('renders/v2_2_1/game_market_entry.png','旧版游戏检查机位'),
 ('verification/sop_reaudit/game_rework_market_entry.png','本轮游戏相同检查机位')])]:
 parts.extend(['<h2>'+title+'</h2><div class="grid">'])
 for p,caption in rows:parts.append(f'<figure><img src="{url(p)}"><figcaption>{esc(caption)}</figcaption></figure>')
 parts.append('</div>')
parts.append('<h2>本轮Blender昼夜</h2><div class="grid">')
for mode in ['DAY','NIGHT']:
 for obj in ['gallery','market']:
  p=f'renders/sop_rework/{mode}_{obj}.png';parts.append(f'<figure><img src="{url(p)}"><figcaption>{mode} {obj}；未匹配实拍机位</figcaption></figure>')
parts.append('</div><h2>21项差异</h2>')
for i in a['items']:parts.append(f'<article><b>{esc(i["id"]+" / "+i["status"])}</b><p>{esc(i["current_model"])}</p><p>下一步：{esc(i["next_action"])}</p></article>')
parts.append('<h2>全部候选及排除依据</h2><div class="photos">')
for s in sources:parts.append(f'<figure><img loading="lazy" src="{url(s["file"])}"><small>{esc(s["id"])}<br>{esc(s["observations"])}</small><br><a href="{esc(s["source_url"],quote=True)}">来源</a></figure>')
parts.append('</div></html>');(V/'复核.html').write_text(''.join(parts))
files=[native,V/'runtime_rework_validation.json',R/'renders/sop_rework/cameras.json']+images+list((R/'renders/sop_rework').glob('*.png'))
write(V/'integrated_rework_manifest.json',{'status':'REWORK_REQUIRED','photo_acceptance':False,'assets':assets,'application':bound(R/'builds/review/索菲亚广场 · 持枪漫游.app/Contents/MacOS/索菲亚广场 · 持枪漫游'),'local_preview_zip':bound(R/'builds/review/SophiaWalk.zip'),'files':[bound(p) for p in files]})
checks={}
for name,cmd,expected in [('reference_strict',['python3','scripts/validate_references.py','--strict'],2),('release_gate',['python3','scripts/release_gate.py'],1),('default_packaging',['python3','scripts/build_demo.py'],1),('regressions',['python3','-m','unittest','discover','-s','tests','-v'],0)]:
 cp=subprocess.run(cmd,cwd=R,capture_output=True,text=True)
 checks[name]={'command':cmd,'exit_code':cp.returncode,'expected_exit_code':expected,'passed':cp.returncode==expected,'output_tail':(cp.stdout+cp.stderr)[-2000:]}
 assert cp.returncode==expected,(name,cp.stdout,cp.stderr)
write(V/'gate_tests.json',{'meaning':'Gate behavior, not scene acceptance','all_checks_pass':True,'checks':checks})
print('Integrated rework report written; photo acceptance remains blocked.')
