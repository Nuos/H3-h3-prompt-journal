# 台灯五章音乐时尚片与受控A/B变体：输出工作表

将本文件复制到任务目录并填写；它是规划/交付模板，不是直接送入 H3 的全部正文。填写完的计划、参考权限和审计记录与生成提示词分开保存。

## 1. 当前任务与输入

| 输入项 | 当前任务值、来源与待核验内容 |
|---|---|
| Picture 1与参考授权范围 | 确认单图中的成年人物、服装、房间、同一台灯、台灯初态、可用空间和初帧构图；图像missing时保留占位。正文只描述变化，不重复臆造外貌。原模板要求的不透明舞蹈内层若图中不可见，标unknown并需要明确服装设定依据，不能宣称已从图中确认。 |
| 变体与比较目标 | 选择cute_jump、dark_skirt_throw或用户自定义Hero；声明faithful_variant保留真实正文差异，还是controlled_ab主动统一摄影等控制项。根据正文映射p83文件到可爱跳跃、p84文件到暗奢甩裙，不按文件名词义选择。 |
| 音乐来源与节奏参数 | 给定生成配乐的目标BPM／拍号／小节数，或实际可听音轨及onset数据。案例124 BPM、4/4、31拍是新建音乐计划，未量测前状态planned，不标为detected或已精准同步。 |
| Hero机械与衣料条件 | 确认可抛甩的既有裙结构、可完成跳跃的站立与落地区域、服装内层和画幅。跳跃的双手不触裙、双脚后折靠拢；甩裙先抓握与蓄力。若服装／空间不支持所选动作，标资产不兼容并另拟改编。 |
| 生成与剪辑规格 | 记录官方模式、4–15秒生成范围、标准24FPS、成片时长、镜头切换允许范围，以及声画同步容差与实际验收方法。灯开关是初态加四次切换，保持未量测与已量测两个表。 |

## 2. 本案例交付

### 语义版本与源文件映射

variant_id、真实调式／配器、Moment05/06/07/09/10动作、各版roll允许位置、原路径和错误文件名注释。

### 共享节奏与灯态计划

精确拍号／拍位／秒值、显示值、生成帧、量化误差、灯初态及四切换、自由过渡边界、计划与实测状态。

### 每版H3提示词与变更表

公共资产和时轴、逐段身体／摄影／声音、独立Hero链、faithful或controlled路由标记；列明统一摄影等工程修改。

### 成片验收表

实际onset、灯态变化帧、身体重音、roll回正、跳跃落地或布料滞后、片尾锁机和A/B差异，未生成时留missing／pending。

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
| R1 | 按音乐调式和Hero正文识别版本：源p83文件=可爱A major后折腿跳跃；源p84文件=暗奢E minor双手甩裙，文件名和README标签相反。 | unverified | 填入实际检查记录 |
| R2 | 五章灯态是ON→OFF→ON→OFF→ON，共五状态、四次切换；初态ON不算一次切换。同一盏灯及房间保持，熄灯使用原房间残余照明，不新造光源。 | unverified | 填入实际检查记录 |
| R3 | 124 BPM／31拍／15秒及灯点是计划数学关系，不是生成音轨实测。保留整拍、细分和自由过渡标签，并记录24FPS舍入误差，不宣称小数时间恰好落在原生帧边界。 | unverified | 填入实际检查记录 |
| R4 | 受控A/B须逐项审计摄影差异；原文暗奢02/04/06/09和可爱版并非同一roll规则。统一roll预算属于显式改编，不能假称原两版只在三个层面分叉。 | unverified | 填入实际检查记录 |
| R5 | 每段动作有明确支撑与发起→行进→重音→刹停→释放，连续段身体结构不同且状态可达；轻弹脚不离地，提膝不是踢腿，最终跳跃不提前泄露。 | unverified | 填入实际检查记录 |
| R6 | 跳跃版双手高举而不抓裙，双脚向后靠拢且落地；甩裙版先握裙蓄力、手向外发力、裙边滞后。二者不能拼成同一Hero动作链。 | unverified | 填入实际检查记录 |
| R7 | ROLL绕光轴、短促且有触发，使用后回正；discrete camera states要说明切镜或连续路径。Moment08近静止微视差与片尾hard lock不同，不能混写。 | unverified | 填入实际检查记录 |
| R8 | bullet-time feel不是字面慢动作或真实冻结；以短暂可读峰值、正常下降／制动、衣料残余惯性表达，并给实际时长。没有证据不能承诺自然跳跃长时间悬停。 | unverified | 填入实际检查记录 |
| R9 | 参考图提供视觉资产，正文集中描述变化；全程保持资产需显式允许计划灯态造成的照明变化。未知内层、缺台灯或不支持Hero的裙结构不得伪称图中已存在。 | unverified | 填入实际检查记录 |
| R10 | 配乐与整体声场分列，开关click只对应四次实际切换；额外strobe、快门声、随机灯闪或提前Hero会破坏该变体的计数和因果，必须删除或另列变体。 | unverified | 填入实际检查记录 |

记录静态检查结果、仍缺素材/测量、是否已实际生成，以及实际生成后才可评估的身份、动作、声音和接缝表现。
