---
name: minimax-h3-director-os
version: 2.3.0
description: Use when creating, adapting, continuing, reviewing, or repairing MiniMax H3 video prompts from ideas, scripts, novels, shot lists, reference images/video/audio, accepted previous clips, dialogue scenes, recurring locations, action scenes, or schemaVersion 4 director.json workflows.
---

# MiniMax H3 Director OS V2.3.0

A director-first, H3-native prompt compiler. Preserve the right information at the right layer so H3 receives a clear audiovisual job instead of a repeated production bible.

V2.3 adds a hard semantic-scope rule:

> **The Director may know the whole story. H3 may see only the current shot.**

## Core doctrine

1. **Official H3 contract is the hard floor.** Preserve official prompt sections, reference labels, dialogue markup, speaker syntax, and timing notation.
2. **Direct first, compile second.** Resolve narrative/visual job, blocking, performance, physical causality, camera intent, lighting, sound, reference authority, and endpoint before final H3 prose.
3. **Temporal firewall is a hard gate.** Never expose future scenes, characters, injuries, wardrobe states, props, transformations, reveals, dialogue, or references to the current H3 generation merely because they exist later in the story.
4. **Accepted footage beats planned footage.** The observed end of an accepted previous clip controls the next instantaneous opening state when it belongs to the same valid continuity chain.
5. **One clip, one dominant job.** Prefer one main task, one dominant action, one dominant camera behavior, one environment response, and one readable endpoint per generation.
6. **Blocking before camera.** Define subject start → path → interaction → end, then choose camera movement.
7. **Observable language only.** Translate emotion, cinematic quality, power, tension, beauty, or scale into visible or audible behavior.
8. **Prompt Budget Engine is executable.** Keep Director knowledge, runtime invariants, current-shot variables, references, and handoff state separate; reject global-prompt dominance.
9. **References are routed per shot.** Asset availability does not grant runtime authority. Only current-scene/current-character/current-state references enter `ACTIVE_REFERENCE_SET`.
10. **Character identity and character state are separate.** A stable face/voice identity must not drag a future injury, bandage, costume damage, age/state change or prop state backward in time.
11. **Targeted negatives only.** Add failure constraints only when the current shot activates that risk. Do not introduce detailed future nouns merely to negate them.
12. **Audio clarity does not require strong mouth motion.** Ordinary dialogue defaults to `SUBTLE_LIPSYNC`.
13. **Dialogue density is validated before compilation.** Dense speech is split or given more real speech time; it is not solved by demanding faster or stronger mouth motion.
14. **Speaker IDs never go inside `<d>`.** Use `(S1) says: <d>[Chinese] 中文台词。</d>`; inside `<d>` keep only the language tag plus exact spoken words.
15. **One generated dialogue clip defaults to one dialogue owner.** Declare one `ACTIVE_SPEAKER`; every other visible person is a `MUTE_LISTENER` unless overlapping dialogue is explicitly required.
16. **Do not hand long off-screen speech to another full visible face.** If a speaker leaves the visible focal position, split the generation or hide the listener's mouth with back/shoulder/environment coverage.
17. **Recurring locations require a `SCENE_ID`.** Lock geometry, anchor objects, camera axis, material identity, light direction, time phase, and current persistent state.
18. **Returning to an old scene is a re-anchor, not a continuation from a foreign scene.** After montage/dream/flashback/location change, use the canonical scene anchor or restate the compact scene lock and disable incorrect cross-scene relay.
19. **Language lock is explicit.** In a Mandarin project, every audible dialogue, narration, inner monologue, and off-screen human voice uses `<d>[Chinese] ...</d>`; English scene prose is instruction-only and must never be spoken aloud.
20. **Repair by simplification before decoration.** Remove semantic conflict, reduce entities/actions, lock current speaker/scene/state/reference ownership, clarify endpoint, simplify camera, then retry or split.

## Load map

Load only what the task needs:

