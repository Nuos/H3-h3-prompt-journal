# M1 案例依据与适用边界

## 核心摘要

从案例提炼 M1 的三项能力：**整理作品意图与约束、分配段落功能与观众信息、设计情绪能量与可识别母题**。先回答“观众应理解、期待或感受到什么”，再把动作、摄影、声音和排时的实现目标交给相应责任模块。[CE01][CE07][CE08]

本文件提供可离线使用的提炼规则和审阅问题。规则正文足以支持当前职责；文末固定来源与同目录 `case-index.json` 用于追溯，不要求安装者取得任何兄弟目录。H3 的官方模式和 Label 由本包官方映射资料负责，不能把案例旧提示词包装直接视为当前官方协议。

**关键词：** 作品目标、必保事件、可调范围、段落任务、观众信息、情绪能量、动作母题、案例作用范围、证据边界。

## 目录导航

1. 内容边界和读取范围
2. 按子模块读取
3. 可执行编排与审阅规则
4. 十个主要案例怎样支持 M1
5. 来源冲突和修复责任
6. 局部任务的使用示例
7. 不可泛化项与未验证能力
8. 集中来源

## 1. 内容边界和读取范围

案例内容固定于项目提交 `0ce8b7b1890052bf1d4dd233ef20e68817b38f28`，`case-studies` 树为 `70a8a2a632d633f5d532db23cad99c772dc23026`。冻结开发方案原案例基线 `35658d3615d02c6aa6e4221fb223d73b86aa6875` 作为历史追溯保留；本文件记录本次实际读取的提交，不改写开发方案。

本次登记 29 个案例，其中 15 个为 10 月案例。先扫描 29 案 README 入口，再选出 10 个主要案例和 4 个补充案例，余下 15 案仅登记入口和专业责任位置。**并未宣称逐字语义审计了 29 案的全部文本。**

实际全文阅读 17 个文件：10 个主要案例的 README、两份方法论、四人队形/贴纸喜剧/水上综艺三份完整短提示词，以及动作链喜剧/右入展示两份补充 README；另对 6 个文件定位阅读。全部 98 个文本文件的路径和哈希进入来源清单；“进入清单”与“阅读正文”分别记录。未查看图片、视频、音频，未分析或执行动作迁移工作流 JSON。

| 证据代码 | 沿用冻结方案的含义 | 本文件怎样使用 |
|---|---|---|
| F | 原文可确认事实，包含作者写出的结果报告 | 能确认某条方法、时间或作者判断写在来源中；不能当作本次复现 |
| D | 架构推论与开发提案 | `CASE-R01`—`CASE-R12` 是从案例提炼的 M1 设计规则 |
| I | 已有实现与已执行检查 | 只在存在对应实现或执行记录时使用；**不表示“推断”** |
| U | 尚未验证或证据不足 | 未进行的 H3 推理、媒体审阅、长篇影视剧能力保持未验证 |

原文摘要、短摘录、精确行号、Git blob、SHA-256、阅读范围和不可泛化常量均在 `case-index.json` 中。该索引的 `reading_status` 和 `read_ranges` 是实际阅读范围的依据。

## 2. 按子模块读取

| 调用职责 | 优先规则 | 最小专业问题 | 返回范围 |
|---|---|---|---|
| **M1.1 意图与约束整理** | R01、R03、R08、R09、R11、R12 | 作品要达到什么目的？哪些事件、台词和条件必须保留？哪些实现可调？ | 目标、保留项、可调项、优先级、来源、冲突与缺项 |
| **M1.2 段落功能与信息结构** | R02、R03、R07、R10、R12 | 每段为何存在？观众在该段获得什么？事件顺序和结尾承担什么作用？ | 段落功能、信息/预期变化、主要观看任务及事件关系 |
| **M1.3 情绪能量与母题** | R04、R05、R06、R08、R10、R12 | 情绪如何变化？什么特征被识别、变形或回收？留白/高潮/收束为何发生？ | 定性走向、母题意图、可观察表达方向及未核实的音乐条件 |

这里的 R 编号分别对应 `CASE-Rxx`。只读取当前子任务需要的规则和案例；已有兼容输入可以直接使用，不要求为了取得数据重新运行其他子模块。完整输入输出字段、父模块接受方式和状态枚举以本包公开合同为准。

## 3. 可执行编排与审阅规则

