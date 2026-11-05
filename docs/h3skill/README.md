# H3 通用核心技能

**当前新增模块：** M4 `h3-action-performance` v0.1.0。

**模块合同：** M1、M2、M3、M4 各自为 `1.0.0`；不表示全部共享对象已冻结。

**更新日期：** 2026-11-05（America/Los_Angeles）。

**开发基线：** `skillplan-v0.1.2-608813b`；M4 本轮读取仓库 `545a99015cfa00a6f07ee05d1d0f21e09d89d46c`。

## 核心摘要

依据冻结的十二模块方案，已交付 **M1 作品意图与段落功能**、**M2 素材解析、资产绑定与参考权限**、**M3 场景空间、人物站位与交互调度**，本轮新增 **M4 人物表演、动作链与物理因果**。M4 包含表演事件与前提、动作机制与交互过程、结果与动作接续三个可独立调用的子模块，输出版本化 `ActionPlan`。各包可独立复制使用其声明的文字编排和离线合同检查能力。

领域方法限定为 `case-studies/` 文本，重点为 10 月案例。Anthropic 资料只规定技能结构与开发方式，MiniMax 官方资料只规定输入协议。完整视频逆向、H3 模型调用、物理求解和真实媒体质量均不是这四个包已实现的能力。

## 关键结论

1. M1 决定作品目标，M2 管理身份与参考权限，M3 建立空间条件，M4 定义动作如何发生；摄影、声音、绝对时间、权威状态和最终模型编译继续由各责任模块处理。
2. M4 及三个子模块采用公开最小合同，兼容的外部输入可替代上游执行；三个专业分区由 M4 父模块唯一接受。
3. 动作前提、机制与结果分别表达。事件关系检查不证明人体物理成立；计划出态不等于真实生成末态，状态变化请求不等于 M8 已接受。
4. 不设置统一人数、动作密度、禁走路或禁慢动作规则；案例中的剑鞘状态、接触切换和动作迁移均保留作用范围。
5. M1—M3 运行包、原案例及冻结方案保持原字节。开发报告、测试与审阅证据位于运行包外，旧报告保留历史含义。

**关键词：** M1、M2、M3、M4、表演事件、动作机制、物理因果、结果接续、H3 Label、独立调用、版本化提案。

## 目录导航

1. 模块入口
2. M4 动作计划与 H3 交接
3. M3 空间计划与 H3 交接
4. 既有 M2 与 H3 的对应
5. 调用与文件组织
6. 验证入口和完成边界
7. 基线与历史记录

## 1. 模块入口

| 模块 | 技能入口 | 子模块 | 当前实现 |
|---|---|---|---|
| M1 作品意图与段落功能 | [h3-work-intent/SKILL.md](h3-work-intent/SKILL.md) | M1.1 意图约束；M1.2 段落信息；M1.3 情绪母题 | 文字工作流、独立合同与确定性检查；本轮运行包未改 |
| M2 素材解析、资产绑定与参考权限 | [h3-asset-reference/SKILL.md](h3-asset-reference/SKILL.md) | M2.1 资产登记；M2.2 主体绑定；M2.3 属性权限 | 文字工作流、独立合同、冲突/版本/引用检查和交接 |
| M3 场景空间、人物站位与交互调度 | [h3-scene-blocking/SKILL.md](h3-scene-blocking/SKILL.md) | M3.1 空间拓扑；M3.2 站位路线；M3.3 互动遮挡 | 文字工作流、独立合同、图上可达／引用／版本检查、父接受和交接 |
| M4 人物表演、动作链与物理因果 | [h3-action-performance/SKILL.md](h3-action-performance/SKILL.md) | M4.1 事件前提；M4.2 动作机制；M4.3 结果接续 | 文字工作流、独立合同、事件依赖／条件／引用／版本检查、父接受和交接 |
| M5—M12 | 冻结方案中的后续职责 | 依已锁定职责推进 | 未因本轮交付而标为实现 |

### M2 的三个产物

| 子模块 | 输出对象 | 关键内容 |
|---|---|---|
| M2.1 | AssetRegistry | 来源与版本、媒体通道、可访问性、观察状态及缺项 |
| M2.2 | EntityRegistry | 稳定实体、源内定位、资产多对多绑定、授权依据 |
| M2.3 | ReferenceMap | 属性允许/禁止/未知、明确范围、来源竞争与显式裁决 |

三对象在 `M2State.content` 中分别为 `asset_registry`、`entity_registry`、`reference_map`。M2State 是本包的组合记录，不替代全部 ProjectPlan。

## 2. M4 动作计划与 H3 交接

