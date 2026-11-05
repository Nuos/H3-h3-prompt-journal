# H3 模式、引用与提示词交付规则

本文是为案例技能编写的离线操作说明。依据 MiniMax-H3 官方提交 `199b7d0e1fd95e7b3eafa8c15eca692534142427`，核对日期为 2026-11-04（America/Los_Angeles）。本文不是官方原文镜像；精确来源列在文末。案例中的演员、人数、服装、时长、焦距、舞种和成功叙述均不能自动成为模型通用约束。

## 1. 先确定真实输入模式

| 模式 | 需要的真实输入与编排责任 |
|---|---|
| T2VA | 从文字建立声画时间线；不要声称绑定了未提供的图像或音轨。 |
| I2VA | 已提供图像作为实际首帧；保留其开场空间、人物和物体状态，再展开动作。 |
| FL2VA | 已提供首尾两帧；写清可观察的连续变化如何抵达尾帧。单镜是默认建议，明确多镜需求才拆镜。 |
| L2VA | 已提供图像作为实际尾帧；构造合理的此前状态，并在实际最后一镜收束。 |
| Ref2VA | 根据各素材的实际职责建立内容、构图、视频结构和音频引用；定妆照不自动等于首帧。 |

正式交付前确认运行时确实支持所选输入。提示词、工作流 JSON 和参考标签都是编排材料，本技能不执行模型推理，也不安装 ComfyUI 节点。[H1–H3]

## 2. 输出字段与镜头语法

基础四模式依次使用：`integrated_multimodal_description`、`overall_soundscape`、`non_diegetic_music`。Ref2VA 依次使用：`subject_definitions`、`summary`、`retention_analysis`、`detailed_description`、`overall_soundscape`、`non_diegetic_music`。不要混用两种主描述字段。[H1–H3]

生成端正文用英文。对白、歌词及画面内文字保留原语言；中文解释与审计结果放在提示词文件之外。Ref2VA 在 `[Shot 1]` 之前用一两句建立总体风格；基础模式从 `[Shot 1]` 开始建立风格与开场。第一镜没有切镜时间；以后用连续编号和 `At MM:SS.mmm,` 标记严格递增的切点。切点必须落在当前生成切片时长内。[H2–H3]

首尾帧模式在字段前使用官方对齐句。可从 `assets/output-template.md` 选择对应模板，将实际尾帧时长格式化为两位小数，最后镜头编号替换为真实编号。首尾帧对齐要求不能通过文字声明代替真实素材传入。[H2]

每镜写清当前构图、可见主体及其位置、环境与光照、动作引发的状态变化、摄影机运动和当下声音。将起点、过程、落点连成完整事件；避免只交付情节摘要、抽象气氛词或引用关系清单。运镜写成可理解的英文动作，区分光学变焦、相机平移与机身转向。[H2–H3]

## 3. Ref2VA 标签与保留关系

| 标签 | 实际职责 | 需要防止的误用 |
|---|---|---|
| `<Subject N>` | 可重复使用的可见内容，例如人物、道具、场景、服装、动作或风格 | 把 Subject 当作文件序号。一个 Subject 可有多个来源，一个文件也可提供多个 Subject。 |
| `<Picture N>` | 首帧、关键帧、尾帧或分镜/构图锚点 | 仅用于定义身份的图片，不必另写一条独立 Picture 定义。 |
| `<Video N>` | 源视频编辑、续接，或镜头/剪辑/时序结构 | 只参考运动和节奏时，不应自动称为直接编辑原视频。 |
| `<Audio N>` | 明确启用的独立音频，或参考视频中明确启用的音轨 | 文件带声音不代表已经启用音频引用；Video 与 Audio 独立编号。 |

标签在六节中保持同义。只作为某个 Subject 来源的 Picture/Video 可以写在其定义内部；若作为独立时间/构图锚点使用，则登记独立职责。`summary` 的任务类型根据实际用途选择 `keyframe completion`、`reference generation`、`video editing`、`video continuation`、`audio reuse`、`audio reference`，多项用 ` + ` 连接。[H3]

