# Testing

このページでは、poke-pipelineプロジェクトにおけるテストの書き方と実行方法について説明します。

## テスト戦略

### テストの種類

1. **単体テスト (Unit Tests)**: 個別の関数やクラスのテスト
2. **統合テスト (Integration Tests)**: モジュール間の連携テスト
3. **機能テスト (Functional Tests)**: エンドツーエンドの動作テスト
4. **パフォーマンステスト**: 速度やメモリ使用量のテスト

### テストディレクトリ構成

```
tests/
├── unit/
│   ├── test_transform.py
│   ├── test_fetch.py
│   └── test_utils.py
├── integration/
│   ├── test_api_client.py
│   └── test_data_pipeline.py
├── functional/
│   └── test_end_to_end.py
├── fixtures/
│   ├── sample_pokemon.json
│   └── sample_species.json
└── conftest.py
```

## テストフレームワーク

### pytest の使用

```bash
# 基本的な実行
pytest

# 詳細出力
pytest -v

# 特定のファイルのみ
pytest tests/test_transform.py

# 特定のテストのみ
pytest tests/test_transform.py::test_filter_by_language

# カバレッジ付き
pytest --cov=src --cov-report=html
```

### 非同期テストの実行

```bash
# pytest-asyncioを使用
pytest tests/test_async_fetch.py
```

## 単体テストの書き方

### JsonTransformerのテスト例

```python
# tests/unit/test_transform.py
import pytest
from src.extract.transform import JsonTransformer


class TestJsonTransformer:
    def setup_method(self):
        """各テストメソッドの前に実行"""
        self.transformer = JsonTransformer()

    def test_filter_by_language_japanese_only(self):
        """日本語のみを抽出するテスト"""
        data = {
            "names": [
                {"language": {"name": "ja"}, "name": "ピカチュウ"},
                {"language": {"name": "en"}, "name": "Pikachu"},
                {"language": {"name": "fr"}, "name": "Pikachu"}
            ]
        }

        result = self.transformer.filter_by_language(data)

        assert len(result["names"]) == 1
        assert result["names"][0]["name"] == "ピカチュウ"

    def test_collapse_name_basic(self):
        """名前の折りたたみテスト"""
        data = {
            "type": {"name": "electric"},
            "species": {"name": "pikachu"}
        }

        result = self.transformer.collapse_name(data)

        assert result["type"] == "electric"
        assert result["species"] == "pikachu"

    def test_strip_url_removes_urls(self):
        """URL削除のテスト"""
        data = {
            "name": "pikachu",
            "url": "https://pokeapi.co/api/v2/pokemon/25/",
            "type": {
                "name": "electric",
                "url": "https://pokeapi.co/api/v2/type/13/"
            }
        }

        result = self.transformer.strip_url(data)

        assert "url" not in result
        assert "url" not in result["type"]
        assert result["name"] == "pikachu"
        assert result["type"]["name"] == "electric"

    def test_unwrap_single_dict_list(self):
        """単一辞書リストのアンラップテスト"""
        data = {
            "stats": [{"base_stat": 35, "effort": 0}]
        }

        result = self.transformer.unwrap_single_dict_list(data)

        assert isinstance(result["stats"], dict)
        assert result["stats"]["base_stat"] == 35

    def test_all_transform_integration(self):
        """全変換処理の統合テスト"""
        data = {
            "id": 25,
            "name": "pikachu",
            "types": [
                {
                    "slot": 1,
                    "type": {
                        "name": "electric",
                        "url": "https://pokeapi.co/api/v2/type/13/"
                    }
                }
            ],
            "names": [
                {"language": {"name": "ja"}, "name": "ピカチュウ"},
                {"language": {"name": "en"}, "name": "Pikachu"}
            ]
        }

        result = self.transformer.all_transform(data)

        # 基本フィールドの確認
        assert result["id"] == 25
        assert result["name"] == "pikachu"

        # URL削除の確認
        assert "url" not in str(result)

        # 日本語フィルタリングの確認
        assert len(result["names"]) == 1
        assert result["names"][0]["name"] == "ピカチュウ"


# パラメータ化テストの例
@pytest.mark.parametrize("language,expected", [
    ("ja", True),
    ("ja-Hrkt", True),
    ("en", False),
    ("fr", False),
])
def test_language_filtering(language, expected):
    """言語フィルタリングのパラメータ化テスト"""
    transformer = JsonTransformer()
    data = {"language": {"name": language}, "name": "test"}

    result = transformer.filter_by_language([data])

    if expected:
        assert len(result) == 1
    else:
        assert len(result) == 0
```

