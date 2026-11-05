# H3 分层参考与帆板写真 MV 高潮编排：方法与修复

## 导航

1. 方法来源与适用范围
2. 条件分支与冲突处理
3. 失败表现与修复
4. 迁移示例
5. 规则证据

## 方法来源与适用范围

把源案例的三层参考架构和文字高潮控制转为可迁移的制作契约，修复“同一定妆图作为三段不同起始状态”、独立片段无状态交接及配乐重制后节拍漂移的问题，并明确哪些结果仍须观看生成视频和量测音频才能判定。

本方法由原案例文本、逐案评估和 H3 官方协议共同整理。原案经验、评估发现与本次补齐的数据/检查接口须分别表述；案例作者的成功报告不等于本次实测。原稿快照保留原貌，冲突由本文件及技能入口裁决。

- 本例默认三段各 15 秒、9:16、约 128 BPM、单一成年角色和帆板浪峰跳跃均为案例方案；迁移时人物、设备、时长、拍号和动作阶段由当前请求确定。
- 首帧来源和逐段 IN/OUT 契约、属性级参考冲突裁决、planned/measured/missing 状态、双时长表、新配乐事件差值与验收容差均为评估驱动的工程补齐，不伪称源文已经实现。
- 源 prompt.md 使用自由标题、REFERENCE ROLES 和 TIMELINE 等区块，本技能将其转译到当前官方三/六字段协议，不能把原文格式直接称为官方协议。
- README.zh-CN.md 第 209 行“小型转面展示”与音乐上下文冲突，以原英文 mini-turnaround、prompt.md 的 musical turnaround 和扩展词表释义为准；角色不因该词必须转身。
- 源文“人物定妆 / 第一帧”与“身份图不控制构图”的表述需限定：真正首帧必含初始构图；仅作为身份参考时不能承诺其像素成为首帧。
- 第三段“纯文字”只指摄影和动作控制，不表示没有图像参考。新增接续帧或更换输入模式属于修复分支，需重新登记实际资产与权限，不能偷偷改变标签含义。
- 源文报告约 128 BPM，但当前没有原始音轨可复核。若只做 128 BPM 的数学规划，15 秒等于 32 拍；这不证明真实音频为恒定精确 128 BPM，也不证明 3 秒是拍点。
- 当前案例目录只有五份文本，没有 README 声称的图片及 result-video.mp4；没有 H3/Suno 运行参数、成片、完整音轨、重制版本或比较实验结果，均不可补造。
- 源落地/落水措辞统一解释为板体回接水面并继续滑行；不引入人物跌水。英雄画面是可读的动态稳定构图，没有把整个海面冻结。
- 本设计只产出提示词、计划与验收方法；素材连续性、设备物理可信度、音乐峰值对齐和第三段撤图的实际效果必须由真实产物检验。

## 条件分支与冲突处理

