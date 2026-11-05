# M5 摄影机、景别、构图与焦点：开发与验收记录

**技能：** `h3-camera-visibility` v0.1.0。  
**合同：** `1.0.0`。  
**日期：** 2026-11-05（沿用项目 America/Los_Angeles 日期口径；执行记录使用 UTC）。  
**开发基线：** `skillplan-v0.1.2-608813b`。  
**仓库读取基线：** `aa4ae291fa8afa0a62fa96ffde26ca25a8db8352`。

## 核心摘要

本轮交付第五核心模块 M5，包含四个公开、可独立调用的子模块：M5.1 观察机位与光轴、M5.2 取景构图与可见性、M5.3 焦点与景深策略、M5.4 摄影机运动与触发。运行包位于 [h3-camera-visibility/](h3-camera-visibility/)，按观看任务输出带来源、版本、未知项和明确所有权的 `CameraPlan`。

交付包括技能入口、四份专业规则、公共合同与路由登记、Python 标准库合同工具、独立／组合设计样例、案例证据和来源索引，以及五种 MiniMax H3 输入模式与四类参考 Label 的编排／审计映射。测试、前向试用、发布检查和本记录位于运行包之外。

这是文字编排／审计和确定性合同实现。真实可见性、完整光学可行性、空间碰撞、实际时序和 H3 生成质量分别保留验证边界；本轮没有运行 H3，也没有将案例作者的效果报告当作实测结果。第 1—4 模块、冻结开发方案和案例原文继续保留其既有字节。

## 关键结论

1. **职责按专业决定划分。** 机位、取景、焦点、路径各有唯一子模块写入区；M5 父级只接受符合原请求与版本的提案，不在聚合时另写竞争值。
2. **独立调用实际可用。** 兼容外部输入可以直接满足合同；M5.2 不要求先运行 M1—M4 或 M5.1。必要信息未知时明确限制结论，不能伪装为不适用。
3. **案例规则保留适用范围。** 不把手持、低机位、固定人数、禁角度数字、锁焦或 1:1 同步提升为所有任务的强制要求。
4. **共享时间线允许不同响应。** 提前到位、同相响应、滞后追随和固定观察分别表达；摄影事件与人物动作独立编号，精确时间交 M7。
5. **内部计划与 H3 字段分开。** `CameraPlan` 不是新增的模型顶层参数。基础四模式的摄影正文进入 `integrated_multimodal_description`，Ref2VA 进入 `detailed_description` 等六字段的对应职责；最终编译归 M11。
6. **通过范围可追溯。** 合同通过、Agent 语义审阅、官方目录格式检查和真实媒体结果分别记录，不用一个总通过掩盖尚未检查的层次。

**关键词：** M5、CameraPlan、机位、光轴、构图、动作可见性、焦点、景深、摄影事件、参考 Label、独立调用、原子接受。

## 目录

1. 任务要求与对应交付
2. 四个公开子模块及合同
3. 领域方法与案例边界
4. H3 五模式、字段和 Label
5. 目录与官方创建规范
6. 四项架构原则的实现
7. 工具、样例与调用
8. 实际验证和修订
9. 发布、保护范围与后续边界
10. 集中来源

## 1. 任务要求与对应交付

| 用户要求 | 本轮实现 | 可复核位置 |
| --- | --- | --- |
| 根据开发方案完成第 5 核心模块 | 固定 M5 四子模块与 `CameraPlan`，不改冻结规划 | [技能入口](h3-camera-visibility/SKILL.md)、[模块登记](h3-camera-visibility/references/module-registry.json) |
| 结合 case 案例集合，保持内容边界 | 摄影领域规则使用仓库案例；事实、作者报告、设计与未知分别标识 | [案例证据](h3-camera-visibility/references/case-evidence.md)、[案例索引](h3-camera-visibility/references/case-index.json) |
| 遵守 Anthropic Skills 创建规范 | `SKILL.md` 元数据及按需资源；运行包无兄弟目录依赖；执行官方基本验证器 | [来源和许可](h3-camera-visibility/references/provenance-and-license.md)、[交付检查](validation/m5/delivery-checks.json) |
| 明确 H3 输入模式、模块／Label | 五模式、两套字段结构、四类参考 Label 逐项列明 | [H3 映射](h3-camera-visibility/references/h3-label-mapping.md) |
| 提供对应的编排和审计要求 | 四域专业规则、参考范围、未知处理、逐镜表达和修复责任表 | [审计交接](h3-camera-visibility/references/audit-and-handoff.md) |
| 高内聚、低耦合、模块化、路由信息 | 五个节点登记全部 18 条原则，公开最少输入、权限、依赖、返回和变更影响 | [模块登记](h3-camera-visibility/references/module-registry.json)、[合同指南](h3-camera-visibility/references/contract-guide.md) |
| 记录提交到对应文件夹 | 本报告、独立测试、前向试用、发布清单与核验工具均位于 `docs/h3skill/` | [README](README.md)、[发布清单](release-manifest-m5.json) |

