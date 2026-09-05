# MINIMAX-H3-skill

## 项目简介 / Overview

**MiniMax H3 Director OS V2.3** 是一套面向 MiniMax H3 的生产级导演提示词生成 Skill。它把 H3 原生提示词契约、电影导演方法、数字真人、自然对白、说话者唯一归属、场景锁、当前上下文隔离、参考素材白名单、长视频连续性与 QC 融合到同一套系统中。

**MiniMax H3 Director OS V2.3** is a production-grade director and prompt-generation Skill for MiniMax H3. It combines the H3-native prompt contract, cinematic directing, digital-human control, natural dialogue, exclusive speaker ownership, scene locking, active-context isolation, reference allowlisting, long-form continuity, and QC.

## V2.3 核心更新 / V2.3 Core Update

V2.3 重点修复实际成片中出现的 **未来场景提前出现、未来人物泄漏、参考图过载导致角色同化** 问题。

V2.3 focuses on practical failures where **future scenes appear early, inactive characters leak into the current clip, or an oversized reference bank causes one character identity to overpower another**.

### PROJECT DATABASE ≠ H3 CURRENT CONTEXT

项目数据库可以保存完整角色、场景、道具、声纹与参考素材，但每一个 H3 生成段只接收当前活动上下文。

The director database may contain the full project, but each H3 generation receives only the active context slice.

```text
Project Database
    ↓
Active Context Filter
    ↓
Reference Allowlist
    ↓
Speaker / Scene Locks
    ↓
H3 Prompt
```

### ACTIVE_CONTEXT_ONLY / 当前上下文隔离

每镜只允许进入 H3：

- 当前 `SCENE_ID`；
- 当前可见人物；
- 当前唯一 `ACTIVE_SPEAKER`；
- 当前动作与连续性状态；
- 当前真正需要的参考素材；
- 真正全局的语言、质量、格式与自然口型约束。

Only the current scene, visible characters, active speaker, current continuity/action state, required references, and truly global language/quality/format constraints enter the H3 conditioning.

未来人物、未来场景、未来道具不得通过全局 Prompt 提前暴露，也不要用“不要出现某人物/某房间”这种负面句式再次把概念暴露给模型。

Future characters, locations, and props should be absent from the current conditioning entirely rather than mentioned in negative wording.

完整规则见 [`references/active-context-isolation.md`](./references/active-context-isolation.md)。

See [`references/active-context-isolation.md`](./references/active-context-isolation.md) for the full contract.

### REFERENCE_ALLOWLIST / 参考素材白名单

普通镜头优先只启用 **2–4 个高价值参考**：

- 每名可见人物通常 1 个主身份参考；
- 1 个当前场景锚点；
- 必要时再加 1 个服装或关键道具参考。

Ordinary shots should usually use only **2–4 high-value references**: one main identity reference per visible character, one active-scene anchor, and only an additional wardrobe/prop reference when truly needed.

如果项目资产池包含几十张素材，镜头层必须用 `disabledAssetIds` 或等效机制禁用非白名单资产。不要把同一人物的眼睛、嘴、手、动作、表情、转面等十几张参考同时注入一个双人镜头。

When a project contains dozens of references, shot-level gating must disable non-allowlisted assets. Do not inject a large eye/lip/hand/expression/turnaround bank for one character into a two-character dialogue shot.

## V2.2 Speaker Ownership + Scene Lock / 说话者归属 + 场景锁

对白默认一段生成只有一个 `ACTIVE_SPEAKER`，其他人物均为 `MUTE_LISTENER`。Speaker 改变时优先切段；避免“人物 A 离屏长对白 + 人物 B 完整正脸”的高风险构图。

Dialogue defaults to one `ACTIVE_SPEAKER` per generated clip, with all other visible characters as `MUTE_LISTENER`. Speaker changes normally start a new segment, and long off-screen dialogue over another character's full frontal face is avoided.

每个重复地点建立 `SCENE_ID + SCENE_LOCK`，锁定空间几何、锚点道具、摄影轴线、材质、主光方向和持续状态。离开场景后返回时使用 `CANONICAL_SCENE_ANCHOR` 重新锚定。

Every recurring location uses `SCENE_ID + SCENE_LOCK` for geometry, anchor props, camera axis, materials, primary-light direction, and persistent state. Returning later requires re-anchoring from the canonical scene anchor.

完整规则见 [`references/speaker-scene-lock.md`](./references/speaker-scene-lock.md)。

## V2.1 Natural Dialogue / 自然对白

普通影视对白默认 `SUBTLE_LIPSYNC`：声音保持清晰，但嘴唇只做小幅自然开合，下颌基本稳定；旁白和内心独白要求可见人物 `CLOSED_LIPS`。

Ordinary cinematic dialogue defaults to `SUBTLE_LIPSYNC`: speech remains clear while lip and jaw motion stay restrained; narration and inner monologue keep visible mouths `CLOSED_LIPS`.

## 核心原则 / Core Principles

