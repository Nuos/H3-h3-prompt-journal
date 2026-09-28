# 案例研究 003 — 微型摄影机锚点流飞行｜逐段翻译

> 对应原始 `README.md`。每一段先列关键词、术语和概念（IPA、词性缩写、简体中文释义），再给出整段简体中文译文。

## Inputs｜输入

### 段落 1
**原文：** `<Picture 1>` — The same person, pose 1 (first anchor)

**关键词与术语：**
- pose /poʊz/ n.：姿态
- anchor /ˈæŋkər/ n.：锚点；连续动作中必须经过的参考状态

**整段翻译：**  
`<Picture 1>` = 同一个人物的姿态 1，即第一个动作锚点。

### 段落 2
**原文：** `<Picture 2>` — The same person, pose 2 (second anchor)

**关键词与术语：**
- second anchor /ˈsekənd ˈæŋkər/ n. phr.：第二个锚点

**整段翻译：**  
`<Picture 2>` = 同一个人物的姿态 2，即第二个动作锚点。

### 段落 3
**原文：** `<Picture 3>` — The same person, pose 3 (final anchor)

**关键词与术语：**
- final anchor /ˈfaɪnəl ˈæŋkər/ n. phr.：最终锚点

**整段翻译：**  
`<Picture 3>` = 同一个人物的姿态 3，即最终动作锚点。

### 段落 4
**原文：** Target duration: **15 seconds**, single continuous shot

**关键词与术语：**
- duration /duˈreɪʃən/ n.：时长
- continuous shot /kənˈtɪnjuəs ʃɑːt/ n. phr.：连续镜头；不中断的一镜到底式镜头

**整段翻译：**  
目标时长：**15 秒**，单一连续镜头。

### 段落 5
**原文：** All three images show the **same person** — poses are waypoints, not separate identities

**关键词与术语：**
- waypoint /ˈweɪpɔɪnt/ n.：路径点；运动过程中的中间必经状态
- separate identity /ˈseprət aɪˈdentəti/ n. phr.：独立人物身份

**整段翻译：**  
三张图展示的都是**同一个人物**——这些姿态只是运动路径上的路标，不是三个不同的人物身份。

## The problem｜问题

### 段落 6
**原文：** H3 treats reference images as destinations.

**关键词与术语：**
- treat as /triːt æz/ v. phr.：把……当作
- destination /ˌdestɪˈneɪʃən/ n.：终点；最终停留状态

**整段翻译：**  
H3 很容易把参考图像当成动作“终点”。

### 段落 7
**原文：** Give it three poses of one person, and it produces a slideshow: hold Pose 1 → crossfade → hold Pose 2 → crossfade → hold Pose 3. Or worse, a slow elegant orbit around a frozen body, treating the poses as static portraits to admire. The energy dies. The reference images become endpoints to *reach and hold*, not anchors to *flow through*.

**关键词与术语：**
- slideshow /ˈslaɪdʃoʊ/ n.：幻灯片式切换
- hold /hoʊld/ v.：保持；在某姿态停留
- crossfade /ˈkrɔːsfeɪd/ n./v.：交叉淡化
- orbit /ˈɔːrbɪt/ n./v.：环绕；环绕摄影
- frozen body /ˈfroʊzən ˈbɑːdi/ n. phr.：冻结不动的人体
- static portrait /ˈstætɪk ˈpɔːrtrət/ n. phr.：静态肖像
- endpoint /ˈendpɔɪnt/ n.：终点状态
- flow through /floʊ θruː/ v. phr.：连续穿行经过；不停下来

**整段翻译：**  
如果给它同一个人物的三个姿态，模型很容易生成“幻灯片”：保持 Pose 1 → 交叉淡化 → 保持 Pose 2 → 交叉淡化 → 保持 Pose 3。更糟糕的情况，是摄影机缓慢、优雅地环绕一个几乎冻结不动的人体，把这些姿态当成静态肖像来欣赏。这样一来，整段影像的能量就消失了。参考图变成了必须“抵达并停住”的终点，而不是需要“流动穿过”的锚点。

