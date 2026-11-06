# M9 公共合同与命令

## 1. 范围和版本

本包实现 `contract_version: "1.0.0"`、`route_version: "1.0.0"`，父对象为 `ShotEditGenerationPlan`，始终标为 `draft`。机读字段以 [contracts.json](contracts.json) 为准，节点责任、读写权限、路由、资源、失败返回点和兼容性见 [module-registry.json](module-registry.json)。本合同是冻结方案 v0.1.2 的 M9 工程实现，不是 H3 的新输入字段。

运行只依赖 Python 3.10+ 标准库。复制整个技能目录即可执行；运行时不读取兄弟技能、仓库案例路径、网络或宿主 SDK。脚本只将 JSON 写到 stdout，不修改输入文件、不发起生成或剪辑任务、不自动调用上游。案例来源路径用于追溯；随包专业参考和明确输入用于工作。

`passed_with_unverified` 表示已实现的结构和显式关系检查通过。来源、能力、批准信息仍是调用者提供的声明；脚本不验证网页真实性，不识别自然语言中的隐含矛盾，不识别真实媒体切点、动作或接缝，也不代表完整 G1/G2 或 G3/G4 通过。`failed` 退出码为 2，成功或信息性影响分析为 0。运行异常、重复 JSON 键、非有限数字、未知版本和未声明字段均拒绝。

## 2. 三个独占子合同

| 子模块 | 输入只读投影 | 唯一写入分区 | 输出消费者 |
| --- | --- | --- | --- |
| M9.1 | M4/external 的阶段和事件 ID；M5/external 的同镜摄影事件 ID | `ShotMap` | M9.2、M9.3、M11、M12 |
| M9.2 | `ShotMap`；带版本源片及范围；M8/external 连续性政策 | `EditGraph` | M9.3、M7、M8、M11、M12 |
| M9.3 | `ShotMap`、`EditGraph`；M8/external 状态与政策；M11/external 能力；M7/external 时长记录；M2/external 素材 ID | `GenerationPlan` | M7、M8、M11、M12 |

每个投影使用 `{owner, source_id, source_version, values}`。`owner` 只能是该字段声明的上游或 `external`；本适配合同的 `source_version` 是**非空字符串**，必须与 `sources[source_id].version` 完全一致。来源记录包含 `kind / locator / version / excerpt`。真实外部资料可替代上游执行，仍须提供具体值和出处；`external` 不是跳过校验的开关。未知值不以空字符串或猜测值顶替。

这里的投影是有版本的适配格式，不宣称既有 M2—M8/M11 对象可以原封不动传入。例如 M7 通用 Projection 与 `Mapping.edit_binding` 的版本类型可能不同；必须按接收合同转换并保留原始版本标识。`Mapping.edit_binding` 要求的只读记录是 `{owner, source_id, source_version, path, value}`，不能直接使用本包通用投影。M8 既有 `EditValues.boundaries` 是按 ID 索引的 `EditBoundary`，字段为 `boundary_id / boundary_type / from_shot / to_shot / invariants / match_attributes / approved_changes / cue`，不能把 `EditGraph` 整包当成它。适配时由明确的执行环节、连续性策略和 M8 已有许可形成该最小投影；没有不变量或已批准变化的证据时回交 M8，不为满足格式捏造批准项。

### M9.1：ShotMap

`phases / shots / panels / events` 分别使用独立稳定 ID。镜头的 `phase_ids` 与 `panel_ids` 声明归属；画格反向标注 `shot_id` 和 `phase_ids`。多个阶段、多个画格可属于同一镜头，同一阶段也可跨真实切镜，`assignment_note` 说明使用哪一部分及理由。脚本核对关系，不判断这段文字是否充分表达相位。

`events.kind` 区分 `cut / camera_change / assembly_join`。真实 `cut` 的出入镜 ID 必须不同；同镜摄影变化和同镜装配接缝保持同一镜 ID。M5 提供的 `camera_event_ids` 不能改成切镜。阶段、事件 ID 必须来自实际输入；M9 不重新编写 M4 动作或 M5 摄影方案。画格目的可为 `storyboard / key_state / first_frame_intent / last_frame_intent / reference_only`，意图标签不是最终模型参考 Label。

### M9.2：EditGraph

`segments` 是具体剪辑实例，独立于镜头和生成任务。一个实例可包含多个 `shot_ids`，同一来源可被多个实例重复使用。`source_id` 对应只读源范围的 `media_id`，源范围另有 `media_version`，不能把它与证据 `source_id` 混用。`assembly` 恰好一次列出每个实例；重复采用来源时使用新的实例 ID。

