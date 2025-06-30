# tests/test_json_path.py

from pathlib import Path

from util.paths_json import get_dirpath_sub_jsons, get_dirpath_sub_json
from config.dirpath import JSON_DIR_PATH


def test_get_dirpath_sub_jsons_returns_directories():
    """json/ 以下のサブディレクトリが Path のリストで返るか"""
    result = get_dirpath_sub_jsons()
    assert isinstance(result, list)
    assert all(isinstance(p, Path) for p in result)
    assert all(p.is_dir() for p in result)


def test_get_dirpath_sub_json_finds_expected_dir():
    """指定されたディレクトリ名が存在する場合、それを返す"""
    dirs = get_dirpath_sub_jsons()
    if not dirs:
        return  # サブディレクトリが存在しないならテストスキップ

    dirname = dirs[0].name  # 最初のディレクトリ名を使用
    target = get_dirpath_sub_json(dirs, dirname)
    assert target.name == dirname
    assert target in dirs


def test_get_dirpath_sub_json_raises_on_invalid_name():
    """存在しないディレクトリ名が与えられたら ValueError を返す"""
    dirs = get_dirpath_sub_jsons()
    invalid = "__no_such_dir__"
    while any(p.name == invalid for p in dirs):
        invalid += "_x"
    try:
        get_dirpath_sub_json(dirs, invalid)
    except ValueError as e:
        assert invalid in str(e)
    else:
        assert False, "ValueError が発生しなかった"
