# 道具脱离、触镜与局部扇风的连续动作链：方法与修复

## 导航

1. 方法来源与适用范围
2. 条件分支与冲突处理
3. 失败表现与修复
4. 迁移示例
5. 规则证据

## 方法来源与适用范围

把动作名清单改成“起态→动作→结果→下一态”的有条件动作表，保持实体身份与所有权，区分永久身份和阶段性姿态，补足音乐事件、时长预算及错误动作主体。

本方法由原案例文本、逐案评估和 H3 官方协议共同整理。原案经验、评估发现与本次补齐的数据/检查接口须分别表述；案例作者的成功报告不等于本次实测。原稿快照保留原貌，冲突由本文件及技能入口裁决。

- 全部4个案例文本和review已完整阅读；本地成片未分发，本次未读取或核验。README所列15.08秒、24fps是作者描述，不是本次测量。
- 永久身份与暂时状态分开；袜、人物、服装、空间可替换，动作前提和道具归属仍需重新设计。
- 动作状态表是自然语言计划，不是物理引擎、手势识别或逐帧自动验收。
- 脚本检查仅验证计划数据；真实布料、触镜与关节运动仍靠生成后审片。

## 条件分支与冲突处理

| 条件 | 执行动作 | 案例/评估依据 |
|---|---|---|
| 新参考图左右脚与原案相反 | 根据图像重映射角色，例如LEFT_FOOT为抬起穿袜脚、RIGHT_FOOT为支撑脚，并同步修改全部移除、悬空、落脚和裸足规则。 | case-studies/2026-09-action-chain-sock-fan-comedy/prompt.txt:19–44 |
| 没有实际音轨但有15秒目标 | 输出音头为missing的时间预算，不把ACCENT编号当作测量；必要时删重复扇风/加速循环或扩展创作长度。 | docs/casereview/2026-09-action-chain-sock-fan-comedy.md:29,40 |
| 文字要求左脚始终不动又要左右脚tap | 把在地支撑限制限定到移除—触镜下落阶段，双脚落稳后显式进入舞步阶段。 | docs/casereview/2026-09-action-chain-sock-fan-comedy.md:41 |
| 投掷和落地一段过密 | 保留投掷→接触→下落→落脚的先后，减少可选反应或重复步法；跨片分割时选择落稳后的状态，避免隐藏中间事件。 | case-studies/2026-09-action-chain-sock-fan-comedy/prompt.txt:235–287；docs/casereview/2026-09-action-chain-sock-fan-comedy.md:40 |

## 失败表现与修复

| 失败表现 | 修复步骤 | 依据 |
|---|---|---|
| 脱下的袜子消失、重新出现在脚上或换手 | 在相邻状态写清道具所有者、穿戴变化与物体位置；双手协作结束后固定持物手的解剖身份。 | case-studies/2026-09-action-chain-sock-fan-comedy/prompt.txt:70–111,484–515 |
| 袜子还没触镜，抬起脚已落下 | 把下降门槛写为触镜完成且下落已开始，单独给反弹/下落可辨认时段。 | case-studies/2026-09-action-chain-sock-fan-comedy/prompt.txt:235–266 |
| 用全臂大甩代替掌部扇风 | 保留投掷随挥终态，逐级指定肩上臂肘前臂稳定，腕为主动关节，掌在近似同高左右摆。 | case-studies/2026-09-action-chain-sock-fan-comedy/prompt.txt:300–370 |
| 全程左脚不动与后段左脚tap冲突 | 拆分单腿支撑、双脚落稳、舞步三阶段；保留解剖身份与赤脚属性，撤销过期的在地不动约束。 | docs/casereview/2026-09-action-chain-sock-fan-comedy.md:41 |
| 15秒内动作闪过、重音顺序无法兑现 | 先预算移除和接触链的最小可读时段，减少重复舞步或扩展故事并分片；未测音轨先标missing。 | docs/casereview/2026-09-action-chain-sock-fan-comedy.md:29,40 |
| 正文写成手看袜子 | 改成“人物的视线再次落到该手持有的袜子”，保留手臂投掷准备作为另一个动作。 | case-studies/2026-09-action-chain-sock-fan-comedy/vocabulary-expanded.zh-CN.md:107 |

## 迁移示例

**任务**

现代排练室成年男舞者，参考图左脚抬起穿条纹袜、右脚赤脚支撑；做18秒闻袜嫌弃、扔向镜头、落脚后手掌扇风的喜剧，不指定原案服装。

