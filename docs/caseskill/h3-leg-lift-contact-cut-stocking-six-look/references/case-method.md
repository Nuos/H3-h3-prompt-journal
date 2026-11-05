# H3 触地事件驱动的服饰硬切：方法与修复

## 导航

1. 方法来源与适用范围
2. 条件分支与冲突处理
3. 失败表现与修复
4. 迁移示例
5. 规则证据

## 方法来源与适用范围

把时间戳和物理事件同时写入可核对的服饰状态转换表，让旧外观在空中和下降段持续、新外观在接触时切入且有稳定展示时间。

本方法由原案例文本、逐案评估和 H3 官方协议共同整理。原案经验、评估发现与本次补齐的数据/检查接口须分别表述；案例作者的成功报告不等于本次实测。原稿快照保留原貌，冲突由本文件及技能入口裁决。

- 帧率映射、最小保持帧数、声音策略和完整尾段是工程补齐；没有视频生成结果时仅验证规划。
- 袜饰枚举、固定单腿支撑和具体接触时刻是此案例局部内容，不扩展成所有服装/道具切换的统一限制。

## 条件分支与冲突处理

| 条件 | 执行动作 | 案例/评估依据 |
|---|---|---|
| 没有动作视频，但知道接触事件和姿态 | 删除Video1引用，写明自给的支撑/活动腿机制及事件表，继续作为无视频参考版本。 | case-studies/2026-10-leg-lift-contact-cut-stocking-six-look/README.md:48；docs/casereview/2026-10-leg-lift-contact-cut-stocking-six-look.md:44 |
| 相邻两次接触过密 | 优先减小抬腿幅度或减少转换次数，再考虑延长片段；不能取消可见保持或让cut与next_lift重合。 | case-studies/2026-10-leg-lift-contact-cut-stocking-six-look/prompt.md:60-76；docs/casereview/2026-10-leg-lift-contact-cut-stocking-six-look.md:39 |
| 用户只要求换一种袜纹，却写“服装完全不变” | 保留固定服装属性并把袜纹列为唯一明确例外，其余身份、鞋、场景和机位保持。 | case-studies/2026-10-leg-lift-contact-cut-stocking-six-look/prompt.md:110-123,604-618；docs/casereview/2026-10-leg-lift-contact-cut-stocking-six-look.md:29,46 |
| 源视频是渐变换装而目标要触地硬切 | 继承点地节奏和动作机制，显式抛弃渐变形式；用事件状态转换实现目标编辑语义。 | case-studies/2026-10-leg-lift-contact-cut-stocking-six-look/README.md:17,42-44 |

## 失败表现与修复

| 失败表现 | 修复步骤 | 依据 |
|---|---|---|
| 脚还悬空时袜纹已经改变 | 检查切点绑定是否写成时间触发而非首接触事件，将旧look延续到下降结束，并记录实际接触/切换帧差。 | case-studies/2026-10-leg-lift-contact-cut-stocking-six-look/prompt.md:37-58,707-719 |
| 换装和下一次抬腿黏在一起 | 增加明确hold_end与next_lift顺序，保留足够可见保持帧，新look在离地前已经完成硬切。 | case-studies/2026-10-leg-lift-contact-cut-stocking-six-look/prompt.md:60-76,321-359 |
| 支持腿换位或髋突然偏移 | 恢复固定支持脚和主要承重锚，压低活动腿动作幅度并检查切前切后姿态一致。 | case-studies/2026-10-leg-lift-contact-cut-stocking-six-look/prompt.md:131-185,604-618 |
| 时间线到4.69秒结束但文件目标5.17秒 | 补稳定尾段并按fps报告实际总帧数；不留下未定义尾部让模型重新变装。 | docs/casereview/2026-10-leg-lift-contact-cut-stocking-six-look.md:43 |

## 迁移示例

**任务**

成人服装展示，目标剪辑时间线为30fps、8秒；H3使用官方标准24FPS生成8秒。保留人物/鞋/背景，只展示三次袜纹变化；接触计划在2、4、6秒，原音轨已含三声触地。

**预期处理示例**

