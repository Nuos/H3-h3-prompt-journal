# M2 forward-use 实际试用结果

## 结论

任务一已交付可独立进入 M2.3 的请求、双图权限提案、人可读权限表和 H3 模式/字段交接；两轮真实结构检查均通过。任务二已交付 SEG01 请求、保留矛盾的初版和人工语义修订版、逐项权限表及待决事项；修订提案仍真实拒绝，未被包装成可接受/可生成状态。

只使用案例文字。未提供、读取或生成图片/视频/音频；没有调用模型、媒体服务或远程写入，没有修改技能、案例或冻结计划，也没有执行 accept。

## 真实 CLI 结果

|运行包|任务|route|request check|proposal check --request|语义/媒体|
|---|---|---|---|---|---|
|原始 snapshot|任务一|exit 0|exit 0|exit 0，request_match_checked=true|均 unverified|
|原始 snapshot|任务二初版|exit 0|exit 0|exit 1，rejected，request_match_checked=false|均 unverified|
|定稿 snapshot-final-run|任务一，同一输入|exit 0|exit 0|exit 0，request_match_checked=true|均 unverified|
|定稿 snapshot-final-run|任务二初版，同一输入|exit 0|exit 0|exit 1，rejected，request_match_checked=false|均 unverified|
|定稿 snapshot-final-run|任务二人工修订版|复用已检查请求；未重复 route|复用已检查请求；未重复 request check|exit 1，rejected，request_match_checked=false|均 unverified|

共执行 13 次 CLI 读操作：两轮各 6 次，加一次修订提案检查。每次 stdout、stderr、退出码、时间、命令、实际请求/提案/脚本 SHA256 均保存在 execution 中。检查命令自身 execution_status=completed 不等于提案被接受；route 只作分发，未运行模型或下游模块。

## 初次错误与修订

真实依赖读取错误见 initial-errors.json，原始快照和首次结果未覆盖。人工复核删除了初版错误扩张的 audio_content/reference 许可，只保留 audio_timing/reference；原始 No signal copy 与 1:1 copy 对立要求完整保留。另补入 README 排除图1环境与 prompt 从图1取环境光色的语义冲突。详见 revision-log.md。

## 交付文件

- `task1-identity/actual-input.md`、`request.json`、`proposal.json`、`permissions.md`、`handoff.md`。
- `task2-xiashan-seg01/actual-input.md`、`request.json`、`proposal.json`（初版）、`proposal.revised.json`（当前候选）、`permissions.md`（初版）、`permissions.revised.md`、`handoff-and-decisions.md`。
- `execution/snapshot/`：首次 6 次真实运行记录及 commands.md。
- `execution/snapshot-final-run/`：定稿 6 次复核和修订版检查记录及 commands.md。
- `source-manifest.json` + `snapshot/`：首次实际读取的 18 个文件。
- `final-source-manifest.json` + `snapshot-final/`：中途捕获但未用于 CLI 的 20 个文件。
- `final-run-source-manifest.json` + `snapshot-final-run/`：最终实际运行的 20 个文件，全部可读。
- `build_forward_use.py`、`run_cli.py`、`finalize_report.py`：实际使用的本地构建、命令记录和报告脚本。运行记录是事实依据，不建议覆盖历史目录重跑。

## 使用版本

每个文件逐份捕获，不声称是一次原子仓库快照。完整案例及依赖哈希见上述清单；中途版本保留供追溯。H3 模式/字段采用本地 h3-label-mapping.md 与对应来源记录，未在本次联网验证上游。

|文件|最终使用 SHA256|
|---|---|
|`docs/h3skill/h3-asset-reference/SKILL.md`|`0515fd25fa248430f553e5cce8ff54c448ed4ef1aaf8d430a4452372a81abd6b`|
|`docs/h3skill/h3-asset-reference/references/contracts.json`|`292d0c81f7d2a7bf70d2268b18e0bc49a5bc4e62d0d081b9de171ba07df38740`|
|`docs/h3skill/h3-asset-reference/references/module-registry.json`|`8bfc341327c02783023380b1bc95dcb0dfe47c15a25c1f7ce83952513b436407`|
|`docs/h3skill/h3-asset-reference/references/contract-guide.md`|`11ca02243e400c6916c8b3fb677b1aa91e8650bc2aaacaca3926d097fc8a61da`|
|`docs/h3skill/h3-asset-reference/scripts/m2_contract.py`|`8241bb99f396c51e5c56c8ff21bb7930b45b8b9f644ca51bdbca8fda2b2e255a`|
|`docs/h3skill/h3-asset-reference/references/h3-label-mapping.md`|`0e7727e22c167b1a5978ff16f9132e121262314220ce92f66380d1035a5bfa19`|
|`docs/h3skill/h3-asset-reference/references/h3-protocol-source.json`|`8b98325a703b8564af80da4804167bc4f9a26dab410b3a49ade1feda299fd910`|

## 尚未完成的工作

任务一的结构通过不能证明图像真实性、跨图同人、授权事实、最终标签或视频效果。任务二的同属性多来源细分尚未写成 combine 决定，真实音频/服装/环境分歧仍待权威澄清，时间/媒体版本待补。没有声称运行 accept、M11 编译、媒体核验、音频分析或成片审校。