| 条件 | 执行动作 | 案例/评估依据 |
|---|---|---|
| Picture 1 是棚拍定妆照，而第二、三段要求延续海面高速或浪前状态 | 把它降为身份来源，另写当前 IN 状态；如果必须精确首帧，准备真实接续帧并使用支持该约束的模式。不能既锁棚拍首帧又声明一开始已在大浪前。 | docs/casereview/2026-08-furina-windsurfing-fashion-mv.md:43 |
| 第三段摄影图锁死了与腾空主视觉冲突的视角 | 沿用本案例的移除摄影指导图分支，保留人物/装备参考并用文字安排完整高潮。若当前任务仍需要该图，明确作为新的比较分支处理，记录构图是否服从预期。 | case-studies/2026-08-furina-windsurfing-fashion-mv/prompt.md:123-133,149-185；docs/casereview/2026-08-furina-windsurfing-fashion-mv.md:32,45 |
| 人物大特写与完整板帆同框在英雄窗口发生冲突 | 英雄窗口优先让人物、板、帆及离水间隙可辨，采用足以容纳装备的中景长焦；回水后的写真收尾再收紧肖像。保持长焦的构图目标，不强制相机贴近人物。 | case-studies/2026-08-furina-windsurfing-fashion-mv/prompt.md:941-947,999-1033,1053-1079；case-studies/2026-08-furina-windsurfing-fashion-mv/vocabulary-expanded.zh-CN.md:48（画面优先级为工程补齐） |
| 只有节拍风格要求，没有音轨 | 填写 planned 节拍与叙事窗口，measured_BPM、measured_onsets 和 final_music_version 均保持 missing；生成临时配乐或后期选曲后重新测量。 | case-studies/2026-08-furina-windsurfing-fashion-mv/prompt.md:191-242；docs/casereview/2026-08-furina-windsurfing-fashion-mv.md:33,44（证据状态为工程补齐） |
| Suno 返回轨的高潮或时长与完整视频不同 | 保留原视频动作事件表，为新音乐重新标记事件和偏差；修改音乐安排或经过审查的剪辑，再检验跳跃链与接缝，不能通过冻结空中人物来补齐时长。 | case-studies/2026-08-furina-windsurfing-fashion-mv/prompt.md:1230-1236,1291-1334；docs/casereview/2026-08-furina-windsurfing-fashion-mv.md:44 |
| 用户要迁移到滑雪、滑板或赛车写真 | 迁移分层参考、阶段递进、稳定主视觉和全片音频交接方法；重新定义运动物体、接触点和物理链，不把板/帆/boom 或水面跳跃禁令照搬为其他运动的规范。 | case-studies/2026-08-furina-windsurfing-fashion-mv/prompt.md:1465（跨运动状态重定义为工程补齐） |

## 失败表现与修复

| 失败表现 | 修复步骤 | 依据 |
|---|---|---|
| 三视图被生成成三个人或带箭头的拼贴画面 | 把身份和装备抽象成可复用 Subject，明确多视角图只提供结构、摄影图只提供镜头关系；删除版面复现和箭头继承。 | case-studies/2026-08-furina-windsurfing-fashion-mv/prompt.md:300-311,795-806；case-studies/2026-08-furina-windsurfing-fashion-mv/vocabulary-expanded.zh-CN.md:17-19 |
| 每段回到同一棚拍姿势，下一帧突然瞬移到不同海浪 | 移除不成立的“同一 Picture 1 精确开场”要求，按真实输入模式给出当前开场帧或状态，把前段实际 OUT 作为接缝检查依据。 | docs/casereview/2026-08-furina-windsurfing-fashion-mv.md:43 |
| 第三段仍机械复现前两段摄影图，或删除图后角色和装备也漂移 | 只撤销摄影图权限，保留角色与装备定义；重新写清上浪、离水、稳定主视觉和回水阶段的机位，而非删除所有参考。 | case-studies/2026-08-furina-windsurfing-fashion-mv/prompt.md:137-185,746-806 |
| Hero Shot 变成整幅冻结或悬空数秒，随后凭空跳到水面 | 定义平稳随动与连续下降，保持海浪、发丝和装备运动；重新安排起跳/主视觉/回水时间，逐项检查动作链，不能以冻结填充时长。 | case-studies/2026-08-furina-windsurfing-fashion-mv/prompt.md:999-1051；case-studies/2026-08-furina-windsurfing-fashion-mv/vocabulary-expanded.zh-CN.md:54-56 |
| mini-turnaround 被翻译成让人物转身或装备翻转 | 以原文音乐段落及扩展词表为准，改写为音乐转接，可对应镜头轻微方向变化或预备动作；不沿用 README 中文的“小型转面展示”。 | case-studies/2026-08-furina-windsurfing-fashion-mv/README.zh-CN.md:205-212；case-studies/2026-08-furina-windsurfing-fashion-mv/prompt.md:419-427,949-961；case-studies/2026-08-furina-windsurfing-fashion-mv/vocabulary-expanded.zh-CN.md:73,99 |
| 新配乐一覆盖就宣称全片仍在原 3 秒/9–10 秒精确卡点 | 对新配乐重新测量并登记全局事件，区分三段的局部窗口与整片最终高潮；重新剪辑/安排音乐后复验，未测量时保持待验证。 | case-studies/2026-08-furina-windsurfing-fashion-mv/prompt.md:1230-1236,1291-1334；docs/casereview/2026-08-furina-windsurfing-fashion-mv.md:44 |
| 根据源蓝白外观和缺失图片补造新人物、鞋或索具细节 | 外观与结构全部参数化，从当前真实资产取值；未看见的接头或服装背面写 unknown，文件不存在写 missing，不把源文字当当前图像观察。 | docs/casereview/2026-08-furina-windsurfing-fashion-mv.md:30；case-studies/2026-08-furina-windsurfing-fashion-mv/README.md:98-104 |

