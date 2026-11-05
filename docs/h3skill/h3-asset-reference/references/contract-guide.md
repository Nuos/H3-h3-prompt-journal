# M2 公开合同与离线调用

## 目录导航

1. 版本、对象与字段责任
2. 最小请求与独立调用
3. 资产、实体、绑定与权限
4. 范围、声音与冲突裁决
5. 子提案和父接受
6. 命令、状态与执行记录
7. 真实依赖的变更影响
8. 使用边界与受控示例

## 1. 版本、对象与字段责任

技能版本为 `0.1.0`，本模块公开合同为 `1.0.0`。只固定 M2 自身的接口，不宣称十二模块的共享 Schema 已全部实现。合同、算法与 ID 方案是对冻结架构的 D 类实现细化；领域方法仍以所列案例文本为依据。

`contracts.json` 是 JSON Schema Draft 2020-12 形状定义。`m2_contract.py` 只执行该固定文件使用的 Schema 词汇，并加上来源、引用、字段责任、范围重叠与版本检查；它不是接受任意 Schema 的通用校验器。Schema 本身不表达全部跨对象约束，因此只通过 JSON Schema 不等于通过 M2 确定性检查。

| `kind` | 用途 | 责任 |
|---|---|---|
| `M2Request` | 一次任务的版本、目标和最小只读输入 | 当前调用者/Agent |
| `M2Proposal` | 单个子模块对自己分区的候选更新 | M2.1 / M2.2 / M2.3 |
| `M2ProposalBatch` | 同作品、同基版本的一组提案 | 调用者收集；每分区只能一个提案 |
| `M2State` | 三对象的共同快照，始终保持 `draft` | 由 M2 唯一接受 |
| `M2ToolResult` | 命令报告、确定性诊断和可选新状态 | 离线工具；不是模型请求 |

`M2State.content` 的三分区直接对应冻结方案中的公开对象：

| 分区 | 公开对象 | 唯一专业责任 |
|---|---|---|
| `asset_registry` | `AssetRegistry` | M2.1：资产及来源、访问、观察状态 |
| `entity_registry.entities` / `.bindings` | `EntityRegistry` | M2.2：稳定实体与来源选择 |
| `reference_map.permissions` / `.decisions` | `ReferenceMap` | M2.3：属性权限、范围和冲突决定 |

M2State 另含 `work_id`、非负整数 `version`、`owner_module: M2`、`status: draft`、`sources`、`issues`、`accepted_proposals`、`consumers` 与可选标题所在的 `display` 对象。版本 0 的空三分区仅是起点。所有稳定 ID 使用 1–64 个 ASCII 字母、数字、点、下划线、连字符，首字符为字母；后端 `<Subject N>` 等标签不能充当稳定 ID。

## 2. 最小请求与独立调用

请求必含 `kind`、`contract_version`、`request_id`、`target`、`work_id`、`base_version`、`sources`、`inputs`。每次只展开需要的输入，不要求运行指定上游生产者。

| `target` | 必需 `inputs` | 可独立处理的职责 |
|---|---|---|
| `M2` | `material_brief` | 开始整体素材与权限整理；逐步建立子请求 |
| `M2.1` | `material_brief` | 资产来源、待提供项和观察依据登记 |
| `M2.2` | `asset_context`、`binding_brief` | 已知资产与目标实体的源选择绑定 |
| `M2.3` | `asset_context`、`entity_context`、`permission_brief` | 已知绑定的按属性权限与范围分配 |

`material_brief`、`binding_brief`、`permission_brief` 为非空文字，或显式 `{ "state": "unknown", "reason": "缺少什么" }`。`asset_context` 是选定的 `AssetRegistry` 记录映射；`entity_context` 包含选定的 `entities` 和 `bindings` 映射。它们可以来自用户、已有项目或其他兼容实现；不必先调用 M1、M2.1 或 M2.2。投影中应包含被选记录实际引用的实体、资产及派生来源。

三个子节点均可另读相关的 `intent_context` 和 `capability_context` 文字/未知项；前者可来自已有 M1 WorkBrief 的必要投影，后者可来自带版本的 M11 能力资料。完整 M2 请求也可携带后续子任务所需字段。局部子请求不得夹带其他节点不读取的字段。

完整 M2 请求可附 `asset_context`、`binding_brief`、`entity_context`、`permission_brief`。逐提案与该请求对照时，只检查当前子节点声明读取的结构投影：M2.1 无只读分区，M2.2 读取资产，M2.3 读取资产与实体；不要求子节点把自己负责写入的分区再复制进只读 context。若分步过程产生新资产或实体版本，应显式构造新子请求并保留其真实来源请求 ID，再对照该请求。

`route` 只核对显式目标和合同，然后返回单节点分派、资源及返回点；它不判断自然语言是否应触发技能，不自动运行上游，也不替 Agent 整理语义。未知输入可保留为部分任务，但不能据此推出完整结果已通过。

