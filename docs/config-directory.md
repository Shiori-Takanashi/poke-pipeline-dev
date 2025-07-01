# config/ ディレクトリ解説

このディレクトリには、パイプライン全体の設定を管理するファイルが格納されています。

## ファイル一覧

### constant.py
アプリケーション全体で使用される定数を定義するファイルです。

**主要な定数:**
- `BASE_URL`: PokeAPIのベースURL (`https://pokeapi.co/api/v2/`)
- `SEMAPHORE_INT`: 非同期処理での同時実行数制限 (50)
- `RETRYS_INT`: API呼び出し失敗時のリトライ回数 (5)
- `TIMEOUT_INT`: APIリクエストのタイムアウト時間 (10秒)

### target.py
データ収集の対象となるエンドポイントを定義するファイルです。

**主要な設定:**
- `FETCH_TARGET`: 取得対象のエンドポイント一覧
  - pokemon-species (ポケモン種族データ)
  - pokemon (ポケモン個体データ)
  - pokemon-form (ポケモンフォルムデータ)
  - type (タイプデータ)
  - ability (特性データ)
  - move (技データ)
  - version (バージョンデータ)
  - version-group (バージョングループデータ)

- `MONSTER_TARGET`: ポケモン関連データのサブセット
  - pokemon-species
  - pokemon
  - pokemon-form

### dirpath.py
ディレクトリパスの設定を管理するファイルです。プロジェクト内で使用される各種ディレクトリの絶対パスや相対パスを定義しています。

### filepath.py
ファイルパスの設定を管理するファイルです。特定のファイルへのパスや、ファイル名の生成ルールなどを定義しています。

## 使用方法

これらの設定ファイルは他のモジュールからインポートして使用されます：

```python
from config.constant import BASE_URL, SEMAPHORE_INT
from config.target import FETCH_TARGET
```

設定を変更する際は、このディレクトリ内のファイルを編集することで、アプリケーション全体の挙動を調整できます。
