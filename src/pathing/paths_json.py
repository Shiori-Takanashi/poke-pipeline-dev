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
