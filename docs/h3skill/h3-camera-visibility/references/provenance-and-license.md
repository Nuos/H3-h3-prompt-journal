# M5 来源、许可与内容边界

## 核心摘要

本包实现冻结方案的第五核心职责：摄影机、景别、构图、焦点与运镜，输出 `CameraPlan`。创作方法限定为本仓库 `case-studies/` 文本；`docs/skillplan/` 定义开发边界；MiniMax 官方文件定义模型输入协议；Anthropic 和 Agent Skills 文件定义技能结构与创建要求。合同、路由和样例均明确属于实现设计。

**关键结论：** 四个子模块分别提出机位、取景、焦点与运动候选，M5 父级唯一接受。文字编排、确定性合同检查、语义审阅和真实媒体结果分别报告。

**关键词：** M5、CameraPlan、案例边界、固定版本、参考权限、独立调用、来源与许可。

## 1. 固定基线

| 来源 | 固定版本 | 用途 |
| --- | --- | --- |
| 开发方案 | v0.1.2；`608813b6e51531ac47f860bc384a454a504fe9ff` | 十二模块职责、M5 四子模块、HC／LC／MD／RT |
| 冻结控制 | `0ce8b7b1890052bf1d4dd233ef20e68817b38f28` | 冻结成员与完整性规则 |
| 本轮仓库 | `aa4ae291fa8afa0a62fa96ffde26ca25a8db8352` | M1—M4 实现、案例与既有许可 |
| 案例目录树 | `70a8a2a632d633f5d532db23cad99c772dc23026` | 内容边界；逐文件读取范围见索引 |
| MiniMax-H3 | `199b7d0e1fd95e7b3eafa8c15eca692534142427` | 五模式、基础三字段、Ref2VA 六字段与 Label |
| Anthropic Skills | `ca45fc496a3436251f191354091d557da31c15b5` | 官方模板、创建指南与基本验证器 |
| Agent Skills | `83021e2be457a9b6679148719c1f6074f0ad975e` | Anthropic 规范入口指向的字段和目录规范 |

固定版本用于复现，不代表未来最新版。官方逐文件来源、原字节哈希和本轮核验见 [协议来源记录](h3-protocol-source.json) 及包外开发记录。

框架 `01-core-framework.md` 的 M5 小节限定机位、光轴、景别、构图、焦点、视场和运动职责；`06-modularity-routing-principles.md` 第 211 行列出 M5.1—M5.4，第 224—239 行明确 M5.2 可以独立使用外部输入。原文维持冻结，本包在其允许空间内细化合同。

## 2. 证据类别

| 代号 | 意义 | 使用边界 |
| --- | --- | --- |
| F | 可定位的案例文本事实或方案 | 不自动等同生成成功 |
| A | 作者对效果或失败的报告 | 保留报告归属，不当成本轮实测 |
| D | 本轮设计与实现细化 | 合同、示例、测试变体均不冒充案例事实 |
| I | 已执行的工具或 Agent 文字任务 | 仅证明记录中的执行范围 |
| U | 资料不足、媒体缺失或尚未检查 | 保留未验证，不用其他层次的通过代替 |

文件清点与哈希核对不代表语义全文阅读。完整读取、相关段落读取及仅登记分别记录；图片、视频、音频不在本轮文本证据范围内。本包未运行 H3 推理，也不观察未提供的生成片。

现有案例对机位和路径较充分，对完整光学、景深求解及通用影视对白覆盖不足。因此焦点分区交付“清晰对象与范围、保持或变化、相关缺口”的合同和编排要求；不提供未经案例支持的通用焦距、光圈或成功率配方。

## 3. 独立调用与唯一写入

`viewpoints`、`framing`、`focus`、`movements` 分别属于 M5.1—M5.4；M5 父级执行组合接受。独立输入可以来自用户、已有公开计划或其他实现，必须保留来源和版本。跨职责修订通过公开请求，不改写其他模块的内部状态。

完整复制 `h3-camera-visibility/` 即可使用本包的文字规则与 Python 标准库工具。脚本不导入兄弟技能，也不依赖外层测试和发布工具。路由定位、合同检查与 Agent 语义工作分别发生；自然语言任务需要 Agent 读取资源执行，不由 `route` 命令自动完成。

运行包仅含 `SKILL.md`、`scripts/`、`references/`、`assets/`。`SKILL.md` 元数据仅保留 `name` 和 `description`；所有参考资源由入口给出读取条件。测试、开发报告与发布清单保存在包外。`agents/openai.yaml` 是可选宿主配置，本包未将其作为 Anthropic 规范必需项。

## 4. 许可与归属

仓库既有 MIT 许可及 LoveRain1997 版权归属按原文保留于 [案例许可](case-source-LICENSE.txt)。新增项目代码与说明遵循仓库许可；复制独立包时继续保留该文件。

MiniMax 两份协议文本以原字节随包保存，不擅自改标为本项目 MIT 或 Apache 许可。归属见 [H3 通知](h3-NOTICE.txt)，完整官方许可原文和来源记录见 `h3-protocol-source.json`。本包不含模型权重、不调用模型服务。

Anthropic 创建指南、基本验证器和 Agent Skills 规范保留各自许可与固定来源，开发快照位于包外。M5 合同工具部分通用机制参照本仓库 M4 的 MIT 代码，并建立独立 M5 字段和检查；运行时不导入旧包。

## 集中来源

- [冻结方案](https://github.com/Nuos/H3-h3-prompt-journal/tree/608813b6e51531ac47f860bc384a454a504fe9ff/docs/skillplan)。
- [本轮案例基线](https://github.com/Nuos/H3-h3-prompt-journal/tree/aa4ae291fa8afa0a62fa96ffde26ca25a8db8352/case-studies)。
- [前四模块基线](https://github.com/Nuos/H3-h3-prompt-journal/tree/aa4ae291fa8afa0a62fa96ffde26ca25a8db8352/docs/h3skill)。
- [Anthropic 技能仓库](https://github.com/anthropics/skills/tree/ca45fc496a3436251f191354091d557da31c15b5)；[创建指南](https://github.com/anthropics/skills/blob/ca45fc496a3436251f191354091d557da31c15b5/skills/skill-creator/SKILL.md)。
- [Agent Skills 规范](https://github.com/agentskills/agentskills/blob/83021e2be457a9b6679148719c1f6074f0ad975e/docs/specification.mdx)。
- [H3 基础四模式](https://github.com/MiniMax-AI/MiniMax-H3/blob/199b7d0e1fd95e7b3eafa8c15eca692534142427/skills/h3-prompt-writing/references/base-en.txt)；[Ref2VA](https://github.com/MiniMax-AI/MiniMax-H3/blob/199b7d0e1fd95e7b3eafa8c15eca692534142427/skills/h3-prompt-writing/references/ref-en.txt)。
