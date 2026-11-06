# M11 公共合同与运行命令

**核心摘要：** 四个子模块通过同一版本化请求信封独立运行，分别形成能力、绑定、正文和任务导出分区；父模块以真实原请求重新核对后接受。

**关键结论：** 脚本编译 Agent 已组织好的语义资料；不执行自然语言创作、媒体解析、工作流推理或其他模块。已有兼容结果可以替代上游重跑。

**关键词：** M11Request、M11Proposal、M11State、1.0.0、独立调用、版本、幂等。

**目录导航：** 1. 环境与版本；2. 信封；3. 四个独立输入；4. 语义片段；5. 参数；6. 父接受；7. 命令；8. 上游适配；9. 结果范围。

## 1. 环境与版本

使用 Python 3.10+ 标准库。复制整个 `h3-model-protocol/` 目录即可使用；不导入 M1—M10 的私有脚本或外部仓库资源。程序只读取显式 JSON 与包内资料，将 JSON 结果写到 stdout，不覆盖输入、不联网、不生成媒体。

本合同与路由版本均为 `1.0.0`。目录技能版本为 `0.1.0`，与合同版本分别管理。精确数据类型、必需字段及允许值见 [contracts.json](contracts.json)，职责与路由见 [module-registry.json](module-registry.json)。这些都是本项目内部工程对象，不新增 H3 原生字段。

JSON 中重复对象键、非有限数、错误字段类型、未知字段和未支持的合同版本应被拒绝。带版本的显式适配可以迁移外部数据；不能只改版本字符串后把旧结构当作兼容。

## 2. 请求、提案与状态信封

请求使用 `kind: M11Request`，携带 `contract_version / route_version / work_id / base_version / request_id / target / sources / inputs`。`target` 为四个子模块之一。`sources` 是来源 ID 到 `kind / locator / version / excerpt` 的映射；来源陈述与真实执行证据分别保存。

`propose` 根据请求确定性形成 `M11Proposal`。提案保留原请求标识、完整输入上下文与来源，只在 `changes` 写入对应独占分区。提案不是第二个可以任意修改语义的入口；创作语义改变先修订请求。

`check` 必须同时取得真实原请求，重新计算并核对候选结果。它不接受提案凭自己的 `context` 自证授权。父状态 `M11State` 的对外对象类型为 `CompilationResult`；可以只有本次接受的部分分区，不能把空分区解释成已完成。

专业结果的 `evidence_snapshot` 保存实际消费来源的版本与内容摘要，并参与结果指纹。独立下游不能在保留旧结果的同时无声替换它依赖的来源。摘要用于检测声明变化，不证明外部文档、媒体或部署声明真实。

| 子模块 | `changes` 唯一键 | 专业产物 |
| --- | --- | --- |
| M11.1 | `capability_profile` | CapabilityProfile |
| M11.2 | `reference_binding` | ReferenceBinding |
| M11.3 | `prompt_compilation` | PromptCompilation |
| M11.4 | `task_export` | TaskExport |

## 3. 四个独立输入

| 入口 | `inputs` 中的公开字段 | 含义与缺项处理 |
| --- | --- | --- |
| M11.1 | `profile` | 后端／模型／工作流／协议版本、来源、协议模式和运行能力；真实运行未知可以明确登记 |
| M11.2 | `capability_profile / plan / assets / subjects / reference_items / audio_bindings / speakers` | 当前任务时长与真实镜头、素材用途及版本、抽象内容、独立参考角色、音频关系、实际发声顺序；无关集合显式为空 |
| M11.3 | `binding / fragments / obligations / utterances / complete_silence / music_present`，可选 `visible_text` | 经确认的绑定、自足英文片段、必保信息、原台词、静音和配乐决定；输入已经具备即可独立编译 |
| M11.4 | `compilation / capability_profile / parameters / asset_map` | 经确认编译、目标版本的运行映射、实际参数及素材值；未知运行映射阻塞导出 |

“独立”表示可以直接提供兼容外部结果，并经过同样核验；不表示可以省略本职责实际必需的信息。下游结果保留必要输入声明，以便重新验证来源和编译关系；它不是对外部数据真实性的数字签名。

### M11.1 能力资料

