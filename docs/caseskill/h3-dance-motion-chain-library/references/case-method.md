# 舞蹈动链检索、时间容量与状态衔接编排：方法与修复

## 导航

1. 方法来源与适用范围
2. 条件分支与冲突处理
3. 失败表现与修复
4. 迁移示例
5. 规则证据

## 方法来源与适用范围

从庞大知识库提取本任务真正需要的动作链，在时间容量、身体与道具状态、音乐、摄影和参考权限之间建立可审查的连接；让正文说明动作如何开始、达到主结果、制动并接入下一链，而非罗列动作名。

本方法由原案例文本、逐案评估和 H3 官方协议共同整理。原案经验、评估发现与本次补齐的数据/检查接口须分别表述；案例作者的成功报告不等于本次实测。原稿快照保留原貌，冲突由本文件及技能入口裁决。

- 正文是Rev.1.4只读镜像，固定本次repo提交；不引用外部动作库／video-to-h3-prompt当前实现为已验证依赖，也不改写原始镜像。
- 全部2767行正文已完整阅读；原媒体、八份反推报告、统一参数和批量生成记录未附于本案，作者的实测、实现度等级和星级仅按source-reported保存。
- 新增工程schema、模式标签、双层旋转计数、片型路由、已测／推测／计划／missing状态与逐窗验收表不是Agent Skills或MiniMax官方规定。
- 元数据缺口不限于review：C25标题7拍但分解到8；C35题称五圈/8.5拍、分解约4–5圈且只到拍5、H3写Four；D8英文聚散与中文灯起起身不同；D18标题8+8拍但写再下8拍，D20标题8×2拍但只分解到8；K9题6拍但分解到8，K16题2拍分解到3；遇到这些ID必须先裁决。
- H01 15.1秒、H07 28.1秒、J6 16.1秒、J7 16.6秒、J8 15.5秒及J9 2.7秒不能按标准H3单次4–15秒直接执行；原片长保留，目标生成／编辑方案另行定义。
- J母规则换pose必须换机位、尾镜必须推脸与J3固定桌面/J8固定自拍等范本互有例外；按实际片型取规则，不让母模板抹平有证据的固定机位变体。
- K23/K24标大姿势锁死却包含抬膝、转正和抱膝，选用时应拆pose跳切或允许完整身体转换；未知过程继续标推测。
- 源码个别H3句把头发颜色、房间、衣物、器具混入动作；迁移阶段只保留当前资产支持的功能和物理，不会因选链而增加新身份／环境。
- 旋转≤2次、Hero2–4处／70%进度、四人／2×2、禁俯拍等均为案例经验或局部风格，须有作用域；相对拍也不是原视频自动等速的证据。
- 此技能负责提示词编排与审校，scripts/audit_plan.py只能检查计划结构与约束；无法仅由JSON证明动作物理完成、真实声画同步或H3生成成功。

## 条件分支与冲突处理

