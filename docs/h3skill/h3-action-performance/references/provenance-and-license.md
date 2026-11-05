# M4 来源、许可与内容边界

## 核心摘要

本包将冻结方案的第四核心职责实现为可独立读取、调用和检查的技能。**创作领域依据来自本仓库 `case-studies/` 文本；开发边界来自冻结 `docs/skillplan/`；H3 官方资料只界定输入协议；Anthropic 与 Agent Skills 资料只界定技能格式和创建要求。** 工程合同和示例夹具是本轮设计，不是新增案例事实。

**关键结论：** M4 负责动作语义并输出 ActionPlan。M4.1、M4.2、M4.3 分别维护事件与前提、机制与过程、结果与接续；父模块唯一接受子提案。结构检查、专业审阅与真实媒体验收分别报告。

**关键词：** M4、固定版本、证据边界、动作语义、独立使用、领域规则、许可归属。

## 1. 固定基线

| 来源 | 固定版本 | 用途 |
| --- | --- | --- |
| 开发方案 | v0.1.2；`608813b6e51531ac47f860bc384a454a504fe9ff` | 十二模块职责、ActionPlan、M4 三子模块及 HC／LC／MD／RT 强制原则 |
| 冻结控制 | `0ce8b7b1890052bf1d4dd233ef20e68817b38f28` | 冻结成员、变更边界、校验基线 |
| 本轮仓库 | `545a99015cfa00a6f07ee05d1d0f21e09d89d46c` | M1—M3 已完成实现、现行案例文本和原许可 |
| 案例目录树 | `70a8a2a632d633f5d532db23cad99c772dc23026` | 可用案例集合；实际读取范围由案例索引逐项登记 |
| MiniMax-H3 | `199b7d0e1fd95e7b3eafa8c15eca692534142427` | 五模式、基础三字段／Ref2VA 六字段、四类 Label 与声音／镜头格式 |
| Anthropic Skills | `ca45fc496a3436251f191354091d557da31c15b5` | 官方模板、创建指南和基础格式验证器 |
| Agent Skills | `83021e2be457a9b6679148719c1f6074f0ad975e` | Anthropic 仓库指向的元数据、命名及可选目录规范 |

固定提交用于复现，不代表未来最新版。官方源文件和许可的详细版本、Git blob、SHA-256 及本轮核对状态见 `h3-protocol-source.json` 和外层开发记录。本包只保存运行时需要的协议快照，不依赖外层规范快照才能运行。

冻结框架 `01-core-framework.md` 第 176—189 行定义 M4 的输入、输出、越权边界与通过条件；`06-modularity-routing-principles.md` 第 210 行定义三个子模块，第 103—127 行规定最小公共合同，第 249—281 行规定递归验收。`05-workflow-routing.md` 第 143 行定义 M4 进入与回传，第 265—269 行定义戏剧、交互、音乐与专项动作分支。原文保持冻结；本包实现细化不能反向改写基线。

## 2. 证据等级与能力边界

| 类别 | 意义 | M4 使用方式 |
| --- | --- | --- |
| F 来源事实 | 原文本可定位的陈述 | 提炼动作结构及原作用域，不改写为普遍成功定律 |
| A 作者报告 | 作者对效果、失败或修订的陈述 | 保留报告归属，不当成本轮视频观察 |
| D 设计细化 | 为实现冻结职责作出的工程或创作设计 | 合同、样例、接口与测试变体明确标识设计性质 |
| I 实现与执行 | 本轮代码、命令与实际 Agent 文字使用记录 | 只证明报告中的执行范围；I 不表示“推断” |
| U 未验证 | 尚无输入、实际观察或足够证据 | 保留未知；不把文本通过升级为生成质量 |

案例索引区分完整读取、局部定位和仅登记，不能用文件哈希证明已理解其内容。图片、视频和音频不在本轮领域文本读取证据中。动作的可执行表达和物理求解不同：本包不计算人体动力学、碰撞、接触力、运动捕捉或可见性投影。

已有案例以舞蹈、剑舞、换装、交互和动作迁移为主。戏剧表演使用冻结框架的目标／触发／反应接口与案例中可定位的因果链，不声称已覆盖完整对白、复杂心理表演或多场景长剧的真实生成回归。

