# 案例研究 007 — 连续 BGM 的两段式电影感角色揭示

> 本文件按原文段落顺序翻译。每一段先列出需要重点理解的关键词、术语或概念（IPA、词性缩写、简体中文释义），再给出整段简体中文译文。基础词汇、介词、冠词、数词等不重复列出。

## Inputs｜输入

### 段落 1
**原文：** `<Picture 1>` — Same character's complete pose library, body, costume, hairstyle, accessories, church environment, all photographed poses

**关键词与术语：**
- pose library /poʊz ˈlaɪbreri/ n. phr.：姿态库；供模型复用的一组已批准人物姿势参考
- costume /ˈkɑːstuːm/ n.：服装；角色造型服饰
- hairstyle /ˈherstaɪl/ n.：发型
- accessories /əkˈsesəriz/ n.：配饰
- photographed poses /ˈfoʊtəɡræft ˈpoʊzɪz/ n. phr.：已经拍摄得到的姿态

**整段翻译：**  
`<Picture 1>` = 同一角色的完整姿态库，以及该角色的身体、服装、发型、配饰、教堂环境和全部已拍摄姿态。

### 段落 2
**原文：** `<Picture 2>` — The ONLY facial identity reference for the same character

**关键词与术语：**
- facial identity /ˈfeɪʃəl aɪˈdentəti/ n. phr.：面部身份；用于稳定人物脸部一致性的身份特征
- reference /ˈrefrəns/ n.：参考；参考图
- identity reference /aɪˈdentəti ˈrefrəns/ n. phr.：身份参考

**整段翻译：**  
`<Picture 2>` = 同一角色唯一的人脸身份参考。

### 段落 3
**原文：** Plus supplementary pose references in the same scene

**关键词与术语：**
- supplementary /ˌsʌplɪˈmentəri/ adj.：补充的；辅助性的
- pose reference /poʊz ˈrefrəns/ n. phr.：姿态参考

**整段翻译：**  
另外还包含同一场景中的补充姿态参考图。

### 段落 4
**原文：** Reference BGM track (instrumental) and reference motion sample

**关键词与术语：**
- BGM /ˌbiː dʒiː ˈem/ n.：Background Music，背景音乐
- instrumental /ˌɪnstrəˈmentl/ adj./n.：纯器乐的；器乐曲
- motion sample /ˈmoʊʃən ˈsæmpl/ n. phr.：运动样例；动作与节奏参考样片

**整段翻译：**  
还提供参考 BGM 音轨（纯器乐）以及参考运动样片。

### 段落 5
**原文：** Target duration: **30 seconds total** (Part 1 0–15s + Part 2 15–30s), 16:9, 24fps

**关键词与术语：**
- target duration /ˈtɑːrɡɪt duˈreɪʃən/ n. phr.：目标时长
- fps /ˌef piː ˈes/ n.：frames per second，每秒帧数

**整段翻译：**  
目标总时长为 **30 秒**（第一段 0–15 秒 + 第二段 15–30 秒），画幅比例 16:9，帧率 24fps。

### 段落 6
**原文：** Format: realistic photographic cinematography with high-end motion-graphics editing

**关键词与术语：**
- photographic /ˌfoʊtəˈɡræfɪk/ adj.：摄影式的；具有真实摄影观感的
- cinematography /ˌsɪnəməˈtɑːɡrəfi/ n.：电影摄影；摄影语言
- motion graphics /ˈmoʊʃən ˈɡræfɪks/ n.：动态图形；动态图形设计
- high-end /ˌhaɪ ˈend/ adj.：高规格的；高端制作水准的

**整段翻译：**  
形式：真实摄影质感的电影摄影，并结合高规格动态图形剪辑。

### 段落 7
**原文：** Setting: a believable, restrained British-Puritan-style church — same location throughout

**关键词与术语：**
- setting /ˈsetɪŋ/ n.：场景设定；故事发生环境
- believable /bɪˈliːvəbl/ adj.：可信的；具有现实可信度的
- restrained /rɪˈstreɪnd/ adj.：克制的；不过度装饰的
- Puritan /ˈpjʊrɪtən/ adj./n.：清教徒的；清教徒
- throughout /θruːˈaʊt/ adv.：贯穿始终地

