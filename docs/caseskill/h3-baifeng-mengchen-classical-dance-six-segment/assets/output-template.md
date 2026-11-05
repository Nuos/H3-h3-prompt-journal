# 白凤蒙尘：动链反推与双生成匹配剪辑：输出工作表

将本文件复制到任务目录并填写；它是规划/交付模板，不是直接送入 H3 的全部正文。填写完的计划、参考权限和审计记录与生成提示词分开保存。

## 1. 当前任务与输入

| 输入项 | 当前任务值、来源与待核验内容 |
|---|---|
| 视觉权威与动作起点 | 明确图1控制的人物/服装/环境范围，并区分实际首帧与身份场景参考；后段给上一段真实出口。 |
| 音乐与分段 | 提供源音频、全曲窗口、BPM/拍号/首拍依据、局部时长和是否仅复用原音轨；未测数据标记为输入估计。 |
| 动链来源与叙事机制 | 给可用动作链版本/正文、身体高度与支撑点变化、旋转和恢复意图；没有外部动链库时只采用随案可读动作，不假装调用未提供模块。 |
| 生成与剪辑环境 | 记录实际模型/平台支持时长、输出fps、是否允许整段重复采样、计划接缝时间及额外素材余量；不从原案例猜平台能力。 |

## 2. 本案例交付

### 动作链与镜头表

全局/局部时间、入态、支撑、动作因果、主机制、特写信息和出态。

### 原稿档案与可提交修订稿

只读来源、工程变更说明、官方Ref2VA正文及准确的段间接口。

### 双生成执行/取用清单

每次输入图/音频/提示词版本、生成时长、source local in/out、目标时间、fps及接缝余量。

### 匹配剪辑与验收记录

身体/手轨迹/相机共同相位、实际选帧、音轨连续、缺陷和待生成验证项。

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
| BM-01 | 动作链必须写入态、动力、承重、路径、峰值、回收和出态；动作名或形容词不能替代过程。 | unverified | 填入实际检查记录 |
| BM-02 | 段内特写改变观察信息，段间匹配保持动作状态；二者分别设计。 | unverified | 填入实际检查记录 |
| BM-03 | 档案原文与当前可提交修订稿分别保存；旧SEG03入出态冲突必须在实际正文和边界表同时修复。 | unverified | 填入实际检查记录 |
| BM-04 | 双生成方案必须给出两次真实输入、生成时长、取用区间和最终位置，不能只写完整原文不拆或前后各生成一次。 | unverified | 填入实际检查记录 |
| BM-05 | 平台时长限制从当前运行时核实；原文12.455秒双生成选择不是H3统一只能生成半段的证据。 | unverified | 填入实际检查记录 |
| BM-06 | 同一音乐源的连续窗口在剪辑处不重启；实际接缝以帧率与选帧记录定义。 | unverified | 填入实际检查记录 |
| BM-07 | 参考图的身份/环境权威不能与跨段动作起点混淆；没有精确首帧用途时不强制整图首帧复制。 | unverified | 填入实际检查记录 |
| BM-08 | 甩发揭眼、低位起身及反向截断都要有具体支撑和运动因果；不得用新增人物、道具或无因抖动替代本任务的身体表演。 | unverified | 填入实际检查记录 |
| BM-09 | 原案0.25–0.55秒特写、最多一次全转、无对白/口型是片风格规则；迁移时按任务保留或调整。 | unverified | 填入实际检查记录 |

记录静态检查结果、仍缺素材/测量、是否已实际生成，以及实际生成后才可评估的身份、动作、声音和接缝表现。
