# 帆板写真音乐短片：词汇精读增补

v1.1.0 · 2026-09-28。对应 [案例原文](./README.md)、[案例译文](./README.zh-CN.md)、[完整制作提示词](./prompt.md)、[提示词译文](./prompt.zh-CN.md)。源基线 `73f9aa2c7e55f222b06f8547e5e108c56e6a2287`。本文件按原文章节扩充 50 项词汇，保留原文本与原翻译。

IPA 采用常见美式宽式读音；`n.` 名词，`v.` 动词，`adj.` 形容词，`adv.` 副词，`phr.` 短语。人名、作品名和产品名不在缺少依据时另编读音。

## 一、Layer 1 / Reference：把“分层参考”拆开理解

| 编号 | 词汇、IPA、词性 | 基本义 → 本文义、搭配与辨析 |
|---|---|---|
| 01 | layered /ˈleɪərd/ adj. | 分层的。`layered reference architecture` 指职责层次，不是把三幅参考图作为半透明图层叠在视频里。 |
| 02 | architecture /ˈɑːrkɪtektʃər/ n. | 架构、组织方式。这里是参考信息的分工结构，不取教堂案例中的建筑空间义。 |
| 03 | segregated /ˈseɡrɪɡeɪtɪd/ adj.; v. pp. | 分隔开的。`role-segregated` 指把参考职责分开，避免人物图、装备图与机位图互相越权。 |
| 04 | equal-weight /ˌiːkwəl ˈweɪt/ adj. | 等权的。作者用它概括模型对输入参考的处理倾向；不是已经读取到的模型权重参数。 |
| 05 | compromise /ˈkɑːmprəmaɪz/ n.; v. | 折中、妥协；损害。原文用它批评多种参考互相牵制而造成的折中结果，不能只译成“合作”。 |
| 06 | simultaneously /ˌsaɪməlˈteɪniəsli/ adv. | 同时地。指模型试图一并复现各图不同目标，可能把角色表布局也当成输出构图。 |
| 07 | turnaround /ˈtɜːrnəraʊnd/ n. | 此处为角色多视图/转面参考，呈现正侧背等视角；不是要求最终视频出现一圈人物自转。后文音乐语境另有不同含义。 |
| 08 | storyboard /ˈstɔːribɔːrd/ n. | 分镜图、按镜头组织的画面计划。`not a storyboard` 说明装备参考不规定镜头顺序。 |
| 09 | layout /ˈleɪaʊt/ n. | 版面布局。`turnaround-sheet layout` 是多视图在参考表上的排列，不应复制成多个同一人物并排出现在影片中。 |
| 10 | scope /skoʊp/ n. | 范围、职责边界。虽是概括性学习词，但直接对应各图 Controls / Does NOT control 的划分：必须同时理解允许与不允许提供的信息。 |

**原句回读：** `Picture 2 is not a storyboard. Do not reproduce the turnaround-sheet layout.`
**译文：** 图片 2 不是分镜图；不要复现角色多视图参考表的排版。保留的是人物与装备结构，不是表格布局。

## 二、CHARACTER AND WINDSURFING EQUIPMENT REFERENCE

| 编号 | 词汇、IPA、词性 | 基本义 → 本文义、搭配与辨析 |
|---|---|---|
| 11 | windsurfing /ˈwɪndsɜːrfɪŋ/ n. | 帆板运动。人物站在带帆的板上借风运动，不能只按普通冲浪、桨板或风筝冲浪理解装备。 |
| 12 | equipment /ɪˈkwɪpmənt/ n. | 装备的总称，通常不可数。本文包括板、帆、桅杆、帆杆与索具，不应逐项随意增删。 |
| 13 | board /bɔːrd/ n. | 板体。`windsurf board` 指承载人物的帆板，不是分镜板 storyboard，也不是抽象组织“董事会”。 |
| 14 | sail /seɪl/ n. | 帆。承受风力并形成主要视觉斜线；不是衣服飘带。`transparent sail` 限定材料外观，不能因此丢失帆面结构。 |
| 15 | mast /mæst/ n. | 桅杆，支撑帆的主要杆件。与人物手握的 boom 区分，不能互换位置。 |
| 16 | boom /buːm/ n. | 此处是帆板上供操控握持的帆杆/帆把结构；不是爆炸声、吊杆摄影机或经济繁荣。必须由 windsurfing equipment 确定义项。 |
| 17 | rigging /ˈrɪɡɪŋ/ n. | 索具、连接和控制帆装的装具系统。不能照搬成角色骨骼绑定 rig，也不应凭空添加参考中没有的绳索布局。 |
| 18 | footwear /ˈfʊtwer/ n. | 鞋类、足部穿着。装备图也负责鞋，不能因进入水上运动就自动改成赤脚。 |
| 19 | translucent /trænzˈluːsənt/ adj. | 半透明的，透光但不完全清晰透视。修饰飘动布料；区别于 transparent 的清晰透明。 |
| 20 | ornamental /ˌɔːrnəˈmentəl/ adj. | 装饰性的。`gold ornamental details` 指既有服装饰件，不是新增魔法粒子或悬浮装饰。 |

