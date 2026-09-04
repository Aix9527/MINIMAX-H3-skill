# Natural Dialogue Motion / 自然对白口型

## 中文

该模块用于解决生成视频中人物说话时嘴唇和下颌动作过大的问题。普通影视对白默认使用 `SUBTLE_LIPSYNC`，声音清晰度与嘴部动作幅度必须分开控制。

如需防止人物串台词，同时读取 [Speaker Ownership & Scene Lock](speaker-scene-lock.md)。

### H3 对白语法硬规则

正确：

```text
人物描述与声线 (S1) says: <d>[Chinese] 中文台词。</d>
```

错误：

```text
<d>[Chinese][S1] 中文台词。</d>
```

`(S1)` 必须位于 `<d>` 外；`<d>` 内只能包含语言标签和实际台词。

中文项目中，每一条可听人物对白、旁白、内心独白和离屏人声都必须使用 `<d>[Chinese] ...</d>`。英文镜头描述只是指令，不允许被朗读、翻译成英文对白或替代中文台词。

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
| `NATURAL_LIPSYNC` | 正常交流 | 自然口型，避免过度咬字 |
| `EMPHATIC_LIPSYNC` | 强烈争辩、情绪强调 | 允许适度更明显的口型 |
| `SHOUT_OR_SING` | 喊叫、尖叫、歌唱 | 只有这里允许大幅张口与连续明显口型 |

### 对白时间结构

对白不应默认占满整个生成段。优先保留：

`反应/吸气 → 说话 → 短暂停顿 → 嘴部回落 → 说话者或听者反应`

8 秒镜头可参考：

- `0.0–1.0s` 视线、吸气、准备说话；
- `1.0–6.2s` 对白；
- `6.2–8.0s` 嘴部回落、呼吸、反应。

台词过长时，优先级改为：

1. 拆成多个生成段；
2. 延长可用对白时长；
3. 保持原说话者作为主要可见人物；
4. 只有确实需要时才使用短离屏对白。

不要再默认使用“人物 A 说到一半 → 切人物 B 完整正脸 → A 离屏继续长时间说话”。这会增加台词被人物 B 接管的风险。

### 听者反应安全规则

需要听者反应时：

- 最稳：等说话者台词结束后再切完整听者正脸；
- 对白仍在继续时，优先展示听者背影、后脑、肩部、手部或环境；
- 如果必须显示听者脸，避免嘴部成为清晰视觉焦点，并明确 `MUTE_LISTENER / CLOSED_LIPS / no speech / no phoneme motion`；
- 对白所有权改变时优先切成新的生成段。

### 旁白与内心独白

同一人物内心独白继续使用同一个 `(S1)`，并采用：

```text
The woman (S1) says in an off-screen voiceover: <d>[Chinese] 中文内心独白。</d> while her on-screen lips remain completely closed.
```

独立旁白使用新的稳定 Speaker ID，例如 `(S5)`，同样使用 `says in an off-screen voiceover`。不要创造 `S1-VO` 之类的非标准 `<d>` 标记。

### 摄影建议

普通对白优先中近景、三分之四侧角或自然视平线。除非剧情需要，不要让嘴成为画面中心，不要在长对白中持续正脸大特写。

对于多人对白，摄影首先服务“谁在说”而不是追求反打变化。高可靠性模式下，一段生成只让一个人物拥有对白，下一人物开口时再切下一段。

### 对白专用 Negative

普通对白存在嘴部过度运动风险时可加入：

`exaggerated lip movement, over-articulated speech, large repetitive mouth opening, excessive jaw pumping, chewing-like dialogue motion, continuous mouth motion during pauses`

存在串台词风险时可加入：

`wrong speaker, voice swap, dialogue ownership transfer, non-speaker lip-sync, multiple mouths sharing one line`

中文项目存在语言漂移时可加入：

`English speech, English dialogue, translated dialogue, prompt text read aloud`

不要把这些 Negative 加到无对白镜头。

## English

This module addresses overly visible lip and jaw motion during generated dialogue. Ordinary cinematic dialogue defaults to `SUBTLE_LIPSYNC`. Audio intelligibility and visible mouth-motion amplitude must be controlled separately.

For wrong-speaker prevention, also read [Speaker Ownership & Scene Lock](speaker-scene-lock.md).

### Canonical H3 dialogue syntax

Correct:

```text
Speaker identity and voice (S1) says: <d>[Chinese] 中文台词。</d>
```

Incorrect:

```text
<d>[Chinese][S1] 中文台词。</d>
```

The stable speaker ID stays outside `<d>`. Inside `<d>`, include only the language tag and exact spoken words.

For a Mandarin Chinese project, every audible dialogue, narration, inner monologue, and off-screen human voice uses `<d>[Chinese] ...</d>`. English descriptive prose is instruction-only and must never be spoken or substituted for Chinese dialogue.

### Default rules

- Ordinary dialogue defaults to `SUBTLE_LIPSYNC`.
- Use small lip openings and minimal jaw displacement.
- Do not visibly over-articulate every syllable.
- During pauses, lips return toward closed or near-closed rest.
- Carry performance primarily through eyes, gaze, breath, brows, posture, hands, and reaction latency.
- Voice may remain clear and foregrounded without visually strong articulation.
- Non-speakers keep relaxed closed or near-closed lips.
- Narration, inner monologue, and off-screen thought default to `CLOSED_LIPS` for visible characters.

### Lip-motion levels

| Mode | Use | Visible motion |
|---|---|---|
| `CLOSED_LIPS` | narration, inner monologue, non-speakers | no dialogue articulation |
| `SUBTLE_LIPSYNC` | default cinematic dialogue | small lip motion, mostly stable jaw |
| `NATURAL_LIPSYNC` | ordinary conversation | natural articulation without over-enunciation |
| `EMPHATIC_LIPSYNC` | heated argument or deliberate emphasis | moderately stronger articulation |
| `SHOUT_OR_SING` | shouting, screaming, singing | large openings allowed only here |

### Dialogue timing

Prefer:

`reaction / inhale → speech → short pause → mouth settles → reaction`

If a line is too long, prioritize splitting it across generation clips, adding time, and keeping the original speaker visually dominant. Do not default to carrying a long off-screen line across another character's full frontal face.

### Safe listener reactions

When speech is still active, prefer the listener's back-of-head, shoulder, hands, or environment inserts. A full listener face is safest after the active speaker finishes. If a listener face must remain visible during speech, explicitly declare `MUTE_LISTENER / CLOSED_LIPS / no speech / no phoneme motion` and keep the mouth away from the focal center.

### Voiceover

Reuse the same stable speaker ID for the same character and use the exact phrase `says in an off-screen voiceover`. Immediately state that the corresponding on-screen lips remain completely closed. Independent narration gets its own stable `(Sx)` ID.

### Camera guidance

Prefer medium close-ups, three-quarter angles, or natural eye-level framing. In multi-character dialogue, camera design serves speaker ownership first. In high-reliability mode, each generated clip has one dialogue owner and a speaker change starts a new clip.

### Conditional negatives

Mouth-motion risk:

`exaggerated lip movement, over-articulated speech, large repetitive mouth opening, excessive jaw pumping, chewing-like dialogue motion, continuous mouth motion during pauses`

Wrong-speaker risk:

`wrong speaker, voice swap, dialogue ownership transfer, non-speaker lip-sync, multiple mouths sharing one line`

Mandarin language drift:

`English speech, English dialogue, translated dialogue, prompt text read aloud`

Do not add these negatives to silent shots.
