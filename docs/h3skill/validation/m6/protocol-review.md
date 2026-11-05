# M6 协议与职责边界独立审阅

审阅日期：2026-11-05。审阅者：独立协议复核 Agent。方式：只读对照目标文档、随包官方原文和冻结 M6 方案；仅本记录写入包外验证目录。

## 范围与结论

全文审阅 `h3-sound-music-dialogue/SKILL.md`、`references/h3-label-mapping.md`、`references/audit-and-handoff.md`、`references/provenance-and-license.md`，对照官方固定提交 `199b7d0e1fd95e7b3eafa8c15eca692534142427` 的 base/ref 原文，以及冻结方案 `01-core-framework.md` 的 M6 和 `06-modularity-routing-principles.md` 的 M6.1—M6.4。

M6 四分区、M7 排时／M9 编辑／M11 标签编译边界，以及完整复制与新增声音互斥、歌词 cue 不自动产生人物口型、未知证据不冒充媒体观察，均与所查来源相符。发现以下两项需修订的文档问题；本次不把其他 Agent 正在补齐的运行文件视为缺陷，也不宣告整个包完成验收。

## 发现与必要修正

### PR-M6-01：精确原文行号误引

- 位置：`references/h3-label-mapping.md` 第 93、96、114 行。
- 事实：第 93 行把逐词逐标点保留规则引为 B128，该行实际为空行，规则在 B129；第 96 行引为 B144／R222，实际分别是画内文字标题／空行，跨切与截断规则在 B142／R221；第 114 行的 B158／B168 实际分别是代码围栏／案例标题，两个 `N/A` 规则在 B154／B162。
- 影响：映射文本的规则本身基本正确，但所声明的可复现精确定位不能直接支持相应结论。
- 必要修正：按实际随包原文改为 B129、B142／R221、B154／B162；同页第 112 行的声音分类依据宜由 B156—174 收紧为 B152—166，覆盖两个正式定义。不要改动官方原文来迁就现有引用。
- 状态：发现时待修订；本记录未代改运行包。

### PR-M6-02：完整参考 Label 的模式范围没有写明

- 位置：`SKILL.md` 第 75 行；`references/h3-label-mapping.md` 第 29 行及第 60—73 行。
- 事实：入口先列出五种模式，随后无条件要求核对／联用四类参考 Label，未显式区分基础模式与 Ref2VA。映射页的 T2VA 行仅说没有音频资产时不虚构 Audio 引用，仍可能被解读成有音频资产即可在基础正文加入完整参考标签。官方 R231 明确区分 T2VA 不使用完整参考 Label；B16—34 另外规定 I2VA／FL2VA／L2VA 各自的 Picture 对齐首行。
- 影响：单独执行入口的 Agent 可能把 Ref2VA 的 Subject／Video／Audio 引用语法扩展到基础四模式。
- 必要修正：在入口与映射页增加明确限定：四类完整参考关系、Audio 定义／保留分析和 Subject 与 Sx 联用按 Ref2VA 协议交 M11；基础四模式使用基础三字段及各自官方 Picture 对齐语法，不直接引入完整参考标签体系。若任务确需音频参考绑定，交 M11 判断适用模式，不由 M6 静默改模式。
- 状态：发现时待修订；该项是协议范围澄清，不改变 M6 内部 SoundPlan 的声音资产记录能力。

## 来源与可复现性

本次重新计算两份原文的 SHA-256、Git blob SHA 与行数，均与 `references/h3-protocol-source.json` 一致：base 为 222 行，SHA-256 `2cfebc096a6e08370f288d468d90b60f7f9bcb938f94bf090816e910e48e75fc`；ref 为 341 行，SHA-256 `1e574f356716ad55612247ffb7bbccbcdb484ad96599d63c7dca1af186b1fab7`。

| 被审阅文件 | 审阅时 SHA-256 |
| --- | --- |
| `SKILL.md` | `7494c20e3c6593b340ea811671247852cd5760ede2f424c5c4cd4ed6eed7bdc5` |
| `references/h3-label-mapping.md` | `03ec117ed521156595425f90f7f9a534303828a8b84883974365a909c6e89401` |
| `references/audit-and-handoff.md` | `70003f3fe39cf80bfb670540f53237ab631871a34c196109e218eb350ac4af34` |
| `references/provenance-and-license.md` | `3bb6178a33105db6d28fc52dc76c137e13a953a5e5fb760a7ec10e2702b207c4` |

