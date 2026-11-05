# H3 右入单状态展示与硬切装配：方法与修复

## 导航

1. 方法来源与适用范围
2. 条件分支与冲突处理
3. 失败表现与修复
4. 迁移示例
5. 规则证据

## 方法来源与适用范围

把状态目录、独立生成任务和音频对位编辑分开，保留源案例经反推修订后的真实结构，并让首帧状态、切点两侧内容和可变属性成为可检查契约。

本方法由原案例文本、逐案评估和 H3 官方协议共同整理。原案经验、评估发现与本次补齐的数据/检查接口须分别表述；案例作者的成功报告不等于本次实测。原稿快照保留原貌，冲突由本文件及技能入口裁决。

- 状态参数化、生成/编辑双时长、帧号与候选处置表是工程补齐。
- 源README同时有“切点两侧都在迈步”与“pose中切走”，以最终prompt的具体首尾状态裁决。
- 原4.4秒候选的处置证据未归档，必须保持unknown，不擅自判为误报。

## 条件分支与冲突处理

| 条件 | 执行动作 | 案例/评估依据 |
|---|---|---|
| 出现上一状态未消失、下一状态已进场 | 检查是否错误合并成一个生成任务；恢复独立片段，各段仅一个当前状态，后期直接硬切。 | case-studies/2026-10-sock-showcase-right-entry-three-shot/README.md:14-15,24-26 |
| 用户要求真正的一镜到底画内连续变装 | 说明这与本技能独立任务/硬切结构不同，转给事件触发或连续变装流程，不把跳切伪称无缝单镜。 | case-studies/2026-10-sock-showcase-right-entry-three-shot/README.md:24-26；docs/casereview/2026-10-sock-showcase-right-entry-three-shot.md:32 |
| 短片段不满足当前工作流最小时长 | 设计生成余量与可用区间，分别记录generation_duration和edit_duration；核查裁后首尾动作再装配。 | docs/casereview/2026-10-sock-showcase-right-entry-three-shot.md:39（工程补齐） |
| 需要复现源片标签 | 开启文字层，把主题横幅与镜头编号作为后期文字轨按状态同步切换；无文字任务则整体省略。 | case-studies/2026-10-sock-showcase-right-entry-three-shot/README.md:16,32-38 |

## 失败表现与修复

| 失败表现 | 修复步骤 | 依据 |
|---|---|---|
| 一次生成三种袜子并出现多人重影 | 按状态拆为三个独立任务，不给单段前后look变化指令。 | case-studies/2026-10-sock-showcase-right-entry-three-shot/README.md:15,24-26 |
| 人物从左走出、画面空置后才出现下个状态 | 删除走出与清屏；保留当前pose到末帧，下一镜首帧新look右入，交由剪辑硬切。 | case-studies/2026-10-sock-showcase-right-entry-three-shot/README.md:14,22-26；case-studies/2026-10-sock-showcase-right-entry-three-shot/prompt.md:4 |
| 把pose→跨步拼接写成跨步中无缝续接 | 以三个最终prompt的末帧与首帧描述为准，显式标visible jump cut。 | case-studies/2026-10-sock-showcase-right-entry-three-shot/prompt.md:25,52,79；docs/casereview/2026-10-sock-showcase-right-entry-three-shot.md:43 |
| 源服装、厨房或字幕被一起继承 | 只借编辑结构，场景/身份取当前资产，袜饰为明确变量，文字由开关决定。 | case-studies/2026-10-sock-showcase-right-entry-three-shot/README.md:28-38,52；case-studies/2026-10-sock-showcase-right-entry-three-shot/prompt.md:5,27 |

## 迁移示例

**任务**

目标剪辑时间线为30fps、9秒，展示三种不同纹理长袜；H3按官方标准24FPS生成，固定服装和摄影机，无文字；编辑切点计划3秒和6秒，音频后期整轨铺底。

**预期处理示例**