## 統合テストの書き方

### API クライアントの統合テスト

```python
# tests/integration/test_api_client.py
import pytest
import asyncio
from unittest.mock import AsyncMock, patch
from src.fetch.client import ApiClient


class TestApiClientIntegration:
    @pytest.fixture
    def client(self):
        """APIクライアントのフィクスチャ"""
        return ApiClient()

    @pytest.mark.asyncio
    async def test_fetch_pokemon_integration(self, client):
        """ポケモンデータ取得の統合テスト"""
        # モックデータの準備
        mock_response = {
            "id": 25,
            "name": "pikachu",
            "types": [{"type": {"name": "electric"}}]
        }

        with patch.object(client, '_make_request', return_value=mock_response):
            result = await client.fetch_pokemon(25)

            assert result["id"] == 25
            assert result["name"] == "pikachu"
            assert result["types"][0]["type"]["name"] == "electric"

    @pytest.mark.asyncio
    async def test_fetch_multiple_pokemon(self, client):
        """複数ポケモンの並行取得テスト"""
        pokemon_ids = [1, 2, 3]

        with patch.object(client, 'fetch_pokemon', side_effect=lambda x: {"id": x, "name": f"pokemon_{x}"}):
            results = await asyncio.gather(*[client.fetch_pokemon(id) for id in pokemon_ids])

            assert len(results) == 3
            assert all(result["id"] in pokemon_ids for result in results)
```

## 機能テストの書き方

### エンドツーエンドテスト

```python
# tests/functional/test_end_to_end.py
import pytest
import tempfile
from pathlib import Path
from unittest.mock import patch
from src.extract.transform import JsonTransformer
from util.io_json import read_json, write_json


class TestEndToEnd:
    def test_complete_data_transformation_flow(self):
        """完全なデータ変換フローのテスト"""
        # テストデータの準備
        raw_data = {
            "id": 1,
            "name": "bulbasaur",
            "types": [
                {"slot": 1, "type": {"name": "grass", "url": "https://pokeapi.co/api/v2/type/12/"}},
                {"slot": 2, "type": {"name": "poison", "url": "https://pokeapi.co/api/v2/type/4/"}}
            ],
            "names": [
                {"language": {"name": "ja"}, "name": "フシギダネ"},
                {"language": {"name": "en"}, "name": "Bulbasaur"}
            ]
        }

        # 一時ファイルでのテスト
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            input_file = temp_path / "input.json"
            output_file = temp_path / "output.json"

            # 入力データの保存
            write_json(raw_data, input_file)

            # 変換処理の実行
            transformer = JsonTransformer()
            data = read_json(input_file)
            result = transformer.all_transform(data)
            write_json(result, output_file)

            # 結果の検証
            final_result = read_json(output_file)
            assert final_result["id"] == 1
            assert final_result["name"] == "bulbasaur"
            assert len(final_result["names"]) == 1
            assert final_result["names"][0]["name"] == "フシギダネ"
            assert "url" not in str(final_result)
```

## テストデータの管理

### フィクスチャファイルの作成

```python
# tests/conftest.py
import pytest
from pathlib import Path
import json


@pytest.fixture
def sample_pokemon_data():
    """サンプルポケモンデータ"""
    return {
        "id": 25,
        "name": "pikachu",
        "types": [{"type": {"name": "electric"}}],
        "names": [
            {"language": {"name": "ja"}, "name": "ピカチュウ"},
            {"language": {"name": "en"}, "name": "Pikachu"}
        ]
    }


@pytest.fixture
def sample_species_data():
    """サンプル種族データ"""
    return {
        "id": 25,
        "name": "pikachu",
        "genera": [
            {"language": {"name": "ja"}, "genus": "ねずみポケモン"},
            {"language": {"name": "en"}, "genus": "Mouse Pokémon"}
        ]
    }


@pytest.fixture
def fixtures_dir():
    """フィクスチャディレクトリのパス"""
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def temp_dir():
    """一時ディレクトリ"""
    import tempfile
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)
```

