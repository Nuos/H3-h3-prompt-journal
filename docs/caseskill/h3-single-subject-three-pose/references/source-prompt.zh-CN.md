# Case Study 003｜Micro-Cam Anchor-Flow Flight｜英文 Prompt 逐段翻译

> 对应原始 `prompt.md`。本文件按原提示词结构逐段处理：先给出关键词、术语与概念（IPA、词性缩写、简体中文释义），再给出整段简体中文翻译。基础词汇、介词、冠词、数词等不重复释义。

# REFERENCE PRIORITY — ABSOLUTE｜参考优先级——绝对规则

## 段落 1
**原文：** <Picture 1>, <Picture 2>, and <Picture 3> are the ONLY visual references.

**关键词与术语：**
- visual reference /ˈvɪʒuəl ˈrefrəns/ n. phr.：视觉参考
- absolute /ˈæbsəluːt/ adj.：绝对的；不可让位的

**整段翻译：**  
`<Picture 1>`、`<Picture 2>` 和 `<Picture 3>` 是**唯一视觉参考**。

## 段落 2
**原文：** All three pictures show the SAME PERSON.

**关键词与术语：**
- same person /seɪm ˈpɜːrsən/ n. phr.：同一个人物

**整段翻译：**  
三张图片展示的都是**同一个人物**。

## 段落 3
**原文：** Picture 1 = first pose. Picture 2 = second pose. Picture 3 = final pose.

**关键词与术语：**
- pose /poʊz/ n.：姿态

**整段翻译：**  
Picture 1 = 第一个姿态；Picture 2 = 第二个姿态；Picture 3 = 最终姿态。

## 段落 4
**原文：** The three images are the ONLY source of truth for the person's appearance.

**关键词与术语：**
- source of truth /sɔːrs əv truːθ/ n. phr.：唯一事实来源；决定最终结果的权威参考
- appearance /əˈpɪrəns/ n.：外观

**整段翻译：**  
这三张图片是人物外观的**唯一权威事实来源**。

# VISUAL APPEARANCE — REFERENCE ONLY｜视觉外观——仅由参考图决定

## 段落 5
**原文：** The input images determine the visual appearance.

**关键词与术语：**
- determine /dɪˈtɜːrmɪn/ v.：决定

**整段翻译：**  
输入图片决定最终视觉外观。

## 段落 6
**原文：** Do not redesign the appearance. Do not create a new visual style. Do not reinterpret the reference images.

**关键词与术语：**
- redesign /ˌriːdɪˈzaɪn/ v.：重新设计
- reinterpret /ˌriːɪnˈtɜːrprɪt/ v.：重新解释 / 改写

**整段翻译：**  
不要重新设计外观。不要创建新的视觉风格。不要对参考图进行重新解释。

## 段落 7
**原文：** Do not redesign the environment. Do not redesign the clothing. Do not redesign the hairstyle. Do not redesign the person's face.

**关键词与术语：**
- environment /ɪnˈvaɪrənmənt/ n.：环境
- clothing /ˈkloʊðɪŋ/ n.：服装
- hairstyle /ˈherstaɪl/ n.：发型

**整段翻译：**  
不要重新设计环境、服装、发型或人物的脸。

## 段落 8
**原文：** Do not add new visual effects that change the appearance.

**关键词与术语：**
- visual effect /ˈvɪʒuəl ɪˈfekt/ n. phr.：视觉特效

**整段翻译：**  
不要加入会改变人物原始外观的新视觉特效。

## 段落 9
**原文：** The generated video only controls: camera movement, camera position, camera angle, perspective, parallax, framing, spatial movement, and natural human pose transitions.

**关键词与术语：**
- camera movement /ˈkæmərə ˈmuːvmənt/ n. phr.：运镜
- perspective /pərˈspektɪv/ n.：透视
- parallax /ˈpærəlæks/ n.：视差
- framing /ˈfreɪmɪŋ/ n.：构图 / 取景
- spatial movement /ˈspeɪʃəl ˈmuːvmənt/ n. phr.：空间运动
- pose transition /poʊz trænˈzɪʃən/ n. phr.：姿态过渡

**整段翻译：**  
生成视频只负责控制以下内容：摄影机运动、机位、摄影角度、透视、视差、构图、空间运动，以及自然的人体姿态过渡。

## 段落 10
**原文：** The camera is moving through the visual world established by the reference images.

**关键词与术语：**
- established by /ɪˈstæblɪʃt baɪ/ phr.：由……确立
- visual world /ˈvɪʒuəl wɜːrld/ n. phr.：视觉世界 / 参考图确定的空间与外观体系

**整段翻译：**  
摄影机只是在参考图已经建立的视觉世界中移动。

# IDENTITY LOCK｜身份锁定

## 段落 11
**原文：** The SAME PERSON remains identical throughout the entire 15 seconds.

**关键词与术语：**
- identical /aɪˈdentɪkəl/ adj.：完全一致的
- throughout /θruːˈaʊt/ adv.：贯穿始终

**整段翻译：**  
整个 15 秒内必须始终是**同一个人物**，身份完全一致。

## 段落 12
**原文：** Preserve: exact face, facial structure, facial proportions, hairstyle, hair color, clothing, body proportions, makeup, skin appearance.

**关键词与术语：**
- facial structure /ˈfeɪʃəl ˈstrʌktʃər/ n. phr.：面部结构
- facial proportions /ˈfeɪʃəl prəˈpɔːrʃənz/ n. phr.：面部比例
- body proportions /ˈbɑːdi prəˈpɔːrʃənz/ n. phr.：身体比例
- makeup /ˈmeɪkʌp/ n.：妆容
- skin appearance /skɪn əˈpɪrəns/ n. phr.：皮肤外观

**整段翻译：**  
严格保持：精确的人脸、面部结构、面部比例、发型、发色、服装、身体比例、妆容和皮肤外观。

## 段落 13
**原文：** Do not create another person. Do not change the face. Do not change the hairstyle. Do not change the clothing. Do not change body proportions. Do not invent accessories.

**关键词与术语：**
- invent accessories /ɪnˈvent əkˈsesəriz/ v. phr.：自行添加参考中不存在的配饰

**整段翻译：**  
不要创建另一个人物。不要改变脸、发型、服装或身体比例，也不要自行发明新配饰。

# CORE CONCEPT｜核心概念

## 段落 14
**原文：** Create a FAST, CONTINUOUS, HIGH-DENSITY FIRST-PERSON PORTRAIT MV.

