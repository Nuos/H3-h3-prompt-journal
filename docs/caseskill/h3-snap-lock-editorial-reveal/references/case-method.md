# H3 音频事件驱动的快照与硬锁：方法与修复

## 导航

1. 方法来源与适用范围
2. 条件分支与冲突处理
3. 失败表现与修复
4. 迁移示例
5. 规则证据

## 方法来源与适用范围

将案例5.30秒固定事件表转为带帧边界、相机状态、构图和绝对取向的编排方法，同时保留源文翻译分歧、帧预算不足与旋转累积歧义。

本方法由原案例文本、逐案评估和 H3 官方协议共同整理。原案经验、评估发现与本次补齐的数据/检查接口须分别表述；案例作者的成功报告不等于本次实测。原稿快照保留原貌，冲突由本文件及技能入口裁决。

- 帧状态表、绝对roll字段和不足预算的blocked处理属于工程补齐。
- 角度数用于本案例roll参考系的可核对定义，不把其他运镜库的局部无度数规则强加此处。
- 新输入若禁怼脸，保留肩颈和身份可读性，不能因源例极端face burst而覆盖用户要求。

## 条件分支与冲突处理

| 条件 | 执行动作 | 案例/评估依据 |
|---|---|---|
| 新任务要求中段+90度、结尾再+90度且最终仍+90度 | 列出累计+180的矛盾，让目标取向与相对旋转二选一或重新设计前段取向；不得默默补回正动作。 | case-studies/2026-09-snap-lock-editorial-reveal/prompt.md:105,277,404-420；docs/casereview/2026-09-snap-lock-editorial-reveal.md:40 |
| 24fps下坚持0.08秒三个可数冲击 | 标记帧预算不足，给出可调整的冲击数/窗口/fps方案；不把文字中的三次当成视频中已实现三次。 | case-studies/2026-09-snap-lock-editorial-reveal/prompt.md:320-345；case-studies/2026-09-snap-lock-editorial-reveal/vocabulary-expanded.zh-CN.md:107 |
| 用户偏好连续平滑上摇 | 明确其属于另一运镜机制，不把全程平滑运动塞入本两态严格快照方案。 | case-studies/2026-09-snap-lock-editorial-reveal/prompt.md:10-19,464-478 |
| 仅提供一张图片，没有音频 | 可交付未绑定音频的构图状态草案；时间标planned并保留audio missing，不宣称已完成原例音乐同步。 | case-studies/2026-09-snap-lock-editorial-reveal/README.md:5-12,128；case-studies/2026-09-snap-lock-editorial-reveal/prompt.md:82-102 |

## 失败表现与修复

| 失败表现 | 修复步骤 | 依据 |
|---|---|---|
| 足部到面部变成匀速上摇 | 逐段明确离散构图和不可运动的LOCK窗口，检查是否同时存在continuous tilt/upward travel指令。 | case-studies/2026-09-snap-lock-editorial-reveal/prompt.md:164-225,464-478 |
| 静镜仍慢推或残留视差 | 定位前一burst的结束帧，缩短或重设运动窗口，不将速度渐降占进LOCK；回到固定构图和清晰主体。 | case-studies/2026-09-snap-lock-editorial-reveal/prompt.md:20-53,479-488 |
| 相机roll被实现为人物横躺或脸变形 | 把camera_roll和body_orientation分列，检查背景水平基准随相机变化，人物结构不变。 | case-studies/2026-09-snap-lock-editorial-reveal/prompt.md:103-120,340-343；case-studies/2026-09-snap-lock-editorial-reveal/vocabulary-expanded.zh-CN.md:43-59 |
| 三冲击在两帧内糊成一次抖动 | 回到帧预算修改冲击设计，保留独立事件和恢复，而非增加“清晰三次”字样。 | case-studies/2026-09-snap-lock-editorial-reveal/prompt.md:320-345；docs/casereview/2026-09-snap-lock-editorial-reveal.md:27 |

## 迁移示例

**任务**

做一个新的6秒揭示：所有前段画面直立，末段转成顺时针横置；30fps，用户已指定0、1、2、3、5秒音频事件，肩颈需始终保留在上身/脸部画面，不要极端怼脸。

**预期处理示例**