### 3.1 M1.1：固定目标，同时保留明确的创作自由

**CASE-R01｜先登记目的、必保事项和可调范围。** 从当前请求提取体裁/用途、作品目的、用户固定事件与台词、许可变化和条件冲突。案例是研究依据，不替当前用户决定角色、场景和时长。水上综艺明确固定情节锚点，同时允许其间动作和摄影自由设计；海滩剑舞则区分固定原现场与允许奇幻替景的两个版本。[CE01][CE07][CE21][CE25]

审阅：目标缺失时标明缺项，继续可做的整理；同一范围出现互斥要求时记录冲突和返回对象。不得为使表格完整而虚构用户意图，也不得把用户明确允许的自由执行改成无依据的逐动作限制。

**CASE-R03｜保护事件、施动者、后果和必要顺序。** 用户给定的情节锚点与因果关系必须能在段落方案中找到对应位置。保留原台词和归属，交 M6 处理声音；保留事件意义和依赖，交 M4 处理身体过程。外观替换不能悄悄倒转故事或更换施动者。[CE25][CE26][CE27][CE28][CE29]

审阅：明确遗漏、反转或未经授权更换关键事件时形成失败诊断；只缺证据时保留未知。不要仅凭“看起来合理”增加来源不存在的事件。

**CASE-R08｜分开情绪参考和画面授权。** 歌词、标题、运动参考可以说明情绪或段落含义；其中的人物、物件、场景与动作不自动获得画面生成权限。需要实体化时记录当前授权，并交 M2 核对参考范围；用户已明确要求歌词可视化时，不套用其他案例的全局禁令。[CE04][CE07][CE20]

审阅：独舞歌词出现“有人”，不能据此新增宾客；借用剑路，不自动继承原参考中的敌人和战斗场景。反过来，当前任务已允许新增世界时，也不能擅自锁死成原背景。

**CASE-R09｜案例常量逐项条件化。** 人数、段数、时长、BPM、画幅、特定人物、场景、镜头模式、口型与声音策略均从当前任务取值。单人、四人、连续舞蹈、独立蒙太奇和自由执行分别有案例；它们不是一组可以同时叠加的通用硬规则。[CE07][CE10][CE17][CE25]

审阅：拒绝把“18 段、单人、139.5 BPM、海滩、一镜到底、无对白”作为新任务默认要求。案例知识中的参数只有在当前范围明确采用后才能生效。

**CASE-R11｜局部变更先列保留项和许可变化。** A/B 改版、角色替换或局部修改应说明改什么、保留什么、影响哪些段落。变更情绪时，不顺带重写身份、关键事件、台词、时长和已确认的其他条件。原假设被证据否定时，保留修正依据，不把补救动作伪装成源片事实。[CE21][CE29][CE30]

审阅：台灯 A/B 的受控变奏可以用于整理变更边界，不能据此声称任何作品都只需修改三个字段。修复生成问题时也不能凭空增加“走出画框—空帧—重新入画”的新机制。

### 3.2 M1.2：段落有功能，观看有重点

**CASE-R02｜每个相关段落给出作用和观众信息。** 为段落说明它在当前作品中的功能、观众应理解/期待/感受什么，以及主要可见信息。可以使用建立、展开、揭示、反差、留白、回收、收束等与任务匹配的表达；这些不是必须逐一出现的固定结构公式。[CE01][CE08][CE15][CE16][CE23][CE24]

审阅：只写“电影感、唯美、高级”或一串机位名称，还没有完成段落功能设计。段落相似可以是有意呼应，需要解释其作用；无需强迫每段全新。

**CASE-R07｜给主要观看任务排优先级。** 明确本段最需要看清的信息和可让步的次要信息，交给 M5/M9 作为设计目标。一个主要视觉问题允许多个服务于它的动作；不等于一段只能有一个动作、一镜或一次生成。[CE03][CE08][CE09][CE18]

审阅：完整剑路、脸部微表情、脚部接触与远景环境可能竞争构图资源。M1保留目标和优先级，由 M5 解决观察位置与取景；不要用更多摄影词掩盖冲突，也不要在此自行提交权威机位或剪辑点。

**CASE-R10｜分开中段交接和作品结尾。** 中段说明下一段为何仍有必要，终章说明当前作品目标怎样完成。结尾可以克制、安静、幽默、英雄式或保持开放，取决于当前作品意图；不能统一改成高能胜利定格。[CE11][CE14][CE22][CE24][CE26]

