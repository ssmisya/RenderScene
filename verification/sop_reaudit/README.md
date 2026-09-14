# 主工程返工已整合，实景 SOP 仍未通过

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
| 近期原照 | 共筛查 75 张候选；有效近期目标外景仍仅2张，未达10张/3独立作者及覆盖要求。 |
| 差异表 | 21项继续开放，8项已有实际建模修订；无项目伪标MATCHED。 |
| 返工 | 主工程、GLB、碰撞和本地应用已整合；其余差异未解决。 |
| 实拍机位比对 | 未完成；本页是检查视图，无6点相机标定，不宣称1%精度。 |
| 技术验证 | 当前资产的独立Mac应用 17/17 项通过；新中柱碰撞、拱洞通行、昼夜均实际测试。原生检查9项通过，GLB实际重导入通过。 |
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
