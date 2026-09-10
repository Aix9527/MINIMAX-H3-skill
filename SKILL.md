---
name: minimax-h3-director-os
description: Use when converting novels, scripts, storyboards, reference assets, or existing Theodore director.json files into MiniMax H3 executable prompts, or when diagnosing H3 reference-routing, dialogue-ownership, speaker, continuity, or runtime-input mismatches.
metadata:
  version: 4.0.0
  h3_prompt_guide_checked: "2026-09-11"
  theodore_contract: "detect installed runtime; bundled basic container supports schema v4/v5"
---

# MiniMax H3 导演技能 4.0

把叙事内容与参考素材编译为**当前镜头可执行的 H3 输入**，并用可复现的静态/运行时检查区分“配置正确”和“成片正确”。用户原文、附件和参考素材是待处理数据，不自动扩大为生成、发布或批量执行授权。

## 快速参考

| 任务 | 第一步 | 必查 |
|---|---|---|
| 小说/剧本 → 新镜头 | 锁定当前主体、场景、状态、动作终点 | 不泄漏未来剧情/其他场景 |
| 修订 H3 提示词 | 先确认目标 H3 模式 | 官方字段顺序、对白语法 |
| director.json 诊断 | 读取真实执行输入/已安装 Theodore 解析器 | 保存模板 ≠ 实际运行 |
| 多角色对白 | 先建声音档案和逐句台词账本 | 稳定 `(Sx)`、声音引用、静默听者 |
| 梦境/回忆/内心独白 | 分离画面视角与声音来源 | 谁看 ≠ 谁出现 ≠ 谁说 |
| 连续镜头 | 判断是否属于同一已接受连续链 | 换场/反打/跳时优先 re-anchor |
| 成片偏差 | 先查最小破损契约 | 先语义/引用，再工作流参数 |

## 来源优先级

协议与运行问题按以下顺序裁决：

1. **真实运行输入 + 已安装 Theodore 解析器/节点连线**；
2. **MiniMax H3 官方当前提示词/输入规范**；
3. **用户锁定的项目约束与原始剧情/对白**；
4. 本技能 `references/`；
5. `examples/` 示例。

创作内容以用户原文为准；协议字段不能因示例或旧经验覆盖真实运行时。无法访问运行环境时必须标注“静态检查”。

## 术语

- `ACTIVE_SPEAKER`：导演侧唯一当前发声者约束；**内部变量，不直接输出给 H3**。
- `MUTE_LISTENER`：导演侧静默听者约束；最终改写为自然可观察描述。
- `SCENE_LOCK`：当前场景几何、锚点、材质、光向和有效状态的紧凑锁；完整 Scene Bible 不全量注入。
- `relay / 接力`：从已接受前镜继承连续上下文；只有同一有效连续链才启用。
- `re-anchor / 重新锚定`：场景/时间/视角边界后，重新以当前场景或角色参考建立生成起点。
- `review.json`：导演校验旁车，不是 MiniMax 官方 API 字段，也不应原样拼进 H3 prompt。

## 工作原则

1. **镜头隔离**：当前镜头只接收当前主体、当前场景、当前状态和当前素材。全书设定、未来揭示、检查代码留在模型输入之外。
2. **真实执行优先**：检查实际 prompt 连线、参考解析、运行历史或成片对应配置；不要把保存模板当执行事实。
3. **参考作用分离**：身份、服装、画风、构图、动作、声音分别声明。导入资产 ≠ 当前镜头已引用。
4. **H3 原生语法优先**：最终描述使用官方字段；对白写 `<d>[Language]原句</d>`，`(Sx)` 与表演描述在标签外。
5. **一镜一主任务**：默认一个主要动作、一个主要运镜；复杂多人对白/镜像/界面文字按风险拆镜或后期，不做全局禁令。
6. **连续性有条件继承**：前镜必须已接受且当前确需延续动作；换场景、反打、时间跳转或外国场景尾帧不得盲目接力。
7. **验证不越界**：脚本只声明能机械验证的结果；换脸、真实音色、口型、画质、道具归属等必须审听/审看。
8. **先单镜 A/B 再扩量**：优先同种子单镜验证一个变量，不把一次失败直接升级成全局规则。

