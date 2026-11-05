# H3 右入单状态展示与硬切装配：输出工作表

将本文件复制到任务目录并填写；它是规划/交付模板，不是直接送入 H3 的全部正文。填写完的计划、参考权限和审计记录与生成提示词分开保存。

## 1. 当前任务与输入

| 输入项 | 当前任务值、来源与待核验内容 |
|---|---|
| 固定视觉锚 | 给出人物参考、场景来源、固定主服装与配饰、正面全身机位。参考图权限明确排除当前状态允许变化的鞋袜属性，未提供场景不自动继承源厨房。 |
| 有序状态目录 | 每状态定义袜饰的材质/花纹/高度等实际差异，状态数决定片段数；无文字版不生成源编号和横幅。 |
| 音频与编辑时窗 | 提供目标音轨、总时长、已核验切点或明确的计划边界、输出fps与文字开关；原2.267/4.233是该案例文字记录，不是新音频测量值。 |
| 生成能力 | 提供实际H3最小/最大时长、帧数规则及是否允许生成余量后裁切。源1.667–2.267秒不自动代表当前部署能够原样调用。 |

## 2. 本案例交付

### 状态与不变量清单

每状态唯一变化、固定视觉项、参考权限例外、文字开关。

### 逐镜独立提示词

当前状态从首帧生效、右入跨步、落定pose、单人、固定全身机位和片段尾态六锚。

### 编辑决策表

镜头ID、状态ID、全局区间、局部时长、实际生成长度、可用裁切窗、硬切两侧动作、音频窗口、fps/帧号。

### 片段与成片验收表

首帧状态、人物数、入画方向、终帧pose、构图、切点、总长、原轨复用及尚未核验的候选点。

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
| SRE01 | 每个状态独立生成，首帧已经是该状态并处于画右跨步中；单段不描述画内换装。 | unverified | 填入实际检查记录 |
| SRE02 | 终帧保留pose，下一镜从跨步进入；两侧不是同一动作无缝续接。 | unverified | 填入实际检查记录 |
| SRE03 | 只改变状态目录指定的袜饰属性，其余身份、主服装、场景和机位保持；图像权威保留明确例外。 | unverified | 填入实际检查记录 |
| SRE04 | 不添加走出清屏、空帧或另一人物来解释状态变化，硬切本身负责重置片段。 | unverified | 填入实际检查记录 |
| SRE05 | 生成片段与后期整轨音频装配分工明确；fully_copy提示文字不替代真实音频复用。 | unverified | 填入实际检查记录 |
| SRE06 | 切点检测阈值及4.4秒候选只属于源分析记录；没有逐帧证据不能断言它是误报或无关。 | unverified | 填入实际检查记录 |
| SRE07 | 实际调用前核验短时长/帧数支持，可用生成余量和裁切实现目标，但不虚构调用能力。 | unverified | 填入实际检查记录 |
| SRE08 | 一镜一状态、右侧入画和无文字是本展示策略的默认，不作为全部H3任务的统一限制。 | unverified | 填入实际检查记录 |

记录静态检查结果、仍缺素材/测量、是否已实际生成，以及实际生成后才可评估的身份、动作、声音和接缝表现。
