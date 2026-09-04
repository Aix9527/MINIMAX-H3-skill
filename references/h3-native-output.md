# H3 Native Output Contract

This module preserves MiniMax H3's official prompt-writing shape. Director logic may enrich content, but must not rename official fields or invent competing dialogue syntax.

## Public model baseline

MiniMax H3 is an omni-modal video model that understands text, images, video and audio, generates native stereo audio with video, and publicly supports 4–15 second clips. A target runtime may impose narrower limits.

Official upstream references:

- https://github.com/MiniMax-AI/MiniMax-H3
- https://github.com/MiniMax-AI/MiniMax-H3/tree/main/skills/h3-prompt-writing

## Base modes

Use this exact order for T2VA, I2VA, FL2VA and L2VA:

```text
integrated_multimodal_description: ...

overall_soundscape: ...

non_diegetic_music: ...
```

`integrated_multimodal_description` carries visual action, camera, speakers, dialogue, synchronized diegetic events, shot timing and image alignment.

`overall_soundscape` carries ambience, room tone, foley and non-verbal physical sound. Do not repeat dialogue or audience-only score here.

`non_diegetic_music` carries only audience-only score.

## Shot timing

- First shot: `[Shot 1] ...` with no timestamp.
- Later editorial shots: `[Shot 2] At 00:04.000, ...`
- Times are strictly increasing shot start times inside the requested duration.
- Do not create a new `[Shot N]` merely to mark an action phase inside one continuous take.

## Canonical dialogue grammar — hard requirement

Assign stable vocal speaker IDs by spoken appearance: `(S1)`, `(S2)`, `(S3)`...

**Speaker ID, identity, action and delivery MUST remain outside `<d>`.**

Inside `<d>`, include **only** the language tag and exact spoken words.

Correct:

```text
The young woman with a quiet Mandarin Chinese voice (S1) says: <d>[Chinese] 我下一站下车。</d>
```

Incorrect:

```text
<d>[Chinese][S1] 我下一站下车。</d>
```

Incorrect:

```text
<d>[Chinese] (S1) 我下一站下车。</d>
```

Do not invent IDs such as `[S1]` inside the dialogue block or compound textual aliases such as `S1-VO` as dialogue markup. Reuse the same stable `(S1)` when the same person speaks visibly or in voiceover.

### Voiceover

Use the official wording `says in an off-screen voiceover` and immediately state that the corresponding on-screen lips remain closed.

```text
The woman (S1) says in an off-screen voiceover: <d>[Chinese] 我还记得那条路。</d> while her on-screen lips remain completely closed.
```

For an independent narrator, assign a separate stable ID such as `(S5)` and use the same voiceover grammar. State that all visible characters remain closed-lipped while the narrator speaks.

### Language locking

The language tag inside `<d>` controls the intended spoken language. Preserve source dialogue verbatim.

When the project requires one spoken language throughout, add a compact project-level hard lock, for example:

```text
All audible human speech must be Mandarin Chinese. Never translate Chinese dialogue or narration into English. English descriptive prose is instruction-only and must never be spoken aloud.
```

Do **not** translate the executable scene description into Chinese merely to force Chinese speech. The official writing guide uses English rewrite prose while preserving dialogue, lyrics and exact visible scene text in their original language.

For Mandarin projects, use `<d>[Chinese] ...</d>` on every audible dialogue, narration, inner-monologue or voiceover block. Do not leave narration as an untagged quoted sentence in descriptive prose.

## I2VA

The picture is the target first frame. Begin from what is actually visible and describe forward evolution without conflicting with the image.

## FL2VA

The first picture anchors the opening and the last picture anchors the ending. Describe the continuous motion path that progressively closes the visible difference.

## L2VA

Infer a plausible opening and converge toward the supplied last frame. Do not treat the final image as a first-frame reference.

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

- `<Subject N>` — persistent identity/concept.
- `<Picture N>` — picture/keyframe/composition relation.
- `<Video N>` — video/edit/continuation/motion relation.
- `<Audio N>` — explicit audio reuse/reference relation.

`retention_analysis` must state what transfers, what changes, and what must not transfer.

## Language of rewrite prose

For workflows based on the official prompt-writing guide, write rewrite sections in English while preserving dialogue, lyrics and exact visible scene text in their original language. If a proven runtime explicitly requires Chinese production prose, follow that runtime without changing official field names or canonical dialogue grammar.
