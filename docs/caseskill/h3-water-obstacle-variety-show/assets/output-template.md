# 剧情锚点驱动的水上闯关与失败反转：输出工作表

将本文件复制到任务目录并填写；它是规划/交付模板，不是直接送入 H3 的全部正文。填写完的计划、参考权限和审计记录与生成提示词分开保存。

## 1. 当前任务与输入

| 输入项 | 当前任务值、来源与待核验内容 |
|---|---|
| 主角与参考权限 | 确认人物身份图和允许保留的外观属性；本方法默认图像只约束身份、服装和可见配饰，赛道、观众及摄影由文字另行定义。不要将静态图认作声音或动作证据。 |
| 挑战、结局与必要事件 | 给出起点、障碍序列、接近成功的条件、反转原因和喜剧收尾；逐个标明不可删事件及可换障碍。未指定时可按案例结构提出可替换方案。 |
| 时长、对白与声画要求 | 记录总创作时长、开场与结束台词、是否必须严格无切镜。将未知语言、配音、音乐或字幕要求列为 missing；剧情节拍不推导为 BPM。 |
| 执行自由度与可用素材 | 分别列出可由模型决定的步法、闪避、观众反应、镜头及声音时序；记录是否已有前段末帧、真实音轨和平台支持的规格。 |

## 2. 本案例交付

### 身份与自由度契约

人物参考绑定、场地生成范围、不可变项和明确允许变化项。

### 剧情依赖与状态表

必要事件、前提、结果、位置、支撑/抓握、干湿状态及跨片交接。

### 时间预算和H3正文

故事总时间、4–15秒生成切片、每段剧情与自由度、对白和声画事件关系。

### 验收与修订记录

逐事件勾选、顺序错误、场地跳变、干湿错误、台词缺失和可操作修复；区分文本检查与尚未执行的生成验证。

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
| W1 | 参考图只锁定已约定的人物身份与外观；新增场地和游戏道具由文本定义，不从身份图臆造。 | unverified | 填入实际检查记录 |
| W2 | 必经剧情按因果顺序执行，抓牢先于侧击，侧击导致失握，入水先于湿发收尾。 | unverified | 填入实际检查记录 |
| W3 | 在不破坏必要事件的条件下，明确授权模型选择微动作、镜头、表演和观众反应；自由不能取消锚点。 | unverified | 填入实际检查记录 |
| W4 | 同一赛道、终点墙与相邻水池保持连通，人物从真实上一状态继续；切镜不重置位置或干湿状态。 | unverified | 填入实际检查记录 |
| W5 | 故事节拍不等同于音乐音头；无音轨时只能提出音乐情绪与事件关系。 | unverified | 填入实际检查记录 |
| W6 | 时间不足时先压缩可选反应、重复闪避和解说，保留反转因果与收尾对白；长创作方案另拆生成片段。 | unverified | 填入实际检查记录 |
| W7 | “一镜到底般的感觉”仅指连续观感，原案允许八个镜头；严格无切镜必须单独设计和检查。 | unverified | 填入实际检查记录 |
| W8 | 0.3、0.8、1是未明确单位的作者经验，不作为官方参数、价格、速度或提高规格后动作不变的保证。 | unverified | 填入实际检查记录 |

记录静态检查结果、仍缺素材/测量、是否已实际生成，以及实际生成后才可评估的身份、动作、声音和接缝表现。
