# 角色声音档案与跨镜一致性

目标有两个：**同一角色跨镜保持可辨认的声音身份**；**不同角色不串台、不共用错误声线**。年龄标签、角色名或固定 seed 只能辅助，不构成音色锁定证明。

## 1. 声音身份与画面身份分离

- 参考图回答“长什么样”；
- 参考音频回答“听起来是谁”；
- `speakerId` 回答“这条声音在全片属于哪个稳定发声源”；
- 当前镜头的情绪/音量/语速属于表演状态，不应覆盖角色声音身份。

角色不在画面中仍可保留声音身份；角色在画面中也不代表它自动获得当前台词。

## 2. 导演侧声音档案

使用 `review.json -> voices` 保存声音注册表。它是**校验旁车**，不是 MiniMax 官方 API 字段，也不能原样拼入 H3 prompt。

推荐结构：

```json
{
  "voices": {
    "CHEN": {
      "speakerId": "S1",
      "voiceAlias": "CHEN_VOICE",
      "language": "Chinese",
      "ageImpression": "young adult man",
      "timbre": "low, clear, restrained",
      "pace": "measured",
      "accent": "standard Mandarin",
      "testClips": {
        "normal": "NOT_TESTED",
        "excited": "NOT_TESTED",
        "whisper": "NOT_TESTED"
      }
    }
  }
}
```

核心字段：

| 字段 | 必填 | 含义 |
|---|---:|---|
| `speakerId` | 是 | 全片稳定 `(S1)/(S2)...`，不按镜头重新编号 |
| `voiceAlias` | 是 | `assets` 中真实声音参考别名 |
| `language` | 是 | 目标说话语言 |
| `ageImpression` | 建议 | 年龄感，不是硬音色锁 |
| `timbre` | 建议 | 音域/明暗/粗糙度等 |
| `pace` | 建议 | 基准语速与咬字 |
| `accent` | 可选 | 口音/方言 |
| `testClips` | 建议 | normal/excited/whisper 三类试听状态 |
| `sharedVoiceReason` | 条件 | 多角色有意共用同一声音参考时必须解释 |

## 3. Speaker ID 规则

H3 的 `(Sx)` 是**目标视频全局发声源编号**：

- 按目标视频中首次实际发声顺序分配；
- 同一角色后续可见对白、画外音、内心独白复用同一 ID；
- 不因换镜、换场、梦境、回忆重新编号；
- 独立旁白是独立发声源，拥有自己的 ID；
- `(Sx)` 本身不锁音色，仍需声音参考或稳定声音描述。

最终 prompt 中 `(Sx)` 必须放在 `<d>` 外。

## 4. H3 Ref2VA 声音参考约束

当前公开 H3 Ref2VA 约束：

- 独立 audio reference ≤ 3；
- 每段独立音频 2–15 秒；
- 独立音频总时长 ≤ 15 秒；
- 混合参考文件总数 ≤ 12；
- **音频参考不能单独作为唯一参考输入**，必须同时存在 image 或 video；
- 参考顺序具有语义，`<Audio 1>`, `<Audio 2>`… 应与实际请求顺序一致。

因此不要把“3 个音频上限”误写成 Theodore 永久固定的 `ref_audio_0/1/2` 内部字段。导播层应维护稳定角色→声音别名映射，再以实际解析后的引用顺序生成 `<Audio N>`。

## 5. 声音样本

每角色使用本人录音、获准使用的声音，或用户明确确认的合成角色声音。优先：

- 单一说话人；
- 无背景音乐；
- 无其他人声；
- 低环境噪声/混响；
- 2–15 秒；
- 内容与目标语言/口音相符。

不要从多人混音视频随便截一段就标记“干净声音库”。

`assets` 导入后必须**实际引用**。例如：

```text
{{ref:CHEN_VOICE}} is the voice-timbre reference for <Subject 1> (S1).
```

若引用视频同步音轨，使用目标 Theodore 安装实际支持的 `.audio`/`includeVideoAudio` 机制，并以运行解析结果为准。

## 6. 只绑定当前实际说话人

每镜只输入当前真实发声者需要的声音参考：

- 不把全剧声音库全部设为 `fixed`；
- 不因为角色“可能出现”就注入其声音；
- 不因画面切到听者而转移声音所有权；
- 多人连续对白优先切成多个生成段；确需同镜时逐句分时并明确说话者。

声音引用与角色图像引用可以不同步：画外音角色可以不可见，但声音参考仍需激活。

## 7. H3 编译方式

声音身份参考：

```text
<Audio 1> is the voice-timbre reference for <Subject 1> (S1).
```

当前对白：

```text
CHEN BUFAN (S1) speaks quietly with the same low, clear Mandarin vocal identity:
<d>[Chinese]别怕，我在。</d>
```

情绪写在 `<d>` 外：

```text
CHEN BUFAN (S1) shouts urgently: <d>[Chinese]快跑！</d>
CHEN BUFAN (S1) whispers, barely audible: <d>[Chinese]别回头。</d>
```

不要把 `ACTIVE_SPEAKER`、`voiceAlias`、`testClips` 等导演变量输出成画面文字或可朗读台词。

## 8. 三段试听门禁

扩量前至少试听同一角色：

| 片段 | 目标 |
|---|---|
| `normal` | 基础音色、语言、语速 |
| `excited` | 高能量下是否漂移 |
| `whisper` | 低音量下是否仍像同一角色 |

再让两名相近年龄/性别角色交替发言，检查可辨识度。

没有实际音频时，只能交付**文字声线草案**；不能声称“已绑定”“已克隆”“已试听”。

## 9. 自动校验

```powershell
python scripts/validate_voice.py project.director.json `
  --review project.review.json `
  --input-root D:/ComfyUI/input `
  --theodore-root D:/ComfyUI/custom_nodes/ComfyUI_Theodore_Director `
  --output voice-preflight.json
```

脚本可以检查：

- `speakerId` 格式/重复；
- `voiceAlias` 是否存在、类型是否正确；
- 当前发声者声音参考是否真实激活；
- 未登记说话人；
- 不同人物无解释地共用同一声音；
- prompt 是否缺少对应 `(Sx)`。

脚本**不能**辨认实际音色、样本是否混入他人、真实年龄、情绪稳定性或口型。报告保持 `audioListening=NOT_TESTED`，直到人工试听完成。

## 10. 反模式

| 反模式 | 正确做法 |
|---|---|
| 用 seed 保证音色一致 | 实际声音参考 + 审听 |
| 每镜重新分配 S1/S2 | 全片按首次发声顺序固定 |
| 全剧声音都 fixed | 当前镜只路由实际发声者 |
| 音频单独做 Ref2VA 唯一输入 | 同时提供图或视频 |
| 把导入当激活 | 检查实际 resolve result |
| `<d>` 内写年龄/情绪/Speaker | 只放 `[Language]台词原文` |
| 无音频却称已锁音色 | 标注未验证 |

官方提示词参考：
`https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/docs/VIDEO_PROMPT_WRITING_GUIDE_ref_en.md`
