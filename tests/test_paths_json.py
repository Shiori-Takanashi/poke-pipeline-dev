import unittest
from pathlib import Path
from scripts.paths_json import get_dirpath_sub_jsons, get_dirpath_sub_json_by_name
from config.dirpath import JSON_DIR_PATH


class TestPathsJson(unittest.TestCase):

    def test_get_dirpath_sub_jsons_valid_path(self):
        """有効なパスでのサブディレクトリ取得テスト"""
        # 実際のJSONディレクトリが存在する場合のテスト
        if JSON_DIR_PATH.exists():
            result = get_dirpath_sub_jsons()
            self.assertIsInstance(result, list)
            # 結果がすべてディレクトリパスであることを確認
            for path in result:
                self.assertIsInstance(path, Path)

    def test_get_dirpath_sub_jsons_nonexistent_path(self):
        """存在しないパスでのエラーテスト"""
        nonexistent_path = Path("/nonexistent/path")
        with self.assertRaises(FileNotFoundError):
            get_dirpath_sub_jsons(nonexistent_path)

    def test_get_dirpath_sub_json_by_name_found(self):
        """名前指定でのディレクトリ取得テスト（見つかる場合）"""
        if JSON_DIR_PATH.exists():
            sub_dirs = get_dirpath_sub_jsons()
            if sub_dirs:
                # 最初のディレクトリを使ってテスト
                test_dirname = sub_dirs[0].name
                result = get_dirpath_sub_json_by_name(sub_dirs, test_dirname)
                self.assertEqual(result.name, test_dirname)

    def test_get_dirpath_sub_json_by_name_not_found(self):
        """名前指定でのディレクトリ取得テスト（見つからない場合）"""
        if JSON_DIR_PATH.exists():
            sub_dirs = get_dirpath_sub_jsons()
            with self.assertRaises(ValueError):
                get_dirpath_sub_json_by_name(sub_dirs, "nonexistent_directory")

    def test_get_dirpath_sub_json_by_name_empty_list(self):
        """空のリストでの名前指定テスト"""
        with self.assertRaises(ValueError):
            get_dirpath_sub_json_by_name([], "any_name")


if __name__ == "__main__":
    unittest.main()