**整段翻译：**  
场景设定：一座可信、克制的英式清教徒风格教堂；全片始终保持同一地点。

## Media files｜媒体文件

**关键词与术语：**
- facial identity lock /ˈfeɪʃəl aɪˈdentəti lɑːk/ n. phr.：人脸身份锁定
- supplementary poses /ˌsʌplɪˈmentəri ˈpoʊzɪz/ n. phr.：补充姿态
- pacing /ˈpeɪsɪŋ/ n.：节奏控制；剪辑速度组织

| 文件 | 中文作用说明 |
|---|---|
| `picture-1-pose-library.png` | Picture 1：完整姿态库、服装与教堂环境 |
| `picture-2-face-identity.png` | Picture 2：同一角色的人脸身份锁定 |
| `picture-1-additional-poses.png` | 补充姿态（同一角色、同一教堂） |
| `picture-1-supplementary-poses.png` | 用于第二段选择的更多参考姿态 |
| `reference-motion-sample.mp4` | 运动方式 / 节奏参考样片 |
| `reference-bgm-tokyo-drifter.wav` | 参考纯器乐 BGM（无人声） |

## The problem｜问题

### 段落 1
**原文：** A character reveal is not one video. It's two.

**关键词与术语：**
- character reveal /ˈkærəktər rɪˈviːl/ n. phr.：角色揭示；通过镜头逐步介绍角色的影视段落

**整段翻译：**  
一次角色揭示并不是“一条视频”的问题，而是“两段视频”的问题。

### 段落 2
**原文：** Any character trailer longer than ~20 seconds faces a structural break: the first half must *introduce*, the second half must *establish*. These are different jobs. Trying to do both with one continuous prompt produces a flat, unmodulated video — a 30-second opening that never pays off.

**关键词与术语：**
- character trailer /ˈkærəktər ˈtreɪlər/ n. phr.：角色预告片
- structural break /ˈstrʌktʃərəl breɪk/ n. phr.：结构断点；叙事功能发生转换的位置
- establish /ɪˈstæblɪʃ/ v.：确立；在观众认知中正式建立角色形象
- continuous prompt /kənˈtɪnjuəs prɑːmpt/ n. phr.：连续单一提示词
- unmodulated /ʌnˈmɑːdjəleɪtɪd/ adj.：缺乏起伏变化的；未形成节奏调制的
- pay off /ˈpeɪ ˌɔːf/ v. phr.：形成回报；在叙事或节奏上兑现前面的铺垫

**整段翻译：**  
任何超过约 20 秒的角色预告片都会遇到一个结构性断点：前半段必须负责“引入”角色，后半段必须负责“确立”角色。这是两种不同的任务。如果试图只用一条连续提示词同时完成两者，结果往往是一条平直、缺乏调制的影片——像是一个持续了 30 秒却始终没有兑现铺垫的开场。

### 段落 3
**原文：** But splitting into two separate prompts creates a different disaster: at the seam, the music restarts, the church changes, the lighting shifts, the character "rediscovers" themselves, and the audience feels two unrelated clips glued together instead of one trailer.

**关键词与术语：**
- seam /siːm/ n.：接缝；两段生成视频之间的衔接点
- restart /ˌriːˈstɑːrt/ v.：重新开始
- lighting shift /ˈlaɪtɪŋ ʃɪft/ n. phr.：光照发生变化
- rediscover /ˌriːdɪˈskʌvər/ v.：重新发现；此处指模型像重新生成角色一样再次介绍人物
- glued together /ɡluːd təˈɡeðər/ adj. phr.：被生硬拼接在一起的

**整段翻译：**  
但如果把它拆成两条彼此独立的提示词，又会产生另一种灾难：到了两段的接缝处，音乐重新起头、教堂发生变化、光线漂移，角色仿佛又一次“重新认识自己”，观众感受到的是两个毫不相关的片段被粘在一起，而不是一支完整预告片。

