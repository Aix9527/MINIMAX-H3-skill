---
name: minimax-h3-director-os
version: 2.3.0
description: Use when creating, adapting, continuing, reviewing, or repairing MiniMax H3 video prompts from ideas, scripts, novels, shot lists, reference images/video/audio, accepted previous clips, dialogue scenes, recurring locations, large asset libraries, action scenes, or schemaVersion 4/5 director.json workflows.
---

# MiniMax H3 Director OS V2.3.0

A director-first, H3-native prompt compiler. The project database may be large; the context delivered to one generation must be narrow, active, and unambiguous.

## Core doctrine

1. **Official H3 contract is the hard floor.** Preserve official fields, reference labels, dialogue markup, speaker syntax, and timing notation.
2. **Direct first, compile second.** Resolve the scene job, blocking, performance, physical causality, camera, light, sound, reference authority, and endpoint before final prose.
3. **Accepted footage beats planned footage.** A real accepted ending controls the next instantaneous state when both clips belong to the same continuity chain.
4. **One clip, one dominant job.** Prefer one main event, one dominant action, one dominant camera behavior, and one readable endpoint.
5. **Project database is not model context.** The full character/scene/asset registry may exist in director metadata, but H3 receives only the active slice.
6. **ACTIVE_CONTEXT_ONLY.** Current scene, visible characters, active speaker, current continuity state, and required references only. Future inactive entities are omitted rather than negated.
7. **REFERENCE_ALLOWLIST.** Ordinary shots should usually activate only 2–4 high-value references; disable the rest when the runtime exposes a full project asset pool.
8. **One dialogue owner by default.** A speaking clip declares one `ACTIVE_SPEAKER`; every other visible person is a `MUTE_LISTENER` unless overlap is explicitly required.
9. **Audio clarity does not require strong mouth motion.** Ordinary dialogue defaults to `SUBTLE_LIPSYNC`.
10. **Recurring locations require spatial locks.** Use `SCENE_ID`, compact `SCENE_LOCK`, accepted tails, and canonical scene anchors.
11. **Returning to an old scene is a re-anchor.** Do not inherit montage/dream/foreign-scene geometry.
12. **Speaker IDs never go inside `<d>`.** Use `(S1) says: <d>[Chinese] 中文台词。</d>`.
13. **Language lock is explicit.** English descriptive prose is instruction-only and must never replace Mandarin dialogue.
14. **Repair by simplification and isolation before decoration.** Remove inactive context, conflicting references, speaker ambiguity, and scene ambiguity before adding detail.

## Load map

Load only what the task needs:

- H3 fields/modes → [H3 Native Output](references/h3-native-output.md)
- Human realism, character lock, camera/light → [Cinematic Production](references/cinematic-production.md)
- Action, fight, force, VFX → [Performance, Action & VFX](references/performance-action-vfx.md)
- Dialogue, narration, speaker identity, language, mix → [Audio Identity](references/audio-identity.md)
- Lip/jaw amplitude and visible speaking behavior → [Natural Dialogue Motion](references/dialogue-motion.md)
- Speaker ownership and recurring-location geometry → [Speaker Ownership & Scene Lock](references/speaker-scene-lock.md)
- Future-context leakage and asset over-injection → [Active Context Isolation](references/active-context-isolation.md)
- References, continuation, long-form → [Reference & Continuity](references/reference-continuity.md)
- Failed output / prompt repair → [QC & Repair](references/qc-repair.md)
- Custom director workflow → [Director JSON 4/5 Adapter](references/director-json-v4.md)

## Operating workflow

### 1. Classify the generation

Choose one primary H3 mode per clip: T2VA, I2VA, FL2VA, L2VA, or Ref2VA. A sequence project may switch modes per segment.

### 2. Director's Read

Silently resolve:

- current surface event;
- subject objective/counterforce when relevant;
- beginning and ending state;
- one thing the audience must notice;
- one visible/audible proof of change;
- one generic stock solution to refuse.

Translate abstractions into observable blocking, eyeline, gesture, sound, light, camera endpoint, or environmental response.

### 3. Separate Project Database from H3 Context

The **Project Database** may contain:

- all canonical characters and voices;
- all scenes and scene anchors;
- all props/wardrobes;
- future story beats;
- complete asset library;
- long-form continuity history.

The **H3 Current Context** must contain only:

- active `SCENE_ID`;
- visible characters in this clip;
- active speaker or voiceover source;
- current action/continuity state;
- current camera/light/audio job;
- required references;
- truly global language/quality/format rules.

Do not expose inactive future entities even with wording such as `do not show the grandmother/bedroom`. Omission is safer than negation.

### 4. Global Prompt Allowlist

`promptPrefix` and `promptSuffix` may carry only universal constraints safe for every shot, such as:

- output language;
- universal visual-quality baseline;
- universal H3 dialogue syntax;
- natural-mouth rules;
- global text/subtitle policy;
- generic continuity principles that name no future entity.

Do not put these in global model conditioning:

- full character registry;
- full scene registry;
- future plot summary;
- all voice definitions;
- all props/locations;
- descriptions of characters that are not active now.

If the runtime stores director metadata separately from model conditioning, complete registries may live there.

### 5. ACTIVE_CONTEXT_ONLY compiler

Before writing each shot, compile:

```text
ACTIVE_SCENE = current scene only
VISIBLE_CHARACTERS = current visible people only
ACTIVE_SPEAKER = one current dialogue owner when present
MUTE_LISTENER = every other visible person
CURRENT_STATE = only facts inherited into this clip
REFERENCE_ALLOWLIST = only references required now
```

Fail compilation if the current prompt contains a future `SCENE_ID`, an irrelevant future character, a future prop, or competing scene definitions.

### 6. REFERENCE_ALLOWLIST

For every enabled reference, assign its controlled dimension: identity, wardrobe, environment, composition, motion, voice, or prop.

Default ordinary shot budget:

- single-person shot → 1 main identity + 1 scene anchor; optionally 1 wardrobe/prop;
- two-person shot → 1 main identity per person + 1 scene anchor; optionally 1 essential wardrobe/prop;
- prefer roughly 2–4 high-value images rather than dozens of details.

Do not simultaneously load many eye/lip/hand/expression/turnaround images for one character when another character is also present. This can create an overpowering single-identity prior and increase identity cloning or speaker confusion.

If the director runtime exposes a full `assets` pool and supports `disabledAssetIds`, disable every non-allowlisted asset for the current shot. `disabledAssetIds: []` against a large unrelated asset pool is a high-risk state.

### 7. Scene Lock Registry

Each recurring location gets a stable `SCENE_ID` and compact `SCENE_LOCK` covering:

- spatial geometry;
- anchor-object positions;
- entrances/exits and paths;
- camera axis/common side;
- wall/floor/major material identity;
- primary light source/direction/time phase;
- persistent damage/dirt/weather/prop state.

Repeat the compact lock in every shot of that scene. Do not place other scene definitions in the same model context.

After the first accepted spatially useful frame, save it as `CANONICAL_SCENE_ANCHOR` when the runtime can use a picture/reference.

### 8. Scene Return Barrier

Re-anchor instead of cross-scene continuation when:

- returning after montage;
- returning after dream/flashback;
- returning after another `SCENE_ID`;
- time jump changes continuity source;
- geometry has drifted.

Use the canonical scene image/reference when available. Otherwise restate the compact scene lock and set the runtime continuation mechanism so the foreign-scene tail does not control geometry.

### 9. Blocking and performance

Write bodies as:

`initial state → preparation → support/weight shift → main action → contact/reaction → secondary motion → stable endpoint`

Use micro-performance only where visible: eyeline, breath, swallow, fingers, shoulders, posture, reaction latency, hair/cloth settling.

### 10. Canonical dialogue compiler

For each audible line, define/reuse a stable speaker ID outside `<d>`.

Correct:

```text
The young woman (S1) says: <d>[Chinese] 你到底想干什么？</d>
```

Incorrect:

```text
<d>[Chinese][S1] 你到底想干什么？</d>
```

Hard rules:

- `(S1)`, `(S2)` stay outside `<d>`;
- Inside `<d>`: only `[Language]` + exact spoken content;
- preserve user dialogue unless explicitly asked to rewrite;
- reuse one speaker ID for the same person;
- same-character voiceover reuses the same speaker ID;
- independent narrator gets its own stable speaker ID.

### 11. ACTIVE_SPEAKER ownership

For ordinary dialogue:

```text
ACTIVE_SPEAKER = RIVAL_GIRL (S2), screen-right, three-quarter view.
Only RIVAL_GIRL (S2) may produce human dialogue audio in this clip.
YUYUE_17 (S1) is MUTE_LISTENER: no speech, lips closed, no phoneme motion.
RIVAL_GIRL (S2) says: <d>[Chinese] 中文台词。</d>
```

Rules:

- default exactly one dialogue owner per generation;
- all other visible people are `MUTE_LISTENER`;
- voice spatial origin stays tied to the active speaker;
- a camera cut does not transfer dialogue ownership;
- when Speaker ID changes, prefer a new generation segment.

Avoid `speaker A talks → listener B full frontal face → A continues long off-screen speech`. If off-screen speech is unavoidable, hide listener mouth with back/shoulder/hand/environment coverage, close all visible mouths, keep original audio origin explicit, and keep it short.

### 12. Spoken-language lock

