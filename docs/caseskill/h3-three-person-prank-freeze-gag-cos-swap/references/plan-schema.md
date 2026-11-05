# 编排清单与静态检查

本文定义本技能自有的 `plan.json`，**不是 MiniMax API 请求体**。它把素材、时间、人工检查结论与实际提示词对应起来，防止“表里写了”被误认为“运行时已传入”。复制 `assets/plan-template.json` 到当前任务输出目录，再按实际任务填写。

## 字段

| 字段 | 填写规则 |
|---|---|
| `schema_version`、`case_id` | 保留模板值，确保调用的是本案例技能。 |
| `delivery_kind` | `component` 仅交动作/运镜组件；`prompts` 交完整 H3 提示词。组件不伪装为可提交生成请求。 |
| `status` | 草案为 `draft`；资料、语义审核与交付内容齐备后改为 `ready`。 |
| `assembly` | 连续成片用 `sequential`；独立 A/B 或候选用 `variants`；仅组件用 `component`。 |
| `runtime` | 默认 `official-2026-10-28`，即标准 4–15 秒/24 FPS。确有运行时证据才选择 `verified-custom`，填写 `evidence`、`min_duration_s`、`max_duration_s`、`fps`。自定义配置仅改变已核实的输出时长和 FPS，不自动解除输入容量。 |
| `fps` | 目标生成帧率，与 runtime 一致。可另填 `edit_fps` 表示后期交付帧率；这不改变模型的原生生成帧率。 |
| `assets` | 每项有唯一 `id`、`kind`（image/video/audio）、`locator`、`status`（provided/missing）、职责列表 `roles`。视频/音频填写实际 `duration_s`；视频轨需参与声音时显式 `audio_enabled: true`。 |
| `references` | 每项填写精确 `label`、`asset_ids` 和 `role`。可选 `standalone` 用于标识是否独立定义；来源图片标签仍登记，即便只出现在 Subject 定义内部。 |
| `segments` | 每次生成一项：唯一 `id`、`mode`、`duration_s`（生成时长）、`global_start_s`（裁后片段在最终成片中的起点）、`reference_labels`、`shots`、相对路径 `prompt_file`。关键帧模式还需 `first_frame_asset_id` 或 `last_frame_asset_id`。 |
| `edit_window_s` | 可选的片段内 `[起点,终点]`，必须位于生成时长内。原生最短4秒的输出可裁成3秒展示片，不能把3秒当成已支持的直接生成时长。 |
| `edit_holds` | 可选的后期追加定格列表。每项有 `at_s`（裁后、尚未追加任何定格时的局部位置）、正值 `duration_s` 和 `evidence`（所取保留帧及理由）。位置递增并落在裁后片长内；原生生成动作中的暂停不放在此表，以免重复计时。 |
| `edit_duration_s` | 可选的最终使用时长，须等于裁切窗长度加上全部后期追加定格时长；不裁切时以完整生成时长为底数。 |
| `shots` | 每段从 1 重新编号；每镜 `id`、`start_s`、`end_s`、`action`、`camera`、`sound`。时间连续覆盖该段，正文切点与表一致。 |
| `handoffs` | 连续多段时，每对相邻段有一项 `from`、`to`、`type`（continuous/hard_cut）、`evidence`、`audio_strategy`。在 evidence 写具体人物、持物、运动、相机和衣物状态，以及真实传递资产。 |
| `case_checks` | 使用 `assets/case-contract.json` 中的全部检查 ID；填写 pass/fail/unverified/not_applicable 及证据。not_applicable 需要适用性解释。 |
| `unresolved` | 尚未解决的版本、素材、时间、动作与空间问题；不得为了通过检查而直接清空。 |

`frame_count` 是可选的生成帧数，若填写则核对与时长/FPS 的量化误差。`entry_state`、`exit_state`、音频全局偏移、节拍事件、动作单元和案例专用状态表可作为额外字段保留；脚本不会假装已经理解这些自然语言状态。

镜头局部时间始终覆盖完整生成时长。连续成片的 `global_start_s` 按裁后片长推进；如连续三段各生成4秒、只取各段0–3秒，则全局起点为0、3、6，最终成片9秒。交接证据应检查实际裁切窗两端，而非被丢弃的原始末帧。30 FPS 交付可以是后期时间线规格；未经证实不能把它写成 H3 原生生成能力。

若喜剧片先生成14秒，取其中13.5秒并在三个已选帧各追加0.5秒定格，则 `duration_s=14`、`edit_window_s=[0,13.5]`、三个 `edit_holds`、`edit_duration_s=15`。全局时间按15秒推进。这里核对的是编辑计划的算术，不意味着脚本已经实际合成视频。

## 最小形状示例

以下是结构示例，`case_id`、检查项、资产和描述必须用当前任务实值替换。此示例不是合格交付。

```json
{
  "schema_version": "1.0",
  "case_id": "从本技能模板保留",
  "delivery_kind": "prompts",
  "status": "draft",
  "assembly": "sequential",
  "runtime": {"profile": "official-2026-10-28"},
  "fps": 24,
  "assets": [],
  "references": [],
  "segments": [{
    "id": "SEG01", "mode": "T2VA", "duration_s": 8,
    "global_start_s": 0, "reference_labels": [],
    "prompt_file": "prompts/SEG01.txt",
    "shots": [{"id": 1, "start_s": 0, "end_s": 8,
      "action": "完整可观察动作", "camera": "具体机位与路径", "sound": "实际声音或明确静音"}]
  }],
  "handoffs": [],
  "case_checks": [],
  "unresolved": ["尚未填写本案例人工检查项"]
}
```

## 执行

从技能根目录运行；计划和提示词保存在任务目录，勿覆盖技能模板。

```bash
python3 scripts/audit_plan.py /absolute/task/plan.json
python3 scripts/audit_plan.py /absolute/task/plan.json --strict --check-files
```

依赖仅为 Python 3.10+ 标准库，无 API 密钥、联网或模型依赖。`--check-files` 只读 plan 目录内列明的提示词文件，禁止越界路径；它不会打开媒体、执行源工作流或运行 H3。返回 0 为所选静态检查无错误，1 为结构/一致性错误，2 为文件或 JSON 输入错误。草案运行允许 warnings；严格交付不得有未解决项或未审人工检查。

检查范围包括：案例 ID、必需人工检查记录、资产/引用绑定、输出时间线、关键帧资产、每次生成的输入容量、相邻段交接记录、提示词官方字段顺序和切点。**通过仅说明结构与声明一致**，不证明动作物理成立、人物一致、嘴型同步、拍点准确、真实资产已经被生成器读取或最终画面合格。

## 人工验收职责

先按 case-contract 中的逐条规则审实际输出，填写具体的镜头/状态/素材证据，再运行脚本。不要让脚本生成 `pass` 作为自己的证据。看不到媒体时，在交付中明确视觉、音频与推理验收尚未实施；不得声称已经听过、测过或生成过。发生矛盾时按 `references/case-method.md` 的修复分支修改，再重跑受影响的检查。
