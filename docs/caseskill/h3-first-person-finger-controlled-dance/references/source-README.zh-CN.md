# 案例研究 008 — 单图第一人称手指控制舞蹈｜逐段翻译

> 对应原始 `README.md`。按段落顺序处理：每段先列关键词、术语和概念（IPA、词性缩写、简体中文释义），再给出整段简体中文译文。基础词汇、介词、冠词、数词等不重复释义。

## Inputs｜输入

### 段落 1
**原文：** `<Picture 1>` — The ONLY visual reference. Locks dancer's appearance, face, hairstyle, costume, environment, lighting, and the original high-angle smartphone perspective

**关键词与术语：**
- visual reference /ˈvɪʒuəl ˈrefrəns/ n. phr.：视觉参考
- lock /lɑːk/ v.：锁定；稳定保持
- appearance /əˈpɪrəns/ n.：外观
- high-angle /ˌhaɪ ˈæŋɡəl/ adj.：高机位俯拍角度
- smartphone perspective /ˈsmɑːrtfoʊn pərˈspektɪv/ n. phr.：手机摄影透视关系

**整段翻译：**  
`<Picture 1>` 是**唯一视觉参考**。它负责锁定舞者的外观、脸、发型、服装、环境、光照，以及原图中的高机位手机摄影透视。

### 段落 2
**原文：** Target: vertical 9:16 first-person smartphone recording, continuous single shot

**关键词与术语：**
- first-person /ˌfɜːrst ˈpɜːrsən/ adj.：第一人称的
- continuous single shot /kənˈtɪnjuəs ˈsɪŋɡəl ʃɑːt/ n. phr.：连续单镜头

**整段翻译：**  
目标：9:16 竖屏第一人称手机拍摄，一镜到底连续镜头。

### 段落 3
**原文：** Prompt language: **English** (descriptive blocks + literal command clauses)

**关键词与术语：**
- descriptive block /dɪˈskrɪptɪv blɑːk/ n. phr.：描述性模块
- literal command clause /ˈlɪtərəl kəˈmænd klɔːz/ n. phr.：字面命令条款；明确且可直接执行的规则句

**整段翻译：**  
提示词语言：**英文**，由描述性模块与字面命令条款组成。

### 段落 4
**原文：** Output: short-form viral dance video controlled by a foreground finger

**关键词与术语：**
- short-form /ˌʃɔːrt ˈfɔːrm/ adj.：短视频形式的
- viral /ˈvaɪrəl/ adj.：具有传播性、短视频爆款风格的
- foreground /ˈfɔːrɡraʊnd/ n.：前景

**整段翻译：**  
输出目标：由前景手指控制人物动作的短视频爆款风格舞蹈视频。

## Media files｜媒体文件

### 段落 5
**原文：** Original AnimateDiff补帧 demo clip used as the visual reference source

**关键词与术语：**
- demo clip /ˈdemoʊ klɪp/ n. phr.：演示视频片段
- visual reference source /ˈvɪʒuəl ˈrefrəns sɔːrs/ n. phr.：视觉参考来源

**整段翻译：**  
`reference-dance-demo.mp4` 是原始 AnimateDiff 补帧演示片段，用作视觉参考来源。

## What this prompt solves｜这个提示词解决什么问题

### 段落 6
**原文：** A solo dancer + a controlling hand in the same frame, and the hand must visibly *cause* the dance.

**关键词与术语：**
- solo dancer /ˈsoʊloʊ ˈdænsər/ n. phr.：单人舞者
- controlling hand /kənˈtroʊlɪŋ hænd/ n. phr.：控制手
- visibly cause /ˈvɪzəbli kɔːz/ v. phr.：以肉眼可见的因果关系触发

**整段翻译：**  
画面中同时存在一名舞者和一只控制她的手，而且必须让观众明确看出：**手的动作会直接导致舞者动作发生**。

### 段落 7
**原文：** Two problems collide here. **First**, the model's prior for "dance" is to freelance — once a dancer is on screen, the model improvises choreography it considers aesthetically pleasing, ignoring any external cue. **Second**, a hand in the foreground is almost always a problem: H3 will either grow it to dominate the frame, slide it across the center to cover the face, or shrink it to a barely visible background element. None of these work when the hand is supposed to be the puppeteer.

