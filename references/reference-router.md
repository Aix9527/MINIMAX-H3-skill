# Reference Router / 当前镜头参考资产路由

This module turns the Reference Authority concept into a per-shot filtering system.

The complete asset library may contain many character sheets, expressions, locations, motion videos, voice samples and future-state references. H3 must receive only the subset that is valid for the current generation segment.

## 1. ACTIVE_REFERENCE_SET

Before compiling H3 reference labels, construct an `ACTIVE_REFERENCE_SET`.

Filter in this order:

1. current scene;
2. current visible/audible characters;
3. current character state/version;
4. current active speaker;
5. current controlled dimension;
6. current generation mode and continuity type.

Only surviving assets are exposed to H3.

## 2. Reference authority dimensions

Resolve one winner per controlled dimension unless an intentional blend is explicitly defined:

`identity | age/anatomy | hair | wardrobe | prop | environment | composition | motion | camera | timing | voice | music | style`

Every selected reference should have a declared role. Do not include a reference merely because it is available.

## 3. Dialogue-shot priority

For dialogue clips, use this conservative production priority:

1. `ACTIVE_SPEAKER` identity/state references;
2. current `SCENE_ID` canonical environment anchor when needed;
3. visible `MUTE_LISTENER` identity/state references;
4. only then optional wardrobe/prop/composition/motion references that solve a real control problem.

This is a production heuristic, not an official H3 numerical limit. The goal is to prevent a listener or unrelated protagonist from dominating the visual reference stack while another character owns the dialogue.

Flag `REFERENCE_OWNER_MISMATCH` when the active speaker is visually important but most identity-bearing references belong to another person.

## 4. State-safe references

A reference is valid only if its depicted temporal state is valid now.

Examples:

- pre-accident shot → do not use the same character's post-injury bandaged portrait;
- clean wardrobe shot → do not use a torn/bloodied later-state sheet;
- present-day room → do not use the destroyed-after-explosion version unless that damage already exists;
- hidden character → do not use reveal-state imagery before the reveal.

If the only available canonical reference shows a future state, either crop/use a dimension that does not transfer the future feature when that is genuinely reliable, or exclude it and describe current identity more conservatively. Never silently inject the future state.

## 5. Scene references

Current-scene environment references may own:

- geometry;
- anchor-object placement;
- material identity;
- light direction/time phase;
- camera-axis context.

A foreign-scene image must not remain active simply because it was used in the previous generation.

After scene/montage/dream/time boundaries, use `reanchor_after_drift` or an intentional scene re-anchor and rebuild the `ACTIVE_REFERENCE_SET` from the new/current scene.

## 6. Continuation references

For `seamless_continuation`, the accepted previous tail may own instantaneous opening pose/composition/motion phase, while canonical character and scene references continue to own identity and stable environment dimensions.

Do not let an output-derived tail become the sole identity reference for long chains. Re-anchor to canonical identity/environment references after roughly 2 consecutive output-derived extensions, and no later than 3, or sooner if drift appears. This remains a workflow heuristic rather than an H3 limit.

## 7. Reference conflict rules

Reject or repair when:

- two different people both own `identity` for one target;
- a listener reference stack visually overwhelms the active speaker;
- current text says `PRE_ACCIDENT` but a selected image shows `POST_WAKE` bandages;
- current scene is `RIVER_A` but environment references depict `BEDROOM_A`;
- motion reference implies an action that belongs to a future beat;
- first/last-frame references contradict the declared scene or character state;
- voice sample owner does not match the declared speaker ID.

## 8. Sparse-reference principle

More references are not automatically safer.

Every extra asset adds another possible transfer path. Prefer the smallest set that controls the dimensions that actually matter in the current shot.

Ask for each asset:

- What dimension does this reference own?
- Why is that dimension needed now?
- Is the depicted character/scene/state valid now?
- What must not transfer from this reference?

If those questions cannot be answered, omit the asset from the current runtime set.

## 9. Runtime annotation

When useful, make authority explicit near the reference use:

```text
<Picture 1>: RIVAL_GIRL identity + current wardrobe only.
<Picture 2>: YUYUE_17 PRE_ACCIDENT identity only; do not transfer pose.
<Picture 3>: SCENE_RIVER_A geometry + light direction only.
```

Do not repeat a huge asset manifest in every shot. Include only the current active references.

## 10. Preflight gates

Before emission check:

- `ACTIVE_SPEAKER_REFERENCE_MISSING` — speaker needs visual identity control but has none while another character dominates references;
- `REFERENCE_OWNER_MISMATCH` — selected reference owner conflicts with controlled subject/dimension;
- `FUTURE_REFERENCE_LEAK` — future state/scene/reference enters current shot;
- `FOREIGN_SCENE_REFERENCE` — inactive scene reference survives a scene boundary;
- `REFERENCE_DIMENSION_CONFLICT` — multiple undeclared winners control the same dimension;
- `REFERENCE_BLOAT` — references are included without an active control role.

Repair by removing or rerouting references before adding more negative prompt text.
