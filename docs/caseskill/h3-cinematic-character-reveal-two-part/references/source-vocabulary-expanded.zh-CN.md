# 两段式角色揭示：逐段词汇与术语增补

v1.1.0 · 2026-09-28。对应 [README 原文](./README.md)、[README 逐段译文](./README.zh-CN.md)、[提示词原文](./prompt.md)、[提示词逐段译文](./prompt.zh-CN.md)。源基线：`73f9aa2c7e55f222b06f8547e5e108c56e6a2287`。本文件扩充 60 项释义，保留原文件全部内容。

IPA 以常见美式宽式读音为主。`n.` 名词，`v.` 动词，`adj.` 形容词，`adv.` 副词，`phr.` 短语。词条同时解释基本义、本文义和容易混淆的语境；方法名称不默认视为模型接口参数。

## 一、The problem / seam contract：引入、确立与跨段衔接

| 编号 | 词汇、IPA、词性 | 基本义 → 本文义与搭配 |
|---|---|---|
| 01 | reveal /rɪˈviːl/ v.; n. | 揭示、使原先未被看清的东西显露。`character reveal` 是逐步让角色形象可见并成立，不只是全身一下入画。 |
| 02 | introduce /ˌɪntrəˈduːs/ v. | 引入、介绍。前半段让观众第一次接触角色；不同于 establish 所强调的把形象稳定地确立下来。 |
| 03 | establish /ɪˈstæblɪʃ/ v. | 建立、确立。这里说角色形象最终获得清晰和权威感；不等于建立镜头 establishing shot，后者在提示词里被排除。 |
| 04 | unmodulated /ʌnˈmɑːdʒəleɪtɪd/ adj. | 没有调节变化的。`unmodulated video` 指强弱、快慢缺少发展，不是在讨论电信载波调制。 |
| 05 | pay off /peɪ ɔːf/ v. phr. | 获得回报、兑现铺垫。`opening that never pays off` 指一直铺垫却没有显著高潮或结论，不是影片没有盈利。 |
| 06 | seam /siːm/ n. | 接缝。这里是两段生成片的边界，涉及末帧、音轨、环境和表演，不只是剪辑软件时间线上的一条线。 |
| 07 | contract /ˈkɑːntrækt/ n. | 契约、共同遵守的规则。`seam contract` 是作者对双段约束的比喻，不是法律合同或程序可执行协议。 |
| 08 | clause /klɔːz/ n. | 条款；语法上也可指分句。本文指连续性规则项，需与两个 prompt 中的对应措辞一起阅读。 |
| 09 | commitment /kəˈmɪtmənt/ n. | 承诺、必须履行的要求。表格里分别写第一段应留下什么、第二段应接续什么。 |
| 10 | assumption /əˈsʌmpʃən/ n. | 假设、默认前提。`not an assumption` 指不能指望下一次生成自动记得上一段；不是反对所有创作假设。 |

**原句回读：** `Split the prompt, but write the seam as a contract.`
**译文：** 可以把提示词拆开，但必须把接缝两端需要共同保持的状态明确写成规则。`but` 连接允许拆分与必须补足的条件。

## 二、REFERENCE：词义不止“保持不变”