冻结方案的 M5 职责见 `01-core-framework.md` 的 M5 小节；四子模块与独立 M5.2 用例见 `06-modularity-routing-principles.md` 第 211、224—241 行。该方案明确要求补充光学样本与测试才能宣称完整视场／景深覆盖，本轮据此交付清晰目标、光学缺口和检查边界。[S1]

## 2. 四个公开子模块及合同

| 入口 | 必需 `inputs` 键 | 唯一提案分区 | 核心专业结果 |
| --- | --- | --- | --- |
| M5 | `camera_brief` | 父接受，不作跨区子提案 | 路由、组合检查、版本与问题记录 |
| M5.1 | `viewpoint_brief` | `/content/viewpoints` | 观看任务、位置、高度、距离、光轴、机身滚转 |
| M5.2 | `framing_brief`、`viewpoint_context` | `/content/framing` | 景别、视场、画面关系、关键动作与接触可见条件 |
| M5.3 | `focus_brief`、`framing_context` | `/content/focus` | 清晰目标、焦点保持／变化、清晰范围、光学依据缺口 |
| M5.4 | `movement_brief`、`viewpoint_context` | `/content/movements` | 独立摄影事件、起终位置、主路径、位姿变化、触发和响应 |

最少输入是公开数据要求，不等于强制调用某个上游生产者。上下文可以是对应分区、带来源版本的兼容外部对象，或带具体理由的 `unknown`。四个子模块均以 `M5Proposal` 返回 M5；父级使用实际原请求数组进行接受。

四个分区统一为 `items` 映射，稳定 ID 与镜头 ID、动作 ID、H3 参考 Label、说话者编号分别管理。公共对象为 `M5Request`、`M5Proposal`、`M5ProposalBatch`、`M5State`。准确字段、必填性和枚举见 [contracts.json](h3-camera-visibility/references/contracts.json)。

父接受检查身份、基版本、原请求与上下文保真、分区所有权、来源冲突、跨镜引用、只读投影及开放阻断问题。整个批次通过才返回一个新版本草稿；输入文件不被覆盖。精确重复提案返回幂等结果，复用同一提案 ID 却改变内容会被拒绝；技术重试与创作修订分开。

专业 `Fact.state=known` 表示有来源的要求或计划已被明确，不表示画面经过测量。`visibility_assessment` 和 `focus_assessment` 在 1.0.0 中只允许 `unverified`。内部引用可以检查存在性与镜头归属；外部自由载荷不被重新解释成隐藏协议，外部内容真实性保留未验证。

## 3. 领域方法与案例边界

### 3.1 本轮使用的证据

| 编号 | 案例 | 提取内容 | 保留的限制 |
| --- | --- | --- | --- |
| C01 | `physical-camera-position-library` | 从空间位置、距离、高度、光轴解释视角 | 作者效果报告不是普遍保证；普通镜头不必填满所有参数 |
| C02 | `camera-movement-discipline-library` | 主运动、路径、触发与停止，区分相机和人物事件 | 文本含不同同步表述；手持、1:1 和风格限制只在对应任务中成立 |
| C03 | `advanced-camera-combinations` | 复合运动的主路径、阶段转换与遮挡中路径连续 | 局部标题／描述冲突须裁决；`SHOT` 阶段名不能自动解释为真实切镜 |
| C04 | `four-subject-formation-choreography` | 多人层次、身体信息和交叉阶段可读性 | 主体身份不等于固定画面槽位，不据此设通用人数上限 |
| C05 | `leg-lift-contact-cut-stocking-six-look` | 接触事件、关键可见点与动作阶段 | 具体服装、切换和接触模板不是所有作品的固定方案 |
| C06 | `summer-pool-beach-waterline-mv-4-segment` | 水线观察、连续路径、面部清晰与柔化前景 | 相机可由观看任务驱动；保留剧情动作和相机独立性 |
| C07 | `identity-only-half-body-dance-six-segment` | 身份参考权限与当前机位／构图分开 | 身份照片不能自动成为首帧或全属性摄影约束 |

