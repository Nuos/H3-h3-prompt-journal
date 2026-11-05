# 双图分权半身舞：身份、首帧动作与镜头职责分离：输出工作表

将本文件复制到任务目录并填写；它是规划/交付模板，不是直接送入 H3 的全部正文。填写完的计划、参考权限和审计记录与生成提示词分开保存。

## 1. 当前任务与输入

| 输入项 | 当前任务值、来源与待核验内容 |
|---|---|
| 两张图片的属性权限 | 记录脸部身份、发型、服装、体型、场景、光向各由哪张图提供，哪些姿势、手位、朝向和构图不继承。 |
| 首帧舞谱/交接态 | 给从0秒起的支撑脚、膝预载、重心方向、手臂起点与目标；后段优先继承上一段出口，而非每段新建无关站姿。 |
| 音频与全局映射 | 提供每段真实音频、全曲起止、BPM/首拍和片段时长；无全曲偏移时标明仅有局部数据。 |
| 镜头风格与可见范围 | 指定半身距离、手持响应、肩颈/手部边界、重要步法是否需要短暂展示以及当前图2与调色方案的优先级。 |

## 2. 本案例交付

### 双图属性权限表

脸、发型、服装、体型、环境、光向、姿态、构图的授权/排除与冲突优先级。

### 连续时间与接合表

全局起止、局部拍点、0秒预载、段间支撑/朝向/手位/动量/镜位接口。

### 肖像舞镜头与提示词

舞句、关键足部可见窗口、动作中切镜、高光观看位置及官方Ref2VA正文。

### 首帧泄漏及连续性Gate

参考角色检查、动作空白检查、段缝一致性和实际输出待核验清单。

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
| ID-01 | 每张图片必须同时说明授权属性和不继承属性；身份参考不自动成为首帧姿态参考。 | unverified | 填入实际检查记录 |
| ID-02 | 禁止照片姿态后，必须给出正向动作来源；0秒至首拍的预载/余势不可留白。 | unverified | 填入实际检查记录 |
| ID-03 | 后段开场与前段出口逐字段配对，不能用各段新的dance-ready position代替跨段连续性。 | unverified | 填入实际检查记录 |
| ID-04 | 半身感限定相机距离和可见范围，不授权复制照片的头角、手位、身体朝向或静态构图。 | unverified | 填入实际检查记录 |
| ID-05 | 关键足部动作须有实际可见窗口；半身偏好与全身技法冲突时调整观看位置，不写看不见的技术验收。 | unverified | 填入实际检查记录 |
| ID-06 | Motion Cut保持同动作、方向、肢体轨迹、重心与动量；高光峰值不自动要求停住。 | unverified | 填入实际检查记录 |
| ID-07 | 全曲与局部音频必须有可追溯映射，局部数字不能被当成全曲测量；六段时长仅为案例样本。 | unverified | 填入实际检查记录 |
| ID-08 | 旧案冷白银灰/金色及动中结束是可选片风格；换参考图时必须声明与新光照的优先级。 | unverified | 填入实际检查记录 |

记录静态检查结果、仍缺素材/测量、是否已实际生成，以及实际生成后才可评估的身份、动作、声音和接缝表现。
