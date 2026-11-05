# M2 案例证据与适用边界

## 核心摘要

按当前任务逐项分配“什么素材为哪个实体、哪个属性、哪个范围提供依据”。素材出现、素材可访问、内容已观察、属性获准继承、模型实际采用，是五个不同事实。执行 M2 时只接受有来源的声明与观察；将未解决的权限竞争返回责任方。

**来源基线：** `Nuos/H3-h3-prompt-journal@faa8edc311589d68d37e93524c7cb8e553fff857`；`case-studies` Git tree 为 `70a8a2a632d633f5d532db23cad99c772dc23026`。

**内容边界：** 29 个案例目录中的 97 份文本，加共享词汇索引 1 份，共 98 份；其中 15 个案例为 2026-10。逐文件路径、字节数、SHA-256、Git blob、实际阅读方式见 `case-index.json`。29 份案例 README、两份 methodology 及指定重点提示词已经语义阅读；其余文件按索引记录全文机器读取、关键词检索或局部阅读，**不称为 98 份逐字语义审定**。29 份受跟踪媒体文件没有读取；本地稀疏检出未含媒体不等于远端没有媒体。

**证据分层：** 以下“F”仅指源文本确实这样写；作者所述成功率、实测、成片效果仍为作者报告。“D”是本技能从文本提炼的工程规则。结构检查、语义执行、媒体观察各自记录；文字样例通过不能提升为视频效果通过。Anthropic 与 MiniMax 官方资料只负责格式、模式和协议，不成为本案例集的新创作样本。

**关键词：** 资产登记、稳定身份、参考权限、属性范围、来源状态、版本冲突、动作参考、音频用途。

## 目录导航

1. 读取路由
2. 十二条可执行规则
3. 已知冲突及返回位置
4. 十个代表任务
5. 事实与验证边界
6. 固定来源

## 1. 读取路由

| 当前问题 | 优先规则 | 重点来源 |
|---|---|---|
| 素材缺失、作者声称观察过、原文件仅在本地 | C01、C10 | E05、E07、E08、E15 |
| 一图多人、多图同人、身份与画面位置混淆 | C02、C03、C04 | E01、E02、E09、E10 |
| 保留身份但更换场景、动作迁移、道具状态 | C05、C06、C07 | E04、E05、E06、E13 |
| 音乐复制、仅作节奏、无音频输入、歌词泄漏 | C08、C11、C12 | E03、E11、E12、E14 |
| 分段参考范围或摘要与提示词不一致 | C09、C12 | E02、E03、E09 |

只读当前需要的证据；不因加载本文件而执行全部案例、运行 ComfyUI 或读取全部媒体。C01—C12 为本包的 D 类规则标识，不是 H3 字段或官方 Label。

## 2. 十二条可执行规则

### C01｜分别登记存在、访问、观察与用途（M2.1）

- **F：** 神裂案例 README 的 Inputs 与 Assets 明说真人成片、参考图、音频为本地文件、不随公开仓库分发；宋韵案例同样要求生成时自行提供素材。E05、E15。
- **D：** 为每个输入保留稳定资产 ID、来源定位、版本/哈希依据、可访问性及观察来源；文件名、README 参数或加载器控件不构成已打开媒体的证据。
- **适用边界：** “登记缺失素材”可以完成；依赖该素材的身份比对、编译就绪或媒体结论仍应未验证。纯文本生成未要求外部素材时，不制造缺图阻塞。

### C02｜图片数量与实体数量分别处理（M2.2）

- **F：** 四主体 prompt 第 8—18 行以一张 Picture 1 区分四人；三姿态 prompt 第 3—9 行明确“三张图是同一人”。E02、E10。
- **D：** 支持一资产绑定多实体、多资产绑定同一实体；保存源图区域/可辨认特征与稳定实体 ID 的关系。未知区域写未知，不凭文本捏造坐标。
- **适用边界：** 源图“最左侧”用于辨认来源，不能把目标镜头动态站位写进永久身份；也不能从 Picture/Subject 编号推断人数、身份或实体类型。

### C03｜把每份参考拆成属性授权与排除项（M2.3）

