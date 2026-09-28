# 双人异速舞蹈：逐段词汇增补

版本：v1.1.0 · 2026-09-28。对应 [README.md](./README.md)、[原逐段译文](./README.zh-CN.md) 与 [中文提示词](./prompt.md)。本文件增补词义、词性、搭配和辨析，不替换或缩减已有译文。英文原文基线：`73f9aa2c7e55f222b06f8547e5e108c56e6a2287`。

音标采用常见美式宽式 IPA；复合表达按组成词标读，不表示该表达是标准化技术名称。`n.` 名词，`v.` 动词，`adj.` 形容词，`adv.` 副词，`phr.` 短语。以下 50 项按原文章节归组；“本文义”是对本文语言的解释，不是对模型效果的独立验证。

## 一、Inputs 与标题：先区分人物、速度和编舞

| 编号 | 词汇、音标、词性 | 基本义 → 本文义、搭配与辨析 |
|---|---|---|
| 01 | asymmetric /ˌeɪsɪˈmetrɪk/ adj. | 不对称的。本文指两个人的动作数量和进度不相等，不是人体长得不对称。`asymmetric speed`＝非对称速度安排；名词为 `asymmetry`。 |
| 02 | ratio /ˈreɪʃioʊ/ n. | 比率，强调两个量之间的比例关系。`action-count ratio` 是同一观察时间窗内动作完成数之比；不能把 3:1 偷换为动作幅度之比。 |
| 03 | duo /ˈduːoʊ/ n. | 两人组合、二重奏。`duo choreography` 是为双人关系设计的编舞；不自动意味着两个人同步。 |
| 04 | choreography /ˌkɔːriˈɑːɡrəfi/ n. | 编舞及编排出的动作组织。这里包括谁领舞、谁观察、何时模仿，不只是一串舞步名称。相关动词 `choreograph`＝编排舞蹈。 |
| 05 | identity /aɪˈdentəti/ n. | 身份、个体同一性。`both identities locked` 要求两张脸各自持续对应原来的两个人，不是把两个人合并成一张脸。 |
| 06 | instrumental /ˌɪnstrəˈmentəl/ adj.; n. | 器乐的；器乐曲。`instrumental BGM` 排除歌唱和人声素材，不等于“没有音乐”。本文又用多条否定命令强化无人声条件。 |
| 07 | reference /ˈrefərəns/ n. | 参照、参考资料。`single reference image` 指输入来源只有一张，不是画面里只能有一个人。应区分输入数量与主体数量。 |
| 08 | target /ˈtɑːrɡɪt/ n.; v. | 目标；以……为目标。Inputs 中是目标输出描述，不是已经观测到的生成结果。`target duration` 同样是要求时长。 |

**原句回读：** `Single reference image, both identities locked from it`。
**译文：** 只使用一张参考图，两个人各自的身份都由这张图锁定。这里 `both` 管“两个人的身份”，不管“参考图”。

## 二、The problem：为什么 fast / slow 容易失去差异

| 编号 | 词汇、音标、词性 | 基本义 → 本文义、搭配与辨析 |
|---|---|---|
| 09 | synchronize /ˈsɪŋkrənaɪz/ v. | 使同步。`synchronize dancers to the beat`＝使舞者动作对齐节拍；是时间关系，不是把外观变得一样。 |
| 10 | beat /biːt/ n. | 节拍、拍点。是周期性的时间参照；不等于一整段舞句，也不保证每拍只做一个动作。 |
| 11 | default /dɪˈfɔːlt/ v.; n. | 默认采用；默认值。`default to mirror-sync`＝在缺少更明确约束时倾向采用镜像同步；不是说每次生成都必然如此。 |
| 12 | mirror-sync /ˈmɪrər sɪŋk/ n. phr. | 本文的概括性说法：两人以镜像或近似对应方式同步运动。`mirror` 说明对应关系，`sync` 说明时间对齐，不能只译成“镜子”。 |
| 13 | tempo /ˈtempoʊ/ n. | 音乐或动作推进速度。这里首先是二人被拉到同一运动速度；应与单个动作的位移速度及整曲 BPM 分开。 |
| 14 | downbeat /ˈdaʊnbiːt/ n. | 小节第一拍、下拍。文中与 tempo、phrasing 并列，分别谈速度、主要拍位和分句方式，不能统统译作“节奏”。 |
| 15 | phrasing /ˈfreɪzɪŋ/ n. | 分句、乐句或舞句组织。强调动作如何成组、停连和收束；同一 tempo 下也可以有不同 phrasing。 |
| 16 | brief /briːf/ n. | 创作简报、任务说明。`the brief wanted the opposite` 指原创作要求恰好相反；此处不是形容词“短暂的”。 |
| 17 | continuous /kənˈtɪnjuəs/ adj. | 连续不中断的。形容心海不断衔接下一动作；不直接说明画面是一镜到底，也不等于每个关节始终快速移动。 |
| 18 | delayed /dɪˈleɪd/ adj. | 延迟的、晚发生的。修饰七七的反应或动作开始时间；与 `slow` 的执行速度慢不同，可以同时存在。 |
| 19 | lag /læɡ/ n.; v. | 落后量；滞后。`with a lag` 强調两人动作进度之间存在差距；`lag behind`＝落在……之后。 |
| 20 | round /raʊnd/ v. | 数值语境中取整、近似化。作者用 `rounded them to` 比喻把细致要求压成粗略解释，并非声称模型真的执行了四舍五入算法。 |