详细原文路径、行号、事实类别、相反条件和阅读范围统一见 [case-evidence.md](h3-camera-visibility/references/case-evidence.md)。整个案例文本目录的清点和逐文件哈希由 [case-index.json](h3-camera-visibility/references/case-index.json) 记录；文件被登记不等于已语义全文阅读，原视频、图像和音频也不因文本索引而成为已观察媒体。[S2]

本轮清点 **29 个案例、98 个文本文件**，含案例目录内 97 个文本及根目录共享词汇索引；其中 **11 个全文阅读、3 个按相关段落阅读、84 个仅清点**。98 个文件的 Git blob、SHA-256、字节数、行数及当前工作副本均重新核对，没有继承前模块的全文阅读声明。

### 3.2 本轮形成的专业规则

机位说明以观看任务为起点，区分世界方向、身体左右和画面左右；相机高度、光轴俯仰、绕光轴滚转和人物倾倒分别表达。取景说明指出要看清的主体、部位或关系，并绑定动作的必要阶段，例如接触建立、保持、释放和结果，而非只写“清楚”。

焦点计划先明确何种信息需要清晰，再说明保持或改变焦点的原因和条件。人物前后移动、多个景层、接触点与面部竞争，均可以记录为待协调需求；没有尺度与光学资料时不编造焦距、光圈或景深数值。

摄影运动说明主路径、起终条件、沿途光轴、转换理由及停止或稳定条件。提前、同相、滞后、固定是可选的任务关系；`none` 可表示没有动作相位关系的观看任务运动。固定摄影机不冻结人物，绕行后回到原点也不因端点相同而成为静止。

这些规则中的合同字段、所有权、未知对象与离线样例属于本轮 D 类实现设计；它们不被写成原案例已经提供的工程系统。领域规则不使用范围外摄影教程来补成未经验证的通用光学配方。

## 4. H3 五模式、字段和 Label

### 4.1 五种输入模式

| 模式 | 官方结构 | M5 编排／审计 |
| --- | --- | --- |
| T2VA | 基础三字段 | 从文字观看任务形成摄影过程；不虚构参考资产 |
| I2VA | 首帧对齐首行＋基础三字段 | 对齐实际首帧的构图和观察关系，再描述后续变化 |
| FL2VA | 首尾帧对齐首行＋基础三字段 | 在首尾观察条件之间组织可说明的路径；按任务决定单镜或明确多镜 |
| L2VA | 尾帧对齐首行＋基础三字段 | 从合理前态收敛到尾帧，不把尾帧当作首帧 |
| Ref2VA | 六字段 | 按真实参考用途说明保留／改变及逐镜摄影过程 |

基础三字段依次为 `integrated_multimodal_description`、`overall_soundscape`、`non_diegetic_music`。Ref2VA 六字段依次为 `subject_definitions`、`summary`、`retention_analysis`、`detailed_description`、`overall_soundscape`、`non_diegetic_music`。摄影主正文分别使用前者第一字段与后者第四字段，声音字段仍由声音职责提供内容。[S3]

M5 没有新增 H3 顶层 `camera_movement`、`camera_position`、`focus_plan` 或 `appearance_description`。Ref2VA 使用英语描述，仅对白／歌词和画内文字按官方规则保留原语言。镜头标记、实际素材顺序和最终编译归 M11，切镜归 M9，绝对时间和偏移归 M7。[S3]

### 4.2 四类参考 Label

| Label | 与 M5 的关系 | 审计要求 |
| --- | --- | --- |
| `<Subject N>` | 目标视频中复用或修改的可见内容，可包含主体、动作、风格等 | 不当作源文件编号；当前镜头仍须描述实际位置与行动 |
| `<Picture N>` | 实际帧、关键帧或分镜构图锚点 | 身份来源图不自动增加独立 Picture 条目，也不自动决定机位 |
| `<Video N>` | 编辑、续接，或整段摄影／剪辑／节奏结构 | 仅参考运镜不自动变成源视频编辑；继承属性须限定 |
| `<Audio N>` | 已启用的复制或参考音频信号 | 源视频带声音不等于已启用音频；音乐不自动要求每拍运镜 |

