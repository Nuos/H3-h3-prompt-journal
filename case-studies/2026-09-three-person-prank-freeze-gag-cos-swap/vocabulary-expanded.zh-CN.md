# 三人恶作剧与定格笑点：词汇精读增补

v1.1.0 · 2026-09-28。对应 [README](./README.md)、[README 译文](./README.zh-CN.md)、[prompt](./prompt.md)、[prompt 译文](./prompt.zh-CN.md)。源基线 `73f9aa2c7e55f222b06f8547e5e108c56e6a2287`。本文件扩充 50 项词汇，不删改既有译文，不增加动作内容。

IPA 使用常见美式宽式读音；`n.` 名词，`v.` 动词，`adj.` 形容词，`adv.` 副词，`phr.` 短语。解释按反推方法、画外人物、动作因果、剪辑与换装边界分组。

## 一、The problem / five-channel forensics：从画面推断动作

| 编号 | 词汇、IPA、词性 | 基本义 → 本文义、搭配与辨析 |
|---|---|---|
| 01 | reverse-engineer /ˌrɪvɜːrs ˌendʒɪˈnɪr/ v. | 逆向分析、从结果重建生成过程。本文从既有视频推断镜头与动作，不是破解软件或恢复唯一真实脚本。 |
| 02 | sparse /spɑːrs/ adj. | 稀疏的。`sparse frame walk` 指抽帧间隔较大，短暂伸手可能恰好落在两帧之间而被漏掉。 |
| 03 | dense /dens/ adj. | 密集的。`dense extraction` 指在有歧义时增加抽帧密度，区别于提升单张图像分辨率。 |
| 04 | sampling /ˈsæmplɪŋ/ n. | 采样、抽取样本。这里从连续视频抽帧，不是音乐采样器，也不等于生成模型采样步数。 |
| 05 | ambiguous /æmˈbɪɡjuəs/ adj. | 有歧义、容许多种解释的。`ambiguous window` 是短时间段中动作原因尚不清楚，不是画面一定失焦。 |
| 06 | hypothesis /haɪˈpɑːθəsɪs/ n. | 假设、候选解释。复数 hypotheses；不同脚本可产生近似画面，所以假设需要由更多证据区分。 |
| 07 | adjudicate /əˈdʒuːdɪkeɪt/ v. | 裁定、在竞争解释间作判断。这里借用裁定义讨论证据比较，不表示真实法律裁判。 |
| 08 | reconcile /ˈrekənsaɪl/ v. | 对账、使彼此吻合。`reconcile peaks with picture causes` 要给音频能量峰找到可见事件，不能只凭音量大就判音乐强拍。 |
| 09 | envelope /ˈenvəloʊp/ n. | 包络。`RMS envelope` 指音频强弱随时间变化的概括曲线，不是信封，也不是音高曲线。 |
| 10 | onset /ˈɑːnset/ n. | 起始、起音。`onset regularity` 关注声音事件开始时刻是否规律；不等于仅统计所有音量峰。 |

**原句回读：** `sampling density is a discriminator, not a quality dial`。
**译文：** 抽样密度是区分候选解释的工具，不只是调节画质的旋钮。作者讨论的是证据分辨能力，而不是生成画面精细程度。

## 二、subject_definitions / off-camera actor：手、袖子、车头属于谁

| 编号 | 词汇、IPA、词性 | 基本义 → 本文义、搭配与辨析 |
|---|---|---|
| 11 | off-camera /ˌɔːf ˈkæmərə/ adj.; adv. | 画外的、未完整入镜的。拍摄者虽然不露脸，仍是剧情施动者，不应当成不存在。 |
| 12 | rider /ˈraɪdər/ n. | 骑乘者。这里是坐在踏板车上拍摄的第三人，与画面中的两位女生分开。 |
| 13 | scooter /ˈskuːtər/ n. | 踏板车。原文车头下沿作为机位线索，不是任意绿色背景块。 |
| 14 | fairing /ˈferɪŋ/ n. | 车辆外壳、整流罩。`front fairing` 是前部罩壳，不是车轮、车把或人物服饰。 |
| 15 | clutter /ˈklʌtər/ n. | 杂乱物、无关视觉杂项。作者提醒不要把有因果作用的袖子与车头误当 clutter 而丢弃。 |
| 16 | neutral /ˈnuːtrəl/ adj. | 中性的、不介入的。`neutral observer` 指仅观看、不参与事件的摄影机角色；本案第三人显然还在施加动作。 |
| 17 | agent /ˈeɪdʒənt/ n. | 行动者、施动者。这里不是软件智能体，也不是经纪人，而是动作链中的实际执行者。 |
| 18 | interfere /ˌɪntərˈfɪr/ v. | 干预、打断。第三人的手从机位方向介入，使另外人物原定动作改变；不能只译成“出现在画面”。 |
| 19 | sabotage /ˈsæbətɑːʒ/ v.; n. | 蓄意干扰、破坏原本计划。此处用于喜剧反击被打断的机制，不应扩大为新的伤害情节。 |
| 20 | deliberate /dɪˈlɪbərət/ adj. | 有意安排的。与 accidental backfire 对照：第三人有意干预，反击者的失误则是干预的结果。 |

