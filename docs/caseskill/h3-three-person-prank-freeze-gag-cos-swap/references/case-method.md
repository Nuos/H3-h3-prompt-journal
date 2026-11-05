# 三人画外干扰、定格笑点与仅换皮复现：方法与修复

## 导航

1. 方法来源与适用范围
2. 条件分支与冲突处理
3. 失败表现与修复
4. 迁移示例
5. 规则证据

## 方法来源与适用范围

先还原谁先做了什么、使谁的动作改变，再冻结时间与因果结构进行外观迁移；明确区分演员动作、第一人称摄影、后期定格和三类声音，修复原案时长、帧数、字段数量及道具清单的含混。

本方法由原案例文本、逐案评估和 H3 官方协议共同整理。原案经验、评估发现与本次补齐的数据/检查接口须分别表述；案例作者的成功报告不等于本次实测。原稿快照保留原貌，冲突由本文件及技能入口裁决。

- 本案限定三人、第一人称手持、三次冻结、无配乐及功能面罩；这些是模板变体，不应成为全部H3任务硬约束。
- 原目录未提供本次可独立复算的源视频抽帧表、RMS曲线、BPM判定日志或外部video-to-h3-prompt固定版本，作者叙述不作独立实验结论。
- 实际顶层12字段而非README所称14；此字段布局也不是官方H3通用强制schema。
- 原文15.3秒、首定格0.6秒与~15s/~0.5s表达不严格等价；帧取整、基片与成片时轴、定格追加／替代方式为工程补齐，需在每个任务显式裁决。
- 示例的14秒基片、13.5秒裁窗和三个0.5秒追加保持是新请求的工程示范，未伪称源案例或已量测结果。
- B早期small bottle和后期blue bottle是否同一物件缺少交接说明；保留澄清／证据需求，不自动新增道具。

## 条件分支与冲突处理

| 条件 | 执行动作 | 案例/评估依据 |
|---|---|---|
| 用户只换COS，但新造型没有可开合面罩 | 报告功能依赖冲突；沿用兼容头盔需属于明确可改造外观，否则把第一轮笑点重写标为机制改编，不能同时承诺动作与道具完全不变。 | case-studies/2026-09-three-person-prank-freeze-gag-cos-swap/README.md:33,55；docs/casereview/2026-09-three-person-prank-freeze-gag-cos-swap.md:39 |
| 用户严格要求15.000秒，并要求完全复刻原文到15.3秒 | 两条约束不兼容：提交可审阅的≤15秒重排版本并列出改动，或保留15.3秒后期成片但核算生成基片与新增定格；不将15.3秒写为标准H3单次duration。 | docs/casereview/2026-09-three-person-prank-freeze-gag-cos-swap.md:44；工程补齐：官方4–15秒边界 |
| 三个声音峰看似有固定间隔 | 先检视起音规律、频谱和画面事件，把水声／冲击SFX分离；没有持续乐曲证据时不计算并宣称音乐BPM。 | case-studies/2026-09-three-person-prank-freeze-gag-cos-swap/README.md:24；case-studies/2026-09-three-person-prank-freeze-gag-cos-swap/vocabulary-expanded.zh-CN.md:18-20,103 |
| 第三人的手在抽帧间消失，无法确认谁转了头 | 缩小疑点窗口并按源fps逐帧检查；保留两个因果版本和缺证。4–8fps只是作者本次策略，不能保证捕获所有3–5帧动作。 | case-studies/2026-09-three-person-prank-freeze-gag-cos-swap/README.md:17,24,53；docs/casereview/2026-09-three-person-prank-freeze-gag-cos-swap.md:45 |
| 模型把定格演成人物站住，背景仍动 | 把freeze从performance移到editing，明确保持整帧、追加帧数、叠层和恢复帧；需精确可复现时把该操作列入后期执行表。 | case-studies/2026-09-three-person-prank-freeze-gag-cos-swap/README.md:18,31；case-studies/2026-09-three-person-prank-freeze-gag-cos-swap/prompt.zh-CN.md:421-447 |

