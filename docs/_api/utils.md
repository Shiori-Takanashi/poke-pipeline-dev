# Utilities

ユーティリティモジュールは、プロジェクト全体で共通して使用される汎用的な機能を提供します。

## 概要

このモジュールは、ファイルI/O、ディレクトリ操作、言語処理、データ処理などの共通機能を提供し、コードの重複を削減し、保守性を向上させます。

## 主要コンポーネント

### io_json.py

JSON ファイルの読み書きを行うユーティリティです。

```python
from util.io_json import read_json, write_json
```

#### 関数一覧

##### read_json(file_path)

JSONファイルを読み込みます。

**パラメータ:**
- `file_path`: JSONファイルのパス（Path または str）

**戻り値:**
- 読み込んだJSONデータ（dict または list）

**例:**
```python
from pathlib import Path
from util.io_json import read_json

data = read_json(Path("data/pokemon.json"))
print(data["name"])
```

##### write_json(data, file_path, indent=2)

データをJSONファイルに書き込みます。

**パラメータ:**
- `data`: 書き込むデータ
- `file_path`: 出力先ファイルパス（Path または str）
- `indent`: インデントのスペース数（デフォルト: 2）

**例:**
```python
from util.io_json import write_json

pokemon_data = {"name": "pikachu", "id": 25}
write_json(pokemon_data, "output/pikachu.json")
```

##### read_json_batch(file_paths)

複数のJSONファイルを一括読み込みします。

**パラメータ:**
- `file_paths`: ファイルパスのリスト

**戻り値:**
- 読み込んだデータのリスト

### directory.py

ディレクトリ操作を行うユーティリティです。

```python
from util.directory import ensure_dir, list_files, clean_directory
```

#### 関数一覧

##### ensure_dir(directory_path)

ディレクトリが存在しない場合は作成します。

**パラメータ:**
- `directory_path`: ディレクトリパス（Path または str）

**例:**
```python
from util.directory import ensure_dir

ensure_dir("data/pokemon")
ensure_dir("logs")
```

##### list_files(directory_path, pattern="*")

指定したディレクトリ内のファイルを一覧取得します。

**パラメータ:**
- `directory_path`: ディレクトリパス
- `pattern`: ファイル名パターン（デフォルト: "*"）

**戻り値:**
- ファイルパスのリスト

**例:**
```python
from util.directory import list_files

# 全ファイル
all_files = list_files("data")

# JSONファイルのみ
json_files = list_files("data", "*.json")
```

##### clean_directory(directory_path, keep_recent=10)

ディレクトリ内の古いファイルを削除します。

**パラメータ:**
- `directory_path`: ディレクトリパス
- `keep_recent`: 保持する最新ファイル数（デフォルト: 10）

### language.py

言語処理に関するユーティリティです。

```python
from util.language import is_japanese, extract_language, normalize_language_code
```

#### 関数一覧

##### is_japanese(language_code)

言語コードが日本語かどうかを判定します。

**パラメータ:**
- `language_code`: 言語コード（str）

**戻り値:**
- 日本語の場合True、それ以外False

**例:**
```python
from util.language import is_japanese

print(is_japanese("ja"))      # True
print(is_japanese("ja-Hrkt")) # True
print(is_japanese("en"))      # False
```

##### extract_language(data, language_key="language")

データから言語情報を抽出します。

**パラメータ:**
- `data`: 抽出対象のデータ
- `language_key`: 言語キー名（デフォルト: "language"）

**戻り値:**
- 言語コード（str）

##### normalize_language_code(language_code)

言語コードを正規化します。

**パラメータ:**
- `language_code`: 言語コード

**戻り値:**
- 正規化された言語コード

### process_idx.py

インデックス処理に関するユーティリティです。

```python
from util.process_idx import pad_index, parse_index_range, generate_index_list
```

#### 関数一覧

##### pad_index(index, width=5)

インデックスを指定した桁数でゼロパディングします。

**パラメータ:**
- `index`: インデックス値（int）
- `width`: パディング幅（デフォルト: 5）

**戻り値:**
- パディングされた文字列

**例:**
```python
from util.process_idx import pad_index

print(pad_index(1))    # "00001"
print(pad_index(25))   # "00025"
print(pad_index(1000)) # "01000"
```

##### parse_index_range(range_str)

範囲文字列を解析してインデックスリストを生成します。

**パラメータ:**
- `range_str`: 範囲文字列（例: "1-10", "1,3,5-8"）

**戻り値:**
- インデックスのリスト

