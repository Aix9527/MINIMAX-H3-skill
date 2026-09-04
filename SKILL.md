---
name: minimax-h3-director-os
version: 2.1.1
description: Use when creating, adapting, continuing, reviewing, or repairing MiniMax H3 video prompts from ideas, scripts, novels, shot lists, reference images/video/audio, accepted previous clips, dialogue scenes, action scenes, or schemaVersion 4 director.json workflows.
---

# MiniMax H3 Director OS V2.1.1

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
11. **Language lock is explicit.** In a Mandarin project, every audible dialogue, narration, inner monologue, and off-screen human voice uses `<d>[Chinese] ...</d>`; English scene prose is instruction-only and must never be spoken aloud.
12. **Repair by simplification before decoration.** Remove conflict, reduce action, lock identity/space, clarify endpoint, simplify camera, then retry or split.

## Load map

Load only what the task needs:

- Final H3 field/mode formatting → [H3 Native Output](references/h3-native-output.md)
- Human realism, character lock, micro-performance, camera/light → [Cinematic Production](references/cinematic-production.md)
- Fight, chase, force, collision, spell, destruction, VFX → [Performance, Action & VFX](references/performance-action-vfx.md)
- Dialogue, narration, speaker identity, language lock, mix → [Audio Identity](references/audio-identity.md)
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
- stable voice identity and spoken language;
- stable reference ownership;
- true global exclusions.

**Shot variables**

- opening state;
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
- prop ownership/condition;
- persistent injury/environment damage;
- light/time/weather phase;
- completed dialogue/beat and reserved future beat.

If a runtime has a global prompt field, put true invariants there. Otherwise include only compact invariant clauses relevant to the current clip.

### 4. Reference Contract

Assign explicit authority per controlled dimension:

- `<Subject N>` → persistent identity of person/object/place/action concept.
- `<Picture N>` → target frame, storyboard, composition, first/last-frame anchor.
- `<Video N>` → edit source, continuation source, motion/blocking/camera/timing reference.
- `<Audio N>` → voice, exact audio reuse, rhythm/timing, music, or continuation audio.

Per dimension, choose one winner: `identity`, `wardrobe`, `environment`, `composition`, `motion`, `camera`, `timing`, `voice`, `music`, `style`.

### 5. First-frame spatial audit

For I2VA or any clip beginning from an actual image/final frame, inspect foreground/midground/background, subject position/orientation, doors/paths/obstacles, camera side/height, plausible entrances/exits, and light direction. Do not invent inaccessible geometry or people with no plausible entrance.

### 6. Blocking and performance

Write bodies as a cause-and-effect chain:

`initial state → preparation → support/weight shift → main action → contact/reaction → secondary motion → stable endpoint`

Use micro-performance where useful: eyeline, breath, swallow, jaw, fingers, shoulders, posture, reaction latency, hair/cloth settling. Non-focus characters stay quiet unless the story gives them a job.

### 7. Canonical dialogue compiler

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

### 8. Spoken-language lock

For a Mandarin Chinese project, add a compact project-level constraint:

```text
All audible human speech must be Mandarin Chinese. Never translate Chinese dialogue, narration, inner monologue, or off-screen speech into English. English descriptive prose is instruction-only and must never be spoken aloud.
```

Every audible line must still carry its own `<d>[Chinese] ...</d>` tag. Do not leave narration as plain quoted Chinese inside English descriptive prose.

If language drift appears in generated video, add only to speaking shots:

`English speech, English dialogue, translated dialogue, prompt text read aloud`

### 9. Natural dialogue motion

Visible ordinary dialogue defaults to:

`lip_motion_mode = SUBTLE_LIPSYNC`

Rules:

- small lip-opening amplitude;
- minimal jaw displacement;
- no exaggerated syllable-by-syllable articulation;
- lips relax toward closed or near-closed during pauses;
- emotion is carried mainly by eyes, gaze, breath, brows, posture, hands, and reaction timing;
- audio may be clear without increasing visible mouth amplitude;
- non-speaking characters stay closed or near-closed at the lips.

Available modes:

`CLOSED_LIPS < SUBTLE_LIPSYNC < NATURAL_LIPSYNC < EMPHATIC_LIPSYNC < SHOUT_OR_SING`

Escalate only when the event genuinely requires stronger articulation.

Prefer timing:

`reaction / inhale → speech → short pause → mouth settles → reaction`

If a line is too long, split it, add time, cut to a listener reaction, or continue voice off-screen.

### 10. Voiceover and narration

Use the exact phrase `says in an off-screen voiceover`.

Same character:

```text
The woman (S1) says in an off-screen voiceover: <d>[Chinese] 中文内心独白。</d> while her on-screen lips remain completely closed.
```

Independent narrator:

```text
The narrator (S5) says in an off-screen voiceover: <d>[Chinese] 中文旁白。</d> All visible characters' lips remain completely closed.
```

### 11. Camera and light

Camera contract:

`shot scale + angle + primary movement + speed/amplitude if meaningful + subject relationship + endpoint`

Prefer one primary movement. Preserve axis, screen direction, eyelines, and inherited movement phase.

Light must have a source. State only variables that change the visible result.

### 12. Action, combat and VFX

For ordinary action, specify direction, mass, support, path, force, reaction, recovery.

For combat:

`prepare/weight → attack → counter → contact → feedback → recovery/endpoint`

Use `LIGHT`, `HEAVY`, `ULTIMATE` only when useful. Every major VFX must answer source, spatial anchor, trajectory, collision/environment interaction, persistence, and decay.

### 13. Adaptive timeline

- 4–6s → usually one continuous shot, one main action, one result.
- 7–9s → one shot with 2 phases, or 2 shots only for a real information change.
- 10–12s → 2–3 meaningful phases/shots.
- 13–15s → up to 3–4 meaningful phases/shots when genuinely needed.

`[Shot 1]` has no timestamp. Later editorial shots use strictly increasing `At MM:SS.mmm` start times.

### 14. Long-form segmentation

Split at completed micro-events, stable poses/compositions, reactions/value turns, intentional edits, or clean continuation phases. From segment two onward, accepted footage/final frame controls the opening instantaneous state; canonical references continue to control identity. Completed dialogue and actions do not replay.

### 15. Compile

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
- Audio identity → wrong speaker, voice drift, non-speaker lip-sync, dialogue masked by music/SFX.
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
- identity/reference ownership is unambiguous;
- **no `<d>[Chinese][Sx] ...</d>` pattern exists**;
- every speaker ID is outside `<d>`;
- every Mandarin audible line uses `<d>[Chinese] ...</d>`;
- narration/inner monologue uses canonical voiceover wording and closed visible lips;
- ordinary visible dialogue defaults to `SUBTLE_LIPSYNC` unless stronger articulation is justified;
- long dialogue has natural pre/post speech breathing or reaction time;
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
- Never promise deterministic success; identify high-risk shots and simplify them when needed.