- **F：** 半身六段 README 的 Grants/Denies 表与 prompt 第 7—45 行分别指定面部、身体、服装、环境，明确排除起手姿态；下山 README 第 25—32 行按正面服装与脸/背部分权。E01、E03。
- **D：** 对每个实体记录资产、允许继承属性、明确禁止继承属性、生效范围及依据；未声明的控制权保持待定，不把“参考这张图”解释成全属性授权。
- **适用边界：** 一个资产可以承担多项明确职责；“每图只管一件事”是分权表达，不能限制为一图仅一个属性。

### C04｜单独决定姿态、首帧与摄影权限（M2.2、M2.3）

- **F：** 半身六段 prompt 明说 Picture 1 “NOT an opening-frame reference”，并将开场交给书面编舞；三姿态案例则有意让三图提供姿态路标。E01、E10。
- **D：** 身份授权不自动包含首帧姿态、构图或摄影。需要姿态继承时明确授权，并把动作起态交 M4/M8、摄影要求交 M5。
- **适用边界：** 不禁止所有姿态参考。若实际模式把图片作为强首帧条件，向 M11 核对能力及模式冲突，不能仅写一句否定句便宣称解除后端条件。

### C05｜分别决定人物与世界是否继承（M2.3）

- **F：** 神裂 methodology 第二、八节对比“人物+晴日海滩均锁定”与“人物保留、背景重建”；夏日四段 prompt 第 20—22 行只保留身份、重建环境。E05、E06。
- **D：** 将人物、服装、道具、场景、光线、摄影分别列权；固定场景与替换场景须有相容的当前版本决定。
- **适用边界：** 不把“Picture 1 是唯一视觉权威”设为跨案例默认；新场景的空间计划归 M3、风格计划归 M10。身份锁定也不自动禁止获准的服装变化。

### C06｜动作视频只输出获准的运动信息（M2.1、M2.3）

- **F：** 动作迁移 prompt 的 STRICT REFERENCE SEPARATION 把图、视频首帧、视频后续、音频分开；OPENING POSE TRANSFER 明许开场身体机制，禁止源视频身份和环境。E04。
- **D：** 分别登记视频允许贡献的动作、摄影、初态、时间依据；源视频演员可以只是动作来源，不自动成为第二个目标实体。图的世界与视频的运动不能整体捆绑继承。
- **适用边界：** 保留“首帧几何”和“开场体态”两项权限，不只抄小标题中的 CAMERA GEOMETRY ONLY；M4/M5/M7 负责适配，M11 负责实际视频/音频通道。此案例不能证明系统已具备自动动捕或完整逆向解析能力。

### C07｜分开外观恒定项与随时间变化的状态（M2.3）

- **F：** 神裂 README 第 53—61 行规定剑鞘外观取自图、SEG03 起持刀与空鞘状态取自全曲计划；三袜案例只允许镜头间改变袜饰。E05、E08。
- **D：** 登记哪些属性固定、哪些属性可在什么范围改变，向 M8 交付变化许可及来源；不让参考图初始状态覆盖当前状态。
- **适用边界：** “保持身份”不等于所有道具和服装永不变化；状态时间表及具体握持过程归 M8/M4。六 LOOK 的具体袜饰不是本技能默认内容。E13。

### C08｜明确每条声音素材的使用目的（M2.1、M2.3）

- **F：** 半身六段直接复用音轨；紫纱七段注明“No signal copy”并后期铺原曲；台灯 A/B 的 Inputs 明确无外部音频、自建音乐。E01、E11、E12。
- **D：** 分开记录完整/局部信号复制、仅节奏参考、声音身份参考和生成声音意图；若只引用源窗口，记录所属资产及源时间域，不将局部 0 秒误当全曲 0 秒。
- **适用边界：** M2 提供授权和来源；M6 决定声音语义，M7 负责权威排时，M9 负责后期装配，M11 负责标签。不把所有 MV 强制为音轨复制、禁对白或禁口型。

### C09｜给引用设定实体、镜头、段落与阶段范围（M2.3）

- **F：** 帆板案例 README Layer 1/2 指定 Picture 2 是人物/装备图而非分镜；Picture 3 仅用于第一、二段，第三段主动取消。E09。
- **D：** 记录“参考什么、作用于谁、何处、何时”；独立生成时提供本段必需资产及权限投影，不能假定前一段图片或指令仍在上下文中。
- **适用边界：** 取消某段参考是明确创作决定，不是缺失资产的自动补救；不能在同一未授权变更里悄悄删除必需参考。

