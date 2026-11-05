# M11 时序交接复核稿

本文件由根代理在阅读独立试用原稿后补充。`m11-handoff.md` 保留原始试用输出，不覆盖其历史。数值和实际命令结果不变；本复核收窄“视觉切换”的镜头含义。

## 1. 可以确定的时间

| 事件 | gen02 局部时间 | 编辑域依据 |
| --- | --- | --- |
| cameraReadyA 到位 | 3/4秒，即0.750秒 | 23/4秒，即5.750秒 |
| contactA 接触 | 17/16秒，即1.0625秒 | 97/16秒，即6.0625秒 |
| 已选视觉切换边界 | 16/15秒，显示为1.067秒 | 零基第182帧；91/15秒 |
| 片段覆盖终点 | 3秒 | 区间端边界，不等同最后一帧PTS |

相机在接触前0.3125个作品秒到位，满足至少0.2秒。切换的精确编辑误差为1/240秒，小于0.005秒。生成FPS未知，不给出生成帧号，也不声称实际H3输出精确执行。

## 2. 视觉变化与真实切镜

原任务只给出“M9的一个已选视觉切换”，没有给出切换类型、目标视角或Shot拓扑。原稿称其为“第二个实际镜头”并写“switch to the view”，收紧了题目未明确的语义。

M7目前交付的是这一个已选变化的时间边界。M11消费时保留M9已选内容；若对应决定明确为真实cut，才使用实际的后续`[Shot N] At 00:01.067`结构。若为同镜头中的换装、状态或内容变化，在现有Shot内描述，不增加镜头数。当前资料不足以选定二者，不能凭数值检查通过就自行决定。

可交给M11的内部英文时间说明为：

> The camera is in position by 0.750 seconds. The established contact occurs at 1.0625 seconds. Place the already selected visual change after the contact, at the precise local time of 16/15 seconds, displayed as approximately 1.067 seconds. Preserve the existing decision about whether this change is a cut or a change within the current shot.

这段是内部编译交接，M11须结合已有的具体动作、画面和模式编译正文；它不是独立完整H3提示词。当前不新增Subject、Picture、Video或Audio标签，不用sourceA等内部时钟ID冒充素材标签。

## 3. 精度保留

权威编辑数据是`frame_index=182`与`91/15`秒；`1.067`只是生成局部显示值。不要从该显示值再计算编辑ceil：6.067×30=182.01，再取ceil会成为第183帧。保留精确有理时间和帧号，另记显示误差；不能把字符串格式化后的数值重新当原始数据。

基础四模式向`integrated_multimodal_description`交接，Ref2VA向`detailed_description`交接；本任务没有给模式，不由M7选模式。实际音画执行和最终媒体仍未验证。
