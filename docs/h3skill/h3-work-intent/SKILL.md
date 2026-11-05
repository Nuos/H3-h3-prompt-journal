---
name: h3-work-intent
description: "为 MiniMax H3 视频创作整理作品意图、必保事件与约束优先级，编排段落功能、观众信息、情绪能量和动作/视觉母题，输出可追溯的 WorkBrief、局部审计和 H3 字段交接。用于开始或修订 MV/有限叙事视频方案、解释每段为何存在、审查内容遗漏或信息顺序，以及单独调用 M1.1 意图约束、M1.2 段落信息、M1.3 情绪母题。仅检查机位、拍点、素材绑定或请求直接生成视频时转交相应职责，不代替完整 H3 编译器。"
---

# H3 作品意图与段落功能

将创作要求组织为有来源、有边界的作品意图。回答：观众应理解、期待或感受到什么；每段为何存在；哪些事件必须保留；内容如何发展；判断依据是什么。

实现 M1 及 M1.1、M1.2、M1.3。采用**子提案、父接受**；M1 是 WorkBrief 的唯一权威接受者。保持三个子模块可直接调用，不隐式启动其他核心模块。

## 1. 先选择范围与资源

读取用户当前要求与所需输入投影，不依赖未提供的会话记忆。选择完整 M1 或一个子模块；已给出兼容输入时直接使用，不重复执行上游。段落是作品语义单元，不等同于镜头、分镜格或生成任务。

| 当前任务 | 目标 | 必读资源 | 输出去向 |
|---|---|---|---|
| 新建/总体修订作品意图 | M1 | 本文件、合同指南、审计交接；按需读三个子模块 | WorkBrief、局部检查、调用者/G0 的 M1 部分 |
| 整理目标、必保项、可调项和冲突 | M1.1 | 意图与约束 | M1Proposal → M1 接受；可独立交付提案 |
| 组织段落作用、观众信息和因果顺序 | M1.2 | 段落与信息 | M1Proposal → M1 接受；可直接交下游审阅 |
| 组织情绪/能量走向、母题与变奏 | M1.3 | 情绪与母题 | M1Proposal → M1 接受 |
| 核对 H3 输入模式、字段或 Label 的贡献 | 当前 M1 任务的交接检查 | H3 映射；发生歧义时读相应官方原文 | M11 接口的语义约束，保留未完成的编译工作 |
| 仅审计已有产物 | 明确的 M1/M1.x 范围 | 合同、对应子模块、审计交接 | 带位置/证据/修复目标的发现；不自动改写 |

资源由本文件单跳定位：

- [合同指南](references/contract-guide.md)：第一次构造请求、独立调用、接受提案或解释脚本结果时读。
- [机读字段合同](references/contracts.json)、[模块与路由登记](references/module-registry.json)：接入自动化、校验兼容版本或定位最小输入时读相关节点。
- [意图与约束](references/intent-constraints.md)：M1.1 的编排与局部审计。
- [段落与信息](references/paragraph-information.md)：M1.2 的编排与局部审计。
- [情绪与母题](references/emotion-motif.md)：M1.3 的编排与局部审计。
- [审计与交接](references/audit-and-handoff.md)：证据状态、父子接受、失败回传、变更及下游边界。
- [案例证据](references/case-evidence.md)：需要选择领域方法、辨别案例冲突或确认某条规则依据时读。
- [29 案角色索引](references/case-index.json)：按 `CASE-Rxx`/`CExx` 或案例 ID 定位来源；使用合同指南末尾的选择性读取示例，不默认全文加载大索引。
- [H3 字段和 Label 映射](references/h3-label-mapping.md)：检查五种模式的编排去向和对应审计条件。
- [H3 基础模式官方原文](references/h3-base-official.txt)、[H3 Ref2VA 官方原文](references/h3-ref-official.txt)、[协议来源记录](references/h3-protocol-source.json)：需要精确拼写、语法、例外或版本依据时读取；原文示例仅作为协议说明。
- [来源与许可](references/provenance-and-license.md)：检查来源固定点、再分发归属和当前适用边界时读。

## 2. 建立最小输入

使用 `M1Request`，合同版本 `1.0.0`，记录请求 ID、目标模块、作品 ID、基版本、来源及输入。接受自由文本任务后由 Agent 转为该合同；脚本不自动理解自然语言。

| 目标 | 最小业务输入 |
|---|---|
| M1 / M1.1 | `work_type` 与 `creative_request` |
| M1.2 | `work_type`、`intent_context`、`paragraph_material` |
| M1.3 | `work_type`、`intent_context`、`emotion_material` |

`work_type` 取 `drama`、`mv` 或 `hybrid`。这里的 drama 只表示当前任务侧重叙事，不能据此宣称已经验证完整影视剧创作能力。源证据优先覆盖仓库已有 MV、喜剧、揭示与综艺案例。

缺相关输入时记录具体缺项。可用 `{ "state": "unknown", "reason": "..." }` 表示允许未知的语义文本；不要用空字符串、伪造事实或“不适用”隐藏缺项。继续完成无依赖的部分，保留阻塞范围。