## 3. 资产、实体、绑定与权限

### 来源与授权分开

每个 `sources` 条目保存 `kind`、`locator`、`version`、`excerpt`。支持 `user_requirement`、`approved_plan`、`case_text`、`external_input`、`media_observation`、`design_decision`、`official_document`、`hypothesis`。

内容通过 `source_refs` 指向依据。`authority_refs` 则专指当前目标中允许分配用途的用户要求或已批准计划，只能引用 `user_requirement` / `approved_plan`。来源类别只是所提交记录的声明；工具不能认证谁真正批准了计划，也不能判断授权文字是否涵盖该实体、属性和范围，必须人工/Agent 回查原文。案例证据、图片里可见的事实、作者自述和模型猜测都不能单独转成目标授权。

同一来源 ID 的内容不可在 `accept` 时改写；新增证据、版本或授权使用新 ID。使用 `check PROPOSAL --request REQUEST` 时，提案必须保留请求所声明的来源投影原值，可以新增来源，不能借保留同一个 `source_request_id` 改写原授权文字。文字保真仍需语义审查。

### AssetRegistry

资产条目最少包含：`media_type`、`channels`、`locator`、`source_version`、`description`、`availability`、`access_state`、`observation_state`、`observation_refs`、`source_refs`。

| 字段 | 允许值/意义 |
|---|---|
| `media_type` | `image` / `video` / `audio` / `text` |
| `channels` | 图像为 `visual`，音频为 `audio`，视频可声明 `visual` 和/或 `audio`，文字为 `text`；不由扩展名猜测 |
| `availability` | `provided` / `pending` / `unavailable` |
| `access_state` | `accessible` / `not_checked` / `inaccessible`；这里记录外部已取得的访问结论，脚本不访问定位符 |
| `observation_state` | `unobserved` / `description_only` / `observed` |
| `locator` / `source_version` | 具体定位与媒体版本；尚未取得时使用显式 unknown |

记录 `observed` 必须附 `media_observation` 类来源和非空 `observation_scope`，说明实际检查了哪些帧、区域或音频区间；并不代表全片已观察，也不代表工具认证了该观察。作者的效果说明只能保留为案例文字。观察可以是过去版本的记录，与当前能否访问区分开；版本和范围由审阅者核对。

可选 `sha256` 为已计算的 64 位小写十六进制摘要；脚本不替调用者计算媒体摘要。可选 `duration_seconds` 为已取得且有来源的时长，不是从段落或 BPM 猜测的值。`derived_from` 引用已登记源资产，可表达独立提取音频或取出的帧；不允许悬空或循环派生，也不据此声称执行过提取。

### EntityRegistry

实体条目含 `kind`、`description`、`source_refs`，类型支持 `person`、`animal`、`object`、`scene`、`motion`、`style`、`voice`、`soundtrack`、`other`。具体类型区分用途，不限制人数或要求每份文件只能对应一个实体。

绑定条目含 `entity_id`、`asset_id`、`channel`、`source_selector`、`state`、`authority_refs`、`source_refs`。`source_selector` 明确指出同一文件中的哪个人、区域、场景内容或轨道；源图“左边人物”只是定位源内容，不是目标画面里该人物的永久站位。

`state` 为 `confirmed` / `candidate` / `unknown`。`confirmed` 表示**目标与源选择的指定关系已经有明确授权**，不表示素材外观已经被视觉确认；实际媒体仍可待提供。确认绑定必须有具体选择文字和授权来源。候选绑定不直接获得允许继承的权限。

多个同类型目标实体若指向同一资产、同一通道、完全相同的选择文字，须使用不同源选择，或在相关绑定中用 `shared_selection_reason` 记录明确授权的共享原因，例如用户确实要求一个身份复制为两个目标。自然语言选择是否真的定位了不同人，仍须语义/视觉核对。

### ReferenceMap

每条权限只规定一个 `binding_id`、一个 `attribute`、一个明确范围和一种决定。由绑定解析出资产与实体，避免独立填写三组 ID 后彼此漂移。权限字段是：`binding_id`、`attribute`、`decision`、`use`、`scope`、`authority_refs`、`source_refs`、`reason`，以及可选 `source_window`。

`decision` 为 `allow` / `forbid` / `unknown`。未列出的属性仍未获授权，不会默认继承；unknown 不等于禁止，也不等于允许。属性枚举包括身份、外观、服饰、姿态、表情、场景、空间、运动、摄影、风格、照明、色彩、音色、音频内容/时序，以及首帧、尾帧和关键帧；精确拼写见 Schema 的 `Permission.attribute`。

