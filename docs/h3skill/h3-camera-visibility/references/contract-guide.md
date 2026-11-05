# M5 离线合同、独立调用与父接受

合同版本：`1.0.0`；实现版本：`0.1.0`。命令运行环境为 Python 3.10+ 标准库。

本合同组织摄影语义与已实现的确定性关系检查。`local_contract: pass` 不表示机位、视场、光学、碰撞或生成片已经验证；工具的整体结果继续为 `unverified`，有阻断错误时为 `fail`。

## 导航

1. 子模块与最少信息
2. 请求、提案和状态
3. 四个 CameraPlan 分区
4. 已知、未知和证据
5. 唯一父接受与重试
6. 命令、结果与操作效果
7. 变更影响与版本边界

## 1. 四个可独立调用的职责

| 目标 | `inputs` 必需键 | 最少语义信息 | 唯一写入区 |
| --- | --- | --- | --- |
| M5 | `camera_brief` | 整体观看任务与要协调的摄影范围 | 仅父接受，不产生跨区子提案 |
| M5.1 | `viewpoint_brief` | 观看任务与机位需求；相关空间未知须明确 | `/content/viewpoints` |
| M5.2 | `framing_brief`、`viewpoint_context` | 构图任务、相应机位与动作可见需求 | `/content/framing` |
| M5.3 | `focus_brief`、`framing_context` | 清晰任务和相应取景范围 | `/content/focus` |
| M5.4 | `movement_brief`、`viewpoint_context` | 摄影运动任务、起终机位与触发条件 | `/content/movements` |

确切字段、类型和最少输入见 [contracts.json](contracts.json)，路由登记见 [module-registry.json](module-registry.json)。`M5` 是父路由和组合接受入口；不能把父目标直接当作拥有四分区任意写入权的子提案。

必要输入未知时用 `{"state":"unknown","reason":"具体缺口"}`；不能直接省略合同必需键。已知的外部机位、构图等兼容输入可以直接供给，独立子模块不要求执行其他模块。真实缺项会限制对应结论，不能被独立调用的承诺掩盖。

四个子模块均返回 M5。`brief` 接受非空文字或带理由的未知对象。上下文可用相应分区、带来源与版本的 `ExternalContext`，或未知对象。`task_context`、`reference_context`、`space_context`、`action_context`、`state_context` 按需只读；声明上游所有者不等于要求先执行该上游模块。

## 2. 四类公开信封

| 对象 | 身份与用途 |
| --- | --- |
| `M5Request` | 以 `request_id`、`target`、`work_id`、`base_version` 保存实际发出的原请求及 `sources`、`inputs` |
| `M5Proposal` | 以 `proposal_id`、`module_id`、`source_request_id` 绑定原请求；保存 `context`、本分区 `changes`、问题与解决记录 |
| `M5ProposalBatch` | 将同一 `work_id`、同一 `base_version` 的子提案组成原子批次 |
| `M5State` | 父级拥有的 `CameraPlan` 草稿；保存内容、来源、版本、问题、接受收据和消费者 |

所有对象使用 `contract_version:"1.0.0"`。稳定 ID 与面向读者的中文描述分开；H3 `<Subject N>`、`[Shot N]`、发声编号与内部事件 ID 也分开。公开对象不允许通过额外字段越权写入其他模块。

`sources` 记录来源 ID、类型、定位、版本和必要摘记。该记录说明调用者声称使用什么依据，不自行证明来源真实。设计选择、案例文字、官方协议与媒体观察不能互相替代。提案的 `sources` 和 `context` 必须保真对应实际原请求；需要新信息时形成新的原请求，再产生新提案。

## 3. CameraPlan 的四个分区