**关键词与术语：**
- model prior /ˈmɑːdəl ˈpraɪər/ n. phr.：模型先验倾向
- freelance /ˈfriːlæns/ v.：自由发挥；不再严格服从控制
- improvise /ˈɪmprəvaɪz/ v.：即兴生成
- choreography /ˌkɔːriˈɑːɡrəfi/ n.：编舞
- external cue /ɪkˈstɜːrnəl kjuː/ n. phr.：外部提示信号
- dominate the frame /ˈdɑːmɪneɪt ðə freɪm/ v. phr.：占据画面主导
- puppeteer /ˌpʌpɪˈtɪr/ n.：操偶者；控制动作的人

**整段翻译：**  
这里有两个问题同时发生。**第一**，模型对“跳舞”的默认先验是自由发挥——只要舞者出现在画面里，模型就会自行即兴编舞，优先选择它认为好看的动作，而忽视外部控制信号。**第二**，前景手部本身也极易失控：H3 可能把它放大到压倒画面，也可能让它滑到中央遮住脸，或者反过来把它缩小成几乎看不见的背景元素。如果这只手承担的是“操偶者”职责，这三种结果都不可接受。

### 段落 8
**原文：** The third hidden problem: most prompt authors would write a list of dance moves (hip sway, arm wave, hair flip) and let the model sequence them. That fails because the model doesn't *see* a connection between the hand in the foreground and the dancer's body, so the two drift out of sync, or the hand disappears during the most important beat.

**关键词与术语：**
- hidden problem /ˈhɪdən ˈprɑːbləm/ n. phr.：隐性问题
- hip sway /hɪp sweɪ/ n. phr.：摆胯
- arm wave /ɑːrm weɪv/ n. phr.：手臂波浪动作
- hair flip /her flɪp/ n. phr.：甩发
- sequence /ˈsiːkwəns/ v.：按顺序排列动作
- drift out of sync /drɪft aʊt əv sɪŋk/ v. phr.：逐渐失去同步

**整段翻译：**  
第三个隐藏问题是：很多提示词作者会直接列一串舞蹈动作，比如摆胯、挥臂、甩发，然后让模型自己排序。但这样会失败，因为模型并不会自动理解前景手与舞者身体之间存在因果关系；结果往往是两者逐渐失去同步，或者在最关键的节拍处，手甚至直接消失。

## The breakthrough｜关键突破

### 段落 9
**原文：** State the control relationship as a literal mapping, then forbid alternatives.

**关键词与术语：**
- control relationship /kənˈtroʊl rɪˈleɪʃənʃɪp/ n. phr.：控制关系
- literal mapping /ˈlɪtərəl ˈmæpɪŋ/ n. phr.：字面映射；明确的一对一输入输出规则
- forbid /fərˈbɪd/ v.：禁止

**整段翻译：**  
把控制关系写成**明确的一对一映射**，然后禁止其他解释。

### 段落 10
**原文：** The prompt establishes an explicit, one-to-one control grammar at the top:

**关键词与术语：**
- explicit /ɪkˈsplɪsɪt/ adj.：明确的
- one-to-one /ˌwʌn tə ˈwʌn/ adj.：一对一的
- control grammar /kənˈtroʊl ˈɡræmər/ n. phr.：控制语法

**整段翻译：**  
提示词在最前面建立一套明确的一对一控制语法：

```
UP → WOMAN RISES.
DOWN → WOMAN LOWERS.
LEFT → WOMAN MOVES LEFT.
RIGHT → WOMAN MOVES RIGHT.
```

对应中文：  
向上 → 女性身体上升。  
向下 → 女性身体下降。  
向左 → 女性身体向左移动。  
向右 → 女性身体向右移动。

### 段落 11
**原文：** Each direction is then given a paragraph defining exactly how the body responds (torso extension for UP, hip drop for DOWN, full-body weight shift for LEFT/RIGHT) and — crucially — a negative clause: `LEFT and RIGHT must not become tiny hip twitches`. Without this, the model would interpret "left/right movement" as subtle hip sways. The prompt forces a *visible full-body shift*.

