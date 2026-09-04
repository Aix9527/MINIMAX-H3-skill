---
name: minimax-h3-director-os
version: 2.1.0
description: Use when creating, adapting, continuing, reviewing, or repairing MiniMax H3 video prompts from ideas, scripts, novels, shot lists, reference images/video/audio, accepted previous clips, dialogue scenes, action scenes, or schemaVersion 4 director.json workflows.
---

# MiniMax H3 Director OS V2.1

A director-first, H3-native prompt compiler. Preserve the right information at the right layer so H3 receives a clear audiovisual job instead of a giant repeated production bible.

## Core doctrine

1. **Official H3 contract is the hard floor.** Preserve official prompt sections, reference labels, dialogue markup, and timing syntax.
2. **Direct first, compile second.** Resolve narrative/visual job, blocking, performance, physical causality, camera intent, lighting, sound, reference authority, and endpoint before writing final H3 prose.
3. **Accepted footage beats planned footage.** The observed end of an accepted previous clip controls the next instantaneous opening state.
4. **Blocking before camera.** Define subject start → path → interaction → end, then choose camera movement.
5. **One clip, one dominant job.** Prefer one main narrative/visual task, one dominant action, one dominant camera behavior, one environment response, and one readable endpoint per generation.
6. **Observable language only.** Translate emotion, cinematic quality, power, tension, beauty, or scale into visible or audible behavior.
7. **Prompt Budget Engine.** Keep project invariants, shot variables, and handoff state separate.
8. **Targeted negatives only.** Add failure constraints only when the current shot activates that risk.
9. **Audio clarity does not require strong mouth motion.** Ordinary dialogue defaults to `SUBTLE_LIPSYNC`.
10. **Repair by simplification before decoration.** Remove conflict, reduce action, lock identity/space, clarify endpoint, simplify camera, then retry or split.

## Load map

Load only what the task needs:

- Final H3 field/mode formatting → [H3 Native Output](references/h3-native-output.md)
- Human realism, character lock, micro-performance, camera/light → [Cinematic Production](references/cinematic-production.md)
- Fight, chase, force, collision, spell, destruction, VFX → [Performance, Action & VFX](references/performance-action-vfx.md)
- Dialogue, narration, speaker identity, mix hierarchy → [Audio Identity](references/audio-identity.md)
- Visible speaking characters, lip/jaw amplitude, voiceover mouth behavior → [Natural Dialogue Motion](references/dialogue-motion.md)
- I2V, references, continuation, long-form → [Reference & Continuity](references/reference-continuity.md)
- Failed output or prompt review → [QC & Repair](references/qc-repair.md)
- Established `.director.json` workflow → [Director JSON v4](references/director-json-v4.md)

Do not load every module merely to make the prompt look sophisticated.

## Operating workflow

### 1. Classify the H3 task

Choose one primary generation mode per clip:

- T2VA — text builds the audiovisual clip.
- I2VA — supplied picture is the target first frame.
- FL2VA — supplied pictures constrain first and last frames.
- L2VA — supplied picture is the required last frame.
- Ref2VA — multimodal reference/edit/continuation using subjects, pictures, videos, and/or audio.

For long work, classify the project as a sequence, then choose the H3 mode independently per segment.

### 2. Director's Read

For narrative/performance work, silently resolve:

- surface event;
- subject objective;
- obstacle or counterforce;
- beginning and ending state;
- one thing the audience must notice;
- one visible/audible proof of the change;
- one generic stock solution to refuse.

Do not paste abstract labels into the prompt. Translate them into blocking, eyeline, gesture, silence, sound, camera endpoint, or environmental change.

### 3. Prompt Budget Engine

**Project invariants**

- world/style identity;
- canonical appearance and age;
- recurring wardrobe/props/persistent damage or FX;
- voice identity;
- stable reference ownership;
- true global exclusions.

**Shot variables**

