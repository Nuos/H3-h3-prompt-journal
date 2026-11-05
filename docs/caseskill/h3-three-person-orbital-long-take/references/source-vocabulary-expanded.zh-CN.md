# 三人遮挡衔接环绕长镜头：词汇精读增补

v1.1.0 · 2026-09-28。对应 [README 原文](./README.md)、[README 译文](./README.zh-CN.md)、[提示词原文](./prompt.md)、[提示词译文](./prompt.zh-CN.md)。保留原文件全部内容；本增补按原章节定位词义，不重新编写镜头方案。源文本基线：`73f9aa2c7e55f222b06f8547e5e108c56e6a2287`。

IPA 以常见美式宽式读音为主。`n.` 名词；`v.` 动词；`adj.` 形容词；`adv.` 副词；`phr.` 短语。以下 50 项优先解释词在原文中的实际作用。

## 一、REFERENCE PRIORITY / MASTER ENVIRONMENT

| 编号 | 词汇、IPA、词性 | 基本义、本文义与搭配 |
|---|---|---|
| 01 | priority /praɪˈɔːrəti/ n. | 优先次序。`reference priority` 说明不同参考图各自管什么、发生冲突时听谁的，不是图像文件的排序位置。 |
| 02 | absolute /ˈæbsəluːt/ adj. | 绝对的、无条件的。标题中用来强化硬约束；它表达作者要求的力度，并不证明模型一定严格执行。 |
| 03 | master /ˈmæstər/ n.; adj. | 主控者；主控的。`master environment` 是作为空间基准的环境，不取“师傅的房间”义。与其他图只提供外观形成权限区分。 |
| 04 | spatial /ˈspeɪʃəl/ adj. | 空间的，涉及位置、距离和方向。`spatial coordinate system` 是三人在同一环境中的位置参照，区别于音乐的 temporal reference。 |
| 05 | coordinate /koʊˈɔːrdənət/ n. | 坐标。这里是 `coordinate system` 的组成词；动词 `coordinate` /koʊˈɔːrdəneɪt/ 则表示协调，读音和词性不同。 |
| 06 | source /sɔːrs/ n. | 来源。`the only environment source` 限定环境信息来自 Picture 1，不只是要求“画风相似”。 |
| 07 | respective /rɪˈspektɪv/ adj. | 各自的、分别对应的。`their respective people's appearance` 指图片 2 管人物 2、图片 3 管人物 3，不能交叉换脸。 |
| 08 | reconstruct /ˌriːkənˈstrʌkt/ v. | 重建。`reconstruct a different room` 指另造一间房；与在同一房间改变机位、看到先前未入画区域不同。 |
| 09 | generic /dʒəˈnerɪk/ adj. | 泛化的、通用模板式的。`generic studio` 是没有原房间具体特征的通用摄影棚，不是“普通”这一价值判断。 |
| 10 | consistent /kənˈsɪstənt/ adj. | 一致、相容。`consistent with Picture 1` 要求尺度、灯光、接地等共同成立，不能只凭颜色接近就算空间一致。 |

**原句回读：** `Picture 2 and Picture 3 provide ONLY their respective people's appearance.`
**译文：** 图片 2 和图片 3 只提供各自对应人物的外观。`ONLY` 限定参考职责，不能借它们引入新背景。

## 二、THREE PEOPLE IN ONE PHYSICAL SPACE / VISIBILITY

| 编号 | 词汇、IPA、词性 | 基本义、本文义与搭配 |
|---|---|---|
| 11 | physically /ˈfɪzɪkli/ adv. | 在物理空间中。`physically present` 强调三人从一开始就在同一场景里；它不等于三人从一开始都被镜头看见。 |
| 12 | present /ˈprezənt/ adj. | 在场的、存在的。这里不是名词“礼物”，也不是动词 `present` /prɪˈzent/“展示”。 |
| 13 | integrate /ˈɪntəɡreɪt/ v. | 整合进整体。`physically integrated` 指人的接地、光影和尺寸融入同一空间，不是简单把三张照片并排拼贴。 |
| 14 | scale /skeɪl/ n. | 尺度、大小关系。`body scale` 是身体相对环境的尺寸；不应与画面中的占比混为一谈，后者还能通过机位变化改变。 |
| 15 | contact /ˈkɑːntækt/ n. | 接触。`contact with the floor` 包含脚底与地面的合理贴合关系，不是人物悬在地面上方却加一个阴影。 |
| 16 | visibility /ˌvɪzəˈbɪləti/ n. | 可见性。规定镜头能看见谁；与人物是否在空间中实际存在是两个不同条件。 |
| 17 | conceal /kənˈsiːl/ v. | 遮藏，使不可见。`concealed by the body` 指由当前人物的身体形成遮挡，不是把下一人删除后再生成。 |
| 18 | silhouette /ˌsɪluˈet/ n. | 外轮廓、剪影。原文连远处剪影也禁止提前出现；只遮住脸但留一个人形轮廓，仍违反该可见性要求。 |
| 19 | reflection /rɪˈflekʃən/ n. | 反射、映像。镜子或反光面中出现人物也算可见；不能只检查正面画面里有没有其他人。 |
| 20 | simultaneously /ˌsaɪməlˈteɪniəsli/ adv. | 同时地。仅最后揭示允许三人同时可见，不是让三个人依次淡入却从未真正共处一帧。 |

