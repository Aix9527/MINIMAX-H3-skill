# 更新日志 / Changelog

## 2.3.0 — 2026-09-05

### 中文

- 新增 `Shot Scope Compiler`：明确“Director 可以知道整部故事，但 H3 每次只能看到当前镜头”，把未来场景、未来人物、未来伤势、未来道具、未来对白和未来参考图隔离在 runtime Prompt 之外。
- 新增 `Temporal Firewall`：人物稳定身份与时间状态拆分，防止同一角色的未来绷带、伤势、服装破损、年龄/形态状态提前出现。
- 新增 `Reference Router`：完整素材库先按当前场景、当前人物、当前状态、ACTIVE_SPEAKER 和控制维度过滤，再形成 `ACTIVE_REFERENCE_SET`。
- 对对白镜头加入参考优先级：ACTIVE_SPEAKER 身份/状态 → 当前场景 anchor → MUTE_LISTENER → 其他当前必要参考；增加 `REFERENCE_OWNER_MISMATCH` 检查。
- 将 `promptPrefix` 改为白名单语义：仅允许真正全局成立的语言、H3 对白语法、对白所有权、总风格和通用文本排除；禁止完整角色表、完整 Scene Bible、未来状态/剧情/参考资产进入每镜 runtime Prompt。
- 修正 `speaker-scene-lock.md` 中“全局 Prompt 可以保存完整 Scene Bible”的高风险规则：完整 Scene Bible 现在只属于 Director/compiler 知识层。
- 新增 `Dialogue Density Gate`：按 `spoken_Han_characters / available_speech_seconds` 做生产级预检；>6.5 chars/s 默认 HARD_SPLIT。该阈值明确标注为生产启发式而非 H3 官方限制。
- 新增 `Semantic Negative Hygiene`：Negative 不得通过“no future bedroom / no future bandage”等形式重新把未来概念喂给模型。
- 新增 Director Preflight Linter 错误族：`SCOPE_LEAK / FUTURE_BEAT_LEAK / CHARACTER_STATE_CONFLICT / INACTIVE_CHARACTER_LEAK / FUTURE_REFERENCE_LEAK / REFERENCE_OWNER_MISMATCH / GLOBAL_PROMPT_DOMINANCE / ENTITY_SCOPE_OVERLOAD / SPEAKER_OWNERSHIP_CONFLICT / DIALOGUE_DENSITY_OVERLOAD / SCENE_RELAY_CONFLICT / NEGATIVE_SEMANTIC_LEAK`。
- QC 修复顺序调整为：先检查实际 runtime Prompt、Shot Scope、Reference Router、人物状态和跨场景 relay，再评估二采、加速、denoise、seed、CFG、scheduler 等工作流变量。
- `director-json-v4.md` 增加 `.director.json` 输出前语义硬门，禁止“JSON 语法正确但语义泄漏”的文件直接交付。
- README 与主 `SKILL.md` 升级为 V2.3。

### English

- Added `Shot Scope Compiler`: the Director may know the entire story, while each H3 runtime prompt sees only the current executable shot.
- Added a hard `Temporal Firewall` that separates stable character identity from time-sensitive state, preventing future injuries, bandages, wardrobe damage or transformations from leaking backward.
- Added `Reference Router` and per-shot `ACTIVE_REFERENCE_SET` filtering by scene, character, state, active speaker and controlled dimension.
- Added dialogue-shot reference priority and `REFERENCE_OWNER_MISMATCH` detection.
- Converted `promptPrefix` into a whitelist-only runtime layer and removed complete character/scene/future-state registries from global H3 prompt semantics.
- Removed the unsafe rule that allowed a complete Scene Bible to live in the global runtime prompt; the full Scene Bible is now Director/compiler knowledge only.
- Added the `Dialogue Density Gate` using spoken Han characters per available speech second, with explicit production-heuristic thresholds.
- Added semantic-negative hygiene so detailed future entities are not reintroduced merely to negate them.
- Added semantic-scope preflight error families and made semantic validation mandatory before `.director.json` emission.
- Reordered QC so runtime prompt scope, references, temporal state and relay are inspected before sampler/second-pass/acceleration tuning.
- Updated README and the main `SKILL.md` to V2.3.

