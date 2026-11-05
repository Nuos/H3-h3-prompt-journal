#!/usr/bin/env python3
"""Preserve the first candidate, record the human semantic correction, and write reports."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, shlex, subprocess, sys
out=Path(__file__).resolve().parent
repo=out.parents[4]
task=out/'task2-xiashan-seg01'
p=json.loads((task/'proposal.json').read_text())
p['proposal_id']='PROP-TASK2-XIASHAN-SEG01-R1'
del p['changes']['reference_map']['permissions']['AUDIO-REF-ONLY']
manifest=json.loads((out/'source-manifest.json').read_text())
hashes={x['path']:x['sha256'] for x in manifest['files']}
readme='case-studies/2026-10-xiashan-veiled-solo-twelve-segment/README.md'
p['sources']['SRC-README-ENV']={'kind':'case_text','locator':readme,'version':'sha256:'+hashes[readme],
 'excerpt':'| PICTURE 1(正面全身,无头部) | 正面服装/身体 | 脸、背、环境 |\n| PICTURE 2(三视图) | 脸(五官/眉眼/发型)、背部结构、半纱只遮口鼻、安全裤一句 | 环境、光线、姿势、构图、相机 |'}
p['issues'].append({'issue_id':'ENV-SOURCE-CONFLICT','owner':'user','state':'open','blocking':True,
 'description':'README 明确图1不负责环境，prompt SEG01 的 COLOR & ATMOSPHERE 却声明环境语言来自 Picture 1。两条都保留，尚无授权决定是否可从图1继承环境光色；该语义矛盾未被简单属性检查自动识别。',
 'source_refs':['SRC-TASK','SRC-README-ENV','SRC-COLOR']})
revised=task/'proposal.revised.json'
if revised.exists(): raise SystemExit('Refusing to overwrite revision')
revised.write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n')
(task/'permissions.revised.md').write_text('# 修订后人可读权限表\n\n这是当前交付候选。初版 `proposal.json` 和 `permissions.md` 保留供追溯；修订不删除原始需求矛盾。所有权限范围仅 SEG01。\n\n'
 +'|权限 ID|绑定|属性|决策|用途|理由|\n|---|---|---|---|---|---|\n'
 +''.join('|'+pid+'|'+v['binding_id']+'|'+v['attribute']+'|'+v['decision']+'|'+v['use']+'|'+v['reason'].replace('|','/')+'|\n' for pid,v in p['changes']['reference_map']['permissions'].items())
 +'\n额外语义阻塞：README 排除图1环境用途，而 prompt 的 COLOR 段从图1继承环境语言；见 `ENV-SOURCE-CONFLICT`。没有选择任何冲突分支；`decisions` 仍为空。\n')
runner=out/'snapshot-final-run/docs/h3skill/h3-asset-reference/scripts/m2_contract.py'
request=task/'request.json'
cmd=[sys.executable,str(runner),'check',str(revised),'--request',str(request)]
start=datetime.now(timezone.utc).isoformat()
cp=subprocess.run(cmd,cwd=repo,text=True,capture_output=True)
record={'start_time':start,'end_time':datetime.now(timezone.utc).isoformat(),'cwd':str(repo),'argv':cmd,'command':shlex.join(cmd),
 'exit_code':cp.returncode,'script_sha256':hashlib.sha256(runner.read_bytes()).hexdigest(),
 'request_sha256':hashlib.sha256(request.read_bytes()).hexdigest(),'proposal_sha256':hashlib.sha256(revised.read_bytes()).hexdigest(),
 'stdout':cp.stdout,'stderr':cp.stderr}
log=out/'execution/snapshot-final-run/task2-xiashan-seg01--proposal-revised-check.json'
if log.exists(): raise SystemExit('Refusing to overwrite check result')
log.write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
with (out/'execution/snapshot-final-run/commands.md').open('a') as f:
 f.write('## 7. 人工语义修订后的真实检查\n\n```sh\n'+record['command']+'\n```\n\n退出码：'+str(cp.returncode)+'。开始：'+start+'。\n')
result=json.loads(cp.stdout)
(out/'revision-log.md').write_text('''# 首次错误与修订记录

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
''')
(out/'task1-identity/handoff.md').write_text('''# 任务一：双图权限与 H3 交接

## 完成范围与证据

`request.json` 是可独立路由到 M2.3 的完整请求：资产上下文和实体上下文直接随请求提供，不需要先调用 M2.1/M2.2。`proposal.json` 只提出 reference_map 变更，不修改资产或实体登记。原始与定稿运行包均已实际执行 route、request check 和 `check proposal --request request`；提案 deterministic pass，request_match_checked=true。语义、媒体、总评仍 unverified。

|案例素材|文字授权的继承|明确排除|后续责任|
|---|---|---|---|
|Picture 1 / IMG-FACE|面部身份、五官结构、可辨认比例|头角、身体/手臂/手位、站姿、静态构图、编舞、首帧锚定|补图后核验身份和选择区域；M5 按文字落实半身机位|
|Picture 2 / IMG-BODY-SCENE 的人物部分|身体比例/尺度、服装、配饰、可见发型|精确静态站姿、照图开场、编舞|M4 从文字动作定义开场，M5 负责机位|
|Picture 2 的环境部分|环境/建筑/背景、光向/曝光、空间深度、写实摄影质感|未授权从环境图片推断具体测量值|M3/M5 接收场景与画面要求，待媒体核验|

完整机器记录与逐项表见 `proposal.json`、`permissions.md`。scope=work 表达六段共同双图规则。没有把图1的半身照片直接变成 I2VA 首帧，也没有把两图共同“参考”扩张为复制全部像素属性。

## 模式与标签

候选交接为 **Ref2VA**：双图按属性参考，不是首/尾帧约束。M11 仍须结合目标后端能力确认最终模式。I2VA、FL2VA、L2VA 均需要此任务没有给出的实际帧锚定意图/素材；不得因为存在图片就自动选择。

`IMG-FACE`、`IMG-BODY-SCENE`、`PERFORMER`、`ENVIRONMENT` 是 M2 内部 ID。案例的 `<Picture 1>`/`<Picture 2>` 只保留源文标识，不宣称已完成上传编号。M11 应按角色选择官方 `<Subject n>` / `<Picture n>`：人物身份引用应与表演者实体绑定，环境/风格角色另行表达；同一图的 BODY 与 SCENE 选择不应因此混为人物姿态。

## Ref2VA 字段交接

|官方字段|本案交接内容|
|---|---|
|subject_definitions|唯一表演者、双图所负责属性、独立的环境角色；编号待真实上传分配|
|summary|六段舞蹈共同目标；新动作起步、半身肖像式摄影关系|
|retention_analysis|保留面部/身体/服装/环境的明确属性；排除两图姿态、编舞、静态首帧；不宣称所有内容 fully preserved|
|detailed_description|从源案例交接动作链与镜头文字；半身机位属于 M5，首帧动作属于 M4，不由身份图推断|
|overall_soundscape|交 M6 核对；当前图片权限提案没有实际音频，不产生声音事实|
|non_diegetic_music|源案例逐段要求 Audio 1 1:1 作为最终音轨。该要求记录为待 M6/M7/M11 对接；音频文件、具体源窗口、最终混音均未核验|

依据固定的 `h3-label-mapping.md`：Ref2VA 使用上面六字段；T2VA/I2VA/FL2VA/L2VA 的基础三字段为 integrated_multimodal_description、overall_soundscape、non_diegetic_music。此表是交接，不是已编译 H3 请求或已执行模式选择。

## 未完成与限制

缺两张实图及其来源版本、真实区域与跨图身份核验；段音频也没有提供。当前可以完成文字权限整理与结构校验，不能完成媒体读取、上传、最终 H3 标签分配、模型调用或成片评价。未执行 accept；通过结构检查不等于已接受提案或可立即生成。
''')
(out/'task2-xiashan-seg01/handoff-and-decisions.md').write_text('''# 任务二：SEG01 可完成部分、缺项与实际决定

当前交付候选为 `proposal.revised.json`；`proposal.json` 是保留的初版。二者都不是已接受状态。修订候选在定稿运行包上实际返回 rejected；不把原文矛盾静默改成可生成的单一政策。

## 已完成的文字登记

|对象|可登记内容|不能据此宣称|
|---|---|---|
|图1 / IMG-FRONT|原文指定正面身体、正面服装；C1 的入态明确使用图1站姿|没有看到实图，不能验证“无头部”、体型、服装或站姿；C1 入态不自动成为视频首帧|
|图2 / IMG-THREE-VIEW|原文指定脸、眉眼、发型、背部服装、口鼻半纱面纱；衣装和面纱不随歌词改变|未核验图2内容、同人一致性或安全裤；不能额外命名/补写服装细节|
|场景|星海高台夜景、单人且背景无其他人物是文字目标；保留图1环境权限的相反说明|没有观察环境图片，不把文本场景当成图片证据|
|Audio 1 / AUDIO-SEG01|BPM 134.0、beat 0.4478 s、bar 1.7910 s、首拍 0.441 s、歌词起点 0.766/4.433/8.116 均按源文登记为 audio_timing/reference|这些数值未测音频；节奏参考没有扩张成音频内容或角色音色授权|

README 的图2排除项还包括环境、光线、姿势、构图、相机；后续编译应保持这些边界，不把同一张图的身份权限扩成全部画面属性。详细原始分工和全部源文见快照及 actual-input.md。

## 必须保留并需要权威澄清的要求

|问题|原始要求 A|原始要求 B|实际需要的决定|
|---|---|---|---|
|音频用途|subject_definitions：referenced only for rhythm；No signal copy|summary / retention：complete final audio track、reused 1:1、fully_copy，不重生/改动音乐|确认最终音频政策以及两句原要求的适用范围；本次不能选掉任一条。copy forbid 与 copy allow 已同时保留|
|服装来源|图1只负责正面，图2负责背面与面纱|COLOR 段：The costume comes solely from Picture 1|明确“solely”究竟限于正面还是覆盖全服装；如要缩窄原文，须有权威决定|
|图1环境权限|README 分权表：图1明确不管环境|prompt COLOR & ATMOSPHERE：authorized environment language, from Picture 1|明确是否允许图1提供环境光色，或仅把这些词当独立文字美术要求；两份来源目前相反，ENV-SOURCE-CONFLICT 保持 open|
|SEG01 音频/时间版本|prompt：0.000–11.116 s，段内独立提交 mp3|README 切段表另一套边界从 0–12.860 s 开始；其后总边界也与 141.845 s 描述不一致|提供/指定实际 SEG01 音频、版本、源窗口与采用的切段时间表；交 M7 核对|

这张表列出真实决策点；不会要求用户重新批准已经明确的图1正面、图2脸/背面分工。对已有兼容分工的精细结构表达，可以在后续 M2 工程修订中完成。

## 实际检查的边界

最终修订提案的四个 blocking 结构诊断为：

- FACE-HAIR 与 FRONT-BODY：competing_reference_sources；两者共用粗属性 appearance，实际文字分别指头部/身体。本次没有进一步构造有权威的 combine 决定，保留了待处理诊断。
- BACK-VEIL 与 FRONT-CLOTHES：competing_reference_sources；两者共用 clothing，实际文字分别指背面/正面。该诊断本身不是新发现的用户矛盾。
- COLOR-EXCLUSIVE 与 BACK-VEIL：permission_conflict；反映“全服装只来自图1”与图2背面/面纱权威的字面冲突。
- AUDIO-EXACT-COPY 与 AUDIO-NO-COPY：permission_conflict；同一 audio_content/copy 的真实相反要求。

环境来源冲突由人工阅读保留为 open issue；脚本未自动证明其自然语言语义。proposal 在请求配对检查前已被权限检查拒绝，因此本次 `--request` 虽已传入，结果仍为 request_match_checked=false；不要宣称该修订提案已通过 request 配对验证。

## H3 交接

Ref2VA 是候选路线，不将“0.00 seconds fully referenced”自动改成 I2VA 首帧。`FRONT-ANCHOR` 仍为 unknown。真实文件、上传顺序和官方 `<Subject n>`/`<Picture n>`/`<Audio n>` 由 M11 确认，M2 内部 ID 不替代它们。

原案同时写了 subject_definitions、summary、retention_analysis 与 integrated_multimodal_description。按本地固定官方映射，Ref2VA 应使用 **subject_definitions / summary / retention_analysis / detailed_description / overall_soundscape / non_diegetic_music**。本次仅建议 M11 把连续动作正文迁移到 detailed_description；没有改写案例。不能把“字段迁移建议”记成已经完成编译。

音频交 M6，源窗口/节拍网格交 M7，SEG01 所称“承接上一段”但缺失的前态交 M9。最终是否 fully_copy 必须等音频政策与实际输出声音范围明确：若用户另行决定保留原音乐又新增声音，需要重核相应复制语义；本次没有做混音或选择新方案。

## 实际缺项

两张图、SEG01 音频文件、媒体版本/哈希、选择区域、真实时长/源窗口、可核验的前段终态、后端能力与上传编号均未提供。旧 Windows 路径只是案例文字；没有尝试访问或假装挂载。没有视频输出可评，案例历史验证与生成结果不作为本次验证成绩。
''')
final_manifest=json.loads((out/'final-run-source-manifest.json').read_text())
key_paths=['docs/h3skill/h3-asset-reference/SKILL.md','docs/h3skill/h3-asset-reference/scripts/m2_contract.py','docs/h3skill/h3-asset-reference/references/contracts.json','docs/h3skill/h3-asset-reference/references/module-registry.json','docs/h3skill/h3-asset-reference/references/contract-guide.md','docs/h3skill/h3-asset-reference/references/h3-label-mapping.md','docs/h3skill/h3-asset-reference/references/h3-protocol-source.json']
sha_table='|文件|最终使用 SHA256|\n|---|---|\n'+''.join('|`'+i['path']+'`|`'+i['sha256']+'`|\n' for i in final_manifest['files'] if i['path'] in key_paths)
(out/'RESULTS.md').write_text('''# M2 forward-use 实际试用结果

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

'''+sha_table+'''
## 尚未完成的工作

任务一的结构通过不能证明图像真实性、跨图同人、授权事实、最终标签或视频效果。任务二的同属性多来源细分尚未写成 combine 决定，真实音频/服装/环境分歧仍待权威澄清，时间/媒体版本待补。没有声称运行 accept、M11 编译、媒体核验、音频分析或成片审校。
''')
print(json.dumps({'revised_check_exit':cp.returncode,'outcome':result['outcome'],'request_match_checked':result.get('request_match_checked'),
 'blocking_diagnostics':[{'code':d['code'],'path':d['path']} for d in result['diagnostics'] if d.get('blocking')],
 'summary':str(out/'RESULTS.md')},ensure_ascii=False,indent=2))
