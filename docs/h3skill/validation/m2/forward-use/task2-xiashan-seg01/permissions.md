# 人可读权限表

这是文字权限提案，不是已接受状态或媒体观察。内部 ID 不直接充当 H3 官方标签。

|权限 ID|绑定|属性|决策|用途|理由|
|---|---|---|---|---|---|
|FRONT-BODY|FRONT|appearance|allow|reference|正面身体用途；不推断未见的头部。|
|FRONT-CLOTHES|FRONT|clothing|allow|reference|subject_definitions 指定正面服装唯一来自图1。|
|FACE-ID|FACE-BACK|identity|allow|reference|面部身份、眼眉来自图2。|
|FACE-HAIR|FACE-BACK|appearance|allow|reference|图2负责脸与发型，图1无头部信息。|
|BACK-VEIL|FACE-BACK|clothing|allow|reference|图2负责背面服装与半纱面纱；面纱全程遮口鼻、眼眉可见；不新增服装描述。|
|COLOR-EXCLUSIVE|FACE-BACK|clothing|forbid|reference|保留 COLOR 段“costume comes solely from Picture 1”的排他要求；按其字面会排除图2服装权限，与 BACK-VEIL 冲突，未裁决。|
|FRONT-POSE|FRONT|pose|allow|reference|原文 C1 入态明写 Picture 1 standing pose；只保留该链入态，不提升为首帧锚定。|
|FRONT-ANCHOR|FRONT|first_frame|unknown|anchor|0.00 fully referenced 没有明确等同于实图首帧；且开场是袖/衣摆局部特写，待 M11 澄清。|
|ENV-LIGHT|ENV-LOOK|lighting|allow|reference|原文授权的环境调色与光照语言；非媒体观察。|
|ENV-COLOR|ENV-LOOK|color|allow|reference|调色只影响光和环境，不授权变装。|
|AUDIO-TIMING|MUSIC|audio_timing|allow|reference|BPM 134.0、beat 0.4478、bar 1.7910、首拍 0.441 与歌词起点按文字登记，未分析音频。|
|AUDIO-REF-ONLY|MUSIC|audio_content|allow|reference|保留 referenced only for rhythm；只借用节奏语义，不增加音色模仿授权。|
|AUDIO-NO-COPY|MUSIC|audio_content|forbid|copy|保留明确的 No signal copy。|
|AUDIO-EXACT-COPY|MUSIC|audio_content|allow|copy|同时保留 reused 1:1、complete final audio track 与 fully_copy；不得擅自选掉另一要求。|

`decisions` 为空。本次未执行 accept。本表范围仅 SEG01；两组相反服装/音频要求同时保留，尚不能成为可接受权限状态。