状态总数为4：LOOK0初态，LOOK1/2/3分别计划在t=2/4/6秒切换。H3标准24FPS生成对应第48/96/144帧；目标30fps编辑时间线对应第60/120/180帧，两套帧号均采用零基t=f/fps约定，不混用。若要求直接30FPS生成，须有当前运行时的verified-custom证据。每轮示例起抬在接触前0.4秒，接触后展示到2.3/4.3/6.3秒附近；先在24FPS源上按可实现的整帧边界记录实际保持时长，转为30fps后重新检查，不能承诺生成恰好9个原生帧。未见实际音轨时事件标用户给定待核验。远腿维持主要承重，近腿轻抬后直接落回原接触位置；旧袜纹保持到接触前一帧，接触帧立即硬切新纹理。6.3–8秒保留LOOK3稳定尾段。原音轨直接保留，不额外叠加鞋声或夜景环境声；生成后分别比较实际接触帧、切换帧及声音事件。

示例是编排示范；其中任务给定参数和演算不代表当前已经读取了对应媒体，也不代表一次 H3 推理已完成。完整生成端交付仍需按输出模板选择正确字段和真实素材绑定。

## 规则证据

以下行号对应本技能来源索引中的固定快照；`review` 指 `source-review.md`。工程补齐项以其所解决的原文/评估缺口为依据，不伪称上游已实现该检查。

| 规则 | 原文或评估位置 |
|---|---|
| LCC01 | case-studies/2026-10-leg-lift-contact-cut-stocking-six-look/prompt.md:37-106,221-231,679-739 |
| LCC02 | case-studies/2026-10-leg-lift-contact-cut-stocking-six-look/prompt.md:43-78,187-219,577-602 |
| LCC03 | case-studies/2026-10-leg-lift-contact-cut-stocking-six-look/prompt.md:19-35,131-185,604-638 |
| LCC04 | case-studies/2026-10-leg-lift-contact-cut-stocking-six-look/prompt.md:108,187-219；docs/casereview/2026-10-leg-lift-contact-cut-stocking-six-look.md:44 |
| LCC05 | docs/casereview/2026-10-leg-lift-contact-cut-stocking-six-look.md:31,37-45 |
| LCC06 | case-studies/2026-10-leg-lift-contact-cut-stocking-six-look/README.md:3,50；case-studies/2026-10-leg-lift-contact-cut-stocking-six-look/prompt.md:563-575；docs/casereview/2026-10-leg-lift-contact-cut-stocking-six-look.md:43 |
| LCC07 | case-studies/2026-10-leg-lift-contact-cut-stocking-six-look/README.md:48-50；case-studies/2026-10-leg-lift-contact-cut-stocking-six-look/prompt.md:297-307,620-638；docs/casereview/2026-10-leg-lift-contact-cut-stocking-six-look.md:31,46 |
| LCC08 | case-studies/2026-10-leg-lift-contact-cut-stocking-six-look/README.md:17,42-48；case-studies/2026-10-leg-lift-contact-cut-stocking-six-look/prompt.md:5,119-120；docs/casereview/2026-10-leg-lift-contact-cut-stocking-six-look.md:33,44 |
| LCC09 | case-studies/2026-10-leg-lift-contact-cut-stocking-six-look/prompt.md:7,640-677（冲突识别与工程补齐） |

| 规则 | 文件与行号 | 支持内容 |
|---|---|---|
| LCC01 | case-studies/2026-10-leg-lift-contact-cut-stocking-six-look/prompt.md：37-106;221-231;679-739 | 接触和起抬分离，旧态持续到触地。 |
| LCC02 | case-studies/2026-10-leg-lift-contact-cut-stocking-six-look/prompt.md：43-78;187-219 | 接触—切换—保持—稳定—再抬的状态机顺序。 |
| LCC03 | case-studies/2026-10-leg-lift-contact-cut-stocking-six-look/prompt.md：19-35;131-185;604-638 | 身体支撑与切前切后位置连续。 |
| LCC04 | docs/casereview/2026-10-leg-lift-contact-cut-stocking-six-look.md：44 | 六次转换对应七个状态。 |
| LCC05 | docs/casereview/2026-10-leg-lift-contact-cut-stocking-six-look.md：31;37-45 | 需结合帧率和误差预算，不能由毫秒精度推断实现。 |
| LCC06 | case-studies/2026-10-leg-lift-contact-cut-stocking-six-look/prompt.md：563-575 | 原正文最后明确区间止于4.690秒。 |
| LCC07 | docs/casereview/2026-10-leg-lift-contact-cut-stocking-six-look.md：31;46 | 固定机位不排除外观硬切。 |
| LCC08 | case-studies/2026-10-leg-lift-contact-cut-stocking-six-look/README.md：17;42-48 | 改写源morph且动作视频可选，须补无视频输入。 |
| LCC09 | case-studies/2026-10-leg-lift-contact-cut-stocking-six-look/prompt.md：7;640-677 | 原声不改和新环境/鞋声条款需显式确定混音职责。 |