官方依据：[基础模式原文](https://github.com/MiniMax-AI/MiniMax-H3/blob/199b7d0e1fd95e7b3eafa8c15eca692534142427/skills/h3-prompt-writing/references/base-en.txt)、[Ref2VA 原文](https://github.com/MiniMax-AI/MiniMax-H3/blob/199b7d0e1fd95e7b3eafa8c15eca692534142427/skills/h3-prompt-writing/references/ref-en.txt)。职责依据：[冻结核心框架](https://github.com/Nuos/H3-h3-prompt-journal/blob/608813b6e51531ac47f860bc384a454a504fe9ff/docs/skillplan/01-core-framework.md)、[冻结模块化方案](https://github.com/Nuos/H3-h3-prompt-journal/blob/608813b6e51531ac47f860bc384a454a504fe9ff/docs/skillplan/06-modularity-routing-principles.md)。

## 验证边界

本次只做文本协议和职责审阅及原文完整性核对；未执行 M6 运行脚本，未取得或听取真实音频，未观看生成视频，未做转写、口型、音色、节拍、混音、H3 推理或 G3／G4 真实媒体验证。许可部分仅核对归属和来源声明，没有作法律适用或部署许可结论。文档后续修改应按新版本复核，不将本记录的旧哈希误作为最终发布结果。

## 修复后复查追加记录

同日收到开发者修订后，重新读取两个改动文件并逐项对照原文，保留以上首次发现与旧哈希：

| 发现 | 实际修复与复查结果 | 状态 |
| --- | --- | --- |
| PR-M6-01 | 映射页当前第 95、98、116 行已分别使用 B129、B142／R221、B154／B162；第 114 行声音分类依据已改为 B152—165，覆盖 B154 与 B162 两项正式定义。核对相应原文内容相符。 | 已修复并复查 |
| PR-M6-02 | `SKILL.md` 第 75 行明确限定四类完整参考 Label 属于 Ref2VA；映射页第 37 行明确基础四模式不套入完整参考结构，并把音频参考与模式能力冲突交 M11 处理。保留共用说话者／对白标记，未把模式修订责任交给 M6。 | 已修复并复查 |

修复后 `SKILL.md` SHA-256 为 `ef8a9c61d9b70250e3cb57e16a1a04848dc8248ac245b1e072319f17d355735e`；`references/h3-label-mapping.md` 为 `40e88dcdc11f019b8f358bebd3454679fd9e4e47da407d191dfdbd5632830674`。另两份被审阅文件的哈希与首次记录一致。

本次四份文档范围内没有剩余的已识别协议或职责边界问题。该结论只关闭以上两项文字发现，不替代整个运行包、编译器、案例覆盖或真实媒体的独立验收；未做真实媒体验证的边界保持不变。

## 主线程后续补充复核

独立审阅后的映射页增加了“当前已预裁资产”和“长母轨的局部窗口”的区分。主线程于 2026-11-05T15:48:41.254500+00:00 全文读取最终映射页，对照随包 R92—100、R187—205，确认其参照对象仍是本次实际声明的音频资产；完整源信号作为完整最终音轨、存在额外声层时转为部分复制的官方边界未被放宽。该段明确标注项目的来源交接细化，不冒称逐字官方表述。

此次映射页 SHA-256 为 `c2d9717448db22bb9c8a1753d0f6c3ce8a48dcb1d0f85eab1838afdb936d75f2`。以上独立审阅哈希保留为其当时版本；这条追加记录属于主线程文字复核，不改称独立审阅者已审过后续字节，也不提供新的媒体验证。

## 最后一次字段归属说明修订

2026-11-05T15:52:25.903807+00:00，运行合同作者只读核对报告后指出，“生成或静音”容易混淆 M6.3 与 M6.4 的公开字段。主线程已统一入口、专业说明、映射、合同指南及登记中的文字：`Music.use_strategy=none` 表示无配乐；`Effect.event_kind=whole_track_silence` 表示明确全片静音，由父 M6 做互斥检查。运行逻辑与公开字段未变；21 项行为测试、14 次隔离调用及官方格式检查在该修订后重新执行并通过。

此项是本地合同职责说明的修订，未改变官方输入语法。最终被改动文档的身份如下，前面的旧版本记录保留其历史含义：

| 文件 | SHA-256 |
| --- | --- |
| `SKILL.md` | `08907980148921f708027eb8d0f3b4a0d89a7f4259712f5244f4399cb79ef158` |
| `references/h3-label-mapping.md` | `dd47d8fa00e186202eb04f8f4e005406f39d08f9d033d5971de211ec60d32f0f` |
| `references/music-and-audio-policy.md` | `d4efb01021a552808c12f30084fa5ae5c5ca04ba018cb6fc894ddca9688116c8` |
| `references/ambience-and-action-sounds.md` | `40917bbd1dc2c29e2fdd19b5781ca41d9670f71be3fe2de16d0cd8f6cf630c5c` |
| `references/contract-guide.md` | `78e4307bb74119f4d09f7db227085f5954d47c9586f3da882df4ef2d42ee9c59` |
| `references/module-registry.json` | `f7ee53579c181c91cb6e78df0182dd844726b0e63bb0ae9f1291e4143d554d23` |
