# Performance, Action & VFX

Use for fights, chases, forceful physical action, supernatural abilities, transformations, collisions, destruction, or any shot where motion readability is a primary risk.

## Physical performance chain

Build action as:

`initial state → anticipation/preparation → support & weight → main motion → contact/reaction → secondary motion → recovery → endpoint`

Track:

- which foot/hand/body region supports or initiates;
- direction and path;
- mass and momentum;
- contact point;
- reaction delay and counterforce;
- hair/cloth/prop inertia;
- post-contact balance and final pose.

Avoid simultaneous full-body mannequin motion. Eyes often lead the head, head leads torso, cloth/hair settle after body motion.

## Combat choreography

A readable exchange:

`prepare/weight → attack → counter → contact → feedback → recovery`

Do not stage characters as stationary turrets trading effects unless the scene intentionally demands ritual stillness.

At high speed, preserve a readable pre-contact and post-contact moment. Motion blur must not erase the actual hit.

## Impact grammar

Impact tiers are internal shorthand, not mandatory words in every final prompt.

- **LIGHT**: graze, light block, small deflection; compact sound/particle response, minor camera accent.
- **HEAVY**: decisive collision; body compression/rebound, strong material response, brief readable timing accent, debris/fluid when physically present.
- **ULTIMATE**: finishing or scene-scale event only; large spatial response, major light/pressure/shock effect and environment consequence.

Never make every hit ULTIMATE.

## VFX contract

For each major effect define only applicable fields:

- `source` — body, weapon, floor, sky, object, portal, etc.;
- `attachment / spatial anchor`;
- `color/material` if identity-critical;
- `behavior / trajectory`;
- `trail / secondary effect` when motion creates one;
- `environmentInteraction`;
- `collisionReaction`;
- `persistence`;
- `decay / residue`.

The effect must move with the actual source. A sword trail follows the real swing path; lightning emitted from a palm begins at the palm; an array on the floor contacts the floor.

## Environment damage state

Destruction is continuity, not decoration. Track when present:

- wall/floor/roof damage;
- debris location;
- fire/ice/water/smoke state;
- structural integrity;
- scorch, crack, blood, dust or other persistent marks;
- character injury caused by the event.

Accepted damage persists into later shots until repaired/cleared on screen or an intentional scene/time cut explains the change.

## VFX and human readability

Do not let particles hide the face, hands, contact point, dialogue mouth, or story-critical prop. Use the environment response to sell power instead of simply filling the frame with glow.

## Safer simplification order

If an action shot fails:

1. remove secondary attacks/effects;
2. reduce simultaneous actors;
3. choose one camera intention;
4. expose the contact point;
5. shorten the action path;
6. split attack and reaction into separate shots;
7. move an impossible event off-screen and show its consequence.