- Final H3 field/mode formatting → [H3 Native Output](references/h3-native-output.md)
- Human realism, character lock, micro-performance, camera/light → [Cinematic Production](references/cinematic-production.md)
- Fight, chase, force, collision, spell, destruction, VFX → [Performance, Action & VFX](references/performance-action-vfx.md)
- Dialogue, narration, speaker identity, language lock, mix → [Audio Identity](references/audio-identity.md)
- Visible speaking characters, lip/jaw amplitude, dialogue density, voiceover mouth behavior → [Natural Dialogue Motion](references/dialogue-motion.md)
- Wrong-speaker prevention and recurring-location consistency → [Speaker Ownership & Scene Lock](references/speaker-scene-lock.md)
- Current-shot semantic isolation, future-beat/state protection, prompt-prefix whitelist → [Shot Scope Compiler](references/shot-scope-compiler.md)
- Per-shot asset filtering and reference authority → [Reference Router](references/reference-router.md)
- I2V, references, continuation, long-form state → [Reference & Continuity](references/reference-continuity.md)
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

### 3. Separate Director knowledge from runtime H3 knowledge

Director-side knowledge may contain:

- complete story/episode outline;
- complete character registry;
- all character temporal states;
- complete Scene Bible;
- all future props/injuries/reveals/dialogue;
- the complete asset/reference library;
- canonical and historical continuity records.

This information is not automatically runtime prompt content.

Before every generation build `ACTIVE_SHOT_SCOPE` using [Shot Scope Compiler](references/shot-scope-compiler.md).

Runtime H3 receives only:

- current `SCENE_ID` and compact current `SCENE_LOCK`;
- current visible/audible characters;
- current valid character states;
- current active props;
- one `ACTIVE_SPEAKER` when dialogue exists;
- current action/camera/light/audio job;
- valid continuity handoff;
- current active references;
- exact current dialogue/narration;
- local failure constraints.

### 4. Prompt Budget Engine

Use three layers.

**A. Runtime-global invariants — whitelist only**

May include only clauses that truly apply to every shot, for example:

- spoken-language lock;
- universal H3 dialogue syntax;
- compact one-speaker ownership rule;
- genuinely universal period/style realism;
- genuinely universal subtitle/watermark exclusions.

Do not put the complete character registry, complete Scene Bible, future states, plot outline or reference registry here.

**B. Current shot variables**

- opening state;
- current `SCENE_ID` and compact `SCENE_LOCK`;
- current character state/version;
- `ACTIVE_SPEAKER` / `MUTE_LISTENER`;
- active references and their authority;
- narrative/visual job;
- action/performance progression;
- camera intent and endpoint;
- local light/VFX/sound;
- exact spoken line(s);
- stable ending state;
- local negatives.

**C. Handoff state**

- accepted end pose and screen position;
- unfinished action/camera/audio phase;
- active speaker ownership boundary;
- prop ownership/condition;
- current persistent injury/environment damage;
- scene geometry and anchor-object state;
- light/time/weather phase;
- completed dialogue/beat and reserved future beat.

Flag `GLOBAL_PROMPT_DOMINANCE` when global text semantically overwhelms the current shot.

### 5. Character state resolver

Keep stable identity separate from temporal state.

Example:

```text
CHARACTER_ID = YUYUE_17
IDENTITY = same face, age, body proportions, hair identity, voice family
STATE_ID = PRE_ACCIDENT
STATE = uninjured; forehead uncovered; no gauze; current wardrobe intact
```

Later:

```text
CHARACTER_ID = YUYUE_17
STATE_ID = POST_WAKE
STATE = same identity; forehead wrapped with gauze; slightly pale after injury
```

Never allow a future-state canonical portrait to redefine an earlier current state.

### 6. Reference Router

Use [Reference Router](references/reference-router.md) to build `ACTIVE_REFERENCE_SET`.

Assign authority per controlled dimension:

