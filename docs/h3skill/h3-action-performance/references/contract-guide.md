# M4 离线调用合同与父接受规则

合同版本：`1.0.0`。工具版本：`0.1.0`。运行环境：Python 3.10+ 标准库。

本合同把 M4 的动作语义分为 `events`、`mechanics`、`outcomes` 三个分区。工具只检查公开数据合同、显式 ID / 版本关系、有向图及相同属性键的字符串值；不生成提示词，不调用 H3，不求解物理，不观察媒体，不认证生成效果。`local_contract: pass` 只说明已实现的确定性检查没有发现阻断错误，`overall` 仍为 `unverified`。

## 导航

- §1：独立子模块和最少输入。
- §2：四类公开信封、来源和版本。
- §3：事件、机制、结果分区及跨模块请求。
- §4：显式状态属性和相邻继承的检查边界。
- §5：只读上下文、原请求保真和原子父接受。
- §6：route / check / accept / impact 命令。
- §7：审计记录、原则注册和包外测试。

## 1. 可单独调用的三个模块

| 模块 | 最少输入 | 唯一写入区 | 返回父级 |
|---|---|---|---|
| M4.1 表演事件与前提 | `action_brief` | `/content/events` | M4 |
| M4.2 动作机制与交互过程 | `event_context`、`mechanics_brief` | `/content/mechanics` | M4 |
| M4.3 结果与动作接续 | `event_context`、`mechanics_context`、`outcome_brief` | `/content/outcomes` | M4 |

外部调用者无需安装 M1～M3。`event_context`、`mechanics_context` 可直接按本包合同提供；确实未知时使用 `{"state":"unknown","reason":"说明缺口"}`。缺少最少输入字段会失败；提供明确 `unknown` 则保留未验证状态。`M4` 目标只路由三个子模块，不直接变成可接受的子提案；每个提案必须绑定实际发给对应子模块的原始请求。

所有类型以 [contracts.json](contracts.json) 为准。公开对象拒绝未声明属性；`ExternalContext.values` 与只读投影的 `value` 是刻意保留的外部 JSON 容器。不可用其绕过 M4 写入权限。

## 2. 请求、提案和状态

| 信封 | 必需身份和数据 | 用途 |
|---|---|---|
| `M4Request` | `request_id`、`target`、`work_id`、`base_version`、`sources`、`inputs` | 保存实际原请求 |
| `M4Proposal` | `proposal_id`、`module_id`、`source_request_id`、`work_id`、`base_version`、`sources`、`context`、`changes`、`issues`、`resolutions` | 子模块返回分区替换提案 |
| `M4ProposalBatch` | `batch_id`、`work_id`、`base_version`、`proposals` | 一个版本上的原子组合，单批每个子模块至多一个提案 |
| `M4State` | `work_id`、`version`、`owner:M4`、`object_type:ActionPlan`、`status:draft`、`sources`、`content`、`issues`、`accepted_proposals`、`consumers` | M4 父级持有的动作计划草稿 |

所有信封带 `contract_version:"1.0.0"`。ID 使用英文字母起头的稳定标识，允许字母、数字、点、下划线、连字符，长度不超过 64；人类可读中文名称放在标签、目标、描述中。版本为非负整数，布尔值不能充作整数。当前版本不隐式迁移其他合同版本。

`sources` 是源 ID 到 `{kind,locator,version,excerpt}` 的映射。允许用户需求、批准方案、案例文字、外部输入、媒体观察、设计决定、官方文档和假设来源；类型只能表达调用者所声明的证据类别。工具校验 ID 可解析以及前后不变，不证明来源真实，不因写成 `media_observation` 就视为已看过媒体。未知信息不应通过虚构来源变成已知。

每个已知事实须携带 `source_refs`。最小未知请求可以有空 `sources`。提案的 `sources` 必须与原请求完全相同，`context` 必须与原请求 `inputs` 完全相同；提案不能偷偷补写原请求没有的观察或改变参考范围。确需引入新信息时，先由父级组织新的原请求，再返回新提案。

## 3. ActionPlan 的三个分区

### 3.1 `events`

`entities` 声明 actor / prop / environment 的稳定 ID 与来源；`requirements` 保存需求文字、覆盖的事件 ID 及来源；`items` 为事件表。事件含表演类型、角色与对象 ID、目标、前提、前置事件依赖和 `entry_state`。

