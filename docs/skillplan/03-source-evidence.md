# 通用 AI 视频创作模块：来源证据、覆盖范围与适用性

**文档日期：2026-11-04（America/Los_Angeles）**

**项目基线：`35658d3615d02c6aa6e4221fb223d73b86aa6875`**

**文档状态：开发提炼计划的证据说明；不构成新模块已完成实现或视频效果认证。**

## 核心摘要

本轮以 `case-studies/` 中 2026 年 10 月及之后的案例为重点。固定基线中符合这一时间范围的案例为 **15 个，全部位于 2026-10 目录；没有 11 月或更晚的案例目录**。完整阅读范围为 15 份 README、2 份 methodology、14 份 prompt，合计 **31 个指定文件、9,618 行**；另完整阅读动作链库的实际正文 `dance-motion-chain-h3.md`，共 2,767 行。因此，本轮核心案例文本覆盖为 **32 个文件、12,385 行**。[S01]

这些文本支持提炼共同的创作控制关系：作品意图决定段落任务，参考权限界定可继承和可改变的信息，动作链建立事件与身体的因果过程，摄影机决定观看方式，统一时间轴协调动作、声音与镜头，状态与剪辑契约管理跨镜关系。本文将这些依据映射到统一编号 M1–M12；**模块划分、共享数据接口、依赖关系和开发顺序属于本次架构推论，不是原仓库已经实现的通用引擎**。

案例中同时存在提前运镜、同步运镜、故意滞后运镜，以及动作完成后切镜、动作中匹配切镜、独立蒙太奇等不同方法。通用化必须保留适用条件，不能将这些策略合并成相互矛盾的全局规则。参考图的外观权限、当前事件状态、实际首帧要求也必须分别管理。[S02][S03][S05][S09][S11]

现有 `docs/caseskill/` 已有 29 个独立案例技能及格式、来源、静态工具验证记录；它们提供可复用的起点。历史报告记载 106 个已编写代表任务，但**没有全部执行**，实际离线任务为 2 项独立代理试用和 1 项主编试用。上述验证均不能替代 H3 推理、媒体观察或真实剪辑验收。[S18]

本轮未重新完整阅读或执行动作迁移工作流 JSON，也未查看或测量案例图片、音频和视频。原文中的作者实测、成功叙述、打勾清单与参数说明均按其证据性质保存，不改写成本轮已验证的结果。影视剧的对白、人物目标与冲突、多人反应和长篇叙事连续性，需要新增资料及代表任务后才能形成充分覆盖。

## 关键词

通用视频编排；案例证据；条件化规则；参考权限；动作因果；摄影机几何；音画时序；状态连续性；分镜与剪辑；模型适配；持续审计；影视剧与音乐 MV。

## 目录导航

1. 来源版本与完整阅读边界
2. 十五个案例的文件覆盖清单
3. M1–M12 的证据含义与案例映射
4. 证据分级、规则强度与已有实现
5. 代表性冲突及条件化裁决
6. 影视剧方向的证据空缺
7. 从证据到开发与审计的使用规则
8. 本文可支持和不能支持的结论
9. 固定来源目录 S01–S19

## 1. 来源版本与完整阅读边界

### 1.1 固定基线

| 来源 | 固定版本 | 本文中的用途 |
|---|---|---|
| 本项目与案例目录 | `35658d3615d02c6aa6e4221fb223d73b86aa6875` | PR #1 合并后的项目状态；本文的案例文件链接全部固定到此提交。[S01] |
| 先前案例与评估基线 | `91a33376e9ae84d0b9b3a2c1a7f6991d5b9e358e` | 与当前基线对比，`case-studies/` 没有变更；因此原案文本与先前案例技能来源可以对照。 |
| MiniMax H3 官方资料 | `199b7d0e1fd95e7b3eafa8c15eca692534142427` | 解释模式、引用、字段与运行规格；区分案例写法和当前采用的官方协议。[S17] |
| Agent Skills 官方资料 | `83021e2be457a9b6679148719c1f6074f0ad975e` | 区分技能格式要求、组织建议及评估方法；不据此认证视频创作效果。[S19] |
| 已有案例技能集合 | 本项目当前基线中的 `docs/caseskill/`，集合报告版本 1.0.0 | 记录已经存在的技能、检查器及离线试用；与未来通用模块开发分开。[S18] |

H3 与 Agent Skills 版本也可在现有 `docs/caseskill/_standards/` 的来源清单中核对。固定提交用于保证复核位置稳定，不表示后续开发可以永久忽略官方更新。

### 1.2 读取范围与排除范围

本轮的全文覆盖以实际文件为准：缺少 `methodology.md` 的案例不虚构该文件；动作链库没有 `prompt.md`，其 `dance-motion-chain-h3.md` 是必须补读的主体资料。长文件按连续范围阅读；完全相同的重复段落可用首次出现位置复核，但不同正文、时间值、引用和段间说明均纳入分析。

以下内容不计入本轮“32 文件、12,385 行”的全文覆盖数：

- `h3-motion-transfer-workflow.json`：本轮没有重新完整阅读或执行。此前技能创建阶段曾分析该工作流的连线与参数，那是另一轮记录；本文不以之冒充本轮完整阅读。
- 图片、视频、音频、封面、字幕源文件及本机媒体路径：本轮未查看或测量。README 对它们的说明属于文本证据。
- 8 月和 9 月的 14 个案例：属于已有 29 技能集合的背景，不是本轮 10 月重点全文覆盖的组成部分。
- `case-studies/VOCABULARY-EXPANSION.zh-CN.md`：公共词汇索引，不是独立案例，也未计入本轮文件总数。
- `docs/casereview/`、`docs/caseskill/` 中的评估、封装与修复：作为辅助资料，与原案文本分开标识。

此前技能集合报告中的“10 月 33 份案例文本”包含工作流 JSON；本轮为指定 Markdown 文件加动作链正文，共 32 份。两组统计的口径不同，不互相替代。[S18]

## 2. 十五个案例的文件覆盖清单

表中数字是文件实际行数；“—”表示该文件不存在。案例路径均为 `case-studies/` 下列目录。来源 ID 对应文末固定链接。

