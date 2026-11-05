# h3-camera-visibility：两次前向试用

## 使用范围与证据边界

本记录按指定的 `h3-camera-visibility` 技能完成两项自然语言任务。任务一仅执行 M5.2 构图／可见性审计；任务二执行 M5 摄影方案、焦点要求与 H3 Ref2VA 字段交接。输入只来自本次任务文字与下列实际读取的技能文件。

任务中的摄影位置、距离、动作顺序和参考用途属于用户给定条件；本文新增的构图、路径和焦点安排属于设计建议。当前未提供实际照片、视频、镜头视场、人物尺寸或生成结果，因此不能将方案一致性检查说成真实同框、光学可行性、参考还原或成片质量已经通过。未运行生成、合同验证脚本或其他模块，也未修改技能或仓库。

## 任务一：柜台交接钥匙的 M5.2 审计

### 1. 结论

**现有描述不足以确认“手部交接与接收者脸部反应同框”，但也不足以判定该要求无法实现。** 摄影机在柜台侧面、距手约 1.2 米、高约 1 米、光轴看向双手，只确定了部分机位关系。脸能否进入画面，还取决于视场、画幅及手与脸的相对位置；双手和脸进入画面以后，钥匙、握持关系与表情是否足够大、是否被挡住，又是另一层可见性问题。[构图与可见性规则](sandbox:/workspace/scratch/22d2b2ce8467/H3-h3-prompt-journal/docs/h3skill/h3-camera-visibility/references/framing-and-visibility.md)

本次可完成的是：规定需要同框的信息、找出遮挡和边界风险、给出尽量保留既有机位与动作的修改顺序。实际可见性结论保留为**待视场或画面证据确认**。

### 2. 已知条件与缺口

| 类别 | 内容 | 对本次审计的意义 |
|---|---|---|
| 用户给定机位 | 柜台侧面；距双手约 1.2 米；高度约 1 米；光轴看向双手 | 作为原有条件保留，不能据此计算覆盖到脸的范围 |
| 用户给定动作 | 接收者先握住钥匙，递出者再放手 | 构图必须让先后关系可辨，不改写动作链 |
| 必须传达的信息 | 双手、钥匙及握持关系；接收者的脸部反应 | 在交接的关键阶段同时可见，不能仅在交接后转去看脸 |
| 背景条件 | 另有一人经过 | 检查经过者在画面投影上是否遮挡脸或交接区；“在背景”本身不保证不遮挡 |
| 缺失条件 | 视场／画幅、人物与柜台尺度、脸与手的相对位置、动作幅度及经过者的画面路径 | 无法验证画面边界、主体占比和全过程遮挡 |
| 未提供的证据 | 实际画面、试拍或成片 | 不作真实观测、像素尺寸或成片通过声明 |

焦距与传感器尺寸缺失并不要求先补齐所有摄影参数；实际视场、构图预览或一张能够代表该机位的试拍也能支持后续同框判断。当前没有这些证据，故不补造焦距、俯仰角或“已能看见脸”的结论。

### 3. 分阶段可见性审计

| 阶段 | 画面必须让观众看清的关系 | 遮挡／边界风险 | 本次状态 |
|---|---|---|---|
| 接收者接触前 | 钥匙由递出者持有；接收者的手接近；接收者反应区域在画面内 | 光轴只对准手时，脸可能超出上边界；柜台边沿可能挡住手指接触处 | 条件未充分，尚不能确认 |
| 接收者握住、递出者仍未松手 | 两人短暂共同接触钥匙，接收者已建立握持 | 双手叠在一起，可能无法辨认谁先握住；钥匙被完全藏住，接触关系丢失 | 须以构图保留关键接触线索 |
| 递出者放手 | 递出者手指松开／手离开，接收者仍握住钥匙；脸部反应同时可读 | 松手动作越出边界；递出者手臂或经过者遮挡接收者脸部 | 须保留离开空间并避免关键遮挡 |
| 交接成立 | 接收者保持持有，递出者已脱离；接收者反应与交接结果能被关联 | 接收者把钥匙带出画面太早；背景运动抢占或遮断信息 | 需要容纳既有动作范围，不能假定保持不动 |