| 子模块 | ActionPlan 分区 | 主要产物与审计 |
| --- | --- | --- |
| M4.1 表演事件与前提 | `events` | 稳定事件、执行者、对象、目标、起态、前提与触发；核对必保事件和因果关系 |
| M4.2 动作机制与交互过程 | `mechanics` | 支撑、重心、发力、运动、接触、道具操作与恢复；不以动作名称或结果跳过过程 |
| M4.3 结果与动作接续 | `outcomes` | 可见结果、出态、持续／结束、后继条件和状态请求；不覆盖 M8 权威状态 |

M4 适用于 T2VA、I2VA、FL2VA、L2VA、Ref2VA。基础四模式动作正文进入 `integrated_multimodal_description`；Ref2VA 进入 `detailed_description`。首帧用于动作起态，首尾帧约束可观察的中间变化，尾帧用于动作收敛目标。内部事件 ID 与四类官方参考 Label 分开管理，最终编译由 M11 完成。

完整逐字段、逐 Label 编排与审计见 [M4 H3 映射](h3-action-performance/references/h3-label-mapping.md)；独立输入、三分区、版本、未知项与工具用法见 [M4 合同指南](h3-action-performance/references/contract-guide.md)；专业检查和责任回传见 [M4 审计交接](h3-action-performance/references/audit-and-handoff.md)。

## 3. M3 空间计划与 H3 交接

| 子模块 | SpatialPlan 分区 | 主要产物与审计 |
|---|---|---|
| M3.1 空间坐标与场景拓扑 | `topology` | 坐标约定、锚点、区域及连接；明确世界／身体／屏幕方向 |
| M3.2 站位与移动路线 | `blocking` | 稳定实体的起终位、朝向、路径、层次与队形变化 |
| M3.3 交互区域与遮挡约束 | `interactions` | 接触、交叉、避让、视线、允许遮挡和关键可见条件 |

M3 适用于五种 H3 输入模式。T2VA 从文字组织空间；I2VA 从首帧发展；FL2VA 连接首尾空间端点；L2VA 收敛到尾帧；Ref2VA 按已授权参考用途逐镜组织空间。基础四模式对应三字段，Ref2VA 对应六字段。四类官方参考 Label 与 M3 内部实体／区域／路线 ID 分开，由 M11 完成实际编号和序列化。

完整逐字段、逐 Label 编排／审计说明见 [M3 H3 映射](h3-scene-blocking/references/h3-label-mapping.md)。公开调用与 JSON 示例见 [M3 合同指南](h3-scene-blocking/references/contract-guide.md)，领域规则和来源由技能入口按需路由。

## 4. 既有 M2 与 H3 的对应

| 输入模式 | M2 交接重点 | 官方字段/Label 去向 |
|---|---|---|
| T2VA | 无参考时空集合、文字要求 | `integrated_multimodal_description` 等基础三字段 |
| I2VA | 实际首帧资产与角色、变化边界 | 首帧对齐指令及基础三字段 |
| FL2VA | 首尾帧身份、角色与衔接约束 | 首尾帧对齐指令及基础三字段 |
| L2VA | 尾帧身份、角色与约束 | 尾帧对齐指令及基础三字段 |
| Ref2VA | 定义、引用用途、保留/变化/复制关系 | 六字段；`<Subject N>`、`<Picture N>`、`<Video N>`、`<Audio N>` |

完整逐项编排与审计见 [H3 模式与 Label 映射](h3-asset-reference/references/h3-label-mapping.md)。M2 的稳定 ID 与 H3 编号分别管理；音轨参考、原信号复制、画内角色和实际说话者不混用。

## 5. 调用与文件组织

运行包仅含 `SKILL.md`、必要 `scripts/`、按需 `references/` 和可复制 `assets/`。测试、开发报告及验证记录在包外，避免成为独立调用的隐含依赖。

M2、M3、M4 运行脚本仅依赖 Python 3.10+ 标准库。M4 示例：

```bash
cd docs/h3skill/h3-action-performance
python scripts/m4_contract.py route assets/request-m4-1.json
python scripts/m4_contract.py check assets/proposal-m4-2.json --request assets/request-m4-2.json
python scripts/m4_contract.py accept assets/state-empty.json assets/proposal-batch.json --requests assets/requests.json
```

M4 的 `accept` 对照实际原请求、只读上下文与来源后返回新草稿；不能把接受成功理解为物理、生成或完整关卡通过。既有 M3 示例：

```bash
cd docs/h3skill/h3-scene-blocking
python scripts/m3_contract.py route assets/request-m3-1.json
python scripts/m3_contract.py check assets/proposal-m3-2.json --request assets/request-m3-2.json
python scripts/m3_contract.py accept assets/state-empty.json assets/proposal-batch.json --requests assets/requests.json
```

上例输出的顶层 `state` 是新草稿；`validation.overall` 仍为 `unverified`。样例是设计夹具，替换为任务资料后应重新检查。M3 的 `accept` 必须提供实际原请求数组，以核对上下文与来源保真。

