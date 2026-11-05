# 案例研究 002 — 非对称速度比例双人编舞｜逐段翻译

> 对应原始 `README.md`。按原文段落顺序处理：先列关键词、术语和概念（IPA、词性缩写、简体中文释义），再给出整段简体中文译文。基础词汇、介词、冠词、数词等不重复释义。

## Inputs｜输入

### 段落 1
**原文：** `<Picture 1>` — Two characters together: Kokomi (left) and Qiqi (right)

**关键词与术语：**
- character /ˈkærəktər/ n.：角色；画面中的人物主体
- Kokomi /koʊˈkoʊmi/ n.：心海，角色名
- Qiqi /ˈtʃiːtʃiː/ n.：七七，角色名

**整段翻译：**  
`<Picture 1>` 中同时出现两名角色：心海在左侧，七七在右侧。

### 段落 2
**原文：** Single reference image, both identities locked from it

**关键词与术语：**
- reference image /ˈrefrəns ˈɪmɪdʒ/ n. phr.：参考图像
- identity lock /aɪˈdentəti lɑːk/ n. phr.：身份锁定；固定角色脸部与人物身份特征

**整段翻译：**  
只使用一张参考图，并从这张图中同时锁定两个人物的身份。

### 段落 3
**原文：** Target: butterfly-step dance to instrumental BGM (Paradise-style)

**关键词与术语：**
- butterfly step /ˈbʌtərflaɪ step/ n. phr.：蝴蝶步；一种轻快、交替移步的舞步
- instrumental BGM /ˌɪnstrəˈmentl ˌbiː dʒiː ˈem/ n. phr.：纯器乐背景音乐
- Paradise-style /ˈpærədaɪs staɪl/ adj. phr.：极乐净土式风格；此处指音乐与舞蹈节奏参考

**整段翻译：**  
目标：让人物配合“极乐净土”风格的纯器乐 BGM 跳蝴蝶步舞蹈。

### 段落 4
**原文：** Prompt language: **Chinese**

**关键词与术语：**
- prompt language /prɑːmpt ˈlæŋɡwɪdʒ/ n. phr.：提示词使用语言

**整段翻译：**  
提示词语言：**中文**。

## The problem｜问题

### 段落 5
**原文：** H3 synchronizes dancers to the beat.

**关键词与术语：**
- synchronize /ˈsɪŋkrənaɪz/ v.：同步；使动作与某一节拍一致
- beat /biːt/ n.：音乐节拍

**整段翻译：**  
H3 会倾向于让舞者动作与音乐节拍同步。

### 段落 6
**原文：** Give the model two people and music, and it defaults to mirror-sync: both bodies lock to the same tempo, the same downbeat, the same phrasing. The brief wanted the opposite — Kokomi fast and continuous, Qiqi slow and delayed, a "master leads, student follows with a lag" dynamic. But "fast" and "slow" are adjectives. The model rounded them to "same speed, slightly different."

**关键词与术语：**
- mirror-sync /ˈmɪrər sɪŋk/ n. phr.：镜像同步；两个人物以近似相同节奏同步运动
- tempo /ˈtempoʊ/ n.：速度；音乐整体节奏速度
- downbeat /ˈdaʊnbiːt/ n.：强拍；小节中的主要落点
- phrasing /ˈfreɪzɪŋ/ n.：乐句组织；动作与音乐句法的分段方式
- delayed /dɪˈleɪd/ adj.：延迟的；滞后的
- lag /læɡ/ n.：时间滞后
- round /raʊnd/ v.：近似化；把差异收敛到更接近的状态

**整段翻译：**  
只要给模型两个人和一段音乐，它就很容易默认进入“镜像同步”状态：两个人的身体锁定到相同速度、相同强拍与相同乐句节奏上。但这个任务需要的恰恰相反——心海快速且连续，七七明显更慢并持续滞后，形成“师傅在前面带，学生延迟跟学”的动态。问题在于，“快”和“慢”只是形容词。模型很容易把这种区别近似化成“速度基本一样，只存在轻微差异”。

## The breakthrough｜关键突破

### 段落 7
**原文：** Speed difference is not a feeling. It is a **ratio**.

**关键词与术语：**
- speed difference /spiːd ˈdɪfrəns/ n. phr.：速度差
- ratio /ˈreɪʃioʊ/ n.：比例；可明确计算的数量关系

**整段翻译：**  
速度差不能只写成一种“感觉”，而应当写成一个明确的**比例**。

### 段落 8
**原文：** Instead of describing tempo qualitatively, the prompt gives the model an explicit arithmetic anchor:

**关键词与术语：**
- qualitatively /ˈkwɑːləteɪtɪvli/ adv.：定性地；只描述性质而不量化
- explicit /ɪkˈsplɪsɪt/ adj.：明确写出的
- arithmetic anchor /əˈrɪθmətɪk ˈæŋkər/ n. phr.：算术锚点；用数字关系固定生成规则

**整段翻译：**  
与其定性描述节奏快慢，不如在提示词中直接给模型一个明确的算术锚点：

> 当心海已经完成 **3 个动作**时，七七只完成 **1 个动作**。

### 段落 9
**原文：** This converts an aesthetic tempo gap into a checkable count. The model cannot round "3:1" to "roughly equal." It has to hold the asymmetry or visibly fail the rule.

**关键词与术语：**
- aesthetic /esˈθetɪk/ adj.：审美层面的；视觉与节奏体验上的
- tempo gap /ˈtempoʊ ɡæp/ n. phr.：节奏速度差
- checkable count /ˈtʃekəbl kaʊnt/ n. phr.：可核验的计数
- asymmetry /ˌeɪˈsɪmətri/ n.：非对称性
- visibly fail /ˈvɪzəbli feɪl/ v. phr.：以肉眼可见的方式违反规则

**整段翻译：**  
这就把一种审美上的速度差，转换成可核验的动作计数。模型无法轻易把“3:1”模糊成“差不多一样快”；它要么持续维持这种非对称关系，要么就会明显违反规则。

### 段落 10
**原文：** The second lever is **behavioral motivation**. Qiqi isn't just "slow" — she watches Kokomi, then imitates the action she just saw. This gives the lag a narrative cause rather than an arbitrary speed cap, which makes the desynchronization feel intentional instead of broken.

**关键词与术语：**
- lever /ˈlevər/ n.：杠杆；用于控制模型行为的关键手段
- behavioral motivation /bɪˈheɪvjərəl ˌmoʊtəˈveɪʃən/ n. phr.：行为动机；动作为什么发生的叙事理由
- imitate /ˈɪmɪteɪt/ v.：模仿
- narrative cause /ˈnærətɪv kɔːz/ n. phr.：叙事原因
- arbitrary /ˈɑːrbətreri/ adj.：任意设定的；缺乏因果理由的
- speed cap /spiːd kæp/ n. phr.：速度上限
- desynchronization /diːˌsɪŋkrənaɪˈzeɪʃən/ n.：去同步；故意维持不同步状态

**整段翻译：**  
第二个关键手段是**行为动机**。七七不能只是抽象地“慢”，而是先看心海做动作，然后再模仿她刚刚看到的动作。这样，滞后就具有了叙事原因，而不只是一个任意设置的速度上限；因此，两人不同步会显得是有意设计的编舞，而不是生成出了问题。

### 段落 11｜Technique stack
**原文：** The technique stack:

**关键词与术语：**
- technique stack /tekˈniːk stæk/ n. phr.：技术栈；共同作用的一组提示词控制方法

**整段翻译：**  
本案例使用的技术栈如下：

| 技术 | 中文作用 |
|---|---|
| **Count-Ratio Anchor** | 动作计数 3:1；模型必须维持的具体数值规则 |
| **Watch-Then-Imitate Logic** | 为较慢的主体提供“先看、后模仿”的滞后理由 |
| **Asymmetric Speed Choreography** | 整体时间结构上的非对称速度编舞 |
| **Close-Range Continuous Orbit** | 摄影机持续近距离环绕，并始终兼顾两张脸 |

## The named language｜命名语言

### 段落 12
**原文：** **Asymmetric Speed-Ratio Duo Choreography**

**关键词与术语：**
- asymmetric /ˌeɪsɪˈmetrɪk/ adj.：非对称的
- speed-ratio /spiːd ˈreɪʃioʊ/ n. phr.：速度比例
- duo choreography /ˈduːoʊ ˌkɔːriˈɑːɡrəfi/ n. phr.：双人编舞

**整段翻译：**  
**非对称速度比例双人编舞**

### 段落 13
**原文：** Naming the pattern as a *ratio* rather than a *feeling* is the key. "One fast, one slow" is subjective. "3:1 count-locked" is a specification.

**关键词与术语：**
- pattern /ˈpætərn/ n.：模式；可复用结构
- subjective /səbˈdʒektɪv/ adj.：主观的；缺乏固定量化标准的
- count-locked /kaʊnt lɑːkt/ adj.：按计数锁定的
- specification /ˌspesɪfɪˈkeɪʃən/ n.：规格；可执行的明确约束

**整段翻译：**  
关键在于，把这个模式命名为一种“比例”，而不是一种“感觉”。“一个快、一个慢”仍然是主观描述；“按照 3:1 的动作计数锁定”则是一条明确规格。