不要求钥匙每一处轮廓始终完整外露。手指自然覆盖钥匙的一部分可以接受，只要握持建立、递出者释放和最终持有者仍能被连续辨认。若关键的“先握住、后放手”完全被遮挡，则仅靠前后两帧各自持有钥匙不能证明中间交接顺序已可读。

### 4. 最小修改建议

**第一步只收紧构图要求，不改动作与既有机位参数。** 画面下部纳入双手、钥匙以及接触和松手所需的活动余量；上部纳入接收者完整的表情阅读区域；侧边保留辨认两只手归属所需的手臂线索。以关键交接阶段的双手和脸同时成立为准，不能只检查起始姿态。具体画面边界仍须由实际视场确定。

**第二步检查占比，而不把“纳入更多内容”当成自动解决。** 如果扩大覆盖使钥匙与手指关系小到不可读，或脸小到无法辨认反应，即使都在边界内，也没有满足目标。当前只能提出“动作关系和表情都可读”的结果约束，不能给出已有像素证据。

**第三步处理背景经过者的投影关系。** 优先用画面内的层次与边缘余量避开关键区域。在共同握持和松手阶段，经过者不应穿过双手、钥匙或接收者脸部的画面投影。如果既有构图无法做到，提出一项待采纳的最小调度建议：将经过者的通过区间或通过时机错开关键交接。该项涉及空间／调度的调整，属于交给相应负责人评估的建议，本次不执行 M3、M4 或其他模块重跑。

**仅当前三步不能满足同框时，再提出机位层面的候选修改。** 可评估最小幅度改变取景覆盖或光轴，使手部区域和脸部区域共同进入有效画面。这里不擅自把高度、距离改成新的实测值，也不直接判定应换某个焦距。任何机位修改都需重新检查交接区是否仍能读清。这是 M5.1 的依赖提示，不是本次已实施的修改。

双手与脸是否同时清晰，是本次需注明的焦点依赖：M5.2 的“进入画面、无遮挡、占比足够”不等于已证明景深足够。这里记录“关键阶段两者都应具有足够的可读性”，不展开新的 M5.3 光学方案，也不补造光圈或焦距。[审计与交接规则](sandbox:/workspace/scratch/22d2b2ce8467/H3-h3-prompt-journal/docs/h3skill/h3-camera-visibility/references/audit-and-handoff.md)

### 5. 可直接替换的构图描述

> 保留柜台侧面的既有机位关系。构图在接收者握住钥匙、双方短暂共同接触、递出者放手和接收者继续持有这几个阶段，持续同时容纳双手、钥匙与接收者的脸部反应。双手周围留出接触和松手的活动空间，并保留辨认两只手归属的线索；脸部表情区域不被画面上边界裁掉。允许手指自然遮住钥匙的一部分，但握持建立、松手和最终持有关系应可辨。背景经过者保持在不遮挡关键交接区域与接收者脸部的画面位置。

这是取景目标，不是当前机位已经满足的验证报告。现有资料缺少视场和相对尺度，修改后仍需用实际构图检查关键阶段。

### 6. 本次完成与保留项

- 已完成：M5.2 的文字条件审计、阶段可见性要求、遮挡分类与最小修改顺序。
- 保留待确认：同框覆盖、主体占比、柜台与人物的真实遮挡、脸与手的同时清晰程度。
- 没有推定：1.2 米距离足以或不足以容纳脸；1 米机位必然产生某个俯仰角；任何具体焦距、传感器、视场、光圈或真实成片表现。

## 任务二：水面泡沫后的连续显露镜头

### 1. 方案结论与成立条件

采用**近水面的连续向前运动**：泡沫位于前景，人物位于其后，摄影机沿已选定的同一前进方向持续接近人物所在区域。人物轻轻转头，泡沫漂动及摄影机与前景、人物之间的相对位置变化共同改变遮挡，让脸通过缝隙逐渐获得可读范围。全程保留水线作为空间参照；焦点以人物脸部为目标，允许前景泡沫虚化。

