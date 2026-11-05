# H3 四主体身份锚与队形状态接力：方法与修复

## 导航

1. 方法来源与适用范围
2. 条件分支与冲突处理
3. 失败表现与修复
4. 迁移示例
5. 规则证据

## 方法来源与适用范围

将固定视觉锚、队形节点和动力状态接力组合为可审计的多人编排子流程，解决角色随站位改名、穿越许可冲突、段首回到参考姿势及为了看全队形而退成远景的问题。

本方法由原案例文本、逐案评估和 H3 官方协议共同整理。原案经验、评估发现与本次补齐的数据/检查接口须分别表述；案例作者的成功报告不等于本次实测。原稿快照保留原貌，冲突由本文件及技能入口裁决。

- 穿越许可schema、anchor版本和接缝逐字段diff是本次工程补齐。
- 四人仅是源案例参数；如改人数，须重新设计资产映射、队形和可见性，而非套用原四人路径。
- 不复制源歌词到新素材，不将作者近零漂移自述等同于独立验证。

## 条件分支与冲突处理

| 条件 | 执行动作 | 案例/评估依据 |
|---|---|---|
| 要从自己的象限穿过中心完成层交换 | 取消该时窗的默认通道锁，并建立限时穿越许可、错峰通行和可见性条件；若空间不足则换外侧路径。 | case-studies/2026-10-four-subject-formation-choreography/prompt.md:79-86；docs/casereview/2026-10-four-subject-formation-choreography.md:31,41,46 |
| 用户替换角色或背景 | 重新建立本任务的视觉锚及版本，不把原角色服饰或原场景强加给新资产；保留稳定ID与状态接力方法。 | case-studies/2026-10-four-subject-formation-choreography/prompt.md:6-20；docs/casereview/2026-10-four-subject-formation-choreography.md:29,39（参数化补齐） |
| 只提供新音乐名称，没有音频/节拍表 | 暂做结构时间预算，beat_grid标missing；不直接借用源93.75 BPM、k179–k200或歌词窗口。 | case-studies/2026-10-four-subject-formation-choreography/prompt.md:24-28,88-134；docs/casereview/2026-10-four-subject-formation-choreography.md:33 |
| 要求生成完整原14段最终提示词 | 区分已归档SEG10与其他13段仅总览，新增段落可按结构创作但必须标为新编，不能冒充恢复原最终版。 | case-studies/2026-10-four-subject-formation-choreography/README.md:94-120,157-161；docs/casereview/2026-10-four-subject-formation-choreography.md:23,48 |

## 失败表现与修复

| 失败表现 | 修复步骤 | 依据 |
|---|---|---|
| 换位后角色编号跟着屏幕左右变动 | 按初始资产绑定恢复稳定ID，只更新位置字段，逐段复用已冻结锚块。 | case-studies/2026-10-four-subject-formation-choreography/prompt.md:6-20,32-38 |
| 群舞变成走到新位置再摆拍 | 将路径改为有承重、回弹、转体传导和恢复的连续舞步；各主体在非特写时仍有动作。 | case-studies/2026-10-four-subject-formation-choreography/prompt.md:40-62,88-134 |
| 同时出现禁止穿越与中心交叉 | 把默认通道约束改为带局部许可的规则，核查同时间的空间占用与遮挡。 | case-studies/2026-10-four-subject-formation-choreography/README.md:78-79；docs/casereview/2026-10-four-subject-formation-choreography.md:31,41,46 |
| 段末定格、下一段重新站成参考姿势 | 将段末留作未完成但明确的身体余势，并逐主体复制到下一段INCOMING。 | case-studies/2026-10-four-subject-formation-choreography/README.md:57-68；case-studies/2026-10-four-subject-formation-choreography/prompt.md:36-38,86,134 |
| 为看清队形不断后退成大全景 | 用预置观看角度和切点揭示关系；仅为维持主体距离的后退保留。 | case-studies/2026-10-four-subject-formation-choreography/prompt.md:71,75；docs/casereview/2026-10-four-subject-formation-choreography.md:47 |

## 迁移示例

**任务**

四名新角色保持各自身份，把12秒舞段拆为前后两段；需要一次前后层交换，不能发生身体相交。未提供音乐测量数据。

**预期处理示例**

