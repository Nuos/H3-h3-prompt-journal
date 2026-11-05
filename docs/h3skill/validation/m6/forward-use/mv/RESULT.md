# MV：M6.3 定向审计结果

## 结论与完成范围

本次完成的是**主线程引导后的离线定向审计，非盲测**。以真实任务说明为来源，从技能提供的 M6.3 独立调用样例复制并替换生成请求与提案，实际执行了 2 次业务 CLI 调用：`route` 1 次、携带原请求的 `check` 1 次。路由成功；检查按预期阻断。**最终提案不可接受，未生成已接受状态或最终 SoundPlan，也未执行 accept。**

保留的矛盾是：用户要求 AUDIO-MASTER 完整 1:1 作为完整最终音轨，又要求新增两个清楚脚步声和海浪声。提案忠实保留 `use_strategy=fully_copy`、`whole_source=yes` 与 `additional_audio=yes`，没有自行换成 `partially_copy`，也没有删去音效要求。

所有本次写入均在本目录内；没有修改技能包、调用媒体服务、生成媒体或推送。

## 实际 CLI 结果

运行目录：`trial/20261105T160026.744863Z/`。

| 调用 | 退出码 | 实际结果 | 能说明什么 |
| --- | ---: | --- | --- |
| `route request.json` | 0 | `checked_draft`；`ready_for_call`；M6.3 路由；`invocation=not_invoked` | 请求具备此独立调用的最低输入，返回 M6.3 资源和写入范围。没有调用其他代理或媒体服务。 |
| `check proposal.json --request request.json` | 1 | `rejected`；`fully_copy_conflict`，blocking=true | 正确阻断完整最终音轨复制与新增声音的冲突。 |

两次 stderr 均为空。`check` 同时给出 4 条未核验诊断：`audio_selection` 与 `beat_plan` 各 1 条 `explicit_unknown`，以及此次未构造 `vocal_events`、`effects` 上下文导致的 2 条 `soundtrack_context_unknown`。这不是实测音频质量或完整跨模块通过的证明。

本次没有业务命令调用失败后修补重跑的过程；唯一非零退出是上述真实的、预期的合同拒绝，原样保留。前期只进行了技能阅读与 CLI 帮助查询，未有业务审计产物，随后主线程要求收敛为本次两条命令的定向审计。帮助查询不计入这 2 次业务调用，也不冒充已保存的验证记录。

运行脚本 SHA-256：`7d4173070df5b34d3f77e240bee83c53f9f5eaf9909bd77e97d14c3c652462ee`。完整命令参数、时间、原始输入文件摘要和来源摘要在运行目录的 `command-manifest.json`；stdout、stderr 和退出码分别独立保存。

## 输入与证据的处理

原始任务全文保存为运行目录内 `actual-request.txt`，来源定位仍指向 `../mv-task.txt`。没有沿用样例中的 13.793 秒、audioA、样例 URI 或样例台词。

AUDIO-MASTER 仅是用户登记的素材标识，`available=false`。真实资产版本、时长、源窗口、首拍偏移及实测依据均明确为 Unknown。12 秒只作为目标视频时长，不作为音轨时长。当前合同的 AudioAsset 要求数值型时长，因此没有伪造 `duration_seconds=0` 或其他数值；把未完备的登记放在可保留 Unknown 的外部 `reference_context.values.audio_registration`，`audio_selection` 整体保持 Unknown。

“约 120 BPM”只能构成文字节奏意向，不能推出已对齐的动作秒数；在理想恒定 120 BPM 假设下可计算 0.5 秒节拍间隔，但本提案没有把这个假设写成实测节拍或卡点。歌词仅是 ROLE-B 的 ACT-GESTURE 语义触发线索；歌词原文、批准文本和时间均未知，没有把 ROLE-B 变成歌手或新增口型要求。

`MV-SCOPE-12S` 仅满足独立提案的内部适用范围绑定，不代表已经确定镜头切分、H3 最终编号或模式。此次没有构造 M6.1、M6.2、M6.4 的正式分区；外部上下文中的未知词句是审计数据，不能宣称已经通过正式 VocalEvent 字段校验。

## 后续必要输入与负责模块

| 待决问题或缺失输入 | 负责模块与后续动作 |
| --- | --- |
| 完整最终音轨与新增声层的要求冲突 | 用户经 M1/M2 确认取舍，M6.3 更新策略。可选方向：保留整个最终音轨并撤回新增声层；或明确授权新增声层并改用允许混合的策略。两项都未获同意，当前不能替用户选定。 |
| AUDIO-MASTER 可播放文件、版本、时长和可用性 | M2 登记与核对素材；M6.3 据此填写音频选择。目标 12 秒是否与完整源音轨时长兼容也待核验。 |
| 源窗口及全源使用范围 | M2/M6.3 明确用户授权范围；M9 确认最终声音实现，不能默认裁切、循环、变速仍满足原 1:1 要求。 |
| 经核对的歌词文本及所在位置 | M2 提供素材/转写，M6.2 处理语义歌词事件，M7 对照实际信号定位。未取得文本必须保持 Unknown，不能 NotApplicable。 |
| 首拍偏移、准确拍点、歌词锚点和每个动作的精确卡点 | M7 基于可播放音频及动作资料测量并排时；约 120 BPM 不足以完成。 |
| 两个脚步对应的动作依据 | M4 核对 ACT-STEP 与第二个脚步事件；当前只给出 ROLE-A 的一次落地，不能补造动作。M6.4 在需求冲突解除后设计脚步与海浪层，M7 排时。 |
| 角色音色资料 | M2/M6.1 保留缺口；目前并无新增角色发声要求，歌词提示本身不触发角色演唱或音色克隆。 |
| 生成模式及最终 H3 标签 | M11 确认协议模式与标签；动作参考视频不自动授权使用其中的声音。 |
| 最终媒体验证 | 有实际生成音视频后交 M12 审核；本次没有实际音频、口型、混音或视频质量证据。 |

## 复现与文件

在仓库根目录运行：

```bash
python -B docs/h3skill/validation/m6/forward-use/mv/reproduce.py
```

每次执行在本目录 `trial/` 下创建带时间戳的新目录，保留旧输入和输出。脚本从当前样例复制后替换为本任务数据，实际运行两条 CLI；`check` 的预期非零退出码被记录，不会删除其输出。

首次记录包含：`request.json`、`proposal.json`、`actual-request.txt`、`command-manifest.json`、`route.stdout.txt`、`route.stderr.txt`、`route.exit.txt`、`check.stdout.txt`、`check.stderr.txt`、`check.exit.txt`。