既有 M2 示例：

```bash
cd docs/h3skill/h3-asset-reference
python scripts/m2_contract.py route assets/request-m2-3.json
python scripts/m2_contract.py check assets/proposal-m2-3.json --request assets/request-m2-3.json
python scripts/m2_contract.py accept assets/state-empty.json assets/proposal-batch.json
```

`route` 定位显式目标，语义工作尚未开始；`check` 检查已实现合同关系；`accept` 返回新草稿，真正记录在报告的 `state` 字段；`impact` 按登记消费者读路径定位失效。均不自动解读自然语言、读取媒体或调用 H3。

独立调用最小输入、数据类型、范围语义、未知处理和版本规则分别见 [M3 合同指南](h3-scene-blocking/references/contract-guide.md)与 [M2 合同指南](h3-asset-reference/references/contract-guide.md)。示例资产均为文字示例，不能当作已提供媒体。

## 6. 验证入口和完成边界

- [M4 开发与验收记录](20261105-development-m4-v001.md)：需求、实现、来源、实际验证和能力边界。
- [M4 测试](tests/m4/)与[实际审阅记录](validation/m4/)：独立子模块、组合、负例、可移植运行及文字试用。
- [M4 发布清单](release-manifest-m4.json)与[核验工具](tools/verify_m4_release.py)：复查文件、来源、冻结基线和保护范围。

- [M3 开发与验收记录](20261105-development-m3-v001.md)：M3 发布时的需求、设计、来源、实际验证和限制。
- [M3 测试](tests/m3/)与[实际审阅记录](validation/m3/)：独立子模块、组合、负例及文字试用。
- [M3 发布清单](release-manifest-m3.json)与[核验工具](tools/verify_m3_release.py)：在对应历史提交复查 M3 文件、来源、冻结基线及变更范围。
- [M2 开发与验收记录](20261105-development-m2-v001.md)：用户要求、设计决定、来源、实际验证和能力边界。
- [M2 测试目录](tests/m2/)：运行合同和负例。
- [M2 实际验证记录](validation/m2/)：独立使用、源完整性和本轮发布检查。
- [M2 发布清单](release-manifest-m2.json)：M2 发布快照文件与哈希。
- [M2 发布核验工具](tools/verify_m2_release.py)：重现结构、来源、基线、可移植性与清单检查。
- [M1 原开发记录](20261104-development-m1-v001.md)：首模块的实现与验收。

M3 核验器应在其对应的历史发布提交中执行。确定性工具始终保留专业语义/媒体未验证，实际 Agent 文字试用另有记录；没有 H3 推理、真实生成质量、宿主自动触发率或全流程完成声明。

## 7. 基线与历史记录

`release-manifest.json`、`tools/verify_release.py` 及原 `validation/` 下的 M1 报告对应首模块发布快照 `faa8edc3`。其中旧核验器覆盖当时整个 h3skill 目录，不能作为扩展目录后的全局核验器；M2 的 `release-manifest-m2.json` 与 `verify_m2_release.py` 对应 `91e6ed0b` 发布快照，其中的 README 哈希也具有历史范围。M3 发布使用独立清单和核验器，并核对 M1、M2 运行包字节未变。历史记录不重写为本轮结果。

M3 的 `release-manifest-m3.json` 与 `verify_m3_release.py` 同样对应其历史发布快照，其中 README 哈希不用于否决后续经授权的索引更新。M4 使用独立清单与核验器，逐项核对 M1—M3 运行包和冻结文档未变；旧报告不重写为本轮结果。

从仓库根执行 `python docs/h3skill/tools/verify_m4_release.py` 可复查 M4 发布完整性。实际结果见本轮开发记录；本包没有 H3 推理、真实生成成功率、宿主自动触发率或全部十二模块已完成声明。

集中来源：

- [冻结开发方案](https://github.com/Nuos/H3-h3-prompt-journal/tree/608813b6e51531ac47f860bc384a454a504fe9ff/docs/skillplan)。
- [M1 首次发布目录与原 README](https://github.com/Nuos/H3-h3-prompt-journal/tree/faa8edc311589d68d37e93524c7cb8e553fff857/docs/h3skill)。
- [M3 案例读取基线](https://github.com/Nuos/H3-h3-prompt-journal/tree/91e6ed0b09d17e13cf5f58cccfe0df588c5b1d8a/case-studies)。
- [M3 来源与许可记录](h3-scene-blocking/references/provenance-and-license.md)；[M2 来源与许可记录](h3-asset-reference/references/provenance-and-license.md)。
- [M4 来源与许可记录](h3-action-performance/references/provenance-and-license.md)；[M4 案例读取基线](https://github.com/Nuos/H3-h3-prompt-journal/tree/545a99015cfa00a6f07ee05d1d0f21e09d89d46c/case-studies)。
