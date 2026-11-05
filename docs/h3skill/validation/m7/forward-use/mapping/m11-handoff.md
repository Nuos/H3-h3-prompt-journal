# M11 生成局部时序交接

## 权威时序

任务 `gen02` 局部持续 3 秒，从作品 10 秒开始。以下为计划约束，不是媒体测量。

| 事件 | gen02 局部秒数 | 交接含义 |
|---|---:|---|
| 起始镜头 | 0 | 首镜正文直接开始，不添加 `At 00:00.000` |
| cameraReadyA | 0.750 | 相机已到位；不是开始移动 |
| contactA | 1.0625 | 保留 M4 既定接触动作 |
| M9 既定视觉切换 | 16/15 ≈ 1.066666667 | 只保留题目既定的一次切换 |
| 局部覆盖终点 | 3.000 | 区间终点，不代表最后采样点 |

相机到位早于接触 0.3125 秒，满足至少 0.2 个作品秒。生成局部与作品在此段是 1:1，故局部提前量相同。

## 可并入既有正文的英文时序片段

以下措辞保留已有视觉内容和 M4/M5/M9 选择；M11 应把“selected view / established contact action”替换为已有提示词中具体可见的内容。任务未给出这些内容，不能凭空补写人物、环境或音效。

> Keep the selected opening view. The camera is in position by 0.750 seconds. Show the established contact action at approximately 1.0625 seconds, keeping the opening view through the contact.
>
> At 00:01.067, switch to the view already selected by M9 and continue that view for the remainder of the 3-second clip.

这里只有第二个实际镜头边界使用 `At MM:SS.mmm`。不要把相机到位或接触时刻都改写为新的镜头起点；不新增对白或声音。对于基础四种模式，此片段并入 `integrated_multimodal_description`；如既有任务为 Ref2VA，则并入 `detailed_description`。本题没有确定任务模式，交接不自行选定。`sourceA`、`workA`、`gen02`、`editA` 是时间域标识，不把它们冒充上传素材 Labels。

## 精度与后续编辑依据

精确切换目标是编辑域零基第 **182 帧**，即 `91/15 秒`；对应生成局部 `16/15 秒`。以毫秒写成 `At 00:01.067` 时，显示误差为 `1/3000 秒`，显示时间仍在接触之后。显示时间距接触 0.0045 秒，小于 0.005 秒。

M11 字符串只用于表达生成意图。后续编辑继续使用权威数据 `frame_index=182`，不要从 `1.067` 重新计算并向后量化：加编辑起点后是 `6.067 × 30 = 182.01`，再次 ceil 将成为第 183 帧。精确值和显示字符串必须分别保留。

生成端 FPS/PTS 未知，`At 00:01.067` 不能保证实际 H3 输出在某一帧完成切换；本次没有运行 H3，也未测量媒体。实际生成后的到位、接触及切换位置仍需独立媒体检查。当前只确认给定计划下映射和数值误差关系成立。
