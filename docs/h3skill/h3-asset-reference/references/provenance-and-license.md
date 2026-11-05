# 来源、许可与内容边界

## 核心摘要

领域方法来自本仓库 `case-studies/` 文本；职责与架构来自冻结的 `docs/skillplan/`。Anthropic 资料只提供技能开发规范，MiniMax 官方资料只提供输入协议。官方示例没有被纳入本项目创作案例，案例中的作者效果陈述没有被转成本轮媒体实测。

## 固定版本

| 来源 | 固定点 | 用途 |
|---|---|---|
| 开发方案 | v0.1.2；`608813b6e51531ac47f860bc384a454a504fe9ff` | M2/三个子模块、对象归属、四项架构原则 |
| 冻结控制 | `0ce8b7b1890052bf1d4dd233ef20e68817b38f28` | 冻结清单、范围与变更政策 |
| 本轮仓库/案例读取 | `faa8edc311589d68d37e93524c7cb8e553fff857` | 已完成 M1 的公开接口与本轮案例边界 |
| 案例树 | `70a8a2a632d633f5d532db23cad99c772dc23026` | 29 案、97 份目录内文本及 1 份共享索引 |
| Anthropic Skills | `ca45fc496a3436251f191354091d557da31c15b5` | 模板、创建规范、官方 quick_validate |
| Agent Skills 规范 | `83021e2be457a9b6679148719c1f6074f0ad975e` | Anthropic 仓库转引的名称、元数据与目录规范 |
| MiniMax-H3 | `199b7d0e1fd95e7b3eafa8c15eca692534142427` | 五模式、字段、引用 Label 与保留关系 |

引用固定版本使结果可复核，不声明未来版本不变。每份案例文本的哈希、源 Git blob 与实际阅读方式见 `case-index.json`；官方原文定位和核验记录见 `h3-protocol-source.json`。登记完整性不等于全量逐字语义审阅。

## 归属与再分发

本仓库根许可为 MIT，原作者版权行归属 LoveRain1997。本包新增代码和说明依仓库既有许可交付；独立复制时保留 `case-source-LICENSE.txt`。

两份 H3 官方指南保持原字节，归 MiniMax 原作者。不能把官方文档重新标为本仓库原创、MIT 或 Apache-2.0。协议来源记录包含官方许可声明和许可文本来源，`h3-NOTICE.txt` 保留官方归属通知。本包不包含模型权重，也不执行 H3 或付费服务。

Anthropic 验证器、模板和 Agent Skills 规范位于开发交付外层 `_standards/`，保留各自许可；运行本技能不依赖该目录。`agents/openai.yaml` 是可选的产品展示配置，本包采用用户指定的 Anthropic 基础目录，不为满足形式添加无用途目录。

## 事实、设计与已执行证据

| 类别 | 含义 | 本包例子 |
|---|---|---|
| F | 可定位源文本事实 | 案例对身份/姿态/音频用途的原文 |
| D | 架构与实现细化 | M2State、子提案接受、范围冲突检查 |
| I | 已有实现及实际执行 | 脚本、实际测试和 Agent 试用记录 |
| U | 尚未验证 | 没有提供的素材、真实模型运行与成片效果 |

F/D/I/U 不是观察状态枚举，I 不表示“推断”。作者报告仍有作者归属；代码检查不认证素材真实性；自然语言试用不证明宿主产品的自动触发率。

本包只固定 M2 合同 `1.0.0`。三个共享对象在 M2State 中保持独立字段责任；不宣称已实现全局 ProjectPlan、M3—M12、完整 P5 集成或 P9 媒体验证。外部兼容数据可输入，未实现下游以交接记录保留。

## 集中来源

- [冻结开发方案](https://github.com/Nuos/H3-h3-prompt-journal/tree/608813b6e51531ac47f860bc384a454a504fe9ff/docs/skillplan)。
- [冻结控制清单](https://github.com/Nuos/H3-h3-prompt-journal/blob/0ce8b7b1890052bf1d4dd233ef20e68817b38f28/docs/skillplan/baseline-lock.json)。
- [本轮案例基线](https://github.com/Nuos/H3-h3-prompt-journal/tree/faa8edc311589d68d37e93524c7cb8e553fff857/case-studies)。
- [已完成 M1](https://github.com/Nuos/H3-h3-prompt-journal/tree/faa8edc311589d68d37e93524c7cb8e553fff857/docs/h3skill/h3-work-intent)。
- [仓库 MIT 许可](https://github.com/Nuos/H3-h3-prompt-journal/blob/faa8edc311589d68d37e93524c7cb8e553fff857/LICENSE)。
- [Anthropic 技能模板](https://github.com/anthropics/skills/blob/ca45fc496a3436251f191354091d557da31c15b5/template/SKILL.md)。
- [Anthropic 技能创作指南](https://github.com/anthropics/skills/blob/ca45fc496a3436251f191354091d557da31c15b5/skills/skill-creator/SKILL.md)。
- [Agent Skills 格式规范](https://github.com/agentskills/agentskills/blob/83021e2be457a9b6679148719c1f6074f0ad975e/docs/specification.mdx)。
- [MiniMax-H3 官方提示词目录](https://github.com/MiniMax-AI/MiniMax-H3/tree/199b7d0e1fd95e7b3eafa8c15eca692534142427/skills/h3-prompt-writing)。