### フィクスチャファイルの使用

```python
# tests/unit/test_with_fixtures.py
import pytest
from util.io_json import read_json


class TestWithFixtures:
    def test_load_fixture_data(self, fixtures_dir):
        """フィクスチャデータの読み込みテスト"""
        sample_file = fixtures_dir / "sample_pokemon.json"
        data = read_json(sample_file)

        assert data["name"] == "pikachu"
        assert data["id"] == 25

    def test_use_fixture_data(self, sample_pokemon_data):
        """フィクスチャデータの使用テスト"""
        transformer = JsonTransformer()
        result = transformer.filter_by_language(sample_pokemon_data)

        assert len(result["names"]) == 1
        assert result["names"][0]["name"] == "ピカチュウ"
```

## モックとスタブの使用

### API呼び出しのモック

```python
# tests/unit/test_with_mocks.py
import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from src.fetch.client import ApiClient


class TestWithMocks:
    @pytest.mark.asyncio
    async def test_fetch_with_mock(self):
        """モックを使用したAPI呼び出しテスト"""
        mock_response = {"id": 1, "name": "bulbasaur"}

        with patch('aiohttp.ClientSession.get') as mock_get:
            mock_get.return_value.__aenter__.return_value.json = AsyncMock(return_value=mock_response)

            client = ApiClient()
            result = await client.fetch_pokemon(1)

            assert result["name"] == "bulbasaur"
            mock_get.assert_called_once()

    def test_file_io_mock(self):
        """ファイルI/Oのモック"""
        mock_data = {"test": "data"}

        with patch('util.io_json.read_json', return_value=mock_data) as mock_read:
            from util.io_json import read_json

            result = read_json("dummy_path")

            assert result == mock_data
            mock_read.assert_called_once_with("dummy_path")
```

## パフォーマンステスト

### 実行時間の測定

```python
# tests/performance/test_performance.py
import pytest
import time
from src.extract.transform import JsonTransformer


class TestPerformance:
    def test_transformation_performance(self):
        """変換処理の性能テスト"""
        transformer = JsonTransformer()

        # 大量のテストデータを生成
        large_data = {
            "names": [
                {"language": {"name": "ja"}, "name": f"テスト{i}"}
                for i in range(1000)
            ]
        }

        start_time = time.time()
        result = transformer.filter_by_language(large_data)
        end_time = time.time()

        execution_time = end_time - start_time

        # 1秒以内で完了することを確認
        assert execution_time < 1.0
        assert len(result["names"]) == 1000

    @pytest.mark.benchmark
    def test_benchmark_transformation(self, benchmark):
        """ベンチマークテスト（pytest-benchmarkが必要）"""
        transformer = JsonTransformer()
        data = {"names": [{"language": {"name": "ja"}, "name": "テスト"}]}

        result = benchmark(transformer.filter_by_language, data)

        assert len(result["names"]) == 1
```

## テストの実行

### 基本的な実行方法

```bash
# 全テストの実行
pytest

# 詳細出力
pytest -v

# 特定のディレクトリのみ
pytest tests/unit/

# 特定のマークのみ
pytest -m "unit"

# カバレッジ付き
pytest --cov=src --cov-report=html

# 並列実行
pytest -n auto
```

### 継続的テスト

```bash
# ファイル変更監視
pytest-watch

# または
ptw
```

## テストの品質管理

### カバレッジ目標
- **単体テスト**: 90%以上
- **統合テスト**: 70%以上
- **全体**: 85%以上

### テストメトリクス

```bash
# カバレッジレポート
pytest --cov=src --cov-report=html --cov-report=term-missing

# 失敗したテストの詳細
pytest --tb=long

# 実行時間の測定
pytest --durations=10
```

## 関連項目

- [Development Setup](setup.md) - 開発環境設定
- [Contributing](contributing.md) - コントリビューション方法
- [Usage](../usage.md) - 基本的な使用方法
