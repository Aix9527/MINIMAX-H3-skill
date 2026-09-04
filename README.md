# MINIMAX-H3-skill

## 项目简介 / Overview

**MiniMax H3 Director OS V2.1** 是一套面向 MiniMax H3 的生产级导演提示词生成 Skill。它把 H3 原生提示词契约、电影导演方法、数字真人控制、自然对白口型、物理表演、战斗/VFX、语音身份、参考素材权限、长视频连续性与 QC 融合到同一套系统中。

**MiniMax H3 Director OS V2.1** is a production-grade director and prompt-generation Skill for MiniMax H3. It combines the H3-native prompt contract, cinematic directing, digital-human control, natural dialogue motion, physical performance, combat/VFX, audio identity, reference authority, long-video continuity, and QC in one system.

## V2.1 核心更新 / V2.1 Core Update

V2.1 重点修复“人物说话时嘴巴和下颌动作过于明显”的问题。普通影视对白默认从强口型约束改为 `SUBTLE_LIPSYNC`：声音仍然清晰，但嘴唇只做小幅自然开合，下颌保持稳定，情绪主要由眼神、呼吸、眉部、姿态与反应节奏承担。

V2.1 focuses on reducing overly visible lip and jaw motion during generated dialogue. Ordinary cinematic speech now defaults to `SUBTLE_LIPSYNC`: audio remains clear while visible articulation stays restrained, with small lip openings, minimal jaw travel, and emotional performance carried mainly by eyes, breath, brows, posture, and reaction timing.

### 口型模式 / Lip-Motion Modes

| 模式 / Mode | 中文用途 | English Use |
|---|---|---|
| `CLOSED_LIPS` | 旁白、内心独白、未说话角色，不做对白口型 | narration, inner monologue, non-speakers; no dialogue articulation |
| `SUBTLE_LIPSYNC` | 默认电影对白，小幅嘴唇运动、下颌基本稳定 | default cinematic dialogue; small lip motion, mostly stable jaw |
| `NATURAL_LIPSYNC` | 普通交流，口型可见但不夸张 | ordinary conversation; visible but restrained articulation |
| `EMPHATIC_LIPSYNC` | 强烈争辩、情绪强调 | heated argument or deliberate verbal emphasis |
| `SHOUT_OR_SING` | 喊叫、尖叫、歌唱 | shouting, screaming, or singing |

完整规则见 [`references/dialogue-motion.md`](./references/dialogue-motion.md)。

See [`references/dialogue-motion.md`](./references/dialogue-motion.md) for the complete contract.

## 核心原则 / Core Principles

- **先导演，后编译。** 先确定叙事任务、Blocking、表演、物理因果、摄影机意图、灯光、声音与结束状态，再编译成 H3 提示词。  
  **Direct first, compile second.** Decide narrative job, blocking, performance, physical causality, camera intent, lighting, sound, and endpoint before compiling H3 prompts.
- **真实成片优先于计划。** 上一段已接受成片的真实尾帧和真实结束状态优先于旧计划。  
  **Accepted footage beats planned footage.** The real ending of accepted prior footage overrides what the old plan expected.
- **Blocking before Camera。** 先安排人物在空间里怎么动，再决定镜头怎么动。  
  **Blocking before Camera.** Place and move subjects in space before choosing camera movement.
- **Prompt Budget Engine。** 全局常量、当前镜头变量、交接状态分层管理，不把所有信息重复写进每镜。  
  **Prompt Budget Engine.** Separate project invariants, shot variables, and handoff state instead of repeating everything in every shot.
- **声音清晰不等于嘴型明显。** 对白混音清晰度与可见口型幅度分开控制。  
  **Audio clarity does not require strong mouth motion.** Dialogue intelligibility and visible articulation amplitude are controlled separately.
- **Negative 按需启用。** 只写本镜真实存在的风险。  
  **Targeted negatives only.** Add only the failure risks actually activated by the current shot.

## 架构 / Architecture

```text
SKILL.md                         # 路由 + 导演大脑 + Prompt Budget 编译器 / router + director brain + prompt-budget compiler
references/
  h3-native-output.md            # H3 原生字段与模式契约 / H3 native field and mode contract
  cinematic-production.md        # 数字真人、角色锁、微表演、摄影与灯光 / digital human, character lock, micro-performance, camera/light
  performance-action-vfx.md      # 身体物理、战斗、冲击、VFX、环境损伤 / body physics, combat, impact, VFX, environment damage
  audio-identity.md              # 对白、声纹、旁白与混音 / dialogue, voice identity, narration, mix
  dialogue-motion.md             # 自然对白口型与下颌幅度 / natural dialogue lip and jaw motion
  reference-continuity.md        # Reference 权限、首帧审计、Accepted Footage 连续性 / reference authority, first-frame audit, accepted-footage canon
  qc-repair.md                   # 校验、Take Review 与修复阶梯 / validation, take review, repair ladder
  director-json-v4.md            # 可选 V9/V10.2 兼容 director.json 容器 / optional V9/V10.2-compatible director.json container
docs/
  SOURCE_COMPARISON.md           # 各来源 Skill 优缺点与融合依据 / source-by-source comparison and merge rationale
CHANGELOG.md                     # 版本更新记录 / version changelog
```

