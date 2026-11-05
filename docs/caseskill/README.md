# H3 案例技能集

**为全部 29 个案例各创建一个独立 Agent Skill，覆盖 97 个原始文本文件及 29 份逐案评估。** 每个技能包含专属流程、失败修复、来源快照、H3 官方规则转写、模板和可运行的计划检查器。

**版本：1.0.0；创建日期：2026-11-04（America/Los_Angeles）。** 10 月 15 案、9 月 6 案、8 月 8 案全部覆盖。

**关键词**：Agent Skills；MiniMax-H3；逐案技能；参考权限；动作链；时序；状态交接；可复核交付。

## 目录导航

- [一案一技能目录](#一案一技能目录)
- [每个技能包含什么](#每个技能包含什么)
- [如何使用](#如何使用)
- [验证与范围](#验证与范围)
- [官方规范基线](_standards/README.md)
- [案例映射目录](catalog.json) · [全部原始文本清单](source-manifest.json) · [验证结果](_validation/validation-report.md)

## 一案一技能目录

目录名去除案例日期前缀并规范为 `h3-...`；映射保存在 catalog.json。动作链、动态运镜、物理机位等库型案例同样独立成技能，默认可交组件。

### 2026-10

| 原案例 | 独立技能入口 | 文本数 |
|---|---|---:|
| [2026-10-advanced-camera-combinations](../../case-studies/2026-10-advanced-camera-combinations) | [H3 动作触发的物理运镜组合编排](h3-advanced-camera-combinations/SKILL.md) | 2 |
| [2026-10-baifeng-mengchen-classical-dance-six-segment](../../case-studies/2026-10-baifeng-mengchen-classical-dance-six-segment) | [白凤蒙尘：动链反推与双生成匹配剪辑](h3-baifeng-mengchen-classical-dance-six-segment/SKILL.md) | 2 |
| [2026-10-camera-movement-discipline-library](../../case-studies/2026-10-camera-movement-discipline-library) | [H3 运镜纪律选择与冲突裁决](h3-camera-movement-discipline-library/SKILL.md) | 2 |
| [2026-10-classical-wuxia-dance-13-segment](../../case-studies/2026-10-classical-wuxia-dance-13-segment) | [音乐事件驱动的古典武侠舞分段编排](h3-classical-wuxia-dance-13-segment/SKILL.md) | 3 |
| [2026-10-dance-motion-chain-library](../../case-studies/2026-10-dance-motion-chain-library) | [舞蹈动链检索、时间容量与状态衔接编排](h3-dance-motion-chain-library/SKILL.md) | 2 |
| [2026-10-four-subject-formation-choreography](../../case-studies/2026-10-four-subject-formation-choreography) | [H3 四主体身份锚与队形状态接力](h3-four-subject-formation-choreography/SKILL.md) | 2 |
| [2026-10-h3-motion-transfer](../../case-studies/2026-10-h3-motion-transfer) | [H3 人物优先的多参考动作重建](h3-motion-transfer/SKILL.md) | 3 |
| [2026-10-identity-only-half-body-dance-six-segment](../../case-studies/2026-10-identity-only-half-body-dance-six-segment) | [双图分权半身舞：身份、首帧动作与镜头职责分离](h3-identity-only-half-body-dance-six-segment/SKILL.md) | 2 |
| [2026-10-kanzaki-beach-sword-dance-18-segment](../../case-studies/2026-10-kanzaki-beach-sword-dance-18-segment) | [以道具状态与单镜头组织长篇表演MV](h3-kanzaki-beach-sword-dance-18-segment/SKILL.md) | 3 |
| [2026-10-leg-lift-contact-cut-stocking-six-look](../../case-studies/2026-10-leg-lift-contact-cut-stocking-six-look) | [H3 触地事件驱动的服饰硬切](h3-leg-lift-contact-cut-stocking-six-look/SKILL.md) | 2 |
| [2026-10-physical-camera-position-library](../../case-studies/2026-10-physical-camera-position-library) | [物理摄影机机位：八要素编排与兼容检查](h3-physical-camera-position-library/SKILL.md) | 2 |
| [2026-10-sock-showcase-right-entry-three-shot](../../case-studies/2026-10-sock-showcase-right-entry-three-shot) | [H3 右入单状态展示与硬切装配](h3-sock-showcase-right-entry-three-shot/SKILL.md) | 2 |
| [2026-10-summer-pool-beach-waterline-mv-4-segment](../../case-studies/2026-10-summer-pool-beach-waterline-mv-4-segment) | [夏日人物MV：特殊机位与切镜事件分离](h3-summer-pool-beach-waterline-mv-4-segment/SKILL.md) | 2 |
| [2026-10-waterfront-solo-dance-two-segment](../../case-studies/2026-10-waterfront-solo-dance-two-segment) | [水岸独舞：单镜头取证与双段动作接力](h3-waterfront-solo-dance-two-segment/SKILL.md) | 2 |
| [2026-10-xiashan-veiled-solo-twelve-segment](../../case-studies/2026-10-xiashan-veiled-solo-twelve-segment) | [双图分权与面纱状态保护的多段独舞](h3-xiashan-veiled-solo-twelve-segment/SKILL.md) | 2 |

### 2026-09

| 原案例 | 独立技能入口 | 文本数 |
|---|---|---:|
| [2026-09-action-chain-sock-fan-comedy](../../case-studies/2026-09-action-chain-sock-fan-comedy) | [道具脱离、触镜与局部扇风的连续动作链](h3-action-chain-sock-fan-comedy/SKILL.md) | 4 |
| [2026-09-editorial-lamp-rhythm-fashion-ab](../../case-studies/2026-09-editorial-lamp-rhythm-fashion-ab) | [台灯五章音乐时尚片与受控A/B变体](h3-editorial-lamp-rhythm-fashion-ab/SKILL.md) | 6 |
| [2026-09-purple-veil-dance-seven-segment](../../case-studies/2026-09-purple-veil-dance-seven-segment) | [紫纱亭舞：主动力轮换、实物交接与服装显色](h3-purple-veil-dance-seven-segment/SKILL.md) | 2 |
| [2026-09-snap-lock-editorial-reveal](../../case-studies/2026-09-snap-lock-editorial-reveal) | [H3 音频事件驱动的快照与硬锁](h3-snap-lock-editorial-reveal/SKILL.md) | 4 |
| [2026-09-song-style-classical-dance-six-segment](../../case-studies/2026-09-song-style-classical-dance-six-segment) | [宋韵古典舞的双层节拍、差异化高光与连续交接](h3-song-style-classical-dance-six-segment/SKILL.md) | 4 |
| [2026-09-three-person-prank-freeze-gag-cos-swap](../../case-studies/2026-09-three-person-prank-freeze-gag-cos-swap) | [三人画外干扰、定格笑点与仅换皮复现](h3-three-person-prank-freeze-gag-cos-swap/SKILL.md) | 5 |

### 2026-08

| 原案例 | 独立技能入口 | 文本数 |
|---|---|---:|
| [2026-08-cinematic-character-reveal-two-part](../../case-studies/2026-08-cinematic-character-reveal-two-part) | [双段角色揭示：姿态索引、接缝资产与连续母带](h3-cinematic-character-reveal-two-part/SKILL.md) | 5 |
| [2026-08-dual-subject-speed-contrast](../../case-studies/2026-08-dual-subject-speed-contrast) | [双人异速：动作完成数、观察延迟与可见性](h3-dual-subject-speed-contrast/SKILL.md) | 4 |
| [2026-08-first-person-finger-controlled-dance](../../case-studies/2026-08-first-person-finger-controlled-dance) | [第一人称手势命令与舞者身体同拍响应](h3-first-person-finger-controlled-dance/SKILL.md) | 5 |
| [2026-08-furina-windsurfing-fashion-mv](../../case-studies/2026-08-furina-windsurfing-fashion-mv) | [H3 分层参考与帆板写真 MV 高潮编排](h3-furina-windsurfing-fashion-mv/SKILL.md) | 5 |
| [2026-08-single-subject-three-pose](../../case-studies/2026-08-single-subject-three-pose) | [单人三姿态锚点与近身连续飞行摄影](h3-single-subject-three-pose/SKILL.md) | 5 |
| [2026-08-sticker-character-kitchen-comedy](../../case-studies/2026-08-sticker-character-kitchen-comedy) | [贴纸厨房喜剧：媒介边界、道具归属与四镜因果链](h3-sticker-character-kitchen-comedy/SKILL.md) | 5 |
| [2026-08-three-person-orbital-long-take](../../case-studies/2026-08-three-person-orbital-long-take) | [三人物遮挡接力、独立环绕与近距离群像长镜头](h3-three-person-orbital-long-take/SKILL.md) | 5 |
| [2026-08-water-obstacle-variety-show](../../case-studies/2026-08-water-obstacle-variety-show) | [剧情锚点驱动的水上闯关与失败反转](h3-water-obstacle-variety-show/SKILL.md) | 5 |

## 每个技能包含什么

| 文件/目录 | 用途 |
|---|---|
| `SKILL.md` | 合规 YAML 元数据、触发描述、输入契约、案例专属步骤、验收规则和资源路由。 |
| `agents/openai.yaml` | 展示名、简短说明和调用示例，可选客户端配置。 |
| `references/case-method.md` | 冲突裁决、失败修复、迁移示例和逐条证据。 |
| `references/h3-official.md` | 本次新编的离线 H3 操作规则，固定来源链接在文末。 |
| `references/source-*.md/json`、`provenance.json` | 本案例全部文本与评估的原样快照、哈希和读取索引；不含媒体。 |
| `assets/output-template.md`、`plan-template.json`、`case-contract.json` | 可复制填写的工作表、结构化编排清单和本案例检查项。 |
| `scripts/audit_plan.py` | Python 标准库脚本，核对时间覆盖、引用、容量、关键帧和输出字段。 |
| `evals/evals.json` | 正向、边界和反例任务；是否实际执行另见验证报告。 |
| `LICENSE.txt` | 保留案例原仓库许可，支持单目录复制时的归属。 |

每个技能不依赖其他 case skill 的相对路径。共同规则和检查器在各目录保留完整副本；不需要复制整个集合才能读取单个技能。原始案例的图片、视频和音频仍由具体任务提供。

## 如何使用

让支持 Agent Skills 的客户端发现或注册所需技能目录，或明确要求 agent 阅读该目录的 SKILL.md。仓库交付不等于已经安装到当前聊天客户端。不要将 caseskill 聚合目录本身当成一个技能。

例如，给 agent 的任务可以写成：

> 使用 docs/caseskill/h3-waterfront-solo-dance-two-segment/SKILL.md。根据我提供的实际素材，把独舞拆成连续生成片段，给出全局/局部拍点、状态接力、H3 提示词和检查记录。

技能会先读取当前案例方法，按需要查官方规则和原始文本，复制 assets 中的模板到任务输出目录，生成逐切片提示词。运行检查时：

```bash
python3 docs/caseskill/h3-waterfront-solo-dance-two-segment/scripts/audit_plan.py /absolute/task/plan.json --strict --check-files
```

计划 JSON 是本项目自有编排清单，不是 MiniMax API 请求体。完整生成端提示词保存为独立英文正文；中文解释、案例来源、版本裁决和审核记录保存在正文之外。基础模式与 Ref2VA 采用不同字段，不能混用。

## 验证与范围

- 已编写 106 个代表性任务，覆盖正常、边界与反例；场景定义与实际试用结果分开记录。
- 官方 skills-ref 格式校验、逐案覆盖/来源哈希/资源路径验证和检查器回归结果见 `_validation/`。
- 标准 H3 单次生成按官方 4–15 秒/24 FPS 规划；长案例保存创作段结构并再拆生成切片，不能将长片整个当成一次标准请求。
- 不将作者自述、旧文档数字、未连接的节点保存值或人工填入的 pass 当成模型实测。
- 本次完成技能创建、静态验证与有记录的离线试用；没有实际运行 H3，没有查看/测量原案例媒体，也没有给出生成成功率。

复现批量验证：

```bash
python3 -m pip install ./docs/caseskill/_standards/skills-ref
python3 docs/caseskill/_validation/validate_collection.py
python3 -m unittest discover -s docs/caseskill/_validation -p 'test_*.py' -v
```

官方验证器的依赖只用于集合维护；使用任一技能自带的计划检查器仅需 Python 3.10+，不需要 API 密钥或模型部署。

## 固定来源

- 案例及评估快照：`91a33376e9ae84d0b9b3a2c1a7f6991d5b9e358e`。
- Agent Skills 官方标准：`83021e2be457a9b6679148719c1f6074f0ad975e`。
- MiniMax-H3 官方指南：`199b7d0e1fd95e7b3eafa8c15eca692534142427`。
- 许可归属、来源文件哈希、标准原文与各案例规则证据分别保存在 `_standards`、`source-manifest.json` 和各技能 references 中。
