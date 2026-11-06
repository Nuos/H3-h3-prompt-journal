# M10 公共合同与命令

## 目录

1. 版本、作用域与结果范围
2. 四个独立输入与输出分区
3. 引用、身份、可见性与状态许可
4. 原始请求、提案与父接受
5. 真实依赖、失效与修订
6. 命令与最小使用示例

## 1. 版本、作用域与结果范围

本包采用 `contract_version: "1.0.0"`、`route_version: "1.0.0"`，实现冻结方案 v0.1.2 的 M10 职责。机读字段以 [contracts.json](contracts.json) 为准；节点、读写权、资源与返回点见 [module-registry.json](module-registry.json)。这些对象属于本项目的 D 类工程合同，不是新增的 H3 输入字段。

父对象 `M10State` 的 `object_type` 是 `LookPlan`，`status` 始终为 `draft`。`route` 的 `ready: true` 只表示声明输入满足入口条件，`invocation_status` 仍为 `not_invoked`。`check / accept` 返回 `passed_with_unverified`，表示机器可检查的显式关系通过；它们不判定自然语言是否完整、不验证来源陈述真实性，也不证明灯光、材质、可见性或连续性已经在实际视频中实现。返回值保留 `limitations` 与 `not_run`。

运行依赖 Python 3.10+ 标准库。复制整个技能目录即可运行；脚本只读取指定 JSON 与包内合同／路由文件，只把结果写到 stdout，不覆写输入、不联网、不调用其他模块、不生成媒体。包内 `_schema.py` 仅实现本合同采用的 JSON Schema 词汇，未知关键词拒绝；不是通用 JSON Schema 引擎。

每个来源记录有 `kind / locator / version / excerpt`。投影使用 `owner / source_id / source_version / values`。来源版本是本适配合同的非空字符串，不应直接假定与上游原生对象的整数版本字段互换。兼容用户资料和外部工具输出可以直接提供投影，无须先运行 M1—M9。

`scope_context.values.scopes` 定义本次可用的 `scope_id / level / parent_scope_id`：`level` 为 `work / scene / shot`；已声明的父节点必须存在且层级更广。单镜独立调用允许一条 `shot` 层级的局部根，其 `parent_scope_id: null` 表示本次资料没有声明更广继承，不代表该镜已取得全片规则。M10 读取这些标识，不重写 M3 的场景或 M9 的镜头结构。

## 2. 四个独立输入与输出分区

所有子模块都需要 `brief` 与 `scope_context`。只传与本次任务有关的最小投影；可选字段一旦携带具体主张，必须满足其条件性依赖。

| 子模块 | 额外必需投影 | 可选投影 | 独占输出 |
|---|---|---|---|
| M10.1 | 无 | `reference_context` | `StyleHierarchy.layers` |
| M10.2 | `scene_context` | `reference_context / style_context / visibility_context` | `LightingPlan.setups / visibility_checks` |
| M10.3 | 无 | `reference_context / style_context / lighting_context / identity_context` | `ColorPlan.grades` |
| M10.4 | `identity_context` | `reference_context / style_context / lighting_context / color_context / visibility_context / continuity_context / event_context` | `MaterialEffectPlan.materials / effects / visibility_checks / continuity_handoffs` |

### M10.1：层级与继承

每个被本次 `scope_context` 选中的作用域对应一个 `layers` 条目。层级关系必须与该投影一致，不能环状继承，不能漏掉引用的父层。`style` 只包含 `rendering / visual_language / image_texture`；根层经解析后须完整具备三个字段，子层允许 `{}` 以明确沿用父层。

改变继承值时，`override_keys` 必须恰好列出实际改变的键，`override_reason` 必须非空；没有覆盖时使用空键列表和 `null` 理由。脚本比较明确提供的字符串，不推断两句不同文字是否语义等价。不在此分区写入光源、调色、动作或角色身份。

### M10.2：光源与照明

`setups` 为一个作用域的一组光源。每个光源记录 `kind / location / direction / quality / color_description / temperature_kelvin / intensity_relation` 及证据；`temperature_kelvin` 可为 `null`，表示未声明数值，不能自动补成某个摄影常数。若提供数字则须为正有限数，不能把布尔值当作数值。

照明方案须有自身或祖先作用域的 `scene_context.conditions` 支撑。每个作用域只能有一套当前方案；局部方案通过 `parent_setup_id` 指向最近的已声明祖先方案，实质改变光源内容时写明覆盖理由。只改变证据引用不构成新的视觉覆盖。

