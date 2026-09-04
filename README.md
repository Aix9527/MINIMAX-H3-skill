# MINIMAX-H3-skill

## 项目简介 / Overview

**MiniMax H3 Director OS V2.0** 是一套面向 MiniMax H3 的生产级导演提示词生成 Skill。它把 H3 原生提示词契约、电影导演方法、数字真人控制、物理表演、战斗/VFX、语音身份、参考素材权限、长视频连续性与 QC 融合到同一套系统中，同时避免把整套制作圣经机械复制到每一个镜头。

**MiniMax H3 Director OS V2.0** is a production-grade director and prompt-generation Skill for MiniMax H3. It combines the H3-native prompt contract, cinematic directing, digital-human control, physical performance, combat/VFX, audio identity, reference authority, long-video continuity, and QC in one system—without mechanically pasting the entire production bible into every shot.

## V2.0 设计目标 / V2.0 Design Goal

> 比上一代 V10.2 生产框架提供更多可控能力，同时减少重复提示词，并比 V1.0 更严格地遵守 MiniMax H3 原生格式。
>
> More control than the prior V10.2 production framework, less duplicated prompt text, and stricter MiniMax H3-native formatting than V1.0.

## 核心原则 / Core Principles

- **先导演，后编译。** 先确定叙事任务、Blocking、表演、物理因果、摄影机意图、灯光、声音与结束状态，再编译成 H3 提示词。  
  **Direct first, compile second.** Decide narrative job, blocking, performance, physical causality, camera intent, lighting, sound, and endpoint before compiling H3 prompts.
- **真实成片优先于计划。** 上一段已接受成片的真实尾帧和真实结束状态优先于旧计划。  
  **Accepted footage beats planned footage.** The real ending of accepted prior footage overrides what the old plan expected.
- **Blocking before Camera。** 先安排人物在空间里怎么动，再决定镜头怎么动。  
  **Blocking before Camera.** Place and move subjects in space before choosing camera movement.
- **Prompt Budget Engine。** 全局常量、当前镜头变量、交接状态分层管理，不把所有信息重复写进每镜。  
  **Prompt Budget Engine.** Separate project invariants, shot variables, and handoff state instead of repeating everything in every shot.
- **Negative 按需启用。** 只写本镜真实存在的风险。  
  **Targeted negatives only.** Add only the failure risks actually activated by the current shot.

## 架构 / Architecture

```text
SKILL.md                         # 路由 + 导演大脑 + Prompt Budget 编译器 / router + director brain + prompt-budget compiler
references/
  h3-native-output.md            # H3 原生字段与模式契约 / H3 native field and mode contract
  cinematic-production.md        # 数字真人、角色锁、微表演、摄影与灯光 / digital human, character lock, micro-performance, camera/light
  performance-action-vfx.md      # 身体物理、战斗、冲击、VFX、环境损伤 / body physics, combat, impact, VFX, environment damage
  audio-identity.md              # 对白、声纹、旁白与混音 / dialogue, voice identity, narration, mix
  reference-continuity.md        # Reference 权限、首帧审计、Accepted Footage 连续性 / reference authority, first-frame audit, accepted-footage canon
  qc-repair.md                   # 校验、Take Review 与修复阶梯 / validation, take review, repair ladder
  director-json-v4.md            # 可选 V9/V10.2 兼容 director.json 容器 / optional V9/V10.2-compatible director.json container
docs/
  SOURCE_COMPARISON.md           # 各来源 Skill 优缺点与融合依据 / source-by-source comparison and merge rationale
CHANGELOG.md                     # 版本更新记录 / version changelog
```

## 从 V1.0 到 V2.0 的变化 / What Changed from V1.0

V1.0 的 H3 导演大脑更聚焦，但实际输出有时过于精简。V2.0 恢复了 V10.2 生产框架中最有价值的生产控制能力：数字真人、角色身份锁、微表演、战斗/VFX、环境损伤、语音身份和自适应时间节拍，同时把这些能力改成按需加载，而不是每镜完整重复。

V1.0 had a stronger H3-focused director brain, but practical outputs could become too thin. V2.0 restores the most valuable controls from the V10.2 production framework—digital-human realism, character identity locks, micro-performance, combat/VFX, environment damage, voice identity, and adaptive timing—while routing them only when needed instead of repeating them wholesale in every shot.

### Prompt Budget Engine / 提示词预算引擎

1. **项目级常量 / Project invariants** — 世界/风格、Canonical Identity、Voice、持续状态。 / world/style, canonical identity, voice, persistent state.
2. **镜头级变量 / Shot variables** — 当前动作、摄影、VFX、对白、声音与 Endpoint。 / current action, camera, VFX, dialogue, sound, endpoint.
3. **交接状态 / Handoff state** — Accepted End State、未完成动作、损伤与连续性事实。 / accepted end state, unfinished motion, damage, continuity facts.

这样可以避免旧式做法中把 6–10K 字符的全局制作圣经重复粘贴到每个镜头。

This prevents the old pattern of pasting a 6–10K-character global production bible into every shot.

## 支持任务 / Supported Tasks

- T2VA 文本生成音视频 / text-to-audio-video
- I2VA 首帧图生音视频 / first-frame image-to-audio-video
- FL2VA 首尾帧约束生成 / first-and-last-frame generation
- L2VA 尾帧约束生成 / last-frame-constrained generation
- Ref2VA 全参考、编辑与续写 / full multimodal reference, edit, and continuation
- 对白与旁白场景 / dialogue and narration scenes
- 数字真人与国漫真人感场景 / digital-human and guoman-realism scenes
- 动作、战斗、神通与 VFX 场景 / action, combat, spell, and VFX scenes
- 多段长视频 / multi-segment long-form video
- Prompt 诊断与修复 / prompt diagnosis and repair
- 现有 `schemaVersion: 4` `.director.json` 工作流 / established `schemaVersion: 4` `.director.json` workflow