| 案例目录 | 来源 | README.md | methodology.md | prompt.md | 补充正文 | 合计 |
|---|---|---:|---:|---:|---:|---:|
| `2026-10-advanced-camera-combinations` | [S06] | 57 | — | 328 | — | 385 |
| `2026-10-baifeng-mengchen-classical-dance-six-segment` | [S10] | 155 | — | 475 | — | 630 |
| `2026-10-camera-movement-discipline-library` | [S05] | 93 | — | 234 | — | 327 |
| `2026-10-classical-wuxia-dance-13-segment` | [S02] | 83 | 199 | 543 | — | 825 |
| `2026-10-dance-motion-chain-library` | [S07] | 41 | — | — | `dance-motion-chain-h3.md`：2,767 | 2,808 |
| `2026-10-four-subject-formation-choreography` | [S08] | 164 | — | 148 | — | 312 |
| `2026-10-h3-motion-transfer` | [S16] | 54 | — | 586 | — | 640 |
| `2026-10-identity-only-half-body-dance-six-segment` | [S09] | 54 | — | 1,524 | — | 1,578 |
| `2026-10-kanzaki-beach-sword-dance-18-segment` | [S03] | 115 | 346 | 1,186 | — | 1,647 |
| `2026-10-leg-lift-contact-cut-stocking-six-look` | [S14] | 58 | — | 759 | — | 817 |
| `2026-10-physical-camera-position-library` | [S04] | 61 | — | 795 | — | 856 |
| `2026-10-sock-showcase-right-entry-three-shot` | [S15] | 52 | — | 98 | — | 150 |
| `2026-10-summer-pool-beach-waterline-mv-4-segment` | [S12] | 146 | — | 283 | — | 429 |
| `2026-10-waterfront-solo-dance-two-segment` | [S13] | 48 | — | 119 | — | 167 |
| `2026-10-xiashan-veiled-solo-twelve-segment` | [S11] | 71 | — | 743 | — | 814 |
| **合计** | **15 案** | **15 份／1,252 行** | **2 份／545 行** | **14 份／7,821 行** | **1 份／2,767 行** | **32 份／12,385 行** |

指定三类文件的合计为 `15 + 2 + 14 = 31` 份，行数为 `1,252 + 545 + 7,821 = 9,618`；加入动作链正文后为 `9,618 + 2,767 = 12,385` 行。

## 3. M1–M12 的证据含义与案例映射

### 3.1 统一模块编号

| 模块 | 名称 | 原文支持的核心关系 | 推广时的主要边界 |
|---|---|---|---|
| M1 | 作品意图、叙事／情绪与段落功能 | 先定义作品与每段任务，再组织动作、能量曲线和可识别母题。[S02] methodology L19–29、L71–78；[S03] methodology L210–231。 | MV 情绪曲线不等于完整影视剧因果结构。 |
| M2 | 素材解析、资产绑定与参考权限 | 明确图片、视频、音频分别提供身份、服装、动作、场景、时间等哪些信息。[S03] methodology L39–65；[S09] prompt L7–44；[S11] prompt L20–25。 | 参考身份不自动等于锁首帧、姿态、背景或摄影机。 |
| M3 | 场景空间、人物站位与交互调度 | 人物身份与槽位分开；队形、交叉、承重、接触和观察空间需要明确。[S08] prompt L34–62、L77–86；[S07] 正文 L589、L636–638。 | 四人队形是样本，不设所有题材统一人数上限。 |
| M4 | 人物表演、动作链与物理因果 | 起始条件、发力与支撑、发展、峰值、制动、恢复、下一动作构成完整过程。[S02] methodology L31–69；[S03] methodology L194–201；[S07] 正文 L17–56。 | 舞蹈中的动力链不能未经改造套用于全部生活动作和对白表演。 |
| M5 | 机位、景别、构图、焦点与运镜 | 位置、高度、距离、光轴、路径、构图重点分别描述。[S04] prompt L17–28、L719–750；[S03] methodology L122–130。 | 机位不等于景别；固定位置摇摄、滚转、变焦也不能一概说成摄影机平移。 |
| M6 | 声音、音乐、对白与歌词关系 | 区分节奏参考、完整音轨复制、音乐、环境声、发声、口型和歌词意象。[S07] 正文 L924–927；[S03] methodology L203–208；[S11] README L50–52。 | 无对白、无口型、无字幕是部分 MV 的任务策略，不是影视剧通用禁令。 |
| M7 | 统一时间轴与动作—镜头—声音协同 | 全局与局部时间、首拍相位、动作峰值、摄影机响应和接触声音共享可核对时序。[S02] methodology L130–144；[S05] prompt L11–12、L88–125、L159–167；[S14] README L21–40。 | 共享时钟不意味着所有动作与摄影机必须零时差。 |
| M8 | 主体、道具、场景与跨镜状态连续性 | 外观、数量、持有、位置、当前事件状态和世界关系分别管理。[S03] methodology L132–171、L254–267；[S10] prompt L465–475。 | 连续性允许有原因、有授权的状态变化；不能把参考初始状态永久冻结。 |
| M9 | 分镜组织、转场、剪辑与生成分段 | 先声明连续镜头、动作匹配或独立蒙太奇策略，再规定生成边界与后期连接。[S02] methodology L122–144；[S03] methodology L233–252；[S15] README L20–44。 | 时间块、Shot 标签、真实镜头、生成任务与最终剪辑段不是同一概念。 |
| M10 | 视觉风格、光线、色彩与材质 | 风格基线应明确作用于身份、衣物、环境、光源或调色中的哪一层。[S09] prompt L86–121、L1296–1342；[S11] prompt L34；[S12] prompt L44–58、L152–188。 | 冷暖光源与整体调色需要分开；某种画幅、调色或柔焦不是通用默认值。 |
| M11 | 模型协议编译与运行参数适配 | 创作记录需要变为指定模式的字段、素材引用、时长、帧率与实际参数。[S03] methodology L290–304；[S16] README L21–42；[S17]。 | 案例旧提示词、界面显示值和作者经验上限不能直接充当当前官方协议或有效运行值。 |
| M12 | 持续审计、问题归因与反馈修复 | 输入、结构、时序、连续性与作品表达分别检查；按错误归属修复并复核影响。[S03] methodology L269–288、L306–324；[S02] methodology L178–191；[S15] README L11–16。 | 静态通过、作者报告和实际视频验证必须分开；一轮通过不证明普遍成功率。 |

这里的“原文支持”表示可以找到相应方法或问题的文字依据。它不表示原文已经采用 M1–M12 的模块编号，也不表示相应模块已经完成工程实现。

### 3.2 十五案到模块的主要映射

下表列出每案对通用化最直接的贡献，不穷举该案出现过的所有摄影或声音术语。“主要映射”不排除其他模块协作。