| 条件 | 执行动作 | 案例/评估依据 |
|---|---|---|
| 要求0.5秒完成720°转体、地板滚转、起身和镜头环绕 | 判窗口超载，保留一个可完成短accent或为完整Hero重新分配较长窗口；若720°保留，写一次连续双周、轴心、定点方向、减速和回收，不用多次无终点打转替代。 | case-studies/2026-10-dance-motion-chain-library/dance-motion-chain-h3.md:42-56 |
| 取C19或C25，按标题7拍却需要逐拍分解所有动作 | 记录title_beats=7、decomposition_beats=8，默认以8拍完整分解建立目标工程卡并标修正；若只能7拍，删减／合并动作重新命名variant，不伪称原链完整未改。 | case-studies/2026-10-dance-motion-chain-library/dance-motion-chain-h3.md:398-402,434-438 |
| 取C35要求精确五圈、8.5拍 | 先显示标题5、分解4–5、英文4及分解只到拍5的冲突；选定目标圈数和完整时窗后重建预载／旋转／回收；未知源事实仍保留conflict，不能靠标题声称可控五圈。 | case-studies/2026-10-dance-motion-chain-library/dance-motion-chain-h3.md:494-498 |
| 要醉酒式摄影又要求每个onset都与身体同一帧到位 | 解释两种响应模式互斥；按请求主目标选择delayed_observer并明确延迟，或sync_follow并删除迟反应。Hero可另窗转稳定，但要写模式边界。 | case-studies/2026-10-dance-motion-chain-library/dance-motion-chain-h3.md:23-30,777-817 |
| 将J写真pose快切接入连续舞蹈，或要转身中换场 | pose_jump_cut允许新姿势已就位，连续舞需状态桥接；旋转中换场选择phase_match_cut并匹配方向／速度／肩相位。不能同时要求不跨切动作和同一动作跨切持续。 | case-studies/2026-10-dance-motion-chain-library/dance-motion-chain-h3.md:716-721,750-763,1940-1975 |
| 只有K23/24六格图或K25单帧，要还原实测BPM与完整进入动作 | 给inferred时间设计，明确没有真实时序／音轨；K23/24所谓大姿势锁死却抬膝、抱膝，应拆成pose跳切或明确允许的身体变换，不能保留绝对锁姿标签。 | case-studies/2026-10-dance-motion-chain-library/dance-motion-chain-h3.md:2389-2412 |
| 要求原样运行H07 28.1秒或J9 2.7秒范本 | H07按乐句和源切点拆成4–15秒生成段并记录接续；J9先生成≥4秒，再登记2.7秒编辑选窗。保留源时长作为记录，不能未经verified-custom证据当作标准模型能力。 | case-studies/2026-10-dance-motion-chain-library/dance-motion-chain-h3.md:1025-1035,2174-2192；工程补齐：生成／编辑分离 |
| 用户只给两人，选D或K五人组链 | 按真实人数重编任务角色与接触点，删除不存在的成员或改用双人链；源四人、六人、五人仅作各条适用条件，不复制exactly four。 | case-studies/2026-10-dance-motion-chain-library/dance-motion-chain-h3.md:589,672-680,2508-2535,2579-2582 |
| 取J7九镜原样复刻 | 说明现有时间表只有8镜；以表输出8镜7硬切并显式记录修正，或另增第9镜作为用户改编方案，不凭空补源内容。 | case-studies/2026-10-dance-motion-chain-library/dance-motion-chain-h3.md:2112-2136 |

## 失败表现与修复

| 失败表现 | 修复步骤 | 依据 |
|---|---|---|
| 手臂反复交叉、原地晃动，没有明确动作完成 | 削减独立手势，只保留一条从支撑到主结果再回收的舞句；明确交叉方向、切开时点和最终手位，给下一链可用出态。 | case-studies/2026-10-dance-motion-chain-library/dance-motion-chain-h3.md:43-56 |
| 720°只转一点或连续不停转 | 明确一次episode、2周、支撑轴、进入预载、结束方向和制动；重新分配时间或减少邻近动作，不增加形容词。 | case-studies/2026-10-dance-motion-chain-library/dance-motion-chain-h3.md:44-55 |
| 每条都有动作名却在边界突然换脚、换面向或道具换手 | 对照前OUT与后IN，在可用窗内加入重心／手位桥接或换链；状态卡必须包含握持与动量，不能仅比对站立／坐姿文字。 | case-studies/2026-10-dance-motion-chain-library/dance-motion-chain-h3.md:18,22,45,2760 |
| 摄影落后被当错误修成零延迟，但用户本来要醉酒观察者 | 检查所选camera_response；有意滞后保留并量化，无意拖后才对齐启动／峰值／回收。 | case-studies/2026-10-dance-motion-chain-library/dance-motion-chain-h3.md:23-30,777-817 |
| H3正文照抄K章带入陌生房间、发色、道具或新人物 | 拆离源档案与动作机制，按当前Picture／Subject映射保留材料功能；缺物件标missing或改链，保持源观察与目标指令两栏。 | case-studies/2026-10-dance-motion-chain-library/dance-motion-chain-h3.md:2227-2241,2508-2535；docs/casereview/2026-10-dance-motion-chain-library.md:46 |
| 写真锁姿仍要求膝弹不停，或姿态跳切被补成一段多余走位 | 按片型停用不兼容持续层，明确哪些部位锁定哪些微动；pose_jump_cut首帧新pose已就位，不添加未经要求的连续桥接。 | case-studies/2026-10-dance-motion-chain-library/dance-motion-chain-h3.md:17,1934-1975,2393-2403 |
| 标题拍数、相对拍和源秒数直接混算，时间表超过目标 | 对选链元数据逐条核对，把源自由散板的拍理解为分析分段，重新给目标beats或秒窗；H/J长短范本按官方范围分段／裁窗。 | case-studies/2026-10-dance-motion-chain-library/dance-motion-chain-h3.md:398-450,494-498,1025-1035,2174-2192,2223-2230 |
| 多人都被写成四人齐舞，承重同伴也移动导致接触断裂 | 使用任务实际人数与稳定ID，分别规定基座／被支撑者、固定接触点和转换窗口；局部齐舞、卡农、solo规则按目标选择。 | case-studies/2026-10-dance-motion-chain-library/dance-motion-chain-h3.md:589-680,2232-2242,2508-2535 |

