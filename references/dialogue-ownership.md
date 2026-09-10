# 台词归属、声音来源与主观画面

多角色、画外音、内心独白、回忆、想象、梦境中必须把以下概念分开：

1. **谁拥有这句台词/语义**；
2. **谁真正发出声音**；
3. **谁在画面里**；
4. **这段画面是谁的主观视角**；
5. **谁的嘴需要产生可见发音动作**。

它们经常相同，但不能假设永远相同。

## 1. 逐句台词账本

在 `review.json -> shots -> dialogueLines` 中逐句登记：

```json
{
  "lineId": "L001",
  "characterId": "CHEN",
  "voiceSourceCharacterId": "CHEN",
  "delivery": "inner",
  "language": "Chinese",
  "text": "这件事不对劲。"
}
```

字段：

| 字段 | 含义 |
|---|---|
| `lineId` | 全片唯一台词 ID |
| `characterId` | 台词/语义所有者 |
| `voiceSourceCharacterId` | 实际发声源；省略时默认等于 `characterId` |
| `delivery` | `onscreen/offscreen/inner/narration/dream_speech` |
| `language` | `<d>` 内语言标签 |
| `text` | 必须保留的原始台词 |

镜头级字段：

- `activeSpeakerIds`：当前实际发声源角色 ID；
- `visibleCharacterIds`：当前画面可见角色；
- `visualMode`：`reality/memory/imagination/dream`；
- `viewpointCharacterId`：主观视角角色；
- `speechSeconds`：实际可用于说话的时间窗口。

`review.json` 是导演事实账本，不是模型字段。

## 2. owner 与 voice source

默认：

`characterId == voiceSourceCharacterId`

只有剧情明确要求“模仿、转述录音、变声器、附身声源”等特殊情况才拆开。拆开后：

- `(Sx)`、声音参考、`activeSpeakerIds` 都跟随 `voiceSourceCharacterId`；
- 台词审校/版权/剧情归属仍跟随 `characterId`；
- 必须在镜头描述中自然说明为什么声源与语义所有者不同。

不要为了修串台而随意改 `voiceSourceCharacterId`。

## 3. 常见场景

| 场景 | characterId | voiceSource | 嘴部行为 |
|---|---|---|---|
| 陈不凡当面说话 | 陈不凡 | 陈不凡 | 陈不凡对口型 |
| 陈不凡内心独白 | 陈不凡 | 陈不凡 | 所有可见嘴保持静默 |
| 陈不凡画外音 | 陈不凡 | 陈不凡 | 可见人物不承接声音 |
| 陈不凡梦见沈清月真正说话 | 沈清月 | 沈清月 | 梦中沈清月开口 |
| 陈不凡梦中继续自己的思考 | 陈不凡 | 陈不凡 | 梦中人物不替他开口 |
| 陈不凡转述“她说……” | 陈不凡 | 陈不凡 | 除非切为原声回放 |
| 独立旁白 | narrator | narrator | 所有可见嘴静默 |
| 电话/门外声音 | 对端角色 | 对端角色 | 画内听者不对口型 |

**谁在看 ≠ 谁在画面 ≠ 谁在说。**

## 4. H3 编译语法

普通发言：

```text
CHEN BUFAN (S1) says: <d>[Chinese]别开门。</d>
```

画外音：

```text
CHEN BUFAN (S1) speaks offscreen: <d>[Chinese]你结不了婚。</d>
The visible listener remains silent with closed lips.
```

内心独白/旁白使用 H3 官方稳定 voiceover 语法：

```text
CHEN BUFAN (S1) says in an off-screen voiceover:
<d>[Chinese]这件事不对劲。</d>
His visible lips remain completely closed.
```

梦中他人真正说话：

```text
In the dream, SHEN QINGYUE (S2) speaks:
<d>[Chinese]陈先生，你听见了吗？</d>
CHEN BUFAN remains visible but silent.
```

`(Sx)` 和表演描述始终在 `<d>` 外；`<d>` 内只放 `[Language] + 原句`。

## 5. 稳定 Speaker ID

- 按目标视频首次实际发声顺序分配 `S1/S2/...`；
- 后续跨镜、跨场、回忆、梦境复用；
- 独立旁白单独编号；
- 画面切到另一个人不转移 Speaker ID；
- 不要中途把稳定角色锚点换成多个同义称呼。

Cast key 示例：

```text
(S1): CHEN BUFAN — lean young Chinese man, short layered black hair.
(S2): SHEN QINGYUE — young Chinese woman, long dark hair.
```

左右位置只是镜头状态，不属于声音身份。

## 6. 沉默也是归属约束

对多角色画面，明确非说话者：

```text
SHEN QINGYUE remains visible and silent; her lips stay closed.
Only CHEN BUFAN (S1) produces human dialogue audio.
```

不要把内部变量 `ACTIVE_SPEAKER` / `MUTE_LISTENER` 原样输出给模型；把它们转换成这种自然可观察描述。

## 7. 时间与密度

台词不能默认占满整段。优先结构：

`反应/吸气 → 台词 → 停顿 → 嘴部回中性 → 后续反应`

后续编辑镜头用 H3 `[Shot N] At MM:SS.mmm` 标记真实切点。台词太密时先：

1. 缩短非关键台词（需要用户授权）；
2. 增加真实说话时间；
3. 拆成多个生成段；
4. 最后才考虑更快语速。

不要用“说快一点”解决严重超密度。

## 8. 自动校验

```powershell
python scripts/validate_dialogue.py project.director.json `
  --review project.review.json `
  --input-root D:/ComfyUI/input `
  --theodore-root D:/ComfyUI/custom_nodes/ComfyUI_Theodore_Director `
  --output dialogue-preflight.json
```

脚本检查：

- 台词数量/顺序/原句/语言；
- `lineId` 唯一；
- `voiceSourceCharacterId` 对应 `(Sx)`；
- 实际发声源是否在 `activeSpeakerIds`；
- `onscreen/dream_speech` 发声者是否可见；
- `inner/narration` 是否使用明确 voiceover 语法；
- 声音参考是否实际激活。

脚本不判断：

- 账本是否忠于未提供的小说上下文；
- 成片是否真的串台；
- 谁的嘴实际在动；
- 音色是否与参考一致。

这些必须人工审听/审看。

## 9. 反模式

| 反模式 | 修复 |
|---|---|
| 可见角色自动获得当前台词 | 用账本固定 owner/source |
| 内心独白换成画面人物声线 | 继续使用独白者 voice source |
| 梦境归主角所以所有声音都主角说 | 梦里谁真实说话就用谁的声音 |
| 每个镜头重新编号 S1/S2 | 全片稳定 |
| `<d>` 内塞情绪/角色名 | 放标签外 |
| 长画外音压在另一个完整正脸嘴部 | 缩短、改插入镜头或拆段 |
| 配置 PASS 就宣布无串台 | 必须审听/审看 |

**配置检查通过 ≠ 模型不会串台。**
