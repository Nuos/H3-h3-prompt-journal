# 固定来源与文件覆盖

- 案例：`2026-08-water-obstacle-variety-show`。
- 固定仓库提交：`91a33376e9ae84d0b9b3a2c1a7f6991d5b9e358e`。
- 创建日期：2026-11-04（America/Los_Angeles）；技能版本：1.0.0。
- 覆盖本案例全部 5 个文本文件和对应的逐案评估；原始媒体未读取、未复制。
- 原文快照未改写；其中媒体链接、本机路径和历史工具命令只是来源记录，不是已提供输入，也不应自动执行。
- 只复制本技能目录即可保留规则、模板、脚本与全部案例文本；实际图片、音频和视频仍须由当前任务提供。

## 读取索引

| 离线原件 | 原仓库路径 | 行数 | 在本技能中的作用 |
|---|---|---:|---|
| [source-README.md](source-README.md) | `case-studies/2026-08-water-obstacle-variety-show/README.md` | 95 | 方法、问题、经验及作者结果；完整阅读。 |
| [source-README.zh-CN.md](source-README.zh-CN.md) | `case-studies/2026-08-water-obstacle-variety-show/README.zh-CN.md` | 278 | 方法译注及原案20秒参数经验；完整阅读。 |
| [source-prompt.md](source-prompt.md) | `case-studies/2026-08-water-obstacle-variety-show/prompt.md` | 165 | 身份、因果链、八段和声场的完整原提示词；完整阅读。 |
| [source-prompt.zh-CN.md](source-prompt.zh-CN.md) | `case-studies/2026-08-water-obstacle-variety-show/prompt.zh-CN.md` | 515 | 全部结构化正文的中译与术语解释；完整阅读。 |
| [source-vocabulary-expanded.zh-CN.md](source-vocabulary-expanded.zh-CN.md) | `case-studies/2026-08-water-obstacle-variety-show/vocabulary-expanded.zh-CN.md` | 105 | 剧情节拍、连续观感与参数边界；完整阅读。 |
| [source-review.md](source-review.md) | `docs/casereview/2026-08-water-obstacle-variety-show.md` | 50 | 完整阅读；容量、试跑参数与事件验收缺口已转为工作流及测试。 |

## 版本与校验

`provenance.json` 保存每个原始文本的字节数、SHA-256、Git blob SHA 和固定版本 URL；用于核对来源漂移。修改技能流程时同步更新对应测试和规则证据。

## 许可与归属

案例原稿及评估来自 Nuos/H3-h3-prompt-journal，原仓库为 MIT，Copyright (c) 2026 LoveRain1997；许可全文随技能保存为 `LICENSE.txt`。本次新编案例流程、模板与检查脚本按仓库许可发布。

Agent Skills 规范/创建指南的原文文档为 CC-BY-4.0，参考实现代码为 Apache-2.0。此技能遵循该格式，不含参考实现作为运行依赖；整批目录的 `_standards` 保存规范及其归属。

MiniMax-H3 提示词规则的离线说明为本次原创功能性转写，官方原文通过固定链接及哈希追溯；没有把官方长篇正文复制或重新标为 MIT。MiniMax 官方资料的 Community License 仍适用于其原件。

## 原始文件链接

- [case-studies/2026-08-water-obstacle-variety-show/README.md](https://github.com/Nuos/H3-h3-prompt-journal/blob/91a33376e9ae84d0b9b3a2c1a7f6991d5b9e358e/case-studies/2026-08-water-obstacle-variety-show/README.md)
- [case-studies/2026-08-water-obstacle-variety-show/README.zh-CN.md](https://github.com/Nuos/H3-h3-prompt-journal/blob/91a33376e9ae84d0b9b3a2c1a7f6991d5b9e358e/case-studies/2026-08-water-obstacle-variety-show/README.zh-CN.md)
- [case-studies/2026-08-water-obstacle-variety-show/prompt.md](https://github.com/Nuos/H3-h3-prompt-journal/blob/91a33376e9ae84d0b9b3a2c1a7f6991d5b9e358e/case-studies/2026-08-water-obstacle-variety-show/prompt.md)
- [case-studies/2026-08-water-obstacle-variety-show/prompt.zh-CN.md](https://github.com/Nuos/H3-h3-prompt-journal/blob/91a33376e9ae84d0b9b3a2c1a7f6991d5b9e358e/case-studies/2026-08-water-obstacle-variety-show/prompt.zh-CN.md)
- [case-studies/2026-08-water-obstacle-variety-show/vocabulary-expanded.zh-CN.md](https://github.com/Nuos/H3-h3-prompt-journal/blob/91a33376e9ae84d0b9b3a2c1a7f6991d5b9e358e/case-studies/2026-08-water-obstacle-variety-show/vocabulary-expanded.zh-CN.md)
- [docs/casereview/2026-08-water-obstacle-variety-show.md](https://github.com/Nuos/H3-h3-prompt-journal/blob/91a33376e9ae84d0b9b3a2c1a7f6991d5b9e358e/docs/casereview/2026-08-water-obstacle-variety-show.md)

## 官方基线

- Agent Skills：[规范固定版本](https://github.com/agentskills/agentskills/blob/83021e2be457a9b6679148719c1f6074f0ad975e/docs/specification.mdx)。
- MiniMax H3：[提示词技能入口固定版本](https://github.com/MiniMax-AI/MiniMax-H3/blob/199b7d0e1fd95e7b3eafa8c15eca692534142427/skills/h3-prompt-writing/SKILL.md)。
- 模式细则、容量与许可链接见 `h3-official.md` 文末。
