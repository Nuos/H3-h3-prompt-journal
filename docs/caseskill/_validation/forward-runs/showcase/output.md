# H3 右入单状态展示与硬切装配：9 秒离线试用

本文件由案例的 `assets/output-template.md` 复制后填写。范围为提示词与编辑计划；没有生成或编辑任何媒体，没有改动技能文件。`plan.json` 是案例技能自己的编排清单，不是 H3 API 请求体。当前交付状态为 **draft**。

## 1. 当前任务与输入

用户已确定：最终 9 秒，三种袜子造型按 A→B→C 各展示 3 秒；每段人物从画面右侧进入，并结束在清楚展示袜子的 pose；成片 30fps；全片一首连续音乐。

| 输入项 | 当前值与证据状态 |
|---|---|
| 人物、三套造型参考 | 均未提供。未看过任何人物或造型图。 |
| 固定视觉锚 | 暂拟虚构成年女性、低马尾、白色圆领 T 恤、炭灰短裤、白色低帮鞋、白色无缝影棚、正面固定全身机位。全部是临时创作设定，不代表用户提供的形象。 |
| 三个袜子状态 | 暂拟 A 米白细竖罗纹、B 深海军蓝细绞花、C 酒红底奶油色小菱格；均为中筒。它们让当前无图 T2VA 草稿完整可读，不能冒充实际三套造型。 |
| 音频 | 当前没有音乐文件、时长、来源入点或节拍测量。3 秒与 6 秒是任务指定的计划切点，不声称已对拍。 |
| 画幅与文字 | 暂拟 9:16、1080×1920 编辑画布；关闭字幕、编号、横幅。生成端分辨率/画幅需按实际部署再确认。 |
| 运行时 | 仅采用技能离线官方资料的标准 4–15 秒、24fps；没有验证任何线上部署。最终 30fps 是后期规格。 |

## 2. 状态、不变量与当前模式

| 状态 | 袜子设计（临时） | 保持固定 | 允许变化 |
|---|---|---|---|
| A | 米白，细竖罗纹，棉质，中筒，无标志 | 人物文字设定、发型、主服装、鞋、场景、灯光、机位、动作节奏 | 袜子的颜色、材质、花纹 |
| B | 深海军蓝，细绞花针织，中筒，无标志 | 同 A | 同上 |
| C | 酒红底奶油色小菱格，细针织，中筒，无标志 | 同 A | 同上 |

**当前使用 T2VA。** 三份正文不写不存在的 `<Subject 1>` 或 `<Picture 1>`，`references` 保持空数组。缺失资产登记在 plan 中，但不绑定给模型。重复人物文字描述只能规定目标，不能证明独立生成后的身份一致。

参考到齐后，将人物图用于身份和固定主服装，将三个造型参考分别用于各自袜子状态；各段明确限定人物参考中的袜子不得覆盖当前状态。届时才能据真实文件改写 Ref2VA 的六字段正文和绑定表。只有实际首帧图满足“已经穿当前袜子且正在从右侧跨步进入”时，才考虑 I2VA；普通人物或造型照不是已建立的首帧。

## 3. 可立即执行的生成与编辑安排

1. 在实际运行前核对 H3 部署的时长与帧率支持。计划使用三个独立生成任务，每段 4 秒、24fps；每次只提交对应 `.txt` 正文，并在运行界面设置参数。当前没有提交推理任务。
2. 每段首帧已穿本段袜子，人物已在画面右缘向中心跨步；0–0.6 秒完成进入，0.6–1.3 秒落稳，1.3–2 秒形成展示姿势，2–4 秒持续保持。摄影机固定，身体与双脚完整可见。
3. 每段计划取原生 `[0,3)` 秒，即源帧 `[0,72)`。丢弃 3–4 秒余量；无需加速、减速或追加定格。最终保留窗的末端必须已经处于展示 pose。
4. 将 A/B/C 分别放在成片 `[0,3)`、`[3,6)`、`[6,9)`。硬切由上一段静止 pose 跳到下一段右侧跨步，空间和动作重置是预期效果，不要求动作无缝接续。段内不换装，不安排出画清屏或空镜过渡。
5. 以 30fps 恒定帧率时间线导出。每段 72 个源帧按原时长重采样为 90 个交付帧，合计 270 帧；先采用重复帧的帧采样，不改变动作速度。24→30 的运动节奏需看实际素材后判断，不能靠计划保证平滑；不预先引入光流造成袜纹变形。
6. 删除三个生成片段的全部音轨。待音乐到齐后，选定真实来源入点 `s`，只将同一音频文件的 `[s,s+9)` 连续放入成片 `[0,9)`。不在 3/6 秒重启音乐。若音乐不足 9 秒，须更换或明确修改用法，不悄悄循环。

