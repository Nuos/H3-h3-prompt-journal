# H3 通用核心技能：M1 作品意图与段落功能

**交付版本：** `h3-work-intent` v0.1.0。  
**公开合同：** `1.0.0`，本次只固定 M1 的独立合同，不声称全部共享对象已经实现。  
**开发日期：** 2026-11-04（America/Los_Angeles）。  
**计划基线：** `skillplan-v0.1.2-608813b`。  
**仓库读取基线：** `0ce8b7b1890052bf1d4dd233ef20e68817b38f28`。

## 核心摘要

根据已冻结的十二模块方案，首先交付 **M1 作品意图与段落功能**，含三个可独立调用的子模块：M1.1 意图与约束整理、M1.2 段落功能与信息结构、M1.3 情绪能量与母题。技能目录为 `h3-work-intent/`，入口 `SKILL.md`。

领域知识边界为本仓库 `case-studies/` 的文本。以 10 月案例为重点提炼方法，补用已有喜剧、揭示和综艺案例支持有限叙事任务。Anthropic 资料只提供技能格式/开发规范，MiniMax 官方资料只提供模式与协议依据，不能把这些外部资料的示例另当本项目的新创作案例。

本次交付完整的 M1 技能资源、独立子模块合同、H3 模式/字段/Label 映射、确定性工具、文字样例及验证记录。Agent 执行领域理解与编排；Python 工具执行路由、结构检查、提案接受、版本与影响范围检查。工具不自动理解自然语言，不调用 H3，不证明视频效果。

**关键结论：** M1 能单独使用；每个子模块可由外部兼容输入直接调用；子提案由 M1 唯一接受；H3 正文编译仍属于 M11；本交付不代表全部十二模块或完整 P5 集成已经完成。

**关键词：** 作品意图、WorkBrief、段落功能、观众信息、情绪能量、母题、独立调用、约束、H3 Label、局部审计。

## 目录导航

1. 本次实现范围
2. M1 与 H3 模式/Label 的对应
3. 文件组织与使用入口
4. 独立调用与组合方式
5. 验证与能力边界
6. 后续模块状态
7. 固定来源与交付记录

## 1. 本次实现范围

| 节点 | 负责的专业结果 | 输入可由谁提供 | 唯一输出分区 |
|---|---|---|---|
| M1 | 聚合经核对的作品意图与段落语义，接受提案 | 用户、已有项目、三个子模块的兼容提案 | `WorkBrief` 权威接受路径 |
| M1.1 | 创作目标、必保事件、约束优先级与冲突 | 用户需求或兼容项目记录 | `intent`、`constraints`、`must_keep_events` |
| M1.2 | 段落作用、观众信息、必要的揭示/因果关系 | 已有意图与段落内容，不要求重跑 M1.1 | `paragraphs` |
| M1.3 | 情绪/能量走向、母题与变奏/回收 | 已有意图与情绪/母题内容，不要求重跑其他子模块 | `emotion_energy`、`motifs` |

这三个子模块作为一个技能包内的独立职责入口，不另外创建三个空壳 Skill。合同兼容的用户资料或受控替身可以替代上游生产者；读取和写入范围不依赖其他模块的私有文件。

采用“子提案、父接受”。基版本不一致、分区越权、显式阻塞冲突和批次竞争写入均返回诊断，保留原始输入。领域决定需要修订时回到原责任子模块，不由聚合程序无声改写。

## 2. M1 与 H3 模式/Label 的对应

| 官方模式 | 官方主结构 | M1 的贡献 | 交接边界 |
|---|---|---|---|
| T2VA | `integrated_multimodal_description`、`overall_soundscape`、`non_diegetic_music` | 目标、事件、信息顺序、情绪/母题语义 | 专业模块展开，M11 编译 |
| I2VA | 首帧指令 + 同上三个字段 | 从已确认开头继续发展的作品意图 | 首帧绑定由 M2/M8/M11 核对 |
| FL2VA | 首尾帧指令 + 同上三个字段 | 开始至结束的语义发展和必保事件 | 不把两个静态描述替代中间发展；不编造锚点 |
| L2VA | 尾帧指令 + 同上三个字段 | 符合目标的前置语义及结尾收束 | 最终图片属于实际末镜，编号由 M11 决定 |
| Ref2VA | `subject_definitions`、`summary`、`retention_analysis`、`detailed_description`、`overall_soundscape`、`non_diegetic_music` | `summary` 的作品概括；`detailed_description` 的事件/段落目标；保留意图和声音目标的上游约束 | 不混入基础模式主字段；不代替 M2/M6/M9/M11 |

详细映射同时区分官方**字段名**、引用 **Label**（`<Subject N>`、`<Picture N>`、`<Video N>`、`<Audio N>`）、镜头/说话者/对白标记与本项目内部字段。每项均有编排要求、审计条件和责任方。`WorkBrief`、段落 ID、问题 ID 不是官方 H3 Label。

H3 官方主字段的正确拼写为 `integrated_multimodal_description`；`integrated_multimodel_description` 不应写入。Ref2VA 的 `detailed_description` 不能被 `summary` 代替。官方文档中的写作长度建议也不能据此当作模型 token 硬限制。

## 3. 文件组织与使用入口