规则必须保留适用范围：固定人数、动作密度、转身预算、固定机位、无口型、禁慢走等均不成为全局默认。源文冲突须保留原位置与裁决依据，不能只挑一条有利表述。用户指定的动作或结果仍须追踪，不能以简化模板为由删除。

## 3. 所有权和独立复制

M4 定义动作发生的语义；M3 定义空间，M5 定义观看，M6 定义声音，M7 定义绝对排时，M8 管理权威计划状态，M9 定义镜头与编辑，M11 编译实际模式／Label／参数，M12 保存实际观察和阶段审计。写有交接点不表示其他模块已经实现或已执行。

独立输入可来自用户、外部兼容工具或已有公开计划；不要求全部上游先运行，不导入兄弟技能脚本或私有字段。只读投影和来源必须原样对照，三个专业分区通过父接受产生唯一新版本。仅复制完整 `h3-action-performance/` 目录即可使用其中的文字规则与标准库离线工具；包外测试、审阅和发布清单是开发证据。

运行包只含 `SKILL.md`、`scripts/`、`references/`、`assets/`。`SKILL.md` 保留必需 `name`、`description` 元数据与核心流程；详细规则通过明确读取条件单跳路由。开发报告、测试记录和发布说明保存在包外。`agents/openai.yaml` 为可选产品配置，本包未将它作为 Anthropic 格式的必需条件。

## 4. 许可和归属

本仓库根许可为 MIT，版权归属行保留 LoveRain1997。新增代码和项目说明按仓库既有许可交付；随包 `case-source-LICENSE.txt` 保留原许可，以支持独立复制后的归属说明。

`h3-base-official.txt` 与 `h3-ref-official.txt` 为 MiniMax 官方文档原字节快照，不添加标题或擅自改标 MIT／Apache-2.0。MiniMax 归属通知在 `h3-NOTICE.txt`，官方完整许可原文和获取记录保存在 `h3-protocol-source.json`；许可适用范围以所附原文为准。本包不包含模型权重，也不执行模型或外部付费服务。

Anthropic 与 Agent Skills 的模板、验证器及规范保留各自许可。开发用快照位于外层 `_standards/` 或本轮验证记录，均不是独立运行包的依赖；不将第三方格式规范伪装成本项目的创作案例。

## 5. 集中来源

- [冻结开发方案](https://github.com/Nuos/H3-h3-prompt-journal/tree/608813b6e51531ac47f860bc384a454a504fe9ff/docs/skillplan)。
- [冻结控制](https://github.com/Nuos/H3-h3-prompt-journal/tree/0ce8b7b1890052bf1d4dd233ef20e68817b38f28/docs/skillplan)。
- [本轮案例基线](https://github.com/Nuos/H3-h3-prompt-journal/tree/545a99015cfa00a6f07ee05d1d0f21e09d89d46c/case-studies)。
- [M1—M3 读取基线](https://github.com/Nuos/H3-h3-prompt-journal/tree/545a99015cfa00a6f07ee05d1d0f21e09d89d46c/docs/h3skill)。
- [Anthropic 技能仓库](https://github.com/anthropics/skills/tree/ca45fc496a3436251f191354091d557da31c15b5)；[技能创建指南](https://github.com/anthropics/skills/blob/ca45fc496a3436251f191354091d557da31c15b5/skills/skill-creator/SKILL.md)。
- [Agent Skills 规范](https://github.com/agentskills/agentskills/blob/83021e2be457a9b6679148719c1f6074f0ad975e/docs/specification.mdx)。
- [MiniMax-H3 提示词入口](https://github.com/MiniMax-AI/MiniMax-H3/blob/199b7d0e1fd95e7b3eafa8c15eca692534142427/skills/h3-prompt-writing/SKILL.md)；[基础四模式](https://github.com/MiniMax-AI/MiniMax-H3/blob/199b7d0e1fd95e7b3eafa8c15eca692534142427/skills/h3-prompt-writing/references/base-en.txt)；[Ref2VA](https://github.com/MiniMax-AI/MiniMax-H3/blob/199b7d0e1fd95e7b3eafa8c15eca692534142427/skills/h3-prompt-writing/references/ref-en.txt)。