- **先导演，后编译。** / **Direct first, compile second.**
- **真实成片优先于计划。** / **Accepted footage beats planned footage.**
- **一个对白段默认一个说话者。** / **One dialogue clip defaults to one speaker.**
- **场景是空间状态，不只是风格。** / **A scene is spatial state, not merely style.**
- **项目数据库与当前生成上下文必须隔离。** / **Project database and current model context must be isolated.**
- **参考素材按镜头白名单启用。** / **References are enabled through a shot-level allowlist.**
- **声音清晰不等于嘴型明显。** / **Audio clarity does not require strong mouth motion.**
- **Negative 按需启用。** / **Targeted negatives only.**

## 架构 / Architecture

```text
SKILL.md                         # 导演大脑 + 编译器 / director brain + compiler
references/
  h3-native-output.md            # H3 原生格式 / H3 native format
  cinematic-production.md        # 数字真人、角色、摄影、灯光 / humans, character, camera, light
  performance-action-vfx.md      # 动作、战斗、VFX / action, combat, VFX
  audio-identity.md              # Speaker、对白、旁白、语言与混音 / speaker, dialogue, narration, language, mix
  dialogue-motion.md             # 自然口型 / natural dialogue motion
  speaker-scene-lock.md          # 说话者唯一归属与场景锁 / speaker ownership + scene lock
  active-context-isolation.md    # 当前上下文与参考素材隔离 / active-context + reference isolation
  reference-continuity.md        # Reference 与长序列连续性 / reference + long-form continuity
  qc-repair.md                   # QC 与修复 / QC + repair
  director-json-v4.md            # schemaVersion 4/5 adapter
CHANGELOG.md
```

## 高可靠性双人对白 / High-Reliability Two-Person Dialogue

```text
ACTIVE_SCENE = SCENE_RIVER_A
VISIBLE_CHARACTERS = YUYUE_17 (S1), RIVAL_GIRL (S2)
ACTIVE_SPEAKER = RIVAL_GIRL (S2)
MUTE_LISTENER = YUYUE_17 (S1)

REFERENCE_ALLOWLIST:
- YUYUE primary identity
- RIVAL_GIRL primary identity
- SCENE_RIVER_A anchor
```

不要同时把父母、老人、梦中人物、卧室、工厂和几十张余悦细节图放进这一镜。

Do not simultaneously expose parents, grandmother, dream characters, bedroom, factory, and dozens of detail references for the same protagonist to this shot.

## director.json 运行时说明 / director.json Runtime Notes

自定义 director 工作流可能把导入的 schemaVersion 4 项目迁移到 schemaVersion 5。V2.3 保留运行时实际版本，不强行回退。

A custom director runtime may migrate an imported schemaVersion 4 project to schemaVersion 5. V2.3 preserves the runtime's actual schema version rather than forcing it back.

如果 `assets` 中存在完整项目素材库，则每镜应通过 `disabledAssetIds` 或等效机制只保留当前白名单素材。

If `assets` contains the full project reference library, each shot should use `disabledAssetIds` or an equivalent gate so only the current allowlisted references remain active.

## 支持任务 / Supported Tasks

- T2VA / I2VA / FL2VA / L2VA / Ref2VA
- 小说、剧本、分镜转 H3 / novel, script, storyboard to H3
- 多人物对白与声纹锁 / multi-character dialogue and voice identity
- 旁白与内心独白 / narration and inner monologue
- 重复场景与空间连续性 / recurring scenes and spatial continuity
- 大型参考素材库按镜头路由 / large reference libraries with per-shot routing
- 数字真人、动作、战斗、VFX / digital humans, action, combat, VFX
- 多段长视频 / multi-segment long-form video
- Prompt 诊断与修复 / prompt diagnosis and repair
- `schemaVersion: 4/5` `.director.json`

## 公开命名规范 / Public Naming Policy

对外文档仅使用功能名、Skill 名、框架类型与版本号描述来源和演进；无关个人名、作者名或外部项目品牌名不进入公开说明、Release Notes 或示例文本。

Public-facing documentation uses capability names, Skill names, framework types, and version labels. Unrelated personal names, author names, or external project-brand names are omitted from public documentation, release notes, and examples.

## 版本发布 / Releases

所有正式版本必须具备 **版本号 + Git Tag + GitHub Release**。

Every formal version must have a **version number + Git tag + GitHub Release**.

- **v2.3.0 — MiniMax H3 Director OS V2.3** — Active Context Isolation / 当前上下文隔离
- **v2.2.0 — MiniMax H3 Director OS V2.2** — Speaker Ownership + Scene Lock / 说话者归属 + 场景锁
- **v2.1.1 — MiniMax H3 Director OS V2.1.1** — H3 对白语法与中文语言锁 / H3 dialogue syntax + Mandarin lock
- **v2.1.0 — MiniMax H3 Director OS V2.1** — Natural Dialogue / 自然对白
- **v2.0.0 — MiniMax H3 Director OS V2.0** — Production Modular Rebuild / 生产级模块化重构
- **v1.0.0 — MiniMax H3 Director OS V1.0** — Initial Release / 首个正式版本

查看所有版本 / View all releases: https://github.com/Aix9527/MINIMAX-H3-skill/releases

## 当前版本 / Current Version

**v2.3.0 — MiniMax H3 Director OS V2.3**
