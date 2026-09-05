# Shot Scope Compiler / 当前镜头语义防火墙

This module prevents semantic leakage from the full story bible into the current MiniMax H3 generation segment.

The core rule is:

> **The Director may know the whole story. H3 may see only the current shot.**

A story bible, character registry, scene registry, future state table, or long-form outline is compiler knowledge. It is not automatically runtime prompt content.

## 1. ACTIVE_SHOT_SCOPE

Before writing H3 prose, resolve a temporary `ACTIVE_SHOT_SCOPE` for the current generation segment.

It contains only:

- `ACTIVE_SCENE` — exactly the current scene/location;
- `ACTIVE_CHARACTERS` — characters visible, audible, or physically relevant now;
- `ACTIVE_CHARACTER_STATES` — the state version valid at this point in the story;
- `ACTIVE_SPEAKER` — one dialogue owner by default;
- `ACTIVE_PROPS` — props that matter now;
- `ACTIVE_REFERENCES` — references allowed by the current Reference Router;
- current action/performance/camera/light/audio job;
- accepted handoff facts from the immediately valid continuity chain;
- exact dialogue or narration required now;
- compact local failure constraints.

Everything else remains outside the runtime prompt.

## 2. Temporal firewall

Never expose a future story fact merely because the Director knows it.

Blocked until narratively valid:

- future locations or scene identities;
- characters not yet present or relevant;
- future injuries, bandages, dirt, blood, wetness, costume damage, age/state changes;
- future props or changed prop ownership;
- future reveals, transformations, attacks, deaths, discoveries or VFX states;
- future dialogue or narration;
- references depicting a future version of a character or environment.

Do not use future concepts even as detailed negatives. Saying `no bedroom, no grandmother, no gauze` still exposes those concepts. Prefer abstract local negatives such as `location substitution, scene change, temporal state drift` and positively restate the current valid state.

## 3. Character identity is not character state

Separate long-lived identity from time-sensitive state.

Example:

```text
CHARACTER_ID = YUYUE_17
IDENTITY = same face, age, body proportions, hair identity, voice family

STATE_ID = PRE_ACCIDENT
STATE = uninjured; no forehead wound; no gauze; current wardrobe clean/intact
```

Later:

```text
CHARACTER_ID = YUYUE_17
STATE_ID = POST_WAKE
STATE = same identity; forehead wrapped with gauze; slightly pale after injury
```

A compiler may maintain validity ranges internally, for example:

```text
YUYUE_PRE_ACCIDENT: valid shot_001..shot_005
YUYUE_POST_WAKE: valid from shot_011
```

These ranges do not need to be serialized into schemaVersion 4 unless the surrounding workflow supports them. Their purpose is to prevent state leakage while compiling each shot.

## 4. Scene scope

The full Scene Bible belongs to Director/compiler knowledge.

The runtime H3 prompt receives only:

- the current `SCENE_ID`;
- a compact `SCENE_LOCK` for that scene;
- current scene-state deltas;
- a canonical scene anchor when the mode/reference system supports one.

Do not place every project scene description in `promptPrefix` or `promptSuffix`.

For an 8-second riverbank dialogue shot, a valid scene scope may be:

```text
SCENE_ID = RIVER_A
SCENE_LOCK: river frame-right; dirt path center-left; low orange sun rear-right;
same terrain, vegetation and light direction; remain continuously in this location for the full clip.
```

It must not also describe a later bedroom, dream void, hospital, grandmother, mirror, or post-injury state.

## 5. Global prompt whitelist

`promptPrefix` and equivalent global runtime fields are **whitelist-only**.

Usually allowed:

- spoken-language lock;
- universal H3 dialogue syntax rules;
- compact one-speaker ownership rule;
- genuinely universal visual treatment or period/style identity;
- genuinely universal text/subtitle/watermark exclusions;
- a compact project-wide audio-identity rule when it truly applies to every shot.

Usually forbidden:

- complete character registry;
- complete scene registry;
- future character/state descriptions;
- full story outline;
- future props, injuries, transformations, reveals or dialogue;
- complete reference registry;
- local camera/action instructions;
- negatives that only apply to some shots.

If the workflow literally concatenates prefix/suffix into every H3 prompt, treat those fields as runtime prompt text and keep them extremely small.

## 6. Prompt Budget Gate

Use the Prompt Budget Engine as a real preflight check, not just a writing preference.

Production heuristic, not an official H3 model limit:

- current-shot content should normally dominate the final runtime prompt;
- global invariant text should remain a minority of the prompt;
- if global text is longer or semantically denser than the actual shot job, simplify before emission.

Flag `GLOBAL_PROMPT_DOMINANCE` when the current shot is buried under project-wide content.

Do not optimize only by character count. Semantic diversity matters: three short descriptions of unrelated future scenes are still worse than one compact active-scene lock.

## 7. Entity Mention Budget

For short clips, keep the active semantic world small.

A normal 7–9 second dialogue shot often needs only:

- 1 scene;
- 1 active speaker;
- 0–2 listeners;
- a few immediately relevant props;
- one main action/performance job.

Flag `ENTITY_SCOPE_OVERLOAD` when the runtime prompt contains multiple inactive locations, unrelated characters, future states or story beats.

## 8. Semantic Negative Hygiene

Negative prompts must not become a second story bible.

Prefer category-level constraints:

```text
location substitution, unmotivated scene cut, temporal state drift,
wrong speaker, non-speaker lip-sync, identity drift
```

Avoid introducing inactive future nouns solely to negate them:

```text
no future bedroom, no future grandmother, no future bandage
```

When a current state must be protected, state the valid present positively:

```text
YUYUE_17 remains uninjured throughout this clip; forehead uncovered; no injury-state transition occurs.
```

Use this only when the present state is actually at risk and relevant.

## 9. Director Preflight Linter

Before emitting a final prompt or `.director.json`, check every shot for:

- `SCOPE_LEAK` — inactive scene/location enters current runtime text;
- `FUTURE_BEAT_LEAK` — future event/reveal/dialogue is exposed;
- `CHARACTER_STATE_CONFLICT` — state does not match current timeline;
- `INACTIVE_CHARACTER_LEAK` — unrelated character is injected;
- `FUTURE_REFERENCE_LEAK` — reference depicts a future/inactive state;
- `REFERENCE_OWNER_MISMATCH` — reference ownership conflicts with current subject/speaker;
- `GLOBAL_PROMPT_DOMINANCE` — project text overwhelms current shot job;
- `ENTITY_SCOPE_OVERLOAD` — too many unrelated semantic entities;
- `SPEAKER_OWNERSHIP_CONFLICT` — more than one unplanned dialogue owner;
- `DIALOGUE_DENSITY_OVERLOAD` — spoken content does not fit the available speech window;
- `SCENE_RELAY_CONFLICT` — cross-scene or re-anchor shot incorrectly inherits foreign latent/context;
- `NEGATIVE_SEMANTIC_LEAK` — negatives introduce inactive future concepts.

If a hard error is found, repair or split the shot before final emission. Do not knowingly serialize an invalid `director.json` just because its JSON syntax is valid.

## 10. Compile order

Use this order for long-form narrative work:

`story bible → timeline resolver → character-state resolver → scene resolver → ACTIVE_SHOT_SCOPE → reference router → speaker ownership → dialogue density gate → continuity/relay resolver → prompt budget → preflight linter → H3 runtime prompt → director.json adapter`

The story bible stays upstream. The H3 prompt is a filtered executable slice, not a miniature copy of the whole production plan.
