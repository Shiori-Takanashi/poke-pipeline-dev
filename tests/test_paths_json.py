# tests/test_paths_json.py

import sys
from pathlib import Path
import pytest

# プロジェクトルートを sys.path に追加（import 解決用）
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config.dirpath import JSON_DIR_PATH
from config.target import FETCH_TARGET, MONSTER_TARGET
from src.pathing.paths_json import (
    get_dirpath_sub_jsons,
    get_dirpath_sub_json_by_name,
)


def test_get_dirpath_sub_jsons_returns_list_of_dirs():
    """
    get_dirpath_sub_jsons() が json/ 以下のサブディレクトリ Path のリストを返すこと
    """
    subdirs = get_dirpath_sub_jsons()
    assert isinstance(subdirs, list)
    assert all(isinstance(p, Path) for p in subdirs)
    assert all(p.is_dir() for p in subdirs)


def test_get_dirpath_sub_jsons_not_found(tmp_path):
    """
    json_dir_path が存在しない場合に FileNotFoundError を投げること
    """
    nonexistent = tmp_path / "not_exist"
    with pytest.raises(FileNotFoundError):
        get_dirpath_sub_jsons(json_dir_path=nonexistent)


def test_get_dirpath_sub_json_by_name_found():
    """
    get_dirpath_sub_json_by_name() が有効な name に対して正しい Path を返すこと
    """
    subdirs = get_dirpath_sub_jsons()
    if not subdirs:
        pytest.skip("json/ 以下のサブディレクトリが存在しないためスキップ")
    name = subdirs[0].name  # 存在する最初のディレクトリ名
    path = get_dirpath_sub_json_by_name(subdirs, name)
    assert path.name == name
    assert path.is_dir()


def test_get_dirpath_sub_json_by_name_not_found():
    """
    get_dirpath_sub_json_by_name() が無効な name に対して ValueError を投げること
    """
    subdirs = get_dirpath_sub_jsons()
    # 存在しないユニークな name を作成
    invalid = "__no_such_dir__"
    while any(p.name == invalid for p in subdirs):
        invalid += "_x"
    with pytest.raises(ValueError) as exc:
        get_dirpath_sub_json_by_name(subdirs, invalid)
    assert invalid in str(exc.value)


@pytest.mark.parametrize("name", FETCH_TARGET)
def test_fetch_target_directories_exist(name):
    """
    FETCH_TARGET に列挙されたすべての name がディレクトリとして存在すること
    """
    subdirs = get_dirpath_sub_jsons()
    path = get_dirpath_sub_json_by_name(subdirs, name)
    assert path.is_dir(), f"{name} のディレクトリが見つかりません"


@pytest.mark.parametrize("name", MONSTER_TARGET)
def test_monster_target_directories_exist(name):
    """
    MONSTER_TARGET に列挙されたすべての name がディレクトリとして存在すること
    """
    subdirs = get_dirpath_sub_jsons()
    path = get_dirpath_sub_json_by_name(subdirs, name)
    assert path.is_dir(), f"{name} のディレクトリが見つかりません"
