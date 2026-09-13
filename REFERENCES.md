> 当前主版本已更新为 **V2.1.0**。前脸结构、本轮参考和新机位见 [V2.1 结构修正](V2.1_结构修正与实景核对.md)。当前成片在 `renders/v2_1/`，旧 `renders/v2/` 与 V2 ZIP 保留为历史快照。

# v2 补充说明

当前版本的逐项核对与限制见 [V2_实景核对与使用.md](V2_实景核对与使用.md)，新增 32 张照片的署名与许可见 [实拍照片索引](references/v2/实拍照片索引.md)。以下内容保留上一版资料记录；旧版开放圆亭、推定喷泉、统一高楼体量和统计数不再代表当前工程。

# 实景核对与素材来源

本项目是**有公开实景依据的程序化外景重建**，不是摄影测量、激光扫描或测绘数字孪生，也不代表 2026 年 9 月现场全部细节。参考照片主要拍摄于 2023 年。模型可以从任意方向查看，不是照片投影布景。

## 核对结果

| 项目 | 证据 | 模型处理与可信范围 |
|---|---|---|
| 红砖墙、绿色洋葱顶、金色十字架 | 下列西立面、侧立面、东立面实拍 | 已分别检查并建模；砖墙微观纹理来自通用扫描材质，非本建筑实扫 |
| 总高度约 53.35 m、占地约 721 m² | 黑龙江史志网，圣·索菲亚教堂介绍 | 53.35 m 用作高度锚点；不是按测绘图复核每一层高度，占地不声称精确匹配 |
| 约 42 m 长、28 m 宽 | 中文百科建筑特点，作为次级尺度参考 | 外壳约按该尺度重建；OSM 原始轮廓宽度约 23 m，与文献口径不同，未混称为一致 |
| 西侧高钟楼，东侧较低后入口，两翼小尖塔 | N509FZ 西立面实拍；EditQ 东侧/侧面实拍 | 避免四向对称复制，单独构建正门双层开放钟室和东侧低入口 |
| 中央鼓座拱窗、层叠砖券、菱形金属板 | EditQ 2023 年近照 | 几何表现；窗数、砖券断面、屋面分片尺度由照片估计 |
| 周边道路与建筑轮廓 | OpenStreetMap 原始节点/way 数据 | 以经纬度转换后的平面坐标放置；楼高、门窗、店招和屋顶大部分是推定 |
| 广场大规格灰色铺石、深色小铺块分带 | 三方向实拍 | 材料和分带视觉参考；排布不是逐块测量 |
| 树木、长椅、球形路灯、街具 | 照片及广场空间参考 | 外观近似，摆位与数量为游戏探索补全；不宣称对应当前现场 |
| 砖廊、两个圆形小构筑物 | OSM 独立轮廓 | 位置有地图依据，上部造型推定；砖廊做成可穿行拱洞 |
| 干式喷泉格栅、导览牌、酒店轮廓强化 | 广场背景资料和照片 | 明确为推定的环境补全，独立命名方便关闭/替换 |
| 室内空间 | 本次没有足够室内参考 | 未制作可进入室内，教堂门为关闭状态 |

### 文字尺度参考

- 黑龙江史志网：[圣·索菲亚教堂](https://hljszw.org.cn/news/1406.html)，通高 53.35 m、占地 721 m²、红砖和主次穹顶描述。
- [中文百科：建筑特点](https://zh.wikipedia.org/wiki/圣索菲亚教堂_(哈尔滨))，42 m × 28 m 的近似外包尺度，西长东短布局。不同来源使用“拉丁十字”和“希腊十字”术语不一致，因此模型核对以实际外形为主。

## 实拍图片（仅作核对资料，未用来生成贴图）

### N509FZ，2023-07-21，CC BY-SA 4.0

- [West facade … (20230721150450)](https://commons.wikimedia.org/wiki/File:West_facade_of_St._Sophia_Cathedral,_Harbin_(20230721150450).jpg) → `references/west.jpg`
- [West facade … (20230721150540)](https://commons.wikimedia.org/wiki/File:West_facade_of_St._Sophia_Cathedral,_Harbin_(20230721150540).jpg) → `references/west_oblique.jpg`

### EditQ，2023-10-13，CC BY-SA 4.0

- [Cathedral of Holy Wisdom, Harbin 5](https://commons.wikimedia.org/wiki/File:Cathedral_of_Holy_Wisdom,_Harbin_5.jpg) → `references/front_small.jpg`，实际为**东侧后入口**，文件名是下载时暂用名称，不代表正门。
- [Cathedral of Holy Wisdom, Harbin 6](https://commons.wikimedia.org/wiki/File:Cathedral_of_Holy_Wisdom,_Harbin_6.jpg) → `references/side_small.jpg`，实际为东侧鼓座与低入口近照。
- [Cathedral of Holy Wisdom, Harbin 7](https://commons.wikimedia.org/wiki/File:Cathedral_of_Holy_Wisdom,_Harbin_7.jpg) → `references/rear.jpg`，实际为长侧立面和钟楼视角。

原始作者、许可证和图片接口信息保存在 `commons.json`、`west_metadata.json`。照片保留原作者权利，许可证见 [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)。它们不是用于把真实场景贴到平面上的素材。

## 开放地图

© [OpenStreetMap contributors](https://www.openstreetmap.org/copyright)，[ODbL](https://opendatacommons.org/licenses/odbl/1-0/)。下载日期：2026-09-13。

- 教堂 way ID：338425563。
- 原始数据：`references/osm.xml`；本地坐标：`references/map_local.json`；建筑轴向坐标：`references/map_aligned.json`。
- WGS84 参考原点：45.76819° N, 126.62129° E。
- X 轴沿教堂东西向，约为真东向逆时针 17.3°；Y 与其垂直，Z 向上。小范围采用局部等距近似，经纬度转米，不是工程投影测绘成果。
- 地图数据可能缺失或过时。本项目保留来源标识，周边几何中 `OSM_数字` 对应原始 way。

## 渲染素材（CC0）

Poly Haven：

- [Red Brick 03](https://polyhaven.com/a/red_brick_03)：Diffuse、OpenGL Normal、Roughness，1K。
- [Pavement 04](https://polyhaven.com/a/pavement_04)：Diffuse、OpenGL Normal、Roughness，1K。
- [Kloofendal 48d Partly Cloudy PureSky](https://polyhaven.com/a/kloofendal_48d_partly_cloudy_puresky)：2K HDRI。
- [Poly Haven 许可证](https://polyhaven.com/license)：CC0。原始下载 API 信息保存于 `references/*_asset.json`。

主教堂与街具为本项目生成的原生网格，未导入来源不明的商用模型。程序化节点、原生几何和这些通用 PBR 素材共同构成视觉效果。

## 进一步接近实地所需资料

要达到“现场难以分辨”的高精度复现，还需要带尺度的多角度近照/摄影测量、正射影像、当前街区立面、真实材质扫描，以及按目标游戏引擎做 LOD、遮挡剔除和性能预算。本交付不将程序化重建宣称为已完成这些工作。