**原句回读：** `Subject 3 films AND sabotages both girls.`
**译文：** 第三人既拍摄，也干扰两位女生。`AND` 强調同一个人物的双重职责。

## 三、integrated_multimodal_description / body_mechanics：因果动词

| 编号 | 词汇、IPA、词性 | 基本义 → 本文义、搭配与辨析 |
|---|---|---|
| 21 | provoke /prəˈvoʊk/ v. | 挑起、激起反应。剧情开头的挑衅引出反击，不是独立于后续的无关动作。 |
| 22 | charge /tʃɑːrdʒ/ v. | 蓄积、准备。`charges a mouthful` 是为后续动作做含水准备，不取“收费、充电”义。 |
| 23 | mouthful /ˈmaʊθfʊl/ n. | 一口所容纳的量。强调先含入口中的水，避免凭空出现喷出的液体。 |
| 24 | puff /pʌf/ v.; n. | 鼓起、短促吹出。`cheeks puffed` 表示鼓起的双颊，是含水准备的可见线索，不是身份脸型永久变大。 |
| 25 | visor /ˈvaɪzər/ n. | 头盔面罩、遮护面屏。`flip-up visor` 可上翻；其 UP / DOWN 状态直接决定水喷到哪里。 |
| 26 | flip-up /ˈflɪp ʌp/ adj. | 可向上翻起的。是面罩机械结构，不代表整个头盔翻转或消失。 |
| 27 | redirect /ˌriːdəˈrekt/ v. | 改向。这里通过外力改变头部朝向，使原本朝摄影者的动作转向另一人；不是后期把水花贴到别处。 |
| 28 | retaliation /rɪˌtæliˈeɪʃən/ n. | 反击。是对前一挑衅作出的剧情响应；本文是喜剧语境，不能扩成新的现实报复建议。 |
| 29 | flinch /flɪntʃ/ v.; n. | 受惊时短促一缩、闪躲反应。区别于提前计划的转身，也不同于持续惊恐表演。 |
| 30 | backfire /ˌbækˈfaɪər/ v.; n. | 反噬、适得其反。反击最终落回自己或误及同伴，表示因果反转，不是发动机真的回火。 |

**原句回读：** `Every spray is preceded by a visible charge`。
**译文：** 每次喷水之前，都先有清楚可见的准备动作。`is preceded by` 的时间方向不能译反：准备在前，喷水在后。

## 四、editing / camera_direction：演员停住与后期定格不是一回事

| 编号 | 词汇、IPA、词性 | 基本义 → 本文义、搭配与辨析 |
|---|---|---|
| 31 | freeze-frame /ˈfriːz freɪm/ n. | 定格帧、用单帧保持一段时间的剪辑处理。这里作用于影像层，不是演员在现场突然保持不动半秒。 |
| 32 | gag /ɡæɡ/ n. | 喜剧笑点、视觉包袱。`shock gag` 是惊讶瞬间的笑点，不取“堵嘴器”义。 |
| 33 | hold /hoʊld/ n.; v. | 保持、停留。`freeze hold` 保持的是画面；其他案例的 pose hold 保持的是人物姿态，宾语不同。 |
| 34 | punch-in /ˈpʌntʃ ɪn/ n. | 突然收紧取景或局部放大的处理。micro punch-in 幅度很小，服务笑点，不是摄影机向角色打拳。 |
| 35 | flash /flæʃ/ n.; v. | 短促闪光。`one-frame white flash` 是持续一帧的白闪，不应延长为持续闪烁灯光。 |
| 36 | overlay /ˈoʊvərleɪ/ n. | 叠加层。指加在基础影像之上的白闪等编辑效果，不是新增剧情角色。 |
| 37 | resume /rɪˈzuːm/ v. | 恢复、继续。定格后恢复正常速度动作，不是从刚才动作开头重新播放。 |
| 38 | jolt /dʒoʊlt/ n.; v. | 短促颠动、猛一震。相机轻晃来自拍摄者手臂干预，需与动作有因果，而非全程任意抖动。 |
| 39 | gimbal /ˈɡɪmbəl/ n. | 云台、稳定支架。`never gimbal-smooth` 要求保留手机手持质感，不是字面在画面里禁放云台器材。 |
| 40 | escalation /ˌeskəˈleɪʃən/ n. | 递进、逐次升级。三次同类笑点要有关系发展，不只是复制同一个反应镜头三遍。 |

