# M12 公共合同与运行命令

**核心摘要：** 四个子模块分别接收公开最小输入，形成范围计划、审计台账、独立观察和变更复验记录；父模块对照真实原请求原子接受，保留历史。

**关键结论：** 记录合同正确不证明外部资料真实、电影语义正确或媒体质量合格。脚本与 Agent 的职责分别登记。

**关键词：** M12Request、M12Proposal、M12State、公开投影、版本、历史、幂等。

**目录导航：** 1. 环境；2. 四路输入；3. 来源与版本；4. 独立与组合；5. 结果含义；6. 命令和示例。

## 1. 环境与版本

运行依赖为 Python 3.10+ 标准库。复制整个 `h3-audit-repair/` 目录即可使用本包声明的记录工具与离线规则；不需要安装其他核心模块，也不导入它们的私有脚本。

技能版本 `0.1.0`、公开合同版本 `1.0.0` 与路由版本 `1.0.0` 分别管理。机读结构和严格字段见 `contracts.json`；模块树与责任见 `module-registry.json`。这些对象均属于本项目内部合同，不新增 H3 原生输入字段。

脚本读取显式 JSON 并将 JSON 输出到 stdout，不写回输入、不联网、不解码媒体、不调用其他模块或执行生成。调用方决定是否将返回状态保存为新文件；不能用 shell 重定向覆盖正在读取的输入文件。

## 2. 四路最小输入

| 入口 | 必需资料的语义 | 返回对象 | 资料不足时 |
| --- | --- | --- | --- |
| M12.1 | 用户范围、有效要求、受检对象、检查方法与证据要求 | AuditPlan | 保留适用要求及缺口，不虚构已执行检查 |
| M12.2 | 兼容检查计划、当前对象版本、实际检查结果与支持证据 | AuditLedger | 适用条件保持未验证，具体已证实违例保留失败 |
| M12.3 | 实际媒体与计划身份、观察者／方法／时间域／覆盖、原始观察或测量 | MediaObservationLedger | 缺真实观察时说明缺项；不得把提示词改写成观察 |
| M12.4 | 具体问题、归因证据、版本化变化、已知依赖与复验资料 | ChangeSet | 保留候选责任、待查依赖和未完成复验 |

完整结构以机读合同及可执行示例为准。无关输入不强制补齐；该职责实际需要的信息不能用空字符串或任意默认值冒充已知。

### 2.1 请求信封与引用

请求包含 `kind: M12Request`、`contract_version`、`route_version`、`work_id`、非负整数 `base_version`、`request_id`、`target` 和 `inputs`。目标为 `M12.1` 至 `M12.4` 之一，两个版本均固定 `1.0.0`。稳定 ID 使用 ASCII 字母／数字／下划线／连字符，首字符为字母或数字，最长 128 字符。

每个版本引用 `Ref` 包含 `id / version / digest / owner / kind`；`version` 是非空字符串，`digest` 是小写 SHA-256，`owner` 为 `M1`—`M12` 或 `external`。同一 ID 的责任和类型保持稳定，同一 ID＋版本不能对应不同摘要。Ref 是明确的身份声明；本程序不会读取其代表的外部文件来证明声明真实。

### 2.2 M12.1 的检查计划

`inputs` 包含 `scope_id / scope_version / plan_ref / scope_sources / gates / requirement_ids / checks`。每个检查包含 `id / requirement_id / gate / expected / method / targets / channels / time_window_ms / coverage`。所有列出的要求和 Gate 必须有检查，所有列出的检查都是本范围的必需项。

G0—G2 使用 `coverage: document`、空通道和 `time_window_ms: null`；这表示检查文档和声明，文档中仍可含时间参数。G3 使用 `generated_media` 类型目标，G4 使用 `assembled_media` 类型目标，二者均要求至少一个视频／音频通道、整数毫秒窗口和 `coverage: full_window`。

同一 scope 的接受和复验采用保守范围规则：保留旧 Gate、要求 ID、检查含义、目标身份、方法、通道和覆盖，可扩展范围和推进对象版本；不原位削弱原检查。若用户确实改变任务范围，应保留原 scope／未解决项和授权记录，建立明确的新范围；不能把新的较小范围宣称为旧任务完成。

### 2.3 M12.2 的证据汇总

`inputs` 包含 `plan / current_refs / results / evidence / observations`。`plan` 可由兼容外部资料直接提供；`current_refs` 明确本次有效对象版本。每项 result 给出 `check_id / result / evidence_ids / reason`，缺少支持的声明不能生成有效通过。

