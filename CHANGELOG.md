# 更新日志 / Changelog

## 2.3.0 — 2026-09-05

### 中文

- 新增 `Active Context Isolation` 当前上下文隔离模块，防止未来人物、未来场景、未来道具提前泄漏进当前 H3 片段。
- 明确 `PROJECT DATABASE ≠ H3 CURRENT CONTEXT`：完整项目数据库可以保存全部角色/场景，但单镜 Prompt 只编译当前活动上下文。
- `promptPrefix` / `promptSuffix` 改为真正全局白名单，只允许语言、通用质量、格式、自然口型等不会触发未来视觉实体的约束。
- 禁止在全局 H3 Prompt 中放入完整角色注册表、完整场景注册表、未来剧情摘要或未来道具清单。
- 新增 `ACTIVE_CONTEXT_ONLY`：每镜只允许当前 `SCENE_ID`、可见人物、当前唯一 `ACTIVE_SPEAKER`、当前动作/连续性状态和必要参考素材。
- 新增 `REFERENCE_ALLOWLIST`：普通镜头优先 2–4 个高价值参考；每名可见人物通常只保留 1 个主身份参考 + 当前场景锚点 + 必要服装/道具参考。
- 对含完整项目资产池的 director.json，要求通过 `disabledAssetIds` 禁用非白名单素材；若工作流暴露几十个资产而 `disabledAssetIds` 仍为空，视为高风险。
- 修复“同一角色大量眼部/唇部/手部/表情/转面参考压过第二人物”的问题，降低角色二被角色一同化和 Speaker Swap 风险。
- `SCENE_LOCK` 与 `ACTIVE_CONTEXT_ONLY` 分工明确：前者防止当前场景漂移，后者防止其他场景提前出现。
- director.json Adapter 扩展到 schemaVersion 4/5，保留运行时实际版本，不再强行回退到 4。
- 场景切换、梦境/回忆/蒙太奇返回旧地点时继续强制 re-anchor，并禁用错误的跨场景 latent relay。

### English

- Added `Active Context Isolation` to prevent future characters, locations, and props from leaking into the current H3 clip.
- Formalized `PROJECT DATABASE ≠ H3 CURRENT CONTEXT`: the project may know everything, but a single generated clip receives only the active slice.
- Restricted `promptPrefix` / `promptSuffix` to a true global allowlist: language, universal quality, format, natural-mouth rules, and other constraints that do not name future visual entities.
- The full character registry, full scene registry, future-plot summary, and future prop list must not enter the global H3 conditioning.
- Added `ACTIVE_CONTEXT_ONLY`: compile only the current `SCENE_ID`, visible characters, one active speaker, current continuity/action state, and required references.
- Added `REFERENCE_ALLOWLIST`: ordinary shots should usually use 2–4 high-value references instead of the entire project asset bank.
- When a director project contains a full asset pool, non-allowlisted assets must be disabled through `disabledAssetIds` or an equivalent runtime gate. An empty disable list against dozens of exposed assets is considered high risk.
- Reduced overpowering single-character reference banks that can clone one identity into another character and increase speaker confusion.
- Clarified responsibilities: `SCENE_LOCK` prevents active-scene drift; `ACTIVE_CONTEXT_ONLY` prevents inactive-scene leakage.
- Extended the director adapter to schemaVersion 4/5 and preserve the runtime's actual schema version.
- Scene returns after montage/dream/flashback still require re-anchor and must not inherit a foreign-scene latent tail.

## 2.2.0 — 2026-09-05

### 中文

- 新增 `Speaker Ownership & Scene Lock` 模块。
- 对白生成默认改为“一段生成一个 `ACTIVE_SPEAKER`”，其他可见人物必须为 `MUTE_LISTENER`。
- Speaker 改变时优先切成新的生成段。
- 禁止把“人物 A 长时间离屏说话 + 人物 B 完整正脸”作为默认减口型方案。
- Speaker ID 强制位于 `<d>` 外部，`<d>` 内只保留语言标签和准确台词。
- 新增声音空间来源锁。
- 新增 `SCENE_ID + SCENE_LOCK` 与 `CANONICAL_SCENE_ANCHOR`。
- 新增 Speaker Handoff Barrier 与 Scene Return Barrier。

### English

- Added the `Speaker Ownership & Scene Lock` module.
- Dialogue generation defaults to one `ACTIVE_SPEAKER` per generated clip; all other visible people are `MUTE_LISTENER`.
- Speaker changes normally start a new generation segment.
- Long off-screen speech over another character's full frontal face is no longer a default pattern.
- Speaker IDs remain outside `<d>`.
- Added spatial audio-origin locking, `SCENE_ID + SCENE_LOCK`, canonical scene anchors, speaker-handoff barriers, and scene-return barriers.

## 2.1.1 — 2026-09-05

### 中文

- 修正 H3 对白语法：Speaker ID 必须位于 `<d>` 外部。
- 中文项目所有可听对白、旁白、内心独白与离屏人声强制使用 `<d>[Chinese] ...</d>`。
- 同一人物内心独白复用原 Speaker ID。

### English

- Corrected H3 dialogue syntax so speaker IDs stay outside `<d>`.
- Mandarin projects require `<d>[Chinese] ...</d>` for all audible human speech.
- Same-character voiceover reuses the original speaker ID.

## 2.1.0 — 2026-09-04

### 中文

- 新增 `Natural Dialogue Motion` 自然对白口型模块。
- 普通影视对白默认 `SUBTLE_LIPSYNC`。
- 将声音清晰度与可见口型幅度彻底分离。

### English

- Added the `Natural Dialogue Motion` module.
- Ordinary cinematic dialogue defaults to `SUBTLE_LIPSYNC`.
- Separated audio intelligibility from visible articulation amplitude.

## 2.0.0 — 2026-09-04

### 中文

- 围绕 MiniMax H3 原生提示词契约重构 Skill。
- 增加模块化加载路由、Prompt Budget Engine、数字真人、角色身份锁、微表演、战斗/VFX、环境损伤、语音身份、Reference Authority、首帧空间审计与 Accepted Footage 连续性。

### English

- Rebuilt the Skill around the MiniMax H3 native prompt contract with modular routing, Prompt Budget Engine, digital-human realism, identity locks, micro-performance, combat/VFX, audio identity, reference authority, spatial audit, and accepted-footage continuity.

## 1.0.0 — 2026-09-04

### 中文

- 首个 MiniMax H3 Director OS 正式版本。

### English

- Initial formal MiniMax H3 Director OS release.
