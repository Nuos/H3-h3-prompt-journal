# 夏日人物MV：特殊机位与切镜事件分离：输出工作表

将本文件复制到任务目录并填写；它是规划/交付模板，不是直接送入 H3 的全部正文。填写完的计划、参考权限和审计记录与生成提示词分开保存。

## 1. 当前任务与输入

| 输入项 | 当前任务值、来源与待核验内容 |
|---|---|
| 身份图与属性政策 | 明确保留身份、发型、体型和哪些服装细节，列每场景允许改变的衣物/湿发状态，避免把身份一致等同服装绝不变化。 |
| 分段与音频窗口 | 提供每段时长和源音频起止、使用方式、是否允许新增环境音；没有音乐分析时，镜头切点仅记为设计时间。 |
| 场景/机位/动作 | 提供泳池、海滩、水线或其他场景及相机位置、光轴、滚转、移动路径；列人物支撑、水、毛巾、家具的接触关系。 |
| 风格与衔接优先级 | 选定整片色调、局部暖光是否允许、段际采用硬切还是动作接力，以及前后场景和道具状态。 |

## 2. 本案例交付

### 身份/服装/场景政策表

每场景固定属性、允许变化、冷暖光规则、音频复制/混音规则。

### 分段镜头与事件表

source/local时间、cut/phase/segment_boundary、镜头数、段际接力状态。

### 物理机位与接触关系表

位置、高度、光轴、滚转、路径、预期可见几何和手/道具/水/座位状态。

### 逐段官方提示词与验收清单

自包含Ref2VA正文和视频生成后需要检查的切点、身份、服装、色调、接触及水线。

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
| SM-01 | 身份保留与服装保留独立定义，且每个独立生成任务重新绑定实际身份资产。 | unverified | 填入实际检查记录 |
| SM-02 | 切镜、连续阶段和段际拼接分别登记；时间标记不自动意味着新增Shot。 | unverified | 填入实际检查记录 |
| SM-03 | 音乐源时间与local时间明确换算；未给重音表时不把整数设计切点宣称为实测卡点。 | unverified | 填入实际检查记录 |
| SM-04 | 特殊视点由相机位置/光轴/滚转和环境几何构成，人物身体保持正常重力关系。 | unverified | 填入实际检查记录 |
| SM-05 | 固定贴地镜头在起身过程中保持原位；从该视点转到新场景须依设计cut完成，不能偷偷变成跟拍。 | unverified | 填入实际检查记录 |
| SM-06 | 泡沫是镜头附近的前景层，水线为持续空间约束；泡沫不附着到脸上且不全程挡脸。 | unverified | 填入实际检查记录 |
| SM-07 | 服装、冷暖色调与音频混音政策必须在四段一致或明确标注局部例外，不能互相冲突。 | unverified | 填入实际检查记录 |
| SM-08 | 擦发、放毛巾、起身和跨段入口都要保持手—道具—身体接触与状态连续。 | unverified | 填入实际检查记录 |

记录静态检查结果、仍缺素材/测量、是否已实际生成，以及实际生成后才可评估的身份、动作、声音和接缝表现。
