from pathlib import Path
import json
from typing import Any


def read_json(path: Path) -> Any:
    """JSONファイルを読み込んで返す"""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_txt(data: str, path: Path):
    """文字列をテキストファイルとして出力"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(data)


def flatten(d: dict, parent_key: str = "", sep: str = ".") -> dict:
    """ネストされた辞書をフラット化する"""
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def dict_sample_lines(d: dict, max_items: int = 20) -> list[str]:
    """辞書のキーと値の例を整形してリストで返す"""
    lines = []
    for i, (k, v) in enumerate(d.items()):
        if i >= max_items:
            lines.append(f"... ({len(d) - max_items} more keys)\n")
            break
        lines.append(f"{k!r}: {v!r}\n")
    return lines


def transform_template_dict(item: dict) -> dict | None:
    """'name' と 'url' のみを持つ辞書を、識別用の文字列に変換する

    例:
        入力:
            {"name": "tackle", "url": "https://pokeapi.co/api/v2/move/33/"}
        出力:
            {"ident": "tackle（move/33）"}
    """
    if set(item.keys()) == {"name", "url"}:
        name = item["name"]
        url = item["url"]
        parts = url.rstrip("/").split("/")
        if len(parts) >= 2:
            resource = parts[-2]
            ident = parts[-1]
            return {"ident": f"{name}（{resource}/{ident}）"}
    return None
