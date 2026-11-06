# H3 通用核心技能

**当前新增模块：** M11 `h3-model-protocol` v0.1.0。

**模块合同：** M1—M11 各自为 `1.0.0`；不表示全部共享对象已冻结或所有原生对象可直接拼接。

**更新日期：** 2026-11-05（America/Los_Angeles）。

**开发基线：** `skillplan-v0.1.2-608813b`；M11 本轮读取仓库 `586373218a0790382fc5eeed99574d2d58eb8eb8`。

## 核心摘要

依据冻结的十二模块方案，已交付 M1—M10，本轮新增 **M11 模型协议编译与运行参数适配**，技能名为 `h3-model-protocol`。M11 将已确认的创作计划转换为五种 H3 模式的字段、参考标签、纯正文和有版本证据的工作流参数，包含四个可独立调用的子模块。

领域方法限定为 `case-studies/` 文本，重点使用 10 月案例；合成示例与工程反例明确标记。Anthropic／Agent Skills 规范用于技能结构，MiniMax 官方资料用于协议，实际部署资料用于工作流能力。文本编译、参数导出、真实推理和媒体验收分别报告。

## 关键结论

1. M11.1—M11.4 具有独立输入输出和分区责任；兼容外部资料可替代上游重跑。
2. 基础四模式三字段与 Ref2VA 六字段严格区分；模式由素材用途决定，不由图片数量猜测。
3. Subject／Picture／Video／Audio、实际说话者和真实镜头各自编号，保留稳定来源与绑定。
4. 已确认的动作、角色、台词、镜头和状态不能因格式或能力冲突被编译器静默改写。
5. 缺少实际工作流参数资料时保留明确缺项；模拟 profile 不冒充真实运行能力。
6. 本轮仅新增 M11 包及开发／验证记录并更新索引；M12 仍待实现，既有模块和锁定方案保持原字节。

**关键词：** M1—M11、CapabilityProfile、CompilationResult、模式、Label、协议编译、参数适配、版本与证据。

## 目录导航

1. 模块入口
2. M11 模型协议编译与参数适配
3. M10 视觉风格、光色与材质方案
4. M9 分镜、编辑与生成方案
5. M8 连续性方案与 H3 交接
6. M7 时间方案与 H3 交接
7. M6 声音方案与 H3 交接
8. M5 摄影方案与 H3 交接
9. M4 动作计划与 H3 交接
10. M3 空间计划与 H3 交接
11. 既有 M2 与 H3 的对应
12. 调用与文件组织
13. 验证入口和完成边界
14. 基线与历史记录

## 1. 模块入口

| 模块 | 技能入口 | 子模块 | 当前实现 |
|---|---|---|---|
| M1 作品意图与段落功能 | [h3-work-intent/SKILL.md](h3-work-intent/SKILL.md) | M1.1 意图约束；M1.2 段落信息；M1.3 情绪母题 | 文字工作流、独立合同与确定性检查；运行包保持原字节 |
| M2 素材解析、资产绑定与参考权限 | [h3-asset-reference/SKILL.md](h3-asset-reference/SKILL.md) | M2.1 资产登记；M2.2 主体绑定；M2.3 属性权限 | 文字工作流、独立合同、冲突/版本/引用检查和交接 |
| M3 场景空间、人物站位与交互调度 | [h3-scene-blocking/SKILL.md](h3-scene-blocking/SKILL.md) | M3.1 空间拓扑；M3.2 站位路线；M3.3 互动遮挡 | 文字工作流、独立合同、图上可达／引用／版本检查、父接受和交接 |
| M4 人物表演、动作链与物理因果 | [h3-action-performance/SKILL.md](h3-action-performance/SKILL.md) | M4.1 事件前提；M4.2 动作机制；M4.3 结果接续 | 文字工作流、独立合同、事件依赖／条件／引用／版本检查、父接受和交接 |
| M5 摄影机、景别、构图与焦点 | [h3-camera-visibility/SKILL.md](h3-camera-visibility/SKILL.md) | M5.1 观察机位；M5.2 取景可见；M5.3 焦点景深；M5.4 运动触发 | 文字工作流、独立合同、引用／版本／固定观察检查、父接受和交接 |
| M6 声音、音乐、对白与歌词关系 | [h3-sound-music-dialogue/SKILL.md](h3-sound-music-dialogue/SKILL.md) | M6.1 声源绑定；M6.2 发声事件；M6.3 音轨策略；M6.4 环境动作声 | 文字工作流、独立合同、声音关系／引用／版本检查、父接受和交接 |
| M7 统一时间轴与动作—镜头—声音协同 | [h3-time-synchronization/SKILL.md](h3-time-synchronization/SKILL.md) | M7.1 时间依据；M7.2 事件排时；M7.3 时间域映射与帧量化 | 文字工作流、独立合同、时间数值检查、父接受和交接 |
| M8 主体、道具、场景与跨镜状态连续性 | [h3-state-continuity/SKILL.md](h3-state-continuity/SKILL.md) | M8.1 策略许可；M8.2 计划账本；M8.3 边界交接 | 文字工作流、独立合同、状态关系／来源／版本检查、父接受和交接 |
| M9 分镜组织、转场、剪辑与生成分段 | [h3-shot-edit-generation/SKILL.md](h3-shot-edit-generation/SKILL.md) | M9.1 镜头画格；M9.2 剪辑选窗；M9.3 生成任务 | 文字工作流、独立合同、结构关系／来源／版本检查、父接受和交接 |
| M10 视觉风格、光线、色彩与材质 | [h3-visual-look/SKILL.md](h3-visual-look/SKILL.md) | M10.1 风格继承；M10.2 光源照明；M10.3 色彩调色；M10.4 材质效果 | 文字工作流、四路独立合同、作用域／权限／版本检查与父接受 |
| M11 模型协议编译与运行参数适配 | [h3-model-protocol/SKILL.md](h3-model-protocol/SKILL.md) | M11.1 能力资料；M11.2 模式绑定；M11.3 字段编译；M11.4 参数导出 | 文字编排／审计、独立合同、确定性编译与任务导出；实际运行未验证 |
| M12 持续审计 | 冻结方案中的后续职责 | 依已锁定职责推进 | 本轮尚未实现 |

