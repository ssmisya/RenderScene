"""Bind current technical results and real open defects without granting photo credit."""
from pathlib import Path
import json,hashlib,shutil,html,os
from validate_references import inspect
from sop90_progress import progress
R=Path(__file__).resolve().parents[1];V=R/'verification/sop90';A=R/'references/sop_reaudit'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def bound(p):return {'file':str(p.relative_to(R)),'sha256':sha(p)}
assets={p:sha(R/p) for p in ['Harbin_Sophia_Square.blend','game/Sophia_Square.glb','game/Sophia_Collision.glb']}
runtime=json.loads((R/'builds/review/captures/runtime_validation.json').read_text())
native=json.loads((R/'verification/sop_reaudit/native_rework_validation.json').read_text())
assert runtime['assets']==assets and runtime['all_checks_pass'] and runtime['exported_application']
assert runtime['checks'].get('gallery_transverse_ramp_reaches_landing') is True
assert native['source_scene_sha256']==assets['Harbin_Sophia_Square.blend'] and all(native['checks'].values())
write(V/'runtime_validation.json',runtime);write(V/'native_validation.json',native)
images=[]
for p in sorted((R/'builds/review/captures').glob('*.png')):
 target=V/('game_'+p.name);shutil.copy2(p,target);images.append(bound(target))
a=json.loads((A/'audit.json').read_text());a['assets']=assets
a['runtime_report']=bound(V/'runtime_validation.json');a['blender_report']=bound(V/'native_validation.json')
updates={
 'G03':('根据2025-05-29及2026-06-28照片，重做北侧绿色双孔菱格高窗、退台坡屋顶、八个圆拱屋顶窗及顶部檐口；南侧体量另行保留。高度、位置仍待多机位校准。','SOP90_Gallery_north_lattice_clerestory; SOP90_Gallery_raised_roof_block'),
 'G04':('北侧柱头补齿状砖砌挑檐，拱板增加突出金属顶饰和铆钉；现有砌筑仍需近距离对照。','SOP90_Gallery_north_corbel_and_arch_crest'),
 'M09':('新一百上部改为实体背墙、错缝玻璃板和上下退台，屋顶字架随上层立面重新落位。楼高和退台距离仍是估值，未通过尺寸验收。','SOP90_New100_stepped_curtain_wall; SOP90_New100_roof_letter_support'),
 'G05':('区分端头双灯和廊内单个六边笼灯；按历史近照增加托臂、框架和夜间光源。近期灯具状态及数量未确认。','SOP90_Gallery_interior_lamps_and_guards'),
 'G06':('首个临街入口改为右拱台阶、左侧横向斜坡及护栏；新增连续楔形碰撞。第二入口未擅自复制；两处准确标高和坡度仍待验证。','V221_Gallery_landings_and_rails; SOP90_Gallery_offset_entry_ramp'),
 'G08':('增加朝广场侧的外鼓栏杆、卷草细铁件、矮墙和内侧笼灯。地下出入口及真实落地关系仍未全部重建。','SOP90_Gallery_interior_lamps_and_guards'),
 'M02':('五个系统字体改为从4418像素原照描取的可编辑实体轮廓，并加入便携式LED灯珠纹理。等高等距安装仍与原照有1.83%画面对角线最大误差，未通过1%检查。','SOP90_Daoli_sign_*'),
 'M03':('八杂市金色标识改为原照轮廓实体，包括屋顶轮廓、三拱及文字区域；单照透视未校正，未通过。','SOP90_Bazashi_*'),
 'M04':('拆除遮挡店内的旧实体墙，重建非等宽框扇、横楣、把手和打开的回转门扇；遮挡处的门宽与开启方向尚未完全确认。','SOP90_Market_observed_portals'),
 'M05':('右侧两块挂板、中间凹入冰箱贴店、可读价签、左侧饮料窗口和右侧店招分别建模；货架细节为估计，尚无对应机位验收。','SOP90_Market_gift_shop'),
 'M06':('增加雨棚缺口、双摄像头、右侧排气管和弯头，保留分段接箍及底板拼缝；尺寸、挂点待标定。','SOP90_Market_canopy_fittings'),
 'M10':('删除错误欢迎词；现为屏幕壳体，原照中的食品广告画面尚未重建，明确保留缺陷。','SOP90_Market_observed_portals')}
for item in a['items']:
 if item['id'] in updates:
  assert item['status']!='MATCHED','Never overwrite an accepted item without review'
  item['current_model'],item['implementation_objects']=updates[item['id']]
  item['rework_evidence']=['renders/sop_rework/cameras.json',str((V/'native_validation.json').relative_to(R)),str((V/'runtime_validation.json').relative_to(R))]
 if item['id']=='G06':item['next_action']='同实拍机位校准右拱台阶、横向坡道的宽度/标高，并核实第二入口及地下楼梯。'
 if item['id'] in ['M02','M03']:item['next_action']='根据独立斜视照片校正字形透视、立面曲率与安装位置；同机位对照误差须达标。'
 # A new source can inform several items; it does not automatically close any.
 extra={'G03':['baidu_gallery_201905','zol_50479524','zol_50962487','zol_50962489'],'G04':['zol_50962487'],'G07':['zol_50962488'],'M09':['zol_50962488'],'G05':['gallery_yx2022_detail','gallery_night_trip_2024'],'G08':['gallery_yx2022_detail','gallery_night_trip_2024'],'M08':['market_xinhua_202501'],'S01':['baidu_gallery_201905']}.get(item['id'],[])
 item['photo_ids']=list(dict.fromkeys(item['photo_ids']+extra))
