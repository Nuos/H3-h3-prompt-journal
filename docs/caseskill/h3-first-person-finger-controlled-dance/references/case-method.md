# 第一人称手势命令与舞者身体同拍响应：方法与修复

## 导航

1. 方法来源与适用范围
2. 条件分支与冲突处理
3. 失败表现与修复
4. 迁移示例
5. 规则证据

## 方法来源与适用范围

把前景手与舞者之间的控制关系写成可检查的命令—身体事件表，同时修复原案十条命令与结尾三条的歧义、镜头几何冲突和“立即响应”缺少容差的问题。

本方法由原案例文本、逐案评估和 H3 官方协议共同整理。原案经验、评估发现与本次补齐的数据/检查接口须分别表述；案例作者的成功报告不等于本次实测。原稿快照保留原貌，冲突由本文件及技能入口裁决。

- 原案的单手、单舞者、10–18%面积和1.0–1.2米都是本构图设想，不是官方人数、视场或距离上限。
- 原文把声学特征归于Picture 1，技能改为文本设计的场景声；图片不能提供原音证据。
- 完整阅读5个文本和对应review，未读取演示视频；作者声称同步成功并未被本次独立核验。
- 生成切片遵循共同官方资料4–15秒、24FPS；例子的帧差容差是提议验收标准。

## 条件分支与冲突处理

| 条件 | 执行动作 | 案例/评估依据 |
|---|---|---|
| 正文十条命令末尾又要求三连 | 若用户明确追加，输出十三条；明确替换，输出十条并重写末三条；未明确时标记missing，给两个具体候选并暂不声称总数已经确定。 | case-studies/2026-08-first-person-finger-controlled-dance/vocabulary-expanded.zh-CN.md:101 |
| 音轨未提供，但用户想先预演 | 提出清楚标注的BPM与起拍方案，建立暂定时间表；验收标注待真实音轨音头替换。 | docs/casereview/2026-08-first-person-finger-controlled-dance.md:30,37,45 |
| 参考图是平视半身，用户仍要求原图视角和强俯视全身 | 指出几何/参考权限冲突；提出以人物身份为参考重新设计俯视构图，或保持原视角改成可见身体范围的控制演示。 | docs/casereview/2026-08-first-person-finger-controlled-dance.md:44 |
| 用户只想更复杂好看的舞蹈 | 在四向动作内部改变舞种表现；若主动取消手势控制关系，转用普通舞蹈编排，不继续套本技能。 | case-studies/2026-08-first-person-finger-controlled-dance/prompt.md:47–56 |

## 失败表现与修复

| 失败表现 | 修复步骤 | 依据 |
|---|---|---|
| 舞者先动或落后整拍 | 给每个命令配开始时刻和允许帧差，减少装饰动作，记录手势和身体实际首动帧差。 | case-studies/2026-08-first-person-finger-controlled-dance/prompt.md:45；docs/casereview/2026-08-first-person-finger-controlled-dance.md:45 |
| 左右只有小摆髋或反向移动 | 重申screen-left/screen-right及重心、躯干、髋部同向的可见位移；区分屏幕方向与舞者自身左右。 | case-studies/2026-08-first-person-finger-controlled-dance/prompt.md:39–43 |
| 巨手遮脸、手消失或断开 | 明确前臂到食指连续连接，限制局部活动区域及面积，保持舞者主次关系；审查调整后是否仍能看清命令。 | case-studies/2026-08-first-person-finger-controlled-dance/prompt.md:22,58–60 |
| 最后三条重复执行，总时长溢出 | 移除独立且未归并的结尾指令，只保留已经编号的追加或替换总序列。 | case-studies/2026-08-first-person-finger-controlled-dance/vocabulary-expanded.zh-CN.md:101 |
| 强俯拍却为天花板而切掉脚部 | 按参考图核对可见范围，报告冲突并调整天花板、机位或距离约束；不能简单宣称全部同时成立。 | docs/casereview/2026-08-first-person-finger-controlled-dance.md:44 |

## 迁移示例

**任务**

