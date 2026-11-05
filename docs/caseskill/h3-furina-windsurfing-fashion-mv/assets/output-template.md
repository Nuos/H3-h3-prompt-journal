# H3 分层参考与帆板写真 MV 高潮编排：输出工作表

将本文件复制到任务目录并填写；它是规划/交付模板，不是直接送入 H3 的全部正文。填写完的计划、参考权限和审计记录与生成提示词分开保存。

## 1. 当前任务与输入

| 输入项 | 当前任务值、来源与待核验内容 |
|---|---|
| 当前人物与装备资产 | 列出人物身份图、服装/多视角图和帆板装备图的实际文件、用途、可见特征与缺项。人物身份、衣服、鞋、板体、桅杆、boom、帆和索具分别核对；不可见结构写 unknown，未提供文件写 missing。源角色的蓝眼、冠饰和蓝白配色不自动继承到新任务。 |
| 分段摄影参考与权限 | 分别提供前两段的摄影指导图，说明构图、主体尺度、跟拍方向与摄影机高度；第三段是否沿用源案例的无摄影图策略须明确。指导图的箭头、版面和文字不是场景内容；若图文运镜冲突，先选定或重做同一个摄影意图。 |
| 输出长度与生成模式 | 记录成片长宽比、编辑时间线 fps、每段 generation_duration、edit_duration、局部/全局窗口与实际输入模式。标准 H3 每次生成 4–15 秒、24FPS；45 秒成片需要多个生成任务再装配。精确首帧约束与多图参考不能只靠在 Ref2VA 文本里写 FIRST FRAME 就视为同一能力。 |
| 运动与跨段状态 | 给出运动类型、允许动作、板航向、身体重心、手握 boom 的位置、脚位、帆角、风向、浪相位与摄影机相对位置。提供前段批准的实际 OUT 帧或逐项状态记录；未生成时标 planned，不伪装成已检查的连续性。 |
| 音乐与事件证据 | 提供完整原音轨、测量过的 BPM/拍号/重拍/乐句时码及来源，或声明只有音乐设计目标。源文约 128 BPM 和局部 3 秒/9–10 秒窗口不能当成当前音频的实测结果；本任务没有音频时不创建假 Audio 标签。 |
| 外部配乐与交付接口 | 明确完整视频版本、提取音频版本、交给 Suno 或其他工具的完整参考轨、返回配乐文件与版本、最终时长和同步容差。工具能力与素材尚未核验时只输出交接计划，不虚构 Suno 参数、生成结果或固定时长承诺。 |

## 2. 本案例交付

### 资产与参考权限表

实际文件/版本、局部标签、人物/装备/摄影/声音职责、保留范围、明确排除、缺失或不可见信息、每段是否启用。

### 三段状态与时间表

段落职责、generation_duration、edit_duration、fps、局部/全局窗口、IN/OUT 状态、接续证据与缺项；计划状态与实际批准帧分列。

### 逐段官方格式提示词

每段完整独立的 Ref2VA 六字段英文输出，或按真实模式切换后的三字段输出；正文有可见动作、摄影和声音因果，第三段明确无摄影参考而保留角色/装备来源。

### 动作—摄影—音乐事件表

Drop、预备、板离水、可读主视觉、板触水、释放及收尾的局部/全局时间、planned/measured 来源、动作状态与摄影状态。

### 装配与配乐交接单

片段选择、裁切、全片版本、完整参考音频、外部重制任务、返回轨版本、各声层职责，以及新音乐事件/原视频事件/偏差/修正/复验的对位记录。

### 验收及证据边界

两道接缝、装备接触、波浪和风、水花因果、主视觉可读性及最终音画同步；未实际生成、媒体缺失、未测量音频和源作者经验单独列明。

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
| FWM01 | 把人物身份、装备结构和当段摄影关系分别赋予参考权限；不复制多视角版面或图示箭头，并先解决人物图与装备图的服装冲突。 | unverified | 填入实际检查记录 |
| FWM02 | 源策略第三段只移除摄影指导图，仍保留人物与装备参考；这是为当前高潮重新设计镜头，不是跨段记忆清除或所有任务都应减少图片。 | unverified | 填入实际检查记录 |
| FWM03 | 独立生成的片段必须显式交接运动和构图状态；同一静态定妆图不能同时充当三个互不相同的精确开场帧。按实际模式处理接续素材，文字开场指令仍须结果核验。 | unverified | 填入实际检查记录 |
| FWM04 | 三段按建立高速运动、逼近更大浪壁、最终受控腾空递进；第二段不得提前完成最终跳跃，第三段回水后不再新增主要动作。 | unverified | 填入实际检查记录 |
| FWM05 | 高潮保持帆板运动及装备连接：上浪→离水→空中→下降→板触水→继续滑行；landing 是板体回水，不是人物跌落水中。源动作不含后空翻、复杂旋转或海啸水墙。 | unverified | 填入实际检查记录 |
| FWM06 | Hero Shot 稳定的是摄影构图和运镜强度，人物、帆板、布料和海浪继续运动。主视觉需同时看清人物、帆、板与离水间隙；近景长焦不等于摄影机物理距离必须极近。 | unverified | 填入实际检查记录 |
| FWM07 | 区分原文报告、当前设计目标与实际音频测量；mini-turnaround 是音乐转接。没有当前音频不得编造 BPM、重拍或最强重音时码。 | unverified | 填入实际检查记录 |
| FWM08 | 完整视频先装配，完整音频再交给外部配乐重制，返回音轨必须重新对齐全片事件；不把 Suno 重制视作固定时长或保留原始拍点的保证。 | unverified | 填入实际检查记录 |
| FWM09 | 源三段自由格式提示词需按实际模式迁移为官方 Ref2VA 六字段或基础模式三字段。标准生成每片 4–15 秒、24FPS；多段成片总时长、剪辑帧率和裁切时长单列，不能冒充一次生成能力。 | unverified | 填入实际检查记录 |
| FWM10 | 参考图等权、撤图更有效、Suno 更连贯均保留为源作者的经验或意图，不写成模型内部机制或已验证保证；源资产缺失和实际未执行的部分必须明示。 | unverified | 填入实际检查记录 |

记录静态检查结果、仍缺素材/测量、是否已实际生成，以及实际生成后才可评估的身份、动作、声音和接缝表现。