| 路径 | 用途 | 是否是技能运行所需 |
|---|---|---|
| `h3-work-intent/SKILL.md` | 触发、范围、资源路由、流程与输出边界 | 是 |
| `h3-work-intent/references/` | 三个子模块方法、合同、路由、审计、案例和官方协议依据 | 按任务读取，全部随独立目录提供 |
| `h3-work-intent/scripts/m1_contract.py` | 确定性路由、检查、接受与影响分析 | 使用机器检查时需要 Python 3.10+；标准库 |
| `h3-work-intent/assets/` | 可复制的请求、空简报和子提案示例 | 按任务复制 |
| `_standards/` | 用户指定规范的固定快照、官方最小验证器及许可 | 开发验收资源，不是技能运行依赖 |
| `tests/` | 契约/路由正反例和可重复验证 | 开发资源 |
| `validation/` | 实际命令结果与前向试用证据 | 验收记录 |
| `tools/verify_release.py` | 包结构、引用、来源、冻结完整性与交付清单检查 | 开发资源 |
| `20261104-development-m1-v001.md` | 开发依据、关键设计决定、结果与未完成范围 | 开发记录 |
| `release-manifest.json` | 发布文件列表、字节数与 SHA-256 | 发布一致性记录 |

技能采用 Anthropic 的 `SKILL.md + scripts/ + references/ + assets/` 结构；只有 `SKILL.md` 是规范必需项，本包中的三个可选目录均有实际用途。`name` 与目录名一致，frontmatter 只使用 `name`、`description`。没有把 OpenAI 专用展示文件声明为 Anthropic 必需项。

## 4. 独立调用与组合方式

### 4.1 自然语言调用

完整调用示例：

> 使用 h3-work-intent 整理这个 H3 MV 的作品意图。保留我给出的角色、关键事件和段落顺序，说明每段让观众获得什么信息，规划相对情绪能量和母题，输出 WorkBrief 及未决项。没有音频时不要推算实测拍点。

局部调用示例：

> 只调用 M1.2。使用我已经提供的目标和必保事件，检查这些段落是否有明确功能、是否遗漏事件或提前泄露信息。不要重新创作角色、机位和对白。

### 4.2 命令入口

从 `h3-work-intent/` 目录运行：

```bash
python scripts/m1_contract.py route assets/request-m1.json
python scripts/m1_contract.py check assets/proposal-m1-1.json
python scripts/m1_contract.py accept assets/workbrief-empty.json assets/proposal-m1-1.json
```

精确输入/输出形状、版本处理、局部修订和 `impact` 用法见包内 `references/contract-guide.md`。脚本不修改输入，不提交外部服务；Agent 根据结果完成对应领域工作。

## 5. 验证与能力边界

验收分别保存官方格式检查、补充结构/引用检查、程序正反例、Agent 语义试用及来源完整性。实际结果与范围见 `validation/` 和开发记录；反例被准确拒绝说明检查生效，不能解释成那个创作任务已经就绪。

- 单独复制 `h3-work-intent/` 后，运行所需资源仍在包内；完整项目检索仅用于追溯或新增任务，不是隐含必需依赖。
- 本包语义来源是案例文本；未读取图片/视频来证明作者效果。
- 完整戏剧结构、跨集人物弧线、自动音频测量、全量媒体解析、M11 编译/后端调用、G3/G4 视频/成片验收不在本次完成范围。
- M1 的本地合同与文字能力可以独立验收；冻结路线中 P5 的全系统集成仍依赖后续模块，不因本次 M1 完成而提前标为完成。
- 现有 `docs/skillplan/` 冻结文档与 `case-studies/` 原文保持不变；本次实现状态在新目录登记。

## 6. 后续模块状态

| 编号 | 职责 | 本次状态 |
|---|---|---|
| M1 | 作品意图与段落功能 | 本次独立技能实现与局部验证 |
| M2 | 素材解析、资产绑定与参考权限 | planned；仅保留交接接口 |
| M3 | 场景空间与人物调度 | planned；仅保留交接接口 |
| M4 | 表演动作与物理因果 | planned；仅保留交接接口 |
| M5 | 摄影机、构图、焦点与运镜 | planned；仅保留交接接口 |
| M6 | 声音、音乐与对白 | planned；仅保留交接接口 |
| M7 | 统一时间与协同 | planned；仅保留交接接口 |
| M8 | 状态连续性 | planned；仅保留交接接口 |
| M9 | 分镜、剪辑与生成分段 | planned；仅保留交接接口 |
| M10 | 视觉风格、光线、色彩与材质 | planned；仅保留交接接口 |
| M11 | 模型协议与参数适配 | planned；本次仅提供官方协议映射依据 |
| M12 | 持续审计与修复 | planned；本次仅实现 M1 局部检查及其交接 |

## 7. 固定来源与交付记录

- [技能入口](h3-work-intent/SKILL.md)。
- [H3 逐模式/逐 Label 映射](h3-work-intent/references/h3-label-mapping.md)。
- [三个子模块的公开合同](h3-work-intent/references/contracts.json)与[路由登记](h3-work-intent/references/module-registry.json)。
- [案例证据与范围](h3-work-intent/references/case-evidence.md)。
- [开发与验收记录](20261104-development-m1-v001.md)。
- [实际验证结果](validation/validation-results.json)与[交付文件清单](release-manifest.json)。
- [冻结计划原文](https://github.com/Nuos/H3-h3-prompt-journal/tree/608813b6e51531ac47f860bc384a454a504fe9ff/docs/skillplan)。
- [本次案例读取基线](https://github.com/Nuos/H3-h3-prompt-journal/tree/0ce8b7b1890052bf1d4dd233ef20e68817b38f28/case-studies)。
- [Anthropic Skills 固定版本](https://github.com/anthropics/skills/tree/ca45fc496a3436251f191354091d557da31c15b5)。
- [该仓库转引的 Agent Skills 格式规范](https://github.com/agentskills/agentskills/blob/83021e2be457a9b6679148719c1f6074f0ad975e/docs/specification.mdx)。
- [MiniMax-H3 官方提示词技能固定版本](https://github.com/MiniMax-AI/MiniMax-H3/tree/199b7d0e1fd95e7b3eafa8c15eca692534142427/skills/h3-prompt-writing)。