**原句回读：** `Although all three people physically exist in the same space from the beginning`。
**译文：** 尽管三个人从一开始就实际存在于同一个空间中……后文才规定镜头每次只看见一个人。让步句刻意区分“在场”与“入画”。

## 三、SPATIAL ARRANGEMENT / The problem

| 编号 | 词汇、IPA、词性 | 基本义、本文义与搭配 |
|---|---|---|
| 21 | arrangement /əˈreɪndʒmənt/ n. | 布置、排列。此处是三人的站位与遮挡关系，不是音乐编曲。`spatial arrangement` 需要与摄影机路径共同理解。 |
| 22 | relatively /ˈrelətɪvli/ adv. | 相对地。`relatively close together` 是相对于可完成近距离衔接的尺度，不是三人紧贴或重叠。 |
| 23 | viewing angle /ˈvjuːɪŋ ˈæŋɡəl/ n. phr. | 观看方向或可视角度。这里主要指当前相机观察方向造成的显隐，不应直接当作某个固定镜头视场角数值。 |
| 24 | round /raʊnd/ v. | 绕过。`rounding the current person's body` 指相机绕过身体侧缘，区别于双人案例中 `round` 的“粗略化”比喻。 |
| 25 | linkage /ˈlɪŋkɪdʒ/ n. | 衔接关系、连接机制。文章用它取代 point-to-point flight，强调一个近身环绕如何接入下一个，而不是跨房间飞过去。 |
| 26 | point-to-point /ˌpɔɪnt tə ˈpɔɪnt/ adj. | 点到点的。本文批评把人物当空间终点、以直达移动代替遮挡衔接；不是所有点间运动本身都不合理。 |
| 27 | teleport /ˈteləpɔːrt/ v. | 瞬移。位置突然跳变而没有连续空间过程，区别于人物被挡住后随着相机移动重新显现。 |
| 28 | crossfade /ˈkrɔːsfeɪd/ n.; v. | 交叉淡化：一个画面淡出时另一个淡入。它改变画面混合比例，不提供真实绕过人体的空间轨迹。 |
| 29 | semantic /sɪˈmæntɪk/ adj. | 语义的。README 的 `The semantic of transition` 用法不够自然，可理解为“transition 这个词的语义联想”，不要机械译成一个技术模块。 |
| 30 | poisoned /ˈpɔɪzənd/ adj.; v. pp. | 被毒化的；这里是作者的修辞，形容 transition 已带有不合需求的联想，不是在声称发生了训练数据投毒攻击。 |

**原句回读：** `The real transition is not flight. It is linkage.`
**译文：** 真正需要设计的衔接不是跨空间飞行，而是环绕段之间的连接关系。句子是在重新规定 transition 的创作含义。

## 四、The breakthrough / CORE CAMERA CONCEPT

