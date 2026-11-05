# 水上闯关综艺：逐段词汇增补

v1.1.0 · 2026-09-28。对应 [README 原文](./README.md)、[README 译文](./README.zh-CN.md)、[提示词原文](./prompt.md)、[提示词译文](./prompt.zh-CN.md)。源基线：`73f9aa2c7e55f222b06f8547e5e108c56e6a2287`。保留既有文件，以 50 项语境词汇补充原释义。

IPA 以常见美式宽式读音为主。`n.` 名词；`v.` 动词；`adj.` 形容词；`adv.` 副词；`conj.` 连词；`phr.` 短语。每组先释词，再回读原句。

## 一、The problem / The breakthrough：固定什么，开放什么

| 编号 | 词汇、IPA、词性 | 基本义 → 本文义与辨析 |
|---|---|---|
| 01 | specification /ˌspesəfɪˈkeɪʃən/ n. | 规格、详尽规定。`over-specification` 指把本应自然发生的表演细节规定得过密，不是反对所有明确约束。 |
| 02 | stiff /stɪf/ adj. | 僵硬、缺乏自然变化。`stiff results` 在此评价表演观感，不等于人物材质硬或关节受伤。 |
| 03 | micromanage /ˈmaɪkroʊmænɪdʒ/ v. | 事无巨细地管控。这里是每个机位、动作都写死；与控制故事必要节点的 anchoring 区分。 |
| 04 | spontaneity /ˌspɑːntəˈneɪəti/ n. | 自发性、自然发生感。综艺需要看似临场反应的表演，不表示生成过程没有任何设计。 |
| 05 | improvise /ˈɪmprəvaɪz/ v. | 即兴组织。指在既定剧情节点之间选择具体动作；不是随意改变必须发生的摔倒与落水。 |
| 06 | improvisation /ɪmˌprɑːvəˈzeɪʃən/ n. | 即兴创作过程。是 improvise 的名词形式，不能只记“即兴”而忽略原文规定的自由范围。 |
| 07 | non-negotiable /ˌnɑːn nɪˈɡoʊʃiəbəl/ adj. | 不可协商、不可改变的。`plot anchors` 的前置限定，说明这些节点与开放的细节不在同一权限层级。 |
| 08 | delegate /ˈdeləɡeɪt/ v. | 委派、交由他者决定。`delegated to the model` 指明确授予具体动作与摄影选择权，不是让模型改写全部目标。 |
| 09 | execution /ˌeksəˈkjuːʃən/ n. | 执行、实现方式。`Free the execution`＝放开实现细节；此处不取“处决”义，也不指运行程序命令。 |
| 10 | intact /ɪnˈtækt/ adj. | 完整未损的。`story beats remain intact` 要求必要事件及其先后关系仍在，不只是保留相同人物。 |

**原句回读：** `Lock the story beats. Free the execution.`
**译文：** 锁定剧情节点，放开具体实现方式。这里 `beat` 是叙事事件单位，不能自动理解成音乐节拍。

## 二、subject_definitions / summary：参赛者与赛道

| 编号 | 词汇、IPA、词性 | 基本义 → 本文义与辨析 |
|---|---|---|
| 11 | contestant /kənˈtestənt/ n. | 参赛者。区别于主持人、观众或随意出现的角色；主角是实际尝试完成赛道的人。 |
| 12 | derived /dɪˈraɪvd/ v. pp.; adj. | 来源于、由……导出的。`visually derived from Picture 1` 规定人物外观来源，不规定障碍与背景也来自此图。 |
| 13 | apparent /əˈpærənt/ adj. | 看起来的、表观的。`apparent age` 是视觉年龄印象；后文 `apparent success` 则是看似成功但未真正结束。 |
| 14 | physique /fɪˈziːk/ n. | 体格、体型。与 face、clothing 并列，要求身体总体形态一致，不只锁住脸。 |
| 15 | wearable /ˈwerəbəl/ adj. | 可穿戴的。`wearable accessories` 包括戴在人身上的配饰；禁止新增它们不等于禁止赛道出现必要机关。 |
| 16 | course /kɔːrs/ n. | 赛道、路线。`obstacle course` 不是“障碍课程”，也不是镜头 course 的抽象进程。 |
| 17 | obstacle /ˈɑːbstəkəl/ n. | 障碍、关卡装置。这里是物理可接触设施，需要与人的承重和移动相互作用。 |
| 18 | arena /əˈriːnə/ n. | 竞技场、活动场地。`one continuous arena` 要求同一比赛空间，不是每一镜都换一个水池。 |
| 19 | linear /ˈlɪniər/ adj. | 线性排列、沿顺序连接的。`linear track` 表示关卡连成可理解的前进路线，不是要求镜头始终沿绝对直线。 |
| 20 | runway /ˈrʌnweɪ/ n. | 通道、助跑道。本文指连接关卡的行进道，不是飞机跑道或服装秀 T 台。 |