**关键词与术语：**
- torso extension /ˈtɔːrsoʊ ɪkˈstenʃən/ n. phr.：躯干向上伸展
- hip drop /hɪp drɑːp/ n. phr.：髋部下沉
- weight shift /weɪt ʃɪft/ n. phr.：重心转移
- negative clause /ˈneɡətɪv klɔːz/ n. phr.：负向条款
- twitch /twɪtʃ/ n.：细小抽动
- subtle hip sway /ˈsʌtl hɪp sweɪ/ n. phr.：轻微摆胯
- full-body shift /ˌfʊl ˈbɑːdi ʃɪft/ n. phr.：全身整体位移

**整段翻译：**  
然后，每个方向都用一个段落精确定义身体怎样响应：UP 对应躯干伸展，DOWN 对应髋部下沉，LEFT / RIGHT 对应全身重心与位置发生左右转移。尤其关键的是，还加入一条负向限制：`LEFT and RIGHT must not become tiny hip twitches`，也就是左右动作绝不能退化成很小的摆胯抽动。没有这条约束，模型很容易把“向左 / 向右移动”理解成轻微的胯部摆动。提示词要求的是**肉眼可见的全身位移**。

### 段落 12
**原文：** The same anti-drift logic applies to the hand itself:

**关键词与术语：**
- anti-drift /ˌænti ˈdrɪft/ adj.：防漂移的；防止主体位置和功能逐渐偏离设定

**整段翻译：**  
同样的防漂移逻辑也作用在手本身：

- 手必须是前臂 / 手腕 / 手掌 / 手指连续连接的真实结构，禁止漂浮的“幽灵手”；
- 只能出现在右下象限，占画面面积约 10–18%，既不能变成巨手，也不能缩成细小一条；
- 手不能横跨画面中央，不能遮挡人物脸或躯干。

### 段落 13
**原文：** The dance description is intentionally generic — `confident, sexy viral short-form influencer dance` — because the prompt's purpose is the *control contract*, not the choreography. The usage note at the top of the article tells the user: swap the dance style freely, swap the command sequence freely, but never break the finger-to-body mapping.

**关键词与术语：**
- intentionally generic /ɪnˈtenʃənəli dʒəˈnerɪk/ adj. phr.：有意保持泛化
- influencer dance /ˈɪnfluənsər dæns/ n. phr.：短视频博主式舞蹈
- control contract /kənˈtroʊl ˈkɑːntrækt/ n. phr.：控制契约
- command sequence /kəˈmænd ˈsiːkwəns/ n. phr.：命令序列
- finger-to-body mapping /ˈfɪŋɡər tə ˈbɑːdi ˈmæpɪŋ/ n. phr.：手指动作到身体动作的映射

**整段翻译：**  
舞蹈风格描述被有意保持得很泛化，例如 `confident, sexy viral short-form influencer dance`（自信、性感、短视频爆款博主风舞蹈），因为本提示词真正需要锁定的是**控制契约**，而不是某套固定编舞。文首使用说明明确告诉用户：舞蹈风格可以自由替换，命令序列也可以自由替换，但绝不能破坏“手指动作 → 身体动作”的一对一映射。

### 段落 14｜Technique stack

**关键词与术语：**
- quota /ˈkwoʊtə/ n.：配额；规定可占用的空间比例
- composition lock /ˌkɑːmpəˈzɪʃən lɑːk/ n. phr.：构图锁定
- reaction delay /riˈækʃən dɪˈleɪ/ n. phr.：反应延迟
- anticipation /ænˌtɪsɪˈpeɪʃən/ n.：提前动作
- modular /ˈmɑːdʒələr/ adj.：模块化的
- triplet /ˈtrɪplət/ n.：三连结构

| 技术 | 中文作用 |
|---|---|
| **Literal Control Mapping** | UP / DOWN / LEFT / RIGHT 与身体方向动作建立一对一对应 |
| **Directional Anti-Twitch Clause** | 禁止 LEFT / RIGHT 被解释成小幅摆胯 |
| **Foreground Element Quota** | 前景手只占 10–18% 画面，并固定在右下象限 |
| **No-Drift Composition Locks** | 摄影机距离 1.0–1.2m，人物占画面 70–80%，禁止拉远 |
| **Sync-Within-Beat Rule** | 禁止反应延迟、落后一拍或提前动作 |
| **Command Sequence Table** | 预设 10 拍命令序列：UP→DOWN→L→R→L→R→UP→DOWN→L→R |
| **Modular Dance Section** | 舞蹈风格只是可替换描述，不是硬编码编舞 |
| **Closing Triplet Pose** | 最后以 L→R→UP 三连动作进入并保持终止姿态 |

