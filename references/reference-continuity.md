# Reference Authority & Long-Video Continuity

This module combines reference-role isolation, first-frame geography, accepted-footage canon, and long-sequence state management.

## Reference authority matrix

For each target subject/scene and controlled dimension, select one winning reference or none.

Suggested dimensions:

`identity | age/anatomy | hair | wardrobe | prop | environment | composition | motion | camera | timing | voice | music | style`

A single source may own multiple dimensions. No dimension should have two winners unless the prompt explicitly defines a blend. State what each source must **not** transfer.

### Common roles

- Canonical portrait/character sheet → identity, hair, wardrobe, body design.
- First frame → instantaneous pose, screen position, composition, current lighting.
- Last frame → required endpoint composition/state.
- Motion/reference video → action path, blocking, camera rhythm or timing only as declared.
- Environment picture/video → geography, material, palette, light direction.
- Audio → voice, timing, music or exact sound only as declared.

## First-frame truth

When a source first frame can be inspected, treat it as current spatial truth. Do not overwrite it with a prose description that requires impossible hidden geometry.

When it cannot be inspected, use user-reported facts and do not claim an observed audit.

## Sequence state

Keep two levels.

### Canonical state

Long-lived facts:

- identity and visual version;
- wardrobe/props;
- location/time/world state;
- persistent injury/VFX/damage;
- voice identity;
- completed story beats/dialogue;
- canonical references.

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

`plannedStart → generate → observedStart/observedEnd → take verdict → canonical reconcile → next plannedStart`

## Accepted footage rule

- Accepted/accepted-with-deviation footage updates canon with what is actually observable.
- Rejected footage never updates canon.
- If the plan says a hand reached the handle but accepted footage ends 20 cm short, the next clip starts 20 cm short.
- Pixels can establish physical state, not hidden psychology.

Do not fake `observedEndState` when the clip cannot be viewed. Keep planned state and provenance separate.

## Continuation types

Choose explicitly:

- `seamless_continuation` — same geography/shot/action phase; source ending is the opening.
- `intentional_next_shot` — editorial cut; story state continues, exact frame does not.
- `bridge_between_known_states` — known start and end; often suitable for first/last-frame control.
- `repair_tail` — fix a failed ending before extending it.
- `reanchor_after_drift` — return to canonical references after identity/geography/motion/audio drift.

Do not promise a seamless continuation across a scene/location/time boundary; default to an intentional cut.

## Output-derived chain depth

Repeatedly using only the last generated frame can accumulate drift. As a conservative production rule, re-anchor to canonical identity/environment references after roughly 2 consecutive output-derived extensions, and no later than 3, or sooner if drift is visible. This is a workflow heuristic, not an H3 model limit.

## Segment boundary rules

Prefer boundaries at:

- completed micro-event;
- stable pose/end composition;
- emotional/value turn;
- intentional shot/scene change;
- finished dialogue phrase;
- moment where motion phase is easy to resume.

Do not split a sentence or contact action unless continuation genuinely needs to preserve that open phase.

## Future-beat protection

Each segment receives only its current job. Completed beats are not repeated. Future reveals, attacks, transformations and dialogue are not leaked into earlier segments simply because they appear later in the script.
