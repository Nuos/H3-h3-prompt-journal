# 剧情锚点驱动的水上闯关与失败反转：方法与修复

## 导航

1. 方法来源与适用范围
2. 条件分支与冲突处理
3. 失败表现与修复
4. 迁移示例
5. 规则证据

## 方法来源与适用范围

把“必经剧情 + 明确授权的即兴范围”变成可检查的因果叙事方案，在保留自然表演空间的同时避免漏事件、越过前提和片段接续失真。

本方法由原案例文本、逐案评估和 H3 官方协议共同整理。原案经验、评估发现与本次补齐的数据/检查接口须分别表述；案例作者的成功报告不等于本次实测。原稿快照保留原貌，冲突由本文件及技能入口裁决。

- 水上赛道、七个事件和两句原台词是案例实例；迁移时保留因果与自由度分工，不强制所有任务使用同一道具和人物。
- 所有本文材料已全文阅读；媒体未读取或独立验证。作者结果是经验陈述，不能作为稳定生成证明。
- 低规格试跑仅作为流程建议；实际规格必须按可用平台核对，不把0.3/0.8/1当作API参数。
- 官方4–15秒范围约束生成切片，原案20秒保留为创作方案；本文时间预算尚待生成与审片验证。

## 条件分支与冲突处理

| 条件 | 执行动作 | 案例/评估依据 |
|---|---|---|
| 用户要20秒完整挑战 | 保留20秒故事目标，按官方生成长度分成例如10秒+10秒；在第二障碍恢复后的跑道上交接，传递身份、服装、身体位置、朝向和声音状态。 | docs/casereview/2026-08-water-obstacle-variety-show.md:28,36–41；references/h3-official.md |
| 用户要求一镜到底 | 取消把八个故事段自动解释为切镜的做法，另写能看清关键接触与空间关系的连续摄影路径；不承诺单次20秒生成。 | case-studies/2026-08-water-obstacle-variety-show/vocabulary-expanded.zh-CN.md:105 |
| 有限时长放不下全部事件和两句对白 | 先压缩开场介绍、观众镜头和重复闪避；仍放不下时增加创作时长或标记不可兼容，保留因果完整，不静默删掉抓稳或水后反应。 | docs/casereview/2026-08-water-obstacle-variety-show.md:40–42 |
| 只给身份图而要求按原音卡点 | 把音轨及音头时间列为 missing；先输出剧情锚点和可选音乐弧线，待音轨提供后再绑定事件。 | case-studies/2026-08-water-obstacle-variety-show/prompt.md:5–7,155–165 |

## 失败表现与修复

| 失败表现 | 修复步骤 | 依据 |
|---|---|---|
| 只写“自然有趣”，生成事件顺序丢失 | 恢复必要事件清单及前提/结果，缩小自由度到微动作与摄影；不把每帧都写死。 | case-studies/2026-08-water-obstacle-variety-show/README.md:19–33,54–60 |
| 还未抓牢就被侧击，反转缺乏接近成功的铺垫 | 为双手抓牢和短暂停留分配可辨认时段，明确先抓牢再侧击再失握。 | case-studies/2026-08-water-obstacle-variety-show/prompt.md:109–131 |
| 失足后跳到新地点或落水后头发干燥 | 补上恢复起点、相邻跑道/水池与湿发状态继承，跨片末帧不可用时明示缺失。 | case-studies/2026-08-water-obstacle-variety-show/prompt.md:99–107,133–147 |
| 声画过密导致台词或落水被省略 | 减少可选解说与观众反应，单独保留收尾对白时段；必要时重分故事与生成切片。 | docs/casereview/2026-08-water-obstacle-variety-show.md:40–42 |
| 提高所谓分辨率系数后声称动作必然一致 | 删除保证，记录实际模型、界面规格和试跑版本；改为提升规格后重新审片。 | case-studies/2026-08-water-obstacle-variety-show/vocabulary-expanded.zh-CN.md:103 |

## 迁移示例

**任务**

用成年跑酷教练的身份参考图做20秒夜间闯关喜剧：滚筒顺利、旋转软杆把他绊倒、恢复后抓住终点墙，被侧面软垫打入池中；末尾说“我刚刚都抓住了！”允许综艺切镜。

