# 双人对话声音计划：实际离线试用结果

## 结果及适用范围

本次按主线程收窄后的流程完成定向文字试用，不称严格盲测。使用本仓库 `h3-sound-music-dialogue` 技能，从公开 assets 模板任务化替换并执行真实离线 CLI；直接用户输入作为本轮设计数据，没有新收录案例或媒体观察。

最终组合结果为 `final-state.json`：M6 所有的 SoundPlan，version **1**，status **draft**，工具 disposition **checked_draft**，`validation.local_contract=pass`，`validation.overall=unverified`。含 4 个声源、3 个语音事件、1 个无配乐记录、3 个环境/动作声音事件，5 个 open warning。父接受只说明本地合同可以组合，不能证明声音、动作或视频效果。

## 可交付声音安排

| 顺序 | 事件 | 发声角色与稳定声源 | 原文（逐字及标点保留） | 归属与口型 |
|---|---|---|---|---|
| 1 | VOCAL-01 / spoken_dialogue | ENTITY-CLERK / SOUND-CLERK | 先放在桌上，别松手。 | SHOT-A；店员画面内开口，lip_sync=required |
| 2 | VOCAL-02 / spoken_dialogue | ENTITY-VISITOR / SOUND-VISITOR | 好，我接住了。 | SHOT-B；顾客是否画面内未指定，lip_sync=unknown |
| 3 | VOCAL-03 / voiceover | ENTITY-CLERK / SOUND-CLERK | 这一次，我记住了。 | **暂挂 SHOT-B，尚未确认**；店员仍在画面中但不开口，lip_sync=not_required |

三句只确定上述先后，不写绝对时刻、片长、停顿长度或与动作同步点。三句都是新设计语音，原文和 approved_text 完全相同，没有台词改写；台词无需跨切。店员对白与旁白共用 SOUND-CLERK，没有凭空增加另一位叙述者。

VOICE-REF 仅绑定顾客音色参考。当前无可听文件，媒体版本未知；没有声称已听取或确认质地、口音、声域，没有复制参考原信号或复演参考中台词。

MUSIC-NONE 的 `use_strategy=none` 表示用户明确无画外配乐。ROOM-A、ROOM-B 保持低声室内底声跨两镜连续，音量要求以语音可辨识为设计目标，未写实际测量值。EFFECT-PLACE 绑定 ACT-PLACE 的盒子与桌面轻接触声；保留底声与接触声，所以没有创建 whole_track_silence。

## 两项显式设计假设及交接

**VOCAL-03 和 EFFECT-PLACE 暂挂 SHOT-B，并非用户已确定的镜头事实。** 当前合同要求每条事件具有字符串 shot_id，因此草稿使用现有镜头作暂存归属；来源 `draft_assumption` 的 kind 为 hypothesis，相应问题保持 open。这不能授权下游直接把暂挂值当成确定镜头。确认后应通过新提案重绑定相关声源、事件及外部引用。

- M7：确定旁白和 ACT-PLACE 镜头归属、三句实际时长/起止、接触时刻及语音与动作的关系；本计划未制作绝对时间轴。
- M9：安排 SHOT-A → SHOT-B 底声接缝和必要的声音衔接；台词无需跨切。旁白暂挂和接触暂挂仍须确认。
- 外部动作责任方：用户转述的 ACT-PLACE 是“顾客将盒子放在桌面并释放”，对白出现“别松手”“接住了”，二者关系需确认。声音计划只处理接触，不把释放认定为已验证动作，也不改写动作计划。
- 素材责任方：提供 VOICE-REF 可听文件及版本，核验参考角色、授权和可用性；提供外部动作资料 URL、版本及场景空间证据。当前外部描述仅来自用户转述，没有声称完成外部检索。
- M11：若后续制作完整 H3 正文，再依据稳定实体与声源分配标签；本轮没有生成完整提示词。

真实口型、实际音频可用性/质量、来源真实性、语义意图、节拍证据真实性、生成视频质量及全局 G0–G4 均未核验。没有实际媒体、音色听评、音视频生成、真实服务调用或推送。

## 实际调用与修订历史

合计 **10 次 M6 CLI 调用：6 次返回 0，4 次返回 1**。此数只统计 `m6_contract.py` 的实际进程调用，不把文件读写或报告生成算作验证调用。

| 阶段 | 实际命令 | 结果 |
|---|---|---|
| v1 | 父 route × 1 | pass / unverified |
| v1 | 四子 check × 4 | M6.3 通过；M6.1、M6.2、M6.4 返回 contract_shape |
| v1 | accept × 1 | 拒绝，尚未生成组合状态 |
| v2 | 受影响的 M6.1、M6.2、M6.4 check × 3 | 全部 pass / unverified |
| v2 | accept × 1 | pass / unverified；输出 version 1 draft |

首轮失败源于本次提案的输入形状错误：环境与物件声源的 `voice_requirement` 写成了 `not_applicable`，但合同的 Fact 只接受 KnownFact 或 Unknown。v2 将两者改为有设计来源的 KnownFact“非人声源：不设置人声音色或发声要求”，同步修订请求上下文，并使用新的请求/提案 ID；M6.3 保留原已通过提案。**没有修复或修改运行代码、合同或技能包。** 未增加额外场景、负例或测试框架。

运行脚本 SHA-256 在调用前后均为：

`7d4173070df5b34d3f77e240bee83c53f9f5eaf9909bd77e97d14c3c652462ee`

原始 v1 请求、提案、失败 stdout/stderr，以及 v2 请求、提案和接受输出全部保留。`run-summary.json` 汇总全部命令、退出码及日志位置。

## 文件与复现

- `actual-request.txt`：实际用户任务原文。
- `request-m6.json`、`request-m6-*.json`、`requests.json`：首轮父/子请求。
- `proposal-m6-*-v1.json`、`proposal-batch-v1.json`、`state-empty.json`：首轮提案和初始状态。
- `request-m6-*-v2.json`、`requests-v2.json`、`proposal-m6-*-v2.json`、`proposal-batch-v2.json`：最小输入修订；M6.3 使用 v1。
- `run-20261105T160210375010Z/`：首轮 6 次真实 CLI 输入命令及原始输出。
- `repair-20261105T160241613373Z/`：修订后 4 次真实 CLI 命令及原始输出。
- `final-state.json`：最终组合声音草稿；`run-summary.json`：完整调用汇总。
- `run_trial.py`、`revise_and_finish.py`、`reproduce.sh`：可复现脚本。脚本只在本目录写入文件，使用 `python -B`，不调用真实媒体服务。

从本目录运行 `bash reproduce.sh` 可重现首轮真实输入错误及最小修订流程，生成新时间戳日志目录。旧日志目录保留；顶层同名提案/摘要会按相同设计重建。若只复跑最终有效组合，可执行：

```bash
python -B ../../../../h3-sound-music-dialogue/scripts/m6_contract.py accept state-empty.json proposal-batch-v2.json --requests requests-v2.json
```

技能资源实际读取范围包括 SKILL.md、四子域说明、audit-and-handoff、公开合同/模块注册与合同指南、H3 标签映射说明及 assets 请求/提案/初始状态模板；不依赖其他核心模块执行结果。本试用是可组合草稿验证，未把局部合同成功报告为媒体成功。