### C10｜解析观察保留证据状态与不确定性（M2.1）

- **F：** 水岸 README 单镜头验证流程报告低阈值命中被逐帧排除；三袜 README 报告同景硬切被粗采样漏掉。古典武侠 methodology 第 13 条要求不把推算拍点冒充实测。E07、E08、E16。
- **D：** 接收解析器候选时保留采样方法、源区间、置信限制、观察者与版本；文本转述、推断和直接媒体观察分别登记，冲突候选不自动变成目标作品事实。
- **适用边界：** 0.27、0.06、0.08 是案例设置，不是通用阈值。M2 不把源片解析报告升级为本轮独立复测；实际输出媒体观察仍归 M12。

### C11｜来源内容不自动成为目标人物、道具或声音（M2.2、M2.3）

- **F：** 下山明确歌词不增加人物/物件；神裂只借剑路不带入敌人/魔法；纯 T2VA 恶作剧案例没有参考图，并把画外操作者登记为第三角色。E03、E05、E14。
- **D：** 分开“来源中出现”“分析文本提到”和“目标作品获准出现”。需要目标实体时按当前任务登记，含画外行动者；不把来源演员、歌词意象、相机术语自动实体化。
- **适用边界：** 不继承某案例的全局零路人/固定人数。水上综艺允许生成观众与环境，说明任务可以显式授权未被图片限定的内容。E17。

### C12｜冲突定位到属性、范围与版本（M2.1—M2.3）

- **F：** 下山同段音频声明互斥；四主体摘要禁交叉而具体 SEG10 要求穿越中心；动作迁移正文参数与连接控件存在差异，见第 3 节。
- **D：** 保留两条原始声明及依据，识别是否真为同属性、同用途、同对象、同范围、同版本的竞争；依据用户已确认的取舍处理，否则返回具体缺口。不要默认 README、prompt 或“更新的口号”天然优先。
- **适用边界：** 有意的局部例外与真正矛盾分别处理；只阻塞依赖未决项的结果。不得用重试、另换参考或重述“绝对权威”掩盖缺口。

## 3. 已知冲突及返回位置

| 编号 | 可定位的原文差异 | 执行时的处理 |
|---|---|---|
| X01 音频策略互斥 | 下山 `prompt.md` SEG01 第 23—25 行“仅节奏 / No signal copy”，第 28、32、67、69 行又写完整音轨复用 / `fully_copy`。E03 | 保留两条声音用途主张；未有授权取舍时不得输出已解决的复制策略。返回 M2.3/M6，影响标签时再交 M11。 |
| X02 环境权限竞争 | 下山 README 第 25—30 行：图 1 管正面服装/身体、不管环境；prompt 第 34 行又为光色与环境标注“from Picture 1”。E03 | 区分环境几何、光线与调色是否是明确例外；不把整张图升格为全环境权威。待定部分交 M2.3/M10。 |
| X03 身份与路线混用 | 四主体 README 第 78—79 行禁止中心交叉；prompt 第 36、68、79 行明确 SEG10 中心穿越。E02 | 稳定身份映射可保留，路线决策应回 M3/M4 对照镜头范围；不得把源图位置固定为永久站位。 |
| X04 标题缩写与细项不同 | 动作迁移 prompt 第 158 行说首帧“CAMERA GEOMETRY ONLY”，第 138—153、279—302 行包含开场身体机制。E04 | 以属性表保留“摄影几何”和“获准开场体态”两项，禁止据缩写删除后者或自动继承视觉身份。 |
| X05 工作流控件不等于运行值 | 动作迁移 README 第 42 行写 Duration=9s/124 帧@24；JSON 的 136/191 节点虽有 124 控件字面值，length 实际连接 131/188 运算节点，Duration 节点 132 为 9。E04 | 按文件连线静态代入得到 226 帧，不能把 124 当有效运行值；也不据这一静态计算声称已经执行。版本化能力/运行核验交 M11。8—9 秒不升级为全 H3 限制。 |
| X06 音频通道混用风险 | 同一工作流 LoadAudio 155 经 link 308 接 136 的 `ref_video_audio_0`，经 link 387 接 191 的 `ref_audio_0`。E04 | 登记资产相同、绑定通道不同的事实；M2 保留用途，M11 核对所选分支及实际官方语义，不以文件名或提示词 `<Audio 1>` 猜标签。 |

