# Audio Identity & Narration

H3 generates audiovisual content jointly, so sound belongs on the timeline rather than being appended after the visual description.

For visible dialogue, also read [Natural Dialogue Motion](dialogue-motion.md). Ordinary cinematic dialogue defaults to `SUBTLE_LIPSYNC`, not exaggerated visible articulation.

## Four semantic buses

1. **Dialogue** — spoken by a visible or explicitly off-screen character and potentially lip-synced.
2. **Narration** — independent narrator/voiceover, never a visible character mouth.
3. **Diegetic / SFX / nonverbal** — room tone, weather, footsteps, impacts, breathing, cloth, machinery, crowd, creature sounds.
4. **Non-diegetic music** — audience-only score.

Keep these meanings separated even if the target runtime stores them in fewer fields.

## Stable speaker identity

For recurring speakers maintain an internal voice lock:

- speaker ID / character ID;
- sex/gender presentation when relevant to casting;
- age range;
- pitch/register/timbre;
- pace and articulation;
- accent/language/dialect if requested;
- emotional range or delivery baseline.

Do not reassign a line because the camera happens to cut to another face.

## Dialogue ownership contract

- Preserve user-supplied dialogue exactly unless asked to rewrite.
- Use stable `(S1)`, `(S2)` mapping across a connected project.
- Only the tagged speaker owns and speaks the line.
- A visible speaker uses the selected lip-motion level; ordinary dialogue defaults to `SUBTLE_LIPSYNC`.
- Other visible characters keep relaxed closed or near-closed lips with natural breathing and listening reactions.
- Prefer one clear foreground speaker at a time unless overlap is explicitly scripted.
- Give the speaker enough time; do not speed-read a long line to fit an overloaded shot.
- If dialogue is too dense, split the line, extend timing, cut to a listener reaction, or continue speech off-screen rather than forcing rapid mouth motion.

## Natural dialogue motion

Audio clarity and visible articulation are separate controls.

For ordinary conversational speech:

- small lip-opening amplitude;
- minimal jaw displacement;
- no exaggerated articulation of every syllable;
- lips settle naturally toward neutral during pauses;
- eyes, gaze, breathing, brows, posture and reaction timing carry most of the emotional performance;
- avoid combining precise dialogue with large simultaneous head motion unless story-critical.

Use stronger visible articulation only when the event actually requires it: heated emphasis, shouting, screaming or singing. See [Natural Dialogue Motion](dialogue-motion.md) for the full mode table.

## Narrator and inner-voice bus

Normalize `(旁白)` / `（旁白）` as metadata, not spoken words. Remove the marker from the content before final generation text.

Narration and inner monologue default to `CLOSED_LIPS` for visible characters. Use an independent off-screen narrator or voiceover. Explicitly prevent visible characters from speaking or lip-syncing narration when ambiguity exists.

Narration belongs in the integrated audiovisual description, not in ambient sound or the audience-only music field.

## Mix hierarchy

When dialogue is present:

`dialogue intelligibility > story-critical action cue > ambience > score`

Duck music and strong SFX around speech. Describe audio as clear or intelligible in the foreground mix; do not translate audio clarity into visually exaggerated mouth articulation.

When no dialogue is present, allow ambience and physical sound to lead; do not force music into every clip.

## Dialogue timing

Do not make speech occupy the full clip by default. Prefer a visible timing shape such as:

`reaction / inhale → speech → pause → mouth settles → reaction`

For long lines, preserve readable conversational pace. If the line cannot fit naturally, restructure the shot instead of increasing visible mouth speed.

## Camera guidance for dialogue

For ordinary dialogue, prefer framing that supports performance rather than mouth inspection: medium close-up, three-quarter angle, natural eye level, or listener reaction coverage. Avoid a long frontal extreme close-up for dense dialogue unless the story specifically needs it.

## Audio references

Define `<Audio N>` only when it has a real role, such as:

- voice timbre reference;
- exact audio reuse;
- rhythm/timing reference;
- background music source;
- edit/continuation audio context.

State which aspect transfers and which does not. A voice reference does not automatically authorize transfer of its words, music, environment or visible identity.

Runtime-specific behaviors—such as how a local workflow mixes reference audio with generated ambience—belong to that runtime adapter and must not be treated as a universal H3 law.

## Audio negatives are conditional

Use only when risk exists:

- wrong speaker / voice swap;
- age or gender timbre drift;
- multiple mouths sharing one line;
- non-speaker lip-sync;
- narration spoken by a visible character;
- swallowed or rushed dialogue;
- dialogue masked by music/SFX.

For ordinary dialogue with over-articulation risk, optionally add:

`exaggerated lip movement, over-articulated speech, large repetitive mouth opening, excessive jaw pumping, chewing-like dialogue motion, continuous mouth motion during pauses`

Do not add dialogue-mouth negatives to shots without visible dialogue.