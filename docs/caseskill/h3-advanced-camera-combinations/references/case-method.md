# H3 动作触发的物理运镜组合编排：方法与修复

## 导航

1. 方法来源与适用范围
2. 条件分支与冲突处理
3. 失败表现与修复
4. 迁移示例
5. 规则证据

## 方法来源与适用范围

将案例的十个固定范例转为有场地前提、阶段语义和连续性验收的运镜选择流程，同时保留人物动作主导镜头响应的局部创作纪律。

本方法由原案例文本、逐案评估和 H3 官方协议共同整理。原案经验、评估发现与本次补齐的数据/检查接口须分别表述；案例作者的成功报告不等于本次实测。原稿快照保留原貌，冲突由本文件及技能入口裁决。

- 本设计新增组合选择、continuous_phase字段、参数重定时和缺失输入状态，属于工程补齐。
- 不继承README“取消度数即可稳定”的未经对照验证的强结论。
- 14/13旧计数仅纠正为原文实际15条规则/14词条，不作为用户输出负担。

## 条件分支与冲突处理

| 条件 | 执行动作 | 案例/评估依据 |
|---|---|---|
| 没有遮挡物但选了06或09 | 改选03或01，或先让人物产生真实且时间充分的手臂/衣袖遮挡；不可凭空添加黑场掩盖跳位。 | case-studies/2026-10-advanced-camera-combinations/prompt.md:167-189,245-266；docs/casereview/2026-10-advanced-camera-combinations.md:38 |
| 段长短于物理路线所需时间 | 减少阶段和位移，保留动作触发与完整到位；不靠任意加速或省略回收路径强塞全部组合。 | docs/casereview/2026-10-advanced-camera-combinations.md:36-38（工程补齐） |
| 要求全程连续舞蹈同时选择10 | 说明静态建立与任务冲突，改用03/01，或经任务允许缩短建立段并取消无动作触发的微推进。 | case-studies/2026-10-advanced-camera-combinations/prompt.md:20,270-294；docs/casereview/2026-10-advanced-camera-combinations.md:42 |
| 输入仅给“镜头绕45度” | 把目标翻译为人物身体一侧的可识别终点，并补上路线和保持对准的部位；不推断唯一的高度/距离。 | case-studies/2026-10-advanced-camera-combinations/prompt.md:298-328 |

## 失败表现与修复

| 失败表现 | 修复步骤 | 依据 |
|---|---|---|
| 相机提前漂移或人物不动时仍追随 | 回到触发表，移除没有具体人物事件的改向；若属组合10建立镜头则明确标注例外。 | case-studies/2026-10-advanced-camera-combinations/prompt.md:17-18,270-294 |
| 遮挡结束后出现在无路径可达的一侧 | 补穿越前/后方的路径和足够时间，或将终点改为同侧新机位。 | case-studies/2026-10-advanced-camera-combinations/prompt.md:16,178-185,255-262；docs/casereview/2026-10-advanced-camera-combinations.md:38 |
| 复制一个组合后缺身份职责或开场约束 | 重新执行完整组装步骤，把所需局部公共规则并入最终段落。 | case-studies/2026-10-advanced-camera-combinations/prompt.md:5-23；docs/casereview/2026-10-advanced-camera-combinations.md:43 |
| 连续运镜被错误拆成数个硬切 | 统一使用 Phase/连续阶段及 cut_mode 声明，仅在真实切点写 hard cut。 | docs/casereview/2026-10-advanced-camera-combinations.md:28,36 |

## 迁移示例

**任务**

已有单人身份照和10秒镜头预算。舞者在2秒开始把右臂扫向镜头，场地只允许向舞者左侧移动半步；未提供音频。请设计连续遮挡揭示。

**预期处理示例**

选择06的简化版本，cut_mode=continuous_phase；音乐状态=未测量。0–2秒：镜头位于舞者正前方、对准脸与上胸，人物完成连贯胸肩动作，摄影机小幅实移靠近。2–3秒：右前臂从胸前扫过镜头形成真实遮挡，摄影机仅在遮挡形成后向舞者左侧横移半步。3–4秒：前臂移开时相机已到前左方，继续对准脸和上胸，不跳到身体后侧。4–8秒：人物打开双臂，镜头小幅后退维持构图。8–10秒：摄影机停稳，人物完成末端上臂定势，右手方向作为下一镜钩子。以上是结构性时间安排，不标为实测重拍；身份照没有实际路径时仍登记 missing。

示例是编排示范；其中任务给定参数和演算不代表当前已经读取了对应媒体，也不代表一次 H3 推理已完成。完整生成端交付仍需按输出模板选择正确字段和真实素材绑定。

## 规则证据

以下行号对应本技能来源索引中的固定快照；`review` 指 `source-review.md`。工程补齐项以其所解决的原文/评估缺口为依据，不伪称上游已实现该检查。

| 规则 | 原文或评估位置 |
|---|---|
| ACM01 | case-studies/2026-10-advanced-camera-combinations/prompt.md:4,10-18,298-328 |
| ACM02 | case-studies/2026-10-advanced-camera-combinations/prompt.md:11-16,27-39 |
| ACM03 | case-studies/2026-10-advanced-camera-combinations/prompt.md:18,40；docs/casereview/2026-10-advanced-camera-combinations.md:28,32 |
| ACM04 | docs/casereview/2026-10-advanced-camera-combinations.md:28,36（工程补齐） |
| ACM05 | case-studies/2026-10-advanced-camera-combinations/prompt.md:193-214；docs/casereview/2026-10-advanced-camera-combinations.md:42 |
| ACM06 | case-studies/2026-10-advanced-camera-combinations/prompt.md:270-294；docs/casereview/2026-10-advanced-camera-combinations.md:42（冲突处理） |
| ACM07 | case-studies/2026-10-advanced-camera-combinations/prompt.md:5,19-21；docs/casereview/2026-10-advanced-camera-combinations.md:30-32 |
| ACM08 | case-studies/2026-10-advanced-camera-combinations/prompt.md:5,9；docs/casereview/2026-10-advanced-camera-combinations.md:43-44 |

| 规则 | 文件与行号 | 支持内容 |
|---|---|---|
| ACM01 | case-studies/2026-10-advanced-camera-combinations/prompt.md：4;10-18;298-328 | 原文给出五要素并以相对人体位置改写抽象角度描述。 |
| ACM02 | case-studies/2026-10-advanced-camera-combinations/prompt.md：11-16;27-39 | 位置、距离、高度、换侧与光轴均要求物理操作。 |
| ACM03 | docs/casereview/2026-10-advanced-camera-combinations.md：28-32 | 评估明确原始秒数不等同于任意音频的实测同步。 |
| ACM04 | docs/casereview/2026-10-advanced-camera-combinations.md：28;36 | 对 SHOT 标签含混提出连续阶段/硬切显式化。 |
| ACM05 | case-studies/2026-10-advanced-camera-combinations/prompt.md：193-214 | 标题写前跟随，正文从人物后方起始；以具体正文位置建立一致路线。 |
| ACM06 | case-studies/2026-10-advanced-camera-combinations/prompt.md：270-294 | 组合10有静态建立和先行微推进，需从常规动作触发纪律中列出例外。 |
| ACM07 | docs/casereview/2026-10-advanced-camera-combinations.md：30-32 | 人数、步数、构图限制属局部规约且缺对照试验。 |
| ACM08 | docs/casereview/2026-10-advanced-camera-combinations.md：43-44 | 独立粘贴缺公共输入职责，时长与宽高比存在待澄清项。 |
