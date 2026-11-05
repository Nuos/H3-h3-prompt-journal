# H3 运镜纪律选择与冲突裁决：输出工作表

将本文件复制到任务目录并填写；它是规划/交付模板，不是直接送入 H3 的全部正文。填写完的计划、参考权限和审计记录与生成提示词分开保存。

## 1. 当前任务与输入

| 输入项 | 当前任务值、来源与待核验内容 |
|---|---|
| 人物动作时间轴 | 提供动作起始、空间/高度变化、强调峰值、收势和段末状态；区分实测时间、用户指定时间和暂定时间。 |
| 当前机位与目标观看关系 | 给出高度、距离、左右前后、光轴目标、可用路径及应保留的身体范围；不清楚的几何留待确认。 |
| 响应与剪辑意图 | 明确偏向稳定观看、提前到位、同动跟随或刻意延迟；另行选择连续单镜、收势切或动作相位匹配切，两个选择轴不可混为一条同步铁律。 |
| 音频/片段限制 | 提供片长及已测节拍表；未见音频时不生成测量结论。人数、低机位、步数与快闪密度按当前任务填写，不继承历史实验的全部数字。 |

## 2. 本案例交付

### 规则选择表

当前任务、camera_response、edit_policy、适用历史条目、未选条目及其冲突理由。

### 五字段摄影机块

位置、几何、路径、人物触发和终点；静机字段完整，单位与身体坐标一致。

### 动作—相机时相表

同一时间域下的人物起峰收、相机起到停、delta_t、测量/计划状态和可见性检查。

### 可拼接提示词与审计

将摄影机块和真实动作链合成段落；另外列规则例外、输入缺口、未做推理验证的范围。

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
| CMD01 | 每段先建立机位并选一个主要摄影机行为，微小身体重音不自动触发相机改向。 | unverified | 填入实际检查记录 |
| CMD02 | 共享时间轴不等于零响应延迟；提前到位、同动和延迟观察必须分别选择。 | unverified | 填入实际检查记录 |
| CMD03 | 相机响应模式与剪辑模式独立；收势切和旋转相位匹配切不能同时作为无条件禁令。 | unverified | 填入实际检查记录 |
| CMD04 | 每个相机块具备位置、几何、运动、触发、终点五字段；零移动显式写 none。 | unverified | 填入实际检查记录 |
| CMD05 | 物理变化写真实路径、光轴和到达关系；特殊机位才需要强化位置物件与透视，普通机位不强塞极端描述。 | unverified | 填入实际检查记录 |
| CMD06 | 延迟观察只影响摄影机，人物保持控制；每次过冲最终修正并重新找到主体。 | unverified | 填入实际检查记录 |
| CMD07 | 低机位、无俯拍、1.5秒驻留、提前1.5–2秒、固定快闪密度等均保留来源情境，不作为所有镜头硬限制。 | unverified | 填入实际检查记录 |
| CMD08 | 实测字样只能归为作者原文自述，未有模型参数和可重放证据时不宣称所有规则已证明稳定。 | unverified | 填入实际检查记录 |

记录静态检查结果、仍缺素材/测量、是否已实际生成，以及实际生成后才可评估的身份、动作、声音和接缝表现。