**原句回读：** `three deliberate comedic FREEZE-FRAME holds layered on top`。
**译文：** 在基础连续影像之上，叠加三次有意设计的喜剧定格。`layered on top` 说明它们属于剪辑层。

## 五、skin-only reskin / costume_hair_physics / sound

| 编号 | 词汇、IPA、词性 | 基本义 → 本文义、搭配与辨析 |
|---|---|---|
| 41 | reskin /ˌriːˈskɪn/ v.; n. | 换外观、换皮。本文只改角色扮演造型及其涉及的材料响应，不是只换皮肤颜色。 |
| 42 | causal /ˈkɔːzəl/ adj. | 因果的。`causal skeleton` 是谁做什么、造成什么结果的动作骨架，不是人体骨骼模型。 |
| 43 | dependency /dɪˈpendənsi/ n. | 依赖关系。笑点依赖可翻转面罩，因此服装替换不能把这件功能性道具删掉。 |
| 44 | compatibility /kəmˌpætəˈbɪləti/ n. | 相容性。`compatibility check` 检查新造型是否仍能承载原动作，不只检查两种颜色是否协调。 |
| 45 | strand /strænd/ n. | 一缕头发、细条。湿发聚成较重发缕，区别于干发蓬松散开的状态。 |
| 46 | cling /klɪŋ/ v. | 紧贴、黏附。`cling to face and neck` 描述湿发贴在皮肤上，不是自然静止时头发完全不动。 |
| 47 | lag /læɡ/ n.; v. | 滞后。`weighted lag` 指湿发随头部变化略晚，身体先变向、材料后跟随，不是随机落后一整拍。 |
| 48 | diegetic /ˌdaɪəˈdʒetɪk/ adj. | 叙事空间内的。现场说话、倒水、脚步属于故事世界里的声音；不能把它等同“纯器乐”。 |
| 49 | foley /ˈfoʊli/ n. | 拟音，常在后期为动作补录/制作的声音。`no studio-clean foley` 要求别把粗粝手机现场声做得过分洁净，不是否认所有后期音效。 |
| 50 | vacuum /ˈvækjuːm/ n. | 真空；这里比喻声音突然被抽空的近静音段。定格后环境声再恢复，不是场景物理上失去空气。 |

**原句回读：** `freeze the mechanism and rewrite the surface`。
**译文：** 固定动作机制，只重写外在呈现。这里 freeze 是“禁止改动结构”，与剪辑里的 freeze-frame 不是同一个操作。

## 六、字段和时间边界

**无配乐不等于无后期声音：** 原文明确取消 non-diegetic music，却保留三次定格的喜剧 post-SFX。现场音、后期音效和配乐是不同类别。

**约 15 秒与 15.3 秒：** 提示词最后时间标到 00:15.3，因此只能称约 15 秒，不能把标题自动当作严格 15.000 秒规格。

**RMS：** root mean square，均方根。README 用它帮助定位声音能量变化，不是靠它单独证明音乐 BPM 或剧情原因。

**T2VA / UGC / SFX：** 在本项目分别指文本生成视频及音频、用户生成内容、声音效果。属于缩写解释；其具体模型模式与接口参数还须查实际实现。

## 校读边界

本增补讨论文字和视频编辑层次，不把案例作者的反推结果称为唯一可能的真实拍摄过程。动作描写是源视频喜剧叙事的语言解读，不建议现实中模仿干扰饮水或头颈的行为。