### 编辑决策表

所有区间左闭右开；帧号从 0 起。

| 段 / 状态 | 生成 | 保留局部窗口 / 源帧 | 成片全局窗口 | 30fps 交付帧 | 入态 → 保留出态 | 音频全局窗口 |
|---|---|---|---|---|---|---|
| SEG_A / A | 4s × 24fps = 96 帧 | `[0,3)`s / `[0,72)` | `[0,3)`s | `[0,90)`，显示帧 0–89 | 右缘跨步 → 中央清晰 pose | `[0,3)`，连续音乐前段 |
| SEG_B / B | 4s × 24fps = 96 帧 | `[0,3)`s / `[0,72)` | `[3,6)`s | `[90,180)`，显示帧 90–179 | 右缘跨步 → 中央清晰 pose | `[3,6)`，同一轨不中断 |
| SEG_C / C | 4s × 24fps = 96 帧 | `[0,3)`s / `[0,72)` | `[6,9)`s | `[180,270)`，显示帧 180–269 | 右缘跨步 → 中央清晰 pose | `[6,9)`，同一轨不中断 |

切点位于输出帧 90 和 180 的起点，末边界为 270；270 是帧数和结束边界，不是最后一帧的编号。裁切验收看实际保留末帧（本计划源帧 71），不拿已丢弃的源帧 95 代替。若源片前 3 秒尚未完成 pose，优先重生成该段；调整裁点时必须重新记录入出点，仍保留右入与尾态，不能只因第 4 秒已经站稳就宣称前 3 秒可用。

## 4. 参考权限与文件

| 素材 ID | 实际文件 | 允许用途 | 不继承内容 | 生效范围 | 状态 |
|---|---|---|---|---|---|
| PERSON_REF | 未提供 | 后续身份、发型、主服装固定锚 | 不得用参考中的袜子覆盖 A/B/C 的目标袜子 | 全三段 | missing |
| LOOK_A_REF | 未提供 | A 的袜子颜色、纹理、材质、高度 | 未经明确指定的背景、其他人物、文字 | A | missing |
| LOOK_B_REF | 未提供 | B 的袜子颜色、纹理、材质、高度 | 同上 | B | missing |
| LOOK_C_REF | 未提供 | C 的袜子颜色、纹理、材质、高度 | 同上 | C | missing |
| MUSIC_MASTER | 未提供 | 后期整轨铺设，一首音乐连续 9 秒 | 不推断视频自带音轨，不把提示词当成原轨复制证据 | 全片 | missing |

### 英文 H3 正文

三份文本已写成完整三字段 T2VA 格式，各自只有 `[Shot 1]`，不存在未填占位符；两项声音字段均为 `N/A`，因为片段计划完全静音。按空白分词计数，三份正文分别为 353、355、355 词。

- `prompts/A.txt`：米白罗纹状态。
- `prompts/B.txt`：深海军蓝绞花状态。
- `prompts/C.txt`：酒红小菱格状态。

只将对应 `.txt` 的内容送入生成正文，不附带本工作表、审核表或 `plan.json`。这些草稿可用于临时视觉方案的无图试生成；准确复现用户人物和实际三套造型仍需补素材。

## 5. 验收表及缺项

| 验收对象 | 必查内容 | 当前状态 |
|---|---|---|
| 每段首帧 | 一人、当前袜子已生效、位于画面右侧且正在向内跨步 | 未生成，未验证 |
| 全段造型与身份 | 无换装或纹理漂移；人物、主服装、鞋、影棚和机位一致 | 参考缺失，未生成，未验证 |
| 保留尾态 | 在 3 秒之前已站稳，双脚/双袜可读；源帧 71 附近处于稳定展示 pose | 未生成，未验证 |
| 构图 | 全身与双鞋完整；袜口和袜纹清楚；没有额外人、重复肢体、文字 | 未生成，未验证 |
| 两个接缝 | 输出 89→90、179→180 为 pose→右入跨步硬切；无空帧/转场 | 尚未剪辑 |
| 交付技术 | 9.000 秒、30fps 恒定帧率、270 个视频帧；帧采样与运动观感合理 | 仅算术计划，未编码 |
| 连续音乐 | 单一真实原轨从所选入点持续铺满 9 秒；无生成音轨残留或切点重启 | 音乐缺失，未混音 |