- opening state;
- narrative/visual job;
- action/performance progression;
- camera intent and endpoint;
- local light/VFX/sound;
- spoken line(s);
- stable ending state;
- local negatives.

**Handoff state**

- accepted end pose and screen position;
- unfinished action/camera/audio phase;
- prop ownership/condition;
- persistent injury/environment damage;
- light/time/weather phase;
- completed dialogue/beat and reserved future beat.

If a runtime has a global prompt field, put true invariants there. Otherwise include only compact invariant clauses relevant to visible subjects.

### 4. Reference Contract

Assign explicit authority per controlled dimension. A reference must control something specific.

- `<Subject N>` → persistent identity of person/object/place/action concept.
- `<Picture N>` → target frame, storyboard, composition, first/last-frame anchor.
- `<Video N>` → edit source, continuation source, motion/blocking/camera/timing reference.
- `<Audio N>` → voice, exact audio reuse, rhythm/timing, music, or continuation audio.

Per dimension, choose one winner: `identity`, `wardrobe`, `environment`, `composition`, `motion`, `camera`, `timing`, `voice`, `music`, `style`.

### 5. First-frame spatial audit

For I2VA or any clip beginning from an actual image/final frame, inspect:

- foreground / midground / background;
- subject position and orientation;
- doors, paths, openings, obstacles, occluders;
- camera height, angle, side and plausible path;
- physical entrances/exits;
- current light direction and major shadows.

Do not invent inaccessible geometry or people with no plausible entrance.

### 6. Blocking and performance

Write bodies as a cause-and-effect chain:

`initial state → preparation → support/weight shift → main action → contact/reaction → secondary motion → stable endpoint`

Use micro-performance where useful: eyeline, breath, swallow, jaw, fingers, shoulders, posture, reaction latency, hair/cloth settling. Non-focus characters stay quiet unless the story gives them a job.

### 7. Natural dialogue motion

For visible ordinary dialogue, default to:

`lip_motion_mode = SUBTLE_LIPSYNC`

Rules:

- only the tagged speaker owns and speaks the line;
- small lip-opening amplitude;
- minimal jaw displacement;
- no exaggerated articulation of every syllable;
- lips relax toward closed or near-closed rest during pauses;
- emotion is carried mainly by eyes, gaze, breathing, brows, posture, hands, and reaction timing;
- audio may be clear and foregrounded without increasing visible mouth amplitude;
- non-speaking characters keep relaxed closed or near-closed lips;
- narration, inner monologue, and off-screen thought use `CLOSED_LIPS` for visible characters.

Available modes:

`CLOSED_LIPS < SUBTLE_LIPSYNC < NATURAL_LIPSYNC < EMPHATIC_LIPSYNC < SHOUT_OR_SING`

Escalate above `SUBTLE_LIPSYNC` only when the event genuinely requires stronger visible articulation.

Prefer dialogue timing:

`reaction / inhale → speech → short pause → mouth settles → reaction`

If a line is too long, split it, add time, cut to a listener reaction, or continue the voice off-screen. Do not solve density by making the character talk faster with larger continuous mouth motion.

For ordinary dialogue, prefer medium close-up, three-quarter angle, or natural eye-level framing. Avoid making the mouth the visual focal point unless story-critical.

### 8. Camera and light

Camera contract:

`shot scale + angle + primary movement + speed/amplitude if meaningful + subject relationship + endpoint`

Prefer one primary movement. Preserve axis, screen direction, eyelines, and inherited movement phase.

Light must have a source. State only variables that change the visible result: direction, hardness, temperature, subject/background relationship, motivated source, continuity phase.

### 9. Action, combat and VFX

For ordinary action, specify direction, mass, support, path, force, reaction, recovery.

For combat:

`prepare/weight → attack → counter → contact → feedback → recovery/endpoint`

Use `LIGHT`, `HEAVY`, `ULTIMATE` only when useful; reserve `ULTIMATE` for genuine scene-scale or finishing events.