**关键词与术语：**
- high-density /ˌhaɪ ˈdensəti/ adj.：高密度的；短时间内包含大量运动变化的
- first-person portrait MV /ˌfɜːrst ˈpɜːrsən ˈpɔːrtrət ˌem ˈviː/ n. phr.：第一人称肖像式音乐视频

**整段翻译：**  
创建一条**快速、连续、高密度的第一人称肖像 MV**。

## 段落 15
**原文：** The camera is an EXTREMELY SMALL INVISIBLE FLYING CAMERA.

**关键词与术语：**
- invisible /ɪnˈvɪzəbl/ adj.：不可见的
- flying camera /ˈflaɪɪŋ ˈkæmərə/ n. phr.：飞行摄影机

**整段翻译：**  
摄影机是一台**极其微小、不可见的飞行摄影机**。

## 段落 16
**原文：** The camera itself is never visible. No insect. No bee. No wings. No drone.

**关键词与术语：**
- drone /droʊn/ n.：无人机

**整段翻译：**  
摄影机本体永远不能被看见。不要昆虫、不要蜜蜂、不要翅膀、不要无人机。

## 段落 17
**原文：** The tiny-camera concept is expressed ONLY through: extreme proximity, large-scale perspective, strong parallax, rapid camera movement, close body passes, and constantly changing flight direction.

**关键词与术语：**
- extreme proximity /ɪkˈstriːm prɑːkˈsɪməti/ n. phr.：极近距离
- large-scale perspective /ˌlɑːrdʒ ˈskeɪl pərˈspektɪv/ n. phr.：巨大尺度透视
- close body pass /kloʊs ˈbɑːdi pæs/ n. phr.：贴近身体掠过

**整段翻译：**  
“微型摄影机”这一概念只能通过以下视觉结果表现：极近距离、巨大尺度透视、强视差、高速运镜、贴近身体掠过，以及不断变化的飞行方向。

## 段落 18
**原文：** The person appears gigantic relative to the camera.

**关键词与术语：**
- gigantic /dʒaɪˈɡæntɪk/ adj.：极其巨大的
- relative to /ˈrelətɪv tuː/ phr.：相对于

**整段翻译：**  
相对于摄影机，人物应显得极其巨大。

## 段落 19
**原文：** The camera is physically flying around the person at extremely close range.

**关键词与术语：**
- physically /ˈfɪzɪkli/ adv.：以真实空间运动方式
- close range /kloʊs reɪndʒ/ n. phr.：近距离

**整段翻译：**  
摄影机以真实空间飞行方式，在极近距离围绕人物高速飞行。

# CRITICAL SPEED REQUIREMENT｜关键速度要求

## 段落 20
**原文：** THE CAMERA MUST MOVE FAST.

**整段翻译：**  
**摄影机必须高速运动。**

## 段落 21
**原文：** The flight speed must be substantially faster than a normal cinematic camera.

**关键词与术语：**
- substantially /səbˈstænʃəli/ adv.：显著地
- cinematic camera /ˌsɪnəˈmætɪk ˈkæmərə/ n. phr.：常规电影摄影机

**整段翻译：**  
飞行速度必须显著快于普通电影摄影机的常规运镜速度。

## 段落 22
**原文：** Fast enough to create obvious continuous parallax. Fast enough that the person's body and environment visibly sweep through the foreground. Fast enough that the camera must continuously redirect itself around the moving body.

**关键词与术语：**
- continuous parallax /kənˈtɪnjuəs ˈpærəlæks/ n. phr.：连续视差
- sweep through /swiːp θruː/ v. phr.：快速掠过
- redirect /ˌriːdəˈrekt/ v.：改变运动方向

**整段翻译：**  
速度必须快到产生明显连续视差；快到人物身体与环境能够明显从前景掠过；快到摄影机必须持续围绕正在运动的身体改变自身飞行方向。

## 段落 23
**原文：** Do NOT use slow floating movement. Do NOT use long elegant slow-motion camera movement. Do NOT spend several seconds simply approaching one body part.

**关键词与术语：**
- floating movement /ˈfloʊtɪŋ ˈmuːvmənt/ n. phr.：漂浮式慢运镜
- slow-motion camera movement /ˌsloʊ ˈmoʊʃən ˈkæmərə ˈmuːvmənt/ n. phr.：慢动作式运镜

**整段翻译：**  
禁止慢速漂浮。禁止长时间优雅缓慢运镜。禁止花几秒钟只去接近某一个身体部位。

## 段落 24
**原文：** The camera should almost always be moving. The camera should have strong continuous momentum.

**关键词与术语：**
- momentum /moʊˈmentəm/ n.：动量；持续运动趋势

**整段翻译：**  
摄影机几乎始终都应在运动，并保持强烈、连续的动量感。

# CRITICAL ACTION DENSITY｜关键动作密度

## 段落 25
**原文：** The PERSON MUST ALSO MOVE FREQUENTLY.

**关键词与术语：**
- frequently /ˈfriːkwəntli/ adv.：频繁地

**整段翻译：**  
**人物也必须频繁运动。**

## 段落 26
**原文：** Do NOT make the person remain static for several seconds.

**关键词与术语：**
- static /ˈstætɪk/ adj.：静止的

**整段翻译：**  
不要让人物连续几秒保持静止。

## 段落 27
**原文：** Do NOT only perform: Pose 1 → Pose 2 → Pose 3.

**整段翻译：**  
不要只机械执行：Pose 1 → Pose 2 → Pose 3。

## 段落 28
**原文：**
Pose 1 → small movement → body rotation → limb reposition → Pose 1 variation → transition movement → Pose 2 → small movement → shoulder rotation → head movement → body reposition → Pose 2 variation → transition movement → Pose 3 → final adjustment → final hero pose.

**关键词与术语：**
- body rotation /ˈbɑːdi roʊˈteɪʃən/ n. phr.：身体旋转
- limb reposition /lɪm ˌriːpəˈzɪʃən/ n. phr.：四肢重新定位
- variation /ˌveriˈeɪʃən/ n.：姿态变体
- transition movement /trænˈzɪʃən ˈmuːvmənt/ n. phr.：过渡动作
- final adjustment /ˈfaɪnəl əˈdʒʌstmənt/ n. phr.：最终微调

**整段翻译：**  
应当形成这样的连续动作链：Pose 1 → 小动作 → 身体旋转 → 四肢重新定位 → Pose 1 变体 → 过渡动作 → Pose 2 → 小动作 → 肩部旋转 → 头部运动 → 身体重新定位 → Pose 2 变体 → 过渡动作 → Pose 3 → 最终微调 → 最终 Hero Pose。