图像管身份/环境，音频事件标用户提供待核验。0–0.2秒burst进入鞋部构图，0.2–1秒LOCK；1–1.2秒burst到膝部，1.2–2秒LOCK；2–2.2秒burst到含肩颈的上身构图，2.2–3秒LOCK；3–3.2秒burst到含肩颈的人物近景，3.2–5秒LOCK，期间仅按指定事件安排闭眼。5–5.3秒眼睛睁开，同时camera_roll_abs从0到+90度，人物不转；5.3–6秒LOCK。所有窗口映射为30fps帧数，未加入原例0.08秒三冲击；这是按新输入改编的两态方案，保留了明确最终朝向而没有继承源两次90度累积矛盾。

示例是编排示范；其中任务给定参数和演算不代表当前已经读取了对应媒体，也不代表一次 H3 推理已完成。完整生成端交付仍需按输出模板选择正确字段和真实素材绑定。

## 规则证据

以下行号对应本技能来源索引中的固定快照；`review` 指 `source-review.md`。工程补齐项以其所解决的原文/评估缺口为依据，不伪称上游已实现该检查。

| 规则 | 原文或评估位置 |
|---|---|
| SLR01 | case-studies/2026-09-snap-lock-editorial-reveal/prompt.md:9-53,448-504 |
| SLR02 | case-studies/2026-09-snap-lock-editorial-reveal/prompt.md:346-395；case-studies/2026-09-snap-lock-editorial-reveal/vocabulary-expanded.zh-CN.md:20,91,103 |
| SLR03 | case-studies/2026-09-snap-lock-editorial-reveal/prompt.md:1-8,82-102,505-522；docs/casereview/2026-09-snap-lock-editorial-reveal.md:27 |
| SLR04 | case-studies/2026-09-snap-lock-editorial-reveal/prompt.md:103-120,273-277,404-429；case-studies/2026-09-snap-lock-editorial-reveal/vocabulary-expanded.zh-CN.md:105 |
| SLR05 | case-studies/2026-09-snap-lock-editorial-reveal/prompt.md:320-345；case-studies/2026-09-snap-lock-editorial-reveal/vocabulary-expanded.zh-CN.md:107；docs/casereview/2026-09-snap-lock-editorial-reveal.md:27,40 |
| SLR06 | case-studies/2026-09-snap-lock-editorial-reveal/prompt.md:41-53；case-studies/2026-09-snap-lock-editorial-reveal/prompt.zh-CN.md:44,83,104,134；docs/casereview/2026-09-snap-lock-editorial-reveal.md:29,39 |
| SLR07 | case-studies/2026-09-snap-lock-editorial-reveal/prompt.md:10-19,464-478；case-studies/2026-09-snap-lock-editorial-reveal/README.md:14-37 |
| SLR08 | case-studies/2026-09-snap-lock-editorial-reveal/README.md:90-99；docs/casereview/2026-09-snap-lock-editorial-reveal.md:25,31 |

| 规则 | 文件与行号 | 支持内容 |
|---|---|---|
| SLR01 | case-studies/2026-09-snap-lock-editorial-reveal/prompt.md：9-53;448-504 | 两态定义与运动不能泄漏时间窗口。 |
| SLR02 | case-studies/2026-09-snap-lock-editorial-reveal/vocabulary-expanded.zh-CN.md：20;91;103 | 硬锁摄影机与后期定格单帧的区别。 |
| SLR03 | case-studies/2026-09-snap-lock-editorial-reveal/prompt.md：1-8;82-102;505-522 | 图像视觉权威和音频时序权威分离。 |
| SLR04 | case-studies/2026-09-snap-lock-editorial-reveal/vocabulary-expanded.zh-CN.md：43-59;105 | 角度参考系和两次90度累积歧义。 |
| SLR05 | docs/casereview/2026-09-snap-lock-editorial-reveal.md：27;40 | 冲击帧数和可读性仍须确定。 |
| SLR06 | case-studies/2026-09-snap-lock-editorial-reveal/prompt.zh-CN.md：44;83;104;134 | 中文版本增加与英文即时两态不同的物理和加减速叙述。 |
| SLR07 | case-studies/2026-09-snap-lock-editorial-reveal/prompt.md：10-19;464-478 | 离散构图不应被平滑连接为连续旅程。 |
| SLR08 | docs/casereview/2026-09-snap-lock-editorial-reveal.md：25;31 | 源片采样建议和生成效果不构成唯一反推证明。 |