write(A/'audit.json',a)
sources=json.loads((A/'sources.json').read_text());result=inspect(R,sources,a);p=progress(a,result)
write(V/'reference_validation.json',result);write(V/'progress.json',p)
manifest={'status':'REWORK_IN_PROGRESS_NOT_ACCEPTED','assets':assets,'native':bound(V/'native_validation.json'),'runtime':bound(V/'runtime_validation.json'),'app_zip':bound(R/'builds/review/SophiaWalk.zip'),'audit':bound(A/'audit.json'),'sources':bound(A/'sources.json'),'renders':[bound(x) for x in sorted((R/'renders/sop_rework').glob('*.png'))],'cameras':bound(R/'renders/sop_rework/cameras.json'),'game_images':images,'progress':p}
write(V/'manifest.json',manifest)
text=f'''# 90% 目标持续返工记录

未验收。原 21 项范围保留，至少 19 项有完整实景证据才达到 90.48%。当前可证明通过 {p['numerator']}/{p['denominator']} 项；技术验证不计入这个比例。

## 实际交付与验证

主工程 `Harbin_Sophia_Square.blend`、游戏 GLB、碰撞和本地预览已同步。根目录双击 `启动返工预览.command`；Blender 打开 DAY/NIGHT 场景可直接渲染。

- 原生场景检查 {len(native['checks'])} 项全部通过。
- 独立 Mac 应用检查 {len(runtime['checks'])} 项全部通过，包括右拱台阶、横向斜坡和中柱阻挡。
- 最近一次运行平均 {runtime['mean_fps']:.1f} FPS；仅代表本机本次检查画面，不能代表整图最低帧率。
- 28 项证据门禁回归测试通过，涵盖删项、缺证据、旧资产、重复项和伪造90%等拒绝条件。
- [实际昼夜渲染](../../renders/sop_rework/) / [本轮对照页](复核.html) / [逐项原始差异表](../../references/sop_reaudit/audit.json)。

## 已整改但尚未实景验收

砖廊：北侧双孔菱格高窗及退台屋顶、齿状柱头和拱顶金属饰件；连续拱板与拱上网格、廊内六边笼灯、外鼓卷草栏杆、抬高屋顶；首个入口改为右拱台阶和左侧横向坡道，新增实际斜面碰撞。

菜市场：可编辑的实拍字形和金色标识、LED灯珠材质、非等宽门组、凹入商铺、分开的挂板和价签；雨棚摄像头、缺口、管道。旧墙不再封死新店面。新一百上部重做实体背墙、错缝玻璃板、两级退台和与立面相接的字架。

## 未达到90%的具体原因

有效近期目标外景仍为 {len(result['eligible_recent_photos'])} 张，尚未满足至少10张及完整机位覆盖。新增2025年5月和2026年6月摄影原帖保留逐图拍摄日期；其他近照和街景包括2022、2024年初、2019年5月资料，只用于发现结构差异，不能冒充近期照片。

招牌诊断相机拟合最大偏差1.83%，超过1%阈值；该拟合使用同一张原照提取的轮廓，也不能代替独立多视角核实。市场圆角入口、窗带/面板、屋顶退台、屏幕广告与夜景；砖廊第二入口、地下通道和部分屋顶尺寸仍未闭合。

`MATCHED` 均需源照片、当前资产、相机、渲染和有效对照证明。正式发布门禁保持拒绝，不发布新版本标签。目标仍在执行中，本页是可复查的工程检查点。
'''
(V/'README.md').write_text(text)
# Replace stale summary pages with a link to the current checkpoint.
(R/'verification/sop_reaudit/README.md').write_text('# 当前返工记录\n\n此前批次已由[90%目标持续返工记录](../sop90/README.md)替代。当前仍未实景验收；勿将旧报告或旧截图当作新资产证据。\n')
parts=['<!doctype html><html lang="zh-CN"><meta charset="utf-8"><title>SOP 90% 返工核实</title><style>body{font:16px/1.6 sans-serif;background:#172127;color:#e3e8ed;margin:28px}a{color:#88cdfd}section{display:grid;grid-template-columns:1fr 1fr;gap:20px}img{width:100%;height:430px;object-fit:contain}figure{margin:0}h1{color:#ffc47b}article{border-top:1px solid #5e6c73;padding:10px}</style><h1>持续返工，实景尚未验收</h1><p>21项固定基线，19项才达到90.48%。以下是原照与当前真实渲染的检查视图，没有伪装成标定通过。</p>']
for title,photo,render in [('北侧砖廊','references/sop_reaudit/local/zol_50962487.jpg','renders/sop_rework/DAY_gallery_north.png'),('临街砖廊','references/v2_2/brick_gallery_2025.jpg','renders/sop_rework/DAY_gallery.png'),('道里菜市场','references/sop_reaudit/local/market_primary_20250621.jpg','renders/sop_rework/DAY_market.png')]:
 parts.append('<h2>'+title+'</h2><section>')
 for path,label in [(photo,'实拍参考（原图仅本机）'),(render,'本轮 Blender 实际渲染，未匹配相机')]:
  parts.append('<figure><img src="'+html.escape(os.path.relpath(R/path,V),quote=True)+'"><figcaption>'+label+'</figcaption></figure>')
 parts.append('</section>')
for i in a['items']:parts.append('<article><b>'+html.escape(i['id']+' '+i['subject']+' / '+i['status'])+'</b><p>'+html.escape(i['current_model'])+'</p><p>下一步：'+html.escape(i['next_action'])+'</p></article>')
(V/'复核.html').write_text(''.join(parts))
print('SOP90_CHECKPOINT',p['numerator'],p['denominator'],p['milestone_90_pass'])
