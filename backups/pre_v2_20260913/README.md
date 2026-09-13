# 哈尔滨 · 圣索菲亚广场

可在 Blender 中离线打开、编辑和渲染的外景场景。以实拍照片核对教堂主要结构，以 OpenStreetMap 放置周边建筑轮廓，并补充可供第一人称地图使用的碰撞代理与出生点。

**请先了解精度边界：这是实景参考重建，不是实地扫描。** 教堂的主要外形与四面差异有照片依据；周边楼高、立面、部分街具位置是推定。没有制作教堂室内，也没有声称达到与现场无法分辨的摄影测量级保真。逐项依据见 `REFERENCES.md`。

## 直接使用

1. 在 Blender 5.2.1 LTS 或兼容版本中打开 `Harbin_Sophia_Square.blend`。
2. 按 **F12** 渲染默认广场机位。所有依赖贴图和 HDRI 已打包，不需要联网。
3. 在 `08_CAMERAS_LIGHTS` 集合中选择其他相机，按 **Ctrl + 小键盘 0** 设为活动相机；再按 F12。
4. 想从人眼高度看地图，选择 `02_EYE_LEVEL_170cm`，进入相机视图后使用 **Shift + 波浪键/反引号键** 的 Walk Navigation，鼠标转向、WASD 移动。不同键盘布局可以通过 F3 搜索 `Walk Navigation`。

默认 Cycles、1920 × 1280、96 samples、降噪。这个项目在 Apple M5 / Blender 5.2.1 上制作。脚本优先使用 Metal；非 Mac 机器请在 Blender Preferences → System 中选择自己的渲染设备，或改用 CPU。

## 文件

| 文件/目录 | 用途 |
|---|---|
| `Harbin_Sophia_Square.blend` | 主场景，原生网格、可编辑相机、灯光、材质，纹理内嵌 |
| `renders/` | 实际由 Blender 渲染的检查图 |
| `scripts/build_scene.py` | 从原始地图数据和材质重建整个场景 |
| `scripts/render_scene.py` | 批量渲染指定机位 |
| `scripts/export_game.py` | 导出独立 glTF 游戏资产，不覆盖 Cycles 场景 |
| `game/Sophia_Square.glb` | 支持 glTF 的引擎可导入的外景网格与简化 PBR 材质 |
| `game/Sophia_Collision.glb` | 单独的碰撞代理几何；导入后应作为静态碰撞，不作为可见物体 |
| `game/colliders.json` | 代理的米制尺寸、位置、旋转与多边形数据 |
| `game/map_metadata.json` | 第一人称出生点、围绕教堂的路线、地理参考与单位 |
| `scene_stats.json` | 实际导出的场景统计 |
| `REFERENCES.md` | 实景核对、精度范围、素材许可证 |
| `references/` | 开放地图原始数据、参考照片与作者信息 |
| `assets/textures/` | 本地通用 PBR 贴图和天空 HDRI |

## 场景组织

- `01_CATHEDRAL`：教堂主体，按基础、长墙、后殿、西门钟楼、中央鼓座、洋葱顶、排水和台阶分组。
- `02_SQUARE`：广场地面、铺装分带、排水和推定的地面喷泉格栅。
- `03_OSM_BUILDINGS`：带 OSM way ID 的周边建筑，以及明确标记为 estimated 的背景体量。
- `04_VEGETATION`：逐叶几何树木和入口盆栽。
- `05_STREET_PROPS`：路灯、长椅、拱廊、导览牌和街具。
- `06_ROADS`：地图道路。
- `07_COLLISION`：隐藏的独立代理。开关集合查看线框，不参与渲染。
- `08_CAMERAS_LIGHTS`：五个机位、日光和环境设置。
- `09_GAME_MARKERS`：出生点及闭合的外部探索路线。

## 游戏地图使用范围

1 Blender 单位 = 1 米，场景 Z 向上。glTF 导出为 Y 向上，坐标转换为 `(x, z, -y)`。JSON 保留原始 Blender 坐标；自写引擎加载器时要转换。

建议从 GLB 网格和碰撞代理分别导入。碰撞代理包含实心基础、教堂外壳、树干、街具、道路地面和周边建筑；大面积 U 形建筑保留多边形轮廓，避免用一个大包围盒封住其院落。JSON 的 `polygon` 适合生成静态三角网格碰撞，不能把非凸轮廓直接作为单个凸碰撞体。

`SPAWN_Main`/JSON 初始眼高为 1.70 m，建议人物胶囊半径 0.30 m。玩法范围为**围绕教堂的户外探索**；门关闭。出生点和路线用于地图搭建，不包含游戏角色动画、敌人、武器、战斗系统或已完成的引擎 NavMesh。

GLB 为便携版本：保留建筑几何和扫描 PBR 贴图，程序化噪声与 Cycles 特有细节简化为常规 PBR，因此最终高质量画面以 `.blend` 为准。它仍是精细地图资产，尚未针对某款游戏引擎制作自动 LOD、烘焙光照、流式加载或做帧率基准测试。请在目标引擎配置静态碰撞和材质后测试，不能把代理存在等同于已经完成游戏运行时集成。

## 命令行

在这个目录执行；按机器实际位置设置 Blender 命令：

```sh
# 从保存的工程渲染人眼机位
blender -b Harbin_Sophia_Square.blend --python scripts/render_scene.py -- --view eye --width 1920 --samples 128

# 五个机位，或使用 --cpu
blender -b Harbin_Sophia_Square.blend --python scripts/render_scene.py -- --view all --width 1920 --samples 128

# 完整重建，会重新保存主场景
blender -b --python scripts/build_scene.py

# 导出游戏网格与代理
blender -b Harbin_Sophia_Square.blend --python scripts/export_game.py
```

参考照片的文件名有历史暂用命名，朝向以 `REFERENCES.md` 中核对后的说明为准。分发时请保留 OpenStreetMap 数据署名，以及随附实拍照片作者和许可证信息。

## 已完成的验证

- 主工程在全新后台 Blender 进程中读取并实际渲染五个机位。
- 已检查所有 7 张文件纹理/HDRI 的有效尺寸和内嵌状态。
- 主体几何最高点约为 53.3500 m。
- 125 个碰撞代理在主工程中不参与渲染。
- 两份 GLB 均重新导入 Blender，检查文件头、网格数量、空网格与内嵌图片。
- 环绕路线做了 408 次位置采样，未与定义的障碍物相交；这不替代引擎中的胶囊碰撞和 NavMesh 检查。

详见 `validation.json`、`game/export_validation.json`、`game/route_validation.json`。使用 Walk Navigation 会改变当前观察位置；想保留机位时可先复制相机。
