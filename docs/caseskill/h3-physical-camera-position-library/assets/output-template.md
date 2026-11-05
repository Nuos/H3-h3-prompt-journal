# 物理摄影机机位：八要素编排与兼容检查：输出工作表

将本文件复制到任务目录并填写；它是规划/交付模板，不是直接送入 H3 的全部正文。填写完的计划、参考权限和审计记录与生成提示词分开保存。

## 1. 当前任务与输入

| 输入项 | 当前任务值、来源与待核验内容 |
|---|---|
| 拍摄对象与空间 | 提供主体、场景地面/墙面/障碍、运动轨迹和可用机位空间；区分实际已知与假设。 |
| 机位意图与画幅 | 记录观众应看见的身体部位、环境关系、景别与画幅，再选机位，不仅收集形容词。 |
| 时间与运动策略 | 给每个机位持续区间及主体移动；明确相机锁定、跟随、平移、俯仰、滚转或组合。 |
| 项目约束 | 记录是否禁数值角度、是否要求保留肩颈/全身、是否允许贴近透视及设备入镜；未指定时不强加其他案例政策。 |

## 2. 本案例交付

### 机位参数与兼容表

逐镜方位、高度、距离、光轴、滚转、移动模式、主体路径、可见部位及假设来源。

### 八要素机位描述

可以嵌入当前H3主字段的自然英文句子，与实际时间区间绑定。

### 构图验收与修复建议

预测可见几何、可能误解、冲突消解及待生成验证项目；不把文本检查当画面成功。

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
| CP-01 | 每镜明确机位的八要素，不把25条模板全部堆入同一提示词。 | unverified | 填入实际检查记录 |
| CP-02 | 位置高度、镜头方向和绕光轴滚转分别建模；荷兰角不等于低机位或高机位。 | unverified | 填入实际检查记录 |
| CP-03 | 正上方应同时满足相机在主体正上方、光轴垂直地面；斜上方保留面部可见度是另一方案。 | unverified | 填入实际检查记录 |
| CP-04 | 贴地、后跟、手持等描述保留其真实空间与运动关系，不用裁切、身体伸缩或独立旋转主体伪造透视。 | unverified | 填入实际检查记录 |
| CP-05 | 静止相机与持续跟拍不能在同一时段无说明并存；组合必须明确阶段及转换路径。 | unverified | 填入实际检查记录 |
| CP-06 | 仅在项目明确启用NO DEGREE时，将角度数字改成相对空间几何，保持垂直/斜向/侧前后关系；库本身含数值角度。 | unverified | 填入实际检查记录 |
| CP-07 | 对原库的模型效果保证改写为验收目标；当前材料无对照数据证明物理描述必然胜过短角度标签。 | unverified | 填入实际检查记录 |
| CP-08 | 设备隐藏是该子技能的默认设计要求；若任务明确拍摄剧组设备，按任务重设，而不是把摄影机物理描述误生成为画内摄影机。 | unverified | 填入实际检查记录 |

记录静态检查结果、仍缺素材/测量、是否已实际生成，以及实际生成后才可评估的身份、动作、声音和接缝表现。