| 编号 | 词汇、IPA、词性 | 基本义 → 本文义与搭配 |
|---|---|---|
| 11 | preserve /prɪˈzɜːrv/ v. | 保留原有特征。`preserve the exact face` 指保护参考身份，不许可用所谓优化把脸改成另一人。 |
| 12 | refine /rɪˈfaɪn/ v. | 细化、改善细节。`lock and refine the face` 中 refine 受 same person 约束，不等于重新设计五官比例。 |
| 13 | reconstruct /ˌriːkənˈstrʌkt/ v. | 重建。`from scratch` 是从零开始；原文禁止抛开原图从文字另造角色。 |
| 14 | proportion /prəˈpɔːrʃən/ n. | 比例关系。`body proportions` 是身体各部位的比例，不是角色占画面的面积比例。 |
| 15 | approved /əˈpruːvd/ adj.; v. pp. | 获准使用的。`approved major poses` 指参考库中允许调用的主要姿态；不等于某个外部机构审批。 |
| 16 | supplementary /ˌsʌpləˈmentəri/ adj. | 补充的。`supplementary poses` 增加姿态参照，不自动成为新的面部身份来源。 |
| 17 | identity /aɪˈdentəti/ n. | 个体身份、可辨认的同一性。Picture 2 只负责同一人的脸，不是把 Picture 1、2 混成第三个人。 |
| 18 | remaining /rɪˈmeɪnɪŋ/ adj. | 剩下尚未用尽的。`remaining approved poses` 指库中未重点使用的姿态，不是要求模型凭空补出新姿势。 |
| 19 | emphasize /ˈemfəsaɪz/ v. | 强调、重点呈现。`not emphasized in Part 1` 不必然等于完全没出现过，而是没有承担主要展示。 |
| 20 | photographic /ˌfoʊtəˈɡræfɪk/ adj. | 摄影式的、有照片观感的。强调真实皮肤、材质与光学外观；不等于文件真的由相机实拍。 |

**原句回读：** `Treat these poses as the ONLY approved major poses for this character.`
**译文：** 将这些姿态视为该角色唯一获准使用的主要姿态。`ONLY` 限定允许来源，不是要求每帧完全没有自然微动。

## 三、VISUAL LANGUAGE：把剪辑术语拆成可理解动作

| 编号 | 词汇、IPA、词性 | 基本义 → 本文义与搭配 |
|---|---|---|
| 21 | cinematography /ˌsɪnəməˈtɑːɡrəfi/ n. | 电影摄影，包括机位、景别、光线、镜头运动等；与后期 editing 相关但不是同一个环节。 |
| 22 | editorial /ˌedɪˈtɔːriəl/ adj. | 编辑式的；时尚编辑摄影式的。修饰 transition 时偏剪辑组织，修饰 photography 时偏杂志/宣传影像风格，不能一律译“编辑的”。 |
| 23 | graphic /ˈɡræfɪk/ adj. | 图形结构的。`graphic match` 通过线条、形状或位置相似衔接，不是让人物变成二维图标。 |
| 24 | crop /krɑːp/ n.; v. | 裁切、裁切范围。改变显示的局部，不意味着角色姿态已改变；同一姿态可以有多种 crop。 |
| 25 | reframe /ˌriːˈfreɪm/ v. | 重新构图。可以改变取景与相机关系；范围比单纯 crop 更宽，不能自动理解成大幅运镜。 |
| 26 | wipe /waɪp/ n.; v. | 擦除式或遮挡式转场。本文的 foreground / architectural wipe 依靠前景或建筑遮挡，不一定是后期模板特效。 |
| 27 | shutter /ˈʃʌtər/ n. | 快门。`shutter transition` 是快门式视觉切换，`shutter sound` 才是声音；不要把二者误当同一媒介要求。 |
| 28 | stroboscopic /ˌstroʊbəˈskɑːpɪk/ adj. | 频闪式、断续闪现式的。修饰 photographic echoes 时指摄影图像短促重复显现，不是人物复制成多个新角色。 |
| 29 | negative space /ˈneɡətɪv speɪs/ n. phr. | 负空间、留白。是主体之外参与构图的区域，不是“负面空间”或必须全黑的背景。 |
| 30 | callback /ˈkɔːlbæk/ n. | 回指、再次唤起前面元素。`visual callback` 用不同取景呼应旧细节，区别于重复播放原镜头。 |

**原句回读：** `These techniques are applied to the PHOTOGRAPHIC IMAGE, not to the character's body.`
**译文：** 这些技法作用于摄影图像，而不是作用于人物的身体结构。不能把匹配剪辑做成手臂或脸部的形变。

## 四、CUT 01–13 / CAMERA PRIORITY：身体细节与景别