每项证据包含 `id / kind / origin / source_ref / check_ids / locator / content`。kind 为 `document`、`media_observation`、`applicability` 或 `causal_analysis`；origin 为 `synthetic`、`user_report` 或 `declared_actual`。媒体证据额外通过 `observation_id` 关联独立观察。证据来源必须对应其检查实际使用的对象和版本。

`not_applicable` 需要 `applicability` 中明确 `rule / basis_ref / no_downstream_dependents: true`，还需匹配的 applicability 证据；一句“没有提供文件”不能在语义审阅中充当该依据。媒体通过要求 `declared_actual` 的媒体证据和观察共同成立；这个词仅表示提供方的实际观察声明，脚本不会认证其真实性。

### 2.4 M12.3 的观察登记

`inputs.observations` 至少包含一条真实提供的观察或明确的合成夹具。每条包括媒体及计划 Ref、观察者、带时区的 ISO-8601 `observed_at`、方法、`time_domain: media_ms`、通道、覆盖、来源性质和具体事实。没有观察时不要制造一条空白或假观察；在 M12.2 对原检查返回未验证，并列出待取得的资料。

覆盖以整数毫秒记录，`duration_ms` 为该媒体时长，`windows_ms` 为有序不重叠的半开区间 `[start, end)`；模式为 `full / intervals / sampled`。full 明确覆盖 `[0, duration_ms)`。本版只接收被检查媒体自身的局部毫秒；源素材、作品、生成或剪辑时间不同于该文件时间时，先取得 M7／外部映射并作为来源保留，不让脚本猜换算。

`facts` 中每项包含 `check_id / expected / observed / assessment / location / time_window_ms`；assessment 为 `satisfies / violates / inconclusive`。事实窗口须在实际观察覆盖内。用于认定某项失败的违例窗口还必须位于该检查窗口内，不能把片尾的偏差归到片头检查。抽样事实可以登记，但本版 G3／G4 的正式通过要求完整覆盖当前检查窗口；不能把 sampled 自动升级为 full_window。

### 2.5 M12.4 的修复与复验

`inputs` 包含原始 `audit`、`issues`、`changes`、`dependencies` 和 `retests`；audit 使用与 M12.2 相同的公开输入，程序可重新核对原问题依据。每个复验附完整新 audit，保留原问题的要求和覆盖，不能只传一个“已修复”状态。

依赖图登记版本化 nodes、`upstream / downstream` 方向的 edges，以及图在当前范围是否完整。变更影响沿真实边计算；图不完整时返回已知影响和局限。修改请求、已接受的专业修订、复验结果分别处理，所有结果均不自动触发外部执行。

每个 issue 包含 `id / check_id / object_ref / location / expected / actual / evidence_ids / owner / attribution_basis / causal_evidence_ids / requested_action`。检查 ID、期望和对象身份须对应原检查；owner 可为 `M1`—`M12`、`external` 或 `unresolved`。症状证据与因果证据分开，缺少当前版本的归因依据时，返回责任未决。

每个 change 包含 `id / issue_ids / owner / before / after / reason / status`。before／after 是同一语义对象的不同版本，owner 必须是对象原责任方；status 为 `proposed` 或 `reported_applied`。前者只计算建议影响，后者表示提供方报告已实施的变化并使相关旧结论失效；两者都不意味着本程序实际修改了专业对象。

`dependencies` 使用 `nodes / edges / complete`；每条边指向依赖上游内容的下游对象，不按模块编号推定先后。`retests` 中每项为 `issue_id / audit`。复验不仅核对目标项，还保留原范围、当前版本、证据新鲜度和依赖调查结果。`closed_by_retest` 仅表示该条问题在所声明证据下满足关闭条件，不认证整个任务或证据提供方。

依赖节点和 before 必须与所声明／已接受的当前对象版本一致。直接改动的对象及需要更新的派生文档推进版本；非直接改动的下游媒体可在新计划下重新观察，保持相同 media_ref，但必须提供时间更新、覆盖匹配的新实际观察声明。旧观察仍按当时计划保留，不能改名复用来冒充复验。

## 3. 保留来源与版本

稳定对象 ID 标识同一对象，版本与内容摘要标识某次快照；不要改变内容后仍使用原版本。来源记录与目标引用均保留定位和证据性质，避免把计划、作者报告、实际运行、媒体观察和合成材料混为一类。

接受外部投影时保留原来源、原对象 ID、字段含义和版本。脚本可检查声明之间是否自洽，不能仅凭一个来源标签、内容摘要或 `actual` 声明证明外部事件确实发生。Agent 必须如实记录自己实际取得的材料与执行范围。

旧结果与当前对象不一致时保留旧记录并标明当前有效性；不能用旧媒体观察为新生成片背书。抽样、部分通道和局部时间窗必须满足该检查的原始覆盖要求，不能在汇总时自动扩大。

## 4. 独立调用与父接受

