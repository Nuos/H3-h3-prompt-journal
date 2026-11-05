# 固定来源与文件覆盖

- 案例：`2026-09-snap-lock-editorial-reveal`。
- 固定仓库提交：`91a33376e9ae84d0b9b3a2c1a7f6991d5b9e358e`。
- 创建日期：2026-11-04（America/Los_Angeles）；技能版本：1.0.0。
- 覆盖本案例全部 4 个文本文件和对应的逐案评估；原始媒体未读取、未复制。
- 原文快照未改写；其中媒体链接、本机路径和历史工具命令只是来源记录，不是已提供输入，也不应自动执行。
- 只复制本技能目录即可保留规则、模板、脚本与全部案例文本；实际图片、音频和视频仍须由当前任务提供。

## 读取索引

| 离线原件 | 原仓库路径 | 行数 | 在本技能中的作用 |
|---|---|---:|---|
| [source-README.md](source-README.md) | `case-studies/2026-09-snap-lock-editorial-reveal/README.md` | 132 | 全文读取：采样误判、两态方法、原5.30秒时间预算及作者成片/反推自述。 |
| [source-prompt.md](source-prompt.md) | `case-studies/2026-09-snap-lock-editorial-reveal/prompt.md` | 571 | 全文读取：571行英文执行稿、静态禁止项、短burst、三冲击、闭眼与两次roll逻辑。 |
| [source-prompt.zh-CN.md](source-prompt.zh-CN.md) | `case-studies/2026-09-snap-lock-editorial-reveal/prompt.zh-CN.md` | 278 | 全文读取：278行中文教学改写及术语，发现其加减速/身体连接/附加音效不等同英文。 |
| [source-vocabulary-expanded.zh-CN.md](source-vocabulary-expanded.zh-CN.md) | `case-studies/2026-09-snap-lock-editorial-reveal/vocabulary-expanded.zh-CN.md` | 107 | 全文读取：50项词义/句法、相机动作主语、hard lock与freeze区别、角度/帧预算校读。 |
| [source-review.md](source-review.md) | `docs/casereview/2026-09-snap-lock-editorial-reveal.md` | 50 | 全文读取：版本分歧、roll累积、极短冲击和源片机制证据边界。 |

## 版本与校验

`provenance.json` 保存每个原始文本的字节数、SHA-256、Git blob SHA 和固定版本 URL；用于核对来源漂移。修改技能流程时同步更新对应测试和规则证据。

## 许可与归属

案例原稿及评估来自 Nuos/H3-h3-prompt-journal，原仓库为 MIT，Copyright (c) 2026 LoveRain1997；许可全文随技能保存为 `LICENSE.txt`。本次新编案例流程、模板与检查脚本按仓库许可发布。

Agent Skills 规范/创建指南的原文文档为 CC-BY-4.0，参考实现代码为 Apache-2.0。此技能遵循该格式，不含参考实现作为运行依赖；整批目录的 `_standards` 保存规范及其归属。

MiniMax-H3 提示词规则的离线说明为本次原创功能性转写，官方原文通过固定链接及哈希追溯；没有把官方长篇正文复制或重新标为 MIT。MiniMax 官方资料的 Community License 仍适用于其原件。

## 原始文件链接

- [case-studies/2026-09-snap-lock-editorial-reveal/README.md](https://github.com/Nuos/H3-h3-prompt-journal/blob/91a33376e9ae84d0b9b3a2c1a7f6991d5b9e358e/case-studies/2026-09-snap-lock-editorial-reveal/README.md)
- [case-studies/2026-09-snap-lock-editorial-reveal/prompt.md](https://github.com/Nuos/H3-h3-prompt-journal/blob/91a33376e9ae84d0b9b3a2c1a7f6991d5b9e358e/case-studies/2026-09-snap-lock-editorial-reveal/prompt.md)
- [case-studies/2026-09-snap-lock-editorial-reveal/prompt.zh-CN.md](https://github.com/Nuos/H3-h3-prompt-journal/blob/91a33376e9ae84d0b9b3a2c1a7f6991d5b9e358e/case-studies/2026-09-snap-lock-editorial-reveal/prompt.zh-CN.md)
- [case-studies/2026-09-snap-lock-editorial-reveal/vocabulary-expanded.zh-CN.md](https://github.com/Nuos/H3-h3-prompt-journal/blob/91a33376e9ae84d0b9b3a2c1a7f6991d5b9e358e/case-studies/2026-09-snap-lock-editorial-reveal/vocabulary-expanded.zh-CN.md)
- [docs/casereview/2026-09-snap-lock-editorial-reveal.md](https://github.com/Nuos/H3-h3-prompt-journal/blob/91a33376e9ae84d0b9b3a2c1a7f6991d5b9e358e/docs/casereview/2026-09-snap-lock-editorial-reveal.md)

## 官方基线

- Agent Skills：[规范固定版本](https://github.com/agentskills/agentskills/blob/83021e2be457a9b6679148719c1f6074f0ad975e/docs/specification.mdx)。
- MiniMax H3：[提示词技能入口固定版本](https://github.com/MiniMax-AI/MiniMax-H3/blob/199b7d0e1fd95e7b3eafa8c15eca692534142427/skills/h3-prompt-writing/SKILL.md)。
- 模式细则、容量与许可链接见 `h3-official.md` 文末。