## 失败表现与修复

| 失败表现 | 修复步骤 | 依据 |
|---|---|---|
| 出现两个人，干扰突然凭空发生或被写成A自己做 | 恢复画外Subject3及手臂入口，把发力者、接触部位、受力反应依次写出；先核验短动作证据再锁定解释。 | case-studies/2026-09-three-person-prank-freeze-gag-cos-swap/README.md:16-17；case-studies/2026-09-three-person-prank-freeze-gag-cos-swap/prompt.md:19,87 |
| 第二轮水又喷在A面罩，未击中B | 核对第一次之后A开面罩的显式动作，固定第二轮UP；第三人只抓头盔侧面改变朝向，水释放必须晚于头／肩向B转动。 | case-studies/2026-09-three-person-prank-freeze-gag-cos-swap/prompt.md:49-59,87 |
| 画面定格期间只有人物不动，或恢复时重复整轮动作 | 使用后期整帧保持而非人物姿态停顿；指定capture源帧、持续帧数以及恢复下一源帧，不重播蓄力动作。 | case-studies/2026-09-three-person-prank-freeze-gag-cos-swap/README.md:18,31；case-studies/2026-09-three-person-prank-freeze-gag-cos-swap/vocabulary-expanded.zh-CN.md:65-77 |
| 改COS后出现新实验台、警械或长镜头剧情变了 | 按替换合同回退未授权道具／场景／时轴改动；只更新外观、接触名词及湿发衣料响应，功能依赖单独审查。 | case-studies/2026-09-three-person-prank-freeze-gag-cos-swap/README.md:33,49,55；case-studies/2026-09-three-person-prank-freeze-gag-cos-swap/prompt.md:91 |
| 三次定格总长、片尾与15秒参数互相矛盾 | 决定含定格输出时轴并以整帧对账；源15.3秒保留为来源事实，把重排或后期延长作为明确方案，不静默裁去动作。 | docs/casereview/2026-09-three-person-prank-freeze-gag-cos-swap.md:44 |
| 无音乐要求导致现场声全部消失，或凭三声冲击添加强拍配乐 | 按三类声音分轨；保留场内声和定格SFX，音乐明确none，缺音轨时不输出BPM。 | case-studies/2026-09-three-person-prank-freeze-gag-cos-swap/prompt.md:93-95；case-studies/2026-09-three-person-prank-freeze-gag-cos-swap/vocabulary-expanded.zh-CN.md:99-103 |

## 迁移示例

**任务**

将三人画外干扰的喜剧机制改编成雨衣主题，成人A/B可见、第三人只伸手；保留功能性可翻面罩，但允许重排为严格15秒、24FPS。三个定格从成片4、8、12秒开始，各0.5秒；没有原视频或音轨。

**预期处理示例**

登记source_video=missing、source_audio=missing，所有时点是用户计划；这属于重新定时的机制改编，不称skin-only复刻。生成一段14秒／24FPS连续基片，选择前13.5秒324帧作为live素材，再追加三个12帧定格得到15秒360帧成片。输出帧[96,108)、[192,204)、[288,300)分别保持基片前一帧95、179、263；各窗口首帧一帧白闪，之后微放大保持，恢复源帧96、180、264。A的面罩初态UP；第一轮在第一个保持点前由画外手关DOWN，结果出现后才冻结；两段间A自行开UP；第二轮只改变头盔朝向而不关面罩；第三轮B准备动作被干扰，结果落在最后冻结前。12.5–15秒保留三人关系收束，第三人仍不露脸。主体、动作因果、摄影、编辑分层写；现场水声与短对白按事件生成，三个后期喜剧音效单列，配乐none，不提供BPM。雨衣与湿发仅按接触事件改变；实际动作是否可在所分配时段完成、基片选窗是否成立，均需生成后核验。

