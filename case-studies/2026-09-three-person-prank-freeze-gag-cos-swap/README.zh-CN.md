# 案例研究 009 — 三人恶作剧逆向工程：定格笑点 + 仅换皮 COS 替换｜逐段翻译

> 对应原始 `README.md`。每段先列关键词、术语和概念（IPA、词性缩写、简体中文释义），再给出整段简体中文译文。

## Inputs｜输入

### 段落 1
**原文：** **No reference image** — pure **T2VA** rebuild

**关键词与术语：**
- T2VA /ˌtiː tuː viː ˈeɪ/ n.：Text-to-Video/Audio，纯文本生成视频与音频
- rebuild /ˌriːˈbɪld/ n./v.：重建 / 重新构建

**整段翻译：**  
**不使用参考图**——纯 **T2VA** 重建。

### 段落 2
**原文：** Source: a 15-second real UGC vertical prank clip (9:16), reverse-engineered frame-by-frame

**关键词与术语：**
- UGC /ˌjuː dʒiː ˈsiː/ n.：User-Generated Content，用户生成内容
- reverse-engineer /ˌriːvɜːrs ˌendʒɪˈnɪr/ v.：逆向工程
- frame-by-frame /ˌfreɪm baɪ ˈfreɪm/ adv.：逐帧地

**整段翻译：**  
来源是一条 15 秒真人 UGC 竖屏恶作剧视频（9:16），通过逐帧逆向工程重建。

### 段落 3
**原文：** Target: **~15 seconds**, vertical **9:16 / 24fps**, photorealistic live-action (real human cosplayers, NOT anime)

**关键词与术语：**
- photorealistic /ˌfoʊtoʊˌriːəˈlɪstɪk/ adj.：照片级写实的
- live-action /ˌlaɪv ˈækʃən/ adj.：真人实拍的
- cosplayer /ˈkɑːzpleɪər/ n.：角色扮演者

**整段翻译：**  
目标约 15 秒，9:16 竖屏、24fps，照片级真人实拍质感；必须是真人 coser，**不是动画**。

### 段落 4
**原文：** Two characters reskinned to *Detective Conan* cosplay: Girl A = Hagiwara Chihaya (traffic-police cos), Girl B = Elena Miyano (scientist cos)

**关键词与术语：**
- reskin /ˌriːˈskɪn/ v.：只替换外观 / 换皮
- traffic-police /ˈtræfɪk pəˈliːs/ n. phr.：交通警察
- scientist /ˈsaɪəntɪst/ n.：科学家

**整段翻译：**  
两个角色只做《名侦探柯南》COS 换皮：Girl A = 萩原千速（交警 COS），Girl B = 宫野艾莲娜（科学家 COS）。

### 段落 5
**原文：** Prompt language: **English** structured sections with two short spoken **Japanese** exclamations

**关键词与术语：**
- exclamation /ˌekskləˈmeɪʃən/ n.：感叹词 / 短促惊呼

**整段翻译：**  
提示词主体为**英文结构化模块**，其中包含两句短促的**日语感叹**。

### 段落 6
**原文：** Result render: `result-video.mp4` (0.8-resolution, with audio)

**关键词与术语：**
- render /ˈrendər/ n.：渲染结果

**整段翻译：**  
结果文件：`result-video.mp4`，0.8 分辨率生成，包含音频。

## The problem｜问题

### 段落 7
**原文：** This is the journal's first **reverse-engineering** entry — the prompt was not designed from scratch, it had to be recovered from an existing clip. Three failure modes appeared on the first naive pass:

**关键词与术语：**
- from scratch /frəm skrætʃ/ adv. phr.：从零开始
- recover /rɪˈkʌvər/ v.：从结果中还原
- failure mode /ˈfeɪljər moʊd/ n. phr.：失败模式
- naive pass /naɪˈiːv pæs/ n. phr.：未经充分验证的初步尝试

**整段翻译：**  
这是日志中第一个**逆向工程**案例——提示词不是从零设计，而是必须从现有视频中还原。第一次直接尝试时出现三类失败模式：