可见内容在 `retention_analysis` 使用 `fully_preserved`、`partially_preserved`、`attribute_transfer`、`weak_reference`；音频使用 `fully_copy`、`partially_copy`、`reference`、`weak_reference`。保留关系只评价已定义的参考职责。例如身份图只管身份，目标新增舞步不意味着身份参考被削弱。`fully_copy` 声明完整最终音轨逐一复制，不能同时凭空添加另一套声音。[H3]

## 4. 声音与原文

实际发声源按首次发声顺序分配稳定 `(S1)` 等编号；它与 Subject 编号独立。引用人物实际发声时保留两种编号；仅有 BGM 歌词提示而人物没有发声时，不为舞者捏造 speaker。对白放入 `<d>[Language] …</d>`，动作和声音表现写在标签外。听不清的引用音频标为 `[unclear]`。[H2–H3]

基础模式保持用户对白原文及标点。Ref2VA 直接引用/重演音频时保留原词与原语言，只按官方规则整理基础标点；仅参考音色时不能搬入源对白。场内音乐和同步发声写进主正文，环境与实体动作声音写入 `overall_soundscape`，观众听见而人物听不见的配乐写入 `non_diegetic_music`。环境声的 `N/A` 只用于明确全程静音；没有非场内配乐时配乐字段用 `N/A`。[H2–H3]

旁白使用 `says in an off-screen voiceover`，并在对白块后明确对应镜内人物嘴唇闭合。跨切镜的同一段对白使用 `<scenetrans>` 配合连续声音说明；片尾主动截断使用 `<cutoff>`。可见场景文字使用英文双引号包住。环境声概述通常 1–4 句，非场内配乐通常 1–3 句，不在这两节重复完整歌词或对白。[H2–H3]

## 5. 时长、输入容量与证据边界

官方 README 的标准输出为每次 4–15 秒、24 FPS。长篇案例的原始“段”是创作结构，必要时在段内再拆生成切片，保存全局偏移、末态和后期合成关系。不同运行时只有在记录版本与已核实能力后才能采用其他时长/FPS，不依据“本地部署”推断无限上下文。[H4]

Ref2VA 的标准输入容量按**单次生成**计算：图片最多 9 张；视频最多 3 段，每段 2–15 秒、总长不超过 15 秒；音频最多 3 段，同样每段 2–15 秒、总长不超过 15 秒；混合文件合计最多 12 个。长曲可保留为后期母带，送入某个切片的参考音频需使用相应合法片段。[H4]

Ref2VA 的 350–500 英文词是一般生成任务的写作建议，不是 token 硬上限。对话密集和视频编辑按实际内容安排；正文不能因凑字数丢掉事件或重复规则。不能用格式通过、作者自述或单次样例替代生成稳定性证据。[H3]

本批技能不引入统一人数上限。Hub 专用 3D 动画流程的角色数量、宫格和界面操作规则不属于所有 H3 案例的通用接口约束。用户与具体案例的合理需求在适用范围内决定构图、动作密度和镜头策略。

## 来源

- [H1] MiniMax-AI，H3 Prompt Writing 入口：[固定版本](https://github.com/MiniMax-AI/MiniMax-H3/blob/199b7d0e1fd95e7b3eafa8c15eca692534142427/skills/h3-prompt-writing/SKILL.md)。
- [H2] MiniMax-AI，基础模式指南：[固定版本](https://github.com/MiniMax-AI/MiniMax-H3/blob/199b7d0e1fd95e7b3eafa8c15eca692534142427/skills/h3-prompt-writing/references/base-en.txt)。
- [H3] MiniMax-AI，Ref2VA 指南：[固定版本](https://github.com/MiniMax-AI/MiniMax-H3/blob/199b7d0e1fd95e7b3eafa8c15eca692534142427/skills/h3-prompt-writing/references/ref-en.txt)。
- [H4] MiniMax-AI，模型输入输出说明：[固定版本](https://github.com/MiniMax-AI/MiniMax-H3/blob/199b7d0e1fd95e7b3eafa8c15eca692534142427/README.md)。
- [H5] MiniMax，Community License：[固定版本](https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/42ed227ee7df40d41602854ae760620d6eb651fe/LICENSE)。官方资料保留原许可；本说明不把它们重新许可为 MIT。