### 段落 4
**原文：** The constraint is harder than it sounds because the model's prior is to **reset** between generations. Anything you can name — character, pose, costume, church, palette, BGM key, reverb tail, room ambience — will subtly restart unless you explicitly tell it to keep going.

**关键词与术语：**
- constraint /kənˈstreɪnt/ n.：约束条件
- prior /ˈpraɪər/ n.：先验倾向；模型默认偏向
- reset /ˌriːˈset/ v.：重置
- generation /ˌdʒenəˈreɪʃən/ n.：一次生成过程
- palette /ˈpælət/ n.：色板；整体色彩关系
- key /kiː/ n.：调性；音乐调
- reverb tail /ˈriːvɜːrb teɪl/ n. phr.：混响尾音
- room ambience /ruːm ˈæmbiəns/ n. phr.：空间环境声；室内底噪与空间声场

**整段翻译：**  
这个约束比听起来更难，因为模型在不同生成任务之间存在一种默认的**重置**倾向。凡是可以明确命名的东西——角色、姿态、服装、教堂、色彩体系、BGM 调性、混响尾音、空间环境声——如果不明确要求“继续保持”，都可能在第二次生成时悄然重新开始。

## The breakthrough｜关键突破

### 段落 1
**原文：** Split the prompt, but write the seam as a contract.

**关键词与术语：**
- contract /ˈkɑːntrækt/ n.：契约；此处指明确写进两段提示词的连续性约束协议

**整段翻译：**  
可以拆分提示词，但必须把两段之间的“接缝”写成一份明确的契约。

### 段落 2
**原文：** The two parts are issued as two independent prompts. To make them read as one trailer, the contract has six clauses, written into **both** prompts in matching language:

**关键词与术语：**
- independent prompt /ˌɪndɪˈpendənt prɑːmpt/ n. phr.：独立提示词
- clause /klɔːz/ n.：条款；契约中的规则项
- matching language /ˈmætʃɪŋ ˈlæŋɡwɪdʒ/ n. phr.：相互对应、保持一致的措辞

**整段翻译：**  
两段分别作为两条独立提示词执行。为了让最终结果看起来仍然是一支完整预告片，这份契约包含六项条款，并且必须用相互对应的语言同时写进**两条**提示词中：

| 契约条款 | 第一段的承诺 | 第二段的承诺 |
|---|---|---|
| 同一角色 / 服装 / 教堂 | “角色始终保持为真实摄影主体” | “严格使用第一段已经确立的同一角色、身份、服装和教堂” |
| 最后一帧连续性 | “最后一帧应像是为下一段 15 秒内容有意留下的停顿” | “严格从第一段最后的视觉状态开始” |
| BGM 连续性 | “不要在第 15 秒形成音乐结尾” + “保持和声与节奏动势仍然存续” | “不要重新开始音乐” + “精确延续此前的和声与节奏状态” |
| 声音设计连续性 | “不要在第 15 秒结束声音设计” | “第二段开始时不要创建新的环境声” |
| 镜头不重复 | （第一段默认建立镜头语言） | “不要重复第一段的具体镜头机制” + 明确的规避列表 |
| 姿态库纪律 | “只把这些姿态视为获准使用的主要姿态” | “使用 Picture 1 中第一段未重点展示的其余已批准姿态” |

### 段落 3
**原文：** The non-repetition list in Part 2 is worth highlighting. It doesn't just say "don't repeat." It names the six shot mechanisms Part 1 used — eye-only opening, face reveal, simple architectural reveal, simple hand-to-face match, same negative-space composition, same foreground wipe, same initial pose presentation — and tells the model to avoid them. Without this list, Part 2's first cut will reflexively copy Part 1's first cut, because the model's prior is "this is the structure of a character reveal."

**关键词与术语：**
- non-repetition /ˌnɑːn ˌrepəˈtɪʃən/ n.：不重复机制
- shot mechanism /ʃɑːt ˈmekənɪzəm/ n. phr.：镜头机制；一个镜头的构成与转场方法
- architectural reveal /ˌɑːrkɪˈtektʃərəl rɪˈviːl/ n. phr.：利用建筑元素完成的揭示镜头
- negative-space composition /ˈneɡətɪv speɪs ˌkɑːmpəˈzɪʃən/ n. phr.：负空间构图
- foreground wipe /ˈfɔːrɡraʊnd waɪp/ n. phr.：前景遮挡式转场
- reflexively /rɪˈfleksɪvli/ adv.：反射性地；下意识地

