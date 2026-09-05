# `director.json` schemaVersion 4/5 Adapter

This is a custom orchestration container, not the official MiniMax H3 API schema. Preserve the runtime's existing schema version. Some current workflows may migrate an imported schemaVersion 4 project to schemaVersion 5; do not force it back to 4 after the runtime has migrated it.

## Common top-level shape

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

When editing an existing project, preserve its actual keys and runtime semantics.

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

Keep existing shot IDs during revisions unless the user asks to renumber.

## Active-context layering rule

The runtime may concatenate `promptPrefix + shot.prompt + promptSuffix` into the actual H3 conditioning. Therefore the global layers must not contain inactive future entities.

Use:

- `promptPrefix` only for universal language/quality/format constraints that are safe in every shot;
- `shot.prompt` for the current `ACTIVE_SCENE`, current visible characters, current `ACTIVE_SPEAKER`, current action, camera, light, audio and endpoint;
- `promptSuffix` only for genuinely universal hard locks that do not name future characters/scenes;
- `negativePrompt` only for currently activated failure families;
- director/project metadata for the complete project database when the runtime supports metadata that is not concatenated into model conditioning.

Do **not** put a full character registry, full scene registry, future plot summary or future prop list inside `promptPrefix` or `promptSuffix` merely for convenience.

## Shot-level asset isolation

When `assets` contains the whole project's reference library, each shot must establish a small active reference set and disable the rest when the runtime supports `disabledAssetIds`.

Example:

```json
{
  "disabledAssetIds": [
    "asset_future_character",
    "asset_other_scene",
    "asset_unused_detail"
  ]
}
```

Default guidance:

- one main identity image per visible character;
- one active-scene anchor;
- optionally one essential wardrobe/prop reference;
- prefer roughly 2–4 active high-value images in ordinary shots;
- do not leave `disabledAssetIds: []` when the runtime otherwise exposes dozens of unrelated project assets to the current generation.

A large bank of eye/lip/hand/expression/turnaround images for one character can overpower another character and increase identity cloning or speaker confusion. Activate detail images only for a specific repair task.

## `latentRelay`

Use `true` only for a valid same-continuity inheritance chain. Use `false` for:

- fresh scene openings;
- intentional hard cuts;
- return from montage/dream/flashback to a previous scene;
- any `SCENE_ID` change;
- re-anchor after scene drift;
- a shot whose current reference anchor should override the immediately previous foreign-scene tail.

An inherited shot must continue the current state rather than restart the previous action.

## `secondSampling`

Preserve the user's existing workflow semantics. Do not treat this field as an official H3 model parameter.

## Audio hard lock

Keep only universal audio syntax and natural-mouth rules in global layers. Speaker-specific definitions should enter only shots where that speaker is active/visible, unless the runtime stores speaker metadata outside model conditioning.

## Compiler QC

Before export:

- preserve the runtime's actual schemaVersion;
- verify every speaking shot has only the intended active speaker ownership;
- verify global prefix/suffix contain no future `SCENE_ID` or inactive character registry;
- verify `disabledAssetIds` excludes irrelevant project assets when an asset pool is present;
- verify scene returns use re-anchor instead of foreign-scene latent inheritance;
- verify the H3 field order remains valid inside each `shot.prompt`.