**原句回读：** `The runway and obstacles remain spatially connected and visually understandable from shot to shot.`
**译文：** 镜头切换前后，通道和障碍物仍在空间上相连，位置关系能够被观众理解。`from shot to shot` 是跨镜头连续性。

## 三、retention_analysis / 自由授权句

| 编号 | 词汇、IPA、词性 | 基本义 → 本文义与辨析 |
|---|---|---|
| 21 | retention /rɪˈtenʃən/ n. | 保留、保持。该字段说明人物、场地和剧情哪些必须保持，不是要求显示分析过程或模型内部推理。 |
| 22 | coherent /koʊˈhɪrənt/ adj. | 连贯、相互吻合的。`coherent obstacle course` 要求空间和事件接得上；不是只要颜色风格统一。 |
| 23 | provided /prəˈvaɪdɪd/ conj. | 只要、以……为条件。`provided the beats remain intact` 对前面的创作自由设条件，不是 provide 的“提供了”。 |
| 24 | freedom /ˈfriːdəm/ n. | 自由度。`creative freedom over X` 中 over 列明自由范围，不能无限外推为可以改人物身份。 |
| 25 | placement /ˈpleɪsmənt/ n. | 放置、位置安排。`camera placement` 指机位选择，区别于镜头焦距和后期剪辑顺序。 |
| 26 | broadcast /ˈbrɔːdkæst/ adj.; n. | 广播电视播出的；播出。`broadcast framing` 指综艺转播式取景，不是播出平台的技术协议。 |
| 27 | convincing /kənˈvɪnsɪŋ/ adj. | 可信、让人信服的。这里要求动作与受力看起来合理，不表示场景是真实拍摄而非生成。 |
| 28 | plausible /ˈplɔːzəbəl/ adj. | 合理可能的。`physically plausible` 要求运动符合可理解物理关系；不等于已做严格仿真校验。 |
| 29 | evasive /ɪˈveɪsɪv/ adj. | 躲避的、避让性的。`evasive movements` 是躲关卡的动作，不取言语“闪烁其词”义。 |
| 30 | combination /ˌkɑːmbəˈneɪʃən/ n. | 组合。模型可组合蹲闪、踏步、倾身等，但动作组合仍应服务固定剧情，不是随机并列动作名称。 |

**原句回读：** `provided the required story beats remain intact`。
**译文：** 前提是必须发生的剧情节点完整保留。这个条件从句是自由授权的边界。

## 四、Shot 2–5：过关、失衡、恢复与抓边

| 编号 | 词汇、IPA、词性 | 基本义 → 本文义与辨析 |
|---|---|---|
| 31 | cylinder /ˈsɪlɪndər/ n. | 圆柱体、滚筒。`rolling-cylinder obstacle` 指随脚下受力转动的滚筒关卡，不是固定石柱。 |
| 32 | clear /klɪr/ v. | 通过、越过。`clears this section`＝成功通过这一段，不是把场景清空，也不是让图像变清晰。 |
| 33 | duck /dʌk/ v. | 低头或伏身闪避。与 jump 向上跳不同；此处不是名词“鸭子”。 |
| 34 | lean /liːn/ v. | 倾身、侧靠。`leaning` 可用于避障或平衡，不能与整个身体平移的 stepping 混成一类。 |
| 35 | disrupt /dɪsˈrʌpt/ v. | 打断、扰乱。`disrupt her balance` 指某次物理互动使平衡失去，不是人物无原因突然倒下。 |
| 36 | accidental /ˌæksɪˈdentəl/ adj. | 意外发生的。此处要求表演看似失误；不意味着剧情上不再预设这次摔倒。 |
| 37 | staged /steɪdʒd/ adj.; v. pp. | 刻意摆布、安排痕迹明显的。`rather than staged` 说观感不要像刻意演摔，不否定整段本来经过设计。 |
| 38 | recover /rɪˈkʌvər/ v. | 恢复、重新取得动作控制。摔倒后重新站起并继续比赛；不是医学治疗恢复。 |
| 39 | resume /rɪˈzuːm/ v. | 中断后继续。`resumes the competition` 接续同一次闯关，不能回到开场重新介绍人物。 |
| 40 | secure /sɪˈkjʊr/ v. | 抓牢、确保稳固。`securing the wall edge with both hands` 要求双手真正抓住墙沿，不是手仅靠近墙顶。 |

