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

- `promptPrefix` or runtime global-prompt capability for compact project invariants when the workflow supports it;
- `promptSuffix` for genuinely universal hard constraints such as established audio-identity isolation when they must apply to every shot;
- `shot.prompt` for current opening state, job, timed performance/camera/VFX/audio and endpoint;
- `negativePrompt` for the current shot's activated risk families only.

If the target importer does not expose a true global prompt layer and literally concatenates prefix/suffix into each prompt, keep those layers concise.

## `latentRelay`

Use `true` only when the next shot is meant to inherit the prior accepted visual/AV latent or equivalent continuation context. Use `false` for fresh scene openings, intentional hard cuts that should re-anchor, or when the runtime cannot carry the state reliably.

An inherited shot must continue the current action/camera/audio phase; it must not restart the previous action.

## `secondSampling`

Preserve the user's existing workflow semantics. Do not assume this field is an official H3 model parameter.

## Audio hard lock

If the project has recurring dialogue characters, a compact project-level audio identity contract may live in `promptSuffix`. Avoid repeating the full voice specification inside every shot; per-shot prose should state only the active speaker and delivery delta.