`performance_kind` 可为 `body_action`、`expression`、`gaze`、`speech_action`、`prop_interaction`、`mixed`。`actor_ids` 为实际执行者，必须引用 actor；`object_ids` 为作用对象，可引用另一 actor、prop 或 environment，例如甲看向乙。所有前置依赖必须存在，事件依赖必须无环。事件没有明确需求链接会标为未验证，不会由工具补造用户需求。文字目标与真正用户意图是否相符仍须人工或智能体审阅。

### 3.2 `mechanics`

每条机制记录对应一个 `event_id`，包含：

- `process`：已知时为非空步骤数组；步骤本身可为已知事实或明确未知。
- `support`、`force`、`motion`：已知事实、明确未知或带理由的 `not_applicable`。
- `contact`：已知时包含至少两个稳定参与者 ID、描述与来源；也允许明确未知或有理由的不适用。

接触参与者必须属于同一事件的角色/对象集合。表情或视线事件无需虚构脚底支撑、身体位移、道具接触；可以明确写出不适用的原因。工具并不验证 `not_applicable` 理由在语义或物理上是否正确，审阅者仍需检查。支撑/发力等未知时不能伪装成求解完成。

### 3.3 `outcomes`

每条结果记录对应一个事件，含可见结果、`end_state` 与 `continuation`。接续可以是 `next` 加明确相邻后续事件 ID、`terminal` 加动作段终结理由，或明确未知。`next` 目标必须存在，并在目标事件的 `depends_on` 中明确包含当前事件。`depends_on` 仅声明因果/先后关系，不自动表示相邻动作；一个动作段终结仍可为另一动作段提供因果前提。接续图不能成环。

`change_requests` 只保存跨模块请求，不写其他模块的权威对象：

| 接收模块 | `request_kind` | M4 可提供的内容 |
|---|---|---|
| M3 | `space_change` | 动作需要的空间前提或冲突 |
| M5 | `visibility_need` | 必须可见的动作节点 |
| M6 | `sound_candidate` | 发声、接触、器物声音的候选关联 |
| M7 | `relative_dependency` | 事件先后与相对依赖，不能写绝对秒数排程 |
| M8 | `state_change_request` | 待审核的状态变化，可带 `proposed_state` |

M9 的分段、不可切断过程及接续约束，在 [audit-and-handoff.md](audit-and-handoff.md) 的文字交接中提供；合同 1.0.0 不包含 M9 的结构化 `ChangeRequest`。M9、M11、M12 仍可登记 `consumers.read_paths`，分别用于读取动作边界、正文编译和审计。M8 请求无 `accepted`、`authoritative` 或权威账本写入字段；其 `proposed_state` 只是待审核提案。

## 4. 状态观察与继承的准确含义

已知状态格式为 `{"state":"known","values":{"actor_id":{"property":"token"}},"source_refs":["source_id"]}`；未知时使用整体 `Unknown`。**`known` 只覆盖 `values` 中明确列出的属性，不声称未列属性已知。** 如持物手未知，应省去该属性并在相关未知事实/审计问题中解释，或把整个状态记录标成 `unknown`；不可写字符串 `"unknown"` 来冒充已知观察。

继承检查只针对 M4.3 通过 `continuation.next` 明确声明的相邻接续边：前驱 `end_state` 中属于后续事件共同参与者的每个属性，应在后续 `entry_state` 中用同一属性键和值承接。缺少属性标为 `unverified`，相同属性键却给出不同值会阻断。普通 `depends_on` 不推导状态相等，另列为未推断状态的依赖。此处仅执行字符串完全相等比较；不会判断同义词，不推理自然语言，不求解关节/力学，不自动合并多个前驱的物理结果。属性命名由调用方保持一致。

事件已知但缺少机制或结果记录，起态—过程—出态覆盖检查会给出未完成/未验证诊断。草稿允许分阶段接受 M4.1、再接受 M4.2 和 M4.3；接受草稿不意味着所有内容已完成。已明确矛盾的状态继承、悬空 ID、循环和越权字段属于阻断错误。

## 5. 只读输入与父接受

