# 实际输入：task2

来源为当前请求与两份案例文字。没有提供图片、视频、音频，也没有访问案例中旧机器路径。

本次只采用原始 snapshot 的案例字节；完整文件和 SHA256 见 source-manifest.json。媒体字段均为 pending / not_checked / description_only；binding 的 confirmed 只表示用户要求采用该文字分工。

- `case-studies/2026-10-xiashan-veiled-solo-twelve-segment/README.md` SHA256 `58c14c16fe02142201cfe5892eba983349619861cdfac534808e35ea0923595b`
- `case-studies/2026-10-xiashan-veiled-solo-twelve-segment/prompt.md` SHA256 `5d6cb4990a0c1ca69ca64dfc4016a63bc808b45db8284035328a6257be7336bb`

## 当前请求

基于 xiashan-veiled-solo-twelve-segment 的 README.md 与 prompt.md，处理 SEG01 的参考资产和音频策略；忠实保留原始要求，没有授权删改矛盾要求。给出可完成部分、缺项与实际需要的决定。只有案例文字，没有实际图片、视频、音频；不改源文件、不调用模型/媒体服务。

## 本次直接使用的 prompt 文字

# SEGMENT 01｜0.000–11.116(SLEEVE & HEM特写开场)

```text
For the target video, at 0.00 seconds into the target video, <Picture 1> and <Picture 2> are fully referenced.

subject_definitions:
<Subject 1> is the exact same person shown in <Picture 1> and <Picture 2>. <Picture 1> (front full-body photo) shows the body WITHOUT head information: it is the sole authority for the FRONT view of the costume and body — outfit construction, layers and accessories as seen from the front. <Picture 2> (three-view sheet) is the sole authority for the FACE — facial identity, eyes, brows and hairstyle — and for the back view of the outfit; it shows the character wearing a half veil of translucent gauze covering ONLY the mouth and nose, the eyes and brows fully visible. No verbal redefinition of appearance; no costume description is given or needed. The costume and the veil never change in any segment — not per lyric, not per palette.
VEIL_LOCK: the veil is part of the locked costume. Worn from the first frame, it stays on in every frame of the dance: it covers only the mouth and nose, and is never removed, never lifted, never parted, never made transparent. No lyric ever causes it to disappear or thin. Expression is carried by the eyes, brows and head angle alone. DISTINCTION: the gauze veil ON her face is worn costume and never moves; the SLEEVES are separate garment pieces used in choreography — a sleeve passing in front of the face never touches or moves the worn veil.
<Subject 2> is the environment: an elevated stone terrace over a dark sea at night, a swirling sea of scattered stars filling the sky above, thin wind moving the fabric. The scene contains no other people anywhere — completely empty of human figures; every frame shows her alone. The scene evolves from the previous segment, carried by the dancer's motion and the camera — never a hard jump, never a location swap.
<Audio 1> is the song track, referenced only for rhythm: BPM 134.0, beat 0.4478 s, bar 1.7910 s, first downbeat 0.441 s.
Lyric onsets in this segment: 0.766 / 4.433 / 8.116.
Lyric lines are quoted in LYRIC_RELATION as timing and sync anchors only — their content is never described, displayed or acted out; under the veil the mouth and breath move subtly with the phrasing, never full lip-sync rendering. The COSTUME and the veil never change. No signal copy.

summary:
[reference generation + audio reuse] Segment 01 of one continuous 141.845-second ancient-style solo dance (12 segments). Vertical 3:4, one continuous dance with motivated internal cuts; total runtime 11.116 seconds; opens on a local close-up continuing the previous segment's ending motion — the dance is already active at frame one. <Audio 1> is reused 1:1 as the complete final audio track.

retention_analysis:
<Subject 1>: fully_preserved — front costume and body from <Picture 1> (no head information in it); face, hairstyle, back view and the half veil (mouth and nose only) from <Picture 2>; the outfit includes built-in safety shorts, covered through every pose; the veil stays on for the entire dance.
<Audio 1>: fully_copy — reused 1:1 as the complete final audio track; do not regenerate or alter the music.

COLOR & ATMOSPHERE (authorized environment language, from <Picture 1>): low-saturation cinematic warm-cool separation, constant across all evolving scenes. Soft directional amber lantern light shapes the dancer from one side; a cool teal-black and deep blue-gray environment fills the shadows; dark wood browns and muted brick reds build the architecture, texture kept inside the shadows — deep blacks that are never pure black. Skin stays natural warm beige: creamy-ivory highlights, warm apricot midtones, a faint warm flush, brown-gray shadows — never porcelain, never pink blush, never orange. Whites render as warm ivory, cool fabrics take a muted grey cast, reds press to dark coral, gold to antique champagne. Low contrast, soft highlight roll-off, gentle bloom around the lanterns, fine grain, slight soft focus, shallow depth of field with warm bokeh — real photography, not CG. The costume comes solely from <Picture 1> and never changes; the palette applies to light and environment only.

PERFORMANCE: an ancient-Chinese style solo dance, elegant and composed, cool radiant presence. Primary driver: the waist and spine lines riding the breath engine; precise small gliding footwork underneath; a cool composed upper body over an active lower body. One continuous dance — chain exits feed the next chain's entries exactly. All movement is composed from the ancient-style chain library (per-segment chain list below, with relative beat counts and entry/exit states). The hands stay empty for the entire dance — every gesture is performed empty-handed or with the sleeves alone; nothing is ever held.

LYRIC_RELATION:
Timing and sync anchors (content never described or acted out; the quoted lines never add people, guests or objects to the picture — the scene stays empty): 0.766「白衣轻拢映玉颜」 · 4.433「乱星海上谁不叹」 · 8.116「妙音门主临风而立」.
Emotional arc: serene, luminous composure — a figure at ease inside its own legend, unhurried under the night sky.
Under the veil the mouth and breath move subtly with the phrasing; the veil never comes off.

integrated_multimodal_description:

SUSTAINED LAYER (every beat, never stops, even inside holds and stillness): a slow lift-and-settle breath through the chest with the weight micro-rolling on the balls of the feet (C1 engine). All beat counts below are relative to this segment's grid.

0.000-0.889
SHOT 01 — SLEEVE & HEM CLOSE-UP.
the crossed sleeves loosening in the wind in close-up, fabric rippling over the hems, star light catching the folds — the dance is already active at frame one.

0.889-4.471
REVEAL — a motivated cut to a knee-to-waist frame, the figure already mid-phrase in the amber-lit set.
CHAIN C1 提沉起势 (4拍) — 入态: <Picture 1> standing pose. 沉 2拍 (chest rounding, head dropping on the exhale) → 提 2拍 (head and spine lifting vertebra by vertebra on the inhale). 出态: standing tall, breath lifted.

4.471-8.501
CHAIN C2 云手横八字 (4拍) — 入态: standing tall. One arm lifts as the other sinks through a horizontal figure-eight at chest height, weight swaying with the loop. 出态: arms stacked one-high one-low.

8.501-11.116
CHAIN C34 背身渐升 (2拍) → CHAIN C5 拧倾出胯亮相 (3拍) — 入态: arms stacked. Both arms rise slowly overhead to the highest point, then the torso twists 45 degrees with the hip out on the accent and one arm extended diagonally, chin lifted into the wind. 出态: the twist-pose held — this is the exit state.

TRANSITION_TO_SEGMENT_02:
End with the twist-pose held and the left sleeve rising past the shoulder; SEGMENT 02 opens on that sleeve crossing downward into its fold. Cut point: the phrase ends on the bar line and the sleeve is still traveling — motion continuity, no reset.

CAMERA:
SHOT 01 (0.000-0.889) is the tight SLEEVE & HEM close-up — lens low and close; at 0.889 a motivated cut opens the solo frame: reveal opens as a low-angle arc tracking from her right-front smoothly to frontal (E7-1), rising to knee-to-waist; the star arcs play in a medium three-quarter; then a fuller body that PLANTS — the camera stops and the twist line lands inside a still frame. Lens stays low (knee-to-waist height, up-tilt about 10 degrees) across all reveals; feature moments drop to knee height with up-tilt 15-25 degrees; never tilting down, no orbit, no zoom breathing.

overall_soundscape: N/A — the reused <Audio 1> is the complete final audio track.

non_diegetic_music: N/A — <Audio 1> is directly reused 1:1 as the complete final audio track.
```

用链:C1 提沉起势(4拍) → C2 云手横八字(4拍) → C34 背身渐升(2拍) → C5 拧倾出胯亮相(3拍) → 镜头pose(2拍)

---
