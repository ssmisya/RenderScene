# 2026-09-14 持续核查记录

- 龙头新闻 2025-06-21 门前照片升级为 4418×2712 原图，与旧缩略图同一原照，只计一次。
- 新华社 2025-01-14 报道的圆角照片，明确影像作者张启明，但原图无拍摄 EXIF；暂作辅助，不把刊发时间冒充拍摄时间。
- Shirley 2022 砖廊近照及 Jeremyy Teh 2024 砖廊夜照，用于辨别实体拱圈、砖面、内侧灯和铁栏；不计近期门槛。
- Olivia 原文明确旅行日期 2025-02-28，37 张文章图片链接可检索。站点和图片在普通浏览器均 Access Denied，未取得可目视核查的照片；不计数。来源：https://blog.udn.com/Olivia20090408/186695146
- 蜂鸟 FNYX11414539 2025-10-04《国庆佳节随拍--索菲亚广场》文章可读，7 张图片在原网页正常浏览也全部加载失败（naturalWidth=0）；不把标题及图片数算作通过。来源：https://bbs.fengniao.com/forum/11960967.html
- ZOL 2025-05-29 六张摄影元数据可检索，原帖出现防刷验证；未绕过验证，未计数。来源：https://bbs.zol.com.cn/dcbbs/d19_142283.html

仍按固定 21 项核查范围逐项整改。脚本/模型完成、原照存在、同机位视觉通过是不同证据，不能相互替代。当前尚没有已完成全部证据链的 MATCHED 条目。


### 2026-09-14 additional structural research
- Baidu public panorama loaded successfully at 兆麟街, id `09030600121905071359384139Z`. Visible time machine offers June 2014 and May 2019; selected May 2019. Archived untouched local screenshot. Useful roof/front/street evidence, **not recent**. The 2019 guard and 2025 stair/ramp arrangements differ; do not substitute the older entrance layout for the 2025 photo.
- Jennifer / Pixnet Sophia article `https://julialkpkpk.pixnet.net/blog/post/577338464` explicitly describes mid-October travel, published 2024-12-31. Full-size public originals for market, visitor service and plaza returned HTTP 403. No image obtained, no quota credit. Image proxy domain now displays a domain-for-sale page, rejected as a source.
- note.com authors `miss_okome` (2025.6.12–15 dated itinerary) and `chweb` (2025 summer travel series): public text accessible through web search, direct origin and browser both failed SSL protocol. No matching target exterior original obtained. General food/night-market photos not counted as Sophia architecture.
- Gallery current modeling correction: first street-facing entrance stairs shifted to right opening; transverse left ramp and retaining guard added with continuous wedge collision. Second entrance retained pending its own photo evidence. Dimensions remain estimates.

- Fengniao 2025 National Day thread normal HD mode was also checked; all seven target images have natural width/height 0. Avatar loads, target photographs do not. This public-source attempt yielded no photographs and no credit.
- Technical QA caught a validator compatibility defect after adding mesh ramps: `validate_v2.py` assumed every non-box/cylinder was a polygon and raised `KeyError: points`. The native report remained stale and `report_sop90.py` correctly rejected its asset hash. Added explicit mesh projected-hull clearance; re-ran Blender with `--python-exit-code 1`, actual surface ray tests and standalone ramp walking. The stale report was never accepted or counted as photographic proof.
