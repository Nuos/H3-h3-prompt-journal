# 三人恶作剧、定格笑点与 COS 换皮：案例简评

## 核心结论

**适合作为“逆向因果重建＋仅换外观”的主流程候选。**它提供竞争假设、歧义窗口加密采样、声画对账、画外行动者识别及换皮依赖检查，方法论强于普通成片描述。README 还链接了配套 `video-to-h3-prompt` skill；但本案例文本不能单独证明该外部 skill 的当前实现与回归稳定性。[S1：14—57]

- 源目录：`case-studies/2026-09-three-person-prank-freeze-gag-cos-swap/`
- 全文范围：5 个文本文件；仅评估文字记录，不复核原视频或外部 skill 仓库。
- 源提交：`5056f46e123aef52c7aac9d51a03ce7a5dae53c2`
- 评估日期：2026-11-03。
- 方法论等级：**M3**；skill 就绪等级：**S2**；建议定位：**主流程候选**。

## 1. 模块构成

| 模块 | 内容与用途 |
|---|---|
| 反推取证 | 歧义窗口 4—8fps 采样、0.5s RMS 包络、BPM 误检检查 |
| 因果骨架 | 挑衅→含水准备→骑手干扰→反噬→定格，三轮递进 |
| 主体与物件状态 | 两名可见角色和画外骑手；面罩开合、头部朝向、杯瓶归属 |
| 表演/编辑/声音 | 基础手持长镜头与三次后期定格分层；无配乐，保留现场声及后期音效 |
| 换皮契约 | 固定时间、动作、运镜与声音；仅换外观及受影响的材料物理 |

这些模块能解释“谁先做了什么、导致谁改变”，也避免把剪辑定格写成人体突然停止。[S1—S5]

## 2. 多维简评

| 维度 | 判断 |
|---|---|
| 标准性方法论 | **较强。**含反推假设的淘汰、音画交叉验证、功能道具相容性检查与换皮范围；可转为 SOP。[S1：22—55] |
| 输入输出 | 源视频用于前期反推，最终 H3 提示词为无参考图 T2VA；两阶段输入不能混淆。 |
| 时序/状态 | 面罩 4.8s 放下、7.2s 掀起、9.5s 转头时继续掀起，明确了笑点的必要状态。[S3：37—63] |
| 迁移能力 | 因果表、定格四元组和仅换皮边界可复用；特定人物、服装及三次笑点不应成为通用限制。 |
| 验证证据 | 抽帧、RMS 和结果描述属于作者记录；目录未附候选假设表、采样日志或替换差异表，无法独立复核反推过程。 |

## 3. skill 化判断与最小落地步骤

建议形成“证据事件表→因果状态表→分层提示词→换皮差异检查”四步输出。把人物/道具依赖、定格入点/时长/覆盖/恢复方式和声音类别做成字段。若使用配套外部 skill，应先锁定版本与接口，再验证本案例可复现；当前评级仅覆盖本目录文本。[S1：35—57]

每次换皮须检查面罩等功能道具能否保留，同时确保动作时间表和声音结构没有被改写。生成成功与否应通过画外施动者、干扰先于反应、面罩状态及定格数量等指标验收。

## 4. 主要缺口与优先级

1. **P1：统一字段清单。**README 称“14-field prompt”，最终正文实际有 12 个顶层字段；应以显式 schema 列表校正，避免封装时误判缺失字段。[S1：61；S3：13—95]
2. **P1：精确化编辑时基。**末事件为 15.3s，所以“约 15 秒”不是严格 15.000s；首个定格从 6.2 到恢复 6.8s，也只是约半秒。应给出最终总时长、帧率下的取整规则，并说明时间戳是否已经包含定格时长。[S3：45—79、83；S5：101]
3. **P1：补可复核的过程产物。**保存竞争假设、关键干扰事件的帧位、声音峰值对应关系，以及换皮前后差异表。4—8fps 是案例抽样策略，遇更短动作需继续加密，不能作为普遍充分性保证。[S1：16—24、53—57]

## 5. 全部文本依据

- **[S1]** [README.md](https://github.com/Nuos/H3-h3-prompt-journal/blob/5056f46e123aef52c7aac9d51a03ce7a5dae53c2/case-studies/2026-09-three-person-prank-freeze-gag-cos-swap/README.md)：全文 1—91 行；取证、因果、换皮方法与外部 skill 链接。
- **[S2]** [README.zh-CN.md](https://github.com/Nuos/H3-h3-prompt-journal/blob/5056f46e123aef52c7aac9d51a03ce7a5dae53c2/case-studies/2026-09-three-person-prank-freeze-gag-cos-swap/README.zh-CN.md)：全文 1—305 行；案例译注。
- **[S3]** [prompt.md](https://github.com/Nuos/H3-h3-prompt-journal/blob/5056f46e123aef52c7aac9d51a03ce7a5dae53c2/case-studies/2026-09-three-person-prank-freeze-gag-cos-swap/prompt.md)：全文 1—95 行；完整提示词和事件时间轴。
- **[S4]** [prompt.zh-CN.md](https://github.com/Nuos/H3-h3-prompt-journal/blob/5056f46e123aef52c7aac9d51a03ce7a5dae53c2/case-studies/2026-09-three-person-prank-freeze-gag-cos-swap/prompt.zh-CN.md)：全文 1—628 行；全部英文主体的逐段译注。
- **[S5]** [vocabulary-expanded.zh-CN.md](https://github.com/Nuos/H3-h3-prompt-journal/blob/5056f46e123aef52c7aac9d51a03ce7a5dae53c2/case-studies/2026-09-three-person-prank-freeze-gag-cos-swap/vocabulary-expanded.zh-CN.md)：全文 1—109 行；术语、声音层次与 15.3s 边界。