| 案例／来源 | 主要映射 | 可提炼的具体能力与证据位置 |
|---|---|---|
| 高级运镜组合 [S06] | M5、M7、M12 | 起止机位、物理移动、动作触发和终态的组合模板；prompt L11–23、L44–294。必须检查标题、实际路径和触发时间是否一致。 |
| 白凤蒙尘六段 [S10] | M1、M4、M7、M8、M9 | 用支撑、高度、轴线与受阻恢复表达情绪；README L59–82；prompt L123–134、L327–340、L395–408；跨段手腕、掌心、眼线接续见 L465–475。 |
| 动态运镜纪律库 [S05] | M5、M7、M9、M12 | 提前到位、同步响应、滞后追随及不同切镜策略；prompt L11–12、L37、L77、L88–125、L159–167；五项机位块 L191–201。 |
| 古典武侠舞十三段 [S02] | M1、M4、M7、M8、M9、M12 | 动作母题、持续／主链／微动作分层、局部时间、音乐连续、剪辑模式和导演级自检；methodology L31–78、L122–144、L178–197。 |
| 舞蹈动作链库 [S07] | M3、M4、M5、M7、M12 | 动作分类、入出态、支撑与接触、机位结构及逐窗验收；正文 L17–56、L589、L636–638、L873–878、L1856–1890。标题、分解与示例须交叉核对。 |
| 四人队形编舞 [S08] | M2、M3、M4、M7、M8 | 固定身份与队形位置分开，分配四人的动作机制与交叉时序；prompt L8–20、L34–62、L77–134。 |
| H3 动作迁移 [S16] | M2、M4、M5、M7、M11 | 图片、动作视频、音频三类权限；首帧几何、身体机制、摄影机与重定时；prompt L118–155、L279–441。运行参数仍需独立读取实际工作流。 |
| 仅身份半身舞六段 [S09] | M2、M5、M8、M9、M10 | 图片 grant／deny 权限、姿态与镜头另行指定、动作中同向续接、风格与曝光边界；prompt L7–84、L86–172、L1296–1342。 |
| 海滩剑舞十八段 [S03] | M1、M2、M4、M6、M8、M9、M12 | 参考权限、道具外观／状态双轨、全曲段落功能、单段自包含、后期桥接和双层自检；methodology L39–65、L132–171、L210–252、L290–324。 |
| 抬腿触地换装 [S14] | M4、M5、M7、M8、M9 | 接触事件驱动切换、永久支撑与活动腿、切后保持再起抬、声音与切点共时；README L21–40；prompt L45–106、L153–219、L604–632。 |
| 物理摄影机机位库 [S04] | M3、M5、M7 | 空间位置与光学结果、光轴与高度、固定位置 tilt 与 roll 的区别、八项机位要素；prompt L17–28、L579–657、L719–750。 |
| 右入三造型展示 [S15] | M6、M8、M9、M12 | 逐帧推翻步中变装误判，状态独立生成、硬切装配及整轨铺底；README L11–16、L20–44。 |
| 夏日泳池海滩水线 MV [S12] | M2、M4、M5、M8、M9、M10 | 身份参考与首帧分离，湿发、毛巾、岸线与水线的状态关系，单镜／切镜混合和视觉统一；README L30–44、L111–130；prompt L68–78、L136–148、L182–210、L248–266。 |
| 水岸独舞两段 [S13] | M4、M7、M8、M12 | 动作因果、入出态与小节网格、跨段拍相位、检测假阳性和锚点检查；README L12–30、L42–48；prompt L43–47、L69、L77、L92–95。 |
| 下山面纱独舞十二段 [S11] | M2、M4、M6、M7、M8、M9、M10、M12 | 双图分权、袖子与面纱身份分离、局部续动、稳定／滞后摄影机、歌词分层与末态终止；README L25–56、L64–71；prompt L20–45、L187、L248、L614、L675、L724–736。 |

## 4. 证据分级、规则强度与已有实现

### 4.1 四类证据状态

这四类是不同性质的记录，不是可以混用的“可信度分数”。

| 代码 | 类别 | 可以据此陈述 | 不能据此陈述 |
|---|---|---|---|
| F | 原文可确认事实 | 某文件存在某条规则、某组时间、某种方法或某个作者报告；注明固定文件和位置。 | 作者说“实测稳定”就等于本轮已经复现；原文打勾就等于约束全部成立。 |
| D | 架构推论与开发提案 | 将多个案例共性抽象成 M1–M12、共享记录、条件分支、审计依赖和开发任务；说明推导依据。 | 原仓库已经实现该架构，或所有题材均已验证适用。 |
| I | 已有实现与已执行检查 | 已有 29 个案例技能、静态检查脚本、已保存的格式／来源／回归和三项离线试用结果。 | 新的通用模块已开发完成，或静态检查自动理解并证明了所有创作语义。 |
| U | 尚未验证或证据不足 | 标注待验证的生成、识别、同步、衔接、物理和跨题材效果，提出验证方法。 | 把待验证项填写为 pass，把没有媒体证据的计划状态写成实际成片状态。 |

例如，[S08] README L46–51 的身份漂移描述属于 **F：作者结果报告**；本轮能确认作者写了这些内容，不能把它升级为本轮媒体观察。M3 的通用交互调度设计属于 **D**。现有检查器能检查某些时间、引用和输入合同，属于 **I**。多人在遮挡后的真实身份稳定率仍属于 **U**。

### 4.2 规则强度是另一个维度

证据来源与强制程度需要分别记录：

1. **用户明确要求：** 由当前任务决定，如角色、台词、换装、是否允许切镜、是否允许场景改变。
2. **已核对的模型或工作流约束：** 来自指定版本的官方协议及实际后端能力，记录版本和适用模式。[S17]
3. **项目策略：** 例如单人表演、一镜到底、固定场景、整轨复制；可被其他项目的需求替换。
4. **作者经验与风格选择：** 例如一个主运镜、动作密度参考、无度数描述、先跑某个风险片段；保留条件，不能写成普遍模型硬限制。
5. **待核实声明：** 缺原始音频、成片、执行日志或运行配置时，保留为待验证项。

Agent Skills 对技能格式的规范与视频创作领域约束也应分开。技能目录及有效 `SKILL.md` 是格式基础；`references/`、`scripts/`、`assets/` 和 `agents/openai.yaml` 等属于可选组织。格式检查通过不会证明动作成立、镜头可行或视频连续。[S19]

### 4.3 已有实现能够承接什么

已有 29 案技能提供案例工作流、参考协议说明、输出模板、合同、静态检查器、来源快照和代表任务定义。保存报告给出的结果包括：官方格式验证 29/29、创建器检查 29/29、126 份来源快照一致、234 处证据位置有效、21 项项目回归通过，以及三项实际离线任务。[S18]

这些结果的边界必须保留：

- 234 处检查证明路径与行界有效，不代表机器自动判定每条引文都充分支持结论。
- 历史 40 项上游参考实现测试与本项目 21 项回归是两组不同测试，不能合并成 61 项通用视频模块测试。
- 106 项是已编写场景，不是 106 次已完成试验。
- 三项离线任务中，缺少真实素材的三造型方案保留 draft，严格检查按预期拒绝就绪；不能将其说成已成功生成视频。
- 静态检查器明示未执行语义认证与模型推理。计划、脚本与日志的存在，不等于已经有通用视频观察器、自动剪辑器或闭环生成系统。

未来通用 M1–M12 可以复用上述资料与检查思路；通用接口、模块调度、影视剧配置、媒体验收及跨模块自动回归仍是开发工作，不能以已有文件数量代替完成证明。

## 5. 代表性冲突及条件化裁决

以下“裁决”是进入通用模块前的设计要求。它保留原文、记录问题并提出适用条件，不在本轮改写案例源文件。

### 5.1 响应时序与切镜策略