## 迁移示例

**任务**

做一支 36 秒原创航海角色 MV，分三段各 12 秒。P1 是成年短黑发女性、白绿运动服的棚拍定妆照；P2 记录同款服装及红色帆板、灰色帆装备；G1/G2 为前两段摄影图。没有音频，计划 120 BPM、4/4，第三段要一次清楚的浪峰跳跃。只做提示词和流程。

**预期处理示例**

以下是规划示例，未运行生成或量测音频。三个 generation_duration 均为 12 秒、24FPS，各 288 帧；编辑时间线暂按 24FPS，S1=[0,12)、S2=[12,24)、S3=[24,36)，总 864 帧。P1 仅作身份来源，不能把棚拍照当三个海面段落的精确首帧。S1 结束保留沿既定 +X 航向高速行进，S2 结束到浪壁基部降低重心并保持双手握 boom，S3 从同一浪前状态开始；这些是 planned 接口，实际前段 OUT 帧及脚位/帆角数值仍为 missing，生成后需核准并回填。S1 使用 G1，S2 使用 G2，S3 不带摄影图。

S3 的六字段示例：
subject_definitions:
<Subject 1> is the adult woman from <Picture 1>, with short black hair and the white-and-green sports outfit whose construction is also shown in <Picture 2>. The studio setting is not transferred.
<Subject 2> is the red windsurf board and gray sail assembly from <Picture 2>, including the mast, boom and visible rigging.
summary:
[reference generation] A 12-second vertical fashion-sports sequence follows <Subject 1> riding <Subject 2> up a wave, completing one controlled jump, returning to the water and continuing into an editorial ending. Character and equipment references are retained; there is no cinematography reference for this segment.
retention_analysis:
<Subject 1>: fully_preserved - identity, short black hair and the referenced outfit remain consistent throughout the shot; the studio pose and background are outside this identity role.
<Subject 2>: fully_preserved - the referenced board, sail, mast, boom and visible rigging remain consistent throughout the shot.
detailed_description:
The target video uses realistic vertical sports photography with a restrained fashion-editorial finish. Telephoto framing keeps the performer readable while making enough room for the board and sail during the jump.
[Shot 1] <Subject 1>, the adult short-haired woman in the white-and-green outfit, rides <Subject 2> toward the base of a steep but surfable wave. The red board points along the established travel direction, and both hands keep their established grips on the boom. The gray sail remains loaded by the wind. Her opening stance, wave position and camera angle follow the planned wave-base approach rather than the studio pose. During the first two seconds, the camera tracks beside her at low water level, with spray passing below the face. Wind and water sounds continue underneath the planned temporary score. From 2 to 4 seconds, she rides diagonally up the wave face while lowering her center of gravity; the camera rises gradually and retains the full equipment silhouette. From 4 to 5.5 seconds, the board approaches the crest and the rider prepares for one clean jump, without changing identity, outfit or rigging. At the planned 5.5-second event, the board leaves the water. A burst of spray marks the departure and then falls back toward the wave. From 5.75 to 6.25 seconds, the camera settles into a stable low-angle following composition. The airborne board, performer and gray sail form one readable diagonal, with a visible gap beneath the board. The planned visual peak is centered at 6 seconds. The camera stops aggressive acceleration, but the rider, wave, spray and clothing keep moving naturally. There is no frozen frame, spin or flip. After this brief hero window, the board descends continuously. At the planned 7-second event, it reconnects with the water, producing a distinct splash as the rider absorbs the contact and maintains control. From 7 to 9 seconds, she continues along the same travel direction; the equipment stays connected and the camera follows smoothly. During the final three seconds, the framing eases into a three-quarter fashion portrait, with the gray sail still visible behind her. No additional jump starts before the segment ends.
overall_soundscape:
Continuous ocean, wind and hull-on-water sounds; a distinct splash accompanies the planned water-contact event. No dialogue.
non_diegetic_music:
A temporary instrumental electronic score is planned at 120 BPM in 4/4, building toward the local 6-second visual peak and easing after water contact. This is a design target; no reference audio or measured beat map is available.