四个 Label 在各字段中保持同一含义；`[Shot N]` 与 `(Sx)` 分别是镜头和发声标记，不是 CameraEvent ID。完整逐字段、逐 Label、逐模式编排与审计清单，以及官方 B／R 行号，见 [H3 映射](h3-camera-visibility/references/h3-label-mapping.md)。[S3]

## 5. 目录与官方创建规范

| 路径 | 用途 | 是否为独立运行包内容 |
| --- | --- | --- |
| `h3-camera-visibility/SKILL.md` | 名称、触发描述、任务工作流、按需资源入口 | 是，必需入口 |
| `h3-camera-visibility/references/` | 四专业规则、合同、路由、证据、协议原文和归属 | 是 |
| `h3-camera-visibility/scripts/m5_contract.py` | 确定性合同与引用检查 | 是 |
| `h3-camera-visibility/assets/` | 独立／组合请求、提案、状态设计样例 | 是 |
| `tests/m5/` | 行为测试、执行报告与日志 | 否，开发验收 |
| `validation/m5/` | 官方标准核验、独立复制运行、Agent 试用、审阅 | 否，开发验收 |
| `20261105-development-m5-v001.md` | 本开发记录 | 否 |
| `release-manifest-m5.json`、`tools/verify_m5_release.py` | 发布清单与复核 | 否 |

入口仅使用 `name` 与 `description` 元数据，名称与目录一致，满足小写字母、数字和连字符要求。正文 91 行，低于创建指南建议的 500 行；这是指南的推荐控制值，不伪称所有技能的硬性协议限制。引用资源从入口单跳可达，长说明有导航；案例索引和官方原文按需读取。[S4]

目录由技能创建器初始化后按项目运行边界整理。可选的 `agents/openai.yaml` 未作为本包依赖。包外开发说明不被误标成 Anthropic 全面禁止 README 的规则；这里采用的目录取舍用于保持运行资源集中。标准快照和许可保留原来源。

本轮重新读取并核对 Anthropic、Agent Skills 和 MiniMax 的固定来源及对应文件。实际来源版本与 blob／SHA-256 见 [source-verification.json](validation/m5/standards/source-verification.json)。官方基本验证器检查元数据等基础项；引用可达性、运行依赖、合同行为和冻结范围由项目的独立检查补充，不能仅凭格式验证宣称技能行为全部正确。[S4]

## 6. 四项架构原则的实现

| 规则组 | 本轮具体实现 | 验证方式 |
| --- | --- | --- |
| HC-01—03：高内聚 | 四域按专业决定划分；父级聚合不另作摄影决定；不把术语拆成无独立结果的小模块 | 入口、四专业文档、五节点登记及前向试用审阅 |
| LC-01—05：低耦合 | 最少公开输入、外部来源可替代、只读上下文保真、未知与依赖显式、领域与 H3 编译分离 | 四组独立接受、来源／上下文异常、只读冲突、影响路径测试 |
| MD-01—04：模块化 | 身份与版本、单一分区写入、父原子接受、公开资源和标准库运行边界 | 越权／冲突拒绝、幂等／非删除／版本测试、隔离目录执行 |
| RT-01—06：路由信息 | 显式目标、输入映射、返回点、失败责任、按需资源、操作效果、实际调用轨迹与失效传播 | route／check／accept／impact、实际请求绑定、执行日志和依赖影响测试 |

M5、M5.1、M5.2、M5.3、M5.4 各自登记全部 18 条规范。登记完整性检查只证明条目存在；行为测试和语义试用用于检查相应实现，不将登记本身等同执行证据。[S1]

## 7. 工具、样例与调用

从仓库根使用：

```bash
cd docs/h3skill/h3-camera-visibility
python scripts/m5_contract.py route assets/request-m5-2.json
python scripts/m5_contract.py check assets/proposal-m5-2.json --request assets/request-m5-2.json
python scripts/m5_contract.py accept assets/state-empty.json assets/proposal-batch.json --requests assets/requests.json
```