**原句回读：** `She successfully runs onto the wall and reaches the top, securing the wall edge with both hands.`
**译文：** 她成功冲上弧墙并抵达顶部，双手抓牢墙沿。抓边建立了下一镜失去抓握的前提。

## 五、Shot 6–8 / overall_soundscape / 音乐收束

| 编号 | 词汇、IPA、词性 | 基本义 → 本文义与辨析 |
|---|---|---|
| 41 | padded /ˈpædɪd/ adj. | 有软垫包覆的。修饰机械关卡，属于节目道具状态；不能漏译成裸露硬质撞击装置。 |
| 42 | strike /straɪk/ v.; n. | 击中、打击。本文是侧方机关产生的物理事件，需与角色失去抓握、横向离墙连续相接。 |
| 43 | laterally /ˈlætərəli/ adv. | 向侧面、横向地。`redirects her laterally` 指冲击改变运动方向，不是角色沿墙直直下滑。 |
| 44 | grip /ɡrɪp/ n.; v. | 抓握；抓紧。`lose her grip` 指双手失去对墙沿的控制，应该接在前面的 secure edge 之后。 |
| 45 | splash /splæʃ/ n.; v. | 水花；溅起。`convincing splash` 应由身体入水产生，不是先出现水花、人物随后才落水。 |
| 46 | resurface /ˌriːˈsɜːrfɪs/ v. | 再次浮出水面。前缀 re- 表示重新，承接同一个水池里的入水事件，不是瞬移到岸边。 |
| 47 | stunned /stʌnd/ adj. | 一时发愣、惊住。综艺语境中的短暂反应，不应自动升级为医疗意义的昏迷。 |
| 48 | aggrieved /əˈɡriːvd/ adj. | 感到委屈、不服气。结尾“差一点嘛”的可爱委屈感，不是严重受害指控。 |
| 49 | punchline /ˈpʌntʃlaɪn/ n. | 笑点落句、包袱。这里是结尾台词重新解释整段遭遇，不取拳击动作义。 |
| 50 | resolve /rɪˈzɑːlv/ v. | 收束、趋向结束。`music resolves into a light comedic ending` 指音乐情绪收回轻喜剧结尾，不是“解决故障”。 |

**原句回读：** `She looks exhausted and briefly stunned, then reacts ... with a cute, slightly aggrieved, comedic expression.`
**译文：** 她看起来筋疲力尽，短暂发愣，随后以可爱、略带委屈的喜剧表情作出反应。这里存在明确的表情先后次序。

## 六、专名与技术范围

**Fishbone Reverse：** 原文把它作为关卡名称使用；没有给出足够资料确认官方中文名。保留名称，并按正文“带旋转结构的障碍关卡”理解，不自行编造“鱼骨倒置赛道”的官方译名。

**story beat 与 musical beat：** 前者是剧情节点，后者是音乐拍点；本文允许音乐随挑战发展，不把每个剧情节点自动等同精确一拍。

**分辨率 0.3 / 0.8 / 1：** 原说明给出的是作者工作流中的参数写法，不能在缺少节点和实现说明时解释成通用像素数或宣称更换分辨率绝不会改变随机生成的编排。本次保持原说明，仅注明理解边界。

**single-take-feel：** README 结果部分强调“一镜到底感”；提示词实际分 Shot 1–8 并允许剪辑。feel 是观感，不应擅自升级成严格零切镜要求。
