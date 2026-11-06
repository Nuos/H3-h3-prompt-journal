# 必保内容追溯

本表对照 `task.md` 与实际生成的 `model-prompt.txt`。程序核验 ID、引用和镜头作用域；“文字审阅通过”由 Agent 逐项对照，未检查媒体实现。

| 义务 ID | 来源必保内容 | 输出镜头与文字证据 | 结论 |
| --- | --- | --- | --- |
| `setting-front` | 街角茶铺、明亮写实自然光；人物衣着与柜台内外 | [Shot 1]："bright street-corner tea shop"; "light-gray apron"; "dark-blue jacket"; "counter separates them throughout" | 文字审阅通过；媒体未验证 |
| `framing-front` | 第一镜0秒、正面中景、肩颈手与完整杯子 | [Shot 1]："frontal medium view"; "shoulders and necks, their hands, and the complete ceramic cup" | 文字审阅通过；媒体未验证 |
| `sign-front` | 原文标牌与标点 | [Shot 1]："今日茶已备好！" | 文字审阅通过；媒体未验证 |
| `place-empty-cup` | 罗成先放空陶杯到柜台中央 | [Shot 1]："First, &lt;Subject 2&gt; places an empty ceramic cup at the counter center" | 文字审阅通过；媒体未验证 |
| `luo-line` | 罗成台词一次、字词标点完全保留 | [Shot 1]：&lt;Subject 2&gt; (S1) ... &lt;d&gt;[Chinese] 请给我一杯热茶。&lt;/d&gt; | 文字审阅通过；媒体未验证 |
| `pouring-hands` | 叶青右手壶柄、左手壶盖 | [Shot 1]："handle firmly in the right hand and steadies its lid with the left" | 文字审阅通过；媒体未验证 |
| `pouring-target` | 热茶倒进杯内、杯子原位 | [Shot 1]："pours hot tea"; "stream lands inside the cup"; "stays in its original central position" | 文字审阅通过；媒体未验证 |
| `cut-side` | 第二镜生成局部3.5秒侧面中景 | [Shot 2]：[Shot 2] At 00:03.500, cut to a steady side medium view | 文字审阅通过；媒体未验证 |
| `continuity-side` | 跨镜身份衣着位置与已装茶杯连续 | [Shot 2]："same filled cup remains at the center at the cut"; "identities, light-gray apron, and dark-blue jacket continue unchanged" | 文字审阅通过；媒体未验证 |
| `sign-side` | 第二镜继续保持同一标牌 | [Shot 2]："the wall sign remains readable"；沿用第一镜已给出的原文字面 | 文字审阅通过；媒体未验证 |
| `return-kettle` | 叶青将壶放回柜台内侧 | [Shot 2]："sets the kettle back on the inner counter" | 文字审阅通过；媒体未验证 |
| `ye-line` | 叶青台词一次、字词标点完全保留 | [Shot 2]：&lt;Subject 1&gt; (S2) ... &lt;d&gt;[Chinese] 小心，茶还很烫！&lt;/d&gt; | 文字审阅通过；媒体未验证 |
| `move-cup` | 罗成右手杯柄、谨慎移到外缘 | [Shot 2]："grips the cup handle with the right hand"; "carefully draws the cup ... toward the outer counter edge" | 文字审阅通过；媒体未验证 |
| `ye-hands-clear` | 叶青双手离开杯子 | [Shot 2]："keeps both hands clear of the cup" | 文字审阅通过；媒体未验证 |
| `end-state` | 8秒两人保持结果状态 | [Shot 2]："cup rests securely at the outer edge"; "Hold these positions through the eight-second endpoint" | 文字审阅通过；媒体未验证 |
| `music-front` | 整段配乐复用、观众可闻、新对白与倒水声 | [Shot 1]："complete source music signal from &lt;Audio 1&gt; starts with this shot as audience-only score" | 文字审阅通过；媒体未验证 |
| `music-side` | 配乐跨切连续、新对白落壶轻擦声 | [Shot 2]："&lt;Audio 1&gt; continues seamlessly across the cut and through the end"; "new warning, kettle contact, and cup movement" | 文字审阅通过；媒体未验证 |

## 参考、台词及参数的独立核对

- 两张图片只嵌在 Subject 来源定义中，没有实际首帧／尾帧或独立构图锚。保留范围仅为人物身份与指定衣服。
- 全部模型字段中仅有两个 `<d>` 块，两句中文台词各出现一次且标点未改；`punctuation_trace` 为空。
- 配乐整段保留，新增四类声音层，因此 `partially_copy`、`full_source=true`、`entire_soundtrack=false` 同时成立。
- `target-parameters.json` 保留 1080×1920、24 fps、8000 ms；导出失败没有改变参数。
- `checks/delivery-consistency-check.json` 保存额外的确定性核对。490 是最终正文按空白切词的参考计数，不是模型 token 数或质量保证。