## 48-hour takeaway｜48 小时后的关键结论

### 段落 14
**原文：** Adjectives don't survive generation. "Fast" becomes "normal." "Slow" becomes "normal." The model's default is convergence toward the beat.

**关键词与术语：**
- adjective /ˈædʒɪktɪv/ n.：形容词
- survive generation /sərˈvaɪv ˌdʒenəˈreɪʃən/ v. phr.：在生成过程中稳定保留下来
- convergence /kənˈvɜːrdʒəns/ n.：收敛；逐渐趋向同一状态

**整段翻译：**  
形容词很难在生成过程中稳定保留。“快”容易被模型拉回“正常速度”，“慢”也容易被拉回“正常速度”。模型的默认倾向，是让人物动作逐渐向音乐节拍收敛。

### 段落 15
**原文：** To hold a visible difference, convert the aesthetic intent into a **number the model can track**. A 3:1 action-count ratio is harder to ignore than "one person is faster." And to make the asymmetry feel deliberate rather than defective, give the slower subject a **reason** — she's watching, then copying. Lag with motivation reads as choreography. Lag without motivation reads as a bug.

**关键词与术语：**
- aesthetic intent /esˈθetɪk ɪnˈtent/ n. phr.：审美意图
- track /træk/ v.：持续追踪；在生成过程中保持计数
- deliberate /dɪˈlɪbərət/ adj.：有意设计的
- defective /dɪˈfektɪv/ adj.：看起来像错误或缺陷的
- choreography /ˌkɔːriˈɑːɡrəfi/ n.：编舞
- bug /bʌɡ/ n.：错误；异常表现

**整段翻译：**  
要稳定维持一种肉眼可见的差异，就应把审美意图转换为一个**模型可以持续追踪的数字**。相比“一个人更快”，3:1 的动作计数比例更难被模型忽略。同时，为了让这种非对称看起来是有意设计而不是生成缺陷，还要给较慢的人物一个明确**理由**——她先观察，再模仿。有动机的滞后会被观众理解为编舞；没有动机的滞后，则更像错误。

## The final prompt｜最终提示词

### 段落 16
**原文：** See `prompt.md` for the full prompt (Chinese, ~170 lines).

**关键词与术语：**
- full prompt /fʊl prɑːmpt/ n. phr.：完整提示词

**整段翻译：**  
完整提示词请参见 `prompt.md`（中文，约 170 行）。

### 段落 17
**原文：** The prompt is organized in this order:

**关键词与术语：**
- organize /ˈɔːrɡənaɪz/ v.：组织；按照固定结构排列

**整段翻译：**  
提示词按以下顺序组织：

1. **Reference lock｜参考锁定** —— Picture 1 是唯一参考，两个人物身份均被冻结
2. **Dance type｜舞蹈类型** —— 蝴蝶步、轻快脚步、左右移动
3. **Asymmetric speed rule｜非对称速度规则** —— 心海快速连续，七七缓慢、一次一个动作
4. **Count-ratio anchor｜计数比例锚点** —— 明确写出 3:1 动作数量规格
5. **Behavioral logic｜行为逻辑** —— 七七先观察，再延迟模仿
6. **Negative constraints｜负向约束** —— 禁止同步、禁止追上、禁止突然加速
7. **Camera｜摄影机** —— 近距离连续环绕，腰部到头顶构图
8. **Audio｜声音** —— 仅纯器乐 BGM，禁止人声

## Result｜结果

### 段落 18
**原文：** A duo dance where Kokomi completes roughly 3 butterfly-step actions for every 1 that Qiqi completes, sustained from first second to last, with Qiqi visibly watching and lagging behind throughout.

**关键词与术语：**
- roughly /ˈrʌfli/ adv.：大约；近似维持
- sustain /səˈsteɪn/ v.：持续维持
- visibly /ˈvɪzəbli/ adv.：以肉眼明显可见的方式
- lag behind /læɡ bɪˈhaɪnd/ v. phr.：明显落后

**整段翻译：**  
最终得到一段双人舞：心海每完成大约 3 个蝴蝶步动作，七七只完成约 1 个；这种比例从第一秒持续到最后一秒，并且七七全程都能明显看出是在观察心海、持续落后于心海。

## Tags｜标签

**关键词与术语：**
- prompt engineering /prɑːmpt ˌendʒɪˈnɪrɪŋ/ n.：提示词工程
- choreography /ˌkɔːriˈɑːɡrəfi/ n.：编舞
- desynchronization /diːˌsɪŋkrənaɪˈzeɪʃən/ n.：去同步

**中文对应：**  
`#H3` `#提示词工程` `#编舞` `#非对称速度` `#计数比例` `#双人舞` `#去同步` `#蝴蝶步`