**预期处理示例**

身份图只绑定教练的脸、体型、服装和可见配饰，新增赛道由文字定义。20秒创作方案拆为A片10秒、B片10秒：A的0–1.5秒起点一句“这次看我的”，1.5–4秒通过滚筒，4–6.5秒软杆接触导致跌到平台，6.5–10秒从同一平台起身并进入终点前跑道；A末态记录面向终点、双手自由、头发未湿。B承接该末态，0–3秒冲墙并双手抓稳，3–4秒短暂看似成功，4–6秒软垫从侧面接触上身导致失握并落入墙侧同一水池，6–7秒浮出且头发湿透，7–10秒看向摄影机说“我刚刚都抓住了！”并停留反应。具体滚筒步法、起身动作和综艺机位可以自然选择；终点墙、跑道、水池关系固定。时间是预演预算而非已验证成片；如果台词或抓稳动作容纳不下，先删开场台词与可选观众反应，再调整故事长度。无音轨，音乐仅规定接近成功时增强、落水后轻喜剧收束；不编造BPM。

示例是编排示范；其中任务给定参数和演算不代表当前已经读取了对应媒体，也不代表一次 H3 推理已完成。完整生成端交付仍需按输出模板选择正确字段和真实素材绑定。

## 规则证据

以下行号对应本技能来源索引中的固定快照；`review` 指 `source-review.md`。工程补齐项以其所解决的原文/评估缺口为依据，不伪称上游已实现该检查。

| 规则 | 原文或评估位置 |
|---|---|
| W1 | case-studies/2026-08-water-obstacle-variety-show/prompt.md:5–7,33–35 |
| W2 | case-studies/2026-08-water-obstacle-variety-show/prompt.md:87–153 |
| W3 | case-studies/2026-08-water-obstacle-variety-show/prompt.md:43–55 |
| W4 | case-studies/2026-08-water-obstacle-variety-show/prompt.md:99–107,133–147 |
| W5 | case-studies/2026-08-water-obstacle-variety-show/vocabulary-expanded.zh-CN.md:101 |
| W6 | docs/casereview/2026-08-water-obstacle-variety-show.md:36–42 |
| W7 | case-studies/2026-08-water-obstacle-variety-show/vocabulary-expanded.zh-CN.md:105 |
| W8 | case-studies/2026-08-water-obstacle-variety-show/vocabulary-expanded.zh-CN.md:103 |

| 规则 | 文件与行号 | 支持内容 |
|---|---|---|
| W1 | case-studies/2026-08-water-obstacle-variety-show/prompt.md：5–7,33–35 | 原文限定单图身份范围，外观保持且不新增佩戴物。 |
| W2 | case-studies/2026-08-water-obstacle-variety-show/prompt.md：87–153 | 恢复、双手抓墙、侧击失握、同池落水、湿发吐槽构成可检查的顺序依赖。 |
| W3 | case-studies/2026-08-water-obstacle-variety-show/prompt.md：43–55 | 保留必要事件同时明确授权动作、镜头和反应的自由度。 |
| W4 | case-studies/2026-08-water-obstacle-variety-show/prompt.md：99–107,133–147 | 从跌落继续，落水不换地点，水后保留湿发。 |
| W5 | case-studies/2026-08-water-obstacle-variety-show/vocabulary-expanded.zh-CN.md：101 | 词汇增补明示story beat是剧情节拍，不等于音乐音头。 |
| W6 | docs/casereview/2026-08-water-obstacle-variety-show.md：36–42 | 评估要求时间容量、降级和事件完整性验收；分片限制由共同官方资料提供。 |
| W7 | case-studies/2026-08-water-obstacle-variety-show/vocabulary-expanded.zh-CN.md：105 | 连续观感与严格一镜到底不同，正文包含八镜头。 |
| W8 | case-studies/2026-08-water-obstacle-variety-show/vocabulary-expanded.zh-CN.md：103 | 分辨率系数缺单位，不转写成官方控制接口或稳定性保证。 |
