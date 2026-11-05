# 案例研究 004 — 分层参考架构与文本驱动高潮｜逐段翻译

> 对应原始 `README.md`。按段落顺序处理：每段先列关键词、术语和概念（IPA、词性缩写、简体中文释义），再给出整段简体中文译文。

## Inputs｜输入

### 段落 1
**原文：** `<Picture 1>` — Character key visual / first frame (identity, face, hair, costume)

**关键词与术语：**
- key visual /kiː ˈvɪʒuəl/ n.：主视觉
- first frame /fɜːrst freɪm/ n. phr.：首帧
- identity /aɪˈdentəti/ n.：人物身份

**整段翻译：**  
`<Picture 1>` = 角色主视觉 / 首帧，负责人物身份、脸、头发和服装。

### 段落 2
**原文：** `<Picture 2>` — Character turnaround + windsurfing equipment reference (board, sail, mast, boom)

**关键词与术语：**
- turnaround /ˈtɜːrnəraʊnd/ n.：角色转面参考图 / 多视角设定图
- windsurfing /ˈwɪndsɜːrfɪŋ/ n.：帆板运动
- board /bɔːrd/ n.：帆板板体
- sail /seɪl/ n.：帆
- mast /mæst/ n.：桅杆
- boom /buːm/ n.：帆板横杆 / 帆叉

**整段翻译：**  
`<Picture 2>` = 角色多视角设定 + 帆板器材参考，包括板体、帆、桅杆和横杆。

### 段落 3
**原文：** `<Picture 3>` — Segment-specific cinematography guide (used in segments 1 & 2 only)

**关键词与术语：**
- segment-specific /ˈseɡmənt spəˈsɪfɪk/ adj.：针对特定分段的
- cinematography guide /ˌsɪnəməˈtɑːɡrəfi ɡaɪd/ n. phr.：摄影指导参考

**整段翻译：**  
`<Picture 3>` = 针对特定分段的摄影指导图，只用于第 1、2 段。

### 段落 4
**原文：** Target: **3 × 15-second segments** → 45-second vertical 9:16 fashion-sports music video

**关键词与术语：**
- fashion-sports /ˈfæʃən spɔːrts/ adj. phr.：时尚与运动融合的
- vertical /ˈvɜːrtɪkəl/ adj.：竖屏的

**整段翻译：**  
目标：**3 段 × 15 秒**，最终拼成 45 秒、9:16 竖屏的时尚运动音乐视频。

### 段落 5
**原文：** Post-production: full video audio → Suno remix → final music-video sync

**关键词与术语：**
- post-production /ˌpoʊst prəˈdʌkʃən/ n.：后期制作
- remix /ˌriːˈmɪks/ n./v.：重新编曲 / 混音
- sync /sɪŋk/ n.：同步

**整段翻译：**  
后期流程：完整视频音频 → Suno 重制 / Remix → 最终音乐视频重新同步。

### 段落 6
**原文：** Prompt language: **Chinese** (design doc) + **English** (H3 prompts)

**关键词与术语：**
- design doc /dɪˈzaɪn dɑːk/ n. phr.：设计文档
- H3 prompt /ˌeɪtʃ θriː prɑːmpt/ n. phr.：H3 生成提示词

**整段翻译：**  
提示词语言：**中文**设计文档 + **英文** H3 提示词。

## The problem｜问题

### 段落 7
**原文：** H3 treats all reference images as equal-weight visual targets.

**关键词与术语：**
- equal-weight /ˌiːkwəl ˈweɪt/ adj.：等权重的
- visual target /ˈvɪʒuəl ˈtɑːrɡɪt/ n. phr.：视觉匹配目标

**整段翻译：**  
H3 很容易把所有参考图都当成等权重的视觉目标。

### 段落 8
**原文：** Give it three pictures and it tries to reproduce all three simultaneously — the character, the equipment sheet, and the camera angle all become "things to match." The result is a compromised compromise: the character looks like a turnaround model, the camera framing fights the text instructions, and the equipment renders as a flat illustration rather than a 3D prop in motion.

**关键词与术语：**
- reproduce /ˌriːprəˈduːs/ v.：复现
- simultaneously /ˌsaɪməlˈteɪniəsli/ adv.：同时地
- equipment sheet /ɪˈkwɪpmənt ʃiːt/ n. phr.：器材设定图
- compromised compromise /ˈkɑːmprəmaɪzd ˈkɑːmprəmaɪs/ n. phr.：层层妥协后的折中结果
- framing /ˈfreɪmɪŋ/ n.：取景 / 构图
- flat illustration /flæt ˌɪləˈstreɪʃən/ n. phr.：平面插画
- prop /prɑːp/ n.：道具