## 迁移示例

**任务**

一个成年舞者，Picture1为正面站立、双臂在体侧；10秒、24FPS。新配乐计划120 BPM，先A18拳托腮镜像再A19下蹲起身雨刷手，动作要连得上，镜头跟随高低变化，无切镜。不需要大旋转。

**预期处理示例**

路由continuous_dance、I2VA首帧锚定、continuous剪辑，camera_response按窗选static_observe或sync_follow。音轨missing；120 BPM是创作计划，beat=0.5秒，20拍=10秒=240帧。0–4秒保留A18的8拍：0–1秒右拳收下颌、肘外抬，重心落左足且右脚尖点地；1–2秒右倾头保持；2–3秒镜像左手；3–4秒双拳同托下颌、双脚并拢、面向镜头，终态明确为A19入口。4–10秒把原A19的8拍扩为12拍，记为工程重定时A19@12：4–5秒双膝屈曲下沉，手从下颌收至胸前猫爪；5–6秒低位两次小前挠；6–7秒通过足底伸膝起身并向左上扫臂；7–8秒向右上扫臂；8–9秒一次头顶环臂再收胸；9–10秒直立、双手回脸侧，9.5秒后只保留呼吸和发丝衰减。A18→A19无需重置，持续膝弹在定格和深蹲稳定阶段让位给主链。相机0–4秒固定胸高全身，4–5秒随身体降低，5–6秒保持，6–7秒同步回升，7–10秒固定；所有起止都在同一时轴，没有动作结束后补推。旋转episode=0、总周数=0。实际配乐重音、蹲底支撑、9秒回收和最终姿态须生成后检查；未运行时只标计划通过。

示例是编排示范；其中任务给定参数和演算不代表当前已经读取了对应媒体，也不代表一次 H3 推理已完成。完整生成端交付仍需按输出模板选择正确字段和真实素材绑定。

## 规则证据

以下行号对应本技能来源索引中的固定快照；`review` 指 `source-review.md`。工程补齐项以其所解决的原文/评估缺口为依据，不伪称上游已实现该检查。

