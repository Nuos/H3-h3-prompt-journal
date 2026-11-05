# M1 公开合同与调用指南

## 目录导航

1. 版本与输入输出类型
2. 最小独立请求
3. WorkBrief 字段责任
4. 子提案与父接受
5. 脚本结果与状态
6. 变更影响和修复
7. 来源与按需读取

## 1. 版本与输入输出类型

本包版本 `0.1.0`，M1 合同版本 `1.0.0`。`contracts.json` 是 JSON Schema Draft 2020-12 结构契约及字段语义说明，`module-registry.json` 是四个职责节点与路由登记；`m1_contract.py` 对命名合同执行显式结构与跨字段校验，不是通用 JSON Schema 解释器。动态引用、权限、基版本和组合冲突以显式校验及对应测试为准。

| `kind` | 含义 | 谁形成 |
|---|---|---|
| `M1Request` | 单次请求，包含本节点所需只读输入 | 用户入口/当前 Agent/兼容调用者 |
| `M1Proposal` | 一个子模块负责分区的候选变更 | M1.1 / M1.2 / M1.3 |
| `M1ProposalBatch` | 对同一基版本的多个提案，接受时作为一个整体核对 | M1 调用者收集；不是第二个语义决定者 |
| `WorkBrief` | M1 接受形成的版本化作品意图 | 唯一权威接受路径 M1 |
| `M1ToolResult` | 某次确定性命令的报告/结果封装 | 本包脚本；不是 H3 模型正文 |

只支持已登记版本。破坏性修改需要新合同和显式迁移；不静默把旧输入解释为新语义。M1 合同不冻结未来十二模块的全部字段，仅提供本模块的外部接口。

## 2. 最小独立请求

请求公共字段：`kind`、`contract_version`、`request_id`、`target`、`work_id`、`base_version`、`sources`、`inputs`。所有 ID 为 1–64 个 ASCII 字母、数字、点、下划线、连字符，首字符为字母。`base_version` 为非负整数。

| 目标 | 必需的 `inputs` 键 | 可以独立完成什么 |
|---|---|---|
| M1 | `work_type`、`creative_request` | 开始完整意图工作，逐步构造子模块需要的投影 |
| M1.1 | `work_type`、`creative_request` | 意图、约束和必保事项提案 |
| M1.2 | `work_type`、`intent_context`、`paragraph_material` | 段落作用与信息关系提案 |
| M1.3 | `work_type`、`intent_context`、`emotion_material` | 情绪能量与母题提案 |

`work_type` 为 `drama` / `mv` / `hybrid`；其他必需业务输入是来源可追溯的文字投影。可选 `delivery_use` 和 `notes` 只提供当前任务有关的信息。不可借 `inputs` 注入未声明的整份全局计划。

每个来源保存 `kind`、`locator`、`version`、`excerpt`；使用稳定来源 ID 并由内容记录的 `source_refs` 引用。来源类别包括 `user_requirement`、`case_text`、`design_decision`、`external_input`、`official_document`、`hypothesis`。这些类别和冻结计划的 F/D/I/U 是两个不同维度：前者表示来源性质，后者表示证据/实现层次。不能把 `hypothesis` 称为实测。

可选 `requested_fields` 限定本次希望返回的分区；省略时要求目标节点的全部分区。使用它完成局部修订，避免让 M1.3 为了改能量而重做 M1.1。子模块不能申请其他节点拥有的字段。

对允许未知的语义文本使用：

```json
{"state": "unknown", "reason": "当前仅有案例文字，尚无实际音频或可信拍点。"}
```

缺少本节点的必需输入会返回具体缺项；显式 unknown 不转为事实或不适用。时间只接收有来源的请求值；需要真实测量时交 M6/M7。示例里的参数只属于示例任务。

## 3. WorkBrief 字段责任

顶层记录作品 ID、`version`、`owner_module: M1`、`status: draft`、`sources`、`content`、`issues`、`accepted_proposals` 和 `consumers`；`display` 字段也须存在，可为空对象，其中展示标题 `title` 可选。版本 0 的空简报允许作为接受起点，但不算完整结果。

| `content` 分区 | 负责子模块 | 主要字段与含义 |
|---|---|---|
| `intent` | M1.1 | `work_type`、`creative_goal`、`audience_takeaway`、`delivery_use`、`source_refs`；可选 `target_duration` |
| `constraints` | M1.1 | 以约束 ID 索引：原始约束文本、`must/should/may` 优先级、作品/段落作用域、来源 |
| `must_keep_events` | M1.1 | 以事项 ID 索引：必须保留的事件/原文要求及来源 |
| `paragraphs` | M1.2 | 以段落 ID 索引：次序、作用、进入/离开信息、必保事项归属、信息前序、来源；可选人物目标/表演重点 |
| `emotion_energy` | M1.3 | 以段落 ID 索引：起始/结束情绪、相对能量意图、来源 |
| `motifs` | M1.3 | 以母题 ID 索引：可识别描述、作用段落、发展/变奏意图、来源 |

`target_duration` 使用 `seconds`、`domain`、`basis`、`source_refs`。`domain` 明确区分 `final_work` 与 `generation_request`，`basis` 只能是 `requested`。它是用户/制作需求，不是后端允许值或实测音频时长。没有本次依据时省略或明确 unknown，不套用来源案例的数值。

`paragraphs.*.information_predecessors` 只表达信息关系和语义顺序，不代表秒数；`emotion_energy` 也不是声压、LUFS、BPM 或拍点测量。镜头、实际时间、空间、声音、资产和 H3 标签不属于本合同的写入分区。

空集合需要符合当前语义：没有母题要求可以明确交付空 `motifs` 并在审阅记录说明；遗漏要求不能用空集合蒙混通过。脚本无法知道未提供的原始要求，因此 Agent 仍须逐条回查来源。