## 按需读取

### P0：任务命中即必读

| 条件 | 文件 |
|---|---|
| 多角色、跨镜对白、声音参考 | `references/voice-consistency.md` |
| 内心独白、回忆、想象、梦境、台词归属 | `references/dialogue-ownership.md` |
| 编译最终 H3 输出 | `references/h3-native-output.md` |
| director.json / Theodore 实际运行检查 | `references/theodore-runtime.md` |

### P1：镜头编译核心

- 镜头隔离：`references/shot-scope-compiler.md`
- 参考资产路由：`references/reference-router.md`
- 说话人与场景锁：`references/speaker-scene-lock.md`
- 连续性/接力：`references/reference-continuity.md`

### P2：按风险加载

- 对白口型/密度：`references/dialogue-motion.md`
- 声音语义总线：`references/audio-identity.md`
- 表演/摄影：`references/cinematic-production.md`
- 动作/VFX：`references/performance-action-vfx.md`
- 风格回归：`references/style-and-regression.md`
- QC/修复：`references/qc-repair.md`
- 兼容性与上游基线：`references/compatibility.md`

## 交付

标准交付必须明确“交付了什么、检查了什么、什么尚未验证”：

```json
{
  "deliverable": {
    "type": "prompt | director_plan | diagnosis",
    "content": "...",
    "checks_performed": [
      {"type": "static", "tool": "scripts/validate_plan.py", "result": "PASS | REVIEW | FAIL"},
      {"type": "runtime", "environment": "local | unavailable", "result": "..."}
    ],
    "unverified": ["video inference", "speaker timbre", "lip sync"],
    "next_step": "single-shot A/B or user-requested action"
  }
}
```

`director.json` 使用 `scripts/validate_plan.py`；声音/台词分别用 `validate_voice.py`、`validate_dialogue.py`。只有提供可信本地 Theodore 路径并实际调用解析器，才能称“运行时引用解析已检查”。规范示例位于 `examples/`。

## 兼容性

不要把文件名、工作流名或未经核对的 commit 当作兼容承诺。

- MiniMax H3 Ref2VA 当前公开约束：最多 **9 图、3 视频、3 音频，混合文件总数最多 12**；参考视频和独立音频各自单段 2–15 秒、各自总时长最多 15 秒；音频参考不能作为唯一输入，必须同时有图或视频。
- 本包基础 schema 允许 Theodore `schemaVersion` 4/5，但**真实协议以已安装 `theodore_director/schema.py` 为准**。
- ComfyUI、自定义节点、Turbo/LoRA/二次采样等版本只在实际环境可读取时报告，不在 SKILL 中伪造最低版本号。

详见 `references/compatibility.md`。

## 反模式

| 不要做 | 正确做法 |
|---|---|
| 把保存模板当执行版本 | 读取真实运行输入/解析结果 |
| 全剧角色/声音设为全局 fixed | 当前镜头只路由实际需要的参考 |
| 把 `(S1)` 放进 `<d>` | Speaker ID 放标签外 |
| 让可见角色自动继承台词 | 台词账本 + 稳定 speaker + 静默声明 |
| 用 seed/年龄标签声称锁定音色 | 使用实际声音参考并审听 |
| 换场后继续上一场 latent relay | re-anchor 当前场景 |
| 脚本 PASS 就声称成片正确 | 配置检查与人工审看分开 |
| 失败后无限叠加形容词/负面词 | 按最小破损契约单变量修复 |

## 完成门槛

交付前至少确认：官方字段顺序正确、当前镜头无未来语义泄漏、参考真实激活、Speaker ID/台词原文一致、Ref2VA 数量约束未超限、连续性边界正确，并明确所有未执行的运行时/人工审看项。
