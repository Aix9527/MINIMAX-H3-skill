# Audio Identity & Narration

H3 generates audiovisual content jointly, so sound belongs on the timeline rather than being appended after the visual description.

For visible dialogue, also read [Natural Dialogue Motion](dialogue-motion.md). For wrong-speaker prevention and recurring-scene control, also read [Speaker Ownership & Scene Lock](speaker-scene-lock.md).

## Four semantic buses

1. **Dialogue** — spoken by a visible or explicitly off-screen character.
2. **Narration** — independent narrator/voiceover, never a visible character mouth.
3. **Diegetic / SFX / nonverbal** — room tone, weather, footsteps, impacts, breathing, cloth, machinery, crowd, creature sounds.
4. **Non-diegetic music** — audience-only score.

Keep these meanings separated even if the target runtime stores them in fewer fields.

## Stable speaker identity

For recurring speakers maintain an internal voice lock:

- stable speaker ID `(S1)`, `(S2)`, `(S3)`...;
- character identity;
- age range;
- pitch/register/timbre;
- pace and articulation;
- accent/language/dialect when relevant;
- delivery baseline.

Do not reassign a line because the camera cuts to another face.

## Canonical H3 dialogue ownership

This is a hard compiler rule:

- Speaker ID belongs **outside** `<d>`.
- Speaker identity/action/delivery belongs **outside** `<d>`.
- Inside `<d>`, include only `[Language]` plus the exact spoken content.

Correct:

```text
The young woman with a clear Mandarin Chinese voice (S1) says: <d>[Chinese] 你到底想干什么？</d>
```

Wrong:

```text
<d>[Chinese][S1] 你到底想干什么？</d>
```

Preserve user-supplied dialogue exactly unless asked to rewrite. Reuse the same `(S1)` when the same person speaks again, including voiceover.

## ACTIVE_SPEAKER hard lock

Default each generated dialogue clip to exactly one dialogue owner.

Compile near the start of the shot:

```text
ACTIVE_SPEAKER = YUYUE_17 (S1), screen-left, three-quarter view.
Only YUYUE_17 (S1) may produce human dialogue audio in this clip.
RIVAL_GIRL (S2) is MUTE_LISTENER: no speech, lips closed, no phoneme motion.
YUYUE_17 (S1) says: <d>[Chinese] 中文台词。</d>
```

Rules:

- Only `ACTIVE_SPEAKER` may generate human dialogue audio and visible speech articulation.
- All other visible people are `MUTE_LISTENER` unless overlapping dialogue is explicitly required.
- The voice's spatial origin remains tied to the active speaker's screen position.
- A camera cut to another face never transfers dialogue ownership.
- When the Speaker ID changes, prefer a new generation segment.
- Do not put long dialogue from one character over another character's full frontal face by default.

## Off-screen speech safety

Off-screen speech is higher risk than visible single-speaker dialogue.

Do **not** default to:

`speaker A begins speaking → cut to listener B's full frontal face → A continues a long off-screen line`.

If off-screen speech is unavoidable:

- show back-of-head, shoulder, hands, or environment rather than another complete mouth-forward face;
- explicitly compile `ALL VISIBLE MOUTHS = CLOSED_LIPS`;
- state that the audio continues from the original speaker's direction;
- keep the off-screen portion short;
- if speaker correctness matters more than edit variety, split to a new clip and keep the original speaker visible/dominant.

## Spoken-language hard lock

If a project is Chinese-language, compile every audible human line as `<d>[Chinese] ...</d>` and add a compact project-level lock:

```text
All audible human speech must be Mandarin Chinese. Never translate Chinese dialogue, narration, inner monologue, or off-screen speech into English. English descriptive prose is instruction-only and must never be spoken aloud.
```

Do not leave narration or inner monologue as plain quoted Chinese embedded in English description. Untagged quoted text is ambiguous and may be translated or ignored.

Optional Chinese-language negatives when the runtime shows language drift:

`English speech, English dialogue, translated dialogue, prompt text read aloud`

Use these only on shots with audible human speech.

## Natural dialogue motion

Audio clarity and visible articulation are separate controls.

For ordinary conversational speech:

- default `SUBTLE_LIPSYNC`;
- small lip-opening amplitude;
- minimal jaw displacement;
- no exaggerated articulation of every syllable;
- lips settle naturally toward neutral during pauses;
- eyes, gaze, breathing, brows, posture and reaction timing carry most emotional performance;
- avoid combining precise dialogue with large simultaneous head motion unless story-critical.

Other visible characters remain closed or near-closed at the lips and only perform natural listening reactions.

## Narrator and inner-voice bus

Normalize `(旁白)` / `（旁白）` as metadata, not spoken words.

### Same-character voiceover

Reuse the same speaker ID and use the exact phrase `says in an off-screen voiceover`:

```text
The woman (S1) says in an off-screen voiceover: <d>[Chinese] 大把的存款换了年轻十岁，这不划算啊。</d> while her on-screen lips remain completely closed.
```

Do not create a noncanonical dialogue identifier such as `S1-VO` inside `<d>`.

### Independent narrator

Assign a separate stable speaker ID such as `(S5)`:

```text
The independent mature Mandarin Chinese female narrator (S5) says in an off-screen voiceover: <d>[Chinese] 余悦今年十七岁。</d> All visible characters' lips remain completely closed.
```

Narration belongs in the integrated audiovisual description, not in ambient sound or audience-only music.

## Mix hierarchy

When dialogue is present:

`dialogue intelligibility > story-critical action cue > ambience > score`

Duck music and strong SFX around speech. Describe audio as clear in the foreground mix; do not translate audio clarity into visually exaggerated mouth articulation.

## Dialogue timing

Do not make speech occupy the full clip by default. Prefer:

`reaction / inhale → speech → pause → mouth settles → reaction`

If a line is too dense, first split it across generation segments or add time. Do not solve dense speech by carrying a long off-screen line across another character's full visible face.

## Camera guidance for dialogue

For ordinary dialogue, prefer medium close-up, three-quarter angle, natural eye level, or coverage that preserves the active speaker's ownership. Listener reactions are safest after the spoken line finishes or when the listener's mouth is not visibly available for reassignment.

## Audio references

Define `<Audio N>` only when it has a real role, such as voice timbre, exact audio reuse, rhythm/timing, music source, or continuation audio. State exactly what transfers and what does not.

## Conditional audio negatives

Use only when the risk exists:

- wrong speaker / voice swap;
- age/timbre drift;
- multiple mouths sharing one line;
- non-speaker lip-sync;
- dialogue ownership transfer after a camera cut;
- narration spoken by a visible character;
- swallowed/rushed dialogue;
- dialogue masked by music/SFX;
- English speech or translated dialogue in a Chinese-language project;
- prompt description being read aloud.

For ordinary dialogue with over-articulation risk, optionally add:

`exaggerated lip movement, over-articulated speech, large repetitive mouth opening, excessive jaw pumping, chewing-like dialogue motion, continuous mouth motion during pauses`

Do not add dialogue-mouth negatives to shots without visible dialogue.
