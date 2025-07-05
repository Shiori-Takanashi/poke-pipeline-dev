# Fetch Module

Fetchモジュールは、PokéAPIからデータを取得するための機能を提供します。

## 概要

このモジュールは非同期処理を活用して、効率的にPokéAPIからデータを取得します。セマフォによる並行制御、リトライ機能、エラーハンドリングなどの機能を含みます。

## 主要コンポーネント

### ApiClient

PokéAPIとの通信を担当するクライアントクラスです。

```python
from src.fetch.client import ApiClient

client = ApiClient()
```

#### メソッド

##### fetch_pokemon(pokemon_id)

指定されたIDのポケモンデータを取得します。

**パラメータ:**
- `pokemon_id`: ポケモンID（int）

**戻り値:**
- ポケモンデータの辞書

**例:**
```python
async def main():
    client = ApiClient()
    pokemon_data = await client.fetch_pokemon(25)  # ピカチュウ
    print(pokemon_data['name'])  # "pikachu"
```

##### fetch_pokemon_species(species_id)

指定されたIDのポケモン種族データを取得します。

**パラメータ:**
- `species_id`: 種族ID（int）

**戻り値:**
- 種族データの辞書

##### fetch_endpoint(endpoint, resource_id)

汎用エンドポイントからデータを取得します。

**パラメータ:**
- `endpoint`: エンドポイント名（str）
- `resource_id`: リソースID（int）

**戻り値:**
- リソースデータの辞書

### DataFetcher

データ取得の管理とバッチ処理を行うクラスです。

```python
from src.fetch.fetcher import DataFetcher

fetcher = DataFetcher(max_concurrent=50)
```

#### メソッド

##### fetch_multiple(endpoints, ids)

複数のエンドポイントから複数のリソースを並行取得します。

**パラメータ:**
- `endpoints`: エンドポイント名のリスト
- `ids`: 取得するIDのリスト

**戻り値:**
- 取得結果の辞書

##### fetch_range(endpoint, start_id, end_id)

指定した範囲のリソースを取得します。

**パラメータ:**
- `endpoint`: エンドポイント名
- `start_id`: 開始ID
- `end_id`: 終了ID

**戻り値:**
- 取得結果のリスト

## 使用例

### 基本的な使用方法

```python
import asyncio
from src.fetch.client import ApiClient

async def main():
    client = ApiClient()

    # 単一ポケモンの取得
    pikachu = await client.fetch_pokemon(25)
    print(f"Name: {pikachu['name']}")

    # 種族データの取得
    species = await client.fetch_pokemon_species(25)
    print(f"Species: {species['name']}")

asyncio.run(main())
```

### 複数データの並行取得

```python
import asyncio
from src.fetch.fetcher import DataFetcher

async def main():
    fetcher = DataFetcher(max_concurrent=10)

    # 複数ポケモンの並行取得
    pokemon_ids = [1, 2, 3, 4, 5]
    results = await fetcher.fetch_multiple(['pokemon'], pokemon_ids)

    for pokemon_data in results:
        print(f"Name: {pokemon_data['name']}")

asyncio.run(main())
```

### エラーハンドリング付き取得

```python
import asyncio
from src.fetch.client import ApiClient
from src.fetch.exceptions import FetchError

async def main():
    client = ApiClient()

    try:
        # 存在しないIDを指定
        pokemon = await client.fetch_pokemon(99999)
    except FetchError as e:
        print(f"取得エラー: {e}")
    except Exception as e:
        print(f"予期しないエラー: {e}")

asyncio.run(main())
```

## 設定オプション

### 並行処理の制御

```python
# 最大並行数の設定
fetcher = DataFetcher(max_concurrent=50)

# タイムアウト時間の設定
client = ApiClient(timeout=30)
```

### リトライ設定

```python
# リトライ回数の設定
client = ApiClient(max_retries=3)

# リトライ間隔の設定
client = ApiClient(retry_delay=1.0)
```

### レート制限対応

```python
# リクエスト間隔の設定
client = ApiClient(rate_limit=1.0)  # 1秒間隔
```

## エラーハンドリング

### 例外の種類

- `FetchError`: データ取得時の一般的なエラー
- `TimeoutError`: タイムアウトエラー
- `RateLimitError`: レート制限エラー
- `NotFoundError`: リソースが見つからないエラー

### エラー対応例

```python
async def safe_fetch_pokemon(client, pokemon_id):
    try:
        return await client.fetch_pokemon(pokemon_id)
    except NotFoundError:
        print(f"ポケモンID {pokemon_id} は存在しません")
        return None
    except RateLimitError:
        print("レート制限に達しました。しばらく待ってから再試行してください")
        await asyncio.sleep(60)
        return await client.fetch_pokemon(pokemon_id)
    except FetchError as e:
        print(f"取得エラー: {e}")
        return None
```

## パフォーマンス最適化

### 並行処理の最適化

```python
# CPU集約的な処理の場合
fetcher = DataFetcher(max_concurrent=10)

# I/O集約的な処理の場合
fetcher = DataFetcher(max_concurrent=100)
```

### メモリ使用量の最適化

```python
# ストリーミング処理
async def process_large_dataset(fetcher, ids):
    batch_size = 100
    for i in range(0, len(ids), batch_size):
        batch = ids[i:i+batch_size]
        results = await fetcher.fetch_multiple(['pokemon'], batch)

        # 処理とメモリ解放
        process_batch(results)
        del results  # メモリ解放
```

## 監視とログ

### ログ出力

```python
import logging

# ログの設定
logging.basicConfig(level=logging.INFO)

# 詳細ログの有効化
client = ApiClient(debug=True)
```

### 進捗監視

```python
from tqdm import tqdm

async def fetch_with_progress(fetcher, ids):
    with tqdm(total=len(ids)) as pbar:
        async def fetch_with_callback(pokemon_id):
            result = await fetcher.fetch_pokemon(pokemon_id)
            pbar.update(1)
            return result

        tasks = [fetch_with_callback(id) for id in ids]
        return await asyncio.gather(*tasks)
```

## 関連項目

- [Usage](../usage.md#データ取得コマンド) - コマンドライン使用方法
- [Architecture](../architecture.md#fetch-module) - 設計詳細
- [Examples](../examples/basic.md#データ取得) - 使用例
