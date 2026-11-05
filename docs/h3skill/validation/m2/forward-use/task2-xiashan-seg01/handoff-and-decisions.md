# 任务二：SEG01 可完成部分、缺项与实际决定

当前交付候选为 `proposal.revised.json`；`proposal.json` 是保留的初版。二者都不是已接受状态。修订候选在定稿运行包上实际返回 rejected；不把原文矛盾静默改成可生成的单一政策。

## 已完成的文字登记

|对象|可登记内容|不能据此宣称|
|---|---|---|
|图1 / IMG-FRONT|原文指定正面身体、正面服装；C1 的入态明确使用图1站姿|没有看到实图，不能验证“无头部”、体型、服装或站姿；C1 入态不自动成为视频首帧|
|图2 / IMG-THREE-VIEW|原文指定脸、眉眼、发型、背部服装、口鼻半纱面纱；衣装和面纱不随歌词改变|未核验图2内容、同人一致性或安全裤；不能额外命名/补写服装细节|
|场景|星海高台夜景、单人且背景无其他人物是文字目标；保留图1环境权限的相反说明|没有观察环境图片，不把文本场景当成图片证据|
|Audio 1 / AUDIO-SEG01|BPM 134.0、beat 0.4478 s、bar 1.7910 s、首拍 0.441 s、歌词起点 0.766/4.433/8.116 均按源文登记为 audio_timing/reference|这些数值未测音频；节奏参考没有扩张成音频内容或角色音色授权|

README 的图2排除项还包括环境、光线、姿势、构图、相机；后续编译应保持这些边界，不把同一张图的身份权限扩成全部画面属性。详细原始分工和全部源文见快照及 actual-input.md。

## 必须保留并需要权威澄清的要求

|问题|原始要求 A|原始要求 B|实际需要的决定|
|---|---|---|---|
|音频用途|subject_definitions：referenced only for rhythm；No signal copy|summary / retention：complete final audio track、reused 1:1、fully_copy，不重生/改动音乐|确认最终音频政策以及两句原要求的适用范围；本次不能选掉任一条。copy forbid 与 copy allow 已同时保留|
|服装来源|图1只负责正面，图2负责背面与面纱|COLOR 段：The costume comes solely from Picture 1|明确“solely”究竟限于正面还是覆盖全服装；如要缩窄原文，须有权威决定|
|图1环境权限|README 分权表：图1明确不管环境|prompt COLOR & ATMOSPHERE：authorized environment language, from Picture 1|明确是否允许图1提供环境光色，或仅把这些词当独立文字美术要求；两份来源目前相反，ENV-SOURCE-CONFLICT 保持 open|
|SEG01 音频/时间版本|prompt：0.000–11.116 s，段内独立提交 mp3|README 切段表另一套边界从 0–12.860 s 开始；其后总边界也与 141.845 s 描述不一致|提供/指定实际 SEG01 音频、版本、源窗口与采用的切段时间表；交 M7 核对|

这张表列出真实决策点；不会要求用户重新批准已经明确的图1正面、图2脸/背面分工。对已有兼容分工的精细结构表达，可以在后续 M2 工程修订中完成。

## 实际检查的边界

最终修订提案的四个 blocking 结构诊断为：

- FACE-HAIR 与 FRONT-BODY：competing_reference_sources；两者共用粗属性 appearance，实际文字分别指头部/身体。本次没有进一步构造有权威的 combine 决定，保留了待处理诊断。
- BACK-VEIL 与 FRONT-CLOTHES：competing_reference_sources；两者共用 clothing，实际文字分别指背面/正面。该诊断本身不是新发现的用户矛盾。
- COLOR-EXCLUSIVE 与 BACK-VEIL：permission_conflict；反映“全服装只来自图1”与图2背面/面纱权威的字面冲突。
- AUDIO-EXACT-COPY 与 AUDIO-NO-COPY：permission_conflict；同一 audio_content/copy 的真实相反要求。

环境来源冲突由人工阅读保留为 open issue；脚本未自动证明其自然语言语义。proposal 在请求配对检查前已被权限检查拒绝，因此本次 `--request` 虽已传入，结果仍为 request_match_checked=false；不要宣称该修订提案已通过 request 配对验证。

## H3 交接

Ref2VA 是候选路线，不将“0.00 seconds fully referenced”自动改成 I2VA 首帧。`FRONT-ANCHOR` 仍为 unknown。真实文件、上传顺序和官方 `<Subject n>`/`<Picture n>`/`<Audio n>` 由 M11 确认，M2 内部 ID 不替代它们。

原案同时写了 subject_definitions、summary、retention_analysis 与 integrated_multimodal_description。按本地固定官方映射，Ref2VA 应使用 **subject_definitions / summary / retention_analysis / detailed_description / overall_soundscape / non_diegetic_music**。本次仅建议 M11 把连续动作正文迁移到 detailed_description；没有改写案例。不能把“字段迁移建议”记成已经完成编译。

音频交 M6，源窗口/节拍网格交 M7，SEG01 所称“承接上一段”但缺失的前态交 M9。最终是否 fully_copy 必须等音频政策与实际输出声音范围明确：若用户另行决定保留原音乐又新增声音，需要重核相应复制语义；本次没有做混音或选择新方案。

## 实际缺项

两张图、SEG01 音频文件、媒体版本/哈希、选择区域、真实时长/源窗口、可核验的前段终态、后端能力与上传编号均未提供。旧 Windows 路径只是案例文字；没有尝试访问或假装挂载。没有视频输出可评，案例历史验证与生成结果不作为本次验证成绩。