**向前运动本身不能保证泡沫缝隙一定打开。** 此方案的成立条件是：起始泡沫分布、漂动方向、人物位置与摄影机前进路径的组合，确实会让挡在脸前的投影逐步让开。没有实际媒体，本文只能设计这一条件，不能报告已经观察到某条缝隙、某段参考路径或某个转头时刻。[机位与光轴](sandbox:/workspace/scratch/22d2b2ce8467/H3-h3-prompt-journal/docs/h3skill/h3-camera-visibility/references/viewpoints-and-axis.md)；[运动与触发](sandbox:/workspace/scratch/22d2b2ce8467/H3-h3-prompt-journal/docs/h3skill/h3-camera-visibility/references/movement-and-triggers.md)

### 2. M5 摄影方案

| 分项 | 自然语言方案 | 当前证据边界 |
|---|---|---|
| 观看任务 | 让观众经历遮挡逐渐减弱，并在连续空间中看清人物轻微转头后的脸 | 创作目标，不是已生成表现 |
| 起始视点 | 摄影机处于水面附近，从前景泡沫一侧朝后方人物取景；画面已经保留水线与人物可被定位的线索 | 不指定真实高度、距离或泡沫尺度 |
| 主路径 | 沿同一前进方向平稳向前移动，保持运动方向连续 | 不以变焦、裁切或反向运动代替前进；实际视频路径尚待读取 |
| 光轴 | 以人物脸部所在区域为观看目标；必要时连续小幅校正取景，使脸与水线留在画面内 | 轴向校正不得暗中改变主路径方向；不填写无依据角度 |
| 层次 | 前景泡沫—后方人物—可辨水线；泡沫是显露结构的一部分 | 不假定所有层次同时锐利 |
| 结束状态 | 缝隙扩大到足以读出脸部反应，轻微转头仍可被理解；在该有效构图内结束这一镜头 | 没有指定秒数、固定行程或硬性停止点 |

摄影机的“同一方向”指其平移的主方向保持一致；取景朝向与平移方向分别描述。若实际参考路径含有转弯、后退、剪辑或不能保留水线的段落，不能把这些内容未经说明带入本方案，需在读取媒体后报告具体冲突。

### 3. 动作与摄影事件分开安排

| 连续阶段 | 人物动作 | 摄影机／前景变化 | 应出现的信息 |
|---|---|---|---|
| 建立遮挡 | 人物位于泡沫之后，头部姿态可被连续追踪 | 摄影机开始或已经处于缓和的向前运动；前景泡沫漂动 | 观众能判断人物在泡沫后方，而非凭空出现 |
| 渐进显露 | 人物轻轻转头，不改变既定身份与连续位置 | 前进持续，泡沫在相对投影中逐步让出面部窗口 | 面部可见部分逐渐增加，转头过程不被突变替代 |
| 形成可读窗口 | 转头进入可读的朝向，可自然延续或缓和 | 摄影机继续同向推进，维持有效取景余量 | 脸部关键表情特征获得连续、足够的可见范围，水线仍在 |
| 收束 | 人物保持自然连续状态 | 在已经成立的显露构图内结束；若需缓和运动，只改变推进速度，不反向 | 结果可被读到，不在刚露出的一瞬间立即丢失 |

选择的摄影关系是“提前建立并持续推进”，不要求摄影机与每一个转头节点严格一比一同步，也不编造秒数或帧号。泡沫仍可自然掠过脸的局部，但在显露后不应持续遮住使表情不可读的关键区域。短时遮挡期间，人物和摄影机的位置、运动应保持可解释的连续关系；不通过切镜、更换站位或无过渡的突然显现完成显露。

如果将来实际素材表明现有泡沫与路径不能形成窗口，应先记录这一局部不满足，提出调整起始相对构图、泡沫漂动安排或路径的候选建议。不能在“已满足同向前进”之名下直接添加绕行，也不能改变视频参考的授权范围。

### 4. 焦点与清晰度要求

**焦点从建立镜头时就以人物脸部所在距离层为目标，并随前进维持脸部的可读性。** 即使脸仍被泡沫部分遮挡，焦点也不应被前景泡沫吸走；面部从缝隙露出时，应立即具备足够清晰度。这里提出的是清晰度目标，不宣称已经测出对焦距离或景深。

前景泡沫可以虚化，其轮廓和漂动仍应足以构成可辨的遮挡与缝隙。水线必须保留在画面中，并能作为水面与人物空间关系的视觉参照；“保留水线”不自动意味着水线、泡沫与脸全部同等锐利。若虚化使泡沫成为不可辨的大块遮蔽，或水线完全无法识别，即使脸清楚也没有完整满足方案。