### 段落 8｜失败 1
**原文：** **The invisible third actor.** The camera-holder is also the prankster, but only a green sleeve, a green scooter fairing and an occasional hand ever enter frame. A sparse frame walk reads those as clutter and treats the camera as a neutral observer — which inverts the whole plot.

**关键词与术语：**
- camera-holder /ˈkæmərə ˈhoʊldər/ n.：持机者
- prankster /ˈpræŋkstər/ n.：恶作剧者
- scooter fairing /ˈskuːtər ˈferɪŋ/ n. phr.：踏板车整流罩 / 外壳
- sparse frame walk /spɑːrs freɪm wɔːk/ n. phr.：低密度抽帧检查
- clutter /ˈklʌtər/ n.：无关杂物
- neutral observer /ˈnuːtrəl əbˈzɜːrvər/ n. phr.：中立观察者
- invert /ɪnˈvɜːrt/ v.：颠倒

**整段翻译：**  
**不可见的第三行动者。** 持机者本身就是恶作剧实施者，但画面里通常只出现绿色袖子、绿色踏板车外壳和偶尔伸入的一只手。低密度抽帧很容易把这些当成杂乱背景，把摄影机错误理解成中立观察者，从而把整个剧情因果关系颠倒。

### 段落 9｜失败 2
**原文：** **The one-to-many inverse problem.** Different scripts produce near-identical frames. At low sampling rate, "she sprays herself" and "an off-camera hand turns her head so she sprays her friend" look the same; the 3–5-frame helmet-grab that decides between them disappears entirely.

**关键词与术语：**
- one-to-many inverse problem /ˌwʌn tə ˈmeni ˈɪnvɜːrs ˈprɑːbləm/ n. phr.：一对多逆问题；同一画面可能对应多个不同因果脚本
- sampling rate /ˈsæmplɪŋ reɪt/ n. phr.：采样率
- off-camera /ˌɔːf ˈkæmərə/ adj.：画外的
- helmet-grab /ˈhelmɪt ɡræb/ n. phr.：抓住头盔的短动作

**整段翻译：**  
**一对多逆问题。** 不同脚本可能生成几乎相同的静态帧。在低采样率下，“她喷到自己”和“画外一只手把她的头转向朋友，导致她喷到朋友”看起来可能完全一样；真正决定两种解释的 3–5 帧抓头盔动作会被彻底漏掉。

### 段落 10｜失败 3
**原文：** **Freeze frames mistaken for acting.** The three half-second shock holds are *post-production*, not people freezing on set. Writing them as action freezes the characters instead of the edit.

**关键词与术语：**
- freeze frame /friːz freɪm/ n.：定格帧
- shock hold /ʃɑːk hoʊld/ n. phr.：震惊定格
- post-production /ˌpoʊst prəˈdʌkʃən/ n.：后期制作
- on set /ɑːn set/ phr.：拍摄现场

**整段翻译：**  
**把定格帧误判成人物表演。** 三个约半秒的震惊停顿其实是**后期定格**，不是演员在现场真的突然不动。如果把它们写进动作层，模型会冻结人物，而不是冻结剪辑画面。

## The breakthrough｜关键突破

### 段落 11
**原文：** **Five-channel forensics + a frozen causal skeleton.**

**关键词与术语：**
- forensics /fəˈrensɪks/ n.：取证式分析
- causal skeleton /ˈkɔːzəl ˈskelɪtn/ n. phr.：因果骨架
- frozen /ˈfroʊzən/ adj.：固定不可改动的

**整段翻译：**  
核心突破是：**五通道取证分析 + 冻结的因果骨架**。

### 段落 12
**原文：** Dense 4–8fps extraction over each ambiguous window adjudicated between competing plot hypotheses instead of confirming the most common one; a 0.5s RMS envelope located three energy peaks, and every peak was reconciled with a picture cause; a BPM false-detection guard (onset regularity + spectrogram kick grid) correctly ruled that the track has **no music — pure field audio**. What emerged is a strict THREE-BEAT loop:

