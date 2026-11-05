# 紫纱亭舞：主动力轮换、实物交接与服装显色：输出工作表

将本文件复制到任务目录并填写；它是规划/交付模板，不是直接送入 H3 的全部正文。填写完的计划、参考权限和审计记录与生成提示词分开保存。

## 1. 当前任务与输入

| 输入项 | 当前任务值、来源与待核验内容 |
|---|---|
| 参考分权表 | 分别指定人物/服装/环境图片、动作文字来源、分段音频及其参考或复制角色，明确是否附动作视频。 |
| 音乐时间依据 | 提供实际音频标识、切割manifest、BPM/拍号/首拍和可核实歌词onset；没有manifest时将既有数字标为作者记录或用户输入。 |
| 不变外观与可见性 | 列服装材质/色彩、面纱是否始终遮挡，以及允许可见的轮廓范围；只锁用户指定属性。 |
| 动作与交接要求 | 给分段意图、主动力候选、承重/高度变化、首尾交接物和最终收势，区分舞蹈表达与逐字表演歌词。 |

## 2. 本案例交付

### 音乐与分段manifest

全局区间、真实局部时长、首拍/歌词事件来源、局部换算、末端覆盖。

### 主动力与交接矩阵

每段主导机制、跟随部位、左右肢体/衣料交接物、位置高度、方向、首镜可见性。

### 可见性及显色方案

服装不变量、面纱允许可见范围、主体与背景光色关系、代表镜头试验与待验证指标。

### 逐段H3正文与Gate报告

官方字段提示词、清晰动作时间线、音频角色、越界/漏时/交接/遮面检查。

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
| PV-01 | 段内具体动作的先后、路径、支撑与出态优先于spiral/wave等质量词堆叠。 | unverified | 填入实际检查记录 |
| PV-02 | 主动力轮换按段落计划执行；复合高潮按顺序展开，不将全部部位同时设为主动力。 | unverified | 填入实际检查记录 |
| PV-03 | 匹配剪辑必须匹配具体交接物、左右、空间高度和运动方向，且对象在后段首镜可见。 | unverified | 填入实际检查记录 |
| PV-04 | 全局边界决定局部段长；所有动作区间必须覆盖且不越过该长度，首拍和歌词时间各自保留来源。 | unverified | 填入实际检查记录 |
| PV-05 | 全程面纱锁与眼睛/上脸显露不能并存；按任务选定可见性政策后同步正文与交接表。 | unverified | 填入实际检查记录 |
| PV-06 | 侧弓步的支撑脚、伸腿接地和膝不触地条件要显式，不能靠低位形容词代替。 | unverified | 填入实际检查记录 |
| PV-07 | 紫衣显色方案仅为案例假设/作者经验；通过小规模输出核验后再推广，不称为所有材质的色彩定律。 | unverified | 填入实际检查记录 |
| PV-08 | 音频节奏参考与最终信号复用分开；无歌词manifest时不声称已经实测对齐。 | unverified | 填入实际检查记录 |

记录静态检查结果、仍缺素材/测量、是否已实际生成，以及实际生成后才可评估的身份、动作、声音和接缝表现。
