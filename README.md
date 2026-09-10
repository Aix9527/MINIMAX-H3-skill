# MiniMax H3 Director OS v4.0.0

面向 MiniMax H3 的导演提示词与 `director.json` 编译、诊断技能。将故事、对白和参考素材转换为当前镜头可执行的输入，检查素材引用、台词归属、声音身份及场景连续性。

## v4.0.0 更新

- 主技能增加快速参考、来源优先级、P0/P1/P2 按需读取与交付契约。
- 增加 Ref2VA 参考数量、媒体时长和音频单独引用的静态预检。
- 分离台词所有者与实际声音来源，支持 `voiceSourceCharacterId` 和 `dream_speech`。
- 增加声音档案、对白账本、review schema 和可运行的校验脚本。
- 兼容性以实际安装的解析器与运行输入为准，不承诺未经验证的最低版本。

详细变化见 [CHANGELOG.md](./CHANGELOG.md)，使用说明见 [升级与使用说明.md](./升级与使用说明.md)。

## 安装与使用

将仓库克隆到 Skill 目录下的 `minimax-h3-director-os` 文件夹，或从 [v4.0.0 Release](https://github.com/Aix9527/MINIMAX-H3-skill/releases/tag/v4.0.0) 下载安装包并解压其中的同名目录。

```powershell
git clone https://github.com/Aix9527/MINIMAX-H3-skill.git "$env:USERPROFILE/.codex/skills/minimax-h3-director-os"
```

如果已安装，请先备份本地修改，再更新。重新开启任务/会话加载技能；入口是仓库根目录的 [SKILL.md](./SKILL.md)。

示例请求：

> 把这段剧本编译成 H3 director.json。逐镜检查当前场景、人物状态、实际参考素材、台词所有者和声音来源，并附静态预检结果。

## 校验

在仓库根目录运行（需要 Python 3）：

```powershell
python -m unittest discover -s tests -v
python scripts/validate_plan.py examples/single-dialogue.director.json
python scripts/validate_voice.py examples/voice-consistency.director.json --review examples/voice-consistency.review.json
python scripts/validate_dialogue.py examples/dialogue-ownership.director.json --review examples/dialogue-ownership.review.json
```

检查真实项目时可传入 `--input-root` 和 `--theodore-root`，详见使用说明。不提供实际运行环境时只能称为静态检查；脚本通过不代表视频画质、音色或口型通过。

## 文件结构

| 路径 | 内容 |
|---|---|
| `SKILL.md` | v4.0.0 技能入口 |
| `references/` | 提示词、对白、声音、连续性与运行时参考 |
| `schemas/` | director 和 review JSON schema |
| `scripts/` | 计划、声音及台词预检 |
| `tests/` | 37 项单元测试 |
| `examples/` | 提示词、计划和 review 示例 |
| `core/`、`compiler/`、`intelligence/`、`validator/`、`cases/`、`docs/` | 保留的旧版框架与历史资料，以当前技能入口和参考文档为准 |

## 验证范围

本次更新执行单元测试、Python 编译、JSON 解析和本地链接检查。未执行 GPU 视频生成、声音试听、口型人工检查或本地运行时解析。

## 版本发布

当前版本：**v4.0.0**。GitHub Actions 检查通过后同步版本标签与 Release。历史版本和更新记录保留在 [Releases](https://github.com/Aix9527/MINIMAX-H3-skill/releases) 与更新日志中。
