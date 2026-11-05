# H3 触地事件驱动的服饰硬切：输出工作表

将本文件复制到任务目录并填写；它是规划/交付模板，不是直接送入 H3 的全部正文。填写完的计划、参考权限和审计记录与生成提示词分开保存。

## 1. 当前任务与输入

| 输入项 | 当前任务值、来源与待核验内容 |
|---|---|
| 固定视觉锚与可变属性 | 给出人物/场景参考和允许变化的服饰属性清单；身份、鞋、背景、机位等固定字段与袜饰例外必须分开。只声明可见/已提供信息，不重复虚构外貌。 |
| 状态序列 | 提供初态LOOK0及后续有序look表，明确转换次数N与状态总数N+1；缺新look参考时列missing或经任务允许按文字设计。 |
| 接触动作与参考 | 给出永久支撑脚、活动脚、足部接触表面和每轮起抬/触地/保持需求。Video1可选，但无视频时必须以动作表和明确时间代替，不引用不存在的Video1。 |
| 时间和声音 | 提供片长、输出fps、接触/音频事件来源、最小展示保持帧数及允许偏差；音频全量保留与新增音效两种策略明确选择，避免叠加重复触地声。 |

## 2. 本案例交付

### 固定属性与状态序列表

固定身份/环境/鞋/机位，可变服饰字段，LOOK0初态和N个后续状态。

### 接触—切换帧表

每轮lift_start、contact_time、contact_frame、cut_frame、hold_end、next_lift、旧/新look、音频事件和量化误差。

### 完整H3展示提示词

视觉锚、支撑关系、固定镜头、逐轮动作与外观状态、尾段和音频策略完整定义。

### 生成后事件验收表

逐轮实际接触帧/切换帧/稳定保持帧、支持脚偏移、非许可属性变化和失败修订。

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
| LCC01 | 触地为服饰切换的物理触发；旧look在空中和下降全程保持，切点不等于起抬点。 | unverified | 填入实际检查记录 |
| LCC02 | CONTACT→CUT→PLANTED HOLD→STABLE→NEXT LIFT有序；硬切立即成为新look，保持用于确认展示，不写成逐渐溶解。 | unverified | 填入实际检查记录 |
| LCC03 | 支撑脚保持位置和主要承重，活动脚只做紧凑抬落；换装前后身体/脚位/机位不发生附带跳变。 | unverified | 填入实际检查记录 |
| LCC04 | N次转换有N+1个状态；六次变化LOOK0→6实际是七状态。 | unverified | 填入实际检查记录 |
| LCC05 | 切点毫秒必须结合实际fps成为可核验帧号，不把“同帧”文本要求当成已获得的控制能力。 | unverified | 填入实际检查记录 |
| LCC06 | 全片时间必须覆盖；复现源5.17秒需补4.690–5.170尾段或明确改短总长。 | unverified | 填入实际检查记录 |
| LCC07 | 固定相机、同视角外观硬切、单次生成是三个不同概念，必须分别声明。 | unverified | 填入实际检查记录 |
| LCC08 | Video1缺失时用明确动作/事件表替代；原视频渐变属于被改写的形式，不能按外观或morph全量继承。 | unverified | 填入实际检查记录 |
| LCC09 | 原音轨全量保留与新增环境/接触声不能含混并用；声音策略必须明确并避免重复事件声。 | unverified | 填入实际检查记录 |

记录静态检查结果、仍缺素材/测量、是否已实际生成，以及实际生成后才可评估的身份、动作、声音和接缝表现。
