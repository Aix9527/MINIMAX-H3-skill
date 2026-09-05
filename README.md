# MINIMAX-H3-skill

## 项目简介 / Overview

**MiniMax H3 Director OS V2.3** 是一套面向 MiniMax H3 的生产级导演提示词生成 Skill。它把 H3 原生提示词契约、电影导演方法、数字真人、自然对白、说话者唯一归属、场景锁、人物状态、参考素材权限、长视频连续性与 QC 融合到同一套系统中。

V2.3 的核心原则是：

> **Director 可以知道整部故事，但 H3 每次只能看到当前镜头。**

**MiniMax H3 Director OS V2.3** is a production-grade director and prompt compiler for MiniMax H3. V2.3 introduces hard shot-scoped semantic isolation so the Director may know the whole story while each H3 generation receives only the current executable slice.

## V2.3 核心更新 / V2.3 Core Update

V2.3 重点解决实际长篇生成中出现的：**未来场景串入当前镜头、人物未来状态提前出现、参考图错配、全局 Prompt 过重、长对白过载**。

V2.3 focuses on semantic leakage, temporal-state leakage, wrong reference ownership, global-prompt dominance, and dialogue-density overload.

### 1. Shot Scope Compiler / 当前镜头语义防火墙

生成每一个镜头前先建立 `ACTIVE_SHOT_SCOPE`：

```text
ACTIVE_SCENE
ACTIVE_CHARACTERS
ACTIVE_CHARACTER_STATES
ACTIVE_SPEAKER
ACTIVE_PROPS
ACTIVE_REFERENCES
CURRENT_ACTION / CAMERA / LIGHT / AUDIO
VALID_CONTINUITY_HANDOFF
```

完整角色表、完整 Scene Bible、未来伤势、未来服装、未来人物、未来地点、未来对白和未来参考图保留在 Director/compiler 层，不自动进入当前 H3 runtime prompt。

The complete story/scene/character bible stays upstream. H3 receives only the current scene, characters, valid temporal states, references, action and continuity facts.

完整规则见 [`references/shot-scope-compiler.md`](./references/shot-scope-compiler.md)。

### 2. Temporal Firewall / 时间语义防火墙

人物身份与人物状态分离：

```text
CHARACTER_ID = YUYUE_17
STATE_ID = PRE_ACCIDENT
STATE = uninjured; no forehead wound; no gauze
```

后续镜头才允许：

```text
STATE_ID = POST_WAKE
STATE = same identity; forehead wrapped with gauze; slightly pale after injury
```

同一个人物参考不能因为“身份相同”就把未来伤势、绷带、衣服破损或剧情状态带回更早镜头。

### 3. Reference Router / 当前镜头参考资产路由

完整素材库不是 runtime 参考集。V2.3 先按以下顺序过滤：

```text
当前场景
→ 当前人物
→ 当前人物状态
→ 当前 ACTIVE_SPEAKER
→ 当前控制维度
→ ACTIVE_REFERENCE_SET
```

对白镜头保守优先级：

1. ACTIVE_SPEAKER 身份/当前状态；
2. 当前场景 canonical anchor；
3. 可见 MUTE_LISTENER；
4. 当前真正需要的服装/道具/构图/动作参考。

如果主说话人是人物 B，却大部分身份参考都属于人物 A，会触发 `REFERENCE_OWNER_MISMATCH`。

完整规则见 [`references/reference-router.md`](./references/reference-router.md)。

### 4. promptPrefix 白名单 / Global Prompt Whitelist

V2.3 不再允许把完整角色注册表和完整 Scene Bible 塞进每个镜头的全局 Prompt。

`promptPrefix` 通常只允许：

- 中文/语言锁；
- H3 对白语法；
- 一段生成一个对白所有者；
- 真正全局成立的时代/写实风格；
- 真正全局成立的字幕/水印禁止规则。

通常禁止：

- 完整角色表；
- 完整场景表；
- 未来伤势/绷带/状态；
- 未来角色/地点/道具；
- 完整剧情；
- 完整参考素材清单。

### 5. Dialogue Density Gate / 对白密度门禁

V2.3 在编译前计算：

```text
speech_density = spoken_Han_characters / available_speech_seconds
```

生产启发式（不是 H3 官方模型限制）：