示例是编排示范；其中任务给定参数和演算不代表当前已经读取了对应媒体，也不代表一次 H3 推理已完成。完整生成端交付仍需按输出模板选择正确字段和真实素材绑定。

## 规则证据

以下行号对应本技能来源索引中的固定快照；`review` 指 `source-review.md`。工程补齐项以其所解决的原文/评估缺口为依据，不伪称上游已实现该检查。

| 规则 | 原文或评估位置 |
|---|---|
| R1 | case-studies/2026-09-three-person-prank-freeze-gag-cos-swap/README.md:16-18,24-43；docs/casereview/2026-09-three-person-prank-freeze-gag-cos-swap.md:17-21,29-33 |
| R2 | case-studies/2026-09-three-person-prank-freeze-gag-cos-swap/prompt.md:37-59,87 |
| R3 | case-studies/2026-09-three-person-prank-freeze-gag-cos-swap/README.md:18,31,35-43；case-studies/2026-09-three-person-prank-freeze-gag-cos-swap/prompt.md:45-75,83 |
| R4 | docs/casereview/2026-09-three-person-prank-freeze-gag-cos-swap.md:43-45；工程补齐：基片／输出双时间线与官方能力校验 |
| R5 | case-studies/2026-09-three-person-prank-freeze-gag-cos-swap/README.md:33,49,55；case-studies/2026-09-three-person-prank-freeze-gag-cos-swap/vocabulary-expanded.zh-CN.md:83-95 |
| R6 | case-studies/2026-09-three-person-prank-freeze-gag-cos-swap/README.md:24,31；case-studies/2026-09-three-person-prank-freeze-gag-cos-swap/prompt.md:93-95；case-studies/2026-09-three-person-prank-freeze-gag-cos-swap/vocabulary-expanded.zh-CN.md:97-105 |
| R7 | case-studies/2026-09-three-person-prank-freeze-gag-cos-swap/prompt.md:17,27,65,77,89,91；工程补齐：道具身份与状态账本 |
| R8 | case-studies/2026-09-three-person-prank-freeze-gag-cos-swap/README.md:5-9,57,61-71；docs/casereview/2026-09-three-person-prank-freeze-gag-cos-swap.md:5-8,37,43 |

| 规则 | 文件与行号 | 支持内容 |
|---|---|---|
| R1 | case-studies/2026-09-three-person-prank-freeze-gag-cos-swap/README.md：16-18;24-43 | 画外持机者和稀疏抽帧误判的直接案例依据；证据置信标签为工程补齐。 |
| R2 | case-studies/2026-09-three-person-prank-freeze-gag-cos-swap/prompt.md：37-59;87 | 蓄力、第三人关面罩、A自行开启、第二轮保持UP与先接触后结果的时间链。 |
| R3 | case-studies/2026-09-three-person-prank-freeze-gag-cos-swap/README.md：18;31;35-43 | 后期freeze区别表演、三次叠层和四元组方法。 |
| R4 | docs/casereview/2026-09-three-person-prank-freeze-gag-cos-swap.md：43-45 | 评估明确指出实际字段数、15.3秒片尾、首定格0.6秒及帧取整缺口。 |
| R5 | case-studies/2026-09-three-person-prank-freeze-gag-cos-swap/README.md：33;49;55 | 仅换皮的冻结对象与功能性道具相容规则。 |
| R6 | case-studies/2026-09-three-person-prank-freeze-gag-cos-swap/vocabulary-expanded.zh-CN.md：97-105 | 无配乐、SFX、RMS能量与BPM的边界。 |
| R7 | case-studies/2026-09-three-person-prank-freeze-gag-cos-swap/prompt.md：17;27;65;77;89;91 | 小瓶／蓝瓶清单差异和持续湿润状态；身份账本为工程修补。 |
| R8 | docs/casereview/2026-09-three-person-prank-freeze-gag-cos-swap.md：5-8;37;43 | 外部skill实现未核、实际字段数核对；analysis_only与生成输入角色拆分为工程补齐。 |
