# Speaker Ownership & Scene Lock / 说话者归属与场景锁

## 中文

该模块解决两类高频错误：

1. 人物 A 的台词被人物 B 说出；
2. 同一地点在不同生成段中发生房间布局、道具位置、光线方向或空间关系漂移。

涉及未来剧情/场景/人物状态泄漏时，同时读取 [Shot Scope Compiler](shot-scope-compiler.md)。

## 1. ACTIVE_SPEAKER 唯一对白所有权

对白镜头默认建立一个唯一的 `ACTIVE_SPEAKER`。

每个有声人物镜头先明确：

`ACTIVE_SPEAKER = 角色名 + 稳定 Speaker ID + 画面位置 + 声音来源位置`

硬规则：

- 默认每个生成段只有一个对白所有者。
- 当前 `ACTIVE_SPEAKER` 是唯一允许产生人类对白声音和可见对白口型的人。
- 所有其他可见人物标记为 `MUTE_LISTENER`：不发声、不继承台词、嘴唇闭合或近闭合，只做听者反应。
- Speaker ID 必须位于 `<d>` 外部；`<d>` 内只保留语言标签与准确台词。
- 台词应紧邻说话者身份描述，不把角色名、台词和镜头动作分散到很远的位置。
- 声音的空间来源必须与 `ACTIVE_SPEAKER` 的画面位置一致。
- 如果对白所有权从人物 A 切换到人物 B，优先切成新的生成段。
- 除非剧情明确要求，不在同一生成段中放置两个不同 Speaker ID 的对白。

推荐编译：

```text
ACTIVE_SPEAKER = RIVAL_GIRL (S2), screen-right, three-quarter view.
Only RIVAL_GIRL (S2) may speak in this clip.
YUYUE_17 (S1) is MUTE_LISTENER: lips closed, no speech, no phoneme motion.
RIVAL_GIRL (S2) says: <d>[Chinese] 你到底想干什么？</d>
```

## 2. 禁止高风险“听者正脸 + 离屏长对白”

普通情况下不要采用：

`人物 A 开始说话 → 切人物 B 完整正脸 → A 离屏继续说很久`

这会使模型把剩余声音重新绑定到当前最显眼的人脸。

如果必须让对白离屏继续：

- 不显示另一名人物的完整正脸嘴部；
- 优先使用背影、后脑、肩部、手部、环境插入镜头；
- 明确 `ALL VISIBLE MOUTHS = CLOSED_LIPS`；
- 明确声音从原说话者所在方向继续；
- 离屏持续时间尽量短。

更稳妥的默认策略：**拆成下一段，仍让原说话者作为唯一可见/主要可见对白主体。**

## 3. Speaker Handoff Barrier

当下列任一条件成立时，默认切段：

- Speaker ID 改变；
- 两个人连续互相说话；
- 长台词需要明显切换画面主体；
- 说话者要完全离开画面但声音还要持续；
- 当前镜头已经出现过一次错误说话者。

切段后的新镜头重新声明新的 `ACTIVE_SPEAKER`，不得继承上一镜的对白所有权。

## 4. SCENE_ID 场景锁

每个需要跨生成段保持一致的地点，创建稳定 `SCENE_ID`。

例如：

`SCENE_ID = BEDROOM_A`

为每个 `SCENE_ID` 固定以下不可漂移信息：

- 核心空间几何；
- 墙、门、窗、床、柜子等锚点的相对位置；
- 人物可通行路径；
- 主要道具的位置与朝向；
- 摄影机所在轴线/常用侧；
- 主光来源、方向、色温和时间相位；
- 地面、墙体、主要材质；
- 已经发生且在当前时间点有效的损坏、污渍、伤口或物件状态。

这些信息构成该场景的 Director-side `SCENE_LOCK`。

## 5. 完整 Scene Bible 只属于 Director，不属于运行时 H3

**完整 Scene Bible 不得作为全局 runtime Prompt 注入所有镜头。**

Director/compiler 可以保存整个项目的所有场景资料，但当前 H3 生成段只接收：

- 当前 `SCENE_ID`；
- 当前场景的一条紧凑 `SCENE_LOCK`；
- 当前时间点有效的场景状态；
- 当前需要的 canonical scene anchor/reference。

每个属于该场景的生成段都重复紧凑场景锁，例如：

```text
SCENE_LOCK BEDROOM_A:
left wall = bed; right wall = old wooden cabinet with small mirror;
rear-right = doorway; packed-earth floor; earth-brick walls;
old timber rafters overhead; dim natural light enters from rear-right;
geometry, prop positions and light direction must remain unchanged.
```

不要把其他未来场景、梦境场景、闪回场景或尚未出现的场景描述一起塞进 `promptPrefix`。不要假设“写了不要切场”就能抵消其他场景名称已经进入模型上下文所造成的语义泄漏。