不要从案例复制全局默认：人数、画幅、时长、段数、BPM、旋转预算、景别、是否口型、是否连续切镜，都由本次要求和真实资料决定。

## 3. 执行领域编排

1. **M1.1：** 保存原始要求与来源；整理作品目标、观众应获得的信息、必保事件、约束优先级、允许变化与冲突。逐字要求保留原文。
2. **M1.2：** 给段落稳定 ID，明确作用、进入/离开信息、必保事件归属与必要前序。只保留有依据的人物目标；不填造心理或剧情。向 M5 提观看目标，向 M9 提组织意图。
3. **M1.3：** 给段落安排有依据的情绪与能量发展，定义可识别母题、变奏和回收。允许低潮、留白和有目的的重复。没有音频时只给相对意图，不编造测量结果。
4. **M1 接受：** 核对提案的作品、源请求、基版本、分区所有权、未决项和语义审阅。接受兼容提案形成新 WorkBrief；冲突或过期提案退回相应子模块。不要由聚合器偷偷重写内容。

完整 M1 可以逐步从创作请求建立三类输入。M1.2/M1.3 需要的投影尚未形成时，将后续步骤保留待执行；路由成功不是专业工作已完成。

## 4. 执行确定性检查

运行工具需要 Python 3.10+，仅使用标准库；无需联网、API 密钥、GPU 或 H3 模型。语义编排由当前 Agent/人工完成。

从技能目录运行，输入/输出文件放在当前任务目录：

```bash
python scripts/m1_contract.py route assets/request-m1.json
python scripts/m1_contract.py check assets/proposal-m1-1.json
python scripts/m1_contract.py accept assets/workbrief-empty.json assets/proposal-m1-1.json
```

对真实产物使用 `check ARTIFACT.json --request REQUEST.json` 对照请求；使用 `accept CURRENT.json PROPOSAL.json` 接受单项或批次提案；使用 `impact PREVIOUS.json CURRENT.json` 核对已登记消费者的实际读取依赖。命令只将 JSON 写到标准输出，不原地修改输入；需要保存时使用新的输出路径。

按任务取用可复制模板：

- [完整 M1 请求](assets/request-m1.json)、[M1.1 请求](assets/request-m1-1.json)、[M1.2 请求](assets/request-m1-2.json)、[M1.3 请求](assets/request-m1-3.json)。
- [初始 WorkBrief](assets/workbrief-empty.json)：版本 0 的起始记录，不能当作已完成作品意图。
- [M1.1 提案](assets/proposal-m1-1.json)、[M1.2 提案](assets/proposal-m1-2.json)、[M1.3 提案](assets/proposal-m1-3.json)。

模板是有来源的受控文字例，不是新任务的事实。复制后替换作品/请求/来源/基版本与内容，并重新检查。脚本报告中的 `audit.semantic: unverified` 表示尚需领域判断；不能删掉该状态制造通过。

## 5. 审计与交接

依次核对原始要求保真、必保覆盖、段落功能、信息顺序、情绪/母题依据、父子版本与字段权限。对照本次范围记录 Agent/人工的语义判断及证据；脚本报告独立保存，不改其未执行部分。

H3 交接使用精确字段：

| 模式 | M1 的主要语义去向 |
|---|---|
| T2VA / I2VA / FL2VA / L2VA | `integrated_multimodal_description` 中经专业模块展开的目标、事件与信息顺序 |
| Ref2VA | `summary` 的目标概括、`detailed_description` 的事件展开；保持/变化意图经 M2 进入 `retention_analysis` |
| 全部模式的声音层 | 情绪目标经 M6 变成可听描述，供 `overall_soundscape` / `non_diegetic_music` 使用 |

这是一份贡献矩阵，不是 M1 直接写这些官方字段的授权。`integrated_multimodel_description` 是错误拼写；Ref2VA 使用 `detailed_description`。标签身份、编号、关键帧指令、镜头切点和运行参数由对应领域合同经 M11 序列化。M1 不把内部字段当作官方 Label。

冲突返回产生问题的子模块；素材权限交 M2，动作/摄影/声音交 M4/M5/M6，时间交 M7，状态/编辑交 M8/M9，视觉交 M10，协议交 M11，跨模块/媒体审计交 M12 接口。返回具体问题、对象、基版本、证据、期望修订与复核范围。没有下游实现时交付交接请求，不声称已执行调用。

## 6. 按用户请求交付

默认给出：作品目标；必保/可调事项；逐段功能和信息变化；情绪能量与母题；具体未决项；相应结构化产物。用户只要求单个子模块时只交付该范围。

将内部路由、来源分类、审计和开发说明与创作正文分开。用户要求纯 H3 提示词时，提供本职责已完成的语义交接并列明尚需的专业计划/编译，不把 WorkBrief 冒充可直接提交的完整 H3 请求。

准确报告完成层次：本模块可完成文字编排、局部审阅和确定性合同检查；它只贡献 G0/G1 的相关部分。完整 G1、G2 编译运行、G3 视频、G4 成片需要各自证据。不要从作者报告、文件格式通过或代理试用推导视频稳定率。
