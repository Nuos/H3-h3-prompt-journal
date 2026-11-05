# 第一人称手势命令与舞者身体同拍响应：输出工作表

将本文件复制到任务目录并填写；它是规划/交付模板，不是直接送入 H3 的全部正文。填写完的计划、参考权限和审计记录与生成提示词分开保存。

## 1. 当前任务与输入

| 输入项 | 当前任务值、来源与待核验内容 |
|---|---|
| 视觉参考与构图优先级 | 获取舞者、环境、光线及初始机位参考；记录能否看清前景手和全身、是否确有天花板。只有静态图时不声称已获原音、动作或空间声学测量。 |
| 命令序列与收尾策略 | 提供最终有序方向列表，显式选择结尾三连是追加、替换末三条还是取消。输入含十条主体加结尾三条却未说明时，将歧义列为missing并给两种时长方案，不自行宣称原案一定是十或十三条。 |
| 音轨、拍点和容差 | 提供实际音轨/拍点或用户指定的BPM、起拍偏移、总时长与允许响应帧差。未提供音轨时先写提议节奏，标记audio/onsets为missing，不用参考图推导音乐。 |
| 舞种与动作幅度 | 指定可替换的舞种、UP/DOWN的身体高度变化及左右重心/躯干/髋部可见位移；装饰动作必须服从方向映射。 |

## 2. 本案例交付

### 参考与构图表

操作者手、舞者、屏幕坐标、图像权限、手面积与人物高度度量、几何冲突和missing列表。

### 唯一命令时间表

命令编号、方向、手势起点、身体起点、完成条件、容差、结尾策略与总条数。

### H3提示词与音频条件

参考绑定、连续机位、方向响应、服从控制的舞种、末姿保持及声场/音乐方案。

### 审片清单

按每条命令记录实际起始帧、方向、位移、遮挡、出框和通过/修订；不声称已自动完成视频检测。

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
| F1 | 手是可见动作提示，舞者身体响应当前手势；两个主体的关系必须明确写出。 | unverified | 填入实际检查记录 |
| F2 | LEFT/RIGHT统一采用屏幕坐标；UP/DOWN改变舞者重心高度，不能用相机运动或比例拉伸替代。 | unverified | 填入实际检查记录 |
| F3 | 左右响应包含清楚的重心、躯干和髋部整体位移，单独细小摆髋不算完成命令。 | unverified | 填入实际检查记录 |
| F4 | 先确定结尾三连是追加还是替换，生成唯一编号总序列再绑定拍点。 | unverified | 填入实际检查记录 |
| F5 | 同步是同一命令窗口内的起始与完成关系；明确拍点、允许帧差及无提前响应，不能用“同拍”代替验收。 | unverified | 填入实际检查记录 |
| F6 | 前景手保持连续人体结构与不遮脸躯干；画面面积、人物高度和物理距离分别检查，不能相互替代。 | unverified | 填入实际检查记录 |
| F7 | 强俯视、大量天花板、近距离和全身占比需结合实际参考图验证，有冲突时显式调整而非叠加保证。 | unverified | 填入实际检查记录 |
| F8 | 舞种可替换，装饰动作服从命令映射；一手一舞者属于本案例构图，不是模型人数限制。 | unverified | 填入实际检查记录 |

记录静态检查结果、仍缺素材/测量、是否已实际生成，以及实际生成后才可评估的身份、动作、声音和接缝表现。
