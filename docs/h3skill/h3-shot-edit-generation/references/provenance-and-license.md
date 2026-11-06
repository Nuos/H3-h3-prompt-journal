# M9 来源、许可与内容边界

## 1. 三类来源各负其责

| 来源 | 固定版本 | 本包使用范围 |
| --- | --- | --- |
| 冻结开发方案 | `skillplan-v0.1.2-608813b`，内容提交 `608813b6e51531ac47f860bc384a454a504fe9ff` | M9 职责、三个子模块、五种单位、单写者与 M7／M8／M11／M12 边界 |
| 本轮案例与既有实现 | `Nuos/H3-h3-prompt-journal@36987c56ade886aacfb166a21d6560925c97c330` | 领域方法仅取 `case-studies/` 文本；既有 M1—M8 仅提供工程合同风格与兼容接口参考 |
| Anthropic Skills | `ca45fc496a3436251f191354091d557da31c15b5` | 技能目录、元数据、渐进加载、实用资源与创建／验证流程 |
| Agent Skills 规范 | `83021e2be457a9b6679148719c1f6074f0ad975e` | 由 Anthropic 规范入口指向的公开格式，使用仓库已固定快照 |
| MiniMax-H3 官方协议 | `199b7d0e1fd95e7b3eafa8c15eca692534142427` | 五种输入模式、字段、参考 Label、真实 Shot 和声音语法 |

本轮通过 GitHub 插件重新获取 Anthropic 主分支指向，确认其与上述固定提交一致，并阅读其 `skills/skill-creator/SKILL.md`。MiniMax 的 base-en.txt 与 ref-en.txt 按固定提交重新获取，返回 UTF-8 正文与既有精确快照逐值相等，之后按原字节复制到本包；复制件再由发布核验器检查 SHA-256 和 Git blob。未重新获取的许可及其他文件元数据保留为历史记录，不称作本轮重新验证。

领域规则、官方协议和工程设计不能互相冒充证据。合同字段、命令行、路由、版本接受和示例 JSON 属于本轮 D 类实现，不是 H3 原生 API，也不表示案例作者已经实现了这些程序。

## 2. 实际阅读范围

清点 29 个案例目录中的 98 个文本文件，保存文件身份、哈希、字节数及行数。本轮语义研究全文阅读八个十月案例的 11 份文本，共 4,082 行、223,523 字节；其余 87 份仅清点。没有继承前序模块的阅读声明，也没有宣称全库关键词扫描。具体回执和来源见 `case-index.json`。

重点方法及冲突见 `case-evidence.md`：古风舞的策略选择、剑舞后期桥接与任务自包含、运镜库中的条件切镜规则、身份舞的动作中匹配、水线镜头的同镜阶段、白凤的双生成与交接缺口、触地硬切与单镜标签冲突、右入展示中的姿态到重新入画。

F 是文本事实，A 是作者效果或观察报告，D 是有依据的设计，U 是未知或未验证。来源完整性检查只证明文件身份与范围。图片、音频、视频观察数均为 0，H3 推理数为 0。

## 3. 可独立复制的运行包

运行包包含 `SKILL.md`、`scripts/`、`references/`、`assets/`。三个资源目录按本模块需要提供，不是声称 Agent Skills 要求所有技能都具有它们。子模块以公开合同独立使用，不强制拆成三个独立安装包。`agents/openai.yaml` 属于可选宿主扩展，本包保持已有 Anthropic 通用布局。

包内脚本仅依赖 Python 3.10+ 标准库与随包资源；官方格式检查使用包外既有 Anthropic 校验器及 PyYAML，属于开发验证依赖。运行时不读取兄弟模块、外部案例目录或远端仓库。案例路径和固定来源链接用来追溯，不是隐藏运行依赖。

本轮按用户指定的 GitHub 交付位置开发，不在个人技能目录另行安装。总入口与测试、开发报告、发布清单和实际验证记录置于包外，避免把过程资料当作提示词知识加载。

## 4. 许可与归属

本轮代码和专业文档遵循仓库既有 MIT 许可；案例来源的完整许可保存在 `case-source-LICENSE.txt`。复用既有工程方式保留其项目归属。

MiniMax 官方文档保留原文、原归属和来源记录，不重新标为本项目 MIT 或 Anthropic Apache-2.0。`h3-NOTICE.txt` 保留原通知；`h3-protocol-source.json` 保留官方 README 的许可声明及此前取得的完整协议文本记录。该许可记录明确其获取形式为网页抽取，不声称为逐字节原始 LICENSE 快照。本任务不分发模型权重，也不提供法律判断。

Anthropic 和 Agent Skills 的标准快照、官方校验器及其许可仍放在包外 `_standards/`，原字节不变。

## 5. 可复现范围

可复核的项目包括来源字节与行界、合同与引用、公开 CLI、组合接受、失效范围及单包运行。Agent 文字试用另留实际输入与产物。验证不包括真实源视频切点检测、音频测量、最优裁剪点、接缝感知、H3 生成质量、宿主自动触发率或全流程关卡完成。

## 固定来源

- [冻结核心框架](https://github.com/Nuos/H3-h3-prompt-journal/blob/608813b6e51531ac47f860bc384a454a504fe9ff/docs/skillplan/01-core-framework.md)
- [冻结模块化与路由原则](https://github.com/Nuos/H3-h3-prompt-journal/blob/608813b6e51531ac47f860bc384a454a504fe9ff/docs/skillplan/06-modularity-routing-principles.md)
- [本轮案例基线](https://github.com/Nuos/H3-h3-prompt-journal/tree/36987c56ade886aacfb166a21d6560925c97c330/case-studies)
- [Anthropic 创作指南](https://github.com/anthropics/skills/blob/ca45fc496a3436251f191354091d557da31c15b5/skills/skill-creator/SKILL.md)
- [Agent Skills 规范](https://github.com/agentskills/agentskills/blob/83021e2be457a9b6679148719c1f6074f0ad975e/docs/specification.mdx)
- [MiniMax 基础四模式原文](https://github.com/MiniMax-AI/MiniMax-H3/blob/199b7d0e1fd95e7b3eafa8c15eca692534142427/skills/h3-prompt-writing/references/base-en.txt)
- [MiniMax Ref2VA 原文](https://github.com/MiniMax-AI/MiniMax-H3/blob/199b7d0e1fd95e7b3eafa8c15eca692534142427/skills/h3-prompt-writing/references/ref-en.txt)
