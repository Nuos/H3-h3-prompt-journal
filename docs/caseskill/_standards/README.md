# 官方规范基线与归属

## 核心结论

本集合按 Agent Skills 格式标准创建，每个案例对应一个技能目录。格式必需项、官方组织建议、H3 提示词协议和本项目补齐的检查规则分别记录，不把建议说成格式强制要求。

## 规范快照

| 资料 | 固定提交 | 本地内容与用途 |
|---|---|---|
| Agent Skills 规范/创建指南 | `83021e2be457a9b6679148719c1f6074f0ad975e` | `agent-skills/` 内为未经修改的官方文档快照，包括格式、创建、脚本、描述和评估指南。 |
| 官方 skills-ref 0.1.0 | 同上 | `skills-ref/` 内为未经修改的参考实现，用于元数据验证；不是技能运行依赖。 |
| MiniMax H3 提示词资料 | `199b7d0e1fd95e7b3eafa8c15eca692534142427` | 来源清单保留官方文件 URL、Git blob SHA 与 SHA-256；各技能的 `references/h3-official.md` 是本次原创离线操作说明。 |

来源清单也列出调研时读取的上游文件；并不表示每份原文都被随集合再分发。H3 完整指南没有复制进本集合。官方基线的核对日期是 2026-11-04（America/Los_Angeles）。

## Agent Skills 格式必需项

1. 技能是独立目录，根部有 `SKILL.md`，其 YAML frontmatter 后是 Markdown 指令。
2. `name` 非空、1–64 字符，与目录同名；使用小写字母、数字和连字符，不以连字符开头/结尾，不连续使用连字符。
3. `description` 非空、最多 1024 字符，写明能力与具体触发语境。本集合仅使用 name/description 两个顶层字段。
4. license、compatibility、metadata、allowed-tools 是可选字段。scripts、references、assets 和额外目录也不是格式必需项。

本集合采用小于 500 行的精简入口、按需加载的参考资料、真实输出模板、可运行的确定性检查脚本和 3 类代表任务。这些是工程设计与官方最佳实践的采用记录。`agents/openai.yaml` 是可选客户端展示配置；存在此文件不意味着所有客户端已自动发现或安装技能。

## 从案例到技能的操作标准

完整读取每案全部文本及其评估，记录来源哈希；抽取可迁移步骤、输入职责、状态关系、异常和修复；把旧稿歧义转为明确裁决；使用当前 H3 协议封装最终提示词；用静态检查与代表任务发现缺口。原案角色、固定段数、镜头焦距、舞种容量和作者成功叙述不直接升级为模型硬能力。

以 `case-studies/` 直接子目录为案例单位，所以库型案例也各自有一个技能。库型技能可以只输出可组合的动作/机位组件；需要完整提示词时才启用生成端字段封装。没有设置全体技能统一的人数上限。

## 验证边界

`skills-ref validate` 核对元数据及名称等格式规则，不认证 H3 编排效果。本项目额外检查案例覆盖、正文资源路径、原文哈希、模板合同、脚本运行和典型输入失败。人工检查记录仍需真实内容审核；本次没有运行 H3 或测量视频成功率。

## 许可

- Agent Skills 官方文档归属 agentskills/agentskills 贡献者，使用 CC-BY-4.0；原许可证随 `agent-skills/LICENSE` 保存，复制内容未改写。
- skills-ref 参考实现使用 Apache-2.0；原许可证随 `skills-ref/LICENSE` 保存，复制内容未改写。
- 案例资料保留原仓库的 MIT 许可与 Copyright (c) 2026 LoveRain1997；各独立技能含 `LICENSE.txt`。
- MiniMax 官方资料使用其原始 Community License；本集合没有将官方原件重新许可为 MIT，也不把本技能宣称为 MiniMax 官方发布。

## 官方来源

- [Agent Skills 格式规范](https://github.com/agentskills/agentskills/blob/83021e2be457a9b6679148719c1f6074f0ad975e/docs/specification.mdx)
- [Agent Skills 创建最佳实践](https://github.com/agentskills/agentskills/blob/83021e2be457a9b6679148719c1f6074f0ad975e/docs/skill-creation/best-practices.mdx)
- [Agent Skills 评估指南](https://github.com/agentskills/agentskills/blob/83021e2be457a9b6679148719c1f6074f0ad975e/docs/skill-creation/evaluating-skills.mdx)
- [MiniMax H3 提示词入口](https://github.com/MiniMax-AI/MiniMax-H3/blob/199b7d0e1fd95e7b3eafa8c15eca692534142427/skills/h3-prompt-writing/SKILL.md)
- [MiniMax H3 基础模式指南](https://github.com/MiniMax-AI/MiniMax-H3/blob/199b7d0e1fd95e7b3eafa8c15eca692534142427/skills/h3-prompt-writing/references/base-en.txt)
- [MiniMax H3 Ref2VA 指南](https://github.com/MiniMax-AI/MiniMax-H3/blob/199b7d0e1fd95e7b3eafa8c15eca692534142427/skills/h3-prompt-writing/references/ref-en.txt)