| 问题 | 原文位置与事实 | 条件化裁决 |
|---|---|---|
| 提前、同时、滞后规则同时出现 | [S05] prompt L11–12 要求在强调点前 1.5–2 秒到位；L88–125 允许故意滞后；L145、L159–167 又写同时启动与峰值同步。[S07] 正文 L23–30、L691–692、L777–809 也分别出现这些策略。 | M7 使用同一时间轴，但逐事件选择提前、同相、延迟等响应关系，记录触发、偏移、结束条件。不能把所有策略同时设为全局强制。 |
| 运镜示例不完全符合总则 | [S06] prompt L277–287 先微推、后动作触发，并出现人物 4.8 秒与相机 5.4 秒的不同起点。 | 保留设计意图并检查实际时序；“动作驱动镜头”不等于两个轨迹每个节点都同秒。 |
| “无度数”偏好被当成通用物理规则 | [S03] methodology L93–105 优先物理关系且明确数字角度并非所有任务都禁用；prompt L130 却仍使用25–35度弧线。[S04] prompt L291–308、L396、L442也保留角度数值。 | M5 优先解释实际位置、光轴、路径与构图；数值可作为有用补充。只有当前项目明确禁用数字时才执行该文风规则，不把它升级为模型限制。 |
| 禁止动作中切镜与相位匹配切镜并存 | [S05] prompt L37 说不在动作半途切；L77 明确在旋转中保持方向、速度和肩位切镜。[S07] 正文 L1950、L1968 与 [S09] prompt L159–172 采用不同切点策略。 | M9 先声明动作完成切、动作相位匹配、独立蒙太奇或连续镜头，再调用相应审计规则；切镜政策独立于相机响应偏移。 |
| 生成段、动作章节与真实镜头混淆 | [S10] prompt L55 把 Shot 称为动作章节；L76、L298 又安排插入近景并切回。[S12] prompt L182–210 在同一段中含真实切镜与连续转换。 | M9 展开真实镜头、切点和生成任务三张关联记录，不能用标签数量直接推断实际镜数或切点数。 |

### 5.2 参考权限、空间与状态

| 问题 | 原文位置与事实 | 条件化裁决 |
|---|---|---|
| 身份参考被误当首帧或全部视觉权限 | [S09] prompt L7–44、L60–84 划定图片允许与禁止继承项；[S12] README L30–44 明确身份图不等于首帧；[S03] methodology L154–163 要求当前道具状态覆盖原图初始状态。 | M2 分别登记身份、外观、姿态、场景、摄影机、首尾帧等角色；M8 使用当前事件状态。输入图片数量不能单独决定这些用途。 |
| 固定身份与固定站位混淆 | [S08] README L78–79 要求各守象限、不穿中线；prompt L79–86 却包含中心交叉与换层。 | 身份 ID 始终稳定，槽位可以按授权时序改变；交叉路径、先后、遮挡与结束位置需单独写入 M3。 |
| 相机后退与拍摄距离增加混淆 | [S08] prompt L71 写 backpedal，L75 又要求距离近乎恒定、不退成远景。 | 分开摄影机的世界位移、主体位移和相对距离；跟随向前人物的后退，不自动等于拉远。 |
| 外观规则与状态变化混淆 | [S03] methodology L132–171；prompt L224–240 规定已出鞘但仍继承同一剑与鞘的外观。[S14] prompt L117 的全保留表述与计划改变袜饰并存。 | M2 定义属性保留范围，M8 定义状态与授权变化项；保留对象身份不意味着所有属性永远不变。 |
| 单人表演规则扩散为通用人数限制 | [S02] README L53–55、[S03] prompt L27 是当前作品的单人设定；[S08] 实际研究四人队形，[S07] 包含多人动作模板。 | 人数由当前剧情或编舞确定；不建立适用于全部影视剧与 MV 的统一人数上限。 |
| 两段拔刀被误判为必然连续性错误 | [S03] prompt L118 与L163–179 分别明确两个独立开场拔刀段；L45、L195 允许蒙太奇组织而非逐帧承接。 | 保留原案明确的蒙太奇许可。只有当前任务要求同一物理动作无间断连续时，才要求前段出态直接进入后段入态。 |
| 同一段事件时间冲突 | [S03] prompt L118 要求在3.500–3.850秒拔刀；L124 又在3.870秒发起拔刀。 | 对同一事件建立唯一权威时间，不以重复描述增加“约束强度”；修复后重新检查状态转移和镜头覆盖。 |

### 5.3 动作预算、静止层级与正文交接

| 问题 | 原文位置与事实 | 条件化裁决 |
|---|---|---|
| 动作标题拍数与实际分解不符 | [S07] 正文 C19 L398–400、C25 L434–436 标7拍但展开至第8拍；K9 L2295–2297 标6拍但展开至第8拍；K16 L2342–2344 标2拍却有第3拍。 | M4 以实际动作阶段建立记录，M7 计算总时长；标题、分解、英文示例和时间预算必须一致，不能只验标题。 |
| 中文与英文示例承载不同机制 | [S07] 正文 D8 L619–621 的中文渐亮与英文聚散不对应，英文与D13 L640–642重复。 | 规则抽取必须比较语义，不能把双语字段存在当作对齐完成；不确定时保留冲突并分别标明版本。 |
| 持续层与绝对静止冲突 | [S11] prompt L45 规定持续层在 holds／stillness 中也不停；L724、L730–733 又规定绝对静止与终止。[S13] prompt L77 与L92–95有类似张力。 | M4/M8 分别规定身体大动作、呼吸、衣料、头眼和摄影机的停止范围；最终终止条件可覆盖一般持续层。不能全局要求“永不静止”。 |
| 段间表格与实际提示词不一致 | [S10] prompt L470 要求第三段承接交叠前臂，但L196仍从图片站姿开始；L471写第三段末为承重掌特写，L231–232正文只写低位 held beat。 | M8/M9 同时检查摘要、交接表和实际复制的正文。计划承接条件必须落到片段内容，不能只在末尾总表声明。 |
| 特写标题与内容不一致 | [S11] prompt L170–171 标 HAND 但先写脚部；L475–476 标 HAIR 但描述脚步；[S06] prompt L193 与L196 的前跟标题、后方开场不一致。 | M5 将可见对象、光轴、景别与动作信息交叉核对；镜头名不能覆盖正文实际含义。 |
| 转换次数与状态数混淆 | [S14] README L34–36 标“六款”却枚举 LOOK 0至6。 | M8 对初态和六次转换分别计数；顺序不重复变化时共有七个显示状态。若目标确为六款，必须另行决定减少哪次转换或如何复用状态。 |
| 摘要切点与真实段落边界不符 | [S15] README L22 规定旧镜末尾 pose、每新镜右入；L26又称切点两边都在迈步。prompt L4、L25、L52、L79延续 pose→新步入的结构。 | 选择与实际目标一致的接续，并明确是姿态到步入的跳切还是动作相位匹配；不靠“看起来连续”略过两侧状态。 |

### 5.4 声音、歌词、风格与执行协议

