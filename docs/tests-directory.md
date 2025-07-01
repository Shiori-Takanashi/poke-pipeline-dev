# tests/ ディレクトリ解説

このディレクトリには、プロジェクトの品質を保証するためのテストコードが格納されています。

## ファイル一覧

### test_fetch_target.py
`src/fetch/fetch_target.py` の機能をテストするファイルです。

**テスト対象:**
- データ取得機能の正常動作
- 非同期処理の検証
- エラーハンドリングの確認
- APIレスポンスの妥当性チェック

**テスト内容（推定）:**
- エンドポイントURL生成の正確性
- JSON保存機能の動作確認
- 並列処理の制御
- タイムアウト処理

### test_paths_json.py
`src/pathing/paths_json.py` のパス管理機能をテストするファイルです。

**テスト対象:**
- JSONファイルパスの生成
- ディレクトリ構造の検証
- パスの正規化処理
- ファイル存在チェック

**テスト内容（推定）:**
- 相対パスと絶対パスの変換
- 不正なパス文字列の処理
- ディレクトリ作成の確認
- パス結合の正確性

### test_re_endpoint_name.py
`util/re_endpoint_name.py` の正規表現処理をテストするファイルです。

**テスト対象:**
- エンドポイント名の正規化
- パターンマッチング機能
- 文字列変換ルール
- 特殊文字の処理

**テスト内容（推定）:**
- 様々なエンドポイント名パターンの処理
- 無効な入力に対するエラーハンドリング
- 変換ルールの一貫性
- エッジケースの処理

## テスト実行方法

### 全テストの実行
```bash
# プロジェクトルートから実行
python -m pytest tests/

# または
python -m unittest discover tests/
```

### 個別テストの実行
```bash
# 特定のテストファイルを実行
python -m pytest tests/test_fetch_target.py

# 特定のテストケースを実行
python -m pytest tests/test_fetch_target.py::TestClassName::test_method_name
```

### カバレッジ測定
```bash
# テストカバレッジの測定
pip install coverage
coverage run -m pytest tests/
coverage report
coverage html  # HTML形式のレポート生成
```

## テスト設計方針

### 単体テスト（Unit Tests）
- 各関数・メソッドの個別テスト
- モックを使用した外部依存の排除
- エッジケースの網羅的なテスト

### 統合テスト（Integration Tests）
- モジュール間の連携テスト
- 実際のAPI呼び出しを含むテスト
- データフローの検証

### テストデータ管理
- テスト用のサンプルデータ
- モックレスポンスの管理
- テスト環境の分離

## ベストプラクティス

### テストの命名規則
```python
def test_fetch_target_with_valid_endpoint():
    """有効なエンドポイントでのデータ取得テスト"""
    pass

def test_fetch_target_with_invalid_endpoint():
    """無効なエンドポイントでのエラーハンドリングテスト"""
    pass
```

### アサーション
```python
import unittest

class TestFetchTarget(unittest.TestCase):
    def test_url_generation(self):
        names, urls = get_name_and_url()
        self.assertIsInstance(names, list)
        self.assertIsInstance(urls, list)
        self.assertEqual(len(names), len(urls))
```

### 非同期テスト
```python
import asyncio
import unittest

class TestAsyncFetch(unittest.TestCase):
    def test_async_fetch(self):
        async def test_coro():
            result = await fetch_data()
            self.assertIsNotNone(result)

        asyncio.run(test_coro())
```

## 継続的改善

- **テストカバレッジの向上**: 新機能追加時の対応テスト作成
- **パフォーマンステスト**: 大量データ処理時の性能測定
- **回帰テスト**: バグ修正後の再発防止テスト
- **ドキュメント更新**: テスト仕様書の維持管理
