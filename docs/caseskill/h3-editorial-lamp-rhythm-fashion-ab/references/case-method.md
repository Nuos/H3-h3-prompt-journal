# 台灯五章音乐时尚片与受控A/B变体：方法与修复

## 导航

1. 方法来源与适用范围
2. 条件分支与冲突处理
3. 失败表现与修复
4. 迁移示例
5. 规则证据

## 方法来源与适用范围

把音乐、灯态、动作和摄影统一到可复算的计划时间轴，同时把A/B真正固定的条件与改变的变量分开；依据实际正文而非误标文件名路由，保留资产、身体和材料连续性。

本方法由原案例文本、逐案评估和 H3 官方协议共同整理。原案经验、评估发现与本次补齐的数据/检查接口须分别表述；案例作者的成功报告不等于本次实测。原稿快照保留原貌，冲突由本文件及技能入口裁决。

- 六个案例文本和review均全文阅读；图片、配乐、视频不在本案目录，未运行H3，不能证实README所谓已验证效果与同步成功率。
- 来源原始命名错误保留以便追溯，技能入口以语义variant_id修复；本任务不修改原始case-studies文本。
- faithful_variant与controlled_ab、统一roll预算、时轴状态标签、帧误差表、缺资产检查均是工程补齐，不伪称案例或官方既有规则。
- 可爱文件全局Moment05仍写directional foot sweep，而实际Moment05明确不是leg sweep；以具体动作链裁决为toe point。
- 相机完全相同的A/B需要主动统一02/04/06/09差异；即使时间边界一致也不自动构成严格对照实验。
- 源模板成年、既有裙装内层、台灯、十Moment、124 BPM和局部机位禁项只适用于对应变体；迁移到宽袖等新对象时重新做功能和材料检查。
- 原文把曝光列为精确保留又规定灯开关，以保持资产／色调并允许灯态引发的自然照度差异化解；不能靠自动新增灯掩盖矛盾。
- 末段甩裙的release可能指冲量结束而非手脱离布料；如需持续开裙轮廓，须明确握持状态并容许真实回落，不能同时要求完全松手、最大张开不变和自然惯性。

## 条件分支与冲突处理

| 条件 | 执行动作 | 案例/评估依据 |
|---|---|---|
| 用户点名p83暗奢版但要求双手甩裙 | 按需求输出dark_skirt_throw，并明确源正文实际来自p84-cute-backfolded-jump.txt；同时附文件名错位说明，不把可爱跳跃发给用户。 | case-studies/2026-09-editorial-lamp-rhythm-fashion-ab/vocabulary-expanded.zh-CN.md:5-12 |
| 要求两版相机完全相同以比较音乐和Hero | 建立controlled_ab统一摄影表，例如只在01/03/05/07滚转；移除暗奢额外roll及可爱04含混修正，并记录为工程改编。逐镜diff通过后才称摄影受控。 | docs/casereview/2026-09-editorial-lamp-rhythm-fashion-ab.md:29,35,40 |
| 用户要求124 BPM灯点到毫秒精确，而且生成24FPS | 给理想秒值与最近目标帧并列；3.870968秒映射93帧即3.875秒，明确量化误差。实际生成音乐仍需onset回读，不以计划公式保证帧精确。 | docs/casereview/2026-09-editorial-lamp-rhythm-fashion-ab.md:31,41；工程补齐 |
| 参考图中台灯是唯一光源，但要求关灯后人物和房间仍全部清晰 | 标出照明证据冲突；按图中可证实残余照明降低可见度，或提出获准修改参考／照明设计的变体，不偷偷新增灯。 | case-studies/2026-09-editorial-lamp-rhythm-fashion-ab/p84-cute-backfolded-jump.txt:476-480,1025-1031；工程补齐：可见度检查 |
| 可爱版提示里同时出现foot sweep和toe point | 以Moment05完整身体链为准使用侧步点地，将全局roll触发词修成toe-point accent；不额外插入甩腿。 | case-studies/2026-09-editorial-lamp-rhythm-fashion-ab/p83-dark-luxury-skirt-throw.txt:273-274,570-617 |
| 用户想在空中保持姿态一秒，同时禁止慢动作、冻结和超常物理 | 将空中峰值缩为自然可读瞬间，完整给出下降落地；若坚持长保持，明确转为特殊时间处理变体，不能维持原物理承诺。 | case-studies/2026-09-editorial-lamp-rhythm-fashion-ab/p83-dark-luxury-skirt-throw.txt:988-1024；case-studies/2026-09-editorial-lamp-rhythm-fashion-ab/vocabulary-expanded.zh-CN.md:137-141,158 |

## 失败表现与修复

