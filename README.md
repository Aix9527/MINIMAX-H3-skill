# MINIMAX-H3-skill

## 项目简介 / Overview

**MiniMax H3 Director OS V2.2** 是一套面向 MiniMax H3 的生产级导演提示词生成 Skill。它把 H3 原生提示词契约、电影导演方法、数字真人、自然对白、说话者唯一归属、场景锁、物理表演、战斗/VFX、语音身份、参考素材权限、长视频连续性与 QC 融合到同一套系统中。

**MiniMax H3 Director OS V2.2** is a production-grade director and prompt-generation Skill for MiniMax H3. It combines the H3-native prompt contract, cinematic directing, digital-human control, natural dialogue, exclusive speaker ownership, scene locking, physical performance, combat/VFX, audio identity, reference authority, long-video continuity, and QC in one system.

## V2.2 核心更新 / V2.2 Core Update

V2.2 重点修复两类实际生成问题：**人物串台词**和**同一场景空间漂移**。

V2.2 focuses on two practical generation failures: **dialogue migrating to the wrong character** and **spatial drift within the same recurring scene**.

### ACTIVE_SPEAKER / 唯一对白所有者

普通多人对白默认“一段生成只有一个对白所有者”。每个对白镜头明确：

Every dialogue clip declares exactly one dialogue owner by default:

```text
ACTIVE_SPEAKER = YUYUE_17 (S1), screen-left.
Only YUYUE_17 (S1) may speak in this clip.
RIVAL_GIRL (S2) is MUTE_LISTENER: no speech, lips closed, no phoneme motion.
YUYUE_17 (S1) says: <d>[Chinese] 中文台词。</d>
```

- Speaker ID 永远位于 `<d>` 外。 / Speaker IDs always remain outside `<d>`.
- 非说话人物全部为 `MUTE_LISTENER`。 / All non-speakers become `MUTE_LISTENER`.
- Speaker 改变时优先切成新的生成段。 / A speaker change normally starts a new generation segment.
- 不再默认使用“人物 A 长时间离屏说话 + 人物 B 完整正脸”的高风险构图。 / Long off-screen speech over another character's full frontal face is no longer a default pattern.

完整规则见 [`references/speaker-scene-lock.md`](./references/speaker-scene-lock.md)。

See [`references/speaker-scene-lock.md`](./references/speaker-scene-lock.md) for the full contract.

### SCENE_ID + SCENE_LOCK / 场景锁

每个跨生成段复用的地点必须建立稳定 `SCENE_ID`，并锁定：空间几何、床/柜子/门窗等锚点位置、摄影轴线、材质、主光方向、时间相位与持续损伤状态。

Every recurring location gets a stable `SCENE_ID` that locks geometry, anchor-object positions, camera axis, materials, primary-light direction, time phase, and persistent damage/state.

每个属于该场景的镜头都会重复一条紧凑 `SCENE_LOCK`，而不是只依赖全局 Prompt。

Every shot repeats a compact `SCENE_LOCK` instead of relying only on a project-global prompt.

当“卧室 → 回忆/蒙太奇 → 回卧室”时，返回镜头必须重新锚定卧室，而不能继承蒙太奇尾帧。

When returning from a montage, dream, flashback, time jump, or another location, the old scene is explicitly re-anchored instead of inheriting the immediately previous foreign-scene tail.

## V2.1 自然对白 / V2.1 Natural Dialogue

普通影视对白继续默认 `SUBTLE_LIPSYNC`：声音保持清晰，但嘴唇只做小幅自然开合，下颌基本稳定，情绪主要由眼神、呼吸、眉部、姿态与反应节奏承担。

Ordinary cinematic dialogue still defaults to `SUBTLE_LIPSYNC`: speech remains clear while lip motion stays small, jaw movement remains restrained, and emotional performance is carried primarily by gaze, breath, brows, posture, and reaction timing.

### 口型模式 / Lip-Motion Modes

