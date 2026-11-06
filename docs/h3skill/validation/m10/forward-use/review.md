# M10 独立上下文使用：最终审阅

## 结论与实际范围

两个文字任务均完成，书店任务的三条 CLI 实际执行且退出码均为 0；最终产物符合下列十项任务审阅条件。这里的“完成”指本次文字方案和结构化接受，不是实际图像、音轨、视频或 H3 输出验收。

执行 Agent 不继承开发会话，只得到本次完整技能包、两份原始夏日案例文本和任务。期间因长输出截断、补读和迟未落盘，根 Agent 进行了进度提醒及暂停／继续，并提示使用本包已提供的最小 M10.3 夹具。初稿完成后，根 Agent 要求澄清两处协议措辞。因此本次是**受监督的独立上下文使用**，不标为无人干预首轮成功或宿主自动触发测试。

## 任务与产物

| 任务 | 实际交付 | 可复查结果 |
| --- | --- | --- |
| 原始四段夏日 MV 的视觉整理 | [case-look-plan.md](output/case-look-plan.md) | 四职责的视觉方案、作用域、冲突、责任回传与五模式／参考角色交接；保留 55 秒、四任务、八镜头、四切点和源音轨窗口 |
| 新设计雨夜书店的独立 M10.3 | [bookshop-result.md](output/bookshop-result.md) | 拒绝身份图调色越权和重染发色；保留冷中性、局部暖窗框与棕木；真实图像和色值未知 |
| 最小合同与真实运行 | [execution.json](output/execution.json) | 输入、完整命令、原样 stdout／stderr、时间和退出码；只接受 ColorPlan 到 version 1 的 draft |
| 实际读取与来源 | [read-log.json](output/read-log.json)、[source-manifest.json](source-manifest.json) | 明确全文、部分、补读及未读资源；原始案例复制字节与固定仓库基线一致 |

## 十项任务审阅

| 条件 | 最终评价 | 依据及限制 |
| --- | --- | --- |
| FU01 入口与相关资源使用 | 符合本次范围 | 实读入口、合同指南、H3 映射、最小夹具及原始输入；未读四份专业指南，不能据此宣称所有资源的独立激活均验证 |
| FU02 保留原案结构并给出四职责 | 符合 | 时长、切点、动作、镜头及音轨窗口作为锁定项；四个专业段落分别处理视觉要求 |
| FU03 区分原文、候选与未知 | 符合 | 明确没有实际媒体；源文要求不写成已观察到的效果；未知色值、灯光参数保留 |
| FU04 视觉关系与权限审计 | 符合 | 分开局部暖光／全局调色、湿发／身份；识别跨段服装授权矛盾，交 M2；可见性回 M5、状态回 M8 |
| FU05 五模式及参考角色 | 澄清后符合 | 最终 T2VA 风格明确位于第一镜内；身份来源图只在 Subject 定义中引用，不为此增设独立 Picture 定义；其他模式保留真实首尾帧角色 |
| FU06 独立最小 M10.3 | 符合 | 请求只有必需 brief 与 scope_context；没有强制运行其他模块或虚构全片继承 |
| FU07 待审句的属性越权 | 符合 | 拒绝把身份许可扩成调色来源，拒绝由整体冷调推出改发色；未伪造许可 |
| FU08 实际 CLI 与局部接受 | 符合 | route/check/accept 三个退出码均 0；录制 stdout 与逐项文件一致；部分 LookPlan 仅有 ColorPlan |
| FU09 完成边界与设计标注 | 符合 | 成功状态为 passed_with_unverified；状态 draft；新增调色表达标记为本任务设计样本 |
| FU10 技能文件保持一致 | 符合 | 42 文件试用快照、试用后的包及最终发布包 SHA-256 一致；没有因试用改动技能代码或规则 |

这些条件评价任务产物，不能合计为模型质量通过率。源声明是否真实仍由证据负责，脚本不能替代自然语言、像素或媒体审阅。

## 初稿问题与修订保留

[first-draft-case-look-plan.md](first-draft-case-look-plan.md) 保留修订前原稿。初稿有两处不够精确：T2VA 写为“正文前部”，未明确第一镜内；Picture 写为一般图片／分镜，未充分说明仅作身份来源时不单列 Picture 条目。

根 Agent 在看到真实产物后指出上述歧义，要求依据本包资源核对。Agent 补读 H3 映射、复读入口，修订模式表及 Label 段，并记录读取范围。最终内容与固定官方协议相符；这属于使用产物澄清，未改变技能包，不报告为无需反馈的首稿通过。

## 命令结果与复现

三条原始命令在隔离试用目录执行，详见 execution.json。route 返回 ready=true 但 invocation_status=not_invoked；check 与 accept 返回 passed_with_unverified；接受版本为 1，内容只有 ColorPlan。空状态、请求和提案均与记录中的输入值相同。保存的接受状态与原始 stdout 内 state 相同。核对明细见 [artifact-verification.json](artifact-verification.json)。

在本仓库根可用以下命令复现同一输入的合同结果：

```bash
python -B docs/h3skill/h3-visual-look/scripts/m10_contract.py route docs/h3skill/validation/m10/forward-use/output/bookshop-request.json
python -B docs/h3skill/h3-visual-look/scripts/m10_contract.py check docs/h3skill/validation/m10/forward-use/output/bookshop-proposal.json --request docs/h3skill/validation/m10/forward-use/output/bookshop-request.json
python -B docs/h3skill/h3-visual-look/scripts/m10_contract.py accept docs/h3skill/validation/m10/forward-use/output/bookshop-state-empty.json docs/h3skill/validation/m10/forward-use/output/bookshop-proposal.json --requests docs/h3skill/validation/m10/forward-use/output/bookshop-request.json
```

本轮没有运行其他模块、H3、图像查看或音视频处理；没有验证真实保色、光照、材质、身份保真、无闪烁或无漂移。两项任务也不证明全部影视剧类型、全部模块组合或所有自由文本都已覆盖。
