---
name: minimax-h3-director-os
version: 2.3.1
description: Use when creating, adapting, continuing, reviewing, or repairing MiniMax H3 video prompts from ideas, scripts, novels, shot lists, reference images/video/audio, accepted previous clips, dialogue scenes, recurring locations, large asset libraries, action scenes, or schemaVersion 4/5 director.json workflows.
---

# MiniMax H3 Director OS V2.3.1

A director-first H3-native prompt compiler. The project database may be large; one generation must receive only the narrow current context, and director asset links must remain mechanically consistent.

## Core doctrine

1. **Official H3 contract is the hard floor.** Preserve official fields, reference labels, dialogue markup, speaker syntax, and timing notation.
2. **Direct first, compile second.** Resolve current scene job, blocking, performance, physical causality, camera, light, sound, reference authority, and endpoint before final H3 prose.
3. **Accepted footage beats planned footage.** A real accepted ending controls the next instantaneous state only when both clips belong to the same continuity chain.
4. **One clip, one dominant job.** Prefer one main event, one dominant action, one dominant camera behavior, and one readable endpoint.
5. **Project database is not model context.** The full character/scene/asset registry may exist in director metadata, but H3 receives only the active slice.
6. **ACTIVE_CONTEXT_ONLY.** Current scene, visible characters, active speaker, current continuity state, and required references only. Future inactive entities are omitted rather than negated.
7. **REFERENCE_ALLOWLIST.** Ordinary shots usually activate only 2–4 high-value references; disable the rest when the runtime exposes the full project asset pool.
8. **BIDIRECTIONAL_ASSET_LINK.** `shots[].disabledAssetIds` and `assets[].shotIds` must describe the same relationship in both directions.
9. **One dialogue owner by default.** A speaking clip declares one `ACTIVE_SPEAKER`; every other visible person is a `MUTE_LISTENER` unless overlap is explicitly required.
10. **Audio clarity does not require strong mouth motion.** Ordinary dialogue defaults to `SUBTLE_LIPSYNC`.
11. **Recurring locations require spatial locks.** Use `SCENE_ID`, compact `SCENE_LOCK`, accepted tails, and canonical scene anchors.
12. **Returning to an old scene is a re-anchor.** Do not inherit montage/dream/foreign-scene geometry.
13. **Speaker IDs never go inside `<d>`.** Use `(S1) says: <d>[Chinese] 中文台词。</d>`.
14. **Language lock is explicit.** English descriptive prose is instruction-only and must never replace Mandarin dialogue.
15. **Repair by simplification and isolation before decoration.** Remove inactive context, conflicting references, speaker ambiguity, scene ambiguity, and broken asset links before adding detail.

## Load map

Load only what the task needs:

- H3 fields/modes → [H3 Native Output](references/h3-native-output.md)
- Human realism, character lock, camera/light → [Cinematic Production](references/cinematic-production.md)
- Action, fight, force, VFX → [Performance, Action & VFX](references/performance-action-vfx.md)
- Dialogue, narration, speaker identity, language, mix → [Audio Identity](references/audio-identity.md)
- Lip/jaw amplitude and visible speaking behavior → [Natural Dialogue Motion](references/dialogue-motion.md)
- Speaker ownership and recurring-location geometry → [Speaker Ownership & Scene Lock](references/speaker-scene-lock.md)
- Future-context leakage and asset over-injection → [Active Context Isolation](references/active-context-isolation.md)
- `disabledAssetIds` / `shotIds` consistency → [Director Asset-Link Consistency](references/asset-link-consistency.md)
- References, continuation, long-form → [Reference & Continuity](references/reference-continuity.md)
- Failed output / prompt repair → [QC & Repair](references/qc-repair.md)
- Custom director workflow → [Director JSON 4/5 Adapter](references/director-json-v4.md)

## Operating workflow

### 1. Classify the generation

Choose one primary H3 mode per clip: T2VA, I2VA, FL2VA, L2VA, or Ref2VA. A sequence project may switch modes per segment.

### 2. Director's Read

Silently resolve current event, subject objective/counterforce when relevant, beginning/end state, the one thing the audience must notice, visible/audible proof of change, and one generic stock solution to refuse. Translate abstractions into blocking, eyeline, gesture, sound, light, camera endpoint, or environmental response.

