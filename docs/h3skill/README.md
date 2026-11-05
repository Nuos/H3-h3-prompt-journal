# H3 通用核心技能

**当前新增模块：** M2 `h3-asset-reference` v0.1.0。

**模块合同：** M1 与 M2 各自为 `1.0.0`；不表示全部共享对象已冻结。

**更新日期：** 2026-11-05（America/Los_Angeles）。

**开发基线：** `skillplan-v0.1.2-608813b`；本轮读取仓库 `faa8edc311589d68d37e93524c7cb8e553fff857`。

## 核心摘要

依据冻结的十二模块方案，已交付 **M1 作品意图与段落功能**，本轮新增 **M2 素材解析、资产绑定与参考权限**。M2 含资产登记、主体绑定、属性权限三个可独立调用的子模块，输出版本化 AssetRegistry、EntityRegistry、ReferenceMap。每个技能包可独立复制使用其声明的文字编排和离线合同检查能力。

领域方法限定为 `case-studies/` 文本，重点为 10 月案例。Anthropic 资料只规定技能结构与开发方式，MiniMax 官方资料只规定输入协议。完整视频逆向、H3 模型调用和真实媒体质量均不是这两个包已实现的能力。

## 关键结论

1. M1 负责作品目标；M2 负责素材、身份和参考权限；M11 的实际模式、上传排序、Label 和字段编译边界保持不变。
2. M2 及三个子模块均采用公开最小合同，不强制先执行其他核心模块；子提案由父模块唯一接受。
3. M2 明确区分“素材存在”“已观察”“允许继承”“后端支持”“实际生成符合要求”。
4. 实现、测试和审阅记录位于本目录；冻结方案与 M1 运行包保持原内容。旧测试/发布清单保留其固定提交的历史意义。

**关键词：** M1、M2、素材登记、主体绑定、属性权限、H3 Label、独立调用、来源证据、版本化提案。

## 目录导航

1. 模块入口
2. M2 与 H3 的对应
3. 调用与文件组织
4. 验证入口和完成边界
5. 基线与历史记录

## 1. 模块入口

| 模块 | 技能入口 | 子模块 | 当前实现 |
|---|---|---|---|
| M1 作品意图与段落功能 | [h3-work-intent/SKILL.md](h3-work-intent/SKILL.md) | M1.1 意图约束；M1.2 段落信息；M1.3 情绪母题 | 文字工作流、独立合同与确定性检查；本轮运行包未改 |
| M2 素材解析、资产绑定与参考权限 | [h3-asset-reference/SKILL.md](h3-asset-reference/SKILL.md) | M2.1 资产登记；M2.2 主体绑定；M2.3 属性权限 | 文字工作流、独立合同、冲突/版本/引用检查和交接 |
| M3—M12 | 冻结方案中的后续职责 | 依已锁定职责推进 | 未因本轮交付而标为实现 |

### M2 的三个产物

| 子模块 | 输出对象 | 关键内容 |
|---|---|---|
| M2.1 | AssetRegistry | 来源与版本、媒体通道、可访问性、观察状态及缺项 |
| M2.2 | EntityRegistry | 稳定实体、源内定位、资产多对多绑定、授权依据 |
| M2.3 | ReferenceMap | 属性允许/禁止/未知、明确范围、来源竞争与显式裁决 |

三对象在 `M2State.content` 中分别为 `asset_registry`、`entity_registry`、`reference_map`。M2State 是本包的组合记录，不替代全部 ProjectPlan。

## 2. M2 与 H3 的对应

| 输入模式 | M2 交接重点 | 官方字段/Label 去向 |
|---|---|---|
| T2VA | 无参考时空集合、文字要求 | `integrated_multimodal_description` 等基础三字段 |
| I2VA | 实际首帧资产与角色、变化边界 | 首帧对齐指令及基础三字段 |
| FL2VA | 首尾帧身份、角色与衔接约束 | 首尾帧对齐指令及基础三字段 |
| L2VA | 尾帧身份、角色与约束 | 尾帧对齐指令及基础三字段 |
| Ref2VA | 定义、引用用途、保留/变化/复制关系 | 六字段；`<Subject N>`、`<Picture N>`、`<Video N>`、`<Audio N>` |

完整逐项编排与审计见 [H3 模式与 Label 映射](h3-asset-reference/references/h3-label-mapping.md)。M2 的稳定 ID 与 H3 编号分别管理；音轨参考、原信号复制、画内角色和实际说话者不混用。

## 3. 调用与文件组织

运行包仅含 `SKILL.md`、必要 `scripts/`、按需 `references/` 和可复制 `assets/`。测试、开发报告及验证记录在包外，避免成为独立调用的隐含依赖。

M2 脚本仅依赖 Python 3.10+ 标准库：

```bash
cd docs/h3skill/h3-asset-reference
python scripts/m2_contract.py route assets/request-m2-3.json
python scripts/m2_contract.py check assets/proposal-m2-3.json --request assets/request-m2-3.json
python scripts/m2_contract.py accept assets/state-empty.json assets/proposal-batch.json
```

`route` 定位显式目标，语义工作尚未开始；`check` 检查已实现合同关系；`accept` 返回新草稿，真正记录在报告的 `state` 字段；`impact` 按登记消费者读路径定位失效。均不自动解读自然语言、读取媒体或调用 H3。

独立调用最小输入、数据类型、范围语义、未知处理和版本规则见 [合同指南](h3-asset-reference/references/contract-guide.md)。示例资产均为文字示例，不能当作已提供媒体。

## 4. 验证入口和完成边界

- [M2 开发与验收记录](20261105-development-m2-v001.md)：用户要求、设计决定、来源、实际验证和能力边界。
- [M2 测试目录](tests/m2/)：运行合同和负例。
- [M2 实际验证记录](validation/m2/)：独立使用、源完整性和本轮发布检查。
- [M2 发布清单](release-manifest-m2.json)：本轮文件与哈希。
- [M2 发布核验工具](tools/verify_m2_release.py)：重现结构、来源、基线、可移植性与清单检查。
- [M1 原开发记录](20261104-development-m1-v001.md)：首模块的实现与验收。

从仓库根执行 `python docs/h3skill/tools/verify_m2_release.py` 可复查本轮发布。确定性工具始终保留专业语义/媒体未验证，实际 Agent 文字试用另有记录；没有 H3 推理、真实生成质量、宿主自动触发率或全流程完成声明。

## 5. 基线与历史记录

`release-manifest.json`、`tools/verify_release.py` 及原 `validation/` 下的 M1 报告对应首模块发布快照 `faa8edc3`。其中旧核验器覆盖当时整个 h3skill 目录，不能作为扩展目录后的全局核验器；本轮使用独立的 M2 清单和核验器，并核对 M1 运行包字节未变。历史记录不重写为本轮结果。

集中来源：

- [冻结开发方案](https://github.com/Nuos/H3-h3-prompt-journal/tree/608813b6e51531ac47f860bc384a454a504fe9ff/docs/skillplan)。
- [M1 首次发布目录与原 README](https://github.com/Nuos/H3-h3-prompt-journal/tree/faa8edc311589d68d37e93524c7cb8e553fff857/docs/h3skill)。
- [本轮案例读取基线](https://github.com/Nuos/H3-h3-prompt-journal/tree/faa8edc311589d68d37e93524c7cb8e553fff857/case-studies)。
- [包内来源与许可记录](h3-asset-reference/references/provenance-and-license.md)。