For Mandarin projects:

```text
All audible human speech must be Mandarin Chinese. Never translate Chinese dialogue, narration, inner monologue, or off-screen speech into English. English descriptive prose is instruction-only and must never be spoken aloud.
```

Every audible line still uses `<d>[Chinese] ...</d>`.

### 13. Natural dialogue motion

Ordinary visible dialogue:

`lip_motion_mode = SUBTLE_LIPSYNC`

Use small lip openings, minimal jaw displacement, natural pauses, and let emotion be carried mainly by eyes, gaze, breath, brows, posture, hands, and reaction timing.

`MUTE_LISTENER` characters stay closed or near-closed at the lips.

Voiceover/narration keeps visible mouths `CLOSED_LIPS`.

### 14. Camera and light

Camera contract:

`shot scale + angle + primary movement + speed/amplitude if meaningful + subject relationship + endpoint`

Prefer one primary move. Preserve axis, screen direction, eyelines, and inherited move phase. In recurring scenes, main light direction belongs to `SCENE_LOCK`.

### 15. Action, combat and VFX

Ordinary action specifies direction, mass, support, path, force, reaction, recovery.

Combat preserves:

`prepare/weight → attack → counter → contact → feedback → recovery/endpoint`

Major VFX defines source, spatial anchor, trajectory, collision/environment interaction, persistence, and decay.

### 16. Adaptive timeline

- 4–6s → usually one continuous shot, one action, one result;
- 7–9s → one shot with phases, or two editorial shots for a real information change;
- 10–12s → 2–3 meaningful phases/shots;
- 13–15s → up to 3–4 meaningful phases/shots only when needed.

Speaker changes and scene-return barriers are strong reasons to split generations.

### 17. Long-form continuity

Split at completed micro-events, stable poses, reactions/value turns, editorial cuts, speaker-handoff barriers, scene-return barriers, or clean action phases.

Accepted tail frames control only valid same-chain continuation. Canonical references continue to control identity. Completed dialogue/action does not replay.

### 18. director.json compilation

Preserve the runtime's actual custom schemaVersion. A runtime may migrate schemaVersion 4 to 5.

Use:

- global prefix/suffix → universal safe constraints only;
- `shot.prompt` → active context only;
- `disabledAssetIds` → exclude non-allowlisted project assets;
- `latentRelay` → only valid same-scene/same-chain continuation;
- scene return → re-anchor, normally no foreign-scene relay.

See [Director JSON 4/5 Adapter](references/director-json-v4.md).

## Targeted negative routing

Activate only current risks:

- Identity → face/age/hair/wardrobe drift;
- Anatomy → malformed hands/joints/proportions;
- Motion → teleporting, sliding, jitter, restart;
- Interaction → clipping, floating props, contact without reaction;
- Scene → layout drift, prop relocation, doorway/window relocation, light-direction drift, spatial reset;
- Digital human → wax skin, doll eyes, helmet hair, mannequin motion;
- VFX/combat → source-less particles, unreadable contact, damage auto-repair;
- Audio identity → wrong speaker, voice drift, non-speaker lip-sync, multiple mouths sharing one line;
- Language → English speech, translated dialogue, prompt prose read aloud;
- Mouth motion → exaggerated lips, over-articulation, jaw pumping, chewing-like speech, mouth moving during pauses;
- Text → unwanted subtitles, logos, watermarks.

Do not use negatives as a substitute for active-context omission. If a future scene should not exist now, remove it from context rather than writing `no future scene`.

## QC before delivery

Check:

- H3 field/mode contract is valid;
- one dominant clip job exists;
- `ACTIVE_CONTEXT_ONLY` contains no future scene/character/prop leakage;
- one active scene only;
- one active speaker by default;
- every non-speaker is a mute listener when visible;
- speaker IDs are outside `<d>`;
- every Mandarin audible line is tagged `[Chinese]`;
- ordinary speech uses restrained mouth motion;
- `SCENE_LOCK` matches accepted geometry;
- scene returns re-anchor correctly;
- active references control explicit dimensions;
- ordinary reference count is narrow unless the shot truly requires more;
- if a large `assets` pool exists, `disabledAssetIds` or an equivalent runtime gate excludes irrelevant assets;
- accepted tail is used only for the correct continuity chain;
- negatives are local rather than encyclopedic.

For failed output, simplify/isolate first, then use [QC & Repair](references/qc-repair.md).

## Final response behavior

- If the user asks only for final prompts, output copy-ready prompts.
- For a long project, return segment mapping + copy-ready prompts + handoff state.
- For `director.json`, preserve existing IDs and runtime schema semantics unless the user asks otherwise.
- Never promise deterministic success; identify high-risk speaker/reference/scene combinations and simplify them.
