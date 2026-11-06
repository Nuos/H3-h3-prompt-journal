# 来源、版本与内容边界

**核心摘要：** 领域方法来自本仓库案例文字；架构来自锁定开发方案；H3 语法来自固定官方协议；技能格式来自 Anthropic 及其指向的 Agent Skills 规范。四类来源分工明确。

**关键结论：** 本轮只新增 M11 实现，既有案例、M1—M10 和锁定方案保持原字节；合成示例不冒充案例实测。

**关键词：** 来源、固定版本、案例证据、技能规范、许可。

**目录导航：** 1. 来源分层；2. 离线材料；3. 许可与归属；4. 完成边界。

## 1. 来源分层

| 来源 | 固定位置／版本 | 用途 |
| --- | --- | --- |
| 用户开发方案 | `docs/skillplan`，基线 `skillplan-v0.1.2-608813b` | M11 和四个子职责、模块化、公开合同、路由和 Gate |
| 当前项目基线 | `586373218a0790382fc5eeed99574d2d58eb8eb8` | 读取 M1—M10 的实现方式和案例文本；不以历史验证代替本轮执行 |
| 案例集合 | `case-studies/`，逐文件索引见 `case-index.json` | 编排方法、差异、失败模式及有限的作者报告 |
| MiniMax H3 官方 | `199b7d0e1fd95e7b3eafa8c15eca692534142427` | 五模式、字段、参考 Label 和声音／镜头语法 |
| Anthropic Skills | `ca45fc496a3436251f191354091d557da31c15b5` | 技能模板、目录惯例和 quick validator |
| Agent Skills 规范 | `83021e2be457a9b6679148719c1f6074f0ad975e` | Frontmatter、命名、渐进加载和可选资源结构 |
| 本轮工程设计 | 本模块 `contract_version: 1.0.0` | 可运行投影、确定性检查、测试夹具及示例参数映射 |

案例原文事实、作者主张、规则提炼和工程设计分别标注。某规则在案例有效不等于所有任务通用，也不等于实际生成成功率已被测量。专业内容不从外部无关教程补造。

## 2. 离线材料与技能结构

两份官方协议全文保存在本技能 `references/`，不依赖在线链接才能编译。`h3-protocol-source.json` 保存来源、精确哈希和本轮核对记录。案例证据使用自足摘要与逐文件哈希；完整原案例保留在仓库。

技能入口只使用 `name` 和 `description` 两项必要元数据，目录名与 name 一致。`scripts/` 承担可重复计算，`references/` 承担按需规则，`assets/` 提供可复制模板；`agents/openai.yaml` 是可选产品展示信息。这些资源目录并非所有技能的强制要求。

发布报告、测试、保护基线、标准快照和验证记录放在技能目录外，避免运行包夹带开发过程文档。格式验证需要同时检查元数据、路径、可移植性和真实用例；官方 quick validator 的通过不是功能或媒体质量证书。

## 3. 许可与归属

`case-source-LICENSE.txt` 保留本仓库案例许可原文。官方 H3 快照保留原作者归属，`h3-NOTICE.txt` 与协议来源记录保留已有许可说明；不将官方文件重新标为本项目许可。

本轮重新获取并逐字节核对了 base-en.txt 和 ref-en.txt。来源记录中的其他 H3 元数据、NOTICE 和历史许可摘录明确标记为继承记录，没有冒充本轮重新审定。Anthropic 与 Agent Skills 的标准快照及许可继续保存在仓库 `_standards/`，没有复制为本模块的创作知识。

## 4. 完成边界

模块是可由 Agent 执行的编译／审计流程，附离线协议、公开合同、确定性辅助程序和样例。它不包含 H3 权重、推理服务器或一个已经连通的 ComfyUI 环境，不因导出任务包就完成实际推理和媒体验收。

运行包内的 profile／模板若标记为模拟，仅用于工程验证。真实执行方仍需提供可定位的工作流版本、字段和素材，才能形成对应任务包。实际缺项按合同报告，不用猜测补全。

## 来源入口

- 开发方案：`docs/skillplan/01-core-framework.md`、`05-workflow-routing.md`、`06-modularity-routing-principles.md`。
- 官方协议：`h3-base-official.txt`、`h3-ref-official.txt`、`h3-protocol-source.json`。
- 案例：`case-evidence.md`、`case-index.json`。
- 技能格式：Anthropic `template/SKILL.md`、`spec/agent-skills-spec.md`，以及 Agent Skills `docs/specification.mdx`；精确来源见仓库 `_standards/source-files.json`。
