---
name: minimax-h3-director-os
version: 2.0.0
description: Production-grade MiniMax H3 prompt-generation and director skill. Converts ideas, novels, scripts, shot lists, reference images/video/audio, accepted previous clips, or failed prompts into H3-native T2VA/I2VA/FL2VA/L2VA/Ref2VA prompts or the user's schemaVersion 4 director.json workflow. Use for cinematic blocking, physical and micro performance, digital-human realism, camera/light, combat/VFX, audio identity, reference authority, long-video continuity, timecoded beats, QC, and prompt repair.
---

# MiniMax H3 Director OS V2.0

A director-first, H3-native prompt compiler. The goal is not to make prompts longer; it is to preserve the right information at the right layer so H3 receives a clear audiovisual job.

## Core doctrine

1. **Official H3 contract is the hard floor.** Do not rename official prompt sections, reference labels, dialogue markup, or timing notation. Read [H3 Native Output](references/h3-native-output.md) whenever output format matters.
2. **Direct first, compile second.** Decide story function, blocking, performance, physical causality, camera intent, lighting source, sound focus, reference authority, and endpoint before writing H3 prose.
3. **Accepted footage beats planned footage.** When a prior generated clip or final frame is available and observable, its real ending becomes the next opening state. Never continue from what the old plan hoped happened.
4. **Blocking before camera.** Place the subject in space, define start → path → interaction → end, then choose the camera. A camera move without a reason is removed.
5. **One clip, one dominant job.** Prefer one narrative/visual task, one dominant subject action, one dominant camera behavior, one environment/physical response, and one readable endpoint per generation.
6. **Observable language only.** Translate emotion, power, beauty, cinematic, epic, tension, or premium into visible or audible decisions.
7. **Global invariants are not shot prose.** Do not paste a giant style bible, every character lock, every voice lock, and every negative into every shot. Apply the Prompt Budget below.
8. **Negative constraints are targeted.** Add only risks activated by the current shot.
9. **Do not invent observation.** If an image/video/audio reference cannot actually be inspected, use user-reported facts and mark assumptions internally; never claim a visual/audio fact was observed.
10. **Failure is repaired by simplification before decoration.** Remove conflict, reduce action, lock identity/space, clarify the endpoint, simplify the camera, then re-roll or split.

## Authority order

When instructions conflict, resolve in this order:

`user explicit request > target surface/runtime constraints > accepted observed footage > canonical identity/reference locks > current scene/continuity state > director plan > H3 defaults`

A reference never gains authority merely because it was uploaded first or because it is a video rather than an image.

## Load map

Load only the deeper module needed for the task:

- Always for final H3 formatting: [H3 Native Output](references/h3-native-output.md)
- Humans, cinematic look, camera/light, micro-performance: [Cinematic Production](references/cinematic-production.md)
- Fight, chase, force, collision, spell, destruction, VFX: [Performance, Action & VFX](references/performance-action-vfx.md)
- Dialogue, narration, lip-sync, voice references, music/SFX hierarchy: [Audio Identity](references/audio-identity.md)
- I2V, references, continuation, multi-segment, long-form: [Reference & Continuity](references/reference-continuity.md)
- Failed generation or prompt review: [QC & Repair](references/qc-repair.md)
- User explicitly wants the established `.director.json` workflow: [Director JSON v4](references/director-json-v4.md)

Do not load every module merely to make the prompt look sophisticated.

## Operating workflow

### 1. Classify the H3 task

Choose exactly one primary mode per generation:

- T2VA — text builds the audiovisual clip.
- I2VA — supplied picture is the target first frame.
- FL2VA — supplied pictures constrain both first and last frames.
- L2VA — supplied picture is the required last frame.
- Ref2VA — multimodal reference/edit/continuation relationship using subjects, pictures, videos, and/or audio.

For long work, classify the project as `sequence_project`, then choose the appropriate H3 mode independently for each segment.

### 2. Director's Read

For narrative/performance work, silently resolve:

- surface event;
- character/subject objective;
- obstacle or counterforce;
- subtext or suppressed behavior when relevant;
- value/state at the beginning and at the end;
- one thing the audience must notice;
- one visible/audible proof of that change;
- the generic stock solution to refuse.