| 失败表现 | 修复步骤 | 依据 |
|---|---|---|
| 选择暗奢甩裙却生成可爱跳跃 | 忽略误导文件名，检查Key、Moment09与10三处；以语义variant_id路由并显示真实源路径。 | case-studies/2026-09-editorial-lamp-rhythm-fashion-ab/vocabulary-expanded.zh-CN.md:5-12；docs/casereview/2026-09-editorial-lamp-rhythm-fashion-ab.md:39 |
| 声称只换音乐和结尾，但中段机位频繁多出倾斜 | 审查02/04/06/09真实正文差异，把roll和Dutch逐项加入变体表；若要受控比较则显式统一并记录删改。 | docs/casereview/2026-09-editorial-lamp-rhythm-fashion-ab.md:29,40 |
| 五次开关、随机闪灯或OFF变成全黑后换房间 | 区分初态与四次切换，填满五区间灯态；保留同一房间残余照明；删除未登记实体灯闪与编辑strobe。 | case-studies/2026-09-editorial-lamp-rhythm-fashion-ab/README.md:52-64；case-studies/2026-09-editorial-lamp-rhythm-fashion-ab/p84-cute-backfolded-jump.txt:476-480,1005-1031 |
| 音乐宣称124 BPM，所有动作边界被当成整拍而拖拍 | 先计算拍位，给1.3、2.6、12.25等自由过渡标签；将灯点与核心重音量测，别按README概括推断全部事件同属网格。 | docs/casereview/2026-09-editorial-lamp-rhythm-fashion-ab.md:31,41 |
| 跳跃版抓裙，或前面小弹已离地，最终Hero失去区别 | 选择单一Hero链；可爱06脚不离地、07紧凑提膝、09手后摆不碰裙、10双脚后折并拢再落地；暗奢则抓握蓄力后甩裙。 | case-studies/2026-09-editorial-lamp-rhythm-fashion-ab/p83-dark-luxury-skirt-throw.txt:636-654,687-713,791-947；case-studies/2026-09-editorial-lamp-rhythm-fashion-ab/p84-cute-backfolded-jump.txt:743-865 |
| bullet-time成为整人悬浮或衣料机械冻结 | 写正常速度的短峰值及下降／制动，主体停止后材料仍衰减；Moment08只保留微动，最终相机才硬锁。 | case-studies/2026-09-editorial-lamp-rhythm-fashion-ab/p83-dark-luxury-skirt-throw.txt:744-787,988-1024；case-studies/2026-09-editorial-lamp-rhythm-fashion-ab/p84-cute-backfolded-jump.txt:923-993 |

## 迁移示例

**任务**

同一张成人室内全身参考图含台灯，制作12秒、24FPS的明亮和暗奢两版；音乐新建120 BPM/4拍，五章灯态为ON/OFF/ON/OFF/ON，灯在第1、2、3、4小节起点切换；为公平比较固定所有相机和时间，只在配器及最后双手高举小跳与手抛既有宽袖中分叉。服装不使用裙装。

**预期处理示例**

这属于灯态机制迁移，Hero改为新服装动作，不套用源安全裤或甩裙约束。shared：120 BPM使每拍0.5秒、每小节2秒，成片24拍=12秒；初态ON，[0,2)ON、[2,4)OFF、[4,6)ON、[6,8)OFF、[8,12)ON，四次切换目标帧48/96/144/192；全部为配乐创作计划，音轨尚未量测。十段身体窗示范为0–1、1–2、2–3、3–4、4–5、5–6、6–7、7–7.5、7.5–8、8–12秒，前八段与摄影共享，roll只在01/03/05/07且回正。第09段7.5–8秒各自进入跳跃屈膝摆臂或抓握既有宽袖的蓄力；8秒灯ON与音乐目标重音同时释放，第10段给足起跳／落地或手冲量／袖边滞后。两版约9秒进入同一全身锁机位置，到12秒只剩衣料衰减；不使用字面慢动作。明亮与暗奢只改配器／指定Hero，其余逐镜diff；袖宽、可抓位置和跳跃空间必须由图与设定支持，缺证标unknown。实际生成后再记录音乐onset、灯帧与动作峰值误差。

示例是编排示范；其中任务给定参数和演算不代表当前已经读取了对应媒体，也不代表一次 H3 推理已完成。完整生成端交付仍需按输出模板选择正确字段和真实素材绑定。

## 规则证据

以下行号对应本技能来源索引中的固定快照；`review` 指 `source-review.md`。工程补齐项以其所解决的原文/评估缺口为依据，不伪称上游已实现该检查。