## 6. Accepted Scene Anchor

一个场景第一次得到可接受画面后：

- 选取该场景最稳定、最能说明空间关系的一帧作为 `CANONICAL_SCENE_ANCHOR`；
- 同场连续镜头优先从上一段真实尾帧继续；
- 离开该场景再返回时，不使用中间蒙太奇/其他场景的尾帧作为视觉锚点；
- 返回时重新使用 `CANONICAL_SCENE_ANCHOR` 或该场景专用参考图进行 I2VA/Ref2VA re-anchor；
- 如果运行时无法传入场景参考图，至少重新声明完整紧凑 `SCENE_LOCK`，并关闭不正确的跨场景 latent relay。

## 7. Scene Return Barrier

以下情况必须重新锚定场景而不是直接继承上一段：

- 蒙太奇后返回旧地点；
- 梦境/回忆后返回现实地点；
- 时间跳跃后返回同一地点；
- 中间生成段属于另一个 `SCENE_ID`；
- 当前场景几何已经出现漂移。

返回镜头使用：

`RE-ANCHOR SCENE_ID = ...; ignore the immediately previous foreign-scene geometry.`

并重新构建当前镜头的 `ACTIVE_REFERENCE_SET`，不得保留上一外国场景的环境参考。

## 8. 场景一致性 Negative

仅在存在漂移风险时加入抽象风险族：

`scene redesign, room layout drift, prop relocation, doorway relocation, window relocation, furniture replacement, light direction drift, wall material drift, spatial reset, location substitution, unmotivated scene change`

不要为了否定未来场景而把未来场景名称写进 Negative。详细未来名词仍然属于语义泄漏。

## 9. QC

对白镜头交付前检查：

- 是否只有一个 `ACTIVE_SPEAKER`；
- 是否所有其他人物都明确 `MUTE_LISTENER`；
- 是否存在另一个完整正脸在承接离屏长对白；
- Speaker ID 是否在 `<d>` 外；
- 声音来源方向是否与说话者位置一致；
- ACTIVE_SPEAKER 的身份/状态参考是否被另一角色的大量参考图压过。

场景镜头交付前检查：

- `SCENE_ID` 是否明确；
- 紧凑 `SCENE_LOCK` 是否重复到当前镜头；
- 锚点位置、主光方向、材质是否与前镜一致；
- 返回旧场景时是否使用 canonical scene anchor 或显式 re-anchor；
- 是否误把其他场景/蒙太奇尾帧作为当前场景连续性来源；
- runtime prefix/suffix 是否泄漏其他场景描述。

---

## English

This module prevents two common failures: dialogue migrating to the wrong visible character and spatial redesign of the same location across generated clips. For future-state/scene leakage, also use [Shot Scope Compiler](shot-scope-compiler.md).

### ACTIVE_SPEAKER

Default to exactly one dialogue owner per generated clip. Declare `ACTIVE_SPEAKER = character + stable speaker ID + screen position + spatial audio origin`. Only that speaker may produce human dialogue audio and visible speech articulation. Every other visible person is a `MUTE_LISTENER` with closed or near-closed lips and listening-only behavior.

Keep speaker IDs outside `<d>`. Keep the spoken line adjacent to the speaker declaration. When dialogue ownership changes to another character, split to a new generation segment by default.

### Avoid high-risk off-screen reassignment

Do not default to `speaker A talks → cut to listener B's full frontal face → A continues a long off-screen line`. If off-screen speech is necessary, avoid showing another complete mouth-forward face; prefer back-of-head, shoulder, hand, or environment inserts, explicitly close all visible lips, lock the audio origin to the original speaker's direction, and keep the off-screen portion short.

### SCENE_ID and SCENE_LOCK

Give every recurring location a stable `SCENE_ID` and lock its geometry, anchor-object positions, traversable paths, camera axis, material identity, light source/direction, time phase, and persistent state that is already valid at the current story time.

The complete Scene Bible is Director/compiler knowledge only. It must not be injected into every runtime H3 prompt. Each generated segment receives only the current `SCENE_ID`, a compact current-scene `SCENE_LOCK`, current state deltas and current canonical scene reference when needed.

### Accepted Scene Anchor

After the first accepted view of a location, save a stable frame as the `CANONICAL_SCENE_ANCHOR`. Continue adjacent shots from accepted tail frames when appropriate. When returning after a montage, dream, flashback, time jump, or another scene, re-anchor from the canonical scene image/reference rather than inheriting the immediately previous foreign-scene tail.

### Scene consistency negatives

When risk exists, use abstract risk categories such as: `scene redesign, room layout drift, prop relocation, doorway relocation, window relocation, furniture replacement, light direction drift, wall material drift, spatial reset, location substitution, unmotivated scene change`.

Do not inject detailed future scene nouns merely to negate them.
