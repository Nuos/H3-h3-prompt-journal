# M3 公共合同与离线验收

本合同为冻结方案的 **D 类工程实现设计**，版本 `1.0.0`，技能包版本 `0.1.0`。它不是 MiniMax API、官方 JSON 协议或案例事实。逻辑对象为 `SpatialPlan`；父模块 M3 只接受子模块明确拥有的分区，不替子模块改写语义。`draft` 被接受不等于 H3 正文已编译、媒体已验证或 G0–G4 已通过。

## 导航

1. [公共入口、最小输入和所有权](#1-公共入口最小输入和所有权)
2. [JSON 文件与公共信封](#2-json-文件与公共信封)
3. [三个分区](#3-三个分区)
4. [父接受、问题与版本](#4-父接受问题与版本)
5. [命令与结果](#5-命令与结果)
6. [实际读取与增量影响](#6-实际读取与增量影响)
7. [样例和证据](#7-样例和证据)

## 1. 公共入口、最小输入和所有权

| 公共节点 | 名称 | `inputs` 最小字段 | 唯一可写分区 |
|---|---|---|---|
| M3 | 场景空间、人物站位与交互调度 | `scene_brief` | 无直接语义改写；接受子提案 |
| M3.1 | 空间坐标与场景拓扑 | `scene_brief` | `topology` |
| M3.2 | 站位与移动路线 | `topology_context`, `entity_context`, `blocking_brief` | `blocking` |
| M3.3 | 交互区域与遮挡约束 | `topology_context`, `blocking_context`, `interaction_brief` | `interactions` |

简述为非空字符串，或 `{"state":"unknown","reason":"具体缺口"}`。未知简述可以路由，但其语义未验证。`route` 只验证最小输入并返回目标、该节点建议读取的专业资源与机械依赖；资源清单不表示脚本已读取领域正文。它**不会调用子模块或自动运行 M1/M2**。子模块可以使用外部兼容投影；提供者必须明确来源与版本。M3.1 允许无人物场景，所有集合允许为空；静态方案允许无路线、无互动，不为满足模板虚构人物、动作或接触。

`entity_context` 是 M2 公共 `entities` 映射的兼容投影：每个 ID 对应 `kind / description / source_refs`；`kind` 采用 M2 的公共枚举。M3.2 必须原样复制这一投影到 `blocking.entities`。主体身份或参考授权需改动时返回 M2；相机可用 `kind: other` 明确说明其角色。稳定 ID 不等于首图中的画面槽位。

## 2. JSON 文件与公共信封

完整、可机读的形状见 [contracts.json](contracts.json)；以下说明字段语义。所有对象拒绝未知字段；ID 为以 ASCII 字母开头的 1–64 位标识。版本是非负整数，布尔值不能充当整数。数值必须有限，JSON 重复键和 NaN/Infinity 被拒绝。

| 种类 | 顶层字段 |
|---|---|
| `M3Request` | `kind`, `contract_version`, `request_id`, `target`, `work_id`, `base_version`, `sources`, `inputs` |
| `M3Proposal` | `kind`, `contract_version`, `proposal_id`, `module_id`, `work_id`, `base_version`, `source_request_id`, `sources`, `context`, `changes`, `issues`, `resolutions` |
| `M3ProposalBatch` | `kind`, `contract_version`, `batch_id`, `work_id`, `base_version`, `proposals` |
| `M3State` | `kind`, `contract_version`, `work_id`, `version`, `owner: M3`, `object_type: SpatialPlan`, `status: draft`, `sources`, `content`, `issues`, `accepted_proposals`, `consumers`；可选 `display` |

`Proposal.context` 必须与实际原请求 `inputs` 完整相等，`sources` 也必须完整相等；请求 ID、目标、工作 ID、基准版本同时核对。原请求集合为 **JSON 数组**，见 `assets/requests.json`。调用者负责提供实际原请求；本地脚本不能证明外部文件未被伪造。需要增加设计决定或证据时，应先形成新的明确请求，而非在输出里悄悄添加来源。

`changes` 是所属分区的完整替换，必须且只能包含该分区。此版不支持删除已经接受的 ID。修改一个既有条目的内容需要当前版本和新提案 ID；来源 ID 的内容不可变，来源内容或版本变化必须新建来源 ID。`accepted_proposals` 保存提案规范 JSON 的 SHA-256、来源请求 ID、模块和接受版本。

`sources` 中每条来源包含 `kind / locator / version / excerpt`。来源种类沿用 M2：`user_requirement`, `approved_plan`, `case_text`, `external_input`, `media_observation`, `design_decision`, `official_document`, `hypothesis`。各条目的 `source_refs` 必须可解析，但解析成功不证明证据真伪，也不把设计值变成观察事实。

## 3. 三个分区

### `topology`

- `frames`：`space` 为 `world / entity_local / screen`；`unit` 为 `m / cm / normalized / arbitrary`；明确 `origin` 和 `axes.x/y/z` 的文字定义、`source_refs`。`entity_local` 必须有 `anchor_entity_id`；`screen` 必须有 `view_context`，允许显式 unknown。其他坐标域不混用这两个专属字段。
- `regions`：`scene_id / frame_id / description / traversable / source_refs`。场景 ID 区分空间范围；可选 `exclusive_with` 明确声明互斥区域 ID；区域不同本身不推导互斥。`traversable` 只表示声明的可达性，不表示碰撞网格已验证。
- `connections`：`from_region / to_region / direction / passable / source_refs`，方向为 `both / forward`。此版连接要求同一场景、同一坐标框架，没有坐标变换或跨场景传送模型。

屏幕空间、主体空间与世界空间保持独立。脚本不将世界左右换算为画面左右，不反推相机位置。实体局部框架的锚点缺少投影时明确未验证。

### `blocking`

- `entities`：只读实体投影的完整副本。
- `placements`：`entity_id / region_id / frame_id / position / facing / gaze / layer / scope / source_refs`。`position`、`facing` 是三个有限数构成的向量或显式 unknown；已声明朝向不得为零向量。`gaze` 为 `kind: entity|region` 加 `target_id`，或 `kind: unknown` 加 `reason`。层次为 `foreground / middle / background / unknown`；它是设计意图，不是摄影投影结论。
- `routes`：`entity_id / frame_id / start_placement / end_placement / region_path / scope / source_refs`。`region_path` 为有序区域 ID 序列，允许后续重新进入一个区域。每对相邻区域必须有方向正确、开放的连接；各区域必须显式可通行。起终点必须属于同一实体、坐标框架和兼容场景／镜头，并匹配路径首尾区域。

`scope` 为 `scene_id / shot_id / phase`；后两项可为显式 unknown。`phase` 是声明的语义阶段 ID，不是秒数或真实排时。对站位记录，同一已知 `phase` 明确表示这些位置要在同一空间状态同时成立；移动的起点和终点须用不同相位 ID，不能把包含运动的宽泛阶段作为多个不同瞬时站位的共同相位。只在同一已知场景、镜头、阶段及可比较坐标框架中拒绝同一实体的明确相斥位置／朝向；同比例正向朝向向量等价。不同框架没有转换证据时保留未验证。不同人物共处一个区域、两条路线相交都不自动视为碰撞。不同场景、镜头、阶段不会仅因坐标相同被错误合并。

### `interactions`

- `relations`：`kind / participants / region_id / route_ids / scope / order / occlusion / view_context / description / source_refs`。种类为 `contact / crossing / avoidance / occlusion / eyeline`；参与者至少两个；`order` 引用参与者 ID；遮挡为 `allowed / forbidden / unknown / not_applicable`。可选 `occlusion_target` 为显式 unknown，或 `occluder_id / occluded_id / part`：两个人物／物体 ID 必须是不同的参与者，`part` 明确被遮挡的部位或整体；省略时按目标未知处理。
- 关联路线必须属于参与者、经过交互区域且场景／镜头兼容。同阶段已明确把参与者放在与交互区声明为互斥的区域时拒绝；未提供同阶段站位时保留未验证，不凭空认定已接触。交叉／避让次序不全、观看条件未知保留未验证。只有同一已知场景／镜头／相位、同一方向的遮挡者／被遮挡者／部位、区域和观看条件同时声明允许与禁止遮挡时才拒绝。不同部位、反向遮挡不混同；目标缺失时保留未验证，也不从 description 猜测身份或部位。
- `change_requests`：`target_module / description / read_paths / source_refs`；目标限 `M3.2 / M4 / M5 / M7 / M8`，读取路径必须在当前投影存在。需要移动人物时向 M3.2 提建议，不直接改 `blocking`。

该结构记录交互和遮挡要求，未求解几何接触、遮挡比例、视锥、物体体积、相机穿模、身体动力学或音画同步。M4 负责动作机制，M5 负责观看投影与可见性，M7 负责实际路径占时，M8 负责跨镜状态。

## 4. 父接受、问题与版本

父接受依次执行：形状和局部语义检查、实际原请求对照、工作／版本核对、同分区竞争检查、不可变来源合并、问题所有权检查、接受后完整候选验证。每个批次每分区最多一个提案；成功批次只递增一次版本。

**独立通过不代表可以直接合入空状态。** M3.2 使用的 `topology_context` 必须与接受后候选 `content.topology` 完整相等；M3.3 的两个上下文必须分别与候选 `topology / blocking` 相等。调用者可以同批提供依赖提案，或在状态里已有相同依赖。不能丢掉独立调用借用的拓扑后仍声称组合成立。

`issues` 为 ID 映射，条目包含 `owner / state / blocking / description / source_refs`。新子问题必须为本子模块拥有且 `open`。`resolutions` 为 `issue_id / description / source_refs` 数组，只能由该问题的所有者解决既有开放问题；状态中的 `resolution` 保留解决说明和来源。开放阻塞问题阻止接受；不能擦掉其他所有者的问题。

同一已接受提案 ID 与相同内容的再次调用返回 `idempotent_replay`，不新增版本。该 ID 携带不同内容、旧基准的新提案、已接受操作与新语义混在同批均拒绝。版本拒绝应重新读取当前状态并形成新提案；不能通过循环技术重试掩盖语义冲突。

## 5. 命令与结果

从技能根目录调用；Python 3.10+，仅标准库，不需要 jsonschema。

```sh
python scripts/m3_contract.py route assets/request-m3.json
python scripts/m3_contract.py check assets/request-m3-1.json
python scripts/m3_contract.py check assets/proposal-m3-2.json --request assets/request-m3-2.json
python scripts/m3_contract.py check assets/proposal-batch.json --requests assets/requests.json
python scripts/m3_contract.py accept assets/state-empty.json assets/proposal-batch.json --requests assets/requests.json
python scripts/m3_contract.py check STATE.json
python scripts/m3_contract.py impact BEFORE.json AFTER.json
```

同义 flags：`route --request REQUEST`；`check --proposal PROPOSAL --request REQUEST`；`check --state STATE`；`accept --state STATE --proposals BATCH --requests REQUESTS`；`impact --before BEFORE --after AFTER`。`check` 可检查四类公共输入；提案缺少实际 `--request` 时标记原请求保真未验证。批次本地检查不做父状态组合；最终使用 `accept`。

命令不修改输入文件、不联网、不读取媒体。结果输出 JSON 到 stdout；接受成功的状态在输出 JSON 的顶层 `state` 字段。如需持久化，由调用者从输出取出 `.state` 写入新文件，不能把整个工具结果误作状态。退出码 `0` 表示操作完成且未遇到阻塞；`1` 表示合同／语义拒绝；`2` 表示输入解析或资源错误。每次结果含调用 ID、UTC 起止时间、输入规范摘要、包版本与实际使用的合同摘要。

`execution: completed` 仅说明工具运行完毕；`local_contract: pass` 仅说明声明范围内的机械检查通过。`overall` 保持 `unverified`，除非已有失败则为 `fail`。自然语言意图、来源真伪、媒体观察、几何碰撞和接触、M5 投影、M7 实际时间、生成视频与全局验收均未验证。固定子集形状验证器只支持随包 Schema 所用词汇，不作为通用 JSON Schema 引擎。

## 6. 实际读取与增量影响

`consumers` 中每项包含 `module_id / result_version / source_state_version / read_paths`。读取路径必须为状态中真实存在的 `/content /sources /issues /display` 路径，明确记录实际读取而非笼统声称依赖所有模块。

`impact BEFORE AFTER` 比较同一作品的正序状态，对“变化路径与读取路径相同或互为祖先／后代”的消费者标记 `stale`；消费者在 BEFORE 时已经过期也继续为 stale。无交集的读取返回 `unaffected_by_declared_changes`，这是影响分析结果，不是下游作品验收。未注册消费者一律 `unverified`，显示文本改动不使无对应读取的消费者全局失效。

## 7. 样例和证据

`assets/*.json` 的庭院输入是 **D 类受控合同测试夹具**：人物、区域、路径、坐标为可复现设计值，不是实际用户请求或授权，不是新增案例集合，不是测量或媒体观察。它们演示最小公共接口与依赖组合。案例语义边界及官方 Label 映射请读取相邻领域规则和 H3 映射文档。

仓库实际回归在 `docs/h3skill/tests/m3/`；可复制的技能运行依赖全部位于本目录。将整个 `h3-scene-blocking` 目录复制到独立位置即可执行本工具；测试目录不是运行依赖。测试通过不升级为模型执行、原视频检查或 G 门验收。
