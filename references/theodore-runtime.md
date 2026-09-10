# Theodore 运行适配

这是自定义导播协议，不是MiniMax API。读取目标安装的theodore_director/schema.py；本地可接受v4并迁移到v5，但其他安装不一定相同。不要仅根据工作流文件名V9推断schema版本。保留已有ID与工作流支持的secondSamplingMode语义。

## 引用链

assets中的alias须唯一。镜头prompt使用{{ref:CHEN_FACE}}引用对应素材；shotIds、enabled、disabledAssetIds决定该镜可用性，fixed决定无需显式标签时是否自动注入。不要把所有角色设成全局fixed。没有图的纯文本任务合法；不能把所有0引用都判为错误。

先在导演侧选择期望素材，再运行实际resolve_references，比较requiredAliases与activeAliases。只有期望角色参考缺失才属于阻断；无期望声明时只能提示检查。

```powershell
python scripts/validate_plan.py project.director.json --input-root D:/ComfyUI/input --theodore-root D:/ComfyUI/custom_nodes/ComfyUI_Theodore_Director --review project.review.json --output preflight.json
```

theodore-root指向可信的已安装插件，脚本会导入并执行其中的Python解析器；不能指向不可信压缩包代码。脚本只读取计划/素材是否存在，不加载模型、不发网络请求、不排队、不修改工作流。

review旁车示例：
```json
{"shots":{"shot_001":{"sceneId":"STREAM","requiredAliases":["CHEN_FACE"],"speechSeconds":4}}}
```

sceneId和requiredAliases由导演提供，脚本不会从小说猜测。人物漂移、台词转移、道具换人属于人工/视频审看项。对白字符率是启发式，不能证明声音可听清。

## 真实输入检查

查看实际prompt连线而非节点上被覆盖的widget显示值。明确正面/负面字段是否消费；独立negativePrompt未连接时不能声称负面词已生效。查看参考适配器输出，而非仅数assets。检查是否有额外增强节点把已结构化提示词重新包装。

标注基础生成尺寸、实际交付尺寸、采样组合、加速与画风LoRA的区别。4K标签不等于原生4K，静态规则通过不等于GPU运行通过。不要盲目将Turbo匹配的8步改成几十步。

scripts/validate_plan.py是运行预检，不是完整JSON Schema验证器；schemas/director.schema.json只约束基本容器，真实协议以目标加载器为准。
