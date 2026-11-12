# 系统 B——运镜纪律库（动态运镜纪律案例库）

- **日期：** 2026-10
- **来源：** 舞蹈动链H3.md E 章 (E1–E10 实测运镜纪律) + 用户 "动作负责舞蹈, 摄影机负责观看" 修订标准
- **提示词：** 见 [prompt.md](./prompt.md) — E 章十条运镜纪律 + 十条物理运镜法则 + 词库 + 组合结构全文

## 问题

两种失败模式一直在破坏 H3 舞蹈影片：

1. **摄影机追逐一切**——每一次胸部脉冲、每一个手指重音都会触发运镜。十秒后画框已跳动六次，观众感到眩晕。原稿把 `PUSH + DROP + RISE + TRACK + WRAP + ROLL PUNCH` 塞进单个片段；摄影机没有主轴，因此结果看起来像不断跳跃。
2. **摄影语言过于抽象**——`dynamic tracking`、`camera orbits 40°`、`sweeping camera move`。H3 无法执行这些抽象说法，就像它无法执行 `low angle` 一样。

## 突破点——动作负责舞蹈，摄影机负责观看

摄影机不会对每个细小的身体重音都作出反应。每个片段具有**一种主要的摄影机行为**；只有高度层或空间关系确实发生重大变化时，才进行次要调整。

**摄影机优先顺序：**
1. 建立物理机位；
2. 让编舞在该画框中发生；
3. 只有舞者改变高度、位移、在空间中转向，或揭示新的身体关系时才移动；
4. 再次稳定下来。

这些要求对应的真实拍摄法则（来自 E 章）是：踢腿时摄影机**定住**，让编舞朝镜头展开；队形位移采用平行**横移**；地板动作与舞者的高度层形成镜像（**人蹲机蹲，人起机起**）；摄影机应在**动作释放拍开始移动，而不是在重音峰值时起步**。

## 十条物理运镜法则

```
POSITION LAW      — placement in real distance/height/side/direction, never abstract terms
NO DEGREE LAW     — no degree measurements; define start and end positions physically
OPTICAL-AXIS LAW  — state what body part the lens aims at during each major move
DISTANCE LAW      — distance changes only through real forward/backward travel
HEIGHT LAW        — height changes only through real rise or descent
SIDE-CHANGE LAW   — crossing sides means physically walking a readable path around her
SUBJECT-TRIGGER   — the camera moves only because a written performer action causes it
DANCE LAW         — continuous connected choreography, never slow walking
POSITION CHANGE   — the dancer relocates with 1-2 purposeful steps; the camera does the reframing
HERO LOCK         — when the camera stops it stays physically stable through the final accent
```

## 十三词词库——每个词都是一条物理路径

| 词语 | 物理定义 |
|---|---|
| PUSH-IN（推进） | 摄影师沿现有轴线向她行走 |
| PULL-BACK（后拉） | 摄影师在保持构图的同时后退 |
| TRACK（跟移） | 在她身旁以相同速度侧向移动 |
| PASS（越过） | 越过她先前的位置，进入新的侧向关系 |
| WRAP（绕侧行进） | 沿她的一侧行走，同时将她保持在画面内 |
| RISE（升高） | 随她进行真实的向上运动 |
| DROP（降低） | 随她真实下降，朝向下半身 |
| FLOOR SLIDE（贴地滑移） | 横向移动，镜头离地 5–15cm |
| OCCLUSION（遮挡） | 真实物体／身体部位暂时遮住镜头 |
| REVEAL（揭示） | 摄影师持续移动，直到她再次可见 |
| WHIP PAN（甩镜） | 由她的动作触发一次快速的真实摇摄，随后稳定 |
| RECOIL（后退响应） | 摄影师因强烈动作重音而短距离后退 |
| HERO LOCK（重点造型锁定） | 摄影师停步，实际保持机位 |
| TIME-CODE SYNC（时间码同步） | 舞蹈与摄影机共用一条绝对时间轴——按 1:1 同时启动、到达峰值、回收 |

每个词都是**具有起始位置、触发条件和结束位置的路径**，绝不是气氛形容。

## 禁用清单（导致旧稿失败的做法）

```
No camera jumping between positions
No camera movement for every beat
No repeated push-pull / repeated wrap / repeated roll
No orbit unless specifically written
No whip pan unless specifically written
No camera bob synchronized to individual footfalls
No automatic reframing after every body accent
No digital zoom / digital rotation / artificial parallax
```

> The performer generates the movement. The camera observes the movement. The camera moves only for a major spatial reason — and when it moves, it moves **on the same absolute time-code as the choreography**: start with the action, peak with the accent, recover with the release. One timeline, two synchronized motion tracks, one shared set of action peaks.

## 运镜块的五个部分

现代 H3 提示词中的每个摄影机块：

```
CAMERA POSITION:     where the camera is now (real meters)
CAMERA GEOMETRY:     height + distance + side + optical axis + perspective
CAMERA MOVEMENT:     how it travels from here to there (physical path)
MOVEMENT TRIGGER:    which written performer action releases the move
END CAMERA POSITION: where it actually ends up + final framing
```

零运镜片段仍须显式写明 `MOVEMENT: none` 和 `TRIGGER: none permitted`——空缺不写会让模型自行即兴漂移。

## 要点

真实录舞里，摄影师**先站稳，让舞者在画面里完成动作；只有舞者真的改变空间关系时，才移动一次**。每段只设一种主要行为，物理路径必须有触发条件和结束位置，并遵守让摄影机保持安定的纪律。配合*系统 A：物理摄影机位置库*使用——机位回答“在哪里”，运镜回答“如何移动，以及为什么现在移动”。
