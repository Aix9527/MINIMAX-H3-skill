# Source Skill Comparison and V2.0 Merge Rationale

This document records the design review used to build MiniMax H3 Director OS V2.0. It compares capabilities rather than counting ZIP files: some archives are duplicates, some are corpora, some are full production frameworks, and one contains 98 micro-skills.

## Executive finding

No single source was sufficient.

- The official-style H3 skills are strongest at **correct model-native structure**, but are intentionally light on film directing.
- Director craft libraries are strongest at **cinematic intent, blocking, performance, camera and sound**, but are platform-neutral.
- V9/V10.2 are strongest at **production state, digital humans, combat/VFX, validation and custom director JSON**, but V10.2 can over-repeat project-wide material inside every shot.
- Seedance 2.0 is strongest at **accepted-footage continuity, reference authority and long-sequence state**, but its surface-specific mechanics must not be copied into H3.
- ComfyUI-H3-Director is strongest at **practical multi-segment execution, tail-frame relay, caching, audio slots and global prompt separation**, but it is a runtime/plugin rather than a general director brain.

V2.0 therefore uses: `H3 official contract + director brain + production modules + prompt-budget compiler + accepted-footage state`.

## Comparison

| Source | Main strengths | Main weaknesses / risks | What V2.0 keeps |
|---|---|---|---|
| Official MiniMax `h3-prompt-writing` / `start-h3-prompts-from-scratch` | Five H3 modes, exact base/full-reference section order, reference labels, speaker/timing notation, real tail-frame continuation discipline | Minimal directing language; little digital-human/combat/QC depth | Hard output contract and mode semantics |
| `minimax-h3-prompt-standardizer` | Beginner-friendly intake, sensible segmentation, observable language, compact negatives | Simplified reference/continuity model; not a deep director system | Simple input policy, micro-event segmentation, targeted constraints |
| `awesome-minimax-h3-prompts` | Large real-result prompt corpus; demonstrates long prompts, detailed timing, reference locks, camera/action/audio patterns | A corpus, not a governing skill; many entries are reconstructed and cannot prove hidden negatives/workflow | Empirical writing patterns only, never treated as authoritative format |
| `director-craft-framework` | Strong conversion of emotion to body behavior, motivated camera/light, visual causality, failure fallback, director-style review | Very large monolithic instruction surface; platform-neutral equipment language can over-specify H3 | Observable behavior, motivated camera, physical causality, anti-tool-showoff rule |
| `DirectorSKILL` | End-to-end production pipeline: subtext, beats, blocking, coverage, keyframes, sound/edit, QC cost ladder | Broader than H3 prompt generation; many deliverables can distract from a single prompt task | Narrative job, blocking, keyframe control, endpoint and repair ladder |
| `directorskills-main` (98 micro-skills) | Deep craft granularity across cinematography, color, directing, shot design, transitions, sound and story | Highly fragmented; cannot be dumped into one H3 prompt; some film rules are contextual rather than universal | Selected decision rules: axis, eyeline, reaction, shot scale, motivated light, sound hierarchy |
| `director-skills-main/travel-skill` | Excellent first-frame spatial audit, physical camera path, motivated lighting, real/AI material discipline | Travel-domain framing; model recipes are not H3-specific | First-frame spatial truth and “do not invent inaccessible geometry” |
| `seedance-2.0` | Reference authority by dimension, accepted observed state, continuation/re-anchor logic, anti-slop, sequence state, camera endpoint | Seedance surface/model limits are not H3 rules; very large routed skill graph | Authority matrix, accepted-footage canon, chain re-anchor heuristic, anti-slop |
| `ComfyUI-H3-Director` | Real H3 production workflow: 5–15s timeline UI, global prompt, tail-frame relay, reference conversion, segment caching/re-run, audio slots | Runtime-specific; plugin behavior must not be presented as universal H3 semantics | Global-vs-shot separation, segment-level execution mindset, runtime adapter boundary |
| Thedore V9 | Clean Director IR, model adapters, physical performance, reference registry, audio/narrator separation, accepted footage > plan | Cinematic language/digital-human/action detail still relatively thin | Director/adapter separation and canonical observed-state loop |
| Thedore V10.2 | Digital Human Realism, Character Visual Lock, Timecoded Beats, Micro Performance, combat impact, VFX contract, environment damage, QC/validators | Per-shot output can become excessively long by repeating global visual/identity/negative blocks; multi-model breadth adds complexity | All high-value production modules, but routed/condensed rather than copied wholesale |
| MiniMax H3 Director OS V1.0 | H3-focused director brain, Blocking-before-Camera, Reference Contract, spatial audit, anti-slop, H3 compiler | Under-specified production output in practice: digital-human/voice/combat/timing modules were not always re-injected; no modular reference files | Core director logic, upgraded with modular production layers and prompt budget |

## Key design corrections from V1.0

### 1. Prevent “V10.2 bloat” without losing its strengths

V2.0 separates project invariants, shot variables and handoff state. Digital-human rules, character identity and voice locks remain available but are injected only where they affect the current shot.

### 2. Restore adaptive timing

V1.0 said complex clips should be time-structured but actual generated `director.json` could become too prose-heavy and lose timing. V2.0 makes adaptive timeline design part of the root workflow while reserving `[Shot N] At ...` for true editorial shot changes.

### 3. Make negative prompts genuinely targeted

Audio/anatomy/VFX negatives are routed by risk. A silent landscape shot should not carry dialogue-voice constraints; a locked dialogue close-up should not carry combat/debris constraints.

### 4. Preserve production-grade digital humans

V2.0 restores anatomy, skin optics, eyes, hair, cloth/accessory inertia, real-camera behavior and age-aware beautification as an optional module rather than a universal paragraph.

### 5. Preserve combat/VFX/environment state

The V10.2 action stack survives as a specialized module, with physical contact readability and persistent damage folded into continuity.

### 6. Make reference ownership explicit

Reference authority is defined per controlled dimension; media type and upload order do not decide authority. This combines H3's reference labels with the stronger state/authority logic found in the long-sequence skills.

## Resulting V2.0 architecture

```text
MiniMax H3 Director OS V2.0
├── H3 Native Output Contract
├── Director's Read
├── Prompt Budget Engine
├── Reference Contract / Authority Matrix
├── First-frame Spatial Audit
├── Cinematic Production / Digital Human
├── Physical Performance / Combat / VFX
├── Audio Identity / Narrator Bus
├── Canonical + Transient Continuity State
├── Adaptive Timeline
├── Long-form Segment / Accepted-footage Handoff
├── Targeted Negative Router
├── QC / Repair Ladder
└── optional director.json v4 Adapter
```

The intended outcome is **more capability than V10.2 with less duplicated per-shot prose**, while staying inside MiniMax H3's native prompt-writing contract.
