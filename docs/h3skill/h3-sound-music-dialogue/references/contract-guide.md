# M6 运行合同与公开字段

版本：合同 `1.0.0`；技能 `0.1.0`。运行器仅依赖 Python 3.10+ 标准库；无网络、无写文件副作用。输入文件由调用方保存，`accept` 通过 JSON 的 `.state` 返回新草稿。

## 公共协议

沿用前五模块的父子建议模式：`M6Request → M6Proposal → M6ProposalBatch → M6State`。请求含 work_id、base_version、request_id、target、sources、inputs；建议含 proposal_id、module_id、source_request_id、原样 sources/context、changes、issues、resolutions。`sources` 是证据登记表；`content.sources` 是声源实体分区，二者不可混淆。父对象 `SoundPlan` 的唯一写入者为 M6；各子模块仅建议替换自己的一个分区。

| 子模块 | 分区 / 稳定条目 ID | 最少输入 |
|---|---|---|
| M6.1 | sources / sound_source_id | source_brief |
| M6.2 | vocal_events / vocal_event_id | vocal_brief、source_context |
| M6.3 | music / music_id | music_brief、reference_context |
| M6.4 | effects / effect_id | effects_brief、action_context |

父模块 `M6` 只要求 sound_brief。缺少最少字段会拒绝；字段为 `{state: "unknown", reason: "…"}` 是合法显式未知，保留未验证状态。借用其他模块的 `ExternalContext` 须保存 owner、source_id、source_version、values；也可用本包内完整类型分区作为声源/声音事件/音乐/音效上下文。无上游运行器或仓库时仍可独立检查。

## 领域字段与边界

- `SoundSource`：shot_id、applies_to_shots、source_kind、subject_ref、voice_ref、description、voice_requirement、permission。voice/subject 引用保持已有来源；本模块没有最终 Sx 字段。BGM 歌词语义来源为 bgm_audio，不发明人物。
- `VocalEvent`：source_ref、event_kind、original_text、approved_text、rewrite_approval、language、delivery、continuity、lip_sync、audio_origin、track_ref、timing_owner。`inputs.vocal_texts` 以 vocal_event_id 登记原文，检查逐字符及标点一致；批准文本单独保存；改写须 rewrite_approval.value=true、有批准证据，并与原请求 inputs.approved_vocal_texts 对应文本完全一致。language 保留原语种依据，continuity 明确语义起止、跨镜持续条件或未知，不形成权威排时；ref-en 的格式转化交 M11。lyric_semantic 必须 lip_sync=not_required，且若已知声源必须为 bgm_audio。
- `Music`：shot_id、applies_to_shots、use_strategy、audio_selection、whole_source、additional_audio、removals_or_replacements、music_requirement、beat_plan、timing_owner=M7、edit_owner=M9。audio_selection 包含当前 AudioAsset 与 window，AudioAsset 保留 asset_id、asset_version、source_id、source_version、available、duration_seconds；可在 inputs.audio_assets 登记以核对保真。当前资产完整使用且无其他音频才符合 fully_copy；当前资产是预先裁好的文件亦可完整复用。当前登记的是长母轨但仅取窗口，或增加/删除/替换任意声音，均须 partially_copy。
- `BeatPlan`：kind=none/planned/measured、bpm、beat_times_seconds、measurement_asset、source_refs。planned 是候选；measured 必须有 available=true 的对应资产以及 media_observation 证据，单有 BPM 不足以声称实测拍点。时间权威仍是 M7；检查器不读取或测量音频。
- 无配乐与全片静音的字段归属：M6.3 的 `Music.use_strategy=none` 只说明没有配乐；M6.4 的 `Effect.event_kind=whole_track_silence` 才表达明确全片静音，交父 M6 做跨分区互斥检查。
- `Effect`：source_ref、action_ref、event_kind、description、spatial_relation、continuity、audio_origin、track_ref、explicit_silence。动作声音须绑定动作或显式未知；within_registered_audio 须关联复用音轨或显式未知。无音乐不会推导全片静音；whole_track_silence 必须来自原请求 `whole_track_silence` 的明确 user_requirement，并与其他声音互斥。

`SoundSource` 与 `Music` 的 shot_id 是首次声明镜头，applies_to_shots 显式列出所有适用镜头（包含声明镜头）。source_ref/track_ref 可在该范围内跨镜复用同一稳定 ID；越出范围拒绝。ExternalRef.shot_id 表示本次引用适用镜头，不是源历史声明镜头。其他镜头声音事件仍保持自己的 shot_id。

所有领域对象拒绝未声明属性；未定义的最终时间表、编辑操作、Label 编号因此无法写入 M6 分区。`Fact.value`、`ExternalContext.values`、`Projection.value` 是只读证据载荷而非可执行领域字段。缺失真实语义、音频观测与生成质量证据一直保持 unverified，合同通过不等于媒体效果通过。

对白、旁白、唱词和音轨词句提示缺少文字时，`original_text`／`approved_text` 使用明确 `unknown`，不能以 `not_applicable` 隐去应该存在但尚未取得的词句。非语言发声可以有理由地标为无文字。`known` 的其他自由证据载荷不等于脚本已判定其全部自然语言含义。

## 四个命令

```sh
python scripts/m6_contract.py route assets/request-m6-3.json
python scripts/m6_contract.py check assets/proposal-m6-3.json --request assets/request-m6-3.json
python scripts/m6_contract.py accept assets/state-empty.json assets/proposal-batch.json --requests assets/requests.json
python scripts/m6_contract.py impact before-state.json after-state.json
```

`check` 接受请求、建议、建议批次或状态；单建议不传原请求仅可进行结构检查，输出 original_request_missing。`accept` 强制提供真实请求数组，逐个验证请求、建议与证据保真；全部成功才返回新状态。任意失败不返回可接受状态、不改输入、不写文件。退出码：0 本地合同通过（总体仍 unverified），1 合同拒绝，2 输入/IO/解析错误。重复键与非有限 JSON 数字拒绝。

## 版本、幂等与依赖

一批最多写入每个子分区一次。base_version 必须等于父版本；已有 ID 不可通过分区替换删除；已有证据 ID 不可改绑。回执记录规范 JSON 的 SHA-256、原请求 ID、模块 ID、接受版本。完全相同重试返回相同状态；同 ID 变更内容、混合已接受与新建议、未提供原请求均拒绝。只读 typed context / JSON Pointer 投影在最终候选状态再次验证，避免子建议相互覆盖读入前提。

consumer 登记 module_id、result_version、source_state_version、read_paths、status。impact 比较真正变化的 /content、/sources、/issues、/display 路径，只把与已声明 read_paths 相交的消费者标 stale；元数据变化不使所有下游失效。未声明依赖无法由本地脚本推断。开放 blocking issue 必须由所属子模块给出带证据的 resolution 后才能接受。

## 验证范围

contracts.json 使用有限 JSON Schema 词汇：$ref、oneOf、anyOf、type、const、enum、minLength、pattern、minimum、minProperties、required、propertyNames、properties、additionalProperties、minItems、uniqueItems、items。脚本实现这一全集；它不是任意第三方 Schema 解释器。assets 是明确标记的合成设计夹具；测试与可携带性实测记录保存在技能包外。
