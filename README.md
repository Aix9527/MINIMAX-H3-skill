# MINIMAX-H3-skill

**MiniMax H3 Director OS V2.0** is a production-grade prompt-generation skill for MiniMax H3. It combines the model-native prompt contract with cinematic directing, digital-human realism, physical performance, combat/VFX, audio identity, reference authority, long-video continuity and QC—without copying a giant production bible into every shot.

## V2.0 design goal

> More control than V10.2, less duplicated prompt text than V10.2, and stricter MiniMax H3-native formatting than V1.0.

## Architecture

```text
SKILL.md                         # router + director brain + prompt-budget compiler
references/
  h3-native-output.md            # official H3 field/mode contract
  cinematic-production.md        # digital human, character lock, micro-performance, camera/light
  performance-action-vfx.md      # body physics, combat, impact, VFX, environment damage
  audio-identity.md              # dialogue/voice/narrator/mix contracts
  reference-continuity.md        # reference authority, first-frame audit, accepted-footage canon
  qc-repair.md                   # validation, take review and repair ladder
  director-json-v4.md            # optional V9/V10.2-compatible director.json container
docs/
  SOURCE_COMPARISON.md           # source-by-source strengths, weaknesses and merge rationale
CHANGELOG.md
```

## What changed from V1.0

V1.0 had a stronger H3 director brain but could produce prompts that were too thin compared with V10.2. V2.0 restores the high-value production controls—digital-human layers, identity locks, micro-performance, combat/VFX, environment damage, voice identity and adaptive timing—while routing them only when needed.

The key mechanism is the **Prompt Budget Engine**:

1. **Project invariants** — world/style, canonical identity, voice, persistent state.
2. **Shot variables** — current action, camera, VFX, dialogue, sound and endpoint.
3. **Handoff state** — accepted end state, unfinished motion, damage and continuity facts.

This prevents the old pattern where a 6–10k-character global bible was pasted into every shot.

## Supported tasks

- T2VA text-to-audio-video
- I2VA first-frame image-to-audio-video
- FL2VA first/last-frame generation
- L2VA last-frame-constrained generation
- Ref2VA full multimodal reference / edit / continuation
- dialogue and narration scenes
- digital-human / guoman-realism scenes
- action, combat, spell and VFX scenes
- multi-segment long-form video
- prompt diagnosis / repair
- the established `schemaVersion: 4` `.director.json` workflow

## Official H3 baseline

MiniMax's public H3 materials describe an omni-modal model accepting text/image/video/audio context, producing video with native stereo audio, up to 15 seconds and up to 2K. The official prompt-writing skill uses T2VA/I2VA/FL2VA/L2VA/Ref2VA and preserves fixed prompt section order.

Official sources:

- https://github.com/MiniMax-AI/MiniMax-H3
- https://github.com/MiniMax-AI/MiniMax-H3/tree/main/skills/h3-prompt-writing
- https://www.minimax.io/news/minimax-h3-open-source

Target runtimes can impose narrower limits. Existing project/runtime settings always win over generic defaults.

## Usage

Load the repository root [`SKILL.md`](./SKILL.md), then ask naturally, for example:

```text
把这段小说改成 5 个 MiniMax H3 生成段。人物用参考图锁定，战斗段保留物理接触和环境损伤，输出可直接复制的 H3 提示词。
```

or:

```text
根据上一段真实尾帧继续 8 秒，不重复上一段已经完成的转身动作；保持角色身份、衣服、屏幕方向和光线，最后停在可继续生成的稳定画面。
```

or:

```text
按我的 V10.2 schemaVersion 4 格式输出 director.json。
```

## Source review

The design was rebuilt after comparing the uploaded H3 prompt skills, director-craft frameworks, the 98-skill film craft library, Seedance 2.0 sequence system, ComfyUI-H3-Director, Thedore V9, Thedore V10.2 and V1.0. See [`docs/SOURCE_COMPARISON.md`](./docs/SOURCE_COMPARISON.md).
