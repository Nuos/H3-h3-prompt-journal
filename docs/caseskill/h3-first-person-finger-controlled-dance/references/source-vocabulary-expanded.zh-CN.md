# 第一人称手势控舞：词汇精读增补

v1.1.0 · 2026-09-28。对应 [案例原文](./README.md)、[案例译文](./README.zh-CN.md)、[提示词原文](./prompt.md)、[提示词译文](./prompt.zh-CN.md)。原文基线 `73f9aa2c7e55f222b06f8547e5e108c56e6a2287`。本文件保留已有译文，按段落功能扩充 50 项词汇；不改变手势顺序、画幅、距离和面积要求。

IPA 使用常见美式宽式读音。`n.` 名词；`v.` 动词；`adj.` 形容词；`adv.` 副词；`phr.` 短语。短语中的常用词只在影响技术含义时解释。

## 一、What this prompt solves：关系比单独描述更重要

| 编号 | 词汇、音标、词性 | 基本义 → 本文义、搭配与辨析 |
|---|---|---|
| 01 | prior /ˈpraɪər/ n. | 先验、预先形成的倾向。作者用 `model's prior` 解释模型常见生成方向，不是“之前那条提示词”。 |
| 02 | freelance /ˈfriːlæns/ v. | 自由接活；这里比喻自行发挥。`the dancer freelances` 指模型脱离外部手势安排动作，不是在讲舞者职业身份。 |
| 03 | improvise /ˈɪmprəvaɪz/ v. | 即兴创作。文中批评与控制目标无关的即兴编舞；不是说所有舞蹈场景都应禁止即兴。 |
| 04 | cue /kjuː/ n. | 提示信号、启动线索。`movement cue` 是手势对动作的触发，区别于舞者从背景音乐自行选择动作。 |
| 05 | puppeteer /ˌpʌpɪˈtɪr/ n. | 操纵木偶的人。这里比喻前景手的控制角色，不要求出现木偶线、木偶形态或额外人物。 |
| 06 | drift /drɪft/ v.; n. | 逐渐偏离、漂移。`drift out of sync` 是同步关系随时间丢失；与摄影机物理漂动要按语境区分。 |
| 07 | mapping /ˈmæpɪŋ/ n. | 映射、对应规则。这里手指方向对应身体方向，不是地图绘制，也不是把两幅图叠在一起。 |
| 08 | one-to-one /ˌwʌn tə ˈwʌn/ adj. | 一一对应的。每条方向命令对应一个明确身体响应；不是笼统“手在动、身体也在动”。 |
| 09 | literal /ˈlɪtərəl/ adj. | 按字面直接对应的。`literal mapping` 要求向左就身体向左，不许可把 LEFT 隐喻成“俏皮一点”。 |
| 10 | forbid /fərˈbɪd/ v. | 明确禁止。`forbid alternatives` 禁止会削弱对应关系的替代解释，而不取消保持自然人体运动的要求。 |

**原句回读：** `The hand is the visible movement cue and the woman's body immediately follows it.`
**译文：** 手是可见的动作提示信号，人物身体立即跟随这一信号。这里的 `it` 回指动作提示，而不是要求身体贴着手移动。

## 二、integrated_multimodal_description：视角与画面分配

| 编号 | 词汇、音标、词性 | 基本义 → 本文义、搭配与辨析 |
|---|---|---|
| 11 | integrated /ˈɪntəɡreɪtɪd/ adj. | 整合的。字段名说明把参考、视角、人物和手的关系一起描述，不是单独的视频特效。 |
| 12 | multimodal /ˌmʌltiˈmoʊdəl/ adj. | 多模态的，涉及多种信息形式。这里是结构化描述的字段名；不能仅凭名称推断具体模型接口能力。 |
| 13 | perspective /pərˈspektɪv/ n. | 观察视角、透视。这里要求保留参考图的高位手机视角，涉及空间观察关系，不只保留滤镜。 |
| 14 | high-angle /ˌhaɪ ˈæŋɡəl/ adj. | 高角度俯拍的。相机高于人物眼平并向下看，不能译成“人物抬头”或“画面很高”。 |
| 15 | substantially /səbˈstænʃəli/ adv. | 明显地、程度较大地。`looking substantially downward` 要求俯视方向可辨认，而非几乎平视。 |
| 16 | operator /ˈɑːpəreɪtər/ n. | 操作者。`camera operator` 是持手机的人；前景手臂属于操作者，不属于画面里的舞者。 |
| 17 | forearm /ˈfɔːrɑːrm/ n. | 前臂，肘到腕之间的部分。与 upper arm 上臂区分；前臂—腕—掌—指构成连续人体链。 |
| 18 | wrist /rɪst/ n. | 手腕。是手掌连接前臂的关节区，不是“手掌”；原文要求它随指向自然配合。 |
| 19 | palm /pɑːm/ n. | 手掌。这里取身体部位义，不是棕榈树。不能只出现几根悬空手指而丢失手掌与腕的连接。 |
| 20 | quadrant /ˈkwɑːdrənt/ n. | 四分区中的一块。`lower-right quadrant` 指画面右下四分区，不是手必须占整整四分之一画面。 |