**例:**
```python
from util.process_idx import parse_index_range

indices = parse_index_range("1-5,10,15-17")
print(indices)  # [1, 2, 3, 4, 5, 10, 15, 16, 17]
```

##### generate_index_list(total_count, batch_size=100)

指定した総数を基にバッチ処理用のインデックスリストを生成します。

**パラメータ:**
- `total_count`: 総数
- `batch_size`: バッチサイズ（デフォルト: 100）

**戻り値:**
- バッチインデックスのリスト

### re_endpoint_name.py

エンドポイント名の正規化を行うユーティリティです。

```python
from util.re_endpoint_name import normalize_endpoint_name, extract_endpoint_id
```

#### 関数一覧

##### normalize_endpoint_name(endpoint_name)

エンドポイント名を正規化します（ハイフンをアンダースコアに変換）。

**パラメータ:**
- `endpoint_name`: エンドポイント名

**戻り値:**
- 正規化されたエンドポイント名

**例:**
```python
from util.re_endpoint_name import normalize_endpoint_name

print(normalize_endpoint_name("pokemon-species"))  # "pokemon_species"
print(normalize_endpoint_name("version-group"))    # "version_group"
```

##### extract_endpoint_id(url)

URLからエンドポイントIDを抽出します。

**パラメータ:**
- `url`: API URL

**戻り値:**
- エンドポイントID（int）

**例:**
```python
from util.re_endpoint_name import extract_endpoint_id

url = "https://pokeapi.co/api/v2/pokemon/25/"
id = extract_endpoint_id(url)
print(id)  # 25
```

## 使用例

### 基本的な使用方法

```python
from util.io_json import read_json, write_json
from util.directory import ensure_dir
from util.language import is_japanese
from util.process_idx import pad_index

# ディレクトリの作成
ensure_dir("output")

# JSONファイルの読み込み
data = read_json("input/pokemon.json")

# 日本語データのフィルタリング
japanese_data = []
for item in data.get("names", []):
    if is_japanese(item.get("language", {}).get("name", "")):
        japanese_data.append(item)

# インデックスのパディング
padded_id = pad_index(data["id"])

# 結果の保存
output_file = f"output/pokemon_{padded_id}.json"
write_json(japanese_data, output_file)
```

### バッチ処理の例

```python
from util.io_json import read_json_batch
from util.directory import list_files
from util.process_idx import generate_index_list

# 複数ファイルの一括読み込み
json_files = list_files("data", "*.json")
all_data = read_json_batch(json_files)

# バッチ処理用インデックスの生成
batch_indices = generate_index_list(len(all_data), batch_size=50)

# バッチ処理の実行
for batch_start, batch_end in batch_indices:
    batch_data = all_data[batch_start:batch_end]
    # バッチ処理の実行
    process_batch(batch_data)
```

### エラーハンドリング付きの処理

```python
from util.io_json import read_json, write_json
from util.directory import ensure_dir
import logging

def safe_process_file(input_file, output_file):
    try:
        # ディレクトリの確保
        ensure_dir(output_file.parent)

        # データの読み込み
        data = read_json(input_file)

        # データの処理
        processed_data = process_data(data)

        # 結果の保存
        write_json(processed_data, output_file)

        logging.info(f"Successfully processed {input_file}")

    except FileNotFoundError:
        logging.error(f"Input file not found: {input_file}")
    except Exception as e:
        logging.error(f"Error processing {input_file}: {e}")
```

## パフォーマンス最適化

### 大量ファイルの処理

```python
from util.io_json import read_json
from util.directory import list_files
from concurrent.futures import ThreadPoolExecutor

def process_file_parallel(file_path):
    data = read_json(file_path)
    return process_data(data)

# 並列処理で高速化
json_files = list_files("data", "*.json")
with ThreadPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(process_file_parallel, json_files))
```

### メモリ効率的な処理

```python
from util.io_json import read_json
from util.directory import list_files

def process_files_streaming(directory):
    """ファイルをストリーミング処理してメモリ使用量を抑制"""
    for file_path in list_files(directory, "*.json"):
        data = read_json(file_path)
        processed_data = process_data(data)

        # 処理後すぐに結果を保存してメモリ解放
        output_path = f"output/{file_path.stem}_processed.json"
        write_json(processed_data, output_path)

        # 明示的にメモリ解放
        del data, processed_data
```

## 関連項目

- [API Reference](jsontransformer.md) - データ変換API
- [Usage](../usage.md) - 基本的な使用方法
- [Examples](../examples/basic.md) - 使用例
