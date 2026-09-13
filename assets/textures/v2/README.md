# 材质来源与处理

红砖：Poly Haven red_brick_03，4K JPG，CC0。
铺装：Poly Haven pavement_04，4K JPG，CC0。

API 来源记录沿用 references/brick_asset.json / paving_asset.json；原 1K 文件未删除。

brick_face_diff/rough/nor_gl/disp.jpg 是从同一组 4096×4096 红砖扫描中裁切 (2210,690) 至 (2680,855) 的砖面内部，避开灰缝。用于径向拱砖独立 UV，分辨率 470×165；不是把低清图放大到 4K，也不是教堂实拍照片的贴图。

主墙使用4K，游戏导出按最多2K生成临时副本，主工程不被降采样。