**原句回读：** `Show a connected forearm, wrist, palm and fingers.`
**译文：** 呈现彼此连续连接的前臂、手腕、手掌与手指。`connected` 同时限定这组身体部件之间的连续关系。

## 三、手的面积、人的距离与控制方向

| 编号 | 词汇、音标、词性 | 基本义 → 本文义、搭配与辨析 |
|---|---|---|
| 21 | quota /ˈkwoʊtə/ n. | 配额、限定份额。README 的 foreground quota 是前景手的面积区间，既防过大也防过小，不只是上限。 |
| 22 | occupy /ˈɑːkjəpaɪ/ v. | 占据。`occupying 10–18% of image area` 明确谈二维面积；人物 70–80% 的表述则需结合 vertical frame 读，不能混成同一量。 |
| 23 | moderate /ˈmɑːdərət/ adj. | 适度的、不极端的。`moderate-size foreground element` 后面又给面积要求，是用具体范围补充“自然大小”。 |
| 24 | primarily /praɪˈmerəli/ adv. | 主要地。`primarily within` 表示主要活动范围；不能据此许可手跨到中央遮脸，因为后文另有明确禁令。 |
| 25 | dominate /ˈdɑːməneɪt/ v. | 占据视觉主导。手需要可见，但不能夺走舞者的主体地位；可见并不等于占画面最多。 |
| 26 | progressively /prəˈɡresɪvli/ adv. | 逐步地。`progressively make her smaller` 禁止人物随镜头后退越变越小，防的是跨时间漂移。 |
| 27 | index finger /ˈɪndeks ˌfɪŋɡər/ n. phr. | 食指。不能把 index 独立按“索引文件”理解；这里是发出方向命令的具体手指。 |
| 28 | extend /ɪkˈstend/ v. | 伸展、延长。`torso extends upward` 是躯干向上舒展，不是要求身体比例真的被拉长。 |
| 29 | lower /ˈloʊər/ v. | 降低。`woman lowers` 指通过屈膝、降髋使身体高度降低；不能误改为相机下降。 |
| 30 | shift /ʃɪft/ v.; n. | 移动、转移。`weight, torso and hips shift` 要求身体位置/重心有清楚变化，而非只有衣服晃动。 |

**原句回读：** `For LEFT, the index finger moves toward screen-left`。
**译文：** 对于 LEFT，食指朝画面左侧移动。`screen-left` 以屏幕为参照，不是舞者的解剖学左侧；两者在面对相机时可能相反。

## 四、反抽动与同步：不能只“差不多跟上”

