# M3 来源、许可与内容边界

## 核心摘要

本技能的领域方法来自本仓库 `case-studies/` 文本，职责和架构来自冻结的 `docs/skillplan/`。MiniMax 官方资料用于确认输入模式、提示词字段和参考 Label；Anthropic 与 Agent Skills 资料用于技能组织和验证。三类依据分别记录，不能把格式规范当作视频创作案例，或把案例作者报告当作本轮实测。

**关键结论：** M3 接受并维护空间计划，向其他模块提交条件或修改请求。参考权限属于 M2，动作语义属于 M4，摄影方案属于 M5，绝对排时属于 M7，跨镜状态属于 M8，最终模式与 Label 编译属于 M11。任何自动检查结论都必须限定在实际执行范围内。

**关键词：** 固定版本、案例边界、空间计划、来源证据、许可归属、未验证范围。

## 1. 固定来源

| 来源 | 固定提交或标识 | 用途 |
| --- | --- | --- |
| 开发方案 | v0.1.2；`608813b6e51531ac47f860bc384a454a504fe9ff` | M3 职责、三个子模块、`SpatialPlan` 归属与四项架构原则 |
| 冻结控制 | `0ce8b7b1890052bf1d4dd233ef20e68817b38f28` | 冻结清单、变更范围及历史基线 |
| 本轮仓库基线 | `91e6ed0b09d17e13cf5f58cccfe0df588c5b1d8a` | 读取已完成的 M1、M2 公开接口及当前案例文本；不修改其原运行包 |
| 案例树 | `70a8a2a632d633f5d532db23cad99c772dc23026` | 本轮可使用的案例集合；单文件范围及哈希由案例索引登记 |
| Anthropic Skills | `ca45fc496a3436251f191354091d557da31c15b5` | 技能模板、创建规范、官方基础验证器 |
| Agent Skills 规范 | `83021e2be457a9b6679148719c1f6074f0ad975e` | Anthropic 仓库指向的技能元数据、命名和目录标准 |
| MiniMax-H3 | `199b7d0e1fd95e7b3eafa8c15eca692534142427` | T2VA／I2VA／FL2VA／L2VA／Ref2VA、三／六字段、四类参考 Label |

开发框架中 M3 原文位于 `01-core-framework.md` 第 161–174 行；共享对象及唯一写入位于第 319–360 行。三个子模块位于 `06-modularity-routing-principles.md` 第 209 行；该文件第 73–99 行和第 249–281 行规定独立接口、路由及验收。原始文档保持冻结，新实现细化记录在本包及其外层交付记录中。

固定提交用于重现，不代表未来最新版。2026-11-05 核对时，H3 和 Anthropic 两仓库 `main` 分别与上表固定提交一致；核对记录只对其检查时点有效。官方来源文件、Git blob、SHA-256、行数及许可原文随 `h3-protocol-source.json` 保留。

## 2. 领域边界与证据解释

案例中固定人数、左右槽位、禁止交叉、特定景别、旋转预算或遮挡策略，仅在原任务条件内保留。冻结框架明确不设统一人数上限，不禁止一切过中线或遮挡，不把参考图左右顺序视为永久站位。可推广的是明确坐标、稳定身份、可执行路线、交互对象和证据边界的做法，不能省去原规则的适用条件。

| 证据类别 | 含义 | 在 M3 中的解释 |
| --- | --- | --- |
| F：来源事实 | 原文件中可定位的文字 | 案例写明的入画方向、队形、接触或遮挡要求；并不表示本轮看过媒体 |
| A：作者报告 | 作者对生成结果的陈述 | 保留报告归属，本轮未观看或测量该媒体，不能转成实测成功率 |
| D：设计细化 | 为落实冻结框架形成的实现选择 | 空间合同、父模块接受路径、坐标声明、版本和路由规则；不冒称案例作者原有实现 |
| I：实现与执行 | 已实现代码及实际执行记录 | 结构／引用／版本检查和 Agent 文字使用结果；检查范围以记录为准 |
| U：未验证 | 尚无支持结论的输入或执行 | 未读取的真实媒体、实际身体可达性、镜头遮挡效果、模型输出和成片质量 |