## 对白生成建议 / Dialogue Generation Guidance

普通对白不应默认从第 0 秒一直说到最后一帧。优先采用：`反应/吸气 → 说话 → 短暂停顿 → 嘴部回落 → 反应`。如果台词过长，应拆句、延长镜头、切听者反应或让声音离屏继续，而不是强迫角色高速连续动嘴。

Ordinary dialogue should not automatically run from frame one to the final frame. Prefer: `reaction / inhale → speech → short pause → mouth settles → reaction`. If a line is too long, split it, extend the shot, cut to a listener reaction, or continue speech off-screen instead of forcing rapid continuous mouth motion.

普通对白镜头优先中近景、三分之四侧角或自然视平线，不把嘴当作视觉中心。只有剧情确实需要时才使用长时间正脸大特写。

For ordinary dialogue, prefer medium close-ups, three-quarter angles, or natural eye-level framing without making the mouth the visual focal point. Use long frontal extreme close-ups only when the story truly requires them.

## 支持任务 / Supported Tasks

- T2VA 文本生成音视频 / text-to-audio-video
- I2VA 首帧图生音视频 / first-frame image-to-audio-video
- FL2VA 首尾帧约束生成 / first-and-last-frame generation
- L2VA 尾帧约束生成 / last-frame-constrained generation
- Ref2VA 全参考、编辑与续写 / full multimodal reference, edit, and continuation
- 对白、旁白与内心独白 / dialogue, narration, and inner monologue
- 数字真人与国漫真人感场景 / digital-human and guoman-realism scenes
- 动作、战斗、神通与 VFX 场景 / action, combat, spell, and VFX scenes
- 多段长视频 / multi-segment long-form video
- Prompt 诊断与修复 / prompt diagnosis and repair
- `schemaVersion: 4` `.director.json` 工作流 / `schemaVersion: 4` `.director.json` workflow

## 使用方法 / Usage

加载仓库根目录 [`SKILL.md`](./SKILL.md)，然后直接用自然语言提出任务。

Load the repository root [`SKILL.md`](./SKILL.md), then ask naturally.

### 示例：自然对白 / Example: Natural Dialogue

```text
把这段对白生成成 8 秒 MiniMax H3 视频。普通对白使用低幅自然口型，声音清晰但不要明显张嘴或持续下颌开合；保留 1 秒说话前反应和 1.5 秒说话后停顿。

Generate this dialogue as an 8-second MiniMax H3 clip. Use restrained natural lip motion for ordinary speech: keep the voice clear without obvious mouth opening or continuous jaw pumping, with a 1-second pre-speech reaction and a 1.5-second post-speech pause.
```

### 示例：旁白 / Example: Voiceover

```text
这一段使用内心独白，画面中的人物嘴巴保持闭合，只通过眼神和呼吸表现情绪。

Use inner monologue for this segment. Keep the visible character's lips closed and carry emotion only through gaze and breathing.
```

## 来源对比 / Source Review

本 Skill 在对比多套 H3 Prompt Skill、导演框架、电影微 Skill、长序列系统、实际 H3 工作流与前代生产框架后持续重构。完整优缺点与融合依据见 [`docs/SOURCE_COMPARISON.md`](./docs/SOURCE_COMPARISON.md)。

This Skill has been iteratively rebuilt after comparing multiple H3 prompt Skills, director frameworks, film-craft micro-skills, long-sequence systems, practical H3 workflows, and prior production frameworks. See [`docs/SOURCE_COMPARISON.md`](./docs/SOURCE_COMPARISON.md) for the full strengths/weaknesses review and merge rationale.

## 公开命名规范 / Public Naming Policy

对外文档仅使用功能名、Skill 名、框架类型与版本号描述来源和演进；与本仓库无关的个人名、作者名或外部项目品牌名不进入公开说明、Release Notes 或示例文本。

Public-facing documentation uses capability names, Skill names, framework types, and version labels to describe sources and evolution. Unrelated personal names, author names, or external project-brand names are omitted from public documentation, release notes, and examples.

## 版本发布 / Releases

所有正式版本都必须同时具备 **版本号 + Git Tag + GitHub Release**。

Every formal version must have a **version number + Git tag + GitHub Release**.

- **v2.1.0 — MiniMax H3 Director OS V2.1** — 自然对白口型更新 / Natural Dialogue update
- **v2.0.0 — MiniMax H3 Director OS V2.0** — 生产级模块化重构 / production-grade modular rebuild
- **v1.0.0 — MiniMax H3 Director OS V1.0** — 首个正式版本 / initial formal release

查看所有版本 / View all releases: https://github.com/Aix9527/MINIMAX-H3-skill/releases

## 当前版本 / Current Version

**v2.1.0 — MiniMax H3 Director OS V2.1**
