# 案例研究 001 — 三人物遮挡衔接式环绕长镜头｜逐段翻译

> 对应原始 `README.md`。每段先列关键词、术语和概念（IPA、词性缩写、简体中文释义），再给出整段简体中文译文。

## Inputs｜输入

### 段落 1
**原文：** `<Picture 1>` — Person 1 + master environment + master spatial coordinate system

**关键词与术语：**
- master environment /ˈmæstər ɪnˈvaɪrənmənt/ n. phr.：主环境；整个空间的权威参考
- spatial coordinate system /ˈspeɪʃəl koʊˈɔːrdɪnət ˈsɪstəm/ n. phr.：空间坐标系统

**整段翻译：**  
`<Picture 1>` = 人物 1 + 主环境 + 主空间坐标系统。

### 段落 2
**原文：** `<Picture 2>` — Person 2 appearance only

**关键词与术语：**
- appearance /əˈpɪrəns/ n.：外观

**整段翻译：**  
`<Picture 2>` 只负责人物 2 的外观。

### 段落 3
**原文：** `<Picture 3>` — Person 3 appearance only

**整段翻译：**  
`<Picture 3>` 只负责人物 3 的外观。

### 段落 4
**原文：** Target duration: **20 seconds**, single continuous shot

**关键词与术语：**
- continuous shot /kənˈtɪnjuəs ʃɑːt/ n. phr.：连续长镜头

**整段翻译：**  
目标时长：**20 秒**，单一连续长镜头。

## The problem｜问题

### 段落 5
**原文：** H3 kept reading the brief as "the camera flies toward the second person."

**关键词与术语：**
- brief /briːf/ n.：任务说明 / 创作要求
- read as /riːd æz/ v. phr.：理解成

**整段翻译：**  
H3 一直把任务理解成：“摄影机直接飞向第二个人。”

### 段落 6
**原文：** Three characters, three full references, one shared room — and the model kept producing literal point-to-point flights. As soon as the brief said "go to Person 2," H3 cut or teleported or crossfaded. The semantic of *transition* was already poisoned by training data.

**关键词与术语：**
- point-to-point flight /ˌpɔɪnt tə ˈpɔɪnt flaɪt/ n. phr.：点到点直飞
- teleport /ˈteləpɔːrt/ v.：瞬移
- crossfade /ˈkrɔːsfeɪd/ v.：交叉淡化
- semantic /sɪˈmæntɪk/ n./adj.：语义 / 语义层面的
- poisoned /ˈpɔɪzənd/ adj.：被错误先验污染的

**整段翻译：**  
三个角色、三张完整参考图、同一个房间，但模型仍不断生成字面意义上的点到点飞行。只要任务里写“去 Person 2”，H3 就会切镜头、瞬移或交叉淡化。“transition（过渡）”这个语义在模型训练先验中已经被错误用法污染。

## The breakthrough｜关键突破

### 段落 7
**原文：** The real transition is not **flight**. It is **linkage**.

**关键词与术语：**
- linkage /ˈlɪŋkɪdʒ/ n.：衔接；有物理动机的连接关系

**整段翻译：**  
真正的过渡并不是**飞过去**，而是建立**衔接**。

### 段落 8
**原文：** Each character owns a complete close-range orbit — feet to head, traveling horizontally through front-side, three-quarter, side, and rear-side. The camera never stops, never cuts. The current subject's body moves extremely close to the lens, forming a **foreground occlusion**. The camera rounds the shoulder, the hair, the back — and the next character suddenly emerges from behind the obstruction as a fresh orbital center.

**关键词与术语：**
- close-range orbit /ˌkloʊs ˈreɪndʒ ˈɔːrbɪt/ n. phr.：近距离环绕
- three-quarter /ˌθriː ˈkwɔːrtər/ adj.：三分之四角度
- foreground occlusion /ˈfɔːrɡraʊnd əˈkluːʒən/ n. phr.：前景遮挡
- obstruction /əbˈstrʌkʃən/ n.：遮挡物
- orbital center /ˈɔːrbɪtl ˈsentər/ n. phr.：环绕中心

**整段翻译：**  
每个角色都拥有一段完整的近距离环绕——从脚到头，摄影机水平方向经过正侧、三分之四角度、侧面与后侧。摄影机不停、不切。当前人物身体极近距离靠近镜头，形成**前景遮挡**；摄影机绕过肩膀、头发或背部后，下一个人物突然从遮挡后出现，并成为新的环绕中心。

### 段落 9｜Technique stack

| 技术 | 中文作用 |
|---|---|
| **Foreground Occlusion Transition** | 用当前主体形成前景遮挡，作为人物切换机制 |
| **Motivated Camera Movement** | 每段摄影机路径都有明确物理原因 |
| **Continuous Long Take** | 20 秒单镜头，内部无切镜 |
| **Close-Range Orbital Camera** | 每个主体获得完整 360° 近距离环绕 |

