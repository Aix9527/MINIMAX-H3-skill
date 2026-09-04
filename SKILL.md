---
name: minimax-h3-director-os
version: 2.2.0
description: Use when creating, adapting, continuing, reviewing, or repairing MiniMax H3 video prompts from ideas, scripts, novels, shot lists, reference images/video/audio, accepted previous clips, dialogue scenes, recurring locations, action scenes, or schemaVersion 4 director.json workflows.
---

# MiniMax H3 Director OS V2.2.0

A director-first, H3-native prompt compiler. Preserve the right information at the right layer so H3 receives a clear audiovisual job instead of a giant repeated production bible.

## Core doctrine

1. **Official H3 contract is the hard floor.** Preserve official prompt sections, reference labels, dialogue markup, speaker syntax, and timing notation.
2. **Direct first, compile second.** Resolve narrative/visual job, blocking, performance, physical causality, camera intent, lighting, sound, reference authority, and endpoint before final H3 prose.
3. **Accepted footage beats planned footage.** The observed end of an accepted previous clip controls the next instantaneous opening state.
4. **Blocking before camera.** Define subject start → path → interaction → end, then choose camera movement.
5. **One clip, one dominant job.** Prefer one main task, one dominant action, one dominant camera behavior, one environment response, and one readable endpoint per generation.
6. **Observable language only.** Translate emotion, cinematic quality, power, tension, beauty, or scale into visible or audible behavior.
7. **Prompt Budget Engine.** Keep project invariants, shot variables, and handoff state separate.
8. **Targeted negatives only.** Add failure constraints only when the current shot activates that risk.
9. **Audio clarity does not require strong mouth motion.** Ordinary dialogue defaults to `SUBTLE_LIPSYNC`.
10. **Speaker IDs never go inside `<d>`.** Use `(S1) says: <d>[Chinese] 中文台词。</d>`; inside `<d>` keep only the language tag plus exact spoken words.
11. **One generated dialogue clip defaults to one dialogue owner.** Declare one `ACTIVE_SPEAKER`; every other visible person is a `MUTE_LISTENER` unless the user explicitly requires overlapping dialogue.
12. **Do not hand long off-screen speech to another full visible face.** If a speaker leaves the visible focal position, split the generation or hide the listener's mouth with back/shoulder/environment coverage.
13. **Recurring locations require a `SCENE_ID`.** Lock geometry, anchor objects, camera axis, material identity, light direction, time phase, and persistent damage.
14. **Returning to an old scene is a re-anchor, not a continuation from a foreign scene.** After montage/dream/flashback/location change, use the canonical scene anchor or restate the compact scene lock and disable incorrect cross-scene relay.
15. **Language lock is explicit.** In a Mandarin project, every audible dialogue, narration, inner monologue, and off-screen human voice uses `<d>[Chinese] ...</d>`; English scene prose is instruction-only and must never be spoken aloud.
16. **Repair by simplification before decoration.** Remove conflict, reduce action, lock speaker/scene/identity, clarify endpoint, simplify camera, then retry or split.

## Load map

Load only what the task needs:

- Final H3 field/mode formatting → [H3 Native Output](references/h3-native-output.md)
- Human realism, character lock, micro-performance, camera/light → [Cinematic Production](references/cinematic-production.md)
- Fight, chase, force, collision, spell, destruction, VFX → [Performance, Action & VFX](references/performance-action-vfx.md)
- Dialogue, narration, speaker identity, language lock, mix → [Audio Identity](references/audio-identity.md)
- Visible speaking characters, lip/jaw amplitude, voiceover mouth behavior → [Natural Dialogue Motion](references/dialogue-motion.md)
- Wrong-speaker prevention and recurring-location consistency → [Speaker Ownership & Scene Lock](references/speaker-scene-lock.md)
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
- stable voice identity and spoken language;
- stable reference ownership;
- recurring `SCENE_ID` registry;
- true global exclusions.

**Shot variables**