`use` 为 `reference` / `copy` / `anchor`。本合同用 `copy` 表达音频内容原样复制的意图，用 `anchor` 表达实际图像帧约束，用 `reference` 表达其他属性参考。脚本不导出实际复制操作、帧标签或媒体。图像可以提示动作意图，但不能仅凭静态图证明连续运动已被测量。

声音属性要按实际要求选择：只参考节奏、节拍或起点时用 `audio_timing/reference`；只参考音色时用 `voice/reference`；明确要求采用词句并重新演绎时才给相应的 `audio_content/reference`；复制原信号用 `audio_content/copy`。不能把“仅节奏”额外登记为声音内容许可，再依靠 reason 的否定句缩回范围。声音内容和音色也不因同一 `<Audio N>` 来源而自动同时授权。

## 4. 范围、声音与冲突裁决

`scope` 只能选择一种明确形状：

```json
{"kind":"work"}
{"kind":"shots","shot_ids":["SHOT-1","SHOT-2"]}
{"kind":"time","domain":"generation","timeline_id":"GEN-1","start_seconds":0,"end_seconds":2}
{"kind":"unknown","reason":"未确定作用镜头"}
```

时间域只接受 `work` / `generation`，秒数必须有限、非负，终点大于起点，区间为前闭后开 `[start,end)`。这只是消费 M7/M9 或用户已提供的范围，不由 M2 决定权威排时。源取样区间另用 `source_window`，其形状为 `{"domain":"source","unit":"seconds","start_seconds":2,"end_seconds":5}`；有已登记源时长时检查上界。

`source_window` 未填写时，不进一步缩小绑定中 `source_selector` 已选定的内容；这不证明源时长或最终拷贝区间已知。对同一资产、通道、源内选择、属性和用途，一条没有源时间窗限制的禁止记录也约束其子区间。两个显式源时间窗按同样的前闭后开规则判断交集，不能通过把整段允许/禁止改成重叠子窗来逃避矛盾检查。最终目标范围仍另由 `scope` 决定。

两个相邻的同域时间窗不重叠；两个镜头集合按 ID 交集判断。跨时间域、不同时间轴、镜头范围对时间范围，以及 unknown 范围，缺少映射时只能返回 `scope_overlap_unresolved`，不能宣布没有冲突。`work` 必须是明确给出的全作品范围，不能由 unknown 自动补成。

视频的 `audio` 只是所声明的嵌入通道。它可以登记声音参考意图，但不能据此声称已上传独立 `<Audio N>` 输入。需要独立音频时，应登记真实或待提供的独立 `audio` 资产、提取来源与用途，再由 M6/M7/M11 核对声音内容、区间和后端输入。脚本不创造音频、第二人物或模型标签。

同实体、同属性、同用途、已知重叠范围的冲突规则：

- 同一个具体来源选择的 `allow` 与 `forbid` 相冲突。
- 不同具体来源同时 `allow` 时，需要明确选择或共同参考决定；一个来源被排除、另一个来源被允许，不构成同源自相矛盾。
- 实际允许某图成为首/尾/关键帧锚定，同时排除同源姿态、外观、服装、场景、空间或摄影时，需回到当前请求和实际绑定审查。单纯身份参考不会触发锚帧检查。

`use` 是独立权限维度。同一音频的 `audio_content` 可以同时 `reference: allow`（参考词句并重新演绎）与 `copy: forbid`（禁止原信号复制）。前者不授予后者，两条可以共存；同一用途的允许/禁止仍然冲突。不同用途的多源记录不自动竞争，但最终声音组合仍须 M6/M11 审阅。真实帧锚定与同源画面属性排除的跨属性检查不受此用途区分豁免。

`decisions` 每条包含 `permission_ids`、`strategy`、`selected_permission_ids`、`reason`、`authority_refs`、`source_refs`。`select` 必须只选一个候选；`combine` 必须选择至少两个允许且为 `reference` 的兼容候选，例如同一主体的多个视角。不能用 combine 掩盖允许/禁止矛盾、两个独占帧锚定或同时原样复制的冲突。

一次决定只能覆盖同实体、同属性、同用途、**完全相等且已知的范围**。部分交叉范围应先拆分成明确记录再裁决，不能静默扩大选定范围；不得把可共存的参考许可与复制禁令放入同一选择组而丢弃后者。所有候选保留在权限表中；读取生效许可时，先应用 decisions 的选中集合，再消费剩余活动记录，不能把被放弃的旧候选也交给编译器。共同参考的真实兼容性仍需领域审阅。

## 5. 子提案和父接受

`M2Proposal` 记录 `proposal_id`、`module_id`、`work_id`、`base_version`、`source_request_id`、`sources`、`context`、`changes`、`issues`、`resolutions` 及类型/合同版本。`changes` 必须且只能包含该子模块拥有的一整个分区；更新分区时保留其他已登记条目。