建立A/B/C三个独立生成任务，每个generation_duration=4秒、24FPS；各自edit_duration=3秒，计划保留源窗口[0,3)秒并记录实际保留帧[0,72)，第3–4秒为生成余量。每段首帧已有新状态并处于从画右入场的大跨步；0–0.5秒继续入场，0.5–2秒完成落定与不同短pose，2–4秒保持pose，以保证3秒裁切边界仍在pose内。没有走出或清屏。编辑表：A全局0–3秒、B3–6秒、C6–9秒；输出30fps对应第90/180帧，源24FPS帧号另列，不宣称H3原生30FPS能力。前一镜末帧为pose、后一镜首帧为新状态跨步，保留可见跳切。生成后检视计划窗口，若需要改窗，记录实际in/out并保证仍覆盖首帧跨步及末帧pose。原音轨只在最终9秒时间线上铺一次；切点属于用户计划，未测音频时不标为实测重拍。

示例是编排示范；其中任务给定参数和演算不代表当前已经读取了对应媒体，也不代表一次 H3 推理已完成。完整生成端交付仍需按输出模板选择正确字段和真实素材绑定。

## 规则证据

以下行号对应本技能来源索引中的固定快照；`review` 指 `source-review.md`。工程补齐项以其所解决的原文/评估缺口为依据，不伪称上游已实现该检查。

| 规则 | 原文或评估位置 |
|---|---|
| SRE01 | case-studies/2026-10-sock-showcase-right-entry-three-shot/README.md:20-26,40-44；case-studies/2026-10-sock-showcase-right-entry-three-shot/prompt.md:3-5,17-27,44-54,71-81 |
| SRE02 | case-studies/2026-10-sock-showcase-right-entry-three-shot/prompt.md:25,52,79；docs/casereview/2026-10-sock-showcase-right-entry-three-shot.md:43 |
| SRE03 | case-studies/2026-10-sock-showcase-right-entry-three-shot/prompt.md:5,15-25,42-52,69-79；docs/casereview/2026-10-sock-showcase-right-entry-three-shot.md:44 |
| SRE04 | case-studies/2026-10-sock-showcase-right-entry-three-shot/README.md:14-15,22-26；case-studies/2026-10-sock-showcase-right-entry-three-shot/prompt.md:27,54,81 |
| SRE05 | case-studies/2026-10-sock-showcase-right-entry-three-shot/prompt.md:3,90-98；docs/casereview/2026-10-sock-showcase-right-entry-three-shot.md:31 |
| SRE06 | case-studies/2026-10-sock-showcase-right-entry-three-shot/README.md:13；docs/casereview/2026-10-sock-showcase-right-entry-three-shot.md:29,33,45 |
| SRE07 | case-studies/2026-10-sock-showcase-right-entry-three-shot/prompt.md:9,36,63；docs/casereview/2026-10-sock-showcase-right-entry-three-shot.md:39 |
| SRE08 | case-studies/2026-10-sock-showcase-right-entry-three-shot/README.md:32-34；docs/casereview/2026-10-sock-showcase-right-entry-three-shot.md:5,32 |

| 规则 | 文件与行号 | 支持内容 |
|---|---|---|
| SRE01 | case-studies/2026-10-sock-showcase-right-entry-three-shot/prompt.md：3-5;17-27;44-54;71-81 | 每镜首帧新状态与跨步入场的独立任务接口。 |
| SRE02 | docs/casereview/2026-10-sock-showcase-right-entry-three-shot.md：43 | 采用最终prompt的pose→跨步边界修复README冲突。 |
| SRE03 | docs/casereview/2026-10-sock-showcase-right-entry-three-shot.md：44 | 图像权威需保留当前袜饰变更例外。 |
| SRE04 | case-studies/2026-10-sock-showcase-right-entry-three-shot/README.md：14-15;22-26 | 走出清屏是被撤销的过度设计。 |
| SRE05 | case-studies/2026-10-sock-showcase-right-entry-three-shot/prompt.md：3;90-98 | 独立生成与原轨后期铺底是不同步骤。 |
| SRE06 | docs/casereview/2026-10-sock-showcase-right-entry-three-shot.md：29;33;45 | 阈值与候选点缺少足够复核记录，不能硬编码或编造处置原因。 |
| SRE07 | docs/casereview/2026-10-sock-showcase-right-entry-three-shot.md：39 | 源短片段时长不是当前调用能力证明。 |
| SRE08 | docs/casereview/2026-10-sock-showcase-right-entry-three-shot.md：5;32 | 状态展示策略有适用边界。 |