**关键词与术语：**
- dense extraction /dens ɪkˈstrækʃən/ n. phr.：高密度抽帧
- ambiguous window /æmˈbɪɡjuəs ˈwɪndoʊ/ n. phr.：语义不确定的时间窗口
- adjudicate /əˈdʒuːdɪkeɪt/ v.：判定多个候选解释孰对孰错
- hypothesis /haɪˈpɑːθəsɪs/ n.：假设
- RMS envelope /ˌɑːr em ˈes ˈenvəloʊp/ n. phr.：均方根能量包络
- reconcile /ˈrekənsaɪl/ v.：与另一证据相互核对
- false-detection guard /fɔːls dɪˈtekʃən ɡɑːrd/ n. phr.：误检防护
- onset regularity /ˈɑːnset ˌreɡjəˈlærəti/ n. phr.：起音规律性
- spectrogram /ˈspektrəɡræm/ n.：频谱图
- field audio /fiːld ˈɔːdioʊ/ n. phr.：现场同期声

**整段翻译：**  
针对每个含义不确定的窗口，以 4–8fps 做高密度抽帧，用来在多个剧情假设之间判定，而不是去确认最常见的那个解释；再用 0.5 秒 RMS 能量包络定位三个能量峰，并要求每个声音峰值都能在画面中找到对应原因；同时通过“起音规律性 + 频谱 Kick 网格”的 BPM 误检防护，正确判定音轨中**没有音乐，只有纯现场同期声**。最后还原出严格的三拍循环：

```
骑手挑衅 → 女生含一口水准备反击 → 骑手进行物理干扰 →
反噬发生 → 定格震惊笑点   （×3，逐次升级）
```

### 段落 13
**原文：** The edit layer was then separated cleanly: one unbroken handheld take with exactly three ~0.5s freeze holds, each marked by a micro punch-in + one-frame white flash + a record-scratch→impact→vacuum post-SFX.

**关键词与术语：**
- edit layer /ˈedɪt ˈleɪər/ n. phr.：剪辑层
- unbroken handheld take /ʌnˈbroʊkən ˈhændheld teɪk/ n. phr.：不中断手持镜头
- punch-in /ˈpʌntʃ ɪn/ n.：快速推近 / 后期局部放大
- record scratch /ˈrekərd skrætʃ/ n. phr.：唱片刮擦音
- impact /ˈɪmpækt/ n.：冲击音
- vacuum /ˈvækjuəm/ n.：抽空式静音效果
- post-SFX /poʊst ˌes ef ˈeks/ n.：后期音效

**整段翻译：**  
随后把剪辑层完全独立出来：底层是一条不中断的手持实拍；上层准确加入三个约 0.5 秒定格，每次定格都使用“小幅 Punch-in + 1 帧白闪 + 唱片刮擦 → 冲击 → 瞬间抽空”的后期音效组合。

### 段落 14
**原文：** The **cos swap** was done last, under a "skin-only" contract: timestamps, actions, camera, freeze points and sound structure are frozen; only appearance, costume, and the wet-hair/fabric physics they touch are rewritten. A compatibility check handled the one real dependency — the flip-up visor the gags rely on — and character-specific props (lab gear, drawn duty equipment) were explicitly barred from frame so the setting never changes.

**关键词与术语：**
- skin-only /skɪn ˈoʊnli/ adj.：只换外观层
- timestamp /ˈtaɪmstæmp/ n.：时间戳
- compatibility check /kəmˌpætəˈbɪləti tʃek/ n. phr.：兼容性检查
- dependency /dɪˈpendənsi/ n.：依赖关系
- flip-up visor /ˌflɪp ˈʌp ˈvaɪzər/ n. phr.：可掀起式头盔面罩
- duty equipment /ˈduːti ɪˈkwɪpmənt/ n. phr.：执勤装备
- bar from frame /bɑːr frəm freɪm/ v. phr.：明确禁止进入画面

