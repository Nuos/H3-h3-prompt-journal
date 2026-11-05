# 音乐事件驱动的古典武侠舞分段编排：输出工作表

将本文件复制到任务目录并填写；它是规划/交付模板，不是直接送入 H3 的全部正文。填写完的计划、参考权限和审计记录与生成提示词分开保存。

## 1. 当前任务与输入

| 输入项 | 当前任务值、来源与待核验内容 |
|---|---|
| 作品定义 | 记录舞种、情绪能量曲线、每段功能、主要动作与观众必须看到的信息；选择独立蒙太奇、连续动作匹配剪辑或分组一镜到底。 |
| 视觉与道具参考 | 登记图像对身份、服装、场景、灯光、姿势的授权范围，以及现有武器／道具的数量、佩戴或持握方式、相对身体位置与可变状态。 |
| 音乐与分段清单 | 提供源起止、音频文件标识、实际段长、BPM与首拍或拍点表、人声事件和器乐间隙；标出实测、用户给定、从BPM推算和未知。 |
| 动作预算 | 给定风格、动作能力边界、旋转／跳跃／地面段预算、主母题和高潮位置；动作密度由音乐及完整准备恢复时间决定。 |

## 2. 本案例交付

### 作品与参考契约

舞种与能量曲线、剪辑模式、图像授权、武器分支及保持范围、音频最终使用策略。

### 统一音乐事件表

源文件、源起止、段长、局部拍点／人声起止／器乐窗／cut，来源及精度标签，提前动作与入句动作的对应关系。

### 动作与接缝计划

母题发展、每链动力过程、可见技术信息、镜头目的，以及连续边界的身体／道具／构图匹配表。

### 逐段Ref2VA提示词与审计

各自完整的官方六字段执行文本，末段器乐收束，已修复的文本冲突、仍缺媒体证据和待运行回归项。

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
| WX01 | 作品意图、音乐和编舞先于镜头；删除相机文字后动作仍应成立。 | unverified | 填入实际检查记录 |
| WX02 | 动作链包含准备、受力、展开、重音峰值、惯性和恢复；持续层不是所有身体部位始终移动。 | unverified | 填入实际检查记录 |
| WX03 | 母题通过质地、方向、幅度和先后变化贯穿作品；动作密度和技术预算不采用固定数量公式。 | unverified | 填入实际检查记录 |
| WX04 | 源窗口与局部时间分开，拍点／人声起止／剪辑点分别建事件，缺manifest不等于有实测精度。 | unverified | 填入实际检查记录 |
| WX05 | S05的6.044和9.000不能标作6.950和9.633人声的入句时刻；允许提前动作，但应说明提前与对应事件。 | unverified | 填入实际检查记录 |
| WX06 | 图像权威随项目授权；歌词意象不增添物体，武器状态锁定要区分无武器、佩戴入鞘和实际持握。 | unverified | 填入实际检查记录 |
| WX07 | 摄影机说明真实位置与路径；每次切镜或移动必须提供支撑、线条、方向或音乐结构的新信息。 | unverified | 填入实际检查记录 |
| WX08 | 音乐首尾相连与身体接缝是两项检查；跨段连续必须有状态表，蒙太奇跳接必须明确许可。 | unverified | 填入实际检查记录 |
| WX09 | 无歌词、间奏和尾奏仍编排动作；最终收束以实际音频尾为目标，不把缺歌词当成静止指令。 | unverified | 填入实际检查记录 |
| WX10 | 成品时间戳只代表编排意图；按官方Ref2VA字段归一后，文本检查、音频核验和生成回归分别报告。 | unverified | 填入实际检查记录 |

记录静态检查结果、仍缺素材/测量、是否已实际生成，以及实际生成后才可评估的身份、动作、声音和接缝表现。