**整段翻译：**  
第二段中的“不重复列表”尤其值得强调。它并不只是笼统地说“不要重复”，而是明确点出第一段已经使用过的六类镜头机制——仅眼睛开场、面部揭示、简单建筑揭示、简单的手部到面部匹配、相同的负空间构图、相同的前景遮挡转场、相同的初始姿态展示方式——并要求模型主动避开这些方法。如果没有这份列表，第二段的第一个镜头很容易下意识复制第一段的第一个镜头，因为模型的默认先验会把“这就是角色揭示的结构”当作可重复模板。

### 段落 4：Technique stack｜技术栈

**关键词与术语：**
- architecture /ˈɑːrkɪtektʃər/ n.：架构；整体组织方式
- mirror contract clauses /ˈmɪrər ˈkɑːntrækt ˈklɔːzɪz/ n. phr.：镜像契约条款；在两条提示词中分别从各自视角重复同一连续性规则
- discipline /ˈdɪsəplɪn/ n.：纪律；严格执行的约束
- beat-indexed /biːt ˈɪndekst/ adj.：按节拍索引的；按时间节拍编号组织的
- hand-off /ˈhænd ɔːf/ n.：交接；从第一段状态移交到第二段
- pixel priority /ˈpɪksəl praɪˈɔːrəti/ n. phr.：像素优先级；有限画面分辨率优先分配给哪些主体

| 技术 | 中文作用 |
|---|---|
| **Two-Prompt / One-Video Architecture** | 两条独立提示词，但通过明确的接缝契约绑定为一条视频 |
| **Mirror Contract Clauses** | 每一条连续性规则都同时出现在两条提示词中，并分别从该段的视角措辞 |
| **Pose-Library Discipline** | Picture 1 中的姿态是唯一批准使用的主要姿态，不得自行发明 |
| **Face-Lock Separation** | Picture 2 只负责脸，Picture 1 负责其余全部信息；不合并身份、不重新设计 |
| **Beat-Indexed Shot Tables** | 每半段 13 个 CUT，明确写出时间范围与视觉动作 |
| **Non-Repetition Avoidance List** | 第二段直接点名第一段的镜头机制并要求规避 |
| **Continuous-Sound Design** | 空间混响、衣料运动声与 whoosh 转场音色跨接缝延续 |
| **Sister-Half Pacing** | 第一段为建立节奏；第二段为升级 → 高峰 → 收束 |
| **Final-Frame Hand-off** | 第一段以暂停状态姿态结束；第二段严格从该状态起步 |
| **Pixel-Priority Doctrine** | 脸 > 眼睛 > 手部 > 环境，绝不倒置 |

## The named language｜命名语言

### 段落 1
**原文：** **Two-Part Cinematic Reveal with Continuous BGM**

**关键词与术语：**
- cinematic reveal /ˌsɪnəˈmætɪk rɪˈviːl/ n. phr.：电影化角色揭示
- continuous BGM /kənˈtɪnjuəs ˌbiː dʒiː ˈem/ n. phr.：连续背景音乐

**整段翻译：**  
**连续 BGM 的两段式电影感角色揭示**

### 段落 2
**原文：** Three things packed into one name. "Two-Part" flags that this is a two-prompt workflow, not one. "Cinematic Reveal" flags the genre — character introduction, not action. "Continuous BGM" flags the hardest constraint, the one the model's prior most wants to violate: the music must not restart.

**关键词与术语：**
- flag /flæɡ/ v.：标示；明确指出
- genre /ˈʒɑːnrə/ n.：类型；影视类型
- violate /ˈvaɪəleɪt/ v.：违反；破坏约束

**整段翻译：**  
这个名称一次性编码了三层信息。“Two-Part”说明这是一个双提示词工作流，而不是单条提示词；“Cinematic Reveal”说明其类型是角色介绍，而不是动作戏；“Continuous BGM”则点出最困难的约束，也是模型默认先验最容易破坏的地方：音乐绝不能在第二段重新开始。

