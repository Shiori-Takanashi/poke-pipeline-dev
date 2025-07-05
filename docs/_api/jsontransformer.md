# JsonTransformer

`JsonTransformer` クラスは、PokéAPIから取得したJSONデータに対して一連の変換処理を実行するためのクラスです。

## 概要

このクラスは、取得したJSONデータを以下の処理により扱いやすい形式に変換します：

1. **URL削除**: 不要なURLキーを削除
2. **名前の折りたたみ**: 名前のみを持つ辞書を文字列に変換
3. **単一辞書リストのアンラップ**: 単一要素のリストを辞書に変換
4. **言語フィルタリング**: 指定した言語のみを残す

## クラス初期化

```python
from src.extract.transform import JsonTransformer

transformer = JsonTransformer()
```

### 初期化パラメータ

- `strip_ignore_keys`: URL削除時に無視するキーのリスト（デフォルト: `["flavor_text_entries", "varieties"]`）
- `filter_ignore_keys`: 言語フィルタリング時に無視するキーのリスト（デフォルト: `["flavor_varieties"]`）

## メソッド

### strip_url(obj, under_varieties=False)

オブジェクトからURLキーを削除します。

**パラメータ:**
- `obj`: 変換対象のオブジェクト（dict, list, またはプリミティブ）
- `under_varieties`: varietiesキーの下位にいる場合のフラグ（デフォルト: `False`）

**戻り値:**
- URLキーが削除されたオブジェクト

**例:**
```python
data = {
    "name": "pikachu",
    "type": {
        "name": "electric",
        "url": "https://pokeapi.co/api/v2/type/13/"
    }
}

result = transformer.strip_url(data)
# {"name": "pikachu", "type": {"name": "electric"}}
```

### collapse_name(obj)

`name` キーのみを持つ辞書を文字列に変換します。

**パラメータ:**
- `obj`: 変換対象のオブジェクト

**戻り値:**
- 変換されたオブジェクト

**例:**
```python
data = {
    "type": {"name": "electric"},
    "species": {"name": "pikachu"}
}

result = transformer.collapse_name(data)
# {"type": "electric", "species": "pikachu"}
```

### unwrap_single_dict_list(obj)

単一の辞書のみを含むリストを辞書に展開します。

**パラメータ:**
- `obj`: 変換対象のオブジェクト

**戻り値:**
- 展開されたオブジェクト

**例:**
```python
data = {
    "stats": [{"base_stat": 35, "effort": 0}]
}

result = transformer.unwrap_single_dict_list(data)
# {"stats": {"base_stat": 35, "effort": 0}}
```

### filter_by_language(obj, allowed=("ja", "ja-Hrkt"))

指定した言語のみを残すフィルタリングを行います。

**パラメータ:**
- `obj`: 変換対象のオブジェクト
- `allowed`: 許可する言語コードのタプル（デフォルト: `("ja", "ja-Hrkt")`）

**戻り値:**
- フィルタリングされたオブジェクト

**例:**
```python
data = {
    "names": [
        {"language": {"name": "ja"}, "name": "ピカチュウ"},
        {"language": {"name": "en"}, "name": "Pikachu"},
        {"language": {"name": "fr"}, "name": "Pikachu"}
    ]
}

result = transformer.filter_by_language(data)
# {"names": [{"language": {"name": "ja"}, "name": "ピカチュウ"}]}
```

### all_transform(data)

すべての変換処理を順次実行します。

**パラメータ:**
- `data`: 変換対象のJSONデータ

**戻り値:**
- 全変換処理が適用されたデータ

**例:**
```python
raw_data = {
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

result = transformer.all_transform(raw_data)
# 変換後のクリーンなデータ
```

## 使用例

### 基本的な使用方法

```python
from src.extract.transform import JsonTransformer
from util.io_json import read_json, write_json

# トランスフォーマーの初期化
transformer = JsonTransformer()

# JSONファイルの読み込み
data = read_json("path/to/pokemon.json")

# 変換処理の実行
transformed_data = transformer.all_transform(data)

# 結果の保存
write_json(transformed_data, "path/to/transformed_pokemon.json")
```

### 個別メソッドの使用

```python
# 段階的な変換処理
data = read_json("path/to/pokemon.json")

# 1. URL削除
step1 = transformer.strip_url(data)

# 2. 名前の折りたたみ
step2 = transformer.collapse_name(step1)

# 3. 単一辞書リストのアンラップ
step3 = transformer.unwrap_single_dict_list(step2)

# 4. 言語フィルタリング
result = transformer.filter_by_language(step3, allowed=("ja", "ja-Hrkt"))
```

### カスタム設定での使用

```python
# カスタム設定でのインスタンス化
transformer = JsonTransformer()
transformer.strip_ignore_keys = ["custom_key"]
transformer.filter_ignore_keys = ["another_key"]

# 特定の言語のみを対象とする
result = transformer.filter_by_language(data, allowed=("en",))
```

## 処理の流れ

1. **strip_url**: 不要なURLフィールドを削除
2. **collapse_name**: 名前のみの辞書を文字列に変換
3. **unwrap_single_dict_list**: 単一要素リストを展開
4. **filter_by_language**: 言語フィルタリング

## 注意事項

- 変換処理は非破壊的です（元のデータは変更されません）
- 大きなデータセットの処理時はメモリ使用量に注意してください
- 言語フィルタリングは `language` キーを持つ辞書に対してのみ適用されます

## 関連項目

- [Usage](../usage.md#データ変換コマンド) - コマンドライン使用方法
- [Examples](../examples/basic.md#データ変換) - 使用例
- [Architecture](../architecture.md#extract-module) - 設計詳細
