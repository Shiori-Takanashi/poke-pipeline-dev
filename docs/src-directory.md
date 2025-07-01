# src/ ディレクトリ解説

このディレクトリには、アプリケーションのメインとなるソースコードが格納されています。

## ディレクトリ構成

### fetch/
データ収集（フェッチ）に関連する機能を提供するモジュール群です。

#### fetch_target.py
- **目的**: PokeAPIからデータを非同期で取得するメイン機能
- **主要な機能**:
  - `setup_dir()`: JSONファイル保存用ディレクトリの作成
  - `get_name_and_url()`: エンドポイント名とURLの構築
  - `fetch_all()`: 複数エンドポイントからの並列データ取得
  - 非同期HTTP通信によるデータ取得
  - プログレスバー表示
  - エラーハンドリングとリトライ機能

#### fetch_endpoints.py
- **目的**: 特定のエンドポイントに対する詳細なデータ取得機能
- **機能**: 個別エンドポイントの処理ロジック

### extract/
取得したデータの変換・抽出処理を行うモジュール群です。

#### transform.py
- **目的**: データの形式変換や正規化
- **機能**: JSONデータの構造変換、データクリーニング

#### flavor_text.py
- **目的**: フレーバーテキスト（説明文）の処理
- **機能**: 多言語対応テキストの抽出と整形

#### strip_url.py
- **目的**: URL文字列の処理
- **機能**: URLからIDの抽出、パス正規化

### mapping/
データマッピングとリレーション処理を行うモジュール群です。

#### json_mapping.py
- **目的**: JSONデータ間の関連付け
- **機能**: 異なるエンドポイントから取得したデータの関連付け

#### spf_mapping.py
- **目的**: Species-Pokemon-Form（種族-ポケモン-フォルム）の関連付け
- **機能**: ポケモンの階層構造データの整理

### pathing/
ファイルパス管理に関するモジュール群です。

#### paths_json.py
- **目的**: JSONファイルのパス管理
- **機能**: 動的なパス生成、ファイル存在チェック

## 使用例

```python
# データ取得の実行
from src.fetch.fetch_target import fetch_all, get_name_and_url

names, urls = get_name_and_url()
await fetch_all(urls, names)

# データ変換の実行
from src.extract.transform import transform_data
transformed_data = transform_data(raw_json_data)
```

## 設計思想

- **非同期処理**: aiohttp を使用した効率的なAPI呼び出し
- **モジュラー設計**: 機能ごとにモジュールを分離
- **設定駆動**: config/ ディレクトリからの設定読み込み
- **エラーハンドリング**: 堅牢なエラー処理とログ出力