第三段计划事件转换为全局：离水 29.5 秒、第 708 帧；主视觉中心 30 秒、第 720 帧；回水 31 秒、第 744 帧。这里只是 24FPS 时间线计划，不能称为实测卡点。先完成 36 秒完整视频与实际事件表，再提取整轨交接重制；返回音轨的 duration、peak_time 和偏差保持 missing，直到拿到真实文件。若返回峰值偏移，先比较音乐调整和有限剪辑方案，重新检查接缝与跳跃物理连续性，不能让人物悬停补时。

示例是编排示范；其中任务给定参数和演算不代表当前已经读取了对应媒体，也不代表一次 H3 推理已完成。完整生成端交付仍需按输出模板选择正确字段和真实素材绑定。

## 规则证据

以下行号对应本技能来源索引中的固定快照；`review` 指 `source-review.md`。工程补齐项以其所解决的原文/评估缺口为依据，不伪称上游已实现该检查。

| 规则 | 原文或评估位置 |
|---|---|
| FWM01 | case-studies/2026-08-furina-windsurfing-fashion-mv/prompt.md:59-133,292-311；case-studies/2026-08-furina-windsurfing-fashion-mv/vocabulary-expanded.zh-CN.md:17-19（逐属性冲突裁决为工程补齐） |
| FWM02 | case-studies/2026-08-furina-windsurfing-fashion-mv/prompt.md:137-185,746-806,1133-1183；docs/casereview/2026-08-furina-windsurfing-fashion-mv.md:32,45 |
| FWM03 | case-studies/2026-08-furina-windsurfing-fashion-mv/prompt.md:294-298,547-551,789-793,1141；docs/casereview/2026-08-furina-windsurfing-fashion-mv.md:43（IN/OUT 接口为评估驱动的工程补齐） |
| FWM04 | case-studies/2026-08-furina-windsurfing-fashion-mv/prompt.md:263-283,469-471,514-535,575-577,691-715,1071-1083 |
| FWM05 | case-studies/2026-08-furina-windsurfing-fashion-mv/prompt.md:816-846,963-1051,1085-1110；case-studies/2026-08-furina-windsurfing-fashion-mv/prompt.zh-CN.md:708-791,818-833 |
| FWM06 | case-studies/2026-08-furina-windsurfing-fashion-mv/prompt.md:941-947,999-1041；case-studies/2026-08-furina-windsurfing-fashion-mv/vocabulary-expanded.zh-CN.md:48,54-56（可读性优先级为工程补齐） |
| FWM07 | case-studies/2026-08-furina-windsurfing-fashion-mv/prompt.md:191-242,419-427,949-961；case-studies/2026-08-furina-windsurfing-fashion-mv/README.zh-CN.md:205-212；case-studies/2026-08-furina-windsurfing-fashion-mv/vocabulary-expanded.zh-CN.md:65-74,99 |
| FWM08 | case-studies/2026-08-furina-windsurfing-fashion-mv/prompt.md:1187-1287,1291-1334,1441-1465；docs/casereview/2026-08-furina-windsurfing-fashion-mv.md:33,37,44 |
| FWM09 | case-studies/2026-08-furina-windsurfing-fashion-mv/prompt.md:290-490,543-734,785-1129；docs/casereview/2026-08-furina-windsurfing-fashion-mv.md:37,39；官方 H3 格式与能力边界见本技能 references/h3-official.md（协议迁移及生成/编辑分离为工程补齐） |
| FWM10 | case-studies/2026-08-furina-windsurfing-fashion-mv/README.md:14-18,64-72,94-104；docs/casereview/2026-08-furina-windsurfing-fashion-mv.md:29-33,45；case-studies/2026-08-furina-windsurfing-fashion-mv/vocabulary-expanded.zh-CN.md:14,88,107 |

