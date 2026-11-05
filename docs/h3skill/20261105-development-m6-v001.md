# M6 声音、音乐、对白与歌词关系：开发与验收记录 v0.1.0

**记录日期：** 2026-11-05（UTC）。  
**技能包：** `docs/h3skill/h3-sound-music-dialogue/`。  
**包版本：** `0.1.0`；公开合同版本：`1.0.0`。  
**读取基线：** 仓库 `780a8729cca22e13d4fa44f031f8824056a5deee`，Git tree `33be739a4044175b560733745bdd4f71d721e3d5`。  
**冻结方案：** `skillplan-v0.1.2-608813b`，控制记录 `0ce8b7b1890052bf1d4dd233ef20e68817b38f28`。

## 核心摘要

本轮实现第六个核心模块 M6，以及 M6.1 声源与说话者绑定、M6.2 对白与发声事件、M6.3 音乐与音轨使用策略、M6.4 环境与动作声音四个公开子模块。交付包括可独立复制的 Skill 目录、专业编排规则、官方输入模式与 Label 映射、版本化 SoundPlan 合同、标准库 CLI、设计样例、实际验证记录及发布核验工具。

M6 负责观众听到什么、声音来自谁或何处、使用信号还是参考特征，以及声音与事件、镜头和前后段落的关系。子模块只提交其拥有的分区，父 M6 对照真实请求和基版本唯一接受。兼容的用户文字、既有计划或外部上下文可直接满足输入，不强制按编号先执行 M1—M5。

领域方法来自本仓库 `case-studies/`；Anthropic/Agent Skills 资料提供技能创建规范，MiniMax 官方资料提供 H3 输入协议。实际读取范围、作者报告、设计延伸和未验证媒体分别登记。本轮没有听取音频、观看生成视频或调用 H3；合同通过不能解释为对白表演、音色、节拍、混音或生成质量已经通过。

## 关键结论

1. 四个声音子模块各有最小输入、独立入口、字段归属、专业资源、返回与修复路径；一个可安装包不等于只有一个不可拆分的能力。
2. 音轨内歌词提示、画面人物、实际发声者和音色参考分别绑定。歌词不自动转成口型、独立演唱或视觉实体。
3. `fully_copy` 的参照是本次登记的完整源音频作为完整最终音轨；添加、删除、替换声层或只取当前母轨的窗口均属于部分复制关系。已裁好并登记为当前源的短文件可以完整复制。
4. 原词与标点、用户明确批准的改词、音频资产版本和源窗口都有公开记录与确定性检查，不能由提案自行声明批准来绕过真实请求。
5. 同一声源和音轨可以在显式范围内跨镜复用；M6 不占有 M7 的绝对排时、M9 的剪辑决定或 M11 的最终标签编号。
6. 已记录的行为测试、独立目录调用、官方格式检查和文字试用分别证明对应范围；复杂对白、实际媒体和宿主自动触发率仍有明确边界。

**关键词：** M6、SoundPlan、声源、对白原文、歌词提示、音色参考、音轨策略、动作声音、独立调用、输入合同、H3 Label、证据范围。

## 目录导航

