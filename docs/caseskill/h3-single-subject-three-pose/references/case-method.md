# 单人三姿态锚点与近身连续飞行摄影：方法与修复

## 导航

1. 方法来源与适用范围
2. 条件分支与冲突处理
3. 失败表现与修复
4. 迁移示例
5. 规则证据

## 方法来源与适用范围

把姿态图作为连续动作的途经状态，分别规划人物状态和相机空间路线，处理参考属性冲突、运动阶段作用域和路径可读性，形成可审校的15秒连续镜头方案。

本方法由原案例文本、逐案评估和 H3 官方协议共同整理。原案经验、评估发现与本次补齐的数据/检查接口须分别表述；案例作者的成功报告不等于本次实测。原稿快照保留原貌，冲突由本文件及技能入口裁决。

- 五个案例文本和对应review均完整阅读，媒体未读取或独立验证；作者的生成结果不可升格为稳定性保证。
- 15秒七阶段和14–15秒保持是原案结构，可按任务调整；局部时间段不是七次独立生成，保持连续镜头的创作意图。
- 本案没有音频时间轴，音乐卡点不是必需项；静态图不作为动作轨迹或声音证据。
- 环绕行进角度与三分之四人脸视角分开记录；无空间尺寸时保守外绕并记录missing，不声称数值碰撞检测。

## 条件分支与冲突处理

| 条件 | 执行动作 | 案例/评估依据 |
|---|---|---|
| 三张图衣服、背景或身份不一致 | 输出差异与属性权限；可让图1负责身份服装场景、其余只取姿态，但该选择须明确。若用户坚持互相矛盾的身份同时不变，标记无法按同一人物方案成立。 | docs/casereview/2026-08-single-subject-three-pose.md:26,39 |
| 全程“Never stop”与末尾定住并存 | 把规则写成0–14秒飞行、14–15秒终态保持，人物可有自然呼吸但不重新开始大幅姿态转场。 | case-studies/2026-08-single-subject-three-pose/prompt.md:229,577–581 |
| 袖口、头发或窄场地阻断路线 | 保持人物动作，给相机更宽外侧绕行，缩减改向数量；将净距未知列为missing，不保证文字已解决碰撞。 | case-studies/2026-08-single-subject-three-pose/prompt.md:192–233,682；docs/casereview/2026-08-single-subject-three-pose.md:39 |
| 用户说“3/4环绕”但未说明角度或视角 | 把行进弧段和观看方向分别列出；明确本次采用的起止方位/角度，避免把三分之四脸视角直接当270度行进。 | case-studies/2026-08-single-subject-three-pose/prompt.md:376,477,522 |
| 想要严格一镜到底且超过15秒 | 说明长故事需生成切片和衔接设计；可缩短到官方单片范围，或明确分片接续不能仅靠文字保证无缝。 | case-studies/2026-08-single-subject-three-pose/README.md:8,47；references/h3-official.md |

## 失败表现与修复

| 失败表现 | 修复步骤 | 依据 |
|---|---|---|
| 三张图变成轮播、溶解或三个不同人物 | 统一主体ID，分别标姿态锚点；写出重心、躯干、肩臂和头部的连续过渡并删除切图指令。 | case-studies/2026-08-single-subject-three-pose/prompt.md:1–44,130–169,424–456 |
| 相机绕静止人物空转或人物为相机闪避 | 为每段增加与参考相容的姿态微调；分清人物自然运动、相机主动避让的职责。 | case-studies/2026-08-single-subject-three-pose/prompt.md:171–189,403–421,641–660 |
| 近身飞行穿过袖子、头发或肢体 | 指出具体相交段，用身体外侧较宽弧线替换窄缝路线；减少同时发生的路径改向，不声称无几何资料即可保证净距。 | case-studies/2026-08-single-subject-three-pose/prompt.md:192–233,682,784–796 |
| 微型摄影机变成可见无人机或人物变巨人 | 明确人物实际比例不变，微小只指观察点；用近距离透视和视差表达，不生成实体飞行器。 | case-studies/2026-08-single-subject-three-pose/prompt.md:79–104；case-studies/2026-08-single-subject-three-pose/vocabulary-expanded.zh-CN.md:52–59,103 |
| 最后仍高速飞走、拉到全身或背景大全景 | 设置14秒到达第三姿态半身终态并保持至15秒，删除飞行规则对终态的覆盖。 | case-studies/2026-08-single-subject-three-pose/prompt.md:559–581 |
| 脸部接近靠数字变焦，缺少空间视差 | 写明相机从三分之四方向真实接近和后撤，前景与背景相对移动；降低过近造成的畸变风险。 | case-studies/2026-08-single-subject-three-pose/prompt.md:509–553,663–704 |

