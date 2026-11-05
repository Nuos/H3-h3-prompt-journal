# 单人三姿态锚点与近身连续飞行摄影：输出工作表

将本文件复制到任务目录并填写；它是规划/交付模板，不是直接送入 H3 的全部正文。填写完的计划、参考权限和审计记录与生成提示词分开保存。

## 1. 当前任务与输入

| 输入项 | 当前任务值、来源与待核验内容 |
|---|---|
| 同一人物的三姿态参考 | 核对三图是否同一身份、服装和环境；逐图记录Pose 1/2/3的支撑、躯干朝向、四肢、头部。明确哪图主导身份/服装/场景及另两图的姿态权限；存在差异时不把三种外观同时声明为唯一真值。 |
| 允许移动空间与遮挡 | 记录人物活动范围、衣摆与头发可能扫过的区域、背景障碍和可见间隙。未给空间尺寸时标记clearance为missing，以外轮廓绕行为保守路线，不声称已经计算真实净距。 |
| 时间、路线与速度偏好 | 给出总时长、姿态到达时间、相机途经部位、机位高低和镜头运动强度。高速是本案例创作目标，必须与动作可辨认及路线可行性一起检查。 |
| 结尾构图与参考模式 | 明确第三姿态最后露出哪些身体部位、保持多久，以及图片是身份/姿态参考还是强制首帧/末帧。用户要求精确末帧时确认有对应素材；缺少则输出目标构图而非伪造末帧。 |

## 2. 本案例交付

### 三图参考权限与姿态表

主体ID、Pose 1/2/3、身份/服装/场景来源、支撑与四肢/头部配置、冲突和missing。

### 人物—相机并行时间表

每段人物起末状态、身体中间动作、相机路径、可见部位、避让原因和相邻段接点。

### H3正文与终态

连续近身摄影描述、参考绑定、飞行规则作用域、空间后撤和第三姿态半身保持。

### 降级与验收清单

姿态命中、人物身份、连续路径、穿模、可见性及终帧；给窄缝外绕和少转折版本，区分文本检查与实际审片。

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
| P1 | 三图指向同一人物的三个姿态，姿态是连续经过的锚点，不是三个身份或静态轮播画面。 | unverified | 填入实际检查记录 |
| P2 | 人物正常运动且保持正常尺寸；相机负责绕行避让，微小视点只体现为透视、视差和空间移动。 | unverified | 填入实际检查记录 |
| P3 | 每个中间动作必须自然导向下一参考姿态；人物动作和相机路径分别描述且时序对应。 | unverified | 填入实际检查记录 |
| P4 | 近身路线绕过身体、衣料和头发；没有可确认间隙时使用外侧弧线，不以不可见相机为由穿模。 | unverified | 填入实际检查记录 |
| P5 | 持续高速及不冻结仅适用于飞行段，末尾14–15秒半身保持是独立终态。 | unverified | 填入实际检查记录 |
| P6 | 参考图不一致时先定义身份、服装、场景和姿态的属性优先级，不同时锁定冲突属性。 | unverified | 填入实际检查记录 |
| P7 | 靠近与后撤是相机空间位移，保持透视和前后景视差，数字缩放不能代替。 | unverified | 填入实际检查记录 |
| P8 | 提示词中的预判和避障是创作行为规范，未提供碰撞求解、净距计算或生成稳定性保证。 | unverified | 填入实际检查记录 |

记录静态检查结果、仍缺素材/测量、是否已实际生成，以及实际生成后才可评估的身份、动作、声音和接缝表现。
