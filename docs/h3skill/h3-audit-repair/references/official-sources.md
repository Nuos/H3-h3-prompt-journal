# M12 官方格式与协议来源

**核心摘要：** H3 官方文档只授权本包断言输入格式和引用语义；Anthropic／Agent Skills 文档用于技能结构和开发方法；业务内容仍由冻结方案及本仓库案例限定。

**关键词：** 固定提交、SHA256、来源、格式、快照、渐进加载、验证边界。

**目录导航：** 1. 来源层次；2. H3；3. 技能标准；4. 目录落实；5. 验证边界。

## 1. 来源层次与用途

| 来源 | 固定版本／定位 | 本包用途 | 不能据此宣称 |
| --- | --- | --- | --- |
| 项目开发方案 | `skillplan-v0.1.2-608813b`；提交 `608813b6e51531ac47f860bc384a454a504fe9ff` | M12.1–M12.4、对象所有权、G0–G4 和依赖／失效原则 | 方案条目已自动实现或已被模型实测 |
| 案例集合 | 仓库基线 `9fc2520bec5bc9d339e6b88dd1e93b9cd6f6992a` 的 `case-studies/` | 限定业务证据和回归情境；具体逐案来源见案例索引 | 作者报告等同独立测量；同源副本等同新证据 |
| MiniMax H3 官方 | 下述固定提交的基础／参考模式文档 | 五模式、字段、Label、首行、保留与声音／切镜语法 | 部署已支持、推理已完成、输出质量已合格 |
| Anthropic Skills | 下述固定提交的模板、creator、校验器及规范指针 | `SKILL.md` 结构、渐进加载、资源组织、评估方法 | Anthropic 官方认证本包功能 |
| Agent Skills | Anthropic 规范指针指向的开放规范、下述固定提交 | 名称／描述和资源路径等具体格式约束 | 本项目额外合同是规范强制要求 |

方案与案例提供项目内容边界，官方技能规范不引入新的摄影、表演或案例领域事实。所有来源的许可和身份保留原归属，见 [provenance-and-license.md](provenance-and-license.md)。

## 2. H3 官方协议：固定原文及完整性

仓库 `MiniMax-AI/MiniMax-H3`，提交 `199b7d0e1fd95e7b3eafa8c15eca692534142427`。这是刻意固定的协议版本，不代表未来或任意部署的最新行为。

