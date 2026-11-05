# 人可读权限表

这是文字权限提案，不是已接受状态或媒体观察。内部 ID 不直接充当 H3 官方标签。

|权限 ID|绑定|属性|决策|用途|理由|
|---|---|---|---|---|---|
|FACE-IDENTITY|FACE|identity|allow|reference|只用于面部身份、五官结构与可辨认比例；不称已观察。|
|FACE-POSE|FACE|pose|forbid|reference|排除头角、手位、臂位、朝向、站姿及静态构图。|
|FACE-MOTION|FACE|motion|forbid|reference|面部参考不提供编舞。|
|FACE-FIRST|FACE|first_frame|forbid|anchor|原文明确不是 opening-frame reference。|
|BODY-APPEARANCE|BODY|appearance|allow|reference|身体比例、整体尺度、参考中可见发型。|
|BODY-CLOTHING|BODY|clothing|allow|reference|服装与配饰。|
|BODY-POSE|BODY|pose|forbid|reference|不复制精确站姿，也不以该静态姿势开场。|
|BODY-MOTION|BODY|motion|forbid|reference|全身参考不提供编舞。|
|BODY-FIRST|BODY|first_frame|forbid|anchor|不得从这张图的静态姿态开场；首帧由文字新动作定义。|
|SCENE-ENV|SCENE|scene|allow|reference|环境、建筑、背景。|
|SCENE-LIGHT|SCENE|lighting|allow|reference|文字授权借用光线方向与曝光；实图光照未核验。|
|SCENE-SPACE|SCENE|spatial_layout|allow|reference|空间深度与环境关系用途，未推断具体几何。|
|SCENE-STYLE|SCENE|style|allow|reference|写实摄影质感用途。|

`decisions` 为空。本次未执行 accept。本表工作级范围覆盖六段相同双图用法。
