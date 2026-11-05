# 以道具状态与单镜头组织长篇表演MV：输出工作表

将本文件复制到任务目录并填写；它是规划/交付模板，不是直接送入 H3 的全部正文。填写完的计划、参考权限和审计记录与生成提示词分开保存。

## 1. 当前任务与输入

| 输入项 | 当前任务值、来源与待核验内容 |
|---|---|
| 作品与场景权限 | 选择固定参考现场或可替换背景；列出身份、服装、道具、环境、天气和光向的图像授权与排除范围，并定义表演或剧情定位。 |
| 道具状态配置 | 登记道具数量、设计来源、解剖学持握手、鞘所在身体侧、初始状态、允许的拔出／收回区间和跨段是否允许开场重述。资产不可见时不猜测正确手。 |
| 音频与时间表 | 提供源窗、分段文件、段长、可靠拍点／首拍、歌词或器乐事件、音频最终使用政策；保留原裁切，不擅自切齐小节或重新起拍。 |
| 动作与镜头意图 | 为每段选一个主要视觉问题、动作链、一个主运镜及可选辅助、可见部位优先级和后期桥接母题。动作参考若只是文字转写，不虚构已上传Video引用。 |

## 2. 本案例交付

### 参考与状态配置

人物／场景权限、道具外观来源、数量、解剖学握持、鞘的身体附着、段级初态和转换窗口、开场重述许可。

### 音乐与段落设计表

源起止、文件、局部时点与证据级别、视觉问题、动作链、能量位置、主运镜与辅助、可见信息优先级。

### 独立Ref2VA执行文本

逐段完整六字段、英语正文、单Shot连续路径、当前状态覆盖参考初态、统一音频策略，不依赖全局说明或上段上下文。

### 后期桥接与双重审查记录

反光／发丝／剑线等匹配候选，段内与后期边界；状态、时间、镜头、场景、声音和作品完成感的文本审计，另列生成待验证项。

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
| KZ01 | 人物和场景的图像权限分别定义；固定现场与替换背景不能同时设为绝对权威。 | unverified | 填入实际检查记录 |
| KZ02 | 道具外观由参考继承，数量、持有人、位置和当前状态由时间表决定；后续状态覆盖参考图初始入鞘状态。 | unverified | 填入实际检查记录 |
| KZ03 | 原案S01和S02各自独立拔刀是已授权开场设计；应修S02前文／正文矛盾及S01两个拔出时间，而非擅自删除第二次。 | unverified | 填入实际检查记录 |
| KZ04 | 保留真实源窗和相位，不为整齐重切小节；BPM给间隔而不自动给每段首拍或人声时点。 | unverified | 填入实际检查记录 |
| KZ05 | 道具路径由脚步、重心、躯干及持握传递，峰值必须有制动和恢复；动作与镜头同时响应音乐。 | unverified | 填入实际检查记录 |
| KZ06 | 采用本案摄影政策时，一个主运镜至多一个辅助；数字角度要改成位置与路径，且摘要、动作行、相机段同步。 | unverified | 填入实际检查记录 |
| KZ07 | 每段一镜到底与后期匹配是不同阶段；两段一组不要求精确同帧续接，也不授权内部暗切。 | unverified | 填入实际检查记录 |
| KZ08 | 场景连续指同一空间、海岸线与光源逻辑，不等于不同机位下海平线永远占同一屏幕坐标；同一反光桥接必须指同一可见对象。 | unverified | 填入实际检查记录 |
| KZ09 | fully_copy表示完整最终音轨复用；新增环境声时必须改用混合保留方案，原案sole track加底声的冲突不可保留。 | unverified | 填入实际检查记录 |
| KZ10 | 六字段齐全、一个Shot标签和作者勾选只能证明文本结构；重编官方类型、Subject职责与英语正文后仍需另行验证媒体和生成。 | unverified | 填入实际检查记录 |

记录静态检查结果、仍缺素材/测量、是否已实际生成，以及实际生成后才可评估的身份、动作、声音和接缝表现。
