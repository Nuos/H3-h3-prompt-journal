# M11 独立使用与监督修订记录

本目录记录一次新上下文的文字任务：只提供原始任务和独立复制的 M11 技能包，要求实际构造公开合同并运行适用命令。没有提前提供预期模式、标签答案或验收断言。用户剧情为工程合成输入，不属于新增实测案例。

## 结果与范围

- 原任务：[task.md](task.md)。最终交付：[中文说明](output/README.zh-CN.md)、[完整模型正文](output/model-prompt.txt)、[必保内容追溯](output/preservation-trace.zh-CN.md)、[工作流交接与缺项](output/workflow-handoff.json)。
- 首轮机器检查成功后，父审阅发现音场汇总中混入对白执行要求，见 [初次审阅](initial-review.json)。修订把这些要求移入对应镜头，保留动作、原词、切点和参数；技能入口补充了明确声音分层检查。
- 两轮均真实运行 13 次公开 CLI：各 12 次退出 0、1 次按预期返回 `runtime_unknown`。M11.4 无成功提案，没有接受任务导出分区。
- 最终状态为 version 2 / partial，保存两轮共 6 条接受收据。使用新请求 ID 和当前基版本，保留第一次已接受状态的历史。
- 父审阅再次核对三份提案、精确重试、实际正文、参数、17 项义务及完整历史，见 [review.json](review.json)。这些结论限于文字任务和可确定合同，不证明实际视频质量。

## 证据位置

[output/](output/) 是独立使用代理的完整最终交付，包含命令、stdout/stderr、请求、提案、状态、作者安排和最终检查。其 `revision-history/round-1/` 保存首轮产物。父代理先行捕获的 57 份首轮文件经过逐字节比较，合并到这些历史文件及两个未改变的共享文件；准确路径与摘要见 [initial-artifact-map.json](initial-artifact-map.json)，没有丢弃原始文件内容。

[final-input-snapshot.json](final-input-snapshot.json) 记录最终完整技能包摘要。首次实际任务执行已使用修正后的复制音轨编译器；两次任务执行之间只增强了 `SKILL.md` 的声音分层审计提示，脚本未变。更早的资料阅读／help 阶段不计为一次成功编译。

发布整理时仅删除编译器两处行末空格，Python AST 完全相同，见 [finalization.json](finalization.json)。上面的输入快照与使用代理的工具链记录保留当时真实字节。父代理随后对发布版再实际运行 3 次提案核对、1 次已接受状态幂等重试及 1 次运行未知拒绝，全部符合预期；[最终 CLI 复核](release-recheck/record.json) 保存这 5 次调用及发布版摘要。这 5 次与使用代理的两轮 26 次分别计数。

交付说明中的 490 词是 `detailed_description` 按空白切分的计数；完整六字段输出按同一口径为 863。它们不是 token 数，也不是质量评分或硬限制。

## 重现方法

本目录是证据归档，不重复放置整个技能包。以下命令从仓库根直接核对已经保存的自足请求与提案，不要求旧的临时目录存在：

```bash
python docs/h3skill/h3-model-protocol/scripts/m11_contract.py check docs/h3skill/validation/m11/forward-use/output/proposals/m11-3-proposal.json --request docs/h3skill/validation/m11/forward-use/output/requests/m11-3-request.json
python docs/h3skill/h3-model-protocol/scripts/m11_contract.py accept docs/h3skill/validation/m11/forward-use/output/proposals/accepted-proposals.json --requests docs/h3skill/validation/m11/forward-use/output/requests/accepted-requests.json --state docs/h3skill/validation/m11/forward-use/output/results/accepted-state.json
python docs/h3skill/h3-model-protocol/scripts/m11_contract.py propose docs/h3skill/validation/m11/forward-use/output/requests/m11-4-request.json
```

前两条应退出 0；第二条保持原状态并返回 `idempotent: true`；第三条应以 `runtime_unknown` 退出 2。完整实际调用命令见 [commands.zh-CN.md](output/commands.zh-CN.md)。

`run_compilation.py` 保存这次任务调用器的实现，并引用首轮历史状态；它不是任意路径下新建任务的通用启动器。来源定位符和时间戳属于原调用记录。重新创作任务时应重新登记来源及版本，按新工作或当前工作历史构造请求；只改目录路径、继续复用相同来源版本或把新输出当作原历史字节都会破坏来源关系。

真实媒体、后端字段、推理、语速／动作时间可行性、声画同步及完整媒体关卡均未验证。