审阅：中段不应无故做完整音乐终止；终章不能仅因为到时停止就被视为作品完成。先审阅结束的意义，再交 M6/M7/M8/M9 处理声音、时间和接续。

### 3.3 M1.3：情绪有表达方向，母题有可识别关系

**CASE-R04｜把情绪连接到可观察的表达方向。** M1 可以记录“压迫、平静、信任、恢复自主”等内部意图，同时给下游一个可实现、可审阅的方向。白凤案例通过动作路径受阻和恢复表现情绪；四人队形以保护、相互呼应和重新集结组织段落。具体支撑、关节过程、摄影机和光色仍由 M4/M5/M10 完成。[CE13][CE14][CE16][CE17][CE31]

审阅：情绪词本身不是已实现的画面。不能因“压迫”擅自增加绑绳或施压者，也不能把用户要的克制尊严替换成热闹庆典。

**CASE-R05｜母题记录不变特征、变化和回收。** 需要母题时，写清它为何仍可被辨认、在何处出现、改变什么以及回收时的作用。双臂收拢到对角展开可以改变力度、幅度、方向和身体层次，同时保留联系。无母题需求时不强行添加。[CE02][CE21]

审阅：一段一套互不相关的动作不能仅靠同一标题变成母题；有意重现也不应被“禁止重复”误判。动作细节由 M4 编排，视觉实现由 M5/M10 承接。

**CASE-R06｜允许发展、回落、反差、留白和收束。** 能量计划服务作品目的，不强求每段比前段更强。留白、稳定段和漂移段的对比可以承担功能；一个有效策略不应覆盖全片。先写定性意图，再由 M6/M7 依据真实音乐安排时间。[CE02][CE06][CE08][CE19][CE22][CE32]

审阅：无意空站与有意停顿分别判断。没有音频或可信节拍数据时，可继续定性设计；精确卡点、首拍相位和音乐对齐必须保留未验证状态，不自行算出数值就声称实测。[CE05]

### 3.4 三个子模块共同遵守的证据规则

**CASE-R12｜把来源、设计和实测分开。** 作者写“稳定”“成功”、正文标“exact”、来源清单打勾，均不能替代本轮执行与媒体证据。当前输出是作品意图和文本审阅结果，不能据此宣布全片或 H3 输出通过。已有内容与当前创作设想应分别标明来源或设计性质。[CE05][CE11][CE30]

确定性检查可以核对 ID、引用、完整性、版本、声明范围；是否准确理解作者意图、情绪变化是否有说服力，仍需范围明确的语义审阅。未取得真实生成片和成片时，媒体/作品效果保持 U。

## 4. 十个主要案例怎样支持 M1

| 案例 | 可提炼能力 | 主要依据 | 必须留下的边界 |
|---|---|---|---|
| 10 月古典武侠舞十三段 | 作品五问、动作母题、非单调能量与有意停顿 | CE01—CE06 | 13 段、90.5 BPM、单人和武器状态属于原项目 |
| 10 月海滩剑舞十八段 | 作品定位、段落功能、观看优先级和作品级收束 | CE07—CE11 | 两套场景权限不能混用；18 段/海滩/英雄结尾均非通用要求 |
| 10 月白凤蒙尘六段 | 受阻、反差、恢复与尊严收束 | CE12—CE14、CE37 | 不把情绪拟人化为未授权施压者；具体舞步和时长交其他模块 |
| 10 月夏日水线 MV | 同主题的不同段落任务、渐进揭示 | CE15—CE16、CE38 | 水线、泡沫、泳池等是特定作品材料 |
| 10 月四人队形 | 多人关系、保护/信任/重新集结、可辨动作性格 | CE17—CE18 | 不建立统一人数限制；源文交叉路线存在冲突 |
| 10 月下山面纱独舞 | 歌词/情绪/实体授权分离，稳定与漂移对比 | CE19—CE20 | 漂移只在原案指定段落；面纱、总时长等不是新任务默认 |
| 9 月台灯时尚 A/B | 保留与变化的范围、期待—峰值—收束 | CE21—CE22 | 五章、十个动作、台灯、BPM 和两套结尾只属于原案 |
| 8 月双段人物揭示 | 介绍、展开、信息递进、最终视觉回收 | CE23—CE24 | 不采纳“超过20秒一律两段”等泛化表述 |
| 8 月水上综艺 | 必保锚点、执行自由、成功预期/反转/反应 | CE25—CE26 | 仅支持有限短场结构；原时长和分辨率建议不作后端硬限制 |
| 8 月贴纸厨房喜剧 | 角色分工、恶作剧—后果—反应—收尾 | CE27—CE28 | 2D媒介、无盖盐罐、卡通反应和无对白策略是原案设定 |