**原句回读：** `preserve ... windsurf board, mast, boom, transparent blue sail and rigging`。
**译文：** 保留帆板、桅杆、帆杆、透明蓝色帆面以及索具等装备结构。这里几个名词是不同部件，不应统统笼统译成“帆”。

## 三、TIMELINE / CINEMATOGRAPHY：方向、跟拍和腾空

| 编号 | 词汇、IPA、词性 | 基本义 → 本文义、搭配与辨析 |
|---|---|---|
| 21 | predominantly /prɪˈdɑːmənəntli/ adv. | 主要地、以……为主。`predominantly close and medium` 给景别主次，不是禁止所有短暂需要的构图变化。 |
| 22 | telephoto /ˈteləfoʊtoʊ/ n.; adj. | 长焦镜头；长焦的。取景与视角效果需结合摄影距离理解，不能把“长焦”直接等同“相机贴脸”。 |
| 23 | tracking /ˈtrækɪŋ/ n.; adj. | 跟拍、跟踪移动。相机随主体行进保持关系，不是后期人脸追踪软件的专有功能。 |
| 24 | alongside /əˌlɔːŋˈsaɪd/ prep.; adv. | 在旁边、并行地。这里限定侧面跟拍关系，不是相机追在人物后方。因决定机位而保留释义。 |
| 25 | parallel /ˈpærəlel/ adj.; adv. | 平行的、平行地。`moves parallel to the board` 指相机运动方向与板体行进相协调，不代表相机镜头一定朝正前方。 |
| 26 | spray /spreɪ/ n.; v. | 飞散细水花；喷溅。帆板切水与运动形成的水花，区别于整个人撞入水面的较大 splash。 |
| 27 | diagonal /daɪˈæɡənəl/ adj.; n. | 对角的；斜线。帆面与身体构成画面斜线，不是要求海平线永久倾斜。 |
| 28 | airborne /ˈerbɔːrn/ adj. | 腾空、离开支撑面的。说的是人物和装备短时离水，不是悬浮不落或物件失去重量。 |
| 29 | takeoff /ˈteɪkɔːf/ n. | 起跳、离开水面的阶段。必须承接冲上浪壁，区别于已经在空中的 airborne 状态。 |
| 30 | stabilize /ˈsteɪbəlaɪz/ v. | 稳定下来。高潮 Hero frame 中主要让相机停稳，以便看清动作；不等于让海浪、头发和人物全都冻结。 |

**原句回读：** `The camera moves backward while the subject advances.`
**译文：** 相机向后移动，同时主体继续向前行进。`while` 强调两种运动并行，不是先后次序。

## 四、MUSIC STRUCTURE：不要把所有音乐节点都叫“高潮”

