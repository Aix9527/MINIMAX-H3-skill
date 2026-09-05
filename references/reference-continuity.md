# Reference Authority & Long-Video Continuity

This module combines reference-role isolation, first-frame geography, accepted-footage canon, and long-sequence state management.

For per-shot asset filtering, also use [Reference Router](reference-router.md). For future-state isolation, also use [Shot Scope Compiler](shot-scope-compiler.md).

## Reference authority matrix

For each target subject/scene and controlled dimension, select one winning reference or none.

Suggested dimensions:

`identity | age/anatomy | hair | wardrobe | prop | environment | composition | motion | camera | timing | voice | music | style`

A single source may own multiple dimensions. No dimension should have two winners unless the prompt explicitly defines a blend. State what each source must **not** transfer.

### Common roles

- Canonical portrait/character sheet → identity, hair, body design, and only the wardrobe/state that is temporally valid now.
- First frame → instantaneous pose, screen position, composition, current lighting.
- Last frame → required endpoint composition/state.
- Motion/reference video → action path, blocking, camera rhythm or timing only as declared.
- Environment picture/video → geography, material, palette, light direction for the current scene state.
- Audio → voice, timing, music or exact sound only as declared.

A reference that depicts a future injury, costume state, location state or reveal is not automatically valid just because it belongs to the same character or place.

## First-frame truth

When a source first frame can be inspected, treat it as current spatial truth. Do not overwrite it with a prose description that requires impossible hidden geometry.

When it cannot be inspected, use user-reported facts and do not claim an observed audit.

## Sequence state

Keep two levels.

### Canonical state

Long-lived facts that are valid **at the current story time**:

- stable identity and visual version;
- current wardrobe/props;
- current location/time/world state;
- persistent injury/VFX/damage that has already happened;
- voice identity;
- completed story beats/dialogue;
- canonical references valid for the current state.

Do not use canonical state as a container for future planned injuries, bandages, wardrobe damage, transformed forms or future scene states. Future planned facts stay in Director timeline knowledge until their validity boundary is reached.

### Transient shot state

Boundary facts:

- position/pose/orientation;
- left/right and screen direction;
- action phase/contact;
- camera side/height/move/focus phase;
- local lighting/weather;
- currently active sound/music phrase;
- temporary debris/smoke/fire/water state.

Lifecycle:

`plannedStart → resolve current temporal state → build ACTIVE_SHOT_SCOPE / ACTIVE_REFERENCE_SET → generate → observedStart/observedEnd → take verdict → canonical reconcile → next plannedStart`

## Accepted footage rule

- Accepted/accepted-with-deviation footage updates canon with what is actually observable.
- Rejected footage never updates canon.
- If the plan says a hand reached the handle but accepted footage ends 20 cm short, the next clip starts 20 cm short.
- Pixels can establish physical state, not hidden psychology.
- An accepted accidental future-state leak should not silently redefine the story timeline; if the take is rejected for semantic leakage, it does not update canon.

Do not fake `observedEndState` when the clip cannot be viewed. Keep planned state and provenance separate.

## Continuation types

Choose explicitly:

- `seamless_continuation` — same geography/shot/action phase; source ending is the opening.
- `intentional_next_shot` — editorial cut; story state continues, exact frame does not.
- `bridge_between_known_states` — known start and end; often suitable for first/last-frame control.
- `repair_tail` — fix a failed ending before extending it.
- `reanchor_after_drift` — return to canonical references after identity/geography/motion/audio drift.

Do not promise a seamless continuation across a scene/location/time/state boundary; default to an intentional cut/re-anchor when the previous latent/context is foreign to the current scope.

## Output-derived chain depth

Repeatedly using only the last generated frame can accumulate drift. As a conservative production rule, re-anchor to canonical identity/environment references after roughly 2 consecutive output-derived extensions, and no later than 3, or sooner if drift is visible. This is a workflow heuristic, not an H3 model limit.

## Segment boundary rules

Prefer boundaries at:

- completed micro-event;
- stable pose/end composition;
- emotional/value turn;
- intentional shot/scene change;
- character-state transition;
- finished dialogue phrase;
- moment where motion phase is easy to resume.

Do not split a sentence or contact action unless continuation genuinely needs to preserve that open phase.

## Future-beat protection

Each segment receives only its current job. Completed beats are not repeated. Future reveals, attacks, transformations, dialogue, injuries, scene states and references are not leaked into earlier segments simply because they appear later in the script.

Before runtime emission, filter through `ACTIVE_SHOT_SCOPE` and `ACTIVE_REFERENCE_SET`. Future planned information remains in Director/compiler knowledge only.