**整段翻译：**  
如果同时给模型三张图，它会试图三张一起复现——角色、器材设定图、摄影机角度都被当作必须匹配的对象。结果会变成一种层层妥协后的折中：人物看起来像多视角角色设定模特，摄影构图与文字指令相互冲突，器材则容易被渲染成平面插画，而不是处在运动中的三维真实道具。

### 段落 9
**原文：** Worse, when the project needs a **cinematic climax** — a windsurfing aerial jump at the musical peak — a cinematography reference image becomes a cage. The model tries to match the guide image's composition instead of executing the dynamic hero-shot timing the text describes.

**关键词与术语：**
- cinematic climax /ˌsɪnəˈmætɪk ˈklaɪmæks/ n. phr.：电影化高潮
- aerial jump /ˈeriəl dʒʌmp/ n. phr.：腾空跳跃
- musical peak /ˈmjuːzɪkəl piːk/ n. phr.：音乐高潮
- cage /keɪdʒ/ n.：牢笼；比喻过度限制
- hero shot /ˈhɪəroʊ ʃɑːt/ n.：英雄式主视觉镜头
- execute /ˈeksɪkjuːt/ v.：执行

**整段翻译：**  
更糟的是，当项目需要一个**电影化高潮**——例如在音乐顶点完成帆板腾空跳跃——摄影参考图反而会变成“牢笼”。模型会优先匹配指导图构图，而不是按照文本所描述的动态 Hero Shot 时序执行动作。

## The breakthrough｜关键突破

### 段落 10
**原文：** Give each picture a **job title**, and when the job is done, **fire the picture**.

**关键词与术语：**
- job title /dʒɑːb ˈtaɪtl/ n. phr.：职责名称；明确分工
- fire /faɪər/ v.：解雇；此处指在不再需要时移除参考图

**整段翻译：**  
给每张参考图一个明确的**职位 / 职责**；它的工作完成后，就把这张图**解雇**掉。

### Layer 1｜角色分离的参考架构

### 段落 11
**原文：** Instead of three equal-weight references, each picture gets a specific role:

**关键词与术语：**
- role-segregated /roʊl ˈseɡrɪɡeɪtɪd/ adj.：按职责分离的
- specific role /spəˈsɪfɪk roʊl/ n. phr.：明确职责

**整段翻译：**  
不再把三张图当成等权重参考，而是为每张图分配一个明确职责：

| 图片 | 职责 | 控制内容 | 不控制内容 |
|---|---|---|---|
| **Picture 1** | 首帧视觉锚点 | 身份、脸、头发、服装、色彩、开场帧状态 | 摄影机、构图、器材结构 |
| **Picture 2** | 角色 + 器材参考 | 身体结构、服装结构、鞋、帆板、帆、桅杆、横杆、索具 | 分镜、摄影机、运动 |
| **Picture 3** | 摄影参考 | 机位、取景、镜头语言、运动方向、主体尺度、构图 | 人物外观、器材 |

### 段落 12
**原文：** The prompt explicitly tells H3: *"Picture 2 is not a storyboard. Do not reproduce the turnaround-sheet layout."* This prevents the model from flattening a 3D scene into a 2D character sheet.

**关键词与术语：**
- storyboard /ˈstɔːribɔːrd/ n.：分镜
- turnaround-sheet layout /ˈtɜːrnəraʊnd ʃiːt ˈleɪaʊt/ n. phr.：角色转面设定图版式
- flatten /ˈflætn/ v.：平面化

**整段翻译：**  
提示词明确告诉 H3：“Picture 2 不是分镜。不要复现角色转面设定图的版式。”这可以阻止模型把本应是三维运动空间的场景压扁成二维角色设定图。

### Layer 2｜文本驱动高潮

### 段落 13
**原文：** The third segment — the hero moment where the windsurfer launches off a giant wave — uses **only Picture 1 + Picture 2**. No Picture 3.

**关键词与术语：**
- launch off /lɔːntʃ ɔːf/ v. phr.：借势腾空
- giant wave /ˈdʒaɪənt weɪv/ n. phr.：巨浪

