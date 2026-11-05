# 首次错误与修订记录

## 依赖读取

首次读取 `contract-guide.md` 返回文件不存在；后续该依赖落盘后重读成功。首次枚举尚不存在的 forward-use 目录也返回错误。两次实际命令、退出码、原始错误与处置见 `initial-errors.json`。当时未记录时间，未补造时间戳。

## 初版合同与真实检查

两份 request 首次即通过结构检查；任务一 proposal 首次通过。任务二 proposal 首次被拒绝，原始候选 `task2-xiashan-seg01/proposal.json` 与所有首次日志保持不变。没有伪造一次 JSON 语法错误来展示修复流程。

原始运行包把 `audio_content/reference allow` 与 `audio_content/copy forbid` 也报作冲突。定稿运行包重跑同一初版时，这一跨用途诊断消失。两次实际记录均保留；这只能说明相应数据结构下的检查差异。

## 人工语义复核后的修订

主线程随后指出：原文 **only for rhythm** 应落在 `audio_timing/reference`，初版额外的 `AUDIO-REF-ONLY` 使用 `audio_content/reference allow`，扩大或混淆了授权属性。脚本没有识别这个自然语言忠实度问题。本次另存 `proposal.revised.json`，只删除这条由我们误加的内容许可；已有 `AUDIO-TIMING` 保留。原文 `No signal copy` 与 `fully_copy / reused 1:1` 两项相反要求均未删改。

因此，不把本案初版跨用途诊断当作真实需求的合格回归样例；那条额外内容许可本身就是人工建模错误。真正的音频矛盾在修订后仍是同一 binding / scope / attribute / use 下的 `copy forbid` 与 `copy allow`。

同时补入 `ENV-SOURCE-CONFLICT`：README 明确图1不负责环境，而 prompt 把环境光色语言归图1。新增精确 README 摘录与待决问题，不删掉任一侧原始要求，也不声称脚本自动识别了这个语义矛盾。

修订候选使用既有 final-run 固定运行包实际检查，仍返回 rejected。未执行 accept；未向源技能、源案例或冻结计划写入修订。
