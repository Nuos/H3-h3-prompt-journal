# 舞蹈动链检索、时间容量与状态衔接编排：输出工作表

将本文件复制到任务目录并填写；它是规划/交付模板，不是直接送入 H3 的全部正文。填写完的计划、参考权限和审计记录与生成提示词分开保存。

## 1. 当前任务与输入

| 输入项 | 当前任务值、来源与待核验内容 |
|---|---|
| 片型与生成模式 | 声明continuous_dance、posed_portrait、partner_support、edit_swap或fantasy_vfx；根据官方H3规则确定T2VA/I2VA/Ref2VA等实际模式。Picture1作首帧锚定时继承当前身体中间态；仅作身份世界参考时另选支持该角色的模式，不能在I2VA初帧无过渡改姿势。 |
| 舞种、人物与资产 | 给出舞种／密度、实际人数与SubjectID、服装材料、现有道具、可用支撑面和空间。若图片、视频、音频或需要的扇／袖／墙／伙伴缺失，登记missing；不把K章源演员外观、场景、字幕、道具自动写入新任务。 |
| 音乐与时间规格 | 给实际音轨及已核验起音表，或声明创作计划的BPM／拍号／起拍偏移；自由散板可直接用秒窗而不虚构BPM。记录总片长、标准24FPS、各次生成4–15秒与最终编辑时长，长范本须分段、短片须生成余量后裁窗。 |
| 候选链与状态 | 优先提供稳定ID如A18、A19、C27、K7及来源版本。逐条读取完整条目而非只抄H3一句话，登记标题拍数、分解拍数、入态、出态、支撑／重心、方向、手位、道具、动力、峰值、回收、材料和证据标签。 |
| 摄影、剪辑与旋转预算 | 选camera_response=static_observe/sync_follow/anticipate_hit/delayed_observer，选edit_policy=continuous/phrase_end_cut/phase_match_cut/pose_jump_cut；两轴独立。旋转同时记录episode数、每段周数及方向；明确预算单位，不能把多周连续链误判成多个独立旋转事件或反过来。 |
| 保留与变化范围 | 明确首帧继承、持续律动是否可在指定hold停下、服装／身份是否跨镜保持、是否允许场景硬切、是否需要原声回贴、是否允许概念VFX。只启用与当前片型和资产一致的局部规则。 |

## 2. 本案例交付

### 任务模式与参考合同

片型、官方生成模式、首帧／身份参考权限、素材missing状态、人数与资产、摄影响应和剪辑语法、旋转计数单位。

### 选中链工程卡

source_id／version／lines、原拍数与实际分解、目标拍数／秒数、入态／出态、支撑／动力／峰值／制动／道具／材料、证据等级、字段冲突及裁决。

### 逐窗编舞与摄影表

全局和局部时间、BPM或onset依据、主动作完成点、IN/OUT桥接、持续与微表情层适用范围、摄影物理几何和启动／峰值／恢复／延迟；独立生成段自包含。

### H3正文与编辑装配清单

按实际模式编译选中链，清除源外观覆盖，音频方式及生成／剪辑时长分列；必要时记录长片分段、短片裁窗、原声回贴和跨切状态。

### 逐窗审校与生成后验收

十项检查结论、未通过窗口的修复、来源与工程变更表；实际成片未生成则结果栏pending，不填虚构onset、帧数成功率或模型稳定性。

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
| R1 | 先片型分流和版本锁定，再按稳定ID读取所需链；Rev.1.4的A—K及拼舞模板是同一知识库，不是已实现的自动模块，也不需要每次全文注入。 | unverified | 填入实际检查记录 |
| R2 | 单条真实字段优先于概括；库并非所有链都有完整出入态或2–8拍。标题、分解、H3和结束状态冲突先记录并裁决，补齐内容标工程设计；不静默修成来源事实。 | unverified | 填入实际检查记录 |
| R3 | 时间窗先于动作数量；每窗必须从支撑与动力进入，达到唯一主要结果，制动并产生可接的出态。容量表是启发估计，不能宣称某时长对所有人／BPM／动作绝对可行或绝对不可行。 | unverified | 填入实际检查记录 |
| R4 | 连续链满足前OUT=后IN，或显式安排桥接；持续层／动链层／微表情层按支撑与hold兼容，不把不断膝弹、完全锁姿和单脚平衡无条件叠加。 | unverified | 填入实际检查记录 |
| R5 | 共享时间轴不等于所有摄影零相位差；sync_follow、anticipate_hit、delayed_observer和static_observe单窗择一并写时间。提前画框到位、同时到位、迟半拍不能一起当全库铁律。 | unverified | 填入实际检查记录 |
| R6 | 剪辑语法单独选：动作完成处切、旋转相位匹配切、姿态跳切各自保留条件；首帧锚定、身份参考、单张姿势推测也分开，不跨模式机械粘贴。 | unverified | 填入实际检查记录 |
| R7 | 旋转记录episode数与每段周数／方向／轴心／停止点；Hero要完整预载和回收。源≤2次及2–4处Hero是局部经验，计数单位须声明，G实现度和稳定星级不构成官方或本次实测保证。 | unverified | 填入实际检查记录 |
| R8 | 按目标参考映射身体、服装、道具和场景；K章源档案与H3句中的外观世界不可覆盖当前图像权限。单图时间顺序、遮挡内动作与未入镜回收保持inferred标签，不升级成已观测。 | unverified | 填入实际检查记录 |
| R9 | 拍数、BPM、onset和声场分清measured／source-reported／planned／inferred／missing。自由散板可按秒设计；响度不证明固定BPM，原声波形需在装配阶段回贴。源片长不等于官方单次生成参数。 | unverified | 填入实际检查记录 |
| R10 | 多人固定的是当前任务的身份与角色数量，动静、接触及槽位逐人声明；示例四人／2×2／不镜像／solo位置不全局化。每段最终给可判定验收项，未生成不报告完成率或成功视频。 | unverified | 填入实际检查记录 |

记录静态检查结果、仍缺素材/测量、是否已实际生成，以及实际生成后才可评估的身份、动作、声音和接缝表现。
