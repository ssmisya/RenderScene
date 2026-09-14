> **当前状态：持续返工，90% 实景目标尚未达到。** 原 21 项核实范围保持不变，至少 19 项有完整实拍对照才能达到 90.48%。本轮已修改砖廊偏置台阶/横向坡道、拱板、灯具、栏杆和屋顶，以及市场实体字形、门组、凹入商铺与雨棚细节。新增北侧菱格高窗、坡屋顶、齿状柱头和新一百实体退台玻璃幕墙。当前分支 `codex/sop-reaudit-v2.2.1`；本机双击 **`启动返工预览.command`**。原生检查 15 项、独立游戏检查 18 项通过；它们不计为实景通过率。详见 [当前证据与差异](verification/sop90/README.md) 和 [逐项进度](verification/sop90/progress.json)。原正式应用与历史标签保留，正式发布门禁继续拒绝。

> **V2.2.1 定点修正（2026-09-14）**：修复棚廊悬空扶手、孤立台阶和薄片山花，补连续平台、砖材质；重做道里菜市场面板拼缝、入口、雨棚、绿色招牌和屋顶字支架。操作入口仍为 `启动游戏Demo.command`，新版游戏包为 `SophiaWalk_macOS_v2.2.1_demo.zip`。对照和说明见 [本轮验证](verification/v2_2_1/README.md)。本轮仅 2 张照片具备有效近期拍摄依据，正式实景验收仍未通过；没有宣称两处达到 100% 复原。以下 V2.2 初版说明和报告保留其历史含义。

# 哈尔滨圣索菲亚广场 · V2.2 可玩 Demo

当前工作分支：`codex/v2.2-playable-demo`。V2.1 稳定基线、历史标签和资产保留；V2.2 属于 V2 主线的开发 Demo。**游戏可以运行，周边实景还原验收仍为 NOT_ACCEPTED。**

## 马上体验

1. 双击根目录 **`启动游戏Demo.command`**，选择进入白天或夜晚。
2. WASD 行走，鼠标环顾，Shift 跑，空格跳，左键开火、右键瞄准、R 换弹。
3. N 切换昼夜，F 手电，G 收枪，Esc 打开菜单并释放鼠标。

独立 Mac 应用位于 `builds/索菲亚广场 · 持枪漫游.app`，可分享压缩包为 `SophiaWalk_macOS_v2.2_demo.zip`。不需要先开 Blender 或 Godot 编辑器。克隆仓库后先执行 `git lfs pull` 获取模型与应用 ZIP。

游戏说明和源码索引：[demo/README.md](demo/README.md)。双击 `打开Godot工程.command` 可继续开发；`构建游戏Demo.command` 可从当前模型重新打包。

## Blender 主工程

主文件仍为 **`Harbin_Sophia_Square.blend`**，两套场景是 `01_DAY_白天` / `02_NIGHT_夜晚`。双击 `打开白天.command` / `打开夜晚.command`，或直接打开主文件；F12 渲染。当前成片在 [renders/v2_2/](renders/v2_2/)。旧版 `preview.html`、ZIP 和 `renders/v2_1/` 是历史成果。

本次增加砖廊回折和端头构件、钢构拱廊与格栅、商业楼屋顶窗框和檐部细节；替换缺乏依据的旋转木马为待核位置的圆形采光设施。Blender 与游戏导出同步，粗糙鸽子继续保持删除。

这些是依据照片进行的局部修订，**周边楼体、门窗店招、转角、栏杆、教堂细部仍有已知偏差；不宣称 100% 还原或已实现照片级游戏画面**。游戏中也存在离线材质和实时材质差异。

## 强制实景标准

已查看 18 张图片，其中 10 张满足本批次近期 / 可辨范围条件，来自 4 个独立拍摄来源。部分仅能验证体量，不能验证细小装饰。拍摄日不明、室内和虚焦照片不计入相应数量。当前目标是 2025 常设建筑，2026 最新状态未确认。

- [实景复原与地图扩展 SOP](docs/实景复原与地图扩展SOP.md)：至少 10 张近期独立照片，逐细节对照，发现不一致返工，覆盖和时间均必须通过。
- [照片来源](references/v2_2/README.md) / [逐项差异表](references/v2_2/audit.json)：9 项待处理，不得以照片数量代替准确性。
- [自动实景检查](verification/v2_2/reference_validation.json)：当前 NOT_ACCEPTED。

`AGENTS.md` 已要求后续地图工作遵守 SOP。任何正式“还原通过”结论都需要零未解决差异和对应渲染证据。

## 当前文件与验证

| 文件 / 目录 | 用途 |
|---|---|
| `Harbin_Sophia_Square.blend` | 可离线编辑 / 渲染的原生工程，使用的图片与字体已内嵌 |
| `demo/` | 可编辑 Godot 工程、脚本、PBR 资产、声音和 Mac 导出设置 |
| `game/` | Blender 导出的可见 GLB、碰撞 GLB、灯光与地图元数据 |
| `renders/v2_2/` | 6 张 Blender 实渲及独立游戏应用截图 |
| `verification/v2_2/` | 运行、素材来源、发布校验与限制说明 |
| `validation_v2_2.json` | 原生场景的结构、打包资源、日夜隔离和路线检查 |
| `game/export_validation.json` | GLB 实际重新导入的检查结果 |
| `MANIFEST_v2_2.json` | 本批主工程、导出、Demo 包和成片的哈希 |
| `scripts/setup_godot.py` / `build_demo.py` | 项目内安装锁定引擎、同步资产、构建 Mac 应用 |
| `scripts/v22_street_refinements.py` | 本轮街景几何修订 |
| `scripts/validate_references.py` | 强制参考 / 差异门槛；当前 strict 模式返回 2 |
| `backups/`、旧 ZIP / GLB、旧 MANIFEST | 历史资产，保留不删除 |

本机独立应用已做图形运行检查；详细硬件、短时帧率和 15 项结果见运行报告。单人户外原型，未制作敌人、联网、建筑内部、专项 LOD、全地图长期性能验证。

```sh
# 当前主工程渲染 / 验证（命令在项目根目录执行）
/Applications/Blender.app/Contents/MacOS/Blender -b Harbin_Sophia_Square.blend --python scripts/render_v22.py
/Applications/Blender.app/Contents/MacOS/Blender -b Harbin_Sophia_Square.blend --python scripts/validate_v22.py
python3 scripts/setup_godot.py
python3 scripts/build_demo.py
python3 scripts/validate_references.py --strict
```

完整程序化重建为 `blender -b --python scripts/build_scene.py`，会覆盖主工程；若有手工修改，先另存。Blender 5.2.1 LTS / Godot 4.7.2 是本次实际验证版本。

许可与历史：[demo/LICENSES.txt](demo/LICENSES.txt)、[REFERENCES.md](REFERENCES.md)、[版本管理.md](版本管理.md)、[CHANGELOG.md](CHANGELOG.md)、[V2.1 历史说明](docs/V2.1_README_历史.md)。
