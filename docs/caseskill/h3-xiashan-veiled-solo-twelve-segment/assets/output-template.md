# 双图分权与面纱状态保护的多段独舞：输出工作表

将本文件复制到任务目录并填写；它是规划/交付模板，不是直接送入 H3 的全部正文。填写完的计划、参考权限和审计记录与生成提示词分开保存。

## 1. 当前任务与输入

| 输入项 | 当前任务值、来源与待核验内容 |
|---|---|
| 参考权威表 | 逐图登记可提供的信息。无头正面照只授权正面服装与身体；三视图可授权脸、发型、背部和穿戴物。环境、色调、姿势、首帧必须另列，不因一张图出现过就自动继承。 |
| 不可变资产清单 | 标明面纱、眼镜、头饰等的佩戴、遮挡、透明度和可变形边界，并给舞袖、环境纱帘等相近材质的物体独立名字。 |
| 时间与音频证据 | 提供全曲或分段时长、源起止、BPM／首拍或实测拍点、歌词 SRT／onset 表、最终音频使用策略；没有媒体或文件则标为用户给定／待验证，不能报告40/40通过。 |
| 舞蹈与镜头配置 | 给出主要动作驱动、技术峰值、地面段、静止定义、可用模式及适用段、空间演进和背景人物许可。将段数、旋转次数、半纱设计与相机高度视为项目参数。 |

## 2. 本案例交付

### 权威与资产配置

每张图的授权／排除属性，穿戴物、舞袖、门帘的状态与接触边界，背景与调色来源，镜头模式白名单。

### 时间和动作总表

源段界、段长、局部拍点、证据状态、链入态／出态、已分配拍数与余时、技术峰值和静止覆盖区间。

### 逐段可提交提示词

英语Ref2VA六字段、完整内联规则、真实切镜与镜头内阶段、统一音频使用策略；与只读原稿区分。

### 接缝与验证清单

相邻段可见对象／方向／支撑／速度表，静止切点例外，资产背景试段、双段接缝、地面、旋转、终止检查及尚未验证项。

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
| XS01 | 每段执行文本必须包含所需规则；统一配置负责维护，独立任务不依赖文件末尾全局段。 | unverified | 填入实际检查记录 |
| XS02 | 图像权威按属性分开，正面服装图不同时控制环境与色调；无头信息不能用于面部锁定。 | unverified | 填入实际检查记录 |
| XS03 | 穿戴面纱、可挥动舞袖、可推开的场景纱帘是三个对象；动作主语、接触和不可变状态必须区分。 | unverified | 填入实际检查记录 |
| XS04 | 141.845秒正文时间表与181.956秒README不能并用；局部拍点需从源时间换算，动作拍数与窗口余时全部分配。 | unverified | 填入实际检查记录 |
| XS05 | 绝对静止覆盖持续微运动层；若选择宏观静止，则删除absolute等绝对措辞并说明仍可呼吸。 | unverified | 填入实际检查记录 |
| XS06 | 歌词提供时序和情绪，不默认增添人、物、字幕或完整口型；没有SRT和音频不能声称逐句已对齐。 | unverified | 填入实际检查记录 |
| XS07 | 接缝的对象必须在前段实际结尾和后段实际开头可见；静止起步与首段开场是显式例外，不套用仍在运动的模板。 | unverified | 填入实际检查记录 |
| XS08 | 稳定与延迟观察模式通过段级白名单选择；不能同时要求稳定、不环绕及延迟环绕。 | unverified | 填入实际检查记录 |
| XS09 | 手、地面支撑与身体发力应驱动袖摆；地面技术需写接触转换，不以衣料运动代替动作因果。 | unverified | 填入实际检查记录 |
| XS10 | 原案混合的首帧话术、integrated_multimodal_description和音频参考／全复用冲突须编译为单一Ref2VA方案；原文仅作档案。 | unverified | 填入实际检查记录 |

记录静态检查结果、仍缺素材/测量、是否已实际生成，以及实际生成后才可评估的身份、动作、声音和接缝表现。
