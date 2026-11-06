# 规则修订后复核交付

先读revision-report.zh.md。此次延续首轮状态，没有重建独立试验或覆盖旧输出。

| 文件/目录 | 内容 |
|---|---|
| revision-report.zh.md | 修订原因、当前结论、责任与复验安排、实际接受结果 |
| revision-manifest.json | 精确规则摘要、唯一变化项和保持不变的范围 |
| evidence-and-gates.rule-snapshot.md | 本次已读更新规则的固定副本 |
| interface-summary.json | 公开接口执行摘要与状态边界 |
| requests/first-round-accepted-requests.json | 首轮已接受原请求副本 |
| requests/audit-request.json | 本次M12.2原请求 |
| requests/repair-request.json | 本次M12.4原请求 |
| requests/accept-requests.json / accept-proposals.json | 本次实际接受的请求/提案配对 |
| results/ | 每次原始提案、检查和接受输出，含stderr |
| commands/ | 准确argv、时间、退出码、完整stdout/stderr |
| state/base-state.json | 首轮version=1状态副本 |
| state/current-state.json | 追加后的version=2状态 |
| state/current-view.json | 程序返回的当前视图 |
| preserved-files-integrity.json | 原task.md、sources/、output/未变核对 |

唯一审计结果变化：CHK-COMPILE-SOUND由unverified改为fail。新增声音策略问题回传M6确认保留范围与partially_copy，再由M11编译；实际混音与同步继续等待媒体观察。