| 编号 | 词汇、音标、词性 | 基本义 → 本文义、搭配与辨析 |
|---|---|---|
| 31 | sway /sweɪ/ v.; n. | 摆动、侧向摇摆。这里须伴随可见全身方向变化；不允许用极小局部摆髋替代 LEFT / RIGHT。 |
| 32 | twitch /twɪtʃ/ n.; v. | 短促细小的抽动。`tiny hip twitches` 正是被排除的廉价替代动作，与清楚侧移的幅度和持续性不同。 |
| 33 | horizontal /ˌhɔːrəˈzɑːntəl/ adj. | 水平的。LEFT / RIGHT 的方向轴；区别于 UP / DOWN 的 vertical 竖直轴。 |
| 34 | unmistakable /ˌʌnmɪˈsteɪkəbəl/ adj. | 清楚到不易误认的。指手势—身体方向关系应直接可读，不是要求夸张卡通动作。 |
| 35 | corresponding /ˌkɔːrəˈspɑːndɪŋ/ adj. | 相对应的。`corresponding body movement` 必须对应当前这条手势，不是任意一个仍在进行的舞步。 |
| 36 | synchronized /ˈsɪŋkrənaɪzd/ adj.; v. pp. | 同步的。文中进一步限定起始同时、在同一音乐拍内发展，比泛泛“卡点”更具体。 |
| 37 | reaction /riˈækʃən/ n. | 反应。`reaction delay` 是手势已经开始而身体尚未响应的间隔，区别于动作本身持续的时长。 |
| 38 | anticipation /ænˌtɪsəˈpeɪʃən/ n. | 预期；这里指提前启动。`no anticipation` 禁止舞者在手势发出之前就开始对应动作，不是禁止所有自然身体准备。 |
| 39 | independently /ˌɪndɪˈpendəntli/ adv. | 独立地、自行地。`independently freestyle` 指脱离手势规则自由跳舞；与身体各部位的自然协调不同。 |
| 40 | sacrifice /ˈsækrəfaɪs/ v. | 牺牲、以失去某项为代价。`Never sacrifice control for choreography` 表示复杂舞步必须服从控制关系。 |

**原句回读：** `begins as the corresponding finger gesture begins and develops within the same musical beat`。
**译文：** 身体动作与对应手势一同开始，并在同一个音乐节拍内展开。`as` 在此表示同时，不表示“因为”。

## 五、DANCE STYLE、结尾与声音

| 编号 | 词汇、音标、词性 | 基本义 → 本文义、搭配与辨析 |
|---|---|---|
| 41 | viral /ˈvaɪrəl/ adj. | 广泛传播的。`viral dance` 是社交平台流行舞的风格标签，不是病毒相关，也不保证作品会走红。 |
| 42 | short-form /ˌʃɔːrt ˈfɔːrm/ adj. | 短内容形式的。修饰 dance / video 时强调短视频内容形态，并非某一种特定舞种。 |
| 43 | isolation /ˌaɪsəˈleɪʃən/ n. | 分离；舞蹈语境中指身体局部的独立控制。`waist isolation` 不是把腰与人体切开。 |
| 44 | pronounced /prəˈnaʊnst/ adj. | 明显的、突出的。`pronounced hip accents` 不是“发音出来的髋动作”；这里不取 pronounce 的言语意义。 |
| 45 | tasteful /ˈteɪstfəl/ adj. | 有分寸、审美克制的。与 non-explicit 合读，保留成熟时尚表达，不引导裸体或明确性行为。 |
| 46 | deliberate /dɪˈlɪbərət/ adj. | 有意、明确的。`strong, deliberate gestures` 要求方向清楚，不能只让手漂在前景无意义晃动。 |
| 47 | handheld /ˈhændheld/ adj. | 手持的。允许自然轻微不稳，但不许可大幅改变已锁定的高角度与人物距离。 |
| 48 | instability /ˌɪnstəˈbɪləti/ n. | 不稳定性。这里限定为 subtle natural camera instability，是微小手持感，不是脸部身份漂移。 |
| 49 | punchy /ˈpʌntʃi/ adj. | 有冲击力、起音干脆的。`punchy beats` 形容音乐拍点，不能照字面让人物挥拳。 |
| 50 | crisp /krɪsp/ adj. | 清脆、清晰、边界分明的。`crisp percussion` 指打击乐起音利落，区别于含混拖尾的大混响声。 |

**原句回读：** `Never sacrifice hand-to-body control for complicated choreography.`
**译文：** 绝不能为了复杂编舞而牺牲手势对身体的控制关系。这里 `for` 表示以什么换取什么。

## 六、需要保留原文、另作提醒的两点

**高位俯拍与天花板：** 原文同时要求明显向下俯拍和画面上部有相当天花板。这可能依赖参考图本身的构图，不能靠词义解释消除潜在冲突。本次不擅自删改其中一句。

**十条命令与结尾三条命令：** 正文先列十条序列，随后又写结尾 LEFT → RIGHT → UP。词义增补不自行认定这是替换最后三条还是另加三条；实际执行仍需明确序列边界。

`non_diegetic_music` 表示供观众听到、并非故事空间中声源发出的配乐，不等于“无人声音乐”。与 `instrumental` 的维度不同：前者说声源所属层次，后者说是否有歌唱。