## The named language｜命名语言

### 段落 15
**原文：** **Finger-Controlled First-Person Dance**

**关键词与术语：**
- finger-controlled /ˈfɪŋɡər kənˈtroʊld/ adj.：由手指控制的
- first-person /ˌfɜːrst ˈpɜːrsən/ adj.：第一人称的

**整段翻译：**  
**手指控制的第一人称舞蹈**

### 段落 16
**原文：** The name encodes the three things that make this prompt work: the hand is the *controller* (not a prop), the camera is *first-person* (not a third-party observer), and the dancer is *in the shot* (not a stock figure pasted in). Lose any of these and the prompt collapses into either an unconstrained dance video or a hand-in-foreground demo with no relationship between them.

**关键词与术语：**
- encode /ɪnˈkoʊd/ v.：编码；把核心约束浓缩在名称中
- controller /kənˈtroʊlər/ n.：控制者
- prop /prɑːp/ n.：道具
- third-party observer /ˌθɜːrd ˈpɑːrti əbˈzɜːrvər/ n. phr.：第三方观察者
- stock figure /stɑːk ˈfɪɡjər/ n. phr.：素材化、无上下文的人物
- unconstrained /ˌʌnkənˈstreɪnd/ adj.：缺乏约束的

**整段翻译：**  
这个名称编码了提示词成立所依赖的三件事：手必须是**控制器**而不是普通道具；摄影机必须是**第一人称**而不是第三方观察者；舞者必须真实处于这个镜头关系中，而不是后来贴进去的素材人物。三者缺一，提示词都会退化成普通、不受控制的舞蹈视频，或者变成“前景有一只手但与舞者毫无关系”的演示片。

## 48-hour takeaway｜48 小时后的关键结论

### 段落 17
**原文：** When a prompt has two visible actors, name their *relationship* explicitly.

**关键词与术语：**
- actor /ˈæktər/ n.：行动主体；画面中会产生动作的主体
- explicitly /ɪkˈsplɪsɪtli/ adv.：明确地

**整段翻译：**  
当一个提示词中存在两个可见的行动主体时，必须把它们之间的**关系**明确写出来。

### 段落 18
**原文：** Most prompt authors describe each actor's appearance and actions separately and hope the model connects them. It doesn't. A dancer description and a hand description, written in isolation, become two independent scenes that happen to share a frame. The connection only appears if the prompt *itself* contains the connection — and the simplest way to write a connection is a literal mapping: hand goes up, body goes up; hand goes left, body goes left.

**关键词与术语：**
- in isolation /ɪn ˌaɪsəˈleɪʃən/ adv. phr.：彼此孤立地
- independent scene /ˌɪndɪˈpendənt siːn/ n. phr.：彼此独立的场景逻辑
- literal mapping /ˈlɪtərəl ˈmæpɪŋ/ n. phr.：字面映射

**整段翻译：**  
很多作者会分别描述每个主体的外观和动作，然后期待模型自动把二者联系起来，但模型往往不会这样做。孤立书写的“舞者描述”和“手部描述”会变成两个恰好共享同一个画面的独立场景。只有当提示词本身明确写出两者联系时，因果关系才会稳定出现。最简单的写法就是字面映射：手向上，身体向上；手向左，身体向左。

### 段落 19
**原文：** **1. Define each direction with a body response, not just a label.** "LEFT means the body moves left" is too abstract. Specify the body parts that move: weight, torso, hips — and how. The model will follow mechanics more reliably than abstract directions.

**关键词与术语：**
- body response /ˈbɑːdi rɪˈspɑːns/ n. phr.：身体响应
- mechanics /məˈkænɪks/ n.：动作机制；具体身体运动关系
- abstract direction /ˈæbstrækt dəˈrekʃən/ n. phr.：抽象方向指令

**整段翻译：**  
**1. 每个方向都要定义对应的身体响应，而不能只写方向标签。** “LEFT 表示身体向左”仍然过于抽象。应该明确写出哪些身体部位移动——重心、躯干、髋部——以及怎样移动。相比抽象方向，模型对具体动作机制的遵从度更高。