## The breakthrough｜关键突破

### 段落 8
**原文：** Invert the agency.

**关键词与术语：**
- invert /ɪnˈvɜːrt/ v.：反转
- agency /ˈeɪdʒənsi/ n.：行动主体性；谁承担主要主动运动

**整段翻译：**  
把行动主体性反过来。

### 段落 9
**原文：** The **person moves normally** and does not avoid the camera. The **camera is the agile one** — an extremely small invisible flying point that predicts body movement and dodges at high speed. The person is gigantic relative to the camera. The camera sweeps past feet, legs, torso, shoulders, hair — constantly redirecting around the moving body without ever slowing down.

**关键词与术语：**
- agile /ˈædʒəl/ adj.：敏捷的
- invisible flying point /ɪnˈvɪzəbl ˈflaɪɪŋ pɔɪnt/ n. phr.：不可见的飞行点
- predict /prɪˈdɪkt/ v.：预判
- dodge /dɑːdʒ/ v.：闪避
- gigantic /dʒaɪˈɡæntɪk/ adj.：巨大的
- torso /ˈtɔːrsoʊ/ n.：躯干
- redirect /ˌriːdəˈrekt/ v.：重新改变运动方向

**整段翻译：**  
**人物正常运动**，而且不主动躲避摄影机。真正敏捷的是**摄影机**——把它设定成一个极小、不可见的飞行点，能够预判身体运动并以高速闪避。相对于摄影机，人物显得极其巨大。摄影机从脚部、腿部、躯干、肩膀、头发旁高速掠过，并不断围绕正在运动的人体改变方向，过程中绝不减速停顿。

### 段落 10
**原文：** The three reference poses are not destinations. They are **anchors** — waypoints in a continuous high-density flight. Between each anchor, the person performs multiple intermediate movements (weight transfer, torso rotation, limb reposition, head turn) that naturally lead toward the next pose. The camera never stops. The person never freezes.

**关键词与术语：**
- high-density flight /ˌhaɪ ˈdensəti flaɪt/ n. phr.：高密度飞行；短时间内持续发生大量路径变化
- intermediate movement /ˌɪntərˈmiːdiət ˈmuːvmənt/ n. phr.：中间动作
- weight transfer /weɪt ˈtrænsfɜːr/ n. phr.：重心转移
- torso rotation /ˈtɔːrsoʊ roʊˈteɪʃən/ n. phr.：躯干旋转
- limb reposition /lɪm ˌriːpəˈzɪʃən/ n. phr.：四肢重新定位
- head turn /hed tɜːrn/ n. phr.：转头

**整段翻译：**  
三张参考姿态不是终点，而是**锚点**——它们只是一次连续、高密度摄影机飞行中的必经路标。两个锚点之间，人物要完成多个自然的中间动作，例如重心转移、躯干旋转、四肢重新定位、转头等，并由这些动作自然过渡到下一个参考姿态。摄影机永不停下，人物也绝不冻结。

### 段落 11｜Technique stack
**关键词与术语：**
- structure /ˈstrʌktʃər/ n.：结构
- avoidance /əˈvɔɪdəns/ n.：规避；闪避
- scale inversion /skeɪl ɪnˈvɜːrʒən/ n. phr.：尺度反转
- action density /ˈækʃən ˈdensəti/ n. phr.：动作密度
- motivated movement /ˈmoʊtəveɪtɪd ˈmuːvmənt/ n. phr.：具有明确物理原因的运动

| 技术 | 中文作用 |
|---|---|
| **Anchor-Flow Pose Structure** | 三个姿态作为路径锚点，而不是动作终点 |
| **High-Speed Body Avoidance** | 摄影机高速躲避正在运动的身体部位 |
| **Tiny Invisible Camera** | 尺度反转：人物巨大、摄影机极小 |
| **Dual Action Density** | 摄影机与人物都必须频繁运动 |
| **Motivated Camera Movement** | 每一次闪避都必须可以用空间与物理关系解释 |

