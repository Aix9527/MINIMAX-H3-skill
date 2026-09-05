# Director Asset-Link Consistency / 导播资产双向关系一致性

## 中文

该模块解决 `director.json` 中一种机械但高影响的错误：镜头层通过 `disabledAssetIds` 禁用了某素材，但该素材自身的 `assets[].shotIds` 仍声明属于该镜头；或者素材已在镜头中启用，但 `asset.shotIds` 没有声明该镜头。

典型运行时报错：

`未找到或已禁用素材: <asset alias>`

当素材文件实际存在且 fingerprint 正确时，应首先检查双向关系是否冲突，而不是重新生成素材。

## 1. 唯一真值

对支持 `disabledAssetIds` 的 schemaVersion 4/5 director 项目，镜头级 allowlist 是当前生成的唯一真值。

对任意资产 `A` 和镜头 `S`，必须恒成立：

```text
A.id NOT IN S.disabledAssetIds
    ⇔
S.id IN A.shotIds
```

也就是：

- 资产在镜头中启用 → `asset.shotIds` 必须包含该镜头；
- 资产在镜头中禁用 → `asset.shotIds` 不得包含该镜头。

禁止出现“shot 禁用、asset 仍声明归属”或“shot 启用、asset 未声明归属”的分裂状态。

## 2. REFERENCE_ALLOWLIST 编译顺序

生成/修改 director.json 时使用下面顺序：

1. 为每个镜头计算 `REFERENCE_ALLOWLIST`；
2. 用完整项目资产集合减去 allowlist，生成 `shot.disabledAssetIds`；
3. **最后反向重建所有 `assets[].shotIds`**，不要保留旧版本中遗留的 shotIds；
4. 运行双向关系校验器；
5. 校验通过后才能交付。

推荐算法：

```text
for each asset:
    asset.shotIds = [
        shot.id for shot in shots
        if asset.id not in shot.disabledAssetIds
    ]
```

## 3. 不要把旧 shotIds 当成历史记录

当 V2.3 Active Context Isolation 缩小素材白名单时，旧项目里一个资产可能曾经属于 19 个镜头。新的白名单如果只允许它出现在 3 个镜头，就必须把 `asset.shotIds` 同步缩成这 3 个镜头。

`shotIds` 在这个工作流里是当前关联关系，不是审计历史。

## 4. 文件存在性与关系冲突分开检查

报“未找到或已禁用素材”时分两步：

### A. 文件/指纹

- alias 是否在导入素材包中存在；
- `fingerprint` 是否与实际文件 SHA256 一致；
- path/sourcePath 是否能被当前导入器解析。

### B. 关联关系

- 资产是否被当前镜头禁用；
- `asset.shotIds` 是否仍错误包含当前镜头；
- 当前镜头启用资产是否都反向声明当前镜头。

如果文件与 fingerprint 均匹配，只修关系，不重新生成图片。

## 5. 自动校验

仓库提供：

```bash
python scripts/validate_director_asset_links.py project.director.json
```

自动修复：

```bash
python scripts/validate_director_asset_links.py project.director.json --repair --output fixed.director.json
```

验证器会检查：

- 重复/缺失 asset id；
- 重复/缺失 shot id；
- `disabledAssetIds` 是否引用不存在资产；
- `asset.shotIds` 是否引用不存在镜头；
- 每个 asset/shot 的双向启用关系是否完全一致。

交付 schemaVersion 4/5 director.json 前必须通过该校验。

---

## English

This module prevents a mechanical but high-impact director.json inconsistency: a shot disables an asset through `disabledAssetIds` while the asset's own `shotIds` still claims that shot, or the reverse.

For every asset `A` and shot `S`, enforce:

```text
A.id NOT IN S.disabledAssetIds
    ⇔
S.id IN A.shotIds
```

Treat the shot-level reference allowlist as the source of truth. After computing every shot's `disabledAssetIds`, rebuild all `assets[].shotIds` from those allowlists instead of preserving stale relationships from an older project version.

When the runtime reports a missing-or-disabled asset, first separate file/fingerprint validation from relationship validation. If the alias exists and its fingerprint matches the supplied file, repair the bidirectional link rather than regenerating the image.

Before delivery, run:

```bash
python scripts/validate_director_asset_links.py project.director.json
```

or use `--repair` to rebuild `assets[].shotIds` from the current shot-level disable lists.