Every major VFX must answer: source, spatial anchor, trajectory, collision/environment interaction, persistence, decay.

### 10. Audio direction

Treat sound as synchronized attention:

- foreground → dialogue / decisive action cue;
- midground → room tone, weather, crowd, machinery;
- background → distant ambience / low-frequency atmosphere;
- non-diegetic music → audience-only score.

Use stable speaker IDs and exact user dialogue. Narration is an independent off-screen bus and never drives a visible mouth.

### 11. Adaptive timeline

- 4–6s → usually one continuous shot, one main action, one result.
- 7–9s → one shot with 2 phases, or 2 shots only for a real information/relationship change.
- 10–12s → 2–3 meaningful phases/shots.
- 13–15s → up to 3–4 meaningful phases/shots when genuinely needed.

`[Shot 1]` has no timestamp. Later editorial shots use strictly increasing `At MM:SS.mmm` start times. Do not use a new `[Shot N]` merely to mark phases inside one continuous take.

### 12. Long-form segmentation

Split at completed micro-events, stable poses/compositions, reactions/value turns, intentional edits, or clean continuation phases.

From segment two onward, accepted footage/final frame controls the opening instantaneous state; canonical references continue to control identity. Completed dialogue and actions do not replay.

### 13. Compile

Use [H3 Native Output](references/h3-native-output.md) and preserve exact field names/order.

If the user explicitly asks for `schemaVersion: 4` `director.json`, compile the same per-shot H3 prompt inside that container via [Director JSON v4](references/director-json-v4.md).

## Targeted negative routing

Activate only relevant families:

- Identity → face/age/hair/wardrobe/prop drift.
- Anatomy → malformed hands, impossible joints/proportions.
- Motion → teleporting, foot sliding, jitter, action restart.
- Interaction → clipping, floating props, contact without reaction.
- Camera/continuity → axis reversal, camera jump, reset of inherited movement.
- Digital-human → wax/plastic skin, doll eyes, helmet hair, mannequin motion.
- VFX/combat → source-less particles, unreadable contact, effect drift, damage auto-repair.
- Audio identity → wrong speaker, voice age/gender drift, non-speaker lip-sync, dialogue masked by music/SFX.
- Ordinary dialogue mouth motion → exaggerated lip movement, over-articulated speech, large repetitive mouth opening, excessive jaw pumping, chewing-like dialogue motion, continuous mouth motion during pauses.
- Text → unwanted subtitles, logos, watermarks, random UI/text.

Do not add dialogue-mouth negatives to silent shots.

## QC before delivery

Check observable contracts:

- mode and output fields match;
- one dominant clip job exists;
- action has start, causal path, reaction, endpoint;
- camera move has reason and endpoint;
- first-frame geography is physically possible;
- identity/reference ownership is unambiguous;
- dialogue speaker and narrator are isolated;
- ordinary visible dialogue defaults to `SUBTLE_LIPSYNC` unless stronger articulation is justified;
- narration/inner monologue keeps visible mouths `CLOSED_LIPS`;
- long dialogue has natural pre/post speech breathing or reaction time;
- VFX has source and physical interaction;
- persistent damage survives when required;
- completed action/dialogue does not replay;
- timecodes fit duration and rise strictly;
- negatives are local rather than encyclopedic;
- the prompt does not repeat a giant global bible unnecessarily.

For failed output, use [QC & Repair](references/qc-repair.md).

## Final response behavior

- If the user asks only for the final prompt, output only the copy-ready prompt.
- If the user asks for options, keep each option executable.
- If the user asks for a long project, return segment mapping + copy-ready prompts + explicit handoff state.
- If the user asks for `director.json`, output valid JSON in the established schema and preserve shot IDs on revisions unless asked to renumber.
- Never promise deterministic success; identify high-risk shots and simplify them when needed.
