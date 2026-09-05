# `director.json` schemaVersion 4 Adapter

Use only when the user explicitly wants the established V9/V10.2-style `.director.json` workflow. This is a custom orchestration container, not the official MiniMax H3 API schema.

## Top-level key order

```json
{
  "schemaVersion": 4,
  "project": {},
  "defaults": {},
  "promptPrefix": "",
  "promptSuffix": "",
  "continuity": {},
  "assets": [],
  "shots": []
}
```

Preserve an existing project's values. For a new project using the user's established workflow, common defaults are 24 fps and the existing `h3_av_latent` continuity settings already used by that workflow; do not overwrite runtime values merely because this reference contains an example.

## Shot shape

```json
{
  "id": "shot_001",
  "title": "C01-01 ...",
  "prompt": "integrated_multimodal_description: ...\n\noverall_soundscape: ...\n\nnon_diegetic_music: ...",
  "negativePrompt": "...",
  "durationSeconds": 9,
  "enabled": true,
  "seed": null,
  "disabledAssetIds": [],
  "latentRelay": false,
  "secondSampling": false
}
```

Keep the exact shot IDs during revisions unless the user asks to renumber.

## Layering rule

Do not recreate the V10.2 bloat pattern by pasting the full project bible into every `shot.prompt`.

Use:

- `promptPrefix` for **whitelist-only universal invariants** that truly apply to every generation;
- `promptSuffix` for genuinely universal hard constraints that must apply to every shot;
- `shot.prompt` for the current opening state, current `SCENE_ID`, current character state, current references, timed performance/camera/VFX/audio and endpoint;
- `negativePrompt` for the current shot's activated risk families only.

The complete character registry, complete Scene Bible, future injuries, future props, future characters, future scene descriptions and future dialogue belong to Director/compiler knowledge. They must not be serialized into a runtime prefix merely because they exist elsewhere in the project.

If the target importer literally concatenates prefix/suffix into each H3 prompt, treat those fields as normal runtime prompt text and keep them extremely small.

## `promptPrefix` whitelist

Normally allowed:

- spoken-language lock;
- universal speaker-ID / `<d>` syntax rules;
- compact one-dialogue-owner rule;
- genuinely universal period/style realism;
- genuinely universal text/subtitle/watermark exclusions;
- compact project-wide audio-identity isolation when it truly applies to every shot.

Normally forbidden:

- complete character registry;
- complete scene registry;
- future character/state descriptions;
- full plot outline or future beats;
- future injury/bandage/damage states;
- complete reference registry;
- local camera/action instructions;
- local negatives.

## Shot-scoped compilation

Before serializing each `shots[n].prompt`, apply [Shot Scope Compiler](shot-scope-compiler.md).

Each shot receives only its active semantic slice:

`ACTIVE_SCENE + ACTIVE_CHARACTERS + ACTIVE_CHARACTER_STATES + ACTIVE_SPEAKER + ACTIVE_REFERENCES + current action/camera/light/audio + valid continuity handoff`.

Inactive scenes, future states and unrelated references stay upstream in the Director knowledge layer.

## Reference routing

Before emitting runtime reference labels, apply [Reference Router](reference-router.md).

For dialogue shots, the active speaker has first identity/state reference priority; current scene anchor follows when needed; visible listeners come after that. A listener/protagonist reference stack must not visually dominate a different active speaker without an explicit reason.

## `latentRelay`

Use `true` only when the shot is meant to inherit the prior accepted visual/AV latent or equivalent continuation context from the same valid continuity chain.

Use `false` for:

- fresh scene openings;
- montage/dream/flashback/location boundaries;
- explicit re-anchor shots;
- foreign-scene returns;
- any shot whose current `SCENE_ID` is incompatible with the previous latent/context.

An inherited shot must continue the current action/camera/audio phase; it must not restart the previous action.

Flag `SCENE_RELAY_CONFLICT` when a shot crosses a scene/time/state boundary but still inherits foreign latent/context.

## `secondSampling`

Preserve the user's existing workflow semantics. Do not assume this field is an official H3 model parameter.

Prompt/semantic correctness must be established before blaming second sampling, acceleration, CFG, seed or denoise for a scene/state leak. If a generated clip depicts an inactive future scene/character/state that is explicitly present in the runtime prompt or reference set, repair the prompt scope first.

## Audio hard lock

If the project has recurring dialogue characters, a compact project-level audio identity contract may live in `promptSuffix`. Avoid repeating the full voice specification inside every shot; per-shot prose should state only the active speaker and delivery delta.

## Preflight before JSON emission

Valid JSON syntax is not enough. Before returning the final `.director.json`, validate every enabled shot for:

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

Repair, simplify or split a failing shot before emission. Do not knowingly serialize a semantically invalid `.director.json` just because the container schema is correct.