- **`viewpoints`：** 观察位置、光轴与位姿。与外部主体、镜头及坐标关系建立明确引用，必要距离和高度保留单位与来源。
- **`framing`：** 画面范围、景别、构图和关键可见条件。指出对应动作阶段，区分取景要求与已经满足要求的证据。
- **`focus`：** 焦点对象、清晰范围、保持／变化策略与光学条件。资料未知时保留未知，不自动填入具体镜头参数。
- **`movements`：** 摄影事件、起终机位、路径、触发和响应。相机事件与动作事件独立编号；固定观察只描述相机行为。

具体子对象和枚举以机读合同为准；不要将专业自然语言检查表中的每一列直接当作 JSON 字段。合同中没有的跨职责修订用独立交接文字表达，或者提出明确合同扩展，不塞入未声明键。

四个分区均为 `{"items":{"稳定ID":记录}}`；记录共同包含 `shot_id` 与 `source_refs`。各类记录的主要字段如下：

| 分区 | ID 字段 | 专业字段与引用 |
| --- | --- | --- |
| `viewpoints` | `viewpoint_id` | `viewing_task`、`position`、`height`、`distance`、`optical_axis`、`roll` |
| `framing` | `framing_id` | `viewpoint_ref`、`shot_scale`、`field_of_view`、`composition`、`targets`、`visibility_assessment` |
| `focus` | `focus_id` | `framing_ref`、`focus_mode`、`focus_target`、`depth_of_field`、`clear_subjects`、`focus_changes`、`optical_basis`、`focus_assessment` |
| `movements` | `camera_event_id` | `viewpoint_ref`、`framing_ref`、`focus_ref`、`action_event_ref`、`movement_mode`、`coordination_strategy`、三项位姿变化、`path_start`、`path_end`、`path_description`、`trigger` |

三项位姿变化为 `position_change`、`optical_axis_change`、`roll_change`，取值为 `unchanged / changed / unknown`。`movement_mode` 为 `fixed / moving / unknown`；`coordination_strategy` 为 `ahead / same_phase / lag / fixed / none / unknown`。`none` 用于不与人物动作作相位配合的任务运动，例如按观看任务连续穿过水面前景；仍须声明运动触发或具体未知理由。固定观察不能同时声明位姿改变；运动后回到原端点仍可构成有效路径，不能仅凭起终位置相同判静止。

`targets` 至少一项，每项包含独立 `target_id`、`description`、`priority`、`action_event_ref`、`required_visibility` 和 `source_refs`。优先级为 `primary / secondary`。`focus_mode` 为 `fixed / follow / rack / unknown`。精确字段组合与必填性由 schema 决定，不从本表推导额外字段。

`PlanRef` 使用内部记录 ID、带来源版本与镜头 ID 的外部引用，或明确未知。`ActionRef` 还允许有理由的 `not_applicable`，以容纳没有人物动作触发的摄影事件。内部引用检查存在性和镜头归属；外部引用只检查声明的来源、版本与镜头身份，不能据此声称已经核验外部自由载荷里的全部记录。

机位、取景和运动互有关系，但不存在按编号强制执行的顺序。独立提案可以检查其所声明的输入；父接受还要核对这些只读输入与最终候选记录的一致性，不能让子模块把外部上下文偷偷写入不属于自己的分区。

## 4. 未知和证据

未知意味着缺少当前判断所需的资料；不适用意味着该要求不属于当前事件且有明确理由。两者不能互换。某项清晰目标已经写成计划，只说明目标明确；没有镜头、尺度或实际观察时不能把精确景深和真实可见性写成通过。

专业事实用 `Fact`：已知为 `{"state":"known","value":"已明确的计划或要求","source_refs":["SRC-1"]}`，未知为带理由的未知对象。`known` 表示该计划陈述有输入依据，不表示经过光学计算或生成验证。`visibility_assessment` 和 `focus_assessment` 本版本只能为 `{"state":"unverified","reason":"待核验条件"}`；禁止夹具或脚本把计划目标伪装为真实画面通过。

外部上下文中的自由 JSON 载荷只承载被声明的只读业务数据。脚本不把其中任意同名的 `state`、`source_refs` 自动重新解释成 M5 协议，也不据此获得外部数据写入权。

