# Case 012 简评：台灯节奏时尚片 A/B 双版

## 核心结论

**可封装“共享时间骨架＋受控变体”专项原型，但须先修正版本路由。** 两组正文提供灯光、音乐、动作与镜头的协同范例；实际文件内容与文件名相反，且镜头约束的差异超出 README 宣称的范围。词汇增补已指出命名问题，尚未同步修正文档与执行入口。[S1–S6]

- 案例目录：`case-studies/2026-09-editorial-lamp-rhythm-fashion-ab`
- 评估范围：全部 **6 个文本文件**；未查看图片、音视频，未运行 H3。
- 源提交：`5056f46e123aef52c7aac9d51a03ce7a5dae53c2`
- 评估日期：2026-11-03（America/Los_Angeles）
- 方法论等级：**M2**；skill 就绪等级：**S2**；建议定位：**专项子技能候选**。

## 1. 模块构成

| 功能模块 | 内容与协作关系 |
|---|---|
| 参考与服装层 | 单图管理成年人物、房间、台灯及不透明舞蹈安全裤等固定资产。[S2][S4] |
| 音乐与灯态 | 自建 124 BPM、4/4 配乐；五章灯态为 ON→OFF→ON→OFF→ON。[S1][S2][S4] |
| 身体及相机 | 十个 moment，采用发起→行进→重音→刹停→释放；离散机位响应动作。[S2][S4] |
| 变体层 | 可爱版侧步、轻弹、后折腿跳跃；暗奢版划腿、手臂释放、甩裙末段。[S2–S5] |
| 文档与校读 | README 的机制总结、双语全文及词汇扩展共同构成使用资料。[S1–S6] |

## 2. 多维简评

**模块关系较明确。** 先确定音乐网格，再让灯态、动作重音与机位响应共用时间线。31 拍按 124 BPM 计算正好 15 秒；五个灯态包含初始 ON，之后实际发生四次切换。该结构可迁移到其他节奏道具。[S1]

**参数化潜力高，但 A/B 尚未受控。** 两版可共享灯点和 moment 边界，音乐风格、身体动作与结尾 Hero 可成为变体参数。实际“暗奢”文件包含 A major 可爱跳跃，“可爱”文件包含 E minor 暗奢甩裙；对应中文文件也跟随实际正文，而非文件名。[S2–S6]

**镜头差异需单独审计。** README 声称骨架逐字相同、ROLL 分布完全一致；暗奢实际正文在 Moment 2 使用 Dutch-angle movement、Moment 4 明确反向 roll，Moment 6、9 允许选用 roll，与可爱版的限制不同。不能把这组材料当作只改变三个层面的严格对照实验。[S1][S2][S4]

**音乐精度是计划值。** 内部生成配乐没有外部音轨或 onset 验证记录。灯点可由公式复算，不代表实际生成自动对齐；1.300、2.600 秒等 moment 边界也不是 124 BPM 的整拍位置。文本中的 bullet-time feel 同时排除字面慢动作，需转为可观察的节奏和材质要求。[S1][S2][S4]

## 3. skill 化判断与最小落地步骤

建议把公共时间表、灯态和资产限制存成共享配置，逐版记录音乐、动作、镜头规则差异；由一份变体清单生成双语提示词。检查文件名—调式—Hero 对应、roll 分布与灯态覆盖，再以实际音频及视频回读验收同步。现有两套长提示词尚不足以证明跨版本稳定。

## 4. 主要缺口与优先级

1. **P0｜修正版本入口。** 建立准确的文件到变体映射，并同步 README 和中文说明；当前依文件名选择会得到相反的动作与配乐。[S1，11–12、34–50 行；S6，5–12、174 行]
2. **P1｜提取真实公共配置。** 用差异清单核对每个 moment，尤其是 2、4、6、9 的 roll；取消未经核实的“逐字相同”表述。[S2，435、556、670、844 行；S4，381、521、627、784 行]
3. **P1｜验证实际同步。** 标明整拍、细分拍及自由过渡边界，记录配乐生成与灯点对齐结果；补充多次生成记录后再评价成功率。[S1，52–79、99、111 行]

## 5. 全部文本依据

以下六份文本均已全文阅读；行号列出主要证据位置。文件名按仓库原样列出。

- [S1] [README.md](https://github.com/Nuos/H3-h3-prompt-journal/blob/5056f46e123aef52c7aac9d51a03ce7a5dae53c2/case-studies/2026-09-editorial-lamp-rhythm-fashion-ab/README.md)：全文 1–115 行；版本声明 3–50，音乐与灯点 52–79，相机纪律 81–87，复用总结 95–102。
- [S2] [p83-dark-luxury-skirt-throw.txt](https://github.com/Nuos/H3-h3-prompt-journal/blob/5056f46e123aef52c7aac9d51a03ce7a5dae53c2/case-studies/2026-09-editorial-lamp-rhythm-fashion-ab/p83-dark-luxury-skirt-throw.txt)：全文 1–1306 行；实际为可爱版，112–125 行含 NEW CUTE / A major，267–279 为 roll 限制，791–866 起为跳跃蓄力与 Hero。
- [S3] [p83-dark-luxury-skirt-throw.zh-CN.txt](https://github.com/Nuos/H3-h3-prompt-journal/blob/5056f46e123aef52c7aac9d51a03ce7a5dae53c2/case-studies/2026-09-editorial-lamp-rhythm-fashion-ab/p83-dark-luxury-skirt-throw.zh-CN.txt)：全文 1–370 行；对应实际可爱版全文译解，未修复文件名语义。
- [S4] [p84-cute-backfolded-jump.txt](https://github.com/Nuos/H3-h3-prompt-journal/blob/5056f46e123aef52c7aac9d51a03ce7a5dae53c2/case-studies/2026-09-editorial-lamp-rhythm-fashion-ab/p84-cute-backfolded-jump.txt)：全文 1–1234 行；实际为暗奢版，104–110 行含 dark / E minor，381、521、627、784 为额外 roll 约束，743–808 起为甩裙蓄力与 Hero。
- [S5] [p84-cute-backfolded-jump.zh-CN.txt](https://github.com/Nuos/H3-h3-prompt-journal/blob/5056f46e123aef52c7aac9d51a03ce7a5dae53c2/case-studies/2026-09-editorial-lamp-rhythm-fashion-ab/p84-cute-backfolded-jump.zh-CN.txt)：全文 1–355 行；对应实际暗奢版全文译解。
- [S6] [vocabulary-expanded.zh-CN.md](https://github.com/Nuos/H3-h3-prompt-journal/blob/5056f46e123aef52c7aac9d51a03ce7a5dae53c2/case-studies/2026-09-editorial-lamp-rhythm-fashion-ab/vocabulary-expanded.zh-CN.md)：全文 1–176 行；5–12、174 行明确提示文件名与实际内容相反，其他章节解释音乐、动作、机位与服装层术语。