`task_context`、`reference_context`、`space_context`、`state_context` 分别属于 M1、M2、M3、M8。已知外部上下文含 `owner`、`source_id`、`source_version`、`values`，来源版本须与请求 `sources` 中记录一致；未知外部上下文用 `Unknown`。M4 完整保留这些输入的 JSON 结构和值，不据此获得外部所有权。透明载荷中的 `state`、`source_refs` 等业务字段不会被再次解释为 M4 协议。

`readonly_projection` 是 `{path,source_version,value}` 数组：路径只允许 `/content`、`/sources`、`/issues` 范围，版本须等于请求的 `base_version`，父接受时投影值须与最终候选状态完全相同。已知 `event_context`、`mechanics_context` 也须与候选状态对应分区相同。这样允许一个原子批次先提交事件、再让机制和结果读取同批事件；单独合法的 M4.2 提案不能把其只读事件上下文偷偷插入空父状态。

父接受执行以下顺序：

1. 校验父状态、批次及原请求数组的结构与身份。
2. 用实际原请求核对请求 ID、目标子模块、`work_id`、版本、完整来源和完整只读输入。
3. 验证每个子模块只写自己的分区，每批每个子模块至多一个提案。
4. 检查幂等收据。同提案 ID、同规范化 JSON SHA256 的精确重放返回原状态且不增版本；同 ID 不同内容拒绝。精确重放与新提案不得混批。
5. 新提案必须基于当前父版本。分区替换不得删除已接受实体、事件、机制、结果、请求或需求 ID；已接受实体身份与需求文字、来源和事件覆盖不得改写。
6. 来源 ID 不得绑定不同内容；新问题必须由当前子模块拥有且为开放状态。解决问题须引用先前父状态中由本子模块拥有的开放问题，并提供理由及来源。
7. 检查合并后的只读投影、图、引用、接触、状态继承及问题状态。有开放阻断问题则拒绝整批。
8. 全部通过才一次性增加父版本、记录提案收据并标记受影响的消费者；输出新的 `.state`，不修改输入文件。

“不可删除”保护已接受要求不被分区替换抹掉，不代替语义覆盖判断。当前合同不提供删除/改写已接受需求或重命名实体的特权入口；此类需求应由用户/父级明确组织后续合同迁移或新计划，不通过换措辞绕过。

## 6. 四个命令

从 skill 根目录执行：

```bash
python scripts/m4_contract.py route assets/request-m4-1.json
python scripts/m4_contract.py check assets/proposal-m4-2.json --request assets/request-m4-2.json
python scripts/m4_contract.py accept assets/state-empty.json assets/proposal-batch.json --requests assets/requests.json
python scripts/m4_contract.py impact before-state.json after-state.json
```

也支持 `--request`、`--proposal`、`--state`、`--proposals`、`--before`、`--after` 形式。`--requests` 必须是实际 `M4Request` 的 JSON 数组，不是根据提案现场拼出的替代记录。`accept` 输出为报告信封，候选状态在顶层 `.state`；后续调用应提取这个对象。

退出码：0 表示已实现的本地检查通过（整体仍未验证）；1 表示合同、来源、版本、图或接受条件阻断；2 表示参数、文件、资源或 JSON 解析错误。解析器拒绝重复键和非有限数字。脚本仅向 stdout 写 JSON；不联网、不写状态文件、不调模型。

`route` 只返回路由与资源，不执行子模块；`check` 缺少实际原请求时将来源保真标为未验证，不能替代 `accept`。`impact` 比较声明的 read path 与真实字段变化的祖先/后代交集，并保留已经 stale 的消费者。它不发现未登记的依赖；只更改 `/display` 不会使仅读取 `/content` 的消费者失效。

## 7. 审计记录与测试位置

工具结果包含调用 ID、命令、开始/结束时间、合同/实现/路由/注册表版本、输入摘要、实际加载资源摘要、来源版本、操作 ID、输出版本、幂等结果和错误码。运行成功为 `execution:completed`，与 `validation` 分开。源真实性、意图、物理、媒体、H3 生成效果和全局 G0～G4 均不由该工具证明。

HC / LC / MD / RT 注册和资源列表见 [module-registry.json](module-registry.json)。测试程序、实跑报告在仓库包外 `docs/h3skill/tests/m4/`；运行包不依赖这些测试路径。`assets` 的所有示例均明确标注为 **D 类合成设计夹具**，不能作为案例观察或官方能力证据。