## The named language｜命名语言

### 段落 12
**原文：** **Micro-Cam Anchor-Flow Flight**

**关键词与术语：**
- Micro-Cam /ˈmaɪkroʊ kæm/ n.：微型摄影机
- Anchor-Flow /ˈæŋkər floʊ/ n.：锚点流；经过锚点但不停驻的动作结构
- flight /flaɪt/ n.：飞行路径

**整段翻译：**  
**微型摄影机锚点流飞行**

### 段落 13
**原文：** Two ideas in one name. "Anchor-Flow" tells the model: poses are passed through, not landed on. "Micro-Cam" tells the model: the camera is a tiny agile flyer, not a cinematic crane. Together they break the two default failure modes — static slideshow and slow orbit — in a single concept.

**关键词与术语：**
- land on /lænd ɑːn/ v. phr.：落在并停留于
- agile flyer /ˈædʒəl ˈflaɪər/ n. phr.：敏捷飞行主体
- cinematic crane /ˌsɪnəˈmætɪk kreɪn/ n. phr.：电影摇臂 / 吊臂式摄影机
- failure mode /ˈfeɪljər moʊd/ n. phr.：失败模式；模型常见错误倾向

**整段翻译：**  
这个名称同时包含两个概念。“Anchor-Flow”告诉模型：姿态应该被连续穿过，而不是“抵达后停下”；“Micro-Cam”告诉模型：摄影机是一个极小、敏捷的飞行体，而不是传统电影吊臂。把二者结合起来，就能用一个统一概念同时打破两种默认失败模式——静态幻灯片，以及缓慢环绕。

## 48-hour takeaway｜48 小时后的关键结论

### 段落 14
**原文：** Reference images aren't destinations — they're waypoints.

**关键词与术语：**
- waypoint /ˈweɪpɔɪnt/ n.：路径节点；必经但不必停留的位置

**整段翻译：**  
参考图不是终点，而是路径节点。

### 段落 15
**原文：** The model freezes when it thinks "reach pose and hold." It needs a **continuous flight grammar** where poses are milestones along a moving path, not stopping points. And the energy comes from **inverted agency**: instead of a static camera watching a posing model, make the camera the active agent that dodges and redirects around a naturally moving person.

**关键词与术语：**
- continuous flight grammar /kənˈtɪnjuəs flaɪt ˈɡræmər/ n. phr.：连续飞行语法
- milestone /ˈmaɪlstoʊn/ n.：里程碑；路径上的阶段节点
- stopping point /ˈstɑːpɪŋ pɔɪnt/ n. phr.：停驻点
- inverted agency /ɪnˈvɜːrtɪd ˈeɪdʒənsi/ n. phr.：反转的行动主体性
- active agent /ˈæktɪv ˈeɪdʒənt/ n. phr.：主动行动主体

**整段翻译：**  
当模型把任务理解为“到达某个姿态并保持”时，它就容易把人物冻结。需要的是一种**连续飞行语法**：让姿态成为移动路径上的里程碑，而不是停驻点。影像的能量则来自**行动主体性反转**：不是让一个静止摄影机观看人物摆姿势，而是让摄影机成为主动行动者，持续围绕自然运动的人体闪避并改变方向。

### 段落 16
**原文：** The 15-second timeline structure also matters. Breaking the shot into seven micro-segments (0–2.5s, 2.5–5s, 5–7.5s, 7.5–9.5s, 9.5–11.8s, 11.8–13.5s, 13.5–15s) with a specific camera trajectory for each gives the model a beat sheet it can follow, rather than a vague "make it dynamic."

**关键词与术语：**
- timeline structure /ˈtaɪmlaɪn ˈstrʌktʃər/ n. phr.：时间轴结构
- micro-segment /ˈmaɪkroʊ ˈseɡmənt/ n. phr.：微型时间段
- camera trajectory /ˈkæmərə trəˈdʒektəri/ n. phr.：摄影机运动轨迹
- beat sheet /biːt ʃiːt/ n. phr.：节拍表；按时间列出的动作执行表
- dynamic /daɪˈnæmɪk/ adj.：动态强的；具有运动变化的