建立A/B/C/D固定ID及新资产锚，不沿用原四角色服饰；12秒分为0–6和6–12的计划时窗，音乐同步待核验。0–2秒四人在四角错拍抬臂；2–4秒仅A/B获准沿左侧前后通道交换，A先从前位向外半步再退，B待通道空出后向前，两人不同时占据通道；C/D在右侧通过膝部回弹和不同高度手臂维持舞蹈。4–6秒A完成后位承重，B前位左脚承重、右臂向右外送；段1 OUT明确B左脚支撑、躯干向右扭、右臂仍外送。段2 IN复制这组状态而非回到参考站姿，6–9秒由B余势带动C/D错拍展开，9–12秒四条手臂线形成可区分的末端构图。避碰是文本路径设计，仍需实际场地尺寸和生成结果确认。

示例是编排示范；其中任务给定参数和演算不代表当前已经读取了对应媒体，也不代表一次 H3 推理已完成。完整生成端交付仍需按输出模板选择正确字段和真实素材绑定。

## 规则证据

以下行号对应本技能来源索引中的固定快照；`review` 指 `source-review.md`。工程补齐项以其所解决的原文/评估缺口为依据，不伪称上游已实现该检查。

| 规则 | 原文或评估位置 |
|---|---|
| FSC01 | case-studies/2026-10-four-subject-formation-choreography/README.md:37-55；case-studies/2026-10-four-subject-formation-choreography/prompt.md:6-20,32-38 |
| FSC02 | case-studies/2026-10-four-subject-formation-choreography/prompt.md:8-20,36-38 |
| FSC03 | case-studies/2026-10-four-subject-formation-choreography/README.md:70-82；case-studies/2026-10-four-subject-formation-choreography/prompt.md:40-42,79-86 |
| FSC04 | case-studies/2026-10-four-subject-formation-choreography/prompt.md:50-62 |
| FSC05 | case-studies/2026-10-four-subject-formation-choreography/README.md:78-79；case-studies/2026-10-four-subject-formation-choreography/prompt.md:79-86,100-118；docs/casereview/2026-10-four-subject-formation-choreography.md:31,39-46 |
| FSC06 | case-studies/2026-10-four-subject-formation-choreography/prompt.md:71,75,142；docs/casereview/2026-10-four-subject-formation-choreography.md:47 |
| FSC07 | case-studies/2026-10-four-subject-formation-choreography/README.md:57-68；case-studies/2026-10-four-subject-formation-choreography/prompt.md:36-38,86,134 |
| FSC08 | case-studies/2026-10-four-subject-formation-choreography/README.md:118-120,154-155；case-studies/2026-10-four-subject-formation-choreography/prompt.md:44-48,142-148 |
| FSC09 | case-studies/2026-10-four-subject-formation-choreography/README.md:46-51,94-120；docs/casereview/2026-10-four-subject-formation-choreography.md:23,33,48 |

| 规则 | 文件与行号 | 支持内容 |
|---|---|---|
| FSC01 | case-studies/2026-10-four-subject-formation-choreography/prompt.md：6-20;32-38 | 视觉锚与固定主体ID明确分离外观和当前空间位置。 |
| FSC02 | case-studies/2026-10-four-subject-formation-choreography/prompt.md：36-38 | 下一段继承动作而非参考图姿势。 |
| FSC03 | case-studies/2026-10-four-subject-formation-choreography/prompt.md：40-42;79-86 | 动作链与队形节点关联。 |
| FSC04 | case-studies/2026-10-four-subject-formation-choreography/prompt.md：50-62 | 四种运动性格、错拍与非特写持续运动。 |
| FSC05 | docs/casereview/2026-10-four-subject-formation-choreography.md：31;39-46 | 抽取默认通道锁的同时要为局部穿越保留许可。 |
| FSC06 | docs/casereview/2026-10-four-subject-formation-choreography.md：47 | 退步跟随与退成大全景的动作目的不同。 |
| FSC07 | case-studies/2026-10-four-subject-formation-choreography/prompt.md：36-38;86;134 | 入态、出态和末端遮挡轨迹构成接缝契约。 |
| FSC08 | case-studies/2026-10-four-subject-formation-choreography/prompt.md：44-48;142-148 | 歌词与音频职责不能变成自动可视化对象。 |
| FSC09 | docs/casereview/2026-10-four-subject-formation-choreography.md：23;33;48 | 完整工程和量化效果证据不齐，需保留边界。 |