**原句回读：** `both bodies lock to the same tempo, the same downbeat, the same phrasing`。
**译文：** 两个人的身体动作被锁到相同的速度、相同的小节拍位以及相同的舞句组织上。三个 `same` 强调三种不同层面的同化。

## 三、The breakthrough：把模糊描述变成可比较关系

| 编号 | 词汇、音标、词性 | 基本义 → 本文义、搭配与辨析 |
|---|---|---|
| 21 | qualitatively /ˈkwɑːləteɪtɪvli/ adv. | 定性地，以性质而非数字描述。`describe tempo qualitatively` 如“很快、很慢”；相对的是可计数的数量关系，不是“质量很高地”。 |
| 22 | explicit /ɪkˈsplɪsɪt/ adj. | 明说的、明确的。`explicit arithmetic anchor` 要求比例直接写出，不由模型从氛围词自行猜测。 |
| 23 | arithmetic /əˈrɪθmətɪk/ adj.; /əˈrɪθmətɪk/ n. | 算术的；算术。这里修饰 anchor，说明参照是动作计数关系；不表示模型会因此拥有严格的计数保证。 |
| 24 | anchor /ˈæŋkər/ n.; v. | 锚；固定参照。这里是用于检查差异的 3:1 计数规则，与相机路径中的空间锚点不是同一个维度。 |
| 25 | convert /kənˈvɜːrt/ v. | 转换。`convert A into B`＝把 A 改写成 B；本文是将审美意图转换成动作数约束，不是转换视频格式。 |
| 26 | aesthetic /esˈθetɪk/ adj. | 审美的。`aesthetic tempo gap` 指观众应感到的速度反差，强调创作目的，而非一个现成测量指标。 |
| 27 | gap /ɡæp/ n. | 间隔、差距。此处是两人速度/进度的差别，不是画面里的物理空隙。`tempo gap` 与 `spatial gap` 必须分别理解。 |
| 28 | checkable /ˈtʃekəbəl/ adj. | 可检查、可核对的。完成三个动作对一个动作比“明显快一些”更方便人工判断，但依然需要定义什么算一个动作。 |
| 29 | count /kaʊnt/ n.; v. | 数量、计数；计数。`a checkable count` 取名词义；`count actions` 取动词义。舞蹈动作计数不能自动等同视频帧数。 |
| 30 | roughly /ˈrʌfli/ adv. | 大约、粗略地。`roughly equal`＝大致相等；在 Result 中修饰 3 倍，显示作者的结果描述不是逐帧精确测量报告。 |

**原句回读：** `This converts an aesthetic tempo gap into a checkable count.`
**译文：** 这样就把一个审美层面的速度反差，改写成了能够检查的动作数量关系。`into` 后面才是转换的结果。

## 四、行为原因：七七不是单纯被限速

