# M7 前向使用：时间映射与接触后切换

## 实际完成

仅依据本任务给定的计划数据和技能包公开文档、公开示例、CLI，构造了一个独立 `M7.3` Request 与 Proposal，保留 M4、M5、M9 与外部生成任务上下文。M9 的 `editDecision1` 对应 `source_to_work`；`editDecision2` 对应 `generation_to_edit`。`work_to_generation` 绑定外部任务的局部起点，不冒充新增 M9 决策。未修改技能包或运行器，未读取开发报告、其他验证结果或 `tests/m7/` 预期答案。

实际调用运行器 **12 次**：help 1 次、route 1 次、check 1 次、map 6 次、quantize 1 次、convert 2 次，全部退出码为 0，所有 stderr 为空。Request/Proposal 首次检查即通过本地合同检查，无输入修订或重试。完整 argv、工作目录、退出码和输出文件索引在 `commands.json`；每次 stdout/stderr 单独保存。`run-validation.py` 根据自身位置找到仓库，可在另一检出路径复跑。

`03-check.stdout.txt` 的实际结果为 `local_contract=pass`、`disposition=checked_draft`、`overall=unverified`、`numeric_precision=unverified`。工作域帧率、完整工作域时长、生成端帧率、完整编辑域时长按未知输入保留；未知项未阻断已知区间的秒数映射。未调用 `accept`，未形成已接受的父状态。

## 时间映射与结果

三段已定映射：

- `work = 10 + (source − 2) / 2`，源覆盖 `[2,8)`，作品覆盖 `[10,13)`。
- `generation = work − 10`，生成局部覆盖 `[0,3)`。
- `edit = 5 + generation`，成片覆盖 `[5,8)`。

覆盖终点是区间边界，不被当作最后一个已知媒体采样点。结果单位均为秒：

| 事件 | sourceA | workA | gen02 局部 | editA |
|---|---:|---:|---:|---:|
| M4 contactA | 4.125 = 33/8 | 11.0625 = 177/16 | 1.0625 = 17/16 | 6.0625 = 97/16 |
| M5 cameraReadyA | 3.5 = 7/2 | 10.75 = 43/4 | 0.75 = 3/4 | 5.75 = 23/4 |

6 次 `map` 的实际输出与表中结果一致；2 次 `convert` 给出源域零基帧号 contactA=99、cameraReadyA=84。`cameraReadyA` 表示到位时刻，未被改写为相机开始运动。

作品域到位提前量：`11.0625 − 10.75 = 5/16 = 0.3125 秒`，大于等于要求 `1/5 = 0.2 秒`，余量 `9/80 = 0.1125 秒`。该关系在 `run-validation.py` 中用有理数独立核算，结果存于 `results.json`。本次未创建 M7.2 调度提案，因此不能把该关系说成由 M7.2 的 constraint checker 检验通过。

## 唯一既定视觉切换的帧边界

编辑时钟原点为 0，30 FPS，零基帧坐标为 `time × 30`。接触点对应 `6.0625 × 30 = 181.875`，向后取整得到 **第 182 帧**。

| 项目 | 精确值 | 十进制说明 |
|---|---:|---:|
| 编辑边界 | 182/30 = 91/15 秒 | 6.0666666667 秒 |
| 前一编辑帧 | 181/30 秒 | 6.0333333333 秒，早于接触 |
| 相对接触的延迟 | 91/15 − 97/16 = 1/240 秒 | 0.0041666667 秒 |
| 允许误差 | 1/200 秒 | 0.005 秒 |
| 误差余量 | 1/1200 秒 | 0.0008333333 秒 |
| 切换对应生成局部时刻 | 16/15 秒 | 1.0666666667 秒 |
| 切换对应作品时刻 | 166/15 秒 | 11.0666666667 秒 |

`10-cut-quantize.stdout.txt` 实际返回 `frame_index=182`、`quantized_time="91/15"`、`error_seconds="1/240"`、`within_tolerance=true`、`numeric_precision=calculated_conditionally`、`media_verified=false`。这些是给定 CFR 计划成立时的数值结论。

M11 毫秒表示取 `At 00:01.067`，与精确生成局部边界相差 `1/3000 秒`。只在连续时间数值上比较，显示时间仍晚于 contactA，距 contactA 为 `0.0045 秒 ≤ 0.005 秒`。编辑权威数据仍保留第 182 帧及 `91/15` 秒；不得从显示字符串反向重新 ceil 到编辑帧，因为 `6.067 × 30 = 182.01`，再次 ceil 会变成第 183 帧并违反本题误差限。详见 `m11-handoff.md`。

## 前向使用中实际遇到的问题

初次读取 `references/contract-guide.md` 时该文件尚未落盘，真实 `cat` 命令退出 1，错误为 `No such file or directory`。该历史观察单独保存在 `historical-guide-read.json`，没有伪装成当前重跑。后来文件可读，已核对其 Request/Proposal、外部只读绑定、未知状态、CLI 和精度边界说明；本次正式调用没有接口阻断。

检查输出重复列出部分未知值，并出现计算视图路径 `/request/inputs/timebase/items/...`、`/changes/timebase/items/...`，后者并非本 M7.3 文件真实写入分区；真实 Proposal 仅写 `changes.mappings`。这影响诊断路径的直接定位，不影响本次数值和通过状态；未据此修改技能。

## 验证范围与交付清单

已验证：实际 JSON 的本地合同、M7.3 路由、三段线性映射、两个事件的跨域秒数、源帧坐标、编辑域 ceil 量化及误差界；提前关系与 M11 时间显示由精确有理数另行复核。输出仍是草案。

未验证：源素材真实性、实际媒体帧率和 PTS、物理动作、实际相机到位、视觉切换内容、声音或口型、生成质量、全局 G0–G4；生成端帧率未知，未计算生成端帧号，未运行 H3。题目未提供场景、镜头内容或 H3 模式，因此 M11 交接是可并入既有正文的时序片段，不能独立冒充完整可提交创作提示词。

主要文件：`request.json`、`proposal.json`、`results.json`、`m11-handoff.md`、`commands.json`、`01` 至 `12` 的 stdout/stderr、`run-validation.py`、`task-copy.txt`、`historical-guide-read.json`、`public-input-hashes.json`。
