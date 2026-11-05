# 道具脱离、触镜与局部扇风的连续动作链：输出工作表

将本文件复制到任务目录并填写；它是规划/交付模板，不是直接送入 H3 的全部正文。填写完的计划、参考权限和审计记录与生成提示词分开保存。

## 1. 当前任务与输入

| 输入项 | 当前任务值、来源与待核验内容 |
|---|---|
| 参考图和初始身体状态 | 确认人物身份、服装、机位及左右脚起态。以人物解剖学左右为准记录哪脚支撑、哪脚抬起、布料物穿在哪；参考图不满足起态时重写起态或请求相符素材，不能假装符合。 |
| 实体与两手角色 | 给人物、左右手、左右脚、布料物稳定ID。明确哪只解剖学手在双手协作后持物并投掷/扇风，另一只手何时转为捂嘴；不是只写“同一只手”而不绑定左右。 |
| 动作链与不可省前提 | 确认检查、闻、投掷、触镜、反弹、下落、落脚和扇风中哪些必须保留；写出接触点、所有权变化、释放时点及阻止并发的条件。 |
| 音轨、时长及节奏要求 | 读取已提供音轨的实际音头时刻或用户给定标记；记录总故事长度、每态可辨认的预算和结束保持。只有图片或抽象ACCENT标签时标记audio/onsets为missing。 |

## 2. 本案例交付

### 实体和阶段不变量表

解剖学左右、手部职责、道具归属、支撑状态、穿戴状态及各规则生效区间。

### 动作状态表

每态前提、活动/保持部位、动作、结果、下一态接口和不允许并发的动作。

### 音频事件与片段计划

实际或missing的音头、动作时间预算、容差、重复段降级、生成切片和跨片末态。

### 正式正文及验收记录

可用H3结构的正文和逐态人工审片清单，明确计划检查与未完成的媒体验证。

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
| S1 | 身份标签永久，支撑、穿戴和位置是随阶段变化的状态；左右采用人物解剖学坐标。 | unverified | 填入实际检查记录 |
| S2 | 上一态结束必须满足下一态前置条件；道具从穿戴、手持到飞行的归属变化必须可追踪。 | unverified | 填入实际检查记录 |
| S3 | 将两手角色绑定到具体解剖学手，持物→投掷→扇风是同一只手，另一只手保持捂嘴职责。 | unverified | 填入实际检查记录 |
| S4 | 释放先于飞行，触镜先于反弹，下落开始后才允许抬起脚下降；不能用同时发生省略因果。 | unverified | 填入实际检查记录 |
| S5 | 扇风阶段保持近端肩臂肘前臂总体稳定，只让腕掌产生主要横摆；允许后来下身有独立节奏。 | unverified | 填入实际检查记录 |
| S6 | 支撑脚不移动只适用于单腿支撑阶段，不能与后续该脚tap同时写成全程禁令。 | unverified | 填入实际检查记录 |
| S7 | STATE 8 的看物主体必须是人物与眼睛，不是持物的手。 | unverified | 填入实际检查记录 |
| S8 | 抽象重音标签必须有实际时刻、持续预算和容差才构成可验收音乐计划；无音轨不得虚构。 | unverified | 填入实际检查记录 |
| S9 | 25个自然语言状态和作者成功自述不等于已通过物理、同步或稳定性验证。 | unverified | 填入实际检查记录 |

记录静态检查结果、仍缺素材/测量、是否已实际生成，以及实际生成后才可评估的身份、动作、声音和接缝表现。