四个补充案例分别提供：保留因果骨架的外观替换、对无依据机制的修正、克制反应承载喜剧、按音乐功能组织段落。[CE29]—[CE32] 其余 15 案逐案角色见 `case-index.json`：它们是后续动作、参考、摄影、连续性、时间或剪辑模块的索引入口，本轮未将其全部规则导入 M1。

## 5. 来源冲突和修复责任

| 冲突/差异 | 原文事实 | M1 的处理及返回责任 |
|---|---|---|
| 连续舞蹈与独立蒙太奇 | 白凤要求段间续动；剑舞方法允许分组而不强求逐帧接力。[CE10][CE37] | 记录当前段间关系意图；交 M9 声明边界，M8 按类型核对 |
| 禁中心交叉与实际中心交叉 | 四人 README 禁跨中线，prompt 又明确穿越中心和换层。[CE33][CE34] | 保留差异，不同时复制为硬规则；M1保留保护/重组意图，M3核对路线 |
| 两处总时长不一致 | 下山导语为141.845秒，工作流清单末值出现181.956。[CE35][CE36] | 记录来源冲突；不自动选择较新或较大数值；交 M7 核对真实清单/音频 |
| 固定现场与允许替景 | 海滩方案A保留现场，方案B允许替景；夏日案区分人物身份与场景重建。[CE07][CE38] | 依据当前要求选择权限提案，交 M2 接受；不混合两个版本 |
| 不停运动与有意留白 | 方法论允许有意停顿；台灯案使用期待/收束，下山案依靠局部对比。[CE02][CE06][CE19][CE22] | 先核对停顿功能，交 M4/M7/M9 实现；不设全局“永不静止” |
| 两段人物揭示被作者概括为通则 | 角色揭示案以两段承担不同任务，并提出“超过20秒”的泛化判断。[CE23][CE24] | 保留段落功能证据；不把时长或段数升格为模型能力限制 |

这些处理属于 D 类提炼设计。保留案例原文，不通过改写来源消除冲突。若当前用户输入已明确选择一种策略，就按该授权处理，不为已解决的问题重复要求确认。

## 6. 局部任务的使用示例

### 6.1 单独整理 M1.1：水上综艺的必保事项

输入已有“滚筒成功、摔倒、恢复前进、抓住墙缘、机关侧击、落水、湿发反应收尾”的事件和两句指定台词，同时允许自由设计避障细节。输出应保留事件、顺序、原台词和自由范围；不要求先运行动作模块，也不自行把自由执行改成毫秒级动作清单。[CE25][CE26]

局部审阅可以核对必保事件覆盖；物理过程、声线、实际时长是否可执行分别交 M4/M6/M7，不能在 M1 直接标成媒体通过。

### 6.2 单独处理 M1.2：四人队形的段落任务

输入已有四个主体及“保护、信任、重新集结”的目标。输出应说明观众如何读到关系变化，以及保护/分开/汇合/重新展开的段落意义。可以引用已提供的事件，但不重新定义四人的身份、不强制保持固定象限，也不自行决定完整交叉轨迹。[CE17][CE18][CE33][CE34]

局部审阅核对关系目标是否仍被保留；路径、遮挡、时间与构图分别交 M3/M7/M5。

### 6.3 单独处理 M1.3：母题回收与克制收束

输入已有“收拢—对角展开”的动作母题和结尾“恢复自主、保持尊严”的意图。输出应保留母题的可识别联系，提出力度/幅度/方向等变化方向，并说明结尾为何不转成胜利庆典。可在没有实际音频的情况下给定性走向；精确拍点和动作时刻保持待核对。[CE02][CE05][CE14]

这些示例复用案例已有材料，示范局部职责和交接。它们没有引入新的通用戏剧学说，也不替代本包合同与实际验收记录。

## 7. 不可泛化项与未验证能力