| 编号 | 词汇、IPA、词性 | 基本义 → 本文义与搭配 |
|---|---|---|
| 31 | foreground /ˈfɔːrɡraʊnd/ n. | 前景、靠近镜头的画面层。面纱、头发边缘或建筑均可作前景，不固定指画面下半部。 |
| 32 | architecture /ˈɑːrkɪtektʃər/ n. | 建筑及其空间结构。`through church architecture` 指借柱、拱等布置画面，不是切换到另一座教堂。 |
| 33 | veil /veɪl/ n. | 面纱、头纱。其遮挡与运动属于服装材料，不应翻译成抽象“神秘面纱”而忽略具体物体。 |
| 34 | headpiece /ˈhedpiːs/ n. | 头饰。与 hairstyle 发型分开；身份保持包括二者，不能把头饰重画成新的发型。 |
| 35 | contour /ˈkɑːntʊr/ n. | 外形轮廓、边线。`sleeve contour` 指袖子的可见形状，常作图形匹配参照。 |
| 36 | align /əˈlaɪn/ v. | 对齐。`aligns with costume trim` 是建筑线与服装饰边视觉对齐，不要求两件物体在空间中真的相连。 |
| 37 | shallow /ˈʃæloʊ/ adj. | 浅的。`shallow depth of field` 指清晰范围薄，不是场景空间浅，也不是人物内容“肤浅”。 |
| 38 | depth of field /depθ əv fiːld/ n. phr. | 景深，画面中可接受清晰的距离范围。与相机到人物的距离、背景是否存在不是同一个概念。 |
| 39 | bust /bʌst/ n. | 胸像、胸部以上的人像范围。景别列表中按肖像覆盖理解，不取雕塑材质义或其他口语义。 |
| 40 | medium-full /ˈmiːdiəm fʊl/ adj.; n. phr. | 中全景式覆盖，通常保留人物大部分身体。实际边界应看正文，不能硬规定每次都必须从同一关节裁切。 |

**原句回读：** `Use a precise reframing rather than a large camera move.`
**译文：** 采用精确的重新构图，而不是大幅摄影机运动。`rather than` 排除的是过大的运动方式，不是否定一切微小调整。

## 五、MUSIC / SOUND EFFECTS：配器与声学不混译

| 编号 | 词汇、IPA、词性 | 基本义 → 本文义与搭配 |
|---|---|---|
| 41 | instrumental /ˌɪnstrəˈmentəl/ adj. | 纯器乐的。与后面的 no singing / choir / vocal samples 一起排除人声，不等于音量很低或没有配乐。 |
| 42 | ecclesiastical /ɪˌkliːziˈæstɪkəl/ adj. | 教会的、与教会相关的。修饰 atmosphere 是音乐意象，不代表原文在准确复原某种宗教礼仪音乐。 |
| 43 | organ /ˈɔːrɡən/ n. | 管风琴。此处取乐器义，不是人体器官；与教堂气氛、器乐配乐相关。 |
| 44 | resonance /ˈrezənəns/ n. | 共鸣、共振。`bell resonance` 是钟声鸣响质感；与 room reverb 的空间混响不能完全等同。 |
| 45 | chamber /ˈtʃeɪmbər/ n.; adj. | 房间；室内乐的。`chamber strings` 指室内乐规模弦乐，不是把弦乐器放进画面里的小房间。 |
| 46 | strings /strɪŋz/ n. pl. | 弦乐组、弦乐声部。`low strings` 指低音弦乐层次，不是低处垂下的绳子。 |
| 47 | celesta /səˈlestə/ n. | 钢片琴，具有清亮、钟铃般音色的键盘乐器。与 piano 并列为可选音色，不是同一乐器的另一拼写。 |
| 48 | harmonic /hɑːrˈmɑːnɪk/ adj. | 和声的。`harmonic state` 包括当下和声进行的状态，区别于只保持相同速度。 |
| 49 | rhythmic /ˈrɪðmɪk/ adj. | 节奏的。`rhythmic state` 指拍点与节奏组织状态；相同 BPM 并不足以说明两段节奏相位连续。 |
| 50 | reverb /ˈriːvɜːrb/ n. | 混响，reverberation 的常用简称。`reverb tail` 是声源停止或减弱后仍衰减的空间尾音，不是新开始的一段环境声。 |