| 编号 | 词汇、IPA、词性 | 基本义 → 本文义、搭配与辨析 |
|---|---|---|
| 31 | chiptune /ˈtʃɪptuːn/ n. | 芯片音色风格音乐。这里是电子音乐风格标签，不代表必须调用特定游戏机硬件。 |
| 32 | synthpop /ˈsɪnθpɑːp/ n. | 合成器流行音乐。synth 为 synthesizer 的简称；与 chiptune 可有交集但不是同义词。 |
| 33 | syncopation /ˌsɪŋkəˈpeɪʃən/ n. | 切分节奏，把重音安排在通常的弱位或拍间等位置；不等于音画不同步。 |
| 34 | four-on-the-floor /ˌfɔːr ɑːn ðə ˈflɔːr/ n. phr. | 四拍节奏中底鼓均匀落在每一拍上的常见型态。是鼓点组织，不是四个人在地板跳舞。 |
| 35 | kick /kɪk/ n. | 此处为底鼓声。若出现在身体动作中才可能是踢腿；音乐词表里不能照字面添加踢腿镜头。 |
| 36 | snare /sner/ n. | 军鼓、小鼓声部。与低音 kick、踩镲 hi-hat 区分，决定不同重音与高频层次。 |
| 37 | build-up /ˈbɪldʌp/ n. | 逐渐累积张力的铺垫段。不是技术“构建项目”，也不必整个段落都加速。 |
| 38 | drop /drɑːp/ n. | 电子音乐中张力释放、主要节奏进入的节点/段落。`main drop` 不是人物落水或镜头掉下去。 |
| 39 | turnaround /ˈtɜːrnəraʊnd/ n. | 本文音乐语境中的短转接、转折。`mini-turnaround` 与前面的角色多视图同词异义，不能都译成“人物转面”。 |
| 40 | release /rɪˈliːs/ n.; v. | 释放、张力缓和。这里是音乐/视觉能量松开的段落，不是必须松手放掉装备。 |

**原句回读：** `music's accent decides the action; music's release decides the camera ease`。
**译文：** 音乐重音决定动作落点，音乐张力的释放决定镜头何时缓和。两半句分别规定“击中”和“松开”。

## 五、Text-driven climax / H3 + Suno split：移除参考与后期合成

| 编号 | 词汇、IPA、词性 | 基本义 → 本文义、搭配与辨析 |
|---|---|---|
| 41 | climax /ˈklaɪmæks/ n. | 高潮、能量发展的顶点。本文为巨浪腾空与音乐峰值相接，不是每个 15 秒片段都同等猛烈。 |
| 42 | constrain /kənˈstreɪn/ v. | 约束、限制。`over-constrain the camera` 是构图参考限制过多，使动态高潮无法自由实现。 |
| 43 | dismiss /dɪsˈmɪs/ v. | 解雇、让离开。作者把参考图拟人化为员工，意指不再把 Picture 3 作为最后一段输入，不是删除项目原图。 |
| 44 | sole /soʊl/ adj. | 唯一的。`text is the sole director` 指文字成为机位与高潮控制来源；人物与装备仍由 Picture 1、2 参考。 |
| 45 | extract /ɪkˈstrækt/ v. | 提取。`extract full audio` 从完整视频中取出整条声音轨，与逐段重新作曲不同。 |
| 46 | remix /ˌriːˈmɪks/ v.; /ˈriːmɪks/ n. | 重新混制、重做编排；重混版本。本文描述把完整音频交给音乐工具重制，不能假设输出时长与拍点会自动完全不变。 |
| 47 | coherent /koʊˈhɪrənt/ adj. | 连贯统一的。`coherent musical arc` 指整曲有共同发展结构，不是三个互不相关短音轨相接。 |
| 48 | fragment /ˈfræɡmənt/ n. | 片段、碎片。`disconnected fragments` 批评缺少整体音乐上下文，不是说视频分段生成本身错误。 |
| 49 | sync /sɪŋk/ n.; v. | 同步、对齐。`final sync edit` 是最终音画对齐处理；不能漏译成单纯把音乐放回视频。 |
| 50 | post-production /ˌpoʊst prəˈdʌkʃən/ n. | 后期制作。本文包括合段、提取音频、重制配乐、放回音乐、再次校齐，区别于生成每段画面的阶段。 |

**原句回读：** `generate all video first, then remix the complete audio`。
**译文：** 先生成所有视频片段，再重制完整音频。`first / then` 规定制作顺序，不能颠倒成每生成一段就独立定稿一首配乐。

## 六、同词异义回查

**turnaround：** Character turnaround＝人物多视图参考；musical turnaround＝音乐转接。本文第 07、39 项是有意分义，不是重复凑词条。

**boom：** 本文是帆板操控杆件；其他影视文本中还可能指吊杆。要先定位 equipment 段，再决定译名。

**drop / release / peak：** drop 是节奏进入与张力落下的事件；release 是放松或释放阶段；peak 是强度顶点。它们可以靠近，但不应全部压成“高潮”。

## 校读边界

删去第三段 Picture 3，表示不给该段输入摄影指导图，不表示系统自动记住前段画面。关于分段生成、音乐重制效果的结论属于案例作者经验；本词表不把它们当作未经测试的接口保证。镜头“压缩感”还依赖拍摄距离及构图，不能仅由 telephoto 一词推出完整透视关系。