### M2 的三个产物

| 子模块 | 输出对象 | 关键内容 |
|---|---|---|
| M2.1 | AssetRegistry | 来源与版本、媒体通道、可访问性、观察状态及缺项 |
| M2.2 | EntityRegistry | 稳定实体、源内定位、资产多对多绑定、授权依据 |
| M2.3 | ReferenceMap | 属性允许/禁止/未知、明确范围、来源竞争与显式裁决 |

三对象在 `M2State.content` 中分别为 `asset_registry`、`entity_registry`、`reference_map`。M2State 是本包的组合记录，不替代全部 ProjectPlan。

## 2. M11 模型协议编译与运行参数适配

| 子模块 | 独占职责 | 交付与审计 |
| --- | --- | --- |
| M11.1 能力与版本资料 | CapabilityProfile | 模型／后端／工作流／协议版本，能力证据和明确未知 |
| M11.2 模式与素材序列化绑定 | 模式和绑定分区 | 按用途选择模式，稳定 ID 到素材顺序及四类 Label 的映射 |
| M11.3 提示词字段编译 | 模型字段与正文 | 基础三字段／Ref2VA 六字段、首尾帧首行、Shot／Sx、原词和语义追溯 |
| M11.4 运行参数与任务包导出 | 参数和任务包分区 | 有证据的工作流映射、时长和素材一致性、导出状态与诊断 |

四个子模块均可通过兼容最小输入独立调用，不强制先执行 M1—M10。M11 消费已经确认的创作语义；遇到能力冲突回 M9／M7，涉及专业决定时回对应模块，不自行改剧情、角色、动作或台词。

T2VA／I2VA／FL2VA／L2VA 使用 `integrated_multimodal_description` 等三字段；Ref2VA 使用六字段，主正文为 `detailed_description`。四类官方参考标签、真实镜头和说话者编号分别管理。内部 profile、参数、诊断和追溯不进入纯模型正文。完整编排／审计要求见 [M11 五模式与逐 Label 映射](h3-model-protocol/references/h3-label-mapping.md)。

官方提示词资料充分时可以完成文字编译；导出适用于实际工作流的参数包还需目标版本的字段证据。合成 profile 仅展示映射合同，案例时长不构成统一模型限制，编译和导出不表示已运行 H3。调用、字段及能力边界见 [M11 公共合同](h3-model-protocol/references/contract-guide.md)，领域来源见 [M11 案例证据](h3-model-protocol/references/case-evidence.md)。

## 3. M10 视觉风格、光色与材质方案

| 子模块 | 权威分区 | 主要产物与审计 |
| --- | --- | --- |
| M10.1 风格层级与继承 | StyleHierarchy | 全片／场景／镜头关系、明确例外、独立任务有效风格 |
| M10.2 光源与照明 | LightingPlan | 光源、方向与空间依据、光质、局部光色及观看条件 |
| M10.3 色彩与调色 | ColorPlan | 基调、对比、曝光倾向、保护属性及局部色彩关系 |
| M10.4 材质与视觉效果 | MaterialEffectPlan | 对象与表面绑定、状态／效果条件、可见性和连续性交接 |

暖色光源与全片冷中性调色分别归 M10.2／M10.3；湿发、湿衣的表面状态不自动授权改变发色、发型或服装身份。各子模块使用公开最小输入，接受兼容用户／外部投影，不强制先运行 M1—M9。参考权限由 M2 决定，可见性与 M5 协调，持续范围交 M8，最终模型字段和 Label 交 M11。

基础四模式的视觉描述进入 `integrated_multimodal_description`；I2VA／FL2VA／L2VA 分别保留实际首帧／首尾帧／尾帧约束。Ref2VA 通过定义、摘要、保留分析和 `detailed_description` 保持风格参考角色一致。四类官方 Label 保持 Subject／Picture／Video／Audio 的实际用途；本模块不新增 Style／Lighting／Material Label 或 H3 顶层字段。

完整五模式与逐 Label 编排／审计见 [M10 H3 映射](h3-visual-look/references/h3-label-mapping.md)，独立及组合调用见 [M10 合同指南](h3-visual-look/references/contract-guide.md)，条件化领域证据见 [M10 案例证据](h3-visual-look/references/case-evidence.md)，失败回传见 [M10 审计与交接](h3-visual-look/references/audit-and-handoff.md)。

## 4. M9 分镜、编辑与生成方案