- **不用案例参数填空。** 段数、人数、画幅、总长、BPM、题材、角色、场景、道具、固定时点、调色和特定镜头政策逐项取当前输入；不得因模板缺值而默认沿用案例。
- **不把主功能变成数量禁令。** “一个主要视觉问题”是观看优先级，可以有多个服务于它的事件。M1 的段落不等于 M9 的镜头、分镜格或生成任务。
- **不把抽象意图原样塞入成品。** M1 内部可以记录情绪和目的；下游应将其变成可见事件、观看信息和必要的声音描述。规则 ID、来源、审计记录属于内部交付，不应混入纯模型正文。
- **保留有限叙事能力的边界。** 贴纸喜剧、水上综艺、人物揭示支持有限的因果、反转、反应与信息递进；不能以这些例子声称已经建立完整影视剧结构、复杂对白系统、长篇人物弧线或集级叙事验证。
- **不宣称媒体效果已证实。** 本文件验证来源与提炼关系；未运行 H3，未审阅生成视频或成片，不给出稳定率、画面正确率或跨题材有效率。

## 8. 集中来源

以下均来自 `case-studies/` 原案例文本，固定到本次实际读取提交。行号锚点用于人工复核；精确字节、Git blob、SHA-256、短摘录与读取范围保存在同目录 `case-index.json`。本文规则是 D 类提炼，所列原文存在性为 F；作者报告不视为本次媒体测量。

