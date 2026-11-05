# M8 来源、许可与内容边界

## 1. 本包范围

本包实现第八核心模块“状态、连续性与镜头交接”。M8.1 管理连续性策略，M8.2 管理计划状态与转换，M8.3 只读检查边界并提出结果或修订要求。父 M8 是接受版本的唯一写入入口。实际媒体观察属于 M12，不能把计划账本、作者报告或合同通过写成生成效果已验证。

创作领域方法仅从本仓库 `case-studies/` 已读文本提取。冻结开发方案决定模块职责及合同设计，MiniMax 官方资料决定输入模式与字段/Label，Anthropic/Agent Skills 资料决定技能创建格式。合同、运行器、路由、审计条件及夹具均为本轮实现，不是新发现的 H3 模型能力。

## 2. 固定来源

| 来源 | 固定版本或入口 | 用途 |
| --- | --- | --- |
| 冻结开发方案 | `skillplan-v0.1.2-608813b`；`608813b6e51531ac47f860bc384a454a504fe9ff` | M8.1/M8.2/M8.3、单一职责、版本接受及 M12 边界 |
| 冻结控制 | `docs/skillplan/AGENTS.md`、`LOCK.md`、`baseline-lock.json` | 保持冻结原文与控制文件 |
| 本轮输入仓库 | `f1456793d21bfb411d36eea13cee2916c3bd20c5` | 原案例文本和已完成模块的公开接口 |
| MiniMax-H3 | `199b7d0e1fd95e7b3eafa8c15eca692534142427` | 五种模式、基础三字段、Ref2VA 六字段和四类 Label |
| Anthropic Skills | `ca45fc496a3436251f191354091d557da31c15b5` | `skills/skill-creator/SKILL.md`、模板与创建/校验流程 |
| Agent Skills | `83021e2be457a9b6679148719c1f6074f0ad975e` | Anthropic 规范入口指向的字段和目录规范 |

本轮通过 GitHub connector 按固定提交重新获取 MiniMax 的 base-en.txt 和 ref-en.txt，与既有 M7 快照按 UTF-8 字节比较一致后复制到本包；新的验证时间与方式记录在 [h3-protocol-source.json](h3-protocol-source.json)。上游历史验证记录保留为历史，不冒充本轮分支 HEAD、许可或其他文件的重新获取。未来上游变化不自动改变本包的固定协议。

## 3. 证据与实际阅读

F 为案例明确要求，A 为作者报告，D 为本轮设计/推导，P 为官方格式或协议，I 为实际执行的清点/读取/验证，U 为未知或未验证。不同证据层不互相替代。

[case-index.json](case-index.json) 清点固定提交中的 29 个案例目录、98 个文本文件，记录每个文件的 SHA-256、Git blob、字节/行数和关键词计数。语义证据仅覆盖 4 个十月案例、6 个文件：3 个全文、3 个选段。其余 92 个文本只有索引，不宣称已完成语义审阅；媒体检查数为 0。完整文件的列入和哈希成功也不能证明其中所有方法正确。

[case-evidence.md](case-evidence.md) 提供离线可读的必要摘录、固定原文地址、案例专属参数与可迁移规则的区分。重点为剑舞的持剑/空鞘状态、身份与姿态权限分离、白凤 SEG03→SEG04 正文/交接表缺口，以及触地换装的接触/保持/释放和区间计数。时空省略、倒叙、伤情状态等未由本轮四个案例直接证实的内容，明确作为合同设计或未知处理。

状态区间可以返回先前值，是冻结开发路线图 §6.3 的合同设计；不能说触地换装案例实际出现了相同袜饰回返。所有案例时码、片段数、左右关系、具体武器/服装/场景都是各案条件，不作全局默认。

## 4. 独立使用与技能目录

运行包由 `SKILL.md`、必要 `scripts/`、按需 `references/`、可复制 `assets/` 组成。它可独立复制使用，不通过运行时导入兄弟模块获得规则或脚本。这里的可选资源目录是本模块的实际需要，官方并未要求每个技能都必须具有这些目录。`agents/openai.yaml` 是宿主扩展，不是 Anthropic 通用格式的必选项。

兼容公开输入可以代替先运行 M1—M7；无需强制完整流水线。M8.3 不自行改状态，M8.2 不替 M4 设计动作、替 M7 改时码，M8 不执行 M9 剪辑、M11 编译或 M12 媒体观测。仓库交付不表示已在某个宿主自动安装或已经测得触发率。

## 5. 许可与归属

本轮实现遵循项目既有 MIT 许可；案例来源许可完整保存在 [case-source-LICENSE.txt](case-source-LICENSE.txt)。复制或调整项目已有合同机制不改变原项目归属。

MiniMax 官方原文保留来源、原字节及原有归属，不重新标为本项目 MIT 或 Apache-2.0。[h3-NOTICE.txt](h3-NOTICE.txt) 保留 MiniMax 通知；协议 JSON 保存官方 README 的许可声明以及既有完整许可文本记录。许可文本的已记录获取方式是网页抽取，不冒称原始文件逐字节快照。此包只做提示词规划和离线检查，不交付模型权重或调用生成服务。

Anthropic 与 Agent Skills 的标准、校验器及其许可证置于包外 `_standards/`；对应发布检查登记其身份。测试输入输出、发布清单和验证记录也置于包外 `validation/m8/`，不混入运行时知识资源。

## 6. 可复现范围与限制

来源核验可重算字节哈希与 Git blob；合同检查可复核结构、引用地址、允许状态变化、区间/边界关系与版本接受。上述验证与实际 H3 运行、视频解码、运动/身份稳定性、声音接缝或观众感知效果分别表述。发现缺失证据时保留未知和所需输入，不用默认静音、默认状态相同或自动修正掩盖缺口。

## 来源入口

- [冻结核心框架](https://github.com/Nuos/H3-h3-prompt-journal/blob/608813b6e51531ac47f860bc384a454a504fe9ff/docs/skillplan/01-core-framework.md)
- [冻结开发路线图](https://github.com/Nuos/H3-h3-prompt-journal/blob/608813b6e51531ac47f860bc384a454a504fe9ff/docs/skillplan/02-development-roadmap.md)
- [案例输入基线](https://github.com/Nuos/H3-h3-prompt-journal/tree/f1456793d21bfb411d36eea13cee2916c3bd20c5/case-studies)
- [MiniMax 基础模式](https://github.com/MiniMax-AI/MiniMax-H3/blob/199b7d0e1fd95e7b3eafa8c15eca692534142427/skills/h3-prompt-writing/references/base-en.txt)
- [MiniMax Ref2VA](https://github.com/MiniMax-AI/MiniMax-H3/blob/199b7d0e1fd95e7b3eafa8c15eca692534142427/skills/h3-prompt-writing/references/ref-en.txt)
- [Anthropic 创建标准](https://github.com/anthropics/skills/blob/ca45fc496a3436251f191354091d557da31c15b5/skills/skill-creator/SKILL.md)
- [Agent Skills 规范](https://github.com/agentskills/agentskills/blob/83021e2be457a9b6679148719c1f6074f0ad975e/docs/specification.mdx)