| 子模块 | 权威分区 | 主要产物与审计 |
| --- | --- | --- |
| M9.1 镜头、分镜格与事件归属 | ShotMap | 阶段／事件到真实镜头的关系、分镜格用途、历史标签对照 |
| M9.2 剪辑拓扑、选窗与转场 | EditGraph | 源素材版本与候选窗、装配顺序、边界执行位置与连续性策略 |
| M9.3 生成任务划分 | GenerationPlan | 内容分配、独立上下文、能力依据与入出段条件 |

基础四模式的逐镜内容进入 `integrated_multimodal_description`；I2VA／FL2VA／L2VA 分别遵守真实首帧／首尾帧／尾帧约束。Ref2VA 的逐镜正文使用 `detailed_description`，通过定义、摘要和保留分析明确参考作用。`<Picture N>` 可承担分镜／帧锚，`<Video N>` 可提供编辑源、续接源或整段时间结构；Subject 与 Audio 分别保留可见内容和声音角色。

`[Shot N]` 对应每个生成目标内的真实镜头，不能把阶段、故事板画格或后台任务数量直接写成切镜数量。后期桥接和裁剪保留在编辑计划。最终编号、协议和参数交 M11，M9 的内部三分区不新增 H3 字段。

完整映射见 [M9 H3 模式与 Label](h3-shot-edit-generation/references/h3-label-mapping.md)，领域方法及冲突见 [M9 案例证据](h3-shot-edit-generation/references/case-evidence.md)，独立／组合调用见 [M9 合同指南](h3-shot-edit-generation/references/contract-guide.md)。

## 5. M8 连续性方案与 H3 交接

| 子模块 | 权威职责 | 主要产物与审计 |
| --- | --- | --- |
| M8.1 连续性策略与变化许可 | ContinuityPolicy | 持续范围、不变项、允许变化、来源和边界规则 |
| M8.2 计划状态与转换登记 | StateLedger | 初态、转换依据、终态、来源版本；计划与观察分开 |
| M8.3 边界交接与接续检查 | 只读状态形成交接结果 | 前镜末态／交接表／后镜初态，接缝要求与责任回传 |

基础四模式的状态与变化事件进入 `integrated_multimodal_description`；I2VA／FL2VA／L2VA 分别遵守实际首帧／首尾帧／尾帧约束。Ref2VA 的身份与外观依据、参考保留与允许变化分别交接到官方分析字段，逐镜状态过程进入 `detailed_description`，声音持续由 `overall_soundscape`／`non_diegetic_music` 承接。

`<Subject N>`、`<Picture N>`、`<Video N>`、`<Audio N>` 保持各自获准的素材角色；不能从参考图片静默继承不合本段计划的姿态或道具状态，也不能用文字绕过实际首帧约束。模型字段和最终 Label 编号归 M11；内部账本不是新增 H3 原生字段。

M8.3 不改写 M8.2 状态，实际媒体观察仍归 M12。完整五模式／Label 编排与审计见 [M8 映射](h3-state-continuity/references/h3-label-mapping.md)，独立调用见 [M8 合同](h3-state-continuity/references/contract-guide.md)，专业问题回传见 [M8 审计](h3-state-continuity/references/audit-and-handoff.md)。

## 6. M7 时间方案与 H3 交接

| 子模块 | TimingMap 分区 | 主要产物与审计 |
| --- | --- | --- |
| M7.1 时间依据与单位归一 | `timebase` | 时钟、单位、帧率、首拍和拍点依据、明确未知；理论网格不冒充实测 |
| M7.2 事件排时与同步约束 | `schedule` | 起止、先后、重叠、偏移、必要持续与容量；事件身份和责任保留 |
| M7.3 时间域映射与帧量化 | `mappings` | 源／作品／生成／编辑换算、M9 选择的变速与定格、帧号、误差和容差 |

基础四模式的时间事件进入 `integrated_multimodal_description`；I2VA、FL2VA、L2VA 另外遵守各自首／尾帧对齐指令。Ref2VA 的逐镜时序进入 `detailed_description`，Video／Audio 源窗口与目标生成局部时间分开；参考用途、保留程度和关键帧位置按官方分析字段交接。全片声音字段保持同一时间来源。

`[Shot N]` 代表真实镜头，第一镜不加切点时间戳；后续切点使用局部 `At MM:SS.mmm`。`<Picture N>`、`<Video N>`、`<Audio N>` 的时间角色不能混用，`<Subject N>` 不承担时间域标识。`TimingMap` 是项目内部对象，未新增 H3 原生字段。完整五模式／Label 编排与审计见 [M7 映射](h3-time-synchronization/references/h3-label-mapping.md)。

## 7. M6 声音方案与 H3 交接

| 子模块 | SoundPlan 分区 | 主要产物与审计 |
| --- | --- | --- |
| M6.1 声源与说话者绑定 | `sources` | 声源、实体／独立旁白／音轨关系、声音身份与来源；不按资产编号反推说话者 |
| M6.2 对白与发声事件 | `vocal_events` | 原文、语言、发声方式、歌词角色与延续条件；原词保真、无默认口型 |
| M6.3 音乐与音轨使用策略 | `music` | 完整／部分复制、参考、生成或无配乐、源窗口及音乐依据；避免策略矛盾 |
| M6.4 环境与动作声音 | `effects` | 环境与动作声、具体来源、触发、已在源内或新增及延续条件，以及明确全片静音 |