## 2.2.0 — 2026-09-05

### 中文

- 新增 `ACTIVE_SPEAKER` 唯一对白所有权。
- 所有非说话人物默认 `MUTE_LISTENER`。
- 新增高风险“听者正脸 + 长离屏对白”防护。
- 新增稳定 `SCENE_ID / SCENE_LOCK`、`CANONICAL_SCENE_ANCHOR` 与 Scene Return Barrier。
- 返回旧场景时要求 re-anchor，禁止直接继承外国场景尾帧。

### English

- Added exclusive `ACTIVE_SPEAKER` ownership and `MUTE_LISTENER` rules.
- Added protection against long off-screen speech over another visible full face.
- Added `SCENE_ID / SCENE_LOCK`, canonical scene anchors, and explicit scene-return re-anchoring.

## 2.1.1 — 2026-09-04

### 中文

- 修正 H3 对白语法：Speaker ID 必须位于 `<d>` 外。
- 强化中文语言锁：所有可听中文人声使用 `<d>[Chinese] ...</d>`。

### English

- Corrected H3 dialogue syntax so Speaker IDs stay outside `<d>`.
- Strengthened Mandarin language locking for all audible human speech.

## 2.1.0 — 2026-09-04

### 中文

- 新增 `Natural Dialogue Motion` 自然对白口型模块。
- 普通影视对白默认改为 `SUBTLE_LIPSYNC`，不再把“正确同步”理解成明显嘴唇和下颌运动。
- 新增 `CLOSED_LIPS / SUBTLE_LIPSYNC / NATURAL_LIPSYNC / EMPHATIC_LIPSYNC / SHOUT_OR_SING` 五级口型模式。
- 将声音清晰度与可见口型幅度彻底分离。
- 旁白、内心独白和离屏思绪默认 `CLOSED_LIPS`。
- 新增对白时间结构：`反应/吸气 → 说话 → 停顿 → 嘴部回落 → 反应`。
- 长对白优先拆句、延长镜头、切听者反应或离屏继续说话，避免高速连续动嘴。
- 新增对白专用 Negative。

### English

- Added the `Natural Dialogue Motion` module.
- Ordinary cinematic dialogue now defaults to `SUBTLE_LIPSYNC`.
- Added five lip-motion modes: `CLOSED_LIPS / SUBTLE_LIPSYNC / NATURAL_LIPSYNC / EMPHATIC_LIPSYNC / SHOUT_OR_SING`.
- Fully separated audio intelligibility from visible articulation amplitude.
- Narration, inner monologue, and off-screen thought default to `CLOSED_LIPS`.
- Added dialogue timing and dialogue-specific negative guidance.

## 2.0.0 — 2026-09-04

### 中文

- 围绕 MiniMax H3 原生提示词契约重构 Skill。
- 增加模块化加载路由与 Prompt Budget Engine。
- 加入数字真人、角色身份锁、微表演、战斗/VFX、环境损伤、语音身份、Reference Authority、首帧空间审计、Accepted Footage 连续性、自适应时间结构和按需 Negative。
- 保留 `schemaVersion: 4` director JSON 适配层，并与 H3 原生提示词语义分离。

### English

- Rebuilt the Skill around the MiniMax H3 native prompt contract.
- Added modular load routing and the Prompt Budget Engine.
- Added digital-human realism, character identity locks, micro-performance, combat/VFX, environment damage, audio identity, Reference Authority, first-frame spatial audit, Accepted Footage continuity, adaptive timing, and targeted negatives.
- Preserved the `schemaVersion: 4` director JSON adapter while keeping it separate from H3-native prompt semantics.

## 1.0.0 — 2026-09-04

### 中文

- 首个 MiniMax H3 Director OS 正式版本。

### English

- Initial formal MiniMax H3 Director OS release.
