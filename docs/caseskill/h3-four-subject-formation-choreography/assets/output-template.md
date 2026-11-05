# H3 四主体身份锚与队形状态接力：输出工作表

将本文件复制到任务目录并填写；它是规划/交付模板，不是直接送入 H3 的全部正文。填写完的计划、参考权限和审计记录与生成提示词分开保存。

## 1. 当前任务与输入

| 输入项 | 当前任务值、来源与待核验内容 |
|---|---|
| 主体与场景资产表 | 提供参考图及四个主体的唯一ID、图中初始定位、稳定外观/服饰标记和场景权限。图中位置只用于首次识别，不能在换位后重分配ID；资产缺失标missing。 |
| 段落和音乐时间域 | 提供目标总时长、分段区间、已测beat/onset表及local/global映射；93.75 BPM与源k标签只用于复现本源材料，不能套给新曲。 |
| 场地、队形及通道 | 提供地面坐标约定、可用空间、禁入区、队形节点、交叉/层交换需求和可通过间隙；无空间证据时把避碰判断保留为规划待核验。 |
| 动作与接缝状态 | 提供每人动作风格、承重脚、躯干朝向、手臂运动和段末方向；后续段必须有前段outgoing状态，缺失时先建立接缝设计。 |

## 2. 本案例交付

### 身份锚与参考职责表

稳定Subject ID、参考定位、身份/服装/场景作用域、anchor版本和缺失资产。

### 逐人队形与穿越许可表

每个时间窗的起终位置、支撑脚、动作链、通道、参与交叉者、让行顺序、遮挡/避碰待核验项。

### 段落接缝表

每人OUTGOING/INCOMING对照，含位置、承重、躯干、手臂余势、方向和未解决差异。

### 完整片段提示词

固定锚和本段动态编排完整组装；可单独阅读，不依赖未提供的其他13段文本。

### 时序与证据核对表

local/global、beat来源、实际/计划状态，说明哪些结论仅来自案例文字及哪些未做连续生成验证。

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
| FSC01 | 同一任务的视觉锚逐段复用相同版本，主体ID不随站位与镜头前后变化重新编号。 | unverified | 填入实际检查记录 |
| FSC02 | 参考图负责已声明的身份/场景，后续段的起始动作来自INCOMING而非重新摆参考姿势。 | unverified | 填入实际检查记录 |
| FSC03 | 队形换位必须有支撑脚—承重—膝胯—肩臂—恢复的动作链，不能只有目的地或普通步行。 | unverified | 填入实际检查记录 |
| FSC04 | 主体动作性格和错拍关系保持可区分，共同重音之外不把四人写成同步复制。 | unverified | 填入实际检查记录 |
| FSC05 | 把中心交叉和层交换编码成局部许可；不同时保留全局不穿越和正文交叉动作。 | unverified | 填入实际检查记录 |
| FSC06 | 区分同距跟随后退与拉远揭示队形：前者可依动作使用，后者受本案例近景观看策略限制。 | unverified | 填入实际检查记录 |
| FSC07 | 每段OUTGOING与下一段INCOMING逐主体传承位置、承重、旋转、手臂路径和行进方向。 | unverified | 填入实际检查记录 |
| FSC08 | 歌词只塑造情绪/力度，不把歌词名词自动生成道具、特效或字幕；音频是否原样保留按任务职责显式声明。 | unverified | 填入实际检查记录 |
| FSC09 | 原14段总览、93.75 BPM和近零漂移自述不得当成完整工程与通用性能证据。 | unverified | 填入实际检查记录 |

记录静态检查结果、仍缺素材/测量、是否已实际生成，以及实际生成后才可评估的身份、动作、声音和接缝表现。