M6 适用 T2VA、I2VA、FL2VA、L2VA、Ref2VA。基础四模式的逐镜声音进入 `integrated_multimodal_description`；Ref2VA 的声音来源和复制／参考关系进入定义、摘要及保留分析，逐镜正文使用 `detailed_description`。环境与动作声音汇总到 `overall_soundscape`，仅观众可听配乐进入 `non_diegetic_music`。

四类官方参考 Label 与 `(Sx)` 分开：可见主体、具体帧、视频结构、音频信号各按实际用途绑定；声音编号由 M11 按实际发声顺序统一分配。直接复用配乐里的歌词提示不自动新增说话者。官方 `fully_copy` 要求完整原音频就是完整最终音轨，有新增、删除、替换或局部复制时使用 `partially_copy`。

完整编排与审计见 [M6 H3 映射](h3-sound-music-dialogue/references/h3-label-mapping.md)、[M6 合同](h3-sound-music-dialogue/references/contract-guide.md)、[M6 审计交接](h3-sound-music-dialogue/references/audit-and-handoff.md)。

## 8. M5 摄影方案与 H3 交接

| 子模块 | CameraPlan 分区 | 主要产物与审计 |
| --- | --- | --- |
| M5.1 观察机位与光轴 | `viewpoints` | 位置、高度、距离、光轴、位姿与观察条件；不把景别当机位 |
| M5.2 取景、构图与可见性 | `framing` | 景别、画面关系、关键动作／接触的可见条件与遮挡范围 |
| M5.3 焦点与景深策略 | `focus` | 清晰对象与层次、保持／变化策略、光学条件与未知项 |
| M5.4 摄影机运动与触发 | `movements` | 独立摄影事件、起终机位、路径、触发、四类响应策略 |

M5 对应 T2VA、I2VA、FL2VA、L2VA、Ref2VA。基础四模式的摄影内容进入 `integrated_multimodal_description`；Ref2VA 使用 `retention_analysis` 表达获准保留／改变的关系，`detailed_description` 逐镜呈现实际摄影过程。H3 没有由本模块新增的 `camera_movement` 顶层字段；内部 CameraPlan 与官方输入结构分开。

四类参考 Label 为 `<Subject N>`、`<Picture N>`、`<Video N>`、`<Audio N>`。机位、构图或摄影参考必须按实际素材用途绑定，不能由身份图片自动继承，也不能以音频节拍默认触发每次运镜。真实素材序列化和 Label 编号归 M11。

完整逐项编排与审计见 [M5 H3 映射](h3-camera-visibility/references/h3-label-mapping.md)，独立输入与父接受见 [M5 合同指南](h3-camera-visibility/references/contract-guide.md)，具体检查与责任回传见 [M5 审计交接](h3-camera-visibility/references/audit-and-handoff.md)。

## 9. M4 动作计划与 H3 交接

| 子模块 | ActionPlan 分区 | 主要产物与审计 |
| --- | --- | --- |
| M4.1 表演事件与前提 | `events` | 稳定事件、执行者、对象、目标、起态、前提与触发；核对必保事件和因果关系 |
| M4.2 动作机制与交互过程 | `mechanics` | 支撑、重心、发力、运动、接触、道具操作与恢复；不以动作名称或结果跳过过程 |
| M4.3 结果与动作接续 | `outcomes` | 可见结果、出态、持续／结束、后继条件和状态请求；不覆盖 M8 权威状态 |

M4 适用于 T2VA、I2VA、FL2VA、L2VA、Ref2VA。基础四模式动作正文进入 `integrated_multimodal_description`；Ref2VA 进入 `detailed_description`。首帧用于动作起态，首尾帧约束可观察的中间变化，尾帧用于动作收敛目标。内部事件 ID 与四类官方参考 Label 分开管理，最终编译由 M11 完成。

完整逐字段、逐 Label 编排与审计见 [M4 H3 映射](h3-action-performance/references/h3-label-mapping.md)；独立输入、三分区、版本、未知项与工具用法见 [M4 合同指南](h3-action-performance/references/contract-guide.md)；专业检查和责任回传见 [M4 审计交接](h3-action-performance/references/audit-and-handoff.md)。

## 10. M3 空间计划与 H3 交接

| 子模块 | SpatialPlan 分区 | 主要产物与审计 |
|---|---|---|
| M3.1 空间坐标与场景拓扑 | `topology` | 坐标约定、锚点、区域及连接；明确世界／身体／屏幕方向 |
| M3.2 站位与移动路线 | `blocking` | 稳定实体的起终位、朝向、路径、层次与队形变化 |
| M3.3 交互区域与遮挡约束 | `interactions` | 接触、交叉、避让、视线、允许遮挡和关键可见条件 |

M3 适用于五种 H3 输入模式。T2VA 从文字组织空间；I2VA 从首帧发展；FL2VA 连接首尾空间端点；L2VA 收敛到尾帧；Ref2VA 按已授权参考用途逐镜组织空间。基础四模式对应三字段，Ref2VA 对应六字段。四类官方参考 Label 与 M3 内部实体／区域／路线 ID 分开，由 M11 完成实际编号和序列化。

