> **V2.2 更新**：可玩入口为根目录 `启动游戏Demo.command`；当前总说明见 [README.md](README.md)，游戏操作见 [demo/README.md](demo/README.md)，实景验收仍未通过。以下为既有资产说明，V2.1 路径属于历史版本。

# 哈尔滨圣索菲亚教堂及周边 · Blender 场景资产包

## 先确认交付形式

本包是真实、可编辑的三维网格、PBR 材质和 Blender 建工程脚本，**不是 AI 效果图，也不是将图片改后缀得到的模型**。

**本包不含预先保存的 `.blend` 文件。** 制作环境没有可运行的 Blender，且安装下载未成功。因此交付的是：

- `Harbin_Sophia_Scene.glb`：完整三维场景，材质图片已内嵌，可在 Blender 中导入。
- `build_blender_scene.py`：在用户本地 Blender 中创建完整场景、灯光、相机、材质、辅助碰撞体，随后保存真正的 `Harbin_Sophia.blend`。
- `source/scene_geometry.npz`：与 GLB 一致的原始可编辑网格数据。脚本直接读取，不依赖第三方插件。
- `renders/`：由相同网格生成的 **VTK 检查预览**，不是 Blender / Cycles 的实机渲染结果。预览图内也标注了这一点。

脚本已完成 Python 语法检查；网格、GLB、纹理打包在当前环境中实际生成并检查。**尚未完成 Blender 运行测试、游戏引擎测试或逐像素实景匹配测试。**

## 1. 在 Blender 中打开并渲染

### Windows：不用手动写代码

1. 将 ZIP **完整解压**到可写入的文件夹；不要只提取 GLB 或单独提取脚本。
2. 安装并使用 Blender 4.2 或更新版本。脚本按 4.2+ 接口编写，但未在此环境实机验证兼容性。
3. 双击 `BUILD_AND_OPEN_WINDOWS.bat`。脚本会寻找系统安装的 Blender，创建 `Harbin_Sophia.blend`，随后打开该工程。
4. 在 Blender 中按 **F12** 渲染默认的西北侧相机。也可以双击 `BUILD_AND_RENDER_WINDOWS.bat`，直接创建工程并输出第一张图片。

如果找不到 Blender，将真正的 `blender.exe` 拖到 BAT 文件上；或使用下面的通用方法。不要将 Blender 快捷方式 `.lnk` 作为可执行文件拖入。

### Windows / macOS / Linux 通用方法

先在 Blender 中新建空白文件，避免覆盖正在编辑的场景。切换到 **Scripting / 脚本** 工作区，在 Text Editor 中使用 **Open / 打开** 选择包内的 `build_blender_scene.py`，然后按 **Alt+P / Run Script**。

脚本会清空当前场景对象，读取本包网格并创建工程。完成后，包所在文件夹出现 `Harbin_Sophia.blend`。按 F12 即可开始渲染。

macOS / Linux 还可以在终端执行：

```bash
bash build_and_open.sh
# Blender 不在默认位置时：
bash build_and_open.sh /完整路径/到/blender
```

命令行创建工程并渲染：

```bash
blender --background --python build_blender_scene.py -- --render
```

使用 Eevee 输出 1280 宽预览：

```bash
blender --background --python build_blender_scene.py -- --engine EEVEE --resolution 1280 --render
```

使用 Cycles 渲染全部六台相机：

```bash
blender --background --python build_blender_scene.py -- --all-cameras --samples 128
```

保存位置：工程为 `Harbin_Sophia.blend`；本地 Blender 输出图片为 `blender_renders/`。脚本在开始渲染前先保存工程，所以渲染被取消不等于建模结果丢失。默认使用 CPU，避免误判用户显卡；可在 Blender 内自行选择受支持的设备。

### 只导入现成模型，不运行脚本

在 Blender 使用 **File → Import → glTF 2.0 (.glb/.gltf)**，选择 `Harbin_Sophia_Scene.glb`。注意是“导入”，不是“打开 .blend”。

GLB 包含网格、贴图、PBR 材质及相机，但不包含 Blender 专用的 Nishita 天空、Cycles 设置及隐藏碰撞辅助集合。查看材质可切换 Material Preview；要按本包设置渲染，推荐运行建工程脚本。

## 2. 场景内容