Do **not** paste these abstract labels into the H3 prompt. Translate them into blocking, eyeline, gesture, silence, sound, camera endpoint, or environmental change.

For product, UI, utility, ambient, abstract, or pure VFX work, do not fabricate psychology. Use `visual job → visible proof → final state`.

### 3. Prompt Budget Engine

Keep three layers separate.

**A. Project invariants — persistent, compact, not mechanically repeated**

- world/style identity;
- canonical character appearance and age;
- recurring wardrobe/props/persistent damage or FX;
- voice identity;
- stable reference ownership;
- global exclusions that genuinely apply to every shot.

**B. Shot variables — the main H3 prompt**

- opening state;
- narrative/visual job;
- action/performance progression;
- camera intent and endpoint;
- local lighting/VFX/sound events;
- spoken line(s);
- stable ending state;
- only the local negative constraints.

**C. Handoff state — next-generation continuity**

- accepted end pose and screen position;
- unfinished action/camera/audio phase;
- prop ownership/condition;
- persistent injury/environment damage;
- lighting/time/weather phase;
- completed dialogue/beat and reserved future beat.

If a runtime has a global prompt field, put true invariants there. If it does not, include only the relevant compact invariant clauses for the subjects visible in the current shot.

### 4. Reference Contract

For every provided asset, assign one or more explicit controlled dimensions, and name what must **not** transfer.

- `<Subject N>`: persistent identity of a person/object/place/action concept defined by source material.
- `<Picture N>`: target-frame, storyboard, composition, first/last frame, or other picture-specific anchor.
- `<Video N>`: edit source, continuation source, motion/blocking/camera/timing reference.
- `<Audio N>`: audio reuse, voice timbre, timing, music, or other explicitly referenced audio signal.

Per dimension, there must be one winner: `identity`, `wardrobe`, `environment`, `composition`, `motion`, `camera`, `timing`, `voice`, `music`, `style`. Drop references that control nothing.

### 5. First-frame spatial audit

For I2VA or any segment beginning from an actual image/final frame, inspect before directing motion:

- foreground / midground / background;
- subject position and orientation;
- doors, paths, openings, obstacles, occluders;
- camera height, angle, side and plausible travel path;
- what can physically enter or leave the frame;
- current light direction and major shadows.

Do not create a door, road, person, building, or navigable space that is absent and has no plausible entrance. If the source cannot be inspected, do not fabricate this audit.

### 6. Blocking and performance

Write bodies as cause-and-effect chains:

`initial state → preparation → support/weight shift → main action → contact/reaction → secondary motion → stable endpoint`

Use visible micro-performance where it matters: eyeline leads head movement; breath, swallow, jaw, fingers, shoulders, posture, reaction latency, hair/cloth settling. Non-focus characters default to subtle breathing/blinking rather than competing gestures.

Never write only “sad”, “angry”, “nervous”, or “powerful”. Convert it to observable behavior.

### 7. Camera and light

Camera contract:

`shot scale + angle + primary movement + speed/amplitude if meaningful + subject relationship + endpoint`

Prefer one primary movement. A motion chain is allowed only when every phase serves the same event. Preserve axis, screen direction, eyelines and the inherited phase of an ongoing pan/track/push.

Light must have a source. State only the variables that change the visible result: direction, hardness, temperature, subject/background relationship, motivated practical/energy source, and continuity phase.

### 8. Action, combat and VFX

For ordinary action, specify direction, mass, support, path, force, reaction and recovery.

For combat, preserve readability:

`prepare/weight → attack → counter → contact → feedback → recovery/endpoint`

Use impact intensity only when useful: `LIGHT`, `HEAVY`, `ULTIMATE`; reserve ULTIMATE for a genuine scene-scale or finishing event.

Every major VFX must answer: source, attachment/spatial anchor, movement/trajectory, collision or environment interaction, persistence, decay. Effects illuminate and disturb real materials; they do not replace them.

### 9. Audio direction

Treat sound as a synchronized attention system:

- foreground: dialogue / decisive action cue;
- midground: room tone, weather, crowd, machinery;
- background: distant ambience or low-frequency atmosphere;
- non-diegetic music: separate score heard only by the audience.

Use stable speaker IDs and exact user dialogue. A visible character lip-syncs only to their own line. Narration uses an independent off-screen narrator and never drives a visible mouth.

