#!/usr/bin/env python3
"""Write reviewable handoff files from actual CLI outputs and an explicit text review."""
from pathlib import Path
import hashlib
import json
import re

OUT=Path(__file__).resolve().parent
def read(name): return json.loads((OUT/name).read_text(encoding='utf-8'))
def dump(name,obj): (OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def text(name,s): (OUT/name).write_text(s,encoding='utf-8')

binding=read('results/reference-binding.json')
comp=read('results/prompt-compilation.json')
req=read('requests/m11-3-request.json')
state=read('results/accepted-state.json')
records=read('command-log.json')
prompt=comp['rendered_prompt']
detail=comp['fields']['detailed_description']
obligations=req['inputs']['obligations']

checks={
 'six_fields_in_required_order':comp['field_order']==['subject_definitions','summary','retention_analysis','detailed_description','overall_soundscape','non_diegetic_music'],
 'mode_ref2va':comp['mode']=='Ref2VA',
 'no_alignment_first_or_last_frame':comp['alignment_instruction'] is None,
 'two_real_shot_headers':re.findall(r'^\[Shot \d+\]',detail,re.M)==['[Shot 1]','[Shot 2]'],
 'exact_second_cut': '[Shot 2] At 00:03.500,' in detail,
 'first_shot_no_timestamp':not re.search(r'^\[Shot 1\] At ',detail,re.M),
 'luo_exact_once':prompt.count('<d>[Chinese] 请给我一杯热茶。</d>')==1,
 'ye_exact_once':prompt.count('<d>[Chinese] 小心，茶还很烫！</d>')==1,
 'only_two_dialogue_blocks':len(re.findall(r'<d>.*?</d>',prompt))==2,
 'exact_visible_sign': '"今日茶已备好！"' in detail,
 'speaker_mapping':binding['labels']['speakers']=={'luo_voice':'S1','ye_voice':'S2'},
 'no_unresolved_placeholders':'{{' not in prompt and '}}' not in prompt,
 'all_17_obligation_ids_traced':len(comp['obligation_trace'])==17 and {o['obligation_id'] for o in obligations}=={o['obligation_id'] for o in comp['obligation_trace']},
 'target_parameters_preserved':read('target-parameters.json')=={'duration_ms':8000,'width':1080,'height':1920,'fps':24},
 'no_unearned_export_partition':set(state['content'])=={'capability_profile','reference_binding','prompt_compilation'} and state['status']=='partial',
 'official_source_hashes_match_package':all(
     hashlib.sha256((OUT.parent/'h3-model-protocol/references'/f'h3-{n}-official.txt').read_bytes()).hexdigest()==read('source-register.json')[f'official-{n}']['sha256']
     for n in ['base','ref'])
}
assert all(checks.values()),checks
dump('checks/delivery-consistency-check.json',{
    'status':'pass','scope':'Additional deterministic checks of delivered text and stored results; not a substitute for the public CLI or semantic/media review.',
    'checks':checks,'detailed_description_whitespace_word_count':len(detail.split()),
    'not_checked':['spoken duration','media identity','actual audio content','backend support','generated visuals or sound']})

mapping={
 'mode':'Ref2VA','task_types':binding['task_types'],'labels':binding['labels'],
 'media_inputs':binding['media_inputs'],
 'speakers':[
   {'speaker_id':'luo_voice','person':'罗成','subject_id':'luo_cheng','subject_label':'<Subject 2>','speaker_label':'S1','first_vocal_ms':600,'time_basis':'agent_arrangement','utterance':'请给我一杯热茶。'},
   {'speaker_id':'ye_voice','person':'叶青','subject_id':'ye_qing','subject_label':'<Subject 1>','speaker_label':'S2','first_vocal_ms':4100,'time_basis':'agent_arrangement','utterance':'小心，茶还很烫！'}],
 'asset_availability':'Only user text declarations are supplied. All declared-media:// URIs are non-resolving identity locators; no media was provided, opened, decoded, uploaded, or loaded by a backend.',
 'stable_identity_rule':'Keep asset_id and subject_id stable. Picture and other category indices belong to this caller order and must be regenerated when it changes.',
 'audio_retention':{'asset_id':'room_music','version':'audio-1','retention':'partially_copy','full_source':True,'entire_soundtrack':False,'additional_layers':['new-dialogue','tea-pouring','kettle-set-down','cup-base-sliding']}
}
dump('reference-and-speaker-map.json',mapping)

evidence={
 'setting-front':('街角茶铺、明亮写实自然光；人物衣着与柜台内外','"bright street-corner tea shop"; "light-gray apron"; "dark-blue jacket"; "counter separates them throughout"'),
 'framing-front':('第一镜0秒、正面中景、肩颈手与完整杯子','"frontal medium view"; "shoulders and necks, their hands, and the complete ceramic cup"'),
 'sign-front':('原文标牌与标点','"今日茶已备好！"'),
 'place-empty-cup':('罗成先放空陶杯到柜台中央','"First, <Subject 2> places an empty ceramic cup at the counter center"'),
 'luo-line':('罗成台词一次、字词标点完全保留','<Subject 2> (S1) ... <d>[Chinese] 请给我一杯热茶。</d>'),
 'pouring-hands':('叶青右手壶柄、左手壶盖','"handle firmly in the right hand and steadies its lid with the left"'),
 'pouring-target':('热茶倒进杯内、杯子原位','"pours hot tea"; "stream lands inside the cup"; "stays in its original central position"'),
 'cut-side':('第二镜生成局部3.5秒侧面中景','[Shot 2] At 00:03.500, cut to a steady side medium view'),
 'continuity-side':('跨镜身份衣着位置与已装茶杯连续','"same filled cup remains at the center at the cut"; "identities, light-gray apron, and dark-blue jacket continue unchanged"'),
 'sign-side':('第二镜继续保持同一标牌','"the wall sign remains readable"；沿用第一镜已给出的原文字面'),
 'return-kettle':('叶青将壶放回柜台内侧','"sets the kettle back on the inner counter"'),
 'ye-line':('叶青台词一次、字词标点完全保留','<Subject 1> (S2) ... <d>[Chinese] 小心，茶还很烫！</d>'),
 'move-cup':('罗成右手杯柄、谨慎移到外缘','"grips the cup handle with the right hand"; "carefully draws the cup ... toward the outer counter edge"'),
 'ye-hands-clear':('叶青双手离开杯子','"keeps both hands clear of the cup"'),
 'end-state':('8秒两人保持结果状态','"cup rests securely at the outer edge"; "Hold these positions through the eight-second endpoint"'),
 'music-front':('整段配乐复用、观众可闻、新对白与倒水声','"complete source music signal from <Audio 1> starts with this shot as audience-only score"'),
 'music-side':('配乐跨切连续、新对白落壶轻擦声','"<Audio 1> continues seamlessly across the cut and through the end"; "new warning, kettle contact, and cup movement"')
}
trace=[]
for o in obligations:
    label,excerpt=evidence[o['obligation_id']]
    trace.append({**o,'source_locator':'task.md / 创作计划','output_field':'detailed_description',
                  'output_shot':binding['labels']['shots'][o['shot_id']],
                  'review_label_zh':label,'text_evidence':excerpt,
                  'machine_scope':'Obligation ID is declared, covered, and assigned to the proper shot; this is not semantic proof.',
                  'agent_text_review':'pass','media_validation':'unverified'})
dump('preservation-trace.json',trace)
rows=['# 必保内容追溯\n','本表对照 `task.md` 与实际生成的 `model-prompt.txt`。程序核验 ID、引用和镜头作用域；“文字审阅通过”由 Agent 逐项对照，未检查媒体实现。\n',
      '| 义务 ID | 来源必保内容 | 输出镜头与文字证据 | 结论 |','| --- | --- | --- | --- |']
for t in trace:
    excerpt=t['text_evidence'].replace('<','&lt;').replace('>','&gt;')
    rows.append(f"| `{t['obligation_id']}` | {t['review_label_zh']} | {t['output_shot']}：{excerpt} | 文字审阅通过；媒体未验证 |")
rows.extend(['\n## 参考、台词及参数的独立核对\n',
 '- 两张图片只嵌在 Subject 来源定义中，没有实际首帧／尾帧或独立构图锚。保留范围仅为人物身份与指定衣服。',
 '- 全部模型字段中仅有两个 `<d>` 块，两句中文台词各出现一次且标点未改；`punctuation_trace` 为空。',
 '- 配乐整段保留，新增四类声音层，因此 `partially_copy`、`full_source=true`、`entire_soundtrack=false` 同时成立。',
 '- `target-parameters.json` 保留 1080×1920、24 fps、8000 ms；导出失败没有改变参数。',
 '- `checks/delivery-consistency-check.json` 保存额外的确定性核对。464 是正文按空白切词的参考计数，不是模型 token 数或质量保证。\n'])
text('preservation-trace.zh-CN.md','\n'.join(rows))

missing=[
 {'id':'runtime-identity','owner':'M11.1 / 部署资料提供方','missing':'实际后端名称和版本、H3 模型/权重版本、工作流名称和版本。'},
 {'id':'mode-support','owner':'M11.1 / 部署资料提供方','missing':'目标部署已暴露 Ref2VA、两图片参考和独立音频复用的版本证据。'},
 {'id':'parameter-mapping','owner':'M11.4 / 工作流提供方','missing':'duration_ms/seconds、width、height、fps 的实际节点或字段路径、类型、单位、必需项、枚举/范围和对应版本依据。'},
 {'id':'prompt-and-mode-slots','owner':'M11.4 / 工作流提供方','missing':'完整六字段 rendered_prompt 的输入位置和封装方式、模式字段位置及真实取值。'},
 {'id':'media-slots','owner':'M11.4 / 工作流提供方','missing':'实际素材输入槽位、通道/序列格式、资产上限与同一身份映射规则。'},
 {'id':'actual-media','owner':'M2 / 素材提供方','missing':'portrait_ye img-1、portrait_luo img-2、room_music audio-1 的真实可访问文件/上传对象，以及带版本的 asset_map 值；现有声明 URI 不能作为提交值。'},
 {'id':'media-inspection','owner':'M2 / M6 / M12','missing':'两张图的实际身份/衣着与参考权限范围；音频实际8秒、无歌词、信号内容与可用许可依据的独立核对。任务文字已声明许可，本轮未独立验证。'},
 {'id':'execution-and-acceptance','owner':'执行方 / M12','missing':'真实工作流调用与返回、媒体解码观察、动作和口型、文字清晰度、配乐混合、两镜连续性、时长/帧率/尺寸测量。'}
]
handoff={
 'status':'protocol_text_ready_runtime_export_blocked','work_id':'tea-shop-eight-second',
 'accepted_state':{'version':state['version'],'status':state['status'],'partitions':list(state['content'])},
 'mode':'Ref2VA','target_parameters':read('target-parameters.json'),
 'prompt_file':'model-prompt.txt','fields_file':'model-fields.json',
 'binding_file':'results/reference-binding.json','source_register':'source-register.json',
 'runtime_asset_map':{},'actual_export_attempt':'results/m11-4-export-blocked.json',
 'export_error':read('results/m11-4-export-blocked.json')['errors'],
 'missing':missing,
 'executable_payload':None,
 'next_step':'Obtain versioned deployment evidence and real media values, update the CapabilityProfile and asset_map, then regenerate/check/accept the affected partitions at the current state version. Do not change the target creative plan or dimensions to conceal missing evidence.',
 'not_performed':['network access','media generation','media decoding','backend submission','H3 inference','video acceptance']
}
dump('workflow-handoff.json',handoff)

command_lines=['# 实际命令与结果\n',
 '调用器：`python output/run_compilation.py`；工作目录为本任务目录。以下命令由调用器以 subprocess 参数数组真实运行；所有 CLI 操作的 cwd 均为当前提供的 `h3-model-protocol`。完整命令、参数、stdout/stderr 路径和退出码也见 `command-log.json`。\n',
 'M11.4 的退出码 2 是实际预期阻塞。没有为其伪造提案，也没有将错误输出当作成功提案接受。各 stderr 文件均为空；诊断由 stdout 的结构化 JSON 返回。\n']
for r in records:
    command_lines.extend([f"## {r['name']} — exit {r['exit_code']}\n",'```sh',r['command'],'```',
      f"\nstdout：`{r['stdout_file']}`（{r['stdout_bytes']} bytes）；stderr：`{r['stderr_file']}`（{r['stderr_bytes']} bytes）。\n"])
text('commands.zh-CN.md','\n'.join(command_lines))

text('README.zh-CN.md','''# 8 秒茶铺片段：H3 文本编译交付

## 1. 交付结论

已用指定技能包的当前公开脚本完成 **M11.1 能力登记、M11.2 模式与参考绑定、M11.3 正文编译**。三份提案均与真实请求核对，返回 `valid: true`、`passed_with_unverified`；父接受完成，状态为 **version 1 / partial**。M11.4 已实际尝试，因 `runtime_unknown` 退出 2。没有可执行工作流请求，也没有实际视频。[C1–C5]

完整模型正文位于 **`model-prompt.txt`**；`model-fields.json` 是同一内容的精确六字段对象。正文与工程记录分开，可直接审阅，不含合同元数据。1080×1920、24 fps、8000 ms 目标完整保留于 `target-parameters.json` 与 M11.4 请求。[T、C3、C4]

## 2. 来源事实与表达安排

### 2.1 用户文字提供的事实

来源是 `task.md`，全文及 SHA-256 已进入 `source-register.json`。用户指定了明亮写实自然光的街角茶铺；叶青在柜台内、浅灰围裙，罗成在柜台外、深蓝夹克；柜台分隔双方。指定两镜、0 秒开始、3.5 秒切到侧面中景、8 秒停留结果；指定放杯、倒茶的手部关系、杯中落水、回壶、右手杯柄移到外缘、叶青双手离杯的动作链。两句台词与墙上标牌按原中文字及标点保留。[T]

三项媒体仅有用户文字声明，未提供可查看的真实文件。`portrait_ye` / `img-1`、`portrait_luo` / `img-2` 只承担身份和指定衣服参考；`room_music` / `audio-1` 被声明为已获许可、8 秒、无歌词、观众专属的配乐信号。许可与内容属于来源声明，本轮没有独立证明。[T]

### 2.2 Agent 作出的具体安排

公开合同要求说话者首个发声毫秒数。原任务只规定发声顺序和所属镜头，因此暂定罗成 **600 ms**、叶青 **4100 ms** 开始说话；正文对应约 0.6 秒、约 4.1 秒。这是编排选择，不能误称为用户原始规定或实际录音测量。两句均完整放在各自镜头内，不跨切、不截断。[A、P1]

另将两个中景写成稳定机位，罗成为日常语气、叶青为清楚温和的提醒，并把杯子在外缘稳定停留、罗成手仍握柄及茶壶已放回内侧写成结果细节。这些是为表达既定动作而作的具体化，不新增镜头或改切点。`author-arrangements.json` 独立记录这些安排；人物面容、发型、性别和配乐乐器/速度均未凭空补写。[A]

## 3. 模式与映射

选择 **Ref2VA**：图片是身份/衣服来源，没有实际首帧或尾帧；音频需要原信号复用。任务类型由实际用途生成 `[reference generation + audio reuse]`。两张 Picture 仅嵌在 Subject 来源定义中，没有单独帧锚条目，也没有图像对齐首行。[P2、C2、C3]

| 调用方顺序 | 稳定资产 ID / 版本 | 本次来源标签 | 内容角色 | 人物标签 / 说话者 |
| --- | --- | --- | --- | --- |
| 1 | portrait_ye / img-1 | `<Picture 1>` | 叶青身份、浅灰围裙 | `<Subject 1>` / S2 |
| 2 | portrait_luo / img-2 | `<Picture 2>` | 罗成身份、深蓝夹克 | `<Subject 2>` / S1 |
| 3 | room_music / audio-1 | `<Audio 1>` | 整段观众配乐信号 | 无人物说话者 |

Subject 顺序与 S 顺序独立：罗成先实际说话，所以 S1 属于罗成。资产编号只是本次序列化结果；变更素材排列时应重新编译标签，仍须保留稳定资产/人物 ID。[P1、P2、C2]

音频关系为 **`partially_copy` + `full_source: true` + `entire_soundtrack: false`**。原因是完整配乐作为一个声音层复用，最终音轨还添加对白、倒水、落壶、杯底轻擦；`fully_copy` 在此协议中指源音频成为完整最终音轨，不能正确表达本任务。未分配配乐 S 编号，也未补写歌词。[T、P2、C2]

## 4. 必保内容与验证范围

`preservation-trace.zh-CN.md` 与 `preservation-trace.json` 给出 17 项义务的来源、适用镜头、输出证据及审阅状态。脚本记录 ID 覆盖与镜头关系；Agent 另外对照全文核对了角色、位置、动作次序、手部关系、跨镜状态、配乐与原词。机器追溯不是自然语言语义证明。[C3、P1]

额外确定性核对见 `checks/delivery-consistency-check.json`：精确六字段、两镜标题、3.5 秒切点、首镜无时间戳、两句中文各一个 `<d>`、原标牌、人物/S 映射、17 个义务覆盖、未解析标记缺席、参数不变，以及没有错误接受导出分区，均通过。正文空白切词计数为 464，仅作为公开指南 350–500 词建议的参考，非 token 限制。[C6、P2]

| 层次 | 本轮结论 | 边界 |
| --- | --- | --- |
| 公共合同、绑定、字段、显式时间与引用 | 三模块程序检查通过，`passed_with_unverified` | 只核对显式声明及已实现规则 |
| 文字语义保真 | Agent 逐项审阅通过 | 未用生成视频验证 |
| 工作流导出 | 已执行尝试，因 runtime_unknown 阻塞 | 尚无部署字段与实际素材值 |
| 来源真实性、媒体内容与许可 | 未独立验证 | 只有用户文字与包内协议快照 |
| 实际后端、推理与成片 | 未执行、未验证 | 不声明 G2 全面通过或 G3/G4 通过 |

## 5. 可交接资料与具体缺项

本次已能交接纯正文、六字段 JSON、版本化能力/绑定/编译结果、全部请求/提案、已接受部分状态、目标参数、媒体清单、追溯表和实际失败诊断。`workflow-handoff.json` 是独立的交接清单，**不是可执行后端 payload**。[C1–C5]

实际导出还缺：后端/模型/工作流版本；部署对 Ref2VA、图片和音频通道的支持证据；时长、宽、高、帧率的节点/字段路径、类型、单位和取值范围；完整正文及模式的输入位置；素材槽位、序列格式与数量限制；三份真实媒体和带版本的 `asset_map` 值。官方提示词指南只能支持协议语法，不能证明本地字段或数值能力。[P1、P3]

为满足公开 Asset 合同必须有 URI 的条件，请求用了 `declared-media://...` 作为**仅供标识的未解析声明定位符**。它们不是实际文件、上传对象或已可访问地址。M11.4 的 `asset_map` 保持空对象，没有拿这些定位符伪装真实可提交素材。这是文字任务接入当前合同的边界，补齐媒体时须替换为真实、可核对的输入值。[P1、C2、C4]

补齐资料后应以当前接受版本继续修订来源/能力，重编译实际依赖分区，再尝试 M11.4；不得通过换成模拟 profile、改时长/尺寸/帧率、增减镜头或改台词来消除阻塞。[P1、P3]

## 6. 实际使用问题

1. **预期阻塞：部署未知。** 实际返回 `runtime_unknown`，路径 `/inputs/capability_profile/runtime`；这符合公开合同，不属于编译器故障。目标支持状态是未知，不能解释为 1080×1920 或 24 fps 不受支持。[C4]
2. **文本媒体声明需要 URI 字段。** 合同没有直接用本任务素材 ID 代替 URI 的输入形式；本次显式采用非执行定位符并在交接记录解释。这种声明仍然能通过结构检查，因此“程序通过”不代表媒体可访问。[P1、C2]
3. **最早发声时间需要补足。** 任务没有逐句精确发声起点，公开合同需要它；本次独立记录所作安排。声音节奏是否能自然容纳全部动作和台词，必须等待实际音频/视频测量。[A、P1]
4. **程序未证明语义/质量。** 义务覆盖只验证声明。两张图的真实身份、手部物理正确性、杯中落水、汉字清晰度和声画同步，仍是媒体观察事项。无需通过修改剧情来假装已经验证。[C1–C3]

本次当前包的公开命令正常运行，未发现需要修改技能包才能完成前三个分区的问题。M11.4 没有成功提案，因此没有运行其 `check`，也没有接受该分区。没有调用与本次需要无关的 `impact` 或执行额外媒体任务。

## 7. 文件与复查入口

| 文件/目录 | 内容 |
| --- | --- |
| model-prompt.txt / model-fields.json | 完整 H3 正文及六字段 |
| requests/ | 四个真实任务请求；前三个接受批次 |
| proposals/ | 三个实际成功提案及接受批次 |
| results/ | 路由、专业结果、导出错误和接受结果/状态 |
| checks/ | 三个公共 check 与交付一致性核对 |
| command-log.json / commands.zh-CN.md / logs/ | 实际命令、退出码、全部 stdout/stderr |
| reference-and-speaker-map.json | 参考、人物、声音与素材声明映射 |
| preservation-trace.* | 17 项必保内容的结构追溯与文字证据 |
| workflow-handoff.json / target-parameters.json | 当前交接范围、目标参数和具体缺项 |
| source-register.json / author-arrangements.json | 用户来源、官方快照来源、独立作者安排 |
| toolchain-snapshot.json | 当前包内容哈希与 Python 环境版本 |
| run_compilation.py / build_delivery.py | 本次调用器与交付生成器；均不修改技能包 |

### 证据索引

- **T**：原始 `task.md`，`source-register.json` 中 `task-plan` 保留全文、版本与哈希。
- **A**：`author-arrangements.json`；`source-register.json` 中 `agent-arrangement`。
- **P1**：指定技能包 `references/contract-guide.md`，尤其 3–6、9 节。
- **P2**：指定技能包 `references/h3-ref-official.txt`，尤其 1–6 节；固定官方提交 `199b7d0e1fd95e7b3eafa8c15eca692534142427`。
- **P3**：指定技能包 `references/runtime-export.md` 与 `references/capability-and-version.md`。
- **C1–C3**：`checks/m11-1-check.json`、`checks/m11-2-check.json`、`checks/m11-3-check.json`，以及同编号请求/提案与 `results` 专业结果。
- **C4**：`requests/m11-4-request.json` 与 `results/m11-4-export-blocked.json`。
- **C5**：`results/accept-result.json` 与 `results/accepted-state.json`。
- **C6**：`checks/delivery-consistency-check.json` 与 `preservation-trace.json`。
''')
print(json.dumps({'status':'pass','delivery_checks':len(checks),'obligations':len(trace),'detailed_description_whitespace_words':len(detail.split()),'accepted_status':state['status']},ensure_ascii=False))