**整段翻译：**  
第三段，也就是帆板选手从巨浪上腾空的 Hero Moment，只使用 **Picture 1 + Picture 2**，不使用 Picture 3。

### 段落 14
**原文：** This is not because of cross-segment visual memory (each 15s clip is independently generated). It's because a cinematography guide image would **over-constrain the camera** during the most complex action sequence:

**关键词与术语：**
- cross-segment visual memory /ˌkrɔːs ˈseɡmənt ˈvɪʒuəl ˈmeməri/ n. phr.：跨分段视觉记忆
- independently generated /ˌɪndɪˈpendəntli ˈdʒenəreɪtɪd/ adj. phr.：独立生成的
- over-constrain /ˌoʊvərkənˈstreɪn/ v.：过度约束

**整段翻译：**  
这样做并不是因为模型拥有跨分段视觉记忆——实际上每个 15 秒片段都是独立生成的——而是因为在最复杂的动作序列中，摄影指导图会**过度约束摄影机**：

```
巨浪 → 沿浪面上行 → 起跳 → 腾空 → Hero Shot → 落地 → 时尚化收尾
```

### 段落 15
**原文：** When the text needs to precisely time camera stops, music peaks, and spray explosions to specific seconds, a guide image fights the text. Removing it lets the text be the sole director.

**关键词与术语：**
- precisely time /prɪˈsaɪsli taɪm/ v. phr.：精确控制时间点
- spray explosion /spreɪ ɪkˈsploʊʒən/ n. phr.：水花爆发
- sole director /soʊl dəˈrektər/ n. phr.：唯一导演 / 唯一控制源

**整段翻译：**  
当文字需要把摄影机停止、音乐高潮和水花爆发精确安排到具体秒数时，指导图会和文本抢控制权。移除 Picture 3 后，文本就成为唯一导演。

### Layer 3｜音乐驱动时间轴

### 段落 16
**原文：** The 15-second timeline is not divided evenly. It's divided by **musical function**:

**关键词与术语：**
- timeline /ˈtaɪmlaɪn/ n.：时间轴
- musical function /ˈmjuːzɪkəl ˈfʌŋkʃən/ n. phr.：音乐功能段落

**整段翻译：**  
15 秒并不是平均切分，而是按**音乐功能**切分：

```
0–3s    Build-up｜铺垫
3s      Main Drop｜主 Drop
3–10s   High-energy｜高能段
6–7s    Mini-turnaround｜小型转面展示
9–10s   Absolute visual peak｜绝对视觉高潮
10–12s  Release｜释放
12–15s  Next phrase｜下一乐句
```

### 段落 17
**原文：** The rule: **music's accent decides the action; music's release decides the camera ease.** The 9–10s hero shot must align with the strongest musical accent — camera stops aggressive movement, stabilizes into a low-angle telephoto hero frame, and holds.

**关键词与术语：**
- accent /ˈæksent/ n.：重音
- release /rɪˈliːs/ n.：释放段
- camera ease /ˈkæmərə iːz/ n. phr.：摄影机缓和 / 减速
- align with /əˈlaɪn wɪð/ v. phr.：与……对齐
- aggressive movement /əˈɡresɪv ˈmuːvmənt/ n. phr.：强烈、快速的镜头运动
- low-angle telephoto /ˌloʊ ˈæŋɡəl ˈteləfoʊtoʊ/ n. phr.：低机位长焦
- stabilize /ˈsteɪbəlaɪz/ v.：稳定下来

**整段翻译：**  
规则是：**音乐重音决定动作发生，音乐释放决定摄影机何时缓下来。** 9–10 秒的 Hero Shot 必须与最强音乐重音对齐：摄影机停止激进移动，稳定到低机位长焦 Hero Frame，并保持。

### Layer 4｜H3 + Suno 分工工作流

### 段落 18
**原文：** The final music is not generated per-segment. Instead:

**关键词与术语：**
- per-segment /pər ˈseɡmənt/ adj.：逐分段的

**整段翻译：**  
最终音乐不按每个 15 秒分段单独生成，而采用以下流程：

```
H3 生成 3 段 → 剪成完整视频 → 提取完整音频 → Suno 重制完整音频 → 回填最终音乐 → 最终同步剪辑
```

### 段落 19
**原文：** This gives Suno the complete musical structure (build-up → drop → development → climax → ending) rather than three disconnected 15-second fragments.

