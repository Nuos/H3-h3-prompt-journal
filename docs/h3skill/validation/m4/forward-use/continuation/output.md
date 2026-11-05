# 剑舞段落动作接续审计与修订

## 1. 审计结论与证据边界

草稿与当前批准的计划条件存在直接冲突，应撤回“参考图姿态就是首帧”“再次拔剑”“改为左手持剑”“完整继承运动源及音轨”和“已通过连续性门禁”等表述。修订保留海滩剑舞及借用挥剑运动质地的目标，把本段明确接到**唯一一把剑已出鞘、由解剖学右手持有、原剑鞘留在腰侧且为空**的计划状态；末态继续满足右手持剑。[I]

本次交付是人类可读的动作计划草案及 Ref2VA 动作正文片段。可确认的是输入约束之间的关系、原草稿的文字冲突及修订稿对已知道具状态的语义一致性。未提供真实图片、视频、音频或生成结果，因此没有媒体观察、实测拍点、接触物理验证或生成片连续性结论，也没有执行 H3 或结构校验器。[I][S][A]

证据优先级为：本任务已批准条件 → 与其兼容的技能约束 → 固定提交中的案例方法论。案例支持外观锁定与状态锁定分开、独立片段显式交代状态等方法；案例中的具体动作或某一版本的全曲安排不会自动成为本任务已批准条件。[I][C][S]

## 2. 问题清单

| 草稿问题 | 冲突或缺口 | 本次修订及责任 |
| --- | --- | --- |
| `integrated_multimodal_description` | 与本任务 Ref2VA 模式的正文映射不符。 | 动作片段归入 `detailed_description`；完整装配交 M11。本次按要求不输出六字段。[L] |
| `begins exactly in the reference photo's sheathed pose` | 身份图只提供人物与原道具外观，并未被授权为本段首帧。把该姿态当起点会覆盖已出鞘的计划状态。 | 去掉姿态锚定；M2 保持素材角色边界，M8 提供本段完整计划入态。[I][C][L] |
| `draws the sword again` | 前一段计划出态已是出鞘，剑鞘为空；没有再次入鞘、时间省略或状态重置的批准。 | 删除重复拔剑，直接承接已出鞘的持剑表演；不补造入鞘事件、第二把剑或隐藏转场。[I][O] |
| `now in the left hand` | 从已知右手持有跳到左手，没有合法接续，且段末仍要求右手持剑。 | 移除左手改持，沿用现有右手握持；不增添未经批准的双手交接来替草稿解围。这是本段的保守接续修订，不是替全曲新增永久持物规则。[I][M][O] |
| `Follow <Video 1> completely, including its actor and soundtrack` | 只批准借用一段挥剑的运动质地；完整继承源人物、服装、场景、剪辑及音轨超出范围。`<Video N>` 的整段视频语义也不应代替孤立运动属性绑定。 | M2 确定运动源选段和授权属性；M11 将运动/姿态属性映射到合适的 Subject 引用，避免完整 Video 继承。本次没有真实素材注册表，英文片段不用虚构数字标签。[I][L] |
| `At 2.000 seconds, the camera cuts close` | 没有动作时长、实测拍点、机位或切点依据；精确数字与特写切镜均是未批准方案。 | 删除时间与摄影安排。M7 协调动作容量与时窗；若需要切镜，交 M5/M9 协调。连续表演本身也不等于已经批准一镜到底。[I][A] |
| `proves that the sword contact is physically correct` | 未说明要接触的目标或机制；镜头接近不能证明力学正确，文本更不能证明生成接触已正确。 | 只保留现有右手与剑柄握持的计划要求，不新增碰撞、击中或承重接触；M4.2 审动作机制，M5 审可见性，M12 在有媒体后审实际结果。[I][M][A] |
| `The finished video has passed the continuity gate` | 没有成片、门禁记录或实际状态观测。 | 删除通过声明，将当前状态写为文字审计及动作语义草案；媒体门禁留待实际材料到位后处理。[I][A] |

## 3. 动作语义修订草案

以下 ID 仅用于本报告追踪，不是 H3 素材标签、镜头号或已登记的运行时实体：角色 `dancer_01`，剑 `sword_01`，剑鞘 `sheath_01`，动作事件 `sword_phrase_01`。[K][L]

