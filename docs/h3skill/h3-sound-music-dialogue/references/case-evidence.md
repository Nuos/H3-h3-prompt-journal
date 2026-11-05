# M6 案例证据、矛盾与验证边界

本模块以 `case-studies/` 为领域边界，以冻结方案中 M6 的职责为实现约束。**案例写了某种声音要求，不等于本轮已听到该声音，也不等于生成结果已经达到要求。** 官方材料只补充模式、字段与 Label 的协议语义；不把协议支持当作案例已经验证的对白、音色或混音能力。

## 导航

1. 来源与证据分级
2. 本轮实际覆盖
3. 可定位的核心证据 E01—E07
4. 四项领域规则的依据与新增部分
5. 不能推出的结论

## 1. 来源与证据分级

- 案例仓库：`Nuos/H3-h3-prompt-journal`。
- 本轮案例固定提交：`780a8729cca22e13d4fa44f031f8824056a5deee`；树 `33be739a4044175b560733745bdd4f71d721e3d5`。
- 逐文件路径、SHA-256、Git blob SHA-1、行数、读取者与实际范围见 [case-index.json](case-index.json)。本轮计算的全部 98 文件 Git blob 哈希均与该固定树一致。
- 冻结设计职责见 [01-core-framework.md](https://github.com/Nuos/H3-h3-prompt-journal/blob/608813b6e51531ac47f860bc384a454a504fe9ff/docs/skillplan/01-core-framework.md) 的 M6、[03-source-evidence.md](https://github.com/Nuos/H3-h3-prompt-journal/blob/608813b6e51531ac47f860bc384a454a504fe9ff/docs/skillplan/03-source-evidence.md) 的声音矛盾清单，以及 [06-modularity-routing-principles.md](https://github.com/Nuos/H3-h3-prompt-journal/blob/608813b6e51531ac47f860bc384a454a504fe9ff/docs/skillplan/06-modularity-routing-principles.md) 的模块化规则。冻结计划自己的旧快照和读取统计不算作本轮读取。
- 官方 H3 版本、原文行号和许可独立记录在 [h3-protocol-source.json](h3-protocol-source.json)、[h3-label-mapping.md](h3-label-mapping.md) 与 [provenance-and-license.md](provenance-and-license.md)。

| 代号 | 含义 | 可以支持什么 |
| --- | --- | --- |
| F | 源文本事实、明确要求或文本内矛盾 | 某版稿件确实这样写；不是成片效果证明 |
| A | 作者报告的分析、观察或结果 | 方法的案例背景；本轮未独立复现 |
| D | 从案例提炼的规则、本轮设计或扩展接口 | 可审查的设计决定；不能写成媒体实测结果 |
| P | 官方协议语义 | 模式、字段、Label、说话者与话语格式 |
| I | 本轮实际执行的文字读取、检索、哈希或工具检查 | 对应操作确实发生，不延伸为音视频验证 |
| U | 尚不明确或尚未验证 | 显式缺项与后续验证任务 |

## 2. 本轮实际覆盖（I）

截至本索引编制，取得 29 个案例目录内及案例集合的 **98 个文本文件**（91 Markdown、6 TXT、1 JSON），合计 2,507,574 字节、45,614 行。全部进行声音关键词检索，命中 1,813 行；这不构成全文阅读。

实际全文读取 **8 文件**，局部读取 **5 文件**，其余 **85 文件仅作关键词索引**。全文涉及 5 个案例；加局部核心证据共涉及 7 个案例，其中 5 个为十月案例。厨房 prompt 的全文由主线程读取并回报，本证据分工另核对其 L90–109。所有范围及读取回执在机读索引中保留。

| 实际读取状态 | 文件与范围 |
| --- | --- |
| 全文 | 滨水独舞 README L1–48、prompt L1–119；下山十二段 README L1–71；袜饰三镜 README L1–52、prompt L1–98；三人恶作剧 README L1–91、prompt L1–95；厨房喜剧 prompt L1–109 |
| 局部 | 下山 prompt L1–70；海岸剑舞 prompt L95–155；抬腿换装 prompt L630–690；三人恶作剧 README.zh-CN L1–52、prompt.zh-CN L595–628 |
| 其余 | 机读索引中 `keyword_index_only` 的文件，以及局部文件未声明的范围；不借用冻结方案的全文覆盖说法 |
| 媒体 | **0 个实际读取或试听。** 未读取原始／生成音视频及图片；案例链接到媒体、给出路径或声明测量结果均不改变此状态 |

关键词包括 audio、sound、music、voice、dialogue、vocal、speech、lyrics，以及音乐、声音、对白、台词、音轨、歌词、旁白、说话、静音、音效。哈希／行数计算与关键词扫描是机器文本操作，不能用来宣称 Agent 逐篇理解了全部文件。

## 3. 可定位的核心证据

### E01 — 滨水双段：人声未知、整轨复用与首拍时间域

来源：[prompt L3–7](https://github.com/Nuos/H3-h3-prompt-journal/blob/780a8729cca22e13d4fa44f031f8824056a5deee/case-studies/2026-10-waterfront-solo-dance-two-segment/prompt.md#L3-L7)、[L22–54](https://github.com/Nuos/H3-h3-prompt-journal/blob/780a8729cca22e13d4fa44f031f8824056a5deee/case-studies/2026-10-waterfront-solo-dance-two-segment/prompt.md#L22-L54)、[L59–102](https://github.com/Nuos/H3-h3-prompt-journal/blob/780a8729cca22e13d4fa44f031f8824056a5deee/case-studies/2026-10-waterfront-solo-dance-two-segment/prompt.md#L59-L102)、[README L7–8、L24–34](https://github.com/Nuos/H3-h3-prompt-journal/blob/780a8729cca22e13d4fa44f031f8824056a5deee/case-studies/2026-10-waterfront-solo-dance-two-segment/README.md#L7-L34)。

- **F：** prompt L6 明言人声内容未核实、没有歌词锚点，要求 Audio 1 原样复用。L26/L73 写完整复制，两个声音字段将它描述为完整最终音轨。
- **F：** 段二的源区间从 12.070 秒开始，L69 仍重复首拍 0.070 秒；其动作块从局部 0.000 秒开始。只凭文本不能确认局部首拍是否真实相同。
- **A：** README 的单镜检测、BPM 和拍网格来自作者报告，本轮没有重做分析。
- **D：** 未核实人声不得补词；已提交切片与原主时间线分开；源窗口可在 M6 登记，实际时间映射交 M7、裁切／装配交 M9。
- **限度：** 该案对舞蹈复用音轨、剧情 T2VA 的工作流偏好是局部经验，不是所有作品必须采用的模式或当前后端硬限制。

### E02 — 下山十二段：参考／复制矛盾与歌词视觉化

来源：[prompt L19–41](https://github.com/Nuos/H3-h3-prompt-journal/blob/780a8729cca22e13d4fa44f031f8824056a5deee/case-studies/2026-10-xiashan-veiled-solo-twelve-segment/prompt.md#L19-L41)、[README L15–21](https://github.com/Nuos/H3-h3-prompt-journal/blob/780a8729cca22e13d4fa44f031f8824056a5deee/case-studies/2026-10-xiashan-veiled-solo-twelve-segment/README.md#L15-L21)、[README L50–56](https://github.com/Nuos/H3-h3-prompt-journal/blob/780a8729cca22e13d4fa44f031f8824056a5deee/case-studies/2026-10-xiashan-veiled-solo-twelve-segment/README.md#L50-L56)。

- **F：** prompt L23–25 说仅参考节奏、无信号复制；L28/L32 又要求完整 1:1 最终音轨。它们是同一局部稿件中需裁决的策略冲突。
- **A：** README 报告场景词与歌词引出额外宾客，并描述面纱变化问题及修复。
- **F：** 原稿要求歌词原句作为节奏／口部辅助提示，同时排除把歌词内容直接演成场景；并非完全禁止所有口部动作。
- **D：** 分离原词句、音轨来源、情绪用途、独立人物发声和视觉授权。原案例的局部口型意图不推广到其他 MV；也不恢复全局人数或全局摄影机约束。
- **U：** 本轮没有听曲、逐句校对 SRT、核验作者的 40/40 对位或查看生成媒体。

### E03 — 海岸剑舞：完整复制与追加环境／动作声

来源：[prompt L95–145](https://github.com/Nuos/H3-h3-prompt-journal/blob/780a8729cca22e13d4fa44f031f8824056a5deee/case-studies/2026-10-kanzaki-beach-sword-dance-18-segment/prompt.md#L95-L145)。

- **F：** L103 要求指定切片作为完整声音，L111 写 `fully_copy`；L142 又要求加入轻微海浪、风、脚步、衣料和剑挥声，L145 要求音乐原样复制。
- **F：** L111/L125/L142 明确歌词只作时间提示，不要求人物对口型。
- **D/P：** 当前协议的完整复制针对完整最终音轨。新加任何声音须改变为部分复制关系；只有确实源内已有且不改动时才能继续完整复制。声音细小或后期添加不豁免这条含义。
- **U：** 源音轨是否已含所列声音未核实，不能据场景内容直接判定。

### E04 — 抬腿接触换装：接触声因果与完整复制冲突

来源：[prompt L640–677](https://github.com/Nuos/H3-h3-prompt-journal/blob/780a8729cca22e13d4fa44f031f8824056a5deee/case-studies/2026-10-leg-lift-contact-cut-stocking-six-look/prompt.md#L640-L677)。

- **F：** 原稿要求夜间环境、喷泉、微风与鞋底接触石面的声音，并写出脚下降、接触、声音和切镜的事件关系；同段要求完整原音轨不变。
- **D：** 提取动作与声音的因果联系，并保留复制／新增矛盾作为必审项；不能摘取因果模板后宣称该混音已经成功。
- **所有权：** M4 提供动作接触，M6 提交声音事件与策略，M7 定位，M9 处理切点；声音模块不擅自增加落脚动作或改剪辑。

### E05 — 袜饰三镜：生成切片与连续主音轨

来源：[README L8、L40–43](https://github.com/Nuos/H3-h3-prompt-journal/blob/780a8729cca22e13d4fa44f031f8824056a5deee/case-studies/2026-10-sock-showcase-right-entry-three-shot/README.md#L8-L43)、[prompt L3、L18–31](https://github.com/Nuos/H3-h3-prompt-journal/blob/780a8729cca22e13d4fa44f031f8824056a5deee/case-studies/2026-10-sock-showcase-right-entry-three-shot/prompt.md#L3-L31)、[prompt L90–98](https://github.com/Nuos/H3-h3-prompt-journal/blob/780a8729cca22e13d4fa44f031f8824056a5deee/case-studies/2026-10-sock-showcase-right-entry-three-shot/prompt.md#L90-L98)。

- **F：** 三个独立生成任务使用 0–2.267、2.267–4.233、4.233–5.900 的切片，最后整条音频连续铺底。
- **A：** 切点落在重拍及原片逐帧对位是作者报告，本轮未试听／看帧。
- **D：** 声源版本、已给窗口、目标段与主音轨关系需要清楚；切镜不自动重播整首歌。示例中的极短生成段长度不能当成已核验的当前 API 合法值。

### E06 — 三人恶作剧：短对白、非语言发声、场内声与局部近静音

来源：[prompt L31–79](https://github.com/Nuos/H3-h3-prompt-journal/blob/780a8729cca22e13d4fa44f031f8824056a5deee/case-studies/2026-09-three-person-prank-freeze-gag-cos-swap/prompt.md#L31-L79)、[prompt L93–95](https://github.com/Nuos/H3-h3-prompt-journal/blob/780a8729cca22e13d4fa44f031f8824056a5deee/case-studies/2026-09-three-person-prank-freeze-gag-cos-swap/prompt.md#L93-L95)、[README L22–40](https://github.com/Nuos/H3-h3-prompt-journal/blob/780a8729cca22e13d4fa44f031f8824056a5deee/case-studies/2026-09-three-person-prank-freeze-gag-cos-swap/README.md#L22-L40)、[README L73–80](https://github.com/Nuos/H3-h3-prompt-journal/blob/780a8729cca22e13d4fa44f031f8824056a5deee/case-studies/2026-09-three-person-prank-freeze-gag-cos-swap/README.md#L73-L80)。

- **F：** L35/L63 将两句短日语感叹分别绑定 A/B，L75/L79 描述咳嗽与笑声；不是所有出场者都有对白。
- **F：** L93 列倒水、吞咽、塑料面罩、喷水、笑声等场内声音，并另外要求三次定格的倒带／冲击／约半秒近静音效果，动作恢复时环境声返回。
- **F：** L95 无画外音乐，但保留现场声音和后期效果。无配乐、局部近静音与全片静音不同。
- **A：** README 描述 RMS、密集抽帧和 BPM 假检测防护，以及带声结果；本轮没有执行该分析，也没有听结果文件。
- **D：** 分离语言、非语言人声、物理声、后期效果；事件逐一绑定来源。该旧稿的 14 区块格式不能当作当前 T2VA 官方模板。

### E07 — 厨房喜剧：无对白／无配乐仍保留厨房声

来源：[prompt L103–109](https://github.com/Nuos/H3-h3-prompt-journal/blob/780a8729cca22e13d4fa44f031f8824056a5deee/case-studies/2026-08-sticker-character-kitchen-comedy/prompt.md#L103-L109)。

- **F：** 原稿要求自然厨房环境及烹饪声，排除对白、人物说话、歌唱和旁白，配乐写 `None`。
- **D/P：** 可以明确没有音乐和人物发声，同时保留其他声音。当前协议的无配乐值由 M11 按所选模式归一；不能把案例旧值直接推广为所有模式的正确格式。
- **U：** 本轮没有观看或试听该案媒体，因此不能宣称烹饪拟音、同步或混音已经验证。

## 4. 四项领域规则的依据与新增部分

| 子模块 | 本次直接案例依据 | D 类实现扩展与未验证部分 |
| --- | --- | --- |
| M6.1 声源与说话者 | E06 的角色感叹／笑声分配；E01 人声未知；E02 歌词视觉化问题 | 稳定声源与音色权限接口、旁白身份、跨镜声音身份，不宣称已具备语音克隆或声纹验证结果 |
| M6.2 对白与发声事件 | E06 短感叹和非语言发声；E02/E03 不同歌词关系；E07 明确无人物发声 | 原文／批准版／格式版、长对白、打断、重叠、跨镜延续的合同与审计接口；完整剧情验证仍缺 |
| M6.3 音乐与音轨策略 | E01/E05 切片与主轨；E02 参考／复制矛盾；E03/E04 新增声冲突 | 使用策略及来源窗口审计；不附带自动节拍检测、切片制作或混音能力 |
| M6.4 环境与动作声音 | E04 接触声；E06 场内声与定格后期效果；E07 厨房声音 | 独立事件与触发接口、跨切持续语义；真实可听性、同步和效果质量需媒体检验 |

## 5. 不能从本轮材料推出的结论

不能据此宣称已经验证复杂影视对白、完整轮流说话、抢话／重叠、长句精确排时、音色稳定、精细口型、旁白声像、声音分离、具体混音数值或跨镜声音质量。不能根据案例标题、文件名或作者的“exact”“已校验”把数值写成当前实测事实。

同样，历史稿件的单人、锁机位、无字幕、无口型或微口型是各自任务的局部选择，不会在 M6 恢复成全局创作限制。当前任务和来源权限决定适用范围。

本轮可交付的是可追溯的声音编排、审计规则与合同实现。合同检查、Agent 文字审阅、作者报告、实际媒体检查分别报告；没有实际媒体时，听觉质量与 G3/G4 均保留 U。后续如新增真实对白或音频分析样本，按实际提交、读取范围、方法及结果补入索引，不改写本次覆盖历史。
