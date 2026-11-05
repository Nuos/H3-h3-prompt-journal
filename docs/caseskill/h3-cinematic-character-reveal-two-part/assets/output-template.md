# 双段角色揭示：姿态索引、接缝资产与连续母带：输出工作表

将本文件复制到任务目录并填写；它是规划/交付模板，不是直接送入 H3 的全部正文。填写完的计划、参考权限和审计记录与生成提示词分开保存。

## 1. 当前任务与输入

| 输入项 | 当前任务值、来源与待核验内容 |
|---|---|
| 同一角色的分工参考 | 登记姿态/身体/服装/场景来源与唯一脸部来源；多张图服务同一个角色，不合并成新人。补充姿态图不得自动接管人脸。 |
| 可定位的批准姿态库 | 为实际可见姿态建立ID、文件/图内区域、主要几何、允许微动和已使用方式；参考未给时不能虚构Pose 01–11映射。 |
| 时长与剪辑表 | 记录全片时长、生成切片、时间块、块内真实切镜及最低可读时间；案例30秒是两次15秒生成，不是一次标准长请求。 |
| 声音素材与传递能力 | 明确使用真实连续母带还是重新生成音乐，登记母带全局位置、合法分段参考、环境声底层、运行时能否接收末帧/关键帧/参考音轨。 |
| 允许回调与禁止重复 | 定义去重对象是同一姿态、同一构图还是同一转场机制，并明确是否允许同姿态换裁切/视角的视觉回调。 |

## 2. 本案例交付

### 参考权限与姿态索引

每个输入的实际用途、角色唯一脸部来源、批准姿态ID与图内位置、各段已用/待重点展示状态。

### 展开后的真实镜头表

创作块ID与实际Shot映射、全局/局部起止、帧预算、视觉事件与音乐证据、姿态/景别/机制。

### 双端交接包

第一段出态、第二段入态、末帧/末段资产、相机/光照/衣料余势、音频偏移、环境声底层与运行时可用性。

### 两段H3正文与去重报告

各段独立完整字段、真实参考绑定，逐镜去重/回调例外、静态检查和待生成验证范围。

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
| CR-01 | 脸部唯一来源与身体/服装/姿态/场景来源分别绑定到同一角色；补充姿态不得混入新脸或新增人物。 | unverified | 填入实际检查记录 |
| CR-02 | 所有主要姿态必须能在真实参考中定位；Pose 01–11是原稿标签，不是已经建立的图内索引。允许微动不等于允许发明主要姿态。 | unverified | 填入实际检查记录 |
| CR-03 | 每段13 CUT是时间块数量，包含多次分切的块须展开，不能直接报告恰好13个实际镜头或全片26镜头。 | unverified | 填入实际检查记录 |
| CR-04 | 跨生成精确接续需要实际末帧/状态和运行时支持；两张原始定妆图及双端重述不足以证明上一片段状态已传入。 | unverified | 填入实际检查记录 |
| CR-05 | 连续BGM和环境声有全局偏移与编辑/复用方案；第二段不从音轨0秒重启，完整音轨复制与新增声效不得冲突。 | unverified | 填入实际检查记录 |
| CR-06 | 无BPM/拍表时不能把秒数表称为已验证卡点；五拍高潮和块内快切需明确实际拍点、细分拍及帧预算。 | unverified | 填入实际检查记录 |
| CR-07 | 镜头去重按具体机制和构图审计，允许回调需声明变化维度；两段建筑遮挡实际相似，不能照抄完全不重复的结果断言。 | unverified | 填入实际检查记录 |
| CR-08 | 图形剪辑改变摄影图像关系，不能变形角色身体；近景优先保留身份和服装细节，稳定姿态允许任务指定的眼睛/衣料微动。 | unverified | 填入实际检查记录 |
| CR-09 | 30秒原案按两个15秒生成切片规划；引入/升级/收束为创作结构，约20秒、纯器乐或特定教堂风格都不是H3通用能力限制。 | unverified | 填入实际检查记录 |

记录静态检查结果、仍缺素材/测量、是否已实际生成，以及实际生成后才可评估的身份、动作、声音和接缝表现。
