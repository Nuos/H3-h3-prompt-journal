# 来源、许可与实现边界

## 核心摘要

本包的领域方法取自 `Nuos/H3-h3-prompt-journal/case-studies/` 文本；结构与职责取自已冻结的 `docs/skillplan/`。Anthropic/Agent Skills 文档仅规定技能格式与开发方式，MiniMax-H3 文档仅规定对应模式和提示词协议。来源版本分别固定，不因较新的文件日期自动覆盖当前任务授权。

## 固定来源

| 来源 | 固定提交/基线 | 用途 | 包内追溯资源 |
|---|---|---|---|
| 开发方案 | `608813b6e51531ac47f860bc384a454a504fe9ff`，v0.1.2；冻结控制提交 `0ce8b7b1890052bf1d4dd233ef20e68817b38f28` | M1/三个子模块、WorkBrief责任、四项架构原则、路由/审计要求 | 合同、路由和审计交接 |
| 案例文本 | `0ce8b7b1890052bf1d4dd233ef20e68817b38f28`；案例树 `70a8a2a632d633f5d532db23cad99c772dc23026` | 当前领域事实、方法提炼、差异与冲突 | `case-evidence.md`、`case-index.json` |
| Anthropic Skills | `ca45fc496a3436251f191354091d557da31c15b5` | 官方最小模板、创建工作流、quick_validate | 交付外层 `_standards/`；本包运行不依赖该目录 |
| Agent Skills 标准 | `83021e2be457a9b6679148719c1f6074f0ad975e` | Anthropic 仓库直接转引的正式格式规范 | 本包入口遵循其 name/description、目录和渐进读取约定 |
| MiniMax-H3 | `199b7d0e1fd95e7b3eafa8c15eca692534142427` | 五种模式、精确字段名及标签语义 | `h3-label-mapping.md`、`h3-protocol-source.json`、两份官方文本 |

`case-index.json` 保存所有登记文本的 Git blob、SHA-256、原文定位及实际阅读范围。登记哈希不表示逐字语义审计；读过提示词也不等于读过或复现了对应媒体。

## 归属与再分发记录

- 本仓库根 `LICENSE` 为 MIT，版权行归属原项目作者 LoveRain1997。独立复制本技能时保留包内 `case-source-LICENSE.txt`；该文件是根许可的逐字副本。
- 本包新增合同、代码和业务说明在本仓库既有许可体系下交付。案例原文的归属、具体参数与作者报告保留；本包提炼不冒充案例作者的原始实现。
- `_standards/` 中的 Anthropic skill-creator 验证器及相关文件保留 Apache-2.0 文本；其转引的 Agent Skills 规范保留文档 CC BY 4.0 归属。开发资源没有成为技能的隐含外部运行依赖。
- MiniMax 官方文本保持原字节与来源记录，不把它们重新标为本仓库原创或 MIT。具体来源与许可声明以 `h3-protocol-source.json` 中登记的官方文档/仓库信息为准；本包不包含模型权重，也不执行模型服务。

## 从来源到实现

| 层次 | 本包允许的结论 | 不允许的跳跃 |
|---|---|---|
| 案例原文 F | 来源确实有某条规则/描述/作者报告 | 作者说成功 ⇒ 本次已实测成功 |
| 本包设计 D | 已定义三子模块、分区、接受与检查合同 | 合同已写 ⇒ 所有上下游已实现 |
| 执行记录 I | 某版本、输入和命令/语义试用实际产生记录 | 静态通过 ⇒ 视频稳定 |
| 尚未验证 U | 素材、编译、后端或媒体缺口如实保留 | 缺证据 ⇒ 不适用或默认通过 |

冻结方案中的完整 P5 集成、P7 全量迁移、P9 媒体验证都有各自前提。本次发布是 M1 独立实现及其局部验收，不改写冻结文档历史状态、不提前宣布整个路线完成。

## 集中来源

- [冻结开发方案](https://github.com/Nuos/H3-h3-prompt-journal/tree/608813b6e51531ac47f860bc384a454a504fe9ff/docs/skillplan)。
- [冻结控制记录](https://github.com/Nuos/H3-h3-prompt-journal/blob/0ce8b7b1890052bf1d4dd233ef20e68817b38f28/docs/skillplan/baseline-lock.json)。
- [案例读取基线](https://github.com/Nuos/H3-h3-prompt-journal/tree/0ce8b7b1890052bf1d4dd233ef20e68817b38f28/case-studies)。
- [项目 MIT 许可原文](https://github.com/Nuos/H3-h3-prompt-journal/blob/0ce8b7b1890052bf1d4dd233ef20e68817b38f28/LICENSE)。
- [Anthropic 模板](https://github.com/anthropics/skills/blob/ca45fc496a3436251f191354091d557da31c15b5/template/SKILL.md)。
- [Anthropic 正式标准转引](https://github.com/anthropics/skills/blob/ca45fc496a3436251f191354091d557da31c15b5/spec/agent-skills-spec.md)。
- [Agent Skills 格式规范](https://github.com/agentskills/agentskills/blob/83021e2be457a9b6679148719c1f6074f0ad975e/docs/specification.mdx)。
- [MiniMax-H3 官方提示词技能](https://github.com/MiniMax-AI/MiniMax-H3/tree/199b7d0e1fd95e7b3eafa8c15eca692534142427/skills/h3-prompt-writing)。
