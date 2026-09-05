# MINIMAX-H3-skill

## 项目简介 / Overview

**MiniMax H3 Director OS V2.3.1** 是一套面向 MiniMax H3 的生产级导演提示词生成 Skill。它整合 H3 原生提示词契约、数字真人、自然对白、说话者唯一归属、场景锁、当前上下文隔离、参考素材白名单、导演资产双向关系一致性、长视频连续性与 QC。

**MiniMax H3 Director OS V2.3.1** is a production-grade director and prompt-generation Skill for MiniMax H3. It combines H3-native formatting, digital-human control, natural dialogue, exclusive speaker ownership, scene locking, active-context isolation, reference allowlisting, bidirectional director asset-link consistency, long-form continuity, and QC.

## V2.3.1 修复 / V2.3.1 Fix

V2.3.1 修复一种实际导播台报错：素材文件真实存在，但镜头通过 `disabledAssetIds` 禁用了该素材，而素材自身的 `assets[].shotIds` 仍声明属于该镜头，导致运行时出现：

```text
未找到或已禁用素材: <asset alias>
```

V2.3.1 fixes a runtime error where an asset file exists, but the shot disables it while the asset's own `shotIds` still claims that shot.

### BIDIRECTIONAL_ASSET_LINK

对任意资产 `A` 和镜头 `S`，必须恒成立：

```text
A.id NOT IN S.disabledAssetIds
    ⇔
S.id IN A.shotIds
```

也就是：镜头启用资产时，资产必须反向声明该镜头；镜头禁用资产时，资产不得继续声明该镜头。

After computing every shot-level `REFERENCE_ALLOWLIST`, V2.3.1 rebuilds all `assets[].shotIds` from the actual disable lists instead of preserving stale relationships from an older project version.

### 自动校验器 / Validator

```bash
python scripts/validate_director_asset_links.py project.director.json
```

自动修复 / Repair:

```bash
python scripts/validate_director_asset_links.py project.director.json --repair --output fixed.director.json
```

完整规则见 [`references/asset-link-consistency.md`](./references/asset-link-consistency.md)。

See [`references/asset-link-consistency.md`](./references/asset-link-consistency.md) for the full contract.

## V2.3 Active Context Isolation / 当前上下文隔离

V2.3 解决实际成片中出现的 **未来场景提前出现、未来人物泄漏、参考图过载导致角色同化** 问题。

核心结构：

```text
Project Database
    ↓
Active Context Filter
    ↓
Reference Allowlist
    ↓
Bidirectional Asset Links
    ↓
Speaker / Scene Locks
    ↓
H3 Prompt
```

项目数据库可以保存完整角色、场景、道具、声纹与参考素材，但每一个 H3 生成段只接收当前活动上下文。

### ACTIVE_CONTEXT_ONLY

每镜只允许进入 H3：

- 当前 `SCENE_ID`；
- 当前可见人物；
- 当前唯一 `ACTIVE_SPEAKER`；
- 当前动作与连续性状态；
- 当前真正需要的参考素材；
- 真正全局的语言、质量、格式与自然口型约束。

未来人物、场景和道具应完全从当前 conditioning 中省略，而不是写成负面句式继续暴露给模型。

完整规则见 [`references/active-context-isolation.md`](./references/active-context-isolation.md)。

### REFERENCE_ALLOWLIST

普通镜头通常只启用 **2–4 个高价值参考**：每名可见人物 1 个主身份参考、1 个当前场景锚点，必要时再加 1 个关键服装/道具参考。

当 `assets` 包含完整项目素材库时，每镜必须通过 `disabledAssetIds` 或等效机制禁用非白名单素材，并同步重建 `assets[].shotIds`。

## V2.2 Speaker Ownership + Scene Lock / 说话者归属 + 场景锁

对白默认一段生成只有一个 `ACTIVE_SPEAKER`，其他人物均为 `MUTE_LISTENER`。Speaker 改变时优先切段；避免“人物 A 离屏长对白 + 人物 B 完整正脸”的高风险构图。