## 48-hour takeaway｜48 小时后的关键结论

### 段落 1
**原文：** Continuity is a contract, not an assumption.

**关键词与术语：**
- continuity /ˌkɑːntəˈnuːəti/ n.：连续性；跨镜头或跨生成保持一致的状态
- assumption /əˈsʌmpʃən/ n.：假设；未经明确声明的默认前提

**整段翻译：**  
连续性是一份契约，而不是一种想当然的假设。

### 段落 2
**原文：** Anything that needs to survive a prompt boundary — character identity, room ambience, BGM key, visual state — must be named in both prompts. Saying it once in Part 1 and hoping Part 2 inherits it is a recipe for a restart. The model's default between sessions is to begin clean. To defeat that default, you write the inheritance into the second prompt's opening section as a *new* rule the model will follow.

**关键词与术语：**
- prompt boundary /prɑːmpt ˈbaʊndri/ n. phr.：提示词边界；两个独立生成任务之间的边界
- visual state /ˈvɪʒuəl steɪt/ n. phr.：视觉状态
- inherit /ɪnˈherɪt/ v.：继承
- session /ˈseʃən/ n.：会话；一次相对独立的生成上下文
- inheritance /ɪnˈherɪtəns/ n.：继承机制；跨段保留上一段状态

**整段翻译：**  
任何需要跨越提示词边界继续存在的内容——角色身份、空间环境声、BGM 调性、视觉状态——都必须在两条提示词中明确写出来。只在第一段说一次，然后期待第二段自动继承，本质上就是在为“重新开始”创造条件。模型在不同生成会话之间的默认行为是从一个干净状态重新起步。要抵消这种默认行为，就必须把“继承上一段状态”写进第二条提示词的开头，把它重新声明为模型此刻要执行的一条**新规则**。

### 段落 3
**原文：** **1. Pose libraries beat pose invention.** A character that has 9–10 photographed poses in Picture 1 can do 30 seconds of varied shots without the model inventing a single new pose. The trick is to never say "show new poses." Say: "treat these as the ONLY approved major poses." This makes the library a constraint, not a suggestion.

**关键词与术语：**
- pose invention /poʊz ɪnˈvenʃən/ n. phr.：姿态发明；模型自行生成参考中不存在的新姿势
- varied shots /ˈverid ʃɑːts/ n. phr.：多样化镜头
- approved /əˈpruːvd/ adj.：获批准的；允许使用的

**整段翻译：**  
**1. 姿态库优于临时发明姿态。** 如果 Picture 1 已经提供 9–10 个拍摄好的姿态，那么完全可以用它们完成 30 秒的多样化镜头，而无需让模型额外发明任何新姿态。关键不是说“展示新的姿态”，而是明确写成：“把这些姿态视为唯一获准使用的主要姿态。”这样，姿态库就从一种建议变成了硬约束。

### 段落 4
**原文：** **2. Non-repetition lists beat non-repetition platitudes.** "Don't repeat Part 1" is too vague. Listing the exact six shot mechanisms Part 1 used gives the model concrete things to avoid. Vague rules get vague compliance.

**关键词与术语：**
- platitude /ˈplætɪtuːd/ n.：空泛套话；缺乏可执行细节的陈词
- concrete /ˈkɑːnkriːt/ adj.：具体的；可操作的
- compliance /kəmˈplaɪəns/ n.：遵从；对规则的执行程度

**整段翻译：**  
**2. 明确的不重复清单优于“不重复”的空泛要求。** “不要重复第一段”过于模糊。把第一段实际使用过的六类镜头机制逐项列出来，模型才会获得具体的规避目标。模糊的规则，只会得到模糊的执行。

### 段落 5
**原文：** **3. Final-frame design is hand-off design.** Part 1's last shot is not a closing shot — it's a *pause-state pose* that Part 2 opens on. The last 1.4 seconds of Part 1 and the first 0.9 seconds of Part 2 are designed together as one continuous breath. The seam disappears when both ends of it are written as handoff.