| 模式 / Mode | 中文用途 | English Use |
|---|---|---|
| `CLOSED_LIPS` | 旁白、内心独白、未说话角色 | narration, inner monologue, non-speakers |
| `SUBTLE_LIPSYNC` | 默认电影对白 | default cinematic dialogue |
| `NATURAL_LIPSYNC` | 普通交流 | ordinary conversation |
| `EMPHATIC_LIPSYNC` | 强烈争辩、情绪强调 | heated argument or emphasis |
| `SHOUT_OR_SING` | 喊叫、尖叫、歌唱 | shouting, screaming, singing |

完整规则见 [`references/dialogue-motion.md`](./references/dialogue-motion.md)。

See [`references/dialogue-motion.md`](./references/dialogue-motion.md) for the complete contract.

## 核心原则 / Core Principles

- **先导演，后编译。** 先确定叙事任务、Blocking、表演、物理因果、摄影、灯光、声音与结束状态，再编译 H3 提示词。  
  **Direct first, compile second.** Resolve narrative job, blocking, performance, physical causality, camera, lighting, sound, and endpoint before compiling H3 prompts.
- **真实成片优先于计划。** 上一段已接受成片的真实状态优先于旧计划。  
  **Accepted footage beats planned footage.** The observed accepted state overrides the old plan.
- **一个对白段默认一个说话者。** 其他人物均为静默听者。  
  **One dialogue clip defaults to one speaker.** Other visible characters are mute listeners.
- **场景不是风格描述，而是空间状态。** 重复地点必须锁几何和锚点。  
  **A scene is spatial state, not merely style.** Recurring locations lock geometry and anchors.
- **声音清晰不等于嘴型明显。** 语音清晰度与可见口型幅度分开控制。  
  **Audio clarity does not require strong mouth motion.** Audio intelligibility and visible articulation amplitude are separate controls.
- **Prompt Budget Engine。** 全局常量、镜头变量、交接状态分层管理。  
  **Prompt Budget Engine.** Separate project invariants, shot variables, and handoff state.
- **Negative 按需启用。** 只写当前镜头真实存在的风险。  
  **Targeted negatives only.** Add only failure risks activated by the current shot.

## 架构 / Architecture

```text
SKILL.md                         # 导演大脑 + 编译器 / director brain + compiler
references/
  h3-native-output.md            # H3 原生格式 / H3 native format
  cinematic-production.md        # 数字真人、角色、摄影、灯光 / humans, character, camera, light
  performance-action-vfx.md      # 动作、战斗、VFX / action, combat, VFX
  audio-identity.md              # Speaker、对白、旁白、语言与混音 / speaker, dialogue, narration, language, mix
  dialogue-motion.md             # 自然口型 / natural dialogue motion
  speaker-scene-lock.md          # 说话者唯一归属与场景锁 / exclusive speaker ownership + scene lock
  reference-continuity.md        # Reference 与长序列连续性 / reference + long-form continuity
  qc-repair.md                   # QC 与修复 / QC + repair
  director-json-v4.md            # schemaVersion 4 adapter
CHANGELOG.md
```

## 对白高可靠性策略 / High-Reliability Dialogue Strategy

如果人物 A 说完后人物 B 要接话，优先生成两个段，而不是强行塞进一个段。

If character A speaks and character B answers, prefer two generation clips instead of forcing both speaker ownership states into one clip.

长对白需要换画面时，优先保留原说话者，或者切背影、肩部、手部、环境插入；不要让另一人物的完整正脸在长时间离屏对白期间成为唯一显眼人脸。

When dense speech needs visual variation, keep the original speaker dominant or use back-of-head, shoulder, hand, or environment inserts. Avoid making another character's full frontal face the only salient face during long off-screen speech.

## 场景高可靠性策略 / High-Reliability Scene Strategy

场景第一次获得满意画面后，保存一帧作为 `CANONICAL_SCENE_ANCHOR`。同场连续镜头可接真实尾帧；离开后再返回时，优先使用该场景锚点图重新 I2VA/Ref2VA，而不是继承其他场景尾帧。