1. [需求与交付对应](#1-需求与交付对应)
2. [四子模块、合同和路由](#2-四子模块合同和路由)
3. [H3 输入模式、字段与 Label](#3-h3-输入模式字段与-label)
4. [案例边界与真实读取范围](#4-案例边界与真实读取范围)
5. [关键实现与审计行为](#5-关键实现与审计行为)
6. [目录结构与独立复制](#6-目录结构与独立复制)
7. [实际验证、修复与试用](#7-实际验证修复与试用)
8. [复现命令](#8-复现命令)
9. [发布范围与尚未验证事项](#9-发布范围与尚未验证事项)
10. [固定来源](#10-固定来源)

## 1. 需求与交付对应

| 本轮要求 | 实现与可检查产物 |
| --- | --- |
| 根据已冻结方案先完成 M6 | [技能入口](h3-sound-music-dialogue/SKILL.md)及四份专业规则；不调整模块清单或冻结文件 |
| 结合案例，内容边界为 `case-studies/` | [案例证据](h3-sound-music-dialogue/references/case-evidence.md)与[逐文件索引](h3-sound-music-dialogue/references/case-index.json)，记录来源、哈希、读取范围、适用条件及设计延伸 |
| 遵循 Anthropic 技能创建规范 | 必需 `SKILL.md`、合法 YAML `name`/`description`、名称与目录一致；渐进披露及同目录资源；[官方格式检查](validation/m6/official-format-check.json) |
| 明确对应的官方模块／Label | [H3 映射](h3-sound-music-dialogue/references/h3-label-mapping.md)：五模式、基础三字段、Ref2VA 六字段、四类参考 Label 及发声标记 |
| 明确编排及审计要求 | 同页逐项映射、[审计交接](h3-sound-music-dialogue/references/audit-and-handoff.md)、[合同指南](h3-sound-music-dialogue/references/contract-guide.md)和 CLI |
| 高内聚、低耦合、模块化、信息路由 | [模块登记](h3-sound-music-dialogue/references/module-registry.json)记录父子边界、最小输入、替代输入、依赖、返回、版本、失败和复验路径 |
| 记录并提交到对应文件夹 | 本报告、`validation/m6/`、`release-manifest-m6.json` 与 `tools/verify_m6_release.py`；总索引补充 M6 |

冻结框架明确指出，现有样本主要支持音乐时间和参考权限，完整对白工作流仍需剧情验证。本轮增加可执行的对白合同与文字试用，并保留这一证据限制，没有把支持字段等同于真实生成表现。[S1][S2]

## 2. 四子模块、合同和路由

### 2.1 职责、最小输入与唯一写入范围

| 节点 | 最小输入 | 产物／写入分区 | 主要判断 |
| --- | --- | --- | --- |
| M6 | `sound_brief`；组合接受另需真实子请求、基状态和提案批次 | 版本化 `SoundPlan` 草稿；唯一父接受者 | 跨分区声源、原文、音轨策略和静音关系 |
| M6.1 | `source_brief` | `/content/sources` | 谁／何处发声，声音身份如何关联实体、旁白或音轨 |
| M6.2 | `vocal_brief`、`source_context` | `/content/vocal_events` | 对白、旁白、歌唱、歌词语义提示或非语言发声的原文、语言、方式及延续 |
| M6.3 | `music_brief`、`reference_context` | `/content/music` | 完整／部分复制、特征参考、生成或无配乐；实际资产、版本、源窗口和音乐依据 |
| M6.4 | `effects_brief`、`action_context` | `/content/effects` | 环境与动作声的来源、触发、持续／停止、源内已有或新增，以及明确的全片静音指令 |

最小输入可以是有具体理由的 `Unknown`，以便继续可支持的局部工作；不能把缺失信息冒充 `NotApplicable`。`ExternalContext` 保留 `owner`、`source_id`、`source_version` 和 `values`，可以来自符合合同的外部生产者，不要求执行其对应编号模块。

公开记录为 `M6Request`、`M6Proposal`、`M6ProposalBatch`、`M6State`。`M6ToolResult.state` 是父级接受后返回的实际新状态。分区字段与证据来源表分别管理，`sources` 证据登记不等于 `/content/sources` 的声音源记录。

### 2.2 四项架构原则如何落地

| 原则 | 本轮实际机制 | 限制 |
| --- | --- | --- |
| 高内聚 HC | 声源、发声、音乐策略、环境动作声分别拥有专业规则和分区；父级只检查组合关系 | 父模块不能静默改写子模块的创作值 |
| 低耦合 LC | 有版本的公开 JSON、只读投影、替代输入、明确未知；领域声音语义与 H3 后端映射分开 | 外部上下文的真实含义和权限仍需 Agent 审阅，不能仅凭结构合法认定正确 |
| 模块化 MD | 四子节点可各自 route/check；完整依赖随包；只有标准库运行依赖；批次原子接受 | 独立调用不意味着自动生成媒体或自动执行其他节点 |
| 信息路由 RT | 显式目标、触发、最小输入映射、资源选择、成功／失败返回、修复责任方、重试和调用追踪 | 路由输出只表示下一步应读什么、调用谁；不冒充专业工作已执行 |

`route / check / accept / impact` 是确定性工具入口。自然语言理解与声音编排由读取专业资源的 Agent 完成。各次调用记录输入摘要、版本、来源版本、实际载入的合同／登记摘要、错误与副作用声明；不会通过隐含递归调用改动其他模块。

## 3. H3 输入模式、字段与 Label

### 3.1 五种模式

| 模式 | 正式结构 | M6 的交接要求 |
| --- | --- | --- |
| T2VA | 基础三字段 | 依据文字要求组织发声、音乐和环境关系，不虚构参考资产 |
| I2VA | 官方首帧对齐指令 + 基础三字段 | 图片提供视觉起态，不能证明台词、音色或真实音频偏移 |
| FL2VA | 官方首尾帧对齐指令 + 基础三字段 | 说明中间声音路径及终止／持续条件，不由画面端点推定配乐重启 |
| L2VA | 官方尾帧对齐指令 + 基础三字段 | 声音与事件收敛到尾态，尾帧不被当作音频起始点 |
| Ref2VA | 六字段和显式参考关系 | 按实际用途处理音频复制或参考，并保持主体、说话者、资产和目标镜头一致 |

基础三字段依次为 `integrated_multimodal_description`、`overall_soundscape`、`non_diegetic_music`。Ref2VA 六字段依次为 `subject_definitions`、`summary`、`retention_analysis`、`detailed_description`、`overall_soundscape`、`non_diegetic_music`。内部 SoundPlan 不作为新增 H3 顶层字段。[P1][P2]

M6.1 将声源绑定交给主正文和 Ref2VA 定义；M6.2 将话语与发声方式交给主正文；M6.3 将信号关系交给 Audio 定义、任务类型、保留分析及相应声音字段；M6.4 将特定动作声音交给主正文、将全片环境概括交给 `overall_soundscape`。仅观众可听的配乐进入 `non_diegetic_music`；画内广播、乐器或手机音乐进入主正文。

### 3.2 Label、话语与模式边界

| 标记 | M6 必须提供／审计的信息 |
| --- | --- |
| `<Subject N>` | 可见主体与实际声源的语义关系；身份参考不自动提供音色权限 |
| `<Picture N>` | 画面锚点及主体可见状态；不据静态图推断声音属性 |
| `<Video N>` | 视觉时序／编辑关系，以及其音轨是否实际启用 |
| `<Audio N>` | 实际复制或参考的信号、音色／节奏等属性、目标范围；与 Video 独立编号 |
| `(Sx)` | 目标中的独立实际发声源；跨镜复用，编号不由 Subject 编号推导 |
| `<d>[Language] …</d>` | 实际对白／歌词；姓名、动作、声源位置和表演方式放在标签外 |
| `<scenetrans>`、`<cutoff>` | 分别对应跨切继续及片尾截断；M6 提供意图，M7/M9 提供时间与切点，M11 编译 |

完整四类参考 Label 体系属于 Ref2VA。基础四模式保留各自正式 Picture 对齐用法，不直接套入 Subject/Video/Audio 的完整参考结构。五模式共用的发声／话语标记另按官方规则处理。M11 负责模式与最终编号，M6 不能在声音设计中静默改变输入协议。[P1][P2]

原文内部保留两份事实：用户原始文字、已批准使用的文字。基础模式逐词逐标点保留；Ref2VA 的基本标点规范和听不清时 `[unclear]` 规则由 M11 显式处理，不覆盖原始记录。画外旁白对应画内人物时还须明确嘴唇闭合；旁白没有对应人物时不能为了闭嘴说明而虚构一个人物。

## 4. 案例边界与真实读取范围

本轮对固定读取基线下 29 个案例目录中的 **98 个文本文件**建立来源索引，共 2,507,574 字节、45,614 行；关键词搜索匹配 1,813 行。索引读取与全文审阅分别记录：8 个文件全文阅读，5 个文件局部阅读，85 个文件仅建立关键词索引。完整阅读覆盖 5 个案例，全文或局部审阅合计 7 个案例，其中 5 个为 10 月案例。**媒体查看数为 0**。详细文件、行范围及各类读取说明见[来源索引](h3-sound-music-dialogue/references/case-index.json)。

| 证据 | 案例及实际作用 | 不能推出的结论 |
| --- | --- | --- |
| E01 | 10 月 waterfront：音轨连续、歌词内容未知、节拍词句与动作的来源关系 | 没有实际音频时不能声称已转写歌词或测量重拍 |
| E02 | 10 月 xiashan：节奏参考与完整音轨复用的冲突、作者报告的歌词视觉化问题 | 局部嘴部限制不是所有人物／所有 MV 的通用规则 |
| E03 | 10 月 kanzaki：已裁片段的资产身份、音轨复制与新增海滩／动作声冲突、无需口型的词句提示 | 不能把母轨窗口与当前已裁资产混成一个未登记对象 |
| E04 | 10 月 leg-lift：接触事件、声音与切点的关系 | M6 不因此占有动作机制或剪辑时间 |
| E05 | 10 月 sock-showcase：分段输入与连续最终母轨、跨镜不重启 | 文本提出连续性不代表真实混音已经验证 |
| E06 | 9 月 prank：短促日语发声、咳嗽／笑声、场景声与后期效果、局部近静音 | 短句样本不足以证明复杂长对白、多人重叠和打断的成功率 |
| E07 | 8 月 kitchen：无对白／歌唱／旁白／配乐时仍保留厨房动作声 | 无配乐不能推导全片无声；旧案例 `None` 不覆盖官方 `N/A` 规则 |

证据标记分别表示源文本事实 F、作者报告 A、本轮设计 D、官方协议 P、实际执行的读取／检查 I、未知 U。完整对白合同、复杂事件类型及两个新的文字任务属于本轮设计与试用，未伪装为案例原文或生成成功证据。专业规则只保留案例可支持的条件，当前明确用户要求优先。

## 5. 关键实现与审计行为

### 5.1 原文、音轨与证据保真

- `inputs.vocal_texts` 按事件 ID 锁定原文，核对每个字符和标点；遗漏事件或改 ID 不能绕过原文约束。
- 改词需要保留 `original_text`，新 `approved_text` 匹配真实请求 `approved_vocal_texts`，`rewrite_approval.value` 明确为 `true` 并有用户要求／批准方案来源；提案自身的批准声明不足以授权。
- 对白、旁白、唱词和歌词语义提示缺少文字时必须保留具体 `Unknown`，不能写成 `NotApplicable`；非语言发声可说明为何没有话语文本。
- `inputs.audio_assets` 登记后核对资产 ID、版本及窗口关系；替换音频须显式成为新的真实输入。
- 原请求来源表、只读上下文与提案必须一致。结构检查不替代来源真实性、授权范围或自然语言意图判断。

### 5.2 声音业务关系

- Source/Music 使用稳定 ID；`shot_id` 是声明镜头，`applies_to_shots` 显式列跨镜适用范围。范围外引用会失败，范围内跨镜复用不强迫另建新身份。
- `lyric_semantic` 是配乐中的语义提示，不自动生成新声音、说话者或必需口型。实际演唱须作为独立发声意图登记。
- `fully_copy` 与全片任意镜头的新发声／新效果互斥；原音轨已有声音应标为源内已有。当前长源仅复制窗口、增加或替换声层，使用部分复制关系。
- 已预裁并登记的源文件若完整作为最终音轨且没有额外声音，可以完整复制；不得偷换其与母轨的身份。
- “实测拍点”要求已登记且可用的同版音频及 `media_observation` 依据。脚本验证证据结构和对象一致性，不实际测量；仅有约 120 BPM 不能生成首拍偏移或真实拍点。
- 无配乐与全片静音分开。全片静音必须存在于实际请求并有明确用户依据，且不得与可听事件并存。未知声场不能归为静音。

### 5.3 父接受、重试与复验

`accept` 核对真实原请求、来源、只读上下文、分区归属和基版本后，一次性接受整个批次。任一阻断失败不返回部分状态，不写输入文件。精确重试返回相同状态；相同提案 ID 携带不同内容被拒绝。创作修改应使用新的提案 ID 和当前基版本。

`impact` 根据消费者实际登记的 `read_paths` 与变化路径交集，标记受影响的消费者；不会把任何元数据变化都扩成全量失效。未登记的语义依赖仍须 Agent 审阅。所有成功本地检查仍保留 `validation.overall: unverified`，不将 SoundPlan 草稿接受升级为全部 G0—G4 或媒体通过。

## 6. 目录结构与独立复制

| 位置 | 内容与角色 |
| --- | --- |
| `h3-sound-music-dialogue/SKILL.md` | 92 行入口；仅 `name` 与 `description` 前置字段；任务路由、工作流与交付边界 |
| `h3-sound-music-dialogue/references/` | 四专业规则、合同、模块登记、H3 映射、官方原文与来源许可、案例索引及审计规则 |
| `h3-sound-music-dialogue/scripts/m6_contract.py` | Python 3.10+ 标准库 CLI；不联网、不读媒体、不改输入 |
| `h3-sound-music-dialogue/assets/` | 21 个 JSON 文件；独立／组合请求、提案、基状态和设计夹具说明 |
| `tests/test_m6_contract.py`、`tests/m6_portability.py` | 包外行为测试与独立目录执行验证 |
| `validation/m6/` | 格式、行为、便携、协议审阅、实际文字任务及基线记录 |
| `release-manifest-m6.json`、`tools/verify_m6_release.py` | 发布文件身份、格式和资源检查、案例来源与保护范围验证 |

Anthropic 的必需文件是 `SKILL.md`；`scripts/`、`references/`、`assets/` 是按需要使用的资源目录，不被描述为每个技能都必须具备的固定四件套。开发报告与测试放在运行包外。包内专业资源由入口直接定位，链接不依赖兄弟技能目录；同目录复制后无需 M1—M5 文件或第三方 Python 包。`assets/` 均为设计样例，不能作为真实媒体证据。[A1][A2]

官方 H3 原文与通知保留原字节及来源归属；不把上游未知或单独声明的许可改称本仓库 MIT。领域案例许可和协议来源分别见[来源与许可](h3-sound-music-dialogue/references/provenance-and-license.md)。

## 7. 实际验证、修复与试用

### 7.1 已记录的机器检查

| 检查 | 实际结果 | 证明范围 |
| --- | --- | --- |
| 官方 `quick_validate` | 通过；`Skill is valid!` | 官方最小格式检查；非空、名称匹配和资源完整性另由发布工具补足 |
| 黑盒 CLI 行为测试 | 21 项通过 | 独立调用、分区、组合、原子失败、版本、精确重试、原文／批准／资产保真、音轨策略、歌词语义、未知和定向失效 |
| 独立目录调用 | 14 次通过；输入保持不变 | 只复制本包，在 `python -I -S` 环境执行四子节点 route/check、父 route、批次 check/accept、状态 check、精确重试和 impact |
| 官方来源身份 | 两份 H3 原文与固定提交哈希一致；6 份标准快照身份一致 | 字节与所登记来源一致，不表示本轮拥有媒体观察 |
| 发布核验 | 13 组检查通过 | 文件哈希、目录／路由／JSON／标准库、官方映射、98 文本来源、9 份冻结方案、290 项保护范围；最终提交树另行比较 |

可复查记录：[行为运行](validation/m6/behavior-test-run.json)、[详细测试输出](validation/m6/behavior-test.stderr.txt)、[便携运行](validation/m6/portability-run.json)、[官方格式](validation/m6/official-format-check.json)、[发布检查](validation/m6/release-check.json)。运行记录保存实际开始／结束时间、输入或实现摘要及结果。临时开发探针不计入正式 21 项测试数。

### 7.2 独立文档审阅与修订

[协议审阅记录](validation/m6/protocol-review.md)保留首次发现、当时文件哈希和修复后复查。两项已识别问题已修复：精确官方行号误引，以及完整参考 Label 的 Ref2VA 模式范围没有写明。后续补充的预裁资产说明由主线程对照原文复核，保留与独立审阅时版本的区别。

代码及合同审阅还促成以下具体修正：稳定声源／音轨显式跨镜范围；改词批准与实际请求精确绑定；语言和延续事实必填但允许未知；语言事件缺词不能写成不适用。对应正反例进入正式测试。发布核验工具另外修补了快照必须明确未截断、先前已读取的保护文件不能被删除后以旧 tree 冒充仍存在的问题。这里不把静态发现伪写成曾在真实 H3 生成中复现的失败。

报告交叉核对另发现“生成或静音”的简写容易混淆字段归属，已统一澄清：M6.3 的 `Music.use_strategy=none` 表示无配乐，M6.4 的 `Effect.event_kind=whole_track_silence` 才表示明确全片静音；父 M6 检查其与其他声层互斥。该项修订涉及入口、专业说明、映射和登记文字，不修改已有运行字段或逻辑。

### 7.3 两个实际使用任务

两位单独执行任务的 Agent 依据任务说明和包内公开资源实际调用 CLI。主线程提供任务并收窄到最小可复现调用路径；任务目录保存输入、候选、真实命令输出、复现方法与判断。它们是定向文字试用，不是盲测、案例视频或大样本评测。

- **MV 声音冲突任务：** 12 秒双人海边 MV，同时要求 AUDIO-MASTER 成为完整最终音轨及新增脚步／海浪；歌词未转写，只有约 120 BPM，没有真实媒体、源时长、偏移或测量。实际执行 M6.3 `route` 与携带原请求的 `check`，共 2 次业务调用：路由退出 0；检查退出 1，明确给出阻断性 `fully_copy_conflict`。另保留音频选择、音乐测量及未构造其他分区的未知。没有执行 accept，没有生成已接受 SoundPlan，也没有擅自改用部分复制或删掉新增声音。[实际结果](validation/m6/forward-use/mv/RESULT.md)、[命令与输入摘要](validation/m6/forward-use/mv/trial/20261105T160026.744863Z/command-manifest.json)、[复现脚本](validation/m6/forward-use/mv/reproduce.py)。
- **双人对白任务：** 保留三句中文原文及标点，区分店员画外旁白和访客音色参考；无配乐但保留室内环境及放置物件声，环境可跨切、对白不跨切。实际执行 10 次 CLI：首轮父 route、四子 check 和 accept 共 6 次，其中 4 次因提案把非人声源 `voice_requirement` 写成非法 `not_applicable` 而失败；修订输入后只重跑受影响的三次 check 与 accept，4 次均通过。最终得到 version 1、status=draft 的 SoundPlan，含 4 声源、3 话语事件、1 无配乐记录、3 环境／动作声事件、5 个 open warning。`local_contract=pass`，`overall=unverified`；运行代码未变。旁白与 ACT-PLACE 暂挂 SHOT-B 是明确的未确认设计假设，访客是否可见、绝对时间、音色文件和动作／对白关系继续待核实。[最终说明](validation/m6/forward-use/dialogue/FINAL.md)、[10 次实际调用与修订记录](validation/m6/forward-use/dialogue/run-summary.json)、[声音草稿](validation/m6/forward-use/dialogue/final-state.json)、[复现入口](validation/m6/forward-use/dialogue/reproduce.sh)。

试用期间还说明过“语言文本缺失必须未知、不得不适用”以及无配乐／全片静音字段归属的窄修订。执行步骤由主线程收敛，不能据这些任务计算独立触发成功率或盲测通过率。完成后的任务结果与实施版本分别保留；预期拒绝也保留原始输出，不只保存成功结果。

## 8. 复现命令

在完整仓库检出中，从仓库根目录执行：

```bash
python -B -m unittest discover -s docs/h3skill/tests -p test_m6_contract.py -v
python -B docs/h3skill/tests/m6_portability.py
python docs/h3skill/_standards/anthropics-quick-validate.py docs/h3skill/h3-sound-music-dialogue
python -B docs/h3skill/tools/verify_m6_release.py
```

正式格式脚本使用其上游环境依赖；运行 Skill 自身只依赖 Python 标准库。若工作区只是部分文件快照，发布工具要求实际取得的、明确未截断的递归 Git tree，并核对其预期身份；这不把缺失媒体视为已下载或已阅览。`--tree-snapshot` 的基树检查只证明该固定树，最终提交树仍需另行比较。

独立复制技能目录后，在该目录执行：

```bash
python scripts/m6_contract.py route assets/request-standalone-m6-2.json
python scripts/m6_contract.py check assets/proposal-standalone-m6-2.json --request assets/request-standalone-m6-2.json
python scripts/m6_contract.py accept assets/state-empty.json assets/proposal-batch.json --requests assets/requests.json
```

更换设计样例为真实任务输入后应重新检查。`accept` 只向标准输出返回 `.state`，不自动保存、混音或运行 H3。

## 9. 发布范围与尚未验证事项

发布范围限于新增 M6 运行包、本报告、新的 M6 测试／工具／验证记录／清单，以及 `docs/h3skill/README.md` 的 M6 导航更新。保护范围有 290 个源文件：原 `case-studies/`、冻结 `docs/skillplan/` 和 M1—M5 运行包。155 个已物化文件核对本地字节，全部 290 项同时可用固定树的 Git blob 与 mode 核对；媒体身份检查不等于媒体语义检查。

工作区是通过 GitHub 接口取得的源文件快照，并非 Git 工作树。本轮不宣称执行过本地 `git diff --check`。发布前后通过 Git tree 比较核对真实修改路径、blob、mode 和保护范围；并使用带预期旧 HEAD 的非强制更新避免覆盖并发改动。发布清单排除它自身及由其派生的发布检查输出，避免自引用哈希循环。

本轮没有完成 M7—M12。没有执行自动听写、音色识别、节拍检测、音频合成、声音克隆、混音或 H3 推理；没有验证真实口型、对白语速容量、复杂多人重叠、跨镜音响效果或生成质量。任务合同可表达这些待核实关系，不能据此宣称媒体能力已完成。宿主自动触发率、任意任务鲁棒性与大规模用户效果也没有测量。

## 10. 固定来源

- [S1 冻结核心框架](https://github.com/Nuos/H3-h3-prompt-journal/blob/608813b6e51531ac47f860bc384a454a504fe9ff/docs/skillplan/01-core-framework.md)：M6 职责、SoundPlan、跨模块边界与样本限制。
- [S2 冻结模块化与路由原则](https://github.com/Nuos/H3-h3-prompt-journal/blob/608813b6e51531ac47f860bc384a454a504fe9ff/docs/skillplan/06-modularity-routing-principles.md)：HC/LC/MD/RT、独立能力和四子模块。
- [S3 案例读取基线](https://github.com/Nuos/H3-h3-prompt-journal/tree/780a8729cca22e13d4fa44f031f8824056a5deee/case-studies)：本轮领域证据唯一目录；具体范围见随包 case-index。
- [P1 MiniMax H3 基础官方原文](https://github.com/MiniMax-AI/MiniMax-H3/blob/199b7d0e1fd95e7b3eafa8c15eca692534142427/skills/h3-prompt-writing/references/base-en.txt)。
- [P2 MiniMax H3 Ref2VA 官方原文](https://github.com/MiniMax-AI/MiniMax-H3/blob/199b7d0e1fd95e7b3eafa8c15eca692534142427/skills/h3-prompt-writing/references/ref-en.txt)。
- [A1 Anthropic skills 固定提交](https://github.com/anthropics/skills/tree/ca45fc496a3436251f191354091d557da31c15b5)：技能创建方式、模板及最小校验器；快照身份沿用并复查已有 `_standards/`。
- [A2 Agent Skills 正式规范固定提交](https://github.com/agentskills/agentskills/blob/83021e2be457a9b6679148719c1f6074f0ad975e/docs/specification.mdx)：前置字段、目录与渐进披露；实际格式记录单独保存。

H3 原文 SHA-256：base `2cfebc096a6e08370f288d468d90b60f7f9bcb938f94bf090816e910e48e75fc`；ref `1e574f356716ad55612247ffb7bbccbcdb484ad96599d63c7dca1af186b1fab7`。来源定位与许可记录不替代运行结果，运行结果也不替代实际媒体证据。