| 项目 | 已知约束与本次草案 |
| --- | --- |
| 目标 | 同一角色延续海滩剑舞，在一段挥剑中使用经限定授权的运动质地。运动源具体选段及其可描述质地尚未提供；不能声称已经提取或复现。[I] |
| 入态与前提 | 唯一一把剑已出鞘，解剖学右手持有；原剑鞘固定腰侧且为空。此为计划入态。完整站姿、支撑脚、朝向、重心和前段残余动量未知，不能声称已从上一段视频读取。[I][O] |
| 触发 | 在与上述入态相容的表演准备成立后进入挥剑；不绑定未经确认的音频拍点或 `2.000` 秒。[E] |
| 机制草案 | 支撑与重心移动连接躯干转动，带动右肩、右臂和手腕完成挥剑；右手保留剑柄握持，剑路应具有身体净空和可控制的减速。这里给出机制要求，尚未批准具体支撑脚、步幅、挥剑平面、幅度、速度或空间坐标。[M] |
| 接触与持物 | 已知相关接触是右手与剑柄的握持。没有指定外部接触对象，因此不增加刀刃碰撞、击中、触地或接收动作，也不把它们伪记为已验证的不适用项。[I][M] |
| 结果与恢复 | 挥剑后经过可解释的减速与衔接，再进入可兼容的后续动作；不要求瞬间逆向，不擅自添加结束定格。具体恢复姿态和动量需随下一动作及时间窗确定。[O] |
| 出态与后继前提 | 段末仍为右手持有同一把已出鞘剑，原剑鞘仍留在腰侧且为空。更完整的出态需要补齐支撑、姿态、朝向、空间位置和动量，才能判断下一动作是否可直接接续。[I][O] |

| 状态项 | 本段计划入态 | 本段计划出态 | 当前可确认范围 |
| --- | --- | --- | --- |
| 剑数量与身份 | 唯一原剑 | 同一原剑 | 文字层保持一致 |
| 持有者与手 | 同一角色，解剖学右手 | 同一角色，解剖学右手 | 草案沿用既有握持，不增设交接 |
| 出入鞘 | 已出鞘 | 已出鞘 | 没有批准的入鞘、再次拔剑或重置 |
| 剑鞘 | 腰侧固定且为空 | 腰侧固定且为空 | 外观与当前占用状态分开约束 |
| 支撑、姿态、朝向、位置、动量 | 未提供完整数值或描述 | 待动作及后继协调 | 尚不能确认全身状态连续或动作可达 |

以上入出态均是计划关系，不是对生成片的观察。独立片段需要自足的状态说明；获得更多计划信息后，应把具体入态直接写入片段，而不是只要求模型“记住上一段”。[C][O]

## 4. 英文 Ref2VA 动作正文片段

下面只给出 `detailed_description` 内的动作正文，不是完整六字段成品。人物与运动源采用描述性指称，等待 M2/M11 按实际素材注册表绑定；“supporting stance”和“clear, controllable path”仍是待空间与时间协调的机制要求。片段不声明最终可执行性或媒体验证通过。[I][L]

```text
The beach sword-dance phrase begins with the same character holding the single, already-unsheathed sword in the anatomical right hand. The original empty scabbard remains secured at the waist. Continue from this planned prop state without another draw or a hand transfer.

Borrow only the movement quality of the selected sword-swing reference. Preserve the established character and original prop appearance in the beach setting; the source actor, costume, environment, editing and soundtrack are outside the transfer scope.

From a compatible supporting stance, connect the weight shift and torso rotation to the right shoulder, arm and wrist as they drive the sword sweep. Maintain the existing right-hand grip on the hilt. Guide the blade along a clear, controllable path, then decelerate through coordinated torso and arm control so the phrase can flow into a compatible following movement. At the end of this segment, the same sword remains unsheathed in the anatomical right hand, and the original empty scabbard remains secured at the waist.
```

该片段明确了必要道具状态和动作机制方向，保留了剑舞目标。它没有填造来源视频的具体节奏、轨迹、速度或力量质地；这些内容须在运动源可用、空间与时长协调完成后具体化。未给声音方案也不等于决定静音。[I][M][A]

## 5. 责任交接