## 4. 十个代表任务

下表是执行/评估输入的设计，**不是已经运行的测试结果**。资产内容未提供时，用源文声明建立待验证记录，不伪造视觉观察。

| 任务 | 应形成的 M2 结果 | 应被拦截的错误 | 来源 |
|---|---|---|---|
| 面部图+全身图，仅编排新起手 | 一个实体、两资产、分属性权限 | 身份图自动变首帧姿态 | E01 |
| 合照四人换层/交叉 | 四稳定实体、源图区域与身份绑定 | 左侧槽位被当成永久人物 ID | E02 |
| 正面无头图+脸/背三视图 | 同人多来源、前后属性职责及缺口 | 从无头素材声称已观察脸部 | E03 |
| 图的人物世界+视频动作+独立音频 | 三类参考分权，视频演员排除于目标身份 | 原视频服装、场景随动作泄漏 | E04 |
| 剑已出鞘的第三段 | 图提供外观、状态许可引用当前计划 | 每段重置为参考图收刀状态 | E05 |
| 同人跨泳池与海滩 | 身份保留、场景重建及服装范围待核 | 将人物图原背景视为绝对世界 | E06 |
| 只提交已有单镜头分析报告 | 带来源和方法的候选/报告状态 | 把“报告说逐帧检查过”写成本轮媒体复测 | E07 |
| 三个袜饰状态分镜 | 相同人物、变化属性与每镜作用域 | 人物复制或全局服装锁阻断合法变装 | E08 |
| 帆板第三段取消摄影指导图 | 当前段引用集合明确，装备图仍有效 | 沿用前两段 Picture 3，或删掉未授权资产 | E09 |
| 三张图为同人不同姿态 | 一个实体、三个授权姿态路标 | 自动建三人，或统一禁止姿态继承 | E10 |

## 5. 事实与验证边界

1. 全部 98 份文本均完整读取以计算哈希并检索；这只证明来源覆盖与字节可追溯，不证明全部规则语义正确。
2. `case-index.json` 的 `semantic_review` 区分全文、片段、连接字段和关键词索引。译文/词汇增补是衍生说明，不能重复计为独立成功样本。
3. 本文件没有读取图像、视频或音频，没有运行 H3、ComfyUI、切镜检测、节拍分析或成片评估；案例作者声称的“near zero drift”等不得写成本轮结果。
4. 固定案例内容不等于当前任务权限。用户明确指令优先；新的任务选择、实物素材或能力证据到来后，形成有来源的新版本，并复核真正受影响的范围。
5. 原案例参数、人数、固定镜头、零背景人物、禁口型、动作预算及后期服务均保留适用条件，不成为 M2 的隐藏全局要求。

## 6. 固定来源

所有链接均固定到读取提交；下面各目录的精确文本文件及哈希均列于 `case-index.json`。正文的文件名、行号与章节用于定位证据，链接集中于本节。

