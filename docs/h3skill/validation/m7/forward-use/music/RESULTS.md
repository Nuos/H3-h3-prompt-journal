# 音乐任务独立前向使用记录

## 可交付结论

已形成 M7.1 时间依据和 M7.2 局部排程，两份提案均通过实际合同检查；结果是 `local_contract: pass`、`overall: unverified`、`numeric_precision: unverified`，不是完整 TimingMap。全部依据来自题目设计条件，未读取媒体、未运行 H3、未向外发布，也未修改技能或运行器。

| 项目 | 当前局部结果 | 限制与后续责任 |
| --- | --- | --- |
| 生成时钟 | 单次 12 秒，局部窗口 `[0,12)` | 原点是生成局部零点，不是音乐首拍；M11 补生成 FPS 和采样方式 |
| 音乐 | 名义 BPM 100；若按恒定名义速度，拍间隔 `60/100=3/5` 秒 | 无音频和首拍偏移，绝对拍点未知；M2/M12 协调补资料，M6 确认音乐及相位依据 |
| actionA | `[0.5,2.5)`，持续 2 秒，保留不可删除或缩短的约束 | 起点是否落拍未知；具体动作语义和接触时刻未提供，不能用起点替代动作强调点 |
| 摄影机 | 固定镜头 `[0,12)`，覆盖 actionA 全部 2 秒 | 作为独立 M5 事件，不按每拍重新启动 |
| 后续动作 | 未设计 | M4 补 `[2.5,12)`；题目也未给 `[0,0.5)` 动作，均不推断静止或空白 |
| 编辑时钟 | 计划 30 FPS | 未给采样模式、编辑放置、速度和跨域映射；由 M9 补充，不借用为生成 FPS |
| 切镜 | 当前提案未新增 cut 事件 | M9 已给单次生成且无新增真实切镜要求 |

不能接受“首拍从 0 秒开始、动作与相机每拍同时启动”的建议作为已知事实：BPM 只确定名义间隔，不给首拍相位；动作与摄影机已有各自窗口。actionA 的两秒等于 `10/3` 个名义拍间隔，这不构成缩短它的理由。秒域包含关系已能表达，而帧号、帧精确同步、实际音乐对齐和完整跨域 TimingMap 均尚未建立。

## 实际输入与检查记录

最终使用的输入和结果：

- M7.1：[Request](run-001/request-m7-1.json)、[Proposal](run-001/proposal-m7-1.json)、[check stdout](run-001/m7-1-check.stdout.txt)。
- M7.2：[Request](run-003/request-m7-2.json)、[Proposal](run-003/proposal-m7-2.json)、[check stdout](run-003/m7-2-check.stdout.txt)。
- 原始任务：[original-task.txt](original-task.txt)。

| 尝试 | 实际调用 | 退出码 | 结果与处理 |
| --- | --- | --- | --- |
| run-001 | M7.1 route、check | 0、0 | 局部合同通过，保留显式未知 |
| run-001 | M7.2 route、check | 1、1 | `contract_shape`：误把事件 ReadonlyRecord 结构用于父状态 readonly_projection |
| run-002 | M7.2 route、check | 1、1 | 删除多余 projection 后暴露 `unresolved_source`：m4_design、m5_design 未在 sources 中登记 |
| run-003 | M7.2 route、check | 0、0 | 将外部上下文及绑定的 source_id 对齐到已有 user_design，版本保持一致；通过，未知仍保留 |

共 **8 次实际 route/check 调用，4 次成功、4 次失败**。另实际查看顶层及 check 子命令帮助各 1 次，共 10 次运行器调用；未调用 accept、convert、quantize 或 map。各尝试的 `commands.json` 保存完整命令参数、实际工作目录、退出码、输入 SHA-256 及对应 stdout/stderr 文件名。所有失败输入均原样保存，未被最终版本覆盖：

- [run-001 命令记录](run-001/commands.json)
- [run-002 命令记录](run-002/commands.json)
- [run-003 命令记录](run-003/commands.json)
- [初始读取及顶层帮助记录](read-and-help/commands.json)
- [check 帮助的既有调用记录](check-help-observed.json)

运行器原始 stdout 的 trace 还保留 call_id、开始/完成时间、合同/注册表摘要及输入摘要。stderr 均为空。`run_validation.py` 是首次尝试的可移植重放脚本，会有意复现首次输入错误；它以 `__file__` 定位仓库，拒绝覆盖已有证据。最终产物以上述 run-001/M7.1 与 run-003/M7.2 为准。

## 使用障碍与验证边界

首次按 SKILL.md 读取合同指南时文件尚未落盘，真实 `cat` 失败保存在 [initial-missing-guide-failure.json](initial-missing-guide-failure.json)。后来指南已提供并完成阅读，故未形成最终阻断。公开指南明确区分 ReadonlyRecord 与父状态 readonly_projection，并要求 ExternalContext.source_id 登记；本次两次输入错误属于使用者适配失误，依其诊断和指南修正后可继续，无需修改合同。

实际验证范围是：公开 CLI 能路由当前局部输入；Request/Proposal 形状、上下文保真和来源引用可检查；秒域动作窗口与固定相机覆盖能通过当前合同约束；缺首拍、FPS、编辑起点等信息会保留 unverified。检查没有确认设计来源的真实性、音乐实测节拍、动作自然度、H3 执行结果或完整 G0–G4 质量，也没有完成 M7 父状态接收和 M7.3 映射量化。未读取其他验证结果、开发报告或 tests/m7/ 预期答案。

依据：任务原文，以及技能公开的 `SKILL.md`、`references/time-bases.md`、`references/event-scheduling.md`、`references/audit-and-handoff.md`、`references/contracts.json`、`references/contract-guide.md` 和 assets 示例。当前未发现仍然阻断本题局部交付的工具错误。