## The named language｜命名语言

### 段落 10
**原文：** **Occlusion-Linked Orbital Long Take**

**关键词与术语：**
- occlusion-linked /əˈkluːʒən lɪŋkt/ adj.：通过遮挡衔接的
- orbital long take /ˈɔːrbɪtl lɔːŋ teɪk/ n. phr.：环绕式长镜头

**整段翻译：**  
**遮挡衔接式环绕长镜头**

### 段落 11
**原文：** Naming the pattern mattered. Once the prompt contained the named language, H3 stopped trying to interpret "go to" and started treating each segment as a separate orbital problem to solve independently.

**关键词与术语：**
- pattern /ˈpætərn/ n.：可复用模式
- independently /ˌɪndɪˈpendəntli/ adv.：独立地

**整段翻译：**  
给这个模式命名非常重要。提示词中出现明确命名后，H3 不再把“go to”理解成直接飞向某人，而开始把每个分段当作一个独立的环绕问题来解决。

## 48-hour takeaway｜48 小时后的关键结论

### 段落 12
**原文：** H3 prompt engineering is less about piling constraints and more about **teaching the model a different way of thinking about transition**.

**关键词与术语：**
- pile constraints /paɪl kənˈstreɪnts/ v. phr.：堆叠约束
- prompt engineering /prɑːmpt ˌendʒɪˈnɪrɪŋ/ n.：提示词工程

**整段翻译：**  
H3 提示词工程与其说是不断堆约束，不如说是在**教模型用另一种方式理解“过渡”**。

### 段落 13
**原文：** Constraints like "no cut" and "no morph" are necessary but not sufficient. The model needs a generative grammar — a named pattern it can reproduce.

**关键词与术语：**
- sufficient /səˈfɪʃənt/ adj.：充分的
- generative grammar /ˈdʒenərətɪv ˈɡræmər/ n. phr.：生成语法；可供模型复现的结构规则
- morph /mɔːrf/ v.：形变

**整段翻译：**  
“不要切镜”“不要形变”等约束虽然必要，但并不充分。模型还需要一套**生成语法**——也就是一个有名称、可复现的结构模式。

## The final prompt｜最终提示词

### 段落 14
**原文：** See `prompt.md` for the full 1413-line prompt that solved this case.

**整段翻译：**  
解决本案例的完整约 1413 行提示词见 `prompt.md`；逐段中文翻译见 `prompt.zh-CN.md`。

### 段落 15
**整段翻译：**  
提示词结构依次为：
1. **Reference priority｜参考优先级** —— 每张图控制什么
2. **Master environment lock｜主环境锁定** —— Picture 1 负责整个空间
3. **Three people, one space｜三人物同一空间** —— 空间融合规则
4. **Visibility rule｜可见性规则** —— 最终揭示前一次只出现一个人物
5. **Spatial arrangement｜空间排布** —— 物理距离与遮挡几何
6. **Identity lock｜身份锁定** —— 精确保留脸、服装、发型
7. **Per-character orbit specification｜逐人物环绕规格**
8. **Camera behavior｜摄影机行为** —— 近距离环绕与动机化运动
9. **Optical behavior｜光学行为** —— 真实透视、视差、禁止鱼眼
10. **Absolute negative constraints｜绝对负向约束**
11. **Final creative intent｜最终创作意图** —— 用一句物理描述概括整条镜头

## Result｜结果

### 段落 16
**原文：** 20-second continuous single-take H3 output:

**关键词与术语：**
- single-take /ˌsɪŋɡəl ˈteɪk/ adj.：一镜到底式的

**整段翻译：**  
最终 H3 输出为 20 秒连续一镜到底：
- 人物 1 完整环绕（约 6 秒）→ 遮挡揭示；
- 人物 2 完整环绕（约 6 秒）→ 遮挡揭示；
- 人物 3 完整环绕（约 6 秒）→ 短暂后拉；
- 最终三人物近距离半身合影（约 2 秒）。

### 段落 17
**原文：** All three people visible together for the first and only time in the final frame, proving their physical co-presence throughout.

**关键词与术语：**
- co-presence /ˌkoʊ ˈprezəns/ n.：共同在场

**整段翻译：**  
三个人物只在最终画面第一次、也是唯一一次同时可见，从而证明三者从始至终都真实处于同一物理空间。

## Tags｜标签

**中文对应：**  
`#H3` `#提示词工程` `#摄影机语言` `#长镜头` `#前景遮挡` `#环绕` `#三人物` `#遮挡衔接`