## 段落 29
**原文：** The three reference poses are ANCHORS.

**关键词与术语：**
- anchor /ˈæŋkər/ n.：锚点

**整段翻译：**  
三张参考姿态只是**锚点**。

## 段落 30
**原文：** Between each anchor, the person performs multiple natural intermediate movements.

**关键词与术语：**
- intermediate movement /ˌɪntərˈmiːdiət ˈmuːvmənt/ n. phr.：中间过渡动作

**整段翻译：**  
每两个锚点之间，人物都要完成多个自然中间动作。

## 段落 31
**原文：** These intermediate movements must be derived from the reference poses. Do not invent unrelated choreography.

**关键词与术语：**
- derive from /dɪˈraɪv frəm/ v. phr.：从……推导
- unrelated choreography /ˌʌnrɪˈleɪtɪd ˌkɔːriˈɑːɡrəfi/ n. phr.：与参考姿态无关的编舞

**整段翻译：**  
这些中间动作必须从参考姿态自然推导出来，不能自行发明无关编舞。

# WHO MOVES AND WHO AVOIDS｜谁运动、谁闪避

## 段落 32
**原文：** The PERSON moves normally. The PERSON does NOT avoid the camera. The CAMERA avoids the PERSON.

**关键词与术语：**
- avoid /əˈvɔɪd/ v.：躲避

**整段翻译：**  
**人物正常运动。人物不躲摄影机。摄影机躲人物。**

## 段落 33
**原文：** This distinction is absolute.

**关键词与术语：**
- distinction /dɪˈstɪŋkʃən/ n.：区别

**整段翻译：**  
这一职责区分是绝对规则。

## 段落 34
**原文：** The person performs natural pose transitions. The camera predicts the movement of the person's body and rapidly changes its own flight path to avoid collision.

**关键词与术语：**
- predict /prɪˈdɪkt/ v.：预判
- flight path /flaɪt pæθ/ n. phr.：飞行路径
- collision /kəˈlɪʒən/ n.：碰撞

**整段翻译：**  
人物只负责自然姿态过渡。摄影机预判人物身体运动，并高速改变自己的飞行路径以避免碰撞。

## 段落 35
**原文：** The camera is agile. The person is not reacting to the camera.

**关键词与术语：**
- agile /ˈædʒəl/ adj.：敏捷的
- react to /riˈækt tuː/ v. phr.：对……作出反应

**整段翻译：**  
摄影机非常敏捷；人物不能因为摄影机接近而作出躲避反应。

# HIGH-SPEED CAMERA AVOIDANCE｜高速摄影机闪避

## 段落 36
**原文：** The camera must avoid moving body parts at HIGH SPEED. Do not slow down to avoid collision. Avoidance itself must be a rapid camera maneuver.

**关键词与术语：**
- avoidance /əˈvɔɪdəns/ n.：闪避
- maneuver /məˈnuːvər/ n.：机动动作

**整段翻译：**  
摄影机必须以**高速**闪避运动中的身体部位。不能为了避碰而减速；闪避本身就必须是一种快速摄影机机动。

## 段落 37｜腿部闪避示例
**原文：** Moving leg enters camera path → immediate lateral acceleration → tight outside-leg arc → instant upward acceleration.

**关键词与术语：**
- lateral acceleration /ˈlætərəl əkˌseləˈreɪʃən/ n. phr.：横向加速
- tight arc /taɪt ɑːrk/ n. phr.：小半径紧凑弧线

**整段翻译：**  
运动中的腿进入摄影机路径 → 立即横向加速 → 沿腿外侧做小半径紧凑弧线 → 立刻向上加速。

## 段落 38｜手臂闪避示例
**原文：** Moving arm crosses camera path → rapid downward dodge → close pass underneath arm → immediate upward redirection.

**关键词与术语：**
- downward dodge /ˈdaʊnwərd dɑːdʒ/ n. phr.：向下闪避
- underneath /ˌʌndərˈniːθ/ adv.：从下方
- redirection /ˌriːdəˈrekʃən/ n.：重新定向

**整段翻译：**  
运动中的手臂横穿摄影机路径 → 摄影机快速向下闪避 → 紧贴手臂下方掠过 → 立即重新向上改变方向。

## 段落 39｜躯干闪避示例
**原文：** Torso rotates into camera trajectory → fast lateral displacement → curved orbit around torso → immediate forward acceleration.

**关键词与术语：**
- trajectory /trəˈdʒektəri/ n.：运动轨迹
- displacement /dɪsˈpleɪsmənt/ n.：位移
- curved orbit /kɜːrvd ˈɔːrbɪt/ n. phr.：曲线环绕

**整段翻译：**  
躯干旋转进入摄影机轨迹 → 快速横向位移 → 沿躯干做曲线环绕 → 立即向前加速。

## 段落 40｜肩部闪避示例
**原文：** Shoulder enters trajectory → quick outward arc → shoulder passes close to foreground → camera accelerates toward head.

**关键词与术语：**
- outward arc /ˈaʊtwərd ɑːrk/ n. phr.：向外弧线

**整段翻译：**  
肩膀进入摄影机轨迹 → 摄影机快速向外绕弧 → 肩膀从前景近距离掠过 → 摄影机再加速朝头部飞去。

## 段落 41｜头部闪避示例
**原文：** Head turns toward camera → camera rapidly shifts to three-quarter angle → continues orbit.

**关键词与术语：**
- three-quarter angle /ˌθriː ˈkwɔːrtər ˈæŋɡəl/ n. phr.：三分之四角度

**整段翻译：**  
头部转向摄影机 → 摄影机迅速切到三分之四角度 → 继续环绕。

## 段落 42
**原文：** Every dodge should take place while maintaining high velocity. Never stop. Never freeze. Never wait for the person.

**关键词与术语：**
- velocity /vəˈlɑːsəti/ n.：速度

**整段翻译：**  
所有闪避都必须在维持高速度的过程中完成。永远不要停、不要冻结、不要等待人物。

# 15 SECOND HIGH-DENSITY STRUCTURE｜15 秒高密度结构

## 段落 43
**整段翻译：**
- 0.0–2.5s：Picture 1 + 脚部 / 下半身快速飞行
- 2.5–5.0s：Picture 1 → Picture 2 快速转化
- 5.0–7.5s：Picture 2 + 快速身体环绕
- 7.5–9.5s：Picture 2 → Picture 3 快速转化
- 9.5–11.8s：Picture 3 + 上半身 / 头部高速环绕
- 11.8–13.5s：快速接近人脸 + 改变方向
- 13.5–15.0s：极高速后撤 → Picture 3 半身 Hero Frame → 保持