| 规则 | 原文或评估位置 |
|---|---|
| R1 | case-studies/2026-10-dance-motion-chain-library/dance-motion-chain-h3.md:1-13,914-933,1934-1951,2221-2225,2756-2764；docs/casereview/2026-10-dance-motion-chain-library.md:5,23,37 |
| R2 | case-studies/2026-10-dance-motion-chain-library/dance-motion-chain-h3.md:206-246,398-402,434-450,494-498,619-621,2112-2136；docs/casereview/2026-10-dance-motion-chain-library.md:31,45 |
| R3 | case-studies/2026-10-dance-motion-chain-library/dance-motion-chain-h3.md:42-56；工程补齐：容量启发与硬约束区分 |
| R4 | case-studies/2026-10-dance-motion-chain-library/dance-motion-chain-h3.md:17-22,31-41,2758-2761；工程补齐：层间互斥与状态字段 |
| R5 | case-studies/2026-10-dance-motion-chain-library/dance-motion-chain-h3.md:23-30,686-698,777-817；docs/casereview/2026-10-dance-motion-chain-library.md:43 |
| R6 | case-studies/2026-10-dance-motion-chain-library/dance-motion-chain-h3.md:716-721,750-763,919-933,1953-1975,2393-2412；docs/casereview/2026-10-dance-motion-chain-library.md:44 |
| R7 | case-studies/2026-10-dance-motion-chain-library/dance-motion-chain-h3.md:20-22,494-498,861-910,2764；工程补齐：双层旋转计数 |
| R8 | case-studies/2026-10-dance-motion-chain-library/dance-motion-chain-h3.md:2223-2241,2278-2282,2393-2412；docs/casereview/2026-10-dance-motion-chain-library.md:32,46 |
| R9 | case-studies/2026-10-dance-motion-chain-library/dance-motion-chain-h3.md:924-928,935-945,1025-1035,2142-2192,2227-2230；工程补齐：官方24FPS／4–15秒与编辑裁窗 |
| R10 | case-studies/2026-10-dance-motion-chain-library/dance-motion-chain-h3.md:55,589-680,2508-2535,2579-2582；docs/casereview/2026-10-dance-motion-chain-library.md:32,39 |

| 规则 | 文件与行号 | 支持内容 |
|---|---|---|
| R1 | case-studies/2026-10-dance-motion-chain-library/dance-motion-chain-h3.md：1-13;914-933;1934-1951;2221-2225;2756-2764 | Rev.1.4及各模块用途、片型与来源范围。 |
| R2 | case-studies/2026-10-dance-motion-chain-library/dance-motion-chain-h3.md：206-246;398-402;434-450;494-498;619-621;2112-2136 | B短句缺字段、C19/C25拍数、C27的19拍、C35圈数、D8两种不同链、J7镜数的实际冲突。 |
| R3 | case-studies/2026-10-dance-motion-chain-library/dance-motion-chain-h3.md：42-56 | 容量先行、完整动力与四种失败诊断、逐窗十项检查。 |
| R4 | case-studies/2026-10-dance-motion-chain-library/dance-motion-chain-h3.md：17-22;45;2758-2761 | 三层结构、OUT/IN与动力进入／回收的来源；兼容性字段为工程补齐。 |
| R5 | case-studies/2026-10-dance-motion-chain-library/dance-motion-chain-h3.md：23-30;686-698;777-817 | 同步总则与提前画框到位／醉酒滞后三类不能无条件合取。 |
| R6 | case-studies/2026-10-dance-motion-chain-library/dance-motion-chain-h3.md：716-721;750-763;919-933;1953-1975;2393-2412 | 完成处切、旋转相位切、首帧继承、pose跳切与单图推测分属不同语法。 |
| R7 | case-studies/2026-10-dance-motion-chain-library/dance-motion-chain-h3.md：20-22;494-498;861-910;2764 | 旋转预算与多圈Hero并存，源经验实现度并无批量验证记录。 |
| R8 | case-studies/2026-10-dance-motion-chain-library/dance-motion-chain-h3.md：2223-2241;2278-2282;2393-2412 | 源档案带外观／物件；回收未入镜、单图时序明确推测。 |
| R9 | case-studies/2026-10-dance-motion-chain-library/dance-motion-chain-h3.md：924-928;935-945;1025-1035;2142-2192;2227-2230 | 声音三模式、过长过短范本、响度与自由散板推测；官方能力对照属于共同规范补充。 |
| R10 | case-studies/2026-10-dance-motion-chain-library/dance-motion-chain-h3.md：55;589-680;2508-2535;2579-2582 | 逐窗验证及四人／六人／双人／五人各自不同的案例边界。 |
