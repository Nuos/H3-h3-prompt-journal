# M8 公开运行合同

合同版本 `1.0.0`；技能包版本 `0.1.0`；Python 3.10+ 标准库。脚本读取本包的 `contracts.json` 与 `module-registry.json`，不依赖仓库中的其他技能、案例文件或开发工具。案例路径作为来源定位符保留，不会在运行时读取。

按需导航：[所有权与最小调用](#1-所有权与最小调用) · [请求、提案与来源](#2-请求提案与来源) · [确定性检查](#3-确定性检查的范围) · [父级接受](#4-父级接受历史与失效) · [CLI](#5-公开-cli) · [夹具与验证边界](#6-夹具与验证边界)。

## 1. 所有权与最小调用

| 目标 | 最小 `inputs` | 唯一可写分区 | 职责 |
|---|---|---|---|
| M8 | `continuity_brief` | 父级原子接受 | `route` 列出子模块，不执行子模块 |
| M8.1 | `policy_brief`, `edit_context` | `ContinuityPolicy` | 边界类型、不变项、变化许可、接续线索 |
| M8.2 | `ledger_brief`, `policy_context` | `StateLedger` | 计划状态、转换、状态区间链 |
| M8.3 | `handoff_brief`, `policy_context`, `ledger_context`, `prompt_context` | `ContinuityHandoffs` | 只读核对正文末态—交接表—正文初态，关联 M12 接续决定 |

`M8State.content` 固定包含这三个分区。`owner=M8`，`object_type=StateContinuity`，`status=draft`。M8.3 发现状态错误时通过诊断的 `repair_target=M8.2` 回传，不修改 `StateLedger`。M12 观察只存在于只读 `actual_context`，M8 输出仅保存观察 ID 与接续决定。

独立调用可以直接携带合同兼容的外部上下文，无须先运行 M1–M7、M9、M11 或 M12。独立 `check` 检查外部提供的策略/账本及其引用。父级 `accept` 还要求这些上下文与当前或同批接受的本级拥有分区完全一致；不能用未纳入父对象的外部账本替换父对象。这是独立调用与父级写入的区别。

## 2. 请求、提案与来源

`M8Request` 必需字段：`kind`、`contract_version`、`work_id`、`base_version`、`request_id`、`target`、`sources`、`inputs`。`M8Proposal` 必需字段：`kind`、`contract_version`、`work_id`、`base_version`、`proposal_id`、`module_id`、`source_request_id`、`sources`、`context`、`changes`、`issues`、`resolutions`。

提案的 `context` 必须逐值等于真实原请求的 `inputs`，`sources` 也必须逐值相同。`check --request` 和 `accept --requests` 不接受只有提案自述而没有原请求的证明。目标、工作 ID、版本、请求 ID 必须匹配；每份子模块提案恰好写入自己的完整分区。JSON 重复键、非有限数、布尔值冒充整数、未声明字段和不兼容合同版本均拒绝。

来源记录包含 `kind / locator / version / excerpt`。来源 ID 一旦被父级接受，不得重绑到新版本或不同内容；来源更新使用新 ID。每个已知事实采用：

```json
{"state":"known","value":"后侧腿支撑","source_refs":["design"]}
```

这里的 `known` 表示明确声明的计划值，不表示视频已实现。未知采用 `{"state":"unknown","reason":"尚未取得末帧观察"}`；不以空白、0 或猜测代替。由 `hypothesis` 支撑的事实不能标为已知，假设也不能充当授权上下文。所有已知属性使用非空字符串，需表达数量/单位时在字符串内明确写出；本合同不负责量纲计算。

可选上下文统一使用 `{owner, source_id, source_version, values}`：

| 字段 | 归属 | `values` |
|---|---|---|
| `policy_context` | M8.1 | 完整 `ContinuityPolicy` |
| `ledger_context` | M8.2 | 完整 `StateLedger` |
| `edit_context` | M9 | `boundaries`，含类型、前后镜、必守项、批准变化和线索 |
| `reference_context` | M2 | `references`，含角色、允许与禁止属性 |
| `prompt_context` | M11 | `documents`，含正文和人工明确的状态声明 |
| `actual_context` | M12 | `observations`，含媒体与计划绑定、观察方法和覆盖范围 |
| `task_context` / `spatial_context` / `action_context` / `camera_context` / `sound_context` / `timing_context` | M1 / M3 / M4 / M5 / M6 / M7 | 不透明的只读对象；不自动解释上游全部语义 |

允许兼容适配器以 `owner=external` 提供内容，来源和版本要求相同。`Binding` 通过 `owner / source_id / source_version / path / value` 绑定只读原记录；`path` 是 JSON Pointer，`value` 必须逐值相等。M4 过程绑定另需 `ActionAdapter`，明确 `action_id / from_state / to_state / changed_attributes / steps / source_refs`，至少两条过程描述；不能借一个无关动作证明状态变化。

可选 `readonly_projection` 保存父对象的 `path / source_version / value`。请求的投影版本必须等于 `base_version`；接受时比对真实父对象在该版本的值。该投影不授予任何额外写入权。

## 3. 确定性检查的范围

### 3.1 策略

M8.1 不得改变原 `edit_context` 的边界类型、前后镜、匹配属性或线索，不能删除上游要求的不变项。变化许可必须属于上游 `approved_changes`；同一属性不能同时是许可变化和不变项/匹配项。单镜连续政策要求前后镜 ID 相同。

| 边界类型 | 比较要求 |
|---|---|
| `continuous_shot` | 同一镜；不变项保持，其他变化须有可追溯过程 |
| `continuous_action_cut` | 不变项保持；支撑、持物、道具归属、接触、朝向、方向、动作阶段变化须有过程；获准的非物理属性变化可由边界转换解释 |
| `match_cut` | 只强制指定匹配属性与不变项；其他差异需要明确变化许可 |
| `montage` | 保持声明的不变项；地点、服装等可在许可范围内变化；需要明确线索 |
| `ellipsis` | 保持声明的因果/叙事不变项；时间、地点、已完成状态变化需要许可与省略线索 |

物理属性按最后一级名称识别：`support / holding / prop_owner / contact / facing / direction / action_phase`。其他专业不变项由作者显式列入策略；脚本不推断未声明的物理规律。蒙太奇与省略的线索未知时返回 `unverified`，不能宣称连续性已确认。

### 3.2 计划状态与转换

`StateLedger` 包含 `states / transitions / chains`。每个状态是 `basis=planned`；每次转换列出端点、`changed_attributes`、原因和模式。模式为 `process / boundary / hold`。过程需要精确 M4 绑定，边界需要对应策略，保持不能悄然改变属性。任何显式 `policy_id` 都必须存在，且转换两端状态的镜头 ID 必须分别等于该策略的 `from_shot / to_shot`，不能借用其他镜头的变化许可。两端属性键应一致；缺失字段不能冒充未知。

参考图用途在 `reference_uses` 与只读 M2 权限逐项核对。`identity` 角色仅能提供属性末级名为 `identity` 或 `face` 的值，不能提供姿态、支撑、朝向或构图；真正的首帧适配器需明确 `first_frame` 角色及相应许可。

`coverage=complete_continuous` 的链要求 N 次转换、N+1 个具名区间，区间与状态顺序一一绑定；区间采用同一 `clock_id`、`unit=seconds`，相邻端点相等且每区间长度大于零。允许不同区间回到相同状态值，甚至重复引用同一状态 ID；区间 ID 必须唯一。这里校验的是调用者声明的覆盖范围，不是自动发现全片状态。浮点数采用 JSON/Python 的数值精确相等，不自行加入时间容差；复杂时基先由 M7 归一。

`coverage=snapshots` 不套用 N+1 连续区间证明，`intervals` 必须为空，结果明确标记覆盖未核实。此类锚点不代表中间动作、接触或时刻已得到证明。

### 3.3 正文末态—交接表—正文初态

M8.3 要求前镜 `final` 状态与后镜 `initial` 状态分别绑定正文声明；交接表须逐值等于账本属性。正文声明不能靠一个自述表格独立通过。

`prompt_context.values.documents` 保存原正文、镜头 ID、文档版本与 `declarations`。每个声明明确端点、状态 ID、人工审核者、`method=literal_state_declaration`、属性及逐属性文本片段。`Span.start/end` 使用 **Python Unicode 码点索引、左闭右开 `[start,end)`**，不是 UTF-8 字节，也不是 JavaScript UTF-16 代码单元。脚本检查 `text[start:end] == quote`，已知属性的字面值必须出现在对应片段中。内置中文示例包含“近侧脚掌接触石面”等非 ASCII 文本。

这是一份人工明确的文本状态适配合同。脚本不抽取自然语言状态，不理解同义、指代、否定、镜头可见性或文本中相互矛盾的其他句子。无法按字面对应的提示词由作者先审阅并修订明确表述；媒体中的手掌是否真的可见仍归 M12。仅在交接表写“手掌特写”、正文没有该字面值时不能通过。

### 3.4 M12 实际观察

观察必须包含媒体 ID/版本、计划工作 ID/版本、所比较计划状态的 SHA-256 `plan_state_digest`、状态 ID、属性、判定、方法、覆盖、定位符和 `media_observation` 来源。`plan_state_digest` 对整个计划状态记录使用排序键、无多余空格、保留 Unicode 的标准化 JSON 计算；脚本 `digest` 可用于同口径计算。摘要只是内容绑定，不是真实性签名。

出现对应观察后，`planned_only` 被拒绝。接续必须明确选择 `continue_from_observed / regenerate / replan / await_observation` 并关联观察 ID。观察未知不能直接继续；声明偏差必须有显式不同属性。选择从观察继续时，下一镜初态需要满足策略中存续项和连续物理属性；不一致回传 M8.2。重生成、重规划或等待观察保留为待办，不作为可发布判定。

M8 不改写观察，不把计划末态复制成已观察事实。任何实际观察路径均输出 `actual_authenticity_unverified`：脚本只检查声明与绑定，没有读取或验证媒体。历史计划与媒体引用保留在追加记录及接受来源中。

## 4. 父级接受、历史与失效

`accept` 接收 `M8State`、`M8ProposalBatch` 和原请求数组。顺序：形状与版本 → 原请求保真 → 所有权 → 来源与当前基础版本 → 内存中合并 → 只读上下文比对 → 语义/阻断项检查 → 新版本与回执 → 消费者失效。失败不返回候选 `state`，输入文件和调用者对象均不改动。

每批每个子模块至多一份提案。已接受记录不得删改，修订追加新 ID 并保留历史；相应完整分区及所需只读证据一并携带。来源版本更新同样使用新来源 ID。`contexts` 保存每个子模块最近一次被接受的真实输入快照，不是可由子模块额外写入的全局对象。

回执同时记录提案和原请求摘要。完全相同的已接受请求/提案重放返回 `idempotent_replay`，版本不增；同 ID 异内容、重放与新写混批、过期 `base_version`、未解决阻断项均拒绝。没有自动重试、隐式合并或重基；调用者按诊断完成有界修订后用新 ID 提交。

`impact` 以实际内容、来源、只读上下文、问题和显示字段变化路径与注册 `read_paths` 求交，标记 `stale`。可注册 `/content /sources /contexts /issues /display` 下的路径。父/子路径相交均算依赖变化；已经失效的消费者保持失效。显示标题变化只影响声明读取它的消费者。依赖原观察或正文快照的消费者应注册对应 `/contexts` 路径；未注册的语义依赖不在自动失效保证内。

## 5. 公开 CLI

在技能目录执行：

```bash
python scripts/m8_contract.py route assets/request-standalone-m8-1.json
python scripts/m8_contract.py check assets/proposal-standalone-m8-2.json --request assets/request-standalone-m8-2.json
python scripts/m8_contract.py check assets/proposal-standalone-m8-3.json --request assets/request-standalone-m8-3.json
python scripts/m8_contract.py accept assets/state-empty.json assets/proposal-batch.json --requests assets/requests.json
python scripts/m8_contract.py impact --before assets/state-empty.json --after assets/state-empty.json
```

全部命令只向标准输出返回 JSON。`status=passed` 表示所实现的确定性检查通过；`passed_with_unverified` 表示存在明确未知、待办或无法验证的证据；`failed` 表示合同/内容冲突。前两者退出码 0，失败退出码 2。成功接受仍是 `accepted_draft`，不替代全文人工审计或视频检验。

`route` 返回资源、最小输入、写入范围和返回点，`invocation=not_invoked`；不是已经执行专业推理。父级请求若只有 `continuity_brief`，仍可列出三条路由，但逐条返回 `missing_inputs / call_ready=false`，整体为 `requires_child_inputs`，不声称已具备子模块调用条件。跟踪记录保存工作/请求/提案/模块身份、基础版本、来源版本、输入 JSON 摘要、合同摘要与路由版本、时间、修订返回点、纯输出副作用声明，以及未进行媒体验证的明确标记。

## 6. 夹具与验证边界

`assets/request-standalone-m8-{1,2,3}.json` 及对应 proposal 是独立调用设计夹具；`requests.json / proposal-batch.json / state-empty.json` 是父级组合演示。案例 018/019 只提供约束依据，夹具正文、状态区间与适配器是 D 类工程设计，不是案例原文逐字复刻或真实生成结果。

包外 `tests/m8` 覆盖关键合同反例，`tests/m8_portability.py` 将单包复制到临时非仓库目录运行。脚本不实现 NLP、视频/音频读取、可见性判断、自动物理推理、生成后效果认证或完整 G1/G2 任务门禁。对这些事项的正文审阅和真实媒体测试，必须分别由技能调用者和 M12 完成。
