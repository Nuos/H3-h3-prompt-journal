# 任务一：双图权限与 H3 交接

## 完成范围与证据

`request.json` 是可独立路由到 M2.3 的完整请求：资产上下文和实体上下文直接随请求提供，不需要先调用 M2.1/M2.2。`proposal.json` 只提出 reference_map 变更，不修改资产或实体登记。原始与定稿运行包均已实际执行 route、request check 和 `check proposal --request request`；提案 deterministic pass，request_match_checked=true。语义、媒体、总评仍 unverified。

|案例素材|文字授权的继承|明确排除|后续责任|
|---|---|---|---|
|Picture 1 / IMG-FACE|面部身份、五官结构、可辨认比例|头角、身体/手臂/手位、站姿、静态构图、编舞、首帧锚定|补图后核验身份和选择区域；M5 按文字落实半身机位|
|Picture 2 / IMG-BODY-SCENE 的人物部分|身体比例/尺度、服装、配饰、可见发型|精确静态站姿、照图开场、编舞|M4 从文字动作定义开场，M5 负责机位|
|Picture 2 的环境部分|环境/建筑/背景、光向/曝光、空间深度、写实摄影质感|未授权从环境图片推断具体测量值|M3/M5 接收场景与画面要求，待媒体核验|

完整机器记录与逐项表见 `proposal.json`、`permissions.md`。scope=work 表达六段共同双图规则。没有把图1的半身照片直接变成 I2VA 首帧，也没有把两图共同“参考”扩张为复制全部像素属性。

## 模式与标签

候选交接为 **Ref2VA**：双图按属性参考，不是首/尾帧约束。M11 仍须结合目标后端能力确认最终模式。I2VA、FL2VA、L2VA 均需要此任务没有给出的实际帧锚定意图/素材；不得因为存在图片就自动选择。

`IMG-FACE`、`IMG-BODY-SCENE`、`PERFORMER`、`ENVIRONMENT` 是 M2 内部 ID。案例的 `<Picture 1>`/`<Picture 2>` 只保留源文标识，不宣称已完成上传编号。M11 应按角色选择官方 `<Subject n>` / `<Picture n>`：人物身份引用应与表演者实体绑定，环境/风格角色另行表达；同一图的 BODY 与 SCENE 选择不应因此混为人物姿态。

## Ref2VA 字段交接

|官方字段|本案交接内容|
|---|---|
|subject_definitions|唯一表演者、双图所负责属性、独立的环境角色；编号待真实上传分配|
|summary|六段舞蹈共同目标；新动作起步、半身肖像式摄影关系|
|retention_analysis|保留面部/身体/服装/环境的明确属性；排除两图姿态、编舞、静态首帧；不宣称所有内容 fully preserved|
|detailed_description|从源案例交接动作链与镜头文字；半身机位属于 M5，首帧动作属于 M4，不由身份图推断|
|overall_soundscape|交 M6 核对；当前图片权限提案没有实际音频，不产生声音事实|
|non_diegetic_music|源案例逐段要求 Audio 1 1:1 作为最终音轨。该要求记录为待 M6/M7/M11 对接；音频文件、具体源窗口、最终混音均未核验|

依据固定的 `h3-label-mapping.md`：Ref2VA 使用上面六字段；T2VA/I2VA/FL2VA/L2VA 的基础三字段为 integrated_multimodal_description、overall_soundscape、non_diegetic_music。此表是交接，不是已编译 H3 请求或已执行模式选择。

## 未完成与限制

缺两张实图及其来源版本、真实区域与跨图身份核验；段音频也没有提供。当前可以完成文字权限整理与结构校验，不能完成媒体读取、上传、最终 H3 标签分配、模型调用或成片评价。未执行 accept；通过结构检查不等于已接受提案或可立即生成。
