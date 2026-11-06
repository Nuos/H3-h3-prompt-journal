# 8 秒茶铺片段：H3 文本编译交付

## 1. 交付结论

已用指定技能包的当前公开脚本完成 **M11.1 能力登记、M11.2 模式与参考绑定、M11.3 正文编译**。最终三份提案均与真实请求核对，返回 `valid: true`、`passed_with_unverified`；父接受完成，状态为 **version 2 / partial**。M11.4 已实际尝试，因 `runtime_unknown` 退出 2。没有可执行工作流请求，也没有实际视频。[C1–C5]

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

`preservation-trace.zh-CN.md` 与 `preservation-trace.json` 给出 17 项义务的来源、适用镜头、输出证据及最终审阅状态。脚本记录 ID 覆盖与镜头关系；Agent 另外对照全文核对了角色、位置、动作次序、手部关系、跨镜状态、配乐与原词。机器追溯不是自然语言语义证明。[C3、P1]

**有监督修订记录：** 首轮三个机器检查已通过，但根 Agent 逐字段审阅发现 `overall_soundscape` 混入了对白同步和人声清晰度要求，违反该字段的环境/物理声音范围。第二轮把这些要求分别放回两个 `detailed_description` 镜头，音场汇总只留倒水、落壶、杯底轻擦。首轮完整记录保存在 `revision-history/round-1/`；最终使用新请求 ID `tea-m11-*-v2` 和当前 base_version 1 重跑，再接受为 version 2。技能入口随后补充了明确的声音分层提示，脚本未变，最终包哈希已重新记录。不能把首轮机器通过表述为首轮全部语义正确。[R、C1–C5]

额外确定性核对见 `checks/delivery-consistency-check.json`：精确六字段、两镜标题、3.5 秒切点、首镜无时间戳、两句中文各一个 `<d>`、原标牌、人物/S 映射、17 个义务覆盖、未解析标记缺席、参数不变、最终声音字段位置，以及没有错误接受导出分区，均通过。正文空白切词计数为 490，仅作为公开指南 350–500 词建议的参考，非 token 限制。[C6、P2]

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
5. **首轮字段范围问题由独立审阅发现。** 当对白同步/清晰度写入 `overall_soundscape` 时，当前机器检查未拒绝；本轮按根 Agent 审阅修订。程序能检查对白标记位置，不能全面判定普通英文说明究竟属于哪个声音层。该问题属于本次文本编排错误与自动检查的语义边界，最终已经纠正。[R]

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
| revision-notes.json / revision-history/round-1/ | 根 Agent 审阅触发的第二轮修订说明及首轮原始记录 |
| run_compilation.py / build_delivery.py | 本次调用器与交付生成器；均不修改技能包 |

### 证据索引

- **T**：原始 `task.md`，`source-register.json` 中 `task-plan` 保留全文、版本与哈希。
- **A**：`author-arrangements.json`；`source-register.json` 中 `agent-arrangement`。
- **R**：`revision-notes.json`、`revision-history/round-1/` 与第二轮请求/提案/状态；依据包内官方指南第 6 节及 SKILL.md 声音分层要求。
- **P1**：指定技能包 `references/contract-guide.md`，尤其 3–6、9 节。
- **P2**：指定技能包 `references/h3-ref-official.txt`，尤其 1–6 节；固定官方提交 `199b7d0e1fd95e7b3eafa8c15eca692534142427`。
- **P3**：指定技能包 `references/runtime-export.md` 与 `references/capability-and-version.md`。
- **C1–C3**：`checks/m11-1-check.json`、`checks/m11-2-check.json`、`checks/m11-3-check.json`，以及同编号请求/提案与 `results` 专业结果。
- **C4**：`requests/m11-4-request.json` 与 `results/m11-4-export-blocked.json`。
- **C5**：`results/accept-result.json` 与 `results/accepted-state.json`。
- **C6**：`checks/delivery-consistency-check.json` 与 `preservation-trace.json`。
