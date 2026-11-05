# 水岸独舞：单镜头取证与双段动作接力：输出工作表

将本文件复制到任务目录并填写；它是规划/交付模板，不是直接送入 H3 的全部正文。填写完的计划、参考权限和审计记录与生成提示词分开保存。

## 1. 当前任务与输入

| 输入项 | 当前任务值、来源与待核验内容 |
|---|---|
| 源片与检测证据 | 提供源片或逐帧/候选点记录；只给文字时把单镜头结论标成作者报告，记录缺失的检测版本、参数、分数与核对帧。 |
| 音频与时间基准 | 记录实际音频标识、总时长、已核实 BPM/拍号/全局首拍和分段起点；无实测音频时只采用用户给定值并标明来源，不虚构歌词。 |
| 身份与空间参考 | 分别指明图片用于身份服装、场景还是精确首帧。后段若靠动作接力开场，不把同一静态人物照强制当精确首帧。 |
| 动作链与终止要求 | 提供每条链的支撑脚、重心、朝向、手臂位置、旋转方向、拍数及最终是否完全静止。 |

## 2. 本案例交付

### 切镜取证表

候选时间、检测参数/版本、逐帧窗口、连续性观察、判定及证据状态。

### 全局/局部音乐时间表

BPM来源、首拍、拍长、小节长、片段全局区间、局部强拍与引入/尾段。

### 动作接力状态表

逐链入态—过程—出态、前段出口与后段入口、终止状态的生效时间。

### 逐段H3提示词与提交清单

官方模式正文、明确图像/音频绑定、时长与机位，另附文本Gate结果和仍待生成验证的项目。

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
| WF-01 | 低阈值命中只是候选，单镜头结论需要逐帧证据；缺少原片时保持作者报告标记。 | unverified | 填入实际检查记录 |
| WF-02 | 局部拍点等于全局拍点减片段起点；在强拍切出的后段首拍为0，不能继续沿用全片首拍偏移。 | unverified | 填入实际检查记录 |
| WF-03 | 每条动作链必须给出可配对的入态、拍数/时长、出态；物理动量不能在分段处复位。 | unverified | 填入实际检查记录 |
| WF-04 | 参考图片的身份用途和精确首帧用途分别声明；接力状态优先于未被指定为首帧的静态人物姿势。 | unverified | 填入实际检查记录 |
| WF-05 | 最终停势覆盖持续呼吸层的范围和起始时刻必须显式设定，避免同时要求绝对静止与每拍微动。 | unverified | 填入实际检查记录 |
| WF-06 | 锁定正面全身机位是此类连续独舞方案的可选任务约束，不是全部H3片段的默认机位。 | unverified | 填入实际检查记录 |
| WF-07 | 首拍未到的引入和最终残余时长分别标注，不以整数小节假设覆盖全部时间线。 | unverified | 填入实际检查记录 |
| WF-08 | 舞蹈音轨1:1复用需要真实分段资产；人声未核实时不编造歌词锚点，原本机路径不能视为当前可用资产。 | unverified | 填入实际检查记录 |

记录静态检查结果、仍缺素材/测量、是否已实际生成，以及实际生成后才可评估的身份、动作、声音和接缝表现。