完整逐字段、逐 Label 编排／审计说明见 [M3 H3 映射](h3-scene-blocking/references/h3-label-mapping.md)。公开调用与 JSON 示例见 [M3 合同指南](h3-scene-blocking/references/contract-guide.md)，领域规则和来源由技能入口按需路由。

## 11. 既有 M2 与 H3 的对应

| 输入模式 | M2 交接重点 | 官方字段/Label 去向 |
|---|---|---|
| T2VA | 无参考时空集合、文字要求 | `integrated_multimodal_description` 等基础三字段 |
| I2VA | 实际首帧资产与角色、变化边界 | 首帧对齐指令及基础三字段 |
| FL2VA | 首尾帧身份、角色与衔接约束 | 首尾帧对齐指令及基础三字段 |
| L2VA | 尾帧身份、角色与约束 | 尾帧对齐指令及基础三字段 |
| Ref2VA | 定义、引用用途、保留/变化/复制关系 | 六字段；`<Subject N>`、`<Picture N>`、`<Video N>`、`<Audio N>` |

完整逐项编排与审计见 [H3 模式与 Label 映射](h3-asset-reference/references/h3-label-mapping.md)。M2 的稳定 ID 与 H3 编号分别管理；音轨参考、原信号复制、画内角色和实际说话者不混用。

## 12. 调用与文件组织

M11 示例（Python 3.10+ 标准库）：

```bash
cd docs/h3skill/h3-model-protocol
python scripts/m11_contract.py route assets/examples/m11-1-request.json
python scripts/m11_contract.py propose assets/examples/ref2va-request.json
python scripts/m11_contract.py accept assets/examples/proposals.json --requests assets/examples/requests.json --state assets/examples/state-empty.json
```

四个 `m11-N-request.json` 分别示范独立子职责，五模式请求可直接调用 M11.3。`propose` 输出中的 `changes.prompt_compilation.rendered_prompt` 是完整模型文本，字段外的对齐首行不会丢失；`fields` 保持精确三字段或六字段。合成参数任务包标记 `simulation_only`，真实运行资料未知时拒绝 M11.4 导出。详见 [M11 合同指南](h3-model-protocol/references/contract-guide.md)。

M10 示例（Python 3.10+ 标准库）：

```bash
cd docs/h3skill/h3-visual-look
python scripts/m10_contract.py route assets/request-standalone-m10-1.json
python scripts/m10_contract.py check assets/proposal-standalone-m10-2.json --request assets/request-standalone-m10-2.json
python scripts/m10_contract.py accept assets/state-empty.json assets/proposal-batch.json --requests assets/requests.json
```

四个子模块均可接受兼容最小输入。`accept` 输出 `.state` 内的新草稿，不写回输入；权限、来源、继承与版本检查不等于实际光照、颜色和材质效果已经通过。精确字段、最小夹具、影响分析及失败回传见 [M10 合同指南](h3-visual-look/references/contract-guide.md)。

M9 示例（Python 3.10+ 标准库）：

```bash
cd docs/h3skill/h3-shot-edit-generation
python scripts/m9_contract.py route assets/request-standalone-m9-1.json
python scripts/m9_contract.py check assets/proposal-standalone-m9-2.json --request assets/request-standalone-m9-2.json
python scripts/m9_contract.py accept assets/state-empty.json assets/proposal-batch.json --requests assets/requests.json
```

独立输入与字段约束见 [M9 合同指南](h3-shot-edit-generation/references/contract-guide.md)。M9 的结构、引用和版本检查与文字审阅、真实媒体检验分别报告；接入既有 M7／M8 时按其公开合同显式适配，不把三分区整包直接传入。

M8 示例：

```bash
cd docs/h3skill/h3-state-continuity
python scripts/m8_contract.py route assets/request-standalone-m8-3.json
python scripts/m8_contract.py check assets/proposal-standalone-m8-3.json --request assets/request-standalone-m8-3.json
python scripts/m8_contract.py accept assets/state-empty.json assets/proposal-batch.json --requests assets/requests.json
```

M8 的 `accept` 返回 `.state` 内的新草稿；M8.3 独立读取兼容策略与状态即可检查边界，无需先运行其他模块。合同或明确状态关系通过不等于自由文字语义或实际媒体已通过；精确字段与可运行示例见 [M8 合同指南](h3-state-continuity/references/contract-guide.md)。

M7 示例：

```bash
cd docs/h3skill/h3-time-synchronization
python scripts/m7_contract.py route assets/request-standalone-m7-2.json
python scripts/m7_contract.py check assets/proposal-standalone-m7-2.json --request assets/request-standalone-m7-2.json
python scripts/m7_contract.py accept assets/state-empty.json assets/proposal-batch.json --requests assets/requests.json
```

M7 的 `accept` 返回 `.state` 内的新草稿。合同与数学换算通过不表示已测得真实拍点或生成精度；精确命令、独立最小输入和已实现关系见 [M7 合同指南](h3-time-synchronization/references/contract-guide.md)。


运行包以 `SKILL.md` 为必需入口，配备必要 `scripts/`、按需 `references/` 和可复制 `assets/`；M11 另有可选的 `agents/openai.yaml` 界面元数据，运行脚本不依赖它。测试、开发报告及验证记录在包外，避免成为独立调用的隐含依赖。

M2—M6 运行脚本仅依赖 Python 3.10+ 标准库。M6 示例：