profile 区分协议能力与运行能力。当前 `protocol_version` 精确固定为包内官方来源提交 `199b7d0e1fd95e7b3eafa8c15eca692534142427`，不能用另一个版本号冒充已支持语法。协议部分固定五种输入模式的合法格式；运行部分记录目标版本实际支持的模式、参数位置、必需参数、媒体位置与有依据的限制。`runtime.status: unknown` 表示实际运行资料不足，可用于协议阶段，不能制造可执行导出。

模拟运行映射明确标记 `simulation`。仅有例子数值或案例经验时，不填写成真实 `production` 能力；生产字段须引用标记为 `deployment` 或 `workflow` 的来源，官方提示词来源不能替代部署字段证据。若来源提供了声称已验证的生产资料，脚本仍只检查显式声明和一致性，没有在本机复现该声明。

### M11.2 模式、资产、内容与声音

`plan.duration_ms` 和各镜 `start_ms` 使用生成局部毫秒。第一镜从 0 开始，后续时刻严格递增且小于有效时长。`shot_id` 保留 M9 的真实镜头身份，不根据动作阶段的数量增镜。

资产记录稳定 ID、媒体类型、URI、版本、用途和来源。URI 是运行输入定位声明，不代表脚本已下载、解码或观察文件。Subject 记录稳定内容 ID、来源资产、已授权描述、保留关系和出现镜头；独立参考项只为实际帧／分镜／视频结构等角色登记。

音频绑定明确复制／参考、完整源信号／完整最终轨、额外／替换音层以及必要的说话者关系。Video 和其同步 Audio 共用来源时，保留各自标签与通道；编号不表示配对。没有启用同步音轨，不从视频文件自动产生 Audio。

`speakers` 按已确认实际发声起点生成 S 序号，不能以资产列表或 Subject 编号代替。是否真实发声由 M6／用户语义资料决定；复用配乐中的歌词提示不自动建立人物声音源。

## 4. M11.3 片段、原词与追溯

`fragments` 包含整体风格、必要的摘要、按真实镜头排列的正文、环境物理声音和配乐文字。Agent 先按领域计划完成这些英文内容，再由脚本封装字段与编号。脚本不会从任意散文自动推导完整电影语义。

使用合同规定的稳定引用标记：

| 标记 | 解析依据 |
| --- | --- |
| `{{ref:稳定引用ID}}` | 本次绑定中的 Subject，或只有一个启用通道的资产映射 |
| `{{ref:资产ID.video}}`、`{{ref:资产ID.audio}}` | 同一视频资产同时启用视觉与同步音频时，显式选择独立通道；不以相同编号推定配对 |
| `{{speaker:声音源ID}}` | 本次实际发声顺序对应的 S 编号 |
| `{{utterance:发声事件ID}}` | 完整原词、语言、说话者及必要的发声格式 |
| `{{shot:镜头ID}}` | 当前任务内的真实 Shot 编号 |

不要手填不受映射管理的序号。未定义引用、未解析标记或模板占位符阻止正式模型输出。未知占位语法不能被当作普通正文悄悄保留。

`obligations` 为必须保留的内容登记 ID、说明和适用镜头；镜头片段记录自己覆盖的义务 ID。机器可核验 ID 覆盖和作用域，但“这句话是否真的完成了该义务”需要 Agent 对照审阅。声明有覆盖不等于语义必然合格。

`utterances` 保留发声事件 ID、英文语言名、文字、局部 `start_ms` 和实际 `shot_id`，并按来源区分新生成与原音轨复制。起点必须落在本镜范围内，正文插入顺序应与发声先后相符；实际声音源的首个言语事件与 `speakers.first_vocal_ms` 一致。若源音频原文需要按 Ref2VA 的标点规则规范化，必须携带 `source_text` 和明确 `punctuation_change`；不能静默翻译、改词或补猜听不清的内容。

| 发声来源 | 合同要求 | 编排与审计 |
| --- | --- | --- |
| `origin: generated`（默认） | 必须有 `speaker_id`；重演或仅参考音色也属于这一类 | 不把源信号复制与新录／重演混为一谈 |
| `origin: copied_audio`，具体人物／旁白发声 | `audio_asset_id / source_text / source_language / source_refs`，以及实际 `speaker_id` | Audio 必须是已启用的 reuse 信号；原词、语言、声音源和复制时间窗一致 |
| `origin: copied_audio`，纯 BGM／完整音轨中的语词提示 | 同样保留音轨与原词来源，不指定虚构 `speaker_id` | 编译为 Audio 来源加 `<d>`，不额外产生 S；Audio 已绑定具体声音源时不能省略该源 |