真实未决事项：人物参考；三造型参考或精确描述；音乐文件、长度和入点；实际运行时参数；画幅/分辨率、主服装与场景的临时选择是否合适；生成后的人物、纹理、动作、构图、音频与接缝表现。只收到图像也不能提前关闭媒体验收项。

### SRE 案例检查记录

下列状态区别了计划已经写出和媒体已经验证。`SRE08=pass` 仅指人工审阅了本任务的策略适用性；不表示视频通过。

| ID | 状态 | 证据与边界 |
|---|---|---|
| SRE01 | unverified | Plan and all three prompts specify one independent T2VA generation per state and right-entry stride from frame 0. No generated frames exist to verify execution. |
| SRE02 | unverified | Retain [0,3) with hold from 2 s; hard cut to next clip entry stride. The pose-to-stride reset is deliberate. No actual seam has been inspected. |
| SRE03 | unverified | Fixed descriptors are repeated verbatim except the sock catalogue. Real person/look references are absent; appearance consistency and future reference-retention exceptions are not verified. |
| SRE04 | unverified | All prompts prohibit exit, empty interval, second person and in-shot state changes. Actual generated behavior remains unverified. |
| SRE05 | unverified | Plan strips clip audio and lays one original music track across 0–9 s. No music file or rendered mix exists; actual audio reuse has not occurred. |
| SRE06 | not_applicable | No source video, cut detector or candidate-cut analysis is used in this offline task. Historical thresholds and the historical 4.4-second candidate are not imported as evidence. |
| SRE07 | unverified | Offline standard is 4–15 s at 24 fps. Each draft requests 4 s and plans a 3 s crop; 30 fps is editing output only. Actual deployment capability has not been checked. |
| SRE08 | pass | Manual review of this plan: separate states and right entry follow this user task; text is an explicit provisional off setting. These are local creative choices and are not stated as universal H3 restrictions. |

## 6. 实际脚本运行

在技能根目录实际执行，Python 标准库，无联网、无模型调用：

```bash
python3 scripts/audit_plan.py /workspace/scratch/4a76d93cd636/research/forward-runs/showcase/plan.json --check-files
python3 scripts/audit_plan.py /workspace/scratch/4a76d93cd636/research/forward-runs/showcase/plan.json --strict --check-files
```

| 运行 | 退出码 | 错误 | 警告 | 解释 |
|---|---:|---:|---:|---|
| 草案检查，加正文文件检查 | 0 | 0 | 12 | 结构、提示词字段和时间算术未报错；资料及实际验收仍不完整。 |
| 严格检查，加正文文件检查 | 1 | 13 | 0 | 未达到 ready；真实缺项与尚未实施检查导致不通过。 |

严格检查 13 条错误由 `status=draft` 1 条、未决事项 1 条、缺失资产 5 条、未实施的 SRE01/02/03/04/05/07 共 6 条组成。没有把这些项目改成虚假 pass 来消除错误。机器输出明确记录 `semantic_validation=not_performed`、`model_inference=not_performed`，人工检查声明也未被脚本独立证实。

完整输出见 `audit-draft.json`、`audit-strict.json`，命令、退出码和汇总见 `audit-runs.json`。这次试用表明技能能给出可执行的两种时间线和有效的静态格式检查，也能在缺图、缺音频、未验证运行时的情况下保留严格门槛；它没有验证生成质量。

## 7. 本次依据

仅使用指定案例技能的离线文件，无新联网查询。下列路径均位于案例根目录 `/workspace/scratch/4a76d93cd636/H3-h3-prompt-journal/docs/caseskill/h3-sock-showcase-right-entry-three-shot/`：

- `SKILL.md`：工作流、输出要求和必跑审计。
- `references/case-method.md`：每状态独立生成、右入→pose→硬切、4 秒生成后裁为 3 秒的双时间线。
- `references/h3-official.md`：离线官方固定版本的字段格式、T2VA 无引用规则和 4–15 秒/24fps 标准；本次没有把离线资料称为已验证的当前部署能力。
- `references/plan-schema.md`、`assets/case-contract.json`：计划结构、人工检查职责和严格检查含义。
- `scripts/audit_plan.py`：实际运行的静态检查程序。