`window` 用半开区间 `[start, end)`，显式保留 `domain: source_local | generation_local`、`unit: second | frame`、`basis: planned | observed` 和 `range_source_ref`。脚本仅在同单位同坐标域内检查正区间、来源范围与边界，不进行 fps、源时间、作品时间或成片时间换算。帧坐标必须是整数。选窗的范围证据必须属于对应源范围；`observed` 必须有提供的 `media_observation` 来源，计划不能转成观察事实。证据声明仍须由人或外部观察者负责。

`playback` 使用 `normal`、`speed_intent`（正的 factor 和理由）或 `freeze_intent`（明确保留事件的 anchor_event_id 和理由）。动作保持不自动转成定格。脚本不输出变速后的长度、定格保持时长或权威排时。每个实例有一个 `time_requests` 记录，要求 M7 完成时间映射。

`boundaries` 同时声明：

- `execution_stage`：`model_internal / post_edit / no_cut`。
- `continuity_strategy`：`continuous_action / match_cut / montage / ellipsis / same_shot_continuation`。
- 出入实例、出入镜头、显式事件、理由、来源，以及只读连续性 `policy_id`。

每个装配相邻实例之间恰有一个边界。一个多镜源实例内部的相邻镜头必须有明确 `model_internal` 切镜；这允许一次生成中存在多次切镜。同镜跨任务的接缝可为 `post_edit + same_shot_continuation`，不会因此新增镜头。内部切镜同一实例的两端必须引用明确 `cut`；跨实例边界不能伪称同一模型请求内切镜。连续性政策的 ID、边界 ID 和镜头端点必须一致，`pending` 不通过正式提案；M9 不能授予状态变化许可。本版 Policy 投影没有独立的策略授权字段，脚本仅核对政策的 ID、端点与批准状态；该 continuity_strategy 是否真正符合不变量、允许变化和原批准含义，仍须 M8/Agent 审阅，不能从 ID 匹配推出语义已获批准。

本版将“每个镜头在一个生成源内出现一次”作为 `shot_ids` 的明确表示范围。若同一视觉镜头在后期多次出现，用不同 segment 实例复用来源；不要在同一 `shot_ids` 列表重复 ID。完整语义与源片范围仍需专业复验。

### M9.3：GenerationPlan

`tasks` 独立声明任务 ID、`output_source_id`、能力 profile、模式意图、按源内顺序排列的镜头、M7 时间请求、完整任务上下文、入口/出口状态 ID 及素材 ID。任务数与镜头数没有一对一约束；内切可以在同一任务中，同镜也可以分给不同任务。

`context` 必须分别有主体、参考权限、场景、初态、动作、摄影、声音和末态的非空文字。脚本只检查字段存在，不证明“承接上一段”等文字已足够独立执行。`entry_state_ids / exit_state_ids` 引用 M8/external 提供的对应镜头与边缘状态；这里的 initial/final 表示**该任务在该镜头内的边缘**，不强迫同镜分段的每个任务都到达整镜初末帧。状态的实际内容与跨任务兼容性由 M8/Agent 审阅。

`coverage` 逐条关联任务与采用实例。`coverage_kind` 的 `full / partial` 表示所承担镜头内容的范围；每一行仍覆盖该选中 segment 声明的全部阶段。`candidate_overlap` 只能是未选候选；选择候选后要明确改为 full/partial/intentional_repeat。每个待生成 segment 恰好有一个 `selected: true` 分配；它的 `source_id` 必须等于任务 `output_source_id`。同镜分担通常通过多个 segment 和不同 output source 表达。候选不自动进入成片。

`reused_segment_ids` 明确登记已观察、直接复用的源片实例，它们不需要重新生成，也不能同时拥有选中生成分配。纯既有素材剪辑可以只调用 M9.2；也可调用 M9.3 显式交付零生成任务，此时所有 segment 都须登记为已观察复用，四个任务相关数组及能力/时间记录可以为空。

能力 profile 要保留 `backend / workflow / status / supported_modes / duration_limit / max_shots / supports_same_shot_split / source_refs`。正式脚本提案只接受 `status: known`；缺少 profile、unknown 能力或未知引用返回失败。技能仍可交付带“能力待核实、不可执行”标记的自然语言候选拆分；这种候选不应伪装为脚本已经接受的正式任务。示例里的能力是清楚标记的虚构测试夹具，不是 H3 真实能力证明，更不是固定 15 秒规则。

任务时长通过 `time_request_id` 引用 M7/external 的 `TimeRecord`。只比较同单位时长与给定能力上限；不换算或生成权威排时。待生成选窗还必须已有同单位的 `generation_local` 坐标，且不越过该任务的 M7 时长。否则回 M7 先给出映射。`m7_requests` 与 `m11_handoffs` 恰好覆盖每个任务；M11 交接只保留镜头顺序和模式意图，不包含最终 Label、H3 JSON 字段或后端参数。

## 3. 请求、提案与父接受

