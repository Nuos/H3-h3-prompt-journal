# H3 动作触发的物理运镜组合编排：输出工作表

将本文件复制到任务目录并填写；它是规划/交付模板，不是直接送入 H3 的全部正文。填写完的计划、参考权限和审计记录与生成提示词分开保存。

## 1. 当前任务与输入

| 输入项 | 当前任务值、来源与待核验内容 |
|---|---|
| 动作链与人物参考 | 提供本段单一表演者、连续动作链及身份/服装参考职责。只有占位符时登记 missing，不声称已查看图像；姿势与相机不从身份照自动继承。 |
| 片段规格 | 提供总时长、宽×高或明确宽高比、是否连续拍摄。原文“Vertical 4:3”有歧义，不能直接作为尺寸参数。 |
| 场地与摄影机条件 | 提供可用前后侧向空间、地面状态、遮挡物、近景距离与身体动作幅度，判断绕侧、超越和贴地升起是否可行。 |
| 节奏证据 | 接收已测 onset/重拍时间表或明确结构性时间安排。未提供音频测量时可编排时长预算，但须标为未核验音乐同步。 |

## 2. 本案例交付

### 运镜决策与前提表

选用组合编号、适用动作、可用空间、遮挡条件、未满足条件和已采用的简化。

### 人物—摄影机连续阶段表

start/end、人物起始与动作峰、相机起点/路线/光轴/到位、continuous_phase 或 hard_cut、音乐证据状态。

### 完整 H3 片段正文

包含参考职责、场景、完整动作链、物理机位、同步关系和段末钩子，可单独阅读；审计说明放正文之外。

### 修复与待核验项

记录07方位、10例外、宽高比、时长改动及未测音频/未提供资产，避免把工程修复冒充原文。

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
| ACM01 | 用起点—物理路径—主体触发—终点—最终构图展开运镜；术语可以保留为索引，执行正文不得只靠术语或角度数。 | unverified | 填入实际检查记录 |
| ACM02 | 每次前后、升降、换侧均写实际位移及光轴目标，不用数字变焦或未描述的瞬移代替。 | unverified | 填入实际检查记录 |
| ACM03 | 人物与相机共用时间轴；只有实际音频数据支持时才把时间点标为已核验重拍。 | unverified | 填入实际检查记录 |
| ACM04 | 本库 SHOT 默认解释为同一镜头内的连续阶段；实际硬切需要显式另行声明。 | unverified | 填入实际检查记录 |
| ACM05 | 组合07按正文采用背后起始，标题前方起始不再与正文混用。 | unverified | 填入实际检查记录 |
| ACM06 | 组合10的静态建立和先行微推进必须标为局部例外；严格动作触发任务取消该预先移动。 | unverified | 填入实际检查记录 |
| ACM07 | 单人、上半身优先、一两步位移是案例局部条件；不宣称去掉角度数字本身已被证明提高 H3 稳定性。 | unverified | 填入实际检查记录 |
| ACM08 | 独立粘贴输出必须同时携带参考职责与所需公共规则，且用明确宽高比代替含混的“Vertical 4:3”。 | unverified | 填入实际检查记录 |

记录静态检查结果、仍缺素材/测量、是否已实际生成，以及实际生成后才可评估的身份、动作、声音和接缝表现。
