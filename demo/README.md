> 实景验收重审中：V2.2.1 不代表修正完成。正式构建默认被门禁拦截；本地QA可用 `python3 scripts/build_demo.py --preview`，输出仅在 `builds/review/`。详见 `verification/sop_reaudit/README.md`。

> V2.2.1 更新：修复棚廊 / 菜市场，新增棚廊登阶检查。最新报告与定点游戏截图在根目录 `verification/v2_2_1/`、`renders/v2_2_1/`；发布包为 `SophiaWalk_macOS_v2.2.1_demo.zip`。下文 V2.2 原始报告仍作为历史记录。

# 索菲亚广场 · 持枪漫游 V2.2 Demo

Godot 4.7.2 / macOS / Metal Forward+。复用本仓库 Blender 外景、PBR 贴图与碰撞代理，提供可运行的单人第一人称外景原型。**实景还原验收未通过**；这是可玩开发版本，周边并非 100% 复原。

## 直接运行

回到项目根目录，双击 `启动游戏Demo.command`。本机已有独立应用 `builds/索菲亚广场 · 持枪漫游.app`，无需先打开 Blender 或 Godot 编辑器。首次从 Git 克隆后执行 `git lfs pull`，启动脚本会自动解压根目录 `SophiaWalk_macOS_v2.2_demo.zip`。

入口菜单选择「进入白天」或「进入夜晚」。按 Esc 释放鼠标并返回菜单。

| 操作 | 按键 |
|---|---|
| 行走、环顾 | WASD、鼠标 |
| 奔跑、跳跃 | Shift、空格 |
| 开火、瞄准、换弹 | 左键、右键、R |
| 白天 / 夜晚 | N |
| 手电、收枪 | F、G |
| 隐藏界面、保存截图 | H、P |
| 菜单、释放鼠标 | Esc |

截图存到应用所在 `builds/captures/`；编辑器运行时存到 `demo/qa/`。窗口默认 1280×800，UI 基准画布 1440×900。眼高 1.70 米；教堂和周边建筑当前只开放外部。武器为自制简化演示模型，声音为合成音效。没有敌人、联网、任务系统、建筑内部或破坏系统。

## 编辑与重建

- 双击根目录 `打开Godot工程.command`：打开 `project.godot`，F6/F5 运行。
- 双击 `构建游戏Demo.command`：准备锁定版本的本地引擎，重新同步 GLB / 灯光 / 天空，导出独立 Mac 应用。
- 引擎、导出模板放在根目录 `.tools/godot/`，不改系统安装。`engine_lock.json` 固定官方下载地址和 SHA-256。

```sh
python3 scripts/setup_godot.py
python3 scripts/build_demo.py
```

以上命令在仓库根目录运行。导出结果位于 `builds/`，历史发布 ZIP 不会自动覆盖；确认后手动更新版本化 ZIP。

Blender 修改后的完整同步顺序：

```sh
/Applications/Blender.app/Contents/MacOS/Blender -b Harbin_Sophia_Square.blend --python scripts/validate_v22.py
/Applications/Blender.app/Contents/MacOS/Blender -b Harbin_Sophia_Square.blend --python scripts/export_game.py
/Applications/Blender.app/Contents/MacOS/Blender -b --python scripts/verify_game.py
python3 scripts/build_demo.py
```

GLB 使用可迁移 PBR 副本。Cycles 程序化材质与光能参数不能逐项直接复制到 Godot；当前游戏材质和灯光仍与 Blender 离线成片有差异。没有配置分区加载、专项 LOD 或完整地图性能预算。

## 文件用途

| 文件 / 目录 | 作用 |
|---|---|
| `project.godot`、`main.tscn` | 项目设置与启动场景 |
| `scripts/main.gd` | 导入地图、静态碰撞、日夜灯光、菜单、HUD、命中点和运行 QA |
| `scripts/player.gd` | 胶囊角色、鼠标视角、台阶、跳跃、枪械与手电 |
| `assets/square.glb` | 当前 Blender 可见网格的同步副本 |
| `assets/collision.glb` | 独立简化碰撞代理 |
| `assets/lighting.json` | Blender 夜灯位置和目标点，运行时换算为 Godot 灯光 |
| `assets/day_sky.hdr` | 复用的 Poly Haven CC0 天空 |
| `assets/manifest.json` | 构建所使用主工程 / GLB 的 SHA-256 |
| `assets/square_*`、`*.import` | GLB 导入材质纹理与可重复导入设置 |
| `audio/` | 自制演示音效，生成器为根目录 `scripts/create_demo_audio.py` |
| `export_presets.cfg`、`engine_lock.json` | Mac 导出参数与锁定引擎版本 |
| `LICENSES.txt` | Godot、开放场景数据、贴图等署名 |

## 验证与限制

实际独立 Mac 应用的图形运行检查保存于根目录 `verification/v2_2/runtime_validation.json`；涵盖 15 项控制、台阶 / 墙体、日夜开关检查。截图为真实引擎视口，不是 Blender 成片或效果图。

```sh
'builds/索菲亚广场 · 持枪漫游.app/Contents/MacOS/索菲亚广场 · 持枪漫游' -- --qa
python3 scripts/validate_references.py --strict
```

第一条会运行约半分钟并自动退出、保存截图和结果。第二条当前**应退出 2**：照片覆盖、时间一致性及 9 项实景差异尚未完成。这不是运行错误；正式实景发布必须先消除这些差异。短时帧率采样不能代表全地图、所有设备或长时间稳定帧率。

实景标准见 `docs/实景复原与地图扩展SOP.md`，证据与未解决项见 `references/v2_2/`。新闻 / 游客照片仅作本地研究，未作为游戏贴图发布。
