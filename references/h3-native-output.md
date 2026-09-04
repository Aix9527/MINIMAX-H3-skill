# H3 Native Output Contract

This module preserves MiniMax H3's official prompt-writing shape. Director logic may enrich the content, but must not rename the fields or invent a competing schema.

## Public model baseline

MiniMax H3 is an omni-modal video model that can understand text, images, video and audio, generate native stereo audio with video, and supports clips up to 15 seconds. Public MiniMax material lists output duration as 4–15 seconds; a specific local or custom workflow may impose a narrower range, which wins for that runtime.

Official upstream references:

- https://github.com/MiniMax-AI/MiniMax-H3
- https://github.com/MiniMax-AI/MiniMax-H3/tree/main/skills/h3-prompt-writing
- https://www.minimax.io/news/minimax-h3-open-source

## Base modes

Use for T2VA, I2VA, FL2VA and L2VA. Exact order:

```text
integrated_multimodal_description: ...

overall_soundscape: ...

non_diegetic_music: ...
```

`integrated_multimodal_description` carries visual action, camera, dialogue, synchronous active sound events, shot timing and image-alignment instructions.

`overall_soundscape` carries diegetic/nonverbal ambience, room tone, foley and action sounds. Do not repeat the dialogue or the audience-only score here.

`non_diegetic_music` carries only audience-only score. If none is desired, state a clean no-score intent rather than inventing music.

### Shot timing

- First shot: `[Shot 1] ...` with no timestamp.
- Later editorial shots: `[Shot 2] At 00:04.000, ...`
- Times are shot start times, strictly increasing, inside the target duration.
- Do not create a new `[Shot N]` just to mark a phase inside a continuous take.

### Dialogue

Assign stable speaker labels `(S1)`, `(S2)` by first spoken appearance. Put spoken content inside:

```text
<d>[Chinese] 原始台词</d>
```

Preserve user-supplied dialogue, lyrics and requested visible text exactly unless the user asks for rewriting.

### I2VA

The picture is the target first frame. Begin from what is actually visible. Describe forward evolution; do not redescribe a conflicting initial composition.

### FL2VA

The first picture is the first-frame target and the last picture is the last-frame target. The motion path must progressively close the visible difference and arrive at the last frame at the end, not teleport there in the final instant.

### L2VA

Infer a plausible opening and converge toward the provided last frame. Do not accidentally treat the last frame as a first-frame reference.

## Ref2VA / full-reference mode

Use exact section order:

```text
subject_definitions:
...

summary:
...

retention_analysis:
...

detailed_description:
...

overall_soundscape:
...

non_diegetic_music:
...
```

Reference labels keep one meaning across every section.

### Reference semantics

- `<Subject N>` — persistent subject identity/concept as defined from source material.
- `<Picture N>` — specific picture/keyframe/composition relation.
- `<Video N>` — source video or temporal/camera/action relation.
- `<Audio N>` — explicit audio reuse/reference relation.

Do not create an `<Audio N>` merely because an uploaded video happens to contain audio; define it only when the audio signal has an explicit role.

`retention_analysis` must say what is copied/referenced/changed and what must not transfer. Natural-language relationships are part of H3's control surface; make ownership unambiguous.

## Language

For workflows based on the official prompt-writing guide, write the rewrite sections in English while preserving dialogue, lyrics and exact visible scene text in their original language. If a user's target runtime is already proven to accept Chinese production prompts and they explicitly want Chinese, follow that runtime/user requirement without changing official field names.
