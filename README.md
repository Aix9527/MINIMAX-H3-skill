# MINIMAX-H3-skill

**MiniMax H3 Director OS V1.0** 是一套面向 MiniMax H3 的导演级视频提示词 Skill。它不是简单的“提示词润色器”，而是把创意、小说、剧本、分镜、参考图/视频/音频或上一段生成结果，编译成可执行、可连续、可质检的 H3 导演指令。

## 核心能力

- 导演决策：先确定叙事任务、blocking、表演和动作，再决定镜头。
- 表演与动作：把抽象情绪翻译为可见身体行为，并约束动作物理因果与终点。
- 摄影与灯光：景别、机位、焦段、主运镜、光源方向都必须服务叙事。
- 声音导演：对白、呼吸、环境声、动作声与非画内音乐进入同一时间系统。
- Reference Contract：明确 Subject / Picture / Video / Audio 各参考素材职责，减少互相覆盖。
- 长视频连续性：使用 Continuity State 继承身份、服装、道具、轴线、动作阶段、灯光、音频和真实尾帧状态。
- H3 原生编译：覆盖 T2VA、I2VA、FL2VA、L2VA、Full Reference、Video Edit、Video Continuation、Multi-Segment。
- QC 与失败修复：优先删冲突、减动作、锁身份/空间、明确终点，再考虑拆段或重建参考锚点。

## 使用

将仓库根目录的 [`SKILL.md`](./SKILL.md) 作为 Agent/Skill 指令加载。然后直接输入自然语言需求，例如：

```text
把这一段小说转换成 3 段连续的 MiniMax H3 视频提示词，每段 10 秒。
人物参考使用 Subject 1，上一段真实尾帧作为下一段起始状态，保留对白与环境声。
```

也可以用于单镜头、首帧图生视频、首尾帧、全参考、续写和失败 Prompt 修复。

## 设计原则

> Director Brain → Blocking → Performance → Physics → Camera → Lighting → Audio → Continuity → Reference Contract → H3 Compiler → QC Repair

重点不是堆叠“电影感、史诗、8K”等形容词，而是让每一句指令都能回答：**摄像机真的能拍到，或者麦克风真的能听到吗？**

## Version

- V1.0 — MiniMax H3 Director OS / Cinematic Sequence Director