- **E01 半身六段**：[README 与 prompt](https://github.com/Nuos/H3-h3-prompt-journal/tree/faa8edc311589d68d37e93524c7cb8e553fff857/case-studies/2026-10-identity-only-half-body-dance-six-segment)。重点：README Grants/Denies；prompt 第 7—84 行。
- **E02 四主体队形**：[README 与 prompt](https://github.com/Nuos/H3-h3-prompt-journal/tree/faa8edc311589d68d37e93524c7cb8e553fff857/case-studies/2026-10-four-subject-formation-choreography)。重点：prompt 第 8—38 行、FORMATION MAP；README 第 78—79 行。
- **E03 下山十二段**：[README 与 prompt](https://github.com/Nuos/H3-h3-prompt-journal/tree/faa8edc311589d68d37e93524c7cb8e553fff857/case-studies/2026-10-xiashan-veiled-solo-twelve-segment)。重点：README 双图分权与歌词三层；prompt SEGMENT 01 第 17—69 行。
- **E04 动作迁移**：[README、prompt 与 workflow.json](https://github.com/Nuos/H3-h3-prompt-journal/tree/faa8edc311589d68d37e93524c7cb8e553fff857/case-studies/2026-10-h3-motion-transfer)。重点：prompt 第 118—153、245—442 行；JSON 节点 131/132/136/155/188/191 及链接 275/308/387/391。
- **E05 神裂海滩剑舞**：[README 与 methodology](https://github.com/Nuos/H3-h3-prompt-journal/tree/faa8edc311589d68d37e93524c7cb8e553fff857/case-studies/2026-10-kanzaki-beach-sword-dance-18-segment)。重点：README 第 49—61、111 行；methodology 第二、四、八节。
- **E06 夏日四段**：[README 与 prompt](https://github.com/Nuos/H3-h3-prompt-journal/tree/faa8edc311589d68d37e93524c7cb8e553fff857/case-studies/2026-10-summer-pool-beach-waterline-mv-4-segment)。重点：README 参考图工作流；prompt PART 1 的 subject_definitions/retention_analysis。
- **E07 水岸双段**：[README](https://github.com/Nuos/H3-h3-prompt-journal/blob/faa8edc311589d68d37e93524c7cb8e553fff857/case-studies/2026-10-waterfront-solo-dance-two-segment/README.md)。重点：第 9、14—22 行。
- **E08 三袜右入**：[README](https://github.com/Nuos/H3-h3-prompt-journal/blob/faa8edc311589d68d37e93524c7cb8e553fff857/case-studies/2026-10-sock-showcase-right-entry-three-shot/README.md)。重点：第 13—16、24—38 行。
- **E09 帆板 MV**：[README 与 prompt](https://github.com/Nuos/H3-h3-prompt-journal/tree/faa8edc311589d68d37e93524c7cb8e553fff857/case-studies/2026-08-furina-windsurfing-fashion-mv)。重点：README Layer 1/2/4；prompt 第二、三节。
- **E10 单人三姿态**：[README 与 prompt](https://github.com/Nuos/H3-h3-prompt-journal/tree/faa8edc311589d68d37e93524c7cb8e553fff857/case-studies/2026-08-single-subject-three-pose)。重点：README Inputs；prompt 第 1—75 行。
- **E11 紫纱七段**：[README 与 prompt](https://github.com/Nuos/H3-h3-prompt-journal/tree/faa8edc311589d68d37e93524c7cb8e553fff857/case-studies/2026-09-purple-veil-dance-seven-segment)。重点：README Inputs/提交工作流；prompt SEGMENT 01 第 22—24 行。
- **E12 台灯 A/B**：[README](https://github.com/Nuos/H3-h3-prompt-journal/blob/faa8edc311589d68d37e93524c7cb8e553fff857/case-studies/2026-09-editorial-lamp-rhythm-fashion-ab/README.md)。重点：Inputs 的无外部音频声明。
- **E13 触地换装**：[README 与 prompt](https://github.com/Nuos/H3-h3-prompt-journal/tree/faa8edc311589d68d37e93524c7cb8e553fff857/case-studies/2026-10-leg-lift-contact-cut-stocking-six-look)。重点：Inputs、六款 LOOK 状态机；prompt 第 3—7、37—69 行。
- **E14 三人恶作剧**：[README](https://github.com/Nuos/H3-h3-prompt-journal/blob/faa8edc311589d68d37e93524c7cb8e553fff857/case-studies/2026-09-three-person-prank-freeze-gag-cos-swap/README.md)。重点：Inputs、invisible third actor、skin-only reskin。
- **E15 宋韵六段**：[README](https://github.com/Nuos/H3-h3-prompt-journal/blob/faa8edc311589d68d37e93524c7cb8e553fff857/case-studies/2026-09-song-style-classical-dance-six-segment/README.md)。重点：双图分工与 Assets 的自行提供声明。
- **E16 古典武侠十三段**：[methodology](https://github.com/Nuos/H3-h3-prompt-journal/blob/faa8edc311589d68d37e93524c7cb8e553fff857/case-studies/2026-10-classical-wuxia-dance-13-segment/methodology.md)。重点：第 13、15、18 条。
- **E17 水上综艺**：[README](https://github.com/Nuos/H3-h3-prompt-journal/blob/faa8edc311589d68d37e93524c7cb8e553fff857/case-studies/2026-08-water-obstacle-variety-show/README.md)。重点：Inputs、Explicit Freedom Grants。