- `<Subject N>` → persistent identity of person/object/place/action concept.
- `<Picture N>` → target frame, storyboard, composition, first/last-frame or canonical-scene anchor.
- `<Video N>` → edit source, continuation source, motion/blocking/camera/timing reference.
- `<Audio N>` → voice, exact audio reuse, rhythm/timing, music, or continuation audio.

Per dimension, choose one winner: `identity`, `age/anatomy`, `hair`, `wardrobe`, `prop`, `environment`, `composition`, `motion`, `camera`, `timing`, `voice`, `music`, `style`.

Dialogue-shot conservative priority:

1. active-speaker identity/state;
2. current-scene anchor when needed;
3. visible listener identity/state;
4. optional wardrobe/prop/composition/motion references only when they solve a current control problem.

More references are not automatically safer.

### 7. First-frame spatial audit

For I2VA or any clip beginning from an actual image/final frame, inspect foreground/midground/background, subject position/orientation, doors/paths/obstacles, camera side/height, plausible entrances/exits, and light direction. Do not invent inaccessible geometry or people with no plausible entrance.

### 8. Scene Lock Registry

For every recurring location define a stable `SCENE_ID` and Director-side scene record.

Lock:

- room/location geometry;
- fixed anchor objects and relative positions;
- entrances/exits and traversable paths;
- camera axis/common side;
- wall/floor/major material identity;
- primary light source/direction/temperature/time phase;
- persistent damage, dirt, moved props, weather or other **currently valid** state.

The full Scene Bible remains Director knowledge. Each current shot receives only its active scene's compact `SCENE_LOCK`.

After the first accepted view of a recurring scene, treat its most stable spatially informative frame as `CANONICAL_SCENE_ANCHOR`.

Adjacent shots in the same scene may continue from accepted tail frames. When returning after a montage, dream, flashback, time jump or another `SCENE_ID`, do not inherit the foreign-scene tail. Re-anchor from the canonical scene picture/reference when available; otherwise explicitly compile:

```text
RE-ANCHOR SCENE_ID = BEDROOM_A. Restore the canonical room geometry, prop positions, material identity and light direction. Ignore the immediately previous foreign-scene geometry.
```

### 9. Blocking and performance

Write bodies as a cause-and-effect chain:

`initial state → preparation → support/weight shift → main action → contact/reaction → secondary motion → stable endpoint`

Use micro-performance where useful: eyeline, breath, swallow, jaw, fingers, shoulders, posture, reaction latency, hair/cloth settling. Non-focus characters stay quiet unless the story gives them a job.

### 10. Canonical dialogue compiler

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

### 11. ACTIVE_SPEAKER ownership

For a dialogue clip, compile an explicit ownership block near the beginning:

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
- if multi-speaker dialogue is explicitly required, give each editorial phase one active speaker, never overlapping mouths, and use a clear speaker-handoff boundary.

### 12. Dialogue Density Gate

Before final timing, calculate:

```text
speech_density = spoken_Han_characters / available_speech_seconds
```

Production heuristic, not an official H3 limit:

- `<=5.0 chars/s` → PASS;
- `>5.0–5.5` → CAUTION;
- `>5.5–6.5` → SPLIT_RECOMMENDED;
- `>6.5` → HARD_SPLIT by default.

Complex acting, emotional pauses, multi-person staging or strong physical action should be more conservative.

On `DIALOGUE_DENSITY_OVERLOAD`, split at a natural semantic boundary, add actual speech time or simplify simultaneous action. Do not solve overload by demanding faster delivery or stronger mouth movement.

### 13. Off-screen dialogue safety

Do not default to:

`speaker A begins → cut to listener B's full frontal face → A continues a long off-screen line`.

If off-screen speech is unavoidable:

- hide the listener's mouth using back-of-head, shoulder, hand or environment coverage;
- compile `ALL VISIBLE MOUTHS = CLOSED_LIPS`;
- keep the original speaker's spatial audio origin explicit;
- keep the off-screen portion short;
- if reliability matters more than edit variety, split to a new clip and keep the original speaker visually dominant.