- [CE01] [case-studies/2026-10-classical-wuxia-dance-13-segment/methodology.md，L19–L29](https://github.com/Nuos/H3-h3-prompt-journal/blob/0ce8b7b1890052bf1d4dd233ef20e68817b38f28/case-studies/2026-10-classical-wuxia-dance-13-segment/methodology.md#L19-L29)。原文提出每段的舞种、情绪能量、动作重点、观看信息和段落功能五问。
- [CE02] [case-studies/2026-10-classical-wuxia-dance-13-segment/methodology.md，L71–L78](https://github.com/Nuos/H3-h3-prompt-journal/blob/0ce8b7b1890052bf1d4dd233ef20e68817b38f28/case-studies/2026-10-classical-wuxia-dance-13-segment/methodology.md#L71-L78)。原文规定主题可识别、变形、回收，能量不必每段递增。
- [CE03] [case-studies/2026-10-classical-wuxia-dance-13-segment/methodology.md，L112–L128](https://github.com/Nuos/H3-h3-prompt-journal/blob/0ce8b7b1890052bf1d4dd233ef20e68817b38f28/case-studies/2026-10-classical-wuxia-dance-13-segment/methodology.md#L112-L128)。摄影变化应带来新的动作信息；项目先声明镜头模式。
- [CE04] [case-studies/2026-10-classical-wuxia-dance-13-segment/methodology.md，L146–L151](https://github.com/Nuos/H3-h3-prompt-journal/blob/0ce8b7b1890052bf1d4dd233ef20e68817b38f28/case-studies/2026-10-classical-wuxia-dance-13-segment/methodology.md#L146-L151)。歌词和文字意象不自动授权画面实体。
- [CE05] [case-studies/2026-10-classical-wuxia-dance-13-segment/methodology.md，L130–L136](https://github.com/Nuos/H3-h3-prompt-journal/blob/0ce8b7b1890052bf1d4dd233ef20e68817b38f28/case-studies/2026-10-classical-wuxia-dance-13-segment/methodology.md#L130-L136)。缺节拍数据或相位不确定时不能把推算当实测。
- [CE06] [case-studies/2026-10-classical-wuxia-dance-13-segment/methodology.md，L160–L168](https://github.com/Nuos/H3-h3-prompt-journal/blob/0ce8b7b1890052bf1d4dd233ef20e68817b38f28/case-studies/2026-10-classical-wuxia-dance-13-segment/methodology.md#L160-L168)。静止是否有意图、音乐依据和接续比一概禁止静止更重要。
- [CE07] [case-studies/2026-10-kanzaki-beach-sword-dance-18-segment/methodology.md，L12–L37](https://github.com/Nuos/H3-h3-prompt-journal/blob/0ce8b7b1890052bf1d4dd233ef20e68817b38f28/case-studies/2026-10-kanzaki-beach-sword-dance-18-segment/methodology.md#L12-L37)。同人物与音乐可以有不同作品定位；海滩固定现场与奇幻替景是两套授权。
- [CE08] [case-studies/2026-10-kanzaki-beach-sword-dance-18-segment/methodology.md，L210–L231](https://github.com/Nuos/H3-h3-prompt-journal/blob/0ce8b7b1890052bf1d4dd233ef20e68817b38f28/case-studies/2026-10-kanzaki-beach-sword-dance-18-segment/methodology.md#L210-L231)。原文要求每段明确功能，配不同重点和情绪任务。
- [CE09] [case-studies/2026-10-kanzaki-beach-sword-dance-18-segment/methodology.md，L122–L130](https://github.com/Nuos/H3-h3-prompt-journal/blob/0ce8b7b1890052bf1d4dd233ef20e68817b38f28/case-studies/2026-10-kanzaki-beach-sword-dance-18-segment/methodology.md#L122-L130)。景别目标有优先级，脸/脚/剑路/环境不能默认同时最清楚。
- [CE10] [case-studies/2026-10-kanzaki-beach-sword-dance-18-segment/methodology.md，L233–L252](https://github.com/Nuos/H3-h3-prompt-journal/blob/0ce8b7b1890052bf1d4dd233ef20e68817b38f28/case-studies/2026-10-kanzaki-beach-sword-dance-18-segment/methodology.md#L233-L252)。分组是组织方式，不强制逐帧首尾姿态匹配。
- [CE11] [case-studies/2026-10-kanzaki-beach-sword-dance-18-segment/methodology.md，L314–L324](https://github.com/Nuos/H3-h3-prompt-journal/blob/0ce8b7b1890052bf1d4dd233ef20e68817b38f28/case-studies/2026-10-kanzaki-beach-sword-dance-18-segment/methodology.md#L314-L324)。作品级自检覆盖记忆点、差异、摄影理由、继续观看和作品收束。
- [CE12] [case-studies/2026-10-baifeng-mengchen-classical-dance-six-segment/README.md，L27–L36](https://github.com/Nuos/H3-h3-prompt-journal/blob/0ce8b7b1890052bf1d4dd233ef20e68817b38f28/case-studies/2026-10-baifeng-mengchen-classical-dance-six-segment/README.md#L27-L36)。六段标题和动作机制呈现由受阻到恢复自主的推进。
- [CE13] [case-studies/2026-10-baifeng-mengchen-classical-dance-six-segment/prompt.md，L121–L134](https://github.com/Nuos/H3-h3-prompt-journal/blob/0ce8b7b1890052bf1d4dd233ef20e68817b38f28/case-studies/2026-10-baifeng-mengchen-classical-dance-six-segment/prompt.md#L121-L134)。压迫通过动作被截断及重心/上身失配表现，原文不授权新增施压者。
- [CE14] [case-studies/2026-10-baifeng-mengchen-classical-dance-six-segment/prompt.md，L395–L408](https://github.com/Nuos/H3-h3-prompt-journal/blob/0ce8b7b1890052bf1d4dd233ef20e68817b38f28/case-studies/2026-10-baifeng-mengchen-classical-dance-six-segment/prompt.md#L395-L408)。结尾恢复自主路径，但明确不是胜利庆典或继续低位挣扎。
- [CE15] [case-studies/2026-10-summer-pool-beach-waterline-mv-4-segment/README.md，L46–L59](https://github.com/Nuos/H3-h3-prompt-journal/blob/0ce8b7b1890052bf1d4dd233ef20e68817b38f28/case-studies/2026-10-summer-pool-beach-waterline-mv-4-segment/README.md#L46-L59)。第一段目的明确为建立夏日MV视觉风格。
- [CE16] [case-studies/2026-10-summer-pool-beach-waterline-mv-4-segment/README.md，L76–L109](https://github.com/Nuos/H3-h3-prompt-journal/blob/0ce8b7b1890052bf1d4dd233ef20e68817b38f28/case-studies/2026-10-summer-pool-beach-waterline-mv-4-segment/README.md#L76-L109)。第三段以机位切换恢复流动感，第四段以水线/泡沫形成渐进揭示。
- [CE17] [case-studies/2026-10-four-subject-formation-choreography/prompt.md，L30–L62](https://github.com/Nuos/H3-h3-prompt-journal/blob/0ce8b7b1890052bf1d4dd233ef20e68817b38f28/case-studies/2026-10-four-subject-formation-choreography/prompt.md#L30-L62)。四人段落明写保护、信任、重新组装的意图，并区分四人动作性格。
- [CE18] [case-studies/2026-10-four-subject-formation-choreography/prompt.md，L64–L86](https://github.com/Nuos/H3-h3-prompt-journal/blob/0ce8b7b1890052bf1d4dd233ef20e68817b38f28/case-studies/2026-10-four-subject-formation-choreography/prompt.md#L64-L86)。新成员、新队形或动作峰值作为切镜所揭示的新信息。
- [CE19] [case-studies/2026-10-xiashan-veiled-solo-twelve-segment/README.md，L15–L20](https://github.com/Nuos/H3-h3-prompt-journal/blob/0ce8b7b1890052bf1d4dd233ef20e68817b38f28/case-studies/2026-10-xiashan-veiled-solo-twelve-segment/README.md#L15-L20)。作者记录全片漂移镜头会削弱对比，只在指定情绪段应用。
- [CE20] [case-studies/2026-10-xiashan-veiled-solo-twelve-segment/README.md，L46–L56](https://github.com/Nuos/H3-h3-prompt-journal/blob/0ce8b7b1890052bf1d4dd233ef20e68817b38f28/case-studies/2026-10-xiashan-veiled-solo-twelve-segment/README.md#L46-L56)。歌词按时间锚、情绪弧线和穿戴物状态区分，引用不添加画面人/物。
- [CE21] [case-studies/2026-09-editorial-lamp-rhythm-fashion-ab/README.md，L14–L30](https://github.com/Nuos/H3-h3-prompt-journal/blob/0ce8b7b1890052bf1d4dd233ef20e68817b38f28/case-studies/2026-09-editorial-lamp-rhythm-fashion-ab/README.md#L14-L30)。A/B变奏保留节奏骨架，只在明确层面分叉。
- [CE22] [case-studies/2026-09-editorial-lamp-rhythm-fashion-ab/README.md，L52–L79](https://github.com/Nuos/H3-h3-prompt-journal/blob/0ce8b7b1890052bf1d4dd233ef20e68817b38f28/case-studies/2026-09-editorial-lamp-rhythm-fashion-ab/README.md#L52-L79)。五章中有期待、最终峰值和最终静态收束。
- [CE23] [case-studies/2026-08-cinematic-character-reveal-two-part/README.md，L28–L49](https://github.com/Nuos/H3-h3-prompt-journal/blob/0ce8b7b1890052bf1d4dd233ef20e68817b38f28/case-studies/2026-08-cinematic-character-reveal-two-part/README.md#L28-L49)。两段有不同揭示职责，第二段避免重复第一段主要机制。
- [CE24] [case-studies/2026-08-cinematic-character-reveal-two-part/prompt.md，L10–L21](https://github.com/Nuos/H3-h3-prompt-journal/blob/0ce8b7b1890052bf1d4dd233ef20e68817b38f28/case-studies/2026-08-cinematic-character-reveal-two-part/prompt.md#L10-L21)。原提示词分别安排建立/神秘出场和展开/高潮/收尾。
- [CE25] [case-studies/2026-08-water-obstacle-variety-show/README.md，L21–L33](https://github.com/Nuos/H3-h3-prompt-journal/blob/0ce8b7b1890052bf1d4dd233ef20e68817b38f28/case-studies/2026-08-water-obstacle-variety-show/README.md#L21-L33)。七个必保情节锚点与其间明确的自由执行范围并存。
- [CE26] [case-studies/2026-08-water-obstacle-variety-show/prompt.md，L111–L153](https://github.com/Nuos/H3-h3-prompt-journal/blob/0ce8b7b1890052bf1d4dd233ef20e68817b38f28/case-studies/2026-08-water-obstacle-variety-show/prompt.md#L111-L153)。接近成功、侧击、落水、反应台词按因果顺序出现。
- [CE27] [case-studies/2026-08-sticker-character-kitchen-comedy/prompt.md，L45–L101](https://github.com/Nuos/H3-h3-prompt-journal/blob/0ce8b7b1890052bf1d4dd233ef20e68817b38f28/case-studies/2026-08-sticker-character-kitchen-comedy/prompt.md#L45-L101)。倒盐恶作剧后有被喂咸食和夸张喜剧反应。
- [CE28] [case-studies/2026-08-sticker-character-kitchen-comedy/README.md，L37–L48](https://github.com/Nuos/H3-h3-prompt-journal/blob/0ce8b7b1890052bf1d4dd233ef20e68817b38f28/case-studies/2026-08-sticker-character-kitchen-comedy/README.md#L37-L48)。真实人手与贴纸的表演职责有明确分工。
- [CE29] [case-studies/2026-09-three-person-prank-freeze-gag-cos-swap/README.md，L16–L33](https://github.com/Nuos/H3-h3-prompt-journal/blob/0ce8b7b1890052bf1d4dd233ef20e68817b38f28/case-studies/2026-09-three-person-prank-freeze-gag-cos-swap/README.md#L16-L33)。案例说明外观替换保留事件、时刻、镜头、定格与声音结构。
- [CE30] [case-studies/2026-10-sock-showcase-right-entry-three-shot/README.md，L11–L30](https://github.com/Nuos/H3-h3-prompt-journal/blob/0ce8b7b1890052bf1d4dd233ef20e68817b38f28/case-studies/2026-10-sock-showcase-right-entry-three-shot/README.md#L11-L30)。作者撤销左出右进的无依据机制，并以唯一变化项引导观看。
- [CE31] [case-studies/2026-09-action-chain-sock-fan-comedy/README.md，L90–L103](https://github.com/Nuos/H3-h3-prompt-journal/blob/0ce8b7b1890052bf1d4dd233ef20e68817b38f28/case-studies/2026-09-action-chain-sock-fan-comedy/README.md#L90-L103)。克制眼神和因果反差承担喜剧，不依赖夸张鬼脸。
- [CE32] [case-studies/2026-08-furina-windsurfing-fashion-mv/README.md，L48–L62](https://github.com/Nuos/H3-h3-prompt-journal/blob/0ce8b7b1890052bf1d4dd233ef20e68817b38f28/case-studies/2026-08-furina-windsurfing-fashion-mv/README.md#L48-L62)。原案按音乐功能而非平均时长划分段落。
- [CE33] [case-studies/2026-10-four-subject-formation-choreography/README.md，L76–L82](https://github.com/Nuos/H3-h3-prompt-journal/blob/0ce8b7b1890052bf1d4dd233ef20e68817b38f28/case-studies/2026-10-four-subject-formation-choreography/README.md#L76-L82)。README要求各守象限且禁止跨中线。
- [CE34] [case-studies/2026-10-four-subject-formation-choreography/prompt.md，L77–L86](https://github.com/Nuos/H3-h3-prompt-journal/blob/0ce8b7b1890052bf1d4dd233ef20e68817b38f28/case-studies/2026-10-four-subject-formation-choreography/prompt.md#L77-L86)。同案prompt明确穿过中心以及前后换层。
- [CE35] [case-studies/2026-10-xiashan-veiled-solo-twelve-segment/README.md，L3–L3](https://github.com/Nuos/H3-h3-prompt-journal/blob/0ce8b7b1890052bf1d4dd233ef20e68817b38f28/case-studies/2026-10-xiashan-veiled-solo-twelve-segment/README.md#L3-L3)。导语列总长141.845秒。
- [CE36] [case-studies/2026-10-xiashan-veiled-solo-twelve-segment/README.md，L58–L62](https://github.com/Nuos/H3-h3-prompt-journal/blob/0ce8b7b1890052bf1d4dd233ef20e68817b38f28/case-studies/2026-10-xiashan-veiled-solo-twelve-segment/README.md#L58-L62)。提交工作流的清单末值出现181.956。
- [CE37] [case-studies/2026-10-baifeng-mengchen-classical-dance-six-segment/README.md，L97–L103](https://github.com/Nuos/H3-h3-prompt-journal/blob/0ce8b7b1890052bf1d4dd233ef20e68817b38f28/case-studies/2026-10-baifeng-mengchen-classical-dance-six-segment/README.md#L97-L103)。白凤案例明确要求段间承接上一段运动状态。
- [CE38] [case-studies/2026-10-summer-pool-beach-waterline-mv-4-segment/README.md，L30–L44](https://github.com/Nuos/H3-h3-prompt-journal/blob/0ce8b7b1890052bf1d4dd233ef20e68817b38f28/case-studies/2026-10-summer-pool-beach-waterline-mv-4-segment/README.md#L30-L44)。夏日MV将人物身份和重设计的场景/姿势/机位分开。