| 编号 | 词汇、音标、词性 | 基本义 → 本文义、搭配与辨析 |
|---|---|---|
| 31 | lever /ˈlevər/ n. | 杠杆；引申为可以改变结果的手段。`the second lever` 指第二种提示策略，不是场景中增加机械杠杆。 |
| 32 | behavioral /bɪˈheɪvjərəl/ adj. | 行为层面的。`behavioral motivation` 指可见观察—模仿行为形成的动机，不是在猜测真人心理。 |
| 33 | motivation /ˌmoʊtəˈveɪʃən/ n. | 动机、促成行动的原因。这里给延迟安排一个剧情理由，使落后具有可理解的因果。 |
| 34 | imitate /ˈɪməteɪt/ v. | 模仿已经看到的行为。`watch then imitate` 强调先观察、后执行；不是凭空同时做同一个动作。 |
| 35 | narrative /ˈnærətɪv/ adj.; n. | 叙事的；叙事。`narrative cause` 是故事层面的原因，对比单纯的数值限速。 |
| 36 | arbitrary /ˈɑːrbətreri/ adj. | 任意指定、缺少内在理由的。`arbitrary speed cap` 指只有外部限制却看不出表演原因；不等于随机噪声。 |
| 37 | cap /kæp/ n.; v. | 上限；设置上限。`speed cap` 是速度上限，不取“帽子、盖子”义。与厨房案例的 jar cap 形成同词异义。 |
| 38 | desynchronization /ˌdiːsɪŋkrənaɪˈzeɪʃən/ n. | 去同步、不同步。这里是有意的两人时间错位，而不是音轨意外偏移。动词为 `desynchronize`。 |
| 39 | intentional /ɪnˈtenʃənəl/ adj. | 有意安排的。对比 `broken`，说明观众应把错拍看作创作设计，而不是系统故障。 |
| 40 | dynamic /daɪˈnæmɪk/ n.; adj. | 相互作用关系；动态的。`a master–student dynamic` 取名词义，指领舞者与学习者的关系，不只是“很有动感”。 |

**原句回读：** `she watches Kokomi, then imitates the action she just saw`。
**译文：** 她先看心海，再模仿自己刚才看到的那个动作。`just saw` 的对象是已发生动作，因此与主动预判下一拍相反。

## 五、结论、负向约束与镜头

| 编号 | 词汇、音标、词性 | 基本义 → 本文义、搭配与辨析 |
|---|---|---|
| 41 | specification /ˌspesəfɪˈkeɪʃən/ n. | 明确规格、执行要求。`3:1 count-locked` 被作者当作规格表达；不是宣称它具有软件级形式验证。 |
| 42 | convergence /kənˈvɜːrdʒəns/ n. | 趋同、收敛。本文比喻两人动作向共同节拍靠拢，不是在报告数值优化算法的收敛结果。 |
| 43 | track /træk/ v.; n. | 跟踪、持续掌握；音轨。`a number the model can track` 取动词义；`BGM track` 才指音乐音轨。 |
| 44 | deliberate /dɪˈlɪbərət/ adj. | 有意而审慎安排的。`deliberate asymmetry`＝有设计目的的不对称；与副词 `deliberately`“有意地”区别。 |
| 45 | defective /dɪˈfektɪv/ adj. | 有缺陷的。`rather than defective` 是观感上的对比：有意落后，而非看起来动作出故障。 |
| 46 | catch up /kætʃ ʌp/ v. phr. | 追上既有进度差。`no catching up` 不只禁止瞬间加速，还要求落后关系不能在后半段被消除。 |
| 47 | acceleration /əkˌseləˈreɪʃən/ n. | 加速、速度变化过程。`no sudden acceleration` 禁止七七突然追赶；不是禁止她任何自然的起步或关节速度变化。 |
| 48 | orbit /ˈɔːrbɪt/ n.; v. | 围绕主体运行、环绕拍摄。镜头位置绕二人改变，区别于相机原地转向的 pan，也区别于绕光轴的 roll。 |
| 49 | framing /ˈfreɪmɪŋ/ n. | 取景范围及画面组织。`waist-to-head framing` 明确人体覆盖范围，比仅说“近一点”更具体；不等于帧率。 |
| 50 | sustained /səˈsteɪnd/ adj. | 持续维持的。`sustained from first second to last` 要求速度差贯穿全片，不是只在某一个展示镜头成立。 |

**原句回读：** `Lag with motivation reads as choreography. Lag without motivation reads as a bug.`
**译文：** 有行动原因的滞后会被看作编舞；没有行动原因的滞后则会被看作错误。`read as` 在这里是“被观众理解为”，不是“朗读”。

## 六、必须一起记住的三组差别

**slow / delayed / lagging：** slow 描述执行速度慢；delayed 描述开始或响应较晚；lagging 描述相对另一人的进度落后。原文希望这几种关系共同产生效果，不能只用一个“慢”概括。

**tempo / beat / phrasing：** tempo 是推进速度，beat 是时间拍点，phrasing 是动作/音乐如何成句。两个人可以听同一首音乐，却完成不同数量的动作。

**identity lock / motion freeze：** 锁定身份是维持谁是谁，不是把人物冻住。这里双人身份不变，但身体动作必须不断发展。

## 校读边界

README 中关于模型“不能把 3:1 变成相等”等句子属于作者的经验性论断。学习时应掌握其表达方式，但不能把自然语言约束理解为保证计数正确的执行器。`3 actions` 的动作边界仍需在实际检查中明确。本次只增补词汇与语言理解，不重新认定成片是否达到比例。