这五类用于说明证据性质，不替代合同中的状态枚举。I 表示实现与执行，不能解释成“推断”。计划中的坐标、距离或占位尺寸若来自创作设定，需保留设计身份；不能以数字形式伪装为实测值。仅有二维文字几何或路线检查，不能推出真实人体、道具、摄影机均无碰撞。

本包只实现其已声明的 M3 范围。独立输入可由用户、兼容外部工具或已有 M1／M2 产物提供；不要求先运行其他模块，也不把兄弟技能的内部文件作为隐藏依赖。M4—M12 的未实现功能仍通过公开交接或未决项表达，不能因已写出 H3 字段映射而宣称完整提示词编译、H3 推理或媒体验收已完成。

## 3. 归属与再分发

本仓库根许可为 MIT，版权行归属 LoveRain1997。本包新增代码和项目说明按仓库既有许可交付；独立复制技能时保留 `case-source-LICENSE.txt` 及随附的来源记录。

`h3-base-official.txt` 和 `h3-ref-official.txt` 是 MiniMax 官方文档的原字节快照，归 MiniMax 原作者。本包不将它们重新标为本项目原创、MIT 或 Apache-2.0。完整官方许可及来源随 `h3-protocol-source.json` 保存，归属通知保留在 `h3-NOTICE.txt`；许可范围以所附原文为准。本包没有模型权重，也不执行模型或外部付费服务。

Anthropic 模板、基础验证器和 Agent Skills 规范沿用各自许可，开发用快照位于交付外层 `_standards/`；M3 运行包不依赖该目录。`SKILL.md` 提供元数据和核心流程，`references/` 提供按需规则与来源，`scripts/` 提供声明的确定性工具，`assets/` 提供可复制输入模板。`agents/openai.yaml` 属于可选产品配置，不属于 Anthropic 最小目录的必需文件。

## 4. 集中来源

- [冻结开发方案](https://github.com/Nuos/H3-h3-prompt-journal/tree/608813b6e51531ac47f860bc384a454a504fe9ff/docs/skillplan)。
- [冻结控制清单](https://github.com/Nuos/H3-h3-prompt-journal/blob/0ce8b7b1890052bf1d4dd233ef20e68817b38f28/docs/skillplan/baseline-lock.json)。
- [本轮案例基线](https://github.com/Nuos/H3-h3-prompt-journal/tree/91e6ed0b09d17e13cf5f58cccfe0df588c5b1d8a/case-studies)。
- [已完成 M1](https://github.com/Nuos/H3-h3-prompt-journal/tree/91e6ed0b09d17e13cf5f58cccfe0df588c5b1d8a/docs/h3skill/h3-work-intent)；[已完成 M2](https://github.com/Nuos/H3-h3-prompt-journal/tree/91e6ed0b09d17e13cf5f58cccfe0df588c5b1d8a/docs/h3skill/h3-asset-reference)。
- [仓库 MIT 许可](https://github.com/Nuos/H3-h3-prompt-journal/blob/91e6ed0b09d17e13cf5f58cccfe0df588c5b1d8a/LICENSE)。
- [Anthropic 技能模板](https://github.com/anthropics/skills/blob/ca45fc496a3436251f191354091d557da31c15b5/template/SKILL.md)；[技能创建指南](https://github.com/anthropics/skills/blob/ca45fc496a3436251f191354091d557da31c15b5/skills/skill-creator/SKILL.md)。
- [Agent Skills 格式规范](https://github.com/agentskills/agentskills/blob/83021e2be457a9b6679148719c1f6074f0ad975e/docs/specification.mdx)。
- [MiniMax-H3 提示词入口](https://github.com/MiniMax-AI/MiniMax-H3/blob/199b7d0e1fd95e7b3eafa8c15eca692534142427/skills/h3-prompt-writing/SKILL.md)；[基础模式原文](https://github.com/MiniMax-AI/MiniMax-H3/blob/199b7d0e1fd95e7b3eafa8c15eca692534142427/skills/h3-prompt-writing/references/base-en.txt)；[Ref2VA 原文](https://github.com/MiniMax-AI/MiniMax-H3/blob/199b7d0e1fd95e7b3eafa8c15eca692534142427/skills/h3-prompt-writing/references/ref-en.txt)。