教堂主体包含红砖外墙、砖饰带与拱券、西侧门廊、西侧高钟楼、真实开孔的钟楼窗、钟体、中央多边形鼓座、洋葱形主穹顶、屋面菱形接缝、十字架、侧翼、东侧不同于正门的后殿，以及台阶、门窗及格栅。门窗不是贴在单一立方体上的整张建筑照片。

场地为约 260 × 282 米的地面基底，广场主体位于教堂北侧。场景包含铺装、绿化、座椅、路灯、栏柱、低层服务建筑、周边商用建筑简化体量及少量道路车辆。**周边不是逐栋实测复刻；构件布局中存在估计与概括。**

默认没有雪、游客和临时展陈；不使用上一轮 AI 概念图里的虚构宫殿街景。日照为展示性日光设置，不是按某日某时哈尔滨太阳方位进行的严格复现。

### 材质

包含红砖、砖饰、绿色涂漆金属、广场花岗岩、深色石材、浅色建筑石材、沥青、木材及金属等材质。主体材质提供 Base Color、ORM、OpenGL Normal；主要纹理尺寸 1024–2048 像素，UV 按米制尺度铺设。

所有贴图为本次程序化制作的原创纹理，**不是现场扫描、摄影测量或实物采样贴图**。绿色屋面按涂漆铁皮表达，不把它说成铜绿屋顶。PBR 支持不等于近距离照片级复刻；最终显示也取决于渲染器、采样与曝光。

### Blender 集合

`01_LANDMARK` 教堂；`02_GROUND` 地面；`03_PUBLIC_REALM` 公共设施；`04_CONTEXT` 简化周边；`05_STREET` 街道元素；`06_OPTIONAL` 非实景附加牌（默认隐藏）；`07_CAMERAS` 相机；`08_LIGHTING` 光照；`09_COLLISION_HIDDEN` 辅助碰撞体；`10_GAME_MARKERS_HIDDEN` 建议出生点。

作者坐标：米制，+X 为建筑东侧，+Y 为北侧，+Z 向上；这只是建模坐标，并非 GIS 测绘配准。GLB 使用其标准的 Y-up 轴约定，导入器应负责坐标转换。

## 3. 实景还原边界

**定位：基于公开实景照片与资料的外观重建初版，不是测绘级数字孪生。**

53.35 米的公开总高作为主要尺度锚点；红砖、洋葱顶、前后立面区别和十字形主体组织有资料支撑。穹顶曲线、窗间细节和建筑尺度之间的精确关系没有施工图或点云支撑。估计项被详细列在 `docs/实景核对与偏差.md`，来源目录在 `reference/sources.json`。

**不能承诺**：教堂所有构件误差小于某数值、周边建筑和铺装一一精确对应、2026 年现况完全一致，或与任意实景机位像素级重合。

## 4. 开放世界 / FPS 地图用途

这是可供继续开发的**室外关卡场景资产底稿**，不是已经在游戏引擎中完成验收的可发行关卡。

`game/Harbin_Sophia_Landmark.glb` 可单独导入地标；`game/Collision_Proxies.glb` 和 `game/collision_shapes.json` 提供简化静态碰撞参考。碰撞文件独立于可见模型，不会把半透明辅助体混进最终渲染。

凸体代理与凹的教堂整体轮廓有区别：`COL_STATIC` 是凹轮廓静态代理，不能简单当作 Unreal 的单个凸 UCX。引擎内仍需设定碰撞方式、检查穿透及地面高度、烘焙导航、调整角色胶囊、制作 LOD/HLOD、做遮挡和性能优化。

当前不含：教堂内部、可进入商铺、可破坏物、玩家控制器、武器、敌人 AI、已烘焙导航网格、光照贴图 UV2、平台帧率测试。教堂门默认为关闭；1.72 米相机和建议出生点只用于人尺度观察，并不是已经跑通的第一人称控制器。

## 5. 源码、检查与使用

`source/build_assets.py` 是几何与材质的原始生成程序，重建所需依赖为 NumPy、SciPy、Pillow、Shapely。**普通使用不必运行它**；Blender 的建工程脚本只需 Blender 自带的 bpy 和 NumPy。

`docs/asset_report.json` 记录资产数量；`docs/validation_report.json` 记录实际执行的检查，不应将其当作 Blender 官方 glTF Validator 或游戏性能测试。

在本包范围内，本次制作的源代码、网格和程序化纹理以 CC0 方式提供。外部引用的照片、实际建筑设计、地标名称或其他第三方内容仍按其各自权利状态处理；本包不附带现场照片、任何字体文件或 Blender 安装程序，也不对第三方权利作保证。