本方案不安排先对泡沫、再拉到脸的焦点转移，因为当前观看目标要求面部显露后直接可读，前景清晰不是必要条件。若后续创作明确要求先读泡沫的细节，再读脸，才需要另行讨论焦点转移的触发与重获清晰的时间。当前不补造焦距、光圈、传感器尺寸、拉焦距离或景深范围。[焦点与景深规则](sandbox:/workspace/scratch/22d2b2ce8467/H3-h3-prompt-journal/docs/h3skill/h3-camera-visibility/references/focus-and-depth.md)

### 5. 参考边界与 H3 Ref2VA 交接

这是 Ref2VA 的**参考生成**设计：照片只提供人物身份，视频只提供摄影路径。照片不自动成为第一帧；视频不授权复制其中的人物、场景、动作、焦点、剪辑或声音。摄影路径以外的水面、泡沫显露、转头与焦点安排来自本次创作要求。

当前未附实际媒体，以下 `<Subject 1>` 与 `<Video 1>` 是**待绑定的占位标签**。它们不是已读取的媒体事实，也不代表已经创建了可提交的完整输入。身份照片只作为 `<Subject 1>` 的来源说明，不另建一个要求模型锚定具体帧构图的 `<Picture 1>` 条目。最终标签编号和实际媒体对应关系交给 M11 按实际输入整理。[H3 映射规则](sandbox:/workspace/scratch/22d2b2ce8467/H3-h3-prompt-journal/docs/h3skill/h3-camera-visibility/references/h3-label-mapping.md)；[Ref 官方协议本地副本](sandbox:/workspace/scratch/22d2b2ce8467/H3-h3-prompt-journal/docs/h3skill/h3-camera-visibility/references/h3-ref-official.txt)

六字段顺序保持如下。英文文本是可继续编排的内容草案；未能填写的字段明确交接，不用虚构观察填满。

#### subject_definitions

> `<Subject 1>`: The person whose identity is supplied by the designated identity photograph. Use that photograph for identity only. The person's pose, expression, framing, background, and camera viewpoint are defined by this new shot.
>
> `<Video 1>`: The designated camera-path reference video. Use only its authorized camera trajectory. The requested shot uses one continuous forward direction; the reference's people, scene content, actions, focus treatment, cuts, and audio are outside its assigned role.

交接说明：实际身份描述、可引用的路径内容和是否存在方向冲突，均需附上媒体后确认。这两条只是媒体角色与引用位置的定义，不含“照片里是什么长相”“视频如何运动”的虚构观察。

#### summary

> `[reference generation]` A single continuous shot near the water surface gradually reveals `<Subject 1>` through gaps in drifting foreground foam. The camera advances in one consistent forward direction, using `<Video 1>` only as the designated camera-path reference. `<Subject 1>` gently turns their head as the face becomes readable. Keep the waterline in frame and maintain readable facial detail while allowing the foreground foam to remain soft.

#### retention_analysis

| 标签 | 拟用保留方式 | 限定范围 |
|---|---|---|
| `<Subject 1>` | `fully_preserved` | 完整保留获授权的身份特征；不要求保留照片的姿态、表情、光线、背景或构图 |
| `<Video 1>` | `attribute_transfer` | 只迁移已授权且符合本次约束的摄影路径；实际路径是否兼容要等媒体提供后确认 |

英文交接文本：

> `<Subject 1>` — `fully_preserved`: Preserve the identity supplied by the designated photograph within its identity-only role. The new shot defines the person's head turn, expression, surrounding water, foam, framing, and focus treatment.
>
> `<Video 1>` — `attribute_transfer`: Transfer the authorized camera trajectory only, subject to the requested continuous forward direction. Do not inherit the reference video's people, action, setting, cuts, focus treatment, or audio.

这些是保留目标，不是已经验证的还原结果。如果实际参考视频路径与单一方向前进冲突，不能把筛选或改造后的路径冒充完整复现，应先说明冲突再落实实际引用范围。

#### detailed_description