`visibility_checks` 覆盖本次显式提供的 M5 可见性要求；没有提供对应要求时不虚构检查记录。检查的 `preserved_by_design` 表示计划声明，实际画面依然未验证；`conflict / unverified` 不能通过本次正式提案。

### M10.3：色彩与调色

`grades` 分开记录 `palette / temperature_bias / contrast / saturation / exposure_intent`，并通过 `parent_grade_id` 与覆盖理由处理局部差异。现场暖光可以与冷中性整体调色并存，两个字段不互相覆盖，也不需要数值相等。冷色、低饱和和固定曝光偏好都不是全局默认。

`identity_change` 必须为 `false`。当输入给出身份投影时，`protected_identity_ids` 必须列出其作用域内的全部对应身份，不能漏掉、添加未知身份或以调色为由改变固有属性。未提供身份资料的独立调色提案可以使用空列表，但不能据此声称已完成具体角色身份审查。机器检查字段声明；实际文字是否偷换发色、服装或造型，仍需 Agent 审阅。

### M10.4：材质与效果

`materials` 与 `effects` 至少有一个非空。材质条目引用 `identity_context` 内的 `entity_id / surface_id`；`base_material` 必须保持提供的基础材质。`appearance` 描述表面读感，不是身份重设计通道。

`conditions` 仅接受已声明的表面属性：`wetness / roughness / wear / temperature / cleanliness / opacity`。每项必须有可核对的基准值；与基准相同则 `permission_id: null`。不同值既须属于 M2／外部资产投影允许变化的属性，也须有 M8／外部状态许可，且许可的实体、表面、属性、值与作用域全部匹配。湿发许可不能转成改发色或发型的许可。

每个获准变化精确对应一条 `continuity_handoffs`，供 M8 接受视觉状态要求；M10 不写 `StateLedger`，不自动增加状态转换。未使用表面状态变化时不需要 `continuity_context`。

效果使用 `constant` 或 `event` 触发；后者须引用 `event_context` 的实际事件 ID。M10 不在效果条目里编造秒数、动作或切点。`blocks_key` 返回 M5 修订，`managed` 必须有明确 `mitigation`；字符串存在不能证明该措施在画面中有效。

## 3. 引用、身份、可见性与状态许可

`reference_uses` 必须明确资产、用途、作用域与实体目标。本合同的用途为 `style / lighting / color / material / effects`。许可只允许身份的图片不能提供风格、光线、调色或材质；其他用途同样不能凭输入模式或 Label 自动升级。

`reference_context.assets` 记录 `allowed_uses / forbidden_uses / scope_ids / target_ids`。作用域许可可覆盖其已声明的后代作用域，但不能反向扩展。用途同时出现在允许与禁止列表时，返回 M2 解决冲突。

**空 `target_ids` 表示未绑定具体实体的作用域级参考，不是任意实体通配符。** 作用域级使用需要作用域级许可；限制于特定实体的许可不能扩展成整镜／整场景使用。实体绑定的使用则须逐项包含在许可目标列表内。材质与效果已有具体目标时，`reference_uses.target_ids` 必须与该条目实际目标完全相同。

引用检查也覆盖只读 `style_context / lighting_context / color_context`。携带 `reference_uses` 的投影必须同时带有所用资产的最小许可闭包；不能把冲突的身份参考藏在“上游已定风格”里跳过检查。无引用的最小输入仍不需要 `reference_context`，也不要求执行 M2。投影内的作用域、重复 ID、已声明检查和来源同样要自洽。

可见性要求用 ID 指向已提供的目标和作用域；输出逐项覆盖，不能把单镜检查伪装成全片检查。只读照明投影中的可见性记录同样必须落在已知且被照明方案覆盖的作用域。没有实际媒体时，所有这些记录均是计划约束，不能转成 M12 媒体观察。

## 4. 原始请求、提案与父接受

请求包含 `kind / contract_version / work_id / base_version / request_id / target / sources / inputs`。子提案包含相同工作和基版本，并增加 `proposal_id / module_id / source_request_id / context / changes / issues`。提案 `context` 必须逐值等于实际原请求的 `inputs`，`sources` 也必须完全相同。`check` 必须传 `--request`；不给自证提案单独通过的入口。