M12.2 可以直接接收兼容外部检查计划，不要求先运行 M12.1；M12.3 可以独立登记实际观察，不要求先取得全部创作模块；M12.4 可以接收兼容问题与依赖资料，直接形成局部路由。独立意味着数据来源可替代，仍需满足公开合同。

子提案不是任意改写记录的第二入口。核对和父接受须取得真实原请求，重新核对确定性结果、工作标识、版本、责任与来源。接受失败不能留下半份状态。

重复接受同一请求及相同结果应保持幂等；新要求、不同事实或修订属于新请求。历史检查与观察不可变，新结果另存；当前失效状态不抹去原失败或通过记录。专业字段的修订始终通过原责任模块。

范围扩展后，新的审计不能退回较小的旧 scope；修复记录仍可引用原始历史 audit 来说明问题来源。当前视图以 `scope_current_validity` 单独说明原审计范围是否已经过时，不把旧范围的通过当作扩大后范围的通过。

## 5. 分开理解结果

| 层级 | 含义 |
| --- | --- |
| 路由可进入 | 显式目标与输入通过本合同的确定性检查，不表示外部语义检查或观察已经执行 |
| 合同／程序通过 | 显式记录满足本实现的类型、版本、引用及关系检查 |
| 范围内审计结果 | 有对应证据的 pass／fail／unverified／not_applicable |
| 当前有效性 | 旧结果在依赖变化后可能 stale，原结论保留为历史 |
| 实际运行或媒体验收 | 需要真正的执行、观察或测量证据，不能由上述状态推导 |

严格 JSON 应拒绝重复键、非有限数、未支持版本和错误字段类型。错误输入返回结构化错误；专业缺证据应尽可能保留可交付的局部结果，而不是冒充已验证。

## 6. 命令与示例

在技能目录先运行：

```bash
python scripts/m12_contract.py --help
```

分发示例均明确为 synthetic 工程材料；媒体观察示例不会据此通过 G3。四个请求共享 `WORK_SYNTHETIC` 和基版本 0，可分别使用，也可组成一次原子接受。

| 示例文件 | 独立入口 | 演示内容 |
| --- | --- | --- |
| `assets/scope-request.json` | M12.1 | 单项 G2 范围与检查计划 |
| `assets/audit-request.json` | M12.2 | 具有文档声明证据的范围内失败 |
| `assets/observation-request.json` | M12.3 | 明确标记合成性质的观察合同，不能认证媒体 |
| `assets/repair-request.json` | M12.4 | 文档问题、归因声明、建议变更和已知依赖；尚未实施或复验 |
| `assets/empty-state.json` | 父 M12 | 初始版本 0、空记录和空接受历史 |

以下命令使用 M12.2 演示直接调用；将请求路径换成表中另一个请求即可使用对应入口。输出保存在技能目录旁的 `m12-demo-output/`：

```bash
mkdir -p ../m12-demo-output
python scripts/m12_contract.py route assets/audit-request.json
python scripts/m12_contract.py propose assets/audit-request.json > ../m12-demo-output/audit-proposal.json
python scripts/m12_contract.py check ../m12-demo-output/audit-proposal.json --request assets/audit-request.json
```

`check` 必须同时取得原请求，不以提案内部自报的来源替代原请求。父接受使用一一对应的原请求数组、提案数组和当前 state：

```bash
python - <<'PY'
import json
from pathlib import Path
out = Path('../m12-demo-output')
for source, destination in [
    (Path('assets/audit-request.json'), out / 'requests.json'),
    (out / 'audit-proposal.json', out / 'proposals.json'),
]:
    value = json.loads(source.read_text(encoding='utf-8'))
    destination.write_text(json.dumps([value], ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
PY
python scripts/m12_contract.py accept ../m12-demo-output/proposals.json --requests ../m12-demo-output/requests.json --state assets/empty-state.json > ../m12-demo-output/accepted.json
```

成功输出含 `status / idempotent / state / current_view / verification_boundary`。只有其中 `state` 是下一次接受的输入状态，不能把整个成功响应当作 state。调用方将它另存为新文件后使用；同一提案与原请求完整重试返回幂等结果，不增加版本。新请求的 `base_version` 必须等于当前状态版本，使用新 request ID。

一个原子批次至多包含每个子模块的一项提案；所有提案都须通过核对，工作、基版本及新声明的当前对象版本彼此一致。任一项失败都不返回半份新状态。接口成功退出码为 0，合同错误退出码为 2 并输出结构化 `errors`；`fail` 审计结论本身是有效业务结果，不是程序崩溃。

自然语言审计可复制 `assets/audit-report-template.md`，将每条结论关联到实际证据；该模板不能直接作为 H3 提示词。
