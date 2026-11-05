# 固定来源与文件覆盖

- 案例：`2026-10-h3-motion-transfer`。
- 固定仓库提交：`91a33376e9ae84d0b9b3a2c1a7f6991d5b9e358e`。
- 创建日期：2026-11-04（America/Los_Angeles）；技能版本：1.0.0。
- 覆盖本案例全部 3 个文本文件和对应的逐案评估；原始媒体未读取、未复制。
- 原文快照未改写；其中媒体链接、本机路径和历史工具命令只是来源记录，不是已提供输入，也不应自动执行。
- 只复制本技能目录即可保留规则、模板、脚本与全部案例文本；实际图片、音频和视频仍须由当前任务提供。

## 读取索引

| 离线原件 | 原仓库路径 | 行数 | 在本技能中的作用 |
|---|---|---:|---|
| [source-README.md](source-README.md) | `case-studies/2026-10-h3-motion-transfer/README.md` | 54 | 全文读取：三参考分权、作者效果自述、8–9秒经验与ComfyUI摘要，识别其和JSON差异。 |
| [source-h3-motion-transfer-workflow.json](source-h3-motion-transfer-workflow.json) | `case-studies/2026-10-h3-motion-transfer/h3-motion-transfer-workflow.json` | 4982 | 全文完整解析阅读：62节点全部字段、91连线、所有顶层字段和内嵌提示词；compact输出省去空白但没有省略字段，另补读被工具截断的节点137/139/147/153/132/154。 |
| [source-prompt.md](source-prompt.md) | `case-studies/2026-10-h3-motion-transfer/prompt.md` | 586 | 全文读取：586行完整重建正文、首帧权限、初始化顺序、运动提取、音频和八项核查。 |
| [source-review.md](source-review.md) | `docs/casereview/2026-10-h3-motion-transfer.md` | 50 | 全文读取：有效参数、音频端口/旁路、裁剪冲突、模型名不符以及生成前后验收边界。 |

## 版本与校验

`provenance.json` 保存每个原始文本的字节数、SHA-256、Git blob SHA 和固定版本 URL；用于核对来源漂移。修改技能流程时同步更新对应测试和规则证据。

## 许可与归属

案例原稿及评估来自 Nuos/H3-h3-prompt-journal，原仓库为 MIT，Copyright (c) 2026 LoveRain1997；许可全文随技能保存为 `LICENSE.txt`。本次新编案例流程、模板与检查脚本按仓库许可发布。

Agent Skills 规范/创建指南的原文文档为 CC-BY-4.0，参考实现代码为 Apache-2.0。此技能遵循该格式，不含参考实现作为运行依赖；整批目录的 `_standards` 保存规范及其归属。

MiniMax-H3 提示词规则的离线说明为本次原创功能性转写，官方原文通过固定链接及哈希追溯；没有把官方长篇正文复制或重新标为 MIT。MiniMax 官方资料的 Community License 仍适用于其原件。

## 原始文件链接

- [case-studies/2026-10-h3-motion-transfer/README.md](https://github.com/Nuos/H3-h3-prompt-journal/blob/91a33376e9ae84d0b9b3a2c1a7f6991d5b9e358e/case-studies/2026-10-h3-motion-transfer/README.md)
- [case-studies/2026-10-h3-motion-transfer/h3-motion-transfer-workflow.json](https://github.com/Nuos/H3-h3-prompt-journal/blob/91a33376e9ae84d0b9b3a2c1a7f6991d5b9e358e/case-studies/2026-10-h3-motion-transfer/h3-motion-transfer-workflow.json)
- [case-studies/2026-10-h3-motion-transfer/prompt.md](https://github.com/Nuos/H3-h3-prompt-journal/blob/91a33376e9ae84d0b9b3a2c1a7f6991d5b9e358e/case-studies/2026-10-h3-motion-transfer/prompt.md)
- [docs/casereview/2026-10-h3-motion-transfer.md](https://github.com/Nuos/H3-h3-prompt-journal/blob/91a33376e9ae84d0b9b3a2c1a7f6991d5b9e358e/docs/casereview/2026-10-h3-motion-transfer.md)

## 官方基线

- Agent Skills：[规范固定版本](https://github.com/agentskills/agentskills/blob/83021e2be457a9b6679148719c1f6074f0ad975e/docs/specification.mdx)。
- MiniMax H3：[提示词技能入口固定版本](https://github.com/MiniMax-AI/MiniMax-H3/blob/199b7d0e1fd95e7b3eafa8c15eca692534142427/skills/h3-prompt-writing/SKILL.md)。
- 模式细则、容量与许可链接见 `h3-official.md` 文末。