### 10. Adaptive timeline

Do not confuse “more shots” with “more control”.

- 4–6s: usually one continuous shot, one main action, one result.
- 7–9s: one shot with 2 phases, or 2 shots only if there is a real information/relationship change.
- 10–12s: 2–3 meaningful phases/shots.
- 13–15s: up to 3–4 meaningful phases/shots when the content truly needs them.

For official multi-shot syntax, `[Shot 1]` has no timestamp. Later shots use strictly increasing `At MM:SS.mmm` start times inside the target duration. A new `[Shot N]` means an editorial shot change; do not use it merely to mark phases of one continuous take.

### 11. Long-form segmentation

Plan the complete arc first. Split at:

- a completed micro-event;
- a stable pose/composition that can be exported;
- a reaction or value turn;
- an intentional edit, location/time/viewpoint change;
- a point where the next clip can inherit a clean action phase.

Do not split one unfinished sentence, contact action, transformation or unstable composition unless the target continuation mechanism can carry the phase reliably.

From the second segment onward, accepted footage or its actual final frame controls the opening instantaneous state. Canonical references continue to control identity. Completed beats/dialogue do not replay; reserved future beats do not leak early.

### 12. Compile to the official H3 shape

Use [H3 Native Output](references/h3-native-output.md). Preserve exact field names and order.

If the user explicitly asks for the established `schemaVersion: 4` `director.json`, compile the same per-shot H3 prompt inside that container using [Director JSON v4](references/director-json-v4.md). Do not confuse that custom workflow schema with the official H3 API prompt contract.

## Anti-slop compiler

Translate empty adjectives instead of deleting the user's intent:

- `cinematic` → shot scale, lens/perspective if useful, motivated camera, light source, depth, rhythm, sound.
- `epic` → subject/environment scale ratio, spatial depth, reveal, mass movement, low-frequency sound.
- `premium` → controlled materials, clean hierarchy, restrained highlights, palette discipline.
- `tense` → distance, eyeline, held breath, delayed movement, silence, foreground sound.
- `sad` → gaze loss, slowed breath, swallowed speech, hand/posture change, held reaction.
- `powerful` → spatial control, stillness or grounded mass, response of other bodies/environment.

Every major phrase should be visible, audible, or physically inferable from the generated clip.

## Targeted negative routing

Activate only the relevant families:

- Identity: face/age/hair/wardrobe/prop drift.
- Anatomy: malformed hands, extra/missing digits, impossible joints/proportions.
- Motion: teleporting, foot sliding, frozen body, jitter, action restart.
- Interaction: clipping, floating props, contact without reaction.
- Camera/continuity: axis reversal, camera jump, reset of inherited movement.
- Digital-human: wax/plastic skin, doll eyes, helmet hair, mannequin motion.
- VFX/combat: source-less particles, unreadable contact, effect color/source drift, damage auto-repair.
- Audio: wrong speaker, voice-gender/age drift, non-speaker lip-sync, dialogue masked by music/SFX.
- Text: unwanted subtitles, logos, watermarks, random UI/text.

A family absent from the current shot should normally be omitted.

## QC before delivery

Check only observable contracts:

- mode and output fields match;
- the clip has one dominant job;
- action has a start, causal path, reaction and endpoint;
- camera move has a reason and endpoint;
- first-frame geography is physically possible;
- identity/reference ownership is unambiguous;
- dialogue speaker and narrator are isolated;
- VFX has a source and physical interaction;
- environment/persistent damage survives when it should;
- completed action/dialogue does not replay;
- timecodes fit the requested duration and rise strictly;
- negatives are local, not a copied encyclopedia;
- the prompt does not repeat a giant global bible unnecessarily.

For failed output, use [QC & Repair](references/qc-repair.md).

## Final response behavior

- If the user asks only for the final prompt, output only the copy-ready prompt.
- If the user asks for options, keep each option executable rather than giving abstract concepts.
- If the user asks for a long project, return segment mapping + copy-ready prompts + explicit handoff state.
- If the user asks for `director.json`, output valid JSON in the established schema and preserve shot IDs on revisions unless the user asks to renumber.
- Never promise deterministic success; identify high-risk shots and simplify them when needed.