**关键词与术语：**
- final-frame design /ˈfaɪnəl freɪm dɪˈzaɪn/ n. phr.：末帧设计
- pause-state pose /pɔːz steɪt poʊz/ n. phr.：暂停状态姿态；为下一段保留的稳定动作状态
- continuous breath /kənˈtɪnjuəs breθ/ n. phr.：连续的一口气；比喻不中断的节奏过程
- handoff /ˈhændˌɔːf/ n.：交接；状态移交

**整段翻译：**  
**3. 末帧设计，本质上就是交接设计。** 第一段的最后一个镜头不是“收尾镜头”，而是一个供第二段继续使用的**暂停状态姿态**。第一段最后 1.4 秒与第二段最初 0.9 秒应当被当成同一次连续呼吸来共同设计。当接缝两端都被明确写成“状态交接”时，这道接缝本身就会从观感中消失。

## The final prompt｜最终提示词

### 段落 1
**原文：** See `prompt.md` for both Part 1 and Part 2 in full (usage notes in Chinese + structured English prompts).

**关键词与术语：**
- usage notes /ˈjuːsɪdʒ noʊts/ n. phr.：使用说明
- structured prompt /ˈstrʌktʃərd prɑːmpt/ n. phr.：结构化提示词

**整段翻译：**  
完整的第一段与第二段提示词请参见 `prompt.md`（中文使用说明 + 结构化英文提示词）。本目录中的 `prompt.zh-CN.md` 提供逐段词汇释义与简体中文翻译。

### 段落 2
**原文：** The prompt file is organized as:

**关键词与术语：**
- organize /ˈɔːrɡənaɪz/ v.：组织；按结构编排

**整段翻译：**  
提示词文件按照以下结构组织：

1. **Usage notes｜使用说明** —— 双 Picture 架构、BGM 连续性契约、不重复原则
2. **Part 1（0–15s）** —— 眼睛钩子 → 面部揭示 → 9 个姿态与剪辑 CUT 语法 → 暂停状态交接
3. **Part 2（15–30s）** —— 从第一段末帧状态继续 → 节奏升级蒙太奇 → Hero Reveal → 最终 Key Visual

### 段落 3
**原文：** Each part has its own beat-indexed shot table (13 cuts each, 26 total), its own negative-list, and matching continuity contract clauses for character / church / BGM / sound design.

**关键词与术语：**
- negative-list /ˈneɡətɪv lɪst/ n. phr.：负向约束列表；明确禁止出现的内容
- continuity contract /ˌkɑːntəˈnuːəti ˈkɑːntrækt/ n. phr.：连续性契约
- sound design /saʊnd dɪˈzaɪn/ n. phr.：声音设计

**整段翻译：**  
每一段都有独立的按节拍索引镜头表（每段 13 个 CUT，共 26 个）、独立负向约束列表，以及在角色 / 教堂 / BGM / 声音设计四个方面相互对应的连续性契约条款。

## Result｜结果

### 段落 1
**原文：** A 30-second two-part character trailer that reads as one film:

**关键词与术语：**
- read as /riːd æz/ v. phr.：呈现为；在观感上被理解为
- trailer /ˈtreɪlər/ n.：预告片

**整段翻译：**  
最终结果是一支 30 秒、由两段组成、但观感上像一部完整影片的角色预告片：

### 段落 2
**原文：** **Part 1 (0–15s):** Eye extreme close-up → face reveal → nine photographed poses strung together with hard cuts, graphic matches, architectural wipes, negative-space compositions, and a shutter-transition final pose held as a pause-state hand-off

**关键词与术语：**
- extreme close-up /ɪkˈstriːm ˈkloʊs ʌp/ n.：大特写
- hard cut /hɑːrd kʌt/ n.：硬切
- graphic match /ˈɡræfɪk mætʃ/ n.：图形匹配剪辑
- architectural wipe /ˌɑːrkɪˈtektʃərəl waɪp/ n.：建筑遮挡式转场
- shutter transition /ˈʃʌtər trænˈzɪʃən/ n.：快门式转场