`route` 返回入口、最少输入与相关资源，不执行专业 Agent。`check` 检查单个公共对象或批次各提案；组合后的一致性由 `accept` 对照父状态核对。`accept` 结果中的 `.state` 是新草稿；后续需提取该对象使用。`impact BEFORE AFTER` 根据消费者登记的 `read_paths` 标记失效，无法发现未登记的语义依赖。

脚本仅用 Python 3.10+ 标准库，不联网、不改输入文件、不调用 H3。JSON 解析拒绝重复键、非有限数和溢出浮点。正常退出码 0 表示本地合同检查通过，1 表示明确阻断，2 表示解析、参数或执行错误；`validation.overall` 在非失败时保持 `unverified`。

四组 `request-standalone-m5-N.json`／`proposal-standalone-m5-N.json` 展示单独调用，`request-minimal-m5-2.json` 展示显式未知。组合样例包括道具交接、多人全身覆盖、固定接触观察、滞后揭示和按任务启动的水线运动，均为 D 类设计夹具，不是案例转录或真实生成结果。

完整复核命令：

```bash
python docs/h3skill/tests/m5/run_tests.py
python docs/h3skill/validation/m5/run_delivery_checks.py
python docs/h3skill/tools/verify_m5_release.py
```

## 8. 实际验证和修订

### 8.1 分层记录

合同测试实际执行 **38 项，38 项通过，0 failures、0 errors、0 skips**。测试结果保存本次被测脚本、schema、路由、合同指南、夹具与测试代码的 SHA-256，以便区分当前执行证据和后续文件修改。

| 检查层次 | 实际记录 | 能证明的范围 |
| --- | --- | --- |
| 行为测试 | [test-results.json](tests/m5/test-results.json)、[完整日志](tests/m5/unittest-output.txt) | 所列确定性合同与 CLI 场景 |
| 官方基本格式与独立复制 | [delivery-checks.json](validation/m5/delivery-checks.json)、[日志目录](validation/m5/logs/) | 基本目录／元数据、标准库依赖、无兄弟目录时可执行 |
| Agent 前向试用 | [forward-use.md](validation/m5/forward-use.md) | 两个任务的实际资源读取、专业文字输出及局限 |
| 独立合同审阅 | [independent-review.md](validation/m5/independent-review.md) | 定向静态检查、已关闭缺口及本人未执行的范围 |
| 主审阅 | [review.md](validation/m5/review.md) | 原请求覆盖、领域边界、协议映射及已知缺口 |
| 发布复核 | [release-check.json](validation/m5/release-check.json) | 来源哈希、冻结文件、旧包、授权路径与发布清单 |

### 8.2 已处理的具体问题

合同脚本复核发现，异常 `accept` 批次若是数组或标量，记录操作身份时可能在生成受控报告前访问错误类型。该路径以结构检查和类型防护处理，并增加回归任务，避免把不合法输入变成未捕获的运行异常。

父路由登记原先沿用子请求的“输入原样成为提案上下文”措辞，可能误导调用者直接将父 `camera_brief` 当作所有子模块原请求。现已明确父路由只返回四个入口；调用方按各自最少输入建立真实子请求，保持来源与基版本，再供父接受核对。

消费者枚举最初只列出 M5 以外的核心模块，无法登记本包内构图、焦点或运动结果对机位的依赖。现已允许四个 M5 子模块作为消费者，并用实际接受机位修订的任务验证：读取该机位的子结果变为 `stale`，只读取未变构图的结果保持 `current`，原状态不被修改。依赖仍由显式 `read_paths` 声明，不推断未登记的依赖。

前向试用的水线任务首次将“只使用视频的摄影路径”直接写为 `attribute_transfer`。对照官方 Ref2VA 第 165—168、207 行，这个词要求把特征转移到另一可辨识目标主体，不能仅以“只借一类属性”为理由。映射说明现已补齐四种视觉关系词的定义和摄影反例；首次输出保留，修订另附。是否完整保留或改变路径，应只在该 Video 已定义的摄影角色内判断；尚未取得媒体时仍是待绑定的计划关系。

文档与实际 schema 同步了四分区记录、响应策略、外部引用检查限度和独立夹具名称。对 `Fact.value` 的自由业务载荷保持不透明；不同自然语言写法不因字面不等被错误升级为机位移动，固定观察的确定性检查使用公开的位姿变化枚举，端点语义由 Agent 审阅。

### 8.3 验证边界