请求字段为 `kind / contract_version / work_id / base_version / request_id / target / sources / inputs`。提案保留相同工作、基版本与来源，增加 `proposal_id / module_id / source_request_id / context / changes / issues`。`context` 必须逐值等于**实际原请求**的 `inputs`，`sources` 也须完全相同。没有 `--request` 的自证提案不提供检查入口。

三个分区分别由 M9.1/2/3 独占写入；子模块无法添加自己的 `changes` 之外的字段。`issues` 可以记录未解决事项，但非空 issues 不会通过正式提案，错误带 `owner` 返还相应责任方。技术重试使用原始内容与原 ID；创意修订使用新 request/proposal ID 和当前 parent `base_version`。

`accept` 原子验证整批：实际请求集、来源、工作和基版本、分区独占、每个提案、只读兄弟投影与候选父内容。失败不输出半接受 state，不改输入文件。仅一个模块也可独立接受成为部分草稿；兄弟分区尚未存在时，其兼容外部输入仍可使用。父已有或同批新建对应分区时，投影值必须与该分区完全一致。

相同已接受 proposal/request 的摘要重复提交时，返回当前 state 且 `idempotent: true`，不增加版本。重用 ID 但改变内容、同一 request 授权不同提案、混合旧重试和新修订、旧基版本、同批双写或来源冲突均拒绝。相同来源 ID 和版本的内容不可变化；版本改变时保留旧 receipt，相关消费者变 stale。receipt 摘要用于识别内容变化和错误复用，不是来源真实性的数字签名。

接受只替换提案独占的原始分区，不“修复”其创作决定；版本加一并追加 receipt。父对象保存 `content / contexts / sources / receipts / consumers / stale_modules`。未同步更新的已有依赖分区保留旧内容并标 stale，不能将它们视为新版本已复验的结果。与候选父内容冲突的新提案本次不接受。

## 4. 影响检查

每次成功接受根据实际输入投影、实际使用的证据和兄弟分区生成 `read_paths`。M9.2 读取 `ShotMap`，M9.3 读取 `ShotMap / EditGraph`；其他来源按实际引用记录。注册表列出一般依赖，receipt 记录本次实际读取范围。M7/M8/M11/M12 等外部消费者只能在实际读取后登记对应 `consumer_id / read_paths / status`，不能从“可能受影响”伪造读取记录。

`impact` 比较 before/after 快照，用 JSON Pointer 前缀重叠判断；数组作为已声明的集合读取路径处理，不猜测插入后的稳定索引。保留先前 stale，比较前后读取集合的并集，避免删除读取记录就掩盖本次失效。显示标题变化只有读取 `/display` 的消费者才受影响；不全局重验所有模块。影响分析本身不更新或执行消费者。

对父草稿的真实修改使用新请求和 `accept`；`impact` 可以比较尚未接受的拟议快照，因此只做快照结构检查，不要求 after 已取得新 receipt。`accept` 则核对已接受分区、上下文摘要和实际依赖记录，不允许用手改 state 绕过正式修订。

## 5. 可执行示例

从本技能根目录运行：

```bash
python scripts/m9_contract.py route assets/request-standalone-m9-1.json
python scripts/m9_contract.py check assets/proposal-standalone-m9-1.json --request assets/request-standalone-m9-1.json
python scripts/m9_contract.py check assets/proposal-standalone-m9-2.json --request assets/request-standalone-m9-2.json
python scripts/m9_contract.py check assets/proposal-standalone-m9-3.json --request assets/request-standalone-m9-3.json
python scripts/m9_contract.py accept assets/state-empty.json assets/proposal-batch.json --requests assets/requests.json
python scripts/m9_contract.py impact --before assets/impact-before.json --after assets/impact-after.json
```

每个独立请求都有自己的兼容投影，无需兄弟脚本。`requests.json / proposal-batch.json` 把相同三组组成原子批。示例有两镜、四画格、三阶段、三个剪辑实例和三个生成任务：中间任务包含两镜；转体阶段跨真实切点；两镜都跨任务；pan→track 是同镜摄影事件；后期同镜接缝与模型内切镜分别表示。

这些都是 D 类工程夹具：规划数字、能力上限、许可与状态不是案例实测或官方能力证据。真实项目必须替换资料与来源。`assets/impact-before.json` 是示例接受后的草稿；after 只改显示标题，展示未读取显示字段的消费者不失效。测试另行覆盖关键依赖变更和保留旧 stale。

包外开发验证命令（从仓库根）：

```bash
python -m unittest discover -s docs/h3skill/tests/m9 -p 'test_*.py'
python docs/h3skill/tests/m9_portability.py
```

便携性验证把单个技能包复制到临时目录，用隔离 Python、空 PATH 和非仓库 cwd 执行帮助、三路独立 route/check/accept、组合接受、幂等和影响检查；不调用或依赖 M1—M8。
