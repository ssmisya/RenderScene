# 哈尔滨圣索菲亚广场 · v2

可离线打开、编辑、渲染的 Blender 原生外景工程，内含白天与夜晚两套场景。主文件：**Harbin_Sophia_Square.blend**。

## 仓库版本

**默认主版本：V2 · `main` · `v2.0.0`**。克隆后先执行 `git lfs pull` 下载模型、贴图及成片。完整流程见 [版本管理.md](版本管理.md)，版本记录见 [CHANGELOG.md](CHANGELOG.md)。

## 直接使用

1. 打开主工程，或双击 `打开白天.command` / `打开夜晚.command`。
2. Blender 顶部 Scene 菜单切换 **01_DAY_白天** / **02_NIGHT_夜晚**。
3. 按 **F12** 渲染，默认 **2400 × 1600、Cycles 192 samples**。本机已使用 Apple M5 / Metal 实渲。
4. 成片在 **renders/v2/**，每个机位都有 DAY / NIGHT 对照。双击 `preview.html` 可查看离线画廊。
5. 用 F3 搜索 **Walk Navigation**，鼠标转向、WASD 移动；相机的人眼高度为 1.70 m。

完整说明：[V2_实景核对与使用.md](V2_实景核对与使用.md)。文件与脚本索引：[目录与使用指南.md](目录与使用指南.md)。

## 这一版

- 新补充 32 张实拍参考，涵盖门廊细节、游客机位、广场反向视角和夜景；作者、许可和原页面都保存在 `references/v2/`。
- 重做分格双扇门、浮雕、径向砌砖、拱券齿饰和退台；扫描材质升到 4K，补充风化与近景细节。
- 分开处理周边商业街、高层与裙房，新增钟塔、封闭亭屋等可辨认环境元素；修正广场与透笼街的边界。
- 白天无人工灯光或自发光网格；夜间开启独立的教堂投光、射灯、商业灯光与广场路灯。
- 原工程、脚本、成片和旧游戏导出保存在 `backups/pre_v2_20260913/`；根目录更早的 ZIP、GLB 等资产未覆盖。

这是**照片参考重建**，尚非实地扫描或 1:1 数字孪生。周边楼高、上层体量、装饰及临时街具仍有推定，室内与写实动态人群未制作。具体已核对与仍估计的部分见完整说明。

## 主要目录

| 目录或文件 | 用途 |
|---|---|
| Harbin_Sophia_Square.blend | 当前主工程，全部使用中的图片、字体内嵌 |
| renders/v2/ | 7 个机位 × 两种光照的 Blender 实渲 |
| assets/textures/v2/ | 4K 扫描材质及拱砖面裁切；原 1K 资源仍保留 |
| references/v2/ | 新参考照片、联系表、许可、逐图索引 |
| scripts/ | 重建、灯光、渲染、验证、游戏导出脚本 |
| game/ | 可见网格 GLB、碰撞 GLB、出生点、路线、夜灯参数 |
| validation_v2.json | 场景、纹理、字体、日夜隔离、尺寸与路线检查 |
| game/export_validation.json | 两份 GLB 重新导入检查 |
| renders/v2/render_validation.json | 成片尺寸、像素内容检查 |
| backups/pre_v2_20260913/ | 本轮修改前的可回退快照 |

## 游戏使用

1 单位 = 1 米。Blender Z 向上；导出 glTF Y 向上，坐标为 `(x,z,-y)`。可见网格与碰撞代理分别导入引擎，非凸建筑使用静态三角网格碰撞或凸分解。出生点、眼高与绕行路线在 `game/map_metadata.json`。

游戏 GLB 使用最多 2K 的便携 PBR 副本；它不完整表达 Cycles 程序化风化、世界环境与夜间照明。`game/lighting_v2.json` 提供夜灯布置参数，但目标引擎需要转换光强并重新调光。尚未完成特定游戏引擎的 LOD、NavMesh、流式加载和运行帧率测试。

## 命令行

在主工程目录运行，把 `blender` 替换为本机 Blender 可执行文件：

```sh
blender -b Harbin_Sophia_Square.blend --python scripts/render_v2.py -- --mode both --view all
blender -b Harbin_Sophia_Square.blend --python scripts/validate_v2.py
blender -b Harbin_Sophia_Square.blend --python scripts/export_game.py
blender -b --python scripts/verify_game.py
```

完整重建使用 `blender -b --python scripts/build_scene.py`，会覆盖主工程与派生数据。已有手工修改时请先另存。

开放素材署名：Poly Haven CC0；© OpenStreetMap contributors / ODbL；实拍照片作者与 CC 许可见 `references/v2/实拍照片索引.md` 及 `REFERENCES.md`。
