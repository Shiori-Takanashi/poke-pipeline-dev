#!/usr/bin/env python3
import sys
from pathlib import Path

# ─── 設定 ──────────────────────────────────

# 出力先（相対パス）
OUTPUT_PATH = Path("out/tree.txt")

# 対象ディレクトリ（省略時はカレント）
TARGET_DIR = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")

# CASE 1: 完全に無視したいディレクトリ名
IGNORE_DIRS_CASE1 = {"__pycache__"}

# CASE 2: 完全に無視したいファイル名
IGNORE_FILES_CASE2 = {"__init__.py"}

# CASE 3: 親ディレクトリ "json" の直下ファイルは無視、孫以降のディレクトリも無視
PARENT_DIRS_CASE3 = {"json"}

# CASE 4: 親ディレクトリ（".venv", ".git", ".trash"）は表示するが
#         その直下のファイル／ディレクトリをすべて無視
PARENT_DIRS_CASE4 = {".venv", ".git", ".trash", ".pytest_cache", ".vscode"}


# ─── 判定関数 ──────────────────────────────


def should_skip_dir(parent: Path, name: str) -> bool:
    """
    ディレクトリをスキップすべきか判定。
    """
    # CASE1: ディレクトリ名そのものを無視
    if name in IGNORE_DIRS_CASE1:
        return True

    parts = parent.parts

    # CASE3: "json" の孫以降のディレクトリを無視
    # 例: parent = Path(".../json/pokemon") の場合 parts に "json" が含まれ、
    #     depth_from_parent = len(parts) - index_of("json") = 2 → 孫 → 無視
    for idx, p in enumerate(parts):
        if p in PARENT_DIRS_CASE3:
            if len(parts) - idx >= 2:
                return True

    # CASE4: 直前の親が PARENT_DIRS_CASE4 に該当 → 子ディレクトリを無視
    if parent.name in PARENT_DIRS_CASE4:
        return True

    return False


def should_skip_file(parent: Path, name: str) -> bool:
    """
    ファイルをスキップすべきか判定。
    """
    # CASE2: 名前そのものを無視
    if name in IGNORE_FILES_CASE2:
        return True

    parts = parent.parts

    # CASE3: "json" 配下のすべてのファイルを無視
    if any(p in PARENT_DIRS_CASE3 for p in parts):
        return True

    # CASE4: 直前の親が PARENT_DIRS_CASE4 に該当 → 子ファイルを無視
    if parent.name in PARENT_DIRS_CASE4:
        return True

    return False


# ─── ツリー出力ロジック ──────────────────────


def build_tree(path: Path, prefix: str = "") -> list[str]:
    """
    path 以下を再帰的に調べ、フィルタリング後の行リストを返す。
    """
    lines: list[str] = []
    try:
        entries = sorted(path.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower()))
    except PermissionError:
        return lines

    for idx, entry in enumerate(entries):
        is_last = idx == len(entries) - 1
        connector = "└── " if is_last else "├── "
        name = entry.name

        if entry.is_dir():
            if should_skip_dir(path, name):
                continue
            lines.append(f"{prefix}{connector}{name}/")
            new_prefix = prefix + ("    " if is_last else "│   ")
            lines += build_tree(entry, new_prefix)

        elif entry.is_file():
            if should_skip_file(path, name):
                continue
            lines.append(f"{prefix}{connector}{name}")

    return lines


def main():
    # 出力先ディレクトリ確保
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    # ヘッダ
    output_lines = [f"{TARGET_DIR}/"]

    # ツリー構築
    output_lines += build_tree(TARGET_DIR)

    # ファイル書き出し
    OUTPUT_PATH.write_text("\n".join(output_lines), encoding="utf-8")
    print(f"Tree output saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