**整段翻译：**  
**COS 换皮**最后才进行，并严格遵守“只换皮”契约：时间戳、动作、摄影机、定格点和声音结构全部冻结不动；只改人物外观、服装，以及这些外观直接影响的湿发 / 布料物理。随后只对真正存在的依赖做兼容性检查——笑点动作需要可掀起头盔面罩——并明确禁止角色专属道具（实验室装备、拔出的执勤装备）进入画面，以免外观替换反过来改变场景设定。

### 段落 15｜Technique stack

| 技术 | 中文作用 |
|---|---|
| **Dense discriminative sampling** | 对模糊时间窗用 4–8fps 密集采样，在候选剧情中做判别 |
| **Audio-visual reconciliation** | 每个 RMS 峰值必须有画面原因；同时防止 BPM 误检 |
| **Off-camera actor tracking** | 把袖子 / 手 / 车壳归并成一个真实画外行动者 Subject 3 |
| **Layer separation** | 真人动作 / 摄影机 / 剪辑特效 / 声音分别写入独立字段 |
| **N-Beat escalation** | 同一干扰循环重复三次并逐级升级 |
| **Freeze-frame four-tuple** | 定格入点、时长、覆盖效果、恢复方式四项分开定义 |
| **Skin-only reskin** | 冻结因果骨架，只改外观和被外观触及的物理 |

## The named language｜命名语言

### 段落 16
**原文：** **Freeze-Gag Causal Loop with Skin-Only Reskin**

**关键词与术语：**
- causal loop /ˈkɔːzəl luːp/ n. phr.：因果循环
- reskin /ˌriːˈskɪn/ n.：换皮 / 仅改表层角色设定

**整段翻译：**  
**定格笑点因果循环 + 仅换皮 Reskin**

### 段落 17
**原文：** The deliverable is not a description of frames but an executable cause→effect chain a different cast can wear. Once the loop (provoke → charge → sabotage → backfire → freeze) is locked, swapping two original girls for two cosplayers touches `subject_definitions`, `costume_hair_physics`, and the handful of costume words an action physically reaches — and nothing else.

**关键词与术语：**
- deliverable /dɪˈlɪvərəbl/ n.：最终交付物
- executable /ˈeksɪkjuːtəbl/ adj.：可执行的
- cast /kæst/ n.：演员阵容
- provoke /prəˈvoʊk/ v.：挑衅
- sabotage /ˈsæbətɑːʒ/ v.：干扰 / 破坏
- backfire /ˌbækˈfaɪər/ v.：反噬
- costume_hair_physics /ˈkɑːstuːm her ˈfɪzɪks/ n. phr.：服装与头发物理字段

**整段翻译：**  
交付物不是“逐帧描述”，而是一条其他演员也能直接套用的、可执行的因果链。只要“挑衅 → 蓄力 → 干扰 → 反噬 → 定格”的循环锁定，把原来的两个女生换成两个 coser 时，只需要修改 `subject_definitions`、`costume_hair_physics`，以及少量被动作直接触及的服装相关词汇，其他机制全部不动。

## 48-hour takeaway｜48 小时后的关键结论

### 段落 18
**原文：** When reversing footage, **sampling density is a discriminator, not a quality dial**: sparse frames are for building candidate hypotheses, dense frames are for killing the wrong ones. And treat the camera as a *potential actor* until proven otherwise — a purposeful moving object in frame (a hand, a sleeve, a fairing) always has a controller.

**关键词与术语：**
- discriminator /dɪˈskrɪməneɪtər/ n.：判别器 / 用于区分候选解释的手段
- sparse /spɑːrs/ adj.：稀疏的
- candidate hypothesis /ˈkændɪdət haɪˈpɑːθəsɪs/ n. phr.：候选假设
- potential actor /pəˈtenʃəl ˈæktər/ n. phr.：潜在行动主体

**整段翻译：**  
逆向视频时，**采样密度是判别工具，不是画质旋钮**：稀疏抽帧用于建立候选假设，密集抽帧用于淘汰错误假设。同时，在证据证明摄影机只是观察者之前，应把摄影机视为**潜在行动者**；画面中任何带有目的性运动的物体——手、袖子、车壳——背后都存在一个控制者。

