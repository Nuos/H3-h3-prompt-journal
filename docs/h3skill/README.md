# H3 通用核心技能

**当前新增模块：** M3 `h3-scene-blocking` v0.1.0。

**模块合同：** M1、M2、M3 各自为 `1.0.0`；不表示全部共享对象已冻结。

**更新日期：** 2026-11-05（America/Los_Angeles）。

**开发基线：** `skillplan-v0.1.2-608813b`；M3 本轮读取仓库 `91e6ed0b09d17e13cf5f58cccfe0df588c5b1d8a`。

## 核心摘要

依据冻结的十二模块方案，已交付 **M1 作品意图与段落功能**、**M2 素材解析、资产绑定与参考权限**，本轮新增 **M3 场景空间、人物站位与交互调度**。M3 含空间坐标与场景拓扑、站位与移动路线、交互区域与遮挡约束三个可独立调用的子模块，输出版本化 `SpatialPlan`。各包可独立复制使用其声明的文字编排和离线合同检查能力。

领域方法限定为 `case-studies/` 文本，重点为 10 月案例。Anthropic 资料只规定技能结构与开发方式，MiniMax 官方资料只规定输入协议。完整视频逆向、H3 模型调用和真实媒体质量均不是这三个包已实现的能力。

## 关键结论

1. M1 决定作品目标，M2 管理身份与参考权限，M3 建立空间条件；动作、摄影、时间和最终模型编译继续由各责任模块处理。
2. M3 及三个子模块采用公开最小合同，兼容的外部输入可替代上游执行；三个专业分区由 M3 父模块唯一接受。
3. 世界方向、人物自身左右和屏幕方向分别记录。图上可达不证明几何无碰撞，文字可见性要求不证明实际镜头无遮挡。
4. 不设置统一人数、禁跨中线或禁遮挡规则；保留案例差异和作用范围。
5. M1、M2 运行包及冻结方案原字节不变。开发报告、测试与审阅证据位于运行包外，旧报告保留历史含义。

**关键词：** M1、M2、M3、空间拓扑、人物站位、移动路线、交互遮挡、H3 Label、独立调用、版本化提案。

## 目录导航

1. 模块入口
2. M3 空间计划与 H3 交接
3. 既有 M2 与 H3 的对应
4. 调用与文件组织
5. 验证入口和完成边界
6. 基线与历史记录

## 1. 模块入口

| 模块 | 技能入口 | 子模块 | 当前实现 |
|---|---|---|---|
| M1 作品意图与段落功能 | [h3-work-intent/SKILL.md](h3-work-intent/SKILL.md) | M1.1 意图约束；M1.2 段落信息；M1.3 情绪母题 | 文字工作流、独立合同与确定性检查；本轮运行包未改 |
| M2 素材解析、资产绑定与参考权限 | [h3-asset-reference/SKILL.md](h3-asset-reference/SKILL.md) | M2.1 资产登记；M2.2 主体绑定；M2.3 属性权限 | 文字工作流、独立合同、冲突/版本/引用检查和交接 |
| M3 场景空间、人物站位与交互调度 | [h3-scene-blocking/SKILL.md](h3-scene-blocking/SKILL.md) | M3.1 空间拓扑；M3.2 站位路线；M3.3 互动遮挡 | 文字工作流、独立合同、图上可达／引用／版本检查、父接受和交接 |
| M4—M12 | 冻结方案中的后续职责 | 依已锁定职责推进 | 未因本轮交付而标为实现 |

### M2 的三个产物

| 子模块 | 输出对象 | 关键内容 |
|---|---|---|
| M2.1 | AssetRegistry | 来源与版本、媒体通道、可访问性、观察状态及缺项 |
| M2.2 | EntityRegistry | 稳定实体、源内定位、资产多对多绑定、授权依据 |
| M2.3 | ReferenceMap | 属性允许/禁止/未知、明确范围、来源竞争与显式裁决 |

三对象在 `M2State.content` 中分别为 `asset_registry`、`entity_registry`、`reference_map`。M2State 是本包的组合记录，不替代全部 ProjectPlan。

## 2. M3 空间计划与 H3 交接

| 子模块 | SpatialPlan 分区 | 主要产物与审计 |
|---|---|---|
| M3.1 空间坐标与场景拓扑 | `topology` | 坐标约定、锚点、区域及连接；明确世界／身体／屏幕方向 |
| M3.2 站位与移动路线 | `blocking` | 稳定实体的起终位、朝向、路径、层次与队形变化 |
| M3.3 交互区域与遮挡约束 | `interactions` | 接触、交叉、避让、视线、允许遮挡和关键可见条件 |