# 0.0–2.5s｜PICTURE 1 — IMMEDIATE HIGH-SPEED START

## 段落 44
**原文：** Start directly from Picture 1. Do not spend time establishing the shot.

**关键词与术语：**
- establishing /ɪˈstæblɪʃɪŋ/ n./adj.：建立环境信息的

**整段翻译：**  
直接从 Picture 1 开始，不要浪费时间做建立镜头。

## 段落 45
**原文：** The camera starts extremely close to the feet. Immediately accelerate.

**关键词与术语：**
- accelerate /əkˈseləreɪt/ v.：加速

**整段翻译：**  
摄影机从极靠近脚部的位置开始，并立即加速。

## 段落 46
**原文：** Camera trajectory: feet → outside ankle → fast lower-leg orbit → knee → lateral dodge → thigh.

**关键词与术语：**
- ankle /ˈæŋkəl/ n.：脚踝
- lower leg /ˌloʊər ˈleɡ/ n.：小腿
- thigh /θaɪ/ n.：大腿

**整段翻译：**  
摄影机轨迹：脚部 → 外侧脚踝 → 快速环绕小腿 → 膝盖 → 横向闪避 → 大腿。

## 段落 47
**原文：** Do NOT stay around the feet. Do NOT complete a slow orbit.

**整段翻译：**  
不要停留在脚部附近，也不要完成缓慢完整环绕。

## 段落 48
**原文：** The camera should already be moving rapidly within the first moment.

**整段翻译：**  
从最开始的瞬间，摄影机就应已经处于高速运动状态。

## 段落 49
**原文：** The person immediately begins subtle physical movement from Picture 1.

**关键词与术语：**
- subtle physical movement /ˈsʌtl ˈfɪzɪkəl ˈmuːvmənt/ n. phr.：轻微自然身体动作

**整段翻译：**  
人物也要立即从 Picture 1 的姿态开始产生轻微自然身体运动。

## 段落 50
**原文：** Examples: weight transfer, leg adjustment, torso movement, shoulder movement, head movement. These movements must remain consistent with the reference pose.

**关键词与术语：**
- weight transfer /weɪt ˈtrænsfɜːr/ n. phr.：重心转移
- adjustment /əˈdʒʌstmənt/ n.：微调
- consistent with /kənˈsɪstənt wɪð/ adj. phr.：与……一致

**整段翻译：**  
例如：重心转移、腿部微调、躯干运动、肩部运动、头部运动。这些动作必须与参考姿态保持一致。

# 2.5–5.0s｜PICTURE 1 → PICTURE 2

## 段落 51
**原文：** The person now actively transitions toward Picture 2. The transformation happens quickly. Do not make the person slowly pose.

**关键词与术语：**
- actively transition /ˈæktɪvli trænˈzɪʃən/ v. phr.：主动连续过渡
- transformation /ˌtrænsfərˈmeɪʃən/ n.：状态转化

**整段翻译：**  
人物现在主动向 Picture 2 过渡，转换必须快速，不要让人物慢慢“摆到”下一个姿态。

## 段落 52
**原文：** Use multiple connected body movements: leg reposition → torso rotation → shoulder change → arm reposition → head adjustment → Picture 2 pose.

**关键词与术语：**
- connected movement /kəˈnektɪd ˈmuːvmənt/ n. phr.：彼此连续衔接的动作

**整段翻译：**  
使用多个彼此连续的身体动作：腿部重新定位 → 躯干旋转 → 肩部变化 → 手臂重新定位 → 头部调整 → Picture 2 姿态。

## 段落 53
**原文：** The camera simultaneously travels upward. Trajectory: thigh → waist → torso → side orbit → rapid dodge → shoulder region.

**关键词与术语：**
- simultaneously /ˌsaɪməlˈteɪniəsli/ adv.：同时地
- waist /weɪst/ n.：腰部

**整段翻译：**  
摄影机同时向上飞行。路径：大腿 → 腰部 → 躯干 → 侧向环绕 → 快速闪避 → 肩部区域。

## 段落 54
**原文：** The camera changes direction multiple times. No straight flight. No pause.

**关键词与术语：**
- straight flight /streɪt flaɪt/ n. phr.：直线飞行

**整段翻译：**  
摄影机必须多次改变方向。禁止直线飞行，禁止停顿。

# FIRST HIGH-SPEED DODGE SEQUENCE｜第一次高速闪避序列

## 段落 55
**原文：** As the person changes pose: leg moves → camera rapidly shifts sideways. Arm moves → camera drops. Torso rotates → camera curves around it. Shoulder changes → camera redirects outward.

**关键词与术语：**
- sideways /ˈsaɪdweɪz/ adv.：向侧方
- drop /drɑːp/ v.：向下移动

**整段翻译：**  
人物改变姿态时：腿移动 → 摄影机快速横移；手臂移动 → 摄影机下降；躯干旋转 → 摄影机沿躯干弧线绕行；肩部变化 → 摄影机向外重新定向。

## 段落 56
**原文：** Each dodge happens immediately. The camera remains fast. The person never stops moving. The camera never waits.

**整段翻译：**  
每次闪避都要立即发生。摄影机持续高速，人物持续运动，摄影机绝不等待。

## 段落 57
**原文：** At approximately 5 seconds: the person's pose clearly resolves into Picture 2.

**关键词与术语：**
- resolve into /rɪˈzɑːlv ˈɪntuː/ v. phr.：最终明确收束为

**整段翻译：**  
约第 5 秒时，人物姿态应清楚收束为 Picture 2。

# 5.0–7.5s｜PICTURE 2 — RAPID ORBIT

## 段落 58
**原文：** Do NOT freeze on Picture 2. Immediately continue.

**整段翻译：**  
到达 Picture 2 后不要冻结，必须立即继续运动。

## 段落 59
**原文：** The camera performs a rapid ascending 3/4 orbit around the person.

**关键词与术语：**
- ascending /əˈsendɪŋ/ adj.：向上升的
- 3/4 orbit /ˌθriː ˈkwɔːrtər ˈɔːrbɪt/ n. phr.：三分之四角度环绕

**整段翻译：**  
摄影机围绕人物完成一次快速向上的三分之四角度环绕。

## 段落 60
**原文：** Use several trajectory changes: forward → lateral → upward → outward → inward → orbital redirection.

**关键词与术语：**
- inward /ˈɪnwərd/ adv.：向内
- orbital redirection /ˈɔːrbɪtl ˌriːdəˈrekʃən/ n. phr.：环绕中的重新定向