| 责任模块 | 需要接收或处理的事项 | 本次不能代为确认的事项 |
| --- | --- | --- |
| M2：参考与绑定 | 区分身份/原道具外观参考与运动质地参考，明确实际运动源、选段和可转移属性。 | 真实素材身份、源动作观察结果、未授权内容的继承。 |
| M3：空间 | 以计划入态确定支撑、剑路、身体净空、可达范围及方向关系。 | 未知机位或空间下的精确动作可行性。 |
| M4.1–M4.3：动作 | 维护事件前提；细化支撑—驱动—握持—剑路—减速；明确结果与后继要求。 | 没有源动作、空间和时窗时的完整机制闭合。 |
| M8：状态 | 接收本报告的入出态要求，维护正式连续性状态；补齐站姿、朝向、位置、动量，并核对前段计划出态。 | 把本报告自动写成已接受的权威状态，或把计划状态当成实际视频状态。 |
| M7：时间 | 给动作准备、挥动、减速与衔接分配可行时窗，必要时提出简化或分段建议。 | 实测拍点、精确秒数或凭空加速。 |
| M5 / M9：可见性与边界 | 如后续需要摄影或切镜，保证关键握持及接续状态可读，并核对切点两侧状态。 | 特写证明物理正确；未经批准的切镜、时间省略或重置。 |
| M6：声音 | 接收“不继承运动源音轨”的授权边界，待声音需求明确后再协调。 | 默认照搬源音轨、默认静音或虚构声画拍点。 |
| M11：H3 编译 | 将修订动作放入 Ref2VA 正文字段；用实际注册素材建立正确标签绑定；仅在确有镜头计划时生成镜头标记。 | 将语义占位片段冒充已绑定、可直接提交的完整六字段提示词。 |
| M12：实际结果审计 | 获得真实媒体后核对人物/道具、握持、动作机制、时序和段间连续性，将问题返回对应责任模块。 | 在没有媒体时宣布接触正确、成片连续或门禁通过。 |

这些交接按实际依赖处理，不要求为本次文字修订机械地运行全部上游模块。[S][A]

## 6. 可以确认到哪一层

- **已完成：输入与文字审计。** 已区分批准条件、冲突草稿、技能规则和案例依据，指出重复拔剑、持手跳变、引用越权、时间/摄影越权及伪验证声明。
- **已完成：有限的动作语义修订。** 已知剑/手/剑鞘状态的文字接续闭合，剑舞及限定运动借用目标保留；机制只到草案层，具体空间与时长仍开放。
- **未完成：完整计划验收。** 没有完整依赖版本、正式 M8 接收结果、精确起终姿态、运动源绑定或时窗，不能授予整体 G2 通过。没有运行结构校验器，不能宣称结构校验通过。
- **未进行：生成与媒体验证。** 没有 H3 运行、真实图像/音视频或成片审计，不作 G3/G4 通过声明。局部文字检查不能替代这些层级。[K][A]

剩余未知集中在：实际运动源及选段、运动质地的具体描述、完整计划入态、身体与剑的可行空间路径、动作时窗与后继状态，以及未来成片是否兑现计划。本次保留这些缺口，不追加摄影、声音或时间省略方案。

## 7. 来源与读取范围

下列路径均相对于仓库根目录；精确 SHA256、案例提交及片段范围见同目录 `read-manifest.json`。

- [I] `docs/h3skill/validation/m4/forward-use/continuation/input.md`：本任务输入及当前批准条件，完整读取。
- [S] `docs/h3skill/h3-action-performance/SKILL.md`：M4 主技能，完整读取。
- [K] `docs/h3skill/h3-action-performance/references/contract-guide.md`：计划契约与验收边界，完整读取。
- [E] `docs/h3skill/h3-action-performance/references/performance-events.md`：事件与前提，完整读取。
- [M] `docs/h3skill/h3-action-performance/references/action-mechanics.md`：动作机制，完整读取。
- [O] `docs/h3skill/h3-action-performance/references/outcomes-and-continuation.md`：结果与接续，完整读取。
- [A] `docs/h3skill/h3-action-performance/references/audit-and-handoff.md`：审计与责任交接，完整读取。
- [L] `docs/h3skill/h3-action-performance/references/h3-label-mapping.md`：Ref2VA 字段与标签映射，完整读取。
- [C] `case-studies/2026-10-kanzaki-beach-sword-dance-18-segment/methodology.md`：按提交 `545a99015cfa00a6f07ee05d1d0f21e09d89d46c` 取得原始字节并计算 SHA256，通过关键词选取片段；语义引用限于已显示的外观/状态分离、全曲道具状态及独立片段不应重置参考图起态等内容，不声称已逐段审阅全文。

本次未联网，未读取 `tests` 或其他试用输出，未修改技能包或其他仓库文件；仅写出本报告与读取清单。