| 规则 | 文件与行号 | 支持内容 |
|---|---|---|
| FWM01 | case-studies/2026-08-furina-windsurfing-fashion-mv/prompt.md：59-133;292-311 | 人物、装备、摄影图各有职责；明确三视图不是分镜、指导箭头不进入画面。 |
| FWM02 | case-studies/2026-08-furina-windsurfing-fashion-mv/prompt.md：137-185;746-806;1133-1141 | 第三段移除摄影指导图但保留人物/装备，且三个片段独立生成。 |
| FWM03 | docs/casereview/2026-08-furina-windsurfing-fashion-mv.md：43 | 评估直接指出同一 Picture 1 与三段不同运动初态的冲突，并要求起始帧来源和连续状态；IN/OUT 表是对应的工程补齐。 |
| FWM04 | case-studies/2026-08-furina-windsurfing-fashion-mv/prompt.md：469-471;514-535;575-577;691-715;1071-1083 | 从高速滑行向大浪递进，第二段保留腾空，最终收尾不再开新动作。 |
| FWM05 | case-studies/2026-08-furina-windsurfing-fashion-mv/prompt.md：816-846;963-1051;1085-1110 | 高潮是一次受控帆板跳跃并回水继续滑行，排除翻转、断裂装备和不合物理的浪墙。 |
| FWM06 | case-studies/2026-08-furina-windsurfing-fashion-mv/vocabulary-expanded.zh-CN.md：48;54-56 | 长焦与物理拍摄距离、短暂腾空与悬浮、稳定摄影与冻结画面的关键区别。 |
| FWM06 | case-studies/2026-08-furina-windsurfing-fashion-mv/prompt.md：941-947;999-1041 | 源主视觉要求人物、帆、板同框可读，同时后续下降自然连续。 |
| FWM07 | case-studies/2026-08-furina-windsurfing-fashion-mv/README.zh-CN.md：205-212 | 中文表把音乐 mini-turnaround 误译成转面展示；结合原英文正文及扩展词表修正，不能直接继承该译法。 |
| FWM07 | case-studies/2026-08-furina-windsurfing-fashion-mv/vocabulary-expanded.zh-CN.md：65-74;99 | 音乐语汇的语义边界，明确 mini-turnaround 为音乐转接而非角色转身。 |
| FWM08 | case-studies/2026-08-furina-windsurfing-fashion-mv/prompt.md：1187-1287;1291-1334 | 先合完整视频、提完整音频、外部重制、放回并最终调节音画同步。 |
| FWM08 | docs/casereview/2026-08-furina-windsurfing-fashion-mv.md：33;37;44 | 重制不保证长度与节拍点，需要记录输入/输出版本并重新建立对位表。 |
| FWM09 | docs/casereview/2026-08-furina-windsurfing-fashion-mv.md：37-39 | 评估要求把三段提示、状态交接、剪辑/音轨任务及最小验收标准转为可复用接口；官方字段与生成能力由共同 H3 文档约束，不能归因于原案例的自由格式正文。 |
| FWM10 | docs/casereview/2026-08-furina-windsurfing-fashion-mv.md：29-33;45 | 源经验缺系统输入表、重制前后事件表和重复对照；等权说法不能当模型内部机制。 |
| FWM10 | case-studies/2026-08-furina-windsurfing-fashion-mv/README.md：98-104 | 源文字宣称的角色图、装备图、两段摄影参考图及结果视频，在当前可读目录中不存在，不能据文字链结当作已验证媒体。 |
