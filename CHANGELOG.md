# 更新日志 / Changelog

## 2.1.0 — 2026-09-04

### 中文

- 新增 `Natural Dialogue Motion` 自然对白口型模块。
- 普通影视对白默认改为 `SUBTLE_LIPSYNC`，不再把“正确同步”理解成明显嘴唇和下颌运动。
- 新增 `CLOSED_LIPS / SUBTLE_LIPSYNC / NATURAL_LIPSYNC / EMPHATIC_LIPSYNC / SHOUT_OR_SING` 五级口型模式。
- 将声音清晰度与可见口型幅度彻底分离：声音可以清楚、靠前、可懂，但嘴部仍保持低幅自然动作。
- 旁白、内心独白和离屏思绪默认 `CLOSED_LIPS`，可见人物不得跟随旁白做口型。
- 新增对白时间结构：`反应/吸气 → 说话 → 停顿 → 嘴部回落 → 反应`。
- 长对白优先拆句、延长镜头、切听者反应或离屏继续说话，避免高速连续动嘴。
- 新增对白摄影建议：普通对白优先中近景、三分之四侧角和自然视平线，避免把嘴持续放在视觉中心。
- 新增对白专用 Negative：过度嘴唇运动、过度咬字、重复大张嘴、下颌抽动、咀嚼式说话和停顿时嘴仍持续运动。
- README 更新为 V2.1 中英双语说明。
- 发布工作流增加 Skill 合同校验并自动同步当前版本 Tag 与 GitHub Release。

### English

- Added the `Natural Dialogue Motion` module.
- Ordinary cinematic dialogue now defaults to `SUBTLE_LIPSYNC` instead of treating correct synchronization as strong visible lip and jaw motion.
- Added five lip-motion modes: `CLOSED_LIPS / SUBTLE_LIPSYNC / NATURAL_LIPSYNC / EMPHATIC_LIPSYNC / SHOUT_OR_SING`.
- Fully separated audio intelligibility from visible articulation amplitude: speech may remain clear, foregrounded, and intelligible while mouth motion stays restrained.
- Narration, inner monologue, and off-screen thought now default to `CLOSED_LIPS`; visible characters must not articulate voiceover.
- Added dialogue timing structure: `reaction / inhale → speech → pause → mouth settles → reaction`.
- Long lines should be split, given more time, covered with listener reactions, or continued off-screen instead of forcing rapid continuous mouth motion.
- Added dialogue-camera guidance: prefer medium close-ups, three-quarter angles, and natural eye level for ordinary speech rather than making the mouth the persistent visual focal point.
- Added dialogue-specific negatives for exaggerated lip motion, over-articulation, repetitive large openings, excessive jaw pumping, chewing-like speech motion, and mouth movement that continues through pauses.
- Updated the README with bilingual V2.1 documentation.
- Added Skill contract checks and automatic current-version Tag/Release synchronization to the release workflow.

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
