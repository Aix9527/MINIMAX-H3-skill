# Natural Dialogue Motion / 自然对白口型

## 中文

该模块用于解决生成视频中人物说话时嘴唇和下颌动作过大的问题。普通影视对白默认使用 `SUBTLE_LIPSYNC`，声音清晰度与嘴部动作幅度必须分开控制。

### 默认规则

- 普通对白默认：`SUBTLE_LIPSYNC`。
- 嘴唇小幅开合，下颌位移最小化。
- 不要求每个音节都出现清晰、夸张的可视口型。
- 停顿时嘴唇自然回到闭合或近闭合状态。
- 表演优先由眼神、视线、呼吸、眉部、姿态、手部与反应延迟承担。
- 声音可以清晰、靠前、可懂，但不能把“声音清晰”翻译成“嘴巴动作明显”。
- 非说话角色保持自然闭口或近闭口，只允许呼吸、眨眼与听者反应。
- 旁白、内心独白、离屏思绪默认 `CLOSED_LIPS`，可见角色不得跟随旁白做口型。

### 口型等级

| 模式 | 适用场景 | 嘴部动作 |
|---|---|---|
| `CLOSED_LIPS` | 旁白、内心独白、未说话角色 | 不做对白口型 |
| `SUBTLE_LIPSYNC` | 默认电影对白 | 小幅嘴唇运动、下颌基本稳定 |
| `NATURAL_LIPSYNC` | 正常交流、口型可见但非视觉重点 | 自然口型，避免过度咬字 |
| `EMPHATIC_LIPSYNC` | 强烈争辩、情绪强调 | 允许适度更明显的口型 |
| `SHOUT_OR_SING` | 喊叫、尖叫、歌唱 | 只有这里允许大幅张口与连续明显口型 |

### 对白时间结构

对白不应默认占满整个生成段。优先保留：

`反应/吸气 → 说话 → 短暂停顿 → 嘴部回落 → 听者或说话者反应`

示例：8 秒镜头可采用：

- `0.0–1.0s` 视线、吸气、准备说话；
- `1.0–6.2s` 对白；
- `6.2–8.0s` 嘴部回落、呼吸、反应。

如果对白过长，应优先拆句、延长镜头、切听者反应镜头或改用离屏继续说话，而不是强迫角色高速连续动嘴。

### 摄影建议

普通对白优先中近景、三分之四侧角或自然视平线。除非剧情需要，不要让嘴成为画面中心，不要在长对白中持续正脸大特写。可以在声音连续时切到听者反应，减少连续可见口型负担。

### 对白专用 Negative

仅在普通对白且确实存在嘴部过度运动风险时加入：

`exaggerated lip movement, over-articulated speech, large repetitive mouth opening, excessive jaw pumping, chewing-like dialogue motion, continuous mouth motion during pauses`

不要把这些 Negative 加到无对白镜头。

## English

This module addresses overly visible lip and jaw motion during generated dialogue. Ordinary cinematic dialogue defaults to `SUBTLE_LIPSYNC`. Audio intelligibility and visible mouth-motion amplitude must be controlled separately.

### Default rules

- Ordinary dialogue defaults to `SUBTLE_LIPSYNC`.
- Use small lip openings and minimal jaw displacement.
- Do not require visibly exaggerated articulation for every syllable.
- During pauses, lips naturally return toward closed or near-closed rest.
- Carry performance primarily through eyes, gaze, breath, brows, posture, hands, and reaction latency.
- Voice may remain clear, foregrounded, and intelligible without visually strong articulation.
- Non-speaking characters keep relaxed closed or near-closed lips, with only breathing, blinking, and listening reactions.
- Narration, inner monologue, and off-screen thought default to `CLOSED_LIPS`; visible characters must not articulate the voiceover.

### Lip-motion levels

| Mode | Use | Visible motion |
|---|---|---|
| `CLOSED_LIPS` | narration, inner monologue, non-speakers | no dialogue articulation |
| `SUBTLE_LIPSYNC` | default cinematic dialogue | small lip motion, mostly stable jaw |
| `NATURAL_LIPSYNC` | ordinary conversation where the mouth is visible but not the focus | natural articulation without over-enunciation |
| `EMPHATIC_LIPSYNC` | heated argument or deliberate verbal emphasis | moderately stronger articulation |
| `SHOUT_OR_SING` | shouting, screaming, singing | large openings and sustained visible articulation are allowed only here |

### Dialogue timing

Dialogue should not automatically fill the entire generated clip. Prefer:

`reaction / inhale → speech → short pause → mouth settles → reaction`

For an 8-second clip, a useful pattern is:

- `0.0–1.0s` gaze, inhale, pre-speech preparation;
- `1.0–6.2s` dialogue;
- `6.2–8.0s` mouth settles, breath, reaction.

If a line is too long, split it, extend the shot, cut to a listener reaction, or continue the voice off-screen instead of forcing rapid continuous mouth motion.

### Camera guidance

For ordinary dialogue, prefer medium close-ups, three-quarter angles, or natural eye-level framing. Unless the story requires it, do not make the mouth the visual focal point and do not hold a long frontal extreme close-up through an entire line. Dialogue audio may continue over a listener reaction shot.

### Dialogue-specific negatives

Only when ordinary dialogue has a real over-articulation risk, add:

`exaggerated lip movement, over-articulated speech, large repetitive mouth opening, excessive jaw pumping, chewing-like dialogue motion, continuous mouth motion during pauses`

Do not add these negatives to silent shots.