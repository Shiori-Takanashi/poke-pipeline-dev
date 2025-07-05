from __future__ import annotations
from pathlib import Path
from typing import List, Optional
import json

from config.dirpath import JSON_DIR_PATH
from config.target import FETCH_TARGET
from config.json_type import JSON_TYPE


class JsonPathBuilder:
    def __init__(self, endpoint_name, json_type):
        self.ident: Optional[str] = None
        self.endpoint_name: Optional[str] = None
        self.json_type: Optional[str] = None
        self.idx: Optional[str | int] = None
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

    def _get_sub_json_dirpath_by_name(
        self, endpoint_name: str, json_type: str
    ) -> Optional[Path]:

        if endpoint_name not in FETCH_TARGET:
            return None

        if json_type not in JSON_TYPE:
            return None

        self.endpoint_name = endpoint_name
        self.json_type = json_type

        self.ident = self._build_ident(self.endpoint_name, self.json_type)

        self.sub_json_dirpath = next(
            (p for p in self.sub_json_dirpaths if p.name == self.ident), None
        )
        return self.sub_json_dirpath

    def _build_ident(self, endpoint_name: str, json_type: str) -> str:
        ident = f"{json_type}_{endpoint_name}"
        self.ident = ident
        return ident

    def get_jsonpath(self, endpoint_name: str, json_type: str, idx: str | int) -> Path:
        self.endpoint_name = endpoint_name
        self.json_type = json_type
        self.idx = idx
        self._get_sub_json_dirpaths()
        jsonpath_pre = self._get_sub_json_dirpath_by_name(
            self.endpoint_name, self.json_type
        )
        jsonpath = jsonpath_pre / f"{idx:05}.json"
        if jsonpath.exists():
            return jsonpath