| 问题 | 原文位置与事实 | 条件化裁决 |
|---|---|---|
| 音频仅作节奏参考与完整复制并存 | [S11] prompt L23–25 说只参考节奏、无信号复制，L28、L32又要求完整1:1音轨。 | M6 先选择音轨策略，M11 按官方模式表达；引用、局部复用和完整复制不能同时无条件生效。[S17] |
| 完整音轨复制又要求添加声音 | [S03] prompt L103、L111 与L141–145；[S14] prompt L640–677。 | 先确认所谓“完整音轨”究竟指最终混音还是其中音乐素材。完整最终音轨复制与额外新增声音不能未经声明合并；需要后期混音时另列任务。 |
| 歌词时间和动作说明不一致 | [S02] prompt L185–190 对首个发声及各句时点的说明与L193–195的 vocal表不一致。 | M7 回到实际音频或可信清单核对；缺音频时记录为未核实，不能仅据“exact”或打勾声明通过。 |
| 歌词意象被自动实体化 | [S11] README L15–21 报告歌词与场景词引出额外宾客、面纱变化；prompt L20–41对歌词、表情和穿戴物分权。 | M2/M6 分开原句、发声、字幕、情绪作用和视觉授权；歌词中出现人物或物体不自动授权生成它们。 |
| 首拍相位被每段复制 | [S13] prompt L69 在第二段仍声明相同首拍数值；[S11] prompt L23及各段重复首拍0.441。 | 保留全局节拍索引和裁切起点，将全局事件转换为局部时间；没有测量依据时不能声称每段已准确重新起拍。 |
| 风格基线与局部光源混淆 | [S12] README整体冷中性方向与prompt L44、L58、L152暖光及L188禁暖表述并存。 | M10 区分物理光源、色温、环境材质和最终调色；有意暖光与整体冷调可以共存，需写清作用层级。 |
| 原文长短片段被说成均可单次生成 | [S07] 正文 H01 L935–941、H07 L1025–1031、J6–J9 L2085–2178存在不同长度；[S15] prompt L17、L45、L72请求2.267、1.966、1.667秒。 | M11 核对当前后端，不把素材时长等同合法生成时长；需要延长生成后裁切或拆段时，保留原创作目标并记录生成／编辑时间线。[S17] |
| 作者工作流经验被泛化为 H3 硬上限 | [S16] prompt L10–12、L584–586声明8–9秒上限，并同时写9秒、124帧、24FPS。仅按普通帧数换算，124/24约为5.17秒。 | 该文本存在需要核对的参数关系；本轮未读JSON，不能裁定有效连线值。后续必须读取指定工作流和执行记录，再比较官方版本能力，不能照抄“所有迁移最多8–9秒”。 |
| 案例旧格式与官方协议不同 | [S10] prompt L36–52、[S11] prompt L19–43、[S15] prompt L24等存在自定义区块或字段混用。 | M11 将创作意图编译到所选模式的当前格式。基础模式三字段与Ref2VA六字段分开，保留原始来源，不把旧稿直接升级为协议模板。[S17] |

### 5.5 可读性与证据不能相互替代

“全身、表情、手、脚、道具全轨迹同时清楚”经常是多个视觉目标竞争。剑舞方法论要求先确定这一刻观众必须看清什么，再决定景别与距离。[S03] methodology L122–130。通用审计应检查镜头是否覆盖所需动作证据，而不是要求每个镜头永远把所有部位纳入。

同样，切点检测、关键帧检测与作者文字判断都可能出错。右入三造型案例记录了提高抽样密度、调整检测阈值并逐帧复核后推翻“步内变装”解释的过程。[S15] README L11–16。这支持 M12 保留“假设—证据—修正”链条；具体阈值只属于该素材与方法，不能成为所有视频的通用常数。

## 6. 影视剧方向的证据空缺

案例对舞蹈、表演 MV、动作迁移、展示和摄影机控制的支持较强。将模块用于影视剧时，下列能力需要新增来源、规则与代表任务；不能用目前案例的数量填补证据空缺。

| 待补能力 | 现有依据能够支持到哪里 | 后续需要的证据或任务 |
|---|---|---|
| 戏剧因果与信息分配 | M1已有段落任务、能量曲线、动作母题、受阻与恢复的表达。 | 人物目标、冲突、选择、后果；观众与角色的知识差；铺垫、揭示和回收的可复核场景。 |
| 多角色对白与反应 | M6能够区分音乐、对白、口型与画面文字；本轮多数案例主动不生成对白。 | 台词轮次、说话者与声线绑定、听者反应、停顿与打断、画外发声、跨镜持续台词。 |
| 多人交互与道具交接 | M3/M4有四人队形、接触和承重模板，M8有道具数量与持有状态。 | 对话站位、目光、走位、交接、短时遮挡后再现，以及多人同时执行不同目标的场景。 |
| 场景地理与叙事剪辑 | M5/M9有物理机位、局部接续、动作匹配和蒙太奇政策。 | 场景入口与出口、行动轴线、正反打、视线对应、空间建立镜头、时空省略及有意打破连续性的案例。 |
| 人物心理与细微表演 | M1/M4已有舞蹈情绪和头眼、手部细节。 | 同一台词的不同意图、压抑与伪装、听到信息后的反应、无台词表演，避免只用抽象情绪词。 |
| 叙事声音设计 | M6已有音乐权威、环境声和歌词用途区分。 | 音乐进入退出、环境声提示画外事件、对白可懂度、声画错位、声音桥及最终混音验收。 |
| 长篇故事状态 | M8支持独立片段中的身份、持物和环境状态。 | 时间跳跃、回忆、服装或伤痕有因果变化、跨地点路线、连续多场戏的状态账本。 |
| 成片质量与迭代效率 | M12已有静态检查和案例中的失败归因思路。 | 实际H3生成及固定样本评估、问题定位准确率、修改后效果与代价、接缝和声音的真实观察记录。 |

这些补充不要求推翻已有 29 个案例技能。更合适的开发方向是复用共同的对象、事件、空间、时间与状态接口，在上层分别配置影视剧叙事流程和音乐 MV 流程。该组织方式属于 D 类架构提案，仍需通过任务检验。

## 7. 从证据到开发与审计的使用规则

### 7.1 一条通用规则必须保留的最小证据

每条提炼规则至少应记录：

- 规则 ID、所属模块及适用任务；
- 固定来源文件、行范围和原文含义；
- 证据类别 F／D／I／U，以及作者报告是否已复现；
- 生效条件、例外、允许变化项和不适用条件；
- 与其他规则的冲突及裁决理由；
- 检查方式：确定性检查、文本语义审核、媒体观察或实际运行；
- 失败时的负责模块、最小修复范围及需要复核的下游项目。

例如，提前到位与滞后追随应成为同一 M7 接口下的不同策略；单镜连续与独立蒙太奇应成为 M9 的不同模式。不能将所有规则复制进每个任务的提示词。

### 7.2 保留原案与修订后的通用规则

原案文件继续作为不可混淆的历史来源。通用开发文件应另存提炼规则、裁决记录和示例，不悄悄改写原案来消除冲突。已有案例技能对某些问题的处理可以作为 I 类实现参考，但必须说明它与原始提示词的差异。[S18]

作品层可以维护统一规则库和状态记录；每次生成时，由 M11 注入该片段必要的身份、状态、参考和执行要求。案例强调的“单段自包含”是实际输入完整性要求，并不排斥作者侧集中维护公共规则。[S03] methodology L290–304；[S11] README L15、L60。

### 7.3 审计状态应随证据变化

建议至少区分“待补输入、文本草稿、静态检查完成、语义复核完成、待生成、媒体已观察、接续已验收”等状态。名称与实现可在开发阶段调整，但不得以填写状态字段代替证据。

任何会改变动作、时长、参考权限、片段边界或道具状态的修改，都应触发相应下游复核。例如更换音乐要重新检查局部时间、动作峰值、镜头响应与剪辑点；改变道具持有手要检查动作链、镜头可见性与下一镜入态。是否自动化以及自动化范围，属于待开发与验证工作。

