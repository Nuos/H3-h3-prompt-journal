# H3 运镜纪律选择与冲突裁决：方法与修复

## 导航

1. 方法来源与适用范围
2. 条件分支与冲突处理
3. 失败表现与修复
4. 迁移示例
5. 规则证据

## 方法来源与适用范围

把历史 E1–E10 经验与后续修订法则拆成可选择的条件规则，先裁决响应时相和剪辑策略，再据人物空间变化决定相机是否需要移动。

本方法由原案例文本、逐案评估和 H3 官方协议共同整理。原案经验、评估发现与本次补齐的数据/检查接口须分别表述；案例作者的成功报告不等于本次实测。原稿快照保留原貌，冲突由本文件及技能入口裁决。

- camera_response/edit_policy两轴、delta_t字段和路由流程是本次工程补齐，不是原文现成协议。
- 该技能先解决文本规则选择与冲突，不能由规则通过推断生成模型一定服从。
- 正文PART2实际上加入了第11项TIME-CODE SYNC，README计数不同；交付按具体规则条目检索，不依赖旧总数。

## 条件分支与冲突处理

| 条件 | 执行动作 | 案例/评估依据 |
|---|---|---|
| 踢腿向镜头且当前构图可容纳完整动作 | 选 stable_observe/Plant，让动作进入画面；不为每一次踢腿再推近。 | case-studies/2026-10-camera-movement-discipline-library/prompt.md:14,31 |
| 大队形展开后的重拍必须完整入画 | 选 anticipate_hit，在前一动作释放阶段退到所需宽景；实际提前量依据可用时间和路径，不照搬1.5–2秒。 | case-studies/2026-10-camera-movement-discipline-library/prompt.md:11-12,16,30；docs/casereview/2026-10-camera-movement-discipline-library.md:28-30 |
| 用户要求醉酒第一视角，同时要求人与镜头完全同起同落 | 指出两种响应规则冲突并按主要意图选择；若保留轻微醉酒感，用明确延迟、有限过冲和回收，移除零延迟要求。 | case-studies/2026-10-camera-movement-discipline-library/prompt.md:88-125,159-167；docs/casereview/2026-10-camera-movement-discipline-library.md:45 |
| 用户要求转身中换场 | 选 phase_match_cut，记录切前切后的同侧肩方向、转向和速度；不套用 E3 的全局动作中途禁切。 | case-studies/2026-10-camera-movement-discipline-library/prompt.md:37,77；docs/casereview/2026-10-camera-movement-discipline-library.md:30,46 |

## 失败表现与修复

| 失败表现 | 修复步骤 | 依据 |
|---|---|---|
| 每拍都推拉、横移或摇晃 | 删去没有重大空间原因的相机事件，只保留主要观看行为与必要的重新到位。 | case-studies/2026-10-camera-movement-discipline-library/README.md:9-24；case-studies/2026-10-camera-movement-discipline-library/prompt.md:203-218 |
| 延迟观察被同步规则抵消 | 移除全段同起同峰要求，保留共同时间轴并显式给出延迟和回收区间。 | case-studies/2026-10-camera-movement-discipline-library/prompt.md:88-125,159-167；docs/casereview/2026-10-camera-movement-discipline-library.md:28 |
| 静镜仍产生漂移 | 补齐 none 运动和 none permitted 触发，同时锁定终点机位，检查是否还残留浮动/跟拍词。 | case-studies/2026-10-camera-movement-discipline-library/prompt.md:191-215 |
| 旋转换场被截成动作结束后切，或跨切突然反转 | 明确 phase_match_cut，补相同肩方位、转向、速度及下一镜初始状态。 | case-studies/2026-10-camera-movement-discipline-library/prompt.md:77；docs/casereview/2026-10-camera-movement-discipline-library.md:30 |

## 迁移示例

**任务**

8秒单人舞，0–3秒连续抬臂，3–5秒人物向左转，5–8秒稳定结束；希望第一视角稍迟钝，画面仍可读。没有实际音频。

**预期处理示例**

camera_response=delayed_observer，edit_policy=continuous；所有时间为计划值，音乐同步未测。0–3秒镜头保持正前方胸高位置观察抬臂，不逐拍跟手。3秒人物开始向左转，3.25秒相机才沿人物左侧实际横移，维持脸与肩颈可见；0.25秒是明确设定的创作延迟。4.6–5.2秒出现一次小幅过冲并后退修正，5.2秒重新建立前左构图。5.2–8秒相机锁定，人物完成末端动作。五字段中的 TRIGGER 引用3秒转身，movement_start 写3.25秒，避免同时保留全段零延迟同步禁令。

示例是编排示范；其中任务给定参数和演算不代表当前已经读取了对应媒体，也不代表一次 H3 推理已完成。完整生成端交付仍需按输出模板选择正确字段和真实素材绑定。

## 规则证据

以下行号对应本技能来源索引中的固定快照；`review` 指 `source-review.md`。工程补齐项以其所解决的原文/评估缺口为依据，不伪称上游已实现该检查。

| 规则 | 原文或评估位置 |
|---|---|
| CMD01 | case-studies/2026-10-camera-movement-discipline-library/README.md:14-24；case-studies/2026-10-camera-movement-discipline-library/prompt.md:151-157,203-218 |
| CMD02 | case-studies/2026-10-camera-movement-discipline-library/prompt.md:11-12,88-125,159-167；docs/casereview/2026-10-camera-movement-discipline-library.md:28,38-45 |
| CMD03 | case-studies/2026-10-camera-movement-discipline-library/prompt.md:36-41,64-77；docs/casereview/2026-10-camera-movement-discipline-library.md:30,46 |
| CMD04 | case-studies/2026-10-camera-movement-discipline-library/prompt.md:191-201 |
| CMD05 | case-studies/2026-10-camera-movement-discipline-library/prompt.md:50-62,135-148 |
| CMD06 | case-studies/2026-10-camera-movement-discipline-library/prompt.md:88-125 |
| CMD07 | case-studies/2026-10-camera-movement-discipline-library/prompt.md:8-19,64-86；docs/casereview/2026-10-camera-movement-discipline-library.md:30-32 |
| CMD08 | docs/casereview/2026-10-camera-movement-discipline-library.md:32,47 |

| 规则 | 文件与行号 | 支持内容 |
|---|---|---|
| CMD01 | case-studies/2026-10-camera-movement-discipline-library/README.md：14-24;75-93 | 主要观看行为及重大空间触发为修订的核心纪律。 |
| CMD02 | case-studies/2026-10-camera-movement-discipline-library/prompt.md：11-12;88-125;159-167 | 提前、延迟和零延迟同步同时存在，必须条件化。 |
| CMD03 | case-studies/2026-10-camera-movement-discipline-library/prompt.md：36-41;64-77 | 收势切和旋转中相位匹配切属于不同情境。 |
| CMD04 | case-studies/2026-10-camera-movement-discipline-library/prompt.md：191-201 | 五字段与显式零移动为原文接口要求。 |
| CMD05 | case-studies/2026-10-camera-movement-discipline-library/prompt.md：50-62;135-148 | 特殊机位物理化及其适用边界。 |
| CMD06 | case-studies/2026-10-camera-movement-discipline-library/prompt.md：88-125 | 人物稳定、摄影机迟滞—过冲—修正—重新构图。 |
| CMD07 | docs/casereview/2026-10-camera-movement-discipline-library.md：28-32 | 评估要求保留历史参数的局部情境。 |
| CMD08 | docs/casereview/2026-10-camera-movement-discipline-library.md：32;47 | 目录不含支持稳定性结论的可重放实验记录。 |
