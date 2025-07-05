import unittest
import tempfile
import json
from pathlib import Path
from scripts.json_mapping import JsonPathExporter


class TestJsonPathExporter(unittest.TestCase):

    def setUp(self):
        """テスト用の一時ディレクトリとファイルを作成"""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.test_json_dir = self.temp_dir / "test_json"
        self.test_json_dir.mkdir()

        # テスト用のJSONファイルを作成
        for i in range(1, 4):
            test_file = self.test_json_dir / f"{i:05d}.json"
            test_file.write_text('{"test": "data"}')

    def tearDown(self):
        """テスト後のクリーンアップ"""
        import shutil

        shutil.rmtree(self.temp_dir)

    def test_init_with_subdir(self):
        """サブディレクトリ指定でのインスタンス化テスト"""
        exporter = JsonPathExporter("test_subdir")
        self.assertIsInstance(exporter, JsonPathExporter)

    def test_init_without_subdir(self):
        """サブディレクトリ指定なしでのインスタンス化テスト"""
        exporter = JsonPathExporter()
        self.assertIsInstance(exporter, JsonPathExporter)

    def test_make_path_index(self):
        """パスインデックス作成テスト"""
        exporter = JsonPathExporter()
        result = exporter.make_path_index(self.test_json_dir)
        expected = {"00001": "00001.json", "00002": "00002.json", "00003": "00003.json"}
        self.assertEqual(result, expected)

    def test_write_index_to_file(self):
        """ファイル書き込みテスト"""
        with tempfile.TemporaryDirectory() as temp_dir:
            exporter = JsonPathExporter()
            exporter.output_dir = Path(temp_dir)

            test_data = {"test": "data"}
            exporter.write_index_to_file(test_data, "test-label")

            output_file = Path(temp_dir) / "test-label.py"
            self.assertTrue(output_file.exists())

    def test_process(self):
        """プロセス実行テスト"""
        with tempfile.TemporaryDirectory() as temp_dir:
            exporter = JsonPathExporter()
            exporter.output_dir = Path(temp_dir)

            exporter.process([self.test_json_dir])

            output_file = Path(temp_dir) / "test_json.py"
            self.assertTrue(output_file.exists())


if __name__ == "__main__":
    unittest.main()