```bash
cd docs/h3skill/h3-sound-music-dialogue
python scripts/m6_contract.py route assets/request-m6-3.json
python scripts/m6_contract.py check assets/proposal-m6-3.json --request assets/request-m6-3.json
python scripts/m6_contract.py accept assets/state-empty.json assets/proposal-batch.json --requests assets/requests.json
```

M6 的四个子模块各有独立请求与提案；`accept` 返回报告中的 `.state`，只表示草稿接受。源音频未取得或真实声音未经检查时，音色、口型、语速容量、音轨贴合和完整媒体关卡保持未验证。

M5 示例：

```bash
cd docs/h3skill/h3-camera-visibility
python scripts/m5_contract.py route assets/request-m5-2.json
python scripts/m5_contract.py check assets/proposal-m5-2.json --request assets/request-m5-2.json
python scripts/m5_contract.py accept assets/state-empty.json assets/proposal-batch.json --requests assets/requests.json
```

M5 的四个子模块可单独接收兼容输入。`accept` 返回报告中的 `.state`，仍是草稿；`validation.overall` 保持未验证，不代表光学可行性、媒体效果或全局关卡通过。既有 M4 示例：

```bash
cd docs/h3skill/h3-action-performance
python scripts/m4_contract.py route assets/request-m4-1.json
python scripts/m4_contract.py check assets/proposal-m4-2.json --request assets/request-m4-2.json
python scripts/m4_contract.py accept assets/state-empty.json assets/proposal-batch.json --requests assets/requests.json
```

M4 的 `accept` 对照实际原请求、只读上下文与来源后返回新草稿；不能把接受成功理解为物理、生成或完整关卡通过。既有 M3 示例：

```bash
cd docs/h3skill/h3-scene-blocking
python scripts/m3_contract.py route assets/request-m3-1.json
python scripts/m3_contract.py check assets/proposal-m3-2.json --request assets/request-m3-2.json
python scripts/m3_contract.py accept assets/state-empty.json assets/proposal-batch.json --requests assets/requests.json
```

上例输出的顶层 `state` 是新草稿；`validation.overall` 仍为 `unverified`。样例是设计夹具，替换为任务资料后应重新检查。M3 的 `accept` 必须提供实际原请求数组，以核对上下文与来源保真。

既有 M2 示例：

```bash
cd docs/h3skill/h3-asset-reference
python scripts/m2_contract.py route assets/request-m2-3.json
python scripts/m2_contract.py check assets/proposal-m2-3.json --request assets/request-m2-3.json
python scripts/m2_contract.py accept assets/state-empty.json assets/proposal-batch.json
```

`route` 定位显式目标，语义工作尚未开始；`check` 检查已实现合同关系；`accept` 返回新草稿，真正记录在报告的 `state` 字段；`impact` 按登记消费者读路径定位失效。均不自动解读自然语言、读取媒体或调用 H3。

独立调用最小输入、数据类型、范围语义、未知处理和版本规则分别见 [M3 合同指南](h3-scene-blocking/references/contract-guide.md)与 [M2 合同指南](h3-asset-reference/references/contract-guide.md)。示例资产均为文字示例，不能当作已提供媒体。

## 13. 验证入口和完成边界

- [M11 开发与验收记录](20261105-development-m11-v001.md)：四子模块、模式／Label、源案例、参数证据与完成边界。
- [M11 行为测试](tests/test_m11_contract.py)与[验证记录](validation/m11/)：独立调用、五模式编译、负例、便携运行和前向使用。
- [M11 发布清单](release-manifest-m11.json)与[核验工具](tools/verify_m11_release.py)：新产物、官方来源、标准快照和既有文本保护。

- [M10 开发与验收记录](20261105-development-m10-v001.md)：四子模块、H3 映射、案例证据、实现与完成边界。
- [M10 行为测试](tests/test_m10_contract.py)与[实际验证记录](validation/m10/)：最小输入、独立／组合调用、风险反例、独立包运行和 Agent 文字试用。
- [M10 发布清单](release-manifest-m10.json)与[核验工具](tools/verify_m10_release.py)：文件、官方来源、案例、冻结方案和原模块保护。

- [M9 开发与验收记录](20261105-development-m9-v001.md)：职责、模式／Label、案例冲突、实际验证与完成边界。
- [M9 行为测试](tests/m9/)与[实际验证记录](validation/m9/)：独立／组合调用、负例、便携运行和 Agent 文字试用。
- [M9 发布清单](release-manifest-m9.json)与[核验工具](tools/verify_m9_release.py)：新增文件、官方源、案例、冻结方案及原模块保护。

- [M8 开发与验收记录](20261105-development-m8-v001.md)：职责、H3 映射、案例依据、实际验证与完成边界。
- [M8 行为测试](tests/m8/)与[实际验证记录](validation/m8/)：独立／组合调用、合法变化、冲突、来源保真、便携运行与 Agent 文字试用。
- [M8 发布清单](release-manifest-m8.json)与[核验工具](tools/verify_m8_release.py)：文件、来源、协议、冻结基线及原模块保护范围。

