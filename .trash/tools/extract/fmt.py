from pathlib import Path
import json
from typing import Any

INPUT_PATH = Path("out/jp878.json")
OUTPUT_PATH = Path("out/jp878_re.json")


def transform_template_dict(d: dict) -> str | None:
    """典型的な {'name': ..., 'url': ...} 形式の辞書を文字列へ変換"""
    if set(d.keys()) == {"name", "url"}:
        name = d["name"]
        url = d["url"]
        suffix = "/".join(url.rstrip("/").split("/")[-2:])
        return f"{name}（{suffix}）"
    return None


def transform_element(elem: Any) -> Any:
    """リストや辞書の中身を再帰的に変換し、Noneや空リストは除外"""
    if elem is None:
        return None
    elif isinstance(elem, list):
        transformed = [transform_element(e) for e in elem]
        filtered = [e for e in transformed if e not in (None, [], {})]
        return filtered if filtered else None
    elif isinstance(elem, dict):
        result = transform_template_dict(elem)
        if result is not None:
            return result
        transformed = {k: transform_element(v) for k, v in elem.items()}
        # None, [], {} を除外
        filtered = {k: v for k, v in transformed.items() if v not in (None, [], {})}
        return filtered if filtered else None
    else:
        return elem


def main():
    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    transformed = {
        k: v
        for k, v in {
            key: transform_element(value) for key, value in data.items()
        }.items()
        if v not in (None, [], {})
    }

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(transformed, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
