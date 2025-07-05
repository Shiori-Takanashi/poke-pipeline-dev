# Config Module

Configモジュールは、プロジェクト全体の設定を管理するためのモジュールです。

## 概要

このモジュールは、ファイルパス、定数、対象エンドポイントなどの設定を一元管理し、コードの保守性と再利用性を向上させます。

## 主要コンポーネント

### constant.py

アプリケーション全体で使用される定数を定義します。

```python
from config.constant import *
```

#### 定数一覧

##### API関連
- `API_BASE_URL`: PokéAPIのベースURL
- `API_VERSION`: APIバージョン
- `MAX_CONCURRENT_REQUESTS`: 最大並行リクエスト数
- `REQUEST_TIMEOUT`: リクエストタイムアウト時間
- `RETRY_ATTEMPTS`: リトライ試行回数

##### ログ関連
- `LOG_LEVEL`: ログレベル
- `LOG_FORMAT`: ログフォーマット
- `LOG_FILE_MAX_SIZE`: ログファイルの最大サイズ

##### データ処理関連
- `SUPPORTED_LANGUAGES`: サポートする言語コード
- `DEFAULT_LANGUAGE`: デフォルト言語
- `BATCH_SIZE`: バッチ処理サイズ

### target.py

データ取得対象のエンドポイントを定義します。

```python
from config.target import ENDPOINTS, ENDPOINT_LIMITS
```

#### エンドポイント設定

##### ENDPOINTS
取得対象のエンドポイントリスト：

```python
ENDPOINTS = [
    "pokemon",
    "pokemon-species",
    "pokemon-form",
    "type",
    "ability",
    "move",
    "version",
    "version-group"
]
```

##### ENDPOINT_LIMITS
各エンドポイントの取得上限：

```python
ENDPOINT_LIMITS = {
    "pokemon": 1010,
    "pokemon-species": 1010,
    "type": 20,
    "ability": 327,
    "move": 919
}
```

### dirpath.py

ディレクトリパスを定義します。

```python
from config.dirpath import *
```

#### ディレクトリパス一覧

- `PROJECT_ROOT`: プロジェクトルートディレクトリ
- `JSON_DIR`: JSONファイル保存ディレクトリ
- `DATABASE_DIR`: データベースファイル保存ディレクトリ
- `LOG_DIR`: ログファイル保存ディレクトリ
- `CONFIG_DIR`: 設定ファイル保存ディレクトリ
- `DOCS_DIR`: ドキュメント保存ディレクトリ
- `TESTS_DIR`: テストファイル保存ディレクトリ

### filepath.py

ファイルパスを定義します。

```python
from config.filepath import *
```

#### ファイルパス一覧

- `DATABASE_FILE`: SQLiteデータベースファイル
- `LOG_FILE`: メインログファイル
- `CONFIG_FILE`: 設定ファイル
- `SPECIES_MAPPING_FILE`: 種族マッピングファイル

### json_type.py

JSONデータの型定義を行います。

```python
from config.json_type import PokemonData, SpeciesData
```

#### 型定義

##### PokemonData
```python
from typing import Dict, List, Optional
from pydantic import BaseModel

class PokemonData(BaseModel):
    id: int
    name: str
    types: List[Dict[str, str]]
    abilities: List[Dict[str, str]]
    stats: List[Dict[str, int]]
    height: int
    weight: int
```

##### SpeciesData
```python
class SpeciesData(BaseModel):
    id: int
    name: str
    names: List[Dict[str, str]]
    genera: List[Dict[str, str]]
    flavor_text_entries: List[Dict[str, str]]
```

## 使用例

### 基本的な使用方法

```python
from config.constant import API_BASE_URL, MAX_CONCURRENT_REQUESTS
from config.target import ENDPOINTS
from config.dirpath import JSON_DIR
from config.filepath import DATABASE_FILE

# API設定の使用
print(f"API URL: {API_BASE_URL}")
print(f"Max concurrent: {MAX_CONCURRENT_REQUESTS}")

# エンドポイント設定の使用
for endpoint in ENDPOINTS:
    print(f"Processing endpoint: {endpoint}")

# パス設定の使用
json_path = JSON_DIR / "pokemon.json"
print(f"JSON path: {json_path}")
```

### 環境固有の設定

```python
import os
from config.constant import LOG_LEVEL

# 環境変数での設定上書き
log_level = os.getenv("LOG_LEVEL", LOG_LEVEL)
api_url = os.getenv("API_BASE_URL", API_BASE_URL)
```

### データベース設定

```python
from config.filepath import DATABASE_FILE
import sqlite3

# データベース接続
conn = sqlite3.connect(DATABASE_FILE)
```

## 設定のカスタマイズ

### 開発環境での設定

```python
# config/constant.py
if os.getenv("ENVIRONMENT") == "development":
    LOG_LEVEL = "DEBUG"
    MAX_CONCURRENT_REQUESTS = 10
    REQUEST_TIMEOUT = 60
```

### 本番環境での設定

```python
# config/constant.py
if os.getenv("ENVIRONMENT") == "production":
    LOG_LEVEL = "INFO"
    MAX_CONCURRENT_REQUESTS = 50
    REQUEST_TIMEOUT = 30
```

### テスト環境での設定

```python
# config/constant.py
if os.getenv("ENVIRONMENT") == "test":
    LOG_LEVEL = "WARNING"
    MAX_CONCURRENT_REQUESTS = 5
    DATABASE_FILE = ":memory:"
```

## 設定の検証

### 設定値の妥当性チェック

```python
from config.constant import MAX_CONCURRENT_REQUESTS, REQUEST_TIMEOUT

def validate_config():
    assert MAX_CONCURRENT_REQUESTS > 0, "MAX_CONCURRENT_REQUESTS must be positive"
    assert REQUEST_TIMEOUT > 0, "REQUEST_TIMEOUT must be positive"
    assert REQUEST_TIMEOUT <= 300, "REQUEST_TIMEOUT must be <= 300 seconds"

validate_config()
```

### 必要なディレクトリの作成

```python
from config.dirpath import JSON_DIR, LOG_DIR, DATABASE_DIR

def ensure_directories():
    for directory in [JSON_DIR, LOG_DIR, DATABASE_DIR]:
        directory.mkdir(parents=True, exist_ok=True)

ensure_directories()
```

## 設定の動的変更

### 実行時設定変更

```python
import config.constant as const

# 実行時に設定を変更
const.MAX_CONCURRENT_REQUESTS = 20
const.LOG_LEVEL = "DEBUG"
```

### 設定ファイルからの読み込み

```python
import yaml
from pathlib import Path

def load_config_from_file(config_file: Path):
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)

    # 設定の適用
    const.MAX_CONCURRENT_REQUESTS = config.get('max_concurrent', const.MAX_CONCURRENT_REQUESTS)
    const.LOG_LEVEL = config.get('log_level', const.LOG_LEVEL)
```

## 型安全性

### 型チェック

```python
from typing import List, Dict, Any
from config.json_type import PokemonData

def process_pokemon_data(data: Dict[str, Any]) -> PokemonData:
    # pydanticによる型チェックとバリデーション
    return PokemonData(**data)
```

### 設定の型定義

```python
from typing import Final

# 型安全な定数定義
API_BASE_URL: Final[str] = "https://pokeapi.co/api/v2"
MAX_CONCURRENT_REQUESTS: Final[int] = 50
```

## 関連項目

- [Architecture](../architecture.md#configuration-layer) - 設計詳細
- [Usage](../usage.md#設定のカスタマイズ) - 設定使用方法
- [Development](../development/setup.md) - 開発環境設定
