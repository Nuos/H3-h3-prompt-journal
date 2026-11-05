# H3 人物优先的多参考动作重建：方法与修复

## 导航

1. 方法来源与适用范围
2. 条件分支与冲突处理
3. 失败表现与修复
4. 迁移示例
5. 规则证据

## 方法来源与适用范围

把人物/世界锚、非外观运动提取、目标音频重定时和工作流预检组成可复用流程；将自然语言编排顺序、真实节点运行和生成后视觉验收明确分开。

本方法由原案例文本、逐案评估和 H3 官方协议共同整理。原案经验、评估发现与本次补齐的数据/检查接口须分别表述；案例作者的成功报告不等于本次实测。原稿快照保留原貌，冲突由本文件及技能入口裁决。

- 共同audit_plan.py只能检查规划结构与时序，不替代ComfyUI节点执行、依赖安装或视频逐帧检查。
- 保存的活动加速分支由161=true选择，实际beta4+ExtendIntermediateSigmas参数与旧“6步”说明需要运行时核验；不要把显示缓存的sigma张量当实时结果。
- 工作流含Comfy core、KJNodes、VideoHelperSuite、rgthree、easy showAnything及若干无cnr_id节点；完整环境依赖未齐。
- 本设计修复的是编排和预检规范，没有改动或运行源workflow。

## 条件分支与冲突处理

| 条件 | 执行动作 | 案例/评估依据 |
|---|---|---|
| 只有动作参考，没有人物/世界图 | 保存动作提取草案并将身份/世界输入标missing；不使用源视频的人物或背景自动填补。 | case-studies/2026-10-h3-motion-transfer/prompt.md:30-44,47-115 |
| 任务只需要提示词，不需要运行ComfyUI | 交付参考职责、动作/时序映射和提示词，工作流检查只作可选工程交接，不下载权重或声称已经生成。 | docs/casereview/2026-10-h3-motion-transfer.md:12,27,29,37（职责工程化） |
| 用户要12秒迁移而案例写9秒上限 | 查询当前运行模式的实际时长能力；有明确支持再规划12秒，否则按能力和乐句拆段。不凭案例文字一刀切认定不支持。 | docs/casereview/2026-10-h3-motion-transfer.md:5,44 |
| 工作流元数据下载文件名与widget选中模型不同 | 以实际加载目标及存在性为预检对象，分别记录声明来源与选择值，缺文件时停止运行准备但继续提示词设计。 | case-studies/2026-10-h3-motion-transfer/h3-motion-transfer-workflow.json（节点128、170）；docs/casereview/2026-10-h3-motion-transfer.md:44 |
| 续段加噪后不知道裁剪哪个范围 | 先写清接续帧和裁剪时间，再将帧数转换为秒核对音频；没有依据不机械裁22或26帧。 | case-studies/2026-10-h3-motion-transfer/h3-motion-transfer-workflow.json（节点194、208、211-213）；docs/casereview/2026-10-h3-motion-transfer.md:43 |

## 失败表现与修复

| 失败表现 | 修复步骤 | 依据 |
|---|---|---|
| 输出保留参考视频脸、服装或原室内背景 | 重新建立参考权限和人物/世界锚，在动作表中只保留机制，删除源外观描述后重试；需要生成结果才能确认修复。 | case-studies/2026-10-h3-motion-transfer/prompt.md:47-115,395-413 |
| 开场构图跟着图1而丢失源动作的朝向 | 保留图1身份/世界，单独重建Video1首帧距离、身体朝向和承重关系。 | case-studies/2026-10-h3-motion-transfer/prompt.md:138-206,279-304 |
| 报告9秒124帧或1344×768但连线值不同 | 沿132→131→136和115→136追踪，说明226帧/24fps及选择器参数；实际节点运行输出另行核验。 | case-studies/2026-10-h3-motion-transfer/h3-motion-transfer-workflow.json（节点115、131、132、136）；docs/casereview/2026-10-h3-motion-transfer.md:41 |
| 音乐未生效或续段声画偏移 | 检查155启用状态与端口角色，统一213与212的裁剪时间；不得只在提示词里重复音频权威。 | case-studies/2026-10-h3-motion-transfer/h3-motion-transfer-workflow.json（节点155、136、191、212、213）；docs/casereview/2026-10-h3-motion-transfer.md:42-43 |

## 迁移示例

**任务**

把一段8秒室内转身—点步—抬腿动作迁移给图1湖边平台上的新人物，用另一个8秒音频；已提供目标强调点2秒和5秒，尚未运行工作流。

**预期处理示例**

