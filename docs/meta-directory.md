# meta/ ディレクトリ解説

このディレクトリには、データ処理のためのメタデータや、エンドポイント間のマッピング情報が格納されています。

## ファイル一覧

### map_endpoints.json
API エンドポイント間の関連性をマッピングしたファイルです。

**想定内容:**
- エンドポイント名とURL の対応
- エンドポイント間の依存関係
- データ取得の優先順位
- エラー時の代替エンドポイント

**使用例:**
```json
{
  "pokemon": {
    "base_url": "https://pokeapi.co/api/v2/pokemon/",
    "dependencies": ["pokemon-species"],
    "priority": 2
  },
  "pokemon-species": {
    "base_url": "https://pokeapi.co/api/v2/pokemon-species/",
    "dependencies": [],
    "priority": 1
  }
}
```

### map_form.json
ポケモンのフォルム（姿）に関するマッピング情報です。

**想定内容:**
- フォルムIDと名前の対応
- フォルム変更条件
- フォルム固有のデータ
- 地方別フォルムの情報

**使用例:**
```json
{
  "alolan-forms": {
    "region": "alola",
    "pokemon": [
      {"original_id": 26, "form_id": 10100, "name": "pikachu-alola"},
      {"original_id": 37, "form_id": 10101, "name": "vulpix-alola"}
    ]
  }
}
```

### map_pokemon.json
ポケモン個体に関するマッピング情報です。

**想定内容:**
- ポケモンIDと名前の対応
- 図鑑番号とAPIでのIDの関連
- バージョン別の差異情報
- 特殊なポケモン（メガ進化等）の情報

**使用例:**
```json
{
  "id_mapping": {
    "1": {"name": "bulbasaur", "dex_number": 1},
    "25": {"name": "pikachu", "dex_number": 25},
    "10001": {"name": "deoxys-normal", "dex_number": 386}
  }
}
```

### map_species.json
ポケモン種族に関するマッピング情報です。

**想定内容:**
- 種族IDと名前の対応
- 進化チェーンの情報
- 世代別の登場情報
- 種族固有のデータ

**使用例:**
```json
{
  "evolution_chains": {
    "1": ["bulbasaur", "ivysaur", "venusaur"],
    "4": ["charmander", "charmeleon", "charizard"]
  },
  "generations": {
    "1": {"range": [1, 151], "region": "kanto"},
    "2": {"range": [152, 251], "region": "johto"}
  }
}
```

### map_spf.json
Species-Pokemon-Form（種族-ポケモン-フォルム）の関連をマッピングしたファイルです。

**想定内容:**
- 3つのエンティティ間の関連性
- データの階層構造
- 正規化のためのルール
- 変換テーブル

**使用例:**
```json
{
  "pikachu": {
    "species_id": 25,
    "pokemon_variants": [
      {"pokemon_id": 25, "form_id": null, "name": "pikachu"},
      {"pokemon_id": 10080, "form_id": 10080, "name": "pikachu-rock-star"},
      {"pokemon_id": 10081, "form_id": 10081, "name": "pikachu-belle"}
    ]
  }
}
```

## 活用方法

### データ整合性チェック
```python
from util.io_json import read_json

# マッピング情報の読み込み
endpoint_map = read_json("meta/map_endpoints.json")
pokemon_map = read_json("meta/map_pokemon.json")

# データの整合性確認
def validate_pokemon_data(pokemon_id):
    if str(pokemon_id) in pokemon_map["id_mapping"]:
        return True
    return False
```

### データ変換処理
```python
# SPFマッピングを使用した正規化
spf_map = read_json("meta/map_spf.json")

def normalize_pokemon_data(raw_data):
    species_name = raw_data["species"]["name"]
    if species_name in spf_map:
        mapping_info = spf_map[species_name]
        # 正規化処理...
```

### バッチ処理の制御
```python
# エンドポイントマップを使用した処理順序制御
endpoint_map = read_json("meta/map_endpoints.json")

def get_processing_order():
    endpoints = list(endpoint_map.keys())
    return sorted(endpoints, key=lambda x: endpoint_map[x]["priority"])
```

## 更新と保守

### マッピング情報の更新
1. **API仕様変更時**: エンドポイント情報の更新
2. **新データ追加時**: 新しいポケモン・フォルムの追加
3. **データ構造変更時**: マッピングルールの見直し

### バージョン管理
```json
{
  "metadata": {
    "version": "1.0.0",
    "last_updated": "2025-07-01",
    "api_version": "v2"
  },
  "mappings": {
    // マッピングデータ
  }
}
```

### 検証プロセス
```python
def validate_mapping_consistency():
    """マッピングファイル間の整合性チェック"""
    pokemon_map = read_json("meta/map_pokemon.json")
    species_map = read_json("meta/map_species.json")
    spf_map = read_json("meta/map_spf.json")

    # 整合性チェックロジック
    # ...
```

## 注意点

- **データ同期**: API更新時のマッピング情報更新
- **バックアップ**: 手動で作成したマッピング情報の保護
- **検証**: データ処理前のマッピング整合性確認
- **ドキュメント**: マッピングルールの明文化

## 設計原則

- **分離**: エンドポイント毎のマッピング分離
- **拡張性**: 新しいエンティティ追加への対応
- **可読性**: 人間が理解しやすい構造
- **自動化**: マッピング情報の自動生成機能