结构检查只核对字段与类型；引用检查只核对已声明 ID 及关系；自然语言中的路径是否可行、遮挡是否合理、焦点优先级是否满足任务仍由 Agent 审阅。无媒体时真实结果保持未验证。

## 5. 父级唯一接受

父接受对照实际原请求数组进行以下检查：

1. 核对请求、提案、批次和父状态的身份、目标、合同版本与基版本。
2. 核对完整来源及只读上下文，拒绝未经声明的增补或改写。
3. 检查每个子模块只写自身分区；同批不接受同一分区的竞争写入。
4. 检查相同提案 ID 的收据；精确重复接受保持幂等，ID 相同但内容不同应拒绝。
5. 检查合并后的引用、固定观察条件、只读投影与已实现的跨分区关系；开放阻断问题必须退回责任方。
6. 全部条件通过才返回一个新版本草稿及受影响消费者；不在失败时提交部分结果。

接受操作只返回新 JSON，不覆写状态文件。父级不在组合中改写子模块专业语义；需要改值时以当前基版本组织新提案。历史问题和修复依据保留，不能删除旧记录制造从未失败的假象。

## 6. 四个离线命令

在技能目录执行：

```bash
python scripts/m5_contract.py route assets/request-m5-2.json
python scripts/m5_contract.py check assets/proposal-m5-2.json --request assets/request-m5-2.json
python scripts/m5_contract.py check assets/proposal-batch.json --requests assets/requests.json
python scripts/m5_contract.py accept assets/state-empty.json assets/proposal-batch.json --requests assets/requests.json
python scripts/m5_contract.py impact before-state.json after-state.json
```

`accept` 的 `--requests` 是真实 `M5Request` 数组，不能根据提案现场伪造替代记录。输出中的 `.state` 是新草稿；后续检查需提取该对象。未提供实际原请求的单独 `check` 不能证明来源与上下文保真。

`check` 批次逐项检查提案及其声明的只读上下文；与父状态合并后的跨分区一致性由 `accept` 检查。四组 `request-standalone-m5-N.json`／`proposal-standalone-m5-N.json` 演示只提供本模块所需外部上下文的调用；`request-minimal-m5-2.json` 演示缺少真实机位时保留未知；组合样例使用 `requests.json` 与 `proposal-batch.json`。这些全是设计夹具。

`route` 返回目标、必需输入、资源和返回点，不执行 Agent；脚本仅实际读取合同和路由登记。专业规则需由使用技能的 Agent 按入口指示读取，不能将路由列出的全部文件写成已经执行／读取的证据。

退出码 0 表示本地合同检查通过，1 表示已实现条件阻断，2 表示参数、文件或 JSON 解析等执行错误。输入解析拒绝重复键和非有限数字。工具不联网、不调用 H3、不生成媒体，也不修改输入文件。

## 7. 影响与版本

消费者通过 `read_paths` 声明真实依赖；`impact` 根据变化路径与读取路径的祖先／后代关系标记 `stale`，保留先前失效状态。它无法发现未登记的语义依赖，审阅者应补查。无关展示文字改变不应自动触发全部制作流程。

`consumers` 可以登记 M5.1—M5.4 的已有结果，也可以登记 M1—M4、M6—M12 的下游结果。例如 M5.2 的构图结果读取了某个机位，登记对应 `/content/viewpoints/items/ID` 后，该机位变化会使该结果失效；未读取这一机位的结果保持原状态。路由登记中的潜在消费者不是自动依赖，仍须给出真实读取路径。

工具结果记录调用、输入摘要、来源与合同版本、实际读取资源、操作身份、输出状态和错误。该轨迹证明具体检查被执行，不证明未检查语义或媒体质量。

破坏性字段或语义变化使用新的合同版本和迁移说明。当前版本不自动迁移其他模块或不同版本的输入。`assets/` 全部是 D 类设计夹具；测试和开发报告放在包外，独立运行不依赖它们。
