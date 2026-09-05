# Active Context Isolation / 当前上下文隔离

## 中文

该模块用于防止长项目中的“未来内容泄漏”：当前镜头本来只需要河边与两名人物，但项目级 Prompt 或素材池中同时存在未来的卧室、老人、工厂、梦境等信息，模型可能在当前片段后半段提前把这些内容生成出来。

核心原则：**项目数据库可以很完整，但送给 H3 的单镜上下文必须很窄。**

## 1. ACTIVE_CONTEXT_ONLY

每次生成前先从项目数据库编译一个当前上下文切片，只允许进入本镜：

- 当前 `SCENE_ID`；
- 当前可见人物；
- 当前唯一 `ACTIVE_SPEAKER`（有对白时）；
- 当前动作与连续性状态；
- 当前真正需要的参考素材；
- 当前必要的风格/语言/质量硬锁。

未来场景、未来人物、未来道具、未来剧情、未激活的参考素材不得进入当前 H3 Prompt。

不要通过负面句式告诉模型未来内容“不要出现”，例如：

```text
Do not show the grandmother or bedroom yet.
```

这仍然把 grandmother / bedroom 概念暴露给模型。更安全的做法是：**完全不把这些概念编译进当前生成上下文。**

## 2. Global Prompt 白名单

`promptPrefix` / `promptSuffix` 只允许真正全局且不会触发未来视觉内容的信息：

- 目标语言；
- 通用视觉质量与数字真人规则；
- 通用对白语法；
- 通用口型幅度规则；
- 通用安全/格式约束；
- 不指向具体未来实体的连续性原则。

禁止放入全项目角色注册表、完整场景注册表、未来剧情摘要、未来道具清单、所有人物声纹详细定义。

具体人物、场景与道具应在当前 `shot.prompt` 中按需编译。

## 3. REFERENCE_ALLOWLIST

长项目的素材库可以包含大量图片，但每个生成段必须建立镜头级参考白名单。

默认建议：

- 单人镜头：1 个角色主身份参考 + 1 个当前场景参考；必要时再加 1 个服装/道具参考；
- 双人镜头：每人最多 1 个主身份参考 + 1 个当前场景参考；必要时最多再加 1 个关键服装/道具参考；
- 普通镜头优先总计 2–4 个高权重参考，而不是把同一角色的眼睛、嘴、手、动作、表情、转面等十几张细节图全部同时注入；
- 当前镜头未使用的资产必须通过运行时禁用机制排除，例如 `disabledAssetIds`。

多张同一角色参考可能形成过强单角色先验；当镜头还要求第二名相似年龄角色时，会提高“角色二被角色一同化”、身份混淆和 Speaker Swap 风险。

## 4. Reference Authority

每个启用参考都必须声明它控制什么：

- identity；
- wardrobe；
- environment；
- composition；
- motion；
- voice；
- prop。

没有明确控制维度的参考不进入本镜。

同一维度尽量只保留一个赢家。例如角色身份已经由主肖像控制，就不要再同时加载多张眼部、唇部、表情、转面图，除非当前镜头确实需要修复对应维度。

## 5. 场景隔离

当前镜头只包含一个活动场景定义：

```text
ACTIVE_SCENE = SCENE_RIVER_A
SCENE_LOCK: ...
```

不要在同一 H3 Prompt 中同时定义 `SCENE_RIVER_A + SCENE_VOID_A + SCENE_BEDROOM_A`。

项目可以在导演数据库中保存三个场景，但编译到 H3 时只能选择当前活动场景。

## 6. 人物隔离

当前镜头只编译可见人物和必要离屏声源。未出现的未来人物不进入 H3 Prompt。

双人对白推荐：

```text
VISIBLE_CHARACTERS = YUYUE_17 (S1), RIVAL_GIRL (S2)
ACTIVE_SPEAKER = RIVAL_GIRL (S2)
MUTE_LISTENER = YUYUE_17 (S1)
```

不要把奶奶、父母、未来梦中人物等完整身份描述同时放在这个河边镜头的全局前缀中。

## 7. Shot Compiler Gate

编译完成后执行硬检查：

- 当前 Prompt 是否出现不属于本镜的未来 `SCENE_ID`？有则失败；
- 是否出现当前不可见且无离屏声音任务的角色名/身份描述？有则失败；
- 启用参考是否超过当前镜头所需维度？超出则裁剪；
- `disabledAssetIds` 是否真正排除了非白名单资产？如果工作流支持该字段但为空，应视为高风险；
- 当前镜头是否同时存在多个场景锚点？有则失败；
- 当前镜头是否同时存在大量同一角色细节参考和第二人物？有则优先缩减参考。

## 8. 与 Scene Lock 的关系

`SCENE_LOCK` 解决“同一个场景不要漂移”；`ACTIVE_CONTEXT_ONLY` 解决“别把其他场景提前生成进来”。两者必须同时存在。

推荐顺序：

`Project DB → Active Context Filter → Reference Allowlist → Scene/Speaker Locks → H3 Prompt`

---

## English

This module prevents **future-context leakage** in long projects. A project database may contain many future characters, locations, props, and references, but a single H3 generation should receive only the context that is active now.

### ACTIVE_CONTEXT_ONLY

Compile only the current scene, visible characters, active speaker, current continuity state, required references, and truly global quality/language constraints. Do not expose future scenes or future characters even in negative wording.

### Global prompt allowlist

Global prefix/suffix may contain language, universal quality, dialogue syntax, natural lip-motion rules, format constraints, and generic continuity principles. Do not place the full project character registry, scene registry, future-plot summary, or future prop list in the global H3 prompt.

### REFERENCE_ALLOWLIST

Use a small shot-level reference set. As a default, prefer 2–4 high-value references per ordinary shot: one primary identity reference per visible character, one active-scene anchor, and only an additional wardrobe/prop reference when truly needed. Disable all non-allowlisted assets at runtime, for example through `disabledAssetIds` when supported.

Loading many eye/lip/hand/expression/turnaround images for one character while also asking for a second similar character can create an overpowering single-character prior, increasing identity cloning and speaker confusion.

### Scene isolation

Only one active scene definition enters a clip. The director database may know many scenes, but the H3 prompt should receive only `ACTIVE_SCENE = current_scene` plus its compact lock.

### Compiler gate

Fail compilation when the current prompt contains a future scene, an irrelevant future character, unnecessary references, multiple competing scene anchors, or an empty asset-disable list in a runtime that otherwise exposes the whole project asset pool.

`SCENE_LOCK` prevents the active scene from drifting. `ACTIVE_CONTEXT_ONLY` prevents inactive scenes from leaking into the active clip. Use both.