## 迁移示例

**任务**

同一位成年模特穿短夹克的三张图：图1重心在右腿、图2肩部侧转左臂抬起、图3正对镜头双手自然垂下；做15秒近身高速展示，最后半身保持1秒。

**预期处理示例**

三图绑定同一主体S，图1主导脸、夹克及摄影棚，图2/3只提供姿态途经点；此分工须核对三图确实相容。0–2.5秒从图1姿态的脚踝外侧起飞，模特轻换重，相机沿小腿外侧上升；2.5–5秒模特连续转躯干、肩部并抬左臂到图2，相机从腰外侧向肩外侧走弧，左臂进入前方时改向外绕，避免穿过袖口；5–7.5秒围绕躯干外侧上升，模特有小幅头肩调整而不定格；7.5–9.5秒左臂自然放下、肩部回正到图3，相机在肩外侧升到头侧；9.5–11.8秒用约100度上身弧段回到三分之四脸视角；11.8–13.5秒从该方向靠近脸，13.5–14秒沿连续弧线转向并后撤至头、肩、上躯干入画，14–15秒保持。净距未测量，clearance=missing，因此采用外轮廓绕行，不安排穿臂缝或穿头发；若最后0.5秒不足以自然后撤，提前开始后撤并减少脸部接近段。此时间与角度是新方案，不是已核验路径。无音频需求，保留纯动作/摄影计划，不编造BPM。

示例是编排示范；其中任务给定参数和演算不代表当前已经读取了对应媒体，也不代表一次 H3 推理已完成。完整生成端交付仍需按输出模板选择正确字段和真实素材绑定。

## 规则证据

以下行号对应本技能来源索引中的固定快照；`review` 指 `source-review.md`。工程补齐项以其所解决的原文/评估缺口为依据，不伪称上游已实现该检查。

| 规则 | 原文或评估位置 |
|---|---|
| P1 | case-studies/2026-08-single-subject-three-pose/prompt.md:1–44,130–169 |
| P2 | case-studies/2026-08-single-subject-three-pose/prompt.md:79–104,171–189 |
| P3 | case-studies/2026-08-single-subject-three-pose/prompt.md:301–456,613–638 |
| P4 | case-studies/2026-08-single-subject-three-pose/prompt.md:192–233,663–704 |
| P5 | case-studies/2026-08-single-subject-three-pose/prompt.md:229–233,559–581；docs/casereview/2026-08-single-subject-three-pose.md:38 |
| P6 | docs/casereview/2026-08-single-subject-three-pose.md:26,39 |
| P7 | case-studies/2026-08-single-subject-three-pose/prompt.md:509–581,663–704 |
| P8 | case-studies/2026-08-single-subject-three-pose/vocabulary-expanded.zh-CN.md:105–107 |

| 规则 | 文件与行号 | 支持内容 |
|---|---|---|
| P1 | case-studies/2026-08-single-subject-three-pose/prompt.md：1–44,130–169 | 同一人物三图，姿态锚点与中间动作的核心定义。 |
| P2 | case-studies/2026-08-single-subject-three-pose/prompt.md：79–104,171–189 | 不可见微小视点由透视等表现，人物不躲相机。 |
| P3 | case-studies/2026-08-single-subject-three-pose/prompt.md：301–456,613–638 | 两次姿态过渡分别配人物动作和同步相机路径。 |
| P4 | case-studies/2026-08-single-subject-three-pose/prompt.md：192–233,663–704 | 腿外侧、臂下、肩外侧的避让例及无瞬移/穿模要求。 |
| P5 | docs/casereview/2026-08-single-subject-three-pose.md：38 | 评估要求Never stop保留作用域，与14–15秒保持协调。 |
| P6 | docs/casereview/2026-08-single-subject-three-pose.md：26,39 | 评估指出三图属性冲突和空间契约未定义，应补优先级。 |
| P7 | case-studies/2026-08-single-subject-three-pose/prompt.md：509–581,663–704 | 接近/后撤为真实空间运动、前后景视差及半身终态。 |
| P8 | case-studies/2026-08-single-subject-three-pose/vocabulary-expanded.zh-CN.md：105–107 | 拟人化预判/避让不是仓库提供的真实算法与物理保证。 |
