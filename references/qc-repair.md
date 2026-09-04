# QC & Repair Ladder

Diagnose the generated result or prompt by the smallest broken contract. Do not respond to failure by adding more adjectives.

## Hard-fail categories

- wrong identity/age/wardrobe/prop owner;
- broken first-frame geography;
- impossible or restarted action phase;
- wrong dialogue speaker / visible character narrating VO;
- unreadable key contact/action;
- missing or contradictory endpoint;
- reference ownership conflict;
- persistent damage/state disappearing without explanation;
- invalid H3 section order, labels or timestamps.

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

1. remove conflicting reference/instruction;
2. reduce simultaneous actions;
3. clarify identity or spatial lock;
4. add/clarify endpoint;
5. simplify camera;
6. expose physical contact/reaction;
7. fix dialogue ownership/mix;
8. regenerate;
9. rebuild first/last frame or canonical anchor;
10. split/replan the shot.

After repeated failures of the same shot, change the shot design rather than stacking prompt clauses: shorter, closer, simpler, different angle, reaction/insert, first-last-frame control, or show only the consequence.

## Prompt-budget QC

Reject a prompt as over-specified when:

- the same global style paragraph appears in every shot;
- character descriptions are repeated even though a canonical reference already owns them;
- many camera moves compete;
- every available VFX/impact adjective is enabled;
- negative prompt includes risks absent from the shot;
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

## Final validator checklist

- correct H3 mode and field order;
- duration and timecodes valid;
- references resolved and stable;
- dialogue exact and correctly assigned;
- ambience/music separated;
- one dominant narrative/visual job;
- camera endpoint readable;
- action endpoint readable;
- continuity handoff explicit for sequences;
- only relevant negative families active.
