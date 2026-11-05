# 固定来源与文件覆盖

- 案例：`2026-08-three-person-orbital-long-take`。
- 固定仓库提交：`91a33376e9ae84d0b9b3a2c1a7f6991d5b9e358e`。
- 创建日期：2026-11-04（America/Los_Angeles）；技能版本：1.0.0。
- 覆盖本案例全部 5 个文本文件和对应的逐案评估；原始媒体未读取、未复制。
- 原文快照未改写；其中媒体链接、本机路径和历史工具命令只是来源记录，不是已提供输入，也不应自动执行。
- 只复制本技能目录即可保留规则、模板、脚本与全部案例文本；实际图片、音频和视频仍须由当前任务提供。

## 读取索引

| 离线原件 | 原仓库路径 | 行数 | 在本技能中的作用 |
|---|---|---:|---|
| [source-README.md](source-README.md) | `case-studies/2026-08-three-person-orbital-long-take/README.md` | 74 | 全文74行：三图身份与环境分工、遮挡接力方法、README的360度和20秒结果陈述、6秒三人加约2秒结尾。 |
| [source-README.zh-CN.md](source-README.zh-CN.md) | `case-studies/2026-08-three-person-orbital-long-take/README.zh-CN.md` | 194 | 全文194行：README全部逐段中文译注；核对它保留作者成功与证明措辞，并不构成独立实验，识别three-quarter旧译。 |
| [source-prompt.md](source-prompt.md) | `case-studies/2026-08-three-person-orbital-long-take/prompt.md` | 1413 | 全文1413行：参考权限、固定三人站位、严格可见性、上下上环绕、第二接力高度、竞争时间表、物理路径、微动作、短后拉及负向约束。 |
| [source-prompt.zh-CN.md](source-prompt.zh-CN.md) | `case-studies/2026-08-three-person-orbital-long-take/prompt.zh-CN.md` | 1599 | 全文1599行：192段完整中译与原文回读，核对全部时点、相机中心重置与连续性、低位和肩背遮挡、最终群像及证明措辞。 |
| [source-vocabulary-expanded.zh-CN.md](source-vocabulary-expanded.zh-CN.md) | `case-studies/2026-08-three-person-orbital-long-take/vocabulary-expanded.zh-CN.md` | 107 | 全文107行：50项词汇、在场／可见／揭示、环绕／摇摄／滚转、身体遮挡与相机位置、最终同框证据边界和非接口命名。 |
| [source-review.md](source-review.md) | `docs/casereview/2026-08-three-person-orbital-long-take.md` | 50 | 全文50行：专项子技能范围、环绕定义与时间预算两个P0、站位视场净空联合预检、重复生成证据缺失。 |

## 版本与校验

`provenance.json` 保存每个原始文本的字节数、SHA-256、Git blob SHA 和固定版本 URL；用于核对来源漂移。修改技能流程时同步更新对应测试和规则证据。

## 许可与归属

案例原稿及评估来自 Nuos/H3-h3-prompt-journal，原仓库为 MIT，Copyright (c) 2026 LoveRain1997；许可全文随技能保存为 `LICENSE.txt`。本次新编案例流程、模板与检查脚本按仓库许可发布。

Agent Skills 规范/创建指南的原文文档为 CC-BY-4.0，参考实现代码为 Apache-2.0。此技能遵循该格式，不含参考实现作为运行依赖；整批目录的 `_standards` 保存规范及其归属。

MiniMax-H3 提示词规则的离线说明为本次原创功能性转写，官方原文通过固定链接及哈希追溯；没有把官方长篇正文复制或重新标为 MIT。MiniMax 官方资料的 Community License 仍适用于其原件。

## 原始文件链接

- [case-studies/2026-08-three-person-orbital-long-take/README.md](https://github.com/Nuos/H3-h3-prompt-journal/blob/91a33376e9ae84d0b9b3a2c1a7f6991d5b9e358e/case-studies/2026-08-three-person-orbital-long-take/README.md)
- [case-studies/2026-08-three-person-orbital-long-take/README.zh-CN.md](https://github.com/Nuos/H3-h3-prompt-journal/blob/91a33376e9ae84d0b9b3a2c1a7f6991d5b9e358e/case-studies/2026-08-three-person-orbital-long-take/README.zh-CN.md)
- [case-studies/2026-08-three-person-orbital-long-take/prompt.md](https://github.com/Nuos/H3-h3-prompt-journal/blob/91a33376e9ae84d0b9b3a2c1a7f6991d5b9e358e/case-studies/2026-08-three-person-orbital-long-take/prompt.md)
- [case-studies/2026-08-three-person-orbital-long-take/prompt.zh-CN.md](https://github.com/Nuos/H3-h3-prompt-journal/blob/91a33376e9ae84d0b9b3a2c1a7f6991d5b9e358e/case-studies/2026-08-three-person-orbital-long-take/prompt.zh-CN.md)
- [case-studies/2026-08-three-person-orbital-long-take/vocabulary-expanded.zh-CN.md](https://github.com/Nuos/H3-h3-prompt-journal/blob/91a33376e9ae84d0b9b3a2c1a7f6991d5b9e358e/case-studies/2026-08-three-person-orbital-long-take/vocabulary-expanded.zh-CN.md)
- [docs/casereview/2026-08-three-person-orbital-long-take.md](https://github.com/Nuos/H3-h3-prompt-journal/blob/91a33376e9ae84d0b9b3a2c1a7f6991d5b9e358e/docs/casereview/2026-08-three-person-orbital-long-take.md)

## 官方基线

- Agent Skills：[规范固定版本](https://github.com/agentskills/agentskills/blob/83021e2be457a9b6679148719c1f6074f0ad975e/docs/specification.mdx)。
- MiniMax H3：[提示词技能入口固定版本](https://github.com/MiniMax-AI/MiniMax-H3/blob/199b7d0e1fd95e7b3eafa8c15eca692534142427/skills/h3-prompt-writing/SKILL.md)。
- 模式细则、容量与许可链接见 `h3-official.md` 文末。
