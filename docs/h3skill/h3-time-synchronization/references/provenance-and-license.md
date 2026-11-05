# M7 来源、许可与内容边界

## 核心摘要

本包实现冻结方案的第七核心职责：统一时间轴与动作—镜头—声音协同，输出版本化 `TimingMap`。创作领域方法限定为本仓库 `case-studies/` 的文本；开发方案规定架构；MiniMax 官方资料规定输入模式和提示词协议；Anthropic 与 Agent Skills 资料规定技能格式。时钟合同、精确换算、路由和设计夹具属于本轮实现。

**关键结论：** M7.1—M7.3 分别提出时间依据、事件排时和域间映射候选，由父 M7 唯一接受。合同通过、数学换算通过、文字审阅、作者报告与真实媒体效果分别表述。

**关键词：** M7、TimingMap、时间域、同步关系、帧率、量化误差、来源、独立调用。

## 1. 固定来源与版本

| 来源 | 固定版本 | 用途 |
| --- | --- | --- |
| 开发方案 | `skillplan-v0.1.2-608813b`；内容提交 `608813b6e51531ac47f860bc384a454a504fe9ff` | 十二模块与 M7 三个子模块的职责、架构和路由 |
| 冻结控制 | `docs/skillplan/AGENTS.md`、`LOCK.md`、`baseline-lock.json` | 保护全部冻结原文和控制记录 |
| 本轮仓库输入 | `075fb72797fdca42bc47e38516cf3dbc16f4442d` | 案例文本、M1—M6 公开接口及既有发布约定 |
| MiniMax-H3 | `199b7d0e1fd95e7b3eafa8c15eca692534142427` | 五种模式、基础三字段、Ref2VA 六字段和 Label |
| Anthropic Skills | `ca45fc496a3436251f191354091d557da31c15b5` | 目录模板、渐进加载、创建过程与基础校验器 |
| Agent Skills | `83021e2be457a9b6679148719c1f6074f0ad975e` | Anthropic 规范入口所指向的字段和目录规范 |

2026-11-05 再次读取三个上游主分支，与上述固定版本一致。重新获取 MiniMax 的 base-en.txt 和 ref-en.txt，并与随包离线快照按 UTF-8 字节比较一致。将精确版本、原路径、哈希与协议映射保存在 `h3-protocol-source.json`；未来上游变化不自动改变本包。

冻结文档的 M7 合同、M7.1—M7.3 拆分，以及高内聚、低耦合、模块化、信息路由四项要求是本包的开发依据。M1—M6 运行包、全部案例文本和冻结控制文件保持原字节。新增实现与验证记录保存在 `docs/h3skill/` 的对应位置。

## 2. 证据分层

| 类别 | 含义 | 不能被升级为 |
| --- | --- | --- |
| F | 案例原文中的方法、数值、设计或明确规则 | 新任务的实测或普遍模型能力 |
| A | 作者报告的成功、失败或测量结果 | 本轮独立复验的媒体效果 |
| D | 本轮合同、公式实现、路由和设计夹具 | 案例原文事实 |
| P | 官方协议或技能格式资料 | 新增创作领域经验 |
| I | 本轮实际读取、比较、脚本或文字任务执行 | 未执行的 H3 推理与媒体测量 |
| U | 未取得或未验证 | 默认零值、静音或通过 |

来源索引登记实际阅读范围。全库文件清点与关键词扫描不等于全文阅读；本轮只把真实阅读过的文件或行范围列为方法证据。图片、视频和音频不作为本轮已检查的媒体效果依据。

案例侧重点包括分段音轨、首拍偏移、动作链、相机提前／同步策略、触地切换和生成／编辑的分工。复杂对白排时、变速／定格数值换算及有理数帧率的额外任务属于工程设计与验证，不虚构为已在原案例完整实现。

## 3. 独立使用与职责边界

包内只包含 `SKILL.md`、必要 `scripts/`、按需 `references/` 和可复制 `assets/`。测试、开发报告、校验记录和发布清单置于包外。官方只要求 SKILL.md 及必要元数据；使用三个可选资源目录是本包的需要，不宣称所有技能均必须具有这三个目录。

M7.1、M7.2、M7.3 是一个技能内的三个公开职责入口，分别有最小输入、拥有分区、返回点和验证规则。完整包独立复制后不依赖兄弟模块代码或本仓库私有对话状态；用户提供的兼容公开输入可以替代上游执行结果。父级接受是唯一权威写入路径。

Host 是否扫描 `docs/h3skill/` 由宿主配置决定。仓库交付不代表已安装到个人技能目录，也不表示已测得自动触发率。`agents/openai.yaml` 是可选宿主扩展；本包按 Anthropic 通用格式交付，不以该文件作为必需项。

## 4. 代码与资料许可

本轮实现遵循本仓库既有 MIT 许可，原案例版权归属保存在 `case-source-LICENSE.txt`。合同运行器复用并调整本仓库 M6 的通用机制时，保留项目来源；运行时不导入兄弟包。

MiniMax 官方原文保留原字节和 MiniMax 归属，不将其重标为本项目 MIT 或 Apache-2.0。官方通知及完整既有许可记录随协议来源资料保留。本轮交付是提示词编排和离线时间检查，不涉及模型权重、服务调用或部署授权评估。

Anthropic 和 Agent Skills 校验器、标准快照及各自许可证位于包外 `_standards/`，保持原字节。当前实际规范源也重新读取，并以发布记录登记其版本。

## 5. 可复现范围

Python 3.10+ 标准库运行器执行本包明确实现的合同、数值关系、版本接受和变更影响检查；格式校验使用官方工具并另做非空字段、目录名和资源路由检查。实际行为测试、隔离复制运行和 Agent 文字任务分别保留原始输入与输出。

不从这些检查推导自动音频分析、实测拍点、视频解码、精确 H3 卡点、口型、剪辑执行或 G3/G4 生成效果。审计结果始终说明已检查范围及未确定项。

## 来源入口

- [冻结开发框架](https://github.com/Nuos/H3-h3-prompt-journal/blob/608813b6e51531ac47f860bc384a454a504fe9ff/docs/skillplan/01-core-framework.md)
- [冻结模块化原则](https://github.com/Nuos/H3-h3-prompt-journal/blob/608813b6e51531ac47f860bc384a454a504fe9ff/docs/skillplan/06-modularity-routing-principles.md)
- [本轮案例基线](https://github.com/Nuos/H3-h3-prompt-journal/tree/075fb72797fdca42bc47e38516cf3dbc16f4442d/case-studies)
- [Anthropic 创建标准](https://github.com/anthropics/skills/blob/ca45fc496a3436251f191354091d557da31c15b5/skills/skill-creator/SKILL.md)
- [Agent Skills 规范](https://github.com/agentskills/agentskills/blob/83021e2be457a9b6679148719c1f6074f0ad975e/docs/specification.mdx)
- [MiniMax 基础模式](https://github.com/MiniMax-AI/MiniMax-H3/blob/199b7d0e1fd95e7b3eafa8c15eca692534142427/skills/h3-prompt-writing/references/base-en.txt)
- [MiniMax Ref2VA](https://github.com/MiniMax-AI/MiniMax-H3/blob/199b7d0e1fd95e7b3eafa8c15eca692534142427/skills/h3-prompt-writing/references/ref-en.txt)
