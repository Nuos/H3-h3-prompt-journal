# 宋韵古典舞的双层节拍、差异化高光与连续交接：输出工作表

将本文件复制到任务目录并填写；它是规划/交付模板，不是直接送入 H3 的全部正文。填写完的计划、参考权限和审计记录与生成提示词分开保存。

## 1. 当前任务与输入

| 输入项 | 当前任务值、来源与待核验内容 |
|---|---|
| 作品与交付约束 | 给定总长、分段窗、情绪曲线、共同画幅或多版交付计划、连续动作匹配还是允许蒙太奇，以及腾空、支撑、地面动作的允许范围；段数与技术动作数量按新任务决定。 |
| 图像权限与服装能力 | 指定完整人物／服装／场景参考和仅作身份结构澄清的参考；确认水袖、裙腰、裙幅及可见支撑空间。没有圆裙就不生成圆盘式裙形，没有实际上一段末帧就不声称已经继承其真实状态。 |
| 音乐与事件 | 提供各段音频文件、源起止、实际段长、BPM、首拍相位或拍点表、结构重音和人声事件；每项标记用户给定、源案例记载、实测、推算或未知，并指定原音完整复用还是允许叠加拟音。 |
| 可执行动作与边界状态 | 登记每段主动作的支撑部位、准备、峰值、恢复，人物解剖学左右、身体朝向、下一落脚、双手与袖尾状态，以及需要保持还是重新编排的接缝；新项目允许简化原案高难动作。 |

## 2. 本案例交付

### 素材与交付契约

人物／场景Subject及参考权限、服装结构边界、允许动作、共同画幅或混合画幅合成方案、音频最终使用策略。

### 双层音乐与高光表

每段源起止和局部事件、精确计算与显示精度、细拍／慢舞句／★◆的层级、高光主导变量、共享子机制及准备恢复预算。

### 身体材料交接和摄影机计划

左右明确的支撑与动作链、腰头至裙缘／腕至袖尾的延迟、段间目标状态表、跟拍／重构图／锁定区间、真实切镜及最终三个对象的停止条件。

### 逐段Ref2VA与证据分层审计

每段可独立提交的六字段英文正文，修订后的时间与旧回指清单，翻译术语修正，未核验音频相位／末帧／成片效果及下一步实际核验项。

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
| SG01 | 完整视觉参考与身份结构澄清参考权限分开，参考图不自动等于首帧或前段实际末态；歌词中的原文色词不构成新增视觉色彩指令。 | unverified | 填入实际检查记录 |
| SG02 | 段内时间由源窗口换算，细拍、慢舞句和结构重音分层；使用唯一递增拍表，BPM不能替代未知相位或实测音频。 | unverified | 填入实际检查记录 |
| SG03 | 高光以主导机制和支撑／路径区分；承认S03与S05共享换腿子动作，删除S05第二Hero与不存在的720度历史回指。 | unverified | 填入实际检查记录 |
| SG04 | 脚与重心驱动躯干、手腕和水袖，裙摆始终依附腰头并有材料滞后；衣料比喻与力学意图不是已验证物理模拟。 | unverified | 填入实际检查记录 |
| SG05 | 接缝要求左右明确的动态状态匹配，不能只用同一身份或“某只脚”证明连续；无生成末帧时仅声明计划目标。 | unverified | 填入实际检查记录 |
| SG06 | 前五段竖幅倾向与末段16:9必须有交付契约；新项目先选共同画幅，保留混合旧片时明示母版、留边／裁切与独立版本。 | unverified | 填入实际检查记录 |
| SG07 | 跟拍、短重构图和硬锁有明确区间；锁定相机时人体可继续；景别按真实身体覆盖，three-quarter为四分之三侧面。 | unverified | 填入实际检查记录 |
| SG08 | 持续舞句不等于禁止切镜，动作阶段不等于Shot；技术峰值先完整呈现，再让脸部构图完成情绪收束。 | unverified | 填入实际检查记录 |
| SG09 | 结尾必须选相机硬锁且微动允许，或全画面冻结其一；原音完整复用与叠加拟音也要分别选择，不用一句绝对约束覆盖不同对象。 | unverified | 填入实际检查记录 |
| SG10 | 原案Hero命名、六段结构和双层节奏属于案例编排；翻译与作者结果陈述不增加独立实验，文本检查不认证模型同步或连续性。 | unverified | 填入实际检查记录 |

记录静态检查结果、仍缺素材/测量、是否已实际生成，以及实际生成后才可评估的身份、动作、声音和接缝表现。