| 包内原文 | 官方不可变链接 | Git blob SHA-1 | SHA256／UTF-8 字节数 |
| --- | --- | --- | --- |
| `h3-base-official.txt` | [base-en.txt](https://github.com/MiniMax-AI/MiniMax-H3/blob/199b7d0e1fd95e7b3eafa8c15eca692534142427/skills/h3-prompt-writing/references/base-en.txt) | `40cf586a634d677d6b7107b367cf0ec9621be728` | `2cfebc096a6e08370f288d468d90b60f7f9bcb938f94bf090816e910e48e75fc`；15773 |
| `h3-ref-official.txt` | [ref-en.txt](https://github.com/MiniMax-AI/MiniMax-H3/blob/199b7d0e1fd95e7b3eafa8c15eca692534142427/skills/h3-prompt-writing/references/ref-en.txt) | `7ae1b2d07d743fd2392258a96449be9e9e322d35` | `1e574f356716ad55612247ffb7bbccbcdb484ad96599d63c7dca1af186b1fab7`；23553 |

本轮通过 GitHub 连接器重新取得上述两份固定源文件，完整 UTF-8 内容的 SHA256 和远端 Git blob 标识与 M11 离线快照一致，再将原始快照复制入本包。原文未添加标题、导航、转译或版权前言；因此原始行号可用于逐条复核。M12 映射说明另放在 [h3-label-mapping.md](h3-label-mapping.md)。

`h3-protocol-source.json` 保留来源元数据、历史校验和许可证记录，并单独记录本轮两份原文的新核对。`h3-NOTICE.txt` 原样保留。此前记录中的官方 README、官方技能入口与许可证提取文本属于继承资料；本轮没有重新读取它们，不能给它们标记新的远端验证。许可证提取文本也不声称与原始 LICENSE 文件逐字节相同。

原文按需查阅位置：基础四模式及首行 B:5–70；完整主正文和声音 B:76–171；参考六字段 R:13–37；Label R:41–118；任务前缀 R:120–155；保留等级 R:160–211；切镜与声音 R:215–306。

## 3. Anthropic 与 Agent Skills 标准

Anthropic 固定提交为 `ca45fc496a3436251f191354091d557da31c15b5`。本轮重新读取完整 [skill-creator/SKILL.md](https://github.com/anthropics/skills/blob/ca45fc496a3436251f191354091d557da31c15b5/skills/skill-creator/SKILL.md)：Git blob `65b3a402dbd09b8e83f9d637c6b553875189085c`，SHA256 `dcd4803e61e913e6fc27294184cd3a71f09f5e924ff20c8a9a20173e7b3c2bcf`，33168 个 UTF-8 字节。该文用于结构和开发流程，不作为 H3 内容证据。

下列文件沿用仓库 `docs/h3skill/_standards/` 的固定快照和 `source-files.json` 清单；本轮本地读取不冒充再次远端下载。标准快照是开发核验资料，安装本技能不依赖上级或兄弟目录。

| 官方依据 | 固定源链接 | 快照 SHA256 | 对本包的要求 |
| --- | --- | --- | --- |
| Anthropic 模板 | [template/SKILL.md](https://github.com/anthropics/skills/blob/ca45fc496a3436251f191354091d557da31c15b5/template/SKILL.md) | `eb685d91de039ed864fbd790cddf31684b017fd4a34ee1a55760d8d7cdbadefa` | 技能入口包含 YAML `name`、`description` 和 Markdown 指令 |
| Anthropic 官方校验器 | [quick_validate.py](https://github.com/anthropics/skills/blob/ca45fc496a3436251f191354091d557da31c15b5/skills/skill-creator/scripts/quick_validate.py) | `67cf5703402013936c8fb75ad6a1afecd8841d45cc5e606b634eb05825fde365` | 实际运行检查它覆盖的结构；不扩称语义／媒体认证 |
| Anthropic 规范指针 | [agent-skills-spec.md](https://github.com/anthropics/skills/blob/ca45fc496a3436251f191354091d557da31c15b5/spec/agent-skills-spec.md) | `ff22f2be775f4b757c9a7a2df0421de4c94021d34d9382cea5dd567ff0cdad2c` | 具体开放格式以其所指规范为依据 |
| Agent Skills 规范 | [specification.mdx](https://github.com/agentskills/agentskills/blob/83021e2be457a9b6679148719c1f6074f0ad975e/docs/specification.mdx) | `b9079c0c10b7930e8c6a20ff2bc10cda2a3343c55185120e3f1116a1a529b220` | 必需入口、名称／描述限制、可选资源、相对引用和渐进加载 |

Agent Skills 规范固定提交为 `83021e2be457a9b6679148719c1f6074f0ad975e`。两套标准的许可快照和精确 Git blob／字节数沿用 `_standards/source-files.json`；本包不复制这些标准全文，也不更改它们。

## 4. 官方技能结构如何落实到 M12

| 结构项 | 官方要求或建议 | 本包落实方式 |
| --- | --- | --- |
| 目录与名称 | 技能目录至少含 `SKILL.md`；名称 1–64 字符、允许小写字母／数字／连字符、无首尾或连续连字符，且与父目录同名 | `h3-audit-repair/SKILL.md`，frontmatter 的 `name` 同名 |
| 触发描述 | 必需非空 `description`，不超过 1024 字符，说明做什么和何时使用 | 说明 H3 持续审计、G0–G4、真实观察、修复和复检场景 |
| 主体指令 | Markdown；建议聚焦且低于 500 行，详细信息按需加载 | 主文件承载执行路由、证据门槛和返回合同；长表和来源放 `references/` |
| `scripts/` | 可选，代码应独立或明确依赖，并有可理解错误 | 合同检查脚本明确 Python 与输入要求；不隐式调用兄弟模块 |
| `references/` | 可选，聚焦的领域／过程资料，按需读取 | 自包含协议快照、映射、合同说明、证据／修复说明和来源记录 |
| `assets/` | 可选，静态模板／资源 | 可复制请求示例、状态模板和审计报告模板；内部对象不序列化成 H3 原生字段 |
| 相对引用 | 明确技能内相关文件的路径，避免无穷嵌套查找 | SKILL 路由直达配套资源；源文长文件使用本文行号导航，不污染原始字节 |
| `agents/openai.yaml` | 不是 Anthropic 必需项；开放规范允许附加资源 | 仅作可选客户端适配；不能称为 Anthropic 强制目录要求 |
| 验证与迭代 | 使用现实提示和可判定预期；真实技能／基线运行、计时和评分证据与计划分开 | 开发验证置于仓库 `validation/m12/`，不把测试通过等同运行效果提升 |

可选资源不是为凑目录而添加；只保留本模块执行需要的内容。开发记录、测试输出、发布清单不必进入安装包；这种仓库分层是项目组织选择，不声称为官方强制目录树。

## 5. 必须保留的验证边界

结构校验只能支撑格式范围内的结论；合同测试只能支撑测试过的输入／输出不变量。新上下文中的 Agent 文本任务、with-skill／baseline 成对行为对比、触发率评估与 H3 推理是不同验证项目，分别以实际执行记录报告。仅有 Agent 文本使用记录不能宣称已完成成对基线对比或触发率评估；没有执行 H3 推理时，其运行状态必须保留 `not_run`，不能宣称生成质量实验完成。

M12 的 G0–G2 文本审阅不能替代 G3 片段／G4 整片的实际媒体检查。案例作者的成功报告、官方协议陈述、计划状态和工程 fixture 均不能单独证明本次媒体已合格。验证记录应明确“检查了什么、使用什么证据、仍未检查什么”；旧版结论不能自动适用于新版本。

本轮具体来源核对记录见仓库 `docs/h3skill/validation/m12/standards-verification.json`；H3 两份原文的包内可移植来源记录见 [h3-protocol-source.json](h3-protocol-source.json)。
