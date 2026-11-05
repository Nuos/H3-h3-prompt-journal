# 双人异速：动作完成数、观察延迟与可见性：输出工作表

将本文件复制到任务目录并填写；它是规划/交付模板，不是直接送入 H3 的全部正文。填写完的计划、参考权限和审计记录与生成提示词分开保存。

## 1. 当前任务与输入

| 输入项 | 当前任务值、来源与待核验内容 |
|---|---|
| 角色参考与稳定身份 | 指出每张图中各角色的可识别特征及初始位置，分别绑定主体；一张图片可定义两个主体，摄影机绕行后仍按身份而非屏幕左右编号。 |
| 可计数动作单元 | 给出动作开始/完成姿态、是否允许不同单元、连续衔接方式。计数脚步需脚部可见；近景可选膝、髋或手臂的完整循环作为判据。 |
| 时间关系 | 给定总时长、动作完成数比例、统计窗口、容差及观察延迟；原案未给总时长或BPM，不把它们补成历史事实。 |
| 摄影与声音 | 记录近景、环绕路径、最低入画部位、能否放宽景别，以及器乐/人声要求和实际音频是否已提供。 |

## 2. 本案例交付

### 主体与事件定义

快慢Subject映射、动作单元进入/完成姿态、判据可见部位及参考权限。

### 双人配对事件表

观察前导、δ、两人各事件起止、完成时刻、窗口归属、目标/计划完成数和比例容差。

### 摄影及声音组件或完整提示词

按任务提供连续环绕组件，或正确模式的英文H3正文；中文时序与待核验项在正文之外。

### 逐项验收记录

区分计划计数与生成后实测计数，记录遮挡、同步化、追赶和身份串位等失败。

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
| DS-01 | 两个角色保持独立稳定身份；一张输入图不等于一个Subject，绕行后不按当前屏幕左右重新分配快慢角色。 | unverified | 填入实际检查记录 |
| DS-02 | 完成数比例必须附动作单元起止、统计窗口和容差；比例只在定义的窗口验收，不能替代逐事件计数。 | unverified | 填入实际检查记录 |
| DS-03 | 响应延迟、执行时长、累计落后分别建模；3∶1完成数不等于所有身体部位瞬时速度恒为三倍。 | unverified | 填入实际检查记录 |
| DS-04 | 慢者仅模仿此前看见的动作，不预知下一动作；快者持续衔接，慢者不突然追赶恢复同步。 | unverified | 填入实际检查记录 |
| DS-05 | 计数判据必须在当前景别中可见；腰至头顶或膝上构图不能声称验证了被裁掉的完整脚步。 | unverified | 填入实际检查记录 |
| DS-06 | 近距离环绕可连续通过不同视角，不等于横摇、画面滚转或新增切镜；两人身份与动作相位贯穿镜头。 | unverified | 填入实际检查记录 |
| DS-07 | 沿用原案纯器乐时排除各种人声，但音乐仍是有效声音；若用户改声音策略，以当前明确任务为准。 | unverified | 填入实际检查记录 |
| DS-08 | 作者“约三倍”是结果报告；没有真实媒体计数时，不声称本次已达到比例或能保证模型稳定异速。 | unverified | 填入实际检查记录 |

记录静态检查结果、仍缺素材/测量、是否已实际生成，以及实际生成后才可评估的身份、动作、声音和接缝表现。
