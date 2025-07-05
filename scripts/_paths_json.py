from pathlib import Path
from typing import Dict, List
from config.dirpath import JSON_DIR_PATH


def get_dirpath_sub_jsons(json_dir_path: Path = JSON_DIR_PATH) -> List[Path]:
    """
    JSON_DIR_PATH（json/ディレクトリ）以下のディレクトリを列挙し、
    ディレクトリパスをリストにして返す
    """
    if not json_dir_path.exists():
        raise FileNotFoundError(f"{json_dir_path} does not exist.")

    dirpath_sub_jsons = [p for p in json_dir_path.iterdir() if p.is_dir()]

    return dirpath_sub_jsons


def get_dirpath_sub_json_by_name(
    dirpath_sub_jsons: List[Path], dirname_json: str
) -> Path:
    """
    dirpath_sub_jsons の中から、name が dirname_json に一致する Path を返す。
    """
    for dirpath_sub_json in dirpath_sub_jsons:
        if dirname_json == dirpath_sub_json.name:
            return dirpath_sub_json
    raise ValueError(f"Directory '{dirname_json}' not found.")


if __name__ == "__main__":
    print(f"JSON directory path: {JSON_DIR_PATH}")

    try:
        sub_dirs = get_dirpath_sub_jsons()
        print(f"Found {len(sub_dirs)} JSON subdirectories:")

        for i, sub_dir in enumerate(sub_dirs, 1):
            print(f"  {i:2d}. {sub_dir.name} ({sub_dir})")

        # 各サブディレクトリのJSONファイル数も表示
        print("\nJSON file counts:")
        for sub_dir in sub_dirs:
            json_files = list(sub_dir.glob("*.json"))
            print(f"  {sub_dir.name}: {len(json_files)} files")

        # 特定のディレクトリ名での検索例
        if sub_dirs:
            test_dirname = sub_dirs[0].name
            found_dir = get_dirpath_sub_json_by_name(sub_dirs, test_dirname)
            print(f"\nTest search for '{test_dirname}': {found_dir}")

    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
