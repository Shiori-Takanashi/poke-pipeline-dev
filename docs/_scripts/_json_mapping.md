# json_mapping.py

## 概要
JSONディレクトリ内のサブディレクトリから、各ディレクトリ内のJSONファイルのマッピング辞書を生成し、Pythonファイルとして出力するクラス。

## 主要機能

### JsonPathExporter クラス
JSONファイルのパスマッピングを生成・エクスポートするクラス。

#### メソッド詳細

1. **`__init__(output_subdir: str | None = None)`**
   - 出力先ディレクトリを設定
   - `output_subdir`が指定された場合：`META_DIR_PATH / output_subdir`
   - 未指定の場合：`META_DIR_PATH`直下

2. **`make_path_index(dir_path: Path) -> dict[str, str]`**
   - 指定されたディレクトリ内の`.json`ファイルをスキャン
   - ファイル名（拡張子なし）をキー、ファイル名をバリューとする辞書を生成
   - 例：`{"00001": "00001.json", "00002": "00002.json"}`

3. **`write_index_to_file(data: dict, label: str) -> None`**
   - 辞書データをPythonファイルとして書き出し
   - ラベルから定数名を生成（ハイフンをアンダースコアに変換し大文字化）
   - 例：`pokemon-species` → `POKEMON_SPECIES`

4. **`process(dir_paths: list[Path]) -> None`**
   - 複数のディレクトリを一括処理
   - 各ディレクトリのマッピングを生成し、個別のPythonファイルとして出力

## 使用例

### 直接実行
```bash
python -m scripts.json_mapping
```

### プログラマティック使用
```python
from scripts.json_mapping import JsonPathExporter

# デフォルト出力先（meta/直下）
exporter = JsonPathExporter()

# サブディレクトリ指定
exporter = JsonPathExporter("constants")

# 処理実行
json_subdirs = get_dirpath_sub_jsons()
exporter.process(json_subdirs)
```

## 出力例
```python
# meta/pokemon.py
POKEMON = {
    "00001": "00001.json",
    "00002": "00002.json",
    "00003": "00003.json"
}
```

## 依存関係
- `config.dirpath`: `META_DIR_PATH`, `JSON_DIR_PATH`
- `scripts.paths_json`: `get_dirpath_sub_jsons`

## 用途分析

### 実際の用途
1. **定数ファイル生成**: JSONファイルのマッピング辞書をPython定数として生成
2. **開発支援**: 手動でのファイル名管理を自動化
3. **データアクセス最適化**: ファイル名による高速アクセス

### 必要性評価

#### ⚠️ **必要性：中（要再検討）**
- **問題点1**: `target.py`で既に定義済みの情報を重複生成
- **問題点2**: ディレクトリスキャンによる暗黙的な依存関係
- **問題点3**: 設定駆動型アプローチが存在する場合、静的ファイル生成の意義が薄い

#### 改善提案
1. **エラーハンドリング強化**: 不正なファイル名やアクセス権限エラーの処理
2. **設定可能性向上**: ファイル名パターンや出力形式のカスタマイズ
3. **増分更新**: 変更されたディレクトリのみ再処理
4. **target.py連携**: FETCHターゲット定義からの動的パス生成

## アーキテクチャ改善案：target.py連携

### ユーザー意見
現在の実装では、JSONディレクトリを直接スキャンしてマッピングを生成していますが、`config/target.py`で定義されている`FETCH_TARGET`や`MONSTER_TARGET`からパスを動的生成する方が設計として優れているのではないでしょうか。

具体的には：
- `target.py`の設定値（例：`"pokemon-species"`）
- `util/re_endpoint_name.py`の`rename_endpoint_name()`関数を使用
- ディレクトリ名への変換（例：`"pokemon-species"` → `"pokemon_species"`）
- `build_path()`のような汎用関数の導入

これにより、設定駆動型のより保守性の高いアーキテクチャになると考えられます。

### 技術的分析と推奨事項

#### ✅ **賛成：設定駆動型アプローチの利点**

**現在の問題点**:
1. **設定の重複**: `target.py`で定義済みなのに、ディレクトリスキャンで再発見
2. **一貫性の欠如**: エンドポイント名とディレクトリ名の変換ルールが暗黙的
3. **保守性**: 新しいターゲット追加時に複数箇所の変更が必要

**提案する改善アーキテクチャ**:

```python
from config.target import FETCH_TARGET
from util.re_endpoint_name import rename_endpoint_name

def build_path(endpoint_name: str, base_dir: Path = JSON_DIR_PATH) -> Path:
    """エンドポイント名からディレクトリパスを構築"""
    dir_name = rename_endpoint_name(endpoint_name)
    return base_dir / dir_name

def build_constant_name(endpoint_name: str) -> str:
    """エンドポイント名から定数名を構築"""
    return rename_endpoint_name(endpoint_name).upper()

class ConfigDrivenJsonPathExporter(JsonPathExporter):
    def __init__(self, targets: List[str] = None, output_subdir: str = None):
        super().__init__(output_subdir)
        self.targets = targets or FETCH_TARGET

    def process_from_targets(self) -> None:
        """設定されたターゲットからマッピングを生成"""
        for target in self.targets:
            dir_path = build_path(target)
            if dir_path.exists():
                path_index = self.make_path_index(dir_path)
                const_name = build_constant_name(target)
                self.write_index_to_file(path_index, target, const_name)
            else:
                print(f"Warning: Directory not found for target '{target}': {dir_path}")

    def write_index_to_file(self, data: dict, label: str, const_name: str = None) -> None:
        """改良版：定数名を明示的に指定可能"""
        if const_name is None:
            const_name = build_constant_name(label)

        output_path = self.output_dir / f"{rename_endpoint_name(label)}.py"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(f"{const_name} = ")
            json.dump(data, f, indent=4, ensure_ascii=False)
```

#### **実装例**

```python
# 新しい使用方法
if __name__ == "__main__":
    # FETCH_TARGET全体を処理
    exporter = ConfigDrivenJsonPathExporter()
    exporter.process_from_targets()

    # 特定のターゲットのみ処理
    monster_exporter = ConfigDrivenJsonPathExporter(targets=MONSTER_TARGET)
    monster_exporter.process_from_targets()

    # カスタムターゲット
    custom_exporter = ConfigDrivenJsonPathExporter(targets=["pokemon", "ability"])
    custom_exporter.process_from_targets()
```

#### **メリット**

1. **単一責任原則**: `target.py`が唯一の設定源
2. **DRY原則**: 重複する設定定義を排除
3. **型安全性**: 定義されたターゲットのみ処理
4. **拡張性**: 新しいターゲット追加が簡単
5. **テスタビリティ**: モックしやすい設計
6. **エラー検出**: 存在しないディレクトリの早期発見

#### **考慮事項**

1. **後方互換性**: 既存の`process()`メソッドとの併存
2. **パフォーマンス**: 個別ディレクトリチェックによる若干のオーバーヘッド
3. **複雑性**: シンプルな実装から若干複雑化

#### **段階的移行計画**

1. **Phase 1**: `build_path()`と`build_constant_name()`関数の追加
2. **Phase 2**: `ConfigDrivenJsonPathExporter`クラスの実装
3. **Phase 3**: 既存コードの段階的移行
4. **Phase 4**: 従来の`process()`メソッドの非推奨化

## 代替案検討

### 1. ✅ **推奨：設定駆動型動的ロード方式**
```python
from config.target import FETCH_TARGET
from util.re_endpoint_name import rename_endpoint_name

def get_files_for_target(target: str) -> Dict[str, str]:
    """target設定から動的にファイルマッピングを取得"""
    dir_name = rename_endpoint_name(target)
    dir_path = JSON_DIR_PATH / dir_name
    if not dir_path.exists():
        return {}
    return {f.stem: f.name for f in dir_path.glob("*.json")}

# 使用例
pokemon_files = get_files_for_target("pokemon")
species_files = get_files_for_target("pokemon-species")
```
**メリット**:
- 設定一元化、重複排除
- 実行時最新状態、静的ファイル不要
- target.py変更時の自動対応
**デメリット**:
- 実行時オーバーヘッド（軽微）
- IDEサポート不足（型ヒントで解決可能）

### 2. 静的ファイル生成方式（現行）
**メリット**: IDEサポート、実行時オーバーヘッドなし
**デメリット**: 設定重複、保守コスト、一貫性リスク

### 3. データベース方式
**メリット**: 高速クエリ、複雑な検索
**デメリット**: 過剰エンジニアリング、外部依存

## 結論

### 現在の評価
**このファイルの必要性は限定的**。`target.py`で設定管理されている環境では、静的ファイル生成よりも設定駆動型の動的アプローチが適している。

### 推奨方針
1. **最優先**: 設定駆動型動的ロード方式への移行
2. **段階移行**: 既存の静的ファイルを段階的に廃止
3. **最終目標**: `json_mapping.py`の完全な置き換えまたは大幅な簡素化

### 削除可能性
#### ⚠️ **将来的な削除候補**
- **条件**: 設定駆動型アプローチの完全実装後
- **影響**: `spf_mapping.py`等の依存先の修正が必要
- **代替**: `target.py`ベースの動的マッピング関数

**設定駆動型アプローチを採用すれば、このファイルは不要になる可能性が高い**。重複機能を排除し、よりクリーンなアーキテクチャを実現すべき。