### 3. Separate Project Database from H3 Context

The **Project Database** may contain all canonical characters/voices, all scenes/anchors, all props/wardrobes, future beats, the complete asset library, and long-form history.

The **H3 Current Context** contains only:

- active `SCENE_ID`;
- visible characters;
- active speaker/voiceover source;
- current action/continuity state;
- current camera/light/audio job;
- required references;
- truly global language/quality/format rules.

Do not expose inactive future entities even through `do not show X` wording. Omission is safer than negation.

### 4. Global Prompt Allowlist

`promptPrefix` / `promptSuffix` may carry only universal constraints safe for every shot: language, visual-quality baseline, H3 dialogue syntax, natural-mouth rules, text/subtitle policy, and generic continuity principles that name no future entity.

Do not place a full character registry, scene registry, future plot summary, voice registry, or prop/location list in global model conditioning.

### 5. ACTIVE_CONTEXT_ONLY compiler

For each shot compile:

```text
ACTIVE_SCENE = current scene only
VISIBLE_CHARACTERS = current visible people only
ACTIVE_SPEAKER = one current dialogue owner when present
MUTE_LISTENER = every other visible person
CURRENT_STATE = only facts inherited into this clip
REFERENCE_ALLOWLIST = only references required now
```

Fail if the current prompt contains a future `SCENE_ID`, irrelevant future character, future prop, or competing scene definitions.

### 6. REFERENCE_ALLOWLIST

Assign each enabled reference one controlled dimension: identity, wardrobe, environment, composition, motion, voice, or prop.

Default ordinary shot budget:

- one-person shot → 1 main identity + 1 scene anchor; optional 1 wardrobe/prop;
- two-person shot → 1 main identity per person + 1 scene anchor; optional 1 essential wardrobe/prop;
- usually 2–4 high-value images total.

Do not load a large eye/lip/hand/expression/turnaround bank for one character when another character is also present.

When the runtime exposes a full `assets` pool, calculate the allowlist first, then disable every non-allowlisted asset through `disabledAssetIds` or the runtime equivalent.

### 7. BIDIRECTIONAL_ASSET_LINK

For every asset `A` and shot `S`, enforce:

```text
A.id NOT IN S.disabledAssetIds
    ⇔
S.id IN A.shotIds
```

Compilation order is mandatory:

1. compute each shot's `REFERENCE_ALLOWLIST`;
2. generate complete `shot.disabledAssetIds` from the full asset pool;
3. rebuild every `asset.shotIds` from those disable lists;
4. discard stale `shotIds` inherited from an older wider-reference project;
5. run the asset-link validator before delivery.

A shot must never disable an asset while the asset still claims that shot in `shotIds`. That split state can surface as `未找到或已禁用素材` even when the image exists.

Before delivering schemaVersion 4/5 director JSON, run:

```bash
python scripts/validate_director_asset_links.py project.director.json
```

Repair mode:

```bash
python scripts/validate_director_asset_links.py project.director.json --repair --output fixed.director.json
```

If an alias exists in the supplied asset pack and its fingerprint matches the file SHA256, repair the relationship rather than regenerating the image.

### 8. Scene Lock Registry

Each recurring location gets a stable `SCENE_ID` and compact `SCENE_LOCK` covering geometry, anchor-object positions, entrances/exits, camera axis/common side, wall/floor/material identity, primary light direction/time phase, and persistent damage/dirt/weather/prop state.

Repeat the compact lock in every shot of that scene. Do not place other scene definitions in the same model context. Save a useful accepted frame as `CANONICAL_SCENE_ANCHOR` when possible.

### 9. Scene Return Barrier

Re-anchor after montage, dream/flashback, another `SCENE_ID`, a time-jump that invalidates the previous visual source, or observed geometry drift. Use the canonical scene image/reference when available; otherwise restate the compact scene lock and disable foreign-scene continuation.

### 10. Blocking and performance

Write bodies as:

`initial state → preparation → support/weight shift → main action → contact/reaction → secondary motion → stable endpoint`

Use micro-performance only where visible: eyeline, breath, swallow, fingers, shoulders, posture, reaction latency, hair/cloth settling.

### 11. Canonical dialogue compiler

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

### 12. ACTIVE_SPEAKER ownership

For ordinary dialogue:

```text
ACTIVE_SPEAKER = RIVAL_GIRL (S2), screen-right, three-quarter view.
Only RIVAL_GIRL (S2) may produce human dialogue audio in this clip.
YUYUE_17 (S1) is MUTE_LISTENER: no speech, lips closed, no phoneme motion.
RIVAL_GIRL (S2) says: <d>[Chinese] 中文台词。</d>
```

Default exactly one dialogue owner per generation. Voice origin remains tied to the active speaker. A camera cut does not transfer ownership. When speaker ID changes, prefer a new generation segment.

Avoid `speaker A talks → listener B full frontal face → A continues long off-screen speech`. If unavoidable, hide the listener mouth with back/shoulder/hand/environment coverage, close all visible mouths, keep original audio origin explicit, and keep it short.

### 13. Spoken-language lock

For Mandarin projects:

```text
All audible human speech must be Mandarin Chinese. Never translate Chinese dialogue, narration, inner monologue, or off-screen speech into English. English descriptive prose is instruction-only and must never be spoken aloud.
```

Every audible line still uses `<d>[Chinese] ...</d>`.

### 14. Natural dialogue motion

Ordinary visible dialogue uses `lip_motion_mode = SUBTLE_LIPSYNC`: small lip openings, minimal jaw displacement, natural pauses, and performance led mainly by eyes, gaze, breath, brows, posture, hands, and reaction timing.

`MUTE_LISTENER` characters stay closed or near-closed at the lips. Voiceover/narration keeps visible mouths `CLOSED_LIPS`.

### 15. Camera, action, VFX

Camera contract:

`shot scale + angle + primary movement + speed/amplitude if meaningful + subject relationship + endpoint`

Prefer one primary move and preserve axis, screen direction, eyelines, inherited movement phase, and recurring-scene light direction.

Ordinary action specifies direction, mass, support, path, force, reaction, recovery. Combat preserves `prepare/weight → attack → counter → contact → feedback → recovery/endpoint`. Major VFX defines source, spatial anchor, trajectory, collision/environment interaction, persistence, and decay.

### 16. Adaptive timeline and segmentation

- 4–6s → usually one continuous shot, one action, one result;
- 7–9s → one shot with phases, or two editorial shots for a real information change;
- 10–12s → 2–3 meaningful phases/shots;
- 13–15s → up to 3–4 meaningful phases/shots only when needed.

Speaker changes and scene-return barriers are strong reasons to split generations. Accepted tail frames control only valid same-chain continuation. Completed dialogue/action does not replay.

### 17. director.json compilation

Preserve the runtime's actual custom schemaVersion; a runtime may migrate schemaVersion 4 to 5.

Use:

- global prefix/suffix → universal safe constraints only;
- `shot.prompt` → active context only;
- `disabledAssetIds` → exclude non-allowlisted project assets;
- `assets[].shotIds` → rebuilt to match active asset/shot links exactly;
- `latentRelay` → valid same-scene/same-chain continuation only;
- scene return → re-anchor, normally no foreign-scene relay.

See [Director JSON 4/5 Adapter](references/director-json-v4.md).

## Targeted negative routing

Activate only current risks: identity drift, anatomy errors, motion restart/jitter, interaction clipping, scene layout/prop/light drift, digital-human artifacts, VFX contact/source errors, wrong speaker/non-speaker lip-sync, language translation, exaggerated mouth motion, unwanted text/logos/watermarks.

Do not use negatives as a substitute for active-context omission.

## QC before delivery

Check:

- H3 field/mode contract is valid;
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
- large asset pools are narrowed through `disabledAssetIds`;
- every asset/shot pair satisfies `BIDIRECTIONAL_ASSET_LINK`;
- `python scripts/validate_director_asset_links.py <file>` passes for director exports;
- accepted tail is used only for the correct continuity chain;
- negatives are local rather than encyclopedic.

For failed output, simplify/isolate first, then use [QC & Repair](references/qc-repair.md).

## Final response behavior

- If the user asks only for final prompts, output copy-ready prompts.
- For a long project, return segment mapping + copy-ready prompts + handoff state.
- For `director.json`, preserve existing IDs and runtime schema semantics unless the user asks otherwise.
- Never promise deterministic success; identify high-risk speaker/reference/scene combinations and simplify them.