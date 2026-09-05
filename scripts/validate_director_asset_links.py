#!/usr/bin/env python3
"""Validate bidirectional asset/shot links in schemaVersion 4/5 director.json files."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def validate(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    assets = data.get("assets") or []
    shots = data.get("shots") or []

    asset_by_id: dict[str, dict[str, Any]] = {}
    for asset in assets:
        aid = asset.get("id")
        if not aid:
            errors.append("asset without id")
            continue
        if aid in asset_by_id:
            errors.append(f"duplicate asset id: {aid}")
        asset_by_id[aid] = asset

    shot_by_id: dict[str, dict[str, Any]] = {}
    for shot in shots:
        sid = shot.get("id")
        if not sid:
            errors.append("shot without id")
            continue
        if sid in shot_by_id:
            errors.append(f"duplicate shot id: {sid}")
        shot_by_id[sid] = shot

    asset_ids = set(asset_by_id)
    shot_ids = set(shot_by_id)

    for shot in shots:
        sid = shot.get("id")
        if not sid:
            continue
        disabled = set(shot.get("disabledAssetIds") or [])
        unknown = disabled - asset_ids
        for aid in sorted(unknown):
            errors.append(f"{sid}: disabledAssetIds references unknown asset {aid}")

    for asset in assets:
        aid = asset.get("id")
        if not aid:
            continue
        claimed = set(asset.get("shotIds") or [])
        unknown_shots = claimed - shot_ids
        for sid in sorted(unknown_shots):
            errors.append(f"{aid}: shotIds references unknown shot {sid}")

        for shot in shots:
            sid = shot.get("id")
            if not sid:
                continue
            disabled = aid in set(shot.get("disabledAssetIds") or [])
            claims = sid in claimed
            active = not disabled
            if claims != active:
                alias = asset.get("alias") or aid
                if disabled and claims:
                    errors.append(
                        f"{sid}: {alias} is disabled but asset.shotIds still claims this shot"
                    )
                elif active and not claims:
                    errors.append(
                        f"{sid}: {alias} is active but asset.shotIds does not claim this shot"
                    )

    return errors


def repair(data: dict[str, Any]) -> dict[str, Any]:
    assets = data.get("assets") or []
    shots = data.get("shots") or []
    asset_ids = {a.get("id") for a in assets if a.get("id")}

    for shot in shots:
        disabled = shot.get("disabledAssetIds") or []
        shot["disabledAssetIds"] = [aid for aid in disabled if aid in asset_ids]

    for asset in assets:
        aid = asset.get("id")
        if not aid:
            continue
        asset["shotIds"] = [
            shot["id"]
            for shot in shots
            if shot.get("id") and aid not in set(shot.get("disabledAssetIds") or [])
        ]
    return data


def self_test() -> int:
    broken = {
        "schemaVersion": 5,
        "assets": [
            {"id": "asset_a", "alias": "A", "shotIds": ["shot_001"]},
            {"id": "asset_b", "alias": "B", "shotIds": []},
        ],
        "shots": [
            {"id": "shot_001", "disabledAssetIds": ["asset_a"]},
        ],
    }
    before = validate(broken)
    if len(before) != 2:
        print("SELF-TEST RED failed: expected 2 bidirectional conflicts", file=sys.stderr)
        for err in before:
            print(err, file=sys.stderr)
        return 1

    repaired = repair(json.loads(json.dumps(broken)))
    after = validate(repaired)
    if after:
        print("SELF-TEST GREEN failed: repair left conflicts", file=sys.stderr)
        for err in after:
            print(err, file=sys.stderr)
        return 1

    print("SELF-TEST PASS: broken links detected and repaired")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("director_json", nargs="?", type=Path)
    parser.add_argument("--repair", action="store_true")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        return self_test()

    if not args.director_json:
        parser.error("director_json is required unless --self-test is used")

    data = json.loads(args.director_json.read_text(encoding="utf-8"))
    if args.repair:
        data = repair(data)
        target = args.output or args.director_json
        target.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    errors = validate(data)
    if errors:
        for err in errors:
            print(f"ERROR: {err}", file=sys.stderr)
        return 1

    print("PASS: director asset links are bidirectionally consistent")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