用成年街舞教练的全身高位手机照片做8秒手势控舞，120BPM示意音乐，保持10条命令，最后三条替换成左、右、上，结尾定住。

**预期处理示例**

最终十条是UP、DOWN、LEFT、RIGHT、LEFT、RIGHT、UP、LEFT、RIGHT、UP，LEFT/RIGHT均指画面方向。0–1秒建立右下连续前臂和舞者全身；命令分别于1.0、1.5、2.0、2.5、3.0、3.5、4.0、4.5、5.0、5.5秒开始，每条在0.5秒窗口内完成相应升高、屈膝降低或整体侧移。第十条于6.0秒完成UP，6–8秒保持最终姿态。此120BPM为用户指定的示意网格，实际音轨尚未提供，onsets=missing；实际生成后以手势首动到身体首动0–2帧作为本方案提议容差，不能提前，24FPS下2帧约0.083秒，该阈值不是模型性能保证。手面积约10–18%，人物高度约70–80%作为参考构图目标；如照片视场不支持，则优先保留完整身体和不遮挡的手，调整构图目标，不强加天花板。街舞肩部和腰部装饰只在四向响应中出现，不追加旋转。

示例是编排示范；其中任务给定参数和演算不代表当前已经读取了对应媒体，也不代表一次 H3 推理已完成。完整生成端交付仍需按输出模板选择正确字段和真实素材绑定。

## 规则证据

以下行号对应本技能来源索引中的固定快照；`review` 指 `source-review.md`。工程补齐项以其所解决的原文/评估缺口为依据，不伪称上游已实现该检查。

| 规则 | 原文或评估位置 |
|---|---|
| F1 | case-studies/2026-08-first-person-finger-controlled-dance/prompt.md:26–45 |
| F2 | case-studies/2026-08-first-person-finger-controlled-dance/prompt.md:35–43 |
| F3 | case-studies/2026-08-first-person-finger-controlled-dance/prompt.md:39–43 |
| F4 | case-studies/2026-08-first-person-finger-controlled-dance/vocabulary-expanded.zh-CN.md:101 |
| F5 | docs/casereview/2026-08-first-person-finger-controlled-dance.md:30,37–45 |
| F6 | case-studies/2026-08-first-person-finger-controlled-dance/prompt.md:22–24,58–60 |
| F7 | case-studies/2026-08-first-person-finger-controlled-dance/vocabulary-expanded.zh-CN.md:99 |
| F8 | case-studies/2026-08-first-person-finger-controlled-dance/prompt.md:9–11,47–56；docs/casereview/2026-08-first-person-finger-controlled-dance.md:32 |

| 规则 | 文件与行号 | 支持内容 |
|---|---|---|
| F1 | case-studies/2026-08-first-person-finger-controlled-dance/prompt.md：26–45 | 正文定义前景食指控制身体和四向关系。 |
| F2 | case-studies/2026-08-first-person-finger-controlled-dance/prompt.md：35–41 | 上下由重心与屈膝变化，左右明确screen-left/right。 |
| F3 | case-studies/2026-08-first-person-finger-controlled-dance/prompt.md：39–43 | 排除细小髋抽动，要求可见的整体同向变化。 |
| F4 | case-studies/2026-08-first-person-finger-controlled-dance/vocabulary-expanded.zh-CN.md：101 | 原案十条和结尾三条语义未统一，不能默认为一类。 |
| F5 | docs/casereview/2026-08-first-person-finger-controlled-dance.md：30,37–45 | 评估指出缺BPM、命令时刻与容差，建议用实际帧差验收。 |
| F6 | case-studies/2026-08-first-person-finger-controlled-dance/prompt.md：22–24,58–60 | 连续手部、右下位置、面积、人高、距离及机位控制。 |
| F7 | case-studies/2026-08-first-person-finger-controlled-dance/vocabulary-expanded.zh-CN.md：99 | 俯拍与天花板潜在冲突要依赖真实参考构图检查。 |
| F8 | case-studies/2026-08-first-person-finger-controlled-dance/prompt.md：9–11,47–56 | 舞种替换可行的局部方法以控制关系优先为条件。 |