| 编号 | 词汇、IPA、词性 | 基本义、本文义与搭配 |
|---|---|---|
| 31 | foreground /ˈfɔːrɡraʊnd/ n. | 前景，靠近相机的画面层次。这里人体侧缘进入极近前景，承担遮挡功能，不是“画面下方”的同义词。 |
| 32 | occlusion /əˈkluːʒən/ n. | 遮挡。这里由当前人物身体挡住后方人物；遮挡物、被遮物和相机必须有可理解的相对位置。 |
| 33 | obstruction /əbˈstrʌkʃən/ n. | 阻挡物、遮蔽物。与 occlusion 相比，更偏向造成遮挡的物或障碍；原句 `behind the obstruction`＝在遮挡物后方。 |
| 34 | emerge /ɪˈmɜːrdʒ/ v. | 显现、从遮挡后出来。不是突然被创造出来；人物原先已存在，只是现在进入视线。 |
| 35 | orbital /ˈɔːrbɪtəl/ adj. | 环绕轨道式的。修饰 camera 或 long take 时，说明相机围绕主体移动，而非人物自转。 |
| 36 | orbit /ˈɔːrbɪt/ n.; v. | 环绕；环绕运行。每人对应一段近距离环绕，随后通过遮挡换中心；不等于相机原地摇向另一人。 |
| 37 | close-range /ˌkloʊs ˈreɪndʒ/ adj. | 近距离的。强调摄影机与人的物理距离；`close-up` 则是景别，二者有关但不等同。 |
| 38 | motivated /ˈmoʊtəveɪtɪd/ adj. | 有动机、有根据的。`motivated camera movement` 是为绕开身体、改变视线等可解释原因而动，不是说摄影机有主观情绪。 |
| 39 | long take /lɔːŋ teɪk/ n. phr. | 长镜头，连续拍摄/呈现的一段镜头。这里强调无内部切镜，不是英文 `long shot`“远景”。 |
| 40 | reveal /rɪˈviːl/ n.; v. | 揭示、显露。在本案例中下一人物由遮挡后显露；结尾 final reveal 则让三人的空间关系一起可见。 |

**原句回读：** `the next character suddenly emerges from behind the obstruction as a fresh orbital center`。
**译文：** 下一位人物突然从遮挡物后显露，并成为新的环绕中心。`suddenly` 是显露的观感，不许可瞬移。

## 五、Optical behavior / negative constraints / 结尾

| 编号 | 词汇、IPA、词性 | 基本义、本文义与搭配 |
|---|---|---|
| 41 | perspective /pərˈspektɪv/ n. | 透视关系。人物大小、远近与相对位置随机位而呈现的几何关系；不是泛指“审美角度”。 |
| 42 | parallax /ˈpærəlæks/ n. | 视差。相机移动时近远物体相对位移不同，是空间连续感的线索，不等于整体画面做同速平移。 |
| 43 | fisheye /ˈfɪʃaɪ/ n.; adj. | 鱼眼镜头/鱼眼式的。原文排除这类强烈投影变形；不能把所有广角或近距离透视都叫 fisheye。 |
| 44 | morph /mɔːrf/ v.; n. | 形变过渡。`no morph` 禁止人物 1 连续变成另一身份；不禁止同一人物正常转头或改姿势。 |
| 45 | enumerate /ɪˈnuːməreɪt/ v. | 逐项列举。`failure modes enumerated` 要求点明具体失败方式，区别于只写一句泛泛的“不要出错”。 |
| 46 | prohibition /ˌproʊəˈbɪʃən/ n. | 禁止条款。应读清其宾语：禁止的是换环境、提前露脸等具体事件，不是禁止所有变化。 |
| 47 | sufficient /səˈfɪʃənt/ adj. | 足够的。`necessary but not sufficient`＝必要但不充分；有 no cut 还需要正面规定怎样连续衔接。 |
| 48 | generative /ˈdʒenərətɪv/ adj. | 能生成结构的。`generative grammar` 在此指可复用的镜头组织模式，不是宣称采用了语言学的某个形式语法系统。 |
| 49 | pull-back /ˈpʊlbæk/ n. | 后拉镜头。在结尾适度后撤以容纳三人；要与直接改变焦距的 zoom-out 区分，也不是跨房间远离主体。 |
| 50 | co-presence /ˌkoʊˈprezəns/ n. | 共同在场。结尾三人同框是影片要呈现的空间结果；仅凭最终一帧不能独立证明生成过程每一刻都维持同一三维场景。 |

**原句回读：** `Constraints like "no cut" and "no morph" are necessary but not sufficient.`
**译文：** “不切镜”“不做形变”这样的约束是必要的，但还不够。原文后面要求的是能连续组织画面的正面方法。

## 六、跨段辨析

**在场、可见、揭示：** `present` 管是否位于场景中；`visible` 管当前镜头是否看见；`revealed` 管何时从不可见转为可见。不能因下一人物尚不可见，就把他安排成之后才生成。

**orbit、pan、roll：** 环绕改变相机围绕主体的位置；摇摄改变镜头指向；滚转绕光轴改变画面倾斜。后三者中 pan、roll 是用于辨析的相关术语，不冒充本文新增指令。

**long take、long shot：** 前者谈镜头连续时长，后者谈远景景别。原文需要的是近距离长镜头，二者完全不矛盾。

## 校读说明

本次保存作者的“遮挡衔接”方案，不把写入提示词后的效果描述当作已重复验证的模型能力。标题中的技术命名是案例作者组织经验的方法名，不应误认成 H3 接口中的正式参数。
