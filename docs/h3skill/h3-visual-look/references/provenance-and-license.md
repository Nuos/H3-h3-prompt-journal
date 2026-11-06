# M10 来源、许可与内容边界

## 1. 来源分工

| 来源 | 固定版本 | 使用范围 |
| --- | --- | --- |
| 冻结开发方案 | `skillplan-v0.1.2-608813b`；提交 `608813b6e51531ac47f860bc384a454a504fe9ff` | M10 职责、四个子模块、LookPlan、单写者、最小合同及跨模块边界 |
| 案例与既有工程基线 | `Nuos/H3-h3-prompt-journal@c8ec1a4e5162ec5179ed9bec99d2f46a437ae67c` | 领域证据只来自 `case-studies/`；M1—M9 提供兼容的工程接口风格 |
| Anthropic Skills | `ca45fc496a3436251f191354091d557da31c15b5` | 技能目录、frontmatter、渐进加载、创建与格式验证方式 |
| Agent Skills 规范 | `83021e2be457a9b6679148719c1f6074f0ad975e` | Anthropic 规范入口所指向的公开格式，使用固定快照 |
| MiniMax-H3 官方协议 | `199b7d0e1fd95e7b3eafa8c15eca692534142427` | 五种输入模式、字段、Label、风格开场与参考保留规则 |

本轮重新获取两份 MiniMax 官方提示词文件，返回的完整 UTF-8 正文与既有精确快照相同，远端 blob SHA 也一致；复制件由发布核验再次核对 SHA-256 与 Git blob。其他官方文件元数据、NOTICE 与许可协议记录保留为历史材料，不声称本轮重新获取。详细记录见 [h3-protocol-source.json](h3-protocol-source.json)。固定版本不意味着宣称其永久是最新版本。

Anthropic／Agent Skills 的六个标准快照已在本轮按固定官方树与本地字节、SHA-256、Git blob 复核，记录在包外发布验证中。官方标准只提供创建规则，不能为领域方法或模型效果背书。

## 2. 实际内容边界与阅读范围

[case-index.json](case-index.json) 登记 29 个案例目录、98 个文本文件：目录内 97 个，另有根层词汇文件 1 个。来源分析选取 6 案例的 9 文件，2 个全文、7 个部分阅读，范围合计 809 行；其余 89 文件仅作身份盘点，不宣称全文研究。阅读记录没有继承前序模块的完成声明。

重点证据覆盖独立生成与公共风格展开、图像属性分权、局部暖光与冷中性基调、湿发毛巾和水线泡沫、服装与面纱边界、动作观看优先级及源文授权矛盾。逐条原文定位、限制与四分区推导见 [case-evidence.md](case-evidence.md)。

F 为原文事实，A 为作者经验或生成现象报告，D 为本模块设计，U 为未知。JSON 示例、版本接受、路由命令及示例剧情属于 D，不冒充案例实测或 H3 原生 API。本轮图片查看、音视频解码、H3 推理均为 0；独立 Agent 文字使用另有输入、产物和读取记录。

## 3. 可复制的运行包

包根为 `SKILL.md` 与按需使用的 `scripts/`、`references/`、`assets/`。资源目录不是所有技能的强制要求；四子模块是独立可调用职责，并非四个必须分拆安装的技能。`agents/openai.yaml` 是可选宿主扩展，不属于本次 Anthropic 格式的必需项。

运行器只依赖 Python 3.10+ 标准库及随包资料，不读取兄弟技能目录、案例原目录或远端仓库。公开来源路径供追溯使用，不构成隐含运行依赖。官方格式检查使用包外已有验证器及 PyYAML，属于开发检查依赖。

交付位置按用户指定的 GitHub 仓库，不进行个人技能安装。开发报告、测试、发布清单和执行记录位于包外，技能本身可单目录复制。

## 4. 许可与归属

本轮代码与专业文档沿用仓库既有 MIT 许可。案例来源许可完整保存在 [case-source-LICENSE.txt](case-source-LICENSE.txt)，保留原版权归属；复用既有工程方式同样保留项目来源。

MiniMax 官方文本保留原文、出处及归属，不重新标为本项目 MIT 或 Anthropic Apache-2.0。[h3-NOTICE.txt](h3-NOTICE.txt) 保留已有通知；来源 JSON 保留此前官方 README 的声明及完整协议文本记录。该协议是历史网页抽取记录，未冒称为原始 LICENSE 字节快照。本任务不分发模型权重。

Anthropic 和 Agent Skills 的标准快照、官方验证器及对应许可继续位于包外 `_standards/`，不改原字节。

## 5. 可复查边界

本轮可以复查来源身份、读取范围、合同关系、引用权限、版本与失效、CLI、父接受及独立目录运行。Agent 的文字方案审阅与程序检查分别记录。它们不能证明真实打光、像素调色、物理材质、实际遮挡、无闪烁、无风格漂移、H3 模型输出或宿主自动触发率。

## 固定来源

- [冻结核心框架](https://github.com/Nuos/H3-h3-prompt-journal/blob/608813b6e51531ac47f860bc384a454a504fe9ff/docs/skillplan/01-core-framework.md)
- [冻结模块化与路由原则](https://github.com/Nuos/H3-h3-prompt-journal/blob/608813b6e51531ac47f860bc384a454a504fe9ff/docs/skillplan/06-modularity-routing-principles.md)
- [本轮案例基线](https://github.com/Nuos/H3-h3-prompt-journal/tree/c8ec1a4e5162ec5179ed9bec99d2f46a437ae67c/case-studies)
- [Anthropic 创建指南](https://github.com/anthropics/skills/blob/ca45fc496a3436251f191354091d557da31c15b5/skills/skill-creator/SKILL.md)
- [Agent Skills 规范](https://github.com/agentskills/agentskills/blob/83021e2be457a9b6679148719c1f6074f0ad975e/docs/specification.mdx)
- [MiniMax 基础四模式](https://github.com/MiniMax-AI/MiniMax-H3/blob/199b7d0e1fd95e7b3eafa8c15eca692534142427/skills/h3-prompt-writing/references/base-en.txt)
- [MiniMax Ref2VA](https://github.com/MiniMax-AI/MiniMax-H3/blob/199b7d0e1fd95e7b3eafa8c15eca692534142427/skills/h3-prompt-writing/references/ref-en.txt)