**原句回读：** `keep harmonic and rhythmic momentum alive`。
**译文：** 保持和声与节奏的推进动势仍在延续。`alive` 是比喻“没有收死”，不是添加生物声音。

## 六、Part 2 / FINAL KEY VISUAL / 总结语言

| 编号 | 词汇、IPA、词性 | 基本义 → 本文义与搭配 |
|---|---|---|
| 51 | sustained /səˈsteɪnd/ adj.; v. pp. | 持续保持的。`sustained chord` 指延长的和弦声，不是反复敲击同一拍。 |
| 52 | chord /kɔːrd/ n. | 和弦。不要与 `cord` 绳索混淆；最终器乐和弦是音乐收束，不是配饰细节。 |
| 53 | momentum /moʊˈmentəm/ n. | 动量、动势。修饰音乐时是推进感，修饰布料或身体时还可指运动惯性；不要统译“冲量”。 |
| 54 | uninterrupted /ˌʌnɪntəˈrʌptɪd/ adj. | 未中断的。`same uninterrupted soundtrack` 比“相同音乐风格”强，要求听感上是同一条音轨持续播放。 |
| 55 | residual /rɪˈzɪdʒuəl/ adj. | 残余的。`residual movement` 指主体已稳定后头发、面纱、衣料仍有轻微余动，不是重新启动一个主动作。 |
| 56 | escalation /ˌeskəˈleɪʃən/ n. | 逐步加强。这里指后半段剪辑与展示强度增长，不等同所有镜头无差别加速。 |
| 57 | resolve /rɪˈzɑːlv/ v. | 收束到、得到落点。`resolve into the final image` 是视觉/情绪收束，不是单纯修复技术问题。 |
| 58 | definitive /dɪˈfɪnətɪv/ adj. | 定版式的、最终确立的。`definitive character image` 指最能确定角色形象的终帧，不代表已有官方认证。 |
| 59 | platitude /ˈplætɪtuːd/ n. | 空泛套话。`non-repetition platitudes` 指只说“别重复”却不说明哪些机制不能重复。 |
| 60 | compliance /kəmˈplaɪəns/ n. | 遵守程度、按要求执行。`vague compliance` 形容模糊规则带来的模糊执行，不能当成法律合规评估。 |

**原句回读：** `Hair, veil and clothing have subtle residual movement.`
**译文：** 头发、面纱与衣物保留细微的残余运动。终帧稳定不等于突然把全部材质机械冻住。

## 七、原文校读补充，不改写原命令

**数量：** README 写“six shot mechanisms”，随后实际列了七项。应分别掌握这七项，不把文字中的 six 当作已核实的数量。

**不重复的边界：** Part 2 的建筑遮挡镜头与 Part 1 存在机制相似之处，不能仅凭 README 的“完全不重复”就断言镜头设计已通过逐镜审计。本增补只解释用词。

**three-quarter：** 是三分之四侧向观感的常用表达，不是跨所有场景统一的 45°–60° 硬参数。原译文中的角度范围只能视作帮助理解的近似说明。

**sttained glass：** 原 prompt 的拼写多了一个 t；应按 stained glass“彩绘玻璃”理解，原文不在本轮修改。

**Index / British Puritan：** 原文给的是风格关联线索，未明确说明 Index 的出处。保留名称，不自行补写成已确认的作品、宗教派别或历史建筑分类。

**跨生成连续：** 把同样的连续性要求写进两条提示词，不等于音频样本和末帧一定自动传入下一次生成。语言理解与实际工具传参是两个层面。