- [M7 开发与验收记录](20261105-development-m7-v001.md)：职责、来源、实现、验证与完成边界。
- [M7 行为测试](tests/m7/)与[实际验证记录](validation/m7/)：时间数学、负例、独立调用与文字试用。
- [M7 发布清单](release-manifest-m7.json)与[核验工具](tools/verify_m7_release.py)：文件、协议、来源、冻结基线与保护范围。


- [M6 开发与验收记录](20261105-development-m6-v001.md)：职责、来源、实现、实际检查与完成边界。
- [M6 行为测试](tests/test_m6_contract.py)与[实际验证记录](validation/m6/)：独立／组合调用、负例、便携运行与 Agent 文字试用。
- [M6 发布清单](release-manifest-m6.json)与[核验工具](tools/verify_m6_release.py)：文件、来源、格式、冻结基线与发布范围。

- [M5 开发与验收记录](20261105-development-m5-v001.md)：职责、实现、来源、验证与能力边界。
- [M5 测试](tests/m5/)与[实际审阅记录](validation/m5/)：独立调用、组合、失败任务、可移植性与 Agent 文字试用。
- [M5 发布清单](release-manifest-m5.json)与[核验工具](tools/verify_m5_release.py)：来源、保护范围、运行资源与记录完整性。

- [M4 开发与验收记录](20261105-development-m4-v001.md)：需求、实现、来源、实际验证和能力边界。
- [M4 测试](tests/m4/)与[实际审阅记录](validation/m4/)：独立子模块、组合、负例、可移植运行及文字试用。
- [M4 发布清单](release-manifest-m4.json)与[核验工具](tools/verify_m4_release.py)：复查文件、来源、冻结基线和保护范围。

- [M3 开发与验收记录](20261105-development-m3-v001.md)：M3 发布时的需求、设计、来源、实际验证和限制。
- [M3 测试](tests/m3/)与[实际审阅记录](validation/m3/)：独立子模块、组合、负例及文字试用。
- [M3 发布清单](release-manifest-m3.json)与[核验工具](tools/verify_m3_release.py)：在对应历史提交复查 M3 文件、来源、冻结基线及变更范围。
- [M2 开发与验收记录](20261105-development-m2-v001.md)：用户要求、设计决定、来源、实际验证和能力边界。
- [M2 测试目录](tests/m2/)：运行合同和负例。
- [M2 实际验证记录](validation/m2/)：独立使用、源完整性和本轮发布检查。
- [M2 发布清单](release-manifest-m2.json)：M2 发布快照文件与哈希。
- [M2 发布核验工具](tools/verify_m2_release.py)：重现结构、来源、基线、可移植性与清单检查。
- [M1 原开发记录](20261104-development-m1-v001.md)：首模块的实现与验收。

M3 核验器应在其对应的历史发布提交中执行。确定性工具始终保留专业语义/媒体未验证，实际 Agent 文字试用另有记录；没有 H3 推理、真实生成质量、宿主自动触发率或全流程完成声明。

## 14. 基线与历史记录

`release-manifest.json`、`tools/verify_release.py` 及原 `validation/` 下的 M1 报告对应首模块发布快照 `faa8edc3`。其中旧核验器覆盖当时整个 h3skill 目录，不能作为扩展目录后的全局核验器；M2 的 `release-manifest-m2.json` 与 `verify_m2_release.py` 对应 `91e6ed0b` 发布快照，其中的 README 哈希也具有历史范围。M3 发布使用独立清单和核验器，并核对 M1、M2 运行包字节未变。历史记录不重写为本轮结果。

M3 的 `release-manifest-m3.json` 与 `verify_m3_release.py` 同样对应其历史发布快照，其中 README 哈希不用于否决后续经授权的索引更新。M4 使用独立清单与核验器，逐项核对 M1—M3 运行包和冻结文档未变；旧报告不重写为本轮结果。

M4 的清单和核验器同样对应其历史发布快照，其中 README 哈希保留历史含义。M5 另建清单与核验器，核对 M1—M4 运行包、冻结开发文件和原案例保持不变。

在 M5 对应历史发布提交中，从仓库根执行 `python docs/h3skill/tools/verify_m5_release.py` 可复查 M5 发布完整性。历史结果见 M5 开发记录；该结果不代表 H3 推理、真实生成成功率、宿主自动触发率或全部十二模块完成。

集中来源：

