# 交付索引

先读 **audit-report.zh.md**。本次是合成制作资料的文字审计，没有真实媒体观察或生成。

| 文件 | 用途 |
|---|---|
| audit-report.zh.md | 简洁中文结论、四项问题、修复与复验顺序、实际接受结果 |
| audit-checks.json | 21项检查、四条要求、G0–G4范围与逐项证据定位 |
| repair-retest-plan.json | 责任分配、已有计划变更、依赖边界及完整复验安排 |
| interface-summary.json | 实际CLI调用与接受摘要、失败尝试和程序验证边界 |
| requests/accept-requests.json | 最终接受的三份原请求数组 |
| requests/accept-proposals.json | 与原请求逐一配对的提案数组 |
| state/current-state.json | accept原样返回的当前状态，version=1 |
| state/current-view.json | 当前状态视图 |
| commands/ | 每次调用的准确argv、工作目录、时间、退出码、stdout、stderr |
| results/ | 每次调用未经修改的stdout与stderr |
| target-declarations.json | 缺失媒体/资产的显式声明及摘要边界 |
| source-manifest.json / source-integrity.json | 输入摘要及执行前后未改动核对 |

所有请求尝试均保留。原始输入未改。程序accepted表示声明与记录合同接收成功；总审计仍为fail，并不代表生产可交付。