### 段落 19
**原文：** When reskinning, freeze the mechanism and rewrite the surface; the moment a costume change starts moving timestamps or beats, it has stopped being a reskin. A replacement table (appearance before/after, plus every carried-over change) is what keeps that boundary honest.

**关键词与术语：**
- mechanism /ˈmekənɪzəm/ n.：机制
- surface /ˈsɜːrfɪs/ n.：表层外观
- replacement table /rɪˈpleɪsmənt ˈteɪbl/ n. phr.：替换对照表
- carried-over /ˈkærid ˌoʊvər/ adj.：连带继承的

**整段翻译：**  
做 Reskin 时，应冻结机制，只改表层；只要服装变化开始推动时间戳或剧情节拍发生改变，它就已经不再是“换皮”。使用替换表——记录修改前 / 修改后外观，以及所有连带变化——可以严格守住这个边界。

### 段落 20
**原文：** This entry is the worked example produced by the companion skill `video-to-h3-prompt` — its five-channel pipeline, freeze-frame recipe and skin-only replacement SOP are documented there.

**关键词与术语：**
- worked example /wɜːrkt ɪɡˈzæmpəl/ n. phr.：完整演算案例
- companion skill /kəmˈpænjən skɪl/ n. phr.：配套技能
- SOP /ˌes oʊ ˈpiː/ n.：Standard Operating Procedure，标准作业流程

**整段翻译：**  
本案例是配套技能 `video-to-h3-prompt` 的完整演算示例；其五通道管线、定格帧方法和只换皮替换 SOP 均在该技能项目中说明。

## The final prompt｜最终提示词

### 段落 21
**原文：** See `prompt.md` for the full paste-ready prompt: short Chinese usage notes followed by the complete English 14-field prompt.

**关键词与术语：**
- paste-ready /ˈpeɪst ˌredi/ adj.：可直接复制使用的
- field /fiːld/ n.：结构化字段

**整段翻译：**  
完整可直接复制的提示词见 `prompt.md`：前面是简短中文使用说明，后面是完整英文 14 字段 Prompt；逐段翻译见 `prompt.zh-CN.md`。

### 段落 22
**整段翻译：**  
字段顺序：
1. `subject_definitions` —— 三个主体；Subject 3 是始终不完整露脸的骑手 / 干扰者
2. `environment_definition` / `lighting_definition` —— 夜间住宅巷道、冷色正面手机补光
3. `integrated_multimodal_description` —— [Shot 1] + 严格递增时间戳 + 三拍循环 + 场内声音
4. `camera_direction` —— 手持第一人称 POV、由干扰动作引发的抖动、定格 Punch-in
5. `editing` —— 一镜到底 + 恰好三次白闪定格笑点
6. `performance` / `body_mechanics` / `costume_hair_physics`
7. `negative_constraints` / `overall_soundscape` / `non_diegetic_music`（明确静音 / 无配乐）

## Result｜结果

### 段落 23
**整段翻译：**  
最终得到约 15 秒、具有一镜到底感的竖屏恶作剧：
- 骑手往 A 的靴子倒水；A 含一口水蓄力，面罩被拍下，攻击被打断并喷到自己面罩——**Freeze 1**；
- A 再次含水，头盔被转向 B，意外喷到 B 的脸 / 眼镜——**Freeze 2**；
- B 喝水准备反击，攻击中途被挡住，反而呛住——**Freeze 3**；
- 两人最后笑成一团，挽着手看向镜头；全片无音乐，只有现场同期声和三次喜剧后期音效。

## Assets｜资产

**整段翻译：**
- `prompt.md`：完整最终 T2VA Prompt，可直接复制
- `result-video.mp4`：生成结果，9:16，约 15 秒，带音频

## Tags｜标签

**中文对应：**  
`#H3` `#提示词工程` `#逆向工程` `#视频转提示词` `#第一人称` `#画外行动者` `#三拍结构` `#定格帧` `#喜剧节奏` `#COS换皮` `#现场同期声` `#竖屏视频` `#T2VA`
