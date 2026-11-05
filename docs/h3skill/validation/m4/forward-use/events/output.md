# M4.1 事件正向使用试验

## 实际结果

已按任务输入形成 `request.json` 与 `proposal.json`，只提交 M4.1 的 `changes.events`。实际运行一次 `check --request`，**返回码为 0，`local_contract=pass`，`overall=unverified`**；工具处置为 `checked_draft`。这表示本次请求及提案通过该运行版本的本地合同检查，不代表动作物理可行、视频表现成功或父模块验收完成。

原始标准输出保存在 `check.stdout.json`，标准错误保存在 `check.stderr.txt`（为空），准确命令、开始与结束时间、退出码保存在 `check-run.json`。执行环境设置 `PYTHONDONTWRITEBYTECODE=1`。未运行 H3、未联网、未执行其他测试，也未修改技能实现、原案例或任务输入。

## 已完成的事件与前提

| 顺序 | 稳定事件 ID | 事件与进入条件 |
| --- | --- | --- |
| 1 | `remove_sock` | 同一表演者以赤裸的解剖左脚着地支撑；解剖右脚抬起、穿同一只白袜且没有鞋。双手配合脱下该袜，过程中左脚持续支撑、右脚保持抬起。 |
| 2 | `hold_sock` | 依赖事件 1 完成，白袜已脱离右脚。一只手持该白袜、另一只手空出；解剖右脚赤裸并悬空。 |
| 3 | `inspect_sock` | 依赖事件 2 建立持袜状态。表演者转头看向同一只白袜并将其举起查看；解剖右脚仍赤裸悬空。 |

三个事件共用 `performer` 与 `white_sock`，以 `depends_on` 保留顺序，未扩展为原案例全部状态。硬要求通过 `requirements` 指向相关事件，且指回同一任务输入来源。提案的 `sources` 与请求一致，`context` 与请求的 `inputs` 一致。

`KnownFact` 和 `entry_state.state=known` 在这里表示任务已经给出的设计要求或由既定事件顺序要求的进入条件，**不是媒体观察结论**。全部来源归为 `user_requirement`，没有新增 `media_observation` 来源。

## 保留的未知与范围边界

最终由解剖左手还是解剖右手持袜未给出。在事件 2、3 的前提中分别保留显式 `Unknown`，并留下 `holding_hand_unknown` 的开放警告；没有默认左右，也没有编造换手动作。补充明确的持袜手左右后，才可确定这一点。

未给出音频、节拍、时长或媒体，所以没有绝对秒数、音频同步点或实测动作质量结论。本次只做事件与前提；没有填入 M4.2 力学过程、M4.3 结果验证、M7 时间线或 M8 状态账本。若后续要完成整个 M4，需要分别补充这些模块对应的设计及验证，不能从本次返回码推导其已完成。

实际检查输出包含四条非阻断诊断：

- 两条 `explicit_unknown`：分别对应事件 2、3 的持袜手左右。
- 一条 `/changes/mechanics` 的 `coverage_unavailable`，目标为 M4.2。
- 一条 `/changes/outcomes` 的 `coverage_unavailable`，目标为 M4.3。

本次范围内没有阻断诊断。工具还明确将语义意图、来源真实性、物理可行性、媒体观察、生成视频质量和全局 G0–G4 留为 `unverified`。M4.1 单独提交仍会提示全链条覆盖尚未完成，因此不能把 `pass` 表述为整个 M4 已通过。

## 读取与版本记录

依据为 `input.md`、`SKILL.md`、M4.1 事件资源、合同指南及合同中实际读取的定义；详细范围与读取时 SHA256 见 `read-manifest.json`。原案例在任务中被引用，但本试验没有另行打开原案例，也没有将原作者的媒体评价当作本次观察。

阅读过程中，部分长文的工具展示曾截断，随后仅补读了清单所列的 SKILL 与合同指南行段。没有读取 `tests/m4`、其他正向试验目录、评审或预期答案。

`read-manifest.json` 的主 `sha256` 字段统一记录文件原始字节摘要，`hash_scope=raw_file_bytes`。CLI trace 的摘要按规范化 JSON 计算，单独记录在 `cli_reported_digest`，不能直接与字节摘要比较。检查后读取并重算合同、registry、请求和提案的规范化摘要，四者均与原始 CLI trace 一致。

合同文件前后读取的字节 SHA256 均为 `5561fd66ae2d2ad37ffd980cf677af29e0939325e45d528ca5208a76b13067bd`，没有据此发现版本变化；其 CLI 规范化摘要为 `e6a1dac15a056365ab42799b0475b79c1049dbe82963b8eddfd02dd333c9c26e`。registry 检查后读取的字节摘要为 `17a6ac5cfec08432a6bebd769d490c5b032e59dd84df400fcaf5e77c77ef2be9`，对应 CLI 规范化摘要为 `0c9ae839740f7ddd82f46fd13e64d680451b22441bc0f5edbe70183d30a993a0`。本次没有在执行前读取 registry 内容，所以不声称观察到其名称修改前后的差异。工具包版本为 `0.1.0`，合同、路由与 registry 版本均为 `1.0.0`。

## 错误与修正经过

请求和提案首次落盘后直接执行一次真实检查。命令没有报错，返回码为 0；没有修正或重跑请求／提案，也没有以改动实现来使检查通过。保留的未知和覆盖提示均来自本次实际输出，未删改为全面通过。

报告初稿曾把 trace 的规范化 JSON 摘要误认为原始文件字节摘要，进而错误声称资源版本发生变化。收到摘要口径提醒后，实际读取相关文件、分别重算两种摘要并修正该判断；此修正没有改变请求、提案或 CLI 输出，也没有重新运行检查。含错误判断的初稿保留为 `output.initial.md`，当时的清单保留为 `read-manifest.initial.json`，仅用于审计修正过程；应以最终 `output.md` 与 `read-manifest.json` 为准。
