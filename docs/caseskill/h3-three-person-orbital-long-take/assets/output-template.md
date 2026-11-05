# 三人物遮挡接力、独立环绕与近距离群像长镜头：输出工作表

将本文件复制到任务目录并填写；它是规划/交付模板，不是直接送入 H3 的全部正文。填写完的计划、参考权限和审计记录与生成提示词分开保存。

## 1. 当前任务与输入

| 输入项 | 当前任务值、来源与待核验内容 |
|---|---|
| 三个身份槽位与图片 | 把实际文件分别绑定到Person 1、Person 2、Person 3，记录各自可见的身份、发型、服装与体型依据；确认它们确实表示三个不同人物。没有图像时使用明确待绑定槽位，不编造人物性别、脸部、服装细节，也不把三张同一人的照片自动当成三位人物。 |
| 主环境和空间资料 | 指定唯一主环境来源，登记可见地面、固定锚点、墙面家具、光照、反光面、可用机位空间及未知区域；如有平面图、尺寸或预演，记录其来源。单张图提供视觉依据，不自动提供已校准的完整三维坐标。 |
| 时长与环绕验收 | 指定总长、画幅、每人必须经过的水平视角与垂直取景范围，区分多视角环绕弧和真正360度方位覆盖；明确单次生成一镜到底是否硬性要求，以及是否接受较短改编或经披露的隐藏接缝合成。 |
| 可见性与演员活动边界 | 指定普通环绕只见当前人物、两次转接是否也禁止旧人物任何边缘与新人同框、最后群像何时开始；定义三人固定站位附近的微动作范围、各自独立动作和允许的接触／间距。 |
| 光学与声音 | 提供已知视场／镜头、清晰可读需求、最终半身覆盖范围，以及静音、现场声或配乐要求；没有音频输入时不凭fashion-MV标签捏造原曲、BPM或音频复用。 |

## 2. 本案例交付

### 身份与空间契约

三个固定人物槽位到实际素材／Subject的映射、独立主环境Subject、参考权限、可见锚点和未知区域、站位与微动作范围。

### 环绕与显隐计划

明确弧线或360度验收、三次水平／垂直路径、每阶段present与visible集合、转接例外许可、遮挡表面、接入机位和反射／净空待核验项。

### 唯一时间轴和最终群像方案

每个环绕、转接、制动、后拉与稳定窗口，原案冲突修复、总长核算、三人相近摄影待遇、最终身体覆盖与现有站位的相容性。

### 单镜头Ref2VA与执行边界

六字段英文提示词、一个Shot内连续阶段、实际声音策略、概念20秒与已核验范围内候选的明确标记；文本审计、待空间预检和待生成回归分别报告。

## 3. 参考权限与时间

| 素材 ID | 实际文件/来源 | 允许参考 | 不继承内容 | 生效片段/镜头 | 证据状态 |
|---|---|---|---|---|---|
| 按实际填写 | 按实际填写 | 按实际填写 | 按实际填写 | 按实际填写 | provided/missing |

| 创作段 | 生成切片 | 全局起止 | 局部时长 | 音频偏移 | 入态→出态 | 交接素材/后期策略 |
|---|---|---|---|---|---|---|
| 按实际填写 | 按实际填写 | 按实际填写 | 按实际填写 | 按实际填写 | 按实际填写 | 按实际填写 |

## 4. H3 生成正文模板

只在要求完整提示词时使用。选一种模式，删除不适用模板，填入实际对象、镜头和声音；不要把本页标题、检查表或中文说明送入生成器。以下大括号表示待填字段，最终 `.txt` 中不得残留。

### Ref2VA：六字段

```text
subject_definitions: {define actual reusable content and reference roles}

summary: {task-type prefix and target relationships}

retention_analysis: {one applicable preservation/copy relationship per independently used reference}

detailed_description: {one or two style sentences before Shot 1}
[Shot 1] {composition, visible subjects, environment, causal action, camera, sound and active references}
[Shot 2] At {MM:SS.mmm}, {only include if an actual cut is planned}

overall_soundscape: {ambient and physical sound; N/A only for explicit total silence}

non_diegetic_music: {audience-only score or N/A}
```

### T2VA / I2VA / FL2VA / L2VA：三字段

T2VA 不加图像对齐句。其他模式先选择对应的官方对齐句并填入实际最后一镜编号、两位小数时长，随后空一行。

```text
I2VA: For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.
FL2VA: How the reference pictures align with the target video — Picture 1 (from Shot 1) aligns with the 0.00-second mark of the target video; Picture 2 (from Shot {N}) aligns with the {S.SS}-second mark of the target video.
L2VA: How the reference pictures align with the target video — <Picture 1> (from [Shot {N}]) aligns with the {S.SS}-second mark of the target video.
```

上面用于选择的 `I2VA:`、`FL2VA:`、`L2VA:` 前缀不属于生成端正文，复制时删除。

```text
integrated_multimodal_description: [Shot 1] {style, initial composition and full audiovisual development}

overall_soundscape: {ambient and physical sound}

non_diegetic_music: {audience-only music or N/A}
```

## 5. 逐项验收与未验证范围

| ID | 判据 | 结果 | 具体证据/修复 |
|---|---|---|---|
| OL01 | 三个身份槽位各自绑定实际参考；Picture 1兼管主环境，Picture 2/3只管各自外观，角色顺序和环绕中心变化不重编号、不换身份。 | unverified | 填入实际检查记录 |
| OL02 | 三人始终在场与当前可见谁分开；反射、剪影和局部肢体也属于可见内容，转接残留遮挡边缘的许可要显式定义。 | unverified | 填入实际检查记录 |
| OL03 | 多视角环绕弧和完整360度采用不同验收，不能以垂直扫描、人物自转或前侧到后侧的片段冒充整圈。 | unverified | 填入实际检查记录 |
| OL04 | 站位、相机路径、视场、身体活动净空和最终半身群像必须联合检查；单张环境图不等于已校准三维空间或已证明可行布局。 | unverified | 填入实际检查记录 |
| OL05 | 换环绕中心保持摄影机轨迹连续；P1高位结束接P2头部，P2低位结束接P3脚部，遮挡表面必须符合当前高度与真实服装。 | unverified | 填入实际检查记录 |
| OL06 | 转接单独占用时间，不与下一正式环绕重复计时；保存最终群像预算，完成优先不能变成无上限超时或牺牲第三人。 | unverified | 填入实际检查记录 |
| OL07 | 人物在有限站位范围独立微动，摄影机绕开人体；近身视差和遮挡来自空间运动，不靠人物故意挡镜、原地摇摄或身份形变。 | unverified | 填入实际检查记录 |
| OL08 | 结尾采用有减速转向窗口的短物理后拉，在近距离半身群像停止；停止相机不冻结三人，最终同框不证明全过程物理连续。 | unverified | 填入实际检查记录 |
| OL09 | 原案20秒一镜到底保留为概念要求；已核验标准H3单次4–15秒，较短改编或多段拼接都必须明示对原要求的变更。 | unverified | 填入实际检查记录 |
| OL10 | Occlusion-Linked Orbital Long Take是案例方法名，不是H3接口参数；一个连续镜头只有一个Shot，译文与作者成功陈述不能当成新增实测结果。 | unverified | 填入实际检查记录 |

记录静态检查结果、仍缺素材/测量、是否已实际生成，以及实际生成后才可评估的身份、动作、声音和接缝表现。