**关键词与术语：**
- development /dɪˈveləpmənt/ n.：发展段
- disconnected /ˌdɪskəˈnektɪd/ adj.：彼此断裂的

**整段翻译：**  
这样 Suno 得到的是完整音乐结构——铺垫 → Drop → 发展 → 高潮 → 结尾——而不是三个互不相连的 15 秒碎片。

### 段落 20｜Technique stack

| 技术 | 中文作用 |
|---|---|
| **Role-Segregated Reference** | 每张参考图只承担一个明确职责，避免等权重妥协 |
| **Text-Driven Climax** | 第三段移除 Picture 3，让文字独占导演权 |
| **Music-Driven Timeline** | 按 BPM / 音乐功能切分；重音决定动作 |
| **H3 + Suno Split** | H3 负责视觉，Suno 负责完整最终音乐 |
| **Hero Shot Timing Lock** | 音乐峰值时摄影机停止并保持标志性画面 |

## The named language｜命名语言

### 段落 21
**原文：** **Layered Reference Architecture with Text-Driven Climax**

**关键词与术语：**
- layered /ˈleɪərd/ adj.：分层的
- reference architecture /ˈrefrəns ˈɑːrkɪtektʃər/ n. phr.：参考图架构
- text-driven /tekst ˈdrɪvn/ adj.：文本驱动的

**整段翻译：**  
**分层参考架构与文本驱动高潮**

### 段落 22
**原文：** "Layered" tells the model: these images are not equal — each has a role. "Text-Driven Climax" tells the model: when the action peaks, text is the only director. Together they solve the two failure modes — reference-image compromise and climax constraint — in one concept.

**关键词与术语：**
- compromise /ˈkɑːmprəmaɪz/ n.：妥协
- climax constraint /ˈklaɪmæks kənˈstreɪnt/ n. phr.：高潮阶段被参考图限制

**整段翻译：**  
“Layered”告诉模型：这些图并不等权，每张都有自己的角色；“Text-Driven Climax”则告诉模型：动作进入高潮后，文字是唯一导演。两者合起来，同时解决“多参考图互相妥协”和“高潮镜头被参考图束缚”这两种失败模式。

## 48-hour takeaway｜48 小时后的关键结论

### 段落 23
**原文：** A reference image is an employee, not a partner. Give it a job title, tell it what it does NOT control, and when its job is done, dismiss it.

**关键词与术语：**
- employee /ɪmˈplɔɪiː/ n.：雇员；比喻受分工约束的参考图
- dismiss /dɪsˈmɪs/ v.：撤下；停止使用

**整段翻译：**  
参考图更像“员工”，而不是平等合作伙伴。要给它明确职位，告诉它哪些事情**不归它控制**；职责完成后，就把它撤下。

### 段落 24
**原文：** The most important experiment in this project was **removing Picture 3 from the final segment**. The instinct is to add more references for more control. But during a climax — when camera, action, music, and spray all need to hit specific marks at specific seconds — a guide image becomes a constraint that fights the text. Less reference input gave more output control.

**关键词与术语：**
- instinct /ˈɪnstɪŋkt/ n.：直觉
- hit specific marks /hɪt spəˈsɪfɪk mɑːrks/ v. phr.：准确命中特定时间 / 动作点
- output control /ˈaʊtpʊt kənˈtroʊl/ n. phr.：对生成结果的控制力

**整段翻译：**  
这个项目最重要的实验，是**在最终分段移除 Picture 3**。直觉上，人们往往认为参考图越多，控制越强；但在高潮阶段，当摄影机、动作、音乐与水花都必须在具体秒数准确命中特定节点时，摄影指导图会变成与文字争夺控制权的约束。减少参考输入，反而带来了更强的输出控制。

### 段落 25
**原文：** And for multi-segment music videos: **generate all video first, then remix the complete audio.** Feeding Suno the full 45-second audio structure produces a coherent musical arc; feeding it three isolated 15-second clips produces three unrelated tracks.

**关键词与术语：**
- coherent /koʊˈhɪrənt/ adj.：连贯的
- musical arc /ˈmjuːzɪkəl ɑːrk/ n. phr.：完整音乐发展弧线
- isolated /ˈaɪsəleɪtɪd/ adj.：彼此孤立的

**整段翻译：**  
对于多分段音乐视频，还应遵循：**先把所有视频生成并拼完整，再处理整条音频。** 把完整 45 秒音频结构交给 Suno，可以得到连贯的音乐发展弧线；如果分别输入三个孤立的 15 秒片段，则更容易得到三首彼此无关的音乐。