**整段翻译：**  
连续使用多次轨迹变化：向前 → 横向 → 向上 → 向外 → 向内 → 环绕重新定向。

## 段落 61
**原文：** The camera passes extremely close to: waist, torso, shoulder, arm.

**整段翻译：**  
摄影机极近距离掠过腰部、躯干、肩膀和手臂。

## 段落 62
**原文：** The body should feel enormous. Foreground elements sweep rapidly across the frame. Strong spatial parallax. Continuous momentum.

**关键词与术语：**
- enormous /ɪˈnɔːrməs/ adj.：巨大无比的
- spatial parallax /ˈspeɪʃəl ˈpærəlæks/ n. phr.：空间视差

**整段翻译：**  
身体必须显得非常巨大。前景元素高速掠过画面，形成强烈空间视差，并保持连续动量。

# PICTURE 2 MICRO-MOVEMENTS｜Picture 2 微动作

## 段落 63
**原文：** While the camera orbits, the person performs several subtle editorial movements.

**关键词与术语：**
- editorial movement /ˌedɪˈtɔːriəl ˈmuːvmənt/ n. phr.：时尚编辑摄影式微动作

**整段翻译：**  
摄影机环绕过程中，人物完成多个细微的编辑摄影式姿态调整。

## 段落 64
**原文：** Examples: small shoulder rotation → head movement → arm adjustment → torso shift → slight body turn → return toward the Picture 2 configuration.

**关键词与术语：**
- configuration /kənˌfɪɡjəˈreɪʃən/ n.：整体姿态配置

**整段翻译：**  
例如：小幅肩部旋转 → 头部运动 → 手臂微调 → 躯干位移 → 轻微身体转向 → 回到接近 Picture 2 的姿态配置。

## 段落 65
**原文：** Do not create dance choreography. These are continuous professional-model pose adjustments. The person must never look frozen.

**关键词与术语：**
- professional-model /prəˈfeʃənəl ˈmɑːdəl/ adj.：职业模特式的
- pose adjustment /poʊz əˈdʒʌstmənt/ n. phr.：姿态微调

**整段翻译：**  
不要创建舞蹈编舞。这些只是职业模特式连续姿态微调。人物绝不能看起来冻结不动。

# 7.5–9.5s｜PICTURE 2 → PICTURE 3

## 段落 66
**原文：** The person now rapidly transitions toward Picture 3. Use multiple connected movements. Do not morph. Do not crossfade. Do not teleport.

**关键词与术语：**
- morph /mɔːrf/ v.：形变过渡
- crossfade /ˈkrɔːsfeɪd/ v.：交叉淡化
- teleport /ˈteləpɔːrt/ v.：瞬移

**整段翻译：**  
人物现在快速向 Picture 3 过渡，必须使用多个连续动作。不要形变、不要交叉淡化、不要瞬移。

## 段落 67
**原文：** The camera simultaneously becomes faster. Camera trajectory: side orbit → rapid shoulder dodge → upward acceleration → head-side arc → three-quarter approach.

**关键词与术语：**
- head-side arc /hed saɪd ɑːrk/ n. phr.：沿头部侧面的弧线路径
- approach /əˈproʊtʃ/ n.：接近

**整段翻译：**  
与此同时摄影机进一步加速。轨迹：侧向环绕 → 快速闪避肩膀 → 向上加速 → 沿头部侧面弧线移动 → 三分之四角度接近。

## 段落 68
**原文：** The camera must dynamically avoid every moving body part. The person continues moving normally. The camera is the only thing performing evasive maneuvers.

**关键词与术语：**
- dynamically /daɪˈnæmɪkli/ adv.：动态地
- evasive maneuver /ɪˈveɪsɪv məˈnuːvər/ n. phr.：规避机动

**整段翻译：**  
摄影机必须动态避开每个正在运动的身体部位。人物继续正常运动，只有摄影机负责做规避机动。

## 段落 69
**原文：** At approximately 9.5 seconds: the person's body clearly resolves into Picture 3.

**整段翻译：**  
约第 9.5 秒时，人物身体姿态应清楚收束到 Picture 3。

# 9.5–11.8s｜PICTURE 3 — HIGH-SPEED UPPER-BODY ORBIT

## 段落 70
**原文：** Picture 3 is now established. Do not stop. Immediately perform a fast upper-body orbit.

**关键词与术语：**
- upper-body orbit /ˌʌpər ˈbɑːdi ˈɔːrbɪt/ n. phr.：围绕上半身环绕

**整段翻译：**  
Picture 3 姿态已经确立。不要停，立即围绕上半身快速环绕。

## 段落 71
**原文：** Trajectory: torso → shoulder → side of head → behind shoulder silhouette → three-quarter face.

**关键词与术语：**
- silhouette /ˌsɪluˈet/ n.：轮廓 / 剪影

**整段翻译：**  
轨迹：躯干 → 肩部 → 头部侧面 → 肩后轮廓区域 → 三分之四人脸。

## 段落 72
**原文：** Use approximately 90–150 degrees of orbital movement. Do not make it a slow 360-degree rotation.

**整段翻译：**  
环绕角度约 90–150 度，不要做缓慢 360 度完整绕圈。

## 段落 73
**原文：** The camera remains extremely close. The face gradually becomes dominant.

**关键词与术语：**
- dominant /ˈdɑːmɪnənt/ adj.：占据视觉主导的

**整段翻译：**  
摄影机始终极近距离，人物脸部逐渐成为画面主导。

# FINAL BODY AVOIDANCE｜最终身体闪避

## 段落 74
**原文：** If the person performs any final head, shoulder or arm movement: camera immediately changes trajectory.

**整段翻译：**  
如果人物在最后阶段发生任何头部、肩部或手臂运动，摄影机必须立即改变轨迹。

## 段落 75
**原文：** Head moves → lateral camera dodge. Shoulder moves → outward arc. Hair moves → camera shifts around it. Arm moves → camera drops or redirects.

**整段翻译：**  
头部移动 → 摄影机横向闪避；肩部移动 → 向外绕弧；头发移动 → 摄影机绕开头发；手臂移动 → 摄影机下降或重新定向。

## 段落 76
**原文：** The camera never collides. The camera never slows down simply to avoid the body.

**关键词与术语：**
- collide /kəˈlaɪd/ v.：碰撞

**整段翻译：**  
摄影机永远不能碰撞，也不能仅仅为了避开身体而明显减速。

# 11.8–13.5s｜FACE APPROACH

