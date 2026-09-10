# 兼容性与上游基线

本文件只记录**可以被来源或真实运行时证明**的兼容事实。不要用工作流文件名、节点显示名或某次成功运行推断整个组件版本兼容。

## 1. MiniMax H3 公开基线

本技能于 **2026-09-11** 对照 MiniMax H3 官方公开仓库/提示词指南检查以下能力：

- H3-Base-FL2VA：文本、首帧、尾帧、首尾帧条件；
- H3-Base-Ref2VA：图像、视频、音频多模态参考；
- Ref2VA 最大输入：
  - image ≤ 9；
  - video ≤ 3；
  - audio ≤ 3；
  - 混合文件总数 ≤ 12；
- 每个参考视频 2–15 秒，视频总时长 ≤ 15 秒；
- 每个独立参考音频 2–15 秒，音频总时长 ≤ 15 秒；
- 独立音频参考不能作为唯一参考输入，必须伴随至少一张图或一段视频；
- 参考顺序具有语义，`<Picture N>` / `<Video N>` / `<Audio N>` 的编号必须与实际请求中的参考顺序一致；
- Full-reference rewrite 使用：
  `subject_definitions → summary → retention_analysis → detailed_description → overall_soundscape → non_diegetic_music`；
- Speaker 使用稳定 `(S1)`, `(S2)`…；对白原文放 `<d>[Language]...</d>`。

官方入口：

- `https://huggingface.co/MiniMaxAI/MiniMax-H3`
- `https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/docs/VIDEO_PROMPT_WRITING_GUIDE_base_en.md`
- `https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/docs/VIDEO_PROMPT_WRITING_GUIDE_ref_en.md`

## 2. Theodore 兼容策略

本包的 `schemas/director.schema.json` 只约束基础容器并接受 `schemaVersion` 4/5。它**不是 Theodore 完整协议的权威来源**。

当提供 `--theodore-root` 时：

1. `scripts/validate_plan.py` 导入已安装的 `theodore_director.schema.load_plan`；
2. 调用实际 `resolve_references`；
3. 以该安装版本的真实解析结果作为运行时引用事实。

因此：

- 不写死 “Theodore >= 某 commit”；
- 不根据 `V7/V8/V9` 工作流名推断 schema；
- 不把压缩包内代码当可信运行时解析器；
- 发现目标安装与本包示例不同时，以目标安装为准并报告差异。

## 3. ComfyUI / 自定义节点

只有在能够读取实际环境时，才报告：

- ComfyUI 版本；
- H3 模型/节点版本；
- Turbo/LoRA/二次采样实现；
- 节点是否真正消费 `negativePrompt`；
- 参考适配器是否实际输出图片/视频/音频引用。

无法访问环境时写：

`runtime compatibility: NOT_CHECKED`

不要把 “节点存在” 写成 “功能已验证”。

## 4. 兼容性报告模板

```json
{
  "compatibility": {
    "h3_prompt_contract": "checked_against_official_2026-09-11",
    "theodore_runtime": "checked | not_checked",
    "schema_detected": "4 | 5 | unknown",
    "comfyui_runtime": "checked | not_checked",
    "reference_resolution": "native | static",
    "unverified": []
  }
}
```