- opening state;
- current `SCENE_ID` and compact `SCENE_LOCK`;
- one `ACTIVE_SPEAKER` if dialogue is present;
- `MUTE_LISTENER` declarations for all other visible people;
- narrative/visual job;
- action/performance progression;
- camera intent and endpoint;
- local light/VFX/sound;
- exact spoken line(s);
- stable ending state;
- local negatives.

**Handoff state**

- accepted end pose and screen position;
- unfinished action/camera/audio phase;
- active speaker ownership must end at clip boundary unless explicitly continued;
- prop ownership/condition;
- persistent injury/environment damage;
- scene geometry and anchor-object state;
- light/time/weather phase;
- completed dialogue/beat and reserved future beat.

If a runtime has a global prompt field, put true invariants there. Otherwise include only compact invariant clauses relevant to the current clip.

### 4. Reference Contract

Assign explicit authority per controlled dimension:

- `<Subject N>` → persistent identity of person/object/place/action concept.
- `<Picture N>` → target frame, storyboard, composition, first/last-frame or canonical-scene anchor.
- `<Video N>` → edit source, continuation source, motion/blocking/camera/timing reference.
- `<Audio N>` → voice, exact audio reuse, rhythm/timing, music, or continuation audio.

Per dimension, choose one winner: `identity`, `wardrobe`, `environment`, `composition`, `motion`, `camera`, `timing`, `voice`, `music`, `style`.

### 5. First-frame spatial audit

For I2VA or any clip beginning from an actual image/final frame, inspect foreground/midground/background, subject position/orientation, doors/paths/obstacles, camera side/height, plausible entrances/exits, and light direction. Do not invent inaccessible geometry or people with no plausible entrance.

### 6. Scene Lock Registry

For every recurring location define a stable `SCENE_ID` and compact `SCENE_LOCK`.

Lock:

- room/location geometry;
- fixed anchor objects and their relative positions;
- entrances/exits and traversable paths;
- camera axis/common side;
- wall/floor/major material identity;
- primary light source/direction/temperature/time phase;
- persistent damage, dirt, moved props, weather or other state.

Repeat the compact scene lock inside every shot belonging to that scene. Do not rely only on a project-global style paragraph.

After the first accepted view of a recurring scene, treat its most stable spatially informative frame as `CANONICAL_SCENE_ANCHOR`.

Adjacent shots in the same scene may continue from accepted tail frames. When returning after a montage, dream, flashback, time jump or another `SCENE_ID`, do not inherit the foreign-scene tail. Re-anchor from the canonical scene picture/reference when available; otherwise explicitly compile:

```text
RE-ANCHOR SCENE_ID = BEDROOM_A. Restore the canonical room geometry, prop positions, material identity and light direction. Ignore the immediately previous foreign-scene geometry.
```

### 7. Blocking and performance

Write bodies as a cause-and-effect chain:

`initial state → preparation → support/weight shift → main action → contact/reaction → secondary motion → stable endpoint`

Use micro-performance where useful: eyeline, breath, swallow, jaw, fingers, shoulders, posture, reaction latency, hair/cloth settling. Non-focus characters stay quiet unless the story gives them a job.

### 8. Canonical dialogue compiler

For every audible human line, first define or reuse a stable speaker ID outside `<d>`.

Correct:

```text
The young woman with a clear Mandarin Chinese voice (S1) says: <d>[Chinese] 你到底想干什么？</d>
```

Incorrect:

```text
<d>[Chinese][S1] 你到底想干什么？</d>
```

Hard rules:

- `(S1)`, `(S2)` etc. stay outside `<d>`.
- Inside `<d>`: only `[Language]` + exact spoken content.
- Preserve the user's exact dialogue unless explicitly asked to rewrite.
- Reuse the same speaker ID across shots.
- Do not create `S1-VO` or other invented speaker markup inside `<d>`.
- For the same character's voiceover, reuse `(S1)`.
- For an independent narrator, assign a separate stable ID such as `(S5)`.

### 9. ACTIVE_SPEAKER ownership

For a dialogue clip, compile an explicit ownership block near the beginning of the shot:

```text
ACTIVE_SPEAKER = RIVAL_GIRL (S2), screen-right, three-quarter view.
Only RIVAL_GIRL (S2) may produce human dialogue audio in this clip.
YUYUE_17 (S1) is MUTE_LISTENER: no speech, lips closed, no phoneme motion.
RIVAL_GIRL (S2) says: <d>[Chinese] 中文台词。</d>
```

Rules:

- default exactly one `ACTIVE_SPEAKER` per generated clip;
- all other visible people become `MUTE_LISTENER`;
- voice spatial origin stays tied to the active speaker's screen position;
- dialogue ownership does not transfer because the camera cuts to another face;
- when Speaker ID changes, default to a new generation segment;
- if the user explicitly requests multi-speaker dialogue in one clip, give each editorial phase one active speaker, never overlapping mouths, and use a clear speaker-handoff boundary.

### 10. Off-screen dialogue safety

Do not default to:

`speaker A begins → cut to listener B's full frontal face → A continues a long off-screen line`.

This creates speaker reassignment risk.

If off-screen speech is unavoidable:

- hide the listener's mouth using back-of-head, shoulder, hand or environment coverage;
- compile `ALL VISIBLE MOUTHS = CLOSED_LIPS`;
- keep the original speaker's spatial audio origin explicit;
- keep the off-screen portion short;
- if reliability matters more than edit variety, split to a new clip and keep the original speaker visually dominant.

### 11. Spoken-language lock

For a Mandarin Chinese project, add a compact project-level constraint:

```text
All audible human speech must be Mandarin Chinese. Never translate Chinese dialogue, narration, inner monologue, or off-screen speech into English. English descriptive prose is instruction-only and must never be spoken aloud.
```

Every audible line must still carry its own `<d>[Chinese] ...</d>` tag. Do not leave narration as plain quoted Chinese inside English descriptive prose.

If language drift appears in generated video, add only to speaking shots:

`English speech, English dialogue, translated dialogue, prompt text read aloud`

### 12. Natural dialogue motion

Visible ordinary dialogue defaults to:

`lip_motion_mode = SUBTLE_LIPSYNC`

Rules:

- small lip-opening amplitude;
- minimal jaw displacement;
- no exaggerated syllable-by-syllable articulation;
- lips relax toward closed or near-closed during pauses;
- emotion is carried mainly by eyes, gaze, breath, brows, posture, hands, and reaction timing;
- audio may be clear without increasing visible mouth amplitude;
- `MUTE_LISTENER` characters stay closed or near-closed at the lips.

Available modes:

`CLOSED_LIPS < SUBTLE_LIPSYNC < NATURAL_LIPSYNC < EMPHATIC_LIPSYNC < SHOUT_OR_SING`

Prefer timing:

`reaction / inhale → speech → short pause → mouth settles → reaction`

If a line is too long, first split the line across generation segments or add time. Do not solve dense speech by putting a long off-screen voice over another character's full visible face.

### 13. Voiceover and narration

Use the exact phrase `says in an off-screen voiceover`.

Same character:

```text
The woman (S1) says in an off-screen voiceover: <d>[Chinese] 中文内心独白。</d> while her on-screen lips remain completely closed.
```

Independent narrator:

```text
The narrator (S5) says in an off-screen voiceover: <d>[Chinese] 中文旁白。</d> All visible characters' lips remain completely closed.
```

### 14. Camera and light

Camera contract:

`shot scale + angle + primary movement + speed/amplitude if meaningful + subject relationship + endpoint`

Prefer one primary movement. Preserve axis, screen direction, eyelines, and inherited movement phase.

Light must have a source. In a recurring scene, the main light source/direction is part of `SCENE_LOCK` and must not drift unless the story explicitly changes time or lighting.

### 15. Action, combat and VFX

For ordinary action, specify direction, mass, support, path, force, reaction, recovery.

For combat:

`prepare/weight → attack → counter → contact → feedback → recovery/endpoint`

Use `LIGHT`, `HEAVY`, `ULTIMATE` only when useful. Every major VFX must answer source, spatial anchor, trajectory, collision/environment interaction, persistence, and decay.

### 16. Adaptive timeline