**预期处理示例**

先重映射：LEFT_FOOT=抬起穿袜脚，RIGHT_FOOT=赤脚支撑脚；RIGHT_HAND在双手脱袜后持物并投掷，LEFT_HAND随后捂嘴。18秒故事分两段9秒：A段0–2秒双手脱袜，2–3秒右手持袜并由人物看袜，3–4秒靠鼻短闻一次，4–5秒移开袜子、眼神反应且左手捂嘴，5–6秒右臂准备，6–7秒释放并随挥、袜子逼近镜头，7–7.5秒轻触，7.5–8秒反弹且开始下落，8–9秒此时才让左裸脚下降并落稳。B段0–1秒承接双脚赤脚、左手捂嘴、右臂前伸的末态，1–3秒腕掌往返扇风，3–5秒右脚tap后左脚tap并小幅换重，5–7秒适度加快，7–8秒最后一次较大掌摆，8–9秒保持。右脚“不得离地”的规则只管A段单腿支撑，不影响B段tap。没有音轨，audio/onsets=missing，以上时间是创作预算；若触镜到落地不可辨认，延长该部分并减少B段循环，不同时完成全部事件。生成片段均在官方4–15秒范围内；是否成功仍需实际审片。

示例是编排示范；其中任务给定参数和演算不代表当前已经读取了对应媒体，也不代表一次 H3 推理已完成。完整生成端交付仍需按输出模板选择正确字段和真实素材绑定。

## 规则证据

以下行号对应本技能来源索引中的固定快照；`review` 指 `source-review.md`。工程补齐项以其所解决的原文/评估缺口为依据，不伪称上游已实现该检查。

| 规则 | 原文或评估位置 |
|---|---|
| S1 | case-studies/2026-09-action-chain-sock-fan-comedy/prompt.txt:19–44 |
| S2 | case-studies/2026-09-action-chain-sock-fan-comedy/README.md:34–57 |
| S3 | case-studies/2026-09-action-chain-sock-fan-comedy/prompt.txt:484–499；docs/casereview/2026-09-action-chain-sock-fan-comedy.md:27,41 |
| S4 | case-studies/2026-09-action-chain-sock-fan-comedy/prompt.txt:187–266 |
| S5 | case-studies/2026-09-action-chain-sock-fan-comedy/prompt.txt:300–426 |
| S6 | docs/casereview/2026-09-action-chain-sock-fan-comedy.md:41 |
| S7 | case-studies/2026-09-action-chain-sock-fan-comedy/vocabulary-expanded.zh-CN.md:107 |
| S8 | docs/casereview/2026-09-action-chain-sock-fan-comedy.md:29,39–40 |
| S9 | case-studies/2026-09-action-chain-sock-fan-comedy/vocabulary-expanded.zh-CN.md:111 |

| 规则 | 文件与行号 | 支持内容 |
|---|---|---|
| S1 | case-studies/2026-09-action-chain-sock-fan-comedy/prompt.txt：19–44 | 定义解剖脚身份及袜子移除后的状态变化。 |
| S2 | case-studies/2026-09-action-chain-sock-fan-comedy/README.md：34–57 | 上一动作结束态连接下一起态，明确物体归属。 |
| S3 | docs/casereview/2026-09-action-chain-sock-fan-comedy.md：27,41 | 评估指出两手没有绑定解剖学左右，需要在技能输入补齐。 |
| S4 | case-studies/2026-09-action-chain-sock-fan-comedy/prompt.txt：187–266 | 释放、飞行、触镜、反弹下落后右脚才下降。 |
| S5 | case-studies/2026-09-action-chain-sock-fan-comedy/prompt.txt：300–426 | 腕掌主动、近端稳定，同时允许后续下身节奏。 |
| S6 | docs/casereview/2026-09-action-chain-sock-fan-comedy.md：41 | 永久在地与左脚tap矛盾，应改为阶段规则。 |
| S7 | case-studies/2026-09-action-chain-sock-fan-comedy/vocabulary-expanded.zh-CN.md：107 | 明确标出“持袜手看袜子”的主语错误。 |
| S8 | docs/casereview/2026-09-action-chain-sock-fan-comedy.md：29,39–40 | 重音只是标签，缺实际onset与逐态时间预算。 |
| S9 | case-studies/2026-09-action-chain-sock-fan-comedy/vocabulary-expanded.zh-CN.md：111 | 文字25态不能当作生成结果完成的证据。 |