- [冻结开发方案](https://github.com/Nuos/H3-h3-prompt-journal/tree/608813b6e51531ac47f860bc384a454a504fe9ff/docs/skillplan)。
- [M1 首次发布目录与原 README](https://github.com/Nuos/H3-h3-prompt-journal/tree/faa8edc311589d68d37e93524c7cb8e553fff857/docs/h3skill)。
- [M3 案例读取基线](https://github.com/Nuos/H3-h3-prompt-journal/tree/91e6ed0b09d17e13cf5f58cccfe0df588c5b1d8a/case-studies)。
- [M3 来源与许可记录](h3-scene-blocking/references/provenance-and-license.md)；[M2 来源与许可记录](h3-asset-reference/references/provenance-and-license.md)。
- [M4 来源与许可记录](h3-action-performance/references/provenance-and-license.md)；[M4 案例读取基线](https://github.com/Nuos/H3-h3-prompt-journal/tree/545a99015cfa00a6f07ee05d1d0f21e09d89d46c/case-studies)。

- [M5 来源与许可记录](h3-camera-visibility/references/provenance-and-license.md)；[M5 案例读取基线](https://github.com/Nuos/H3-h3-prompt-journal/tree/aa4ae291fa8afa0a62fa96ffde26ca25a8db8352/case-studies)。

M5 的清单、README 哈希与验证记录对应 M5 的历史发布。M6 单独新增清单与核验器，并核对原案例、冻结计划和 M1—M5 运行包的保护范围。M6 发布时，M7—M12 保持待实现；该历史状态保留在 M6 发布提交中。M6 的路由登记本身不构成后续模块执行记录。

在 M6 对应历史发布提交中，从仓库根运行 `python docs/h3skill/tools/verify_m6_release.py` 可复查 M6 发布完整性；完整执行证据与尚未验证的媒体能力见 M6 开发记录。

- [M6 来源与许可记录](h3-sound-music-dialogue/references/provenance-and-license.md)；[M6 案例读取基线](https://github.com/Nuos/H3-h3-prompt-journal/tree/780a8729cca22e13d4fa44f031f8824056a5deee/case-studies)。

M7 使用独立清单与核验器，保护 M1—M6 运行包、案例文本、冻结开发与控制文件及既有标准快照。M6 清单中的 README 哈希保留 M6 发布时含义，不能用于否决本次经授权的索引更新。M7 发布时 M8—M12 仍未实现，该历史范围不改变。

在 M7 对应历史发布提交中，从仓库根运行 `python docs/h3skill/tools/verify_m7_release.py` 可复查 M7 发布完整性。合同、数值关系、文字试用与真实媒体的完成范围分别见 M7 开发记录。

- [M7 来源与许可记录](h3-time-synchronization/references/provenance-and-license.md)；[M7 案例读取基线](https://github.com/Nuos/H3-h3-prompt-journal/tree/075fb72797fdca42bc47e38516cf3dbc16f4442d/case-studies)。

M8 使用独立发布清单与核验器，核对 339 个保护文件（原案例文本、冻结方案及控制记录、标准快照和 M1—M7 运行包）。M7 清单中的 README 哈希保留历史发布含义，不能用于否决本次经授权的索引更新。M8 发布时，M9—M12 尚未实现；该历史范围保留。

在 M8 对应历史发布提交中，从仓库根运行 `python docs/h3skill/tools/verify_m8_release.py` 可复查 M8 发布完整性；行为、文字试用和未执行的媒体层检查分别见 M8 开发记录。

- [M8 来源与许可记录](h3-state-continuity/references/provenance-and-license.md)；[M8 案例读取基线](https://github.com/Nuos/H3-h3-prompt-journal/tree/f1456793d21bfb411d36eea13cee2916c3bd20c5/case-studies)。


M9 使用独立发布清单与核验器；保护原案例、冻结方案与控制记录、标准快照和 M1—M8 运行包的 367 个文本／代码文件。旧清单中的 README 哈希表示各自发布快照，本轮经授权更新集合索引不改写历史清单。M9 发布时 M10—M12 尚未实现；该历史范围保留。

在 M9 对应历史发布提交中，从仓库根运行 `python docs/h3skill/tools/verify_m9_release.py` 可复查该次 M9 发布完整性。实际合同检查与文字试用见 M9 开发记录，H3 推理及媒体／成片验收未执行。

- [M9 来源与许可记录](h3-shot-edit-generation/references/provenance-and-license.md)；[M9 案例读取基线](https://github.com/Nuos/H3-h3-prompt-journal/tree/36987c56ade886aacfb166a21d6560925c97c330/case-studies)。


M10 使用独立发布清单与核验器；保护原案例文本、冻结方案与控制记录、标准快照和 M1—M9 运行包的 397 个文本／代码文件。旧清单中的共享 README 哈希表示各自发布快照，本轮索引更新不改写历史清单。M10 历史发布时，M11—M12 尚未实现；该历史状态不代表当前模块清单。

在 M10 对应历史发布提交中，从仓库根运行 `python docs/h3skill/tools/verify_m10_release.py` 复查 M10 发布完整性。实际行为检查、独立目录运行和前向使用见 [M10 开发记录](20261105-development-m10-v001.md)及 [M10 验证记录](validation/m10/validation-results.json)。H3 推理、像素分析和媒体／成片验收未执行。

- [M10 来源与许可记录](h3-visual-look/references/provenance-and-license.md)；[M10 案例读取基线](https://github.com/Nuos/H3-h3-prompt-journal/tree/c8ec1a4e5162ec5179ed9bec99d2f46a437ae67c/case-studies)。

M11 使用独立清单和核验器，保护基线提交 `586373218a0790382fc5eeed99574d2d58eb8eb8` 中除本索引外的 1694 个既有文本／代码文件。M1—M10、原案例、锁定开发方案及历史验证均保留原字节。M12 的模块实现和完整全流程集成不因 M11 发布而标为完成。

从仓库根运行 `python docs/h3skill/tools/verify_m11_release.py` 复查本次发布；完整命令与验证边界见 [M11 开发记录](20261105-development-m11-v001.md)和 [M11 验证结果](validation/m11/validation-results.json)。

- [M11 来源与许可记录](h3-model-protocol/references/provenance-and-license.md)；[M11 案例读取基线](https://github.com/Nuos/H3-h3-prompt-journal/tree/586373218a0790382fc5eeed99574d2d58eb8eb8/case-studies)。
