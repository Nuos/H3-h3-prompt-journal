# 贴纸厨房喜剧：媒介边界、道具归属与四镜因果链：输出工作表

将本文件复制到任务目录并填写；它是规划/交付模板，不是直接送入 H3 的全部正文。填写完的计划、参考权限和审计记录与生成提示词分开保存。

## 1. 当前任务与输入

| 输入项 | 当前任务值、来源与待核验内容 |
|---|---|
| 角色图与媒介契约 | 提供角色参考、必须保留的轮廓/配色/服装/平面性，以及允许暂时变化的表情、泪、肿包、鼓嘴和二维特效。图片不自动把厨房或真人手变成卡通。 |
| 真实环境与参与者 | 说明实拍风格的厨房、锅/灶/凳子位置、POV方向、真人手的数量和动作职责；不得因换镜复制额外手或道具。 |
| 道具状态与所有权 | 记录盐罐开口、封盖是否存在、盐流入口/出口、每时段持有人；给出锅铲翻炒、轻敲、舀食的连续用途。 |
| 喜剧时间和声音 | 给总时长、四阶段或其他明确因果结构、实际切点、最低可读时间及容差；确认环境声、对白与配乐是否允许。 |

## 2. 本案例交付

### 媒介与角色职责表

二维/实拍归属、固定身份、允许变化、每阶段行动者及禁止行为的作用域。

### 道具状态和所有权表

盐罐开口、位置、持有人、盐流；锅铲在翻炒/轻敲/舀食/送入口各阶段的连续状态。

### 因果分镜与内部时间预算

真实Shot数量、切点、动作窗口、接触先后和最终保持范围；标明原参数与新增调度。

### 英文H3提示词及验收清单

官方模式字段、明确图片权限、声场策略，附逐镜二维外观、道具交接、动作路径和切点验证项目。

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
| SK-01 | 仅角色保持二维贴纸媒介；厨房、蒸汽、盐、锅和真人手保持实拍，不把角色图的画风扩散到全景。 | unverified | 填入实际检查记录 |
| SK-02 | 恒定身份与允许的暂时卡通表情/形变分开；鼓嘴、肿包、X眼和星星不构成整体三维化或新主体。 | unverified | 填入实际检查记录 |
| SK-03 | 倒盐所用罐口全程无遮挡，盐从实际开口流进锅；封盖禁令补充正向几何，不替代可见动作路径。 | unverified | 填入实际检查记录 |
| SK-04 | 人手不碰罐只约束Shot 1倒盐阶段；Shot 2夺罐必须有明确许可和所有权转移，不能互相冲突。 | unverified | 填入实际检查记录 |
| SK-05 | 原10秒结构为四镜头、三切点3/5/8秒；每镜头动作有可读时间，毫秒记法不是实测时间准确性保证。 | unverified | 填入实际检查记录 |
| SK-06 | 先倒入盐再喂同锅食物；同一锅铲和真实人手各司其职，接罐后的放置与再操作必须连续。 | unverified | 填入实际检查记录 |
| SK-07 | 瞬间僵住、刚性姿态微颤、随后跌落和最终保持构图分别定时，不能用全片冻结禁掉后续反应。 | unverified | 填入实际检查记录 |
| SK-08 | 环境声存在时overall_soundscape写厨房声，只有配乐缺席时non_diegetic_music为N/A；不得把无对白/无音乐误作绝对静音。 | unverified | 填入实际检查记录 |
| SK-09 | 媒介纳入身份、封盖否定清单属于案例方法；不声称身份指令必然优于风格指令，或一次样本证明所有混合媒介有效。 | unverified | 填入实际检查记录 |

记录静态检查结果、仍缺素材/测量、是否已实际生成，以及实际生成后才可评估的身份、动作、声音和接缝表现。