| 密度 | 判定 |
|---|---|
| `<= 5.0 chars/s` | PASS |
| `>5.0–5.5` | CAUTION |
| `>5.5–6.5` | SPLIT_RECOMMENDED |
| `>6.5` | HARD_SPLIT |

长对白优先拆段或增加真实对白时间，不通过“说快一点”“嘴型更明显”解决。

完整规则见 [`references/dialogue-motion.md`](./references/dialogue-motion.md)。

### 6. Director Preflight Linter / 输出前硬门

最终 Prompt / `.director.json` 输出前检查：

```text
SCOPE_LEAK
FUTURE_BEAT_LEAK
CHARACTER_STATE_CONFLICT
INACTIVE_CHARACTER_LEAK
FUTURE_REFERENCE_LEAK
REFERENCE_OWNER_MISMATCH
GLOBAL_PROMPT_DOMINANCE
ENTITY_SCOPE_OVERLOAD
SPEAKER_OWNERSHIP_CONFLICT
DIALOGUE_DENSITY_OVERLOAD
SCENE_RELAY_CONFLICT
NEGATIVE_SEMANTIC_LEAK
```

硬错误必须先修复、简化或拆段，不能因为 JSON 语法有效就继续输出。

## V2.2 Speaker + Scene Lock

V2.2 建立了两个重要基础：**人物对白唯一归属**和**重复场景空间锁定**。V2.3 保留并加强这两项能力。

### ACTIVE_SPEAKER / 唯一对白所有者

```text
ACTIVE_SPEAKER = YUYUE_17 (S1), screen-left.
Only YUYUE_17 (S1) may speak in this clip.
RIVAL_GIRL (S2) is MUTE_LISTENER: no speech, lips closed, no phoneme motion.
YUYUE_17 (S1) says: <d>[Chinese] 中文台词。</d>
```

- Speaker ID 永远位于 `<d>` 外。 / Speaker IDs always remain outside `<d>`.
- 非说话人物全部为 `MUTE_LISTENER`。 / All non-speakers become `MUTE_LISTENER`.
- Speaker 改变时优先切成新的生成段。 / A speaker change normally starts a new generation segment.
- 不默认使用“人物 A 长时间离屏说话 + 人物 B 完整正脸”。

完整规则见 [`references/speaker-scene-lock.md`](./references/speaker-scene-lock.md)。

### SCENE_ID + SCENE_LOCK / 场景锁

每个跨生成段复用的地点建立稳定 `SCENE_ID`，锁定空间几何、锚点位置、摄影轴线、材质、主光方向、时间相位与当前有效的持续状态。

完整 Scene Bible 现在只属于 Director/compiler 层；每个 H3 镜头只重复当前场景的紧凑 `SCENE_LOCK`。

返回旧场景时必须重新锚定，而不是继承蒙太奇、梦境、闪回或其他场景尾帧。

## V2.1 Natural Dialogue / 自然对白

普通影视对白继续默认 `SUBTLE_LIPSYNC`：声音保持清晰，但嘴唇只做小幅自然开合，下颌基本稳定，情绪主要由眼神、呼吸、眉部、姿态与反应节奏承担。

| 模式 / Mode | 中文用途 | English Use |
|---|---|---|
| `CLOSED_LIPS` | 旁白、内心独白、未说话角色 | narration, inner monologue, non-speakers |
| `SUBTLE_LIPSYNC` | 默认电影对白 | default cinematic dialogue |
| `NATURAL_LIPSYNC` | 普通交流 | ordinary conversation |
| `EMPHATIC_LIPSYNC` | 强烈争辩、情绪强调 | heated argument or emphasis |
| `SHOUT_OR_SING` | 喊叫、尖叫、歌唱 | shouting, screaming, singing |

## 核心原则 / Core Principles

- **Director knows the whole story; H3 sees only the current shot.**
- **Temporal firewall is a hard gate.** Future scenes/states/references do not leak backward.
- **Accepted footage beats planned footage.**
- **One clip, one dominant job.**
- **One dialogue clip defaults to one ACTIVE_SPEAKER.**
- **Character identity and temporal state are separate.**
- **References are routed per current shot and control dimension.**
- **A recurring scene is spatial state, not merely style.**
- **Audio clarity does not require strong mouth motion.**
- **Dialogue density is checked before compilation.**
- **Negative prompts are local risk controls, not a second story bible.**

## 架构 / Architecture

