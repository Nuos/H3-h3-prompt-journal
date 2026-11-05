# H3 人物优先的多参考动作重建：输出工作表

将本文件复制到任务目录并填写；它是规划/交付模板，不是直接送入 H3 的全部正文。填写完的计划、参考权限和审计记录与生成提示词分开保存。

## 1. 当前任务与输入

| 输入项 | 当前任务值、来源与待核验内容 |
|---|---|
| 图像人物与世界参考 | 给出Picture1实际文件、用途与可用地面/空间；该案例默认图1同时拥有身份、衣着、环境和光线。若用户分开人物与场景资产，先显式改参考职责表。 |
| 动作参考视频 | 给出Video1文件和截取时窗，提取首帧机位/身体朝向与后续准备—发起—展开—重音—恢复。源人物、服装、背景、灯光不作为输出外观。 |
| 目标音频与时间证据 | 给出Audio1文件、目标窗口及实测节拍/乐句表；没有测量资料时标missing，不填写虚构BPM或宣称重定时已完成。 |
| 运行能力和工程资产 | 若请求执行，提供实际H3模式、模型/编码器/VAE、节点版本、GPU资源、workflow、目标fps和规格。若只写提示词，运行字段标未执行，不要求安装或下载模型。 |
| 续接参数 | 仅续段需要上一段视频、接续帧范围、噪声策略、目标裁剪点及音频裁剪点；帧和秒要有同一fps/时间原点。 |

## 2. 本案例交付

### 参考权限与素材清单

每个资产的文件/缺失状态、角色、允许继承、拒绝继承、实际输入端口与作用时窗。

### 动作和相机重建表

源事件、首帧身体/几何、目标人物机制、新世界可行性、目标时点及节奏证据。

### 完整H3迁移提示词

人物与世界约束、开场构图、动作链、相机路线、音频职责和明确边界；不用源片人物外观填空。

### 工作流预检摘要（可选）

活动/旁路节点、实际权重与依赖、有效参数来源、帧数/时长换算、分辨率、音频端口、裁剪一致性、阻塞项。

### 前后两阶段验收表

提交前静态检查与生成后八项结果检查分列，附素材/配置哈希、种子、失败类型和重试记录；未运行明确写未执行。

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
| MTR01 | 参考按身份/世界、运动/相机、时序分权；Video1人物不作为第二个输出主体。 | unverified | 填入实际检查记录 |
| MTR02 | 首帧只继承相机几何和开场身体机制，不继承源外观、服装、背景或照明。 | unverified | 填入实际检查记录 |
| MTR03 | 人物优先重建是提示词组织顺序，不是已证实的模型内部计算顺序或独立运行阶段。 | unverified | 填入实际检查记录 |
| MTR04 | 目标音频重定时必须基于提供的BPM/事件/乐句证据；整段变速源片不等价于动作机制重建。 | unverified | 填入实际检查记录 |
| MTR05 | 8–9秒仅属案例经验；可用时长以当前模式和真实部署能力为准。 | unverified | 填入实际检查记录 |
| MTR06 | 工作流参数优先沿连线求有效值，不能将1344×768和124帧旧widget直接报告为实际输出。 | unverified | 填入实际检查记录 |
| MTR07 | 必须验证活动音频节点和ref_video_audios/ref_audios端口职责，不能仅写Audio1就认为音频已输入模型。 | unverified | 填入实际检查记录 |
| MTR08 | 续接视频/音频裁剪必须共享时间原点；22帧、26帧、1秒不能不加解释地混用。 | unverified | 填入实际检查记录 |
| MTR09 | 预检不能确认未生成的视频每帧身份；八项视觉/时序核对应在有输出后执行。 | unverified | 填入实际检查记录 |
| MTR10 | 新世界的支撑面和机位通道必须能容纳源动作，不能仅换场景文字而忽略足部接触与运动空间。 | unverified | 填入实际检查记录 |

记录静态检查结果、仍缺素材/测量、是否已实际生成，以及实际生成后才可评估的身份、动作、声音和接缝表现。