> Use a restrained, continuous visual treatment with a clear relationship between the foreground foam, the person behind it, and the waterline. Let the foreground remain soft while the face carries the readable detail.
>
> `[Shot 1]` Near the water surface, drifting foam occupies the foreground and partially obscures `<Subject 1>` behind it. Keep the waterline visible in the composition. The camera advances smoothly in one consistent forward direction toward the person's area, following the authorized forward trajectory assigned to `<Video 1>`. Maintain a continuous view toward the face, with only the framing adjustment needed to keep both the face and the waterline in the image.
>
> `<Subject 1>` gently turns their head while the camera continues forward. Arrange the starting foam gaps and their drift so that the foam progressively clears a viewing window across the face. Let the reveal grow from partial facial visibility into a sustained view of the features needed to read the person's expression. Keep the person's position and motion continuous throughout any brief foreground occlusion.
>
> Maintain focus on the face as the camera approaches, so that newly exposed facial features are readable as soon as they appear. The foam may remain out of focus, but its moving edges and gaps should still communicate the gradual reveal. Continue the same forward movement into the readable facial view, retaining the waterline and enough framing margin for the gentle head turn. End within this clear, continuous composition.

只有一个 `[Shot 1]`，不加时间戳，不把显露阶段拆成新的镜号。这里的“Arrange”是生成设计指令，不是对实际泡沫分布的观察。

#### overall_soundscape

**交接状态：待声音要求确定。** 当前没有提供声音要求或声音参考。摄影路径视频不赋予声音复制权限。该字段应由 M6／最终编排环节依据实际声音意图填写；本次不凭空增加水声、呼吸、对白，也不把未给出声音要求解释为必须静音。

#### non_diegetic_music

**交接状态：待音乐意图确定。** 当前未要求配乐或无配乐。本次不新增音乐参考、不指定曲目，也不把摄影路径的视频音轨带入该字段。最终输出需要明确音乐意图后填写。

因此，本次提供的是完整的**六字段交接结构与 M5 可负责的内容**，不是已经绑定媒体、确定声音并完成协议封装的投递成品。自然语言方案已完成，不需要为它构造机读 JSON 或补跑其他模块。

### 6. 可检查的结果范围

| 检查层级 | 可以检查什么 | 当前结果 |
|---|---|---|
| 文字方案 | 单镜头、方向、光轴、遮挡显露、人物动作与焦点目标之间是否自洽 | 已完成文字审计；方案有明确成立条件 |
| 参考授权 | 照片是否仅提供身份，视频是否仅提供摄影路径；标签角色是否混用 | 文字边界已明确；实际媒体绑定未验证 |
| 实际路径 | 成片摄影机是否持续同向前进；是否以变焦、反向、绕行或切镜替代 | 当前无成片，未验证 |
| 遮挡与显露 | 脸是否通过漂动泡沫的缝隙逐渐显露；遮挡前后空间是否连续 | 当前无媒体，未验证；不能由“向前”推导为已满足 |
| 构图与焦点 | 水线是否持续在画面中；面部显露时能否读出反应；前景虚化是否仍保留缝隙关系 | 当前无画面和光学信息，未验证 |
| 参考保留 | 实际身份与路径是否按授权范围保留，且未带入无关内容 | 需参考媒体与生成结果对照；当前未验证 |
| H3 协议交付 | 六字段顺序、实际标签编号、真实媒体对应、声音字段是否完整 | 已给结构与角色规则；未执行最终封装或验证脚本 |

实际结果检查应针对可见表现，不声称从没有标定的画面中恢复了精确焦距、距离、运动速度或三维轨迹。本次没有 G3／G4 的真实媒体或成片通过证据。[审计与交接规则](sandbox:/workspace/scratch/22d2b2ce8467/H3-h3-prompt-journal/docs/h3skill/h3-camera-visibility/references/audit-and-handoff.md)

## 实际读取记录

以下记录仅列实际读取过的文件。范围中的“完整”表示已补读首次输出中被截断的部分；没有把可见目录名或引用链接当成已读取文件。

