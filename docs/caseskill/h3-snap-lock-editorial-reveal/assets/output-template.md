# H3 音频事件驱动的快照与硬锁：输出工作表

将本文件复制到任务目录并填写；它是规划/交付模板，不是直接送入 H3 的全部正文。填写完的计划、参考权限和审计记录与生成提示词分开保存。

## 1. 当前任务与输入

| 输入项 | 当前任务值、来源与待核验内容 |
|---|---|
| 视觉参考与范围 | 提供图像参考及身份/服装/环境职责，不凭空描写图中外貌。给出允许的景别、是否允许面部近景和所需揭示顺序，服从当前任务的裁切范围。 |
| 音频事件 | 提供实际音频、窗口和已核验onset/主重音/末事件；无测量时标missing或使用用户指定计划点，不沿用源2.050/5.100冒充新曲测量。 |
| 时间与帧率 | 提供总时长、fps、每次burst与lock最少可读帧预算、冲击数和误差范围；未给fps不得报告同帧控制。 |
| 旋转与执行版本 | 定义原图为绝对roll零点，明确顺时针的观察坐标、每段绝对角度及最后是相对旋转还是目标朝向。执行以英文离散两态规则为基线，中文文件按教学改写读取。 |

## 2. 本案例交付

### 两态帧表

start/end帧、对应时间、HARD_LOCK/BURST、构图、绝对roll、delta_roll、运动类型和人物微动权限。

### 音频事件映射

事件ID、来源/测量状态、触发的视觉事件、原始时点与量化时点/误差。

### 冲击与旋转决策记录

冲击数和最少帧预算、绝对朝向轨迹、源文冲突的取舍及blocked项。

### 完整H3快照提示词

视觉参考、相机两态与时间边界、人物动作、画面清晰恢复和最终锁定，避免夹带教学改写冲突。

### 逐事件验收

实际运动/静止帧、可数冲击、roll与人物姿态、音画事件差和未生成状态。

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
| SLR01 | HARD LOCK和INSTANT BURST互斥；所有相机运动必须完全落在burst窗口，不能拖入静态区。 | unverified | 填入实际检查记录 |
| SLR02 | 相机硬锁不等于后期freeze-frame；人物可以保留已允许的呼吸、眼动和发丝微动。 | unverified | 填入实际检查记录 |
| SLR03 | 图像拥有所声明视觉职责，音频拥有事件时间；更换音频后重新建立时间表，不能套源毫秒点。 | unverified | 填入实际检查记录 |
| SLR04 | 相机绕光轴的roll与身体转向分开，必须记录绝对取向及累计关系。 | unverified | 填入实际检查记录 |
| SLR05 | 三次冲击要逐个占用可检查帧并回稳；极短区间的可读性要经实际帧率和视频确认。 | unverified | 填入实际检查记录 |
| SLR06 | 英文执行稿与中文教学改写不等价，不混合即刻启停与另加预备加减速的规则。 | unverified | 填入实际检查记录 |
| SLR07 | 编辑式快照是分立构图逻辑，不自动等同一条真实摄影机连续扫过身体的路径。 | unverified | 填入实际检查记录 |
| SLR08 | 8fps以上密采样只是源作者建议，原帧核对和音频标注才是具体事件证据；成片相似不唯一证明源结构。 | unverified | 填入实际检查记录 |

记录静态检查结果、仍缺素材/测量、是否已实际生成，以及实际生成后才可评估的身份、动作、声音和接缝表现。
