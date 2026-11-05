# 有记录的离线技能试用

本目录保存三项真实任务的提示词/组件、计划和脚本结果。camera、showcase 由收到任务和技能路径的独立代理完成，未给预期答案；leg-contact 由集合主编执行，明确属于了解实现的完整试用，不计为独立盲测。主编已阅读这些实际产物并保存 [内容核对](editor-review.json)。

| 任务 | 产物 | 目的与实际结果 |
|---|---|---|
| 摄影组件 | [camera/output.md](camera/output.md) | 相机提前0.5秒到位，转身中一次匹配切，人物不冻结；组件计划严格检查通过。 |
| 三造型展示 | [showcase/output.md](showcase/output.md) | 三段4秒生成各裁3秒，最终30FPS，缺真实参考和音乐时保留draft；严格检查按预期拒绝。 |
| 触地换纹 | [leg-contact/README.md](leg-contact/README.md) | 8秒T2VA，三次接触/四状态、24FPS生成与30FPS编辑分开；正文和计划严格检查通过。 |

106个场景是各技能已编写的回归任务库，**没有宣称全部执行**。三项试用也不是模型生成基准，没有生成或测量视频。

## 在仓库根部复现静态检查

```bash
python3 docs/caseskill/h3-camera-movement-discipline-library/scripts/audit_plan.py docs/caseskill/_validation/forward-runs/camera/plan.json --strict --check-files
python3 docs/caseskill/h3-leg-lift-contact-cut-stocking-six-look/scripts/audit_plan.py docs/caseskill/_validation/forward-runs/leg-contact/plan.json --strict --check-files
python3 docs/caseskill/h3-sock-showcase-right-entry-three-shot/scripts/audit_plan.py docs/caseskill/_validation/forward-runs/showcase/plan.json --check-files
python3 docs/caseskill/h3-sock-showcase-right-entry-three-shot/scripts/audit_plan.py docs/caseskill/_validation/forward-runs/showcase/plan.json --strict --check-files
```

最后一条预期返回1，原因是保留的draft/缺项/未实施检查；前三条返回0。已在最终存放路径重跑，结果见 [reproduction-results.json](reproduction-results.json)。各任务原始日志中的绝对路径是初次执行环境的记录，复现请使用上面的仓库相对路径。

检查器不验证自然语言语义、素材真实性、镜头物理可行性或生成品质。组件模式不含生成片段，因此不会将组件正文冒充已被自动语义检验的完整H3正文。