| 序号 | 绝对路径 | 实际读取范围 | 用途 |
|---|---|---|---|
| 1 | `/workspace/scratch/22d2b2ce8467/H3-h3-prompt-journal/docs/h3skill/h3-camera-visibility/SKILL.md` | 完整；首次输出有短截断，补读第 40–70 行 | 模块职责、执行范围、资源导航 |
| 2 | `/workspace/scratch/22d2b2ce8467/H3-h3-prompt-journal/docs/h3skill/h3-camera-visibility/references/contract-guide.md` | 完整；补读第 30–75 行 | 独立子模块、自然语言交付和验证边界 |
| 3 | `/workspace/scratch/22d2b2ce8467/H3-h3-prompt-journal/docs/h3skill/h3-camera-visibility/references/framing-and-visibility.md` | 完整 | 任务一 M5.2；任务二遮挡与显露 |
| 4 | `/workspace/scratch/22d2b2ce8467/H3-h3-prompt-journal/docs/h3skill/h3-camera-visibility/references/h3-label-mapping.md` | 完整；补读第 28–83 行 | Ref2VA 字段顺序、标签、保留方式、镜号 |
| 5 | `/workspace/scratch/22d2b2ce8467/H3-h3-prompt-journal/docs/h3skill/h3-camera-visibility/references/viewpoints-and-axis.md` | 完整 | 水面附近机位、主路径和光轴分离 |
| 6 | `/workspace/scratch/22d2b2ce8467/H3-h3-prompt-journal/docs/h3skill/h3-camera-visibility/references/focus-and-depth.md` | 完整 | 面部清晰、前景虚化及未测量边界 |
| 7 | `/workspace/scratch/22d2b2ce8467/H3-h3-prompt-journal/docs/h3skill/h3-camera-visibility/references/movement-and-triggers.md` | 完整；补读第 15–55 行 | 连续前进、事件关系及遮挡后连续性 |
| 8 | `/workspace/scratch/22d2b2ce8467/H3-h3-prompt-journal/docs/h3skill/h3-camera-visibility/references/audit-and-handoff.md` | 完整 | 执行／审计状态、责任边界、交付与未验证项 |
| 9 | `/workspace/scratch/22d2b2ce8467/H3-h3-prompt-journal/docs/h3skill/h3-camera-visibility/references/h3-ref-official.txt` | 部分；先作关键词检索，检索输出有截断；随后完整读取第 24–145 行 | 核对 Subject／Picture／Video／Audio 的角色、身份照片引用方式、summary 的 `[reference generation]` 前缀 |

没有读取：案例 evidence/index、其他历史案例、仓库其余文档、个人记忆、实际媒体、schema 与脚本。未检查案例证据文件是否已经落盘，也没有把未读到的证据链接说成已核验。机器合同与脚本的有效性不在本次前向试用结论中。

## 前向试用发现与后续复验点

### 已能顺利完成的路径

1. **M5.2 可以独立处理用户已有机位与动作。** 两个数值被作为给定条件保留，没有被提升为足够证明视场、清晰度或同框的证据，也没有要求重跑前置模块。
2. **M5 可以区分“摄影机向前”与“面部被显露”。** 显露被写成需由起始遮挡关系与相对运动共同满足的条件，避免把推进方向当作画面结果的充分条件。
3. **无媒体仍可完成有边界的 Ref2VA 交接。** 身份照片没有被自动提升为首帧，摄影路径视频没有被扩大为全视频编辑、动作、焦点或声音参考。

### 本次暴露的使用风险

- **同框与清晰可能被混为一项通过条件。** 任务一必须同时保留构图可见性与景深未验证两个状态；把脸写入构图不等于确认脸与手都清楚。
- **摄影路径标签仍需真实媒体复验。** 任务二的 `<Video 1>` 是未绑定角色。实际素材若含转弯或反向，必须重新确认可引用的路径范围；不能以当前占位草案声称已经匹配该视频。
- **六字段完整交接不等于六字段都能填入观察事实。** M5 的输入没有声音意图时，应明确声音字段的交接状态，不能为了形式完整而编造声场或断言静音。这次已保留该缺口。
- **自然语言流程不能替代机器合同测试。** 本次未读取或运行 schema／脚本，因此不对它们的可运行性、字段校验能力或接受回执作结论。

在已读规则支持的自然语言流程中，未发现阻止完成两项任务的确定性缺陷。以上风险是本次输出需要守住的边界，不能据此断言技能实现有 bug。案例证据、机器合同或脚本的具体问题，应由随后针对这些资源的读取与执行复验判断。


---