图1拥有新人物、衣着、湖边平台和光线；视频只提供开场全身机位、转身与腿部承重机制；音频2秒/5秒作为用户给定目标点而非本技能实测。先核对平台足部支撑与侧向空间：0–2秒由源开场支撑脚发起转身，2秒肩线到位；2–5秒通过点步完成重心转移，5秒抬腿达到计划峰值；5–8秒收腿、落脚并延续手臂恢复。相机在图1世界按视频固定全身关系观察，不带入室内墙面。提交前标音频端口和模型配置待核验，生成后八项检查全部未执行；不承诺8秒必然成功，也不把原workflow的9秒设置当作本次参数。

示例是编排示范；其中任务给定参数和演算不代表当前已经读取了对应媒体，也不代表一次 H3 推理已完成。完整生成端交付仍需按输出模板选择正确字段和真实素材绑定。

## 规则证据

以下行号对应本技能来源索引中的固定快照；`review` 指 `source-review.md`。工程补齐项以其所解决的原文/评估缺口为依据，不伪称上游已实现该检查。

| 规则 | 原文或评估位置 |
|---|---|
| MTR01 | case-studies/2026-10-h3-motion-transfer/prompt.md:26-44,47-115,366-413 |
| MTR02 | case-studies/2026-10-h3-motion-transfer/prompt.md:118-186,279-304 |
| MTR03 | case-studies/2026-10-h3-motion-transfer/prompt.md:245-276；docs/casereview/2026-10-h3-motion-transfer.md:27 |
| MTR04 | case-studies/2026-10-h3-motion-transfer/prompt.md:416-467 |
| MTR05 | case-studies/2026-10-h3-motion-transfer/README.md:40-50；docs/casereview/2026-10-h3-motion-transfer.md:5,41-44 |
| MTR06 | case-studies/2026-10-h3-motion-transfer/h3-motion-transfer-workflow.json:1050-1422；docs/casereview/2026-10-h3-motion-transfer.md:41 |
| MTR07 | case-studies/2026-10-h3-motion-transfer/h3-motion-transfer-workflow.json:683-745（节点155）；节点136、191；docs/casereview/2026-10-h3-motion-transfer.md:42 |
| MTR08 | case-studies/2026-10-h3-motion-transfer/h3-motion-transfer-workflow.json:3052-3456（节点194、211-213）；docs/casereview/2026-10-h3-motion-transfer.md:43 |
| MTR09 | case-studies/2026-10-h3-motion-transfer/prompt.md:487-537；docs/casereview/2026-10-h3-motion-transfer.md:31,37 |
| MTR10 | case-studies/2026-10-h3-motion-transfer/prompt.md:446-484；docs/casereview/2026-10-h3-motion-transfer.md:33 |

| 规则 | 文件与行号 | 支持内容 |
|---|---|---|
| MTR01 | case-studies/2026-10-h3-motion-transfer/prompt.md：26-44;47-115;366-413 | 图像/视频/音频信息域分离及源人物不作为输出第二主体。 |
| MTR02 | case-studies/2026-10-h3-motion-transfer/prompt.md：118-186;279-304 | 首帧允许继承的几何和肢体机制范围。 |
| MTR03 | docs/casereview/2026-10-h3-motion-transfer.md：27 | 提示词顺序不等同实际多阶段模型执行。 |
| MTR04 | case-studies/2026-10-h3-motion-transfer/prompt.md：416-467 | 目标音频重定时及连续机制链。 |
| MTR05 | docs/casereview/2026-10-h3-motion-transfer.md：5;41-44 | 9秒属于案例配置经验，不能推出通用能力上限。 |
| MTR06 | case-studies/2026-10-h3-motion-transfer/h3-motion-transfer-workflow.json：1050-1422;3703-3745 | 131/132长度表达式与115分辨率连线取代旧widget值。 |
| MTR07 | case-studies/2026-10-h3-motion-transfer/h3-motion-transfer-workflow.json：683-745;1124-1358;2114-2364 | 155 mode=4及136/191音频端口；节点ID是可靠定位，具体范围含相邻节点。 |
| MTR08 | docs/casereview/2026-10-h3-motion-transfer.md：43 | 22帧说明、26帧视频裁剪和1秒音频裁剪并不一致。 |
| MTR09 | case-studies/2026-10-h3-motion-transfer/prompt.md：487-537 | 原文八项问答是视觉目标；需拆生成前后才能真实验收。 |
| MTR10 | docs/casereview/2026-10-h3-motion-transfer.md：33 | 新场景支撑与通路可能使原动作不可迁移。 |