**整段翻译：**  
**第一段（0–15 秒）：** 眼睛大特写 → 面部揭示 → 用硬切、图形匹配、建筑遮挡转场、负空间构图把 9 个已拍摄姿态串联起来 → 最后通过快门式转场进入一个作为暂停状态交接的最终姿态。

### 段落 3
**原文：** **Part 2 (15–30s):** Continues from Part 1's final pose, escalates tempo through a rapid detail montage and a five-beat character peak, resolves with a slow Hero Reveal into a clean final Key Visual — face locked to Picture 2, character large and dominant, restrained church ambience, sustained instrumental chord

**关键词与术语：**
- escalate /ˈeskəleɪt/ v.：升级；逐步增强
- rapid detail montage /ˈræpɪd ˈdiːteɪl ˌmɑːnˈtɑːʒ/ n. phr.：快速细节蒙太奇
- five-beat peak /faɪv biːt piːk/ n. phr.：五拍高潮
- Hero Reveal /ˈhɪəroʊ rɪˈviːl/ n.：主角式最终揭示
- Key Visual /kiː ˈvɪʒuəl/ n.：主视觉
- sustained chord /səˈsteɪnd kɔːrd/ n. phr.：持续和弦

**整段翻译：**  
**第二段（15–30 秒）：** 从第一段最后姿态直接继续，通过快速细节蒙太奇和五拍式角色高潮不断提升节奏，随后用减速的 Hero Reveal 收束到干净的最终 Key Visual——人脸由 Picture 2 锁定，人物在画面中保持大比例与主导地位，教堂环境声保持克制，音乐以持续的器乐和弦完成收束。

### 段落 4
**原文：** **Continuous BGM and room ambience** across the seam, with no musical restart, no new church, no character redesign

**关键词与术语：**
- across the seam /əˈkrɔːs ðə siːm/ phr.：跨越两段接缝
- redesign /ˌriːdɪˈzaɪn/ v.：重新设计

**整段翻译：**  
**BGM 与空间环境声跨接缝连续保持**：音乐不重新起头，不出现新的教堂，也不重新设计角色。

### 段落 5
**原文：** **No shot mechanism repeats** between halves — Part 1's eye-hook / face-reveal / architectural-wipe grammar is explicitly absent from Part 2, which uses a different visual vocabulary (callback reinterpretation, rapid detail montage, architectural cut, rhythmic pose montage, momentary silence, peak build, Hero reveal)

**关键词与术语：**
- visual vocabulary /ˈvɪʒuəl voʊˈkæbjəleri/ n. phr.：视觉词汇；一组可重复调用的影像表达手法
- callback /ˈkɔːlbæk/ n.：回调；对前文视觉元素的再引用
- reinterpretation /ˌriːɪnˌtɜːrprɪˈteɪʃən/ n.：重新解释；以不同方式再次使用同一视觉元素
- rhythmic montage /ˈrɪðmɪk ˌmɑːnˈtɑːʒ/ n. phr.：节奏化蒙太奇
- momentary silence /ˈmoʊmənteri ˈsaɪləns/ n. phr.：瞬时静默
- peak build /piːk bɪld/ n. phr.：高潮构建

**整段翻译：**  
**两段之间不重复任何镜头机制**：第一段的眼睛钩子 / 面部揭示 / 建筑遮挡式转场语法，在第二段中被明确排除。第二段改用另一套视觉词汇，包括：视觉回调的重新解释、快速细节蒙太奇、建筑切分、节奏化姿态蒙太奇、瞬时静默、高潮构建与 Hero Reveal。

## Tags｜标签

**关键词与术语：**
- prompt engineering /prɑːmpt ˌendʒɪˈnɪrɪŋ/ n.：提示词工程
- face lock /feɪs lɑːk/ n.：人脸锁定
- motion graphics /ˈmoʊʃən ˈɡræfɪks/ n.：动态图形设计
- aesthetic /esˈθetɪk/ n.：审美风格；视觉美学

**中文对应：**  
`#H3` `#提示词工程` `#角色揭示` `#两段式工作流` `#连续BGM` `#姿态库` `#人脸锁定` `#按节拍索引剪辑` `#动态图形` `#教堂美学` `#电影预告片`