## MiniMax H3 原生基线 / Official H3 Baseline

MiniMax 公开资料将 H3 描述为统一多模态视频模型，可理解文本、图像、视频与音频上下文，并原生生成视频与立体声音频；公开资料支持最长 15 秒、最高 2K。官方 Prompt Skill 使用 T2VA / I2VA / FL2VA / L2VA / Ref2VA，并保持固定的字段顺序。

MiniMax public materials describe H3 as an omni-modal video model that understands text, image, video, and audio context and natively generates video with stereo audio; public materials list clips up to 15 seconds and up to 2K. The official prompt-writing Skill uses T2VA / I2VA / FL2VA / L2VA / Ref2VA with fixed section ordering.

### 官方来源 / Official Sources

- https://github.com/MiniMax-AI/MiniMax-H3
- https://github.com/MiniMax-AI/MiniMax-H3/tree/main/skills/h3-prompt-writing
- https://www.minimax.io/news/minimax-h3-open-source

目标运行时如果有更窄的时长、分辨率或参数限制，应以项目/运行时配置优先。

If a target runtime imposes narrower duration, resolution, or parameter limits, project/runtime settings take precedence.

## 使用方法 / Usage

加载仓库根目录 [`SKILL.md`](./SKILL.md)，然后直接用自然语言提出任务。

Load the repository root [`SKILL.md`](./SKILL.md), then ask naturally.

### 示例 1：小说转 H3 / Example 1: Novel to H3

```text
把这段小说改成 5 个 MiniMax H3 生成段。人物用参考图锁定，战斗段保留物理接触和环境损伤，输出可直接复制的 H3 提示词。

Convert this novel excerpt into 5 MiniMax H3 generation segments. Lock character identity with reference images, preserve physical contact and environment damage in combat scenes, and output H3 prompts ready to copy.
```

### 示例 2：尾帧续写 / Example 2: Continue from Accepted Tail Frame

```text
根据上一段真实尾帧继续 8 秒，不重复上一段已经完成的转身动作；保持角色身份、衣服、屏幕方向和光线，最后停在可继续生成的稳定画面。

Continue for 8 seconds from the actual accepted tail frame. Do not repeat the completed turn from the previous clip; preserve identity, wardrobe, screen direction, and lighting, and end on a stable frame suitable for further continuation.
```

### 示例 3：导播台 JSON / Example 3: Director JSON

```text
按我的 V10.2 schemaVersion 4 格式输出 director.json。

Output director.json using my V10.2 schemaVersion 4 format.
```

## 来源对比 / Source Review

V2.0 是在对比多套 H3 Prompt Skill、导演框架、98 个电影微 Skill、Seedance 2.0、ComfyUI-H3-Director、V9/V10.2 生产框架与 V1.0 后重构的。完整优缺点与融合依据见 [`docs/SOURCE_COMPARISON.md`](./docs/SOURCE_COMPARISON.md)。

V2.0 was rebuilt after comparing multiple H3 prompt Skills, director frameworks, the 98-skill film craft library, Seedance 2.0, ComfyUI-H3-Director, the V9/V10.2 production frameworks, and V1.0. See [`docs/SOURCE_COMPARISON.md`](./docs/SOURCE_COMPARISON.md) for the full strengths/weaknesses review and merge rationale.

## 公开命名规范 / Public Naming Policy

对外文档仅使用功能名、Skill 名、框架类型与版本号描述来源和演进；与本仓库无关的个人名、作者名或外部项目品牌名不进入公开说明、Release Notes 或示例文本。

Public-facing documentation uses capability names, Skill names, framework types, and version labels to describe sources and evolution. Unrelated personal names, author names, or external project-brand names are omitted from public documentation, release notes, and examples.

## 版本发布 / Releases

所有正式版本都必须同时具备 **版本号 + Git Tag + GitHub Release**。README 中出现的正式版本不得只存在于 commit 历史中。

Every formal version must have a **version number + Git tag + GitHub Release**. A formal version shown in the README must not exist only in commit history.

- **v2.0.0 — MiniMax H3 Director OS V2.0** — 当前稳定版本 / current stable version
- **v1.0.0 — MiniMax H3 Director OS V1.0** — 首个正式版本 / initial formal release

查看所有版本 / View all releases: https://github.com/Aix9527/MINIMAX-H3-skill/releases

### 以后版本的发布规则 / Release Policy for Future Versions

1. 更新 `SKILL.md` 中的版本号。 / Update the version in `SKILL.md`.
2. 更新 `CHANGELOG.md`，说明新增、修复和兼容性变化。 / Update `CHANGELOG.md` with features, fixes, and compatibility changes.
3. 创建同版本 Git Tag，例如 `v2.1.0`。 / Create a matching Git tag, e.g. `v2.1.0`.
4. 创建对应 GitHub Release，并使用中英双语 Release Notes。 / Create the matching GitHub Release with bilingual release notes.
5. Release 必须指向该版本真实代码提交，而不是随意指向最新 `main`。 / The Release must point to the actual version commit, not arbitrarily to the latest `main`.

## 当前版本 / Current Version

**v2.0.0 — MiniMax H3 Director OS V2.0**