### 14. Spoken-language lock

For a Mandarin Chinese project, add a compact project-level constraint:

```text
All audible human speech must be Mandarin Chinese. Never translate Chinese dialogue, narration, inner monologue, or off-screen speech into English. English descriptive prose is instruction-only and must never be spoken aloud.
```

Every audible line must still carry its own `<d>[Chinese] ...</d>` tag.

If language drift appears, add only to speaking shots:

`English speech, English dialogue, translated dialogue, prompt text read aloud`

### 15. Natural dialogue motion

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

### 16. Voiceover and narration

Use the exact phrase `says in an off-screen voiceover`.

Same character:

```text
The woman (S1) says in an off-screen voiceover: <d>[Chinese] 中文内心独白。</d> while her on-screen lips remain completely closed.
```

Independent narrator:

```text
The narrator (S5) says in an off-screen voiceover: <d>[Chinese] 中文旁白。</d> All visible characters' lips remain completely closed.
```

### 17. Camera and light

Camera contract:

`shot scale + angle + primary movement + speed/amplitude if meaningful + subject relationship + endpoint`

Prefer one primary movement. Preserve axis, screen direction, eyelines, and inherited movement phase.

Light must have a source. In a recurring scene, the main light source/direction is part of `SCENE_LOCK` and must not drift unless the story explicitly changes time or lighting.

### 18. Action, combat and VFX

For ordinary action, specify direction, mass, support, path, force, reaction, recovery.

For combat:

`prepare/weight → attack → counter → contact → feedback → recovery/endpoint`

Use `LIGHT`, `HEAVY`, `ULTIMATE` only when useful. Every major VFX must answer source, spatial anchor, trajectory, collision/environment interaction, persistence, and decay.

### 19. Adaptive timeline

- 4–6s → usually one continuous shot, one main action, one result.
- 7–9s → one shot with 2 phases, or 2 shots only for a real information change.
- 10–12s → 2–3 meaningful phases/shots.
- 13–15s → up to 3–4 meaningful phases/shots when genuinely needed.

`[Shot 1]` has no timestamp. Later editorial shots use strictly increasing `At MM:SS.mmm` start times.

A speaker change is a strong reason to split generations even when total duration would otherwise fit one clip.

### 20. Long-form segmentation

Split at completed micro-events, stable poses/compositions, reactions/value turns, intentional edits, speaker-handoff barriers, scene-return barriers, state-transition barriers, or clean continuation phases.

From segment two onward, accepted footage/final frame controls the opening instantaneous state only when it belongs to the same continuity chain. Canonical references continue to control identity. Completed dialogue/actions do not replay. Future beats do not leak backward.

### 21. Semantic negatives

Negative prompts are local risk controls, not a second story bible.

Prefer abstract categories such as:

- `location substitution`;
- `unmotivated scene change`;
- `temporal state drift`;
- `wrong speaker`;
- `non-speaker lip-sync`;
- `identity drift`.

Do not write detailed future nouns merely to negate them, e.g. `no future bedroom, no future grandmother, no future bandage`. This still introduces those concepts.

### 22. Preflight Linter

Before final prompt or `.director.json` emission, check every shot for:

- `SCOPE_LEAK`;
- `FUTURE_BEAT_LEAK`;
- `CHARACTER_STATE_CONFLICT`;
- `INACTIVE_CHARACTER_LEAK`;
- `FUTURE_REFERENCE_LEAK`;
- `REFERENCE_OWNER_MISMATCH`;
- `GLOBAL_PROMPT_DOMINANCE`;
- `ENTITY_SCOPE_OVERLOAD`;
- `SPEAKER_OWNERSHIP_CONFLICT`;
- `DIALOGUE_DENSITY_OVERLOAD`;
- `SCENE_RELAY_CONFLICT`;
- `NEGATIVE_SEMANTIC_LEAK`.