## 8. 本文可支持和不能支持的结论

本文能够支持：15 个重点案例的文件覆盖是完整且可复核的；M1–M12 的主要职责具有具体原文依据；案例间存在值得条件化的共同方法与冲突；已有技能集合提供格式、来源和部分静态工具基础；影视剧应用需要进一步补齐证据。

本文不能支持：12 个通用模块已经全部实现；原案所有规则均正确；动作、相机或音乐已按提示词真实执行；人物身份、物理动作、对白和剪辑接缝已通过媒体验证；106 个任务已经全部运行；采用这些模块必然提高视频成功率。

后续完成状态应由实际交付、明确的验收任务和保存的验证结果决定。本轮交付属于完整保存分析和制定开发提炼计划，不将计划叙述为已完成的软件或生成结果。

## 固定来源目录

以下链接集中列出来源。除 H3 与 Agent Skills 官方资料外，项目链接全部固定到 `35658d3615d02c6aa6e4221fb223d73b86aa6875`。正文给出的文件与行范围以这一版本为准。

## S01 案例目录基线

- [case-studies 目录：本轮项目基线](https://github.com/Nuos/H3-h3-prompt-journal/tree/35658d3615d02c6aa6e4221fb223d73b86aa6875/case-studies)
- [先前案例来源基线](https://github.com/Nuos/H3-h3-prompt-journal/tree/91a33376e9ae84d0b9b3a2c1a7f6991d5b9e358e/case-studies)
- [已有案例技能总索引](https://github.com/Nuos/H3-h3-prompt-journal/blob/35658d3615d02c6aa6e4221fb223d73b86aa6875/docs/caseskill/README.md)

## S02 古典武侠舞十三段

- [README.md，L1–83](https://github.com/Nuos/H3-h3-prompt-journal/blob/35658d3615d02c6aa6e4221fb223d73b86aa6875/case-studies/2026-10-classical-wuxia-dance-13-segment/README.md#L1-L83)
- [methodology.md，L1–199](https://github.com/Nuos/H3-h3-prompt-journal/blob/35658d3615d02c6aa6e4221fb223d73b86aa6875/case-studies/2026-10-classical-wuxia-dance-13-segment/methodology.md#L1-L199)
- [prompt.md，L1–543](https://github.com/Nuos/H3-h3-prompt-journal/blob/35658d3615d02c6aa6e4221fb223d73b86aa6875/case-studies/2026-10-classical-wuxia-dance-13-segment/prompt.md#L1-L543)
- [第五段动作与 vocal 时间表，L185–195](https://github.com/Nuos/H3-h3-prompt-journal/blob/35658d3615d02c6aa6e4221fb223d73b86aa6875/case-studies/2026-10-classical-wuxia-dance-13-segment/prompt.md#L185-L195)

## S03 海滩剑舞十八段

- [README.md，L1–115](https://github.com/Nuos/H3-h3-prompt-journal/blob/35658d3615d02c6aa6e4221fb223d73b86aa6875/case-studies/2026-10-kanzaki-beach-sword-dance-18-segment/README.md#L1-L115)
- [methodology.md，L1–346](https://github.com/Nuos/H3-h3-prompt-journal/blob/35658d3615d02c6aa6e4221fb223d73b86aa6875/case-studies/2026-10-kanzaki-beach-sword-dance-18-segment/methodology.md#L1-L346)
- [prompt.md，L1–1186](https://github.com/Nuos/H3-h3-prompt-journal/blob/35658d3615d02c6aa6e4221fb223d73b86aa6875/case-studies/2026-10-kanzaki-beach-sword-dance-18-segment/prompt.md#L1-L1186)
- [第一段拔刀与镜头说明，L118–145](https://github.com/Nuos/H3-h3-prompt-journal/blob/35658d3615d02c6aa6e4221fb223d73b86aa6875/case-studies/2026-10-kanzaki-beach-sword-dance-18-segment/prompt.md#L118-L145)
- [单镜与后期桥接方法，L233–252](https://github.com/Nuos/H3-h3-prompt-journal/blob/35658d3615d02c6aa6e4221fb223d73b86aa6875/case-studies/2026-10-kanzaki-beach-sword-dance-18-segment/methodology.md#L233-L252)

## S04 物理摄影机机位库

- [README.md，L1–61](https://github.com/Nuos/H3-h3-prompt-journal/blob/35658d3615d02c6aa6e4221fb223d73b86aa6875/case-studies/2026-10-physical-camera-position-library/README.md#L1-L61)
- [prompt.md，L1–795](https://github.com/Nuos/H3-h3-prompt-journal/blob/35658d3615d02c6aa6e4221fb223d73b86aa6875/case-studies/2026-10-physical-camera-position-library/prompt.md#L1-L795)
- [八项机位要素，L719–750](https://github.com/Nuos/H3-h3-prompt-journal/blob/35658d3615d02c6aa6e4221fb223d73b86aa6875/case-studies/2026-10-physical-camera-position-library/prompt.md#L719-L750)

## S05 动态运镜纪律库

- [README.md，L1–93](https://github.com/Nuos/H3-h3-prompt-journal/blob/35658d3615d02c6aa6e4221fb223d73b86aa6875/case-studies/2026-10-camera-movement-discipline-library/README.md#L1-L93)
- [prompt.md，L1–234](https://github.com/Nuos/H3-h3-prompt-journal/blob/35658d3615d02c6aa6e4221fb223d73b86aa6875/case-studies/2026-10-camera-movement-discipline-library/prompt.md#L1-L234)
- [提前到位与切点策略，L8–77](https://github.com/Nuos/H3-h3-prompt-journal/blob/35658d3615d02c6aa6e4221fb223d73b86aa6875/case-studies/2026-10-camera-movement-discipline-library/prompt.md#L8-L77)
- [滞后摄影机，L88–125](https://github.com/Nuos/H3-h3-prompt-journal/blob/35658d3615d02c6aa6e4221fb223d73b86aa6875/case-studies/2026-10-camera-movement-discipline-library/prompt.md#L88-L125)
- [同时启动规则，L139–167](https://github.com/Nuos/H3-h3-prompt-journal/blob/35658d3615d02c6aa6e4221fb223d73b86aa6875/case-studies/2026-10-camera-movement-discipline-library/prompt.md#L139-L167)

## S06 高级运镜组合

- [README.md，L1–57](https://github.com/Nuos/H3-h3-prompt-journal/blob/35658d3615d02c6aa6e4221fb223d73b86aa6875/case-studies/2026-10-advanced-camera-combinations/README.md#L1-L57)
- [prompt.md，L1–328](https://github.com/Nuos/H3-h3-prompt-journal/blob/35658d3615d02c6aa6e4221fb223d73b86aa6875/case-studies/2026-10-advanced-camera-combinations/prompt.md#L1-L328)
- [组合十的路径与时间，L277–287](https://github.com/Nuos/H3-h3-prompt-journal/blob/35658d3615d02c6aa6e4221fb223d73b86aa6875/case-studies/2026-10-advanced-camera-combinations/prompt.md#L277-L287)

## S07 舞蹈动作链库

- [README.md，L1–41](https://github.com/Nuos/H3-h3-prompt-journal/blob/35658d3615d02c6aa6e4221fb223d73b86aa6875/case-studies/2026-10-dance-motion-chain-library/README.md#L1-L41)
- [dance-motion-chain-h3.md，L1–2767](https://github.com/Nuos/H3-h3-prompt-journal/blob/35658d3615d02c6aa6e4221fb223d73b86aa6875/case-studies/2026-10-dance-motion-chain-library/dance-motion-chain-h3.md#L1-L2767)
- [动作与验收结构，L17–56](https://github.com/Nuos/H3-h3-prompt-journal/blob/35658d3615d02c6aa6e4221fb223d73b86aa6875/case-studies/2026-10-dance-motion-chain-library/dance-motion-chain-h3.md#L17-L56)
- [C19 至 C25 的标题与分解，L398–436](https://github.com/Nuos/H3-h3-prompt-journal/blob/35658d3615d02c6aa6e4221fb223d73b86aa6875/case-studies/2026-10-dance-motion-chain-library/dance-motion-chain-h3.md#L398-L436)
- [D8 的中英文机制，L619–621](https://github.com/Nuos/H3-h3-prompt-journal/blob/35658d3615d02c6aa6e4221fb223d73b86aa6875/case-studies/2026-10-dance-motion-chain-library/dance-motion-chain-h3.md#L619-L621)
- [K9 至 K16 的拍数与分解，L2295–2344](https://github.com/Nuos/H3-h3-prompt-journal/blob/35658d3615d02c6aa6e4221fb223d73b86aa6875/case-studies/2026-10-dance-motion-chain-library/dance-motion-chain-h3.md#L2295-L2344)

## S08 四人队形编舞

- [README.md，L1–164](https://github.com/Nuos/H3-h3-prompt-journal/blob/35658d3615d02c6aa6e4221fb223d73b86aa6875/case-studies/2026-10-four-subject-formation-choreography/README.md#L1-L164)
- [prompt.md，L1–148](https://github.com/Nuos/H3-h3-prompt-journal/blob/35658d3615d02c6aa6e4221fb223d73b86aa6875/case-studies/2026-10-four-subject-formation-choreography/prompt.md#L1-L148)
- [摄影机与队形时序，L71–86](https://github.com/Nuos/H3-h3-prompt-journal/blob/35658d3615d02c6aa6e4221fb223d73b86aa6875/case-studies/2026-10-four-subject-formation-choreography/prompt.md#L71-L86)

## S09 仅身份半身舞六段

- [README.md，L1–54](https://github.com/Nuos/H3-h3-prompt-journal/blob/35658d3615d02c6aa6e4221fb223d73b86aa6875/case-studies/2026-10-identity-only-half-body-dance-six-segment/README.md#L1-L54)
- [prompt.md，L1–1524](https://github.com/Nuos/H3-h3-prompt-journal/blob/35658d3615d02c6aa6e4221fb223d73b86aa6875/case-studies/2026-10-identity-only-half-body-dance-six-segment/prompt.md#L1-L1524)
- [素材权限与姿态权威，L7–84](https://github.com/Nuos/H3-h3-prompt-journal/blob/35658d3615d02c6aa6e4221fb223d73b86aa6875/case-studies/2026-10-identity-only-half-body-dance-six-segment/prompt.md#L7-L84)
- [动作中匹配剪辑，L157–172](https://github.com/Nuos/H3-h3-prompt-journal/blob/35658d3615d02c6aa6e4221fb223d73b86aa6875/case-studies/2026-10-identity-only-half-body-dance-six-segment/prompt.md#L157-L172)

## S10 白凤蒙尘六段

- [README.md，L1–155](https://github.com/Nuos/H3-h3-prompt-journal/blob/35658d3615d02c6aa6e4221fb223d73b86aa6875/case-studies/2026-10-baifeng-mengchen-classical-dance-six-segment/README.md#L1-L155)
- [prompt.md，L1–475](https://github.com/Nuos/H3-h3-prompt-journal/blob/35658d3615d02c6aa6e4221fb223d73b86aa6875/case-studies/2026-10-baifeng-mengchen-classical-dance-six-segment/prompt.md#L1-L475)
- [第三段的实际开场与末态，L190–232](https://github.com/Nuos/H3-h3-prompt-journal/blob/35658d3615d02c6aa6e4221fb223d73b86aa6875/case-studies/2026-10-baifeng-mengchen-classical-dance-six-segment/prompt.md#L190-L232)
- [段间匹配表，L465–475](https://github.com/Nuos/H3-h3-prompt-journal/blob/35658d3615d02c6aa6e4221fb223d73b86aa6875/case-studies/2026-10-baifeng-mengchen-classical-dance-six-segment/prompt.md#L465-L475)

## S11 下山面纱独舞十二段

- [README.md，L1–71](https://github.com/Nuos/H3-h3-prompt-journal/blob/35658d3615d02c6aa6e4221fb223d73b86aa6875/case-studies/2026-10-xiashan-veiled-solo-twelve-segment/README.md#L1-L71)
- [prompt.md，L1–743](https://github.com/Nuos/H3-h3-prompt-journal/blob/35658d3615d02c6aa6e4221fb223d73b86aa6875/case-studies/2026-10-xiashan-veiled-solo-twelve-segment/prompt.md#L1-L743)
- [参考、音轨与持续层，L20–45](https://github.com/Nuos/H3-h3-prompt-journal/blob/35658d3615d02c6aa6e4221fb223d73b86aa6875/case-studies/2026-10-xiashan-veiled-solo-twelve-segment/prompt.md#L20-L45)
- [故意滞后运镜，L183–187](https://github.com/Nuos/H3-h3-prompt-journal/blob/35658d3615d02c6aa6e4221fb223d73b86aa6875/case-studies/2026-10-xiashan-veiled-solo-twelve-segment/prompt.md#L183-L187)
- [终止状态与摄影机停止，L724–736](https://github.com/Nuos/H3-h3-prompt-journal/blob/35658d3615d02c6aa6e4221fb223d73b86aa6875/case-studies/2026-10-xiashan-veiled-solo-twelve-segment/prompt.md#L724-L736)

## S12 夏日泳池海滩水线 MV

- [README.md，L1–146](https://github.com/Nuos/H3-h3-prompt-journal/blob/35658d3615d02c6aa6e4221fb223d73b86aa6875/case-studies/2026-10-summer-pool-beach-waterline-mv-4-segment/README.md#L1-L146)
- [prompt.md，L1–283](https://github.com/Nuos/H3-h3-prompt-journal/blob/35658d3615d02c6aa6e4221fb223d73b86aa6875/case-studies/2026-10-summer-pool-beach-waterline-mv-4-segment/prompt.md#L1-L283)
- [身份图与首帧边界，L30–44](https://github.com/Nuos/H3-h3-prompt-journal/blob/35658d3615d02c6aa6e4221fb223d73b86aa6875/case-studies/2026-10-summer-pool-beach-waterline-mv-4-segment/README.md#L30-L44)
- [水线段连续三阶段，L248–266](https://github.com/Nuos/H3-h3-prompt-journal/blob/35658d3615d02c6aa6e4221fb223d73b86aa6875/case-studies/2026-10-summer-pool-beach-waterline-mv-4-segment/prompt.md#L248-L266)

## S13 水岸独舞两段

- [README.md，L1–48](https://github.com/Nuos/H3-h3-prompt-journal/blob/35658d3615d02c6aa6e4221fb223d73b86aa6875/case-studies/2026-10-waterfront-solo-dance-two-segment/README.md#L1-L48)
- [prompt.md，L1–119](https://github.com/Nuos/H3-h3-prompt-journal/blob/35658d3615d02c6aa6e4221fb223d73b86aa6875/case-studies/2026-10-waterfront-solo-dance-two-segment/prompt.md#L1-L119)
- [第二段拍点、持续层与静止，L69–95](https://github.com/Nuos/H3-h3-prompt-journal/blob/35658d3615d02c6aa6e4221fb223d73b86aa6875/case-studies/2026-10-waterfront-solo-dance-two-segment/prompt.md#L69-L95)

## S14 抬腿触地换装

- [README.md，L1–58](https://github.com/Nuos/H3-h3-prompt-journal/blob/35658d3615d02c6aa6e4221fb223d73b86aa6875/case-studies/2026-10-leg-lift-contact-cut-stocking-six-look/README.md#L1-L58)
- [prompt.md，L1–759](https://github.com/Nuos/H3-h3-prompt-journal/blob/35658d3615d02c6aa6e4221fb223d73b86aa6875/case-studies/2026-10-leg-lift-contact-cut-stocking-six-look/prompt.md#L1-L759)
- [接触、保持、状态数与声画关系，L21–40](https://github.com/Nuos/H3-h3-prompt-journal/blob/35658d3615d02c6aa6e4221fb223d73b86aa6875/case-studies/2026-10-leg-lift-contact-cut-stocking-six-look/README.md#L21-L40)
- [切换与后续抬腿解耦，L153–219](https://github.com/Nuos/H3-h3-prompt-journal/blob/35658d3615d02c6aa6e4221fb223d73b86aa6875/case-studies/2026-10-leg-lift-contact-cut-stocking-six-look/prompt.md#L153-L219)

## S15 右入三造型展示

- [README.md，L1–52](https://github.com/Nuos/H3-h3-prompt-journal/blob/35658d3615d02c6aa6e4221fb223d73b86aa6875/case-studies/2026-10-sock-showcase-right-entry-three-shot/README.md#L1-L52)
- [prompt.md，L1–98](https://github.com/Nuos/H3-h3-prompt-journal/blob/35658d3615d02c6aa6e4221fb223d73b86aa6875/case-studies/2026-10-sock-showcase-right-entry-three-shot/prompt.md#L1-L98)
- [误判修正、独立状态与装配，L11–44](https://github.com/Nuos/H3-h3-prompt-journal/blob/35658d3615d02c6aa6e4221fb223d73b86aa6875/case-studies/2026-10-sock-showcase-right-entry-three-shot/README.md#L11-L44)

## S16 H3 动作迁移

- [README.md，L1–54](https://github.com/Nuos/H3-h3-prompt-journal/blob/35658d3615d02c6aa6e4221fb223d73b86aa6875/case-studies/2026-10-h3-motion-transfer/README.md#L1-L54)
- [prompt.md，L1–586](https://github.com/Nuos/H3-h3-prompt-journal/blob/35658d3615d02c6aa6e4221fb223d73b86aa6875/case-studies/2026-10-h3-motion-transfer/prompt.md#L1-L586)
- [作者时长上限说明，L10–12](https://github.com/Nuos/H3-h3-prompt-journal/blob/35658d3615d02c6aa6e4221fb223d73b86aa6875/case-studies/2026-10-h3-motion-transfer/prompt.md#L10-L12)
- [运行参数文字说明，L582–586](https://github.com/Nuos/H3-h3-prompt-journal/blob/35658d3615d02c6aa6e4221fb223d73b86aa6875/case-studies/2026-10-h3-motion-transfer/prompt.md#L582-L586)

本项来源是 README 与 prompt 文本，**不表示本轮已经完整阅读或执行其工作流 JSON**。

## S17 MiniMax H3 官方协议

- [官方 README：固定版本能力说明](https://github.com/MiniMax-AI/MiniMax-H3/blob/199b7d0e1fd95e7b3eafa8c15eca692534142427/README.md)
- [官方提示词技能 SKILL.md](https://github.com/MiniMax-AI/MiniMax-H3/blob/199b7d0e1fd95e7b3eafa8c15eca692534142427/skills/h3-prompt-writing/SKILL.md)
- [基础模式指南 base-en.txt](https://github.com/MiniMax-AI/MiniMax-H3/blob/199b7d0e1fd95e7b3eafa8c15eca692534142427/skills/h3-prompt-writing/references/base-en.txt)
- [参考模式指南 ref-en.txt](https://github.com/MiniMax-AI/MiniMax-H3/blob/199b7d0e1fd95e7b3eafa8c15eca692534142427/skills/h3-prompt-writing/references/ref-en.txt)
- [项目保存的官方来源清单与哈希](https://github.com/Nuos/H3-h3-prompt-journal/blob/35658d3615d02c6aa6e4221fb223d73b86aa6875/docs/caseskill/_standards/minimax-h3-source-manifest.json)

## S18 已有案例技能与验证边界

- [完整验证报告](https://github.com/Nuos/H3-h3-prompt-journal/blob/35658d3615d02c6aa6e4221fb223d73b86aa6875/docs/caseskill/_validation/validation-report.md)
- [29 案技能映射](https://github.com/Nuos/H3-h3-prompt-journal/blob/35658d3615d02c6aa6e4221fb223d73b86aa6875/docs/caseskill/catalog.json)
- [已有技能来源清单](https://github.com/Nuos/H3-h3-prompt-journal/blob/35658d3615d02c6aa6e4221fb223d73b86aa6875/docs/caseskill/source-manifest.json)
- [三项实际离线任务记录](https://github.com/Nuos/H3-h3-prompt-journal/blob/35658d3615d02c6aa6e4221fb223d73b86aa6875/docs/caseskill/_validation/forward-runs/README.md)
- [现有规范版本、工程组织与许可说明](https://github.com/Nuos/H3-h3-prompt-journal/blob/35658d3615d02c6aa6e4221fb223d73b86aa6875/docs/caseskill/_standards/README.md)

## S19 Agent Skills 官方标准

- [Agent Skills 格式规范](https://github.com/agentskills/agentskills/blob/83021e2be457a9b6679148719c1f6074f0ad975e/docs/specification.mdx)
- [技能创建最佳实践](https://github.com/agentskills/agentskills/blob/83021e2be457a9b6679148719c1f6074f0ad975e/docs/skill-creation/best-practices.mdx)
- [技能评估指南](https://github.com/agentskills/agentskills/blob/83021e2be457a9b6679148719c1f6074f0ad975e/docs/skill-creation/evaluating-skills.mdx)
- [项目保存的 Agent Skills 来源清单](https://github.com/Nuos/H3-h3-prompt-journal/blob/35658d3615d02c6aa6e4221fb223d73b86aa6875/docs/caseskill/_standards/agentskills-source-manifest.json)