## 4. 子提案与父接受

子提案包含 `proposal_id`、`module_id`、`work_id`、`base_version`、`source_request_id`、`sources`、`changes`、`issues`、`resolutions`，以及公共类型/合同版本字段。`changes` 只能包含该子模块负责的分区。

分区替换是明确的最小公开操作，不是 JSON 任意路径写入。修改某个分区时提交该分区完整的新值，保留未变项目；不得将遗漏旧项目当成隐含删除授权。需要变化的字段若归其他模块，则写问题/交接请求。

批次形状：

```json
{
  "kind": "M1ProposalBatch",
  "contract_version": "1.0.0",
  "proposals": []
}
```

上方仅说明外壳；实际批次必须包含非空的有效提案。同一批次针对同一 `WorkBrief` 基版本，任意分区只允许一份提案写入。父接受一次形成一个新版本；逐次接受时，后续提案需重新读取新的基版本，不能盲目改数字继续提交。

`issues` 保存问题 ID、代码、状态、文字、责任模块、字段、阻塞标记和来源。`resolutions` 只能解决当前子模块拥有的既存问题，需保留原因与来源。子模块不能自行消除用户、父模块、兄弟模块或外部模块拥有的阻塞问题。修复的真实语义正确性仍要单独审阅。

接受结果不覆盖输入。以下命令从技能目录运行，演示如何保存到一个新的任务目录：

```bash
mkdir -p /tmp/m1-example-task
python scripts/m1_contract.py accept assets/workbrief-empty.json assets/proposal-m1-1.json > /tmp/m1-example-task/acceptance.json
python - <<'PY'
import json
from pathlib import Path
task = Path('/tmp/m1-example-task')
result = json.loads((task / 'acceptance.json').read_text())
if result.get('outcome') != 'accepted':
    raise SystemExit('Proposal was not accepted; inspect diagnostics first.')
target = task / 'workbrief-v1.json'
with target.open('x', encoding='utf-8') as stream:
    json.dump(result['work_brief'], stream, ensure_ascii=False, indent=2)
    stream.write('\n')
PY
python scripts/m1_contract.py check /tmp/m1-example-task/workbrief-v1.json
```

例子路径只是临时演示；真实任务选择自己的新目录。`open('x')` 防止覆盖已有版本。仅 M1.1 的接受结果仍是部分 WorkBrief，其他分区及总体语义不因此完成。

## 5. 脚本结果与状态

四个命令都返回 `M1ToolResult` 封装。`accept` 成功时真正的新简报在 `work_brief` 中；不要把整个工具报告当 WorkBrief 传入下一次调用。

| 命令 | 额外返回 | 含义 |
|---|---|---|
| `route REQUEST.json` | `dispatch`、资源、返回点、输入投影 | 分派定义已找到；`semantic_execution` 仍为 `not_started` |
| `check ARTIFACT.json --request REQUEST.json` | `checked_kind`、`request_match_checked`、诊断 | 校验结构、可确定引用及请求匹配；省略请求时不声称已核对请求范围 |
| `accept CURRENT.json PROPOSAL.json` | `work_brief` 或拒绝详情 | 形成新草稿；失败时不生成替代权威简报 |
| `impact PREVIOUS.json CURRENT.json` | 变化路径、失效/未影响/既存未验证消费者 | 仅分析实际登记的依赖 |

报告包括 `execution_status`、`outcome`、`audit`、`diagnostics`、`limitations` 和实际执行记录。`audit.structure`、`audit.deterministic`、`audit.semantic`、`audit.media`、`audit.overall` 分开；语义/媒体在这些确定性命令中保持 `unverified`。

退出码 0 表示本次确定性命令完成，**不表示作品已完成或就绪**；1 表示确定性错误/阻塞；2 表示文件/JSON 等输入错误。局部草稿可以结构有效，但仍有未验证部分。专业语义审阅另记审阅者、输入版本、规则、证据和结论，不把脚本报告中的未验证改成通过。

## 6. 变更影响和修复

`consumers` 只登记真实存在的消费者：消费者 ID、模块 ID、结果版本、`source_work_version` 和 `read_paths`。路径使用 JSON Pointer，例如 `/content/paragraphs/P01/function`；只读自身公开需要的数据。

修改后执行 `impact`，按真实读路径相交关系标记失效。纯 `display/title` 变化不会使只读段落内容的消费者失效。曾依赖其他旧版本的记录保持其已有未验证状态，不能因为本次路径未变就补写通过。

没有登记的下游依赖保持未知；程序不能凭十二模块列表声称已找到全部影响，也不调用这些模块。语义修订回到责任子模块，技术输入问题修复后重新执行原命令；本工具不创建隐藏的自动重试循环。

## 7. 来源与按需读取

合同与路由是对冻结方案的 D 类实现细化。源事实、源冲突和规则适用条件见 `case-evidence.md`；H3 字段与引用标签见 `h3-label-mapping.md`。大索引按 ID 读取，例如仅查看一条母题规则及其证据：

```bash
python - <<'PY'
import json
from pathlib import Path
index = json.loads(Path('references/case-index.json').read_text())
rule = next(r for r in index['rules'] if r['id'] == 'CASE-R05')
evidence = [e for e in index['evidence'] if e['id'] in rule['evidence_ids']]
print(json.dumps({'rule': rule, 'evidence': evidence}, ensure_ascii=False, indent=2))
PY
```

全部运行资源随技能目录提供；不要求取得 `docs/skillplan/`、测试目录或其他核心技能才能进行上述独立调用。追溯新的上游证据时可以读取来源链接，但不得静默改写当前版本的规则。
