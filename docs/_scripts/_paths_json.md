# paths_json.py

## 概要
JSONディレクトリ構造を操作するユーティリティ関数群。ディレクトリの列挙と名前による検索機能を提供。

## 主要機能

### 関数詳細

1. **`get_dirpath_sub_jsons(json_dir_path: Path = JSON_DIR_PATH) -> List[Path]`**
   - **目的**: JSON_DIR_PATH以下のサブディレクトリを列挙
   - **パラメータ**:
     - `json_dir_path`: 検索対象ディレクトリ（デフォルト：`JSON_DIR_PATH`）
   - **戻り値**: ディレクトリパスのリスト
   - **例外**: `FileNotFoundError` - 指定パスが存在しない場合

2. **`get_dirpath_sub_json_by_name(dirpath_sub_jsons: List[Path], dirname_json: str) -> Path`**
   - **目的**: 名前を指定してディレクトリパスを取得
   - **パラメータ**:
     - `dirpath_sub_jsons`: 検索対象ディレクトリリスト
     - `dirname_json`: 検索するディレクトリ名
   - **戻り値**: 一致するディレクトリパス
   - **例外**: `ValueError` - 指定名のディレクトリが見つからない場合

## 使用例

### 基本的な使用
```python
from scripts.paths_json import get_dirpath_sub_jsons, get_dirpath_sub_json_by_name

# すべてのJSONサブディレクトリを取得
subdirs = get_dirpath_sub_jsons()
print(f"Found {len(subdirs)} directories")

# 特定の名前でディレクトリを検索
pokemon_dir = get_dirpath_sub_json_by_name(subdirs, "pokemon")
```

### モジュール実行
```bash
python -m scripts.paths_json
```

## 出力例（モジュール実行時）
```
JSON directory path: /home/user/project/json
Found 8 JSON subdirectories:
   1. ability (/home/user/project/json/ability)
   2. move (/home/user/project/json/move)
   3. pokemon (/home/user/project/json/pokemon)
   4. pokemon_form (/home/user/project/json/pokemon_form)
   5. pokemon_species (/home/user/project/json/pokemon_species)
   6. type (/home/user/project/json/type)
   7. version (/home/user/project/json/version)
   8. version_group (/home/user/project/json/version_group)

JSON file counts:
  ability: 327 files
  move: 919 files
  pokemon: 1302 files
  pokemon_form: 2345 files
  pokemon_species: 1302 files
  type: 20 files
  version: 38 files
  version_group: 25 files

Test search for 'ability': /home/user/project/json/ability
```

## 依存関係
- `config.dirpath`: `JSON_DIR_PATH`
- 標準ライブラリ: `pathlib`, `typing`

## 用途分析

### 実際の用途
1. **ディレクトリ探索**: JSON構造の動的探索
2. **パス解決**: 名前ベースでのディレクトリアクセス
3. **バリデーション**: ディレクトリ存在確認
4. **開発支援**: プロジェクト構造の可視化

### 使用箇所
- `json_mapping.py`: サブディレクトリ列挙
- `spf_mapping.py`: 特定ディレクトリアクセス（間接的）
- 手動実行: 構造確認・デバッグ

## 必要性評価

#### ✅ **必要性：中〜高**

**必要な理由**:
1. **抽象化**: ディレクトリ操作の共通インターフェース
2. **再利用性**: 複数箇所で使用される基本機能
3. **保守性**: ディレクトリ構造変更に対する耐性
4. **デバッグ支援**: 構造確認機能

**懸念点**:
1. **機能の限定性**: 比較的単純な機能
2. **pathlib重複**: 標準ライブラリで代替可能

## 代替案検討

### 1. 標準ライブラリ直接使用
```python
# 直接pathlibを使用
subdirs = [p for p in JSON_DIR_PATH.iterdir() if p.is_dir()]
target_dir = next((p for p in subdirs if p.name == "pokemon"), None)
```
**メリット**: 依存なし、シンプル
**デメリット**: コード重複、エラーハンドリング不足

### 2. クラスベース設計
```python
class JsonDirManager:
    def __init__(self, base_path: Path):
        self.base_path = base_path

    def list_subdirs(self) -> List[Path]:
        # ...

    def find_by_name(self, name: str) -> Path:
        # ...
```
**メリット**: 状態管理、機能拡張しやすい
**デメリット**: オーバーエンジニアリング

### 3. 設定ファイルベース
```yaml
# json_structure.yaml
directories:
  - name: pokemon
    path: pokemon
  - name: abilities
    path: ability
```
**メリット**: 設定可能、明示的
**デメリット**: 設定ファイル管理が必要

## パフォーマンス考慮

### 現在の実装
- **時間計算量**: O(n) - ディレクトリ数に比例
- **空間計算量**: O(n) - ディレクトリリストを保持
- **I/O**: ディレクトリスキャン1回

### 最適化案
1. **キャッシュ機能**: 結果をメモリに保持
2. **遅延評価**: 必要時のみスキャン
3. **非同期処理**: 大量ディレクトリでの並列処理

## 結論

**このファイルは必要**だが、**機能統合の余地あり**。

### 推奨事項
1. **現状維持**: 基本機能は有用で他モジュールが依存
2. **機能拡張**: エラーハンドリング、キャッシュ機能の追加
3. **統合検討**: 将来的に`json_mapping.py`と統合可能

### 削除リスク
- `json_mapping.py`の動作に影響
- 手動デバッグ機能の喪失
- 将来の機能拡張における基盤の損失

**総合評価**: **保持推奨** - シンプルだが重要な基盤機能
