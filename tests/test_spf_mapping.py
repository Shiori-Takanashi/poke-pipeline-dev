import unittest
import tempfile
import json
from pathlib import Path
from unittest.mock import patch, MagicMock
from scripts.spf_mapping import MonsterMap, get_json_files_mapping


class TestGetJsonFilesMapping(unittest.TestCase):

    def setUp(self):
        """テスト用の一時ディレクトリとJSONファイルを作成"""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.test_subdir = self.temp_dir / "test_subdir"
        self.test_subdir.mkdir()

        # テスト用のJSONファイルを作成
        for i in range(1, 4):
            test_file = self.test_subdir / f"{i:05d}.json"
            test_file.write_text('{"test": "data"}')

    def tearDown(self):
        """テスト後のクリーンアップ"""
        import shutil

        shutil.rmtree(self.temp_dir)

    @patch("scripts.spf_mapping.JSON_DIR_PATH")
    def test_get_json_files_mapping_existing_dir(self, mock_json_dir):
        """存在するディレクトリでのマッピング取得テスト"""
        mock_json_dir.__truediv__ = lambda self, other: self.temp_dir / other
        mock_json_dir.__truediv__.return_value = self.test_subdir

        # パッチ適用後に関数を再インポート
        from scripts.spf_mapping import get_json_files_mapping

        with patch("pathlib.Path.exists", return_value=True):
            with patch("pathlib.Path.glob") as mock_glob:
                mock_files = [
                    MagicMock(stem="1", name="00001.json"),
                    MagicMock(stem="2", name="00002.json"),
                    MagicMock(stem="3", name="00003.json"),
                ]
                mock_glob.return_value = mock_files

                result = get_json_files_mapping("test_subdir")
                expected = {
                    "00001": "00001.json",
                    "00002": "00002.json",
                    "00003": "00003.json",
                }
                self.assertEqual(result, expected)

    def test_get_json_files_mapping_nonexistent_dir(self):
        """存在しないディレクトリでのマッピング取得テスト"""
        with patch("scripts.spf_mapping.JSON_DIR_PATH") as mock_json_dir:
            mock_json_dir.__truediv__.return_value.exists.return_value = False

            from scripts.spf_mapping import get_json_files_mapping

            result = get_json_files_mapping("nonexistent")
            self.assertEqual(result, {})


class TestMonsterMap(unittest.TestCase):

    def setUp(self):
        """テスト用のMonsterMapインスタンスを作成"""
        self.monster_map = MonsterMap()

    def test_init(self):
        """インスタンス化テスト"""
        self.assertIsInstance(self.monster_map.map, dict)

    def test_extract_idx_from_data_with_url(self):
        """URLからのID抽出テスト"""
        test_entries = [
            {"url": "https://example.com/api/pokemon/1/"},
            {"url": "https://example.com/api/pokemon/25/"},
        ]
        result = self.monster_map._extract_idx_from_data(test_entries)
        self.assertEqual(result, [1, 25])

    def test_extract_idx_from_data_with_pokemon_url(self):
        """pokemon URLからのID抽出テスト"""
        test_entries = [
            {"pokemon": {"url": "https://example.com/api/pokemon/1/"}},
            {"pokemon": {"url": "https://example.com/api/pokemon/25/"}},
        ]
        result = self.monster_map._extract_idx_from_data(test_entries)
        self.assertEqual(result, [1, 25])

    def test_extract_idx_from_data_with_form_url(self):
        """form URLからのID抽出テスト"""
        test_entries = [
            {"form": {"url": "https://example.com/api/pokemon-form/1/"}},
            {"form": {"url": "https://example.com/api/pokemon-form/25/"}},
        ]
        result = self.monster_map._extract_idx_from_data(test_entries)
        self.assertEqual(result, [1, 25])

    def test_extract_idx_from_data_invalid_entries(self):
        """無効なエントリでのID抽出テスト"""
        test_entries = [{"name": "test"}, {"invalid": "data"}]
        result = self.monster_map._extract_idx_from_data(test_entries)
        self.assertEqual(result, [])

    @patch("scripts.spf_mapping.read_json")
    @patch("scripts.spf_mapping.SPECIES")
    @patch("scripts.spf_mapping.SPECIE_DIR_PATH")
    def test_process_species(self, mock_specie_dir, mock_species, mock_read_json):
        """species処理テスト"""
        mock_species.get.return_value = "00001.json"
        mock_read_json.return_value = {
            "varieties": [{"url": "https://example.com/api/pokemon/1/"}]
        }

        result = self.monster_map.process_species(1)
        self.assertEqual(result, [1])

    @patch("scripts.spf_mapping.read_json")
    @patch("scripts.spf_mapping.POKEMON")
    @patch("scripts.spf_mapping.POKEMON_DIR_PATH")
    def test_process_pokemon(self, mock_pokemon_dir, mock_pokemon, mock_read_json):
        """pokemon処理テスト"""
        mock_pokemon.get.return_value = "00001.json"
        mock_read_json.return_value = {
            "forms": [{"url": "https://example.com/api/pokemon-form/1/"}]
        }

        result = self.monster_map.process_pokemon([1])
        self.assertEqual(result, [1])

    def test_make_spf_map(self):
        """SPFマップ作成テスト"""
        test_triples = [
            {"species": 1, "pokemon": 1, "form": 1},
            {"species": 1, "pokemon": 1, "form": 2},
        ]
        result = MonsterMap.make_spf_map(test_triples)
        expected = {
            "m00001": {"species": 1, "pokemon": 1, "form": 1},
            "m00002": {"species": 1, "pokemon": 1, "form": 2},
        }
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