## 段落 77
**原文：** Accelerate toward the face. This is a rapid spatial approach. Do NOT zoom. The camera physically moves closer.

**关键词与术语：**
- spatial approach /ˈspeɪʃəl əˈproʊtʃ/ n. phr.：真实空间接近
- zoom /zuːm/ v.：变焦

**整段翻译：**  
向人脸加速接近。这必须是真实空间中的快速接近，而不是变焦；摄影机本体实际向脸部飞近。

## 段落 78
**原文：** Approach from a three-quarter angle. Then perform a very short frontal arc.

**关键词与术语：**
- frontal arc /ˈfrʌntl ɑːrk/ n. phr.：正面短弧线

**整段翻译：**  
先从三分之四角度接近，然后做一段非常短的正面弧线运动。

## 段落 79
**原文：** The face becomes extremely large in frame. The person's identity must remain exact. No face transformation. No facial distortion.

**关键词与术语：**
- face transformation /feɪs ˌtrænsfərˈmeɪʃən/ n. phr.：脸部形变 / 身份变化
- facial distortion /ˈfeɪʃəl dɪˈstɔːrʃən/ n. phr.：面部扭曲

**整段翻译：**  
人脸在画面中变得极大，但人物身份必须保持精确一致。禁止脸部变化，禁止面部扭曲。

# 13.5–15s｜EXTREME FAST PULL-BACK

## 段落 80
**原文：** Immediately reverse camera momentum. Rapidly accelerate backward.

**关键词与术语：**
- reverse momentum /rɪˈvɜːrs moʊˈmentəm/ v. phr.：反转运动动量
- backward /ˈbækwərd/ adv.：向后

**整段翻译：**  
立即反转摄影机动量，并高速向后加速。

## 段落 81
**原文：** This must feel like a sudden high-speed spatial retreat. Do NOT use digital zoom. The camera physically flies backward.

**关键词与术语：**
- spatial retreat /ˈspeɪʃəl rɪˈtriːt/ n. phr.：空间后撤
- digital zoom /ˈdɪdʒɪtl zuːm/ n. phr.：数字变焦

**整段翻译：**  
这一运动必须像突然的高速空间后撤。不要使用数字变焦，摄影机必须真实向后飞离。

## 段落 82
**原文：** The giant-scale perspective rapidly decreases. The person's upper body becomes visible. Continue until the frame reaches a HALF-BODY PORTRAIT.

**关键词与术语：**
- half-body portrait /ˌhæf ˈbɑːdi ˈpɔːrtrət/ n. phr.：半身肖像

**整段翻译：**  
巨大尺度透视迅速减弱，人物上半身重新进入画面，直到构图达到**半身肖像**。

# FINAL HERO FRAME｜最终 Hero Frame

## 段落 83
**原文：** At approximately 14 seconds: reach the Picture 3 half-body composition.

**整段翻译：**  
约第 14 秒时，达到 Picture 3 对应的半身构图。

## 段落 84
**原文：** The final composition should clearly correspond to Picture 3. Show: head, shoulders, upper torso.

**关键词与术语：**
- correspond to /ˌkɔːrəˈspɑːnd tuː/ v. phr.：与……明确对应
- upper torso /ˌʌpər ˈtɔːrsoʊ/ n. phr.：上躯干

**整段翻译：**  
最终构图必须清楚对应 Picture 3，只展示头部、肩膀和上躯干。

## 段落 85
**原文：** Do not show full body. Do not pull farther away. Do not reveal a large environment.

**整段翻译：**  
不要展示全身，不要继续拉远，也不要突然揭示大范围环境。

## 段落 86
**原文：** From approximately 14–15 seconds: HOLD. The final frame is the Picture 3 hero portrait.

**关键词与术语：**
- hold /hoʊld/ v.：保持画面

**整段翻译：**  
约 14–15 秒：**保持**。最后一帧就是 Picture 3 对应的 Hero Portrait。

# CAMERA MOVEMENT DENSITY｜摄影机运动密度

## 段落 87
**原文：** The camera should perform MANY movement changes during the 15 seconds.

**整段翻译：**  
15 秒内摄影机应发生**大量方向和运动方式变化**。

## 段落 88
**原文：** Avoid long single-direction travel.

**关键词与术语：**
- single-direction travel /ˌsɪŋɡəl dəˈrekʃən ˈtrævəl/ n. phr.：长时间单一方向移动

**整段翻译：**  
避免长时间单一方向飞行。

## 段落 89
**原文：** Use frequent transitions: forward → lateral → curve → upward → dodge → orbit → redirect → accelerate → dodge → reverse.

**整段翻译：**  
频繁切换：向前 → 横向 → 曲线 → 向上 → 闪避 → 环绕 → 重新定向 → 加速 → 闪避 → 反向。

## 段落 90
**原文：** The camera trajectory should constantly evolve.

**关键词与术语：**
- evolve /ɪˈvɑːlv/ v.：持续演化

**整段翻译：**  
摄影机轨迹必须持续演化。

## 段落 91
**原文：** The viewer should continuously feel: "I don't know exactly where the tiny camera will move next." But the movement must remain physically coherent.

**关键词与术语：**
- physically coherent /ˈfɪzɪkli koʊˈhɪrənt/ adj. phr.：在物理空间中连续自洽的

**整段翻译：**  
观众应持续产生这样的感觉：“我无法准确预测这台微型摄影机下一步会飞到哪里。”但所有运动必须仍然符合物理空间连续性。

# PERSON MOVEMENT DENSITY｜人物动作密度

## 段落 92
**原文：** The person should perform multiple visible movements throughout the video.

**整段翻译：**  
人物在整条视频中应持续完成多个肉眼可见的动作变化。

## 段落 93
**原文：** Between Picture 1 and Picture 2: at least several connected body adjustments. Between Picture 2 and Picture 3: at least several connected body adjustments.

**整段翻译：**  
Picture 1 与 Picture 2 之间至少包含多个连续身体调整；Picture 2 与 Picture 3 之间同样至少包含多个连续身体调整。

## 段落 94
**原文：** These movements can include: leg movement, weight transfer, torso rotation, arm repositioning, shoulder movement, head turn, body orientation change.

**关键词与术语：**
- orientation /ˌɔːriənˈteɪʃən/ n.：朝向

**整段翻译：**  
这些动作可以包括：腿部运动、重心转移、躯干旋转、手臂重新定位、肩部运动、转头、身体朝向变化。

## 段落 95
**原文：** All intermediate movements must naturally lead toward the next reference pose. Do not add unrelated dance choreography.