| 规则 | 原文或评估位置 |
|---|---|
| R1 | case-studies/2026-09-editorial-lamp-rhythm-fashion-ab/vocabulary-expanded.zh-CN.md:5-12；docs/casereview/2026-09-editorial-lamp-rhythm-fashion-ab.md:27,39 |
| R2 | case-studies/2026-09-editorial-lamp-rhythm-fashion-ab/README.md:52-64；case-studies/2026-09-editorial-lamp-rhythm-fashion-ab/p84-cute-backfolded-jump.txt:155-173,476-480 |
| R3 | docs/casereview/2026-09-editorial-lamp-rhythm-fashion-ab.md:25,31,41；工程补齐：精确拍格与帧量化表 |
| R4 | docs/casereview/2026-09-editorial-lamp-rhythm-fashion-ab.md:29,35,40；case-studies/2026-09-editorial-lamp-rhythm-fashion-ab/p83-dark-luxury-skirt-throw.txt:435,556,670,844；case-studies/2026-09-editorial-lamp-rhythm-fashion-ab/p84-cute-backfolded-jump.txt:381,521,627,784 |
| R5 | case-studies/2026-09-editorial-lamp-rhythm-fashion-ab/p83-dark-luxury-skirt-throw.txt:298-338,573-607,636-654,687-713,794-830 |
| R6 | case-studies/2026-09-editorial-lamp-rhythm-fashion-ab/p83-dark-luxury-skirt-throw.txt:866-947,988-1024；case-studies/2026-09-editorial-lamp-rhythm-fashion-ab/p84-cute-backfolded-jump.txt:743-865,949-967 |
| R7 | case-studies/2026-09-editorial-lamp-rhythm-fashion-ab/p83-dark-luxury-skirt-throw.txt:223-292,744-787；case-studies/2026-09-editorial-lamp-rhythm-fashion-ab/p84-cute-backfolded-jump.txt:179-257,973-993 |
| R8 | case-studies/2026-09-editorial-lamp-rhythm-fashion-ab/p83-dark-luxury-skirt-throw.txt:988-1024；case-studies/2026-09-editorial-lamp-rhythm-fashion-ab/p84-cute-backfolded-jump.txt:923-959；docs/casereview/2026-09-editorial-lamp-rhythm-fashion-ab.md:31 |
| R9 | case-studies/2026-09-editorial-lamp-rhythm-fashion-ab/p83-dark-luxury-skirt-throw.txt:7-55；case-studies/2026-09-editorial-lamp-rhythm-fashion-ab/p84-cute-backfolded-jump.txt:5-53,1005-1031；工程补齐：未知资产状态与灯光例外 |
| R10 | case-studies/2026-09-editorial-lamp-rhythm-fashion-ab/p83-dark-luxury-skirt-throw.txt:1210-1244；case-studies/2026-09-editorial-lamp-rhythm-fashion-ab/p84-cute-backfolded-jump.txt:1041-1057,1141-1168；工程补齐：编辑闪光与实体灯态冲突裁决 |

| 规则 | 文件与行号 | 支持内容 |
|---|---|---|
| R1 | case-studies/2026-09-editorial-lamp-rhythm-fashion-ab/vocabulary-expanded.zh-CN.md：5-12 | 正文与文件名反转的明确对照，是本技能路由依据。 |
| R2 | docs/casereview/2026-09-editorial-lamp-rhythm-fashion-ab.md：25 | 31拍15秒及五状态包含初始ON，只有四次切换。 |
| R3 | docs/casereview/2026-09-editorial-lamp-rhythm-fashion-ab.md：31;41 | 生成音乐精度是计划值、Moment自由边界与量测缺口。 |
| R4 | case-studies/2026-09-editorial-lamp-rhythm-fashion-ab/p84-cute-backfolded-jump.txt：381-383;521-523;627-629;784-786 | 暗奢额外Dutch／roll真实位置，否定README同一roll分布。 |
| R4 | case-studies/2026-09-editorial-lamp-rhythm-fashion-ab/p83-dark-luxury-skirt-throw.txt：435;556-558;670;844 | 可爱相应段禁roll与04含混correction，为受控版本的显式裁决对象。 |
| R5 | case-studies/2026-09-editorial-lamp-rhythm-fashion-ab/p83-dark-luxury-skirt-throw.txt：298-338;636-654;687-713 | 动作阶段、去重复、轻弹与提膝边界。 |
| R6 | case-studies/2026-09-editorial-lamp-rhythm-fashion-ab/p83-dark-luxury-skirt-throw.txt：791-947;1008-1024 | 后摆臂蓄力、手不触裙、后折双脚及下降落地。 |
| R6 | case-studies/2026-09-editorial-lamp-rhythm-fashion-ab/p84-cute-backfolded-jump.txt：743-865;949-967 | 抓握／蓄力／手冲量／布料滞后及相机锁点。 |
| R7 | case-studies/2026-09-editorial-lamp-rhythm-fashion-ab/p84-cute-backfolded-jump.txt：179-257;695-739;973-993 | 离散机位、roll光轴定义、近静止与末段硬锁差别。 |
| R8 | case-studies/2026-09-editorial-lamp-rhythm-fashion-ab/p83-dark-luxury-skirt-throw.txt：988-1024 | bullet-time与禁止字面慢动作／不自然冻结并存，转为可观察峰值。 |
| R9 | case-studies/2026-09-editorial-lamp-rhythm-fashion-ab/p83-dark-luxury-skirt-throw.txt：7-55 | 单图资产锁及内层要求；未知资产、初帧和灯态例外为工程补齐。 |
| R10 | case-studies/2026-09-editorial-lamp-rhythm-fashion-ab/p84-cute-backfolded-jump.txt：1041-1057;1159-1168 | 可选编辑strobe与四个click并存，工程选择需防止混入实体灯闪。 |
