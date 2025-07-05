# Usage

このページでは、poke-pipelineの具体的な使用方法について説明します。

## CLI コマンド

### デモコマンド

```bash
# 基本的なデモ実行
python -m cli.demo

# 特定のポケモンIDでデモ実行
python -m cli.demo --pokemon-id 25  # ピカチュウ
```

### データ取得コマンド

```bash
# 単一ポケモンの取得
python -m src.fetch.main --pokemon-id 1

# 複数ポケモンの取得
python -m src.fetch.main --pokemon-id 1,2,3

# 範囲指定での取得
python -m src.fetch.main --range 1-10

# 全ポケモンの取得（注意：時間がかかります）
python -m src.fetch.main --all
```

### データ変換コマンド

```bash
# JSONデータの変換
python -m src.extract.transform

# 特定ファイルの変換
python -m src.extract.transform --input path/to/input.json --output path/to/output.json
```

## API使用例

### JsonTransformerの使用

```python
from src.extract.transform import JsonTransformer

# インスタンスの作成
transformer = JsonTransformer()

# サンプルデータ
data = {
    "name": "pikachu",
    "types": [
        {"type": {"name": "electric", "url": "https://pokeapi.co/api/v2/type/13/"}},
        {"type": {"name": "normal", "url": "https://pokeapi.co/api/v2/type/1/"}}
    ],
    "names": [
        {"language": {"name": "ja"}, "name": "ピカチュウ"},
        {"language": {"name": "en"}, "name": "Pikachu"},
        {"language": {"name": "fr"}, "name": "Pikachu"}
    ]
}

# 全変換処理の実行
result = transformer.all_transform(data)
print(result)
```

### 個別変換メソッドの使用

```python
# URL削除
clean_data = transformer.strip_url(data)

# 名前の折りたたみ
collapsed_data = transformer.collapse_name(data)

# 言語フィルタリング
filtered_data = transformer.filter_by_language(data, allowed=("ja", "ja-Hrkt"))

# 単一辞書リストのアンラップ
unwrapped_data = transformer.unwrap_single_dict_list(data)
```

## 設定のカスタマイズ

### 対象エンドポイントの変更

`config/target.py` で取得対象を変更できます：

```python
# 特定のエンドポイントのみを対象とする場合
ENDPOINTS = [
    "pokemon",
    "pokemon-species",
    "type"
]
```

### ディレクトリパスの変更

`config/dirpath.py` でデータ保存先を変更できます：

```python
# JSONデータの保存先
JSON_DIR = Path("custom_json")

# データベースファイルの保存先
DATABASE_DIR = Path("custom_database")
```

### ログ設定

ログレベルや出力先は `config/constant.py` で設定できます：

```python
# ログレベル
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR

# ログファイル
LOG_FILE = "logs/custom.log"
```

## バッチ処理

### 大量データの処理

```bash
# 非同期処理で高速取得
python -m src.fetch.async_main --max-concurrent 50

# 進捗表示付き
python -m src.fetch.main --progress
```

### スケジュール実行

cronやタスクスケジューラーで定期実行する場合：

```bash
# 毎日午前2時に実行（cron例）
0 2 * * * cd /path/to/poke-pipeline && python -m src.fetch.main --all
```

## データ形式

### 取得データの構造

```json
{
  "id": 1,
  "name": "bulbasaur",
  "types": [
    {"type": "grass"},
    {"type": "poison"}
  ],
  "names": [
    {"language": "ja", "name": "フシギダネ"}
  ]
}
```

### 変換後データの構造

```json
{
  "id": 1,
  "name": "bulbasaur",
  "types": ["grass", "poison"],
  "names": "フシギダネ"
}
```

## パフォーマンス最適化

### 並行処理の調整

```python
# 最大並行数を調整
MAX_CONCURRENT = 50  # デフォルト

# タイムアウト設定
REQUEST_TIMEOUT = 30  # 秒
```

### メモリ使用量の削減

```python
# 大きなデータセットの処理時
# ストリーミング処理やバッチ処理を使用
```

## デバッグ

### ログの確認

```bash
# ログファイルの確認
tail -f logs/__main__.log

# 特定レベルのログのみ表示
grep "ERROR" logs/__main__.log
```

### デバッグモードの実行

```bash
# 詳細ログ付きでの実行
python -m src.fetch.main --debug --verbose
```

## 次のステップ

- [Architecture](architecture.md) - システム設計の詳細
- [API Reference](api/jsontransformer.md) - APIドキュメント
- [Examples](examples/basic.md) - より多くの使用例
