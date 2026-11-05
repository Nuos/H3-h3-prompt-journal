# 修订后人可读权限表

这是当前交付候选。初版 `proposal.json` 和 `permissions.md` 保留供追溯；修订不删除原始需求矛盾。所有权限范围仅 SEG01。

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
|AUDIO-NO-COPY|MUSIC|audio_content|forbid|copy|保留明确的 No signal copy。|
|AUDIO-EXACT-COPY|MUSIC|audio_content|allow|copy|同时保留 reused 1:1、complete final audio track 与 fully_copy；不得擅自选掉另一要求。|

额外语义阻塞：README 排除图1环境用途，而 prompt 的 COLOR 段从图1继承环境语言；见 `ENV-SOURCE-CONFLICT`。没有选择任何冲突分支；`decisions` 仍为空。