## Media files｜媒体文件

### 段落 26
**整段翻译：**
- `picture-1-character-key-visual.png`：Picture 1，角色主视觉 / 首帧锚点
- `picture-2-turnaround-equipment.png`：Picture 2，角色转面 + 帆板器材参考
- `picture-3-segment1-cinematography-guide.png`：Picture 3，第 1 段摄影指导
- `picture-3-segment2-cinematography-guide.png`：Picture 3，第 2 段摄影指导
- `result-video.mp4`：最终生成视频

### 段落 27
**原文：** Note: Segment 3 (the final hero moment) intentionally has **no Picture 3** — camera control is text-only.

**关键词与术语：**
- intentionally /ɪnˈtenʃənəli/ adv.：有意地
- text-only /tekst ˈoʊnli/ adj.：只由文本控制的

**整段翻译：**  
注意：第 3 段，也就是最终 Hero Moment，**有意不使用 Picture 3**；摄影机完全由文本控制。

## The final prompt｜最终提示词

### 段落 28
**原文：** See `prompt.md` for the full production document (~1465 lines, Chinese design doc + three English H3 prompts).

**关键词与术语：**
- production document /prəˈdʌkʃən ˈdɑːkjumənt/ n. phr.：制作文档

**整段翻译：**  
完整制作文档见 `prompt.md`（约 1465 行，中文设计文档 + 三组英文 H3 提示词）；英文主体的逐段翻译见 `prompt.zh-CN.md`。

### 段落 29
**整段翻译：**  
文档依次包括：
1. 项目结构——9:16 竖屏、时尚运动混合类型、视觉能量曲线
2. 多图参考经验——Picture 1/2/3 的职责分离
3. 第 3 段例外——为什么高潮移除 Picture 3
4. 音乐设计——BPM 128、4/4 拍、时间轴功能图
5. 第 1 段提示词——高速帆板入场（Picture 1+2+3）
6. 第 2 段提示词——进入大浪区（Picture 1+2+3）
7. 第 3 段提示词——最终 Hero Moment，摄影机仅由文本控制（Picture 1+2，无 Picture 3）
8. 分段比较表——每段参考图使用情况
9. 为什么第 3 段使用纯文本摄影语言
10. 后期工作流——H3 → 完整视频 → 提取音频 → Suno → 最终同步
11. 音乐视频同步图——视觉节拍与音乐功能如何对应
12. 完整工作流图——端到端制作流程
13. 四条保留经验——参考职责分离、Picture 3 分段使用、音乐作为导演、H3 与 Suno 分工

## Result｜结果

### 段落 30
**原文：** A 45-second vertical fashion-sports music video produced in three independent 15-second H3 segments, with the final climax segment using text-only camera control and the complete soundtrack remixed by Suno from the full video's extracted audio.

**关键词与术语：**
- soundtrack /ˈsaʊndtræk/ n.：完整配乐轨
- extracted audio /ɪkˈstræktɪd ˈɔːdioʊ/ n. phr.：从视频中提取的音频

**整段翻译：**  
最终得到一条 45 秒竖屏时尚运动音乐视频，由三个独立 15 秒 H3 片段组成；最终高潮段采用纯文本摄影机控制，完整配乐则由 Suno 基于全片提取音频重新制作。

### 段落 31
**原文：** The signature frame: Furina cosplayer airborne above a breaking wave, transparent blue sail fully extended, camera frozen at the musical peak in a low-angle telephoto hero composition.

**关键词与术语：**
- signature frame /ˈsɪɡnətʃər freɪm/ n. phr.：标志性画面
- airborne /ˈerbɔːrn/ adj.：腾空的
- breaking wave /ˈbreɪkɪŋ weɪv/ n. phr.：破碎翻卷的浪
- fully extended /ˈfʊli ɪkˈstendɪd/ adj.：完全展开的

**整段翻译：**  
标志性画面是：芙宁娜 coser 腾空在破浪上方，透明蓝色风帆完全展开；音乐到达高潮时，摄影机停止剧烈运动，以低机位长焦 Hero Composition 锁住画面。

## Tags｜标签

**中文对应：**  
`#H3` `#提示词工程` `#多图参考` `#分层参考` `#文本驱动高潮` `#音乐驱动时间轴` `#帆板` `#时尚MV` `#Suno` `#竖屏视频` `#HeroShot`