完整复制的最终音轨可以已经包含对白；只有从同一原轨直接复制的发声才能与该 `fully_copy` 声明同时成立。新增或重演的发声属于新的声音层。`utterance_source_trace` 记录上述来源关系；它不等于本轮听过源音频。

所有实际台词／歌词都通过逐镜发声事件进入 `<d>`，不使用 `audio_bindings.lyrics`。声音汇总、参考定义和摘要不复述完整原词；程序限制发声标记的结构位置，Agent 另审阅自然语言是否误抄台词，不能以字符串偶然重合代替语义判断。

有实际说话者的每条发声标记之前，最近的 `{{speaker:ID}}` 必须指向该声音源。画外音选择 `mode: off_screen_voiceover`，在对应说话者与发声之间写入官方短语；若声明 `visible_lips_subject`，编译器会在该条 `</d>` 后补上对应可见主体的闭嘴说明。跨镜同句使用相邻镜头之间互相对应的 `continues_from / continues_to`，保留相同发声／复制关系；视频末尾截断使用 `cutoff`。

首尾帧首行由实际末镜与有效时长生成，单独放在 `alignment_instruction`；它在完整 `rendered_prompt` 的最前面，与后续字段之间留一空行，不计入三字段或六字段集合。无对齐首行的模式使用 null。`fields` 与 `field_order` 保存精确字段集合，`rendered_prompt` 是包含字段名的完整纯模型文本。基础模式和 Ref2VA 的风格位置按固定协议处理；合同元数据及独立追溯不进入模型内容。

## 5. M11.4 参数与素材导出

`parameters` 表示计划目标，映射位置、类型、单位和限制由 profile 中相应版本的运行资料决定。生成时长必须与已经编译的任务一致；存在毫秒／秒换算时应精确且可追溯，不用不透明的默认值。

`asset_map` 将已有稳定资产 ID 映射为实际运行输入值。缺少、增加或替换素材都要核对绑定；不能只让标签看起来连续而传入另一张图。没有运行证据时，素材可访问性和后端实际加载仍属于执行方待验事项。

输出任务包与其 provenance／诊断分开。模拟资料始终保留模拟身份；未知 profile 不能导出可执行请求。即使生产资料齐全，导出也只表示按该资料生成了任务输入，不等于已经提交或运行。

本版参数适配器支持显式 JSON Pointer 对象路径或单个字面字段名；提示词映射必须声明 `runtime.prompt.format: text`，写入完整 `rendered_prompt`，保留基础模式的对齐首行。媒体映射须声明 `runtime.media.format: ordered_channel_objects`，写入带 `value / channel / label / input_index` 的有序对象数组。它没有实现数组索引路径、任意工作流节点执行或所有后端专用封装。遇到其他封装，保留已编译结果并要求有依据的适配，不以删首行或新增 H3 字段凑合。

## 6. 父接受、幂等与失效

`accept` 同时接收提案、真实原请求和当前 state。检查工作 ID、当前基版本、请求与提案身份、来源、单一分区责任和组合一致性。失败不返回部分接受状态，也不覆盖任何输入文件。

同一来源 ID 与版本的内容必须稳定。相同已接受请求和完整结果重试返回同一状态，`idempotent: true`；改内容复用旧 ID、混合旧重试与新修订、旧基版本和同批双写应拒绝。子模块接受不授予修改 M1—M10 权威字段的许可。

已接受结果登记实际读取依赖，能力／绑定／正文变化使真正依赖它的下游分区失效。独立外部输入没有读取的兄弟分区，不因兄弟存在而获得隐含依赖。已经 stale 的依赖不能被后续结果无声重新宣称有效。

`impact` 只列出两个 JSON 对象实际变化的路径并要求复查；它不推断这些差异的领域语义、不计算外部消费者依赖，也不调用子模块。实际已接受分区的来源／指纹失效闭包由 `accept` 检查。这个本地适配器不登记或激活外部消费者。

## 7. 命令与样例

在技能目录运行：

```bash
python scripts/m11_contract.py --help
python scripts/m11_contract.py route assets/examples/m11-1-request.json
python scripts/m11_contract.py propose assets/examples/m11-1-request.json > /tmp/m11-1-proposal.json
python scripts/m11_contract.py check /tmp/m11-1-proposal.json --request assets/examples/m11-1-request.json
python scripts/m11_contract.py accept assets/examples/proposals.json --requests assets/examples/requests.json --state assets/examples/state-empty.json
python scripts/m11_contract.py propose assets/examples/ref2va-request.json
```

