# Audio Identity & Narration

H3 generates audiovisual content jointly, so sound belongs on the timeline rather than being appended after the visual description.

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

## Dialogue contract

- Preserve user-supplied dialogue exactly unless asked to rewrite.
- Use stable `(S1)`, `(S2)` mapping across a connected project.
- Only the tagged speaker articulates and lip-syncs that line.
- Other visible characters keep natural non-speaking mouth behavior.
- Prefer one clear foreground speaker at a time unless overlap is explicitly scripted.
- When lip-sync is high priority, simplify head motion, complex gestures, extreme camera motion and loud competing SFX.
- Give the speaker enough time; do not speed-read a long line to fit an overloaded shot.

## Narrator bus

Normalize `(旁白)` / `（旁白）` as metadata, not spoken words. Remove the marker from the content before final generation text.

Use an independent off-screen narrator. Explicitly prevent visible characters from speaking or lip-syncing the narration when ambiguity exists.

Narration belongs in the integrated audiovisual description, not in ambient sound or the audience-only music field.

## Mix hierarchy

When dialogue is present:

`dialogue intelligibility > story-critical action cue > ambience > score`

Duck music and strong SFX around consonant-heavy speech rather than describing everything as equally loud.

When no dialogue is present, allow ambience and physical sound to lead; do not force music into every clip.

## Audio references

Define `<Audio N>` only when it has a real role, such as:

- voice timbre reference;
- exact audio reuse;
- rhythm/timing reference;
- background music source;
- edit/continuation audio context.

State which aspect transfers and which does not. A voice reference does not automatically authorize transfer of its words, music, environment or visible identity.

Runtime-specific behaviors—such as how a local ComfyUI workflow mixes reference audio with generated ambience—belong to that runtime adapter and must not be treated as a universal H3 law.

## Audio negatives are conditional

Use only when risk exists:

- wrong speaker / voice swap;
- age or gender timbre drift;
- multiple mouths sharing one line;
- non-speaker lip-sync;
- narration spoken by a visible character;
- swallowed or rushed dialogue;
- dialogue masked by music/SFX.