## 复核附录 A：retention_analysis 关系词修订（首次输出保留）

### 复核范围与明确更正

本附录保留前面两项首次试用输出原文，只更正任务二对 `<Video 1>` 的关系词判断，并补充可复现的任务文字和实际读取记录。首次输出末尾关于“未发现……确定性缺陷”的陈述是首次试用当时的判断；后续审阅现已发现下面这一项具体输出偏差，不能继续把该陈述理解为关系词已通过官方定义复核。

本轮实际读取了 [h3-ref-official.txt](sandbox:/workspace/scratch/22d2b2ce8467/H3-h3-prompt-journal/docs/h3skill/h3-camera-visibility/references/h3-ref-official.txt) 第 155–207 行。该段定义中，`fully_preserved` 判断的是参考内容的**已定义角色是否完整保留**；`attribute_transfer` 要求参考特征被转移给 **a different identifiable target subject（另一个可识别的目标主体）**。末段要求关系词只在 `subject_definitions` 已定义的参考角色内判定，也明确不把目标视频新增的动作、背景或情节事件自动算作参考保真度损失。

**首次输出把“视频只提供摄影路径”直接归为 `attribute_transfer`，依据不足，应修订。** “只提供摄影路径”是在限定 `<Video 1>` 的角色，不是在建立向另一个可识别主体转移属性的关系。新镜头具有不同人物、水面、泡沫或头部动作，也不能单独证明该路径角色只被部分保留。若媒体到位后，已授权且已定义的摄影路径被完整保留，则该角色内的关系可以是 `fully_preserved`。

当前没有实际照片或视频，因此 `<Subject 1>`、`<Video 1>` 仍是**未绑定占位标签**。摄影路径的具体内容、可引用范围及其与“沿同一方向连续向前运动”的相容性都待确认。下面的关系词仅表示有条件的设计保留目标，不是已观察到的素材性质，也不是已验证的生成结果。

### 修订后的 retention_analysis 交接草案

前提：后续在 `subject_definitions` 中确认照片的身份角色，以及视频实际获授权的摄影路径角色；不得未经确认自行截取路径片段、删掉反向或转弯后仍称完整保留。

```text
Design handoff only. Both references are unbound. The following relationship markers express provisional retention targets within the declared reference roles, not observed reference fidelity. The camera-path role and its authorized scope remain subject to confirmation when the media is supplied.

<Subject 1> (appears in [Shot 1]; identity only): fully_preserved - Preserve the person's identity supplied by the designated photograph. The new shot defines the head turn, expression, framing, environment, and focus treatment; those elements are outside the photograph's assigned identity-only role. Reference binding and identity fidelity remain unverified because the photograph has not been supplied.

<Video 1> (camera path only): fully_preserved - Preserve the authorized camera trajectory defined for this reference in subject_definitions, provided that the supplied trajectory supports the requested continuous movement in one forward direction. This is a provisional retention target, not a claim about an observed video. The reference video's people, scene content, subject actions, focus treatment, cuts, and audio are outside its assigned role. Confirm the actual path and its authorized scope when the media is supplied. If any defined path characteristics are changed or retained only in part, revise the relationship to partially_preserved and state those changes explicitly.
```

关系词的后续选择边界如下：

| 媒体到位后的实际参考关系 | 关系词处理 |
| --- | --- |
| 在确认的摄影路径角色内，定义的路径特征全部保留，且符合本镜头的连续向前要求 | 可采用 `fully_preserved`；另行核验生成结果是否兑现 |
| 同一已定义路径角色仍被使用，但其中某些特征被改变或只保留一部分 | 采用 `partially_preserved`，明确改变或遗漏了什么 |
| 实际只保留宽泛风格、类别、构图或氛围相似性 | 按官方定义评估 `weak_reference`；不能把它当作“尚未提供素材”的代称 |
| 确实将参考特征转移给另一个可识别目标主体 | 才评估 `attribute_transfer`，并指出源特征与目标主体；本任务现有输入尚未建立这种关系 |
| 素材尚缺、路径范围不明，或素材路径与用户要求冲突尚未解决 | 保留待绑定／待确认状态；不能凭缺失信息推断任何关系词已获事实验证 |

### 六字段交接仍不是投递成品