**整段翻译：**  
15 秒的时间轴结构同样关键。把镜头拆为七个微时间段（0–2.5 秒、2.5–5 秒、5–7.5 秒、7.5–9.5 秒、9.5–11.8 秒、11.8–13.5 秒、13.5–15 秒），并为每一段指定摄影机轨迹，就等于给模型一份可以照着执行的节拍表，而不是只给一句模糊的“让画面更有动态感”。

## The final prompt｜最终提示词

### 段落 17
**原文：** See `prompt.md` for the full ~880-line prompt.

**关键词与术语：**
- full prompt /fʊl prɑːmpt/ n. phr.：完整提示词

**整段翻译：**  
完整约 880 行的提示词见 `prompt.md`；本目录的 `prompt.zh-CN.md` 提供逐段术语释义与中文翻译。

### 段落 18
**原文：** The prompt is organized in this order:

**整段翻译：**  
提示词依次包含以下模块：

1. **Reference priority｜参考优先级** —— 三张图，同一个人，姿态仅作为锚点
2. **Visual appearance lock｜视觉外观锁定** —— 参考图只负责外观
3. **Identity lock｜身份锁定** —— 全程精确保持脸、头发与服装
4. **Core concept｜核心概念** —— 极小不可见飞行摄影机，人物相对巨大
5. **Critical speed requirement｜关键速度要求** —— 摄影机必须快速移动，禁止慢速漂浮
6. **Critical action density｜关键动作密度** —— 人物同样必须频繁动作，不能冻结
7. **Who moves and who avoids｜谁运动、谁闪避** —— 人物正常运动，摄影机负责闪避
8. **High-speed camera avoidance｜高速摄影机闪避** —— 针对不同身体部位规定具体闪避模式
9. **15-second structure｜15 秒结构** —— 七个微时间段与对应摄影机轨迹
10. **Physical camera logic｜物理摄影机逻辑** —— 真实三维点、有动量、不瞬移
11. **Optical behavior｜光学行为** —— 真实透视、运动模糊、禁止鱼眼
12. **Absolute negative constraints｜绝对负向约束** —— 枚举全部常见失败模式
13. **Final creative intent｜最终创作意图** —— 用一个完整物理描述概括整条镜头

## Result｜结果

### 段落 19
**原文：** 15-second continuous single-take H3 output:

**关键词与术语：**
- single-take /ˌsɪŋɡəl ˈteɪk/ adj.：一镜到底式的
- output /ˈaʊtpʊt/ n.：生成结果

**整段翻译：**  
H3 最终生成的是一条 15 秒连续单镜头：

- **0–2.5s**：Picture 1 锚点 + 下半身附近快速飞行
- **2.5–5s**：快速过渡 → Picture 2 锚点
- **5–7.5s**：围绕 Picture 2 快速向上环绕
- **7.5–9.5s**：快速过渡 → Picture 3 锚点
- **9.5–11.8s**：上半身 / 头部高速环绕
- **11.8–13.5s**：快速接近人脸 + 改变方向
- **13.5–15s**：极高速后撤 → Picture 3 半身 Hero Frame → 保持

### 段落 20
**原文：** The camera never stops. The person never freezes. Three reference poses flow into each other through a continuous high-speed flight.

**关键词与术语：**
- freeze /friːz/ v.：冻结；停止人体运动
- flow into each other /floʊ ˈɪntuː iːtʃ ˈʌðər/ v. phr.：彼此连续流动过渡

**整段翻译：**  
摄影机从不停下，人物也从不冻结。三个参考姿态通过一次连续的高速摄影机飞行自然流动并相互衔接。

## Tags｜标签

**中文对应：**  
`#H3` `#提示词工程` `#摄影机语言` `#微型摄影机` `#锚点流` `#身体闪避` `#三姿态` `#高速飞行` `#单人物`