```text
SKILL.md                         # 导演大脑 + 编译器 / director brain + compiler
references/
  h3-native-output.md            # H3 原生格式 / H3 native format
  cinematic-production.md        # 数字真人、角色、摄影、灯光
  performance-action-vfx.md      # 动作、战斗、VFX
  audio-identity.md              # Speaker、对白、旁白、语言与混音
  dialogue-motion.md             # 自然口型 + 对白密度门禁
  speaker-scene-lock.md          # 说话者唯一归属 + 当前场景锁
  shot-scope-compiler.md         # 当前镜头语义防火墙 + Temporal Firewall
  reference-router.md            # 当前镜头参考资产路由
  reference-continuity.md        # Reference 与长序列连续性
  qc-repair.md                   # QC、语义泄漏诊断与修复
  director-json-v4.md            # schemaVersion 4 adapter + preflight
CHANGELOG.md
```

## 推荐长篇编译链 / Recommended Long-Form Compile Chain

```text
Story Bible
→ Timeline Resolver
→ Character-State Resolver
→ Scene Resolver
→ ACTIVE_SHOT_SCOPE
→ Reference Router
→ Speaker Ownership
→ Dialogue Density Gate
→ Continuity / Relay Resolver
→ Prompt Budget
→ Preflight Linter
→ H3 Runtime Prompt
→ director.json Adapter
```

## 支持任务 / Supported Tasks

- T2VA / I2VA / FL2VA / L2VA / Ref2VA
- 小说、剧本、分镜转 H3 / novel, script, storyboard to H3
- 多人物对白与声纹锁 / multi-character dialogue and voice identity
- 旁白与内心独白 / narration and inner monologue
- 重复场景与空间连续性 / recurring scenes and spatial continuity
- 人物时间状态管理 / temporal character-state management
- 当前镜头参考素材路由 / shot-scoped reference routing
- 数字真人 / digital-human scenes
- 动作、战斗、VFX / action, combat, VFX
- 多段长视频 / multi-segment long-form video
- Prompt / 视频失败诊断与修复 / prompt and failed-output diagnosis
- `schemaVersion: 4` `.director.json`

## 使用方法 / Usage

加载仓库根目录 [`SKILL.md`](./SKILL.md)，然后直接提出任务。

Load [`SKILL.md`](./SKILL.md) from the repository root and describe the task naturally.

### 示例：长篇小说 / Example: Long Narrative

```text
把这段小说编译成 H3 director.json。Director 可以保存完整故事资料，但每个 runtime shot 只允许当前场景、当前人物状态和当前参考图；先做 Dialogue Density Gate 和 Preflight Linter。
```

### 示例：重复房间 / Example: Recurring Room

```text
这个卧室会在多个镜头重复出现。建立 BEDROOM_A 场景锁；完整 Scene Bible 留在 Director 层，当前 H3 镜头只注入 BEDROOM_A 的紧凑锁；回忆结束返回卧室时重新锚定。
```

## 来源对比 / Source Review

本 Skill 在对比多套 H3 Prompt Skill、导演框架、电影微 Skill、长序列系统、实际 H3 工作流与前代生产框架后持续重构。完整融合依据见 [`docs/SOURCE_COMPARISON.md`](./docs/SOURCE_COMPARISON.md)。

## 公开命名规范 / Public Naming Policy

对外文档仅使用功能名、Skill 名、框架类型与版本号描述来源和演进；与本仓库无关的个人名、作者名或外部项目品牌名不进入公开说明、Release Notes 或示例文本。

## 版本发布 / Releases

所有正式版本都必须同时具备 **版本号 + Git Tag + GitHub Release**。

- **v2.3.0 — MiniMax H3 Director OS V2.3** — SceneScope + Temporal Firewall + Reference Router + Dialogue Density Gate
- **v2.2.0 — MiniMax H3 Director OS V2.2** — Speaker Ownership + Scene Lock
- **v2.1.1 — MiniMax H3 Director OS V2.1.1** — H3 对白语法与中文语言锁修正
- **v2.1.0 — MiniMax H3 Director OS V2.1** — Natural Dialogue
- **v2.0.0 — MiniMax H3 Director OS V2.0** — production-grade modular rebuild
- **v1.0.0 — MiniMax H3 Director OS V1.0** — initial formal release

## 当前版本 / Current Version

**v2.3.0 — MiniMax H3 Director OS V2.3**
