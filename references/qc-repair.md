# QC & Repair Ladder

Diagnose the generated result or prompt by the smallest broken contract. Do not respond to failure by adding more adjectives.

For long-form narrative work, semantic scope is checked before sampler/workflow tuning.

## Hard-fail categories

- wrong identity/age/wardrobe/prop owner;
- broken first-frame geography;
- impossible or restarted action phase;
- wrong dialogue speaker / visible character narrating VO;
- unreadable key contact/action;
- missing or contradictory endpoint;
- reference ownership conflict;
- persistent damage/state disappearing without explanation;
- invalid H3 section order, labels or timestamps;
- inactive scene appears inside the current runtime prompt;
- future character/state/injury/prop/reveal/dialogue leaks into an earlier shot;
- future/inactive reference is routed into the current shot;
- cross-scene shot inherits foreign latent/context when it should re-anchor;
- dialogue density exceeds the available speech window without a deliberate high-speed requirement.

## Semantic Leakage / 语义泄漏

Typical symptoms:

- current riverbank shot suddenly cuts to a later bedroom/dream/other location;
- a character appears before their story entrance;
- future injury/bandage/dirt/costume state appears early;
- future prop or reveal appears before its beat;
- the active speaker visually turns into the listener/protagonist because references are dominated by the wrong owner;
- an unrelated future scene appears near the end of an otherwise correct clip.

When these occur, diagnose in this order:

1. inspect the **actual runtime prompt**, including global prefix/suffix concatenation;
2. inspect `ACTIVE_SHOT_SCOPE` for inactive scene/entity/state leakage;
3. inspect current references for future-state or wrong-owner assets;
4. inspect character-state validity;
5. inspect dialogue density and simultaneous task overload;
6. inspect latent/context continuity across scene boundaries;
7. only then inspect second sampling, acceleration, denoise, seed, CFG, scheduler or other workflow parameters.

If the wrong future scene/state is explicitly present in runtime text or references, the prompt/compiler is the root cause even if a sampler or acceleration path makes the failure more visible.

## Take verdict

Use one of:

- `KEEP`
- `KEEP_WITH_POST_FIX`
- `EDIT`
- `RE-ROLL`
- `REWRITE`
- `REPLAN_SHOT`

Accepted footage updates canon; rejected footage does not.

## One-variable repair rule

When possible, change the smallest variable that can fix the failure so you can learn what caused it. Typical order:

1. remove semantic-scope leak / future beat / inactive scene;
2. remove conflicting or wrong-owner reference;
3. fix current character state/version;
4. reduce simultaneous actions/entities;
5. fix dialogue density by splitting or adding real speech time;
6. clarify identity or spatial lock;
7. add/clarify endpoint;
8. simplify camera;
9. expose physical contact/reaction;
10. fix dialogue ownership/mix;
11. fix foreign-scene relay/re-anchor;
12. regenerate;
13. only after semantic correctness is clean, A/B workflow variables such as second sampling or acceleration;
14. rebuild first/last frame or canonical anchor;
15. split/replan the shot.

After repeated failures of the same shot, change the shot design rather than stacking prompt clauses: shorter, closer, simpler, different angle, reaction/insert, first-last-frame control, or show only the consequence.

## Prompt-budget QC

Reject a prompt as over-specified when:

- the same global style paragraph appears in every shot;
- global prefix/suffix semantically dominates the current shot;
- complete character or Scene Bible content is injected into every runtime prompt;
- character descriptions are repeated even though a canonical reference already owns them;
- many camera moves compete;
- every available VFX/impact adjective is enabled;
- negative prompt includes risks absent from the shot;
- negative prompt introduces future scene/state nouns merely to negate them;
- soundtrack, ambience, SFX and dialogue are all described as foreground;
- timecodes exist only to make prose look precise but do not correspond to real shot changes.

Reject a prompt as under-specified when:

- the action has no endpoint;
- the first-frame motion path is physically unclear;
- identity/reference ownership is ambiguous;
- a long 10–15s clip has multiple events but no timing/ordering;
- dialogue speaker is unclear;
- VFX has no source/interaction;
- a continuation does not state the accepted opening state.

## Preflight error codes

Use these names when auditing a prompt/director file:

- `SCOPE_LEAK`
- `FUTURE_BEAT_LEAK`
- `CHARACTER_STATE_CONFLICT`
- `INACTIVE_CHARACTER_LEAK`
- `FUTURE_REFERENCE_LEAK`
- `REFERENCE_OWNER_MISMATCH`
- `GLOBAL_PROMPT_DOMINANCE`
- `ENTITY_SCOPE_OVERLOAD`
- `SPEAKER_OWNERSHIP_CONFLICT`
- `DIALOGUE_DENSITY_OVERLOAD`
- `SCENE_RELAY_CONFLICT`
- `NEGATIVE_SEMANTIC_LEAK`

Hard errors are repaired before final `.director.json` emission.

## Final validator checklist

- correct H3 mode and field order;
- duration and timecodes valid;
- runtime prompt contains only the current scene/entities/states;
- no future beat/state/reference leakage;
- references resolved and stable;
- active speaker is not visually outvoted by another character's reference stack;
- dialogue exact and correctly assigned;
- dialogue density fits the actual speech window or is intentionally split;
- ambience/music separated;
- one dominant narrative/visual job;
- camera endpoint readable;
- action endpoint readable;
- continuity handoff explicit for sequences;
- scene/time boundaries use correct re-anchor/relay behavior;
- only relevant negative families active.