M3 适用于五种 H3 输入模式。T2VA 从文字组织空间；I2VA 从首帧发展；FL2VA 连接首尾空间端点；L2VA 收敛到尾帧；Ref2VA 按已授权参考用途逐镜组织空间。基础四模式对应三字段，Ref2VA 对应六字段。四类官方参考 Label 与 M3 内部实体／区域／路线 ID 分开，由 M11 完成实际编号和序列化。

完整逐字段、逐 Label 编排／审计说明见 [M3 H3 映射](h3-scene-blocking/references/h3-label-mapping.md)。公开调用与 JSON 示例见 [M3 合同指南](h3-scene-blocking/references/contract-guide.md)，领域规则和来源由技能入口按需路由。

## 3. 既有 M2 与 H3 的对应

| 输入模式 | M2 交接重点 | 官方字段/Label 去向 |
|---|---|---|
| T2VA | 无参考时空集合、文字要求 | `integrated_multimodal_description` 等基础三字段 |
| I2VA | 实际首帧资产与角色、变化边界 | 首帧对齐指令及基础三字段 |
| FL2VA | 首尾帧身份、角色与衔接约束 | 首尾帧对齐指令及基础三字段 |
| L2VA | 尾帧身份、角色与约束 | 尾帧对齐指令及基础三字段 |
| Ref2VA | 定义、引用用途、保留/变化/复制关系 | 六字段；`<Subject N>`、`<Picture N>`、`<Video N>`、`<Audio N>` |

完整逐项编排与审计见 [H3 模式与 Label 映射](h3-asset-reference/references/h3-label-mapping.md)。M2 的稳定 ID 与 H3 编号分别管理；音轨参考、原信号复制、画内角色和实际说话者不混用。

## 4. 调用与文件组织

运行包仅含 `SKILL.md`、必要 `scripts/`、按需 `references/` 和可复制 `assets/`。测试、开发报告及验证记录在包外，避免成为独立调用的隐含依赖。

M2、M3 运行脚本仅依赖 Python 3.10+ 标准库。M3 示例：

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

## 5. 验证入口和完成边界

- [M3 开发与验收记录](20261105-development-m3-v001.md)：本次需求、设计、来源、实际验证和限制。
- [M3 测试](tests/m3/)与[实际审阅记录](validation/m3/)：独立子模块、组合、负例及文字试用。
- [M3 发布清单](release-manifest-m3.json)与[核验工具](tools/verify_m3_release.py)：复查本轮文件、来源、冻结基线及变更范围。
- [M2 开发与验收记录](20261105-development-m2-v001.md)：用户要求、设计决定、来源、实际验证和能力边界。
- [M2 测试目录](tests/m2/)：运行合同和负例。
- [M2 实际验证记录](validation/m2/)：独立使用、源完整性和本轮发布检查。
- [M2 发布清单](release-manifest-m2.json)：M2 发布快照文件与哈希。
- [M2 发布核验工具](tools/verify_m2_release.py)：重现结构、来源、基线、可移植性与清单检查。
- [M1 原开发记录](20261104-development-m1-v001.md)：首模块的实现与验收。

从仓库根执行 `python docs/h3skill/tools/verify_m3_release.py` 可复查 M3 本轮发布。确定性工具始终保留专业语义/媒体未验证，实际 Agent 文字试用另有记录；没有 H3 推理、真实生成质量、宿主自动触发率或全流程完成声明。

## 6. 基线与历史记录

`release-manifest.json`、`tools/verify_release.py` 及原 `validation/` 下的 M1 报告对应首模块发布快照 `faa8edc3`。其中旧核验器覆盖当时整个 h3skill 目录，不能作为扩展目录后的全局核验器；M2 的 `release-manifest-m2.json` 与 `verify_m2_release.py` 对应 `91e6ed0b` 发布快照，其中的 README 哈希也具有历史范围。M3 本轮使用独立清单和核验器，并核对 M1、M2 运行包字节未变。历史记录不重写为本轮结果。

集中来源：

- [冻结开发方案](https://github.com/Nuos/H3-h3-prompt-journal/tree/608813b6e51531ac47f860bc384a454a504fe9ff/docs/skillplan)。
- [M1 首次发布目录与原 README](https://github.com/Nuos/H3-h3-prompt-journal/tree/faa8edc311589d68d37e93524c7cb8e553fff857/docs/h3skill)。
- [M3 案例读取基线](https://github.com/Nuos/H3-h3-prompt-journal/tree/91e6ed0b09d17e13cf5f58cccfe0df588c5b1d8a/case-studies)。
- [M3 来源与许可记录](h3-scene-blocking/references/provenance-and-license.md)；[M2 来源与许可记录](h3-asset-reference/references/provenance-and-license.md)。