**整段翻译：**  
所有中间动作都必须自然导向下一个参考姿态，不要加入无关舞蹈编排。

# NO STATIC SECTIONS｜禁止静态段落

## 段落 96
**原文：** Do NOT allow: long static pose.

**整段翻译：**  
禁止长时间静态姿态。

## 段落 97
**原文：** Do NOT allow: camera flying around a completely frozen person.

**整段翻译：**  
禁止摄影机围绕一个完全冻结的人物空转。

## 段落 98
**原文：** Do NOT allow: several seconds of empty camera movement.

**关键词与术语：**
- empty camera movement /ˈempti ˈkæmərə ˈmuːvmənt/ n. phr.：没有人物动作配合的空运镜

**整段翻译：**  
禁止出现持续几秒、缺乏人物动作配合的空运镜。

## 段落 99
**原文：** Both camera and person should remain active. Camera movement = continuous. Person movement = frequent.

**整段翻译：**  
摄影机和人物都必须保持活跃：摄影机运动 = 连续；人物运动 = 高频发生。

# PHYSICAL CAMERA LOGIC｜摄影机物理逻辑

## 段落 100
**原文：** The camera is a real moving point in 3D space.

**关键词与术语：**
- moving point /ˈmuːvɪŋ pɔɪnt/ n. phr.：运动点
- 3D space /ˌθriː ˈdiː speɪs/ n. phr.：三维空间

**整段翻译：**  
摄影机必须被视为三维空间中的一个真实运动点。

## 段落 101
**原文：** Perspective changes according to actual camera position. Closer body parts move faster across frame. Distant background moves differently.

**关键词与术语：**
- according to /əˈkɔːrdɪŋ tuː/ phr.：依据
- distant background /ˈdɪstənt ˈbækɡraʊnd/ n. phr.：远处背景

**整段翻译：**  
透视必须根据真实摄影机位置变化。距离摄影机更近的身体部位应更快掠过画面，远处背景则以不同速度移动。

## 段落 102
**原文：** Camera acceleration has momentum. Camera deceleration has momentum. Camera turns through physical arcs.

**关键词与术语：**
- deceleration /ˌdiːseləˈreɪʃən/ n.：减速
- physical arc /ˈfɪzɪkəl ɑːrk/ n. phr.：真实空间弧线

**整段翻译：**  
摄影机加速要体现动量，减速也要体现动量；转向必须沿真实空间弧线完成。

## 段落 103
**原文：** Camera cannot teleport. Camera cannot pass through solid geometry.

**关键词与术语：**
- solid geometry /ˈsɑːlɪd dʒiˈɑːmətri/ n. phr.：实体几何结构

**整段翻译：**  
摄影机不能瞬移，也不能穿过任何实体几何结构。

# OPTICAL BEHAVIOR｜光学行为

## 段落 104
**原文：** Use realistic perspective. Strong perspective during close passes. Natural motion blur during high-speed movement. Natural depth changes. Natural focus transitions.

**关键词与术语：**
- motion blur /ˈmoʊʃən blɜːr/ n. phr.：运动模糊
- depth change /depθ tʃeɪndʒ/ n. phr.：景深 / 空间深度变化
- focus transition /ˈfoʊkəs trænˈzɪʃən/ n. phr.：焦点过渡 / 拉焦

**整段翻译：**  
使用真实透视。近距离掠过时要有强透视，高速运动时产生自然运动模糊，并保持自然的空间深度变化与焦点过渡。

## 段落 105
**原文：** No extreme fisheye. No warped face. No stretched body parts. No artificial distortion.

**关键词与术语：**
- fisheye /ˈfɪʃaɪ/ n.：鱼眼
- warped /wɔːrpt/ adj.：扭曲的
- stretched /stretʃt/ adj.：被异常拉长的
- distortion /dɪˈstɔːrʃən/ n.：畸变

**整段翻译：**  
不要极端鱼眼，不要人脸扭曲，不要身体部位异常拉伸，也不要人工畸变。

# VISUAL APPEARANCE｜视觉外观

## 段落 106
**原文：** The input images determine the visual appearance. Do not redesign or reinterpret the appearance. Do not create a new visual style. Do not create a new visual treatment.

**关键词与术语：**
- visual treatment /ˈvɪʒuəl ˈtriːtmənt/ n. phr.：视觉处理方式

**整段翻译：**  
输入图决定视觉外观。不要重新设计或重新解释外观，不要创造新的视觉风格，也不要添加新的视觉处理体系。

## 段落 107
**原文：** The camera movement is independent from the visual appearance. The reference images remain the visual source throughout the video.

**关键词与术语：**
- independent from /ˌɪndɪˈpendənt frəm/ phr.：与……相互独立

**整段翻译：**  
摄影机运动与视觉外观是两个独立维度。参考图始终是整个视频的视觉来源。

# ABSOLUTE NEGATIVE CONSTRAINTS｜绝对负向约束

## 段落 108｜摄影机形态禁止项
**原文：** NO bee. NO insect. NO wings. NO insect body. NO flying creature. NO drone. NO visible camera. NO camera operator. NO third-person view.

**关键词与术语：**
- flying creature /ˈflaɪɪŋ ˈkriːtʃər/ n. phr.：飞行生物
- camera operator /ˈkæmərə ˈɑːpəreɪtər/ n. phr.：摄影师
- third-person view /ˌθɜːrd ˈpɜːrsən vjuː/ n. phr.：第三人称视角

**整段翻译：**  
禁止蜜蜂、昆虫、翅膀、昆虫身体、任何飞行生物、无人机、可见摄影机、摄影师以及第三人称视角。

## 段落 109｜人物反应禁止项
**原文：** NO static person. NO frozen person. NO person avoiding the camera. NO person reacting to the camera. NO person moving away from the camera specifically to avoid collision.

**关键词与术语：**
- frozen person /ˈfroʊzən ˈpɜːrsən/ n. phr.：冻结不动的人
- specifically /spəˈsɪfɪkli/ adv.：专门为了某一目的

**整段翻译：**  
禁止静止人物、冻结人物、人物主动躲摄影机、人物对摄影机作出反应，以及人物为了避碰而特意远离摄影机。

## 段落 110｜姿态过渡禁止项
**原文：** NO slideshow. NO crossfade. NO image morphing. NO instant pose replacement. NO teleportation. NO slow pose transitions. NO long static pose.

**关键词与术语：**
- slideshow /ˈslaɪdʃoʊ/ n.：幻灯片式切换
- image morphing /ˈɪmɪdʒ ˈmɔːrfɪŋ/ n. phr.：图像形变
- instant pose replacement /ˈɪnstənt poʊz rɪˈpleɪsmənt/ n. phr.：瞬间替换姿态
- teleportation /ˌteləpɔːrˈteɪʃən/ n.：瞬移

