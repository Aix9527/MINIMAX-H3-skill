# 更新日志 / Changelog

## 2.2.0 — 2026-09-05

### 中文

- 新增 `Speaker Ownership & Scene Lock` 模块。
- 对白生成默认改为“一段生成一个 `ACTIVE_SPEAKER`”，其他可见人物必须为 `MUTE_LISTENER`。
- Speaker 改变时优先切成新的生成段，降低人物 A 的台词从人物 B 口中说出的概率。
- 禁止把“人物 A 长时间离屏说话 + 人物 B 完整正脸”作为默认减口型方案。
- Speaker ID 继续强制位于 `<d>` 外部，`<d>` 内只保留语言标签和准确台词。
- 新增声音空间来源锁：对白声源必须与 `ACTIVE_SPEAKER` 的画面位置一致。
- 新增 `SCENE_ID + SCENE_LOCK`：锁定空间几何、锚点道具、门窗/床/柜子相对位置、摄影轴线、材质、主光方向、时间相位和持续状态。
- 同一场景每个生成段都重复紧凑场景锁，不再只依赖全局 Prompt。
- 新增 `CANONICAL_SCENE_ANCHOR` 策略：场景首次生成成功后保存稳定锚点帧；离开后返回时重新锚定，不继承蒙太奇/梦境/其他场景尾帧。
- 新增 Speaker Handoff Barrier 与 Scene Return Barrier。
- 新增场景一致性 Negative：`scene redesign, room layout drift, prop relocation, doorway relocation, window relocation, furniture replacement, light direction drift, wall material drift, spatial reset`。
- 修正 V2.1 中“长对白可默认切听者正脸并离屏继续”的高风险策略，改为优先拆段或保留原说话者为视觉主体。

### English

- Added the `Speaker Ownership & Scene Lock` module.
- Dialogue generation now defaults to one `ACTIVE_SPEAKER` per generated clip; all other visible people are `MUTE_LISTENER`.
- A speaker change normally starts a new generation segment, reducing dialogue reassignment to the wrong face.
- Long off-screen speech over another character's full frontal face is no longer a default mouth-motion reduction strategy.
- Speaker IDs remain outside `<d>`; only language tags and exact spoken words remain inside `<d>`.
- Added spatial audio-origin locking so dialogue stays tied to the active speaker's screen position.
- Added `SCENE_ID + SCENE_LOCK` for geometry, anchor props, door/window/bed/cabinet relationships, camera axis, materials, primary-light direction, time phase, and persistent state.
- Every generated clip in a recurring location repeats a compact scene lock instead of relying only on a global prompt.
- Added `CANONICAL_SCENE_ANCHOR`: after a scene is accepted, save a stable anchor frame; when returning later, re-anchor instead of inheriting a montage/dream/foreign-scene tail.
- Added Speaker Handoff Barrier and Scene Return Barrier.
- Added scene-consistency negatives for layout, prop, doorway/window, material, and light-direction drift.
- Replaced the high-risk V2.1 pattern of long off-screen speech over a full listener face with segment splitting or continued visual ownership by the original speaker.

## 2.1.1 — 2026-09-05

### 中文

- 修正 H3 对白语法：Speaker ID 必须位于 `<d>` 外部。
- 中文项目所有可听对白、旁白、内心独白与离屏人声强制使用 `<d>[Chinese] ...</d>`。
- 同一人物内心独白复用原 Speaker ID，不使用非标准 `S1-VO` 标记。
- 英文镜头描述仅作为指令，不允许被朗读或翻译成英文对白。

### English

- Corrected H3 dialogue syntax so speaker IDs stay outside `<d>`.
- Mandarin projects require `<d>[Chinese] ...</d>` for all audible dialogue, narration, inner monologue, and off-screen human speech.
- Same-character voiceover reuses the original speaker ID instead of noncanonical `S1-VO` markup.
- English scene prose is instruction-only and must not be spoken or substituted for dialogue.

## 2.1.0 — 2026-09-04

### 中文

- 新增 `Natural Dialogue Motion` 自然对白口型模块。
- 普通影视对白默认改为 `SUBTLE_LIPSYNC`，不再把“正确同步”理解成明显嘴唇和下颌运动。
- 新增 `CLOSED_LIPS / SUBTLE_LIPSYNC / NATURAL_LIPSYNC / EMPHATIC_LIPSYNC / SHOUT_OR_SING` 五级口型模式。
- 将声音清晰度与可见口型幅度彻底分离。
- 旁白、内心独白和离屏思绪默认 `CLOSED_LIPS`。
- 新增对白时间结构与对白专用 Negative。

### English

- Added the `Natural Dialogue Motion` module.
- Ordinary cinematic dialogue now defaults to `SUBTLE_LIPSYNC`.
- Added five lip-motion modes.
- Separated audio intelligibility from visible articulation amplitude.
- Narration, inner monologue, and off-screen thought default to `CLOSED_LIPS`.
- Added dialogue timing structure and dialogue-specific negatives.

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