- 4–6s → usually one continuous shot, one main action, one result.
- 7–9s → one shot with 2 phases, or 2 shots only for a real information change.
- 10–12s → 2–3 meaningful phases/shots.
- 13–15s → up to 3–4 meaningful phases/shots when genuinely needed.

`[Shot 1]` has no timestamp. Later editorial shots use strictly increasing `At MM:SS.mmm` start times.

A speaker change is a strong reason to split generations even when the total duration would otherwise fit one clip.

### 17. Long-form segmentation

Split at completed micro-events, stable poses/compositions, reactions/value turns, intentional edits, speaker-handoff barriers, scene-return barriers, or clean continuation phases.

From segment two onward, accepted footage/final frame controls the opening instantaneous state only when it belongs to the same continuity chain. Canonical references continue to control identity. Completed dialogue and actions do not replay.

### 18. Compile

Use [H3 Native Output](references/h3-native-output.md) and preserve exact field names/order.

If the user explicitly asks for `schemaVersion: 4` `director.json`, compile the same per-shot H3 prompt inside that container via [Director JSON v4](references/director-json-v4.md).

## Targeted negative routing

Activate only relevant families:

- Identity → face/age/hair/wardrobe/prop drift.
- Anatomy → malformed hands, impossible joints/proportions.
- Motion → teleporting, foot sliding, jitter, action restart.
- Interaction → clipping, floating props, contact without reaction.
- Camera/continuity → axis reversal, camera jump, reset of inherited movement.
- Scene consistency → scene redesign, room layout drift, prop relocation, doorway/window relocation, furniture replacement, light-direction drift, wall-material drift, spatial reset.
- Digital-human → wax/plastic skin, doll eyes, helmet hair, mannequin motion.
- VFX/combat → source-less particles, unreadable contact, effect drift, damage auto-repair.
- Audio identity → wrong speaker, voice drift, non-speaker lip-sync, multiple mouths sharing one line, dialogue masked by music/SFX.
- Chinese language drift → English speech, translated dialogue, prompt text read aloud.
- Ordinary dialogue mouth motion → exaggerated lip movement, over-articulated speech, large repetitive mouth opening, excessive jaw pumping, chewing-like dialogue motion, continuous mouth motion during pauses.
- Text → unwanted subtitles, logos, watermarks, random UI/text.

Do not add speaking-related negatives to silent shots.

## QC before delivery

Check observable contracts:

- mode and output fields match;
- one dominant clip job exists;
- action has start, causal path, reaction, endpoint;
- camera move has reason and endpoint;
- first-frame geography is physically possible;
- recurring location has a stable `SCENE_ID` and compact `SCENE_LOCK`;
- returning to a scene uses re-anchor logic rather than a foreign-scene tail;
- identity/reference ownership is unambiguous;
- no `<d>[Chinese][Sx] ...</d>` pattern exists;
- every speaker ID is outside `<d>`;
- every Mandarin audible line uses `<d>[Chinese] ...</d>`;
- each dialogue clip has one `ACTIVE_SPEAKER` by default;
- every other visible person is a `MUTE_LISTENER`;
- no long off-screen line is placed over another full visible speaking-capable face by default;
- narration/inner monologue uses canonical voiceover wording and closed visible lips;
- ordinary visible dialogue defaults to `SUBTLE_LIPSYNC` unless stronger articulation is justified;
- long dialogue has natural pre/post speech breathing or is split across clips;
- VFX has source and physical interaction;
- persistent damage survives when required;
- completed action/dialogue does not replay;
- timecodes fit duration and rise strictly;
- negatives are local rather than encyclopedic.

For failed output, use [QC & Repair](references/qc-repair.md).

## Final response behavior

- If the user asks only for the final prompt, output only the copy-ready prompt.
- If the user asks for options, keep each option executable.
- If the user asks for a long project, return segment mapping + copy-ready prompts + explicit handoff state.
- If the user asks for `director.json`, output valid JSON in the established schema and preserve shot IDs on revisions unless asked to renumber.
- Never promise deterministic success; identify high-risk speaker-handoff and scene-return shots and simplify them when needed.