此次只修订 `retention_analysis` 的关系解释，不重做整份 M5 方案。六字段的交接状态复核如下：

| 字段 | 当前状态及未完成事项 |
| --- | --- |
| `subject_definitions` | 已限定照片只供身份、视频只供摄影路径；标签未绑定，实际路径及授权范围待媒体确认 |
| `summary` | 已给出所需连续镜头的设计概述；其中参考标签仍为占位，不能视为已匹配实际素材 |
| `retention_analysis` | 按本附录修订为角色范围内的条件化保留目标；没有实际保真度结论 |
| `detailed_description` | 自然语言摄影设计已完成；泡沫缝隙显露、面部清晰、水线留框及路径一致性仍需素材／结果检查 |
| `overall_soundscape` | 声音意图尚未提供，维持待交接状态；摄影路径参考不授予复制其声音的角色 |
| `non_diegetic_music` | 音乐意图尚未提供，维持待交接状态；不添加未经请求的音乐或默认静音结论 |

因此，该输出仍是**包含六字段结构的 M5 设计交接草案**，尚未完成实际媒体绑定、声音决策或最终协议封装，也没有 M11／生成结果验证。当前可检查的是自然语言约束与角色边界是否自洽，不能据此声称存在可直接投递且已验证的 Ref2VA 成品。本附录没有新增任何真实观测、镜头测量参数或路径片段。

## 复核附录 B：原始两项任务文字

以下逐字记录本次接收的两项测试任务，供复现；不把随后审阅意见混入原始任务。

### 任务 1

> 我已经有两名角色在柜台交接钥匙的动作。摄影机在柜台侧面，镜头离手约1.2米，高度约1米，光轴看向两只手。接收者先握住钥匙，递出者再放手。我要求同一画面能看见手部交接和接收者的脸部反应。背景另有一人经过。只帮我做 M5.2 构图/可见性审计和最小修改建议；无需重跑其他模块。现有资料没有焦距、传感器尺寸或视场。

### 任务 2

> 做一个水面附近的连续镜头，前景有飘动泡沫，人物在泡沫后轻轻转头；镜头要沿同一方向向前运动，让脸从泡沫缝隙逐渐露出。不要切镜，保留水线，脸应可读，允许前景虚化。请用 M5 提供摄影方案、焦点要求与 H3 Ref2VA 字段交接。照片只提供身份，视频只提供摄影路径；当前没附实际媒体。不要给我编造真实观测或测量参数。请完成自然语言方案并交代可检查的结果范围，不必构造机读JSON。

## 复核附录 C：本轮追加读取记录与原文完整性

首次读取清单保持原状；本附录的新增读取单列如下，不能倒填为首次试用时已经读过。

| 文件 | 本轮实际读取范围 | 用途与边界 |
| --- | --- | --- |
| `/workspace/scratch/22d2b2ce8467/H3-h3-prompt-journal/docs/h3skill/h3-camera-visibility/references/h3-ref-official.txt` | 第 155–207 行；收到复核要求后实际读取，并在本次落盘前再次读取该区间，均完整返回、无截断 | 核对四个可见内容关系词及“按已定义角色判定”的约束；没有因此声称完整读过全文件 |
| `/workspace/scratch/22d2b2ce8467/m5-forward-use.md` | 复核时读取原报告的末尾 66 行、末尾 14 行、第 105–180 行及末尾 20 行；落盘前再次读取末尾 20 行 | 检查原错误所在交接内容、首次读取日志及结尾状态；这是自有输出复核，不是新增外部证据 |
| 同一 `m5-forward-use.md` | 追加程序以字节读取整份首次文件，并在追加后比较原始前缀 | 只用于原文完整性校验和计算校验值，不把字节读取称作新增文献语义审读 |

本轮没有重读主 Agent 后来更新的映射／movement／contract 文档，没有读取案例 evidence/index、schema、脚本或实际媒体，也没有访问其他历史资料。未运行生成模型或完成运行时合同测试；这些项目不在本附录的核验范围。

追加前原报告的字节数：25424。追加前原报告的 SHA-256：`a46cac2c9ec8f022ad3ed6d6131a169603ba9937de2cfa21ee8c675753086c38`。追加程序验证保存后的文件以前述原始字节串逐字节开头；首次输出保留，全部修订仅在其后追加。