每个重复地点建立 `SCENE_ID + SCENE_LOCK`，锁定空间几何、锚点道具、摄影轴线、材质、主光方向和持续状态。离开场景后返回时使用 `CANONICAL_SCENE_ANCHOR` 重新锚定。

完整规则见 [`references/speaker-scene-lock.md`](./references/speaker-scene-lock.md)。

## V2.1 Natural Dialogue / 自然对白

普通影视对白默认 `SUBTLE_LIPSYNC`：声音保持清晰，但嘴唇只做小幅自然开合，下颌基本稳定；旁白和内心独白要求可见人物 `CLOSED_LIPS`。

## 核心原则 / Core Principles

- **先导演，后编译。** / **Direct first, compile second.**
- **真实成片优先于计划。** / **Accepted footage beats planned footage.**
- **项目数据库与当前生成上下文隔离。** / **Project database and current model context are isolated.**
- **参考素材按镜头白名单启用。** / **References are enabled through a shot-level allowlist.**
- **资产与镜头关系必须双向一致。** / **Asset/shot links must be bidirectionally consistent.**
- **一个对白段默认一个说话者。** / **One dialogue clip defaults to one speaker.**
- **场景是空间状态，不只是风格。** / **A scene is spatial state, not merely style.**
- **声音清晰不等于嘴型明显。** / **Audio clarity does not require strong mouth motion.**

## 架构 / Architecture

```text
SKILL.md
references/
  h3-native-output.md
  cinematic-production.md
  performance-action-vfx.md
  audio-identity.md
  dialogue-motion.md
  speaker-scene-lock.md
  active-context-isolation.md
  asset-link-consistency.md
  reference-continuity.md
  qc-repair.md
  director-json-v4.md
scripts/
  validate_director_asset_links.py
CHANGELOG.md
```

## director.json 运行时说明 / Runtime Notes

自定义 director 工作流可能把 schemaVersion 4 迁移到 schemaVersion 5。Skill 保留运行时实际版本，不强行回退。

如果项目资产池包含几十张素材：

1. 每镜先计算 `REFERENCE_ALLOWLIST`；
2. 生成完整 `disabledAssetIds`；
3. 反向重建所有 `assets[].shotIds`；
4. 运行资产关系校验器；
5. 校验通过后再交付。

文件存在性和关联关系应分开检查。若 alias 在资产包中存在，且 `fingerprint` 与文件 SHA256 一致，应优先修复关联关系，而不是重新生成图片。

## 支持任务 / Supported Tasks

- T2VA / I2VA / FL2VA / L2VA / Ref2VA
- 小说、剧本、分镜转 H3
- 多人物对白与声纹锁
- 旁白与内心独白
- 重复场景与空间连续性
- 大型参考素材库按镜头路由
- schemaVersion 4/5 `.director.json` 修复与校验
- 数字真人、动作、战斗、VFX
- 多段长视频
- Prompt 诊断与修复

## 公开命名规范 / Public Naming Policy

对外文档仅使用功能名、Skill 名、框架类型与版本号描述来源和演进；无关个人名、作者名或外部项目品牌名不进入公开说明、Release Notes 或示例文本。

## 版本发布 / Releases

所有正式版本必须具备 **版本号 + Git Tag + GitHub Release**。

- **v2.3.1 — MiniMax H3 Director OS V2.3.1** — Bidirectional Asset-Link Fix / 资产双向关系修复
- **v2.3.0 — MiniMax H3 Director OS V2.3** — Active Context Isolation / 当前上下文隔离
- **v2.2.0 — MiniMax H3 Director OS V2.2** — Speaker Ownership + Scene Lock
- **v2.1.1 — MiniMax H3 Director OS V2.1.1** — H3 Dialogue Syntax + Mandarin Lock
- **v2.1.0 — MiniMax H3 Director OS V2.1** — Natural Dialogue
- **v2.0.0 — MiniMax H3 Director OS V2.0** — Production Modular Rebuild
- **v1.0.0 — MiniMax H3 Director OS V1.0** — Initial Release

查看所有版本 / View all releases: https://github.com/Aix9527/MINIMAX-H3-skill/releases

## 当前版本 / Current Version

**v2.3.1 — MiniMax H3 Director OS V2.3.1**
