# 三人画外干扰、定格笑点与仅换皮复现：输出工作表

将本文件复制到任务目录并填写；它是规划/交付模板，不是直接送入 H3 的全部正文。填写完的计划、参考权限和审计记录与生成提示词分开保存。

## 1. 当前任务与输入

| 输入项 | 当前任务值、来源与待核验内容 |
|---|---|
| 任务模式与素材角色 | 声明逆向分析、沿用已确认机制的skin-only换皮，或允许重排节拍的新改编。原视频若仅用于观察，登记analysis_only；最终T2VA不绑定参考图。若用户要求图像身份绑定，重新依据官方H3模式选择，不沿用纯T2VA标签。没有媒体时标missing，使用案例文本仅能构造待核验方案。 |
| 可检查的画面与音频 | 记录片长、原始帧率、可定位的画面和声轨；提交有歧义的时间窗、竞争剧情解释及支持帧。音频峰值是候选事件，不以三次响声自动推算BPM；无素材时不复述作者量测为本次观测。 |
| 主体、道具与功能依赖 | 分别登记可见A、可见B、画外持机者的身份与操作权限，追踪杯、瓶、头盔面罩的所有者及开闭状态。确认B早期小瓶与后期蓝瓶是否同一件；无证据时保留待确认，不让道具凭空替换。 |
| 外观替换合同 | 列出替换前后脸发、衣料、配色，以及动作接触的服装词；保持功能性翻转面罩等因果道具兼容。列出禁止改动的角色关系、事件次序、时间、机位、定格和声音。 |
| 输出时间与编辑约定 | 明确duration指生成基片还是含定格的成片，规定所有时间戳使用哪条时间线、原生24FPS与剪辑帧率、定格采用追加还是替代帧。官方标准单次生成4–15秒；15.3秒源案不能直接当作单次标准生成能力。 |

## 2. 本案例交付

### 证据与因果表

逐事件记录时间窗、观察到的画面／声音、竞争解释、最终选择及置信，主体操作权限、接触、结果和缺失素材分列。

### 道具与身体状态账本

每轮开始／结束的面罩开闭、杯瓶持有、头部朝向、湿润部位和画外手入口；每个改变附可见动作或明确待确认。

### H3正文与后期时间表

符合当前输入模式的可用提示词，以及生成基片时长、成片时长、fps、freeze四元组、对白／现场声／SFX／音乐分层；工程计划不得冒充实测。

### 仅换皮差异表与审校报告

记录允许变化、保持字段、连带物理变化及合同破坏项；分别报告生成前计划审校和生成后待验证，不把相似结果证明为唯一源剧情。

## 3. 参考权限与时间

| 素材 ID | 实际文件/来源 | 允许参考 | 不继承内容 | 生效片段/镜头 | 证据状态 |
|---|---|---|---|---|---|
| 按实际填写 | 按实际填写 | 按实际填写 | 按实际填写 | 按实际填写 | provided/missing |

| 创作段 | 生成切片 | 全局起止 | 局部时长 | 音频偏移 | 入态→出态 | 交接素材/后期策略 |
|---|---|---|---|---|---|---|
| 按实际填写 | 按实际填写 | 按实际填写 | 按实际填写 | 按实际填写 | 按实际填写 | 按实际填写 |

## 4. H3 生成正文模板

只在要求完整提示词时使用。选一种模式，删除不适用模板，填入实际对象、镜头和声音；不要把本页标题、检查表或中文说明送入生成器。以下大括号表示待填字段，最终 `.txt` 中不得残留。

### Ref2VA：六字段

```text
subject_definitions: {define actual reusable content and reference roles}

summary: {task-type prefix and target relationships}

retention_analysis: {one applicable preservation/copy relationship per independently used reference}

detailed_description: {one or two style sentences before Shot 1}
[Shot 1] {composition, visible subjects, environment, causal action, camera, sound and active references}
[Shot 2] At {MM:SS.mmm}, {only include if an actual cut is planned}

overall_soundscape: {ambient and physical sound; N/A only for explicit total silence}

non_diegetic_music: {audience-only score or N/A}
```

### T2VA / I2VA / FL2VA / L2VA：三字段

T2VA 不加图像对齐句。其他模式先选择对应的官方对齐句并填入实际最后一镜编号、两位小数时长，随后空一行。

```text
I2VA: For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.
FL2VA: How the reference pictures align with the target video — Picture 1 (from Shot 1) aligns with the 0.00-second mark of the target video; Picture 2 (from Shot {N}) aligns with the {S.SS}-second mark of the target video.
L2VA: How the reference pictures align with the target video — <Picture 1> (from [Shot {N}]) aligns with the {S.SS}-second mark of the target video.
```

上面用于选择的 `I2VA:`、`FL2VA:`、`L2VA:` 前缀不属于生成端正文，复制时删除。

```text
integrated_multimodal_description: [Shot 1] {style, initial composition and full audiovisual development}

overall_soundscape: {ambient and physical sound}

non_diegetic_music: {audience-only music or N/A}
```

## 5. 逐项验收与未验证范围

| ID | 判据 | 结果 | 具体证据/修复 |
|---|---|---|---|
| R1 | 画外持机者是本案第三个行动者；摄影视点不意味着中立观察。手、袖子、道具只在有连续证据时归并到同一主体，身份推断保留置信与缺证。 | unverified | 填入实际检查记录 |
| R2 | 每个喜剧结果必须有可见准备、干扰者先行动、接触及受力改变；源案面罩UP→第三人关DOWN→A自己开UP→第二轮保持UP的顺序不可在skin-only中改变。 | unverified | 填入实际检查记录 |
| R3 | 三次定格属于后期画面保持；用入点／持续帧数／叠层／恢复方式四项定义，演员表演层不写成所有人自行停住。三次和半秒是本案例选择，不是H3普遍要求。 | unverified | 填入实际检查记录 |
| R4 | 明确时间戳是否包含定格，并使总时长、帧率、定格区间可对账。原15.3秒与首0.6秒冲突必须记录；官方标准生成能力和后期延长成片分开描述。 | unverified | 填入实际检查记录 |
| R5 | 仅换皮冻结行动者、因果、时点、摄影、定格和声音，只允许外观与其接触到的材料响应变化；功能性道具被删除或时间被移动即转为机制改编。 | unverified | 填入实际检查记录 |
| R6 | 现场声、后期SFX、配乐分列；没有音乐不等于全轨静音。RMS峰值或响声不能单独证明节拍、BPM或因果，未获取音轨不报告实测结果。 | unverified | 填入实际检查记录 |
| R7 | 所有杯瓶有稳定身份与拥有者；湿发、衣料、面罩水膜随事件累积，不因定格恢复或换皮重置。B的小瓶与蓝瓶描述差异应核实或显式裁决，不能暗中增删道具。 | unverified | 填入实际检查记录 |
| R8 | 分析来源与生成参考分离；本案T2VA无图输入，原视频逆向分析不自动变成Ref2VA。实际12字段和外部配套skill链接不构成额外官方强制规范或已验证实现。 | unverified | 填入实际检查记录 |

记录静态检查结果、仍缺素材/测量、是否已实际生成，以及实际生成后才可评估的身份、动作、声音和接缝表现。