M2.1 的 context 为空；M2.2 只读 `context.asset_registry`；M2.3 只读 `context.asset_registry` 和 `context.entity_registry`。独立检查使用这些外部兼容投影解析引用。父接受时再逐条对照它们与候选共同状态，防止基版本数字相同但实际上读了另一版内容。

批次用 `{"kind":"M2ProposalBatch","contract_version":"1.0.0","proposals":[...]}`。各提案的作品和基版本相同，每分区只允许一位提交者；一个批次整体产生一个新版本。分步接受时后续提案必须重新审阅最新输入，不能只改 base_version 数字。

当前合同不执行删除已接受 ID 的操作；从完整分区漏掉旧条目会被拒绝。保留旧权限候选，通过有来源的修改或显式裁决确定生效条目。后续若需要正式退休/删除合同，应扩展版本与迁移规则，不能用遗漏条目作为隐含删除。

`issues` 保存问题 ID、责任者、open/resolved 状态、阻塞标记、说明和来源。父接受保留问题；一个子模块只能通过 `resolutions` 解决自己已有的 open 问题。未经解决的用户或其他模块问题不会被新提案删除。保存部分草稿不等于解除这些阻塞。

**父接受没有原始请求参数，因此不能替代 `check --request`。** 正式接受前应分别将各子提案与它的实际原请求核对，再做语义审查和父接受。accept 核对当前状态、来源不可重定义、字段责任、版本、投影和跨对象一致性；它不认证原始用户意图，也不证明先前审阅已真实执行。

## 6. 命令、状态与执行记录

从技能目录执行；Python 3.10+ 标准库即可，无 GPU、API 密钥或联网依赖：

```bash
python scripts/m2_contract.py route assets/request-m2-2.json
python scripts/m2_contract.py check assets/proposal-m2-2.json --request assets/request-m2-2.json
python scripts/m2_contract.py check assets/proposal-batch.json
python scripts/m2_contract.py accept assets/state-empty.json assets/proposal-batch.json
python scripts/m2_contract.py impact previous-state.json current-state.json
```

命令只把新 JSON 写入标准输出，不原地修改输入。需要保存时使用新的任务文件；accept 成功的真实 `M2State` 位于返回对象的 `state` 键下，不要把整个 `M2ToolResult` 当作下一次输入。

| 结果 | 正确解释 |
|---|---|
| `execution_status: completed` | 技术计算已经结束 |
| `outcome: accepted_draft` | M2 返回新草稿；不代表 G0/G1、素材就绪或视频质量通过 |
| `audit.deterministic: pass` | 本次已执行的结构/引用/版本/范围检查未发现确定性错误 |
| `audit.semantic: unverified` | 文字、来源真实性、当前授权、源选择与任务保真仍需审阅 |
| `audit.media: unverified` | 未执行媒体观察或 H3 推理 |
| `audit.overall: unverified` | 保留未验证边界；发现确定性错误时为 fail |

退出码 0 表示这次确定性操作完成；1 表示确定性错误/拒绝；2 表示文件、JSON 或资源读取错误。重复 JSON 键、非有限数值和坏 JSON 被明确拒绝，不采用“最后一个键覆盖前面”处理。调用记录保存调用 ID、UTC 起止、输入规范 JSON 摘要、合同版本、实际读取的资源、操作类型和重试次数。dispatch 中的领域资源只是后续应读清单，不冒充脚本已经执行了语义读取。

## 7. 真实依赖的变更影响

`consumers` 只登记真实的消费关系：消费者 ID 对应 `module_id`、`result_version`、`source_state_version`、`read_paths`。路径为 JSON Pointer，指向实际消费的 `/content`、`/sources`、`/issues` 或 `/display` 内的字段。当前版本引用的路径必须存在。

`impact PREVIOUS CURRENT` 只接受同作品的先后快照，按路径及祖先/后代关系标记 `stale` 或 `unchanged_dependencies`。未读取标题的消费者不因标题改变自动重做；已经引用旧版的消费者仍为 stale。`unchanged_dependencies` 只是声明读字段未变化，不是新一次语义通过。未登记的下游依赖保持 unknown，不推断十二模块全部无需复验。

## 8. 使用边界与受控示例

全部示例围绕 CASE-019 的参考分权文字构造，使用 `WORK-IDENTITY-DEMO`，包含三项待提供资产、表演者/场景/音乐实体，以及三份独立提案。`SRC-EXAMPLE-REQUEST` 明确标记为**受控示例任务的授权**；不能把它复制进真实项目充当用户许可。模板不包含真实图片、音频或已测时长。

独立使用本目录即可取得运行资源，不依赖兄弟技能、开发测试或冻结计划目录。源计划用于追溯，不是脚本运行依赖。该实现不负责完整源片逆向、真实素材下载/提取、真实主体识别、模型能力认证、最终提示词编译、H3 推理或成片审计；相关缺项以有版本的交接记录返回责任模块。