**整段翻译：**  
禁止幻灯片、交叉淡化、图像形变、瞬间替换姿态、瞬移、缓慢姿态过渡以及长时间静态姿态。

## 段落 111｜运镜失败模式禁止项
**原文：** NO long slow camera movement. NO slow hovering. NO fixed foot orbit. NO staying around the feet. NO straight feet-to-head flight. NO single-direction flight. NO repetitive orbit. NO slow 360-degree spin.

**关键词与术语：**
- hovering /ˈhʌvərɪŋ/ n.：悬停
- fixed foot orbit /fɪkst fʊt ˈɔːrbɪt/ n. phr.：固定围绕脚部环绕
- repetitive orbit /rɪˈpetətɪv ˈɔːrbɪt/ n. phr.：重复环绕

**整段翻译：**  
禁止长时间慢运镜、慢速悬停、固定绕脚、一直停留在脚部、从脚到头的直线飞行、单一方向飞行、重复环绕，以及缓慢 360 度旋转。

## 段落 112｜碰撞与穿模禁止项
**原文：** NO camera collision. NO camera passing through body. NO camera passing through limbs. NO camera passing through clothing. NO camera passing through hair. NO clipping. NO impossible camera positions.

**关键词与术语：**
- clipping /ˈklɪpɪŋ/ n.：穿模
- impossible camera position /ɪmˈpɑːsəbl ˈkæmərə pəˈzɪʃən/ n. phr.：物理上不可能的机位

**整段翻译：**  
禁止摄影机碰撞、穿过身体、四肢、服装或头发；禁止穿模；禁止物理上不可能的机位。

## 段落 113｜图像质量与身份禁止项
**原文：** NO random camera shake. NO floating camera. NO fisheye distortion. NO face distortion. NO body deformation. NO extra limbs. NO identity drift. NO clothing changes. NO hairstyle changes.

**关键词与术语：**
- random camera shake /ˈrændəm ˈkæmərə ʃeɪk/ n. phr.：随机抖动
- body deformation /ˈbɑːdi ˌdiːfɔːrˈmeɪʃən/ n. phr.：身体变形
- extra limb /ˈekstrə lɪm/ n. phr.：额外肢体
- identity drift /aɪˈdentəti drɪft/ n. phr.：身份漂移

**整段翻译：**  
禁止随机摄影机抖动、漂浮式摄影机、鱼眼畸变、人脸扭曲、身体变形、额外肢体、身份漂移、服装变化和发型变化。

## 段落 114｜结尾禁止项
**原文：** NO distant final shot. NO full-body final frame. NO wide ending.

**关键词与术语：**
- distant final shot /ˈdɪstənt ˈfaɪnəl ʃɑːt/ n. phr.：远距离最终镜头
- wide ending /waɪd ˈendɪŋ/ n. phr.：广角 / 大景别结尾

**整段翻译：**  
禁止远距离最终镜头，禁止全身最终画面，禁止大景别收尾。

# FINAL CREATIVE INTENT｜最终创作意图

## 段落 115
**原文：** Create ONE extremely fast continuous 15-second first-person flight.

**整段翻译：**  
创建**一条**极高速、连续 15 秒的第一人称飞行镜头。

## 段落 116
**原文：** The tiny invisible camera begins at the person's feet. It immediately accelerates upward. It does not stay at the feet.

**整段翻译：**  
微型不可见摄影机从人物脚部开始，立即向上加速，并且不能停留在脚部。

## 段落 117
**原文：** It continuously moves upward while orbiting, curving and rapidly changing direction around the gigantic moving person.

**整段翻译：**  
摄影机持续向上飞，同时围绕这个相对巨大的运动人物进行环绕、曲线飞行与快速变向。

## 段落 118
**原文：** The person is NOT avoiding the camera. The person actively performs multiple natural pose movements.

**整段翻译：**  
人物**不是**在躲摄影机；人物主动完成多个自然姿态动作。

## 段落 119
**原文：** The person transitions: Picture 1 → multiple intermediate movements → Picture 2 → multiple intermediate movements → Picture 3.

**整段翻译：**  
人物动作路径：Picture 1 → 多个中间动作 → Picture 2 → 多个中间动作 → Picture 3。

## 段落 120
**原文：** The camera simultaneously predicts and avoids the moving body.

**整段翻译：**  
摄影机同时预判并闪避正在运动的身体。

## 段落 121
**原文：** Leg enters trajectory: camera dodges. Arm enters trajectory: camera dodges. Torso rotates: camera redirects. Shoulder moves: camera orbits. Head turns: camera changes angle.

**整段翻译：**  
腿进入轨迹：摄影机闪避。手臂进入轨迹：摄影机闪避。躯干旋转：摄影机重新定向。肩部移动：摄影机环绕。头部转动：摄影机改变角度。

## 段落 122
**原文：** The camera remains FAST throughout. There are no long pauses. There are many camera direction changes. There are many visible human movement changes.

**整段翻译：**  
摄影机全程保持**高速**。没有长停顿，摄影机方向频繁变化，人物也持续出现大量肉眼可见的动作变化。

## 段落 123
**原文：** The camera finally reaches the face, rapidly reverses direction and performs an extremely fast physical pull-back.

**关键词与术语：**
- physical pull-back /ˈfɪzɪkəl ˈpʊlbæk/ n. phr.：真实空间后拉

**整段翻译：**  
摄影机最终到达人脸附近，然后迅速反向，并完成一次极高速的真实空间后撤。

## 段落 124
**原文：** It resolves into the Picture 3 half-body hero composition. The final frame holds for the last moment.

**整段翻译：**  
镜头最终收束到 Picture 3 对应的半身 Hero Composition，并在最后时刻保持最终画面。

## 段落 125
**原文：** The complete result must feel like ONE HIGH-SPEED, CONTINUOUS, THREE-POSE EDITORIAL CAMERA FLIGHT rather than three static images connected together.

**关键词与术语：**
- editorial camera flight /ˌedɪˈtɔːriəl ˈkæmərə flaɪt/ n. phr.：编辑摄影式摄影机飞行
- static image /ˈstætɪk ˈɪmɪdʒ/ n. phr.：静态图像

**整段翻译：**  
最终完整结果必须像**一次高速、连续、贯穿三个姿态的编辑摄影式摄影机飞行**，而不是三张静态图片被简单连接起来。