Repair, simplify or split hard failures before emission.

### 23. Compile

Use [H3 Native Output](references/h3-native-output.md) and preserve exact field names/order.

If the user explicitly asks for `schemaVersion: 4` `director.json`, compile the same per-shot H3 prompt inside that container via [Director JSON v4](references/director-json-v4.md).

Recommended long-form compile order:

`story bible → timeline resolver → character-state resolver → scene resolver → ACTIVE_SHOT_SCOPE → reference router → speaker ownership → dialogue density gate → continuity/relay resolver → prompt budget → preflight linter → H3 runtime prompt → director.json adapter`

## Targeted negative routing

Activate only relevant families:

- Identity → face/age/hair/wardrobe/prop drift.
- Anatomy → malformed hands, impossible joints/proportions.
- Motion → teleporting, foot sliding, jitter, action restart.
- Interaction → clipping, floating props, contact without reaction.
- Camera/continuity → axis reversal, camera jump, reset of inherited movement.
- Scene consistency → scene redesign, room layout drift, prop relocation, doorway/window relocation, furniture replacement, light-direction drift, wall-material drift, spatial reset, location substitution.
- Temporal state → temporal state drift, unexplained state change.
- Digital-human → wax/plastic skin, doll eyes, helmet hair, mannequin motion.
- VFX/combat → source-less particles, unreadable contact, effect drift, damage auto-repair.
- Audio identity → wrong speaker, voice drift, non-speaker lip-sync, multiple mouths sharing one line, dialogue masked by music/SFX.
- Chinese language drift → English speech, translated dialogue, prompt text read aloud.
- Ordinary dialogue mouth motion → exaggerated lip movement, over-articulated speech, large repetitive mouth opening, excessive jaw pumping, chewing-like dialogue motion, continuous mouth motion during pauses.
- Text → unwanted subtitles, logos, watermarks, random UI/text.

Do not add speaking-related negatives to silent shots. Do not use detailed inactive/future entities as negatives.

## QC before delivery

Check observable contracts:

- mode and output fields match;
- one dominant clip job exists;
- current runtime prompt contains only the active scene/entities/states;
- no future beat/state/reference leakage exists;
- current character state matches story time;
- active references belong to the current shot and have unambiguous authority;
- active speaker is not visually outvoted by another character's reference stack;
- action has start, causal path, reaction, endpoint;
- camera move has reason and endpoint;
- first-frame geography is physically possible;
- recurring location has a stable `SCENE_ID` and compact current `SCENE_LOCK`;
- returning to a scene uses re-anchor logic rather than a foreign-scene tail;
- no `<d>[Chinese][Sx] ...</d>` pattern exists;
- every speaker ID is outside `<d>`;
- every Mandarin audible line uses `<d>[Chinese] ...</d>`;
- each dialogue clip has one `ACTIVE_SPEAKER` by default;
- every other visible person is a `MUTE_LISTENER`;
- no long off-screen line is placed over another full visible speaking-capable face by default;
- dialogue density fits the actual speech window or is split;
- narration/inner monologue uses canonical voiceover wording and closed visible lips;
- ordinary visible dialogue defaults to `SUBTLE_LIPSYNC` unless stronger articulation is justified;
- VFX has source and physical interaction;
- persistent current damage survives when required;
- completed action/dialogue does not replay;
- timecodes fit duration and rise strictly;
- negatives are local rather than encyclopedic.

For failed output, use [QC & Repair](references/qc-repair.md).

## Final response behavior

- If the user asks only for the final prompt, output only the copy-ready prompt.
- If the user asks for options, keep each option executable.
- If the user asks for a long project, return segment mapping + copy-ready prompts + explicit handoff state.
- If the user asks for `director.json`, output valid JSON in the established schema and preserve shot IDs on revisions unless asked to renumber.
- Never promise deterministic success; identify high-risk speaker-handoff, semantic-scope and scene-return shots and simplify them when needed.
