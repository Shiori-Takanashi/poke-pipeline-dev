from pathlib import Path
from typing import List, Optional

from config.dirpath import JSON_DIR_PATH
from config.target import FETCH_TARGET


class JsonPathGetter:
    def __init__(self):
        self.name: Optional[str] = None
        self.sub_json_dirpaths: Optional[List[Path]] = None
        self.sub_json_dirpath: Optional[Path] = None

    def _get_sub_json_dirpaths(self, json_dir_path: Path = JSON_DIR_PATH) -> List[Path]:
        """
        JSON_DIR_PATH（json/ディレクトリ）以下のディレクトリを列挙し、
        ディレクトリパスをリストにして返す
        """
        if not json_dir_path.exists():
            raise FileNotFoundError(f"{json_dir_path} does not exist.")

        self.sub_json_dirpaths = [p for p in json_dir_path.iterdir() if p.is_dir()]
        return self.sub_json_dirpaths

    def _get_sub_json_dirpath_by_name(self, name: str) -> Optional[Path]:
        if name not in FETCH_TARGET:
            return None

        self.name = name

        self.sub_json_dirpath = next(
            (p for p in self.sub_json_dirpaths if p.name == self.name), None
        )
        return self.sub_json_dirpath