### 段落 20
**原文：** **2. Negate the cheap interpretation.** "LEFT/RIGHT must not become tiny hip twitches" prevents the model from satisfying the prompt with the easiest possible interpretation. Always include the wrong-but-allowed version in the negative list.

**关键词与术语：**
- cheap interpretation /tʃiːp ɪnˌtɜːrprɪˈteɪʃən/ n. phr.：最低成本解释；模型最容易用来“勉强满足”指令的实现
- satisfy /ˈsætɪsfaɪ/ v.：满足约束
- wrong-but-allowed /rɔːŋ bət əˈlaʊd/ adj. phr.：语义上不理想但未被禁止的
- negative list /ˈneɡətɪv lɪst/ n. phr.：负向约束列表

**整段翻译：**  
**2. 主动否定最低成本解释。** “LEFT / RIGHT 不能变成细小摆胯抽动”会阻止模型用最容易的方式敷衍满足提示词。凡是“形式上不算违反、但实际效果错误”的实现，都应该明确写入负向列表。

### 段落 21
**原文：** **3. Quota the foreground element.** A 10–18% area constraint for the hand prevents both the "giant hand" failure (model inflates the controller) and the "barely visible hand" failure (model shrinks it). Specifying the range is much more reliable than saying "natural size."

**关键词与术语：**
- area constraint /ˈeriə kənˈstreɪnt/ n. phr.：画面面积约束
- inflate /ɪnˈfleɪt/ v.：异常放大
- barely visible /ˈberli ˈvɪzəbl/ adj. phr.：几乎不可见
- specify /ˈspesɪfaɪ/ v.：明确规定

**整段翻译：**  
**3. 给前景元素规定面积配额。** 把手限定在画面 10–18% 的面积范围，可以同时避免“巨手”失败——模型把控制手异常放大——以及“几乎看不见的手”失败——模型把它缩得过小。明确指定范围，比只说“自然大小”可靠得多。

## The final prompt｜最终提示词

### 段落 22
**原文：** See `prompt.md` for the full usage notes + ready-to-paste prompt.

**关键词与术语：**
- ready-to-paste /ˌredi tə ˈpeɪst/ adj.：可直接复制使用的

**整段翻译：**  
完整使用说明与可直接复制使用的提示词见 `prompt.md`；本目录的 `prompt.zh-CN.md` 提供英文主体的逐段精读翻译。

### 段落 23
**原文：** The prompt file is organized as:

**整段翻译：**  
提示词文件按以下结构组织：

1. **Usage notes｜使用说明**（中文）—— 单图工作流、可替换舞蹈风格、不可破坏的控制规则
2. **integrated_multimodal_description** —— Picture 1 参考范围、高机位 POV、手部面积配额、身体距离锁
3. **Control grammar｜控制语法** —— UP / DOWN / LEFT / RIGHT 与身体响应定义
4. **Anti-twitch / anti-drift clauses｜防抽动 / 防漂移条款** —— 分别约束身体与手
5. **Dance style description｜舞蹈风格描述** —— 泛化的短视频舞蹈词汇，可替换
6. **Command sequence｜命令序列** —— 硬编码的 10 拍序列
7. **Closing triplet｜收尾三连** —— L → R → UP 最终姿态
8. **Soundscape + music｜声场与音乐** —— 室内环境声 + 短视频舞曲

## Result｜结果

### 段落 24
**原文：** A continuous first-person smartphone recording, locked to the high-angle perspective of Picture 1:

**关键词与术语：**
- locked to /lɑːkt tuː/ adj. phr.：锁定到；保持一致

**整段翻译：**  
最终得到一条连续第一人称手机录像，并锁定 Picture 1 的高机位透视：

- 右下前景有一只手，清晰做出 UP / DOWN / LEFT / RIGHT 手势；
- 舞者立即根据每个手势做完整身体响应：上升、下沉、向左整体位移、向右整体位移；
- 没有幽灵手、漂浮手指、手遮脸、舞者过远等问题；
- 一共 10 组手势—身体动作配对，并以一个保持住的自信姿态结束；
- 音乐使用节拍强烈的短视频舞曲，并与手势发生时点同步。

## Tags｜标签

**中文对应：**  
`#H3` `#提示词工程` `#第一人称POV` `#手指控制` `#舞蹈` `#短视频` `#单图` `#控制映射` `#防漂移` `#爆款舞蹈` `#中文教程`