五模式编译请求分别位于 `assets/examples/t2va-request.json`、`i2va-request.json`、`fl2va-request.json`、`l2va-request.json`、`ref2va-request.json`。它们提供完整兼容输入，支持不先运行 M11.1／M11.2 的独立 M11.3 调用。`music-reference-request.json` 示范只参考音乐风格而不搬入源歌词；`music-cue-request.json` 示范直接复用 BGM 的 Audio 语词提示不自动建立人物说话者；`fullcopy-dialogue-request.json` 示范完整最终音轨中已经包含原对白。

Python API 为 `route(request)`、`propose(request)`、`check(proposal, request)`、`accept(proposals, requests, state)`、`impact(before, after)`。公开输入失败抛出可定位的 `ContractError`，CLI 输出结构化失败并返回 2；成功返回 0。获取 `propose` 输出并重定向到文件是调用方的显式操作，脚本本身不写文件。

完整样例链见 `assets/examples/requests.json` 和 `assets/examples/proposals.json`；空父状态见 `assets/examples/state-empty.json`。四个 `m11-N-request.json` 可分别调用。协议资料不足时的模板见 `assets/profiles/official-protocol-only.json`，模拟完整运行映射见 `assets/profiles/simulation.json`。所有合成主体、源 URI、参数和能力演示保留工程夹具身份，不是原案媒体或生产运行证据。

## 8. M1—M10 的公开适配边界

M11 接受本合同的显式投影，不宣称所有旧模块 JSON 可直接互换。适配时保留来源对象／版本、原 ID、单位和字段权威，并说明真正读取的字段。

| 已有对象／公开输出 | M11 消费方式 | 不应改变 |
| --- | --- | --- |
| M2 资产、主体、权限 | 资产／Subject／参考用途与来源投影 | 资产身份、属性授权、实际通道 |
| M3／M4／M5 空间、动作、摄影 | 已确认的逐镜画面片段与义务 | 位置、动作因果、相机行为与观看任务 |
| M6 声音与原词 | 声源、发声事件、Audio 策略、声音片段 | 台词、歌词角色、音轨复制／参考决定 |
| M7 时间 | 目标生成局部毫秒及切点，保留原时间域映射来源 | 源时间、作品时间与生成时间之间的权威关系 |
| M8 状态／连续性 | 起末态和允许变化进入相应镜头及义务 | 计划状态与实际媒体观察的区别 |
| M9 `m11_handoffs` | `task_id / shot_ids / mode_intent` 进入本次任务声明；保留 `owner / source_refs` | 镜头结构、编辑选择和分段决定 |
| M9 `capability_context.values.profiles[]` | 将 `backend / workflow / supported_modes / duration_limit / max_shots / supports_same_shot_split` 及状态和来源作为有边界的规划资料 | `known` 或合成资料不能自动升级为实际后端支持；缺少模型／工作流版本或参数证据时继续未确认 |
| M10 LookPlan | 展开本生成任务实际生效的风格、光照、调色、材质／效果，写入适用片段 | 身份属性、风格层级、例外与持续范围 |

上游原生版本可能是整数，本包来源版本使用字符串时应显式保留转换规则。项目对象版本相容不要求各模块修订号数值相等。

## 9. 结果与验证范围

`route` 的 `ready` 只表示入口条件，`invocation_status` 保持 `not_invoked`。`check` 的 `valid: true` 与 `passed_with_unverified` 表示可确定检查通过，仍保留自由文本语义、来源真实性、真实工作流及媒体效果未验证。`accept` 输出新的 `.state`：空初态为 `draft`，部分分区为 `partial`，四分区齐备为 `compiled_unexecuted`；这些状态均不签发全部关卡通过。

专业审计的 `pass / fail / unverified / not_applicable / stale` 含义见 [审计与交接](audit-and-handoff.md)。缺少相关证据时不能以 not_applicable 隐去；合同格式通过也不能替代能力、语义或媒体证据。

对于当前机读合同尚不能表示的合法 H3 表达，Agent 应明确指出实现缺口并保留创作语义，可形成单独人工编排候选；不得伪造机器检查通过或把实现限制写成官方模型限制。
