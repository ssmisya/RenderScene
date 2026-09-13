> 当前离线验证针对 V2.1.0，临时测试 blend 在成功渲染后删除。

# 离线可移植性检查

把主工程复制到项目内不含 assets 目录的隔离子目录，检查各图片的相邻外部路径确实不存在，再用内嵌资源实际渲染夜景。

`offline_validation.json` 是结果，`offline/NIGHT_Portability.png` 是低分辨率验证帧，不是最终交付成片。

验证用的 `.blend` 是临时副本，可能在验证后清理；当前工作版本始终是项目根目录的 `Harbin_Sophia_Square.blend`。