本轮前向试用用于检查技能说明能否引导 Agent 完成受限任务，保留原始输出和读取记录。没有进行 Claude 宿主自动触发率／有无技能 A/B 基准，也没有测量普遍创作质量、运行成本或真实生成成功率。

两项任务均形成实际输出；其中水线任务的关系词首次有偏差，定向补读官方原文后完成追加修订。首次 25,424 字节及其 SHA-256 被保留并核验，不把修订后的结果伪装为首次全对。独立合同审阅未发现其已检查范围内仍未关闭的阻断问题；它没有独立重跑行为测试，也没有逐项审计全部 schema，具体覆盖如实列在记录中。

G0 的输入与依赖、G1 的专业计划、G2 的编译和运行契约只验证本轮记录中的局部范围；本地合同通过不代表三个关卡整体通过。G3／G4 需要真实媒体，本轮均未执行。官方协议原文与字段映射不等于已经实现 M11，也不等于已经验证某个推理后端的全部能力。

## 9. 发布、保护范围与后续边界

本轮新增 M5 运行包、`tests/m5/`、`validation/m5/`、本报告、M5 发布核验工具与清单，并更新 `docs/h3skill/README.md` 的模块入口。保护范围包含全部 M1—M4 运行包、原案例、九份冻结文件及冻结控制记录；实际检查以源哈希和基线 Git blob 为依据。

`release-manifest-m5.json` 固定交付文件的字节数、SHA-256 和 Git blob SHA。清单不对自己求哈希；最终 `release-check.json` 也排除在该清单自引用之外，两者由 Git 提交固定。旧模块的 README 哈希和发布报告继续保留历史含义，不重写为本轮结果。

后续若要把焦点／景深规划推进为更完整的光学验证，需要在内容边界允许的范围内新增具体样本、参数、计算或媒体观察证据；若要验证 H3 实际效果，需要真实输入、运行及观察流程。本轮不借此修改冻结规划，也不将 M6—M12 标为已实现。

## 10. 集中来源

- **[S1] 冻结方案：** [固定开发方案目录](https://github.com/Nuos/H3-h3-prompt-journal/tree/608813b6e51531ac47f860bc384a454a504fe9ff/docs/skillplan)，重点为 `01-core-framework.md`、`05-workflow-routing.md`、`06-modularity-routing-principles.md`；控制记录见仓库 `docs/skillplan/baseline-lock.json`。
- **[S2] 领域边界：** [固定案例目录](https://github.com/Nuos/H3-h3-prompt-journal/tree/aa4ae291fa8afa0a62fa96ffde26ca25a8db8352/case-studies)；逐条证据、来源性质与本轮阅读范围见 [case-evidence.md](h3-camera-visibility/references/case-evidence.md) 和 [case-index.json](h3-camera-visibility/references/case-index.json)。
- **[S3] H3 协议：** [基础四模式](https://github.com/MiniMax-AI/MiniMax-H3/blob/199b7d0e1fd95e7b3eafa8c15eca692534142427/skills/h3-prompt-writing/references/base-en.txt)、[Ref2VA](https://github.com/MiniMax-AI/MiniMax-H3/blob/199b7d0e1fd95e7b3eafa8c15eca692534142427/skills/h3-prompt-writing/references/ref-en.txt)；离线原文、归属与哈希见 [h3-protocol-source.json](h3-camera-visibility/references/h3-protocol-source.json)。
- **[S4] 技能创建：** [Anthropic 创建指南](https://github.com/anthropics/skills/blob/ca45fc496a3436251f191354091d557da31c15b5/skills/skill-creator/SKILL.md)、[Anthropic 仓库](https://github.com/anthropics/skills/tree/ca45fc496a3436251f191354091d557da31c15b5)、[其规范入口所指 Agent Skills 规范](https://github.com/agentskills/agentskills/blob/83021e2be457a9b6679148719c1f6074f0ad975e/docs/specification.mdx)；本轮来源核对见 [标准记录](validation/m5/standards/source-verification.json)。
- **实现来源：** [前四模块固定基线](https://github.com/Nuos/H3-h3-prompt-journal/tree/aa4ae291fa8afa0a62fa96ffde26ca25a8db8352/docs/h3skill)；M5 合同工具复用本仓库 MIT 通用机制，领域合同独立，运行时不导入兄弟包。
