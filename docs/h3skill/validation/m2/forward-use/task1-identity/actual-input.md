# 实际输入：task1

来源为当前请求与两份案例文字。没有提供图片、视频、音频，也没有访问案例中旧机器路径。

本次只采用原始 snapshot 的案例字节；完整文件和 SHA256 见 source-manifest.json。媒体字段均为 pending / not_checked / description_only；binding 的 confirmed 只表示用户要求采用该文字分工。

- `case-studies/2026-10-identity-only-half-body-dance-six-segment/README.md` SHA256 `c3726c8d92958ba60393b5f0b7c07b6ebd3c9f1152095e0f66423ab871c92695`
- `case-studies/2026-10-identity-only-half-body-dance-six-segment/prompt.md` SHA256 `e1ba6733d366f4a3e1499ba17e8d57a3bb2b51be8d775a2192ceff1f278d6818`

## 当前请求

基于 identity-only-half-body-dance-six-segment 的 README.md 与 prompt.md，把当前双图用途整理为可直接独立调用 M2.3 的请求和提案，并给人可读权限表及 H3 模式/字段交接。只拿到了案例文字，图片/视频/音频没有提供；不改技能、案例、冻结计划，不调用模型/媒体服务或远程写入。

## 本次直接使用的 prompt 文字

# Identity-Only Half-Body Portrait Dance, Six Segments (111 BPM)

> Final H3 prompt, ready to paste. `<Picture 1>` = facial identity ONLY. `<Picture 2>` = full-body appearance + environment ONLY. Neither picture supplies the opening pose — the "half-body portrait feel of Picture 1" is demoted to camera/lens language. Each of the six segments is ONE continuous dance starting from its own first choreographed beat.

### Segment 1

<Picture 1> is ONLY the facial identity reference for the performer.

Use <Picture 1> only to preserve:
facial identity,
facial structure,
eyes,
eyebrows,
nose,
mouth,
jawline,
skin appearance,
and recognizable facial proportions.

<Picture 1> is NOT a pose reference.
<Picture 1> is NOT a body-position reference.
<Picture 1> is NOT a choreography reference.
<Picture 1> is NOT an opening-frame reference.
Do not reproduce the head angle, hand position, arm position, body orientation, stance, or static composition of <Picture 1>.

<Picture 2> is the full-body appearance and environment reference.

Use <Picture 2> to preserve:
body proportions,
overall body scale,
clothing,
accessories,
hair as visible in the full-body reference,
environment,
architecture,
background,
lighting direction,
exposure,
spatial depth,
and realistic photographic appearance.

<Picture 2> is NOT a choreography reference.
Do not reproduce the exact standing posture shown in <Picture 2>.
Do not begin the video by copying the static pose from <Picture 2>.

There is exactly one performer.
No duplicate performer, clone, additional person, or invented background figure.

<Audio 1> is the exact audio for this segment and must be reused 1:1 as the final audio track.

Segment duration: 11.033 seconds.
Tempo: 111 BPM.
Beat: 0.5405 seconds.
Bar: 2.1622 seconds.
Phrase: 4.3243 seconds.

This is ONE continuous dance performance from the first frame to the exact audio endpoint.
The dancer never stops for a camera change, Motion Cut, portrait shot, Hero Action shot, or framing change.

Begin directly with the first choreographed movement specified below.
Do not begin from either reference image's static pose.

## CAMERA / LENS LANGUAGE

Use intimate premium portrait photography inspired by the half-body photographic distance of <Picture 1>.

This is a CAMERA / LENS LANGUAGE instruction only.
It does not copy the pose, head angle, hand placement, body orientation, or composition of <Picture 1>.

Default framing:
close-up,
bust,
half-body,
medium-close.

The performer occupies most of the available resolution.
Prioritize face, shoulders, torso, and hands.

Use a real physically operated handheld camera.
The operator may subtly anticipate the dancer, slightly lag behind the movement, or hold briefly while the dancer moves into the frame.
Do not mechanically track every limb.

When meaningful footwork occurs, physically lower or retreat slightly to reveal the active feet for a brief moment, then immediately return to the intimate half-body relationship.
Do not remain in a long full-body shot.


