# Cinematic Production Layer

Use this module when the shot contains people, acting, high-value visual identity, cinematic lighting/camera, or digital-human realism. It merges the strongest production ideas without forcing every clause into every shot.

## Visual style as a project invariant

Define a compact project look once:

- world/genre and medium;
- palette and contrast policy;
- material behavior;
- skin/rendering policy when humans are present;
- atmosphere/volumetric rule;
- camera/lens character only if it changes the look;
- one or two quality anchors;
- explicit forbidden style drift.

Do not repeat this whole bible in every shot. Per shot, include only the visible delta: e.g. `hard side window light replaces the previous soft courtyard light`.

## Digital Human Realism

Use `OFF / BALANCED / STRONG / MAX` as an internal routing level.

Control realism through visible layers rather than resolution buzzwords:

- anatomy: age-correct craniofacial and body proportions, subtle asymmetry;
- skin microstructure: pores, lip lines, eye/nose-region detail, tone variation;
- skin optics: layered subsurface response, localized oil sheen, vascular warmth, varied roughness;
- eyes: wet cornea, iris depth, tear meniscus, natural sclera, source-motivated catchlight;
- hair: strand breakup, baby hair/flyaways, irregular hairline, delayed secondary motion;
- fabric/accessories: weight, fold memory, inertia and delayed settling;
- camera reality: plausible perspective, depth of field, focus behavior, restrained motion blur;
- light reality: highlights and rim/catch lights must have a source;
- micro-motion: blink, breath, swallow, gaze and reaction latency as needed.

Anatomy wins over beautification. Do not adultize children/adolescents, erase age cues on older characters, or replace real structure with anime eye/jaw proportions unless the requested style explicitly requires it.

## Character identity lock

Keep a compact canonical record per recurring character:

- face/age identity;
- hair;
- costume layers and recurring accessories;
- body build/proportion;
- persistent injury/mark/FX;
- forbidden mutations;
- voice identity in the audio module.

Only inject the visible character locks needed for the current shot. If a canonical reference image is active, avoid redundantly rewriting every static facial detail; state what the reference owns and what may change.

## Micro-performance

Performance follows the scene's narrative job. Useful channels:

- eyes/eyeline;
- eyelids/brows;
- lips/jaw/swallow;
- breath/chest;
- fingers/grip;
- shoulders/posture;
- distance/weight shift;
- reaction delay;
- settling after the action.

Use 1–4 channels that actually carry the scene. Do not animate all channels at once like a checklist.

### Power without cliché

Do not mechanically map `low angle = powerful` or `high angle = weak`. Power may be shown by stillness, spatial ownership, who crosses whose space, who waits, who forces the other person to move, who receives the reaction shot, and who controls silence.

## Camera grammar

Every shot should know:

`size + angle + position + primary move + relation to subject + endpoint`

Lens anchors are optional and must produce a visible effect:

- wide / ~24–35mm: spatial energy, proximity, speed, environment relationship;
- normal / ~40–55mm: natural observation and dialogue;
- tele / ~70–100mm: isolation, compression, intimacy, crowding;
- macro: material/detail event.

A close-up must be earned by a change in information, emotion, power or reaction.

A reaction shot often carries more narrative value than repeating the action that caused it.

## Lighting grammar

Describe motivated source → direction → hardness → temperature → subject/background relationship → continuity.

Dark does not mean underexpose everything. Use occlusion, negative fill, direction and controlled background separation.

Energy/VFX light must affect skin, fabric, floor, walls, haze and reflections according to proximity.

## Continuity geometry

For linked shots preserve unless intentionally reset:

- 180-degree axis;
- screen direction;
- eyeline;
- left/right placement;
- camera side/height;
- inherited focus and move phase.

An intentional cut may reset camera grammar, but story geography must remain legible.