After the first accepted view of a recurring location, save a stable frame as `CANONICAL_SCENE_ANCHOR`. Adjacent shots may continue from accepted tails; when returning later, re-anchor from that scene reference with I2VA/Ref2VA instead of inheriting another scene's tail.

## 支持任务 / Supported Tasks

- T2VA / I2VA / FL2VA / L2VA / Ref2VA
- 小说、剧本、分镜转 H3 / novel, script, storyboard to H3
- 多人物对白与声纹锁 / multi-character dialogue and voice identity
- 旁白与内心独白 / narration and inner monologue
- 重复场景与空间连续性 / recurring scenes and spatial continuity
- 数字真人 / digital-human scenes
- 动作、战斗、VFX / action, combat, VFX
- 多段长视频 / multi-segment long-form video
- Prompt 诊断与修复 / prompt diagnosis and repair
- `schemaVersion: 4` `.director.json`

## 使用方法 / Usage

加载仓库根目录 [`SKILL.md`](./SKILL.md)，然后直接提出任务。

Load [`SKILL.md`](./SKILL.md) from the repository root and describe the task naturally.

### 示例：两人对白 / Example: Two-Person Dialogue

```text
把这段两人对话生成成 H3 视频。每个生成段只允许一个 ACTIVE_SPEAKER，另一个人物必须 MUTE_LISTENER；Speaker 改变时切下一段。

Generate this two-person conversation for H3. Allow only one ACTIVE_SPEAKER per generated clip; the other person must be a MUTE_LISTENER. Start a new clip when the speaker changes.
```

### 示例：重复房间 / Example: Recurring Room

```text
这个卧室会在多个镜头重复出现。建立 BEDROOM_A 场景锁，固定床、柜子、门、窗、光线方向和材质；回忆结束返回卧室时重新锚定 BEDROOM_A。

This bedroom recurs across multiple clips. Create a BEDROOM_A scene lock for bed, cabinet, door, window, light direction, and materials; re-anchor BEDROOM_A after the flashback ends.
```

## 来源对比 / Source Review

本 Skill 在对比多套 H3 Prompt Skill、导演框架、电影微 Skill、长序列系统、实际 H3 工作流与前代生产框架后持续重构。完整融合依据见 [`docs/SOURCE_COMPARISON.md`](./docs/SOURCE_COMPARISON.md)。

This Skill has been iteratively rebuilt after comparing multiple H3 prompt Skills, director frameworks, film-craft micro-skills, long-sequence systems, practical H3 workflows, and prior production frameworks. See [`docs/SOURCE_COMPARISON.md`](./docs/SOURCE_COMPARISON.md) for the merge rationale.

## 公开命名规范 / Public Naming Policy

对外文档仅使用功能名、Skill 名、框架类型与版本号描述来源和演进；与本仓库无关的个人名、作者名或外部项目品牌名不进入公开说明、Release Notes 或示例文本。

Public-facing documentation uses capability names, Skill names, framework types, and version labels. Unrelated personal names, author names, or external project-brand names are omitted from public documentation, release notes, and examples.

## 版本发布 / Releases

所有正式版本都必须同时具备 **版本号 + Git Tag + GitHub Release**。

Every formal version must have a **version number + Git tag + GitHub Release**.

- **v2.2.0 — MiniMax H3 Director OS V2.2** — Speaker Ownership + Scene Lock / 说话者归属 + 场景锁
- **v2.1.1 — MiniMax H3 Director OS V2.1.1** — H3 对白语法与中文语言锁修正 / H3 dialogue syntax and Mandarin language-lock correction
- **v2.1.0 — MiniMax H3 Director OS V2.1** — 自然对白口型 / Natural Dialogue
- **v2.0.0 — MiniMax H3 Director OS V2.0** — 生产级模块化重构 / production-grade modular rebuild
- **v1.0.0 — MiniMax H3 Director OS V1.0** — 首个正式版本 / initial formal release

查看所有版本 / View all releases: https://github.com/Aix9527/MINIMAX-H3-skill/releases

## 当前版本 / Current Version

**v2.2.0 — MiniMax H3 Director OS V2.2**
