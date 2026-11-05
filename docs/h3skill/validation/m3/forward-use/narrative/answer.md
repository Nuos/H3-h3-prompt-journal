# 水上闯关：独立 M3.1 空间提案

**结论：采用一个世界框架、一个场景、五个连续赛道区域。** 本提案只依据案例文字，属于可修改的定性拓扑设计。

## 坐标与区域

设计框架 `F_course`：原点取起跑平台的赛道入口参考点；+X 指起跑端朝终点端的总体纵向，+Y 仅作横向命名，+Z 向上。单位为 `arbitrary`，不提供数值坐标、长度或摄影投影。纵向次序不等于实测共线；世界左右也不能换算为画面左右。

| 次序 | 稳定区域 ID | 空间约束 |
|---|---|---|
| 1 | `R_start` | 起跑平台 |
| 2 | `R_rollers` | 第一段滚筒障碍 |
| 3 | `R_fishbone` | Fishbone 及其摔倒平台 |
| 4 | `R_runway` | 同一赛道的连接跑道 |
| 5 | `R_wall` | 终点曲墙及抓握上缘 |

相邻区域按表中顺序建立四条向前连接；`passable` 与 `traversable` 仅记录文字要求的可通过性。Fishbone 摔倒不离开其平台；墙顶只保留抓握边缘，不补建站立平台。曲墙侧邻同一比赛泳池，末端落水和随后浮出仍在该泳池；水域关系写入终点区域说明，不建立普通步行连接。

## 依据与保留项

情节依据为 `case-studies/2026-08-water-obstacle-variety-show/prompt.md` 的 summary、retention_analysis 及 Shot 2–8；`README.md` 的 Inputs 与 The breakthrough 补充参考图用途和锚点范围。坐标轴、区域划分和连接表示是本次设计决定，已在请求来源中与案例文字分开标记；Picture 1 不作为场地依据。

尺寸、间距、高差、净空、机关安装点、实际落水侧与精确落点、镜头位置和投影全部未知。当前只提出空间结构，不新增剧情或运行其他核心模块。合同检查只能确认结构与请求一致性，不能确认视频效果、物理可行性或全局完成状态。

实跑 `route request`、`check request`、`check proposal --request request` 均返回 `0`，`local_contract=pass`，`overall=unverified`；实际命令、结果和读取文件 SHA256 已随附。