四个分区分别由四个子模块独占写入，`changes` 不允许越权添加别的分区、H3 参数或 M8 状态。未解决的 `issues` 会返回带 `owner` 的失败记录。字段或来源未知时可保留在文字候选与问题记录中，不应填占位文字伪装为正式提案；本脚本本身不自动识别所有自然语言占位词。

父 `accept` 原子检查一项或一批提案：真实原请求集、工作与基版本、提案 ID、来源、独占分区、条件性依赖及候选兄弟投影。既有或同批形成的兄弟分区存在时，所读取投影中的每一行必须与候选分区对应行一致；允许提供有闭包的最小行子集。不存在对应兄弟分区时，可以直接使用有来源的兼容外部投影。

只接受一个子模块时，形成部分 `LookPlan` 草稿，不要求补齐其余三个分区。失败不输出半接受 state，也不修改原文件。接受过程仅替换该子模块所属分区，不能自动“修复”其创作决定。

成功接受后版本加一，并保留 `contexts / sources / receipts / consumers / stale_modules`。Receipt 保存原请求、提案、输出、上下文及实际来源的摘要。相同已接受 ID 和完整内容重试返回当前 state，`idempotent: true`，不增加版本。改变内容却重用 ID、复用已接受 request 授权新 proposal、混合旧重试与新修订、旧基版本、同批双写和来源冲突均拒绝。

同一来源 ID 和版本的内容不得改变；来源变更使用新版本。正式接受还检查现有分区与上下文摘要、来源最新接受记录、实际读取路径和 stale 状态，不能靠手改输出或删依赖记录让旧结果变成新通过。摘要用于内容一致性检查，不是来源真实性的数字签名。

## 5. 真实依赖、失效与修订

每个被接受子模块只登记本次实际读取的 `read_paths`：它的输入投影、实际引用的来源，以及真正提供的兄弟快照。没有读 `style_context` 的最小调色调用不会仅因风格分区存在而获得依赖。

变更按 JSON Pointer 前缀交集判断；数组按已声明的集合路径处理，不猜测插入后的稳定索引。外部 M5／M8／M11／M12 等消费者只有实际读取后才能登记读取路径，路由表不构成执行证据。

失效沿已登记的真实依赖传递。例如材质只读取照明，照明读取风格；风格修订后照明变 stale，材质也会沿该实际依赖变 stale。新材质提案即使重新取得风格快照，也不能把尚未复验的照明或调色当成 current。须先重验这些依赖，或在同一原子批中提交相容的新提案；否则 `accept` 拒绝该批。

`impact` 比较同一作品的 before/after，可用于尚未接受的拟议快照，因此只要求快照结构有效，不要求 after 已生成新 receipt。它合并前后读取集合并保留此前 stale，防止删除依赖记录掩盖失效；只改显示标题时，不使未读取 `/display` 的消费者失效。影响分析不自行复验、修订或调用消费者。

## 6. 命令与最小使用示例

从技能目录运行：

```bash
python scripts/m10_contract.py route assets/request-minimal-m10-1.json
python scripts/m10_contract.py check assets/proposal-minimal-m10-1.json --request assets/request-minimal-m10-1.json
python scripts/m10_contract.py check assets/proposal-minimal-m10-2.json --request assets/request-minimal-m10-2.json
python scripts/m10_contract.py check assets/proposal-minimal-m10-3.json --request assets/request-minimal-m10-3.json
python scripts/m10_contract.py check assets/proposal-minimal-m10-4.json --request assets/request-minimal-m10-4.json
python scripts/m10_contract.py accept assets/state-empty.json assets/proposal-minimal-m10-4.json --requests assets/request-minimal-m10-4.json
python scripts/m10_contract.py accept assets/state-empty.json assets/proposal-batch.json --requests assets/requests.json
python scripts/m10_contract.py impact --before assets/impact-before.json --after assets/impact-after.json
```

`request-minimal-* / proposal-minimal-*` 只包含各自必需投影，示范四个子模块无需兄弟快照独立运行。`request-standalone-* / proposal-standalone-*` 提供完整且自足的外部投影，示范层级覆盖、暖光与冷中性调色并存、湿发许可、受控背景效果及跨模块交接；它们的四组组合在 `requests.json / proposal-batch.json` 中。

这些人物、环境、许可和数字均为 D 类工程夹具，不能当作源案例实测、真实用户授权、物理摄影结论或 H3 能力依据。`impact-before/after` 仅示范显示标题修改不使视觉内容依赖失效；实际项目必须替换资料、来源与目标，并另行完成语义和媒体检查。
